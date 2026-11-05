"""R-ALC-06: demolition plan D100 vs new floor plan A100, element by element. D100 is registered to A100 by 20 identical wall
poche rectangles (dx +71.0 / dy +199.65 pt, same 1/4" scale). Each demo line is moved to the A100 frame and crossed with the
new walls (bands) within 10 pt; each new wall is crossed back. Writes etapas/DEMO_CRUCE.md. Text only."""
import json, math
K = '/root/cc/work'
c = json.load(open(f'{K}/etapas/4_canon/takeoff_canon.json'))
g = json.load(open(f'{K}/etapas/4_canon/demo_geom.json'))
DX, DY = 71.0, 199.65
def seg_band(w):
    b = w['band']; m = (b['c0'] + b['c1']) / 2
    return ((b['lo'], m), (b['hi'], m)) if b['ori'] == 'H' else ((m, b['lo']), (m, b['hi']))
def near(s1, s2, tol=10.0):
    (a, b), (c_, d) = s1, s2
    hor1, hor2 = abs(a[1] - b[1]) < 1, abs(c_[1] - d[1]) < 1
    if hor1 != hor2: return 0.0
    if hor1:
        if abs(a[1] - c_[1]) > tol: return 0.0
        lo, hi = max(min(a[0], b[0]), min(c_[0], d[0])), min(max(a[0], b[0]), max(c_[0], d[0]))
    else:
        if abs(a[0] - c_[0]) > tol: return 0.0
        lo, hi = max(min(a[1], b[1]), min(c_[1], d[1])), min(max(a[1], b[1]), max(c_[1], d[1]))
    return max(0.0, hi - lo) / 18.0
L = ["# DEMO_CRUCE - D100 demolition vs A100 new floor plan (wall by wall)", "",
     "Registration D100 -> A100: dx +71.0 / dy +199.65 pt (20 identical wall poche rectangles, 1/4\" = 1'-0\" both).", "",
     "| Demo element | LF | New wall on the same line (overlap LF) | Result |", "|---|---|---|---|"]
for e in g:
    s = tuple((x - DX, y - DY) for x, y in e['polyline'])
    hits = [(w['id'], round(near(s, seg_band(w)), 2)) for w in c['walls'] if near(s, seg_band(w)) > 0.5]
    L.append(f"| {e['id']} | {e['lf']} | {', '.join(f'{i} ({v})' for i, v in hits) or 'none'} | " +
             ("demolished, new wall on the same line" if hits else "demolished, no new wall on this line") + " |")
L += ["", "| New wall | On a demolished line | Result |", "|---|---|---|"]
for w in c['walls']:
    hits = [e['id'] for e in g if near(tuple((x - DX, y - DY) for x, y in e['polyline']), seg_band(w)) > 0.5]
    L.append(f"| {w['id']} | {', '.join(hits) or '-'} | {'new, replaces demolished element' if hits else 'new'} |")
open(f'{K}/etapas/DEMO_CRUCE.md', 'w').write('\n'.join(L) + '\n'); print('\n'.join(L[4:12]))
