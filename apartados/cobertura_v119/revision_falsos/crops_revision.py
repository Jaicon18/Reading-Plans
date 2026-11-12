"""crops de revisión: por cada fila ROJO de un CSV de cobertura -> <out>/<id>_ctx.png (radio 12 ft) y <id>_zoom.png (radio 4 ft),
círculo rojo en (x, y). uso: crops.py pdf csv out [ids...]"""
import sys, csv, os, fitz
from PIL import Image, ImageDraw
sys.path.insert(0, "/tmp/v119/take-off-metal-frame-drywall/tools"); import compuerta_entrega as ce
pdf, cs, out = sys.argv[1:4]; ids = set(sys.argv[4:])
os.makedirs(out, exist_ok=True)
doc = fitz.open(pdf); pags = {(p.get_label() or str(i + 1)): p for i, p in enumerate(doc)}
for r in csv.DictReader(open(cs)):
    if r["tipo"] != "muro" or r["estado"] != "ROJO" or ids and r["id"] not in ids:
        continue
    pg = pags[r["hoja"]]; esc = ce.cob_escala(doc, pg); x, y = float(r["x"]), float(r["y"])
    L = float(r["largo_ft"]) * esc
    for tag, rad, px in (("ctx", max(12 * esc, 0.7 * L), 900), ("zoom", 4 * esc, 700)):
        dpi = int(min(600, px / (2 * rad) * 72))
        clip = fitz.Rect(x - rad, y - rad, x + rad, y + rad) * pg.rotation_matrix; clip.normalize(); clip &= pg.rect
        f = os.path.join(out, f"{r['id']}_{tag}.png")
        pg.get_pixmap(dpi=dpi, clip=clip).save(f)
        q = fitz.Point(x, y) * pg.rotation_matrix; k = dpi / 72; R = 1.3 * esc * k
        im = Image.open(f).convert("RGB"); dr = ImageDraw.Draw(im)
        cx, cy = (q.x - clip.x0) * k, (q.y - clip.y0) * k
        dr.ellipse((cx - R, cy - R, cx + R, cy + R), outline=(255, 0, 0), width=3); im.save(f)
print("ok")
