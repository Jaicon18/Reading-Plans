"""rev16 (revisión dirigida de rev15, COORDINACIÓN 10-nov, orden del usuario 'revisa todo otra vez'):
 1 ELEC 221 / 321 / 421: A0.00 'FIRE BARRIERS - ELECTRICAL AND IT ROOMS 2 HR' + 'INCIDENTAL USE AREAS (TABLE 509) ... ELECTRICAL ROOMS'
   vs code plans 1HR FP = conflicto plano-plano -> base = opción mayor (2 HR, +1 capa por cara, criterio de DATA 118B) + DEDUCT ALTERNATE DA-6.
 2 cove de corridor 7/A7.23: el detalle dibuja las piezas con el símbolo de madera (caja con X, igual que los top plates) -> el dibujo
   específico manda sobre el legend GYP-1 'METAL SUSPENSION SYSTEM, OR WOOD FRAMING' (R-ALC-10) -> framing de madera, Div. 06 EXCLUDED
   (U-139): fuera los tracks y cripples de SOF-L2-01 / L2-02 / L3-316 / L3-318 / L4-02 (el board sigue). Lobby (5/A7.31) y stair FCU
   (11/A6.01) no dibujan madera: siguen metálicos.
 6 2HR SHAFT CEILING: la membrana está en el plenum de L1 (1/A5.08) -> CLG-L1-SHN / SHS dibujados en el RCP de L1 (geometría del fork)."""
import json, math, re
W = '/root/cr/work'; CP = f'{W}/etapas/4_canon/takeoff_canon.json'
c = json.load(open(CP))
WALLS = c['walls'] + c['existing_walls']
idx = {w['id']: w for w in WALLS}
LOG = []
A00 = ("A0.00 code summary prints 'ELECTRICAL AND IT ROOMS' '2 HR' (fire barrier ratings) and 'INCIDENTIAL USE AREAS (TABLE 509):' 'ELECTRICAL ROOMS'; "
       "the code plan of the level draws the room 1HR FP -> plan vs plan conflict (IBC 2018 Section 707.3: fire barriers where required): base carries the "
       "larger option (2 HR = 2 layers 5/8\" Type X each face, as DATA 118B), the 1 HR as DEDUCT ALTERNATE DA-6, delta -DA6TOT SF (RFI-04)")
# ---- 1. ELEC 221 / 321 / 421: +1 capa por cara ----
ELEC = {'UNTYPED-L2-12': '3/A0.01 ELEC 221', 'NULL-L3-08': '1/A0.02 ELEC 321', 'NULL-L3-09 A': '1/A0.02 ELEC 321', 'NULL-L3-09 B': '1/A0.02 ELEC 321',
        'W.4-L4-18 A': '2/A0.02 ELEC 421', 'W.4-L4-18 B': '2/A0.02 ELEC 421', 'W.6-L4-09 A': '2/A0.02 ELEC 421', 'W.6-L4-09 B': '2/A0.02 ELEC 421'}
filas = []
for wid, cp in ELEC.items():
    w = idx[wid]
    if 'ELECTRICAL AND IT ROOMS 2 HR' not in str(w['source']):
        w['layers'] = int(w.get('layers') or 1) + 1
        w['source'] = str(w['source']).replace(' | height', f" | rating: {A00} [{cp}]" + ' | height', 1) if ' | height' in str(w['source']) else str(w['source']) + f" | rating: {A00} [{cp}]"
        w['location'] = str(w['location']).replace('[TYPE ASSUMED - RFI-04] ', '')
        LOG.append(f"{wid} +1 layer: {w['length_ft']} x {w['height_ft']} x {w['faces']} = +{round(w['length_ft'] * w['height_ft'] * w['faces'], 2)} SF")
    filas.append({"id": wid, "faces": w['faces'], "layers": 1})
# cara de 421 dentro de W.6-L4-08 (muro sur de 421): ancho de 421 = CLG-L4-119 10.8 SF / 8.77 ft = 1.2315 ft [DERIVADO]; ambas caras +1 capa
b8 = idx['W.6-L4-08 A']; y8 = b8['path'][0][1]; L421 = round(10.8 / 8.77, 4)
for nid, base, fx in (('W.6-L4-08 C', 'W.6-L4-08 B', '421 Elec (2nd layer, 2 HR)'), ('W.6-L4-08 D', 'W.6-L4-08 A', '412 Corridor side of the 421 segment (2nd layer, 2 HR)')):
    if nid not in idx:
        n = json.loads(json.dumps(idx[base])); n['id'] = nid
        n['path'] = [[round(1060.08 - L421 * 18, 2), y8], [1060.08, y8]]; n['length_ft'] = round(L421, 2); n['faces'] = 1; n['layers'] = 1
        n['board'] = '5/8 type X'
        n['location'] = f"L4 Elec 421 south wall segment (inside W.6-L4-08) | faces: {fx}"
        n['source'] = (f"3/A7.50; A7.50 [DERIVED] length = Elec 421 inside width: CLG-L4-119 10.8 SF (contour measured on 1/A2.04) / 8.77 ft (W.6-L4-09 A) = "
                       f"{L421} ft | rating: {A00} [2/A0.02 ELEC 421] | height: " + str(idx[base].get('height_source')))
        c['walls' if idx[base] in c['walls'] else 'existing_walls'].append(n); idx[nid] = n
        LOG.append(f"{nid} {n['length_ft']} x {n['height_ft']} x 1 = +{round(n['length_ft'] * n['height_ft'], 2)} SF")
    filas.append({"id": nid, "faces": 1, "layers": 1})
