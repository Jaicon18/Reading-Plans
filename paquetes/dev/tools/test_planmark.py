#!/usr/bin/env python3
"""test_planmark.py — v73: los 6 tests obligatorios del contrato de planmark.py (referencias/herramientas.md) sobre
un PDF SINTÉTICO (página rotada 90°, walls dibujados como dos líneas paralelas): ningún proyecto real."""
import os
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
D = tempfile.mkdtemp(prefix="pm_")
os.environ["PLANMARK_CACHE"] = os.path.join(D, "cache")
import pymupdf as fitz  # noqa: E402
import planmark as P  # noqa: E402

F = []


def ok(n, c):
    print(("OK   " if c else "FALLA"), n)
    c or F.append(n)


def pdf(path, extra=False):
    doc = fitz.open()
    pg = doc.new_page(width=400, height=600)          # sin rotar 400 x 600; mostrada (rot 90) 600 x 400
    pg.set_rotation(90)
    M = pg.derotation_matrix
    for (x0, y0, x1, y1) in ((100, 100, 500, 100), (100, 108, 500, 108),      # wall H (mostrada) y 100..108
                             (300, 150, 300, 350), (308, 150, 308, 350)):     # wall V x 300..308
        pg.draw_line(fitz.Point(x0, y0) * M, fitz.Point(x1, y1) * M, width=2)
    if extra:
        pg.draw_line(fitz.Point(50, 380) * M, fitz.Point(60, 380) * M, width=1)
    doc.save(path)


A, B = os.path.join(D, "a.pdf"), os.path.join(D, "b.pdf")
pdf(A)
pdf(B, extra=True)
OKS = [{"id": "WH", "band": {"ori": "H", "c0": 100, "c1": 108, "lo": 100, "hi": 500}, "lf": 22.2, "tagged": True},
       {"id": "WV", "band": {"ori": "V", "c0": 300, "c1": 308, "lo": 150, "hi": 350}, "lf": 11.1, "tagged": True}]
h = P.Hoja(A, 1, 72)
r = h.verify(OKS)
ok("1 factor correcto: todos pasan", all(v >= 0.04 for _, v in r))
h2 = P.Hoja(A, 1, 72)
h2.F = 1.37
out2 = os.path.join(D, "t2.jpg")
try:
    h2.overview(OKS * 3, "x", out2)
    ok("2 factor equivocado aborta", False)
except P.MarcaRechazada as e:
    ok("2 factor equivocado aborta con diagnóstico", "factor" in str(e))
ok("2 no escribe archivo", not os.path.exists(out2))
malo = {"id": "FAKE", "band": {"ori": "H", "c0": 300, "c1": 306, "lo": 400, "hi": 560}, "lf": 8.0}
out3 = os.path.join(D, "t3.jpg")
try:
    h.overview(OKS * 4 + [malo], "x", out3)
    ok("3 tag inventado aborta", False)
except P.MarcaRechazada as e:
    ok("3 tag inventado aborta y lo nombra (puntual)", "FAKE" in str(e) and "puntuales" in str(e))
ok("3 no escribe archivo", not os.path.exists(out3))
try:
    P.Hoja(A, 1, 72, w_pt=400.0, h_pt=600.0)
    ok("4 dimensiones sin rotar dan ScaleError", False)
except P.ScaleError:
    ok("4 dimensiones sin rotar dan ScaleError", True)
tr = {"ori": "V", "c0": 100, "c1": 108, "lo": 100, "hi": 500}           # banda H con el punto transpuesto
try:
    h.verify([{"id": "T", "band": tr, "lf": 1}])
    ok("5 punto transpuesto aborta", False)
except P.MarcaRechazada:
    ok("5 punto transpuesto aborta", True)
ok("6 dos PDFs, misma página y dpi: dos PNG distintos", P.Hoja(A, 1, 72).png != P.Hoja(B, 1, 72).png)
o = os.path.join(D, "ov.jpg")
h.overview(OKS, "test", o)
ok("overview escribe con marcas buenas", os.path.exists(o))
s = os.path.join(D, "sh.jpg")
h.sheet(OKS, s)
ok("sheet escribe contact sheet", os.path.exists(s))
print("test_planmark:", "OK" if not F else f"{len(F)} fallo(s)")
sys.exit(1 if F else 0)
