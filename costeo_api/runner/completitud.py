#!/usr/bin/env python3
"""completitud.py — compuerta de completitud de una lectura (R80e.37), sin API.

Falla si:
  - alguna hoja de planta del trade (--plan-sheets) no tiene walls;
  - algún type del schedule que la propia lectura declara (partition_types / types / schedule) no tiene walls ni razón
    "none" (walls_none_reason / types_none_reason);
  - (opcional --otro) algún type / element que la OTRA lectura sí trae falta en esta.
Imprime JSON {"ok", "faltan_hojas", "faltan_types", "faltan_vs_otra", "walls", "lf"}."""
import json
import sys


def types_de(c):
    out = set()
    for w in c.get("walls") or []:
        el = w.get("element", "wall")
        out.add(str(w.get("tag") or "").upper() if el == "wall" else el)
    return out - {""}


def schedule(c):
    s = set()
    for k in ("partition_types", "types", "schedule"):
        v = c.get(k)
        if isinstance(v, dict):
            s |= {str(x).upper() for x in v.keys()}
        elif isinstance(v, list):
            s |= {str(x.get("type") or x.get("tag") or x.get("id") if isinstance(x, dict) else x).upper() for x in v}
    out = set()
    for x in s:                                   # "H1/H2A/H2B" o "1, 1A" = varios types en una entrada
        out |= {y.strip() for y in x.replace(",", "/").split("/")}
    return out - {"", "NONE"}


def revisar(c, plan_sheets, otro=None):
    hojas = {w.get("sheet") for w in c.get("walls") or []}
    none = {str(k).upper() for k in (c.get("types_none_reason") or {}).keys()}
    tp = types_de(c)
    # types del schedule existentes (no los que la propia lectura declara existentes / excluidos con razón)
    excl = {str(k).upper() for k in (c.get("excluded") or {})} if isinstance(c.get("excluded"), dict) else set()
    faltan_t = sorted(t for t in schedule(c) if t not in tp and t not in none and t not in excl)
    faltan_h = sorted(h for h in plan_sheets if h not in hojas)
    vs = sorted(types_de(otro) - tp - none - excl) if otro else []
    return {"ok": not faltan_t and not faltan_h and not vs, "faltan_hojas": faltan_h, "faltan_types": faltan_t,
            "faltan_vs_otra": vs, "walls": len(c.get("walls") or []),
            "lf": round(sum(float(w.get("length_ft") or 0) for w in c.get("walls") or []), 2)}


if __name__ == "__main__":
    c = json.load(open(sys.argv[1]))
    hojas = sys.argv[2].split(",") if len(sys.argv) > 2 else []
    otro = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else None
    r = revisar(c, hojas, otro)
    print(json.dumps(r))
    sys.exit(0 if r["ok"] else 1)
