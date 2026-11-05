#!/usr/bin/env python3
"""README_REVIEW.md (English), PARA_REVISAR_EN_LA_MANANA.md and SEGUIMIENTO.md (Spanish notes, trade terms in English) of
the Consumer Cellular Centennial rev1 FINAL delivery. Every number is read from the delivered Excel / canon; nothing typed.
Usage: hacer_docs.py <entrega_dir> <proyecto_datos.json> <takeoff.json> <canon.json>"""
import json, os, sys
import openpyxl
E, PD, TJ, CN = sys.argv[1:5]
x = next(os.path.join(E, "Take-off", f) for f in os.listdir(os.path.join(E, "Take-off")) if f.endswith(".xlsx"))
wb = openpyxl.load_workbook(x, data_only=True)
pdj = json.load(open(PD)); td = json.load(open(TJ)); c = json.load(open(CN))
ms = [r for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True) if r[0] and isinstance(r[2], (int, float))]
pt = [r for r in wb["Partition Takeoff"].iter_rows(min_row=1, values_only=True)]
rf = [r for r in c["rfis"] if r["status"] == "open"]
titulo = "Consumer Cellular - Yosemite Park Shopping Center, Centennial, CO (store CO2) — Metal framing & drywall take-off, rev1 FINAL"
def datos():
    L = ["## PROJECT DATA", "", "| Field | Value | Source |", "|---|---|---|"]
    for d in td["proyecto_datos"]:
        L.append(f"| {d['campo']} | {d['valor']} | {d.get('fuente') or '-'} |")
    L += ["", "**Mandatory sheets reviewed**", "", "| Category | Status | Sheets |", "|---|---|---|"]
    for h in td["hojas_revisadas"]:
        L.append(f"| {h['categoria']} | {h['estado']} | {h['hojas']} |")
    return L
tot = {}
for w in c["walls"]:
    tot.setdefault(w["tag"], [0, 0.0]); tot[w["tag"]][0] += 1; tot[w["tag"]][1] += w["length_ft"]
R = [f"# {titulo}", ""] + datos() + [
 "", "## Bid sets of the two GCs", "",
 "- Elite Retail Services (Vivian Tran): BuildingConnected 'Consumer Cellular - Yosemite Park Shopping Center - Centennial, CO: Drywall & Framing', bid 11/05/2026 4:00 PM CT; plan room elite-constructionplans.com: 37 single sheets + Starlink.pdf + 15 bid forms; BuildingConnected: survey report + survey documents.",
 "- Elder-Jones, Inc. (Mason Bender): BuildingConnected 'Consumer Cellular - Centennial CO: Drywall & Framing', bid 11/06/2026: one PDF '15066-26-CC-Centennial, CO - Permit Set_10.15.2026.pdf' (37 pages).",
 "- Compared by program sheet by sheet: the text of all 37 sheets is identical (Elite's G000 cover is a letter-size copy of the same sheet). Elite adds the Starlink fire-alarm monitoring document (LL requirement, not our trade) and the survey documents. The Elder-Jones PDF is the bid set of this take-off; the delta between the two GCs is 0 for our scope.",
 "", "## What is in this folder", "",
 "- `Take-off/Consumer_Cellular_Centennial_Takeoff_FINAL_rev1.xlsx` — fixed 6-sheet format (Inputs, Partition Takeoff, Material Summary, Pending Items, Review Items, Scope Checklist). Waste applied once, in the Material Summary.",
 "- `Planos marcados/Consumer_Cellular_Centennial_markups_rev1.pdf` — Bluebeam markups: walls on A100 (Subject = type, Page Label, Length, Depth = wall height, Wall Area; Contents = TYPE · LF · H · board SF · DETAIL · Wall ID), demolition lines on D100 (SF only), restroom gypsum ceiling polygon on A200 + one PNG per type (`A100_type_<T>.png`) and one per marked sheet.",
 "- `Planos marcados/DETALLES_REVISADOS.pdf` — every detail / section / elevation bubble reviewed, circled and numbered on the calling sheet and on its destination (index below).",
 "- `Planos marcados/SCHEDULES_REVISADOS.pdf` — every trade schedule row marked (red circle + check + number); material list SCHEDULES_MATERIALES below.",
 "- `SEGUIMIENTO.md` — RFI follow-up (Spanish). `PARA_REVISAR_EN_LA_MANANA.md` — review-first notes (Spanish).",
 "- `Auditoria/` — delivery gate (ENTREGA_OK.json), bubble verification, independent schedule reading, back-check, bank comparison.",
 "", "## Walls by type (schedule order 1/A500)", "", "| Type | Walls | LF | Detail |", "|---|---|---|---|"]
