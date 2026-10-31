# Reading A - O'Reilly Auto Parts, 23rd Ave., Evans, CO #1 (metal frame and drywall)

Output: `takeoff_canon_A.json` (33 walls, 54 nodes, 25 details, 14 RFIs). Builder scripts and crops are in `work/`.

## Sheets read
- **A1.1 (p37):** floor plan, wall types S21/S24/S41/S42/S43/S61, interior wall and ceiling notes 1-4, key notes 1-6. The sheet is a 400 dpi raster. I measured it at the pixel level.
- **A1.2 (p38):** interior finish plan, finish schedule and finish types (C-1 ACT, C-2 exposed, C-3 paint on gypsum).
- **A2.1 (p39):** elevations. West entry stucco block, south stucco band over D1/D2, eave elevations.
- **A3.1 (p40):** sections 1 and 3 (entry pier, vestibule head). Key notes 1-37.
- **A3.2 (p41):** sections 1 and 3 (CMU with Z-furring to the eave), 7 (plan section at the pier).
- **A3.3 (p42):** scuppers only. No framing.
- **A3.4 (p43):** section 1 (6" CFMF band over D1/D2, 7'-11 5/8").
- **A4.1 (p44):** restroom elevations, accessory schedule note 1 (FRT blocking), key 17, elevation 14 (B.O. header 106'-10").
- **A4.2 (p45):** details 2 (joint/reveal), 4 (corner box-out), 5/6/7 (S42 full height, S42 header wall, office/restroom hard lid), key notes 1-22.
- **A5.1 (p46):** door schedule. Details 7/8 (600S162-33 box header, double jamb studs).
- **A5.2 (p47):** window types A/B1/B2/C/D1/D2. Details 1, 3, 11, 12, 13.
- **A6.1 (p48):** overview only.
- **S4.1 (p33):** framing key plan. Key note 3 (16 ga entry framing), key note 4 (header wall).
- **S5.1 (p34):** details 1-5 (S42 header and full-height walls, kickers, struts, deflection track).
- **S5.2 (p35):** CMU/PEMB connections. No CFMF.
- **S5.3 (p36):** details 1 (600S162-43 band at window lintel) and 3 (600S162-54 + 800S162-54 entry framing).

Scale: A1.1 is 1/8" = 1'-0". I checked it against the grids: grid 1-2 (30'-0") = 270.72 pt, which is 9.024 pt/ft horizontal. Grid A-B (25'-0") = 226.6 pt, which is 9.06 pt/ft vertical. The overall 86'-4" = 779.1 pt. `constants.plan_scale_pt_per_ft` = 9.04 (the mean). Each `length_op` uses the scale for its own direction.

North arrow (A1.1, A1.2): north is page-left. So grid 1 is the north wall, grid A east, grid 4 south and grid C west (the storefront facade).

## Tag count on A1.1 (by hand; inventario_tags.py found 0 because the sheet is raster)

| Type | Tags | Walls | LF |
|---|---|---|---|
| S21 (Z-furring on CMU) | 10 | 6 (N, E1, E2, S, W1, W2) | 250.71 |
| S24 (CMU + Z-furring + 3-5/8" lining to 8'-6") | 5 | 3 | 35.67 |
| S41 (corner box-outs, key note 5) | 4 | 4 legs | 6.46 |
| S42 (Parts A/B/C demising, full height + header wall) | 4 | 4 (H1 full, H2 header, V1 header, V2 full) | 122.61 |
| S43 (office/restrooms, 8'-6") | 8 | 5 | 53.58 |
| S61 (6" restroom wall) | 1 | 1 | 8.50 |
| Exterior CFMF, untagged (piers 8"+6" rows, storefront head 8"+6" rows, south band 6", vestibule heads 6") | - | 10 records | 157.91 |

## Heights and where they come from
- **S21:** to the eave / top of purlin. East wall 14.625 ft (T.O. low eave 114'-7 1/2", 2/A3.2, A2.1). West wall 16.396 ft (T.O. high eave 116'-4 3/4", 1/A3.1). North and south walls 15.511 ft (average of the sloped eave). 3/A3.2 shows the furring and board running to the roof. These are DERIVED because the bottom of the purlin is not printed (RFI-01).
- **S24, S43, S61:** 8'-6" (types on A1.1; 7/A4.2 B.O. framing 108'-6"). Faces inside the rooms go to 8'-6". Outside faces go to 9'-0", because 7/A4.2 wraps the board up the edge of the 6" joist.
- **S41:** 12'-0" (S41 type note). The board on the exposed face also goes to 12'-0".
- **S42 full-height walls:** to the top of the purlin at the wall line. H1 = 15.173 ft; V2 = 16.309 ft (linear roof 1/4:12, west to east). On the Parts A side the board goes to 12'-0" (S42 type note; 5/A4.2: ceiling 11'-6" + 6"). On the Parts B/C sides the board goes to the roof framing.
- **S42 header walls:** from B.O. 106'-10" (6/A4.2; 14/A4.1) to the roof. H2 = 8.34 ft; V1 = 8.866 ft at mid-length.
- **Entry piers:** 20.667 ft (1/A3.1, floor to T.O. metal stud 120'-8").
- **Storefront head:** 9.333 ft (3/A3.1, 111'-4" to 120'-8").
- **South band:** 7.969 ft (1/A3.4, printed 7'-11 5/8").
- **Vestibule heads:** 5.021 ft (111'-4" to T.O. high eave 116'-4 1/4", 3/A3.1; RFI-14).

## Other items in the canon
- **Openings:** doors 2, 3, 7 and windows D1, D2 are in the CMU/furring, with masonry lintels (header `not_called`, RFI-13). Doors 4, 5, 6 have a 600S162-33 box header (7/A5.1, 4 pieces). Doors 1, 8 and storefronts A, B1, B2, C are listed under `none`: they are storefront under framed heads.
- **misc_items:**
  - kickers, lateral and angled struts (S5.1);
  - stud ties (3/S5.3);
  - 6" joists for office/restroom/vestibule hard lids (7/A4.2, 3/A3.1);
  - gypsum ceiling board, carried here because `ceilings[]` cannot model 6" joists;
  - glass mat exterior sheathing (keys 19).
- **blocking_items:** S42 header (2) FRT 2x nailers (6/A4.2); restroom accessories; fire extinguishers; water heater.
- **plywood_strips:** key note 5 FRT 8'-0" to 10'-0" on the S41 box faces; 3/A3.1 key 34 head soffit.
- **trim_items:** corner bead from 7/A4.2; DRMF/JDM reveals at the two S42 joints (2/A4.2).

## Pending items / RFIs (14, each with options A/B/C)
- RFI-01: bottom of purlin.
- RFI-02: S24 Z-furring height. There is no Z-furring family.
- RFI-03: the S42 header extends past the corner on A1.1 but not on S4.1.
- RFI-04: the 36'-0" south dimension is not drawn to scale on A1.1.
- RFI-05: whether there is board on top of the hard-lid joists.
- RFI-06: 1/4" gypsum and resilient channel at the entry pier/head, and the pier returns.
- RFI-07: W-4 sanitary panels in the restrooms.
- RFI-08: the MEP sweep was excluded.
- RFI-09: S5.1 bracing member lengths.
- RFI-10: blocking quantities, plus 14/A4.1 key 12 and wall-sign backing.
- RFI-11: J mold / corner bead at the header bottoms and roof edges.
- RFI-12: note 2.B flat-strap bracing.
- RFI-13: metal heads at CMU openings.
- RFI-14: vestibule heads and joists.

There is also 1 `accesorios_rfi` entry (stud reinforcement MEP).

## validar_canon
`python3 validar_canon.py takeoff_canon_A.json tools` prints **CANON ERROR** on two true data items. I did not change the data to get past them.
1. `opening_schedule.sources` has no M sheet. The gate (58.4) requires one, but the estimator excluded MEP, so nothing was swept. The `mep_sweep` key cannot have `sheets []` either (accesorios.py rejects it). I recorded the exclusion under `mep_sweep_excluded_info` and in RFI-08.
2. S21 `stud_size` "1-1/2" Z-furring (150ZF125-18)" has no family in canon.py's STUD_FAM.

I made a probe copy, `work/test_M.json`, which is not a deliverable. It changes only those two items (adds M1 to the sources and maps S21 to 1-5/8"). With those changes it prints **CANON OK**, so the rest of the canon passes canon.py and inventario.py. Both gate items are written in `lectura_notas_info`.

Time spent: about 2.5 h of agent time.
