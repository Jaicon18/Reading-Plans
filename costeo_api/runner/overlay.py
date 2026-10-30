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


def _clave(lista):
    """Clave de identidad de los ítems de una lista del canon: ref, o id (walls, nodes); None = lista sin identidad."""
    if lista and all(isinstance(x, dict) and x.get("ref") for x in lista):
        return "ref"
    if lista and all(isinstance(x, dict) and x.get("id") for x in lista):
        return "id"
    return None


def aplicar_canon(canon, ov):
    """Aplica el overlay; si trae "groups", cada grupo (una decisión o un paquete de decisiones) en orden."""
    c = copy.deepcopy(canon)
    for g in ov.get("groups") or []:
        c = _aplicar_uno(c, g)
    if ov.get("canon"):
        c = _aplicar_uno(c, ov)
    return c


def _aplicar_uno(c, ov):
    o = ov.get("canon") or {}
    for k in o.get("top_remove") or []:
        c.pop(k, None)
    for k in o.get("constants_remove") or []:
        (c.get("constants") or {}).pop(k, None)
    # listas con identidad (ref / id): alta / reemplazo / baja / orden
    for lista, items in (o.get("items_upsert") or {}).items():
        cur = c.setdefault(lista, [])
        kk = (o.get("items_key") or {}).get(lista) or _clave(items) or "ref"
        pos = {x.get(kk): i for i, x in enumerate(cur)}
        for it in items:
            if lista in LISTAS:
                _check(it, lista)
            if it[kk] in pos:
                cur[pos[it[kk]]] = it
            else:
                cur.append(it)
                pos[it[kk]] = len(cur) - 1
    for lista, keys in (o.get("items_remove") or {}).items():
        kk = (o.get("items_key") or {}).get(lista) or _clave(c.get(lista) or []) or "ref"
        c[lista] = [x for x in c.get(lista) or [] if x.get(kk) not in set(keys)]
    for lista, pa in (o.get("items_patch") or {}).items():
        kk = (o.get("items_key") or {}).get(lista) or _clave(c.get(lista) or []) or "ref"
        cur = c.get(lista) or []
        for i, x in enumerate(cur):
            if str(x.get(kk)) in pa:
                cur[i] = aplicar_parche(x, pa[str(x.get(kk))])
    for lista, orden in (o.get("items_order") or {}).items():
        kk = (o.get("items_key") or {}).get(lista) or _clave(c.get(lista) or []) or "ref"
        idx = {k: i for i, k in enumerate(orden)}
        c[lista] = sorted(c.get(lista) or [], key=lambda x: idx.get(x.get(kk), len(idx)))
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


IDK = ("side", "ref", "id")


def _idk(lista):
    for k in IDK:
        if lista and all(isinstance(x, dict) and x.get(k) is not None for x in lista) and \
                len({x[k] for x in lista}) == len(lista):
            return k
    return None


def parche(a, b):
    """Parche mínimo a → b: dicts por clave; listas de dicts con identidad (side / ref / id) por ítem; resto = set."""
    if isinstance(a, dict) and isinstance(b, dict):
        p = {"__dict__": {k: parche(a.get(k), b[k]) for k in b if a.get(k) != b[k]}}
        rm = [k for k in a if k not in b]
        if rm:
            p["__del__"] = rm
        return p
    if isinstance(a, list) and isinstance(b, list) and _idk(b) and _idk(a) == _idk(b):
        k = _idk(b)
        ia, ib = {x[k]: x for x in a}, {x[k]: x for x in b}
        return {"__by__": k, "items": {str(i): parche(ia.get(i), ib[i]) if i in ia else {"__set__": ib[i]}
                                       for i in ib if ia.get(i) != ib[i]},
                "del": [i for i in ia if i not in ib], "order": [x[k] for x in b]}
    return {"__set__": b}


def aplicar_parche(a, p):
    if "__set__" in p:
        return copy.deepcopy(p["__set__"])
    if "__dict__" in p:
        out = copy.deepcopy(a) if isinstance(a, dict) else {}
        for k, sp in p["__dict__"].items():
            out[k] = aplicar_parche(out.get(k), sp)
        for k in p.get("__del__") or []:
            out.pop(k, None)
        return out
    if "__by__" in p:
        k = p["__by__"]
        cur = [copy.deepcopy(x) for x in (a or []) if x.get(k) not in set(p.get("del") or [])]
        pos = {str(x.get(k)): i for i, x in enumerate(cur)}
        for i, sp in p["items"].items():
            if i in pos:
                cur[pos[i]] = aplicar_parche(cur[pos[i]], sp)
            else:
                cur.append(aplicar_parche(None, sp))
        idx = {x: n for n, x in enumerate(p.get("order") or [])}
        return sorted(cur, key=lambda x: idx.get(x.get(k), len(idx)))
    return a


def diff(a, b):
    """Overlay mínimo que lleva el canon a → b (genérico: listas por ref / id, constants y claves de primer nivel)."""
    o = {"constants": {}, "top": {}, "top_remove": [], "constants_remove": [], "items_upsert": {}, "items_remove": {},
         "items_order": {}}
    for k in sorted(set(a) | set(b)):
        if a.get(k) == b.get(k):
            continue
        if k not in b:
            o["top_remove"].append(k)
            continue
        if k == "constants":
            ca, cb = a.get(k) or {}, b[k]
            o["constants"] = {x: cb[x] for x in cb if ca.get(x) != cb[x]}
            o["constants_remove"] = [x for x in ca if x not in cb]
            continue
        kk = _clave(b[k]) if isinstance(b[k], list) else None
        unico = kk and len({x[kk] for x in b[k]}) == len(b[k]) and \
            len({x.get(kk) for x in a.get(k) or []}) == len(a.get(k) or [])
        if unico and isinstance(a.get(k), list) and (not a[k] or _clave(a[k]) == kk):
            ia = {x[kk]: x for x in a.get(k) or []}
            ib = {x[kk]: x for x in b[k]}
            up = [ib[x] for x in ib if x not in ia]                       # alta: el ítem lo crea la decisión
            pa = {str(x): parche(ia[x], ib[x]) for x in ib if x in ia and ia[x] != ib[x]}   # cambio: solo campos
            if pa:
                o.setdefault("items_patch", {})[k] = pa
            rm = [x for x in ia if x not in ib]
            if up:
                o["items_upsert"][k] = up
            if rm:
                o["items_remove"][k] = rm
            o["items_order"][k] = [x[kk] for x in b[k]]
            o.setdefault("items_key", {})[k] = kk
        else:
            o["top"][k] = b[k]
    return {kk: v for kk, v in o.items() if v}


def aplicar_takeoff(tk, ov):
    t = copy.deepcopy(tk)
    for g in ov.get("groups") or []:
        t = _takeoff_uno(t, g)
    return _takeoff_uno(t, ov)


def _takeoff_uno(t, ov):
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
