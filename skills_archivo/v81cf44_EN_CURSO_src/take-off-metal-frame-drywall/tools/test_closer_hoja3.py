#!/usr/bin/env python3
"""test_closer_hoja3.py — R80w.16: closer.py acepta hojas de 3 dígitos SIN guion (X301, X602, S200) y con sufijo de
letra (X421.A) en las citas N/HOJA de partidas, fuentes CONFIRMADO y header_source. Sintético; falla con closer v80v
(solo X12.01 / X-410: todo set numerado X301 quedaba sin poder sellar)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import closer
from closer import Wall, Val, CierreRechazado

w = Wall(1, "T1", "room 1 north (X421)")
w.partida("STUD", Val(10, "DERIVADO", operacion="ROUNDUP(...) per D/X301"), "pcs")
w.partida("BOARD:Room", Val(5, "DERIVADO", operacion="L x H per 3/X426.A"), "SF")
v = Val(12.5, "CONFIRMADO", fuente="X421 printed 12'-6\"")
w.abertura("puerta", "D1", 3.33, 7.17, head="6/X602", header="steel_by_others", header_source="6/X602 steel header")
try:
    w.partida("TRACK_TOP", Val(1, "DERIVADO", operacion="no sheet cited"), "LF")
    raise SystemExit("partida sin cita aceptada (protección)")
except CierreRechazado:
    pass
assert closer.RE_HOJA.search("X421.A") and closer.RE_HOJA.search("S200") and closer.RE_HOJA.search("X-410")
print("test_closer_hoja3 OK")
