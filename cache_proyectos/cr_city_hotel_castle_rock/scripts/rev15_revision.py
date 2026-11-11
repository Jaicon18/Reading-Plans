"""rev15 (usuario 10-nov 'revisa todo otra vez': revisión completa de rev14 por 3 revisores, 18 puntos de COORDINACIÓN).
Cambios al canon (cada uno con su N/HOJA; nada en silencio):
 1  A0.06 GN 6 'ALL METAL STUDS TO BE SPACED @ 16" O.C. UNLESS NOTED OTHERWISE': C-H studs (shaft walls + MB-1) a 16 in. o.c.
 2  A3.04 duct chases 401 NE / 401-402: stipple de cielo impreso -> cargados como CLG-L4-405C (RS-1 board + RC).
 3  1/A5.08 '2HR SHAFT CEILING' base del north shaft (8/A9.03) + south shaft (7/A9.03, base no cortada): supuesto conservador MB-1
    (A0.08, la única membrana horizontal 2 HR impresa) CARGADO + RFI-29 (U-048).
 8  walls: W.62-L4-02/03 cara corridor continua (+0.77 ft), XW.6.6 L4 exterior continua (9 huecos, +5.76 LF), W.6-L4-09 en dos caras.
 13 118B / 120: 1a capa de las caras 2 HR a la altura de la 2a (13.7917, RFI-28 / IBC 2018 707.5).
 15 hanger wire de corridors: drop 9 1/2" impreso en 7/A7.23.
 12 CBU: mesh tape + setting compound (09 29 00 2.6.E.3, 3.6.G).
 17 cajas de closet del muro exterior de las guest rooms con stipple (1/A3.02, 1/A3.03) -> Type C FS-1 + RC."""
import json, math, re
W = '/root/cr/work'; CP = f'{W}/etapas/4_canon/takeoff_canon.json'
c = json.load(open(CP))
WALLS = c['walls'] + c['existing_walls']
idx = {w['id']: w for w in WALLS}
LOG = []


def nuevo_wall(base, nid, **kw):
    n = json.loads(json.dumps(base)); n['id'] = nid; n.update(kw)
    (c['walls'] if base in c['walls'] else c['existing_walls']).append(n)
    idx[nid] = n
    return n


# ---- 8. walls (revisión walls F01-F03; vectores verificados en A2.04 x=853.6 / A7.50 x=1070.16) ----
if 'W.62-L4-02 C' not in idx:
    b = idx['W.62-L4-02']
    nuevo_wall(b, 'W.62-L4-02 C', path=[[853.6, 613.84], [853.6, 620.8]], length_ft=0.77, faces=1,
               location="L4 Corridor 412 face of W.62-L4-02/03 across the 401/402 DW.4 junction | faces: 412 Corridor (continuous line)",
               source="1/A2.04; A2.04 [DERIVED] length (1/A2.04 vector: corridor face x=853.6 continuous 608.9-625.7 across the DW.4 junction; "
                      "rows W.62-L4-02 / -03 stop at 613.84 and restart at 620.8 -> (620.8-613.84)/9 = 0.77) | full review walls F01",
               decision=b['decision'], img=b.get('img'), tag_ids=[])
    LOG.append("W.62-L4-02 C +0.77 LF x 10.4375 x 1 face x 2 layers = +16.07 SF")
EXT = ['XW.6.6-L4-03 B', 'XW.6.6-L4-04 A', 'XW.6.6-L4-05 A', 'XW.6.6-L4-06 A', 'XW.6.6-L4-07 A', 'XW.6.6-L4-08 A', 'XW.6.6-L4-09 A',
       'XW.6.6-L4-10 A', 'XW.6.6-L4-11 A', 'XW.6.6-L4-12 B', 'XW.6.6-L4-13 C', 'XW.6.6-L4-14 B', 'XW.6.6-L4-15 B']
