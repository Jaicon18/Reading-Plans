# Rev3 changes - O'Reilly Auto Parts, Evans CO, pass 2

Backups: `takeoff_canon_AB_rev2.json`, `overlay_OReilly_p2_rev2.json`. Edited: `takeoff_canon_AB.json` (reading: door deductions, HEAD-A-8 per-segment sources, new RFI-15), `overlay_OReilly_p2.json` (G01, G02, G06, G15, G18), `canon_ov.json` (re-applied), `revision_dirigida.md`, `overlay_mapeo.md`, `overlay_sin_objeto.md`.
Checks: `validar_canon.py takeoff_canon_AB.json tools` = CANON OK; `overlay.aplicar_canon` -> `canon_ov.json`, `validar_canon.py canon_ov.json tools` = CANON OK; `tools/canon.py canon_ov.json /tmp/rev3_out` -> `familias_out.json partition_types.avisos = []`. No materials calculated.

PURLIN = "[PENDIENTE] assumed 8\" purlin depth per PEMB shop drawing (not printed), estimator decision RFI-01" (-0.667 ft; the 10" scaled on 1/A3.1 was removed from every source / op).

| # | Item | Before | After | N/SHEET | Image |
|---|---|---|---|---|---|
| 1.1 | S21-N, S21-S wall + roof-side faces height | 14.678 (15.511 - 0.833 scaled) | **14.844** (15.511 - 0.667, PURLIN), height_status PENDIENTE | 3/A3.2, 1/A3.4, 2/A3.2, 1/A3.2 | - (not printed: no crop possible) |
| 1.2 | S21-E wall + Parts C face | 13.792 | **13.958** (14.625 - 0.667) | 2/A3.2, 3/A3.4 | - |
| 1.3 | S21-W1 / S21-W2 wall + faces; EXT-MS2-8 Parts B face | 15.563 | **15.729** (16.396 - 0.667) | 1/A3.2 | - |
| 1.4 | S42-01 wall + Parts C face | 14.339 | **14.505** (15.172 - 0.667) | S42/A1.1, 1/A3.2 | - |
| 1.5 | S42-02 wall + Parts B / C faces | 7.506 | **7.672** (8.339 - 0.667) | 6/A4.2 | - |
| 1.6 | S42-03 wall + Parts B face | 8.036 | **8.202** (8.869 - 0.667) | 6/A4.2 | - |
| 1.7 | S42-04 wall + Parts B face | 15.478 | **15.644** (16.311 - 0.667) | S42/A1.1 | - |
| 1.8 | VH-B1 / VH-B2 / VH-C wall height | 4.120 | **4.286** (4.953 - 0.667) | 3/A3.1 | - |
| 1.9 | S21-E above-lid faces (Office 102, R.R. 103/104) | 4.792 | **4.958** (14.625 - 0.667 - 9.0) | 7/A4.2, 2/A3.2 | - |
| 1.10 | S21-S R.R. 104 above-lid face | 4.889 | **5.055** (14.722 - 0.667 - 9.0) | 7/A4.2, 1/A3.2 | - |
| 1.11 | QTR-GYP-EXT-MS | 174.86 SF | **175.34 SF** (EXT-MS2 Parts B 2.92 x 15.729) | 1/A3.1 | - |
| 1.12 | RC-EXT-MS | 120.51 LF | 120.51 LF (rows unchanged: ROUNDUP(15.729/2)+1 = 9) | 1/A3.1 | - |
| 1.13 | CB-S42-HDR-BOTTOM | 193.92 LF | **194.25 LF** (2 x 7.672 at the free end) | 6/A4.2 | - |
| 1.14 | JDM-S42-JOINTS | 40.81 LF | **41.30 LF** (7.672 / 8.202 / 8.723) | 2/A4.2 | - |
| 1.15 | CJ-S21 | 86.30 LF | **87.29 LF** (2 x 14.844 + 2 x 13.958 + 2 x 14.844) | A1.1 note 3.A | - |
| 1.16 | Level 5 items with board top under the purlin (14 items) | 6524.35 SF total | **6582.90 SF** total (e.g. L5-S21-N-B0 311.16 -> 315.49; L5-S42-01-B1 554.45 -> 560.86) | A1.2 | - |
| 1.17 | RFI-01 text / rfi_cierre | "purlin depth scaled 10\" on 1/A3.1 (0.833 ft)" | CLOSED (decision), depth PURLIN, delta -0.667 ft | 1/A3.2 | - |
| 2.1 | S21-N Parts C face deduction | 71.89 SF (doors 3 + 2) | **0** (R70.3, deduct_info note) | A5.1, A1.1 | - |
| 2.2 | S21-N Parts A face deduction | 23.89 SF (door 7) | **0** | A5.1, A1.1 | - |
| 2.3 | S43-OF-S both faces deduction | 23.89 SF each (door 4) | **0** | A5.1, 7/A5.1 | - |
| 2.4 | S43-RR-S faces deduction | 47.78 (Parts C) + 23.89 (R.R. 103) + 23.89 (R.R. 104) (doors 5 / 6) | **0** | A5.1 | - |
| 2.5 | S21-S windows D1 / D2, storefront A / B1 / B2 / C heads | 76.49 SF / head bands | **kept** (not doors) | A5.2, 1/A3.4 | - |
| 3.1 | HEAD-A-8 Parts Area A face (30.667 x 0.667, base 11.333) | one source "1/A5.2 ... 1/A3.1 / 2/A3.1" | same quantity; per-segment source: 18'-8" = 1/A5.2 printed 8"; 12'-0" = 2/A3.1 -> HEAD DETAIL 1/A5.2; 11'-4" -> 12'-0"; board_source RFI-06 A | 1/A5.2, 2/A3.1, A5.2 | img_rev3/rev3_A5.2_typeA_elevation_segments_head_callout.png, img_rev3/rev3_A5.2_1_head_detail_8in_interior_board.png, img_rev3/rev3_A3.1_2_section_12-0_segment_head.png, img_rev3/rev3_A1.1_west_string_sections_per_segment.png |
| 3.2 | HEAD-A-8 vestibule 100A face (8.0 x 0) | "no face" (C-3 at the head) | 0 kept, **[PENDIENTE] RFI-15** (new): (A) 0 per 3/A3.1 / (B) +5.33 SF 5/8" X + 5.33 SF 1/4" + 8.0 LF RC + 3.50 SF 5/8" X + 3.08 SF 1/4" underside + 8.0 LF corner bead / (C) other | 3/A3.1, 1/A5.2, A1.2 | img_rev3/rev3_A3.1_3_section_vestibule_8-0_segment_head.png, img_rev3/rev3_A3.1_3_vestibule_head_zoom_5x.png, img_rev3/rev3_A1.2_finish_schedule_100_100A.png |
| 3.3 | GWB-HEAD-A-UNDERSIDE (5/8" X) | 13.42 SF (canon) | 13.42 SF, upserted in overlay G06 with RFI-06 A op | 1/A5.2 | img_rev3/rev3_A5.2_1_head_detail_8in_interior_board.png |
| 3.4 | QTR-GYP-HEAD-A-UNDERSIDE (1/4") | none (no object in rev2) | **11.82 SF** = 30.667 x 4.625"/12 (RFI-06 A; 1/A5.2 draws 1/4" on the vertical face only) | 1/A5.2 | img_rev3/rev3_A5.2_1_head_detail_8in_interior_board.png |
| 3.5 | CB-HEAD-A-UNDERSIDE | 30.667 LF | 30.667 LF (kept) | 1/A5.2 | - |
| 3.6 | Piers EXT-MS1 / EXT-MS2 + head: 1/4" + RC | QTR-GYP-EXT-MS / RC-EXT-MS | kept, op now cites RFI-06 A (see 1.11 / 1.12) | 1/A3.1, 1/A5.2 | - |
| 3.7 | RFI-06 text / rfi_cierre | option A, underside 5/8" + CB | option A: 5/8" X / 1/4" / RC on piers and head, underside 5/8" X + 1/4" + CB; vestibule split to RFI-15 | 1/A5.2 | - |
| 4.1 | revision_dirigida.md | no corner rule section | **Corner ownership** section: R70.2 / R70.3 quoted; S24-OF/S43-OF-W, S24-OF/S43-OF-E, S24-RR/S43-RR-W, S24-RRS/S43-RR-S -> S24 owner; S21-S/S24-RR -> S21-S owner; S21-E / S21-S vs S24 parallel, no corner | A1.1, 1A/A4.1 | img_revision/e_A1.1_*.png |

Not changed, flagged:
- Overlay G09 still uses a **purlin bay scaled 5.0 ft** on 1/S5.1 / 4/S5.1 (PEMB-6IN-S42-02, PEMB-6IN-S42-01, L4X4-S42-03). That is also a scaled value under rule #0. It was outside the rev3 scope.
- VH-B1/B2/C faces: "drawn ~8\"" on 3/A5.2. No height is printed for those faces.
- ZF-RUNNER-S21 deducts the bottom runner at doors 3 / 2 / 7 (12.667 LF). Skill E10 says bottom track at doors is not deducted. This is track, not board, so it was left as is.
