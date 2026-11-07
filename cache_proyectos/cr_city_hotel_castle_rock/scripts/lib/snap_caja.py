"""E2 (auditoría COORDINACIÓN 7-nov): el lado de un shower se mide a la CARA DEL WALL (línea de muro >= 1.0 pt), no al extremo
de las diagonales del shower pan. snap(pg, caja) mueve cada lado hacia afuera hasta la cara de muro más cercana (<= 6 pt) que
cubra >= 50 % del lado; si no hay muro (curb / vidrio) el lado no se mueve."""
_cache = {}


def _thick(pg, todas=False):
    k = (id(pg), todas)
    if k not in _cache:
        H, V = [], []
        for dr in pg.get_drawings():
            if not todas and (dr.get('width') or 0) < 1.0:
                continue
            for it in dr['items']:
                if it[0] == 're' and todas:
                    r = it[1]
                    H += [(r.y0, r.x0, r.x1), (r.y1, r.x0, r.x1)]; V += [(r.x0, r.y0, r.y1), (r.x1, r.y0, r.y1)]
                if it[0] == 'l':
                    a, b = it[1], it[2]
                    if abs(a.y - b.y) < 0.3 and abs(a.x - b.x) > 2:
                        H.append((a.y, min(a.x, b.x), max(a.x, b.x)))
                    elif abs(a.x - b.x) < 0.3 and abs(a.y - b.y) > 2:
                        V.append((a.x, min(a.y, b.y), max(a.y, b.y)))
        _cache[k] = (H, V)
    return _cache[k]


def _cubre(lo, hi, a, b):
    return max(0.0, min(hi, b) - max(lo, a)) >= 0.5 * (hi - lo)


def snap(pg, x0, x1, y0, y1, tol=6.0):
    """Un lado que YA está sobre una línea dibujada (cualquier grosor, +-0.6 pt, >= 50 % del lado) no se mueve."""
    H, V = _thick(pg)
    Ht, Vt = _thick(pg, True)
    def mejor(lines, c, lo, hi, hacia):
        todas = Vt if lines is V else Ht
        if any(abs(p - c) <= 0.6 and _cubre(lo, hi, a, b) for p, a, b in todas):
            return c
        # cara de muro gruesa justo ADENTRO del lado (<= 2.5 pt): el lado ya está en el muro (309 top, 404 E)
        if any(0 < (p - c) * hacia <= 2.5 and _cubre(lo, hi, a, b) for p, a, b in lines):
            return c
        cand = [p for p, a, b in lines if _cubre(lo, hi, a, b) and (0 <= (c - p) * hacia <= tol)]
        return (max(cand) if hacia > 0 else min(cand)) if cand else c
    return (mejor(V, x0, y0, y1, +1), mejor(V, x1, y0, y1, -1), mejor(H, y0, x0, x1, +1), mejor(H, y1, x0, x1, -1))
