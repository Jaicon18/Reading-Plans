#!/usr/bin/env python3
"""rev8 (COORDINACIÓN 7-nov, revisión de TODOS los walls, punto 2): el markup de un wall sigue la geometría MEDIDA (cada
tramo / jog = su segmento), nunca una recta del LF total puesta desde un punto. Corre después de rev6_auditoria.py.
 (a) walls medidos en piezas o con jog: `paths` = las piezas con las coordenadas impresas en su operación (Source), en la hoja
     donde se midieron;
 (b) barrido: un wall de un solo tramo recto cuya operación da UNA cota '(hi - lo)/esc = LF' en la MISMA hoja y escala, y
     cuyo path tiene ese largo pero corrido (> 1.5 pt) -> el path va a [lo, hi] medido.
Salida: canon en su lugar + etapas/4_canon/out/rev8_walls.json."""
import json, re, math
W = '/root/cr/work'
CP = f'{W}/etapas/4_canon/takeoff_canon.json'
c = json.load(open(CP))
HS = list(json.load(open(f'{W}/set_texto.json'))['hojas'])
SC = {k: (v['value'] if isinstance(v, dict) else v) for k, v in c['constants']['plan_scale_by_sheet'].items()}
MAN = {   # id base: (hoja, [piezas], nota)  — coordenadas de la operación impresa del Source, leídas en vectores
    "W.6-L4-12": ("A7.55", [[[1246.8, 1122.4], [1246.8, 1240.3]], [[1251.8, 1235.25], [1270.1, 1235.25]]],
                  "1/A7.55 x 1241.8/1251.8 from 1122.4 to 1240.3 + jog 1251.8-1270.1 at the 1230.2/1240.3 lines"),
    "W.6-L4-14": ("A7.55", [[[1372.65, 1122.4], [1372.65, 1383.4]], [[1349.5, 1379.15], [1367.6, 1379.15]]],
                  "1/A7.55 x 1367.6/1377.7 from 1122.4 to 1383.4 + jog 1349.5-1367.6 at the 1374.1/1384.2 lines"),
    "FW.4-L4-15": ("A6.01", [[[407.8, 1119.4], [407.8, 1101.4], [477.0, 1101.4], [477.0, 1122.6]]],
                   "7/A6.01 FEC box: west jog x 407.8 1101.4-1119.4, top y 1101.4 407.8-477.0, east side x 477.0 1101.4-1122.6"),
    "FW.2-L4-07": ("A6.01", [[[298.0, 1119.4], [317.9, 1119.4]], [[374.8, 1119.4], [407.8, 1119.4]]],
                   "7/A6.01 y 1119.4: west of the door 298.0-317.9 and east of the door 374.8-407.8"),
    "FW.2-L2-09": ("A2.02", [[[709.9, 623.6], [719.6, 623.6]], [[747.4, 623.6], [764.5, 623.6]]],
                   "1/A2.02 two furring pieces either side of the stair door 216.1 (709.9-719.6 and 747.4-764.5)"),
    "FW.2-L4-01": ("A6.00", [[[408.2, 135.9], [426.5, 135.9]], [[490.2, 135.9], [502.7, 135.9]]],
                   "5/A6.00 408.2-426.5 and 490.2-502.7 (entrance 426.5-490.2 open)"),
    "FW.2-L2-02": ("A2.02", [[[798.0, 457.4], [798.0, 523.2]]], "1/A2.02 hatched furring 457.4-523.2"),
    "FW.2-L4-04": ("A2.04", [[[704.45, 624.4], [704.45, 787.3]]], "A2.04 624.4-787.3 (= 7/A6.01 x 286.0 1122.6-1448.4)"),
    "W.62-L4-07": ("A2.04", [[[852.7, 1209.0], [1248.1, 1209.0]]], "A2.04 corridor face 852.7-1248.1 (operation)"),
    "FW.2-L2-13": ("A2.02", [[[1654.6, 1186.6], [1654.6, 1188.7]], [[1654.6, 1193.9], [1654.6, 1267.8]]],
                   "1/A2.02 furring face: 209 closet 1186.6-1188.7 and shower 1193.9-1267.8 (W.6-L2-01 1188.7-1193.9 interrupts)"),
    "CH.6-L4-01": ("A7.50", None, "3/A7.50 centerline N wall 1008.5 to S wall 1051.8"),
    "CH.6-L4-03": ("A7.50", None, "3/A7.50 centerline N wall 1008.5 to S wall 1051.8"),
}
LOG = []
for w in c['walls'] + c['existing_walls']:
    b = w['id'].split(' ')[0]
    if b not in MAN or 'cement' in str(w.get('board', '')):
        continue
    hoja, piezas, nota = MAN[b]
    if piezas is None:                       # CH: mismo eje, corrido -0.5 ft
        (x0, _), (x1, _) = w['path'][0], w['path'][-1]
        piezas = [[[x0, 1008.5], [x1, 1051.8]]]
    L = sum(math.dist(p[i], p[i + 1]) for p in piezas for i in range(len(p) - 1)) / SC[hoja]
    assert abs(L - w['length_ft']) <= 0.1, (w['id'], L, w['length_ft'])
    if abs(L - w['length_ft']) > 0.02:       # la suma de la operación impresa no daba el LF cargado (W.6-L4-14: 14.50 + 1.01 = 15.51, no 15.54)
        LOG.append({"id": w['id'], "lf_corregido": [w['length_ft'], round(L, 2)]})
        w['source'] = w['source'].replace(f"-> {w['length_ft']})", f"-> {round(L, 2)}) [261.0/18 + 18.1/18 = {round(L, 2)}; the sum printed before was {w['length_ft']}]", 1)
        w['length_ft'] = round(L, 2)
    antes = (w['sheet'], w['path'])
    w['sheet'], w['page'] = hoja, HS.index(hoja) + 1
    w['path'] = piezas[0]
    if len(piezas) > 1:
        w['paths'] = piezas
    w['geometry_note'] = f"markup = measured pieces: {nota}"
    LOG.append({"id": w['id'], "antes": antes, "despues": (hoja, piezas), "lf": w['length_ft']})
