#!/usr/bin/env python3
"""CR City Hotel rev5 - decisiones del usuario sobre la revisión de código (carpeta 'Revision de codigo 2026-11-06').
Regla R80e.38-4: mientras un RFI está abierto, el BASE lleva la opción de MAYOR cantidad y la otra va como DEDUCT ALTERNATE.
Todo número por closer.Val / r2 (estado + operación). Corre en la cadena después de canon_extras (antes de imagenes_walls).
 1. L4 rated walls hasta el UNDERSIDE OF ROOF SHEATHING (2/A0.10; shafts 10/A9.03): los 54 rows de punto1.json,
    altura = 8.9375 + sum(frac x peralte de su zona S1.05). Caras de cement board: la extensión es 5/8" Type X (row aparte).
 2. ELEC/TELE 120 en 2 HR, 4 paredes (RFI-23).  3. DATA 118B en 2 HR (RFI-24).  4. FW.4-L4-19 1 HR, cara del bar (RFI-25).
 5. XW.6.6-2 (L4): 04/A9.05 remata el board interior en el top plate -> NO se carga (sin RFI).
Escribe canon['deduct_alternates'] y canon['rev5_cambios']."""
import json, sys, re, copy
sys.path.insert(0, '/root/skill/take-off-metal-frame-drywall/tools')
from closer import Val, r2
W = '/root/cr/work'
CP = f'{W}/etapas/4_canon/takeoff_canon.json'
c = json.load(open(CP))
if c.get('rev5_cambios'):
    print('ya aplicado'); raise SystemExit
P1 = json.load(open(f'{W}/etapas/4_canon/rev5/punto1.json'))
EW = c['existing_walls']; IDX = {e['id']: e for e in EW}
HEAD = ("2/A0.10 'FIRE PARTITIONS AND FIRE BARRIERS EXTEND TO UNDERSIDE OR ROOF SHEATHING' (UNRATED ROOF ASSEMBLY, A0.08 RS-1 no rating); "
        "CODE: IBC 2018 §707.5 / §708.4 (https://codes.iccsafe.org/content/IBC2018P6/chapter-7-fire-and-smoke-protection-features; verified in ICC 2026-11-06, _PUENTE_CLAUDE COD-001)")
cambios, ded = [], []

# ---------- 1. cabeza de los rated walls de L4 hasta el roof sheathing
assert len(P1['rows']) == 54
ext_sf = 0.0; dup_sf = 0.0
for r in P1['rows']:
    e = IDX.get(r['id'])
    assert e is not None and abs(e['length_ft'] - r['lf']) < 1e-6 and abs(e['height_ft'] - 8.9375) < 1e-6, r['id']
    add = round(sum(p['frac'] * p['peralte_ft'] for p in r['partes']), 6)
    zonas = ' + '.join(f"{p['frac']} x {p['peralte_ft']} ft ({p['zona']})" for p in r['partes'])
    v = Val(add, 'DERIVADO', operacion=f"roof framing depth over the run (S1.05 framing schedule and zones): {zonas} -> {add} ft", unidad='ft')
    if 'cement' in e['board']:
        # tile backer OVERLAY: the rated layers of this same face are their own row (Type X W.R., full length) and that row
        # already runs to the roof sheathing -> no extension here (a 5/8" strip above the tile would be counted twice)
        sib = [x for x in EW if x['id'].split(' ')[0] == e['id'].split(' ')[0] and x is not e and 'cement' not in x['board']
               and str(x['location']).split('faces:')[-1].strip() == str(e['location']).split('faces:')[-1].strip()]
        assert sib and all(x['length_ft'] >= e['length_ft'] for x in sib), ('cement overlay sin cara rated propia', e['id'])
        e['head_detail'] = (f"tile backer overlay up to the 8'-11 1/4\" line; the rated layers of this face ({', '.join(x['id'] for x in sib)}) "
                            f"run to the underside of the roof sheathing (2/A0.10)")
        sf = 0.0
        no_dup = r2(e['length_ft'] * v.v * e['faces'] * (e.get('layers') or 1))
        dup_sf += no_dup
    else:
        h0 = e['height_ft']; e['height_ft'] = round(h0 + v.v, 6); e['height_status'] = 'DERIVADO'
        e['height_source'] = (f"{v.operacion}; 8'-11 1/4\" (LEVEL 4 to underside of roof framing, 1/A5.06) + {v.v} = {e['height_ft']} ft to the underside of the roof sheathing; {HEAD}")
        e['height_note'] = e['height_source']; e['head_detail'] = '2/A0.10 to underside of roof sheathing' + ('; 10/A9.03 HEAD OF SHAFT (no top enclosure)' if str(e['type_id']).startswith('CH') else '')
        e['source'] = str(e['source']).split(' | height:')[0] + f" | height: {e['height_source']}"
        sf = r2(e['length_ft'] * v.v * e['faces'] * (e.get('layers') or 1))
    ext_sf += sf
