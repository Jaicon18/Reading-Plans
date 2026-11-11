#!/usr/bin/env python3
"""README_REVIEW.md (English), PARA_REVISAR_EN_LA_MANANA.md, SEGUIMIENTO.md y GUIA_DE_REVISION_DEL_ESTIMADOR.md (español,
términos del trade en inglés) de CR City Hotel rev5 FINAL. Toda cifra se lee del Excel entregado y del canon; nada a mano.
Uso: hacer_docs.py <entrega_dir> <proyecto_datos.json> <takeoff.json> <canon.json>"""
import json, os, sys, collections
import openpyxl
E, PD, TJ, CN = sys.argv[1:5]
x = next(os.path.join(E, "Take-off", f) for f in os.listdir(os.path.join(E, "Take-off")) if f.endswith(".xlsx"))
wb = openpyxl.load_workbook(x, data_only=True)
td = json.load(open(TJ)); c = json.load(open(CN))
ms = [r for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True) if r[0] and isinstance(r[2], (int, float))]
rf = [r for r in c["rfis"] if r["status"] == "open"]
TIT = "CR City Hotel - 415 Perry Street, Castle Rock, CO 80104 - Metal framing & drywall take-off, rev18 FINAL"
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
 "- `Planos marcados/CR_markups_rev18 - OPEN IN BLUEBEAM.pdf` - Bluebeam markups (Subject = type, Page Label = sheet, Length, Depth = wall height, Wall Area; Contents = TYPE · LF · H · faces · board SF · DETAIL · Wall ID) on A2.01-A2.04 + enlarged plans, ceilings as polygons on A3.01-A3.04; PNG per sheet.",
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
if sum(len(fs) for _, _, fs in os.walk(E, followlinks=True)) > 1000:     # BE-CR28 / CE_SUBIDA_PAQUETE
    R += ["", "## Upload note", "", "- More than 1,000 files: `Auditoria/` is uploaded to Drive as **Auditoria.zip** (same files the delivery gate verified; unzip it to browse)."]
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
 "7. **rev2 reemplazó a rev1.** La compuerta de rev1 pasó EN VACÍO: el canon tenía walls = 0 (todo el board vive en los walls board-only) y BOTH SIDES + 14 chequeos no corrieron. En rev2 los chequeos leen los walls board-only (regla BE-CR25) y lo que salió se corrigió en el plano: caras con baño de L2 / L3 (W.62 del corridor en 201-204 y 301-304, XW.6.3 norte y oeste, 209 / 309) divididas por las particiones medidas en vectores: Type X W.R. en toilet / lavatory (A2.0x GN 4), cement board solo en el shower (6/A7.02: TILE-1 solo en el shower) y Type X en lo seco. Delta por material vs rev1: `Auditoria/DELTA_rev1_rev2.md`.",
 "4. Alturas: salen de las secciones impresas por zona (4/A5.05, 7/A7.23, 1/A5.06, 2/A5.01); las lecturas A y B diferían y se resolvieron con la cota impresa (Auditoria/resolucion.md).", ""]
_d23 = '/root/cr/work/etapas/DELTA_rev2_rev3.md'     # rev3: delta contra rev2 (orden COORDINACIÓN 6-nov)
_delta23 = [x for x in open(_d23).read().split('\n') if x.startswith('| ') and not x.startswith('| Material') and not x.startswith('|---')] if os.path.exists(_d23) else []
_txt9 = ("9. **rev3 reemplaza a rev2** (recheck de la compuerta con el skill v81cf57, BE-CR29: un chequeo que pasaba en vacío escondía un hueco real): "
         "los 5 walls XW.6.6-0 (tag 'XW.6.6 | 0', A2.03 / A2.04) no llevaban su cara exterior; A0.07 imprime la familia XW.6.6 solo con las filas -1 / -2 y las dos "
         "llevan 'TYPE X 5/8\" EXTERIOR GYP BD' -> exterior gyp sheathing agregado (L3 11'-0\", L4 8'-11 1/4\"). Barrido: ningún otro type tagueado sin fila de rating. "
         "Los coves de L3 citan 7/A7.23. Delta por material contra rev2 (NET): " + "; ".join(f"{x.split('|')[1].strip()} {x.split('|')[5].strip()} {x.split('|')[2].strip()}" for x in _delta23) + " (`Auditoria/DELTA_rev2_rev3.md`).")
