#!/usr/bin/env python3
"""recortes_walls.py (CR desde cero): imagen circulada por wall board-only (path en rojo + círculo) desde la copia
limpia, reabierta y verificada (tamaño > 0 y píxeles rojos presentes); height_img = la hoja que cita su altura."""
import json, os, re, sys, math
import pymupdf as fitz
from PIL import ImageDraw
from PIL import Image
canon_p, pdf, sheet_map, out = sys.argv[1:5]
c = json.load(open(canon_p)); d = fitz.open(pdf)
pg = {}
for l in open(sheet_map):
    x = [t.strip() for t in l.strip().strip("|").split("|")]
    if len(x) >= 2 and x[0].isdigit():
        pg.setdefault(x[1], int(x[0]) - 1)
os.makedirs(out, exist_ok=True); os.makedirs(os.path.join(out, "sheets"), exist_ok=True)
SH = re.compile(r"\b([A-Z]\d\.\d{2})\b")
hojas = {}
def hoja_img(sh):
    if sh not in hojas and sh in pg:
        p = os.path.join(out, "sheets", f"{sh}.png")
        if not os.path.exists(p):
            d[pg[sh]].get_pixmap(dpi=30).save(p)
        hojas[sh] = p
    return hojas.get(sh)
n = bad = 0
for e in c.get("existing_walls", []):
    if e.get("sheet") not in pg or not e.get("path"):
        continue
    page = d[pg[e["sheet"]]]
    pts = [p for q in (e.get("paths") or [e["path"]]) for p in q]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    r = fitz.Rect(min(xs) - 60, min(ys) - 60, max(xs) + 60, max(ys) + 60) & page.rect
    fn = os.path.join(out, re.sub(r"[^\w.\-]+", "_", e["id"]) + ".png")
    z = 90 / 72.0
    pix = page.get_pixmap(dpi=90, clip=r)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    from PIL import ImageDraw
    dr = ImageDraw.Draw(im)
    T = lambda p: ((p[0] - r.x0) * z, (p[1] - r.y0) * z)
    for q in (e.get("paths") or [e["path"]]):
        dr.line([T(p) for p in q], fill=(255, 0, 0), width=4)
    cx, cy = T(((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2))
    rad = max(14, 0.6 * z * max(max(xs) - min(xs), max(ys) - min(ys)))
    dr.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], outline=(255, 0, 0), width=2)
    im.save(fn)
    im = Image.open(fn).convert("RGB")
    rojos = sum(1 for px in im.getdata() if px[0] > 200 and px[1] < 60 and px[2] < 60)
    if rojos < 5:
        bad += 1; continue
    e["img"] = os.path.relpath(fn, os.path.dirname(canon_p))
    m = SH.search(str(e.get("height_source") or ""))
    hi = hoja_img(m.group(1)) if m else None
    e["height_img"] = os.path.relpath(hi, os.path.dirname(canon_p)) if hi else e["img"]
    n += 1
json.dump(c, open(canon_p, "w"), indent=1, ensure_ascii=False)
print("recortes", n, "sin verificar", bad)
