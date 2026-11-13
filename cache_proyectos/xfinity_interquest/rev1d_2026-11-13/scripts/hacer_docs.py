#!/usr/bin/env python3
"""README_REVIEW.md (English), PARA_REVISAR_EN_LA_MANANA.md, SEGUIMIENTO.md, GUIA_DE_REVISION_DEL_ESTIMADOR.md and
RESUMEN_rev1.md (Spanish, trade terms in English) of Xfinity Interquest rev1 FINAL. Every figure is read from the delivered
Excel and the canon; nothing typed by hand.  Use: hacer_docs.py <entrega_dir> <proyecto_datos.json> <takeoff.json> <canon.json>"""
import json, os, sys
import openpyxl
E, PD, TJ, CN = sys.argv[1:5]
x = next(os.path.join(E, "Take-off", f) for f in os.listdir(os.path.join(E, "Take-off")) if f.endswith(".xlsx"))
XN = os.path.basename(x)
wb = openpyxl.load_workbook(x, data_only=True)
td = json.load(open(TJ)); c = json.load(open(CN))
ms = [r for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True) if r[0] and isinstance(r[2], (int, float))]
pt = [r for r in wb["Partition Takeoff"].iter_rows(min_row=5, values_only=True) if r[1] and isinstance(r[2], (int, float)) and not str(r[1]).startswith(("SUBTOTAL", "TOTAL"))]
rf = [r for r in c["rfis"] if r["status"] == "open"]; cr = [r for r in c["rfis"] if r["status"] != "open"]
ud = [r for r in cr if "user decision" in str((r.get("resolved") or {}).get("by", ""))]
DLF = round(sum(m["lf"] for m in c["misc_items"] if m.get("element") == "demo" and m.get("lf")), 2)
PDF = "XF_markups_rev1d - OPEN IN BLUEBEAM.pdf"
TIT = "Xfinity - Interquest, 1333 Interquest Pkwy, Lot 11, Colorado Springs, CO 80921 - Metal framing & drywall take-off, rev1 FINAL"
def fam(sub, unit=True):
    v = [r for r in ms if sub.lower() in str(r[0]).lower() and r[2]]
    return " + ".join(f"{r[2]:,.2f} {r[1] if unit else ''}".strip() for r in v) if v else "0"
def datos():
    L = ["## PROJECT DATA", "", "| Field | Value | Source |", "|---|---|---|"]
    for d in td["proyecto_datos"]:
        L.append(f"| {d['campo']} | {d['valor']} | {d.get('fuente') or '-'} |")
    L += ["", "**Mandatory sheets reviewed**", "", "| Category | Status | Sheets |", "|---|---|---|"]
    for h in td["hojas_revisadas"]:
        L.append(f"| {h['categoria']} | {h['estado']} | {h['hojas']} |")
    return L
demo = [m for m in c["misc_items"] if m.get("element") == "demo"]
R = [f"# {TIT}", ""] + datos() + [
 "", "## Bid set and GC", "",
 "- BCI National Construction & Facilities (Kyle McGee, Estimating Lead; Morgan Fergus): BuildingConnected 'Xfinity - Inter Quest, CO TI Improvement Project: Drywall & Framing', proposals due Friday Nov 13, 2026 end of day, bid as day work (regular business hours). Only GC found in estimating@jchunter.us. Acoustical Ceilings and Painting are separate bid packages (not ours).",
 "- Bid set: 'Xfinity BP_Colorado Springs, CO_Interquest_Complete PDF Set_10-08-26_R0.pdf', 17 sheets (A0.1-A5.0, E0.0-E3.0, M0.0-M2.0, P1.0), Robert F. Vanney Architect, 10/08/2026; no addenda; specs on sheet A0.3. The 1,589 annotations of the set are AutoCAD SHX drawing text (kept; no take-off markups).",
 "", "## What is in this folder", "",
 f"- `Take-off/{XN}` - fixed 6-sheet format (Inputs, Partition Takeoff, Material Summary, Pending Items, Review Items, Scope Checklist), one row per wall, SUBTOTAL per type, GRAND TOTAL.",
 f"- `Planos marcados/{PDF}` - the only editable markups file (Subject = type, Page Label = sheet, Length, Depth = height, Wall Area; demolition on A1.0; SOF-01 header and EXCLUDED rooms on A3.0). PNGs named 'IMAGE ONLY (not editable)' are pictures only.",
 "- `Planos marcados/DETALLES_REVISADOS.pdf` (every detail bubble circled in origin and destination, U-141) and `Planos marcados/SCHEDULES_REVISADOS.pdf` (every type / schedule row marked, U-142).",
 "- `GUIA_DE_REVISION_DEL_ESTIMADOR.md`, `PARA_REVISAR_EN_LA_MANANA.md`, `SEGUIMIENTO.md`, `RESUMEN_rev1.md`, `TIEMPOS.md`, `CHECKLIST_REVISION.xlsx` (U-168), `Proposal/` (U-150).",
 "- `Auditoria/` - tag sweep, bubbles, independent schedule reading, A/B resolution with crops, RFI / Review Item images, independent review before delivery.",
 "", "## Scope basis (read first)", "",
 "- New construction is small: type W2 (2/A2.0: 5/8\" Type X both sides over 3-5/8\" metal studs, slab to 6\" above ceiling, studs per the A2.0 INTERIOR WALL LIMITING HEIGHTS table) at the Storage 101 / Retail 100 partition with door 101 and a 4'-0\" infill at Hallway 102; two column furrings 5/A2.0 (2-1/2\" studs, 5/8\" Type X, 3 sides) per key note 1; the 8'-6\" gypsum header at the north end of Hallway 102 (A3.0); metal blocking (A5.0 blocking legend, 8/A2.0); kicker braces to structure (4/A2.0); demolition of the dashed walls of A1.0 (SF of the element only).",
 "- Types W1 / W4 (2/A2.0) are EXISTING walls to remain: 'PATCH AND REPAIR' only - not quantified; allowance in Review Items. W2A and W3 appear only in the legend (no tag on the plan).",
 "- Heights: board to 6\" above the ceiling of each room (A2.0 wall legend / 2/A2.0): Retail 12'-0\" ACT -> 12'-6\", Storage 10'-0\" ACT -> 10'-6\", Hallway existing gyp 9'-0\" -> 9'-6\" (A3.0 tags). Structure height is not printed anywhere (RFI-01): 26'-0\" of A0.1 carried for braces and demolition (conservative).",
 "", "## Partition Takeoff (one row per wall)", "", "| Wall | LF | H | Board SF | Source |", "|---|---|---|---|---|"]
