#!/usr/bin/env python3
"""test_traza_stud25.py — R80w.22: el renglón 2-1/2" stud (familia sin "(todos los gauges)") sale con desglose por wall y
N/HOJA como las otras familias de stud (antes: "default (no sheet)" sin desglose). Sintético; falla con trazabilidad v80v."""
import json, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trazabilidad as T
d = tempfile.mkdtemp()
F = '2-1/2" stud'
json.dump({"familias": {F: 12.0}, "filas": [], "partition_types": {"types": {}}, "accesorios": {}},
          open(os.path.join(d, "familias_out.json"), "w"))
json.dump({"walls": [{"id": "W1", "stud_size": '2-1/2"', "lf": 12.0}]}, open(os.path.join(d, "studs_out.json"), "w"))
json.dump({"caras": []}, open(os.path.join(d, "board_out.json"), "w"))
json.dump({"renglones": []}, open(os.path.join(d, "corridas_out.json"), "w"))
cp = os.path.join(d, "canon.json")
json.dump({"walls": [{"id": "W1", "detail": "TYPE B2E/X301"}]}, open(cp, "w"))
out = T.aplicar({"materials": [{"material": '2-1/2" stud', "unit": "LF", "net": 12.0, "familia": F, "source": "x"}],
                 "walls": []}, d, cp)
c = out["materials"][0]["cita"]
assert "Breakdown" in c and "W1" in c and "2E/X301" in c, c
print("test_traza_stud25 OK")
