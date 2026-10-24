import sys, json, pymupdf as fitz
pdf, pno, js, out = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
clip = None
if len(sys.argv) > 5: clip = fitz.Rect(*map(float, sys.argv[5].split(',')))
dpi = int(sys.argv[6]) if len(sys.argv) > 6 else 60
d = fitz.open(pdf); p = d[pno-1]
R = json.load(open(js))
pix = p.get_pixmap(dpi=dpi, clip=clip)
import PIL.Image as I, PIL.ImageDraw as D
im = I.frombytes('RGB', (pix.width, pix.height), pix.samples); dr = D.Draw(im)
z = dpi/72; ox, oy = (clip.x0, clip.y0) if clip else (0, 0)
for i, r in enumerate(R):
    if not (18 < r['w'] < 30 and 18 < r['h'] < 30): continue
    x, y = (r['cx']-ox)*z, (r['cy']-oy)*z; rad = 16*z
    dr.ellipse([x-rad, y-rad, x+rad, y+rad], outline=(255, 0, 0), width=3)
    dr.text((x+rad, y-rad), str(r.get('id', i)), fill=(255, 0, 0))
im.save(out)
