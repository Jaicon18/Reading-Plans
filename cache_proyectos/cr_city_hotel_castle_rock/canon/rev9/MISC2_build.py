#!/usr/bin/env python3
"""rev9 MISC2: L4 412 Corridor (field ceiling) = contorno de contornos_L4L1.json (A2.04) menos paneles WS-1 medidos en 1/A3.04 (offset L4 13.2/18.7)."""
import sys, json, importlib.util
sys.path.insert(0, '/root/cr/work/etapas/4_canon/rev9')
W = '/root/cr/work'
spec = importlib.util.spec_from_file_location('mb', f'{W}/etapas/4_canon/rev9/MISC_build.py')
src = open(f'{W}/etapas/4_canon/rev9/MISC_build.py').read()
# reutiliza solo las funciones (rect, img, sarea, orient, pip, keyhole)
ns = {}
exec(src.split('R = {}')[0], ns)
exec('\n'.join(l for l in src.split('# =============== PASADA 2')[1].split('K2 = {')[0].splitlines()[1:]), ns)
rect, img, sarea, orient, keyhole = ns['rect'], ns['img'], ns['sarea'], ns['orient'], ns['keyhole']
K = 'L4 412 Corridor (field ceiling)'
C = json.load(open(f'{W}/etapas/4_canon/rev9/contornos_L4L1.json'))[K]['polygon']
dx, dy = 13.2, 18.7
WSr = {'WS-1 medio (junto a Stair 1)': (821.52, 670.32, 857.04, 749.04),
       'WS-1 lobby ascensor S (tag CORRIDOR 412)': (732.24, 1035.6, 857.04, 1082.52),
       'WS-1 tramo E-W': (1217.76, 1239.96, 1296.48, 1281.0)}
ws = {n: rect(x0 - dx, y0 - dy, x1 - dx, y1 - dy) for n, (x0, y0, x1, y1) in WSr.items()}
ring = keyhole(C, list(ws.values()))
Ac, Aw, Ar = abs(sarea(C)) / 81, sum(abs(sarea(P)) for P in ws.values()) / 81, abs(sarea(ring)) / 81
print(f'contorno {Ac:.2f}  WS-1 {Aw:.2f}  contorno-WS1 {Ac - Aw:.2f}  shoelace(anillo) {Ar:.2f}')
assert abs(Ar - (Ac - Aw)) < 0.01
fn = img('A2.04', 'L4-412_field_final', (690, 430, 1500, 1290), red=[ring], blue=list(ws.values()),
         txt=f'L4 412 field {Ar:.2f} SF = {Ac:.2f} - WS-1 {Aw:.2f} (azul)')
fn2 = img('A3.04', 'L4-412_WS1_A304', (700, 640, 1310, 1300), blue=[rect(*v) for v in WSr.values()], txt='WS-1 en 1/A3.04 (marco exterior)')
out = {K: {'sheet': 'A2.04', 'polygon': ring, 'area_sf': round(Ar, 2), 'contorno_sf': round(Ac, 2), 'ws1_sf': round(Aw, 2),
           'ws1': list(ws.values()),
           'ws1_detalle': {n: {'rcp_A3.04': list(v), 'sf': round((v[2] - v[0]) * (v[3] - v[1]) / 81, 2)} for n, v in WSr.items()},
           'nhoja': '1/A2.04 (WS-1 en 1/A3.04; 3/A7.23 y 3/A7.24)', 'img': fn, 'img_ws1_rcp': fn2,
           'metodo': 'anillo único keyhole: contorno de contornos_L4L1.json (caras A2.04) con los 3 paneles WS-1 como huecos (puente de ancho cero, '
                     'recorridos en sentido inverso). Paneles = marco exterior dibujado en 1/A3.04 (la leyenda WS-1 incluye los bordes de millwork), '
                     f'trasladados a A2.04 con (-{dx}, -{dy}).',
           'nota': f'WS-1 medido {Aw:.2f} SF contra 134.6 del source: medio 34.52 (3.95 x 8.75 ft), E-W 39.88 (8.75 x 4.56), lobby 72.29 '
                   '(13.87 x 5.21 ft incluyendo el marco doble; solo la zona de listones da 13.12 x 4.47 = 58.6).'}}
json.dump(out, open(f'{W}/etapas/4_canon/rev9/contornos_MISC2.json', 'w'), indent=1)
