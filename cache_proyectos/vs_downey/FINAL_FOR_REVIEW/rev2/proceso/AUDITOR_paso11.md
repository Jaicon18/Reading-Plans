# AUDIT - VS #679 Stonewood Center - blind re-quantification (metal framing + gypsum board)

Tags: [CONFIRMADO] read on sheet / [DERIVADO] operation shown / [PENDIENTE] not resolved.

## Method / calibration
- [DERIVADO] A02.01 plan 1/4in=1-0 => 18 pt/ft (72pt/in x 0.25); checked against printed 4-0 dim on A03.01 (71.4pt measured = 17.9 pt/ft) and 8-9 restroom dims on A02.01
- Vector hatch classification on A02.01 (page 13, rotation 270 applied): standard = single-direction 45deg hatch; RFID = cross-hatch; insulated = dense triangle hatch; storefront = sparse dotted hatch. Walls = paired parallel 1.44pt face lines 4.5-11.5pt apart. Segments break at intersections/openings (LF is net of openings).
- Full per-segment list (171 segments W001-W171, faces, heights, sources) is in AUDIT.json `walls`.

## Totals by partition type (A02.01 Partition Schedule M)
| Type | Segments | LF | Board SF |
|---|---|---|---|
| INSULATED | 13 | 43.2 | 424.0 |
| RFID | 4 | 55.9 | 998.0 |
| STANDARD | 148 | 582.2 | 9191.0 |
| STOREFRONT | 6 | 19.1 | 0 |

**Total wall board SF: 10613** [DERIVADO] length x face height, no opening deduction; storefront faces excluded (finish per A08)

Heights: standard/RFID T.O. stud +/-12-0 AFF [CONFIRMADO A/A12.01, C/A12.01]; insulated & storefront tight to structure, deck 17-0 / lowest structure 12-1 [CONFIRMADO A01.01]. Board faces: to ceiling per A03.01, +6in above ACT (C/A12.01), none toward voids (A/A12.01). RFID non-sales face foil-backed 5/8.

## Openings
| Host | Door | Size | Source |
|---|---|---|---|
| W036-W046 FR front wall (H948.6) | 5QG x6 (FR1-5 + AFR6) | 3-0 x 5-7 1/2 x 1 3/4 leaf, partial height door (5QG) | [CONFIRMADO] 6/A00.02; R.O. [PENDIENTE] A10.08 D1/D2 |
| W033/W034 Go-back (H891.6) | 5UG pair | PR 2-1 5/16 x 7-4 3/8 | [CONFIRMADO] 1/A00.02; R.O. [PENDIENTE] A10.08 G1/G2 |
| W119-W122 CW closet #1/#2 (V730) | 6L x2 backwrap blind | 2-4 3/4 x 8-4 1/4 | [CONFIRMADO] 2/A00.02; R.O. [PENDIENTE] A10.08 K1/K2 |
| W159/W160 display window #1 wall (V2485) | 6L x1 window display blind | 2-4 3/4 x 8-4 1/4 | [CONFIRMADO] 1/A00.02; detail J1/J2 A10.08 |
| W015/W017 RFID wall (V693) | 7B sales/non-sales HM | 3-0 x 7-0 | [CONFIRMADO] A00.02; vector gap 67pt=3.7ft [DERIVADO] |
| W087/W088 restroom walls (H1776.9) | 8A x2 toilet HM | 3-0 x 7-0 | [CONFIRMADO] 2/A00.02 |
| W085 MGR office (H1681.8) | 11 office HM | 3-0 x 7-0 | [CONFIRMADO] A00.02 |
| west insulated/existing wall (gap y1678-1773) | 12 service HM 90 MIN | 3-0 x 7-0 | [CONFIRMADO] A00.02 - in (E)/exterior wall |
| storefront entry | 1A rolling grille | 18-1 +/- x 11-3 (to B.O. coil) | [CONFIRMADO] A00.02 |
| W052/W053 FR alcove wall gap x1380-1446 | cased opening Trans #4 (no door) | 66pt = 3.7 ft | [DERIVADO] |
| W113/W114 break room east wall gap y1429-1495 | cased opening (no door in schedule) | 66pt = 3.7 ft | [DERIVADO] |