segs = [idx[i] for i in EXT]
for a in segs:
    if 'exterior face continuous across' in str(a['source']):
        continue
    (x0, y0), (x1, y1) = a['path']
    hor = abs(y0 - y1) < 0.01
    sig = [b for b in segs if b is not a and abs((b['path'][0][1] if hor else b['path'][0][0]) - (y0 if hor else x0)) < 0.01
           and 0 < ((b['path'][0][0] - x1) if hor else (b['path'][0][1] - y1)) < 9.0]
    if sig:
        nb = sig[0]['path'][0]
        gap = round(((nb[0] - x1) if hor else (nb[1] - y1)) / 9.0, 4)
        a['path'] = [[x0, y0], [nb[0], y0] if hor else [x0, nb[1]]]
        L0 = a['length_ft']; a['length_ft'] = round(L0 + gap, 2)
        a['source'] = str(a['source']) + (f" | exterior face continuous across the interior wall junction (review walls F02; A2.04 exterior "
                                          f"line continuous; as L2 / L3): {L0} + gap {gap} ft to {sig[0]['id']} = {a['length_ft']}")
        LOG.append(f"{a['id']} {L0} -> {a['length_ft']} LF (+{gap} x {a['height_ft']} = +{round(gap * a['height_ft'], 2)} SF sheathing)")
w9 = idx['W.6-L4-09']
if w9['faces'] == 2:
    w9['faces'] = 1; w9['path'] = [[1060.08, 1145.04], [1060.08, 1302.84]]
    w9['location'] = "L4 Elec 421 east wall | faces: 421 Elec"
    _s9 = str(w9['source']); _k = _s9.find(' | height')
    _n9 = " | full review walls F03: split by face, 421 face x=1060.08 1145.04-1302.84 = 8.77 ft"
    w9['source'] = (_s9[:_k] + _n9 + _s9[_k:]) if _k >= 0 else _s9 + _n9
    nuevo_wall(w9, 'W.6-L4-09 B', path=[[1070.16, 1134.96], [1070.16, 1312.92]], length_ft=9.89,
               location="L4 corridor 412 face of the Elec 421 east wall | faces: 412 Corridor",
               source="3/A7.50; A7.50 [DERIVED] length (3/A7.50 vectors at 18 pt/ft: corridor face x=1070.16 from 1134.96 to 1312.92 = 177.96/18 = 9.89) "
                      "| full review walls F03 | height: " + str(w9.get('height_source')))
    LOG.append("W.6-L4-09 corridor face 8.77 -> 9.89 (+1.12 x 10.225 = +11.45 SF)")

for _old, _new in (('W.62-L4-02', 'W.62-L4-02 A'), ('W.6-L4-09', 'W.6-L4-09 A')):   # CB_BE_VS_13: el markup agrupa por id base
    if _old in idx and _new not in idx:
        idx[_old]['id'] = _new; idx[_new] = idx.pop(_old)

# ---- 13. 118B / 120: 1a capa de las caras 2 HR hasta 13.7917 (RFI-28, IBC 2018 707.5) ----
BAND = [('W.6-L1-20 D', 'W.6-L1-20 C', 2, "DATA 118B; BREAK 115 (1st layer each side, 12.0 -> 13.7917)"),
        ('W.6-L1-23 G', 'W.6-L1-23 C', 1, "ELEC/TELE 120 (1st layer, 12.0 -> 13.7917)"),
        ('W.6-L1-23 H', 'W.6-L1-23 E', 1, "DATA 118B (1st layer, 12.0 -> 13.7917)")]
for nid, bid, fc, fx in BAND:
    if nid in idx:
        continue
    b = idx[bid]
    hs = ("DERIVED: 13.7917 - 12.0 = 1.7917 ft (band above the 1st-layer rows W.6-L1-20 A/B and W.6-L1-23 B, which stop at 12'-0\" B.O. DECK "
          "5/A5.04; every layer of the 2 HR fire barrier to the underside of the floor sheathing, IBC 2018 Section 707.5, as the 2nd layer RFI-28)")
    nuevo_wall(b, nid, faces=fc, layers=1, height_ft=1.7917, height_source=hs, height_note=hs, height_status='DERIVADO',
               location=f"L1 {b['location'].split('|')[0].replace('L1 ', '').strip()} - 1st layer band 12.0 to 13.7917 | faces: {fx}",
               source=str(b['source']).split(' | ')[0] + f" | full review rfi F10: 1st layer of the 2 HR faces raised to the 2nd layer height; {hs}")
    LOG.append(f"{nid} {b['length_ft']} x 1.7917 x {fc} = +{round(b['length_ft'] * 1.7917 * fc, 2)} SF")

