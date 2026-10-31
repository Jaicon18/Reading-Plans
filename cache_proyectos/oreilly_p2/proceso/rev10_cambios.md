# Rev10 changes: O'Reilly Auto Parts, Evans CO, pass 2 (element 6: trim, control joints, jamb return, compound / tape + RFI-25 / RFI-26)

Backups: `takeoff_canon_AB_rev9.json` (canon before rev10) and `overlay_OReilly_p2_rev9.json` (overlay before rev10).
Edited files:
- `takeoff_canon_AB.json`: 7 new trim items, the JDM split, and new RFI-25 / RFI-26 / RFI-27.
- `overlay_OReilly_p2.json`: G01 adds DRMF under the purlin. G18 now holds CJ-S21, CJ-S42-01 and CJ-VEE-PIERS. G09 and G10 got notes. New group G-rev10 holds the taping note.
- `canon_ov.json` was regenerated with `overlay.aplicar_canon`, which is idempotent.
- `overlay_mapeo.md` and `overlay_sin_objeto.md` were updated.

Checks:
- `validar_canon.py` reports CANON OK on both canons.
- `tools/canon.py canon_ov.json /tmp/rev10_out` exits with rc 0 and `partition_types.avisos = []`. The AVISO count is the same as rev9.
- Rule #0: nothing was scaled. Crops are circled and stored in `img_rev10/`; the scripts are in `img_rev10/_work/` (`r.py`, `annot_rev10.py`, `edit_rev10.py`).

