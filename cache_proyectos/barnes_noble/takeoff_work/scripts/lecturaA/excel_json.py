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
 ('RFI-01', 'Exterior types 1 / 1A / 1B / 1C: 5/8" gyp bd "BY FUTURE TENANT" (1, 1A, 1B, 1C/A-410). Framing included, gyp bd EXCLUDED (estimator decision). Confirm. ALSO A-002 Responsibility Schedule (Div 05): "PERIMETER STUDS, INSULATION, VAPOR BARRIER F/I BY LL" - the perimeter framing of types 1 / 1A / 1B / 1C may be by the landlord. Carried today: framing INCLUDED (estimator decision). Confirm who furnishes / installs the perimeter studs.', f'If gyp bd is in our scope: + {rfi01} SF 5/8" gyp bd (one face, {round(sum(w["length_ft"] for w in ext), 2)} LF x wall height) + finishing' + '; if perimeter studs are by LL: - 8,901 LF studs (1A 1,692 + 1 4,236 + 1B 2,333 + 1C 640, studs_out) with their bottom / top track, bracing and the 1B sheathing (2,469.22 SF)'),
 ('RFI-02', 'Type boundaries along a facade are not dimensioned: north 1A / 1 change and south 1B / 1 change (A-101).', 'North: 33.54 LF move from type 1 to 1A if the change is at the adjacent tenant edge (x=800.4 pt) instead of W2-03; south: 1.55 LF move 1 <-> 1B (door 10 jamb). Same 3-5/8" framing for 1 / 1A; 1B is 8" studs.'),
 ('RFI-03', 'B.O. deck is V.I.F. and sloped: 24\'-0" (2/A-400B) to 25\'-7" (2/A-400A); walls to deck loaded at 25\'-0" (1/A-400A, 1/A-400B), east facade 25\'-7", west 24\'-0".', f'Each 1 ft of deck height = {lf25} LF of studs-to-deck walls x 1 ft (studs, board where to deck, bracing rows)'),
 ('RFI-04', 'Type 2 height 25\'-0" exceeds the 22\'-0" limit of 3-5/8" 14 ga SJ @16" (A-410 metal stud schedule). Carried: 3-5/8" 14 ga SJ @16" + diagonal bracing @32" O.C. to structure above (8/A-410 Top Track Detail).', f'Diagonal braces: {braces} pcs (ROUNDUP(L x 12 / 32) + 1 per type 2 wall), brace member and length not printed - not priced. Alternative: 6" 20 ga SJ (26\'-8") on {lf(("2",))} LF'),
 ('RFI-05', 'Cafe south line: type 1 on A-101 and E1 / E2 (6" studs, void at existing wall) on 1/A-221. Counted ONCE as E1 / E2. E2 / E1 change point not drawn.', 'If both furring and 6" wall exist: + 50.24 LF type 1 furring (3-5/8") x 25\'-0". E2 / E1 split at the H2a faces: 0.20 LF moves.'),
 ('RFI-06', 'Cafe wall heights H1, H2a, H2b, H3a, H3b, F not printed (sections break at the top; A-225 finish plan and A-226A elevations give finish tops 11\'-0", 11\'-6", 15\'-0" only). Loaded to deck 25\'-0" (rule 53.3).', f'If studs stop at ~11\'-6": - {lf_cp} LF x 13.5 ft of studs / board on these walls'),
 ('RFI-07', 'Exterior furring 3-5/8" (types 1, 1A, 1C) at 24\'-0" to 25\'-7" exceeds 22\'-0" (14 ga SJ); 1B 8" studs are not in the A-410 schedule. Gauge / bracing to CMU not shown.', 'Alternative 6" studs on the 3-5/8" furring, or lateral bracing to the CMU at mid-height: price per LF of furring' + '; audit F-16: A-410 stud schedule caps 3-5/8" at 22\'-0" even at 14 ga - same applies to all 3-5/8" walls to 25 ft (types 1, 1A, 1C, 2): stop studs at nested bracing below deck or upsize'),
 ('RFI-08', 'Type I: 5/8" FRT plywood to top of WD-1 and GWB above (I/A-221): top of WD-1 not printed. GWB loaded full height.', 'Each 1 ft of WD-1 height moves 3.31 SF from GWB to FRT plywood'),
 ('RFI-09', 'Door headers: no header schedule in the set and 1/A-500 shows no header; headers carried 0 LF.', f'If a 2-piece track header is required at every door: + {hdr} LF ((R.O. + 1\'-4") x 2)'),
 ('RFI-10', 'Existing exterior doors 10, 12 (overhead), 13 are EXISTING V.I.F.: furring openings measured on the plan (3.49, 10.00, 6.33 ft); heads not printed.', 'Furring header / head track at these openings sized in the field; additional head track carried 19.0 LF (doors 12, 13)'),
 ('RFI-11', 'W.R. gyp bd in wet rooms (A-410 partition note 7 and 2/A-410 "restroom / cafe walls only") vs. the estimator rule (MR only behind toilet / lavatory, which here back onto the exterior EXT-07, gyp by tenant). Regular board carried.', f'If W.R. on every restroom / janitor face: {wet_sf} SF change from regular to W.R. board' + '; audit: Men\'s, Women\'s and Janitor faces about 1,326 SF + drinking fountain alcove + kitchenette wall (A-410 "*" note, note 7, 2/A-410, A-101 general note 8)'),
 ('RFI-12', 'Ceramic cove tile base (Cafe 103, Men\'s 108, Women\'s 109) and restroom wall tile (A-200, TL-2): cement board backer not detailed on the partitions.', 'If cement board is required behind the tile: + wall tile area of A-200 elevations (not dimensioned here)' + '; audit A-09: tile base 22/A-201 5/8" cement board 1\'-2" x Men\'s + Women\'s perimeter (2 x 32.33 LF) = about 76 SF'),
 ('RFI-13', 'FRP-1 (A-510: Cafe Work Room, Janitor, Cafe below counter): extent / height not printed for the partitions. Not quantified.', 'FRP-1 SF = Cafe Workroom walls (~81 LF) x 10\'-0" + Janitor walls x height - to be confirmed'),
 ('RFI-14', 'Cafe 11\'-0" framed soffit open faces (2/A-221): GWB vs WD-1 split not printed; GWB loaded full height to deck.', 'Each 1 ft of WD-1 on the open faces = 32.89 SF less GWB'),
 ('RFI-15', 'Suspended GWB ceilings: carrying channel direction not shown (E-W assumed); Cafe Seating cloud is drawn as USG drywall grid (4/A-121) but carried as the 5/A-121 hat channel system.', 'N-S direction changes carrying / furring LF; USG grid = main tees + cross tees instead of hat / CRC channels (same area 573.69 SF)'),
 ('RFI-16', 'Vestibule GWB ceiling box (4/A-210, 1/A-210): 8" joists @16", 8" box beam, posts, ledger, 3/4" plywood, 5/8" GWB 94.67 SF + 0.78 ft fascias - not priced by the package (no 8" joist family).', 'Pending: 94.67 SF GWB ceiling + fascia ~23 SF + 8" framing per 4/A-210' + '; audit A-04: vestibule GWB ceiling 10\'-6" (A-121 key note 5) about 8\'-5" x 12\'-8" = 107 SF suspended GWB (5/A-121), perimeter about 42 LF'),
 ('RFI-17', 'Column surrounds C25: stud spacing not printed (16" assumed); 9 columns counted on A-101 (reading B mentioned 10).', 'Each additional column: + 8 LF track x 2, 8 studs x 8 ft, 64 SF board, 32 LF corner bead'),
 ('RFI-18', 'Type 4 curved walls: printed 25\'-1" (taken) vs average of the two vector faces 25.68 ft.', '+1.20 LF type 4 if the face average is used'),
 ('RFI-19', 'Board height where a ceiling exists: 2/A-410 extends gyp to deck only where there is no ceiling (taken: ceiling + 6"); A-410 partition note 2 asks gyp on both sides for the full stud height.', f'Full height everywhere: + {full_sf} SF 5/8" gyp bd'),
 ('RFI-20', 'Grab & Go header soffit (3/A-221, 6\'-2" x ~7"): framing to deck and its faces not dimensioned - not priced.', '3.73 SF GWB soffit + two faces 6.17 LF x (deck - 7\'-1")' + '; audit A-05: Grab & Go GWB ceiling 7\'-1" (A-121) about 18 SF GWB + framing'),
 ('RFI-21', 'Cafe Seating GWB cloud edge: 6" fascia (4/A-121, measured on the detail, not dimensioned) and edge molding DGCM27.', '107.21 LF edge x 0.5 ft = 53.6 SF GWB + 107.21 LF edge trim'),
 ('RFI-22', 'Types 3 and 4: "F.R.P. over 5/8" plywood where shelving occurs" (3/A-410, 4/A-410) - fixture plan A-111 does not define the extent on the partial walls.', f'5/8" plywood + FRP on {lf(("3", "4"))} LF x height per face where shelving occurs'),
 ('RFI-23', 'FRT wood blocking / backing is called but not dimensioned: A-101 key notes C12 (12/A-412), C16 (8/A-413), C20 (6/A-412) "PROVIDE F.R.T. BLOCKING AS NEEDED"; 3/A-412 and 4/A-412 "F.R.T. BLOCKING IN WALL BEHIND GWB" (office); 13/A-412, 14/A-412 FRT wood blocking at cabinets / counter; 8A/A-413 "CONTINUOUS 2x4 F.R.T. WOOD BLOCKING (TYP.)" at receiving table; 7/A-413 and 7A/A-413 stock room shelving fastened to FRT wood blocking (C14, C27); P-201 water heater (EWH-2, unnumbered detail) 2x4 metal stud backing + steel backing plates. Rows / heights / extents not dimensioned - not quantified. Confirm extent or accept allowance.', 'Receiving table only: 17\'-3\" (8/A-413) x 3 rows read on 8A/A-413 = 51.75 LF 2x4 FRT [DERIVED, rows to verify]; office 3/A-412 + 4/A-412, breakroom 6/A-412, stock room shelving C14 / C27 (7/A-413) and water heater (P-201): + 1 row per shelf / counter line x elevation width - nothing carried today' + '. Audit counts (approx.): toilet rooms 3/4" FRT plywood behind 6 grab bars, 2 lavatories, 2 baby changing stations (21/A-201, 26/A-201, A-200) + 2 framed openings for recessed waste receptacles; 6 recessed FE cabinets C11 (4/A-101); stock room shelving C14 / C27 about 43 units = about 387 LF FRT (7/A-413); receiving table 17\'-3" x 4 rows = 69 LF (8A/A-413); Manager\'s Office about 86 LF (3, 4, 14/A-412); kitchenette about 10.7 LF (6/A-412); menu board about 57 SF FRT plywood (4/A-226A); janitor about 23 SF 3/4" plywood (11/A-200); cafe sign about 6 LF x 2 rows (1/A-226A); W-3 surface blocking 1/A-414, 7/A-414 by GC / fixture installer'),
 ('RFI-24', 'Gypsum board control joints: none labeled or detailed on A-410, A-121, A-221 or A-510 ("CJ" only in the M-100 legend). ASTM C840 limits uninterrupted wall runs to 30 ft; type 2 walls W2-01 (48.77 LF), W2-03 (94.24 LF), W2-04 (56.76 LF) exceed it. Not carried - confirm.', 'Type 2: floor(L / 30) = 1 + 3 + 1 = 5 joints x 25.0 ft x 2 faces = + 250.0 LF control joint; if RFI-01 brings exterior gyp bd into scope: EXT-02 5 x 25.0 + EXT-03 2 x 24.0 + EXT-07 1 x 25.0 = + 198.0 LF (one face)'),
 ('RFI-25', 'A-101 key note C5: "DEMISING PARTITION TO BE PATCHED AND REPAIRED TO MAINTAIN EXISTING FIRE RATING. PREPARE WALLS FOR NEW FINISH. ADD GWB/FURRING AS REQUIRED." Extent of patching and of added GWB / furring on the existing demising walls is not defined. Not carried - confirm scope and extent.', 'Allowance basis: demising wall LF x height x 1 face of 5/8" Type X gyp bd (+ furring if required) - LF of C5 walls to be confirmed on A-101; nothing carried today'),
 ('RFI-26', 'Type 1B sheathing product: 1B/A-410 calls 1/2" EXTERIOR GYP SHEATHING; A-001A Div 09 A.3 calls a glass mat gypsum substrate for exterior sheathing. Carried: 1/2" exterior gyp sheathing 2,469.22 SF gross (1B walls, wall height) - door 12 (EXISTING overhead, 10\'-0" wide, head not printed, RFI-10) not deducted.', 'Same SF (2,469.22) as glass mat sheathing instead of exterior gyp; - 10.0 ft x door 12 head height if the opening is deducted'),
 ('RFI-27', 'Board type: A-001A Div 09 A.2 and 4/A-121, 5/A-121 call 5/8" TYPE X gypsum board; A-410 partition types read "5/8" GYP BD". Carried as 5/8" regular.', '16,562.77 SF switch from 5/8" regular to 5/8" Type X (same SF, unit price change)'),
 ('RFI-28', 'Types 3 and 4 base anchorage: 3/A-410, 4/A-410 and A/A-410 draw a moment clip at the stud base with Hilti Kwik HUS-EZ anchors; spacing not printed separately. Not carried (expansion anchors 0).', 'If one clip per stud: + 162 moment clips (type 3 = 40 studs, type 4 = 122 studs, studs_out) + 324 Kwik HUS-EZ 1/4" x 1-5/8" (2 per clip)'),
 ('RFI-29', 'Corner guards: A-101 key note C22 "STAINLESS STEEL CORNER GUARDS AT 48" A.F.F. FOR ALL OUTSIDE GYPSUM BOARD CORNERS AT STOCKROOM WALLS" vs A-001A "METAL CORNER GUARDS (2"X2"X72") AT ALL OUTSIDE CORNERS". Extent and installer (drywall vs Div 10) not defined. Not carried.', 'C22: stock room outside corners only, about 4 to 6 corners x 4 ft; spec: every outside corner x 6 ft including 36 column surround corners (9 x 4)'),
 ('RFI-30', 'Access panels: M-100 general note 30 and E general note 12 "THE GENERAL CONTRACTOR SHALL INSTALL ACCESS PANELS"; A-002 F/I tenant contractor; quantity not shown on any sheet. Not carried.', 'Install only: allowance of 4 to 6 panels in the GWB ceilings (restrooms, Cafe bands / soffit, vestibule)'),
]
rfis = [{'id': a, 'pregunta': b, 'delta': d} for a, b, d in RF]

