#!/usr/bin/env python3
"""completitud.py — compuerta de completitud de una lectura (R80e.37), sin API.

Falla si:
  - alguna hoja de planta del trade (--plan-sheets) no tiene walls;
  - algún type del schedule que la propia lectura declara (partition_types / types / schedule) no tiene walls ni razón
    "none" (walls_none_reason / types_none_reason);
  - (opcional --otro) algún type / element que la OTRA lectura sí trae falta en esta.
Imprime JSON {"ok", "faltan_hojas", "faltan_types", "faltan_vs_otra", "walls", "lf"}.

R80e.40 — conteos(): CONTEOS por type y hoja contra fuentes que no son la lectura (sin API):
  - cada partition tag del inventario (id, type, hoja, centro) debe tener un wall de su type a <= tol_ft de su band;
  - cada símbolo de columna de la planta (simbolos.columnas) debe tener un column_wrap encima (o columns_none_reason);
  - en planos AMPLIADOS (escala >= 18 pt/ft) cada línea discontinua larga (simbolos.discontinuas: "SOFFIT ABOVE")
    debe tener un soffit_side encima (o dashed_none_reason con la nota que dice qué es).
Lo que falta sale con hoja y coordenadas para continuar la lectura SOBRE esos tags concretos."""
import json
import re
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


def _rect(b):
    if not isinstance(b, dict):
        return None
    o = b.get("ori")
    try:
        if o == "H":
            return b["lo"], min(b["c0"], b["c1"]), b["hi"], max(b["c0"], b["c1"])
        if o == "V":
            return min(b["c0"], b["c1"]), b["lo"], max(b["c0"], b["c1"]), b["hi"]
        if o == "BOX":
            return (b["x0"], b["y0"], b["x1"], b["y1"]) if "x0" in b else (b["c0"], b["lo"], b["c1"], b["hi"])
        if o == "D":
            (x0, y0), (x1, y1) = b["p0"], b["p1"]
            return min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)
    except (KeyError, TypeError, ValueError):
        return None
    return None


def _dist(r, x, y):
    return (max(r[0] - x, 0, x - r[2]) ** 2 + max(r[1] - y, 0, y - r[3]) ** 2) ** 0.5


def _escala(c, h):
    cs = c.get("constants") or {}
    return float(((cs.get("plan_scale_by_sheet") or {}).get(h) or {}).get("value")
                 or (cs.get("plan_scale_pt_per_ft") or {}).get("value") or 9.0)


def conteos(c, inventario=None, pdf=None, hojas_pag=None, tol_ft=6.0, titulos=None):
    """-> {"faltan_tags": [...], "faltan_columnas": [...], "faltan_discontinuas": [...], "resumen": {...}}"""
    # types_none_reason excusa un tag del inventario SOLO si el type es existente / by others / fuera de alcance;
    # "no lo encontré" no excusa un tag que el inventario sí tiene en el plano
    exc = re.compile(r"exist|by others|future tenant|landlord|N\.?I\.?C\b|not in (contract|scope)|by owner", re.I)
    tnr = {str(k).upper(): str(v) for k, v in (c.get("types_none_reason") or {}).items()}
    none = {k for k, v in tnr.items() if exc.search(v)}
    walls = [w for w in c.get("walls") or [] if _rect(w.get("band"))]
    out = {"faltan_tags": [], "faltan_columnas": [], "faltan_discontinuas": [], "resumen": {},
           "alturas_placeholder": alturas_placeholder(c, titulos)}
    # 1) partition tags del inventario
    for v in ((inventario or {}).get("ocurrencias") or {}).values():
        for t in v:
            if not str(t.get("id", "")).startswith("PT") or not t.get("center_pt"):
                continue
            ty, h = str(t.get("type")).upper(), t.get("sheet")
            if ty in none:
                continue
            x, y = t["center_pt"]
            ok = any(str(w.get("tag")).upper() == ty and (w["band"].get("sheet") or w.get("sheet")) == h and
                     _dist(_rect(w["band"]), x, y) <= tol_ft * _escala(c, h) for w in walls)
            k = (h, ty)
            r = out["resumen"].setdefault(f"{h} type {ty}", {"tags": 0, "con_wall": 0})
            r["tags"] += 1
            if ok:
                r["con_wall"] += 1
            else:
                out["faltan_tags"].append({"id": t["id"], "type": ty, "sheet": h, "center_pt": [round(x, 1), round(y, 1)],
                                           "none_reason": tnr.get(ty)})
    if not pdf or not hojas_pag:
        return out
    import fitz
    import simbolos
    doc = fitz.open(pdf)
    planta = {w.get("sheet") for w in walls}
    for h in sorted(planta):
        if h not in hojas_pag:
            continue
        pg = doc[hojas_pag[h]]
        # 2) columnas sin column_wrap
        if not c.get("columns_none_reason"):
            cw = [_rect(w["band"]) for w in walls if w.get("element") == "column_wrap" and
                  (w["band"].get("sheet") or w.get("sheet")) == h]
            for col in simbolos.columnas(pg):
                cx, cy = (col["x0"] + col["x1"]) / 2, (col["y0"] + col["y1"]) / 2
                if not any(_dist(r, cx, cy) <= 1.0 * _escala(c, h) for r in cw):
                    out["faltan_columnas"].append({"sheet": h, "center_pt": [round(cx, 1), round(cy, 1)],
                                                   "size_pt": round(col["x1"] - col["x0"], 1)})
        # 3) líneas discontinuas largas en planos ampliados sin soffit_side
        esc = _escala(c, h)
        if esc >= 18 and not c.get("dashed_none_reason"):
            ss = [_rect(w["band"]) for w in c.get("walls") or [] if w.get("element") == "soffit_side" and
                  _rect(w.get("band")) and (w["band"].get("sheet") or w.get("sheet")) == h]
            for dl in simbolos.discontinuas(pg, min_pt=3 * esc):
                L = dl["hi"] - dl["lo"]
                if dl["ori"] == "H":
                    cub = sum(max(0, min(r[2], dl["hi"]) - max(r[0], dl["lo"])) for r in ss
                              if r[1] - 1 * esc <= dl["c"] <= r[3] + 1 * esc)
                else:
                    cub = sum(max(0, min(r[3], dl["hi"]) - max(r[1], dl["lo"])) for r in ss
                              if r[0] - 1 * esc <= dl["c"] <= r[2] + 1 * esc)
                if cub < 0.5 * L:
                    out["faltan_discontinuas"].append({"sheet": h, "ori": dl["ori"], "c_pt": dl["c"], "lo_pt": dl["lo"],
                                                       "hi_pt": dl["hi"], "ft": round(L / esc, 2)})
    return out