# ---- 1. C-H studs a 16" o.c. (A0.06 GN 6) ----
GN6 = "A0.06 GENERAL NOTE 6 'ALL METAL STUDS TO BE SPACED @ 16\" O.C. UNLESS NOTED OTHERWISE' (spec 09 21 16.23 3.1.A.1 'comply with framing spacing indicated')"
RXS = re.compile(r"ROUNDUP\(([\d.]+)/2\.0\)\+1 = (\d+) studs x (span )?([\d.]+) ft(.*?)= ([\d.]+)")
for m in c['misc_items']:
    if not re.search(r"C-H stud", m.get('familia', '')) or 'GN 6' in str(m.get('op')) or 'GENERAL NOTE 6' in str(m.get('source')):
        continue
    old = m['qty']; mo = RXS.search(str(m.get('op')))
    if mo:
        L, sp, H = float(mo.group(1)), mo.group(3) or '', float(mo.group(4))
        n = math.ceil(round(L / (16 / 12.0), 6)) + 1
        m['qty'] = round(n * H, 2)
        m['op'] = f"ROUNDUP({L}/1.3333)+1 = {n} studs x {sp}{H} ft{mo.group(5)}= {m['qty']} (16 in. o.c., A0.06 GN 6)" + str(m['op'])[mo.end():]
    else:   # filas escaladas por área (CLG-L1-01 / CLG-L1-18): mismo factor x 24/16
        mo = re.match(r"\s*([\d.]+) SF x ([\d.]+) = ([\d.]+)", str(m['op']))
        A, f = float(mo.group(1)), float(mo.group(2))
        f2 = round(f * 24 / 16, 4); m['qty'] = round(A * f2, 2)
        m['op'] = f"{A} SF x {f2} = {m['qty']} (factor {f} at 24 in. o.c. x 24/16 -> 16 in. o.c., A0.06 GN 6)" + str(m['op'])[mo.end():]
    m['source'] = re.sub(r"spacing 24 in\. o\.c\. per UL U415( \(not printed on A0\.06\))?|@ 24\" o\.c\.?", "@ 16\" o.c. (A0.06 GN 6)", str(m['source']))
    m['source'] = str(m['source']) + f" | {GN6}; UL U415 allows up to 24 in., the printed note governs (16 in.)"
    LOG.append(f"{m['ref']} {old} -> {m['qty']} LF")

for w in WALLS:   # stud_text del Partition Takeoff (rev10) con el espaciado impreso
    if '@ 24" o.c.' in str(w.get('stud_text')):
        w['stud_text'] = w['stud_text'].replace('@ 24" o.c.', '@ 16" o.c. (A0.06 GN 6)')
    if 'UL U415' in str(w.get('decision')) and 'GN 6' not in str(w.get('decision')):
        w['decision'] = str(w['decision']) + ' | C-H studs @ 16" o.c. (A0.06 GN 6)'

# ---- 15. hanger wire de corridors: drop 9 1/2" impreso en 7/A7.23 ----
for m in c['misc_items']:
    if m['familia'] == 'hanger wire' and m['ref'].split(' ')[0] in ('CLG-L2-56', 'CLG-L2-58', 'CLG-L3-87', 'CLG-L3-88') and '9 1/2' not in str(m['op']):
        A = float(re.match(r"\s*([\d.]+) SF", m['op']).group(1)); n = math.ceil(A / 16); old = m['qty']
        m['qty'] = round(n * 0.7917, 2)
        m['op'] = f"ROUNDUP({A}/16) = {n} hangers (4 ft x 4 ft) x drop 0.7917 ft (9 1/2\" printed on 7/A7.23) = {m['qty']}"
        m['source'] = str(m['source']) + " | full review rfi F12: drop 9 1/2\" printed on 7/A7.23 'WALL DETAIL - CORRIDOR CEILING' (was 0.5 ft by scaling)"
        LOG.append(f"{m['ref']} {old} -> {m['qty']} LF")

