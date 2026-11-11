"""R2 M2 / M3: take-off legends of the markups PDF, complete and readable in the VISIBLE orientation of each sheet (/Rotate 270).

Tool limits (etapas/TOOL_LIMITS_CALC.md): markups_bluebeam.leyendas_por_hoja draws the A2.0 legend in UNROTATED page space (it
reads sideways on a /Rotate 270 sheet), markups_demo.py draws no legend on A1.0, markups_rcp.py lists only the quantified ceiling
rows on A3.0 (no EXCLUDED entry, its long line runs out of the box) and the LEGEND page lists only wall types.
Here, on the final markups PDF:
  1. the legend content streams the tools appended on A2.0 / A3.0 (a small stream with the white box + the streams with the
     'TAKE-OFF LEGEND' text and sample lines) are removed - nothing of the plan is touched (only streams made of the legend ops);
  2. a legend box is drawn on A1.0 (DEMO), A2.0 (wall types in schedule order) and A3.0 (SOF-01 board + EXCLUDED), in the visible
     frame (point x derotation_matrix, text rotate = page rotation), in the corner of the sheet with the least ink;
  3. the LEGEND page gets a second table 'Other take-off markups': DEMO (A1.0), SOF-01 board (A3.0), EXCLUDED rooms (A3.0).
The legends are page content (not annotations): they are not markups and do not enter the Bluebeam Markups List.
Counts / LF / SF come from the canon and the annotations of the same PDF (nothing is measured here).
Use: python3 -I scripts/leyendas_hojas.py <in.pdf> <out.pdf>"""
import json, os, re, sys, tempfile
import pymupdf as fitz

K = '/root/xf/work'
c = json.load(open(f'{K}/etapas/4_canon/takeoff_canon.json'))
pin, pout = sys.argv[1], sys.argv[2]
doc = fitz.open(pin)
pag = {(p.get_label() or '').strip(): p for p in doc}
HEX = 'TAKE-OFF LEGEND'.encode().hex()


def quitar_leyenda(p):
    """Removes the legend streams a tool appended at the END of the page /Contents. Returns how many were removed."""
    xs = p.get_contents()
    i_tit = [i for i, x in enumerate(xs) if HEX in doc.xref_stream(x).decode('latin-1').lower()]
    if not i_tit:
        return 0
    ini = i_tit[0]
    if ini > 0 and re.search(rb' re\s.*1 1 1 rg B', doc.xref_stream(xs[ini - 1]), re.S):
        ini -= 1
    quitar = xs[ini:]
    for x in quitar:                                        # only legend ops: box, sample lines, helv / hebo text
        s = doc.xref_stream(x)
        if len(s) > 3000 or (b'/helv' not in s and b'/hebo' not in s and b' re' not in s and b' l' not in s):
            raise SystemExit(f'{p.get_label()}: stream {x} is not a legend stream - nothing removed')
    arr = '[' + ' '.join(f'{x} 0 R' for x in xs[:ini]) + ']'
    doc.xref_set_key(p.xref, 'Contents', arr)
    return len(quitar)


def caja(p, W, H):
    """Least-ink place of the sheet for a W x H box (visible frame): ink map of the page rendered with its annotations at 18 dpi
    (integral image) + page text blocks, scanned every 12 pt; never over the title block / notes column (right 30 %)."""
    import numpy as np
    z = 18 / 72.0
    pix = p.get_pixmap(dpi=18, annots=True)
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3].min(axis=2) < 235
    for b in p.get_text("blocks"):
        q = fitz.Rect(b[:4]) * p.rotation_matrix
        q.normalize()
        a[int(q.y0 * z):int(q.y1 * z) + 1, int(q.x0 * z):int(q.x1 * z) + 1] = True
    I = np.pad(a.astype(np.int32).cumsum(0).cumsum(1), ((1, 0), (1, 0)))
    R = p.rect
    best = None
    y = R.y0 + 40
    while y + H < R.y1 - 40:
        x = R.x0 + 40
        while x + W < R.x1 * 0.7:
            x0, y0, x1, y1 = int(x * z), int(y * z), int((x + W) * z) + 1, int((y + H) * z) + 1
            ink = I[y1, x1] - I[y0, x1] - I[y1, x0] + I[y0, x0]
            if best is None or ink < best[0]:
                best = (ink, fitz.Rect(x, y, x + W, y + H))
            x += 12
        y += 12
    return best[1]


