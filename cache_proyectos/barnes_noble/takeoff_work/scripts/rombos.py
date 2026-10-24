"""Detecta símbolos de partition tag (rombo) en hojas con texto vectorizado. Uso: rombos.py pdf pagina out.json"""
import sys, json, pymupdf as fitz
pdf, pno = sys.argv[1], int(sys.argv[2])
d = fitz.open(pdf); p = d[pno-1]; M = p.rotation_matrix
out = []
for dr in p.get_drawings():
    its = dr['items']
    pts = []
    if all(s[0] == 'l' for s in its) and 4 <= len(its) <= 8:
        for s in its: pts += [fitz.Point(s[1]) * M, fitz.Point(s[2]) * M]
    elif len(its) == 1 and its[0][0] == 'qu':
        q = its[0][1]; pts = [fitz.Point(x) * M for x in (q.ul, q.ur, q.lr, q.ll)]
    else:
        continue
    xs = [a.x for a in pts]; ys = [a.y for a in pts]
    w, h = max(xs)-min(xs), max(ys)-min(ys)
    if not (18 < w < 28 and 18 < h < 28): continue
    cx, cy = (max(xs)+min(xs))/2, (max(ys)+min(ys))/2
    if not all((abs(a.x-cx) < 1.0) or (abs(a.y-cy) < 1.0) for a in pts): continue
    r = {'cx': round(cx, 2), 'cy': round(cy, 2), 'w': round(w, 1), 'h': round(h, 1)}
    if not any(abs(r['cx']-o['cx']) < 2 and abs(r['cy']-o['cy']) < 2 for o in out):
        out.append(r)
out.sort(key=lambda r: (round(r['cy']/40), r['cx']))
for i, r in enumerate(out): r['id'] = i
print(pno, len(out), file=sys.stderr)
json.dump(out, open(sys.argv[3], 'w'), indent=0)
