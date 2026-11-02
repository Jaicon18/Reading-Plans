# Chick-fil-A #2284 River Point (Sheridan, CO) — Stage 2 reading brief (common to readers A and B)

Project: existing Chick-fil-A restaurant, 4090 River Point Pkwy, Sheridan CO 80110. Reinvestment remodel: building
addition (~573 SF), kitchen and drive-thru upgrade / expansion, new canopies. Architect Mayse & Associates.
Our scope = cold-formed METAL framing (Div. 05 40 / 09 22) and GYPSUM / CEMENT BOARD (Div. 09 29) ONLY, incl.
taping/finishing quantities and demolition of gypsum board and metal framing.

## Your sandbox (work ONLY here; do not open any other directory, repo or previous take-off)
`<SB>` = your sandbox root (given in your task). Contents:
- `plano.pdf` — clean bid set (172 pages, 3024 x 2160 pt, rotation 0). Open with `python3 -I` and `import pymupdf as fitz`.
  Text extractable (`page.get_text('words')`), geometry vector (`page.get_drawings()`), pt origin top-left.
- `plano_con_texto_MEP.pdf` — same set but keeps the "AutoCAD SHX Text" annotations: on M/P/E sheets (pages 76-117)
  the drawing text lives ONLY in those annotations (read them with `page.annots()` → `annot.info['content']` / rect).
  Use it only for the MEP sweep.
- `SHEET_MAP.json` — page (1-based) → sheet number. Key pages: G-000 p1 (sheet index, code data), A-050 Demolition
  Plan p6, A-052 RCP Demolition p7, A-201 Floor Plan p12, A-202 Dimensional Control Plan + WALL TYPE SCHEDULES +
  WALL NOTES (B/C/D/E/F/G/H notes) p13, A-211 Wall & Floor Finish Plan p14, A-221 RCP p15, A-230 Roof p16,
  A-301/A-302 Ext. Elevations p17-18, A-401 Building Section p19, A-402 Wall Sections p20, A-501..A-503 Exterior
  Details p21-23, A-601..A-603 Kitchen Elevations p24-26, A-604/A-605 BOH Details p27-28, A-611 Restroom p29,
  A-621..A-623 Dining Elevations p30-32, A-624 FOH Details p33, A-625 Dining Interior Details p34, A-701 Millwork p35,
  A-801 Door Schedule p36, A-901..A-911 SPECIFICATIONS p37-47 (find 05 40 00 / 09 21 16 / 09 29 00 / 09 22 16),
  S-001 p64, S-201 Roof Framing p66, S-241 DROPPED CEILING PLAN p67, S-600 Typical Wood Framing p70, S-601 p71,
  S-610 p72, S-801 Typical Nonstructural Details p73, S-901/S-902 specs p74-75, M/P/E p76-117, K kitchen p118-133.
  Pages 48-63 are raster vendor canopy sheets (OMD) and 139-172 vapor-control / civil / landscape: not our trade.
- `inventario/inventario.json` + `inventario.md` + `recortes/` — Stage-1 partition-tag inventory by script: 26 tags,
  ALL on A-202 (p13): M2.1 x2, M3.5 x3, W4 x1, W4.1 x2, W6 x12, W8 x2, SW6 x4 (ids PTnnnn, bbox, circled crops).
- `skill/` (SKILL.md + tools/), `tools` link, `validar_canon.py`.

## WALL TYPES (A-202 WALL TYPE SCHEDULE) and what is OURS
- METAL (framing + board are ours) → `walls[]` (element "wall" or the closed-list element that fits):
  - M2.1 = 2" metal Z channel 2'-0" o.c. with 1/2" sheathing on exposed side (furring on existing wall).
  - M3.5 = 3-5/8" metal studs sistered to existing framing with 1/2" sheathing on exposed side.
  Gauge / stud spec: specs A-90x section 05 40 00 / 09 22 16 and S-801 (nonstructural); if not printed → RFI.
- WOOD (W4, W4.1, W6, W8, SW6; S-600 wood framing) = framing Div. 06 EXCLUDED (never quantified, never RFI).
  Their "INTERIOR SHEATHING" when it is gypsum or cementitious board IS ours → board-only entries in
  `existing_walls[]` (schema below). The same block is used for EXISTING walls that receive new board.