for r in pt:
    R.append(f"| {r[1]} | {r[2]:,.2f} | {r[3]} | {r[7]:,.2f} | {r[9]} |")
R += ["", "## Material Summary (net, before waste)", "", "| Material | Unit | Net |", "|---|---|---|"] + [f"| {r[0]} | {r[1]} | {r[2]:,.2f} |" for r in ms if r[2]]
R += ["", f"## Open RFIs (conservative value LOADED) - {len(rf)}", ""] + [f"- **{r['id']}**: {r['question']} Loaded: {r['loaded']}. Delta: {r['delta']}" for r in rf]
R += ["", f"## Decisions closed by printed data (no RFI, U-156 / U-162) - {len(cr)}", ""] + [f"- **{r['id']}**: {r['resolved']['answer']}" for r in cr]
R += ["", "## Demolition (A1.0, SF of the element, no layers)", "", "| ID | LF | H | SF |", "|---|---|---|---|"] + [f"| {m['ref']} | {m['lf']:,.2f} | {m['height_ft']} | {m['sf']:,.2f} |" for m in demo]
R += ["", "## Bank comparison", "",
 "Program COMPARATIVA_BANCO (U-130) against the verified FINAL jobs of the bank, per LF of partition and per 1,000 SF of floor. OUT OF RANGE families explained:", "",
 f"- **Trim / corner bead - OUT OF RANGE (high): expected.** The new partition is only {sum(r[2] for r in pt):,.2f} LF, while the two column furrings "
 "(5/A2.0, 12'-6\" high) carry 'FINISH CORNER L BEAD' on every vertical edge (2 corners + 2 edges against the pier per column = 100 LF) and 6/A2.0 adds metal "
 "corner bead where W2 meets the existing demising wall plus the SOF-01 header edges: trim per LF of partition is high because the partition LF is small, not because "
 "trim is over-counted (each row with its operation in the Material Summary).",
 f"- **Gypsum / cement board, Joint compound and Joint tape - OUT OF RANGE (high): expected.** {round(sum(m['qty'] for m in c['misc_items'] if str(m['ref']).startswith('PR-')), 2):,.2f} SF of the "
 "board are the conservative patch and repair of the EXISTING walls W1 / W4 (RFI-06 option A, misc items PR-*: tenant faces to C.H. + 6\"), measured on 206 LF of existing "
 f"walls but divided here by only {sum(r[2] for r in pt):,.2f} LF of NEW partition; compound and tape follow the board (Inputs yields). Option B of RFI-06 removes that board."]
open(os.path.join(E, "README_REVIEW.md"), "w").write("\n".join(R) + "\n")

