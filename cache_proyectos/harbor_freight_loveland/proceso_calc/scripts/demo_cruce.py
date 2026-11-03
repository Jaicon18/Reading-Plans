"""R-ALC-06 / BE-VS-08: demolition plan vs new floor plan, wall by wall (HFT Loveland). Each D1.0 demo element (canon
demo_geom, D1.0 registered to A1.1 by the resolution: both 3/32" = 1'-0" (6.75 pt/ft), dx +27.9 / dy -61.3 pt, grid A
bubble / lease line) is crossed with the new A1.1 walls within 10 pt; each new A1.1 wall is crossed back.
Writes etapas/DEMO_CRUCE.md (+ copy to FINAL/proceso). Text only, quantities from the canon."""
import json, math, os, shutil
K = os.environ.get("K") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
c = json.load(open(os.path.join(K, "etapas", "4_canon", "takeoff_canon.json")))
demo = json.load(open(os.path.join(K, "etapas", "6_markups", "demo_geom.json")))
OFF = {"D1.0": (27.9, -61.3)}
NEW = "A1.1"


def segs(pts):
    return list(zip(pts, pts[1:]))


def dseg(p, a, b):
    (x, y), (x1, y1), (x2, y2) = p, a, b
    dx, dy = x2 - x1, y2 - y1
    L = dx * dx + dy * dy
    t = 0 if L == 0 else max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / L))
    return math.hypot(x - x1 - t * dx, y - y1 - t * dy)


new = []
for w in c["walls"]:
    b = w["band"]
    if b.get("sheet") != NEW:
        continue
    m = (b["c0"] + b["c1"]) / 2
    pts = [(b["lo"], m), (b["hi"], m)] if b["ori"] == "H" else [(m, b["lo"]), (m, b["hi"])]
    new.append((w["id"], "new metal wall " + (w.get("tag") or ""), pts))
for e in c.get("existing_walls") or []:
    new.append((e["id"], "existing wall, new board only", [tuple(p) for p in e["path"]]))


def near(pts, sign):
    """New-plan walls that run ALONG the demolished element: >= 40 % of its sample points within 10 pt (a wall that
    only touches it at a corner or crosses it does not count)."""
    out = set()
    for wid, kind, q in new:
        k = sum(1 for p in pts if min(dseg(p, a, b) for a, b in segs(q)) <= 10.0)
        if k >= 0.4 * len(pts):
            out.add((wid, kind))
    return out


def sample(pts, n=6):
    out = []
    for a, b in segs(pts):
        for i in range(n + 1):
            out.append((a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n))
    return out


rows, hit = [], {}
for e in demo:
    if e["sheet"] not in OFF:
        rows.append((e["id"], e["sheet"], e["keynote"], e["sf"], "demolished", "-", "sheet not registered to the new plan"))
        continue
    dx, dy = OFF[e["sheet"]]
    best = None
    for s in (1, -1):
        pts = [(x + s * dx, y + s * dy) for x, y in sample([tuple(p) for p in e["polyline"]])]
        nb = near(pts, s)
        if best is None or len(nb) > len(best[1]):
            best = (s, nb)
    nb = sorted(best[1])
    for wid, _ in nb:
        hit.setdefault(wid, []).append(e["id"])
    rep = "; ".join(f"{w} ({k})" for w, k in nb) or "no new wall on that line (space opened / new layout)"
    rows.append((e["id"], e["sheet"], e["keynote"], e["sf"], "demolished", rep,
                 "layers per RFI-02; height = B.O. structure of the bay (A1.2)" if e.get("layers", 1) > 1 else "furring, 1 face (RFI-02)"))
L = ["# Demolition plan vs new floor plan - cross table (Harbor Freight Tools - Loveland, CO, rev1)", "",
     "D1.0 demolition elements registered to A1.1 (3/32\" = 1'-0\", dx +27.9 / dy -61.3 pt of the resolution). 'New on that line' = A1.1 walls running along the demolished element (>= 40 % of its length within 10 pt); 'no new wall' = the line is open in the new layout. Resolution table: 4_canon/demo_cruce.md.", "",
     "| Demo element | Sheet | Keynote | SF | Status | New on that line (A1.1) | Difference / note |", "|---|---|---|---|---|---|---|"]
for r in rows:
    L.append("| " + " | ".join(str(x) for x in r) + " |")
L += ["", "## New A1.1 elements vs demolition plan", "", "| A1.1 element | Kind | Demolished element on the same line | Status |", "|---|---|---|---|"]
for wid, kind, _ in new:
    d = hit.get(wid)
    st = "replaces demolished construction" if d else "new where nothing was demolished"
    L.append(f"| {wid} | {kind} | {', '.join(d) if d else '-'} | {st} |")
out = os.path.join(K, "etapas", "DEMO_CRUCE.md")
open(out, "w").write("\n".join(L) + "\n")
fd = os.path.join(K, "FINAL", "proceso")
os.makedirs(fd, exist_ok=True)
shutil.copy2(out, os.path.join(fd, "DEMO_CRUCE.md"))
print(len(rows), "demo rows,", len(new), "new elements")
