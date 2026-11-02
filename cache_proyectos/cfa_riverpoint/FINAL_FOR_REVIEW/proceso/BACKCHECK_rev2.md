# Back-check of the rev2 corrections (step 11 verification) - CFA #2284 River Point, Sheridan, CO

Date: 2026-11-02. Scope: only the lines of `CAMBIOS_rev2.md` and the FAIL / GAP findings of `CERTIFICADO_AUDITORIA.md` / `COMPARATIVA_AUDITORIA.md` and `CERTIFICADO_PASO12.md`. Full audit not redone.
Sources: `cfa_work/plano/bidset_CLEAN_SIN_MARKUPS.pdf` (pymupdf text + vectors) and the rev2 deliverables (`Take-off/CFA2284_RiverPoint_Takeoff_FINAL_rev2.xlsx`, `Planos marcados/*_rev2.*`). No canon / reading / resolution files were opened.
Evidence crops (circled in red, reopened and checked): `/tmp/claude-0/-home-user-reading-plans/00739bfa-f4e4-5132-80c8-c9e8628b8f17/scratchpad/cfa_backcheck/*.png`. MS = Material Summary, PT = Partition Takeoff, SC = Scope Checklist.

## A. CAMBIOS_rev2.md lines

| # | Item | rev1 | rev2 | Check | Evidence | Result |
|---|---|---|---|---|---|---|
| 1 | C.R. channel bracing on M2.1 / M3.5 / MB-01 | 56.79 LF | 0 | A1/A-605 and A2/A-605 draw no C.R. channel. MS row 17 is now only the ceiling bridging (50.87 LF, A2/S-241). | A1+A2/A-605 p28 `a605_A1A2.png`; MS r17 | PASS |
| 2 | Wall braces 362S162-33 @ 48" | 0 | 16.96 LF, 7 pcs | D1/S-801 prints "brace @ 48" O.C. per sched. (alt sides)" at a 1:1 slope, schedule H <= 6'-0" = single 362S162-33. Pieces: M3.5-01 3, M3.5-02 2, MB-01 2. Lengths: (12.333 - 10.667) x 1.414 = 2.357 ft and (12.333 - 10.5) x 1.414 = 2.593 ft, giving 7.07 + 4.71 + 5.18 = 16.96. Note: the M3.5 braces rest on general note C.4/A-202 plus typical D1, not on a detail drawn at those walls. This is conservative (11.78 LF). | D1/S-801 p73 `s801_D1C1.png`; A-202 C.4 p13; MS r13 | PASS |
| 3 | 54 mil bent plates | 0 | 7 pcs | D1/S-801 "54 mil bent plate @ 48" O.C.": one per brace = 7. | `s801_D1C1.png`; MS r22 | PASS |
| 4 | L1-1/2x1-1/2x33 mil angle at MB-01 | 0 | 3.333 LF | C2/S-801 "L1 1/2" x 1 1/2" x 33 mil cont. angle". MB-01 is 3.333 LF. | C2/S-801 p73 `s801_C2.png`; MS r16 | PASS |
| 5 | Menu board blocking T&B | 3.333 LF | 6.666 LF | C2/S-801 "33 mil blkg. T&B": 2 x 3.333. MS r26 BLK-MENU = 6.67. | `s801_C2.png`; MS r26 | PASS |
| 6 | Soffit cross brace 362S162-33 @ 32" | 0 | 67.56 LF, 16 pcs | C4/A-624 and C3/S-801 print it at 32" O.C. and a 1:1 slope. Counts: SRV-W ROUNDUP(18.122/2.667)+1 = 8, SRV-N 4 (shared corner), GT 3+1 = 4, total 16. Length = width x 1.414: SRV-W 2.83 ft wide (EQ/EQ on A-221) gives 4.006 ft; SRV-N 2'-4" gives 3.30; GT 4'-0" gives 5.58 (-1.4 %). | C4/A-624 p33 `a624_C4.png`; C3/S-801 `s801_C3.png`; A-221 `a221_srv.png`; MS r13 | PASS |
| 7 | Play-bay ceiling 6" rim track | 0 | 29.77 LF | The A-221 PT-41 hatch fill vector is 53.1 x 215.3 pt = 2.95 x 11.96 ft, perimeter 29.82 LF (-0.2 %). The printed length 1'-11 3/4"+4'-0"+4'-0"+1'-11 3/4" = 11.96 ft. A3/S-241 rim. | A-221 p15 `a221_playbay.png`; MS r31 | PASS |
| 8 | MB-01 stud size | 3-5/8" | 6" @ 16" | D3/A-624 prints "2X6 wood framing or 6" metal framing at 16" O.C."; the metal option was taken. MS r5 / r7 6" track 3.33, r10 6" stud 42 = 4 x 10.5. PT r13 is 6". | D3/A-624 p33 `a624_D3.png` | PASS |
| 9 | Roof hatch shaft top runner | 24 LF std | 12 std + 12 slotted | C1/S-801 prints "3" long legged slotted cont. track to match stud depth" where the studs reach the trusses. A1/A-604 shaft runs to the roof hatch. MS r14 RH-SHAFT-T 12 and r23 RH-SHAFT-TT 12. | `s801_D1C1.png`; A1/A-604 p27 `a604_A1.png` | PASS |
| 10 | Gauge 33 mil vs S-902 0.0538" | no note | RFI-18 closed (A) | S-902 C05000-C 2.5.A.1 reads "Minimum base-metal thickness: 0.0538 inch"; S-801 prints 362S162-33. SC RFI-18 is CLOSED option A, and every framing row carries the note. | S-902 p75 `spec_S902_25.png` | PASS |
| 11 | Ceiling board product 332.06 SF | 5/8" regular | 5/8" sag-resistant | C09250 2.1.E "Ceiling Type" and 3.2.A.3 "Ceiling surfaces" confirmed. **But the MS r19 Material label still reads "5/8" gypsum board, regular".** The product is only in the I-column note (TOOL_LIMITS 10). The row that is bought contradicts its own note. | A-909 p45 `spec_C09250_2x.png`, `spec_C09250_3x.png`; MS r19 A-col | **FAIL** (label; 0 SF) |
| 12 | Restroom gyp above tile | 1/2" regular 148.02 | 1/2" MR 148.02 + RFI-21 | A-202 G.1 prints 1/2" gypsum board; C09250 2.2.A / 2.2.A.2 prints WR backing board with a 5/8" Type X core. So the plan thickness was loaded with the spec product. MS r20 = 69.96 + 78.06 = 148.02; r21 = 1583.66 - 148.02 + 16 = 1451.64. RFI-21 is closed (A). Citation A2/A-604 = "Tile to gyp transition at restroom" (valid). | A-202 p13; `spec_C09250_2x.png`; MS r20 / r21 | PASS |
| 13 | J-bead at menu board gyp edge | 0 | 13.683 LF | D3/A-624 "7'-0" A.F.F. bott. of gypsum bd." is an exposed edge; C09250 2.3.A.2.b LC-Bead. The length is the full menu wall: 2.617 + 7.733 + 3.333 = 13.683. | `a624_D3.png`; MS r28 | PASS |
| 14 | J trim at play area wall base | 0 | 59.69 LF | A2/A-624: the "J" trim sits on top of the 1/2" cement board on the **dining** face (tile floor / tile base side). The play side has 1/2" gyp, FRP and vinyl base, with no cement board (A1/A-624 confirms Dining / Play Area). 59.69 LF is the play-room inside perimeter (the Level 5 length). The dining face of the enclosure is EX-DIN-03 = 30.79 LF. | A2/A-624 `a624_A2.png`, A1/A-624 `a624_A1.png`; PT r30; MS r29 | **FAIL** (-28.90 LF net; 7 to 4 sticks) |
| 15 | Draftstop patch at beverage chases | n/a | 16 SF + RFI-20 | A-052 general note 9 "Patch existing draftstop wall between kitchen and service at new beverage chases". Allowance 2 x 2 x 2 x 2 = 16 SF is in MS r21 and in BREAKDOWN_half_inch_gyp_rev2.md. RFI-20 is in Pending. | A-052 p7 `a052_n9.png` | PASS |
| 16 | Demo of board under restroom cement board (DEMO-14) | 0 | 617.08 SF + RFI-19 | A-050 KN10 "Remove existing wall finishes" is tagged in Men's and Women's. 178.77 + 110.6 + 199.49 + 128.23 = 617.09 = MS r24 DEMO-14. | A-050 p6 `a050_kn10.png`, `a050_rr.png` | PASS |
| 17 | W6-04-KIT length | 2.317 | 2.229 | A-202 prints 2'-2 3/4" = 2.229. PT r84 2.23 x 1.5 x 2 = 6.69 SF; cement board 1800.53 - 0.26 = 1800.27 = MS r30. | A-202 p13 `a202_w604.png` | PASS |
| 18 | Strongback 362T125-54 own row | in track row | 26.51 LF own row | C3/S-801 "362T125-54 strongback ... to each truss @ 48" O.C." MS r15 = 26.51; r14 158.87 = 197.39 - 26.51 - 12. | `s801_C3.png`; MS r14 / r15 | PASS |
| 19 | RFI-17 | open | closed, 6" metal | D3/A-624 prints the framing. SC RFI-17 is CLOSED with its 3-5/8" and wood alternatives. | `a624_D3.png`; SC A52 | PASS |
| 20 | Kitchen base RFI ref | RFI-02 | RFI-03 | PT J36-J43 now read "RFI-03 (closed, estimator decision option A)". Pending RFI-02 is the M3.5 spacing only. | PT J36 | PASS |
| 21 | Roof hatch 3x3x1/4 clip angles | n/a | EXCLUDED | A1/A-604 "3"x3"x1/4" clip angle bolt to stud wall @ 48" O.C. & weld to mtl. bar" is misc. steel. SC ALC-E16. | `a604_A1.png` | PASS |
| 22 | K-001 note 6 Unistrut | n/a | EXCLUDED | K-001 (p118) note 6 "GC to provide Unistrut for suspended shelving and ... shrouds" is equipment / MEP. SC ALC-E17. | K-001 p118 text | PASS |
| 23 | Spec section on every framing / board row | missing | constants.ms_notes | Most rows carry "Spec: C09111 / C09250". **MS r17 (C.R. channel bridging), r22 (bent plates) and r27 (corner bead) carry no spec reference**, so the "every row" claim is not met. | MS r17 / r22 / r27 col I | **FAIL** (text) |
| 24 | Citations / internal codes | malformed | clean | Scan of the 6 visible sheets: no "R-ALC", "resolver", "PT00xx", ".png", "GA-216", "3/CT-73B" or "n/A-202" number-only citations. CT-73B now appears only as a finish tag ("WD-3 / CT-73B A-211"). | workbook scan | PASS |
| 25 | Bluebeam PDF format | see audit 7 | fixed | See section C. | rev2 PDF | PASS |
| 26a | Cement board mesh tape LF | 0 | 666.1 LF | 0.37 x 1800.27 = 666.10; C09250 2.4.B.2 / 2.4.D.2 / 3.5.E say "as recommended by manufacturer". | `spec_C09250_2x.png`, `spec_C09250_35E.png`; MS r25 | PASS |
| 26b | Mesh tape waste | - | 6 % (Inputs B6) | The value comes from a yield (Inputs B24), and Inputs C23 / C24 say "Yields carry no waste". The paper tape and compound rows use 0 %, but MS r25 applies 6 %. | MS r25 D-col | **FAIL** (purchase 706.07 vs 666.10 LF, +39.97 LF) |
| 26c | Setting-type compound at cement board | 0 | 129.62 lb (note only) | 0.072 x 1800.27 = 129.62 is correct, but it sits only in the r25 note. No quantity row exists, so it is not in Net / Purchase / Pieces to buy (TOOL_LIMITS 12). | MS r25 I-col | **FAIL** (+129.62 lb missing from the buy list) |
| 27 | Compound / tape driver note | unexplained | explained | MS r45 / r46 note: driver = gyp SF only; cement board in its own row. | MS r45 / r46 | PASS |
| 28 | 1/2" gyp breakdown | cut off | md file | BREAKDOWN_half_inch_gyp_rev2.md: 26 sources, total 1451.66 = NET 1451.64. | proceso md | PASS |
| 29 | Compound / tape after the MR change | 137.93 lb / 708.82 LF | 139.08 lb / 714.74 LF | Driver 1451.64 + 332.06 + 148.02 = 1931.72 SF. 0.072 x 1931.72 = 139.084 lb; 0.37 x 1931.72 = 714.736 LF. Both match MS r45 / r46 (J formulas =Inputs!B23*1931.72 and =Inputs!B24*1931.72). | MS r19-21, r45-46; Inputs B23 / B24 | PASS |
| 30 | MB-01 own type INFILL | merged | split | PT r12-14 TYPE INFILL with its own subtotal; r9 / r10 M3.5 are separate. | PT r9-15 | PASS |
| 31 | OTHER FRAMING subtotal | none | none (tool limit) | Audit (6) / COMPARATIVA #9 asked for a SUBTOTAL row (73.44 LF / 78.06 SF). PT r17-25 still has none. | PT r17-26 | **FAIL** (open) |
| 32 | Hidden sheet `_reglas` | present | kept | Audit (6) / COMPARATIVA #8 asked for 6 sheets. The workbook still has 7, and `_reglas` (hidden) is in Spanish ("reglas.py compuerta OK"). | workbook sheet list | **FAIL** (open) |
| 33 | Inputs C26 lumber note | other project | standing input | Inputs C26 now reads "estimator standing input; not used". | Inputs C26 | PASS |
| 34 | Demo vs new plan cross table | missing | DEMO_CRUCE.md | Present: 20 demo elements plus the 4 DEMO-14 parts, each against A-202. | proceso md | PASS |
| 35 | Review items wording | stale | MB-01 6"; M3.5 "A 8"" | Review Items D6 (4/8) and D8 (6/8) confirmed. | Review Items D6 / D8 | PASS |

