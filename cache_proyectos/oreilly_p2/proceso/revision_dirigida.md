# Directed review (part A) - O'Reilly Auto Parts, Evans CO, pass 2

Canon edited in place: `takeoff_canon_AB.json` (backup before review: `takeoff_canon_AB_v1_pre_revision.json`).
Checks: `python3 validar_canon.py takeoff_canon_AB.json tools` -> **CANON OK**; `python3 tools/canon.py takeoff_canon_AB.json /tmp/x_out` -> `familias_out.json partition_types.avisos = []` (the 5 R11 notices are closed).
Crops: `img_revision/` (rendered with pymupdf from `bidset_SIN_MARKUPS.pdf`, every crop reopened and checked).

| # | Item | Before | After | N/SHEET | Image |
|---|---|---|---|---|---|
| a1 | S43-OF-W / OF-E / OF-S, S43-RR-W / RR-S: height of each face | Room faces (office 102, R.R. 103 / 104) 8.5. Outside faces (break area / Parts Area C 105) 9.0 | **No change. Confirmed.** No face goes above 9.0 | S43/A1.1 type: "STUDS TO 8'-6\" A.F.F.", board "5/8\" TYPE 'X' EACH SIDE", with no separate board height, so the board follows the studs. 7/A4.2: inside board to B.O. FRAMING EL. 108'-6\" (8'-6\"). The outside board passes the 6\" joist (6\" printed) and ends with corner bead (key 7) and 1x4 trim (key 12), so 9'-0\". The break area / Parts Area C is C-2 exposed (A1.2), but 7/A4.2 stops the outside board at 9'-0\" (it does not run to the roof). A1.2: office / R.R. ceiling C-3 at 8'-6\" | a_A4.2_7_S43_8-6_plus_6.png, a_A1.1_wall_types_S24_S43_S61.png, a_A1.2_finish_schedule_ceiling_heights.png |
| a2 | S43 board by face | 5/8 type X on office / Parts C faces, type X W.R. on the restroom faces | No change | A1.1 note 3.B (W.R. at restrooms) | a_A1.1_wall_types_S24_S43_S61.png |
| a3 | S24 / S61 faces | 8.5 | No change. S24: "5/8\" type X interior side to 8'-6\" A.F.F." with no board on the Z-furring behind. S61: studs to 8'-6\" | S24/A1.1, S61/A1.1 | a_A1.1_wall_types_S24_S43_S61.png |
| b1 | EXT-MS1-8 / EXT-MS2-8 interior board | Parts A 12.0 full length. MS2 Parts B face 16.396 | No change. Confirmed | 1/A3.1: key 20 + 33 + 35 run from the floor to about 8\" above B.O. SHEATHING 111'-4\", about 6\" above the ACT (scaled 11.9 ft), so 12.0 is correct | b_A3.1_1_wall_section_MS_interior.png |
| b2 | HEAD-A-8 interior face | One face, "Parts Area A 100", 0.667 x 38.667 (full storefront length) | **Parts Area A 30.667 x 0.667** (base 11.333) + **Vestibule 100A 8.0 at height 0** | A5.2 type A prints 18'-8\" (R.O.) + 8'-0\" (HOLD = vestibule) + 12'-0\" (R.O.). A1.2 vestibule C-3 ceiling at 11'-4\" = the head. 3/A3.1 draws no wall board above the head inside the vestibule | b_A3.1_2_head_section.png, b_A5.2_1_head_storefrontA_underside.png |
| b3 | Underside of the storefront A head | Not carried | **misc GWB-HEAD-A-UNDERSIDE 13.42 SF 5/8\" type X**: 30.667 x (3-1/2\" + 7/8\" + 1/4\" + 5/8\" = 5.25\") | 1/A5.2: the 5/8\" type X runs under the interior half of the head from the storefront frame to the finished face. 3-1/2\" is printed. It is a single layer: the 1/4\" is on the vertical face only | b_A5.2_1_head_storefrontA_underside.png |
| b4 | Dependent items | QTR-GYP-EXT-MS 182.63. RC-EXT-MS 131.43 | **177.29 SF / 123.43 LF**. The HEAD-A share went from 38.667 to 30.667 | 1/A5.2, 1/A3.1 | - |
| c1 | S24-OF length | 11.708 DERIVADO | **11.708 DERIVADO** (kept). Source improved | A1.1 prints 11'-0\" between the S43 inner stud faces, + 2 x (3-5/8\" stud + 5/8\" outer board). S24 owns both corners (vector, see e). There is no enlarged office plan, so no printed dimension gives the wall length directly. That is why it is not CONFIRMADO | e_A1.1_S24-OF_corners_zoom.png |
| c2 | S24-RR length | 16.823 DERIVADO | **16.823 DERIVADO** (kept) | A1.1 **and 1A/A4.1** print 7'-10\" + 6\" + 7'-10\" (the enlarged plan agrees), + S43-RR-W 4-1/4\" + S24-RRS stud 3-5/8\" (owns both corners) | c_A4.1_1A_enlarged_RR_plan.png |
| c3 | S24-RRS length | 8.854 DERIVADO (8'-6\" + 4-1/4\") | **8.854 DERIVADO**. Op is now 8.5 + 3.625/12 + 0.625/12 | **1A/A4.1 prints 8'-6\" + 3 5/8\"** (the S43-RR-S stud), so only the 5/8\" outer board comes from the type. A1.1 8'-6\" (break area) agrees | c_A4.1_1A_enlarged_RR_plan.png |
| d1 | S42 header wall past the S42-03 corner | S42-02 = 18.74 ft, ends at the corner (band hi 827.6) | **Yes, it continues on A1.1.** S42-02 = **25.455** (18.74 + 6.715). Band hi 888.3 pt. Faces: Parts A 18.74 @ 5.167, Parts B 6.715 @ 8.339 (new), Parts C 25.455 @ 8.339. Node N24 changed from L to T (branch S42-03, through S42-02) + N50 free end | A1.1: dashed double line (554.0-558.0 pt) continues from 827.6 to 888.3 pt (60.7 pt / 9.04 = 6.715 ft, not dimensioned). The 16'-10 7/8\"± dimension ends on it at 879 pt. The S4.1 framing key plan (key note 4) stops the header at the corner, so **RFI-14** was raised (A = carried as A1.1 / B = stop at the corner). 1/S5.1 and 2/A4.2 are sections and do not show the plan extent | d_A1.1_S42_corner_x826.png, d_A1.1_S42_continuation_end_888pt.png, d_S4.1_framing_key_plan_S42.png |
| d2 | S42 dependent items | KICKERS 141.4. LAT-STRUT 69.07. ANG-STRUT 64.0. BLK-S42-HDR-NAILERS 138.15. CB-S42-HDR-BOTTOM 165.48 | **155.54** (22 kickers). **75.79**. **64.0** (still 8). **151.58**. **195.59** (+ 2 x 8.339 at the new free end) | 1/S5.1, 5/S5.1, 6/A4.2 | - |
| e1 | S24-OF / S43-OF-W, S24-OF / S43-OF-E | S43 band lo 321.7 (inside the S24 band: R11 0.465 / 0.442 ft) | S43-OF-W / OF-E band lo **322.4** (= S24 face). Length 8.0 CONFIRMADO is unchanged | A1.1 40x vector: the S24 hatch fills the corner square, and the S24 inner line (321.1-322.4 pt) stops at the S43 inner line. Owner = S24 (R70.2 / R78.35). This agrees with the lengths (S24-OF 11'-0\" + 2 x 4-1/4\") and with nodes N34-N37 | e_A1.1_S24-OF_x_S43-OF-W_corner_40x.png |
| e2 | S24-RR / S43-RR-W | S43-RR-W lo 321.7 (R11 0.442 ft) | lo **322.4**. Owner = S24-RR | A1.1 40x: same pattern as e1 | e_A1.1_S24-RR_x_S43-RR-W_corner_40x.png |
| e3 | S24-RRS / S43-RR-S | S43-RR-S hi 1072.4 (S24-RRS reads 0.431 ft into S43-RR-S) | S43-RR-S hi **1071.8** (= S24-RRS face). Owner = S24-RRS, which runs to the S43-RR-S outer face (8'-6\" + 3 5/8\" + 5/8\") | A1.1 16x: the S24-RRS hatch runs down to the S43-RR-S outer face beside the door 6 jamb stub | e_A1.1_S24-RRS_x_S43-RR-S_corner_16x.png |
| e4 | S21-S / S24-RR | S21-S lo 319.2 (R11 0.354 ft: the S21-S end fell inside the S24-RR band tolerance) | S21-S lo **318.1** (and S21-N lo 318.1 for symmetry). Both are owners of their corners, as already in the length 85.0. The band is now 768.5 pt = 85.01 ft | A1.1 40x: the S21-S furring line starts at the east CMU face (317.2-318.1 pt) and runs past the S21-E / S24-RR ends. S24-RR ends at the S21-S face 1074.9 | e_A1.1_S21-S_x_S24-RR_corner_40x.png |

Result: `partition_types.avisos = []`. No R11 notice is left.
New RFI: **RFI-14** (S42 header continuation, A1.1 vs S4.1).

---

# Rev3 adjustments (pass 2)

Backups before rev3: `takeoff_canon_AB_rev2.json`, `overlay_OReilly_p2_rev2.json`. Crops: `img_rev3/` (rendered with pymupdf from `bidset_SIN_MARKUPS.pdf`, circled, reopened and checked). Full change list: `rev3_cambios.md`.

## Rev3 point 1 - RFI-01 purlin depth

The B.O. of the PEMB purlin is not printed (1/A3.1, 2/A3.1, 3/A3.1, 1/A3.2, 2/A3.2, 3/A3.2, 1/A3.4, S4.1, S5.1). The 10" value scaled on 1/A3.1 was removed from every source / op (rule #0). Heights now use **-0.667 ft = [PENDIENTE] assumed 8" purlin depth per PEMB shop drawing (not printed), estimator decision RFI-01**. Wall `height_status` = PENDIENTE with `pending_reason` and `sheets_searched` (S21-N/E/S/W1/W2, S42-01..04, VH-B1/B2/C).

## Rev3 point 2 - doors not deducted from board faces (R70.3), wall by wall

| Wall | Openings in the wall | Board deduction before | After |
|---|---|---|---|
| S21-N | Doors 3, 2 (Parts C face), door 7 (Parts A face), CMU openings | 71.89 + 23.89 SF | **0** (doors inside the run) |
| S21-E | none | none | no change |
| S21-S | Windows D1 / D2 | 76.49 SF (windows) | **kept** (window) |
| S21-W1 / W2 | none | none | no change |
| S24-OF / S24-RR / S24-RRS | none (doors 4 / 5 / 6 are in S43) | none | no change |
| S43-OF-S | Door 4 | 23.89 SF each face | **0** both faces |
| S43-RR-S | Doors 5, 6 | 47.78 (Parts C) + 23.89 (R.R. 103) + 23.89 (R.R. 104) | **0** all faces |
| S43-OF-W / OF-E / RR-W, S61-RR | none | none | no change |
| S41-B1V / B1H / B2H / B2V | none | none | no change |
| S42-01..04 | none (header walls: base 6.833 is the header bottom over open passages, not a door) | none | no change |
| EXT-MS1/MS2 piers, HEAD-A-8 | Storefront A (openings_extra) | head face starts at the storefront head (base 11.333) | **kept** (storefront). The vestibule face height 0 is the vestibule soffit (RFI-15), not a door split |
| VH-B1 / VH-B2 / VH-C | Vestibule storefronts B1 / B2 / C (C holds a door) | faces start at the head (base 11.333) | **kept** (storefront head band, not a deduction) |

No face was split at height 0 by a door. Not board, left as they were: Level 5 items (L5-S21-N-B0/B1, L5-S43-OF-S-*, L5-S43-RR-S-A0) and W-4 panels keep the door deduction (finish area, not board).

## Rev3 point 3 - storefront A head wall, interior face per segment

| Segment (A5.2 type A, printed) | Section / detail at this segment | Board on the interior face: from -> to (printed) | Carried |
|---|---|---|---|
| 18'-8" (R.O.) | 1/A5.2 (head callout cut in this segment on the A5.2 type A elevation) | storefront head 11'-4" (A5.2 "11'-4\" (R.O.)"; B.O. SHEATHING EL. 111'-4" 2/A3.1) -> 8" above (1/A5.2 printed 8") = 12'-0" | 18.667 x 0.667 = 12.45 SF 5/8" X + 1/4" + 1 RC row; underside 18.667 x 0.4375 = 8.17 SF 5/8" X + 18.667 x 0.3854 = 7.19 SF 1/4"; 18.667 LF corner bead |
| 8'-0" (HOLD) vestibule 100A | 3/A3.1 (A1.1 section mark in this segment) | 11'-4" -> 11'-4": 3/A3.1 draws the vestibule soffit framing on the head line and no board on the interior face (insulation only); A1.2 100A walls "-", C-3 11'-4". But 3/A3.1 tags this head "HEAD DETAIL 1/A5.2" (8") | **[PENDIENTE] RFI-15**: (A) 0 carried / (B) +5.33 SF 5/8" X face (8.0 x 0.667) + 5.33 SF 1/4" + 8.0 LF RC + 3.50 SF 5/8" X underside + 3.08 SF 1/4" underside + 8.0 LF corner bead / (C) other |
| 12'-0" (R.O.) | 2/A3.1 (A1.1 section mark in this segment) -> HEAD DETAIL 1/A5.2 | 11'-4" -> 12'-0" (2/A3.1 key notes 20 / 33 / 35 short leg; 1/A5.2 8") | 12.0 x 0.667 = 8.00 SF 5/8" X + 1/4" + 1 RC row; underside 5.25 SF 5/8" X + 4.63 SF 1/4"; 12.0 LF corner bead |

RFI-06 = A applied in the overlay (G06): HEAD-A-8 faces with per-segment sources, GWB-HEAD-A-UNDERSIDE 13.42 SF, new QTR-GYP-HEAD-A-UNDERSIDE 11.82 SF (1/4", width 3-1/2" + 7/8" + 1/4" = 4.625"; 1/A5.2 itself draws the 1/4" on the vertical face only), CB-HEAD-A-UNDERSIDE 30.667 LF; piers keep 1/4" + RC in QTR-GYP-EXT-MS / RC-EXT-MS. Images: img_rev3/rev3_A1.1_west_string_sections_per_segment.png, rev3_A5.2_typeA_elevation_segments_head_callout.png, rev3_A5.2_1_head_detail_8in_interior_board.png, rev3_A3.1_2_section_12-0_segment_head.png, rev3_A3.1_3_section_vestibule_8-0_segment_head.png, rev3_A3.1_3_vestibule_head_zoom_5x.png, rev3_A1.2_finish_schedule_100_100A.png.

## Corner ownership

Rules used (SKILL.md, quoted):

- **R70.2**: "Cada esquina L / T tiene UN dueño: un wall llega a la cara exterior del otro y el otro arranca en su cara. Ni esquina sin dueño ni doble. Vale también para exteriores."
- **R70.3**: "La door va DENTRO del run: un R.O. entre dos walls colineales es parte del wall (las doors no se descuentan). Un hueco colineal sin explicar = falla; un cambio de type justo en la door no saca la door de ambos walls."
- The owner itself was read with **R78.35** (the wall whose stud core crosses the corner square in the plan vector runs through; the other dies against it).

| Corner | Node | Owner | Why |
|---|---|---|---|
| S24-OF / S43-OF-W | N36 (T) | **S24-OF** | A1.1 40x vector: the S24 hatch fills the corner square; the S43 inner line stops at the S24 face (322.4 pt). S24-OF length = 11'-0" printed between the S43 inner stud faces + 2 x 4-1/4" (it runs to the S43 outer face). S43-OF-W 8'-0" printed starts at the S24 face (band lo 322.4). Image: img_revision/e_A1.1_S24-OF_x_S43-OF-W_corner_40x.png |
| S24-OF / S43-OF-E | N37 (T) | **S24-OF** | Same pattern as N36; S43-OF-E band lo 322.4 = S24 face. Image: img_revision/e_A1.1_S24-OF_corners_zoom.png |
| S24-RR / S43-RR-W | N40 (L) | **S24-RR** | A1.1 40x: S24 hatch through the corner; S24-RR length includes the S43-RR-W stud + outer board 4-1/4"; S43-RR-W band starts at the S24 face (322.4). Image: img_revision/e_A1.1_S24-RR_x_S43-RR-W_corner_40x.png |
| S24-RRS / S43-RR-S | N42 (L) | **S24-RRS** | A1.1 16x: the S24-RRS hatch runs to the S43-RR-S outer face; length 8'-6" + 3-5/8" printed (1A/A4.1) + 5/8" outer board = 8.854; S43-RR-S band hi 1071.8 = S24-RRS face. Image: img_revision/e_A1.1_S24-RRS_x_S43-RR-S_corner_16x.png |
| S21-S / S24-RR | - (S24-RR end) | **S21-S** | A1.1 40x: the S21-S furring line runs from the east CMU face (318.1 pt) past the S21-E / S24-RR ends (S21-S = 85'-0" CMU face to CMU face, owner of both its corners); S24-RR stops at the S21-S face (band hi 1074.9 = S21-S c0 1074.9). Image: img_revision/e_A1.1_S21-S_x_S24-RR_corner_40x.png |
| S21-E / S24-OF, S24-RR | - | no corner | Parallel walls: the S24 studs stand in front of the S21-E Z-furring (adjacent_to S21-E, S24 band c0 319.2 = S21-E face). R70.2 does not apply; S21-E has board only above the hard lid there (RFI-02) |
| S21-S / S24-RRS | - | no corner | Parallel: S24-RRS stands in front of S21-S (adjacent_to S21-S). R70.2 does not apply |

Observation (not changed): S24-RRS band lo 321.7 reads 0.7 pt (0.08 ft) into the S24-RR band (face 322.4) at N41, where S24-RR is the owner; below the R11 tolerance, `partition_types.avisos = []`.
