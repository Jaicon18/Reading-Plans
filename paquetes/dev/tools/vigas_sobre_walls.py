#!/usr/bin/env python3
"""vigas_sobre_walls.py v71 — walls interiores que corren JUSTO bajo una línea de viga del plan estructural.

Por qué existe (arbitraje #15A/#15B, 2026-10-17, regla E26): #15B llevó a B.O.D. walls cuyo tipo dice "TO UNDERSIDE
OF STRUCTURE" estando bajo una viga de la planta estructural (S*): esos studs paran bajo la viga (stops_under_beam),
no en el deck. Mirarlo a ojo variaba entre agentes; la geometría vectorial no.

Qué hace (determinista):
  1. Registra la hoja S* contra la planta de arquitectura con las burbujas de GRID que tienen las dos hojas
     (labels de número -> eje x, de letra -> eje y; ajuste lineal por eje: x_S = sx * x_A + dx). Sin al menos
     2 grids comunes por eje -> error (o --map sx,dx,sy,dy a mano, con su fuente).
  2. Toma las líneas de viga de la hoja S* (lw >= --lw, default 2.0; largo >= 3 ft) y las lleva a coordenadas
     de la planta A.
  3. Cruza contra la band de cada wall del takeoff_canon.json (band {ori H|V, c0, c1, lo, hi} en la planta A):
     una viga paralela cuyo eje cae dentro de la band (± --tol pt) y se solapa en largo = wall bajo viga.
SALIDA: lista {wall, tag, ori, beam_lw, covered_ft, pct, beam_axis_pt, profile, depth_ft, d_source} (v68: marca W
del rótulo más cercano a la viga en la hoja S y su peralte AISC) — cada uno con imagen y la decisión
stops_under_beam {profile, depth_ft, source} en el canon (altura_stud.py), o motivo si no aplica.

Uso:
  python3 vigas_sobre_walls.py bidset.pdf <hoja S, ej. S2.20> <hoja A, ej. A02.01> takeoff_canon.json [--lw 2.0]
         [--tol 3.0] [--map sx,dx,sy,dy] [--json salida.json]
Las páginas se buscan por número de hoja (como contar_tags.py). Coordenadas: página rotada (rotation_matrix).
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

RX_GRID_NUM = re.compile(r"^\d{1,2}(\.\d)?$")
RX_GRID_LET = re.compile(r"^[A-Z](\.\d)?$")
PT_FT = 18.0          # escala de verificación (1/4" = 1'-0"); solo para reportar covered_ft
# v68 (#16A: un solo peralte W12x19 para walls bajo W14x30 / W14x22 / W18x35): peralte nominal d (in) de las marcas
# W más comunes en planta de techo (AISC Steel Construction Manual, tabla 1-1). Una marca fuera de la tabla -> d_source.
AISC_D_IN = {"W8X10": 7.89, "W8X18": 8.14, "W10X12": 9.87, "W10X19": 10.2, "W12X14": 11.9, "W12X16": 12.0,
             "W12X19": 12.2, "W12X22": 12.3, "W12X26": 12.2, "W14X22": 13.7, "W14X26": 13.9, "W14X30": 13.8,
             "W16X26": 15.7, "W18X35": 17.7, "W18X40": 17.9, "W21X44": 20.7}
RX_MARCA = re.compile(r"^W\d{1,2}X\d{2,3}$")


def ajustar(pares):
    """Mínimos cuadrados 1D: [(a, s)] -> (k, d) con s = k * a + d."""
    n = len(pares)
    if n < 2:
        raise ValueError(f"registro: {n} grid(s) común(es) en el eje; hacen falta 2 (o --map con fuente)")
    ma = sum(a for a, _ in pares) / n
    ms = sum(s for _, s in pares) / n
    va = sum((a - ma) ** 2 for a, _ in pares)
    if va < 1e-9:
        raise ValueError("registro: grids sin separación en el eje")
    k = sum((a - ma) * (s - ms) for a, s in pares) / va
    d = ms - k * ma
    res = max(abs(k * a + d - s) for a, s in pares)
    if res > 4.0:
        raise ValueError(f"registro: residuo {round(res, 2)} pt > 4 (grids que no coinciden entre hojas)")
    return k, d


def registrar(grids_a, grids_s):
    """grids_*: {label: (x, y)}. Números fijan x, letras fijan y. Devuelve (sx, dx, sy, dy) de A -> S."""
    px = [(grids_a[k][0], grids_s[k][0]) for k in grids_a if k in grids_s and RX_GRID_NUM.match(k)]
    py = [(grids_a[k][1], grids_s[k][1]) for k in grids_a if k in grids_s and RX_GRID_LET.match(k)]
    sx, dx = ajustar(px)
    sy, dy = ajustar(py)
    return sx, dx, sy, dy


def a_planta(seg, mapa):
    """Segmento de la hoja S -> coordenadas de la planta A."""
    sx, dx, sy, dy = mapa
    (x0, y0), (x1, y1) = seg
    return ((x0 - dx) / sx, (y0 - dy) / sy), ((x1 - dx) / sx, (y1 - dy) / sy)


def marca(t):
    return str(t or "").upper().replace(" ", "").replace("×", "X")


def _dist_rotulo(viga, x, y):
    """Distancia perpendicular del rótulo al eje de la viga si cae dentro de su largo (± 1 pt); si no, None."""
    (x0, y0), (x1, y1) = viga["p0"], viga["p1"]
    if abs(x1 - x0) >= abs(y1 - y0):
        return abs(y - (y0 + y1) / 2) if min(x0, x1) - 1 <= x <= max(x0, x1) + 1 else None
    return abs(x - (x0 + x1) / 2) if min(y0, y1) - 1 <= y <= max(y0, y1) + 1 else None


def perfil(viga, rotulos, max_pt=36.0, otras=None):
    """v68: rótulo W de la viga = el rótulo de marca W más cercano al segmento (paralelo o no), a <= max_pt del eje y
    dentro de su largo. rotulos: [(texto, x, y)] en coordenadas de la planta A. Sin rótulo -> None (RFI con d).
    v71 (arbitraje #19, P4): con `otras` (las demás vigas de la hoja), un rótulo que está MÁS CERCA de otra viga
    paralela no es de esta (dos vigas paralelas a pocas pulgadas: cada rótulo tiene un solo dueño)."""
    (x0, y0), (x1, y1) = viga["p0"], viga["p1"]
    mejor = None
    for t, x, y in rotulos:
        m = marca(t)
        if not RX_MARCA.match(m):
            continue
        d_esta = _dist_rotulo(viga, x, y)
        if d_esta is not None and otras:
            if any(o is not viga and (_dist_rotulo(o, x, y) is not None) and _dist_rotulo(o, x, y) < d_esta - 0.01
                   for o in otras):
                continue
        if abs(x1 - x0) >= abs(y1 - y0):           # viga H
            if not (min(x0, x1) - 1 <= x <= max(x0, x1) + 1):
                continue
            dist = abs(y - (y0 + y1) / 2)
        else:
            if not (min(y0, y1) - 1 <= y <= max(y0, y1) + 1):
                continue
            dist = abs(x - (x0 + x1) / 2)
        if dist <= max_pt and (mejor is None or dist < mejor[0]):
            mejor = (dist, m)
    if mejor is None:
        return None
    m = mejor[1]
    return {"profile": m, "d_in": AISC_D_IN.get(m), "depth_ft": round(AISC_D_IN[m] / 12.0, 3) if m in AISC_D_IN else None,
            "d_source": "AISC d nominal" if m in AISC_D_IN else "fuera de tabla: d_source obligatorio"}


CERCA_PT = 18.0       # v71: otra viga paralela con eje a <= 1 ft de la band = candidata (ambigüedad si su rótulo difiere)


def cruzar(vigas, walls, tol=3.0, min_ft=1.0):
    """vigas: [{"p0": (x, y), "p1": (x, y), "lw": w}] en coordenadas de la planta A.
    walls: walls del canon con band {ori, c0, c1, lo, hi}. Devuelve los walls bajo viga.
    v71 (P4): manda la viga cuyo EJE cae dentro de la band; si otra viga paralela con OTRO rótulo tiene el eje a
    <= CERCA_PT de la band y también se solapa, el wall sale con profile None + `candidatas` (las dos con su rótulo)
    + `decision`: se decide con imagen (RFI), nunca por el rótulo más cercano."""
    out = []
    for w in walls:
        b = w.get("band")
        if not b or b.get("ori") not in ("H", "V"):
            continue
        c0, c1 = sorted((float(b["c0"]), float(b["c1"])))
        lo, hi = sorted((float(b["lo"]), float(b["hi"])))
        mejor, cands = None, []
        for v in vigas:
            (x0, y0), (x1, y1) = v["p0"], v["p1"]
            if b["ori"] == "H":
                if abs(y1 - y0) > 1.0:
                    continue
                eje, a, z = (y0 + y1) / 2, min(x0, x1), max(x0, x1)
            else:
                if abs(x1 - x0) > 1.0:
                    continue
                eje, a, z = (x0 + x1) / 2, min(y0, y1), max(y0, y1)
            dentro = c0 - tol <= eje <= c1 + tol
            if not dentro and not (c0 - CERCA_PT <= eje <= c1 + CERCA_PT):
                continue
            solape = min(hi, z) - max(lo, a)
            if solape / PT_FT < min_ft:
                continue
            c = {"solape": solape, "eje": eje, "lw": v.get("lw"), "perfil": v.get("perfil"), "dentro": dentro}
            cands.append(c)
            if dentro and (mejor is None or solape > mejor["solape"]):
                mejor = c
        if mejor:
            otros = {(c["perfil"] or {}).get("profile") for c in cands if c is not mejor} - \
                {(mejor["perfil"] or {}).get("profile")}
            if otros:
                out.append({"wall": w["id"], "tag": w.get("tag"), "ori": b["ori"], "profile": None, "depth_ft": None,
                            "candidatas": [{"profile": (c["perfil"] or {}).get("profile"),
                                            "beam_axis_pt": round(c["eje"], 2), "inside_band": c["dentro"],
                                            "covered_ft": round(c["solape"] / PT_FT, 3)} for c in cands],
                            "decision": "dos vigas paralelas a <= 1 ft con rótulos distintos: decidir con imagen de la "
                                        "hoja S (RFI); nunca el rótulo más cercano"})
                continue
            pf = mejor["perfil"] or {}
            out.append({"wall": w["id"], "tag": w.get("tag"), "ori": b["ori"], "beam_lw": mejor["lw"],
                        "beam_axis_pt": round(mejor["eje"], 2), "covered_ft": round(mejor["solape"] / PT_FT, 3),
                        "pct": round(100 * mejor["solape"] / max(hi - lo, 1e-9), 1),
                        "profile": pf.get("profile"), "depth_ft": pf.get("depth_ft"),
                        "d_source": pf.get("d_source") or "sin rótulo W junto a la viga: RFI con d"})
    return out


def _pagina(doc, hoja):
    import contar_tags
    return contar_tags.pagina_de_hoja(doc, hoja)


def burbujas(cands):
    """cands: [(label, x, y)]. Las burbujas de grid de una hoja están ALINEADAS: los números en una fila (misma y),
    las letras en una columna (misma x). Se toma la fila / columna con más labels distintos (no el texto más grande:
    un '1' de un título o una key note no es un grid)."""
    out = {}
    for rx, eje in ((RX_GRID_NUM, 2), (RX_GRID_LET, 1)):
        grupos = {}
        for lab, x, y in cands:
            if rx.match(lab):
                grupos.setdefault(round((x, y)[eje - 1] / 6.0), []).append((lab, x, y))
        if not grupos:
            continue
        mejor = max(grupos.values(), key=lambda g: len({lab for lab, _, _ in g}))
        for lab, x, y in mejor:
            out.setdefault(lab, (x, y))
    return out


def _grids(page, min_size=14.0):
    import pymupdf
    m = page.rotation_matrix
    cands = []
    for blk in page.get_text("dict")["blocks"]:
        for ln in blk.get("lines", []):
            for s in ln["spans"]:
                t = s["text"].strip()
                if s["size"] >= min_size and (RX_GRID_NUM.match(t) or RX_GRID_LET.match(t)):
                    r = pymupdf.Rect(s["bbox"]) * m
                    cands.append((t, (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2))
    return burbujas(cands)


def _rotulos(page):
    import pymupdf
    m = page.rotation_matrix
    out = []
    for w in page.get_text("words"):
        if RX_MARCA.match(marca(w[4])):
            r = pymupdf.Rect(w[:4]) * m
            out.append((w[4], (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2))
    return out


def _vigas(page, lw, min_pt=54.0):
    m = page.rotation_matrix
    out = []
    for dr in page.get_drawings():
        w = dr.get("width") or 0
        if w < lw:
            continue
        for it in dr["items"]:
            if it[0] == "l":
                a, b = it[1] * m, it[2] * m
                if abs(a - b) >= min_pt:
                    out.append({"p0": (a.x, a.y), "p1": (b.x, b.y), "lw": round(w, 2)})
    return out


def main(argv):
    a = argv[1:]
    opts = {"--lw": "2.0", "--tol": "3.0", "--map": None, "--json": None}
    for k in list(opts):
        if k in a:
            i = a.index(k)
            opts[k] = a[i + 1]
            del a[i:i + 2]
    if len(a) != 4:
        print(__doc__)
        return 2
    pdf, hoja_s, hoja_a, canon = a
    try:
        import pymupdf
        doc = pymupdf.open(pdf)
        ps, pa = doc[_pagina(doc, hoja_s)], doc[_pagina(doc, hoja_a)]
        mapa = tuple(float(x) for x in opts["--map"].split(",")) if opts["--map"] else \
            registrar(_grids(pa), _grids(ps))
        vigas = []
        rot = _rotulos(ps)
        crudas = _vigas(ps, float(opts["--lw"]))
        for v in crudas:
            pf = perfil(v, rot, otras=crudas)         # v68: rótulo en la hoja S; v71: un dueño por rótulo
            p0, p1 = a_planta((v["p0"], v["p1"]), mapa)
            vigas.append({"p0": p0, "p1": p1, "lw": v["lw"], "perfil": pf})
        walls = json.load(open(canon)).get("walls") or []
        res = cruzar(vigas, walls, float(opts["--tol"]))
    except (ValueError, KeyError, OSError) as e:
        print(f"ERROR vigas_sobre_walls.py: {e}", file=sys.stderr)
        return 1
    out = {"registro_A_a_S": {"sx": round(mapa[0], 5), "dx": round(mapa[1], 2), "sy": round(mapa[2], 5),
                              "dy": round(mapa[3], 2)}, "vigas": len(vigas), "walls_bajo_viga": res}
    s = json.dumps(out, indent=1)
    if opts["--json"]:
        open(opts["--json"], "w").write(s)
    print(s)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
