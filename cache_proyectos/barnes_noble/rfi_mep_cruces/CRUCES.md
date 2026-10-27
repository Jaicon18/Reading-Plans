# Duct crossings at new full-height walls (types 2, 5, E1, E2) — M-102 HVAC plan

Estimator decision: RFI-ACC-stud-reinforcement-mep = count. Rule R80e.30: targeted count only.
- **Method:** visual count on M-102 (HVAC plan, page 48). Each crossing was located by rooms and grid lines and then found at the same place on A-101 (page 6). No geometric registration was used.
- **Wall IDs:** from rev11 (`../FINAL_FOR_REVIEW_2026-10-24_rev11`).
- **Images:** each crossing has two circled crops in `img/`, one of M-102 and one of A-101 at the same location. Each crop was reopened and checked.
- **Formula** (6/A-410 penetration details; skill rule):
  - plates = MAX(1, ROUNDUP(duct width / 16")) x stud rows;
  - every wall here is one stud row;
  - 1 duct sleeve per crossing.

## Crossings
| # | Wall ID | Type | Rooms (A-101) | Duct (M-102) | Width | Plates | Sleeves | Images |
|---|---|---|---|---|---|---|---|---|
| X01 | W2-03 | 2 | Stock Room 111 / Corridor 110 | 14" DIA supply main from RTU-7 into the BOH | 14" [CONFIRMED] | 1 | 1 | `X01_M-102_W2-03.png`, `X01_A-101_W2-03.png` |
| X02 | W2-06.1 | 2 | Corridor 110 / Women's Restroom 109 (above door 9) | 6" DIA branch to CD-1 50 CFM | 6" [CONFIRMED] | 1 | 1 | `X02_*` |
| X03 | W2-06.5 | 2 | Corridor 110 / Men's Restroom 108 (above door 8) | 6" DIA branch to CD-1 50 CFM | 6" [CONFIRMED] | 1 | 1 | `X03_*` |
| X04 | W5-01 | 5 | Women's 109 / Men's 108 (plumbing wall) | exhaust EF-1 / EF-2 6" DIA to the riser drawn on the wall line (8" DIA, note 4: exhaust up through roof) | 6" [CONFIRMED] (riser 8") | 1 | 1 | `X04_*` |
| X05 | W2-07 | 2 | Men's 108 / Janitor 107 | exhaust 6" DIA from EF-3 | 6" [CONFIRMED] | 1 | 1 | `X05_*` |
| X06 | W2-08 | 2 | Janitor 107 / Break Room 106 | 10" DIA supply main | 10" [CONFIRMED] | 1 | 1 | `X06_*` |
| X07 | W2-09 | 2 | Break Room 106 / Manager's Office 105 | 8" DIA to CD-1 125 CFM | 8" [CONFIRMED] | 1 | 1 | `X07_*` |
| X08 | W2-01 | 2 | Sales / Storage 112 (south wall) | 10" DIA from RTU-4 ending at SG-1 10/8 300 CFM on the wall | 10" [CONFIRMED] | 1 | 1 | `X08_*` |
| | | | | | **Total** | **8** | **8** | |

**PENDING:** none. Every width is printed on M-102.

**X04 note:** the 8" exhaust riser is drawn on the W5-01 line. Either a 6" branch crosses the wall into the riser, or the riser runs inside the wall. The count is 1 plate + 1 sleeve either way. Confirm with the mechanical contractor.

## Walls with no duct crossing (checked)
| Wall ID | Type | Why |
|---|---|---|
| W2-02 | 2 | Only a transfer grille (T02 below), no duct |
| W2-04 | 2 | BOH north wall: the supply mains run below it inside the BOH. The CU-1 refrigerant lines (notes 13, 15) are piping, not duct |
| W2-05, W2-06.2, W2-06.3, W2-06.4 | 2 | The mains pass above the chase notch on the corridor side and the branches drop inside the rooms |
| C-E2, C-E1-S, C-E1-P.2, C-E1-B | E2 / E1 | No duct reaches the Cafe south walls. The AHU-1 12" duct crosses the Workroom / Cafe wall and the RTU-2 14" duct crosses the Workroom north wall, but those are type H walls (outside this list) |

## Transfer grilles (wall openings without duct; not in the total)
| # | Wall ID | Type | Opening (M-102) | If counted: plates / sleeves | Images |
|---|---|---|---|---|---|
| T01 | W2-03 | 2 | TG-1 12"x10" 380 CFM, Corridor 110 (note 8: "RETURN AIR GRILLE TO BE MOUNTED AS HIGH AS POSSIBLE ABOVE CEILING") | 1 / 0 | `T01_*` |
| T02 | W2-02 | 2 | TG-1 14"x6" 240 CFM, Storage 112 west wall (note 8) | 1 / 0 | `T02_*` |

If the estimator also frames the transfer grille openings: + 2 plates (no sleeves).

## Result for rev12 (the Excel is not modified here)
- **Stud reinforcement at MEP penetrations:** 8 PCS (8 crossings x 1 plate).
- **Duct sleeves:** 8 PCS.
- **Optional transfer grille openings:** + 2 plates.
- **Source:** M-102 + A-101 (crossing locations); 6/A-410 (penetration details).
