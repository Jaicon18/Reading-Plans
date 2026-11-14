#!/usr/bin/env python3
"""F04 auditoría U-181: constants.board_sf_concealed = capas ocultas (Level 1 / fire-tape, spec 09 29 00 3.6.E.1):
 (a) capas interiores de caras multicapa de existing_walls: LF x H x faces x (layers - 1);
 (b) membrana de cielo (resilient_channel) oculta sobre un cielo colgado (usg_grid) del mismo cuarto: min(área sup, área inf).
Solo board del 'board driver' (regular / X / X WR / C); cement board y sheathing fuera. Uso: capas_ocultas.py <canon.json>"""
import json, sys, collections
p = sys.argv[1]; c = json.load(open(p, encoding="utf-8"))
SKIP = ("cement", "sheath", "exterior", "shaftliner", "liner")
wa = 0.0; nw = 0
for w in c.get("existing_walls") or []:
    b = str(w.get("board") or "").lower()
    ly = int(w.get("layers") or 1)
    if ly < 2 or any(s in b for s in SKIP):
        continue
    wa += float(w["length_ft"]) * float(w["height_ft"]) * int(w.get("faces") or 1) * (ly - 1); nw += 1
cuartos = collections.defaultdict(lambda: {"up": [], "low": []})
for x in c.get("ceilings") or []:
    if any(s in str(x.get("board") or "").lower() for s in SKIP):
        continue
    nm = str(x.get("room") or "")
    if x.get("system") == "resilient_channel" and " above " in f" {nm.lower()} ".replace("(", " ").replace(")", " "):
        cuartos["__oculta__ " + nm]["up"].append(float(x.get("area_sf") or 0)); cuartos["__oculta__ " + nm]["low"].append(1e9)
        continue                             # membrana FS-1 sobre ACT / GYP-1 (el nombre lo dice): toda oculta
    k = nm.split(" - ")[0].strip()
    cuartos[k]["up" if x.get("system") == "resilient_channel" else "low"].append(float(x.get("area_sf") or 0))
ca, det = 0.0, []
for k, v in sorted(cuartos.items()):
    if v["up"] and v["low"]:
        a = min(sum(v["up"]), sum(v["low"])); ca += a; det.append(f"{k} {a:.1f}")
tot = round(wa + ca, 2)
c.setdefault("constants", {})["board_sf_concealed"] = {"value": tot, "status": "DERIVED",
    "source": "spec 09 29 00 3.6.E.1 (Level 1: concealed areas) - audit U-181 F04",
    "operation": f"(a) {nw} multi-layer board-only walls: LF x H x faces x (layers - 1) = {wa:.2f} SF; (b) rated membrane concealed above a dropped ceiling: rows named 'above ACT / GYP-1' in full, else min(upper, lower) area of the same room = {ca:.2f} SF ({len(det)} rooms: {'; '.join(det[:12])}{' ...' if len(det) > 12 else ''}); total {tot} SF [DERIVED]",
    "walls_sf": round(wa, 2), "ceilings_sf": round(ca, 2)}
json.dump(c, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("board_sf_concealed", tot, "walls", round(wa, 2), "ceilings", round(ca, 2), len(det))
