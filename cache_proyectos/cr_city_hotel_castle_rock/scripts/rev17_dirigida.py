"""rev17 (revisión dirigida de rev16, COORDINACIÓN 10-nov): caras reales de ELEC 221 / 321 / 421 medidas en vectores (rev17/medidas.json),
un tramo = una fila, DA-6 recalculado; WS-1 de L4 un solo criterio (EXCLUDED las 3 zonas: RS-1 sin rating, el RCP imprime WS-1)."""
import json, re
W = '/root/cr/work'; CP = f'{W}/etapas/4_canon/takeoff_canon.json'
c = json.load(open(CP)); M = json.load(open(f'{W}/etapas/4_canon/rev17/medidas.json'))
WALLS = c['walls'] + c['existing_walls']; idx = {w['id']: w for w in WALLS}; LOG = []
A00 = ("A0.00 code summary prints 'ELECTRICAL AND IT ROOMS' '2 HR' (fire barrier ratings) and 'INCIDENTIAL USE AREAS (TABLE 509):' 'ELECTRICAL ROOMS'; "
       "the code plan of the level draws the room 1HR FP -> plan vs plan conflict (IBC 2018 Section 707.3: fire barriers where required): base carries the "
       "larger option (2 HR = 2 layers 5/8\" Type X each face, as DATA 118B), the 1 HR as DEDUCT ALTERNATE DA-6, delta -DA6TOT SF (RFI-04)")
# F1: UNTYPED-L2-12 no encierra ELEC 221 (está al este del corridor 216, junto a LINEN 222)
u = idx['UNTYPED-L2-12']
if int(u.get('layers') or 1) == 2:
    u['layers'] = 1
    u['source'] = re.sub(r" \| rating: A0\.00 .*?\[3/A0\.01 ELEC 221\]", "", str(u['source']))
    u['location'] = "L2 corridor 216 east stub at LINEN 222 / door 222.1 | faces: 222 LINEN; corridor 216"
    u['source'] += (" | full review F1: this stub is EAST of corridor 216 next to LINEN 222 (1/A2.02 x=845.4); ELEC 221 is the closet WEST of the "
                    "corridor behind door 221.1 (x 784.92-799.2) -> no 2 HR layer here")
    LOG.append("UNTYPED-L2-12 2nd layer removed (-41.76 SF): does not enclose ELEC 221")


def nueva(base, nid, path, L, H, faces, board, loc, src):
    n = json.loads(json.dumps(idx[base])); n.update(id=nid, path=path, length_ft=L, height_ft=H, faces=faces, layers=1, board=board, location=loc,
                                                     source=src + " | rating: " + A00 + " | height: " + str(idx[base].get('height_source')))
    (c['walls'] if idx[base] in c['walls'] else c['existing_walls']).append(n); idx[nid] = n
    LOG.append(f"{nid} {L} x {H} x {faces} = +{round(L * H * faces, 2)} SF ({board})")
    return n


F = []
if 'W.4-L2-15 E' not in idx:   # F3: ELEC 221 cara S = muro norte del bath 210 (W.4-L2-15), tramo 0.92 ft
    s221 = "1/A2.02; A2.02 [DERIVED] length = ELEC 221 inside width on the bath 210 north wall: (793.2 - 784.92)/9 = 0.92 ft (vectors, full review F3)"
    nueva('W.4-L2-15 A', 'W.4-L2-15 E', [[784.92, 1202.64], [793.2, 1202.64]], 0.92, 9.2396, 1, '5/8 type X', "L2 ELEC 221 south wall segment | faces: ELEC 221 (2nd layer, 2 HR)", s221)
    nueva('W.4-L2-15 B', 'W.4-L2-15 F', [[784.92, 1206.4], [793.2, 1206.4]], 0.92, 9.2396, 1, '5/8 type X WR', "L2 bath 210 side of the ELEC 221 segment | faces: bath 210 (2nd rated layer under the CBU)", s221)
if 'W.4-L3-26 E' not in idx:   # ELEC 321 cara S = muro norte del bath 310 (W.4-L3-26), tramo 0.96 ft
    s321 = "1/A2.03; A2.03 [DERIVED] length = ELEC 321 inside width on the bath 310 north wall: (793.56 - 784.92)/9 = 0.96 ft (vectors, full review F3)"
    nueva('W.4-L3-26 A', 'W.4-L3-26 E', [[784.92, 1202.64], [793.56, 1202.64]], 0.96, 9.2396, 1, '5/8 type X', "L3 ELEC 321 south wall segment | faces: ELEC 321 (2nd layer, 2 HR)", s321)
    nueva('W.4-L3-26 B', 'W.4-L3-26 F', [[784.92, 1206.4], [793.56, 1206.4]], 0.96, 9.2396, 1, '5/8 type X WR', "L3 bath 310 side of the ELEC 321 segment | faces: bath 310 (2nd rated layer under the CBU)", s321)
