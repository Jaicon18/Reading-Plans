#!/usr/bin/env python3
"""docs_entrega.py (CR desde cero): README_REVIEW.md (EN), PARA_REVISAR_EN_LA_MANANA.md (ES), SEGUIMIENTO.md, RESUMEN_rev1.md
generados desde takeoff.json + canon + Excel (nada a mano: se regeneran en cada corrida)."""
import json, os, sys, glob
import openpyxl
W = "/root/cr0/work"; D = os.path.join(W, "PRUEBA DESDE CERO 13-nov")
tk = json.load(open(os.path.join(W, "takeoff.json"))); c = json.load(open(os.path.join(W, "etapas/4_canon/takeoff_canon.json")))
xl = glob.glob(os.path.join(D, "Take-off", "*.xlsx"))[0]
wb = openpyxl.load_workbook(xl, data_only=True)
ms = [(r[0], r[1], r[2]) for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True) if r[0] and isinstance(r[2], (int, float))]
pdata = "\n".join(f"| {x['campo']} | {x['valor']} | {x.get('fuente', '')} |" for x in tk["proyecto_datos"])
sheets = "\n".join(f"| {x['categoria']} | {x['estado']} |" for x in tk["hojas_revisadas"])
alt = tk.get("add_alternates") or []
rfis = tk.get("rfis") or []
bank = open(os.path.join(W, "COMPARATIVA_BANCO.md")).read() if os.path.exists(os.path.join(W, "COMPARATIVA_BANCO.md")) else ""
fuera = ""
if "OUT OF RANGE:" in bank:
    fuera = bank.split("OUT OF RANGE:", 1)[1].split("\n", 1)[0].strip()
mat = "\n".join(f"| {m[0]} | {m[1]} | {m[2]:,.1f} |" for m in ms if m[2])
excl = [r for r in wb["Scope Checklist"].iter_rows(min_row=2, values_only=True) if r and r[0] and "EXCLUDED" in " ".join(str(x or "") for x in r)]
exc = "\n".join(f"- {r[1]} — {str(r[3] or '')[:220]}" for r in excl)
readme = f"""# README_REVIEW — CR City Hotel, Castle Rock CO — take-off rev1 (PRUEBA DESDE CERO 13-nov)

## PROJECT DATA
| Field | Value | Source |
|---|---|---|
{pdata}

## MANDATORY SHEETS REVIEWED
| Category | Status |
|---|---|
{sheets}

## What this delivery is
Metal framing (Div. 05 / 09 21 16.23 C-H shaft walls) and gypsum board (Div. 09) take-off, built from scratch on the bid set with skill
v81cf138s (10 steps, independent A / B readings, blind heights H-A / H-B, A/B resolution with crops, programs compute every quantity).
The building is WOOD framed (A0.06 / A0.07 W, DW, FW, FI, XW types): wood framing is Div. 06 and EXCLUDED; those walls are BOARD ONLY.
Metal in scope = C-H shaft walls (north and south shafts, 7/A9.03, 8/A9.03, 1/A7.50, 3/A7.50) and the ceiling suspension / resilient channel.

## Files
- Take-off/{os.path.basename(xl)} — fixed 6-sheet Excel (Inputs, Partition Takeoff, Material Summary, Pending Items, Review Items, Scope Checklist).
- Planos marcados/CR_markups_rev1 - OPEN IN BLUEBEAM.pdf — editable Bluebeam markups (Subject, Page Label, Length, Depth = height, Wall Area).
- Planos marcados/<SHEET> - IMAGE ONLY (not editable) - ... rev1.png — one image per marked sheet.
- Planos marcados/DETALLES_REVISADOS.pdf, SCHEDULES_REVISADOS.pdf — every detail bubble / schedule row followed and circled.
- Proposal/ — proposal with FBM prices (dated) and template rates.
- Auditoria/ — independent audit, heights A / B, double-ceiling review, coverage. If the folder has more than 1,000 files it is uploaded as Auditoria.zip.

## Material Summary (NET, waste added in the Excel)
| Material | Unit | Net |
|---|---|---|
{mat}

## Alternates
""" + "\n".join(f"- ALTERNATE #{a['n']} (ADD): {a['texto']}. {a['razon']}" for a in alt) + f"""

## Open RFIs ({len(rfis)}) — conservative value LOADED in each
""" + "\n".join(f"- {r['id']}: {r['pregunta']} {r['delta']}" for r in rfis) + f"""

## Clarifications & Exclusions
- Wood framing, FRT blocking, plywood (Div. 06), CMU / concrete, brick, siding, SFRM, ACT, wood slat ceilings, FRP, insulation, acoustical sealant, plaster finish: EXCLUDED (other trades).
- All fasteners (screws, anchors, pins) EXCLUDED (estimator rule U-053).
- Retail 124 gypsum board and finish: by future tenant (printed note A2.01). Grey toned area: separate permit (A2.01 / A2.02). Food & Beverage interiors (Kitchen 100, 410 / 411 / 419): not in scope (printed notes 1/A7.45, A2.04, 3/A7.50); rated perimeter faces loaded.
- Ducts / framed openings for MEP: EXCLUDED (R-ALC-03). MEP plans were not downloaded for this reason.
{exc}

## Bank comparison
{bank or 'COMPARATIVA_BANCO.md pending'}

Out-of-range families explained:
- Studs: wood-framed building (A0.06 / A0.07 wood types, Div. 06 EXCLUDED); the only metal studs are the C-H shaft walls, so studs per LF of partition are far below metal-framed projects.
- Track: same reason; only J-runner of the C-H shaft walls.
- Bracing / blocking: wood blocking is Div. 06 (EXCLUDED); no C.R. bracing in wood walls or C-H shaft walls.
"""
open(os.path.join(D, "README_REVIEW.md"), "w").write(readme)
para = f"""# PARA REVISAR EN LA MAÑANA — CR City Hotel (PRUEBA DESDE CERO 13-nov)

## PROJECT DATA
| Field | Value | Source |
|---|---|---|
{pdata}

## Lo esencial
- Take-off completo desde cero con el skill vigente; edificio de madera: walls BOARD ONLY (framing Div. 06 EXCLUDED); metal = shaft walls C-H y suspensión de cielos.
- RFIs abiertos: {len(rfis)} (cada uno con el valor conservador ya CARGADO; detalle en SEGUIMIENTO.md y Pending Items).
- ALTERNATE (ADD): {len(alt)} — forro 3 3/8" de la escalera 1 (material no impreso, U-195).
- Review Items del Excel: decisiones del estimador con las dos cifras y su delta.
"""
open(os.path.join(D, "PARA_REVISAR_EN_LA_MANANA.md"), "w").write(para)
seg = "# SEGUIMIENTO — RFIs (CR City Hotel, PRUEBA DESDE CERO 13-nov)\n\n| RFI | Question | (A) / (B) / (C) and delta | Loaded |\n|---|---|---|---|\n" + \
      "\n".join(f"| {r['id']} | {r['pregunta']} | {r['delta']} | see delta |" for r in rfis) + "\n"