ya = {m['ref'] for m in c['misc_items']}
KZ = {}


def area_poly(P):
    return abs(sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))) / 2


# ---- 17. cajas de closet del muro exterior (1/A3.02, 1/A3.03) con stipple sin renglón ----
CB = json.load(open(f'{W}/etapas/4_canon/rev15/chase_boxes.json'))
for bx in CB['boxes']:
    if bx.get('status') != 'NOT LOADED' or not bx.get('stipple'):
        continue
    fl = 'L2' if bx['sheet'] == 'A3.02' else 'L3'
    rid = f"CLG-{fl}-{bx['unit']}C"; A = float(bx['area_sf'])
    KZ[rid] = {"sheet": bx['sheet'], "polygons_final": [bx['polygon']], "polygon": bx['polygon'], "area_sf": A, "nhoja": f"1/{bx['sheet']}",
               "img": bx.get('img'), "metodo": "rev15 F06: box measured in vectors on the RCP (wall faces)"}
    if f"{rid} board" in ya:
        continue
    src = (f"{fl} Guest room {bx['unit']} closet box at the exterior wall: {bx['sheet']} [DERIVED] area {A} SF ({bx['area_op']}) | stipple of the "
           f"unit ceiling printed inside the box on 1/{bx['sheet']} (review rcp F06; was notched out of the FS-1 polygon without a row) | "
           f"FS-1 (A0.08: 5/8\" TYPE C GYP BD CEILING, RESILIENT CHANNELS, UL L546) as the unit")
    c['misc_items'].append({"ref": f"{rid} board", "familia": '5/8" gyp board Type C', "qty": A, "op": f"{A} SF x 1 layer(s) = {A}",
                            "source": src, "detail": f"1/{bx['sheet']} (stipple, FS-1)"})
    rc = round(A * 12 / 16, 2)
    c['misc_items'].append({"ref": f"{rid} RC", "familia": "resilient channel (printed)", "qty": rc, "op": f"{A} SF x 12 / 16 in. o.c. = {rc} LF",
                            "source": src + " | resilient channel 16 in. o.c. (UL L546 / FS-1, as the unit rows; RFI-14)", "detail": "A0.08 FS-1"})
    LOG.append(f"{rid} +{A} SF Type C, +{rc} LF RC")

# ---- 2. duct chases A3.04 (401 NE, 401/402) ----
TP = f'{W}/etapas/4_canon/rev14/rcp_cuartos.json'
T = json.load(open(TP))
GEO = {}
try:
    GEO = json.load(open(f'{W}/etapas/4_canon/rev15/geometria_rcp.json'))
except Exception:
    pass
DUCT = {'(401 NE duct chase, no number)': 'CLG-L4-401D', '(401/402 duct chase, no number)': 'CLG-L4-402D'}
for r in T['rooms']:
    if r['sheet'] == 'A3.04' and r['room'] in DUCT:
        rid = DUCT[r['room']]; P = r['polygon']; A = round(area_poly(P) / 81.0, 2)
        r['disposition'] = 'missing_loaded'; r['rows'] = [rid + ' board']
        r.pop('reason', None); r.pop('reason_short', None)
        KZ[rid] = {"sheet": "A3.04", "polygons_final": [P], "polygon": P, "area_sf": A, "nhoja": "1/A3.04", "img": r.get('img'),
                   "metodo": "rev15 F01: chase measured in vectors on 1/A3.04 (wall faces)"}
        if f"{rid} board" in ya:
            continue
        src = (f"L4 {r['room']}: A3.04 [DERIVED] area {A} SF (polygon measured in vectors on 1/A3.04 / 81) | ceiling stipple printed inside the chase on "
               f"1/A3.04 (full review rcp F01: the earlier exclusion 'no ceiling drawn' was wrong) | treated as CLG-L4-405C")
        c['misc_items'].append({"ref": f"{rid} board", "familia": '5/8" gyp board Type X', "qty": A, "op": f"{A} SF x 1 layer(s) = {A}",
                                "source": src + " | RS-1 board on resilient channel under the roof (A0.08 RS-1; unit General Note 1 A7.00); [CONFIRMED] height 8.94 (1/A5.06 8'-11 1/4\")",
                                "detail": "1/A3.04 (stipple, RS-1)"})
        rc = round(A * 12 / 16, 2)
        c['misc_items'].append({"ref": f"{rid} RC", "familia": "resilient channel (printed)", "qty": rc, "op": f"{A} SF x 12 / 16 in. o.c. = {rc} LF",
                                "source": src + " | resilient channel 16 in. o.c. (UL L546 / RS-1, as the L4 RS-1 rows)", "detail": "A0.08 RS-1"})
        LOG.append(f"{rid} +{A} SF Type X, +{rc} LF RC")

