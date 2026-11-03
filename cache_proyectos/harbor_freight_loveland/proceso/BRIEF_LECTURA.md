# Harbor Freight Tools - Loveland, CO — Stage 2 reading brief (common to readers A and B)

Project: Harbor Freight Tools tenant improvement in an EXISTING building, 1325 E. Eisenhower Blvd., Loveland, CO 80537.
Architect ADA Architects (Lakewood, OH). GC inviting: Marco Contractors. Invite data (NOT a drawing source, verify in the set):
15,813 SF existing building; deck height 18'-3" to 16'-11". Scope summary on A0.0: new restrooms / break room, offices,
NEW 1-HOUR FIRE-RATED DEMISING WALL (type D) to separate the adjacent tenant and the landlord riser room.
Our scope = cold-formed METAL framing (Div. 05 40 / 09 22) and GYPSUM BOARD (Div. 09 29) ONLY, incl. taping/finishing
quantities, and DEMOLITION of gypsum board and metal framing. FRP: ours only if the finish schedule / specs put FRP on
our gypsum walls — record where FRP occurs (rooms, height, sheet) in misc_items with familia "FRP panels" (qty SF, the
calculator decides scope); if FRP is by others / tenant vendor, say so with N/SHEET.

## Your sandbox (work ONLY here; do not open any other directory, repo or previous take-off)
`<SB>` = your sandbox root (given in your task). Contents:
- `plano.pdf` — clean bid set, 50 pages, 2592 x 1728 pt. Pages 1-30 rotation 0; pages 31-50 rotation 270 (use page.rect /
  coordinates of the page AS SEEN, i.e. rotated, like the PNG). `python3 -I` + `import pymupdf as fitz`.
  Text extractable on most sheets; drawing text of some M/E sheets and EMS-1..4 (p47-50) lives ONLY in "AutoCAD SHX Text"
  annotations (`page.annots()` → `annot.info['content']`). A0.3 (p6) and A0.4 (p7) are mostly RASTER (render them at
  150-200 dpi and read as images: they may hold project specifications — check for gypsum / metal stud / FRP specs).
- `SHEET_MAP.json` — page (1-based) → sheet. p1 A0.0 Cover + index + CODE AND BUILDING DATA; p2 AS1.0; p3 AS1.1;
  p4 D1.0 DEMOLITION PLAN (200 series keynotes, general demolition notes, demo legend); p5 A0.2 GENERAL NOTES; p6 A0.3;
  p7 A0.4; p8 A1.1 FLOOR PLAN (scale 3/32" = 1'-0"; wall legend, 300 series keynotes, floor plan notes); p9 A1.1A LIFE
  SAFETY; p10 A1.2 FIXTURE PLAN (fixture wall blocking); p11 A1.3 FINISH PLAN + ROOM / FINISH SCHEDULE; p12 A1.3A
  FINISH DETAILS (fixture wall blocking detail, corner guard detail); p13 A2.0 REFLECTED CEILING PLAN (+ wall type E note,
  ceiling key notes, bracing); p14 A3.0 / p15 A3.1 exterior elevations / sections; p16 A4.0 ENLARGED RR / BR PLANS +
  interior elevations; p17 A4.1 WALL TYPES & DETAILS (WALL TYPE A, B, C, D (1-hour), E; lateral bracing 2/A4.1;
  control joint 7/A4.1; slip track 10/A4.1; wall type notes); p18 A4.2; p19 A4.3; p20 A5.0 DOOR SCHEDULE; p21 A5.1 door /
  window details; p22 A5.2 vestibule enlarged plans / storefront elevations; p23 A5.3 storefront details (vestibule
  bulkhead section, box header, typical slip track detail); p24-30 S1.0..S4.1 structural (B.O. structure / joist info);
  p31-34 M; p35-36 P; p37 FP1.0; p38-46 E; p47-50 EMS (vendor, SHX text only).
- `inventario/inventario.json` + `inventario.md` + `recortes/` — Stage-1 inventory by script. Types found: A, B, C, E (+ D
  title "WALL TYPE D : 1-HOUR FIRE RATED WALL" not parsed — D exists, A4.1). The plan tags are SINGLE LETTERS inside
  a symbol, so the script could not count them: it lists hundreds of `partition_ambiguo` candidates (PAnnnn). Only those
  on plan sheets that are real wall-type tags matter: put each REAL tag id you use in the wall's `tag_ids`; you do not
  need to dispose of the hundreds of loose-text candidates (notes, legends, grid letters) — the calculator stage does it
  by program. But COUNT every wall-type tag symbol on A1.1 / A4.0 / A5.2 / A2.0 yourself and list them (tag letter,
  page, x, y) in `constants.tag_sweep_info` so A vs B can be compared.
