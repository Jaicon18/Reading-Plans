#!/usr/bin/env python3
"""simbolos.py — elementos SIN tag de type detectados por PROGRAMA en el vector de la planta (R80e.40).

  columnas(page)        cuadrados con hatch (muchos trazos cortos dentro de un cuadrado) del MISMO tamaño repetidos
                        >= 3 veces (el grupo modal = símbolo de columna del set) -> candidatos a column wrap.
  discontinuas(page)    cadenas colineales de trazos cortos con paso regular (línea discontinua: "SOFFIT ABOVE",
                        bordes de ceiling) de largo >= min_pt -> candidatos a soffit side.
Coordenadas en la página ROTADA (como se ve), igual que las bands del canon. Solo detecta: la lectura decide con el
plano (keynote / sección) si el candidato lleva el elemento."""
import collections

import fitz


def _segmentos(page):
    m = page.rotation_matrix
    for x in page.get_drawings():
        for it in x["items"]:
            if it[0] == "l":
                yield it[1] * m, it[2] * m, x


def columnas(page, min_rep=3):
    m = page.rotation_matrix
    pts = []
    for x in page.get_drawings():
        r = x["rect"] * m
        if r.width <= 8 and r.height <= 8 and x.get("fill") is None:
            pts.append(((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2, r))
    cell = collections.defaultdict(list)
    for i, (x, y, _) in enumerate(pts):
        cell[(int(x // 5), int(y // 5))].append(i)
    par = list(range(len(pts)))

    def f(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for (cx, cy), ids in cell.items():
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for j in cell.get((cx + dx, cy + dy), []):
                    for i in ids:
                        if abs(pts[i][0] - pts[j][0]) <= 5 and abs(pts[i][1] - pts[j][1]) <= 5:
                            par[f(i)] = f(j)
    comp = collections.defaultdict(list)
    for i in range(len(pts)):
        comp[f(i)].append(i)
    cand = []
    for ids in comp.values():
        if len(ids) < 12:
            continue
        x0 = min(pts[i][2].x0 for i in ids); y0 = min(pts[i][2].y0 for i in ids)
        x1 = max(pts[i][2].x1 for i in ids); y1 = max(pts[i][2].y1 for i in ids)
        if 10 <= x1 - x0 <= 40 and abs((x1 - x0) - (y1 - y0)) <= 1.0:
            cand.append({"x0": round(x0, 1), "y0": round(y0, 1), "x1": round(x1, 1), "y1": round(y1, 1),
                         "trazos": len(ids)})
    por = collections.defaultdict(list)
    for c in cand:
        por[(round(c["x1"] - c["x0"]), round(c["y1"] - c["y0"]))].append(c)
    grupos = [g for g in por.values() if len(g) >= min_rep]
    return max(grupos, key=len) if grupos else []


def discontinuas(page, min_pt=72.0, trazo=(2.0, 15.0), hueco_max=8.0):
    """-> [{ori, c, lo, hi, trazos}] líneas discontinuas H / V (largo >= min_pt)."""
    lin = collections.defaultdict(list)
    for a, b, _ in _segmentos(page):
        if abs(a.y - b.y) < 0.3 and trazo[0] <= abs(a.x - b.x) <= trazo[1]:
            lin[("H", round(a.y, 0))].append((min(a.x, b.x), max(a.x, b.x)))
        elif abs(a.x - b.x) < 0.3 and trazo[0] <= abs(a.y - b.y) <= trazo[1]:
            lin[("V", round(a.x, 0))].append((min(a.y, b.y), max(a.y, b.y)))
    out = []
    for (ori, c), segs in lin.items():
        segs.sort()
        run = [segs[0]]
        for s in segs[1:] + [(1e9, 1e9)]:
            if s[0] - run[-1][1] <= hueco_max and s[0] > run[-1][1]:
                run.append(s)
                continue
            if len(run) >= 4 and run[-1][1] - run[0][0] >= min_pt:
                out.append({"ori": ori, "c": c, "lo": round(run[0][0], 1), "hi": round(run[-1][1], 1), "trazos": len(run)})
            run = [s]
    return out
