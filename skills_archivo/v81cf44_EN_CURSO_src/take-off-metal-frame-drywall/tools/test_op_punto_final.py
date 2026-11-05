#!/usr/bin/env python3
"""test_op_punto_final.py — R80w.13: una operación escrita que termina la frase con punto ("... / 18 = 15.85. Tagged ...")
no rompe chequeos_v73.r73_8 (antes: ValueError float('15.85.') y TODAS las reglas A_R73_* fallaban por excepción).
Sintético; falla con chequeos_v73 v80v. La regla sigue detectando una operación que no cuadra."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chequeos_v73 as C

bien = {"walls": [{"id": "W-1", "length_ft": 15.85, "length_op": "(1996.7 - 1711.4) / 18 = 15.85. Tagged on two sheets"}]}
assert C.r73_8(bien) == [], C.r73_8(bien)
mal = {"walls": [{"id": "W-2", "length_ft": 15.85, "length_op": "(1996.7 - 1711.4) / 18 = 12.5. note"}]}
assert C.r73_8(mal), "operación que no cuadra no detectada"
dec = {"walls": [{"id": "W-3", "length_ft": 0.5, "length_op": "9 / 18 = .5"}]}
assert C.r73_8(dec) == [], C.r73_8(dec)
print("test_op_punto_final OK")
