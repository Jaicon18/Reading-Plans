VERDICT: FAIL
LIBRARY: 34 PASS · 3 FAIL · 3 N/A

# Back-check rev8 (re-check): Barnes & Noble Colorado Springs, metal frame & drywall
Date: 2026-10-27. File under test: `Barnes_Noble_ColoradoSprings_Takeoff_FINAL_rev8.xlsx` (md5 593a7ba2ed08cf9272850c7ecea9969d), opened with openpyxl data_only=True. The rev8 markups PDF was also checked for BE-44 and BE-48. It was regenerated at 06:30, after the first back-check.

Plan text was read on these crops:
- 5/A-410, 7/A-210 and 5/A-121, rendered at 110-200 dpi from the clean bid set (pages 28, 13 and 8).
- The certificate crops: A-410 note 8, 9/A-410 and 5/A-121.

Material Summary rows moved: there are 2 new rows (R28 Tek screws, R29 16 ga wire). The old R48/R57 are now R50 (Type S) and R59 (S-12).

## 1. Re-test of the 5 previous FAILs

| Previous FAIL | rev8 now | Plan text | Result |
|---|---|---|---|
| C7-05 / BE-17 (drywall screws by gauge) | MS!C59 S-12 = **13,372.31**, I59 "1.2 x 11143.59 SF of board on the 18/16/14 ga walls (C-F, C-H2a, C-H2b, W2-01 … W2-09)". MS!C50 Type S = **6,069.95**, I50 "1.2 … x 5058.29 SF", J50 = 6,069.948 | Note 8.E: "#7 X 1-1/4" HI-LOW TYPE "S" … TO 25 GAUGE OR 20 GAUGE STUDS" / "#6 X 1-1/4" TYPE S-12 … TO 18 GAUGE OR 16 GAUGE STUDS OR TRACKS" | **Fixed.** I recomputed from the R19 + R20 breakdowns over the walls marked 14 ga SJ in the Partition Takeoff (type 2 + H2A + H2B + F). That gives 11,143.59 SF (type 2 subtotal 10,839.34 + C-H2a 304.25). 16,201.88 − 11,143.59 = 5,058.29 SF. The sum is unchanged (19,442.26). **But BE-17 fails again on the new Tek row (see §3)** |
| BE-12 (RFI-38 "metal joist post"; slab-pin quote cut off) | Pending!B41: "…a 16 ga wire @ 12'-0" O.C. each way at each brace point (the 1-5/8" x 16 ga metal joist framing @ 48" is the horizontal carrying member)". C41: "(no post)". Pending!B2: "A-410 note 8.F X-DNI 2 rows @ 16" O.C. (printed, conservative); 9/A-410 0.177" PAF @ 24" = alternative" | 5/A-121: "16 GA. WIRE 12'-0" O.C. EACH WAY AND WITHIN 6'-0" OF EACH WALL", "1 5/8" x 16 GA. METAL JOIST FRAMING @ 48" O.C.". 9/A-410: "0.177 DIA. HILTI POWDER ACTUATED FASTENER W/ 3/4" EMBEDMENT AT 24"" | **PASS.** "metal joist post" is gone from the workbook. B2 no longer has a broken quotation mark. It now paraphrases 9/A-410 accurately instead of quoting it in full (comment) |
| BE-16 (5/A-410 "(4) TEK SCREWS" without a row) | New MS!R28 = **10,088 PCS**: "2518 clips x 4 = 10072 + 7/A-210 "(4) #10-16 SCREWS": 4 clips x 4 = 16" | 5/A-410: "2" x 2" 16 GA. CLIP ANGLE 1/4" LESS THAN STUD WIDTH" / "(4) TEK SCREWS". 7/A-210: "…ATTACH TO JAMB AND RUNNER TRACK USING (4) #10-16 SCREWS" | **Fixed for 5/A-410.** 2,518 x 4 = 10,072, and R26 carries 2,518 clips. **BE-16 still fails on 7/A-210 (see §3)** |
| BE-46 (16 ga wire inside hanger wire) | MS!C17 Hanger wire = **2,689.79**. The breakdown sums to 2,689.79 and contains only hangers + fixture hangers + "SPLAY-WIRES-5-A121 743.29". New MS!R29 "16 ga wire at seismic brace points (5/A-121)" = **131.42 LF** | 5/A-121: "(4)-12 GA. SPLAY WIRES" (12 ga, same as the hangers); "16 GA. WIRE 12'-0" O.C. …" | **Fixed.** R17 now holds 12 ga only. **BE-46 fails again on the new Tek row (see §3)** |
| BE-47 (RFI-51 "Slab pins at 12" O.C." and "posts") | Pending!C56: "…the detail members (braces, cross members, bracing) add about + 724 screws … Slab pins carried per note 8.F (2 rows @ 16" X-DNI); 9/A-410 alternative 0.177" PAF @ 24" = - 640.61 pcs" | — | **PASS.** The workbook has 0 hits for "Slab pins at 12", "metal joist post" and "+ 321". "posts" is gone from the list. The −640.61 figure matches Pending!C2 "24in: -640.61 pcs" (960.91 − 320.30) |

## 2. Error library (40 tests)

| ID | Result | Evidence |
|---|---|---|
| BE-01 | PASS | MS!I13 has FIRESTOP-* lines per wall; RFI-35 C38 = 264.21 LF; unchanged from rev8 |
| BE-02 | PASS | MS!I20 includes ceilings Women's 109 61.19 + Men's 108 61.11 |
| BE-03 | PASS | R20 W.R. covers W2-05…W2-08 and W5-01; RFI-11 C14 1,092.59 = 222.93 + 223.02 + 485.75 + 88.63 + 122.30 − 50.04 |
| BE-04 | PASS | No C-* face in R20; the Work Room is FRT plywood (RFI-11) |
| BE-05 | PASS | Board by face is unchanged; Partition Takeoff board total 14,881.32 is unchanged |
| BE-06 | PASS | SS-N, SS-E, SS-IN-N, SS-IN-E, SS-GG + SS-GG-BOTTOM-GWB present (R11, R12, R19, R39) |
| BE-07 | PASS | C-I-E1 and C-I-E2 0.603 LF each (I SIM.) |
| BE-08 | PASS | Partition LF unchanged: GRAND TOTAL 569.816 |
| BE-09 | PASS | 17 "EXISTING - EXCLUDED" markups; no existing wall in the Excel; RFI-01 |
| BE-10 | PASS | SS-GG 6.167 x 17.917 quantified; RFI-34 T.O. WD-1 15'-0" |
| BE-11 | PASS | MS!I40 JANITOR-FRT-11-A200 17 SF + RFI-33 |
| BE-12 | PASS | See §1. The quotes in I28, I29, B41 and B55 match the crops. "#8" in the R28 title is an unprinted size; it is handled under BE-17 |
| BE-13 | PASS | SERVER-ROOM-BACKBOARD 32 SF + RFI-50 |
| BE-14 | PASS | No new "not printed" claims; the 7/A-210 clip count is "not printed" and that is true on the crop |
| BE-15 | PASS | R29 describes the 16 ga wire as vertical at the brace point. The 1-5/8" is "the horizontal carrying member". This matches 5/A-121 |
| BE-16 | **FAIL** | 5/A-410 Teks are now carried (R28). 7/A-210 also prints "RUNNER TRACK ATTACHED TO HEADER SUING (2) TEK SCREWS AT 16" O.C" (twice, top and bottom runner) and "#10-16 TEK SCREWS (TYP.)" at the head attachment. Neither has a row, an exclusion or an RFI line (RFI-51 B56 mentions only the 7/A-210 clip-angle count) |
| BE-17 | **FAIL** | Drywall screws are fixed (§1). The new R28 is titled "#8 Tek screws at clip angles", but the clip is "2" x 2" 16 GA." (5/A-410) and no size is printed. Note 8.A: "18/16 GAUGE - #10 - 16 X 3/4" TEKS WITH PHILIPS PAN HEAD". At minimum, the clips on the 14 ga walls (type 2, C-H2a, C-H2b, C-F: 1,470 clips = 5,880 screws) cannot be #8. 7/A-210 prints #10-16 for its own 16 ga clips |
| BE-18 | PASS | No GAP from the certificate is left (N-01 RFI-46, N-03 RFI-53, O6 Teks now R28) |
| BE-19 | PASS | Slab pins on note 8.F "2 ROWS AT 16" O.C." (960.91) with 9/A-410 @ 24" in RFI; #8 pan head @ 24" printed (8/A-410); cement board spacing → RFI-51 |
| BE-20 | PASS | Framed soffit studs (R12 SS-*, R37 13 joists x 4.716 = 61.31) + 2 tracks (R13) |
| BE-21 | PASS | No glass mat row (ALC-09 NOT APPLICABLE) |
| BE-22 | PASS | MS!R46 = 0 citing 1/A-500, 2/A-500 |
| BE-23 | PASS | No acoustical sealant row; ALC-19 EXCLUDED |
| BE-24 | PASS | Bottom = top: 450.02 + 118.59 (+72 other) each, separate rows R4-R9 |
| BE-25 | PASS | 5/A-121 suspension for the GWB ceilings; 4/A-121 USG grid for the cloud (R22-R25) |
| BE-26 | N/A | No ballistic type |
| BE-27 | N/A | No ATM recess (R44 = 0) |
| BE-28 | N/A | No new canopy or parapet (ALC-03, ALC-14) |
| BE-29 | PASS | Headers 0 + RFI-09 (+83.32 LF) |
| BE-40 | PASS | All 56 rows have N/SHEET. Every breakdown sums to its Net within 0.1: R15 207.46 vs 207.45, R19 15,109.23 vs 15,109.29 (Δ0.06), R36 739.88 vs 739.90, R39 1,790.48 vs 1,790.51. R35 sums to 957.03. Every operation row reproduces its Net: R37 13 x 4.716; R50 J 6,069.948; R52 960.91; R58 6 x 296 = 1,776; R59 1.2 x 11,143.59 |
| BE-41 | PASS | Visible sheets have 0 hits for .py, .json, _out, studs_out, canon, "Paso 12", v80*, cache_ or etapas. "(v80o …)" in B2, "Paso 12 2nd pass" and "canon constants" are gone. The hidden _reglas sheet was ignored |
| BE-42 | PASS | Order 2, 5, 3, 4, H1 … C; the subtotals add up to 569.816 = GRAND TOTAL |
| BE-43 | PASS | Exactly 6 visible sheets (Inputs, Partition Takeoff, Material Summary, Pending Items, Review Items, Scope Checklist) + hidden _reglas |
| BE-44 | PASS | rev8 markups: 112 annotations = 77 walls (A-101 + A-221) + 17 EXISTING + 18 legend. Σ LF per type = Excel on all 17 types plus OTHER FRAMING (137.31). Σ LF x H matches within 0.15 SF (type I) |
| BE-45 | PASS | 1.2 screws/SF (Inputs C20); 4 Teks per clip printed; pins 1.5 per LF of track (8.F); 4 / 6 framing screws per piece (8.A min. 2 / 3 per connection) |
| BE-46 | **FAIL** | The wire is fixed (§1). The new R28 mixes two products: 10,072 Teks (labeled "#8") + 16 "#10-16 SCREWS" from 7/A-210, under a "#8 Tek screws" title |
| BE-47 | PASS | All 85 RFI/ALC IDs cited exist. Numbers I spot-checked against their rows all match: RFI-38 743.29 / 131.42; RFI-51 4 / 1686 / 2331 / 781 (= 485 + 296) / 291 / 282 / −640.61; RFI-53 −401.0 / 29; RFI-27 15,109.29; ALC-07, ALC-10, ALC-11 1,006.54; RFI-46 6.52 + 122.32; RFI-40 479.85. See the ALC-04 comment |
| BE-48 | PASS | rev8 markups PDF: 0 hits for .json, .py, _out, takeoff_canon, cache_ or "Paso 12" in page text or annotations. Keywords and Creator metadata are now blank (they read "markups_bluebeam" before) |
| BE-49 | PASS | No new dimension used |
| BE-50 | PASS | E-301 265119 → RFI-53 with delta; 2/E-103 → RFI-50 |

## 3. Blocking issues
1. **BE-17 + BE-46 (MS!R28).** Retitle R28 "#10-16 x 3/4" Tek screws, pan head, at 16 ga clip angles (A-410 note 8.A 18/16 ga; size not printed on 5/A-410; 7/A-210 prints #10-16)". The quantity stays 10,088. This fixes both tests: there is one product (#10-16) in the row, and the size follows the printed note for 16 ga. Alternative: split the row by stud gauge and send the 16 pcs from 7/A-210 to their own #10-16 row. In both cases, flag the 5/A-410 size as "not printed" in RFI-51.
2. **BE-16 (7/A-210).** Give a destination to "RUNNER TRACK ATTACHED TO HEADER SUING (2) TEK SCREWS AT 16" O.C" (top and bottom runner) and to the head attachment "#10-16 TEK SCREWS (TYP.)". Either add them to the R28 count as 2 x (ROUNDUP(L/1.333) + 1) per runner track, using the header length of the vestibule nested header, or add an RFI-51 line with that delta.

## 4. Non-blocking comments
- Scope Checklist ALC-04 D5 (QUANTIFIED) still lists "X-EDNI fasteners 8.C". Rev8 carries no X-EDNI row; it is the alternative in RFI-51. Change it to "8/A-410 #8 pan head + P.A.F. (R27, R30); X-EDNI 8.C = alternative, RFI-51".
- R29 (16 ga wire) has selling unit "piece" and Pieces = 152. Use "continuous coil (LF)" as R17 and Inputs B19 do.
- S-12 uses the gross 14 ga faces (11,143.59), while the −50.04 SF cement-board base deduction sits in the Type S remainder. About 37 SF of that base is on 14 ga walls, so the error is roughly 45 screws in the split. The total is unchanged. Not material.
- R58 and R59 still have no live J formula, while R50 to R55 do. R52 N/SHEET cites only 9/A-410 (it should add "A-410 note 8.F"). R50 and R59 N/SHEET should name "8.E".
- Client-facing texts still carry internal audit codes: "rev7 plan check C7-03" (I27), "C7-01" (I29, Pending C41 "Plan check (rev8): C7-01"), "C-03" (I31), "C-07" (Pending C7, B38). "skill default" appears in I43, Pending C3 and B34. Replace these with plain wording (e.g. "plan check rev7" with no code, "estimator default").
- Pending!B2 now paraphrases 9/A-410 instead of quoting it. If a literal quote is wanted, use "0.177 DIA. HILTI POWDER ACTUATED FASTENER W/ 3/4" EMBEDMENT AT 24"".
- Comments carried over from the first rev8 back-check and still open: the C7-04 piece split (485 / 296 vs the certificate's 491 / 290, +12 screws); the 9/A-410 "#8 SCREWS … STUD TO TRACK" vs 8.A #10-16 conflict, now mentioned in RFI-51; menu-board FRT 60.61 vs 60.6 and restroom backing 17.78 vs 17.77 rounding; certificate observations O1, O3, O5, O7 and O8.
