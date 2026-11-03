# BACKCHECK rev5 — CFA #2284 River Point (self back-check of every rev5 change against the drawing)

Program: scripts/backcheck_rev5.py (crops of the clean bid set located by the printed text; Excel evidence searched in the rev5 Excel). No Material Summary quantity changed in rev5 (proceso/CAMBIOS_rev5.md: delta 0 on every row).

| # | Item | N/SHEET | What the drawing shows | Excel rev5 | Crop | Result |
|---|---|---|---|---|---|---|
| 1 | BC-01 RFI-10 closed (R-ALC-07) | A4/S-601 + S-201 | A4/S-601 prints 16'-10 3/4" (F.V.) T/EXIST TOP PLATE = bearing of the existing 2x10 roof joists on the east wall (B.O. structure at that wall): DEMO-09 / -10 loaded to 16'-10 3/4" (R-ALC-07, never to an assumed ceiling). | found in Scope Checklist | backcheck_rev5_img/bc01.png | PASS |
| 2 | BC-02 RFI-10 DEMO-08 bay | S-201 | (+13'-6") TOP OF JOIST of the 16" TJI bay: B.O. = 13'-6" - 16" = 12'-2" = DEMO-08 height. | found in Review Items, Scope Checklist | backcheck_rev5_img/bc02.png | PASS |
| 3 | BC-03 RFI-09 closed (nearest printed spec rule) | A2/S-241 | LGS CEILING JOIST SCHEDULE: 600S162-33 @ 16", column BRIDGING LOCATION = MID SPAN (no member printed). | found in Material Summary, Scope Checklist | backcheck_rev5_img/bc03.png | PASS |
| 4 | BC-04 RFI-09 member | S-902 C05400 3.3.I.1 / 3.4.E.2 | 'Bridging: Cold-rolled steel channel' = the member loaded (1 row 1-1/2" C.R. channel per LGS ceiling, 50.87 LF). | found in Material Summary, Scope Checklist | backcheck_rev5_img/bc04.png | PASS |
| 5 | BC-05 opening schedule (BE-90) | A-801 | DOOR SCHEDULE doors 01-13: all in existing / storefront / wood walls; none tagged on M2.1-01, M3.5-01 / -02 or MB-01 (A-202). | found in Scope Checklist | backcheck_rev5_img/bc05.png | PASS |
| 6 | BC-06 node topology (BE-89) | A-202 | M3.5-01 / M3.5-02 / MB-01 ends die into the existing kitchen wall faces EX-KIT-01..03 (abut, 0 studs - same count as rev4). | found in Partition Takeoff, Material Summary, Review Items, Scope Checklist | backcheck_rev5_img/bc06.png | PASS |
| 7 | BC-07 quote fix (BE-12) | A-611 note 3 | Printed text reads 'CEMEMNTITIOUS BOARD TO STOP - RE: DETAIL' (typo in the plan): quoted verbatim [sic]. | found in Scope Checklist | backcheck_rev5_img/bc07.png | PASS |
| 8 | BC-08 wall type schedule (fichas.json) | A-202 | WALL TYPE SCHEDULE - EXTERIOR / - INTERIOR read independently for fichas.json (SW6, M2.1, M3.5, W4, W4.1, W6, W8). | found in Inputs, Partition Takeoff, Material Summary, Scope Checklist | backcheck_rev5_img/bc08.png | PASS |

Nodes: 4 free of 18 (22%); the 4 free ends are soffit sides on A-221 that die on wood walls (no metal wall there).
RESULT: PASS (8 items)
