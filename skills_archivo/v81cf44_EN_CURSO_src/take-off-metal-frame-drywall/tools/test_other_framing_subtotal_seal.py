#!/usr/bin/env python3
"""test_other_framing_subtotal_seal.py — v81cf8 T5 + T6 (BE-CF18): (T5) the OTHER FRAMING block of the Partition
Takeoff has its SUBTOTAL row (LF and board SF); (T6) the delivered workbook has exactly the 6 fixed sheets: the seal
of reglas.py goes to <excel>.sello.json (bound to the workbook sha), read by reglas.leer_sello; an old workbook with
the hidden `_reglas` sheet is still read. v81cf7: no OTHER FRAMING subtotal and a 7th hidden sheet."""
import copy, json, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import openpyxl
import plantilla_excel as P
import reglas
d = copy.deepcopy(P.EJEMPLO)
d["other_framing"] = [{"type": "Soffit side", "wall": "SS-1", "location": "soffit", "length_lf": 10.0, "height_ft": 1.0,
                       "stud_size": "3-5/8\"", "stud_oc_in": 16, "layers": 1, "board_sf": 10.0, "source": "1/A-501", "status": "DERIVADO"},
                      {"type": "Soffit side", "wall": "SS-2", "location": "soffit", "length_lf": 5.0, "height_ft": 1.0,
                       "stud_size": "3-5/8\"", "stud_oc_in": 16, "layers": 1, "board_sf": 5.0, "source": "1/A-501", "status": "DERIVADO"}]
t = tempfile.mkdtemp()
x = os.path.join(t, "t.xlsx")
P._escribir(d, x, {"huella": {"version": "test", "canon": "abc"}})
wb = openpyxl.load_workbook(x)
assert wb.sheetnames == ["Inputs", "Partition Takeoff", "Material Summary", "Pending Items", P.HOJA_REVISAR, P.HOJA_ALCANCES], wb.sheetnames
assert any(r[1] == "SUBTOTAL OTHER FRAMING" for r in wb["Partition Takeoff"].iter_rows(values_only=True)), "no OTHER FRAMING subtotal"
assert reglas.leer_sello(x) == {"version": "test", "canon": "abc"}
open(x, "ab").write(b"\0")                     # workbook changed after the seal -> no longer sealed
assert reglas.leer_sello(x) is None
y = os.path.join(t, "old.xlsx")                # backward compatibility: hidden _reglas sheet
wo = openpyxl.Workbook(); reglas.sellar(wo, {"huella": {"canon": "old"}}); wo.save(y)
assert reglas.leer_sello(y) == {"canon": "old"}
print("test_other_framing_subtotal_seal OK")
