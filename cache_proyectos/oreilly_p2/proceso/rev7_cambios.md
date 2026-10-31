# Rev7 changes: O'Reilly Auto Parts, Evans CO, pass 2 (element 3: stud ties, control joint studs, Z-furring behind S24)

Backups: `takeoff_canon_AB_rev6.json` and `overlay_OReilly_p2_rev6.json`.

Edited files:
- `takeoff_canon_AB.json` (the reading):
  - new misc TIES-HEAD-A
  - new misc STUD-DBL-CJ-S42
  - RFI-11 rewritten
- `overlay_OReilly_p2.json`: new group **G-rev7** with the user decisions:
  - RFI-19 = A and RFI-03 = A, both CLOSED
  - ops of PEMB-6IN-S42-02 / -01, L4X4-S42-03 and KICKERS-S42-HDR
  - new misc CONT-6IN-S42-03-KICKER
- `overlay_mapeo.md`: new user rev7 row; the "not decided" line is updated.
- `canon_ov.json`, regenerated with `overlay.aplicar_canon`. Applying it twice gives the same result.

Checks:
- `validar_canon.py` reports CANON OK on both files.
- `tools/canon.py canon_ov.json /tmp/rev7_out` gives `partition_types.avisos = []`.

Family totals that changed against rev6:
- **3-5/8" stud:** 1865.52 -> **2051.54 LF** (+140.0 ties, +46.02 doubled studs)
- **6" stud:** 1299.57 -> **1349.90 LF** (+50.33 third CONT line)
- **1-1/2" Z-furring:** unchanged at 2517.5 LF

Rule #0 applies: no length was scaled. Every count and length below comes from printed dimensions, spacings and elevations. Each crop in `img_rev7/` was rendered with pymupdf from `bidset_SIN_MARKUPS.pdf`, circled, then reopened and checked.

