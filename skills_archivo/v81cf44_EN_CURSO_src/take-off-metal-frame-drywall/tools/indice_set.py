# -*- coding: utf-8 -*-
"""indice_set.py -- EL INDICE COMPLETO DEL BID SET, leido del propio PDF (PASO 0, regla v42).

Dos fuentes cotejadas una contra la otra:
  1. el DRAWING / SHEET INDEX impreso (la lista oficial de hojas del set);
  2. el TITLE BLOCK de cada pagina (el rotulo real: el texto MAS GRANDE con forma de numero de hoja).
El indice manda para el TITULO y el title block manda para QUE PAGINA del PDF es; donde se contradicen se DICE
en vez de elegir. Nunca se declara una hoja faltante sin barrer TODO el PDF por rotulo.

v73 (P05 de la prueba 21B): antes leia dos pickles que ninguna tool del paquete escribia y traia coordenadas fijas
de un set concreto (columna de numeros, fin de titulo, pagina del indice). Ahora:
  - `construir_cache(pdf)` arma el cache de palabras con pymupdf (todas las paginas) y el mapa de title blocks;
    `indice()` y las demas lo llaman solas si el cache no esta;
  - la pagina del indice es la que imprime "DRAWING INDEX" / "SHEET INDEX" (o la de mas numeros de hoja);
  - las columnas se detectan por la x de los numeros de hoja (sin constantes del proyecto): el titulo de cada
    numero son las palabras de su renglon a la derecha hasta la columna siguiente o un hueco > GAP_PT.
Uso: python3 indice_set.py <plano.pdf>   (cache en $TAKEOFF_WORK, por defecto el directorio actual)
"""
import collections
import os
import pickle
import re
import sys

_TW = os.environ.get("TAKEOFF_WORK", os.getcwd())
B = _TW
WORDS = os.path.join(B, '.words_titleblock.pkl')
MAPA = os.path.join(B, '.mapa_hojas.pkl')
PDF = None                       # ruta del set (main o construir_cache la fijan)
GAP_PT = 60.0                    # hueco que corta un titulo dentro de su renglon
SIZE_MIN = 20.0                  # el rotulo del title block va grande; las referencias internas, chicas

RE_HOJA = re.compile(r'^([A-Z]{1,2}-?\d{1,3}\.\d{1,2}|[A-Z]\d\.\d{1,2})$')
RE_NUM_TB = RE_HOJA
RE_REV = re.compile(r'^(.+?)\s+(\d{1,2}/\d{1,2}/\d{2,4})$')
RE_TIT_IDX = re.compile(r'\b(DRAWING|SHEET)\s+(INDEX|LIST)\b', re.I)


def _palabras_pagina(pg):
    """[{text, x0, x1, top, bottom, size}] en coordenadas de la pagina mostrada."""
    import pymupdf as fitz
    M = pg.rotation_matrix
    out = []
    d = pg.get_text("dict")
    for b in d.get("blocks", []):
        for ln in b.get("lines", []):
            for sp in ln.get("spans", []):
                txt = sp.get("text", "").strip()
                if not txt:
                    continue
                r = fitz.Rect(sp["bbox"]) * M
                # un span puede traer varias palabras: se reparten por ancho proporcional
                ws = txt.split()
                tot = sum(len(w) for w in ws) + len(ws) - 1
                x = r.x0
                for w in ws:
                    wd = (r.x1 - r.x0) * len(w) / max(tot, 1)
                    out.append({"text": w, "x0": x, "x1": x + wd, "top": r.y0, "bottom": r.y1,
                                "size": float(sp.get("size") or 0)})
                    x += wd + (r.x1 - r.x0) / max(tot, 1)
    return out


