#!/usr/bin/env python3
"""revision_markups.py (R80e.136, 3-nov-2026) — REVISIÓN RÁPIDA de markups Bluebeam vs Excel, por PROGRAMA.

Para que el estimador no tenga que revisar wall por wall en Bluebeam. Lee el PDF de markups (annots Line/PolyLine
con /Contents "TYPE · LF · H · SF · DETAIL · Wall ID", /Depth, /Subject) y el Excel de formato fijo (hoja Partition
Takeoff) y, por cada markup de wall:
  (a) LF re-medido desde la geometría con la escala IMPRESA de la hoja (--scale A1.1=1/8) vs LF del Excel y del texto
      de la etiqueta (tolerancia ±0.5 %);
  (b) Depth del markup vs H del Excel (exacta, ±0.001 ft) y H de la etiqueta; cita de la fuente de la altura (canon,
      height_source + estado) — una altura PENDIENTE se marca;
  (c) Wall Area = LF × H: etiqueta vs Excel (±0.5 %);
  (d) Wall ID y TYPE iguales al Excel.
Filas del Excel que agrupan varios walls ("S42-01+S42-02") se comparan contra la SUMA de sus markups (LF) y contra la
H de cada segmento en el canon (la H de la fila es ponderada).
Salidas en <out>: revision_markups.xlsx + .md (VERDE / ROJA, orden del partition schedule), img/ROJA_<id>.png
(recorte circulado de cada fila roja) y mapa_alturas_<hoja>.png (cada wall pintado por su altura, leyenda, Wall ID).

Test: python3 revision_markups.py --selftest (corre desde test_markups_excel.py).
R80e.138 (BE-119): la H se compara contra la altura IMPRESA que cita la fuente (canon height_source), no contra el Excel; sin
altura impresa o con supuesto (RFI) = AMBER con las hojas citadas.
Uso: python3 revision_markups.py markups.pdf takeoff.xlsx out_dir --scale A1.1=1/8 [--canon takeoff_canon.json]
     [--order S21,S24,...] [--title "Project"]
"""
import argparse
import colorsys
import json
import math
import os
import re
import sys
from fractions import Fraction

TOL_LF = 0.005
TOL_H = 0.001


def ftin(s):
    """14'-10.125" -> 14.84375 ; 8.5 -> 8.5"""
    s = str(s).strip()
    m = re.match(r"^(\d+)'\s*-?\s*([\d.]+)?\"?$", s)
    if m:
        return int(m.group(1)) + float(m.group(2) or 0) / 12
    return float(s)


HOJA_RX = re.compile(r"\b(?:\d{1,2}[A-Z]?/)?[A-Z]{1,3}-?\d{1,3}(?:\.\d{1,2})?(?:\.?[A-Z])?\b")   # U-138 (Chuze): A421, A435.A, A-301
_FI = r"(\d+)'\s*-?\s*(\d+(?:\.\d+)?)?(?:\s+(\d+)/(\d+))?\""


def _fi(m, k=1):
    ft, inch, a, b = m.group(k), m.group(k + 1), m.group(k + 2), m.group(k + 3)
    return int(ft) + (float(inch or 0) + (int(a) / int(b) if a else 0)) / 12


def datum_ff(canon):
    """Elevación impresa del FINISH FLOOR del set (p. ej. 'FINISH FLOOR EL. 100'-0"'), tomada de las citas del canon."""
    for w in (canon or {}).get("walls") or []:
        m = re.search(r"FINISH FLOOR EL\.\s*" + _FI, str(w.get("height_source") or ""), re.I)
        if m:
            return _fi(m)
    return None


CAUSA_KEYS = ("length_cause", "area_cause", "measure_cause", "markup_cause")   # = verificar_markups_excel
_TOK = re.compile(r"(\d+)'\s*-?\s*(\d+(?:\.\d+)?)?(?:\s+(\d+)/(\d+))?\"?|(\d+(?:\.\d+)?)\"|(\d+(?:\.\d+)?)\s*ft\b|(\d+\.\d+)")


def _tok_ft(m):
    if m.group(1) is not None:
        return _fi(m)
    if m.group(5) is not None:
        return float(m.group(5)) / 12
    return float(m.group(6) if m.group(6) is not None else m.group(7))