tot = round(sum(idx[f['id']]['length_ft'] * idx[f['id']]['height_ft'] * f['faces'] * f['layers'] for f in filas), 2)
c['deduct_alternates'] = [d for d in c.get('deduct_alternates') or [] if d.get('id') != 'DA-6']
c['deduct_alternates'].append({
    "id": "DA-6", "rfi": "RFI-04", "texto": "ELEC 221 / 321 / 421 as drawn on their code plans 3/A0.01, 1/A0.02, 2/A0.02 (1HR FP: 1 layer each face)",
    "delta_sf": -tot, "material": '5/8" Type X', "filas": filas,
    "operacion": " + ".join(f"{f['id']} {idx[f['id']]['length_ft']} x {idx[f['id']]['height_ft']} x {f['faces']} face(s) x {f['layers']} layer(s)" for f in filas) + f" = {tot} SF"})
LOG.append(f"ELEC 2 HR total +{tot} SF Type X; DA-6 -{tot}")
for w in WALLS + [idx[k] for k in ('W.6-L4-08 C', 'W.6-L4-08 D')]:
    if 'DA6TOT' in str(w.get('source')):
        w['source'] = str(w['source']).replace('DA6TOT', f"{tot:.2f}")

# ---- 2. cove de corridor 7/A7.23 = madera (Div. 06 EXCLUDED) ----
COVE = ('SOF-L2-01', 'SOF-L2-02', 'SOF-L3-316', 'SOF-L3-318', 'SOF-L4-02')
fuera = [m for m in c['misc_items'] if m['ref'] in [f"{r} track" for r in COVE] + [f"{r} cripples" for r in COVE]]
if fuera:
    c['misc_items'] = [m for m in c['misc_items'] if m not in fuera]
    trk = round(sum(m['qty'] for m in fuera if m['ref'].endswith(' track')), 2); crp = round(sum(m['qty'] for m in fuera if m['ref'].endswith(' cripples')), 2)
    c.setdefault('wood_excluded', [])
    c['wood_excluded'] = [x for x in c['wood_excluded'] if not (isinstance(x, dict) and x.get('id') == 'COVE-7A723')] if isinstance(c['wood_excluded'], list) else c['wood_excluded']
    nota = {"id": "COVE-7A723", "items": [m['ref'] for m in fuera],
            "reason": ("7/A7.23 'WALL DETAIL - CORRIDOR CEILING' draws the cove framing members with the wood symbol (box with X, the same as the wall top "
                       "plates of the detail); the GYP-1 legend 'GYPSUM BOARD ON METAL SUSPENSION SYSTEM, OR WOOD FRAMING' allows either and the specific "
                       "detail governs (R-ALC-10) -> wood framing, Div. 06 EXCLUDED (U-139); the gypsum board of the coves stays loaded"),
            "delta_if_metal": f"+{trk} LF ceiling / soffit track, +{crp} LF 2-1/2\" cripple studs"}
    if isinstance(c['wood_excluded'], list):
        c['wood_excluded'].append(nota)
    else:
        c['wood_excluded_cove'] = nota
    for r in COVE:
        b = next((m for m in c['misc_items'] if m['ref'] == f"{r} board"), None)
        if b and 'Div. 06 EXCLUDED' not in str(b['source']):
            b['source'] = str(b['source']) + " | cove framing = wood per 7/A7.23 (wood symbol), Div. 06 EXCLUDED; board only (R-ALC-10, U-139)"
    LOG.append(f"cove 7/A7.23 wood: -{trk} LF track, -{crp} LF cripples (Div. 06 EXCLUDED)")
DET = {'SOF-L1-01': "5/A7.31 'DETAIL - LOBBY CEILING' draws the coffer drop with no X-box member (PLASTER FINISH, metal 'T' grid 7/A7.31)",
       'SOF-L4-01': "11/A6.01 'GYP BD SOFFIT AT FCU. CONTINUES FULL WIDTH OF STAIR.' (framing not drawn: standing rule R-ALC-01 / BE-CF11, metal option when the detail does not choose)"}
