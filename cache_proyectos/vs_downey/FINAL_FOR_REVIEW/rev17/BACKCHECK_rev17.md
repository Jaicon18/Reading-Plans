# BACK-CHECK rev17 — VS #679 Downey (FINAL)

## rev17 changes (resolved by the drawings, A03.01 vector geometry; RCP aligned 1:1 with A02.01)
1. ROOM 4 BEAUTY 3: ceiling = A03.01 vector area 1,008.10 SF (was 995.26; the gross used the south width while north of W076 the west face is 0.433 ft farther out).
2. CORRIDOR (E of BREAK ROOM): only y 1527.5-1685.5 is gyp bd P-230 = 6.167 x 8.778 = 54.13 SF (was 106.89); the rest is the RECEIVING ACT-2 grid = ACT, EXCLUDED (trade we do not do).
3. FR ALCOVE: ends at the FR LOUNGE wall (x 1350.5) = 36.317 x 4.583 = 166.45 SF (was 174.06; 7.61 SF overlapped FR LOUNGE).
4. VS DISPLAY WINDOW 1 / 2: net of the blind vestibules (carried in their own row) = 35.00 / 34.94 SF (were 47.96 each).
Chain recalculated by the programs: board, main / cross tees, angle molding, hangers, hanger wire, lateral bracing (small ceilings: 22 clusters = 825.26 LF splay wire + 145.93 LF stud struts), finishing.

| Material | Unit | rev16 | rev17 | Δ |
|---|---|---|---|---|
| 3-5/8" metal stud (LF of material) | LF | 18,050.60 | 18,034.52 | -16.08 |
| Hanger wire | LF | 7,519.34 | 7,368.37 | -150.97 |
| 5/8" gypsum board, Type X | SF | 20,964.81 | 20,891.29 | -73.52 |
| USG drywall suspension main tee DGLW26 | LF | 2,298.32 | 2,253.05 | -45.27 |
| USG drywall suspension cross tee DGLW424 | LF | 3,439.49 | 3,400.60 | -38.89 |
| USG angle molding DGWM24 | LF | 1,223.01 | 1,187.97 | -35.04 |
| Hanger wire 12 ga - hanger count (one per hanger, height per room) | PCS | 713.00 | 703.00 | -10.00 |
| Joint compound, all purpose | LB | 1,585.57 | 1,580.28 | -5.29 |
| Joint tape, paper | LF | 8,148.07 | 8,120.86 | -27.21 |

3-5/8" metal stud FINAL: 18,034.52 + 148.61 (framed soffit rows) = 18,183.13 LF. Open RFIs: 0.

---
# BACK-CHECK rev16 — VS #679 Downey (FINAL)

## rev16 change
Printed note A/A12.01 + C/A12.01 "ADDITIONAL STUD REQ'D AT EQ. STUDS" carried: 1 additional full-height stud per diagonal brace (A/S03.01 centers each diagonal over a vertical stud), by program from the diagonal layout per wall (diag_brace_bays_info, 255 diagonals): 3-5/8" 253 studs = 3,041.00 LF; 6" W070 2 studs = 24.00 LF. Storefront diagonals not included (the note is on the interior partition sections).

| Material | Unit | rev15 | rev16 | Δ |
|---|---|---|---|---|
| 6" metal stud (LF of material) | LF | 123.09 | 147.09 | +24.00 |
| 3-5/8" metal stud (LF of material) | LF | 15,009.60 | 18,050.60 | +3,041.00 |

3-5/8" metal stud FINAL: 18,199.21 LF. Markups 178/178 OK (A02.01 + A01.01 demo). REGLAS OK. Open RFIs: 0.

---
# BACK-CHECK rev15 — VS #679 Downey — 3-5/8" metal stud (blind, directed)

An independent auditor recounted the 3-5/8" metal stud from the canon and the drawings without seeing the take-off total or the Excel. Each family difference was resolved with one directed check (crop). Crops: proceso/evidence_backcheck_stud/.

