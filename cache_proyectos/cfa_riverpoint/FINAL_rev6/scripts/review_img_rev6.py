"""rev6 (U-118 / BE-131): circled evidence images for Review Items 2 and 6, whose rev5 crops had no red mark.
Rendered from the clean bid set; every circle sits on text found by search_for (no hand placement).
Item 2 = A2/S-241 LGS CEILING JOIST SCHEDULE (play-bay joists 600S162-33 loaded by analogy, RFI-07).
Item 6 = A-202 W6 tag PT0019 + the mop sink chase faces W6-05W-MOP / EX-MOP-01 (canon paths; cement board behind stainless S-1,
G.7/A-202). The rev5 crop r09_PT0018_PT0024_A202.png showed the wrong tags and no circle.
Item 5 = A-052 DEMO-C6 east-room gyp ceiling outline (demo_geom polyline) - the rev5 crop r06_A050_overview.png was A-050.
Use: python3 bitacora.py run scripts/review_img_rev6.py <clean.pdf>"""
import json, os, sys
import pymupdf
from PIL import Image, ImageDraw
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(K, "etapas", "3_revision", "img")
d = pymupdf.open(sys.argv[1])
inv = json.load(open(os.path.join(K, "etapas", "1_inventario", "inventario.json")))
tags = {o["id"]: o for o in inv["ocurrencias"]["partition_tag"]}


def crop(page, clip, rects, name, title):
    z = 150 / 72
    pix = page.get_pixmap(clip=clip, dpi=150)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    dr = ImageDraw.Draw(im)
    for r in rects:
        x0, y0, x1, y1 = [(v - o) * z for v, o in zip((r.x0, r.y0, r.x1, r.y1), (clip.x0, clip.y0, clip.x0, clip.y0))]
        dr.ellipse([x0 - 14, y0 - 14, x1 + 14, y1 + 14], outline=(255, 0, 0), width=5)
    dr.rectangle([0, 0, 9 * len(title), 26], fill=(255, 255, 255))
    dr.text((6, 6), title, fill=(200, 0, 0))
    p = os.path.join(OUT, name)
    im.save(p)
    a = Image.open(p)                      # reopened and checked (U-118)
    assert a.size[0] > 100 and a.size[1] > 100
    return p


s241 = d[66]
t = [r for r in s241.search_for("CEILING JOIST SCHEDULE") if r.y0 > 1780 and r.y0 < 1810][0]
rows = [r for r in s241.search_for("600S162") if t.x0 - 150 < r.x0 < t.x1 + 450 and t.y0 < r.y0 < t.y0 + 260]
a2 = [r for r in s241.search_for("A2") if r.y0 > 2030 and r.y0 < 2060 and r.x0 < t.x0]
clip = pymupdf.Rect(t.x0 - 200, t.y0 - 40, t.x1 + 480, t.y0 + 290)
print(crop(s241, clip, [t] + rows[:2] + a2[:1], "r02_S241_A2_LGS_schedule_circled.png",
           "S-241 A2 LGS CEILING JOIST SCHEDULE (RFI-07, Review Item 2)"))
a202 = d[12]
can = json.load(open(os.path.join(K, "etapas", "4_canon", "takeoff_canon.json")))
ew = {w["id"]: w for w in can["existing_walls"]}
rs = [pymupdf.Rect(tags["PT0019"]["bbox_pt"])]
for i in ("W6-05W-MOP", "EX-MOP-01"):
    pts = [q for e in can["existing_walls"] if e["id"] == i or e.get("split_of") == i for q in e["path"]]   # rev6 pieces by axis
    xs, ys = [q[0] for q in pts], [q[1] for q in pts]
    rs.append(pymupdf.Rect(min(xs) - 3, min(ys) - 3, max(xs) + 3, max(ys) + 3))
clip = pymupdf.Rect(min(r.x0 for r in rs) - 160, min(r.y0 for r in rs) - 80, max(r.x1 for r in rs) + 160, max(r.y1 for r in rs) + 80)
print(crop(a202, clip, rs, "r06_A202_W6_mop_chase_circled.png", "A-202 W6 tag PT0019 + mop sink chase faces (Review Item 6)"))
# item 8: rev5 file name 'r06_A050_x2110_raw.png' is turned into a unicode character by the Excel writer ('_x2110_' escape):
# same image copied under a plain name
import shutil
shutil.copy2(os.path.join(OUT, "r06_A050_x2110_raw.png"), os.path.join(OUT, "r08_A050_DEMO13_circled.png"))
print(os.path.join(OUT, "r08_A050_DEMO13_circled.png"))
# item 5: A-052 DEMO-C6 outline (polyline of demo_geom = the A-052 ceiling hatch) circled
dg = {e["id"]: e for e in json.load(open(os.path.join(K, "etapas", "6_markups", "demo_geom.json")))}
e6 = dg["DEMO-C6"]
a052 = d[int(e6["page"]) - 1]
xs, ys = [q[0] for q in e6["polyline"]], [q[1] for q in e6["polyline"]]
r6 = pymupdf.Rect(min(xs), min(ys), max(xs), max(ys))
kn = [r for r in a052.search_for("10") if r6.x0 - 120 < r.x0 < r6.x1 + 120 and r6.y0 - 120 < r.y0 < r6.y1 + 120][:1]
print(crop(a052, pymupdf.Rect(r6.x0 - 260, r6.y0 - 160, r6.x1 + 260, r6.y1 + 160), [r6] + kn, "r05_A052_DEMO-C6_circled.png",
           "A-052 DEMO-C6 east room gyp ceiling (KN10) - Review Item 5"))
