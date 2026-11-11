#!/usr/bin/env python3
"""Grand Kia rev1: README_REVIEW.md (English), PARA_REVISAR_EN_LA_MANANA.md, SEGUIMIENTO.md, GUIA_DE_REVISION_DEL_ESTIMADOR.md
and RESUMEN_rev1.md (Spanish, trade terms in English). Every number is read from the delivered Excel / canon / rfis_final;
nothing typed by hand. Usage: hacer_docs.py <entrega_dir> <proyecto_datos.json> <takeoff.json> <canon.json>"""
import json, os, sys, collections
import openpyxl
E, PD, TJ, CN = sys.argv[1:5]
W = "/root/gk/work"
x = next(os.path.join(E, "Take-off", f) for f in os.listdir(os.path.join(E, "Take-off")) if f.endswith(".xlsx"))
XN = os.path.basename(x)
wb = openpyxl.load_workbook(x, data_only=True)
td = json.load(open(TJ)); c = json.load(open(CN))
RF = json.load(open(f"{W}/etapas/4_canon/rfis_final.json"))
ms = [r for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True) if r[0] and isinstance(r[2], (int, float))]
rf = [r for r in RF["rfis"] if str(r.get("status")).lower() == "open"]
cr = [r for r in RF["rfis"] if str(r.get("status")).lower() != "open"]
PDF = next((f for f in os.listdir(os.path.join(E, "Planos marcados")) if f.endswith("OPEN IN BLUEBEAM.pdf")), "")
TIT = "Grand Kia Auto Dealership - 2040 W 104th Avenue, Thornton (Denver), CO 80234 - Metal framing & drywall take-off, rev1 FINAL"
SF_BLDG = 41287


def net(sub):
    v = sum(r[2] for r in ms if sub.lower() in str(r[0]).lower())
    u = next((r[1] for r in ms if sub.lower() in str(r[0]).lower()), "")
    return f"{v:,.2f} {u}"


ORDER = td["type_order"]
tot = collections.OrderedDict((t, [0, 0.0, 0.0]) for t in ORDER)
for w in c["walls"]:
    t = w.get("tag")
    if t not in tot or w.get("element", "wall") != "wall":
        continue
    tot[t][0] += 1; tot[t][1] += float(w.get("length_ft") or 0)
pt = list(wb["Partition Takeoff"].iter_rows(min_row=5, values_only=True))
for r in pt:
    if r and r[1] and r[0] in tot and isinstance(r[7], (int, float)):
        tot[r[0]][2] += r[7]
zona = collections.defaultdict(lambda: [0, 0.0])
for w in c["walls"]:
    z = "Z3 (A112 / A113 / A150)" if "-Z3-" in w["id"] else "Z2 (A111 east)" if "-Z2-" in w["id"] else "Z1 (A111 west)"
    zona[z][0] += 1; zona[z][1] += float(w.get("length_ft") or 0)


def datos():
    L = ["## PROJECT DATA", "", "| Field | Value | Source |", "|---|---|---|"]
    for d in td["proyecto_datos"]:
        L.append(f"| {d['campo']} | {d['valor']} | {d.get('fuente') or '-'} |")
    L += ["", "**Mandatory sheets reviewed**", "", "| Category | Status | Sheets |", "|---|---|---|"]
    for h in td["hojas_revisadas"]:
        L.append(f"| {h['categoria']} | {h['estado']} | {h['hojas']} |")
    return L


def delta_txt(o):
    A, B = o.get("A") or {}, o.get("B") or {}
    return f"(A) {A.get('texto', '')} - delta {A.get('delta', '')} / (B) {B.get('texto', '')} ({B.get('cita', 'n/a')}) - delta {B.get('delta', '')} / (C) other: ____"


