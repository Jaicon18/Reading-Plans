#!/usr/bin/env python3
"""test_traza_stud_fam.py — R80w.18: el desglose de studs de trazabilidad.py asigna cada wall a su familia con la regla
de canon.py (STUD_FAM): un stud_size "PENDING - 6\\" assumed (RFI)" o "3-5/8\\" + 6\\"" suma en la familia 6" (antes: igualdad
exacta -> desglose corto -> ValueError y el Excel no se armaba). Sintético; falla con trazabilidad v80v."""
import json, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trazabilidad as T
d = tempfile.mkdtemp()
F6 = '6" stud (todos los gauges)'
json.dump({"familias": {F6: 30.0}, "filas": [], "partition_types": {"types": {}}, "accesorios": {}},
          open(os.path.join(d, "familias_out.json"), "w"))
json.dump({"walls": [{"id": "W1", "stud_size": '6"', "lf": 10.0},
                     {"id": "W2", "stud_size": 'PENDING - 6" assumed (RFI-00)', "lf": 15.0},
                     {"id": "W3", "stud_size": '3-5/8" + 6"', "lf": 5.0}]}, open(os.path.join(d, "studs_out.json"), "w"))
json.dump({"caras": []}, open(os.path.join(d, "board_out.json"), "w"))
json.dump({"renglones": []}, open(os.path.join(d, "corridas_out.json"), "w"))
cp = os.path.join(d, "canon.json")
json.dump({"walls": [{"id": "W1", "detail": "T1/X301"}, {"id": "W2", "detail": "1/X502"}, {"id": "W3", "detail": "1/X502"}]},
          open(cp, "w"))
dd = {"materials": [{"material": '6" metal stud (LF of material)', "unit": "LF", "net": 30.0, "familia": F6, "source": "x"}],
      "walls": []}
out = T.aplicar(dd, d, cp)
assert "= 30" in out["materials"][0]["cita"], out["materials"][0]["cita"]
print("test_traza_stud_fam OK")
