# B&N runner: variation between runs (#4, #5, #7) vs rev13 and rev2 (2026-10-31)

Sources: rev13 = final take-off with the estimator's decisions; rev2 = first pass of the subscription method; #4, #5, #7 = runner (API). LF and SF come from the Partition Takeoff and Material Summary of each Excel (`variacion.py`).

**Read this first:**
- The runs are NOT the same pipeline. Between #4, #5 and #7 the programs changed (R80e.46 to R80e.56: trim.py, height per face, nodes, openings gate, etc.). So the dispersion between runs mixes reading variation and pipeline change. This matters most for materials.
- #7 reused the readings of #6 (plus 1 correction). It is not an independent third reading.
- Class: SYSTEMATIC = mean error > 5 % and > 2x the dispersion; READING VARIATION = dispersion > 5 % with mean error ≤ 5 %; MIXED = both above 5 %.
- Type 1 / 1A / 1B / 1C (existing exterior) are excluded in all sources (RFI-01).

**Systematic, by type (the same error every run):**
- 4 (hourglass) −20.5 %: the reading takes 4 pieces; rev13 splits the curved walls into 6 chords + end returns (22 pieces).
- H2A −63 %: always 4.5 ft vs 12.2 ft (the dimension chain on A-221 is not closed).
- E1 −15.4 %; D +19.8 %; F +166 % in #4 / #5 (fixed in #7).

**Reading variation:** type 2 (CV 7 %, mean −0.4 %), B, and partly 5, C, I.