## Breakdown by family (LF)
| Family | rev14 | Blind back-check | rev15 | Δ rev15 vs back-check | Source |
|---|---|---|---|---|---|
| a) Wall studs (field + nodes, by wall ID / type; incl. SS1 50.16 and W001 extension) | 11,003.81 | 10,997.32 + SS1 46.58 (auditor counted SS1 in f) | 11,003.81 | -40.09 (-0.36 %) | A02.01, M/A02.01, A/A12.01, C/A12.01, A01.01 |
| b) Openings: jambs + cripples (16 openings) | 912.16 | 912.13 | 912.16 | +0.03 | A02.01, A10.08, S01.01 note 15 |
| d) Diagonal bracing to structure, interior partitions | 1,411.15 | 1,414.86 | 1,411.15 | -3.71 (0.26 %) | A/S03.01 @48" O.C. |
| e) Compression struts, ceiling lateral bracing | 527.94 | 523.91 | 523.94 | +0.03 | J/A12.02, K/A12.02, A03.01, A01.01, A/S03.01 |
| f) Storefront piers SP1 + SP2 | 438.66 | 438.66 | 219.32 | corrected (see 2) | A/S02.01 |
| f) SF built-up box posts (6) + (16) | 329.00 | 328.99 | 329.00 | 0 | A/S02.01, S01.01 notes 6, 16 |
| f) Grille portal head box | 96.24 | 96.24 | 144.36 | corrected (see 3) | B/S02.01, D/A08.10 |
| f) Display window head trusses | 170.02 | 121.97 | 121.97 | 0 (see 1) | F/S02.01, A03.01 |
| f) Storefront diagonal braces to structure | 0 | ~53 | 53.10 | corrected (see 4) | B, P, F/S02.01 + A/S03.01 |
| f) Display window platform edge boxes | 141.70 | 141.70 | 141.70 | 0 | A/A10.0x |
| f) Suspended stud (backwrap + valances, S/S03.01) | 85.62 | 85.62 | 85.62 | 0 | S/S03.01 |
| f) Framed soffits B/A10.03 + F/A10.05 (own rows) | 148.61 x 2 | 148.61 | 148.61 | corrected (see 5) | B/A10.03, F/A10.05 |
| f) Other small items (A1 shelving stud, hanger studs, water heater, traffic counter, W001 ext.) | 63.49 | 56.49 | 63.49 | +7.00 (W001 extension counted by the auditor in a) | S03.02, A/A12.02, E/A12.02, N1/S03.01 |
| **Total 3-5/8" metal stud** | **15,476.98** | **15,313.08** (before its own corrections) | **15,158.21** | -0.24 % vs back-check corrected (15,194.97) | |

Total in the Excel: main row "3-5/8" metal stud" 15,009.60 LF + "3-5/8" stud, framed soffit F/A10.05" 26.55 + "B/A10.03" 122.06 = **15,158.21 LF**. Headers / box beams (DBL 3-5/8") are a separate row (222.12 LF) and the 64.00 LF head-truss diagonals are in "storefront structural framing".

## Corrections applied in rev15 (each with a directed check)
1. Display window ceiling height: A03.01 prints VS DISPLAY WINDOW #1 / #2 = 11'-2" P-230; the 10'-2" tag is the blind vestibule strip. Head truss studs 3.542 -> 2.541 ft (-48.05 LF). Same fix on the display window hanger drops (4.75 / 4.375 ft): hanger wire -42.62 LF, struts -4.00 LF.
2. SP1 / SP2 piers: the 4 corners are SF built-up box posts (6)/(16), already carried; the corners were also counted twice in the pier faces. Studs between posts = 8 per pier (-219.34 LF).
3. Grille portal head box: B/S02.01 draws 3 stud lines, not 2 (+48.12 LF).
4. Storefront diagonal braces to structure: B, P, F/S02.01 "3 5/8" DIAG BRACE. SEE DETAIL A/S03.01" (storefront framing 48" O.C.): 17 x 2.209 x 1.414 = +53.10 LF.
5. Double count: the 7 framed soffit ceilings already make their 3-5/8" members (own rows 26.55 + 122.06); the same 148.61 LF were also in misc items inside the main stud row. Misc copy removed (-148.61 LF). New gate reglas.py A_SOFFIT_DOBLE (BE-VS-12).

