# LECTURA B — VS #679 Stonewood Center (Downey CA) — reading notes

Canon: `takeoff_canon_B.json`. Validation: `python3 validar_canon.py takeoff_canon_B.json tools` printed **CANON OK**. Generator: `gen.py`. Fragments are in `2_lectura/B/`.

## Sheets read
A02.01 (the full plan, swept by vector hatch, plus the Partition Schedule and keynotes), A03.01 RCP (ceiling heights and keynotes), A00.02 door schedule, A00.03 finish schedule, A05.01 finish plan (WC-1 wainscot), A07.01 elevations, A08.01 / A08.15 storefront, A10.01 (R/S column wrap, B fluted pilaster), A12.01 (A, C, E, F, R), A12.02 (N, E, A, J), A13.01 restrooms, A14.01 shelving, S01.01 (Table 1-3 stud matrix, coded notes L, notes C), S02.01 storefront framing, S03.01 (A, E, L, N, R, G), S03.02, S05.01, M02.01 / P02.01 (registered sweep). I looked at the other M and P sheets for crossings: they hold notes, schedules and details only.

## Method
The text on the sheets is outlined. Walls were found from the A02.01 vector hatch:
- standard partition: 0.48 pt lines at 135°
- RFID and storefront: crosshatch
- insulated: zig-zag triangles

The band coordinates are the hatch extents, in as-seen pt at 18 pt/ft (1/4" = 1'-0", checked against the 4'-6" HOLD dimension). Lengths are DERIVED from the vectors. Each L corner has one owner (the H wall). Door R.O.s sit inside their runs.

## Walls by hatch type (count / LF)
| Type (hatch, M/A02.01) | Count | LF |
|---|---|---|
| (N) Standard partition, both faces, A/A12.01 | 60 | 396.19 |
| (N) Standard partition furred one side at (E) demising or void, C/A12.01 | 33 | 269.53 |
| RFID shielded, A/A12.01 + A/S03.01 | 2 | 59.22 |
| (N) Insulated wall, C/A12.01 | 8 | 45.22 |
| (N) Storefront wall (piers / ends), S02.01 | 6 | 21.39 |
| **Partitions total** | **109** | **791.56** |
| Column wraps, R/A10.01 (1-5/8") | 4 | 16.87 |
| Soffit sides (cashwrap, display heads, portal) | 5 | 78.50 |
| **All wall elements** | **118** | **886.93** |

The (E) demising walls are existing to remain, so they get no new framing. The 1-hour type is struck through on the schedule.

## Heights chain
- **Partition studs:** T.O. stud ±12'-0" A.F.F. [CONFIRMED A/A12.01, C/A12.01], with diagonal braces to structure at 48" o.c. (A/S03.01). Top track is standard; these walls do not reach the deck.
- **Insulated walls:** "tight to structure", so they use the slip-track in L/S03.01. Their height is the B.O. of structure, which is not printed anywhere: 15'-0" is assumed [PENDING, RFI-01].
- **Storefront:** 13'-8 1/2" to the B.O. of the (E) mall soffit (A/A08.01).
- **Faces:**
  - Gyp-ceiling rooms: board goes to the ceiling height on A03.01.
  - ACT rooms: ceiling + 6" (C/A12.01), capped at T.O. stud 12'-0" (RFI-03).
  - RFID wall, sales side: ceiling + 6".
- **Ceilings:** gyp board on a USG drywall grid per N/A12.02, 17 areas totalling 6,228 SF. The hanger drop is pending RFI-01. ACT ceilings are excluded.

## RTU support framing (S05.01) and wood
S05.01 framing is all **wood**:
- new 2x joists to match existing (2x10 assumed, 6 leaders "TYP @ EA RTU"), spanning 19'-8 3/8" and 19'-10 11/16"
- double 2x blocking (coded note 1, C/S05.01)
- MSTA hold-down straps

Under the coordinator's rule (wood is not in scope), these are **EXCLUDED**, along with:
- the E/S03.01 2x6 brace blocking
- the 1x6 shelving furring (D/H A14.01)
- the FRT wood blocking and plywood (A08.15, N/S03.01)

Each exclusion is listed in `wood_exclusions_info`. No wood quantities are carried.

## Metal items carried (misc / blocking)
- Diagonal braces (A/S03.01) and their clips
- Storefront box posts (S02.01 coded notes 6 and 16, 12 posts in all) and beams 1 (DW2), 2, 3, 4 (L/S01.01)
- Water heater shelf framing (N/S03.01): 6" joists, 6" 16 ga track, jack studs, clips
- In-wall metal blocking per E/F A12.01: restrooms, shelving A-1 / A-2 / A-8, mirror keynote 41
- Corner bead
- FRP WC-1 at 4'-0" in the restrooms, break room, hallway and electrical room
- Access panels (RCP keynotes 5 and 8)
- 31 registered MEP crossings (M02.01 / P02.01, dx/dy ≈ 0)

## RFIs (15)
| RFI | Subject |
|---|---|
| 01 | B.O. structure (deck) height |
| 02 | Stock shelving walls: S03.02 13'-0" vs 12'-0" |
| 03 | Stock ACT ceiling + 6" exceeds the stud height |
| 04 | Stud spacing halved at spines with fixtures on both sides |
| 05 | Door R.O. / head |
| 06 | Break-room cased opening head |
| 07 | Cashwrap soffit detail |
| 08 | Water heater shelf elevation |
| 09 | Accessory blocking lengths |
| 10 | 1/4" + 3/8" panel alternative |
| 11 | Third beam 1 span (S02.01) |
| 12 | Shelving blocking rows |
| 13 | FRP extent / tile base backer |
| 14 | 1/2" MR at the storefront mall face carried in the Type X W.R. family |
| 15 | Keynote-8 access panel count |