cambios.append({'n': 1, 'que': 'L4 rated walls to the underside of the roof sheathing (2/A0.10, 10/A9.03)', 'rows': 54,
                'sf': Val(r2(ext_sf), 'DERIVADO', operacion=f"sum of the 49 rated-layer rows: length x faces x layers x depth over the run = {r2(ext_sf)}; the 5 cement-board overlay rows are not extended (their face's rated layers already are): {r2(dup_sf)} SF of the code-review figure was double counted", unidad='SF').as_dict(),
                'corregido_vs_revision': r2(dup_sf)})

def nuevo(base_id, nid, L, H, caras, capas, path, loc, src, tipo='W.6-2', board='5/8 type X'):
    b = IDX[base_id]
    nw = {k: copy.deepcopy(b[k]) for k in ('floor', 'sheet', 'page', 'decision', 'keynote', 'img', 'height_img', 'height_source', 'height_note', 'height_status')}
    nw.update({'id': nid, 'type_id': tipo, 'type': tipo.rsplit('-', 1)[0], 'path': path, 'length_ft': L.v, 'height_ft': H, 'faces': caras, 'layers': capas,
               'board': board, 'location': loc, 'source': src, 'tag_ids': [], 'length_status': 'DERIVADO'})
    EW.append(nw); IDX[nid] = nw
    return r2(L.v * H * caras * capas)

PT = 18.0
def seg(a, b, op):
    return Val(r2(abs(b - a) / PT), 'DERIVADO', operacion=f"{op}: ({b} - {a}) / {PT} pt/ft (1/A7.50 vector)", unidad='ft')
SRC2 = ("1/A7.50; A0.00 Code Summary 'ELECTRICAL AND IT ROOMS - 2 HR'; 1/A0.01 ELEC/TELE 120 '2HR FB'; CODE: IBC 2018 §707.1 / §707.5 "
        "(https://codes.iccsafe.org/content/IBC2018P6/chapter-7-fire-and-smoke-protection-features; verified in ICC 2026-11-06, _PUENTE_CLAUDE COD-001) - the 2 HR comes from the drawings (Table 509 does not rate electrical / IT rooms)")
# ---------- 2. ELEC/TELE 120: W y S a W.6-2 (2 layers por cara); E = tramo de W.6-L1-23, cara ELEC +1 layer y cara Retail 2 layers
s2 = 0.0
for wid in ('W.6-L1-24', 'W.6-L1-25'):
    e = IDX[wid]; e['type_id'] = 'W.6-2'; e['layers'] = 2
    e['source'] = str(e['source']) + f" | RFI-23 (base = larger option while the RFI is open): 2 HR per {SRC2}"
    s2 += r2(e['length_ft'] * e['height_ft'] * e['faces'] * 1)
Le = seg(1299.1, 1348.8, 'ELEC/TELE 120 east wall = W.6-L1-23 segment between W.6-L1-22 and W.6-L1-25')
s2 += nuevo('W.6-L1-23 B', 'W.6-L1-23 C', Le, 12.0, 1, 1, [[2022.5, 1299.1], [2022.5, 1348.8]],
            'L1 ELEC/TELE 120 east wall (segment of the staff-block east wall W.6-L1-23) | faces: ELEC/TELE 120 (2nd layer for 2 HR)',
            f"{SRC2}; [DERIVED] length {Le.operacion} = {Le.v} | height: 12'-0\" B.O. DECK printed on 5/A5.04")
s2 += nuevo('W.6-L1-23 B', 'W.6-L1-23 D', Le, 12.0, 1, 2, [[2022.5, 1299.1], [2022.5, 1348.8]],
            'L1 ELEC/TELE 120 east wall, Retail 124 side | faces: RETAIL 124 side of the 2 HR fire barrier (rated face stays in our scope, RFI-05 criterion)',
            f"{SRC2}; [DERIVED] length {Le.operacion} = {Le.v} | height: 12'-0\" B.O. DECK printed on 5/A5.04")