## Not changed (with reason)
- Struts scope (J/K A12.02 drawn for ACT; K note 3 > 1000 SF; chart shows EMT): already estimator decisions R-ALC-11 / R-ALC-12.
- Field studs inside the R.O. are not deducted and jamb studs run full height: estimator convention of the skill.
- OPEN QUESTION: A/A12.01 and C/A12.01 note "ADDITIONAL STUD REQ'D AT EQ. STUDS. REFER TO STRUCT. DWGS." The structural sheets (A/S03.01) only ask to center the diagonal over a vertical stud with extra screws; no additional stud is drawn. Not carried. If it means one extra stud at each stud that receives a diagonal: +256 x wall height ≈ +3,077 LF. Verify at A/A12.01, C/A12.01, A/S03.01.

## Changes rev14 -> rev15 (NET)
| Material | Unit | rev14 | rev15 | Δ |
|---|---|---|---|---|
| 3-5/8" metal stud (LF of material) | LF | 15,328.37 | 15,009.60 | -318.77 |
| Hanger wire | LF | 7,561.96 | 7,519.34 | -42.62 |

Verdict: 3-5/8" metal stud = 15,158.21 LF (main row 15,009.60 + framed soffit rows 148.61). Every family within 1 % of the blind back-check after the 5 corrections. Open RFIs: 0; 1 open question (additional stud note).

---
# BACK-CHECK rev14 — VS #679 Downey

## rev14 change: compression struts as 3-5/8" metal stud (estimator decision 2026-11-02, R-ALC-12)
All lateral bracing compression struts (5 large + 18 small grid ceilings) moved from EMT (K/A12.02 chart) to 3-5/8" 20 GA metal stud, same lengths. Gauge: A/S03.01 '20 GA. DIAGONAL BRACING OPTIONS - DIAGONAL LENGTH UP TO 10'-0": SINGLE 3 5/8", 20 GA' (all drops <= 7'-8") and S/S03.01. Note on each item: 'Estimator decision 2026-11-02: compression struts as 3-5/8" metal stud; K/A12.02 shows EMT 1.25"/1.5" 20 GA (verify K/A12.02)'.

| Material | Unit | rev13 | rev14 | Δ |
|---|---|---|---|---|
| 3-5/8" metal stud (LF of material) | LF | 14,800.43 | 15,328.37 | +527.94 |
| EMT compression strut 1.5" dia x 20 GA (drop up to 8'-6"), ceiling lateral bracing - printed product K/A12.02 (see Where it comes from) | LF | 97.67 | 0.00 | -97.67 |
| EMT compression strut 1.25" dia x 20 GA (drop up to 7'-0"), ceiling lateral bracing - printed product K/A12.02 (see Where it comes from) | LF | 430.27 | 0.00 | -430.27 |

Final 3-5/8" metal stud: 15,328.37 LF. Open RFIs / pending items: 0.

---
# BACK-CHECK rev13 — VS #679 Downey

## rev13 change: tool fix R80f.4 / BE-CF14 (skill v81cf9)
The 1/2" moisture resistant gyp bd at the storefront (502.17 SF, A/A08.05, D/A08.10) was not in the finishing driver (accesorios.BOARD_DRIVER). Now joint compound and joint tape include it. Drywall screws stay EXCLUDED (fasteners).

| Material | Unit | rev12 | rev13 | Δ |
|---|---|---|---|---|
| Joint compound, all purpose | LB | 1,509.47 | 1,585.57 | +76.10 |
| Joint tape, paper | LF | 7,756.98 | 8,148.07 | +391.09 |

Open RFIs / pending items: 0. Bank: B&N, Chuze, O'Reilly, CFA = 0 families changed; only VS changes (the 2 rows above).

