# Rev4 changes - O'Reilly Auto Parts, Evans CO, pass 2

Backups: `takeoff_canon_AB_rev3.json`, `overlay_OReilly_p2_rev3.json`.
Edited: `takeoff_canon_AB.json` (the reading: S21-S, EXT-MS1-8, EXT-MS2-8, HEAD-A-8 faces and the new RFI-16), `overlay_OReilly_p2.json` (G01 S21-S / EXT-MS2-8 x2 / QTR-GYP-EXT-MS / RC-EXT-MS, G02 S21-S, G06 HEAD-A-8 / CB-HEAD-A-UNDERSIDE), `canon_ov.json` (regenerated with `overlay.aplicar_canon`).
Checks:
- `validar_canon.py takeoff_canon_AB.json tools` = CANON OK
- `validar_canon.py canon_ov.json tools` = CANON OK
- `tools/canon.py canon_ov.json /tmp/rev4_out`: `familias_out.json partition_types.avisos = []`

No materials were calculated.
Crops: `img_rev4/`. Each one was rendered with pymupdf from `bidset_SIN_MARKUPS.pdf` at 130-230 dpi, circled, then reopened and checked.

## 1. Rule BE-110: board per face never deducts openings (doors and windows)

Every face of every wall in the reading and in the overlay was swept for `deduct_sf` / `deduct_opening_sf`.

