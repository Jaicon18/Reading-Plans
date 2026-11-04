"""rev8 review documents (README_REVIEW, PARA_REVISAR_EN_LA_MANANA, SEGUIMIENTO, RFI_PENDIENTES) built from
the rev8 outputs only: takeoff.json (open RFIs with sweep, resolved RFIs), the rev8 Excel (NET of each Material Summary row)
and the BE-117 checker report. rev1-rev7 deliveries stay untouched in cfa_final/FINAL_FOR_REVIEW.
Use: python3 bitacora.py run scripts/docs_rev8.py <excel_rev8>"""
import json, os, re, sys
import openpyxl
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.dirname(K)
F = os.path.join(S, "cfa_final", "FINAL_FOR_REVIEW_rev8")
XL = sys.argv[1]
t = json.load(open(os.path.join(K, "takeoff.json")))
wb = openpyxl.load_workbook(XL, data_only=True)
MS = [(str(r[0]), r[1], r[2]) for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True) if r[0] and r[2] is not None]
vm = open(os.path.join(F, "proceso", "VERIFICACION_MARKUPS_rev8.md")).read()
vm_line = next(l for l in vm.splitlines() if l.startswith("- anotaciones"))
# project data table: verbatim from the rev3 README (G-000 / G-003 facts, unchanged in rev8)
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
                + (f"; sheets opened and checked visually (rev7): {', '.join(b.get('hojas_rev7') or [])}" if b.get('hojas_rev7') else "")
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
      "# README_REVIEW — Chick-fil-A #2284 River Point, Sheridan, CO (CDM Builds) — Metal Framing & Drywall take-off, FINAL FOR REVIEW rev8",
      "Date: 2026-11-04 · Bid due 2026-11-12 11:00 AM MST (CDM BUILDS) · Skill v81cf37 · Delivery gate compuerta_entrega.py GREEN (ENTREGA_OK.json) · uploaded only with subir_entrega.py · Nothing was sent to the GC.",
      "", "## PROJECT DATA"] + datos + [
      "## What changed in rev8",
      "rev8 = rev7 + the drive-thru furr down LOADED (U-048: an open RFI carries the conservative value loaded, never 'nothing loaded'): "
      "C1/A-603 prints '7'-8\" B.O. FURR DOWN' with FRP-2 above and CEILING 10'-2\"; face 2.833 ft of 1/2\" cement board (to 4\" above the ceiling, G.4/A-202), "
      "bottom 2'-0\" deep ASSUMED (depth not printed, RFI-27 with the delta per 6\"), framed as the typical soffit C4/A-624 (3-5/8\" @ 16\", braces @ 32\"), "
      "3 track runs and corner bead, 11.011 LF (run of EX-DT-01). rev7 (every detail bubble followed to the end, 101 views) is unchanged otherwise. "
      "Item by item: proceso/CAMBIOS_rev8.md; back-check proceso/BACKCHECK_rev8.md.", "",
      "## Material Summary rev8 (NET, before waste — see the Excel for waste / purchase)"] + ms_tab() + [
      "", f"## RFIs RESOLVED from the drawings ({len(RES)}) — out of Pending Items, listed in the Scope Checklist"] + res_lines() + [
      "", f"## Open RFIs ({len(OPEN)}) — conservative value already loaded in each"] + rfi_block() + [
      "## Closed RFIs — estimator decision (option A = plans, R-ALC-10)",
      " · ".join(f"{k}" for k in sorted(CLO)) + " — see the Excel Scope Checklist for each delta.", "",
      "## Quality gates (rev8)",
      "- compuerta_entrega.py (skill v81cf37: day-1 checks + two-line bubble chain CE_CALLOUTS + U-048 open RFI loaded): 0 FAIL; result and AMBER list in ENTREGA_OK.json (kept with the calculation folder).",
      "- reglas.py compuerta --excel (all A_* gates) inside the delivery gate: OK.",
      f"- Markups vs Excel (verificar_markups_excel.py, BE-117): {vm_line[2:]} — proceso/VERIFICACION_MARKUPS_rev8.md.",
      "", "## Files",
      "- Take-off/CFA2284_RiverPoint_Takeoff_FINAL_rev8.xlsx (exactly the 6 fixed sheets) + its .sello.json (reglas seal)",
      "- Planos marcados/CFA2284_RiverPoint_Markups_Bluebeam_rev8.pdf + PNG per sheet (A-050, A-052, A-202, A-221)",
      "- proceso/CAMBIOS_rev8.md, VERIFICACION_MARKUPS_rev8.md, BREAKDOWN_half_inch_gyp_rev8.md, BACKCHECK_rev8.md, COBERTURA_rev8.md, DEMO_CRUCE.md; proceso/review_img (circled image of each Review Item), proceso/rfi_img (circled image of each open RFI), proceso/bubbles_img (circled crop of each of the 101 bubble views)",
      "- rev1 - rev7 kept untouched in FINAL_FOR_REVIEW for traceability."]
open(os.path.join(F, "README_REVIEW.md"), "w").write("\n".join(rd) + "\n")
# ---------------- PARA_REVISAR (Spanish, short)
pr = [HEAD, "",
      "# PARA REVISAR EN LA MAÑANA — Chick-fil-A #2284 River Point (CDM Builds), bid 12-nov-2026 11:00 AM MST (10:00 AM hora de California) — rev8", "",
      "## Datos del proyecto"] + datos + [
      "## Qué cambió en rev8",
      "- Furr down del drive-thru CARGADO (C1/A-603: B.O. 7'-8\", CEILING 10'-2\"): cara 2.833 ft de 1/2\" cement board, fondo 2'-0\" SUPUESTO (la profundidad no está impresa, RFI-27 con delta por 6\"), framing como el soffit típico C4/A-624, 11.011 LF.",
      "- Todo lo de rev7 (las 101 burbujas seguidas) sigue igual.", "",
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
      "## Dónde están los archivos (Drive › Claude outputs › Chick-fil-A #2284 River Point - Sheridan, CO (CDM Builds) 11-12-26 › rev8 FINAL — ESTA ES LA VERSIÓN FINAL PARA REVISAR; subido solo con subir_entrega.py)",
      "- Take-off › CFA2284_RiverPoint_Takeoff_FINAL_rev8.xlsx",
      "- Planos marcados › CFA2284_RiverPoint_Markups_Bluebeam_rev8.pdf y las 4 imágenes por hoja",
      "- proceso › CAMBIOS_rev8.md (qué cambió de rev7 a rev8, renglón por renglón), BACKCHECK_rev8.md, VERIFICACION_MARKUPS_rev8.md", "",
      "## Qué tienes que hacer tú (uno a la vez)",
      f"1. Abre el Excel rev8 y revisa la hoja \"Pending Items\" ({len(OPEN)} RFI).",
      "2. Contéstame los RFI aquí en el chat (te los mando con botones, 4 por ventana)."]
open(os.path.join(F, "PARA_REVISAR_EN_LA_MANANA.md"), "w").write("\n".join(pr) + "\n")
# ---------------- SEGUIMIENTO
sg = [HEAD, "",
      "# SEGUIMIENTO rev8 — Chick-fil-A #2284 River Point (items with missing information; conservative value LOADED in each)", "",
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
open(os.path.join(F, "RFI_PENDIENTES.md"), "w").write("\n".join([HEAD, "", "# RFI PENDIENTES rev8", ""] + rfi_block()) + "\n")
print(json.dumps({"open": [r["id"] for r in OPEN], "resolved": sorted(RES), "closed": sorted(CLO)}))