PLACEHOLDER = re.compile(r"not printed|placeholder|no impres|assumed height", re.I)


def titulos_hojas(sheet_map):
    """SHEET_MAP.md -> {sheet: título} (para saber qué hojas son secciones / elevaciones)."""
    out = {}
    for l in open(sheet_map, encoding="utf-8"):
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) >= 2 and c[0].isdigit():
            m = re.match(r"([A-Z]{1,2}-?\d{3}[A-Z]?)\s*(.*)", c[1])
            if m:
                out.setdefault(m.group(1), m.group(2))
    return out


def alturas_placeholder(c, titulos):
    """R80e.44: walls con altura placeholder ("NOT PRINTED", "placeholder") mientras el set tiene secciones /
    elevaciones que la lectura no citó en ninguna altura -> {walls, hojas} para continuar sobre esas hojas."""
    # placeholder = la propia lectura lo declara: height_status PENDIENTE o la palabra "placeholder" en la fuente
    ws = [w["id"] for w in c.get("walls") or [] if w.get("height_ft") is not None
          and (str(w.get("height_status") or "").upper() == "PENDIENTE"
               or re.search(r"placeholder", str(w.get("height_source") or ""), re.I))]
    if not ws:
        return {"walls": [], "hojas": []}
    citadas = " ".join(str(w.get("height_source") or "") for w in c.get("walls") or [])
    hojas = [h for h, t in sorted((titulos or {}).items()) if re.search(r"section|elevation", t, re.I) and h not in citadas]
    return {"walls": ws, "hojas": hojas}


def motivo_conteos(r):
    """Texto para la continuación: los tags / símbolos concretos que faltan, con hoja y coordenadas."""
    l = []
    if r["faltan_tags"]:
        l.append("PARTITION TAGS DEL INVENTARIO SIN WALL DE SU TYPE (léelos en el plano en esa posición; agrega el wall "
                 "o pon el type en types_none_reason con su N/HOJA):")
        l += [f"  - {t['id']} type {t['type']} en {t['sheet']} @ ({t['center_pt'][0]}, {t['center_pt'][1]}) pt"
              + (f" (tu types_none_reason dice: {t['none_reason'][:90]})" if t.get("none_reason") else "") for t in r["faltan_tags"]]
    if r["faltan_columnas"]:
        l.append("SÍMBOLOS DE COLUMNA EN LA PLANTA SIN column_wrap (lee la keynote / detalle: si llevan wrap, agrégalo como "
                 "element column_wrap con band BOX; si no, columns_none_reason con la nota):")
        l += [f"  - {x['sheet']} @ ({x['center_pt'][0]}, {x['center_pt'][1]}) pt, cuadrado {x['size_pt']} pt" for x in r["faltan_columnas"]]
    if r["faltan_discontinuas"]:
        l.append("LÍNEAS DISCONTINUAS LARGAS (SOFFIT ABOVE / borde de ceiling) EN EL PLANO AMPLIADO SIN soffit_side (lee la "
                 "sección del soffit; si es un soffit side agrégalo con su band sobre la línea; si no, dashed_none_reason):")
        l += [f"  - {x['sheet']} {x['ori']} c={x['c_pt']} de {x['lo_pt']} a {x['hi_pt']} pt ({x['ft']} ft)" for x in r["faltan_discontinuas"]]
    ap = r.get("alturas_placeholder") or {}
    if ap.get("walls") and ap.get("hojas"):
        l.append(f"ALTURAS PLACEHOLDER ('NOT PRINTED' / placeholder) en {len(ap['walls'])} wall(s) ({', '.join(ap['walls'][:15])}) "
                 f"mientras el set tiene secciones / elevaciones que no abriste: {', '.join(ap['hojas'])}. Lee el B.O.D. / "
                 "T.O. stud impreso en esas hojas y corrige height_ft + height_source (o deja la RFI con la hoja revisada).")
    return "\n".join(l)


if __name__ == "__main__":
    c = json.load(open(sys.argv[1]))
    hojas = sys.argv[2].split(",") if len(sys.argv) > 2 else []
    otro = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else None
    r = revisar(c, hojas, otro)
    print(json.dumps(r))
    sys.exit(0 if r["ok"] else 1)
