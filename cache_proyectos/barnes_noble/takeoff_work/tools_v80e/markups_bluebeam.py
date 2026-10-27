#!/usr/bin/env python3
"""markups_bluebeam.py — v78 (W3, decisión del usuario): PDF de MARKUPS por wall, entregable FIJO de todo take-off.

Qué hace: copia el bid set y escribe, por cada wall del canon con geometría, una ANOTACIÓN PDF REAL (PolyLine o
Line, editable; nunca una imagen rasterizada) sobre el eje del wall en la hoja de planta donde se midió, para que
aparezca en el Markups List de Bluebeam y se pueda revisar / editar / medir:
  - Subject  = partition type (particion.tipo: tag, EXT-<stud>CFMF, EXT-PARAPET, BULKHEAD-<familia>, CANOPY-COL);
               elementos no-partition (partition_types.OTHER) = "OTHER FRAMING";
  - Contents = "TYPE · LF · H · SF · N/HOJA · id"   (v80e: H = altura del canon, SF = LF x H; sin altura = PENDING;
               N/HOJA = el detalle que trae el canon; sin detalle, la hoja); /Measure con la escala de la hoja
               (constants.plan_scale_pt_per_ft) para que Bluebeam mida Length a escala;
  - Author (/T) = "Take-off"; /NM = "TO-<id>" (la llave con la que `verificar` empareja wall ↔ annot);
  - color por type con PALETA FIJA y determinista (types ordenados alfabéticamente → PALETA[i]; OTHER FRAMING
    siempre lavanda con punteado largo; más types que colores → se repite el color con punteado corto).
Geometría (convención de band, v70; coordenadas en pt de la página MOSTRADA, rotada, como el PNG):
  H  : eje y = (c0 + c1) / 2 de x = lo a x = hi        (p0 / p1 si el canon los trae: ese es el eje)
  V  : eje x = (c0 + c1) / 2 de y = lo a y = hi        (ídem)
  D  : p0 → p1
  BOX: huella x = c0..c1, y = lo..hi → PolyLine cerrada (pier / column_wrap / chase)
Sistema de coordenadas: por defecto pt de la página rotada (display). Se acepta lo que el canon DECLARE:
  `band.units` / `constants.coord_system.value` = "px" con `dpi` (px de un render → pt = px · 72 / dpi) y
  `band.frame` / `constants.coord_system.frame` = "unrotated" (pt del mediabox sin rotar). Sin declaración y fuera
  de la página mostrada pero dentro del mediabox sin rotar → se convierte como "unrotated" y se anota en
  `conversiones`. Fuera de las dos → "sin geometría" con su motivo (nunca se inventa una posición).
Página: `page` del canon (1-based, como el visor) si en esa página está impresa la hoja de la banda; si no, la
página cuyo texto trae el número de hoja con la letra más grande (title block). Una `page` 0-based se detecta así.
Wall sin band / sin coordenadas / sin página → lista "sin geometría" (leyenda + JSON + salida), nunca se inventa.
Leyenda: página NUEVA AL FINAL del PDF (las páginas del bid set conservan su número, así `page` del canon y la
página del visor siguen siendo la misma). Totales por type (walls, LF, marcados / sin geometría) como texto y una
annot Line de muestra por color (Author "Take-off legend", /NM "TO-LEGEND-<type>").

Uso:
  python3 markups_bluebeam.py <bid_set.pdf> <takeoff_canon.json> <salida.pdf> [--json resumen.json]
  python3 markups_bluebeam.py verificar <markups.pdf> <takeoff_canon.json> [--tol 3]
  python3 markups_bluebeam.py zonas <markups.pdf> <takeoff_canon.json> <dir_png> [--n 3] [--prefijo x]
La compuerta de entrega (bitacora.py compuerta) exige un resumen JSON de esta tool con el sha del canon VIGENTE y
`verificar(pdf, canon) == []`: sin PDF de markups verificado = NO ENTREGABLE (R78.20–R78.24).
"""
import hashlib
import json
import math
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

