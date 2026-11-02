# Resolution A vs B: CFA #2284 River Point (stage 3)

The base is reading A (the more complete reading). Each line reads: item, A value / B value, decision, evidence (N/SHEET), and crop image (all crops are in `img/`).
Output: `takeoff_canon.json` (validated: CANON OK). Applied rules: R-ALC-07, R-ALC-10, R-ALC-11 and BE-116 (addendum dated 2026-11-02).

## (1) MB-01, the infill at the removed Eliason door
- MB-01 is 3.33 LF of 3-5/8" metal: A 3.33 LF / B not loaded. **Decision: A is kept.** On A-202 the segment from 617 to 677 pt at x 1541–1551.5 is drawn with the heavy black new-wall outline (1.56 pt). The existing wall around it is drawn grey at 0.72 pt. A-050 KN1 says "existing Eliason door to be removed" at the same opening (60 pt = 3'-4"). No type is printed for the infill, so the conservative metal value (C2/S-801 362S162-33 @ 16") stays loaded. Open RFI-17, Review Item 1. Crops: `img/r01_MB01_A202.png`, `img/r01_MB01_A050.png`, `img/r01_A202_wall_legend.png`.
- B's short untagged new-wall segment at A-202 x≈1541–1551.5, y 617–677 is the same element as MB-01. It is loaded once, as MB-01.

## (2) Soffit sides and (8) corner bead
- Soffit sides: A 73.44 LF / B 61.27 LF. **Decision: A.** A-221 draws the PT-31A C.H. 9'-8" serving soffit as an L: a west strip from y 440 to 766 plus a north strip from y 440 to 482 that runs to the wall at x 1405. The south edge dies on the hatched wall. B modelled only the 1225–1276 rectangle and added a south edge that does not exist. The A-221 bubble at this soffit is C4/A-624 (3-5/8" @ 16"). Crop: `img/r02_soffit_A221.png`.
- Ceiling 1/2" regular (soffit bottoms): A 100.04 SF / B 76.77 SF. **Decision: A** (68.04 + 32.0), because it follows from the soffit geometry above.
- Corner bead: A 73.44 LF / B 61.27 LF. **Decision: A.** C4/A-624 says "corner beads at all gypsum board intersections". The bead runs along the free bottom edges of the soffit geometry above.

## (3) 6" LGS ceiling joists and rim
- 6" joists: A 304.5 LF / B 278.7 LF. **Decision: A.**
  - Men's: A 75.98 vs B 79.38. S-241 prints 11'-3" x 7'-11 1/4" with a step. Only about 4 joists run the full 7.94 ft; the other 6 are 7.36 ft. A's figure matches that count; B ran every joist at full length.
  - Women's: 85.63 vs 85.70. A is kept (the difference is negligible).
  - Play bay: 29.28 LF, A only. Kept under R-ALC-11. A-052 KN10 removes the existing ceiling and support, and A-221 draws a new gyp ceiling there, but S-241 does not show the bay. The A2/S-241 LGS schedule is loaded as the conservative value. Open RFI-07, Review Item 2.
  - Crops: `img/r03_S241_C3_overview.png`, `img/r03_S241_A2_A3_schedule.png`.
- 6" rim track: A 143.2 LF / B 0. **Decision: A.** The rim is printed: the S-241 legend says "dropped ceiling and RIM JOISTS", and A3/S-241 shows "2X RIM JOIST (TO MATCH C.J.)". Under the standing order metal-or-wood → metal, the rim is 6" track. The wood/LGS conflict is closed as RFI-08 (option A). Crop: `img/r03_S241_A2_A3_schedule.png`.
- New, BE-116 / R-ALC-11: bridging, 50.87 LF of "bracing C.R. channel". A2/S-241 prints "BRIDGING LOCATION: MID SPAN" for spans of 0–15 ft, and C09111 §3.2.C (A-909) requires sway bracing. One row is loaded per dropped ceiling (7.04 + 7.04 + 11.25 + 13.58 + 11.96). The bridging member is not printed, so RFI-09 stays open. No hangers or carrying channel were loaded: the ceilings are joist-framed wall to wall, and C09111 §3.2.B covers hung systems only.

## (4) Roof hatch shaft and strongback
- Roof hatch shaft: A 48 LF stud + 24 LF track / B 0. **Decision: A is kept, because it is printed.** A-221 KN8 calls for a "NEW LADDER AND ROOF HATCH RE: A1/A-604". A1/A-604 prints "2X4 WOOD OR 3 5/8" METAL FRAMED WALL ... ALL SIDES OF OPENING", "24" BELOW FINISH CEILING" and a 3'-0" hatch. The shaft height and the second hatch dimension are not printed. Open RFI-14, Review Item 3. Crop: `img/r04_A1_A604_roofhatch.png`.
- Strongback: A 26.51 LF / B 0. **Decision: A is kept, because it is printed.** C3/S-801 prints a "362T125-54 STRONGBACK ... to each truss @ 48" O.C." and "soffit assembly ... attach to provided strongback". C3/S-801 is bubbled on S-241 at the serving soffit. Crop: `img/r04_C3_S801_strongback.png`.

## (5) 5/8" gyp ceilings
- 5/8" gyp ceilings: A 331.69 SF / B 297.02 SF. **Decision: 332.06 SF.**
  - Men's uses B's 85.73 SF. It comes from the printed 11'-3" x 7'-11 1/4" less the notch; A's 85.48 SF came from a vector polygon.
  - Women's uses B's 97.01 SF, built on the printed 5'-9".
  - Entry A (46.36 SF) and Entry B (67.92 SF) are the same in both readings.
  - Play bay: 35.04 SF, A only, kept. A-221 PT-41 draws a gyp ceiling at C.H. 14'-6", and A-052 KN10 removes the existing gyp ceiling and support there.

## (6) Demolition (R-ALC-07)
- Totals: A 2,169.1 SF / B 2,299.5 SF → **2,646.6 SF**.
- Bottom of structure: A-401 D4 prints only "EXISTING ROOF STRUCTURE" with no elevation. A-052 notes and A-402 print no height either. S-201 prints existing member elevations, so the bottoms below are DERIVED from them:
  - **Kitchen truss bay = 12'-4".** This comes from "7"x24" PSL BEAM (TOP OF BM. EL. 14'-4 1/2")" minus 24" TJS = 12'-4 1/2", and from "5 1/4"x18" PSL BM (TOP OF BM.=+13'-8")" minus 16" (24"/16" TJS tapered open-web trusses) = 12'-4". Crop: `img/r06_S201_kitchen_east.png`, `img/r06_A401_section.png`.
  - **North-east TJI zone = 12'-2".** This comes from "16" TJI/L65 @ 32"" with "(+13'-6") TOP OF JOIST" minus 16".
  - **Office / walk-in / east-wall zone:** no usable bottom is printed (2x8 joists with no elevation, a mezzanine at 10'-8", 2x10 roof joists at +17'-3 1/2"). 12'-4" is loaded and marked PENDING. Open RFI-10, Review Item 4.
- Per wall:

| Item | Reading A | Reading B | Decision | Evidence |
|---|---|---|---|---|
| DEMO-01 (KN3) | 16.733 LF (red segments) | 16.9 LF (counted the 3 pt jog) | A's length at 12.333 ft x 2 layers = 412.74 SF | A-050 |
| DEMO-02 / DEMO-03 | — | — | 12.167 ft (NE zone) = 314.59 / 57.72 SF | S-201 |
| DEMO-04 (office west) | 9.683 LF | 9.183 LF | B: 9.183 LF. A's extra 0.5 ft is a 0.48 pt end-cap line beyond the red double-line wall body (998.3–1163.6). 226.51 SF, PENDING | A-050 vectors |
| DEMO-05 / DEMO-06 | — | — | 12.333 ft = 252.97 / 91.41 SF | S-201 |
| DEMO-07 (drive-thru north wall) | 11.661 LF | 11.011 LF | B: the red double-line wall runs 1391.9–1590.1. A started at a 0.48 pt edge line at 1380.2. 271.60 SF | A-050 vectors |
| DEMO-08..10 (KN24 openings) | 2 layers | 1 layer | B: 1 layer. The wall is the building's existing east exterior wall: A-050 KN29 "remove existing exterior finishes, prepare wall for new addition" is on the same line, so the outer face is not gyp. 22.61 + 55.50 + 55.50 SF, PENDING height | `img/r06_A050_east.png` |
| DEMO-13, new (office / walk-in partition at A-050 x 2110.8, 963.7–1163.6) | missing | 11.106 LF | B: the partition is drawn red dashed, i.e. demolished. 273.94 SF, PENDING height | `img/r06_A050_x2110_raw.png`, `img/r06_A050_overview.png` |
| DEMO-11 (half walls), DEMO-12 (menu furr-down) | — | — | Same in both readings: 154.0 / 55.56 SF (RFI-11, RFI-12 open) | — |
| Gyp ceiling demo DEMO-C1..C5 (A-052 KN10, type printed "gyp bd ceiling") | areas from the new S-241 ceilings | areas measured on the A-052 demolition RCP | B, because the demo is measured on the existing-ceiling sheet: Men's 89.95, Women's 111.49, Entry A 47.89, Entry B 69.98, play bay 44.27 SF | A-052 |
| DEMO-C6 (east room) | 38.35 SF | 35.39 SF | Both are A-052 vectors and they disagree. The conservative A value is kept (Review Item 5) | A-052 |

## (7) Level 5
- Level 5: A 731.2 SF / B 826.9 SF. **Decision: A.** A-211 shows the play area's west bay as a storefront (glazing), which cannot take Level 5 or wallcovering. A traced the solid-wall polygon, 59.69 LF x (12.75 – 0.5). B used a full rectangle, 2 x (268 + 339.6) pt, which takes in the glazing bay. Crop: `img/r07_A211_play_WC1.png` (WC-1 circled).

## (9) Board-only entries
- Totals: cement board A 1,387.7 / B 1,306.1 → **1,502.4 SF**; 1/2" gyp A 1,264.5 / B 1,209.3 → **1,393.9 SF**.

| Item | Reading A | Reading B | Decision and evidence |
|---|---|---|---|
| PT0010 W4, serving face | 1.0 ft (G.3) | 10.0 ft (tile) | B. A-622 D3/D4 serving elevations show CT-45 wall tile full height to C.H. 10'-0". The A-622 general note requires "cementitious board substrate for the full height of tile". G.2 applies. Crop: `img/r09_A622_serving_tile.png`. Same decision for W6-01S-SRV (PT0014 serving face, 7.9 LF) and PT0015 W6-02N-SRV: 10.0 ft |
| PT0011 / PT0012 W4.1 boxes | outer-face paths 5.37 / 3.71 LF | inner lines 4.59 / 3.37 LF | A. The exposed (kitchen) face is the outside of the chase box, so A's outer-face paths are right. 1.5 ft |
| PT0013 W6, multi-purpose face | 1.5 ft (KN16) | 1.0 ft | B. A-050 KN16 says 18" "typical in kitchen" only; G.3 1'-0" governs the other back-of-house rooms. The same 1.0 ft is applied to A's W6-08E-SVC, W6-09-OUT (PT0018), W6-10N-SVC (PT0022), SW6-02-SVC, EX-MP-01 and EX-MP-02 |
| PT0017 W6 | 2.37 LF straight, 2 faces | L 3.83 LF | B. The heavy new-wall outline includes the 1'-10" return. Crop: `img/r09_PT0017_A202.png` |
| PT0018 W6 office L | split faces 14.68 x 1.0 + 15.82 x 1.5 | centreline 15.31 x 2 faces | A's inner/outer face paths are kept, with the outer face at 1.0 ft (G.3) |
| PT0019 W6 mop chase | 2.37 x 10.167 cement board | 2.42 x 1.5 x 2 faces | A. A-201 KN25 calls for new stainless panels at the existing mop sink, and G.7 puts cement board behind stainless. A's height to the ceiling is unverified, so this is Review Item 6 |
| PT0022 W6, service face | 12.41 x 1.5 | 12.48 x 1.0 | A's length with B's 1.0 ft height (G.3) |
| PT0023 W6 | 11.06 LF | 4.2 LF | **B.** A-202 prints 4'-2 1/2"; east of 1407 there is no wall, only dashes. B's dining face (5" cement board + gyp to 9'-11") is kept. The drive-thru face (1343–1407) is 3.556 LF x 1.5 ft. A's W6-11N/W6-11S entries (11 LF) are deleted. Crop: `img/r09_PT0023_PT0026_A202.png` |
| PT0024 W6 kitchen / walk-in line | split into piers between the 4'-6" walk-in door openings | continuous run | B. Board never deducts openings; the run is printed 16'-9 1/2". Loaded: kitchen face 16.79 x 1.5, walk-in face 16.33 x 1.0 cement board + 9.667 gyp (G.11). A's six pier entries are deleted |
| PT0026 W8, drive-thru face | 7.65 x 1.0 | 8.15 x 1.5 | A's length (from the inner face of the north wall) with B's 1.5 ft. A-211 shows kitchen finishes (KT-6B / FRP-2) in the drive-thru, so KN16 applies |

## (10) M3.5 stud size
- M3.5 stud size: A 3-5/8" / B 3-5/8" with RFI. **Decision: 8".** The A2/A-605 "PIN & SLEEVE SECTION" is bubbled on A-201 exactly at the two M3.5 walls, at hoods #2 and #3. It prints "8" METAL STUD WALL" and "8" METAL STUD FRAMED BASE". The printed detail at the location wins.
  - Result: 117.3 LF of studs moves from the 3-5/8" family to the 8" family.
  - RFI-01 is closed under R-ALC-10 (option A, with the 3-5/8" delta noted). Review Item 7.
  - The recess framing is loaded per R-ALC-11: 42.67 LF of 8" studs + 8.0 LF of sill track (RFI-13 open).
  - Crops: `img/r10_A2_A605.png`, `img/r10_A201_A2callouts.png`.

## (11) Merged RFIs
- Reading A had 10 RFIs and reading B had 12. The merged list has **17**: 5 closed (estimator decision, option A under R-ALC-10) and 12 open (information printed nowhere; conservative value loaded under R-ALC-11).
- Deleted: B RFI-11, the kitchen plywood removal "as required". It is Div. 06 and now appears as an EXCLUDED note.
- Merged:
  - A RFI-07 + B RFI-06 → RFI-10 / RFI-11 / RFI-12.
  - A RFI-05 + B RFI-04 + B RFI-12 → RFI-05.
  - A RFI-03 → RFI-13.
  - B RFI-09 (gauge part): answered by spec C09111 §2.3.B.1 (0.0312 in min), so it is no longer an RFI; the spacing part remains as RFI-02.
- Added: RFI-16 (wood vs metal legend conflict, closed with delta "computed by program") and RFI-17 (MB-01).
