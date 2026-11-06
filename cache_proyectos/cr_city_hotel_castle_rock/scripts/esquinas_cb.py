#!/usr/bin/env python3
"""CR City Hotel - corner bead por programa (cierra RFI-19: el plano lo resuelve, no es RFI).
Por hoja (marco de coordenadas propio): walls board-only deduplicados por geometría (las entradas por cara se suman),
uniones por extremos a la escala impresa de la hoja:
  - L (dos extremos que se tocan, 60-120 grados) entre dos walls con board en las DOS caras -> 1 outside corner
  - extremo libre de un wall con board en las dos caras que NO es jamb de door opening (otro extremo libre a 2.0-4.5 ft)
    -> 2 outside corners (end of partition: corner bead a cada cara)
  - T / continuación / extremo contra un wall de 1 cara (exterior / shaft) -> 0
LF = n esquinas x altura del wall (height_ft de la fuente impresa del wall). Salida: etapas/4_canon/out/corner_bead.json
+ una imagen circulada por hoja (etapas/4_canon/img/cb/)."""
import json, math, os, collections
import pymupdf as fitz

W = '/root/cr/work'
C = json.load(open(f'{W}/etapas/4_canon/takeoff_canon.json'))
PDF = f'{W}/plans/bidset_SIN_MARKUPS.pdf'
SC = {k: (v['value'] if isinstance(v, dict) else v) for k, v in (C['constants'].get('plan_scale_by_sheet') or {}).items()}
OUT = f'{W}/etapas/4_canon/img/cb'
os.makedirs(OUT, exist_ok=True)


def dseg(p, a, b):
    ax, ay = a; bx, by = b; px, py = p
    L2 = (bx - ax) ** 2 + (by - ay) ** 2
    if L2 == 0:
        return math.dist(p, a), 0.0
    t = max(0, min(1, ((px - ax) * (bx - ax) + (py - ay) * (by - ay)) / L2))
    return math.dist(p, (ax + t * (bx - ax), ay + t * (by - ay))), t


def ang(s, t):
    v1 = (s[1][0] - s[0][0], s[1][1] - s[0][1]); v2 = (t[1][0] - t[0][0], t[1][1] - t[0][1])
    n = math.hypot(*v1) * math.hypot(*v2)
    return math.degrees(math.acos(max(-1, min(1, abs(v1[0] * v2[0] + v1[1] * v2[1]) / n)))) if n else 0


segs = collections.defaultdict(dict)        # sheet -> key -> seg
for w in C['existing_walls']:
    p = [tuple(map(float, q)) for q in w['path']]
    k = tuple(sorted((round(p[0][0]), round(p[0][1]), round(p[-1][0]), round(p[-1][1]))))
    k = (min((round(p[0][0]), round(p[0][1])), (round(p[-1][0]), round(p[-1][1]))), max((round(p[0][0]), round(p[0][1])), (round(p[-1][0]), round(p[-1][1]))))
    s = segs[(w['sheet'], w['floor'])].setdefault(k, {"a": p[0], "b": p[-1], "faces": 0, "h": 0, "ids": [], "floor": w['floor'], "page": w['page'], "types": set()})
    s['faces'] += int(w.get('faces') or 1)
    s['h'] = max(s['h'], float(w.get('height_ft') or 0))
    s['ids'].append(w['id']); s['types'].add(w.get('type_id'))

