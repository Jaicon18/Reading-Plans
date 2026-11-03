# Harbor Freight Tools - Loveland, CO — Stages 4-9 brief (calculation, Excel, markups, gates)

Skill (frozen for this run): T=/tmp/claude-0/-home-user-reading-plans/8286ed83-02db-5490-a21c-6cf4b9d790c9/scratchpad/skill/take-off-metal-frame-drywall/tools (v81cf18).
Work dir: W=/tmp/claude-0/-home-user-reading-plans/8286ed83-02db-5490-a21c-6cf4b9d790c9/scratchpad/hf
- Clean PDF: $W/plano/bidset_ORIG_SIN_MARKUPS.pdf (50 p; p1-30 rotation 0, p31-50 rotation 270). SHEET_MAP: $W/SHEET_MAP.json.
- Inventory: $W/inventario/ (types A, B, C, E parsed; D exists on A4.1; tags are single letters → hundreds of
  partition_ambiguo PAnnnn; dispose of every PA not used in a wall's tag_ids BY PROGRAM in `tags_descartados`
  {id, motivo (loose text / note / grid / legend / non-plan sheet, as the inventory says), imagen = its recorte}).
- Final canon after resolution: $W/etapas/4_canon/takeoff_canon.json (+ $W/etapas/3_revision/resolucion.md,
  review_items.json, demo_geom.json, demo_cruce.md).
- Project data: $W/proceso/proyecto_datos.json (goes to Inputs rows, README, PARA_REVISAR).

## TEMPLATE = the last project's chain (same skill line, same deliverables)
Read /home/user/reading-plans/cache_proyectos/cfa_riverpoint/proceso_calc/cadena_rev4.sh, PROCESO_CORRIDA.md,
TOOL_LIMITS_CALC.md and the scripts in scripts_rev4/ (takeoff_json.py, sellar_y_marcar.py, evidencia_rfis.py,
evidencias_reglas.py, imagenes_hoja.py, demo_geom_markups.py, demo_cruce.py, markups_rev2_post.py, verificar_markups.py,
docs_rev4.py). Copy and ADAPT them to this project into $W/scripts/ (no CFA sheet names, numbers or texts may survive:
BE-102). Do not copy CFA corrections_revN / cambios / rfi16 / malla_cb (project specific) unless the same need appears.
Also look at /home/user/reading-plans/cache_proyectos/chuze/PARCHE_RCP_para_v81cf18 for how ceilings get RCP markups
(markups_rcp.py, rcp_polys.json) — this project has gyp ceilings / bulkheads on A2.0 / A5.3 if the canon has them.

## Mandatory chain (every tool through `python3 $T/bitacora.py run …`, stop and FIX at the first rc != 0; never replace
a tool by hand calculation — BE-58; a tool limit is fixed in the tool with its test or documented in TOOL_LIMITS_CALC.md)
test_ciego → arranque → alcances escanear / renglones → inventario_tags → evidencia.py (runner) → canon.py (+ fo_in /
alcance_in) → inventario.py → framed_openings.py → alcance_filtro.py → vigas_sobre_walls.py → sellar (closer) + planmark →
markups_bluebeam.py → markups_demo.py (demo_geom) → markups_rcp.py (if ceilings) → markups verificar → imagenes por hoja →
takeoff.json → plantilla_excel.py validar / armar / verificar → registro entregable → alcances compuerta →
verificar_markups_excel.py (BE-117: every annot TYPE·LF·H·SF·DETAIL·Wall ID = Excel; /Measure = printed SCALE of its
sheet; every sheet with take-off rows has markups, incl. RCP and demo) → reglas.py compuerta → etapas.py → auditoria_entrega.py.
All must end green (REGLAS OK, markups N/N OK) except the back-check step (done by a separate subagent afterwards).

## Fixed format and standing orders (never change)
- Excel = plantilla_excel.py fixed 6 sheets (Inputs, Partition Takeoff, Material Summary, Pending Items, Review Items,
  Scope Checklist); partitions in schedule order A, B, C, D, E (types present only), SUBTOTAL per type, GRAND TOTAL.
  Project data sheet rows in Inputs (R-ALC-09). File: $W/etapas/8_excel/HFT_Loveland_Takeoff_FINAL_rev1.xlsx.
- Fasteners / screws / anchors / PAF = EXCLUDED 0 rows with note. ACT, insulation, acoustical sealant, paint, tile,
  millwork, storefront, doors, MEP, masonry, roofing, wood (Div. 06) = EXCLUDED notes in Scope Checklist, no RFI.
  Ducts framed openings EXCLUDED. FRP: as decided in resolucion.md.
- Two track families on separate rows (standard vs deflection / slip).
- RFIs in Pending Items with options (A) drawings / (B) code / (C) other, delta, conservative value LOADED, swept-sheets list.
- Markups Bluebeam: Subject = type, Page Label = sheet number, Length (/Measure at printed scale), Depth = height,
  Wall Area; contents TYPE·LF·H·SF·DETAIL·Wall ID in English. One PNG per marked sheet, colour by type, legend in
  schedule order, title project / sheet / date.
- Output folder for delivery (create): $W/FINAL/ with Take-off/HFT_Loveland_Takeoff_FINAL_rev1.xlsx,
  Planos marcados/ (HFT_Loveland_markups_rev1.pdf + one PNG per marked sheet), proceso/ (VERIFICACION_MARKUPS, DEMO_CRUCE,
  TOOL_LIMITS_CALC, PROCESO_CORRIDA). The README / PARA_REVISAR / SEGUIMIENTO are written by the orchestrator.
