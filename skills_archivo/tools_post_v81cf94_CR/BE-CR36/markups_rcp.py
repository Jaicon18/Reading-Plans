#!/usr/bin/env python3
"""markups_rcp.py — R80e.135 / BE-VS-15 (03-nov-2026, TODOS): toda hoja con renglones del take-off lleva markups.

Agrega al PDF de markups (salida de markups_bluebeam.py + markups_demo.py) un POLÍGONO por cada ceiling / soffit /
bulkhead del canon en la hoja del RCP (constants.rcp_sheet), con el formato que verificar_markups_excel cuadra contra
el Excel:
  Subject  = el board del renglón del Excel (ej. '5/8 GYPSUM BOARD TYPE X')
  Contents = '<Subject> · CEILING <room> · <SF> SF · CLG <altura> · <detalle N/HOJA> · <room>'
  /NM      = 'TO-<room>'  (el room es el ID del desglose 'ceiling <room> <SF>' del Material Summary)
  /Measure = escala impresa de la hoja (pt/ft), /IT /PolygonDimension (Bluebeam muestra el Area en SF).
Además dibuja (contenido de página, no annot) los clusters de lateral bracing (4 splay wires + compression strut)
@12'-0" O.C. en cada dirección y a no más de 6'-0" del perímetro, como los cuenta el take-off, y la leyenda del RCP.
Escribe un PNG por hoja.

Entrada: polys.json = [{room, polygon [[x, y], ...] (coordenadas de la página TAL COMO SE VE, page.rect)}].
Uso:  python3 markups_rcp.py <markups.pdf> <takeoff_canon.json> <polys.json> <salida.pdf> <dir_png>
rc 0 = todos los ceilings con área del take-off tienen polígono; rc 1 = falta alguno (lista en stdout).
"""
import json
import math
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import markups_bluebeam as mb  # noqa: E402

RGB = (0.0, 0.55, 0.85)
BRACE_RGB = (0.85, 0.1, 0.55)
MT_AREA = 129            # /MeasurementTypes de un área de Bluebeam Revu
BOARD_TXT = {"5/8 type X": "5/8 GYPSUM BOARD TYPE X", "5/8 regular": "5/8 GYPSUM BOARD",
             "1/2 MR": "1/2 GYPSUM BOARD MOISTURE RESISTANT", "5/8 MR": "5/8 GYPSUM MOISTURE RESISTANT"}



def largo_polilinea(pts):
    """BE-GK18 (Grand Kia): length of a polyline along its path (never first-to-last: a closed loop would read 0)."""
    return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))

def _area(p):
    return abs(sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p)))) / 2


def _clusters(c):
    """Centros de los clusters de bracing (J/A12.02): ROUNDUP(ns/12) x ROUNDUP(ew/12) en ceilings usg_grid."""
    if c.get("system") != "usg_grid" or not c.get("ns_ft") or not c.get("ew_ft"):
        return 0, 0
    return math.ceil(float(c["ns_ft"]) / 12 - 1e-9), math.ceil(float(c["ew_ft"]) / 12 - 1e-9)


def _color_hatch(page, pts, k):
    """Color de los trazos del hatch: constants.rcp_hatch_color {value: [r, g, b]} o el color más común de los trazos
    finos (<= 0.3 pt) que caen dentro del polígono."""
    c = k.get("rcp_hatch_color")
    c = c.get("value") if isinstance(c, dict) else c
    if c:
        return tuple(float(v) for v in c)
    import collections
    x0, y0 = min(p[0] for p in pts), min(p[1] for p in pts)
    x1, y1 = max(p[0] for p in pts), max(p[1] for p in pts)
    cnt = collections.Counter()
    for dr in page.get_drawings():
        r = dr["rect"]
        if dr["type"] == "s" and dr.get("color") and (dr.get("width") or 0) <= 0.3 and x0 <= r.x0 and r.x1 <= x1 and y0 <= r.y0 and r.y1 <= y1:
            cnt[tuple(round(v, 3) for v in dr["color"])] += 1
    return cnt.most_common(1)[0][0] if cnt else None


