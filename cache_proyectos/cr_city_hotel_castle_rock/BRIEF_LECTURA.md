# READING BRIEF — CR City Hotel, 415 Perry St, Castle Rock CO (metal frame & drywall take-off)

You are an INDEPENDENT plan reader (reading {LECTOR} of floor {PISO}). Another reader does the same floor without
seeing your work; never look for or open any other reader's files (/root/cr/work/etapas/2_lectura/* other than your
own output). You only READ and MEASURE; programs calculate materials later. Output in ENGLISH.

## Inputs
- PDF: /root/cr/work/plans/bidset_SIN_MARKUPS.pdf (148 pages, clean copy). Python: `python3 -I -W ignore`, `import fitz`.
- Inventory (partition tags found by script, ids PTnnnn, with page/bbox): /root/cr/work/etapas/1_inventario/inventario.json
  (key `ocurrencias.partition_tag`, plus `partition_ambiguo` / `partition_candidato`) and inventario.md.
- Independent schedule reading (types, layers per face by rating): /root/cr/work/indep/fichas.json (+ NOTAS.md).
  Type ids normalized as "<type>-<rating>": W.6-1, W.62-1, DW.4-1, FW.4-0, FI.6-0, CH.6-2, XW.6.3-2, CM.8-0 ...
  On the plans the tag prints as two tokens "W.62" + "1" (type, then fire rating digit) inside the symbol.
- Sheet → page map (1-based): A2.01 LVL1 p17, A2.02 LVL2 p18, A2.03 LVL3 p19, A2.04 LVL4 p20, A2.05 roof p21,
  A3.01..A3.04 RCP LVL1..4 p22..25, A4.00..A4.05 elevations/building sections p26..31, A5.00..A5.08 wall sections
  p32..40, A6.00 elevator p41, A6.01 lobby stair p42, A6.02 SE stair p43, A7.00 enlarged unit types 1-3 p44,
  A7.05 units 4-6 p49, A7.09 units 7-9 p53, A7.13 units 10-11 p57, A7.16 units 12-13 p60, A7.19 finish schedules p63,
  A7.20-A7.22 corridor elevations p64-66, A7.23-A7.24 corridor RCP p67-68, A7.30 lobby plans p69, A7.31 lobby RCP p70,
  A7.32/A7.33 lobby details p71-72, A7.45 kitchen/utility/trash p75, A7.50 L4 restroom + L1 staff p76, A7.55 L4 F&B p77,
  A8.00 doors p78, A9.01-A9.06 details p81-86, A0.06 interior assemblies p10, A0.07 exterior p11, A0.08 horizontal p12,
  A0.09-A0.11 rated intersections p13-15, S-sheets p87-112. Pages 45-48, 50-52, 54-56, 58-59, 61-63, 73-74 have NO
  extractable text (vector/raster): render them (get_pixmap clip, dpi 150-200) and read visually.
- Scale: read the printed scale of EVERY view you measure (A2.0x = 1/8"=1'-0" = 9 pt/ft; enlarged plans usually
  1/4"=1'-0" = 18 pt/ft — verify each view title). Coordinates = visible page pt (page.rect, rotation 0).

## Scope rules (mandatory)
- Interior types W / FW / DW / FI are WOOD framed: we take off ONLY the gypsum board (faces + layers); wood framing,
  plywood, blocking, nailers = EXCLUDED (Div. 06). Record `framing: "wood"`. CH (C-H shaft wall) = metal studs +
  J runner + 1" shaftliner + board: record `framing: "metal"`. C (CIP concrete) and CM (CMU) walls: no framing or
  board by us UNLESS a furring/finish type (FI / FW) is drawn on them — record those as their own walls.
- Exterior XW types: record the INTERIOR face board (and exterior gyp sheathing layers if the type prints them);
  wood studs / LP Flameblock / siding = excluded. Never join two facades or two grid lines in one wall (one wall per
  straight line / facade / grid segment).
- BOTH SIDES: if the type (fichas.json) has board on two faces, the wall gets TWO faces with the layers of the type
  for its rating. Layers depend on rating (1 HR = 1 layer, 2 HR = 2 layers per face for W / CH ...; W.62-1 = 2 layers
  each side). A tag with no rating digit = say so.
- "GREY TONED AREA IS UNDER A SEPARATE PERMIT AND NOT IN SCOPE": walls inside the grey area are NOT counted (list
  them in `excluded_areas` with the crop).
