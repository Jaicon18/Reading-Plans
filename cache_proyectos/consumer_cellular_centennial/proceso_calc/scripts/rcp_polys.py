"""etapas/6_markups/rcp_polys.json: restroom C-1 ceiling polygon on A200 = the A100 vector polygon of reading A (A100 and
A200 are both 1/4" = 1'-0"; A200 is offset by dx +37.8 / dy +155.3 pt, registered on 5 identical wall poche rectangles: E3-11 179.9 pt, E3-03 128.8 pt, D-01 138.0 x 10.5 pt, E3-01 123.1 pt); checked by eye on etapas/4_canon/img/rcp_check.png before use."""
import json
import pymupdf as fitz
from PIL import Image, ImageDraw
K = '/root/cc/work'
poly = [[659.0, 890.0], [797.0, 890.0], [797.0, 1002.5], [769.6, 1002.5], [769.6, 1029.5], [643.4, 1029.5]]
DX, DY = 37.8, 155.3
poly = [[x + DX, y + DY] for x, y in poly]
json.dump([{"room": "Unisex Restroom", "polygon": poly}], open(f'{K}/etapas/6_markups/rcp_polys.json', 'w'), indent=1)
d = fitz.open(f'{K}/plans/bidset_SIN_MARKUPS.pdf'); p = d[11]
clip = fitz.Rect(600, 980, 940, 1260); pix = p.get_pixmap(dpi=150, clip=clip)
im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples); dr = ImageDraw.Draw(im); s = pix.width / clip.width
dr.polygon([((x - clip.x0) * s, (y - clip.y0) * s) for x, y in poly], outline=(255, 0, 0), width=4)
im.save(f'{K}/etapas/4_canon/img/rcp_check.png'); print('ok')
