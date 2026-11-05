#!/usr/bin/env python3
"""test_soffit_doble.py — R80e.132 / BE-VS-12: misc_item 3-5/8 stud con el mismo LF que un renglón framed soffit = falla."""
import os, sys, types
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reglas as R
fn = R.CHEQUEOS["A_SOFFIT_DOBLE"][0]
sal = {"familias_out.json": {"stud_by_element": {'3-5/8" stud (todos los gauges)': {"3-5/8 stud, framed soffit B/A10.03 (LF)": 122.06}}}}
mal = types.SimpleNamespace(salidas=sal, canon={"misc_items": [{"ref": "valance top members", "familia": '3-5/8" stud (todos los gauges)', "qty": 122.06}]})
bien = types.SimpleNamespace(salidas=sal, canon={"misc_items": [{"ref": "suspended stud", "familia": '3-5/8" stud (todos los gauges)', "qty": 85.62}]})
assert fn(mal) and not fn(bien)
print("test_soffit_doble OK")