def _op(seg):
    """texto entre dos operandos impresos -> '+', '-', 'R' (de A a B = B - A) o None (no es una operación)."""
    t = " " + re.sub(r"\b[A-Z]{1,3}-?\d{1,3}(?:\.\d{1,2})?[A-Z]?\b", " ", seg).lower() + " "
    if re.search(r"\bto\b", t):
        return "R"
    if "+" in t or re.search(r"\babove\b|\bplus\b", t):
        return "+"
    if re.search(r"\s-\s|\bminus\b|\bbelow\b", t):
        return "-"
    return None


def _derivada(t):
    """v81cf25 (CFA rev5, BE-119): altura DERIVADA de valores IMPRESOS con su operación escrita en la cita
    ('C.H. <a> + <b> = <h> ft', '<b> above C.H. <a> - <c> base = <h> ft', 'from C.H. <a> to B.O. <b> = <h>'). El programa REHACE la
    operación con los operandos impresos (izquierda a derecha, cada tramo que termina en el último operando) y solo la acepta
    si da el resultado escrito -> h | None."""
    for eq in reversed(list(re.finditer(r"=\s*", t))):
        rhs = _TOK.match(t, eq.end())
        if not rhs:
            continue
        res = _tok_ft(rhs)
        cl = re.split(r"[;|\[]|->", t[:eq.start()])[-1]
        cl = re.sub(r"\([^()]*\)", " ", cl)
        ts = list(_TOK.finditer(cl))
        vals = [_tok_ft(m) for m in ts]
        for a in range(len(ts)):
            acc, ok = vals[a], True
            for k in range(a + 1, len(ts)):
                op = _op(cl[ts[k - 1].end():ts[k].start()])
                if op is None:
                    ok = False
                    break
                acc = acc + vals[k] if op == "+" else (acc - vals[k] if op == "-" else vals[k] - acc)
            if ok and abs(acc - res) < 0.01:
                return round(res, 4)
    return None


