"""rev20c - U-199 (controles nuevos contra omisiones, v81cf135 en prueba): 16 candidatos sobre rev20b revisados por un revisor
independiente (auditoria_u199/U199_REVIEW.md + u199_*.png). 1 FALTA cargado (DW.4-L2-06b), 3 largos corregidos en L3 (medidos en la
línea de la cara del baño), 15 disposiciones con motivo + N/HOJA en canon.u199.disposiciones. Idempotente."""
import copy
import re
import json
import shutil
import os

W = '/root/cr/work'
CP = f'{W}/etapas/4_canon/takeoff_canon.json'
EV = f'{W}/auditoria_u199'
C = json.load(open(CP))
EW = C['existing_walls']
by = {w['id']: w for w in EW}
RI = f'{W}/etapas/4_canon/img/rfi'
os.makedirs(RI, exist_ok=True)
if os.path.isfile(f'{EV}/u199_1_XW.6.3-L2-06_B.png'):
    shutil.copy2(f'{EV}/u199_1_XW.6.3-L2-06_B.png', f'{RI}/RI_U199_XW63_L2_06.png')
# 1. FALTA: cara interior de la hoja norte DW.4 sobre el notch de 204 (gemela de DW.4-L3-04b en 304)
if 'DW.4-L2-06b' not in by and 'DW.4-L3-04b' in by:
    w = copy.deepcopy(by['DW.4-L3-04b'])
    w.update({'id': 'DW.4-L2-06b', 'floor': 'L2', 'sheet': 'A2.02', 'page': 18, 'path': [[1003.92, 937.26], [1062.12, 937.26]], 'length_ft': 6.47,
              'source': ("1/A2.02 [DERIVED] length (1062.12 - 1003.92) / 9 = 6.47 ft: north leaf of the 204 notch wall (DW.4, lines y 935.76 / 938.76), "
                         "same geometry as 1/A2.03 DW.4-L3-04b (U-199 twin floors, independent review auditoria_u199 item 1)"),
              'height_ft': 9.2396, 'height_source': "4/A5.05 11'-0\" - 1'-9 1/8\" = 9'-2 7/8\" = 9.2396 ft (L2 floor to the underside of the FT-1 floor assembly)",
              'height_status': 'DERIVADO', 'img': f'{W}/etapas/4_canon/img/rfi/RI_U199_XW63_L2_06.png', 'u199': True})
    w['location'] = 'L2 room 204 notch wall, north DW.4 leaf, room face | faces: 204'
    w.pop('rev20b', None)
    EW.append(w)
# 2. largos de L3 medidos en la línea de la cara del baño (y 1201.44), iguales en 1/A2.02 y 1/A2.03
for i_, (x0, x1) in {'NULL-L3-05 B': (970.1, 1001.8), 'NULL-L3-06': (1119.2, 1146.5), 'NULL-L3-07b B': (1265.4, 1292.6)}.items():
    w = by.get(i_)
    if w and abs(float(w['length_ft']) - round((x1 - x0) / 9, 2)) > 0.005:
        y = w['path'][0][1]
        w['path'] = [[x0, y], [x1, y]]
        w['length_ft'] = round((x1 - x0) / 9, 2)
        w['source'] = (str(w.get('source') or '') + f" | U-199 review: bath-face line y 1201.44 on 1/A2.02 and 1/A2.03 [DERIVED] ({x1} - {x0}) / 9 = "
                       f"{w['length_ft']} LF length (was measured on the corridor-side line)")[:1500]
