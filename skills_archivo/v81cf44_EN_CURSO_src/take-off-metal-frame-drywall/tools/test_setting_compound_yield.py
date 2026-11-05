#!/usr/bin/env python3
"""test_setting_compound_yield.py — v81cf8 T3 + T4 (BE-CF17): setting-type joint compound at cement board joints is a
real Material Summary row in LB (misc family), and the yield rows (mesh tape, setting compound) carry NO waste
(Inputs: yields carry no waste). v81cf7: no LB family (note only) and mesh tape bought with 6 % waste."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import canon, familias, plantilla_excel as P
S = "setting-type joint compound at cement board (printed)"
M = "alkali-resistant mesh tape (printed)"
assert S in canon.FAMS and S not in canon.OBLIGATORIAS
assert familias.familia(P.NOMBRES_PLANTILLA[S], "lb") == S
fo = {"familias": {S: 129.62, M: 666.1}, "filas": [], "accesorios": {"familias": {}}}
rows = {m["familia"]: m for m in P.familias_faltantes([], fo, fo["familias"], fo["accesorios"], familias)}
assert rows[S]["unit"] == "LB" and rows[S]["net"] == 129.62, rows[S]
for f in (S, M):
    assert P.waste_celda(rows[f], {"waste_metal": "x", "waste_no": "y"}) == 0, (f, rows[f])
print("test_setting_compound_yield OK")
