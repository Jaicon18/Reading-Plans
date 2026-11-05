"""height_img per wall (U-118): circled crop of the printed height source of each type - 1/A500 section note of the type
(studs to deck / to 6" above ceiling) - plus, for E3 faces, the A200 ceiling tag height of the room. Writes the image and sets
walls[].height_img (and faces[].height_img for E3) in the canon. No quantity."""
import json, os
import pymupdf as fitz
from PIL import Image, ImageDraw
K = '/root/cc/work'; P = f'{K}/etapas/4_canon/takeoff_canon.json'
c = json.load(open(P)); doc = fitz.open(f'{K}/plans/bidset_SIN_MARKUPS.pdf')
OUT = f'{K}/etapas/4_canon/img_runner'; os.makedirs(OUT, exist_ok=True)
def crop(pg, term, name, pad=(140, 90), idx=0):
    p = doc[pg]; R = p.rotation_matrix; q = sorted(((x * R) for x in p.search_for(term)), key=lambda r: r.x0)
    if not q: raise SystemExit(f'not found: {term}')
    r = q[idx]; r.normalize()
    clip = fitz.Rect(r.x0 - pad[0], r.y0 - pad[1], r.x1 + pad[0], r.y1 + pad[1]) & p.rect
    pix = p.get_pixmap(dpi=120, clip=clip); im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    s = pix.width / clip.width; d = ImageDraw.Draw(im)
    d.ellipse([(r.x0 - clip.x0 - 10) * s, (r.y0 - clip.y0 - 10) * s, (r.x1 - clip.x0 + 10) * s, (r.y1 - clip.y0 + 10) * s], outline=(255, 0, 0), width=4)
    f = f'{OUT}/{name}.png'; im.save(f); return 'img_runner/' + name + '.png'
T = {"A3": crop(17, "FURRED WALL TO DECK", "height_A3_1A500"), "C3": crop(17, "WALL TO DECK WITH GYPSUM", "height_C3_1A500"),
     "D": crop(17, "WALL WITH GYPSUM BOARD ON BOTH SIDES", "height_D_1A500", idx=0), "E3": crop(17, "WALL WITH GYPSUM BOARD ON BOTH SIDES", "height_E3_1A500", idx=1)}
deck = crop(6, "PLY DECK", "height_deck_A100")
for w in c['walls']:
    w['height_img'] = T[w['tag']] if w['tag'] == 'E3' else deck
    w['height_img_type'] = T[w['tag']]
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
print('height images', len(c['walls']))