def construir_cache(pdf=None, dest=None):
    """Escribe .words_titleblock.pkl y .mapa_hojas.pkl (lo que antes nadie escribia). -> (WORDS, MAPA)."""
    import pymupdf as fitz
    global PDF
    pdf = pdf or PDF
    if not pdf:
        raise FileNotFoundError("indice_set: falta el PDF del set para armar el cache (pasar la ruta)")
    PDF = pdf
    dest = dest or B
    os.makedirs(dest, exist_ok=True)
    doc = fitz.open(pdf)
    DW = [{"i": i, "ws": _palabras_pagina(pg)} for i, pg in enumerate(doc)]
    pickle.dump(DW, open(os.path.join(dest, '.words_titleblock.pkl'), 'wb'))
    mapa = []
    for d in DW:
        h, sz = numero_de_title_block(d['ws'])
        tit = ''
        if h:
            w0 = next(w for w in d['ws'] if w['text'] == h and abs((w.get('size') or 0) - sz) < 0.01)
            cerca = [w for w in d['ws'] if w is not w0 and abs(w['top'] - w0['top']) < 120 and
                     abs(w['x0'] - w0['x0']) < 400 and (w.get('size') or 0) >= 8]
            tit = ' '.join(w['text'] for w in sorted(cerca, key=lambda w: (round(w['top']), w['x0'])))[:120]
        mapa.append({"page_index": d['i'], "hoja": h, "titulo": tit})
    pickle.dump(mapa, open(os.path.join(dest, '.mapa_hojas.pkl'), 'wb'))
    return os.path.join(dest, '.words_titleblock.pkl'), os.path.join(dest, '.mapa_hojas.pkl')


def _cargar(path):
    if not os.path.isfile(path):
        construir_cache()
    return pickle.load(open(path, 'rb'))


def _todas():
    return _cargar(WORDS)


def pagina_indice():
    """page_index de la hoja que imprime el DRAWING / SHEET INDEX (o la de mas numeros de hoja)."""
    DW = _todas()
    cands = []
    for d in DW:
        txt = ' '.join(w['text'] for w in d['ws'])
        n = sum(1 for w in d['ws'] if RE_HOJA.match(w['text']))
        cands.append((1 if RE_TIT_IDX.search(txt) else 0, n, -d['i'], d['i']))
    cands.sort(reverse=True)
    return cands[0][3] if cands else 0


def _words(i):
    return [x for x in _todas() if x['i'] == i][0]['ws']


def _columnas(nums):
    """x0 de cada columna de numeros de hoja (agrupa por x con tolerancia)."""
    xs = sorted(w['x0'] for w in nums)
    cols = []
    for x in xs:
        if cols and x - cols[-1][-1] <= 15:
            cols[-1].append(x)
        else:
            cols.append([x])
    return [sum(c) / len(c) for c in cols if len(c) >= 2]


def indice():
    """[(hoja, titulo)] del indice impreso, columna por columna, en el orden impreso."""
    ws = _words(pagina_indice())
    nums = [w for w in ws if RE_HOJA.match(w['text'])]
    cols = _columnas(nums)
    out = []
    for k, cx in enumerate(cols):
        sig = cols[k + 1] if k + 1 < len(cols) else float('inf')
        col = sorted([w for w in nums if abs(w['x0'] - cx) <= 15], key=lambda w: w['top'])
        for w in col:
            yc = (w['top'] + w['bottom']) / 2
            fila = sorted([x for x in ws if w['x1'] < x['x0'] < sig - 5 and
                           abs((x['top'] + x['bottom']) / 2 - yc) <= 4], key=lambda x: x['x0'])
            t, last = [], w['x1']
            for x in fila:
                if x['x0'] - last > GAP_PT:
                    break
                t.append(x['text'])
                last = x['x1']
            out.append((w['text'], ' '.join(t).strip()))
    return out


def revisiones():
    """[(descripcion, fecha)] de los renglones de la hoja del indice que terminan en fecha. La ULTIMA es la vigente."""
    ws = _words(pagina_indice())
    filas = collections.defaultdict(list)
    for w in ws:
        filas[round(((w['top'] + w['bottom']) / 2) / 4)].append(w)
    out = []
    for k in sorted(filas):
        seg, last = [], None
        for w in sorted(filas[k], key=lambda w: w['x0']) + [None]:
            if w is None or (last is not None and w['x0'] - last > GAP_PT):
                m = RE_REV.match(' '.join(seg).strip())
                if m:
                    out.append((m.group(1).strip(), m.group(2)))
                seg = []
            if w is not None:
                seg.append(w['text'])
                last = w['x1']
    return out


def paginas():
    """[(page_index, hoja_leida_del_title_block, titulo_leido)] de todas las paginas."""
    return [(x['page_index'], x['hoja'], x['titulo']) for x in _cargar(MAPA)]


