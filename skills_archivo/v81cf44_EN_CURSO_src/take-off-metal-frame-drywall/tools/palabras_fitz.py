# -*- coding: utf-8 -*-
"""palabras_fitz.py — words de una página con PyMuPDF, en el mismo formato que pdfplumber.extract_words(extra_attrs=['size']).

Origen (Chuze, 2026-11-01): arranque.py con pdfplumber tardaba > 2 min por hoja y llegaba a 10 GB de RAM en sets
vectoriales grandes (106 hojas de 3024x2160 pt). PyMuPDF da los mismos words en segundos.
Coordenadas: x0, x1, top, bottom en pt desde arriba-izquierda (igual que pdfplumber) — válido con rotation 0 y
cropbox == mediabox; si no, se usa pdfplumber (el llamador decide con `compatible`).
size = tamaño de fuente del span que contiene el centro del word.
"""
import fitz
import json
import os
import re
import subprocess
import sys
import tempfile


def compatible(page):
    # coords de fitz = relativas a la esquina sup-izq de la página visible (0..w, 0..h), como pdfplumber.
    # Vale con rotation 0 y cropbox del mismo tamaño que el mediabox (un mediabox desplazado no cambia nada).
    cb, mb = page.cropbox, page.mediabox
    return page.rotation == 0 and abs(cb.width - mb.width) < 0.5 and abs(cb.height - mb.height) < 0.5


def words(page):
    spans = []
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            for s in l['spans']:
                spans.append((fitz.Rect(s['bbox']), s['size']))
    out = []
    for x0, y0, x1, y1, t, *_ in page.get_text('words'):
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        size = next((sz for r, sz in spans if r.x0 - 0.5 <= cx <= r.x1 + 0.5 and r.y0 - 0.5 <= cy <= r.y1 + 0.5), 0.0)
        out.append(dict(text=t, x0=x0, x1=x1, top=y0, bottom=y1, size=round(size, 2)))
    return out


# ============================================================================================== BURBUJAS (U-137 / BE-139)
# Detector de burbujas de detalle de dos líneas, unido a palabras_fitz.py por el límite de 199 archivos del skill.
# palabras_fitz.py (burbujas) — U-137 / BE-139 (usuario 4-nov: "¿y qué pasó con los detail call outs?"): detector de BURBUJAS de detalle.
# 
# El detector anterior (CALLOUT en chequeos_biblioteca) solo veía "1/A3.2" escrito en UNA línea; en el plano la burbuja es un
# CÍRCULO con divisoria: número / letra / celda arriba (1, B, B4) y la hoja abajo (A3.2, A-302). CE_CALLOUTS pasaba en vacío
# (1 burbuja en O'Reilly, 0 en CFA y Chuze). Este módulo las encuentra por geometría:
#   - VECTOR: círculos dibujados (path de >= 4 bezier, casi cuadrado, 8–70 pt) con la palabra de arriba = id del detalle y la de
#     abajo = hoja; más "N/HOJA" en una sola palabra / línea en cualquier parte de la hoja.
#   - RASTER (hoja escaneada sin capa de texto): círculos por OpenCV (HoughCircles) con DIVISORIA horizontal (fila oscura que
#     cruza >= 85 % del círculo), OCR de la mitad de arriba (máscara fuera del círculo) y de la de abajo a 200 dpi y, si no
#     calza, a 400 dpi; la hoja se valida contra la lista de hojas del set ("J" final = "1").
#   - Todo círculo con divisoria que no se lee queda en sin_leer (con su posición): la compuerta lo exige verificado a ojo
#     (burbujas_verificadas.json) o FALLA. Nunca se adivina la lectura.
# Uso: palabras_fitz.py (burbujas) <pdf> <página 1-based> [--hojas A1.1,A3.2,...]  -> JSON en stdout (prueba manual).


RX_N = re.compile(r"^(?:[1-9]\d?|[A-Z]\d{0,2})$")
RX_H = re.compile(r"^[A-Z]{1,3}-?\d{1,3}(?:\.\d{1,2})?(?:\.?[A-Z])?$")   # A505.A (Chuze)
RX_UNA = re.compile(r"^([1-9]\d?|[A-Z]\d{0,2})/([A-Z]{1,3}-?\d{1,3}(?:\.\d{1,2})?(?:\.?[A-Z])?)$")


def norm(h):
    return str(h or "").upper().replace(" ", "")


_CACHE = {}


