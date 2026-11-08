#!/usr/bin/env python3
"""rev11 (revisión independiente A de COORDINACIÓN sobre rev10, verificada en el plano):
F2 cielos de baño L4 401-405 (GYP-1 en shower rooms): A0.06 GN 12 'USE WATER-RESISTANT GYPSUM BOARD FOR CEILINGS IN SHOWER ROOMS' -> W.R.
F3 C-H studs de los shaft walls L4: altura del stud = altura del board / liner del mismo muro (1/A5.08 'SHAFT WALLS CONTINUOUS TO
   UNDERSIDE OF ROOF SHEETHING' = 10.4375 ft), no la línea de cielo 8.94.
F5 canopy de entrada: trim = 3 bordes libres del contorno dibujado (6.49 frente + 2 x 6.0), el borde de 6.49 en x 1070.76 apoya en el
   storefront 108.1 (1/A3.01 re 1070.8-1124.8 x 858.96-917.4)."""
import json, re, math
W = '/root/cr/work'
CP = f'{W}/etapas/4_canon/takeoff_canon.json'
c = json.load(open(CP))
log = []
# F1: exterior sheathing de L4 hasta el remate real de cada tramo (04/A9.05 eave, 07/A9.05 brow, 10/A9.05 parapet), medido en vectores
F1 = json.load(open(f'{W}/etapas/4_canon/rev9/F1_sheathing_L4.json'))
for w in c['walls'] + c['existing_walls']:
    k = F1.get(w['id'])
    if k and 'sheathing' in str(w.get('board') or ''):
        old = w['height_ft']; w['height_ft'] = round(float(k['altura_ft']), 4); w['height_status'] = k.get('estado', 'DERIVADO')
        w['source'] = re.sub(r"\| height: [^|]*", "", str(w['source'])) + (f" | height: [DERIVED] {w['height_ft']} ft - exterior sheathing continuous past the ceiling and top plate up to the roof edge "
            f"({k.get('remate')}, {k.get('nhoja')}), measured in vectors at the printed scale from the LEVEL 4 datum "
            f"(eave: 1/A5.06 and 3/A5.07 (459.12 - 182.64) / 27 = 10.24; brow: 07/A9.05 13'-4\" + 6.84/108; parapet: 10/A9.05 14'-0\" - 37.2/108, confirmed on 1/A5.07 at grid 14)")
        rem = k.get('remate')
        if rem == 'brow':
            hs = ("DERIVED above LEVEL 4: B.O. BROW 13'-4\" (printed on 07/A9.05) + 0.0633 ft (6.84 pt / 108 pt/ft, sheathing up to the "
                  "inside bottom of the brow box, measured in vectors on 07/A9.05) = 13.40 ft")
        elif rem == 'parapet':
            hs = ("DERIVED above LEVEL 4: ROOF datum 14'-0\" (printed on 10/A9.05 and A4.01) - 0.344 ft (37.2 pt / 108 pt/ft, cap blocking "
                  "measured in vectors on 10/A9.05, cross-check 1/A5.07 grid 14 = 13.69) = 13.66 ft")
        else:
            hs = ("DERIVED above LEVEL 4: underside of roof framing 8'-11 1/4\" (printed on 1/A5.06) + 1.3025 ft (roof framing and "
                  "sheathing at the eave 04/A9.05, measured in vectors on 1/A5.06 at 27 pt/ft: LEVEL 4 to underside of roof sheathing "
                  "459.12 - 182.64 pt / 27 = 10.24, same on 3/A5.07 at grid 8) = 10.24 ft")
        w['height_source'] = hs; w['height_note'] = hs; w['height_status'] = 'DERIVADO'
        if k.get('img'):
            w['height_img'] = k['img']
        log.append(('F1', w['id'], old, w['height_ft']))
# F2
for m in c['misc_items']:
    r = str(m['ref'])
    if m.get('familia') == '5/8" gyp board Type X' and r.endswith(' board') and re.match(r"CLG-L4-1(06|08|10|12|14) ", r):
        m['familia'] = '5/8" gyp Type X W.R.'
        m['source'] = str(m['source']) + " | board W.R.: A0.06 GN 12 'USE WATER-RESISTANT GYPSUM BOARD FOR CEILINGS IN SHOWER ROOMS' (bath with shower)"
        log.append(('F2', r, m['qty']))