# ---- 3. 2HR SHAFT CEILING (1/A5.08) base north shaft (8/A9.03) + south shaft (7/A9.03): MB-1 conservador + RFI-29 ----
SH = [("CLG-L1-SHN", "north", 2.25, 4.3021, "8/A9.03 shaft interior 2'-3\" x 4'-3 5/8\" [CONFIRMED]", [[735.26, 436.49], [755.51, 436.49], [755.51, 475.21], [735.26, 475.21]]),
      ("CLG-L1-SHS", "south", 3.6667, 2.0104, "7/A9.03 shaft interior 3'-8\" x 2'-0 1/8\" [CONFIRMED]", [[771.95, 1096.33], [804.95, 1096.33], [804.95, 1114.43], [771.95, 1114.43]])]
for rid, nm, a, b_, dims, P in SH:   # rev16 #6: la membrana está en el plenum de L1 (1/A5.08) -> RCP de L1 (A3.01, misma posición de núcleo que A3.02-A3.04)
    A = round(a * b_, 2)
    KZ[rid] = {"sheet": "A3.01", "polygons_final": [P], "polygon": P, "area_sf": A, "nhoja": "1/A5.08",
               "metodo": f"{nm} shaft base at the L1 ceiling plenum (1/A5.08), drawn on the L1 RCP 1/A3.01 at the core position shared by A3.01-A3.04 (inner dims of {dims.split(' [')[0]})"}
    if f"{rid} board" in ya:
        continue
    base = ("1/A5.08 '2HR SHAFT CEILING' + 'STEEL SUPPORT PLATFORM WITH 2HR RATED FIRE PROOFING' at the base of the north shaft (11/A9.03 WALL SECTION - "
            "BASE OF NORTH SHAFT draws the platform only)" if nm == 'north' else
            "south shaft (7/A9.03, CH-L2-01..04 from LEVEL 2): no section cuts its base (only 10/A9.03 head of shaft); IBC 2018 Section 713.11 "
            "'Enclosure at the bottom' item 1: enclosed at the lowest level with construction of the same rating as the shaft (2 HR)")
    src = (f"L1/L2 base of the {nm} shaft: [DERIVED] area {a} x {b_} = {A} SF ({dims}) | {base} | assembly NOT printed -> conservative assumption "
           f"LOADED (U-048, RFI-29): A0.08 MB-1 (the only 2 HR horizontal membrane printed in the set: 3 LAYERS 5/8\" GYP. BD., 1\" GYP. BD. LINER, "
           f"STEEL STUDS w/ C-CHANNEL, J-TRACK), studs @ 16\" o.c. (A0.06 GN 6)")
    ns = math.ceil(round(max(a, b_) / (16 / 12.0), 6)) + 1; sp_ = min(a, b_)
    c['misc_items'] += [
        {"ref": f"{rid} board", "familia": '5/8" gyp board Type X', "qty": round(A * 3, 2), "op": f"{A} SF x 3 layers = {round(A * 3, 2)}",
         "source": src, "detail": "1/A5.08"},
        {"ref": f"{rid} liner", "familia": '1" gypsum shaftliner panel', "qty": A, "op": f"{A} SF x 1 layer = {A}", "source": src + ": 1\" liner",
         "detail": "1/A5.08"},
        {"ref": f"{rid} C-H studs", "familia": 'C-H stud 6" (printed)', "qty": round(ns * sp_, 2),
         "op": f"ROUNDUP({max(a, b_)}/1.3333)+1 = {ns} studs x span {sp_} ft = {round(ns * sp_, 2)} (16 in. o.c., A0.06 GN 6)", "source": src + ": steel studs (6\" C-H as MB-1, RFI-13)",
         "detail": "1/A5.08"},
        {"ref": f"{rid} J-track", "familia": 'J-runner 6" (printed)', "qty": round(2 * max(a, b_), 2), "op": f"2 x {max(a, b_)} (J-TRACK both bearing walls) = {round(2 * max(a, b_), 2)}",
         "source": src + ": J-TRACK", "detail": "1/A5.08"}]
    LOG.append(f"{rid} {A} SF: +{round(A * 3, 2)} SF Type X, +{A} SF liner, +{round(ns * sp_, 2)} LF C-H 6\", +{round(2 * max(a, b_), 2)} LF J-runner")

