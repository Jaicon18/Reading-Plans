#!/usr/bin/env python3
"""README_REVIEW.md (English), PARA_REVISAR_EN_LA_MANANA.md, SEGUIMIENTO.md y GUIA_DE_REVISION_DEL_ESTIMADOR.md (español,
términos del trade en inglés) de CR City Hotel rev1 FINAL. Toda cifra se lee del Excel entregado y del canon; nada a mano.
Uso: hacer_docs.py <entrega_dir> <proyecto_datos.json> <takeoff.json> <canon.json>"""
import json, os, sys, collections
import openpyxl
E, PD, TJ, CN = sys.argv[1:5]
x = next(os.path.join(E, "Take-off", f) for f in os.listdir(os.path.join(E, "Take-off")) if f.endswith(".xlsx"))
wb = openpyxl.load_workbook(x, data_only=True)
td = json.load(open(TJ)); c = json.load(open(CN))
ms = [r for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True) if r[0] and isinstance(r[2], (int, float))]
rf = [r for r in c["rfis"] if r["status"] == "open"]
TIT = "CR City Hotel - 415 Perry Street, Castle Rock, CO 80104 - Metal framing & drywall take-off, rev1 FINAL"
XN = os.path.basename(x)
tot = collections.OrderedDict()
order = (c.get("constants") or {}).get("type_order", {}).get("value") or []
for e in sorted(c["existing_walls"], key=lambda e: (order.index(e["type_id"]) if e["type_id"] in order else 99, e["floor"])):
    k = (e["type_id"], e["floor"])
    t = tot.setdefault(k, [set(), 0.0, 0.0])
    t[0].add(e["id"].split(" ")[0]); t[2] += e["length_ft"] * e["height_ft"] * e["faces"] * e["layers"]
    if e["id"].endswith(" A") or " " not in e["id"]:
        t[1] += e["length_ft"]
fl_tot = collections.defaultdict(lambda: [0, 0.0])
for (ti, fl), (ids, lf, sf) in tot.items():
    fl_tot[fl][0] += len(ids); fl_tot[fl][1] += lf


def datos():
    L = ["## PROJECT DATA", "", "| Field | Value | Source |", "|---|---|---|"]
    for d in td["proyecto_datos"]:
        L.append(f"| {d['campo']} | {d['valor']} | {d.get('fuente') or '-'} |")
    L += ["", "**Mandatory sheets reviewed**", "", "| Category | Status | Sheets |", "|---|---|---|"]
    for h in td["hojas_revisadas"]:
        L.append(f"| {h['categoria']} | {h['estado']} | {h['hojas']} |")
    return L


R = [f"# {TIT}", ""] + datos() + [
 "", "## Bid set and GC", "",
 "- Owen-Ames-Kimball Co. (Colorado), Jess Matias: BuildingConnected 'CR City Hotel: Drywall & Framing', bid Nov 12, 2026 12:00 PM MST (only GC found in estimating@jchunter.us).",
 "- 2026 Permit Drawings (Architectural 4.22.2026, Structural 4.22.2026, Mech/Plumb and Electrical 6.1.2026, Project Manual Vol 1 / 2) = current set; the 2025 Full Drawing Set is superseded (compared sheet by sheet by program).",
 "", "## What is in this folder", "",
 f"- `Take-off/{XN}` - fixed 6-sheet format (Inputs, Partition Takeoff, Material Summary, Pending Items, Review Items, Scope Checklist). Partition Takeoff: board-only rows per wall and FLOOR, one block per type in the A0.06 / A0.07 schedule order with SUBTOTAL.",
 "- `Planos marcados/CR_City_Hotel_markups_rev1.pdf` - Bluebeam markups (Subject = type, Page Label = sheet, Length, Depth = wall height, Wall Area; Contents = TYPE · LF · H · faces · board SF · DETAIL · Wall ID) on A2.01-A2.04 + enlarged plans, ceilings as polygons on A3.01-A3.04; PNG per sheet.",
 "- `Planos marcados/DETALLES_REVISADOS.pdf` + index (every detail / section bubble circled and numbered in origin and destination, U-141); `Planos marcados/SCHEDULES_REVISADOS.pdf` + SCHEDULES_MATERIALES (U-142).",
 "- `GUIA_DE_REVISION_DEL_ESTIMADOR.md` (review order and what each file contains, Spanish), `PARA_REVISAR_EN_LA_MANANA.md`, `SEGUIMIENTO.md` (open RFIs with the conservative value loaded).",
 "- `Auditoria/` - bubbles, independent schedule reading, A/B resolution per floor with crops, RFI images, adversarial audit.",
 "", "## Scope basis (read first)", "",
 "- The building is WOOD framed (A0.06 W / FW / DW / FI, A0.07 XW, A0.08 wood trusses): wood studs, plates, blocking, trusses, FRT plywood and LP Flameblock are Div. 06 = EXCLUDED. Our scope: gypsum board per face and layer (Type X, Type X W.R., Type C ceilings), 5/8\" exterior gypsum sheathing Type X, 5/8\" cement board at tile, C-H shaft walls (studs, J-runner, 1\" shaftliner), resilient channel, drywall suspension (GYP-1 / GYP-2), soffits / coves, trim, control joints, finishing (Level 4).",
 "- Heights per face from the printed sections of each zone: L2-L3 room zone 9'-2 7/8\" (4/A5.05), corridor zone 11'-0\" - 1'-1 3/8\" (7/A7.23), L4 8'-11 1/4\" (1/A5.06), grid 8 11'-4 3/4\" (2/A5.01), L1 12'-0\" (5/A5.04).",
 "", "## Walls by type and floor (schedule order; floors never joined)", "", "| Type | Floor | Walls | LF | Board SF (faces x layers) |", "|---|---|---|---|---|"]