# ---- REV1 (DECISIONES_ESTIMADOR.md, 2026-10-24): RFIs cerrados / N/A con la decisión aplicada
import os
REV1 = os.environ.get('REV1') == '1'
if REV1:
    fam = fo['familias']
    D = 'CLOSED - estimator decision 2026-10-24 (rev1): '
    NA = 'N/A after RFI-01 (perimeter walls existing, rev1): '
    OV = {
     'RFI-01': (D + 'perimeter walls types 1 / 1A / 1B / 1C are EXISTING (1/DM-101 legend solid = to remain + key note 3 "EXTERIOR WALL PATCH AND REPAIR AS REQUIRED TO MAINTAIN EXISTING FIRE RATING"; A-101 Construction Legend "EXISTING EXTERIOR WALL" / "EXISTING PARTITION"; A-002 "PERIMETER STUDS, INSULATION, VAPOR BARRIER F/I BY LL"). Perimeter framing (studs, track, bracing, 1B sheathing) EXCLUDED. Interior face patch & repair (1/DM-101 key note 3, A-101 C5) = ALLOWANCE, amount: $ ________ (blank, estimator to fill).',
                'Applied: - 417.43 LF of perimeter walls (17 walls); 3-5/8" stud 16,812.96 -> 10,120.39 LF; 8" stud 2,332.99 -> 0; 1/2" exterior sheathing 2,469.22 -> 0 SF; bottom / top track 1,051.87 -> 634.44 LF each; bracing 5,230.74 -> 2,827.81 LF. Allowance: blank.'),
     'RFI-02': (NA + 'the north 1A / 1 boundary no longer affects the take-off (both types are existing, excluded).', 'none'),
     'RFI-07': (NA + 'exterior furring 3-5/8" over 22\'-0" (types 1, 1A, 1C) is existing, excluded.', 'none'),
     'RFI-10': (NA + 'doors 10, 12, 13 are existing doors in existing perimeter walls (A-500 EXISTING V.I.F.); no framing in our scope.', 'none'),
     'RFI-26': (NA + 'type 1B (and its 1/2" exterior gyp sheathing) is existing, excluded.', 'none'),
     'RFI-11': (D + 'W.R. gyp bd on ALL faces of Women\'s 109, Men\'s 108, Janitor 107 and the drinking fountain alcove corridor faces (W2-06.2 / .3 / .4) - A-410 "*" note "PROVIDE 5/8" WATER RESISTANT GYP. BD AT JANITOR\'S CLOSET, DRINKING FOUNTAIN, KITCHEN AND ALL TOILET LOCATIONS", A-410 partition note 7, 2/A-410, A-101 general note 8 (plan governs over skill rule D1). New walls only: EXT-07 faces and the break room kitchenette wall (south wall = EXT-07, 7/A-412) are existing -> patch & repair allowance.',
                f'Applied: 5/8" Type X W.R. = {fam.get(chr(53)+"/8\" gyp Type X W.R.", 0):,.2f} SF face by face (Women\'s 226.62 + Men\'s 223.02 + Janitor 485.75 + alcove corridor 88.63). Reconciles the rev0 figures: 935.4 SF (rev0 delta, restroom/janitor faces only) and ~1,326 SF (audit, included EXT-07 faces now existing).'),
     'RFI-23': (D + 'FRT blocking taken off with the counts and rows per detail: stock room shelving 7/A-413 (3 rows), receiving table 8A/A-413 (4 rows), Manager\'s Office 3, 4/A-412 (4 rows), break room cabinets 6/A-412 (2 rows); restroom backing 21, 26/A-201 (10 pcs 3/4" FRT plywood); Cafe menu boards 4/A-226A continuous 3/4" FRT plywood 31" high x C-E1-S.',
                f'Applied: FRT blocking {fam.get("FRT blocking", 0):,.2f} LF (387.0 + 69.0 + 85.6 + 10.67); 3/4" FRT plywood + 60.61 SF menu boards (23.46 x 31/12) + 13.33 SF restroom backing (10 pcs x 16" bay x 12" height ASSUMED - Review Item). Water heater backing (P-201) and W-3 surface blocking (1/A-414, by GC / fixture installer) not carried.'),
     'RFI-27': (D + 'all 5/8" gyp bd on NEW walls = Type X (A-001A Div 09 A.2); W.R. faces = 5/8" Type X W.R. GWB ceilings stay 5/8" regular (decision covers walls; 4/A-121, 5/A-121 call Type X - confirm ceilings).',
                f'Applied: 5/8" Type X {fam.get(chr(53)+"/8\" gyp board Type X", 0):,.2f} SF + Type X W.R. {fam.get(chr(53)+"/8\" gyp Type X W.R.", 0):,.2f} SF; regular remains {fam.get(chr(53)+"/8\" gyp board regular (walls + ceilings)", 0):,.2f} SF (GWB ceilings). If ceilings are Type X too: + that SF moves to Type X.'),
     'RFI-25': ('Merged into RFI-01 allowance (rev1): demising / perimeter wall patch & repair (A-101 C5, 1/DM-101 key note 3) = ALLOWANCE, amount blank.', 'Allowance: $ ________ (blank)'),
    }
    for r in rfis:
        if r['id'] in OV:
            r['pregunta'], r['delta'] = OV[r['id']]
    if os.environ.get('REV3') == '1':
        R3 = 'CLOSED - Review Item rev3 (estimator decision 2026-10-26): '
        OV3 = {
         'RFI-04': (R3 + 'type 2 > 22 ft: 3-5/8" 14 ga SJ + diagonal braces @ 32" O.C. to structure (8/A-410 "PROVIDE DIAGONAL BRACING AT 32" O.C. TO STRUCTURE (TYP.)"); brace member / length not printed - estimator choice 3-5/8" 20 ga stud x 4 ft at 45 deg.',
                    f'Applied: {braces} braces (115 in rev2 + 2 from W2-05 +5.00 LF) x 4.0 ft = {braces*4:.1f} LF 3-5/8" 20 ga stud (DERIVED, member and length = estimator choice; note kept). Citation corrected: diagonal bracing is on 8/A-410 Top Track Detail (rev0-rev2 said 3/A-410).'),
         'RFI-06': (R3 + 'Cafe walls H1, H2a, H2b, H3a, H3b, F studs TO DECK 25\'-0" (1/A-400B draws the Cafe walls floor to B.O. DECK; A-226A elevations break at the top; no section prints a stud top). Board per face = ceiling + 6" (A-410 partition note 3): Workroom ACT-1 10\'-0" -> 10\'-6"; Grab & Go GWB 7\'-1" -> 7\'-7"; Cafe open-to-deck strip at H2a (1/A-121 PT-6 OPEN TO DECK) -> to deck.',
                    'Applied (faces already at these heights in rev2; RCP evidence on 1/A-121).'),
         'RFI-08': (R3 + 'type I WD-1 top = 15\'-0" A.F.F. (6/A-226A; elevation bubble on 1/A-221 looks west at the type I face, verified).',
                    'Applied: 5/8" FRT plywood floor to 15\'-0" = 3.31 LF x 15.0 = 49.65 SF; GWB 15\'-0" to deck = 3.31 x 10.0 = 33.1 SF (2/A-221 studs UP TO DECK).'),
         'RFI-14': ('PARTLY CLOSED rev3: 2/A-221 "3 5/8" @ 16" O.C. METAL STUD UP TO DECK", 5/8" FRT plywood behind WD-1, 5/8" GWB above WD-1 and at soffit bottom, "T.O. WD-1 SEE ELEVATION". East face (6/A-226A, bubble verified): WD-1 11\'-0" to 15\'-0" -> FRT 4.0 ft; GWB 15\'-0" to deck. North face (1/A-226A, bubble verified): WD-1 9\'-0" to 11\'-0" -> FRT 2.0 ft. OPEN: (1) top of the "BN CAFE" sign panel WD-1 on the north face is not printed - carried as GWB; (2) soffit underside 9\'-0" (1/A-226A) vs 11\'-0" (A-121) - framing carried at 11\'-0".',
                    'Applied: FRT SS-E 10.12 x 4.0 = 40.48 SF, SS-N 22.77 x 2.0 = 45.54 SF; SS-E GWB 14 -> 10 ft. Open deltas: each 1 ft of sign-panel WD-1 = 22.77 SF GWB -> 5/8" FRT plywood; if soffit is at 9\'-0": + 2 ft of studs on SS-N (about 19 studs x 2 = 38 LF) and + 2 ft board.'),
         'RFI-15': (R3 + 'Cafe Seating cloud = USG drywall suspension grid as drawn on 4/A-121 (DGLW26 main tee, DGLW424 cross tee, DGCM27 channel molding, DGWM24 angle molding); carrying channel direction E-W confirmed (joists N-S: 1/A-400A joists cut in section, 2/A-400A joists in profile).',
                    'Applied: main tee 194.16 LF (5 x 38.833, @ 48" USG standard), cross tee 457.96 LF (31 x 14.773 = 124 pcs, @ 16" USG standard; 24" alt. = 22 rows / 88 pcs), DGCM27 107.21 LF, DGWM24 107.21 LF; removed from the cloud: furring -310.23 LF, carrying -194.17 LF, ceiling track -107.21 LF.'),
         'RFI-16': ('CLOSED rev3 except post sheathing: vestibule GWB ceiling box per 4/A-210, 6/A-210, 1/A-210 quantified (8" joists, nested box beam, 8" ledger, nested posts, 3/4" FRT plywood, 5/8" GWB). OPEN: 5/A-210 "5/8 GYP. BOARD SHEATHING AS REQUIRED" at the posts - extent not printed; 2 east corner posts may be existing storefront.',
                    'Applied: 8" joist 88.0 LF; 8" 18 ga stud 25.33 LF; ceiling / box track 43.0 LF (6" 25.33 + 8" ledger 12.67 + 3-5/8" 5.0); 3-5/8" stud 126.0 LF; 3/4" FRT plywood 106.6 SF; 5/8" Type X 105.5 SF. Open delta: post sheathing up to 6 posts x 3 faces x 5"/12 x 10.5 = 78.75 SF; if only 4 posts: - 42.0 LF 3-5/8" stud.'),
         'RFI-17': ('PARTLY CLOSED rev3: column surrounds C25 = 9 (CW-01..CW-09, A-101). OPEN: stud spacing not printed (16" assumed).', 'If 24" O.C.: fewer studs per surround (about - 1 stud per face).'),
         'RFI-18': (R3 + 'type 4 curved walls = face-average arc 25.68 LF each (estimator choice vs printed 25\'-1").', 'Applied: + 1.17 LF type 4 (83.64 LF).'),
         'RFI-19': (R3 + 'board height where a ceiling exists = ceiling + 6" (2/A-410, A-410 partition note 3). Kept.', 'none'),
        }
        for r in rfis:
            if r['id'] in OV3:
                r['pregunta'], r['delta'] = OV3[r['id']]
        _wr = fam.get(chr(53) + '/8" gyp Type X W.R.', 0); _tx = fam.get(chr(53) + '/8" gyp board Type X', 0)
        for r in rfis:
            if r['id'] == 'RFI-11':
                r['delta'] = f"Applied (rev3): 5/8\" Type X W.R. = {_wr:,.2f} SF face by face (Women's 222.93 + Men's 223.02 + Janitor 485.75 + alcove corridor 88.63); W2-05 Women's face = 7.51 LF per A-101 (rev3 RI 1)."
            if r['id'] == 'RFI-27':
                r['delta'] = f"Applied (rev3): 5/8\" Type X {_tx:,.2f} SF = walls {_tx - 981.38 - 105.5:,.2f} + GWB ceilings 981.38 + vestibule box 105.5; Type X W.R. {_wr:,.2f} SF; 5/8\" regular 0."
    if os.environ.get('REV2') == '1':
        R2 = 'rev2 (estimator decision 2026-10-25): '
        for r in rfis:
            if r['id'] == 'RFI-27':
                r['pregunta'] = D + 'all 5/8" gyp bd on new walls AND GWB ceilings = Type X (A-001A Div 09 A.2; 4/A-121, 5/A-121 - ' + R2 + 'ceilings to Type X); W.R. faces = 5/8" Type X W.R. No 5/8" regular remains.'
                r['delta'] = f'Applied: 5/8" Type X {fam.get(chr(53)+"/8\" gyp board Type X", 0):,.2f} SF (walls 14,557.36 + ceilings 981.38) + Type X W.R. {fam.get(chr(53)+"/8\" gyp Type X W.R.", 0):,.2f} SF; 5/8" regular 0.'
            if r['id'] == 'RFI-23':
                r['delta'] = r['delta'].replace('13.33 SF restroom backing (10 pcs x 16" bay x 12" height ASSUMED - Review Item)', '17.78 SF restroom backing (10 pcs x 16" bay x 16" high, ' + R2 + '13.33 x 16/12)')
            if r['id'] == 'RFI-01':
                r['pregunta'] += ' ' + R2 + 'break room kitchenette W.R. on existing EXT-07 (6/A-412, 7/A-412) is INSIDE this patch & repair allowance; allowance amount stays BLANK (decided).'
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
if REV1:
    REV = [x for x in REV if x[1] not in ('1', '1A', '1B') and 'RFI-19' not in x[3] or (x[0] == 'detalle')]
    REV = [x for x in REV if not (x[0] == 'floor_plan' and x[1] in ('1', '1A', '1B'))]
    os.environ.get('REV2') == '1' or REV.append(('detalle', None, 8, 'Restroom FRT plywood backing: 10 pcs at 16" stud bay, height NOT printed - 12" assumed (13.33 SF); confirm grab bar / lavatory / baby changing backing size (RFI-23)', '21/A-201'))
