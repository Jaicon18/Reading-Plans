#!/usr/bin/env python3
"""test_markups_excel.py — R80f.7 / BE-117: verificar_markups_excel.py (compuerta A_MARKUPS_EXCEL) pasa con markups =
Excel = escala impresa y falla con (1) un LF del Excel distinto, (2) /Measure con otra escala que la impresa, (3) una
hoja con elementos del canon sin markups. Sintético (PDF de 2 hojas, Excel mínimo)."""
import json
import subprocess
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import openpyxl  # noqa: E402
import pymupdf as fitz  # noqa: E402
import markups_bluebeam as MB  # noqa: E402
import verificar_markups_excel as V  # noqa: E402

d = tempfile.mkdtemp()
doc = fitz.open()
for h in ("X101", "X102"):
    pg = doc.new_page(width=800, height=500)
    pg.insert_text((600, 470), h, fontsize=30)
    pg.insert_text((40, 470), "FLOOR PLAN  SCALE: 1/4\" = 1'-0\"", fontsize=10)
bid = os.path.join(d, "bid.pdf")
doc.save(bid)
W = {"id": "W1", "tag": "T1", "sheet": "X101", "page": 1, "length_ft": 11.111, "height_ft": 9.0, "detail": "1/X301",
     "band": {"ori": "H", "c0": 99, "c1": 101, "lo": 100, "hi": 300, "sheet": "X101"}}
can = {"constants": {"plan_scale_pt_per_ft": {"value": 18.0, "source": "X101 1/4\" = 1'-0\""},
                     "plan_scale_by_sheet": {"X101": {"value": 18.0, "source": "X101 1/4\" = 1'-0\""}}},
       "walls": [W]}
cp = os.path.join(d, "canon.json")
json.dump(can, open(cp, "w"))
mk = os.path.join(d, "6_markups", "markups.pdf")
MB.escribir(bid, cp, mk, os.path.join(d, "6_markups", "markups.json"))


def excel(p, lf=11.111):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Partition Takeoff"
    ws.append(["PARTITION TAKEOFF"])
    ws.append(["Partition / Scope", "Wall #", "Length (LF)", "Height (FT)", "Layers", "Stud Size", "Stud O.C. (in)",
               "Board (SF)", "Location", "Source (DETAIL/SHEET)", "Status"])
    ws.append(["TYPE T1"])
    ws.append(["T1  #W1  -  room", "W1", lf, 9.0, 1, "3-5/8\"", 16, round(11.111 * 9, 2), "room", "1/X301", "[DERIVED]"])
    ms = wb.create_sheet("Material Summary")
    ms.append(["MATERIAL SUMMARY"])
    ms.append(["Material", "Unit", "Net", "Waste %", "Waste", "Purchase", "Selling unit", "Pieces to buy",
               "Where it comes from", "Yield check (live formula)"])
    wb.save(p)
    return p


xl = excel(os.path.join(d, "ok.xlsx"))
f, lin, res = V.verificar(mk, xl, cp)
assert f == [] and res["annots"] == 1 and len(lin) == 1 and lin[0].startswith("OK"), (f, lin)
assert V.buscar_pdf(d, cp, None) == os.path.abspath(mk)

# (1) LF del Excel distinto
f, _, _ = V.verificar(mk, excel(os.path.join(d, "lf.xlsx"), lf=12.5), cp)
assert any("LF 11.11 != Excel 12.5" in x for x in f), f

# (2) /Measure con 1/8" = 1'-0" (9 pt/ft) sobre una hoja impresa a 1/4"
mal = os.path.join(d, "escala.pdf")
dd = fitz.open(mk)
for a in dd[0].annots():
    MB._measure(dd, a, 9.0)
dd.save(mal)
f, _, _ = V.verificar(mal, xl, cp)
assert any("/Measure" in x and "!= escala de la hoja 18.0" in x for x in f), f
# escala del canon que no es la impresa
c2 = json.loads(json.dumps(can))
c2["constants"]["plan_scale_by_sheet"]["X101"]["value"] = 9.0
cp2 = os.path.join(d, "canon_esc.json")
json.dump(c2, open(cp2, "w"))
f, _, _ = V.verificar(mk, xl, cp2)
assert any("rótulo SCALE" in x for x in f), f

