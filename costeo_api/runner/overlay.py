#!/usr/bin/env python3
"""overlay.py — fusiona un overlay de DECISIONES DEL ESTIMADOR al canon y a takeoff.json (R80e.35 / R80e.37).

GENÉRICO: ningún proyecto vive aquí. El overlay es un JSON por proyecto:
{
  "project": "...", "decision_date": "YYYY-MM-DD",
  "canon": {
    "constants": {clave: {"value": v, "source": "N/HOJA ..."}},          # set
    "top":       {clave: valor},                                         # set de claves de primer nivel
    "upsert":    {"misc_items" | "plywood_strips" | "blocking_items" | "trim_items": [ {ref, ...}, ... ]},
    "remove":    {"misc_items" | "plywood_strips" | "blocking_items" | "trim_items": [ref, ...]},
    "walls":     [{"id": W, "faces": [...lista completa...], "set": {campo: valor}}]
  },
  "takeoff": {"rfi_cierre": {...}, "inputs_notas": {...}, "alcances": {ALC-id: {"estado": e, "nota": n}}}
}
Idempotente: aplicar dos veces = aplicar una vez (upsert por ref reemplaza en su lugar; remove por ref; set).
Cada ítem que agrega cantidades debe traer source (N/HOJA u hoja) y op (operación DERIVADA)."""
import copy
import json
import re
import sys

HOJA = re.compile(r"\b[A-Z]{1,2}-?\d{3}")
LISTAS = ("misc_items", "plywood_strips", "blocking_items", "trim_items")


def _check(it, lista):
    if not it.get("ref"):
        raise ValueError(f"overlay {lista}: ítem sin ref")
    if lista != "trim_items" and not HOJA.search(str(it.get("source") or "")):
        raise ValueError(f"overlay {lista} {it['ref']}: source sin hoja")


def aplicar_canon(canon, ov):
    c = copy.deepcopy(canon)
    o = ov.get("canon") or {}
    for k, v in (o.get("constants") or {}).items():
        if not HOJA.search(str((v or {}).get("source") or "")) and "decision" not in str((v or {}).get("source") or ""):
            raise ValueError(f"overlay constants.{k}: source sin hoja / decisión")
        c.setdefault("constants", {})[k] = v
    for k, v in (o.get("top") or {}).items():
        c[k] = v
    for lista, refs in (o.get("remove") or {}).items():
        c[lista] = [x for x in c.get(lista) or [] if x.get("ref") not in set(refs)]
    for lista, items in (o.get("upsert") or {}).items():
        if lista not in LISTAS:
            raise ValueError(f"overlay upsert: lista desconocida {lista}")
        cur = c.setdefault(lista, [])
        pos = {x.get("ref"): i for i, x in enumerate(cur)}
        for it in items:
            _check(it, lista)
            if it["ref"] in pos:
                cur[pos[it["ref"]]] = it
            else:
                cur.append(it)
                pos[it["ref"]] = len(cur) - 1
    byid = {w["id"]: w for w in c.get("walls") or []}
    for wo in o.get("walls") or []:
        w = byid.get(wo["id"])
        if w is None:
            raise ValueError(f"overlay walls: {wo['id']} no está en el canon (la lectura no lo trae)")
        if "faces" in wo:
            w["faces"] = wo["faces"]
        for k, v in (wo.get("set") or {}).items():
            w[k] = v
    return c


def aplicar_takeoff(tk, ov):
    t = copy.deepcopy(tk)
    o = ov.get("takeoff") or {}
    if o.get("rfi_cierre"):
        t["rfi_cierre"] = dict(t.get("rfi_cierre") or {}, **o["rfi_cierre"])
    if o.get("inputs_notas"):
        t["inputs_notas"] = dict(t.get("inputs_notas") or {}, **o["inputs_notas"])
    al = {a["id"]: a for a in t.get("alcances") or []}
    for k, v in (o.get("alcances") or {}).items():
        if k in al:
            al[k].update(v)
        else:
            t.setdefault("alcances", []).append(dict(v, id=k))
    return t


def main(argv):
    if len(argv) != 6:
        print("uso: overlay.py <overlay.json> <canon_in> <canon_out> <takeoff_in> <takeoff_out>")
        return 2
    ov = json.load(open(argv[1]))
    c = aplicar_canon(json.load(open(argv[2])), ov)
    t = aplicar_takeoff(json.load(open(argv[4])), ov)
    json.dump(c, open(argv[3], "w"), indent=1, ensure_ascii=False)
    json.dump(t, open(argv[5], "w"), indent=1, ensure_ascii=False)
    print("overlay OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
