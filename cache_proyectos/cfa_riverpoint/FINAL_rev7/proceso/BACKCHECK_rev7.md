# BACKCHECK rev7 — CFA #2284 River Point (self back-check of every rev7 change against the drawing)

Program: scripts/backcheck_rev7.py (crops of the clean bid set located by the printed text; Excel evidence searched in the rev7 Excel). Items 1-8 = the rev6 changes (still valid); items 9-13 = the rev7 changes. Material Summary rev6 -> rev7: only +0.01 SF 1/2" cement board (rounding of the split pieces), proceso/CAMBIOS_rev7.md.

| # | Item | N/SHEET | What the drawing shows | Excel rev7 | Crop | Result |
|---|---|---|---|---|---|---|
| 1 | BC-01 RFI-10 closed (R-ALC-07) | A4/S-601 + S-201 | A4/S-601 prints 16'-10 3/4" (F.V.) T/EXIST TOP PLATE = bearing of the existing 2x10 roof joists on the east wall (B.O. structure at that wall): DEMO-09 / -10 loaded to 16'-10 3/4" (R-ALC-07, never to an assumed ceiling). | found in Scope Checklist | backcheck_rev7_img/bc01.png | PASS |
| 2 | BC-02 RFI-10 DEMO-08 bay | S-201 | (+13'-6") TOP OF JOIST of the 16" TJI bay: B.O. = 13'-6" - 16" = 12'-2" = DEMO-08 height. | found in Review Items, Scope Checklist | backcheck_rev7_img/bc02.png | PASS |
| 3 | BC-03 RFI-09 closed (nearest printed spec rule) | A2/S-241 | LGS CEILING JOIST SCHEDULE: 600S162-33 @ 16", column BRIDGING LOCATION = MID SPAN (no member printed). | found in Material Summary, Scope Checklist | backcheck_rev7_img/bc03.png | PASS |
| 4 | BC-04 RFI-09 member | S-902 C05400 3.3.I.1 / 3.4.E.2 | 'Bridging: Cold-rolled steel channel' = the member loaded (1 row 1-1/2" C.R. channel per LGS ceiling, 50.87 LF). | found in Material Summary, Scope Checklist | backcheck_rev7_img/bc04.png | PASS |
| 5 | BC-05 opening schedule (BE-90) | A-801 | DOOR SCHEDULE doors 01-13: all in existing / storefront / wood walls; none tagged on M2.1-01, M3.5-01 / -02 or MB-01 (A-202). | found in Scope Checklist | backcheck_rev7_img/bc05.png | PASS |
| 6 | BC-06 node topology (BE-89) | A-202 | M3.5-01 / M3.5-02 / MB-01 ends die into the existing kitchen wall faces EX-KIT-01..03 (abut, 0 studs - same count as rev6). | found in Partition Takeoff, Material Summary, Review Items, Scope Checklist | backcheck_rev7_img/bc06.png | PASS |
| 7 | BC-07 quote fix (BE-12) | A-611 note 3 | Printed text reads 'CEMEMNTITIOUS BOARD TO STOP - RE: DETAIL' (typo in the plan): quoted verbatim [sic]. | found in Scope Checklist | backcheck_rev7_img/bc07.png | PASS |
| 8 | BC-08 wall type schedule (fichas.json) | A-202 | WALL TYPE SCHEDULE - EXTERIOR / - INTERIOR read independently for fichas.json (SW6, M2.1, M3.5, W4, W4.1, W6, W8). | found in Inputs, Partition Takeoff, Material Summary, Scope Checklist | backcheck_rev7_img/bc08.png | PASS |
| 9 | BC-09 one axis per number: EX-RRM-01-CB | KN10/A-050 + A-611 note A.5 (drawn on A-202) | Men's restroom existing wall: 3 straight axes (west / north / east faces) = EX-RRM-01-CB-1, -2, -3; 7.40 + 11.25 + 8.00 = 26.65 LF = rev6 single entry. | found in Partition Takeoff, Material Summary | backcheck_rev7_img/bc09.png | PASS |
| 10 | BC-10 one axis per number: EX-MP-01 | FRP-2/A-211 + G.3/A-202 (drawn on A-202) | Multi-purpose room existing walls: 6 straight axes, each its own row; pieces add up to the rev6 33.917 LF. | found in Partition Takeoff, Material Summary | backcheck_rev7_img/bc10.png | PASS |
| 11 | BC-11 one axis per number: DEMO-02 | KN3/A-050 | L partition demolished (multi-purpose / mech): 2 axes DEMO-02-1 + DEMO-02-2 = 12.928 LF x 12.167 ft x 2 layers = 314.59 SF (rev6 total). | found in Material Summary | backcheck_rev7_img/bc11.png | PASS |
| 12 | BC-12 ceiling demo as AREA polygon: DEMO-C6 | KN10/A-052 | East-room gyp ceiling hatch = 34.57 SF polygon; 38.35 SF reading A loaded (Review Item 5 open, delta -3.78 SF). | found in Material Summary, Review Items | backcheck_rev7_img/bc12.png | PASS |
| 13 | BC-13 Review Item 6 image = PT0019 mop chase | G.7/A-202 + KN25/A-201 | W6 tag PT0019 at the mop sink chase (rev6 image showed PT0018 / PT0024). | found in Partition Takeoff, Material Summary | backcheck_rev7_img/bc13.png | PASS |
| 14 | BC-14 EX-KIT-02 removed | A3/A-601 + A-202 | Kitchen elevation: 'OPEN TO BEYOND' between the hoods = the 10'-0 1/2" critical clear opening to the drive-thru: no wall, no base. | found in removed from every sheet (CAMBIOS_rev7.md) | backcheck_rev7_img/bc14.png | PASS |
| 15 | BC-15 restroom cement / gyp transition | A2/A-604 | CEMENT / GYP. TRANSITION 2 1/4" (+/-) below T/TILE AT RR: cement board to 6'-6 1/4" = 6.521 ft, MR gyp above. | found in Partition Takeoff | backcheck_rev7_img/bc15.png | PASS |
| 16 | BC-16 MB-01 serving face | D3/A-624 | 1/2" GYPSUM BOARD from 7'-0" A.F.F. BOTT. OF GYPSUM BD. to 6" MIN. over the ACT = 3.5 ft; WALL TILE below -> cement board 0-7'-0". | found in Partition Takeoff, Material Summary | backcheck_rev7_img/bc16.png | PASS |
| 17 | BC-17 BOH base 1'-3" | C3/A-604 | WALL BASE DETAIL @ BACK OF HOUSE prints 1' - 3": loaded on the non-kitchen BOH faces. | found in Partition Takeoff, Material Summary, Scope Checklist | backcheck_rev7_img/bc17.png | PASS |
| 18 | BC-18 dining wainscot plywood by G.C. | C1/A-625 | 1/2" PLYWOOD SHEATHING ABOVE CEMENT BOARD BY G.C. to T/PLYWOOD 6'-4": our gyp only above 6'-4". | found in Scope Checklist | backcheck_rev7_img/bc18.png | PASS |
| 19 | BC-19 W6 dining face full-height tile | A4/A-621 | CT-58A wall tile to CEILING 10'-4" -> cement board full height (precedent #15). | found in Partition Takeoff, Scope Checklist | backcheck_rev7_img/bc19.png | PASS |

Nodes: 6 free of 18 (33%); the 4 free ends are soffit sides on A-221 that die on wood walls (no metal wall there).
RESULT: PASS (19 items)