---
# BACK-CHECK rev12 — VS #679 Downey

## rev12 change: lateral bracing also carried on the 18 grid ceilings of 144 SF or less (R-ALC-11, conservative)
Spec A15.04 092900 ¶ N.1 'laterally brace entire suspension system'; J/A12.02 and K/A12.02 print no exemption by area. 25 clusters (1 per 12'-0" each way per ceiling). Delta if the architect exempts ceilings of 144 SF or less: -938.85 LF splay wire / -166.01 LF EMT strut. Verify at J/A12.02, K/A12.02 and spec 092900 ¶ N.1.

Additional head track 5UG (rev11) note confirmed: G/A10.08 draws a DBL 3 5/8" metal stud lintel (header), not an additional head track; stays as conservative assumption.

| Material | Unit | rev11 | rev12 | Δ |
|---|---|---|---|---|
| Hanger wire | LF | 6,623.11 | 7,561.96 | +938.85 |
| EMT compression strut 1.5" dia x 20 GA (drop up to 8'-6"), ceiling lateral bracing - printed product K/A12.02 (see Where it comes from) | LF | 30.67 | 97.67 | +67.00 |
| EMT compression strut 1.25" dia x 20 GA (drop up to 7'-0"), ceiling lateral bracing - printed product K/A12.02 (see Where it comes from) | LF | 331.26 | 430.27 | +99.01 |

Open RFIs / pending items: 0. 3-5/8" stud unchanged (14,800.43 LF).

---
# BACK-CHECK rev11 — VS #679 Downey

## rev11 change: additional head track carried as conservative assumption (R-ALC-11)
Door 5UG, 54" rough opening (G/A10.08), opening with its own box (openings_extra). The estimator standing criterion 'ADD FULL LENGTH ADDL HEAD TRACK @ OPNG > 4'-0"' is not printed in this set (A10.08, A12.01, S01.01, S03.01 swept). Per R-ALC-11 (no source anywhere = conservative assumption carried + note): (4.5 + 2 x 0.667) = 5.83 LF. Verify at G/A10.08 and A/A12.01.

| Material | Unit | rev10 | rev11 | Δ |
|---|---|---|---|---|
| Additional head track at openings over 4'-0" wide | LF | 0.00 | 5.83 | +5.83 |

Open RFIs / pending items: 0. Gates: canon OK, coverage 334/334, REGLAS OK, project data OK.

---
# BACK-CHECK rev10 — VS #679 Downey

## rev10 change (estimator correction 2026-11-02 to RFI-31, rule R-ALC-11)
Lateral bracing of the drywall grid ceilings is CARRIED. Not drawn on the RCP (A03.01) or on N/A12.02, but required by spec A15.04 092900 ¶ N.1 ("laterally brace entire suspension system") and printed as a pattern on J/A12.02 + K/A12.02.

Sources searched (R-ALC-11): S01.01 structural notes (SDC E), S03.01 (A, R, S, N details: wall bracing / suspended framing / water heater only, no ceiling bracing), S03.02 stud size matrix (walls only), M/A02.01 partition schedule (walls only), J/A12.02 and K/A12.02 (ceiling brace pattern + compression strut size chart). Printed pattern = J/A12.02: cluster of (4) 12 GA splay wires + compression strut @12'-0" O.C. each way and within 6'-0" of perimeter. Strut = EMT sized by drop (K/A12.02 chart). The spec gives no spacing, so the printed pattern governs.

| Item | rev9 | rev10 | Δ | Source |
|---|---|---|---|---|
| Hanger wire | 4,576.13 | 6,623.11 | +2,046.98 | J/A12.02, K/A12.02, 092900 ¶ N.1 |
| EMT compression strut 1.5" dia x 20 GA (drop up to 8'-6"), ceiling lateral bracing - printed product K/A12.02 (see Where it comes from) | 0.00 | 30.67 | +30.67 | J/A12.02, K/A12.02, 092900 ¶ N.1 |
| EMT compression strut 1.25" dia x 20 GA (drop up to 7'-0"), ceiling lateral bracing - printed product K/A12.02 (see Where it comes from) | 0.00 | 331.26 | +331.26 | J/A12.02, K/A12.02, 092900 ¶ N.1 |

