#!/usr/bin/env python3
"""test_traza_none_canon.py — R80w.29: un renglón de accesorio en 0 cita el motivo del canon (accesorios_none con su hoja)
aunque la familia tenga texto por defecto (expansion anchors, PAFs, coiling grille): antes el texto fijo pisaba el del
canon y el renglón salía "default (no sheet)". Sintético; falla con trazabilidad v80v."""
import json, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trazabilidad as T
d = tempfile.mkdtemp()
F = "expansion anchors"
json.dump({"familias": {}, "partition_types": {"types": {}}, "filas": [],
           "accesorios": {"nombres_excel": {F: "Expansion anchors X"}}}, open(os.path.join(d, "familias_out.json"), "w"))
for n, v in (("studs_out.json", {"walls": []}), ("board_out.json", {"caras": []}), ("corridas_out.json", {"renglones": []})):
    json.dump(v, open(os.path.join(d, n), "w"))
cp = os.path.join(d, "canon.json")
json.dump({"walls": [], "accesorios_none": [{"familia": F, "why": "no new exterior wall", "source": "B/X200, X201"}]}, open(cp, "w"))
out = T.aplicar({"materials": [{"material": "Expansion anchors X", "unit": "PCS", "net": 0, "familia": F,
                                "source": "accesorios.py"}], "walls": []}, d, cp)
c = out["materials"][0]["cita"]
assert "no new exterior wall" in c and "default (no sheet)" not in c, c
print("test_traza_none_canon OK")
