# COMMON BRIEF — Xfinity Interquest, 1333 Interquest Pkwy Lot 11, Colorado Springs CO 80921 (metal frame & drywall take-off)
GC: BCI National. Architect: Robert F. Vanney. 1,798 SF tenant improvement, 1 story, IBC 2021, Type V-B sprinklered (A0.1).

## Inputs
- PDF (clean copy, 17 pages; keep AutoCAD SHX annotations = drawing text): /root/xf/work/plans/bidset_SIN_MARKUPS.pdf
  Python: `python3 -I -W ignore`, `import fitz` (PyMuPDF), PIL, numpy, opencv available.
- Every page has rotation 270. COORDINATES = VISIBLE frame (page.rect after rotation, 3024 x 2160 pt, origin top-left,
  same as a rendered PNG). fitz get_text() words are in UNROTATED space: convert with `fitz.Rect(w[:4]) * page.rotation_matrix`.
  Render clips with page.get_pixmap(dpi=..., clip=VISIBLE-frame rect) — PyMuPDF takes the clip in visible pt
  (verified 10-nov, BE-XF02); never multiply by derotation_matrix. Check every crop by re-opening it.
- Sheet -> page (1-based): A0.1 title/code p1, A0.2 ADA details p2, A0.3 SPECIFICATIONS p3, A1.0 demolition plan p4,
  A2.0 partition plan + door schedule + wall types 2/A2.0 + stud limiting heights table + details 3..8/A2.0 p5,
  A3.0 RCP + details p6, A4.0 p7, A5.0 p8, E0.0 p9, E1.0 p10, E2.0 p11, E2.1 p12, E3.0 p13, M0.0 p14, M1.0 p15,
  M2.0 p16, P1.0 p17. Pages 9-17 carry their text as "AutoCAD SHX Text" annotations (page.annots(), info['content']).
- Inventory by script: /root/xf/work/etapas/1_inventario/inventario.json (+ inventario.md, recortes/). Wall tags W1..W4
  are in `ocurrencias.partition_candidato` (ids PC00nn) because the script did not read the wall-type legend.
  Detail bubbles: `ocurrencias.detail_bubble` (DB00nn). Full text by sheet: /root/xf/work/set_texto.json.
- Printed scale: read it for EVERY view you measure (A1.0 / A2.0 / A3.0 plans are 1/4"=1'-0" = 18 pt/ft — verify against
  a printed dimension in vector, e.g. a long dimension string, and write the check).
- FORMAT examples from ANOTHER project are in /root/xf/work/ref/EJEMPLO_FORMATO_*.json. Copy only the STRUCTURE/keys,
  never any value, number, sheet or wording from them.

## Our scope (mandatory standing rules of the estimator)
- Ours: cold-formed metal framing (studs, track, slip/deflection track, headers, bracing, metal blocking/backing,
  clips) and gypsum board (board, trims/beads, taping/finishing, control joints), gypsum board ceilings/soffits and their
  framing, demolition of gypsum board / metal framing (demolition = SF of the element only: wall LF x H, ceiling area;
  never layers).
- EXCLUDED, no RFI: acoustical ceilings (ACT) and grid/seismic (other bid package), painting, insulation, wood / F.R.T.
  wood blocking / plywood (Div. 06), all screws/anchors/shot pins/fasteners, acoustical sealant, MEP, duct openings,
  doors/frames/hardware, storefront, millwork, flooring, signage. Areas marked N.I.C. (e.g. LANDLORD ROOM) are not ours
  (record them as excluded with the printed reason and sheet).
- Existing construction to remain = not counted unless the plans call new board/furring/repair on it (cite the note).
- BOTH SIDES: if a wall type puts board on both faces, every wall of that type gets two faces with the type's layers.
- One wall = one straight line of one type (never two axes or facades in one number).
- Plans first, then specs (A0.3), then code with exact section (IBC 2021 / ASTM C754 / C840 / GA-216 / AISI S220);
  only if neither plans nor code resolve it -> open question with what was searched (all sheets, SHX text, synonyms).
- Deck with two printed heights and break not drawn = the higher one. Level of finish not printed = Level 4.

## Honesty #0 (mandatory)
Every number has a status: "CONFIRMADO" (printed dimension, cite N/SHEET and the printed text), "DERIVADO" (operation
written in *_op, e.g. sum of printed dims or vector measurement at the PRINTED scale "(x1-x0)/18 = 12.35"), or
"PENDIENTE" (not printed, not measurable). Never estimate by eye. Lengths along the wall line between faces of the
walls it meets.

## Evidence
Every claim gets a PNG crop with the item circled in red, re-opened and checked; path recorded in the JSON (`img`,
`height_img`). Save crops under your own output folder.
Output in ENGLISH. Write results to disk progressively. Do not compute materials. Do not open other readers' folders
(/root/xf/work/etapas/2_lectura/*, /root/xf/work/indep, /root/xf/work/burbujas other than your own).
