#!/usr/bin/env python3
"""particion.py — regla de partición de walls como PARÁMETRO (no fija). Toma los walls de un takeoff_canon.json y
los reporta como "walls" según el modo pedido.

Por qué existe: dos lecturas del mismo plano daban walls por type distintos porque cada una partía a su manera
(una contaba cada tramo, otra el run completo con sus quiebres). Mientras el estimador no decida la convención,
la regla vive en UNA constante y las dos lecturas se parten con la misma.

MODOS
  "tramo"  un wall por cada tramo RECTO de un type: segmentos colineales (ejes a <= tol_line_ft) y contiguos
           (hueco <= tol_gap_ft) se unen; un quiebre / esquina empieza otro wall. Jog / return <= jog_max_ft que
           toca un wall del mismo type se suma a ese wall (no es wall propio).
  "run"    un wall por RUN CONTINUO del mismo type aunque tenga quiebres: los tramos rectos se encadenan cuando el
           extremo de uno toca el extremo del otro (esquina L, jog, step). Una T (extremo contra el COSTADO del
           otro) NO encadena: el que llega termina en la cara del que sigue.
Nunca se une entre hojas distintas ni entre types distintos. Segmento sin `band` = wall propio + aviso.

Geometría del canon (la misma de partition_types.py): band = {ori: H|V, c0, c1 (caras, perpendicular), lo, hi
(extensión)} en pt de la hoja; escala constants.plan_scale_pt_per_ft.value (default 18). Hoja del wall: `sheet`
(o `plan_sheet`); si falta, el primer sheet number que aparezca en `source`.

Uso:  python3 particion.py takeoff_canon.json [--modo run|tramo] [salida.json]
"""
import json
import math
import re
import sys
from collections import OrderedDict

MODO_DEFAULT = "tramo"     # <- ÚNICA constante a cambiar cuando el estimador decida ("tramo" | "run")
MODOS = ("tramo", "run")
JOG_MAX_FT = 1.0
TOL_LINE_FT = 0.25        # colineales: ejes a <= 3"
TOL_GAP_FT = 0.5          # contiguos / extremos que se tocan: hueco <= 6" (más el espesor del wall)
ESCALA_DEFAULT = 18.0
NO_PARTITION = ("storefront_cripples", "vestibule_head", "grille_head", "roof_step", "fascia_box", "canopy_soffit",
                "ceiling_transition", "ceiling_bulkhead", "soffit_side", "soffit_drop", "soffit_bottom", "joist",
                "ceiling_perimeter")
SHEET_IN_SRC = re.compile(r"(?:^|[\s/;(,])([A-Z]{1,3}-?\d{1,3}(?:\.\d{1,3}[A-Z]?))\b")


def norm_type(tag):
    return re.sub(r"\s+", "-", str(tag or "").strip().upper())


def hoja(w):
    for k in ("sheet", "plan_sheet"):
        if w.get(k):
            return str(w[k]), w.get("page")
    m = SHEET_IN_SRC.search(" " + str(w.get("source") or ""))
    return (m.group(1) if m else "?"), w.get("page")


def escala(canon):
    v = ((canon.get("constants") or {}).get("plan_scale_pt_per_ft") or {})
    return float(v.get("value") or ESCALA_DEFAULT) if isinstance(v, dict) else float(v or ESCALA_DEFAULT)


def geo(w):
    """(ori, eje, lo, hi, espesor) en pt o None."""
    b = w.get("band")
    if not isinstance(b, dict) or b.get("ori") not in ("H", "V"):
        return None
    c0, c1 = float(b["c0"]), float(b["c1"])
    lo, hi = sorted((float(b["lo"]), float(b["hi"])))
    return b["ori"], (c0 + c1) / 2.0, lo, hi, abs(c1 - c0)


def extremos(g):
    ori, eje, lo, hi, _ = g
    return [(lo, eje), (hi, eje)] if ori == "H" else [(eje, lo), (eje, hi)]


def _tramos(ws, esc, tol_line_ft, tol_gap_ft):
    """Une colineales y contiguos del mismo type y hoja en tramos rectos."""
    tramos = []
    for w in ws:
        g = geo(w)
        L = float(w["length_ft"])
        hecho = False
        if g is not None:
            for t in tramos:
                tg = t["geo"]
                if tg is None or tg[0] != g[0] or abs(tg[1] - g[1]) > tol_line_ft * esc:
                    continue
                if g[2] <= tg[3] + tol_gap_ft * esc and g[3] >= tg[2] - tol_gap_ft * esc:
                    t["ids"].append(w["id"])
                    t["lf"] += L
                    t["geo"] = (tg[0], tg[1], min(tg[2], g[2]), max(tg[3], g[3]), max(tg[4], g[4]))
                    hecho = True
                    break
        if not hecho:
            tramos.append({"ids": [w["id"]], "lf": L, "geo": g})
    return tramos


def _tocan(a, b, esc, tol_gap_ft):
    """¿Algún extremo de a toca algún extremo de b? (esquina L / jog / step; no T)."""
    if a["geo"] is None or b["geo"] is None:
        return False
    lim = max(a["geo"][4], b["geo"][4]) + tol_gap_ft * esc
    return any(math.dist(p, q) <= lim for p in extremos(a["geo"]) for q in extremos(b["geo"]))


