"""A3.0 (REFLECTED CEILING PLAN, page 6) room outlines and the SOF-01 header, measured on the A3.0 VECTORS of the clean PDF.

Outputs
 - etapas/6_markups/rcp_polys.json  : input of markups_rcp.py = the misc entry SOF-01-BOARD (gyp header strip, line along its axis,
                                       canon soffit_header_info.band; depth = canon SOF-01-BOARD SF / band LF = developed width);
                                       no ceilings[] in the canon (no new gypsum board ceiling: ACT and existing gyp only).
 - etapas/6_markups/rcp_cuartos.json: U-159 / U-160 table, one row per room printed on A3.0 (100-104 + LANDLORD ROOM N.I.C.), all
                                       'exclusion' with the printed reason and its sheet, the room polygon (visible frame, pt) and
                                       its source; read by scripts/excluded_rcp.py and by the delivery gate CE_RCP_CUARTOS.
 - etapas/4_canon/img/rcp_check.png  : A3.0 crop with every polygon drawn (re-opened and checked).

Measurement (#0 honesty: DERIVADO, vector at the printed 1/4" = 1'-0" = 18 pt/ft): A3.0 wall faces = edges of the filled wall poche
and the 0.72 pt wall outlines (get_drawings, rotation_matrix -> visible frame). For each room a seed inside the room (room name
text when it is printed inside, otherwise the centre of the reading-A rectangle of canon ceilings_info moved to A3.0 by the canon
offset A3.0 = A2.0 + (170.16, 129.12)) and every edge is SNAPPED to the nearest A3.0 vector face parallel to it (<= 3 pt, overlap
>= 30 % of the edge); the landlord room (no reading-A rectangle) is ray-cast from its label to the first face on each side.
The json records, per edge, the vector coordinate used and the offset hypothesis it confirmed. No quantity (rooms are excluded)."""
import json, os, re, sys
import pymupdf as fitz
from PIL import Image, ImageDraw
K = os.environ.get("K") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
c = json.load(open(os.path.join(K, "etapas/4_canon/takeoff_canon.json")))
sm = json.load(open(os.path.join(K, "etapas/SHEET_MAP.json")))
PAG = {v: int(k) for k, v in sm.items()}
RCP = c["constants"]["rcp_sheet"]["value"]
S = float(c["constants"]["plan_scale_pt_per_ft"]["value"])
m = re.search(r"A3\.0\s*=\s*A2\.0\s*\+\s*\(([\d.]+),\s*([\d.]+)\)", c["constants"]["plan_scale_pt_per_ft"]["source"])
DX, DY = float(m.group(1)), float(m.group(2))
doc = fitz.open(os.path.join(K, "plans/bidset_SIN_MARKUPS.pdf"))
p = doc[PAG[RCP] - 1]
R = p.rotation_matrix


def segs(walls_only=True):
    out = []
    for dr in p.get_drawings():
        f = dr.get("fill") is not None
        w = dr.get("width") or 0
        if walls_only and not (f or abs(w - 0.72) < 0.01):
            continue
        for it in dr["items"]:
            if it[0] == "l":
                out.append((it[1] * R, it[2] * R))
            elif it[0] == "re":
                r = fitz.Rect(it[1] * R); r.normalize()
                q = [fitz.Point(r.x0, r.y0), fitz.Point(r.x1, r.y0), fitz.Point(r.x1, r.y1), fitz.Point(r.x0, r.y1)]
                out += [(q[i], q[(i + 1) % 4]) for i in range(4)]
    return out


SW, SA = segs(True), segs(False)


