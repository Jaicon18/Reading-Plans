#!/usr/bin/env python3
"""CR City Hotel - vanos de puerta dentro de los paths de walls (auditoría U-138, hallazgo 7).
Por wall board-only en A2.01-A2.04 (path recto H / V): cobertura de las líneas de muro dibujadas (vectores sólidos de grosor
>= 0.6 pt a <= 4.5 pt del eje, método de la auditoría) -> tramos SIN muro. Un tramo sin muro >= 2.0 ft con un door tag impreso
('NNN.N') a <= 5 ft de su centro = vano de puerta:
  - en un extremo del path -> se recorta el path (y el LF) al tramo con muro;
  - el path entero es vano (cobertura < 15 %) -> el wall sale a excluded_walls (no existe);
  - en medio -> se anota door_openings (no se descuenta: conservador, delta en la fuente).
Escribe el canon en su lugar y etapas/4_canon/out/vanos_puertas.json."""
import json, math, re
import pymupdf as fitz
W = '/root/cr/work'
CP = f'{W}/etapas/4_canon/takeoff_canon.json.base.json'   # BE-CR26: trabaja sobre la salida de build_canon (la que lee finalizar)
c = json.load(open(CP))
c.setdefault('excluded_walls', [])
D = fitz.open(f'{W}/plans/bidset_SIN_MARKUPS.pdf')
SC = 9.0
_seg, _tags = {}, {}


def segs(pg):
    if pg not in _seg:
        out = []
        for d in D[pg].get_drawings():
            if (d.get('width') or 0) < 0.6 or (d.get('dashes') and d['dashes'] not in ('[] 0', '')):
                continue
            for it in d['items']:
                if it[0] == 'l':
                    out.append((it[1].x, it[1].y, it[2].x, it[2].y))
                elif it[0] == 're':
                    r = it[1]
                    out += [(r.x0, r.y0, r.x1, r.y0), (r.x0, r.y1, r.x1, r.y1), (r.x0, r.y0, r.x0, r.y1), (r.x1, r.y0, r.x1, r.y1)]
        _seg[pg] = out
        _tags[pg] = [((w[0] + w[2]) / 2, (w[1] + w[3]) / 2) for w in D[pg].get_text('words') if re.fullmatch(r'\d{3,4}\.\d{1,2}[A-Z]?', w[4])]
    return _seg[pg], _tags[pg]


def cubierto(pg, path, band=4.5):
    (x0, y0), (x1, y1) = path[0], path[-1]
    h = abs(y1 - y0) < abs(x1 - x0)
    a0, a1 = sorted([x0, x1]) if h else sorted([y0, y1])
    cc = (y0 + y1) / 2 if h else (x0 + x1) / 2
    iv = []
    for sx0, sy0, sx1, sy1 in segs(pg)[0]:
        if h:
            if abs(sy1 - sy0) > 0.3 or abs(sy0 - cc) > band:
                continue
            lo, hi = sorted([sx0, sx1])
        else:
            if abs(sx1 - sx0) > 0.3 or abs(sx0 - cc) > band:
                continue
            lo, hi = sorted([sy0, sy1])
        lo, hi = max(lo, a0), min(hi, a1)
        if hi > lo:
            iv.append((lo, hi))
    iv.sort()
    m = []
    for lo, hi in iv:
        if m and lo <= m[-1][1] + 1.0:
            m[-1][1] = max(m[-1][1], hi)
        else:
            m.append([lo, hi])
    return h, a0, a1, cc, m


def nota_largo(src, nota):
    """BE-CF24: la nota del largo va en el segmento de largo, antes de '| height:' (si no, el chequeo la lee como altura)."""
    src = str(src or '')
    return src.replace('| height:', nota + ' | height:', 1) if '| height:' in src else src + nota


res = {"recortados": [], "eliminados": [], "en_medio": []}
grupos = {}
for w in c['existing_walls']:
    if re.match(r'A2\.0[1-4]$', w['sheet']) and len(w['path']) == 2:
        grupos.setdefault(w['id'].split(' ')[0], []).append(w)