# F3
H = {w['id'].split(' ')[0]: float(w['height_ft']) for w in c['existing_walls'] if w['id'].startswith('CH')}
for m in c['misc_items']:
    r = str(m['ref'])
    if r.startswith('CH-STUD '):
        wid = r.split(' ', 1)[1]
        mo = re.match(r"ROUNDUP\(([\d.]+)/2\.0\)\+1 = (\d+) studs x ([\d.]+) ft", str(m['op']))
        if mo and wid in H and abs(float(mo.group(3)) - H[wid]) > 0.01:
            n = int(mo.group(2)); q = round(n * H[wid], 2)
            log.append(('F3', r, m['qty'], q))
            m['qty'] = q
            m['op'] = f"ROUNDUP({mo.group(1)}/2.0)+1 = {n} studs x {H[wid]} ft (= height of the board / liner of the same shaft wall) = {q}"
            m['source'] = str(m['source']) + " | stud height = board / liner height: 1/A5.08 'SHAFT WALLS CONTINUOUS TO UNDERSIDE OF ROOF SHEETHING'"
# F5
for t in c.get('trim_items') or []:
    if t.get('ref') == 'CAN-L1-ENTRY trim':
        t['lf'] = 16.19
        t['op'] = ("6.49 (front edge, 2/A5.03 / 1/A3.01) + 2 x 4.85 (sides, depth 08/A9.05) = 16.19 LF - free edges of the canopy soffit; "
                   "the back edge bears on the storefront 108.1")
        log.append(('F5', t['ref'], 16.19))
json.dump(c, open(CP, 'w'), indent=1)
for l in log:
    print(*l)
# F8: control joints de cielos - A0.06 GN 15 'PROVIDE CONTROL JOINTS IN CEILINGS EXCEEDING 2500 S.F.' + 09 29 00 3.5.D 'Install control joints
# according to ASTM C 840' (ceiling with perimeter relief: <= 50 ft between joints, <= 2500 SF per field). Líneas cada 50 ft en ambas
# direcciones desde el borde del contorno MEDIDO; LF = largo de cada línea dentro del polígono (rayo par / impar, paso 0.5 pt).
c = json.load(open(CP))
def dentro(P, x, y):
    s = False
    for i in range(len(P)):
        (x1, y1), (x2, y2) = P[i], P[(i + 1) % len(P)]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            s = not s
    return s
def largo_dentro(P, fijo, eje, a, b, paso=0.5):
    n = 0
    v = a
    while v < b:
        if (dentro(P, fijo, v) if eje == 'x' else dentro(P, v, fijo)):
            n += 1
        v += paso
    return n * paso
