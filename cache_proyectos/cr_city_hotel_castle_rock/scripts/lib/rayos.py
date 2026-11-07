"""Rectángulo de un cuarto por rayos desde una semilla hasta la cara de muro más cercana (línea >= 1.0 pt) en los 4 sentidos.
O1 rev6: perímetro real del angle molding para los cuartos con área = SF impreso. Toda semilla se verifica con imagen."""
import pymupdf as fitz
_c = {}


def lineas(pg):
    if id(pg) not in _c:
        H, V = [], []
        for dr in pg.get_drawings():
            if (dr.get('width') or 0) < 1.0:
                continue
            for it in dr['items']:
                if it[0] == 'l':
                    a, b = it[1], it[2]
                    if abs(a.y - b.y) < 0.3 and abs(a.x - b.x) > 1.5:
                        H.append((a.y, min(a.x, b.x), max(a.x, b.x)))
                    elif abs(a.x - b.x) < 0.3 and abs(a.y - b.y) > 1.5:
                        V.append((a.x, min(a.y, b.y), max(a.y, b.y)))
                elif it[0] == 're':
                    r = it[1]
                    if r.width > 1.5: H += [(r.y0, r.x0, r.x1), (r.y1, r.x0, r.x1)]
                    if r.height > 1.5: V += [(r.x0, r.y0, r.y1), (r.x1, r.y0, r.y1)]
        _c[id(pg)] = (H, V)
    return _c[id(pg)]


def caja(pg, x, y):
    H, V = lineas(pg)
    izq = max((p for p, a, b in V if p < x - 0.3 and a <= y <= b), default=None)
    der = min((p for p, a, b in V if p > x + 0.3 and a <= y <= b), default=None)
    arr = max((p for p, a, b in H if p < y - 0.3 and a <= x <= b), default=None)
    aba = min((p for p, a, b in H if p > y + 0.3 and a <= x <= b), default=None)
    return izq, der, arr, aba
