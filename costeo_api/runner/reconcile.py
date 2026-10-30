#!/usr/bin/env python3
"""reconcile.py — reconciliación de ids SIN API, solo para APLICAR decisiones del estimador (R80e.35 / R80e.37).

Las cantidades siguen saliendo de la lectura + programas. Aquí solo se traduce: cada wall de la lectura se empareja por
GEOMETRÍA con el canon de referencia (el que usó el estimador al decidir): misma hoja + mismo type + misma orientación,
y distancia entre las bands dentro de la tolerancia (pt de la hoja = tol_ft x escala de la hoja). El wall emparejado toma
el Wall ID de la referencia (en todo el canon: nodes, strips, corners_ok, gaps_ok ...). Lo que no empareja queda con su
id de la lectura.

Al aplicar el overlay, una operación sobre un id que existía en la referencia en ese grupo pero que la lectura no trae
es una "decisión sin objeto": NO se aplica a ciegas y se lista para el estimador.
Una operación que CREA un elemento que la referencia no tenía (p. ej. un misc_item nuevo) sí se aplica."""
import copy
import json
import math
import sys

import overlay

TOL_FT = 2.0      # misma tolerancia de posición que usa comparar.py para emparejar (±2 ft)


def _escala(canon, hoja):
    c = canon.get("constants") or {}
    por = ((c.get("plan_scale_by_sheet") or {}).get(hoja) or {}).get("value")
    return float(por or (c.get("plan_scale_pt_per_ft") or {}).get("value") or 9.0)


def _pts(w):
    b = w.get("band") or {}
    if b.get("ori") in ("H", "V", "BOX"):
        return [b.get("c0"), b.get("c1"), b.get("lo"), b.get("hi")]
    if b.get("ori") == "D":
        return list(b.get("p0") or []) + list(b.get("p1") or [])
    return None


def _dist(a, b):
    pa, pb = _pts(a), _pts(b)
    if not pa or not pb or len(pa) != len(pb) or None in pa or None in pb:
        return math.inf
    return max(abs(x - y) for x, y in zip(pa, pb))


def emparejar(leido, ref):
    """-> {id_leido: id_ref} uno a uno, codicioso por distancia (misma hoja, type, ori, element)."""
    cand = []
    for w in leido.get("walls") or []:
        for r in ref.get("walls") or []:
            if (w.get("sheet"), w.get("tag"), w.get("element", "wall"), (w.get("band") or {}).get("ori")) != \
               (r.get("sheet"), r.get("tag"), r.get("element", "wall"), (r.get("band") or {}).get("ori")):
                continue
            d = _dist(w, r)
            if d <= TOL_FT * _escala(ref, r.get("sheet")):
                cand.append((d, w["id"], r["id"]))
    usados_l, usados_r, mapa = set(), set(), {}
    for d, il, ir in sorted(cand):
        if il in usados_l or ir in usados_r:
            continue
        mapa[il] = ir
        usados_l.add(il)
        usados_r.add(ir)
    return mapa


def renombrar(canon, mapa):
    """Cambia cada id de wall (string exacto) en todo el canon."""
    def f(o):
        if isinstance(o, dict):
            return {k: f(v) for k, v in o.items()}
        if isinstance(o, list):
            return [f(v) for v in o]
        if isinstance(o, str) and o in mapa:
            return mapa[o]
        return o
    return f(copy.deepcopy(canon))


def _ids_op(g):
    """{lista: set(ids)} que toca un grupo (upsert / remove / walls)."""
    o = g.get("canon") or {}
    out = {}
    for lista, items in (o.get("items_upsert") or {}).items():
        kk = (o.get("items_key") or {}).get(lista) or "ref"
        out.setdefault(lista, set()).update(x.get(kk) for x in items)
    for lista, ks in (o.get("items_remove") or {}).items():
        out.setdefault(lista, set()).update(ks)
    return out


def _filtrar(g, faltan):
    """Quita del grupo las operaciones sobre ids sin objeto en la lectura."""
    g = copy.deepcopy(g)
    o = g.get("canon") or {}
    for lista, ks in faltan.items():
        kk = (o.get("items_key") or {}).get(lista) or "ref"
        if lista in (o.get("items_upsert") or {}):
            o["items_upsert"][lista] = [x for x in o["items_upsert"][lista] if x.get(kk) not in ks]
        if lista in (o.get("items_remove") or {}):
            o["items_remove"][lista] = [x for x in o["items_remove"][lista] if x not in ks]
    return g


def aplicar(leido, ref_base, ov):
    """-> (canon con decisiones, mapa de ids, [decisiones sin objeto])."""
    mapa = emparejar(leido, ref_base)
    c = renombrar(leido, mapa)
    ref = copy.deepcopy(ref_base)
    sin = []
    for g in ov.get("groups") or []:
        faltan = {}
        for lista, ids in _ids_op(g).items():
            kk = ((g.get("canon") or {}).get("items_key") or {}).get(lista) or "ref"
            en_ref = {x.get(kk) for x in ref.get(lista) or []}
            en_c = {x.get(kk) for x in c.get(lista) or []}
            # existía en la referencia antes de este grupo y la lectura no lo trae = decisión sin objeto
            f = {i for i in ids if i in en_ref and i not in en_c}
            if f:
                faltan[lista] = f
                sin += [{"group": g.get("label"), "list": lista, "id": i} for i in sorted(f)]
        c = overlay._aplicar_uno(c, _filtrar(g, faltan))
        ref = overlay._aplicar_uno(ref, g)
    return c, mapa, sin


def main(argv):
    if len(argv) != 5:
        print("uso: reconcile.py <canon_leido> <canon_ref_sin_decisiones> <overlay.json> <canon_out>")
        return 2
    c, mapa, sin = aplicar(json.load(open(argv[1])), json.load(open(argv[2])), json.load(open(argv[3])))
    json.dump(c, open(argv[4], "w"), indent=1, ensure_ascii=False)
    print(json.dumps({"emparejados": len(mapa), "sin_objeto": sin}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
