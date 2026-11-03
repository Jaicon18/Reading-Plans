"""Decision 16 (R-ALC-06 / BE-VS-08): demolition plan vs new floor plan, wall by wall. Each A-050 / A-052 demo element
(canon demo_geom, A-050 registered to A-202 by the resolution: 18 pt/ft, offset found by matching the A-202 wall
geometry) is crossed with the new A-202 walls / board-only entries within 10 pt; each new A-202 element is crossed
back. Writes etapas/DEMO_CRUCE.md (+ copy to FINAL_FOR_REVIEW/proceso). Text only, quantities from the canon."""
import json, math, os, shutil
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
c = json.load(open(os.path.join(K, "etapas", "4_canon", "takeoff_canon.json")))
demo = json.load(open(os.path.join(K, "etapas", "6_markups", "demo_geom.json")))
OFF = {"A-050": (-49.0, -98.0), "A-052": (-20.0, -105.0)}


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
    if b.get("sheet") != "A-202":
        continue
    m = (b["c0"] + b["c1"]) / 2
    pts = [(b["lo"], m), (b["hi"], m)] if b["ori"] == "H" else [(m, b["lo"]), (m, b["hi"])]
    new.append((w["id"], "new metal wall " + (w.get("tag") or ""), pts))
for e in c["existing_walls"]:
    kind = "existing wall to remain, new board only" if e["id"].startswith("EX-") else "new wood wall (board only)"
    new.append((e["id"], kind, [tuple(p) for p in e["path"]]))


def near(pts, sign):
    """A-202 elements that run ALONG the demolished element: >= 40 % of its sample points within 10 pt (a wall that
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
        rows.append((e["id"], e["sheet"], e["keynote"], e["sf"], "demolished (A-202 mark)", "-", "existing board removed under new cement board"))
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
    if e["group"] == "ceilings":
        rep = "new 5/8\" sag-resistant gyp ceiling on 6\" LGS joists (S-241 / A-221)" if e["id"] != "DEMO-C6" else "new ACT / multi-purpose room (A-221), no gyp ceiling"
        rows.append((e["id"], e["sheet"], e["keynote"], e["sf"], "demolished", rep, "Review Item 5" if e["id"] == "DEMO-C6" else ""))
        continue
    rep = "; ".join(f"{w} ({k})" for w, k in nb) or "no new wall on that line (space opened / new layout)"
    rows.append((e["id"], e["sheet"], e["keynote"], e["sf"], "demolished", rep,
                 {"DEMO-11": "height PENDING (RFI-11)", "DEMO-12": "drop PENDING (RFI-12)"}.get(e["id"], "height PENDING (RFI-10)") if "PENDING" in str(e.get("h_status")) else ""))
L = ["# Demolition plan vs new floor plan - cross table (CFA #2284 River Point, rev2)", "",
     "A-050 / A-052 demolition elements registered to A-202 (1/4\" = 1'-0\", offsets of the resolution). 'New on that line' = A-202 walls / board-only entries running along the demolished element (>= 40 % of its length within 10 pt); 'no new wall' = the line is open in the new layout.", "",
     "| Demo element | Sheet | Keynote | SF | Status | New on that line (A-202) | Difference / note |", "|---|---|---|---|---|---|---|"]
for r in rows:
    L.append("| " + " | ".join(str(x) for x in r) + " |")
L += ["", "## New A-202 elements vs demolition plan", "", "| A-202 element | Kind | Demolished element on the same line | Status |", "|---|---|---|---|"]
for wid, kind, _ in new:
    d = hit.get(wid)
    st = "replaces demolished construction" if d else ("stays (existing), new board only" if wid.startswith("EX-") else "new where nothing was demolished")
    L.append(f"| {wid} | {kind} | {', '.join(d) if d else '-'} | {st} |")
out = os.path.join(K, "etapas", "DEMO_CRUCE.md")
open(out, "w").write("\n".join(L) + "\n")
fd = os.path.join(os.path.dirname(K), "cfa_final", "FINAL_FOR_REVIEW", "proceso")
os.makedirs(fd, exist_ok=True)
shutil.copy2(out, os.path.join(fd, "DEMO_CRUCE.md"))
print(len(rows), "demo rows,", len(new), "new elements")