open(os.path.join(D, "SEGUIMIENTO.md"), "w").write(seg)
res = "# RESUMEN rev1 — CR City Hotel\n\n" + "\n".join(f"- {m[0]}: {m[2]:,.1f} {m[1]}" for m in ms if m[2]) + "\n"
open(os.path.join(D, "RESUMEN_rev1.md"), "w").write(res)
print("docs OK", len(rfis), "RFIs")
guia = """# Open in Bluebeam: Planos marcados/CR_markups_rev1 - OPEN IN BLUEBEAM.pdf
# ESTIMATOR REVIEW GUIDE - CR City Hotel (PRUEBA DESDE CERO 13-nov)

How to review this delivery (U-148), in this order:
1. Bluebeam: open the markups PDF above. Markups List columns: Subject (type), Page Label (sheet), Length, Depth (height), Wall Area. Each Contents = TYPE · LF · H · SF wall · faces · SF board · N/SHEET · id.
2. Excel `Take-off/CR_City_Hotel_Takeoff_rev1.xlsx`: Partition Takeoff in schedule order with subtotals; every row cites N/SHEET and carries [CONFIRMED] / [DERIVED] (with the operation) / [PENDING].
3. `Planos marcados/ALTURAS_REVISADAS.pdf`: one page per loaded height, with the printed datum circled.
4. `Planos marcados/DETALLES_REVISADOS.pdf` + `SCHEDULES_REVISADOS.pdf`: every detail and schedule used, circled.
5. `Auditoria/INFORME_AUDITORIA_U181.md`: independent audit, findings and how each was closed.
6. Review Items / Pending Items sheets: estimator decisions with both figures and their delta; ALTERNATE (ADD) priced apart.

Limits of this delivery:
- Wood-framed building: wood studs / joists / blocking are Div. 06 (EXCLUDED); board only on wood walls. Metal = C-H shaft walls and the drywall suspension grid.
- Fasteners are EXCLUDED (estimator rule); MEP penetrations EXCLUDED.
- Proposal rows marked [PRICE TO CONFIRM] / [RATE TO CONFIRM] carry 0 in the totals (product not in the FBM dataset or rate not in the template, U-192 (1)): price them before sending.
- Heights come only from printed datums (never scaled).
"""
open(os.path.join(D, "GUIA_DE_REVISION_DEL_ESTIMADOR.md"), "w").write(guia)
