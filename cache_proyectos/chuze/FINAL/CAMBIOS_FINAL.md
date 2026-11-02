# CAMBIOS FINAL — Chuze Fitness Austin Bluffs take-off (rev3 -> FINAL, 2026-11-02)

Source: orchestrator messages 2026-11-02 (estimator decision: close every open RFI with the recommended option = the conservative assumption already loaded) and the estimator standing rules (cache_proyectos/REGLAS_USUARIO_CLAUDE.md, REGLAS_ALCANCE.md). Built only through the tools (canon.py -> plantilla_excel.py armar / verificar, markups verificar).

## 1. Quantity check rev3 -> FINAL (full diff of the two Excels)

* Partition Takeoff: every rev3 row is identical in FINAL (**0 differences** in LF, height, layers, stud, O.C., board SF); FINAL adds the block EXISTING WALLS TO REMAIN - BOARD ONLY with 24 rows + SUBTOTAL (rule 4, after OTHER FRAMING; not in the partition GRAND TOTAL).
* Material Summary: 51 rows rev3 / 51 rows FINAL, 11 rows differ, **all from the four standing rules** (no other row moved): closing the RFIs with the recommended option changed no quantity.

| Material Summary row | Unit | rev3 NET | FINAL NET | rev3 pieces | FINAL pieces | Rule |
|---|---|---|---|---|---|---|
| 5/8" gypsum board, Type X | SF | 30456.68 | 58429.85 | 673 | 1291 | 4 (existing walls D0.07 / D0.52) |
| Cement board screws 1-1/4" (manufacturer spacing) | PCS | 1451.72 | 0 | 1670 | 0 | 1 (fasteners) |
| #10 framing screws - printed stud-to-track fastener (see Where it comes from) | PCS | 1148 | 0 | 1321 | 0 | 1 (fasteners) |
| Metal stud blocking at wall-mounted items (notes) | LF | 225.31 | 253.31 | 13 | 15 | 3 (R-ALC-02) |
| Stud reinforcement at MEP penetrations | PCS | 10 | 0 | 10 | 0 | 2 (R-ALC-03 ducts) |
| Power-driven fasteners and duct sleeves | PCS | 6 | 0 | 6 | 0 | 1 + 2 (fasteners / ducts) |
| Drywall screws #7 x 1-1/4" Type S bugle head (board on 25/20 ga studs) | PCS | 44898.7 | 0 | 44899 | 0 | 1 (fasteners) |
| Framing screws #8-18 x 1/2" pan head (25/20 ga studs) | PCS | 5140 | 0 | 5140 | 0 | 1 (fasteners) |
| Power-driven fasteners, slab pins for the bottom track | PCS | 828.6 | 0 | 829 | 0 | 1 (fasteners) |
| Joint compound, all purpose | LB | 2693.92 | 4707.99 | 2694 | 4708 | 4 (yield of the added board) |
| Joint tape, paper | LF | 13843.76 | 24193.84 | 13844 | 24194 | 4 (yield of the added board) |

## 2. Estimator standing rules applied (deltas)