if os.environ.get('REV3') == '1':
    REV = []   # rev3: all 11 Review Items closed (DECISIONES_ESTIMADOR.md)
n = len(REV)
revisar = []
for i, (fa, t, o, p, h) in enumerate(REV, 1):
    x = {'n': i, 'total': n, 'fase': fa, 'punto': p, 'hoja_detalle': h, 'imagen': 'see FINAL_FOR_REVIEW images'}
    if fa == 'floor_plan': x['type'] = t
    else: x['orden_plano'] = o
    revisar.append(x)
d = json.load(open(K + '/takeoff.json'))
if os.environ.get('REV4') == '1':   # rev4: RFIs abiertos respondidos por el estimador
    R4 = 'CLOSED - estimator answer (rev4): '
    OV4 = {'RFI-14': (R4 + 'Cafe soffit bottom = 11\'-0" (A-121 RCP governs over 1/A-226A 9\'-0"); north face sign band WD-1 top = 15\'-0" (same as east face, 6/A-226A). Both faces: WD-1 11\'-0" to 15\'-0" with 5/8" FRT plywood behind; GWB above to deck and at the soffit bottom (2/A-221).',
                      'Applied: SS-N FRT 22.77 x 4.0 = 91.08 SF (rev3 45.54 at 9\'-0"/11\'-0"); SS-N GWB 14 -> 10 ft; SS-E unchanged (FRT 40.48 SF, GWB 10 ft).'),
           'RFI-16': (R4 + 'vestibule post sheathing = 3/4" FRT plywood, 4 faces, full height (5/A-210 "5/8 GYP. BOARD SHEATHING AS REQUIRED" -> estimator: plywood).',
                      'Applied: 6 posts x 4 faces x 5" x 10.5 ft = 105.0 SF 3/4" FRT plywood (6 posts per 1/A-210).'),
           'RFI-17': (R4 + 'column surrounds C25 stud spacing = 16" O.C. (as carried); count 9.', 'none (as carried)')}
    for r in rfis:
        if r['id'] in OV4:
            r['pregunta'], r['delta'] = OV4[r['id']]
