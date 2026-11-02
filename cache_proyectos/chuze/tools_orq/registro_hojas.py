"""registro_hojas.py — traslación de cada planta ampliada a coordenadas de A101 (escala conocida por rótulo).
Candidatos dx, dy = picos del histograma de diferencias de líneas largas; se elige el PAR (dx, dy) con más segmentos
enteros coincidentes (posición ±0.75 pt y traslape ≥ 60 % en la otra dirección). Salida registro_hojas.json."""
import fitz, json, collections, bisect
P = '/tmp/chuze/plano/bidset_SIN_MARKUPS.pdf'
C = json.load(open('/tmp/chuze/work/etapas/2_lectura/comun/constants.json'))['constants']['plan_scale_by_sheet']
PAGES = {'A421':22,'A422':26,'A423':30,'A424':33,'A425':37,'A426':41,'A427':43,'A428':45,'A429':47,'A431':50,'A432':52,'A434':53,'A435':55}
def lines(p, minlen):
    H, V = [], []
    W = p.rect.width
    for dr in p.get_drawings():
        for it in dr['items']:
            if it[0] != 'l': continue
            a, b = it[1], it[2]
            if max(a.x, b.x) > W * 0.86: continue
            if abs(a.y - b.y) < 0.2 and abs(a.x - b.x) >= minlen: H.append((a.y, min(a.x, b.x), max(a.x, b.x)))
            if abs(a.x - b.x) < 0.2 and abs(a.y - b.y) >= minlen: V.append((a.x, min(a.y, b.y), max(a.y, b.y)))
    return H, V
def peaks(base, mov, k, n=6):
    bc = collections.Counter(round(b * 2) for b in base); h = collections.Counter()
    for m in mov:
        for b2 in bc: h[round(b2 - m * k * 2)] += 1
    return [o / 2.0 for o, _ in h.most_common(n)]
def index(L):
    L = sorted(L); return L, [l[0] for l in L]
def score(base_idx, mov, k, d_par, d_perp):
    L, keys = base_idx; s = 0
    for c, a, b in mov:
        c2, a2, b2 = c * k + d_par, a * k + d_perp, b * k + d_perp
        i = bisect.bisect_left(keys, c2 - 0.75)
        while i < len(keys) and keys[i] <= c2 + 0.75:
            _, x0, x1 = L[i]
            ov = min(b2, x1) - max(a2, x0)
            if ov >= 0.6 * (b2 - a2): s += 1; break
            i += 1
    return s
d = fitz.open(P)
H0, V0 = lines(d[13], 8); iH, iV = index(H0), index(V0)
reg = {}
for s, pg in PAGES.items():
    k = C['A101']['value'] / C[s]['value']
    H, V = lines(d[pg - 1], 40)
    cx = peaks([v[0] for v in V0], [v[0] for v in V], k); cy = peaks([h[0] for h in H0], [h[0] for h in H], k)
    best = max(((score(iV, V, k, dx, dy) + score(iH, H, k, dy, dx), dx, dy) for dx in cx for dy in cy))
    sc, dx, dy = best
    reg[s] = {'k': k, 'dx': dx, 'dy': dy, 'matches': sc, 'n_lines': len(H) + len(V), 'ratio': round(sc / max(1, len(H) + len(V)), 3)}
    print(s, reg[s])
json.dump(reg, open('/tmp/chuze/work/etapas/3_revision/registro_hojas.json', 'w'), indent=1)