def sin_hatch(page, pts, color, r=9, min_pt=16.0, max_abertura_pt2=4 * 324.0):
    """R80f.16 (Chuze FINAL5, regla: el cielo GWB = SOLO el área con hatch, limitada por las caras): partes del polígono
    sin trazos del hatch (un sub-recinto blanco cerrado sin hatch es un hueco). Rasteriza a 1 px / pt los trazos del
    hatch (color) y el polígono, cierra el hatch (r px) y abre lo no cubierto (min_pt) para no contar la franja que el
    hatch deja contra las caras. -> [(área pt², bbox)] de cada parte sin hatch."""
    from PIL import Image, ImageDraw, ImageFilter
    if not color:
        return []
    x0, y0 = int(min(p[0] for p in pts)) - 2, int(min(p[1] for p in pts)) - 2
    x1, y1 = int(max(p[0] for p in pts)) + 3, int(max(p[1] for p in pts)) + 3
    W, H = x1 - x0, y1 - y0
    hm = Image.new("L", (W, H), 0)
    dh = ImageDraw.Draw(hm)
    for dr in page.get_drawings():
        c = dr.get("color")
        if dr["type"] != "s" or not c or max(abs(a - b) for a, b in zip(c, color)) > 0.01:
            continue
        rr = dr["rect"]
        if rr.x1 < x0 or rr.x0 > x1 or rr.y1 < y0 or rr.y0 > y1:
            continue
        for it in dr["items"]:
            if it[0] == "l":
                dh.line((it[1].x - x0, it[1].y - y0, it[2].x - x0, it[2].y - y0), fill=255, width=1)
    k_ = 2 * r + 1
    hm = hm.filter(ImageFilter.MaxFilter(k_)).filter(ImageFilter.MinFilter(k_))
    pm = Image.new("L", (W, H), 0)
    ImageDraw.Draw(pm).polygon([(x - x0, y - y0) for x, y in pts], fill=255)
    hp, pp = hm.load(), pm.load()
    un = Image.new("L", (W, H), 0)
    up = un.load()
    for yy in range(H):
        for xx in range(W):
            if pp[xx, yy] and not hp[xx, yy]:
                up[xx, yy] = 255
    m = int(min_pt) | 1
    op = un.filter(ImageFilter.MinFilter(m)).filter(ImageFilter.MaxFilter(m))
    a = op.load()
    seen, out = set(), []
    for yy in range(H):
        for xx in range(W):
            if a[xx, yy] and (xx, yy) not in seen:
                st, n, bx = [(xx, yy)], 0, [xx, yy, xx, yy]
                seen.add((xx, yy))
                while st:
                    cx, cy = st.pop()
                    n += 1
                    bx = [min(bx[0], cx), min(bx[1], cy), max(bx[2], cx), max(bx[3], cy)]
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < W and 0 <= ny < H and a[nx, ny] and (nx, ny) not in seen:
                            seen.add((nx, ny))
                            st.append((nx, ny))
                bb = (bx[0] + x0, bx[1] + y0, bx[2] + x0 + 1, bx[3] + y0 + 1)
                # un hueco INTERIOR chico (no toca el borde del polígono, < max_abertura_pt2) es una abertura del cielo
                # (difusor, fan, access panel): el board no descuenta aberturas -> no es parte sin hatch
                borde = any(_dist_seg_rect(pts[i], pts[(i + 1) % len(pts)], bb) <= r + 2 for i in range(len(pts)))
                if borde or n >= max_abertura_pt2:
                    out.append((float(n), bb))
    return out


def _dist_seg_rect(a, b, bb):
    """distancia mínima entre el segmento a-b y el rectángulo bb (0 si se tocan)."""
    import math as _m
    best = 1e9
    for k in range(21):
        t = k / 20.0
        x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
        dx = max(bb[0] - x, 0, x - bb[2])
        dy = max(bb[1] - y, 0, y - bb[3])
        best = min(best, _m.hypot(dx, dy))
    return best


def _pagina(doc, hoja, k):
    """Página de la hoja: Page Label = hoja; si no, el title block (texto) de la hoja; si no, constants.rcp_page."""
    for i in range(doc.page_count):
        if doc[i].get_label() == hoja:
            return i
    try:
        i = mb._Paginas(doc).por_titulo(hoja)
        if i is not None:
            return i
    except Exception:                                  # noqa: BLE001
        pass
    sm = k.get("rcp_page")
    return int(sm.get("value") if isinstance(sm, dict) else sm) - 1 if sm else None