def dibujar(p, titulo, filas, W=None):
    """filas: (kind, rgb, dashes, text) - kind 'line' or 'hatch' or 'text'. Visible frame; written with derotation.
    The box width is the longest line + margins (nothing runs out of the box)."""
    M = p.derotation_matrix
    W = max([fitz.get_text_length(titulo, 'hebo', 8.5) + 12] +
            [fitz.get_text_length(t, 'helv', 7.5) + (58 if k != 'text' else 16) for k, _, _, t in filas])
    H = 24.0 + 14.0 * len(filas)
    b = caja(p, W, H)
    p.draw_rect(b * M, color=(0, 0, 0), fill=(1, 1, 1), width=0.8)
    p.insert_text(fitz.Point(b.x0 + 6, b.y0 + 14) * M, titulo, fontsize=8.5, fontname='hebo', rotate=p.rotation)
    for i, (k, rgb, dsh, t) in enumerate(filas):
        y = b.y0 + 28 + 14 * i
        if k == 'line':
            p.draw_line(fitz.Point(b.x0 + 8, y - 3) * M, fitz.Point(b.x0 + 44, y - 3) * M, color=rgb, width=2.5,
                        dashes=f'[{dsh[0]} {dsh[1]}] 0' if dsh else None)
        elif k == 'hatch':
            muestra(p, fitz.Rect(b.x0 + 8, y - 8, b.x0 + 44, y + 2), M)
        p.insert_text(fitz.Point(b.x0 + (50 if k != 'text' else 8), y) * M, t, fontsize=7.5, fontname='helv', rotate=p.rotation)
    return b


def muestra(p, r, M=fitz.Identity):
    """Small grey hatched sample = the look of the EXCLUDED polygons (translucent grey + 45-degree hatch + dashed outline)."""
    p.draw_rect(r * M, color=None, fill=(0.45, 0.45, 0.45), fill_opacity=0.25, width=0)
    k = r.x0 - r.height
    while k < r.x1:
        a, bb = fitz.Point(k, r.y1), fitz.Point(k + r.height, r.y0)
        if a.x < r.x0:
            a = fitz.Point(r.x0, r.y1 - (r.x0 - a.x))
        if bb.x > r.x1:
            bb = fitz.Point(r.x1, r.y0 + (bb.x - r.x1))
        p.draw_line(a * M, bb * M, color=(0.45, 0.45, 0.45), width=0.45)
        k += 5
    p.draw_rect(r * M, color=(0.45, 0.45, 0.45), width=1, dashes='[3 3] 0')


def col(a):
    return tuple(round(v, 3) for v in a.colors['stroke']), (tuple(int(v) for v in a.border['dashes']) or None)


def annots(p, subj=None, tipo=None):
    return [a for a in p.annots() or [] if (subj is None or a.info.get('subject') == subj) and (tipo is None or a.type[1] == tipo)]


rep = {}
# ---- A1.0 demolition
demo = [m for m in c['misc_items'] if m['ref'].startswith('DEMO')]
p = pag['A1.0']
ad = annots(p, 'DEMO')
rgb, dsh = col(ad[0])
lf_d, sf_d = sum(float(m['lf']) for m in demo), sum(float(m['qty']) for m in demo)
rep['A1.0'] = quitar_leyenda(p)
dibujar(p, 'TAKE-OFF LEGEND - A1.0 (demolition)', [
    ('line', rgb, dsh, f"DEMO - existing wall removed (A1.0 key 7) - {len(demo)} element(s) - "
                       f"{lf_d:,.2f} LF - {sf_d:,.2f} SF"),
    ('text', None, None, f"Subject DEMO: Length = LF, Depth = H {demo[0]['height_ft']:g} ft (RFI-01), Wall Area = LF x H = Excel SF")])
# ---- A2.0 walls in schedule order
p = pag['A2.0']
rep['A2.0'] = quitar_leyenda(p)
orden = (c['constants'].get('type_order') or {}).get('value') or []
por = {}
for w in c['walls']:
    if w['band']['sheet'] == 'A2.0':
        d = por.setdefault(w['tag'], [0, 0.0]); d[0] += 1; d[1] += float(w['length_ft'])
ley = {a.info.get('subject'): a for a in annots(pag['LEGEND'])}
tipos = sorted(por, key=lambda t: (orden.index(t) if t in orden else len(orden), t))
filas = []
for t in tipos:
    a = ley.get(t) or next(iter(annots(p, t)), None)
    rgb, dsh = col(a) if a else ((0.5, 0.5, 0.5), None)
    filas.append(('line', rgb, dsh, f"{t} - {por[t][0]} wall(s) - {por[t][1]:,.2f} LF"))
