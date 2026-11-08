#!/usr/bin/env python3
"""rev9 (COORDINACIÓN 7-nov, candidatos #19 / #30 de A2.01): FACP 125 (L1, al este de Stair 2, entre N.1 y P) no tenía ninguna cara.
1/A6.02 'ENLARGED PLAN - SOUTHEAST STAIR - LVL 1' (18 pt/ft): norte = CMU con tag 'FI.2 | 0' (A0.06 FI.2-0: 1 layer 5/8" Type X del lado
del cuarto sobre rigid insulation) -> cara FACP y = 1324.8 de x 1383.0 a 1441.6; este = 'XM.0.1 | 2' (finish '.1 NO FINISH' de la leyenda
de materiales, A0.07): sin gypsum; oeste = muro E de Stair 2 'CM.8 | 2' (CMU, sin board). Sur (grid 14): 1/A2.01 dibuja la misma línea
de furring que FI.2-L1-06 (FI.2-0) en y 1285.1 de x 1653.5 a 1691.9, pero 1/A6.02 no la etiqueta -> en el base (opción mayor) con RFI-26 /
DA-5. Altura: 12'-0" B.O. DECK (5/A5.04), como FI.2-L1-06 (el cuarto está bajo el piso de L2, no dentro de la escalera)."""
import json
W = '/root/cr/work'
CP = f'{W}/etapas/4_canon/takeoff_canon.json'
c = json.load(open(CP))
HS = list(json.load(open(f'{W}/set_texto.json'))['hojas'])
base = next(w for w in c['existing_walls'] if w['id'] == 'FI.2-L1-06')
ya = {w['id'] for w in c['existing_walls']}
nuevos = [
    ("FI.2-L1-11", "A6.02", [[1383.0, 1324.8], [1441.6, 1324.8]], 18.0,
     "L1 FACP 125 north wall, furring on CMU (1/A6.02) | faces: FACP 125",
     "1/A6.02; A6.02 [DERIVED] length (1/A6.02 vector at 18 pt/ft: FACP face of the north CMU band y 1313.4/1324.8 from the Stair 2 east wall face x 1383.0 to the grid-P wall face x 1441.6 = 58.6/18 = 3.26) | height: ",
     "tag 'FI.2 | 0' on 1/A6.02 -> FI.2-0 (A0.06: 1 layer 5/8\" Type X room side over rigid insulation)"),
    ("FI.2-L1-12", "A2.01", [[1653.5, 1285.1], [1691.9, 1285.1]], 9.0,
     "L1 FACP 125 south wall (grid 14), furring on CMU [RFI-26] | faces: FACP 125",
     "1/A2.01; A2.01 [DERIVED] length (1/A2.01 vector at 9 pt/ft: FACP 125 face of the grid-14 CMU wall, furring line y 1285.1 (pair sep 8.7) from 1653.5 to 1691.9 = 38.4/9 = 4.27) | height: ",
     "untagged on 1/A6.02; same furring graphic as FI.2-L1-06 (FI.2-0) on the same grid-14 wall -> FI.2-0 in the base (larger option), RFI-26 / DA-5"),
]
for nid, sh, path, esc, loc, src, tipo in nuevos:
    if nid in ya:
        continue
    nw = json.loads(json.dumps(base))
    L = round((path[1][0] - path[0][0]) / esc, 2)
    nw.update({"id": nid, "sheet": sh, "page": HS.index(sh) + 1, "path": path, "length_ft": L, "faces": 1, "layers": 1,
               "location": loc, "tag_ids": [], "img": None, "img_lectura": None, "keynote": sh,
               "source": src + base['height_source'] + f" | type: {tipo} | detail: 1/{sh}"})
    for k in ('faces_none_reason', 'door_openings', 'paths'):
        nw.pop(k, None)
    c['existing_walls'].insert(c['existing_walls'].index(base) + 1, nw)
    print(nid, L)
c.setdefault('excluded_walls', []).append({"id": "XM.0.1-L1-FACP", "reader": "AB", "floor": "L1", "sheet": "A6.02", "tag_ids": [],
    "reason": "FACP 125 east wall (grid P) 'XM.0.1 | 2' on 1/A6.02: exterior masonry with finish '.1 NO FINISH' (A0.07 finish materials legend) - no gypsum board"})
da = c.setdefault('deduct_alternates', [])
if not any(d.get('id') == 'DA-5' for d in da):
    sf = round(4.27 * float(base['height_ft']), 2)
    da.append({"id": "DA-5", "rfi": "RFI-26", "texto": "FACP 125 south wall (grid 14) without furring: FI.2-L1-12 out", "delta_sf": -sf, "material": "5/8\" Type X"})
json.dump(c, open(CP, 'w'), indent=1)