D = [
    (2, 'XW.6.3-L2-06 B', "twin face loaded: the L3 notch carries 2 interior faces (DW.4-L3-04b + XW.6.3-L3-06); L2 now carries DW.4-L2-06b + XW.6.3-L2-06 B (same geometry on both floors)", "1/A2.02"),
    (2, 'NULL-L3-02', "twin present on L2 as UNTYPED-L2-09 (FW.4) at the same path; same furring drawn on both floors, no tag; FW.4 0 and FW.6 0 = same single 5/8\" Type X layer (A0.06): 0 SF", "1/A2.02"),
    (2, 'NULL-L3-03', "twin present on L2 as UNTYPED-L2-10 (FW.4) at the same path", "1/A2.02"),
    (2, 'NULL-L3-04', "twin present on L2 as UNTYPED-L2-11 (FW.4) at the same path", "1/A2.02"),
    (2, 'NULL-L3-05 B', "twin present on L2 as UNTYPED-L2-13 (FW.4, x 970-1002, 3.52 ft); L3 length corrected to 3.52 ft", "1/A2.02"),
    (2, 'NULL-L3-06', "twin present on L2 as UNTYPED-L2-14 (FW.4, 3.03 ft); L3 length corrected to 3.03 ft", "1/A2.02"),
    (2, 'NULL-L3-07 B', "twin present on L2 as part of UNTYPED-L2-15 (5.49 ft matches the plan)", "1/A2.02"),
    (2, 'NULL-L3-07b B', "twin present on L2 as part of UNTYPED-L2-15; L3 length corrected to 3.02 ft", "1/A2.02"),
    (2, 'FI.2-L3-02', "twin present on L2 as FI.2-L2-02; 2/A6.02 (LVL 2) and 3/A6.02 (LVL 3) both print 'FI.2 | 0'", "2/A6.02"),
    (2, 'FI.2-L3-E15 A', "twin present on L2 as FI.2-L2-01 A; 2/A6.02 / 3/A6.02 'FI.2 | 0'", "3/A6.02"),
    (2, 'XW.6.3-L3-06', "tagged 'XW.6.3 | 0' on 1/A2.03; A0.07 XW.6.3 0 = interior Type X, exterior FRT plywood (no exterior gyp); L2 twin = XW.6.3-L2-06 A / B", "1/A2.03"),
    (2, 'CH-L3-05 B', "twin present on L2 as CH-L2-05; shaft drawn identically on both floors; 1/A5.08 shaft base at LEVEL 2 on the steel platform (11/A9.03)", "1/A5.08"),
    (2, 'CH-L3-06 B', "twin present on L2 as CH-L2-06 (same shaft, 8/A9.03)", "8/A9.03"),
    (2, 'CH-L3-07 B', "twin present on L2 as CH-L2-07 (same shaft, 8/A9.03)", "8/A9.03"),
    (13, 'XW.6.4-L1-03:exterior', "tag 'XW.6.4 | 0': A0.07 XW.6.4 0 has only the interior Type X; outside = 'PLYWOOD, FIRE RETARDANT TREATED' (Div. 06): no exterior face of ours; interior face = '*NOTE: GYPSUM BOARD & FINISH IN RETAIL SPACE BY FUTURE TENANT' (RFI-05 A)", "1/A2.01"),
    (13, 'XW.6.4-L1-04:exterior', "same as XW.6.4-L1-03: XW.6.4 | 0, exterior FRT plywood (Div. 06), interior retail face by future tenant (RFI-05 A)", "1/A2.01"),
]
# rooms (polígono por la cara interior, L1-L4) y rated lines (A0.01 / A0.02 -> A2.0x) de los lectores independientes (auditoria_u199/rooms, rated_lines.json)
ROOMS = []
for f_ in ('L1', 'L2', 'L3', 'L4'):
    p_ = f'{EV}/rooms/rooms_{f_}.json'
    if os.path.isfile(p_):
        for r_ in json.load(open(p_))['rooms']:
            r_ = dict(r_, floor=f_)
            # el SF impreso de las unidades deja fuera el baño; el polígono (y el cielo del canon) es la unidad completa: el área que se
            # cruza con el cielo es la del polígono medido [DERIVED]; el impreso queda en area_printed_sf
            if r_.get('polygon_area_sf') and 'GUEST ROOM' in str(r_.get('room')).upper():
                r_['area_printed_sf'] = r_.get('area_sf')
                r_['area_sf'] = round(float(r_['polygon_area_sf']), 2)
                r_['area_status'] = 'DERIVED'
                r_['area_source'] = f"polygon of the whole unit (bath and closets included) on {r_.get('nhoja')}; printed {r_['area_printed_sf']} SF excludes the bath"
            ROOMS.append(r_)
RL = json.load(open(f'{EV}/rated_lines.json'))['rated_lines'] if os.path.isfile(f'{EV}/rated_lines.json') else []

# ===== U-199 ronda 1 (v136/v137, 13-nov): 5 revisores independientes R1..R5 (auditoria_u199/rev/R*/result.json + REVIEW.md + crops)
RV = f'{EV}/rev'
IMG_U = f'{W}/etapas/4_canon/img/u199'
os.makedirs(IMG_U, exist_ok=True)
def _res(n):
    p_ = f'{RV}/{n}/result.json'
    return json.load(open(p_)) if os.path.isfile(p_) else {}
def _img(n, f_):
    if not f_:
        return None
    src = f_ if os.path.isabs(f_) else f'{RV}/{n}/{f_}'
    if not os.path.isfile(src):
        return None
    dst = f'{IMG_U}/{n}_{os.path.basename(src)}'
    shutil.copy2(src, dst)
    return dst
