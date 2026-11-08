#!/usr/bin/env python3
"""rev9 (COORDINACIÓN, cielos B): contorno REAL de cada cuarto de ceilings[] medido en vectores sobre su planta (A2.0x):
1) región = flood desde la etiqueta del cuarto (la que tiene '<SF impreso> SF' debajo) sobre los walls del canon que limitan la
   unidad (demising / corridor / exterior / CMU / chase; los walls interiores de bath / shower / closet NO), juntas cerradas;
2) contorno ortogonal de la región; cada borde se ajusta a la CARA del wall dibujada en el PDF (línea vectorial más cercana hacia
   el interior, solape >= 50 %): el polígono queda en caras interiores, no en ejes;
3) bath = caja de los walls del canon que nombran 'Bath <n>' ajustada a sus caras exteriores;
4) chequeo: área(contorno) - área(bath) vs SF impreso del cuarto (el SF impreso de las unidades excluye el bath).
Salida: etapas/4_canon/out/contornos_cielos.json + imagen por hoja etapas/4_canon/img/rev9/contornos_<hoja>.png."""
import json, re, sys, fitz, numpy as np, cv2
from PIL import Image, ImageDraw
W = '/root/cr/work'
c = json.load(open(f'{W}/etapas/4_canon/takeoff_canon.json'))
HS = list(json.load(open(f'{W}/set_texto.json'))['hojas'])
pdf = fitz.open(f'{W}/plans/bidset_SIN_MARKUPS.pdf')
Z = 4
INTERIOR = re.compile(r'\b(bath|shower|toilet|vanity|plumbing furring|closet|wardrobe)\b', re.I)
BORDE = re.compile(r'demising|corridor|exterior|lobby|stair|elevator|chase|shaft', re.I)


def lineas(p, R):
    H, V = [], []
    for d in p.get_drawings():
        if not d['rect'].intersects(R):
            continue
        for it in d['items']:
            if it[0] == 'l':
                a, b = it[1], it[2]
                if abs(a.y - b.y) < 0.3 and abs(a.x - b.x) > 6:
                    H.append((a.y, min(a.x, b.x), max(a.x, b.x)))
                if abs(a.x - b.x) < 0.3 and abs(a.y - b.y) > 6:
                    V.append((a.x, min(a.y, b.y), max(a.y, b.y)))
            elif it[0] == 're':
                r = it[1]
                if r.width > 6:
                    H += [(r.y0, r.x0, r.x1), (r.y1, r.x0, r.x1)]
                if r.height > 6:
                    V += [(r.x0, r.y0, r.y1), (r.x1, r.y0, r.y1)]
    return H, V


def snap(v, lo, hi, s, L, maxd=4.6):
    """cara interior del wall: la línea MÁS ADENTRO (dirección s) a <= maxd del borde de la región (que corre por el eje del
    wall del canon), con solape >= 50 % del borde; s = 0 -> la más cercana."""
    best = None
    for (q, a, b) in L:
        d = (q - v) * (s or 1)
        if s and not (-1.2 <= d <= maxd):
            continue
        if not s and abs(q - v) > maxd:
            continue
        ov = min(b, hi) - max(a, lo)
        if ov < 0.5 * (hi - lo):
            continue
        k = -d if s else abs(q - v)
        if best is None or k < best[0]:
            best = (k, q)
    return None if best is None else round(best[1], 2)


def area(P):
    return abs(sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))) / 2


