"""etapas/registro_renglones.json = input of `registro.py crear` (REGLA 50.1), Xfinity - Interquest: the 24 fixed ALC rows of
`alcances.py renglones` + one row per element of the resolved canon (walls W2 / CF, the SOF-01 header, door 101, the demolished
walls DEMO-01..09, the braces, blocking and trims) + one row per room printed on the RCP A3.0 (rcp_cuartos.json). All start
'pendiente'; scripts/registro_marcar.py closes them with registro.py marcar. Text only."""
import json, os
K = os.environ.get("K") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
c = json.load(open(os.path.join(K, "etapas/4_canon/takeoff_canon.json")))
rows = json.load(open(os.path.join(K, "etapas/alcances_renglones.json")))
for w in c["walls"]:
    rows.append({"id": w["id"], "tipo": "wall", "ubicacion": f"{w['sheet']} - {w.get('location', '')}"[:200],
                 "fuente": f"tag {w.get('tag')} ({', '.join(w.get('tag_ids') or []) or 'no tag id'}); {w.get('detail_info') or w.get('detail')}"[:300]})
for o in c["opening_schedule"]["items"]:
    rows.append({"id": o["ref"], "tipo": "abertura", "ubicacion": f"A2.0 - wall {o['wall']}", "fuente": o["source"][:300]})
sh = c["soffit_header_info"]
rows.append({"id": sh["ref"], "tipo": "soffit", "ubicacion": f"{sh['sheet']} - {sh['room']}", "fuente": sh["height_source"]})
for m in c["misc_items"]:
    if m["ref"].startswith(("DEMO", "BRACE")):
        rows.append({"id": m["ref"], "tipo": "otro", "ubicacion": f"{m.get('sheet') or m['source']} - {m.get('label', '')}"[:200],
                     "fuente": str(m["source"])[:300]})
for b in c["blocking_items"]:
    rows.append({"id": b["ref"], "tipo": "otro", "ubicacion": f"blocking on {b['wall']}"[:200], "fuente": b["source"][:300]})
for t in c["trim_items"]:
    rows.append({"id": t["ref"], "tipo": "otro", "ubicacion": t["label"][:200], "fuente": t["source"][:300]})
for r in json.load(open(os.path.join(K, "etapas/6_markups/rcp_cuartos.json")))["rooms"]:
    rows.append({"id": f"RCP-{r['sheet']}-{r['room'].replace(' ', '_')}", "tipo": "cielo", "ubicacion": f"{r['sheet']} - {r.get('name') or r['room']}",
                 "fuente": f"A3.0 room label / ceiling tag; printed reason: {r['reason']} ({r['nhoja']})"})
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "duplicated ledger id"
json.dump(rows, open(os.path.join(K, "etapas/registro_renglones.json"), "w"), indent=1, ensure_ascii=False)
print(len(rows), "ledger rows")
