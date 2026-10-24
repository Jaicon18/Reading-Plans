# Run log - Barnes & Noble Colorado Springs take-off (unattended run, 2026-10-24)

## Start
- Skill package take-off-metal-frame-drywall_FINAL_v80d.zip unzipped; `correr_suite.py` 4/4 OK, `test_ciego_tools.py` 0 findings, before reading plans.
- Cache read first: PARTITIONS_STEP1_rev1.xlsx (56 walls, 985.03 LF), walls_coords.json, type images.
- Bid set downloaded once (gdrive_fetch.py), clean copy made with copia_limpia.py (9,864 foreign annotations removed). Every render / vector read uses the clean copy.
- No specification book for Div 05 / 09 beyond A-002; gauges from the A-410 metal stud schedule; fasteners A-410 partition note 8.
- Existing vs new: A-101 construction legend + DM-101 + A-510. Existing CMU (Div 04) is not ours; new furring only.

## Estimator decisions applied (stored as data)
1. Type 2 > 22'-0": 3-5/8" 14 ga SJ @16" + diagonal bracing @32" O.C. to structure (3/A-410) + RFI-04.
2. Cafe south line counted ONCE as E1 / E2 (A-221 governs) - RFI-05.
3. Gyp bd of types 1 / 1A / 1B / 1C excluded (by future tenant) - RFI-01.
4. Acoustical sealant excluded (all projects).
5. Cafe heights: A-225 searched (finish plan, no top of stud) -> RFI-06; loaded to deck per rule 53.3 / 60.11.

## Stages
1. Inventory: inventario_tags.py (A-101 / A-221 text vectorized -> manual sweep: rhombus symbols detected in vector, labels read on contact sheets, 57 tags, every crop re-opened).
2. Reading A: cache normalized to the canon + openings (A-500), faces by room (A-121 ceilings, partition note 3, 2/A-410), heights (A-400A / A-400B), GWB ceilings (subagent, A-121 / A-210 / A-221), column surrounds C25, accessories.
3. Reading B: two independent subagents (A-101, A-221), brief in 2_lectura/B_input/BRIEF_B.md.
4. comparar.py: 33 match, 23 differ, 17 only A, 10 only B, 3 alerts.
5. Resolution with images (3_revision/resolucion.md) -> 4_canon/takeoff_canon.json.
6. Calculation: canon.py, contar_tags.py, vigas_sobre_walls.py (no S sheets), framed_openings.py, alcance_filtro.py - all through bitacora.py.
7-10. Excel (plantilla_excel.py), Bluebeam markups, gates, delivery.

## Conditional notes checked
- "F.R.P. over 5/8" plywood where shelving occurs" (3/A-410, 4/A-410): fixture plan A-111 not dimensioned for the partial walls -> RFI.
- "Restroom / cafe walls only: W.R. gyp on wet side" (2/A-410) and A-410 partition note 7: wet fixtures back onto the exterior EXT-07 (gyp by tenant) -> MR not loaded on our partitions, RFI-11 with delta.
- "Extend gyp to deck in locations with no ceiling" (2/A-410) vs partition note 2 "full height of studs": board to ceiling + 6" where a ceiling exists (detail governs), RFI with the full-height delta.
- Control / expansion joints: none drawn in partitions or GWB ceilings.

## Package errors found and fixed in this run (tools_v80e, same turn)
| # | Tool | Error | Fix (rule) |
|---|---|---|---|
| 1 | canon.py | no stud family for 8" studs (type 1B) -> ValueError | 8" stud family, optional (v80e) |
| 2 | canon.py | cement board / 1/2" exterior gyp sheathing could not be wall faces | BOARD_FAM entries (v80e) |
| 3 | canon.py | door with no header schedule had no "0 + RFI" path (R71.10 not expressible) | header "not_called" with header_source + header_rfi |
| 4 | canon / accesorios / framed_openings | sheet regex `S\d`, `M\d`, `P\d`, `E\d` rejected "M-102" | optional hyphen |
| 5 | reglas, chequeos_v71/72/73/76, markups, contar_tags, plantilla | sheet regex demanded a decimal (A12.01): "A-101", "2/A-410" never matched | 3-digit sheet numbers accepted |
| 6 | particion, partition_types, etapas, esquinas, inventario, comparar, chequeos_v72/77 | one scale for the whole canon (A-101 1/8" vs A-221 1/2") | constants.plan_scale_by_sheet + criterios.escala_hoja (R80.1) |
| 7 | comparar.py | types upper-cased (H2A) vs inventory (H2a) -> false alerts | compare normalized types |
| 8 | partition_types.py | column wrap without partition tag became a type "" | OTHER FRAMING |
| 9 | vigas_sobre_walls.py | set without S sheets could not run | `NONE` = no structural sheet, empty result with reason |
| 10 | reglas.py A_MEP_SWEEP vs mep.py | mep.py says "registration < 25 -> sheet not used, declare it"; gate failed with no way to declare | `registro.no_usable {motivo, source, img}` |
| 11 | esquinas.py vs chequeos_v75 R75.7 | R75.7 extends short returns to the outer face; R70.2 then flags the corner as double | corners_ok with reason (both rules kept; inconsistency reported) |
| 12 | plantilla_excel.py | no SUBTOTAL per type / schedule order (§0.F inviolable) | SUBTOTAL row per type, GRAND TOTAL = sum of subtotals, `type_order` |
| 13 | indice_set.py / inventario_tags.py | vectorized text: 0 sheets / 0 tags | manual sweep with images (declared) |

## Verification
- Reading B independent; completeness critic subagent (5_auditoria/AUDIT_COMPLETENESS.md).
- Marked images re-opened and checked against the Excel before delivery; Bluebeam markups verified with markups_bluebeam.py verificar.
- Final message written to a file and checked with verif_respuesta.py.