| # | Rule | Applied to | Delta |
|---|---|---|---|
| 1 | ALL SCREWS / FASTENERS EXCLUDED (estimator standing rule 2026-10-31) | canon `fasteners_excluded` -> accesorios.py (R80e.77) + canon fasteners (tool R80w.37); rows kept at 0 with 'EXCLUDED - fasteners' (tool R80w.38); Scope Checklist ALC-X46 | drywall screws 44,898.7 -> 0, framing screws 5,140 -> 0, slab pins 828.6 -> 0, #10 / #12-24 TEK 1,148 -> 0, cement board screws 1,451.72 -> 0, PAFs 0; RFI-ACC-slab-pins closed (no RFI on fasteners) |
| 2 | R-ALC-03 ducts always excluded (2026-11-02) | 6 M110 duct crossings removed from the canon; `mep_sweep.excluded_by_estimator`; none-reason on the row; Scope Checklist ALC-X47 'EXCLUDED - framed openings for ducts (by others)' | stud reinforcement 10 -> 0 PCS, duct sleeves 6 -> 0 PCS; duct part of the MEP RFI removed (pipes: none loaded) |
| 3 | R-ALC-02 accessory blocking without printed width = 3'-0" x 2 rows | A103 straps keys 7 (1 tag, misc accessories), 9 (2 tags, drinking fountain), 16 (10 tags, misc accessories): 4 ft per tag -> 6 LF per tag; 10/A505.B AV niche: 2 printed studs x 3'-0" = 6 LF (was 2 x 2.0). Runs (lockers 8 / 18 / 50, cabinets 33 / 51 / 52, cubbies 48, storage 45) keep their run length | metal stud blocking 225.31 -> 253.31 LF (+28.00) |
| 4 | Estimator decision 2026-11-02: 'repair / replace if required' on existing walls to remain = full face replacement at wall height | AD101 D0.07 'EXISTING WALL TO REMAIN. REMOVE EXISTING FINISH MATERIALS AND SUBSTRATE WHERE REQUIRED. PATCH & REPAIR AS REQUIRED' (19 tags -> 23 straight runs, 555.66 LF, both faces) + D0.52 'EXISTING DEMISING WALL TO REMAIN. MAINTAIN EXISTING FIRE RATING & REPAIR ANY DAMAGE FROM DEMOLITION' (1 run, 113.96 LF, tenant face) at 22.83 ft (B.O. deck, RFI-01); canon existing_walls (tool R80w.39): Partition Takeoff block + one Bluebeam markup per wall on AD101 | 5/8" Type X 30,456.68 -> 58,429.85 SF (+27,973.17 = D0.07 25,371.46 + D0.52 2,601.71); joint compound / tape follow the board (yields) |

