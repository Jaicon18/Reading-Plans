# -*- coding: utf-8 -*-
"""geo.py -- geometria vectorial de una hoja del set, cacheada.

REGLA 41: siempre la copia SIN /Annots.
Escala floor plan A02.01: 1/4"=1'-0" -> 18.0 pt/ft, 1.5 pt por pulgada real.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (antes fijas en /home/claude/boa)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", "/home/claude/boa")
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import os, pickle, math

PDF = f'{_TW}/BOA_SIN_MARKUPS.pdf'
PT_FT = 18.0
PT_IN = 1.5
CACHE = f'{_TW}/.geocache'


def load(page_index):
    os.makedirs(CACHE, exist_ok=True)
    f = os.path.join(CACHE, 'pg%d.pkl' % page_index)
    if os.path.exists(f):
        return pickle.load(open(f, 'rb'))
    import pdfplumber
    with pdfplumber.open(PDF) as pdf:
        pg = pdf.pages[page_index]
        H, V = [], []

        def add(x0, y0, x1, y1, lw):
            x0, x1 = min(x0, x1), max(x0, x1)
            y0, y1 = min(y0, y1), max(y0, y1)
            if abs(y1 - y0) < 0.3 and abs(x1 - x0) >= 0.3:
                H.append((round((y0 + y1) / 2, 2), round(x0, 2), round(x1, 2), round(lw, 2)))
            elif abs(x1 - x0) < 0.3 and abs(y1 - y0) >= 0.3:
                V.append((round((x0 + x1) / 2, 2), round(y0, 2), round(y1, 2), round(lw, 2)))

        D = []   # diagonales: (x0,y0,x1,y1,lw,largo_pt,ang_deg)
        for o in pg.lines:
            lw = o.get('linewidth') or 0.0
            x0, y0, x1, y1 = o['x0'], o['top'], o['x1'], o['bottom']
            dx, dy = abs(x1 - x0), abs(y1 - y0)
            if dx >= 0.3 and dy >= 0.3:
                D.append((round(x0,2), round(y0,2), round(x1,2), round(y1,2), round(lw,2),
                          round(math.hypot(x1-x0, y1-y0),2),
                          round(math.degrees(math.atan2(y1-y0, x1-x0)),2)))
            else:
                add(x0, y0, x1, y1, lw)
        for o in pg.rects:
            lw = o.get('linewidth') or 0.0
            x0, x1, y0, y1 = o['x0'], o['x1'], o['top'], o['bottom']
            if abs(y1 - y0) < 0.3 or abs(x1 - x0) < 0.3:
                add(x0, y0, x1, y1, lw)
            else:
                add(x0, y0, x1, y0, lw); add(x0, y1, x1, y1, lw)
                add(x0, y0, x0, y1, lw); add(x1, y0, x1, y1, lw)
        # curvas: pueden traer diagonales de muro inclinado
        for o in getattr(pg, 'curves', []):
            lw = o.get('linewidth') or 0.0
            pts = o.get('pts') or []
            for i in range(len(pts) - 1):
                (ax, ay), (bx, by) = pts[i], pts[i + 1]
                dx, dy = abs(bx - ax), abs(by - ay)
                if dx >= 0.3 and dy >= 0.3:
                    D.append((round(ax,2), round(ay,2), round(bx,2), round(by,2), round(lw,2),
                              round(math.hypot(bx-ax, by-ay),2),
                              round(math.degrees(math.atan2(by-ay, bx-ax)),2)))
                else:
                    add(ax, ay, bx, by, lw)
        words = [{'t': w['text'], 'x0': round(w['x0'],2), 'x1': round(w['x1'],2),
                  'y0': round(w['top'],2), 'y1': round(w['bottom'],2),
                  'up': w.get('upright', True)} for w in pg.extract_words()]
        wpt, hpt = float(pg.width), float(pg.height)
    d = {'H': H, 'V': V, 'D': D, 'words': words, 'w_pt': wpt, 'h_pt': hpt}
    pickle.dump(d, open(f, 'wb'))
    return d


def ft(pt):   return pt / PT_FT
def inch(pt): return pt / PT_IN
def fmt(pt):
    """pt -> pies-pulgadas legibles."""
    v = pt / PT_FT
    f = int(v); i = (v - f) * 12
    return "%d'-%.2f\"" % (f, i)


def corridas(lines, c, tol=0.4, lw_min=1.1):
    """Tramos colineales de una coordenada c (V: x; H: y) con lw>=lw_min."""
    out = [l for l in lines if abs(l[0] - c) <= tol and l[3] >= lw_min]
    return sorted(out, key=lambda l: l[1])


def near_words(words, x, y, r=40):
    return sorted([w for w in words
                   if abs((w['x0']+w['x1'])/2 - x) <= r and abs((w['y0']+w['y1'])/2 - y) <= r],
                  key=lambda w: (abs((w['x0']+w['x1'])/2 - x) + abs((w['y0']+w['y1'])/2 - y)))