c['misc_items'] = [m for m in c['misc_items'] if not str(m['ref']).startswith('CJ-CLG-')]
tot = 0.0
for x in c.get('ceilings') or []:
    P = x.get('contorno_polygon'); k = x.get('contorno') or {}
    if not P:
        continue
    P = P if isinstance(P[0][0], (int, float)) else P[0]
    esc = 18.0 if str(k.get('sheet', '')).startswith(('A6', 'A7')) else 9.0
    xs = [q[0] for q in P]; ys = [q[1] for q in P]
    W_ = (max(xs) - min(xs)) / esc; H_ = (max(ys) - min(ys)) / esc
    if float(x['area_sf']) <= 2500 and max(W_, H_) <= 50:
        continue
    lin = []
    for j in range(1, int(W_ // 50) + 1):          # líneas N-S cada 50 ft
        xv = min(xs) + 50 * esc * j
        if xv < max(xs) - 1:
            L = largo_dentro(P, xv, 'x', min(ys), max(ys)) / esc
            if L > 0.5: lin.append(('N-S', round(L, 2)))
    for j in range(1, int(H_ // 50) + 1):          # líneas E-W cada 50 ft
        yv = min(ys) + 50 * esc * j
        if yv < max(ys) - 1:
            L = largo_dentro(P, yv, 'y', min(xs), max(xs)) / esc
            if L > 0.5: lin.append(('E-W', round(L, 2)))
    if not lin:
        continue
    q = round(sum(l for _, l in lin), 2); tot += q
    rid = 'CJ-CLG-' + re.sub(r'[^A-Za-z0-9]+', '-', x['room'][:24]).strip('-')
    c['misc_items'].append({"ref": rid, "familia": "control joint", "qty": q,
        "op": f"{len(lin)} line(s) every 50 ft inside the measured ceiling contour ({round(W_, 1)} x {round(H_, 1)} ft, {x['area_sf']} SF): " + " + ".join(f"{d} {l}" for d, l in lin) + f" = {q} LF",
        "source": f"{x['room']}: A0.06 GN 15 'PROVIDE CONTROL JOINTS IN CEILINGS EXCEEDING 2500 S.F.' + 09 29 00 3.5.D 'Install control joints according to ASTM C 840' "
                  f"(<= 50 ft between joints; locations 'VERIFY EXACT LOCATIONS WITH ARCHITECT' - not drawn) [DERIVED] on the contour of {k.get('nhoja')}"})
    print('F8', rid, q, lin)
print('F8 total LF', round(tot, 2))
json.dump(c, open(CP, 'w'), indent=1)
# F10: capas ocultas = Level 1 (09 29 00 3.6.E.1) -> constants.board_sf_concealed (lo usa accesorios.board_yields para el compound)
c = json.load(open(CP))
DRV = ('type x', 'type c', 'w.r', 'wr', 'regular')
conc_w = 0.0
for w in (c.get('walls') or []) + (c.get('existing_walls') or []):
    b = str(w.get('board') or '').lower()
    if 'sheathing' in b or 'shaftliner' in b or 'cement' in b or not any(t in b for t in DRV):
        continue
    ly = int(w.get('layers') or 1)
    if ly > 1:
        conc_w += float(w['length_ft']) * float(w['height_ft']) * int(w.get('faces') or 1) * (ly - 1)
import glob as _g
bath = 0.0
for f in _g.glob(f'{W}/etapas/4_canon/rev9/contornos_L2L3.json'):
    for kk, v in json.load(open(f)).items():
        if kk[:2] in ('L2', 'L3') and v.get('bath_sf'):
            bath += float(v['bath_sf'])
conc = round(conc_w + bath, 2)
c.setdefault('constants', {})['board_sf_concealed'] = {"value": conc, "source": (
    f"[DERIVED] {round(conc_w, 2)} SF inner layers of the multi-layer walls (each face: (layers - 1) x L x H; Type X / W.R. / C, not sheathing / "
    f"shaftliner / cement board) + {round(bath, 2)} SF FS-1 membrane over the L2 / L3 bath boxes (concealed by the dropped GYP-1, A0.08 FS-1) = {conc} SF "
    f"finished to Level 1: 09 29 00 3.6.E.1 'Level 1: For ceiling plenum areas, concealed areas'")}
print('F10 concealed SF', conc)
json.dump(c, open(CP, 'w'), indent=1)
# F9: ADD ALTERNATE AA-1 - Level 5 (skim coat) en el gypsum EXPUESTO de las áreas públicas (corridors, lobbies, stairs, vestibules) si
# se pintan sin wallcovering / plaster: 09 29 00 3.6.E.5 'Level 5: For exposed drywall in public areas that will not receive wall
# covering and/ or plaster finish'; A7.19 'TF-1 ALT - WALLS / CEILINGS PAINT ALT'. Base = Level 4 (TF-1 2 coat plaster, 3.6.E.4).
c = json.load(open(CP))
PUB = re.compile(r"(?i)\b(corridor|lobby|stair|vestibule)\b")
sw = 0.0
for w in (c.get('walls') or []) + (c.get('existing_walls') or []):
    b = str(w.get('board') or '').lower()
    if 'sheathing' in b or 'shaftliner' in b or 'cement' in b:
        continue
    fc = str(w.get('location') or '').split('faces:')[-1] if 'faces:' in str(w.get('location') or '') else ''
    if PUB.search(fc):
        sw += float(w['length_ft']) * float(w['height_ft']) * int(w.get('faces') or 1)      # capa exterior (1 por cara)
scl = 0.0
for m in c['misc_items']:
    r = str(m['ref'])
    if r.endswith(' board') and r.startswith('CLG') and PUB.search(str(m.get('source') or '').split('|')[0]) and 'W.R' not in str(m.get('familia')):
        mo = re.match(r"\s*([\d.]+) SF x (\d+) layer", str(m.get('op') or ''))
        scl += float(mo.group(1)) if mo else float(m['qty'])
tot = round(sw + scl, 2)
c['add_alternates'] = [{"id": "AA-1", "texto": ("Level 5 finish (skim coat over the whole surface, 09 29 00 3.6.D.5 / 3.6.E.5) on the exposed gypsum of the "
    "public areas (corridors, lobbies, stairs, vestibules) if they are painted (A7.19 'TF-1 ALT - WALLS / CEILINGS PAINT ALT') instead of "
    f"2-coat plaster; base = Level 4 [DERIVED: {round(sw, 2)} SF outer wall layer facing public areas + {round(scl, 2)} SF GYP-1 ceilings of public areas]"),
    "delta_sf": tot, "material": "Level 5 skim coat"}]
print('F9 AA-1 SF', tot)
json.dump(c, open(CP, 'w'), indent=1)
# ---------------------------------------------------------------- revisión B (COORDINACIÓN 8-nov, verificada en el plano)
c = json.load(open(CP))
ZR = json.load(open(f'{W}/etapas/4_canon/rev9/contornos_zR11.json'))
def _ar(P):
    return abs(sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))) / 2
# H2: 309 bajo el deck RS-6 de L4 (A2.05 'RS-6 AT LEVEL-4'; A0.08 RS-6 '2 LAYERS, 5/8" TYPE X GYP BOARD', sin RC, RATING '-')
rest = [P for P in ZR['_309_rest']['polygons'] if _ar(P) / 81 > 1]
for x in c['ceilings']:
    if x['room'] == 'L3 Guest room 309' and rest:
        A_ = round(sum(_ar(P) for P in rest) / 81, 2); old = x['area_sf']
        x['area_sf'] = A_; x['contorno_polygon'] = rest[0] if len(rest) == 1 else rest
        x['contorno']['area_medida_sf'] = A_; x['contorno']['nota'] = (f"the part under the L4 deck (RS-6, {ZR['RS6-L3-309']['area_cargar_sf']} SF) moved to "
            "RS6-L3-309 (A2.05 'RS-6 AT LEVEL-4', A0.08 RS-6 2 layers 5/8\" Type X, no resilient channel)")
        x['source'] = str(x['source']) + f" | [DERIVED] FS-1 area = contour {old} SF less the part under the L4 deck RS-6 = {A_} SF (measured, 1/A2.03 + 1/A2.04)"
        log.append(('H2', '309 FS-1', old, A_))
a309 = ZR['RS6-L3-309']['area_cargar_sf']
base_rs6 = next((m for m in c['misc_items'] if m['ref'] == 'RS6-L3 board'), None)
if base_rs6 and not any(m['ref'].startswith('RS6-L3-309') for m in c['misc_items']):
    c['misc_items'].append(dict(base_rs6, ref='RS6-L3-309 board', qty=round(a309 * 2, 2),
        op=f"{a309} SF x 2 layer(s) = {round(a309 * 2, 2)}",
        source=(f"L3 Guest room 309 under the L4 covered deck east of 411 (door 411.3): A3.03 [DERIVED] area {a309} SF (deck footprint 1/A2.04 intersected with the "
                "measured contour of 309, 1/A2.03) | RS-6 (A2.05 'RS-6 AT LEVEL-4'; A0.08 RS-6 '2 LAYERS, 5/8\" TYPE X GYP BOARD' fastened to the wood framing, "
                "no resilient channel, RATING '-')")))
    log.append(('H2', 'RS6-L3-309 board', round(a309 * 2, 2)))
# H6: soffit del smoke curtain 12/A9.03 'SOFFIT AROUND HOUSING' (6 ubicaciones); desarrollo 5.039 ft por LF medido en 12/A9.03
for kk, v in ZR.items():
    if not re.match(r'SOF-L\d-SC[NS]$', kk) or any(m['ref'].startswith(kk + ' ') for m in c['misc_items']):
        continue
    lf = v['lf']; q = round(lf * 5.039, 2); fl = kk.split('-')[1]
    c['misc_items'].append({"ref": f"{kk} board", "familia": "5/8\" gyp board Type X", "qty": q,
        "op": f"{lf} LF x 5.039 ft = {q}", "detail": "12/A9.03",
        "source": (f"{fl} {'service' if kk.endswith('N') else 'lobby'} elevator smoke curtain: 12/A9.03 'SOFFIT AROUND HOUSING' [DERIVED] developed width 5.039 ft per LF "
                   "measured on 12/A9.03 at 1 1/2\"=1'-0\" (drop face 1.239 + bottom 0.374 + housing face 1.198 + return 0.25 + shaft face 1.978); length "
                   f"{lf} ft = the housing drawn on its RCP ({v['sheet']}) | board 5/8\" Type X (drawn 1/2\" and 5/8\"; type not printed - the rated shaft face governs); "
                   "framing drawn wood (Div. 06, excluded); end caps not drawn in plan (2 x ~1.46 SF per location, not loaded)")})
    c.setdefault('trim_items', []).append({"ref": f"{kk} CB", "kind": "corner_bead", "lf": round(2 * lf, 2), "label": "smoke curtain soffit outside corners",
        "source": f"{kk}: 2 outside corners of the drop (12/A9.03) x {lf} LF", "op": f"2 x {lf} = {round(2 * lf, 2)} LF", "status": "DERIVADO", "img": "/root/cr/work/etapas/4_canon/img/rev9/B_H6_A903_det12.png"})
    log.append(('H6', kk, q))
# H8: beam wraps viga por viga: lado expuesto = d - 16.5" (3/S3.02: 2x nailer 1 1/2" sobre el ala; trusses 18" S1.03), d AISC del perfil S1.02
for m in c['misc_items']:
    if m['ref'] == 'BW-L1-RETAIL board' and 'beam by beam' not in str(m['op']):
        old = m['qty']; dep = round(296.78 / 154.23, 5)
        m['qty'] = 296.78
        m['op'] = (f"154.23 LF x {dep} ft = 296.78 (beam by beam: sum LF x (bf + 2 x (d - 16.5\")) / 12 - V1 W24X62 22.344, V2 W24X55 22.322, V3 W24X55 22.344, "
                   "V4 W21X44 20.289, V5 W21X44 19.489, H1 W30X99 31.667, H2 W24X68 15.760 LF; d / bf AISC of the S1.02 sizes, bf = drawn width on 1/A3.01)")
        m['source'] = str(m['source']) + (" | exposed side = d - 16.5\" (3/S3.02: 2x nailer 1 1/2\" on the top flange under the 18\" trusses of S1.03); 2/A5.00 "
                                          "'MAINTAIN CONTINUITY OF MEMBRANE OVER STRUCTURAL STEEL FRAMING VIA GYPSUM BD. & RESILIENT CHANNEL - TYP.'")
        log.append(('H8', m['ref'], old, 296.78))
# H11: fire barriers 2 HR de L1 (W.6-2): cabeza no impresa -> conservador: al underside del floor sheathing de L2 (IBC 2018 Section 707.5)
H_FB = 13.7917
dsf = 0.0
for w in c['existing_walls'] + (c.get('walls') or []):
    if w.get('floor') == 'L1' and str(w.get('type_id')) == 'W.6-2' and abs(float(w['height_ft']) - 12.0) < 0.01:
        dsf += float(w['length_ft']) * (H_FB - 12.0) * int(w.get('faces') or 1) * int(w.get('layers') or 1)
        w['height_ft'] = H_FB; w['height_status'] = 'DERIVADO'
        w['height_source'] = ("DERIVADO: 14'-0\" L1-L2 (5/A5.04) - 1 1/2\" topping - 1/4\" mat - 3/4\" floor sheathing (S1.02) = 14.0 - 0.125 - 0.0208 - 0.0625 "
                              "= 13.7917 ft: 2 HR fire barrier to the underside of the L2 floor sheathing (IBC 2018 Section 707.5; head not detailed, RFI-28 / DA-7)")
        w['source'] = re.sub(r"\| height: [^|]*", "", str(w['source'])) + (" | height: [DERIVED] 13'-9 1/2\" = 14'-0\" L1-L2 - 1 1/2\" topping - 1/4\" mat - 3/4\" sheathing (S1.02): "
            "2 HR fire barrier continuous to the underside of the floor sheathing, IBC 2018 Section 707.5 - the head is not detailed in the set (RFI-28, DA-7: 12'-0\" B.O. DECK 5/A5.04)")
da = c.setdefault('deduct_alternates', [])
if dsf and not any(d.get('id') == 'DA-7' for d in da):
    da.append({"id": "DA-7", "rfi": "RFI-28", "texto": "L1 2 HR fire barriers (W.6-2) ending at 12'-0\" B.O. DECK (5/A5.04) instead of the underside of the L2 floor sheathing", "delta_sf": -round(dsf, 2), "material": "5/8\" Type X"})
    log.append(('H11', 'DA-7', round(dsf, 2)))
json.dump(c, open(CP, 'w'), indent=1)
for l in log:
    if l[0] in ('H2', 'H6', 'H8', 'H11'):
        print(*l)
# F11 (CR-R11-H6, cita = celda del Excel): las burbujas de la cadena se citan en la FILA que gobiernan.
#  A0.09 'FIRE RATED INTERSECTIONS' (leído a ojo, p13): LEVEL 4 = 1,2,3,4 · LEVEL 3 = 5,6,7,8,9 · LEVEL 2 = 10,11,12,13 -> filas XW del piso
#  7/A9.02 'LEVEL 4 WALL TRANSITION' (p82): furring wall (FRT / LP FlameBlock / wood siding) bajo 3'-6" sobre LEVEL 4, muro RE:A0.07 -> XW de L4
#  3/A5.08 'ENLARGED WALL SECTION - COURTYARD NORTH WALL 3' (p40): L1 BAR / KITCHEN, 11'-2 5/8" B.O. DECK y 12'-0" T.O. STEEL/B.O. DECK
#  1/A3.03 y 1/A3.04: RCP de L3 / L4, leyenda GYP-1 -> filas de cielo que ya lo traen en 'detail'
c = json.load(open(CP))
A009 = {'L4': [1, 2, 3, 4], 'L3': [5, 6, 7, 8, 9], 'L2': [10, 11, 12, 13]}
for w in c['walls'] + c['existing_walls']:
    if not str(w.get('type', '')).startswith('XW'):
        continue
    f = w.get('floor'); src = str(w['source'])
    if f in A009 and 'FIRE RATED INTERSECTIONS' not in src:
        src += (f" | floor-line sections at LEVEL {f[1]} (A0.09 FIRE RATED INTERSECTIONS): " + ", ".join(f"{n}/A0.09" for n in A009[f])
                + " - same layers as the A0.07 type (Type X layers continuous at the floor line, FRT wood and LP FlameBlock excluded); no added quantity")
    if f == 'L4' and '7/A9.02' not in src:
        src += (" | 7/A9.02 LEVEL 4 WALL TRANSITION: furring wall below 3'-6\" above LEVEL 4 (FRT furring, LP FlameBlock, wood siding, wall "
                "flashing = not our scope), wall 'EXTERIOR WALL ASSEMBLY, RE:A0.07' = this row")
    w['source'] = src
for w in c['walls'] + c['existing_walls']:
    if w['id'].split(' ')[0] in ('W.6-L1-01', 'W.6-L1-03', 'W.6-L1-04', 'FW.4-L1-02') and '3/A5.08' not in str(w['source']):
        w['source'] = str(w['source']) + (" | cross-check 3/A5.08 (BAR / KITCHEN section): 11'-2 5/8\" B.O. DECK and 12'-0\" T.O. STEEL/B.O. DECK "
                                          "printed, same heights as loaded")
for m in c['misc_items']:
    dt = str(m.get('detail') or '')
    for d_ in ('1/A3.03', '1/A3.04'):
        if d_ in dt and d_ not in str(m['source']):
            m['source'] = str(m['source']) + f" | detail: {d_} (RCP ceiling legend GYP-1)"
d3 = c.get('details', {}).get('3/A5.08')
if d3:
    d3['notes'] = ("L1 BAR / KITCHEN wall section (courtyard north wall, grids 1-5): 11'-2 5/8\" B.O. DECK and 12'-0\" T.O. STEEL/B.O. DECK, "
                   "kitchen ACT ceiling 9'-6\" -> cross-check of W.6-L1-01 / -03 / -04 and FW.4-L1-02 heights")
# F12: XW.6.6-L4-17 cara interior (F&B 410): 2/A5.01 es el corte por el storefront del deck bar (F1); el corte por F&B 410 es 3/A5.07:
#  acabado interior hasta la línea de cielo y = 282.24 -> (523.44 - 282.24) / 27 = 8.93 ft = 8'-11 1/4" impreso en 1/A5.06
for w in c['walls'] + c['existing_walls']:
    if w['id'] == 'XW.6.6-L4-17 B' and abs(float(w['height_ft']) - 11.3958) < 0.01:
        old = float(w['height_ft']); w['height_ft'] = 8.9375; w['height_status'] = 'CONFIRMADO'
        hs = ("1/A5.06 printed 8'-11 1/4\" LEVEL 4 to underside of roof framing; F&B 410 is cut by 3/A5.07 at grid 8: interior finish up to "
              "the ceiling line, vector (523.44-282.24)/27 gives 8.93 (2/A5.01 11'-4 3/4\" is the Deck Bar 411 storefront section, not 410)")
        w['height_source'] = hs; w['height_note'] = hs
        w['source'] = re.sub(r"\| height: [^|]*", "| height: " + hs + " ", str(w['source']))
        print('F12', w['id'], old, 8.9375, round(float(w['length_ft']) * (8.9375 - old) * int(w.get('faces') or 1) * int(w.get('layers') or 1), 2))
json.dump(c, open(CP, 'w'), indent=1)