def altura_impresa(src, status="", ff=None):
    """R80e.138 (BE-119): altura IMPRESA que cita la fuente de la altura (no la H del Excel) -> (h_ft | None, regla, hojas).
    Orden: 'TO x'-y" A.F.F.' · 'EL. a ... to ... EL. b' (diferencia de elevaciones impresas) · cota x'-y" impresa.
    Una altura que depende de un supuesto (PENDIENTE / assumed / RFI) devuelve None con regla 'assumption'."""
    t = str(src or "")
    hojas = sorted(set(HOJA_RX.findall(t)))
    if "PENDIENTE" in str(status).upper() or re.search(r"\[PENDIENTE\]|assumed|not printed", t, re.I):
        return None, "assumption", hojas
    m = re.search(r"\bTO\s+(\d+(?:\.\d+)?)\"\s*A\.?F\.?F", t, re.I)       # v81cf25: 'to 18" A.F.F.' (pulgadas)
    if m:
        return round(float(m.group(1)) / 12, 4), "A.F.F. note", hojas
    m = re.search(r"\bTO " + _FI + r"\s*A\.F\.F", t, re.I)
    if m:
        return round(_fi(m), 4), "A.F.F. note", hojas
    els = list(re.finditer(r"\bEL\b\.?\s*" + _FI, t))   # R80e.142: "EL 111'-4\"" sin punto también es elevación
    if len(els) >= 2:
        return round(abs(_fi(els[-1]) - _fi(els[0])), 4), "printed elevations", hojas
    # BE-GK28 (Grand Kia): vector measurement on the section at the printed scale "(Y1-Y0)/k = h" (the LAST one before the
    # first '|' is the result; intermediate steps such as "xs = 1142.8-128.6 = 1014.2" are not the height); re-computed here
    seg = t.split("|")[0]
    # BE-CR32 (CR City Hotel rev19, unión v81cf91): "printed 8'-11 1/4\" ...; cross-check (523.4-282.1)/27 = 8.94" -> manda la cota
    # IMPRESA; una medición vectorial que solo comprueba (cross-check / check / verified) no la reemplaza
    mi = re.search(r"(?i)\bprinted\s+" + _FI, seg)
    if mi and re.search(r"(?i)cross[- ]?check|\bcheck\b|verified|confirm", seg[mi.end():]):
        return round(_fi(mi), 4), "printed dimension (vector cross-check does not replace it)", hojas
    ad = [m for m in re.finditer(r"(?<![\d.])(\d+\.?\d*)\s*\+\s*(\d+\.?\d*)\s*=\s*(\d+\.?\d*)(?![\d.])", seg)
          if abs(float(m.group(1)) + float(m.group(2)) - float(m.group(3))) <= 0.01]
    if ad and ad[-1].end() >= len(seg.rstrip(" ;,")) - 2:     # BE-GK28b: the operation ENDS with "C.H. + 0.5 = h" (A550 6" above ceiling)
        return round(float(ad[-1].group(3)), 4), "derived: printed operands, operation re-done by program", hojas
    vs = [m for m in re.finditer(r"\((\d+\.?\d*)\s*-\s*(\d+\.?\d*)\)\s*/\s*(\d+\.?\d*)\s*=\s*(\d+\.?\d*)", t.split("|")[0])
          if float(m.group(3)) > 0 and abs((float(m.group(1)) - float(m.group(2))) / float(m.group(3)) - float(m.group(4))) <= 0.01]
    if vs:
        return round(float(vs[-1].group(4)), 4), "derived: vector measurement at the printed scale, operation re-done by program", hojas
    hd = _derivada(t)                                  # v81cf26: después de las elevaciones impresas (R80e.142 manda)
    if hd is not None:
        return hd, "derived: printed operands, operation re-done by program", hojas
    if len(els) == 1 and ff is not None and re.search(r"FINISH FLOOR|F\.F\.", t, re.I):
        return round(_fi(els[0]) - ff, 4), "printed elevation above the printed F.F. datum", hojas
    for m in re.finditer(_FI, t):
        if re.match(r"\s*(wall|thick|deep|wide)", t[m.end():m.end() + 12], re.I):
            continue                                   # espesor / ancho de un wall, no una altura
        if re.search(r"\bEL\.?\s*$", t[max(0, m.start() - 6):m.start()], re.I):   # R80e.142: PANEL / LEVEL no
            continue                                   # una elevación sola (EL. 100'-0") no es una altura (BE-121)
        h = _fi(m)
        # R80f.29 (Chuze FINAL6): "12'-1\" AFF C-5 ... + 6\" (SKILL §7) = 12.58" -> printed ceiling + printed rule
        # increment; the chain is read up to its '=' / ';' (never past the result)
        cola = re.split(r"[=;|]", t[m.end():], maxsplit=1)[0]
        sumas = [int(x) for x in re.findall(r"\+\s*(\d{1,2})\s*\"", cola)]
        if sumas:
            return round(h + sum(sumas) / 12, 4), "printed dimension + printed rule", hojas
        return round(h, 4), "printed dimension", hojas
    return None, "no printed height in the citation", hojas


def escala_pt_per_ft(txt):
    """'1/8' (in = 1 ft) -> 9.0 pt/ft"""
    return float(Fraction(txt)) * 72


def _sf_parte(parts):
    """R80f.29 (Chuze FINAL6): the SF part of the label is the one that carries 'SF' (an EX board-only label has an extra
    'N face(s)' part); 'SF board' = board SF of the Excel row (BE-117, markups_bluebeam), plain 'SF' = LF x H."""
    # U-153 (v81cf60): "<LF x H> SF wall (LF\u00d7H)" va antes del "SF board": manda el SF board; sin board, el SF wall
    cand = [x for x in parts[3:-1] if re.search(r"\bSF\b", x)]
    cand = [x for x in cand if re.search(r"SF board", x)] or cand
    for x in cand:
        if True:
            try:
                return float(x.split()[0].replace(",", "")), bool(re.search(r"SF board", x))
            except ValueError:
                return float("nan"), False
    return float("nan"), False