| # | Wall / face | Where | Before | After |
|---|---|---|---|---|
| 1.1 | S21-S Parts Area B 101 (windows D1 / D2, A5.2 11'-4 3/8" x 3'-4 3/8" R.O.) | canon `walls` | `deduct_opening_sf` 76.49 | removed. `deduct_info` added (BE-110). The height_source text now says "not deducted" |
| 1.2 | same face | overlay G01 (RFI-01 faces) | `deduct_opening_sf` 76.49 | removed (same edit) |
| 1.3 | same face | overlay G02 (RFI-02 faces, applied last) | `deduct_opening_sf` 76.49 | removed (same edit) |
| 1.4 | Result in `board_out` | /tmp/rev4_out | S21-S face 794.01 SF; 5/8 type X total 7081.09 SF | **870.50 SF** (58.643 x 14.844); total **7157.58 SF** (+76.49) |

No other board face had a window or storefront deduction. The doors were already cleared in rev3.
These items have no deduction and need no change:
- VH-B1 / VH-B2 / VH-C and HEAD-A-8. These faces begin at the storefront head (`board_base_ft` 11.333). That is the only wall there, so it is not a deduction.
- The piers start at the floor.

Left as they were, by order (finishes, not board):
- L5-S21-S-A1 (Level 5, still "- openings 76.49").
- The other Level 5 and W-4 rows.

## 2. Storefront A piers and head wall: interior face, edge by edge

| Edge | Printed value | N/SHEET | Image |
|---|---|---|---|
| Head board, bottom | **11'-4" (R.O.)** storefront A head | A5.2 window type A | img_rev4/rev4_A5.2_typeA_elevation_11-4_RO.png |
| Head board, bottom (same line) | **B.O. SHEATHING EL. 111'-4"** | 2/A3.1 | img_rev4/rev4_A3.1_2_head_section_board_short_leg.png |
| Head board, top | **8"** from the B.O. sheathing line to the top of the 5/8" type X (on 1/4" + 7/8" RC) = 12'-0" | 1/A5.2 | img_rev4/rev4_A5.2_1_head_detail_8in_printed.png |
| Head board, above 12'-0" | none: key notes 20 / 33 / 35 short leg only, insulation (16) above | 2/A3.1 (12'-0" segment) -> HEAD DETAIL 1/A5.2 | img_rev4/rev4_A3.1_2_head_section_board_short_leg.png |
| Pier board, bottom | finish floor EL. 100'-0" | 1/A3.1 | img_rev4/rev4_A3.1_1_pier_section_board_top.png |
| Pier board, top | **not printed**. 1/A3.1 (cut at the 6'-0" pier, A1.1) draws the board ending just above ACT 21, on the head-board line. The only printed number for that line is 1/A5.2 8" over 111'-4" (1/A3.1 also prints C.L. STUCCO JOINT EL. 111'-4"). Above it is insulation (16) only, up to the roof | 1/A3.1, 1/A5.2 | img_rev4/rev4_A3.1_1_pier_section_board_top.png |
| Ceiling (reference, not a board edge) | Parts Area A 100 C-1 **11'-6"**; vestibule 100A C-3 11'-4" | A1.2 finish schedule | img_rev4/rev4_A1.2_finish_schedule_100_C1_11-6.png |
| S21 / pier junction | plan only, no height. A vee-shaped control joint separates the S21 board (on Z-furring 10) from the pier board (8" stud + RC 33 + 1/4" 35 + 5/8" X 20) | 7/A3.2 | img_rev4/rev4_A3.2_7_plan_section_S21_pier.png |
| Origin of the alternate 16.4 ft / 5.06 ft reading | **5'-0 3/4"** (111'-4" -> T.O. HIGH EAVE EL. 116'-4 3/4"). This is an exterior stucco / eave dimension, not a board edge. 116.396 - 100 = 16.396; 116.396 - 111.333 = 5.063 | 1/A3.1 | img_rev4/rev4_A3.1_1_pier_section_board_top.png |

A1.1 section marks per segment (1/A3.1 on the 6'-0" pier, 2/A3.1 on the 12'-0" segment, 3/A3.1 on the vestibule): img_rev3/rev3_A1.1_west_string_sections_per_segment.png.

### Answers

- **(a) Piers.** The interior board goes up to **12'-0" A.F.F.**, not to the ceiling (11'-6") and not to the purlin or roof framing like S21.
  - 1/A3.1 draws the board stopping just above the ACT, with insulation only above it.
  - 7/A3.2 is a plan section. It gives no height, and it puts a control joint between the S21 board and the pier board.
  - The top is **not printed for the pier itself**, so it is **[PENDIENTE] RFI-16**.
- **(b) Head.** The board runs from **11'-4"** (A5.2 "11'-4" (R.O.)" / 2/A3.1 B.O. SHEATHING EL. 111'-4") to **12'-0"** (1/A5.2 printed 8").
  - Both edges are printed, so the head is CONFIRMADO.
  - The 5.06 ft reading is rejected because it uses an exterior elevation dimension.

### Before / after

| # | Item | Before (rev3) | After (rev4) | N/SHEET |
|---|---|---|---|---|
| 2.1 | EXT-MS1-8 Parts Area A face (6.0 LF) | 12.0, source "drawn 8\" above the head" | **12.0** kept. Source cites the printed edges. `pending_reason` RFI-16. `height_op` 111.333 - 100 + 8/12 | 1/A3.1, 1/A5.2, 2/A3.1, A1.2 |
| 2.2 | EXT-MS2-8 Parts Area A face (3.08 LF): canon + overlay G01 (both copies) | 12.0 | **12.0** kept, same as 2.1 | same |
| 2.3 | EXT-MS2-8 Parts Area B face (2.92 LF) | 15.729 (C-2 exposed, purlin RFI-01) | unchanged | 1/A3.2, A1.2 |
| 2.4 | HEAD-A-8 Parts Area A face (30.667 LF, base 11.333, 0.667): canon + overlay G06 | 0.667, source per segment | **0.667** kept. `height_status` CONFIRMADO. Source = printed bottom (A5.2 11'-4" R.O. / 2/A3.1 111'-4") + printed top (1/A5.2 8") | A5.2, 2/A3.1, 1/A5.2 |
| 2.5 | HEAD-A-8 vestibule 100A face (8.0 LF) | 0, RFI-15 | unchanged (RFI-15 still open) | 3/A3.1 |
| 2.6 | QTR-GYP-EXT-MS (1/4", RFI-06 A) | 175.34 SF | **175.34 SF**, op re-checked: 6.0 x 12.0 + 3.08 x 12.0 + 2.92 x 15.729 + 30.667 x 0.667 = 72.0 + 36.96 + 45.93 + 20.45 | 1/A3.1, 1/A5.2 |
| 2.7 | RC-EXT-MS (087F125-33 @ 24") | 120.51 LF | **120.51 LF**, op re-checked: 7 x 6.0 + 7 x 3.08 + 9 x 2.92 + 1 x 30.667 | 1/A3.1, 1/A5.2 |
| 2.8 | CB-HEAD-A-UNDERSIDE | 30.667 LF | **30.667 LF** (18.667 + 12.0), op re-checked | 1/A5.2 |
| 2.9 | GWB-HEAD-A-UNDERSIDE / QTR-GYP-HEAD-A-UNDERSIDE | 13.42 SF / 11.82 SF | unchanged (head edges confirmed) | 1/A5.2 |
| 2.10 | RFI-16 (new, in the reading `rfis`, R80e.50 format) | - | (A) Plans 1/A3.1 + 1/A5.2: 12'-0", **carried**, delta 0 / (B) Code: no trade code sets the extent (ASTM C840 / GA-216, no rated assembly on the piers). Board to the roof like S21 = 16.396 ft: **+39.92 SF 5/8" X + 39.92 SF 1/4" + 27.24 LF RC** (9.08 LF x 4.396 ft; 15.729 under the RFI-01 purlin stop = +33.86 SF + 33.86 SF + 18.16 LF) / (C) Other: ____ | 1/A3.1, 2/A3.1, 7/A3.2, 1/A5.2, A5.2, A1.1, A1.2 |

Alternate head reading, for reference only. It is rejected and not raised as an RFI:
- 30.67 x 5.06 = 155.19 SF against 20.45 SF carried, a gap of +134.74 SF per layer.
- The 5.06 ft value is the exterior dimension 111'-4" -> 116'-4 3/4", not a board edge.