TOOL = "markups_bluebeam"
AUTOR = "Take-off"
AUTOR_LEYENDA = "Take-off legend"
NM_PREF = "TO-"
NM_LEY = "TO-LEGEND-"
TITULO_LEYENDA = "TAKE-OFF MARKUPS - LEGEND"
OTHER = "OTHER FRAMING"
LAVANDA = (0.70, 0.50, 1.00)      # OTHER FRAMING: lavanda + punteado largo (gris no se ve sobre la tinta del plano)
DASH_OTHER = (8, 4)
DASH_CICLO = (2, 2)
PALETA = (
    (0.90, 0.10, 0.10), (0.00, 0.45, 0.85), (0.00, 0.60, 0.25), (1.00, 0.50, 0.00),
    (0.55, 0.20, 0.75), (0.00, 0.70, 0.75), (0.85, 0.10, 0.60), (0.60, 0.40, 0.10),
    (0.45, 0.70, 0.00), (0.10, 0.20, 0.55), (0.95, 0.75, 0.00), (0.50, 0.00, 0.10),
    (0.30, 0.55, 0.55), (1.00, 0.40, 0.55), (0.35, 0.35, 0.00), (0.00, 0.35, 0.30),
)
ANCHO = 2.5          # pt del trazo
OPACIDAD = 0.85
TOL_PT = 3.0         # verificar: vértices a <= TOL_PT del eje del canon (medio espesor de una partición típica)
TOL_COLOR = 0.02
HOJA_RX = re.compile(r"\b[A-Z]{1,3}-?(?:\d{1,3}\.\d{1,3}|\d{3}[A-Z]?(?![\w.]))\b")
MT_POLYLENGTH = 130   # /MeasurementTypes de un Polylength de Bluebeam Revu
NHOJA_RX = re.compile(r"\b[0-9A-Z]{1,3}/[A-Z]{1,3}-?\d{1,4}(?:\.\d{1,3})?[A-Z]?\b")


# ----------------------------------------------------------------------------------------------- canon
def _cargar(canon):
    if isinstance(canon, dict):
        return canon
    with open(canon, encoding="utf-8") as f:
        return json.load(f)


