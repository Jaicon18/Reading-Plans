#!/usr/bin/env python3
"""test_misc_pcs.py — R80w.34: un miembro de stud declarado en misc_items con `pcs` (box header, kicker, brace) entra al
driver de framing screws (4 por pieza) igual que los studs de los walls; antes sumaba LF pero 0 piezas. Sintético;
falla con canon.py v80v."""
import os, sys
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import canon as C
import accesorios as A
fam, filas = defaultdict(float), []
data = {"misc_items": [{"ref": "kicker W1", "familia": '3-5/8" stud (todos los gauges)', "qty": 30.0, "pcs": 3,
                        "source": "C/X301", "op": "3 kickers x 10 = 30"}]}
import inspect
fn = [f for n, f in inspect.getmembers(C, inspect.isfunction) if "misc_items" in inspect.getsource(f) and "fam[it[\"familia\"]]" in inspect.getsource(f)][0]
try:
    fn(data, fam, filas)
except TypeError:
    fn(data, fam, filas, [])
n, det = A.piezas({"filas": filas}, {"walls": []})
assert n == 3, (n, det, filas)
print("test_misc_pcs OK")