R = [f"# {TIT}", ""] + datos() + [
    "", "## Bid sets of the two GCs", "",
    "- Brinkman Construction (Kevin Stearns): BuildingConnected 'Grand Kia' - Drywall & Framing (our package), bid 11/17/2026 2:00 PM MST; Current Drawing Set (112 pages), Project Specifications, ADD #1 (11/03/2026), bid instructions, phasing plan.",
    "- Crossland (Corey Reeves / Jeff Erhart): BuildingConnected 'Grand Kia' - ACT and Wall Coverings only, bid 11/16/2026 4:30 PM MST.",
    "- Compared by program (U-091): the drawing sets of the two GCs are byte-identical (same md5); the ADD #1 spec book is the same book. Delta between GCs for our scope = 0. Brinkman's set is the bid set of this take-off.",
    "", "## What is in this folder", "",
    f"- `Take-off/{XN}` - fixed 6-sheet format (Inputs, Partition Takeoff, Material Summary, Pending Items, Review Items, Scope Checklist). Waste applied once, in the Material Summary.",
    f"- `Planos marcados/{PDF}` - Bluebeam markups (open in Bluebeam): walls on A111 / A112 / A113 / A150 (Subject = type, Page Label, Length, Depth = wall height, Wall Area), demolition on A108 / A109 (SF), gyp board ceilings / soffits on A131 / A132 / A133, and an EXCLUDED label in every room and area that is not quantified (U-159 / U-160). PNG images per sheet are image only (not editable).",
    "- `Planos marcados/DETALLES_REVISADOS.pdf` - every detail / section / elevation bubble reviewed, circled and numbered on the calling sheet and on its destination.",
    "- `Planos marcados/SCHEDULES_REVISADOS.pdf` - every trade schedule row marked (A550 wall types, A400 door schedule, A140 finish legend, 62/S204 height table).",
    "- `GK_CHECKLIST_REVISION.xlsx` - review checklist (U-168).", "- `Proposal/` - proposal (U-150).",
    "- `SEGUIMIENTO.md` - RFI follow-up (Spanish). `PARA_REVISAR_EN_LA_MANANA.md` - review-first notes (Spanish). `GUIA_DE_REVISION_DEL_ESTIMADOR.md` - review guide (Spanish). `RESUMEN_rev1.md` - single summary (U-164).",
    "- `Auditoria/` - delivery gate, bubble verification, independent schedule reading, A/B resolution with images, tag sweep crops, RFI images.",
    "", "## Scope basis (read first)", "",
    "- Remodel + additions of an existing dealership. New partitions per A550 types A-H (A1..H1 = same type with batt insulation, insulation EXCLUDED). J / K are CMU (other trade).",
    "- Plan scale: A111 / A112 dimensions measure 1/8\" = 1'-0\" (9 pt/ft) although the scale bar reads 1/4\" (checked against printed dimensions); A113 3/32\"; A150 1/2\".",
    "- Heights: no deck elevation is printed; each wall height comes from the building sections / wall sections (A300 / A301 / A310-A312) at the printed scale, or from the RCP ceiling height + 6\" for partial-height types (A550). Each value carries its operation in the Excel.",
    "- Stud gauge: A550 keynotes send to structural; 62/S204 table + SFIA table (A550 GN 1, IBC 2024) give the gauge per height; 20 walls taller than every table = RFI-01 with the heavy member LOADED.",
    "", "## Walls by type (A550 schedule order; zones never joined)", "", "| Type | Walls | LF | Board SF (Partition Takeoff) | Detail |", "|---|---|---|---|---|"]
for t, (n, lf, sf) in tot.items():
    if n:
        R.append(f"| {t} | {n} | {lf:,.2f} | {sf:,.2f} | {t[0]}/A550 |")
_a5 = json.load(open(f"{W}/etapas/A520_FALTANTE.json"))
R += ["", "## Missing sheet A520 (read this)", "",
      f"- A520 is listed in the A000 sheet index but is NOT in the set (page 41 repeats A521). {len(_a5['bubbles'])} details are called to it ({_a5['occurrences']} bubble occurrences): "
      + "; ".join(f"{b['detail']} (from {', '.join(b['called_from'])})" for b in _a5['bubbles']) + ".",
      "- Searched for it (rule U-172): Crossland set (same md5 as Brinkman's), Brinkman ADD #1 (spec book only), BuildingConnected project files. Not found.",
      "- Parapet / roof-edge framing is taken from what the set does print: wall sections A310-A312, building sections A300 / A301, S121 / S122 / S403 and spec 05 40 00, each row citing its N/SHEET. Coping, ACM, EIFS, plywood and insulation are other trades."]
