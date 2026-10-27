"""Lectura A: normaliza el caché (PARTITIONS_STEP1_rev1 + walls_coords) al esquema del canon y completa
alturas, caras, aberturas. Salida: fragmentos en 2_lectura/A/."""
import json, os, math, re
BN = '/home/user/Reading-Plans/cache_proyectos/barnes_noble'
FINAL = os.environ.get('MODO') == 'final'
REV3 = os.environ.get('REV3') == '1'
REV4 = os.environ.get('REV4') == '1'
OUT = BN + '/takeoff_work/etapas/2_lectura/A'
OUT_W = BN + '/takeoff_work/etapas/4_canon/fragmentos' if FINAL else OUT
wc = {w['wall_id']: w for w in json.load(open(BN + '/walls_coords.json'))['walls']}
inv = json.load(open(BN + '/takeoff_work/etapas/1_inventario/inventario.json'))
# tag_ids (inventario PTnnnn) -> wall de la caché (asignación por cercanía, verificada con imagen)
TAGS = {'EXT-01': ['PT0001'], 'EXT-03': ['PT0002', 'PT0003'], 'EXT-02': ['PT0004', 'PT0005'], 'EXT-07': ['PT0006'],
        'EXT-18': ['PT0008'], 'EXT-17': ['PT0009'], 'EXT-04': ['PT0010'], 'EXT-12': ['PT0011'], 'EXT-05': ['PT0012'],
        'EXT-11': ['PT0013'], 'EXT-09': ['PT0014'], 'EXT-10': ['PT0015'], 'EXT-06': ['PT0016'],
        'EXT-16': ['PT0017'], 'EXT-15': ['PT0018'], 'EXT-14': ['PT0019'], 'EXT-13': ['PT0020'],
        'W2-01': ['PT0021'], 'W2-03': ['PT0022', 'PT0023'], 'W2-04': ['PT0024', 'PT0025', 'PT0026'],
        'W2-09': ['PT0027'], 'W2-05': ['PT0028'], 'W2-06': ['PT0029', 'PT0030'], 'W2-07': ['PT0031'],
        'W5-01': ['PT0032'], 'W3-01': ['PT0033'], 'W3-04': ['PT0034'], 'W3-02': ['PT0035'], 'W3-03': ['PT0036'],
        'W4-01': ['PT0037'],
        'C-H1-N': ['PT0038'], 'C-H1-W': ['PT0039'], 'C-H2a': ['PT0040'], 'C-H2b': ['PT0041'], 'C-H3a': ['PT0042'],
        'C-H3b': ['PT0043'], 'C-E2': ['PT0044'], 'C-E1-P': ['PT0045'], 'C-E1-S': ['PT0046'], 'C-F': ['PT0047'],
        'C-I': ['PT0051'], 'C-A-1': ['PT0052'], 'C-A-2': ['PT0053'], 'C-A-3': ['PT0054'], 'C-B': ['PT0055'],
        'C-D': ['PT0056'], 'C-C': ['PT0057']}
TYPE = {k: w['type'] for k, w in wc.items()}
DET = {'1A': '1A/A-410', '1': '1/A-410', '1B': '1B/A-410', '1C': '1C/A-410', '2': '2/A-410', '5': '5/A-410',
       '3': '3/A-410', '4': '4/A-410', 'H1': 'G/A-221', 'H2a': 'G/A-221', 'H2b': 'G/A-221', 'H3a': 'H/A-221',
       'H3b': 'H/A-221', 'E1': 'E/A-221', 'E2': 'E/A-221', 'F': 'F/A-221', 'I': 'I/A-221', 'A': 'A/A-221',
       'B': 'B/A-221', 'C': 'C/A-221', 'D': 'D/A-221'}
STUD = {'1A': '3-5/8"', '1': '3-5/8"', '1C': '3-5/8"', '1B': '8"', '2': '3-5/8"', '3': '3-5/8"', '4': '3-5/8"',
        '5': '6"', 'H1': '6"', 'H2a': '3-5/8"', 'H2b': '3-5/8"', 'H3a': '6"', 'H3b': '6"', 'E1': '6"', 'E2': '6"',
        'F': '3-5/8"', 'I': '6"', 'A': '3-5/8"', 'B': '3-5/8"', 'C': '3-5/8"', 'D': '3-5/8"'}
D25 = (25.0, 'B.O. DECK ABOVE EL. 25\'-0" V.I.F. - 1/A-400A, 1/A-400B')
D257 = (25.583, 'B.O. DECK ABOVE EL. 25\'-7" V.I.F. - 2/A-400A (east facade)')
D24 = (24.0, 'B.O. DECK ABOVE EL. 24\'-0" V.I.F. - 2/A-400B (west facade)')
HEIGHT = {'EXT-01': D25, 'EXT-02': D25, 'EXT-03': D24, 'EXT-04': D24, 'EXT-05': D24, 'EXT-06': D25, 'EXT-07': D25,
          'EXT-09': D25, 'EXT-10': D25, 'EXT-11': D257, 'EXT-12': D257, 'EXT-17': D257, 'EXT-18': D257,
          'EXT-13': D257, 'EXT-14': D257, 'EXT-15': D257, 'EXT-16': D257}
for k in wc:
    t = TYPE[k]
    if t in ('2', '5', 'E1', 'E2', 'I'):
        HEIGHT[k] = D25
    elif t == '3':
        HEIGHT[k] = (8.0, '8\'-0" A.F.F. T.O. WALL - 3/A-410')
    elif t == '4':
        HEIGHT[k] = (7.5, '7\'-6" A.F.F. T.O. WALL - 4/A-410')
    elif t in ('A', 'B', 'C'):
        HEIGHT[k] = (2.708, '2\'-8 1/2" B.O. SLAB TO T.O. STUD - %s' % DET[t])
    elif t == 'D':
        HEIGHT[k] = (1.0, '1\'-0" B.O. SLAB TO T.O. STUD - D/A-221')
    elif t in ('H1', 'H2a', 'H2b', 'H3a', 'H3b', 'F'):
        HEIGHT[k] = (25.0, 'NOT PRINTED (%s break line at top; A-225 finish plan has no T.O. stud): loaded to deck '
                     '25\'-0" (1/A-400B) per rule 53.3 / 60.11 - RFI-06' % DET[t])
HSTAT = {k: ('PENDING' if TYPE[k] in ('H1', 'H2a', 'H2b', 'H3a', 'H3b', 'F') else 'CONFIRMED') for k in wc}
json.dump({'TAGS': TAGS, 'HEIGHT': HEIGHT, 'HSTAT': HSTAT, 'STUD': STUD, 'DET': DET}, open('/tmp/claude-0/-home-user-Reading-Plans/b9c208e2-64c4-5dc6-9d1d-2546bd4c85dc/scratchpad/lecturaA/_tablas.json', 'w'), indent=1)
print('ok', len(wc))

# ---------------------------------------------------------------- walls (segmentos con band)
import openpyxl
xl = openpyxl.load_workbook(BN + '/PARTITIONS_STEP1_rev1.xlsx')['Walls']
cache = {}
for r in xl.iter_rows(min_row=4, values_only=True):
    if r[0] and r[1] and not str(r[0]).startswith(('SUBTOTAL', 'GRAND')):
        cache[r[0]] = dict(zip(['id', 'type', 'sheet', 'tags', 'location', 'detail', 'framing', 'lf', 'height',
                                'hsrc', 'status', 'notes'], r))
caras = json.load(open('/tmp/claude-0/-home-user-Reading-Plans/b9c208e2-64c4-5dc6-9d1d-2546bd4c85dc/scratchpad/lecturaA/caras.json'))
HALF = {'A-101': {'2': 1.92, '5': 2.64, '3': 1.92, '4': 1.92, '1': 2.28, '1A': 2.28, '1B': 4.74, '1C': 3.0},
        'A-221': {'H1': 10.86, 'H2a': 7.32, 'H2b': 7.32, 'H3a': 10.86, 'H3b': 10.86, 'E1': 10.14, 'E2': 10.14,
                  'F': 6.36, 'I': 10.08, 'A': 9.0, 'B': 11.0, 'C': 9.0, 'D': 9.0}}
SCALE = {'A-101': 9.0, 'A-221': 36.0}

def band_de(wid, seg, t, sheet):
    (x0, y0), (x1, y1) = seg[0], seg[-1]
    h = HALF[sheet][t]
    if abs(y0 - y1) < 0.5 and len(seg) == 2:
        return {'ori': 'H', 'c0': round(y0 - h, 2), 'c1': round(y0 + h, 2), 'lo': round(min(x0, x1), 2),
                'hi': round(max(x0, x1), 2), 'sheet': sheet}
    if abs(x0 - x1) < 0.5 and len(seg) == 2:
        return {'ori': 'V', 'c0': round(x0 - h, 2), 'c1': round(x0 + h, 2), 'lo': round(min(y0, y1), 2),
                'hi': round(max(y0, y1), 2), 'sheet': sheet}
    return {'ori': 'D', 'p0': [round(x0, 2), round(y0, 2)], 'p1': [round(x1, 2), round(y1, 2)], 'sheet': sheet}

walls = {'A-101': [], 'A-221': []}
for wid, w in wc.items():
    t, sheet = w['type'], w['sheet']
    c = cache[wid]
    segs = w['points_pt']
    if w['lf'] == 0:
        continue                       # EXT-08: contado una vez como E1/E2 (RFI-05) -> tag descartado con owner
    page = 6 if sheet == 'A-101' else 15
    base = {'tag': t, 'element': 'wall', 'sheet': sheet, 'page': page, 'location': c['location'], 'source': DET[t],
            'detail': DET[t], 'detail_source': DET[t], 'stud_size': STUD[t], 'stud_source': DET[t], 'oc_in': 16,
            'oc_source': DET[t], 'height_ft': HEIGHT[wid][0], 'height_source': HEIGHT[wid][1],
            'height_status': HSTAT[wid], 'length_source': c['detail'] if False else sheet,
            'status': c['status'].strip('[]'), 'img': 'img_cache/' + ('B&N_A-101_walls_by_type.png' if page == 6 else 'B&N_A-221_cafe_walls_by_type.png')}
    if len(segs) == 1 and len(segs[0]) > 2 and segs[0][0] == segs[0][-1]:      # box cerrado -> 4 tramos rectos
        segs = [[segs[0][i], segs[0][i + 1]] for i in range(len(segs[0]) - 1)]
    if len(segs) == 1 and len(segs[0]) > 2:                                   # arco -> 6 cuerdas D
        p = segs[0]; n = 6; k = [round(i * (len(p) - 1) / n) for i in range(n + 1)]
        for i in range(n):
            q0, q1 = p[k[i]], p[k[i + 1]]
            L = math.dist(q0, q1) / SCALE[sheet]
            walls[sheet].append(dict(base, id=f"{wid}.{i + 1}", tag_ids=TAGS.get(wid, []) if i == 0 else [],
                                     length_ft=round(L, 2),
                                     length_op=f"arc R32'-9\" (A-101) by Bezier vector, chord {i + 1} of {n} = {round(L, 2)} ft (cache arc {w['lf']} ft)",
                                     band={'ori': 'D', 'p0': [round(q0[0], 2), round(q0[1], 2)],
                                           'p1': [round(q1[0], 2), round(q1[1], 2)], 'sheet': sheet}))
        continue
    tot = 0.0
    for i, s in enumerate(segs):
        L = math.dist(s[0], s[-1]) / SCALE[sheet]
        tot += L
    for i, s in enumerate(segs):
        L = math.dist(s[0], s[-1]) / SCALE[sheet]
        sid = wid if len(segs) == 1 else f"{wid}.{i + 1}"
        tid = TAGS.get(wid, []) if (len(segs) == 1 or i == 0) else []
        lf = w['lf'] if len(segs) == 1 else round(L, 2)
        walls[sheet].append(dict(base, id=sid, tag_ids=tid, length_ft=lf,
                                 length_op=f"vector centerline {round(L, 2)} ft" + ('' if len(segs) == 1 else f" (segment {i + 1} of {wid})"),
                                 band=band_de(sid, s, t, sheet)))
for sh, L in walls.items():
    print(sh, len(L), round(sum(w['length_ft'] for w in L), 2))
json.dump(walls, open('/tmp/claude-0/-home-user-Reading-Plans/b9c208e2-64c4-5dc6-9d1d-2546bd4c85dc/scratchpad/lecturaA/_walls_tmp.json', 'w'), indent=1)


# ---------------------------------------------------------------- ETAPA 3: resolución (solo MODO=final)
RESOL = []
if FINAL:
    CB = {w['id']: w for w in json.load(open(BN + '/takeoff_work/etapas/2_lectura/canon_B.json'))['walls']}
    def from_b(w, bid):
        b = CB[bid]
        w['band'] = dict(b['band'], sheet=w['sheet']); w['length_ft'] = b['length_ft']
        w['length_op'] = f"Stage 3 resolution: geometry of reading B {bid} ({b.get('length_op', 'vector')})"
        w['length_status'] = 'DERIVED'
    for w in walls['A-101']:
        if w['id'] == 'W2-05' and not REV3:   # rev3 (RI 1): W2-05 = reading A, printed 12'-11" on A-101
            from_b(w, 'B-A-101-18')
            w['location'] = "Corridor 110 east wall / Women's 109 (starts at the restroom front line)"
    m = {'W2-06.1': 'B-A-101-19a', 'W2-06.2': 'B-A-101-19b', 'W2-06.3': 'B-A-101-19c', 'W2-06.4': 'B-A-101-19d',
         'W2-06.5': 'B-A-101-19e'}
    for w in walls['A-101']:
        if w['id'] in m:
            from_b(w, m[w['id']])
    RESOL.append({'item': 'Type 2 corridor east wall W2-05 / restroom front W2-06 (review items 10, 11)',
                  'decision': 'Reading B: W2-05 starts at the restroom front line (y=1337), 7.92 LF; W2-06 segments measured face to face with one owner per corner (R70.2 / R75.7), 25.86 LF total (= cache 25.86)',
                  'source': 'A-101', 'img': '3_revision/res/res_W205.png', 'delta_lf': round(7.92 - 12.92 + 25.86 - 26.68, 2)})
    t4 = [w for w in walls['A-101'] if w['tag'] == '4']
    base4 = dict(t4[0]); walls['A-101'] = [w for w in walls['A-101'] if w['tag'] != '4']
    for bid, b in CB.items():
        if b.get('tag') == '4':
            nw = dict(base4)
            for k in ('openings', 'faces', 'type_change_rfi'):
                nw.pop(k, None)
            nw.update({'id': 'W4-' + bid.split('-')[-1], 'tag_ids': b.get('tag_ids') or [], 'location': b.get('location', base4['location']),
                       'length_ft': b['length_ft'], 'band': dict(b['band'], sheet='A-101'), 'length_status': b.get('length_status', 'DERIVED'),
                       'length_op': f"Stage 3 resolution: reading B {bid} ({b.get('length_op', '')})", 'img': 'img_cache/B&N_A-101_walls_by_type.png'})
            walls['A-101'].append(nw)
    RESOL.append({'item': 'Type 4 center feature caps and curved walls (review items 12-22, 28-30, 42-48)',
                  'decision': 'Reading B: each cap is an open U (9\'-0" bar + two returns + two legs into the curved walls), not a closed box; curved walls = printed 25\'-1" (6 chords). RFI-18: face-average arc 25.68 LF each (+1.20 LF)',
                  'source': '4/A-410', 'img': '3_revision/res/res_T4n.png', 'delta_lf': round(80.83 - 86.2, 2)})
    for w in walls['A-221']:
        if w['id'] == 'C-E1-P.1':
            w.update({'tag': 'I', 'tag_ids': ['PT0050'], 'detail': 'I/A-221', 'detail_source': 'I/A-221', 'source': 'I/A-221',
                      'stud_size': '6"', 'stud_source': 'I/A-221', 'location': '1\'-0" return at the top of the Workroom door pier (I tag)'})
        if w['id'] == 'C-E1-P.2':
            w['tag_ids'] = ['PT0045']

    # R75.7: return corto (<= 2 ft) medido desde la cara EXTERIOR del tramo al que vuelve
    def ext_return(rid, runid, sheet='A-101', esc=9.0):
        ws = {w['id']: w for w in walls[sheet]}
        r, run = ws[rid], ws[runid]
        br, bu = r['band'], run['band']
        if br['ori'] == 'V' and bu['ori'] == 'H':
            near, far = (bu['c1'], bu['c0']) if abs(br['lo'] - bu['c1']) < abs(br['hi'] - bu['c0']) else (bu['c0'], bu['c1'])
            if abs(br['lo'] - near) <= abs(br['hi'] - near): br['lo'] = round(min(far, br['lo']), 2)
            else: br['hi'] = round(max(far, br['hi']), 2)
            L = (br['hi'] - br['lo']) / esc
        else:
            near_lo = abs(br['lo'] - bu['c0']) < abs(br['hi'] - bu['c0']) or abs(br['lo'] - bu['c1']) < abs(br['hi'] - bu['c1'])
            if near_lo: br['lo'] = round(min(bu['c0'], bu['c1'], br['lo']), 2)
            else: br['hi'] = round(max(bu['c0'], bu['c1'], br['hi']), 2)
            L = (br['hi'] - br['lo']) / esc
        r['length_ft'] = round(L, 2)
        r['length_op'] += f"; R75.7 return measured from the outer face of {runid} = {round(L, 2)} ft"
    for rid, runid in (('W2-06.2', 'W2-06.1'), ('W2-06.2', 'W2-06.3'), ('W2-06.4', 'W2-06.3'), ('W2-06.4', 'W2-06.5'), ('W4-28b', 'W4-28a'), ('W4-28c', 'W4-28a'),
                       ('W4-31b', 'W4-31a'), ('W4-31c', 'W4-31a')):
        ext_return(rid, runid)

    # R70.2: esquinas exteriores sin dueño -> el primer wall llega a la cara exterior del segundo
    def own_corner(a_id, b_id, sheet='A-101', esc=9.0):
        ws = {w['id']: w for w in walls[sheet]}
        a, b = ws[a_id], ws[b_id]
        ba, bb = a['band'], b['band']
        lo_c, hi_c = min(bb['c0'], bb['c1']), max(bb['c0'], bb['c1'])
        old = a['length_ft']
        if abs(ba['lo'] - (lo_c + hi_c) / 2) < abs(ba['hi'] - (lo_c + hi_c) / 2):
            ba['lo'] = round(lo_c, 2)
        else:
            ba['hi'] = round(hi_c, 2)
        a['length_ft'] = round((ba['hi'] - ba['lo']) / esc, 2)
        a['length_op'] = a.get('length_op', '') + f"; R70.2 corner with {b_id}: runs to its outer face ({old} -> {a['length_ft']})"
        return round(a['length_ft'] - old, 2)
    dd = 0.0
    for a_id, b_id in (('EXT-01', 'EXT-03'), ('EXT-02', 'EXT-18'), ('EXT-10', 'EXT-11'), ('EXT-13', 'EXT-14'), ('EXT-16', 'EXT-15')):
        dd += own_corner(a_id, b_id)
    RESOL.append({'item': 'Exterior corners without owner (esquinas.py R70.2)', 'decision': 'EXT-01, EXT-02, EXT-10, EXT-13, EXT-16 run to the outer face of the wall they meet (one owner per corner)',
                  'source': 'A-101', 'img': '1_inventario/recortes/OVERVIEW_A-101_p6.png', 'delta_lf': round(dd, 2)})
    RESOL.append({'item': 'Workroom door pier 1\'-0" return (review items 23, 40, 50)', 'decision': 'Reading B: the I tag (PT0050) leader lands on the 1\'-0" return -> type I 1.00 LF; the E1 tag (PT0045) marks the 2\'-8" HOLD pier -> E1 2.11 LF',
                  'source': '1/A-221', 'img': '3_revision/res/res_E1I.png', 'delta_lf': 0.0})