if os.environ.get('REV3') == '1':   # rev3: textos finales con las cifras vigentes (después de REV2)
    _fam = fo['familias']; _wr = _fam.get(chr(53) + '/8" gyp Type X W.R.', 0); _tx = _fam.get(chr(53) + '/8" gyp board Type X', 0)
    for r in rfis:
        if r['id'] == 'RFI-27':
            r['delta'] = f"Applied (rev3): 5/8\" Type X {_tx:,.2f} SF = walls {_tx - 981.38 - 105.5:,.2f} + GWB ceilings 981.38 + vestibule box 105.5; Type X W.R. {_wr:,.2f} SF; 5/8\" regular 0."

REV5 = os.environ.get('REV5') == '1'
if REV5:   # rev5: auditoría final rev4 (AUDITORIA_rev4/CERTIFICADO_AUDITORIA.md, COMPARATIVA_AUDITORIA.xlsx; regla v80j)
    _fam = fo['familias']; _wr = _fam.get(chr(53) + '/8" gyp Type X W.R.', 0); _tx = _fam.get(chr(53) + '/8" gyp board Type X', 0)
    CL = c['ceilings']
    _cx = round(sum(x['area_sf'] for x in CL if x.get('board') == '5/8 type X' and x.get('system') != 'canopy_joist'), 2)
    _cwr = round(sum(x['area_sf'] for x in CL if x.get('board') == '5/8 type X WR'), 2)
    _misc_tx = round(sum(m['qty'] for m in c.get('misc_items') or [] if m['familia'] == chr(53) + '/8" gyp board Type X'), 2)
    def _flf(room):
        return round(sum((f.get('length_ft') or w['length_ft']) for w in W for f in w.get('faces') or [] if f['room'] == room), 2)
    _wk = round(sum((f.get('length_ft') or w['length_ft']) * f['height_ft'] for w in W for f in w.get('faces') or [] if f['room'] == 'Cafe Workroom 104'), 2)
    _fs = {m['ref']: m['qty'] for m in c.get('misc_items') or [] if m['ref'].startswith('FIRESTOP')}
    _fst = round(sum(_fs.values()), 2)
    _aht = _fam.get('additional head track', 0)
    A5 = 'audit rev4 row {} (rev5): '
    OV5 = {
     'RFI-11': None,
     'RFI-12': (None, None),
     'RFI-13': ('FRP-1 (A-510 Room Finish Schedule: Cafe Work Room 104 FRP-1 all walls, Janitor 107 FRP, Cafe 103 below countertop): installer (A-002) and height not printed for the partitions. Not quantified - ' + A5.format(10) + 'kept open.',
                f'FRP-1 SF = Cafe Work Room 104 faces {_flf("Cafe Workroom 104")} LF x FRP height + Janitor 107 faces {_flf("Janitor Closet 107")} LF x FRP height (A-510); + PVC trim at FRP edges and inside corners'),
     'RFI-20': ('CLOSED - ' + A5.format(6) + 'Grab & Go header soffit QUANTIFIED from the plan: 6\'-2" HOLD (1/A-221) x (B.O. deck 25\'-0" - Grab & Go GWB 7\'-1", 1/A-121) with 6" metal studs @ 16" O.C. (3/A-221); 5/8" FRT plywood substrate on the east face, GWB at the soffit bottom. T.O. WD-1 not printed -> RFI-34.',
                'Applied: SS-GG 6" studs 6 x 17.917 = 107.5 LF; ceiling / soffit track 6.167 x 2 = 12.33 LF; bracing 4 rows x 6.167 = 24.67 LF (5/A-410); 5/8" FRT plywood 6.167 x 17.917 = 110.49 SF; bottom GWB 3.73 SF.'),
     'RFI-23': None,
    }
    for r in rfis:
        if r['id'] == 'RFI-11':
            r['pregunta'] = r['pregunta'] + ' rev5 (' + A5.format('3 / 9').rstrip(': ') + '): + restroom GWB ceilings (A-410 Partition Notes 2 "W.R. ... FOR WALL AND CEILING CONSTRUCTION") and Cafe Work Room 104 GWB faces (A-410 "*" note KITCHEN, 2/A-410 RESTROOM/CAFE WALLS).'
            r['delta'] = (f"Applied (rev5): 5/8\" Type X W.R. = {_wr:,.2f} SF = walls (Women's 222.93 + Men's 223.02 + Janitor 485.75 + alcove corridor 88.63 "
                          f"+ Cafe Work Room 104 {_wk:,.2f}) + restroom ceilings {_cwr:,.2f} (Women's 61.19 + Men's 61.11, 1/A-121). "
                          f"Auditor figures: ceilings 120.2 SF (chase notch deducted; take-off keeps the RCP area, +2.10 SF), Work Room up to 570 SF.")
        if r['id'] == 'RFI-12':
            r['pregunta'] += ' rev5 (' + A5.format(10).rstrip(': ') + '): A-510 also lists ceramic / porcelain WALL TILE at Corridor 110 - backer not detailed.'
            r['delta'] += f'; Corridor 110 wall tile: {_flf("Corridor 110")} LF of corridor faces x tile height (not printed) of 1/2" cement board instead of 5/8" Type X (each 1 ft of tile height = {_flf("Corridor 110")} SF)'
        if r['id'] in ('RFI-13', 'RFI-20'):
            r['pregunta'], r['delta'] = OV5[r['id']]
        if r['id'] == 'RFI-23':
            r['delta'] = r['delta'].replace(' Water heater backing (P-201) and W-3 surface blocking (1/A-414, by GC / fixture installer) not carried.',
                                            ' rev5: water heater backing (P-201) carried conservatively -> RFI-32; janitor 3/4" FRT plywood area (11/A-200) carried 17.0 SF -> RFI-33; W-3 surface blocking (1/A-414, 7/A-414) -> RFI-36.')
        if r['id'] == 'RFI-08':
            r['delta'] = 'Applied (rev3 + rev5): type I 5/8" FRT plywood floor to 15\'-0" (6/A-226A) = (C-I 2.31 + C-I-P.1 1.00 + end faces C-I-E1 / C-I-E2 1.21) 4.52 LF x 15.0 = 67.74 SF; GWB 15\'-0" to deck 4.52 x 10.0 = 45.16 SF.'
        if r['id'] == 'RFI-27':
            r['delta'] = (f"Applied (rev5): 5/8\" Type X {_tx:,.2f} SF = walls {_tx - _cx - _misc_tx:,.2f} + GWB ceilings {_cx:,.2f} (restroom ceilings moved to W.R., RFI-11) "
                          f"+ vestibule box 105.5 + Grab & Go soffit bottom 3.73; Type X W.R. {_wr:,.2f} SF; 5/8\" regular 0.")
    rfis += [
     {'id': 'RFI-31', 'pregunta': 'Additional head track at openings: the note "ADD FULL LENGTH ADDL HEAD TRACK @ OPNG > 4\'-0"" quoted in rev0-rev4 is NOT on A-410 / A-500 (skill default criterion; citation corrected, ' + A5.format(8).rstrip(': ') + '). Carried conservatively at the two 4\'-0" doors: door 3 (C-H2a, 4\'-0" x 8\'-0") and door 11 (W2-03, 4\'-0" x 7\'-0"), A-500 door schedule.',
      'delta': f'Carried {_aht:.2f} LF = 2 x (R.O. 4.00 ft measured jamb gap + 2 x 8" bearing); if not required: - {_aht:.2f} LF. Auditor 11.17 LF assumed R.O. 4\'-3" (frame not printed): + 0.50 LF if the R.O. is 4\'-3".'},
     {'id': 'RFI-32', 'pregunta': 'P-201 WATER HEATER DETAIL ("FOR RESTROOMS AND BREAKROOM"): 2x4 metal stud backing + steel blocking between studs at the anchor locations; member sizes and lengths not printed (Janitor 107, 11/A-200). ' + A5.format(5).rstrip(': ') + ': carried conservatively.',
      'delta': 'Carried: 3-5/8" stud backing 2 x 4.0 ft = 8.0 LF + steel blocking 2 rows x 1.33 ft = 2.67 LF (3-5/8" stud pieces); if by the plumber: - 10.67 LF 3-5/8" stud.'},
     {'id': 'RFI-33', 'pregunta': '11/A-200 Janitor 107: "AREA OF 3/4" FIRE RESISTANT PLYWOOD BLOCKING (TYP)" - extent not dimensioned. ' + A5.format(4).rstrip(': ') + ': carried at the conservative upper bound (width measured on 11/A-200 x 8\'-0" HOLD).',
      'delta': 'Carried 2.125 x 8.0 = 17.0 SF 3/4" FRT plywood; confirm extent (delta down to 0 SF).'},
     {'id': 'RFI-34', 'pregunta': 'Grab & Go header soffit (3/A-221): "T.O. WD-1 SEE ELEVATION" - top of WD-1 on the soffit east face not printed on A-226A / A-226B. Carried conservatively: 5/8" FRT plywood on the full east face (no GWB above WD-1).',
      'delta': '3/A-221 draws the 5/8" FRT plywood substrate full height and 5/8" GWB over it above T.O. WD-1: each 1 ft of face above T.O. WD-1 adds 6.17 SF of 5/8" Type X GWB (plywood 110.49 SF stays; GWB above WD-1 not carried until T.O. WD-1 is known).'},
     {'id': 'RFI-35', 'pregunta': '8/A-410 "METAL STUD/TRACK FIRE STOP AT CEILING LINE, TYP.": applied to every full-height wall with a ceiling on at least one face (1/A-121). ' + A5.format(7).rstrip(': ') + ': carried; confirm with the GC that it is required at all of them.',
      'delta': f'Carried {_fst:.2f} LF track (3-5/8" {_fs.get("FIRESTOP-TRACK-3", 0):.2f} + 6" {_fs.get("FIRESTOP-TRACK-6", 0):.2f}); if not required: - {_fst:.2f} LF.'},
     {'id': 'RFI-36', 'pregunta': 'Surface-mounted 3/4" FRT plywood blocking at the W-3 wall fixtures "BY GC/FIXTURE INSTALLER" (1/A-414, 7/A-414): who furnishes / installs is ambiguous and the W-3 count on A-111 is not taken. Not carried - ' + A5.format(11).rstrip(': ') + '.',
      'delta': 'If by the drywall contractor: + one 3/4" FRT plywood strip per W-3 unit (size per 1/A-414, 7/A-414) x W-3 count from A-111 - PENDING count.'},
    ]

