"""Builds etapas/6_markups/demo_geom.json for markups_demo.py = the resolution's etapas/4_canon/demo_geom.json (one polyline per demolition element on D100), checked one to one against the canon misc_items DEMO-* (same ids, same SF) and with
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
for e in g:
    e["sf"] = m[e["id"]]["qty"]            # the canon SF (canon.py family total) is the markup SF
    for a, b in EN.items():
        e["h_status"] = str(e.get("h_status", "")).replace(a, b)
    e["h_status"] = re.sub(r"standing order R-ALC-\d+", "estimator standing order", e["h_status"])   # rev2 F2: no rule codes
os.makedirs(os.path.join(K, "etapas/6_markups"), exist_ok=True)
json.dump(g, open(os.path.join(K, "etapas/6_markups/demo_geom.json"), "w"), indent=1)
print(len(g), "demo elements,", round(sum(e["sf"] for e in g), 2), "SF; canon misc DEMO total", round(sum(x["qty"] for x in m.values()), 2))
