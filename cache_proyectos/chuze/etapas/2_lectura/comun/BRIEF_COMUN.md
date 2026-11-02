# Chuze Fitness Austin Bluffs — Stage 2 reading brief (common to readers A and B)

Project: Chuze Fitness Austin Bluffs, 3630 Austin Bluffs Pkwy Unit #C190, Colorado Springs CO. Tenant improvement of a
fitness club inside an existing retail building (IEBC Level 3 alteration). Our scope = cold-formed metal framing (Div. 05
40 / 09 22) and gypsum board (Div. 09 29) ONLY.

## Inputs (read-only)
- Clean PDF (no markups, 106 pages, rotation 0, 3024 x 2160 pt): `/tmp/chuze/plano/bidset_SIN_MARKUPS.pdf`
  Open with `python3 -I` and `import pymupdf as fitz`. Text IS extractable (`page.get_text('words')`) and geometry IS vector
  (`page.get_drawings()`); coordinates in pt, origin top-left, same as `page.get_pixmap()`.
- Sheet map: `/tmp/chuze/proceso/SHEET_MAP.md` · S-sheet classification: `/tmp/chuze/proceso/S_CLASIFICACION.md`
- Stage-1 inventory (by script): `/tmp/chuze/work/etapas/1_inventario/inventario.json` and `inventario.md`
  (every partition tag `PTnnnn` with sheet, page and bbox; circled crops in `recortes/`).
- Plan constants (scales per sheet): `/tmp/chuze/work/etapas/2_lectura/comun/constants.json`
- Skill (rules): `/tmp/chuze/skill/take-off-metal-frame-drywall/SKILL.md` — sections 0 (estimator criteria), 1, 4, 5, 7,
  13 (PT1–PT8, wall partition "eje"), and the v80v rules R80e.91–R80e.95 in runner/prompts/lectura.md.
- Specs (Project Manual): `/tmp/chuze/plano/specs.pdf` (Div. 05 40 00, 09 21 16 / 09 22 16 / 09 29 00 when needed).

