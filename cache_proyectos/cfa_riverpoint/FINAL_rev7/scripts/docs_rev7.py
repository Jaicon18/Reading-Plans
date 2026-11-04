"""rev7 review documents (README_REVIEW, PARA_REVISAR_EN_LA_MANANA, SEGUIMIENTO, RFI_PENDIENTES) built from
the rev7 outputs only: takeoff.json (open RFIs with sweep, resolved RFIs), the rev7 Excel (NET of each Material Summary row)
and the BE-117 checker report. rev1-rev6 deliveries stay untouched in cfa_final/FINAL_FOR_REVIEW.
Use: python3 bitacora.py run scripts/docs_rev7.py <excel_rev7>"""
import json, os, re, sys
import openpyxl
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.dirname(K)
F = os.path.join(S, "cfa_final", "FINAL_FOR_REVIEW_rev7")
XL = sys.argv[1]
t = json.load(open(os.path.join(K, "takeoff.json")))
wb = openpyxl.load_workbook(XL, data_only=True)
MS = [(str(r[0]), r[1], r[2]) for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True) if r[0] and r[2] is not None]
vm = open(os.path.join(F, "proceso", "VERIFICACION_MARKUPS_rev7.md")).read()
vm_line = next(l for l in vm.splitlines() if l.startswith("- anotaciones"))
# project data table: verbatim from the rev3 README (G-000 / G-003 facts, unchanged in rev7)
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
                + (f"; sheets opened and checked visually (rev6): {', '.join(b.get('hojas_rev6') or [])}" if b.get('hojas_rev6') else "")
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
      "# README_REVIEW — Chick-fil-A #2284 River Point, Sheridan, CO (CDM Builds) — Metal Framing & Drywall take-off, FINAL FOR REVIEW rev7",
      "Date: 2026-11-04 · Bid due 2026-11-12 11:00 AM MST (CDM BUILDS) · Skill v81cf35 · Delivery gate compuerta_entrega.py GREEN (ENTREGA_OK.json) · uploaded only with subir_entrega.py · Nothing was sent to the GC.",
      "", "## PROJECT DATA"] + datos + [
      "## What changed in rev7",
      "rev7 = rev6 with EVERY detail / elevation / section bubble of our sheets followed to the end of its chain (delivery gate v81cf33+, two-line bubble "
      "detector: 79 bubbles on A-202 / A-221 + the details they call = 101 views read, each with a circled crop in proceso/bubbles_img). "
      "Each view is cited in the rows it governs or written as not applicable with its reason. What the views changed: "
      "(1) EX-KIT-02 removed - A3/A-601 'OPEN TO BEYOND' + A-202 10'-0 1/2\" critical clear opening: no wall there; "
      "(2) restroom cement / gyp transition 2 1/4\" below T/TILE (A2/A-604): cement board 6'-6 1/4\", MR gyp above; "
      "(3) MB-01 serving face gyp from 7'-0\" to 6\" over the serving ACT (D3/A-624) = 3.5 ft; cement board 0-7'-0\" behind the CT-72 tile of the menu board wall; "
      "(4) back-of-house non-kitchen cement board base 1'-3\" (C3/A-604, called by the A-602 / A-603 elevations); "
      "(5) dining wainscot walls: plywood BY G.C. to T/PLYWOOD 6'-4\" (A-625), our gyp only above it; "
      "(6) W6 dining face at the drive-thru: CT-58A tile to the ceiling (A4/A-621) -> cement board full height; "
      "(7) serving tile walls to CEILING 10'-2\" (D2 / D3/A-622, RFI-26 open). New open RFIs: RFI-26 (serving ceiling 10'-2\" vs 10'-0\") and RFI-27 "
      "(drive-thru furr down B.O. 7'-8\", C1/A-603, nothing loaded). Item by item: proceso/CAMBIOS_rev7.md; back-check proceso/BACKCHECK_rev7.md.", "",
      "## Material Summary rev7 (NET, before waste — see the Excel for waste / purchase)"] + ms_tab() + [
      "", f"## RFIs RESOLVED from the drawings ({len(RES)}) — out of Pending Items, listed in the Scope Checklist"] + res_lines() + [
      "", f"## Open RFIs ({len(OPEN)}) — conservative value already loaded in each"] + rfi_block() + [
      "## Closed RFIs — estimator decision (option A = plans, R-ALC-10)",
      " · ".join(f"{k}" for k in sorted(CLO)) + " — see the Excel Scope Checklist for each delta.", "",
      "## Quality gates (rev7)",
      "- compuerta_entrega.py (skill v81cf35: day-1 checks + two-line bubble chain CE_CALLOUTS): 0 FAIL; result and AMBER list in ENTREGA_OK.json (kept with the calculation folder).",
      "- reglas.py compuerta --excel (all A_* gates) inside the delivery gate: OK.",
      f"- Markups vs Excel (verificar_markups_excel.py, BE-117): {vm_line[2:]} — proceso/VERIFICACION_MARKUPS_rev7.md.",
      "", "## Files",
      "- Take-off/CFA2284_RiverPoint_Takeoff_FINAL_rev7.xlsx (exactly the 6 fixed sheets) + its .sello.json (reglas seal)",
      "- Planos marcados/CFA2284_RiverPoint_Markups_Bluebeam_rev7.pdf + PNG per sheet (A-050, A-052, A-202, A-221)",
      "- proceso/CAMBIOS_rev7.md, VERIFICACION_MARKUPS_rev7.md, BREAKDOWN_half_inch_gyp_rev7.md, BACKCHECK_rev7.md, COBERTURA_rev7.md, DEMO_CRUCE.md; proceso/review_img (circled image of each Review Item), proceso/rfi_img (circled image of each open RFI), proceso/bubbles_img (circled crop of each of the 101 bubble views)",
      "- rev1 - rev6 kept untouched in FINAL_FOR_REVIEW for traceability."]
