#!/usr/bin/env python3
"""test_rcp_hatch.py — R80f.16: el polígono de un cielo GWB sigue al HATCH (el cielo = solo el área con hatch,
limitada por las caras): una parte del polígono sin trazos del hatch que toca su borde (caja blanca, rincón fuera del
muro en L) se reporta y markups_rcp sale rc 1; un hueco interior chico (difusor / fan) es una abertura y no se reporta;
el polígono que excluye la parte sin hatch pasa. Sintético; falla con markups_rcp v81cf18 (antes de R80f.16)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pymupdf as fitz
import markups_rcp as MR
doc = fitz.open(); p = doc.new_page(width=400, height=300)
g = (0.5, 0.5, 0.5)
sh = p.new_shape()
for x in range(20, 220, 4):          # hatch 20..220 x 20..120, salvo la caja 160..220 x 20..70 y un hueco 80..90 x 60..70
    for y in range(20, 120, 4):
        if (160 <= x < 220 and 20 <= y < 70) or (80 <= x < 90 and 60 <= y < 70):
            continue
        sh.draw_line((x, y), (x + 1.5, y + 1.0))
sh.finish(color=g, width=0.24); sh.commit()
full = [(20, 20), (220, 20), (220, 120), (20, 120)]
r = MR.sin_hatch(p, full, g)
assert len(r) == 1 and r[0][1][0] >= 155 and r[0][0] > 1500, r
ok = [(20, 20), (160, 20), (160, 70), (220, 70), (220, 120), (20, 120)]
assert MR.sin_hatch(p, ok, g) == [], MR.sin_hatch(p, ok, g)
print("test_rcp_hatch OK")