def _dibujos(p):
    """get_drawings una sola vez por página (Chuze A102: 3.97 M paths, 62 s por llamada)."""
    k = (id(p.parent), p.number)
    if k not in _CACHE:
        _CACHE.clear()
        _CACHE[k] = p.get_drawings()
    return _CACHE[k]


def _circulos_vector(p):
    """círculos dibujados: un path de >= 4 bezier casi cuadrado, o DOS medios círculos (paths de >= 2 bezier) que juntos
    forman el cuadrado (CFA A-221: D3/A-624 dibujada como dos semicírculos + divisoria)."""
    import pymupdf
    out, medios = [], []
    for d in _dibujos(p):
        r = d.get("rect")
        if not r or not (8 <= r.width <= 70):
            continue
        nc = sum(1 for it in d["items"] if it[0] == "c")
        if nc >= 4 and abs(r.width - r.height) <= 0.15 * r.width:
            out.append(r)
        elif nc >= 2 and (abs(r.width - 2 * r.height) <= 0.2 * r.width or abs(r.height - 2 * r.width) <= 0.2 * r.height):
            medios.append(r)
    usados = set()
    for i, r1 in enumerate(medios):
        for j in range(i + 1, len(medios)):
            if i in usados or j in usados:
                continue
            r2 = medios[j]
            u = pymupdf.Rect(r1) | r2
            if abs(u.width - u.height) <= 0.15 * u.width and abs(r1.width * r1.height + r2.width * r2.height
                                                                 - u.width * u.height) <= 0.15 * u.width * u.height:
                out.append(u)
                usados |= {i, j}
    return out

def _clip_gris(p, cx, cy, R, dpi=400):
    import numpy as np
    import pymupdf
    px = p.get_pixmap(dpi=dpi, colorspace=pymupdf.csGRAY, clip=pymupdf.Rect(cx - R, cy - R, cx + R, cy + R))
    return np.frombuffer(px.samples, dtype=np.uint8).reshape(px.height, px.width).copy()


