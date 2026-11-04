# CAMBIOS FINAL7 - Chuze Fitness Austin Bluffs (FINAL6 -> FINAL7, 2026-11-04)

Why: the v33 delivery gate (CE_CALLOUTS, U-113 / BE-124 + U-137) reads the two-line bubbles of every trade sheet (enlarged plans, elevation marks, detail callouts) and follows each chain to its end. FINAL6 left 208 bubbles on the trade sheets and 16 chain links with no disposition. Every bubble now ends either cited N/SHEET in the canon row it governs or declared in callouts_no_aplican.json with the motive read on the detail itself.

## 1. Bubble chain (computed from the canon and callouts_no_aplican.json)

- Distinct callouts reached from the trade sheets: 217 (chains followed through 42 sheets).
- Cited N/SHEET in the canon: 180 (616 citations on 111 wall / existing-wall rows in the new field callout_refs, plus the rows that already cited their detail, plus 5/G005 in the G004 grab bar backing row).
- Declared not applicable with motive: 37 (callouts_no_aplican.json).
- Still open: 0.

How they were disposed:
- Enlarged-plan callouts on A101 (1/A421, 1/A422, 1/A423, 1/A424, 5/A425, 2/A426, 2/A427, 2/A429, 2/A431, 1/A432, 1/A434, 2/A435): cited on every wall measured on that enlarged plan. 1/A428 (Lift Lab) declared: A428 has no new walls.
- Interior elevations: title read from the elevation sheet ('SCALE:' block), cited on the walls of the room named in the title. Read on the plans where the title does not name a room of ours: 9-12/A423.B are titled 'SAUNA 2-' but the elevation mark sits inside IT/AV 132 (racks A2.28, roof ladder A2.163 drawn) - cited on the IT/AV 132 walls; 1/A434.A draws the 5'-0" low wall (A-A421-3, 5.0 ft loaded); 3/A434.A draws the Group X / Recovery south line (A-A427-3).
- Declared with motive: exterior elevations A201 (existing shell, no exterior framing), Lift Lab A428 / A428.A (existing walls), gym elevations A437 / 2/A437.A (paint, graphics, mirrors; mirror backing = A103 item 44 wood, EXCLUDED), millwork A503.A / A503.B / A503.C (casework on 'wall type as scheduled'), sauna heater 9/A504, floor transitions / tile edges / wall covering / locker concrete base / percussion gun bracket on A505.A, access gate, railings, lighting cove bracket, rubber transition on A505.B, vanity light mounting heights 13/A424.C.
- Crops read for anything that could change framing or board (walls, soffits, ceilings, demolition first): no detail draws a stud, track, board or backing that the take-off does not already carry; the detail texts say 'WALL TYPE / PARTITION AS SCHEDULED'. 3/A505.B (12"x8" lighting cove brackets @ 60" o.c.) and 17/A505.A (Hyperice bracket) print no backing.

## 2. Delta per material (Material Summary, FINAL6 -> FINAL7)

No quantity changed: all 67 Material Summary rows (Net and Purchase) are identical to FINAL6. FINAL7 adds citations and declarations only.

Earlier changes: CAMBIOS_FINAL6.md (FINAL5 -> FINAL6).
