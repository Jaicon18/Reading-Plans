#!/usr/bin/env python3
"""CR City Hotel - sellos de closer.py + evidencia planmark.py sobre el canon resuelto (board-only + C-H).
closer: cada wall -> Val(largo) y Val(altura) con su estado (CONFIRMADO exige hoja citada; DERIVADO exige la operación;
PENDIENTE sin valor) y una Cara por face con su board y capas; un rechazo = rc 1 con la lista.
planmark: por hoja, cada wall como banda (H / V / D) desde su path -> verify (tinta del plano bajo cada marca; un wall sobre
papel en blanco = rechazo) + overview circulada etapas/7_imagenes/planmark_<hoja>_<piso>.png.
Salida: etapas/4_canon/out/sellos_evidencia.json"""
import json, sys, os, collections
sys.path.insert(0, '/root/skill/take-off-metal-frame-drywall/tools')
import closer
import planmark
W = '/root/cr/work'
c = json.load(open(f'{W}/etapas/4_canon/takeoff_canon.json'))
PDF = f'{W}/plans/bidset_SIN_MARKUPS.pdf'
res = {"closer": {"ok": 0, "rechazos": []}, "planmark": {}}
for n, w in enumerate(c['existing_walls'], 1):
    try:
        ls = w.get('length_status') or 'DERIVADO'
        st = 'CONFIRMADO' if ls.upper().startswith('CONF') else ('PENDIENTE' if ls.upper().startswith('PEND') else 'DERIVADO')
        closer.Val(w['length_ft'], st, fuente=w.get('source'), operacion=w.get('source'), unidad='ft')
        hs = w.get('height_status') or 'DERIVADO'
        closer.Val(w['height_ft'], hs, fuente=w.get('height_source'), operacion=w.get('height_source'), unidad='ft')
        wl = closer.Wall(n, w['type_id'], w.get('location') or w['id'])
        wl.caras.append(closer.Cara(w['id'], closer.Val(w['height_ft'], hs, fuente=w.get('height_source'), operacion=w.get('height_source')),
                                    w.get('board'), int(w.get('layers') or 1)))
        res['closer']['ok'] += 1
    except closer.CierreRechazado as e:
        res['closer']['rechazos'].append(f"{w['id']}: {e}")


def band(p):
    (x0, y0), (x1, y1) = p[0], p[-1]
    if abs(y1 - y0) <= 1.5:
        y = (y0 + y1) / 2
        return {"ori": "H", "lo": min(x0, x1), "hi": max(x0, x1), "c0": y - 2.5, "c1": y + 2.5}
    if abs(x1 - x0) <= 1.5:
        x = (x0 + x1) / 2
        return {"ori": "V", "lo": min(y0, y1), "hi": max(y0, y1), "c0": x - 2.5, "c1": x + 2.5}
    return {"ori": "D", "p0": [x0, y0], "p1": [x1, y1]}


grp = collections.defaultdict(dict)
for w in c['existing_walls']:
    k = w['id'].split(' ')[0]
    grp[(w['sheet'], w['page'], w['floor'])].setdefault(k, {"id": k, "band": band(w['path']), "lf": w['length_ft'], "tagged": bool(w.get('tag_ids'))})
os.makedirs(f'{W}/etapas/7_imagenes', exist_ok=True)
for (sh, pg, fl), its in sorted(grp.items()):
    h = planmark.Hoja(PDF, pg)
    items = list(its.values())
    try:
        r = h.verify(items)
        out = f'{W}/etapas/7_imagenes/planmark_{sh}_{fl}.png'
        h.overview(items, f"{sh} {fl} - board-only walls (blue tagged / red untagged)", out)
        res['planmark'][f'{sh} {fl}'] = {"walls": len(items), "verify_min_ink": min(x[1] for x in r), "img": out}
    except planmark.MarcaRechazada as e:
        res['planmark'][f'{sh} {fl}'] = {"walls": len(items), "rechazo": str(e)[:400]}
json.dump(res, open(f'{W}/etapas/4_canon/out/sellos_evidencia.json', 'w'), indent=1)
print('closer ok', res['closer']['ok'], 'rechazos', len(res['closer']['rechazos']))
for x in res['closer']['rechazos'][:10]:
    print('  ', x[:200])
for k, v in res['planmark'].items():
    print('planmark', k, v.get('walls'), v.get('verify_min_ink'), v.get('rechazo', '')[:200])
sys.exit(1 if res['closer']['rechazos'] or any('rechazo' in v for v in res['planmark'].values()) else 0)
