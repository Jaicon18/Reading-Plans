#!/usr/bin/env python3
"""Tests de familias.py v62 (arbitraje #11 + #12). Correr: python3 test_familias.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from familias import familia  # noqa: E402


def test_plywood_liner_no_es_sill():
    assert familia("FRT plywood 3/4\" opening liner (jambs/head/sill, 1 ply) - EAST (grid 8)", "lf") != "sill track"
    assert familia("Sill track 600T125 (R.O.+1'-4\") - EAST (grid 8)", "lf") == "sill track"
    assert familia("Header / box beam CFMF (R.O.+1'-4\") - EAST (grid 8)", "lf") == "header / box beam"


def test_plywood_no_es_gyp_regular_12():
    """#12A/#12B: '5/8" FRT plywood ... backboards' caía en 5/8" gyp regular."""
    for n in ("5/8\" FRT plywood (fire-retardant treated) backboards", "5/8\" FRT plywood nailbase (bonded polyiso)"):
        assert familia(n, "sf") == "FRT plywood (SF)", (n, familia(n, "sf"))
    assert familia("5/8\" gypsum board regular Type X (walls)", "sf") == "5/8\" gyp board regular (walls + ceilings)"


def test_framed_opening_no_es_stud_12():
    """#12A/#12B: 'Framed opening ... (3-5/8" metal stud)' caía en 3-5/8" stud."""
    for n in ("Framed opening - MEP ceiling (3-5/8\" metal stud)", "Framed openings MEP, light slots (3-5/8\" stud)",
              "Framed opening 6\" stud at duct"):
        assert familia(n, "lf") == "framed openings MEP", (n, familia(n, "lf"))
    assert familia("3-5/8\" metal stud 362S137-33 (LF of material)", "lf") == "3-5/8\" stud (todos los gauges)"
    assert familia("6\" parapet infill stud 600S162-54", "lf") == "6\" parapet stud"


if __name__ == "__main__":
    n = 0
    for k, f in list(globals().items()):
        if k.startswith("test_") and callable(f):
            f()
            n += 1
            print("OK", k)
    print(f"{n} tests OK")
