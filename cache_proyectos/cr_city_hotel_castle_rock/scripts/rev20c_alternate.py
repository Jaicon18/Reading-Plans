"""rev20c (decisión del usuario 13-nov vía COORDINACIÓN sobre RFI-30, texto literal: "ponlo como alternate"):
el forro de la escalera 127 (LIN-127-L1..L4-N/S/E/W) SALE del base bid y va como ALTERNATE #1 (ADD), completo como lo
dibuja la geometría: 2-1/2" metal stud furring @ 16" o.c. + track + 5/8" Type X, más compound, tape y trims.
- Base: los 16 renglones pasan a excluded_walls con su motivo (7-10/A6.01, 11/A6.01; INTERIOR DRAWINGS referenced, not issued).
- Alternate: canon.add_alternates['ALTERNATE #1'] con cada material [DERIVED] (operación escrita) y su compra con el desperdicio
  de los Inputs (metal 15 %, board 6 %; yields sin desperdicio: compound 0.072 LB/SF, tape 0.37 LF/SF, Inputs 23 / 24).
Idempotente (si ya corrió, no hace nada)."""
import json
import math

CP = '/root/cr/work/etapas/4_canon/takeoff_canon.json'
C = json.load(open(CP))
EW = C['existing_walls']
LIN = [w for w in EW if str(w['id']).startswith('LIN-127-')]
if LIN:
    MOT = ("ALTERNATE #1 (ADD) - user decision 13-nov on RFI-30 ('ponlo como alternate'): NOT in the base bid. 7-10/A6.01 and 11/A6.01 draw "
           "an untagged 3 3/8\" lining on the stair side of the CMU (all 4 sides, L1-L4); no type / material printed - INTERIOR DRAWINGS "
           "referenced (11/A6.01 'RE: INTERIOR DRAWINGS'), not issued in the bid set. Priced apart as ALTERNATE #1 (Proposal; Scope Checklist)")
    C['existing_walls'] = [w for w in EW if not str(w['id']).startswith('LIN-127-')]
    C.setdefault('excluded_walls', [])
    ya = {x.get('id') for x in C['excluded_walls']}
    for w in LIN:
        if w['id'] not in ya:
            C['excluded_walls'].append({'id': w['id'], 'reason': MOT, 'floor': w.get('floor'), 'sheet': w.get('sheet'), 'page': w.get('page'),
                                        'path': w.get('path'), 'length_ft': w.get('length_ft'), 'height_ft': w.get('height_ft'),
                                        'img': w.get('img'), 'alternate': 'ALTERNATE #1'})
    C['alternate_1_rows'] = LIN          # geometría completa de los 16 renglones (traza del alternate)
    rows, b_sf, s_lf, t_lf, n_st = [], 0.0, 0.0, 0.0, 0
    for w in LIN:
        L_, H_ = float(w['length_ft']), float(w['height_ft'])
        n = math.ceil(L_ * 12 / 16) + 1                     # studs @ 16" o.c. + 1 (A0.06 GN 6 'ALL METAL STUDS TO BE SPACED @ 16" O.C.')
        rows.append(f"{w['id']} {L_} x {H_}: board {L_ * H_:.2f} SF, studs ceil({L_} x 12 / 16) + 1 = {n} x {H_} = {n * H_:.2f} LF, track 2 x {L_} = {2 * L_:.2f} LF")
        b_sf += L_ * H_; s_lf += n * H_; t_lf += 2 * L_; n_st += n
    b_sf, s_lf, t_lf = round(b_sf, 2), round(s_lf, 2), round(t_lf, 2)
    mud, tape = round(b_sf * 0.072, 2), round(b_sf * 0.37, 2)
    ITEMS = [
        {"material": '2-1/2" metal stud 20 GA (33 mil), furring @ 16" o.c.', "unit": "LF", "net": s_lf, "purchase": round(s_lf * 1.15, 2),
         "op": f"[DERIVED] sum of the 16 rows: {n_st} studs, sum(studs x H) = {s_lf} LF; purchase x 1.15 (Inputs waste metal 15 %); gauge not printed "
               "(A0.06 STUD SCHEDULE lists 20 GA only) - 20 GA assumed [PENDIENTE]", "fbm": "BASE_S250S125-33"},
        {"material": '2-1/2" track 20 GA (33 mil), top and bottom', "unit": "LF", "net": t_lf, "purchase": round(t_lf * 1.15, 2),
         "op": f"[DERIVED] 2 x sum(L) = {t_lf} LF; purchase x 1.15", "fbm": "BASE_T250T125-33"},
        {"material": '5/8" gypsum board, Type X (one face, stair side)', "unit": "SF", "net": b_sf, "purchase": round(b_sf * 1.06, 2),
         "op": f"[DERIVED] sum(L x H) of the 16 rows = {b_sf} SF; purchase x 1.06 (Inputs waste non-metal 6 %)", "fbm": "D58F12-U"},
        {"material": "Joint compound, all purpose (Level 4)", "unit": "LB", "net": mud, "purchase": mud,
         "op": f"[DERIVED] {b_sf} SF x 0.072 LB/SF (Inputs 23, yield, no waste) = {mud} LB", "fbm": None},
        {"material": "Joint tape, paper", "unit": "LF", "net": tape, "purchase": tape,
         "op": f"[DERIVED] {b_sf} SF x 0.37 LF/SF (Inputs 24, yield, no waste) = {tape} LF", "fbm": "DWT500W"},
        {"material": "Trims (corner bead / J-bead)", "unit": "LF", "net": 0.0, "purchase": 0.0,
         "op": "[DERIVED] 0: the 4 corners of each level are INSIDE corners (tape, no bead); the lining runs into the CMU / floor / roof deck "
               "with no exposed edge drawn on 7-11/A6.01", "fbm": None},
    ]
    C['add_alternates'] = [a for a in C.get('add_alternates') or [] if a.get('id') != 'ALTERNATE #1']
    C['add_alternates'].append({
        "id": "ALTERNATE #1", "n": 1, "rfi": "RFI-30",
        "texto": ("Stair 1 (Room 127) interior lining, Levels 1-4: 2-1/2\" metal stud furring @ 16\" o.c. + top / bottom track + 5/8\" Type X "
                  "gypsum board, one face, Level 4 finish"),
        "razon": ("the drawings show a 3-3/8\" layer on all four sides of the CMU stair enclosure (7-10/A6.01, 11/A6.01) but do not specify "
                   "its material, and the referenced Interior Drawings ('RE: INTERIOR DRAWINGS') were not included in the bid set. Excluded from "
                   "the base bid and priced as an add alternate until clarified"),
        "cantidades": [{"material": it["material"], "qty": it["net"], "unit": it["unit"], "op": it["op"]} for it in ITEMS],
        "delta_sf": b_sf, "material": '5/8" Type X', "items": ITEMS, "filas": rows,
        "labor": {"framing_wall_sf": b_sf, "hang_sf": b_sf, "finish_sf": b_sf}})
    # COORDINACIÓN 13-nov 05:51 (opción a): AA-1 (Level 5 en áreas públicas, alternate IMPRESO, no RFI) = ALTERNATE #2 (ADD), esquema v134
    for a_ in C['add_alternates']:
        if a_.get('id') == 'AA-1':
            sf_ = float(a_['delta_sf'])
            a_.update({
                "id": "ALTERNATE #2", "n": 2, "rfi": "none - printed alternate 1/A7.19 TF-1 ALT",
                "texto": "Level 5 finish (skim coat over the whole surface) on the exposed gypsum board of the public areas (corridors, lobbies, stairs, vestibules)",
                "razon": ("1/A7.19 FINISH SCHEDULE - PUBLIC SPACES lists 'TF-1 ALT - WALLS / CEILINGS PAINT ALT' in place of TF-1 '2 COAT PLASTER / CONC "
                          "FINISH'; 09 29 00 3.6.E.5 requires Level 5 for exposed drywall in public areas that will not receive wall covering or plaster, "
                          "while the base (plaster) is Level 4 (3.6.E.4). The same 1/A7.19 row also lists a vinyl wallcovering (Wolf Gordon Peckham), "
                          "which would stay Level 4; this alternate applies only if the alternate finish is paint"),
                "cantidades": [{"material": "Level 5 skim coat (whole surface)", "qty": sf_, "unit": "SF",
                                "op": "[DERIVED] 18,667.62 SF outer wall board layer facing public areas + 3,007.07 SF GYP-1 ceilings of public areas = 21,674.69 SF"}],
                "material": "Level 5 skim coat"})
    json.dump(C, open(CP, 'w'), indent=1, ensure_ascii=False)
    print(f"rev20c ALTERNATE #1: {len(LIN)} rows out of the base; board {b_sf} SF, studs {s_lf} LF ({n_st}), track {t_lf} LF, mud {mud} LB, tape {tape} LF")
else:
    print("rev20c ALTERNATE #1: already applied")
