"""takeoff.json para plantilla_excel.py: RFIs (deltas del canon), Review Items, Scope Checklist, orden de types."""
import json, math
K = '/home/user/Reading-Plans/cache_proyectos/barnes_noble/takeoff_work'
E = K + '/etapas'
c = json.load(open(E + '/4_canon/takeoff_canon.json'))
fo = json.load(open(E + '/4_canon/out/familias_out.json'))
W = c['walls']
def lf(tags): return round(sum(w['length_ft'] for w in W if w.get('tag') in tags and w.get('element') == 'wall'), 2)
ext = [w for w in W if w.get('tag') in ('1', '1A', '1B', '1C')]
rfi01 = round(sum(w['length_ft'] * w['height_ft'] for w in ext), 1)
t25 = [w for w in W if w.get('element') == 'wall' and abs(w['height_ft'] - 25.0) < 0.01]
lf25 = round(sum(w['length_ft'] for w in t25), 2)
cafe_p = [w for w in W if w.get('tag') in ('H1', 'H2a', 'H2b', 'H3a', 'H3b', 'F')]
lf_cp = round(sum(w['length_ft'] for w in cafe_p), 2)
doors = [o for w in W for o in w.get('openings') or []]
hdr = round(sum((o['ro_w_ft'] + 16 / 12) * 2 for o in doors), 2)
wet = [(w, f) for w in W for f in w.get('faces') or [] if f.get('wet_room_note')]
wet_sf = round(sum((f.get('length_ft') or w['length_ft']) * f['height_ft'] for w, f in wet), 1)
full = [(w, f) for w in W for f in w.get('faces') or [] if f['height_ft'] < w['height_ft'] - 0.01 and w.get('element') == 'wall']
full_sf = round(sum((f.get('length_ft') or w['length_ft']) * (w['height_ft'] - f['height_ft']) for w, f in full), 1)
t2 = {}
for w in W:
    if w.get('tag') == '2':
        t2[w['id'].split('.')[0]] = t2.get(w['id'].split('.')[0], 0) + w['length_ft']