if os.environ.get('REV6') == '1':   # rev6: investigación W.R. / FRT (investigacion_WR_FRT/NOTA_WR_FRT.md)
    _fam = fo['familias']; _wr = _fam.get(chr(53) + '/8" gyp Type X W.R.', 0)
    for r in rfis:
        if r['id'] == 'RFI-11':
            r['pregunta'] = ('CLOSED - estimator decision RFI-11 (rev1) + plan check rev6: W.R. gypsum board on all faces of Women\'s 109, Men\'s 108, Janitor 107 and the drinking fountain alcove (A-410 Partition Notes 2 "PROVIDE WATER RESISTANT GYPSUM BOARD IN ALL BATHROOMS AND JANITOR\'S CLOSET FOR WALL AND CEILING CONSTRUCTION", note 7, "*" note, 2/A-410, 5/A-410; A-001A Div 09 A.4) and on the restroom GWB ceilings (same note 2; 1/A-121 GWB 9\'-0"). '
                             'Cafe Work Room 104: NO W.R. - G/A-221 draws only 5/8" FRT plywood on the Work Room side (FRP-1 finish, A-510); there is no gypsum board on that face (rev6 removes the 570.36 SF GWB faces).')
            r['delta'] = (f"Applied (rev6): 5/8\" Type X W.R. = {_wr:,.2f} SF = walls (Women's 222.93 + Men's 223.02 + Janitor 485.75 + alcove corridor 88.63) "
                          f"+ restroom ceilings 122.30 (Women's 61.19 + Men's 61.11, 1/A-121).")
    _wkl = round(sum(x['lf'] for x in c.get('plywood_strips') or [] if x.get('room') == 'Cafe Workroom 104'), 2)
    for r in rfis:
        if r['id'] == 'RFI-13':
            r['delta'] = f'FRP-1 SF = Cafe Work Room 104 walls {_wkl} LF (FRT plywood faces C-H1-N, C-H1-W, C-H2a, C-H2b x 2, C-E2; G/A-221, E/A-221) x FRP height + Janitor 107 faces {_flf("Janitor Closet 107")} LF x FRP height (A-510); + PVC trim at FRP edges and inside corners'
        for k in ('pregunta', 'delta'):
            r[k] = r[k].replace('Applied (rev5)', 'Applied (rev6)')
    rfis.append({'id': 'RFI-37', 'pregunta': 'CLOSED - resolved from the plan (rev6): the Sales / Cafe faces of C-H1-N and C-H2a are 5/8" gypsum board only. G/A-221 draws one layer on the Sales Floor side ("5/8" GYPSUM BOARD"); C-H1-N Sales face = Sales Area 101 PAINTED GYP. BD. (A-510); C-H2a Cafe face = PT-3 painted wall around door 3 (1/A-225 finish plan, 5/A-226A Cafe Service Line Elevation); the narrow WD-1 left of the door is the type I return C-I-P.1 (already carried). Evidence: investigacion_WR_FRT/ images 12-14.',
                 'delta': 'Applied: - 951.75 SF 5/8" FRT plywood (C-H1-N A 25.90 x 25.0 = 647.50 + C-H2a B 12.17 x 25.0 = 304.25), carried since rev0; GWB on those faces unchanged.'})