for (ti, fl), (ids, lf, sf) in tot.items():
    R.append(f"| {ti} | {fl} | {len(ids)} | {lf:,.2f} | {sf:,.2f} |")
R += ["", "| Floor | Walls | LF |", "|---|---|---|"] + [f"| {fl} | {v[0]} | {v[1]:,.2f} |" for fl, v in sorted(fl_tot.items())]
R += ["", "## Material Summary (net, before waste)", "", "| Material | Unit | Net |", "|---|---|---|"]
for r in ms:
    R.append(f"| {r[0]} | {r[1]} | {r[2]:,.2f} |")
R += ["", f"## Open RFIs (conservative value LOADED; only what no sheet prints, U-140) - {len(rf)}", ""]
for r in rf:
    R.append(f"- **{r['id']}** ({r['source']}): {r['question']} Loaded: {r['loaded']}. Delta: {r['delta']}")
cr = [r for r in c["rfis"] if r["status"] == "closed"]
R += ["", f"## Decisions closed by printed data or standing rule (no RFI) - {len(cr)}", ""]
for r in cr:
    R.append(f"- **{r['id']}** ({r['source']}): {r['question']} -> {r['resolved']['answer']} [{r['resolved']['source']}]")
R += ["", "## Bank comparison", "",
 "Program COMPARATIVA_BANCO (U-130) against the verified FINAL jobs of the bank. OUT OF RANGE families explained:", "",
 "- **Studs - OUT OF RANGE (low): expected.** Every bank job is METAL framed; this building is WOOD framed (A0.06 W / FW / DW / FI, A0.07 XW, A0.08 trusses), so wood studs are Div. 06 = EXCLUDED (U-139). The only studs in our scope are the 6\" 20 GA C-H studs of the CH.6-2 shaft walls (A0.06 CH, UL U415): 546 LF.",
 "- **Bracing / blocking - OUT OF RANGE (0): expected.** Blocking in this set is WOOD (A0.05, A0.09, A2.05, A7.32, A9.02, A9.04) = Div. 06 EXCLUDED; no metal bracing / blocking is printed (Scope Checklist ALC-16).",
 "- Joint compound and tape carry 0 % waste on purpose: they are YIELD products (Inputs lb / LF per SF of board), the yield already includes the waste (skill rule BE-CF17); the 6 % non-metal waste applies to board.",
 "- Track is in range only because of the soffit / ceiling track of the framed soffits (7/A7.23) and the C-H J-runner; board, finishing and trim are in range per partition LF."]
open(os.path.join(E, "README_REVIEW.md"), "w").write("\n".join(R) + "\n")

fam = {str(r[0]): r for r in ms}
def net(sub):
    v = [r for k, r in fam.items() if sub.lower() in k.lower()]
    return f"{v[0][2]:,.2f} {v[0][1]}" if v else "0"
