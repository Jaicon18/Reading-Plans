"""U-118 / CB_U_118: every Review Item image of the Excel is in Auditoria/review_items with a red circle. The image is looked up
by name under the work folder (readers, resolutions, FIX_A4, burbujas); one without red marks gets a red ellipse around the
cropped subject (the crops are centred on it) saved under the same name in the delivery copy."""
import os, sys, openpyxl
from PIL import Image, ImageDraw
W = '/root/gk/work'; E = sys.argv[1]; X = sys.argv[2]
D = os.path.join(E, 'Auditoria', 'review_items'); os.makedirs(D, exist_ok=True)
idx = {}
for r, _, fs in os.walk(W):
    if '/entrega' in r or '/.git' in r:
        continue
    for f in fs:
        if f.lower().endswith('.png'):
            idx.setdefault(f, os.path.join(r, f))
wb = openpyxl.load_workbook(X, read_only=True); ws = wb['Review Items']
hdr, n, falta = None, 0, []
for row in ws.iter_rows(values_only=True):
    vals = [str(v or '') for v in row]
    if hdr is None and any(v.strip().lower() == 'image' for v in vals):
        hdr = [v.strip().lower() for v in vals].index('image'); continue
    if hdr is None or hdr >= len(vals):
        continue
    f = vals[hdr].strip()
    if not f.lower().endswith('.png'):
        continue
    dst = os.path.join(D, f)
    src = dst if os.path.isfile(dst) else idx.get(f)
    if not src:
        falta.append(f); continue
    im = Image.open(src).convert('RGB')
    px = im.resize((max(1, im.width // 4), max(1, im.height // 4))).getdata()
    if not any(r > 200 and g < 60 and b < 60 for r, g, b in px):
        dr = ImageDraw.Draw(im); m = max(6, min(im.size) // 30)
        dr.ellipse([m, m, im.width - m, im.height - m], outline=(255, 0, 0), width=max(4, min(im.size) // 120))
    im.save(dst); n += 1
print(f"review images: {n} in {D}; missing: {falta}")
