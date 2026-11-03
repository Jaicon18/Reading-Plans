#!/usr/bin/env python3
"""verificar_markups_excel.py — R80f.7 / BE-117 (usuario 3-nov-2026, INVIOLABLE): lo que se entrega está 100 %
terminado; TODA verificación de los markups se hace ANTES de entregar, por programa, contra el Excel.

Para CADA anotación del take-off en el PDF de markups (walls, board-only, soffit sides, demo, ceilings / áreas):
  (a) Contents TYPE · LF · H · SF · DETAIL · Wall ID idénticos al renglón del Excel con el mismo Wall ID
      (Partition Takeoff por "Wall #"; si no está ahí, el desglose "ID valor" de Material Summary "Where it comes
      from"); LF / H / SF dentro del redondeo impreso (0.01; 1/8" en H); TYPE en el grupo / renglón; cada N/HOJA
      del DETAIL en el renglón; Depth = H. Sin Wall ID = falla (no se puede cuadrar).
  (b) /Measure (escala) = escala impresa de su hoja: constants.plan_scale_by_sheet[hoja] (o plan_scale_pt_per_ft)
      dentro de 0.5 %; si el texto de la hoja trae rótulos SCALE, la escala del canon tiene que estar entre ellos.
  (c) Length de Bluebeam (largo de la polilínea / escala) vs LF <= 0.5 %; en un área cerrada sin H, área / escala²
      vs SF <= 0.5 %; si no, una causa escrita en el elemento del canon (length_cause / area_cause /
      measure_cause) o un campo "cause: ..." en el Contents.
  (d) toda hoja con elementos del take-off en el canon tiene markups; todo elemento con geometría del canon
      (walls, existing_walls, demo_geom) y todo renglón "Wall #" del Partition Takeoff tiene su anotación.
Uso:
  python3 verificar_markups_excel.py <markups.pdf> <excel.xlsx> <takeoff_canon.json> [--out report.md]
rc 0 = todo OK; rc 1 = fallas (lista en stdout); el reporte lleva una línea por anotación.
La compuerta A_MARKUPS_EXCEL de reglas.py (modo final) corre `verificar` sobre el PDF de entrega (`buscar_pdf`).
"""
import glob
import json
import math
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

TOL_REL = 0.005          # tolerancia relativa de escala y de largo (BE-117)
TOL_NUM = 0.01           # redondeo
TOL_H = 0.01 + 1.0 / 192  # H en ft-in a 1/8"
AUTORES = ("take-off",)
NM_LEY = "TO-LEGEND-"
NHOJA_RX = re.compile(r"\b[0-9A-Z]{1,6}/(?!KN\d)[A-Z]{1,3}-?\d{1,4}(?:\.\d{1,3})?[A-Z]?\b")
HOJA_RX = re.compile(r"(?<![\w/])[A-Z]{1,3}-\d{3}[A-Z]?(?![\w])|(?<![\w/])[A-Z]{1,2}\d\.\d{1,2}(?![\w])")
ID_RX = re.compile(r"^[A-Z0-9][A-Z0-9.\-]*[A-Z0-9]$", re.I)
NUM = r"(\d[\d,]*(?:\.\d+)?|\.\d+)"
LF_RX = re.compile(r"(?<![\w.])" + NUM + r"\s*LF\b")
SF_RX = re.compile(r"(?<![\w.])" + NUM + r"\s*SF\b")
H_FTIN_RX = re.compile(r"\bH\s+(\d+)'-(\d+(?:\.\d+)?)\"")
H_FT_RX = re.compile(r"\bH\s+" + NUM + r"\s*ft\b")
CAUSA_RX = re.compile(r"^\s*(cause|causa)\s*:", re.I)
ESCALA_RX = re.compile(r"(\d+(?:\s*-\s*|\s+)?\d*/?\d*)\s*\"\s*=\s*1\s*'\s*-?\s*0\s*\"?")
QTY_KEYS = ("length_ft", "lf", "area_sf", "sf", "qty", "l_ft")
CAUSA_KEYS = ("length_cause", "area_cause", "measure_cause", "markup_cause")


# ----------------------------------------------------------------------------------------------- utilidades
def _f(x):
    if isinstance(x, dict):
        x = x.get("value")
    try:
        v = float(str(x).replace(",", "")) if isinstance(x, str) else float(x)
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None


def _dec(s):
    s = str(s)
    return len(s.split(".")[1]) if "." in s else 0