def snap(val, lo, hi, vertical, tol=3.0, min_cov=0.2):
    """nearest vector face parallel to the edge (x = val for a vertical edge from y lo..hi): candidate coordinates within tol,
    each scored by the UNION of the segments lying on it (+-0.15 pt) inside lo..hi; coverage >= min_cov of the edge (door
    openings and mullion gaps break the face, e.g. Toilet 104 door in the hallway south wall)."""
    for pool, kind in ((SW, "wall poche / 0.72 pt wall line"), (SA, "thin line (storefront mullions)")):
        on = []
        for a, b in pool:
            if vertical and abs(a.x - b.x) < 0.3:
                on.append((a.x, min(a.y, b.y), max(a.y, b.y)))
            elif not vertical and abs(a.y - b.y) < 0.3:
                on.append((a.y, min(a.x, b.x), max(a.x, b.x)))
        best = None
        for c_ in sorted({round(t[0], 2) for t in on if abs(t[0] - val) <= tol}, key=lambda v: abs(v - val)):
            iv = sorted((max(lo, s0), min(hi, s1)) for cc, s0, s1 in on if abs(cc - c_) <= 0.15 and min(hi, s1) > max(lo, s0))
            tot, cur = 0.0, None
            for a_, b_ in iv:
                if cur is None or a_ > cur[1]:
                    tot += (cur[1] - cur[0]) if cur else 0.0
                    cur = [a_, b_]
                else:
                    cur[1] = max(cur[1], b_)
            tot += (cur[1] - cur[0]) if cur else 0.0
            if tot >= min_cov * (hi - lo):
                best = (c_, round(tot / (hi - lo), 2))
                break
        if best is not None:
            return best[0], f"{kind}, {best[1]:.0%} of the edge"
    return None, None


def ray(x, y):
    o = {}
    for dx, dy, k in ((1, 0, "E"), (-1, 0, "W"), (0, 1, "S"), (0, -1, "N")):
        best = None
        for a, b in SW:
            if dx and abs(a.x - b.x) < 0.3 and min(a.y, b.y) <= y <= max(a.y, b.y):
                t = (a.x - x) * dx
                if t > 0.5 and (best is None or t < best): best = t
            if dy and abs(a.y - b.y) < 0.3 and min(a.x, b.x) <= x <= max(a.x, b.x):
                t = (a.y - y) * dy
                if t > 0.5 and (best is None or t < best): best = t
        o[k] = round(x + dx * best if dx else y + dy * best, 2) if best else None
    return o


def label(term):
    q = [fitz.Rect(r * R) for r in p.search_for(term)]
    for r in q: r.normalize()
    return q


# reading-A rectangles (A2.0 vector) printed in canon ceilings_info, in its order: Retail, Storage, Hallway, Toilet 103, Toilet 104
ci = c["ceilings_info"]
rects = [tuple(float(v) for v in g) for g in re.findall(r"([\d.]+)-([\d.]+) x ([\d.]+)-([\d.]+)", ci)]
ROOMS = [  # room, number, printed reason (A3.0 tag / label), N/SHEET, index of the reading-A rectangle
    ("RETAIL", "100", "2x4 ACT new grid and tiles, acoustical ceilings by others", "A3.0", 0),
    ("STORAGE", "101", "2x4 ACT existing grid & new tiles, acoustical ceilings by others", "A3.0", 1),
    ("HALLWAY", "102", "existing gyp. bd. ceiling 9'-0\" to remain", "A3.0", 2),
    ("EXISTING TOILET", "103", "existing gyp. bd. ceiling 9'-0\" to remain", "A3.0", 3),
    ("EXISTING ACCESS. TOILET", "104", "existing gyp. bd. ceiling 9'-0\" to remain", "A3.0", 4),
    ("LANDLORD ROOM", "LANDLORD ROOM", "Landlord room N.I.C., not in contract", "A3.0 / A2.0", None),
]
assert len(rects) == 5, rects
rooms, fallas = [], []
for name, num, why, nh, ix in ROOMS:
    if ix is not None:
        x0, x1, y0, y1 = rects[ix]
        hyp = {"W": x0 + DX, "E": x1 + DX, "N": y0 + DY, "S": y1 + DY}
        src_h = f"reading-A rectangle (canon ceilings_info, A2.0 vector) {x0}-{x1} x {y0}-{y1} + offset ({DX}, {DY})"
    else:
        lb = label("LANDLORD")
        lb = min(lb, key=lambda r: r.x0)                # plan label (the other hits are in the title block)
        hyp = ray((lb.x0 + lb.x1) / 2, (lb.y0 + lb.y1) / 2 + 40)
        src_h = f"ray cast from the printed 'LANDLORD ROOM (N.I.C.)' label at ({lb.x0:.1f}, {lb.y0:.1f}) to the first wall face"
    ed = {}
    for k in "WENS":
        vert = k in "WE"
        lo, hi = (hyp["N"], hyp["S"]) if vert else (hyp["W"], hyp["E"])
        v, kind = snap(hyp[k], lo, hi, vert)
        if v is None:
            fallas.append(f"{name} {k}: no A3.0 vector face within 3 pt of {hyp[k]:.2f}")
            continue
        ed[k] = {"value": v, "face": kind, "hypothesis": round(hyp[k], 2), "delta_pt": round(v - hyp[k], 2)}
    if len(ed) < 4:
        continue
    W_, E_, N_, S_ = (ed[k]["value"] for k in "WENS")
    poly = [[W_, N_], [E_, N_], [E_, S_], [W_, S_]]
    area = (E_ - W_) * (S_ - N_) / S ** 2
    rooms.append({"sheet": RCP, "room": num, "name": name, "disposition": "exclusion", "reason": why, "nhoja": nh,
                  "polygon": poly, "polygon_frame": "visible frame of A3.0 (page.rect after rotation 270, pt)",
                  "polygon_source": f"A3.0 vector faces: W {W_} / E {E_} / N {N_} / S {S_} ({src_h}); "
                                    f"room {(E_ - W_) / S:.2f} x {(S_ - N_) / S:.2f} ft = {area:.1f} SF (not quantified)",
                  "edges": ed, "area_sf_info": round(area, 1)})