def leer_markups(pdf):
    import pymupdf
    d = pymupdf.open(pdf)
    out = []
    for pi, p in enumerate(d):
        for a in p.annots() or []:
            if a.type[1] not in ("Line", "PolyLine"):
                continue
            c = (a.info.get("content") or "").strip()
            parts = [x.strip() for x in c.split("·")]
            if len(parts) < 6 or "LEGEND" in c:
                continue
            x = d.xref_object(a.xref)
            # pymupdf da los vértices en coordenadas de la página MOSTRADA (y hacia abajo); /Vertices crudo es y hacia arriba
            pts = [(float(q[0]), float(q[1])) for q in (a.vertices or [])]
            dep = re.search(r"/Depth ([\d.]+)", x)
            # v81cf25 (CFA rev5): los rótulos de board-only / demo traen un campo extra ('1 face(s)' / '2 layer(s)')
            # antes del SF y la demo cierra con su keynote ('KN3 A-050'): SF = el campo que dice SF, id = el último
            # campo sin espacios (Wall ID / DEMO ID)
            i_sf = next((k for k in range(3, len(parts)) if re.search(r"\bSF board\b", parts[k])),
                        next((k for k in range(3, len(parts)) if re.search(r"\bSF\b", parts[k])), 3))   # U-153: SF board manda
            # BE-CR11: un Wall ID con lado ('CH-L2-01 A', shaft wall por cara) también es id
            ids_ = [x for x in parts[i_sf + 1:] if x and (" " not in x or re.fullmatch(r"\S+-\w+ [A-Z]", x))]
            out.append({"page": pi, "label": p.get_label() or f"p{pi + 1}", "subject": a.info.get("subject"),
                        "type_txt": parts[0], "lf_txt": float(parts[1].split()[0].replace(",", "")),
                        "h_txt": ftin(parts[2].replace("H", "").strip()),
                        "sf_txt": float(parts[i_sf].split()[0].replace(",", "")), "detail_txt": parts[i_sf + 1] if i_sf + 1 < len(parts) else "",
                        "id": ids_[-1] if ids_ else parts[-1], "pts": pts, "sf_board": bool(re.search(r"(?i)SF board", parts[i_sf])),
                        "len_pt": sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)),
                        "depth": float(dep.group(1)) if dep else None, "rect": tuple(a.rect)})
    return d, out


def _mismo_bloque(mk, ex):
    """R80f.33: the Excel blocks OTHER FRAMING / BOARD ONLY carry a long header; their markups name the block plus the
    element ('OTHER FRAMING - SOFFIT SIDE', 'BOARD ONLY - NO FRAMING'): same block = same type."""
    for b in ("OTHER FRAMING", "BOARD ONLY"):
        if str(ex).upper().startswith(b) and str(mk).upper().startswith(b):
            return True
    return False


def leer_excel(xlsx):
    import openpyxl
    ws = openpyxl.load_workbook(xlsx, data_only=True)["Partition Takeoff"]
    rows, tipo, other = [], None, False
    for r in ws.iter_rows(min_row=5, values_only=True):
        a = str(r[0] or "")
        if a.startswith("TYPE "):
            tipo = a[5:].strip()
            other = "OTHER FRAMING" in a
            continue
        if r[1] and isinstance(r[2], (int, float)) and not str(r[1]).startswith(("SUBTOTAL", "TOTAL")):
            rows.append({"type": "OTHER FRAMING" if other else tipo, "wall": str(r[1]), "lf": float(r[2]),
                         "h": float(r[3]), "detail": r[9], "status": r[10],
                         "board": r[7] if isinstance(r[7], (int, float)) else None,
                         "board_sf": float(r[7]) if isinstance(r[7], (int, float)) else None})
    return rows


