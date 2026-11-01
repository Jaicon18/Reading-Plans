# LECTURA A - VS #679 Stonewood (Downey CA) - notes

Canon: `takeoff_canon_A.json` (validar_canon.py prints CANON OK; inventario OK, 129 elements, 122 with a plan band).
Fragments and scripts: `2_lectura/A/` (runs_p13.json, walls_raw.json, walls_main.json, walls_all.json, frag3.json, rfis.json, img/) and `scripts/`.

## Sheets read
A00.02 (door schedule), A00.03 (finish schedule: P-230 = paint, ACT-2/ACT-7, WC-1 FRP), A02.01 (plan, partition schedule, keynotes), A03.01 (RCP heights and keynotes), A05.01 (finish plan: WC-1 wainscot rooms), A08.01 / A08.05 (storefront; 13'-8 1/2" B.O. mall soffit; ±17'-0" B.O. metal deck; ±15'-11" B.O. joist), A10.01 (R column wrap), A10.02 (B/K Garcy blocking), A10.05 (F/A backwrap soffit), A12.01 (A non-rated, C furred, R RFID), A12.02 (N gyp ceiling, E/A transitions), A13.01 (restroom: 4'-0" FRP, 8'-0" ceiling, blocking keynotes), S01.01 (notes, TABLE 1), S02.01 (storefront framing), S03.01 (A bracing, L deflection track, N water-heater shelf), S05.01 (RTU support framing), M02.01 / P02.01 (crossing sweep, registered dx=dy=0, 61 matches).
Not read in detail (time): A07.xx elevations, A08.10/A08.15, A10.03/A10.07/A10.08, A14.xx, A15.01-06 specs text, the remaining M/P/E sheets.

## Walls by hatch type (A02.01 partition schedule; text is outlined -> types by hatch, lengths from the vector hatch extents at 18 pt/ft)
| type | hatch | count | LF |
|---|---|---|---|
| N-STD (N) standard partition, A/A12.01 + C/A12.01, 3 5/8" 20 GA @16 (6" at the restroom plumbing wall W070) | single diagonal | 109 | 611.54 |
| N-RFID shielded partition (foil-backed non-sales side) | cross-hatch | 4 | 56.29 |
| N-INS (N) insulated wall, 18 GA, C/A12.01, inside face only | triangles | 7 | 44.56 |
| N-SF storefront wall (S02.01) | storefront pattern | 2 | 9.27 |
| Total element "wall" | | 122 | 721.66 |
| column_wrap COL (R/A10.01, 1 5/8") | box | 4 | 16.87 (perimeter) |
| column_wrap N-SF pier boxes at entry (S02.01) | box | 2 | 25.29 (perimeter) |
| soffit_side cashwrap backwrap drop (F/A10.05) | - | 1 | 15.14 |
(E) demising walls: no new framing (rule 8). The struck-through 1-hour fire partition is not used (B/A12.01 VOID).

## Heights chain
- Partition studs: T.O. STUD ±12'-0" A.F.F. (A/A12.01, C/A12.01), braced to structure @48" (A/S03.01); STOCK walls 12.5 ft (12'-0" ACT + 6", RFI-02).
- Board per face: ceiling of the room it faces (A03.01) + 6" (C/A12.01 / schedule); ELECTRICAL has no ceiling -> T.O. stud.
- Insulated walls: "tight to structure" -> B.O. JOIST ±15'-11" (N/A08.05) with 18 GA deep-leg slip track L/S03.01 (RFI-01 vs C/A12.01).
- Storefront: 13'-8 1/2" B.O. (E) mall soffit (A/A08.01, N/A08.05).
- Ceilings (P-230 = 5/8" gyp on drywall grid, N/A12.02): 8'-0" MGR / corridor / restrooms, 9'-0" FR rooms, alcove, lounge, go-back, hallway, 9'-2" CW closets, 10'-6" Room 4, 11'-0" Rooms 1-3, 10'-2" display windows; cashwrap framed soffit 9'-2" / 8'-5" (F/A10.05). ACT rooms (STOCK, RECEIVING, BREAK) are excluded (not our trade). 23 ceiling entries, 6,207 SF.

## RTU support framing (S05.01) - WOOD
- 18 new 2x joists "to match extg" (2x10 assumed, field verify), counted as 6 heavy lines per RTU on A/S05.01. Bays 19'-8 3/8" (RTU-1, RTU-2) and 19'-10 11/16" (RTU-3) -> 355.73 LF.
- Double 2x blocking at the curbs (coded note 1, C/S05.01, Simpson LUS28 at each end): length not printed, 48 LF PENDING (RFI-10).
- Hold-down straps (J1/J2) are hardware; fasteners are excluded.
These items are carried as blocking_items with material "wood" (Div. 06), so the estimator can decide.
Also carried: the water-heater shelf N/S03.01 (6" 20 GA joists, 6" 16 GA edge track, 3/4" FRT plywood, clips), using the MAX sizes (RFI-11).

## RFIs (18)
01 insulated wall height / deflection track; 02 STOCK ceiling vs T.O. stud; 03 storefront top and grille box; 04 1/2" MR board under storefront finish; 05 RFID foil-backed board; 06 suspended soffit stud height; 07 FR alcove ceiling untagged; 08 door R.O. not printed; 09 blocking lengths; 10 RTU wood blocking; 11 water-heater shelf size; 12 diagonal brace length; 13 carrying-direction placeholder; 14 (E) demising repair allowance; 15 outside-corner bead not enumerated; 16 duct crossings; 17 lengths derived from vector (outlined text); 18 roof structure conflict (wood joists vs metal deck).

## Continuation (coverage gaps closed + new estimator wood rule)
Sheets added: A07.01, A07.02, A07.04 (elevations), A08.10, A08.15 (storefront details), A10.03, A10.07, A10.08 (construction and door details), A14.01, A14.02 (shelving and non-sales), A15.01-A15.06 (specifications).
- **Specs.** A15.04 092900 is the gypsum board section: ASTM C754/C1007/C840; deflection L/240 (L/360 at tile); "UL listed fire resistant board throughout" 5/8" (supports Type X); the foil-backed product is printed (H.3); corner bead at external corners and edge trim at dissimilar materials; GA Level 4 finish, so no Level 5. 092950 is the drywall grid suspension. The set has no 054000 or 092216 section, so gauges and deflection track still come from S01.01 and A02.01. No control joints are printed.
- **Door rough openings now printed (A10.08).**
  - FR doors (D): 39 1/4" x 7'-6 1/2".
  - Go-back door (G): 54" x 7'-6 1/2".
  - Cashwrap blind doors (K): 2'-9" x 8'-7 1/8".
  - Display-window blind door (J): 2'-9", head 9.094 ft above the finish floor (derived through the platform).
  - H.M. doors 7B, 8A, 11: B.O. head 7'-0 1/2" printed (A/A10.08); width 3'-0" + 2 x 2" frame = 3'-4", derived.
  - Header: DBL 3 5/8" metal stud lintel.
- **Metal blocking now carried from printed lengths.**
  - A07.04 K1 bench 4'-4"; B1 wardrober 7'-6".
  - C/A10.07 mirrors: 2 rows x (5 x 4'-0" + 3'-6").
  - FR hooks (keynote 57): 6 x 2'-8".
  - B/A10.03: 3 rows of 6" blocking.
  - A14.02 desks 10'-8 13/16" and 5'-9 3/4".
  - Break-room cabinetry 3 rows and coat rack 3 rows: lengths not printed (RFI-09).
  - Total blocking (all metal): see canon `blocking_items`.
- **Wood rule (estimator, applied).** Every wood item is removed from quantities and listed only as an exclusion in `wood_exclusions_info`: the RTU 2x joists and double 2x curb blocking (S05.01), the 3/4" FRT plywood of the water-heater shelf, FRT blocking at doors / storefront / beauty cabinet, wood furring and plywood mounting boards (A14.01), and the 2x4 at the plan tube holder. The old RFI-10 (RTU wood) is dropped. RFI-18 (roof structure) is kept because it changes metal quantities (insulated-wall stud height and hanger-wire drop).
- **MEP.** All M, P and E sheets were swept at overview level and counts recorded in `mep_sweep`. Only M02.01, P02.01, E02.01, E02.51 and E03.01 are plans; none needs a framed opening in a wall. E02.01 boxes and conduit sit in stud cavities.
- **Wall lengths.** The dimensions printed on A02.01 are mostly fixture or niche OVERALL, HOLD and EQ strings, not wall lengths. Three walls are now CONFIRMED by a printed wall dimension: W021 37'-11 3/4" (FR alcove), and W024 and W025 2'-2". All other walls stay DERIVED, with the vector operation stated and a `dim_scan_info` note.
- **RFIs: 19.** RFI-10 was removed. New RFI-19 covers the beauty-cabinet valance soffit (B/A10.03, 1 5/8" framing, count and location not found). New RFI-20 covers the storefront portal built-up box beam and box columns (A08.10, S01.01). RFI-05, RFI-08, RFI-09 and RFI-11 were narrowed using the specs and A10.08.

## Third pass (answer RFIs from the drawings)
- **RFI-19 is closed. Beauty-cabinet valance (B/A10.03).** A06.01 prints 15 cabinets in Room 4. The A/A10.03 TYP bubbles on A02.01 mark 6 cabinet runs, and each run length is printed on A02.01:

  | Run | Printed length |
  |---|---|
  | North | 18'-10 1/2" OVERALL |
  | South | 18'-10 1/2" OVERALL |
  | East at TRANS #5 | 14'-1 1/2" OVERALL (= A/A10.03 14'-1 1/2" HOLD) |
  | Southwest | 9'-4 1/2" OVERALL |
  | Northwest return | 4'-7 1/2" OVERALL |
  | Northeast return | 4'-7 1/2" OVERALL |

  - Total run length is 70.5 LF.
  - Each run is carried as a `soffit_side` (VAL-N, VAL-S, VAL-T5, VAL-SW, VAL-NW, VAL-NE): 1 5/8" studs @16", height 2.167 ft = 8'-4" B.O. soffit (B/A10.03) to the 10'-6" ceiling (A03.01). Board goes on one face only ("no gyp on interior side of valance").
  - The soffit bottom is a `framed_soffit`: 3 5/8" framing with 5/8" board, 70.5 x 1'-11 1/4" = 136.6 SF.
  - The beauty cabinets in Room 2 and Room 5 are freestanding (F and G/A10.03 are VOID), so they get no valance.
- **Cashwrap soffit SS1** is now 15'-1 1/2" HOLD, CONFIRMED from A02.01.
- **RFI-20 is narrowed. Storefront portal (S02.01 plan and sections, S01.01 coded notes).**
  - Beam (1), DBL 6" 20 GA: 2 x 3.77 ft.
  - Beam (2), DBL 8" 18 GA, over the display windows: 2 x 14.20 ft.
  - Beam (3), DBL 10" 16 GA with 20 GA track, front of the grille: 18.81 ft.
  - Beam (4), DBL 10" 16 GA with 16 GA track, back of the grille: 18.21 ft.
  - All beams have 3 5/8" track top and bottom. Beam spans come from the vector at 1/2" = 1'-0" (36 pt/ft), DERIVED; the grille opening 18'-1" is printed on J/A08.10.
  - 12 built-up box posts (coded notes 6 and 16), DBL 3 5/8" 20 GA plus track, x 13'-8 1/2".
  - Grille head box (B/S02.01, D/A08.10): 2 stud lines @16" x 3.208 ft (13'-8 1/2" minus the 10'-6" B.O. portal), with 4 track lines.
  - Display-window head trusses (F/S02.01): 2 stud lines @16" x 3.542 ft per window.
  - 39 clip angles, 2x2 x 16 GA.
  - All of these are carried in `misc_items`. What remains not printed: diagonal lengths, post height to beam bottom, and the 2 1/2" studs below beam 2.
- **RFI-03 is closed.** P/S02.01 and K/S02.01 print the storefront top as "3 5/8", 20 GA TRACK CONT", a standard track, with a diagonal brace and a 2x2x0'-6" 16 GA clip. The grille 1A header is the box beams (3) and (4).
- **RFI-01, RFI-02 and RFI-06 were re-checked and stay open.**
  - RFI-01: C/A12.01 still prints T.O. STUD ±12'-0", against "tight to structure" on A02.01.
  - RFI-02: A03.01 STOCK ceiling 12'-0" against the ±12'-0" T.O. stud of A/A12.01.
  - RFI-06: the suspended stud above the ceiling has no structural detail in S01.01 to S05.01.
- **RFIs now: 17.**
