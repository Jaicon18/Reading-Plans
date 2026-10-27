# BACKCHECK rev5 - Barnes & Noble, Colorado Springs - metal frame & drywall take-off

VERDICT: PASS WITH COMMENTS

- Date: 2026-10-27. Independent back-check of `Barnes_Noble_ColoradoSprings_Takeoff_FINAL_rev5.xlsx` against rev4, the rev4 audit (`AUDITORIA_rev4/`, column "Recommendation") and the bid set without markups (A-221 p.15 @ 36 pt/ft, A-121 p.8, sections 3/A-221).
- Method: openpyxl (data_only) diff of every Material Summary Net value (rev4 -> rev5). Each delta was recomputed from plan dimensions. The 6'-2" opening and the 7 1/4" end faces were measured on the A-221 vectors. Every breakdown string was summed by script. Every source cell was scanned for N/SHEET and for internal file names. Images were checked visually.
- Result: all 9 requested items are applied, and every delta reconciles to the cent (within 0.01 rounding). No item fails. The 7 comments below are mostly about traceability and conservatism. One is a possible scope under-count, in comment C1.

## Material Summary Net diff rev4 -> rev5 (all rows that changed)

| Row | rev4 | rev5 | Delta | Reconciliation |
|---|---|---|---|---|
| 6" metal stud LF | 2,900.00 | 3,007.50 | +107.50 | SS-GG 6 x 17.917 |
| 3-5/8" metal stud LF | 10,778.08 | 10,788.75 | +10.67 | WH backing 8.0 + steel blocking 2.67 (RFI-32) |
| Track, ceilings / soffits | 321.78 | 564.25 | +242.47 | SS-GG 12.33 + fire-stop 142.74 + 87.40 |
| Bracing C.R. | 2,858.98 | 2,883.65 | +24.67 | SS-GG 4 rows x 6.167 |
| 5/8" Type X | 15,579.48 | 14,902.61 | -676.87 | -122.30 ceilings -570.36 Work Room +3.73 soffit bottom +12.06 end faces = -676.87 |
| 5/8" Type X W.R. | 1,020.33 | 1,713.00 | +692.67 | 122.30 + 570.36 = 692.66 (rounding 0.01) |
| 5/8" FRT plywood | 2,709.63 | 2,838.21 | +128.58 | SS-GG 110.49 + end faces 2 x 9.045 = 128.58 |
| 3/4" FRT plywood | 353.46 | 370.46 | +17.00 | Janitor 11/A-200 |
| Additional head track | 0 | 10.67 | +10.67 | doors 3 + 11, 2 x 5.33 |
| Drywall screws | 19,919.77 | 19,938.73 | +18.96 | 1.2 x 15.80 SF new board (16,615.6 SF total) |
| Framing screws | 3,100 | 3,124 | +24 | 4 x 6 SS-GG stud pieces (775 -> 781) |
| Joint compound / tape | 1,195.19 / 6,141.93 | 1,196.32 / 6,147.78 | +1.13 / +5.85 | 0.072 and 0.37 x 15.80 SF |

No other row changed. Cross tee 457.96, curved walls, hanger wire and cement board are unchanged.

## Item-by-item verification

