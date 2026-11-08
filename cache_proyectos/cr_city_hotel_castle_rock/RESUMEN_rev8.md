# RESUMEN rev8 — CR City Hotel (review of ALL the walls + ceiling labels)

Orders of the user (via COORDINACIÓN, 2026-11-07): "revisa todos el rcp plans del proyecto" and "ahora haz una revision de todas las muros del proyecto, absolutamente todos". Each point re-done on the drawings; images in Auditoria/auditoria_rev8/.

## Walls
1. QUANTITY - W.4-L4-21 (Men 418): 1.06 -> 2.13 ft. On 3/A7.50 the wall lines run y 1264.4-1302.8: 38.4/18 = 2.13 ft (= A2.04 (1222.2-1203.0)/9). The audit move to A7.50 had divided an A2.04 length placed on A7.50 by 18. Sweep of every wall (LF vs path / scale of its sheet): no other case.
   W.6-L4-14: 15.54 -> 15.51 ft (its operation 261.0/18 + 18.1/18 = 15.51).
2. MARKUPS ON THEIR WALL - every markup now follows the measured geometry (each piece / jog = its segment): W.6-L4-12, W.6-L4-14 (jogs, 1/A7.55), FW.4-L4-15 (3 runs on 7/A6.01), FW.2-L4-07, FW.2-L2-09, FW.2-L4-01, FW.2-L2-13 (pieces either side of the opening), FW.2-L2-02, FW.2-L4-04, CH.6-L4-01/03, W.62-L4-07, and by sweep W.62-L2-08 B/C, W.62-L2-06 A/B, W.62-L2-07 B/C, W.4-L2-08 B, W.4-L2-15 A, W.4-L2-42 A/B, W.4-L3-15 A/B, W.62-L4-12, W.62-L4-13 B/C. DW.4-L4-04 B/C: end at the face of a perpendicular wall interrupted by its door (written exception).
3. TAGS - W.6.1 tags of A7.30 / A7.45 and XW.6.2 tags of A2.01 linked to their walls; PC0186 / PC0187 = walls inside KITCHEN 100 (F&B, not in this permit); PT0153, PT0347, PT0351 already had a disposition (excluded walls with printed reason: F&B; retail RFI-05).
   NEW wall W.6-L1-32: L-shaped wall at the bar 107 traffic door (1/A7.30, tag W.6.1 PC0176), 5.58 ft x 12'-0", one face of 5/8" Type X W.R. (restrooms vestibule, like W.6-L1-09; the bar face is F&B).
4. A2.01 candidates: waiting for COORDINACIÓN's list (rev9).
5. Openings inside the run on A7.30 / A7.45 / A7.50 / A7.55 now written in the Source (not deducted, U-057, with the solid length). W.6-L1-25: Review Item (double door 120.1 fills the 8.01-ft run; -380.2 SF Type X if deducted). The 0'-2 7/8" strips are explained in the estimator guide (W.R. board above the 9'-0" cement board in NON-rated bath walls).

## Ceilings
- CLG 0'-0" labels fixed: L4 406 Cleaning 8'-11 1/4" (1/A5.06, RS-1 at the underside of the roof framing); L2 Elec 221 9'-10 5/8" (FS-1, 7/A7.23).
- Real room contours for the 44 ceilings[] polygons that are bbox / locator / box today: rev9 (each room read in vectors with an image and area check, as done in O1).

## NET delta rev7 -> rev8
Type X -0.60 SF (W.6-L4-14) · Type X W.R. +86.08 SF (W.4-L4-21 +19.12; W.6-L1-32 +66.96, W.R. like the other restroom-vestibule walls, e.g. W.6-L1-09) · corner bead -17.88 LF (the false free end of W.4-L4-21) · compound +6.16 lb · tape +31.63 LF.

## New gates (all projects)
CE_MARKUP_EN_WALL (every vertex of a wall markup on its drawn band, <= 4.6 pt; exception only with markup_check_note), CR-R8-C (no ceiling without height), canon.py / markups_bluebeam accept walls in measured pieces (`paths`).
