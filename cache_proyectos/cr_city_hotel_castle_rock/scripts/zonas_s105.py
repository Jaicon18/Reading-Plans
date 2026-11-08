#!/usr/bin/env python3
"""PUNTO 1 - rated walls de L4 hasta el UNDERSIDE OF ROOF SHEATHING (2/A0.10), row por row, con el peralte de SU zona del
roof framing (S1.05). Todo número pasa por closer.Val (estado + fuente / operación) y closer.r2 / closer.waste.
Lee el canon de rev4 (solo lectura). Escribe code/punto1.json y code/punto1.md."""
import json, re, sys, collections
sys.path.insert(0, '/root/skill/take-off-metal-frame-drywall/tools')
import closer
from closer import Val, r2, waste

CANON = '/root/cr/work/etapas/4_canon/takeoff_canon.json'
REG = json.load(open('/root/cr/work/etapas/4_canon/rev5/registro.json'))

# ---- peraltes del roof framing [CONFIRMADO, schedule de S1.05]
PERALTE = {
    'RT-1': Val(1.5, 'CONFIRMADO', fuente='S1.05 framing schedule: RT-1 / RTG 18" DEEP PRE-ENGINEERED TRUSSES', unidad='ft'),
    'RJ-1': Val(r2(11.875 / 12, 4), 'CONFIRMADO', fuente='S1.05 framing schedule: RJ-1 11 7/8" TJI 230 @ 16" O.C', unidad='ft'),
    'RJ-2': Val(r2(11.875 / 12, 4), 'CONFIRMADO', fuente='S1.05 framing schedule: RJ-2 11 7/8" TJI 230 @ 12" O.C', unidad='ft'),
    'RJ-3': Val(r2(9.5 / 12, 4), 'CONFIRMADO', fuente='S1.05 framing schedule: RJ-3 9 1/2" TJI 110 @ 16" O.C', unidad='ft'),
}
# ---- zonas en coordenadas de S1.05 (pt), de las líneas vectoriales del plano (no a ojo); prioridad = orden
ZONAS = [
    ('RJ-3', 'S1.05 box BP-3 / RJ-3 north (MSW-3 sides)', (880, 475, 961, 541)),
    ('RJ-3', 'S1.05 box elevator RB-7 / RJ-3 (MSW-1 sides)', (867, 635, 962, 810)),
    ('RJ-3', 'S1.05 box BP-3 / RJ-3 south (MSW-3 sides)', (867, 942, 962, 1026)),
    ('RJ-3', 'S1.05 stair opening RJ-3 (treads 962-1019)', (960, 1024, 1022, 1180)),
    ('RJ-2', 'S1.05 east block RJ-2 strip (west)', (1412, 1011, 1497, 1230)),
    ('RJ-1', 'S1.05 east block RJ-1 bays', (1497, 1011, 1774, 1204)),
    ('RJ-3', 'S1.05 east block MSW-1 box RJ-3', (1649, 1204, 1816, 1299)),
    ('RJ-2', 'S1.05 east block RJ-2 strip (east)', (1774, 1011, 1816, 1204)),
    ('RJ-3', 'S1.05 east block RJ-3 bay', (1816, 1011, 1929, 1299)),
]
DEFAULT = ('RT-1', 'S1.05 main block: RT-1 / RTG 18" trusses (all area not in an RJ zone)')
TOL = 6.0   # pt (0.67 ft a 1/8"): un row a menos de TOL del borde de una zona de otro peralte = frontera

def a_s105(sheet, x, y):
    if sheet == 'A7.50':
        dx, dy, _ = REG['A7.50->A2.04']; x, y = x * 0.5 + dx, y * 0.5 + dy
    elif sheet == 'A7.55':
        dx, dy, _ = REG['A7.55->A2.04']; x, y = x * 0.5 + dx, y * 0.5 + dy
    elif sheet != 'A2.04':
        raise SystemExit(f'hoja sin registro: {sheet}')
    return x + 162.8, y + 17.88       # A2.04 -> S1.05: offset de los grid bubbles (B, C, G, K / 0, 9, 10, 14)

def zona(x, y):
    for z, src, (x0, y0, x1, y1) in ZONAS:
        if x0 <= x <= x1 and y0 <= y <= y1:
            return z, src
    return DEFAULT

def frontera(x, y, z):
    for zz, src, (x0, y0, x1, y1) in ZONAS + [(DEFAULT[0], DEFAULT[1], (-1e9, -1e9, -1e9, -1e9))]:
        if zz == z or PERALTE[zz].v == PERALTE[z].v:
            continue
        if x0 - TOL <= x <= x1 + TOL and y0 - TOL <= y <= y1 + TOL:
            return zz
    if z != 'RT-1':   # dentro de una zona RJ pero a menos de TOL de su borde -> el campo RT-1
        for zz, src, (x0, y0, x1, y1) in ZONAS:
            if zz == z and x0 <= x <= x1 and y0 <= y <= y1 and min(x - x0, x1 - x, y - y0, y1 - y) < TOL:
                return 'RT-1'
    return None