def sha_archivo(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def walls(canon):
    return [w for w in (canon.get("walls") or []) if isinstance(w, dict) and w.get("id")]


def tipo(w):
    """Subject de la annot = partition type del wall (misma convención que la hoja Partition Takeoff)."""
    import particion
    import partition_types as PT
    if w.get("element", "wall") in PT.OTHER:
        return OTHER
    t = particion.tipo(w)
    return t or OTHER


def colores(canon):
    """{type: (rgb, dashes)} determinista: types ordenados, PALETA en ciclo (vuelta 2+ = punteado corto); OTHER FRAMING
    lavanda con punteado largo."""
    ts = sorted({tipo(w) for w in walls(canon)} - {OTHER})
    out = {}
    for i, t in enumerate(ts):
        out[t] = (PALETA[i % len(PALETA)], None if i < len(PALETA) else DASH_CICLO)
    out[OTHER] = (LAVANDA, DASH_OTHER)
    return out


def lf(w):
    try:
        return float(w.get("length_ft") or 0.0)
    except (TypeError, ValueError):
        return 0.0


def cita(w):
    """N/HOJA que trae el canon (detail, detail_source, source); sin detalle, la hoja de la banda."""
    for k in ("detail", "detail_source", "source"):
        m = NHOJA_RX.search(str(w.get(k) or ""))
        if m:
            return m.group(0)
    return str((w.get("band") or {}).get("sheet") or w.get("sheet") or "")


def altura(w):
    """Altura del wall en ft (height_ft numérico o {value}); None si el canon no la trae (PENDING)."""
    h = w.get("height_ft")
    if isinstance(h, dict):
        h = h.get("value")
    try:
        h = float(h)
    except (TypeError, ValueError):
        return None
    return h if h > 0 else None


def ftin(x):
    pulg = round(x * 12.0 * 8.0) / 8.0
    ft, inch = int(pulg // 12), pulg - 12 * int(pulg // 12)
    s = f"{inch:.3f}".rstrip("0").rstrip(".")
    return f"{ft}'-{s}\""


def contenido(w):
    """v80e (usuario 24-oct, todo proyecto): Contents = TYPE · LF · H · SF · N/HOJA · id.
    SF = LF x H (área del wall, una cara); sin altura en el canon -> H PENDING · SF PENDING (nunca se inventa)."""
    h = altura(w)
    hs = f"H {ftin(h)} · {lf(w) * h:,.1f} SF" if h else "H PENDING · SF PENDING"
    return f"{tipo(w)} · {lf(w):.2f} LF · {hs} · {cita(w)} · {w['id']}"


def escala(canon, sheet=None):
    """pt de la hoja por ft real (constants.plan_scale_pt_per_ft, número o {value}); None si no está.
    v80f (R80e.15): si constants.plan_scale_by_sheet trae la hoja, manda esa (un set con planta a 1/8" y planta
    ampliada a 1/2" mediría 4x mal con una sola escala)."""
    k = (canon or {}).get("constants") or {}
    v = (k.get("plan_scale_by_sheet") or {}).get(sheet) if sheet else None
    if v is None:
        v = k.get("plan_scale_pt_per_ft")
    if isinstance(v, dict):
        v = v.get("value")
    try:
        v = float(v)
    except (TypeError, ValueError):
        return None
    return v if v > 0 else None


def _measure(doc, annot, pt_per_ft):
    """v80e: diccionario /Measure (escala) para que Bluebeam muestre la columna Length en ft de la annot."""
    from fractions import Fraction
    pulg = Fraction(pt_per_ft).limit_denominator(1000) / 72   # pulgadas de papel por ft real (9 pt/ft = 1/8")
    r = f"{pulg.numerator}/{pulg.denominator} in = 1 ft" if pulg.denominator != 1 else f"{pulg.numerator} in = 1 ft"
    c = 1.0 / pt_per_ft
    doc.xref_set_key(annot.xref, "Measure",
                     f"<</Type/Measure/Subtype/RL/R({r})/X[<</Type/NumberFormat/U(ft)/C {c:.10f}/D 100>>]"
                     f"/D[<</Type/NumberFormat/U(ft)/C 1/D 100>>]/A[<</Type/NumberFormat/U(sf)/C 1/D 100>>]>>")
    doc.xref_set_key(annot.xref, "IT", "/PolyLineDimension")
    doc.xref_set_key(annot.xref, "MeasurementTypes", str(MT_POLYLENGTH))


def _depth(doc, annot, h_ft):
    """v80e: Depth de Bluebeam = altura del wall (ft decimales); Bluebeam calcula Wall Area = Length x Depth.
    Formato de Revu: /Depth <ft> + /DepthUnit [<</Type/NumberFormat/U(ft)/C 1/864/D 100/FD true/SS()>>]."""
    doc.xref_set_key(annot.xref, "Depth", f"{h_ft:.6g}")
    doc.xref_set_key(annot.xref, "DepthUnit", "[<</Type/NumberFormat/U(ft)/C .001157407/D 100/FD true/SS()>>]")


# ----------------------------------------------------------------------------------------------- geometría
def _num(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None


def eje_canon(w):
    """-> (puntos [(x, y)...] en el sistema del canon, cerrado: bool) o (None, motivo)."""
    b = w.get("band")
    if not isinstance(b, dict):
        return None, "sin band"
    ori = str(b.get("ori") or "").upper()
    p0, p1 = b.get("p0"), b.get("p1")
    if isinstance(p0, (list, tuple)) and isinstance(p1, (list, tuple)) and len(p0) == 2 and len(p1) == 2 \
            and ori in ("H", "V", "D"):
        q = [(_num(p0[0]), _num(p0[1])), (_num(p1[0]), _num(p1[1]))]
        if all(v is not None for p in q for v in p):
            return (q, False), None
    if ori == "D":
        return None, "band D sin p0 / p1"
    c0, c1, lo, hi = (_num(b.get(k)) for k in ("c0", "c1", "lo", "hi"))
    if None in (c0, c1, lo, hi):
        return None, f"band {ori or '?'} sin c0 / c1 / lo / hi numéricos"
    if ori == "H":
        m = (c0 + c1) / 2.0
        return ([(lo, m), (hi, m)], False), None
    if ori == "V":
        m = (c0 + c1) / 2.0
        return ([(m, lo), (m, hi)], False), None
    if ori == "BOX":
        x0, x1 = sorted((c0, c1))
        y0, y1 = sorted((lo, hi))
        return ([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], True), None
    return None, f"band ori '{ori}' desconocida"


def _sistema(canon, w):
    """(units, dpi, frame) declarados por la banda o por constants.coord_system."""
    b = w.get("band") or {}
    cs = (canon.get("constants") or {}).get("coord_system") or {}
    if not isinstance(cs, dict):
        cs = {"value": cs}
    units = str(b.get("units") or cs.get("value") or cs.get("units") or "pt").lower()
    dpi = _num(b.get("dpi") or cs.get("dpi"))
    frame = str(b.get("frame") or cs.get("frame") or "").lower() or None
    return units, dpi, frame


class _Paginas:
    """Página (0-based) de cada hoja, validada contra el texto del PDF."""

    def __init__(self, doc):
        self.doc = doc
        self._txt = {}
        self._mejor = {}

    def texto(self, i):
        if i not in self._txt:
            self._txt[i] = self.doc[i].get_text("text") if 0 <= i < self.doc.page_count else ""
        return self._txt[i]

    def tiene(self, i, hoja):
        return bool(hoja) and re.search(r"(?<![\w.])" + re.escape(hoja) + r"(?![\w.])", self.texto(i)) is not None

    def por_titulo(self, hoja):
        """Página cuyo número de hoja impreso con la letra más grande es `hoja` (title block)."""
        if hoja in self._mejor:
            return self._mejor[hoja]
        mejor, tam = None, 0.0
        for i in range(self.doc.page_count):
            if not self.tiene(i, hoja):
                continue
            for bl in self.doc[i].get_text("dict").get("blocks", []):
                for ln in bl.get("lines", []):
                    for sp in ln.get("spans", []):
                        if sp.get("text", "").strip() == hoja and float(sp.get("size") or 0) > tam:
                            mejor, tam = i, float(sp["size"])
        self._mejor[hoja] = mejor
        return mejor

    def de(self, w, notas):
        hoja = str((w.get("band") or {}).get("sheet") or w.get("sheet") or w.get("plan_sheet") or "").strip()
        pg = w.get("page")
        try:
            pg = int(pg) if pg is not None else None
        except (TypeError, ValueError):
            pg = None
        if pg is not None and (w.get("band") or {}).get("sheet") in (None, w.get("sheet")):
            if 1 <= pg <= self.doc.page_count and (not hoja or self.tiene(pg - 1, hoja)):
                return pg - 1, hoja
            if hoja and 0 <= pg < self.doc.page_count and self.tiene(pg, hoja) and \
                    (pg < 1 or not self.tiene(pg - 1, hoja)):
                notas.append(f"{w['id']}: page {pg} parece 0-based (la hoja {hoja} está en la página {pg + 1})")
                return pg, hoja
        if hoja:
            i = self.por_titulo(hoja)
            if i is not None:
                if pg is not None:
                    notas.append(f"{w['id']}: page {pg} no imprime {hoja}; se usa la página {i + 1} (title block)")
                return i, hoja
        return None, hoja


def geometria(canon, doc, paginas=None, notas=None):
    """-> ({id: {page, sheet, pts_display, cerrado}}, [sin geometría {id, type, lf, motivo}], notas)."""
    import pymupdf as fitz
    paginas = paginas or _Paginas(doc)
    notas = [] if notas is None else notas
    geo, sin = {}, []
    for w in walls(canon):
        r, motivo = eje_canon(w)
        if r is None:
            sin.append({"id": w["id"], "type": tipo(w), "lf": round(lf(w), 3), "motivo": motivo})
            continue
        pts, cerrado = r
        i, hoja = paginas.de(w, notas)
        if i is None:
            sin.append({"id": w["id"], "type": tipo(w), "lf": round(lf(w), 3),
                        "motivo": f"hoja {hoja or '?'} no encontrada en el PDF (page {w.get('page')})"})
            continue
        page = doc[i]
        units, dpi, frame = _sistema(canon, w)
        if units in ("px", "pixel", "pixels"):
            if not dpi:
                sin.append({"id": w["id"], "type": tipo(w), "lf": round(lf(w), 3),
                            "motivo": "coordenadas en px sin dpi declarado"})
                continue
            pts = [(x * 72.0 / dpi, y * 72.0 / dpi) for x, y in pts]
            notas.append(f"{w['id']}: px a {dpi:g} dpi -> pt (x 72/{dpi:g})")
        disp = page.rect
        unrot = fitz.Rect(0, 0, page.rect.height, page.rect.width) if page.rotation % 180 else page.rect

        def dentro(R, q):
            return all(R.x0 - 0.5 <= x <= R.x1 + 0.5 and R.y0 - 0.5 <= y <= R.y1 + 0.5 for x, y in q)
        if frame == "unrotated" or (frame is None and not dentro(disp, pts) and page.rotation and dentro(unrot, pts)):
            if frame is None:
                notas.append(f"{w['id']}: coordenadas fuera de la página mostrada y dentro del mediabox sin rotar "
                             f"(rotación {page.rotation}) -> convertidas con rotation_matrix")
            M = page.rotation_matrix
            pts = [tuple(fitz.Point(x, y) * M) for x, y in pts]
        if not dentro(disp, pts):
            sin.append({"id": w["id"], "type": tipo(w), "lf": round(lf(w), 3),
                        "motivo": f"coordenadas fuera de la hoja {hoja} (sistema no declarado)"})
            continue
        geo[w["id"]] = {"page": i, "sheet": hoja, "pts": [(float(x), float(y)) for x, y in pts], "cerrado": cerrado}
    return geo, sin, notas


# ----------------------------------------------------------------------------------------------- escritura
def _nm(doc, annot, nombre):
    import pymupdf as fitz
    doc.xref_set_key(annot.xref, "NM", fitz.get_pdf_str(nombre))


def _annot(doc, page, pts_disp, rgb, dashes, subject, content, autor, nombre):
    import pymupdf as fitz
    M = page.derotation_matrix
    q = [fitz.Point(x, y) * M for x, y in pts_disp]
    a = page.add_polyline_annot(q)   # v80e: siempre PolyLine = Polylength de Bluebeam (Depth / Wall Area)
    a.set_info(title=autor, subject=subject, content=content)
    a.set_colors(stroke=rgb)
    a.set_border(width=ANCHO, dashes=list(dashes) if dashes else None)
    a.set_opacity(OPACIDAD)
    a.update()
    _nm(doc, a, nombre)
    return a


def totales(canon, geo):
    out = {}
    for w in walls(canon):
        t = tipo(w)
        d = out.setdefault(t, {"walls": 0, "lf": 0.0, "marcados": 0, "sin_geometria": 0})
        d["walls"] += 1
        d["lf"] = round(d["lf"] + lf(w), 3)
        d["marcados" if w["id"] in geo else "sin_geometria"] += 1
    return dict(sorted(out.items(), key=lambda kv: (kv[0] == OTHER, kv[0])))


def _leyenda(doc, canon, geo, sin, cols, nombre_canon):
    """Página nueva AL FINAL: totales por type + annot Line de muestra por color + walls sin geometría."""
    W, H = 1224.0, 792.0                                           # 17 x 11 in, horizontal
    p = doc.new_page(-1, width=W, height=H)
    y = 48.0
    p.insert_text((40, y), TITULO_LEYENDA, fontsize=20, fontname="hebo")
    y += 20
    p.insert_text((40, y), f"Source: {nombre_canon} · one PDF annotation (Line / PolyLine) per wall on the plan "
                           f"sheet where it was measured · Subject = type · Contents = TYPE · LF · H · SF · DETAIL · id",
                  fontsize=8.5, fontname="helv")
    y += 26
    xs = (40, 130, 330, 400, 480, 560)
    for x, h in zip(xs, ("Sample", "Type", "Walls", "LF", "Marked", "No geometry")):
        p.insert_text((x, y), h, fontsize=10, fontname="hebo")
    y += 6
    p.draw_line((40, y), (W - 40, y), color=(0, 0, 0), width=0.5)
    tot = totales(canon, geo)
    filas = 0
    for t, d in tot.items():
        y += 17
        if y > H - 60:
            break
        rgb, dashes = cols.get(t, (LAVANDA, None))
        _annot(doc, p, [(xs[0], y - 4), (xs[0] + 70, y - 4)], rgb, dashes, t,
               f"LEGEND · {t} · {d['walls']} walls · {d['lf']:.2f} LF", AUTOR_LEYENDA, NM_LEY + t)
        for x, v in zip(xs[1:], (t, str(d["walls"]), f"{d['lf']:.2f}", str(d["marcados"]),
                                 str(d["sin_geometria"]))):
            p.insert_text((x, y), v, fontsize=10, fontname="helv")
        filas += 1
    y += 10
    p.draw_line((40, y), (W - 40, y), color=(0, 0, 0), width=0.5)
    y += 16
    p.insert_text((130, y), "TOTAL", fontsize=10, fontname="hebo")
    p.insert_text((330, y), str(sum(d["walls"] for d in tot.values())), fontsize=10, fontname="hebo")
    p.insert_text((400, y), f"{sum(d['lf'] for d in tot.values()):.2f}", fontsize=10, fontname="hebo")
    p.insert_text((480, y), str(len(geo)), fontsize=10, fontname="hebo")
    p.insert_text((560, y), str(len(sin)), fontsize=10, fontname="hebo")
    # walls sin geometría: lista completa (columna derecha), nunca se dibujan
    x2, y2 = 700.0, 94.0
    p.insert_text((x2, y2), f"Walls without geometry (not marked): {len(sin)}", fontsize=10, fontname="hebo")
    for s in sin:
        y2 += 11
        if y2 > H - 30:
            x2, y2 = x2 + 260, 105.0
            if x2 > W - 100:
                break
        p.insert_text((x2, y2), f"{s['id']} · {s['type']} · {s['lf']:.2f} LF · {s['motivo']}"[:62],
                      fontsize=7, fontname="helv")
    return p.number


def _page_labels(doc, hojas):
    """v80e: Page Label = número de hoja (A-101…) en las páginas con markups, para la columna Page Label de
    Bluebeam; las demás páginas conservan su número."""
    if not hojas:
        return
    reglas, n = [], doc.page_count
    for i in range(n):
        if i in hojas:
            reglas.append({"startpage": i, "prefix": str(hojas[i]), "style": "", "firstpagenum": 1})
        elif i == 0 or (i - 1) in hojas:
            reglas.append({"startpage": i, "prefix": "", "style": "D", "firstpagenum": i + 1})
    doc.set_page_labels(reglas)


def escribir(bid_pdf, canon_path, out_pdf, out_json=None):
    """Escribe el PDF de markups y su resumen JSON. -> resumen (dict)."""
    import pymupdf as fitz
    canon = _cargar(canon_path)
    doc = fitz.open(bid_pdf)
    n_bid = doc.page_count
    geo, sin, notas = geometria(canon, doc)
    cols = colores(canon)
    esc = escala(canon)
    por_hoja, por_type = {}, {}
    for w in walls(canon):
        g = geo.get(w["id"])
        if not g:
            continue
        t = tipo(w)
        rgb, dashes = cols[t]
        a = _annot(doc, doc[g["page"]], g["pts"], rgb, dashes, t, contenido(w), AUTOR, NM_PREF + w["id"])
        esc_w = escala(canon, g.get("sheet")) or esc
        if esc_w:
            _measure(doc, a, esc_w)
            if altura(w):
                _depth(doc, a, altura(w))
        k = f"{g['sheet']} (p.{g['page'] + 1})"
        por_hoja[k] = por_hoja.get(k, 0) + 1
        por_type[t] = por_type.get(t, 0) + 1
    ley = _leyenda(doc, canon, geo, sin, cols, "the take-off Excel (Partition Takeoff)")   # v80o (BE-48): sin nombres de archivos
    _page_labels(doc, {**{g["page"]: g["sheet"] for g in geo.values() if g.get("sheet")}, ley: "LEGEND"})
    doc.set_metadata(dict(doc.metadata or {}, keywords=f"{TOOL}; legend_page={ley + 1}; bid_pages={n_bid}",
                          creator=TOOL))
    os.makedirs(os.path.dirname(os.path.abspath(out_pdf)), exist_ok=True)
    doc.save(out_pdf, garbage=1, deflate=True)
    doc.close()
    res = {"tool": TOOL, "pdf": os.path.abspath(out_pdf), "bid_set": os.path.abspath(bid_pdf),
           "canon": None if isinstance(canon_path, dict) else os.path.abspath(canon_path),
           "canon_sha": None if isinstance(canon_path, dict) else sha_archivo(canon_path),
           "pdf_sha": sha_archivo(out_pdf), "leyenda": {"pagina": ley + 1, "posicion": "final"},
           "annots": len(geo), "por_hoja": dict(sorted(por_hoja.items())), "por_type": dict(sorted(por_type.items())),
           "totales": totales(canon, geo), "colores": {t: list(c[0]) for t, c in cols.items()},
           "sin_geometria": sin, "conversiones": notas}
    out_json = out_json or os.path.splitext(out_pdf)[0] + ".json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    res["json"] = os.path.abspath(out_json)
    return res


# ----------------------------------------------------------------------------------------------- verificación
def _dist_seg(p, a, b):
    ax, ay = a
    bx, by = b
    px, py = p
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L2))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def _dist_poli(p, pts):
    return min(_dist_seg(p, pts[i], pts[i + 1]) for i in range(len(pts) - 1)) if len(pts) > 1 else \
        math.hypot(p[0] - pts[0][0], p[1] - pts[0][1])


def _leer_annots(doc):
    """-> {nm: [(page, annot_type_name, info, colors, vertices_display)]} y lista de (page, tipo) sin /NM nuestro."""
    import pymupdf as fitz
    out = {}
    for i in range(doc.page_count):
        pg = doc[i]
        M = pg.rotation_matrix
        for a in pg.annots() or []:
            nm = (a.info or {}).get("id") or ""
            vs = a.vertices or []
            try:
                vd = [tuple(fitz.Point(v) * M) for v in vs]
            except Exception:                                          # noqa: BLE001
                vd = []
            out.setdefault(nm, []).append((i, a.type[1], dict(a.info or {}), dict(a.colors or {}), vd,
                                           tuple((a.border or {}).get("dashes") or ())))
    return out


def verificar(pdf, canon, tol=TOL_PT, detalle=None):
    """Abre el PDF de markups y lo compara con el canon. -> lista de fallas ([] = OK).
    Exige: una annot PolyLine / Line por wall con geometría (en su página), color del type, Subject = type,
    Contents "TYPE · LF · H · SF · N/HOJA · id", Author "Take-off", vértices sobre el eje del canon (<= tol pt) cubriendo sus
    dos extremos; ninguna annot "TO-" de un wall que no está en el canon; leyenda al final con cada type."""
    import pymupdf as fitz
    canon = _cargar(canon)
    fallas = []
    if not pdf or not os.path.isfile(pdf):
        return [f"no existe el PDF de markups {pdf}"]
    doc = fitz.open(pdf)
    meta = (doc.metadata or {}).get("keywords") or ""
    m = re.search(r"bid_pages=(\d+)", meta)
    n_bid = int(m.group(1)) if m else doc.page_count - 1
    paginas = _Paginas(doc)
    geo, sin, _notas = geometria(canon, doc, paginas)
    cols = colores(canon)
    an = _leer_annots(doc)
    ids = {w["id"] for w in walls(canon)}
    for nm in an:
        if nm.startswith(NM_PREF) and not nm.startswith(NM_LEY) and nm[len(NM_PREF):] not in ids:
            fallas.append(f"annot {nm}: wall que no está en el canon")
    for w in walls(canon):
        g = geo.get(w["id"])
        if not g:
            continue
        t = tipo(w)
        lst = an.get(NM_PREF + w["id"]) or []
        if not lst:
            fallas.append(f"{w['id']} ({t}, {g['sheet']} p.{g['page'] + 1}): falta su annot de markup")
            continue
        if len(lst) > 1:
            fallas.append(f"{w['id']}: {len(lst)} annots con el mismo /NM (una por wall)")
        pg, tp, info, colors, vd, dashes = lst[0]
        if tp not in ("PolyLine", "Line"):
            fallas.append(f"{w['id']}: annot tipo {tp}, se espera PolyLine / Line (markup editable, no imagen)")
            continue
        if pg != g["page"]:
            fallas.append(f"{w['id']}: annot en la página {pg + 1}, el wall se midió en la {g['page'] + 1} "
                          f"({g['sheet']})")
        rgb = cols[t][0]
        st = tuple(colors.get("stroke") or ())
        if len(st) != 3 or max(abs(a - b) for a, b in zip(st, rgb)) > TOL_COLOR:
            fallas.append(f"{w['id']}: color {st} != color del type {t} {rgb}")
        if bool(cols[t][1]) != bool(dashes):
            fallas.append(f"{w['id']}: trazo {'punteado' if dashes else 'continuo'}, el type {t} va "
                          f"{'punteado' if cols[t][1] else 'continuo'}")
        if info.get("subject") != t:
            fallas.append(f"{w['id']}: Subject '{info.get('subject')}' != type '{t}'")
        if info.get("content") != contenido(w):
            fallas.append(f"{w['id']}: Contents '{info.get('content')}' != '{contenido(w)}'")
        if info.get("title") != AUTOR:
            fallas.append(f"{w['id']}: Author '{info.get('title')}' != '{AUTOR}'")
        eje = g["pts"]
        if len(vd) < 2:
            fallas.append(f"{w['id']}: annot sin vértices")
            continue
        lejos = max(_dist_poli(v, eje) for v in vd)
        cubre = max(min(math.hypot(e[0] - v[0], e[1] - v[1]) for v in vd) for e in (eje[0], eje[-1]))
        if lejos > tol or cubre > tol:
            fallas.append(f"{w['id']}: vértices fuera del eje del wall ({lejos:.1f} pt del eje, extremos a "
                          f"{cubre:.1f} pt; tolerancia {tol} pt)")
    # leyenda al final
    if doc.page_count <= n_bid:
        fallas.append("falta la página de leyenda (al final del PDF)")
    else:
        txt = doc[doc.page_count - 1].get_text("text")
        if TITULO_LEYENDA not in txt:
            fallas.append(f"la última página no es la leyenda ('{TITULO_LEYENDA}')")
        for t in totales(canon, geo):
            if t not in txt:
                fallas.append(f"leyenda: falta el type {t}")
            if not an.get(NM_LEY + t):
                fallas.append(f"leyenda: falta la annot de muestra del type {t}")
        for s in sin:
            if s["id"] not in txt:
                fallas.append(f"leyenda: falta el wall sin geometría {s['id']}")
    if detalle is not None:
        detalle.update({"annots": sum(1 for k in an if k.startswith(NM_PREF) and not k.startswith(NM_LEY)),
                        "con_geometria": len(geo), "sin_geometria": sin, "paginas": doc.page_count})
    doc.close()
    return fallas


def resumen_vigente(dirs, canon_path):
    """Busca en `dirs` el resumen JSON de esta tool cuyo canon_sha es el del canon vigente. -> (resumen, motivo)."""
    import glob
    sha = sha_archivo(canon_path)
    vistos = []
    for d in dirs:
        if not d or not os.path.isdir(d):
            continue
        for p in sorted(glob.glob(os.path.join(d, "*.json"))):
            try:
                r = json.load(open(p, encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if isinstance(r, dict) and r.get("tool") == TOOL:
                vistos.append(p)
                if r.get("canon_sha") == sha:
                    if r.get("pdf") and not os.path.isabs(r["pdf"]):
                        r["pdf"] = os.path.join(os.path.dirname(p), r["pdf"])
                    return r, None
    if vistos:
        return None, f"el PDF de markups es de otra versión del canon ({', '.join(os.path.basename(v) for v in vistos)})"
    return None, "no hay PDF de markups (markups_bluebeam.py <bid_set.pdf> <takeoff_canon.json> <salida.pdf>)"


def compuerta(canon_path, dirs):
    """Para bitacora.py compuerta: -> lista de fallas (sin PDF de markups verificado y vigente = NO ENTREGABLE)."""
    r, motivo = resumen_vigente(dirs, canon_path)
    if r is None:
        return [motivo]
    # el PDF puede editarse en Bluebeam después de escribirlo (pdf_sha cambia): vale mientras siga verificando
    return verificar(r.get("pdf"), canon_path)


# ----------------------------------------------------------------------------------------------- zonas (PNG)
def zonas(pdf, canon, dest, n=3, prefijo="markups", dpi=110, margen=40.0):
    """Renderiza n zonas (las de más annots, en las hojas con más walls) a PNG con las annots visibles."""
    import pymupdf as fitz
    canon = _cargar(canon)
    doc = fitz.open(pdf)
    geo, _sin, _n = geometria(canon, doc)
    porp = {}
    for i, g in geo.items():
        porp.setdefault(g["page"], []).append(g)
    os.makedirs(dest, exist_ok=True)
    out = []
    for pg, gs in sorted(porp.items(), key=lambda kv: -len(kv[1])):
        xs = [x for g in gs for x, _ in g["pts"]]
        ys = [y for g in gs for _, y in g["pts"]]
        R = fitz.Rect(min(xs), min(ys), max(xs), max(ys))
        # ventana de ~1/2 del bbox de la hoja: tantas zonas como quepan, empezando por la más poblada
        w2, h2 = max(R.width / 2.0, 300.0), max(R.height / 2.0, 220.0)
        cands = []
        for fx in (0.0, 0.5, 1.0):
            for fy in (0.0, 0.5, 1.0):
                c = fitz.Rect(R.x0 + fx * (R.width - w2), R.y0 + fy * (R.height - h2), 0, 0)
                c.x1, c.y1 = c.x0 + w2, c.y0 + h2
                k = sum(1 for g in gs if any(c.contains(fitz.Point(p)) for p in g["pts"]))
                cands.append((k, c))
        cands.sort(key=lambda kc: -kc[0])
        usados = []
        for k, c in cands:
            if len(out) >= n or k == 0:
                break
            if any((c & u).get_area() > 0.4 * c.get_area() for u in usados):
                continue
            usados.append(c)
            clip = (c + (-margen, -margen, margen, margen)) & doc[pg].rect
            ruta = os.path.join(dest, f"{prefijo}_zona{len(out) + 1}.png")
            doc[pg].get_pixmap(clip=clip, dpi=dpi, annots=True).save(ruta)
            out.append({"png": ruta, "page": pg + 1, "clip": [round(v, 1) for v in clip], "walls": k})
        if len(out) >= n:
            break
    doc.close()
    return out


def main(argv):
    a = list(argv[1:])
    tol = TOL_PT
    if "--tol" in a:
        i = a.index("--tol")
        tol = float(a[i + 1])
        del a[i:i + 2]
    if len(a) == 3 and a[0] == "verificar":
        det = {}
        f = verificar(a[1], a[2], tol, det)
        print(f"annots de walls: {det.get('annots')} · walls con geometría: {det.get('con_geometria')} · "
              f"sin geometría: {len(det.get('sin_geometria') or [])}")
        for s in det.get("sin_geometria") or []:
            print(f"  SIN GEOMETRÍA {s['id']} {s['type']} {s['lf']} LF: {s['motivo']}")
        for x in f:
            print("FALLA", x)
        print("MARKUPS OK" if not f else f"MARKUPS NO OK: {len(f)} falla(s)")
        return 0 if not f else 1
    if len(a) >= 4 and a[0] == "zonas":
        n = int(a[a.index("--n") + 1]) if "--n" in a else 3
        pre = a[a.index("--prefijo") + 1] if "--prefijo" in a else "markups"
        for z in zonas(a[1], a[2], a[3], n, pre):
            print(json.dumps(z, ensure_ascii=False))
        return 0
    if len(a) >= 3 and a[0] not in ("verificar", "zonas"):
        js = a[a.index("--json") + 1] if "--json" in a else None
        r = escribir(a[0], a[1], a[2], js)
        print(f"PDF de markups -> {r['pdf']}  (resumen {r['json']})")
        print(f"annots: {r['annots']} · leyenda: página {r['leyenda']['pagina']} (al final)")
        for k, v in r["por_hoja"].items():
            print(f"  {k}: {v} annots")
        for s in r["sin_geometria"]:
            print(f"  SIN GEOMETRÍA {s['id']} {s['type']} {s['lf']} LF: {s['motivo']}")
        for x in r["conversiones"]:
            print("  CONVERSIÓN", x)
        f = verificar(r["pdf"], a[1])
        for x in f:
            print("FALLA", x)
        print("MARKUPS OK" if not f else f"MARKUPS NO OK: {len(f)} falla(s)")
        return 0 if not f else 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
