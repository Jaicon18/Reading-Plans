#!/usr/bin/env python3
"""test_existing_walls.py — R80w.39: muros existentes con board de cara completa (decisión del estimador) como
elemento propio: (1) canon suma el board (L x H x caras x capas) a la familia y devuelve el renglón; path solo con
tramos rectos y largo = path / escala de la hoja; (2) la Partition Takeoff los lista en su bloque con SUBTOTAL;
(3) markups: un markup por muro con Subject 'EXISTING - BOARD ONLY' y Contents LF / H / caras / SF / keynote / id.
Sintético; falla con canon / plantilla / markups v80w.38."""
import os, sys, tempfile
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import canon as C
import markups_bluebeam as MB
import plantilla_excel as P
ex = {"id": "EX-01", "sheet": "X101", "page": 1, "keynote": "D0.07/X101", "path": [[0, 0], [100, 0], [100, 50]],
      "length_ft": 15.0, "height_ft": 10.0, "faces": 2, "layers": 1, "board": "5/8 type X", "location": "test",
      "source": "X101 keynote D0.07", "decision": "estimator decision 2026-11-02"}
data = {"constants": {"plan_scale_by_sheet": {"X101": {"value": 10.0, "source": "X101 title"}}}, "existing_walls": [ex]}
fam, filas = defaultdict(float), []
rows = C._existing_walls(data, fam, filas)
assert fam['5/8" gyp board Type X'] == 300.0 and rows[0]["board_sf"] == 300.0, (dict(fam), rows)
for bad in ({"path": [[0, 0], [100, 50]]}, {"length_ft": 12.0}):
    try:
        C._existing_walls(dict(data, existing_walls=[dict(ex, **bad)]), defaultdict(float), [])
        raise SystemExit(f"aceptado: {bad}")
    except ValueError:
        pass
w = [x for x in MB.walls(data) if x["id"] == "EX-01"][0]
assert MB.tipo(w) == "BOARD ONLY - NO FRAMING" and "2 face(s)" in MB.contenido(w) and "300.00 SF" in MB.contenido(w), MB.contenido(w)
assert MB.eje_canon(w)[0][0] == [(0, 0), (100, 0), (100, 50)]
d = {"proyecto": "T", "walls": [], "existing_walls": rows}
import openpyxl
src = open(P.__file__, encoding="utf-8").read()
assert "EXIST_TYPE" in src and "SUBTOTAL BOARD-ONLY WALLS" in src
print("test_existing_walls OK")