c = json.load(open(CANON))
rows = [e for e in c['existing_walls'] if e['floor'] == 'L4' and abs(e['height_ft'] - 8.9375) < 1e-6
        and re.search(r'-[1-9]$', str(e['type_id'])) and not str(e['type_id']).startswith('XW')]
out, por_zona, por_mat = [], collections.defaultdict(float), collections.defaultdict(float)
N = 100
for e in rows:
    (x0, y0), (x1, y1) = e['path'][0], e['path'][-1]
    cnt = collections.Counter(); fr = set()
    for i in range(N):
        t = (i + 0.5) / N
        sx, sy = a_s105(e['sheet'], x0 + t * (x1 - x0), y0 + t * (y1 - y0))
        z, _ = zona(sx, sy); cnt[z] += 1
        f = frontera(sx, sy, z)
        if f:
            fr.add(f)
    L = Val(e['length_ft'], 'DERIVADO', operacion=f"rev4 row {e['id']} length (canon source: {str(e['source'])[:90]})", unidad='ft')
    caras, capas = e['faces'], e.get('layers') or 1
    mat = '5/8" Type X' if 'cement' in e['board'] else ('1" shaftliner' if 'shaftliner' in e['board'] else
                                                         ('5/8" Type X W.R.' if 'WR' in e['board'] else '5/8" Type X'))
    partes = []
    for z, n in sorted(cnt.items()):
        frac = n / N
        d = PERALTE[z]
        sf = r2(L.v * frac * caras * capas * d.v)
        v = Val(sf, 'DERIVADO', operacion=f"{L.v} ft x {r2(frac, 2)} (part of the run over {z}) x {caras} face(s) x {capas} layer(s) x {d.v} ft ({z} depth, {d.fuente}) = {sf}", unidad='SF')
        partes.append({'zona': z, 'frac': r2(frac, 2), 'peralte_ft': d.v, 'sf': v.as_dict()})
        por_zona[z] += sf; por_mat[mat] += sf
    # alternativa en frontera: todo el row con el peralte vecino
    alt = None
    if fr:
        zz = sorted(fr, key=lambda k: -PERALTE[k].v)[0]
        alt = {'zona_alt': zz, 'sf_alt': r2(L.v * caras * capas * PERALTE[zz].v)}
    out.append({'id': e['id'], 'type': e['type_id'], 'sheet': e['sheet'], 'board_row': e['board'], 'material_ext': mat,
                'lf': L.v, 'faces': caras, 'layers': capas, 'h_rev4': 8.9375, 'partes': partes,
                'delta_sf': r2(sum(p['sf']['v'] for p in partes)), 'frontera': alt,
                'note': 'cement board face: the extension above the tile is plain 5/8" Type X (rated layer), not cement board' if 'cement' in e['board'] else None})
tot = r2(sum(por_zona.values()))
TOT = Val(tot, 'DERIVADO', operacion=' + '.join(f"{z} {r2(v)}" for z, v in sorted(por_zona.items())) + f" = {tot}", unidad='SF')
mats = {m: waste(r2(v), 'BOARD') for m, v in sorted(por_mat.items())}
res = {'rows': out, 'n_rows': len(out), 'lf_cara_capa': r2(sum(r['lf'] * r['faces'] * r['layers'] for r in out)),
       'por_zona_sf': {z: r2(v) for z, v in sorted(por_zona.items())}, 'total': TOT.as_dict(), 'por_material': mats,
       'zonas': [{'zona': z, 'fuente': s, 'rect_S105': r} for z, s, r in ZONAS] + [{'zona': DEFAULT[0], 'fuente': DEFAULT[1]}],
       'peraltes': {k: v.as_dict() for k, v in PERALTE.items()},
       'registro': {'A2.04->S1.05': [162.8, 17.88, 'grid bubbles B/C/G/K and 0/9/10/14 on A2.04 vs S1.05 (same 1/8" scale)'],
                    'A7.50->A2.04': REG['A7.50->A2.04'] + ['image registration at the printed scale ratio 9/18; checked: shaft CH.6-L4-01..04 lands on the shaft box of S1.05'],
                    'A7.55->A2.04': REG['A7.55->A2.04'] + ['image registration at the printed scale ratio 9/18']}}
json.dump(res, open('/root/cr/work/etapas/4_canon/rev5/punto1_check.json', 'w'), indent=1)
print('rows', len(out), '| LF cara x capa', res['lf_cara_capa'], '| por zona', res['por_zona_sf'], '| total', tot)
print('por material', {m: (v['NETO'], v['COMPRA']) for m, v in mats.items()})
print('frontera', [(r['id'], r['frontera']) for r in out if r['frontera']])
