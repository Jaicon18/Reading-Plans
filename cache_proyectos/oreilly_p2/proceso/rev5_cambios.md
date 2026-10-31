# Rev5 changes: O'Reilly Auto Parts, Evans CO, pass 2 (element 2, gypsum board)

Backups: `takeoff_canon_AB_rev4.json` and `overlay_OReilly_p2_rev4.json`.

Edited files:
- `takeoff_canon_AB.json` (the reading):
  - VH faces
  - misc GWB-VH-UNDERSIDE and GWB-S42-HDR-UNDERSIDE
  - plywood HEAD-A-SOFFIT-FRT
  - op texts for the ceilings and GWB-HEAD-A-UNDERSIDE
  - RFI-17 and RFI-18
- `overlay_OReilly_p2.json` (the decisions):
  - G01 VH faces
  - G07 W-4
  - G15 Level 5
  - G19 W.R. split, plus misc GWB-S43-RR-W-ABOVE-WR
  - new group G26, the jamb return
- `canon_ov.json`, regenerated with `overlay.aplicar_canon`. Applying it twice gives the same result.

Checks:
- `validar_canon.py` reports CANON OK on both files.
- `tools/canon.py canon_ov.json /tmp/rev5_out` gives `partition_types.avisos = []`.

No materials were calculated outside the item ops.

All crops are in `img_rev5/`. Each one was rendered with pymupdf from `bidset_SIN_MARKUPS.pdf`, circled, then reopened and checked.