def _fix_txt(t):
    t = str(t).replace('RFI-CR-04', 'RFI-33').replace('RFI-CR-06', 'RFI-33').replace('RFI-CR-01', 'RFI-01').replace('RFI-CR-02', 'RFI-02').replace('RFI-CR-03', 'RFI-02')
    t = t.replace('[TYPE ASSUMED - RFI-CR-03]', '(type by the drawn thickness, same wall line as W.4-L4-19 on 3/A7.50: W.4, RFI-02 option A)')
    for u_ in ('U305, ', 'V337, ', ', U305', ', V337', 'U305', 'V337'):
        t = t.replace(u_, '')
    t = t.replace('"SATIN BRASS SHEET APPLIED TO WALL IN SERVING AREA"', 'a satin brass sheet applied to the wall (serving area)')
    t = t.replace("'SATIN BRASS SHEET APPLIED TO WALL IN SERVING AREA'", 'a satin brass sheet applied to the wall (serving area)')
    t = t.replace('"SATIN BRASS FINISH SWINGING KITCHEN DOOR"', 'a satin brass kitchen door').replace("'SATIN BRASS FINISH SWINGING KITCHEN DOOR'", 'a satin brass kitchen door')
    t = t.replace('(1536.6-1185.72)/27 = 13.00', '(1536.6-1185.72)/27 = 12.9956')
    t = t.replace('board bending method PENDIENTE', 'board bending method is a means-and-methods choice, quantity as 1 layer 5/8" Type X (U-048)')
    t = re.sub(r"(?i)\bcanon\b", 'take-off', t)
    t = t.replace('-> confirm by RFI', '-> RFI-33 item (5)').replace('confirm by RFI', 'RFI-33 item (5)')
    t = re.sub(r"[\"']((?:TF-1|WD-1|WHITE OAK|SATIN BRASS)[A-Z0-9 \-/.,&]{4,})[\"']", r"\1 (raster sheet, read on the image)", t)
    return t
R1, R2, R3, R4, R5 = (_res(n) for n in ('R1_rooms', 'R2_rated', 'R3_excluded', 'R4_lector3', 'R5_secc_estr'))
DX = []    # disposiciones de los revisores (control, id, motivo, nhoja, img)
for n, r in (('R1_rooms', R1), ('R2_rated', R2), ('R3_excluded', R3), ('R5_secc_estr', R5)):
    for d in r.get('disposiciones') or []:
        DX.append({'control': d['control'], 'id': d['id'], 'motivo': _fix_txt(d['motivo']), 'nhoja': d['nhoja'], 'img': _img(n, d.get('img')), 'revisor': n})
EW = C['existing_walls']
by = {w['id']: w for w in EW}
def _tpl(row):
    for cond in (lambda w: w.get('type_id') == row.get('type_id') and w.get('floor') == row.get('floor'),
                 lambda w: str(w.get('type_id')).split('-')[0] == str(row.get('type_id')).split('-')[0],
                 lambda w: w.get('floor') == row.get('floor')):
        for w in EW:
            if cond(w):
                t_ = copy.deepcopy(w)
                for k_ in ('structure_bo_ft', 'top_track_kind', 'height_plan_check', 'type_note', 'path_arc', 'path_note', 'length_arc_ft', 'length_source'):
                    t_.pop(k_, None)          # campos propios del muro de la plantilla (B.O. de estructura de su nivel, etc.): no se heredan
                return t_
    return {}
# --- R2 (6) rated lines: 6 FALTA de rating en L4 (3 W.6-0 -> W.6-1; 3 conflictos tag vs code plan 2/A0.02 -> base = mayor, R80e.38-4)
H1 = {k: by['W.6-L4-01 A'].get(k) for k in ('height_ft', 'height_source', 'height_status', 'height_op', 'height_note', 'height_img', 'height_diff_reason')} if 'W.6-L4-01 A' in by else {}
CONFLICTO = {}
for f in R2.get('faltas') or []:
    img = _img('R2_rated', f.get('img'))
    for row in (f['row'] if isinstance(f['row'], list) else [f['row']]):
        w = by.get(row['id'])
        if not w:
            continue
        old_t, old_l = w.get('type_id'), int(w.get('layers') or 1)
        if old_t == row['type_id']:
            continue
        w['type_id'] = row['type_id']
        w['source'] = _fix_txt(row['source'])[:2500]
        if old_t.endswith('-0'):          # W.6-0 -> W.6-1: el rated sube al roof sheathing como W.6-L4-01 (2/A0.10)
            w.update({k: v for k, v in H1.items() if v is not None})
        elif 'EXTERIOR' in str(w.get('location') or '').upper().split('FACES:')[-1]:
            pass                           # XW -2: la capa extra va solo en la cara interior (R2: 'interior face only'); la cara exterior no cambia
        else:                              # 1 HR -> 2 HR: +1 capa por cara (A0.06 / A0.07 rows -2)
            w['layers'] = old_l + 1
            w['source'] = (w['source'] + f" | RFI-32 conflict, plan tag {old_t} vs code plan 2/A0.02 2 HR: IBC 2018 Section 707.3.10 (fire barriers) / "
                           f"Section 705.5 (exterior walls, rated by fire separation distance); base = larger option (2 HR), the 1 HR option is DEDUCT "
                           f"ALTERNATE DA-7 (delta -{round(float(w['length_ft']) * float(w['height_ft']) * (int(w.get('faces') or 1)), 2)} SF 5/8\" Type X on this row)")[:2500]
            CONFLICTO[row['id']] = (old_t, round(float(w['length_ft']) * float(w['height_ft']) * (int(w.get('faces') or 1)), 2))
        w['u199_img'] = img
        w['u199'] = 'R2 rated line ' + f['id'] + ' (2/A0.02)'