# ---- 12. CBU: juntas por fabricante (09 29 00 2.6.E.3 / 3.6.G) ----
cbu = round(sum(round(float(w['length_ft']) * float(w['height_ft']) * int(w['faces']) * int(w.get('layers') or 1), 2) for w in WALLS   # = familia '5/8" cement board' de canon.py (por fila redondeada)
                if 'cement board' in str(w.get('board'))), 2)
if 'CBU joint mesh tape' not in ya:
    s12 = ("spec 09 29 00 2.6.E.3 'Joint Compound for Tile Backing Panels - Cementitious Backer Units: As recommended by backer unit manufacturer' "
           "+ 3.6.G 'Finish cementitious backer units to comply with unit manufacturer's directions' (A0.06 GN 13: CBU at every partition to receive "
           "ceramic tile); board SF = the cement board rows of the Partition Takeoff")
    c['misc_items'] += [
        {"ref": "CBU joint mesh tape", "familia": "alkali-resistant mesh tape (printed)", "qty": round(cbu * 0.37, 2),
         "op": f"{cbu} SF cement board x 0.37 LF/SF (Inputs joint tape yield) = {round(cbu * 0.37, 2)}", "source": s12, "detail": "09 29 00 2.6.E.3"},
        {"ref": "CBU joint setting compound", "familia": "setting-type joint compound at cement board (printed)", "qty": round(cbu * 0.072, 2),
         "op": f"{cbu} SF cement board x 0.072 lb/SF (Inputs joint compound yield) = {round(cbu * 0.072, 2)}", "source": s12, "detail": "09 29 00 2.6.E.3"}]
    LOG.append(f"CBU {cbu} SF: +{round(cbu * 0.37, 2)} LF mesh tape, +{round(cbu * 0.072, 2)} LB setting compound")

# ---- 6 / 7. U-160: polígono obligatorio + vista RCP correcta (geometria_rcp.json, medida en vectores) ----
G2 = GEO.get('2_poligonos_exclusiones') or {}
POL = {('A3.04', '410'): G2.get('A3.04 410', {}).get('polygon'), ('A3.04', '411'): G2.get('A3.04 411', {}).get('polygon'),
       ('A3.04', '(410.3 vestibule, no number)'): G2.get('A3.04 (410.3 vestibule, no number)', {}).get('polygon'),
       ('A3.04', '420'): (G2.get('A3.04 420 / 421 (terrace)', {}).get('420') or {}).get('polygon'),
       ('A3.04', '421 (terrace)'): (G2.get('A3.04 420 / 421 (terrace)', {}).get('421') or {}).get('polygon'),
       ('A7.45', '101'): G2.get('A7.45 101 Corridor', {}).get('polygon')}
