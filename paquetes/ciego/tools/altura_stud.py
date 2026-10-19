#!/usr/bin/env python3
"""altura_stud.py — altura de stud DETERMINISTA con fuente de cada número (reglas 60.3 y 59.13).

Por qué existe (arbitraje #10, 16-oct-2026): una corrida llevó los studs exteriores hasta el B.O.D. cuando
el detalle los para en un deflection track BAJO la perimeter beam (~ -300 LF de 6" stud). La otra restó
el peralte. Aquí la altura sale de una fórmula y cada número trae su fuente.

ENTRADA (JSON) — todo número es {"value": x, "source": "N/HOJA"}:
{
  "bod_table": {"source": "S2.20",                       # 59.13: B.O.D. interpolado por wall
                "points": [{"y_ft": 0.0, "bod_ft": <n>}, {"y_ft": 60.0, "bod_ft": <n>}]},
  "beams": {"W12x26": {"d_in": {"value": 12.2, "source": "AISC W12X26"}}},   # peralte d
  "walls": [{
      "id": "W57", "type": "exterior",                   # exterior | interior
      "y_ft": {"value": 0.0, "source": "A02.01"},        # posición para interpolar ...
      "y_to_ft": {"value": 47.4, "source": "A02.01"},    # ... opcional: wall con pendiente (dos extremos)
      "bod_ft": {"value": 14.5, "source": "3/S2.20"},    # ... o B.O.D. directo (manda sobre la tabla)
      "stops_under_beam": {"value": true, "source": "10/S5.10"},   # OBLIGATORIO en exterior
      "beam": "W12x26"}]                                 # obligatorio si stops_under_beam
}
FÓRMULA:
  B.O.D.(y) = interpolación lineal en bod_table (sin extrapolar; y fuera de rango -> ValueError)
  H = B.O.D. - d/12  si stops_under_beam (60.3)   |   H = B.O.D.  si no
  wall con y_to_ft: height_ft = lado ALTO (53.2, largo del stud) y height_avg_ft = promedio (board)
VALIDACIONES (ValueError): número sin source; exterior sin stops_under_beam declarado; beam no declarada;
  H <= 0; tabla con y repetida o < 2 puntos.
SALIDA: por tipo {walls, min, max} + renglón por wall con height_ft, operación y fuentes.

Uso:  python3 altura_stud.py entrada.json salida.json
"""
import json
import re
import sys

EPS = 1e-6
RX_SRC = re.compile(r"^([A-Za-z0-9.]{1,6}/)*[A-Z]{1,3}-?\d[\w.\-]*$")


def _src(x, ctx, plano=True):
    if not isinstance(x, str) or not x.strip():
        raise ValueError(f"{ctx}: falta 'source'")
    if plano:
        for p in re.split(r"\s*[,;·]\s*", x.strip()):
            tok = p.split()[0] if p.split() else ""
            if not RX_SRC.match(tok):
                raise ValueError(f"{ctx}: source '{p}' no tiene forma N/HOJA (ej. 10/S5.10, S2.20)")
    return x.strip()


def _num(o, ctx, plano=True):
    if not isinstance(o, dict) or "value" not in o:
        raise ValueError(f"{ctx}: debe ser {{'value': x, 'source': 'N/HOJA'}} (número sin fuente)")
    s = _src(o.get("source"), ctx, plano)
    v = o["value"]
    if isinstance(v, bool):
        return v, s
    try:
        return float(v), s
    except (TypeError, ValueError):
        raise ValueError(f"{ctx}: value no es número: {v!r}")


def _tabla(t):
    if not t:
        return None
    src = _src(t.get("source"), "bod_table")
    pts = sorted((float(p["y_ft"]), float(p["bod_ft"])) for p in t.get("points") or [])
    if len(pts) < 2:
        raise ValueError("bod_table: necesita >= 2 puntos")
    if any(pts[i][0] >= pts[i + 1][0] - EPS for i in range(len(pts) - 1)):
        raise ValueError("bod_table: y_ft repetida")
    return src, pts