## B. First-audit and step-12 FAIL / GAP findings not already covered above

| Ref | Finding | rev1 | rev2 | Check | Evidence | Result |
|---|---|---|---|---|---|---|
| Audit 3a / G-16 | Z-channel size | label 1-1/2" Z | label 1-1/2" Z + PRODUCT note 2" | A-202 M2.1 and A1/A-605 print **2" metal "Z" channel**. MS r8 Material label still reads "1-1/2" Z-furring channel" (TOOL_LIMITS 5 / 10). Only the note says 2". | A1/A-605 `a605_A1A2.png`; MS r8 A-col | **FAIL** (label; 96 LF unchanged) |
| Audit 3b / G-15 | Bracing citations | C09111 3.2.C / C2 as C.R. channel | removed | MS r17 cites A2/S-241 only. C09111 3.2.C ("Sway-brace suspension systems", p45) no longer supports wall bracing. | MS r17 | PASS |
| Audit 3c / G-03 | Ceiling board type | regular | label regular | Same as line 11. | MS r19 | FAIL (counted in line 11) |
| Audit 3d / BE-102 | Malformed citations | 3/CT-73B, 2/A-202 ... | removed | Same as line 24. | scan | PASS |
| Audit 4 / G-06..G-09 | Cross brace, MB-01 kicker, angle, T&B blocking | missing | loaded | Lines 2-6. | - | PASS |
| Audit 4 obs / COMP #16 | J trim A2/A-624 | 0 | 59.69 | Same as line 14 (wrong face / LF). | - | FAIL (counted in line 14) |
| Audit 4 obs / COMP #17 | Restroom KN10 board removal | 0 | 617.08 + RFI-19 | Same as line 16. | - | PASS |
| Audit 5 / COMP #6 | Row 9 merged M3.5-01 + MB-01 | merged | split | Line 30. MB-01 stays at H 10.5 (C.1 = 10.667, -1.6 %, within tolerance). | PT r9, r13 | PASS |
| Audit 5 / COMP #7 / G-18 | 1/2" gyp traceability | 100 SF untraced | soffit bottoms 68.04 + 32.00 listed | BREAKDOWN md and Bluebeam SOFFIT BOTTOM polygons give 100.04 SF. | md; PDF p15 | PASS |
| Audit 6 | 7 sheets / OTHER FRAMING subtotal | open | open | Lines 31 and 32. | - | FAIL (counted in lines 31-32) |
| Audit 6 / COMP #10 | RFI-02 cross-ref; Review 6/8 "A 3-5/8"" | wrong | fixed | Lines 20 and 35. | - | PASS |
| G-01 | A-052 note 9 draftstop patch | GAP | loaded + RFI-20 | Line 15. | - | PASS |
| G-02 | WR backing board | GAP | 1/2" MR + RFI-21 | Line 12. | - | PASS |
| G-04 | Cement board joint treatment | GAP | mesh tape row + compound note | Lines 26a-26c. | - | FAIL (tape LF passes; compound and waste counted in 26b / 26c) |
| G-05 | Menu board LC / J-bead | GAP | 13.68 LF | Line 13. | - | PASS |
| G-10 | Hatch clip angles | GAP | EXCLUDED | Line 21. | - | PASS |
| G-11 | S-902 gauge | GAP | RFI-18 closed | Line 10. | - | PASS |
| G-12 | MB-01 printed framing | GAP | 6" metal | Line 8. | - | PASS |
| G-13 | K-001 Unistrut | GAP | EXCLUDED | Line 22. | - | PASS |
| G-14 | Play-bay rim track | GAP | 29.77 LF | Line 7. | - | PASS |
| G-17 | MS row 12 mixed products | mixed | split r14 / r15 / r16 / r23 | Line 18. | - | PASS |
| Prop. FAIL | Compound / tape driver; bracing vs walls; rim vs ceilings | FAIL | fixed | Lines 1, 7, 27 and 29. | - | PASS |
| BE-14 | "not printed" claims (ALC-08, RFI-17, MS r38) | contradicted | ALC-08, RFI-17, MS r48 fixed | **SC ALC-04 still says "3-5/8" MB-01; standard top track, no deflection track printed"**, which contradicts lines 8 and 9 (6" MB-01; C1/S-801 slotted track loaded). PT J50 / J54 (MR rows) also still cite "C09250 §2.1.B (1/2 in standard interior)" next to 2.2.A. | SC D5; PT J50 / J54 | **FAIL** (text) |
| BE-12 / BE-106 | Inputs C26 other-project precedent | yes | removed | Line 33. | - | PASS |
| BE-55 | Internal codes in client text | yes | removed | Line 24. | - | PASS |
| VS-08 | Demo cross table | missing | present | Line 34. | - | PASS |