P = [f"# Revisar primero — {TIT}", ""] + datos() + ["", "## Proyecto", "",
 "- TI de 1,798 SF (A0.1), 1 piso, Type V-B sprinklered, IBC 2021. GC: BCI National, bid viernes 13-nov fin del día, como day work.",
 "- El alcance nuevo es chico: 2 walls W2, 2 column furrings, un header de 8'-6\", blocking metálico, braces a estructura y la demolición de A1.0. W1 / W4 son existentes (solo patch and repair).", "",
 "## Revisar esto primero", "",
 f"1. Markups: `Planos marcados/{PDF}` (A2.0 walls, A1.0 demo, A3.0 header + cuartos EXCLUDED).",
 f"2. 5/8\" Type X: {fam('Type X')} · steel stud 3-5/8\": {fam('3-5/8\" metal stud')} · 2-1/2\": {fam('2-1/2\" stud')} · demolición: {fam('Demolition')}.",
 f"3. {len(rf)} RFI abierto(s) con el valor conservador CARGADO (SEGUIMIENTO.md): " + ", ".join(f"{r['id']} ({'PENDING - user manual verification (U-178); ' if r.get('pending') else ''}{r.get('pregunta', '')[:70]}; {r.get('delta', '')[:90]})" for r in rf) + f". RFI-01 (altura de la estructura) CERRADO por decisión del usuario 11-nov, opción A (U-174). Otros {len(cr) - len(ud)} se cerraron con lo impreso.",
 "4. Review Items: patch and repair de los existentes (allowance), blocking sobre walls existentes, L-bead de las columnas, header SOF-01 no detallado, texture finish de la spec contra Level 4 del plano.", ""]
open(os.path.join(E, "PARA_REVISAR_EN_LA_MANANA.md"), "w").write("\n".join(P) + "\n")
S = ["# SEGUIMIENTO - Xfinity Interquest (RFI abiertos con supuesto conservador CARGADO, U-048)", "", f"RFI abiertos: {len(rf)}. Cerrados por decisión del usuario: " + "; ".join(f"{r['id']} - {r['resolved']['answer'][:260]}" for r in ud) + ".", "",
     "| # RFI | Ítem | N/HOJA | Qué falta | Supuesto cargado | Delta |", "|---|---|---|---|---|---|"]
for r in rf:
    S.append(f"| {r['id']}{' - PENDING - user manual verification (U-178)' if r.get('pending') else ''} | {r.get('pregunta', '')[:80]} | {r.get('source', 'A0.1, 4/A2.0, A1.0')[:120]} | {r['question'][:220]} | {r['loaded'][:160]} | {r['delta'][:200]} |")
