"""Circled evidence crop per wall (U-118): band outlined + ellipse in red on the clean sheet; etapas/7_imagenes/walls/<id>.png"""
import json, os, pymupdf
from PIL import Image, ImageDraw
W = '/root/gk/work'
c = json.load(open(f'{W}/etapas/4_canon/takeoff_canon.json')); sm = json.load(open(f'{W}/sheetmap.json'))
doc = pymupdf.open(f'{W}/plans/GK_set_SIN_MARKUPS.pdf')
out = f'{W}/etapas/7_imagenes/walls'; os.makedirs(out, exist_ok=True)
n = 0
for w in c['walls']:
    b = w.get('band') or {}
    if not b.get('sheet'):
        continue
    pg = doc[sm[b['sheet']] - 1]
    r = pymupdf.Rect(b['lo'], b['c0'], b['hi'], b['c1']) if b['ori'] == 'H' else pymupdf.Rect(b['c0'], b['lo'], b['c1'], b['hi'])
    clip = pymupdf.Rect(r.x0 - 70, r.y0 - 70, r.x1 + 70, r.y1 + 70) & pg.rect
    z = 2.0
    pix = pg.get_pixmap(clip=clip, matrix=pymupdf.Matrix(z, z))
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples); d = ImageDraw.Draw(im)
    d.rectangle([(r.x0 - clip.x0) * z, (r.y0 - clip.y0) * z, (r.x1 - clip.x0) * z, (r.y1 - clip.y0) * z], outline=(255, 0, 0), width=4)
    d.ellipse([(r.x0 - clip.x0 - 25) * z, (r.y0 - clip.y0 - 25) * z, (r.x1 - clip.x0 + 25) * z, (r.y1 - clip.y0 + 25) * z], outline=(255, 0, 0), width=4)
    d.text((8, 8), f"{w['id']} ({w.get('tag')}) {b['sheet']}", fill=(255, 0, 0))
    im.save(f"{out}/{w['id']}.png"); n += 1
print(n)
