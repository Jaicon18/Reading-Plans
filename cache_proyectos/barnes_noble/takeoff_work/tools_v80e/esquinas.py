#!/usr/bin/env python3
"""esquinas.py — revisa la geometría de los walls de un takeoff_canon.json (R70.2 y R70.3, v70).

Por qué existe: el LF de un partition type sale corrido cuando una esquina no tiene dueño (los dos walls terminan en la
cara del otro y el cuadrado de la esquina no lo cuenta nadie) o tiene dos (los dos la atraviesan), y cuando una door
queda fuera de todo wall (un wall termina en un jamb y el siguiente empieza en el otro). Las cotas impresas son de cara
de finish a cara de finish; las caras se suman en la esquina que el wall posee. Esta herramienta lo hace visible.

REGLAS
  R70.2  Cada esquina L / T entre dos walls de la misma hoja tiene EXACTAMENTE un dueño.
         - esquina sin dueño: ninguno de los dos cubre el cuadrado de la esquina y los dos llegan a él → FALLA.
         - esquina doble: los dos cubren el cuadrado → FALLA.
         - T: uno lo cubre y el otro termina en su cara → bien.
         Una excepción va declarada en `corners_ok: [{"walls": [id1, id2], "reason": "..."}]` (sin motivo no vale).
  R70.3  Hueco colineal: dos walls sobre la misma línea (ejes a <= 3") separados por un hueco de 1.5 a 12 ft.
         Huecos cubiertos por otro elemento de la misma línea (door bulkhead, cripples)
         o cortados por un wall perpendicular no cuentan. Si el hueco es una door / abertura, el R.O. va DENTRO del run (las doors no se descuentan): FALLA salvo que el
         canon lo explique en `gaps_ok: [{"between": [id1, id2], "reason": "..."}]` (p. ej. "storefront", "pasillo").

Geometría (la misma de particion.py): band = {ori: H|V, c0, c1 (caras, perpendicular), lo, hi (extensión)} en pt de la
hoja; escala constants.plan_scale_pt_per_ft.value (default 18). Solo se comparan walls de la misma hoja (`band.sheet`,
`sheet`, `plan_sheet`). Elementos que no son partition (ceilings, soffits, heads, cripples, parapets, wraps) no entran.

Uso:  python3 esquinas.py takeoff_canon.json [salida.json]      (exit 1 si hay fallas)
"""
import json
import sys

ESCALA_DEFAULT = 18.0
TOL_FT = 0.25            # 3": tolerancia para "llega a la cara"
GAP_MIN_FT, GAP_MAX_FT = 1.5, 12.0
NO_PARTITION = {"storefront_cripples", "vestibule_head", "grille_head", "roof_step", "fascia_box", "canopy_soffit",
                "ceiling_transition", "ceiling_bulkhead", "soffit_side", "soffit_drop", "soffit_bottom", "joist",
                "ceiling_perimeter", "parapet", "column_wrap", "pier", "door_bulkhead", "chase"}


def escala(canon):
    v = (canon.get("constants") or {}).get("plan_scale_pt_per_ft") or {}
    return float(v.get("value") or ESCALA_DEFAULT) if isinstance(v, dict) else float(v or ESCALA_DEFAULT)


def hoja(w):
    b = w.get("band") or {}
    return str(b.get("sheet") or w.get("sheet") or w.get("plan_sheet") or "?")


def geo(w):
    b = w.get("band")
    if not isinstance(b, dict) or b.get("ori") not in ("H", "V"):
        return None
    c0, c1 = sorted((float(b["c0"]), float(b["c1"])))
    lo, hi = sorted((float(b["lo"]), float(b["hi"])))
    return {"ori": b["ori"], "c0": c0, "c1": c1, "lo": lo, "hi": hi}


def todas_las_bandas(canon):
    """Todas las bandas (incluye elementos que no son partition: bulkheads, cripples, wraps) para cubrir huecos."""
    return [(w, geo(w)) for w in canon.get("walls") or [] if geo(w)]


def _hueco_explicado_por_geometria(wa, a, b, todas, tol):
    """True si el hueco [a.hi, b.lo] lo cubre otro elemento sobre la misma línea (bulkhead, cripples…) o lo corta un
    wall perpendicular (entonces no es una abertura entre a y b)."""
    eje = (a["c0"] + a["c1"]) / 2
    esp = max(a["c1"] - a["c0"], b["c1"] - b["c0"])
    g0, g1 = a["hi"], b["lo"]
    cub = []
    for w, g in todas:
        if hoja(w) != hoja(wa):
            continue
        if g["ori"] == a["ori"]:
            if abs((g["c0"] + g["c1"]) / 2 - eje) <= esp + tol and g["hi"] > g0 + tol and g["lo"] < g1 - tol:
                cub.append((max(g0, g["lo"]), min(g1, g["hi"])))
        else:
            if g["lo"] <= a["c0"] + tol and g["hi"] >= a["c1"] - tol and g0 + tol < g["c0"] and g["c1"] < g1 - tol:
                return True
    cub.sort()
    tot, fin = 0.0, g0
    for x0, x1 in cub:
        x0 = max(x0, fin)
        if x1 > x0:
            tot += x1 - x0
            fin = x1
    return tot >= 0.8 * (g1 - g0)


def walls_utiles(canon):
    out = []
    for w in canon.get("walls") or []:
        if w.get("element") in NO_PARTITION:
            continue
        g = geo(w)
        if g:
            out.append((w, g))
    return out


