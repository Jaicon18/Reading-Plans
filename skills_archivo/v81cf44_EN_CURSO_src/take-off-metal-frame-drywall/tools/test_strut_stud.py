#!/usr/bin/env python3
"""test_strut_stud.py — R80e.131 / R-ALC-12: un compression strut cargado como EMT hace fallar A_STRUT_STUD;
como 3-5/8 stud pasa."""
import os, sys, types
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reglas as R
fn = R.CHEQUEOS["A_STRUT_STUD"][0]
mal = types.SimpleNamespace(canon={"misc_items": [{"ref": "x", "familia": "EMT compression strut 1.25 dia x 20 GA", "qty": 10}]})
bien = types.SimpleNamespace(canon={"misc_items": [{"ref": "x", "familia": "3-5/8 stud (todos los gauges)", "qty": 10}]})
assert fn(mal), "EMT debe fallar"
assert not fn(bien), "stud debe pasar"
print("test_strut_stud OK")