RX = re.compile(r"\((\d+\.?\d*)\s*-\s*(\d+\.?\d*)\)\s*/\s*(9|18)(?:\.0)?\s*=\s*(\d+\.?\d*)")
for w in c['walls'] + c['existing_walls']:
    if w['id'].split(' ')[0] in MAN or w.get('paths') or len(w.get('path') or []) != 2:
        continue
    t = RX.findall(str(w.get('source') or '').split(' | height')[0])
    if len(t) != 1:
        continue
    hi, lo, esc, val = float(t[0][0]), float(t[0][1]), float(t[0][2]), float(t[0][3])
    if SC.get(w['sheet']) != esc or abs(val - w['length_ft']) > 0.011:
        continue
    (ax, ay), (bx, by) = w['path']
    if abs(ay - by) < 0.3:
        eje, a_, b_ = 'x', min(ax, bx), max(ax, bx)
    elif abs(ax - bx) < 0.3:
        eje, a_, b_ = 'y', min(ay, by), max(ay, by)
    else:
        continue
    lo, hi = min(lo, hi), max(lo, hi)
    if abs((b_ - a_) - (hi - lo)) > 0.6 or not (1.5 < abs(a_ - lo) < 40):
        continue
    antes = list(w['path'])
    w['path'] = [[lo, ay], [hi, ay]] if eje == 'x' else [[ax, lo], [ax, hi]]
    w['geometry_note'] = f"markup moved onto the measured run {lo}-{hi} of its operation (was shifted {round(a_ - lo, 1)} pt)"
    LOG.append({"id": w['id'], "antes": antes, "despues": w['path'], "corrido_pt": round(a_ - lo, 1)})
# ---- punto 3 (tags sin disposición, U-117): ligados a ojo (imágenes etapas/4_canon/img/rev8/tags_*.png)
TAGS = {"PC0170": "W.6-L1-08", "PC0171": "W.6-L1-08", "PC0172": "W.6-L1-07", "PC0175": "W.6-L1-07", "PC0173": "W.6-L1-11",
        "PC0174": "W.6-L1-11", "PC0177": "W.6-L1-04", "PC0184": "W.6-L1-01", "PC0188": "W.6-L1-02", "PC0185": "W.6-L1-03",
        "PC0011": "XW.6.2-L1-01", "PC0012": "XW.6.2-L1-01", "PC0013": "XW.6.2-L1-02", "PC0014": "XW.6.2-L1-02", "PC0010": "XW.6.2-L1-03"}
for w in c['walls'] + c['existing_walls']:
    b = w['id'].split(' ')[0]
    add = [t for t, wid in TAGS.items() if wid == b]
    if add and 'cement' not in str(w.get('board', '')):
        w['tag_ids'] = sorted(set((w.get('tag_ids') or []) + add))
        LOG.append({"id": w['id'], "tags": add})
for t in ("PC0186", "PC0187"):
    c.setdefault('tags_descartados', []).append({"id": t, "floor": "L1", "imagen": "4_canon/img/rev8/tags_A745.png",
        "motivo": "W.6.1 | 0 tag on a wall inside KITCHEN 100 (F&B): 'INTERIOR OF FOOD AND BEVERAGE SPACE IS NOT IN SCOPE OF THIS PERMIT' (1/A7.45)"})
