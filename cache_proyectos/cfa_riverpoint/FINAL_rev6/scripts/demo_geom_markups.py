"""Builds 6_markups/demo_geom.json for markups_demo.py = canon demo_geom (18 elements) + DEMO-C6, whose geometry is
missing from the reconciled canon (misc_items DEMO-C6 38.35 SF has no demo_geom entry). DEMO-C6 polyline = the
existing gyp ceiling hatch extent drawn on A-052 (vector rect 2264.9,387.6 - 2341.3,534.2 pt, east room, KN10);
its SF stays the canon value (Review Item 5: A 38.35 / B 35.39 SF); LF = polyline perimeter / 18 pt/ft."""
import json, os, sys
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
c = json.load(open(os.path.join(K, "etapas/4_canon/takeoff_canon.json")))
g = list(c["demo_geom"])
m = {x["ref"]: x for x in c["misc_items"]}
ids = {e["id"] for e in g}
for ref in sorted(r for r in m if r.startswith("DEMO") and r not in ids):
    if ref == "DEMO-14":       # rev2: existing board under the new restroom cement board: the A-202 paths of those entries
        E = {e["id"]: e for e in c["existing_walls"]}
        # rev6 (U-120): an L / U restroom wall is split by axis in correcciones_rev6.py ('EX-RRM-01-CB-1'...): one demo piece per axis
        parts = [x for i in ("EX-RRM-01-CB", "EX-RRM-02-CB", "EX-RRW-01-CB", "EX-RRW-02-CB")
                 for x in ([E[i]] if i in E else [e for e in c["existing_walls"] if e.get("split_of") == i])]
        for e in parts:
            i = e["id"]
            g.append({"id": f"DEMO-14 {i}", "group": "walls (existing board under new cement board)", "page": 13, "polyline": e["path"],
                      "lf": e["length_ft"], "h_ft": e["height_ft"], "h_status": "DERIVED (board height of the new cement board)",
                      "layers": 1, "sf": round(e["length_ft"] * e["height_ft"], 2), "keynote": "A-050 KN10 (RFI-19)", "sheet": "A-202",
                      "height_source": "height of the new cement board that replaces it: " + str(e.get("height_source") or "")})   # rev5 BE-VS-08
        continue
    if ref != "DEMO-C6":
        sys.exit(f"{ref} without geometry and no vector extent recorded")
    x0, y0, x1, y1 = 2264.9, 387.6, 2341.3, 534.2
    poly = [[x0, y0], [x1, y0], [x1, y1], [x0, y1], [x0, y0]]
    per = sum(((poly[i+1][0]-poly[i][0])**2 + (poly[i+1][1]-poly[i][1])**2) ** 0.5 for i in range(4)) / 18.0
    g.append({"id": "DEMO-C6", "group": "ceilings", "page": 7, "polyline": poly, "lf": round(per, 2), "h_ft": 0.0,
              "h_status": "n/a ceiling (area)", "layers": 1, "sf": m[ref]["qty"],
              "keynote": "KN10 east room (outline = A-052 ceiling hatch; SF = canon, Review Item 5 A 38.35 / B 35.39)",
              "sheet": "A-052", "height_source": "ceiling area (no height): A-052 KN10 'remove existing gyp. bd. ceiling & support'"})
EN = {"CONFIRMADO": "CONFIRMED", "DERIVADO": "DERIVED", "PENDIENTE": "PENDING"}
for e in g:
    for a, b in EN.items():
        e["h_status"] = str(e.get("h_status", "")).replace(a, b)
json.dump(g, open(os.path.join(K, "etapas/6_markups/demo_geom.json"), "w"), indent=1)
print(len(g), round(sum(e["sf"] for e in g), 2), "SF; canon misc DEMO total", round(sum(x["qty"] for r, x in m.items() if r.startswith("DEMO")), 2))