def _bracing_on(k):
    """R80f.13: clusters de lateral bracing solo si el set los pide (constants.ceiling_lateral_bracing != false)."""
    b = k.get("ceiling_lateral_bracing")
    b = b.get("value") if isinstance(b, dict) else b
    return b is not False


def _label(doc, pg, hoja):
    try:                                               # Page Label = hoja (columna Page Label de Bluebeam)
        reglas = list(doc.get_page_labels() or [])
        viejo = next((r for r in reglas if r["startpage"] == pg and r.get("style")), None)
        if viejo:                                      # la página arrancaba una numeración: la corre a pg + 1
            reglas.remove(viejo)
            if pg + 1 < doc.page_count and (pg + 1) not in {r["startpage"] for r in reglas}:
                reglas.append({"startpage": pg + 1, "prefix": viejo.get("prefix", ""), "style": viejo["style"],
                               "firstpagenum": viejo.get("firstpagenum", 1) + 1})
        if pg not in {r["startpage"] for r in reglas}:
            prev = max((r for r in reglas if r["startpage"] < pg), key=lambda r: r["startpage"], default=None)
            reglas.append({"startpage": pg, "prefix": str(hoja), "style": "", "firstpagenum": 1})
            if pg + 1 < doc.page_count and (pg + 1) not in {r["startpage"] for r in reglas} and prev and prev.get("style"):
                reglas.append({"startpage": pg + 1, "prefix": prev.get("prefix", ""), "style": prev["style"],
                               "firstpagenum": prev.get("firstpagenum", 1) + (pg + 1 - prev["startpage"])})
            doc.set_page_labels(sorted(reglas, key=lambda r: r["startpage"]))
    except Exception:                                  # noqa: BLE001
        pass


