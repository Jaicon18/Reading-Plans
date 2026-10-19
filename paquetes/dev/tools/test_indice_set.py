#!/usr/bin/env python3
"""test_indice_set.py — v73 (P05): indice_set arma su propio cache (sin pickles previos) y coteja el indice impreso
contra el title block de cada pagina, sobre un PDF SINTETICO de 4 paginas (ningun proyecto real)."""
import os
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
D = tempfile.mkdtemp(prefix="idx_")
os.environ["TAKEOFF_WORK"] = D
sys.path.insert(0, AQUI)
import pymupdf as fitz  # noqa: E402
import indice_set as I  # noqa: E402

F = []


def ok(n, c):
    print(("OK   " if c else "FALLA"), n)
    c or F.append(n)


pdf = os.path.join(D, "set.pdf")
doc = fitz.open()
p0 = doc.new_page(width=1200, height=800)
p0.insert_text((100, 80), "SHEET INDEX", fontsize=14)
filas = [("Z0.01", "COVER AND INDEX"), ("Z1.01", "FLOOR PLAN"), ("Z5.01", "WALL TYPES"), ("Z9.01", "DETAILS")]
for k, (h, t) in enumerate(filas):
    p0.insert_text((100, 120 + 20 * k), h, fontsize=9)
    p0.insert_text((160, 120 + 20 * k), t, fontsize=9)
p0.insert_text((600, 120), "ISSUED FOR BID 01/02/2030", fontsize=9)
p0.insert_text((1050, 760), "Z0.01", fontsize=30)
for h in ("Z1.01", "Z5.01", "Z5.01"):                 # Z9.01 falta; Z5.01 sale dos veces
    pg = doc.new_page(width=1200, height=800)
    pg.insert_text((300, 300), "SEE 3/Z9.01", fontsize=9)
    pg.insert_text((1050, 760), h, fontsize=30)
doc.save(pdf)
I.PDF = pdf
ok("sin pickles: los arma solo", not os.path.exists(I.WORDS) and I.indice() and os.path.exists(I.WORDS)
   and os.path.exists(I.MAPA))
idx = I.indice()
ok("indice impreso: 4 hojas con titulo", idx == filas)
ok("revision con fecha", I.revisiones() == [("ISSUED FOR BID", "01/02/2030")])
ok("title block por tamano (no la referencia chica)", [h for _, h, _ in I.paginas_por_tamano()] ==
   ["Z0.01", "Z1.01", "Z5.01", "Z5.01"])
fil, av = I.cotejo()
est = {f["hoja"]: f["estado"] for f in fil}
ok("cotejo: Z1.01 CONFIRMADO, Z9.01 y Z5.01 PENDIENTE", est["Z1.01"] == "CONFIRMADO" and est["Z9.01"] == "PENDIENTE"
   and est["Z5.01"] == "PENDIENTE")
ok("avisos dicen faltante y duplicada", any("Z9.01" in a for a in av) and any("Z5.01" in a and "2 paginas" in a for a in av))
print("test_indice_set:", "OK" if not F else f"{len(F)} fallo(s)")
sys.exit(1 if F else 0)