for wid, ws in grupos.items():
    w = ws[0]
    pg = w['page'] - 1
    (x0, y0), (x1, y1) = w['path']
    if abs(x1 - x0) > 1.0 and abs(y1 - y0) > 1.0:
        continue                                   # diagonal: fuera del método
    h, a0, a1, cc, m = cubierto(pg, w['path'])
    L = a1 - a0
    if L < 9:
        continue
    gaps = []
    p = a0
    for lo, hi in m + [[a1, a1]]:
        if lo - p >= 2.0 * SC:
            gaps.append((p, lo))
        p = max(p, hi)
    tags = segs(pg)[1]
    def puerta(g):
        mid = (g[0] + g[1]) / 2
        pt = (mid, cc) if h else (cc, mid)
        return any(math.dist(pt, t) <= 5.0 * SC for t in tags)
    gaps = [g for g in gaps if puerta(g)]
    if not gaps:
        continue
    cov = sum(hi - lo for lo, hi in m) / L
    if cov < 0.15:
        for e in ws:
            c['existing_walls'].remove(e)
            c['excluded_walls'].append({"id": e['id'], "reader": "AB", "floor": e['floor'], "img": e.get('img'), "tag_ids": e.get('tag_ids') or [], "sheet": e.get('sheet'),
                "reason": f"door opening, not a wall: the path ({round(L / SC, 2)} ft on {e['sheet']}) has {round(cov * 100)} % drawn wall lines and a printed door tag at the gap (auditoria U-138 finding 7)"})
        res['eliminados'].append({"id": wid, "lf": round(L / SC, 2), "sheet": w['sheet']})
        continue
    lo_new, hi_new = a0, a1
    medio = []
    for g in gaps:
        if abs(g[0] - a0) < 1.5:
            lo_new = max(lo_new, g[1])
        elif abs(g[1] - a1) < 1.5:
            hi_new = min(hi_new, g[0])
        else:
            medio.append(round((g[1] - g[0]) / SC, 2))
    if (lo_new, hi_new) != (a0, a1):
        cut = round((L - (hi_new - lo_new)) / SC, 2)
        for e in ws:
            (ex0, ey0), (ex1, ey1) = e['path']
            if h:
                e['path'] = [[lo_new, ey0], [hi_new, ey1]]
            else:
                e['path'] = [[ex0, lo_new], [ex1, hi_new]]
            old = e['length_ft']
            e['length_ft'] = round((hi_new - lo_new) / SC, 2)
            e['source'] = nota_largo(e.get('source'), f"; door opening at the end of the path removed: {old} - {cut} = {e['length_ft']} ft (drawn wall lines vs printed door tag, auditoria U-138)")
        res['recortados'].append({"id": wid, "sheet": w['sheet'], "cut_ft": cut})
    if medio:
        for e in ws:
            e['door_openings'] = medio
            e['source'] = nota_largo(e.get('source'), f"; door opening(s) inside the run {medio} ft NOT deducted (conservative)")
        res['en_medio'].append({"id": wid, "sheet": w['sheet'], "gaps_ft": medio})