cambios.append({'n': 2, 'que': 'ELEC/TELE 120 2 HR on all 4 walls (S printed by door 120.1 90 MIN; W / E RFI-23)', 'sf': Val(r2(s2), 'DERIVADO', operacion='W.6-L1-24 50.16 + W.6-L1-25 192.24 + E ELEC 33.12 + E Retail 66.24', unidad='SF').as_dict()})
# rev10 (auditoría U-138, E2): A8.00 door 120.1 ELEC / TELE '90 MIN' + A8.00 'DOOR RATING REQUIREMENTS PER TABLE 716.1(2): FIRE WALLS AND
# FIRE BARRIERS HAVING 2HR RATING: 90 MIN' -> el muro que contiene la puerta (W.6-L1-25, sur) es 2 HR POR LO IMPRESO; DA-1 solo W y E.
_s25 = r2(IDX['W.6-L1-25']['length_ft'] * IDX['W.6-L1-25']['height_ft'] * IDX['W.6-L1-25']['faces'] * 1)
IDX['W.6-L1-25']['source'] = str(IDX['W.6-L1-25']['source']).replace("RFI-23 (base = larger option while the RFI is open): 2 HR per",
    "[CONFIRMED] 2 HR: A8.00 door schedule 120.1 ELEC / TELE '90 MIN' in this wall + A8.00 'DOOR RATING REQUIREMENTS PER TABLE 716.1(2)' + 'FIRE WALLS AND FIRE BARRIES HAVING 2HR RATING: 90 MIN'; also")
ded.append({'id': 'DA-1', 'rfi': 'RFI-23', 'texto': 'ELEC/TELE 120 W and E walls as tagged on 1/A7.50 (rated 0); N 2 HR and S 2 HR (door 120.1 90 MIN, A8.00) stay', 'delta_sf': -r2(s2 - _s25), 'material': '5/8" Type X'})
# ---------- 3. DATA 118B 2 HR completo
Lw = seg(1188.6, 1293.04, 'DATA 118B west wall = W.6-L1-20 segment (Data part)')
Lx = seg(1188.6, 1299.1, 'DATA 118B east wall = W.6-L1-23 segment')
SRC3 = SRC2.replace("1/A0.01 ELEC/TELE 120 '2HR FB'", "IT room DATA 118B (N and S walls already W.6-2 on 1/A7.50)")
s3 = nuevo('W.6-L1-20 B', 'W.6-L1-20 C', Lw, 12.0, 2, 1, [[1878.25, 1188.6], [1878.25, 1293.04]],
           'L1 DATA 118B west wall (segment of W.6-L1-20) | faces: DATA 118B; BREAK 115 (2nd layer each face for 2 HR)',
           f"{SRC3}; [DERIVED] length {Lw.operacion} = {Lw.v} | height: 12'-0\" B.O. DECK printed on 5/A5.04")
s3 += nuevo('W.6-L1-23 B', 'W.6-L1-23 E', Lx, 12.0, 1, 1, [[2022.5, 1188.6], [2022.5, 1299.1]],
            'L1 DATA 118B east wall (segment of W.6-L1-23) | faces: DATA 118B (2nd layer for 2 HR)',
            f"{SRC3}; [DERIVED] length {Lx.operacion} = {Lx.v} | height: 12'-0\" B.O. DECK printed on 5/A5.04")
s3 += nuevo('W.6-L1-23 B', 'W.6-L1-23 F', Lx, 12.0, 1, 2, [[2022.5, 1188.6], [2022.5, 1299.1]],
            'L1 DATA 118B east wall, Retail 124 side | faces: RETAIL 124 side of the 2 HR fire barrier (rated face stays in our scope, RFI-05 criterion)',
            f"{SRC3}; [DERIVED] length {Lx.operacion} = {Lx.v} | height: 12'-0\" B.O. DECK printed on 5/A5.04")