def _tol(s):
    return max(TOL_NUM, 0.5 * 10 ** -_dec(s)) + 1e-6


def _palabras(t):
    return [w for w in re.split(r"[^A-Za-z0-9.]+", str(t or "").upper()) if w]


def _norm(t):
    return re.sub(r"\s+", " ", str(t or "")).strip().upper()


def _cargar(p):
    if isinstance(p, dict):
        return p
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def pulgadas(txt):
    """'1/4' -> 0.25; '1 1/2' / '1-1/2' -> 1.5; '3' -> 3."""
    t = txt.replace("-", " ").split()
    v = 0.0
    for p in t:
        if "/" in p:
            a, b = p.split("/", 1)
            if not a or not b or float(b) == 0:
                return None
            v += float(a) / float(b)
        elif p:
            v += float(p)
    return v or None


def escala_canon(canon, hoja):
    """-> (pt/ft, origen) de constants.plan_scale_by_sheet[hoja] o plan_scale_pt_per_ft; (None, motivo)."""
    k = (canon or {}).get("constants") or {}
    v = (k.get("plan_scale_by_sheet") or {}).get(hoja) if hoja else None
    if v is not None and _f(v):
        return _f(v), f"plan_scale_by_sheet[{hoja}]"
    v = _f(k.get("plan_scale_pt_per_ft"))
    if v:
        return v, "plan_scale_pt_per_ft"
    return None, f"sin escala en el canon para {hoja}"


def escalas_impresas(texto):
    """pt/ft de cada rótulo X" = 1'-0" del texto de la hoja."""
    out = []
    for m in ESCALA_RX.finditer(texto or ""):
        try:
            p = pulgadas(m.group(1).strip())
        except ValueError:
            p = None
        if p:
            out.append(round(72.0 * p, 4))
    return sorted(set(out))


def measure_pt_ft(doc, xref):
    """-> (pt/ft según /X /C, pt/ft según /R, texto R) del /Measure de la annot; (None, None, None) sin /Measure."""
    t, v = doc.xref_get_key(xref, "Measure")
    if t in ("null", None) or not v:
        return None, None, None
    if t == "xref":
        v = doc.xref_object(int(v.split()[0]))
    c = re.search(r"/X\s*\[\s*<<.*?/C\s+([\d.eE+-]+)", v, re.S)
    r = re.search(r"/R\s*\(([^)]*)\)", v)
    pc = 1.0 / float(c.group(1)) if c and float(c.group(1)) > 0 else None
    pr = None
    if r:
        m = re.match(r"\s*([\d\s/.-]+?)\s*in\s*=\s*([\d.]+)\s*ft", r.group(1))
        if m:
            p = pulgadas(m.group(1).strip())
            pr = 72.0 * p / float(m.group(2)) if p else None
    return pc, pr, r.group(1) if r else None


def largo(pts):
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))


def area(pts):
    q = list(pts)
    if len(q) > 2 and q[0] != q[-1]:
        q.append(q[0])
    return abs(sum(q[i][0] * q[i + 1][1] - q[i + 1][0] * q[i][1] for i in range(len(q) - 1))) / 2.0


# ----------------------------------------------------------------------------------------------- Contents
def parse_contents(subject, contents, nm):
    """-> dict {type, id, lf, lf_s, h, h_s, sf, sf_s, detail, causa, campos}."""
    campos = [c.strip() for c in str(contents or "").split("·")]
    o = {"type": str(subject or "").strip(), "campos": campos, "id": None, "detail": None, "causa": None}
    nm = str(nm or "")
    id_ultimo = False
    if nm.startswith("TO-") and not nm.startswith("TOX-"):
        o["id"] = nm[3:]
        id_ultimo = bool(campos) and campos[-1] == o["id"]
    elif nm.startswith("DEMO-"):
        o["id"] = nm[5:]
    if not o["id"] and campos and ID_RX.match(campos[-1]) and re.search(r"[\d-]", campos[-1]):
        o["id"], id_ultimo = campos[-1], True
    det = campos[:-1] if id_ultimo else campos
    resto = [c for c in det[1:] if not CAUSA_RX.match(c)]
    o["detail"] = resto[-1] if resto else None
    for c in campos:
        if CAUSA_RX.match(c):
            o["causa"] = c
    m = LF_RX.search(contents or "")
    o["lf_s"] = m.group(1).replace(",", "") if m else None
    ms = SF_RX.findall(contents or "")
    o["sf_s"] = ms[-1].replace(",", "") if ms else None
    m = H_FTIN_RX.search(contents or "")
    if m:
        o["h"], o["h_s"] = int(m.group(1)) + float(m.group(2)) / 12.0, m.group(0)
    else:
        m = H_FT_RX.search(contents or "")
        o["h"], o["h_s"] = (_f(m.group(1)), m.group(0)) if m else (None, None)
    o["h_pending"] = bool(re.search(r"\bH\s+PENDING\b", contents or ""))
    o["lf"], o["sf"] = _f(o["lf_s"]), _f(o["sf_s"])
    return o


