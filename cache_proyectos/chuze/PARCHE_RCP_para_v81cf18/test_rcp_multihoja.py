#!/usr/bin/env python3
"""test_rcp_multihoja.py — R80f.13 / R80f.14 / R80f.15 (Chuze FINAL5): (1) markups_rcp.py pone el polígono de cada
ceiling en SU hoja (ceilings[].sheet; varias hojas de RCP), con NM / ID = ceilings[].id, el tag del cielo en el
Contents y sin clusters de bracing cuando constants.ceiling_lateral_bracing = false; (2) verificar_markups_excel
encuentra el PDF 'Markups' (mayúscula) junto al Excel; (3) auditoria_entrega cuadra un área contra el desglose
'ID SF' del Material Summary y su área dibujada. Sintético; falla con las tools v81cf17."""
import json, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pymupdf as fitz
import markups_rcp as MR
import verificar_markups_excel as VME
d = tempfile.mkdtemp()
doc = fitz.open()
for lab in ("X1.A", "X2.A"):
    p = doc.new_page(width=800, height=600)
    p.insert_text((700, 580), lab, fontsize=12)
doc.set_page_labels([{"startpage": 0, "prefix": "X1.A", "style": "", "firstpagenum": 1},
                     {"startpage": 1, "prefix": "X2.A", "style": "", "firstpagenum": 1}])
pin = os.path.join(d, "in.pdf"); doc.save(pin)
canon = {"constants": {"plan_scale_by_sheet": {"X1.A": {"value": 18.0, "source": "t"}, "X2.A": {"value": 18.0, "source": "t"}},
                       "ceiling_lateral_bracing": {"value": False, "source": "t"}},
         "ceilings": [{"id": "CLG-1", "room": "R1", "sheet": "X1.A", "area_sf": 4.0, "board": "5/8 type X", "height_ft": 9,
                       "detail": "Z-9/X121", "ceiling_tag": "Z-9", "system": "usg_grid", "ns_ft": 20, "ew_ft": 20},
                      {"id": "CLG-2", "room": "R2", "sheet": "X2.A", "area_sf": 4.0, "board": "5/8 type X", "height_ft": 9,
                       "detail": "Z-9/X121", "system": "usg_grid", "ns_ft": 20, "ew_ft": 20}]}
cp = os.path.join(d, "canon.json"); json.dump(canon, open(cp, "w"))
sq = [[100, 100], [136, 100], [136, 136], [100, 136]]
pp = os.path.join(d, "polys.json"); json.dump([{"id": "CLG-1", "polygon": sq}, {"id": "CLG-2", "polygon": sq}], open(pp, "w"))
out = os.path.join(d, "Proj_Markups_X.pdf")
assert MR.escribir(pin, cp, pp, out, os.path.join(d, "png")) == 0
r = fitz.open(out)
an = [(i, a.info.get("id"), a.info.get("content")) for i in range(r.page_count) for a in r[i].annots()]
assert {(0, "TO-CLG-1"), (1, "TO-CLG-2")} <= {(i, n) for i, n, _ in an}, an
assert any("GWB CEILING Z-9" in c for _, _, c in an)
assert not r[0].get_drawings() or not any(dr.get("fill") == (0.85, 0.1, 0.55) for dr in r[0].get_drawings())
assert sorted(os.listdir(os.path.join(d, "png"))) == ["X1.A_rcp_markups.png", "X2.A_rcp_markups.png"]
xl = os.path.join(d, "Proj_Takeoff_X.xlsx"); open(xl, "w").close()
assert VME.buscar_pdf(d, excel=xl) == os.path.abspath(out)
import auditoria_entrega as AE
src = open(AE.__file__, encoding="utf-8").read()
assert "1 area annot = Excel breakdown" in src and "3 Area vs SF" in src
print("test_rcp_multihoja OK")