braces = sum(math.ceil(L * 12 / 32 - 1e-9) + 1 for L in t2.values())
t4arc = [w for w in W if w.get('tag') == '4' and w['id'][3:5] in ('29', '30')]
RF = [
 ('RFI-01', 'Exterior types 1 / 1A / 1B / 1C: 5/8" gyp bd "BY FUTURE TENANT" (1, 1A, 1B, 1C/A-410). Framing included, gyp bd EXCLUDED (estimator decision). Confirm.', f'If gyp bd is in our scope: + {rfi01} SF 5/8" gyp bd (one face, {round(sum(w["length_ft"] for w in ext), 2)} LF x wall height) + finishing'),
 ('RFI-02', 'Type boundaries along a facade are not dimensioned: north 1A / 1 change and south 1B / 1 change (A-101).', 'North: 33.54 LF move from type 1 to 1A if the change is at the adjacent tenant edge (x=800.4 pt) instead of W2-03; south: 1.55 LF move 1 <-> 1B (door 10 jamb). Same 3-5/8" framing for 1 / 1A; 1B is 8" studs.'),
 ('RFI-03', 'B.O. deck is V.I.F. and sloped: 24\'-0" (2/A-400B) to 25\'-7" (2/A-400A); walls to deck loaded at 25\'-0" (1/A-400A, 1/A-400B), east facade 25\'-7", west 24\'-0".', f'Each 1 ft of deck height = {lf25} LF of studs-to-deck walls x 1 ft (studs, board where to deck, bracing rows)'),
 ('RFI-04', 'Type 2 height 25\'-0" exceeds the 22\'-0" limit of 3-5/8" 14 ga SJ @16" (A-410 metal stud schedule). Carried: 3-5/8" 14 ga SJ @16" + diagonal bracing @32" O.C. to structure above (3/A-410 Top Track Detail).', f'Diagonal braces: {braces} pcs (ROUNDUP(L x 12 / 32) + 1 per type 2 wall), brace member and length not printed - not priced. Alternative: 6" 20 ga SJ (26\'-8") on {lf(("2",))} LF'),
 ('RFI-05', 'Cafe south line: type 1 on A-101 and E1 / E2 (6" studs, void at existing wall) on 1/A-221. Counted ONCE as E1 / E2. E2 / E1 change point not drawn.', 'If both furring and 6" wall exist: + 50.24 LF type 1 furring (3-5/8") x 25\'-0". E2 / E1 split at the H2a faces: 0.20 LF moves.'),
 ('RFI-06', 'Cafe wall heights H1, H2a, H2b, H3a, H3b, F not printed (sections break at the top; A-225 finish plan and A-226A elevations give finish tops 11\'-0", 11\'-6", 15\'-0" only). Loaded to deck 25\'-0" (rule 53.3).', f'If studs stop at ~11\'-6": - {lf_cp} LF x 13.5 ft of studs / board on these walls'),
 ('RFI-07', 'Exterior furring 3-5/8" (types 1, 1A, 1C) at 24\'-0" to 25\'-7" exceeds 22\'-0" (14 ga SJ); 1B 8" studs are not in the A-410 schedule. Gauge / bracing to CMU not shown.', 'Alternative 6" studs on the 3-5/8" furring, or lateral bracing to the CMU at mid-height: price per LF of furring'),
 ('RFI-08', 'Type I: 5/8" FRT plywood to top of WD-1 and GWB above (I/A-221): top of WD-1 not printed. GWB loaded full height.', 'Each 1 ft of WD-1 height moves 3.31 SF from GWB to FRT plywood'),
 ('RFI-09', 'Door headers: no header schedule in the set and 1/A-500 shows no header; headers carried 0 LF.', f'If a 2-piece track header is required at every door: + {hdr} LF ((R.O. + 1\'-4") x 2)'),
 ('RFI-10', 'Existing exterior doors 10, 12 (overhead), 13 are EXISTING V.I.F.: furring openings measured on the plan (3.49, 10.00, 6.33 ft); heads not printed.', 'Furring header / head track at these openings sized in the field; additional head track carried 19.0 LF (doors 12, 13)'),
 ('RFI-11', 'W.R. gyp bd in wet rooms (A-410 partition note 7 and 2/A-410 "restroom / cafe walls only") vs. the estimator rule (MR only behind toilet / lavatory, which here back onto the exterior EXT-07, gyp by tenant). Regular board carried.', f'If W.R. on every restroom / janitor face: {wet_sf} SF change from regular to W.R. board'),
 ('RFI-12', 'Ceramic cove tile base (Cafe 103, Men\'s 108, Women\'s 109) and restroom wall tile (A-200, TL-2): cement board backer not detailed on the partitions.', 'If cement board is required behind the tile: + wall tile area of A-200 elevations (not dimensioned here)'),
 ('RFI-13', 'FRP-1 (A-510: Cafe Work Room, Janitor, Cafe below counter): extent / height not printed for the partitions. Not quantified.', 'FRP-1 SF = Cafe Workroom walls (~81 LF) x 10\'-0" + Janitor walls x height - to be confirmed'),
 ('RFI-14', 'Cafe 11\'-0" framed soffit open faces (2/A-221): GWB vs WD-1 split not printed; GWB loaded full height to deck.', 'Each 1 ft of WD-1 on the open faces = 32.89 SF less GWB'),
 ('RFI-15', 'Suspended GWB ceilings: carrying channel direction not shown (E-W assumed); Cafe Seating cloud is drawn as USG drywall grid (4/A-121) but carried as the 5/A-121 hat channel system.', 'N-S direction changes carrying / furring LF; USG grid = main tees + cross tees instead of hat / CRC channels (same area 573.69 SF)'),
 ('RFI-16', 'Vestibule GWB ceiling box (4/A-210, 1/A-210): 8" joists @16", 8" box beam, posts, ledger, 3/4" plywood, 5/8" GWB 94.67 SF + 0.78 ft fascias - not priced by the package (no 8" joist family).', 'Pending: 94.67 SF GWB ceiling + fascia ~23 SF + 8" framing per 4/A-210'),
 ('RFI-17', 'Column surrounds C25: stud spacing not printed (16" assumed); 9 columns counted on A-101 (reading B mentioned 10).', 'Each additional column: + 8 LF track x 2, 8 studs x 8 ft, 64 SF board, 32 LF corner bead'),
 ('RFI-18', 'Type 4 curved walls: printed 25\'-1" (taken) vs average of the two vector faces 25.68 ft.', '+1.20 LF type 4 if the face average is used'),
 ('RFI-19', 'Board height where a ceiling exists: 2/A-410 extends gyp to deck only where there is no ceiling (taken: ceiling + 6"); A-410 partition note 2 asks gyp on both sides for the full stud height.', f'Full height everywhere: + {full_sf} SF 5/8" gyp bd'),
 ('RFI-20', 'Grab & Go header soffit (3/A-221, 6\'-2" x ~7"): framing to deck and its faces not dimensioned - not priced.', '3.73 SF GWB soffit + two faces 6.17 LF x (deck - 7\'-1")'),
 ('RFI-21', 'Cafe Seating GWB cloud edge: 6" fascia (4/A-121, measured on the detail, not dimensioned) and edge molding DGCM27.', '107.21 LF edge x 0.5 ft = 53.6 SF GWB + 107.21 LF edge trim'),
 ('RFI-22', 'Types 3 and 4: "F.R.P. over 5/8" plywood where shelving occurs" (3/A-410, 4/A-410) - fixture plan A-111 does not define the extent on the partial walls.', f'5/8" plywood + FRP on {lf(("3", "4"))} LF x height per face where shelving occurs'),
]
rfis = [{'id': a, 'pregunta': b, 'delta': d} for a, b, d in RF]
REV = [
 ('floor_plan', '1', None, 'South facade 1B / 1 boundary and Cafe overlap (RFI-02, RFI-05)', 'A-101'),
 ('floor_plan', '1A', None, 'North facade 1A / 1 boundary: W2-03 vs adjacent tenant edge, 33.54 LF (RFI-02)', 'A-101'),
 ('floor_plan', '1B', None, 'Storefront openings left out of the exterior LF (R70.7); reading B measured through them (+65.55 LF)', 'A-101'),
 ('floor_plan', '2', None, 'Corridor wall W2-05 starts at the restroom front (7.92 LF, reading B) - image res_W205.png', 'A-101'),
 ('floor_plan', '4', None, 'Center feature caps = open U + curved walls 25\'-1" (RFI-18)', '4/A-410'),
 ('floor_plan', 'C25', None, 'Column surrounds: 9 counted (B said 10) (RFI-17)', 'A-101'),
 ('floor_plan', 'I', None, 'Workroom door pier: 1\'-0" return = type I (tag PT0050), E1 pier 2.11 LF', '1/A-221'),
 ('detalle', None, 1, 'Board height ceiling + 6" vs full height (RFI-19)', '2/A-410'),
 ('detalle', None, 2, 'Type 2 > 22 ft: 14 ga SJ + diagonal bracing @32" (RFI-04)', '3/A-410'),
 ('detalle', None, 3, 'Cafe heights not printed, loaded to deck (RFI-06)', 'G/A-221'),
 ('detalle', None, 4, 'Type I WD-1 top (RFI-08)', 'I/A-221'),
 ('detalle', None, 5, 'Cafe framed soffit faces (RFI-14)', '2/A-221'),
 ('detalle', None, 6, 'Ceiling system / carrying direction / cloud grid (RFI-15)', '5/A-121'),
 ('detalle', None, 7, 'Vestibule ceiling box not priced (RFI-16)', '4/A-210'),
]
n = len(REV)
revisar = []
for i, (fa, t, o, p, h) in enumerate(REV, 1):
    x = {'n': i, 'total': n, 'fase': fa, 'punto': p, 'hoja_detalle': h, 'imagen': 'see FINAL_FOR_REVIEW images'}
    if fa == 'floor_plan': x['type'] = t
    else: x['orden_plano'] = o
    revisar.append(x)
d = json.load(open(K + '/takeoff.json'))
d.update({'rfis': rfis, 'revisar': revisar})
alc_p = K + '/etapas/alcances_estado.json'
try:
    d['alcances'] = json.load(open(alc_p))
except FileNotFoundError:
    pass
json.dump(d, open(K + '/takeoff.json', 'w'), indent=1, ensure_ascii=False)
print(len(rfis), 'rfis', braces, 'braces', rfi01, lf25, lf_cp, hdr, wet_sf, full_sf)