# ---------------------------------------------------------------- caras (board por face)
RCP = 'A-121'
CEIL = {  # room -> (board height ft, source, MR)
    'Sales Area 101': (None, 'OPEN TO DECK (A-121) - board to deck, 2/A-410 "EXTEND GYPSUM BOARD TO DECK IN LOCATIONS WITH NO CEILING"', False),
    'Storage 112': (None, 'OPEN TO DECK (A-121) - board to deck, 2/A-410', False),
    'Stock Room 111': (None, 'OPEN TO DECK (A-121) - board to deck, 2/A-410', False),
    'Janitor Closet 107': (None, 'OPEN TO DECK (A-121) - board to deck, 2/A-410; greenboard per A-410 partition note 7', True),
    'Corridor 110': (9.5, 'ACT-3 9\'-0" (A-121) + 6" above suspended ceiling (A-410 partition note 3, 2/A-410) = 9.5', False),
    'Break Room 106': (9.5, 'ACT-3 9\'-0" (A-121) + 6" (A-410 partition note 3, 2/A-410) = 9.5', False),
    "Manager's Office 105": (9.5, 'ACT-3 9\'-0" (A-121) + 6" (A-410 partition note 3, 2/A-410) = 9.5', False),
    "Women's Restroom 109": (9.0, 'GWB 9\'-0" (A-121); W.R. gyp bd on wet side to B.O. gyp ceiling (2/A-410, 5/A-410)', True),
    "Men's Restroom 108": (9.0, 'GWB 9\'-0" (A-121); W.R. gyp bd on wet side to B.O. gyp ceiling (2/A-410, 5/A-410)', True),
    'Cafe Seating 102': (None, 'full height of partial wall (3/A-410, 4/A-410)', False),
    'Cafe Workroom 104': (10.5, 'ACT-1 10\'-0" (A-121) + 6" (A-410 partition note 3) = 10.5', False),
    'Cafe 103': (None, 'OPEN TO DECK (A-121, Cafe) - board to deck', False),
    'Grab & Go': (7.583, 'GWB 7\'-1" (A-121) + 6" (A-410 partition note 3) = 7.583', False),
}
def face(side, room, wall_h, length=None, src=None, board=None, layers=1):
    h, hs, mr = CEIL[room]
    hh = wall_h if h is None else min(h, wall_h)
    # MR: el paquete carga MR solo detrás de toilet / lavatory (D1 / 59.9); en este set los fixtures van contra el
    # exterior EXT-07 (gyp by future tenant). Las caras de wet room van regular + RFI-11 (A-410 nota 7, 2/A-410).
    f = {'side': side, 'room': room, 'board': board or '5/8 regular', 'layers': layers,
         'height_ft': round(hh, 3), 'height_source': hs if h is not None else hs + f' = wall height {wall_h}'}
    if mr and not board:
        f['wet_room_note'] = 'A-410 partition note 7 / 2/A-410: W.R. board in wet rooms - not loaded (fixtures back onto exterior EXT-07) - RFI-11'
    if length is not None:
        f['length_ft'] = round(length, 2); f['length_source'] = src or 'A-101 (vector, split at room boundary)'
    return f
S = 'Sales Area 101'
FACES = {
 'W2-01': [('A', 'Storage 112'), ('B', S)], 'W2-02': [('A', S), ('B', 'Storage 112')],
 'W2-03': [('A', 'Stock Room 111'), ('B', S, 81.12), ('B', 'Corridor 110', 13.12)],
 'W2-04': [('A', S), ('B', 'Corridor 110', 29.04), ('B', 'Break Room 106', 19.03), ('B', "Manager's Office 105", 8.69)],
 'W2-05': [('A', 'Corridor 110'), ('B', 'Corridor 110', 5.41), ('B', "Women's Restroom 109", 7.51)],
 'W2-06.1': [('A', 'Corridor 110'), ('B', "Women's Restroom 109")],
 'W2-06.2': [('A', "Women's Restroom 109"), ('B', 'Corridor 110')],
 'W2-06.3': [('A', 'Corridor 110'), ('B', "Women's Restroom 109", 'r:18.05/36.4'), ('B', "Men's Restroom 108", 'r:18.35/36.4')],
 'W2-06.4': [('A', 'Corridor 110'), ('B', "Men's Restroom 108")],
 'W2-06.5': [('A', 'Corridor 110'), ('B', "Men's Restroom 108", 'r:61.95/101.6'), ('B', 'Janitor Closet 107', 'r:39.65/101.6')],
 'W2-07': [('A', "Men's Restroom 108"), ('B', 'Janitor Closet 107')],
 'W2-08': [('A', 'Corridor 110', 5.41), ('A', 'Janitor Closet 107', 7.51), ('B', 'Break Room 106')],
 'W2-09': [('A', 'Break Room 106'), ('B', "Manager's Office 105")],
 'W5-01': [('A', "Women's Restroom 109"), ('B', "Men's Restroom 108")],
}
for k in ('W3-01', 'W3-02', 'W3-03', 'W3-04', 'W3-05', 'W3-06', 'W4-02', 'W4-03'):
    FACES[k] = [('A', 'Cafe Seating 102' if k.startswith('W3') else S), ('B', S)]
CEIL['Sales Area 101 (partial wall)'] = CEIL['Cafe Seating 102']
if FINAL:
    if not REV3:
        FACES['W2-05'] = [('A', 'Corridor 110'), ('B', "Women's Restroom 109")]
    for w in walls['A-101']:
        if w['tag'] == '4':
            FACES[w['id']] = [('A', S), ('B', S)]
for k in ('W4-01', 'W4-04'):
    for i in range(1, 5):
        FACES[f'{k}.{i}'] = [('A', S)]
for i in range(1, 7):
    FACES[f'W4-02.{i}'] = [('A', S), ('B', S)]; FACES[f'W4-03.{i}'] = [('A', S), ('B', S)]
NONE_EXT = ('5/8" GYP BD BY FUTURE TENANT (%s): gyp bd EXCLUDED from our scope (estimator decision) - RFI-01; '
            'framing only')
for sh in walls:
    for w in walls[sh]:
        wid, t = w['id'], w['tag']
        if t in ('1', '1A', '1C', '1B'):
            w['faces'] = []
            w['faces_none_reason'] = NONE_EXT % DET[t]
            if t == '1B':   # auditoría F-01: 1/2" exterior gyp sheathing de 1B/A-410 (cara exterior, altura del wall)
                w['faces'] = [{'side': 'A' if w['location'].split()[0].rstrip(',') in ('West', 'North') else 'B', 'room': 'Exterior face (sheathing)', 'board': '1/2 exterior gyp sheathing',
                               'layers': 1, 'height_ft': w['height_ft'],
                               'height_source': '1B/A-410 1/2" EXTERIOR GYP SHEATHING full stud height = wall height '
                                                + str(w['height_ft']) + ' (product vs glass mat A-001A: RFI-26)'}]
                w['faces_none_reason'] += '; 1/2" exterior gyp sheathing carried on the exterior face (1B/A-410)'
            continue
        spec = FACES.get(wid)
        if spec is None:
            continue
        fl = []
        L = w['length_ft']
        porside = {}
        for s_ in spec:
            porside.setdefault(s_[0], []).append(s_)
        for side, lst in porside.items():
            if len(lst) == 1:
                fl.append(face(side, lst[0][1], w['height_ft']))
                continue
            fijos = 0.0; vals = []
            for s_ in lst:
                v = s_[2] if len(s_) > 2 else None
                if isinstance(v, str) and v.startswith('r:'):
                    a, b = v[2:].split('/'); v = round(L * float(a) / float(b), 2)
                vals.append(v); fijos += v or 0.0
            vals = [v if v is not None else round(L - fijos, 2) for v in vals]
            vals[-1] = round(L - sum(vals[:-1]), 2)
            for s_, v in zip(lst, vals):
                fl.append(face(side, s_[1], w['height_ft'], v))
        if t in ('3', '4'):
            for f in fl:
                f['height_ft'] = w['height_ft']; f['height_source'] = DET[t] + ' T.O. WALL (board full height)'
        w['faces'] = fl
json.dump(walls, open('/tmp/claude-0/-home-user-Reading-Plans/b9c208e2-64c4-5dc6-9d1d-2546bd4c85dc/scratchpad/lecturaA/_walls_tmp.json', 'w'), indent=1)
print('faces ok')

# ---------------------------------------------------------------- Cafe (A-221): caras y FRT plywood
CEIL['Cafe 103'] = (None, 'OPEN TO DECK (A-121 Cafe tag) - board to wall height', False)
def bw(w): return w['band']
strips = []
def strip(w, side, room, h, hsrc, mat='frt_5_8', label='5/8" FRT PLYWOOD', length=None):
    strips.append({'ref': f"{w['id']}-{side}-FRT", 'wall': w['id'], 'lf': round(length or w['length_ft'], 2),
                   'width_ft': round(h, 3), 'material': mat, 'uso': 'substrate', 'label': label,
                   'source': w['detail'], 'room': room,
                   'op': f"{round(length or w['length_ft'], 2)} LF x {round(h, 3)} ft ({hsrc})"})
CAFE_RFI = 'height not printed (A-221 sections break at top; A-225 finish plan; A-226A elevations give finish tops only) - loaded to wall height per rule 53.3 - RFI-06'
for w in walls['A-221']:
    wid, t, H = w['id'], w['tag'], w['height_ft']
    if t in ('H1',):
        if wid == 'C-H1-N':
            b = bw(w); gg = round((b['hi'] - (1112.1 - 10.86)) / 36.0, 2)
            w['faces'] = [face('A', 'Sales Area 101', H, round(w['length_ft'] - gg, 2)),
                          face('A', 'Grab & Go', H, gg, 'A-221 (vector, x of H3b face)'),
                          face('B', 'Cafe Workroom 104', H)]
            strip(w, 'A', 'Sales Area 101', H, CAFE_RFI, length=w['length_ft'] - gg)
            strip(w, 'B', 'Cafe Workroom 104', 10.5, 'to ACT-1 10\'-0" + 6" (assumed equal to GWB; G/A-221 H2a note) - RFI-06')
        else:
            w['faces'] = [face('A', "Manager's Office 105", H), face('B', 'Cafe Workroom 104', H)]
            strip(w, 'B', 'Cafe Workroom 104', 10.5, 'to ACT-1 10\'-0" + 6" - RFI-06')
    elif t == 'H2a':
        w['faces'] = [face('A', 'Cafe Workroom 104', H), face('B', 'Cafe 103', H)]
        strip(w, 'A', 'Cafe Workroom 104', 10.5, 'G/A-221 "H2a = 5/8" GWB, 5/8" FRT PLYWOOD" to ACT-1 + 6" - RFI-06')
        strip(w, 'B', 'Cafe 103', H, CAFE_RFI)
    elif t == 'H2b':
        w['faces'] = []; w['faces_none_reason'] = 'G/A-221 "H2b = 5/8" FRT BOTH SIDES" - plywood only (plywood_strips)'
        strip(w, 'A', 'Cafe Workroom 104', 10.5, 'G/A-221 FRT both sides, to ACT-1 + 6" - RFI-06')
        strip(w, 'B', 'Cafe Workroom 104', 10.5, 'G/A-221 FRT both sides, to ACT-1 + 6" - RFI-06')
    elif t in ('H3a', 'H3b'):
        w['faces'] = [face('B', 'Grab & Go', H)]
        if t == 'H3a':
            strip(w, 'A', 'Sales Area 101', H, 'H/A-221 "H3a = PLYWOOD TO TOP OF WD-1": WD-1 top not printed - loaded to wall height (53.3) - RFI-06')
        else:
            strip(w, 'A', 'Sales Area 101', 8.0, 'H/A-221 "H3b = PLYWOOD UP TO 8\'-0"" [CONFIRMED]')
    elif t == 'E2':
        w['faces'] = []; w['faces_none_reason'] = 'E/A-221 "E2-5/8" FRT PLYWOOD" only (plywood_strips); other side = void at existing exterior wall'
        strip(w, 'A', 'Cafe Workroom 104', H, CAFE_RFI)
    elif t == 'E1':
        w['faces'] = [face('A', 'Cafe 103', H, board='1/2 cement board')]
        w['faces'][0]['height_source'] = 'E/A-221 "E1-1/2" CEMENT BOARD"; ' + CAFE_RFI
    elif t == 'F':
        w['faces'] = []; w['faces_none_reason'] = 'F/A-221 "5/8" FRT PLYWOOD" one side only (plywood_strips)'
        strip(w, 'A', 'Cafe 103', H, 'F/A-221 to bottom of nested stud bracing (elevation not printed) - RFI-06')
    elif t == 'I':
        w['faces'] = [face('A', 'Cafe 103', H)]
        w['faces'][0]['height_source'] = 'I/A-221 "5/8" GWB FROM TOP OF WD-1 TO DECK": WD-1 top not printed - GWB loaded full height (53.3) - RFI-08'
    elif t in ('A', 'B', 'C', 'D'):
        w['faces'] = [face('A', 'Cafe 103', H, board='1/2 cement board'), face('B', 'Cafe 103', H, board='1/2 cement board')]
        for f in w['faces']:
            f['height_source'] = f"{DET[t]} 1/2\" cementitious board both sides, B.O. slab to T.O. stud {H} ft"
        if t in ('A', 'B'):
            strip(w, 'A', 'Cafe 103 (customer side)', H, f'{DET[t]} "3/4" FRT PLYWOOD (SUBSTRATE)" to T.O. stud', mat='frt_3_4', label='3/4" FRT PLYWOOD')
json.dump(walls, open('/tmp/claude-0/-home-user-Reading-Plans/b9c208e2-64c4-5dc6-9d1d-2546bd4c85dc/scratchpad/lecturaA/_walls_tmp.json', 'w'), indent=1)
json.dump(strips, open('/tmp/claude-0/-home-user-Reading-Plans/b9c208e2-64c4-5dc6-9d1d-2546bd4c85dc/scratchpad/lecturaA/_strips_tmp.json', 'w'), indent=1)
print('cafe ok', len(strips))


# ---------------------------------------------------------------- column surrounds C25 (keynote A-101) y soffit sides
KN = {k['id']: k for k in json.load(open(OUT + '/img_cache/keynotes_p6.json'))}
for i, kid in enumerate([26, 27, 28, 29, 30, 64, 65, 66, 67]):
    k = KN[kid]
    walls['A-101'].append({'id': f'CW-{i + 1:02d}', 'tag': '', 'keynote': 'C25', 'element': 'column_wrap', 'sheet': 'A-101', 'page': 6,
        'location': 'Sales Area 101 - existing column, new 24"x24" GWB surround (keynote C25)',
        'source': 'A-101', 'detail': 'C25/A-101', 'detail_source': 'A-101 construction plan key note C25',
        'stud_size': '3-5/8"', 'stud_source': 'A-101 key note C25 "OVER 3 5/8" METAL FRAMING"', 'oc_in': 16,
        'oc_source': 'default 16" O.C. (not printed) - RFI-17',
        'height_ft': 8.0, 'height_source': 'A-101 key note C25 "FROM SLAB TO 8\'-0" AFF"', 'height_status': 'CONFIRMED',
        'length_ft': 8.0, 'length_source': 'A-101 key note C25 24"x24" = 4 faces x 2\'-0"', 'length_op': '4 x 2.0 = 8.0',
        'faces_ft': [2.0, 2.0, 2.0, 2.0], 'fos_chain': {'value': [2.0], 'source': 'A-101 key note C25 "24"x24" GWB SURROUND"'},
        'faces': [{'side': 'A', 'room': 'Sales Area 101', 'board': '5/8 regular', 'layers': 1, 'height_ft': 8.0,
                   'height_source': 'A-101 key note C25 to 8\'-0" AFF', 'length_ft': 8.0, 'length_source': 'A-101 key note C25 (4 x 2\'-0")'}],
        'tag_ids': [], 'status': 'CONFIRMED', 'img': 'img_cache/keynotes_contactos.png',
        'band': {'ori': 'BOX', 'c0': round(k['cx'] - 9, 2), 'c1': round(k['cx'] + 9, 2), 'lo': round(k['cy'] - 9, 2),
                 'hi': round(k['cy'] + 9, 2), 'sheet': 'A-101'}})
SS = [('SS-N', 'outer', 'H', 331.6, 1248.24, 2067.96, 25.0 - 11.0, 'Cafe 11\'-0" zone N open edge to Sales'),
      ('SS-E', 'outer', 'V', 2067.96, 331.6, 695.76, 25.0 - 11.0, 'Cafe 11\'-0" zone E open edge to Sales'),
      ('SS-IN-N', 'inner', 'H', 470.65, 1231.8, 1951.8, 25.0 - 11.5, 'Cafe 11\'-6" band N edge (6" step)'),
      ('SS-IN-E', 'inner', 'V', 1951.8, 470.65, 695.76, 25.0 - 11.5, 'Cafe 11\'-6" band E edge (6" step)')]
for sid, line, ori, c, lo, hi, h, loc in SS:
    L = round((hi - lo) / 36.0, 2)
    fh = h if line == 'outer' else 0.5
    walls['A-221'].append({'id': sid, 'tag': '', 'element': 'soffit_side', 'soffit_of': 'Cafe 103 - 11\'-0" GWB zone',
        'drop_line': line, 'sheet': 'A-221', 'page': 15, 'location': loc, 'source': '2/A-221', 'detail': '2/A-221',
        'detail_source': '2/A-221 "3 5/8" @ 16" O.C. METAL STUD UP TO DECK"', 'stud_size': '3-5/8"', 'stud_source': '2/A-221',
        'oc_in': 16, 'oc_source': '2/A-221', 'height_ft': h,
        'height_source': ('B.O. deck 25\'-0" (1/A-400B) - soffit ' + ('11\'-0"' if line == 'outer' else '11\'-6"') + ' (A-121); studs up to deck per 2/A-221'),
        'height_status': 'DERIVED', 'length_ft': L, 'length_source': 'A-221 (vector, dashed soffit edge)',
        'length_op': f'({hi} - {lo}) / 36 = {L}', 'tag_ids': [], 'status': 'DERIVED', 'img': 'img_ceilings/A121_cafe_GWB_zones.png',
        'faces': [{'side': 'A', 'room': 'Cafe 103', 'board': '5/8 regular', 'layers': 1, 'height_ft': fh,
                   'height_source': ('2/A-221 5/8" GWB on the open face to deck (T.O. WD-1 split not printed, full height per 53.3) - RFI-14' if line == 'outer' else '2/A-221 6" GWB return 11\'-6" - 11\'-0" = 0.5')}],
        'band': ({'ori': 'H', 'c0': c - 2.6, 'c1': c + 2.6, 'lo': lo, 'hi': hi, 'sheet': 'A-221'} if ori == 'H'
                 else {'ori': 'V', 'c0': c - 2.6, 'c1': c + 2.6, 'lo': lo, 'hi': hi, 'sheet': 'A-221'})})