def particion(canon, modo=MODO_DEFAULT, jog_max_ft=JOG_MAX_FT, tol_line_ft=TOL_LINE_FT, tol_gap_ft=TOL_GAP_FT):
    if modo not in MODOS:
        raise ValueError(f"modo '{modo}' no existe: {MODOS}")
    esc = escala(canon)
    grupos = OrderedDict()
    otros, avisos = [], []
    for w in canon.get("walls") or []:
        if w.get("element") in NO_PARTITION:
            otros.append(w["id"])
            continue
        t = norm_type(w.get("tag"))
        sh, pg = hoja(w)
        if geo(w) is None:
            avisos.append(f"{w['id']} ({t}, {sh}) sin band: wall propio, no se puede unir")
        grupos.setdefault((t, sh, pg), []).append(w)
    out = OrderedDict()
    for (t, sh, pg), ws in grupos.items():
        tramos = _tramos(ws, esc, tol_line_ft, tol_gap_ft)
        if modo == "run":
            # componentes conexas por extremos que se tocan
            n = len(tramos)
            padre = list(range(n))

            def raiz(i):
                while padre[i] != i:
                    padre[i] = padre[padre[i]]
                    i = padre[i]
                return i
            for i in range(n):
                for j in range(i + 1, n):
                    if _tocan(tramos[i], tramos[j], esc, tol_gap_ft):
                        padre[raiz(i)] = raiz(j)
            comp = OrderedDict()
            for i in range(n):
                comp.setdefault(raiz(i), []).append(tramos[i])
            walls = []
            for parts in comp.values():
                walls.append({"ids": [x for p in parts for x in p["ids"]], "lf": sum(p["lf"] for p in parts),
                              "tramos": len(parts), "geos": [p["geo"] for p in parts]})
        else:
            jogs = [x for x in tramos if x["lf"] <= jog_max_ft + 1e-9]
            if len(jogs) == len(tramos):
                jogs = []
            walls = [{"ids": list(x["ids"]), "lf": x["lf"], "tramos": 1, "geos": [x["geo"]]}
                     for x in tramos if x not in jogs]
            for j in jogs:                        # el jog suma al wall del mismo type que toca
                toca = [k for k, x in enumerate(tramos) if x not in jogs and _tocan(j, x, esc, tol_gap_ft)]
                if toca:
                    dst = walls[[x for x in tramos if x not in jogs].index(tramos[toca[0]])]
                    dst["ids"] += j["ids"]
                    dst["lf"] += j["lf"]
                    dst.setdefault("jogs", []).append({"ids": j["ids"], "lf": round(j["lf"], 3)})
                else:
                    walls.append({"ids": list(j["ids"]), "lf": j["lf"], "tramos": 1, "geos": [j["geo"]]})
                    avisos.append(f"{'+'.join(j['ids'])} ({t}, {sh}) jog <= {jog_max_ft} ft que no toca a otro "
                                  f"wall del mismo type: queda como wall propio")
        for w in walls:
            w["wall"] = "+".join(w["ids"])
            w["lf"] = round(w["lf"], 3)
            w["sheet"], w["page"] = sh, pg
            gs = [g for g in w.pop("geos") if g is not None]
            if gs:
                xs, ys = [], []
                for g in gs:
                    for p in extremos(g):
                        xs.append(p[0])
                        ys.append(p[1])
                e = max(g[4] for g in gs) / 2.0
                w["bbox_pt"] = [round(min(xs) - e, 2), round(min(ys) - e, 2), round(max(xs) + e, 2),
                                round(max(ys) + e, 2)]
                w["bands"] = [{"ori": g[0], "eje": round(g[1], 2), "lo": round(g[2], 2), "hi": round(g[3], 2),
                               "espesor": round(g[4], 2)} for g in gs]
            else:
                w["bbox_pt"] = None
                w["bands"] = []
        d = out.setdefault(t, {"walls": 0, "lf": 0.0, "filas": []})
        d["filas"] += walls
        d["walls"] += len(walls)
        d["lf"] = round(d["lf"] + sum(w["lf"] for w in walls), 3)
    return {"modo": modo, "types": out, "other_framing": otros, "avisos": avisos, "escala_pt_por_ft": esc,
            "regla": {"jog_max_ft": jog_max_ft, "tol_line_ft": tol_line_ft, "tol_gap_ft": tol_gap_ft}}


def main(argv):
    a = list(argv[1:])
    modo = MODO_DEFAULT
    if "--modo" in a:
        i = a.index("--modo")
        modo = a[i + 1]
        del a[i:i + 2]
    if len(a) not in (1, 2):
        print(__doc__)
        return 2
    r = particion(json.load(open(a[0])), modo)
    if len(a) == 2:
        with open(a[1], "w") as f:
            json.dump(r, f, indent=1, ensure_ascii=False)
    print(f"modo = {r['modo']}")
    for t, d in r["types"].items():
        print(f"{t:14s} {d['walls']:3d} walls {d['lf']:9.2f} LF")
    for x in r["avisos"]:
        print("AVISO:", x)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
