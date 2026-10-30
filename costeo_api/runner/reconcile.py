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
import re
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


def emparejar_ceilings(leido, ref):
    """-> {room_leido: room_ref}: mismo nombre, o mismo número de cuarto (3 dígitos) + mismo system con candidato
    único. Así los walls de la lectura que citan su ceiling (soffit_of) siguen apuntando a él cuando la decisión
    del estimador fija la lista de ceilings con los nombres de la referencia."""
    num = lambda z: set(re.findall(r"\b\d{3}\b", str(z.get("room") or "")))
    rr = ref.get("ceilings") or []
    mapa = {}
    for z in leido.get("ceilings") or []:
        if any(z.get("room") == r.get("room") for r in rr):
            continue
        c = [r for r in rr if num(z) and num(z) == num(r) and z.get("system") == r.get("system")]
        if len(c) == 1 and c[0]["room"] not in mapa.values():
            mapa[z["room"]] = c[0]["room"]
    return mapa


def renombrar_aberturas(leido, ref):
    """Refs de openings de la lectura (p. ej. "D14") -> ref de la referencia ("Door 14") cuando, en el mismo wall
    (ya reconciliado) o en el que lo contiene, los dígitos coinciden y el candidato es único.
    Solo toca walls[].openings[].ref."""
    dig = lambda x: "".join(re.findall(r"\d+", str(x)))
    rws = ref.get("walls") or []
    c = copy.deepcopy(leido)
    mapa = {}
    todas = {str(o.get("ref")) for r in rws for o in r.get("openings") or []}
    usadas = {str(o.get("ref")) for w in c.get("walls") or [] for o in w.get("openings") or []} & todas
    for w in c.get("walls") or []:
        # el mismo wall reconciliado o, si la lectura partió el tramo distinto, los walls de la referencia que lo
        # contienen (misma hoja, traslape >= 80 % sobre la misma línea)
        tol = TOL_FT * _escala(ref, w.get("sheet"))
        cerca = [r for r in rws if r["id"] == w["id"] or (r.get("sheet") == w.get("sheet") and
                 (lambda t: t[0] >= 0.8 and t[1] <= tol)(_traslape(w, r)))]
        refs = [str(o.get("ref")) for r in cerca for o in r.get("openings") or []]
        for o in w.get("openings") or []:
            r = str(o.get("ref"))
            cand = [x for x in refs if x != r and dig(x) and dig(x) == dig(r)]
            if not cand and r not in todas:     # respaldo: el número de door es único en el door schedule del set
                cand = [x for x in todas if dig(x) and dig(x) == dig(r) and x not in usadas]
            if len(cand) == 1 and r not in refs:
                o["ref"] = mapa[r] = cand[0]
                usadas.add(cand[0])
    return c, mapa


