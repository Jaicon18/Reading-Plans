# Resolution of reading A vs reading B — O'Reilly Auto Parts, Evans CO (pass 2)

Base: `takeoff_canon_AB.json` = copy of B, edited in place. Validation: `python3 validar_canon.py takeoff_canon_AB.json tools` -> **CANON OK**.
Scale A1.1 9.04 pt/ft (raster). Plan dimensions are to face of stud (A1.1 General Note B); drawn wall lines = stud faces (S61 lines 997.3 / 1001.7 pt = 6" stud).
Corner convention kept from B: the wall that owns a corner includes the abutting wall's stud + outer board (B's own S24-OF = 11'-0" + 2 x 4-1/4").

**Summary: 36 differences resolved (rows 10, 17, 22 and 31 had no real difference), 1 RFI (RFI-13). Some other items were changed only because they depend on a resolved wall. Those are listed under "Dependent items".**

## Walls

| # | Item | Value A | Value B | Decision (AB) | N/SHEET evidence | Image |
|---|---|---|---|---|---|---|
| 1 | S21-N length | 85.0 | 84.646 | **85.0** DERIVADO (25.0 + 60.0). This facade owns both corners. Faces re-split: Parts C 26.097 + Parts A 58.903 | A1.1 grid string 25'-0" + 60'-0", 86'-4" overall = 8" + 85'-0" + 8" (grids at the CMU inside face). In B, N and E each stop at the other's face, so no wall counts the corner. A's ownership counts it once, as B does for its interior walls | 00, 01 |
| 2 | S21-S length | 85.0 | 84.646 | **85.0** DERIVADO. Faces: Parts C 17.0, Parts B 58.643, R.R. 104 behind S24 9.357 (height 0) | Same as #1 | 00 |
| 3 | S21-E faces (height-0 spans behind S24) | 4 spans (45.26 / 11.74 h0 / 10.85 / 16.8 h0) | 3 spans (56.719 / 11.708 h0 / 16.219 h0) | B structure kept. Lengths: 56.115 / 11.708 h0 / 16.823 h0 (= the resolved S24 lengths) | S24/A1.1: board on the S24 studs only, no board on the furring behind them | 04, 06 |
| 4 | S21-W1 length | 9.12 (measured from the CMU face) | 9.156 | **9.156** (B) DERIVADO | A1.1 west string 4'-0" + 6'-8" to the 6'-0" CFS wall, minus 2 x 8" pilaster / CMU, minus 2-1/8" furring | 02 |
| 5 | S21-N doors 2 / 7 R.O. | 3.333 x 7.167 | 3.0 x 7.0 | **3.333 x 7.167** (A). Face deducts: Parts C 71.89 SF, Parts A 23.89 SF | A5.1 frame type 2 HM frame with 2" face: door 3'-0" x 7'-0" + 2" each side / head | 13 |
| 6 | S21-S windows D1 / D2 jamb return | true | false | **true** (A). Removed B's accesorios_none "gypsum board jamb return" | 12/A5.2: 5/8" type X board returned around the FRT blocking to the frame; 13/A5.2 sill the same | 16 |
| 7 | S24-OF / S43-OF-S length | 11.81 (11'-0" + 2 x 4-7/8") | 11.708 | **11.708** (B) DERIVADO | A1.1 11'-0" between inner stud faces (ticks at 722.7 / 821.9 pt). The side walls' outer stud face + outer board is 4-1/4" each; A also added the inner board | 04 |
| 8 | S24-RR length | 16.77 (measured) | 16.219 | **16.823** DERIVADO: 7.833 + 0.5 + 7.833 + 4.25/12 + 3.625/12 | A1.1 R.R. string 7'-10" + 6" + 7'-10" (ticks 926.8 / 997.3 / 1001.7 / 1072.4 pt). S24-RR runs under the end of S43-RR-W and owns the corner with S24-RRS. B's formula does not reach its own band end. Delta vs A +0.05, vs B +0.60. Faces 8.437 / 8.386 | 06 |
| 9 | S24-RRS length | 8.56 | 8.83 | **8.854** DERIVADO: 8'-6" + 4-1/4" | A1.1 8'-6" printed (break area, extension lines 321.7 / 398.7 pt = S24 face to S43-RR-S face) + S43-RR-S stud and outer board | 07 |
| 10 | S24 boards WR by face | WR on the R.R. faces | WR on the R.R. faces | No difference (B's two R.R. spans kept) | A1.1 note 3.B moisture-resistant type X at restrooms | 06 |
| 11 | S43-OF-W length | 7.43 | 7.88 | **8.0** CONFIRMADO | A1.1 printed 8'-0" (extension lines 321.7 / 394.2 pt = S24-OF face to S43-OF-S face, the exact span of the side wall). Both readings had measured | 05 |
| 12 | S43-OF-E length | 7.43 | 7.88 | **8.0** CONFIRMADO | Same as #11 | 05 |
| 13 | S43-RR-W length | 8.1 | 8.4 | **8.5** CONFIRMADO | A1.1 printed 8'-6" (break area string at x 873 pt, same faces as S43-RR-W) | 07 |
| 14 | S61 length | 8.1 | 8.4 | **8.5** DERIVADO (= 8'-6" between the same S24-RR / S43-RR-S faces) | A1.1 8'-6" | 07, 06 |
| 15 | S43-RR-S length | 16.17 (string only) | 16.43 (measured) | **16.521** DERIVADO: 7.833 + 0.5 + 7.833 + 4.25/12 (owns the S43-RR-W corner). Faces R.R. 103 8.438 / R.R. 104 8.083 | A1.1 R.R. string (B's own check gave 16.52) | 06 |
| 16 | S43 outside-face heights (Parts C / break side of OF-W, OF-E, OF-S, RR-W, RR-S) | 9.0 | 8.5 | **9.0** (A) DERIVADO: 8.5 + 0.5. Wall height stays 8.5. Room-side faces stay 8.5 | 7/A4.2: outside board runs past the 6" ceiling joist (8'-6" to B.O. FRAMING EL. 108'-6" + 6" printed) with corner bead key 7 | 12 |
| 17 | S43 restroom face board | WR | WR | No difference | A1.1 note 3.B | 06 |
| 18 | S41 NW box (B1V / B1H) | NW-V 1.75 / NW-H 1.67 | 2.167 / 1.313 | **B**: 2.167 CONFIRMADO + 1.313 DERIVADO. A deducted 5" instead of the S41 thickness of 4-1/4" | A1.1 2'-2" and 1'-8" printed. S41 = 3-5/8" + 5/8" one side | 10 |
| 19 | S41 SW box (B2H / B2V) | SW-H 1.67 / SW-V 1.17 (measured) | 1.667 / 1.313 | **B**: 1.667 CONFIRMADO + 1.313 DERIVADO | A1.1 prints 1'-8" in both directions at the SW box | 11 |
| 20 | S42-01 length | 40.88 (split at a measured 680 pt) | 38.667 | **38.667** (B) DERIVADO | A1.1 1'-8" + 37'-0" from the S21 face to the 2/A4.2 (ABOVE) control joint, where the hatch changes from the full-height wall to the header wall (S4.1 key note 4) | 08, 09 |
| 21 | S42-02 length | 16.33 | 18.74 | **18.74** (B) DERIVADO: 18.333 + 4.875/12 | A1.1 18'-4" from the joint to the S42-03 face; owns the corner | 09 |
| 22 | S42 face heights | 12.0 / 15.17; 5.17 / 8.34 | 12.0 / 15.172; 5.167 / 8.339 | No difference (rounding only). B kept | 6/A4.2 | — |
| 23 | EXT-MS1 / MS2 length (A: EXT-W-01 / 02) | 5.97 (measured) | 6.0 | **6.0** (B) CONFIRMADO | A1.1 west string 6'-0" + 18'-8" + 8'-0" + 12'-0" + 6'-0" | 02, 03 |
| 24 | Element of the framing over storefront A | storefront_cripples (SF-A) | wall (HEAD-A) | **storefront_cripples** (A). B's ids HEAD-A-8 / -6 kept, opening_ref "Storefront A". openings_extra Storefront A taken from A (jambs abut EXT-MS1 / MS2). opening_schedule "Window A" renamed "Storefront A" and removed from `none` | SKILL R70.7 / R75.4; tools/partition_types.py OTHER = storefront_cripples (OTHER FRAMING, not EXT-CFMF). 38'-8" R.O. A5.2 | 02, 14 |
| 25 | Board over the storefront A head | 0.67 face (SF-A-8) | none (RFI-06) | **0.667 face**, Parts A side, board_base 11.333 (A) | 1/A5.2 head: 5/8" type X + 1/4" on resilient channel drawn 8" above the head. RFI-06 is kept only for board above that point | 14 |
| 26 | EXT-MS1 / MS2 board height, Parts A side | 12.0 | 11.5 | **12.0** (A) DERIVADO: 11.333 + 0.667 | 1/A5.2: board 8" above the 11'-4" head = 12'-0" (6" over the C-1 ACT 11'-6", A1.2) | 14 |
| 27 | EXT-MS2 Parts B face | single face 12.0 | split 3.08 @ 11.5 + 2.92 @ 16.396 | B split kept (S42-04 meets MS2, Parts B C-2 is exposed). Parts A span changed to 12.0 | A1.1 (S42-04 at 824-827.6 pt), A1.2 C-2 | 03 |
| 28 | VH-B1 / VH-B2 length | 4.98 (measured) | 5.667 | **5.667** (B) CONFIRMADO | A5.2 window types B1 / B2 5'-8" (HOLD) | 18 |
| 29 | VH-B1 / B2 / C gauge | 16 ga | 18 ga (600S162-43) | **18 ga kept (B), RFI-13**: delta 20.08 LF wall line, studs 43 -> 54 mil | 3/A3.1 key note 8 "600S162-43 ... AT 24" O.C." vs S4.1 key note 3 "PROVIDE 16ga LIGHT GAUGE STEEL FRAMING AT ENTRY LOCATION". The printed notes conflict | 17, 18, 19 |
| 30 | VH faces | 0.67 board, parts side | none | **0.667 face** (A) | 3/A5.2: 5/8" TYPE "X" GYPSUM BOARD on the parts side of the 6" framing, from the head to above the ACT | 15 |
| 31 | CORN-S / EXT-S-BAND | 36.0, 7.969, 18 ga | 36.0, 7.969, 18 ga minimum | No difference. B kept | 1/S5.3 key 22, 1/A3.4, A1.1 36'-0" | — |
| 32 | Gauge text (cosmetic) | "20 ga (33 mil, 362S162-33)" | "20 ga (33 mil)" | Unified: 20 ga (33 mil, 362S162-33); S61 20 ga (33 mil, 600S162-33); 16 ga (54 mil, 800S162-54 / 600S162-54); 18 ga (43 mil, 600S162-43) | Schedules / 3/S5.3 / 3/A3.1 | — |

## Misc / blocking / trim

| # | Item | Value A | Value B | Decision (AB) | N/SHEET evidence | Image |
|---|---|---|---|---|---|---|
| 33 | Angled strut brace S42 (ANG-STRUT) | missing | 64.0 LF | **B kept** | 5/S5.1 "angled strut brace at each end of wall and @ 16'-0" O.C. (MAX)", 8'-0" max | 20 |
| 34 | 2"x2"x14ga clips at kickers | 20 | 14 | **14** (B) | 2/S5.1 (purlin beyond = S42-03 only, the same section that carries CONT. 6" studs in both readings). 1/S5.1 has no clip | 21 |
| 35 | FCB43.5 clips CORN-S | missing | 30 | **B kept** | 1/S5.3 key 23 drawn 3 rows @ 48" | 22, 23 |
| 36 | Window D blocking | 58.92 incl. sill | 36.19 (sill to RFI-09) | **58.92** (A). RFI-09 removed | 13/A5.2 sill: FIRE TREATED 2X4 WOOD BLOCKING ANCHORED TO MASONRY | 16 |
| 37 | Corner bead S41 boxes | 24.0 | 30.46 (+ top edges) | **24.0** (A) | Top edges at 12'-0" are above the C-1 ACT 11'-6" (A1.2), so they are concealed | 10, 11 |
| 38 | Corner bead S42 header bottom | 160.65 (+ free ends below) | 138.15 | **165.48** = B lengths + A's free ends (2 x 2 x 6.833) | 6/A4.2 B.O. FRAMING EL. 106'-10"; ends of S42-01 / S42-04 at the 2/A4.2 joints | 09 |
| 39 | Reglets / JDM at S42 joints | 43.31 | 69.9 | **43.31** (A method: only where board exists on both sides above 106'-10") | 2/A4.2 key note 9 | 09 |
| 40 | Corner bead 7/A4.2 | 77.92 (+ 3 vertical corners x 9.0) | 52.3 (top only) | **79.73** (resolved lengths + 3 x 9.0) | 7/A4.2 key note 7; 3 outside corners of the office / R.R. block (A1.1) | 12 |
| 41 | Ceiling joists, vestibule | 5 x 5.667 | 5 x 5.375 | **B kept** (26.88) | 3/A3.1 printed 5'-4 1/2" | 18 |

Dependent items (changed only to follow a resolved length or height): CJ-OFFICE-102 56.0 (7 x 8.0); CT-RR 34.0; ceiling GWB office 86.03 SF and R.R. 103 / 104 64.89 SF each (printed 11'-0" x 8'-0" and 7'-10" x 8'-6", net of board); QTR-GYP-EXT-MS 182.63 SF; RC-EXT-MS 131.43 LF; BLK-EXT-DOORS 57.33 LF (#5). A1.1 bands moved to the resolved ends for S24-RR, S24-RRS, S43-OF-W/E, S43-RR-W, S61-RR and S43-RR-S. RFI-04 delta was updated. RFI-06 was reworded: 8" is carried, and the open question is board above that point.

Nodes: the topology is the same, with ids from B (A's L corners at the office are B's T nodes with free S24 ends). Ceilings: both readings have none (C-3 hard lids are in misc_items), so no difference. Details: B's set is kept (enough for CANON OK). A lists extra detail references but no differing values.

## Alerts "TYPE NO INVENTARIADO"

These are not A/B differences. The inventory script could not read the raster Interior Wall Types schedule on A1.1, so it inventoried 0 tags. The schedule visibly lists S21, S24, S41, S42, S43 and S61 (image 00 / A1.1 bottom). EXT-CFMF is the exterior wall type naming (partition_types.py), not a schedule tag.

## RFI raised

- **RFI-13** vestibule head gauge: 18 ga is carried (B, 3/A3.1 key 8) against 16 ga (A, S4.1 key 3). Delta: 20.08 LF wall line x 4.95 ft studs @ 24", from 43 mil to 54 mil.
