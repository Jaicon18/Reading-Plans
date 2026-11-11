"""R-ALC-06: demolition plan A1.0 vs new partition plan A2.0, element by element. A1.0 is registered to A2.0 by the canon offset
(constants.plan_scale_pt_per_ft.source: 'A1.0=A2.0+(81.6,6.84)', north wall 1160.40 pt on A1.0 vs 1160.28 pt on A2.0, same
1/4" = 1'-0"). Each demo line (etapas/4_canon/demo_geom.json) is moved to the A2.0 frame and crossed with the new walls (bands)
within 10 pt; each new wall is crossed back. Writes etapas/DEMO_CRUCE.md. Text only."""
import json, os, re
K = os.environ.get("K") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
c = json.load(open(f'{K}/etapas/4_canon/takeoff_canon.json'))
g = json.load(open(f'{K}/etapas/4_canon/demo_geom.json'))
S = float(c['constants']['plan_scale_pt_per_ft']['value'])
m = re.search(r"A1\.0\s*=\s*A2\.0\s*\+\s*\(([\d.]+),\s*([\d.]+)\)", c['constants']['plan_scale_pt_per_ft']['source'])
DX, DY = float(m.group(1)), float(m.group(2))


def seg_band(w):
    b = w['band']; mm = (b['c0'] + b['c1']) / 2
    if b['ori'] == 'BOX':
        return None
    return ((b['lo'], mm), (b['hi'], mm)) if b['ori'] == 'H' else ((mm, b['lo']), (mm, b['hi']))


def near(s1, s2, tol=10.0):
    if s1 is None or s2 is None:
        return 0.0
    (a, b), (c_, d) = s1, s2
    hor1, hor2 = abs(a[1] - b[1]) < 1, abs(c_[1] - d[1]) < 1
    if hor1 != hor2: return 0.0
    if hor1:
        if abs(a[1] - c_[1]) > tol: return 0.0
        lo, hi = max(min(a[0], b[0]), min(c_[0], d[0])), min(max(a[0], b[0]), max(c_[0], d[0]))
    else:
        if abs(a[0] - c_[0]) > tol: return 0.0
        lo, hi = max(min(a[1], b[1]), min(c_[1], d[1])), min(max(a[1], b[1]), max(c_[1], d[1]))
    return max(0.0, hi - lo) / S


L = ["# DEMO_CRUCE - A1.0 demolition plan vs A2.0 partition plan (element by element)", "",
     f"Registration A1.0 -> A2.0: dx -{DX} / dy -{DY} pt (canon constants; same 1/4\" = 1'-0\" = {S:g} pt/ft).", "",
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
open(f'{K}/etapas/DEMO_CRUCE.md', 'w').write('\n'.join(L) + '\n'); print('\n'.join(L[4:16]))
