#!/usr/bin/env python3
"""inventario.py — ETAPA 1 del take-off: inventario por SCRIPT de lo que el plano dice (no de lo que el ojo cree ver).

Por qué existe: en pruebas ciegas la misma versión del skill dio walls por tag distintos entre corridas (un type con
4 walls contra 8, otro con 12 contra 9). El conteo de tags lo hacía el modelo a ojo. Aquí sale del texto del PDF.

GENÉRICO: ningún tag, hoja, coordenada ni nombre de proyecto vive en este archivo. Todo sale del PDF recibido.

Qué hace
  1. Índice de hojas: número y título de cada página desde el title block (número = token con forma de sheet number
     de mayor tamaño en el cuadrante inferior derecho; título = renglones de mayor tamaño de la columna del title
     block que NO se repiten en la mayoría de las hojas — así se descarta el nombre del proyecto).
  2. Hojas raster (sin texto) -> "NO INVENTARIABLE POR SCRIPT" (no se adivina nada de ellas).
  3. Types del schedule / leyenda de partition types:
       a) títulos de detalle "PARTITION [TYPE] X, Y & Z" / "WALL TYPE X" (todos los tokens deben tener forma de tag)
       b) en las hojas de schedule (título con PARTITION / WALL TYPE), columnas de tokens con forma de tag
          (>= 2 alineados en x, al menos uno con dígito).
  4. Ocurrencias de texto, con hoja, página, bbox (pt, página ROTADA = como se ve el PNG) y texto exacto:
       partition_tag (types del schedule dentro de un símbolo cerrado en hoja de planta),
       partition_ambiguo (type del schedule que no pasa los filtros: sin símbolo, tamaño de grid, hoja sin referencia),
       partition_candidato (forma de tag letra+dígito dentro de símbolo, que NO está en el schedule),
       door_window_tag, detail_bubble (N/HOJA apilado), detail_ref_text (N/HOJA en una línea), keynote, cota.
  5. Por cada type: conteo por hoja y total; un PNG recortado por ocurrencia con la marca circulada. Cada PNG se
     REABRE y se verifica: anillo rojo donde debe y tinta del tag en el centro, y el texto bajo la marca = el tag.

Símbolo cerrado = 8 rayos desde el centro del token chocan con trazos del dibujo dentro de un radio corto.
Single-letter types (B, G, F...) se confunden con grid bubbles: solo cuentan si el tamaño de letra y el radio del
símbolo coinciden (±15 % / ±40 %) con los de los types de varios caracteres de ESA hoja. Si no hay referencia en la
hoja, van a partition_ambiguo con su motivo (nunca se cuentan en silencio).

Uso:  python3 inventario.py <pdf> <out_dir> [--dpi 150] [--sin-recortes]
Salida: <out_dir>/inventario.json, <out_dir>/inventario.md, <out_dir>/recortes/*.png
"""
import hashlib
import json
import math
import os
import re
import sys
from collections import Counter, OrderedDict, defaultdict

import numpy as np
import pymupdf as fitz

SHEET_RE = re.compile(r"^[A-Z]{1,3}-?\d{1,3}(?:[.\-]\d{1,3}[A-Z]?)?$")
TAG_DIGIT_RE = re.compile(r"^[A-Z]{1,2}\d{1,2}[A-Z]{0,2}$")
TYPE_RE = re.compile(r"^(?:[A-Z]{1,2}\d{1,2}[A-Z]{0,2}|[A-Z]{1,2})$")   # token de partition type (p. ej. X1, X1K, Q)
DOOR_RE = re.compile(r"^[A-Z]?\d{2,4}[A-Z]?(?:-\d)?$")
WINDOW_RE = re.compile(r"^[A-Z]{1,3}-\d{1,3}[A-Z]?$")
BUBBLE_ID_RE = re.compile(r"^(?:\d{1,2}[A-Z]?|[A-Z]{1,2}\d?)$")
KEYNOTE_RE = re.compile(r"^\d{1,2}[A-Z]?$")
DETAIL_TXT_RE = re.compile(r"(?<![\w/])(\d{1,2}[A-Z]?|[A-Z]{1,2}\d?)\s*/\s*([A-Z]{1,3}-?\d{1,3}(?:[.\-]\d{1,3}[A-Z]?)?)(?![\w.])")
DIM_RE = re.compile(r"\d+\s*'\s*-?\s*\d+(?:\s+\d+/\d+)?(?:\s*\d+/\d+)?\s*\"|\d+\s*'(?!\s*-?\s*\d)|"
                    r"(?<![\d/'])\d+(?:\s+\d+/\d+|-\d+/\d+)?\s*\"|(?<![\d/])\d+/\d+\s*\"")