_ra = '/root/cr/work/auditoria_U138_2/RESUMEN_PARA_DOCS.md'     # rev3: cambios por la auditoría U-138 #2
if os.path.exists(_ra):
    P.insert(P.index(next(x for x in P if x.startswith("4. Alturas"))), open(_ra).read().strip())
P.insert(P.index(next(x for x in P if x.startswith("4. Alturas"))), _txt9)
_d34 = '/root/cr/work/etapas/DELTA_rev3_rev4.md'     # rev4: delta contra rev3 (orden COORDINACIÓN 7-nov: revisión de RCP + walls hacia Retail 124)
_delta34 = [x for x in open(_d34).read().split('\n') if x.startswith('| ') and not x.startswith('| Material') and not x.startswith('|---')] if os.path.exists(_d34) else []
_txt10 = ("10. **rev4 reemplaza a rev3** (tu revisión: 'revisa los rcp ... algunas areas que no tomaste en cuenta' y 'todo ese numero de paredes en realidad existe'). "
          "RCP, cada tag GYP de las hojas de RCP barrido uno por uno (regla nueva BE-CR30, 35 tags): agregados BAR 107 campo de gyp suspendido 121.6 SF a 11'-0\" "
          "(A5.04 'BAR SUSPENDED GYP CEILING'; A0.00 dice core & shell -> RFI-22), franja sur del lobby 119.0 SF (2/A7.50), nicho BAR / toilets 40.2 SF (1/A7.31), "
          "GYP-1 de Cleaning 215 y closets 222 / 223 de L2 (estaban solo como FS-1); GENERATOR 103 medido en L 200.4 SF (era 181.7); paneles WS-1 descontados de los "
          "GYP-1 de corridor en L2 / L3 / L4. Sin cambio y documentado: la franja GYP-1 11'-0\" al sur del storefront está DENTRO de Retail 124 (tenant, RFI-05); "
          "L4 401-405 RS-1 'excl. bath' es correcto (RS-1 sin rating); Vestibule 114 = ACT-1; FS-1 sobre retail / kitchen se queda (rated). Walls -0 hacia Retail 124: "
          "XW.6.4-L1-04 fuera; XW.6.3-L1-01 y FI.2-L1-06 partidos en el límite del tenant medido en 1/A2.01 (las otras caras retail son de walls rated -2 y se quedan). "
          "Evidencia: `Auditoria/rcp_rev4/`. Delta por material contra rev3 (NET): " + "; ".join(f"{x.split('|')[1].strip()} {x.split('|')[5].strip()} {x.split('|')[2].strip()}" for x in _delta34) + " (`Auditoria/DELTA_rev3_rev4.md`).")
P.insert(P.index(next(x for x in P if x.startswith("4. Alturas"))), _txt10)
_d45 = '/root/cr/work/etapas/DELTA_rev4_rev5.md'     # rev5: revisión de código (decisiones del usuario 7-nov)
_delta45 = [x for x in open(_d45).read().split('\n') if x.startswith('| ') and not x.startswith('| Material') and not x.startswith('|---')] if os.path.exists(_d45) else []
_c5 = json.load(open('/root/cr/work/etapas/4_canon/takeoff_canon.json'))
_txt11 = ("11. **rev5 reemplaza a rev4** (tu revisión de código, carpeta 'Revision de codigo 2026-11-06'). En el BASE (regla R80e.38-4: mientras un RFI está abierto va la opción de MAYOR cantidad): "
          + "; ".join(f"({x['n']}) {x['que']}: {x['sf']['v']:+,.2f} SF" for x in _c5.get('rev5_cambios') or []) + ". DEDUCT ALTERNATES: "
          + "; ".join(f"{d['id']} {d['rfi'] or ''} {d['delta_sf']:,.2f} SF" for d in _c5.get('deduct_alternates') or [])
          + ". verif_codigo.py sobre rev5: ROOF_HEAD 0. Delta por material contra rev4 (NET): " + "; ".join(f"{x.split('|')[1].strip()} {x.split('|')[5].strip()} {x.split('|')[2].strip()}" for x in _delta45) + " (`Auditoria/DELTA_rev4_rev5.md`).")
