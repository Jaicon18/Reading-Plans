#!/usr/bin/env python3
"""test_fasteners_canon.py — R80w.37: con `fasteners_excluded` (decisión del estimador "excluye toda la tornillería",
R80e.77) los fasteners del canon (misc_items de familias de tornillería / anclajes: TEK, cement board screws, #10
framing screws impresos, P.A.F., anchors) también quedan en 0 con la nota EXCLUDED y lo calculado antes; los
materiales que no son fasteners (clip angle, deep-leg track, board) siguen cargados. Sintético; falla con canon v80w.36."""
import os, sys
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import canon as C
mi = [{"ref": "tek", "familia": "#10 framing screws (printed)", "qty": 100, "unit": "pcs", "source": "B/X200", "op": "50 x 2"},
      {"ref": "cbs", "familia": "cement board screws", "qty": 40, "unit": "pcs", "source": "F/X301", "op": "x"},
      {"ref": "clip", "familia": "clip angle (bracing / nested connections)", "qty": 6, "unit": "pcs", "source": "3/X501", "op": "6"},
      {"ref": "dlt", "familia": "deep-leg slotted deflection track (printed)", "qty": 11, "unit": "lf", "source": "1/X501", "op": "11"}]
data = {"misc_items": mi, "fasteners_excluded": {"why": "fasteners (estimator standing rule)", "source": "estimator standing rule 2026-10-31"}}
fam, filas = defaultdict(float), []
C._parapets_blocking(data, fam, filas, [])
assert fam["#10 framing screws (printed)"] == 0 and fam["cement board screws"] == 0, dict(fam)
assert fam["clip angle (bracing / nested connections)"] == 6 and fam["deep-leg slotted deflection track (printed)"] == 11, dict(fam)
ex = [f for f in filas if str(f.get("operacion")).startswith("EXCLUDED")]
assert len(ex) == 2 and "computed before the exclusion = 100" in ex[0]["operacion"], filas
fam2 = defaultdict(float)
C._parapets_blocking({"misc_items": mi}, fam2, [], [])
assert fam2["#10 framing screws (printed)"] == 100, dict(fam2)
assert not C.es_fastener("clip angle (bracing / nested connections)") and C.es_fastener("Kwik HUS-EZ anchors")
print("test_fasteners_canon OK")
