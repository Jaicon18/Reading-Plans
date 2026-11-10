"""rev14 (U-156, usuario 10-nov 'en estos planos siempre viene toda la informacion'): re-barrido de los 9 RFI abiertos.
- RFI-04 (parte): las paredes sur de lobby 217 / 317 están impresas '2HR FB' en 3/A0.01 y 1/A0.02 -> W.6-2 (2 capas por cara).
- RFI-23 cerrado A (2/A0.01 2HR FB en los 4 lados + M3.02 fire/smoke damper) -> DA-1 retirado.
- RFI-26 cerrado B (FACP 125 = 7 SF, puerta 125.1 al sur): FI.2-L1-12 ya no se crea (rev9_facp), sin DA-5."""
import json, re
W = '/root/cr/work'; CP = f'{W}/etapas/4_canon/takeoff_canon.json'
c = json.load(open(CP))
for w in c['walls'] + c['existing_walls']:
    if w['id'] in ('UNTYPED-L2-05', 'NULL-L3-10') and int(w.get('layers') or 1) == 1:
        lv = '3/A0.01 LEVEL 2' if w['id'].startswith('UNTYPED') else '1/A0.02 LEVEL 3'
        old = float(w['length_ft']) * float(w['height_ft']) * int(w['faces'])
        w['layers'] = 2; w['type_id'] = 'W.6-2'; w['type'] = 'W.6'
        w['location'] = str(w['location']).replace('[TYPE ASSUMED - RFI-04] ', '')
        w['source'] = str(w['source']) + (f" | rating (U-156): {lv} CODE PLAN prints '2HR FB' on this wall (lobby to the south shaft box) -> 2 HR fire barrier, "
                                          "A0.06 TYPE - W '5/8\" TYPE 'X' GYP BD. TYP. EACH SIDE - 2 LAYERS FOR 2 HR. CONDITION' (W.6-2, UL U301)")
        w['img_rating'] = f"/root/cr/work/etapas/4_canon/img/rev14/RFI-04_{'A0.01' if lv.startswith('3/') else 'A0.02'}.png"
        print('RFI-04', w['id'], '+', round(old, 2), 'SF')
c['deduct_alternates'] = [d for d in c.get('deduct_alternates') or [] if d.get('id') not in ('DA-1', 'DA-5')]
for w in c['walls'] + c['existing_walls']:
    if w['id'] in ('W.6-L1-24', 'W.6-L1-23 C', 'W.6-L1-23 D') and '2/A0.01' not in str(w['source']):
        w['source'] = str(w['source']) + " | 2 HR printed: 2/A0.01 '2HR FB' solid line on all 4 sides of ELEC / TELE 120 + M3.02 keynote 3 fire/smoke damper (RFI-23 closed)"
json.dump(c, open(CP, 'w'), indent=1)
print('DA', [d['id'] for d in c['deduct_alternates']])
# ---- U-159 (usuario 10-nov): cada cuarto de cada hoja RCP = renglón o exclusión. Tabla etapas/4_canon/rev14/rcp_cuartos.json (medida en
# vectores en A3.04 / A7.45 / A7.50). Faltantes cargados aquí como misc con contorno propio en A3.04 (contornos_zR14.json).
import math
TP = f'{W}/etapas/4_canon/rev14/rcp_cuartos.json'
T = json.load(open(TP))
c = json.load(open(CP))
base = {m['ref'].split('CLG-L4-117 ')[1]: m for m in c['misc_items'] if m['ref'].startswith('CLG-L4-117 ')}
ya = {m['ref'] for m in c['misc_items']}
K = {}
NOMBRES = {'417.4 (stall)': 'CLG-L4-117A', '417.3 (stall)': 'CLG-L4-117B', '418.2 (WC compartment)': 'CLG-L4-118A',
           '(405 chase strip, no number)': 'CLG-L4-405C', '(403 SW chase, no number)': 'CLG-L4-403C', '(404/403 W chase, no number)': 'CLG-L4-404C',
           '(chase a, no number)': 'CLG-L4-412A', '(chase b, no number)': 'CLG-L4-412B', '(chase c, no number)': 'CLG-L4-412C'}