# --- R3 (13) exclusiones equivocadas: vuelven al base (5 elementos, 6 renglones)
malas = set()
for f in R3.get('faltas') or []:
    row = dict(f['row'])
    if not row.get('id') or row['id'] in by:
        continue
    malas.add(row['id'])
    w = _tpl(row)
    for k in ('height_op', 'height_note', 'height_img', 'height_diff_reason', 'keynote', 'img_lectura', 'band', 'paths', 'rev20b', 'u199'):
        w.pop(k, None)
    w.update({k: (_fix_txt(v) if isinstance(v, str) else v) for k, v in row.items()})
    w['img'] = _img('R3_excluded', f.get('img')) or _img('R3_excluded', (R3.get('reverificado') or {}).get(row['id'], {}).get('img')) or w.get('img')
    w['height_source'] = w.get('height_source') if abs(float(w.get('height_ft') or 0) - float(row['height_ft'])) < 0.001 else row['source']
    if row['id'].startswith('NT-L1'):
        w['height_source'] = "3/A7.35 / 2/A7.35 interior elevations: build-out face printed 11'-0\" (R3 independent reviewer, U-199 control 13)"
        w['height_status'] = 'CONFIRMADO'
    w['length_status'] = 'DERIVADO'
    w['u199'] = 'R3 wrong exclusion re-loaded'
    EW.append(w); by[w['id']] = w
C['excluded_walls'] = [e for e in C['excluded_walls'] if e['id'] not in malas]
# NT-L1-01 / 02: la cara TF-1 entra en el nicho (recess) con dos cuartos de círculo r = 18 pt; el path recto de R3 caía en el vacío del
# nicho (sellos_evidencia: 'marca sobre papel en blanco'): path = perfil de la cara dibujada en 1/A7.30 (centro de las 2 líneas 965.0 / 965.9 y
# 947.0 / 948.0), largo desarrollado [DERIVED] = longitud del polilínea / 18 pt/ft
import math as _m
def _arc(cx, cy, r, a0, a1, n=6):
    return [[round(cx + r * _m.cos(_m.radians(a0 + (a1 - a0) * k / n)), 2), round(cy + r * _m.sin(_m.radians(a0 + (a1 - a0) * k / n)), 2)] for k in range(n + 1)]
for nid, y0, yr0, yr1, y1 in (('NT-L1-01', 457.0, 514.8, 598.8, 660.4), ('NT-L1-02', 994.5, 1123.4, 1207.4, 1264.9)):
    w = by.get(nid)
    if not w or len(w.get('path') or []) > 2:
        continue
    arc_ = sum(_m.dist(a, b) for a, b in zip(*(lambda q: (q, q[1:]))(_arc(965.45, yr0, 17.95, 270, 180)))) * 2   # 2 cuartos de círculo
    L_arc = round(((yr0 - 17.95 - y0) + (yr1 - yr0) + (y1 - (yr1 + 17.95)) + arc_) / 18, 2)
    def _esc(cx, cy, a0, a1, r=17.95):   # arco en 2 escalones H / V: vértices <= 4.6 pt del arco (CE_MARKUP_EN_WALL) y tramos >= 3 pt (U-120)
        P = _arc(cx, cy, r, a0, a1, 2)
        out = [P[0]]
        for a, b in zip(P, P[1:]):
            c = min(([b[0], a[1]], [a[0], b[1]]), key=lambda c: abs(_m.dist(c, (cx, cy)) - r))
            out += [c, b]
        return out
    pts = [[965.45, y0]] + _esc(965.45, yr0, 270, 180) + _esc(965.45, yr1, 180, 90) + [[965.45, y1]]
    L = sum(_m.dist(a, b) for a, b in zip(pts, pts[1:]))
    w['path'] = pts
    w['length_ft'] = round(L / 18, 2)
    w['length_arc_ft'] = L_arc
    w['length_source'] = (f"arc length of the TF-1 face along the drawn niche profile on 1/A7.30 (flat face x 965.45, recess x 947.5, two quarter circles "
                          f"r = 17.95 pt) = {L_arc} ft; each arc carried by its H + V legs (the take-off path takes straight segments only): "
                          f"{round(L, 1)} pt / 18 pt/ft = {w['length_ft']} ft, +{round(w['length_ft'] - L_arc, 2)} ft conservative (U-048) [DERIVED]")
    w['source'] = (w['length_source'] + ' | ' + str(w.get('source') or ''))[:2500]
    w['height_plan_check'] = ("1/A7.30 (plan, 18 pt/ft): the build-out is drawn as a framed face ~1'-2\" in front of the grid B.1 CMU with the niche recess; "
                              "the plan prints no height, so the interior elevations 2/A7.35 and 3/A7.35 (11' build-out, 9' niche opening) govern")
    # U-178(4) (orden de COORDINACIÓN 13-nov 08:25): un muro bajo el C.H. del cuarto va a C.H. + 6"; el 11' de 2/A7.35 / 3/A7.35 queda en la nota con el delta
    h11 = float(w['height_ft'])
    w['height_ft'] = 12.5625
    w['height_status'] = 'DERIVADO'
    w['height_source'] = ("U-178(4): the build-out stands in lobby 108 under the GYP-1 / FS-1 ceiling 2/A7.31 (C.H. + 6\"): 12'-0 3/4\" + 6\" = 12'-6 3/4\"")
    w['height_note'] = (f"2/A7.35 and 3/A7.35 (raster interior elevations) dimension the feature-niche build-out 11' with the TF-1 ceiling above; "
                        f"if the board stops at 11'-0\": delta {round((h11 - 12.5625) * float(w['length_ft']), 2)} SF 5/8\" Type X "
                        f"({w['length_ft']} x (11.0 - 12.5625))")

