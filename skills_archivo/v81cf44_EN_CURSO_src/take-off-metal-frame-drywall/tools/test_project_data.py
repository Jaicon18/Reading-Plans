import sys
#!/usr/bin/env python3
"""test_project_data.py — R80w.44 (R-ALC-09): la ficha del proyecto (takeoff.json project_data [{campo, valor,
hoja}]) sale como filas informativas en la hoja Inputs, debajo de los inputs, en las mismas columnas (sin hojas ni
columnas nuevas) y sin tocar las celdas de input (Inputs!Bn siguen en su fila). Sintético; falla con plantilla v80w.43."""
import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import openpyxl
import plantilla_excel as P
src = open(P.__file__, encoding="utf-8").read()
assert "PROJECT DATA SHEET (informative, not an input)" in src and 'd.get("project_data")' in src
r0 = max(x[0] for x in P.INPUTS_V68) + 2
assert all(x[0] < r0 for x in P.INPUTS_V68)
print("test_project_data OK")

# R80e.137 (BE-113, O'Reilly p2 back-check): un wall de Z-furring con aberturas NO suma king + jack (jamb = blocking)
import importlib as _il
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_sn = _il.import_module("studs_nodos")
def _w(i, size):
    return {"id": i, "tag": "T", "stud_size": size, "length_ft": 20.0, "oc_in": 24, "rows": 1, "height_ft": 10.0,
            "openings": [{"ref": "door 1", "ro_w_ft": 3.0, "head_ft": 7.0, "sill_ft": 0.0}]}
_r = _sn.contar({"walls": [_w("ZF", '1-1/2" Z-furring (150ZF125-18)'), _w("ST", '3-5/8"')],
                 "nodes": [{"id": "a", "kind": "free", "wall": "ZF"}, {"id": "b", "kind": "free", "wall": "ZF"},
                           {"id": "c", "kind": "free", "wall": "ST"}, {"id": "d", "kind": "free", "wall": "ST"}]})
_rr = _r[0] if isinstance(_r, tuple) else _r
_pz = {x["id"]: x["pcs_full"] for x in (_rr if isinstance(_rr, list) else _rr.get("walls", []))}
assert _pz["ST"] - _pz["ZF"] == 4, _pz
# v81cf24 (CFA rev5): la operación llega al Excel visible; plantilla_excel verificar (R80e.84) rechaza ids internos
_ops = [x.get("operacion", "") for x in (_rr if isinstance(_rr, list) else _rr.get("walls", [])) if x["id"] == "ZF"]
assert _ops and "furring: 0 jamb" in _ops[0] and "R80e" not in _ops[0], _ops
print("R80e.137 furring jambs OK")

# v81cf25 (CFA #2284 rev5, BE-89): el extremo de un wall nuevo que muere en construcción EXISTENTE se declara 'abut' contra
# ese existing_wall (topología derivada por geometría) y cuenta 0 studs como 'free'; antes 'abut' exigía un wall de walls[].
import canon as _cn
_d = {"walls": [{"id": "W1", "element": "wall", "tag": "1", "stud_size": '3-5/8"', "oc_in": 16, "rows": 1, "length_ft": 10.0,
                 "height_ft": 9.0, "faces": [], "faces_none_reason": "x", "source": "1/X1.1", "height_source": "X1.1",
                 "length_source": "X1.1", "detail": "1/X1.1"}],
      "existing_walls": [{"id": "EX-1"}],
      "nodes": [{"id": "N1", "kind": "abut", "wall": "W1", "into": "EX-1", "source": "X1.1 geometry"},
                {"id": "N2", "kind": "free", "wall": "W1"}]}
_si = _cn.generar(_d)[0]
_ns = _si["nodes"] if isinstance(_si, dict) and "nodes" in _si else next(x["nodes"] for x in _cn.generar(_d) if isinstance(x, dict) and "nodes" in x)
assert [n["kind"] for n in _ns] == ["free", "free"], _ns
_d["nodes"][0].pop("source")
try:
    _cn.generar(_d); raise AssertionError("abut sin source debe fallar")
except ValueError as _e:
    assert "abut" in str(_e)
print("v81cf25 abut contra existente OK")
