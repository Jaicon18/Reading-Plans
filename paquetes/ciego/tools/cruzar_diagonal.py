# -*- coding: utf-8 -*-
"""cruzar_diagonal.py (v72) -- cruce de MEP sobre un muro INCLINADO (band ori D).

Por que existe
--------------
`mep.cruces` trabaja sobre bandas H / V; un muro inclinado se saltaba en SILENCIO y no aparecia ni en la lista de
"con penetracion" ni en la de "sin penetracion".

v72 (arbitraje #20): sin geometria ni offsets de ningun proyecto. El muro sale del canon (band D con p0 / p1 del eje
y el espesor `thick_pt`, o faces_top / faces_bottom) y el offset (dx, dy) de la hoja MEP sale de `mep.registro` en
ESTA corrida. Antes leia `mep.OFF` (offsets de un set, quitados en v71) y fallaba test_sin_colisiones.

Aplica EXACTAMENTE el mismo criterio que mep.cruces:
  1. lineweight >= LW_MIN
  2. la linea tiene que ATRAVESAR el muro y sobresalir SOBRESALE pt por los DOS lados
  3. si la misma linea existe en la arquitectonica, es fondo copiado, no MEP
  4. las lineas paralelas muy juntas se agrupan: un ducto viene en PAREJA y la separacion es su ancho

Uso:  python3 cruzar_diagonal.py takeoff_canon.json <wall_id> <pagina MEP 0-based> <pagina arq 0-based> --dx DX --dy DY
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def eje_de_banda(band):
    """band D del canon -> (P0, P1, u, n, espesor_pt). Usa p0 / p1 (eje) y thick_pt, o el promedio de las caras."""
    if band.get("p0") is not None and band.get("p1") is not None:
        p0, p1 = [float(v) for v in band["p0"]], [float(v) for v in band["p1"]]
    else:
        ft, fb = band["faces_top"], band["faces_bottom"]
        p0 = [(float(ft[0][0]) + float(fb[0][0])) / 2, (float(ft[0][1]) + float(fb[0][1])) / 2]
        p1 = [(float(ft[1][0]) + float(fb[1][0])) / 2, (float(ft[1][1]) + float(fb[1][1])) / 2]
    esp = band.get("thick_pt")
    if esp is None and band.get("faces_top") and band.get("faces_bottom"):
        (ax, ay), (bx, by) = band["faces_top"][0], band["faces_bottom"][0]
        esp = abs(float(by) - float(ay)) if abs(float(bx) - float(ax)) < 1e-6 else math.hypot(bx - ax, by - ay)
    if esp is None:
        raise ValueError("band D sin thick_pt ni faces_top / faces_bottom: no se conoce el espesor del muro")
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    if L < 1e-6:
        raise ValueError("band D con p0 = p1")
    u = ((p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L)
    n = (-u[1], u[0])
    return tuple(p0), tuple(p1), u, n, float(esp)


def _corta(p, q, r, s):
    d = lambda a, b, c: (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    d1, d2, d3, d4 = d(r, s, p), d(r, s, q), d(p, q, r), d(p, q, s)
    return ((d1 > 0) != (d2 > 0)) and ((d3 > 0) != (d4 > 0))


def _dist_normal(pt, o, n):
    """Distancia CON SIGNO del punto al eje, sobre la normal del muro."""
    return (pt[0] - o[0]) * n[0] + (pt[1] - o[1]) * n[1]


def cruces_diagonal(page, off, band, arq, lwmin=None, sob=None):
    import geo
    import mep
    lwmin = mep.LW_MIN if lwmin is None else lwmin
    sob = mep.SOBRESALE if sob is None else sob
    A, R = geo.load(mep._arq(arq)), geo.load(page)
    dx, dy = off["dx"], off["dy"]
    P0, P1, u, n, esp = eje_de_banda(band)
    semi = esp / 2.0
    out = []
    for key in ("H", "V"):
        for c, a, b, lw in R[key]:
            if lw < lwmin:
                continue
            if key == "H":
                p, q = (a + dx, c + dy), (b + dx, c + dy)
            else:
                p, q = (c + dx, a + dy), (c + dx, b + dy)
            if math.hypot(q[0] - p[0], q[1] - p[1]) < 3:
                continue
            if not _corta(p, q, P0, P1):
                continue
            d1, d2 = _dist_normal(p, P0, n), _dist_normal(q, P0, n)
            if not (min(d1, d2) <= -(semi + sob) and max(d1, d2) >= (semi + sob)):
                continue
            if mep._en_arq(A, key, c + (dy if key == "H" else dx), a + (dx if key == "H" else dy),
                           b + (dx if key == "H" else dy)):
                continue
            s = ((p[0] + q[0]) / 2 - P0[0]) * u[0] + ((p[1] + q[1]) / 2 - P0[1]) * u[1]
            out.append({"s": round(s, 2), "key": key, "lw": round(lw, 2),
                        "len": round(math.hypot(q[0] - p[0], q[1] - p[1]), 2)})
    out.sort(key=lambda d: d["s"])
    grupos, act = [], None
    for p in out:
        if act and p["s"] - act[-1]["s"] <= 40:
            act.append(p)
        else:
            act = [p]
            grupos.append(act)
    return grupos


def main(argv):
    a = list(argv[1:])
    opts = {}
    for k in ("--dx", "--dy"):
        if k in a:
            i = a.index(k)
            opts[k] = float(a[i + 1])
            del a[i:i + 2]
    if len(a) != 4 or len(opts) != 2:
        print(__doc__)
        return 2
    canon, wid, pg, arq = a[0], a[1], int(a[2]), int(a[3])
    w = next((x for x in json.load(open(canon)).get("walls") or [] if x.get("id") == wid), None)
    if w is None or str((w.get("band") or {}).get("ori")).upper() != "D":
        print(f"ERROR: {wid} no está en el canon o su band no es ori D", file=sys.stderr)
        return 1
    g = cruces_diagonal(pg, {"dx": opts["--dx"], "dy": opts["--dy"]}, w["band"], arq)
    print(json.dumps({"wall": wid, "grupos": g, "n": len(g)}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