if fallas:
    sys.exit("rcp_polys: " + "; ".join(fallas))
json.dump({"sheet": RCP, "rule": "U-159 / U-160: every room printed on the RCP has a ceiling row or an EXCLUDED markup with the printed reason",
           "rooms": rooms}, open(os.path.join(K, "etapas/6_markups/rcp_cuartos.json"), "w"), indent=1, ensure_ascii=False)

# SOF-01: the gyp header strip of soffit_header_info (A3.0 band) as a soffit line; depth = developed width = board SF / LF
sh = c["soffit_header_info"]
b = sh["band"]
assert b["sheet"] == RCP
brd = next(x for x in c["misc_items"] if x["ref"] == "SOF-01 board")   # rev1c: '<id> board' -> esperados_rcp (BE-AUD07)
ax = (b["c0"] + b["c1"]) / 2
lf = (b["hi"] - b["lo"]) / S
polys = [{"misc": True, "id": "SOF-01", "sheet": RCP, "kind": "line", "lines": [[[b["lo"], ax], [b["hi"], ax]]],
          "lf": round(lf, 3), "depth_ft": round(float(brd["qty"]) / lf, 3), "layers": 1, "board": "5/8 GYPSUM BOARD TYPE X",
          "nhoja": "1/" + RCP, "cause": "SOF-01 gyp. bd. header 8'-6\" AFF at the north end of Hallway 102; board = " + brd["op"],
          "source": "canon soffit_header_info.band (" + sh["area_source"] + ")"}]
json.dump(polys, open(os.path.join(K, "etapas/6_markups/rcp_polys.json"), "w"), indent=1, ensure_ascii=False)

xs = [q[0] for r in rooms for q in r["polygon"]]
ys = [q[1] for r in rooms for q in r["polygon"]]
clip = fitz.Rect(min(xs) - 60, min(ys) - 60, max(xs) + 60, max(ys) + 60)
pix = p.get_pixmap(dpi=90, clip=clip)
im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
dr = ImageDraw.Draw(im)
s = pix.width / clip.width
col = [(255, 0, 0), (0, 120, 255), (0, 160, 0), (200, 0, 200), (255, 120, 0), (0, 160, 160)]
for i, r in enumerate(rooms):
    q = [((x - clip.x0) * s, (y - clip.y0) * s) for x, y in r["polygon"]]
    dr.polygon(q, outline=col[i], width=3 if i else 5)
    dr.text((q[0][0] + 6, q[0][1] + 6), f"{r['name']} {r['room']}", fill=col[i])
for e in polys:
    q = [((x - clip.x0) * s, (y - clip.y0) * s) for x, y in e["lines"][0]]
    dr.line(q, fill=(0, 0, 0), width=6)
f = os.path.join(K, "etapas/4_canon/img/rcp_check.png")
im.save(f)
assert Image.open(f).size[0] > 300
print(json.dumps({r["name"]: [r["polygon"][0], r["polygon"][2], {k: v["delta_pt"] for k, v in r["edges"].items()}] for r in rooms}))