def revisar(pdf, xlsx, scales, canon=None, order=None):
    doc, mk = leer_markups(pdf)
    ex = leer_excel(xlsx)
    cw = {w["id"]: w for w in list((canon or {}).get("walls") or []) + list((canon or {}).get("existing_walls") or [])}
    ff = datum_ff(canon)
    by_id = {}
    for m in mk:                                  # R80f.37: los tramos rectos de un wall (U-120) se suman en uno
        if m["id"] in by_id:
            o = by_id[m["id"]]
            by_id[m["id"]] = dict(o, lf_txt=o["lf_txt"] + m["lf_txt"], len_pt=o["len_pt"] + m["len_pt"],
                                  sf_txt=o["sf_txt"] + m["sf_txt"], pts=o["pts"] + m["pts"])
        else:
            by_id[m["id"]] = m
    res = []
    for r in ex:
        ids = r["wall"].split("+")
        ms = [by_id.get(i) for i in ids]
        fallas, notas, amber, pr = [], [], [], []
        if any(m is None for m in ms):
            fallas.append("no markup for " + ", ".join(i for i, m in zip(ids, ms) if m is None))
            res.append(dict(r, verdict="RED", fallas=fallas, notas=notas, ids=ids, amber=[], printed=[]))
            continue
        lab = ms[0]["label"]
        sc = scales.get(lab)
        if sc is None:
            fallas.append(f"no printed scale given for sheet {lab}")
            lf_med = None
        else:
            lf_med = sum(m["len_pt"] for m in ms) / sc
        lf_txt = sum(m["lf_txt"] for m in ms)
        causa = next((str((cw.get(i) or {}).get(k)) for i in ids for k in CAUSA_KEYS if (cw.get(i) or {}).get(k)), None)
        if lf_med is not None and abs(lf_med - r["lf"]) / r["lf"] > TOL_LF:
            msg = f"LF measured {lf_med:.2f} vs Excel {r['lf']:.3f} ({(lf_med - r['lf']) / r['lf'] * 100:+.2f} %)"
            if causa:     # R80e.143: misma regla que verificar_markups_excel (BE-117): causa escrita en el canon = AMBER
                amber.append(f"{msg}; cause written: {causa[:140]}")
            else:
                fallas.append(msg)
        if abs(lf_txt - r["lf"]) / r["lf"] > TOL_LF:
            fallas.append(f"LF label {lf_txt:.2f} vs Excel {r['lf']:.3f}")
        hs = []
        for i, m in zip(ids, ms):
            h_ref = float(cw[i]["height_ft"]) if (len(ids) > 1 and i in cw) else r["h"]
            hs.append(h_ref)
            if m["depth"] is None:
                fallas.append(f"{i}: no Depth")
            elif abs(m["depth"] - h_ref) > TOL_H:
                fallas.append(f"{i}: Depth {m['depth']:.3f} vs H {h_ref:.3f}")
            if abs(m["h_txt"] - h_ref) > 1 / 96:
                fallas.append(f"{i}: label H {m['h_txt']:.3f} vs H {h_ref:.3f}")
            sf = float((cw.get(i) or {}).get("length_ft") or (r["lf"] if len(ids) == 1 else m["lf_txt"])) * h_ref
            # R80e.143: desde BE-117 (v81cf11) el SF del markup = board SF de la fila del Excel; LF x H queda para
            # markups viejos. Vale cualquiera de los dos; otro número = RED.
            bsf = r.get("board_sf") if len(ids) == 1 else None
            ok_sf = [x for x in (sf, bsf) if x is not None]
            if all(abs(m["sf_txt"] - x) > max(0.05 + 1e-9, TOL_LF * x) and abs(m["sf_txt"] - x) / max(x, 1e-6) > TOL_LF
                   for x in ok_sf) and not (len(ids) > 1 and r.get("board_sf") is not None):
                fallas.append(f"{i}: label SF {m['sf_txt']:.1f} vs LF x H {sf:.1f}"
                              + (f" / Excel board {bsf:.1f}" if bsf is not None else ""))
            if m["type_txt"] != r["type"] and not _mismo_bloque(m["type_txt"], r["type"]):
                fallas.append(f"{i}: TYPE {m['type_txt']} vs Excel {r['type']}")
            w = cw.get(i) or {}
            st = str(w.get("height_status") or "")
            src = str(w.get("height_source") or "")
            hp, regla, hojas = altura_impresa(src, st, ff)
            pr.append({"id": i, "h": hp, "rule": regla, "sheets": hojas})
            if hp is None:
                amber.append(f"{i}: no printed height to compare ({regla}; sheets cited {', '.join(hojas) or 'none'})"
                             + (" - depends on an RFI / assumption" if regla == "assumption" else ""))
            elif m["depth"] is not None and abs(m["depth"] - hp) > TOL_H:
                fallas.append(f"{i}: Depth {m['depth']:.3f} vs printed source H {hp:.3f} ({regla}, {', '.join(hojas)})")
            if src:
                notas.append(f"{i}: {src[:140]}")
        if len(ids) > 1 and all(m.get("sf_board") for m in ms) and r.get("board_sf") is not None:
            tot = sum(m["sf_txt"] for m in ms)
            if abs(tot - r["board_sf"]) > max(0.2, TOL_LF * r["board_sf"]):
                fallas.append(f"{r['wall']}: label SF board sum {tot:.1f} vs Excel Board (SF) {r['board_sf']:.1f}")
        res.append(dict(r, ids=ids, lf_measured=round(lf_med, 3) if lf_med is not None else None, lf_label=round(lf_txt, 3),
                        depth=[m["depth"] for m in ms], h_ref=hs, area=round(sum(m["lf_txt"] * h for m, h in zip(ms, hs)), 1),
                        verdict="RED" if fallas else ("AMBER" if amber else "GREEN"), fallas=fallas, notas=notas,
                        amber=amber, printed=pr, label=lab))
    rank = {t: k for k, t in enumerate(order or [])}
    res.sort(key=lambda x: (x["type"] == "OTHER FRAMING", rank.get(x["type"], len(rank)), x["type"], x["wall"]))
    return doc, mk, res