| # | Item | Before (rev6) | After (rev7) | Printed dimension / N/SHEET | Image |
|---|---|---|---|---|---|
| 1 | TIES-HEAD-A (new, 3-5/8" stud family, 43 mil in the op) | In RFI-11, not carried | **140.0 LF**: 362S162-43 ties @ 48" O.C. across each 6" + 8" stud pair of HEAD-A-6 / -8.<br>**Pairs:** @ 16" over the printed 38'-8" R.O. = 464/16 + 1 = 30.<br>**Rows:** ROUNDUP(9.333/4) + 1 = 4.<br>**Tie length:** 1'-2" (printed 6" + 8"; the tie is drawn across the whole pair).<br>120 ties x 1.167 = 140.0 LF | 3/S5.3 key 19 \"3-5/8\"x18 ga METAL STUD TIES (362S162-43) @ 48\" O.C.\"; 1'-2\" (6\" + 8\") on 3/S5.3; S4.1 framing key plan cuts 3/S5.3 twice on the storefront A head; 2/A3.1 111'-4\" to 120'-8\"; A5.2 type A 38'-8\" | rev7_p1_S5.3_3_ties_key19_1-2.png, rev7_p1_S4.1_keyplan_3S5.3_cuts_head.png |
| 1 | Pier ties EXT-MS1 / EXT-MS2 | In RFI-11 | **Not carried, [PENDIENTE] RFI-11.**<br>3/S5.3 is not cut at the piers, and 1/A3.1 draws and keys no ties.<br>**(A)** 0<br>**(B)** +98.0 LF = 2 piers x 6 pairs (ROUNDUP(72/16) + 1) x 7 rows (ROUNDUP(20.667/4) + 1) x 1'-2\"<br>**(C)** other.<br>The FCB43.5 wind beam clips stay in RFI-11 as well: B = +84 pcs. The other reading's 238.07 LF = head 140.0 + piers 98.0 (204 ties x 1.167) | 1/A3.1 (keys 6 / 7 \"refer to structural\"; A3.1 key 19 = sheathing); S4.1 key plan; 3/S5.3 key 16 \"EL. SEE PEMB DRAWINGS\" | rev7_p1_A3.1_1_pier_no_ties.png |
| 2 | STUD-DBL-CJ-S42 (new, 3-5/8" stud family) | Not carried. Free nodes N22 / N23 / N25 / N26 carried only 1 end stud each | **46.02 LF**: +1 stud on each side at the 2 S42 control joints 2/A4.2 \"ABOVE\". Each extra stud is at its own wall's stud height:<br>S42-01 14.505 + S42-02 7.672 + S42-03 8.202 + S42-04 15.644 = 46.02 LF.<br>The full-height side is cut at the full-height wall and the header side at the header. That is why it is not 2 x (14.505 + 15.644) = 60.30 | A4.2 key note 4 \"362S162-33 COLD FORM METAL STUDS DOUBLED AT CONTROL JOINT\"; 2/A4.2 draws 2 studs on each side, \"framing to be independent across joint\"; A1.1 S42 joint tags 2/A4.2 | rev7_p2_A4.2_2_key4_studs_doubled.png |
| 2 | S21 control joints (CJ-S21) / 7/A3.2 S21-pier joint | CJ-S21 87.29 LF of joint, no framing | **No change.** No doubled studs or extra Z-furring is printed for S21: 2/A4.2 key 4 is a 362S162-33 stud joint, and 7/A3.2 shows only a vee joint between the S21 board and the pier board. Nothing was invented | 7/A3.2; A1.1 note 3.A; 2/A4.2 | rev7_p2_A3.2_7_S21_vee_joint_no_double.png |
| 3 | Z-furring behind S24 | S21-E 84.646 x 13.958 and S21-S 85.0 x 14.844 avg, both full length including the S24 zones | **Confirmed, no change.**<br>**(a) Heights.** The Z-furring behind S24 runs to the eave under the purlin (RFI-02 = A, RFI-01).<br>- East (S24-OF / S24-RR): T.O. LOW EAVE 114'-7 1/2\" - 8\" = 13.958.<br>- South (S24-RRS, R.R. 104 at the east end of the rake wall): local 14.722 - 0.667 = 14.055 for the board above the 9'-0\" hard lid. S21-S studs use the rake average 14.844, which is exact for the wall total.<br>- E and S differ correctly.<br>**(b) No double count.** The Z-furring of S24 lives in S21-E / S21-S. The S24 walls carry only 362S162-33 studs to 8'-6\": S24-OF 59.5 + S24-RR 102.0 + S24-RRS 51.0 = 212.5 LF of 3-5/8\".<br>**(c) Z-furring total:** 2517.5 LF = S21-N 807.77 + S21-E 642.07 + S21-S 753.08 + S21-W1 94.37 + S21-W2 220.21.<br>The other reading splits it as S21 250.7 LF of wall plus a separate S24 Z-furring of 321.55 LF ((7 + 10) x 13.958 + 6 x 14.055). That restarts the count (1 + ROUNDUP) in each S24 zone, although the furring is continuous along the CMU. The S24 zones here are counted inside the continuous S21 runs, about 265 LF (28.531/2 x 13.958 + 9.357/2 x 14.055) | A1.1 type S24 (150ZF125-18 @ 24\" on CMU, no height note; \"STUDS TO 8'-6\" A.F.F.\"); 7/A4.2 8'-6\" + 6\" = 9'-0\"; 2/A3.2 T.O. LOW EAVE 114'-7 1/2\"; 1/A3.2 T.O. HIGH EAVE 116'-4 3/4\" | rev7_p3_A1.1_S24_type_7A4.2_hard_lid.png |
| D | RFI-19 (user decision) | [PENDIENTE], A carried | **CLOSED = A.** Delta 0: PEMB-6IN-S42-02 70.0 LF, PEMB-6IN-S42-01 55.0 LF and L4X4-S42-03 12 pcs stay. The ops now say \"RFI-19 = A (user decision rev7, CLOSED)\" | 1/S5.1, 2/S5.1, 4/S5.1 | img_rev6/rev6_p1p2p3_S5.1_1_6in_24oc_no_length.png |
| D | RFI-03 (user decision) | [PENDIENTE], A carried | **CLOSED = A** (45 deg kickers). Delta 0: KICKERS-S42-HDR 155.54 LF stays | 1/S5.1, 2/S5.1 | img_rev6/rev6_p1p3_S5.1_2_5-0_kicker_reach_purlin_beyond.png |
| D | CONT-6IN-S42-03-KICKER (new, 6" stud family) | Noted only in rev6, not carried | **50.33 LF**: the third continuous 600S200-54 line at the kicker top of S42-03, run = S42-03 printed 50'-4\". The 2 lines \"each side\" at the wall top stay in CONT-6IN-S42-03 (100.67 LF) | 2/S5.1 \"CONT. 6\"x2\"x16ga STUD (600S200-54) FASTENED TO PURLIN W/ (4) #10 SDS\"; A1.1 50'-4\" | rev7_p4_S5.1_2_cont_6in_kicker_top.png |

Note for the tool owner, no quantity changed: `studs_out` counts HEAD-A-6 / -8 at 31 studs, because 38.667 ft is a rounded decimal and gives 29.0003 spaces. The printed 38'-8\" = 464\" / 16\" gives exactly 29 spaces, so 30 studs. TIES-HEAD-A uses the exact 30 pairs.