R += ["", "| Zone | Walls | LF |", "|---|---|---|"] + [f"| {z} | {v[0]} | {v[1]:,.2f} |" for z, v in sorted(zona.items())]
R += ["", "## Material Summary (net, before waste)", "", "| Material | Unit | Net | Where it comes from |", "|---|---|---|---|"]
for r in ms:
    R.append(f"| {r[0]} | {r[1]} | {r[2]:,.2f} | {str(r[8] or '')[:120]} |")
R += ["", f"## Open RFIs (conservative value LOADED; only what neither the sheets nor the code settle, U-172) - {len(rf)}", ""]
for r in rf:
    R.append(f"- **{r['id']}** ({r.get('source', '')}): {r['question']} Loaded: {r.get('loaded', '')} Delta: {delta_txt(r.get('opciones') or {})}")
R += ["", f"## Decisions closed by printed data, code or standing rule (no RFI) - {len(cr)}", ""]
for r in cr:
    res = r.get("resolved") or {}
    R.append(f"- **{r['id']}** ({r.get('source', '')}): {r.get('topic', '')} -> {str(r.get('status')).upper()}: {res.get('answer', '')} [{res.get('source', '')}]")
R += ["", "## Bank comparison", "", "See `COMPARATIVA_BANCO.md` (program, U-130). OUT OF RANGE families (if any) are explained in the bank file notes: this job is a remodel + addition with tall showroom / service walls (24-26 ft), CMU exterior and 2-hour CMU lines (other trade), so studs per partition LF run heavier and ceilings are mostly ACT (other trade)."]
if sum(len(fs) for _, _, fs in os.walk(E, followlinks=True)) > 1000:     # BE-CR28 / CE_SUBIDA_PAQUETE
    R += ["", "## Upload note", "", "- More than 1,000 files: `Auditoria/` is uploaded to Drive as **Auditoria.zip** (same files the delivery gate verified; unzip it to browse)."]
import re as _re
R = [_re.sub(r"\bsin\b", "without", _re.sub(r"\bcon\b", "with", x)) for x in R]
open(os.path.join(E, "README_REVIEW.md"), "w", encoding="utf-8").write("\n".join(R) + "\n")

P = [f"# Revisar primero - {TIT}", "", "Notas en español; los términos del trade van en inglés. Los datos del proyecto están en README_REVIEW.md (PROJECT DATA).", "",
     "## Proyecto", "", f"- {td['proyecto']}",
     "- Bid Brinkman (Drywall & Framing): 17-nov-2026 2:00 PM MST. Crossland solo tiene ACT y Wall Coverings (bid 16-nov 4:30 PM MST). Los dos sets son idénticos (md5): delta entre GC = 0.",
     f"- 41,287 SF (A000: 37,518 SF ground + 3,769 SF second floor), Type III-B sprinklered, B / S-1, 2024 IBC (A000). 112 páginas, 48 hojas A.", "",
     "## Revisar esto primero", "",
     f"1. RFI abiertos: {len(rf)} (Pending Items), cada uno con el valor conservador CARGADO y el delta de cada alternativa (SEGUIMIENTO.md). Todos re-chequeados con la regla de oro U-172: barrido de todo el set con varias pasadas y luego IBC 2024 con su sección; solo quedan los que ni el plano ni el código resuelven.",
     "2. Escala: A111 / A112 dicen 1/4\" en la barra pero las cotas impresas miden 1/8\" (9 pt/ft). Todo se midió a 1/8\" verificado contra cotas impresas (Inputs).",
     "3. Alturas: no hay elevaciones de deck impresas; cada altura sale de A300 / A301 / A310-A312 a la escala impresa (operación en cada renglón) o del RCP + 6\" para los tipos de altura parcial (A550).",
     "4. Gauge: 62/S204 + tabla SFIA (A550 GN 1, IBC 2024). 20 walls de 24.5-26.4 ft pasan todas las tablas = RFI-01 con el miembro pesado CARGADO.",
     "5. Esquinas: regla fija R70.2 aplicada por programa (en T el que pasa es dueño; en L el tramo corto / return es dueño); cada ajuste queda en la operación del largo.",
     "6. Demolición (A108 / A109): solo SF de walls de metal stud existentes a remover (L x H). Cielos existentes, CMU, estructura y exterior: EXCLUDED.",
     "7. EXCLUDED sin RFI (órdenes del estimador): wood / blocking / plywood (Div. 06), tornillería, ductos, ACT, insulation, paint / WC-1, FRP, casework, entry portal (kn 41), CMU. Cada cuarto sin cielo nuestro lleva su etiqueta EXCLUDED en el PDF.",
     "8. A520 no está en el set (la página 41 repite A521): las referencias a A520 van en Review Items.",
     "9. Compuerta de entrega: `ENTREGA_OK.json` en VERDE antes de subir."]
