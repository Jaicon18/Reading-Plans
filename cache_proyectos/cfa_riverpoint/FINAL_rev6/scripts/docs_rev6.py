"""rev6 review documents (README_REVIEW, PARA_REVISAR_EN_LA_MANANA, SEGUIMIENTO, RFI_PENDIENTES) built from
the rev6 outputs only: takeoff.json (open RFIs with sweep, resolved RFIs), the rev6 Excel (NET of each Material Summary row)
and the BE-117 checker report. rev1-rev5 deliveries stay untouched in cfa_final/FINAL_FOR_REVIEW.
Use: python3 bitacora.py run scripts/docs_rev6.py <excel_rev6>"""
import json, os, re, sys
import openpyxl
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.dirname(K)
F = os.path.join(S, "cfa_final", "FINAL_FOR_REVIEW_rev6")
XL = sys.argv[1]
t = json.load(open(os.path.join(K, "takeoff.json")))
wb = openpyxl.load_workbook(XL, data_only=True)
MS = [(str(r[0]), r[1], r[2]) for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True) if r[0] and r[2] is not None]
vm = open(os.path.join(F, "proceso", "VERIFICACION_MARKUPS_rev6.md")).read()
vm_line = next(l for l in vm.splitlines() if l.startswith("- anotaciones"))
# project data table: verbatim from the rev3 README (G-000 / G-003 facts, unchanged in rev6)
r3 = open(os.path.join(S, "cfa_final", "FINAL_FOR_REVIEW", "proceso", "README_REVIEW_rev3.md")).read().splitlines()
i0 = next(i for i, l in enumerate(r3) if l.startswith("## PROJECT DATA"))
i1 = next(i for i, l in enumerate(r3) if l.startswith("## Scope summary"))
datos = r3[i0 + 1:i1]
OPEN = t["rfis"]
RES = {k: v for k, v in t["rfi_cierre"].items() if str(v.get("pregunta", "")).startswith("RESOLVED")}
CLO = {k: v for k, v in t["rfi_cierre"].items() if k not in RES}


def fmt(v, u):
    return f"{v:,.2f} {u}"


def ms_tab():
    out = ["| Material | Unit | Net |", "|---|---|---|"]
    for n, u, v in MS:
        out.append(f"| {n} | {u} | {v:,.2f} |" if isinstance(v, (int, float)) else f"| {n} | {u} | {v} |")
    return out


def short(q, n=230):
    q = re.sub(r"\s+", " ", str(q))
    return q if len(q) <= n else q[:n].rsplit(" ", 1)[0] + " ..."


def rfi_block(lang="en"):
    out = []
    for j, r in enumerate(OPEN, 1):
        o = r.get("opciones") or {}
        b = r.get("barrido") or {}
        hojas = b.get("hojas")
        out += [f"### {r['id']} ({j} of {len(OPEN)})", short(r["pregunta"].split(" - carried:")[0], 600),
                f"- **A (plans/specs, {o.get('A', {}).get('source', '')}):** {o.get('A', {}).get('texto', '')} — delta: {o.get('A', {}).get('delta', '')}",
                f"- **B (trade code, {o.get('B', {}).get('cita', '')}):** {o.get('B', {}).get('texto', '')} — delta: {o.get('B', {}).get('delta', '')}",
                "- **C (other):** ____",
                "- **Loaded now:** option A (conservative value).",
                f"- **Sweep (BE-120, CE_RFI_BARRIDO_IMPRESO):** {('ALL 172 pages (text layer + AutoCAD SHX, set_texto.json)' if hojas == 'ALL' else str(len(hojas or [])) + ' sheets: ' + ', '.join(hojas or []))}"
                + (f"; sheets opened and checked visually (rev5): {', '.join(b.get('hojas_rev5') or [])}" if b.get('hojas_rev5') else "")
                + f" · terms {', '.join(b.get('terminos') or [])}",
                f"- **Printed values next to the terms, reviewed (why they do not answer):** " + "; ".join(f"{h}: {x}" for h, x in sorted((b.get('descartes') or {}).items())),
                ""]
    return out


def res_lines():
    return [f"- {k}: {short(v['pregunta'], 330)}" for k, v in sorted(RES.items())]


ms_row = {n: (u, v) for n, u, v in MS}


def g(prefix):
    for n, (u, v) in ms_row.items():
        if n.startswith(prefix):
            return fmt(v, u)
    return "-"


