#!/usr/bin/env python3
"""markups_demo.py — R80e.118 (usuario, 02-nov-2026, VS #679 Downey): la DEMOLICIÓN se marca con LÍNEA a escala.

Agrega al PDF de markups (salida de markups_bluebeam.py) una anotación PolyLine REAL por elemento de demolición
(partition demolida, column enclosure, furring, board de demising), en la hoja del demolition plan:
  Subject "DEMO", color propio (rojo-naranja, trazo discontinuo), /Measure con la escala calibrada de la hoja
  (Bluebeam muestra Length en ft), /Depth = altura del elemento (Bluebeam calcula Wall Area = Length x Depth),
  contents = "DEMO <id> · <LF> LF · H <h> ft (<estado>) · <SF> SF · <keynote> <hoja>" (U-143: sin capas).
Además escribe una imagen PNG por hoja con las líneas y etiquetas (evidencia visual, mismo estilo que planmark).

Entrada: demo_geom.json = [{id, group, page (1-based), polyline [[x, y], ...] (coordenadas de la página TAL COMO SE
VE, pymupdf page.rect), lf, h_ft, h_status, layers, sf, keynote, sheet}] + pt_per_ft de la hoja.
Uso:
  python3 markups_demo.py <markups.pdf> <demo_geom.json> <pt_per_ft> <salida.pdf> <dir_png>
Sale rc 0 y un resumen JSON en stdout ({annots, sf_total, por_grupo}); rc 1 si un elemento no tiene geometría.
"""
import json
import re
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import markups_bluebeam as mb  # noqa: E402

DEMO_RGB = (0.90, 0.30, 0.0)
DASH = (6, 3)


def _len_pt(pts):
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))


GIRO_MAX = 60.0       # v81cf28 (U-120 / BE-CF21): una polilínea que dobla más de 60° junta dos ejes -> una pieza por eje


def es_area(e):
    """v81cf28 (U-121 / BE-CF21): demo de CIELO / área (h 0, 'n/a (area)', contorno cerrado) = Polygon de área, no Polylength."""
    pts = e.get("polyline") or []
    cerrado = len(pts) >= 4 and math.dist(pts[0], pts[-1]) < 0.5
    return cerrado and not float(e.get("h_ft") or 0) and (str(e.get("group")) == "ceilings" or "area" in str(e.get("h_status")))


