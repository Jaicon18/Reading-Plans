#!/usr/bin/env python3
"""test_markups_path.py — R80w.25 / R80w.26: (1) una band con `path` (arco de un soffit curvo, caja abierta de 3 caras)
se dibuja con ESE eje, así Bluebeam mide el largo cargado (antes: cuerda de 2 puntos / caja cerrada de 4 lados);
(2) la metadata del PDF de markups no lleva el nombre de la herramienta (keywords / creator vacíos). Sintético;
falla con markups_bluebeam v80v."""
import os, sys, tempfile, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pymupdf as fitz
import markups_bluebeam as MB
arc = [[100 + 50 * i, 100 + (i % 2) * 20] for i in range(5)]
(r, motivo) = MB.eje_canon({"band": {"ori": "D", "p0": [100, 100], "p1": [300, 100], "path": arc}})
assert r and len(r[0]) == 5 and r[1] is False, (r, motivo)
(r, _) = MB.eje_canon({"band": {"ori": "BOX", "c0": 10, "c1": 40, "lo": 10, "hi": 20,
                                 "path": [[10, 10], [10, 20], [40, 20], [40, 10]]}})
assert len(r[0]) == 4 and r[1] is False, r
d = tempfile.mkdtemp()
doc = fitz.open(); pg = doc.new_page(width=600, height=400); pg.insert_text((20, 30), "X101", fontsize=40)
pdf = os.path.join(d, "b.pdf"); doc.save(pdf)
can = {"constants": {"plan_scale_pt_per_ft": {"value": 18.0, "source": "X101"}},
       "walls": [{"id": "W1", "tag": "T1", "sheet": "X101", "page": 1, "length_ft": 11.0, "height_ft": 9.0,
                  "detail": "TYPE T1/X301", "band": {"ori": "D", "p0": [100, 100], "p1": [300, 100], "path": arc,
                                                     "sheet": "X101"}}]}
cp = os.path.join(d, "c.json"); json.dump(can, open(cp, "w"))
out = os.path.join(d, "m.pdf")
MB.escribir(pdf, cp, out, os.path.join(d, "m.json"))
m = fitz.open(out).metadata
assert not m.get("keywords") and not m.get("creator"), m
assert MB.verificar(out, cp) == [], MB.verificar(out, cp)
print("test_markups_path OK")