- Untagged walls: a wall drawn with no tag on the floor plan takes its type from the ENLARGED plan of that area
  (A7.xx / A6.xx) or from the nearest typical note; write `type_source` with N/SHEET. If no sheet types it, put
  `type: null` + `type_note` (we will RFI it). Never invent a type.
- Every tag occurrence of the inventory on your sheets ends in a wall (`tag_ids`) or in `tags_descartados`
  [{id, motivo, imagen}] (legend instance, duplicate, other floor, out of scope...).

## Honesty #0 (mandatory)
Every number: `*_status` = "CONFIRMADO" (printed dimension; cite N/SHEET and the dimension text),
"DERIVADO" (operation shown in `*_op`, e.g. sum of printed dims, or vector measurement at the PRINTED scale:
"(x1-x0)/9 = 23.42"), or "PENDIENTE" (not printed and not measurable). Never estimate by eye. Lengths are along the
wall centerline between the faces of the walls it meets (dimension strings are to face of stud, note 1 on A2.0x).

## Heights (per face, per floor)
Board height of each face = from floor to where the board stops, from a PRINTED source: building/wall sections
(A4.03-A4.05, A5.xx), level datums (LEVEL 1 6197.75' etc. on elevations/sections), RCP ceiling heights (A3.0x,
A7.xx RCP), notes ("TO UNDERSIDE OF STRUCTURE", A0.06 GN 4/21 rated walls to deck/sheathing above). Cite N/SHEET. Wall
height = floor to underside of structure above unless a section shows otherwise. A deck with two printed heights and
the break not drawn = take the HIGHER (rule U-146).

## Ceilings / soffits (reader A only)
For each room / area of your floor: ceiling assembly (FS-1 under floors above, RS-x under roof, MB-1, ACT, open),
board type + layers, framing (resilient channel = metal, ours; wood joists = excluded; metal furring / C-channel /
J-track = ours), ceiling height, area in SF (printed room SF from the plan is CONFIRMADO; else DERIVADO from the room
polygon at printed scale), soffits / bulkheads (LF, height, faces) from RCP and enlarged RCP with N/SHEET.
Also: shaft walls (CH) at elevator / stairs / chases of your floor from A6.xx; door frames double-stud notes
(wood = excluded); control joints if drawn; wet areas (water-resistant board per A0.06 GN 11 / floor plan note 4:
toilet / lavatory, janitor, shower, exterior, parking) — mark faces that need moisture-resistant board; tile areas
(cement board per GN 13) from enlarged unit plans / elevations; FRP; corner bead not needed (program).

## Detail bubbles
Every detail / section bubble on your sheets (N/SHEET) that touches a wall or ceiling you record: follow it to its
destination sheet, and inside that detail follow any further bubble, to the end. Put in each wall/ceiling `detail`
the governing N/SHEET list and in `details` a list [{ref "N/SHEET", from_sheet, applies_to, what_it_says (short),
img}] . Bubbles not related to our trade: list with motivo in `details_no_aplican`.

## Evidence
For every wall: a PNG crop with the wall circled in red (fitz: page.draw_circle / shape, or PIL), re-opened and
checked, path in `img`. Height evidence crop in `height_img`. Save crops under your own folder.

## Output (write to disk BEFORE finishing; save partial progress as you go)
Folder: /root/cr/work/etapas/2_lectura/{LECTOR}/ ; file {PISO}.json :
{
 "reader": "{LECTOR}", "floor": "{PISO}", "sheets_read": [...],
 "scale": [{"sheet", "view", "printed", "pt_per_ft"}],
 "levels": [{"name", "elev", "source"}],
 "walls": [{"id": "<type>-<floor>-<nn>", "type": "W.62", "rating": "1", "type_id": "W.62-1", "type_source",
   "framing": "wood|metal", "tag_ids": ["PT...."], "sheet", "page", "location" (rooms on each side / grid),
   "band": {"ori": "H|V", "c0", "c1", "lo", "hi", "sheet"},
   "length_ft", "length_source", "length_op", "length_status",
   "height_ft", "height_source", "height_status",
   "faces": [{"side": "A|B", "room", "layers", "board", "height_ft", "height_source", "wet": bool, "tile": bool}],
   "exterior": bool, "detail": "N/SHEET list", "img", "height_img", "notes"}],
 "ceilings": [...], "soffits": [...], "shaft_walls_note", "details": [...], "details_no_aplican": [...],
 "tags_descartados": [...], "excluded_areas": [...], "open_questions": [{item, sheet, what is missing, sheets and
   terms already searched}]
}
Final message to the orchestrator: under 150 words (counts of walls by type, LF by type, ceilings SF, open questions).
Do not compute materials. Do not read any other reader's output.
