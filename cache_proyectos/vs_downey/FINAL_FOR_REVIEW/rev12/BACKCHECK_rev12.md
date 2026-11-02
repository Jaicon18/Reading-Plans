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