# PC0176: wall en L junto a la traffic door (1/A7.30) que no estaba cargado; cara del bar 107 = F&B (fuera), cara del vestíbulo de los toilets = nuestra
base = next(w for w in c['existing_walls'] if w['id'] == 'W.6-L1-04')
if not any(w['id'] == 'W.6-L1-32' for w in c['existing_walls']):
    nw = json.loads(json.dumps(base))
    piezas = [[[1938.1, 373.6], [1938.1, 413.85], [1877.9, 413.85]]]
    L = round(((413.85 - 373.6) + (1938.1 - 1877.9)) / 18.0, 2)
    nw.update({"id": "W.6-L1-32", "path": piezas[0], "length_ft": L, "tag_ids": ["PC0176"], "faces": 1,
               "location": "L1 L-shaped wall at the bar 107 traffic door / lobby restrooms vestibule (1/A7.30) | faces: restrooms vestibule",
               "faces_none_reason": "other face (Bar 107, F&B) inside the Food & Beverage space: 'INTERIOR OF FOOD AND BEVERAGE SPACE IS NOT IN SCOPE OF THIS PERMIT' (1/A7.30; A7.45, A7.50, A7.55)", "board": "5/8 type X WR",
               "source": (f"1/A7.30; A7.30 [DERIVED] length (1/A7.30 vector at 18 pt/ft: vertical x 1933.0/1943.2 from 373.6 to the corner 413.85 "
                          f"(40.25 pt) + horizontal y 408.8/418.9 from 1877.9 to 1938.1 (60.2 pt) = 100.45/18 = {L}) | height: " + base['height_source'] +
                          " | type: tag W.6.1 with EMPTY rating box (PC0176) -> W.6-0 | detail: 1/A7.30"),
               "img": None, "img_lectura": None, "keynote": "1/A7.30"})
    nw.pop('board_sf', None)
    c['existing_walls'].insert(c['existing_walls'].index(base) + 1, nw)
    LOG.append({"id": "W.6-L1-32", "nuevo": L})
# DW.4-L4-04 B / C: el vértice oeste cae en el vano del muro perpendicular (x 858.7 sin línea entre 608.9 y 625.7): el wall llega a esa cara
for w in c['existing_walls']:
    if w['id'] in ('DW.4-L4-04 B', 'DW.4-L4-04 C'):
        w['markup_check_note'] = "west end at the face of the perpendicular wall, whose line is interrupted by its door opening (x 858.7, y 608.9-625.7 on A2.04)"
# ---- cielos punto C (COORDINACIÓN 7-nov): ninguna etiqueta 'CLG 0'-0"': altura impresa N/HOJA
for x in c['ceilings']:
    if x['room'] == 'L4 406 Cleaning' and not x.get('height_ft'):
        x['height_ft'] = 8.9375; x['height_status'] = 'CONFIRMADO'
        x['height_source'] = "1/A5.06 printed 8'-11 1/4\" LEVEL 4 to underside of roof framing: RS-1 board on resilient channel at the framing"
        x['source'] = x['source'].replace("[DERIVED] height None (not printed on A3.04; not a unit (unit GN1 n/a). Underside roof framing at 8.94 (1/A5.06) likely.)",
                                          "[CONFIRMED] height 8.9375 (1/A5.06 printed 8'-11 1/4\" LEVEL 4 to underside of roof framing; RS-1 on resilient channel)")
        LOG.append({"id": x['room'], "altura": 8.9375})
    if x['room'] == 'L2 Elec 221' and not x.get('height_ft'):
        x['height_ft'] = 9.885; x['height_status'] = 'DERIVADO'
        x['height_source'] = "DERIVADO: 11'-0\" (L2 6211.75' -> L3 6222.75') - 1'-1 3/8\" RATED ASSEMBLY (7/A7.23) = 9'-10 5/8\" (FS-1 membrane = bottom of the floor/ceiling assembly, as the rest of L2)"
        x['source'] = x['source'].replace("[DERIVED] height None (PENDIENTE: no ceiling tag on A3.02 / A7.09 for 221)",
                                          "[DERIVED] height 9.885 (11'-0\" - 1'-1 3/8\" RATED ASSEMBLY, 7/A7.23: FS-1 membrane = bottom of the floor/ceiling assembly)")
        LOG.append({"id": x['room'], "altura": 9.885})
json.dump(c, open(CP, 'w'), indent=1)
json.dump(LOG, open(f'{W}/etapas/4_canon/out/rev8_walls.json', 'w'), indent=1)
for l in LOG:
    print(l['id'], l.get('corrido_pt', ''), l.get('lf_corregido', ''), str(l.get('despues'))[:90])
