# -*- coding: utf-8 -*-
"""cache_detalles.py -- barre el PDF UNA vez y guarda que detalle vive en que hoja.

Extraer palabras de un set completo tarda minutos; la compuerta tiene que correr en segundos o
nadie la corre. Se cachea por paginas, en tandas, y el cache se invalida solo si cambia el
PDF (se guarda su tamano y su mtime).
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (por defecto, el directorio actual)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", _os_rutas.getcwd())
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import os, sys, re, json, subprocess, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verif_detalles as VD

PDF = VD.PDF
CACHE = f'{_TW}/detalles_cache.json'

# Las hojas pesadas (elevaciones exteriores, planos de plomeria) tienen miles de objetos y
# pdfplumber tarda MINUTOS en cada una -- el 2-oct-2026 tres hojas bloquearon el cache por
# mas de 15 minutos. `pdftotext -bbox` da las mismas cajas de palabra en segundos. Es la
# misma regla que ya estaba escrita para arranque.py en sets grandes, aplicada aqui.
_W = re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">'
                r'([^<]*)</word>')


def palabras_rapidas(idx):
    """[{'text','x0','x1','top'}] de una pagina, por pdftotext -bbox (segundos, no minutos)."""
    r = subprocess.run(['pdftotext', '-f', str(idx + 1), '-l', str(idx + 1), '-bbox',
                        PDF, '-'], capture_output=True, text=True)
    out = []
    for x0, y0, x1, _y1, t in _W.findall(r.stdout or ''):
        t = (t.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
              .replace('&quot;', '"').replace('&apos;', "'")).strip()
        if t:
            out.append({'text': t, 'x0': float(x0), 'x1': float(x1), 'top': float(y0)})
    return out


def _burbujas(ws):
    hojas = [w for w in ws if VD.HOJA.match(w['text'])]
    nums = [w for w in ws if VD.NUM.match(w['text'])]
    out = collections.defaultdict(set)
    for h in hojas:
        for n in nums:
            dy = h['top'] - n['top']
            dx = abs((h['x0'] + h['x1']) / 2 - (n['x0'] + n['x1']) / 2)
            if 4 < dy < 30 and dx < 22:
                out[h['text']].add(int(n['text']))
    return out


ESCALA = re.compile(chr(40) + r'\d[^"]{0,12}"\s*=\s*\d+' + chr(39) + r'\s*-\s*\d+"|\bNTS\b|\bN\.T\.S\.' + chr(41))
ETIQ = re.compile(r'^(?:\d{1,2}|[A-Z])$')


def _titulos(ws, tol=9.0):
    """Detalles por su RENGLON DE TITULO: `11 PARAPET INFILL FRAMING  3/4" = 1'-0"`.

    La deteccion por BURBUJA (un numero encima de un numero de hoja) solo ve una de las dos
    formas en que un set rotula sus detalles. En la prueba <proyecto> las hojas estructurales
    (serie S5) y las secciones de muro (serie A09) no llevan burbuja dentro del dibujo: su
    inventario real es el renglon de titulo al pie de cada detalle. Con solo la burbuja, la
    compuerta daba 0 detalles en TODA la serie S -- justo donde esta el PARAPET INFILL
    FRAMING que se me escapo.

    Un renglon de titulo es: etiqueta corta (1-2 digitos o una letra) + titulo en mayusculas
    + escala. La escala es lo que lo separa de cualquier otro texto en mayusculas.
    """
    filas = collections.defaultdict(list)
    for w in ws:
        filas[round(w['top'] / tol)].append(w)
    out = set()
    for _k, fila in filas.items():
        fila.sort(key=lambda w: w['x0'])
        txt = ' '.join(w['text'] for w in fila)
        if not ESCALA.search(txt):
            continue
        for j, w in enumerate(fila):
            if not ETIQ.match(w['text']):
                continue
            sig = fila[j + 1] if j + 1 < len(fila) else None
            if not sig or not sig['text'][:1].isupper() or len(sig['text']) < 2:
                continue
            if 0 < sig['x0'] - w['x1'] < 40:
                out.add(w['text'])
    return out


def cachear_rapido(rotulos):
    """Cachea por pdftotext las paginas cuyo rotulo este en `rotulos`."""
    st = os.stat(PDF)
    d = {'pdf': [st.st_size, int(st.st_mtime)], 'paginas': {}}
    if os.path.exists(CACHE):
        viejo = json.load(open(CACHE, encoding='utf-8'))
        if viejo.get('pdf') == d['pdf']:
            d = viejo
    import pdfplumber, warnings
    warnings.filterwarnings('ignore')
    with pdfplumber.open(PDF) as pdf:
        n = len(pdf.pages)
    for i in range(n):
        if str(i) in d['paginas']:
            continue
        ws = palabras_rapidas(i)
        c = collections.Counter(w['text'] for w in ws if VD.HOJA.match(w['text']))
        rot = c.most_common(1)[0][0] if c else None
        if rot not in rotulos:
            continue
        bur = {h: set(v) for h, v in _burbujas(ws).items()}
        if rot:
            bur.setdefault(rot, set())
            bur[rot] |= {int(t) for t in _titulos(ws) if t.isdigit()}
        d['paginas'][str(i)] = {'rotulo': rot,
                                'burbujas': {h: sorted(v) for h, v in bur.items()},
                                'letras': sorted(t for t in _titulos(ws) if not t.isdigit())}
        json.dump(d, open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False)
        print('  pag %2d = %-8s  %d detalles' % (i, rot, len(d['paginas'][str(i)]['burbujas'].get(rot, []))))
    return d


def main(desde=0, hasta=None, lote=12):
    import pdfplumber, warnings
    warnings.filterwarnings('ignore')
    st = os.stat(PDF)
    d = {'pdf': [st.st_size, int(st.st_mtime)], 'paginas': {}}
    if os.path.exists(CACHE):
        viejo = json.load(open(CACHE, encoding='utf-8'))
        if viejo.get('pdf') == d['pdf']:
            d = viejo
    with pdfplumber.open(PDF) as pdf:
        n = len(pdf.pages)
        hasta = min(hasta if hasta is not None else n, n)
        hechas = 0
        for i in range(desde, hasta):
            if str(i) in d['paginas']:
                continue
            rot = VD.rotulo_de_pagina(pdf, i)
            bur = {h: sorted(v) for h, v in VD.burbujas_de(pdf, i).items()}
            d['paginas'][str(i)] = {'rotulo': rot, 'burbujas': bur}
            hechas += 1
            if hechas >= lote:
                break
    json.dump(d, open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False)
    print('cacheadas %d paginas nuevas | total en cache %d de %d'
          % (hechas, len(d['paginas']), n))
    return len(d['paginas']), n


if __name__ == '__main__':
    a = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    b = int(sys.argv[2]) if len(sys.argv) > 2 else None
    main(a, b)


def paginas(idxs):
    """Cachea SOLO las paginas que se le piden. El barrido completo del set tarda
    minutos; las hojas que el take-off usa de verdad son ~17."""
    import pdfplumber, warnings
    warnings.filterwarnings('ignore')
    st = os.stat(PDF)
    d = {'pdf': [st.st_size, int(st.st_mtime)], 'paginas': {}}
    if os.path.exists(CACHE):
        v = json.load(open(CACHE, encoding='utf-8'))
        if v.get('pdf') == d['pdf']:
            d = v
    with pdfplumber.open(PDF) as pdf:
        for i in idxs:
            if str(i) in d['paginas']:
                continue
            d['paginas'][str(i)] = {'rotulo': VD.rotulo_de_pagina(pdf, i),
                                    'burbujas': {h: sorted(x) for h, x
                                                 in VD.burbujas_de(pdf, i).items()}}
    json.dump(d, open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False)
    return d
