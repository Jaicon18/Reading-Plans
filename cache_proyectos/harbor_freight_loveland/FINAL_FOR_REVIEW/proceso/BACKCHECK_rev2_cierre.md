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
