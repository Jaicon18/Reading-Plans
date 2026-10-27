VERDICT: FAIL
LIBRARY: 32 PASS · 5 FAIL · 3 N/A

# Back-check rev8: Barnes & Noble Colorado Springs, metal frame & drywall
Date: 2026-10-27. I compared `..._Takeoff_FINAL_rev8.xlsx` and `..._FINAL_markups_rev8.pdf` with rev7, PASO12_rev7 (certificate, img/, MATRIZ_COBERTURA › Observations) and BIBLIOTECA_ERRORES (40 tests).
Bid set re-read on A-410 (page 27): 5/A-410, 8/A-410 and 9/A-410 at 130-150 dpi. I also used the certificate crops for 5/A-121, note 8 and E-301 265119.
- Geometry did not change: partitions 569.816 LF, board 16,201.88 SF, and the 77 markups reconcile by type.
- Every rev8 quantity reproduces, except the drywall screw split (C7-05).
- The other FAILs are text defects and one printed accessory with no destination.

## 1. CORREGIR C7-01..C7-09 and GAP N-01, N-03
| ID | rev8 value | Citation in rev8 | Result |
|---|---|---|---|
| C7-01 | 1-5/8" stud row removed (rev7 R13 = 131.42 LF). Hanger wire R17 adds SEISMIC-VERTICAL-WIRE-5-A121 131.42 LF | MS!I17; Pending RFI-38 C41: "horizontal carrying member (no post)" | PASS on the quantity. **RFI-38 B41 still says "5/A-121 draws ... a 1-5/8" x 16 ga metal joist post"** (see BE-12). The 16 ga wire is in the 12 ga hanger wire row (see BE-46) |
| C7-02 | Slab pins R50 = 960.91 (640.61 / 0.666667) | Inputs!C22 "A-410 note 8.F X-DNI 2 rows at 16" O.C." and RFI-ACC-slab-pins: alternatives -480.46 / -640.61. "type K box" removed | PASS. The certificate's 960.92 vs 960.91 is rounding. R50 N/SHEET cites only 9/A-410, not 8.F (comment) |
| C7-03 | R27 #8 pan head = 291; R28 P.A.F. 3/16" x 3/8" = 282; X-EDNI row removed | MS!I27 and I28 quote 8/A-410 word for word (matches the crop). X-EDNI is the alternative in RFI-51 C56 | PASS. I recomputed Σ(ROUNDUP(L/2)+1) over the 32 nested-runner runs (479.85 LF) = 291, and 705 / 5.0 x 2 = 282 |
| C7-04 | R49 #8-18 x 1/2" = 1,940 (4 x 485 pcs); R56 #10-16 x 3/4" = 1,776 (6 x 296 pcs); total 3,716 | MS!I49 and I56; Inputs!C21 | PASS with comment. The certificate has 1,964 + 1,740 = 3,704. The difference comes from the piece split (491/290 vs 485/296): 7,257 / 25 = 290.3, and per-wall ROUNDUP gives 295. Net difference is +12 pcs |
| C7-05 | R48 Type S = 6,402.26 (1.2 x 5,335.22 SF); R57 S-12 = 13,039.99 (1.2 x 10,866.66 SF) | MS!I48 and I57; Inputs!C20 cites 8.E + A-001A Div 09 A.5. "GA-216" removed | **FAIL.** The gypsum on the 14 ga walls from rev8's own R19 + R20 breakdowns is 11,143.59 SF (Type 2 10,839.34 + C-H2a 304.25; C-H2b and C-F carry 0). So S-12 = **13,372.31** and Type S = **6,069.95**, the same as the certificate. The 10,866.66 SF does not reproduce: 276.93 SF is missing and no subset of faces explains it. The total of 19,442.25 is right |
| C7-06 | R34 1/2" = 739.90 SF; R29 5/8" = 50.04 SF; sum 789.94 | MS!I34 (E, A-D/A-221) and I29 (22/A-201); R31 N/SHEET now lists E/A-221, A-D/A-221 and 22/A-201 | PASS. 475 + 52.75 + 57.75 + 154.38 = 739.88 (Δ 0.02) |
| C7-07 | 568.27 LF | Pending RFI-23 C26 and Scope ALC-16 D17; no "585.27" left in the workbook | PASS |
| C7-08 | rev7 README rows #7, #48, #51, #53, #61, #148, #149, #372, #432 cite ALC-X40..X44 | All of these exist in Scope Checklist A26:A30. No ALC-X26..X29 in the rev7 or rev8 README | PASS |
| C7-09 | Legend p.70: "Source: the take-off Excel (Partition Takeoff)" | PDF text scan: 0 hits | PASS. PDF metadata Keywords and Creator still read "markups_bluebeam" (comment) |
| N-01 | R12 adds NESTED-BRACING-T3-T4 122.32 LF (38.68 + 83.64) | RFI-46 B49/C49 extended to 3/A-410 and 4/A-410, with "if not required: minus both" | PASS |
| N-03 | No quantity change. RFI-53 C55: "-401.0 LF hanger wire (29 hangers)" if by the EC | RFI-53 B55 quotes E-301 Sec. 265119 (matches the crop) | PASS |

