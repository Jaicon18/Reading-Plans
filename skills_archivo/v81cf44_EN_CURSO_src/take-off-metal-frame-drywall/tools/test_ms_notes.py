#!/usr/bin/env python3
"""test_ms_notes.py — R80w.47: constants.ms_notes [{match, note, source}] agrega la nota de decisión / verificación
al 'Where it comes from' de cada renglón del Material Summary cuyo nombre casa (incluidos los renglones partidos por
producto); sin source = error. Sintético; falla con trazabilidad v80w.46."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trazabilidad as T
can = {"constants": {"ms_notes": [{"match": r"362S162-54", "note": "Estimator decision (option A). Verify at S100", "source": "RFI-S01"}]}}
assert T._nota_ms('3-5/8" metal stud - 362S162-54', can) == " | Estimator decision (option A). Verify at S100"
assert T._nota_ms("Hanger wire", can) == ""
try:
    T._nota_ms("x", {"constants": {"ms_notes": [{"match": "x", "note": "y"}]}})
    raise SystemExit("sin source aceptado")
except ValueError:
    pass
src = open(T.__file__, encoding="utf-8").read()
assert src.count("_nota_ms(") >= 3
print("test_ms_notes OK")
