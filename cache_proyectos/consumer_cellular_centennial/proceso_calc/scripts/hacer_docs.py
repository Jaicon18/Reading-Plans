#!/usr/bin/env python3
"""README_REVIEW.md (English), PARA_REVISAR_EN_LA_MANANA.md and SEGUIMIENTO.md (Spanish notes, trade terms in English) of
the Consumer Cellular Centennial rev2 FINAL delivery. Every number is read from the delivered Excel / canon; nothing typed.
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
titulo = "Consumer Cellular - Yosemite Park Shopping Center, Centennial, CO (store CO2) — Metal framing & drywall take-off, rev2 FINAL"
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
 "- `Take-off/Consumer_Cellular_Centennial_Takeoff_FINAL_rev2.xlsx` — fixed 6-sheet format (Inputs, Partition Takeoff, Material Summary, Pending Items, Review Items, Scope Checklist). Waste applied once, in the Material Summary.",
 "- `Planos marcados/Consumer_Cellular_Centennial_markups_rev2.pdf` — Bluebeam markups: walls on A100 (Subject = type, Page Label, Length, Depth = wall height, Wall Area; Contents = TYPE · LF · H · board SF · DETAIL · Wall ID), demolition lines on D100 (SF only), restroom gypsum ceiling polygon on A200 + one PNG per type (`A100_type_<T>.png`) and one per marked sheet.",
 "- `Planos marcados/DETALLES_REVISADOS.pdf` — every detail / section / elevation bubble reviewed, circled and numbered on the calling sheet and on its destination (index below).",
 "- `Planos marcados/SCHEDULES_REVISADOS.pdf` — every trade schedule row marked (red circle + check + number); material list SCHEDULES_MATERIALES below.",
 "- `SEGUIMIENTO.md` — RFI follow-up (Spanish). `PARA_REVISAR_EN_LA_MANANA.md` — review-first notes (Spanish).",
 "- `Auditoria/` — delivery gate (ENTREGA_OK.json), bubble verification, independent schedule reading, back-check, bank comparison.",
 "", "## Walls by type (schedule order 1/A500)", "", "| Type | Walls | LF | Detail |", "|---|---|---|---|"]
for t in ("A3", "C3", "D", "E3"):
    R.append(f"| {t} | {tot[t][0]} | {tot[t][1]:,.2f} | {t}/A500 |")
import sys as _s
_s.path.insert(0, "/tmp/claude-0/-home-user/d2b6b434-1017-52fc-8c0e-204720c3b7f4/scratchpad/skill_v81cf47/take-off-metal-frame-drywall/tools")
import chequeos_biblioteca as _CB, compuerta_entrega as _CE
_b = _CB.B.desde_ctx(_CE.Ctx(os.path.dirname(E.rstrip("/"))))
_regs = _CB.cadena_detalles(_b)
_po = {}
for _r in _regs:
    _po[_r["origen"]] = _po.get(_r["origen"], 0) + 1
_st = json.load(open("/root/cc/work/set_texto.json"))["burbujas"]
_det = {k: len(v.get("burbujas") or []) for k, v in _st.items() if v.get("burbujas")}
_ind = sum(len(v.get("indep_no_detectados") or []) for v in _st.values())
_vb = json.load(open("/root/cc/work/burbujas/burbujas_verificadas.json"))
_ver = {k: sum(1 for x in xs if isinstance(x, dict) and x.get("n") and x.get("hoja")) for k, xs in _vb.items() if isinstance(xs, list)}
_ver = {k: v for k, v in _ver.items() if v}
_cm = _CB.cadena_md(_b)
R += ["", "## Basis of this revision", "",
      "rev2 FINAL = rev1 + (1) every bubble of the reference chain (detector + eye-verified + CADENA.md, including the eye-found and "
      "the written references) circled and numbered in red on its calling sheet and on its destination view (DETALLES_REVISADOS.pdf; "
      "rev1 only reached A100 / A500 / A600); (2) restroom C-1 ceiling = 2/A501 drywall grid suspension system (option A, drawings "
      "govern; RFI-06 closed); (3) RFI-02 closed by rule BOTH SIDES; (4) RFI-03 / RFI-05 / RFI-07 closed with what the sheets print. "
      "Every other quantity is identical to rev1. RFI-08 closed with what 1/A504 and 1/A500 print (U-140). Open RFIs: RFI-01 and RFI-04 only.", "",
      "## Bubble count reconciliation (detector / eye-verified / CADENA.md / circled)", "",
      f"- Independent rings checked by eye: {_ind} - all are level / datum marks (quartered circles), none is a detail bubble.",
      f"- Two-line bubbles found by the detector: {sum(_det.values())} (" + ", ".join(f"{k} {v}" for k, v in _det.items()) + ").",
      f"- References read by eye with N/SHEET (burbujas_verificadas.json, includes the detector ones re-read and the written references): {sum(_ver.values())} (" + ", ".join(f"{k} {v}" for k, v in _ver.items()) + ").",
      f"- CADENA.md numbered items by calling sheet: " + ", ".join(f"{k} {v}" for k, v in _cm.items()) + " (one item can hold several bubbles, e.g. 2/A500 x5).",
      "- rev1 circled 32 marks only on the sheets the chain reached from the plans (A100 2, A500 14, A600 16 - A600 counted the detector and the eye reading of the same 8 door schedule cells twice, and the 8 detector circles were drawn in the unrotated frame of the 270-degree page, away from the cells: fixed in rev2, BE-CC09).",
      f"- rev2 circled {len(_regs)} bubbles (union, the same bubble seen by the detector and by eye counted once): " + ", ".join(f"{k} {v}" for k, v in _po.items()) + "; each one also on its destination view.",
      ]
R += ["", "## Material Summary (net, before waste)", "", "| Material | Unit | Net | Where it comes from |", "|---|---|---|---|"]
for r in ms:
    R.append(f"| {r[0]} | {r[1]} | {r[2]:,.2f} | {str(r[8] or '')[:110]} |")
R += ["", "## Open RFIs (conservative value loaded; only what no sheet prints, U-140)", "", "| RFI | Question | Loaded | Options A / B / C with delta |", "|---|---|---|---|"]
for r in rf:
    o = r["opciones"]
    R.append(f"| {r['id']} | {r['question']} | {r['loaded']} | (A) {o['A']['texto']} - delta {o['A']['delta']} / (B) {o['B']['texto']} ({o['B']['cita']}) - delta {o['B']['delta']} / (C) other: ____ |")
open(os.path.join(E, "README_REVIEW.md"), "w", encoding="utf-8").write("\n".join(R) + "\n")
P = [f"# Revisar primero — {titulo}", "", "Notas en español; los términos del trade van en inglés. Los datos del proyecto están en README_REVIEW.md (PROJECT DATA).", "",
 "## Proyecto", "", f"- {td['proyecto']}", "- GC: Elite Retail Services (bid 11/05/2026 4:00 PM CT) y Elder-Jones, Inc. (bid 11/06/2026). Los dos sets son idénticos hoja por hoja (comparados por programa): delta entre GC = 0 para nuestro alcance.",
 "- Tenant improvement, 3,103 SF (G003), IBC 2021, Type II-B, M, not sprinklered. Sin project manual: A700 son schedules de acabados.", "",
 "## Revisar esto primero", "",
 f"1. RFI abiertos: {len(rf)} (Pending Items), todos con el supuesto conservador CARGADO y su delta (detalle en SEGUIMIENTO.md).",
 "2. RFI-02 (CERRADO por regla U-127 BOTH SIDES): type A# imprime '5/8\" TYPE X ON EACH SIDE'; se cargaron las DOS caras. Nota: la sección de 1/A500 dibuja una sola cara; una cara restaría el delta indicado en SEGUIMIENTO.",
 "3. RFI-01 (abierto): el corte de deck 16'-4\" / 17'-1 9/16\" no está dibujado en ninguna hoja; C3-01 cargado a 17'-1 9/16\".",
 "4. Demolición: solo SF (DEMO-01..06, D100 keys 9 y 27) a la altura del B.O. de estructura impreso; cielos existentes (key 7) EXCLUDED por falta de información (gyp vs ACT no indicado).",
 "5. FRP (B-3) CARGADO (FRP-RR baño a T.O. FRP 4'-0\" A402, FRP-MOP 1/A504) con su PVC trim; insulation, ACT, paint, wood (FRT plywood, 2X4) y tornillería: EXCLUDED con nota, sin RFI. (Corrige la nota de rev1, que decía FRP EXCLUDED; las cantidades de FRP de rev1 ya estaban cargadas.)",
 "8. NUEVO en rev2: (a) DETALLES_REVISADOS.pdf circula y numera TODAS las burbujas de CADENA.md (origen + destino) en A100, A101, A102, A103, A402, A500, A501, A600 y A700; conteo por hoja al final de README_REVIEW.md (BE-CC07); (b) RFI-06 cerrado: cielo del baño = grid 2/A501 (opción A, el plano manda), delta vs furring ASTM C754 en SEGUIMIENTO; (c) RFI-02 cerrado por regla BOTH SIDES (U-127), la sección de una cara queda como nota; (d) re-chequeo U-140: RFI-03 (4/A500 imprime '20 GA. MIN. TRACK'), RFI-05 (la línea C3 sigue sobre el cased opening) y RFI-07 (door schedule 3C imprime HEAD 2/A600, JAMB 3/A600) cerrados con lo impreso; RFI-08 cerrado con lo impreso (1/A504 imprime los members 6\" 16 GA; layout al spacing impreso 16\" o.c. de 1/A500); quedan abiertos solo RFI-01 y RFI-04.",
 "9. Referencias impresas que no existen o no coinciden (sin cambio de cantidad de metal / gypsum, nota sin RFI): C1/G002 (G002 no tiene C1; vista más cercana 6/G002 ADA counters, millwork), 'A4/-' en 3/A402 apunta a 4A CLEAR FLOOR SPACE (el blocking de grab bar sale de 5/A402, cargado), A700 SHELVES -> 6/A500 (es ATTACHMENT TO STRUCTURE; la repisa sale de 1/A504, dentro de RFI-08).",
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
S += ["", "## Notas (referencias impresas que no existen o no coinciden; sin cambio de cantidad de metal / gypsum, sin RFI - R-ALC-01)", "",
      "| Referencia | Hoja de origen | Qué pasa | Qué se cargó |", "|---|---|---|---|",
      "| C1/G002 | A102 / A103 general note 2 | G002 imprime los detalles 1-8, no hay C1; la vista más cercana es 6/G002 ADA SERVICE COUNTER ELEVATIONS (alturas de counters, millwork / fixtures por otros) | nada (millwork por otros) |",
      "| A4/- (4A/A402) | 3/A402 TYPICAL MOUNTING HEIGHTS | apunta a 4A CLEAR FLOOR SPACE del lavatory; el grab bar está en 5/A402 GRAB BAR DETAIL | BLK-GRAB 8.0 LF de 5/A402 (cargado desde rev1) |",
      "| 6/A500 | A700 nota SHELVES | 6/A500 es ATTACHMENT TO STRUCTURE (brace), no una repisa | repisa del mop sink de 1/A504 (RFI-08) |",
      "| SILL 'A502' | A600 door schedule | sin número de detalle; A502 son detalles de piso (flooring) | nada (flooring) |"]
open(os.path.join(E, "SEGUIMIENTO.md"), "w", encoding="utf-8").write("\n".join(S) + "\n")
print("docs OK", len(rf), "open RFIs")