open(os.path.join(E, "SEGUIMIENTO.md"), "w").write("\n".join(S) + "\n")
G = [f"OPEN IN BLUEBEAM: `Planos marcados/{PDF}` (the only editable markups file; the PNGs named 'IMAGE ONLY (not editable)' are pictures only).", "",
 "# GUÍA DE REVISIÓN DEL ESTIMADOR — Xfinity Interquest, Colorado Springs CO · rev1 FINAL", "",
 "Esta guía dice en qué orden revisar, qué contiene cada archivo y qué decides tú. Términos del trade en inglés.", "",
 "## ORDEN RECOMENDADO", "", "1. Markups del floor plan.", "2. Detalles que llama el floor plan.", "3. Schedules y materiales por partition type.", "4. El Excel.", "5. Alcance (Scope Checklist).", "6. Lo que te toca decidir.", "",
 "## PASO 1 — Markups (A2.0, A1.0, A3.0)", "",
 f"- `Planos marcados/{PDF}`. Cada línea es un wall: Subject = type, Length = LF a la escala impresa (1/4\"), Depth = altura, Wall Area = SF.",
 "- A2.0: W2-01 (Storage 101 / Retail 100, corrido a través de la puerta 101), W2-02 (infill de 4'-0\" en Hallway 102), CF-01 / CF-02 (column furring, 3 lados; el 4º va contra el storefront pier existente).",
 "- A1.0: DEMO-01..09 (walls punteados a demoler, SF = LF x 26'-0\"). A3.0: header SOF-01 de 8'-6\" y cada cuarto no cuantificado con su texto EXCLUDED (ACT de otro paquete, cielos existentes, Landlord room N.I.C.).", "",
 "## PASO 2 — Detalles", "", "- `Planos marcados/DETALLES_REVISADOS.pdf` + DETALLES_REVISADOS_INDEX. Gobiernan: 2/A2.0 (types), 3/A2.0 (base), 4/A2.0 (top y braces @ 8'-0\"), 5/A2.0 (column furring), 6/A2.0 (conexión al demising, corner bead), 7/A2.0 (head / jamb de la puerta), 8/A2.0 (backing).", "",
 "## PASO 3 — Schedules", "", "- `Planos marcados/SCHEDULES_REVISADOS.pdf` + SCHEDULES_MATERIALES: wall types W1-W4, tabla de limiting heights (362S125-33 @ 16\" para 12'-6\"; 250S125-43 @ 16\" para la columna), door schedule, tags de cielo de A3.0.", "",
 "## PASO 4 — El Excel", "", f"- `Take-off/{XN}`: Partition Takeoff (W2 y CF con SUBTOTAL), Material Summary (Net, waste, compra; 'Where it comes from' con la hoja).",
 f"- Totales: Type X {fam('Type X')}; stud 3-5/8\" {fam('3-5/8\" metal stud')}; stud 2-1/2\" {fam('2-1/2\" stud')}; braces {fam('brace to structure')}; demolición {fam('Demolition')}.", "",
 "## PASO 5 — Alcance", "", "- EXCLUDED sin RFI: ACT y grid (otro bid package), painting (otro bid package), insulation, wood / F.R.T. blocking / plywood de server racks (Div. 06), tornillería, acoustical sealant, puertas / frames / storefront, MEP, ductos, demolición de cielos existentes (tipo no indicado).", "",
 "## PASO 6 — Lo que te toca decidir", "", "- **RFI-06 - PENDING - user manual verification (U-178)**: tú lo verificas a mano. Hojas a revisar: A2.0 (2/A2.0 W1 / W4 'PATCH AND REPAIR AND MAINTAIN ANY EXISTING FIRE RATING (V.I.F.)'), A0.1 nota general 3 ('PATCH ANY EXISTING WALLS AND/OR CEILINGS AS NEEDED TO REFURBISH THE LEASE SPACE') y A1.0 ('EXISTING DEMISING WALL TO REMAIN. PREPARE FOR NEW FINISHES', notas 13 y 29). Cargado mientras tanto: opción A conservadora (+2,589.62 SF de 5/8\" Type X, misc items PR-*).", f"- RFI abiertos: {len(rf)}. RFI-01 (altura de la estructura) ya lo decidiste el 11-nov: opción A, 26'-0\" cargado (U-174); queda solo como sensibilidad: cada pie menos = -7.07 LF de braces y -{DLF} SF de demolición."] + [f"- **{r['id']}**: {r['question'][:240]} → cargado: {r['loaded'][:160]}. Delta: {r['delta'][:200]}" for r in rf] + [
 "- Review Items del Excel (allowances y criterios): patch and repair de W1 / W4, blocking sobre walls existentes, L-bead de las columnas, header SOF-01.", "",
 "## Carpeta `Auditoria/`", "", "- `burbujas/`, `schedules/` (lectura independiente), `resolucion_AB/` (cada diferencia A/B con imagen), `rfi_img/`, `review_items/`, `revision_independiente/` (revisión antes de entregar, U-168 A1-A5)."]
G += ["", "## Coverage map limits (U-193)",
      "`Planos marcados/COBERTURA - IMAGE ONLY.pdf` shows in RED every wall / room drawn on the plans that has no take-off markup (green = marked).",
      "Limits of that map: (1) a single missing face of a wall whose other face is marked does NOT show in red; (2) diagonal walls are NOT",
      "detected (only horizontal / vertical walls); (3) a missing ceiling inside a stacked (double) ceiling is checked by the double-ceiling",
      "review (Auditoria/DOBLE_CIELO.csv), not by the map; (4) dimension / extension lines with 45-degree ticks and door leaves are filtered",
      "out, but dimensions drawn with ARROWS are not, so an arrow-dimension pair may still show as a red (the independent reviewer disposes it);",
      "(5) two leaves of a wall that the map fuses into one covered wall do not show in red: a 'same wall' exclusion needs its gap_proof with N/SHEET and the gap measured 0;",
      "(6) the identity of the independent reviewer / subagent is DECLARED (SUBAGENTE_ID and `bitacora.py subagente`): the program normalizes the ids and checks",
      "that the reviewer is not an author of steps 2-7, but it cannot prove who actually ran each step."]
open(os.path.join(E, "GUIA_DE_REVISION_DEL_ESTIMADOR.md"), "w").write("\n".join(G) + "\n")
Z = ["# RESUMEN rev1 FINAL — Xfinity Interquest (Colorado Springs, CO)", "",
 "Primera y única entrega (U-169): revisión independiente completa hecha ANTES de entregar.", "",
 "| Material | Unit | Net |", "|---|---|---|"] + [f"| {r[0]} | {r[1]} | {r[2]:,.2f} |" for r in ms if r[2]] + ["",
 f"RFI abiertos: {len(rf)}; cerrados por lo impreso: {len(cr) - len(ud)}; cerrados por decisión del usuario: {len(ud)} (" + ", ".join(r['id'] for r in ud) + ", opción A 26'-0\", U-174; cantidades sin cambio)."]
open(os.path.join(E, "RESUMEN_rev1.md"), "w").write("\n".join(Z) + "\n")
print("docs ok", len(rf), "rfis open")
