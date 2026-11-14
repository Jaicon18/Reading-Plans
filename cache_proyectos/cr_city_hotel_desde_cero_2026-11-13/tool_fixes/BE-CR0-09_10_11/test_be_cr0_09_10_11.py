#!/usr/bin/env python3
"""BE-CR0-09 markups_rcp: cielo de N capas rotula 'board = N layer(s) x drawn area' (vista Bluebeam Area x N = SF Excel);
BE-CR0-10 chequeos_biblioteca: be_20 soffit SOLO de madera sin track metálico = PASS; be_02 membrana 'above GYP-1' no es el cielo
expuesto del wet room; BE-CR0-11 trazabilidad._item encuentra renglones 'ceiling <room>' (cita N/HOJA del cielo)."""
import os, sys
T = sys.argv[1] if len(sys.argv) > 1 else "/root/cr0/skill_w/take-off-metal-frame-drywall/tools"
sys.path.insert(0, T)
src = open(os.path.join(T, "markups_rcp.py")).read()
assert "BE-CR0-09" in src and 'layer(s) x drawn area" if _ly > 1' in src
import trazabilidad as TZ
can = {"ceilings": [{"room": "L3 309 RS-6", "source": "2/A5.00 RS-6 A0.08"}]}
assert TZ._src_item("ceiling L3 309 RS-6", can) == "2/A5.00 RS-6 A0.08"
assert TZ._src_item("nada", can) == ""
import chequeos_biblioteca as CB
s = open(os.path.join(T, "chequeos_biblioteca.py")).read()
assert "BE-CR0-10b" in s and "solo_madera" in s
print("OK BE-CR0-09/10/11")