HEAD = "ESTA ES LA VERSIÓN FINAL PARA REVISAR"
# ---------------- README_REVIEW
rd = [HEAD, "",
      "# README_REVIEW — Chick-fil-A #2284 River Point, Sheridan, CO (CDM Builds) — Metal Framing & Drywall take-off, FINAL FOR REVIEW rev6",
      "Date: 2026-11-03 · Bid due 2026-11-12 11:00 AM MST (CDM BUILDS) · Skill v81cf28 · Delivery gate compuerta_entrega.py GREEN (ENTREGA_OK.json) · uploaded only with subir_entrega.py · Nothing was sent to the GC.",
      "", "## PROJECT DATA"] + datos + [
      "## What changed in rev6",
      "rev6 = rev5 run through the delivery gate with the estimator's day-1 standing orders as programs (U-114..U-125: #0 status on every number, "
      "N/SHEET on every line, nothing chosen silently, tag sweep with circled images, visual evidence, English deliverable, one axis per number, "
      "Bluebeam fields on every markup) until GREEN. Changes: (1) every face height carries [CONFIRMED] / [DERIVED] with its operation; "
      "(2) board-only sources cite N/SHEET ('SW6/A-202', 'G.3/A-202', 'A.3/A-621', 'FRP-2/A-211'); (3) ONE AXIS PER NUMBER: 22 board-only entries and "
      "the L partition DEMO-02 that turned a corner are split into one entry per straight axis ('<id>-1', '<id>-2' ...; the pieces add up to the rev5 LF); "
      "(4) gypsum-ceiling demolition (A-052 KN10) marked as AREA polygons in Bluebeam; (5) Review Items and open RFIs name their circled image "
      "(proceso/review_img, proceso/rfi_img): items 2, 5, 6 and 8 got new circled crops (item 6 now shows the PT0019 mop chase, item 5 the A-052 east-room ceiling). "
      "Material Summary: no quantity changed except +0.01 SF of 1/2\" cement board (rounding of the split pieces). DEMO-C6 (Review Item 5, open): the A-052 hatch outline "
      "measures 34.57 SF; 38.35 SF reading A stays loaded until you decide (delta -3.78 SF). Item by item: proceso/CAMBIOS_rev6.md; back-check proceso/BACKCHECK_rev6.md.", "",
      "## Material Summary rev6 (NET, before waste — see the Excel for waste / purchase)"] + ms_tab() + [
      "", f"## RFIs RESOLVED from the drawings ({len(RES)}) — out of Pending Items, listed in the Scope Checklist"] + res_lines() + [
      "", f"## Open RFIs ({len(OPEN)}) — conservative value already loaded in each"] + rfi_block() + [
      "## Closed RFIs — estimator decision (option A = plans, R-ALC-10)",
      " · ".join(f"{k}" for k in sorted(CLO)) + " — see the Excel Scope Checklist for each delta.", "",
      "## Quality gates (rev6)",
      "- compuerta_entrega.py (skill v81cf28, with the day-1 checks U-114..U-125): 0 FAIL; result and AMBER list in ENTREGA_OK.json (kept with the calculation folder).",
      "- reglas.py compuerta --excel (all A_* gates) inside the delivery gate: OK.",
      f"- Markups vs Excel (verificar_markups_excel.py, BE-117): {vm_line[2:]} — proceso/VERIFICACION_MARKUPS_rev6.md.",
      "", "## Files",
      "- Take-off/CFA2284_RiverPoint_Takeoff_FINAL_rev6.xlsx (exactly the 6 fixed sheets) + its .sello.json (reglas seal)",
      "- Planos marcados/CFA2284_RiverPoint_Markups_Bluebeam_rev6.pdf + PNG per sheet (A-050, A-052, A-202, A-221)",
      "- proceso/CAMBIOS_rev6.md, VERIFICACION_MARKUPS_rev6.md, BREAKDOWN_half_inch_gyp_rev6.md, BACKCHECK_rev6.md, COBERTURA_rev6.md, DEMO_CRUCE.md; proceso/review_img (circled image of each Review Item), proceso/rfi_img (circled image of each open RFI)",
      "- rev1 - rev5 kept untouched in FINAL_FOR_REVIEW for traceability."]