if 'W.6-L4-03 C' not in idx:   # F2: ELEC 421 cara N (W.6-L4-03), ancho 1.31 ft, un tramo = una fila de 2 caras
    nueva('W.6-L4-03 A', 'W.6-L4-03 C', [[1036.44, 1140.0], [1060.08, 1140.0]], 1.31, 8.9375, 2, '5/8 type X',
          "L4 ELEC 421 north wall segment | faces: ELEC 421; corridor 412 (2nd layer each face, 2 HR)",
          "3/A7.50; A7.50 [DERIVED] length = ELEC 421 inside width (1060.08 - 1036.44)/18 = 1.31 ft (vectors, full review F2)")
for k in ('W.6-L4-08 C', 'W.6-L4-08 D'):   # F4 + ancho 1.31: el tramo sur en UNA fila de 2 caras
    if k in idx:
        w = idx.pop(k)
        (c['walls'] if w in c['walls'] else c['existing_walls']).remove(w)
if 'W.6-L4-08 C' not in idx:
    nueva('W.6-L4-08 A', 'W.6-L4-08 C', [[1036.44, 1307.85], [1060.08, 1307.85]], 1.31, 10.4375, 2, '5/8 type X',
          "L4 ELEC 421 south wall segment (inside W.6-L4-08) | faces: ELEC 421; corridor 412 (2nd layer each face, 2 HR)",
          "3/A7.50; A7.50 [DERIVED] length = ELEC 421 inside width (1060.08 - 1036.44)/18 = 1.31 ft (vectors; one segment, two faces = one row)")
# DA-6 con las filas reales
FIL = [('NULL-L3-08', 2), ('NULL-L3-09 A', 1), ('NULL-L3-09 B', 1), ('W.4-L4-18 A', 1), ('W.4-L4-18 B', 1), ('W.6-L4-09 A', 1), ('W.6-L4-09 B', 1),
       ('W.4-L2-15 E', 1), ('W.4-L2-15 F', 1), ('W.4-L3-26 E', 1), ('W.4-L3-26 F', 1), ('W.6-L4-03 C', 2), ('W.6-L4-08 C', 2)]
filas = [{"id": i, "faces": f, "layers": 1} for i, f in FIL]
tot = round(sum(idx[i]['length_ft'] * idx[i]['height_ft'] * f for i, f in FIL), 2)
for d in c['deduct_alternates']:
    if d['id'] == 'DA-6':
        old = d['delta_sf']; d['delta_sf'] = -tot; d['filas'] = filas
        d['operacion'] = " + ".join(f"{i} {idx[i]['length_ft']} x {idx[i]['height_ft']} x {f} face(s) x 1 layer(s)" for i, f in FIL) + f" = {tot} SF"
        d['texto'] = "ELEC 221 / 321 / 421 as drawn on their code plans 3/A0.01, 1/A0.02, 2/A0.02 (1HR FP: 1 layer each face); 221 W / N / E walls are W.62-1 (2 layers each face already)"
        LOG.append(f"DA-6 {old} -> {-tot}")
for w in c['walls'] + c['existing_walls']:
    s = str(w.get('source'))
    if 'DA6TOT' in s or re.search(r"DEDUCT ALTERNATE DA-6, delta -[\d.]+ SF", s):
        w['source'] = re.sub(r"DEDUCT ALTERNATE DA-6, delta -[\d.]+ SF", f"DEDUCT ALTERNATE DA-6, delta -{tot:.2f} SF", s).replace('DA6TOT', f"{tot:.2f}")
# F5: WS-1 de L4, un criterio para las 3 zonas: EXCLUDED (RS-1 sin rating; el RCP imprime WS-1)
c['misc_items'] = [m for m in c['misc_items'] if not m['ref'].startswith('CLG-L4-412WS ')]
TP = f'{W}/etapas/4_canon/rev14/rcp_cuartos.json'; T = json.load(open(TP))
Z = M['WS1_L4_A3.04']
ZON = [("(WS-1 N-S corridor 412, no number)", Z['412WS (ya cargada CLG-L4-412WS)']['polygon'], 34.52),
       ("(WS-1 lobby zone of corridor 412, no number)", Z['lobby 412']['hueco_RS1'], 72.29),
       ("(WS-1 E-W corridor 412, no number)", Z['corridor E-W']['polygon'], 39.89)]
rs = "WS-1 wood slat ceiling (other trade); RS-1 roof ceiling unrated, CEILING RE: RCP - no gypsum above at L4"
ya = {(r['sheet'], r['room']) for r in T['rooms']}
for room, P, A in ZON:
    if ('A3.04', room) not in ya:
        T['rooms'].append({"sheet": "A3.04", "room": room, "disposition": "exclusion", "rows": [], "nhoja": "1/A3.04; A0.08 RS-1; 6/A7.23",
                           "reason": rs, "reason_short": rs, "polygon": P, "area_sf": A,
                           "label_xy": [round(sum(q[0] for q in P) / 4, 1), round(sum(q[1] for q in P) / 4, 1)]})
json.dump(T, open(TP, 'w'), indent=1)
LOG.append("WS-1 L4: CLG-L4-412WS removed (-34.52 SF Type X, -25.89 LF RC); 3 zones EXCLUDED (146.70 SF)")
c['rev17_cambios'] = LOG
json.dump(c, open(CP, 'w'), indent=1)
print("\n".join(LOG)); print("DA6", tot)