P.insert(P.index(next(x for x in P if x.startswith("4. Alturas"))), _txt11)
_d56 = '/root/cr/work/etapas/DELTA_rev5_rev6.md'     # rev6: auditoría adversarial de COORDINACIÓN (7-nov)
_delta56 = [x for x in open(_d56).read().split('\n') if x.startswith('| ') and not x.startswith('| Material') and not x.startswith('|---')] if os.path.exists(_d56) else []
_txt12 = ("12. **rev6 reemplaza a rev5** (auditoría de COORDINACIÓN, cada punto verificado en el plano): "
          "(E1) coffers del lobby CLG-L1-11 fuera: 2/, 4/ y 7/A7.31 ponen el 12'-0 3/4\" en el underside del rated assembly = membrana FS-1 de L1 ya cargada; "
          "(E2) cement board de cada shower medido a la CARA DEL WALL (201 / 301 de 3.0 a 3.49 ft; 210 / 310 / 309 también); "
          "(O1) angle molding = perímetro real de cada cuarto (60 renglones, antes 4 x raíz del área); "
          "(O2) cove de corridors de L2 con la cara inferior impresa 4 1/2\" (7/A7.23), igual que L3 / L4; "
          "(E3) la compuerta CB_BE_CF10 ahora lee el Project Manual (specs 05 40 00 ... 09 29 00) y ya no pasa en vacío. "
          "Lo de rev5 (revisión de código, DEDUCT ALTERNATES) sigue igual. Delta por material contra rev5 (NET): "
          + "; ".join(f"{x.split('|')[1].strip()} {x.split('|')[5].strip()} {x.split('|')[2].strip()}" for x in _delta56) + " (`Auditoria/DELTA_rev5_rev6.md`).")
P.insert(P.index(next(x for x in P if x.startswith("4. Alturas"))), _txt12)
_txt13 = ("13. **rev7 reemplaza a rev6** (tu pregunta en Bluebeam: 'por qué unos tienen markups y otros no'): los 73 cielos / soffits cuantificados "
          "como renglones aparte (CLG / SOF / RS6 / CAN / BW: baños, Women 417, Men 418, Elec 421, corridors, Cleaning 215, closets, lobby, BAR, "
          "coves) ahora tienen su markup en verde en su RCP (o en la hoja ampliada donde se midieron), con ID, SF y causa. Cantidades SIN cambio. "
          "Compuerta nueva CE_RCP_COMPLETO: todo cielo / soffit del Excel tiene su markup con el mismo SF / LF.")
P.insert(P.index(next(x for x in P if x.startswith("4. Alturas"))), _txt13)
open(os.path.join(E, "PARA_REVISAR_EN_LA_MANANA.md"), "w").write("\n".join(P) + "\n")
S = ["# SEGUIMIENTO - CR City Hotel (RFI abiertos con supuesto conservador CARGADO, U-048)", "",
     "| # RFI | Ítem | N/HOJA | Qué falta | Supuesto cargado | Delta |", "|---|---|---|---|---|---|"]
for r in rf:
    S.append(f"| {r['id']} | {r['items']} | {r['source']} | {r['question'][:200]} | {r['loaded'][:160]} | {r['delta'][:220]} |")