def recortes(doc, mk, res, out):
    import pymupdf
    by_id = {m["id"]: m for m in mk}
    os.makedirs(os.path.join(out, "img"), exist_ok=True)
    for r in res:
        if r["verdict"] != "RED":
            continue
        ms = [by_id[i] for i in r["ids"] if i in by_id]
        if not ms:
            continue
        p = doc[ms[0]["page"]]
        x0 = min(m["rect"][0] for m in ms); y0 = min(m["rect"][1] for m in ms)
        x1 = max(m["rect"][2] for m in ms); y1 = max(m["rect"][3] for m in ms)
        clip = pymupdf.Rect(x0 - 60, y0 - 60, x1 + 60, y1 + 60) & p.rect
        pix = p.get_pixmap(dpi=150, clip=clip, annots=True)
        from PIL import Image, ImageDraw
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        dr = ImageDraw.Draw(im)
        k = 150 / 72
        dr.ellipse([(x0 - clip.x0 - 20) * k, (y0 - clip.y0 - 20) * k, (x1 - clip.x0 + 20) * k, (y1 - clip.y0 + 20) * k],
                   outline=(255, 0, 0), width=4)
        dr.text((8, 8), f"{r['wall']}: " + "; ".join(r["fallas"])[:160], fill=(255, 0, 0))
        f = os.path.join(out, "img", f"RED_{r['wall'].replace('+', '_')}.png")
        im.save(f)
        r["img"] = os.path.relpath(f, out)


def mapa_alturas(doc, mk, canon, out, title):
    """Una imagen por hoja: cada wall pintado por su altura (canon height_ft o Depth), Wall ID, leyenda."""
    from PIL import Image, ImageDraw
    cw = {w["id"]: w for w in (canon or {}).get("walls") or []}
    files = []
    for pg in sorted({m["page"] for m in mk}):
        ms = [m for m in mk if m["page"] == pg]
        hs = sorted({round(float(cw.get(m["id"], {}).get("height_ft") or m["depth"] or 0), 3) for m in ms})
        col = {}
        for k, h in enumerate(hs):
            r, g, b = colorsys.hsv_to_rgb((k / max(len(hs), 1)) * 0.85, 0.9, 0.85)
            col[h] = (int(r * 255), int(g * 255), int(b * 255))
        p = doc[pg]
        dpi = 72
        pix = p.get_pixmap(dpi=dpi, annots=False)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples).convert("L").convert("RGB")
        im = Image.blend(im, Image.new("RGB", im.size, (255, 255, 255)), 0.55)
        dr = ImageDraw.Draw(im)
        for m in ms:
            h = round(float(cw.get(m["id"], {}).get("height_ft") or m["depth"] or 0), 3)
            pts = [(x, y) for x, y in m["pts"]]
            dr.line(pts, fill=col[h], width=7)
            cx = sum(x for x, _ in pts) / len(pts); cy = sum(y for _, y in pts) / len(pts)
            hp, regla, hojas = altura_impresa(cw.get(m["id"], {}).get("height_source"), cw.get(m["id"], {}).get("height_status"),
                                              datum_ff(canon))
            fuente = (hojas[0] if hojas else "no sheet") + ("" if hp is not None else " ASSUMED")
            dr.text((cx + 6, cy - 6), f"{m['id']} {h:.2f}' [{fuente}]", fill=col[h])
        lab = ms[0]["label"]
        y = 20
        dr.rectangle([15, 10, 470, 40 + 18 * (len(hs) + 2)], fill=(255, 255, 255), outline=(0, 0, 0))
        dr.text((25, y), f"{title} - sheet {lab} - wall heights (ft)", fill=(0, 0, 0)); y += 22
        for h in hs:
            n = sum(1 for m in ms if round(float(cw.get(m["id"], {}).get("height_ft") or m["depth"] or 0), 3) == h)
            dr.rectangle([25, y, 55, y + 12], fill=col[h])
            dr.text((65, y), f"{h:.3f} ft ({int(h)}'-{(h - int(h)) * 12:.2f}\")  - {n} wall(s)", fill=(0, 0, 0))
            y += 18
        f = os.path.join(out, f"height_map_{lab}.png")
        im.save(f)
        files.append(f)
    return files


