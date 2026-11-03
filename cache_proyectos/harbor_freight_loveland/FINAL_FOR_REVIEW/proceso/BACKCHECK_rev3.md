# BACK-CHECK rev1 - Harbor Freight Tools, Loveland CO (job 26041, issue 10/07/26)

Deliverables reviewed: `FINAL/Take-off/HFT_Loveland_Takeoff_FINAL_rev1.xlsx`, `FINAL/Planos marcados/HFT_Loveland_markups_rev1.pdf` (+4 PNG).
Method: I re-measured blind from the clean bid set first. My numbers are frozen in `backcheck/blind.txt`, written before I opened the deliverable. Then I compared three ways. I did not read etapas/2_lectura, 3_revision, 4_canon or the subagent notes.
Evidence crops are in `backcheck/img/`. Circled crops are named F*/O*/P*.

## 1. Three-way comparison (mine / Excel / printed)

| Item | Blind (mine) | Excel | Printed basis | Result |
|---|---|---|---|---|
| Type A LF | 148.4 | 145.72 | A1.1 11'-6 1/2", 12'-7 1/2", 13'-3", 12'-11"; A4.0 20'-8", 16'-4" (6'-3 1/2"+4'-0"+6'-0 1/2" = 16'-4", closes) | PASS (-1.8 %, I used overall dimensions and Excel used clear lengths) |
| Type B LF | 33.3 | 32.04 | A1.1 tag in the Mgr office; A4.0 B tags at the north wall of the BR and RR2 | PASS |
| Type C LF | 11.5 (one C tag) | 23.22 (C-01 north + C-02 east, Support Office) | A1.1: one C tag in Support Office 103, with an inner line drawn on both the N and E walls | PASS with OBS-3 |
| Type D LF | ~240.9 | 239.12 | ±209'-1" V.I.F. (A1.1). Riser room W wall = 18'-7 1/2". 6'-1 1/2" N/S walls (Excel uses the 5.70 clear between faces, which I verified from the vector) | PASS |
| Type E LF | 139.42 + 31.0 gross | 139.42 + 13.54 + 3.67 = 156.63 | 139'-5" "EXTENT OF WALL TYPE E @ 16'-0" A.F.F." (A1.1). The south chain 13'-6 1/2"+13'-9 1/2"+±3'-8" closes to ±74'-0 1/2". Excel leaves out the 13'-9 1/2" storefront/vestibule bay | PASS |
| Vestibule bulkhead LF | ~34.5 | 31.63 | 1/A5.3, A1.1 / A5.2: 13'-9 1/2" + 2 x 8'-11" | PASS |
| Receiving enclosure LF | ~42 (shear-wall segments only) | 59.33 (3 x ~20', openings framed with H-1/H-2) | S2.1 20'-0" x 20'-0", 19'-8", 19'-10", 600S162-54 @ 16" | PASS |
| Heights A | 18'-3" HP / 17'-4" LP | 18.04 / 18.25 / 17.46; A-15 8.5 | A1.2 clearance chart (sales B.O. deck ±18'-3"/±17'-4"); A/A4.1 "stop studs 6" above ceiling between toilet rooms" | PASS |
| Height D | 18'-2" | 18.17 | D/A4.1 "1" below deck", 10/A4.1 | PASS |
| Height E | 16'-0" W / deck S | 16.0 / 18.25 | E/A4.1 notes | PASS |
| Heights B / C | 8'-6" | 8.5 | B, C/A4.1 printed 8'-6" | PASS |
| Board 5/8 X | 240.9 x 18.17 x 2 = 8,754 | 8,689.6 | D/A4.1 both sides, no openings deducted | PASS (-0.7 %) |
| Board regular + MR | ~6,470 (board taken only to 8'-6" on the open-to-structure faces) | 6,994 | A/A4.1 "GYP. BD. CONTINUES TO DECK IF SUSPENDED CEILING DOES NOT OCCUR". Excel applies this correctly to the sales-side faces | PASS (Excel is right) |
| Studs | 16" O.C. on every type | 16" O.C. on every type; D-01 158 studs (209.1 x 0.75 + 1) | A-D/A4.1, S2.1 | PASS |
| Std vs slip track | slip at D and at the vestibule bulkhead | slip row = D only (239.12) | 10/A4.1; 3/A5.3 called at the head of 1/A5.3 | FAIL (F3) |
| Hat channel | 170.4 LF of wall @ 24" | 1,393.75 LF material (E-01 1,193; E-02 146; E-03 54.75) | E/A4.1 | PASS |
| FRP | RR 107/108 to ceiling | 583 SF (2 x 33.1 LF x 8') | A1.3 WC-1 "FRP to ceiling" | PASS |
| Demo SF | none printed for walls (D1.0 207/209/211 give extents only) | 11,412 SF derived | D1.0 | PASS (derived; OBS-5) |
| Headers | 2/A5.1, 5/A5.1, 2/A5.3, 8/A5.3, S2.1 H-1/H-2 | 618.56 LF | same | PASS (OBS-1 citation) |
| Control joints 30' max | D-01 6 per face, E-01 4 | 218 + 64 = 282 LF | 7/A4.1, 9/A4.1, A4.1 note 6 | PASS |
| CRC bracing (A4.1 note 7, walls > 12') | A + D + RE walls | 916.94 LF, which also includes B, C and A-15 (8'-6" walls) | A4.1 note 7 | FAIL (F4) |
| Bracing to structure @ 4'-0" (A1.1 note 1, 2/A4.1) | required | 0. RI-08 says "NOT in the Material Summary" | A1.1 wall legend note 1; 2/A4.1 | FAIL (F1) |
| Gyp shelf 1/A4.1 / A2.0 | required | MR board + 6.1 LF joists + 5.2 LF track | 1/A4.1 | PASS |

## 2. Standing-rule checks

| # | Check | Result | Evidence |
|---|---|---|---|
| R1 | Exactly 6 sheets, named and ordered correctly | PASS | Inputs, Partition Takeoff, Material Summary, Pending Items, Review Items, Scope Checklist |
| R2 | Types in schedule order A,B,C,D,E with a SUBTOTAL per type + GRAND TOTAL | PASS | rows 19/24/27/33/38/43 + 44. See OBS-2 on the bulkhead rows below the total |
| R3 | Project data rows in Inputs | PASS | Inputs A32:C49. See OBS-4 on B13 |
| R4 | Every Material Summary row cites N/SHEET and has a breakdown that sums to NET | FAIL (F5) | Row 20 Sill track has no breakdown. Rows 18/19/23 are off by 0.01-0.03 (OBS-6) |
| R5 | Two track families on separate rows | FAIL (F3) | the vestibule-head track (3/A5.3 slip) is not in the slip family |
| R6 | Fasteners EXCLUDED at 0 | PASS | rows 34, 36-39, 44, 45 |
| R7 | ACT / insulation / paint / MEP / wood / ducts EXCLUDED notes | PASS | Scope ALC-E01, E03, E04, E06, E07, E10, X43 |
| R8 | RFIs with (A) drawings, (B) code, (C) other + conservative value loaded | PASS | RFI-01..04 all have A/B/C and a "loaded" value |
| R9 | Nothing printed left uncarried (R-ALC-11) | FAIL (F1). OBS-7 also applies | A1.1 note 1 + 2/A4.1 bracing; A0.2 "existing gypsum board repaired" |
| R10 | No internal file names or Spanish words in the Excel or markups | FAIL (F2) | Review Items D6 "DISCREPANCIA"; D10 "TOOL_LIMITS_CALC #4", "misc_info BR-01" |
| R11 | No other project's sheet names | PASS (OBS-1) | "T162" in row 19 is a member (T162-54 track, A5.3), not a sheet |
| R12 | Markups: Subject = type, Page Label = sheet, Depth = height | PASS | Every annotation on D1.0 / A1.1 / A4.0 / S2.1 checks out, e.g. D-01 Depth 18.17 |
| R13 | Markup contents TYPE·LF·H·SF·DETAIL·ID equal to the Excel | FAIL (F6) | Excel merges A-14+A-12+A-13 and C-01+C-02 into single rows; the markups carry them as separate walls |
| R14 | /Measure at the printed scale | PASS | A1.1 / D1.0 3/32" (sheet prints 3/32"); A4.0 3/8"; S2.1 1/4" |
| R15 | Dimension chains close | PASS | A1.1 E-side 11'-6 1/2"+12'-11"+18'-7 1/2"+13'-6 1/2"+13'-9 1/2"+3'-8" = 74'-0 1/2" (±74'-0 1/2"). A4.0 6'-3 1/2"+4'-0"+6'-0 1/2" = 16'-4". A1.1 12'-7 1/2"+13'-3" = 25'-10 1/2" vs 25'-10" (1/2" difference, OK) |

## 3. Findings

**F1 - MUST-FIX (printed item missing).** Material Summary has no row for this, and Review Items D10 / RI-08 records it as quantity 0.
- What is wrong: lateral bracing to structure is not carried. The printed requirement is 1-1/2" bracing studs to structure plus a Spazzer 9200 spacing bar at the mid-point between the end of the board and the deck, at unsheathed flanges.
- Printed evidence: A1.1 wall legend note 1 "ALL WALLS BRACED TO STRUCTURE ABOVE @ 4'-0" O.C. MAX." (img/F1_A1.1_note1_bracing.png). 2/A4.1 "LATERAL BRACING @ FREE-STANDING WALLS - metal stud 5'-0" O.C. max, Trade Ready Spazzer 9200 spacing bar" (img/F1_A4.1_det2_bracing.png).
- Correct value (conservative): every A wall with studs to deck except A-04 (both faces boarded to deck) and A-15 (stops at 8'-6"):
  - Spazzer bar: 125.97 LF.
  - Brace studs @ 4'-0" (the stricter A1.1 spacing): 4+8+4+5+7+6+2+2+3+2+2+2+3 = 50 pcs, about 6.5 ft each = about 325 LF of 6" stud. The brace length is not printed, so it needs an RFI.
  - Minimum (walls with ceilings on both faces only, A-07/A-08/A-09 = 22.53 LF): 10 braces, 22.53 LF of bar.
- Delta: +126 LF Spazzer, +50 braces (about +325 LF of 6" stud).

**F2 - MUST-FIX (format).** Review Items D6 and D10 (also D3-D9 wording).
- What is wrong: a Spanish word and internal process names.
  - D6: "tool warning DISCREPANCIA".
  - D10: "misc_info BR-01", "no take-off family in the take-off programs", "TOOL_LIMITS_CALC #4". TOOL_LIMITS_CALC is an internal file name (FINAL/proceso/TOOL_LIMITS_CALC.md).
  - D7/D8: "TOOL LIMIT", "tool rule #20".
  - D4-D9: "resolution crop R.. (review folder)".
- Correct value: plain English with the drawing references only.
- Delta: none on quantities.

**F3 - MUST-FIX (track family).** Material Summary rows 7, 8 and 12.
- What is wrong: the 31.63 LF of top track for the vestibule bulkhead (VH-01..03) sits in row 12, "Top track - roof step and heads", which is neither the slip family nor clearly the standard family. The detail that applies is a slip track.
- Printed evidence: 1/A5.3 calls 3/A5.3 at the stud head at "LINE OF STRUCTURE". 3/A5.3 is the "TYPICAL SLIP TRACK DETAIL - slip track runner, steel stud cut 1" short of deck" (img/F3_A5.3_det1_bulkhead.png, img/F3_A5.3_det3_sliptrack.png).
- Correct value: slip/deflection track 3-5/8" = 31.63 LF on its own slip-family row. The standard / roof-step top track for VH drops to 0.
- Delta: slip +31.63 LF; standard -31.63 LF.

**F4 - MUST-FIX (wrong number).** Material Summary row 18 (CRC bracing).
- What is wrong: the row includes walls that are only 8'-6" high (B-01..03 32.04, C-01..02 23.22, A-15 6.83). The breakdown text also states "ROUNDUP(H x 12 / 48) - 1", but the values are computed on 96" (e.g. D-01 = 2 rows x 209.1 = 418.2).
- Printed evidence: A4.1 wall type note 7 "AT PARTITIONS HIGHER THAN 12'-0" provide horizontal lateral bracing with 1-1/2" 16 GA C.R. channels at 8'-0" O.C. vert." (img/F4_A4.1_note7.png).
- Correct value: 916.94 - 62.09 = 854.85 LF, with the breakdown text corrected to /96.
- Delta: -62.09 LF.

**F5 - MUST-FIX (format).** Material Summary I20 (Sill track, 10.67 LF).
- What is wrong: the row cites only "N/SHEET: 5/A5.1" and has no breakdown summing to NET.
- Correct value: the breakdown per window, 306-W1 + 306-W2 = (4.0 + 1.333) x 2 = 10.67 LF.
- Delta: 0.

**F6 - MUST-FIX (markups vs Excel).** Partition Takeoff rows 17 (A-14+A-12+A-13, 12.04 LF / 312.56 SF) and 26 (C-01+C-02, 23.216 LF / 197.34 SF).
- What is wrong: the markups carry these as separate walls, and the Excel has no row matching their contents:
  - A-12 4.00 LF / 103.84 SF, A-13 2.61 / 67.75, A-14 5.43 / 140.97.
  - C-01 12.28 / 104.38, C-02 10.94 / 92.96.
- Correct value: one Excel row per wall ID, matching the markup Contents.
- Delta: 0 on totals.

**OBS-1.** Material Summary I19 lists "T162" and "D1.0" in N/SHEET. T162 is the "T162-54 TRACK" member on A5.3, not a sheet, so cite it as x/A5.3. D1.0 has no header detail.

**OBS-2.** The vestibule bulkhead rows (Other Framing, 31.63 LF / 290.05 SF) sit below the GRAND TOTAL, which is 656.06 LF. The markup legend total is 687.69 LF. Either include them in the grand total or label the grand total "partitions only".

**OBS-3.** Type C appears as one tag only (Support Office 103, A1.1). C-02 (10.94 LF, inside the D demising wall) is supported by the inner line drawn on the plan. Confirm it is intended, or treat it as B like the Mgr office. If it is not intended, the delta is -10.94 LF / -93 SF.

**OBS-4.** Inputs B13 "B.O. Deck" shows "n/a", but A1.2 prints a clearance chart: sales ±18'-3" / ±17'-4"; sales replenishment ±17'-4" / ±16'-11"; B.O. structure ±16'-9" / ±15'-9 1/2" / ±15'-5" (img/P_A1.2_clearance_chart.png). Load these as project data.

**OBS-5.** Demo 11,412 SF is fully derived. D1.0 prints no wall SF. The markup Contents say "2 layer(s)" where the row means 2 faces x 1 layer (RFI-02 option A). Reword it as "2 faces".

**OBS-6.** Some breakdown totals differ from NET by rounding: row 18 916.95 vs 916.94; row 19 618.53 vs 618.56; row 23 8,689.64 vs 8,689.62.

**OBS-7.** A0.2: "ALL EXISTING GYPSUM BOARD TO BE REPAIRED TO 'LIKE NEW' CONDITION" (img/O_A0.2_existing_gyp.png) does not appear in the Excel or the Scope Checklist. Add a Scope line (N/A with a reason, or an allowance / RFI) so that nothing printed is left silent.

## 4. Counts
Checks: 28 PASS / 8 FAIL (three-way table: 18 PASS / 3 FAIL; rule table: 10 PASS / 5 FAIL). This gives 6 MUST-FIX findings (F1-F6) and 7 OBSERVATIONS. Three-way quantities by type (A-E, bulkhead, RE), heights and board SF: all within 2 % or explained. No quantity error was found in the partition LF.
# BACK-CHECK rev1 - closure in rev2 (Harbor Freight Tools - Loveland, CO)

Deliverables: `Take-off/HFT_Loveland_Takeoff_FINAL_rev2.xlsx` and `Planos marcados/HFT_Loveland_markups_rev2.pdf` with 4 PNGs (_rev2). The rev1 files were moved to `hf/superseded_rev1/`.

Every quantity was recomputed by the chain (canon.py and the tools) from the resolved canon plus the printed data of rev2. The rev2 data are written by scripts/rev2_canon.py, each with its N/SHEET. Each item below was verified by me in the rev2 Excel and PDF.

| # | Finding | Status | rev2 value | Evidence (rev2) |
|---|---|---|---|---|
| F1 | Bracing to structure not carried | FIXED | **Metal stud brace to structure, 6" x 20 GA stud @ 4'-0" O.C.: 412.5 LF (50 braces)** on the 13 type A walls with unsheathed studs above the board (A-01, 02, 03, 05-14). A-04 is excluded because it is boarded to the deck on both faces. A-15, B and C are excluded because they stop at 8'-6". **Trade Ready Spazzer 9200 spacing bar: 125.97 LF** | Material Summary rows "Metal stud brace to structure..." and "Trade Ready Spazzer 9200 spacing bar...", both with a per-wall breakdown and N/SHEET 2/A4.1 (A1.1 note 1). Brace length is not printed, so the conservative value is LOADED: printed Sales B.O. structure ±16'-9" (A1.2) minus the top of the board (8'-6") = 8.25 ft each. **RFI-05** (Pending Items) gives options (A) 2/A4.1 geometry at 45° from the mid-point, delta -120.79 LF; (B) 5'-0" O.C. of 2/A4.1, delta -4 braces / -33.0 LF; (C) other. The sheet sweep covers all 50 sheets plus a program text grep. RI-08 removed. Tool fix BE-HF12. |
| F2 | Spanish words / internal names in visible text | FIXED | Review Items rewritten as estimator sentences with N/SHEET (8 items, n/8). I scanned every cell of the Excel and every markup Contents by program for these terms and found 0 hits: DISCREPANCIA, TOOL, tool rule, misc_info, review folder, canon, calculator, Z-furring slot, R-ALC / R80 codes, .py / .json. | Review Items sheet; the type E stud column reads "1-1/2" metal hat channel"; demo Contents read "estimator standing order". |
| F3 | Vestibule bulkhead slip track sat in the "heads" row | FIXED | **Top slip / deflection track 3-5/8" = 31.63 LF** (VH-01 13.79 + VH-02 8.92 + VH-03 8.92; N/SHEET 1/A5.3, 3/A5.3). The "roof step and heads" rows no longer exist; the bulkhead bottom track is in Bottom track 3-5/8" (54.85 LF). | Material Summary. Tool fix BE-HF11. |
| F4 | C.R. channel on 8'-6" walls; "/48" text | FIXED | **Bracing 1-1/2" C.R. channel @ 96" O.C. = 854.86 LF**. The back-check expected 854.85; the 0.01 is rounding of the unrounded per-wall rows. B-01..03, C-01..02 and A-15 now carry 0 rows (A4.1 note 7, constants.bracing_min_height_ft = 12). The breakdown text now reads "rows = ROUNDUP(H x 12 / 96) - 1 or the rows declared; walls not higher than 12 ft: 0 rows". | Material Summary bracing row. Tool fix BE-HF13. |
| F5 | Sill track without breakdown | FIXED | Sill track 10.67 LF: "306-W1 (A-01) 5.33 + 306-W2 (A-02) 5.33; sill (4.0 + 1.333) x 1 piece each", N/SHEET 5/A5.1, A1.1. A note states the 0.01 rounding against NET. | Material Summary row "Sill track". Tool fix BE-HF16. |
| F6 | Joined Partition Takeoff rows vs per-wall markups | FIXED | One row per wall ID (constants.partition_row_rule = wall_id): A-12 4.00 / 103.84 SF, A-13 2.61 / 67.75, A-14 5.43 / 140.97, C-01 12.28 / 104.38, C-02 10.94 / 92.96. Type totals are unchanged (A 145.72, C 23.22). | verificar_markups_excel 47/47 OK row for row (VERIFICACION_MARKUPS.md); auditoria_entrega 121 checks / 0 failures. Tool fix BE-HF14. |
| O1 | "T162" cited as a sheet; D1.0 cited on headers | FIXED | Header row N/SHEET: 5/A5.1, 2/A5.1, 2/A5.3, 1/A5.3, 8/A5.3, 9/A5.3, S2.1, A1.1, A5.2, A3.1. The T162-54 clip is described as a member of 9/A5.3. | Material Summary header row (canon misc sources BXH-02 / BXH-02-CLIP). |
| O2 | Bulkhead rows below the GRAND TOTAL | FIXED | Bulkhead is now type block **BULKHEAD-VH** (3 rows, 31.63 LF) inside the typed blocks. GRAND TOTAL = **687.69 LF**, equal to the markup legend TOTAL of 687.69 LF / 33 walls. Legend order matches the schedule: A, B, C, D, E, BULKHEAD-VH, RE. | Partition Takeoff; markups LEGEND page. Tool fixes BE-HF14 and BE-HF17. |
| O3 | Type C single tag / C-02 | KEPT, Review Item 1/8 | C-02 is kept as type C. Review Item gives A: keep / B: no inner wall, delta -10.94 LF / about -93 SF, with a plan crop of A1.1 Support Office 103. | Review Items 1/8. |
| O4 | Inputs B.O. Deck "n/a" | FIXED | Inputs B.O. Deck = 18.25 ft. The note cites the A1.2 chart: Sales ±18'-3" / ±17'-4", B.O. structure ±16'-9"; Sales Replenishment ±17'-4" / ±16'-11", B.O. structure ±15'-9 1/2" / ±15'-5". | Inputs row 13. |
| O5 | Demo markup "2 layer(s)" | FIXED | Demo Contents now read "2 faces x 1 layer" (DEMO-01..12) and "1 face" (DEMO-13/14). SF unchanged: 11,412 SF. | Markups D1.0. Tool fix BE-HF15. |
| O6 | Breakdown totals vs NET rounding | FIXED (note) | Rows whose items round differently from NET now carry "(NET x: difference = rounding of the items)": header 618.53 vs 618.56, Type X 8,689.64 vs 8,689.62, sill 10.66 vs 10.67. | Material Summary. Tool fix BE-HF16. |
| O7 | A0.2 "existing gypsum board repaired to like-new" silent | FIXED | Scope Checklist ALC-E11 "Patch and repair of existing gypsum board": INCLUDED (allowance); not measurable from the drawings, allowance by the estimator. Also Review Item 6/8. | Scope Checklist, Review Items. |

## Gates (rev2 chain run, hf/scripts/cadena.sh)
- plantilla_excel validar / armar / verificar: OK.
- alcances compuerta: OK.
- verificar_markups_excel: 47/47 OK. /Measure = printed scale: A1.1 / D1.0 3/32", A4.0 3/8", S2.1 1/4". Every sheet with take-off rows is marked (A1.1, A4.0, D1.0, S2.1).
- reglas.py compuerta: only failure = the separate back-check of rev2 (not annotated in the bitacora).
- etapas.py compuerta: PASA.
- auditoria_entrega: 121 checks, 0 failures.
- Tool suite: 61/61.

---

# rev3 directed revision (coordination order BE-CF16) - changed items only

Excel: `Take-off/HFT_Loveland_Takeoff_FINAL_rev3.xlsx`. Markups: `Planos marcados/HFT_Loveland_markups_rev3.pdf` (+4 PNG _rev3). The rev2 files are in `hf/superseded_rev2/`.

**What changed:** RFI-01 is answered by the drawings. The printed B.O. DECK callouts of A1.2 and A2.0 were located by program (scripts/rev3_d01_zonas.py). Both sheets were registered to A1.1 through grid bubbles F..A. D-01 was then split by grid bay into 7 zones:
- Each zone's limits are the grid lines as drawn.
- Stud height = B.O. deck of the zone − 1" slip gap (10/A4.1).
- Type X runs to the stud top on both faces (D/A4.1).
- A circled crop of each zone's callout is in etapas/4_canon/img_calc/.
- Bay C–B has no callout and takes the higher neighbour (±18'-0 1/2", conservative).
- The riser room walls D-02 / D-03 / D-04 sit east of grid A, under the ±18'-3" callout, and are unchanged at 18.17 ft.

| Zone | Bay (A1.1 grid) | LF | Printed callout (N/SHEET) | Stud / board height |
|---|---|---|---|---|
| D-01a | W end - F | 29.547 | B.O. DECK ±16'-11" (A1.2, A2.0) | 16.83 ft |
| D-01b | F - E | 30.005 | ±17'-3 1/2" (A1.2) | 17.21 ft |
| D-01c | E - D | 29.996 | ±17'-3 1/2" (A2.0) | 17.21 ft |
| D-01d | D - C | 30.000 | ±17'-6" (A1.2), ±17'-5 1/2" (A2.0): higher loaded | 17.42 ft |
| D-01e | C - B | 30.004 | no callout: higher neighbour ±18'-0 1/2" | 17.96 ft |
| D-01f | B - A | 30.018 | ±18'-0 1/2" (A2.0) | 17.96 ft |
| D-01g | A - E end | 29.526 | ±18'-3" (A1.2, A2.0), ±18'-2", ±18'-1 1/2" (A2.0): higher loaded | 18.17 ft |
| total | | 209.096 (= ±209'-1") | | |

**Verification (changed items only, rev2 → rev3, read from the Excel and the PDF):**

| Item | rev2 | rev3 | Check |
|---|---|---|---|
| D wall heights | D-01 18.17 for the full length | the 7 zones above; D-02..04 18.17 | Partition Takeoff rows D-01a..g = the zone table. PASS |
| 5/8" gyp board Type X | 8,689.62 SF | **8,424.88 SF** (-264.74) | Sum of the D rows: 994.56 + 1,032.78 + 1,032.46 + 1,045.20 + 1,077.74 + 1,078.24 + 1,072.98 + 676.66 + 207.14 + 207.14 = 8,424.90 (0.02 = rounding). PASS |
| 6" metal stud | 7,282.84 LF | **7,252.29 LF** (-30.55) | Lower studs in zones a-f. Each zone also rounds its stud count up on its own: a "split" node per zone joint counts the cut stud once, and about 4 studs are added by per-zone rounding (conservative). PASS |
| Slip / deflection track 6" | 239.12 LF | 239.12 LF | Unchanged (same wall length). PASS |
| Bottom / standard top track 6" | 444.17 / 205.05 | 444.17 / 205.05 | Unchanged. PASS |
| C.R. channel bracing | 854.86 | 854.85 | Every zone ≥ 16.83 ft keeps 2 rows (A4.1 note 7); 0.01 is rounding. PASS |
| Joint compound / tape (yields on board SF) | 1,129.25 LB / 5,803.07 LF | 1,110.18 / 5,705.12 | Follow the board SF. PASS |
| Markups Depth of D walls | 18.17 | D-01a 16.83, b 17.21, c 17.21, d 17.42, e 17.96, f 17.96, g 18.17; D-02..04 18.17 | Contents H and the Excel row match for row; verificar_markups_excel N/N OK. PASS |
| RFIs | 5 open | **4 open** (RFI-02..05, same ids). RFI-01 is in the Scope Checklist closed list as "RESOLVED from A1.2 / A2.0 printed B.O. deck callouts" | Each open RFI carries "Swept: all 50 sheets ... incl. SHX text; terms: B.O. DECK, B.O. JOIST, T.O. STEEL, UNDERSIDE, KICKER, BRACE, BRACING, LAYER, EXISTING GYP / PARTITION / STUD / WALL, HEAD, A.F.F.; specific sheets: ..." in its Pending Items question cell. PASS |
| Control joint CJ-01 | 218 LF (12 joints x 18.17 ft) | 218 LF | Not changed: it is the reading's item, conservative at the high point. Zone heights would give slightly less. |
