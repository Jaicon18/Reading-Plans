import sys as _s; _s.path.insert(0, '/tmp/claude-0/-home-user-Reading-Plans/b9c208e2-64c4-5dc6-9d1d-2546bd4c85dc/scratchpad/skill/take-off-metal-frame-drywall/tools')
import etiquetas
import json, math, pymupdf as fitz
from PIL import Image, ImageDraw, ImageFont
K = '/home/user/Reading-Plans/cache_proyectos/barnes_noble/takeoff_work'
E = K + '/etapas'
PDF = '/tmp/claude-0/-home-user-Reading-Plans/b9c208e2-64c4-5dc6-9d1d-2546bd4c85dc/scratchpad/bidset/bidset_SIN_MARKUPS.pdf'
c = json.load(open(E + '/4_canon/takeoff_canon.json'))
fo = json.load(open(E + '/4_canon/out/familias_out.json'))
pt = fo['partition_types']
ORDER = "1A 1 1B 1C 2 5 3 4 H1 H2A H2B H3A H3B E2 E1 F I A B D C".split()
PAL = [(230,25,25),(0,115,215),(0,150,60),(255,128,0),(140,50,190),(0,175,190),(215,25,150),(150,100,25),(90,90,90),
       (200,170,0),(0,90,60),(120,0,0),(0,0,140),(255,90,160),(60,160,255),(170,110,255),(100,200,80),(255,60,0),(0,130,130),(130,0,130),(200,80,40)]
COL = {t: PAL[i % len(PAL)] for i, t in enumerate(ORDER)}
byid = {w['id']: w for w in c['walls']}
def pts(w):
    b = w['band']
    if b['ori'] == 'H':
        e = (b['c0'] + b['c1']) / 2; return [(b['lo'], e), (b['hi'], e)]
    if b['ori'] == 'V':
        e = (b['c0'] + b['c1']) / 2; return [(e, b['lo']), (e, b['hi'])]
    if b['ori'] == 'D':
        return [tuple(b['p0']), tuple(b['p1'])]
    return [(b['c0'], b['lo']), (b['c1'], b['lo']), (b['c1'], b['hi']), (b['c0'], b['hi']), (b['c0'], b['lo'])]
EL = {'column_wrap': 'COLUMN WRAP', 'soffit_side': 'SOFFIT SIDE'}   # rev13: own type in the legend (= markup Subject)
COL.update({'COLUMN WRAP': (115, 64, 13), 'SOFFIT SIDE': (0, 77, 166)})
rows = [(t, f) for t, v in pt['types'].items() for f in v['filas']] + [(EL.get(str(byid.get(o['id'], {}).get('element')), 'OTHER FRAMING'), dict(o, wall=o['id'], ids=[o['id']])) for o in pt['other_framing']]
LABEL = 'rev13 2026-10-28'
doc = fitz.open(PDF)
try:
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
    fbig = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 40)
except OSError:
    font = fbig = ImageFont.load_default()
for sheet, pg, dpi, clip in (('A-101', 6, 110, fitz.Rect(150, 380, 2150, 1560)), ('A-221', 15, 100, fitz.Rect(150, 40, 2200, 920))):
    p = doc[pg - 1]; pix = p.get_pixmap(dpi=dpi, clip=clip)
    im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    im = Image.blend(im, Image.new('RGB', im.size, 'white'), 0.35)
    dr = ImageDraw.Draw(im); z = dpi / 72
    def P(q): return ((q[0] - clip.x0) * z, (q[1] - clip.y0) * z)
    tot = {}
    labs, segs = [], []
    for t, f in rows:
        ws = [byid[i] for i in f['ids'] if i in byid and (byid[i]['band'].get('sheet') or byid[i]['sheet']) == sheet]
        if not ws: continue
        col = COL.get(t.upper(), (170, 110, 255))
        tot[t] = tot.get(t, 0) + f['lf']
        best = None
        own = []
        for w in ws:
            q = [P(x) for x in pts(w)]
            dr.line(q, fill=col, width=7 if sheet == 'A-101' else 9)
            own += [(q[k], q[k + 1]) for k in range(len(q) - 1)]
            L = math.dist(q[0], q[-1]) if len(q) == 2 else 0
            if best is None or L > best[0]: best = (L, q)
        q = best[1]; mx, my = (q[0][0] + q[-1][0]) / 2, (q[0][1] + q[-1][1]) / 2
        segs += own
        labs.append({'text': f['wall'], 'anchor': (mx, my), 'color': col, 'own': own})   # Wall # = Excel
    nleg = len([t for t in ORDER + ['COLUMN WRAP', 'SOFFIT SIDE', 'OTHER FRAMING'] if t in tot])
    for (x0, y0, x1, y1) in ((0, 0, im.size[0] * 0.75, 62), (0, 62, 560, 70 + 30 * nleg)):   # título y leyenda reservados
        segs += [((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0)),
                 ((x0, y0), (x1, y1)), ((x0, y1), (x1, y0)), ((x0, (y0 + y1) / 2), (x1, (y0 + y1) / 2))]
    etiquetas.colocar(dr, labs, font, im.size, obstaculos=segs)   # v80f R80e.21: sin solapes
    # leyenda en orden del schedule
    ly = 70; lx = 20
    dr.rectangle([0, 0, im.size[0] * 0.75, 62], fill='white'); dr.rectangle([0, 62, 560, 70 + 30 * nleg], fill='white')   # fondo legible
    dr.text((lx, 15), f'Barnes & Noble - Colorado Springs, CO | {sheet} | partitions by type | {LABEL}', fill='black', font=fbig)
    for t in ORDER + ['COLUMN WRAP', 'SOFFIT SIDE', 'OTHER FRAMING']:
        if t not in tot: continue
        col = COL.get(t, (170, 110, 255))
        dr.rectangle([lx, ly, lx + 60, ly + 18], fill=col)
        dr.text((lx + 70, ly - 4), (f'TYPE {t}' if t in ORDER else f'OTHER FRAMING - {t}' if t != 'OTHER FRAMING' else t) + f'   {round(tot[t], 2)} LF', fill='black', font=font)
        ly += 30
    out = E + f'/7_imagenes/{sheet}_partitions_by_type.png'
    im.save(out); print(out, im.size, {k: round(v, 2) for k, v in tot.items()})