## C. Re-check of audit items (6) format and (7) Bluebeam on the rev2 files

| Check | Result | Evidence |
|---|---|---|
| (6) Visible sheets in English, schedule order M2.1 / M3.5 / INFILL / other / board only, per-type subtotals for partition types, grand total | PASS | PT r5-r15, r103 |
| (6) Exactly 6 sheets, no hidden Spanish sheet | **FAIL** | `_reglas` hidden (line 32) |
| (6) OTHER FRAMING block subtotal | **FAIL** | line 31 |
| (7) Page labels A-050 / A-052 / A-202 / A-221 on the marked pages (+ LEGEND p173) | PASS | rev2 PDF pages 6 / 7 / 13 / 15 |
| (7) English only in Subject / Contents (no DERIVADO / PENDIENTE / Spanish words) | PASS | 0 hits over 126 annotations |
| (7) One markup per element: 4 metal walls (MB-01 Subject INFILL), 8 soffit sides, 75 board-only, 20 demo elements (DEMO-14 split into its 4 rows), each wall PolyLine with Subject + /Measure + /Depth = height | PASS | 83 + 12 + 7 + 8 PolyLines; DEMO-C1..C6 are area items (Depth n/a, as in rev1) |
| (7) Metal-wall markup SF vs Excel board SF | PASS | Contents = LF x H; the legend page states it is framing SF and lists the Excel board SF (148.75 / 75.03 / 39.38 / 46.67 ...) |
| (7) Polygons for 5 gyp ceilings (332.06 SF), 2 soffit bottoms (100.04 SF), Level 5 (731.2 SF), hatch shaft, 2 pin and sleeve recesses | PASS | p15: 9 Polygons; p13: 2 Polygons, all with /Measure. Observation: the A-221 rev2 PNG shows only the soffit sides, not the ceiling or Level 5 areas (TOOL_LIMITS 7). |