| # | Item | Expected | Found in rev5 | Result |
|---|---|---|---|---|
| 1 | Restroom GWB ceilings 108/109 -> Type X W.R. | about 120.2 SF moved from X to W.R. (A-410 Partition Notes 2) | 61.19 + 61.11 = 122.30 SF moved (RCP area, no chase notch deducted, +2.10 SF documented in RFI-11) | PASS |
| 2 | Janitor 11/A-200 3/4" FRT plywood | +17.0 SF, RFI | JANITOR-FRT-11-A200 17.0 SF (2.125 x 8.0); RFI-33 with delta down to 0 | PASS |
| 3 | Grab & Go soffit 3/A-221 | 6'-2" x 17.917; studs about 107.5 LF; track about 12.33; FRT about 110.5; GWB bottom 3.73; RFI-20 closed; T.O. WD-1 RFI | Vector check: opening 222.12 pt / 36 = 6.170 ft (6'-2"). Height 25.0 - 7.083 = 17.917. Studs ROUNDUP(74/16)+1 = 6 x 17.917 = 107.50. Track 2 x 6.167 = 12.33. FRT 6.167 x 17.917 = 110.49. Bottom GWB 6.167 x 0.604 = 3.73. Bracing ROUNDUP(17.917x12/48)-1 = 4 rows = 24.67. RFI-20 CLOSED, RFI-34 open | PASS (comments C2, C6) |
| 4 | 8/A-410 fire-stop track | +230.14 LF | FIRESTOP-TRACK-3 142.74 = W2-04 56.76 + W2-05 12.92 + W2-06 27.54 + W2-07 7.51 + W2-08 12.92 + W2-09 12.92 + C-H2a 12.17. FIRESTOP-TRACK-6 87.40 = W5-01 5.70 + C-H1-N 29.98 + C-H1-W 12.17 + C-E2 29.30 + C-H3a 4.08 + C-H3b 6.17. Total 230.14. RFI-35 | PASS (comment C1) |
| 5 | Type I end faces "I SIM." | +1.21 LF, FRT 15 ft, GWB 10 ft, no framing | C-I-E1 / C-I-E2 0.603 LF each = +1.206 LF (vector: 21.72 pt / 36 = 0.603 ft = 7.24"). FRT 2 x 9.04, GWB 2 x 6.03. No C-I-E entries in the stud / track / bracing breakdowns. Located at the east (Sales) ends of C-H3a and C-H1-N on both images | PASS |
| 6 | Cafe Work Room 104 -> W.R. | about 570 SF | C-H1-N B 29.98 x 10.5 = 314.79; C-H1-W B 12.17 x 10.5 = 127.78; C-H2a A 12.17 x 10.5 = 127.78. Total 570.36 | PASS |
| 7a | Water heater backing P-201 | RFI + conservative delta | RFI-32: 8.0 + 2.67 LF carried in the 3-5/8" stud row; delta -10.67 | PASS |
| 7b | Additional head track | doors 3 and 11, citation corrected | RFI-31: 10.67 LF (R.O. 4.00 + 2 x 8"), auditor 11.17 alternative stated (+0.50); note declared NOT on A-410 / A-500 | PASS (comment C7) |
| 7c | FRP RFI-13 / Corridor 110 tile in RFI-12 | kept / added with delta | RFI-13 kept (54.32 + 19.43 LF x height); RFI-12 adds Corridor 110 tile, 93.44 SF per ft of height | PASS |
| 7d | W-3 blocking | RFI | RFI-36, delta pending the A-111 count | PASS |
| 8a | MS "Where it comes from" = N/SHEET, no internal files | 0 rows citing .json / .py | 44/44 rows start with N/SHEET; 0 .json / .py in MS (rev4: 39 rows). Internal tool labels remain (C4) | PASS (comment C4) |
| 8b | Breakdowns sum to Net | 3-5/8", 6" stud, 5/8" FRT | 3-5/8" 10,788.75 = Net exactly; 6" 3,007.5 = Net exactly; 5/8" FRT sums to 2,838.18 vs Net 2,838.21 (-0.03 rounding) | PASS (comment C3) |
| 8c | Per-face heights where Board differs from L x H x Layers | all such rows | 21 rows differ; 21/21 carry "Board by face" and their faces re-sum (e.g. W2-03 2,356 + 2,028 + 124.64 = 4,508.64; C-H1-N 647.5 + 30.93 + 314.79 = 993.22) | PASS |
| 8d | Scope Checklist ALC-04/06/07/08/10/11/12/13/15/16 | current figures, closed RFIs | All match the MS (14,902.61 / 1,713.00 / 2,883.65 / 2,838.21 / 370.46 / 981.38 = 859.08 + 122.30); ALC-06 cites 8/A-410; RFI-15, RFI-17 and RFI-20 shown CLOSED | PASS |
| 8e | C-E1-P.1 -> C-I-P.1 | renamed | "C-E1-P.1" is found nowhere in the workbook; C-I-P.1 appears in the Partition Takeoff, the MS breakdowns and the A-221 images | PASS |
| 9 | No change: curved walls 25.68, insulation, cross tee | unchanged; partition total 569.82 | W4-29/30 chords sum to 25.68 each; ALC-X25 excluded; cross tee 457.96; partition total 569.816 (568.61 + 1.206); type I subtotal 4.516 | PASS |

## Comments (none blocks the bid; fix in rev6 or accept)

- **C1 - Fire-stop list applies its own criterion inconsistently (possible under-count of about 38.5 LF).** RFI-35 says the track goes on "every full-height wall with a ceiling on at least one face". By that rule these walls are missing:
  - W2-03: its B face in Corridor 110 (13.12 LF, ACT 9'-0" on A-121) is carried at 9.5 ft.
  - C-H2b: a stub inside Workroom 104 (ACT-1 10'-0"), 1.95 LF.
  - C-E1-S: the Cafe "GWB 9'-0"" band on A-121 runs along the south wall, 23.46 LF (6"). The same may apply to the C-E1-B / C-F / C-I box faces.

  Rev5 copied the auditor's list exactly, so item 4 passes as requested. Add these walls to the list or to the RFI-35 delta: +15.07 LF of 3-5/8" and +23.46 LF of 6".
- **C2 - 3/A-221 section build-up.** The section shows the 5/8" FRT plywood substrate running the full face height, with 5/8" GWB OVER it above T.O. WD-1 and WD-1 below. Rev5 carries plywood on the full face, which is correct and conservative. However, RFI-34 describes the unknown as a swap ("plywood -> GWB 6.17 SF per ft"). From the section, it is an addition: +6.17 SF of 5/8" Type X per ft of face above T.O. WD-1, and the plywood stays. Reword the RFI-34 delta.
- **C3 - Breakdown rounding.** Some stated breakdown totals differ from Net by 0.02-0.06:
  - Type X 14,902.55 vs 14,902.61
  - W.R. 1,712.98 vs 1,713.00
  - Cement board 851.38 vs 851.40
  - 5/8" FRT 2,838.18 vs 2,838.21

  The terms are rounded to 2 decimals while Net uses full precision. Suggest showing 3 decimals, or printing "= Net (rounding)".
- **C4 - Internal tool names still visible.**
  - The MS USG rows (4) start their note with "usg_grid:".
  - The MS "Stud reinforcement" row cites "mep.registro" and has an empty "( rule)" where a file name was stripped.
  - Pending Items RFI-ACC-stud-reinforcement-mep still says "(mep.py rule)".
  - No .json / .py remains in the MS.
- **C5 - Stale text.**
  - The RFI-08 "Applied" line still says type I = 3.31 LF / 49.65 SF FRT / 33.1 SF GWB. Rev5 is 4.516 LF / 67.74 SF / 45.16 SF including the I SIM. end faces.
  - ALC-16 says restroom backing 17.78, while the MS shows 17.77.
  - The A-221 image title is still dated 2026-10-24.
- **C6 - SS-GG track size.** The 12.33 LF of SS-GG track for 6" studs went into the generic "Track, ceilings / soffits / canopy" row. That row is unsized and mostly 3-5/8" (the fire-stop track in it is split by size). Flag the 6" share so purchasing buys 6" track: 12.33 + 87.40 = 99.73 LF of 6".
- **C7 - Head-track citation.** The MS row cites "N/SHEET: A-410, A-500", while RFI-31 says the note is not on A-410 / A-500. Cite "A-500 door schedule (doors 3, 11) - [RFI-31]" so it does not read as a plan requirement.

## Images

- `7_imagenes/A-221_partitions_by_type.png`:
  - C-I-E1 sits at the east end of C-H3a and C-I-E2 at the east end of C-H1-N, which matches the circled I SIM. tags in the audit image C1.
  - SS-GG is drawn on the dashed "SOFFIT ABOVE" line spanning the 6'-2" HOLD opening.
  - C-I-P.1 is labelled correctly.
  - The legend "OTHER FRAMING 65.31 LF" = 22.77 + 10.12 + 20 + 6.25 + 6.167 is correct.
- `planmark/A-221_type_I.png`: the four type I markups (C-I-E1 0.60, C-I-E2 0.60, C-I-P.1 1.00, C-I 2.31) are at the correct locations.

## Resolution of the back-check comments (applied after this report, same rev5)
| Comment | Resolution |
|---|---|
| Fire stop track under-count (W2-03, C-H2b, C-E1-S) | Applied with the same rule, ceiling extent only: W2-03 Corridor 110 face 13.12 + C-H2b 1.95 (Cafe Workroom ACT) + C-E1-S 19.0 (Cafe 9'-0" GWB band, 1/A-121) = +34.07 LF; 8/A-410 total 264.21 LF (3-5/8" 157.81 + 6" 106.40); ceiling / soffit track 564.25 -> 598.32 LF; RFI-35 updated |
| RFI-34 delta wording | Rewritten: GWB is added over the full-height plywood above T.O. WD-1 (+6.17 SF GWB per ft), plywood stays |
| Internal tool names in text | "usg_grid", "mep.registro", "mep.py" removed from Material Summary and Pending Items |
| RFI-08 stale | Delta now 4.52 LF x 15.0 = 67.74 SF FRT + 45.16 SF GWB (incl. end faces) |
| Head track row cites A-410 / A-500 | Source now reads "note not printed in the set; doors 3 and 11 per the A-500 door schedule" |
| Rounding 0.02-0.06 in breakdowns | Accepted (each item rounded to 0.01; the check tolerance is 0.05 + 1e-6 x Net) |
| 6" soffit track in an unsized row | Kept: the ceiling / soffit track row is one row by template (sizes listed in its breakdown) |
