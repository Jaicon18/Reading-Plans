#!/usr/bin/env python3
"""test_fastener_sheet.py — R80w.40: con fasteners_excluded (R80e.77) la fila en 0 de cada familia de tornillería
conserva la hoja de donde salía el item (fuente del cálculo o del none-reason) además de la regla del estimador, en vez
de quedar solo con la regla ("N/SHEET: default (no sheet)" en el Excel). Sintético; falla con accesorios v80w.39."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import accesorios as A
d = {"fasteners_excluded": {"why": "fasteners", "source": "estimator standing rule"},
     "accesorios_none": [{"familia": "expansion anchors", "why": "no exterior wall on slab", "source": "A201"}]}
r = A.calcular({"familias": {}}, d)
src = [x["source"] for x in r["filas"] if x["familia"] == "expansion anchors"]
assert src == ["A201; estimator standing rule"], src
assert r["familias"]["expansion anchors"] == 0.0
print("test_fastener_sheet OK")