def citas(t):
    t = str(t or "")
    out = set(NHOJA_RX.findall(t))
    sin_n = NHOJA_RX.sub(" ", t)
    out |= set(HOJA_RX.findall(sin_n))
    return out


# ----------------------------------------------------------------------------------------------- Excel
def leer_excel(xlsx):
    """-> {"pt": {wall_id: {...}}, "ms": [{material, unit, where, texto}], "errores": [...]}."""
    import openpyxl
    wb = openpyxl.load_workbook(xlsx, data_only=True, read_only=True)
    out = {"pt": {}, "ms": [], "errores": []}
    if "Partition Takeoff" not in wb.sheetnames:
        out["errores"].append("el Excel no tiene la hoja Partition Takeoff")
    else:
        ws = wb["Partition Takeoff"]
        rows = list(ws.iter_rows(values_only=True))
        hr, col = None, None
        for i, r in enumerate(rows[:12]):
            vals = [str(v or "").strip() for v in r]
            if "Wall #" in vals:
                hr, col = i, {v: j for j, v in enumerate(vals) if v}
        if hr is None:
            out["errores"].append("Partition Takeoff sin encabezado 'Wall #'")
        else:
            def c(*ns):
                for n in ns:
                    for k, j in col.items():
                        if k.lower().startswith(n.lower()):
                            return j
                return None
            jw, jl, jh, jsf = c("Wall #"), c("Length"), c("Height"), c("Wall Area", "Wall SF", "Area (SF)", "Board (SF)")
            grupo = ""
            for i, r in enumerate(rows[hr + 1:], start=hr + 2):
                a = str(r[0] or "").strip()
                w = str(r[jw] or "").strip() if jw is not None else ""
                if a.upper().startswith("TYPE ") and not w:
                    grupo = a
                    continue
                if not w or w.upper().startswith(("SUBTOTAL", "TOTAL")):
                    continue
                out["pt"].setdefault(w, []).append({
                    "fila": i, "lf": _f(r[jl]) if jl is not None else None, "h": _f(r[jh]) if jh is not None else None,
                    "sf": _f(r[jsf]) if jsf is not None else None, "grupo": grupo, "a": a,
                    "sf_col": list(col)[[*col.values()].index(jsf)] if jsf is not None else None,
                    "texto": " | ".join(str(v) for v in r if v is not None)})
    if "Material Summary" in wb.sheetnames:
        ws = wb["Material Summary"]
        rows = list(ws.iter_rows(values_only=True))
        hr, col = None, None
        for i, r in enumerate(rows[:12]):
            vals = [str(v or "").strip() for v in r]
            if "Material" in vals and "Where it comes from" in vals:
                hr, col = i, {v: j for j, v in enumerate(vals) if v}
        if hr is not None:
            for i, r in enumerate(rows[hr + 1:], start=hr + 2):
                mat = str(r[col["Material"]] or "").strip()
                if not mat:
                    continue
                out["ms"].append({"fila": i, "material": mat, "unit": str(r[col.get("Unit", 1)] or "").strip().upper(),
                                  "where": str(r[col["Where it comes from"]] or "")})
    wb.close()
    # BE-117g (Chuze FINAL4): renglón unido "A+B" (PT2: wall + return / partes con '+') -> cada pieza apunta a su renglón
    out["union"] = {}
    for w in list(out["pt"]):
        if "+" in w:
            for m in (x.strip() for x in w.split("+")):
                if m and m not in out["pt"]:
                    out["union"][m] = w
    return out