def _esquina(h, v, tol):
    """h = band H, v = band V. Devuelve None si no se tocan; si se tocan: (cubre_h, cubre_v)."""
    # cuadrado de la esquina: x en [v.c0, v.c1], y en [h.c0, h.c1]
    h_llega = h["lo"] <= v["c1"] + tol and h["hi"] >= v["c0"] - tol      # la extensión de h llega a la franja de v
    v_llega = v["lo"] <= h["c1"] + tol and v["hi"] >= h["c0"] - tol
    if not (h_llega and v_llega):
        return None
    cubre_h = h["lo"] <= v["c0"] + tol and h["hi"] >= v["c1"] - tol
    cubre_v = v["lo"] <= h["c0"] + tol and v["hi"] >= h["c1"] - tol
    # cruce completo (los dos siguen de largo a ambos lados) = no es esquina
    h_pasa = h["lo"] < v["c0"] - tol and h["hi"] > v["c1"] + tol
    v_pasa = v["lo"] < h["c0"] - tol and v["hi"] > h["c1"] + tol
    if h_pasa and v_pasa:
        return None
    return cubre_h, cubre_v


def revisar(canon, tol_ft=TOL_FT):
    import criterios                                     # v80e: escala por hoja
    if criterios.multi_escala(canon):
        out = None
        for _, sub in criterios.subcanons_por_hoja(canon):
            r = revisar(sub, tol_ft)
            if out is None:
                out = r
            elif isinstance(r, dict):
                for k, v in r.items():
                    if isinstance(v, list):
                        out[k] = (out.get(k) or []) + v
            else:
                out = out + r
        return out
    esc = escala(canon)
    tol = tol_ft * esc
    ws = walls_utiles(canon)
    todas = todas_las_bandas(canon)
    ok_gaps = {frozenset(x.get("between") or []) for x in canon.get("gaps_ok") or [] if x.get("reason")}
    ok_corners = {frozenset(x.get("walls") or []) for x in canon.get("corners_ok") or [] if x.get("reason")}
    fallas, esquinas, huecos = [], [], []
    for i, (wa, ga) in enumerate(ws):
        for wb, gb in ws[i + 1:]:
            if hoja(wa) != hoja(wb):
                continue
            if ga["ori"] != gb["ori"]:
                (wh, h), (wv, v) = ((wa, ga), (wb, gb)) if ga["ori"] == "H" else ((wb, gb), (wa, ga))
                r = _esquina(h, v, tol)
                if r is None:
                    continue
                cubre_h, cubre_v = r
                e = {"walls": [wh["id"], wv["id"]], "dueno": wh["id"] if cubre_h and not cubre_v else
                     (wv["id"] if cubre_v and not cubre_h else None)}
                if frozenset((wh["id"], wv["id"])) in ok_corners and not (cubre_h != cubre_v):
                    e["estado"] = "EXPLICADA"
                elif cubre_h and cubre_v:
                    e["estado"] = "DOBLE"
                    fallas.append(f"esquina doble {wh['id']} / {wv['id']} ({hoja(wh)}): los dos cubren el cuadrado "
                                  f"de la esquina (R70.2: un solo dueño)")
                elif not cubre_h and not cubre_v:
                    e["estado"] = "SIN DUEÑO"
                    lado = round((v["c1"] - v["c0"]) / esc, 3)
                    fallas.append(f"esquina sin dueño {wh['id']} / {wv['id']} ({hoja(wh)}): ninguno cubre el cuadrado "
                                  f"(falta ~{lado} ft en uno de los dos; R70.2)")
                else:
                    e["estado"] = "OK"
                esquinas.append(e)
            else:
                if abs((ga["c0"] + ga["c1"]) / 2 - (gb["c0"] + gb["c1"]) / 2) > tol:
                    continue
                a, b = (ga, gb) if ga["lo"] <= gb["lo"] else (gb, ga)
                gap = (b["lo"] - a["hi"]) / esc
                if GAP_MIN_FT <= gap <= GAP_MAX_FT and not _hueco_explicado_por_geometria(wa, a, b, todas, tol):
                    par = frozenset((wa["id"], wb["id"]))
                    hz = {"walls": sorted(par), "gap_ft": round(gap, 3), "explicado": par in ok_gaps}
                    huecos.append(hz)
                    if par not in ok_gaps:
                        fallas.append(f"hueco colineal {gap:.3f} ft entre {' y '.join(sorted(par))} ({hoja(wa)}): si es "
                                      f"una door / abertura, su R.O. va dentro del run (R70.3); si no, declararlo en "
                                      f"gaps_ok con su motivo")
    return {"fallas": fallas, "esquinas": esquinas, "huecos": huecos, "escala_pt_por_ft": esc}


def main(argv):
    if len(argv) not in (2, 3):
        print(__doc__)
        return 2
    r = revisar(json.load(open(argv[1])))
    if len(argv) == 3:
        with open(argv[2], "w") as f:
            json.dump(r, f, indent=1, ensure_ascii=False)
    n = {}
    for e in r["esquinas"]:
        n[e["estado"]] = n.get(e["estado"], 0) + 1
    print(f"esquinas: {n}  huecos colineales: {len(r['huecos'])}")
    for x in r["fallas"]:
        print("FALLA:", x)
    print("ESQUINAS OK" if not r["fallas"] else f"ESQUINAS: {len(r['fallas'])} falla(s)")
    return 1 if r["fallas"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