def escribir(pdf_in, canon_p, polys_p, pdf_out, dir_png):
    """R80f.13 (Chuze FINAL5): VARIAS hojas de RCP — la hoja de cada ceiling = ceilings[].sheet (o constants.rcp_sheet);
    el polígono se busca por id (ceilings[].id) o por room; ID del Contents / NM = id si existe; Contents lleva el tag
    del cielo ('GWB CEILING C-5 · <id>') cuando ceilings[].ceiling_tag existe; clusters de bracing solo si el set los
    pide; leyenda por hoja en la esquina con menos tinta; un PNG por hoja."""
    import pymupdf as fitz
    canon = json.load(open(canon_p, encoding="utf-8"))
    _pl = json.load(open(polys_p, encoding="utf-8"))
    _pl = _pl.get("polys", _pl) if isinstance(_pl, dict) else _pl
    polys = {}
    for p in _pl:
        if p.get("misc"):
            continue
        for key in (p.get("id"), p.get("room")):
            if key:
                polys[key] = p["polygon"]
    causas = {(p.get("id") or p.get("room")): p["cause"] for p in _pl if p.get("cause") and not p.get("misc")}
    k = canon.get("constants") or {}
    hoja0 = k.get("rcp_sheet")
    hoja0 = hoja0.get("value") if isinstance(hoja0, dict) else hoja0
    brace = _bracing_on(k)
    doc = fitz.open(pdf_in)
    falta, por_hoja, sinh = [], {}, []
    for c in canon.get("ceilings") or []:
        room, sf = c.get("room"), float(c.get("area_sf") or 0)
        if not sf or str(c.get("status") or "").upper() == "EXCLUDED":
            continue
        cid = c.get("id") or room
        hoja = c.get("sheet") or hoja0
        pts = polys.get(cid) or polys.get(room)
        if not pts or not hoja:
            falta.append(cid)
            continue
        h_ = por_hoja.get(hoja)
        if h_ is None:
            pg = _pagina(doc, hoja, k)
            if pg is None:
                print(json.dumps({"error": f"no encuentro la página de la hoja {hoja}"}))
                return 1
            h_ = por_hoja[hoja] = {"pg": pg, "n": 0, "sf": 0.0, "cl": 0}
        page = doc[h_["pg"]]
        M = page.derotation_matrix
        esc = mb.escala(canon, hoja)
        sub = BOARD_TXT.get(str(c.get("board") or ""), str(c.get("board") or "GYPSUM BOARD").upper())
        det = c.get("detail") or (c.get("system_callout") or {}).get("detail") or ""
        h = float(c.get("height_ft") or 0)
        cz = f" · cause: {causas[cid]}" if cid in causas else ""
        tag = f" · GWB CEILING {c['ceiling_tag']}" if c.get("ceiling_tag") else ""
        txt = f"{sub}{tag} · CEILING {room} · {sf:,.2f} SF · CLG {mb.ftin(h)}{cz} · {det} · {cid}"
        if not c.get("hatch_check_cause") and not causas.get(cid):      # R80f.16: el polígono sigue al hatch
            sh = [(n_, b_) for n_, b_ in sin_hatch(page, pts, _color_hatch(page, pts, k)) if esc and n_ / esc ** 2 >= 1.0]
            if sh:
                sinh.append(f"{cid}: " + "; ".join(f"{n_ / esc ** 2:.2f} SF without hatch at "
                                                   f"{tuple(round(v, 1) for v in b_)}" for n_, b_ in sh))
        a = page.add_polygon_annot([fitz.Point(x, y) * M for x, y in pts])
        a.set_info(title="take-off", subject=sub, content=txt)
        a.set_colors(stroke=RGB, fill=RGB)
        a.set_border(width=1.5)
        a.set_opacity(0.35)
        a.update()
        mb._nm(doc, a, "TO-" + cid)
        if esc:
            mb._measure(doc, a, esc)
            doc.xref_set_key(a.xref, "IT", "/PolygonDimension")
            doc.xref_set_key(a.xref, "MeasurementTypes", str(MT_AREA))
        h_["n"] += 1
        h_["sf"] += sf
        nx, ny = _clusters(c) if brace else (0, 0)
        if nx and ny:
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
            for i in range(nx):
                for j in range(ny):
                    cx = x0 + (x1 - x0) * (i + 0.5) / nx
                    cy = y0 + (y1 - y0) * (j + 0.5) / ny
                    page.draw_polyline([fitz.Point(cx, cy - 5) * M, fitz.Point(cx - 5, cy + 4) * M,
                                        fitz.Point(cx + 5, cy + 4) * M, fitz.Point(cx, cy - 5) * M],
                                       color=BRACE_RGB, fill=BRACE_RGB, width=0.8)
                    h_["cl"] += 1
    # rev7 CR City Hotel (COORDINACIÓN 7-nov, U-124): TODO cielo / soffit cuantificado en misc_items lleva markup, no solo ceilings[].
    # Entradas {"misc": true, id, sheet, kind "area" (polygons, sf) | "line" (lines, lf, depth_ft), board, cause} de polys.json.
    for e in [p for p in _pl if p.get("misc")]:
        hoja, cid = e.get("sheet"), e["id"]
        h_ = por_hoja.get(hoja)
        if h_ is None:
            pg = _pagina(doc, hoja, k)
            if pg is None:
                falta.append(cid)
                continue
            h_ = por_hoja[hoja] = {"pg": pg, "n": 0, "sf": 0.0, "cl": 0}
        page = doc[h_["pg"]]
        M = page.derotation_matrix
        esc = mb.escala(canon, hoja)
        sub = str(e.get("board") or "GYPSUM BOARD").upper()
        piezas = e.get("polygons") if e.get("kind") == "area" else e.get("lines")
        # la causa no lleva cifras con unidad que el lector de Contents tome por LF / SF / H del markup
        e["cause"] = re.sub(r"\bft\b", "feet", re.sub(r"\bSF\b", "sq.ft", re.sub(r"\bLF\b", "lin.ft", str(e.get("cause") or ""))))
        acc_lf = acc_wa = 0.0
        for i_, pts in enumerate(piezas or []):
            nm = "TO-" + cid + (f"~{i_ + 1}" if len(piezas) > 1 else "")
            if e.get("kind") == "area":
                a = page.add_polygon_annot([fitz.Point(x, y) * M for x, y in pts])
                lay_ = int(e.get("layers") or 1)
                sf_p = e["sf"] * lay_ * (_area(pts) / sum(_area(q) for q in piezas))
                txt = (f"{sub} · CEILING {cid} · cause: {e.get('cause')}; board = {lay_} layer(s) x drawn area · "
                       f"{sf_p / lay_:,.2f} SF · {e.get('nhoja') or hoja} · {cid}")
            else:
                a = page.add_polyline_annot([fitz.Point(x, y) * M for x, y in pts])
                # redondeo ACUMULADO (R80e.163): cada etiqueta a <= 0.01 de su geometría y la suma = el total cargado exacto
                _g = [largo_polilinea(q) for q in piezas]; _G = sum(_g) or 1.0   # BE-GK18: path length (a closed loop has first == last point)
                _c1 = e["lf"] * sum(_g[:i_ + 1]) / _G; _c0 = e["lf"] * sum(_g[:i_]) / _G
                lf_p = round(_c1, 2) - round(_c0, 2)
                wa_ = round(round(_c1 * e["depth_ft"], 2) - round(_c0 * e["depth_ft"], 2), 2)
                lf_p = round(lf_p, 2)
                txt = (f"{sub} · {lf_p:,.2f} LF · H {mb.ftin(e['depth_ft'])} · {wa_:,.2f} SF wall (LF×H) · {wa_:,.2f} SF board · "
                       f"SOFFIT {cid} (H = developed width) · cause: {e.get('cause')} · {e.get('nhoja') or hoja} · {cid}")
            a.set_info(title="take-off", subject=sub, content=txt)
            a.set_colors(stroke=(0.1, 0.6, 0.2), fill=(0.1, 0.6, 0.2) if e.get("kind") == "area" else None)
            a.set_border(width=1.5 if e.get("kind") == "area" else 2.5)
            a.set_opacity(0.35 if e.get("kind") == "area" else 0.8)
            a.update()
            mb._nm(doc, a, nm)
            if esc:
                mb._measure(doc, a, esc)
                if e.get("kind") == "area":
                    doc.xref_set_key(a.xref, "IT", "/PolygonDimension")
                    doc.xref_set_key(a.xref, "MeasurementTypes", str(MT_AREA))
                else:
                    mb._depth(doc, a, float(e["depth_ft"]))
        h_["n"] += 1
        h_["sf"] += float(e.get("sf") or (e.get("lf", 0) * e.get("depth_ft", 0)))
    for hoja, h_ in por_hoja.items():
        page = doc[h_["pg"]]
        M = page.derotation_matrix
        lin = [f"TAKE-OFF LEGEND - {hoja} (gypsum board ceilings / soffits)",
               f"blue area = gyp bd ceiling (ceilings), green area / line = gyp bd ceiling / soffit of the misc rows (CLG / SOF / RS / CAN / BW): {h_['n']} items, {h_['sf']:,.2f} SF (Contents: board · ceiling tag · room · SF · ceiling height · detail · id)",
               "measure: /Measure at the printed scale of the sheet; SF = Excel row (ceiling id)"]
        if h_["cl"]:
            lin.insert(2, f"magenta triangle = lateral bracing cluster (splay wires + compression strut): {h_['cl']}")
        R = page.rect
        W_, H_ = 470.0, 20.0 + 14.0 * len(lin)
        cands = [fitz.Rect(R.x0 + 40, R.y0 + 40, R.x0 + 40 + W_, R.y0 + 40 + H_),
                 fitz.Rect(R.x0 + 40, R.y1 - 40 - H_, R.x0 + 40 + W_, R.y1 - 40),
                 fitz.Rect(R.x0 + R.width * 0.4, R.y0 + 40, R.x0 + R.width * 0.4 + W_, R.y0 + 40 + H_),
                 fitz.Rect(R.x0 + R.width * 0.4, R.y1 - 40 - H_, R.x0 + R.width * 0.4 + W_, R.y1 - 40)]
        dr = [d_["rect"] for d_ in page.get_drawings() if d_.get("rect")]
        box = min(cands, key=lambda c_: sum(1 for r_ in dr if r_.intersects(c_)))
        page.draw_rect(box * M, color=(0, 0, 0), fill=(1, 1, 1), width=0.8)
        for i_, t_ in enumerate(lin):
            page.insert_text(fitz.Point(box.x0 + 6, box.y0 + 14 + 14 * i_) * M, t_, fontsize=7.5 if i_ else 8.5,
                             fontname="hebo" if i_ == 0 else "helv", rotate=page.rotation)
        _label(doc, h_["pg"], hoja)
    labels = {i + 1: doc[i].get_label() for i in range(doc.page_count)}
    mb.nm_unicos(doc)                                        # U-167: /NM único en todo el PDF y sin '/'
    doc.save(pdf_out, garbage=3, deflate=True)
    # BE-CR31 (CR City Hotel rev4, v81cf61): los polígonos de ceiling llevan /Measure pero el PDF salía SIN la escala de página /VP en
    # las hojas de RCP (editable() corría en markups_bluebeam ANTES de este paso) -> Bluebeam mostraba la escala por defecto.
    # Se re-aplica editable() al PDF final con las Page Labels que ya trae (U-151 / U-152).
    mb.editable(pdf_out, {k: v for k, v in labels.items() if v})
    os.makedirs(dir_png, exist_ok=True)
    d2 = fitz.open(pdf_out)
    for hoja, h_ in por_hoja.items():
        d2[h_["pg"]].get_pixmap(dpi=110).save(os.path.join(dir_png, f"{hoja}_rcp_markups.png"))
    print(json.dumps({"hojas": {h: {"page": v["pg"] + 1, "areas": v["n"], "sf": round(v["sf"], 2), "clusters": v["cl"]}
                                for h, v in por_hoja.items()}, "sin_poligono": falta, "sin_hatch": sinh}, ensure_ascii=False))
    return 1 if falta or sinh else 0



