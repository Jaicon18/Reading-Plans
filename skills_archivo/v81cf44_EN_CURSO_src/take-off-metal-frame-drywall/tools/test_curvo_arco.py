#!/usr/bin/env python3
"""test_curvo_arco.py — R80w.14: un elemento CURVO (band D con `curved`) se mide por el ARCO; R72.2 (diagonal = promedio
de sus dos caras) no le aplica la cuerda, pero exige la operación del arco. Sintético; falla con chequeos_v72 v80v."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chequeos_v72 as C

base = {"constants": {"plan_scale_pt_per_ft": {"value": 18.0, "source": "X101"}}}
curvo = dict(base, walls=[{"id": "W-C", "length_ft": 40.0, "length_status": "DERIVADO",
                           "length_op": "arc = r x theta = 10.0 x 4.0 rad = 40.0 ft",
                           "band": {"ori": "D", "p0": [0, 0], "p1": [360, 0], "curved": "arc of a round soffit",
                                    "faces_top": [[0, 0], [360, 0]], "faces_bottom": [[0, 10], [360, 10]]}}])
assert C.r72_2(curvo) == [], C.r72_2(curvo)
sin_op = dict(base, walls=[dict(curvo["walls"][0], length_op="40 ft")])
assert C.r72_2(sin_op), "curvo sin operación del arco no detectado"
recto = dict(base, walls=[{"id": "W-D", "length_ft": 40.0, "length_status": "DERIVADO",
                           "band": {"ori": "D", "faces_top": [[0, 0], [360, 0]], "faces_bottom": [[0, 10], [360, 10]]}}])
assert C.r72_2(recto), "diagonal recta con largo distinto del promedio de caras no detectada (protección)"
print("test_curvo_arco OK")