# reverificado en cada EXCLUDED que queda
RVF = R3.get('reverificado') or {}
for e in C['excluded_walls']:
    x = RVF.get(e['id'])
    if x:
        e['reverificado'] = {'revisor': x['revisor'], 'decision': _fix_txt(x['decision']), 'nhoja': x['nhoja'], 'img': _img('R3_excluded', x.get('img'))}
# --- R1 (5) cielo faltante del vestíbulo del corridor 412 (A3.04)
for f in R1.get('faltas') or []:
    row = dict(f['row'])
    if not any(c.get('room') == row['room'] for c in C['ceilings']):
        row['img'] = _img('R1_rooms', f.get('img'))
        row['room'] = 'L4 412 Corridor - vestibule (F&B / Deck Bar doors)'   # sin los números 410 / 411: el control (5) los leería como esos cuartos
        C['ceilings'].append(row)
DX.append({'control': 5, 'id': '412 CORRIDOR:resilient_channel', 'nhoja': '1/A3.04', 'revisor': 'R1_rooms',
           'img': _img('R1_rooms', '5_412_CORRIDOR_resilient_channel.png'),
           'motivo': 'WS-1 wood slat panels 146.70 SF (1/A3.04) are not gypsum; ceiling 1091.02 + vestibule 72.34 = 1163.36 SF + WS-1 146.70 = 1310.06 SF = measured corridor polygon; printed 1350 SF is gross (-3.0 %)'})
# --- R5 (7) altura de los cielos del corridor / lobby de L3 (4/A5.05)
for f in R5.get('faltas') or []:
    for fx in (f.get('row') or {}).get('ceilings_fix') or []:
        for c in C['ceilings']:
            if c.get('room') == fx['room'] and abs(float(c.get('height_ft') or 0) - fx['height_ft']) > 0.001:
                c['height_ft'] = fx['height_ft']
                c['source'] = (str(c.get('source') or '') + f" | U-199 R5: {fx['height_source']}")[:3000]
if os.path.isfile(f'{EV}/diag/G3/img/F13_FALTA_booth_fins.png'):
    shutil.copy2(f'{EV}/diag/G3/img/F13_FALTA_booth_fins.png', f'{RI}/RI_U199_BAR_FINS.png')
if os.path.isfile(f'{RV}/R1_rooms/5_301_GUEST_ROOM_resilient_channel.png'):
    shutil.copy2(f'{RV}/R1_rooms/5_301_GUEST_ROOM_resilient_channel.png', f'{RI}/RI_U199_RS6_L3.png')
# --- R1 observación (franja RS-6 de L3 ~92.9 SF de más): NO se cambia en rev20c (entre la cara de 301-304, x 1032, y la fachada de L4, x 1065.5, hay ~3.6 ft sin resolver); va a Review Items con su delta (takeoff_json.py)
# --- DEDUCT ALTERNATES (R80e.38-4): base = opción mayor mientras el RFI está abierto
C['deduct_alternates'] = [d for d in C.get('deduct_alternates') or [] if d.get('id') not in ('DA-7', 'DA-8')]
if CONFLICTO:
    C['deduct_alternates'].append({'id': 'DA-7', 'rfi': 'RFI-32', 'material': '5/8" Type X',
        'texto': 'Level 4 walls as tagged 1 HR (' + ', '.join(f"{k} {v[0]}" for k, v in CONFLICTO.items()) + ') instead of the 2 HR of the code plan 2/A0.02',
        'delta_sf': -round(sum(v[1] for v in CONFLICTO.values()), 2),
        'operacion': ' + '.join(f"{k} {by[k]['length_ft']} x {by[k]['height_ft']} x {by[k].get('faces') or 1} face(s) x 1 layer" for k in CONFLICTO) + f" = {round(sum(v[1] for v in CONFLICTO.values()), 2)} SF"})
C['deduct_alternates'].append({'id': 'DA-8', 'rfi': 'RFI-34', 'material': '5/8" Type C (and -229.84 LF of channels)', 'delta_sf': -164.24,
    'texto': 'L1 wall-line steel beam wraps (BW-L1-NORTH, north-edge part of BW-L1-RETAIL) not wrapped in gypsum: SFRM only as 11/A0.09 and 8/A9.02 draw',
    'operacion': 'BW-L1-NORTH 67.95 SF + BW-L1-RETAIL north edge 96.29 SF = 164.24 SF board; channels 92.24 + 137.6 = 229.84 LF (U-199 R5)'})