# ---------------------------------------------------------------------------------------------------------------------------
# U-160 (usuario 10-nov: "a los room que no marques nada escribe la razon sobre el ese mismo"): EXCLUDED sobre cada cuarto excluido.
# Uso: python3 markups_rcp.py excluded <markups.pdf> <rcp_cuartos.json> [--out <pdf>]
import tempfile as _tempfile
import pymupdf as fitz

SUBJ = "EXCLUDED"
ROJO = (0.85, 0.0, 0.0)
GRIS = (0.45, 0.45, 0.45)


def texto(r):
    return f"EXCLUDED - {str(r.get('reason') or '').strip().rstrip('.')} ({r.get('nhoja')})"


def exclusiones(cuartos):
    return [r for r in (cuartos.get("rooms") or []) if r.get("disposition") == "exclusion"]


def _dentro(poly, x, y):
    """punto en polígono (ray casting)."""
    n, ok = len(poly), False
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / ((y2 - y1) or 1e-9) + x1:
            ok = not ok
    return ok


def frac_dentro(rect, poly, n=12):
    """U-160 (rev15): fracción de la caja del texto que cae dentro del polígono del cuarto (muestreo n x n)."""
    x0, y0, x1, y1 = rect
    pts = [(x0 + (x1 - x0) * (i + .5) / n, y0 + (y1 - y0) * (j + .5) / n) for i in range(n) for j in range(n)]
    return sum(1 for q in pts if _dentro(poly, *q)) / float(len(pts))


