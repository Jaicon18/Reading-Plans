import sys, json, pymupdf as fitz
pdf, pno, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
lo, hi = float(sys.argv[4]), float(sys.argv[5])
d = fitz.open(pdf); p = d[pno-1]; M = p.rotation_matrix
R = []
for dr in p.get_drawings():
    its = dr['items']
    if len(its) in (4,) and all(i[0] == 'c' for i in its):
        r = fitz.Rect(dr['rect']) * M
        if lo < r.width < hi and abs(r.width - r.height) < 0.6:
            c = ((r.x0+r.x1)/2, (r.y0+r.y1)/2)
            if not any(abs(c[0]-q['cx']) < 1 and abs(c[1]-q['cy']) < 1 for q in R):
                R.append({'cx': round(c[0], 2), 'cy': round(c[1], 2), 'w': round(r.width, 1), 'h': round(r.height, 1)})
R.sort(key=lambda r: (round(r['cy']/40), r['cx']))
for i, r in enumerate(R): r['id'] = i
json.dump(R, open(out, 'w')); print(len(R), sorted(set(r['w'] for r in R))[:20])