for r in T['rooms']:
    if r['sheet'] != 'A3.04' or r.get('disposition') != 'missing_loaded':
        continue
    rid = NOMBRES[r['room']]; A = float(r['area_sf']); P = r['polygon']
    per = round(sum(math.dist(P[i], P[(i + 1) % len(P)]) for i in range(len(P))) / 9.0, 2)
    src = (f"L4 {r['room']}: A3.04 [DERIVED] area {A} SF ({r.get('area_op')}) | measured in vectors on 1/A3.04 (wall faces); U-159 room sweep "
           f"(was without a row) | ceiling: {r.get('tag')} | board: {r.get('board')}")
    K[rid] = {"sheet": "A3.04", "polygons_final": [P], "polygon": P, "area_sf": A, "area_cargar_sf": A, "nhoja": "1/A3.04", "img": r.get('img'),
              "metodo": "U-159: wall faces measured in vectors on 1/A3.04 (rcp_cuartos.json)"}
    r['rows'] = [rid + ' board']; r['disposition'] = 'missing_loaded'
    if f"{rid} board" in ya:
        continue
    if rid.startswith(('CLG-L4-117', 'CLG-L4-118')):   # GYP-1 como el anteroom CLG-L4-117 (misma familia / suspensión)
        f = A / 129.0
        for k, m in base.items():
            n = json.loads(json.dumps(m)); n['ref'] = f"{rid} {k}"; n['source'] = src + " | system as CLG-L4-117 (GYP-1 'GYPSUM BOARD ON METAL SUSPENSION SYSTEM')"
            if k == 'board':
                n['qty'] = A; n['op'] = f"{A} SF x 1 layer(s) = {A}"
            elif k == 'angle molding':
                n['qty'] = per; n['op'] = f"perimeter of the measured polygon on 1/A3.04 = {per} LF"
            elif k == 'hanger wire':
                h = math.ceil(A / 16); n['qty'] = float(h); n['op'] = f"ROUNDUP({A}/16) = {h} hangers x drop 1.0 ft = {float(h)}"
            else:
                n['qty'] = round(float(m['qty']) * f, 2); n['op'] = f"{A} SF x ({m['qty']} / 129.0) = {n['qty']} (same spacing as CLG-L4-117)"
            c['misc_items'].append(n)
    else:                                              # RS-1 board en resilient channel (unit GN 1 / sistema del corridor 412)
        c['misc_items'].append({"ref": f"{rid} board", "familia": '5/8" gyp board Type X', "qty": A, "op": f"{A} SF x 1 layer(s) = {A}",
                                "source": src + f" | RS-1 board on resilient channel under the roof (A0.08 RS-1; unit General Note 1 A7.00); [CONFIRMED] height 8.94 (1/A5.06 8'-11 1/4\")",
                                "detail": "1/A3.04 (stipple, RS-1)"})
        rc = round(A * 12 / 16, 2)
        c['misc_items'].append({"ref": f"{rid} RC", "familia": "resilient channel (printed)", "qty": rc, "op": f"{A} SF x 12 / 16 in. o.c. = {rc} LF",
                                "source": src + " | resilient channel 16 in. o.c. (UL L546 / RS-1, as the L4 RS-1 rows)", "detail": "A0.08 RS-1"})
    print('U-159 loaded', rid, A)
for r in T['rooms']:                                   # 'pending' (sin texto impreso): exclusión con el motivo gráfico impreso y su hoja
    if r.get('disposition') == 'pending':
        r['disposition'] = 'exclusion'
        r['reason'] = {"A7.50": "shaft enclosure (CH.6 | 2), no ceiling drawn on the RCP",
                       "A7.45": "enclosed box, no ceiling drawn on the RCP"}.get(r['sheet'], "duct chase, no ceiling drawn on the RCP")
for r in T['rooms']:                                   # texto del FreeText: motivo + fila de arriba si la hay (FS-1 en L1)
    if r.get('disposition') == 'exclusion':
        rs = str(r.get('reason') or '')
        if re.search(r"INTERIOR OF FOOD AND BEVERAGE", rs, re.I):
            rs = "Food & Beverage interior not in scope of this permit, future TI permit"
        elif re.search(r"ACT-\d", rs):
            rs = "lay-in ACT ceiling (" + re.search(r"ACT-\d", rs).group(0) + "), not drywall scope" + (
                "; FS-1 rated membrane above is loaded" if r.get('rows_above') else "")
        elif 'TERRACE' in rs.upper():
            rs = "exterior roof terrace, no ceiling"
        elif 'hoistway' in rs.lower():
            rs = "elevator hoistway, no ceiling"
        elif 'SHAFT' in rs.upper():
            rs = "2-hour shaft, walls continuous to underside of roof sheathing, no ceiling"
        r['reason_short'] = rs; r['reason'] = rs if len(rs) < 160 else rs[:157] + '...'
# A3.02 / A3.03: todos los cuartos tienen renglón (barrido 10-nov) -> se escriben en la tabla desde el canon
_ya = {(r['sheet'], r['room']) for r in T['rooms']}
for sh, fl, nums in (('A3.02', 'L2', [str(n) for n in range(201, 220)]), ('A3.03', 'L3', [str(n) for n in range(301, 319)])):
    for n in nums:
        if (sh, n) in _ya:
            continue
        rows = [x['room'] for x in c['ceilings'] if x['room'].startswith(fl) and re.search(r'(?<![\d.])' + n + r'(?![\d.])', x['room'])]
        rows += [m['ref'] for m in c['misc_items'] if m['ref'].endswith(' board') and m['ref'].startswith(('CLG-' + fl, 'SOF-' + fl, 'RS6-' + fl))
                 and re.search(r'(?<![\d.])' + n + r'(?![\d.])', str(m['source']).split('|')[0])]
        T['rooms'].append({"sheet": sh, "room": n, "disposition": "row" if rows else "MISSING", "rows": rows})
json.dump(T, open(TP, 'w'), indent=1)
json.dump(K, open(f'{W}/etapas/4_canon/rev9/contornos_zR14.json', 'w'), indent=1)
for m in c['misc_items']:                              # hallazgo U-159: CLG-L1-17 (Toilet 113) se dibujaba en A7.31 con coordenadas de 1/A7.50
    if m['ref'].startswith('CLG-L1-17 ') and 'L1 TOILET 113: A3.01' in str(m['source']):
        m['source'] = str(m['source']).replace('L1 TOILET 113: A3.01', 'L1 TOILET 113: 1/A7.50 (RCP 2/A7.50)', 1)
json.dump(c, open(CP, 'w'), indent=1)