def _choca(caja, evitar):
    x0, y0, x1, y1 = caja
    return any(not (x1 <= e[0] or e[2] <= x0 or y1 <= e[1] or e[3] <= y0) for e in evitar or [])


def caja_interior(poly, margen=0.06, evitar=None):
    """rectángulo grande dentro del polígono: centro = punto interior (rejilla), crece hasta tocar el borde; con 'evitar' (cajas del texto
    impreso de la hoja) no se monta sobre notas / números de cuarto (rev15 F03: 410 tapaba 'SEE ENLARGED RCP'). Si no hay lugar libre,
    se usa la caja sin evitar."""
    if evitar:
        try:
            b = caja_interior(poly, margen, None)
            xs_, ys_ = [q[0] for q in poly], [q[1] for q in poly]
            ev_ = [e for e in evitar if not (e[2] < min(xs_) or e[0] > max(xs_) or e[3] < min(ys_) or e[1] > max(ys_))]
            if ev_:
                return _caja_interior(poly, margen, ev_, minimo=0.15 * (b[2] - b[0]) * (b[3] - b[1])) or b
            return b
        except Exception:
            pass
    return _caja_interior(poly, margen, None)


def _caja_interior(poly, margen=0.06, evitar=None, minimo=0.0):
    xs, ys = [q[0] for q in poly], [q[1] for q in poly]
    bx0, by0, bx1, by1 = min(xs), min(ys), max(xs), max(ys)
    mejor, best = None, -1.0
    for i in range(1, 30):
        for j in range(1, 30):
            x, y = bx0 + (bx1 - bx0) * i / 30, by0 + (by1 - by0) * j / 30
            if not _dentro(poly, x, y) or _choca((x - .5, y - .5, x + .5, y + .5), evitar):
                continue
            hw, hh = 0.5, 0.5
            for _ in range(400):   # crece en x y en y por separado mientras toda la caja quede dentro (y sin texto impreso)
                g = False
                c_ = (x - hw * 1.06, y - hh, x + hw * 1.06, y + hh)
                if frac_dentro(c_, poly, 8) >= 1.0 and not _choca(c_, evitar):
                    hw *= 1.06; g = True
                c_ = (x - hw, y - hh * 1.06, x + hw, y + hh * 1.06)
                if frac_dentro(c_, poly, 8) >= 1.0 and not _choca(c_, evitar):
                    hh *= 1.06; g = True
                if not g:
                    break
            if hw * hh > best:
                best, mejor = hw * hh, (x, y, hw, hh)
    if mejor is None or 4 * best < minimo:
        return None
    x, y, hw, hh = mejor
    hw, hh = hw * (1 - margen), hh * (1 - margen)
    return (x - hw, y - hh, x + hw, y + hh)