# ---------------------------------------------------------------- evidencia por campo (reglas.py, modo final)
import pymupdf as _fz
_DOC = _fz.open('/tmp/claude-0/-home-user-Reading-Plans/b9c208e2-64c4-5dc6-9d1d-2546bd4c85dc/scratchpad/bidset/bidset_SIN_MARKUPS.pdf')
_SEG = {}
def _segs(pg):
    if pg not in _SEG:
        p = _DOC[pg - 1]; M = p.rotation_matrix; L = []
        for dr in p.get_drawings():
            for it in dr['items']:
                if it[0] == 'l':
                    L.append((_fz.Point(it[1]) * M, _fz.Point(it[2]) * M))
                elif it[0] == 'c':
                    pts = [_fz.Point(q) * M for q in it[1:5]]
                    prev = pts[0]
                    for k in range(1, 9):
                        t = k / 8; a = (1 - t) ** 3; b = 3 * (1 - t) ** 2 * t; c = 3 * (1 - t) * t * t; d_ = t ** 3
                        q = _fz.Point(a * pts[0].x + b * pts[1].x + c * pts[2].x + d_ * pts[3].x,
                                      a * pts[0].y + b * pts[1].y + c * pts[2].y + d_ * pts[3].y)
                        L.append((prev, q)); prev = q
        _SEG[pg] = L
    return _SEG[pg]
def _hit(pg, p, n, lim):
    """cara más lejana a cada lado dentro de lim (la propia línea del eje cuenta como t = 0)."""
    best = {1: None, -1: None}
    for a, b in _segs(pg):
        dx, dy = b.x - a.x, b.y - a.y
        den = n[0] * dy - n[1] * dx
        if abs(den) < 1e-9: continue
        t = ((a.x - p[0]) * dy - (a.y - p[1]) * dx) / den       # p + t n
        u = ((a.x - p[0]) * n[1] - (a.y - p[1]) * n[0]) / den
        if -0.02 <= u <= 1.02 and abs(t) <= lim:
            for sg in ((1, -1) if abs(t) < 0.3 else ((1,) if t > 0 else (-1,))):
                tt = 0.0 if abs(t) < 0.3 else t
                if best[sg] is None or abs(tt) > abs(best[sg]): best[sg] = tt
    return best
STATUS_ES = {'CONFIRMED': 'CONFIRMADO', 'DERIVED': 'DERIVADO', 'PENDING': 'PENDIENTE'}
TOPT = {'2': 'deep leg slip track at underside of deck, slotted deflection - 8/A-410 Top Track Detail, 2/A-410',
        '5': 'deep leg slip track at underside of deck - 3/A-410, 5/A-410',
        '3': 'fixed top track at T.O. wall 8\'-0" A.F.F. (open top, capped by board) - 3/A-410',
        '4': 'fixed top track at T.O. wall 7\'-6" A.F.F. - 4/A-410',
        'E1': 'top track to underside of deck - E/A-221', 'E2': 'top track to underside of deck - E/A-221',
        'I': 'top track to underside of deck - I/A-221', 'F': 'top track at bottom of nested stud bracing - F/A-221',
        'H1': 'top track (break line, height not printed) - G/A-221', 'H2a': 'top track (break line) - G/A-221',
        'H2b': 'top track (break line) - G/A-221', 'H3a': 'top track (break line) - H/A-221', 'H3b': 'top track (break line) - H/A-221',
        'A': 'fixed top track under countertop - A/A-221', 'B': 'fixed top track under countertop - B/A-221',
        'C': 'fixed top track under countertop - C/A-221', 'D': 'fixed top track at 1\'-0" - D/A-221'}
DIMG = {'A-410': ('4_canon/img/det/A410_details_4_3_2.png', '4_canon/img/det/A410_details_1C_1A_1B_1.png', '4_canon/img/det/A410_details_5_bracing_toptrack.png'),
        'A-221': ('4_canon/img/det/A221_sections_E_F_G.png', '4_canon/img/det/A221_sections_H_I.png', '4_canon/img/det/A221_counters_A_B_C_D.png')}
def dimg(det):
    n, sh = det.split('/') if '/' in det else ('', det)
    if sh == 'A-410':
        return DIMG['A-410'][1] if n in ('1', '1A', '1B', '1C') else (DIMG['A-410'][2] if n == '5' else DIMG['A-410'][0])
    if sh == 'A-221':
        if n in ('A', 'B', 'C', 'D'): return DIMG['A-221'][2]
        if n in ('H', 'I'): return DIMG['A-221'][1]
        if n == '2': return '4_canon/img/det/A221_soffit_sections_2_3.png'
        return DIMG['A-221'][0]
    return '4_canon/img/det/A101_keynotes_C25.png'
def evidencia(walls):
    for sh, L in walls.items():
        esc = SCALE[sh]; pg = 6 if sh == 'A-101' else 15
        con_tag = {w['id'].split('.')[0] for w in L if w.get('tag_ids')}
        for w in L:
            for k in ('length_status', 'height_status', 'status'):
                v = str(w.get(k) or ('DERIVED' if k != 'height_status' else 'CONFIRMED')).upper()
                w[k] = STATUS_ES.get(v, v if v in STATUS_ES.values() else 'DERIVADO')
            if w['tag'] in ('H1', 'H2a', 'H2b', 'H3a', 'H3b', 'F'):
                w['height_status'] = 'DERIVADO'
                w['height_op'] = 'not printed -> B.O. deck 25\'-0" (1/A-400B) per rule 53.3 / 60.11 (more material) - RFI-06'
                w['sheets_searched'] = 'A-221 (sections E-I, 1-3), A-225 (finish plan and details 1-10), A-226A / A-226B (cafe elevations: finish tops 11\'-0", 11\'-6", 15\'-0" only), A-121 (RCP), A-400B, A-410, A-002 specifications: no top of stud printed'
                w['pending_reason'] = 'stud height of the cafe partition not printed (break line at the top of the section)'
            if w['tag'] == 'I':
                w['sheets_searched'] = 'A-221 (I/A-221, 1/A-221), A-225, A-226A / A-226B (WD-1 top not printed), A-121'
                w['pending_reason'] = 'top of WD-1 (split between FRT plywood and GWB on the cafe face) not printed - RFI-08'
            if w.get('length_status') == 'CONFIRMADO' and not re.search(r'[A-Z]-\d{3}', str(w.get('length_source'))):
                w['length_status'] = 'DERIVADO'
            b = w['band']
            if b['ori'] in ('H', 'V'):
                w['thickness_measured_in'] = round(abs(b['c1'] - b['c0']) / esc * 12, 2)
                w['thickness_check'] = f"faces {b['c0']} / {b['c1']} pt on {sh} = {w['thickness_measured_in']} in"
            elif b['ori'] == 'D':
                (x0, y0), (x1, y1) = b['p0'], b['p1']
                ux, uy = x1 - x0, y1 - y0; ll = math.hypot(ux, uy); n = (-uy / ll, ux / ll)
                lim = HALF[sh].get(w['tag'], 2.5) * (2.2 if w['tag'] in ('1B',) else 1.0) + 1.5
                h0, h1 = _hit(pg, (x0, y0), n, lim), _hit(pg, (x1, y1), n, lim)
                if all(h0[s_] is not None and h1[s_] is not None for s_ in (1, -1)):
                    ft = [[round(x0 + h0[-1] * n[0], 2), round(y0 + h0[-1] * n[1], 2)], [round(x1 + h1[-1] * n[0], 2), round(y1 + h1[-1] * n[1], 2)]]
                    fb = [[round(x0 + h0[1] * n[0], 2), round(y0 + h0[1] * n[1], 2)], [round(x1 + h1[1] * n[0], 2), round(y1 + h1[1] * n[1], 2)]]
                    b['faces_top'], b['faces_bottom'] = ft, fb
                    lt, lb = math.dist(*ft) / esc, math.dist(*fb) / esc
                    w['thickness_measured_in'] = round((abs(h0[1]) + abs(h0[-1])) / esc * 12, 2)
                    w['thickness_check'] = f"normal through the ends hits faces at {round(h0[-1], 2)} / {round(h0[1], 2)} pt"
                    w['faces_avg_info'] = round((lt + lb) / 2, 2)
                    if abs(w['length_ft'] - (lt + lb) / 2) > 0.05:
                        w['length_op'] = w.get('length_op', '') + f"; faces {round(lt, 2)} / {round(lb, 2)} -> average {round((lt + lb) / 2, 2)} (R72.2)"
                        w['length_ft'] = round((lt + lb) / 2, 2)
            if b['ori'] != 'BOX':
                w['length_basis'] = 'axis (centerline of the stud) between nodes; face to face where taken from reading B'
            w['detail_img'] = dimg(w.get('detail') or '')
            w['img'] = w.get('img') or dimg(w.get('detail') or '')
            if w['tag'] in TOPT:
                w['top_track'] = TOPT[w['tag']]
            elif w['tag'] in ('1', '1A', '1B', '1C'):
                w['top_track'] = 'top track to underside of deck (furring full height, R-21 batt to deck per ' + DET[w['tag']] + '); deflection per A-410 partition note 7'
            if w.get('element') == 'wall' and w['tag'] and not w.get('tag_ids'):
                par = w['id'].split('.')[0]
                w['untagged_reason'] = (f"segment of wall {par} (tag on its first segment); joins the tagged wall per particion.py eje"
                                        if par in con_tag else 'untagged return / TYP. copy of a tagged element on ' + sh + ' - joins the tagged wall it touches (particion.py eje)') + f' ({sh})'

if FINAL:
    evidencia(walls)

# ---------------------------------------------------------------- nodos (L / T / free) desde las bands
def ends(w):
    b = w['band']
    if b['ori'] == 'H':
        e = (b['c0'] + b['c1']) / 2; return [(b['lo'], e), (b['hi'], e)]
    if b['ori'] == 'V':
        e = (b['c0'] + b['c1']) / 2; return [(e, b['lo']), (e, b['hi'])]
    if b['ori'] == 'D':
        return [tuple(b['p0']), tuple(b['p1'])]
    return []
def on_body(p, v, tol):
    b = v['band']
    if b['ori'] == 'H':
        e = (b['c0'] + b['c1']) / 2
        return abs(p[1] - e) <= tol and b['lo'] + tol < p[0] < b['hi'] - tol
    if b['ori'] == 'V':
        e = (b['c0'] + b['c1']) / 2
        return abs(p[0] - e) <= tol and b['lo'] + tol < p[1] < b['hi'] - tol
    if b['ori'] == 'D':
        (x0, y0), (x1, y1) = b['p0'], b['p1']; dx, dy = x1 - x0, y1 - y0; L2 = dx * dx + dy * dy
        t = ((p[0] - x0) * dx + (p[1] - y0) * dy) / L2
        if not (0.02 < t < 0.98): return False
        return math.hypot(p[0] - x0 - t * dx, p[1] - y0 - t * dy) <= tol
    return False
nodes = []
for sh in walls:
    tol = 1.0 * SCALE[sh]
    W = [w for w in walls[sh] if w['band']['ori'] != 'BOX' and w.get('element') != 'column_wrap']
    usados = set()
    for w in W:
        for i, p in enumerate(ends(w)):
            if (w['id'], i) in usados: continue
            hecho = False
            for v in W:                                   # L: extremo con extremo de otro wall
                if v is w: continue
                for j, q in enumerate(ends(v)):
                    if (v['id'], j) in usados: continue
                    if math.dist(p, q) <= tol:
                        same = (w['band']['ori'] == v['band']['ori'] and w['band']['ori'] in 'HV')
                        kind = 'split' if same and w['id'].split('.')[0] == v['id'].split('.')[0] else 'L'
                        n = {'id': f"N{len(nodes) + 1}", 'kind': kind, 'walls': [w['id'], v['id']],
                             'source': f"{sh} (vector: ends within {tol / SCALE[sh]:.1f} ft)"}
                        if kind == 'split': n['why'] = 'one wall drawn in collinear segments (cache polyline)'
                        nodes.append(n); usados |= {(w['id'], i), (v['id'], j)}; hecho = True; break
                if hecho: break
            if hecho: continue
            for v in W + [x for x in walls[sh] if x['band']['ori'] == 'BOX']:
                if v is w: continue
                if v['band']['ori'] == 'BOX':
                    b = v['band']
                    if b['c0'] - tol <= p[0] <= b['c1'] + tol and b['lo'] - tol <= p[1] <= b['hi'] + tol:
                        nodes.append({'id': f"N{len(nodes) + 1}", 'kind': 'T', 'branch': w['id'], 'through': v['id'],
                                      'source': f"{sh} (vector)"}); usados.add((w['id'], i)); hecho = True; break
                    continue
                if on_body(p, v, tol):
                    nodes.append({'id': f"N{len(nodes) + 1}", 'kind': 'T', 'branch': w['id'], 'through': v['id'],
                                  'source': f"{sh} (vector: end on the body of {v['id']})"})
                    usados.add((w['id'], i)); hecho = True; break
            if not hecho:
                nodes.append({'id': f"N{len(nodes) + 1}", 'kind': 'free', 'wall': w['id'],
                              'source': f"{sh} (vector: free end)"}); usados.add((w['id'], i))
    for v in walls[sh]:
        if v['band']['ori'] == 'BOX' and v.get('element') != 'column_wrap':
            nodes.append({'id': f"N{len(nodes) + 1}", 'kind': 'free', 'wall': v['id'], 'source': 'closed box (one end)'})
            nodes.append({'id': f"N{len(nodes) + 1}", 'kind': 'free', 'wall': v['id'], 'source': 'closed box (other end)'})
from collections import Counter
print('nodes', Counter(n['kind'] for n in nodes))
json.dump(nodes, open('/tmp/claude-0/-home-user-Reading-Plans/b9c208e2-64c4-5dc6-9d1d-2546bd4c85dc/scratchpad/lecturaA/_nodes_tmp.json', 'w'), indent=1)

# ---------------------------------------------------------------- cambios de type sin nodo dibujado (R75.5 / R73.10)
TCR = {
 'EXT-01': {'alternativas': ['1A/1 change at W2-03 centerline x=498.5 pt (cache reading; printed 15\'-7" to face of W2-03 supports it)',
                             '1A/1 change at the edge of the adjacent tenant building x=800.4 pt (A-101 north facade, EXTERIOR vs ADJACENT TENANT)'],
            'delta_lf': round((800.4 - 498.5) / 9.0, 2), 'source': 'A-101 north facade (no node, no dimension at the 1A/1 change) - RFI-02'},
 'C-E2': {'alternativas': ['E2/E1 change at H2a centerline x=1223.65 pt (taken)', 'at the Workroom face of H2a x=1216.33 pt',
                           'at the Cafe face of H2a x=1230.97 pt'],
          'delta_lf': round((1230.97 - 1216.33) / 36.0 / 2, 2), 'source': '1/A-221 (no node drawn at the E2/E1 change) - RFI-05'},
}
for sh in walls:
    for w in walls[sh]:
        if w['id'] in TCR:
            w['type_change_rfi'] = TCR[w['id']]


TITLES = {'1/A-410': 'Exterior CMU', '1A/A-410': 'Exterior - Split-Faced CMU', '1B/A-410': 'Exterior Wall - Stone at CMU',
          '1C/A-410': 'Exterior Wall - Stone at Stud', '2/A-410': 'Non-Rated Full Height Partition', '3/A-410': 'Non-Rated Partial Height Partition',
          '4/A-410': 'Non-Rated Partial Height Partition', '5/A-410': 'Non-Rated Full Height Partition',
          'E/A-221': 'Section Wall Typ. E1/E2', 'F/A-221': 'Section Wall Typ. F', 'G/A-221': 'Section Wall Typ. H1/H2',
          'H/A-221': 'Section Wall Typ. H3', 'I/A-221': 'Section Wall Typ. I', 'A/A-221': 'Section Through Front Counter',
          'B/A-221': 'Section Wall Typ. B', 'C/A-221': 'Section Wall Typ. C', 'D/A-221': 'Section Wall Typ. D',
          '2/A-221': 'Soffit Section - Cafe Sales Area', 'C25/A-101': 'Key note C25 - existing column, new 24"x24" GWB surround over 3-5/8" metal framing from slab to 8\'-0" AFF'}
NOTES = {'1/A-410': '3-5/8" metal stud, 5/8" gyp bd BY FUTURE TENANT, R-21 batt full height to underside of deck, vapor barrier, 10" CMU (re: structural)',
         '1A/A-410': '3-5/8" metal stud, 5/8" gyp bd BY FUTURE TENANT, R-21 batt to deck, 10" split faced CMU',
         '1B/A-410': '8" metal stud, 5/8" gyp bd BY FUTURE TENANT, 1/2" exterior gyp sheathing, weather barrier, 1" air gap, 4" stone veneer',
         '1C/A-410': '3-5/8" metal stud, 5/8" gyp bd BY FUTURE TENANT, 10" CMU, 4" stone veneer',
         '2/A-410': '3-5/8" studs @16" to bottom of nested stud bracing (see schedule for gauge); 5/8" gyp each side; extend gyp to deck where no ceiling; restroom/cafe walls W.R. gyp on wet side to B.O. gyp ceiling; calls 8/A-410 (top track, slotted deflection) and 5/A-410 (lateral bracing)',
         '3/A-410': '3-5/8" studs @16" to bottom of nested stud bracing; T.O. wall 8\'-0" A.F.F.; 5/8" gyp both sides; F.R.P. over 5/8" plywood where shelving occurs; 3-5/8" x 20 ga track w/ (2) 1/4" Hilti Kwik HUS-EZ + moment clip (A/A-410)',
         '4/A-410': 'as 3/A-410 with T.O. wall 7\'-6" A.F.F.', '5/A-410': '6" studs @16" to bottom of nested stud bracing; 5/8" gyp each side; restroom walls W.R. gyp to B.O. gyp ceiling',
         'E/A-221': '6" metal studs @16" to underside of deck; E1 1/2" cement board, E2 5/8" FRT plywood; void at existing wall',
         'F/A-221': '3-5/8" metal studs @16" to bottom of nested stud bracing; 5/8" FRT plywood', 'G/A-221': 'H1 = 6" stud, H2 = 3-5/8" stud; 5/8" FRT plywood + 5/8" gypsum board (sales); H2a 5/8" GWB + 5/8" FRT plywood; H2b 5/8" FRT both sides',
         'H/A-221': '6" metal studs @16"; 5/8" gypsum board (Grab and Go); H3a plywood to top of WD-1, H3b plywood up to 8\'-0" (sales)',
         'I/A-221': '6" metal studs @16"; 5/8" FRT plywood to top of WD-1, 5/8" GWB from top of WD-1 to deck',
         'A/A-221': '3-5/8" metal studs @16"; 1/2" cementitious board + 3/4" FRT plywood substrate (customer side), FRP-1 over 1/2" cementitious board (cafe side); 2\'-8 1/2" B.O. slab to T.O. stud',
         'B/A-221': '3-5/8" metal studs @16"; 3/4" FRT plywood + 1/2" cementitious board; 2\'-8 1/2"', 'C/A-221': '3-5/8" metal studs; 1/2" cementitious board both sides; 2\'-8 1/2"',
         'D/A-221': '3-5/8" metal studs @16"; FRP-1 over 1/2" cementitious board; 1\'-0" B.O. slab to T.O. stud',
         '2/A-221': '3-5/8" @16" metal stud up to deck at the open edge and at the 11\'-6" step, cross bracing as req\'d, 5/8" GWB, 5/8" F.R.T. plywood, WD-1, wood corner trim',
         'C25/A-101': '24"x24" GWB surround over 3-5/8" metal framing, slab to 8\'-0" AFF'}
