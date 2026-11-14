#!/usr/bin/env python3
"""rcp_cuartos.py (CR desde cero, U-159 / U-160): tabla de cuartos por hoja RCP -> renglón del canon (rows) o exclusión con motivo
impreso + N/HOJA + polígono (rcp_polys.json). Cuartos impresos detectados por compuerta_entrega.cuartos_rcp(set_texto)."""
import json, re, sys
sys.path.insert(0, "/root/cr0/skill_w/take-off-metal-frame-drywall/tools")
import compuerta_entrega as CE
W = "/root/cr0/work"
c = json.load(open(f"{W}/etapas/4_canon/takeoff_canon.json")); st = json.load(open(f"{W}/set_texto.json"))
polys = json.load(open(f"{W}/etapas/6_markups/rcp_polys.json"))
hc = CE.cuartos_rcp(st["hojas"])
rooms, falta = [], []
for h, nums in sorted(hc.items()):
    for n in sorted(nums):
        rx = re.compile(r"(?<![\d.])" + re.escape(n) + r"(?![\d])")
        rows = [x["room"] for x in c.get("ceilings", []) + c.get("ceilings_misc", []) if rx.search(str(x.get("room")))]
        if rows:
            rooms.append({"sheet": h, "room": n, "disposition": "row", "rows": rows}); continue
        ex = next((x for x in c.get("rcp_excluded", []) if rx.search(str(x.get("room")))), None)
        if ex:
            cand = [q for q in polys if q.get("kind") == "excluded" and q["room"] == ex["room"]]
            p = next((q for q in cand if q.get("sheet") == h), cand[0] if cand else None)   # el polígono de la hoja del cuarto
            reason = str(ex.get("reason") or ex.get("motivo") or "").strip()
            nh = re.search(r"\b\d{1,2}/[A-Z]\d\.\d{2}\b", reason + " " + str(ex.get("source") or ex.get("sheet") or ""))
            r = {"sheet": h, "room": n, "disposition": "exclusion", "reason": re.sub(r"\s*\(\d{1,2}/[A-Z]\d\.\d{2}\)\s*$", "", reason)[:180],
                 "nhoja": nh.group(0) if nh else f"1/{ex.get('sheet') or h}"}
            if p:
                pts = p["polygon"]; r["polygon"] = pts; r["draw_sheet"] = p["sheet"]
                r["label_xy"] = [sum(x for x, _ in pts) / len(pts), sum(y for _, y in pts) / len(pts)]
            rooms.append(r); continue
        falta.append(f"{h} {n}")
        rooms.append({"sheet": h, "room": n, "disposition": "missing"})
# F11 auditoría U-181: toda exclusión con polígono se dibuja aunque el detector de cuartos no la vea en su hoja
ya = {(r.get("draw_sheet"), json.dumps(r.get("polygon"))) for r in rooms if r.get("polygon")}
for q in polys:
    if q.get("kind") != "excluded" or (q["sheet"], json.dumps(q["polygon"])) in ya:
        continue
    ex = next((x for x in c.get("rcp_excluded", []) if x.get("room") == q["room"]), None)
    if not ex:
        continue
    pts = q["polygon"]; reason = str(ex.get("reason") or "").strip()
    cxy = [sum(x for x, _ in pts) / len(pts), sum(y for _, y in pts) / len(pts)]
    if any(r.get("draw_sheet") == q["sheet"] and r.get("label_xy") and abs(r["label_xy"][0] - cxy[0]) < 60 and abs(r["label_xy"][1] - cxy[1]) < 25
           for r in rooms):
        continue                                  # misma zona ya rotulada (U-187: ningún texto encima de otro)
    rooms.append({"sheet": q["sheet"], "room": q["room"], "disposition": "exclusion", "reason": reason[:180],
                  "nhoja": f"1/{q['sheet']}", "polygon": pts, "draw_sheet": q["sheet"],
                  "label_xy": [sum(x for x, _ in pts) / len(pts), sum(y for _, y in pts) / len(pts)]})
    ya.add((q["sheet"], json.dumps(pts)))
json.dump({"rooms": rooms}, open(f"{W}/etapas/6_markups/rcp_cuartos.json", "w"), indent=1)
print(len(rooms), "cuartos; sin destino:", falta)