REV7 = os.environ.get('REV7') == '1'
if REV7:   # rev7: Paso 12 sobre rev6 (PASO12_rev6/CERTIFICADO_PASO12.md, MATRIZ_COBERTURA.xlsx; regla v80j)
    _fam = fo['familias']
    MI = {m['ref']: m for m in c.get('misc_items') or []}
    _cmq = round(sum(m['qty'] for k, m in MI.items() if k.startswith('CROSS-MEMBERS')), 2)
    P7 = 'Plan check (rev7): '
    OV7 = {
     'RFI-34': ('CLOSED - ' + P7 + 'T.O. WD-1 at the Grab & Go header = 15\'-0" (5/A-226A 11\'-0" + 4\'-0" WD-1; 6/A-226A 15\'-0"). 3/A-221: 5/8" FRT plywood full face, 5/8" GWB over it above T.O. WD-1.',
                'Applied: + 6.167 x 10.0 = 61.67 SF 5/8" Type X (15\'-0" to deck); FRT plywood unchanged (110.49 SF).'),
     'RFI-12': ('CLOSED (base) / OPEN (installer of tile) - ' + P7 + '22/A-201 Tile Base Detail prints "5/8" CEMENT BOARD" with "1\'-2" CEMENT BOARD BASE" and 5/8" W.R. GYP. BD. above (A-001A Div 09 J.2). Corridor 110 wall tile (A-510) backer: not detailed.',
                f"Applied: + {MI['RESTROOM-BASE-CEMENT']['qty']} SF cement board base on the restroom faces of new walls and the same SF out of W.R. Open: Corridor 110 wall tile backer - each 1 ft of tile height = {_flf('Corridor 110')} SF cement board instead of Type X."),
     'RFI-13': ('FRP-1 (A-510): Cafe Work Room 104 FRP-1 full height to the 10\'-0" ceiling (1-4/A-226B); Janitor 107 FRP-1 to 96" A.F.F. (A-131) / 8\'-0" (9-12/A-200). Who furnishes / installs the FRP is not defined (A-002). Substrate: E/A-221 and G/A-221 call 5/8" FRT plywood on the Work Room faces; 3/A-225 draws a dotted (board) fill - conflict. Not carried - ' + P7 + 'heights corrected.',
                'If FRP is in our scope: Cafe Work Room 87.52 LF x 10.0 = 875.20 SF + Janitor 19.43 LF x 8.0 = 155.44 SF = 1,030.64 SF FRP-1 gross (doors not deducted) + PVC trim (J-mold, inside corners).'),
     'RFI-35': ('3/A-410 Top Track Detail "METAL STUD/TRACK FIRE STOP AT CEILING LINE, TYP." (citation corrected from 8/A-410 - ' + P7 + 'C-07): applied to every full-height wall with a ceiling on at least one face (1/A-121); carried; confirm with the GC.',
                f"Carried per wall (Material Summary breakdown) = {round(sum(m['qty'] for k, m in MI.items() if k.startswith('FIRESTOP-')), 2)} LF; if not required: minus that LF."),
    }
    OV7['RFI-04'] = ('CLOSED - Review Item rev3 (estimator decision 2026-10-26): type 2 > 22 ft: 3-5/8" 14 ga SJ + diagonal braces @ 32" O.C. to structure (3/A-410 Top Track Detail "PROVIDE DIAGONAL BRACING AT 32" O.C. TO STRUCTURE ABOVE (TYP.)"); brace member / length not printed - estimator choice 3-5/8" 20 ga stud x 4 ft at 45 deg. ' + P7 + 'same precedent applied to the Cafe 3-5/8" walls to deck (C-H2a, C-H2b, C-F): 14 ga SJ + 11 diagonal braces = 44.0 LF.',
                     f'Applied: {braces} braces x 4.0 ft = {braces*4:.1f} LF (type 2) + 44.0 LF (Cafe) 3-5/8" 20 ga stud (member and length = estimator choice). Citation history: rev0-rev2 cited the partition type 3 section, rev3-rev6 cited 8/A-410 (that bubble is the Typ. Connection Detail); the Top Track Detail is bubble 3/A-410 (rev7 plan check C-07).')
    OV7['RFI-35'] = ('3/A-410 Top Track Detail "METAL STUD/TRACK FIRE STOP AT CEILING LINE, TYP." (rev5-rev6 cited 8/A-410, which is the Typ. Connection Detail - rev7 plan check C-07): applied to every full-height wall with a ceiling on at least one face (1/A-121); carried; confirm with the GC.', OV7['RFI-35'][1])
    _cbx = MI['RESTROOM-BASE-CEMENT']['qty']
    _wr7 = _fam.get(chr(53) + '/8" gyp Type X W.R.', 0); _tx7 = _fam.get(chr(53) + '/8" gyp board Type X', 0)
    _cl7 = [x for x in c['ceilings'] if x.get('board') == '5/8 type X' and x.get('system') != 'canopy_joist']
    _mtx = [(k, m['qty']) for k, m in MI.items() if m['familia'] == chr(53) + '/8" gyp board Type X']
    OV7['RFI-11'] = (None, f"Applied (rev7): 5/8\" Type X W.R. = {_wr7:,.2f} SF = walls (Women's 222.93 + Men's 223.02 + Janitor 485.75 + alcove corridor 88.63) + restroom ceilings 122.30 - 1'-2\" cement board base {_cbx} (22/A-201).")
    OV7['RFI-27'] = (None, f"Applied (rev7): 5/8\" Type X {_tx7:,.2f} SF = walls {_tx7 - sum(x['area_sf'] for x in _cl7) - sum(v for _, v in _mtx):,.2f} + GWB ceilings {sum(x['area_sf'] for x in _cl7):,.2f} (" + ', '.join(f"{x['room']} {x['area_sf']}" for x in _cl7) + ') + ' + ' + '.join(f'{k} {v}' for k, v in _mtx) + f"; Type X W.R. {_wr7:,.2f} SF; 5/8\" regular 0.")
    OV7['RFI-01'] = (None, None)
    for r in rfis:
        if r['id'] in OV7:
            a_, b_ = OV7[r['id']]
            r['pregunta'] = a_ if a_ is not None else r['pregunta']
            r['delta'] = b_ if b_ is not None else r['delta']
        if r['id'] == 'RFI-03':
            r['pregunta'] += ' ' + P7 + 'the elevations also print 21\'-9" V.I.F. at the right end of 2/A-400A and 23\'-8" V.I.F. on A-400B (joists sloping): the B.O. deck range is wider than 24\'-0" to 25\'-7".'
        if r['id'] == 'RFI-01':
            r['pregunta'] += ' ' + P7 + 'A-410 types 1, 1A, 1B, 1C label the interior board "5/8" GYP BD BY FUTURE TENANT": EXCLUDED with that citation, consistent with this decision. A-413 7/8A general note "IF SHELVING IS TO BE INSTALLED ON EXISTING WALL, G.C. IS TO REMOVE AND REPLACE GYP. BOARD AS REQUIRED FOR INSTALLATION OF WOOD BLOCKING": inside this patch & repair allowance.'
        if r['id'] == 'RFI-ACC-stud-reinforcement-mep' or 'stud reinforcement' in r['pregunta'].lower():
            r['pregunta'] = r['pregunta'].replace('6/A-410 and 7/A-410 penetration details', '6/A-410 and 7/A-410 (pipe firestopping only)')
        if r['id'] not in OV7:
            for k in ('pregunta', 'delta'):
                r[k] = r[k].replace('8/A-410 Top Track Detail', '3/A-410 Top Track Detail').replace('(8/A-410', '(3/A-410').replace(' 8/A-410', ' 3/A-410')
        if r['id'] == 'RFI-01':
            r['delta'] += '; board by future tenant on the existing perimeter (A-410 types 1 / 1A / 1B / 1C): upper bound 417.43 LF x 25.0 = 10,436 SF 5/8" Type X if it were ever in our scope.'
        if r['id'] == 'RFI-23':
            r['delta'] = r['delta'].replace('(387.0 + 69.0 + 85.6 + 10.67)', '(387.0 + 69.0 + 85.6 + 10.67 + FE cabinets 16.0, rev7)')
    NEW7 = [
     ('RFI-38', 'Ceiling seismic bracing: A-121 Ceiling Notes 1 "SEE A-420 DRAWINGS REGARDING CEILING BRACING" - A-420 is not in the set; 5/A-121 draws splay wires and a 16 ga wire @ 12\'-0" O.C. each way at each brace point (the 1-5/8" x 16 ga metal joist framing @ 48" is the horizontal carrying member); A-002 Div 10 "SEISMIC BRACING" F/I by the tenant contractor. Carried conservatively on the GWB suspended ceilings.',
      f"Carried: splay wires {MI['SPLAY-WIRES-5-A121']['qty']} LF (hanger wire row) + 1-5/8\" posts {MI.get('SEISMIC-STRUTS-5-A121', MI.get('SEISMIC-VERTICAL-WIRE-5-A121'))['qty']} LF; if not required (seismic category / A-420): minus both."),
     ('RFI-39', 'Recessed fire extinguisher cabinets (A-101 C11, A-111 KN 9, 4/A-101 "F.R.T. WOOD STUD HEADER ABOVE AND BASE BELOW CABINET"): 4 in new walls (W2-01, W2-03 x 2, Cafe Workroom); cabinet width / rough opening not printed (Cosmopolitan fully recessed, Ambassador 1017F10).',
      'Carried 16.0 LF FRT 2x (4 x (2.0 + 2.0 ft)); each +1 ft of cabinet width = +8.0 LF FRT; jamb studs inside the field studs.'),
     ('RFI-40', '3/A-410 Top Track Detail: "METAL RUNNER AT STUDS - SECURE GWB TO METAL RUNNER" with "DO NOT SECURE METAL STUDS OR GWB TO DEEP LEG TRACK" read as a nested inner runner at every deflection head. Carried; confirm.',
      f"Carried {MI['NESTED-RUNNER-3-A410']['qty']} LF nested inner runner; if a single deep leg track is accepted: minus that LF."),
     ('RFI-41', '8/A-410 Typ. Connection Detail (PARALLEL TO STRUCTURE): full-height walls parallel to the joists (N-S) hang from metal studs spanning joist to joist; joist spacing not printed (A-400A / A-400B).',
      f"Carried {_cmq} LF (members @ 24\" O.C. along the wall x 5.0 ft assumed joist spacing); each 1 ft of joist spacing = {round(_cmq / 5.0, 2)} LF."),
     ('RFI-42', '2/A-221 framed soffit drop "CROSS BRACING AS REQ\'D": member / spacing not printed.',
      f"Carried {MI['SOFFIT-CROSS-BRACING-2-A221']['qty']} LF 3-5/8\" stud (pairs @ 4\'-0\" x 5.0 ft); if not required: minus that LF."),
     ('RFI-43', 'E/A-221 type E1 (Cafe south wall C-E1-S, C-E1-P.2, C-E1-B): 1/2" cement board height not printed; carried to deck 25\'-0" (studs to deck). The Cafe 9\'-0" GWB band runs along C-E1-S (1/A-121).',
      'If the cement board stops at 9\'-0" + 6" (A-410 Partition Notes 3): C-E1-S 19.0 x 15.5 = - 294.5 SF, C-E1-P.2 2.11 x 15.5 = - 32.7 SF, C-E1-B 2.31 x 15.5 = - 35.8 SF.'),
     ('RFI-44', 'H/A-221 "H3a = PLYWOOD TO TOP OF WD-1": T.O. WD-1 on the H3a Sales face not printed (A-225, A-226A). Carried: FRT plywood to deck (25\'-0"), no GWB.',
      'If T.O. WD-1 = 15\'-0" as on the Grab & Go header (6/A-226A): FRT plywood - 40.8 SF (4.08 x 10.0) and 5/8" Type X + 40.8 SF.'),
     ('RFI-45', '1/A-221 Workroom door pier (1\'-0" x 2\'-8" HOLD) against H2a with an internal void: the C-H2a Cafe face may be concealed along the pier.',
      'If concealed: - 2.67 x 25.0 = - 66.7 SF 5/8" Type X on C-H2a (pier faces carried as C-E1-P.2 / C-I-P.1).'),
     ('RFI-46', 'F/A-221 "3 5/8" METAL STUDS @ 16" O.C. TO BOTTOM OF NESTED STUD BRACING": the nested stud bracing member is not drawn; studs carried to deck (estimator decision RI 7).',
      f"Carried {MI['F-NESTED-BRACING']['qty']} LF 3-5/8\" (2 nested members); define member / elevation."),
     ('RFI-47', 'Plywood material / thickness conflicts on A-225: 5/A-225 die wall "3/4" THICK MARINE GRADE PLYWOOD" vs A/A-221, B/A-221 "3/4" FRT PLYWOOD SUBSTRATE" and A-410 "ALL PLYWOOD NEEDS TO BE FRT"; 10/A-225 "1/2" F.R.T. PLYWOOD SUBSTRATE" vs I/A-221, G/A-221, H/A-221 5/8" FRT plywood. Carried as FRT, thickness per the A-221 sections.',
      'Same SF; material / thickness change only: die wall 63.47 SF marine vs FRT; type I end faces 18.08 SF 1/2" instead of 5/8".'),
     ('RFI-48', 'Stock room shelving blocking: 7/A-413 "FRT WOOD BLOCKING IN PARTITION" vs 7A/A-413 "SURFACE MOUNT WOOD BLOCKING" (no FRT). Carried in-partition FRT 2x, 3 rows (387 LF).',
      'Quantity unchanged; if surface-mounted: material / installation method change only (not FRT, no board cut-outs).'),
     ('RFI-49', '2/A-500 Cased Opening Detail: "WOOD BLOCKING" across the stud return; the number / location of cased openings is not marked on A-101.',
      'Carried 1 opening x 17.0 LF wood blocking (not labeled FRT); each additional opening + 17.0 LF.'),
     ('RFI-50', '2/E-103 Server Room: "4\'x8\' FRT PLYWOOD SHEET AND POWER BY GC - ALL OTHER WORK BY OTHERS" (E-301 "fire-rated plywood terminal board"). Carried in the drywall scope (FRT plywood substrate); confirm the trade.',
      'Carried 32.0 SF 3/4" FRT plywood; if by the electrical contractor: - 32.0 SF.'),
     ('RFI-52', 'Vestibule GWB bands above B.O. ceiling 10\'-6": top of the band 11\'-3 1/2" V.I.F. (2/A-210, 3/A-210, "VESTIBULE ASSEMBLY TO MATCH EXISTING STOREFRONT SYSTEM V.I.F.").',
      'Carried 14.96 SF; each 1" of band height = 1.89 SF (front 12.67 + sides 2 x 8.42 ft / 12).'),
     ('RFI-53', 'Light fixtures in the Cafe GWB bands (11\'-6" and 9\'-0", 1/A-121): fixture count in the bands not taken; 5/A-121 "PROVIDE ADDITIONAL WIRE SUPPORT AT ALL LIGHT FIXTURES".',
      'Each fixture in a band = + 1 hanger x 13.5 / 16.0 ft wire.'),
     ('RFI-51', 'Fastener counts not printed: 7/A-210 3"x3"x16 ga clip angles (count per header end); cement board screw spacing (manufacturer standard 8" O.C. used); plywood screws per A-410 note 8.D (24" field / 12" perimeter on 4x8 sheets).',
      f"Carried: clip angles 7/A-210 4 pcs; cement board screws {MI['CEMENT-BOARD-SCREWS']['qty']} pcs; plywood screws {MI['PLYWOOD-SCREWS-8D']['qty']} pcs - adjust to the estimator yields. Framing screws count the stud pieces of the walls and column wraps (781); the detail members (braces, cross members, bracing) add about + 724 screws. 9/A-410 calls #8 screws stud to track while note 8.A calls #10-16 on 18/16 ga - carried per 8.A."),
    ]
    rfis += [{'id': a, 'pregunta': b, 'delta': dd} for a, b, dd in NEW7]
