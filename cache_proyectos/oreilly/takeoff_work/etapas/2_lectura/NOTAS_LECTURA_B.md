# Reading B notes: O'Reilly Auto Parts, 23rd Ave., Evans, CO #1

Output: `takeoff_canon_B.json`. Running `validar_canon.py takeoff_canon_B.json tools` prints **CANON OK**.
The canon was built with `build_canon_B.py`, so every number can be traced to its operation. This reading used `plano.pdf` only.

## Sheets read
- A1.1 (p37): floor plan, wall types S21/S24/S41/S42/S43/S61, key notes, interior notes.
- A1.2 (p38): finish schedule and ceilings C-1/C-2/C-3.
- A2.1 (p39): exterior elevations.
- A3.1 (p40): sections 1/2/3 (pier, head wall, vestibule).
- A3.2 (p41): sections 1-4 (CMU and Z-furring).
- A3.3 (p42): scuppers. Nothing for this trade.
- A3.4 (p43): 1/A3.4 (south windows, exterior studs) and 6/A3.4.
- A4.1 (p44): accessory schedule and blocking note.
- A4.2 (p45): details 2, 4, 5, 6, 7.
- A5.1 (p46): door schedule and 7/8 head/jamb.
- A5.2 (p47): window types A/B1/B2/C/D, 3/A5.2, 10/A5.2.
- S4.1 (p33): key plan and key notes 3 and 4.
- S5.1 (p34): sections 1-5.
- S5.3 (p36): sections 1 and 3 with keynotes.
- A6.1 (p48) and S5.2 (p35): looked at the overview only. Nothing was loaded from them.

## Scale
- A1.1 raster at 400 dpi. Along x: 9.022 pt/ft. Grid 1-4 measures 85'-0" = 766.85 pt, and all 9 ticks of the grid C dimension string match.
- Along y: 9.058 pt/ft. Grid A-C measures 85'-0" = 770.0 pt.
- The raster is 0.4 % anisotropic, so each length uses the scale of its own axis. `plan_scale_pt_per_ft` is set to 9.04, the mean of the two.
- Sections were checked against printed elevations: A3.1 at 54.33 pt/ft and A3.2 at 54.28 pt/ft.

## Tags counted by hand
The sheet is raster, so this is a visual sweep of A1.1.

| Type | Tags | Walls | LF |
|---|---|---|---|
| S21 | 10 | 6 | 250.06 |
| S24 | 4 | 4 | 34.47 |
| S41 | 4 | 4 | 6.22 |
| S42 | 4 | 4 | 115.91 |
| S43 | 6 | 6 | 51.16 |
| S61 | 1 | 1 | 8.64 |

Wall breakdown:
- **S21:** 10 tags give 6 walls, 250.06 LF: N 84.38, E1 45.28, E2 10.85, S 75.54, W1 9.08, W2 24.93. They are in `walls[]` with stud_size `1-1/2" Z-furring (150ZF125-18)`, a family added by the tools update R80e.65.
- **S24:** 34.47 LF: office N 10.85, R.R. 103 N 7.68, R.R. 104 N 7.73, R.R. 104 S 8.21. Height 8'-6" (CONFIRMADO).
- **S41:** 6.22 LF, made of 2 corner box-outs with 2 legs each (key note 5, 4/A4.2). Height 12'-0" (CONFIRMADO).
- **S42:** 115.91 LF:
  - B1 is full height, 38.67 LF, 14.34 ft.
  - B2 is a header wall, 18.74 LF, studs 7.51 ft.
  - V1 is a header wall, 50.33 LF (printed 50'-4"), studs 8.04 ft.
  - V2 is full height, 8.17 LF (printed 8'-2"), 15.48 ft.
  - The header walls start at 6'-10" (6/A4.2).
- **S43:** 51.16 LF. **S61:** 8.64 LF. Both have studs to 8'-6" and 600S162-54 ceiling joists (7/A4.2).

Exterior metal stud:
- **Front storefront piers:** 2 piers x 6'-0", each a 6" row plus an 8" row (16 ga @ 16", 3/S5.3). Height 20.67 ft, from the floor to T.O. metal stud 120'-8" (1/A3.1).
- **Head wall over storefront A (`storefront_cripples`):** 38.67 LF per row, 9.33 ft high. It sits on the PEMB wind beam, so there is no stud header.
- **EXT-S-6:** a 6" 18 ga panel over windows D1/D2 on the south facade. 36.0 LF is measured on 4/A2.1 (DERIVADO). Height 7'-11 5/8" is printed (1/A3.4).
- **Vestibule head walls (VH-C, VH-B1, VH-B2):** 20.83 LF, from the printed 10/A5.2 dimensions. Height 4.12 ft, measured on 3/A3.1.

## Heights and where they come from
- **S43, S61, S24:** 8'-6" from the A1.1 types and 7/A4.2. Faces on the outside of the enclosure go to 9'-0" (T.O. framing 109'-0", 13/A4.1).
- **S41:** 12'-0" (type).
- **S42:**
  - On the Parts Area A side, faces go to 12'-0" (type and 5/A4.2).
  - On the B and C sides, faces go to the bottom of the roof framing.
  - That elevation is derived as B.O. = 116.396 − d/48 − 0.83:
    - d is the distance in ft from grid C.
    - The high eave is 116'-4 3/4" and the low eave is 114'-7 1/2", which gives the 1/4:12 slope.
    - The 0.83 ft purlin depth is measured on 3/A3.1.
  - This is RFI-01.
- **S21:** measured on the wall sections:
  - Front (1/A3.2): 14.77 ft.
  - Rear (2/A3.2): stud 13.24 ft, board 12.39 ft.
  - North and south walls: the average of the two ends.
  - This is RFI-02.

## Pending items and RFIs
There are 9 RFIs, all in A/B/C format:
- 01: roof framing elevation.
- 02: S21 height.
- 03: Z-furring member and height (a family now exists).
- 04: length of the south stucco panel.
- 05: vestibule gauge, 16 ga (S4.1) vs 18 ga (3/A3.1).
- 06: kicker length.
- 07: blocking for toilet accessories.
- 08: a short double line east of the grid 3 column on grid B. It is not loaded.
- 09: number of FRT nailer plies.

Data that is true but that the tools reject:
- **Joist ceilings:** office, R.R. 103/104 and vestibule are loaded as `framed_soffit`. The real joists are 6" (600S162-54 and -43), but the tool loads 3-5/8".
- **Pier interior:** the 1/4" gypsum and the resilient channel (1/A3.1) have no family.

Version 2 (after the tools update R80e.64 / R80e.65):
- The 6 S21 walls (250.06 LF) moved into `walls[]`.
- **MEP:** `mep_sweep` is now `excluded_by_estimator`. `opening_schedule.sources_none.M` gives the reason. "stud reinforcement MEP" is closed with an `accesorios_none` entry. No P or M sheet is listed anywhere.
- The CMU openings in S21 (Doors 2, 3, 7; Windows D1, D2) needed `substrate` and `jamb_return` before the canon would validate. I read them from the details:
  - Substrate: FRT 2x4 blocking (1/A5.1, 11/A5.2).
  - Doors: no gypsum board return (1-6/A5.1).
  - Windows D1, D2: 5/8" Type X return at head and jambs (11/A5.2, 12/A5.2).

Not loaded:
- C-1 acoustical ceiling (other scope).
- 1x4 wood trim (finish carpentry).
- Sanitary wall panel W-4 (finishes).
- CMU lintels and nailers at the top of the masonry (masonry and roofing).

Time: about 3 h.
