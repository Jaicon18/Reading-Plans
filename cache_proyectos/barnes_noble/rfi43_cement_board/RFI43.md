# RFI-43 — 1/2" cement board height on the Cafe south wall, type E1 (C-E1-S, C-E1-P.2, C-E1-B)

Targeted review (R80e.30). E/A-221 prints "E1-1/2" CEMENT BOARD" with no height and "SEE SHEET A-225 FOR FINISH DETAILS". A-225 and A-226A were read as images.

## What the plan prints
| N/SHEET | Printed | Status |
|---|---|---|
| 1/A-225 (finish plan) | South wall of Cafe Sales: "TL-4 ABOVE COUNTERTOP", "B-2 BASE", "FRP-1 BELOW COUNTERTOP" | [CONFIRMED] |
| 6/A-225 (back countertop detail) | "3'-0" AFF TO COUNTERTOP", "CC-1 BACKSPLASH" 4", TL-4 above on the "SCHEDULED PARTITION" | [CONFIRMED] |
| 4/A-226A (Cafe back counter elevation = C-E1-S face) | WD-1 and TL-4 (around the menu boards) up to the top line: **11'-6"** on the main run, **11'-0"** on the 3'-3" box (C-E1-B), with a 6" step. Countertop 3'-0", backsplash 6". FRP-1 below counter, B-2 cove base. Nothing is drawn above 11'-6" | [CONFIRMED] (`01_4-A-226A_C-E1-S_finish_tops.png`) |
| 4/A-226A | Top of TL-4 (where TL-4 ends and WD-1 starts) | [PENDING] (not dimensioned; the menu frames are "7'-0" TO CENTER OF FRAME / MENU") |
| 1/A-121 (RCP) | The strip against C-E1-S is "CAFE GWB 9'-0" PT-5". Behind it: "GWB 11'-6"" (middle band) and "GWB 11'-0"" (center). "CAFE OPEN TO DECK" is at the Workroom side, not at this face | [CONFIRMED] (`02_1-A-121_9-0_band_at_C-E1-S.png`) |

## Height of the cement board per the plan
- **[PENDING]:** the cement board top is not printed, and the two sheets conflict.
  - 1/A-121 puts a 9'-0" GWB ceiling against the wall. With A-410 Partition Notes 3 (+ 6"), the board would stop at **9'-6"**.
  - 4/A-226A draws the wall finishes (TL-4 / WD-1) up to **11'-6"** (11'-0" at the box). That gives **12'-0"** with the + 6".
- **No finish above the ceilings:** none is printed above 11'-6". Nothing on that face is exposed above the ceiling, because the 9'-0" GWB band closes it.
- **Carried today:** 25'-0" (to deck). Neither sheet supports going to deck.

| Alternative | Cement board top | Δ vs carried (25'-0") |
|---|---|---|
| A — 1/A-121 9'-0" band + 6" | 9'-6" | C-E1-S 19.0 x 15.5 = − 294.50 SF; C-E1-P.2 2.11 x 15.5 = − 32.71 SF; C-E1-B 2.31 x 15.5 = − 35.81 SF; total − 363.02 SF |
| B — 4/A-226A finish top 11'-6" + 6" (11'-0" + 6" at the box) | 12'-0" (11'-6" at C-E1-B) | C-E1-S 19.0 x 13.0 = − 247.00 SF; C-E1-P.2 2.11 x 13.0 = − 27.43 SF; C-E1-B 2.31 x 13.5 = − 31.19 SF; total − 305.62 SF |

**Recommendation for rev12 (conservative):** alternative B, 12'-0" (11'-6" at C-E1-B). It covers every finish drawn on 4/A-226A. Keep RFI-43 open with the A − B delta of − 57.40 SF, in case the 9'-0" band governs. The Excel is not modified here.