## 2. Material Summary diff rev7 → rev8 (recomputed)
| Row (rev8) | rev7 → rev8 | Recompute | OK? |
|---|---|---|---|
| R12 3-5/8" stud | 11,479.27 → 11,601.59 | +122.32 (N-01). Gauge split 7,257 (14 ga) + 2,927.08 (20 ga) + 1,417.51 (elements) = 11,601.59; I summed the 20 ga walls and the elements independently | Yes |
| (rev7 R13) 1-5/8" stud | 131.42 → removed | Moved to wire (C7-01) | Yes |
| R17 hanger wire | 2,689.79 → 2,821.21 | +131.42; the breakdown sums 2,821.21 | Yes (product mix, BE-46) |
| R27 #8 pan head | — → 291 | 291 (32 runs) | Yes |
| R28 P.A.F. | — → 282 | 141 x 2 | Yes |
| (rev7 R28) X-EDNI | 720 → removed | Alternative in RFI-51 | Yes |
| R29 / R34 cement board 5/8" / 1/2" | 789.94 → 50.04 + 739.90 | 42.89 LF x 1.1667 = 50.04; 739.88 | Yes |
| R48 Type S / R57 S-12 | 19,442.26 → 6,402.26 + 13,039.99 | **6,069.95 + 13,372.31** | **No (±332.3)** |
| R49 #8-18 / R56 #10-16 | 3,124 → 1,940 + 1,776 | 1,964 + 1,740 (cert); 1,970 + 1,770 with per-wall ROUNDUP | Close (+12) |
| R50 slab pins | 640.61 → 960.91 | 640.61 x 2 / 1.333 = 960.92 | Yes |
| Other rows | unchanged | Board, track, FRT, clips and compound/tape are the same as rev7 | Yes |
BE-40 automated check: every row has N/SHEET, and every breakdown or operation reproduces its Net within 0.1. The exception is R57, whose operation reproduces the Net, but the 10,866.66 SF input in that operation cannot be traced to any source.

## 3. Error library (40 tests)
| Test | Result | Note |
|---|---|---|
| BE-01 | PASS | Fire-stop track 264.21 LF + RFI-35; unchanged |
| BE-02 | PASS | W.R. restroom ceilings 61.19 + 61.11 in R20 |
| BE-03 | PASS | All wet-room gypsum faces are in R20 W.R.; unchanged |
| BE-04 | PASS | No FRT-only face in W.R. or board |
| BE-05 | PASS | Board by face unchanged from rev7 (layers by side) |
| BE-06 | PASS | SS-N/E/IN-N/IN-E/GG + bottoms present |
| BE-07 | PASS | C-I-E1, C-I-E2 (I SIM.) |
| BE-08 | PASS | No LF change; printed dimensions as in rev7 |
| BE-09 | PASS | 17 EXISTING annotations; no existing wall in the Excel |
| BE-10 | PASS | SS-GG 6'-2" HOLD quantified; T.O. WD-1 15'-0" |
| BE-11 | PASS | Janitor 17.0 SF 3/4" FRT + RFI-33 |
| BE-12 | **FAIL** | RFI-38 B41 still attributes "a 1-5/8" x 16 ga metal joist post" to 5/A-121 (contradicts C41 and the plan). RFI-ACC-slab-pins B2 quote is cut off: '9/A-410 "0.177 D)' |
| BE-13 | PASS | 2/E-103 → RFI-50 + 32 SF |
| BE-14 | PASS | The new "not printed" claims (cement-board screw spacing, nested member) are true on the sheets I read |
| BE-15 | PASS | All MS row descriptions match the drawn members. 1-5/8" is gone, #8 and P.A.F. are on 8/A-410. The B41 text is under BE-12 |
| BE-16 | **FAIL** | 5/A-410 prints "(4) TEK SCREWS" per clip angle: 2,518 x 4 = 10,072 pcs. No row, no exclusion and no RFI (certificate O6, still open). R26 only names them |
| BE-17 | **FAIL** | Rows exist by gauge, but the S-12 / Type S counts are off by ±332 (C7-05) |
| BE-18 | PASS | N-01 → RFI-46 + 122.32 LF; N-03 → RFI-53; no GAP left from the certificate |
| BE-19 | PASS | Slab pins on the printed 8.F with the 9/A-410 alternative in RFI; #8 @ 24" printed; cement-board screw spacing → RFI-51. The 1.2/SF drywall yield is the estimator's (O4) |
| BE-20 | PASS | Framed soffit studs + 2 tracks (R35, R13) |
| BE-21 | PASS | No glass mat |
| BE-22 | PASS | Jamb return 0 (1/A-500, 2/A-500) |
| BE-23 | PASS | No acoustical sealant row |
| BE-24 | PASS | Bottom = top = 568.61 = 569.816 - 1.206; separate rows |
| BE-25 | PASS | 5/A-121 suspension; 4/A-121 grid for the cloud |
| BE-26 | N/A | No ballistic type |
| BE-27 | N/A | No ATM recess |
| BE-28 | N/A | No new canopy or parapet |
| BE-29 | PASS | Headers 0 + RFI-09 |
| BE-40 | PASS | See §2; the R57 input belongs to BE-17 |
| BE-41 | PASS | No .json/.py/work folder in the visible sheets ("canon constants" in Inputs C12-C14 is a comment) |
| BE-42 | PASS | Order 2, 5, 3, 4, H1…C; subtotals Σ = 569.816 = GRAND TOTAL |
| BE-43 | PASS | 6 visible sheets + hidden _reglas |
| BE-44 | PASS | 94 plan annotations (A-101 68 + A-221 26) = 77 walls + 17 EXISTING; LEGEND 18. Σ LF and Σ LF x H per type = Excel (max Δ 0.15 SF, type 2) |
| BE-45 | PASS | Screws/SF 1.20 stated in Inputs C20; pins 1.5/LF of track per 8.F; framing screws 4.76 per piece |
| BE-46 | **FAIL** | R17 "Hanger wire" mixes 12 ga hanger and splay wire (R39 "12 ga"; 5/A-121 "(4)-12 GA. SPLAY WIRES") with the 131.42 LF of "16 GA. WIRE" (5/A-121) |
| BE-47 | **FAIL** | Automated scan: every RFI-/ALC- ID cited exists. RFI-51 C56 still says "Slab pins at 12" O.C. (estimator criterion); ... 8.F ... = about + 321 pins", while R50 carries 960.91 per 8.F. The same cell's "+724 screws" list still includes "posts". The 57 unmatched numbers left are deltas or derived values unchanged since rev7 |
| BE-48 | PASS | 0 hits for .json/.py/work folders in the page text, annotation Contents, content streams or xref objects of the 70-page PDF |
| BE-49 | PASS | No new dimension used; 46'-0" stays LWT-01 |
| BE-50 | PASS | E-301 265119 → RFI-53 with delta; 2/E-103 → RFI-50 |

