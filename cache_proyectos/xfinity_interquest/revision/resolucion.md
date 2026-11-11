# Resolution A / B — Xfinity Interquest (A2.0 / A1.0 / A3.0)

Each item: difference -> decision -> N/SHEET -> image. Never averaged, never chosen silently.

1. **W2-01 length** — A 10.64 LF (door gap excluded, 4" stub apart) vs B 13.97 LF (through the door) -> **B: 13.973 LF through the door 101 R.O.; stub W2-01a merged (skill rule: one straight line per tag, openings listed in the wall; board never deducts openings U-057)** — source A2.0 dimension string 4" + 3'-0" DOOR — ![img](img/001_DIF_W2_A2.0_p5.png)
2. **W1 / W4 existing walls** — A 12 lines / B 11 lines (W4-04 10.99 vs 10.59 LF) -> **not quantified: 2/A2.0 types 1 and 4 = existing walls to remain, patch and repair only (no LF enters the take-off; the W4-04 difference has no effect)** — source 2/A2.0 — ![img](img/002_DIF_W4_A2.0_p5.png)
3. **Column furring CF-01 / CF-02** — only in A as walls (B: 2 columns, 4.77 LF in its notes) -> **A: 2 x 2.38 LF exposed perimeter, 3 sides, 12.5 ft (key note 1 + A3.0 12'-0" + 6"); 2-1/2" 250S125-43 @16" per A2.0 table** — source 5/A2.0, A2.0 key note 1, A2.0 limiting heights — ![img](img/003_ONLYA__A2.0_p5.png)
4. **Demolition A1.0** — A 63.53 LF (9 pieces) vs B 63.94 LF (8 pieces, DEMO-01+02 joined) -> **A pieces (same lines, |delta| < 1 %); L element DEMO-08/09 = wall by key note 7; height 26'-0" conservative (RFI-01)** — source A1.0 key note 7 — ![img](img/demo_L_A1.0.png)

## RFIs of the readers re-swept (U-156 / U-162: plans first, then code)

- RFI-01 (open): OPEN - loaded 26'-0" (A0.1 building height, conservative) for the 5 braces of 4/A2.0 and the height of the demolished walls
- RFI-02 (closed): CLOSED by the plans: A3.0 tags the strip 'GYP. BD. 8'-6" AFF' (no 'EXISTING' on this tag, unlike the hallway 9'-0" tag) where A1.0 removes DEMO-01; built as a framed header with type W2 framing, underside 1.73 SF + storage face to 10'-6" + hallway face to 9'-6" (A2.0 wall legend 'TO 6" ABOVE CEILING') - loaded (option A).
- RFI-03 (closed): CLOSED by the plans: A1.0 key note 7 ('ALL EXISTING INTERIOR WALLS, DOORS AND WINDOWS AS SHOWN DASHED TO BE REMOVED') points at the inner dashed pair of the L element = wall; DEMO-08 / DEMO-09 loaded.
- RFI-04 (closed): CLOSED by the plans: A2.0 prints '3'-0" DOOR' between the W2 ends = rough opening as drawn (option A); the wall is measured through the opening, so the R.O. only changes the head length.
- RFI-05 (closed): CLOSED by the plans: A2.0 INTERIOR WALL LIMITING HEIGHTS table, 250S125-43 @16" = 13'-0" >= 12'-6" (lightest 2-1/2" member passing at 16" o.c.) - loaded (option A).
- Reader B open questions: deck height = RFI-01; W2 gauge / spacing = A2.0 limiting heights table (362S125-33 @16", 20 ga per 4/A2.0 'MATCH WALL STUD SIZE & GAUGE (3 5/8" 20 GA. MIN.)'); face heights = A3.0 ceiling tags + legend 6"; patch extent of existing walls = Review Item allowance; header build = 7/A2.0; demo height = RFI-01; column size = vector (5.5" x 5.0").

## Alerts of comparar.py

- TAG SIN WALL PT0018-PT0022: wall-type legend symbols of 2/A2.0 (discarded by both readers with image).
- TYPE NO INVENTARIADO '' : column furring (5/A2.0, no tag) - typed COLUMN FURRING by 5/A2.0 + key note 1.