SEAL = {'sealant_none_reason': 'CONT. ACOUSTICAL SEALANT drawn at the base (bottom runner) - EXCLUDED in all projects (estimator standing order R77.12); no exterior sealant at base of gypsum drawn', 'sealant_source': 'see detail'}
DETAILS = {}
for d_ in sorted(set(DET.values()) | {'C25/A-101', '2/A-221'}):
    DETAILS[d_] = {'layers_per_face': 1, 'source': d_, 'layers_source': d_, 'img': dimg(d_), 'title': TITLES.get(d_, d_),
                   'notes': NOTES.get(d_, ''), **SEAL}

# ---------------------------------------------------------------- metal trim (corner bead)
trim = []
libres = Counter(n['wall'] for n in nodes if n['kind'] == 'free')
for t in ('3', '4'):
    ws = [w for w in walls['A-101'] if w['tag'] == t]
    top2 = sum(w['length_ft'] for w in ws if len(w.get('faces') or []) == 2)
    top1 = sum(w['length_ft'] for w in ws if len(w.get('faces') or []) == 1)
    h = ws[0]['height_ft']
    nfree = sum(libres[w['id']] for w in ws)
    lf = 2 * top2 + top1 + nfree * 2 * h
    trim.append({'ref': f'Corner bead - type {t} partial height walls (top edges + free ends)', 'kind': 'corner_bead', 'img': dimg(DET[t]), 'label': 'corner bead at exposed edges (criterion 53.1)',
                 'lf': round(lf, 2), 'source': DET[t],
                 'op': f"top edges 2 x {round(top2, 2)} + 1 x {round(top1, 2)} (cap box outer face) + {nfree} free end(s) x 2 corners x {h} ft = {round(lf, 2)}"})
cb = [w for w in walls['A-101'] if w['tag'] == '4' and len(w.get('faces') or []) == 1]
if not FINAL: trim.append({'ref': 'Corner bead - type 4 cap boxes outside vertical corners', 'kind': 'corner_bead', 'lf_each': 7.5,
             'qty': 8, 'lf': 60.0, 'source': '4/A-410',
             'op': '2 cap boxes x 4 outside corners x 7\'-6" (T.O. wall 4/A-410) = 60.0'})
trim.append({'ref': 'Corner bead - corridor recess (drinking fountain alcove, W2-06) outside corners', 'kind': 'corner_bead', 'img': '3_revision/res/res_W205.png', 'label': 'corner bead at outside corners (criterion 53.1)',
             'lf_each': 9.5, 'qty': 2, 'lf': 19.0, 'source': 'A-101',
             'op': '2 outside corners x 9.5 ft (ACT-3 9\'-0" + 6", corridor face) = 19.0'})

trim.append({'ref': 'Corner bead - column surrounds C25 (9 ea) outside corners', 'kind': 'corner_bead',
             'img': '5_auditoria/img/F_C25_column_surround_A101.png', 'label': 'corner bead at outside corners (criterion 53.1)',
             'lf_each': 8.0, 'qty': 36, 'lf': 288.0, 'source': 'A-101',
             'op': 'A-101 key note C25 24"x24" GWB surround slab to 8\'-0" A.F.F.: 9 columns x 4 outside corners x 8.0 ft = 288.0 (audit F-05; open top edge 72 LF PENDING)'})


# ---------------------------------------------------------------- ceilings GWB (A-121; medidos en ceilings_measured.json)
CM = {c['room']: c for c in json.load(open(OUT + '/datos/ceilings_measured.json'))}
def ceil(key, room, system, drop, detail=None, **kw):
    c = CM[key]
    d = {'room': room, 'system': system, 'area_sf': c['area_sf'], 'perimeter_ft': c['perimeter_ft'], 'ns_ft': c['ns_ft'],
         'ew_ft': c['ew_ft'], 'height_ft': c['height_ft'], 'source': 'A-121', 'area_op': c.get('area_op'),
         'img': 'img_ceilings/' + os.path.basename(c['img'].split(';')[0].strip())}
    if system in ('furring', 'stud_joist'):
        d['hanger_drop_ft'] = {'value': round(25.0 - c['height_ft'], 3),
                               'source': f"B.O. deck 25'-0\" (1/A-400B) - ceiling {c['height_ft']} (A-121) - RFI-03"}
    if detail:
        d['detail'] = detail
    d.update(kw)
    return d
ceilings = [
 ceil("Women's Restroom", "Women's Restroom 109", 'furring', None, '5/A-121'),
 ceil("Men's Restroom", "Men's Restroom 108", 'furring', None, '5/A-121'),
 ceil('Cafe - 11\'-6" GWB band (recess)', 'Cafe 103 - 11\'-6" GWB band', 'furring', None, '5/A-121'),
 ceil('Cafe - 9\'-0" GWB soffit band (storefront)', 'Cafe 103 - 9\'-0" GWB band', 'furring', None, '5/A-121'),
 ceil('Cafe Seating Area - GWB cloud', 'Cafe Seating Area 102 - GWB cloud', 'furring', None, '5/A-121',
      system_note='4/A-121 USG drywall suspension grid is drawn for this cloud (callout on cloud N edge); package carries the 5/A-121 hat channel + 1-1/2" channel system - grid alternative RFI-15'),
 ceil('Cafe - 11\'-0" GWB zone (outer L, at counter)', 'Cafe 103 - 11\'-0" GWB zone', 'framed_soffit', None, '2/A-221',
      system_callout={'detail': '2/A-221', 'cuts_this': True, 'cut_on': ['A-221'], 'source': '2/A-221 Soffit Section - Cafe Sales Area (cuts the 11\'-0" zone on 1/A-221)'},
      drop_lines={'value': 2, 'source': '2/A-221: stud lines up to deck at the outer open edge (N + E) and at the 11\'-6" step (inner)'}),
]
_cl = CM['Cafe Seating Area - GWB cloud']['perimeter_ft']
for _k, _lab in (('corner_bead', 'Corner bead - Cafe Seating GWB cloud bottom edge'), ('j_bead', 'J-bead - Cafe Seating GWB cloud top of fascia')):
    trim.append({'ref': _lab, 'kind': _k, 'img': '5_auditoria/img/F_cloud_jbead_cornerbead_4-A121.png',
                 'label': '4/A-121 J-BEAD at top of fascia + DUR-A-BEAD corner bead at bottom edge', 'lf': round(_cl, 2),
                 'source': '4/A-121', 'op': f'cloud perimeter {round(_cl, 2)} LF (A-121 measured) x 1 = {round(_cl, 2)} (audit F-06; fascia board strip height not printed - RFI-21)'})

# ---------------------------------------------------------------- aberturas
HSRC = 'A-500 door schedule + 1/A-500 typical hollow metal frame (no header drawn); no header schedule in the set (A-000 index, A-410, A-500)'
def hrfi(ro, pcs=2):
    return (f"Door header not called: if a 2-piece track header is required, +({ro} + 1.333) x {pcs} = "
            f"{round((ro + 16 / 12) * pcs, 2)} LF - RFI-09")
OPN = {  # wall -> [(ref, ro, head, xy, kind, size_src)]
 'W2-01': [('Door 14', 3.0, 7.0, (1898.8, 607.2), 'door', 'A-500 door 14 3\'-0" x 7\'-0"; vector gap 3.00 ft (A-101)')],
 'W2-03': [('Door 11', 4.0, 7.0, (498.5, 1193.5), 'door', 'A-500 door 11 4\'-0" x 7\'-0"; vector gap 4.00 ft')],
 'W2-04': [('Door 4', 3.0, 7.0, (534.7, 1290.45), 'door', 'A-500 door 4 3\'-0" x 7\'-0"; vector gap 3.00 ft')],
 'W2-08': [('Door 5', 3.0, 7.0, (761.7, 1310.3), 'door', 'A-500 door 5 3\'-0" x 7\'-0"; vector gap 3.00 ft')],
 'W2-09': [('Door 6', 3.0, 7.0, (932.95, 1310.3), 'door', 'A-500 door 6 3\'-0" x 7\'-0"; vector gap 3.00 ft')],
 'W2-06.1': [('Door 9', 3.33, 7.0, (579.1, 1339.2), 'door', 'A-500 door 9 3\'-0" x 7\'-0"; vector gap 3.33 ft (frame)')],
 'W2-06.5': [('Door 8', 3.33, 7.0, (700.6, 1339.2), 'door', 'A-500 door 8 3\'-0" x 7\'-0"; vector gap 3.33 ft (frame)'),
             ('Door 7', 3.0, 7.0, (741.9, 1339.2), 'door', 'A-500 door 7 3\'-0" x 7\'-0"; vector gap 3.00 ft')],
 'EXT-03': [('Door 13', 6.33, 7.0, (353.82, 871.7), 'door', 'A-500 door 13 EXISTING V.I.F.; furring gap 6.33 ft (A-101 vector) - RFI-10')],
 'EXT-07': [('Door 10', 3.49, 7.0, (535.7, 1410.84), 'door', 'A-500 door 10 EXISTING V.I.F.; furring gap 3.49 ft (A-101 vector) - RFI-10')],
 'EXT-04': [('Door 12', 10.0, 10.0, (300.8, 1175.3), 'door', 'A-500 door 12 type D EXISTING V.I.F. (overhead); gap 10.00 ft along the angled wall (A-101 vector); head not printed - RFI-10')],
 'C-H2a': [('Door 3', 4.0, 8.0, (1223.65, 587.8), 'door', 'A-500 door 3 4\'-0" x 8\'-0"; vector gap 4.00 ft (A-221)')],
}
items = []
for sh in walls:
    for w in walls[sh]:
        for ref, ro, head, xy, kind, ssrc in OPN.get(w['id'], []):
            w.setdefault('openings', []).append({'ref': ref, 'kind': kind, 'ro_w_ft': ro, 'head_ft': head,
                                                  'img': '4_canon/img/opn/' + ref.replace(' ', '_') + '.png',
                                                  'ro_w_op': f"gap between the jamb faces measured in vector = {ro} ft ({ssrc})",
                                                  'head_source': ('A-500 door schedule height' if ref not in ('Door 12',) else 'A-500 door 12 EXISTING V.I.F. (head not printed) - RFI-10'),
                                                  'source': ssrc, 'xy_pt': list(xy), 'header': 'not_called',
                                                  'header_source': HSRC, 'header_rfi': hrfi(ro),
                                                  'location': 'interior' if not w['tag'].startswith('1') else 'exterior',
                                                  **({'substrate_none_reason': 'Existing exterior door in existing CMU (A-500 EXISTING V.I.F.); no head / jamb detail for the furring at this opening - no substrate printed',
                                                      'jamb_return': False, 'jamb_return_source': 'A-500 (existing door, EXIST. frame; no head / jamb detail for the furring) - gyp bd by future tenant (1/A-410): no jamb return in our scope'} if w['tag'].startswith('1') else {})})
            items.append({'ref': ref, 'wall': w['id'], 'source': ssrc})
opening_schedule = {'sources': ['A-500', 'A-101', 'A-221', 'A-210', 'M-102'],
                    'sources_none': {'S': 'No structural sheets in the bid set (A-000 drawing index: Architectural, Electrical, Mechanical, Plumbing only)'},
                    'items': items + [{'ref': 'Door 1', 'source': 'A-500'}, {'ref': 'Door 2', 'source': 'A-500'}],
                    'none': [{'ref': 'Door 1', 'why': 'Vestibule exterior storefront entrance (EXISTING V.I.F., type A) - storefront system, not in a partition (A-101 C1, A-210)'},
                             {'ref': 'Door 2', 'why': 'Vestibule interior storefront doors (alum/glass, type A) - storefront system (A-101 C1/C3, A-210), not in a partition'}]}

# ---------------------------------------------------------------- tags descartados
descartes = [
 {'id': 'PT0007', 'motivo': 'Type 1 tag on the Cafe south line (A-101): the same line is drawn on enlarged plan 1/A-221 as 6" stud walls E2/E1 (E/A-221 "6" METAL STUDS @16" O.C. TO UNDERSIDE OF DECK", void at existing wall). Enlarged plan governs; counted ONCE as E1/E2 (estimator decision) - RFI-05.', 'owner': 'C-E2', 'imagen': '1_inventario/recortes/PT0007_1_A-101_p6.png'},
 {'id': 'PT0048', 'motivo': 'I tag (SIM.) points to the exposed end face of a wall (finish callout at wall end, I/A-221), not a wall line.', 'imagen': '1_inventario/recortes/PT0048_I_A-221_p15.png'},
 {'id': 'PT0049', 'motivo': 'I tag (SIM.) points to the exposed end face of a wall (finish callout at wall end, I/A-221), not a wall line.', 'imagen': '1_inventario/recortes/PT0049_I_A-221_p15.png'},
 {'id': 'PT0050', 'motivo': 'I tag at the Workroom door pier: marks the inside face finish of the E1 pier (1\'-0" x 2\'-8" HOLD), not a separate wall line - pier counted as E1 (C-E1-P).', 'owner': 'C-E1-P.1', 'imagen': '1_inventario/recortes/PT0050_I_A-221_p15.png'},
]
# ---------------------------------------------------------------- REV1 (decisiones del estimador 2026-10-24, DECISIONES_ESTIMADOR.md)
REV1 = os.environ.get('REV1') == '1'
REV2 = os.environ.get('REV2') == '1'
if REV2:
    for c_ in ceilings:
        if c_.get('system') != 'canopy_joist':
            c_['board'] = '5/8 type X'
            c_['board_source'] = '5/8" Type X (estimator decision rev2): 4/A-121, 5/A-121, A-001A Div 09 A.2'
blocking = []
existing_excluded = []
if REV1:
    PER = ('1', '1A', '1B', '1C')
    RFI01 = ('EXISTING - EXCLUDED (estimator decision RFI-01, 2026-10-24): perimeter walls types 1 / 1A / 1B / 1C are existing - '
             '1/DM-101 legend (solid = to remain) + key note 3, A-101 Construction Legend (existing exterior wall / existing '
             'partition), A-002 "PERIMETER STUDS, INSULATION, VAPOR BARRIER F/I BY LL". Framing, track, bracing and 1B sheathing '
             'excluded; interior face patch & repair = allowance (amount blank).')
    existing_excluded = [w for w in walls['A-101'] if w['tag'] in PER]
    ids = {w['id'] for w in existing_excluded}
    walls['A-101'] = [w for w in walls['A-101'] if w['tag'] not in PER]
    vistos = set()
    for w in existing_excluded:
        for t_ in w.get('tag_ids') or []:
            if t_ in vistos:
                continue
            vistos.add(t_)
            descartes.append({'id': t_, 'motivo': f"Type {w['tag']} tag on {w['id']} ({w['location']}): " + RFI01,
                              'imagen': f"1_inventario/recortes/{t_}_{w['tag']}_A-101_p6.png"})
    nn = []
    for n_ in nodes:
        ws_ = set(n_.get('walls') or []) | {n_.get('wall'), n_.get('branch'), n_.get('through'), n_.get('into')}
        if ws_ & ids:
            otros = [x for x in ws_ - ids if x]
            for o_ in otros:   # el extremo del wall nuevo muere contra el wall existente: extremo libre (stud de cierre)
                nn.append({'id': n_['id'], 'kind': 'free', 'wall': o_,
                           'source': 'A-101: end of the new wall against the EXISTING perimeter wall (RFI-01) - end stud'})
            continue
        nn.append(n_)
    nodes[:] = nn
    # aberturas de los walls existentes: puertas existentes, sin trabajo nuestro
    opening_schedule['items'] = [i_ for i_ in opening_schedule['items'] if i_.get('wall') not in ids]
    for d_ in ('Door 10', 'Door 12', 'Door 13'):
        opening_schedule['items'].append({'ref': d_, 'source': 'A-500'})
        opening_schedule['none'].append({'ref': d_, 'why': 'EXISTING door (A-500 EXISTING V.I.F.) in an EXISTING perimeter wall (RFI-01, 1/DM-101 key note 16 / 15) - no framing in our scope'})
    # board: Type X en walls nuevos (RFI-27); W.R. Type X en caras de wet rooms (RFI-11)
    WET = ("Women's Restroom 109", "Men's Restroom 108", 'Janitor Closet 107')
    ALCOVE = {('W2-06.2', 'B'), ('W2-06.3', 'A'), ('W2-06.4', 'A')}
    for sh in walls:
        for w in walls[sh]:
            for f in w.get('faces') or []:
                if f['board'] != '5/8 regular':
                    continue
                if f['room'] in WET or (w['id'], f['side']) in ALCOVE:
                    f['board'] = '5/8 type X WR'
                    f['board_source'] = ('W.R. on all wet-room faces (estimator decision RFI-11): A-410 "*" note "PROVIDE 5/8" WATER RESISTANT GYP. BD AT '
                                         'JANITOR\'S CLOSET, DRINKING FOUNTAIN, KITCHEN AND ALL TOILET LOCATIONS", partition note 7, 2/A-410; Type X per A-001A (RFI-27)')
                else:
                    f['board'] = '5/8 type X'
                    f['board_source'] = '5/8" Type X on all new walls (estimator decision RFI-27): A-001A Div 09 A.2'
    # FRT blocking (RFI-23, conteos del estimador con hileras)
    for ref, lf, lab, src, op in (
        ('BLK-STOCK', 387.0, 'FASTEN STEEL SHELVING TO FRT WOOD BLOCKING IN PARTITION (C14 / C27 shelving)', '7/A-413',
         'about 43 shelving units x 3\'-0" x 3 rows = 387 LF (audit count on A-111 / A-101 C14, C27; estimator decision RFI-23)'),
        ('BLK-RECEIVING', 69.0, 'CONTINUOUS 2x4 F.R.T. WOOD BLOCKING (TYP.)', '8A/A-413',
         'receiving table 17\'-3" (8/A-413) x 4 rows (8A/A-413) = 69.0 LF'),
        ('BLK-OFFICE', 85.6, 'F.R.T. BLOCKING IN WALL BEHIND GWB (C12)', '4/A-412',
         "Manager's Office elevations 3/A-412 + 4/A-412 about 12.9 + 8.5 = 21.4 ft x 4 rows = 85.6 LF (widths scaled on the elevations)"),
        ('BLK-BREAK', 10.67, 'C20 (A-101): PROVIDE F.R.T. BLOCKING AS NEEDED - kitchenette cabinets', '6/A-412',
         'cabinet run 2\'-9" + 2\'-7" = 5\'-4" x 2 rows = 10.67 LF (existing wall EXT-07: remove / replace gyp per A-413 general note)')):
        IMGB = {'BLK-STOCK': 'F_shelving_blocking_7-A413.png', 'BLK-RECEIVING': 'F_receiving_blocking_8A-A413.png',
                'BLK-OFFICE': 'F_office_frt_blocking_3-4-A412.png', 'BLK-BREAK': 'F_kitchenette_blocking_6-A412.png'}
        blocking.append({'ref': ref, 'lf': lf, 'material': 'FRT', 'label': lab, 'source': src, 'op': op,
                         'img': '5_auditoria/img/' + IMGB[ref]})
    ce1s = [w for w in walls['A-221'] if w['id'].startswith('C-E1-S')][0]
    strips.append({'ref': 'MENU-BOARD-FRT', 'wall': ce1s['id'], 'lf': 23.46, 'width_ft': round(31 / 12, 3), 'material': 'frt_3_4',
                   'uso': 'substrate', 'label': '3/4" FRT PLYWOOD (menu boards 4/A-226A)', 'source': '4/A-226A', 'room': 'Cafe 103',
                   'img': '5_auditoria/img/F_menuboard_frt_blocking_4-A226A.png', 'op': 'continuous strip 31" high x full length of C-E1-S 23.46 LF (A-221) = 60.6 SF (estimator decision RFI-23)'})
    strips.append({'ref': 'RESTROOM-BACKING-FRT', 'wall': 'W2-06.5', 'lf': 13.33, 'width_ft': (16 / 12 if REV2 else 1.0), 'material': 'frt_3_4',
                   'uso': 'substrate', 'label': '3/4" FIRE RETARDANT PLYWOOD BACKING BOARD (TYP) AT ALL GRAB BARS', 'source': '21/A-201',
                   'room': "Men's / Women's Restroom", 'img': '5_auditoria/img/F_grabbar_backing_21-A201.png', 'op': ('10 pcs x 16" stud bay (1.333 ft, 21/A-201) x 16" high (estimator decision rev2) = 13.33 x 16/12 = 17.78 SF' if REV2 else '10 pcs (6 grab bars, 2 lavatories, 2 baby changing stations; 21/A-201, 26/A-201) x 16" stud bay (1.333 ft, 21/A-201) x 1.0 ft height ASSUMED (not printed - Review Item) = 13.33 SF')})