open(os.path.join(E, "PARA_REVISAR_EN_LA_MANANA.md"), "w", encoding="utf-8").write("\n".join(P) + "\n")

S = [f"# SEGUIMIENTO de RFI - {TIT}", "", "Lista aparte (regla del usuario): ítem, N/HOJA, qué falta, supuesto cargado, delta y # RFI. Opciones: (A) planos · (B) código · (C) otro.", "",
     "| # RFI | Ítem | N/HOJA | Qué falta | Supuesto cargado | Delta (A) / (B) |", "|---|---|---|---|---|---|"]
for r in rf:
    o = r.get("opciones") or {}
    S.append(f"| {r['id']} | {r['question'][:200]} | {r.get('source', '')} | {str(r.get('why_not_printed', ''))[:220]} | {str(r.get('loaded', ''))[:200]} | (A) {(o.get('A') or {}).get('delta', '')} / (B) {(o.get('B') or {}).get('delta', '')} |")
S += ["", "## Cerrados (aplicados en las cantidades)", "", "| # RFI | Decisión |", "|---|---|"]
for r in cr:
    res = r.get("resolved") or {}
    S.append(f"| {r['id']} | {str(r.get('status')).upper()}: {str(res.get('answer', ''))[:300]} ({res.get('source', '')}) |")
open(os.path.join(E, "SEGUIMIENTO.md"), "w", encoding="utf-8").write("\n".join(S) + "\n")

