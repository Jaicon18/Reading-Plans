#!/usr/bin/env python3
"""test_rfi_formato.py — R80e.50: Pending Items con opciones (A) / (B) / (C); reglas.A_RFI_FORMATO detecta lo que falta."""
import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import openpyxl
import reglas
import plantilla_excel


def libro(cab, filas):
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Pending Items"; ws.append(cab)
    for f in filas:
        ws.append(f)
    p = os.path.join(tempfile.mkdtemp(), "t.xlsx"); wb.save(p); return p


class Ctx:
    def __init__(self, x):
        self.excel = x


CAB = ["RFI", "Question / condition", "Delta of each alternative"]
ok = libro(CAB, [["RFI-01", "q", "(A) Plans / specs: A-101 3'-0\" | delta +1 SF | (B) Trade code: none cited | (C) Other: ____"]])
assert reglas.a_rfi_formato(Ctx(ok)) == [], "formato bueno marcado como falla"
viejo = libro(CAB, [["RFI-01", "q", "+1 SF"]])
assert reglas.a_rfi_formato(Ctx(viejo)), "delta sin (A)/(B)/(C) no detectado"
cols = libro(CAB + ["(A) extra"], [["RFI-01", "q", "(A) x | (B) y | (C) Other: ____", "x"]])
assert reglas.a_rfi_formato(Ctx(cols)), "columna nueva en Pending Items no detectada (formato fijo)"
a, b = plantilla_excel.opciones_rfi({"id": "RFI-02", "pregunta": "q", "delta": "+2 LF", "source": "2/A-410"})
assert "2/A-410" in a and "delta +2 LF" in a and b.startswith("Trade code"), (a, b)
print("test_rfi_formato OK")
