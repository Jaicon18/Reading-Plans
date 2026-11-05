"""etapas/4_canon/demo_geom.json: one polyline per demolition element on D100 (visible frame, pt), from the D100 vector
coordinates reading A wrote in each DEMO item's length_source; checked by eye on etapas/4_canon/img/demo_check.png."""
import json, re
import pymupdf as fitz
from PIL import Image, ImageDraw
K = '/root/cc/work'
c = json.load(open(f'{K}/etapas/4_canon/takeoff_canon.json'))
G = {"DEMO-01": [[1050.6, 1376.0], [1855.4, 1376.0]], "DEMO-06": [[838.2, 1516.2], [1865.0, 1516.2]]}
for r, x in (("DEMO-02", 1224.1), ("DEMO-03", 1410.6), ("DEMO-04", 1580.6), ("DEMO-05", 1677.5)):
    G[r] = [[x, 1379.6], [x, 1513.0]]
out = []
for m in c['misc_items']:
    if not m['ref'].startswith('DEMO'):
        continue
    out.append({"id": m['ref'], "group": "partition" if m['ref'] != 'DEMO-06' else "furring", "page": 5, "sheet": "D100",
                "polyline": G[m['ref']], "lf": m['lf'], "h_ft": m['height_ft'], "h_status": "DERIVED - " + m['height_source'],
                "layers": 1, "sf": m['qty'], "detail": "1/D100", "keynote": "D100 keynote " + str(m.get('source_info') or m.get('source') or '').split('key')[-1].strip()})
json.dump(out, open(f'{K}/etapas/4_canon/demo_geom.json', 'w'), indent=1)
d = fitz.open(f'{K}/plans/bidset_SIN_MARKUPS.pdf'); p = d[4]
clip = fitz.Rect(780, 1300, 1920, 1580); pix = p.get_pixmap(dpi=100, clip=clip)
im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples); dr = ImageDraw.Draw(im); s = pix.width / clip.width
for e in out:
    pts = [((x - clip.x0) * s, (y - clip.y0) * s) for x, y in e['polyline']]
    dr.line(pts, fill=(255, 0, 0), width=4); dr.text((pts[0][0] + 4, pts[0][1] - 14), e['id'], fill=(255, 0, 0))
im.save(f'{K}/etapas/4_canon/img/demo_check.png'); print(len(out), 'demo elements')