## Fixed scope rules (estimator standing orders — apply, never ask)
- WOOD is always EXCLUDED (Div. 06): wood blocking, FRT plywood, plywood backing, PT wood, nailers. Never quantify them;
  list them only as `"EXCLUDED - wood ... (Div. 06): <item> <N/SHEET>"` notes. If a detail offers metal or wood, take metal.
  (Exception: A101 keynotes A1.11 / A1.13 / A1.14 replace GYP BD with FRT plywood to 24" AFF — record the zone so the board
  below 24" is NOT counted on that face; the plywood itself is EXCLUDED.)
- Trades we do NOT do → EXCLUDED directly, no RFI: ACT, insulation, acoustical sealant, FRP, tile, millwork, structural
  steel / HSS / misc. metals / joist reinforcement, concrete, roofing, MEP.
- Board, Level 5 and special boards NEVER deduct openings (doors, windows, storefront) nor base (R80e.92).
- Demolition plans AD101 / AD102 / AD103 are MANDATORY: every wall is NEW or EXISTING; existing walls to remain are not
  quantified (note them with the demo sheet that proves it). AD note 5: exterior wall furring is removed to CMU —
  check what new furring (type B2E) replaces it.
- A111 general note: locker rooms, restrooms and pool areas = moisture resistant gyp board (and A301 type details: 5/8"
  cement backer board behind all tile, 5/8" MR gyp at all wet rooms, DensArmor Plus at pool / spa rooms) — record per face.
- What is printed is loaded, never asked (R80e.93). Never scale a dimension that is not printed for a decision (R80e.91).
- #0 dimensional honesty: every number [CONFIRMED] printed dimension + sheet, [DERIVED] vector or arithmetic with the
  operation written, or [PENDING]. Verify the sheet scale against one printed dimension before trusting vectors and
  write that check in `length_op` of the first wall of the sheet.

## ONE WALL, ONCE (identical rule for A and B)
- A wall drawn on an ENLARGED plan (A421, A422, A423, A424, A425, A426, A427, A428, A429, A431, A432, A434, A435) is
  measured on that enlarged sheet (sheet = that enlarged sheet).
- A wall that appears on two enlarged plans belongs to the sheet where its TAG sits; tagged on both → the lower sheet
  number owns it; the other sheet puts its tag ids in `tags_descartados` with motivo "same wall as <sheet> (counted there)".
- A101 (overall) measures ONLY the walls that are on no enlarged plan. Every A101 tag of a wall that is on an enlarged
  plan goes to `tags_descartados` with motivo "shown on enlarged plan <sheet> (counted there)" + image.
- Partition rule "eje" (SKILL §13 PT2 / E28): one wall = ONE straight line of one type; collinear contiguous segments of
  the same type = same wall even through doors and T's; an L corner / jog / T between two TAGGED lines = two walls;
  an untagged return joins the tagged wall it touches; a group with no tag at all = one wall (type from the plan note /
  default or `untagged_reason`). Wall length runs THROUGH doors. Each corner has ONE owner.
- Partial height walls (A101 legend "NEW PARTIAL HEIGHT INTERIOR MTL STUD FRAMING"; S200 A/B/C) are walls too
  (record `height_ft` from the plan note "T.O. WALL @ ..." with its sheet).

## Output
One JSON fragment per task in YOUR folder only (A: `/tmp/chuze/work/etapas/2_lectura/A/`, B: `.../2_lectura/B/`), file
name given in your task. Evidence images your JSON cites go in `<your folder>/img/` (relative path `img/<file>.png`):
crop with the wall band highlighted, REOPENED and checked (look at it with the Read tool). Scratch scripts only in
`/tmp/chuze/scratch/<your task id>/`.
Before you finish run: `python3 /tmp/chuze/work/etapas/2_lectura/comun/validar_fragmento.py <your fragment>` →
must print `UNIR OK`. Fix and rerun until it does. English in every text field. Do NOT include a "constants" key.

Wall object (minimum; reader A adds more, see its brief):
```
{"id": "<A|B>-<SHEET>-<n>", "tag": "<type>", "element": "wall", "sheet": "<SHEET>", "page": <1-based>,
 "tag_ids": ["PTnnnn", ...], "location": "<room / area>",
 "new_or_existing": "NEW", "demo_source": "AD101 ...",
 "length_ft": <0.01>, "length_status": "CONFIRMED|DERIVED|PENDING", "length_source": "<sheet>", "length_op": "<op>",
 "length_basis": "face to face" | "centerline / axis",
 "band": {"ori": "H"|"V", "c0": <face pt>, "c1": <face pt>, "lo": <pt>, "hi": <pt>, "sheet": "<SHEET>"},
     // H: c0/c1 = y of the two faces, lo/hi = x extent; V: c0/c1 = x of faces, lo/hi = y extent
     // diagonal / curved: {"ori": "D", "p0": [x,y], "p1": [x,y], "faces_top": [[x,y],[x,y]], "faces_bottom": [[x,y],[x,y]], "sheet": ..}
     // closed box / pier: {"ori": "BOX", "c0": x0, "c1": x1, "lo": y0, "hi": y1, "sheet": ..}
 "thickness_measured_in": <number>, "img": "img/<file>.png"}
```
`tags_descartados`: `[{"id": "PTnnnn", "motivo": "<plan reason>", "imagen": "img/<file>.png"}]`. Every inventory tag of your
sheets ends in exactly one wall's `tag_ids` or in `tags_descartados`. Never discard "because another task covers it"
except with the ONE WALL, ONCE motivo above.

When finished reply with: walls count, LF per type, discarded tags (id + reason), and doubts — each doubt with its two
alternatives and the LF delta (these become RFIs at the end; do NOT stop to ask).
