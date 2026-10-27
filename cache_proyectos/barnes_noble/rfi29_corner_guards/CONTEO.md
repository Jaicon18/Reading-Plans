# RFI-29 Corner guards — outside GWB corners on the new walls (A-101 / A-221)

Estimator decision: RFI-29 = apply the plan and the spec. Rule R80e.30: targeted count only.
- **Scope:** new walls of rev11 only, no existing walls. Each corner was checked on the plan, with a circled crop in `img/`. Each crop was reopened and checked.
- **What counts:** a GWB outside corner (convex) at an L or a finished free end.
- **What does not count:**
  - T junctions (no outside corner).
  - Ends against an existing wall.
  - Hollow metal door frames.
  - Soffit edges (corner bead, overhead).
  - Counters (millwork, 2'-8").
  - Corners with no gypsum board.

## Sources
| N/SHEET | Printed text | Image |
|---|---|---|
| C22/A-101 | "STAINLESS STEEL CORNER GUARDS AT 48" A.F.F. FOR ALL OUTSIDE GYPSUM BOARD CORNERS AT STOCKROOM WALLS." | `S1_A-101_C22_keynote.png` |
| A-001A (Div 09, Protective corner guards) | "INSTALL METAL CORNER GUARDS (2"X2"X72") AT ALL OUTSIDE CORNERS OR AS SPECIFIED IN THE PLANS." | `S2_A-001A_corner_guards_spec.png` |

## (a) Stock Room 111 — stainless steel corner guard 48" A.F.F. (C22/A-101)
| Location | Wall | Outside corners | Image |
|---|---|---|---|
| W2-03, north end | W2-03 (type 2) | 0: ends against the existing north perimeter wall | — |
| W2-03, south end | W2-03 (type 2) | 0: ends against the existing south perimeter wall | — |
| W2-03, door 11 | W2-03 | 0: hollow metal frame | — |
| **Total (a), new walls** | | **0** | |

**Observation (RFI delta):** the C22 leader points to one outside corner of the existing perimeter, at the loading zone bend in the stock room (`A0_C22-existing.png`). That wall is existing (type 1A, board by future tenant, RFI-01), so it is outside this count. If the estimator carries it: + 1 stainless steel corner guard 48".

## (b) All other outside corners — metal corner guard 2"x2"x72" (A-001A)
| # | Location | Wall ID / column | Type | Corners | Image |
|---|---|---|---|---|---|
| 1 | Storage 112, SW corner (Sales side) | W2-01 / W2-02 (N23) | 2 | 1 | `B01_N23_W2-01-W2-02.png` |
| 2 | Drinking fountain alcove (C26): 2 corners at the mouth on the corridor side + 2 at the back on the restroom side (Women's 109, Men's 108) | W2-06.1 / .2 / .3 / .4 / .5 (N32–N35) | 2 | 4 | `B02_N32-N35_W2-06-alcove.png` |
| 3 | Cafe Seating 102 low wall posts, 2 corners per free end (8 ends) | W3-01, W3-05, W3-06, W3-04 (N45, N46, N49, N50, N53–N56) | 3 (8'-0") | 16 | `B03_*.png` (8) |
| 4 | Hourglass display, north end cap (4 bar corners) | W4-28a / b / c / d / e (N57–N60) | 4 (7'-6") | 4 | `B04_hourglass-north-cap.png` |
| 5 | Hourglass display, south end cap (4 bar corners) | W4-31a / b / c / d / e (N75–N78) | 4 (7'-6") | 4 | `B04_hourglass-south-cap.png` |
| 6 | Column surrounds C25 (24"x24" GWB, slab to 8'-0"), freestanding in Sales 101 | CW-01 … CW-09 | column | 9 x 4 = 36 | `B05_CW-01.png` … `B05_CW-09.png` |
| 7 | Cafe Workroom north wall, east end (Sales side) | C-H1-N (type I end face) | H1 | 1 (the south side is flush with C-H2a) | `B06_C-H1-N-east-end.png` |
| 8 | Grab & Go NW corner | C-H3a / C-H3b (N85) | H3 | 1 | `B07_N85_C-H3a-C-H3b.png` |
| 9 | Grab & Go north wall, east end (Sales + Grab & Go sides) | C-H3a (type I end face, N86) | H3a | 2 | `B08_N86_C-H3a-east-end.png` |
| 10 | Workroom door pier, NE corner (Cafe side) | C-I-P.1 / C-E1-P.2 (N90) | I / E1 | 1 (NW is an inside corner) | `B09_N90_pier.png` |
| 11 | SE box of Cafe Sales, NW + NE corners | C-E1-B / C-F / C-I (N92, N94) | E1 / F / I | 2 | `B10_N92-N94_SE-box.png` |
| | **Total (b)** | | | **72** | |

## Checked and not counted
| Item | Why |
|---|---|
| W2-03 and W2-04 free ends | W2-03 runs to the existing perimeter walls; W2-04 continues as C-H1-N (T) |
| W2-02, W2-05, W2-07, W2-08, W2-09 and W5-01 ends | Against the existing perimeter (end stud) |
| Hourglass curved legs (W4-29a–f, W4-30a–f) | The L nodes are arc chords, not corners. The cap-to-leg joints are inside corners |
| C-H2b stub (Cafe Workroom) | 5/8" FRT plywood both sides (G/A-221 H2b), no gypsum board |
| Cafe Workroom box corners at C-E2 (N81, N82) and at C-H1-N / C-H1-W (N79) | Against the demising wall gap, or a T with W2-04 |
| SS-N, SS-E, SS-IN-N, SS-IN-E, SS-GG | Soffit edges (overhead corner bead, already in the trim row) |
| C-A, C-B, C-C, C-D | Counters 2'-8" (millwork) |
| All door openings | Hollow metal frames |

## Result for rev12 (the Excel is not modified here)
- **(a) Stainless steel corner guard 48" A.F.F. (C22/A-101):** 0 on the new walls. The RFI delta is + 1 if the existing C22-tagged corner is carried.
- **(b) Metal corner guard 2"x2"x72" (A-001A):** 72 pcs:
  - type 2: 5;
  - type 3: 16;
  - type 4: 8;
  - column surrounds: 36;
  - Cafe: 7.
- **Notes:**
  - Rows 4–5 (type 4, 7'-6") and row 3 (type 3, 8'-0") take the 72" guard.
  - The 2 restroom-side alcove corners (row 2) are wet-room faces; check them against the tile finish.
