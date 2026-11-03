#!/usr/bin/env python3
"""test_revision_materiales.py — repite un error real: un type cuyo schedule imprime board MR / W.R. (o Type X) en las
dos caras, cargado en el take-off como board REGULAR en una cara -> revision_materiales debe dar ROJO; el mismo wall con el
board correcto -> VERDE."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import revision_materiales as R  # noqa: E402

ficha = {"stud_designation": "362S162-33", "gauge_ga": 20, "oc_in": 16, "height": "STUDS TO 8'-6\" A.F.F.",
         "faces": [{"side": "each side", "layers": 1, "board": "5/8\" Type X W.R."}],
         "sources": {"stud": "W1/A1.1", "board": "W1/A1.1", "height": "W1/A1.1"}}
fila = [{"type": "W1", "wall": "W-1", "lf": 10.0, "h": 8.5, "layers": 1, "stud": '3-5/8" 20 ga (33 mil, 362S162-33)',
         "oc": 16, "board_sf": 170, "location": "", "source": "W1/A1.1"}]
bien = {"W-1": {"faces": [{"side": "A", "board": "5/8 type X WR", "layers": 1, "height_ft": 8.5},
                          {"side": "B", "board": "5/8 type X WR", "layers": 1, "height_ft": 8.5}]}}
mal = {"W-1": {"faces": [{"side": "A", "board": "5/8 type X WR", "layers": 1, "height_ft": 8.5},
                         {"side": "B", "board": "5/8 regular", "layers": 1, "height_ft": 8.5}]}}
r = R.comparar_type("W1", ficha, fila, bien)
assert r["verdict"] == "GREEN", r
r = R.comparar_type("W1", ficha, fila, mal)
assert r["verdict"] == "RED" and any(c["field"].startswith("board type") and c["status"] == "RED" for c in r["checks"]), r
# gauge / altura distintos al schedule -> ROJO
fila2 = [dict(fila[0], stud='3-5/8" 25 ga (18 mil, 362S162-18)', h=9.0)]
r = R.comparar_type("W1", ficha, fila2, bien)
assert {c["field"] for c in r["checks"] if c["status"] == "RED"} >= {"stud designation", "gauge", "height"}, r
assert R.tipo_board('5/8" TYPE "X" GYPSUM BOARD') == "X" and R.tipo_board("5/8 type X WR") == "X-WR"
print("OK test_revision_materiales")

# sumas: breakdown que no cierra -> ROJO; Net > 0 sin hoja impresa -> ROJO; breakdown correcto con origen -> VERDE
ms = [{"row": 4, "name": "Bottom track 3-5/8\"", "unit": "LF", "net": 30.0,
       "where": "N/SHEET: W1/A1.1 | Breakdown [DERIVED]: W-1 10 + W-2 20 = 30 LF"},
      {"row": 5, "name": "Top track 3-5/8\"", "unit": "LF", "net": 31.0,
       "where": "N/SHEET: W1/A1.1 | Breakdown [DERIVED]: W-1 10 + W-2 20 = 30 LF"},
      {"row": 6, "name": "Additional head track", "unit": "LF", "net": 7.33, "where": "N/SHEET: default (no sheet) | Door 3"}]
fil = [{"type": "W1", "wall": "W-1"}, {"type": "W1", "wall": "W-2"}]
sm = {x["row"]: x for x in R.sumas(ms, fil, "/nonexistent")}
assert sm[4]["status"] == "GREEN" and sm[4]["by_type"] == {"W1": 30.0}, sm[4]
assert sm[5]["status"] == "RED" and sm[6]["status"] == "RED", (sm[5], sm[6])
print("OK test sumas")