def reescalar_tramos(c, ids):
    """Tramos de faces (length_ft por side) que una decisión fijó con el largo de la REFERENCIA: se reescalan al largo
    del wall de la LECTURA, proporcionales (la cantidad sigue saliendo de la lectura; la decisión fija el reparto).
    [DERIVED] tramo_i x L_lectura / Σ tramos (el último absorbe el redondeo). -> [(wall, side, Σ, L)]"""
    out = []
    for w in c.get("walls") or []:
        if w["id"] not in ids or w.get("length_ft") is None:
            continue
        L = float(w["length_ft"])
        for lado in ("A", "B"):
            fs = [f for f in w.get("faces") or [] if f.get("side") == lado and f.get("length_ft") is not None]
            tot = sum(float(f["length_ft"]) for f in fs)
            if not fs or tot <= 0 or abs(tot - L) <= 0.05:
                continue
            acc = 0.0
            for i, f in enumerate(fs):
                nv = round(L - acc, 3) if i == len(fs) - 1 else round(float(f["length_ft"]) * L / tot, 3)
                f["length_source"] = (f"{f.get('length_source') or ''} | [DERIVED] decision split rescaled to the reading "
                                      f"length: {f['length_ft']} x {L} / {round(tot, 3)} = {nv}").strip(" |")
                f["length_ft"] = nv
                acc += nv
            out.append((w["id"], lado, round(tot, 3), L))
    return out


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
    c = renombrar(leido, dict(mapa, **emparejar_ceilings(leido, ref_base)))
    c, _ = renombrar_aberturas(c, ref_base)
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
            if lista == "nodes":                # un node se identifica por SUS walls, no por el id (ids de lectura y de
                wn = lambda n: frozenset(str(x) for k in ("wall", "walls", "branch", "through")   # referencia chocan)
                                         for x in ([n.get(k)] if isinstance(n.get(k), str) else (n.get(k) or [])))
                nr = {str(x.get("id")): wn(x) for x in ref.get("nodes") or []}
                nc = {str(x.get("id")): wn(x) for x in c.get("nodes") or []}
                f |= {i for i in ids if str(i) in nr and str(i) in nc and nr[str(i)] != nc[str(i)]}
            if f:
                faltan[lista] = f
                # nodes: derivados de la geometría de la lectura; sus ops sin objeto no son decisiones del estimador
                sin += [{"group": g.get("label"), "list": lista, "id": i, "derivado": lista == "nodes"} for i in sorted(f)]
        # ítems NUEVOS de la decisión que cuelgan de un wall que la lectura no trae (p. ej. un node en SS-IN-E)
        wc = {w["id"] for w in c.get("walls") or []} | \
            {x.get("id") for x in ((g.get("canon") or {}).get("items_upsert") or {}).get("walls") or []}
        wr = {w["id"] for w in ref.get("walls") or []}
        for lista, items in ((g.get("canon") or {}).get("items_upsert") or {}).items():
            kk = ((g.get("canon") or {}).get("items_key") or {}).get(lista) or "ref"
            for it in items:
                cuelga = [it.get("wall")] if isinstance(it.get("wall"), str) else list(it.get("walls") or [])
                if any(isinstance(x, str) and x in wr and x not in wc for x in cuelga) and \
                        it.get(kk) not in faltan.get(lista, set()):
                    faltan.setdefault(lista, set()).add(it.get(kk))
                    sin.append({"group": g.get("label"), "list": lista, "id": it.get(kk), "derivado": lista == "nodes",
                                "motivo": "cuelga de un wall que la lectura no trae"})
        c = overlay._aplicar_uno(c, _filtrar(g, faltan))
        tocados = set((((g.get("canon") or {}).get("items_patch") or {}).get("walls") or {}).keys())
        for wid, lado, tot, L in reescalar_tramos(c, tocados):
            sin.append({"group": g.get("label"), "list": "walls", "id": wid, "derivado": True,
                        "motivo": f"side {lado}: tramos de la decisión Σ {tot} reescalados al largo de la lectura {L}"})
        ref = overlay._aplicar_uno(ref, g)
    # decisiones GENERALES (por atributo) en todos los walls, emparejados o no (R80e.43)
    for k, v in overlay.aplicar_generales(c, ov).items():
        sin.append({"group": "generales", "list": "faces", "id": k, "derivado": True,
                    "motivo": f"decisión general aplicada por atributo a {v} face(s)"})
    # dependencias de una decisión de lista completa (p. ej. ceilings): una constante de la REFERENCIA que la lectura no
    # trae y cuya fuente es un supuesto del estimador con RFI (p. ej. carrying_direction "assumed E-W, RFI-15") viaja
    # con la decisión; se lista
    if any((g.get("canon") or {}).get("top") for g in ov.get("groups") or []):
        cr, cc = (ref_base.get("constants") or {}), c.setdefault("constants", {})
        for k, v in cr.items():
            if k not in cc and isinstance(v, dict) and re.search(r"\bRFI-?\d+", str(v.get("source") or "")):
                cc[k] = copy.deepcopy(v)
                sin.append({"group": "constants", "list": "constants", "id": k, "derivado": True,
                            "motivo": f"supuesto del estimador con RFI que acompaña a una decisión: {str(v.get('source'))[:80]}"})
    # opening_schedule fijado por una decisión: una abertura que la lectura no trae en ningún wall = decisión sin objeto
    sch = c.get("opening_schedule")
    if isinstance(sch, dict) and sch.get("items"):
        dadas = {str(o.get("ref")) for w in c.get("walls") or [] for o in w.get("openings") or []} | \
            {str(i.get("ref")) for i in sch.get("none") or []}
        quedan = [i for i in sch["items"] if str(i.get("ref")) in dadas]
        for i in sch["items"]:
            if i not in quedan:
                sin.append({"group": "opening_schedule", "list": "opening_schedule", "id": i.get("ref"), "derivado": False,
                            "motivo": "la lectura no trae esta abertura en ningún wall"})
        sch["items"] = quedan
        # al revés: una abertura de la lectura que la lista de la decisión no trae conserva su ítem de la lectura
        # (la decisión fijó la lista con los nombres de la referencia; no puede borrar una abertura leída)
        tiene = {str(i.get("ref")) for i in sch["items"]} | {str(i.get("ref")) for i in sch.get("none") or []}
        prop = {str(i.get("ref")): i for i in ((leido.get("opening_schedule") or {}).get("items") or [])}
        for w in c.get("walls") or []:
            for o in w.get("openings") or []:
                r = str(o.get("ref"))
                if r not in tiene:
                    it = dict(prop.get(r) or {"ref": r, "wall": w["id"], "source": o.get("source") or w.get("source")})
                    sch["items"].append(it)
                    tiene.add(r)
                    sin.append({"group": "opening_schedule", "list": "opening_schedule", "id": r, "derivado": True,
                                "motivo": "abertura de la lectura que la lista de la decisión no trae: se conserva"})
    # wet_fixtures de la lectura cuyo face dejó de ser MR porque una decisión cambió el board (p. ej. RFI-27 type X WR):
    # inventario.py exige fixture <-> face MR; el fixture sin face MR se quita y se lista (derivado de la decisión)
    if c.get("wet_fixtures"):
        mr = {(w["id"], str(f.get("room"))) for w in c.get("walls") or [] for f in w.get("faces") or []
              if "MR" in str(f.get("board", "")).upper()}
        quedan = [x for x in c["wet_fixtures"] if (x.get("wall"), str(x.get("room"))) in mr]
        for x in c["wet_fixtures"]:
            if x not in quedan:
                sin.append({"group": "board", "list": "wet_fixtures", "id": x.get("ref"), "derivado": True,
                            "motivo": f"{x.get('wall')} / {x.get('room')}: la decisión cambió el board a no-MR"})
        if quedan:
            c["wet_fixtures"] = quedan
        else:
            c.pop("wet_fixtures")
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
