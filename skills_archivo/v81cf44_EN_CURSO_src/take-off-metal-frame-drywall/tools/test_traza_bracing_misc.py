#!/usr/bin/env python3
"""test_traza_bracing_misc.py — R80w.27: el desglose del renglón de bracing C.R. channel incluye los miembros de bracing
que el canon declara en misc_items (además de las filas de corridas): antes el desglose quedaba corto -> ValueError y
el Excel no se armaba. Sintético; falla con trazabilidad v80v."""
import json, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trazabilidad as T
d = tempfile.mkdtemp()
F = "bracing C.R. channel"
json.dump({"familias": {F: 15.0}, "partition_types": {"types": {}}, "accesorios": {},
           "filas": [{"familia": F, "ref": "M1", "source": "1/X301", "operacion": "3 rows x 1.0 = 5.0 LF"}]},
          open(os.path.join(d, "familias_out.json"), "w"))
json.dump({"walls": []}, open(os.path.join(d, "studs_out.json"), "w"))
json.dump({"caras": []}, open(os.path.join(d, "board_out.json"), "w"))
json.dump({"renglones": [{"id": "W:W1", "bracing_lf": 10.0}]}, open(os.path.join(d, "corridas_out.json"), "w"))
cp = os.path.join(d, "canon.json")
json.dump({"walls": [{"id": "W1", "detail": "TYPE T1/X301"}], "misc_items": [{"ref": "M1", "qty": 5.0}]}, open(cp, "w"))
out = T.aplicar({"materials": [{"material": "Bracing 1-1/2\" C.R. channel", "unit": "LF", "net": 15.0, "familia": F,
                                "source": "x"}], "walls": []}, d, cp)
assert "= 15" in out["materials"][0]["cita"], out["materials"][0]["cita"]
print("test_traza_bracing_misc OK")