| # | Point | Before (rev4) | After (rev5) | Printed dimension / N/SHEET | Image |
|---|---|---|---|---|---|
| 1 | Vestibule heads VH-C / VH-B1 / VH-B2 | 1 face (Parts A) x 0.667 from base 11.333 = 13.40 SF. The source said "drawn ~8\"", which is a scaled value | **Faces:** only the Parts Area A 100 face has board. The vestibule side above the C-3 ceiling has insulation only (3/A3.1, 3/A5.2). The other reading's 89.58 SF (2 faces at full height) is rejected.<br>**Height:** the top of the vertical leg is **not printed**, so 0.667 stays as **[PENDIENTE] RFI-17**:<br>(A) 8\" as on 1/A5.2, carried, 13.40 SF<br>(B) up to the purlin stop 4.286: +72.68 SF<br>(C) other<br>**New: GWB-VH-UNDERSIDE 11.28 SF.** The board runs under the heads (3/A5.2). Width 4 1/2\" + 1 1/2\" + 5/8\" = 6.625\". Envelope 9.104 x 6.219 = 56.62, minus the 45.33 field ceiling | 3/A5.2 (6\", 4 1/2\", 1 1/2\"); A5.2 B1 / B2 / C 11'-4\" R.O., head at 3/A5.2; 10/A5.2 8'-0\" x 5'-8\"; 3/A3.1 | rev5_p1_A5.2_3_vestibule_head_detail.png, rev5_p1_A3.1_3_vestibule_head_parts_face.png, rev5_p1_A5.2_B1_B2_C_heads_11-4_3A5.2.png |
| 2 | Storefront A head underside | 13.42 SF (0.4375 ft) | **13.42 SF, confirmed**. The gypsum runs from the frame's interior edge to the finished face: 3 1/2\" + 7/8\" + 1/4\" + 5/8\" = 5.25\".<br>The 1.17 ft (14\") reading is rejected: the exterior 6\" + 4 1/2\" under the studs is FRT plywood (34) plus stucco (13), not gypsum | 1/A5.2 (3 1/2\", 7/8\", 1/4\", 5/8\"); 2/A3.1 keys 13 / 34 / 20 | rev5_p2_p4_A5.2_1_head_underside_gyp_vs_FRT.png |
| 3 | S42 header underside | not in the canon | **+GWB-S42-HDR-UNDERSIDE 30.79 SF** = 75.788 LF (S42-02 25.455 + S42-03 50.333, the suspended length) x 4.875\" | 6/A4.2 key 6 wraps the bottom at B.O. FRAMING 106'-10\"; S42/A1.1 5/8\" + 3 5/8\" + 5/8\" | rev5_p3_A4.2_6_header_bottom_board.png, rev5_p3_A1.1_S42_type_4.875.png |
| 4 | FRT plywood at the exterior soffit of the storefront A head | not in the canon (HEAD-A-FRT is the vertical sheathing only) | **Yes, it exists. +HEAD-A-SOFFIT-FRT 33.83 SF** = 38.667 (38'-8\" R.O.) x 10.5\" (6\" + 4 1/2\", from the inner face of the vertical FRT to the frame's interior edge). The other reading's 45.12 SF (14\") is rejected | 1/A5.2 (6\", 4 1/2\"); 2/A3.1 key 34 "5/8\" exterior fire treated plywood sheathing"; A5.2 type A 38'-8\" | rev5_p2_p4_A5.2_1_head_underside_gyp_vs_FRT.png, rev5_p4_A3.1_2_soffit_key34.png |
| 5 | Ceilings: Office 102 + Vestibule 100A | 86.03 + 45.33 = 131.36 | **Unchanged, 131.36**. Sources rewritten.<br>**Office:** the A1.1 11'-0\" x 8'-0\" is face of stud (general note B). 7/A4.2 draws the ceiling board butting the wall board, so (11.0 - 0.104) x (8.0 - 0.104) = 86.03.<br>**Vestibule:** 10/A5.2 prints 8'-0\" x 5'-8\" between the frame inner faces, so 45.33. The board under the heads is in GWB-VH-UNDERSIDE (point 1). With it, the vestibule total is 56.62 | A1.1 11'-0\" / 8'-0\", note B; 7/A4.2; 10/A5.2; 3/A3.1 2'-10\" + 2'-10\"; A1.2 C-3 8'-6\" / 11'-4\" | rev5_p5_A1.1_office_11-0_8-0.png, rev5_p5_A1.1_general_note_B.png, rev5_p5_A4.2_7_ceiling_board_edge.png, rev5_p5_A5.2_10_vestibule_8-0_5-8.png |
| 6 | Janitor W.R. (RFI-19 = B) | the whole break face of S43-RR-W was W.R.: 8.5 x 9.0 = 76.5 SF | **W.R. only in the zone behind the fixture: 4.0 x 4.0 = 16.0 SF**. The rest goes back to 5/8\" X: 4.5 x 9.0 = 40.5 (face) + 20.0 (misc GWB-S43-RR-W-ABOVE-WR). The face total stays 76.5.<br>**Fixtures:** floor-mounted janitor sink (key 5) with an eye wash (6), at the north end of the face.<br>**Code:** IBC 1210.2.2 sets the zone at 2'-0\" from the service sink and 4'-0\" A.F.F. GA-216 sets the material. A1.1 note 3.B asks for W.R. at the "janitor's sink areas".<br>The sink width is not printed, so the zone uses an assumed 24\" basin. This is **[PENDIENTE] RFI-18 (RFI-DERIVADO)**:<br>(A) carried<br>(B) whole face: +60.5 W.R. / -60.5 X<br>(C) actual basin | 12/A4.1 keys 5 / 6 / 8 (5'-0\"); A1.1 note 3.B, break area 8'-6\" | rev5_p6_A4.1_12_janitor_sink.png |
| 7 | Jamb return (RFI-26 = A) | 97.53 LF x 0.5 = 48.76 SF (storefront A 61.34 + D1 / D2 without sill) | **11.78 SF** = D1 + D2: 2 x (head 11.365 + sill 11.365 + 2 jambs x 3.365) = 58.92 LF x 0.2 ft (estimator).<br>Storefront A changed to jamb_return false. The 0.5 ft criterion was replaced by constants.jamb_return_width_ft 0.2. D1 / D2 now carry with_sill + sill_return (13/A5.2). The derived jamb trim changes 195.05 -> 117.84 LF | A5.2 D1 / D2 11'-4 3/8\" x 3'-4 3/8\" (R.O.); 12/A5.2 jamb; 13/A5.2 sill; 11/A5.2 head | rev5_p7_A5.2_D1_D2_RO.png, rev5_p7_A5.2_12_13_jamb_sill.png |
| W-4 | W4-PANELS-103 / 104 | 253.77 each (minus door R.O. 23.89) | **277.67 each** = 2 x (7'-10\" + 8'-6\") x 8.5, no deduction. Total 507.54 -> 555.34 | A1.2; 1A/A4.1 | - |
| L5 | level5_items | 39 items, 6582.90 SF, openings and base B-1 deducted | **34 items, 6432.72 SF**.<br>All opening and B-1 deductions were removed. The bases left are board-start lines only (HEAD-A / VH 11.333, S42 header 6.833, plenum 9.0). The ACT 11'-6\" cap is kept because nothing is painted above it.<br>Removed as not W-2: the exterior faces of office 102 / R.R. 103 / 104 are **W-3** (A1.2 note 1). These were L5-S43-OF-W-A0, L5-S43-OF-E-B1, L5-S43-OF-S-A0, L5-S43-RR-W-A0 and L5-S43-RR-S-A0, 402.89 SF before the change.<br>The W-3 bands in Parts A / C (14/A4.1, "W-2/W-3" walls) stay inside the W-2 walls, per the G15 decision. Their band edges are not printed | A1.2 finish schedule + note 1 | rev5_L5_A1.2_schedule_note1_W3.png |

## Family deltas (canon.py, before rev5 -> after)

| Family | Before | After |
|---|---|---|
| 5/8" type X | 7302.36 | 7404.93 (+11.28 VH underside, +30.79 S42 underside, +60.50 from the W.R. split) |
| 5/8" type X W.R. | 781.71 | 721.21 (-60.50) |
| FRT plywood | 373.80 | 407.63 (+33.83) |
| Sanitary wall panels | 507.54 | 555.34 |
| Level 5 | 6582.90 | 6432.72 |
| Jamb return | 48.76 | 11.78 |
| Metal trim | 917.82 | 840.61 (jamb-return beads) |

Joint compound and tape also change, from the tool's own yields.

Not carried and noted only:
- The W-4 panel shown on the break face (12/A4.1 key 8, to 5'-0"). Estimator decision 07 covers the restrooms only.
- Corner bead at the VH head bottoms. 3/A5.2 has no label for it.
