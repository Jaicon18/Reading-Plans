"""Agrega al PDF de markups los walls perimetrales EXISTING - EXCLUDED (rev1, decisión RFI-01): gris punteado,
Subject "EXISTING - EXCLUDED", sin contar en totales (NM con prefijo TOX-, fuera del set que verifica markups_bluebeam).
Uso: python3 bitacora.py run scripts/markups_existing.py <tools_dir> <markups.pdf> <existing_excluded.json>"""
import json, os, sys
sys.path.insert(0, sys.argv[1])
import pymupdf as fitz
import markups_bluebeam as MB
pdf, ex = sys.argv[2], json.load(open(sys.argv[3]))
doc = fitz.open(pdf)
geo, sin, _ = MB.geometria(ex, doc)
n = 0
for w in ex["walls"]:
    g = geo.get(w["id"])
    if not g:
        continue
    txt = (f"EXISTING - EXCLUDED · type {w['tag']} · {w['length_ft']:.2f} LF (not counted) · {w['detail']} · {w['id']} · "
           f"1/DM-101 legend + key note 3, A-101 legend, A-002 (RFI-01)")
    a = MB._annot(doc, doc[g["page"]], g["pts"], (0.55, 0.55, 0.55), (4, 3), "EXISTING - EXCLUDED", txt,
                  "Take-off (existing)", "TOX-" + w["id"])
    n += 1
tmp = pdf + ".tmp.pdf"
doc.save(tmp, garbage=3, deflate=True)
doc.close()
os.replace(tmp, pdf)
print(f"EXISTING - EXCLUDED: {n} annots added ({len(sin)} without geometry)")
sys.exit(0 if n == len(ex["walls"]) else 1)
