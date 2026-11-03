# CAMBIOS tools v81cf11 (03-nov-2026, CFA #2284 River Point rev4)

| Id | Tool | Problem | Fix | Test |
|---|---|---|---|---|
| BE-117 | markups_bluebeam.py `contenido` / `board_sf` (verificar uses the same function) | The SF in each wall markup was LF x H (framing area) and did not equal the Board (SF) of its Excel row | SF = sum of the wall faces (length x height x layers) - openings, written "X SF board"; walls without faces keep LF x H | `test_markups_board_sf.py` (fails with v81cf10 as delivered) |
| BE-117b | markups_bluebeam.py `contenido` (board-only walls) | board-only SF written with 1 decimal (16.1) vs the Excel 16.14 | 2 decimals, identical to the Excel row (test_existing_walls.py updated: 300.00 SF) | `test_existing_walls.py` |
| BE-117c | canon.py TRACK_NOMBRES["slip"] / track_by_element | The slip / deflection top track row always said "2\" deflection leg" even when the head detail prints a 3" long-legged slotted track | leg from walls[].top_track_leg or parsed from top_track_kind_source ("3\" LONG LEGGED"); default 2" | `test_slip_leg_label.py` |
| BE-117d | trazabilidad.py `aplicar` (N/SHEET of every Material Summary row) | A row with any N/SHEET dropped the bare sheets of its items (gyp ceiling row cited C3/S-241, A2/S-241 but not A-221 where the ceilings are drawn): verificar_markups_excel found DETAIL A-221 not in the row | the bare sheets of the item sources not covered by an N/SHEET are added (same rule as the per-product split) | `test_be117_excel_ids.py` |
| BE-117e | accesorios.py `level5` | op "<ref>: L x (h - base) = SF": the markup checker read <ref> = L (59.69) instead of the SF | op "<ref> <SF> SF = L x (h - base)" | `test_be117_excel_ids.py` |
| BE-117f | trazabilidad.py board rows | 1/2" regular board row had no per-ID breakdown (op text cut at 566 chars), so soffit bottoms / walls of that board could not be matched; ceilings were named "ceiling <room>" | 1/2" gyp board joins the per-board branch (faces + ceilings + items); a ceiling with `id` is listed by its id | `test_be117_excel_ids.py` |


# CAMBIOS tools v81cf13 (03-nov-2026, merge of Chuze FINAL4 patch PARCHE_BE117g_para_v81cf13) — generic, all projects

On top of v81cf12 (BE-115: one cumulative line). Chuze-branch ids R80f.7–R80f.10 renumbered to R80f.8–R80f.11 (R80f.7 = A_MARKUPS_EXCEL in the main line). Chuze files were merged as 3-way diffs (base v81cf10 archive, ours v81cf12); BE-117b–f kept (markup SF = board SF from the canon faces, 2 decimals).

| Id | Tool | Problem | Fix | Test |
|---|---|---|---|---|
| BE-117g | verificar_markups_excel.py `leer_excel` / union | A joined Partition Takeoff row "A+B" (PT2: wall + return): each piece was looked up alone (row "without annotation", TYPE vs a Material Summary row, duplicate Wall ID) — Chuze FINAL4 16 FAIL | `union` {piece -> row}; each piece checked for TYPE / H against its row; LF / SF of the pieces summed and squared against the row (±0.5 %); pieces are not duplicates | `test_markups_excel_union.py` |
| R80f.8 | plantilla_excel.py `verificar_excel`; markups_bluebeam.py `resumen_vigente` | language check failed on a quoted proper name in the R80e.121 "PROJECT DATA" block; with two summaries of the same canon the oldest was verified | exemption for any "PROJECT DATA" block; most recent summary verified | `test_chuze_r80f8_11.py` |
| R80f.9 | markups_bluebeam.py `ajustar_a_lf`, `cargar_board`, `NHOJA_RX` | Bluebeam Length vs printed LF up to 1 %; DETAIL "3D/A301" for A2-3D/A301 | run with diff < TOL_PT drawn at LF length; board_out.json SF only for walls without faces (BE-117b first); hyphenated types whole | `test_chuze_r80f8_11.py` |
| R80f.10 | markups_bluebeam.py `leyendas_por_hoja`, `orden_types` | legend only on a last page | legend box on every marked sheet in schedule order | `test_chuze_r80f8_11.py` |
| R80f.11 | auditoria_entrega.py (new) | delivery audit by eye | delivery audit by program, rc 1 = not deliverable | `test_chuze_r80f8_11.py` |


# CAMBIOS tools v81cf18 (03-nov-2026, Chuze Fitness Austin Bluffs FINAL5) — generic, all projects

On top of v81cf17 (BE-115). Origin: Chuze FINAL5 (RCP ceilings with no markups; orchestrator decision #0: drawn geometry wins over hatch-stroke extents).

| Id | Tool | Problem | Fix | Test (fails with v81cf17) |
|---|---|---|---|---|
| R80f.13 | markups_rcp.py `escribir`, `_pagina`, `_bracing_on`, `_label` | One RCP sheet per project (constants.rcp_sheet): a set with ceilings / soffits on several enlarged RCP sheets (Chuze: A421.A ... A426) got no ceiling markups; ID = room text; lateral-bracing clusters drawn even when the set has none; project-specific legend text (J/A12.02); legend at a fixed corner | every ceiling on ITS sheet (ceilings[].sheet, else rcp_sheet; page by Page Label, title block or rcp_page); polygon found by ceilings[].id or room; NM / ID = id; Contents carries "GWB CEILING <ceiling_tag>"; clusters only unless constants.ceiling_lateral_bracing = false; legend per sheet in the corner with the least ink; one PNG per sheet (<sheet>_rcp_markups.png) | `test_rcp_multihoja.py` |
| R80f.14 | verificar_markups_excel.py `buscar_pdf` | The delivery PDF next to the Excel was looked up with the case-sensitive glob "*markup*": "Proj_Markups_X.pdf" was missed and the older walls-only PDF of 6_markups was verified (A_MARKUPS_EXCEL false failures) | any PDF next to the Excel whose name contains "markup" (case-insensitive) | `test_rcp_multihoja.py` |
| R80f.15 | auditoria_entrega.py | Area annotations (RCP polygons) were reported as "annot without Partition Takeoff row"; ceiling sheets were not in the marked-sheets check | an area annot is squared against the "ID SF" breakdown of the Material Summary and its drawn area vs SF (<= 0.5 %); ceilings[].sheet counted as sheets with elements | `test_rcp_multihoja.py` |
| R80f.16 | markups_rcp.py `sin_hatch`, `_color_hatch` | Rule (Chuze FINAL5 audit): the GWB ceiling = the HATCHED area only, bounded by the faces. A ceiling polygon taken from the room region included parts with no C-5 hatch (white display boxes of the storefront soffit, the corner beyond an L-shaped wall in the shower) | every ceiling polygon is checked against the hatch strokes of its sheet (constants.rcp_hatch_color or the commonest thin stroke color): a part without hatch that touches the polygon boundary (>= 1 SF) is reported and markups_rcp exits rc 1 (polygon must follow the hatch boundary; a closed white sub-region without hatch is a hole); a small interior hole (< 4 SF, device / fan) is an opening and is not deducted; `hatch_check_cause` / polygon `cause` documents an exception | `test_rcp_hatch.py` |
