"""Vector helpers: line segments of a page (pymupdf get_drawings), filtered."""
import pymupdf as fitz
PDF = '/root/cr/work/plans/bidset_SIN_MARKUPS.pdf'
_cache = {}
def segs(pi):
    if pi in _cache: return _cache[pi]
    p = fitz.open(PDF)[pi]; out = []
    for d in p.get_drawings():
        w = d.get('width') or 0
        for it in d['items']:
            if it[0] == 'l':
                a, b = it[1], it[2]; out.append((a.x, a.y, b.x, b.y, w))
            elif it[0] == 're':
                r = it[1]
                for (x0,y0,x1,y1) in ((r.x0,r.y0,r.x1,r.y0),(r.x1,r.y0,r.x1,r.y1),(r.x1,r.y1,r.x0,r.y1),(r.x0,r.y1,r.x0,r.y0)):
                    out.append((x0,y0,x1,y1,w))
    _cache[pi] = out; return out
def near_vertical(pi, x, y0, y1, tol=6, minlen=3):
    """vertical segments within tol of x overlapping [y0,y1]"""
    r = []
    for (a,b,c,d,w) in segs(pi):
        if abs(a-c) < 0.3 and abs(a-x) <= tol and abs(b-d) >= minlen:
            lo, hi = min(b,d), max(b,d)
            if hi > y0 and lo < y1: r.append((round(a,2), round(lo,2), round(hi,2), round(w,2)))
    return sorted(set(r))
def near_horizontal(pi, y, x0, x1, tol=6, minlen=3):
    r = []
    for (a,b,c,d,w) in segs(pi):
        if abs(b-d) < 0.3 and abs(b-y) <= tol and abs(a-c) >= minlen:
            lo, hi = min(a,c), max(a,c)
            if hi > x0 and lo < x1: r.append((round(b,2), round(lo,2), round(hi,2), round(w,2)))
    return sorted(set(r))
def h_touching_x(pi, x, y0, y1, tol=4, minlen=2):
    """horizontal segments with an endpoint within tol of x, y in [y0,y1] (junctions on a vertical wall face)"""
    r = []
    for (a,b,c,d,w) in segs(pi):
        if abs(b-d) < 0.3 and y0 <= b <= y1 and abs(a-c) >= minlen and (abs(a-x) <= tol or abs(c-x) <= tol):
            r.append((round(b,2), round(min(a,c),2), round(max(a,c),2), round(w,2)))
    return sorted(set(r))
def v_touching_y(pi, y, x0, x1, tol=4, minlen=2):
    r = []
    for (a,b,c,d,w) in segs(pi):
        if abs(a-c) < 0.3 and x0 <= a <= x1 and abs(b-d) >= minlen and (abs(b-y) <= tol or abs(d-y) <= tol):
            r.append((round(a,2), round(min(b,d),2), round(max(b,d),2), round(w,2)))
    return sorted(set(r))