p419 = next((r['polygon'] for r in T['rooms'] if r['sheet'] == 'A3.04' and r['room'] == '419'), None)
V = {}
for x in GEO.get('1b_markups_en_vista_plan') or []:
    if x.get('room') and x.get('polygon_correct'):
        V[(x['sheet'], x['room'])] = x
for r in T['rooms']:
    if r.get('disposition') != 'exclusion':
        continue
    k = (r['sheet'], r['room'])
    if k in POL and POL[k] and not r.get('polygon'):
        r['polygon'] = POL[k]; r['polygon_src'] = "rev15: wall faces measured in vectors (geometria_rcp.json)"
    if k in V and r.get('polygon') and abs(r['polygon'][0][1] - V[k]['polygon_now'][0][1]) < 1.0:
        r['polygon'] = V[k]['polygon_correct']; r['polygon_src'] = f"rev15: moved to the RCP view ({V[k]['correct_view']}, dy {V[k]['dy']} pt)"
    if k == ('A7.45', '102') and not r.get('draw_sheet'):
        r['polygon'] = [[q[0] / 2 - 173, q[1] / 2 + 166] for q in r['polygon']]; r['draw_sheet'] = 'A3.01'
        r['polygon_src'] = "rev15: 3/A7.45 is a plan (no enlarged RCP) -> drawn on 1/A3.01 (x/2-173, y/2+166)"
    if k == ('A7.45', '122') and not r.get('draw_sheet'):
        r['polygon'] = [[q[0] / 2 - 206, q[1] / 2 + 570] for q in r['polygon']]; r['draw_sheet'] = 'A3.01'
        r['polygon_src'] = "rev15: 2/A7.45 is a plan (no enlarged RCP) -> drawn on 1/A3.01 (x/2-206, y/2+570, coverage 1.0)"
    if k == ('A7.45', '(NW box, no number)') and not r.get('draw_sheet'):
        pnw = G2.get('A7.45 (NW box, no number)', {}).get('polygon')
        r['polygon'] = [[q[0] / 2 - 173, q[1] / 2 + 166] for q in pnw]; r['draw_sheet'] = 'A3.01'; r['nhoja'] = '1/A3.01'
        r['reason'] = r['reason_short'] = "exterior equipment box outside the building (1/A2.01), not drawn on the RCP, no ceiling"
        r['polygon_src'] = "rev15 (review rcp F07): the box is outside the building; 1/A3.01 does not draw it (edge coverage 0.12) -> outline at its 1/A3.01 position"
    if k == ('A7.50', '419') and p419:
        r['polygon'] = p419; r['draw_sheet'] = 'A3.04'
        r['polygon_src'] = "rev15: A7.50 has no L4 RCP (3/A7.50 is a plan) -> drawn on 1/A3.04 with the A3.04 419 outline"
        a419 = next(x for x in T['rooms'] if x['sheet'] == 'A3.04' and x['room'] == '419')
        r['reason'] = a419.get('reason'); r['nhoja'] = a419.get('nhoja')
# ---- 14. cove / soffit framing: R-ALC-01 (GYP-1 'ON METAL SUSPENSION SYSTEM, OR WOOD FRAMING' -> metal); 7/A7.23 draws the cove pieces with the
# wood symbol (X) but no text -> the standing rule governs (BE-CF11); metal option complete = 2 tracks + cripple studs @ 16" o.c. (A0.06 GN 6)
for m in list(c['misc_items']):
    if not (m['ref'].startswith('SOF-') and m['ref'].endswith(' track')):
        continue
    rid = m['ref'][:-6]
    if f"{rid} cripples" in ya:
        continue
    b = next(x for x in c['misc_items'] if x['ref'] == f"{rid} board")
    mo = (re.match(r"\s*([\d.]+) LF x \(([\d.]+) bottom \+ ([\d.]+) vertical\)", b['op']) or re.match(r"\s*([\d.]+) LF x ([\d.]+) ft vertical", b['op'])
          or re.match(r"\s*([\d.]+) x \(([\d.]+) bottom \+ ([\d.]+) face\)", b['op']))
    LF = float(mo.group(1)); vh = float(mo.group(mo.lastindex))
    n = math.ceil(round(LF / (16 / 12.0), 6)) + 1; q = round(n * vh, 2)
    c['misc_items'].append({"ref": f"{rid} cripples", "familia": '2-1/2" stud', "qty": q,
                            "op": f"ROUNDUP({LF}/1.3333)+1 = {n} cripple studs x vertical face {vh} ft = {q} (16 in. o.c., A0.06 GN 6)",
                            "source": (f"{str(b['source']).split('|')[0].strip()} | framed soffit vertical face {vh} ft (op of {rid} board) | R-ALC-01 / BE-CF11: the "
                                       "GYP-1 legend 'GYPSUM BOARD ON METAL SUSPENSION SYSTEM, OR WOOD FRAMING' -> metal option (7/A7.23 draws the cove pieces with "
                                       "the wood 'X' symbol, no text; wood framing would be Div. 06 EXCLUDED, U-139); metal soffit = top + bottom track (row "
                                       f"{rid} track) + cripple studs at 16\" o.c. (A0.06 GN 6); stud size not printed: 2-1/2\" (review rfi F11)"),
                            "detail": "7/A7.23"})
    LOG.append(f"{rid} cripples +{q} LF 2-1/2\" stud ({n} x {vh})")
