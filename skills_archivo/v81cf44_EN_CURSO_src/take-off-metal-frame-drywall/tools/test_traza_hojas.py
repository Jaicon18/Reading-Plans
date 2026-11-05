#!/usr/bin/env python3
"""test_traza_hojas.py — R80w.28: trazabilidad cita hojas de 3 dígitos sin guion (X101), con sufijo de letra (10/X505.B) y
el grid de drywall cita la hoja de sus ceilings (antes: "default (no sheet)" en renglones con fuente). Sintético; falla
con trazabilidad v80v."""
import json, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trazabilidad as T
assert T.RX_NH.search("10/X505.B").group(0) == "10/X505.B"
assert T.RX_HOJA.search("A101, A102 sheets").group(0) == "A101"
d = tempfile.mkdtemp()
F = "USG drywall main tee (DGLW26)"
json.dump({"familias": {F: 10.0}, "partition_types": {"types": {}}, "accesorios": {},
           "filas": [{"familia": "ceilings", "room": "R1", "source": "C-5/X121; X421.A", "operacion": "usg_grid: main tee 10"}]},
          open(os.path.join(d, "familias_out.json"), "w"))
for n, v in (("studs_out.json", {"walls": []}), ("board_out.json", {"caras": []}), ("corridas_out.json", {"renglones": []})):
    json.dump(v, open(os.path.join(d, n), "w"))
cp = os.path.join(d, "canon.json"); json.dump({"walls": []}, open(cp, "w"))
out = T.aplicar({"materials": [{"material": "X main tee", "unit": "LF", "net": 10.0, "familia": F, "source": "x"}], "walls": []}, d, cp)
assert "default (no sheet)" not in out["materials"][0]["cita"] and "5/X121" in out["materials"][0]["cita"], out["materials"][0]["cita"]
print("test_traza_hojas OK")
