#!/usr/bin/env python3
"""test_curved_molding.py — R80w.35: el tramo curvo del perímetro de un drywall grid lleva su molding CURVA impresa
(moldings.curved {ft, source}) y sale de la molding recta; el renglón cae en su propia familia y se compra por pieza.
Sintético; falla con canon / familias / plantilla v80v."""
import os, sys
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import canon as C
import familias as F
import plantilla_excel as P
c = {"room": "R1", "system": "usg_grid", "area_sf": 100.0, "perimeter_ft": 40.0, "ns_ft": 10.0, "ew_ft": 10.0,
     "board": "5/8 type X", "source": "X121", "hanger_drop_ft": {"value": 10.0, "source": "X121"},
     "main_oc_in": {"value": 48, "source": "X121"}, "cross_oc_in": {"value": 16, "source": "X121"},
     "moldings": {"value": ["angle"], "source": "spec X", "curved": {"ft": 15.0, "source": "spec X curved molding"}}}
fam, filas = defaultdict(float), []
C._ceilings({"ceilings": [c]}, fam, filas)
assert fam[C.F_AM] == 25.0 and fam[C.F_CURV] == 15.0, dict(fam)
assert F.familia("Brand SC1 curved perimeter molding at the circle", "lf") == C.F_CURV
assert P.clase_compra({"material": "Brand SC1 curved perimeter molding", "unit": "LF", "metal": False}, {})[0].startswith("molding")
print("test_curved_molding OK")
