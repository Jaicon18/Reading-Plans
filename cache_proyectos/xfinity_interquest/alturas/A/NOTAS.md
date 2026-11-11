# Notes: independent height reading (Xfinity Interquest, clean bid set)

Sources used: bidset_SIN_MARKUPS.pdf (A0.1, A1.0, A2.0, A3.0, A4.0, A5.0), set_texto.json, and the location maps (MAPA_A1.0/A2.0/A3.0). No other files were opened.

## Common printed values
- A3.0 RCP ceiling tags: Retail 100 = '2x4 ACT 12'-0" AFF'; Storage 101 = '2x4 ACT 10'-0" AFF' (existing grid and new tiles); Hallway 102 = 'EXISTING GYP. BD. 9'-0" AFF'; Toilets 103/104 = 'GYP. BD. 9'-0" AFF'; header at the north end of Hallway 102 = 'GYP. BD. 8'-6" AFF'.
- A4.0 room finish schedule, ceiling height column: 12'-0", 10'-0", 9'-0", 9'-0", 9'-0". These match A3.0, so there is no conflict.
- A5.0 interior elevations: '12'-0" TO B.O. CEILING' (Retail) and '9'-0" (V.I.F.) B.O. EXIST CEILING' (toilet rooms). These also match A3.0.
- "6 inches above ceiling" appears in 4 places on A2.0: 2/A2.0 Wall Type 2 'FROM SLAB TO 6" ABOVE CEILING U.N.O.', the Wall Legend 'FULL HEIGHT PARTITION TO 6" ABOVE CEILING U.N.O.', 4/A2.0 dimension '6" TYP' above the suspended ceiling, and Key Note 1 (column furring) 'BOARD TO 6" ABOVE CEILING'.
- No deck, structure or bottom-of-joist height is printed on any A, E, M or P sheet. The only overall height is on A0.1 BUILDING DATA: 'HEIGHT IN STORIES: 1 STORY - 26 FT'.

## W2-01: 12.5 ft, DERIVED
- Location: the new W2 partition (hatched, legend "6 inches above ceiling") on the line between Storage 101 (west) and Retail 100 (east), from door 101 down to the W4 junction at the hallway.
- The wall separates two ceilings: Retail 12'-0" and Storage 10'-0". The instructions use the governing/higher side, and 4/A2.0 shows a single top-of-wall 6" above the ceiling. So: 12'-0" + 0'-6" = 12.5 ft.
- Alternative: on the Storage side alone it would be 10'-0" + 6" = 10.5 ft. The 12.5 value was used because the stud and board run continuously to one top track.
- Stud limit check (not a height source): 3-5/8" studs. The limiting-heights table (362S125-xx) allows 12'-6", for example 362S125-27 @ 16" o.c. = 15'-0".

## W2-02: 12.5 ft, DERIVED
- Location: the W2 segment at the east side of Hallway 102 (the 4'-0" segment), with Hallway 102 (9'-0" GYP. BD.) on one side and Retail 100 (12'-0" ACT) on the other.
- Governing side is Retail: 12'-0" + 0'-6" = 12.5 ft.
- Alternative on the Hallway side: 9'-0" + 6" = 9.5 ft.

## CF-01 and CF-02: 12.5 ft each, DERIVED
- Location: the existing columns at the storefront (east) wall inside Retail 100, tagged 5/A2.0 SIM.
- Detail 5/A2.0 is a plan detail and prints no height. A2.0 Key Note 1 says '(1) LAYER 5/8" GYP. BOARD TO 6" ABOVE CEILING'. The ceiling is Retail 12'-0" ACT, so 12'-0" + 0'-6" = 12.5 ft.

## DEMO-01 to DEMO-11: 26.0 ft each, DERIVED
- A1.0 Key Note 7: 'ALL EXISTING INTERIOR WALLS, DOORS, AND WINDOWS AS SHOWN DASHED TO BE REMOVED.' A1.0 prints no height for these walls.
- No structure or deck height is printed anywhere in the set, so the project rule U-174 applies: use the building height from A0.1, 'HEIGHT IN STORIES: 1 STORY - 26 FT', giving 26.0 ft.
- Alternatives seen, none of which is a printed height of the existing walls:
  - Existing ceilings: Storage grid 10'-0" (existing grid to remain), and 9'-0" B.O. existing ceiling at the toilets.
  - A1.0 Demolition Note 18a 'FULL HEIGHT WALL FROM FLOOR TO CEILING' applies only to temporary barriers.
  - The 26 ft is a building/code height (to roof) and is very likely higher than the real existing partitions. Flag this for field verification.

## SOF-01: 3.407 ft developed, DERIVED
- Location: the gypsum board header across the north end of Hallway 102. On A3.0 it is the strip between two horizontal lines, x = 846.84 to 923.28 pt, about 4'-3" long, matching the 4'-3 1/8" hallway width on A2.0. The leader from tag 'GYP. BD. 8'-6" AFF' ends on this strip.
- Sides of the header:
  - North side is Storage 101: '2x4 ACT 10'-0" AFF'.
  - South side is Hallway 102: 'EXISTING GYP. BD. 9'-0" AFF'.
- Top of board follows the wall rule of 6" above that side's ceiling (2/A2.0, Wall Legend, 4/A2.0):
  - North face: (10'-0" + 0'-6") - 8'-6" = 2.000 ft
  - South face: (9'-0" + 0'-6") - 8'-6" = 1.000 ft
  - Underside width: no printed dimension. Scaled on A3.0 between the two header vector lines (visible coordinates 1618.20 pt and 1625.52 pt) = 7.32 pt / 18 pt per ft = 0.407 ft (4.88 in). This equals the printed W2 wall thickness '4 7/8"' on A2.0, but that dimension belongs to the W2 wall, not the header, so it was not used as the source.
  - Total = 2.000 + 1.000 + 0.407 = 3.407 ft.
- Doubts:
  - The north face is taken to the Storage 10'-0" ceiling. If the header board stopped at the hallway ceiling plane only, the faces would differ.
  - The underside is a scaled value, not a printed dimension.

## Room ceiling heights (ALTURAS_CUARTOS.csv)
- Retail 100: 12'-0" new ACT. Storage 101: 10'-0" existing grid with new ACT tiles. Hallway 102: 9'-0" existing gyp. bd. Toilet 103: 9'-0" existing gyp. bd. Access. Toilet 104: 9'-0" existing gyp. bd. Landlord Room (N.I.C.): not printed.
- Hallway 102 and Toilet 103 share one A3.0 tag. A branch leader from that tag enters 103.
- A4.0 and A5.0 agree with A3.0 in every case.