def piezas_por_eje(pts):
    """[[pts del eje 1], [pts del eje 2], ...]: corta la polilínea en cada vértice con giro > GIRO_MAX (tramos < 3 pt no)."""
    out, cur = [], [pts[0]]
    for i in range(1, len(pts)):
        cur.append(pts[i])
        if i < len(pts) - 1:
            a = (pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1])
            b = (pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
            la, lb = math.hypot(*a), math.hypot(*b)
            if la >= 3 and lb >= 3:
                g = math.degrees(math.acos(max(-1.0, min(1.0, (a[0] * b[0] + a[1] * b[1]) / (la * lb)))))
                if g > GIRO_MAX:
                    out.append(cur)
                    cur = [pts[i]]
    out.append(cur)
    return [x for x in out if len(x) >= 2]


def escribir(pdf_in, geom, pt_per_ft, pdf_out, dir_png):
    import pymupdf as fitz  # noqa: F811
    els = json.load(open(geom, encoding="utf-8"))
    doc = fitz.open(pdf_in)
    out, malos = {"annots": 0, "sf_total": 0.0, "por_grupo": {}, "elementos": []}, []
    por_pag = {}
    for e in els:
        pts = e.get("polyline") or []
        if len(pts) < 2:
            malos.append(e.get("id"))
            continue
        pg = int(e["page"]) - 1
        page = doc[pg]
        h = float(e.get("h_ft") or 0)
        xid = e.get("xid") or e["id"]                  # R80e.134: id del desglose del Excel ("P03-N 1" = pieza de P03-N)
        det = e.get("detail") or f"{e.get('keynote', '')} {e.get('sheet', '')}"
        # R80e.134 / BE-117: formato estándar que verificar_markups_excel cuadra contra el Excel (DETAIL N/HOJA al final)
        # BE-HF15 (back-check O5): "2 faces x 1 layer" written as in the element (layers_info), not "2 layer(s)"
        m_l = re.match(r"\s*(\d+\s+faces?(?:\s*x\s*\d+\s+layers?)?)", str(e.get("layers_info") or ""), re.I)
        lay = m_l.group(1) if m_l else f"{e.get('layers')} layer(s)"
        # U-143 (usuario 5-nov): demolición = solo SF del elemento; el markup no lleva capas / caras / materiales
        if es_area(e):
            # v81cf28: área de cielo demolido = Polygon con /Measure de área (Bluebeam: Area en SF), sin LF ni Depth
            txt = (f"DEMO · {float(e.get('sf') or 0):,.2f} SF · {e.get('keynote', '')} {e.get('h_status', '')} · {xid} · {det}")
            M = page.derotation_matrix
            a = page.add_polygon_annot([fitz.Point(x, y) * M for x, y in pts[:-1]])
            a.set_info(title="take-off", subject="DEMO", content=txt)
            a.set_colors(stroke=DEMO_RGB, fill=DEMO_RGB)
            a.set_border(width=mb.ANCHO, dashes=list(DASH))
            a.set_opacity(0.30)
            a.update()
            mb._nm(doc, a, f"DEMO-{xid}")
            mb._measure(doc, a, float(pt_per_ft))
            doc.xref_set_key(a.xref, "IT", "/PolygonDimension")
            doc.xref_set_key(a.xref, "MeasurementTypes", "129")
            out["annots"] += 1
        else:
            ps = piezas_por_eje([tuple(p) for p in pts])
            tot = _len_pt(pts) or 1.0
            for k, pz in enumerate(ps, 1):
                # una pieza por eje (U-120): LF y SF repartidos por largo dibujado; el grupo suma el renglón del Excel
                f_ = _len_pt(pz) / tot if len(ps) > 1 else 1.0
                xk = f"{xid} {k}" if len(ps) > 1 else xid
                txt = (f"DEMO · {float(e.get('lf') or 0) * f_:.2f} LF · H {mb.ftin(h)} · "
                       f"{float(e.get('sf') or 0) * f_:,.2f} SF · {e.get('keynote', '')} {e.get('h_status', '')} · {xk} · {det}")
                a = mb._annot(doc, page, pz, DEMO_RGB, DASH, "DEMO", txt, "take-off", f"DEMO-{xk}")
                mb._measure(doc, a, float(pt_per_ft))
                if h:
                    mb._depth(doc, a, h)
                out["annots"] += 1
        sf = float(e.get("sf") or 0)
        out["sf_total"] += sf
        g = out["por_grupo"].setdefault(e.get("group", "other"), {"n": 0, "lf": 0.0, "sf": 0.0})
        g["n"] += 1
        g["lf"] += float(e.get("lf") or 0)
        g["sf"] += sf
        out["elementos"].append({"id": e["id"], "page": e["page"], "len_measured_ft": round(_len_pt(pts) / float(pt_per_ft), 2),
                                 "lf": e.get("lf"), "sf": sf})
        por_pag.setdefault(pg, []).append(e)
    # R80e.134: Page Label = número de hoja en las páginas de demo (columna Page Label de Bluebeam / verificador)
    try:
        reglas = [r for r in (doc.get_page_labels() or [])]
        hojas = {int(e["page"]) - 1: e.get("sheet") for e in els if e.get("sheet")}
        ya = {r["startpage"] for r in reglas}
        for pg_, sh in hojas.items():
            if pg_ in ya:
                continue
            prev = max((r for r in reglas if r["startpage"] < pg_), key=lambda r: r["startpage"], default=None)
            reglas.append({"startpage": pg_, "prefix": str(sh), "style": "", "firstpagenum": 1})
            if pg_ + 1 < doc.page_count and (pg_ + 1) not in ya:
                if prev and prev.get("style"):
                    reglas.append({"startpage": pg_ + 1, "prefix": prev.get("prefix", ""), "style": prev["style"],
                                   "firstpagenum": prev.get("firstpagenum", 1) + (pg_ + 1 - prev["startpage"])})
        doc.set_page_labels(sorted(reglas, key=lambda r: r["startpage"]))
    except Exception:                                  # noqa: BLE001
        pass
    doc.save(pdf_out, garbage=3, deflate=True)
    # PNG por hoja: líneas + etiqueta corta
    os.makedirs(dir_png, exist_ok=True)
    src = fitz.open(pdf_in)
    for pg, es in por_pag.items():
        page = src[pg]
        z = 100 / 72.0
        pix = page.get_pixmap(dpi=100)
        from PIL import Image, ImageDraw
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        d = ImageDraw.Draw(im)
        for e in es:
            q = [(x * z, y * z) for x, y in e["polyline"]]
            d.line(q, fill=(230, 77, 0), width=5)
            x0, y0 = q[0]
            lab = f"{e['id']} {e.get('lf')} LF x {e.get('h_ft')} = {e.get('sf')} SF"
            d.rectangle([x0, y0 - 18, x0 + 7 * len(lab), y0], fill=(255, 255, 255), outline=(230, 77, 0))
            d.text((x0 + 3, y0 - 16), lab, fill=(200, 50, 0))
        sh = es[0].get("sheet", f"p{pg + 1}")
        d.rectangle([10, 10, 900, 44], fill=(255, 255, 255), outline=(0, 0, 0))
        d.text((18, 20), f"{sh} DEMO - {len(es)} elements, {round(sum(float(x.get('sf') or 0) for x in es), 2)} SF "
                         f"(line = element measured to scale)", fill=(0, 0, 0))
        im.save(os.path.join(dir_png, f"{sh}_DEMO.png"))
    out["sf_total"] = round(out["sf_total"], 2)
    for g in out["por_grupo"].values():
        g["lf"], g["sf"] = round(g["lf"], 2), round(g["sf"], 2)
    out["sin_geometria"] = malos
    return out


def main(argv):
    if len(argv) != 6:
        print(__doc__)
        return 2
    r = escribir(argv[1], argv[2], argv[3], argv[4], argv[5])
    print(json.dumps({k: v for k, v in r.items() if k != "elementos"}, ensure_ascii=False))
    return 1 if r["sin_geometria"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
