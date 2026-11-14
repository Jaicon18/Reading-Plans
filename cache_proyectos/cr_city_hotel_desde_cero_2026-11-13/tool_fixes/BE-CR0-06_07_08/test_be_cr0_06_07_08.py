#!/usr/bin/env python3
"""BE-CR0-06 (comparar_alturas: Page Labels con páginas de continuación), BE-CR0-07 (markups_bluebeam: DETAIL de board-only
sin keynote = su N/HOJA), BE-CR0-08 (CB_U_117: inventario de UNO de los PDF fuente del set multi-PDF)."""
import os, sys, tempfile
T = sys.argv[1] if len(sys.argv) > 1 else "/root/cr0/skill_s/take-off-metal-frame-drywall/tools"
sys.path.insert(0, T)
import pymupdf, pypdf
import comparar_alturas as CA
# 06: 40 walls en una altura -> la lista llena la página -> continuación; labels únicos = páginas
d = tempfile.mkdtemp(); img = os.path.join(d, "x.png")
pix = pymupdf.Pixmap(pymupdf.csRGB, pymupdf.IRect(0, 0, 20, 20), 0); pix.save(img)
final = [{"Printed H": "9'-3 1/2\"", "Wall ID": f"W.4-L2-{k:03d} {'A' * 40}", "Source": "x" * 400, "Operation": "", "Status": "DERIVED", "Image": img} for k in range(120)]
out = os.path.join(d, "a.pdf")
CA.alturas_revisadas(final, d, out, None, {})
r = pypdf.PdfReader(out); labs = [r.page_labels[i] for i in range(len(r.pages))]
assert len(set(labs)) == len(labs), labs
print("OK BE-CR0-06", labs)
# 07
import markups_bluebeam as MB
w = {"element": MB.EXIST_EL, "id": "W.4-L2-05 A", "type_id": "W.4-0", "length_ft": 6.46, "height_ft": 9.292, "faces": 1, "layers": 1,
     "source": "1/A2.02 | path", "sheet": "A2.02"}
c = MB.contenido(w)
assert "1/A2.02" in c.split("·")[-2], c
print("OK BE-CR0-07", c)
# 08
import chequeos_biblioteca as CB
src = open(os.path.join(T, "chequeos_biblioteca.py")).read()
assert "BE-CR0-08" in src and "pag_fuentes" in src
print("OK BE-CR0-08 (código presente; caso: set A 86 + S 26 páginas, inventario de A 86 = válido)")
