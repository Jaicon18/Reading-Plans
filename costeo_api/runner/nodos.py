#!/usr/bin/env python3
"""nodos.py — nodes L / T / free derivados por PROGRAMA de las bands del canon (R80e.53).

Cada extremo de cada wall va a UN solo node (canon.py exige exactamente 2 extremos por wall):
  - el extremo cae a <= tol_ft de un wall perpendicular de la misma hoja y ese wall también termina ahí -> L
    (consume un extremo de cada uno);
  - cae sobre el cuerpo del otro                                                                     -> T
    (branch = este; el through no consume extremo);
  - nada                                                                                             -> free.
Los walls sin band H / V (diagonales, BOX, piers, soffits…) reciben sus 2 extremos como free.
Se usa solo cuando la lectura no armó la topología (casi todo free)."""


def _escala(c, h):
    cs = c.get("constants") or {}
    return float(((cs.get("plan_scale_by_sheet") or {}).get(h) or {}).get("value")
                 or (cs.get("plan_scale_pt_per_ft") or {}).get("value") or 9.0)


def _seg(w):
    b = w.get("band") or {}
    if b.get("ori") not in ("H", "V") or w.get("element", "wall") != "wall":
        return None
    return b["ori"], (b["c0"] + b["c1"]) / 2, b["lo"], b["hi"], b.get("sheet") or w.get("sheet")


def derivar(c, tol_ft=1.0):
    walls = c.get("walls") or []
    sg = {w["id"]: _seg(w) for w in walls if _seg(w)}
    usados, nodos = set(), []

    def nuevo(**k):
        nodos.append(dict(id=f"NP{len(nodos) + 1}", **k))

    for wid, (o, cc, lo, hi, h) in sg.items():
        tol = tol_ft * _escala(c, h)
        for fin in ("lo", "hi"):
            if (wid, fin) in usados:
                continue
            a = lo if fin == "lo" else hi
            hit = None
            for xid, (o2, c2, lo2, hi2, h2) in sg.items():
                if xid == wid or o2 == o or h2 != h:
                    continue
                # punto del extremo: a lo largo de este wall = a; perpendicular = cc
                if abs(a - c2) <= tol and lo2 - tol <= cc <= hi2 + tol:
                    fin2 = "lo" if abs(cc - lo2) <= tol else "hi" if abs(cc - hi2) <= tol else None
                    hit = (xid, fin2)
                    break
            usados.add((wid, fin))
            if hit and hit[1] and (hit[0], hit[1]) not in usados:
                usados.add(hit)
                nuevo(kind="L", walls=[wid, hit[0]], source=f"{h} (vector: ends within {tol_ft} ft) [DERIVED nodos.py]")
            elif hit and not hit[1]:
                nuevo(kind="T", branch=wid, through=hit[0], source=f"{h} (vector: end on the body of {hit[0]}) [DERIVED nodos.py]")
            else:
                nuevo(kind="free", wall=wid, source=f"{h} (vector: free end) [DERIVED nodos.py]")
    for w in walls:
        if w["id"] not in sg:
            for _ in range(2):
                nuevo(kind="free", wall=w["id"], source=f"{w.get('sheet')} (no H / V band: ends taken as free) [DERIVED nodos.py]")
    return nodos


def podar(c):
    """R80e.60: después de las decisiones, un node que cita un wall que ya no está en el canon (excluido por decisión,
    p. ej. EXISTING) se ajusta sin romper "cada wall exactamente 2 extremos": L con un solo wall vivo -> free de ese wall;
    T sin through -> free de la rama; sin branch o free sin wall -> fuera. -> número de nodes ajustados."""
    ids = {w.get("id") for w in c.get("walls") or []}
    out, n = [], 0
    for x in c.get("nodes") or []:
        k = x.get("kind")
        if k == "L":
            vivos = [w for w in x.get("walls") or [] if w in ids]
            if len(vivos) == len(x.get("walls") or []):
                out.append(x); continue
            n += 1
            for w in vivos:
                out.append({"id": f"{x['id']}f", "kind": "free", "wall": w,
                            "source": f"{x.get('source', '')}; L partner excluded by decision -> free end (R80e.60)"})
        elif k == "T":
            if x.get("branch") in ids and x.get("through") in ids:
                out.append(x); continue
            n += 1
            if x.get("branch") in ids:
                out.append({"id": f"{x['id']}f", "kind": "free", "wall": x["branch"],
                            "source": f"{x.get('source', '')}; through wall excluded by decision -> free end (R80e.60)"})
        elif k == "free" and x.get("wall") is not None and x.get("wall") not in ids:
            n += 1
        else:
            out.append(x)
    c["nodes"] = out
    return n