def medir(sh, items, G=14, extra_excl=()):
    p = pdf[HS.index(sh)]
    im = Image.new('L', (int(p.rect.width * Z), int(p.rect.height * Z)), 0)
    d = ImageDraw.Draw(im)
    for w in c['walls'] + c['existing_walls']:
        if w.get('sheet') != sh:
            continue
        loc = str(w.get('location', ''))
        if w['id'].split('-')[0] in extra_excl:
            continue
        l0 = loc.split('|')[0]
        if w['id'].split('-')[0] in ('W.4',) or 'plumbing furring' in l0.lower():
            continue
        for P in (w.get('paths') or [w['path']]):
            d.line([(x * Z, y * Z) for x, y in P], fill=255, width=3 * Z)
    m = np.array(im)
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (G * Z, G * Z))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, k)
    free = (m == 0).astype(np.uint8)
    n, lab = cv2.connectedComponents(free, connectivity=4)
    words = p.get_text('words')
    out = []
    for it in items:
        num, sf = it['num'], it['sf']
        cand = [w_ for w_ in words if w_[4] == num]
        # etiqueta con '<sf> SF' debajo
        def tiene_sf(w_):
            return any(abs(v[1] - w_[3]) < 30 and abs((v[0] + v[2]) / 2 - (w_[0] + w_[2]) / 2) < 40 and v[4].replace(',', '') == str(int(round(sf))) for v in words)
        cand = [w_ for w_ in cand if tiene_sf(w_)] or cand
        if it.get('punto'):
            cand = [(it['punto'][0] - 1, it['punto'][1] - 1, it['punto'][0] + 1, it['punto'][1] - 5, num)]
        res = None
        for w_ in cand:
            cx, cy = int((w_[0] + w_[2]) / 2 * Z), int((w_[3] + 6) * Z)
            if not free[cy, cx]:
                it['_en_linea'] = True; continue
            reg = (lab == lab[cy, cx]).astype(np.uint8)
            a_sf = reg.sum() / (Z * Z) / 81
            if a_sf > 4000:
                it['_fuga'] = round(a_sf); continue
            res = reg
            break
        if res is None:
            out.append({**it, "estado": "sin región"}); continue
        cs, _ = cv2.findContours(res, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        C = max(cs, key=cv2.contourArea)
        ap = cv2.approxPolyDP(C, 1.5 * Z, True)[:, 0, :] / Z
        # ortogonalizar: cada vértice toma x del borde vertical y y del horizontal
        P = [list(map(float, q)) for q in ap]
        Q = []
        for i in range(len(P)):
            a, b = P[i], P[(i + 1) % len(P)]
            Q.append(('H' if abs(b[1] - a[1]) < abs(b[0] - a[0]) else 'V', a, b))
        bx0 = min(q[0] for q in P); by0 = min(q[1] for q in P); bx1 = max(q[0] for q in P); by1 = max(q[1] for q in P)
        R = fitz.Rect(bx0 - 15, by0 - 15, bx1 + 15, by1 + 15)
        HL, VL = lineas(p, R)
        def dentro(x, y):
            xi, yi = int(x * Z), int(y * Z)
            return 0 <= yi < res.shape[0] and 0 <= xi < res.shape[1] and res[yi, xi] > 0
        edges = []
        for t, a, b in Q:
            if t == 'H':
                y = (a[1] + b[1]) / 2; xm = (a[0] + b[0]) / 2
                s = 1 if dentro(xm, y + 2.5) else -1 if dentro(xm, y - 2.5) else 0
                v = snap(y, min(a[0], b[0]), max(a[0], b[0]), s, HL)
                edges.append(('H', v if v is not None else round(y, 2), v is not None))
            else:
                x = (a[0] + b[0]) / 2; ym = (a[1] + b[1]) / 2
                s = 1 if dentro(x + 2.5, ym) else -1 if dentro(x - 2.5, ym) else 0
                v = snap(x, min(a[1], b[1]), max(a[1], b[1]), s, VL)
                edges.append(('V', v if v is not None else round(x, 2), v is not None))
        # fusionar bordes consecutivos del mismo tipo
        E2 = []
        for e in edges:
            if E2 and E2[-1][0] == e[0]:
                continue
            E2.append(e)
        if len(E2) > 1 and E2[0][0] == E2[-1][0]:
            E2.pop()
        poly = []
        for i in range(len(E2)):
            e1, e2 = E2[i], E2[(i + 1) % len(E2)]
            poly.append([e2[1], e1[1]] if e1[0] == 'H' else [e1[1], e2[1]])
        A = area(poly) / 81
        # bath de la unidad: caja de los walls del canon 'Bath <n>' / 'Shower <n>' (ejes) -> caras exteriores (±1.8 pt, ajuste a línea)
        bw = [w for w in c['walls'] + c['existing_walls'] if w.get('sheet') == sh and
              re.match(rf"\s*(L\d\s+)?(\[[^\]]*\]\s*)?(bath|shower)\s+{num}\b", str(w.get('location', '')).split('|')[0], re.I)]
        bath = None
        if bw:
            ps = [q for w in bw for P_ in (w.get('paths') or [w['path']]) for q in P_]
            x0, x1 = min(q[0] for q in ps), max(q[0] for q in ps); y0, y1 = min(q[1] for q in ps), max(q[1] for q in ps)
            px0, py0, px1, py1 = [min(q[0] for q in poly), min(q[1] for q in poly), max(q[0] for q in poly), max(q[1] for q in poly)]
            def cl(v, lo, hi): return min(max(v, lo), hi)
            bx = [cl(snap(x0 - 1.8, y0, y1, 0, VL, 1.5) or x0 - 1.8, px0, px1), cl(snap(x1 + 1.8, y0, y1, 0, VL, 1.5) or x1 + 1.8, px0, px1)]
            by = [cl(snap(y0 - 1.8, x0, x1, 0, HL, 1.5) or y0 - 1.8, py0, py1), cl(snap(y1 + 1.8, x0, x1, 0, HL, 1.5) or y1 + 1.8, py0, py1)]
            bath = [[bx[0], by[0]], [bx[1], by[0]], [bx[1], by[1]], [bx[0], by[1]]]
        Ab = area(bath) / 81 if bath else 0.0
        out.append({**it, "estado": "medido", "polygon": poly, "area_sf": round(A, 2), "bath": bath, "bath_sf": round(Ab, 2),
                    "sin_bath_sf": round(A - Ab, 2), "err_vs_impreso": round((A - Ab - sf) / sf, 4) if sf else None, "bordes_sin_cara": sum(1 for e in E2 if not e[2]),
                    "n_bordes": len(E2)})
    return out


if __name__ == '__main__':
    fl = sys.argv[1]; sh = {'L1': 'A2.01', 'L2': 'A2.02', 'L3': 'A2.03', 'L4': 'A2.04'}[fl]
    its = []
    for x in c['ceilings']:
        if x.get('floor') != fl: continue
        m = re.search(r'\b([1-4]\d\d)\b', x['room'])
        mm = re.search(r'printed (?:room SF on \S+ \(|)"?(?:\d+ / )?(\d+) SF', x['source']) or re.search(r'(\d+) SF printed', x['source'])
        if m: its.append({"num": m.group(1), "sf": float(mm.group(1)) if mm else float(x['area_sf']), "room": x['room']})
    for r in medir(sh, its):
        print(f"{r['num']} imp {r['sf']:7} med {r.get('area_sf')!s:8} bath {r.get('bath_sf')!s:7} sinbath {r.get('sin_bath_sf')!s:8} err {r.get('err_vs_impreso')!s:8} sincara {r.get('bordes_sin_cara')}/{r.get('n_bordes')} {r.get('estado')} {r['room'][:30]}")


def imagen(sh, res, fn, clip=None):
    p = pdf[HS.index(sh)]
    clip = clip or fitz.Rect(min(q[0] for r in res if r.get('polygon') for q in r['polygon']) - 30, min(q[1] for r in res if r.get('polygon') for q in r['polygon']) - 30,
                             max(q[0] for r in res if r.get('polygon') for q in r['polygon']) + 30, max(q[1] for r in res if r.get('polygon') for q in r['polygon']) + 30)
    S = 2
    pix = p.get_pixmap(matrix=fitz.Matrix(S, S), clip=clip)
    im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    d = ImageDraw.Draw(im)
    for r in res:
        if not r.get('polygon'):
            continue
        P = [((x - clip.x0) * S, (y - clip.y0) * S) for x, y in r['polygon']]
        d.line(P + [P[0]], fill=(220, 0, 0), width=3)
        if r.get('bath'):
            B = [((x - clip.x0) * S, (y - clip.y0) * S) for x, y in r['bath']]
            d.line(B + [B[0]], fill=(0, 90, 255), width=2)
        cx = sum(q[0] for q in P) / len(P); cy = sum(q[1] for q in P) / len(P)
        d.text((cx - 30, cy + 40), f"{r['num']} {r['area_sf']} / {r.get('sin_bath_sf')} vs {r['sf']}", fill=(220, 0, 0))
    im.save(fn)
