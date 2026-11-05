#!/usr/bin/env python3
"""test_spec_items.py — R80w.41 / R80w.42 / R80w.43 (spec sweep): (1) familias impresas nuevas: malla álcali-
resistente en juntas de cement backer y sealer gasket bajo runners estructurales (familia propia, no 'joint tape' /
'cement board' / track; compra en rollo, waste no metal); (2) el producto impreso de un trim item y el grado /
recubrimiento de una designación (constants.product_specs) parten / rotulan el renglón; (3) una fila de bracing a
<= 12" del tope en los walls con slip track (constants.bracing_top_row_at_structure) = +1 fila x LF de slip.
Sintético; falla con las tools v80w.40."""
import os, sys
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import canon as C
import familias as F
import plantilla_excel as P
import trazabilidad as T
n1 = P.NOMBRE_PLANTILLA["alkali-resistant mesh tape (printed)"] if hasattr(P, "NOMBRE_PLANTILLA") else None
for fam in ("alkali-resistant mesh tape (printed)", "sealer gasket (printed)"):
    assert fam in C.FAMS
    nm = P.nombre_plantilla(fam, {})
    assert F.familia(nm, "lf") == fam, (nm, F.familia(nm, "lf"))
    assert P.clase_compra({"unit": "LF", "material": nm, "metal": False})[0] == "roll (LF)"
can = {"constants": {"product_specs": {"600S162-33": {"value": "ASTM A1003 G60", "source": "05 40 00 2.3.B"}}},
       "trim_items": [{"ref": "t1", "kind": "corner_bead", "lf": 5.0},
                      {"ref": "t2", "kind": "corner_bead", "lf": 3.0, "product": {"value": "curved-edge cornerbead", "source": "09 29 00 2.6.A.2.g"}}],
       "misc_items": [{"ref": "m1", "familia": '6" stud (todos los gauges)', "qty": 10, "op": "600S162-33 frame", "source": "2/X131"}]}
g = T._por_producto("METAL trim", "metal trim (corner bead, casing, shadow molding)", [("t1", 5.0), ("t2", 3.0)], {}, can)
assert set(g) == {"corner bead", "curved-edge cornerbead"}, g
g = T._por_producto('6" metal stud', '6" stud (todos los gauges)', [("m1", 10.0)], {}, can)
assert list(g) == ["600S162-33 ASTM A1003 G60"], g
data = {"deck_height": {"value": 20.0}, "constants": {"bracing_top_row_at_structure": {"value": True, "source": "09 22 16 2.2.C.1"}},
        "walls": [{"id": "W1", "height_ft": 20.0, "length_ft": 10.0}, {"id": "W2", "height_ft": 10.0, "length_ft": 5.0}]}
co = {"renglones": [{"id": "W:W1", "element": "wall", "top_lf": 10.0}, {"id": "W:W2", "element": "wall", "top_lf": 5.0}]}
fam, filas = defaultdict(float), []
C._bracing_top_row(data, co, fam, filas)
assert fam["bracing C.R. channel"] == 10.0 and len(filas) == 1, (dict(fam), filas)
print("test_spec_items OK")
