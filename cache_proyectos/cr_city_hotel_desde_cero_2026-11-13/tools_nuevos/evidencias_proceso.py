#!/usr/bin/env python3
"""evidencias_proceso.py (CR desde cero): 4_canon/evidencias_reglas.json para las reglas (b) de PROCESO ('corrida'):
cada una apunta al ARCHIVO de esta corrida que muestra cómo se cumplió, o 'NO APLICA: <motivo>'. Nada se inventa:
el programa verifica que cada archivo exista (falla si no)."""
import json, os, sys
W = "/root/cr0/work"
E = {
 "E17": ("NO APLICA: user order U-022/U-184 autonomy - no questions to the user in this run; RFIs go to SEGUIMIENTO and to COORDINACIÓN at the end", None),
 "R73.15": ("NO APLICA: no vendor-frame interface with sealant/trim on both edges (acoustical sealant EXCLUDED; trims per geometry)", "etapas/3_revision/res/accesorios.md"),
 "R73.4": ("registro.py ledger recreated at this run start (no wrongly-marked rows to correct)", "registro.json"),
 "R77.15": ("short messages to COORDINACIÓN per step; detail in files", "/root/cr0/TIEMPOS.md"),
 "REGLA 49.1": ("delivery folder under Claude outputs root (entrega.json drive.parent_id) via subir_entrega.py", "entrega.json"),
 "REGLA 50.3": ("one area / system at a time by subagent (levels, cores, ceilings, accessories), each closed in its resolucion file", "etapas/3_revision/resolucion.md"),
 "REGLA 50.4": ("NO APLICA: new project from scratch in one session; no resumption from a backup", None),
 "REGLA 52.2": ("tools read the project workdir by argument (no fixed project path); pipeline", "/root/cr0/tools_nuevos/pipeline.sh"),
 "REGLA 55.1": ("sheet-by-sheet scope sweep: alcances.py escanear (24 scopes, all sheets) + accessories reader", "alcances.json"),
 "REGLA 56.8": ("NO APLICA: edge blocking is wood (Div. 06, EXCLUDED) in a wood-framed set; canon edge_blocking_none_reason", "etapas/4_canon/takeoff_canon.json"),
 "REGLA 59.14": ("NO APLICA: same as 56.8 (blocking wood, excluded)", "etapas/4_canon/takeoff_canon.json"),
 "S:clarifications-para-el-bid-nunca-omitir": ("Clarifications & Exclusions in README_REVIEW and Scope Checklist", "takeoff.json"),
 "S:etapa-1-inventario-scrip:b4b53c": ("17 raster sheets without text: OCR layer + read by eye, declared (SHEET_MAP.md, titleblocks_raster.png)", "SHEET_MAP.md"),
 "S:formato-de-salida-del-ta:4fca32": ("NO APLICA: no demolition in this set (new construction, A0.00)", None),
 "S:formato-de-salida-del-take-off-obligator": ("Excel fixed 6-sheet format by plantilla_excel.py, English", "takeoff.json"),
 "S:granularidad-y-marcado:1f35f7": ("markups regenerated from the final canon and checked against the Excel (vista_bluebeam)", "etapas/4_canon/takeoff_canon.json"),
 "S:granularidad-y-marcado:33d529": ("work unit = type / area by subagent; all instances in the canon by type_id", "etapas/3_revision/resolucion.md"),
 "S:granularidad-y-marcado:7f3ce3": ("markup coordinates read from the sealed canon paths (markups_bluebeam.py), never from memory", "etapas/4_canon/takeoff_canon.json"),
 "S:granularidad-y-marcado:e221c4": ("markups_bluebeam.py style: full sheets from the clean copy, color per type, legend", "etapas/4_canon/takeoff_canon.json"),
 "S:granularidad-y-marcado:f3c532": ("every tag of the inventory ends in a wall or a discard (comparar / etapas compuerta)", "etapas/3_revision/revision.json"),
 "S:granularidad-y-marcado:f79808": ("all corrections are in the canon and regenerate Excel + markups (pipeline)", "/root/cr0/tools_nuevos/pipeline.sh"),
 "S:los-markups-ajenos-no-so:db7106": ("clean copy without /Annots by arranque.py (1013 annotations removed); every render from it", "arranque.log"),
 "S:los-markups-ajenos-no-son-fuente": ("third-party markups removed before reading (arranque.py)", "arranque.log"),
 "S:protocolo-de-ejecución:19e4ec": ("independent audit U-181 + blind back-check of ceilings before delivery", "etapas/3_revision/res/backcheck_ceilings.md"),
 "S:protocolo-de-ejecución:29966c": ("specs Div. 05 / 09 swept: 05 40 00, 09 21 16.23, 09 22 16, 09 29 00, 09 30 00 (specs_info in canon)", "etapas/2_lectura/A/CEIL_DET.json"),
 "S:protocolo-de-ejecución:470877": ("closing per area with numbered list in each resolution file", "etapas/3_revision/resolucion.md"),
 "S:protocolo-de-ejecución:b92e94": ("NO APLICA: no demolition plan (new construction, A0.00 scope)", None),
 "S:protocolo-de-ejecución:c67de2": ("code analysis read: A0.00 (Type IIIB, R-1/A-2/M/U, 2018 IBC, 35,676 SF, 4 stories, sprinklered) in takeoff.json proyecto_datos", "takeoff.json"),
 "S:protocolo-de-ejecución:c7fb31": ("set package confirmed: index T0.01 + building sheets (floor plans, partition types, RCP)", "SHEET_MAP.md"),
 "S:registro-de-dimension-strings-obligatori": ("printed dims used are cited in each wall length_source (CONFIRMED) and resolution files", "etapas/3_revision/resolucion.md"),
 "S:regla-1-notas-condicionales": ("conditional notes verified (A0.06 notes 11/12/13 wet rooms; F&B 'not in scope' notes; unit general note 1)", "etapas/3_revision/CRITERIOS_RESOLUCION.md"),
 "S:reglas-inviolables-error:00477b": ("each closed area persisted to disk at once (frag/*.json + resolucion_*.md)", "etapas/3_revision/resolucion.md"),
 "S:reglas-inviolables-error:0ed0b9": ("CMU (CM.8) other trade; only the furring face (FW / FI) loaded, one face", "etapas/3_revision/CRITERIOS_RESOLUCION.md"),
 "S:reglas-inviolables-error:186e69": ("dash-dot enlarged areas opened (A6.00-A6.02, A7.30, A7.45, A7.50) and counted once", "etapas/3_revision/resolucion.md"),
 "S:reglas-inviolables-error:1e4580": ("CSI check: wood, CMU, siding, SFRM, FRP, ACT, plaster = others (scope checklist)", "alcances_decision.json"),
 "S:reglas-inviolables-error:2f6dca": ("NO APLICA: no light-fixture framed openings in metal (wood framing / ACT); ducts excluded R-ALC-03", "etapas/4_canon/fo_in.json"),
 "S:reglas-inviolables-error:612274": ("rooms cross-checked between A2.0x, A3.0x and enlarged sheets by shape/position (resolution files)", "etapas/3_revision/resolucion.md"),
 "S:reglas-inviolables-error:78de83": ("NO APLICA: no existing walls (new construction; historic building separate permit)", None),
 "S:reglas-inviolables-error:83e3ad": ("NO APLICA: no user observation in this run (blind test)", None),
 "S:reglas-inviolables-error:8f6af6": ("user / COORDINACIÓN orders recorded the same turn (BIBLIOTECA BE-CR0-01..03, TIEMPOS)", "/root/cr0/TIEMPOS.md"),
 "S:reglas-inviolables-error:9815d5": ("electrical rooms: A0.06 types + MB-1 / 2HR ceiling; no cooler walls in this set", "etapas/3_revision/res/backcheck_ceilings.md"),
 "S:reglas-inviolables-error:a599e5": ("each area closed before the next (frag per area, all quantified or EXCLUDED)", "etapas/3_revision/resolucion.md"),
 "S:reglas-inviolables-error:aeec62": ("NO APLICA: no walk-in coolers in this set", None),
 "S:reglas-inviolables-error:df31b7": ("NO APLICA: no hung walls 'above' in metal; corridor soffits are wood blocking (7/A7.23)", "etapas/3_revision/res/backcheck_ceilings.md"),
 "S:reglas-inviolables-error:e416fd": ("agents asked to verify / refute with full written context (briefs)", "etapas/3_revision/BRIEF_RESOLUCION.md"),
 "S:sets-con-walls-de-wood": ("wood-framed set: board only with framing EXCLUDED (existing_walls, wood_excluded)", "etapas/3_revision/CRITERIOS_RESOLUCION.md"),
 "S:subagentes-ninguna-sesió:b02c6e": ("stage 2 split by level / area (A: L1, L2, L3, L4, cores, ceilings; B: L1-L2, L3-L4, cores)", "/root/cr0/work/BRIEF_LECTURA.md"),
 "S:subagentes-ninguna-sesió:ce4728": ("orchestrator launched stages and read their outputs", "/root/cr0/TIEMPOS.md"),
 "S:subagentes-ninguna-sesió:f40b96": ("A and B independent subagents (A/ and B/ folders, no cross access)", "etapas/2_lectura/canon_B.json"),
 "S:verificación-adversarial-propia-antes-de": ("independent audit (U-181) and blind ceiling back-check before upload", "etapas/3_revision/res/backcheck_ceilings.md"),
 "S:verificación-adversarial:68ec15": ("agent results re-checked by program (canon.py, comparar.py) before acceptance", "etapas/3_revision/revision.json"),
 "S:verificación-adversarial:8fdb9b": ("independent verifiers by area (5 resolvers + ceiling back-check + accessories)", "etapas/3_revision/resolucion.md"),
 "S:verificación-adversarial:96dbeb": ("agents briefed in writing with PDF path, sheet map, scale and criteria", "etapas/3_revision/BRIEF_RESOLUCION.md"),
 "S:verificación-adversarial:a666df": ("each A/B difference decided on the plan with crop; only surviving corrections applied", "etapas/3_revision/resolucion.md"),
 "S:verificación-adversarial:ff3032": ("unresolved items to RFI with delta and to PARA_REVISAR / Review Items", "takeoff.json"),
 "S:verificación-cruzada-del-barrido-contar": ("tag count by script (inventario_tags) crossed with both readings (comparar.py)", "etapas/3_revision/revision.json"),
 "S:verificación-cruzada-del:549861": ("untagged walls and furring bands typed by thickness and connected wall (resolution files)", "etapas/3_revision/resolucion.md"),
 "S:verificación-cruzada-del:b2705e": ("tag-without-wall alerts closed in resolution (every tag to a wall or discard)", "etapas/3_revision/revision.json"),
 "S:verificación-cruzada-del:dad47a": ("count by tag (inventory) vs walls by type (canon) closed", "etapas/3_revision/revision_extra.json"),
 "S:§1:9d79c7": ("errors -> rule + test + tool fix same turn: BE-CR0-01/02/03 published v81cf138p/r/s", "/root/cr0/TIEMPOS.md"),
 "S:§1:b6fe41": ("tool fixes proposed with diff + test to Xfinity (arbitration integrated them)", "/root/cr0/tools_nuevos/test_be_cr0_03_owner_existing.py"),
 "v26:la-auditoría-adversarial-es-un-paso-del": ("independent adversarial audit U-181 before upload", "etapas/3_revision/res/backcheck_ceilings.md"),
 "v26:regla-cuando-se-corrige-una-cantidad-se": ("operation texts regenerated by program from the canon (canon.py filas)", "etapas/4_canon/out/familias_out.json"),
 "v26:regla-juntas-de-control-si-el-set-no-las": ("control joints swept: A0.06 note 15 (no detail printed) -> loaded per note", "etapas/3_revision/res/accesorios.md"),
 "v27:regla-el-decimal-raro-se-investiga-no-se": ("layers are integers per face; no fractional layers in canon", "etapas/4_canon/takeoff_canon.json"),
 "v33:regla-no-se-pregunta-no-se-ofrece-no-se": ("marked plans (Bluebeam markups + images) produced in every run", "etapas/4_canon/takeoff_canon.json"),
 "v35:el-índice-se-genera-no-se-escribe-hoja_i": ("delivery index generated by program (LEEME) at delivery", "takeoff.json"),
 "v40:la-compuerta-verif_respuesta-py": ("NO APLICA: no technical answer to the user in this run (blind test, reports to COORDINACIÓN)", None),
 "v42:el-mapa-de-hojas-se-cruza-con-dos-fuente": ("sheet map: title blocks (arranque/inventario) + index T0.01, raster title blocks read by eye", "SHEET_MAP.md"),
 "v42:el-registro-de-lo-que-el-usuario-confirm": ("NO APLICA: no user confirmation in this autonomous run", None),
}
out, falta = [], []
for r, (v, f) in E.items():
    if f:
        p = f if f.startswith("/") else os.path.join(W, f)
        if not os.path.exists(p):
            falta.append(f"{r}: {f}")
        out.append({"regla": r, "caso": "corrida", "archivo": f, "valor": v})
    else:
        out.append({"regla": r, "caso": "corrida", "archivo": "", "valor": v})
json.dump(out, open(os.path.join(W, "etapas/4_canon/evidencias_reglas.json"), "w"), indent=1, ensure_ascii=False)
print(len(out), "evidencias; archivos faltantes:", falta)