## Gypsum ceilings (A03.01; board per A15.04 092900 = 5/8 Type X)
| Room | SF | Height ft |
|---|---|---|
| MGR office | 71.6 | 8.0 |
| Corridor E of break/office | 106.9 | 8.0 |
| Gender neutral restrooms (2) | 120.8 | 8.0 |
| Backwrap/cashwrap soffit (B.O. 8-5) | 21.4 | 8.42 |
| Fitting rooms FR1-5 (5 x 23.3) + AFR6 58.8 | 175.1 | 9.0 |
| FR alcove | 166.5 | 9.0 |
| FR lounge (net of go-back) | 124.6 | 9.0 |
| Go-back closet | 10.0 | 9.0 |
| Hallway | 88.3 | 9.0 |
| CW closets #1/#2 | 11.0 | 9.17 |
| Room #4 Beauty 3 + Trans #5 | 1054.4 | 10.5 |
| Room #3 VSL 3 + Trans #4 | 1174.1 | 11.0 |
| Room #2 VSL 2 + Trans #3 (net pilasters) | 1418.7 | 11.0 |
| Room #1 VSL 1 + Trans #2 (net pilasters) | 1426.6 | 11.0 |
| VS Display Windows #1/#2 (2 x 47.9) | 95.8 | 11.17 |

**Total gypsum ceiling: 6065.8 SF, all 5/8 Type X** [DERIVADO]. By height: {'8.0': 299.3, '8.42': 21.4, '9.0': 564.5, '9.17': 11.0, '10.5': 1054.4, '11.0': 4019.4, '11.17': 95.8}

Non-gyp: Stock/Electrical ACT-2 12-0; Receiving ACT-2 10-4; Break room ACT-7 10-0; Trans #1 storefront entry SF-91 stucco 10-6 (not gyp; substrate per A08)

## Stud spacing
- S01.01 Table 1: 362S162-33 20ga @16 max 17-6; -43 @16 19-0; -54 20-6; 600S162-33/43/54 25-6/28-6/30-0 [CONFIRMADO S01.01]
- Table 2 VSBeauty/Pink cabinet walls: 3-5/8 20ga @16 max, diagonal bracing at ~11-6 AFF [CONFIRMADO]
- Table 3 stock shelving walls -> S03.02 A1 (362S162-33 @16, 13-0), A2 (-33 @12 / -43 @16, 13-0 to double track), A3 (-33 @8 14-0, -43 @12 14-0, -54 @12 16-0, -54 @16 13-0, 600S162-43 @16 18-0) [CONFIRMADO S03.02]
- At shelving on each side of a single stud wall: halve stud spacing and halve diagonal spacing of A/S03.01 [CONFIRMADO S01.01]