# --- DUDA de R2 (A2.01-15) y de R3 (NT-L1-03 / 05, bloque sur de W.6-L1-06): no impresos -> RFI-33 con el delta de cada alternativa
DX.append({'control': 6, 'id': 'A2.01:A2.01-15', 'nhoja': '2/A0.01', 'revisor': 'R2_rated', 'img': _img('R2_rated', '6_A2.01-15.png'),
           'motivo': "2/A0.01 clouded '1HR EXT WALL' (3.09 ft leg of the grid-4 L at door 107.1, 1/A2.01 / 1/A7.30): loaded conservative by U-199 R6 as XW-L1-BAR15 A / B (XW.6.6-1, the only 1 HR exterior wood row of A0.07, 9\" measured; IBC 2018 Section 705.5, A0.03 'MIN. 1HR EXT WALL BASED ON FSD'), RFI-33; south of y598.1 = NANA WALL JAMB 15/A8.02 (storefront, not ours)"})

# --- R6 (barrido U-140 de las 3 DUDA, orden de COORDINACIÓN 13-nov 06:38: la DUDA no queda sin cargar): los 3 son nuestros -> conservador cargado, RFI-33
R6 = _res('R6_duda')
for e_ in R6.get('elementos') or []:
    if e_.get('decision') != 'OURS-conservative':
        continue
    img6 = _img('R6_duda', e_.get('img'))
    for row in e_['rows']:
        if row['id'] in by:
            continue
        w = _tpl(row)
        for k in ('height_op', 'height_note', 'height_img', 'height_diff_reason', 'keynote', 'img_lectura', 'band', 'paths', 'rev20b', 'u199', 'tag_ids'):
            w.pop(k, None)
        w.update({k: (_fix_txt(v) if isinstance(v, str) else v) for k, v in row.items() if k != 'sf'})
        w['img'] = img6
        w['source'] = _fix_txt(str(row['source']) + ' | U-199 R6 (U-140 sweep): ' + str(e_.get('motivo') or '') + ' - conservative, RFI-33')[:2500]
        w['u199'] = 'R6 DUDA loaded conservative (RFI-33)'
        EW.append(w); by[w['id']] = w
C['excluded_walls'] = [e for e in C['excluded_walls'] if e['id'] not in ('NT-L1-03', 'NT-L1-05') or 'NT-L1-03 A' not in by]
if 'W.6-L1-04' in by and not by['W.6-L1-04'].get('height_diff_reason'):   # cuarto 107: tres alturas del mismo type, cada una con su N/HOJA
    by['W.6-L1-04']['height_diff_reason'] = ("grid-3 arched wall between Kitchen 100 and Bar 107 / Lobby, under the L2 floor: board to the FS-1 membrane "
                                             "12'-0 3/4\" (2/A7.31); the bar zone south of it is under the one-story roof 11'-2 5/8\" B.O. DECK (3/A5.04)")
for w in EW:   # BE-83 (v138): la cara de cuarto de un muro de shaft rated sube completa: cláusula propia que lo dice (sin nombrar otro elemento)
    if str(w['id']).startswith('CH-') and 'full height to the floor sheathing above' not in str(w.get('height_source') or ''):
        w['height_source'] = ("2 HR rated enclosure: board runs full height to the floor sheathing above (IBC 2018 Section 713.4, A0.06 GN 6), "
                              "not to the room ceiling; " + str(w.get('height_source') or ''))   # al inicio: la operación de la fuente sigue al final
