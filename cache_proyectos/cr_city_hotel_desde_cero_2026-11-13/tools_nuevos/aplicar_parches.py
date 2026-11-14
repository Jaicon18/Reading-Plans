#!/usr/bin/env python3
"""aplicar_parches.py — aplica los parches de los revisores (etapas/4_canon/parches/*.json) al canon unido, en orden de nombre.
Formato: {"autor": "...", "ops": [
  {"op": "set", "list": "existing_walls", "id": "W.6-L1-04", "fields": {...}, "reason": "... N/HOJA"},
  {"op": "add", "list": "misc_items", "entry": {...}, "reason": "..."},
  {"op": "del", "list": "existing_walls", "id": "...", "reason": "..."},
  {"op": "top", "key": "rcp_tags", "value": ...},            # reemplaza clave de nivel superior
  {"op": "merge_top", "key": "u199", "value": {...}} ]}      # dict.update / list.extend
Un id que no existe = error (rc 1): nunca se aplica en silencio. Lo aplicado queda en canon.parches_aplicados_info.
Uso: python3 -s aplicar_parches.py <takeoff_canon.json> <dir_parches>"""
import glob, json, os, sys

def main(cp, dp):
    c = json.load(open(cp, encoding="utf-8"))
    log, err = [], []
    for f in sorted(glob.glob(os.path.join(dp, "*.json"))):
        P = json.load(open(f, encoding="utf-8"))
        for o in P.get("ops", []):
            op, L = o.get("op"), o.get("list")
            if op in ("set", "del"):
                lst = c.get(L) or []
                hit = [e for e in lst if isinstance(e, dict) and e.get("id") == o["id"]]
                if not hit:
                    err.append(f"{os.path.basename(f)}: {op} {L} id '{o['id']}' no existe"); continue
                if op == "set":
                    for e in hit:
                        for k, v in o["fields"].items():
                            if v is None: e.pop(k, None)
                            else: e[k] = v
                else:
                    c[L] = [e for e in lst if not (isinstance(e, dict) and e.get("id") == o["id"])]
            elif op == "add":
                c.setdefault(L, []).append(o["entry"])
            elif op == "top":
                c[o["key"]] = o["value"]
            elif op == "merge_top":
                cur = c.get(o["key"])
                if isinstance(o["value"], dict):
                    cur = cur if isinstance(cur, dict) else {}; cur.update(o["value"])
                else:
                    cur = (cur if isinstance(cur, list) else []) + list(o["value"])
                c[o["key"]] = cur
            else:
                err.append(f"{os.path.basename(f)}: op desconocida {op}"); continue
            log.append({"file": os.path.basename(f), "autor": P.get("autor", ""), "op": op, "list": L or o.get("key"),
                        "id": o.get("id") or (o.get("entry") or {}).get("id", ""), "reason": o.get("reason", "")})
    c["parches_aplicados_info"] = log
    json.dump(c, open(cp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"parches: {len(log)} ops aplicadas, {len(err)} errores")
    for e in err: print("  ERROR", e)
    return 1 if err else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
