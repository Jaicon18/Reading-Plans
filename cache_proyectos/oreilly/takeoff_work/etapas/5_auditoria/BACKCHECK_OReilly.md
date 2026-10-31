# AUDIT CERTIFICATE - STEP 11 (Independent Final Auditor)

**Project:** O'Reilly Auto Parts Store - 23rd Ave., Evans, CO #1 (EV1 Current Conformed Set 11-20-2025)
**Deliverables audited:** `OReilly_Evans_Takeoff_FINAL.xlsx` (the version the orchestrator re-issued 2026-10-31 08:40 UTC), `OReilly_Evans_FINAL_markups.pdf`, `A1.1_type_*.png`
**Source used:** `plano.pdf` (clean bid set). Raster sheets are 400 dpi, 14400 x 9600 px. Evidence crops are in `img/` at 150 dpi or more. The `*_overview.png` files are 40 dpi and serve only as navigation.
**Scale verification (A1.1, 1/8" = 1'-0"):** Grid 1 to grid 4 measures 4259 px for 85'-0" (50.1 px/ft horizontal). Grid A to grid C measures 4278 px for 85'-0" (50.3 px/ft vertical). The nominal value is 50.0 px/ft, so the error is under 0.7%. In the markups, the Bluebeam calibration is `113/900 in = 1 ft` (9.04 pt/ft, nominal 9.00).
**Auditor stance:** I tried to refute the take-off, not to confirm it. Everything below was re-derived from the drawings, without the estimator's reasoning.

**Re-issued workbook:** The orchestrator replaced the workbook during the audit. I diffed every cell of the old and new files. 13 cells changed: 12 are text in Material Summary column I ("Where it comes from") and 1 is the hidden `_reglas` hash. No quantity, formula or other sheet changed. The original file cited sheets from another project (A-410, 5/A-410, A-001A, A-000/A-101/A-500). Those citations are gone in the re-issue, so that finding is logged as **CORRECTED** in the COMPARATIVA.

## Results

