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
