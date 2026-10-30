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


def _clase(w):
    """(element normalizado, type normalizado): un BOX o un tag de columna = column_wrap; el type solo cuenta en walls."""
    el = str(w.get("element") or "wall")
    b = (w.get("band") or {}).get("ori")
    tag = str(w.get("tag") or "").upper()
    if el == "wall" and (b == "BOX" or tag.startswith("C25") or tag in ("CW", "COLUMN")):
        el = "column_wrap"
    return el, (tag.replace("A", "A") if el == "wall" else "")


def _traslape(a, b):
    """Traslape relativo a lo largo del eje (H / V) con la misma línea c: fracción del más corto."""
    ba, bb = a.get("band") or {}, b.get("band") or {}
    if ba.get("ori") not in ("H", "V") or ba.get("ori") != bb.get("ori"):
        return 0.0, math.inf
    try:
        ca, cb = (ba["c0"] + ba["c1"]) / 2, (bb["c0"] + bb["c1"]) / 2
        lo, hi = max(ba["lo"], bb["lo"]), min(ba["hi"], bb["hi"])
        corto = min(ba["hi"] - ba["lo"], bb["hi"] - bb["lo"])
    except (KeyError, TypeError):
        return 0.0, math.inf
    return (max(0.0, hi - lo) / corto if corto > 0 else 0.0), abs(ca - cb)


def emparejar(leido, ref):
    """-> {id_leido: id_ref} uno a uno, codicioso: 1) por distancia de bands (misma hoja, clase, ori);
    2) si no, por traslape >= 80 % sobre la misma línea (otra partición de los tramos)."""
    cand = []
    for w in leido.get("walls") or []:
        for r in ref.get("walls") or []:
            if w.get("sheet") != r.get("sheet") or _clase(w) != _clase(r):
                continue
            tol = TOL_FT * _escala(ref, r.get("sheet"))
            if (w.get("band") or {}).get("ori") == (r.get("band") or {}).get("ori"):
                d = _dist(w, r)
                if d <= tol:
                    cand.append((d, w["id"], r["id"]))
                    continue
            t, dc = _traslape(w, r)
            if t >= 0.8 and dc <= tol:
                cand.append((tol + (1 - t) * tol + dc, w["id"], r["id"]))
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
    for lista, pa in (o.get("items_patch") or {}).items():
        out.setdefault(lista, set()).update(pa.keys())
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
        if lista in (o.get("items_patch") or {}):
            o["items_patch"][lista] = {k: v for k, v in o["items_patch"][lista].items() if k not in {str(x) for x in ks}}
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
            en_ref = {str(x) for x in en_ref}
            en_c = {str(x) for x in en_c}
            f = {i for i in ids if str(i) in en_ref and str(i) not in en_c}
            if f:
                faltan[lista] = f
                # nodes: derivados de la geometría de la lectura; sus ops sin objeto no son decisiones del estimador
                sin += [{"group": g.get("label"), "list": lista, "id": i, "derivado": lista == "nodes"} for i in sorted(f)]
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