| # | Item | Before | After | N/SHEET | Image |
|---|---|---|---|---|---|
| a | 14/A4.1 key 12 | no object (overlay_sin_objeto) | **0 carried + new RFI-25.** The key list says "12 WALL CONSTRUCTION, REFER TO FLOOR PLAN FOR TYPES", which is unambiguous (key 13 is the FRT blocking). The A1.1 mark 14/A4.1 looks at S42-03 (50'-4"), and key 12 has 2 leaders to the header band 106'-10" -> 111'-6". A1.2 note 6 calls 14/A4.1 the typical paint scheme. RFI-25 B (FRT continuous blocking, other pass): 2 rows x 50.333 = **+100.67 LF** (1 row +50.33) | A4.1 keys, 14/A4.1, A1.1, A1.2 n.6 | rev10_a_A4.1_key12_legend_14_S42-03.png |
| b | Kicker clips 2"x2"x14ga / L4x4x3/16 | 14 / 12 | **14 / 12 unchanged + new RFI-26.** No count is labelled on S5.1 or S4.1. 2/S5.1 (S42-03) draws a clip at each kicker top (@ 48" printed), so 14. The L4x4 has no spacing, so 12 (RFI-19 A, user decision). 1/S5.1 (S42-02) draws the kicker coped and screwed (2) #10, with no clip and no L4x4, so the plan resolves S42-02 = 0. RFI-26 B: 22 clips (+8) and 19 L4x4 (+7, 12 + ROUNDUP(25.455/5)+1) | 1-4/S5.1, S4.1 key plan | rev10_b_S5.1_1_2_3_4_S4.1_clip_L4x4_counts.png |
| 1 | CB-7A42-TOP / CB-S41-BOXES / CB-S42-HDR-BOTTOM / CB-HEAD-A-UNDERSIDE | 79.73 / 24.0 / 194.25 / 30.667 | **Unchanged, verified.** 7/A4.2 key 7. The S41 tops at 12'-0" sit above the ACT 11'-6". 6/A4.2: 151.58 + 27.33 + 15.34. 1/A5.2 head corner | 7/A4.2, 4/A4.2, 6/A4.2, 1/A5.2 | rev10_p1p2_A4.2_2_6_7_reglet_corner_bead.png |
| 1 | Pier / storefront A jambs | 0 | **+22.67 CB-SF-A-PIER-JAMBS** (2/A5.2 board returned to the frame: 2 x 11'-4") + **+53.33 CSB-SF-A-FRAME** (casing at the frame: head 30.667 + jambs 22.667). Decision 26 still keeps the return SF out; the drawn corner gets trim | 2/A5.2, 1/A5.2, A1.1 3.C, rule 53.1 | rev10_p1_A5.2_1_2_3_storefront_vestibule_edges.png |
| 1 | Vestibule heads / VH underside (11.28 SF) | 0 | **+20.08 CB-VH-UNDERSIDE** (Parts A face to underside corner: 5.667 + 5.667 + 8.75) + **+46.67 CSB-VEST-FRAMES** (C-3 ceiling perimeter at the frames 27.33 + Parts A underside edge at B1 / B2 / C 19.33) | 3/A5.2, 10/A5.2, A1.2 | rev10_p1_A5.2_1_2_3_storefront_vestibule_edges.png |
| 1 | Exterior doors 2 / 7 / 3 | 0 | **+35.33 CB-DOORS-2-7 + 35.33 CSB-DOORS-2-7** (1-4/A5.1: board returned around the FRT 2x4 to the HM frame, head + 2 jambs, R.O. 3.333 x 7.167). **+22.0 J-DOOR-3-CLADDING** (5/6/A5.1: board stops at the 24 ga cladding, 6 + 8 + 8). Interior doors 4 / 5 / 6: the HM frame wraps the wall, so no trim | 1-6/A5.1 | rev10_p1_A5.1_doors_2_7_3_board_edges.png |
| 1 | S42 free ends / EXT-MS pier outer edges | - | Already in CB-S42-HDR-BOTTOM (the free ends). The pier outer edges are inside corners or sit at the 7/A3.2 joint, so no bead | A1.1, 7/A3.2 | - |
| 2 | J-ROOF-EXPOSED | 352.82 | **Unchanged, verified.** Sum of 14 faces = 352.823. Only Parts B / C (C-2 exposed) and the plenum faces above the hard lid are included. The Parts A faces (C-1 ACT 11'-6") are excluded, and so are the S43 9'-0" tops (those take corner bead) | A1.1 3.C, A1.2 schedule | rev10_p2p3_A1.1_3A_3C_A1.2_ceilings.png |
| 2 | JDM-S42-JOINTS | 41.30 (DRMF + JDM in one row) | **JDM 41.30 + new DRMF-S42-JOINTS 41.30 (shadow_molding).** 2/A4.2 draws one DRMF-625-75 on one board edge and one JDM-625 on the other, so there are 2 pieces per LF of joint | 2/A4.2 key 9 | rev10_p1p2_A4.2_2_6_7_reglet_corner_bead.png |
| 3 | CJ-S21 | 87.29 (30 ft rule, 2 per wall) | **188.54.** A1.1 3.A says to locate the joints at the masonry CJs shown on the elevations. A2.1 key 23 shows N 5 x 14.844 + E 5 x 13.958 + S 3 x 14.844, carried at full board height (positions are not dimensioned). New **RFI-27** B (30 ft rule) = -101.25 | A1.1 3.A, A2.1 key 23 | rev10_p3_A2.1_key23_masonry_CJ_S21.png |
| 3 | S42 control joints | 0 extra | The 2/A4.2 joints are already reglet joints and are not duplicated. **+26.51 CJ-S42-01**: 38'-8" > 30 ft with no 2/A4.2 joint, so 1 joint x (12.0 + 14.505) (RFI-27) | A1.1 3.A, A1.1 | rev10_p2p3_A1.1_3A_3C_A1.2_ceilings.png |
| 3 | 7/A3.2 vee joint S21 / pier | 0 | **+27.73 CJ-VEE-PIERS**: north pier 12.0 (printed, marked on A1.1) + south pier 15.729 (same assembly, not marked, conservative, RFI-27) | 7/A3.2, A1.1 | rev10_p3_A3.2_7_vee_joint_A1.1_piers.png |
| 3 | Ceilings > 2500 SF / change of direction | - | Not applicable. The GWB ceilings are 45-86 SF. "Where framing or furring changes direction" is read as the ceiling clause (ASTM C840). Control joint family **87.29 -> 242.78 LF** | A1.1 3.A, A1.2 | - |
| 4 | Jamb return D1 / D2 | 11.78 SF; trim 117.84 | **Unchanged, verified.** 11/12/13/A5.2: board returned at head, sill and 2 jambs. 2 x (11.365 x 2 + 2 x 3.365) = 58.92 x 0.2 = 11.78 SF (decision 26 A). Trim 2 x 58.92 (corner bead + casing) is consistent | 11-13/A5.2 | rev10_p4_A5.2_11_12_13_D1_D2_jamb_return.png |
| 5 | Joint compound / tape | 585.08 lb / 3,006.67 LF on 8,126.14 SF | **Unchanged.** SKILL.md A9-A11 says yield x (5/8" + MR + 3/8"), excluding sheathing, glass mat and FRT. It has no exclusion for board behind W-4 panels (555.34 SF) or above the ACT. The set prints no fire-tape note and no finish level (Paso 2 / Alturas checklist: declare it), so Level 4 is declared everywhere. Note TAPING-BASE added (G-rev10). Level 5 6,432.72 SF stays a separate row | SKILL.md §12 A9-A11, l.1287, l.1349; A1.2 | - |

Family totals (canon_ov):
- Metal trim: 840.61 -> **1,117.32 LF** (+276.71).
- Control joint: 87.29 -> **242.78 LF**.

Unchanged: joint compound 585.08 lb, joint tape 3,006.67 LF, Level 5 6,432.72 SF, jamb return 11.78 SF, clip angle 26 pcs, FRT blocking 499.16 LF.

New RFIs:
- **RFI-25**: 14/A4.1 key 12. A = 0 carried; B = +100.67 LF.
- **RFI-26**: clip and L4x4 counts. A = 14 / 12 carried; B = +8 / +7.
- **RFI-27**: control joint count. A = 242.78 carried; B = -101.25.