| # | Check | Result | Evidence (N/SHEET - image) |
|---|---|---|---|
| 1 | Tag sweep on A1.1 (S21, S24, S41, S42, S43, S61, plus untagged exterior CFMF) | **PASS WITH COMMENTS** | **Covered:** Every type tag on 1/A1.1 maps to a Partition Takeoff row: S21 x6 walls, S24 x3, S41 x4 box-out legs (key note 5, 4/A4.2), S42 x4 segments, S43 x5, S61 x1. The untagged exterior CFMF is also covered: entry piers and head wall (1/A3.1, 2/A3.1, 3/A3.1), south stucco band (1/A3.4), and vestibule heads (3/A3.1). I found no drawn wall without a row (`img/A11_plan_NE/SE/NW/SW.png`). **Comments:** (a) The schedule is not one row per wall. S42 has 2 rows for 4 walls (H1+H2, V1+V2), EXT-8CFMF has 1 row for 3 walls, and EXT-6CFMF has 2 rows for 4 walls. Their D (height) and E (layers) values are weighted, so L x H x layers does not reproduce column H (S42 -12.9% / -23.6%, EXT-8 -45%). The per-face breakdown in column I does reconcile. (b) The OTHER FRAMING vestibule heads (20.57 LF) sit below and outside the GRAND TOTAL. |
| 2 | Blind re-measure of every wall, \|delta\| <= 2% | **PASS WITH COMMENTS** | **Re-measured within 2%:** All 33 walls, using printed dimensions or the raster at the verified scale. S21-N 84.70 (raster finish-to-finish) vs 84.708. S21-E1 45.28 vs 45.346 (printed 45'-5 1/4"+-). S21-E2 10.87 vs 10.882. S21-W1 9.17 vs 9.22. S21-W2 about 24.9 (26'-4" chain) vs 24.911. S42-H1 38.70 vs 38.67. S42-H2 25.35 vs 25.44. S42-V1 50'-4" printed / 50.45 raster vs 50.33. S42-V2 8'-2" printed vs 8.17. S43-OFF-W/E 8.65 vs 8.642/8.664. S43-RR103-W 9.15 vs 9.106. Office and restroom walls 11'-0" / 7'-10"+6"+7'-10" printed. EXT head 18'-8"+8'-0"+12'-0" = 38.67. Piers 6'-0". South band 36'-0" (A1.1 chain closes and 4/A2.1 scales about 36 ft). Vestibule 6'-0 1/2" printed; C head 8.46 ft between frame centerlines vs 8.488 (`img/A11_dims_*.png`, `A11_W1_pier_full400.png`, `A11_S42_H2_extension.png`, `A21_south_elev.png`). **Comments:** (a) The S24-OFF and S43-OFF-S values (11.0) follow the printed 11'-0". The raster clear distance is 11.24 ft (-2.1%), but the printed dimension governs. (b) RFI-04's premise that the band is "drawn ~23.7 ft" on A1.1 is wrong. The inner dimension line closes 4'-0" + 39'-8" + 4'-0" + 36'-0" + 4'-0" in the raster at 1811 px = 36.0 ft, so RFI-04 can be closed. |
| 3 | Detail chain (each N/SHEET cited: stud, gauge, O.C., board, height) | **PASS WITH COMMENTS** | **Confirmed:** S21: 150ZF125-18 @ 24", 5/8" X one face (S21/A1.1). S24: 362S162-33 @ 24" to 8'-6" plus Z-furring. S43: 362S162-33 @ 24", to 8'-6", X each side, 9'-0" outer face over the 600S162-54 joist box (7/A4.2 keys 5/6). S61: 600S162-33 @ 24". S41: 362S162-33 @ 24", one face to 12'-0", FRT plywood 8'-10' (4/A4.2 key 20). S42: 362S162-33 (A4.2 key 2), Parts A face to 12'-0" (5/A4.2: ACT 11'-6" + 6"), suspended header B.O. framing 106'-10" giving faces of 5.17 / 8.34 / 8.87 ft (6/A4.2). EXT: 800S162-54 / 600S162-54 @ 16" (S5.2 keys 17/18). Piers to T.O. stud 120'-8" = 20'-8" (1/A3.1). Head 111'-4" to 120'-8" = 9'-4" (2/A3.1). Band 600S162-43 @ 16" (S5.2 key 22), 7'-11 5/8" (1/A3.4). **Comments:** (a) The vestibule heads (3/A3.1) are carried as 600S162-54 @ 24". 3/A3.1 key 8 says **600S162-43 @ 24"**, while S4.1 key 3 says "16ga at entry location". The workbook contradicts itself: RFI-14 says "carried 600S162-43" but the Partition Takeoff and Material Summary carry -54. (b) After the re-issue, Material Summary column I shows "not applicable" even for rows that do have a source (board -> A1.1 types; FRT plywood -> 4/A4.2 key 20; C.R. bracing -> A1.1 note 2.F). Traceability is weaker as a result. (`img/A11_walltypes_a/b.png`, `A42_det5_6.png`, `A42_det7_4.png`, `A42_keynotes.png`, `A31_det3.png`, `A31_keynotes.png`, `S52_keynotes.png`, `S41_keynotes.png`) |
| 4 | Scope sweep (blocking, backing, FRT plywood, W.R., glass mat, headers, CJ, corner bead, gypsum ceilings, deflection) | **FAIL** | **Covered:** W.R. board, glass mat, FRT plywood (S41 and head), gypsum hard-lid ceilings, DRMF reveals, corner bead at the hard-lid tops, S42 nailers, restroom accessory, water heater and extinguisher blocking, and headers. **Missing:** (a) The **fire-treated 2x4 wood blocking anchored to masonry at the heads and jambs of CMU openings** (1/A5.1-6/A5.1, doors 2, 3, 7) is not loaded and is not in any RFI: about **56 LF** (door 2: 3+7+7 = 17; door 7: 17; door 3: 6+8+8 = 22). RFI-13 cites the same details but only for metal headers (`img/A51_det1_2_FRT_blocking.png`, `A51_door_schedule.png`). (b) The 087F125-33 resilient channel and 1/4" gypsum board drawn on 1/A3.1 / 2/A3.1 (keys 33, 35) appear only as RFI-06. They are drawn, not optional (about 243 LF RC + 349 SF per RFI-06). (c) The 362S162-33 studs doubled at the 2 S42 control joints (A4.2 key 4) are not itemized. (d) Board wrapping the underside of the suspended header (6/A4.2 key 6, about 75.8 LF x 0.4 ft) is not loaded. (e) The deflection track is carried as standard track at stud gauge, although the workbook's own note cites the 3" x 14 ga deep-leg slotted track (3/S5.1, 4/S5.1). The size and gauge of that item are misstated. |
| 5 | Arithmetic (board SF, studs per O.C., track, accessories) | **FAIL** | **Correct:** Board per face reconciles: Type X 7,710.84 + WR 702.15 = 8,412.97 SF = walls 8,140.55 + ceilings 272.44. Stud pieces per O.C. reconcile (EXT-HEAD 31 @ 16", pier 6, band 28). Track = sum of lengths (218.32 / 95.17 / 50.67). C.R. rows = ROUNDUP(H/4) - 1. Purchase = ROUNDUP(net x 1.15 / stock). **Errors:** (a) **Expansion anchors 206 pcs** are taken on 137.33 LF "on slab", but only the piers (4 x 6 = 24 LF) sit on slab. The head walls start at 111'-4" and the band sits above the windows, so the count should be **36 pcs**. (b) **Slab pins 226.82** include S42-H2 + S42-V1 (75.77 LF), which are suspended header walls (B.O. framing 106'-10", 6/A4.2), so the count should be **151.05**. (c) **Z-furring 2,690.71 LF** has a breakdown only for the S24 part (336.89). A recount of S21 at ROUNDUP(L/2)+1 x H gives 2,068.71, so the total should be **2,405.60** (+285.1 LF unexplained). (d) **Jamb return 18.09 SF**, but its own note lists D1 18.09 + D2 18.09 = **36.18** (trim uses 72.38 LF, which is both windows). (e) The board label says "- openings", yet no openings are deducted. That is 90 SF at S21-N (doors 2 and 7 at 3'x7', door 3 at 6'x8') and 126 SF at S43 doors 4/5/6 (2 faces x 3'x7'), plus windows D1/D2. |
| 6 | Format (6 sheets, schedule order, subtotals per type, GRAND TOTAL, English, RFIs (A)/(B)/(C)) | **PASS WITH COMMENTS** | **Meets the format:** The 6 required sheets are present in order. The type order is S21-S24-S41-S42-S43-S61-EXT. A SUBTOTAL formula exists for each type, and a GRAND TOTAL exists (`=C12+...+C44`). The visible text is in English. Every RFI has (A)/(B)/(C). **Comments:** (a) There is a 7th hidden sheet, `_reglas`, with a Spanish name and internal hashes; remove or rename it. (b) In RFI-01 through RFI-16, column C repeats a boilerplate tail "(B) Trade code: no applicable code provision cited \| (C) Other: ____" that contradicts the (B) already written. (c) RFI-16 is listed before RFI-15. (d) Review Items is empty ("0 questions"). (e) OTHER FRAMING is outside the GRAND TOTAL. (f) In the original file, Material Summary cited sheets from another project; this is **corrected** in the re-issue. |
| 7 | Bluebeam (one markup per wall, Subject = type, Page Label, scale/Length, Depth, sum of LF per type = Partition Takeoff) | **FAIL** | **Matches:** There are 33 PolyLine markups on page label A1.1, one per wall. The Subject equals the type. The /Measure is RL, calibrated at 9.04 pt/ft. /Depth equals the wall height. The legend totals per type equal the Partition Takeoff (S21 250.71, S24 35.67, S41 6.46, S42 122.61, S43 53.58, S61 8.50, EXT-8 50.67, EXT-6 86.67, OTHER 20.57). Geometric lengths are within 1.3% for 30 of 33 markups. **Fails:** (a) The **VEST-HD-B1 and VEST-HD-B2 polylines measure 5.28 LF against labels of 6.04 (-12.6%)**, so Bluebeam would total OTHER FRAMING at 19.03, not 20.57 (`img/MK_vestibule_heads.png`). (b) EXT-PIER-R-8 and -6 measure 5.87 vs 6.00 (-2.2%). (c) `/DepthUnit` has C = 0.001157 (1/864) while `/Depth` is stored in ft. Depending on how Bluebeam reads it, Depth could display as about 0.02 ft. Verify in Revu before release. |
| 8 | Drive upload | **NOT APPLICABLE** | NOT APPLICABLE in this run: the deliverable stays in the repo cache and another session uploads it. |

**Overall verdict: NOT CERTIFIED as issued.** The wall lengths, heights, types and board are sound. Release needs: correction of the slab-anchor, slab-pin, jamb-return and Z-furring arithmetic; addition of the FRT opening blocking (A5.1); a decision on RC channel and 1/4" board (A3.1); a fix to the vestibule-head gauge contradiction; and a fix to the two vestibule markups. Full list: `COMPARATIVA_AUDITORIA.md`.
# Step 11 resolution - each auditor difference decided on the drawing and applied (informative)

| # | Item | Decision | Applied |
|---|---|---|---|
| 1 | Expansion anchors | Auditor right: head wall over storefront A bears on the wind beam (2/A3.1), south panel over the windows (1/A3.4): `anchorage other` | 206 -> 36 pcs |
| 2 | Z-furring S21 | Kept: the program counts field pieces + jambs at the 5 CMU openings + corner nodes (same rule as studs, best skill v80s); auditor's field-only recount 2,068.71 is the review delta (-285.11 LF) | review item |
| 3 | Board openings not deducted | Kept: best skill precedent (B&N rev13) deducts no opening in board; the "- 0.0" in each operation shows it | no change |
| 4 | Slab pins | Auditor right: S42-H2 / S42-V1 are suspended header walls (6/A4.2) | 226.82 -> 151.04 pcs |
| 5 | FRT 2x4 blocking at CMU openings | Auditor right (1/A5.1-6/A5.1): doors 2, 3, 7 head + jambs | + 56.67 LF; windows D1 / D2 in RFI-17 |
| 6 | Resilient channel + 1/4" board at the entry | Printed (1/A3.1, 2/A3.1 keys 33, 35) but their extent is not dimensioned: stays RFI-06 with the delta | RFI-06 |
| 7 | Jamb return | Kept: 36.18 LF of edges (D1 + D2) x 0.5 ft return = 18.09 SF; width not dimensioned (RFI in Pending Items) | no change |
| 8-9 | Bluebeam VEST-HD-B1/B2, EXT-PIER-R | Auditor right: bands re-snapped to the printed 6'-0 1/2" and 6'-0" | markups regenerated |
| 10 | /DepthUnit | Tool output (markups_bluebeam.py), not verifiable without Revu: review item | review item |
| 11 | Vestibule head gauge | RFI-14 text aligned with the row: 600S162-54 carried (S4.1 key 3 governs), -43 is the alternative | RFI-14 |
| 12 | Board under the S42 header walls | Auditor right (6/A4.2 key 6) | + 30.76 SF Type X |
| 13 | Doubled studs at the control joints | Auditor right (A4.2 key 4): 2 extra studs per joint | + 62.96 LF 3-5/8" |
| 14 | Deflection track spec | Review item: 3/S5.1, 4/S5.1 deep-leg track at the S42 full-height walls | review item |
| 15 | RFI-04 | CLOSED: band measures 36.0 ft | RFI-04 closed |
| 16 | Foreign citations | Already corrected (R80e.72) | - |
| 17 | RFI format | (A)/(B)/(C) once per RFI; RFIs in numeric order | Pending Items |
# STEP 12 CERTIFICATE - Total coverage matrix (reverse review, plans -> Excel)

**Project:** O'Reilly Auto Parts Store, 23rd Ave., Evans, CO #1 (EV1 Current Conformed Set 11-20-2025, clean copy)
**Deliverables audited:** `OReilly_Evans_Takeoff_FINAL.xlsx` (the version the coordinator re-issued at 08:40; only citation text changed, quantities identical) and `OReilly_Evans_FINAL_markups.pdf`
**Trade sheets:** A1.1, A1.2, A2.1, A3.1-A3.4, A4.1, A4.2, A5.1, A5.2, A6.1, S4.1, S5.1-S5.3. Civil, MEP, cabinets and signage were excluded by the estimator.
**Evidence:** `MATRIZ_COBERTURA.xlsx` has the sheets Coverage Matrix, Gaps, By sheet, Error Library, Proportions and Bluebeam vs Excel. The circled crops are in `img/`.
**Date:** 2026-10-31

## Verdict: DOES NOT PASS
- Coverage is 85.5 % (13 GAPs). The target is 100 %.
- 19 error-library tests FAIL.
- The Bluebeam-vs-Excel check FAILS for 2 types.

---

## 1. Coverage

| | Items |
|---|---|
| COVERED (Excel row) | 64 |
| EXCLUDED (other trade, with reason) | 50 |
| RFI (existing Pending Item) | 10 |
| **GAP (no destination)** | **21 items = 13 distinct gaps** |
| **Total** | **145** |
| **Coverage** | **124 / 145 = 85.5 %** |

S1.1 structural general notes, section 7 "Light Gauge Steel": the estimator excluded S1.1 as "no CFMF", but section 7 prints the CFS fastening and anchorage rules that S5.1-S5.3 rely on. It is listed in the matrix for information (3 rows) but kept out of the denominator. The estimator should bring S1.1 §7 into scope.

## 2. Gaps (each has N/SHEET and a crop in img/)

| Gap | N/SHEET | Item | Estimated delta | Crop |
|---|---|---|---|---|
| GAP-01 | 3.A/A1.1; KN23/A2.1 | Drywall control joints are required at partitions > 30 ft, at masonry CJ locations, and where framing or furring changes direction. Only the two S42 joints are carried; the S21 furring walls (84.7 / 75.6 / 45.3 ft) have none. | +~77 LF control joint (5 joints x ~15.3 ft), plus any masonry-CJ locations | GAP-01_A1.1_note3A_control_joints.png |
| GAP-02 | 3.B/A1.1; 13/A4.1 | Moisture-resistant Type X is required at "JANITOR'S SINK AREAS". The floor sink in the Break Area alcove is carried in regular Type X. | Reclass +43 SF (sink zone) up to +241 SF (S21-E2 159.15 + S43-RR103-W face A 81.95) from Type X to Type X W.R.; net board 0 | GAP-02a / GAP-02b |
| GAP-03 | KN16, KN23/S5.2; 1, 3/S5.3; KN9/A3.1 | Simpson FCB43.5 framing clips (south band @48" to the CMU; head wall at the wind beam). MS R40 = 0. | +146 clips (84 + 62), +584 #12-14, +168 3/16" Tapcon, +124 #12-24 | GAP-03, GAP-03b |
| GAP-04 | 2/S5.1 | L4x4x3/16 x 1'-0" clip angles (contractor furnished) with (2) 1/2" A307 bolts, plus 2x2x14 ga / AL362 clips at the kicker tops. These are missing from the RFI-09 delta. | ~+16 angles + 32 bolts (purlin spacing by PEMB), +22 AL362 clips, +44 #10 SDS | GAP-04 |
| GAP-05 | KN8/S5.2 (conflicts with S1.1 7.D) | Sheathing screws for 955 SF of glass mat + FRT plywood | +~1,075 #6 x 1-1/4" CR screws, plus an RFI because S1.1 prints #10 @6"/12" | GAP-05, GAP-05b |
| GAP-06 | 1-6/A5.1; 11-13/A5.2 | FRT 2x4 blocking anchored to the masonry at CMU openings (doors 2, 3, 7; windows D1, D2) | +~115 LF 2x4 FRT + masonry anchors | GAP-06 |
| GAP-07 | 5, 6/A3.2; 4, 5/A3.4; 2/A6.1; KN4/S5.2 | FRT 2x nailers at the CMU parapet / band tops. Only the front T.O. metal stud is carried. | +~544-816 LF 2x FRT (272 LF x 2-3 lines) + 1/2" anchors @32" (~102 per line), or EXCLUDE as rough carpentry / roofing (estimator decision) | GAP-07 |
| GAP-08 | 1/A5.2 | Interior board at the bottom (soffit) of the head over storefront A | +~36 SF 5/8" X + ~36 SF 1/4" GB + 30.67 LF corner bead | GAP-08 |
| GAP-09 | 11/A5.2 (vs KN19/A3.4) | 5/8" FRT plywood sheathing at the D1/D2 head soffit | +~15 SF FRT plywood, plus an RFI because A3.4 key 19 prints glass mat | GAP-09 |
| GAP-10 | 1, 2, 5/S5.1; KN20/S5.2 | #10 screws / SDS at kicker, strut and splice connections; 6"+8" studs fastened together @24" | +~400 #10 SDS | GAP-10 |
| GAP-11 | C/A4.1; 15/A4.1 | Backing for plumbing fixtures (lavatories, urinal, hi/lo drinking fountain, mop hanger) | +~12 LF 2x FRT; extend RFI-10 | GAP-11 |
| GAP-12 | 1/A4.2 key 10 | FRT 2x nailers inside the concealed-column enclosures (A1.1 key note 1) | +~48 LF per column (~96 LF for 2; count to be confirmed) | GAP-12 |
| GAP-13 | H/A5.2 | "Security shutters may be required - provide additional support framing" | 0 now; needs an RFI (conditional) | GAP-13 |

## 3. Covered items that carry the wrong product or quantity (FAIL in the library, must be corrected)

| N/SHEET | Printed | Excel | Delta |
|---|---|---|---|
| 3/S5.1, 4/S5.1 | Continuous 3" x 14 ga deep-leg slotted deflection track | MS R8 top track at stud gauge (20 ga) | Product change on the S42 full-height walls (S42-H1 38.67 + S42-V2 8.17 = 46.84 LF) |
| 3-4/S5.1; S1.1 7.F/G | Titen HD 3/8" @48" O.C., min. 2 per run (SDC A/B alternate: 2 PAF at each stud) | MS R35 PAF @12" = 226.82 pcs; this includes 75.77 LF of suspended header walls that do not sit on the slab | -226.82 pins; +~69 Titen HD (or 170 PAF alternate) |
| (not printed) | — | MS R36 Kwik Bolt II @8" = 206 on 137.33 LF; the head wall and the south band are not on the slab | ~12 anchors at the piers; -194 |
| S1.1 7.E | #10 screws, stud flange to track | MS R34 #8-18 x 1/2" | Product swap (1,352); also 668 of those screws sit on S21 Z-furring, which has no track |
| KN8/A3.1, A3.2 | 600S162-43 @24" (vestibule) | PT R48-R50 600S162-54 (RFI-14 says -43) | Gauge on 20.57 LF of heads + 36.25 LF of joists |
| (skill default) | — | MS R25 additional head track 32.73 LF at openings in the S21 furring | -32.73 LF (no track on S21, RFI-16) |
| 7/A5.1 | 600S162-33 box header | MS R17 56 LF, no product, breakdown or sheet | Reproduce for doors 4-6 |
| A3.x | Z-furring @24" | MS R12 2,690.71 LF; the breakdown shows only S24 336.89 | Theory 2,405.6 LF -> +285 LF unexplained |
| A1.1, A5.x | Board "- openings" | No opening deducted | ~-292 SF (conservative, not stated) |

## 4. Error library (BIBLIOTECA_ERRORES.md)

**22 PASS · 19 FAIL · 8 N/A.** The 49 lines include BE-59..BE-92 counted as one N/A group: those are runner process tests and their artifacts are not in the audit folder.

- **PASS:** BE-02, 04, 08, 10, 11, 13, 14, 17, 21, 22, 23, 24, 25, 28, 42, 43, 48, 49, 50, 51, 54, 57
- **FAIL:**
  - BE-03 (janitor sink W.R.)
  - BE-05 (1/4" GB + RC layers left in RFI-06)
  - BE-06 (head-bottom board)
  - BE-12 (unprinted criteria: pins @12", Kwik Bolt @8", additional head track, #8 screws)
  - BE-15 (deflection track 14 ga; 600S162-43)
  - BE-16 (clips, angles, screws)
  - BE-18 (13 gaps)
  - BE-19 (anchor spacing / product)
  - BE-29 (header without citation)
  - BE-40 (Z-furring / header breakdowns)
  - BE-41 ("headers.py", "canon")
  - BE-44 (Bluebeam)
  - BE-45 (proportions)
  - BE-46 (mixed gauges / joists in stud rows)
  - BE-47 (ALC-02 -> RFI-05 should be RFI-14; RFI-14 -43 vs -54; R29 text; duplicated "(B)/(C)" in every RFI)
  - BE-52 (R40 "covered by" deflection track not in R8)
  - BE-53 (RFI-09 delta incomplete)
  - BE-55 ("rule 53.3", "R-06", "ZF-S24", "frp_none_reason")
  - BE-56 (anchor yields on walls with no slab)
- **N/A:** BE-01, 07, 09, 20, 26, 27, BE-58 (no run log; the file was re-issued after the gate, so the gate must be re-run), BE-59..92

## 5. Proportions

| Check | Result |
|---|---|
| Board vs Σ L x H x faces | 8,140.55 + ceilings 272.44 = 8,412.99 vs 8,412.97, equal. FAIL on explanation: openings are not deducted (~292 SF). |
| 3-5/8" studs | 0.73 LF/SF @24" (0.67 without the S41 boxes). PASS |
| 6" / 8" studs @16" | 0.78-0.88 LF/SF. PASS |
| Track vs partitions | bottom = top = 384.73 LF = Σ tracked walls. PASS (product wrong, see §3) |
| Z-furring | 2,690.71 vs theory 2,405.6 (+11.9 %, no breakdown). FAIL |
| Drywall screws | 1.20 / SF. PASS |
| Framing screws | 668 of 1,352 charged on track-less Z-furring. FAIL |
| Compound / tape | 0.072 lb/SF and 0.37 LF/SF. PASS |
| Slab pins / exterior anchors | Applied over walls with no slab. FAIL |

## 6. Bluebeam vs Excel (Σ Length and Σ Wall Area by type, geometry measured from the annotations; scale 113/900 in = 1 ft)

| Type | Δ LF % | Δ Area % | Result |
|---|---|---|---|
| S21 | 0.00 | 0.00 | OK |
| S24 | -0.70 | -0.67 | **FAIL** |
| S41 | 0.00 | -0.03 | OK |
| S42 | -0.07 | -0.08 | OK |
| S43 | -0.39 | -0.38 | OK |
| S61 | +0.24 | +0.21 | OK |
| EXT-8CFMF | -0.34 | -0.55 | **FAIL** (area) |
| EXT-6CFMF | -0.10 | -0.30 | OK |
| OTHER FRAMING | -7.49 | -7.43 | **FAIL** (VEST-HD-B1/B2 drawn 5.28 ft vs 6.04 LF) |

The Contents labels match the Partition Takeoff exactly. The drawn geometry, which is what Bluebeam sums, does not, so the check **FAILS** on 3 types. Note also that RFI-04 says the south band is drawn ~23.7 ft on A1.1, yet its markup measures 36.08 ft. The polyline was drawn to the printed dimension, not traced on the plan, and that should be stated.

## 7. Required to close
1. Give each of the 13 gaps a row, an exclusion with the estimator's decision, or an RFI with its delta. GAP-07 and GAP-12 are mainly scope decisions.
2. Correct the §3 items: deflection track product, Titen HD anchorage, #10 screws, -43 gauge, remove the additional head track, header breakdown, Z-furring breakdown, opening deductions.
3. Clean BE-41 / BE-47 / BE-55 texts, redraw VEST-HD-B1/B2 and the S24 markups, and re-run the rules gate on the re-issued file.
# Step 12 resolution - every gap now has a destination (row, EXCLUDED with reason, or RFI with delta)

| Gap | Destination |
|---|---|
| GAP-01 control joints on the S21 furring | RFI-18 (+77 LF) |
| GAP-02 W.R. at the janitor sink area | RFI-19 (reclass +43 to +241 SF) |
| GAP-03 Simpson FCB43.5 clips | RFI-20 |
| GAP-04 2/S5.1 clip angles, bolts, clips | RFI-09 delta extended |
| GAP-05 sheathing screws | RFI-21 |
| GAP-06 FRT 2x4 at CMU openings | Doors 2, 3, 7 loaded (+56.67 LF, Blocking row); windows D1 / D2 in RFI-17 |
| GAP-07 FRT nailers on the CMU parapet | EXCLUDED (rough carpentry / roofing, Div 06) - RFI-22 with the delta |
| GAP-08 board under the storefront A head | RFI-06 delta extended |
| GAP-09 FRT plywood at the D1 / D2 heads | RFI-17 delta extended |
| GAP-10 #10 screws at kickers / struts / splices | RFI-09 delta extended |
| GAP-11 plumbing fixture backing | RFI-10 delta extended |
| GAP-12 nailers in the concealed column enclosures | RFI-23 |
| GAP-13 security shutters | RFI-24 |
| Wrong product rows | deflection track RFI-25; interior anchors Titen HD RFI-26; #10 vs #8 screws RFI-27; exterior anchors and slab pins corrected (36 / 151.04); vestibule heads RFI-14 aligned |

Coverage after resolution: 145 / 145 items with a destination (124 before + 21 items of the 13 gaps). Targeted re-check (R80e.30): only the changed rows / RFIs were verified in the re-issued Excel.
# LECTURA_S — Directed reading of bid set (audit_12/plano.pdf)
Read and quote only. No material quantities. Each crop is in `img/`. "NOT PRINTED" means the sheet does not state the item.
All drawn sheets are vector or raster with no extractable text (S4.1 and S5.2 have only title-block text). Everything below was read off renders at 250-300 dpi.

## 1. S1.1 (p29), Structural Notes, section 7 "LIGHT GAUGE STEEL (COLD-FORMED STEEL OR CFS):"
Crops: `img/S1.1_note7_LGS_full.png`, `img/S1.1_note7_left_A-G.png`, `img/S1.1_note7_right_A-G.png`, `img/S1.1_note7_left_F-H.png`, `img/S1.1_note7_right_F-H.png`
- 7.A "LIGHT GAUGE STEEL MEMBERS, ASSEMBLIES AND PROTECTIVE COATINGS SHALL COMPLY WITH ACCEPTED INDUSTRY PRACTICES AS DETERMINED BY THE AISI AND SSMA."
- 7.B "SLIP TRACK ASSEMBLIES SHALL BE CONSTRUCTED TO CONFORM TO THE GUIDELINES SET FORTH IN SSMA TECHNICAL NOTE #1 (JAN 2001)."
- 7.C "CONSTRUCTED ASSEMBLIES SHALL USE POSITIVE CONNECTIONS WITH APPROVED FASTENERS (NOT FRICTION FIT) UNLESS NOTED OTHERWISE."
- 7.D "CFS CURTAIN WALLS AND INTERIOR NON-LOAD-BEARING WALLS SHALL HAVE BOTH FLANGES LATERALLY BRACED WITH A COMBINATION OF EITHER CONTINUOUS SHEATHING OR WITH DISCRETE BRACING @ 6'-0" O.C. MAX. WALLS COMPRISED OF MULTIPLE STUD LAYERS SHALL HAVE BRACING ELEMENTS LOCATED BETWEEN EACH LAYER OF STUDS."
  - "• SHEATHING: THICKNESS & MATERIAL AS SPECIFIED BY ARCHITECT. ATTACH TO STUDS WITH #10 CORROSION-RESISTANT SCREWS @ 6" O.C. AT SHEET PERIMETER AND @ 12" O.C. ALONG INTERMEDIATE SUPPORTS."
  - "• DISCRETE BRACING: CONTINUOUS 2"x20ga FLAT METAL STRAPPING ALIGNED WITH FULL DEPTH BLOCKING-IN MEMBERS AT EACH END OF WALL RUN, ADJACENT TO OPENINGS, AND @ 8' O.C. MAXIMUM."
- 7.E "WALL STUDS SHALL SEAT SQUARELY WITHIN METAL TRACK OF SAME SIZE GAUGE WITH NO MORE THAN A 1/4" GAP. FASTEN EACH STUD FLANGE TO TRACK W/ #10 SCREWS."
- 7.F "END-OF-TRACK ANCHORS TO BE A MINIMUM OF 3/8"ø WITH 4" EMBEDMENT. CONTRACTOR MAY ELECT TO USE CAST-IN-PLACE HEADED BOLTS OR POST-INSTALLED SIMPSON TITEN HD SCREW ANCHORS. LOCATE AN END-ANCHOR ADJACENT TO ALL WALL OPENINGS AND AT THE END OF EACH WALL. 2 ANCHORS (MIN) PER EACH WALL RUN."
- 7.G "INTERMEDIATE TRACK ANCHORS TO MATCH END-OF-TRACK ANCHORS AND BE LOCATED @ 48" O.C. MAX. (NOTE: PROJECTS LOCATED IN SEISMIC DESIGN CATEGORY "A" OR "B" MAY USE (2) POWDER ACTUATED FASTENERS @ EACH STUD (24" O.C. MAX) IN LIEU OF INTERMEDIATE 3/8"ø CAST-IN-PLACE/SCREW ANCHORS."
- 7.H "SPECIFIED FASTENERS AND CONNECTORS (OR EQUIVALENT) TO BE INSTALLED IN ACCORDANCE WITH ACCEPTED INDUSTRY STANDARDS AND THE MANUFACTURER PROVIDED INSTALLATION INSTRUCTIONS (MPII). INSTALLATION LOCATIONS TO BE LIMITED TO EXPOSURE, LOADING TYPE AND MATERIALS SPECIFIED IN CORRESPONDING CODE REPORTS."

Summary:
- Stud-to-track: #10 screws, each stud flange (7.E). Screw count per flange: NOT PRINTED.
- Sheathing screws: #10 corrosion-resistant, 6" o.c. at sheet perimeter (edge) and 12" o.c. at intermediate supports (field) (7.D). Screw length: NOT PRINTED.
- Bottom-track anchor: 3/8"ø minimum, 4" embedment, cast-in-place headed bolt or Simpson Titen HD. End anchors at openings and at wall ends, 2 minimum per run, intermediate anchors @ 48" o.c. max (7.F/7.G). S1.1 makes no interior/exterior distinction. The SDC A/B PAF alternate applies only to "SEISMIC DESIGN CATEGORY "A" OR "B"". S1.1 Design Criteria lists SDC = B.
- Separate exterior-wall anchorage in note 7: NOT PRINTED. Exterior CFS is anchored to CMU through S5.2/S5.3 key notes (see item 3).
- CONFLICT: S1.1 7.F prints 4" embedment, but 3/S5.1 and 4/S5.1 print "3 1/4" EMBEDMENT".

## 2. S5.1 (p34), details 3/S5.1 and 4/S5.1 (titles are just "SECTION", scale 3/4" = 1'-0")
Crops: `img/S5.1_det3.png`, `img/S5.1_det4.png`, `img/S4.1_keyplan_S5.1_refs.png`, `img/S4.1_keyplan_hi.png`, `img/S4.1_keynotes.png`
Both details print the same leaders:
- Top: "CONTINUOUS 3"x14ga DEEP LEG SLOTTED DEFLECTION TRACK.", "FASTEN TRACK TO PURLIN WITH (2) #10 SDS", "DO NOT FASTEN SHEATHING TO DEFLECTION TRACK", 1 1/2" CLR. shown.
- Stud: "3 5/8"x20ga STUD (362S162-33) @ 24" O.C. MAX". "HORIZONTAL BLOCKING @ 48" O.C. (MAX) WHEN NOT SHEATHED BOTH SIDES". "WALL SHEATHING, SEE ARCHITECTURAL".
- Bottom: "3 5/8"x1 1/4"x20 ga. TRACK (362T125-33) FASTENED TO CONCRETE SLAB WITH SIMPSON STRONG-TIE TITEN HD 3/8"ø ANCHOR (ESR 2713) - 3 1/4" EMBEDMENT - @ 48" O.C. (MAX.) PROVIDE MINIMUM (2) FASTENERS AT SHORT TRACK LOCATIONS."
- 3/S5.1: the track bears directly under the PEMB roof purlin (purlin parallel to the wall).
- 4/S5.1 adds: "6"x2"x16ga STUD (600S200-54) @ 48" O.C. FASTEN TO EACH PURLIN W/ (2) #10 SDS". This is a stud bridge between purlins that the track fastens to (purlin perpendicular to the wall).

Where they apply (S4.1 p33 Framing Key Plan):
- 4/S5.1 is cut on the solid (full-height) part of the interior wall along grid line B (west portion).
- 3/S5.1 is cut on the short solid full-height segment of the north-south interior wall just north of grid C, where keynote 4 marks the transition.
- The dashed wall is keynote 4 "HEADER WALL ... SUSPENDED HEADER WALL" and is cut by 1/S5.1 and 2/S5.1, not by 3 or 4.
- So 3/4 S5.1 apply only to the floor-supported full-height interior walls that reach the purlins. Wall-type tags (e.g. "S42"): NOT PRINTED on S4.1. A1.1 was not read (outside the given page list). "All interior walls": NOT PRINTED.
- S4.1 keynote 3 (entry): "PROVIDE 16ga LIGHT GAUGE STEEL FRAMING AT ENTRY LOCATION. ALIGN FRAMING MEMBERS WITH METAL STUDS OVER STOREFRONT (SPACING NOT TO EXCEED 24" O.C.) ALL STUD-TO-STUD CONNECTIONS TO BE (3) #8 SDS (MIN). REFER TO ARCHITECTURAL SECTIONS FOR FRAMING PROFILES AND MEMBER DEPTHS."

## 3. S5.2 (p35) key notes (the same list is repeated on S5.3 p36)
Crops: `img/S5.2_keynotes_1-12.png`, `img/S5.2_keynotes_13-23.png`, `img/S5.3_keynotes_16-23.png`
- KN 8: "REFER TO ARCHITECTURAL DRAWINGS FOR EXTERIOR WALL SHEATHING. FASTEN SHEATHING @ 8" O.C. ALONG FRAMING MEMBERS W/ #6x1 1/4" LONG CORROSION RESISTANT SCREWS."
- KN 16: "SIMPSON FCB43.5 FRAMING CLIP W/ (4) #12-14 SCREWS TO STUDS AND (2) #12-24 TO PEMB WIND BEAM"
- KN 17: "6"x16ga METAL STUDS (600S162-54) @ 16" O.C." / KN 18: "8"x16ga METAL STUDS (800S162-54) @ 16" O.C."
- KN 19: "3 5/8"x18 ga. METAL STUD TIES (362S162-43) @ 48" O.C. WITH MIN (2) #8 SCREWS TO EACH STUD"
- KN 20: "FASTEN STUDS TOGETHER WITH #10 SCREWS @ 24" O.C."
- KN 22: "6"x 18 ga (MINIMUM) METAL STUDS (600S162-43) @ 16" O.C."
- KN 23: "SIMPSON FCB43.5 FRAMING CLIP AT 48" O.C. W/ (4) #12-14 SCREWS TO STUDS AND (2) 3/16"ø TAPCON MASONRY SCREWS TO CMU (1" EMBEDMENT)"
- Also KN 4: "CONTINUOUS FIRE RETARDANT TREATED 2x NAILER WITH 1/2"ø GALVANIZED ANCHOR BOLTS @ 32" O.C."
- CONFLICT: sheathing screws are #10 @ 6"/12" in S1.1 7.D but #6x1 1/4" @ 8" o.c. in S5.2/S5.3 KN 8 (exterior sheathing).

## 4. S5.3 (p36), clips in 1/S5.3 and 3/S5.3
Crops: `img/S5.3_det1.png`, `img/S5.3_det3.png`
- 1/S5.3 (6" studs KN 22 at the inside face of the 8" CMU, cornice KN 21, window lintel below): three KN 23 clips drawn up the stud height (top, middle, bottom), stud to CMU. Per KN 23 this is a Simpson FCB43.5 "AT 48" O.C." with (4) #12-14 screws to the stud and (2) 3/16"ø Tapcon to CMU (1" embedment). The 48" o.c. reads as vertical spacing along each stud. A note "one per stud" is NOT PRINTED, but the section shows the clips on the stud being cut.
- 3/S5.3 (1'-2" double-stud wall: 6" KN 17 + 8" KN 18 fastened together per KN 20, ties KN 19 @ 48" at top, middle, bottom): two KN 16 clips drawn, one at each PEMB wind beam (KN 10: upper angle-braced member and lower tube). Per KN 16 each clip is a Simpson FCB43.5 with (4) #12-14 screws to studs and (2) #12-24 to the PEMB wind beam. No spacing is printed for KN 16, so it reads as one clip per stud at each wind-beam crossing.
- S4.1 references: 1/S5.3 at the east wall (window zone, KN 8/9). 3/S5.3 twice at the south (grid C) wall. 2/S5.3 and 2/S5.3 SIM also appear at the south wall.

## 5. A5.2 (p47), D1/D2 head and jamb
Crops: `img/A5.2_det11_head.png`, `img/A5.2_det12_jamb.png`, `img/A5.2_type_D1_D2.png`
- Window types D1 and D2 (one elevation): "11'-4 3/8" (R.O.)" wide x "3'-4 3/8" (R.O.)" high, two lites, glazing tag 1. "ALUMINUM STOREFRONT FRAMING (2" X 4 1/2") SYSTEM, THERMALLY BROKEN, FIXED UNIT." The elevation is cut by 11/A5.2 (head), 12/A5.2 (jamb) and 13/A5.2 (sill).
- 11/A5.2 HEAD DETAIL: "6" COLD FORM METAL FRAMING." "FIRE TREATED 2X4 WOOD BLOCKING ANCHORED TO MASONRY." "5/8" FIRE TREATED PLYWOOD SHEATHING." "5/8" TYPE "X" GYPSUM BOARD." "1 1/2" (25 GA.) COLD FORM METAL Z-FURRING FRAMING AT 24" O.C. WITH 1 1/2" FOIL FACE POLYISOCYANURATE INSULATION (MIN R-9) BETWEEN." Also "EXTERIOR CONCRETE MASONRY SMOOTH FACE UNIT (CMU) WALL SYSTEM", "EXTERIOR PORTLAND CEMENT (STUCCO)", "STUCCO EXPANSION JOINT. REFER TO DETAIL 4/A3.1." Dimensions: 1", 5/8", 6", 7 5/8", 1 1/2", 5/8".
- 12/A5.2 JAMB DETAIL: "FIRE TREATED WOOD BLOCKING." (size NOT PRINTED; drawn about 1 1/2" thick, in the Z-furring layer). "5/8" TYPE "X" GYPSUM BOARD." "1 1/2" (25 GA.) COLD FORM METAL Z-FURRING FRAMING AT 24" O.C. WITH 1 1/2" FOIL FACE POLYISOCYANURATE INSULATION (MIN R-9) BETWEEN." "CONCRETE MASONRY SPLITFACE UNIT (CMU) JAMB UNIT". FRT plywood at the jamb: NOT PRINTED.

## 6. A4.1 (p44), backing for plumbing fixtures and water heater
Crops: `img/A4.1_notes.png`, `img/A4.1_keynotes_13-18.png`, `img/A4.1_elev10_kn13.png`, `img/A4.1_elev13.png`, `img/A4.1_accessory_gen_notes.png`
- General Note C: "REFER TO PLUMBING DRAWINGS FOR FIXTURE TYPES AND ADDITIONAL REQUIREMENTS. PROVIDE ADDITIONAL COLD FORM METAL FRAMING OR FIRE TREATED BLOCKING AS REQUIRED FOR PROPER SUPPORT."
- KN 13: "FIRE TREATED 2X WOOD BLOCKING." Drawn in 10/A4.1 (grab bar section) behind the grab bar flange in the wall (KN 12), with the boxed note "GRAB BAR SUPPORT BAR FASTENER & MOUNTING SUPPORT SHALL BE ABLE TO WITHSTAND 250#/FT. IN BENDING, SHEAR & TENSION." Dimensions printed there are grab-bar clearances only (MIN. 1 1/4" / MAX. 1 1/2", 1 1/2" TYP.). Blocking length and height: NOT PRINTED.
- KN 17: "WALL MOUNTED WATER HEATER AND SUPPORT PLATFORM, REFER TO PLUMBING DRAWINGS. PROVIDE FIRE TREATED BLOCKING OR ADDITIONAL COLD FORM FRAMING AS REQUIRED FOR INSTALLATION." Drawn in 13/A4.1 as a bracket-supported platform above the drinking fountain (KN 4) and janitor sink (KN 5). The only nearby dimension is "4'-0"", the width of the wall panel (KN 8) zone under it. Blocking size, extent and platform dimensions: NOT PRINTED.
- Accessory General Note 1: "CONTRACTOR TO PROVIDE FIRE TREATED WOOD BLOCKING FOR INSTALLATION OF TOILET ACCESSORIES, INCLUDING OWNER FURNISHED AND CONTRACTOR INSTALLED ACCESSORIES. COORDINATE REQUIREMENTS WITH OWNER."
- No dimensioned backing for lavatories, water closets or urinals is drawn on A4.1. Backing size/extent: NOT PRINTED.
