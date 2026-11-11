"""height_img per wall / face (U-118), Xfinity - Interquest: circled crop of the PRINTED height source, from the clean PDF.
 - W2 walls: 2/A2.0 WALL TYPE 2 / 2A note '... FROM SLAB TO 6" ABOVE CEILING U.N.O.' (A2.0 p5);
 - each face: the A3.0 (p6) ceiling tag of its room: RETAIL '2x4 ACT 12'-0" AFF', STORAGE '2x4 ACT 10'-0" AFF',
   HALLWAY 'EXISTING GYP. BD. 9'-0" AFF';
 - column wraps CF-01 / CF-02: 5/A2.0 column furring detail ('FINISH CORNER L BEAD', 5/8" Type X over 2 1/2" studs)
   + the retail tag for the face.
The term is located by text search on the page (rotation_matrix -> visible frame); the occurrence used is the one nearest to
the hint point read on the rendered sheet. Writes etapas/4_canon/img_runner/height_*.png and sets walls[].height_img,
walls[].height_img_type and faces[].height_img in the canon. Every image is re-opened (size check) after writing. No quantity."""
import json, os, re
import pymupdf as fitz
from PIL import Image, ImageDraw
K = os.environ.get("K") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(K, "etapas", "4_canon", "takeoff_canon.json")
c = json.load(open(P))
doc = fitz.open(os.path.join(K, "plans", "bidset_SIN_MARKUPS.pdf"))
OUT = os.path.join(K, "etapas", "4_canon", "img_runner")
os.makedirs(OUT, exist_ok=True)


def crop(pg, term, hint, name, pad=(150, 90), extra=None):
    """pg 1-based; circled crop of the occurrence of `term` nearest to `hint` (visible pt); extra = second term of the same
    note to grow the circle (multi-line notes)."""
    p = doc[pg - 1]
    R = p.rotation_matrix
    def near(t):
        q = [fitz.Rect(x * R) for x in p.search_for(t)]
        for r in q:
            r.normalize()
        if not q:
            raise SystemExit(f"not found on page {pg}: {t}")
        return min(q, key=lambda r: abs(r.x0 - hint[0]) + abs(r.y0 - hint[1]))
    r = near(term)
    if extra:
        r |= near(extra)
    clip = fitz.Rect(r.x0 - pad[0], r.y0 - pad[1], r.x1 + pad[0], r.y1 + pad[1]) & p.rect
    pix = p.get_pixmap(dpi=130, clip=clip)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    s = pix.width / clip.width
    d = ImageDraw.Draw(im)
    d.ellipse([(r.x0 - clip.x0 - 12) * s, (r.y0 - clip.y0 - 10) * s, (r.x1 - clip.x0 + 12) * s, (r.y1 - clip.y0 + 10) * s],
              outline=(255, 0, 0), width=4)
    f = os.path.join(OUT, name + ".png")
    im.save(f)
    chk = Image.open(f)                       # re-opened: the crop exists and is not empty
    assert chk.size[0] > 200 and chk.size[1] > 100, f
    return f


W2 = crop(5, "FROM SLAB TO 6\"", (1292, 603), "height_W2_type_2A2.0", extra="CEILING U.N.O.")
CF = crop(5, "FINISH CORNER 'L' BEAD", (2142, 1269), "height_CF_5A2.0", pad=(200, 150))
TAG = {"Retail": crop(6, "12'-0\" AFF", (1206, 1954), "height_ceiling_retail_12-0_A3.0"),
       "Storage": crop(6, "10'-0\" AFF", (429, 1420), "height_ceiling_storage_10-0_A3.0"),
       "Hallway": crop(6, "9'-0\" AFF", (432, 1712), "height_ceiling_hallway_9-0_A3.0")}
n = 0
for w in c["walls"]:
    typ = CF if w.get("tag") == "CF" else W2
    w["height_img_type"] = typ
    w["height_img"] = typ
    for f in w.get("faces") or []:
        room = str(f.get("room") or "")
        k = next((k for k in TAG if re.search(k, room, re.I)), None)
        if k:
            f["height_img"] = TAG[k]
    n += 1
json.dump(c, open(P, "w"), indent=1, ensure_ascii=False)
print("height images:", n, "walls;", ", ".join(os.path.basename(x) for x in [W2, CF] + list(TAG.values())))
