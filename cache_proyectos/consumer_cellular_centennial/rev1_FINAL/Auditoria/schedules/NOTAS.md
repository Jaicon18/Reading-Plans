# NOTAS - independent schedule reader (2026-11-05)

Coordinates: x,y in pt on the visible (rotated) page, top-left of the row label. Rendered with `clip` in visible coords; `search_for` boxes times `rotation_matrix`. All crops are in img/.

## Partition types (A500, 1/A500)
- The A500 diamonds print **A#, C#, D, E, H**. The "#" stands for the stud size from the plan-view legend (1 = 1-5/8", 2 = 2-1/2", 3 = 3-5/8", 4 = 6").
- A100 tags: A3 x4, C3 x2 (one may be a legend instance), D x1, E3 x11. **H is not tagged on A100**, so it is probably unused.
- Gauge, all @16" o.c.: A = 20 GA, C = 18 GA, D = 6" 20 GA, E = 18 GA, H = 6" 20 GA. No SSMA designations except the brace (362S137-33).
- Faces: C, D and E say "ON EACH SIDE". H says "ON ONE SIDE".
- **A (furred wall) text says "ON EACH SIDE", but only the tenant face is drawn**, with a 1/2" gap to the existing wall. This conflict needs an RFI.
- Heights: A, C, D and H studs go to B.O. (E) deck (ply deck @16'-4" / 17'-1 9/16"). The board stops 6" above the ceiling.
- E3 studs stop 6" above the ceiling and are braced per 3/A500 (and 6/A500). Its top track is 20 GA with 1/2" deflection.
- Detail 4/A500 C-channel is printed 3-5/8" x 20 GA. That does not match the 6" studs in D and H.
- Detail 5/A500 is not referenced by any type.

## Schedules / flags
- A600: the frame is HM knockdown. Jamb 3/A600 has double studs and 3 anchors per jamb. Head 2/A600 is 2" min. to the finished ceiling. Doors 1A and 2B are existing.
- A700 is titled "ARCHITECTURAL SPECIFICATIONS" but holds only the schedules. It contains no written specs.
- In the A700 FF&E schedule, "shelving above mop sink on 6/A500" is a wrong reference. The shelving is on A504.
- Ceilings:
  - C-1 gyp. bd.: restroom only, 8'-0", painted PT-1.
  - C-2 ACT: 11'-11" in sales, BOH and hall; 9'-0" in office and utility.
  - Existing soffit: 11'-9", PT-1.
  - C-3: legend only.
- FRP to 4'-0" in the restroom (A402) and at the mop sink (A504).
- Blocking:
  - 20 GA strap per A104 (logo wall, slat wall, kitchenette).
  - Backing plate per 4/A104.
  - Grab bars: 20 GA track per 5/A402.
  - "Provide blocking at all wall mounted fixtures" (A402 GN 4).
  - Pendant light: FRT plywood per 1/A501.
  - Exterior signage blocking per A300/A301.
- Set label: the title blocks print "90% SET / DESIGN INTENT ONLY / NOT FOR CONSTRUCTION" under the seal graphic. They are sealed 10/15/2026. "Permit Set" is not printed. GC names and bid dates are not in the set (they come from the estimator).
- The drawing index calls A503 "SLAB DETAILS", but its text is UL firestop systems. It was not examined further.