## D. Recomputations

- Joint compound: Inputs B23 0.072 lb/SF x (1451.64 + 332.06 + 148.02 = 1931.72 SF) = **139.08 lb**, which matches MS r45. PASS.
- Joint tape: Inputs B24 0.37 LF/SF x 1931.72 = **714.74 LF**, which matches MS r46. PASS.
- For reference, the same yields on 1800.27 SF of cement board give 666.10 LF of mesh tape (r25) and 129.62 lb of setting compound (note only).

## Summary

Lines checked: 71 (37 in A: the 35 CAMBIOS lines with line 26 split into 3; 26 in B; 8 in C). The compound and tape recomputations in D also pass (line 29). **PASS 56, FAIL 15.** The 15 failures are 6 unique defects; the other rows repeat them.

Unique failures and deltas:
1. **J trim A2/A-624 (line 14)**: loaded on the play-room perimeter, 59.69 LF. It belongs on the dining face of the enclosure (EX-DIN-03), 30.79 LF. Delta -28.90 LF; purchase 7 to 4 sticks.
2. **Cement board setting-type compound (line 26c)**: 129.62 lb is only a note. +129.62 lb is missing from the quantity and purchase columns.
3. **Mesh tape waste (line 26b)**: 6 % applied to a yield-based row, against the "Yields carry no waste" rule. Purchase 706.07 to 666.10 LF (-39.97 LF).
4. **Row labels contradict the product (line 11 / audit 3c, audit 3a / G-16)**: MS r19 "5/8" gypsum board, regular" should read sag-resistant ceiling board (332.06 SF); MS r8 "1-1/2" Z-furring" should read 2" Z channel (96 LF). Label only, 0 quantity.
5. **Format (lines 31, 32; C)**: the hidden Spanish `_reglas` sheet is still there (7 sheets), and the OTHER FRAMING block still has no subtotal (73.44 LF / 78.06 SF).
6. **Stale or incomplete text (line 23; BE-14)**: SC ALC-04 still says MB-01 is 3-5/8" and that no deflection track is printed. PT J50 / J54 cite §2.1.B standard board on the MR rows. MS r17 / r22 / r27 have no spec reference.

BACK-CHECK RESULT: FAIL - (1) J trim -28.90 LF; (2) setting compound +129.62 lb not in a quantity row; (3) mesh tape waste +39.97 LF purchase; (4) MS r19 / r8 labels (5/8" "regular", 1-1/2" Z); (5) `_reglas` sheet + no OTHER FRAMING subtotal; (6) stale text ALC-04, PT J50 / J54, missing spec refs MS r17 / r22 / r27.
