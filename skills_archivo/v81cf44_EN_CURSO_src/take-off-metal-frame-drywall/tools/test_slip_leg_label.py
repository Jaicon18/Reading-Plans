#!/usr/bin/env python3
"""test_slip_leg_label.py — BE-117c (CFA rev4): the slip / deflection top track row names the deflection leg PRINTED in
the head detail (C1/S-801 '3" LONG LEGGED SLOTTED CONT. TRACK'), not a fixed 2" (v81cf10 as delivered)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import canon, familias
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "canon.py"), encoding="utf-8").read()
assert "{leg} deflection leg" in src, "slip label still fixed"
n = canon.TRACK_NOMBRES["slip"][1].format(sz='8"', leg='3"')
assert n == 'Top slip / deflection track 8" (3" deflection leg, walls to structure)', n
assert familias.familia(n, "lf") == "top / deflection track (todos)"
assert canon.TRACK_NOMBRES["slip"][1].format(sz='6"', leg='2"').endswith('(2" deflection leg, walls to structure)')
print("test_slip_leg_label OK")