# ---------------------------------------------------------------- REV3 (11 Review Items cerrados, DECISIONES_ESTIMADOR.md)
misc = []
if REV3:
    import math as _m
    # RI 2: curved walls type 4 = face-average arc 25.68 LF each (RFI-18, estimator choice): 6 chords scaled
    for pref in ('W4-29', 'W4-30'):
        ch = sorted([w for w in walls['A-101'] if w['id'].startswith(pref)], key=lambda w: w['id'])
        tot = sum(w['length_ft'] for w in ch)
        for w in ch:
            k_ = 25.68 / tot
            b = w['band']; (x0, y0), (x1, y1) = b['p0'], b['p1']; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            b['p0'] = [round(cx + (x0 - cx) * k_, 2), round(cy + (y0 - cy) * k_, 2)]
            b['p1'] = [round(cx + (x1 - cx) * k_, 2), round(cy + (y1 - cy) * k_, 2)]
            for fk in ('faces_top', 'faces_bottom'):   # caras escaladas igual: largo = promedio de caras (R72.2)
                if b.get(fk):
                    b[fk] = [[round(cx + (px - cx) * k_, 2), round(cy + (py - cy) * k_, 2)] for px, py in b[fk]]
            b['arc_note'] = f'chord and faces scaled x {round(k_, 4)} to the face-average arc 25.68 LF per curved wall (estimator choice, RFI-18 / rev3 RI 2)'
            w['length_ft'] = round(w['length_ft'] * k_, 2)
            w['length_op'] += f' x {round(k_, 4)} (rev3 RI 2 / RFI-18: face-average arc 25.68 LF per curved wall, estimator choice)'
        d_ = round(25.68 - sum(w['length_ft'] for w in ch), 2)
        ch[-1]['length_ft'] = round(ch[-1]['length_ft'] + d_, 2)
    # RI 8: type I WD-1 to 15'-0" (6/A-226A) -> 5/8" FRT plywood floor to 15'-0"; GWB 15'-0" to deck (2/A-221 rule)
    for w in walls['A-221']:
        if w['tag'] == 'I':
            strips.append({'ref': f"{w['id']}-A-FRT", 'wall': w['id'], 'lf': w['length_ft'], 'width_ft': 15.0, 'material': 'frt_5_8',
                           'uso': 'substrate', 'label': '5/8" FRT PLYWOOD behind WD-1 (I/A-221)', 'source': 'I/A-221', 'room': 'Cafe 103',
                           'img': '../../ri08_wd1/2_A-221_bubble_6-A226A_looks_at_C-I.png',
                           'op': f"{w['length_ft']} LF x 15.0 ft (WD-1 top 15'-0\" A.F.F., 6/A-226A, bubble verified on 1/A-221; rev3 RI 8)"})
            for f in w.get('faces') or []:
                f['height_ft'] = 10.0
                f['height_source'] = "GWB from top of WD-1 15'-0\" (6/A-226A) to deck 25'-0\" = 10.0 ft (2/A-221 studs UP TO DECK; rev3 RI 8)"
    # RI 9: soffit faces (2/A-221, 6/A-226A east, 1/A-226A north, bubbles verified)
    for w in walls['A-221']:
        if w['id'] == 'SS-E':
            strips.append({'ref': 'SS-E-WD1-FRT', 'wall': 'SS-E', 'lf': w['length_ft'], 'width_ft': 4.0, 'material': 'frt_5_8', 'uso': 'substrate',
                           'label': '5/8" F.R.T. PLYWOOD behind WD-1 (2/A-221)', 'source': '6/A-226A', 'room': 'Cafe 103',
                           'img': '../../ri09_soffit/2_A-226A_6_soffit_east_face_WD-1_band.png',
                           'op': f"{w['length_ft']} LF x 4.0 ft (WD-1 11'-0\" to 15'-0\", printed 4'-0\" band, 6/A-226A; rev3 RI 9)"})
            for f in w.get('faces') or []:
                f['height_ft'] = 10.0; f['height_source'] = "GWB above WD-1 15'-0\" to deck 25'-0\" (2/A-221; rev3 RI 9)"
        if w['id'] == 'SS-N' and REV4:   # rev4 RFI-14 (estimator): soffit 11'-0" (A-121); WD-1 11'-0" -> 15'-0" as the east face
            strips.append({'ref': 'SS-N-WD1-FRT', 'wall': 'SS-N', 'lf': w['length_ft'], 'width_ft': 4.0, 'material': 'frt_5_8', 'uso': 'substrate',
                           'label': '5/8" F.R.T. PLYWOOD behind WD-1 (2/A-221)', 'source': '1/A-226A', 'room': 'Cafe 103',
                           'img': '../../ri09_soffit/4_A-221_bubble_1-A226A_looks_south_north_face.png',
                           'op': f"{w['length_ft']} LF x 4.0 ft (WD-1 11'-0\" to 15'-0\": soffit bottom 11'-0\" per A-121 governs, top 15'-0\" as east face 6/A-226A - estimator decision RFI-14, rev4)"})
            for f in w.get('faces') or []:
                f['height_ft'] = 10.0; f['height_source'] = "GWB above WD-1 15'-0\" to deck 25'-0\" (2/A-221; RFI-14 rev4)"
        elif w['id'] == 'SS-N':
            strips.append({'ref': 'SS-N-WD1-FRT', 'wall': 'SS-N', 'lf': w['length_ft'], 'width_ft': 2.0, 'material': 'frt_5_8', 'uso': 'substrate',
                           'label': '5/8" F.R.T. PLYWOOD behind WD-1 (2/A-221)', 'source': '1/A-226A', 'room': 'Cafe 103',
                           'img': '../../ri09_soffit/4_A-221_bubble_1-A226A_looks_south_north_face.png',
                           'op': f"{w['length_ft']} LF x 2.0 ft (WD-1 9'-0\" to 11'-0\" printed on 1/A-226A; sign panel top not printed = GWB, RFI-14; soffit 9'-0\" vs 11'-0\" conflict RFI-14; rev3 RI 9)"})
    # RI 10: Cafe Seating cloud = USG drywall suspension grid (4/A-121)
    for c_ in ceilings:
        if 'cloud' in c_['room']:
            c_['system'] = 'usg_grid'
            c_['detail'] = '4/A-121'
            c_['system_callout'] = {'detail': '4/A-121', 'on_plan': True, 'source': '1/A-121: section bubble 4/A-121 on the N edge of the Cafe Seating cloud'}
            c_['system_note'] = 'USG drywall suspension grid drawn on 4/A-121 (DGLW26 main tee, DGLW424 cross tee, DGCM27, DGWM24) - rev3 RI 10'
            c_['main_oc_in'] = {'value': 48, 'source': 'USG drywall suspension standard 48" O.C. (spacing not printed on 4/A-121) - note'}
            c_['cross_oc_in'] = {'value': 16, 'source': 'USG drywall suspension standard 16" O.C. (not printed on 4/A-121; 24" alternative = 84 pcs) - note'}
            c_['img'] = '../../ri10_11/1_A-121_4_USG_drywall_suspension.png'
    # RI 6: diagonal braces type 2 > 22 ft (RFI-04, estimator choice)
    misc.append({'ref': 'DIAG-BRACES-T2', 'familia': '3-5/8" stud (todos los gauges)', 'qty': 468.0, 'unit': 'LF', 'source': '8/A-410',
                 'label': '3-5/8" 20 ga stud diagonal brace @ 32" O.C. to structure (8/A-410 Top Track Detail "PROVIDE DIAGONAL BRACING AT 32\" O.C. TO STRUCTURE (TYP.)")',
                 'op': '117 braces (ROUNDUP(L x 12 / 32) + 1 per type 2 wall; 115 in rev2 + 2 from W2-05 +5.00 LF) x 4.0 ft at 45 deg (estimator choice; member / length not printed) = 468.0 LF (rev3 RI 6)'})
    # RI 11: vestibule GWB ceiling box (4/A-210, 6/A-210, 1/A-210)
    VB = '../../ri10_11/5_A-210_4_vestibule_section.png'
    for ref, fam_, q, src, op in (
        ('VEST-JOISTS', '8" joist', 88.0, '4/A-210', '8" JOISTS @ 16" O.C.: ROUNDUP(152/16)+1 = 11 x (7\'-8" + 2" + 2" = 8.0 ft) = 88.0 LF (1/A-210 12\'-8" N-S)'),
        ('VEST-BOX-BEAM-STUD', '8" stud (todos los gauges)', 25.33, '6/A-210', 'NESTED BEAM (2) 8" x 18 GA studs x 12.667 = 25.33 LF ("8" BOX BEAM BEARING ON CORNER POST", 4/A-210)'),
        ('VEST-BOX-BEAM-TRACK', 'track de ceilings / soffits', 25.33, '6/A-210', 'NESTED BEAM 6" x 16 GA top & bottom track (2) x 12.667 = 25.33 LF'),
        ('VEST-LEDGER', 'track de ceilings / soffits', 12.67, '4/A-210', '"8" LEDGER" 1 x 12.667 = 12.67 LF (east, at existing storefront)'),
        ('VEST-POSTS-STUD', '3-5/8" stud (todos los gauges)', 126.0, '6/A-210', 'NESTED COLUMN (2) 3-5/8" x 18 GA studs x 10.5 ft (B.O. CEILING 10\'-6") x 6 posts (1/A-210: 4 west + 2 east corners - confirm east 2) = 126.0 LF'),
        ('VEST-POSTS-TRACK', 'track de ceilings / soffits', 5.0, '6/A-210', 'NESTED COLUMN 3-5/8" x 16 GA top & bottom track 6 x 2 x 5" = 5.0 LF'),
        ('VEST-GWB', '5/8" gyp board Type X', 105.5, '4/A-210', '(1) LAYER OF 5/8" GYP. BD.: ceiling 7.667 x 12.667 = 97.1 SF + box beam faces 12.667 x 8" = 8.4 SF = 105.5 SF (Type X per rev2)')):
        misc.append({'ref': ref, 'familia': fam_, 'qty': q, 'unit': 'SF' if 'gyp' in fam_ else 'LF', 'source': src, 'op': op, 'img': VB})
    if REV4:   # RFI-16 (estimator): posts 3/4" FRT plywood, 4 faces, full height
        strips.append({'ref': 'VEST-POSTS-PLYWOOD', 'wall': 'VESTIBULE', 'lf': 10.0, 'width_ft': 10.5, 'material': 'frt_3_4', 'uso': 'substrate',
                       'label': '3/4" FRT plywood post sheathing (5/A-210 "SHEATHING AS REQUIRED"; estimator: plywood, 4 faces)', 'source': '5/A-210', 'room': 'Vestibule 100',
                       'img': VB, 'op': '6 posts x 4 faces x 5" (= 10.0 LF) x 10.5 ft = 105.0 SF (estimator decision RFI-16, rev4)'})
    strips.append({'ref': 'VEST-PLYWOOD', 'wall': 'VESTIBULE', 'lf': 12.667, 'width_ft': 8.417, 'material': 'frt_3_4', 'uso': 'substrate',
                   'label': 'ONE LAYER OF 3/4" PLYWOOD (FRT per A-410 "ALL PLYWOOD NEEDS TO BE FRT")', 'source': '4/A-210', 'room': 'Vestibule 100',
                   'img': VB, 'op': '12.667 x 8.417 (8\'-5" E-W, 1/A-210) = 106.6 SF (rev3 RI 11)'})

