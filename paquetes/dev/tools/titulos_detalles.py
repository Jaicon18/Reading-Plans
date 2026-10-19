# -*- coding: utf-8 -*-
"""titulos_detalles.py -- el ROTULO de cada detalle, para poder triar los que faltan.

Un numero de detalle no dice nada; su titulo si. "6/A12.01" no alarma a nadie, pero
"PARTITION TYPE C1" dice de inmediato que se cuantifico un tipo sin abrir su detalle.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (antes fijas en /home/claude/boa)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", "/home/claude/boa")
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import os, sys, re, json, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verif_detalles as VD

NUM = re.compile(r'^\d{1,2}$')
CACHE_T = f'{_TW}/titulos_cache.json'


def de_pagina(pdf, idx, rot, quiero):
    ws = pdf.pages[idx].extract_words() or []
    out = {}
    for h in [w for w in ws if w['text'].strip() == rot]:
        for n in [w for w in ws if NUM.match(w['text'].strip())]:
            dy = h['top'] - n['top']
            dx = abs((h['x0'] + h['x1']) / 2 - (n['x0'] + n['x1']) / 2)
            if 4 < dy < 30 and dx < 22 and int(n['text']) in quiero:
                # el titulo va a la DERECHA de la burbuja, casi a la misma altura
                t = [w['text'] for w in ws
                     if abs(w['top'] - n['top']) < 26 and n['x1'] < w['x0'] < n['x1'] + 430]
                out[int(n['text'])] = re.sub(r'\s+', ' ', ' '.join(t)).strip()[:85]
    return out


def main():
    import pdfplumber, warnings
    warnings.filterwarnings('ignore')
    faltan, uni, cit = VD.verificar()
    pedir = {h: set(s) for h, s, _ in faltan}
    cache = json.load(open(VD.CACHE, encoding='utf-8'))
    pag_de = {}
    for i, pg in cache['paginas'].items():
        if pg.get('rotulo') and pg['rotulo'] in pedir and pg.get('burbujas', {}).get(pg['rotulo']):
            pag_de.setdefault(pg['rotulo'], int(i))
    res = collections.OrderedDict()
    with pdfplumber.open(VD.PDF) as pdf:
        for h in sorted(pedir):
            if h not in pag_de:
                res[h] = {'_': 'pagina no cacheada'}
                continue
            res[h] = de_pagina(pdf, pag_de[h], h, pedir[h])
    json.dump(res, open(CACHE_T, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for h, d in res.items():
        print('===', h, '(pagina %s)' % pag_de.get(h))
        for k in sorted(d, key=lambda x: (isinstance(x, str), x)):
            print('   %-4s %s' % (k, d[k]))
    return res


if __name__ == '__main__':
    main()
