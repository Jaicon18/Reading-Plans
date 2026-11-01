# PASO 12 - Error library (BIBLIOTECA_ERRORES.md) vs VS #679 Downey take-off rev2

Files: Takeoff_rev2.xlsx, takeoff_canon.json, VS679_bidset_LIMPIO.pdf (crops rendered at 110-170 dpi, _work/img/). 105 unique test IDs (BE-109 does not exist; BE-101 has two definitions, both evaluated).

**54 PASS · 17 FAIL · 34 N/A** - verdict: NOT DELIVERABLE until the FAILs are corrected.

| ID | Result | Evidence |
|---|---|---|
| BE-01 | N/A | No 'FIRE STOP' top-track / ceiling-line detail in the set: B/A12.01 (fire barrier) is VOID and the one-hour partition is struck through on M/A02.01; A/A12.01 and C/A12.01 show standard top track (A12.01 p31) |
| BE-02 | N/A | No W.R. note for walls or ceilings: A15.04 092900 H prints 'UL LISTED FIRE RESISTANT GYPSUM BOARD THROUGHOUT' only; A13.01 general notes / keynotes 1-32 have no MR/W.R. call (A13.01 p33, A15.04 p40) |
| BE-03 | PASS | Wet rooms (restrooms W/E, hallway, break room, electrical): no W.R. printed; all their faces are 5/8 Type X per 092900 H (Partition Takeoff W048-W050, W061, W068, W070, W073, I07). Observation: the same restrooms are named 'RESTROOM 1/2' on W048-W050/W061/W077 and 'RESTROOM W/E' on W068/W070/W073/ceilings |
| BE-04 | PASS | No face carries W.R.; the only MR board (1/2" MR under SF-91, D/A08.10) is on storefront faces that draw gyp bd |
| BE-05 | PASS | M/A02.01: (1) layer 5/8 Type X ea. side (STD), one side at void/furred (C/A12.01), RFID non-sales foil-backed / sales Type X; Excel 'Board by face' matches side by side (W074-W077 regular=foil side, other side Type X) |
| BE-06 | PASS | Cashwrap backwrap soffit SS1 both sides (Room 4 2.58 ft + soffit 0.75 ft) + bottom 30.91 SF (F/A10.05); beauty valances VAL-N/S/T5/SW/NW/NE face + bottom 136.6 SF (B/A10.03 'G.C. SHALL NOT APPLY GYP. BD. TO INTERIOR SIDE OF VALANCE') |
| BE-07 | N/A | Partition types are by hatch on A02.01 (SHEET_MAP); no partition tags, no 'SIM.' tags |
| BE-08 | PASS | Walls with printed dims within 1": FR walls W083/W084/W091/W094/W095 5.11-5.12 vs 5'-2" (A02.01), FR widths 4'-6" HOLD (ceilings 4.5), Room 4 runs 18'-10 1/2" OVERALL = 18.875; canon length_printed_ft on 3 walls all within 1". Observation: 107 of 118 lengths are DERIVADO from the A02.01 vector |
| BE-09 | PASS | (E) demising walls excluded (types_none_reason, A02.01 keynote 26 / A01.01 keynote 7); repair 'if required' = RFI-13 (Pending Items) |
| BE-10 | PASS | HOLD dims quantified: FR 4'-6" HOLD (ceilings FR1-FR5), GO-BACK 5'-0" HOLD, display window 13'-5 7/8" HOLD, CW closets 2'-1" HOLD |
| BE-11 | PASS | Every 'PLYWOOD / FRT BLOCKING' area (A08.10/A08.15, N/S03.01, K/A10.08, S/A14.01) has a destination: EXCLUDED Div. 06 by estimator order (ALC-10, ALC-26) |
| BE-12 | FAIL | (1) Pending Items RFI-ACC-deflection-clips: 'the general note asks for them at non-load-bearing walls' - no such note in S01.01 Structural Notes B.1-B.14, A15.04 092900 or M/A02.01 Partition Schedule General Notes 1-4; Material Summary R59 says 'none in the set' (contradiction). (2) Canon/blocking 'Beauty cabinet fluted wall runs' cites K/A10.03 - K/A10.03 'BEAUTY CABINET SECTION AT FLUTED WALL' is VOID (also F, G, J/A10.03 VOID) (A10.03 p27) |
| BE-13 | PASS | E/M/P sweep registered (canon mep_sweep, E01.01-E07.02 = 0 framed items); IT/music plywood mounting boards S/A14.01, R/A14.01 = EXCLUDED wood; access panels RFI-22 |
| BE-14 | FAIL | Material Summary R17 'Ceiling perimeter track at GWB ceilings (size not printed, RFI)': the size IS printed - B/A10.03 '5/8" GYP BD ON 1-5/8" MTL FRAMING AT 16" O.C.' (valance face) and '5/8" GYP BD ON 3-5/8" MTL FRAMING AT 16" O.C.' (soffit bottom); and no RFI for it exists in Pending Items. R17 breakdown is exactly the VAL/SS1 soffit-side tracks (VAL 141.0 LF + SS1 30.25 LF) |
| BE-15 | FAIL | (1) R35 'Metal stud blocking at wall-mounted items' 1,543.3 LF bought as 'stick 20 ft' studs: F/A12.01 prints '6" X 18 GA. BACKING TRACK' and E/A12.01 '6" X 18 GA. BACKING PLATE'; S01.01 B.7 'TRACK BLOCKING ... SUCH AS F/A12.01 ... SHALL BE 18 GA (43 MIL) WITH 1 1/4" FLANGES'. (2) R18 bridging C.R. channel carried on every wall at every 48" row: R/S03.01 NOTE 'BRIDGING IS NOT REQUIRED IF SHEATHING IS ATTACHED TO BOTH FACES OF THE STUD (SHEATHING INCLUDES ... GYPSUM BOARD ...)' (S03.01 p45, A12.01 p31, S01.01 p43) |
| BE-16 | FAIL | M/S01.01 'TOP TRACK SPLICE - STRUCTURAL STUDS': METAL STUD x 1'-0" (gauge to match track) at every top-track splice - no row; the canon writes 'top track splices per M/S01.01' on every wall but no quantity reaches the Material Summary |
| BE-17 | N/A | All fasteners EXCLUDED by estimator order (Material Summary R50, R52-R55, R60-R61 = 0 with note) |
| BE-18 | FAIL | GAPs: (a) M/S01.01 top-track splice pieces (BE-16); (b) B/A10.03 3 rows '6" CONTINUOUS METAL BLOCKING ... TYP AT THREE LOCATIONS' carried only on the 2 x 18'-10 1/2" runs (113.25 LF); the VAL-SW 9.375 run and one 4.625 return carry no blocking and the TRANS 5 W-face beauty run carries the 4-row Garcy pattern (B/A10.02) instead of 3 rows |
| BE-19 | N/A | Fasteners excluded (estimator order); no fastener spacing carried |
| BE-20 | FAIL | R41/R42 framed soffit computed as ROUNDUP(depth/1.333)+1 = 3 members x run length (3 x 70.5 = 211.5 LF; 3 x 15.139 = 45.42 LF), i.e. members running along the soffit; B/A10.03 draws the soffit bottom '5/8" GYP BD ON 3-5/8" MTL FRAMING AT 16" O.C.' as members spanning wall-to-valance (1'-11 1/4" GYP TO GYP) spaced 16" along the run |
| BE-21 | PASS | No glass mat carried |
| BE-22 | PASS | R48 jamb return = 0 citing A/A08.10, D/A08.10 and door frames A00.02 / A10.08 |
| BE-23 | PASS | No acoustical sealant row; ALC-19 EXCLUDED |
| BE-24 | PASS | Bottom 787.04+5.56+16.86+52.7 = 862.16 LF = top 741.99+5.56+16.86+52.7 + deep-leg 45.05 (R4-R11, R29); separate rows; partitions GRAND TOTAL 809.454 = 787.04+5.56+16.86 |
| BE-25 | PASS | Every GWB ceiling cites N/A12.02 (usg_grid, A03.01 bubble N/A12.02 TYP) or its soffit detail F/A10.05 / B/A10.03; A15.04 092950 drywall grid |
| BE-26 | N/A | No ballistic type in M/A02.01 |
| BE-27 | N/A | No ATM / equipment recess (R46, A02.01 keynotes) |
| BE-28 | N/A | No canopy / parapet (ALC-03, ALC-14; A08.01) |
| BE-29 | PASS | Headers from S01.01 coded note 15 'HEADER: DOUBLE 3 5/8", 20 GA WITH 3 5/8" 20 GA TRACK AT BOTTOM' + A10.08 lintels; 16 openings in R19 |
| BE-40 | FAIL | Rows without a valid N/SHEET or breakdown summing the NET: R7/R11 'N/SHEET: default (no sheet)' 52.7 LF; R16 1-5/8" stud 496.5 LF (only 88+92 listed); R22 1/2" sheathing 502.17 SF (only 78.17 listed); R24-R27 USG grid 'default (no sheet)' and no total; R34 stud blocking at edge 71.1 LF (listed values do not sum to 71.1; canon edge_blocking_none_reason says none printed); R37 cement board 'default (no sheet)'; R41/R42 breakdown mixes both soffits (45.42 + 211.5 'shown = 45.42' / '= 211.5') |
| BE-41 | PASS | No .json/.py/work folders in the 6 visible sheets |
| BE-42 | PASS | Order STD, FUR, COL, INS, RFID, SF = M/A02.01 row order (FUR = STD row as furring); subtotals 441.786+211.005+16.872+45.05+59.81+34.931 = 809.454 = GRAND TOTAL (Partition Takeoff C84-C120) |
| BE-43 | PASS | Exactly 6 visible sheets + hidden _reglas |
| BE-44 | FAIL | No Bluebeam markup PDF in the delivery (only the clean bid set, 0 /Annots on 71 pages): cuadre per type cannot be shown |
| BE-45 | PASS | Board 18,111 SF X vs walls+ceilings consistent; track = partitions; compound/tape = 18,666 SF board x yields. Observations: hangers 713 for ~6,350 SF of GWB ceiling (8.9 SF/hanger vs 16 SF at 4'x4', +1 each direction); bridging ratio covered in BE-15 |
| BE-46 | FAIL | R30 one row mixes DBL 10" 16 GA studs, 3-5/8" 20 GA track, 3-5/8" 16 GA track (808.87 LF); R28 mixes 5 clip products (2x2x16 clip angle, L2x2x16x5", 2x2x6" 12 GA clip, 1-1/2x1-1/2x16 clip, R/S03.01 channel clip); R22 '1/2" EXTERIOR gypsum sheathing' holds 1/2" MOISTURE RESISTANT gyp bd (printed D/A08.10, A/A08.05); R21 '5/8" regular' is the RFID FOIL-BACKED board (M/A02.01, 092900 H.3); R51 'Access panel 36"x12"' qty 3 includes the 24"x24" (A03.01 keynote 8); R35 mixes E/A12.01 plate and F/A12.01 track |
| BE-47 | FAIL | IDs cited but not in Pending Items: RFI-04 (ALC-09), RFI-05 (ALC-23), RFI-06 (ALC-13), RFI-08 (ALC-05) - closed in the canon, still cited as open questions; R17 cites an 'RFI' that does not exist |
| BE-48 | N/A | No markup PDF delivered; bid-set copy has no added pages and no .json/.py text |
| BE-49 | PASS | Sampled: 18'-10 1/2" OVERALL (Room 4 runs), 14'-1 1/2" / 14'-6" OVERALL (TRANS 5 faces), 4'-6" HOLD (FR) belong to the element quantified |
| BE-50 | PASS | MEP overlaps go to RFI-15 (ducts) / RFI-22 (access panels); stud reinforcement at MEP excluded by estimator order (R45) |
| BE-51 | FAIL | R31 metal reveal: Unit LF, Selling unit 'piece', H31 '=ROUNDUP(F31,0)' = 100 'pieces' for 99.21 LF (trim stick 10 ft is Inputs B18) |
| BE-52 | PASS | 'covered by' claims re-checked: GAP19 bridging -> R18 per-wall breakdown contains every wall; pipe-rail blocking (gap 11) -> 8'-3" row present in every Garcy run |
| BE-53 | PASS | RFI-17 and RFI-26 deltas list the printed pieces of their details (diagonals 16 pcs, 2 1/2" studs, edge members) |
| BE-54 | N/A | No per-product split of board (Type S/S-12): fasteners excluded |
| BE-55 | FAIL | Internal codes in client text: 'GAP1..GAP19' (R12, R15, R20, R23, R28, R30-R33, R35, R39), schema keys 'misc_items', 'frp_info', 'pvc_trim_items' (R49), 'readings A and B' (ALC-08), 'skill standing rule U8' (ALC-19), 'rule 58.7' (ALC-20) |
| BE-56 | N/A | Fasteners excluded |
| BE-57 | PASS | Every non-metal row (board, cement board, FRP, PVC, Level 5) uses 0.06; metal rows 0.15 |
| BE-58 | PASS | _reglas: 'reglas.py compuerta OK' with canon/reglas hashes v73 (run log not in delivery) |
| BE-59 | PASS | All Partition Schedule types with walls (STD, FUR, COL, INS, RFID, SF) or types_none_reason ((E), one-hour struck) |
| BE-60 | PASS | Canon has plan_scale_pt_per_ft 18, every ceiling has system_callout / detail |
| BE-61 | N/A | runner-internal process test (B&N/O'Reilly API runner); no run log, costos.csv, sandbox or reading A/B files in this delivery - not testable on this project's deliverables |
| BE-62 | PASS | Column wraps CW1-CW4 as COL elements |
| BE-63 | N/A | runner-internal process test (B&N/O'Reilly API runner); no run log, costos.csv, sandbox or reading A/B files in this delivery - not testable on this project's deliverables |
| BE-64 | N/A | runner-internal process test (B&N/O'Reilly API runner); no run log, costos.csv, sandbox or reading A/B files in this delivery - not testable on this project's deliverables |
| BE-65 | PASS | plan_scale_pt_per_ft 18 and band.sheet A02.01 on every wall |
| BE-66 | N/A | runner-internal process test (B&N/O'Reilly API runner); no run log, costos.csv, sandbox or reading A/B files in this delivery - not testable on this project's deliverables |
| BE-67 | N/A | runner-internal process test (B&N/O'Reilly API runner); no run log, costos.csv, sandbox or reading A/B files in this delivery - not testable on this project's deliverables |
| BE-68 | N/A | runner-internal process test (B&N/O'Reilly API runner); no run log, costos.csv, sandbox or reading A/B files in this delivery - not testable on this project's deliverables |
| BE-69 | PASS | Board split by product/use (regular-foil, Type X, 1/2") - product naming issues in BE-46 |
| BE-70 | PASS | Soffit sides SS1 + 6 VAL carried |
| BE-71 | N/A | runner-internal process test (B&N/O'Reilly API runner); no run log, costos.csv, sandbox or reading A/B files in this delivery - not testable on this project's deliverables |
| BE-72 | PASS | 4 column wraps of A02.01 carried (CW1-CW4, ALC-15) |
| BE-73 | PASS | Returns W116-W120 carried inside type STD |
| BE-74 | N/A | runner-internal process test (B&N/O'Reilly API runner); no run log, costos.csv, sandbox or reading A/B files in this delivery - not testable on this project's deliverables |
| BE-75 | N/A | runner-internal process test (B&N/O'Reilly API runner); no run log, costos.csv, sandbox or reading A/B files in this delivery - not testable on this project's deliverables |
| BE-76 | PASS | Type X applied on every face except the RFID foil side; 0 'regular' faces outside RFID |
| BE-77 | N/A | runner-internal process test (B&N/O'Reilly API runner); no run log, costos.csv, sandbox or reading A/B files in this delivery - not testable on this project's deliverables |
| BE-78 | PASS | Heights from A12.01 ±12'-0" T.O. STUD and A01.01 structure callouts, no placeholders |
| BE-79 | N/A | runner-internal process test (B&N/O'Reilly API runner); no run log, costos.csv, sandbox or reading A/B files in this delivery - not testable on this project's deliverables |
| BE-80 | PASS | Column wraps carried (4), none excused |
| BE-81 | N/A | runner-internal process test (B&N/O'Reilly API runner); no run log, costos.csv, sandbox or reading A/B files in this delivery - not testable on this project's deliverables |
| BE-82 | PASS | Single plan sheet A02.01; no wall counted twice (W-ids unique, Σ = 809.454 LF) |
| BE-83 | PASS | No face above its room ceiling + 0.5 ft (script over canon faces vs ceilings) |
| BE-84 | PASS | Corner bead derived: 924.25 LF outside corners + wraps/piers/cased openings (R36) |
| BE-85 | PASS | accesorios_none do not contradict decisions |
| BE-86 | PASS | length_source cites A02.01 band |
| BE-87 | N/A | Skill numbering, not a project deliverable |
| BE-88 | PASS | Pending Items has the 3 fixed columns; alternatives (A)/(B)/(C) inside 'Delta of each alternative' |
| BE-89 | PASS | 105 walls x exactly 2 ends from 165 nodes (59 L, 49 T, 57 free) |
| BE-90 | PASS | Opening schedule declared (16 openings + 2 none with reason) |
| BE-91 | N/A | runner-internal process test (B&N/O'Reilly API runner); no run log, costos.csv, sandbox or reading A/B files in this delivery - not testable on this project's deliverables |
| BE-92 | N/A | runner-internal process test (B&N/O'Reilly API runner); no run log, costos.csv, sandbox or reading A/B files in this delivery - not testable on this project's deliverables |
| BE-93 | PASS | Faces topped at room ceilings (see BE-83) |
| BE-94 | N/A | runner-internal process test (B&N/O'Reilly API runner); no run log, costos.csv, sandbox or reading A/B files in this delivery - not testable on this project's deliverables |
| BE-95 | N/A | runner-internal process test (B&N/O'Reilly API runner); no run log, costos.csv, sandbox or reading A/B files in this delivery - not testable on this project's deliverables |
| BE-96 | N/A | runner-internal process test (B&N/O'Reilly API runner); no run log, costos.csv, sandbox or reading A/B files in this delivery - not testable on this project's deliverables |
| BE-97 | PASS | W020 STOCK both sides named with side (B STOCK / A STOCK) |
| BE-98 | PASS | (E) demising excluded by type with cite (RFI-13) |
| BE-99 | N/A | Process test (blind-test selection); nothing in this delivery reads a human take-off |
| BE-100 | PASS | Bid set: 0 /Annots on 71 pages (pymupdf) |
| BE-101 | FAIL | (section version) Pending item RFI-ACC-deflection-clips option (A) claims a printed general note that is not printed (see BE-12) and R59 = 0 'none in the set'; (table version: runner cost rows = N/A) |
| BE-102 | FAIL | N/SHEET fields cite truncated sheets that do not exist in SHEET_MAP: 'C/A12', 'A/A12', 'B/A10', 'P/A07', 'N/S03', 'A/S02' (A12, A10, A07, S03, S02 are not sheets; B/A10 could be A10.02 or A10.03), and 'I06/I05' (wall ids) in R15 |
| BE-103 | N/A | No markups delivered; sheets are vector, not raster |
| BE-104 | N/A | No type with two systems (FUR = C/A12.01 stud furring only) |
| BE-105 | FAIL | Printed product carried as unsized default: R17 'size not printed' while B/A10.03 prints 1-5/8" / 3-5/8" framing (BE-14); F/A12.01 18 GA backing track and E/A12.01 18 GA plate replaced by generic 'metal stud blocking' sticks (BE-15) |
| BE-106 | PASS | 'estimator' phrases cite this project's order (VS #679 brief 2026-11-01) or are labelled precedent (Inputs B26 'precedent ... previous project'). Observation: R50-R61 name another project ('O'Reilly') in client text |
| BE-107 | PASS | fasteners_excluded: every screw/anchor/pin row = 0 with EXCLUDED note |
| BE-108 | N/A | Precedent files (SKILL_working.md) not in delivery |
| BE-110 | PASS | Board not reduced for openings (ALC-07); no scaled heights |
| BE-111 | PASS | Interior SF faces at room ceilings; only MALL CONCOURSE faces use B.O. (E) MALL SOFFIT 13'-8 1/2" (A/A08.01) |
| BE-112 | N/A | No PEMB, CMU furring or hung header walls of the O'Reilly type |
| BE-VS-01 | PASS | Heights cite A01.01 'LOWEST POINT OF DECK 17'-0" / STRUCTURE 12'-1"' and keynote 19/20 callouts (canon estructura_a0101_info) |
| BE-VS-02 | PASS | All GWB ceilings 5/8 Type X per A15.04 092900 H |
| BE-VS-03 | FAIL | Coverage GAPs remain: top-track splices M/S01.01; beauty-cabinet blocking runs (B/A10.03) - see BE-16 / BE-18 |
| BE-VS-04 | FAIL | Double count: ceiling ROOM 4 BEAUTY 3 = 24.444 x 48.333 - closets - cashwrap soffit (1,131.86 SF) does not deduct the beauty-valance soffit zone (70.5 LF x 1'-11 1/4" = 136.6 SF) that is carried again as 'ceiling BEAUTY CABINET VALANCE 136.6' (R23); B/A10.03 ends the ceiling at the valance ('SEE CEILING PLAN' at valance top) |

## FAIL detail (quantity impact; never scaled)

- **BE-12** - Quote attributed to a printed general note that is not printed; blocking cites a VOID detail. Source: Pending Items RFI-ACC-deflection-clips vs S01.01 Structural Notes B.1-B.14, A15.04 092900, M/A02.01 general notes 1-4 (no deflection-clip note); canon blocking 'Beauty cabinet fluted wall runs' cites K/A10.03 = VOID (A10.03). Fix: Rewrite RFI-ACC-deflection-clips as 'not printed / skill default' (only L/S03.01 deep-leg track is printed) or delete it; cite B/A10.03 (not K/A10.03) for the beauty-cabinet blocking. Delta: 0 (text); RFI delta 55 pcs is a default, not a printed quantity.
- **BE-14** - R17 says ceiling perimeter track size 'not printed, RFI' - size is printed and no such RFI exists. Source: B/A10.03 '5/8" GYP BD ON 1-5/8" MTL FRAMING AT 16" O.C.' (valance) and '...ON 3-5/8" MTL FRAMING AT 16" O.C.' (soffit bottom); F/A10.05. Fix: Split R17: 1-5/8" track at valances (VAL 2 x 70.5) and 3-5/8" track at SS1; remove 'not printed, RFI'. Delta: Reclassify 141.0 LF to 1-5/8" track + 30.25 LF to 3-5/8" track (R17 171.25 -> 0).
- **BE-15** - (1) In-wall blocking bought as 3-5/8" stud sticks; printed product is 6" x 18 GA backing track (F) / 6" x 18 GA flat backing plate (E), 18 ga with 1-1/4" flanges. (2) Bridging C.R. channel and clips carried on double-faced walls where R/S03.01 says bridging is not required. Source: F/A12.01, E/A12.01, S01.01 B.7; R/S03.01 NOTE 'BRIDGING IS NOT REQUIRED IF SHEATHING IS ATTACHED TO BOTH FACES OF THE STUD (... GYPSUM BOARD ...)'; S01.01 N note 2. Fix: R35 -> '6" x 18 GA backing track 1-1/4" flange (F/A12.01)' 1,302.63 LF + '6" x 18 GA backing plate (E/A12.01)' 198.0 LF + E-or-F 39.0 LF (lockers, comm boards) + signage 3.67 LF; R18 / R28 bridging only on single-faced walls and above board height. Delta: Bridging 1-1/2" CRC -837.55 LF net (1,739.06 -> 901.51); R/S03.01 channel clips approx -868 EA (1,031 -> approx 163); blocking: 1,543.3 LF of 3-5/8" stud -> 6" 18 ga track/plate (same LF).
- **BE-16** - Top-track splice pieces printed, no row. Source: M/S01.01 TOP TRACK SPLICE - STRUCTURAL STUDS 'METAL STUD x 1'-0" (GAGE TO MATCH GAGE OF TRACK)'; canon top_track 'top track splices per M/S01.01'. Fix: Add row: 3-5/8" stud x 1'-0" per top-track splice (one per joint of the 10 ft runs). Delta: +40 PCS x 1'-0" = +40 LF 3-5/8" 20 ga stud minimum (one joint per 10 ft on the walls longer than 10 ft); up to approx +85 LF if counted per purchased stick joint.
- **BE-18** - Coverage GAPs: splices (BE-16) and beauty-cabinet blocking not on every B/A10.03 run. Source: B/A10.03 '6" CONTINUOUS METAL BLOCKING BEHIND GYP BD, TYP AT THREE LOCATIONS (7'-9", 4'-5", 0'-11" C of blocking)'; runs VAL-N/S 18.875, T5 14.125, SW 9.375, NW/NE 4.625 (A02.01). Fix: 3 rows on every beauty-cabinet run (70.5 LF), and not the 4-row Garcy pattern on the TRANS 5 W face. Delta: 3 x 70.5 = 211.5 LF required vs 113.25 + 56.5 + 18.5 = 188.25 LF carried on these faces -> approx +23.25 LF 6" 18 ga track (verify which 4'-7 1/2" face is the beauty return on A02.01).
- **BE-20** - Framed soffit bottom framing counted as 3 members running the length instead of members @16" O.C. spanning wall-to-valance. Source: B/A10.03 '5/8" GYP BD ON 3-5/8" MTL FRAMING AT 16" O.C.', 1'-11 1/4" GYP TO GYP; F/A10.05 for the cashwrap soffit. Fix: Joists = sum per run (ROUNDUP(L/1.333)+1) x depth, plus the two runner tracks along each run. Delta: Valances: 63 joists x 1.9375 = 122.06 LF vs 211.5 -> -89.44 LF 3-5/8" stud; cashwrap (if F/A10.05 frames the same way): 13 x 2.042 = 26.55 vs 45.42 -> -18.87 LF; runner tracks along the runs per BE-14.
- **BE-40** - Rows without N/SHEET or without a breakdown that sums the NET. Source: Material Summary R7, R11, R16, R22, R24-R27, R34, R37, R41, R42. Fix: Give each row its N/SHEET (R24-R27: N/A12.02 + A15.04 092950; R37: A00.03 B-13 / A05.01) and a per-item breakdown that sums the NET; split R41/R42 text. Delta: 0 (traceability); R34 71.1 LF has no identifiable source - remove or justify.
- **BE-44** - No Bluebeam markups in the delivery. Source: Delivery package (bid set has 0 /Annots). Fix: Deliver the markup PDF (one annot per wall, Subject = type, Depth = height) and the per-type reconciliation. Delta: n/a.
- **BE-46** - Several products / sizes in one row; wrong product names. Source: R30 (DBL 10" 16 GA studs + 3-5/8" 20 GA track + 3-5/8" 16 GA track), R28 (5 clip products), R22 (1/2" MR gyp bd per D/A08.10, A/A08.05 carried as exterior sheathing), R21 (RFID foil-backed board per M/A02.01 / 092900 H.3 named 'regular'), R51 (36x12 + 24x24 panels), R35 (E plate + F track). Fix: One product, size and gauge per row; rename R21 '5/8" foil-backed gyp bd' and R22 '1/2" moisture resistant gyp bd'; split R51 into 2 x 36"x12" and 1 x 24"x24". Delta: R30 808.87 LF split: 10" 16 ga studs 74.04 LF; 3-5/8" 16 ga track 36.42 LF; 3-5/8" 20 ga track/members 698.41 LF; quantities otherwise unchanged.
- **BE-47** - RFI IDs cited that are not in Pending Items. Source: Scope Checklist ALC-05 (RFI-08), ALC-09 (RFI-04), ALC-13 (RFI-06), ALC-23 (RFI-05); Material Summary R17 'RFI'. Fix: Cite the closed answer (sheet + detail) instead of the RFI, or put the RFI in Pending Items. Delta: 0.
- **BE-51** - Metal reveal in LF sold as 'piece' with Pieces = ROUNDUP(LF). Source: Material Summary R31 H31 '=ROUNDUP(F31,0)'. Fix: Pieces = ROUNDUP(F31/Inputs!B18) (10 ft sticks) or sell by LF. Delta: 100 'pieces' -> 10 sticks of 10 ft.
- **BE-55** - Internal process codes and schema keys in client text. Source: GAP1-GAP19 (R12, R15, R20, R23, R28, R30-R33, R35, R39), 'misc_items', 'frp_info', 'pvc_trim_items' (R49), 'readings A and B' (ALC-08), 'skill standing rule U8' (ALC-19), 'rule 58.7' (ALC-20). Fix: Replace with plain descriptions and sheet/detail citations. Delta: 0.
- **BE-101** - Pending item whose option (A) claims a printed requirement that the set does not print. Source: RFI-ACC-deflection-clips vs S01.01 / A15.04 / M/A02.01. Fix: See BE-12. Delta: 0.
- **BE-102** - N/SHEET citations to sheets that do not exist (truncated) and wall IDs as sheet. Source: 'C/A12', 'A/A12', 'B/A10', 'P/A07', 'N/S03', 'A/S02', 'I06/I05' (R15) in Material Summary N/SHEET fields; SHEET_MAP has only A12.01/A12.02, A10.01-A10.08, A07.01/02/04, S03.01/S03.02, S02.01. Fix: Full sheet numbers in every N/SHEET (e.g. C/A12.01, B/A10.03). Delta: 0.
- **BE-105** - Printed products replaced by defaults. Source: B/A10.03 framing sizes (R17); F/A12.01 + S01.01 B.7 18 GA backing track and E/A12.01 plate (R35). Fix: See BE-14 and BE-15. Delta: see BE-14 / BE-15.
- **BE-VS-03** - Coverage not at 0 GAP. Source: M/S01.01 splices; B/A10.03 blocking runs. Fix: See BE-16 / BE-18. Delta: +40 LF splice studs; approx +23.25 LF blocking.
- **BE-VS-04** - Beauty-valance soffit zone counted in the Room 4 ceiling and again as its own ceiling. Source: canon ceiling ROOM 4 BEAUTY 3 area_op '24.444 x 48.333 - CW closets 18.71 - cashwrap soffit 30.91' (valance not deducted) + 'BEAUTY CABINET VALANCE' 136.6 SF (Material Summary R23); B/A10.03 ceiling ends at the valance. Fix: Deduct 136.6 SF from the Room 4 ceiling and its grid/hangers. Delta: -136.6 SF 5/8" Type X (R23 18,111.16 -> 17,974.56); grid / hangers / compound pro rata in that 136.6 SF.

## Other observations (not library FAILs)

- Display window ceilings: canon height 11.167 but hanger drop computed with 10.167 (approx +20 LF of wire); vestibule area_op prints 3.556 x 13.49 = 47.964 while 25.9 SF is carried.
- Bottom track carried across openings (R7, 52.7 LF): bottom track is cut out at door openings; only the top track runs across.
- Same restrooms named RESTROOM 1/2 and RESTROOM W/E.
- Bridging carried on column wraps CW1-CW4 and piers SP1/SP2 (R18) with no detail calling it.
- Methods: deltas computed by scripts in _work/ (an1.py, an3.py) from canon faces/lengths; PDF crops in _work/img/.