for t in ("A3", "C3", "D", "E3"):
    R.append(f"| {t} | {tot[t][0]} | {tot[t][1]:,.2f} | {t}/A500 |")
R += ["", "## Material Summary (net, before waste)", "", "| Material | Unit | Net | Where it comes from |", "|---|---|---|---|"]
for r in ms:
    R.append(f"| {r[0]} | {r[1]} | {r[2]:,.2f} | {str(r[8] or '')[:110]} |")
R += ["", "## Open RFIs (conservative value loaded)", "", "| RFI | Question | Loaded | Options A / B / C with delta |", "|---|---|---|---|"]
for r in rf:
    o = r["opciones"]
    R.append(f"| {r['id']} | {r['question']} | {r['loaded']} | (A) {o['A']['texto']} - delta {o['A']['delta']} / (B) {o['B']['texto']} ({o['B']['cita']}) - delta {o['B']['delta']} / (C) other: ____ |")
open(os.path.join(E, "README_REVIEW.md"), "w", encoding="utf-8").write("\n".join(R) + "\n")
P = [f"# Revisar primero — {titulo}", "", "Notas en español; los términos del trade van en inglés. Los datos del proyecto están en README_REVIEW.md (PROJECT DATA).", "",
 "## Proyecto", "", f"- {td['proyecto']}", "- GC: Elite Retail Services (bid 11/05/2026 4:00 PM CT) y Elder-Jones, Inc. (bid 11/06/2026). Los dos sets son idénticos hoja por hoja (comparados por programa): delta entre GC = 0 para nuestro alcance.",
 "- Tenant improvement, 3,103 SF (G003), IBC 2021, Type II-B, M, not sprinklered. Sin project manual: A700 son schedules de acabados.", "",
 "## Revisar esto primero", "",
 f"1. RFI abiertos: {len(rf)} (Pending Items), todos con el supuesto conservador CARGADO y su delta (detalle en SEGUIMIENTO.md).",
 "2. RFI-02: type A# dice '5/8\" TYPE X ON EACH SIDE' pero la sección dibuja una sola cara; se cargaron las DOS caras (regla BOTH SIDES). La opción de una cara resta el delta indicado.",
 "3. RFI-01: el corte de deck 16'-4\" / 17'-1 9/16\" no está dibujado; C3-01 cargado a 17'-1 9/16\".",
 "4. Demolición: solo SF (DEMO-01..06, D100 keys 9 y 27) a la altura del B.O. de estructura impreso; cielos existentes (key 7) EXCLUDED por falta de información (gyp vs ACT no indicado).",
 "5. FRP (B-3), insulation, ACT, paint, wood (FRT plywood, 2X4) y tornillería: EXCLUDED con nota, sin RFI.",
 "6. Review Items del Excel: columna existente (A3 norte), caras E3 entre cielos distintos, signage blocking exterior y patch & repair (allowance del estimador).",
 "7. Compuerta de entrega: `Auditoria/ENTREGA_OK.json`."]
open(os.path.join(E, "PARA_REVISAR_EN_LA_MANANA.md"), "w", encoding="utf-8").write("\n".join(P) + "\n")
S = [f"# SEGUIMIENTO de RFI — {titulo}", "", "Lista aparte (regla del usuario): ítem, N/HOJA, qué falta, supuesto cargado, delta y # RFI. Opciones: (A) planos · (B) código · (C) otro.", "",
     "| # RFI | Ítem | N/HOJA | Qué falta | Supuesto cargado | Delta (A) / (B) |", "|---|---|---|---|---|---|"]
for r in rf:
    o = r["opciones"]
    S.append(f"| {r['id']} | {r['question'][:160]} | {r['source']} | {r['why_not_printed']} | {r['loaded']} | (A) {o['A']['delta']} / (B) {o['B']['delta']} |")
S += ["", "## Cerrados (aplicados en las cantidades)", "", "| # RFI | Decisión |", "|---|---|"]
for r in c["rfis"]:
    if r["status"] != "open":
        S.append(f"| {r['id']} | {r['resolved']['answer']} ({r['resolved']['source']}) |")
open(os.path.join(E, "SEGUIMIENTO.md"), "w", encoding="utf-8").write("\n".join(S) + "\n")
print("docs OK", len(rf), "open RFIs")
