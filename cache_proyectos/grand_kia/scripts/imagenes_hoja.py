"""Grand Kia: one PNG per marked sheet, rendered from the delivered Bluebeam PDF WITH its markups (U-158 name:
'<SHEET> - IMAGE ONLY (not editable) - walls|ceilings|walls and ceilings revN.png'). Image only; the editable file is the PDF.
Usage: imagenes_hoja.py <markups.pdf> <out_dir> <rev>"""
import sys, os, json
import pymupdf as fitz
pdf, out, rev = sys.argv[1:4]
sm = json.load(open('/root/gk/work/sheetmap.json'))
PAG = {}
for k, v in sm.items():
    if isinstance(v, int) and ' ' not in k:
        PAG.setdefault(v, k)
WALLS = {'A111', 'A112', 'A113', 'A150', 'A108', 'A109', 'A200', 'A220'}
CEIL = {'A131', 'A132', 'A133', 'A130'}
doc = fitz.open(pdf)
n = 0
for i, p in enumerate(doc):
    h = PAG.get(i + 1)
    if not h or h not in WALLS | CEIL:
        continue
    if not list(p.annots()):
        continue
    kind = 'walls' if h in WALLS else 'ceilings'
    if h in ('A108', 'A109'):
        kind = 'walls'
    pix = p.get_pixmap(dpi=100, annots=True)
    pix.save(os.path.join(out, f"{h} - IMAGE ONLY (not editable) - {kind} {rev}.png")); n += 1
print(n, 'sheet images')