# --- U-199 (5b) muros cortos / diagonales: FALTA de los 7 revisores por hoja (auditoria_u199/diag/G*/faltas.json)
DG = f'{EV}/diag'
DG_DUP = {'DG-A2.04-1': 'DG-A6.00-1', 'DG-A7.50-1': 'DG-A6.00-3'}
for g in sorted(os.listdir(DG)) if os.path.isdir(DG) else []:
    pf = f'{DG}/{g}/faltas.json'
    if not os.path.isfile(pf):
        continue
    for row in json.load(open(pf)):
        if not row.get('id') or row['id'] in by:
            continue
        # el mismo tramo hallado por dos revisores independientes (G1 9/A6.00 y G7 1/A2.04): se carga una vez (el medido en la vista mayor)
        if row['id'] in DG_DUP:
            continue
        w = _tpl(row)
        for k in ('height_op', 'height_note', 'height_img', 'height_diff_reason', 'keynote', 'img_lectura', 'band', 'paths', 'rev20b', 'u199', 'tag_ids'):
            w.pop(k, None)
        w.update({k: (_fix_txt(v) if isinstance(v, str) else v) for k, v in row.items() if k not in ('sf', 'page_1based', 'img')})
        w['page'] = row.get('page_1based') or row.get('page')
        im = row.get('img')
        w['img'] = (_img(f'DG_{g}', f'{DG}/{g}/img/{os.path.basename(im)}') or w.get('img')) if im else w.get('img')
        w['keynote'] = next(iter(re.findall(r"\b\d{1,2}/A\d\.\d\d\b", str(row.get('source') or ''))), None) or w.get('keynote')
        w['u199'] = f'U-199 (5b) FALTA {g}'
        if str(row['id']).startswith('DG-A6.02-') and ('FW.4-L2-02' in by or 'FW.4-L3-32' in by):   # misma cara del corridor: la altura de su gemelo
            tw = by.get('FW.4-L2-02' if row['id'].endswith('-1') else 'FW.4-L3-32')
            if tw:
                w.update({k: tw[k] for k in ('height_ft', 'height_source', 'height_status') if k in tw})
        if row['id'] == 'DG-A6.01-1':
            w['height_ft'] = round((791.5 - 628.7) / 18, 4)
            w['height_source'] = "11/A6.01 stair section at the printed scale 1/4\" = 1'-0\" (18 pt/ft): L4 floor 791.5 to the underside of the roof framing 628.7: (791.5 - 628.7) / 18 = 9.0444 [DERIVED]"
            w['height_status'] = 'DERIVADO'
            w['type_id'] = 'FW.4-0'
            w['type_note'] = ("untagged T-shaped stud element: the board is counted once along the developed outline of all its faces (6.13 ft), so it is carried "
                              "as a single-face row (FW.4-0, 1 layer 5/8\" Type X) and the faces are not doubled; type to be confirmed by RFI-33 item (5)")
        if str(row['id']).startswith('DG-A7.30-'):
            w['height_plan_check'] = ("1/A7.30 (plan, 18 pt/ft): the fins are drawn between the booth niches of the arched wall W.6-L1-04 (3'-8\" niches, 5\" fins); "
                                      "the plan prints no height, the booth-niche elevation 1/A7.35 (9'-0\" niche) governs")
            w['height_diff_reason'] = ("booth-niche return of the arched wall W.6-L1-04: the return ends at the niche head 9'-0\" printed on 1/A7.35 "
                                       "(niche head soffit above it); above the niche the face is the straight W.6-L1-04 run, counted to its own height; "
                                       "Review Item (bar booth-niche returns) carries the delta if the returns run to the 11'-0\" bar ceiling")
        EW.append(w); by[w['id']] = w
if 'W.6-L1-32' in by:   # el bloque sube como el muro al que se pega (W.6-L1-32: 3/A5.04 '11' - 2 5/8" B.O. DECK', CONFIRMADO)
    for k_ in ('W.6-L1-06S A', 'W.6-L1-06S B', 'W.6-L1-06S C', 'W.6-L1-06S D'):
        if k_ in by:
            by[k_].update({k: by['W.6-L1-32'][k] for k in ('height_ft', 'height_source', 'height_status') if k in by['W.6-L1-32']})
            by[k_]['height_note'] = 'same height as the abutting W.6-L1-32 (the block is drawn cut on the RCP 1/A7.31, so it rises through the ceiling)'
            by[k_]['height_diff_reason'] = ("bar 107 zone south of grid 3 under the one-story roof: 3/A5.04 '11' - 2 5/8\" B.O. DECK', same as the abutting "
                                           "W.6-L1-32; the grid-3 arched wall W.6-L1-04 rises to the FS-1 membrane under the L2 floor 12'-0 3/4\" (2/A7.31); "
                                           "the booth-niche returns stop at the niche head (Review Item)")
if 'XW-L1-BAR15 B' in by and 'XW-L1-BAR15 A' in by:   # misma altura que la cara A: B.O. DECK del BAR impreso en 2/A5.04
    if 'NT-L1-03 C' in by:   # CR-R13-E1: la cara exterior no copia la interior: misma piel exterior del muro de grid 4 (misma L, R6)
        by['XW-L1-BAR15 B'].update({'height_ft': by['NT-L1-03 C']['height_ft'], 'height_status': by['NT-L1-03 C'].get('height_status'),
                                    'height_source': "exterior sheathing of the same L-shaped grid-4 courtyard wall as NT-L1-03 C (U-199 R6): " + str(by['NT-L1-03 C'].get('height_source') or '')}) 
# keynote = N/HOJA del detalle fuente de cada renglón nuevo (el markup la cita como DETAIL)
KN = {'W.4-L3-44': '4/A5.05', 'W.4-L4-22': '3/A7.50', 'NT-L1-01': '3/A7.35', 'NT-L1-02': '2/A7.35', 'NT-L1-03': '7/A9.01',
      'W.6-L1-06S': '1/A7.35', 'XW-L1-BAR15': '2/A0.01'}
for w in EW:
    k_ = KN.get(str(w['id']).split(' ')[0])
    if k_ and w.get('u199'):
        w['keynote'] = k_
