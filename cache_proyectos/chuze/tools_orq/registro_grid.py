"""registro_grid.py — traslación ampliada -> A101 por burbujas de grid (numéricas fijan x, de letra fijan y).
Candidato dx = X_A101[label] - k * x_label_ampliada; se toma el cluster (±1.5 pt) con más etiquetas distintas."""
import fitz, json, re, collections
P = '/tmp/chuze/plano/bidset_SIN_MARKUPS.pdf'
C = json.load(open('/tmp/chuze/work/etapas/2_lectura/comun/constants.json'))['constants']['plan_scale_by_sheet']
PAGES = {'A421':22,'A422':26,'A423':30,'A424':33,'A425':37,'A426':41,'A427':43,'A428':45,'A429':47,'A431':50,'A432':52,'A434':53,'A435':55}
NUM = re.compile(r'^\d(?:\.5)?$'); LET = re.compile(r'^[A-I](?:\.\d)?$')
def labels(p, size_min):
    out = []
    for b in p.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            for s in l['spans']:
                t = s['text'].strip()
                if s['size'] >= size_min and (NUM.match(t) or LET.match(t)):
                    r = fitz.Rect(s['bbox']); out.append((t, (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2, s['size']))
    return out
d = fitz.open(P)
# A101: posición de cada grid (mediana de sus burbujas)
L0 = labels(d[13], 8)
gx = collections.defaultdict(list); gy = collections.defaultdict(list)
for t, x, y, sz in L0:
    (gx if NUM.match(t) else gy)[t].append(x if NUM.match(t) else y)
X0 = {k: sorted(v)[len(v) // 2] for k, v in gx.items()}; Y0 = {k: sorted(v)[len(v) // 2] for k, v in gy.items()}
def cluster(c):
    best = (0, None)
    for _, v in c:
        g = {t for t, w in c if abs(w - v) <= 1.5}
        if len(g) > best[0]: best = (len(g), sorted(w for t, w in c if abs(w - v) <= 1.5))
    return (best[1][len(best[1]) // 2], best[0]) if best[1] else (None, 0)
reg = {}
for s, pg in PAGES.items():
    k = C['A101']['value'] / C[s]['value']
    L = labels(d[pg - 1], 8)
    cxs = [(t, X0[t] - k * x) for t, x, y, sz in L if t in X0]
    cys = [(t, Y0[t] - k * y) for t, x, y, sz in L if t in Y0]
    dx, nx = cluster(cxs); dy, ny = cluster(cys)
    reg[s] = {'k': k, 'dx': dx, 'dy': dy, 'grids_x': nx, 'grids_y': ny}
    print(s, reg[s])
json.dump({'A101_grids_x': X0, 'A101_grids_y': Y0, 'hojas': reg}, open('/tmp/chuze/work/etapas/3_revision/registro_grid.json', 'w'), indent=1)