for m in c['misc_items']:
    r = m['ref'].replace(' cripples', '')
    if m['ref'].endswith(' cripples') and r in DET and 'wood' in str(m['source']):
        m['source'] = (str(m['source']).split(' | R-ALC-01')[0] + f" | {DET[r]}: metal framed soffit (GYP-1 legend 'GYPSUM BOARD ON METAL SUSPENSION "
                       "SYSTEM') = top + bottom track + cripple studs at 16\" o.c. (A0.06 GN 6); stud size not printed: 2-1/2\"")
# ---- 3. áreas sin número del RCP (blancos.json, medidas en vectores) ----
B = json.load(open(f'{W}/etapas/4_canon/rev16/blancos.json'))
TP = f'{W}/etapas/4_canon/rev14/rcp_cuartos.json'; T = json.load(open(TP))
ya_t = {(r['sheet'], r['room']) for r in T['rooms']}
def cen(P):
    return [round(sum(q[0] for q in P) / len(P), 1), round(sum(q[1] for q in P) / len(P), 1)]
STAIR_ROWS = {}
for x in c['ceilings']:
    if x['room'].startswith('L4 Lobby stair'):
        STAIR_ROWS['stair-W'] = x['room']
    elif x['room'].startswith('L4 SE stair 413'):
        STAIR_ROWS['stair-E'] = x['room']
for it in B['items']:
    k = (it['sheet'], it['room'])
    if it.get('action') == 'EXCLUDED' and k not in ya_t:
        T['rooms'].append({"sheet": it['sheet'], "room": it['room'], "name": it['room'], "disposition": "exclusion", "vertical": it['vertical'],
                           "rows": [], "nhoja": it['nhoja'], "reason": it['reason'], "reason_short": it['reason'], "polygon": it['polygon'],
                           "area_sf": it['area_sf'], "label_xy": cen(it['polygon']), "polygon_src": it.get('poly_method'), "img": it.get('img')})
        LOG.append(f"{it['sheet']} {it['room']}: EXCLUDED ({it['reason']})")
    elif k in ya_t:
        for r in T['rooms']:
            if (r['sheet'], r['room']) == k:
                r['vertical'] = it['vertical']
    elif it['sheet'] == 'A3.04' and it['vertical'] in STAIR_ROWS:
        T['rooms'].append({"sheet": "A3.04", "room": it['room'], "disposition": "row", "vertical": it['vertical'], "rows": [STAIR_ROWS[it['vertical']]]})
    elif it['sheet'] == 'A3.01' and it['vertical'] in ('shaft-N', 'shaft-S'):
        T['rooms'].append({"sheet": "A3.01", "room": it['room'], "disposition": "row", "vertical": it['vertical'],
                           "rows": ["CLG-L1-SHN board" if it['vertical'] == 'shaft-N' else "CLG-L1-SHS board"]})
for r in T['rooms']:   # entradas previas de A3.04 sin la clave
    if r['sheet'] == 'A3.04' and not r.get('vertical'):
        for v, pat in (('hoistway-service', 'service elevator hoistway'), ('hoistway-lobby', 'lobby elevator hoistway'), ('shaft-N', 'north shaft'), ('shaft-S', 'south shaft')):
            if pat in r['room']:
                r['vertical'] = v
E = B['elec_tele_120_A7.50']
if ('A7.50', '120') not in ya_t:
    T['rooms'].append({"sheet": "A7.50", "room": "120", "name": "ELEC/TELE", "disposition": "exclusion", "rows": [], "nhoja": "2/A7.50",
                       "reason": "lay-in ACT ceiling (ACT grid drawn, no tag), not drywall scope; FS-1 rated membrane above is loaded",
                       "reason_short": "lay-in ACT ceiling (ACT grid drawn, no tag), not drywall scope; FS-1 rated membrane above is loaded",
                       "polygon": E['polygon'], "area_sf": E['area_sf'], "label_xy": cen(E['polygon'])})
    LOG.append("A7.50 120 ELEC/TELE: EXCLUDED (ACT grid)")
Pz = B['passage_410_411_A3.04']
if ('A3.04', Pz['room']) not in ya_t:
    rs = "Food & Beverage interior not in scope of this permit, future TI permit (passage reached only from 410 / 411)"
    T['rooms'].append({"sheet": "A3.04", "room": Pz['room'], "disposition": "exclusion", "rows": [], "nhoja": "1/A2.04", "reason": rs, "reason_short": rs,
                       "polygon": Pz['polygon'], "area_sf": Pz['area_sf'], "label_xy": cen(Pz['polygon'])})
    LOG.append("A3.04 passage 410/411: EXCLUDED (F&B, 1/A2.04)")