Existing walls loaded (straight runs on the AD101 vector at 3/32" = 6.75 pt/ft, stopped at demolished partitions and at the tenant demising line; nothing N.I.C.; drawing: imagenes_FINAL/AD101_existing_walls_D007_D052.png; same ids in the Partition Takeoff and the markups). Audit correction: EX-15 44.56 -> 38.98 LF (started between two D0.35 partitions); EX-04, EX-07, EX-09, EX-10 split into straight runs A / B; EX-03 / EX-14 / EX-04A measured as straight runs through the existing doors (board not deducted at openings).

| Wall | Keynote | Where | LF | Faces | SF |
|---|---|---|---|---|---|
| EX-01 | D0.07/AD101 | grid C.5 wall, Open Gym / lobby (west wall to the rev-8 cloud, D0.35 beyond) | 77.33 | 2 | 3,530.89 |
| EX-02 | D0.07/AD101 | north exit corridor, south wall (stair room to door D0.10) | 22.16 | 2 | 1,011.83 |
| EX-03 | D0.07/AD101 | north restroom block, corridor wall + west return | 26.67 | 2 | 1,217.75 |
| EX-04A | D0.07/AD101 | north restroom block, wall x1273 (through existing door D0.10, board not deducted) | 9.64 | 2 | 440.16 |
| EX-04B | D0.07/AD101 | north restroom block, wall x1348 | 4.27 | 2 | 194.97 |
| EX-05 | D0.07/AD101 | grid E wall, D0.45 wall to the curved storefront | 49.82 | 2 | 2,274.78 |
| EX-06 | D0.07/AD101 | men's locker north wall (above the removed lockers D0.58) | 35.99 | 2 | 1,643.3 |
| EX-07A | D0.07/AD101 | wall line y1622 over the women's shower area | 32.89 | 2 | 1,501.76 |
| EX-07B | D0.07/AD101 | locker east end wall x599 | 6.25 | 2 | 285.38 |
| EX-08 | D0.07/AD101 | women's shower area, west wall | 22.65 | 2 | 1,034.2 |
| EX-09A | D0.07/AD101 | women's shower / restroom east wall x575 (to the demising wall) | 41.07 | 2 | 1,875.26 |
| EX-09B | D0.07/AD101 | women's sinks room, south wall | 9.42 | 2 | 430.12 |
| EX-10A | D0.07/AD101 | women's restroom north wall | 17.64 | 2 | 805.44 |
| EX-10B | D0.07/AD101 | return wall x444 above the restroom | 4.98 | 2 | 227.39 |
| EX-11 | D0.07/AD101 | women's restroom east wall x444 | 10.74 | 2 | 490.39 |
| EX-12 | D0.07/AD101 | pool room west wall | 17.81 | 2 | 813.2 |
| EX-13 | D0.07/AD101 | room east of the pool, north wall | 10.79 | 2 | 492.67 |
| EX-14 | D0.07/AD101 | room east of the pool, east wall (through the door, board not deducted) | 14.86 | 2 | 678.51 |
| EX-15 | D0.07/AD101 | wall north of the men's locker room (from the D0.35 demo partitions, jog, to the east wall) | 38.98 | 2 | 1,779.83 |
| EX-16 | D0.07/AD101 | men's locker room west wall (to the demising wall) | 41.04 | 2 | 1,873.89 |
| EX-17 | D0.07/AD101 | men's restroom / corridor wall (to the demising wall) | 16.53 | 2 | 754.76 |
| EX-18 | D0.07/AD101 | corridor east wall (to the demising wall) | 16.53 | 2 | 754.76 |
| EX-19 | D0.07/AD101 | men's restroom north + east wall (to the demising wall) | 27.6 | 2 | 1,260.22 |
| EX-20 | D0.52/AD101 | existing south demising wall, tenant face (to the D0.50 concrete wall) | 113.96 | 1 | 2,601.71 |

## 3. RFI -> decision -> note (41 RFIs closed; Pending Items is empty; each one is a CLOSED row of the Scope Checklist)

| RFI | Decision applied | Internal note | Delta |
|---|---|---|---|
| RFI-01 | estimator decision 2026-11-02 (recommended option): 22'-10" (22.83 ft) everywhere, one zone | Recommend RFI to GC to confirm in field | applied in the quantities (0) |
| RFI-02 | estimator decision 2026-11-02 (recommended option): B2E studs to deck with 2" slip track; board to ceiling + 6" (E/A301) | - | applied in the quantities (0) |
| RFI-03 | estimator decision 2026-11-02 (recommended option): 6" studs and track | - | applied in the quantities (0) |
| RFI-04 | estimator decision 2026-11-02 (recommended option): 16" O.C.; 20 ga head D/E walls, 25 ga head C/F/G walls | Recommend RFI to GC to confirm in field | applied in the quantities (0) |
| RFI-05 | estimator decision 2026-11-02 (recommended option): 5/8" Type X everywhere; 5/8" Type X MR in locker rooms, restrooms, showers | - | applied in the quantities (0) |
| RFI-06 | estimator decision 2026-11-02 (recommended option): 5/8" cement backer board behind every printed tile zone (A421.C / A421.B / A424.C / A425.B elevations, A111 note 6 wainscot 5'-0", showers full height to the 9'-0" ceiling), tile top + 6", 1,209.77 SF (Material Summary cement backer row); gypsum board NOT deducted behind the backer (conservative) | - | applied in the quantities (0) |
| RFI-07 | estimator decision 2026-11-02 (recommended option): 2 layers 5/8" Type X each side | - | applied in the quantities (0) |
| RFI-08 | estimator decision 2026-11-02 (recommended option): drywall grid by us | - | applied in the quantities (0) |
| RFI-09 | estimator decision 2026-11-02 (recommended option): 6" x 20 ga @ 24" O.C. for 16/A502; storefront soffit drop edges framed like 8/A502 | Recommend RFI to GC to confirm in field | applied in the quantities (0) |
| RFI-10 | estimator decision 2026-11-02 (recommended option): soffit bottom 10'-0" | Recommend RFI to GC to confirm in field | applied in the quantities (0) |
| RFI-11 | estimator decision 2026-11-02 (recommended option): as drawn | - | applied in the quantities (0) |
| RFI-12 | estimator decision 2026-11-02 (recommended option): steel header by others at door / storefront heads (6/A602, 8/A602 'REF: STRUCT.'): 0 LF of metal stud header loaded | Recommend RFI to GC to confirm in field | applied in the quantities (0) |
| RFI-13 | estimator decision 2026-11-02 + estimator standing rule R-ALC-02 (2026-11-01): runs (lockers keys 8 / 18 / 50, cabinets keys 33 / 51 / 52, cubbies key 48, storage key 45) keep their run length (recommended option); single accessories whose width is not printed (A103 straps keys 7 / 9 / 16, 10/A505.B AV niche) = 3'-0" x 2 rows = 6 LF each | Recommend RFI to GC to confirm in field | +28.00 LF metal stud blocking (225.31 -> 253.31): keys 7 / 9 / 16 straps 52.0 -> 78.0 LF, 10/A505.B 4.0 -> 6.0 LF |
| RFI-14 | estimator decision 2026-11-02 (recommended option): 9 RTU curb caps 2/A131 as loaded (600S162-33 frame); the #10 TEK screws of the cap are EXCLUDED (estimator standing rule 2026-10-31, fasteners) | Recommend RFI to GC to confirm in field | applied in the quantities (0 framing); TEK screws excluded with the fasteners |
| RFI-15 | estimator decision 2026-11-02 (recommended option): trap primer 12x12 access panels - valve count not shown on P602: 0 loaded; G002 item 76 swimsuit spinner panel: no spinner on the plans (pool infilled): 0 | Recommend RFI to GC to confirm in field | applied in the quantities (0) |
| RFI-16 | estimator decision 2026-11-02 (recommended option): AD102 D0.63 hardlid repair / infill and D0.59 24" board strip: extents not dimensioned, not quantified (patch & repair allowance left to the estimator) | Recommend RFI to GC to confirm in field | applied in the quantities (0) |
| RFI-17 | estimator decision 2026-11-02 (recommended option): no gyp board on the top of head G walls | - | applied in the quantities (0) |
| RFI-18 | estimator decision 2026-11-02 (recommended option): as RFI-04 | Recommend RFI to GC to confirm in field | applied in the quantities (0) |
| RFI-19 | estimator decision 2026-11-02 (recommended option): casework framing EXCLUDED | - | applied in the quantities (0) |
| RFI-20 | estimator decision 2026-11-02 (recommended option): A6D, 5.23 LF, to deck | Recommend RFI to GC to confirm in field | applied in the quantities (0) |
| RFI-21 | estimator decision 2026-11-02 (recommended option): ceiling + 6"; deck where the face is open/finished to deck | Recommend RFI to GC to confirm in field | applied in the quantities (0) |
| RFI-22 | estimator decision 2026-11-02 (recommended option): A3C | Recommend RFI to GC to confirm in field | applied in the quantities (0) |
| RFI-23 | estimator decision 2026-11-02 (recommended option): new B2E (34.29 LF) | - | applied in the quantities (0) |
| RFI-24 | estimator decision 2026-11-02 (recommended option): A6D, 3.16 LF, 7'-0" | Recommend RFI to GC to confirm in field | applied in the quantities (0) |
| RFI-25 | estimator decision 2026-11-02 (recommended option): not loaded (existing curved storefront to remain, AD101 D0.15); the A1.15 impact board zone is on that wall | - | applied in the quantities (0) |
| RFI-26 | estimator decision 2026-11-02 (all projects): an existing wall to remain with 'remove existing finish materials and substrate where required' (AD101 D0.07, 19 tags = 23 straight runs) or an existing demising wall 'repair any damage' (AD101 D0.52) gets the full face replaced at wall height: 5/8" Type X loaded on both faces of the D0.07 walls (555.66 LF) and on the tenant face of the D0.52 demising wall (113.96 LF) at 22.83 ft, one row per wall in the Partition Takeoff block EXISTING WALLS TO REMAIN - BOARD ONLY and one markup per wall on AD101; A1.11 / A1.13 FRT plywood = wood, EXCLUDED (Div. 06); no re-furring of the existing CMU walls (only the tagged B2E furring) | Recommend RFI to GC to confirm in field | +27,973.17 SF 5/8" Type X (D0.07 25,371.46 + D0.52 2,601.71) |
| RFI-27 | estimator decision 2026-11-02 (recommended option): 12'-1" | - | applied in the quantities (0) |
| RFI-28 | estimator decision 2026-11-02 (recommended option): 6 x 16 ga track at the top of the 5'-0" low wall, 9.99 LF (inside the metal blocking row) | - | applied in the quantities (0) |
| RFI-29 | estimator decision 2026-11-02 (recommended option): 7'-0" / 9'-0" / 10'-0" / 3'-4" x 7'-2" | Recommend RFI to GC to confirm in field | applied in the quantities (0) |
| RFI-30 | estimator decision 2026-11-02 (recommended option): as loaded | - | applied in the quantities (0) |
| RFI-31 | estimator decision 2026-11-02 (recommended option): C3D | - | applied in the quantities (0) |
| RFI-32 | estimator decision 2026-11-02 (recommended option): 2-1/2" studs for B2E; MR board per the A111 note 3 room list (LOCKER / RESTROOM / SHOWER / TOILET / POOL / JANITOR / LAUNDRY / SPA / SAUNA rooms, constants.mr_rooms_note) | - | applied in the quantities (0) |
| RFI-33 | estimator decision 2026-11-02 (recommended option): 0 LF - openings framed with the grid's own main / cross tees (rows of the USG grid) | Recommend RFI to GC to confirm in field | applied in the quantities (0) |
| RFI-34 | estimator decision 2026-11-02 (recommended option): 0 (EXCLUDED) | - | applied in the quantities (0) |
| RFI-35 | estimator decision 2026-11-02 (recommended option): 6" 20 ga stud, 3 braces per soffit x 2.83 ft (diagonal of the 2'-0" box) = 16.96 LF | Recommend RFI to GC to confirm in field | applied in the quantities (0) |
| RFI-36 | estimator decision 2026-11-02 (recommended option): kickers of the wall stud @ 48" O.C. at 45 deg from the top of each head-C wall that stops at the ceiling to the deck (ROUNDUP(L/4)+1 per wall), 424.23 LF (3-5/8" 380.74 + 6" 43.49) | Recommend RFI to GC to confirm in field | applied in the quantities (0) |
| RFI-37 | estimator decision 2026-11-02 (recommended option): 1/A506 as drawn - 16 ga x 4" legs deflection track around the 2'-6" x 3'-0" hatch (11.0 LF) + 16 ga top runner tracks 2 x 5'-0" (10.0 LF); steel ladder 3/A506 = misc. metals EXCLUDED | Recommend RFI to GC to confirm in field | applied in the quantities (0) |
| RFI-ACC-slab-pins | estimator standing rule 2026-10-31 (all projects): all fasteners EXCLUDED (slab pins / PAF, screws, anchors, TEK, bolts = 0); no RFI on fasteners | - | -828.6 slab pins (fasteners excluded) |
| RFI-ACC-stud-reinforcement-mep | estimator standing rule R-ALC-03 (2026-11-02, all projects): framed openings / stud reinforcement for ducts crossing walls or ceilings EXCLUDED (by others); pipes: no pipe size printed at the crossings on P110 / P111, none loaded (recommended option) | Recommend RFI to GC to confirm in field | -10 stud reinforcement plates, -6 duct sleeves |
| RFI-ACC-access-panel | estimator decision 2026-11-02 (recommended option): access panel 24"x24" x 1 (A131 A4.10) loaded; trap primer 12x12 panels: valve count not shown (P602), 0 loaded | Recommend RFI to GC to confirm in field | applied in the quantities (0) |
| RFI-ACC-gypsum-board-jamb-return | estimator decision 2026-11-02 (recommended option): no cased-opening head / jamb detail in the set; board stops at the frame (6/A602, 8/A602): 0 SF loaded | Recommend RFI to GC to confirm in field | applied in the quantities (0) |

