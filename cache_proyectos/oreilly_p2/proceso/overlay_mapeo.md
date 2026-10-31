# Overlay mapping - estimator decisions -> this canon (O'Reilly pass 2)

Overlay: `overlay_OReilly_p2.json` (format `overlay.py`, 20 groups, idempotent).
Test: `overlay.aplicar_canon(...)` -> `canon_ov.json` (copy in this folder) -> `validar_canon.py canon_ov.json tools` = **CANON OK**. `canon.py` -> `partition_types.avisos = []`.
Rule followed: the answers were given to another pass's RFI numbers. They were mapped **by content**. Only the decision (A/B) was used. Every quantity below was derived from this set (source N/SHEET + op), not copied from RESPUESTAS_RFI_ESTIMADOR.md.

| Est. # | Estimator decision | Object in this canon | Change applied | Source |
|---|---|---|---|---|
| 01 | A: studs / Z-furring stop under the purlin | RFI-01 (this canon's option **B**). Walls S21-N/E/S/W1/W2, S42-01..04, VH-B1/B2/C. Roof-side faces of S21, S42 Parts B/C, EXT-MS2 Parts B | Heights and roof-side board faces -0.667 ft: **[PENDIENTE] assumed 8" purlin depth per PEMB shop drawing (not printed), estimator decision RFI-01** (rev3; no scaled value). Dependents: QTR-GYP-EXT-MS 175.34, RC-EXT-MS 120.51, CB-S42-HDR-BOTTOM 194.25, JDM-S42-JOINTS 41.30, CJ-S21 87.29, Level 5 items. RFI-01 CLOSED (depth pending shop drawing) | 1/A3.2, 2/A3.2, 1/A3.4 |
| 02 | A: S24 Z-furring to the eave + board above the hard lid | RFI-02 (option A). The height-0 faces of S21-E (behind S24-OF / S24-RR) and of S21-S (behind R.R. 104) | Those faces now carry board from 9'-0\" (top of the 7/A4.2 hard lid) to the furring top: 4.792 / 4.792 / 4.889 ft, board_base 9.0. RFI-02 CLOSED | 7/A4.2, 2/A3.2, 1/A3.2 |
| 03 | A: S42 header extension included (as A1.1) | RFI-14 (raised in part A d). S42-02 continuation 6.715 ft is already in the canon | No quantity change. RFI-14 CLOSED option A | A1.1 |
| 05 | B: no board above the hard lid joists (IBC 703.2) | Hard lid 7/A4.2 (key 6 also points at the top of the joists). The canon carries only the undersides (GWB-CLG-*) | Confirmed, delta 0. Note added to takeoff.inputs_notas | 7/A4.2 |
| 06 | A: 5/8" X over 1/4" over RC 087F125-33 on piers and head + underside (5/8" X, 1/4", corner bead) | RFI-06 (option A, 8" above the head). QTR-GYP-EXT-MS / RC-EXT-MS (piers + head face), HEAD-A-8 faces, GWB-HEAD-A-UNDERSIDE | rev3: HEAD-A-8 faces per segment (18'-8" 1/A5.2, 12'-0" 2/A3.1 -> 1/A5.2: 11'-4" to 12'-0"); + misc QTR-GYP-HEAD-A-UNDERSIDE 11.82 SF; + trim CB-HEAD-A-UNDERSIDE 30.667 LF. Vestibule 8'-0" segment: new RFI-15 [PENDIENTE] (A 0 / B +5.33 SF) | 1/A5.2, 2/A3.1, 3/A3.1, A5.2 |
| 07 | A: W-4 panels on the 4 walls of each restroom | frp_none_reason (W-4 was excluded as finish) | + misc W4-PANELS-103 / -104, 253.77 SF each = 2 x (7'-10\" + 8'-6\") x 8.5 - door R.O. 3.333 x 7.167 (family "sanitary wall panels (printed)"). frp_none_reason reworded | A1.2, 1A/A4.1, A5.1 |
| 09 | A: + 600S200-54 by spacing, L4x4x3/16, 2x2x14ga clips | RFI-10 (option B, partly) | + PEMB-6IN-S42-02 70.0 LF (1/S5.1 @ 24\", 14 x 5.0). + PEMB-6IN-S42-01 55.0 LF (4/S5.1 @ 48\", 11 x 5.0). + L4X4-S42-03 12 pcs (2/S5.1, one per purlin crossing, purlin bay scaled 5.0 ft). The 2x2x14ga clips stay CLIP-2X2-S42-03 = 14 (this canon's count, one per S42-03 kicker; the other pass's count was not copied). RFI-10 CLOSED | 1/S5.1, 2/S5.1, 4/S5.1 |
| 10 | A: continuous blocking 14/A4.1 + fixture backing | RFI-12 (accessories part) | + blocking BLK-GRAB-BARS 18.0 LF FRT (grab bars B 48\" + C 18\" + D 42\" per restroom, 10/A4.1 key 13). The continuous 14/A4.1 blocking has no object: see overlay_sin_objeto.md | 10/A4.1, A4.1 accessory schedule |
| 11 | A: corner bead at header bottoms + J molding against the roof | CB-S42-HDR-BOTTOM (already carried). Board faces ending at the roof in C-2 areas | + trim J-ROOF-EXPOSED 352.82 LF j_bead (sum of the S21 / S42 / EXT-MS2 Parts B/C and plenum faces, op lists each) | A1.1 note 3.C, A1.2 |
| 12 | A: + 3\"x16ga diagonal strap at S41 | RFI-07 (option B) | + misc STRAP-S41 96.91 LF = 2 sides x SQRT(L^2 + 12^2) for the 4 S41 walls. RFI-07 CLOSED | A1.1 note 2.B |
| 13 | A: metal headers at CMU openings = 0 | Doors 2 / 3 / 7, windows D1 / D2: header steel_by_others (masonry lintel) | Confirmed, delta 0. Note added | S4.1 |
| 14 | A: vestibule heads 600S162-43 (18 ga) | RFI-13 (option A carried). VH-B1 5.667 + VH-B2 5.667 + VH-C 8.75 = 20.08 LF (this canon's lengths) | RFI-13 CLOSED, delta 0 | 3/A3.1 key 8 |
| 15 | B: Level 5 under semi-gloss W-2 (GA-214 / ASTM C840) | accesorios_none "Level 5 finish" | Removed that line. + constants.level5_tags ["W-2"]. + 39 level5_items (6582.90 SF, rev3 heights under an assumed 8" purlin): W-2 faces of Parts A / B / C, office and plenum. Parts A capped at the ACT 11'-6\". Base B-1 4\" deducted where scheduled. Openings deducted | A1.2 |
| 16 | B: + 1-1/2\" runner top and bottom of the S21 Z-furring (ASTM C754) | S21 walls (no track in the canon) | + misc ZF-RUNNER-S21 564.58 LF = 2 x 288.625 - doors 12.667 | S21/A1.1 |
| 17 | A: FRT blocking D1 / D2 stays | BLK-WIN-D 58.92 | Confirmed, delta 0 | 12/A5.2, 13/A5.2 |
| 18 | A: + control joints in S21 | S21-N / S21-E / S21-S (> 30 ft) | + misc CJ-S21 87.29 LF (rev3) = 2 joints per wall x the board height under the purlin | A1.1 note 3.A |
| 19 | B: Type X W.R. behind the janitor sink wet fixtures | S43-RR-W break-area face (12/A4.1: janitor sink, eye wash) | board 5/8 type X -> 5/8 type X WR. Reclassification only, total SF unchanged | 12/A4.1 |
| 20 | A: FCB43.5 one per stud | FCB-CORN-S 30 (3 rows x 48\" horizontal) | 84 pcs = 3 rows (1/S5.3 key 23) x 28 studs @ 16\" (key 22) | 1/S5.3 |
| 22 | Keep excluded: FRT parapet nailers = Div. 06 | RFI-12 (nailers part) | EXCLUDED (takeoff.alcances ALC-FRT-NAILERS). RFI-12 partly closed. Still open: sign backing (A3.1 key 31) and extinguisher blocking (A4.2 key 21) | A3.1 key 11, 1/S5.3 key 4 |
| 24 | A: shutters not carried, with note | A5.2 general note H (no item in the canon) | Note only (takeoff.inputs_notas SHUTTERS), delta 0 | A5.2 |
| 25 | B: deflection per A1.1 note 2.C; deep-leg stays | deflection_clips.note_source + DLT-S42-FULL | Confirmed, delta 0 | A1.1 note 2.C, 3/S5.1 |
| (user) | RFI-13 closed by est. 14 | RFI-13 | See 14. This canon's 20.08 LF used | 3/A3.1 |
| (user) | Exclusions: fasteners, MEP / electrical / civil / cabinets | fasteners_excluded, mep_sweep, accesorios_none | Already in the canon, no change | - |

Not decided (stay open): RFI-03 kicker length, RFI-04 joist span, RFI-05 cornice, RFI-08 board behind box-outs, RFI-11 wall ties / wind beam clips, RFI-12 remainder (sign backing / extinguisher blocking). Already closed in the other pass, no object here: 04, 08, 21, 26-anchors, 27.

**Total: 21 decisions applied (20 groups; 10 and 22 share the RFI-12 group). 4 have no object (overlay_sin_objeto.md).**