## 4. Open issues
Blocking (FAIL):
1. **C7-05 / BE-17.** Set R57 S-12 = 1.2 x 11,143.59 = **13,372.31** and R48 Type S = 1.2 x 5,058.29 = **6,069.95**. The total stays 19,442.25. Write the operation from the faces of the 14 ga walls (Type 2 + C-H2a), or explain the 276.93 SF.
2. **BE-12.** Rewrite RFI-38 B41 without the "metal joist post": the 1-5/8" is the horizontal member @ 48" and the brace point is 16 ga wire. Complete the 9/A-410 quote in RFI-ACC-slab-pins B2: "0.177 DIA. HILTI POWDER ACTUATED FASTENER W/ 3/4" EMBEDMENT AT 24"".
3. **BE-47.** In RFI-51 C56, delete "Slab pins at 12" O.C. (estimator criterion) ... + 321 pins" and remove "posts" from the "+724 screws" list.
4. **BE-16.** Give the 5/A-410 "(4) TEK SCREWS" per clip angle a destination: a row of 10,072 pcs, or "included in R49/R56" with the operation, or an RFI-51 line with the delta.
5. **BE-46.** Split the 131.42 LF of 16 ga wire out of R17 into its own row (R17 → 2,689.79 LF of 12 ga).

Comments (non-blocking):
- C7-04: piece split 485/296 vs the certificate's 491/290 (+12 screws). State the rounding method in I49/I56. I56 and I57 have no live J formula, while the other yield rows do.
- R50 N/SHEET cites only 9/A-410; add "A-410 note 8.F". R48 and R57 N/SHEET should name "8.E" as Inputs C20 does.
- 9/A-410 prints "#8 SCREWS EA. SIDE OF STUD TO TRACK (TYP.)" for all walls, while 8.A asks for #10-16 on heavy gauge. Consider one RFI line.
- 8/A-410 parallel condition also prints "(2) #8 SCREW AT EACH STUD" and "ATTACH TO TRACK W/ #8 SCREWS AT 24" O.C." for the cross members. These are only covered by the "+724" mention in RFI-51.
- PDF metadata Keywords and Creator read "markups_bluebeam" (tool name). This is outside BE-48's scope, but should be cleared.
- Client-facing texts carry process tags: "(v80o: printed spacings, BE-19)" in B2, "Paso 12 2nd pass (rev8)" in RFI-38/46/51/53, "studs_out" in RFI-28 C31, "canon constants" in Inputs C12-C14 (O2).
- The rev8 README cites internal paths (../PASO12_rev7/..., BIBLIOTECA_ERRORES.md, "Rule v80j"). PARA_REVISAR_EN_LA_MANANA.md sits in the deliverable folder; move it before sending.
- Certificate observations still open: O1 (C-F nested bracing vs nested runner), O3, O5, O7 (RFI-51 after RFI-53), O8 ("pressure treated" for SS-GG in R37).
- Rounding: menu-board FRT is 60.61 in RFI-23/ALC-16 and 60.6 in R38; restroom backing is 17.78 vs 17.77.