- "INTERIOR SHEATHING" material per face is fixed by A-202 notes G.1-G.13 and H.1-H.3 + A-211 finish plan +
  interior elevations (A-60x, A-611, A-62x): G.1 exposed/painted = 1/2" gyp; G.2 behind wall tile = 1/2" cement
  backer; G.3 FRP on wood studs BOH = 1/2" cement board to 1'-0" AFF + 1/2" CDX plywood above (plywood = wood,
  EXCLUDED); G.4 FRP on metal studs = 1/2" cement board full height to 4" above ceiling; G.5 FRP at play area =
  1/2" gyp; G.6/G.7 behind stainless panels = 1/2" cement board; G.8 behind wallcovering = 1/2" gyp; G.9/G.10/G.12/
  G.13 plywood = EXCLUDED; G.11 cooler/freezer = 1 ft cement board base + 1/2" gyp Level 1 to 6" above ceiling;
  H.1 kitchen tile base = 1/2" cement board to 1'-0"; H.2 non-kitchen tile base = cement board to 5"; H.3 vinyl
  base = gyp. Framing height notes C.1-C.3 (6" above ceiling / to deck at draft-stopping partitions).
  Board keys you may use: "1/2 regular" (1/2" gyp), "1/2 cement board", "5/8 regular", "5/8 type X" (only if a
  rated assembly prints it). Waterproof membrane (Composeal), FRP, stainless panels, plywood, wallcovering, tile,
  paint = other trades → EXCLUDED notes, no RFI.

## Fixed scope rules (estimator standing orders — apply, never ask)
- Wood always EXCLUDED (Div. 06) incl. wood blocking, plywood, sheathing of SW6 exterior walls, wood ceiling joists.
  Only a note: "EXCLUDED - wood framing / blocking (Div. 06), not in scope: <item> <N/SHEET>". Metal-or-wood → metal.
- Trades we do NOT do → EXCLUDED, no RFI: ACT and its grid, insulation, acoustical sealant if not ours, FRP, tile,
  stainless panels, millwork, wallcovering, paint, roofing, MEP, structural steel, prefabricated metal canopies
  (A-104 / A-105 / OMD), walk-in cooler/freezer panels, signage. Fasteners/screws/anchors/PAF = EXCLUDED (0).
- Framed openings for ducts = EXCLUDED always. Existing ceiling demolition with no ceiling type shown =
  EXCLUDED "for lack of information" (0 SF). Accessory blocking with no printed width = 3'-0" x 2 rows; metal only
  (wood blocking excluded).
- DEMOLITION of gypsum board and metal framing IS ours (A-050 keynotes 3, 8, 10, 12, 14, 20, 24, 29…; A-052
  keynotes incl. 3 "menuboard furr down", 10 "gyp bd ceiling & support"). For each demo element: misc_items entry
  {ref "DEMO-nn", familia "demolition - gypsum board and metal framing", qty SF, unit "SF", source N/SHEET + keynote,
  op "L x H x layers = SF"} and a `demo_geom` list entry {id, group, page, polyline [[x,y],...] in pt of A-050/A-052,
  lf, h_ft, h_status, layers, sf, keynote, sheet}. Height of each demolished element searched in ALL sheets
  (sections, elevations, RCP, notes, S sheets) with #0 status before assuming; cross-check demo plan vs new floor plan
  wall by wall. Only gyp/metal parts are ours: if a demolished wall is wood-framed, only its board SF is ours.
- Board, Level 5 and special boards NEVER deduct openings nor base. What is printed is loaded, never asked.
  Never scale a height / spacing that is not printed. Board height on a face comes from a dimension whose two ends
  are edges of the board on THAT face.
- #0 dimensional honesty: every number CONFIRMED (printed dim + sheet) / DERIVED (vector or arithmetic, op written) /
  PENDING. Verify each plan sheet's scale against one printed dimension and write that check in `length_op` of the
  first wall/entry of the sheet.
- Every RFI = options {A: {texto, source N/SHEET, delta}, B: {texto, cita (trade code: ASTM C840 / GA-216 / ASTM C754 /
  AISI S220 / IBC), delta}, C: ""}. Unknowns never stop the work: conservative assumption + RFI.

## Schemas
- Canon keys: exactly the canon schema of `skill/SKILL.md` §4 and `skill/runner/prompts/lectura.md` (read that file:
  its generic rules apply; its sheet names A-410/A-221/… belong to another project — use THIS project's sheets).
- `existing_walls[]` (board-only walls; read the docstring of `_existing_walls` in tools/canon.py):
  {id ("<TYPE>-<n><face/zone suffix>", e.g. "W6-03A-CB"), sheet "A-202" (or the plan sheet you measured on), page,
  keynote (finish note G.x/H.x or demo keynote), path [[x,y],...] straight H/V segments in pt ON THAT SHEET,
  length_ft (= path length / constants.plan_scale_by_sheet[sheet] within 0.05 ft), height_ft (+ in source the chain),
  faces (1 or 2 with the SAME board and height; otherwise separate entries), layers, board (key above), location,
  source (N/SHEET of the type + finish note + height source), decision: "Scope rule R-ALC-01 (user 2026-11-01): gypsum /
  cement board is our scope on any substrate; wood framing Div. 06 excluded"}. Faces with different boards by zone
  (cement board base + gyp above) = two entries (heights split, e.g. 1.0 ft + remainder).
- constants: plan_scale_pt_per_ft {value, source} AND plan_scale_by_sheet {"A-202": {value, source}, ...}.
- ceilings[] for gyp ceilings/soffits from A-221 (+ S-241, sections): board key, area_sf, height, perimeter, source;
  ceiling framing that is wood = EXCLUDED; metal furring/hat channel/suspension printed = ours.
- mep_sweep with the M-/P- sheets listed (ducts crossing walls are EXCLUDED anyway; record count + reason).

## ONE WALL, ONCE
A-201 and A-202 show the same plan: measure each wall ONCE on A-202 (where the tags are); A-201 is for keynotes.
Every inventory tag ends in exactly one wall's/entry's `tag_ids` or in `tags_descartados` [{id, motivo, imagen}].
Untagged walls: new wood walls (hatched per legend) → board-only by the G/H notes; existing walls that receive new
finish/board per A-211 / elevations / demo keynotes → board-only entries; existing walls with no new board → not
counted (note the sheet that proves it).

## Output
Write `<SB>/takeoff_canon_<A|B>.json` and validate: `cd <SB> && python3 validar_canon.py takeoff_canon_<X>.json tools`
→ must print "CANON OK" (fix and rerun until it does). English in every text field. Do NOT generate evidence
images (programs do it from your coordinates); bands/paths must lie on the drawn line. Scratch only in `<SB>/scratch/`.
When finished reply ONLY with a short summary: LF per metal type, board SF per board key (walls / existing_walls /
ceilings), demo SF, RFI count with one line each (id, question, A delta / B delta), discarded tags.