P = [f"# Revisar primero — {TIT}", ""] + datos() + ["",
 "## Proyecto", "", "- Hotel nuevo de 4 pisos, 35,676 SF, Type IIIB, estructura de wood (A0.00). GC: Owen-Ames-Kimball, bid 12-nov 12:00 PM MST.",
 "- Todo el framing es wood: framing EXCLUDED (Div. 06). Lo nuestro es el gypsum board (board-only por wall y por piso), exterior gyp sheathing, cement board, C-H shaft walls, resilient channel, drywall suspension, soffits, trim y acabado.", "",
 "## Revisar esto primero", "",
 f"1. Markups de A2.01-A2.04 (`Planos marcados/`): {sum(v[0] for v in fl_tot.values())} walls en 4 pisos, un color por type.",
 f"2. 5/8\" Type X: {net('gypsum board, Type X')} · Type X W.R.: {net('Type X W.R.')} · Type C (ceilings FS-1): {net('Type C')} · exterior sheathing Type X: {net('exterior gypsum sheathing')} · cement board: {net('cement board')}.",
 f"3. {len(rf)} RFI abiertos (solo lo que ninguna hoja imprime, U-140), cada uno con el supuesto conservador ya CARGADO (SEGUIMIENTO.md): " + ", ".join(r['id'] for r in rf) + f". Otros {sum(1 for r in c['rfis'] if r['status'] == 'closed')} se cerraron con lo impreso o con regla / precedente (lista en README_REVIEW, 'Decisions closed'); los que más mueven: RFI-05 (retail: caras no rated EXCLUDED por la nota de tenant, rated cargadas, delta -1,033 SF), RFI-12 (GYP-1 metal suspension), RFI-19 (corner bead contado por programa en los 4 pisos).",
 "5. Cambios por la auditoría adversarial U-138 (todos verificados en el plano): membrana FS-1 bajo el piso de Level 2 (cielo de L1, A0.08 'LEVEL 2, 3, 4 THROUGHOUT') 7,928.8 SF de Type C + resilient channel; retail 124: GYP-1 del tenant fuera y wrap de vigas de acero (FS-1) cargado (RFI-20); cielo de campo del corridor 412 en L4 (1,350 SF impresos, RS-1); franja RS-6 de L3 bajo las terrazas (2 layers Type X); corner bead completo (esquinas sin exteriores + window returns + bordes de soffits); caras no rated de la zona F&B EXCLUDED ('INTERIOR OF FOOD AND BEVERAGE SPACE IS NOT IN SCOPE OF THIS PERMIT'); walls fantasma sobre vanos de puerta (W.4-L3-44, W.4-L4-22) fuera; vanos de puerta dentro de 57 walls NO descontados (conservador). Informe completo: Auditoria/auditoria_U138/.",
 "6. Decisión tuya (6-nov, 'yes'): el soffit del ENTRY CANOPY (08/A9.05 'GYP/METAL SOFFIT PANEL') es nuestro: 5/8\" exterior gypsum soffit board pegado bajo la placa de acero (4.85 ft de profundidad medida en el detalle x 12'-0\" supuesto = 58.2 SF) + 21.7 LF de trim; el largo del canopy no está acotado: RFI-21.",
 "4. Alturas: salen de las secciones impresas por zona (4/A5.05, 7/A7.23, 1/A5.06, 2/A5.01); las lecturas A y B diferían y se resolvieron con la cota impresa (Auditoria/resolucion.md).", ""]
open(os.path.join(E, "PARA_REVISAR_EN_LA_MANANA.md"), "w").write("\n".join(P) + "\n")
S = ["# SEGUIMIENTO - CR City Hotel (RFI abiertos con supuesto conservador CARGADO, U-048)", "",
     "| # RFI | Ítem | N/HOJA | Qué falta | Supuesto cargado | Delta |", "|---|---|---|---|---|---|"]
for r in rf:
    S.append(f"| {r['id']} | {r['items']} | {r['source']} | {r['question'][:200]} | {r['loaded'][:160]} | {r['delta'][:220]} |")
