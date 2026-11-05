#!/usr/bin/env python3
"""test_track_por_estructura.py — R80w.36: la familia del top track de un wall sale de si sus studs llegan a estructura
(height_ft >= deck_height), no de la letra del head / top_track_kind declarado. (1) wall con head 'standard' declarado
pero studs al deck -> slip; (2) wall por debajo del deck -> standard; (3) zona de altura al deck (from_x / to_x en pt,
plan_scale_by_sheet) -> esa parte del top LF a slip, el resto standard; Σ = familia. Sintético; falla con canon v80w.35."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import canon as C
data = {"deck_height": {"value": 20.0, "source": "X201"},
        "constants": {"plan_scale_by_sheet": {"X1": {"value": 10.0, "source": "X1 title"}},
                      "slip_track_rule": {"value": "slip where studs reach structure", "source": "spec 09 22 16; D/X301"}},
        "walls": [{"id": "W1", "sheet": "X1", "stud_size": '6"', "height_ft": 20.0, "length_ft": 10.0,
                   "top_track_kind": "standard", "top_track_kind_source": "C/X301"},
                  {"id": "W2", "sheet": "X1", "stud_size": '6"', "height_ft": 10.0, "length_ft": 5.0,
                   "top_track_kind": "standard", "top_track_kind_source": "C/X301"},
                  {"id": "W3", "sheet": "X1", "stud_size": '6"', "height_ft": 10.0, "length_ft": 8.0,
                   "height_zones_info": [{"from_x": 100.0, "to_x": 130.0, "height_ft": 20.0}],
                   "top_track_kind": "standard", "top_track_kind_source": "C/X301"}]}
co = {"renglones": [{"id": "W:W1", "element": "wall", "bottom_lf": 10.0, "top_lf": 10.0},
                    {"id": "W:W2", "element": "wall", "bottom_lf": 5.0, "top_lf": 5.0},
                    {"id": "W:W3", "element": "wall", "bottom_lf": 8.0, "top_lf": 8.0}]}
fam = {"bottom track (todos)": 23.0, "top / deflection track (todos)": 23.0}
t = C.track_by_element(data, co, fam)
slip = sum(v for k, v in t["top"].items() if "slip" in k)
std = sum(v for k, v in t["top"].items() if "standard" in k)
assert abs(slip - 13.0) < 1e-6, t      # W1 10 + W3 zone 30 pt / 10 = 3
assert abs(std - 10.0) < 1e-6, t       # W2 5 + W3 rest 5
assert abs(sum(t["top"].values()) - 23.0) < 1e-6 and list(t["bottom"].values()) == [23.0], t
tr = C.top_track_tramos(data["walls"][0], data, 10.0)
assert list(tr) == ["slip"] and "D/X301" in tr["slip"][1], tr
print("test_track_por_estructura OK")
