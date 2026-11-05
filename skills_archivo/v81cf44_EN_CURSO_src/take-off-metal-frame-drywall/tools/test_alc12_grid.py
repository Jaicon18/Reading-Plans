#!/usr/bin/env python3
"""test_alc12_grid.py — R80w.15: ALC-12 (ceiling suspension) se cierra cuantificado con un drywall suspension grid
completo (main tee + cross tee + hanger wire) aunque furring / carrying channel = 0; un sistema incompleto sigue
fallando. Sintético; falla con alcances.py v80v (no existe alc12_ok y exigía furring + carrying siempre)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import alcances as A
fam12 = [x for x in A.ALCANCES if x[0] == "ALC-12"][0][3]
grid = {"USG drywall main tee (DGLW26)": 10.0, "USG drywall cross tee (DGLW424)": 20.0, "hanger wire": 30.0,
        "track de ceilings / soffits": 5.0}
assert A.alc12_ok(grid, fam12), "grid completo no aceptado"
hat = {"furring channel": 1.0, "carrying channel": 1.0, "hanger wire": 1.0, "track de ceilings / soffits": 1.0}
assert A.alc12_ok(hat, fam12), "sistema de hat channel completo no aceptado (protección)"
assert not A.alc12_ok({"USG drywall main tee (DGLW26)": 10.0, "hanger wire": 3.0}, fam12), "grid sin cross tee aceptado"
assert not A.alc12_ok({"furring channel": 1.0, "hanger wire": 1.0, "track de ceilings / soffits": 1.0}, fam12), \
    "hat channel sin carrying aceptado"
print("test_alc12_grid OK")
