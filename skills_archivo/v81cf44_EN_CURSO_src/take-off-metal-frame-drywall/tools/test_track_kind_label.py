#!/usr/bin/env python3
"""test_track_kind_label.py — R80w.31 / R80w.32 / R80w.33: (1) con walls[].top_track_kind el top track sale en dos
renglones por tamaño (slip / deflection a estructura vs standard) que suman la familia; (2) OTHER FRAMING se rotula en
inglés llano con su detalle ('Soffit side (16/X502)'), no con la clave del esquema; (3) los textos fijos que el Excel
muestra (Inputs, exclusiones) no hablan del "skill". Sintético; falla con canon / plantilla v80v."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import canon as C
import plantilla_excel as P
data = {"walls": [{"id": "W1", "stud_size": '6"', "top_track_kind": "slip", "top_track_kind_source": "D/X301"},
                  {"id": "W2", "stud_size": '6"', "top_track_kind": "standard", "top_track_kind_source": "C/X301"}]}
co = {"renglones": [{"id": "W:W1", "element": "wall", "bottom_lf": 10.0, "top_lf": 10.0},
                    {"id": "W:W2", "element": "wall", "bottom_lf": 5.0, "top_lf": 5.0}]}
fam = {"bottom track (todos)": 15.0, "top / deflection track (todos)": 15.0}
t = C.track_by_element(data, co, fam)
assert len(t["top"]) == 2 and abs(sum(t["top"].values()) - 15.0) < 1e-6, t
assert any("slip" in k for k in t["top"]) and any("standard" in k for k in t["top"]), t
assert list(t["bottom"].values()) == [15.0], t
try:
    C.track_by_element({"walls": [{"id": "W1", "stud_size": '6"', "top_track_kind": "slip"}]}, co, fam)
    raise SystemExit("top_track_kind sin fuente aceptado")
except ValueError:
    pass
assert P.etiqueta_elemento({"element": "soffit_side", "source": "16/X502"}) == "Soffit side (16/X502)"
txt = " ".join(str(r[4]) for r in P.INPUTS_V68) + " ".join(P.EXCLUIDAS_SIEMPRE.values())
assert "skill" not in txt.lower(), "texto del skill en una celda visible"
print("test_track_kind_label OK")