import re as _re
_RX_INT = _re.compile(r'\s*\(?(?:evidence|Evidence)?:?\s*\b[\w-]*_[\w-]*/(?:[\w./-]*)?\)?')
def _limpia(t):
    return _re.sub(r'\s{2,}', ' ', _RX_INT.sub('', t)).replace(' ;', ';').replace(' .', '.') if isinstance(t, str) else t
for r in rfis:
    r['pregunta'], r['delta'] = _limpia(r['pregunta']), _limpia(r['delta'])
REV8 = os.environ.get('REV8') == '1'
if REV8:   # rev8: Paso 12 2.ª pasada (PASO12_rev7/)
    _fam = fo['familias']; MI = {m['ref']: m for m in c.get('misc_items') or []}
    P8 = 'Plan check (rev8): '
    for r in rfis:
        if r['id'] == 'RFI-38':
            r['delta'] = f"Carried: splay wires {MI['SPLAY-WIRES-5-A121']['qty']} LF (hanger wire row) + vertical 16 ga wire at each brace point {MI['SEISMIC-VERTICAL-WIRE-5-A121']['qty']} LF (16 ga wire row); the 1-5/8\" x 16 ga metal joist framing @ 48\" on 5/A-121 is the horizontal carrying member (no post) - {P8}C7-01. If not required: minus both."
        if r['id'] == 'RFI-46':
            r['pregunta'] += ' ' + P8 + 'the same phrase is printed on the partition types 3 and 4 (3/A-410, 4/A-410): nested stud at the top of each wall.'
            r['delta'] = f"Carried {MI['F-NESTED-BRACING']['qty']} LF (F) + {MI['NESTED-BRACING-T3-T4']['qty']} LF (types 3 / 4) 3-5/8\" stud; define member / elevation; if not required: minus both."
        if r['id'] == 'RFI-53':
            r['pregunta'] += ' ' + P8 + 'E-301 Sec. 265119: "THIS CONTRACTOR SHALL PROVIDE AND INSTALL ALL NECESSARY SUPPORT MEDIA FOR ALL LIGHTING FIXTURES ... FIXTURES SHALL NOT BE SUPPORTED FROM ROOF DECK" - overlap with the 5/A-121 fixture wires carried.'
            r['delta'] += f" If the fixture supports are by the electrical contractor (E-301 265119): - {MI['HANGERS-FIXTURES-5-A121']['qty']} LF hanger wire (29 hangers)."
        if r['id'] == 'RFI-51':
            r['delta'] += (f" {P8}relief channel to structure carried with 8/A-410 #8 pan head screws ({MI['PAN-HEAD-8-A410']['qty']} pcs) + P.A.F. at cross members ({MI['PAF-CROSS-MEMBERS-8-A410']['qty']} pcs); "
                           "note 8.C X-EDNI (2 rows @ 16\" = 720 pcs) is the alternative if the track bears directly on structural steel. Slab pins carried per note 8.F (2 rows @ 16\" X-DNI); 9/A-410 alternative 0.177\" PAF @ 24\" = - 640.61 pcs.")
        if r['id'] == 'RFI-23':
            r['delta'] = r['delta'].replace(f'{_fam.get("FRT blocking", 0):,.2f} LF', f'{_fam.get("FRT blocking", 0) - (fo.get("wood_blocking_lf") or 0):,.2f} LF FRT + 2X wood {fo.get("wood_blocking_lf") or 0:,.2f} LF (2/A-500)')
if os.environ.get('REV7') == '1':
    d['inputs_notas'] = {'joint_compound_lb_per_sf': 'YIELD: 72 lb per 1,000 SF; Level 4 finish printed on A-001A Div 09 A.8 "PROVIDE AT A MINIMUM A LEVEL 4 FINISH".'}
    if os.environ.get('REV8') == '1':
        d['inputs_notas'].update({
            'slab_pin_spacing_ft': 'YIELD: A-410 note 8.F X-DNI 2 rows at 16" O.C. = 0.667 ft per pin (9/A-410 PAF @ 24" = alternative, RFI).',
            'drywall_screws_per_sf': 'YIELD: estimator 1.2 / SF; products per A-410 note 8.E (Type S 25/20 ga, Type S-12 18/16/14 ga) and A-001A Div 09 A.5.'})
d.update({'rfis': rfis, 'revisar': revisar})
alc_p = K + '/etapas/alcances_estado.json'
try:
    d['alcances'] = json.load(open(alc_p))
except FileNotFoundError:
    pass