def _pr(r):
    return " / ".join(f"{x['h']:.3f} ({x['rule']}, {', '.join(x['sheets'][:3])})" if x["h"] is not None
                      else f"n/a ({x['rule']})" for x in r.get("printed") or [])


def escribir(res, out, title, scales, maps):
    import openpyxl
    from openpyxl.styles import PatternFill, Font
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Markup review"
    ws.append([f"{title} - quick markup review (program: revision_markups.py)"])
    ws.append([f"Printed scales: {scales} · tolerance LF ±0.5 %, H exact (±0.001 ft) · GREEN = all checks pass"])
    hdr = ["Type", "Wall ID", "Excel LF", "Measured LF (printed scale)", "Label LF", "Excel H (ft)", "Depth (ft)",
           "Printed source H (ft) / rule / sheets", "Wall Area LF x H (SF)", "Detail", "Verdict", "Failures / amber",
           "Height source (citation)", "Image"]
    ws.append(hdr)
    for c in ws[3]:
        c.font = Font(bold=True)
    g, rd = PatternFill("solid", fgColor="C6EFCE"), PatternFill("solid", fgColor="FFC7CE")
    am = PatternFill("solid", fgColor="FFEB9C")
    for r in res:
        ws.append([r["type"], r["wall"], r["lf"], r.get("lf_measured"), r.get("lf_label"),
                   " / ".join(f"{h:.3f}" for h in r.get("h_ref") or [r["h"]]),
                   " / ".join(f"{d:.3f}" for d in r.get("depth") or [] if d is not None), _pr(r), r.get("area"),
                   r.get("detail"), r["verdict"], "; ".join(r["fallas"] + r.get("amber", [])), "; ".join(r["notas"]),
                   r.get("img", "")])
        ws.cell(ws.max_row, 11).fill = {"GREEN": g, "AMBER": am}.get(r["verdict"], rd)
    for col, wdt in zip("ABCDEFGHIJKLMN", (14, 16, 10, 14, 10, 14, 14, 30, 14, 14, 9, 60, 70, 28)):
        ws.column_dimensions[col].width = wdt
    wb.save(os.path.join(out, "markup_review.xlsx"))
    n_g = sum(r["verdict"] == "GREEN" for r in res)
    n_a = sum(r["verdict"] == "AMBER" for r in res)
    L = [f"# {title} — quick markup review", "",
         f"Program: revision_markups.py · printed scales {scales} · LF ±0.5 %, H exact vs the PRINTED source height · "
         f"GREEN {n_g} / AMBER {n_a} / RED {len(res) - n_g - n_a}", "",
         "| Type | Wall ID | Excel LF | Measured LF | Excel H | Depth | Printed source H | Area SF | Verdict | Failures / amber |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for r in res:
        L.append(f"| {r['type']} | {r['wall']} | {r['lf']:.3f} | {r.get('lf_measured')} | "
                 f"{' / '.join(f'{h:.3f}' for h in r.get('h_ref') or [r['h']])} | "
                 f"{' / '.join(f'{d:.3f}' for d in r.get('depth') or [] if d is not None)} | {_pr(r)} | {r.get('area')} | "
                 f"{ {'GREEN': '🟢 GREEN', 'AMBER': '🟠 AMBER'}.get(r['verdict'], '🔴 RED')} | "
                 f"{'; '.join(r['fallas'] + r.get('amber', []))} |")
    L += ["", "Height maps: " + ", ".join(os.path.basename(m) for m in maps)]
    open(os.path.join(out, "markup_review.md"), "w").write("\n".join(L) + "\n")
    return n_g


def _selftest_imports():
    pass


import subprocess
import tempfile


def _selftest():
    d = tempfile.mkdtemp()
    pdf, xlsx, out = os.path.join(d, "m.pdf"), os.path.join(d, "t.xlsx"), os.path.join(d, "out")
    doc = pymupdf.open()
    p = doc.new_page(width=2592, height=1728)
    doc.set_page_labels([{"startpage": 0, "prefix": "A1.1", "style": "", "firstpagenum": 1}])
    # escala impresa 1/8" = 1'-0" -> 9 pt/ft
    for wid, x0, length_ft, h_lbl, depth in (("W-1", 100, 20.0, "10'-0\"", 10.0), ("W-2", 400, 10.2, "8'-0\"", 9.0)):
        a = p.add_polyline_annot([(x0, 200), (x0 + length_ft * 9, 200)])
        lf = 20.0 if wid == "W-1" else 10.0
        h = 10.0 if wid == "W-1" else 8.0
        a.set_info(content=f"A1 · {lf:.2f} LF · H {h_lbl} · {lf * h:,.1f} SF · 1/A5.1 · {wid}", subject="A1")
        a.update()
        doc.xref_set_key(a.xref, "Depth", str(depth))
    doc.save(pdf)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Partition Takeoff"
    for _ in range(4):
        ws.append([None])
    ws.append(["TYPE A1"])
    ws.append(["A1 #W-1", "W-1", 20.0, 10.0, 1, "3-5/8\"", 16, 200, "x", "1/A5.1", "[CONFIRMED]"])
    ws.append(["A1 #W-2", "W-2", 10.0, 8.0, 1, "3-5/8\"", 16, 80, "x", "1/A5.1", "[CONFIRMED]"])
    wb.save(xlsx)
    canon = os.path.join(d, "c.json")
    json.dump({"walls": [{"id": "W-1", "height_ft": 10.0, "height_source": "A1 'STUDS TO 10'-0\" A.F.F.' (1/A5.1)"},
                         {"id": "W-2", "height_ft": 8.0, "height_source": "A1 'STUDS TO 8'-6\" A.F.F.' (1/A5.1)"}]},
              open(canon, "w"))
    r = subprocess.run([sys.executable, os.path.abspath(__file__), pdf, xlsx, out, "--scale", "A1.1=1/8", "--canon", canon],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert "GREEN 1 / AMBER 0 / RED 1" in r.stdout, r.stdout
    assert "vs printed source H 8.500" in r.stdout, r.stdout          # R80e.138: Depth vs altura IMPRESA
    assert altura_impresa("EL. 100'-0\" to T.O. METAL STUD EL. 120'-8\"") [0] == 20.6667
    assert altura_impresa("x [PENDIENTE] assumed 8\" purlin")[1] == "assumption"
    assert altura_impresa("T.O. EL. 100'-0\" (1/A3.1)")[0] is None        # BE-121: elevación sola != altura
    assert altura_impresa("(same 1'-2\" wall): FINISH FLOOR to T.O. EL. 120'-8\"", ff=100.0)[0] == 20.6667
    assert "RED W-2" in r.stdout and "LF measured" in r.stdout and "Depth 9.000 vs H 8.000" in r.stdout, r.stdout
    assert os.path.exists(os.path.join(out, "height_map_A1.1.png"))
    assert os.path.exists(os.path.join(out, "img", "RED_W-2.png"))
    print("OK selftest revision_markups")




def main():
    if sys.argv[1:] == ["--selftest"]:
        import openpyxl, pymupdf  # noqa: F401
        globals().update(openpyxl=openpyxl, pymupdf=pymupdf)
        _selftest()
        return 0
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf"); ap.add_argument("xlsx"); ap.add_argument("out")
    ap.add_argument("--scale", action="append", default=[], help="SHEET=1/8 (printed scale, inches = 1 ft)")
    ap.add_argument("--canon"); ap.add_argument("--order"); ap.add_argument("--title", default="Take-off")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    scales = {s.split("=")[0]: escala_pt_per_ft(s.split("=")[1]) for s in a.scale}
    canon = json.load(open(a.canon)) if a.canon else None
    doc, mk, res = revisar(a.pdf, a.xlsx, scales, canon, (a.order or "").split(",") if a.order else None)
    recortes(doc, mk, res, a.out)
    maps = mapa_alturas(doc, mk, canon, a.out, a.title)
    n_g = escribir(res, a.out, a.title, {k: f"{v:.3f} pt/ft" for k, v in scales.items()}, maps)
    json.dump(res, open(os.path.join(a.out, "markup_review.json"), "w"), indent=1, default=str)
    n_a = sum(r["verdict"] == "AMBER" for r in res)
    print(f"GREEN {n_g} / AMBER {n_a} / RED {len(res) - n_g - n_a}")
    for r in res:
        if r["verdict"] == "RED":
            print(f"RED {r['wall']}: {'; '.join(r['fallas'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
