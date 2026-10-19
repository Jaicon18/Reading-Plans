#!/usr/bin/env python3
"""test_registro_v73.py — v73 (F01): registro.py corregir. Datos sintéticos."""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import registro as R  # noqa: E402

F = []


def ok(n, c):
    print(("OK   " if c else "FALLA"), n)
    c or F.append(n)


d = tempfile.mkdtemp()
p = os.path.join(d, "registro.json")
R.crear(p, [{"id": "ALC-90", "tipo": "otro", "ubicacion": "scope", "fuente": "Z0.01"},
            {"id": "W-1", "tipo": "wall", "ubicacion": "room 901", "fuente": "Z1.01"}])
R.marcar(p, "ALC-90", "verificado", "QUANTIFIED: workbook row 12")
r = R.corregir(p, "ALC-90", "verificado", "NO APLICA: Z5.01 no rated partition; scan hits are backboards (Z9.01)")
ok("la última entrada manda", R.leer(p)["renglones"][0]["nota"].startswith("NO APLICA"))
ok("historial guarda la anterior", "QUANTIFIED" in R.leer(p)["renglones"][0]["historial"][-1][3])
ok("contador de correcciones", r["corregido"] == 1)
try:
    R.corregir(p, "W-1", "verificado", "x")
    ok("no corrige un pendiente (usar marcar)", False)
except R.RegistroRoto:
    ok("no corrige un pendiente (usar marcar)", True)
try:
    R.corregir(p, "ALC-90", "pendiente_rfi", "sin número")
    ok("pendiente_rfi exige RFI", False)
except R.RegistroRoto:
    ok("pendiente_rfi exige RFI", True)
reg = json.load(open(p))
reg["renglones"][0]["ubicacion"] = "editado"
json.dump(reg, open(p, "w"))
try:
    R.leer(p)
    ok("edición a mano sigue detectada", False)
except R.RegistroRoto:
    ok("edición a mano sigue detectada", True)
print("test_registro_v73:", "OK" if not F else f"{len(F)} fallo(s)")
sys.exit(1 if F else 0)
