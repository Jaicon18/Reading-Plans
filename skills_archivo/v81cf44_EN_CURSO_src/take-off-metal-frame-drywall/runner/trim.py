#!/usr/bin/env python3
"""trim.py — metal trim (corner bead / J-bead) derivado por PROGRAMA de la geometría del canon (R80e.49, regla 53.1).

Categorías (cada una solo si la lectura no trae ya un trim_item de esa categoría):
  - partial height (6 ft <= h < 12 ft): walls cuyo tope queda expuesto (ningún cuarto que miran tiene ceiling a su altura o debajo):
    corner bead 2 x LF (los dos bordes superiores) + 2 esquinas x altura por cada extremo libre (node kind free);
  - column wraps con board de gypsum: 4 esquinas exteriores x altura por cada uno;
  - GWB cloud: perímetro del cloud (ceilings con "cloud") -> corner bead del borde inferior + J-bead del borde superior.
Cada ítem lleva source (hoja) y op [DERIVED]. Nunca pisa trim_items de la lectura."""
import re

CAT = {"partial": re.compile(r"partial|top edge|parcial", re.I), "column": re.compile(r"column|C25|wrap", re.I),
       "cloud": re.compile(r"cloud", re.I)}


def _tiene(c, cat):
    return any(CAT[cat].search(" ".join(str(t.get(k) or "") for k in ("ref", "label", "kind", "op", "source")))
               for t in c.get("trim_items") or [] if isinstance(t, dict))


def derivar(c):
    num = lambda t: set(re.findall(r"\b\d{3}\b", str(t or "")))
    ceil = [(num(z.get("room")), float(z["height_ft"])) for z in c.get("ceilings") or []
            if isinstance(z, dict) and z.get("height_ft") is not None]
    libres = {}
    for n in c.get("nodes") or []:
        if isinstance(n, dict) and n.get("kind") == "free":
            for w in ([n.get("wall")] if n.get("wall") else (n.get("walls") or [])):
                libres[w] = libres.get(w, 0) + 1
    nuevos = []
    if not _tiene(c, "partial"):
        lf_top, esq, ids = 0.0, 0.0, []
        for w in c.get("walls") or []:
            if w.get("element", "wall") != "wall" or w.get("height_ft") is None or w.get("length_ft") is None:
                continue
            h = float(w["height_ft"])
            if h >= 12 or h < 6:                # < 6 ft = counter / knee wall bajo countertop: su tope lo cubre la cubierta
                continue
            techo = [hc for f in w.get("faces") or [] if isinstance(f, dict) for n, hc in ceil if n & num(f.get("room"))]
            if techo and min(techo) <= h + 0.5:
                continue                        # un ceiling cubre el tope: no hay borde expuesto
            lf_top += 2 * float(w["length_ft"])
            esq += 2 * h * libres.get(w["id"], 0)
            ids.append(w["id"])
        if ids:
            nuevos.append({"ref": "PROG-CB-PARTIAL", "kind": "corner_bead", "label": "Corner bead - partial height walls (top edges + free ends)",
                           "lf": round(lf_top + esq, 2), "source": "A-410 partial height types; A-101",
                           "op": f"[DERIVED] top edges 2 x LF ({round(lf_top, 2)}) + free ends 2 corners x height ({round(esq, 2)}) on {', '.join(ids)}"})
    if not _tiene(c, "column"):
        cw = [w for w in c.get("walls") or [] if w.get("element") == "column_wrap" and w.get("height_ft")
              and any(isinstance(f, dict) and "gyp" in str(f.get("board", "")).lower() or "type x" in str(f.get("board", "")).lower()
                      for f in w.get("faces") or [])]      # sin board de gypsum (p. ej. solo FRT plywood) = sin corner bead
        if cw:
            lf = sum(4 * float(w["height_ft"]) for w in cw)
            nuevos.append({"ref": "PROG-CB-COLUMNS", "kind": "corner_bead", "label": "Corner bead - column wraps outside corners",
                           "lf": round(lf, 2), "source": str(cw[0].get("detail") or cw[0].get("sheet") or "A-101"),
                           "op": f"[DERIVED] {len(cw)} column wrap(s) x 4 outside corners x height = {round(lf, 2)}"})
    if not _tiene(c, "cloud"):
        cl = [z for z in c.get("ceilings") or [] if isinstance(z, dict) and re.search("cloud", str(z.get("room")) + str(z.get("system")), re.I)
              and z.get("perimeter_ft")]
        for z in cl:
            p = float(z["perimeter_ft"])
            for kind, lab in (("corner_bead", "bottom edge"), ("j_bead", "top of fascia")):
                nuevos.append({"ref": f"PROG-{kind.upper()}-CLOUD", "kind": kind, "label": f"{kind} - GWB cloud {lab}", "lf": round(p, 2),
                               "source": str(z.get("source") or "A-121"), "op": f"[DERIVED] cloud perimeter {p} LF x 1 ({z.get('room')})"})
    if nuevos:
        c.setdefault("trim_items", []).extend(nuevos)
    return nuevos