TITLE_SKIP_RE = re.compile(r"\d+\s*\"?\s*=\s*\d|SCALE|N\.?T\.?S\.?$|\d{1,2}/\d{1,2}/\d{2,4}|^\d+$|^[-–:\s]*$")
SCHED_TITLE_RE = re.compile(r"\b(PARTITION|WALL)\s*(TYPES?|SCHEDULE|LEGEND)\b|\bPARTITIONS\b")
DETAIL_TYPE_TITLE_RE = re.compile(r"^\s*(?:PARTITION|WALL)\s+(?:TYPES?\s+)?(.+?)\s*$")
PLAN_TITLE_RE = re.compile(r"\bPLANS?\b")
STOP = {"AND", "OR", "THE", "OF", "TO", "AT", "AS", "ON", "IN", "BY", "SEE", "TYP", "NTS", "SIM", "EQ", "UNO", "NO",
        "YES", "FOR", "ALL", "MAX", "MIN", "TOP", "BE", "IF", "IS", "UP", "DN", "NEW", "END", "PER", "TBD"}
PUNCT = ".,;:()[]{}\"'"


# ----------------------------------------------------------------------------------------------- lectura de página
def palabras(page):
    """Palabras con bbox en coordenadas de la página ROTADA (display), tamaño de letra y línea."""
    m = page.rotation_matrix
    out = []
    raw = page.get_text("rawdict")
    for bi, b in enumerate(raw.get("blocks", [])):
        for li, l in enumerate(b.get("lines", [])):
            for s in l.get("spans", []):
                cur, box = [], None
                for ch in s.get("chars", []) + [None]:
                    c = None if ch is None else ch["c"]
                    if c is None or c.isspace():
                        if cur:
                            r = box * m
                            out.append({"t": "".join(cur), "r": r, "size": s["size"], "line": (bi, li)})
                        cur, box = [], None
                        continue
                    cur.append(c)
                    rb = fitz.Rect(ch["bbox"])
                    box = rb if box is None else box | rb
    return out


def lineas(page):
    """Renglones (texto unido) con bbox display y tamaño máximo."""
    m = page.rotation_matrix
    out = []
    for b in page.get_text("dict").get("blocks", []):
        for l in b.get("lines", []):
            t = "".join(s["text"] for s in l["spans"])
            if t.strip():
                out.append({"t": t.strip(), "r": fitz.Rect(l["bbox"]) * m,
                            "size": max(s["size"] for s in l["spans"])})
    return out


