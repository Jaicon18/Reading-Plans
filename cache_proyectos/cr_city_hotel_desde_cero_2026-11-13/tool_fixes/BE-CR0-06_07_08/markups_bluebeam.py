#!/usr/bin/env python3
"""markups_bluebeam.py — v78 (W3, decisión del usuario): PDF de MARKUPS por wall, entregable FIJO de todo take-off.

Qué hace: copia el bid set y escribe, por cada wall del canon con geometría, una ANOTACIÓN PDF REAL (PolyLine o
Line, editable; nunca una imagen rasterizada) sobre el eje del wall en la hoja de planta donde se midió, para que
aparezca en el Markups List de Bluebeam y se pueda revisar / editar / medir:
  - Subject  = partition type (particion.tipo: tag, EXT-<stud>CFMF, EXT-PARAPET, BULKHEAD-<familia>, CANOPY-COL);
               elementos no-partition (partition_types.OTHER) = "OTHER FRAMING";
  - Contents = "TYPE · LF · H · <LF x H> SF wall (LF×H) · <board> SF board (faces×layers) · N/HOJA · id" (v81cf60, U-153; v80e: H = altura del canon, SF = LF x H; sin altura = PENDING;
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
  python3 markups_bluebeam.py <bid_set.pdf> <takeoff_canon.json> <salida.pdf> [--json resumen.json] [--inventario inventario.json]
     (v81cf59, U-151 / U-152: la salida va sin firmas /Sig, con Page Label = hoja en todas las páginas y escala de página /VP)
  python3 markups_bluebeam.py verificar <markups.pdf> <takeoff_canon.json> [--tol 3]
  python3 markups_bluebeam.py sf_wall <entregado.pdf> <nuevo.pdf>   (U-153: /DepthUnit /C 1 + etiqueta "SF wall (LF\u00d7H)")
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
# v80s (R80e.36): elementos de OTHER FRAMING que la hoja Partition Takeoff lista por nombre (column_wrap, soffit_side):
# Subject, color y entrada de leyenda propios; colores fijos fuera de la PALETA (no corren los colores de los types)
OTHER_EL = {"column_wrap": ("OTHER FRAMING - COLUMN WRAP", (0.45, 0.25, 0.05), (6, 3)),
            "soffit_side": ("OTHER FRAMING - SOFFIT SIDE", (0.00, 0.30, 0.65), (6, 3))}
EXIST_EL = "existing_board"   # R80w.39
OTHER_EL[EXIST_EL] = ("BOARD ONLY - NO FRAMING", (0.55, 0.55, 0.55), (3, 2))
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
NHOJA_RX = re.compile(r"\b[0-9A-Z]{1,3}(?:-[0-9A-Z]{1,3})?/[A-Z]{1,3}-?\d{1,4}(?:\.\d{1,3})?[A-Z]?\b")   # R80f.9: type con guion (A2-3D/A301) entero


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
    # solo-metal: los existing_walls entran en el for de abajo con su propio markup (R80w.39)
    out = [w for w in (canon.get("walls") or []) if isinstance(w, dict) and w.get("id")]
    for e in canon.get("existing_walls") or []:          # R80w.39: muro existente, solo board -> su propio markup
        if isinstance(e, dict) and e.get("id"):
            out.append(dict(e, element=EXIST_EL, band={"sheet": e.get("sheet"), "path": e.get("path")}))
    return out


def tipo(w):
    """Subject de la annot = partition type del wall (misma convención que la hoja Partition Takeoff)."""
    import particion
    import partition_types as PT
    if w.get("element") == EXIST_EL:                  # R80w.39
        if w.get("type_id"):                          # v81cf53 (BE-CR06): wood-framed set, board only POR TYPE
            if w.get("stud_text"):                     # CR-R10-m2: shaft wall C-H (misma etiqueta que la fila del Excel)
                return f"{w['type_id']} - SHAFT WALL (C-H STUDS AND J-RUNNER IN THE MATERIAL SUMMARY)"
            return f"{w['type_id']} - BOARD ONLY (WOOD FRAMING EXCLUDED)"
        return OTHER_EL[EXIST_EL][0]
    if w.get("element", "wall") in PT.OTHER and w.get("partition_row") and w.get("tag"):   # BE-HF14: typed row
        return PT.tipo_fila(w)
    if w.get("element", "wall") in PT.OTHER:
        el = str(w.get("element"))
        return OTHER_EL.get(el, (OTHER,))[0]           # v80s: column wrap / soffit side con su propio Subject
    t = particion.tipo(w)
    if not t and str(w.get("element")) in OTHER_EL:   # v80s
        return OTHER_EL[str(w.get("element"))][0]
    return t or OTHER


def colores(canon):
    """{type: (rgb, dashes)} determinista: types ordenados, PALETA en ciclo (vuelta 2+ = punteado corto); OTHER FRAMING
    lavanda con punteado largo."""
    esp = {v[0] for v in OTHER_EL.values()}
    orden = [str(t) for t in ((canon.get("constants") or {}).get("type_order") or {}).get("value") or []] \
        if isinstance((canon.get("constants") or {}).get("type_order"), dict) else []
    def _k(t):                                        # v81cf53 (BE-CR06): leyenda en el orden del schedule (U-121)
        base = t.split(" - ")[0]
        return (orden.index(base) if base in orden else len(orden), t)
    ts = sorted({tipo(w) for w in walls(canon)} - {OTHER} - esp, key=_k)
    out = {}
    for i, t in enumerate(ts):
        out[t] = (PALETA[i % len(PALETA)], None if i < len(PALETA) else DASH_CICLO)
    out[OTHER] = (LAVANDA, DASH_OTHER)
    for nom, rgb, dash in OTHER_EL.values():
        out[nom] = (rgb, dash)
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


SF_WALL = "SF wall (LF\u00d7H)"          # U-153 / BE-149: = Wall Area de Bluebeam (Length x Depth)
SF_BOARD = "SF board (faces\u00d7layers)"  # BE-117: = Board (SF) del renglón del Excel


def contenido(w, lf_t=None, sf_board_t=None):
    """v80e (usuario 24-oct, todo proyecto): Contents = TYPE · LF · H · SF · N/HOJA · id.
    v81cf60 (U-153 / BE-149, usuario 6-nov "haz algo para no halla errores"): SF = "<LF x H> SF wall (LF\u00d7H)" (el número que
    Bluebeam muestra en la columna Wall Area = Length x Depth) seguido de "<board> SF board (faces\u00d7layers)" (Board (SF) del
    Excel); sin board solo el SF wall; sin altura en el canon -> H PENDING · SF PENDING (nunca se inventa).
    `lf_t` / `sf_board_t`: LF y board SF de un tramo recto (R80f.37)."""
    h = altura(w)
    L = lf(w) if lf_t is None else float(lf_t)
    lfs = f"{L:.2f}" if lf_t is None else f"{L:.3f}"
    if w.get("element") == EXIST_EL:                  # R80w.39: board de las caras del muro existente
        nf, ly = int(w.get("faces") or 1), int(w.get("layers") or 1)
        bs = L * h * nf * ly if sf_board_t is None else sf_board_t
        return (f"{tipo(w)} · {lfs} LF · H {ftin(h)} · {L * h:,.2f} {SF_WALL} · {nf} face(s) · {bs:,.2f} {SF_BOARD} · "
                f"{w.get('keynote') or cita(w)} · {w['id']}")      # BE-CR0-07: board-only sin keynote -> su N/HOJA (detail / source)
    bs = board_sf(w)                                  # BE-117 (user 3-nov): SF = the board SF of the Excel row
    if bs is None and w.get("id") in BOARD_SF:        # R80f.9 (Chuze): wall sin faces en el canon -> board_out.json
        bs = BOARD_SF[w["id"]]
    if bs is not None and sf_board_t is not None:
        bs = sf_board_t
    if h and bs is not None:
        hs = f"H {ftin(h)} · {L * h:,.2f} {SF_WALL} · {bs:,.2f} {SF_BOARD}"
    else:
        hs = f"H {ftin(h)} · {L * h:,.2f} {SF_WALL}" if h else "H PENDING · SF PENDING"
    return f"{tipo(w)} · {lfs} LF · {hs} · {cita(w)} · {w['id']}"


def board_sf(w):
    """BE-117: board SF of a wall = sum of its faces (face length or wall LF) x face height x layers - openings
    (R.O. width x head height per face, the board_caras.py model); None without faces (no board on the wall)."""
    if w.get("id") in BOARD_SF:                       # R80e.133: el valor del Excel (board_out) manda
        return BOARD_SF[w["id"]]
    fs = [f for f in (w.get("faces") or []) if isinstance(f, dict)]
    if not fs:
        # BE-HF9 (HFT Loveland): a wall declared WITHOUT gypsum board (faces_none_reason, e.g. a structural CFS wall
        # sheathed with plywood by others) has 0 SF board in the Excel; LF x H in its markup failed BE-117
        return 0.0 if str(w.get("faces_none_reason") or "").strip() else None
    tot = 0.0
    for f in fs:
        try:
            L = float(f.get("length_ft") or w.get("length_ft") or 0)
            tot += L * float(f.get("height_ft") or 0) * int(f.get("layers") or 1)
        except (TypeError, ValueError):
            return None
    for o in w.get("openings") or []:
        try:
            tot -= float(o.get("ro_w_ft") or 0) * min(float(o.get("head_ft") or 0), max(float(f.get("height_ft") or 0) for f in fs)) * len(fs)
        except (TypeError, ValueError):
            pass
    return round(tot, 2)


BOARD_SF = {}


def cargar_board(canon_path):
    """R80f.9 (BE-117): board SF por wall (suma de caras de board_out.json de la carpeta out/ del canon) = la columna
    Board (SF) de la Partition Takeoff; sin board_out el SF sigue siendo LF x H."""
    BOARD_SF.clear()
    if not isinstance(canon_path, str):
        return
    p = os.path.join(os.path.dirname(os.path.abspath(canon_path)), "out", "board_out.json")
    if os.path.isfile(p):
        for c_ in json.load(open(p, encoding="utf-8")).get("caras") or []:
            BOARD_SF[c_["wall"]] = round(BOARD_SF.get(c_["wall"], 0.0) + float(c_.get("sf") or 0), 2)


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
    """v80e: Depth de Bluebeam = altura del wall (ft decimales); Bluebeam calcula Wall Area = Length x Depth / DepthUnit C.
    v81cf60 (U-153 / BE-149): /DepthUnit con /C 1 (el /Depth ya está en ft). Con /C 1/864 (= .001157407, lo de antes) Bluebeam
    mostraba el Wall Area x864; lo encontró el usuario en Bluebeam (CH.6-2 A2.03). compuerta_entrega.py CE_VISTA_BLUEBEAM
    simula el Markups List y FALLA con cualquier factor != 1."""
    doc.xref_set_key(annot.xref, "Depth", f"{h_ft:.6g}")
    doc.xref_set_key(annot.xref, "DepthUnit", f"[<</Type/NumberFormat/U(ft)/C {DEPTH_C:g}/D 100/FD true/SS()>>]")


DEPTH_C = 1          # U-153 / BE-149: nunca otro valor


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
    pa = b.get("path")                          # R80w.25: eje dibujado explícito (arco, caja abierta de 3 caras)
    if isinstance(pa, list) and len(pa) >= 2:
        q = [(_num(p[0]), _num(p[1])) for p in pa if isinstance(p, (list, tuple)) and len(p) == 2]
        if len(q) == len(pa) and all(v is not None for p in q for v in p):
            return (q, q[0] == q[-1]), None
        return None, "band.path con puntos no numéricos"
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
            if 1 <= pg <= self.doc.page_count and (not hoja or self.tiene(pg - 1, hoja) or not self.texto(pg - 1).strip()):   # R80e.71: hoja raster
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
        if pg is not None and 1 <= pg <= self.doc.page_count:
            # R80e.108: sheet number OUTLINED (vector curves, ni texto ni raster): no se encuentra por título en NINGUNA
            # página -> manda la página 1-based del canon (la misma del SHEET_MAP), declarada en las notas
            notas.append(f"{w['id']}: sheet number {hoja} not in the text layer (outlined); page {pg} of the canon used")
            return pg - 1, hoja
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
        if w.get("paths"):                       # rev8: piezas medidas del wall (el verificador las acepta todas)
            geo[w["id"]]["piezas_w"] = [[(float(x), float(y)) for x, y in p_] for p_ in w["paths"]]
    return geo, sin, notas


# ----------------------------------------------------------------------------------------------- escritura
def ajustar_a_lf(pts, lf_ft, esc, tol=TOL_PT):
    """R80f.9 (BE-117): un tramo recto cuya banda vectorial difiere del LF del take-off (cota impresa, cara a cara) en
    menos de `tol` pt se dibuja con el largo del LF, centrado en la banda: Bluebeam Length = LF de la fila del Excel y
    los vértices siguen sobre el eje (verificar, tol pt). Diferencias mayores no se tocan (se revisan / explican)."""
    if not esc or not lf_ft or len(pts) != 2:
        return pts
    (x0, y0), (x1, y1) = pts
    L = math.hypot(x1 - x0, y1 - y0)
    want = float(lf_ft) * float(esc)
    if L <= 0 or abs(L - want) > tol or abs(L - want) < 1e-6:
        return pts
    cx, cy, k = (x0 + x1) / 2.0, (y0 + y1) / 2.0, want / L / 2.0
    return [(cx - (x1 - x0) * k, cy - (y1 - y0) * k), (cx + (x1 - x0) * k, cy + (y1 - y0) * k)]


GIRO_EJE = 60.0          # R80f.37 (U-120): una polilínea que dobla más de 60° son dos ejes -> un markup por tramo recto
SEP_TRAMO = "~"          # /NM de un tramo: TO-<id>~<k> (k = 1..n); el Contents termina con el Wall ID del renglón


def tramos_rectos(pts, giro=GIRO_EJE, min_seg=3.0):
    """R80f.37: corta la polilínea en los vértices donde gira más de `giro` grados -> [[pts del tramo 1], ...]. Un arco
    (tramos cortos < min_seg pt) no se corta."""
    if len(pts) < 3:
        return [list(pts)]
    out, cur = [], [pts[0]]
    for i in range(1, len(pts) - 1):
        a, b, c = pts[i - 1], pts[i], pts[i + 1]
        u, v = (b[0] - a[0], b[1] - a[1]), (c[0] - b[0], c[1] - b[1])
        cur.append(b)
        nu, nv = math.hypot(*u), math.hypot(*v)
        if nu >= min_seg and nv >= min_seg:
            cg = max(-1.0, min(1.0, (u[0] * v[0] + u[1] * v[1]) / (nu * nv)))
            if math.degrees(math.acos(cg)) > giro:
                out.append(cur)
                cur = [b]
    cur.append(pts[-1])
    out.append(cur)
    return out


def repartir(total, partes, dec=2):
    """R80f.37: reparte `total` en proporción a `partes`, redondeado, el último absorbe el redondeo (la suma = total)."""
    s_ = sum(partes) or 1.0
    xs = [round(total * p_ / s_, dec) for p_ in partes[:-1]]
    return xs + [round(total - sum(xs), dec)]


def contenido_tramo(w, lf_t, sf_t):
    """R80f.37: Contents del tramo = el del wall con su LF, su SF wall (LF x H del tramo) y su SF board (mismo TYPE, H, N/HOJA y
    Wall ID al final)."""
    return contenido(w, lf_t, sf_t)


# U-167 / BE-156 (CR City Hotel rev18, CSV de Bluebeam del usuario sin 5 markups): un /NM con "/" ("bedroom/closet") no sale
# en el Markups List / CSV de Bluebeam, y 92 EXCLUDED con /NM repetido (fitz-A0...) tampoco son confiables. Todo /NM va ÚNICO en
# todo el PDF y sin "/" ni "\\": se escribe con nm_seguro (reversible, %2F / %5C) y se lee con nm_leer.
_NM_ESC = (("%", "%25"), ("/", "%2F"), ("\\", "%5C"))


def nm_seguro(nombre):
    s = str(nombre)
    for a, b in _NM_ESC:
        s = s.replace(a, b)
    return s


def nm_leer(nm):
    s = str(nm or "")
    for a, b in reversed(_NM_ESC):
        s = s.replace(b, a)
    return s


def _nm(doc, annot, nombre):
    import pymupdf as fitz
    doc.xref_set_key(annot.xref, "NM", fitz.get_pdf_str(nm_seguro(nombre)))



def nm_unicos(doc, pref="TOA"):
    """U-167: deja todo /NM del PDF único y sin '/' ni '\\'. Los del take-off (TO- / TOX- / DEMO-) con '/' se re-escriben con
    nm_seguro (su llave se conserva); un /NM vacío, repetido (fitz-A0... de cada página) o con '/' de otra annot pasa a
    '<pref>-<Page Label>-<k>'. Un TO- repetido NO se renombra (es un error del canon que verificar reporta). -> n renombrados"""
    vistos, n = set(), 0
    for i in range(doc.page_count):
        pg = doc[i]
        lab = nm_seguro(pg.get_label() or f"p{i + 1}").replace(" ", "_")
        for k, a in enumerate(pg.annots() or [], 1):
            nm = (a.info or {}).get("id") or ""
            if nm.startswith(("TO-", "TOX-", "DEMO-")):
                nuevo = nm_seguro(nm_leer(nm)) if ("/" in nm or "\\" in nm) else nm
            elif nm and nm not in vistos and "/" not in nm and "\\" not in nm:
                nuevo = nm
            else:
                nuevo = f"{pref}-{lab}-{k}"
                j = 1
                while nuevo in vistos:
                    j += 1
                    nuevo = f"{pref}-{lab}-{k}-{j}"
            if nuevo != nm:
                doc.xref_set_key(a.xref, "NM", __import__("pymupdf").get_pdf_str(nuevo))
                n += 1
            vistos.add(nuevo)
    return n


def nm_fallas(pdf):
    """U-167: /NM repetido en el PDF o con '/' o '\\' = falla (Bluebeam deja el markup fuera del Markups List / CSV). -> [fallas]"""
    import pikepdf
    cuenta, malos = {}, []
    with pikepdf.open(pdf) as d:
        for i, page in enumerate(d.pages):
            for a in page.obj.get("/Annots") or []:
                try:
                    if str(a.get("/Subtype") or "") in ("/Popup", "/Link", "/Widget"):
                        continue
                    nm = str(a.get("/NM") or "")
                except Exception:                                       # noqa: BLE001
                    continue
                cuenta[nm] = cuenta.get(nm, 0) + 1
                if "/" in nm or "\\" in nm:
                    malos.append(f"página {i + 1}: /NM con '/' o '\\': {nm[:80]} (U-167)")
    if cuenta.get(""):
        malos.append(f"{cuenta.pop('')} markup(s) sin /NM (U-167)")
    dup = {k: v for k, v in cuenta.items() if v > 1}
    if dup:
        malos.append(f"{sum(dup.values())} markups con /NM repetido ({len(dup)} nombres; ej. {', '.join(list(dup)[:3])}) (U-167)")
    return malos


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
        d = out.setdefault(t, {"walls": 0, "lf": 0.0, "marcados": 0, "sin_geometria": 0})   # campo: conteo de la leyenda
        d["walls"] += 1   # campo: conteo de la leyenda
        d["lf"] = round(d["lf"] + lf(w), 3)
        d["marcados" if w["id"] in geo else "sin_geometria"] += 1
    return dict(sorted(out.items(), key=lambda kv: (kv[0].startswith(OTHER), kv[0])))


def celda_legible(v, ancho, fs=10.0, minimo=3.5):
    """BE-CR36 (CR rev19, usuario 12-nov 'datos ensimados'): texto de una celda de la LEGEND que cabe en su columna: baja la letra hasta
    'minimo' (3.5 pt); nunca recorta (el verificador exige el type completo en la leyenda). -> (fontsize, texto)"""
    import pymupdf
    v = str(v)
    while fs > minimo and pymupdf.get_text_length(v, fontname="helv", fontsize=fs) > ancho:
        fs = round(fs - 0.5, 2)
    return fs, v      # nunca se recorta: la leyenda lleva el type completo (verificar: 'falta el type ...'); la letra baja hasta caber


def _leyenda(doc, canon, geo, sin, cols, nombre_canon):
    """Página nueva AL FINAL: totales por type + annot Line de muestra por color + walls sin geometría."""
    W, H = 1224.0, 792.0                                           # 17 x 11 in, horizontal
    p = doc.new_page(-1, width=W, height=H)
    y = 48.0
    p.insert_text((40, y), TITULO_LEYENDA + (f" - {canon['markup_label']}" if canon.get("markup_label") else ""),
                  fontsize=20, fontname="hebo")
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
    tot = {t: tot[t] for t in orden_types(canon, list(tot))}     # BE-HF17: legend page in schedule order (R80f.10)
    filas = 0
    for t, d in tot.items():
        y += 17
        if y > H - 60:
            break
        rgb, dashes = cols.get(t, (LAVANDA, None))
        _annot(doc, p, [(xs[0], y - 4), (xs[0] + 70, y - 4)], rgb, dashes, "LEGEND",   # BE-XF07: Subject LEGEND, never a type
               f"LEGEND · {t} · {d['walls']} walls · {d['lf']:.2f} LF", AUTOR_LEYENDA, NM_LEY + t)   # campo: conteo de la leyenda
        for k_, (x, v) in enumerate(zip(xs[1:], (t, str(d["walls"]), f"{d['lf']:.2f}", str(d["marcados"]),   # campo: conteo de la leyenda
                                               str(d["sin_geometria"])))):
            fs_, v_ = celda_legible(v, (xs[k_ + 2] if k_ + 2 < len(xs) else W - 40) - x - 6)   # BE-CR36 (U-187): nada se encima
            p.insert_text((x, y), v_, fontsize=fs_, fontname="helv")
        filas += 1
    y += 10
    p.draw_line((40, y), (W - 40, y), color=(0, 0, 0), width=0.5)
    y += 16
    p.insert_text((130, y), "TOTAL", fontsize=10, fontname="hebo")
    p.insert_text((330, y), str(sum(d["walls"] for d in tot.values())), fontsize=10, fontname="hebo")   # campo: conteo de la leyenda
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


def orden_types(canon, types):
    """R80f.10: orden del schedule de partition types (constants.type_order / type_order del canon), luego el resto
    alfabético, y al final OTHER FRAMING y los bloques especiales."""
    k = (canon.get("constants") or {}).get("type_order") or canon.get("type_order") or []
    if isinstance(k, dict):
        k = k.get("value") or []
    rank = {str(t).upper(): i for i, t in enumerate(k)}
    esp = [v[0] for v in OTHER_EL.values()] + [OTHER]
    return sorted(types, key=lambda t: (t in esp, rank.get(str(t).upper(), len(rank)), esp.index(t) if t in esp else 0, str(t)))


def leyendas_por_hoja(doc, canon, geo, cols):
    """R80f.10 (BE-117): cada hoja con markups lleva su leyenda (types de ESA hoja en el orden del schedule, color, nro.
    de walls y LF), dibujada en la esquina con menos tinta del plano (no es una annot: no cuenta como markup)."""
    import pymupdf as fitz
    por_pag = {}
    for w in walls(canon):
        g = geo.get(w["id"])
        if g:
            d = por_pag.setdefault(g["page"], {}).setdefault(tipo(w), [0, 0.0])
            d[0] += 1; d[1] += lf(w)
    for pg, ts in por_pag.items():
        page = doc[pg]
        orden = orden_types(canon, list(ts))
        Wd, Hd = 330.0, 30.0 + 13.0 * len(orden)
        R = page.rect
        cands = [fitz.Rect(R.x0 + 40, R.y0 + 40, R.x0 + 40 + Wd, R.y0 + 40 + Hd),
                 fitz.Rect(R.x0 + 40, R.y1 - 40 - Hd, R.x0 + 40 + Wd, R.y1 - 40),
                 fitz.Rect(R.x0 + R.width * 0.4, R.y0 + 40, R.x0 + R.width * 0.4 + Wd, R.y0 + 40 + Hd)]
        dr = [d_["rect"] for d_ in page.get_drawings() if d_.get("rect")]
        box = min(cands, key=lambda c: sum(1 for r in dr if r.intersects(c)))
        page.draw_rect(box, color=(0, 0, 0), fill=(1, 1, 1), width=0.8)
        hoja = next((g["sheet"] for g in geo.values() if g["page"] == pg and g.get("sheet")), "")
        page.insert_text((box.x0 + 6, box.y0 + 14), f"TAKE-OFF LEGEND - {hoja} (partition schedule order)", fontsize=8.5, fontname="hebo")
        for i, t in enumerate(orden):
            y = box.y0 + 28 + 13 * i
            rgb, dashes = cols[t]
            page.draw_line((box.x0 + 8, y - 3), (box.x0 + 40, y - 3), color=rgb, width=2.5,
                           dashes=f"[{dashes[0]} {dashes[1]}] 0" if dashes else None)
            n, L = ts[t]
            page.insert_text((box.x0 + 46, y), f"{t} - {n} wall(s) - {L:,.2f} LF", fontsize=7.5, fontname="helv")


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


def _hojas_inventario(inventario, canon_path):
    """{página base 1: hoja} del inventario.json de inventario_tags.py ({"sheets": [{"page", "sheet"}]}); `inventario` = ruta,
    dict {página: hoja} o None (se busca etapas/1_inventario/inventario.json o inventario.json subiendo desde el canon)."""
    if isinstance(inventario, dict):
        return {int(k): v for k, v in inventario.items() if v}
    p = inventario
    if p is None and isinstance(canon_path, str):
        d = os.path.dirname(os.path.abspath(canon_path))
        for _ in range(5):
            for c in (os.path.join(d, "etapas", "1_inventario", "inventario.json"), os.path.join(d, "1_inventario", "inventario.json"),
                      os.path.join(d, "inventario.json")):
                if os.path.isfile(c):
                    p = c
                    break
            if p or os.path.dirname(d) == d:
                break
            d = os.path.dirname(d)
    if not p or not os.path.isfile(p):
        return {}
    try:
        d = json.load(open(p, encoding="utf-8"))
        return {int(x["page"]): x["sheet"] for x in d.get("sheets") or [] if x.get("sheet")}
    except Exception:                                                   # noqa: BLE001
        return {}


def editable(out_pdf, hojas):
    """U-151 / U-152 (v81cf59): deja el PDF de markups listo para Bluebeam SIN intervención: quita las firmas digitales /Sig del
    set (sello visible aplanado) y pone Page Label = hoja en todas las páginas (quitar_firmas_labels), y la escala de PÁGINA
    /VP con el /Measure de sus markups en cada hoja con markups (escala_pagina). `hojas` = {página base 1: hoja}.
    -> {"firmas_quitadas", "escalas"}. Lo verifica compuerta_entrega.py CE_PDF_EDITABLE."""
    import tempfile
    import escala_pagina
    import quitar_firmas_labels
    fd, tmp = tempfile.mkstemp(suffix=".pdf", dir=os.path.dirname(os.path.abspath(out_pdf)))
    os.close(fd)
    try:
        q = quitar_firmas_labels.quitar(out_pdf, tmp, hojas)
        esc = escala_pagina.poner(tmp, out_pdf)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    return {"firmas_quitadas": q, "escalas": {p: rs for p, rs in esc}}


def escribir(bid_pdf, canon_path, out_pdf, out_json=None, inventario=None):
    """Escribe el PDF de markups y su resumen JSON. -> resumen (dict).
    v81cf59 (U-151 / U-152): el PDF sale sin firmas /Sig, con Page Label = hoja en todas las páginas (hojas del inventario.json de
    inventario_tags.py, `inventario`, + las hojas marcadas) y con escala de página /VP por hoja (editable())."""
    import pymupdf as fitz
    cargar_board(canon_path)
    canon = _cargar(canon_path)
    cargar_board(canon_path)                             # R80f.9
    doc = fitz.open(bid_pdf)
    n_bid = doc.page_count
    geo, sin, notas = geometria(canon, doc)
    cols = colores(canon)
    esc = escala(canon)
    por_hoja, por_type, por_wall = {}, {}, []
    for w in walls(canon):
        g = geo.get(w["id"])
        if not g:
            continue
        t = tipo(w)
        rgb, dashes = cols[t]
        esc_w = escala(canon, g.get("sheet")) or esc
        if w.get("paths"):          # rev8 (v81cf64): wall en varias piezas medidas (tramos a cada lado de un vano, jogs): cada
            trs = [t_ for p_ in w["paths"] for t_ in tramos_rectos([tuple(q) for q in p_])]    # pieza es su markup, sin ajustar
            g["pts"] = [tuple(q) for q in w["paths"][0]]
            g["piezas_w"] = [[tuple(q) for q in p_] for p_ in w["paths"]]
        else:
            g["pts"] = ajustar_a_lf(g["pts"], lf(w), esc_w)   # R80f.9 (BE-117)
            trs = tramos_rectos(g["pts"])
        if len(trs) == 1:
            piezas = [(g["pts"], contenido(w), NM_PREF + w["id"])]
        else:                                            # R80f.37 (U-120): un markup por tramo recto, LF / SF repartidos
            lts = [sum(math.dist(q[i], q[i + 1]) for i in range(len(q) - 1)) for q in trs]
            lfs = repartir(float(lf(w)), lts, 3)        # 3 decimales: un tramo corto no se desvía del Length medido por el redondeo
            m_sf = re.search(r"([\d,]+(?:\.\d+)?) SF board", contenido(w))    # U-153: el SF wall se recalcula por tramo
            sfs = repartir(float(m_sf.group(1).replace(",", "")), lts) if m_sf else [None] * len(trs)
            piezas = [(q, contenido_tramo(w, lf_, sf_), f"{NM_PREF}{w['id']}{SEP_TRAMO}{k}")
                      for k, (q, lf_, sf_) in enumerate(zip(trs, lfs, sfs), 1)]
        for pts_, cont_, nm_ in piezas:
            a = _annot(doc, doc[g["page"]], pts_, rgb, dashes, t, cont_, AUTOR, nm_)
            if esc_w:
                _measure(doc, a, esc_w)
                if altura(w):
                    _depth(doc, a, altura(w))
        k = f"{g['sheet']} (p.{g['page'] + 1})"
        # R80e.82: una fila por wall con las columnas de la lista de markups de Bluebeam (Subject, Page Label, Length,
        # Depth, Wall Area = Length x Depth); Length = largo de los vértices / escala (lo que mide Revu)
        pts = g["pts"]
        lpt = sum(((pts[i + 1][0] - pts[i][0]) ** 2 + (pts[i + 1][1] - pts[i][1]) ** 2) ** 0.5 for i in range(len(pts) - 1))
        lg = round(lpt / esc_w, 2) if esc_w else None
        dp = altura(w)
        por_wall.append({"id": w["id"], "Subject": t, "Page Label": g.get("sheet"), "Length": lg,
                         "LF takeoff": w.get("length_ft"), "Depth": dp,
                         "Wall Area": round(lg * float(dp), 2) if lg is not None and dp else None})
        por_hoja[k] = por_hoja.get(k, 0) + 1
        por_type[t] = por_type.get(t, 0) + 1
    leyendas_por_hoja(doc, canon, geo, cols)               # R80f.10 (BE-117): leyenda en cada hoja marcada
    ley = _leyenda(doc, canon, geo, sin, cols, "the take-off Excel (Partition Takeoff)")   # v80o (BE-48): sin nombres de archivos
    _page_labels(doc, {**{g["page"]: g["sheet"] for g in geo.values() if g.get("sheet")}, ley: "LEGEND"})
    # R80w.26: sin nombre de la herramienta en la metadata del entregable (keywords / creator vacíos, R80e.29 f)
    doc.set_metadata(dict(doc.metadata or {}, keywords="", creator=""))
    os.makedirs(os.path.dirname(os.path.abspath(out_pdf)), exist_ok=True)
    nm_unicos(doc)                                           # U-167: /NM único en todo el PDF y sin '/'
    doc.save(out_pdf, garbage=1, deflate=True)
    doc.close()
    hojas = _hojas_inventario(inventario, canon_path)                  # U-151: Page Label = hoja en TODAS las páginas
    hojas.update({g["page"] + 1: g["sheet"] for g in geo.values() if g.get("sheet")})
    hojas[ley + 1] = "LEGEND"
    ed = editable(out_pdf, hojas)                                      # U-151 / U-152: sin /Sig, labels, /VP por hoja
    res = {"tool": TOOL, "editable": ed, "pdf": os.path.abspath(out_pdf), "bid_set": os.path.abspath(bid_pdf),
           "canon": None if isinstance(canon_path, dict) else os.path.abspath(canon_path),
           "canon_sha": None if isinstance(canon_path, dict) else sha_archivo(canon_path),
           "pdf_sha": sha_archivo(out_pdf), "leyenda": {"pagina": ley + 1, "posicion": "final"},
           "annots": len(geo), "por_hoja": dict(sorted(por_hoja.items())), "por_type": dict(sorted(por_type.items())),
           "totales": totales(canon, geo), "colores": {t: list(c[0]) for t, c in cols.items()},
           "sin_geometria": sin, "conversiones": notas, "walls": por_wall}
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
            nm = nm_leer((a.info or {}).get("id") or "")     # U-167
            vs = a.vertices or []
            try:
                vd = [tuple(fitz.Point(v) * M) for v in vs]
            except Exception:                                          # noqa: BLE001
                vd = []
            out.setdefault(nm, []).append((i, a.type[1], dict(a.info or {}), dict(a.colors or {}), vd,
                                           tuple((a.border or {}).get("dashes") or ())))
    return out


def _verificar_tramos(w, t, g, items, cols, tol):
    """R80f.37: los tramos rectos de un wall: misma página, color, Subject, Author; Contents con el TYPE al principio y el
    Wall ID al final; Σ LF de los tramos = LF del wall; cada tramo sobre el eje y los extremos del eje cubiertos."""
    f_ = []
    rgb = cols[t][0]
    lf_sum, vs_all = 0.0, []
    for pg, tp, info, colors, vd, dashes in items:
        if tp not in ("PolyLine", "Line") or pg != g["page"]:
            f_.append(f"{w['id']}: tramo tipo {tp} / página {pg + 1} (se espera PolyLine en la {g['page'] + 1})")
        st = tuple(colors.get("stroke") or ())
        if len(st) != 3 or max(abs(a - b) for a, b in zip(st, rgb)) > TOL_COLOR:
            f_.append(f"{w['id']}: tramo con color {st} != {rgb}")
        if info.get("subject") != t or info.get("title") != AUTOR:
            f_.append(f"{w['id']}: tramo con Subject / Author distinto")
        c = str(info.get("content") or "")
        if not (c.startswith(t + " ·") and c.endswith("· " + w["id"])):
            f_.append(f"{w['id']}: Contents del tramo '{c[:60]}' sin TYPE / Wall ID")
        m = re.search(r"·\s*([\d,]+(?:\.\d+)?) LF", c)
        lf_sum += float(m.group(1).replace(",", "")) if m else 0.0
        if len(vd) < 2 or max(min(_dist_poli(v, q_) for q_ in (g.get("piezas_w") or [g["pts"]])) for v in vd) > tol:
            f_.append(f"{w['id']}: tramo fuera del eje del wall")
        vs_all += vd
        if len(vd) >= 3 and tramos_rectos(vd) and len(tramos_rectos(vd)) > 1:
            f_.append(f"{w['id']}: un tramo todavía dobla (U-120)")
    if abs(lf_sum - float(lf(w))) > 0.011:
        f_.append(f"{w['id']}: Σ LF de los tramos {lf_sum:.2f} != LF {lf(w):.2f}")
    eje = g["pts"]
    if vs_all and max(min(math.hypot(e[0] - v[0], e[1] - v[1]) for v in vs_all) for e in (eje[0], eje[-1])) > tol:
        f_.append(f"{w['id']}: los tramos no cubren los extremos del eje")
    return f_


def verificar(pdf, canon, tol=TOL_PT, detalle=None):
    """Abre el PDF de markups y lo compara con el canon. -> lista de fallas ([] = OK).
    Exige: una annot PolyLine / Line por wall con geometría (en su página), color del type, Subject = type,
    Contents "TYPE · LF · H · SF · N/HOJA · id", Author "Take-off", vértices sobre el eje del canon (<= tol pt) cubriendo sus
    dos extremos; ninguna annot "TO-" de un wall que no está en el canon; leyenda al final con cada type."""
    import pymupdf as fitz
    cargar_board(canon)                                  # R80f.9
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
        if nm.startswith(NM_PREF) and not nm.startswith(NM_LEY) and nm[len(NM_PREF):].split(SEP_TRAMO)[0] not in ids:
            fallas.append(f"annot {nm}: wall que no está en el canon")
    for w in walls(canon):
        g = geo.get(w["id"])
        if not g:
            continue
        t = tipo(w)
        lst = an.get(NM_PREF + w["id"]) or []
        legs = sorted((k for k in an if k.startswith(NM_PREF + w["id"] + SEP_TRAMO)), key=lambda k: int(k.rsplit(SEP_TRAMO, 1)[1]))
        if legs and not lst:                             # R80f.37: tramos rectos de un wall que dobla
            fallas += _verificar_tramos(w, t, g, [an[k][0] for k in legs], cols, tol)
            continue
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
    vistos, ok = [], []
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
                    ok.append((os.path.getmtime(p), p, r))
    if ok:          # R80f.8 (v81cf13, Chuze): varias versiones con el mismo canon (FINAL3 / FINAL4) -> la más reciente
        return max(ok, key=lambda x: (x[0], x[1]))[2], None
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
    cargar_board(canon)
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


# ----------------------------------------------------------------------------------------------- U-153 arreglo de un PDF entregado
def arreglar_sf_wall(src, dst):
    """U-153 / BE-149 (v81cf60): arregla un PDF de markups YA ENTREGADO sin rehacerlo: /DepthUnit /C 1 en todo markup con /Depth
    y etiqueta de wall con "<LF x H> SF wall (LF\u00d7H)" (LF de la etiqueta x /Depth = el Wall Area que muestra Bluebeam) delante
    del "SF board (faces\u00d7layers)"; una etiqueta de wall sin board con "<x> SF" pasa a "<LF x H> SF wall (LF\u00d7H)". La
    DEMO (U-143) ya rotula SF = LF x H y solo recibe /C 1. -> {"depthunit": n, "etiquetas": n, "sin_cambio": n}."""
    import pikepdf
    pdf = pikepdf.open(src)
    n = {"depthunit": 0, "etiquetas": 0, "sin_cambio": 0}
    for page in pdf.pages:
        for a in page.obj.get("/Annots") or []:
            try:
                nm = str(a.get("/NM") or "")
                du = a.get("/DepthUnit")
                dep = a.get("/Depth")
            except Exception:                                           # noqa: BLE001
                continue
            if du is not None:
                for nf in du:
                    if float(nf.get("/C", 1)) != DEPTH_C:
                        nf.C = DEPTH_C
                        n["depthunit"] += 1
            if dep is None or not nm.startswith(NM_PREF) or nm.startswith(NM_LEY):
                continue
            c = str(a.get("/Contents") or "")
            if "SF wall" in c:
                n["sin_cambio"] += 1
                continue
            parts = c.split(" · ")
            m_lf = re.match(r"\s*([\d,]+(?:\.\d+)?) LF$", parts[1]) if len(parts) > 2 else None
            i_h = next((k for k, x in enumerate(parts) if x.startswith("H ")), None)
            if not m_lf or i_h is None:
                n["sin_cambio"] += 1
                continue
            wsf = float(m_lf.group(1).replace(",", "")) * float(dep)
            nuevo = f"{wsf:,.2f} {SF_WALL}"
            i_b = next((k for k, x in enumerate(parts) if re.fullmatch(r"[\d,]+(?:\.\d+)? SF board", x)), None)
            if i_b is not None:
                parts[i_b] += " (faces\u00d7layers)"
                parts.insert(i_h + 1, nuevo)
            else:
                i_s = next((k for k, x in enumerate(parts) if re.fullmatch(r"[\d,]+(?:\.\d+)? SF", x)), None)
                if i_s is None:
                    n["sin_cambio"] += 1
                    continue
                parts[i_s] = nuevo
            a.Contents = pikepdf.String(" · ".join(parts))
            n["etiquetas"] += 1
    pdf.save(dst)
    pdf.close()
    return n


def main(argv):
    a = list(argv[1:])
    tol = TOL_PT
    if "--tol" in a:
        i = a.index("--tol")
        tol = float(a[i + 1])
        del a[i:i + 2]
    if len(a) == 3 and a[0] == "sf_wall":           # U-153: markups_bluebeam.py sf_wall <entregado.pdf> <nuevo.pdf>
        print(json.dumps(arreglar_sf_wall(a[1], a[2]), ensure_ascii=False))
        return 0
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
        inv = a[a.index("--inventario") + 1] if "--inventario" in a else None
        r = escribir(a[0], a[1], a[2], js, inv)
        print(f"firmas /Sig quitadas: {r['editable']['firmas_quitadas']} · escala de página /VP: {r['editable']['escalas']}")
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
