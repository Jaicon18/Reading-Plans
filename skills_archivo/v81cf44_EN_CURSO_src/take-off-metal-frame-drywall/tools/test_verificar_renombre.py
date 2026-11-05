#!/usr/bin/env python3
"""test_verificar_renombre.py — R80w.46: verificar (1) acepta un renglón de accesorios renombrado por el canon
(acc_nombres, p. ej. joint compound setting-type del spec) leyendo familias_out.json, y (2) no marca "en español" el
VALOR citado del plano en la ficha del proyecto de Inputs (nombre propio 'Camino del Rio'); el rótulo y la hoja se
siguen revisando. Sintético; falla con plantilla v80w.45."""
import json, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import openpyxl
import plantilla_excel as P
d = tempfile.mkdtemp()
wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Inputs"
r0 = max(x[0] for x in P.INPUTS_V68) + 2
ws.cell(r0, 1, "PROJECT DATA SHEET (informative, not an input)")
ws.cell(r0 + 1, 1, "Owner / tenant"); ws.cell(r0 + 1, 2, "Tenant: Chuze Fitness (1011 Camino del Rio South)"); ws.cell(r0 + 1, 3, "G001")
ms = wb.create_sheet("Material Summary"); ms.append(["x"]); ms.append(["x"]); ms.append(["Material", "Unit", "Net", "Waste %", "Waste", "Purchase", "Selling unit", "Pieces to buy", "Where it comes from", "Yield check (live formula)"])
ms.append(["Joint compound - setting-type taping and sandable topping (09 29 00 2.7.C)", "LB", 1, 0, 0, 1, "lb", 1, "N/SHEET: GA-216", None])
wb.create_sheet("Partition Takeoff")
x = os.path.join(d, "t.xlsx"); wb.save(x)
json.dump({"accesorios": {"nombres_excel": {"joint compound": "Joint compound - setting-type taping and sandable topping (09 29 00 2.7.C)"}}},
          open(os.path.join(d, "familias_out.json"), "w"))
err = P.verificar_excel(x)
assert not any("'joint compound'" in e for e in err), [e for e in err if "joint compound" in e]
assert not any("Inputs!B" in e and "español" in e for e in err), [e for e in err if "Inputs" in e]
print("test_verificar_renombre OK")