# ---------------------------------------------------------------- REV5 (auditoría final rev4, AUDITORIA_rev4/, regla v80j)
REV5 = os.environ.get('REV5') == '1'
AUD = '../../AUDITORIA_rev4/img/'
if REV5:
    WRX = 'A-410 Partition Notes 2 "W.R. GYPSUM BOARD IN ALL BATHROOMS AND JANITOR\'S CLOSET FOR WALL AND CEILING CONSTRUCTION"'
    # audit row 3: restroom GWB ceilings -> Type X W.R.
    for c_ in ceilings:
        if c_['room'] in ("Women's Restroom 109", "Men's Restroom 108"):
            c_['board'] = '5/8 type X WR'
            c_['board_source'] = WRX + ' (audit rev4 row 3, rev5); Type X per A-001A Div 09 A.2; ceiling tag 1/A-121'
            c_['img_wr'] = AUD + 'C4_A-410_partition_note_2_WR_ceilings.png'
    # audit row 9: Cafe Workroom 104 GWB faces -> Type X W.R. (A-410 "*" note KITCHEN, 2/A-410 RESTROOM/CAFE WALLS)
    for w in walls['A-221']:
        for f in w.get('faces') or []:
            if f['room'] == 'Cafe Workroom 104' and f['board'] == '5/8 type X':
                f['board'] = '5/8 type X WR'
                f['board_source'] = ('W.R. on the Cafe Workroom 104 faces (audit rev4 row 9, rev5): A-410 "*" note "PROVIDE 5/8" WATER RESISTANT '
                                     'GYP. BD AT JANITOR\'S CLOSET, DRINKING FOUNTAIN, KITCHEN AND ALL TOILET LOCATIONS", 2/A-410 "RESTROOM/CAFE '
                                     'WALLS ONLY: PROVIDE W.R. GYPSUM BOARD ON WET SIDE(S)"; G/A-221; Type X per A-001A')
    # audit row 4: janitor 11/A-200 "AREA OF 3/4" FIRE RESISTANT PLYWOOD BLOCKING (TYP)" - conservative upper bound
    strips.append({'ref': 'JANITOR-FRT-11-A200', 'wall': 'JANITOR 107', 'lf': 2.125, 'width_ft': 8.0, 'material': 'frt_3_4', 'uso': 'substrate',
                   'label': '3/4" FRT plywood area (sheet, SF) behind the janitor shelving / water heater shelf (11/A-200)', 'source': '11/A-200',
                   'room': 'Janitor Closet 107', 'img': AUD + 'C4_A-200_11_janitor_FR_plywood.png',
                   'op': '11/A-200 prints "AREA OF 3/4 FIRE RESISTANT PLYWOOD (TYP)" as a hatched area (a sheet, not a 2x member): width 2\'-1 1/2" (measured on 11/A-200 at 1/2"=1\'-0", not dimensioned) x 8\'-0" HOLD printed = 17.0 SF - conservative upper bound, extent RFI-33 (audit rev4 row 4)'})
    # audit row 6: Grab & Go header soffit 3/A-221 (6'-2" HOLD 1/A-221; GWB 7'-1" A-121; deck 25'-0")
    GGH = round(25.0 - (7 + 1 / 12), 3)
    walls['A-221'].append({
        'id': 'SS-GG', 'tag': '', 'element': 'soffit_side', 'sheet': 'A-221', 'page': 15,
        'location': 'Grab & Go header soffit over the open east side (6\'-2" HOLD)', 'source': '3/A-221', 'detail': '3/A-221',
        'detail_source': '3/A-221 "6" METAL STUDS @ 16" O.C."', 'stud_size': '6"', 'stud_source': '3/A-221', 'oc_in': 16, 'oc_source': '3/A-221',
        'height_ft': GGH, 'height_source': 'B.O. deck 25\'-0" (1/A-400B) - Grab & Go GWB 7\'-1" (1/A-121); studs to deck per 3/A-221',
        'height_status': 'DERIVADO', 'length_ft': 6.167, 'length_source': '1/A-221 printed 6\'-2" HOLD',
        'length_op': '6\'-2" HOLD printed on 1/A-221 = 6.167 ft (vector check (331.89 - 109.81) / 36 = 6.169)', 'tag_ids': [], 'status': 'DERIVADO',
        'img': AUD + 'C4_A-221_3_GrabGo_soffit_6-2_HOLD.png', 'length_status': 'DERIVADO',
        'faces_none_reason': 'east (Sales) face = 5/8" FRT plywood full height, carried as plywood (conservative: T.O. WD-1 not printed, "SEE ELEVATION" on 3/A-221 - RFI-34); west face is above the Grab & Go GWB ceiling (no finish); soffit bottom GWB carried in misc_items',
        'band': {'ori': 'V', 'c0': 1226.48, 'c1': 1248.2, 'lo': 109.81, 'hi': 331.89, 'sheet': 'A-221'},
        'thickness_measured_in': 7.24, 'thickness_check': 'faces 1226.48 / 1248.2 pt on A-221 = 7.24 in (7 1/4" printed)',
        'length_basis': 'printed HOLD dimension between the C-H3a and C-H1-N faces', 'detail_img': '4_canon/img/det/A221_soffit_sections_2_3.png'})
    for k_, (nid, end) in enumerate((('N-GG1', 'C-H3a south face'), ('N-GG2', 'C-H1-N north face'))):
        nodes.append({'id': nid, 'kind': 'free', 'wall': 'SS-GG', 'source': f'1/A-221 (soffit ends at the {end}; header over the opening, no wall connection)'})
    strips.append({'ref': 'SS-GG-FRT', 'wall': 'SS-GG', 'lf': 6.167, 'width_ft': GGH, 'material': 'frt_5_8', 'uso': 'substrate',
                   'label': '5/8" PRESSURE TREATED FRT PLYWOOD SUBSTRATE (3/A-221)', 'source': '3/A-221', 'room': 'Sales Area 101',
                   'img': AUD + 'C3_A-221_soffits_2_3.png',
                   'op': f'6.167 x {GGH} = full east face (conservative: T.O. WD-1 not printed - RFI-34; each 1 ft of GWB above WD-1 = 6.17 SF plywood -> GWB)'})
    misc.append({'ref': 'SS-GG-BOTTOM-GWB', 'familia': '5/8" gyp board Type X', 'qty': 3.73, 'unit': 'SF', 'source': '3/A-221',
                 'op': 'soffit bottom 5/8" GWB 6.167 x 7 1/4" (0.604 ft) = 3.73 SF (3/A-221)', 'img': AUD + 'C3_A-221_soffits_2_3.png'})
    # audit row 7: 8/A-410 "METAL STUD/TRACK FIRE STOP AT CEILING LINE, TYP." - full-height walls with a ceiling on one face
    FS = ('W2-04', 'W2-05', 'W2-06.1', 'W2-06.2', 'W2-06.3', 'W2-06.4', 'W2-06.5', 'W2-07', 'W2-08', 'W2-09', 'W5-01',
          'C-H1-N', 'C-H1-W', 'C-H2a', 'C-E2', 'C-H3a', 'C-H3b')
    wb_ = {w['id']: w for sh in walls for w in walls[sh]}
    # back-check rev5: same rule, ceiling extent only on walls whose ceiling covers part of the wall
    FSP = {'W2-03': (13.12, 'Corridor 110 face'), 'C-H2b': (1.95, 'Cafe Workroom 104 ACT'), 'C-E1-S': (19.0, 'Cafe 103 9\'-0" GWB band, 1/A-121')}
    FS = FS + tuple(FSP)
    for sz in ('3-5/8"', '6"'):
        xs = [(i if i not in FSP else f'{i} ({FSP[i][1]})', FSP[i][0] if i in FSP else wb_[i]['length_ft']) for i in FS if wb_[i]['stud_size'] == sz]
        q = round(sum(v for _, v in xs), 2)
        misc.append({'ref': f'FIRESTOP-TRACK-{sz[0]}', 'familia': 'track de ceilings / soffits', 'qty': q, 'unit': 'LF', 'source': '8/A-410',
                     'label': f'{sz} track fire stop at ceiling line (8/A-410 "METAL STUD/TRACK FIRE STOP AT CEILING LINE, TYP.")',
                     'op': ' + '.join(f'{i} {v}' for i, v in xs) + f' = {q} LF {sz} track (full-height walls with a ceiling on at least one face, 1/A-121; audit rev4 row 7)',
                     'img': AUD + 'C4_A-410_8_firestop_track_ceiling_line.png'})
    # audit row 5: water heater backing P-201 (RFI-32, conservative)
    for ref, q, op in (('WH-BACKING-STUD', 8.0, '2 pcs 3-5/8" stud backing x 4.0 ft = 8.0 LF (sizes not printed on P-201 - RFI-32, conservative)'),
                       ('WH-STEEL-BLOCKING', 2.67, 'steel blocking between studs at the anchor points 2 rows x 1.333 ft (16" bay) = 2.67 LF 3-5/8" stud pieces (RFI-32, conservative)')):
        misc.append({'ref': ref, 'familia': '3-5/8" stud (todos los gauges)', 'qty': q, 'unit': 'LF', 'source': 'P-201',
                     'label': 'P-201 WATER HEATER DETAIL: 2x4 metal stud backing + steel blocking between studs (Janitor 107, 11/A-200)',
                     'op': op, 'img': AUD + 'C4_P-201_water_heater_backing.png'})
    # audit row 1: type I end faces "I SIM." (1/A-221) at C-H3a and C-H1-N - finish only, framing inside the host wall
    descartes[:] = [d_ for d_ in descartes if d_['id'] not in ('PT0048', 'PT0049')]
    for wid, host, tid, (lo, hi) in (('C-I-E1', 'C-H3a', 'PT0048', (88.09, 109.81)), ('C-I-E2', 'C-H1-N', 'PT0049', (331.89, 353.61))):
        L = round((hi - lo) / 36.0, 3)
        walls['A-221'].append({
            'id': wid, 'tag': 'I', 'element': 'pier', 'sheet': 'A-221', 'page': 15,
            'location': f'Type I end face (I SIM.) at the east end of {host}, Sales side', 'source': 'I/A-221', 'detail': 'I/A-221',
            'detail_source': 'I/A-221', 'stud_size': '6"', 'stud_source': 'I/A-221', 'oc_in': 16, 'oc_source': 'I/A-221',
            'height_ft': 25.0, 'height_source': 'B.O. DECK ABOVE EL. 25\'-0" V.I.F. - 1/A-400A, 1/A-400B', 'height_status': 'CONFIRMADO',
            'length_ft': L, 'length_source': '1/A-221 printed 7 1/4" wall thickness',
            'length_op': f'end face = wall thickness 7 1/4" printed on 1/A-221 (vector ({hi} - {lo}) / 36 = {L})', 'tag_ids': [tid],
            'status': 'DERIVADO', 'length_status': 'DERIVADO', 'img': AUD + 'C1_A-221_I_SIM_tags_no_row.png',
            'parts': [{'stud_size': '6"', 'studs_drawn': {'value': 0, 'source': f'framing of the end face is the end stud of {host} (already counted in {host}); I/A-221 adds finish only'}}],
            'type_lf_basis': 'end face width (finish only)',
            'bottom_track': False, 'top_track': False, 'track_source': f'I/A-221 (end face of {host} - its bottom / top track is the track of {host} on 1/A-221)',
            'bracing_rows': 0, 'bracing_rows_source': f'I/A-221 (end face of {host} - bracing belongs to {host} per 5/A-410)',
            'jamb_strips_none_reason': 'I/A-221 end face: no storefront jamb; the FRT plywood is the WD-1 substrate carried as plywood_strips (1/A-221, I/A-221)',
            'faces': [{'side': 'A', 'room': 'Sales Area 101', 'board': '5/8 type X', 'layers': 1, 'length_ft': L, 'length_source': '1/A-221 7 1/4" wall thickness (end face)', 'height_ft': 10.0,
                       'height_source': 'GWB from top of WD-1 15\'-0" (6/A-226A) to deck 25\'-0" = 10.0 ft (I/A-221, 2/A-221)',
                       'board_source': '5/8" Type X on all new walls (estimator decision RFI-27): A-001A Div 09 A.2'}],
            'band': {'ori': 'V', 'c0': 1246.2, 'c1': 1250.2, 'lo': lo, 'hi': hi, 'sheet': 'A-221'},
            'thickness_measured_in': 1.33, 'thickness_check': 'finish-only element on the end face (band drawn 4 pt for the markup)',
            'detail_img': '4_canon/img/det/A221_sections_H_I.png'})
        strips.append({'ref': f'{wid}-A-FRT', 'wall': wid, 'lf': L, 'width_ft': 15.0, 'material': 'frt_5_8', 'uso': 'substrate',
                       'label': '5/8" FRT PLYWOOD behind WD-1 (I/A-221)', 'source': 'I/A-221', 'room': 'Sales Area 101',
                       'img': AUD + 'C1_A-221_I_SIM_tags_no_row.png',
                       'op': f"{L} LF x 15.0 ft (WD-1 top 15'-0\" A.F.F., 6/A-226A; audit rev4 row 1)"})

# ---------------------------------------------------------------- REV6 (investigación W.R. / FRT, investigacion_WR_FRT/)
REV6 = os.environ.get('REV6') == '1'
if REV6:
    # G/A-221 draws ONE layer on the Cafe Work Room side of H1 / H2a: 5/8" FRT plywood (crosshatch; FRP-1 over it per A-510);
    # the gypsum board layer is on the Sales / Office side only. The Work Room GWB faces (rev0-rev5) are removed; the FRT strips stay.
    for w in walls['A-221']:
        if w['id'] in ('C-H1-N', 'C-H1-W', 'C-H2a'):
            w['faces'] = [f for f in w.get('faces') or [] if f['room'] != 'Cafe Workroom 104']
            w['faces_note'] = ('Cafe Work Room 104 side = 5/8" FRT plywood only (G/A-221 graphics: single crosshatched layer; '
                               'A-510 104 walls FRP-1) - carried in plywood_strips; no gypsum board on that face (rev6)')
    # RFI-37 resolved from the plan (rev6): Sales / Cafe faces = gypsum board only, no FRT plywood behind it:
    # G/A-221 Sales side one layer "5/8" GYPSUM BOARD"; C-H1-N Sales face = Sales Area 101 "PAINTED GYP. BD." (A-510);
    # C-H2a Cafe face = "PT-3" painted wall around door 3 (1/A-225, 5/A-226A); the WD-1 strip left of the door is the type I return (C-I-P.1)
    strips[:] = [x for x in strips if x['ref'] not in ('C-H1-N-A-FRT', 'C-H2a-B-FRT')]

