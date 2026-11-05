#!/usr/bin/env python3
"""test_grid_moldings.py — R80w.23 / R80w.24: (1) un drywall grid cuyo spec imprime UNA sola molding (angle) no carga
la channel molding duplicada (`moldings {value, source}` en el ceiling); sin el campo, las dos como antes. (2) el nombre
del renglón del Material Summary sale del producto impreso (constants.product_names -> familias_out.nombres_familia
-> plantilla). Sintético; falla con canon.py / plantilla_excel.py v80v."""
import os, sys
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import canon as C
import plantilla_excel as P
base = {"room": "R1", "system": "usg_grid", "area_sf": 100.0, "perimeter_ft": 40.0, "ns_ft": 10.0, "ew_ft": 10.0,
        "board": "5/8 type X", "source": "X121", "hanger_drop_ft": {"value": 10.0, "source": "X121"},
        "main_oc_in": {"value": 48, "source": "X121"}, "cross_oc_in": {"value": 16, "source": "X121"}}
def corre(c):
    fam, filas = defaultdict(float), []
    C._ceilings({"ceilings": [c]}, fam, filas)
    return fam
f = corre(dict(base, moldings={"value": ["angle"], "source": "spec 09 51 23 one angle molding"}))
assert f[C.F_AM] == 40.0 and f[C.F_CM] == 0.0, dict(f)
f = corre(dict(base))
assert f[C.F_AM] == 40.0 and f[C.F_CM] == 40.0, "sin moldings: las dos (protección)"
try:
    corre(dict(base, moldings={"value": ["angle"]}))
    raise SystemExit("moldings sin source aceptado")
except ValueError:
    pass
fo = {"nombres_familia": {C.F_MT: "Brand X main tee HD1 (spec X)"}}
assert P.nombre_plantilla(C.F_MT, fo) == "Brand X main tee HD1 (spec X)"
assert P.nombre_plantilla(C.F_CT, fo) == P.NOMBRES_PLANTILLA[C.F_CT], "sin override: nombre de la plantilla"
print("test_grid_moldings OK")