def buscar_ms(ex, wid):
    """Valor 'ID valor' del desglose de Material Summary. -> [(renglón, valor)]."""
    rx = re.compile(r"(?<![\w.\-])" + re.escape(wid) + r"\s*:?\s+(-?\d[\d,]*(?:\.\d+)?)(?![\w/])")
    out = []
    for m in ex["ms"]:
        h = rx.search(m["where"])
        if h:
            out.append((m, _f(h.group(1))))
    return out


def tipo_ok(tipo, texto):
    toks = _palabras(texto)
    for w in _palabras(tipo):
        if len(w) < 3 and not re.search(r"\d", w):
            continue
        if not any(t.startswith(w) for t in toks):
            return False
    return True


# ----------------------------------------------------------------------------------------------- canon
def indice_canon(canon):
    """-> ({id: elemento}, {hoja: [ids]}, ids con geometría que se marcan)."""
    idx, hojas, geo = {}, {}, []
    for k, v in canon.items():
        if not isinstance(v, list):
            continue
        for e in v:
            if not isinstance(e, dict):
                continue
            eid = e.get("id") or e.get("ref")
            if eid:
                idx.setdefault(str(eid), e)
            hoja = (e.get("band") or {}).get("sheet") if isinstance(e.get("band"), dict) else None
            hoja = hoja or e.get("sheet")
            if hoja and any(_f(e.get(q)) for q in QTY_KEYS) and str(e.get("status") or "").upper() != "EXCLUDED":
                hojas.setdefault(str(hoja), []).append(str(eid or k))
            if k in ("walls", "existing_walls", "demo_geom") and eid:
                geo.append(str(eid))
    return idx, hojas, geo


# ----------------------------------------------------------------------------------------------- PDF
def leer_annots(pdf):
    import pymupdf as fitz
    doc = fitz.open(pdf)
    out, textos = [], {}
    for i in range(doc.page_count):
        pg = doc[i]
        for a in pg.annots() or []:
            info = a.info or {}
            nm = info.get("id") or ""
            autor = str(info.get("title") or "").strip().lower()
            if nm.startswith(NM_LEY) or not (autor in AUTORES or nm.startswith(("TO-", "TOX-", "DEMO-"))):
                continue
            if i not in textos:
                textos[i] = pg.get_text("text")
            if "TAKE-OFF MARKUPS - LEGEND" in textos[i]:
                continue
            pc, pr, rtxt = measure_pt_ft(doc, a.xref)
            t, dv = doc.xref_get_key(a.xref, "Depth")
            out.append({"page": i, "label": pg.get_label() or "", "tipo_pdf": a.type[1], "nm": nm,
                        "subject": info.get("subject") or "", "contents": info.get("content") or "",
                        "verts": [tuple(v) for v in (a.vertices or [])], "measure_c": pc, "measure_r": pr,
                        "measure_txt": rtxt, "depth": _f(dv) if t not in ("null", None) else None})
    imp = {i: escalas_impresas(t) for i, t in textos.items()}
    doc.close()
    return out, imp


