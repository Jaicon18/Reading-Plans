#!/usr/bin/env python3
"""test_z_size_label.py — v81cf8 T1 (BE-CF16): the Z-furring row of the Material Summary shows the PRINTED size (a 2"
Z channel was labelled "1-1/2" Z-furring"). canon.py writes nombres_contexto.z_size from constants.z_furring_size or
the walls' stud_size; plantilla_excel.nombre_plantilla uses it; absent = old label. Fails with v81cf7."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plantilla_excel as P
F = "1-1/2\" Z-furring"
assert P.nombre_plantilla(F, {"nombres_contexto": {"z_size": "2\""}}) == "2\" Z-furring channel (LF of material)"
assert P.nombre_plantilla(F, {"nombres_contexto": {}}) == "1-1/2\" Z-furring channel (LF of material)"
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "canon.py"), encoding="utf-8").read()
assert '"z_size"' in src and "z_furring_size" in src, "canon.py does not emit nombres_contexto.z_size"
print("test_z_size_label OK")
