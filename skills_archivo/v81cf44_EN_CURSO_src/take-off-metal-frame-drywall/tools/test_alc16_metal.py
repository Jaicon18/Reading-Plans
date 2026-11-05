#!/usr/bin/env python3
"""test_alc16_metal.py — R80w.30: ALC-16 (blocking) se cierra cuantificado con blocking / backing METÁLICO (renglón de
metal stud blocking > 0) cuando la madera está excluida; antes solo contaba "FRT blocking" y el backing metálico impreso
no podía cerrarse. Sintético; falla con alcances.py v80v."""
import json, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import openpyxl
import alcances as A
d = tempfile.mkdtemp()
wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Material Summary"
ws.append(["Material", "Unit", "Net"]); ws.append(["Metal stud blocking at wall-mounted items (notes)", "LF", 25.0])
x = os.path.join(d, "t.xlsx"); wb.save(x)
esc = {"alcances": {a[0]: {"nombre": a[1], "hallazgos": []} for a in A.ALCANCES}}
ren = os.path.join(d, "ren.json"); json.dump(A.renglones(esc), open(ren, "w"))
reg = os.path.join(d, "reg.json")
import subprocess
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "registro.py"), "crear", reg, ren], check=True,
               capture_output=True)
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "registro.py"), "marcar", reg, "ALC-16",
                "verificado", "metal backing X103 keys"], check=True, capture_output=True)
fallas, _ = A.compuerta(reg, esc, x)
assert not [f for f in fallas if f.startswith("ALC-16")], [f for f in fallas if f.startswith("ALC-16")]
print("test_alc16_metal OK")