res = {"_metodo": __doc__, "por_hoja": {}, "por_floor": {}}
doc = fitz.open(PDF)
ARCOS = {}
for (sh, fl0), d in sorted(segs.items()):
    sc = SC.get(sh) or 9.0
    tol = 0.75 * sc
    L = list(d.values())
    for s in L:
        s['two'] = s['faces'] >= 2
    ends = []                                  # (seg idx, end point, otro extremo)
    for i, s in enumerate(L):
        for e, o in ((s['a'], s['b']), (s['b'], s['a'])):
            ends.append((i, e, o))
    corners, libres = [], []
    vistos = set()
    for i, e, o in ends:
        s = L[i]
        toca = []
        for j, t in enumerate(L):
            if j == i:
                continue
            dd, tt = dseg(e, t['a'], t['b'])
            if dd <= tol:
                toca.append((j, tt))
        if not toca:
            libres.append((i, e, o))
            continue
        for j, tt in toca:
            t = L[j]
            en_extremo = min(math.dist(e, t['a']), math.dist(e, t['b'])) <= tol
            a = ang((s['a'], s['b']), (t['a'], t['b']))
            if en_extremo and 60 <= a <= 120 and len(toca) == 1:
                key = frozenset((i, j))
                if key in vistos:
                    continue
                vistos.add(key)
                if s['two'] and t['two']:
                    corners.append({"kind": "L", "at": [round(e[0], 1), round(e[1], 1)], "n": 1, "h": min(s['h'], t['h']) or s['h'],
                                    "walls": [s['ids'][0], t['ids'][0]]})
    # extremos libres: jamb de door opening = esquina del bbox de un door swing (arco vectorial de 2-4.5 ft) a <= 0.9 ft,
    # u otro extremo libre a 2.0-4.5 ft (vano)
    pg0 = doc[L[0]['page'] - 1]
    if pg0.number not in ARCOS:
        bx = []
        for dr in pg0.get_drawings():
            for it in dr['items']:
                if it[0] == 'c':
                    q = fitz.Rect(it[1], it[1]); [q.include_point(z) for z in it[2:]]
                    bx.append(q)
        # un swing de 90 grados puede venir en varios tramos: unir arcos que se tocan
        ARCOS[pg0.number] = [r for r in bx if 1.5 * 9 <= max(r.width, r.height) <= 4.6 * 18]
    swings = [r for r in ARCOS[pg0.number] if 2.0 * sc <= max(r.width, r.height) <= 4.6 * sc]
    # door tags impresos (texto 'NNN.N' / 'NNNN.N' de la hoja, door schedule A8.00): un extremo libre a <= 4.5 ft del
    # centro de un door tag es jamb de esa puerta (frame / casing by others, sin corner bead)
    if ('T', pg0.number) not in ARCOS:
        ARCOS[('T', pg0.number)] = [((w[0] + w[2]) / 2, (w[1] + w[3]) / 2) for w in pg0.get_text('words')
                                    if __import__('re').fullmatch(r'\d{3,4}\.\d{1,2}[A-Z]?', w[4])]
    tags = ARCOS[('T', pg0.number)]
    def jamb(e):
        if any(math.dist(e, t) <= 4.5 * sc for t in tags):
            return True
        for r in swings:
            for cx, cy in ((r.x0, r.y0), (r.x1, r.y0), (r.x0, r.y1), (r.x1, r.y1)):
                if math.dist(e, (cx, cy)) <= 0.9 * sc:
                    return True
        return False
    for i, e, o in libres:
        s = L[i]
        if not s['two']:
            continue
        door = jamb(e) or any(k != i and 2.0 * sc <= math.dist(e, e2) <= 4.5 * sc for k, e2, _ in libres)
        if door:
            continue
        corners.append({"kind": "END", "at": [round(e[0], 1), round(e[1], 1)], "n": 2, "h": s['h'], "walls": [s['ids'][0]]})
    lf = round(sum(c['n'] * c['h'] for c in corners), 2)
    fl = fl0
    # imagen circulada
    pg = doc[L[0]['page'] - 1]
    img = None
    if corners:
        sh_ = pg.new_shape()
        for c in corners:
            x, y = c['at']
            sh_.draw_circle(fitz.Point(x, y) * pg.derotation_matrix if False else fitz.Point(x, y), 6)
            sh_.finish(color=(1, 0, 0) if c['kind'] == 'L' else (0, 0, 1), width=1.6)
        sh_.commit()
        img = f'{OUT}/CB_{sh}_{fl}.png'
        pg.get_pixmap(dpi=110).save(img)
        doc = fitz.open(PDF)
    res['por_hoja'][f'{sh} {fl}'] = {"floor": fl, "scale_pt_per_ft": sc, "walls_geom": len(L), "L_corners": sum(1 for c in corners if c['kind'] == 'L'),
                           "free_ends": sum(1 for c in corners if c['kind'] == 'END'), "corners": corners, "lf": lf, "img": img}
    f = res['por_floor'].setdefault(fl, {"lf": 0, "n_corners": 0, "sheets": []})
    f['lf'] = round(f['lf'] + lf, 2); f['n_corners'] += sum(c['n'] for c in corners); f['sheets'].append(sh)
json.dump(res, open(f'{W}/etapas/4_canon/out/corner_bead.json', 'w'), indent=1)
for sh, v in res['por_hoja'].items():
    print(sh, v['floor'], 'geom', v['walls_geom'], 'L', v['L_corners'], 'END', v['free_ends'], 'LF', v['lf'])
print(json.dumps({k: (v['lf'], v['n_corners']) for k, v in res['por_floor'].items()}))
