# -*- coding: utf-8 -*-
"""titulo_cita.py -- {hoja: {numero: TITULO}} leido del rotulo de cada detalle.

Hace falta porque verif_citas solo sabe si el NUMERO existe.  "5/S5.20" existe
(TYPICAL WALL FRAMING CONNX) pero no es el detalle del bracing: el bracing vive
dentro de 1/S5.20.  Un numero que existe y no corresponde es el error peor,
porque pasa cualquier revision que solo compare numeros.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (por defecto, el directorio actual)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", _os_rutas.getcwd())
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import os, sys, json, collections, warnings
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cadena_detalles as CD
import verif_citas as VC

CACHE_T = f'{_TW}/titulos_detalle_cache.json'


def de_pagina(ws, rot):
    """{numero: titulo} de una pagina, con los dos formatos de rotulo del set."""
    out = {}
    # serie A: numero ARRIBA del rotulo de hoja; el titulo va a la derecha del numero
    hojas = [w for w in ws if w['text'].strip() == rot]
    nums = [w for w in ws if VC.NUM.match(w['text'].strip())]
    for h in hojas:
        for n in nums:
            dy = h['top'] - n['top']
            dx = abs((h['x0'] + h['x1']) / 2.0 - (n['x0'] + n['x1']) / 2.0)
            if 4 < dy < 30 and dx < 22:
                t = [w['text'] for w in ws
                     if abs(w['top'] - n['top']) < 26 and n['x1'] < w['x0'] < n['x1'] + 440]
                out.setdefault(int(n['text']), ' '.join(t)[:90].strip())
    # serie S: numero + titulo + escala en el mismo renglon
    filas = collections.defaultdict(list)
    for w in ws:
        filas[round(w['top'] / 6)].append(w)
    for g in filas.values():
        g = sorted(g, key=lambda w: w['x0'])
        if not VC.ESCALA.search(' '.join(w['text'] for w in g)):
            continue
        for j, w in enumerate(g):
            if not VC.NUM.match(w['text'].strip()):
                continue
            der = [x for x in g[j + 1:] if x['x0'] - w['x1'] < 500]
            tit = ' '.join(x['text'] for x in der)[:90].strip()
            if sum(1 for c in tit if c.isupper()) >= 6:
                out.setdefault(int(w['text']), tit)
    return out


def titulos(pags=None, rehacer=False):
    if os.path.exists(CACHE_T) and not rehacer and not pags:
        return json.load(open(CACHE_T, encoding='utf-8'))
    import pdfplumber
    warnings.filterwarnings('ignore')
    out = json.load(open(CACHE_T, encoding='utf-8')) if os.path.exists(CACHE_T) else {}
    cache = json.load(open(CD.CACHE, encoding='utf-8'))
    with pdfplumber.open(VC.PDF) as pdf:
        for i, pg in cache['paginas'].items():
            if pags is not None and int(i) not in pags:
                continue
            rot = (pg.get('rotulo') or '').strip()
            if not rot:
                continue
            d = out.setdefault(rot, {})
            for n, t in de_pagina(pdf.pages[int(i)].extract_words(x_tolerance=1.5) or [], rot).items():
                d.setdefault(str(n), t)
    json.dump(out, open(CACHE_T, 'w', encoding='utf-8'), indent=0, ensure_ascii=False)
    return out


if __name__ == '__main__':
    p = [int(a) for a in sys.argv[1:]] or None
    t = titulos(p)
    for h in sorted(t):
        for n in sorted(t[h], key=int):
            print('  %-8s %-3s  %s' % (h, n, t[h][n]))
