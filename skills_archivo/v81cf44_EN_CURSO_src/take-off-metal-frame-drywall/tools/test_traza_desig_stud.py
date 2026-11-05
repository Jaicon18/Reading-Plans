#!/usr/bin/env python3
"""test_traza_desig_stud.py — R80w.21: el renglón de STUDS no se parte por una designación de TRACK (600T250-54) que el
gauge del wall cita para su track (antes: "6\\" metal stud - 600T250-54", un stud rotulado como track). Sintético;
falla con trazabilidad v80v."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trazabilidad as T
walls = {"W1": {"gauge": "25 ga studs; track 600T250-54 per B/X200"}, "W2": {"gauge": "20 ga"},
         "W3": {"gauge": "600S162-43 per X501"}}
its = [("W1", 10.0), ("W2", 5.0), ("W3", 2.0)]
out = T._por_producto('6" metal stud (LF of material)', '6" stud (todos los gauges)', its, walls, {"walls": []})
assert not any("T250" in k for k in out), out
assert "600S162-43" in out, out
tr = T._por_producto('Bottom track 6"', "bottom track (todos)", its, walls, {"walls": []})
assert "600T250-54" in tr, tr                         # el TRACK sí se agrupa por su designación (protección)
print("test_traza_desig_stud OK")