def cotejo():
    """El indice y las paginas, cruzados, diciendo lo que NO cuadra. -> (filas, avisos)."""
    idx = indice()
    pag = paginas()
    donde = collections.defaultdict(list)
    for i, h, t in pag:
        if h:
            donde[h].append(i)
    filas, avisos = [], []
    for h, t in idx:
        ps = donde.get(h, [])
        if len(ps) == 1:
            estado = 'CONFIRMADO'
        elif not ps:
            estado = 'PENDIENTE'
            avisos.append('%s esta en el indice pero NINGUNA pagina la rotula en su title block con el lector '
                          'automatico; hay que abrirla antes de declararla faltante' % h)
        else:
            estado = 'PENDIENTE'
            avisos.append('%s sale rotulada en %d paginas (%s): abrirlas una por una'
                          % (h, len(ps), ', '.join(str(x + 1) for x in ps)))
        filas.append(dict(hoja=h, titulo=t, paginas=[p + 1 for p in ps], estado=estado))
    listadas = {h for h, _ in idx}
    for i, h, t in pag:
        if h and h not in listadas:
            avisos.append('la pagina %d se rotula %s y el indice no la lista' % (i + 1, h))
    sin = [i + 1 for i, h, t in pag if not h]
    if sin:
        avisos.append('%d paginas sin numero de hoja legible (paginas %s): quedan [PENDIENTE] de abrir; NO se '
                      'declaran faltantes.' % (len(sin), ', '.join(str(x) for x in sin)))
    return filas, avisos


def numero_de_title_block(ws):
    """(hoja, tamano) leido del title block: el token MAS GRANDE con forma de numero de hoja."""
    c = [((w.get('size') or 0), w['text']) for w in ws if RE_NUM_TB.match(w['text'])]
    c = [x for x in c if x[0] >= SIZE_MIN]
    if not c:
        return None, 0.0
    c.sort(reverse=True)
    return c[0][1], round(c[0][0], 2)


def paginas_por_tamano():
    """[(page_index, hoja, tamano)] de todas las paginas, con el detector por tamano."""
    out = []
    for d in sorted(_todas(), key=lambda x: x['i']):
        h, sz = numero_de_title_block(d['ws'])
        out.append((d['i'], h, sz))
    return out


def reconciliar():
    """Cuadra las paginas del PDF contra las hojas del indice, y DICE con que las cuadra."""
    idx = dict(indice())
    pag = paginas_por_tamano()
    donde = collections.defaultdict(list)
    for i, h, sz in pag:
        if h:
            donde[h].append(i + 1)
    sin = [i + 1 for i, h, sz in pag if not h]
    extra = {h: ps for h, ps in donde.items() if len(ps) > 1}
    falta = [h for h in idx if h not in donde]
    nolista = [h for h in donde if h not in idx]
    return dict(n_paginas=len(pag), n_indice=len(idx), donde=dict(donde), sin_numero=sin,
                duplicadas=extra, sin_pagina=falta, fuera_del_indice=nolista)


def civiles_por_posicion():
    """[(pagina, hoja, titulo)] DERIVADO por posicion: N paginas sin rotulo y exactamente N hojas del indice sin
    pagina, en el mismo orden. Nunca CONFIRMADO (nadie leyo esos title blocks); si no cuadra, no se asigna."""
    r = reconciliar()
    sin = r['sin_numero']
    falta = [h for h, _ in indice() if h in set(r['sin_pagina'])]
    if len(sin) != len(falta):
        return [], ('PENDIENTE: %d paginas sin rotulo contra %d hojas sin pagina -- la cuenta no cuadra, asi que '
                    'NO se asigna ninguna por posicion' % (len(sin), len(falta)))
    tit = dict(indice())
    return ([(p, h, tit.get(h, '')) for p, h in zip(sin, falta)],
            'DERIVADO por posicion: %d paginas sin rotulo legible y %d hojas del indice sin pagina, en el mismo '
            'orden del indice.' % (len(sin), len(falta)))


def main(argv):
    global PDF
    if len(argv) >= 2:
        PDF = argv[1]
        construir_cache(PDF)
    idx = indice()
    rev = revisiones()
    filas, avisos = cotejo()
    print('INDICE impreso (pagina %d): %d hojas' % (pagina_indice() + 1, len(idx)))
    print('paginas del PDF: %d' % len(paginas()))
    print('REVISIONES:')
    for a, b in rev:
        print('   %-42s %s' % (a, b))
    ok = sum(1 for f in filas if f['estado'] == 'CONFIRMADO')
    print('cruce indice <-> title block: %d CONFIRMADO, %d PENDIENTE' % (ok, len(filas) - ok))
    for a in avisos:
        print('   - %s' % a)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