cambios.append({'n': 3, 'que': 'DATA 118B 2 HR (RFI-24)', 'sf': Val(r2(s3), 'DERIVADO', operacion='W 139.20 + E Data 73.68 + E Retail 147.36', unidad='SF').as_dict()})
ded.append({'id': 'DA-2', 'rfi': 'RFI-24', 'texto': 'DATA 118B west and east walls as tagged (W.6.1 | 0 / W.6-0)', 'delta_sf': -r2(s3), 'material': '5/8" Type X'})
# ---------- 4. FW.4-L4-19 1 HR: cara del bar 1 layer + (R80e.38) ambas caras hasta el roof sheathing
exec(open(f'{W}/scripts/zonas_s105.py').read().split("c = json.load(open(CANON))")[0], globals())
e = IDX['FW.4-L4-19']
(x0, y0), (x1, y1) = e['path'][0], e['path'][-1]
from collections import Counter
cnt = Counter(zona(*a_s105(e['sheet'], x0 + (i + .5) / 100 * (x1 - x0), y0 + (i + .5) / 100 * (y1 - y0)))[0] for i in range(100))
dep = r2(sum(n / 100 * PERALTE[z].v for z, n in cnt.items()), 4)
D4 = Val(dep, 'DERIVADO', operacion=' + '.join(f"{n / 100} x {PERALTE[z].v} ft ({z})" for z, n in cnt.items()) + f" = {dep} ft", unidad='ft')
base_bar = r2(e['length_ft'] * 8.9375)
e['type_id'] = 'FW.4-1'; h0 = e['height_ft']; e['height_ft'] = r2(h0 + dep, 4); e['height_status'] = 'DERIVADO'
e['height_source'] = f"roof framing depth over the run (S1.05): {D4.operacion.replace(' = ', ' -> ')}; 8'-11 1/4\" (LEVEL 4 to underside of roof framing, 1/A5.06) + {dep} = {e['height_ft']} ft to the underside of the roof sheathing; {HEAD}"
e['id'] = 'FW.4-L4-19 A'; IDX['FW.4-L4-19 A'] = e
e['head_detail'] = '2/A0.10 to underside of roof sheathing'
e['source'] = str(e['source']).split(' | height:')[0] + f" | height: {e['height_source']} | RFI-25: tag 'FW.4 | 1' on 1/A2.04 + 2/A0.02 '1HR FP' -> 1 HR"
L4 = Val(e['length_ft'], 'DERIVADO', operacion='rev4 row FW.4-L4-19: (1484.0-1375.4)/9 = 12.07', unidad='ft')
s4 = nuevo('FW.4-L4-19 A', 'FW.4-L4-19 B', L4, e['height_ft'], 1, 1, e['path'],
           'L4 Deck Bar 411 south wall | faces: 411 Deck Bar side (1 HR fire partition, RFI-25)',
           f"1/A2.04 tag 'FW.4 | 1'; 2/A0.02 '1HR FP'; A2.04 [DERIVED] length (A2.04 vector wall lines at printed scale 1/8\"=1'-0\" (9 pt/ft); (1484.0-1375.4)/9 = 12.07); CODE: IBC 2018 §708 (https://codes.iccsafe.org/content/IBC2018P6/chapter-7-fire-and-smoke-protection-features; verified in ICC 2026-11-06, _PUENTE_CLAUDE COD-001) | height: {e['height_source']}",
           tipo='FW.4-1')
IDX['FW.4-L4-19 B']['head_detail'] = '2/A0.10 to underside of roof sheathing'
ext_corr = r2(e['length_ft'] * dep)
cambios.append({'n': 4, 'que': 'FW.4-L4-19 1 HR (RFI-25)', 'sf': Val(r2(s4 + ext_corr), 'DERIVADO',
                operacion=f"bar face {e['length_ft']} x {e['height_ft']} = {s4} (= {base_bar} at 8.9375 ft + {r2(s4 - base_bar)} head to sheathing) + corridor face head {e['length_ft']} x {dep} = {ext_corr}", unidad='SF').as_dict()})
ded.append({'id': 'DA-3', 'rfi': 'RFI-25', 'texto': 'FW.4-L4-19 as FW.4-0 (A0.06 FW row, no rating): no bar face, corridor face to the roof framing line', 'delta_sf': -r2(s4 + ext_corr), 'material': '5/8" Type X'})
# ---------- 5. XW.6.6-2 de L4: no se carga
cambios.append({'n': 5, 'que': "XW.6.6-2 (L4) interior face: NOT extended - 04/A9.05 'ROOF DETAIL - PITCHED LEVEL 4 ROOF' ends the interior board at the top plate / ceiling (heel space filled with spray foam); no new RFI",
                'sf': Val(0, 'DERIVADO', operacion='04/A9.05 detail read: no extension -> 0 SF', unidad='SF').as_dict()})
ded.append({'id': 'DA-4', 'rfi': None, 'texto': 'XW.6.6-2 Level 4 interior face extension to the roof sheathing - not in base (04/A9.05 ends the board at the top plate)', 'delta_sf': 0, 'material': '-'})
c['rev5_cambios'] = cambios; c['deduct_alternates'] = ded
json.dump(c, open(CP, 'w'), indent=1)
for x in cambios:
    print(x['n'], x['sf']['v'], x['que'][:70])
print('deduct', [(d['id'], d['delta_sf']) for d in ded])