- `skill/` (SKILL.md + tools/ + runner/prompts/lectura.md), `tools` link, `validar_canon.py`.

## WALL TYPES (A4.1, p17) — read each section yourself; summary to orient only
CORRECTION (BE-HF01, found by reader B): the A/B/C lines below were mis-assigned from text order. Per the drawn sections:
A = 6" x 20 GA studs @ 16" to deck, board both sides; B = 2-1/2" furring, 8'-6", board one face; C = 3-5/8" furring,
8'-6", board one face. D and E as written.
- A: read the section (may be existing / masonry / other). B: 6" x 20 GA metal studs @ 16" O.C., 5/8" gyp bd, "gyp bd
  continues to deck if suspended ceiling does not occur". C: low wall (2-1/2" x 20 GA track, 8'-6", "end gyp bd 6" above
  suspended ceiling"). D: 1-HOUR demising, 6" x 20 GA studs @ 16", 1 layer 5/8" Type X each side, to existing deck,
  slip track (10/A4.1). E: 5/8" gyp bd on 1-1/2" metal hat channel @ 24" O.C. vertical over existing masonry;
  "E at SOUTH wall to underside of existing roof deck; E at WEST wall to 16'-0" A.F.F." (also A2.0 / A1.1 key note
  "EXTENT OF WALL TYPE E @ 16'-0" A.F.F."). Lateral bracing 2/A4.1 (Spazzer 9200 spacing bar, metal stud brace 5'-0"
  O.C. max at mid-point between end of board above ceiling and structure). Control joints 30'-0" max (7/A4.1).
