"""etapas/6_markups/rcp_polys.json: polígono de cada ceiling (FS-1 / RS-1) en su RCP (A3.01-A3.04) por PROGRAMA:
flood fill desde el número del cuarto sobre la hoja rasterizada (1 px = 1 pt, texto tapado, líneas de muro dilatadas
2 px para cerrar juntas), contorno -> polígono ortogonal simplificado. Se acepta solo si el área del polígono /
(9 pt/ft)^2 cae dentro de ±15 % del SF impreso del cuarto; si no, el ceiling queda marcado con un rectángulo de la
caja del flood (reporte en rcp_polys_check.json) y se lista. Imagen de control por hoja en 4_canon/img/rcp_check_<hoja>.png."""
import json, re, os, fitz, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
W = '/root/cr/work'
c = json.load(open(f'{W}/etapas/4_canon/takeoff_canon.json'))
pdf = fitz.open(f'{W}/plans/bidset_SIN_MARKUPS.pdf')
PG = {'A3.01': 22, 'A3.02': 23, 'A3.03': 24, 'A3.04': 25}
RCP = {'L1': 'A3.01', 'L2': 'A3.02', 'L3': 'A3.03', 'L4': 'A3.04'}
cache = {}
def raster(sh):
    if sh in cache: return cache[sh]
    p = pdf[PG[sh] - 1]
    pix = p.get_pixmap(matrix=fitz.Matrix(1, 1), colorspace=fitz.csGRAY)
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width).copy()
    for w in p.get_text('words'):                       # tapa el texto
        x0, y0, x1, y1 = [int(round(v)) for v in w[:4]]
        a[max(0, y0 - 1):y1 + 1, max(0, x0 - 1):x1 + 1] = 255
    dark = a < 160
    dark = ndimage.binary_dilation(dark, iterations=2)
    cache[sh] = (p, dark)
    return cache[sh]
out, chk = [], []
for x in c.get('ceilings') or []:
    fl = x.get('floor'); sh = RCP.get(fl)
    if not sh: continue
    p, dark = raster(sh)
    m = re.search(r'\b([1-4]\d\d)\b', x['room'])
    hits = p.search_for(m.group(1)) if m else []
    best = None
    for r in hits:
        cx, cy = int((r.x0 + r.x1) / 2), int(r.y1 + 3)
        free = ~dark
        if not free[cy, cx]: continue
        lab, n = ndimage.label(free)
        reg = lab == lab[cy, cx]
        area_sf = reg.sum() / 81.0
        if area_sf > 5000: continue
        e = abs(area_sf - x['area_sf']) / x['area_sf']
        if best is None or e < best[0]: best = (e, reg, area_sf)
    x['sheet'] = sh
    if best is None:
        if hits:   # localizador: caja alrededor del número impreso del cuarto (no es geometría medida; SF = impreso)
            r = hits[0]
            out.append({"room": x['room'], "polygon": [[r.x0 - 12, r.y0 - 8], [r.x1 + 12, r.y0 - 8], [r.x1 + 12, r.y1 + 8], [r.x0 - 12, r.y1 + 8]]})
            chk.append({"room": x['room'], "sheet": sh, "status": "locator at the printed room number (SF = printed)"})
        else:   # caja de los walls del canon que nombran el cuarto (hoja de planta), geometría del canon resuelto
            key = (m.group(1) if m else ('STAIR 1' if 'Lobby stair' in x['room'] else '413' if '413' in x['room'] else None))
            ws_ = [e for e in c['existing_walls'] if key and key.lower() in str(e.get('location', '')).lower() and e.get('floor') == fl and e['sheet'].startswith('A2.0')]
            if not ws_ and 'stair' in x['room'].lower():   # escaleras de L4: walls del canon de esa escalera (A6.01 / A6.02 / A2.04)
                kk = 'lobby stair' if 'Lobby' in x['room'] else 'se stair'
                ws_ = [e for e in c['existing_walls'] if e.get('floor') == fl and (kk in str(e.get('location', '')).lower() or ('413' in str(e.get('location', '')) and kk == 'se stair'))]
            if ws_:
                hs = ws_[0]['sheet']; ps = [pt for e in ws_ if e['sheet'] == hs for pt in e['path']]
                xs_ = [q[0] for q in ps]; ys_ = [q[1] for q in ps]
                out.append({"room": x['room'], "polygon": [[min(xs_), min(ys_)], [max(xs_), min(ys_)], [max(xs_), max(ys_)], [min(xs_), max(ys_)]]})
                x['sheet'] = hs
                chk.append({"room": x['room'], "sheet": hs, "status": f"box of the canon walls naming '{key}' on {hs} (room number not printed on {sh})"})
            else:
                chk.append({"room": x['room'], "sheet": sh, "status": "no region"})
        continue
    e, reg, asf = best
    ys, xs = np.nonzero(reg)
    if e <= 0.15:
        # contorno ortogonal: escaneo por filas de 3 pt -> polígono de la envolvente fila a fila
        rows = {}
        for yy in range(ys.min(), ys.max() + 1, 3):
            xx = xs[ys == yy]
            if len(xx): rows[yy] = (xx.min(), xx.max())
        left = [(rows[k][0], k) for k in sorted(rows)]; right = [(rows[k][1], k) for k in sorted(rows, reverse=True)]
        poly = [[float(a_), float(b_)] for a_, b_ in left + right]
        st = "polygon"
    else:
        poly = [[float(xs.min()), float(ys.min())], [float(xs.max()), float(ys.min())], [float(xs.max()), float(ys.max())], [float(xs.min()), float(ys.max())]]
        st = "bbox (flood area off printed SF)"
    out.append({"room": x['room'], "polygon": poly})
    chk.append({"room": x['room'], "sheet": sh, "status": st, "flood_sf": round(asf, 1), "printed_sf": x['area_sf'], "err": round(e, 3)})
st_ = {k['room']: k['status'] for k in chk}
for x in c.get('ceilings') or []:
    if x['room'] in st_:
        x['area_cause'] = (f"polygon = {st_[x['room']]} (locates the room on the RCP); loaded SF = PRINTED room SF {x['area_sf']} (plan room tag), "
                           f"FS-1 / RS-1 over the whole unit incl. bath / closets")
        x['hatch_check_cause'] = (f"polygon = {st_[x['room']]}; it locates the room on the RCP. The loaded SF is the PRINTED room SF "
                                  f"({x['area_sf']} SF, plan room tag) - for FS-1 the whole unit incl. bath / closets (the rated membrane is continuous above the "
                                  f"GYP-1 dropped bath ceiling), so the RCP hatch does not match the polygon one-to-one")
for o in out:
    o['cause'] = next((x['area_cause'] for x in c.get('ceilings') or [] if x['room'] == o['room'] and x.get('area_cause')), None)
json.dump(out, open(f'{W}/etapas/6_markups/rcp_polys.json', 'w'), indent=1)
json.dump(chk, open(f'{W}/etapas/6_markups/rcp_polys_check.json', 'w'), indent=1)
json.dump(c, open(f'{W}/etapas/4_canon/takeoff_canon.json', 'w'), indent=1)
import collections
print(len(out), 'polys', collections.Counter(k['status'] for k in chk))