Reduced spacing walls:
- W133,W134 (V1148, Trans #5 / Beauty 2 spine): cabinets/shelving both faces (A03.01/A06.01 fixtures both sides); Table 2 3-5/8in 20ga @16 -> 8in o.c.; diagonals A/S03.01 48in -> 24in [DERIVADO] S01.01 N note
- W146,W147 (V1593, Trans #3 spine): fixtures both faces; 16 -> 8in o.c. [DERIVADO] S01.01 N note
- W152,W153 (V2037.8, Trans #2 / Beauty 1 spine): fixtures both faces; Table 2 16 -> 8in o.c. [DERIVADO] S01.01 N note
- W014-W016 RFID wall at stock/CW closets: stock racks 2442F/F7 10ft H on west face (Table 3 -> S03.02 A1/A2/A3) + keynote 33 wall-mounted shelving A-1 on CW closet face: shelving both sides -> halve Table 3 spacing (e.g. A3 362S162-33 @8 -> 4in, or upsize per S03.02) [DERIVADO] A02.01 + S01.01 + S03.02
- W075-W077 (H1554, break room / MGR office): A-2 shelving/keynote 33 shown on both faces; 16 -> 8in o.c. [DERIVADO] A02.01 [PENDIENTE] verify A14.01
- W018 (stock north furring), W010/W071 (receiving, F6 racks + A-8 keynote 28 shelving): Table 3 stock racks 10ft H one side only -> S03.02 table (A1 16in @13-0 max partial height / A2 12-16in / A3 8-16in); not halved [DERIVADO]

## Special framing
- **storefront_S02_01**:
  - (3) Beam DBL 10in DP 16ga + 3-5/8 20ga track T&B + 14ga web stiffeners at bearing: entry grille line ~18.1 LF [DERIVADO vector A/S02.01 1/2in scale 36pt/ft; matches 18-1 grille A00.02]
  - (4) Beam DBL 10in DP 16ga + 3-5/8 16ga track T&B: north line at entry ~18.1 LF [DERIVADO]
  - (2) Beam DBL 8in DP 18ga + 3-5/8 20ga track: display window glazing lines 2 x ~13.3 LF [DERIVADO]
  - (1) Beam DBL 6in DP 20ga + 3-5/8 20ga track: 2 x ~3.9 LF [DERIVADO]
  - (6) built-up box posts DBL 3-5/8 20ga: 6 ea [CONFIRMADO count tags A/S02.01]; (16) box posts per H/S03.01: 6 ea [CONFIRMADO count]
  - Storefront walls 3-5/8in 20ga structural (1-5/8 flange) @16in o.c.; diag braces 3-5/8 20ga; 2x2x0-6 16ga clips w/(3)#8; 3-5/8 20ga cont track [CONFIRMADO sections P/K/F/B S02.01]
  - Storefront wall LF (hatch type N storefront on A02.01) 19.1 LF [DERIVADO]
- **display_window_platforms**: [PENDIENTE] A08.05 not quantified in this pass; A05.01 keynote 12 confirms tiled platforms (top and face) exist at display windows #1/#2 (2 x ~3.55 x 13.5 ft footprint DERIVADO)
- **column_wraps**: R/A10.01: (1) 5/8 Type X on 1-5/8 metal studs tight, 14in max; 4 sales-floor columns on A02.01 (19x19pt symbols) [DERIVADO count], ~4.2 LF perimeter each, to ceiling 10-6/11-0 -> ~180 SF board, 16 corner beads [DERIVADO]
- **cashwrap_soffit**: F/A10.05: backwrap soffit 5/8 gyp on 3-5/8 metal stud, suspended stud to structure + diag bracing; B.O. soffit 9-2 and 8-5 AFF, 4 7/8in fascia; length 17-7 1/8 plywood to plywood [CONFIRMADO A/A10.05] + closet returns
- **beauty_valances**: B/A10.03: valance 5/8 gyp on 1-5/8 mtl framing @16; B.O. soffit 8-4 AFF; gyp to gyp 1-11 1/4; NO board on interior side of valance; suspended metal stud + diagonal brace; 14-1 HOLD gyp to gyp per A/A10.03 [CONFIRMADO]; count of beauty cabinet runs [PENDIENTE A06.01]
- **deflection_track**: L/S03.01 18ga vertical slotted slip track, 3/4in defl gap: at walls to structure = insulated (43.2 LF) + storefront (19.1 LF) = 62.3 LF [DERIVADO]; standard/RFID walls stop at +/-12-0 braced (A/A12.01), no slip track
- **bracing**: A/S03.01: diagonal 3-5/8 20ga @48in o.c. max interior partitions (storefront 48in); halve to 24in at walls in reduced-spacing list; Table 2 bracing at ~11-6 AFF [CONFIRMADO S01.01/S03.01]. Approx braces = 638 LF std+RFID / 4 ft = ~160 diagonals [DERIVADO]
- **bridging**: R/S03.01: 1-1/2 x 1/2 16ga CRC through studs @4-0 o.c. vertically (S03.02 shows standard bridging 5-0 at stock walls): ~2 rows x 638 LF = ~1,276 LF std/RFID + ~4 rows x 43 LF insulated = ~173 LF [DERIVADO]
- **metal_blocking**:
  - A10.03 B/G: 6in continuous metal blocking behind gyp at 3 heights (C.L. 7-9, 4-5, 0-11 AFF) at beauty cabinet walls [CONFIRMADO]
  - A02.01 keynote 33 / A14.01 A: in-wall blocking for wall shelving (A-1, A-2, A-8) [CONFIRMADO note; LF PENDIENTE]
  - A02.01 keynote 41: mirror locations in-wall blocking [CONFIRMADO note]
  - A02.01 keynote 10: 1-1/2x1-1/2x48 SS corner guards (blocking) - ~16 tags [DERIVADO]
  - A07.xx / A13.xx blocking lengths [PENDIENTE - not opened in this pass]
- **corner_bead**: A15.04 092900 O.3: corner bead at all external corners; estimated ~70 vertical corners (spine wall T-caps 16, pilasters 18, column wraps 16, cased openings 8, misc 12) x ~10.5 ft = ~735 LF [DERIVADO]
- **frp**: WC-1 Kemlite FRP (A00.03) wainscot in Electrical, Break Room, Hallway, Restrooms (A05.01 room tags); keynote 8: only at exposed walls, not behind shelving/lockers/panels, see E/A13.02; gross perimeters ~177 LF less doors ~15 LF = ~162 LF [DERIVADO]; height and trim (cap/inside/outside corner) [PENDIENTE E/A13.02]
- **cement_board**: Restrooms: B-13 porcelain cove base + FC-156 floor; wall tile extent [PENDIENTE A13.01]; cement board behind any wall tile per 092900 O.1.b (cementitious backer units)

## Findings (easy to miss)
1. Lowest point of structure is 12-1 AFF (A01.01) while Stock has ACT-2 at 12-0 (A03.01) and A05.01 keynote 10 says paint walls to 12-0: board 6in above ACT (C/A12.01) and studs +/-12-0+ cannot fit under the 12-1 structure - verify field heights / clips.
2. A01.01 note: existing angled braces both sides of column - GC to verify an 11-0 gyp bd ceiling is achievable; sales rooms are 11-0 gyp ceilings.
3. Almost the whole sales floor ceiling is GYPSUM BOARD (P-230 paint), ~6,066 SF of 5/8 Type X on drywall grid - ACT is only in Stock, Receiving, Break.
4. RFID shielded partition (cross-hatch) runs the full BOH/sales line (~56 LF): non-sales face is FOIL-BACKED 5/8 board, plus detail A/S03.01 and R/A12.01 RFID antennas.
5. S01.01 note: shelving on both sides of a single stud wall halves stud spacing AND diagonal brace spacing - applies to trans/beauty spine walls and RFID wall at stock/CW closets.
6. Table 3 (stock racks) is NOT a stud table on S01.01 - it points to S03.02 tables A1/A2/A3 (8in/12in/16in spacing, 362S162-33 to 600S162-43) depending on height and bracing.
7. Insulated wall type: 18ga min 3-5/8 studs tight to structure (deck 17-0) with batt + vapor barrier; keynote 7 adds R-13 insulation in furring along exterior wall.
8. North and south demising walls are NEW standard partitions (furring) along the full 122 ft length - board one face only (A/A12.01 no board in void), 9 pilaster boxes each side ends.
9. Pilaster boxes at N and S demising walls (9 total) and gondola T-caps add many external corners (corner bead) and short framing pieces.
10. Storefront S02.01 built-up beams DBL 10in 16ga with 14ga web stiffeners and 12 box posts (coded notes 6 and 16) - structural cold-formed, not standard partition.
11. Backwrap soffit (F/A10.05) and beauty valances (B/A10.03) are suspended stud framing with diagonal braces to structure; valance interior side gets NO board.
12. Partition schedule: restroom walls adjacent to sales and fitting-room walls adjacent to non-sales get 3-1/2 batt (STC 42) - FR rooms back up to non-sales stock at W019/AFR6 and RFID wall.
13. Display window ceilings 11-2 gyp and a 10-2 gyp soffit at the window wall (A03.01) plus 6L blind door into display window #1.
14. FRP (WC-1) wainscot in non-sales rooms only at exposed walls (A05.01 kn 8) with keynote 43 (merch flow board above FRP) and kn 20 chalkboard paint above FRP.
15. Fitting room doors 5QG are partial height (5-7 1/2) - FR walls 9-0 ceiling, studs to +/-12-0; 6 doors + go-back pair 5UG.
16. A15.04 092900 B.1: L/360 deflection limit at walls receiving tile vs L/240 typical (restrooms / FR tile) - may change stud gauge.
17. Column wraps R/A10.01 (VS) vs L/A10.01 (PINK): 14in max, notify VS&Co if columns larger; 4 columns in sales floor.

## Not covered / PENDIENTE
A07.01-A07.04, A08.05/.10/.15, A10.07, A10.08 R.O. details, A13.01-02, A14.01-02 not opened in this pass; per-wall printed dimensions not cross-checked one by one (vector lengths used).
