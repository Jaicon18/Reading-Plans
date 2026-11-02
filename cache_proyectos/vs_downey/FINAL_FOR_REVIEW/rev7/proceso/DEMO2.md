# DEMO pass 2 - gypsum board and metal framing demolition, VS #679 Downey (A01.01, page 12)

Scale 1/4"=1'-0" = 18 pt/ft on A01.01 and A02.01 (same grid, same orientation; the north demising wall lines y 834.7/845.6 pt and every heavy existing wall coincide on both pages). Calibrated: lease line x 316.5-2559.2 pt = 2242.7 pt vs 124'-7 1/8" printed on A02.01. Lengths are vector geometry (DERIVADO). Geometry for markups: `demo_geom.json` (60 polylines, A01.01 page coordinates). Canon: 35 demo misc_items (were 26), `CANON OK`.

## Task A - heights

No sheet prints an existing partition, furring or enclosure height. Checked: A01.01 general notes M (GN 1: space cleared to "exposed underside of structure", "stripped columns"), keynotes D (K2 removes every existing ceiling/soffit; K19/K20 structure heights noted on plan), plan callouts and the LOWEST POINT OF DECK 17'-0" / STRUCTURE 12'-1" box; A02.01 partition schedule (E) row and keynotes (K26 (E) tenant separation wall to remain); A03.01 / A04.01 notes (new ceilings only, no existing ceiling shown); A07 / A08 elevations and sections (new work; A08.05 prints B.O. (E) MALL SOFFIT 13'-8 1/2", B.O. joist ±15'-11", B.O. deck ±17'-0" at the storefront); A12.01 / A10 details (new work, B/A12.01 1-hour tenant wall is VOID); S01.01-S05.01 (existing roof = wood joists on steel beams, no partitions).

Rule used: each element runs full height to the printed bottom of structure over it.