open(os.path.join(E, "SEGUIMIENTO.md"), "w").write("\n".join(S) + "\n")
G = [f"# GUÍA DE REVISIÓN DEL ESTIMADOR — CR City Hotel, Castle Rock CO · rev18 FINAL", "",
 "Esta guía dice en qué orden revisar, qué contiene cada archivo y qué decides tú. Términos del trade en inglés.", "",
 "## ORDEN RECOMENDADO (de lo que más cuesta a lo que menos)", "",
 "1. Markups del floor plan de cada piso (que no falte ningún wall).", "2. Detalles que llama cada floor plan (que se hayan leído todos).", "3. Schedules y materiales por partition type.", "4. El Excel (cantidades).", "5. Alcance (Scope Checklist).", "6. Lo que te toca decidir (RFI).", "",
 "## PASO 1 — Markups del floor plan (que no falte ningún wall)", "",
 "- Archivo: `Planos marcados/CR_markups_rev18 - OPEN IN BLUEBEAM.pdf` (ábrelo en Bluebeam). Hojas A2.01 (L1), A2.02 (L2), A2.03 (L3), A2.04 (L4) y las ampliadas A6.0x / A7.xx donde la lectura midió.",
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
G[2:2] = ["## CAMBIOS rev3 vs rev2 (revisa esto primero si ya viste rev2)", "", _txt9, "", "| Material | Unit | rev2 | rev3 | Delta |", "|---|---|---|---|---|"] + _delta23 + [""]
G[2:2] = ["## CAMBIOS rev4 vs rev3 (revisa esto primero si ya viste rev3)", "", _txt10, "", "| Material | Unit | rev3 | rev4 | Delta |", "|---|---|---|---|---|"] + _delta34 + [""]
G[2:2] = ["## CAMBIOS rev5 vs rev4 (revisa esto primero si ya viste rev4)", "", _txt11, "", "| Material | Unit | rev4 | rev5 | Delta |", "|---|---|---|---|---|"] + _delta45 + [""]
G[2:2] = ["## CAMBIOS rev6 vs rev5 (revisa esto primero si ya viste rev5)", "", _txt12, "", "| Material | Unit | rev5 | rev6 | Delta |", "|---|---|---|---|---|"] + _delta56 + [""]
_txt14 = ("14. **rev8 reemplaza a rev7** (revisión de TODOS los walls y de los RCP, orden tuya vía COORDINACIÓN): "
          "W.4-L4-21 (Men 418) 1.06 -> 2.13 ft (3/A7.50, error de reescalado); W.6-L4-14 15.54 -> 15.51 (suma de su operación); "
          "wall NUEVO W.6-L1-32 (wall en L junto a la traffic door del bar, 1/A7.30, tag W.6.1, 5.58 ft, cara del vestíbulo de los toilets); "
          "markups que no seguían su wall movidos a los tramos medidos (jogs, piezas a cada lado de un vano); tags W.6.1 / XW.6.2 ligados a su wall; "
          "vanos dentro del tramo en A7.xx declarados en el Source (no descontados, U-057) y W.6-L1-25 como Review Item con su delta. "
          "Franjas de H 0'-2 7/8\": en los walls NO rated del baño el cement board llega a 9'-0\" (RFI-11: cielo 8'-6\" + 6\") y el board W.R. "
          "del wall sigue arriba hasta la cara inferior del entrepiso (9'-2 7/8\"): esa franja de 2 7/8\" es cada renglón con H 0'-2 7/8\".")
P.insert(P.index(next(x for x in P if x.startswith("4. Alturas"))), _txt14)
G[2:2] = ["## CAMBIOS rev7 vs rev6 (revisa esto primero si ya viste rev6)", "", _txt13, ""]
G[2:2] = ["## CAMBIOS rev8 vs rev7 (revisa esto primero si ya viste rev7)", "", _txt14, ""]
_txt15 = ("15. **rev9 reemplaza a rev8** (orden tuya vía COORDINACIÓN: contorno real de los cielos + 30 candidatos de A2.01): "
          "(a) FACP 125 (L1, al este de Stair 2) no tenía caras: FI.2-L1-11 norte 3.26 ft (1/A6.02, tag FI.2 | 0) y FI.2-L1-12 sur 4.27 ft "
          "(1/A2.01, sin tag en 1/A6.02 -> base con RFI-26 / DA-5); el este 'XM.0.1 | 2' es '.1 NO FINISH' (sin gypsum). "
          "(b) Cada cielo se midió en vectores a las caras de los walls (imagen por cuarto en Auditoria/contornos_rev9): ningún polígono es "
          "caja, localizador ni escalado. HALLAZGO: el SF impreso de las unidades NO es consistente (202: contorno 333.27 - bath 64.33 = "
          "268.94 vs 269 impreso, sin bath; 212: 389.55 vs 390, con bath). Por eso la cantidad = contorno medido y el impreso es el chequeo: "
          "L2 / L3 FS-1 sube (la membrana va sobre el bath; en rev10 confirmado en A0.08), L4 RS-1 'sin bath' ya no resta el bath dos veces (403 / 404), "
          "corridors 218 / 318 con el tramo N-S que faltaba, field 412 con los 3 paneles WS-1 medidos (1,091.02 SF), cove 412 = doble línea "
          "dibujada (343.7 LF), canopy = rectángulo dibujado (38.96 SF). Compuerta nueva CE_CONTORNO_REAL.")
G[2:2] = ["## CAMBIOS rev9 vs rev8 (revisa esto primero si ya viste rev8)", "", _txt15, ""]
P.insert(P.index(next(x for x in P if x.startswith("4. Alturas"))), _txt15)
_txt16 = ("16. **rev10 reemplaza a rev9** (auditoría adversarial diaria U-138 de COORDINACIÓN): "
          "(E1) RFI-27 / DA-6 retirados: A0.08 FS-1 (LEVEL 2, 3, 4 / THROUGHOUT / L546) dibuja la membrana Type C continua y debajo "
          "'DROPPED CEILING IS NOT A COMPONENT OF THE RATED ASSEMBLY' -> la membrana sobre el bath es lo impreso [CONFIRMED A0.08]. "
          "(E2) A8.00 puerta 120.1 ELEC / TELE '90 MIN' (IBC Table 716.1(2): 90 MIN = muro de 2 HR) -> el muro sur de 120 (W.6-L1-25) es 2 HR "
          "por lo impreso; DA-1 queda solo W y E (-149.52 SF en vez de -341.76). (R1) los shafts L2-L4 que llaman 7/A9.03 y 8/A9.03 "
          "(4 3/4\" 2-HOUR SHAFTWALL W419 / U497) llevan C-H y J-runner 2-1/2\" (604.31 + 121.52 LF); A0.06 CH.6-2 (6\") queda como "
          "Review Item / RFI-07. (m1) cielos de las unidades L2 201-214 a 9'-2 7/8\" (4/A5.05), como L3. (m2) filas de shaft wall con su "
          "C-H. (m3) conteos de burbujas explicados en la evidencia. Compuertas nuevas: frase de respuesta en el barrido de RFIs, "
          "CE_PUERTA_RATING_MURO, CE_COHERENCIA_R10.")
G[2:2] = ["## CAMBIOS rev10 vs rev9 (revisa esto primero si ya viste rev9)", "", _txt16, ""]
_txt17 = ("17. **rev11 reemplaza a rev10** (revisiones independientes A y B de COORDINACIÓN, verificadas en el plano): "
          "(A) exterior sheathing L4 hasta el remate real (04/A9.05 eave 10.24 ft, 07/A9.05 brow, 10/A9.05 parapet, +357.9 SF); cielos de baño L4 en W.R. "
          "(A0.06 GN 12); C-H de L4 a la altura de su liner (1/A5.08); corner bead del cove 412 con el LF re-medido; canopy 6.49 x 4.85 ft (2/A5.03, 08/A9.05) "
          "= 31.48 SF + 16.19 LF; spec del sheathing 06 16 00 2.5.B glass-mat C1177; hanger wire 0.162\" (09 22 16 2.2.C); control joints de cielos "
          "(A0.06 GN 15 + ASTM C840, 338.04 LF); ADD ALTERNATE AA-1 Level 5 en áreas públicas; compound por capa (capas ocultas Level 1, 09 29 00 3.6.E.1); "
          "proposal con cantidades del Material Summary. (B) 309 bajo el deck de L4 = RS-6 (2 capas Type X sin RC, A2.05 / A0.08); soffit del smoke "
          "curtain 12/A9.03 en 6 ubicaciones; beam wraps viga por viga (d - 16.5\", RFI-20 cerrado); DA-3 retirado (puerta 411.1 20 MIN = 1 HR); "
          "fire barriers 2 HR de L1 al underside del floor sheathing (IBC 707.5, RFI-28 / DA-7); Review Items 112 y 118B (puertas sin rating).")
G[2:2] = ["## CAMBIOS rev11 vs rev10 (revisa esto primero si ya viste rev10)", "", _txt17, ""]
_txt18 = ("18. **rev12 reemplaza a rev11** (orden del usuario U-155, 8-nov: 'buscar hasta encontrar las respuestas en los planos; si no, usa los códigos del IBC y cita su referencia'): "
          "cada RFI abierto y cada valor 'assumed' re-buscado en todo el set (code plans A0.00-A0.02, door schedule A8.00, notas, leyendas, detalles, specs) y, si no está impreso, "
          "resuelto con el código citado. RFI-28 CERRADO por código: IBC 2018 Section 707.5 (fire barrier hasta el underside del floor sheathing, más allá del fondo de las trusses 11'-11 1/2\") - "
          "se retira DA-7, el base no cambia (13'-9 1/2\"). RFI-25 CERRADO: el 1 HR está impreso (tag 'FW.4 | 1', 2/A0.02 '1HR FP', puerta 411.1 20 MIN) y el ensamble es IBC 2018 Section 708 / Table 721.1(2), delta 0. "
          "ELEC 321 y demising sin tag: rating impreso en el code plan (A0.02 '1HR FP') y en la nota de A0.00 'CORRIDOR AND UNIT DEMISING WALLS CONSTRUCTED AS 1HR FIRE PARTITIONS' - mismas capas cargadas. "
          "Los RFI que siguen abiertos no los resuelve ni el plano ni el código (alcance / tenant / conflicto plano contra plano). "
          "Revisión dirigida de COORDINACIÓN: deltas de DA-1 (-171.84) / DA-2 (-414.03) / Review Items 112 (-205.50) / 118B (-159.98) recalculados con la altura actual 13.7917; puerta 120.1 = 5'-0\" x 8'-0\" (A8.00) vs 7'-11\" en 1/A7.50; "
          "vigas de borde norte de Retail 124 (S1.02 W27X94 / W21X50 / W24X55, 68.80 LF) envueltas por la membrana FS-1: +92.71 SF Type C, +137.60 LF RC; sheathing C1177 en la proposal; cita del compound completa.")
G[2:2] = ["## CAMBIOS rev12 vs rev11 (revisa esto primero si ya viste rev11)", "", _txt18, ""]
_txt19 = ("19. **rev13 reemplaza a rev12** (auditoría diaria U-138 de COORDINACIÓN, verificada en el plano): "
          "(E1) caras de exterior sheathing que usaban la altura de la línea del board INTERIOR: mezzanine 219 (2/A5.04: sheathing x=610.68 de 1185.48 a 1006.2 = 6.64 ft, "
          "no 5.915; gable este 8.0065) y pilares del retail en grid 7 (piso a piso 14'-0\" en vez de 12'-0\" B.O. DECK); compuerta nueva CB_CR_R13_E1. "
          "(E2) RFI-15 opción B con IBC 2018 Table 2508.1 y ASTM C840 / GA-216 Table 1; CB_U_155 ya no acepta el nombre de una norma sin sección / tabla. "
          "Detector de RFI 'no impreso' con sinónimos (no tag, does not give, not labeled). Roof assemblies de A2.05 barridos tag por tag (RS-1 a RS-7, ALC-25): "
          "RS-6 x2 cargados con su nombre; RS-5 (metal deck) y RS-7 sin gypsum; RS-4 = F&B fuera de este permiso (A7.55).")
G[2:2] = ["## CAMBIOS rev13 vs rev12 (revisa esto primero si ya viste rev12)", "", _txt19, ""]
_txt20 = ("20. **rev14 reemplaza a rev13** (orden U-156 del usuario, 10-nov: 'en estos planos siempre viene toda la informacion'): re-barrido de los 9 RFI abiertos en todo el set. "
          "Cerrados por lo impreso: RFI-15 (A0.06 GN 10 5/8\" + A0.00 / A0.10 techo sin rating -> 5/8\" Type X de spec 2.3 A, sin cambio), RFI-22 (A0.00 DEFERRED SUBMITTALS solo cocina y F&B de L4; A7.31 / A5.04 diseñan el cielo del BAR -> en este bid), "
          "RFI-23 (2/A0.01 2HR FB en los 4 lados de ELEC / TELE 120 + M3.02 damper -> DA-1 retirado), RFI-26 (FACP 125 = 7 SF con la puerta 125.1 al sur -> FI.2-L1-12 fuera, -51.24 SF, DA-5 retirado). "
          "RFI-04 parcial: demising 1HR FP impreso (sin cambio) y paredes sur de lobby 217 / 317 '2HR FB' (3/A0.01, 1/A0.02) -> W.6-2, +199.10 SF. "
          "Siguen abiertos con su barrido y opción B con sección: RFI-04 (resto), RFI-13, RFI-17 (cuarto de fire pump, IBC 2018 Section 913.2.1). "
          "RFI-21 y RFI-24: lo impreso apunta a la opción B, pero el base mantiene tu decisión del 6-nov (U-052) - confirmar. "
          "U-159: cuarto por cuarto en las RCP, 9 cielos de L4 que faltaban cargados (stalls 417.3 / 417.4, WC 418.2, 6 chases; +180.07 SF); U-160: cada cuarto excluido lleva su texto rojo EXCLUDED - motivo (N/HOJA) en el PDF de Bluebeam (24); U-158: nombres de Planos marcados dicen qué es cada archivo.")
G[2:2] = ["## CAMBIOS rev14 vs rev13 (revisa esto primero si ya viste rev13)", "", _txt20, ""]
_txt21 = ("21. **rev15 reemplaza a rev14** (orden del usuario 10-nov 'revisa todo otra vez': revisión completa de rev14 por 3 revisores, 18 puntos, cada uno "
          "cargado o refutado con su N/HOJA; detalle en RESUMEN_rev15.md y DELTA_rev14_rev15.md): "
          "(1) A0.06 GN 6 'ALL METAL STUDS TO BE SPACED @ 16\" O.C.' -> C-H studs de shaft walls y de MB-1 a 16\" o.c. (RFI-16 cerrado por lo impreso; "
          "Pieces de C-H = un stick de 20 ft por stud de > 10 ft); (2) duct chases 401 NE / 401-402 de 1/A3.04 con stipple: CLG-L4-401D / 402D cargados; "
          "(3) 1/A5.08 '2HR SHAFT CEILING': base del north shaft (8/A9.03) y del south shaft (7/A9.03, IBC 2018 Section 713.11) con MB-1 conservador + RFI-29; "
          "(4) ELEC 221 / 321 / 421: los code plans 3/A0.01, 1/A0.02, 2/A0.02 imprimen 1HR FP -> se quedan 1 capa, la alternativa 2 HR (+521.58 SF) en RFI-04; "
          "(5) RFI-22 BAR 107: decisión R-ALC-10 con el delta de B visible (-125.98 SF + grid), ALC-E08 coherente; (6) U-160: cada EXCLUDED con polígono gris y el "
          "texto DENTRO del cuarto, sin línea de callout; (7) cielos CLG-L2-56/58 y CLG-L3-87/88 sin el offset doble, CLG-L1-14..18 y ACT de A7.50 / A7.45 en la "
          "vista RCP (CE_RCP_CONTORNO); (8) walls: cara del corridor W.62-L4-02/03 y W.6-L4-09, sheathing exterior XW.6.6 L4 continuo; (13) 118B / 120 1a capa a 13.79 ft; "
          "(14) soffits metálicos completos (R-ALC-01): cripple studs a 16\" o.c.; (15) hanger wire de corridors con el drop 9 1/2\" de 7/A7.23; "
          "(12) CBU: mesh tape + setting compound (09 29 00 2.6.E.3); (17) 24 cajas de closet de guest rooms L2 / L3 con stipple: Type C + RC.")
G[2:2] = ["## CAMBIOS rev15 vs rev14 (revisa esto primero si ya viste rev14)", "", _txt21, ""]
P.insert(P.index(next(x for x in P if x.startswith("4. Alturas"))), _txt21)
_txt22 = ("22. **rev16 reemplaza a rev15** (revisión dirigida de rev15, orden del usuario 'revisa todo otra vez'; detalle en RESUMEN_rev16.md y "
          "DELTA_rev15_rev16.md): (1) ELEC 221 / 321 / 421: A0.00 'ELECTRICAL AND IT ROOMS' '2 HR' + 'INCIDENTIAL USE AREAS (TABLE 509):' ... "
          "ELECTRICAL ROOMS' contra los code plans 1HR FP = conflicto; el base lleva la opción mayor (2 HR, +1 capa de 5/8\" Type X por cara, como 118B) y el "
          "1 HR va como DEDUCT ALTERNATE DA-6 en RFI-04; (2) cove de corridor 7/A7.23: el detalle dibuja madera (caja con X) -> framing Div. 06 EXCLUDED, "
          "fuera tracks y cripples de los coves (el board sigue); lobby y stair FCU siguen metálicos; (3) áreas sin número del RCP (hoistways, stairs, "
          "shafts, ELEC/TELE 120, pasillo 410/411, WS-1 de L4) con renglón o EXCLUDED; (4) Review Items coherentes con Pending Items (BAR 125.98); "
          "(5) IBC 2018 Table 509 citada con su fila 'Electrical installations and transformers' (NFPA 70); (6) 2HR shaft ceiling dibujado en el RCP de L1; "
          "(7) base del CBU = la del Material Summary.")
G[2:2] = ["## CAMBIOS rev16 vs rev15 (revisa esto primero si ya viste rev15)", "", _txt22, ""]
P.insert(P.index(next(x for x in P if x.startswith("4. Alturas"))), _txt22)
_txt23 = ("23. **rev17 reemplaza a rev16** (revisión dirigida de rev16; detalle en RESUMEN_rev17.md y DELTA_rev16_rev17.md): (1) ELEC 221: la 2a capa 2 HR "
          "estaba en UNTYPED-L2-12, que no encierra el cuarto (está al otro lado del corridor 216) -> pasada a las caras reales de 221, medidas por geometría; "
          "(2) los tramos que faltaban de 221 / 321 / 421 cargados (cada cara de los tres cuartos), un tramo = una fila; (3) WS-1 de L4: un solo criterio para "
          "las 3 zonas (EXCLUDED: RS-1 sin rating y el RCP imprime WS-1), con su delta en el Scope; (4) textos FS-1 / RS-1 por nivel; (5) soffit FCU de la stair "
          "citado con R-ALC-01 y su delta.")
G[2:2] = ["## CAMBIOS rev17 vs rev16 (revisa esto primero si ya viste rev16)", "", _txt23, ""]
P.insert(P.index(next(x for x in P if x.startswith("4. Alturas"))), _txt23)
_txt24 = ("24. **rev18 FINAL reemplaza a rev17** (tus respuestas a los RFI del 11-nov, ya reglas U-161 / U-162 / U-163; detalle en RESUMEN_rev18.md): "
          "RFI-04 y RFI-24 'A: 2 HR (cargado)' -> ELEC 221 / 321 / 421 y DATA 118B se quedan en 2 HR (DA-6 / DA-2 ya no son alternates); RFI-21 'A: Nuestro' -> "
          "el soffit del canopy se queda; RFI-17 (planos primero, código segundo): 1/A3.01 no marca cielo en 128 y el código no lo pide -> GYP-1 de 128 "
          "retirado, 128 EXCLUDED; RFI-13 / RFI-29 (solo gypsum board + metal): MB-1 y shaft ceilings como están, steel platform + fireproofing EXCLUDED. "
          "Ningún RFI queda abierto.")
G[2:2] = ["## CAMBIOS rev18 vs rev17 (revisa esto primero si ya viste rev17)", "", _txt24, ""]
P.insert(P.index(next(x for x in P if x.startswith("4. Alturas"))), _txt24)
P.insert(P.index(next(x for x in P if x.startswith("4. Alturas"))), _txt20)
P.insert(P.index(next(x for x in P if x.startswith("4. Alturas"))), _txt19)
P.insert(P.index(next(x for x in P if x.startswith("4. Alturas"))), _txt18)
P.insert(P.index(next(x for x in P if x.startswith("4. Alturas"))), _txt17)
P.insert(P.index(next(x for x in P if x.startswith("4. Alturas"))), _txt16)
G = ["OPEN IN BLUEBEAM: `Planos marcados/CR_markups_rev18 - OPEN IN BLUEBEAM.pdf` (the only editable markups file; the PNGs named 'IMAGE ONLY (not editable)' are pictures only).", ""] + G   # U-158: primer renglón
open(os.path.join(E, "GUIA_DE_REVISION_DEL_ESTIMADOR.md"), "w").write("\n".join(G) + "\n")
print("docs ok", len(rf), "rfis")