# ----------------------------------------------------------------------------------------------- verificación
def verificar(pdf, xlsx, canon_p):
    """-> (fallas [str], líneas del reporte [str], resumen dict)."""
    fallas, lineas = [], []
    for p, n in ((pdf, "PDF de markups"), (xlsx, "Excel"), (canon_p, "canon")):
        if not isinstance(p, dict) and (not p or not os.path.isfile(p)):
            return [f"no existe el {n} {p}"], [], {"annots": 0, "fallas": 1}
    canon = _cargar(canon_p)
    ex = leer_excel(xlsx)
    fallas += [f"Excel: {e}" for e in ex["errores"]]
    idx, hojas_canon, ids_geo = indice_canon(canon)
    ans, imp = leer_annots(pdf)
    # agrupación por id base (p.ej. 'DEMO-14 EX-RRM-01-CB' -> 'DEMO-14' cuando el Excel trae el total del grupo)
    vistos_id, grupos = {}, {}
    uniones = {}   # BE-117g: renglones unidos "A+B" del Partition Takeoff
    hojas_mk = {}
    for a in ans:
        a["p"] = parse_contents(a["subject"], a["contents"], a["nm"])
        hoja = a["label"] or ""
        hojas_mk.setdefault(hoja, 0)
        hojas_mk[hoja] += 1
    for a in ans:
        P = a["p"]
        prob = []
        wid = P["id"]
        hoja = a["label"]
        tag = f"p.{a['page'] + 1} {hoja or '?'} {wid or a['nm'] or '(sin /NM)'}"
        # ---- (a) Contents vs Excel
        if P["campos"] and not _norm(P["campos"][0]).startswith(_norm(P["type"])):
            prob.append(f"Contents TYPE '{P['campos'][0]}' != Subject '{P['type']}'")
        if not wid:
            prob.append("sin Wall ID en el Contents / NM (no se puede cuadrar con el Excel)")
        if P["h_pending"]:
            prob.append("H PENDING en el Contents (no terminado)")
        if P["lf"] is None and P["sf"] is None:
            prob.append("Contents sin LF ni SF")
        if not P["detail"] or not citas(P["detail"]):
            prob.append(f"DETAIL sin N/HOJA ('{P['detail']}')")
        if P["h"] is not None and a["depth"] is not None and abs(P["h"] - a["depth"]) > TOL_H:
            prob.append(f"Depth {a['depth']} != H {P['h']:.3f}")
        fila = None
        if wid:
            vistos_id.setdefault(wid, []).append(a)
            pt = ex["pt"].get(wid)
            union = ex.get("union", {}).get(wid)
            if not pt and union:
                # pieza de un renglón unido: TYPE y H por pieza; LF / SF se suman y se cuadran al final contra el renglón
                fila = ex["pt"][union][0]
                if not tipo_ok(P["type"], fila["grupo"] + " " + fila["a"]):
                    prob.append(f"TYPE '{P['type']}' != grupo '{fila['grupo']}' / '{fila['a'][:40]}'")
                if P["h"] is not None and (fila["h"] is None or abs(P["h"] - fila["h"]) > TOL_H):
                    prob.append(f"H {P['h_s']} != Excel {fila['h']}")
                suma = uniones.setdefault(union, {"lf": 0.0, "sf": 0.0, "n": 0, "fila": fila})
                suma["lf"] += P["lf"] or 0.0
                suma["sf"] += P["sf"] or 0.0
                suma["n"] += 1
                vistos_id.setdefault(union, []).append(a)
                fila_txt = f"PT fila {fila['fila']} (parte de {union})"
            elif pt:
                if len(pt) > 1:
                    prob.append(f"Wall # {wid} en {len(pt)} renglones del Partition Takeoff")
                fila = pt[0]
                if not tipo_ok(P["type"], fila["grupo"] + " " + fila["a"]):
                    prob.append(f"TYPE '{P['type']}' != grupo '{fila['grupo']}' / '{fila['a'][:40]}'")
                if P["lf"] is not None and (fila["lf"] is None or abs(P["lf"] - fila["lf"]) > _tol(P["lf_s"])):
                    prob.append(f"LF {P['lf_s']} != Excel {fila['lf']}")
                if P["h"] is not None and (fila["h"] is None or abs(P["h"] - fila["h"]) > TOL_H):
                    prob.append(f"H {P['h_s']} != Excel {fila['h']}")
                if P["sf"] is not None and (fila["sf"] is None or abs(P["sf"] - fila["sf"]) > _tol(P["sf_s"])):
                    prob.append(f"SF {P['sf_s']} != Excel {fila['sf_col']} {fila['sf']}")
                falt = sorted(c for c in citas(P["detail"]) if c not in fila["texto"])
                if falt:
                    prob.append(f"DETAIL {', '.join(falt)} no está en el renglón del Excel (fila {fila['fila']})")
                fila_txt = f"PT fila {fila['fila']}"
            else:
                ms = buscar_ms(ex, wid)
                base = wid.split()[0]
                agrupado = False
                if not ms and base != wid:
                    ms, agrupado = buscar_ms(ex, base), True
                if not ms:
                    prob.append(f"Wall ID {wid} no está en el Excel (Partition Takeoff 'Wall #' ni desglose de "
                                f"Material Summary)")
                    fila_txt = "sin renglón"
                else:
                    m, val = ms[0]
                    fila_txt = f"MS fila {m['fila']}"
                    if not tipo_ok(P["type"], m["material"]):
                        prob.append(f"TYPE '{P['type']}' != renglón '{m['material'][:50]}'")
                    falt = sorted(c for c in citas(P["detail"]) if c not in m["where"])
                    if falt:
                        prob.append(f"DETAIL {', '.join(falt)} no está en el renglón del Excel ({fila_txt})")
                    if agrupado:
                        grupos.setdefault((base, m["fila"], m["unit"], val), []).append(a)
                    else:
                        mine = P["sf"] if m["unit"] == "SF" else P["lf"] if m["unit"] == "LF" else None
                        s = P["sf_s"] if m["unit"] == "SF" else P["lf_s"]
                        if mine is None:
                            prob.append(f"Contents sin {m['unit']} para comparar con el Excel ({val})")
                        elif val is None or abs(mine - val) > _tol(s):
                            prob.append(f"{m['unit']} {s} != Excel {val} ({fila_txt})")
        else:
            fila_txt = "sin renglón"
        # ---- (b) escala
        esc, origen = escala_canon(canon, hoja)
        if not esc:
            prob.append(origen)
        else:
            if a["measure_c"] is None:
                prob.append("sin /Measure (Bluebeam no mide a escala)")
            else:
                if abs(a["measure_c"] / esc - 1) > TOL_REL:
                    prob.append(f"/Measure {a['measure_c']:.3f} pt/ft != escala de la hoja {esc} pt/ft ({origen})")
                if a["measure_r"] is not None and abs(a["measure_r"] / esc - 1) > TOL_REL:
                    prob.append(f"/Measure R '{a['measure_txt']}' != escala de la hoja {esc} pt/ft")
            im = imp.get(a["page"]) or []
            if im and not any(abs(x / esc - 1) <= TOL_REL for x in im):
                prob.append(f"escala del canon {esc} pt/ft no es ningún rótulo SCALE impreso en {hoja} ({im})")
        # ---- (c) largo / área medidos
        med = ""
        el = idx.get(wid or "") or idx.get((wid or "").split(" ")[0]) or {}
        causa = next((str(el[k]) for k in CAUSA_KEYS if el.get(k)), None) or P["causa"]
        vs = a["verts"]
        if esc and len(vs) >= 2:
            cerrado = a["tipo_pdf"] == "Polygon" or (len(vs) > 3 and math.dist(vs[0], vs[-1]) < 0.5)
            if P["lf"]:
                lg = (largo(vs) + (math.dist(vs[-1], vs[0]) if a["tipo_pdf"] == "Polygon" else 0)) / esc
                d = lg / P["lf"] - 1
                med = f"Length {lg:.2f} vs LF {P['lf_s']} ({d * 100:+.2f} %)"
                if abs(d) > TOL_REL and not causa:
                    prob.append(f"Length {lg:.2f} ft vs LF {P['lf_s']} = {d * 100:+.2f} % (> 0.5 %, sin causa escrita)")
            elif cerrado and P["sf"] and P["h"] is None:
                ar = area(vs) / esc ** 2
                d = ar / P["sf"] - 1
                med = f"Area {ar:.2f} vs SF {P['sf_s']} ({d * 100:+.2f} %)"
                if abs(d) > TOL_REL and not causa:
                    prob.append(f"Area {ar:.2f} SF vs SF {P['sf_s']} = {d * 100:+.2f} % (> 0.5 %, sin causa escrita)")
            if causa and med:
                med += f" · causa: {causa[:60]}"
        elif len(vs) < 2:
            prob.append("annot sin vértices")
        a["prob"] = prob
        a["linea"] = (f"{'FAIL' if prob else 'OK  '} | {tag} | {P['type']} | LF {P['lf_s']} H {P['h_s']} SF {P['sf_s']} | "
                      f"{fila_txt} | /Measure {a['measure_txt']} | {med}" + (" | " + "; ".join(prob) if prob else ""))
    # grupos (id base con total en el Excel)
    for (base, fila, unit, val), lst in grupos.items():
        tot = sum((x["p"]["sf"] if unit == "SF" else x["p"]["lf"]) or 0 for x in lst)
        if val is None or abs(tot - val) > TOL_NUM * max(1, len(lst)) + 1e-6:
            msg = f"grupo {base}: suma de {len(lst)} annots {tot:.2f} {unit} != Excel {val} (MS fila {fila})"
            for x in lst:
                x["prob"].append(msg)
                x["linea"] = x["linea"].replace("OK   |", "FAIL |", 1) + " | " + msg
    for a in ans:
        if a["prob"]:
            fallas.append(f"{a['nm'] or a['p']['id'] or '?'} (p.{a['page'] + 1} {a['label']}): " + "; ".join(a["prob"]))
        lineas.append(a["linea"])
    # duplicados
    for wid, lst in vistos_id.items():
        if len(lst) > 1 and wid not in uniones:   # BE-117g: las piezas de un renglón "A+B" son varias a propósito
            fallas.append(f"{wid}: {len(lst)} anotaciones con el mismo Wall ID")
    # ---- (d) hojas y elementos sin markups
    for hoja, ids in sorted(hojas_canon.items()):
        if not hojas_mk.get(hoja):
            fallas.append(f"hoja {hoja}: {len(ids)} elemento(s) del take-off en el canon ({', '.join(ids[:6])}) y "
                          f"ningún markup en el PDF")
    for eid in ids_geo:
        if eid not in vistos_id:
            fallas.append(f"{eid}: elemento del canon sin anotación en el PDF de markups")
    for k, g in uniones.items():
        if True:
            fl = g["fila"]
            if fl["lf"] is not None and abs(g["lf"] - fl["lf"]) > max(0.02, 0.005 * fl["lf"]):
                fallas.append(f"{k}: suma LF de las piezas {g['lf']:.2f} != Excel {fl['lf']} (fila {fl['fila']})")
            if fl["sf"] is not None and g["sf"] and abs(g["sf"] - fl["sf"]) > max(0.2, 0.005 * fl["sf"]):
                fallas.append(f"{k}: suma SF de las piezas {g['sf']:.1f} != Excel {fl['sf']} (fila {fl['fila']})")
    for wid in ex["pt"]:
        if wid not in vistos_id:
            fallas.append(f"{wid}: renglón 'Wall #' del Partition Takeoff sin anotación en el PDF de markups")
    res = {"annots": len(ans), "ok": sum(1 for a in ans if not a["prob"]), "fail": sum(1 for a in ans if a["prob"]),
           "hojas_markups": {k: v for k, v in sorted(hojas_mk.items())}, "hojas_canon": sorted(hojas_canon),
           "fallas": len(fallas)}
    return fallas, lineas, res