3-5/8" metal stud: no change (14,800.43 LF). In rev8 the struts were carried as 3-5/8" stud; the printed strut is EMT (K/A12.02 chart), so rev10 carries EMT in 2 rows by size.

Not carried, with delta: 18 grid ceilings of 144 SF or less (closets, fitting rooms, office, restrooms, hallway, display windows): +25 clusters = +938.87 LF splay wire + 166.00 LF EMT strut if the spec "entire suspension system" is applied to them. Verify at J/A12.02, K/A12.02 (note 3: ceilings > 1000 SF), A03.01 and spec A15.04 092900 ¶ N.1.

Gates: canon OK, coverage 334/334, project data OK, REGLAS OK (skill v81cf5, suite 37/37). Every Material Summary row cites its sheet (fastener exclusion -> S01.01 B.10-B.14 / R/S01.01; track "other" -> A02.01; cement board -> A05.01; grille head -> S02.01, J/A08.10).

---
# BACK-CHECK rev2 — VS #679 Downey (step 11 blind auditor + step 12 error library)

## Step 11 — independent blind auditor (did not see the take-off)
| Item | Auditor | Take-off rev2 | Result |
|---|---|---|---|
| Standard + furred walls | 582.2 LF (pieces cut at every door) | 652.79 LF (runs through doors) | Consistent: ~49 LF of door openings; board is not reduced for openings (estimator rule) |
| RFID / insulated | 55.9 / 43.2 LF | 59.81 / 45.05 LF | Consistent (within 4 LF) |
| Wall board | ~10,613 SF (openings excluded, storefront faces excluded) | ~12,100 SF walls | Difference = door openings x faces (~1,000 SF) + storefront / piers faces; explained |
| Gyp ceilings | 6,066 SF, Type X (A15.04) | Type X (rev1 corrected); Room 4 valance zone deducted in rev2 | Consistent |
| Reduced stud spacing (shelving both faces) | Trans #2, #3, #5 spines, RFID, break / office | Applied in rev2 (8" O.C. on spines + zones, Table A3 at I03, diagonals @ 24") | Consistent |
| Corner bead | ~735 LF estimate | 924.25 LF counted (88 corners x face height) + trims | Take-off counts every corner; kept |
| Deflection track | ~62 LF (incl. storefront walls) | 45.05 LF (INS walls) | Storefront walls take printed standard track "3 5/8, 20 GA TRACK CONT" (P/S02.01, K/S02.01): kept |
| FRP | ~162 LF exposed walls | 665.28 SF = 166 LF x 4'-0" | Consistent |
| Structure heights | deck 17'-0", structure 12'-1" (A01.01) | same (corrected in rev1) | Consistent |

