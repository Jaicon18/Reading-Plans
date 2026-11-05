#!/usr/bin/env python3
"""test_no_sheet_and_misc_product.py — R80w.48: verificar falla una fila del Material Summary con "N/SHEET: default
(no sheet)"; R80w.49: un misc_item con `product {value, source}` parte el renglón de su familia por producto de compra
(p. ej. sill sealer gasket vs isolation strip). Sintético; falla con plantilla / trazabilidad v80w.47."""
import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import openpyxl
import plantilla_excel as P
import trazabilidad as T
d = tempfile.mkdtemp()
wb = openpyxl.Workbook(); wb.active.title = "Inputs"
ms = wb.create_sheet("Material Summary"); ms.append(["x"]); ms.append(["x"])
ms.append(["Material", "Unit", "Net", "Waste %", "Waste", "Purchase", "Selling unit", "Pieces to buy", "Where it comes from", "Yield check (live formula)"])
ms.append(["Gypsum board jamb return at openings", "SF", 1, 0, 0, 1, "sheet", 1, "[CRITERION] N/SHEET: default (no sheet) | edges", None])
wb.create_sheet("Partition Takeoff")
x = os.path.join(d, "t.xlsx"); wb.save(x)
assert any("default (no sheet)" in e for e in P.verificar_excel(x))
can = {"misc_items": [{"ref": "g1", "familia": "sealer gasket (printed)", "qty": 10, "product": {"value": "sill sealer gasket", "source": "05 40 00 2.9.E"}},
                      {"ref": "g2", "familia": "sealer gasket (printed)", "qty": 5, "product": {"value": "isolation strip", "source": "09 22 16 2.4.B"}}]}
g = T._por_producto("Sealer gasket", "sealer gasket (printed)", [("g1", 10.0), ("g2", 5.0)], {}, can)
assert g == {"sill sealer gasket": [("g1", 10.0)], "isolation strip": [("g2", 5.0)]}, g
print("test_no_sheet_and_misc_product OK")