def _leer_clip(p, cx, cy, r, hojas):
    """círculo vectorial SIN palabras dentro (texto AutoCAD SHX dibujado como líneas, O'Reilly S4.1): se rasteriza a 400 dpi
    y se lee como raster. Sin divisoria -> no es burbuja de dos líneas (grid bubble, keynote): None."""
    dpi = 400
    b = _clip_gris(p, cx, cy, r * 1.25, dpi)
    ri = int(r * dpi / 72)
    x0, y0 = b.shape[1] // 2, b.shape[0] // 2
    if y0 - ri < 0 or x0 - ri < 0 or y0 + ri >= b.shape[0] or x0 + ri >= b.shape[1]:
        return None
    dy = _divisoria(b, x0, y0, ri)
    if dy is None:
        return None
    n, h, hm = _leer(b, x0, y0, ri, dy)
    # segunda lectura a 250 dpi (independiente): id y hoja deben coincidir
    b2 = _clip_gris(p, cx, cy, r * 1.25, 250)
    r2 = int(r * 250 / 72)
    n2, h2, hm2 = _leer(b2, b2.shape[1] // 2, b2.shape[0] // 2, r2, int(dy * 250 / dpi))
    hs = [x for x in (_hoja_valida(v, hojas) for v in (hm, h, hm2, h2)) if x]
    ids = [v for v in (n, n2) if RX_N.match(v or "")]
    if hs and len(set(hs)) == 1 and len(hs) >= 2 and ids and len(set(ids)) == 1:
        return {"n": ids[0], "hoja": hs[0]}
    return {"n": None, "hoja": None, "lecturas": {"id": [n, n2], "hoja": [hm, h, hm2, h2]}}


def vector(p, hojas=None):
    import pymupdf
    ws = p.get_text("words")
    circ = _circulos_vector(p)
    lineas = _lineas_h(p)
    out, sin, usados, n_div = [], [], set(), 0
    vistos = []
    for r in circ:
        cx, cy, rr = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2, r.width / 2
        if any(abs(cx - a) < 2 and abs(cy - b) < 2 for a, b in vistos):
            continue                                   # mismo círculo dibujado dos veces (relleno + borde)
        vistos.append((cx, cy))
        dentro = [w for w in ws if r.contains(pymupdf.Point((w[0] + w[2]) / 2, (w[1] + w[3]) / 2))]
        pos = {"x": round(cx, 1), "y": round(cy, 1), "r": round(rr, 1)}
        arriba = [w for w in dentro if (w[1] + w[3]) / 2 < cy]
        abajo = [w for w in dentro if (w[1] + w[3]) / 2 >= cy]
        n = next((w[4] for w in arriba if RX_N.match(w[4])), None)
        h = next((w[4] for w in abajo if RX_H.match(w[4]) and re.search(r"\d", w[4])), None)
        if n and h and hojas and not _hoja_valida(h, hojas):
            h = None                                   # 'B / 101' (cuarto) no es hoja del set
        if n and h:
            n_div += 1
            out.append(dict(pos, n=n, hoja=h, metodo="vector círculo 2 líneas"))
            usados.update(id(w) for w in dentro)
            continue
        if not dentro and 8 <= rr <= 25 and _divisoria_vector(lineas, cx, cy, rr):   # sin divisoria dibujada no es burbuja
            lr = _leer_clip(p, cx, cy, rr, hojas)
            if lr is None:
                continue
            n_div += 1
            if lr["n"]:
                out.append(dict(pos, n=lr["n"], hoja=lr["hoja"], metodo="vector círculo sin texto (SHX) + OCR 400/250 dpi"))
            else:
                sin.append(dict(pos, n=None, hoja=None, lecturas=lr["lecturas"], metodo="vector círculo sin texto, sin leer"))
        elif h and not n and hojas and not _hoja_valida(h, hojas):
            continue                                   # 'G250' en un círculo = tag de equipo (Chuze A102), no una hoja del set
        elif h and not n:
            # marca de elevación interior / sección (CFA A-202): la hoja va DENTRO del círculo y los ids (B4, C2, C1) en
            # las puntas, fuera del círculo (r .. 2 r del centro)
            ids = [w[4] for w in ws if RX_N.match(w[4]) and w not in dentro and
                   rr <= (((w[0] + w[2]) / 2 - cx) ** 2 + ((w[1] + w[3]) / 2 - cy) ** 2) ** .5 <= 2.0 * rr]
            n_div += 1
            if ids:
                for i_ in sorted(set(ids)):
                    out.append(dict(pos, n=i_, hoja=h, metodo="vector marca de elevación (hoja dentro, ids en las puntas)"))
            elif _divisoria_vector(lineas, cx, cy, rr):
                sin.append(dict(pos, n=None, hoja=h, metodo="vector círculo incompleto"))
        elif n and _divisoria_vector(lineas, cx, cy, rr):
            # número arriba sin hoja legible abajo y con divisoria dibujada: burbuja sin leer (sin divisoria = keynote /
            # grid bubble de una línea, no es burbuja de detalle — Chuze A102: 257 grid / keynote circles)
            n_div += 1
            sin.append(dict(pos, n=n, hoja=h, metodo="vector círculo incompleto"))
    for w in ws:
        m = RX_UNA.match(w[4])
        if m and id(w) not in usados:
            out.append({"x": round((w[0] + w[2]) / 2, 1), "y": round((w[1] + w[3]) / 2, 1), "r": None, "n": m.group(1),
                        "hoja": m.group(2), "metodo": "vector N/HOJA en una línea"})
    return {"burbujas": out, "sin_leer": sin, "circulos": n_div}


def _ocr(img, wl, psm="7"):
    import cv2
    if img is None or img.size == 0 or min(img.shape[:2]) < 8:
        return ""
    f = tempfile.mktemp(suffix=".png")
    cv2.imwrite(f, img)
    r = subprocess.run(["tesseract", f, "-", "--psm", psm, "-c", f"tessedit_char_whitelist={wl}"], capture_output=True, text=True)  # stderr al pipe
    os.remove(f)
    return r.stdout.strip().replace(" ", "")


def _anillo_real(a, x, y, r, dy):
    """filtro de falsos positivos en texturas (hatch de CMU, piedra, piso moteado — O'Reilly A1.2 / A2.1 / A3.x, 545
    'sin leer' en la primera corrida): borde = anillo oscuro (>= 55 % en el mejor radio 0.94–1.06 r, Hough da el radio con
    error), franja de adentro (0.72–0.86 r) <= 25 % oscura, interior <= 28 % y la divisoria NO sigue de largo más allá del
    círculo (1.6–2.4 r a los dos lados < 60 %; las puntas del rombo llegan a ~1.45 r). Calibrado con las 30 burbujas reales
    y los 4 falsos positivos de A1.1 (burbujas reales: franja <= 0.22, interior <= 0.22, cruce <= 0.31)."""
    import numpy as np
    H, W = a.shape
    if y - r < 0 or x - r < 0 or y + r >= H or x + r >= W:
        return False
    ang = np.linspace(0, 2 * np.pi, 96, endpoint=False)

    def fr(rr):
        return (np.clip((x + rr * np.cos(ang)).astype(int), 1, W - 2), np.clip((y + rr * np.sin(ang)).astype(int), 1, H - 2))
    ring = 0
    for f in (0.94, 0.97, 1.0, 1.03, 1.06):
        X, Y = fr(r * f)
        ring = max(ring, (np.minimum.reduce([a[Y, X], a[Y + 1, X], a[Y - 1, X], a[Y, X + 1], a[Y, X - 1]]) < 140).mean())
    dentro = np.mean([(a[fr(r * f)[1], fr(r * f)[0]] < 140).mean() for f in (0.72, 0.79, 0.86)])
    yy, xx = np.ogrid[-r:r + 1, -r:r + 1]
    c = a[y - r:y + r + 1, x - r:x + r + 1]
    m = ((xx * xx + yy * yy) <= (0.7 * r) ** 2) & (np.abs(yy - dy) > 3)
    interior = (c[m] < 140).mean()
    yd = min(max(y + dy, 1), H - 2)
    lados = []
    for s_ in (-1, 1):
        x0, x1 = sorted((int(x + s_ * 1.6 * r), int(x + s_ * 2.4 * r)))
        x0, x1 = max(0, x0), min(W, x1)
        lados.append((a[yd - 1:yd + 2, x0:x1].min(0) < 140).mean() if x1 > x0 else 0)
    return ring >= 0.55 and dentro <= 0.25 and interior <= 0.28 and min(lados) < 0.6


def _divisoria(a, x, y, r):
    best, by = 0, None
    for yy in range(y - int(.25 * r), y + int(.25 * r) + 1):
        f = (a[yy, x - int(.8 * r):x + int(.8 * r)] < 110).mean()
        if f > best:
            best, by = f, yy
    return (by - y) if best >= 0.85 else None


def _leer(a, x, y, r, dy):
    import cv2
    import numpy as np
    c = a[y - r:y + r + 1, x - r:x + r + 1].copy()
    yy, xx = np.ogrid[-r:r + 1, -r:r + 1]
    c[(xx * xx + yy * yy) > (0.80 * r) ** 2] = 255
    yd = r + dy
    c[max(0, yd - 4):yd + 5, :] = 255
    top = c[int(0.18 * r):max(int(0.18 * r) + 2, yd - 3), int(0.25 * r):int(1.75 * r)]
    up = lambda im: cv2.copyMakeBorder(cv2.resize(im, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC), 25, 25, 25, 25,   # noqa: E731
                                       cv2.BORDER_CONSTANT, value=255)
    al = "0123456789ABCDEFGHJKLMNPRSTUVWXYZ"
    n = _ocr(up(top), al)
    if not RX_N.match(n):
        n2 = _ocr(up(top), al, psm="8")
        n = n2 if RX_N.match(n2) else n
    m = int(.12 * r)
    bot = a[y + dy + 4:y + r - m, x - int(.75 * r):x + int(.75 * r)]
    h = _ocr(up(bot), al + ".-") if bot.size else ""
    # segunda lectura de la hoja con máscara de círculo a 0.94 r (el borde del círculo pegado al último "1" lo vuelve "3":
    # 1/A3.1 leída A3.3 sin máscara). Prueba sobre 10 burbujas reales de A1.1 O'Reilly: 9/10 bien, la errada no es hoja del set.
    c2 = a[y - r:y + r + 1, x - r:x + r + 1].copy()
    c2[(xx * xx + yy * yy) > (0.94 * r) ** 2] = 255
    bot2 = c2[r + dy + 4:int(1.9 * r), :]
    h2 = _ocr(up(bot2), al + ".-") if bot2.size else ""
    return n, h, h2


def _hoja_valida(h, hojas):
    """corrige la confusión del OCR en el último carácter ("J" / "I" / "l" -> "1") y valida contra las hojas del set."""
    cands = [h, re.sub(r"[JIl|]$", "1", h), re.sub(r"[JIl|](?=\.)", "1", h)]
    if not hojas:
        return next((c for c in cands if RX_H.match(c)), None)
    hn = {norm(x).replace("-", ""): x for x in hojas}
    for c in cands:
        if RX_H.match(c) and norm(c).replace("-", "") in hn:
            return hn[norm(c).replace("-", "")]
    return None


def raster(p, hojas=None, dpi=200):
    import cv2
    import numpy as np
    import pymupdf
    pix = p.get_pixmap(dpi=dpi, colorspace=pymupdf.csGRAY)
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width)
    k = 72.0 / dpi
    cs = cv2.HoughCircles(cv2.medianBlur(a, 3), cv2.HOUGH_GRADIENT, dp=1, minDist=40, param1=120, param2=40,
                          minRadius=int(8 / k), maxRadius=int(25 / k))
    out, sin, n_div = [], [], 0
    for x, y, r in ([] if cs is None else cs[0]):
        x, y, r = int(x), int(y), int(r)
        if y - r < 0 or x - r < 0 or y + r >= a.shape[0] or x + r >= a.shape[1]:
            continue
        dy = _divisoria(a, x, y, r)
        if dy is None or not _anillo_real(a, x, y, r, dy):
            continue
        n_div += 1
        n, h, hm = _leer(a, x, y, r, dy)
        # lectura independiente del id a 400 dpi del recorte (el id debe coincidir)
        R = r * k * 1.25
        X, Y = x * k, y * k
        px2 = p.get_pixmap(dpi=400, colorspace=pymupdf.csGRAY, clip=pymupdf.Rect(X - R, Y - R, X + R, Y + R))
        b = np.frombuffer(px2.samples, dtype=np.uint8).reshape(px2.height, px2.width).copy()
        s_ = 400 / dpi
        n2, h4, _ = _leer(b, b.shape[1] // 2, b.shape[0] // 2, int(r * s_), int(dy * s_))
        hs = [_hoja_valida(v, hojas) for v in (hm, h, h4)]
        validas = [v for v in hs if v]
        # hoja: la lectura con máscara manda; vale solo si ninguna otra lectura válida la contradice y al menos otra coincide
        # o ninguna otra es válida (nunca se elige entre dos hojas distintas: eso queda sin leer)
        hv = None
        if validas and len(set(validas)) == 1 and (hs[0] or len(validas) >= 2):
            hv = validas[0]
        crudos = [n, n2]
        ids = [v for v in (n, n2) if RX_N.match(v or "")]
        nv = ids[0] if ids and len(set(ids)) == 1 else None
        n = nv
        pos = {"x": round(x * k, 1), "y": round(y * k, 1), "r": round(r * k, 1)}
        if n and RX_N.match(n) and hv:
            out.append(dict(pos, n=n, hoja=hv, metodo="raster círculo con divisoria + OCR 200/400 dpi"))
        else:
            sin.append(dict(pos, n=None, hoja=None, lecturas={"id": crudos, "hoja": [hm, h, h4]}, metodo="raster círculo con divisoria sin leer"))
    return {"burbujas": out, "sin_leer": sin, "circulos": n_div}


def indep_raster(p, dpi=200):
    """U-137 conteo INDEPENDIENTE (no Hough): parte de las DIVISORIAS (segmentos horizontales oscuros) y prueba un anillo
    oscuro de radio 11–25 pt alrededor (72 puntos, >= 85 % oscuros). Devuelve [(x, y, r)] en pt. Validación del detector."""
    import cv2
    import numpy as np
    import pymupdf
    k = 72.0 / dpi
    pix = p.get_pixmap(dpi=dpi, colorspace=pymupdf.csGRAY)
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width)
    hor = cv2.morphologyEx((a < 140).astype(np.uint8), cv2.MORPH_OPEN,
                           cv2.getStructuringElement(cv2.MORPH_RECT, (int(18 / k), 1)))
    n, lab, st, _ = cv2.connectedComponentsWithStats(hor, 8)
    ang = np.linspace(0, 2 * np.pi, 72, endpoint=False)
    out = []
    for i in range(1, n):
        x, y, w, h, _ = st[i]
        if not (20 / k <= w <= 130 / k) or h > 60 / k:
            continue
        sub = lab[y:y + h, x:x + w] == i
        ry = int(np.argmax(sub.sum(1)))
        xs_ = np.where(sub[ry])[0]
        cx, cy = x + xs_.mean(), y + ry
        best = (0, 0, 0, 0)
        for rr in np.arange(11 / k, min(25 / k, (xs_.max() - xs_.min()) / 2 + 3), 2.0):
            for oy in range(-int(0.3 * rr), int(0.3 * rr) + 1, 3):
                for ox in range(-int(0.3 * rr), int(0.3 * rr) + 1, 3):
                    X = (cx + ox + rr * np.cos(ang)).astype(int)
                    Y = (cy + oy + rr * np.sin(ang)).astype(int)
                    if X.min() < 1 or Y.min() < 1 or X.max() >= a.shape[1] - 1 or Y.max() >= a.shape[0] - 1:
                        continue
                    v = np.minimum.reduce([a[Y, X], a[Y + 1, X], a[Y - 1, X], a[Y, X + 1], a[Y, X - 1]])
                    f = (v < 140).mean()
                    if f > best[0]:
                        best = (f, rr, ox, oy)
        f, rr, ox, oy = best
        if f >= 0.85:
            # interior claro (una burbuja no es una mancha negra) y la divisoria cruza el círculo
            m = np.zeros_like(a, dtype=np.uint8)
            cv2.circle(m, (int(cx + ox), int(cy + oy)), int(rr * 0.8), 1, -1)
            if (a[m == 1] < 140).mean() < 0.45:
                out.append((round((cx + ox) * k, 1), round((cy + oy) * k, 1), round(rr * k, 1)))
    # una burbuja = un solo anillo
    dedup = []
    for c in out:
        if all(abs(c[0] - d[0]) > 6 or abs(c[1] - d[1]) > 6 for d in dedup):
            dedup.append(c)
    return dedup