def _ajustar(t, w, h):
    """(fontsize, texto con saltos) que cabe en w x h; multi-línea, letra de 7 pt hacia abajo hasta 1.6 pt (vector: legible con zoom)."""
    for fs in [7.0, 6.0, 5.5, 5.0, 4.5, 4.0, 3.5, 3.0, 2.6, 2.2, 1.9, 1.6]:
        cw = fs * 0.52; por = max(1, int((w - 2) / cw)); ln, cur = [], ""
        for pal in t.split():
            if len(pal) > por:
                pal = pal[:por]
            if cur and len(cur) + 1 + len(pal) > por:
                ln.append(cur); cur = pal
            else:
                cur = (cur + " " + pal).strip()
        ln.append(cur)
        if len(ln) * fs * 1.22 + 2 <= h:
            return fs, "\n".join(ln)
    return None, None


def aplicar(pdf, cuartos, out=None):
    """U-160 (rev15, revisión completa rev14 F02/F03/F08): cada exclusión = polígono gris del cuarto (OBLIGATORIO) + FreeText rojo
    DENTRO del cuarto (caja interior, multi-línea / letra reducida), sin línea de callout /CL. Sin polígono = falta."""
    doc = fitz.open(pdf)
    paginas = {(p.get_label() or "").strip(): p for p in doc}
    hechos, faltan = [], []
    for r in exclusiones(cuartos):
        p = paginas.get(str(r.get("draw_sheet") or r.get("sheet")))   # rev15: draw_sheet = vista RCP de otra hoja (p. ej. 1/A3.01)
        poly = r.get("polygon")
        if p is None or not poly or len(poly) < 3:
            faltan.append(f"{r.get('sheet')} {r.get('room')}: sin página o sin polígono del cuarto (U-160: polígono obligatorio)")
            continue
        t = texto(r)
        DR, RM = p.derotation_matrix, p.rotation_matrix   # BE-GK16: polygon in VISIBLE pt; annotations live in the unrotated page space
        if any(a.info.get("subject") == SUBJ and a.info.get("content") == t and a.type[1] == "FreeText"
               and frac_dentro(tuple(a.rect * RM), poly) >= 0.9 for a in p.annots() or []):
            hechos.append((r["sheet"], r["room"]))
            continue
        a = p.add_polygon_annot([fitz.Point(x, y) * DR for x, y in poly])
        a.set_colors(stroke=GRIS, fill=GRIS)
        a.set_opacity(0.25)
        a.set_border(width=1.0, dashes=[3, 3])
        a.set_info(title="Take-off excluded", subject=SUBJ,
                   content=t + (f" [EDGE NOT DRAWN: {r['edge_not_drawn']}]" if r.get("edge_not_drawn") else ""))
        a.update()
        txt_imp = [tuple(fitz.Rect(b[:4]) * RM) for b in p.get_text("blocks") if str(b[4]).strip()]
        # BE-CR36 (CR rev19, U-187): tampoco encima de otro FreeText ya puesto en la hoja (dos cuartos vecinos: 118B / 119 en A7.50)
        txt_imp += [tuple(fitz.Rect(an.rect * RM) + (-2, -2, 2, 2)) for an in p.annots() or [] if an.type[1] == "FreeText"]
        x0, y0, x1, y1 = caja_interior(poly, evitar=txt_imp)
        fs, tt = _ajustar(t, x1 - x0, y1 - y0)
        if fs is None:
            faltan.append(f"{r.get('sheet')} {r.get('room')}: el texto no cabe dentro del cuarto ni a 1.6 pt")
            continue
        alto = len(tt.split("\n")) * fs * 1.22 + 2
        cy = (y0 + y1) / 2
        rect = fitz.Rect(x0, cy - alto / 2, x1, cy + alto / 2)
        a = p.add_freetext_annot(rect * DR, tt, fontsize=fs, text_color=ROJO, fill_color=None, align=1, rotate=p.rotation)   # sin relleno: no tapa notas impresas (F03 410)
        a.set_border(width=0)
        a.set_info(title="Take-off excluded", subject=SUBJ, content=t)
        a.update()
        for k in ("CL", "LE", "IT"):          # sin callout: ninguna línea sale del texto (F08)
            if doc.xref_get_key(a.xref, k)[0] != "null":
                doc.xref_set_key(a.xref, k, "null")
        r["text_rect"] = [round(v, 2) for v in rect]
        hechos.append((r["sheet"], r["room"]))
    leg = paginas.get("LEGEND")
    if leg is not None and hechos and not any(a.info.get("subject") == SUBJ for a in leg.annots() or []):
        ys = [a.rect.y1 for a in leg.annots() or []]
        y0 = (max(ys) if ys else 60) + 18
        a = leg.add_freetext_annot(fitz.Rect(40, y0, 520, y0 + 24),
                                   "EXCLUDED - room not quantified; the red text on the room gives the printed reason and its sheet "
                                   "(grey hatch = room outline, no quantity)", fontsize=8, text_color=ROJO)
        a.set_info(title="Take-off legend", subject=SUBJ, content="EXCLUDED legend")
        a.update()
    dst = out or pdf
    tmp = _tempfile.mktemp(suffix=".pdf", dir=os.path.dirname(os.path.abspath(dst)))
    mb.nm_unicos(doc, pref="EXCL")                           # U-167: EXCLUDED con /NM único (antes fitz-A0... repetido)
    doc.save(tmp, garbage=3, deflate=True)
    doc.close()
    os.replace(tmp, dst)
    return hechos, faltan


def contar(pdf):
    """{hoja: n FreeText EXCLUDED} del PDF."""
    d = fitz.open(pdf)
    out = {}
    for p in d:
        n = sum(1 for a in p.annots() or [] if a.info.get("subject") == SUBJ and a.type[1] == "FreeText"
                and a.info.get("content") != "EXCLUDED legend")
        if n:
            out[(p.get_label() or "").strip()] = n
    return out



if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "excluded":
        _a = sys.argv[2:]
        _h, _f = aplicar(_a[0], json.load(open(_a[1])), _a[_a.index("--out") + 1] if "--out" in _a else None)
        print(len(_h), "EXCLUDED markups;", "faltan", _f)
        sys.exit(1 if _f else 0)
    if len(sys.argv) != 6:
        print(__doc__)
        sys.exit(2)
    sys.exit(escribir(*sys.argv[1:]))