def _interp(tab, y, ctx):
    src, pts = tab
    if y < pts[0][0] - EPS or y > pts[-1][0] + EPS:
        raise ValueError(f"{ctx}: y={y} fuera de bod_table [{pts[0][0]}, {pts[-1][0]}] (no se extrapola)")
    for (y0, b0), (y1, b1) in zip(pts, pts[1:]):
        if y0 - EPS <= y <= y1 + EPS:
            b = b0 + (b1 - b0) * (y - y0) / (y1 - y0)
            return b, f"interp({y}; {y0}->{b0}, {y1}->{b1}) = {round(b, 3)} [{src}]"


def calcular(data):
    tab = _tabla(data.get("bod_table"))
    beams = {}
    for k, b in (data.get("beams") or {}).items():
        d, s = _num(b.get("d_in"), f"beam {k}.d_in", plano=False)
        if d <= EPS:
            raise ValueError(f"beam {k}: d_in <= 0")
        beams[k] = (d, s)
    walls = data.get("walls")
    if not isinstance(walls, list) or not walls:
        raise ValueError("'walls' vacío o ausente")
    filas, res, ids = [], {}, set()
    for w in walls:
        wid = w.get("id")
        if not wid or wid in ids:
            raise ValueError(f"wall sin id o repetido: {wid!r}")
        ids.add(wid)
        tp = w.get("type")
        if tp not in ("exterior", "interior"):
            raise ValueError(f"{wid}: type debe ser exterior | interior")
        fuentes = []
        if "bod_ft" in w:
            b, s = _num(w["bod_ft"], f"{wid}.bod_ft")
            bods, bop = [b], [f"B.O.D. {b} [{s}]"]
            fuentes.append(s)
        else:
            if tab is None:
                raise ValueError(f"{wid}: sin bod_ft y sin bod_table")
            bods, bop = [], []
            for k in ("y_ft", "y_to_ft"):
                if k in w:
                    y, s = _num(w[k], f"{wid}.{k}")
                    fuentes.append(s)
                    b, o = _interp(tab, y, wid)
                    bods.append(b)
                    bop.append(o)
            if not bods:
                raise ValueError(f"{wid}: falta y_ft (o bod_ft)")
            fuentes.append(tab[0])
        if "stops_under_beam" in w:
            sub, s = _num(w["stops_under_beam"], f"{wid}.stops_under_beam")
            if not isinstance(sub, bool):
                raise ValueError(f"{wid}: stops_under_beam.value debe ser true/false")
            fuentes.append(s)
        elif tp == "exterior":
            raise ValueError(f"{wid}: exterior sin 'stops_under_beam' declarado con su detalle (60.3)")
        else:
            sub = False
        d = 0.0
        if sub:
            bm = w.get("beam")
            if bm not in beams:
                raise ValueError(f"{wid}: beam '{bm}' no declarada en beams (60.3)")
            d, s = beams[bm]
            fuentes.append(s)
        hs = [b - d / 12.0 for b in bods]
        if min(hs) <= EPS:
            raise ValueError(f"{wid}: altura <= 0")
        H, Havg = max(hs), sum(hs) / len(hs)
        op = "; ".join(bop) + (f" - d {d}\"/12 = {round(d / 12, 3)} (stud bajo la viga, 60.3)" if sub else
                               " (stud a B.O.D.)") + f" -> H {[round(h, 3) for h in hs]}"
        filas.append({"id": wid, "type": tp, "height_ft": round(H, 3), "height_avg_ft": round(Havg, 3),
                      "operacion": op, "source": " · ".join(dict.fromkeys(fuentes))})
        r = res.setdefault(tp, {"walls": 0, "min_ft": H, "max_ft": H})
        r["walls"] += 1
        r["min_ft"], r["max_ft"] = round(min(r["min_ft"], H), 3), round(max(r["max_ft"], H), 3)
    return {"resumen_por_tipo": res, "renglones": filas}


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    try:
        out = calcular(json.load(open(argv[1])))
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as e:
        print(f"ERROR altura_stud.py: {e}", file=sys.stderr)
        return 1
    open(argv[2], "w").write(json.dumps(out, indent=1))
    print(json.dumps(out["resumen_por_tipo"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