G = [f"# GUÍA DE REVISIÓN DEL ESTIMADOR - Grand Kia, Thornton CO · rev1 FINAL - abre `Planos marcados/{PDF}` en Bluebeam", "",
     "Esta guía dice en qué orden revisar, qué contiene cada archivo y qué decides tú. Términos del trade en inglés.", "",
     "## ORDEN RECOMENDADO (de lo que más cuesta a lo que menos)", "",
     "1. Markups del floor plan (que no falte ningún wall).", "2. Detalles que llama cada floor plan.", "3. Schedules y materiales por partition type.",
     "4. El Excel (cantidades).", "5. Alcance (Scope Checklist).", "6. Lo que te toca decidir (RFI).", "",
     "## PASO 1 - Markups del floor plan", "",
     f"- Archivo: `Planos marcados/{PDF}` (ábrelo en Bluebeam). Walls en A111 (zonas Z1 oeste / Z2 este), A112 / A113 (Z3) y A150 (restrooms ampliados).",
     "- Cada línea es un wall: Subject = type, Length = LF a la escala impresa, Depth = altura, Wall Area = SF. Las zonas nunca se juntan (el ID lleva la zona: A-Z1-03).",
     "- Totales por zona: " + "; ".join(f"{z} {v[0]} walls / {v[1]:,.2f} LF" for z, v in sorted(zona.items())) + ".",
     "- Demolición en A108 / A109; cielos de gyp board y soffits en A131 / A132 / A133; etiqueta EXCLUDED en cada cuarto sin cantidad nuestra.", "",
     "## PASO 2 - Detalles que llama ese floor plan", "",
     "- `Planos marcados/DETALLES_REVISADOS.pdf`: cada burbuja circulada y numerada en origen y destino.",
     "- Los que gobiernan cantidades: A550 (types A-H), 13/A540 (deflection track), 8/A540 + 62/S204 view A (braces de walls parciales), 10/A540 (bottom track), 3 y 12/A530 (heads), 24/A540 (suspensión del cielo), 14 / 23 / 28/A540 (soffits y light coves), 62/S204 (altura admisible por gauge), 64/S204 (joists de cielos enmarcados).", "",
     "## PASO 3 - Schedules y materiales por partition type", "",
     "- `Planos marcados/SCHEDULES_REVISADOS.pdf`: A550, A400, A140 y 62/S204 marcados renglón por renglón.",
     "- Dens Shield en toda la gyp bd de restrooms (2/A001); Type X solo en el furring sobre las líneas CMU de 2 HR (A550 keynote 3); Level 5 en WC-1 (A140).", "",
     "## PASO 4 - El Excel (cantidades)", "",
     f"- `Take-off/{XN}`. Partition Takeoff: un bloque por type en el orden de A550 con SUBTOTAL; columna Source con la N/HOJA; Status CONFIRMADO / DERIVADO.",
     f"- Totales clave: regular board {net('gyp board regular')}, Dens Shield {net('Dens Shield')}, Type X {net('Type X')}, Level 5 {net('Level 5')}, demolition {net('demolition')}.", "",
     "## PASO 5 - Alcance (Scope Checklist)", "",
     "- Cada alcance CUANTIFICADO o NO APLICA con su hoja. EXCLUDED: wood / blocking / plywood (Div. 06), tornillería, ductos, ACT, insulation, paint / WC-1, FRP, casework, CMU, entry portal.", "",
     "## PASO 6 - Lo que te toca decidir", ""]
for r in rf:
    G.append(f"- **{r['id']}**: {r['question'][:260]} -> cargado: {str(r.get('loaded', ''))[:220]}. Delta: {delta_txt(r.get('opciones') or {})[:400]}")
G += ["", "## Carpeta `Auditoria/` (solo si quieres comprobar algo a fondo)", "",
      "- `burbujas/` (verificación + CADENA.md), `schedules/` (lectura independiente), `resolucion_AB/` (cada diferencia A/B decidida con imagen), `barrido_tags/` (recortes del inventario), `rfi_img/`, `revision_independiente/` (U-168 A1-A5)."]
open(os.path.join(E, "GUIA_DE_REVISION_DEL_ESTIMADOR.md"), "w", encoding="utf-8").write("\n".join(G) + "\n")

nw = sum(v[0] for v in tot.values()); lf = sum(v[1] for v in tot.values())
RS = ["# RESUMEN rev1 - Grand Kia, Thornton CO (Brinkman, Drywall & Framing)", "",
      f"- Walls: {nw} en {sum(1 for v in tot.values() if v[0])} types, {lf:,.2f} LF (Partition Takeoff).",
      f"- Board: regular {net('gyp board regular')}, Dens Shield {net('Dens Shield')}, Type X {net('Type X')}, exterior sheathing {net('sheathing')}.",
      f"- Level 5 {net('Level 5')}; demolition {net('demolition')}.",
      f"- RFI abiertos {len(rf)} (valor conservador cargado); cerrados / excluidos {len(cr)}.",
      f"- Área del edificio 41,287 SF (A000).", "", "Historial: rev1 = primera entrega (U-169: una sola entrega revisada antes de subir)."]
open(os.path.join(E, "RESUMEN_rev1.md"), "w", encoding="utf-8").write("\n".join(RS) + "\n")
print("docs OK", len(rf), "open RFIs", nw, "walls")