**Materials:** dominated by pipeline changes (trim 42 → 927 LF, 6" stud 1,700 → 3,119 LF after the fixes). In #7, the remaining systematic gaps are:
- 3-5/8" stud −20 %: 3 doors without an opening, the hourglass, H2A, inner soffit sides, and the 8/A-410 cross members (the decision exists, but the reading has no item);
- cement board, FRT plywood and W.R.: decision items missing from the reading (R80e.56, not run yet).

## By type (Length LF / Board SF)

| Type | rev13 | rev2 | #4 | #5 | #7 | runs CV (LF) | runs mean vs rev13 | class |
|---|---|---|---|---|---|---|---|---|
| 2 | 278.6 / 10839 | 273.6 / 10744 | 268.3 / 9460 | 304.4 / 12861 | 259.8 / 10332 | 7.0 % | -0.4 % | READING VARIATION |
| 3 | 38.7 / 309 | 38.7 / 619 | 38.7 / 309 | 38.7 / 309 | 38.7 / 309 | 0.0 % | +0.0 % | OK |
| 4 | 83.6 / 627 | 82.5 / 1237 | 66.4 / 861 | 68.2 / 887 | 64.8 / 838 | 2.0 % | -20.5 % | SYSTEMATIC |
| 5 | 5.7 / 103 | 5.7 / 103 | 9.9 / 179 | 5.9 / 294 | 5.7 / 103 | 27.2 % | +25.9 % | MIXED |
| A | 20.3 / 110 | 20.3 / 110 | 20.8 / 112 | 20.4 / 55 | 20.9 / 113 | 0.9 % | +2.0 % | OK |
| B | 3.2 / 17 | 3.2 / 17 | 2.8 / 15 | 3.3 / 9 | 3.2 / 17 | 7.4 % | -3.4 % | READING VARIATION |
| C | 3.2 / 17 | 3.2 / 17 | 2.2 / 12 | 3.3 / 9 | 3.2 / 17 | 16.2 % | -8.8 % | MIXED |
| D | 5.1 / 10 | 5.1 / 10 | 6.2 / 33 | 6.2 / 17 | 6.2 / 33 | 0.2 % | +19.8 % | SYSTEMATIC |
| E1 | 27.9 / 280 | 27.9 / 697 | 23.6 / 238 | 22.3 / 217 | 24.8 / 321 | 4.4 % | -15.4 % | SYSTEMATIC |
| E2 | 29.3 / 0 | 29.3 / 0 | 28.5 / 570 | 29.1 / 0 | 29.4 / 1054 | 1.4 % | -0.9 % | OK |
| F | 3.3 / 0 | 3.3 / 0 | 9.8 / 0 | 13.0 / 0 | 3.2 / 9 | 46.8 % | +165.8 % | SYSTEMATIC |
| H1 | 42.1 / 794 | 42.1 / 1237 | 38.5 / 837 | 42.9 / 670 | 41.7 / 1105 | 4.5 % | -2.6 % | OK |
| H2A | 12.2 / 304 | 12.2 / 432 | 4.5 / 90 | 4.5 / 113 | 4.5 / 161 | 0.4 % | -63.0 % | SYSTEMATIC |
| H2B | 1.9 / 0 | 1.9 / 0 | 2.0 / 0 | 2.0 / 0 | 2.0 / 41 | 0.9 % | +1.4 % | OK |
| H3A | 4.1 / 72 | 4.1 / 31 | 4.0 / 120 | 4.0 / 40 | 4.0 / 71 | 0.5 % | -1.5 % | OK |
| H3B | 6.2 / 152 | 6.2 / 47 | 6.8 / 135 | 6.7 / 167 | 6.2 / 112 | 3.7 % | +6.3 % | OK |
| I | 4.5 / 45 | 3.3 / 83 | 7.2 / 145 | 5.2 / 75 | 5.2 / 94 | 16.6 % | +29.9 % | MIXED |
| OTHER FRAMING (incl. column wraps) | 137.3 / 980 | 131.1 / 1050 | 101.3 / 879 | 39.9 / 1127 | 111.1 / 1017 | 37.5 % | -38.8 % | MIXED |

## Principal materials

| Material | rev13 | rev2 | #4 | #5 | #7 | #4 vs rev13 | #5 vs rev13 | #7 vs rev13 | runs CV | runs mean vs rev13 | class |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5/8" Type X | 14,267 | 15,539 | 8,267 | 16,130 | 15,595 | -42.1 % | +13.1 % | +9.3 % | 26.9 % | -6.6 % | MIXED |
| 5/8" Type X W.R. | 1,093 | 1,024 | 941 | 1,581 | 943 | -13.9 % | +44.7 % | -13.7 % | 26.1 % | +5.7 % | MIXED |
| 3-5/8" stud | 11,602 | 10,059 | 7,811 | 10,634 | 9,277 | -32.7 % | -8.3 % | -20.0 % | 12.5 % | -20.3 % | MIXED |
| 6" stud | 3,162 | 2,900 | 1,960 | 1,700 | 3,119 | -38.0 % | -46.2 % | -1.4 % | 27.3 % | -28.6 % | MIXED |
| Bottom track 3-5/8" | 450 | 444 | 425 | 515 | 478 | -5.5 % | +14.5 % | +6.3 % | 7.8 % | +5.1 % | MIXED |
| Bottom track 6" | 119 | 119 | 111 | 65 | 117 | -6.3 % | -45.5 % | -1.2 % | 24.0 % | -17.7 % | MIXED |
| 1/2" cement board | 434 | — | 980 | 306 | 374 | +125.7 % | -29.4 % | -13.8 % | 54.7 % | +27.5 % | MIXED |
| 5/8" cement board | 50 | — | — | — | — | — | — | — | — | -100.0 % | SYSTEMATIC |
| FRT plywood 5/8" | 2,686 | 2,528 | 3,635 | 3,411 | 2,143 | +35.3 % | +27.0 % | -20.2 % | 21.4 % | +14.0 % | MIXED |
| FRT plywood 3/4" | 370 | 142 | 376 | 290 | 364 | +1.6 % | -21.7 % | -1.8 % | 11.1 % | -7.3 % | MIXED |
| FRP panels | 2,001 | — | 2,001 | 2,090 | 2,001 | +0.0 % | +4.4 % | +0.0 % | 2.1 % | +1.5 % | OK |
| METAL trim | 957 | 892 | 328 | 42 | 927 | -65.7 % | -95.6 % | -3.1 % | 85.3 % | -54.8 % | MIXED |
| Blocking FRT | 568 | 552 | 552 | 552 | 552 | -2.8 % | -2.8 % | -2.8 % | 0.0 % | -2.8 % | OK |