# ---------------------------------------------------------------- REV7 (Paso 12 sobre rev6: PASO12_rev6/, regla v80j)
REV7 = os.environ.get('REV7') == '1'
if REV7:
    import math as _m7
    P12 = '../../PASO12_rev6/img/'
    wb7 = {w['id']: w for sh in walls for w in walls[sh]}
    TX = '5/8" Type X on all new walls (estimator decision RFI-27): A-001A Div 09 A.2'
    # C-01: T.O. WD-1 at the Grab & Go header = 15'-0" (5/A-226A 11'-0" + 4'-0" WD-1; 6/A-226A 15'-0"): GWB over the plywood to deck
    ss = wb7['SS-GG']; ss.pop('faces_none_reason', None)
    DETAILS['3/A-221'] = {'layers_per_face': 1, 'source': '3/A-221', 'layers_source': '3/A-221', 'img': P12 + 'A-221_3-GrabGo-soffit.png',
                          'title': 'Soffit Section - Grab & Go', 'notes': '6" metal studs @ 16" O.C.; 5/8" pressure treated FRT plywood substrate full face; 5/8" GWB above T.O. WD-1 (15\'-0", 5/A-226A, 6/A-226A); GWB at the soffit bottom', **SEAL}
    ss['faces'] = [{'side': 'A', 'room': 'Sales Area 101', 'board': '5/8 type X', 'layers': 1, 'height_ft': 10.0,
                    'height_source': "GWB from T.O. WD-1 15'-0\" (5/A-226A 11'-0\" + 4'-0\" WD-1; 6/A-226A 15'-0\") to deck 25'-0\" over the full-height FRT plywood (3/A-221) - rev7 plan check C-01",
                    'board_source': TX}]
    # C-04: C-E1-S exposed Cafe face = 19'-0" HOLD (1/A-221)
    for f in wb7['C-E1-S']['faces']:
        f['length_ft'] = 19.0
        f['length_source'] = '1/A-221 printed 19\'-0" HOLD (finished face to finished face: pier to SE box) - rev7 plan check C-04'
    wb7['C-E1-S']['faces'].append(dict(wb7['C-E1-S']['faces'][0], room='concealed: behind the Workroom door pier and inside the SE box (no cement board)',
                                       length_ft=round(wb7['C-E1-S']['length_ft'] - 19.0, 2), height_ft=0.0,
                                       length_source='1/A-221: wall length 23.46 - 19\'-0" HOLD exposed face',
                                       height_source='0 ft: face concealed by the pier (C-E1-P) and the SE box (C-E1-B / C-F / C-I) - 1/A-221'))
    # C-09: door 4 is in W2-04 (A-101 / A-500), not in W2-05 - labels only (the opening was already in W2-04)
    wb7['W2-05']['location'] = "Corridor 110 / Women's 109"
    if 'door 4' not in wb7['W2-04']['location']:
        wb7['W2-04']['location'] += ' (door 4 inside wall)'
    # C-06: vestibule box members are 7/A-210 (nested stud details) and 8/A-210 (nested stud column & beam); 6/A-210 = glazing base
    for m in misc:
        if m.get('source') == '6/A-210':
            m['source'] = '8/A-210' if 'BEAM' in m['ref'] else '7/A-210'
            m['op'] = m['op'] + ' (citation corrected: 7/A-210 nested stud details, 8/A-210 nested stud column & beam; 6/A-210 is the glazing base detail - rev7 plan check C-06)'
    # C-03: 22/A-201 "1'-2" CEMENT BOARD BASE" (5/8" cement board, W.R. above) on the restroom faces of new walls
    RR = ("Women's Restroom 109", "Men's Restroom 108")
    rr = [(w['id'], f.get('length_ft') or w['length_ft']) for w in walls['A-101'] for f in w.get('faces') or [] if f['room'] in RR]
    lrr = round(sum(v for _, v in rr), 2); drr = 3.33 + 3.33   # doors 9 (Women's) and 8 (Men's) open in these faces
    cbx = round((lrr - drr) * 14 / 12, 2)
    opc = ' + '.join(f'{i} {v}' for i, v in rr) + f' = {lrr} LF - doors 8, 9 ({drr}) = {round(lrr - drr, 2)} LF x 1\'-2" = {cbx} SF'
    misc.append({'ref': 'RESTROOM-BASE-CEMENT', 'familia': 'cement board', 'qty': cbx, 'unit': 'SF', 'source': '22/A-201',
                 'op': '5/8" CEMENT BOARD BASE 1\'-2" (22/A-201; A-001A Div 09 J.2): ' + opc + ' - rev7 plan check C-03', 'img': P12 + 'A-201_22-tile-base.png'})
    misc.append({'ref': 'RESTROOM-BASE-WR-DEDUCT', 'familia': '5/8" gyp Type X W.R.', 'qty': -cbx, 'unit': 'SF', 'source': '22/A-201',
                 'op': f'W.R. board replaced by the 1\'-2" cement board base on the same faces (22/A-201): - {cbx} SF', 'img': P12 + 'A-201_22-tile-base.png'})
    # GAP: gauges per type (A-410 Metal Stud Schedule; Partition Notes 5 "ALL METAL STUDS TO BE MIN. 20 GAUGE"; schedule note 2 track = stud)
    SCH = 'A-410 Metal Stud Schedule (16" O.C. max unsupported height)'
    for w in wb7.values():
        sz, H, t = w.get('stud_size'), float(w.get('height_ft') or 0), str(w.get('tag'))
        if sz == '3-5/8"' and (t == '2' or H > 22.0):
            w['gauge'] = '14 ga SJ'
            w['gauge_source'] = SCH + ': 3-5/8" 14 SJ 22\'-0" is the heaviest; walls to 25\'-0" carried 14 ga SJ + diagonal bracing @ 32" (3/A-410) - estimator precedent RFI-04'
        elif sz == '6"' and H > 17.9:
            w['gauge'] = '20 ga SJ'; w['gauge_source'] = SCH + ': 6" 20 SJ 26\'-8" >= wall height'
        else:
            w['gauge'] = '20 ga'; w['gauge_source'] = SCH + ' + Partition Notes 5 "ALL METAL STUDS TO BE MIN. 20 GAUGE"'
    # Cafe 3-5/8" walls to 25'-0" (> 22'-0"): precedent RFI-04 = diagonal braces @ 32" O.C. x 4 ft
    cb = [(i, wb7[i]['length_ft']) for i in ('C-H2a', 'C-H2b', 'C-F')]
    nb = sum(_m7.ceil(L * 12 / 32 - 1e-9) + 1 for _, L in cb)
    misc.append({'ref': 'DIAG-BRACES-CAFE', 'familia': '3-5/8" stud (todos los gauges)', 'qty': nb * 4.0, 'unit': 'LF', 'source': '3/A-410',
                 'label': 'Diagonal braces @ 32" O.C. to structure (3/A-410), Cafe 3-5/8" walls to deck (> 22\'-0")',
                 'op': ' + '.join(f'{i} (ROUNDUP({L} x 12 / 32) + 1 = {_m7.ceil(L * 12 / 32 - 1e-9) + 1})' for i, L in cb) + f' = {nb} braces x 4.0 ft = {nb * 4.0} LF (estimator precedent RFI-04)',
                 'img': P12 + 'A-410_metal-stud-schedule.png'})
    # GAP: clip angles 5/A-410 at every C.R. channel / stud crossing ((4) Tek screws each)
    cl, clop = 0, []
    for w in wb7.values():
        if w.get('element') not in ('wall', 'soffit_side', 'column_wrap') or w.get('bracing_rows') == 0:
            continue
        rows = max(0, _m7.ceil(round(float(w['height_ft']) * 12 / 48, 6)) - 1)
        if not rows:
            continue
        st = 12 if w.get('element') == 'column_wrap' else _m7.ceil(float(w['length_ft']) * 12 / 16 - 1e-9) + 1
        cl += rows * st; clop.append(f"{w['id']} {rows}x{st}")
    misc.append({'ref': 'CLIP-ANGLES-5-A410', 'familia': 'clip angle (bracing / nested connections)', 'qty': cl, 'unit': 'PCS', 'source': '5/A-410',
                 'op': '2" x 2" 16 GA. CLIP ANGLE at each stud per bracing row, (4) TEK SCREWS (5/A-410): rows x studs = ' + ' + '.join(clop) + f' = {cl} pcs',
                 'img': P12 + 'A-410_5-lateral-bracing-clip-angle.png'})
    misc.append({'ref': 'CLIP-ANGLES-7-A210', 'familia': 'clip angle (bracing / nested connections)', 'qty': 4, 'unit': 'PCS', 'source': '7/A-210',
                 'op': '3"x3"x16 GA. CLIP ANGLES at the nested header to jamb connection (7/A-210): 2 header ends x 2 (front / back) = 4 pcs (conservative; count not printed - RFI-51)',
                 'img': P12 + 'A-210_7-clip-angles.png'})
    # GAP: full-height walls (deflection head to structure): nested inner runner (3/A-410) + X-EDNI 8.C + cross members 8/A-410
    FH = [w for w in wb7.values() if w.get('element') in ('wall', 'soffit_side') and float(w['height_ft']) >= 13.5
          and w.get('top_track') is not False]
    lfh = round(sum(float(w['length_ft']) for w in FH), 2)
    misc.append({'ref': 'NESTED-RUNNER-3-A410', 'familia': 'nested inner runner (deflection head)', 'qty': lfh, 'unit': 'LF', 'source': '3/A-410',
                 'op': '3/A-410 "METAL RUNNER AT STUDS - SECURE GWB TO METAL RUNNER" + "DO NOT SECURE METAL STUDS OR GWB TO DEEP LEG TRACK": inner runner = length of every wall / soffit side to deck = ' + ' + '.join(f"{w['id']} {w['length_ft']}" for w in FH) + f' = {lfh} LF (RFI-40 confirms the reading)',
                 'img': P12 + 'A-410_3-top-track-detail.png'})
    nx = _m7.ceil(lfh * 2 / (16 / 12))
    misc.append({'ref': 'X-EDNI-8C', 'familia': 'X-EDNI fasteners, top track to structure', 'qty': nx, 'unit': 'PCS', 'source': 'A-410',
                 'op': f'A-410 Partition Notes (typical fastener) 8.C "0.145\\" DIA. HILTI X-EDNI ... 2 ROWS AT 16\\" O.C. FOR CONTINUOUS APPLICATIONS SUCH AS TRACKS": {lfh} LF deep leg track to structure x 2 rows / 1.333 ft = {nx} pcs',
                 'img': P12 + 'A-410_partition-note-8C.png'})
    PAR = [w for w in FH if w['band']['ori'] == 'V']   # joists N-S (RFI-15 closed): N-S walls run parallel to the joists
    cmo, cm = [], {}
    for w in PAR:
        n = _m7.ceil(float(w['length_ft']) / 2.0 - 1e-9) + 1
        cm[w['stud_size']] = cm.get(w['stud_size'], 0) + n * 5.0
        cmo.append(f"{w['id']} ROUNDUP({w['length_ft']}/2)+1 = {n}")
    for sz, q in cm.items():
        misc.append({'ref': f'CROSS-MEMBERS-8-A410-{sz[0]}', 'familia': '6" stud (todos los gauges)' if sz == '6"' else '3-5/8" stud (todos los gauges)',
                     'qty': round(q, 2), 'unit': 'LF', 'source': 'TYPCONN/A-410',
                     'op': f'TYPCONN/A-410 Typ. Connection Detail - PARALLEL TO STRUCTURE: metal stud per schedule spanning joist to joist, (1) P.A.F. each end, track attached @ 24" O.C.: ' + '; '.join(c for c in cmo if wb7[c.split()[0]]['stud_size'] == sz) + f' members x 5.0 ft (joist spacing not printed, assumed - RFI-41) = {round(q, 2)} LF {sz} 20 ga (A-410 schedule, min. 20 ga)',
                     'img': P12 + 'A-410_8-connection-detail.png'})
    # GAP: 2/A-221 FRT plywood continues above T.O. WD-1 behind the GWB (SS-N, SS-E): 11'-0" to deck = 14 ft; cross bracing AS REQ'D
    for st_ in strips:
        if st_['ref'] in ('SS-N-WD1-FRT', 'SS-E-WD1-FRT'):
            st_['width_ft'] = 14.0
            st_['op'] = f"{st_['lf']} LF x 14.0 ft: 2/A-221 draws the 5/8\" F.R.T. plywood continuous from the soffit bottom 11'-0\" to deck 25'-0\" (WD-1 band 11'-0\" to 15'-0\", 5/8\" GWB over the plywood above) - rev7 plan check"
    nbr = _m7.ceil((wb7['SS-N']['length_ft'] + wb7['SS-E']['length_ft']) / 4.0)
    misc.append({'ref': 'SOFFIT-CROSS-BRACING-2-A221', 'familia': '3-5/8" stud (todos los gauges)', 'qty': nbr * 2 * 5.0, 'unit': 'LF', 'source': '2/A-221',
                 'op': f'2/A-221 "CROSS BRACING AS REQ\'D": (SS-N {wb7["SS-N"]["length_ft"]} + SS-E {wb7["SS-E"]["length_ft"]}) / 4 ft = {nbr} pairs x 2 x 5.0 ft = {nbr * 10.0} LF 3-5/8" stud (conservative; member / spacing not printed - RFI-42)',
                 'img': P12 + 'A-221_2-cross-bracing.png'})
    # GAP: E2 Workroom face FRT to ACT-1 + 6" (same rule as the H1 / H2 Workroom faces, estimator precedent RI 7, A-410 Partition Notes 3)
    for st_ in strips:
        if st_['ref'] == 'C-E2-A-FRT':
            st_['width_ft'] = 10.5
            st_['op'] = f"{st_['lf']} LF x 10.5 ft (Cafe Workroom ACT-1 10'-0\" (1/A-121) + 6\" - A-410 Partition Notes 3; same rule as the H1 / H2 Workroom faces, estimator precedent RI 7) - rev7 plan check"
    # GAP: H3b Sales face above the 8'-0" plywood (H/A-221 "H3b = PLYWOOD UP TO 8'-0""): GWB to deck (A-410 Partition Notes 2 full height)
    wb7['C-H3b']['faces'].append({'side': 'A', 'room': 'Sales Area 101', 'board': '5/8 type X', 'layers': 1, 'height_ft': 17.0,
                                  'height_source': 'GWB 8\'-0" (top of plywood, H/A-221) to deck 25\'-0" = 17.0 ft - A-410 Partition Notes 2 "GYP. BOARD ON BOTH SIDES FOR THE FULL HEIGHT OF THE STUDS" - rev7 plan check',
                                  'board_source': TX})
    # GAP: F/A-221 "TO BOTTOM OF NESTED STUD BRACING" - nested bracing member (conservative 2 runners)
    misc.append({'ref': 'F-NESTED-BRACING', 'familia': '3-5/8" stud (todos los gauges)', 'qty': round(2 * wb7['C-F']['length_ft'], 2), 'unit': 'LF', 'source': 'F/A-221',
                 'op': f'F/A-221 "TO BOTTOM OF NESTED STUD BRACING": 2 nested members x {wb7["C-F"]["length_ft"]} LF = {round(2 * wb7["C-F"]["length_ft"], 2)} LF (conservative; member not drawn - RFI-46)',
                 'img': P12 + 'A-221_F-nested-stud-bracing.png'})
    # GAP: vestibule GWB bands above B.O. ceiling 10'-6" to 11'-3 1/2" V.I.F. (2/A-210 front +1.63 SF, 3/A-210 sides +13.33 SF)
    misc.append({'ref': 'VEST-GWB-BANDS', 'familia': '5/8" gyp board Type X', 'qty': 14.96, 'unit': 'SF', 'source': '2/A-210',
                 'op': '2/A-210: (11\'-3 1/2" - 10\'-6") 0.792 x 12.67 = 10.03 SF - 8.4 carried = + 1.63 SF; 3/A-210: 2 sides x 8.42 ft x 0.792 = 13.33 SF; total 14.96 SF (V.I.F.)',
                 'img': P12 + 'A-210_3-side-elev-fascia.png'})
    # GAP: A-510 Finish Notes 8 "ALL OUTSIDE CORNERS SHALL BE FINISHED WITH METAL CORNER BEADS": soffit bottom edges
    sfe = [(i, wb7[i]['length_ft']) for i in ('SS-N', 'SS-E', 'SS-IN-N', 'SS-IN-E', 'SS-GG')]
    misc.append({'ref': 'CORNER-BEAD-SOFFITS', 'familia': 'metal trim (corner bead, casing, shadow molding)', 'qty': round(sum(v for _, v in sfe), 2), 'unit': 'LF', 'source': 'A-510',
                 'op': 'A-510 Finish Notes 8 metal corner bead at the soffit bottom outside edges (2/A-221, 3/A-221): ' + ' + '.join(f'{i} {v}' for i, v in sfe) + f' = {round(sum(v for _, v in sfe), 2)} LF',
                 'img': P12 + 'A-510_finish-note-8.png'})
    # GAP: Grab & Go GWB ceiling 7'-1" (1/A-121)
    ceilings.append({'room': 'Grab & Go', 'system': 'furring', 'area_sf': round(4.08 * 6.167, 2), 'perimeter_ft': round(2 * (4.08 + 6.167), 2),
                     'ns_ft': 6.167, 'ew_ft': 4.08, 'height_ft': 7.083, 'source': 'A-121',
                     'area_op': "[DERIVED] 4.08 (C-H3a) x 6.167 (6'-2\" HOLD, 1/A-221) = 25.16 SF; tag \"GRAB & GO GWB 7'-1\" PT-7\" (1/A-121) - rev7 plan check",
                     'img': P12 + 'A-121_grab-and-go-gwb-7-1.png',
                     'hanger_drop_ft': {'value': 17.917, 'source': "B.O. deck 25'-0\" (1/A-400B) - ceiling 7'-1\" (A-121) - RFI-03"},
                     'detail': '5/A-121', 'board': '5/8 type X', 'board_source': '5/8" Type X (estimator decision rev2): 4/A-121, 5/A-121, A-001A Div 09 A.2'})
    # GAP: recessed FE cabinets in new walls - 4/A-101 "F.R.T. WOOD STUD HEADER ABOVE AND BASE BELOW CABINET" (C11 x 4 in new walls)
    blocking.append({'ref': 'BLK-FE-CABINETS', 'lf': 16.0, 'material': 'FRT', 'label': 'F.R.T. WOOD STUD HEADER ABOVE AND BASE BELOW CABINET (4/A-101)', 'source': '4/A-101',
                     'op': '4 recessed cabinets in new walls (C11 on A-101: W2-01, W2-03 x 2, Cafe Workroom) x (header 2.0 + base 2.0 ft) = 16.0 LF FRT 2x (cabinet width not printed - RFI-39)',
                     'img': P12 + 'A-101_4-fire-extinguisher-detail.png'})
    # GAP: 2/A-500 cased opening wood blocking across the stud return
    blocking.append({'ref': 'BLK-CASED-OPENING', 'lf': 17.0, 'material': 'wood', 'label': 'WOOD BLOCKING at cased opening (2/A-500)', 'source': '2/A-500',
                     'op': '1 cased opening x (2 jambs x 7.0 + head 3.0) = 17.0 LF (conservative; count / location per plan not confirmed - RFI-49)',
                     'img': P12 + 'A-500_2-cased-opening-wood-blocking.png'})
    # GAP: 2/E-103 server room "4'x8' FRT PLYWOOD SHEET AND POWER BY GC" (E-301 terminal board)
    strips.append({'ref': 'SERVER-ROOM-BACKBOARD', 'wall': 'SERVER ROOM', 'lf': 4.0, 'width_ft': 8.0, 'material': 'frt_3_4', 'uso': 'substrate',
                   'label': '4\'x8\' FRT PLYWOOD SHEET BY GC (2/E-103)', 'source': '2/E-103', 'room': 'Server room',
                   'img': P12 + 'E-103_2_server-room-FRT-plywood-by-GC.png', 'op': '1 sheet 4 x 8 = 32.0 SF 3/4" FRT plywood (2/E-103 "BY GC"; E-301 fire-rated plywood terminal board) - RFI-50 confirms trade'})
    # GAP: 5/A-121 "PROVIDE ADDITIONAL WIRE SUPPORT AT ALL LIGHT FIXTURES" (GWB ceilings): D6 Women's 4 + Men's 4 + cloud 21
    misc.append({'ref': 'HANGERS-FIXTURES-5-A121', 'familia': 'hanger wire', 'qty': 401.0, 'unit': 'LF', 'source': '5/A-121',
                 'op': '5/A-121 additional wire at all light fixtures: Women\'s 4 + Men\'s 4 (D6, 1/A-121) x drop 16.0 = 128.0 + Cafe Seating cloud 21 (7 x 3, 1/A-121) x drop 13.0 = 273.0; 29 hangers = 401.0 LF',
                 'img': P12 + 'A-121_detail-5-tie-wire-fixture-support.png'})
    # GAP: 5/A-121 seismic splay wires (A-420 referenced by ceiling note 1 is not in the set) - conservative, RFI-38
    G = [("Women's", 1, 16.0), ("Men's", 1, 16.0), ("Cafe 11'-6\" band", 1, 13.5), ("Cafe 9'-0\" band", 1, 16.0), ('Cafe cloud', 4, 13.0), ('Grab & Go', 1, 17.917)]
    wl = round(sum(n * 4 * d * 1.414 for _, n, d in G), 2); sl = round(sum(n * d for _, n, d in G), 2)
    gop = '; '.join(f'{r} {n} x drop {d}' for r, n, d in G)
    misc.append({'ref': 'SPLAY-WIRES-5-A121', 'familia': 'hanger wire', 'qty': wl, 'unit': 'LF', 'source': '5/A-121',
                 'op': f'5/A-121 splay wires 4 per brace group @ 12\'-0" O.C. each way, at 45 deg: groups {gop} -> sum(groups x 4 x drop x 1.414) = {wl} LF (conservative; A-420 not in the set - RFI-38)',
                 'img': P12 + 'A-121_detail-5-seismic-splay-wires.png'})
    misc.append({'ref': 'SEISMIC-STRUTS-5-A121', 'familia': '1-5/8" stud', 'qty': sl, 'unit': 'LF', 'source': '5/A-121',
                 'op': f'5/A-121 "1 5/8\\" x 16 GA. METAL JOIST" compression post per brace group: groups {gop} -> sum(groups x drop) = {sl} LF (conservative - RFI-38)',
                 'img': P12 + 'A-121_detail-5-seismic-splay-wires.png'})
    FRP_R7 = ('FRP-1 (A-510): Cafe Work Room 104 FRP-1 full height to the 10\'-0" ceiling (1-4/A-226B); Janitor 107 FRP-1 to 96" A.F.F. (A-131) / 8\'-0" (9-12/A-200); '
              'Cafe 103 below countertop. Installer not defined (A-002) - not carried, RFI-13 with delta (1,030.64 SF) - PVC trim with it.')
    # FIRESTOP track per wall (biblioteca BE-40): one misc per wall instead of one per size
    fs = [m for m in misc if m['ref'].startswith('FIRESTOP-TRACK')]
    misc[:] = [m for m in misc if not m['ref'].startswith('FIRESTOP-TRACK')]
    for m in fs:
        for part in m['op'].split(' = ')[0].split(' + '):
            wid, val = part.rsplit(' ', 1)
            misc.append({'ref': 'FIRESTOP-' + wid.split(' (')[0], 'familia': 'track de ceilings / soffits', 'qty': float(val), 'unit': 'LF', 'source': '3/A-410',
                         'op': f'3/A-410 "METAL STUD/TRACK FIRE STOP AT CEILING LINE, TYP.": {m["ref"][-1] == "3" and "3-5/8" or "6"}" track along {wid} = {val} LF (RFI-35)',
                         'img': m.get('img')})

# ---------------------------------------------------------------- REV8 (Paso 12 2.ª pasada sobre rev7: PASO12_rev7/)
REV8 = os.environ.get('REV8') == '1'
if REV8:
    P7I = '../../PASO12_rev7/img/'
    # C7-01: 5/A-121 "1 5/8" x 16 GA. METAL JOIST FRAMING @ 48" O.C." is the horizontal carrying member, not a post;
    # the vertical member at each brace point is "16 GA. WIRE 12'-0" O.C. EACH WAY"
    for m in list(misc):
        if m['ref'] == 'SEISMIC-STRUTS-5-A121':
            misc.remove(m)
            misc.append({'ref': 'SEISMIC-VERTICAL-WIRE-5-A121', 'familia': '16 ga wire (seismic brace points)', 'qty': m['qty'], 'unit': 'LF', 'source': '5/A-121',
                         'op': m['op'].replace('"1 5/8\\" x 16 GA. METAL JOIST" compression post per brace group', '"16 GA. WIRE 12\'-0\\" O.C. EACH WAY AND WITHIN 6\'-0\\" OF EACH WALL" vertical wire at each brace point')
                               + ' - rev7 plan check C7-01: the 1-5/8" x 16 ga metal joist framing @ 48" O.C. on 5/A-121 is the horizontal carrying member (no post drawn)',
                         'img': P7I + 'A-121_5_1-5-8-metal-joist-framing-48OC-horizontal.png'})
    # C7-03: 8/A-410 (specific) governs over note 8.C: relief channel to steel with #8 pan head screws @ 24" O.C. + 6" from ends;
    # cross members (1) 3/16" x 3/8" P.A.F. at each end
    for m in list(misc):
        if m['ref'] == 'X-EDNI-8C':
            misc.remove(m)
    FH8 = [w for w in wb7.values() if w.get('element') in ('wall', 'soffit_side') and float(w['height_ft']) >= 13.5]
    n8 = sum(_m7.ceil(float(w['length_ft']) / 2.0 - 1e-9) + 1 for w in FH8)
    misc.append({'ref': 'PAN-HEAD-8-A410', 'familia': '#8 pan head screws, relief channel to structure', 'qty': n8, 'unit': 'PCS', 'source': 'TYPCONN/A-410',
                 'op': 'TYPCONN/A-410 "CONTINUOUS 20 GA. X 2" MIN DEEP RELIEF CHANNEL - ANCHOR TO STEEL PLATE WITH #8 PAN HEAD SELF TAPPING SCREWS AT 24" O.C. AND 6" FROM ENDS": sum(ROUNDUP(L / 2) + 1) over '
                       + f'{len(FH8)} runs to structure ({round(sum(float(w["length_ft"]) for w in FH8), 2)} LF) = {n8} pcs (rev7 plan check C7-03; note 8.C X-EDNI = alternative in RFI-51)',
                 'img': P7I + 'A-410_8_typ-connection-8-screws-24OC-PAF.png'})
    ncm = sum(_m7.ceil(float(w['length_ft']) / 2.0 - 1e-9) + 1 for w in FH8 if w['band']['ori'] == 'V')
    misc.append({'ref': 'PAF-CROSS-MEMBERS-8-A410', 'familia': 'P.A.F. at cross members', 'qty': 2 * ncm, 'unit': 'PCS', 'source': 'TYPCONN/A-410',
                 'op': f'TYPCONN/A-410 PARALLEL TO STRUCTURE "METAL STUD PER SCHEDULE W/ (1) 3/16" 3/8" P.A.F. AT EACH END": {ncm} cross members x 2 = {2 * ncm} pcs (RFI-41)',
                 'img': P7I + 'A-410_8_typ-connection-8-screws-24OC-PAF.png'})
    # C7-06: one thickness per row - 22/A-201 base = 5/8" cement board (its own family)
    for m in misc:
        if m['ref'] == 'RESTROOM-BASE-CEMENT':
            m['familia'] = '5/8" cement board'
    # BE-16: 5/A-410 "(4) TEK SCREWS" per clip angle; 7/A-210 "(4) #10-16 SCREWS" per clip
    ncl5 = [m for m in misc if m['ref'] == 'CLIP-ANGLES-5-A410'][0]['qty']
    # 7/A-210 "RUNNER TRACK ATTACHED TO HEADER SUING (2) TEK SCREWS AT 16" O.C" (top + bottom runner) on the 12.667 ft nested header (6/A-210)
    import math as _m7
    # 7/A-210 "RUNNER TRACK ATTACHED TO HEADER SUING (2) TEK SCREWS AT 16" O.C" (top + bottom runner), header 12'-8" (1/A-210 front chain 152")
    nrt = 2 * 2 * (_m7.ceil(12.667 / (16 / 12)) + 1)
    # 8/A-210 "(8) #10-16 TEKS 16"O.C., TYP." on the nested beam (12.667 ft) and the 6 nested columns (10.5 ft)
    nnb = (_m7.ceil(12.667 / (16 / 12)) + 1) * 8
    nnc = 6 * (_m7.ceil(10.5 / (16 / 12)) + 1) * 8
    # 7/A-210 "HEAD ATTACHMENT SEE DETAIL" clip with "#10-16 TEK SCREWS (TYP.)": 8 drawn per clip, one clip per header end (count not printed - RFI-51)
    nha = 2 * 8
    tot = ncl5 * 4 + 16 + nrt + nnb + nnc + nha
    misc.append({'ref': 'TEK-SCREWS-CLIPS', 'familia': 'Tek screws at clip angles', 'qty': tot, 'unit': 'PCS', 'source': '5/A-410; 7/A-210; 8/A-210; 1/A-210; A-410 note 8.A',
                 'op': (f'5/A-410 "2\" x 2\" 16 GA. CLIP ANGLE ... (4) TEK SCREWS": {ncl5} clips x 4 = {ncl5 * 4} + 7/A-210 "(4) #10-16 SCREWS": 4 clips x 4 = 16 + '
                        f'7/A-210 "RUNNER TRACK ATTACHED TO HEADER SUING (2) TEK SCREWS AT 16\" O.C" top and bottom runner: 2 runners x 2 x (ROUNDUP(12.667 / 1.333) + 1) = {nrt} + '
                        f'8/A-210 "(8) #10-16 TEKS 16\"O.C., TYP.": nested beam (ROUNDUP(12.667 / 1.333) + 1) x 8 = {nnb} + nested columns 6 x (ROUNDUP(10.5 / 1.333) + 1) x 8 = {nnc} + '
                        f'7/A-210 head attachment "#10-16 TEK SCREWS (TYP.)": 2 clips x 8 = {nha}; total {tot} pcs. Header 12\'-8\" = 1/A-210 front dimension chain (152\"). '
                        'Size: 5/A-410 prints none; the clip is 16 ga, so A-410 note 8.A "18/16 GAUGE - #10 - 16 X 3/4\" TEKS" applies (7/A-210 and 8/A-210 print #10-16)'),
                 'img': '../../PASO12_rev6/img/A-410_5-lateral-bracing-clip-angle.png'})
    # N-01: types 3 / 4 "3 5/8" METAL STUDS @ 16" O.C. TO BOTTOM OF NESTED STUD BRACING" (same phrase as F/A-221) - RFI-46
    t34 = [(w['id'], w['length_ft']) for w in walls['A-101'] if w['tag'] in ('3', '4')]
    q34 = round(sum(v for _, v in t34), 2)
    misc.append({'ref': 'NESTED-BRACING-T3-T4', 'familia': '3-5/8" stud (todos los gauges)', 'qty': q34, 'unit': 'LF', 'source': '3/A-410',
                 'op': f'3/A-410, 4/A-410 (partition types 3, 4) "3 5/8\\" METAL STUDS @ 16\\" O.C. TO BOTTOM OF NESTED STUD BRACING": one nested stud at the top of each wall = type 3 38.68 + type 4 83.64 = {q34} LF (conservative; member not drawn - RFI-46)',
                 'img': P7I + 'A-410_3-4_types-nested-stud-bracing.png'})