- DERIVADO: the bay has a joist callout (K20 @16'-8" north bay, @16'-3" bay 3-2 between B and A), or the wall runs directly under a printed beam (P03 south cross wall under grid-B beam @14'-11"; west restroom furring under the west beam @12'-1"). Column enclosures go to the lowest printed beam framing into the column. B2/A2 go to B.O. (E) mall soffit 13'-8 1/2" (A08.05 sections N/J/E/A + A08.01; keynote 6 "to bottom of (E) mall bulkhead").
- PENDIENTE: the bay has no joist callout. These are carried at the highest printed member bounding the bay (conservative): 5-4 between B and A, and 5-4 south of A, at 14'-11 1/2"; 4-3 south of A at 16'-4"; 4-3 between B and A at 15'-0"; west of grid 5 south of A at 12'-1" (the only printed member there). Also PENDIENTE: the A5 enclosure (its grid-A beam segment has no callout) and B5 (no outline).
- Demising wall board: kept at the estimator decision of 12'-0", matching the replace item. The printed evidence shows the rated U465 wall runs to deck 17'-0" (A01.01, A08.05), but the schedule replaces board only "if required". Flagged.

## Final demo table

| id | element | keynote | L (ft) | H (ft) | H source | H status | layers | SF |
|---|---|---|---|---|---|---|---|---|
| P01 | back-of-house: wall between the stockroom and the three small rooms | keynote 4 | 19.41 | 16.667 | bottom of existing joists K20 @16'-8" A.F.F. printed in the north bay (west of grid 4), A01.01 | DERIVADO | 2 | 647.01 |
| P02 | back-of-house: east wall of the three small rooms | keynote 4 | 13.67 | 16.667 | bottom of existing joists K20 @16'-8" A.F.F. printed in the north bay (west of grid 4), A01.01 | DERIVADO | 2 | 455.68 |
| P03-N | back-of-house: cross walls of the three small rooms (north bay) | keynote 4 | 13.5 | 16.667 | bottom of existing joists K20 @16'-8" A.F.F. printed in the north bay (west of grid 4), A01.01 | DERIVADO | 2 | 450.01 |
| P03-BB54 | back-of-house: cross walls of the three small rooms (under the grid-B beam) | keynote 4 | 4.5 | 14.917 | wall runs directly under the grid-B beam K19 @14'-11" A.F.F. (grids 5-4), A01.01 | DERIVADO | 2 | 134.25 |
| P04 | back-of-house: south wall of the north room, east part | keynote 4 | 4.34 | 16.667 | bottom of existing joists K20 @16'-8" A.F.F. printed in the north bay (west of grid 4), A01.01 | DERIVADO | 2 | 144.67 |
| P05-N | back-of-house / sales floor dividing wall, north wall to south wall (openings excluded) (north bay) | keynote 4 | 12.81 | 16.667 | bottom of existing joists K20 @16'-8" A.F.F. printed in the north bay (west of grid 4), A01.01 | DERIVADO | 2 | 427.01 |
| P05-M54 | back-of-house / sales floor dividing wall, north wall to south wall (openings excluded) (between grids B and A, grids 5-4) | keynote 4 | 19.48 | 14.958 | no joist callout in the bay grid B-A / grids 5-4; carried at the highest printed member bounding the bay: grid-A beam K19 @14'-11 1/2" (grid-B beam @14'-11", grid-A beam near grid 4 @14'-7 1/2"), A01.01 | PENDIENTE | 2 | 582.76 |
| P05-S54 | back-of-house / sales floor dividing wall, north wall to south wall (openings excluded) (south of grid A, grids 5-4) | keynote 4 | 15.98 | 14.958 | no joist callout in the bay south of grid A / grids 5-4; carried at the highest printed member bounding the bay: grid-A beam K19 @14'-11 1/2" (@14'-7 1/2" near grid 4), A01.01 | PENDIENTE | 2 | 478.06 |
| P06 | back-of-house: short wall east of the three small rooms | keynote 4 | 3.32 | 14.958 | no joist callout in the bay grid B-A / grids 5-4; carried at the highest printed member bounding the bay: grid-A beam K19 @14'-11 1/2" (grid-B beam @14'-11", grid-A beam near grid 4 @14'-7 1/2"), A01.01 | PENDIENTE | 2 | 99.32 |
| P07 | back-of-house: room walls south of grid B | keynote 4 | 12.21 | 14.958 | no joist callout in the bay grid B-A / grids 5-4; carried at the highest printed member bounding the bay: grid-A beam K19 @14'-11 1/2" (grid-B beam @14'-11", grid-A beam near grid 4 @14'-7 1/2"), A01.01 | PENDIENTE | 2 | 365.27 |
| P08 | back-of-house: corridor wall | keynote 4 | 16.43 | 14.958 | no joist callout in the bay south of grid A / grids 5-4; carried at the highest printed member bounding the bay: grid-A beam K19 @14'-11 1/2" (@14'-7 1/2" near grid 4), A01.01 | PENDIENTE | 2 | 491.52 |
| P09 | back-of-house: wall north of the restrooms | keynote 4 | 14.26 | 14.958 | no joist callout in the bay south of grid A / grids 5-4; carried at the highest printed member bounding the bay: grid-A beam K19 @14'-11 1/2" (@14'-7 1/2" near grid 4), A01.01 | PENDIENTE | 2 | 426.60 |
| P10 | back-of-house: wall east of the restrooms | keynote 4 | 10.06 | 14.958 | no joist callout in the bay south of grid A / grids 5-4; carried at the highest printed member bounding the bay: grid-A beam K19 @14'-11 1/2" (@14'-7 1/2" near grid 4), A01.01 | PENDIENTE | 2 | 300.95 |
| P11 | restrooms: dividing wall | keynote 4 | 7.22 | 14.958 | no joist callout in the bay south of grid A / grids 5-4; carried at the highest printed member bounding the bay: grid-A beam K19 @14'-11 1/2" (@14'-7 1/2" near grid 4), A01.01 | PENDIENTE | 2 | 215.99 |
| P12 | restrooms: north wall | keynote 4 | 5.36 | 12.083 | no joist callout in the bay south of grid A / west of grid 5; only printed member bounding it is the west beam K19 @12'-1" (= LOWEST POINT OF STRUCTURE 12'-1"), A01.01 | PENDIENTE | 2 | 129.53 |
| P13-SW5 | back-of-house: angled wall south-west of column A5 (south of grid A, west of grid 5) | keynote 4 | 7.3 | 12.083 | no joist callout in the bay south of grid A / west of grid 5; only printed member bounding it is the west beam K19 @12'-1" (= LOWEST POINT OF STRUCTURE 12'-1"), A01.01 | PENDIENTE | 2 | 176.41 |
| P13-S54 | back-of-house: angled wall south-west of column A5 (south of grid A, grids 5-4) | keynote 4 | 1.5 | 14.958 | no joist callout in the bay south of grid A / grids 5-4; carried at the highest printed member bounding the bay: grid-A beam K19 @14'-11 1/2" (@14'-7 1/2" near grid 4), A01.01 | PENDIENTE | 2 | 44.87 |
| P14-S54 | fitting-room block south of grid A, grids 4-3 (4 rooms + corridor wall) (south of grid A, grids 5-4) | keynote 4 | 29.52 | 14.958 | no joist callout in the bay south of grid A / grids 5-4; carried at the highest printed member bounding the bay: grid-A beam K19 @14'-11 1/2" (@14'-7 1/2" near grid 4), A01.01 | PENDIENTE | 2 | 883.12 |
| P14-S43 | fitting-room block south of grid A, grids 4-3 (4 rooms + corridor wall) (south of grid A, grids 4-3) | keynote 4 | 31.17 | 16.333 | no joist callout in the bay south of grid A / grids 4-3; carried at the highest printed member bounding the bay: grid-4 beam K19 @16'-4" (same rule as the new-work take-off), A01.01 | PENDIENTE | 2 | 1,018.20 |
| P15-M43 | sales floor: mid-floor display wall between grids 3 and 2 (fixtures both faces) (between grids B and A, grids 4-3) | keynote 4 | 2.3 | 15.0 | no joist callout in the bay grid B-A / grids 4-3; carried at the printed grid-B beam K19 @15'-0", A01.01 | PENDIENTE | 2 | 69.00 |
| P15-M32 | sales floor: mid-floor display wall between grids 3 and 2 (fixtures both faces) (between grids B and A, grids 3-2) | keynote 4 | 31.05 | 16.25 | bottom of existing joists K20 @16'-3" A.F.F. printed in the bay grid B-A / grids 3-2, A01.01 | DERIVADO | 2 | 1,009.12 |
| FS-SW5 | south demising wall, from the west wall to the fitting rooms (back-of-house, restrooms, fitting rooms) (south of grid A, west of grid 5) | keynote 7 | 7.06 | 12.083 | no joist callout in the bay south of grid A / west of grid 5; only printed member bounding it is the west beam K19 @12'-1" (= LOWEST POINT OF STRUCTURE 12'-1"), A01.01 | PENDIENTE | 1 | 85.31 |
| FS-S54 | south demising wall, from the west wall to the fitting rooms (back-of-house, restrooms, fitting rooms) (south of grid A, grids 5-4) | keynote 7 | 32.33 | 14.958 | no joist callout in the bay south of grid A / grids 5-4; carried at the highest printed member bounding the bay: grid-A beam K19 @14'-11 1/2" (@14'-7 1/2" near grid 4), A01.01 | PENDIENTE | 1 | 483.59 |
| FS-S43 | south demising wall, from the west wall to the fitting rooms (back-of-house, restrooms, fitting rooms) (south of grid A, grids 4-3) | keynote 7 | 11.94 | 16.333 | no joist callout in the bay south of grid A / grids 4-3; carried at the highest printed member bounding the bay: grid-4 beam K19 @16'-4" (same rule as the new-work take-off), A01.01 | PENDIENTE | 1 | 195.02 |
| FW | west wall at the restrooms | keynote 7 | 7.22 | 12.083 | runs directly under the west beam K19 @12'-1" A.F.F. (= LOWEST POINT OF STRUCTURE 12'-1"), A01.01 | DERIVADO | 1 | 87.24 |
| FN | north demising wall at the stockroom | keynote 7 | 15.78 | 16.667 | bottom of existing joists K20 @16'-8" A.F.F. printed in the north bay (west of grid 4), A01.01 | DERIVADO | 1 | 263.01 |
| CB4 | column B4 enclosure | keynote 3 | 4.76 | 14.917 | lowest printed beam framing into column B4: grid-B beam K19 @14'-11" (grids 5-4; 4-3 @15'-0", grid-4 beam @16'-4"), A01.01; general note 1 'stripped columns' = enclosure removed up to the structure | DERIVADO | 1 | 71.00 |
| CA4 | column A4 enclosure | keynote 3 | 4.78 | 14.625 | lowest printed beam framing into column A4: grid-A beam K19 @14'-7 1/2" (callout next to grid 4), A01.01; general note 1 'stripped columns' | DERIVADO | 1 | 69.91 |
| CB3 | column B3 enclosure | keynote 3 | 4.8 | 15.0 | lowest printed beam framing into column B3: grid-B beam K19 @15'-0" (grids 4-3; 3-2 @15'-3 1/2"), A01.01; general note 1 'stripped columns' | DERIVADO | 1 | 72.00 |
| CA3 | column A3 enclosure | keynote 3 | 4.83 | 15.292 | lowest printed beam framing into column A3: grid-A beam K19 @15'-3 1/2" (grids 3-2; no callout on grids 4-3), A01.01; general note 1 'stripped columns' | DERIVADO | 1 | 73.86 |
| CB2 | column B2 enclosure (column to the storefront line, under the mall bulkhead) | keynote 3 | 8.17 | 13.708 | enclosure lies under the existing mall bulkhead (A02.01 keynote 2 bulkhead lines x 2470.3-2574.7 pt): 13'-8 1/2" A.F.F. B.O. MALL SOFFIT printed on A08.05 sections N, J, E, A and A08.01; A01.01 keynote 6 'REMOVE ALL TENANT STOREFRONT MATERIALS TO BOTTOM OF (E) MALL BULKHEAD' | DERIVADO | 1 | 111.99 |
| CA2 | column A2 enclosure (column to the storefront line, under the mall bulkhead) | keynote 3 | 8.19 | 13.708 | enclosure lies under the existing mall bulkhead (A02.01 keynote 2 bulkhead lines x 2470.3-2574.7 pt): 13'-8 1/2" A.F.F. B.O. MALL SOFFIT printed on A08.05 sections N, J, E, A and A08.01; A01.01 keynote 6 'REMOVE ALL TENANT STOREFRONT MATERIALS TO BOTTOM OF (E) MALL BULKHEAD' | DERIVADO | 1 | 112.27 |
| CA5 | column A5 enclosure (chase from the west wall around the roof drain leader and the column) | keynote 3 | 17.61 | 14.958 | enclosure runs along the grid-A beam between the west wall and grid 5; that beam segment has no height callout on A01.01; carried at the nearest printed grid-A beam callout K19 @14'-11 1/2" (grids 5-4) - the west beam it abuts is @12'-1", the grid-B beam on the same bay line is @12'-8" | PENDIENTE | 1 | 263.41 |
| CB5 | column B5 enclosure (outline not drawn - typical size, confirm in field) | keynote 3 | 4.79 | 12.667 | lowest printed beam framing into column B5: grid-B beam K19 @12'-8" (west of grid 5; @14'-11"± east of it), A01.01 | PENDIENTE (size and H) | 1 | 60.67 |
| DB | existing demising wall board removal for the replace (north + south) | A02.01 (E) row + keynote 7 | 249.19 | 12.0 | estimator decision kept with the replace item (deck 17'-0" printed, A01.01 / A08.05) | estimator decision | 1 | 2,990.25 |
| **TOTAL** | | | | | | | | **13,488.88** |

L status: DERIVADO everywhere, except B5 perimeter (PENDIENTE: typical size) and the demising board (north CONFIRMADO A02.01 124'-7 1/8", south DERIVADO). By H status: DERIVADO 4,129.03 SF; PENDIENTE 6,369.60 SF (B5 included); estimator decision 2,990.25 SF.

## Task B - cross-check A01.01 (demo) vs A02.01 (new), vector overlay

| # | A01.01 | A02.01 | result |
|---|---|---|---|
| R1 | North demising wall, solid heavy pair y 834.7/845.6 pt, x 324-2520 (keynote 7) | same lines; keynote 26 (E) tenant separation wall to remain | REMAIN; board replace 'if required' (demising_board) |
| R2 | South demising wall, solid heavy y 1918.3-1929.1 pt (keynote 7) | same; keynote 26 | REMAIN; furring against it removed (FS) and rebuilt |
| R3 | West wall and pilasters, solid heavy (V 319.95, 360.15, 360.85, 367.85, 420.35; H 953.6, 1191.45, 1211.15, 1260.55) | identical lines | REMAIN |
| R4 | Mall neutral piers at the storefront corners (keynote 11) | same | REMAIN (patch/repair, no quantity) |
| X1 | Solid existing interior partitions | - | none on A01.01 (GN 1: all partitions removed) |
| X2 | 15 dashed partitions P01-P15 (keynote 4) | no wall on the same centerline over its length (checked within 10 pt, all 1.44 pt new-wall pairs + heavy existing pairs) | DEMOLISHED, none reused |
| X3 | Column enclosures B4, A4, B3, A3 (keynote 3) | new column wraps CW1-CW4 (R/A10.01) at the same columns | DEMOLISHED, then new wrap (new-work take-off) |
| X4 | Column enclosures B2, A2, dashed, from column to storefront line (keynote 3) | new pier boxes SP1/SP2 x 2481.4-2559.2 pt at the same place, larger | DEMOLISHED, then rebuilt; H corrected to 13'-8 1/2" |
| X5 | Furring: south demising wall (FS), west restroom wall (FW), north stockroom (FN) | new furring along the south wall (y 1915), new insulated wall I07 (x 364.6-371), new furring W001 along the north wall (y 846-852.5) | DEMOLISHED, then rebuilt |
| N1 | - | new walls: 118 canon walls (STD, RFID, FUR, INS, column wraps, pier boxes, storefront) | NEW only (A02.01). None sits on an existing partition to remain |

## Differences found (N/SHEET + crop in xcheck/, each as _A0101.png and _A0201.png)

| # | item | N/SHEET | finding / change | crop |
|---|---|---|---|---|
| D01 | A5 enclosure | A/A01.01 keynote 3 (2 leaders, one to the dashed band) | rev5: 'no outline drawn, typical size 4.79 ft'. The keynote 3 leader lands on a dashed band x 371.6-521.8 / y 1552.1-1568.7 pt that runs from the west wall around the roof drain leader (keynote 21) and column A5. Re-measured as 3 sides = 317.0 pt = 17.61 ft (west side against the wall). H stays PENDIENTE at 14'-11 1/2". +191.76 SF (71.65 -> 263.41) | xcheck/D01_A5_enclosure_band_A0101.png |
| D02 | North furring at the stockroom | A/A01.01 keynote 7 'where occurs' + A02.01 W001 FUR | rev5 left it out. A dashed line at y 854.6, 9.0 pt off the wall face (845.6), x 364.3-648.4, drawn like the south furring. A02.01 builds new furring in the same place. Added FN: 15.78 ft x 16.667 x 1 = 263.01 SF | xcheck/D02_north_furring_stockroom_A0101.png |
| D03 | Display-window back walls | A/A01.01 keynote 4 (door pairs) | Dashed pair x 2488.1/2491.0 is 2.9 pt (~2") thick, so it is not metal stud / gyp bd. A02.01 builds new hatched back walls at x~2484 in the same place. Not carried, flagged | xcheck/D03_display_window_back_walls_A0101.png |
| D04 | B2 / A2 pier enclosures | A/A01.01 keynote 3; A02.01 SP1/SP2; A08.05 | New pier boxes are rebuilt at the same location. These boxes sit under the mall bulkhead, so H changes from 15'-3 1/2" (beam) to 13'-8 1/2" (B.O. (E) mall soffit) -> -25.92 SF | xcheck/D04_B2_A2_pier_boxes_A0101.png |
| D05 | P03 cross walls | A/A01.01 keynote 4; A02.01 | New walls at y 1038.5 (x 696.8-744.5) and y 1192.8 (x 696.8-726.3) sit 2.7 and 7.4 pt off the demo lines y 1041.2 and 1200.2, over part of their length. These are a new hatched type with new extents, so the demo stands | xcheck/D05_P03_new_wall_same_line_A0101.png |
| D06 | P08 corridor wall | A/A01.01 keynote 4; A02.01 | New wall at y 1607 (x 696.8-726.3, 1.6 ft) is 1.9 pt off the demo line. The demo stands | xcheck/D06_P08_new_wall_same_line_A0101.png |
| D07 | P12 restroom north wall | A/A01.01 keynote 4; A02.01 | The new restroom north wall at y 1777 (x 434-489.5) is 4.3 pt off. It is new construction, so the demo stands | xcheck/D07_P12_restroom_north_wall_A0101.png |
| D08 | P14 fitting-room walls | A/A01.01 keynote 4; A02.01 | New walls at x 1098.2 and 1184.7 (y 1880-1912, about 1.5 ft each) sit near the demo walls x 1095.7 and 1175.5. The demo stands | xcheck/D08_P14_room_wall_A0101.png |
| D09 | South and west furring | A/A01.01 keynote 7; A02.01 keynote 7 + INSULATED WALL | Existing furring is replaced by new furring (y 1915) and the new insulated wall I07 at the same line. Consistent with removing it | xcheck/D09_furring_rebuilt_S_and_W_A0101.png |
| D10 | Column wraps B4/A4/B3/A3 | A/A01.01 keynote 3; A02.01 column notes / R/A10.01 | Existing enclosures are removed and new wraps are built. Consistent | xcheck/D10_column_wraps_B4_A4_B3_A3_A0101.png |
| D11 | B5 | A/A01.01 keynote 3 | There is a leader but no enclosure outline (only the 0.96 pt column symbol). A02.01 has no wrap here. Kept at typical size, PENDIENTE | xcheck/D11_B5_no_outline_A0101.png |
| D12 | Storefront boxes N / center / S | A/A01.01 keynote 6 | Dashed boxes x 2486.6-2552.8 at y 952.9-968.0, 1292.8-1303.1 and 1794.2-1809.2 have no keynote 3 and no stated material. Not carried, flagged | xcheck/D12_storefront_boxes_not_carried_A0101.png |
| D13 | P15 mid-floor display wall | A/A01.01 keynote 4 TYP | Nothing is built in this place on A02.01. The demo stands; H changes from 12'-0" to 16'-3" in bay 3-2 (joists K20) | xcheck/D13_P15_display_wall_A0101.png |

Also in xcheck/: demo_geom_A0101_all.png, demo_geom_A0101_BOH.png (geometry over A01.01), demo_geom_on_A0201_BOH.png (same geometry over A02.01).

## What changed vs rev5 (SF)

| group | rev5 SF | pass 2 SF | delta | why |
|---|---|---|---|---|
| partitions (keynote 4) | 6,609.12 | 8,549.35 | +1,940.23 | H 12'-0" -> printed structure per bay (12'-1" to 16'-8"); L unchanged 275.38 -> 275.39 (rounding, split by bay) |
| column enclosures (keynote 3) | 669.27 | 835.11 | +165.84 | A5 re-measured from the drawn band (+191.76); B2/A2 to the mall soffit 13'-8 1/2" (-25.92); B4/A4/B3/A3/B5 unchanged (now DERIVADO except B5) |
| furring (keynote 7) | 702.60 | 1,114.17 | +411.57 | north stockroom furring added (+263.01); south furring H by bay (+147.96); west furring 12'-0" -> 12'-1" (+0.60) |
| demising board removal | 2,990.25 | 2,990.25 | 0.00 | kept with the replace item (estimator decision), flagged |
| **TOTAL** | **10,971.24** | **13,488.88** | **+2,517.64** | |

## Still PENDIENTE / not carried

- Partition and furring heights in bays without a joist callout (6,045.52 SF carried at the highest printed member bounding the bay). Field verify whether existing partitions stopped at an existing ceiling.
- B5 enclosure size (no outline). A5 enclosure height (no callout on that grid-A beam segment).
- Demising board height: estimator decision 12'-0" vs rated wall to deck 17'-0". Extent of the replace is a field condition.
- Keynote 2 ceilings and soffits: gyp bd vs ACT not shown. The mid-floor soffit outline at grids 4-3 is not carried.
- Storefront zone: display-window back walls (2") and three storefront boxes, material not stated. Not carried.
- Framing removed is information only (studs @16" o.c. + track); SF is the carried unit.
