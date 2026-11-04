# CFA #2284 River Point — rev7 detail-bubble chain (reader brief)

Goal: every detail / elevation / section bubble that our take-off sheets point to must be followed to the end of its chain and
end in ONE of two dispositions, with evidence:
- **governs**: the view prints something that sets or checks a quantity of our scope (metal framing Div. 05/09, gypsum board,
  cement board, demo of gyp / metal) for specific canon entries -> list those canon ids and what the view prints for them.
- **no_aplica**: the view shows nothing of our scope for any canon entry -> a motive of at least one full sentence that says
  WHAT the view shows (e.g. "exterior elevation: brick / EIFS / storefront only; SW6 exterior sheathing is wood Div. 06").

Our scope (estimator standing orders, apply, never ask): metal studs / track / furring, gypsum board and 1/2" cement board on
ANY substrate (wood walls W4 / W4.1 / W6 / W8 / SW6 are wood framing EXCLUDED Div. 06 but their gyp / cement board IS ours,
loaded as board-only entries in `existing_walls`), demolition of gyp board and metal framing. NOT ours: wood, plywood / CDX,
FRP, tile, stainless panels, paint, wallcovering, millwork, insulation, ACT, MEP, prefabricated canopies, fasteners.

## Files (read only — do not modify anything outside your own output file)
- Bid set: `/tmp/claude-0/-home-user-reading-plans/00739bfa-f4e4-5132-80c8-c9e8628b8f17/scratchpad/cfa_work/plano/bidset_CLEAN.pdf`
  (172 pages, 3024 x 2160 pt, keeps the AutoCAD SHX text annotations). Page map: `.../scratchpad/cfa_work/proceso/SHEET_MAP.json`
  (page 1-based -> sheet). Open with `python3 -I`, `import pymupdf`. Render crops with `page.get_pixmap(clip=..., dpi=110-150)`
  and LOOK at them with the Read tool; text: `page.get_text('words')` + `page.annots()` content (SHX).
- `cfa_burbujas/markers.json`: each bubble (view "A3/A-601" = view A3 on sheet A-601) with the center of its marker on A-202
  (pt). Interior-elevation markers are diamonds with 4 view labels around one center: the label position (top / right / bottom /
  left of the diamond) = the direction the elevation looks. Find the label words around the center on A-202 (page 13) to know
  which wall each view looks at.
- `cfa_burbujas/canon_walls.json`: every take-off entry (metal `walls` and board-only `existing_walls`) with its A-202 path (pt),
  location, height, board, faces and current source text. `cfa_burbujas/canon_otros.json`: ceilings + misc items.

## Rules (#0 dimensional honesty)
- Never scale. A value is [CONFIRMED] only if printed (quote it, with the view N/SHEET); [DERIVED] with its operation; else say
  "not printed".
- Compare what each view prints (ceiling height, tile / wainscot / cement board base height, FRP extent, board to deck, etc.)
  with the canon entry's height / board. Report every difference as a DELTA with the printed value and its N/SHEET. Do not fix
  anything yourself.
- Follow the chain: list every bubble printed INSIDE each view (e.g. "C3/A-625" inside A1/A-621) and open it too; it gets its
  own disposition (governs / no_aplica) with the same rules.
- Evidence: for every view save one crop PNG in `cfa_burbujas/out/img/<VIEW with / replaced by _>.png` (e.g. `A3_A-601.png`)
  of the view on its sheet with the relevant printed items circled in red (PIL ellipse, width >= 4, pure red (255,0,0)). Reopen
  each PNG with Read to verify it shows the view.
- English in every text field.

## Output
Write `cfa_burbujas/out/<YOUR_GROUP>.json` = list of
`{"view": "A3/A-601", "sheet_page": 24, "looks_at": "room / wall description", "disposition": "governs" | "no_aplica",
  "canon_ids": [...], "printed": ["quote 1 (what it is)", ...], "check": [{"id": "...", "canon": "...", "view_prints": "...",
  "result": "OK" | "DELTA", "note": "..."}], "motivo": "... (only for no_aplica)", "inner_bubbles": ["C3/A-625", ...],
  "img": "out/img/A3_A-601.png"}`
(one object per view, including the inner ones you followed). When done reply with a SHORT summary: views read, governs /
no_aplica counts, and every DELTA in one line each.