# rev8 (COORDINACIÓN 7-nov, walls punto 5): en las hojas ampliadas (1/4" = 18 pt/ft) los vanos dentro del tramo cargado tampoco
# se descuentan (U-057, conservador) y el Source lo tiene que decir, igual que en A2: solo se DOCUMENTA (no se recorta nada).
_SC0 = SC
for w in c['existing_walls']:
    if not re.match(r'A7\.(30|45|50|55)$', w['sheet']) or len(w['path']) != 2 or w.get('door_openings'):
        continue
    (x0, y0), (x1, y1) = w['path']
    if abs(x1 - x0) > 1.0 and abs(y1 - y0) > 1.0:
        continue
    SC = 18.0
    try:
        h, a0, a1, cc, m = cubierto(w['page'] - 1, w['path'])
        L = a1 - a0
        gaps, p_ = [], a0
        for lo, hi in m + [[a1, a1]]:
            if lo - p_ >= 2.0 * SC:
                gaps.append((p_, lo))
            p_ = max(p_, hi)
        tags = segs(w['page'] - 1)[1]
        gaps = [g for g in gaps if any(math.dist(((g[0] + g[1]) / 2, cc) if h else (cc, (g[0] + g[1]) / 2), t) <= 5.0 * SC for t in tags)]
    finally:
        SC = _SC0
    if gaps and L > 0:
        anch = [round((g[1] - g[0]) / 18.0, 2) for g in gaps]
        w['door_openings'] = anch
        solido = round(w['length_ft'] - sum(anch), 2)
        w['source'] = nota_largo(w.get('source'), f"; door opening(s) inside the run {anch} ft NOT deducted (conservative, U-057; solid wall {solido} ft)")
        res['en_medio'].append({"id": w['id'], "sheet": w['sheet'], "gaps_ft": anch, "solido_ft": solido})
# correcciones verificadas a ojo (auditoría U-138 hallazgos 7 y 10; imágenes en auditoria_U138/img y scratchpad del 6-nov)
_hs = list(json.load(open(f'{W}/set_texto.json'))['hojas'])
for wid, why in (("W.4-L3-44", "the path is entirely the opening of door 308.2 on A2.03 (no wall drawn; verified by eye)"),
                 ("W.4-L4-22", "the path is entirely the opening of door 418.2 on 3/A7.50 between two drawn stubs (verified by eye); its coordinates were 3/A7.50, not A2.04")):
    for e in [e for e in c['existing_walls'] if e['id'].split(' ')[0] == wid]:
        c['existing_walls'].remove(e)
        c['excluded_walls'].append({"id": e['id'], "reader": "AB", "floor": e['floor'], "img": e.get('img'), "tag_ids": e.get('tag_ids') or [], "sheet": e.get('sheet'), "reason": "door opening, not a wall: " + why})
        res['eliminados'].append({"id": e['id'], "lf": e['length_ft'], "sheet": e['sheet']})
for e in c['existing_walls']:
    if e['id'].split(' ')[0] == 'W.4-L4-21' and e['sheet'] == 'A2.04':
        # rev8 (COORDINACIÓN 7-nov, revisión de walls punto 1): el path venía con el largo de A2.04 (19.2 pt a 9 pt/ft) puesto
        # sobre A7.50 y se dividió entre 18 -> 1.06 ft (error de reescalado). En 3/A7.50 las dos líneas del wall corren
        # y 1264.4-1302.8 (x 881.6 / 888.8): 38.4 / 18 = 2.13 ft = A2.04 (1222.2-1203.0)/9 = 2.13 ft.
        old = e['length_ft']
        e['sheet'], e['page'] = 'A7.50', _hs.index('A7.50') + 1
        e['path'] = [[885.2, 1264.4], [885.2, 1302.8]]
        e['length_ft'] = round((1302.8 - 1264.4) / 18.0, 2)
        e['source'] = str(e.get('source') or '').replace('A2.04 [DERIVED]', '3/A7.50 [DERIVED]')
        e['source'] = nota_largo(e['source'], f"; on 3/A7.50 (1/4\" = 18 pt/ft) the wall lines run y 1264.4-1302.8: (1302.8-1264.4)/18 = {e['length_ft']} ft (= A2.04 (1222.20-1203.00)/9 = 2.13 ft)")
json.dump(c, open(CP, 'w'), indent=1)
json.dump(res, open(f'{W}/etapas/4_canon/out/vanos_puertas.json', 'w'), indent=1)
print('eliminados', len(res['eliminados']), round(sum(x['lf'] for x in res['eliminados']), 2), 'LF;',
      'recortados', len(res['recortados']), round(sum(x['cut_ft'] for x in res['recortados']), 2), 'LF;', 'en medio', len(res['en_medio']))
for k in ('eliminados', 'recortados', 'en_medio'):
    print(k, res[k][:12])
