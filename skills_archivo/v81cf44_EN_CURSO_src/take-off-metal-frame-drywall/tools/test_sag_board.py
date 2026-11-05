#!/usr/bin/env python3
"""test_sag_board.py — v81cf8 T2 (BE-CF15): board key "5/8 ceiling sag-resistant" -> family '5/8" gyp ceiling board
SAG-RESISTANT' in canon (BOARD_FAM, FAMS, optional), familias.py, plantilla name, finishing driver and ALC-11 (a
ceiling-type board was carried as "5/8 regular" with only a note). Fails with v81cf7."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import canon, familias, accesorios, plantilla_excel as P, alcances
F = "5/8\" gyp ceiling board SAG-RESISTANT"
assert canon.BOARD_FAM.get("5/8 ceiling sag-resistant") == F
assert F in canon.FAMS and F not in canon.OBLIGATORIAS
assert familias.familia("5/8\" gypsum ceiling board, SAG-RESISTANT (ceiling type)", "sf") == F
assert familias.familia("5/8\" gypsum board, regular", "sf") == "5/8\" gyp board regular (walls + ceilings)"
assert F in accesorios.BOARD_DRIVER
assert "SAG-RESISTANT" in P.NOMBRES_PLANTILLA[F]
assert any(a[0] == "ALC-11" and F in a[3] for a in alcances.ALCANCES)
print("test_sag_board OK")
