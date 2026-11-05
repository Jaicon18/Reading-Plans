#!/usr/bin/env python3
"""test_markups_board_sf.py — BE-117 (user 3-nov): the SF in the Contents of a wall markup is the BOARD SF of its
Excel row (faces x height x layers), not LF x H (the old Contents showed LF x H instead of the board SF of the row)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import markups_bluebeam as MB
w = {"id": "W1", "tag": "A1", "element": "wall", "length_ft": 14.167, "height_ft": 10.667, "detail": "1/A-501", "sheet": "A-101",
     "faces": [{"side": "A", "room": "K", "board": "1/2 cement board", "layers": 1, "height_ft": 10.5}]}
ct = MB.contenido(w)
assert "148.75 SF board" in ct, ct
w2 = dict(w, faces=[])
assert "151.1 SF" in MB.contenido(w2), MB.contenido(w2)
print("test_markups_board_sf OK")