# (3) hoja X102 con elementos en el canon y sin markups
c3 = json.loads(json.dumps(can))
c3["walls"].append(dict(W, id="W2", sheet="X102", page=2, band=dict(W["band"], sheet="X102")))
cp3 = os.path.join(d, "canon_hoja.json")
json.dump(c3, open(cp3, "w"))
f, _, _ = V.verificar(mk, xl, cp3)
assert any(x.startswith("hoja X102") for x in f) and any(x.startswith("W2:") for x in f), f

# CLI: rc 1 con falla, rc 0 bien, reporte de una línea por anotación
rep = os.path.join(d, "r.md")
assert V.main(["v", mk, xl, cp, "--out", rep]) == 0
assert "- OK   | p.1 X101 W1 |" in open(rep, encoding="utf-8").read()
assert V.main(["v", mal, xl, cp]) == 1

# compuerta de reglas.py registrada
import reglas  # noqa: E402
assert "A_MARKUPS_EXCEL" in reglas.CHEQUEOS
shutil.rmtree(d, ignore_errors=True)
# R80e.136 (O'Reilly 3-nov): revision_markups.py (revisión rápida VERDE/ROJA + mapa de alturas) — su test sintético
_rm = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "revision_markups.py"),
                      "--selftest"], capture_output=True, text=True)
assert _rm.returncode == 0 and "OK selftest revision_markups" in _rm.stdout, _rm.stdout + _rm.stderr
print("test_markups_excel OK")

# v81cf25 (CFA #2284 rev5): revision_markups (BE-119) con los rótulos reales de markups_bluebeam / markups_demo y alturas
# DERIVADAS de valores impresos. Antes: 86 RED de 87 (SF leído del campo 'N face(s)', TYPE board-only / OTHER FRAMING
# distinto del encabezado del Excel, Depth comparada contra la primera cota de la cita en vez de la operación impresa).
import revision_markups as _RMv
assert _RMv._derivada("A-202 note C.1 framing 6\" above adjacent ceiling: kitchen C.H.10'-2\" (A-221) + 0.5 = 10.667 ft") == 10.667
assert _RMv._derivada("hanger studs from the soffit bottom C.H. 9'-8\" (A-221) to the B.O. structure 12'-8\" (S-201 C4: T.O. 14'-8\" - 24\" TJS) = 3'-0\"") == 3.0
assert _RMv._derivada("A-202 note G.11 6\" above finish ceiling 10'-2\" - 1 ft base = 9.667 ft") == 9.667
assert _RMv._derivada("D3/A-624 B.O. gypsum bd 7'-0\" A.F.F. to serving ACT 10'-0\" (A-221) + 6\" min = 3.5 ft") == 3.5
assert _RMv._derivada("A-611 CEILING 9'-4\" - T/TILE 6'-8 1/2\" = 2.625 ft") == 2.625
assert _RMv._derivada("C.H. 10'-2\" + 0.5 = 11.0 ft") is None                      # operación que no da el resultado escrito
assert _RMv.altura_impresa("A-050 KN16 '1/2\" DUROCK from floor to 18\" A.F.F. typical in kitchen'")[0] == 1.5
assert _RMv.altura_impresa("A-202 note C.1 6\" above kitchen C.H.10'-2\" (A-221) = 10.667 ft [DERIVED]", "DERIVADO")[0] == 10.667
print("revision_markups v81cf25 (rótulos reales + alturas derivadas) OK")
import tempfile as _tf, pymupdf as _pm
_d = _pm.open(); _pg = _d.new_page(width=600, height=400)
for _k, _c in enumerate(("BOARD ONLY - NO FRAMING · 19.31 LF · H 0'-5\" · 1 face(s) · 8.05 SF board · A-621 note A.6 · W6-01N-CB",
                         "DEMO · 16.73 LF · H 12'-4\" · 2 layer(s) · 412.74 SF · KN3 DERIVED · DEMO-01 · KN3 A-050")):
    _a = _pg.add_polyline_annot([(50, 50 + 40 * _k), (300, 50 + 40 * _k)]); _a.set_info(content=_c); _a.update()
_p = _tf.mktemp(suffix=".pdf"); _d.save(_p)
_mk = {m["id"]: m for m in _RMv.leer_markups(_p)[1]}
assert _mk["W6-01N-CB"]["sf_txt"] == 8.05 and _mk["W6-01N-CB"]["sf_board"], _mk
assert _mk["DEMO-01"]["sf_txt"] == 412.74 and not _mk["DEMO-01"]["sf_board"], _mk
print("revision_markups v81cf25 rótulos board-only / demo OK")