## Step 12 — error library (105 tests): 54 PASS / 17 FAIL / 34 N/A -> all 17 FAIL resolved
| Test | Finding | Resolution (rev2) |
|---|---|---|
| BE-12 / BE-101 | deflection clip pending item quoted a note that is not printed | deflection clips declared none (S01.01 B.1-B.14, A15.04, M/A02.01, L/S03.01 swept); pending item removed |
| BE-14 / BE-105 | ceiling track "size not printed" | perimeter = angle molding (N/A12.02); 1-5/8" valance track (B/A10.03); 3-5/8" backwrap drop (F/A10.05) |
| BE-15 | blocking bought as 3-5/8" studs; bridging on every wall | 6" x 18 GA backing track (F/A12.01) / plate (E/A12.01) rows; bridging only where both faces are not sheathed (R/S03.01): C.R. channel 1,739 -> 982.5 LF |
| BE-16 / BE-VS-03 | top-track splice M/S01.01 | applies to structural studs only; storefront top tracks < 10 ft -> 0 (S01.01 B.12) |
| BE-18 | beauty-cabinet blocking missing on some runs | 3 rows on all 6 runs (B/A10.03), +23.25 LF |
| BE-20 | soffit bottoms counted as 3 members along | members @ 16" spanning + ceiling-line level as drawn (B/A10.03, F/A10.05) |
| BE-40 / BE-102 | rows without N/SHEET; truncated citations | citation regex fixed (C/A12.01 no longer truncated; wall ids no longer read as sheets) |
| BE-44 | no markups PDF | false: markups PDF delivered (Drive, Planos marcados) |
| BE-46 | mixed products | rows split by product: storefront members, clips, backing track / plate; boards 5/8" FOIL-BACKED and 1/2" MOISTURE RESISTANT in own rows |
| BE-47 | closed RFIs cited as open | rewritten "closed: <answer> (N/SHEET)" |
| BE-51 | reveal pieces = LF | reveal / metal FRP trim bought by 10 ft trim stick |
| BE-55 | internal codes in client text | removed (scan of the Excel: 0 hits) |
| BE-VS-04 | Room 4 ceiling double count | valance zone deducted (-136.6 SF) |

## Left for the estimator (small, listed in PARA_REVISAR)
- Room 4 grid / hangers not reduced pro rata for the valance zone (about -45 LF main tee, -73 LF cross tee, -13 hangers).
- Partial-length bridging on W032, W050, W072, W077, W099 (about -109 LF channel if bridged only on the unsheathed length).
- Column wraps / piers: bridging per R/S03.01 rule carried (one face sheathed) although no detail draws it (-110 LF channel, -160 clips if excluded).

## rev4 (2026-11-02)
Estimator answered all 8 open RFIs (RFI-10, 11, 13, 15, 17, 22, 25, 26); decisions applied with N/SHEET in the take-off; no other change to the quantities checked above. Coverage 334/334; reglas.py re-run on rev4.

## rev5 (2026-11-02)
Estimator correction: gypsum board and metal framing demolition IS our scope (rule R-ALC-04). Demolition quantified from A01.01 keynotes 3, 4, 7 + existing demising board removal for the Type X replace: 10,971.24 SF (lengths from A01.01 vector geometry at 18 pt/ft calibrated on the printed 124'-7 1/8" lease line; existing heights not printed: +/-12'-0" and printed structure heights, PENDING). Visual check of the K4 crop done by the orchestrator. No other quantity changed.

## rev6 (2026-11-02)
Estimator decision: existing ceiling demolition EXCLUDED for lack of information (A01.01 keynote 2); no quantity change.

## rev7 (2026-11-02)
Rule R-ALC-06 applied: demo heights searched on all sheets (none printed for existing partitions; carried to the printed bottom of structure per bay, DERIVADO / PENDIENTE), cross-check A01.01 vs A02.01 wall by wall (A5 enclosure and north stockroom furring added; B2/A2 to bulkhead bottom), demo line markups (60 PolyLine DEMO with /Measure and Depth). Demolition 10,971.24 -> 13,488.88 SF. Visual check of A01.01_DEMO.png by the orchestrator.

## rev7.1 — text only: RFI-29 closed (estimator option A, partitions to structure); no quantity change.

## rev8 (2026-11-02)
Spec sweep A15.01-A15.06 + cross-check of every Material Summary row (SPEC_XCHECK.md); applied: door head runners 092900 M.2 (+40 LF), edge trim O.4 (+60 LF), FRP trim per 097216.16 (+96 LF), ceiling lateral bracing 092900 N.1 (RFI-31), storefront board 5/8" Type X W.R. (RFI-30). Project data sheet gate A_PROYECTO_DATOS green.

## rev9 (2026-11-02)
Estimator decision option A (drawings govern, R-ALC-10) on RFI-30..34: 1/2" MR storefront, no grid lateral bracing, metal FRP trim, angle molding only, 12 GA hanger wire; each with note: spec text, delta, sheet + spec section to verify.
