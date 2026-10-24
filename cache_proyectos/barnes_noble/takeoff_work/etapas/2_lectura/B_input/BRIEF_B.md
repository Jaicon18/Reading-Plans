# Lectura B — brief (independent reading, Stage 2B)

You are an independent reader of a construction bid set (metal frame / drywall take-off). Another reader (A)
measures the same walls; you must NOT see A. FORBIDDEN to open: anything under
`/home/user/Reading-Plans/cache_proyectos/barnes_noble/` EXCEPT `takeoff_work/etapas/1_inventario/` and
`takeoff_work/etapas/2_lectura/B_input/`, and your own output folder `takeoff_work/etapas/2_lectura/B/`.
Do NOT open `2_lectura/A/`, `PARTITIONS_STEP1*.xlsx`, `walls_coords.json`, the PNGs in barnes_noble/, or git history.

PDF (clean copy, no markups): `/tmp/claude-0/-home-user-Reading-Plans/b9c208e2-64c4-5dc6-9d1d-2546bd4c85dc/scratchpad/bidset/bidset_SIN_MARKUPS.pdf`
(69 pages, every page rotation 270). Open it with `python3 -I` + `import pymupdf as fitz`. Text is VECTORIZED
(no extractable text): read dimensions visually from high-DPI crops (200–300 dpi). Geometry IS vector:
use `page.get_drawings()` and convert every point with `fitz.Point(p) * page.rotation_matrix` so all coordinates are
in pt of the DISPLAYED (rotated) page, origin top-left (same as `page.get_pixmap()`; `get_pixmap(clip=Rect)` takes
the displayed coords directly).

Write scripts and scratch images ONLY in your own scratch dir: `/tmp/claude-0/-home-user-Reading-Plans/b9c208e2-64c4-5dc6-9d1d-2546bd4c85dc/scratchpad/lecturaB_<sheet>/`.
Evidence images that your JSON cites go in `takeoff_work/etapas/2_lectura/B/img/` (relative path in the JSON).

## Rules (inviolable)
- #0 dimensional honesty: every length is [CONFIRMED] (printed dimension, cite sheet), [DERIVED] (vector
  measurement or arithmetic of printed dims, write the operation) or [PENDING]. Never eyeball-scale a raster.
- Scale: verify against a printed dimension before trusting vectors (write the check).
- Wall partition rule ("eje" mode): one wall = ONE straight line of one partition type. Collinear contiguous
  segments of the same type = same wall even if crossed by a T or a door. Door / rough opening stays INSIDE the
  wall (wall length runs through doors to the corner / intersection). An L corner, jog or T between two TAGGED
  lines = two walls. An untagged return / jog joins the tagged wall it touches. A closed box (pier) = one wall.
  Exterior walls: one wall per facade / axis; never join two facades. Two tags on the same line = one wall.
- Corner ownership: each corner has ONE owner (one wall runs to the outer face, the other stops at its face).
- Every inventory tag of your sheet must end in a wall's `tag_ids` or in `tags_descartados` with a plan reason
  + image (e.g. a tag pointing to a finish face, not a wall). Never discard "because another task covers it".
- Partition types are the tag text. Thickness from the two vector faces of the wall (`thickness_measured_in`).
- English in every text field of the JSON.

## Output: ONE JSON fragment `takeoff_work/etapas/2_lectura/B/<SHEET>.json`
```
{"walls": [ {
   "id": "B-<SHEET>-<n>",            // unique
   "tag": "<partition type>", "element": "wall", "sheet": "<SHEET>", "page": <1-based pdf page>,
   "tag_ids": ["PT00xx", ...],       // inventory ids (tags_<SHEET>.json) that mark this wall
   "location": "<room / facade, English>",
   "length_ft": <number>, "length_status": "CONFIRMED|DERIVED|PENDING",
   "length_source": "<sheet / detail, e.g. A-101>", "length_op": "<operation or vector method>",
   "band": {"ori": "H"|"V", "c0": <face pt>, "c1": <other face pt>, "lo": <start pt>, "hi": <end pt>},
        // H: c0/c1 = the two face y's, lo/hi = x extent;  V: c0/c1 = face x's, lo/hi = y extent
        // diagonal or curved wall: {"ori": "D", "p0": [x,y], "p1": [x,y], "faces_top": <ft>, "faces_bottom": <ft>}
        //   (length_ft = average of the two face lengths; for an arc give the arc length in length_op)
        // closed box / pier: {"ori": "BOX", "x0":..,"y0":..,"x1":..,"y1":..}
   "thickness_measured_in": <number>,
   "img": "img/<file>.png"           // crop with the wall circled/highlighted, REOPENED and checked
 } ],
 "tags_descartados": [ {"id": "PT00xx", "motivo": "<plan reason>", "imagen": "img/<file>.png"} ]
}
```
Do NOT include a "constants" key. Measure lengths to the nearest 0.01 ft. When finished, reply with a short
summary: number of walls, LF per type, discarded tags, doubts (each with the two alternatives and the LF delta).