dibujar(p, 'TAKE-OFF LEGEND - A2.0 (partition schedule order)', filas)
# ---- A3.0 ceilings / soffits + EXCLUDED
p = pag['A3.0']
rep['A3.0'] = quitar_leyenda(p)
rcp = [e for e in json.load(open(f'{K}/etapas/6_markups/rcp_polys.json')) if e.get('sheet') == 'A3.0']
ex = [a for a in annots(p, 'EXCLUDED', 'Polygon')]
filas = []
for e in rcp:
    a = next((a for a in annots(p, tipo='PolyLine') if e['id'] in (doc.xref_get_key(a.xref, 'NM')[1] or '')), None)
    rgb, dsh = col(a) if a else ((0.1, 0.6, 0.2), None)
    filas.append(('line', rgb, dsh, f"{e['id']} - gyp. bd. header 8'-6\" AFF: {e['lf']:.2f} LF x {e['depth_ft']:.3f} ft = "
                                    f"{e['lf'] * e['depth_ft']:,.2f} SF board"))
filas.append(('hatch', None, None, f"EXCLUDED - {len(ex)} room(s) not quantified: grey hatch = room, red text = reason + sheet"))
filas.append(('text', None, None, '/Measure at the printed scale (1/4" = 1\'-0"); SF = Excel row'))
dibujar(p, 'TAKE-OFF LEGEND - A3.0 (gypsum board ceilings / soffits)', filas)
# ---- LEGEND page: other take-off markups
p = pag['LEGEND']
y = 200.0
p.insert_text((40, y), 'Other take-off markups (not walls)', fontsize=12, fontname='hebo')
y += 18
for x, h in zip((40, 130, 450, 510, 580), ('Sample', 'Markup / Subject', 'Items', 'LF', 'SF')):
    p.insert_text((x, y), h, fontsize=10, fontname='hebo')
y += 6
p.draw_line((40, y), (1184, y), color=(0, 0, 0), width=0.5)
rgb, dsh = col(ad[0])
filas = [(('line', rgb, dsh), 'DEMO (A1.0 key 7)', len(demo), f'{lf_d:,.2f}', f'{sf_d:,.2f}')]
for e in rcp:
    a = next((a for a in annots(pag['A3.0'], tipo='PolyLine') if e['id'] in (doc.xref_get_key(a.xref, 'NM')[1] or '')), None)
    filas.append((('line',) + col(a), f"{e['id']} - {a.info.get('subject') if a else ''} (A3.0)", 1, f"{e['lf']:.2f}",
                  f"{e['lf'] * e['depth_ft']:,.2f}"))
filas.append((('hatch',), 'EXCLUDED (A3.0) - room not quantified', len(ex), '-', '-'))
for smp, name, n, L, S in filas:
    y += 17
    if smp[0] == 'line':
        p.draw_line((40, y - 4), (110, y - 4), color=smp[1], width=2.5, dashes=f'[{smp[2][0]} {smp[2][1]}] 0' if smp[2] else None)
    else:
        muestra(p, fitz.Rect(40, y - 10, 110, y + 1))
    for x, v in zip((130, 450, 510, 580), (name, str(n), L, S)):
        p.insert_text((x, y), v, fontsize=10, fontname='helv')
y += 22
p.insert_text((40, y), 'EXCLUDED rooms: red text on the room = printed reason and its sheet; grey hatched outline, no /Measure, '
                       'Subject EXCLUDED (filter it in the Markups List).', fontsize=8.5, fontname='helv')
labels = {i + 1: doc[i].get_label() for i in range(doc.page_count)}
tmp = tempfile.mktemp(suffix='.pdf', dir=os.path.dirname(os.path.abspath(pout)))
doc.save(tmp, garbage=3, deflate=True)
os.replace(tmp, pout)
sys.path.insert(0, os.environ.get('T', '/root/xf/skill/take-off-metal-frame-drywall/tools'))
import markups_bluebeam as mb
mb.editable(pout, {k: v for k, v in labels.items() if v})      # Page Labels + /VP kept
d = fitz.open(pout)
txt = {lb: d[i].get_text() for i, lb in enumerate(labels.values())}
falta = [h for h in ('A1.0', 'A2.0', 'A3.0') if f'TAKE-OFF LEGEND - {h}' not in txt[h]] + \
        [k for k in ('DEMO', 'EXCLUDED', 'SOF-01') if k not in txt['LEGEND']] + \
        ([] if 'EXCLUDED' in txt['A3.0'].split('TAKE-OFF LEGEND - A3.0')[-1] else ['A3.0 EXCLUDED entry'])
print('old legend streams removed:', rep, '| legends drawn: A1.0, A2.0, A3.0, LEGEND page | missing:', falta)
sys.exit(1 if falta else 0)
