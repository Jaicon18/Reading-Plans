"""Builds etapas/6_markups/demo_geom.json for markups_demo.py = the resolution's etapas/4_canon/demo_geom.json (one polyline per demolition element on A1.0, from the canon DEMO bands), checked one to one against the canon misc_items DEMO-* (same ids, same SF) and with
the states written in English. No geometry or quantity is created here.  Use: python3 bitacora.py run scripts/demo_geom_markups.py"""
import json, os, re, sys
K = os.environ.get("K") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
c = json.load(open(os.path.join(K, "etapas/4_canon/takeoff_canon.json")))
g = json.load(open(os.path.join(K, "etapas/4_canon/demo_geom.json")))
m = {x["ref"]: x for x in c["misc_items"] if x["ref"].startswith("DEMO")}
ids = {e["id"] for e in g}
falta = sorted(set(m) - ids) + sorted(ids - set(m))
mal = [e["id"] for e in g if e["id"] in m and abs(float(e["sf"]) - float(m[e["id"]]["qty"])) > 0.15]
if falta or mal:
    sys.exit(f"demo_geom vs canon: missing {falta}, SF differs {mal}")
EN = {"CONFIRMADO": "CONFIRMED", "DERIVADO": "DERIVED", "PENDIENTE": "PENDING"}
S = float(c["constants"]["plan_scale_pt_per_ft"]["value"])
for e in g:
    e["sf"] = m[e["id"]]["qty"]            # the canon SF (canon.py family total) is the markup SF
    # R2 M1: Bluebeam Wall Area = Length (vertices x /Measure) x Depth. The band gives the length to the pt (e.g. 43.44 pt =
    # 2.41333 ft -> 62.75 SF) while the canon rounds LF to 3 decimals (2.413 x 26 = 62.74). The far end of the polyline is moved
    # along its own axis (< 0.01 pt) so that its length = canon lf x scale: Bluebeam Length x Depth = canon SF exactly.
    (x0, y0), (x1, y1) = e["polyline"][0], e["polyline"][-1]
    L0 = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
    L1 = float(m[e["id"]]["lf"]) * S
    if L0 > 0 and abs(L1 - L0) < 0.5:
        e["polyline"][-1] = [round(x0 + (x1 - x0) * L1 / L0, 4), round(y0 + (y1 - y0) * L1 / L0, 4)]
    if abs(round(float(m[e["id"]]["lf"]) * float(m[e["id"]]["height_ft"]), 2) - float(e["sf"])) > 0.005:
        sys.exit(f"{e['id']}: canon lf x h != canon SF")
    for a, b in EN.items():
        e["h_status"] = str(e.get("h_status", "")).replace(a, b)
    e["h_status"] = re.sub(r",?\s*conservative higher value U-\d+ / R-ALC-\d+", ", conservative higher value (estimator standing rule)", e["h_status"])   # no internal rule codes in the markup text
os.makedirs(os.path.join(K, "etapas/6_markups"), exist_ok=True)
json.dump(g, open(os.path.join(K, "etapas/6_markups/demo_geom.json"), "w"), indent=1)
print(len(g), "demo elements,", round(sum(e["sf"] for e in g), 2), "SF; canon misc DEMO total", round(sum(x["qty"] for x in m.values()), 2))