if REV7:   # fasteners de plywood (8.D) y de cement board, sobre las cantidades finales
    psf = round(sum(float(x['lf']) * float(x['width_ft']) for x in strips), 2)
    npl = _m7.ceil(psf * 34 / 32)
    misc.append({'ref': 'PLYWOOD-SCREWS-8D', 'familia': 'plywood screws (Teks/3)', 'qty': npl, 'unit': 'PCS', 'source': 'A-410',
                 'op': f'A-410 Partition Notes 8.D "#10-24 X 1-1/4\\" TEKS/3 ... 24\\" O.C. FIELD, 12\\" O.C. PERIMETER": 4x8 sheet on studs @ 16" = 24 perimeter + 10 field = 34 screws / 32 SF; {psf} SF FRT plywood x 34/32 = {npl} pcs'})
    csf = round(sum((f.get('length_ft') or w['length_ft']) * f['height_ft'] for sh in walls for w in walls[sh] for f in w.get('faces') or [] if 'cement' in f['board'])
                + sum(m['qty'] for m in misc if 'cement board' in m['familia'] and 'screw' not in m['familia']), 2)
    ncb = _m7.ceil(csf * 32 / 15)
    misc.append({'ref': 'CEMENT-BOARD-SCREWS', 'familia': 'cement board screws', 'qty': ncb, 'unit': 'PCS', 'source': 'E/A-221; A/A-221; B/A-221; C/A-221; D/A-221; 22/A-201',
                 'op': f'cement board screws @ 8" O.C. on studs @ 16" (manufacturer standard, spacing not printed - RFI-51): 3x5 board = 4 studs x 8 = 32 screws / 15 SF; {csf} SF x 32/15 = {ncb} pcs'})

# ---------------------------------------------------------------- REV9 (plan check rev8: C8-01..C8-08, regla v80j + R80e.30)
REV9 = os.environ.get('REV9') == '1'
SPLITS9 = []
if REV9:
    import math as _m9, re as _re9
    P6I = '../../PASO12_rev6/img/'
    # C8-01: 3/A-410, 4/A-410 "3 5/8" X 20GA TRACK W/ (2)-1/4"ø X 1 5/8" HILTI KWIK HUSEZ CONCRETE SCREW AND MOMENT CLIP - SEE DETAIL"
    # (A/A-410): that track is not on slab pins (note 8.F); the anchors stay in RFI-28
    for w in walls['A-101']:
        if w['tag'] in ('3', '4'):
            w['anchorage'] = {'value': 'other', 'source': f"{w['tag']}/A-410; A/A-410 (Kwik HUS-EZ + moment clip, RFI-28)"}
    # C8-03: 8/A-410 #8 screws: "ATTACH TO TOP CORD OF EXIST'G STRUCTURE W/ #8 SCREWS" (both conditions),
    # PARALLEL "(2) #8 SCREW AT EACH STUD" and "ATTACH TO TRACK W/ #8 SCREWS AT 24" O.C."
    wb9 = {w['id']: w for sh in walls for w in walls[sh]}
    FH9 = [w for w in wb9.values() if w.get('element') in ('wall', 'soffit_side') and float(w['height_ft']) >= 13.5]
    ncm9 = sum(_m9.ceil(float(w['length_ft']) / 2.0 - 1e-9) + 1 for w in FH9 if w['band']['ori'] == 'V')
    lh9 = round(sum(float(w['length_ft']) for w in FH9 if w['band']['ori'] == 'H'), 2)
    nx9 = sum(_m9.ceil(float(w['length_ft']) / 5.0 - 1e-9) + 1 for w in FH9 if w['band']['ori'] == 'H')
    n8s = 2 * ncm9 + ncm9 + 2 * ncm9 + nx9
    misc.append({'ref': 'SCREWS-8-A410', 'familia': '#8 screws, top chord / cross members (typ. connection)', 'qty': n8s, 'unit': 'PCS', 'source': 'TYPCONN/A-410',
                 'op': (f'TYPCONN/A-410 PARALLEL TO STRUCTURE: "(2) #8 SCREW AT EACH STUD" {ncm9} cross members x 2 = {2 * ncm9} + "ATTACH TO TRACK W/ #8 SCREWS AT 24\" O.C." '
                        f'sum(ROUNDUP(L / 2) + 1) over the walls parallel to the joists = {ncm9} + "ATTACH TO TOP CORD OF EXIST\'G STRUCTURE #8 SCREWS" {ncm9} cross members x 2 ends = {2 * ncm9}; '
                        f'PERPENDICULAR TO STRUCTURE: "ATTACH TO TOP CORD OF EXIST\'G STRUCTURE W/ #8 SCREWS" one per joist crossing, sum(ROUNDUP(L / 5.0) + 1) over {lh9} LF '
                        f'= {nx9} (joist spacing 5\'-0" not printed, same assumption as the cross members - RFI-41); total {n8s} pcs'),
                 'img': '../../PASO12_rev7/img/A-410_8_typ-connection-8-screws-24OC-PAF.png'})
    # C8-04: the ceiling / soffit track row is split by size (8/A-210, 4/A-210, 3/A-410, 2/A-221, 3/A-221)
    t36 = ['SS-N', 'SS-E', 'SS-IN-N', 'SS-IN-E', 'VEST-POSTS-TRACK']
    t6 = ['SS-GG', 'VEST-BOX-BEAM-TRACK']
    for m in misc:
        if m['ref'].startswith('FIRESTOP-') and m['familia'] == 'track de ceilings / soffits':
            (t6 if ': 6" track' in m['op'] else t36).append(m['ref'])
    SPLITS9 = [{'from': 'track de ceilings / soffits', 'to': 'ceiling / soffit track 3-5/8"', 'items': t36,
                'source': '3/A-410 (fire stop at ceiling line, 3-5/8" walls); 2/A-221 (soffit sides); 8/A-210 (nested column 3-5/8" track)'},
               {'from': 'track de ceilings / soffits', 'to': 'ceiling / soffit track 6"', 'items': t6,
                'source': '3/A-410 (fire stop at ceiling line, 6" walls); 3/A-221 (6" metal studs); 8/A-210 (nested beam "6"x16 GA TOP & BOTTOM TRACK")'},
               {'from': 'track de ceilings / soffits', 'to': 'ledger track 8"', 'items': ['VEST-LEDGER'], 'source': '4/A-210 "8" LEDGER"'}]
    # C8-08: 22/A-201 cement board base replaces gypsum board on these faces: per wall, for the board / screw split by gauge
    RR9 = ("Women's Restroom 109", "Men's Restroom 108")
    pw9 = {}
    for w in walls['A-101']:
        for f_ in w.get('faces') or []:
            if f_['room'] in RR9:
                dw = sum(float(o['ro_w_ft']) for o in w.get('openings') or [] if o.get('kind') == 'door' and o['ref'] in ('Door 8', 'Door 9'))
                pw9[w['id']] = round(pw9.get(w['id'], 0) + ((f_.get('length_ft') or w['length_ft']) - dw) * 14 / 12, 4)
    for m in misc:
        if m['ref'] == 'RESTROOM-BASE-CEMENT':
            m['board_base_sf_by_wall'] = pw9
    # C8-07: no plan-check item codes in client texts
    for m in misc:
        m['op'] = _re9.sub(r'\s*[-(]?\s*rev7 plan check C7?-\d+(?:\s*/\s*C7?-\d+)*\s*[:)]?', '', m['op']).replace(' (; ', ' (').replace('(rev7 plan check; ', '(')

frag_walls = {sh: {'walls': walls[sh]} for sh in walls}
frag_walls['A-101']['tags_descartados'] = [d for d in descartes if d['id'] == 'PT0007' or 'RFI-01' in d['motivo']]
frag_walls['A-221']['tags_descartados'] = [d for d in descartes if d['id'] != 'PT0007' and not (FINAL and d['id'] == 'PT0050')]
general = {
 'project': 'Barnes & Noble - Colorado Springs, CO (3173 Cinema Point) - bid set 250918',
 'constants': {'plan_scale_pt_per_ft': {'value': 9.0, 'source': 'A-101 1/8"=1\'-0" (grid C-D 30\'-0" CL/CL = 270 pt)'},
               'plan_scale_by_sheet': {'A-221': {'value': 36.0, 'source': '1/A-221 1/2"=1\'-0" (printed 28\'-5 7/8" = 1025.6 pt)'}},
               'carrying_direction': {'value': 'E-W', 'source': 'not printed (5/A-121 N.T.S., no plan arrow on A-121) - assumed E-W, RFI-15 with N-S delta'},
               'furring_oc_in': {'value': 24, 'source': '5/A-121 "7/8" HAT CHANNEL FRAMING @ 24" O.C. MAX"'},
               'carrying_oc_in': {'value': 48, 'source': '5/A-121 "1-1/2" CHANNEL @ 48" O.C. MAX"'},
               'hanger_oc_in': {'value': 48, 'source': '5/A-121 "HANGING WIRE TO STRUCTURE ABOVE AT 48" O.C. MAX"'},
               **({'slab_pin_spacing_ft': {'value': 0.666667, 'source': 'A-410 note 8.F X-DNI 2 rows @ 16" O.C. (printed, conservative); 9/A-410 0.177" PAF @ 24" = alternative'},
                   'drywall_screws_per_sf': {'value': 1.2, 'source': 'Estimator yield 1.2 screws / SF; products per A-410 Partition Notes 8.E (Type S on 25/20 ga, Type S-12 on 18/16 ga; field 12" ceilings, 24" walls) and A-001A Div 09 A.5'}} if os.environ.get('REV8') == '1' else {}),
               **({'addl_head_track_min_ro_ft': {'value': 3.9, 'source': 'RFI-31 conservative (audit rev4 row 8): additional head track note not printed in the set - doors 3 (C-H2a) and 11 (W2-03) 4\'-0" per the A-500 door schedule, carried with head track R.O. + 1\'-4"'}} if REV5 else {}),
               'bracing_spacing_in': {'value': 48, 'source': '5/A-410 lateral bracing CR 1-1/2" 16 ga @ 4\'-0" O.C. full wall height'}},
 'details': DETAILS,
 'opening_schedule': opening_schedule,
 'plywood_strips': strips,
 'nodes': nodes,
 'trim_items': trim,
 **({'blocking_items': blocking} if blocking else {}),
 **({'misc_items': misc} if misc else {}),
 **({'family_splits': SPLITS9} if SPLITS9 else {}),
 **({'corners_ok': [{'walls': list(p), 'reason': 'R75.7 (estimator rule): a short return (<= 2 ft) is measured from the OUTER face of the run it returns to, so return and run share the corner square by rule; esquinas.py R70.2 flags it as double - package inconsistency reported (PARA_REVISAR)'}
                    for p in (('W2-06.1', 'W2-06.2'), ('W2-06.3', 'W2-06.2'), ('W2-06.3', 'W2-06.4'), ('W2-06.5', 'W2-06.4'),
                              ('W4-28a', 'W4-28b'), ('W4-28a', 'W4-28c'), ('W4-31a', 'W4-31b'), ('W4-31a', 'W4-31c'))],
     'gaps_ok': [{'between': ['W2-06.1', 'W2-06.5'], 'reason': 'Drinking fountain recess (key note C26, A-101): the corridor wall steps back; the gap is closed by W2-06.2 / W2-06.3 / W2-06.4'}]} if FINAL else {}),
 'ceilings': ceilings,
 'deflection_clips': {'none_reason': 'Deflection by deep leg track / slotted deflection at the top of full height walls (8/A-410 Top Track Detail, 2/A-410 "SLOTTED DEFLECTION", A-410 partition note 7 "PROVIDE DEFLECTION TRACK AS REQUIRED"); no deflection clips called', 'source': '8/A-410'},
 'accesorios_rfi': [
   {'familia': 'stud reinforcement MEP', 'motivo': 'MEP sweep not registrable: the registration check of M-102 (page 48) vs A-101 (page 6) gave 20 / 14 matching wall segments (< 25 required); the HVAC sheet is not used for geometric crossings (registration rule). Ducts crossing the full-height type 2 / 5 / E walls must be counted from M-102 by the estimator.',
    'delta': 'per duct crossing a stud wall: + MAX(1, ROUNDUP(duct width / 16")) stud reinforcement plates x stud rows (6/A-410 penetration details); plus 1 duct sleeve each', 'source': 'M-102',
    'img': '4_canon/img/M102_registro_check.png', 'fuentes_revisadas': 'M-102 HVAC plan (page 48); mep.py registro (20 / 14 votes); P-101A..P-102D plumbing sheets (pipes <= 1" in cavity); 6/A-410 and 7/A-410 penetration details'}],
 'mep_sweep': {'sheets': ['M-102', 'P-101A', 'P-101B', 'P-102A', 'P-102B'], 'source': 'M-102, P-101A, P-101B, P-102A, P-102B', 'registro': {'dx_pt': -131.04, 'dy_pt': -477.0, 'matches': 14, 'source': 'M-102 vs A-101 (mep.registro)',
               'no_usable': {'motivo': 'registration below 25 matching wall segments (20 V / 14 H) and the check feature (type 4 center fixture) lands ~70 pt off -> sheet not used for geometric crossings (registration rule); stud reinforcement MEP to RFI', 'source': 'M-102', 'img': '4_canon/img/M102_registro_check.png'}}},
 'accesorios_none': [
   {'familia': 'extra framing ATM', 'why': 'No ATM / equipment recess in the set (A-101, A-500, A-221 reviewed)', 'source': 'A-101'},
   {'familia': 'gypsum board jamb return', 'why': 'No opening with a gypsum board return: doors in hollow metal frames (1/A-500); cased opening 2/A-500 is wood jamb + B-1 trim; storefronts are Div 08', 'source': '1/A-500'},
   {'familia': 'access panel', 'why': 'No access panel shown in GWB ceilings or walls (A-121 ceiling key notes 1-11, M-102 and P sheets reviewed)', 'source': 'A-121'},
   {'familia': 'Level 5 finish', 'why': 'No LEVEL 5 finish in A-510 room finish schedule / finish notes (paint finishes PT-1..PT-8 only)', 'source': 'A-510'}],

 'tile_base_none_reason': 'A-510 room finish schedule: ceramic cove tile base in Cafe 103, Men\'s 108, Women\'s 109; no cement board backer drawn behind the base on any partition detail (2/A-410, 5/A-410); cement board is loaded only where E/A-221 and A, B, C, D/A-221 draw it (wall faces) - backer for restroom base / wall tile (A-200, TL-2) = RFI-12 with delta',
 'frp_none_reason': FRP_R7 if os.environ.get('REV7') == '1' else 'FRP-1 (A-510: Cafe Work Room 104 walls, Janitor 107 walls, Cafe 103 below countertop) - no FRP height / extent printed for partitions (A-225 finish plan dashed FRP-1 zones only) - not quantified, RFI-13 with delta',
 'edge_blocking_none_reason': 'No stud blocking at gypsum board edges in the set: details 2/A-410, 3/A-410, 4/A-410, 5/A-410 (lateral bracing CR @ 4\'-0"), 1/A-500, 2/A-500 reviewed - none draws blocking at horizontal board joints (bridging per A-410 partition note 4 is carried as bracing C.R. channel)',
 'deck_breaks_none_reason': 'No stepped deck breaks: deck slopes continuously, B.O. DECK 24\'-0" (2/A-400B, west) to 25\'-7" (2/A-400A, east), 25\'-0" at 1/A-400A and 1/A-400B; interior walls to deck loaded at 25\'-0" - RFI-03',
}
def _ren(o):   # rev5 (audit rev4 row 21): the type I return carries its type in the ID
    t = json.dumps(o, ensure_ascii=False)
    if REV5:
        t = t.replace('C-E1-P.1', 'C-I-P.1')
    if os.environ.get('REV7') == '1':   # rev7 plan check C-07 / C-08: Top Track Detail = 3/A-410; 8/A-410 = Typ. Connection Detail
        t = t.replace('8/A-410', '3/A-410').replace('TYPCONN/A-410', '8/A-410')
        t = t.replace('(6/A-410 penetration details)', '(take-off default, not printed: 6/A-410 and 7/A-410 are pipe firestopping only)')
        t = t.replace('6/A-410 and 7/A-410 penetration details', '6/A-410 and 7/A-410 (pipe firestopping only; no reinforcement plate printed)')
    return json.loads(t)
for sh, fr in frag_walls.items():
    os.makedirs(OUT_W, exist_ok=True)
    json.dump(_ren(fr), open(OUT_W + f'/{sh}.json', 'w'), indent=1, ensure_ascii=False)
json.dump(_ren(general), open(OUT_W + '/general.json', 'w'), indent=1, ensure_ascii=False)
if FINAL:
    json.dump(RESOL, open(BN + '/takeoff_work/etapas/3_revision/resolucion_items.json', 'w'), indent=1, ensure_ascii=False)
for f in ('_walls_tmp.json', '_strips_tmp.json', '_nodes_tmp.json'):
    os.path.exists('/tmp/claude-0/-home-user-Reading-Plans/b9c208e2-64c4-5dc6-9d1d-2546bd4c85dc/scratchpad/lecturaA/' + f) and os.remove('/tmp/claude-0/-home-user-Reading-Plans/b9c208e2-64c4-5dc6-9d1d-2546bd4c85dc/scratchpad/lecturaA/' + f)
print('fragments written')
