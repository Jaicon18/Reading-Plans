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