open(os.path.join(F, "README_REVIEW.md"), "w").write("\n".join(rd) + "\n")
# ---------------- PARA_REVISAR (Spanish, short)
pr = [HEAD, "",
      "# PARA REVISAR EN LA MAÑANA — Chick-fil-A #2284 River Point (CDM Builds), bid 12-nov-2026 11:00 AM MST (10:00 AM hora de California) — rev7", "",
      "## Datos del proyecto"] + datos + [
      "## Qué cambió en rev7 (todas las burbujas de detalle seguidas hasta el final: 101 vistas, cada una citada o declarada no aplica con motivo)",
      "- EX-KIT-02 fuera: A3/A-601 'OPEN TO BEYOND' + A-202 abertura de 10'-0 1/2\" (no hay wall).",
      "- Restrooms: transición cement / gyp 2 1/4\" bajo T/TILE (A2/A-604): cement board 6'-6 1/4\", MR gyp arriba.",
      "- Menu board MB-01: gyp de la cara de servicio de 7'-0\" a 6\" sobre el ACT (D3/A-624) = 3.5 ft; cement board 0-7'-0\" detrás del tile CT-72.",
      "- Base de cement board 1'-3\" en BOH sin cocina (C3/A-604); wainscot del comedor = plywood BY G.C. hasta 6'-4\" (A-625), nuestro gyp solo arriba.",
      "- W6 del comedor junto al drive-thru: tile CT-58A hasta el ceiling (A4/A-621) -> cement board de altura completa.",
      "- RFI nuevos abiertos: RFI-26 (ceiling de servicio 10'-2\" vs 10'-0\") y RFI-27 (furr down del drive-thru a 7'-8\", sin cargar).", "",
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
      "## Dónde están los archivos (Drive › Claude outputs › Chick-fil-A #2284 River Point - Sheridan, CO (CDM Builds) 11-12-26 › rev7 FINAL — ESTA ES LA VERSIÓN FINAL PARA REVISAR; subido solo con subir_entrega.py)",
      "- Take-off › CFA2284_RiverPoint_Takeoff_FINAL_rev7.xlsx",
      "- Planos marcados › CFA2284_RiverPoint_Markups_Bluebeam_rev7.pdf y las 4 imágenes por hoja",
      "- proceso › CAMBIOS_rev7.md (qué cambió de rev6 a rev7, renglón por renglón), BACKCHECK_rev7.md, VERIFICACION_MARKUPS_rev7.md", "",
      "## Qué tienes que hacer tú (uno a la vez)",
      f"1. Abre el Excel rev7 y revisa la hoja \"Pending Items\" ({len(OPEN)} RFI).",
      "2. Contéstame los RFI aquí en el chat (te los mando con botones, 4 por ventana)."]
open(os.path.join(F, "PARA_REVISAR_EN_LA_MANANA.md"), "w").write("\n".join(pr) + "\n")
# ---------------- SEGUIMIENTO
sg = [HEAD, "",
      "# SEGUIMIENTO rev7 — Chick-fil-A #2284 River Point (items with missing information; conservative value LOADED in each)", "",
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
open(os.path.join(F, "RFI_PENDIENTES.md"), "w").write("\n".join([HEAD, "", "# RFI PENDIENTES rev7", ""] + rfi_block()) + "\n")
print(json.dumps({"open": [r["id"] for r in OPEN], "resolved": sorted(RES), "closed": sorted(CLO)}))