if REV5 and d.get('alcances'):
    _fr = fo.get('frt_plywood_by_material') or {}
    N5 = {
     'ALC-06': f"Bracing C.R. channel @ 4'-0\" O.C. per A-410 partition note 4 and 5/A-410 = {_fam.get('bracing C.R. channel', 0):,.2f} LF; diagonal bracing type 2 > 22'-0\" per 8/A-410 Top Track Detail (RFI-04 CLOSED rev3: 117 braces = 468.0 LF)",
     'ALC-07': f"Quantified (rev5): 5/8\" Type X {_tx:,.2f} SF + 5/8\" Type X W.R. {_wr:,.2f} SF (A-410, A-001A, RFI-27, RFI-11); no 5/8\" regular. Perimeter walls existing (RFI-01).",
     'ALC-08': (f"Quantified (rev6): 5/8\" Type X W.R. {_wr:,.2f} SF = all faces of Women's 109, Men's 108, Janitor 107 and drinking fountain alcove corridor faces (A-410 Partition Notes 2 and 7, '*' note, 2/A-410, 5/A-410) + restroom GWB ceilings {_cwr:,.2f} SF (A-410 Partition Notes 2); Cafe Work Room 104 = FRT plywood + FRP-1, no gypsum (G/A-221, A-510); existing EXT-07 faces = patch allowance." if os.environ.get('REV6') == '1' else f"Quantified (rev5): 5/8\" Type X W.R. {_wr:,.2f} SF = all faces of Women's 109, Men's 108, Janitor 107, drinking fountain alcove corridor faces and Cafe Work Room 104 faces (A-410 '*' note, note 7, 2/A-410) + restroom GWB ceilings {_cwr:,.2f} SF (A-410 Partition Notes 2); existing EXT-07 faces = patch allowance."),
     'ALC-10': f"FRT plywood 5/8\" {_fr.get('FRT plywood substrate (5/8 in.)', 0):,.2f} SF (Cafe types G, H, E2, F, I and Grab & Go soffit 3/A-221; soffit faces 2/A-221) + 3/4\" {_fr.get('FRT plywood substrate (3/4 in.)', 0):,.2f} SF (counters A/B, menu boards 4/A-226A, restroom backing 21/A-201, vestibule 4/A-210, 5/A-210, janitor 11/A-200) - breakdown in Material Summary",
     'ALC-11': f"Quantified (rev5): suspended GWB ceilings and soffits per A-121 (5/A-121, 4/A-121) and 2/A-221 = 981.38 SF: 5/8\" Type X {_cx:,.2f} SF + restroom ceilings 5/8\" Type X W.R. {_cwr:,.2f} SF (A-410 Partition Notes 2).",
     'ALC-12': "Furring channel @ 24\", carrying channel @ 48\", hanger wire 103 pcs, ceiling track per 5/A-121 on A-121; carrying direction E-W (RFI-15 CLOSED rev3: joists N-S on 1/A-400A, 2/A-400A); Cafe Seating cloud = USG drywall suspension grid 4/A-121; M-100 (p46), M-101 (p47), M-102 (p48) hangers are MEP",
     'ALC-13': "Quantified: framed soffit 2/A-221 (SS-N, SS-E, SS-IN-N, SS-IN-E) and Grab & Go header soffit 3/A-221 (SS-GG, RFI-20 CLOSED rev5; T.O. WD-1 RFI-34); E-102 (p36) bulkhead is signage (by others)",
     'ALC-15': "Column wraps C25 x 9 on A-101, studs @ 16\" O.C. (RFI-17 CLOSED rev4), carried under OTHER FRAMING",
     'ALC-16': f"Quantified (rev1, RFI-23): FRT blocking {_fam.get('FRT blocking', 0):,.2f} LF (7/A-413 387.0, 8A/A-413 69.0, 3-4/A-412 85.6, 6/A-412 10.67) + 3/4\" FRT plywood menu boards 60.61 SF (4/A-226A) + restroom backing 17.78 SF (21/A-201) + janitor 17.0 SF (11/A-200, RFI-33); water heater backing P-201 10.67 LF 3-5/8\" stud (RFI-32); W-3 surface blocking 1/A-414 RFI-36.",
     'ALC-04': f"Bottom track and top / deflection track = partition LF per type (A-101, A-221; 2/A-410, 3/A-410); + fire stop track at ceiling line {_fst:.2f} LF (8/A-410, RFI-35) and additional head track {_aht:.2f} LF (RFI-31); M-302 (p51) mention is plumbing expansion fittings",
     'ALC-20': "Cement board at wet walls (A-510 tile finishes, RFI-12 incl. Corridor 110 wall tile); FRP-1 extent RFI-13 / RFI-22 not carried",
    }
    if os.environ.get('REV7') == '1':
        N5['ALC-24'] = 'QUANTIFIED: Level 4 finish printed - A-001A Div 09 A.8 "PROVIDE AT A MINIMUM A LEVEL 4 FINISH" (joint compound / tape yields per Inputs); no Level 5 (A-510).'
        N5['ALC-02'] = 'NOT APPLICABLE (rev1, estimator decision RFI-01): perimeter walls types 1 / 1A / 1B / 1C are existing; their interior board is labeled "5/8" GYP BD BY FUTURE TENANT" on 1, 1A, 1B, 1C/A-410 - EXCLUDED with that citation.'
        N5['ALC-06'] = N5['ALC-06'].replace('8/A-410', '3/A-410') + ' + 2" x 2" 16 ga clip angles at every stud per bracing row (5/A-410) and 2/A-221 soffit cross bracing (RFI-42).'
        N5['ALC-04'] = N5['ALC-04'].replace('8/A-410', '3/A-410') + '; nested inner runner at deflection heads (3/A-410, RFI-40); X-EDNI fasteners 8.C; cross members at walls parallel to joists (8/A-410 Typ. Connection, RFI-41).'
        N5['ALC-17'] = 'RFI: access panels RFI-30; recessed FE cabinets framed per 4/A-101 (FRT header + base, RFI-39); no framed MEP opening drawn in GWB walls (A-121, M-102, P-101A).'
        N5['ALC-12'] = N5['ALC-12'] + '; Grab & Go GWB ceiling 7\'-1" added; additional hangers at light fixtures and seismic splay wires per 5/A-121 (RFI-38); 16 ga tie wire (5/A-121) = consumable of the furring / carrying install, no separate row.'
        N5['ALC-18'] = 'Metal trim (corner bead, J-bead) per A-410, A-121, A-510 Finish Notes 8 (incl. soffit bottom edges 65.31 LF); no control joint printed (RFI-24).'
        _c7 = [x for x in c['ceilings'] if x.get('system') != 'canopy_joist']
        N5['ALC-11'] = f"Quantified (rev7): suspended GWB ceilings and soffits per A-121 (5/A-121, 4/A-121) and 2/A-221 = {sum(x['area_sf'] for x in _c7):,.2f} SF (incl. Grab & Go 7'-1\" 25.16 SF): 5/8\" Type X + restroom ceilings 5/8\" Type X W.R. (A-410 Partition Notes 2)."
        N5['ALC-12'] = N5['ALC-12'].replace('hanger wire 103 pcs', f"hanger wire {(fo.get('hanger_pcs') or {}).get('total_pcs')} pcs at 48\" + 29 at light fixtures")
        if os.environ.get('REV8') == '1':
            N5['ALC-16'] = N5['ALC-16'].replace(f"FRT blocking {_fam.get('FRT blocking', 0):,.2f} LF", f"FRT blocking {_fam.get('FRT blocking', 0) - (fo.get('wood_blocking_lf') or 0):,.2f} LF")
        N5['ALC-16'] = N5['ALC-16'].replace('(7/A-413 387.0, 8A/A-413 69.0, 3-4/A-412 85.6, 6/A-412 10.67)', '(7/A-413 387.0, 8A/A-413 69.0, 3-4/A-412 85.6, 6/A-412 10.67, 4/A-101 FE cabinets 16.0) + 2X wood 17.0 LF (2/A-500)')
        for x in d['alcances']:
            if x['id'] in ('ALC-24', 'ALC-17'):
                x['estado'] = 'CUANTIFICADO' if x['id'] == 'ALC-24' else x['estado']
        d['alcances'] += [
         {'id': 'ALC-X40', 'nombre': 'Acoustical lay-in ceilings ACT-1 / ACT-3 (tile + Prelude XL grid + wires)', 'estado': 'NO APLICA',
          'nota': 'EXCLUDED: Div 09 51 acoustical ceilings by the ACT contractor - A-002 lists "ACOUSTICAL CEILING SYSTEM" as its own line (F/I tenant contractor); ACT-1 Cafe Workroom 10\'-0", ACT-3 Corridor, Break Room, Manager\'s Office 9\'-0" (1/A-121, A-510 finish legend); ACT portion of 5/A-121. Wall board heights use these ceilings + 6".'},
         {'id': 'ALC-X41', 'nombre': 'Unistrut space frame / strut channel', 'estado': 'NO APLICA',
          'nota': 'EXCLUDED: A-001A Div 05 D "UNISTRUT SPACE FRAME GRID SYSTEM ... AS REQUIRED FOR LIGHTING, CEILING ACCESSORIES OR MECHANICAL SYSTEMS SUSPENSION" and A-002 cafe signage "STRUT CHANNEL" = lighting / sign / MEP supports by those trades; the sign blocking is carried (4/A-226A menu boards).'},
         {'id': 'ALC-X42', 'nombre': 'Caulk at the base of wet-area walls', 'estado': 'NO APLICA',
          'nota': 'EXCLUDED: A-101 general note 8 "BOTTOM OF THE WALL CAULKED AT FLOOR LEVEL" = joint sealant (Div 07), excluded like all sealants (estimator standing order).'},
         {'id': 'ALC-X43', 'nombre': 'Partition seismic bracing (A-002 Div 10)', 'estado': 'NO APLICA',
          'nota': 'EXCLUDED as a separate item: A-002 Div 10 "SEISMIC BRACING" is listed with the specialties; partition lateral bracing is carried per 5/A-410 and 3/A-410; ceiling bracing per 5/A-121 carried under RFI-38.'},
         {'id': 'ALC-X44', 'nombre': 'Remove & replace existing GWB for shelving blocking (7/A-413)', 'estado': 'RFI',
          'nota': 'Inside the RFI-01 patch & repair allowance (existing perimeter walls): A-413 general note "G.C. IS TO REMOVE AND REPLACE GYP. BOARD AS REQUIRED FOR INSTALLATION OF WOOD BLOCKING".'},
        ]
    for x in d['alcances']:
        if x['id'] in N5:
            x['nota'] = N5[x['id']]
            if os.environ.get('REV6') == '1':
                x['nota'] = x['nota'].replace('(rev5)', '(rev6)')

json.dump(d, open(K + '/takeoff.json', 'w'), indent=1, ensure_ascii=False)
print(len(rfis), 'rfis', braces, 'braces', rfi01, lf25, lf_cp, hdr, wet_sf, full_sf)
