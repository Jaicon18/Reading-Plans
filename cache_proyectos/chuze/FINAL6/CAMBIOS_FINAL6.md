# CAMBIOS FINAL6 - Chuze Fitness Austin Bluffs (FINAL5 -> FINAL6, 2026-11-03)

Why: the delivery gate (compuerta_entrega.py, BE-121) compared every markup Depth against the PRINTED height of its source and found heights stored rounded in the canon (22'-10" as 22.83 ft, 14'-5" as 14.42 ft, 12'-1" as 12.083 ft). tools/alturas_exactas.py (R80f.20) replaced 278 rounded heights with the exact ft-in value before canon.py; every quantity was then recomputed by the full tool chain (bitacora). No length, type or RFI decision changed. Also recomputed with the exact heights: the B.O. deck constant and the 15 ceiling hanger drops (hanger wire), and 14 precomputed items written with 22.83 (head C kickers, control joints, Retail Storage 126 studs to deck; +0.17 LF). Second change (same gate, BE-122 materials vs Partition Type Schedule): 7 type-A walls carried one board face while A/A301 prints '- BOTH SIDES'; the second face (plumbing chase / 9-1/2" gap, A424) is now loaded with the same MR board and height as face A: A-A424-12, -12r, -13, -13r, -14, -14r, A-A424-6 (+218.42 SF MR). Faces in closed cavities (112.49 SF) are a Review Item with the alternative.

## 1. Heights made exact (count of values)

| Stored | Exact | Printed | Count |
|---|---|---|---|
| 22.83 | 22.8333 | 22'-10" | 173 |
| 22.833 | 22.8333 | 22'-10" | 31 |
| 14.83 | 14.8333 | 14'-10" | 11 |
| 12.083 | 12.0833 | 12'-1" | 10 |
| 7.17 | 7.1667 | 7'-2" | 10 |
| 13.83 | 13.8333 | 13'-10" | 8 |
| 12.583 | 12.5833 | 12'-7" | 6 |
| 1.98 | 1.9792 | 1'-11.75" | 6 |
| 12.83 | 12.8333 | 12'-10" | 4 |
| 10.83 | 10.8333 | 10'-10" | 3 |
| 14.33 | 14.3333 | 14'-4" | 3 |
| 14.42 | 14.4167 | 14'-5" | 3 |
| 12.58 | 12.5833 | 12'-7" | 2 |
| 12.08 | 12.0833 | 12'-1" | 2 |
| 7.167 | 7.1667 | 7'-2" | 2 |
| 10.083 | 10.0833 | 10'-1" | 1 |
| 11.33 | 11.3333 | 11'-4" | 1 |
| 4.6 | 4.5833 | 4'-7" | 1 |
| 3.6 | 3.5833 | 3'-7" | 1 |

## 2. Delta per material (Material Summary, NET before waste / Purchase)

| Material Summary row | Unit | FINAL5 Net | FINAL6 Net | Delta Net | FINAL5 Purchase | FINAL6 Purchase |
|---|---|---|---|---|---|---|
| 2-1/2" stud | LF | 2,009.04 | 2,009.34 | +0.30 | 2,310.40 | 2,310.74 |
| 6" metal stud (LF of material) - per source | LF | 10,858.76 | 11,008.73 | +149.97 | 12,487.57 | 12,660.04 |
| 6" metal stud (LF of material) - 600S125-30 | LF | 388.11 | 388.17 | +0.06 | 446.33 | 446.40 |
| 3-5/8" metal stud (LF of material) - per source | LF | 3,170.24 | 3,170.59 | +0.35 | 3,645.78 | 3,646.18 |
| 3-5/8" metal stud (LF of material) - 362S125-30 | LF | 259.56 | 259.50 | -0.06 | 298.49 | 298.43 |
| 3-5/8" metal stud (LF of material) - 362S162-54 ASTM A1003 structural grade, G60 (05 40 00 1.1.A.3, 2.3.B, 2.6) | LF | 8,953.56 | 8,954.65 | +1.09 | 10,296.59 | 10,297.85 |
| Ceiling / soffit track (size per source, see Where it comes from) | LF | 567.58 | 599.61 | +32.03 | 652.72 | 689.55 |
| Bracing 1-1/2" C.R. channel | LF | 6,301.09 | 6,317.61 | +16.52 | 7,246.25 | 7,265.25 |
| Hanger wire | LF | 2,497.64 | 2,498.24 | +0.60 | 2,872.29 | 2,872.98 |
| 5/8" gypsum board, Type X MR (MOISTURE RESISTANT, 09 29 00 2.3.E) | SF | 5,483.88 | 5,831.23 | +347.35 | 5,812.91 | 6,181.10 |
| 5/8" gypsum board, Type X | SF | 58,393.09 | 57,241.60 | -1,151.49 | 61,896.68 | 60,676.10 |
| 5/8" gypsum board, Type X W.R. (water resistant) | SF | 1,493.04 | 1,493.20 | +0.16 | 1,582.62 | 1,582.79 |
| METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim - curved-edge cornerbead, notched / flexible flange (09 29 00 2.6.A.2.g) | LF | 62.20 | 62.72 | +0.52 | 71.53 | 72.13 |
| METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim - corner bead | LF | 332.52 | 342.59 | +10.07 | 382.40 | 393.98 |
| Control joint, gypsum board walls (ASTM C840, 30 ft max) | LF | 363.93 | 363.99 | +0.06 | 418.52 | 418.59 |
| Joint compound - setting-type taping and sandable topping (09 29 00 2.7.C) | LB | 4,706.64 | 4,648.75 | -57.89 | 4,706.64 | 4,648.75 |
| Joint tape, paper | LF | 24,186.90 | 23,889.43 | -297.47 | 24,186.90 | 23,889.43 |

Rows changed: 17 of 67. Partition LF unchanged (lengths were not touched).

## 3. Gate tools fixed (skill v81cf24, BE-124)
- R80f.17 revision_markups: the label 'SF board' (BE-117) is checked against the Excel Board (SF), not LF x H; printed height + printed increment of the chain ('10'-0" AFF + 6"').
- R80f.18 revision_materiales: schedule board = primary + conditional by room; heavier board / gauge / closer spacing with a cited source = AMBER; layers not printed are not demanded; END face is not a side; canon MR = Type X MR row.
- R80f.19 compuerta_entrega: reglas.py checks the DELIVERED markups PDF.
- R80f.20 alturas_exactas.py (this change).

## 4. Later changes in FINAL6 (delivery gates v25 / v27 and back-check)
- **Demolition (R-ALC-04), new Material Summary row**: 34 AD101 runs (D0.35 / D0.45 dashed partitions of the legend 'EXISTING TO BE REMOVED' + 5 solid stubs that a D0.35 leader points at), 476.37 LF / 21,653.88 SF (L x H x 2 faces, H = B.O. deck 22'-10" per 6/A429.B / RFI-01; D0.45 from 60" A.F.F.). The grid-4 run stops at the D0.56 storefront glazing (storefront is not ours). Corridor walls at the restrooms (D0.35 + D0.07 leaders): per the legend the dashed upper part is demolished and the solid lower part stays and is re-boarded (EX-17 6.01 LF, EX-18 1.67 LF, both 16.53 LF before: Type X board -1,159.02 SF, with its compound / tape; Review Item with the delta of each alternative). D0.04 is drawn with the storefront glazing symbol: not loaded, Review Item with its delta. D0.32 column furring, D0.17 soffits and general note 5 furring: not dimensioned, Review Item.
- **BE-03 (wet rooms in MR)**: A-A425.A-1 face A (135 WOMEN'S LOCKER ROOM, 71.65 SF) and A-A424.A-1 face B (men's locker entry, 79.06 SF) from 5/8" Type X to 5/8" MR (A111 note 3): MR +150.71 SF, Type X -150.71 SF.
- **BE-06 (headwall bottom)**: A-A422.A-1 (15/A502 HEADWALL SECTION - ACT) bottom board 6" stud + 2 x 5/8" = 7.25" x 13.33 LF = +8.05 SF Type X (with its joint compound / tape).
- These are inside the MR / Type X / joint compound / joint tape deltas of section 2.
- Texts and evidence only (no quantity): height labels (CONFIRMED / DERIVED / PENDING; the B.O. deck 22'-10" is DERIVED everywhere), circled height images, one markup per straight run (U-120), BE-HF05 one Partition Takeoff row per Wall ID.

## Soffit sides - second independent reading (Z7) resolved (3_revision/resolucion.md R-Z7-01..10)
11 sides / 220.24 LF -> 15 sides / 230.93 LF. Printed dimension first, otherwise drawn geometry at 1/4" = 18 pt/ft; nothing averaged. A421.A-2 14.39 -> 14.63 (printed 14'-7 1/2", 8/A502); A421.A-1 circle 62.2 -> 62.96 (16/A502); A421.A-3 7.5 -> 7.65 (9/A502); A422.A-1 13.33 -> 12.79 (15/A502, wall face to wall face); A423.A box south edge 9.0 -> 9.39 + west end 2.64 (16/A502); A424.A men's entry 6/A502: headwall 5.33 -> 4.75 + box front 5.33 (5'-4") + two ends 2.0 (2'-0"), box face height 1.98 ft as drawn (Review Item); A424.A-2 kept (the other edge is the EXISTING D0.43 ceiling, AD102); A424.A-3 15.94 -> 11.52 (7/A502); A425.A-1 4.83 -> 5.01; A425.A-2 5.0 -> 7.54 (diagonal exposed edge, 6/A502).
Material Summary: 6" stud +56.30 LF, ceiling / soffit track +18.38 LF, C.R. bracing +2.87 LF, 5/8" MR -21.78 SF, 5/8" Type X +75.12 SF, corner bead +5.36 LF, curved corner bead +0.76 LF, joint compound +3.84 LB, tape +19.73 LF.
- **Soffit sides (R-Z7, 3_revision/resolucion.md)**: an independent second reading of the RCP soffit sides (reader B, Z7) was compared with reading A and each difference decided on the RCP / A502 crops (printed dimension first, else drawn geometry at 18 pt/ft): now 16 sides / 235.40 LF (was 11 / 220.24 LF). Added: the 6/A502 men's entry box front and two ends (A424.A, face height 1.98 ft drawn - Review Item), the west end of the 16/A502 fountain box (A423.A) and the east edge of the 6/A502 women's entry triangle (A425.A, corrected after the back-check); lengths re-measured on A421.A (14'-7 1/2" printed, circle 62.72 to its drawn ends), A422.A, A424.A (headwalls between wall faces) and A425.A. Studs, soffit track, bracing, Type X / MR board, corner beads, compound and tape follow by the tool chain.