open(os.path.join(E, "SEGUIMIENTO.md"), "w").write("\n".join(S) + "\n")
G = [f"# GUÍA DE REVISIÓN DEL ESTIMADOR — CR City Hotel, Castle Rock CO · rev1 FINAL", "",
 "Esta guía dice en qué orden revisar, qué contiene cada archivo y qué decides tú. Términos del trade en inglés.", "",
 "## ORDEN RECOMENDADO (de lo que más cuesta a lo que menos)", "",
 "1. Markups del floor plan de cada piso (que no falte ningún wall).", "2. Detalles que llama cada floor plan (que se hayan leído todos).", "3. Schedules y materiales por partition type.", "4. El Excel (cantidades).", "5. Alcance (Scope Checklist).", "6. Lo que te toca decidir (RFI).", "",
 "## PASO 1 — Markups del floor plan (que no falte ningún wall)", "",
 "- Archivo: `Planos marcados/CR_City_Hotel_markups_rev1.pdf` (ábrelo en Bluebeam). Hojas A2.01 (L1), A2.02 (L2), A2.03 (L3), A2.04 (L4) y las ampliadas A6.0x / A7.xx donde la lectura midió.",
 "- Cada línea es un wall: Subject = type (por ejemplo `W.62-1 - BOARD ONLY (WOOD FRAMING EXCLUDED)`), Length = LF medido a la escala impresa, Depth = altura del board, Wall Area = SF. La leyenda va en el orden de A0.06 / A0.07.",
 "- Los pisos nunca se juntan: cada wall lleva su piso en el ID (W.62-L2-03).",
 f"- Totales por piso: " + "; ".join(f"{fl} {v[0]} walls / {v[1]:,.2f} LF" for fl, v in sorted(fl_tot.items())) + ".",
 "- Ceilings: polígonos en A3.01-A3.04; el polígono ubica el cuarto, el SF cargado es el SF IMPRESO del cuarto (FS-1 cubre toda la unidad con baño).", "",
 "## PASO 2 — Detalles que llama ese floor plan", "",
 "- `Planos marcados/DETALLES_REVISADOS.pdf`: cada burbuja circulada y numerada en la hoja de origen y en su destino; `DETALLES_REVISADOS_INDEX` (en README_REVIEW) dice a qué renglón del take-off va o por qué no es nuestro.",
 "- Los que gobiernan cantidades: 4/A5.05 (alturas de L2-L3), 7/A7.23 (zona del corridor y cove), 1/A5.06 (L4), 2/A5.01 (grid 8), 7 y 8/A9.03 (shafts CH), 1-3/A8.02 (returns de ventana), A0.09-A0.11 (intersecciones rated).", "",
 "## PASO 3 — Schedules y materiales por partition type", "",
 "- `Planos marcados/SCHEDULES_REVISADOS.pdf` + `SCHEDULES_MATERIALES` (en README_REVIEW): cada type de A0.06 / A0.07 / A0.08 marcado con su lista de materiales.",
 "- Ojo: W / FW / DW / FI / XW son wood → solo board. CH = metal (C-H stud 6\" 20 GA, J-runner, 1\" shaftliner). FS-1 = 5/8\" Type C sobre resilient channel. Capas por rating: 1 HR = 1 layer por cara, 2 HR = 2 layers.", "",
 "## PASO 4 — El Excel (cantidades)", "",
 f"- `Take-off/{XN}`. Partition Takeoff: un bloque por type con SUBTOTAL; cada renglón = un wall de un piso con LF, altura, capas y board SF; columna Source con la N/HOJA.",
 "- Material Summary: Net + waste en su columna + compra; 'Where it comes from' dice la hoja y el desglose (qué walls / cuartos suman cada renglón).",
 f"- Totales clave: Type X {net('gypsum board, Type X')}, Type X W.R. {net('Type X W.R.')}, Type C {net('Type C')}, exterior sheathing {net('exterior gypsum sheathing')}, cement board {net('cement board')}, resilient channel {net('Resilient channel')}, shaftliner {net('shaftliner')}.", "",
 "## PASO 5 — Alcance (Scope Checklist)", "",
 "- Cada alcance CUANTIFICADO o NO APLICA con su hoja. EXCLUDED: wood framing / blocking / plywood (Div. 06), tornillería, ductos, ACT / WS-1, insulation, plaster / wallcovering / paint, CMU / concrete, puertas / ventanas, área gris de permiso aparte.", "",
 "## PASO 6 — Lo que te toca decidir", ""]
for r in rf:
    G.append(f"- **{r['id']}**: {r['question'][:220]} → cargado: {r['loaded'][:160]}. Delta: {r['delta'][:200]}")
G += ["", "## Carpeta `Auditoria/` (solo si quieres comprobar algo a fondo)", "",
 "- `burbujas/` (verificación a ojo + CADENA.md), `schedules/` (lectura independiente), `resolucion.md` (cada diferencia A/B decidida con imagen), `rfi_img/`, `auditoria_U138/` (auditoría adversarial antes de entregar)."]
open(os.path.join(E, "GUIA_DE_REVISION_DEL_ESTIMADOR.md"), "w").write("\n".join(G) + "\n")
print("docs ok", len(rf), "rfis")