open(os.path.join(F, "README_REVIEW.md"), "w").write("\n".join(rd) + "\n")
# ---------------- PARA_REVISAR (Spanish, short)
pr = [HEAD, "",
      "# PARA REVISAR EN LA MAÑANA — Chick-fil-A #2284 River Point (CDM Builds), bid 12-nov-2026 11:00 AM MST (10:00 AM hora de California) — rev6", "",
      "## Datos del proyecto"] + datos + [
      "## Qué cambió en rev6 (corrida con la compuerta de las preferencias del día 1, U-114..U-125)",
      "- Cada altura de cara con su estado [CONFIRMED] / [DERIVED] y la operación; cada renglón con N/HOJA.",
      "- Un eje por número: 22 renglones BOARD ONLY y la demo DEMO-02 que doblaban esquina quedan partidos por eje (<id>-1, <id>-2...; suman lo mismo que rev5).",
      "- Demolición de cielos de gyp (A-052 KN10) marcada como ÁREA en Bluebeam.",
      "- Review Items y RFI abiertos con su imagen circulada (proceso/review_img, proceso/rfi_img); imágenes nuevas en los items 2, 5, 6 y 8.",
      "- Cantidades: iguales a rev5 salvo +0.01 SF de 1/2\" cement board (redondeo de las piezas). DEMO-C6 (Review Item 5): el hatch de A-052 mide 34.57 SF; quedan cargados 38.35 SF (lectura A) hasta que decidas (delta -3.78 SF).", "",
      "## Lo más importante (5 puntos)",
      "1. **Casi todo es madera.** W4, W4.1, W6, W8 y SW6 son wood stud (A-202 + S-101 nota 4): framing EXCLUDED (Div. 06); su gypsum board y cement board SÍ están cargados (bloque \"BOARD ONLY\").",
      f"2. **Smoke partition al deck (+14'-8\", S-201, RFI-04 resuelto):** M3.5-01 y MB-01 suben al deck con track 3\" long-leg slotted (C1/S-801); 8\" stud {g('8\" stud')}, 3-5/8\" por fuente {g('3-5/8\" metal stud (LF of material) - per source')}.",
      f"3. **Board:** 1/2\" gyp {g('1/2\" gypsum board regular')} · 1/2\" MR {g('1/2\" gypsum board, MOISTURE')} · 5/8\" ceiling sag-resistant {g('5/8\" gypsum ceiling')} · 1/2\" cement board {g('1/2\" cement board')} · Level 5 {g('Level 5')}.",
      f"4. **Demolición de gyp / metal:** {g('Demolition')} (alturas por bahía de A4/S-601; DEMO-08/-09/-10 al B.O. de estructura impreso por la regla R-ALC-07; RFI-10 cerrado).",
      "5. **Tornillería, ductos y trades que no hacemos:** EXCLUDED, sin RFI.", "",
      f"## RFI resueltos con los planos / reglas fijas: {len(RES)}",
      ", ".join(sorted(RES)) + " — fuera de Pending Items; en el Scope Checklist como \"RESOLVED from drawings\".", "",
      f"## RFI abiertos: {len(OPEN)} (en todos ya está cargado el valor conservador y el barrido completo del set)"] + \
     [f"- {r['id']}: {short(r['pregunta'].split(' - carried:')[0], 200)}" for r in OPEN] + [
      "Detalle con opciones A (planos) · B (código) · C (otro) y delta: SEGUIMIENTO.md y hoja \"Pending Items\" del Excel.", "",
      f"## RFI cerrados (decisión del estimador = opción A, R-ALC-10): {len(CLO)}",
      ", ".join(sorted(CLO)) + " — en el Scope Checklist del Excel con su delta.", "",
      f"## Markups verificados contra el Excel (BE-117): {vm_line[2:]}", "",
      "## Dónde están los archivos (Drive › Claude outputs › Chick-fil-A #2284 River Point - Sheridan, CO (CDM Builds) 11-12-26 › rev6 FINAL — ESTA ES LA VERSIÓN FINAL PARA REVISAR; subido solo con subir_entrega.py)",
      "- Take-off › CFA2284_RiverPoint_Takeoff_FINAL_rev6.xlsx",
      "- Planos marcados › CFA2284_RiverPoint_Markups_Bluebeam_rev6.pdf y las 4 imágenes por hoja",
      "- proceso › CAMBIOS_rev6.md (qué cambió de rev5 a rev6, renglón por renglón), BACKCHECK_rev6.md, VERIFICACION_MARKUPS_rev6.md", "",
      "## Qué tienes que hacer tú (uno a la vez)",
      f"1. Abre el Excel rev6 y revisa la hoja \"Pending Items\" ({len(OPEN)} RFI).",
      "2. Contéstame los RFI aquí en el chat (te los mando con botones, 4 por ventana)."]
open(os.path.join(F, "PARA_REVISAR_EN_LA_MANANA.md"), "w").write("\n".join(pr) + "\n")
# ---------------- SEGUIMIENTO
sg = [HEAD, "",
      "# SEGUIMIENTO rev6 — Chick-fil-A #2284 River Point (items with missing information; conservative value LOADED in each)", "",
      "| # | Item | N/SHEET | What is missing (not printed) | Loaded (option A) | Delta | Sweep |", "|---|---|---|---|---|---|---|"]
for r in OPEN:
    o = r.get("opciones") or {}
    b = r.get("barrido") or {}
    np_ = r["pregunta"].split(" - not printed:")[-1] if " - not printed:" in r["pregunta"] else "printed nowhere"
    hj = b.get("hojas")
    sg.append(f"| {r['id']} | {short(r['pregunta'].split(' - carried:')[0], 160)} | {o.get('A', {}).get('source', '')} | {short(np_, 200)} | "
              f"{o.get('A', {}).get('texto', '')} | {o.get('A', {}).get('delta', '')} | {'ALL' if hj == 'ALL' else len(hj or [])} sheets, {len(b.get('terminos') or [])} terms |")
sg += ["", f"## Resolved from the drawings / standing rules ({len(RES)})"] + res_lines() + [
       "", "Block of open RFIs with options A / B / C: RFI_PENDIENTES.md and Excel 'Pending Items'."]
open(os.path.join(F, "SEGUIMIENTO.md"), "w").write("\n".join(sg) + "\n")
open(os.path.join(F, "RFI_PENDIENTES.md"), "w").write("\n".join([HEAD, "", "# RFI PENDIENTES rev6", ""] + rfi_block()) + "\n")
print(json.dumps({"open": [r["id"] for r in OPEN], "resolved": sorted(RES), "closed": sorted(CLO)}))
