"""rev8 (COORDINACIÓN 7-nov, revisión de walls punto 2): un markup de wall sigue la geometría medida del wall: cada vértice y el
punto medio de cada tramo caen DENTRO de la banda del wall dibujada en el vector (a <= tol de una línea del plano; tol = medio
grosor del wall + 1.5 pt). Devuelve los markups fuera: (nm, página, label, peor distancia pt, punto)."""
import math
import pymupdf as fitz


def _segs(page):
    S = []
    for dr in page.get_drawings():
        if (dr.get('width') or 0) < 0.3:
            continue
        for it in dr['items']:
            if it[0] == 'l':
                S.append((it[1].x, it[1].y, it[2].x, it[2].y))
            elif it[0] == 're':
                r = it[1]
                S += [(r.x0, r.y0, r.x1, r.y0), (r.x1, r.y0, r.x1, r.y1), (r.x0, r.y1, r.x1, r.y1), (r.x0, r.y0, r.x0, r.y1)]
    return S


def _d(px, py, s):
    x0, y0, x1, y1 = s
    dx, dy = x1 - x0, y1 - y0
    L2 = dx * dx + dy * dy
    t = 0 if L2 == 0 else max(0, min(1, ((px - x0) * dx + (py - y0) * dy) / L2))
    return math.hypot(px - (x0 + t * dx), py - (y0 + t * dy))


def revisar(markups_pdf, plano_pdf, pag_plano, tol=5.0, prefijo=("TO-",), excluir=("TO-CLG", "TO-SOF", "TO-RS6", "TO-CAN", "TO-BW", "TO-LEGEND", "TO-L")):
    """pag_plano: {label: índice de página en el plano limpio}. Solo polilíneas (walls)."""
    dm = fitz.open(markups_pdf)
    dp = fitz.open(plano_pdf)
    out, n = [], 0
    cache = {}
    for i in range(dm.page_count):
        pg = dm[i]
        lab = pg.get_label()
        if lab not in pag_plano:
            continue
        for a in pg.annots() or []:
            nm = a.info.get('id') or ''
            nm = dm.xref_get_key(a.xref, 'NM')[1].strip('()') if not nm else nm
            if a.type[1] != 'PolyLine' or not nm.startswith(prefijo) or nm.startswith(excluir):
                continue
            if lab not in cache:
                cache[lab] = _segs(dp[pag_plano[lab]])
            S = cache[lab]
            M = pg.rotation_matrix
            vs = [fitz.Point(p) * ~pg.derotation_matrix if False else fitz.Point(p) for p in a.vertices]
            pts = list(vs)   # vértices (un tramo puede cruzar un vano cargado sin descontar, U-057)
            peor = max(((min(_d(p.x, p.y, s) for s in S), (round(p.x, 1), round(p.y, 1))) for p in pts), default=(0, None))
            n += 1
            if peor[0] > tol:
                out.append((nm, i + 1, lab, round(peor[0], 1), peor[1]))
    return n, out
