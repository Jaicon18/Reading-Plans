"""burbujas_verificadas.json for the gate: the verifier's _destinos {N/SHEET: {detalle_existe, x, y, x1, y1, img}} also written
under each destination sheet as [{detalle_existe: N, x, y, x1, y1, img}] (format of CE_DETALLES_CIRCULADOS). Original kept."""
import json, shutil, os
K = '/root/cc/work/burbujas'
if not os.path.exists(f'{K}/burbujas_verificadas_lector.json'):
    shutil.copy2(f'{K}/burbujas_verificadas.json', f'{K}/burbujas_verificadas_lector.json')
b = json.load(open(f'{K}/burbujas_verificadas_lector.json'))
for nt, d in (b.get('_destinos') or {}).items():
    if not d.get('detalle_existe'):
        continue
    if nt.count('/') != 1:
        continue
    n, h = nt.split('/')
    lst = b.setdefault(h, [])
    if not any(str(x.get('detalle_existe')) == n for x in lst):
        lst.append({"detalle_existe": n, "x": d['x'], "y": d['y'], "x1": d.get('x1'), "y1": d.get('y1'), "img": d['img'], "title": d.get('title')})
json.dump(b, open(f'{K}/burbujas_verificadas.json', 'w'), indent=1, ensure_ascii=False)
print(sum(1 for d in b['_destinos'].values() if d.get('detalle_existe')), 'destinations')
# A100 SHEET SYMBOLS: the partition diamond '#' = 'SEE SHEET A500 FOR WALL CONFIGURATION, CONSTRUCTION AND INSULATION DETAILS'
# (legend printed on A100) and general note 2 'FOR ALL PARTITION CONNECTION DETAILS (TOP AND BOTTOM) SEE SHEET A500': every
# partition tag on A100 is a reference to 1/A500 -> recorded as an eye-verified reference with its circled legend crop
import pymupdf as fitz
from PIL import Image, ImageDraw
d = fitz.open('/root/cc/work/plans/bidset_SIN_MARKUPS.pdf'); p = d[6]; R = p.rotation_matrix
r = (p.search_for('SEE SHEET A500 FOR')[0] * R); r.normalize()
clip = fitz.Rect(r.x0 - 120, r.y0 - 40, r.x1 + 160, r.y1 + 60) & p.rect
pix = p.get_pixmap(dpi=150, clip=clip); im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples); s = pix.width / clip.width
ImageDraw.Draw(im).ellipse([(r.x0 - clip.x0 - 90) * s, (r.y0 - clip.y0 - 25) * s, (r.x1 - clip.x0 + 20) * s, (r.y1 - clip.y0 + 25) * s], outline=(255, 0, 0), width=4)
os.makedirs(f'{K}/img_verif', exist_ok=True); im.save(f'{K}/img_verif/A100_leyenda_A500.png')
b = json.load(open(f'{K}/burbujas_verificadas.json'))
lst = b.setdefault('A100', [])
if not any(x.get('hoja') == 'A500' for x in lst):
    lst.append({"x": round((r.x0 + r.x1) / 2, 1), "y": round((r.y0 + r.y1) / 2, 1), "img": "img_verif/A100_leyenda_A500.png", "n": "1", "hoja": "A500",
                "dibujo": "A100 SHEET SYMBOLS: partition diamond = 'SEE SHEET A500 FOR WALL CONFIGURATION, CONSTRUCTION AND INSULATION DETAILS' (1/A500 PARTITION TYPES); A100 general note 2"})
json.dump(b, open(f'{K}/burbujas_verificadas.json', 'w'), indent=1, ensure_ascii=False)
print('A100 -> 1/A500 reference added')
# destination of the A100 legend reference: 1/A500 PARTITION TYPES title on A500
p5 = d[17]; R5 = p5.rotation_matrix; q = sorted((x * R5 for x in p5.search_for('PARTITION TYPES')), key=lambda r: r.x0)
t = q[0]; t.normalize()
clip = fitz.Rect(t.x0 - 80, t.y0 - 40, t.x1 + 80, t.y1 + 40) & p5.rect
pix = p5.get_pixmap(dpi=150, clip=clip); im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples); s = pix.width / clip.width
ImageDraw.Draw(im).ellipse([(t.x0 - clip.x0 - 50) * s, (t.y0 - clip.y0 - 18) * s, (t.x1 - clip.x0 + 12) * s, (t.y1 - clip.y0 + 18) * s], outline=(255, 0, 0), width=4)
im.save(f'{K}/img_verif/A500_destino_1.png')
b = json.load(open(f'{K}/burbujas_verificadas.json'))
l5 = b.setdefault('A500', [])
if not any(str(x.get('detalle_existe')) == '1' for x in l5):
    l5.append({"detalle_existe": "1", "x": round(t.x0 - 30, 1), "y": round((t.y0 + t.y1) / 2, 1), "x1": round(t.x1, 1), "y1": round(t.y1, 1), "img": "img_verif/A500_destino_1.png", "title": "1 PARTITION TYPES"})
json.dump(b, open(f'{K}/burbujas_verificadas.json', 'w'), indent=1, ensure_ascii=False)
print('A500 destination 1 added')