def segmentos(page):
    """Trazos del dibujo como segmentos (x1, y1, x2, y2) en coordenadas display (transformación vectorizada)."""
    pa, pb = [], []
    for d in page.get_drawings():
        for it in d.get("items", []):
            k = it[0]
            if k == "l":
                pts = [(it[1].x, it[1].y), (it[2].x, it[2].y)]
            elif k == "re":
                r = it[1]
                pts = [(r.x0, r.y0), (r.x1, r.y0), (r.x1, r.y1), (r.x0, r.y1), (r.x0, r.y0)]
            elif k == "qu":
                q = it[1]
                pts = [(q.ul.x, q.ul.y), (q.ur.x, q.ur.y), (q.lr.x, q.lr.y), (q.ll.x, q.ll.y), (q.ul.x, q.ul.y)]
            elif k == "c":
                p0, p1, p2, p3 = it[1], it[2], it[3], it[4]
                pts = []
                for i in range(7):
                    u = i / 6.0
                    a, b_, c, e = (1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u ** 3
                    pts.append((a * p0.x + b_ * p1.x + c * p2.x + e * p3.x, a * p0.y + b_ * p1.y + c * p2.y + e * p3.y))
            else:
                continue
            pa.extend(pts[:-1])
            pb.extend(pts[1:])
    if not pa:
        return np.zeros((0, 4))
    m = page.rotation_matrix
    A, B = np.array(pa, dtype=float), np.array(pb, dtype=float)

    def tr(P):
        return np.stack([P[:, 0] * m.a + P[:, 1] * m.c + m.e, P[:, 0] * m.b + P[:, 1] * m.d + m.f], axis=1)
    return np.hstack([tr(A), tr(B)])


class Trazos:
    """Segmentos de una página en arrays numpy, para lanzar rayos rápido."""

    def __init__(self, segs):
        a = np.asarray(segs, dtype=float).reshape(-1, 4)
        self.x1, self.y1, self.x2, self.y2 = a[:, 0], a[:, 1], a[:, 2], a[:, 3]
        self.xmin, self.xmax = np.minimum(self.x1, self.x2), np.maximum(self.x1, self.x2)
        self.ymin, self.ymax = np.minimum(self.y1, self.y2), np.maximum(self.y1, self.y2)

    def cerca(self, cx, cy, rad):
        m = (self.xmax >= cx - rad) & (self.xmin <= cx + rad) & (self.ymax >= cy - rad) & (self.ymin <= cy + rad)
        return self.x1[m], self.y1[m], self.x2[m], self.y2[m]


def simbolo(trazos, r, size):
    """¿El token está dentro de un símbolo cerrado? 8 rayos desde el centro; devuelve dict o None."""
    cx, cy = (r.x0 + r.x1) / 2.0, (r.y0 + r.y1) / 2.0
    half = max(r.width, r.height) / 2.0
    dmax = half * 1.6 + size * 1.4
    x1, y1, x2, y2 = trazos.cerca(cx, cy, dmax)
    if not len(x1):
        return None
    ex, ey, px, py = x2 - x1, y2 - y1, x1 - cx, y1 - cy
    tmin = 0.25 * min(r.width, r.height)
    hits = []
    with np.errstate(divide="ignore", invalid="ignore"):
        for k in range(8):
            a = k * math.pi / 4.0
            dx, dy = math.cos(a), math.sin(a)
            den = dx * ey - dy * ex
            t = (px * ey - py * ex) / den
            s = (px * dy - py * dx) / den
            ok = (np.abs(den) > 1e-9) & (t > tmin) & (t <= dmax) & (s >= -1e-6) & (s <= 1 + 1e-6)
            if not ok.any():
                return None
            hits.append(float(t[ok].min()))
    orto = (hits[0] + hits[2] + hits[4] + hits[6]) / 4.0
    diag = (hits[1] + hits[3] + hits[5] + hits[7]) / 4.0
    ratio = diag / orto if orto else 0
    forma = "rect" if ratio > 1.2 else ("circle" if ratio > 0.85 else "diamond/hex")
    return {"radio": round(sum(hits) / 8.0, 2), "forma_aprox": forma}


# ------------------------------------------------------------------------------------------------ índice de hojas
def _numero_hoja(ws, W, H):
    c = [w for w in ws if SHEET_RE.match(w["t"].strip(PUNCT)) and w["r"].x0 > W * 0.7 and w["r"].y0 > H * 0.55]
    if not c:
        return None
    c.sort(key=lambda w: (-round(w["size"], 1), -w["r"].y1))
    return c[0]


def indice_hojas(doc, cache):
    hojas = []
    regiones = {}
    for i, page in enumerate(doc):
        W, H = page.rect.width, page.rect.height
        ws, ls = cache[i]["words"], cache[i]["lines"]
        num = _numero_hoja(ws, W, H)
        texto = sum(len(w["t"]) for w in ws)
        h = {"page": i + 1, "sheet": num["t"].strip(PUNCT) if num else None, "title": None,
             "rotation": page.rotation, "width_pt": round(W, 2), "height_pt": round(H, 2),
             "text_chars": texto, "images": len(page.get_images()), "inventariable": True, "motivo": ""}
        if texto < 20:
            h["inventariable"] = False
            h["motivo"] = ("NO INVENTARIABLE POR SCRIPT: página sin texto extraíble (raster / escaneada"
                           + (f", {h['images']} imagen(es)" if h["images"] else "") + ")")
        elif num is None:
            h["motivo"] = "sheet number NO IDENTIFICADO en el title block (puede estar vectorizado)"
        if num is not None:
            x_lim = num["r"].x0 - 0.08 * W
            regiones[i] = [l for l in ls if l["r"].x0 >= x_lim and l["r"].y0 >= H * 0.45]
        hojas.append(h)
    rep = Counter()
    for i, reg in regiones.items():
        for t in {re.sub(r"\s+", " ", l["t"]).upper() for l in reg}:
            rep[t] += 1
    n = max(1, len(regiones))
    lim = max(3, 0.25 * n)
    for i, reg in regiones.items():
        h = hojas[i]
        cand = [l for l in reg if rep[re.sub(r"\s+", " ", l["t"]).upper()] <= lim
                and not TITLE_SKIP_RE.search(l["t"]) and l["t"].strip(PUNCT) != h["sheet"]
                and not SHEET_RE.match(l["t"].strip(PUNCT))]
        if not cand:
            h["title"] = None
            continue
        smax = max(l["size"] for l in cand)
        sel = [l for l in cand if abs(l["size"] - smax) < 0.6]
        sel.sort(key=lambda l: (round(l["r"].y0), l["r"].x0))
        bloque = [sel[0]]
        for l in sel[1:]:       # renglones consecutivos del mismo título
            if l["r"].y0 - bloque[-1]["r"].y1 < 2.5 * l["size"] and abs(l["r"].x0 - bloque[0]["r"].x0) < 6 * l["size"]:
                bloque.append(l)
        h["title"] = " ".join(l["t"] for l in bloque)
    cnt = Counter(h["sheet"] for h in hojas if h["sheet"])
    for h in hojas:
        if h["sheet"] and cnt[h["sheet"]] > 1:
            h["motivo"] = (h["motivo"] + "; " if h["motivo"] else "") + \
                f"sheet number repetido en {cnt[h['sheet']]} páginas (se cita con página)"
        h["es_schedule_partition"] = bool(h["title"] and SCHED_TITLE_RE.search(h["title"].upper()))
        h["titulo_planta"] = bool(h["title"] and PLAN_TITLE_RE.search(h["title"].upper()))
    return hojas


# ---------------------------------------------------------------------------------------------- types del schedule
def _tokens_titulo(resto):
    toks = [t for t in re.split(r"\s*(?:,|&|/|\+|\bAND\b)\s*|\s+", resto.upper()) if t]
    if toks and all(TYPE_RE.match(t) and t not in STOP for t in toks):
        return toks
    return None


def types_schedule(hojas, cache):
    tipos = OrderedDict()

    def add(t, h, via):
        tipos.setdefault(t, {"type": t, "fuentes": []})
        f = f"{h['sheet'] or '?'} (p.{h['page']}) {via}"
        if f not in tipos[t]["fuentes"]:
            tipos[t]["fuentes"].append(f)

    for h in hojas:
        i = h["page"] - 1
        for l in cache[i]["lines"]:
            m = DETAIL_TYPE_TITLE_RE.match(l["t"].upper())
            if m:
                toks = _tokens_titulo(m.group(1))
                if toks:
                    for t in toks:
                        add(t, h, f"título de detalle '{l['t']}'")
        if not h.get("es_schedule_partition"):
            continue
        ws = [w for w in cache[i]["words"] if TYPE_RE.match(w["t"]) and w["t"] not in STOP]
        # columnas: tokens con forma de tag alineados en x (±4 pt) y seguidos en y (paso <= 3 tamaños)
        ws.sort(key=lambda w: (w["r"].x0, w["r"].y0))
        usados = set()
        for a in range(len(ws)):
            if a in usados:
                continue
            col = [a]
            for b in range(len(ws)):
                if b == a or b in usados or b in col:
                    continue
                wb, wl = ws[b], ws[col[-1]]
                if abs(wb["r"].x0 - ws[a]["r"].x0) <= 4 and 0 < wb["r"].y0 - wl["r"].y0 <= 3 * wl["size"] \
                        and abs(wb["size"] - wl["size"]) < 0.5:
                    col.append(b)
            if len(col) >= 2 and any(TAG_DIGIT_RE.match(ws[k]["t"]) for k in col):
                for k in col:
                    usados.add(k)
                    add(ws[k]["t"], h, "columna del schedule")
    return list(tipos.values())


# -------------------------------------------------------------------------------------------------- ocurrencias
def _firma(t):
    """Forma de un sheet number: Z09.01 y Z9.01 -> 'L9.9'; EQ-2 -> 'L-9' (para no tomar equipos por hojas)."""
    return re.sub(r"[A-Z]+", "L", re.sub(r"\d+", "9", t))


def _occ(kind, w, h, extra=None):
    r = w["r"]
    o = {"kind": kind, "text": w["t"], "page": h["page"], "sheet": h["sheet"],
         "bbox_pt": [round(r.x0, 2), round(r.y0, 2), round(r.x1, 2), round(r.y1, 2)],
         "center_pt": [round((r.x0 + r.x1) / 2, 2), round((r.y0 + r.y1) / 2, 2)], "size": round(w["size"], 2)}
    if extra:
        o.update(extra)
    return o


def ocurrencias(doc, hojas, cache, tipos):
    T = {t["type"] for t in tipos}
    out = defaultdict(list)
    puertas_sched = set()
    for h in hojas:
        if h["title"] and re.search(r"\bDOOR", h["title"].upper()):
            for w in cache[h["page"] - 1]["words"]:
                if DOOR_RE.match(w["t"].strip(PUNCT)):
                    puertas_sched.add(w["t"].strip(PUNCT))
    sheets_validas = {x["sheet"] for x in hojas if x["sheet"]}
    firmas = {_firma(x) for x in sheets_validas}
    for h in hojas:
        if not h["inventariable"]:
            continue
        i = h["page"] - 1
        ws, ls = cache[i]["words"], cache[i]["lines"]
        trazos = None

        def sim(w):
            nonlocal trazos
            if trazos is None:
                trazos = Trazos(segmentos(doc[i]))
            return simbolo(trazos, w["r"], w["size"])

        # --- detail bubbles (id encima de un sheet number) ---
        en_burbuja = set()
        # parte inferior: sheet number del índice, o con forma de hoja con "." / "-" (p. ej. Z9.01, Z-101) aunque no exista
        shs = [k for k, w in enumerate(ws) if SHEET_RE.match(w["t"].strip(PUNCT)) and
               (w["t"].strip(PUNCT) in sheets_validas or (re.search(r"[.\-]", w["t"]) and
                                                          _firma(w["t"].strip(PUNCT)) in firmas))]
        for k in shs:
            s = ws[k]
            sc = (s["r"].x0 + s["r"].x1) / 2
            for j, w in enumerate(ws):
                if j == k or not BUBBLE_ID_RE.match(w["t"]):
                    continue
                wc = (w["r"].x0 + w["r"].x1) / 2
                gap = s["r"].y0 - w["r"].y1
                if abs(wc - sc) <= max(0.6 * s["r"].width, 4) and -1 <= gap <= 2.2 * s["size"]:
                    ref = f"{w['t']}/{s['t'].strip(PUNCT)}"
                    propio = s["t"].strip(PUNCT) == h["sheet"]
                    existe = s["t"].strip(PUNCT) in sheets_validas
                    out["detail_bubble"].append(_occ("detail_bubble", {"t": ref, "r": w["r"] | s["r"],
                                                                       "size": s["size"]}, h,
                                                     {"ref": ref, "self_sheet": propio, "hoja_existe": existe}))
                    en_burbuja.update((j, k))
                    break
        # --- referencias N/HOJA en una línea ---
        for l in ls:
            for m in DETAIL_TXT_RE.finditer(l["t"]):
                out["detail_ref_text"].append(_occ("detail_ref_text", {"t": m.group(0), "r": l["r"], "size": l["size"]},
                                                   h, {"ref": f"{m.group(1)}/{m.group(2)}", "line": l["t"]}))
            # --- cotas ---
            for m in DIM_RE.finditer(l["t"]):
                out["cota"].append(_occ("cota", {"t": m.group(0).strip(), "r": l["r"], "size": l["size"]}, h,
                                        {"line": l["t"]}))
        # --- tags ---
        for j, w in enumerate(ws):
            t = w["t"].strip(PUNCT)
            if j in en_burbuja or not t:
                continue
            if t in T:
                s = sim(w)
                out["_ptype"].append(_occ("partition", dict(w, t=t), h, {"type": t, "simbolo": s,
                                                                          "exact_text": w["t"]}))
            elif TAG_DIGIT_RE.match(t) and t not in STOP:
                s = sim(w) if h.get("titulo_planta") else None
                if s:
                    out["partition_candidato"].append(_occ("partition_candidato", dict(w, t=t), h,
                                                           {"simbolo": s, "motivo": "forma de tag dentro de símbolo, "
                                                            "NO está en el schedule de partition types"}))
            if DOOR_RE.match(t) or WINDOW_RE.match(t):
                s = sim(w) if h.get("titulo_planta") else None
                if s and (t in puertas_sched or WINDOW_RE.match(t)):
                    out["door_window_tag"].append(_occ("door_window_tag", dict(w, t=t), h,
                                                       {"simbolo": s, "en_door_schedule": t in puertas_sched}))
                elif s and KEYNOTE_RE.match(t):
                    out["keynote"].append(_occ("keynote", dict(w, t=t), h, {"simbolo": s}))
            elif KEYNOTE_RE.match(t) and h.get("titulo_planta"):
                s = sim(w)
                if s:
                    out["keynote"].append(_occ("keynote", dict(w, t=t), h, {"simbolo": s}))
    return out


def clasificar(hojas, occ):
    """Separa partition_tag (cuenta) de partition_ambiguo (no cuenta, con motivo)."""
    por_pag = defaultdict(list)
    for o in occ.pop("_ptype", []):
        por_pag[o["page"]].append(o)
    hj = {h["page"]: h for h in hojas}
    tags, amb, txt = [], [], []
    for pg, os_ in por_pag.items():
        h = hj[pg]
        ref = [o for o in os_ if o["simbolo"] and len(o["type"]) >= 2 and re.search(r"\d", o["type"])]
        es_planta = h.get("titulo_planta") and not h.get("es_schedule_partition") and bool(ref)
        if ref:
            sz = Counter(round(o["size"], 1) for o in ref).most_common(1)[0][0]
            rad = sorted(o["simbolo"]["radio"] for o in ref)[len(ref) // 2]
        for o in os_:
            mot = None
            if h.get("es_schedule_partition"):
                mot = "hoja de schedule / leyenda de partition types (no es ocurrencia de planta)"
            elif not h.get("titulo_planta"):
                mot = "hoja que no es de planta (título sin PLAN)"
            elif not o["simbolo"]:
                mot = "sin símbolo cerrado alrededor (texto suelto, nota o leyenda)"
            elif not ref:
                mot = "la hoja no tiene types de varios caracteres en símbolo que sirvan de referencia"
            elif abs(o["size"] - sz) > 0.15 * sz:
                mot = f"tamaño de letra {o['size']} ≠ {sz} de los tags de la hoja (posible grid bubble / otro símbolo)"
            elif abs(o["simbolo"]["radio"] - rad) > 0.4 * rad:
                mot = f"radio de símbolo {o['simbolo']['radio']} ≠ {rad} de los tags de la hoja (otro símbolo)"
            if mot and (h.get("es_schedule_partition") or not (h.get("titulo_planta") or o["simbolo"])):
                o["kind"] = "partition_texto"          # texto suelto fuera de planta: se guarda, no se recorta
                o["motivo"] = mot
                txt.append(o)
            elif mot:
                o["kind"] = "partition_ambiguo"
                o["motivo"] = mot
                amb.append(o)
            else:
                o["kind"] = "partition_tag"
                tags.append(o)
        h["es_planta_partition"] = bool(es_planta)
    occ["partition_tag"] = sorted(tags, key=lambda o: (o["type"], o["page"], o["center_pt"][1], o["center_pt"][0]))
    for a in range(len(tags)):              # mismo type, misma hoja, símbolos que se tocan: ¿duplicado o dos walls?
        for b in range(a + 1, len(tags)):
            ta, tb = tags[a], tags[b]
            if ta["type"] == tb["type"] and ta["page"] == tb["page"]:
                d = math.dist(ta["center_pt"], tb["center_pt"])
                if d < ta["simbolo"]["radio"] + tb["simbolo"]["radio"] + max(ta["size"], tb["size"]):
                    for o, otro in ((ta, tb), (tb, ta)):
                        o.setdefault("superpuesto_con", []).append(otro["center_pt"])
    occ["partition_ambiguo"] = sorted(amb, key=lambda o: (o["type"], o["page"]))
    occ["partition_texto"] = sorted(txt, key=lambda o: (o["type"], o["page"]))
    for h in hojas:
        h.setdefault("es_planta_partition", False)
    for k, lst in occ.items():
        for n, o in enumerate(lst, 1):
            o["id"] = f"{k[:2].upper()}{n:04d}" if k != "partition_tag" else f"PT{n:04d}"
    return occ


# ------------------------------------------------------------------------------------------------------ recortes
ROJO = (1, 0, 0)


def recortes(doc, occs, out_dir, dpi=150, margen=60.0):
    """PNG por ocurrencia con el tag circulado; se reabre y se verifica. Devuelve lista de fallas."""
    os.makedirs(out_dir, exist_ok=True)
    fallas = []
    z = dpi / 72.0
    por_pag = defaultdict(list)
    for o in occs:
        por_pag[o["page"]].append(o)
    for pg, lst in por_pag.items():
        tmp = fitz.open()
        tmp.insert_pdf(doc, from_page=pg - 1, to_page=pg - 1)
        page = tmp[0]
        src = doc[pg - 1]
        tp = src.get_textpage()
        for o in lst:
            x0, y0, x1, y1 = o["bbox_pt"]
            cx, cy = o["center_pt"]
            rad = max(x1 - x0, y1 - y0) / 2.0 + 0.9 * o["size"]
            if o.get("simbolo"):
                rad = max(rad, o["simbolo"]["radio"] + 3)
            disp = fitz.Rect(cx - rad, cy - rad, cx + rad, cy + rad)
            ann = page.add_circle_annot(disp * page.derotation_matrix)
            ann.set_colors(stroke=ROJO)
            ann.set_border(width=2.0)
            ann.update()
            mg = max(margen, rad + 25)
            clip = fitz.Rect(cx - mg, cy - mg, cx + mg, cy + mg) & page.rect
            pix = page.get_pixmap(clip=clip, dpi=dpi)
            nombre = f"{o['id']}_{re.sub(r'[^A-Za-z0-9]+', '_', o.get('type') or o['text'])}_{o['sheet'] or 'p'}" \
                     f"_p{pg}.png"
            ruta = os.path.join(out_dir, nombre)
            pix.save(ruta)
            page.delete_annot(ann)
            ok, det = verificar_png(ruta, clip, (cx, cy), rad, z, src, o, tp)
            o["png"] = nombre
            o["png_verificado"] = ok
            if not ok:
                fallas.append(f"{o['id']} {o.get('type') or o['text']} {o['sheet']} p.{pg}: {det}")
        tmp.close()
    return fallas


def verificar_png(ruta, clip, c, rad, z, page, o, tp=None):
    """Reabre el PNG: anillo rojo a `rad` del centro, tinta oscura en el centro y el texto bajo la marca = el tag."""
    pix = fitz.Pixmap(ruta)
    n, W, H, s = pix.n, pix.width, pix.height, pix.samples
    if abs(W / clip.width - z) > 0.02 or abs(H / clip.height - z) > 0.02:
        return False, f"factor pt->px {W / clip.width:.3f} ≠ {z:.3f}"

    def px(x, y):
        x, y = int(round(x)), int(round(y))
        if not (0 <= x < W and 0 <= y < H):
            return None
        k = (y * W + x) * n
        return s[k], s[k + 1], s[k + 2]

    ccx, ccy = (c[0] - clip.x0) * z, (c[1] - clip.y0) * z
    rojos = 0
    for k in range(16):
        a = k * math.pi / 8
        hit = False
        for dr in range(-4, 5):
            p = px(ccx + (rad * z + dr) * math.cos(a), ccy + (rad * z + dr) * math.sin(a))
            if p and p[0] > 180 and p[1] < 90 and p[2] < 90:
                hit = True
                break
        rojos += hit
    if rojos < 12:
        return False, f"anillo rojo no aparece donde debe ({rojos}/16 rayos)"
    bx0, by0, bx1, by1 = o["bbox_pt"]
    oscuros = tot = 0
    for yy in range(int((by0 - clip.y0) * z), int((by1 - clip.y0) * z) + 1):
        for xx in range(int((bx0 - clip.x0) * z), int((bx1 - clip.x0) * z) + 1):
            p = px(xx, yy)
            if p:
                tot += 1
                oscuros += (sum(p) / 3 < 200)
    if not tot or oscuros / tot < 0.02:
        return False, f"sin tinta en el centro de la marca ({oscuros}/{tot})"
    zona = fitz.Rect(bx0 - 1, by0 - 1, bx1 + 1, by1 + 1) * page.derotation_matrix
    txt = " ".join(w[4] for w in page.get_text("words", clip=zona, textpage=tp))
    esperado = (o.get("type") or o["text"]).split("/")[0]
    if esperado not in re.sub(r"\s+", "", txt) and esperado not in txt:
        return False, f"texto bajo la marca '{txt.strip()}' ≠ '{esperado}'"
    return True, "ok"


def overview(doc, hojas, occ, out_dir, dpi=60):
    """Una imagen por hoja de planta con TODOS los tags contados circulados y numerados (lista = inventario.md).
    Se reabre y se verifica el anillo de cada marca; si una falla, la imagen se borra y se reporta."""
    fallas, hechas = [], []
    z = dpi / 72.0
    for h in hojas:
        if not h.get("es_planta_partition"):
            continue
        lst = [o for o in occ["partition_tag"] if o["page"] == h["page"]]
        tmp = fitz.open()
        tmp.insert_pdf(doc, from_page=h["page"] - 1, to_page=h["page"] - 1)
        page = tmp[0]
        rad = 16.0
        for o in lst:
            cx, cy = o["center_pt"]
            a = page.add_circle_annot(fitz.Rect(cx - rad, cy - rad, cx + rad, cy + rad) * page.derotation_matrix)
            a.set_colors(stroke=ROJO)
            a.set_border(width=3.0)
            a.update()
            n = int(o["id"][2:])
            page.insert_text(fitz.Point(cx + rad * 0.8, cy - rad * 0.8) * page.derotation_matrix, str(n),
                             fontsize=13, color=ROJO, rotate=page.rotation)
        nombre = f"OVERVIEW_{h['sheet'] or 'p'}_p{h['page']}.png"
        ruta = os.path.join(out_dir, nombre)
        page.get_pixmap(dpi=dpi).save(ruta)
        pix = fitz.Pixmap(ruta)
        malas = []
        for o in lst:
            cx, cy = o["center_pt"][0] * z, o["center_pt"][1] * z
            ok = 0
            for k in range(16):
                ang = k * math.pi / 8
                for dr in range(-3, 4):
                    x, y = int(round(cx + (rad * z + dr) * math.cos(ang))), int(round(cy + (rad * z + dr) * math.sin(ang)))
                    if 0 <= x < pix.width and 0 <= y < pix.height:
                        r_, g_, b_ = pix.pixel(x, y)[:3]
                        if r_ > 180 and g_ < 110 and b_ < 110:
                            ok += 1
                            break
            if ok < 10:
                malas.append(o["id"])
        tmp.close()
        if malas:
            os.remove(ruta)
            fallas.append(f"overview {h['sheet']} p.{h['page']}: marcas sin anillo en {malas} — imagen NO escrita")
        else:
            hechas.append(nombre)
            h["overview_png"] = nombre
    return hechas, fallas


# ------------------------------------------------------------------------------------------------------- reporte
def resumen_types(tipos, occ, hojas):
    res = OrderedDict()
    planta = {h["page"] for h in hojas if h.get("es_planta_partition")}
    for t in [x["type"] for x in tipos]:
        os_ = [o for o in occ["partition_tag"] if o["type"] == t]
        am = [o for o in occ["partition_ambiguo"] if o["type"] == t]
        tx = [o for o in occ.get("partition_texto", []) if o["type"] == t]
        por = OrderedDict()
        for o in os_:
            k = f"{o['sheet'] or '?'} (p.{o['page']})"
            por[k] = por.get(k, 0) + 1
        res[t] = {"total_planta": sum(1 for o in os_ if o["page"] in planta), "total": len(os_), "por_hoja": por,
                  "ambiguos": len(am), "texto_fuera_de_planta": len(tx), "ocurrencias": [o["id"] for o in os_]}
    return res


def md(inv):
    L = [f"# Inventario por script — {inv['pdf']}", "",
         f"md5 `{inv['md5']}` · {inv['pages']} páginas · coordenadas en pt de la página ROTADA (como el PNG) · "
         f"generado por inventario.py (sin lectura a ojo)", "",
         "## Partition types (del schedule / leyenda del PDF)", ""]
    for t in inv["partition_types"]["schedule"]:
        L.append(f"- **{t['type']}** — {'; '.join(t['fuentes'][:3])}")
    hp = [h for h in inv["sheets"] if h.get("es_planta_partition")]
    cols = [f"{h['sheet'] or '?'} p.{h['page']}" for h in hp]
    L += ["", "## Ocurrencias por type y hoja (solo tags en símbolo, en hojas de planta)", "",
          "| Type | " + " | ".join(cols) + " | TOTAL | ambiguos (no contados) |",
          "|---|" + "---|" * (len(cols) + 2)]
    for t, d in inv["partition_types"]["conteo"].items():
        fila = [str(d["por_hoja"].get(f"{h['sheet'] or '?'} (p.{h['page']})", 0)) for h in hp]
        L.append(f"| {t} | " + " | ".join(fila) + f" | **{d['total_planta']}** | {d['ambiguos']} |")
    L += ["", "## Ocurrencias contadas (lista numerada, una imagen por ocurrencia)", ""]
    for h in hp:
        if h.get("overview_png"):
            L.append(f"Vista de hoja {h['sheet']} p.{h['page']} con cada tag circulado y numerado: "
                     f"![overview](recortes/{h['overview_png']})")
    L.append("")
    for n, o in enumerate(inv["ocurrencias"]["partition_tag"], 1):
        L.append(f"{n}. `{o['id']}` **{o['type']}** — {o['sheet']} p.{o['page']} @ ({o['center_pt'][0]:.0f}, "
                 f"{o['center_pt'][1]:.0f}) pt · símbolo {o['simbolo']['forma_aprox']} · "
                 f"{'⚠ SUPERPUESTO con otro tag igual (¿duplicado o dos walls?) · ' if o.get('superpuesto_con') else ''}"
                 f"![{o['id']}](recortes/{o.get('png', '')}) {'✔' if o.get('png_verificado') else '✘ NO VERIFICADO'}")
    L += ["", "## Ambiguos (NO contados — revisar)", ""]
    for o in inv["ocurrencias"]["partition_ambiguo"]:
        L.append(f"- `{o['id']}` {o['type']} — {o['sheet']} p.{o['page']} @ ({o['center_pt'][0]:.0f}, "
                 f"{o['center_pt'][1]:.0f}): {o['motivo']}" + (f" · recortes/{o['png']}" if o.get("png") else ""))
    cand = Counter(o["text"] for o in inv["ocurrencias"]["partition_candidato"])
    L += ["", "## Tags en símbolo que NO están en el schedule (posible type faltante en el schedule → RFI)", "",
          ", ".join(f"{k} ×{v}" for k, v in sorted(cand.items())) or "ninguno", "",
          "## Otras ocurrencias (conteo)", ""]
    for k in ("partition_texto", "door_window_tag", "detail_bubble", "detail_ref_text", "keynote", "cota"):
        L.append(f"- {k}: {len(inv['ocurrencias'].get(k, []))}")
    L += ["", "## Hojas NO inventariables por script", ""]
    ni = [h for h in inv["sheets"] if not h["inventariable"]]
    L += [f"- p.{h['page']} {h['sheet'] or '(sin número)'}: {h['motivo']}" for h in ni] or ["- ninguna"]
    L += ["", "## Índice de hojas", "", "| Página | Sheet | Title | Planta con tags | Nota |", "|---|---|---|---|---|"]
    for h in inv["sheets"]:
        L.append(f"| {h['page']} | {h['sheet'] or '—'} | {h['title'] or '—'} | "
                 f"{'sí' if h.get('es_planta_partition') else ''} | {h['motivo']} |")
    if inv["avisos"]:
        L += ["", "## Avisos", ""] + [f"- {a}" for a in inv["avisos"]]
    return "\n".join(L) + "\n"


def inventario(pdf, out_dir, dpi=150, con_recortes=True):
    os.makedirs(out_dir, exist_ok=True)
    doc = fitz.open(pdf)
    md5 = hashlib.md5(open(pdf, "rb").read()).hexdigest()
    cache = [{"words": palabras(p), "lines": lineas(p)} for p in doc]
    hojas = indice_hojas(doc, cache)
    tipos = types_schedule(hojas, cache)
    avisos = []
    if not tipos:
        avisos.append("NO se encontró schedule / leyenda de partition types en el texto del PDF: no hay types que "
                      "buscar (¿schedule raster? revisar a mano y declararlo)")
    occ = clasificar(hojas, ocurrencias(doc, hojas, cache, tipos))
    if con_recortes:
        fallas = recortes(doc, occ["partition_tag"] + occ["partition_ambiguo"], os.path.join(out_dir, "recortes"), dpi)
        avisos += [f"PNG NO VERIFICADO: {f}" for f in fallas]
        _, fov = overview(doc, hojas, occ, os.path.join(out_dir, "recortes"))
        avisos += [f"PNG NO VERIFICADO: {f}" for f in fov]
    malas = Counter(o["ref"] for o in occ.get("detail_bubble", []) if not o.get("hoja_existe"))
    if malas:
        avisos.append("detail bubbles que citan una hoja que NO está en el índice (¿numeración distinta o hoja "
                      "faltante? → RFI): " + ", ".join(f"{k} ×{v}" for k, v in sorted(malas.items())))
    inv = {"pdf": os.path.basename(pdf), "pdf_path": os.path.abspath(pdf), "md5": md5, "pages": doc.page_count,
           "coord_system": "pt, página rotada (display); origen arriba-izquierda, igual que el PNG renderizado",
           "sheets": hojas,
           "partition_types": {"schedule": tipos, "conteo": None},
           "ocurrencias": {k: v for k, v in occ.items()},
           "no_inventariables": [{"page": h["page"], "sheet": h["sheet"], "motivo": h["motivo"]}
                                 for h in hojas if not h["inventariable"]],
           "avisos": avisos}
    inv["partition_types"]["conteo"] = resumen_types(tipos, occ, hojas)
    with open(os.path.join(out_dir, "inventario.json"), "w") as f:
        json.dump(inv, f, indent=1, ensure_ascii=False)
    with open(os.path.join(out_dir, "inventario.md"), "w") as f:
        f.write(md(inv))
    return inv


def main(argv):
    a = list(argv[1:])
    dpi, rec = 150, True
    if "--dpi" in a:
        i = a.index("--dpi")
        dpi = int(a[i + 1])
        del a[i:i + 2]
    if "--sin-recortes" in a:
        a.remove("--sin-recortes")
        rec = False
    if len(a) != 2:
        print(__doc__)
        return 2
    inv = inventario(a[0], a[1], dpi, rec)
    for t, d in inv["partition_types"]["conteo"].items():
        print(f"{t:8s} planta {d['total_planta']:3d}  " + "  ".join(f"{k}:{v}" for k, v in d["por_hoja"].items())
              + (f"  (ambiguos {d['ambiguos']})" if d["ambiguos"] else ""))
    for h in inv["no_inventariables"]:
        print(f"NO INVENTARIABLE p.{h['page']} {h['sheet'] or ''}: {h['motivo']}")
    for x in inv["avisos"]:
        print("AVISO:", x)
    return 1 if any(x.startswith("PNG NO VERIFICADO") for x in inv["avisos"]) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