## 4. Tool changes (generic, test fails before, rows in tools/CAMBIOS_tools_v80w.md)

* R80w.37 canon.py: `fasteners_excluded` also zeroes the canon fastener families (TEK, cement board screws, P.A.F., anchors) with 'EXCLUDED - ... computed before = X' (`test_fasteners_canon.py`).
* R80w.38 plantilla_excel.py: a canon family excluded by the estimator keeps its Material Summary row at 0 with the note (`test_excluded_zero_row.py`).
* R80w.39 canon.py / plantilla_excel.py / markups_bluebeam.py: `existing_walls` (board only, straight-run path, length = path / sheet scale) -> board family, Partition Takeoff block EXISTING WALLS TO REMAIN - BOARD ONLY with SUBTOTAL, one markup per wall (Subject 'EXISTING - BOARD ONLY', Depth = height) (`test_existing_walls.py`).
* R80w.40 accesorios.py: an excluded fastener row keeps the sheet citations of its item (`test_fastener_sheet.py`).

## 5. Text / status

* `takeoff.json`: `rfis` = [] and `rfi_cierre` with the 41 decisions (plantilla R80e.96: decided RFIs leave Pending Items and become CLOSED rows of the Scope Checklist).
* ALC-05 and ALC-17: registro pendiente_rfi -> verificado (registro.py marcar, RFI answered); ALC-08 / ALC-16 notes annexed (registro.py anexar).
* B.O. deck (`deck_height`) status PENDIENTE -> DERIVADO by estimator decision (RFI-01 closed); Inputs note rewritten; walls already showed [DERIVED].
* Partition Takeoff unchanged (no quantity, height or status moved).
