"""Writes etapas/4_canon/evidencias_reglas.json: one entry per process rule (type b, case 'corrida') with the file of THIS run
(Xfinity - Interquest, Colorado Springs, CO - BCI National) that shows how it was met, or 'NO APLICA: <reason>'.
Text only, no quantities (figures quoted are read from the canon). Paths are relative to etapas/."""
import json, os
K = os.environ.get("K") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(K, "etapas", "4_canon", "evidencias_reglas.json")
c = json.load(open(os.path.join(K, "etapas", "4_canon", "takeoff_canon.json")))
nrf = sum(1 for r in c["rfis"] if r["status"] == "open")
ncl = sum(1 for r in c["rfis"] if r["status"] != "open")
PC, RS, RV, TL = "PROCESO_CORRIDA.md", "3_revision/resolucion.md", "3_revision/revision.md", "TOOL_LIMITS_CALC.md"
E = [
 ("S:subagentes-ninguna-sesió:ce4728", PC, "The orchestrator ran the stages as separate agents (inventory, readings A / B, independent schedule reader, bubble verifier, resolution, this calculation stage) and passed only file paths; no figure was handed between readings."),
 ("S:subagentes-ninguna-sesió:b02c6e", PC, "One trade floor plan (A2.0) + demolition plan A1.0 + RCP A3.0: each reading covered the whole set in one agent (2 new W2 walls, 2 column wraps, 9 demolished walls); no further split needed."),
 ("S:subagentes-ninguna-sesió:f40b96", PC, "Readings A and B independent (etapas/2_lectura/A and B, same clean PDF, inventory and brief BRIEF_COMUN.md); compared by program in 3_revision."),
 ("S:etapa-1-inventario-scrip:b4b53c", "1_inventario/inventario.md", "Inventory by script (inventario_tags.py): 22 wall-type candidates W1 x10, W2 x3, W2A x1, W3 x1, W4 x7 on A2.0 (the 2/A2.0 legend was not read by the script; types completed by scripts/inventario_types.py from the independent schedule reader indep/fichas.json); every candidate has a wall tag_id or a discard with motive in canon tags_descartados."),
 ("E17", PC, f"Unattended run: no question to the estimator; open points = {nrf} open RFI with options A / B / C and delta (Pending Items) and 6 Review Items in the Excel; {ncl} RFIs closed by the plans (rfi_cierre)."),
 ("S:§1:9d79c7", TL, "Tool limits found in this run are written in TOOL_LIMITS_CALC.md with the program fix (project scripts, no hand edit of the canon)."),
 ("S:§1:b6fe41", TL, "Fixes of this run: planmark BOX band keys, column-wrap studs for closer.py, markups_rcp 'excluded' on rotated pages (scripts/excluded_rcp.py), TO- misc markups in markups_bluebeam.verificar (scripts/verificar_final.py), pikepdf install."),
 ("R73.4", "../registro.json", "registro.py crear by bitacora with the 24 ALC rows + every canon element + every A3.0 room (scripts/registro_renglones.py); closed with registro.py marcar (scripts/registro_marcar.py); never edited by hand."),
 ("R73.15", PC, "Vendor frame interface: door 101 hollow metal frame by others (A2.0 door schedule, A0.3 3 anchors per jamb); our head = 7/A2.0 track header with nested stud, jambs by the stud program."),
 ("R77.15", PC, "Messages short; detail lives in the files (Excel Pending Items / Review Items, resolucion.md, TOOL_LIMITS_CALC.md, VERIFICACION_MARKUPS.md)."),
 ("S:formato-de-salida-del-take-off-obligator", PC, "Excel by plantilla_excel.py (fixed 6-sheet format, English, one row per wall W2-01 / W2-02 / CF-01 / CF-02, SUBTOTAL per type W2 / CF, GRAND TOTAL); demolition rows as SF only."),
 ("S:formato-de-salida-del-ta:4fca32", RS, "Demolition SF = LF x H per element (DEMO-01..09, A1.0 key 7), no layers; H = 26'-0\" conservative (RFI-01); each op in canon misc_items."),
 ("S:registro-de-dimension-strings-obligatori", "4_canon/takeoff_canon.json", "Dimensions used per wall in length_source / length_op (A2.0 printed 4\", 3'-0\" DOOR, 4'-0\"; vector bands at 18 pt/ft checked on the printed 25'-8 3/4\", 18'-6 3/4\", 44'-6\" and 29'-0 3/4\")."),
 ("S:regla-1-notas-condicionales", RS, "Conditional notes checked on their sheet: 2/A2.0 'TO 6\" ABOVE CEILING U.N.O.' (each face to its own ceiling), A2.0 key note 1 column furring 'IF EXISTING COLUMNS ARE LOCATED IN SALES AREA', key note 4 water resistant board at wet areas (restrooms existing), A2.0 table 'OPTION: CONTINUOUS BRIDGING'."),
 ("S:verificación-adversarial-propia-antes-de", RS, "Own review = independent double reading A / B compared by comparar.py and resolved item by item on the drawing with crops (resolucion.md, scripts/resolver.py)."),
 ("S:verificación-adversarial:8fdb9b", RS, "Two full independent readings of every element; differences decided on the drawing (W2-01 through the door, existing W1 / W4 not quantified, column furring, demolition pieces)."),
 ("S:verificación-adversarial:96dbeb", RS, "Each A / B difference decided by refuting one side on the drawing with crops (3_revision/img)."),
 ("S:verificación-adversarial:a666df", RS, "Only differences that survived the drawing check changed the canon; the rest kept as RFIs / Review Items."),
 ("S:verificación-adversarial:68ec15", RS, "Reader outputs were evidence with N/SHEET and crops; numbers come only from canon.py and the other tools of this run."),
 ("S:verificación-adversarial:ff3032", RS, f"Unresolved items -> {nrf} open RFI with delta and 6 Review Items; tool limits in TOOL_LIMITS_CALC.md."),
 ("S:los-markups-ajenos-no-son-fuente", PC, "Clean copy plans/bidset_SIN_MARKUPS.pdf used for every render and measure (pages 9-17 keep their AutoCAD SHX text annotations = drawing text, read as text, not as markups)."),
 ("S:los-markups-ajenos-no-so:db7106", PC, "First step of the project: clean copy bidset_SIN_MARKUPS.pdf; all crops of this run from that copy."),
 ("S:granularidad-y-marcado:33d529", RS, "Work unit = the complete type (W2, CF column furring) plus demolition by element and the SOF-01 header."),
 ("S:granularidad-y-marcado:e221c4", "7_imagenes/A2.0 - IMAGE ONLY (not editable) - walls rev1.png", "Marked plans produced by programs from the canon coordinates: markups_bluebeam.py / markups_demo.py / markups_rcp.py + scripts/excluded_rcp.py PDF, planmark.py evidence per type, imagenes_hoja.py PNG per sheet."),
 ("S:granularidad-y-marcado:7f3ce3", "4_canon/out/cierres_resumen.json", "Bands come from the sealed canon (closer.py seals of the 4 walls W2-01, W2-02, CF-01, CF-02), never from memory."),
 ("S:granularidad-y-marcado:f79808", PC, "Markups and images regenerated from the final canon in the same chain run (scripts/cadena.sh)."),
 ("S:granularidad-y-marcado:1f35f7", "7_imagenes/imagenes_hoja.json", "Final visual check on the delivered PNGs (re-opened; Wall IDs and LF / SF labels from familias_out.json / canon)."),
 ("S:granularidad-y-marcado:f3c532", "6_markups/markups.json", "Each marked sheet shows all instances of its types; markup LF per wall = canon LF (markups_bluebeam.py verificar)."),
 ("S:sets-con-walls-de-wood", RS, "NO APLICA: no wood stud walls in this set (2/A2.0 metal studs); wood only as F.R.T. blocking / 3/4\" FRT plywood = Div. 06 EXCLUDED."),
 ("S:reglas-inviolables-error:78de83", RS, "Existing walls get new board only where the drawings call it: none here; W1 / W4 'patch and repair' = allowance Review Item, not quantified."),
 ("S:reglas-inviolables-error:1e4580", PC, "Vendor / other-division items excluded: storefront, doors / frames / hardware, ACT, painting, insulation, F.R.T. wood and plywood, fasteners, MEP."),
 ("S:reglas-inviolables-error:2f6dca", "4_canon/fo_in.json", "No new GWB ceiling with devices: SOF-01 header only; no access panel located (A0.1 note 7 generic, A3.0 note 4); ducts EXCLUDED by standing order."),
 ("S:reglas-inviolables-error:0ed0b9", RS, "NO APLICA: no furred wall on an existing wall in this set; the column furring CF-01 / CF-02 (5/A2.0) wraps existing columns, board one side per 5/A2.0."),
 ("S:reglas-inviolables-error:186e69", RS, "Detail sheets opened: 2/A2.0-8/A2.0, A2.0 limiting heights table, A3.0 details 2-4, A5.0 elevations and blocking legend, A4.0 room finish schedule."),
 ("S:reglas-inviolables-error:612274", RS, "Rooms matched between A1.0 (existing / demolition) and A2.0 (new): same 1/4\" scale, offset A1.0 = A2.0 + (81.6, 6.84) pt; demo lines checked by eye (4_canon/img/demo_check.png) and crossed by program (DEMO_CRUCE.md)."),
 ("S:reglas-inviolables-error:00477b", PC, "Every wall / element persisted in the canon files on disk (canon A, B, resolved) before quantifying."),
 ("S:reglas-inviolables-error:8f6af6", PC, "Estimator standing orders kept as data in BRIEF_COMUN.md and proceso/proyecto_datos.json."),
 ("S:reglas-inviolables-error:a599e5", PC, "Types closed one by one inside each reading; this stage computes only from the closed canon."),
 ("S:reglas-inviolables-error:83e3ad", PC, "NO APLICA in this run: no estimator remark on a delivered file yet (first delivery rev1)."),
 ("S:reglas-inviolables-error:df31b7", RS, "Hung element: none (no gypsum ceiling suspension; SOF-01 is a framed header like type W2; ACT grid by others)."),
 ("S:reglas-inviolables-error:aeec62", RS, "NO APLICA: no walk-in cooler / freezer in the set (A2.0)."),
 ("S:reglas-inviolables-error:9815d5", RS, "NO APLICA: no riser room and no new rated partition (2/A2.0 W2 non-rated; A0.1 V-B sprinklered)."),
 ("S:reglas-inviolables-error:e416fd", RS, "Resolution done on the comparar.py crops with the A2.0 vector bands; each decision with its rule in resolucion.md."),
 ("S:verificación-cruzada-del-barrido-contar", RV, "Second path: comparar.py crosses the inventory candidates with both readings."),
 ("S:verificación-cruzada-del:dad47a", "1_inventario/inventario.md", "Every inventory candidate has a wall (tag_ids PT0002 / PT0003 for W2-01 / W2-02) or a discard with motive (W1 / W4 existing, 2/A2.0 legend instances) in canon tags_descartados."),
 ("S:verificación-cruzada-del:b2705e", RS, "Untagged drawn elements found and assigned: column furring at the two storefront columns (5/A2.0, key note 1), SOF-01 gyp header (A3.0), metal blocking of A5.0 / 8/A2.0."),
 ("S:verificación-cruzada-del:549861", RS, "Furring bands against existing construction: CF-01 / CF-02 column furring (5/A2.0) included; no wall furring in the set."),
 ("S:protocolo-de-ejecución:c7fb31", "0_mapa/SHEET_MAP.md", "Package confirmed: 17 sheets A0.1-A5.0, E0.0-E3.0, M0.0-M2.0, P1.0 (A0.1 sheet index), no addenda; the set contains the building (partition plan, types, RCP)."),
 ("S:protocolo-de-ejecución:b92e94", RS, "Demolition plan A1.0 read with its key notes and general demolition notes; walls to remain vs demolish vs new crossed with A2.0 (DEMO_CRUCE.md)."),
 ("S:protocolo-de-ejecución:c67de2", PC, "Code data from A0.1 with the printed edition: 2021 IBC (also 2021 IMC / IPC, 2023 NEC, ANSI A117.1-2009), construction type V-B fully sprinklered (existing), use group M (existing A-2), 1,798 SF leased, 1 story - 26 ft, 24 occupants (proceso/proyecto_datos.json, Inputs)."),
 ("S:protocolo-de-ejecución:29966c", RS, "Specs in the set = A0.3 SPECIFICATIONS (lightgage framing, gypsum board, hollow metal frames, painting, trim); cited on the material rows with the 2/A2.0 type notes and A2.0 general notes."),
 ("S:protocolo-de-ejecución:470877", "4_canon/takeoff_canon.json", "Numbered wall list with location per type before quantifying (canon walls[].location / faces rooms)."),
 ("S:protocolo-de-ejecución:19e4ec", RS, "Own verification = double reading + resolution + independent schedule reader + bubble verifier (burbujas/CADENA.md)."),
 ("S:clarifications-para-el-bid-nunca-omitir", PC, "Clarifications & exclusions in the Scope Checklist (EXCLUDED rows: ACT, painting, insulation, wood Div. 06, fasteners, sealant, doors / frames, storefront, MEP, ducts, existing ceiling demolition, patch & repair allowance, existing walls W1 / W4) and Pending Items (RFI-01)."),
 ("REGLA 49.1", PC, "Deliverables saved in the project work folder (etapas/8_excel, etapas/7_imagenes); nothing uploaded or sent by this stage."),
 ("REGLA 50.3", PC, "One type / system at a time inside each reading; progress persisted as canon files on disk."),
 ("REGLA 50.4", PC, "NO APLICA: first calculation run of this project, no previous backup to resume."),
 ("REGLA 52.2", PC, "Tools run with TAKEOFF_WORK = this run's etapas and BITACORA = work/bitacora.jsonl (scripts/env.sh)."),
 ("REGLA 55.1", PC, "Sheet-by-sheet scope sweep = hojas_revisadas of takeoff.json (17 sheets) + alcances.py escanear / compuerta."),
 ("REGLA 56.8", RS, "Metal blocking printed (A5.0 blocking legend EV-44 / EV-45, A2.0 key notes 5 / 6 + 8/A2.0) carried in blocking items; no NTS edge-blocking detail."),
 ("REGLA 59.14", PC, "NO APLICA: no NTS edge-blocking detail in this set."),
 ("v26:la-auditoría-adversarial-es-un-paso-del", RS, "Self-audit = A / B resolution (resolucion.md) + independent schedule reader + bubble verifier."),
 ("v26:regla-cuando-se-corrige-una-cantidad-se", "4_canon/takeoff_canon.json", "When a length changed in the resolution (W2-01 through the door, 10.64 -> 13.973 LF) its length_op / length_source were rewritten in the element."),
 ("v26:regla-juntas-de-control-si-el-set-no-las", RS, "No control joint printed; longest new run 10.64 ft (W2-01 between door and post): none carried (Scope Checklist ALC-18)."),
 ("v27:regla-el-decimal-raro-se-investiga-no-se", PC, "No fractional layers in the canon (layers are integers per face)."),
 ("v33:regla-no-se-pregunta-no-se-ofrece-no-se", PC, "Marked plans produced without being asked: markups PDF (walls + demolition + RCP EXCLUDED), one PNG per type and per marked sheet."),
 ("v35:el-índice-se-genera-no-se-escribe-hoja_i", PC, "The file list of the delivery is generated from the folder listing in the final report."),
 ("v40:la-compuerta-verif_respuesta-py", PC, "Final report written from the tool outputs (Excel, gates, markups JSON, VERIFICACION_MARKUPS.md)."),
 ("v42:el-mapa-de-hojas-se-cruza-con-dos-fuente", "0_mapa/SHEET_MAP.md", "Sheet map from the title block of each page (inventario.json) crossed with the A0.1 sheet index (17 sheets)."),
 ("v42:el-registro-de-lo-que-el-usuario-confirm", PC, "Estimator standing orders saved as data (BRIEF_COMUN.md, proyecto_datos.json); no new confirmation in this run."),
]
out = [{"regla": r, "caso": "corrida", "archivo": a, "valor": v} for r, a, v in E]
# Unnumbered titled views of the canon details (WALL LEGEND / LIMITING HEIGHTS on A2.0, BLOCKING LEGEND on A5.0): the sheet prints
# NO detail number, so the N/HOJA citation the detail rules ask for does not exist (gate limit, TOOL_LIMITS_CALC.md). Each one is
# recorded as 'NO APLICA: <why>' with its sheet and image, plus what was read in it (canon details[*].notes).
DET_RULES = ["S:§1:b657b3", "S:regla-2-verifica-cada-tipo-individualmen", "S:granularidad-y-marcado:c05930",
             "S:protocolo-de-ejecución:e177fd", "REGLA 54.6", "v26:regla-medir-lo-no-acotado-dentro-de-un-d",
             "v34:regla-no-se-cierra-un-proyecto-sin-haber", "v37:y-la-regla-general-que-esto-confirma",
             "v37:2-una-layer-que-las-secciones-no-rotulan"]
SEAL_RULES = ["REGLA 54.4", "REGLA 56.6", "REGLA 59.12"]
import re as _re
for k, d in (c.get("details") or {}).items():
    if _re.match(r"^[0-9A-Z]{1,3}/", k):
        continue                                          # numbered detail: its own N/HOJA in the canon
    sh = k.split("/")[-1]
    base = f"'{d.get('title')}' is an unnumbered titled view printed on {sh} (no detail bubble / number on the sheet)"
    for r in DET_RULES:
        out.append({"regla": r, "caso": k, "source": sh, "img": d.get("img"),
                    "valor": f"NO APLICA: N/HOJA - {base}; read complete: {d.get('notes')}"})
    for r in SEAL_RULES:
        out.append({"regla": r, "caso": k, "source": sh, "img": d.get("img"),
                    "valor": f"NO APLICA: {base}; {d.get('sealant_none_reason')}"})
json.dump(out, open(P, "w"), indent=1, ensure_ascii=False)
print(len(out))
