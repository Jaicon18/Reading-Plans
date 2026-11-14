#!/usr/bin/env python3
"""doble_cielo.py (U-190 REGLA DE ORO #3): Auditoria/DOBLE_CIELO.csv cuarto por cuarto desde el canon (ceilings + ceilings_misc + rcp_excluded):
Room, Level, Type single / double, Upper ceiling, Lower ceiling, Heights, N/SHEET, Framing, Row / reason."""
import csv, json, re, collections
W = "/root/cr0/work"; D = W + "/PRUEBA DESDE CERO 13-nov/Auditoria"
c = json.load(open(W + "/etapas/4_canon/takeoff_canon.json"))
g = collections.OrderedDict()
for x in c.get("ceilings", []) + c.get("ceilings_misc", []):
    m = re.match(r"(L\d)\s+(.+?)\s+-\s", str(x["room"]) + " - ")
    k = (m.group(1), m.group(2)) if m else (str(x.get("level")), str(x["room"]))
    g.setdefault(k, []).append(x)
rows = []
def fr(x):
    s = str(x.get("system"))
    return {"resilient_channel": "resilient channel (A0.08 / UL L546 item 6)", "usg_grid": "USG drywall suspension grid (GYP-1 legend, 09 22 16 2.2.F)"}.get(s, s)
for (lv, rm), xs in g.items():
    xs = sorted(xs, key=lambda x: -float(x.get("height_ft") or 0))
    up, lo = xs[0], (xs[1] if len(xs) > 1 else None)
    rows.append({"Room": rm, "Level": lv, "Type": "double" if lo else "single",
                 "Upper ceiling": f"{up.get('board')} {up.get('assembly', {}).get('id', '') if isinstance(up.get('assembly'), dict) else ''}".strip(),
                 "Lower ceiling": (lo.get("board") if lo else ""),
                 "Heights": " / ".join(f"{float(x.get('height_ft') or 0):.3f} ft" for x in xs),
                 "N/SHEET": str(up.get("source") or "")[:120],
                 "Framing": " | ".join(sorted({fr(x) for x in xs})),
                 "Row / reason": "; ".join(f"{'upper' if x is up else 'lower'}: {x['room']}" for x in xs)})
for x in c.get("rcp_excluded", []):
    rows.append({"Room": x.get("room"), "Level": str(x.get("room", ""))[:2], "Type": "single", "Upper ceiling": "EXCLUDED", "Lower ceiling": "",
                 "Heights": "", "N/SHEET": str(x.get("sheet") or ""), "Framing": "",
                 "Row / reason": f"upper: EXCLUDED - {x.get('reason') or x.get('motivo')}; lower: none"})
with open(D + "/DOBLE_CIELO.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print("DOBLE_CIELO", len(rows), "cuartos;", sum(1 for r in rows if r["Type"] == "double"), "dobles")