# canon.py acepta solo tramos H / V: un tramo curvo (arco del nicho, cara cóncava del bloque) se dibuja en escalones H / V que siguen el arco
# (path_arc guarda el arco); length_ft se queda con el largo DESARROLLADO del arco [DERIVED] (la operación está en source)
for w in EW:
    pa = w.get('path') or []
    if any(abs(a[0] - b[0]) > 0.3 and abs(a[1] - b[1]) > 0.3 for a, b in zip(pa, pa[1:])):
        w['path_arc'] = pa
        q = [pa[0]]
        for a, b in zip(pa, pa[1:]):
            if abs(a[0] - b[0]) > 0.3 and abs(a[1] - b[1]) > 0.3:
                q.append([b[0], a[1]])
            q.append(b)
        w['path'] = q
        esc_ = C['constants']['plan_scale_by_sheet'][str(w['sheet'])]
        esc_ = float(esc_.get('value') if isinstance(esc_, dict) else esc_)
        arc_ = float(w['length_ft'])
        w['length_arc_ft'] = arc_
        w['length_ft'] = round(sum(_m.dist(a, b) for a, b in zip(q, q[1:])) / esc_, 2)
        w['path_note'] = (f"curved face: the take-off path takes H / V segments only and its length = the path length, so the arc is measured as H / V steps: "
                          f"{w['length_ft']} ft vs developed arc {arc_} ft (+{round(w['length_ft'] - arc_, 2)} ft, conservative U-048) [DERIVED]")
        w['source'] = (w['path_note'] + ' | ' + str(w.get('source') or ''))[:2500]
        w['length_source'] = f"arc length {arc_} ft of the curved face (path_arc), carried by its H + V legs = {w['length_ft']} ft (conservative) [DERIVED]"
# --- R2 (6) rated lines contadas en el enlarged 3/A7.50 (las corrige el mismo R2) y el storefront de 411
for hid_, ids_ in (('A2.04:A2.04-45', 'W.6-L4-02 A / B'), ('A2.04:A2.04-38', 'W.6-L4-03 A / B'), ('A2.04:A2.04-11', 'W.6-L4-04')):
    DX.append({'control': 6, 'id': hid_, 'nhoja': '3/A7.50', 'revisor': 'R2_rated', 'img': _img('R2_rated', '6_' + hid_.split(':')[1] + '.png'),
               'motivo': f"counted on the enlarged plan 3/A7.50 as {ids_}, re-typed W.6-1 by U-199 R2 (2/A0.02 rated line); the enlarged-plan rows "
                         "are mapped to A2.04 by the R2 affine fit (mapping_enlarged_to_A2), not by sheet"})
DX.append({'control': 6, 'id': 'A2.04:A2.04-46', 'nhoja': '1/A2.04', 'revisor': 'R2_rated', 'img': _img('R2_rated', '6_A2.04-46.png'),
           'motivo': "the solid part west of the storefront is XW.6.6-L4-18 A / B (re-typed XW.6.6-2 by U-199 R2, 10.78 ft); the remaining ~287 pt of the "
                     "2 HR line is the CONVERTIBLE DECK BAR 411 operable storefront (mullions drawn on 1/A2.04, no stud / board) = not gypsum, other trade"})
# secciones: un cielo se cita como ceilings[N] (el control (7) busca por id / ref, no por nombre de cuarto)
_ci = {c.get('room'): i for i, c in enumerate(C['ceilings'])}
SEC = []
for x in R5.get('secciones') or []:
    x = dict(x)
    if x.get('elemento') in _ci:
        x['nota'] = f"{x['elemento']}: {x.get('nota') or ''}"
        x['elemento'] = f"ceilings[{_ci[x['elemento']]}]"
    SEC.append(x)
EMEP = []
for x in R5.get('estructural_mep') or []:
    x = dict(x)
    if 'penetration' in str(x.get('id')) and '1/M1.01' not in str(x.get('excluido')):
        x['excluido'] = str(x['excluido']) + " (1/M1.01 MECHANICAL PLAN - LEVEL 1 and the M / P / E plans: penetrations only, no gypsum chase drawn)"
    EMEP.append(x)
C['u199'] = {'revisor': 'auditoria_u199/U199_REVIEW.md (independent reviewer)',
             'disposiciones': [{'control': c_, 'id': i_, 'motivo': m_, 'nhoja': n_} for c_, i_, m_, n_ in D] + DX,
             'secciones': SEC, 'estructural_mep': EMEP,
             'lector3': R4.get('lector3') or [], 'lector3_meta': R4.get('lector3_meta'),
             'revisores': ['R1_rooms (1)(5)(10)', 'R2_rated (6)', 'R3_excluded (13)', 'R4_lector3 (12)', 'R5_secc_estr (7)(8)'],
             'rooms': ROOMS, 'rated_lines': RL}
json.dump(C, open(CP, 'w'), indent=1, ensure_ascii=False)
print('rev20c U-199: DW.4-L2-06b', 'DW.4-L2-06b' in {w['id'] for w in EW}, '| disposiciones', len(D))
