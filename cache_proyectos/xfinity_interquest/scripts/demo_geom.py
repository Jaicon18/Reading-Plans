"""etapas/4_canon/demo_geom.json: one polyline per demolition element on A1.0 (DEMOLITION FLOOR PLAN, page 4), visible frame pt,
taken from the band of each canon misc_items DEMO-* (the A1.0 vector band reading A wrote: dashed double line of A1.0 key 7):
  H band -> axis y = (c0 + c1) / 2 from x = lo to hi;  V band -> axis x = (c0 + c1) / 2 from y = lo to hi.
LF of the polyline is re-measured at the printed 1/4" = 1'-0" (18 pt/ft) and must equal the canon lf (|d| <= 0.02 ft).
Checked by eye on etapas/4_canon/img/demo_check.png (re-opened after writing). No quantity is created here."""
import json, math, os, sys
import pymupdf as fitz
from PIL import Image, ImageDraw
K = os.environ.get("K") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
c = json.load(open(os.path.join(K, "etapas/4_canon/takeoff_canon.json")))
sm = json.load(open(os.path.join(K, "etapas/SHEET_MAP.json")))
PAG = {v: int(k) for k, v in sm.items()}
S = float(c["constants"]["plan_scale_pt_per_ft"]["value"])
out, mal = [], []
for m in c["misc_items"]:
    if not m["ref"].startswith("DEMO"):
        continue
    b = m["band"]
    ax = (b["c0"] + b["c1"]) / 2
    pl = [[b["lo"], ax], [b["hi"], ax]] if b["ori"] == "H" else [[ax, b["lo"]], [ax, b["hi"]]]
    lf_m = math.dist(*pl) / S
    if abs(lf_m - float(m["lf"])) > 0.02:
        mal.append(f"{m['ref']}: polyline {lf_m:.3f} ft vs canon {m['lf']}")
    out.append({"id": m["ref"], "group": "partition", "page": PAG[b["sheet"]], "sheet": b["sheet"], "polyline": pl,
                "lf": m["lf"], "h_ft": m["height_ft"], "height_source": m.get("height_source"),
                "h_status": m.get("height_status", "") + " - " + str(m.get("height_source") or ""),
                "layers": 1, "sf": m["qty"], "detail": str(m.get("source") or b["sheet"]),
                "keynote": str(m.get("source") or "A1.0 key 7"), "length_op": m.get("length_op"),
                "band_source": "canon misc_items " + m["ref"] + ".band (" + str(m.get("length_source") or "")[:160] + ")"})
if mal:
    sys.exit("demo polylines vs canon LF: " + "; ".join(mal))
json.dump(out, open(os.path.join(K, "etapas/4_canon/demo_geom.json"), "w"), indent=1)
d = fitz.open(os.path.join(K, "plans/bidset_SIN_MARKUPS.pdf"))
p = d[PAG["A1.0"] - 1]
xs = [q[0] for e in out for q in e["polyline"]]
ys = [q[1] for e in out for q in e["polyline"]]
clip = fitz.Rect(min(xs) - 80, min(ys) - 80, max(xs) + 80, max(ys) + 80)
pix = p.get_pixmap(dpi=110, clip=clip)
im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
dr = ImageDraw.Draw(im)
s = pix.width / clip.width
for e in out:
    pts = [((x - clip.x0) * s, (y - clip.y0) * s) for x, y in e["polyline"]]
    dr.line(pts, fill=(255, 0, 0), width=4)
    dr.text((pts[0][0] + 4, pts[0][1] - 14), e["id"], fill=(255, 0, 0))
os.makedirs(os.path.join(K, "etapas/4_canon/img"), exist_ok=True)
f = os.path.join(K, "etapas/4_canon/img/demo_check.png")
im.save(f)
assert Image.open(f).size[0] > 300
print(len(out), "demo elements on A1.0;", round(sum(e["sf"] for e in out), 2), "SF (canon)")