for r in T['rooms']:   # bordes que la hoja RCP no dibuja (CE_RCP_CONTORNO): motivo escrito en el polígono EXCLUDED
    if r['sheet'] == 'A3.04' and r['room'] in ('420', '421 (terrace)'):
        r['edge_not_drawn'] = "A3.04 does not draw the roof terraces (no number, no outline); outline = 1/A2.04 terrace edge + offset plan->RCP"
    if r['sheet'] == 'A7.45' and r['room'] == '(NW box, no number)':
        r['edge_not_drawn'] = "the box is drawn only on 1/A2.01 / 3/A7.45 (outside the building); outline at its 1/A3.01 position"
T['rooms'] = [r for r in T['rooms']]
json.dump(T, open(TP, 'w'), indent=1)
MP = f'{W}/etapas/4_canon/rev9/contornos_MISC.json'
M_ = json.load(open(MP))
for k_, sh_ in (('CLG-L2-56', 'A3.02'), ('CLG-L2-58', 'A3.02'), ('CLG-L3-87', 'A3.03'), ('CLG-L3-88', 'A3.03')):
    if M_.get(k_, {}).get('sheet') != sh_:
        M_[k_]['sheet'] = sh_
        M_[k_]['nota_rev15'] = (f"rev15 (review rcp F04): the contour was measured in {sh_} coordinates (edge coverage 0.98-1.0 on {sh_}); "
                                f"labeled A2.0x, so the plan->RCP offset was added twice (coverage 0.28-0.36)")
        LOG.append(f"{k_}: contour sheet -> {sh_} (no double offset)")
json.dump(M_, open(MP, 'w'), indent=1)
for w in WALLS:   # punto 10 (review rfi F06): demising / lobby cerrados por los code plans en rev14 -> sin '[TYPE ASSUMED - RFI-04]'
    if w['id'].split(' ')[0] in ('UNTYPED-L2-01', 'UNTYPED-L2-02', 'NULL-L3-01') and '[TYPE ASSUMED' in str(w.get('location')):
        w['location'] = re.sub(r"\[TYPE ASSUMED - RFI-04\]\s*", "", str(w['location']))
        w['source'] = str(w['source']) + " | rating printed: '1HR FP' demising on 3/A0.01 / 1/A0.02 + A0.00 'CORRIDOR AND UNIT DEMISING WALLS CONSTRUCTED AS 1HR FIRE PARTITIONS' (RFI-04 part closed by the code plans)"
        LOG.append(f"{w['id']}: '[TYPE ASSUMED - RFI-04]' removed (closed by the code plans)")
json.dump(KZ, open(f'{W}/etapas/4_canon/rev9/contornos_zR15.json', 'w'), indent=1)
c.setdefault('rev15_cambios', [])
c['rev15_cambios'] = LOG
json.dump(c, open(CP, 'w'), indent=1)
print("\n".join(LOG))