def _lineas_h(p):
    """líneas horizontales indexadas por franja de 4 pt de altura: {int(y / 4): [(x0, x1, y)]}."""
    L = {}
    for d in _dibujos(p):
        for it in d["items"]:
            if it[0] == "l" and abs(it[1].y - it[2].y) < 0.5:
                seg = (min(it[1].x, it[2].x), max(it[1].x, it[2].x), it[1].y)
            elif it[0] == "re" and it[1].height < 0.8:
                seg = (it[1].x0, it[1].x1, it[1].y0)
            else:
                continue
            if seg[1] - seg[0] >= 8:
                L.setdefault(int(seg[2] // 4), []).append(seg)
    return L


def _divisoria_vector(lineas, cx, cy, r):
    for b in range(int((cy - 0.3 * r) // 4), int((cy + 0.3 * r) // 4) + 1):
        for x0, x1, y in lineas.get(b, ()):
            # la divisoria termina en el círculo; una línea guía que lo atraviesa (tag de equipo G002 de Chuze A102) no
            if abs(y - cy) <= 0.3 * r and (min(x1, cx + r) - max(x0, cx - r)) >= 1.6 * r and \
                    x0 >= cx - 1.2 * r and x1 <= cx + 1.2 * r:
                return True
    return False


def indep_vector(p):
    """conteo independiente en hojas vector: círculos dibujados con una línea horizontal dentro que cruza >= 80 % del
    diámetro cerca del centro (la divisoria), sin mirar el texto."""
    circ = []
    for r in _circulos_vector(p):
        c = ((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2, r.width / 2)
        if 8 <= c[2] <= 25 and all(abs(c[0] - d[0]) > 2 or abs(c[1] - d[1]) > 2 for d in circ):
            circ.append(c)
    L = _lineas_h(p)
    return [(round(cx, 1), round(cy, 1), round(r, 1)) for cx, cy, r in circ if _divisoria_vector(L, cx, cy, r)]

def detectar(p, hojas=None, raster_pag=None):
    if raster_pag is None:
        raster_pag = len(p.get_text("text").strip()) < 200
    r = raster(p, hojas) if raster_pag else vector(p, hojas)
    ind = indep_raster(p) if raster_pag else indep_vector(p)
    todos = r["burbujas"] + r["sin_leer"]
    falta = [c for c in ind if all(((b["x"] - c[0]) ** 2 + (b["y"] - c[1]) ** 2) ** .5 > 8 for b in todos if b.get("r"))]
    r["conteo_independiente"] = len(ind)
    r["indep_no_detectados"] = [{"x": x, "y": y, "r": rr} for x, y, rr in falta]
    return r


if __name__ == "__main__":  # palabras_fitz.py <pdf> <página 1-based> [--hojas ...] -> burbujas de la página
    import pymupdf
    a = sys.argv[1:]
    hs = a[a.index("--hojas") + 1].split(",") if "--hojas" in a else None
    d = pymupdf.open(a[0])
    print(json.dumps(detectar(d[int(a[1]) - 1], hs), ensure_ascii=False, indent=1))