def reporte(pdf, xlsx, canon_p, fallas, lineas, res):
    out = [f"# Markups vs Excel (R80f.7 / BE-117) — {'OK' if not fallas else 'FALLA'}", "",
           f"- PDF: `{pdf}`", f"- Excel: `{xlsx}`", f"- canon: `{canon_p}`",
           f"- anotaciones: {res['annots']} · OK {res['ok']} · FAIL {res['fail']} · fallas totales {len(fallas)}",
           f"- markups por hoja: {res['hojas_markups']} · hojas con elementos en el canon: {res['hojas_canon']}", "",
           "## Una línea por anotación", ""] + [f"- {x}" for x in lineas] + ["", "## Fallas", ""] + \
          ([f"- {x}" for x in fallas] or ["- ninguna"])
    return "\n".join(out) + "\n"


def buscar_pdf(d, canon_p=None, excel=None):
    """PDF de markups de ENTREGA: $TAKEOFF_MARKUPS_PDF; si no, *markup*.pdf junto al Excel; si no, el *.pdf más
    reciente de 6_markups/ (carpeta de trabajo, etapas/, junto al canon). None si no hay."""
    e = os.environ.get("TAKEOFF_MARKUPS_PDF")
    if e and os.path.isfile(e):
        return os.path.abspath(e)
    cands = []
    if excel:
        cands = glob.glob(os.path.join(os.path.dirname(os.path.abspath(excel)), "*markup*.pdf"))
    if not cands:
        dirs = [os.path.join(d, "6_markups"), os.path.join(d, "etapas", "6_markups")]
        if canon_p:
            dirs.append(os.path.join(os.path.dirname(canon_p), "..", "6_markups"))
        for x in dirs:
            cands += glob.glob(os.path.join(x, "*.pdf"))
    cands = sorted({os.path.abspath(c) for c in cands}, key=lambda p: (os.path.getmtime(p), p))
    return cands[-1] if cands else None


def main(argv):
    args = [a for a in argv[1:]]
    out = None
    if "--out" in args:
        i = args.index("--out")
        out = args[i + 1]
        del args[i:i + 2]
    if len(args) != 3:
        print(__doc__)
        return 2
    pdf, xlsx, canon_p = args
    fallas, lineas, res = verificar(pdf, xlsx, canon_p)
    if out:
        with open(out, "w", encoding="utf-8") as f:
            f.write(reporte(pdf, xlsx, canon_p, fallas, lineas, res))
    print(json.dumps(res, ensure_ascii=False))
    for x in fallas:
        print("FALLA:", x)
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