- Heights: B.O. structure / deck: search D1.0 notes, A1.1 notes ("ALL WALLS BRACED TO STRUCTURE ABOVE @ 4'-0" O.C.
  MAX", "all exposed walls to underside of structure"), A2.0 (ceiling heights, "TO UNDERSIDE OF STRUCTURE"), A3.x sections,
  A4.x, S sheets (joist bearing / T.O. steel). Ceiling height per room from A2.0 RCP / A1.3 room schedule. Every height
  CONFIRMED with sheet, DERIVED with operation, or PENDING + RFI with conservative value. Never scale a height.

## Fixed scope rules (estimator standing orders — apply, never ask)
- Wood always EXCLUDED (Div. 06) incl. FRT wood blocking, plywood: only a note "EXCLUDED - wood framing / blocking (Div. 06),
  not in scope: <item> <N/SHEET>". If a detail gives "metal or wood" → metal.
- Trades we do NOT do → EXCLUDED, no RFI: ACT / acoustical ceilings and their grid / seismic, insulation (batt, rigid),
  acoustical sealant, tile, paint, wall covering, millwork / casework, storefront, doors / frames, roofing, MEP, structural
  steel, masonry, signage, fixtures. Fasteners / screws / anchors / PAF = EXCLUDED (0). Framed openings for ducts = EXCLUDED.
  Existing ceiling demolition with no ceiling type shown = EXCLUDED "for lack of information" (0 SF).
- Accessory blocking with no printed width = 3'-0" x 2 rows per accessory (printed rows / length govern); metal only.
  Fixture wall blocking (A1.2 / A1.3A "FIXTURE WALL BLOCKING DETAIL"): if metal, quantify by its printed extent.
- DEMOLITION of gypsum board and metal framing IS ours (D1.0 keynotes: e.g. 205 "remove existing gyp bd wall and
  associated framing", 216, 218 "existing walls to be removed" etc. — read all 200-series keynotes and the demo legend).
  For each demo element: misc_items entry {ref "DEMO-nn", familia "demolition - gypsum board and metal framing", qty SF,
  unit "SF", source N/SHEET + keynote, op "L x H x layers = SF"} and a `demo_geom` list entry (top-level key in your canon
  is NOT allowed — write it to `<SB>/demo_geom_<A|B>.json` instead) {id, group, page, polyline [[x,y],...] in pt of D1.0,
  lf, h_ft, h_status, layers, sf, keynote, sheet}. Height searched in ALL sheets with #0 status (partitions to be
  demolished with no printed height = to the printed B.O. structure of their bay, never to an assumed ceiling).
  Cross-check demo plan vs new floor plan wall by wall and write the table to `<SB>/demo_cruce_<A|B>.md`.
  Only gyp / metal is ours; masonry demolition is not.
- Board and Level 5 NEVER deduct openings nor base. What is printed is loaded, never asked. Board height on a face comes
  from a dimension whose two ends are edges of the board on THAT face. A face goes up to the ceiling of the room it faces
  (+6" where the type says so); to deck only where the room is open to structure or the type/detail says full height.
- Two kinds of track, always separate: standard track (bottom + top of walls that do not reach structure) and deflection /
  slip track (top of walls that reach structure, 10/A4.1 and A5.3 typical slip track detail).
- #0 dimensional honesty: every number CONFIRMED (printed dim + sheet) / DERIVED (vector or arithmetic, op written) /
  PENDING. Verify the plan scale against one printed dimension and write that check in `length_op` of the first wall.
- Specs: there is NO project manual in the set; sweep A0.2 general notes, A0.3 / A0.4 (raster), A4.1 wall type notes and
  any spec text on the sheets for gypsum / metal framing / FRP / finish level, and cite the note in each material. Where
  the set is silent apply the trade code (ASTM C754 / C840, GA-216, AISI S220) with its citation.
- Every RFI = options {A: {texto, source N/SHEET, delta}, B: {texto, cita (trade code), delta}, C: ""}, with
  `fuentes_revisadas` = the list of sheets and search terms you swept (sweep the WHOLE set + text grep BEFORE any RFI;
  if the answer is printed anywhere, apply it with N/SHEET instead of an RFI). Unknowns never stop the work: conservative
  value LOADED + RFI.

## Schemas
- Canon keys: exactly the canon schema of `skill/SKILL.md` §4 and `skill/runner/prompts/lectura.md` (read that file: its
  generic rules apply; its sheet names A-410 / A-221 / … belong to another project — use THIS project's sheets).
- `existing_walls[]` (board-only entries, e.g. type E board on hat channel over existing masonry if the schema fits better
  as wall with furring — read the docstring of `_existing_walls` in tools/canon.py and SKILL.md; the hat-channel furring
  is METAL and ours, so type E must carry its hat channel quantity: use walls[] with the furring element the schema allows
  (search SKILL.md for "hat channel" / "Z-furring" / "furring") ).
- constants: plan_scale_pt_per_ft {value, source} AND plan_scale_by_sheet {"A1.1": {value, source}, ...} (3/32" = 1'-0"
  → 6.75 pt/ft; verify with a printed dimension).
- ceilings[] for gypsum ceilings / soffits / bulkheads from A2.0 + A5.3 vestibule bulkhead section (board key, area_sf,
  height, perimeter, system, source); ACT = EXCLUDED (note only).
- mep_sweep with the M- / P- sheets listed (ducts crossing walls are EXCLUDED anyway; record count + reason).

## ONE WALL, ONCE
A1.1 is the trade floor plan (measure there); A4.0 / A5.2 enlarged plans: a wall inside an enlarged area is counted ONCE
(on the sheet where its tag is clearest; record which). Untagged walls: give default_type_source / part_of /
untagged_reason.

## Output
Write `<SB>/takeoff_canon_<A|B>.json` and validate: `cd <SB> && python3 validar_canon.py takeoff_canon_<X>.json tools`
→ must print "CANON OK" (fix and rerun until it does). English in every text field. Do NOT generate evidence images
(programs do it from your coordinates); bands / paths must lie on the drawn line. Scratch only in `<SB>/scratch/`.
Also write `<SB>/notas_<A|B>.md`: project data sheet (name, address, type, owner/tenant, architect, GC, SF, stories,
construction type, occupancy, codes, occupant load, sprinklered, demo yes/no, specs yes/no — each with its SHEET), the
heights chain, the FRP finding, and the list of sheets you opened.
When finished reply ONLY with a short summary (≤ 25 lines): LF per type, board SF per board key, ceilings SF, demo SF,
RFI count with one line each (id, question, A delta / B delta), problems with the tools/schema.