json.dump(T, open(TP, 'w'), indent=1)
# WS-1 del corridor 412 de L4: RS-1 continuo arriba (supuesto conservador, U-048; en L2 / L3 la membrana FS-1 sigue sobre el WS-1)
Wq = B['ws1_corridor_412_A3.04']; A = Wq['area_sf']
if not any(m['ref'] == 'CLG-L4-412WS board' for m in c['misc_items']):
    srcw = (f"L4 Corridor 412 WS-1 wood slat area: A3.04 [DERIVED] area {A} SF ({Wq['area_op']}) | the corridor 412 RS-1 field had a hole here; the WS-1 "
            "slats hang from their own grid below (6/A7.23 WOOD SLAT DETAIL 2, 5/A7.23 'HANGER WIRE BY OTHERS'); whether the RS-1 board continues above "
            "the WS-1 is not printed -> conservative (U-048): RS-1 continuous like the FS-1 over the WS-1 at L2 / L3 | RS-1 board on resilient channel "
            "(A0.08 RS-1); [CONFIRMED] height 8.94 (1/A5.06 8'-11 1/4\")")
    c['misc_items'] += [{"ref": "CLG-L4-412WS board", "familia": '5/8" gyp board Type X', "qty": A, "op": f"{A} SF x 1 layer(s) = {A}", "source": srcw, "detail": "1/A3.04 (WS-1, RS-1)"},
                        {"ref": "CLG-L4-412WS RC", "familia": "resilient channel (printed)", "qty": round(A * 0.75, 2), "op": f"{A} SF x 12 / 16 in. o.c. = {round(A * 0.75, 2)} LF",
                         "source": srcw + " | resilient channel 16 in. o.c. (RFI-14)", "detail": "A0.08 RS-1"}]
    KZ = {"CLG-L4-412WS": {"sheet": "A3.04", "polygons_final": [Wq['polygon']], "polygon": Wq['polygon'], "area_sf": A, "nhoja": "1/A3.04",
                           "metodo": "WS-1 rectangle measured in vectors on 1/A3.04 (hatch border lines)"}}
    json.dump(KZ, open(f'{W}/etapas/4_canon/rev9/contornos_zR16.json', 'w'), indent=1)
    LOG.append(f"CLG-L4-412WS +{A} SF Type X, +{round(A * 0.75, 2)} LF RC (RS-1 over the L4 WS-1, conservative)")
# L1 FS-1: sin membrana sobre los hoistways (atraviesan el piso de L2) ni sobre las bases de shaft (el 2HR shaft ceiling es su fondo)
f1 = next(x for x in c['ceilings'] if x['room'].startswith('L1 FS-1 membrane'))
if 'hoistways and shaft bases cut' not in str(f1['source']):
    P = f1['contorno_polygon']
    def sa(Q):
        return sum(Q[i][0] * Q[(i + 1) % len(Q)][1] - Q[(i + 1) % len(Q)][0] * Q[i][1] for i in range(len(Q))) / 2
    so = sa(P)
    holes = [next(i['polygon'] for i in B['items'] if i['sheet'] == 'A3.01' and i['vertical'] == v) for v in ('hoistway-service', 'hoistway-lobby')]
    holes += [[[735.26, 436.49], [755.51, 436.49], [755.51, 475.21], [735.26, 475.21]], [[771.95, 1096.33], [804.95, 1096.33], [804.95, 1114.43], [771.95, 1114.43]]]
    cut = 0.0
    for H in holes:
        H = H if (sa(H) > 0) != (so > 0) else H[::-1]
        cut += abs(sa(H)) / 81
        P = P[:9] + [H[0], H[1], H[2], H[3], H[0], P[8]] + P[9:]   # keyhole desde el vértice (642.02, 372.3)
    new_a = round(abs(sa(P)) / 81, 2)
    old = f1['area_sf']; f1['contorno_polygon'] = P; f1['area_sf'] = new_a
    if isinstance(f1.get('contorno'), dict):
        f1['contorno']['area_medida_sf'] = new_a
    f1['source'] = (f"[DERIVED] area {new_a} SF = {old} - {round(cut, 2)} SF (hoistways and shaft bases cut: service hoistway 43.06 + lobby hoistway 64.20 "
                    f"(they pass through the L2 floor, 1-12/A6.00) + north / south shaft bases 9.68 + 7.37 (their 2HR shaft ceiling CLG-L1-SHN / SHS is the "
                    f"bottom, 1/A5.08)) | " + str(f1['source']))
    for k_ in ('area_cause', 'hatch_check_cause'):
        if f1.get(k_):
            f1[k_] = str(f1[k_]).replace(f"{old} SF", f"{new_a} SF")
    LOG.append(f"L1 FS-1 membrane {old} -> {new_a} SF Type C (-{round(cut, 2)})")
c['rev16_cambios'] = LOG
json.dump(c, open(CP, 'w'), indent=1)
print("\n".join(LOG))
