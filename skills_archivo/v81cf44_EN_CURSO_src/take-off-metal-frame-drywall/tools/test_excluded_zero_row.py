#!/usr/bin/env python3
"""test_excluded_zero_row.py — R80w.38: una familia del canon que el estimador EXCLUYE (fila con operación
"EXCLUDED - ...", p. ej. los fasteners del canon con fasteners_excluded, R80w.37) sale en el Material Summary con
NET 0 y su nota, en vez de desaparecer; una familia en 0 sin exclusión sigue sin renglón. Sintético; falla con
plantilla_excel v80w.36."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import familias
import plantilla_excel as P
fo = {"filas": [{"familia": "cement board screws", "ref": "x", "source": "F/X301",
                 "operacion": "EXCLUDED - fasteners (rule); computed before the exclusion = 40"}],
      "unidades": {"cement board screws": "pcs", "1/4\" gypsum board (printed)": "sf"}}
fam_canon = {"cement board screws": 0.0, "1/4\" gypsum board (printed)": 0.0}
out = P.familias_faltantes([], fo, fam_canon, {"familias": {}}, familias)
assert [m["familia"] for m in out] == ["cement board screws"] and out[0]["net"] == 0.0, out
print("test_excluded_zero_row OK")
