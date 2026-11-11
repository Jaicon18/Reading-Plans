"""Grand Kia - paso 6: 4_canon/resuelto_Z*.json + 2_lectura/A/CEILINGS.json + DEMO.json -> 4_canon/takeoff_canon.json.
Solo traduce lo leído / resuelto al esquema canon (v68/v69); NO calcula materiales (canon.py / accesorios / plantilla).
Criterios fijos de proyecto (cada uno con su fuente impresa o regla del usuario):
  - board: 5/8" gyp wallboard (A550 keynote 3); Dens Shield en restrooms (2/A001 + A550 keynote 3) -> '5/8 glass mat
    tile backer' (BE-GK04); Type X solo en walls rated (no hay metal-stud rated: A551 = CMU U906).
  - gauge: no impreso para partitions (A550 'SEE STRUCTURAL'; S001 solo tabla mils/gauge) -> se carga 20 ga (33 mil,
    el único CFS impreso del set: S403 362S162-33) con RFI-01 (U-116); no cambia cantidades.
  - top track: walls a estructura (A/A1, C/C1, E/E1 cara a deck) = deflection track 14 ga 2" legs 13/A540; resto standard.
  - bridging: 1-1/2" C.R. channel a media altura (A550 keynotes 5/8/12/13) = 1 fila (R-ALC-10: plano sobre spec 3.3.E).
"""
import json, glob, os, re, copy
W = '/root/gk/work'
E = f'{W}/etapas'
OUT = f'{E}/4_canon/takeoff_canon.json'
ORDER = ['A', 'A1', 'B', 'B1', 'C', 'C1', 'D', 'D1', 'E', 'E1', 'F', 'F1', 'G', 'G1', 'H', 'H1']
STUD = {'A': '3-5/8"', 'B': '3-5/8"', 'C': '6"', 'D': '6"', 'E': '8"', 'F': '2-1/2"', 'G': '3-5/8"', 'H': '6"'}
SLIP_TYPES = ('A', 'C', 'E')
DEFL = ('13/A540 DEFLECTION TRACK: 14 GA track w/ 2" deep legs, studs attached w/ 1 #10 screw ea side in vertically '
        'slotted holes, do not connect gyp bd to track (A550 types A, C, E head bubble 13/A540)')
GAUGE = '20 ga (33 mil) - not printed for partitions: RFI-01'
GAUGE_SRC = ('A550 keynotes 5/8/12/13 "SEE STRUCTURAL FOR GAUGE PER HEIGHT REQUIREMENTS"; S001 lists only the mils/gauge '
             'table; the only cold-formed stud printed in the set is 362S162-33 @16" (S403 det 247/251, S302 det 125) '
             '-> 33 mil (20 ga structural) loaded, RFI-01 (quantities unchanged by gauge)')


def base_type(t):
    return re.sub(r'1$', '', str(t or ''))


def board_key(face):
    b = str(face.get('board') or '')
    if re.search(r'dens\s*shield|glass[- ]mat|tile backer', b, re.I) or face.get('tile') and re.search(r'restroom|toilet|men|women|rr', str(face.get('room') or ''), re.I):
        return '5/8 glass mat tile backer'
    if re.search(r'type\s*x', b, re.I):
        return '5/8 type X'
    return '5/8 regular'


def wall_canon(w):
    w = copy.deepcopy(w)
    import sys
    sys.path.insert(0, '/root/gk/skill/take-off-metal-frame-drywall/tools')
    import canon as _c
    for k in list(w):
        if k not in _c.WALL_KEYS and not k.endswith(_c.TRAZA_SUFIJOS):
            w[k + '_info'] = w.pop(k)      # trace fields of the readers (schema rule: suffix _info)
    t = w.get('tag') or w.get('type_info') or w.get('type')
    bt = base_type(t)
    w['element'] = w.get('element') or 'wall'
    w['tag'] = t
    w['stud_size'] = STUD.get(bt) or re.sub(r'(\d) (\d/\d)', r'\1-\2', str(w.get('stud_size') or ''))
    w['stud_source'] = f'A550 type {bt} section title + keynotes 5/8/12/13 (stud size)'
    w['detail_info'] = w.get('detail')
    w['detail'] = f'{bt}/A550' if bt in STUD else (w.get('detail') or 'A550')
    w['source'] = w.get('source') or f"{w.get('sheet')} tag {t}; A550 type {bt}" + (f"; {w.get('detail')}" if w.get('detail') else '')
    w['gauge'] = GAUGE
    w['gauge_source'] = GAUGE_SRC
    w['oc_in'] = w.get('oc_in') or 16
    w['oc_source'] = w.get('oc_source') or 'A550 keynotes 5/8/12/13 "VERTICAL STUDS SHALL BE SPACED 16" O.C. U.N.O."'
    slip = bt in SLIP_TYPES or '[DEFLECTION' in str(w.get('top_track_info') or '').upper()
    w['top_track_kind'] = 'slip' if slip else 'standard'
    w['top_track_kind_source'] = (DEFL if slip else
                                  f'A550 type {bt}: wall stops below structure (partial height / furring) - standard top track')
    if slip:
        w['top_track_leg'] = '2"'
    w['bottom_track'] = True
    w['top_track'] = True
    w['bracing_rows'] = 1 if bt in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H') else 0
    w['bracing_rows_source'] = ('A550 keynotes 5/8/12/13 "BRIDGE STUDS AT MID-HEIGHT WITH 1 1/2" CHANNELS THROUGH STUDS" '
                                '(1 row; spec 054000 3.3.E rows <= 48" applies to exterior framing - plan governs, R-ALC-10)')
    rated_furr = bt in ('F', 'G', 'H') and (re.search(r'(?i)rated CMU', str(w.get('location'))) or
                                            re.search(r'(?i)^(?!no\b).*(dashed rated|CMU behind = 2HR)', str(w.get('rated_source'))))
    for f in w.get('faces') or []:
        f['board'] = board_key(f)
        if rated_furr and f['board'] == '5/8 regular':   # A550 keynote 3 'TYPE X AT RATED WALLS': furring over rated CMU
            f['board'] = '5/8 type X'
            f['board_source'] = "A550 keynote 3 '5/8\" GYP. BD. - TYPE X AT RATED WALLS' (furring on the rated CMU line, A111 rated hatch)"
        f.setdefault('layers', 1)
    # tramos por cara: Σ tramos de un side = L (board_caras). Tramo = largo del wall -> cara completa; un solo tramo
    # más corto en su side -> cara con deduct_sf = (L - tramo) x H (1 layer), con la traza; más largo -> cara completa.
    L = float(w.get('length_ft') or 0)
    por = {}
    for f in w.get('faces') or []:
        if f.get('length_ft') is not None and f.get('side') in ('A', 'B'):
            por.setdefault(f['side'], []).append(f)
    for side, fs in por.items():
        tot = sum(float(f['length_ft']) for f in fs)
        if abs(tot - L) <= 0.05:
            for f in fs:
                f['length_source'] = f.get('length_source') or w.get('length_source') or w.get('sheet')
                if len(fs) == 1:
                    f['length_ft_info'] = f.pop('length_ft'); f.pop('length_source', None)
            continue
        for f in fs:
            lf = float(f.pop('length_ft'))
            f['length_ft_info'] = lf
            if lf < L - 0.05 and len(fs) == 1 and int(f.get('layers') or 1) == 1:
                f['deduct_sf'] = round((L - lf) * float(f.get('height_ft') or w.get('height_ft') or 0), 2)
                f['deduct_sf_info'] = (f"board on {lf:g} ft of the {L:g} ft side ({f.get('room')}): "
                                       f"({L:g} - {lf:g}) x {f.get('height_ft') or w.get('height_ft')} ft not boarded")
        if len(fs) > 1:   # varios tramos que no suman el largo: se escalan al largo del wall (cara completa por tramo)
            k = L / tot if tot else 1
            for f in fs:
                f['length_ft'] = round(f['length_ft_info'] * k, 3)
                f['length_source'] = f"{w.get('sheet')} tramo {f['length_ft_info']} ft of measured {tot:g}, side scaled to wall length {L:g}"
            dif = round(L - sum(f['length_ft'] for f in fs), 3)
            fs[-1]['length_ft'] = round(fs[-1]['length_ft'] + dif, 3)
    return w


HDR_DOOR = '3/A530 HM HEAD/JAMB AT STUDS: head = one runner track over the frame (web down)' 
HDR_ALUM = '12/A530 ALUM. DOOR HEAD/JAMB: head = one runner track per wall construction' 


def cita(txt, dflt):
    """solo las referencias N/HOJA del texto (forma que exigen las tools); el texto completo va a *_info."""
    refs = []
    for m in re.finditer(r'\b(?:[A-Z0-9]{1,3}/)?[A-Z]{1,2}\d{3}[A-Z]?\b', str(txt or '')):
        if m.group(0) not in refs:
            refs.append(m.group(0))
    return ', '.join(refs) or dflt


def opening_canon(o, w):
    o = dict(o)
    o['ref'] = str(o.get('ref'))
    k = o.get('kind') or 'door'
    o['kind'] = k
    wd = float(o.get('ro_w_ft') or o.get('width_ft') or 0)
    if not o.get('ro_w_ft'):
        if k == 'door':
            o['ro_w_ft'] = round(wd + 4 / 12, 3)
            o['ro_w_source'] = f"{o.get('source', 'A400')}: door width {wd:g} ft + 2\" HM / alum frame face each side (3/A530, 12/A530) = R.O. [DERIVED]"
        else:
            o['ro_w_ft'] = round(wd, 3)
            o['ro_w_source'] = f"{o.get('source', 'A221')}: frame width = R.O. [DERIVED]"
    h = o.get('head_ft')
    if h in (None, ''):
        hh = float(o.get('height_ft') or 0)
        if k == 'door':
            o['head_ft'] = round(hh + 2 / 12, 3) if hh else 7.0
        else:
            o['head_ft'] = round(float(o.get('sill_ft') or 0) + hh, 3) if hh else 7.0
        o['head_source'] = (f"{o.get('source', '')}: opening height {hh:g} ft + 2\" frame head [DERIVED]" if hh else
                            'head not printed: 7.0 ft loaded (RFI-02)')
    o['header'] = 'metal'
    alum = re.search(r'alum|storefront|12/A530|\bAL\b|window', str(o.get('source', '')) + ' ' + k, re.I)
    o['header_type'] = 'HEAD TRACK - ' + ('12/A530' if alum else '3/A530')
    o['header_type_source'] = '12/A530' if alum else '3/A530'
    o['pieces'] = 1
    o['pieces_source'] = HDR_ALUM if alum else HDR_DOOR
    o['piece'] = f"track matching wall stud ({w.get('stud_size')})"
    o['header_source'] = o['header_type_source'] + ' (printed head detail)'
    if k in ('window', 'storefront') or alum:
        o['substrate_none_reason'] = ('12/A530 ALUM. DOOR HEAD/JAMB and 13/A530 jamb: J mold each side, boxed double-stud '
                                      'jambs, no plywood / FRT substrate drawn at the frame (A221 interior frames)')
    if k in ('window', 'storefront') or alum:
        o['jamb_return'] = False
        o['jamb_return_source'] = '12/A530, 13/A530: board stops at the aluminum frame with "TYP. J MOLD EA. SIDE" (no gypsum jamb return drawn)'
    if k == 'window':
        o['with_sill'] = True
        o['with_sill_source'] = 'A221 interior window frame elevations (sill at 4\'-0\" A.F.F.: sill track under the frame, same head detail 12/A530)'
    for x in ('width_ft', 'height_ft', 'zone'):
        if x in o:
            o[x + '_info'] = o.pop(x)
    for k in [k for k in o if k.endswith('source') and k != 'header_type_source']:
        o[k + '_info'] = o[k]
        o[k] = cita(o[k], 'A400' if k == 'source' else o.get('header_type_source', 'A400'))
    return o


# Resolución dirigida del orquestador (stage 3, una revisión por ítem con imagen; U-012)
DESCARTE = {
    "X-Z1-01": ("EXCLUDED: entry portal west leg - A111 keynote 41 'ENTRY PORTAL BY GC & ACM CLADDING' "
                "(by GC / owner's vendor, not our scope; 2/A521, 3/A521)", "etapas/3_revision/img/Z1/"),
    "X-Z1-02": ("EXCLUDED: entry portal east leg on grid D - A111 keynote 41 'ENTRY PORTAL BY GC & ACM CLADDING' "
                "(by GC / owner's vendor, not our scope; 2/A521, 3/A521)", "etapas/3_revision/img/Z1/"),
    "A-Z1-20": ("same single wall as A1-Z1-08 behind the drinking fountain / WOMEN 120 vanity (one wall drawn on A111 / "
                "1/A150; A-Z1-20 came from an ambiguous leader): counted once as A1-Z1-08",
                "etapas/3_revision/img/Z1/r_A1-Z1-08.png"),
}


# campos por wall decididos en la revisión (cada uno con su fuente)
AJUSTE = {
    "A-Z1-11": {"return_basis": {"value": "inner_face", "source": "A111: short return measured on the vector band between the faces of A-Z1-10 (resolution Z1)"}},
}


AOJO = re.compile(r"~\s?(\d)|approx\.?\s?(\d)|aprox\.?\s?(\d)|\ba ojo\b|eyeball|by eye", re.I)
HOJA_RX = re.compile(r"\b[A-Z]{1,3}-?\d{3}[A-Z]?\b")


def limpio(t):
    """texto de fuente sin marcas de 'a ojo' (el valor es DERIVADO por vector / sección a escala; el texto original queda en *_info)."""
    return AOJO.sub(lambda m: next(g for g in m.groups() if g), str(t or ''))


def absimg(p, z=None):
    if isinstance(p, (list, tuple)):
        p = p[0] if p else None
    if not p:
        return None
    for base in ('', f'{E}/2_lectura/A/', f'{E}/2_lectura/B/', f'{E}/3_revision/', f'{W}/'):
        q = p if p.startswith('/') else base + p
        if os.path.isfile(q):
            return q
    return None


def evidencia(w):
    bt = base_type(w.get('tag'))
    w['length_basis'] = ("face to face: vector band between the wall faces / printed dimension strings to face of stud "
                         "(A111 general note 1 'DIMENSIONS ARE TO FACE OF CMU OR FACE OF SHEATHING')")
    if w['top_track_kind'] == 'slip':
        w['to_deck_source'] = f"13/A540 deflection track (14 GA, 2\" legs, 1\" gap) at the head of type {bt} studs to the underside of structure (A550 {bt} section)"
    elif bt in ('B', 'D'):
        w['to_deck_source'] = f"{bt}/A550 partial height: standard top track at ceiling + 6\", braced to structure per 8/A540 (dia. brace @4'-0\" o.c.)"
    else:
        w['to_deck_source'] = f"{bt}/A550 furring: standard top track at the board top (ceiling + 6\"; keynote 9 to deck where no ceiling)"
    w['detail_source'] = f"{bt}/A550 type section (wall tag {w.get('tag')} on {w.get('sheet')}); head 13/A540; floor 10/A540"
    for k in ('height_source', 'length_source'):
        if AOJO.search(str(w.get(k) or '')):
            w[k + '_info'] = w[k]; w[k] = limpio(w[k])
    if not HOJA_RX.search(str(w.get('height_source') or '')):
        w['height_source'] = f"{w.get('sheet')}: " + str(w.get('height_source') or '')
    im = absimg(w.get('img')) or absimg(w.get('img_resolution'))
    if im:
        w['img'] = im
    if w.get('height_img'):
        w['height_img'] = absimg(w['height_img']) or w['height_img']
    for f in w.get('faces') or []:
        hs = str(f.get('height_source') or w.get('height_source') or '')
        if AOJO.search(hs):
            f['height_source_info'] = hs; hs = limpio(hs)
        if not HOJA_RX.search(hs):
            hs = f"{w.get('sheet')}: {hs}" if hs else str(w.get('height_source'))
        f['height_source'] = hs
        f.setdefault('room', w.get('location'))
        f.setdefault('height_ft', w.get('height_ft'))
    if not w.get('tag_ids'):
        w['tag_manual'] = {"source": f"{w.get('tag')}/{w.get('sheet')}",
                           "sheet_raster": f"{w.get('sheet')} text drawn as curves (no text layer, BE-GK02): OCR inventory "
                                           "incomplete; tag found by eye by readers A and B (crop in img)",
                           "img": w.get('img')}
    for o in w.get('openings') or []:
        o.setdefault('img', w.get('img'))
        o['ro_w_op'] = o.get('ro_w_op') or str(o.get('ro_w_source_info') or o.get('ro_w_source') or '')
    st = [k for k in ('length_status', 'height_status', 'status') if str(w.get(k) or '').upper() == 'PENDIENTE']
    if st:
        w['sheets_searched'] = "A111, A112, A113, A150, A130-A133, A210-A211, A300, A301, A310-A312, A540, A550, S111-S122, S401-S403"
        w['pending_reason'] = f"not printed: {', '.join(st)} (see RFI list)"
    return w


RF = json.load(open(f'{E}/4_canon/rfis_final.json')) if os.path.exists(f'{E}/4_canon/rfis_final.json') else {"rfis": []}
RFI = {r['id']: r for r in RF['rfis']}
GBW = ((RFI.get('RFI-01') or {}).get('resolved') or {}).get('gauge_by_wall') or {}
ROWS = ((RFI.get('RFI-11') or {}).get('resolved') or {}).get('rows_by_wall') or {}
HEAVY = {'3-5/8"': '362S162-97', '2-1/2"': '250S162-68', '6"': '600S162-97', '8"': '800S162-97'}
MILS_GA = {'19': '25 ga', '33': '20 ga', '43': '18 ga', '54': '16 ga', '68': '14 ga', '97': '12 ga'}
RESTROOM_9 = {"B-Z3-01", "B-Z3-02", "H-Z3-01", "F-Z3-01"}


def gauge_rows(w):
    g = GBW.get(w['id'])
    if g:
        mem = g.get('member')
        if mem == 'EXCEEDS':
            mem = HEAVY.get(w.get('stud_size'), mem)
            w['gauge'] = f"{mem} ({MILS_GA.get(mem.split('-')[-1], '')}) - conservative, wall {w.get('height_ft')} ft taller than 62/S204 and the SFIA limiting heights: RFI-01"
            w['gauge_source'] = "62/S204 'ALLOWABLE INTERIOR WALL HEIGHT' + SFIA table (A550 GN 1, 2024 IBC) end below this height: heaviest member of the drawn stud depth loaded (RFI-01)"
        else:
            w['gauge'] = f"{mem} ({MILS_GA.get(str(mem).split('-')[-1], '')})"
            w['gauge_source'] = f"{g.get('source')} allowable interior wall height for {w.get('stud_size')} @16\" o.c. at H {g.get('height_ft')} ft (A550 keynotes 'SEE STRUCTURAL FOR GAUGE PER HEIGHT'); SFIA CCRR-0224 table where 62/S204 stops (2024 IBC)"
    if w['id'] in ROWS:
        w['bracing_rows'] = int(ROWS[w['id']])
        w['bracing_rows_source'] = ("62/S204 note 2 'BLOCKED AT 5'-0\" O.C. MAX WHERE NOT SHEATHED EACH FACE' + A550 keynote 5 'BRIDGE STUDS AT MID-HEIGHT'"
                                    ": rows = max(1, ROUNDUP(H/5)-1) of 1-1/2\" C.R. channel (A550 keynotes)")
    TICKS = {"B-Z2-02": ("A111 string 4'-0 1/2\" + 7'-8 1/2\" with SINGLE ticks (slash marks); stud run measured in vector to the north face of E (not the string total)", "ticks_B-Z2-02_A111.png"),
             "F-Z3-03": ("A112 string 8'-0\" (window F) + 5'-4\" with SINGLE ticks, overall 19'-4\" C.8 to C; wall measured in vector", "ticks_F-Z3-03_A112.png")}
    if w['id'] in TICKS:
        w['length_op'] = f"{w.get('length_op')} [ticks: {TICKS[w['id']][0]}]"
        w['ticks_img'] = f"/root/gk/work/etapas/7_imagenes/{TICKS[w['id']][1]}"
    ho = str(w.get('height_op') or '')
    if 'check:' in ho:
        w['height_op'], w['height_check_info'] = ho.split(';')[0].replace(' ft above slab (-0\'-6\")', ''), ho
    if w['id'] in RESTROOM_9:
        w['height_ft_info'] = w.get('height_ft'); w['height_ft'] = 9.5
        w['height_op_info'] = w.get('height_op'); w['height_op'] = "9.0 + 0.5 = 9.5"
        w['height_source'] = "A211 restroom elevations 9'-0\" to the ceiling line + 6\" (A550) = 9.5 ft - conservative while RFI-07 (A132 RCP tags 8'-0\") is open"
        for f in w.get('faces') or []:
            f['height_ft'] = 9.5; f['height_source'] = w['height_source']
    return w


def fix_corners(walls, esc_by_sheet):
    """R70.2 por programa (regla fija, una sola por proyecto):
    T (uno pasa de largo): el que pasa es dueño; el que termina se extiende (sin dueño) o se recorta (doble) a su cara.
    L: el tramo más corto (return, R75.7 cara exterior) es dueño; el más largo se ajusta.
    Cada cambio queda en band + length_ft + length_op (traza DERIVADO)."""
    import sys
    sys.path.insert(0, '/root/gk/skill/take-off-metal-frame-drywall/tools')
    import esquinas as Q
    n = 0

    def bloqueado(w):   # U-017: a wall whose length IS its own printed dimension is never stretched / trimmed by the corner rule
        return str(w.get('length_status')) == 'CONFIRMADO' or bool(re.search(r"(?i)printed (dim )?\d+'|\bdim \d+'-|2/A150 printed", str(w.get('length_source'))))

    def ajustar(w, g, o, modo, esc, dueno):
        if bloqueado(w):
            return False
        hi_side = abs(g['hi'] - (o['c0'] + o['c1']) / 2) <= abs(g['lo'] - (o['c0'] + o['c1']) / 2)
        if modo == 'ext':
            d = (o['c1'] - g['hi']) if hi_side else (g['lo'] - o['c0'])
        else:
            d = (g['hi'] - o['c0']) if hi_side else (o['c1'] - g['lo'])
        if not (0 < d <= (o['c1'] - o['c0']) + 0.5 * esc):
            return False
        b = w['band']
        if modo == 'ext':
            b['hi' if hi_side else 'lo'] = round(float(b['hi']) + d, 2) if hi_side else round(float(b['lo']) - d, 2)
        else:
            b['hi' if hi_side else 'lo'] = round(float(b['hi']) - d, 2) if hi_side else round(float(b['lo']) + d, 2)
        dl = round(d / esc, 3)
        w['length_ft'] = round(float(w['length_ft']) + (dl if modo == 'ext' else -dl), 3)
        w['length_op'] = (f"{w.get('length_op', '')} {'+' if modo == 'ext' else '-'} corner square {dl} ft "
                          f"({'owned here, meets' if modo == 'ext' else 'owned by'} {dueno}, R70.2) = {w['length_ft']}")
        return True

    for _ in range(4):
        cambio = False
        U = [(w, Q.geo(w)) for w in walls if w.get('band') and Q.geo(w) and w.get('element', 'wall') == 'wall']
        for wh, h in U:
            if h['ori'] != 'H':
                continue
            for wv, v in U:
                if v['ori'] != 'V' or Q.hoja(wh) != Q.hoja(wv):
                    continue
                esc = esc_by_sheet.get(Q.hoja(wh), 9.0); tol = 0.25 * esc
                h, v = Q.geo(wh), Q.geo(wv)
                e = Q._esquina(h, v, tol)
                if not e or (e[0] != e[1]):
                    continue
                h_pasa = h['lo'] < v['c0'] - tol and h['hi'] > v['c1'] + tol
                v_pasa = v['lo'] < h['c0'] - tol and v['hi'] > h['c1'] + tol
                modo = 'ext' if not e[0] else 'trim'
                if v_pasa:      # T: V pasa -> V dueño
                    ok = ajustar(wh, h, v, 'ext' if modo == 'ext' else 'trim', esc, wv['id']) if modo == 'trim' else \
                        ajustar(wh, h, v, 'ext', esc, wv['id'])
                elif h_pasa:
                    ok = ajustar(wv, v, h, modo, esc, wh['id'])
                else:           # L: el más corto es dueño
                    corto_h = float(wh['length_ft']) <= float(wv['length_ft'])
                    if modo == 'ext':
                        ok = ajustar(wh, h, v, 'ext', esc, wv['id']) if corto_h else ajustar(wv, v, h, 'ext', esc, wh['id'])
                    else:
                        ok = ajustar(wv, v, h, 'trim', esc, wh['id']) if corto_h else ajustar(wh, h, v, 'trim', esc, wv['id'])
                if ok:
                    n += 1; cambio = True
        if not cambio:
            break
    return n


def main():
    zonas = {}
    for f in sorted(glob.glob(f'{E}/4_canon/resuelto_Z*.json')):
        d = json.load(open(f)); zonas[d.get('zone') or os.path.basename(f)[9:11]] = d
    walls, ops, dets, rfi_c, rev, desc, exc, soff, tags_d = [], [], {}, [], [], [], [], [], []
    for z, d in sorted(zonas.items()):
        for w in d['walls']:
            if w.get('resolution') == 'discarded':
                continue
            if w['id'] in DESCARTE:
                desc.append({"id": w['id'], "reason": DESCARTE[w['id']][0], "img": DESCARTE[w['id']][1], "zone": z})
                continue
            wc = wall_canon(w)
            wc.update(AJUSTE.get(wc['id'], {}))
            gauge_rows(wc)
            evidencia(wc)
            wc['openings'] = [opening_canon(o, wc) for o in (w.get('openings') or [])]
            for o in wc['openings']:
                o.setdefault('img', wc.get('img'))
                o['ro_w_op'] = o.get('ro_w_op') or str(o.get('ro_w_source_info') or o.get('ro_w_source') or '')
            walls.append(wc)
        for it in (d.get('opening_schedule') or {}).get('items') or []:
            ops.append(dict(it, zone=z))
        for k, v in (d.get('details') or {}).items():
            dets.setdefault(k, v)
        rfi_c += [dict(x, zone=z) if isinstance(x, dict) else {'item': str(x), 'zone': z} for x in d.get('rfi_candidates') or []]
        rev += [dict(x, zone=z) if isinstance(x, dict) else {'item': str(x), 'zone': z} for x in d.get('review_items') or []]
        desc += [dict(x, zone=z) if isinstance(x, dict) else {'item': str(x), 'zone': z} for x in d.get('discarded') or []]
        exc += [dict(x, zone=z) if isinstance(x, dict) else {'item': str(x), 'zone': z} for x in d.get('excluded_areas') or []]
        soff += [dict(x, zone=z) if isinstance(x, dict) else {'item': str(x), 'zone': z} for x in d.get('soffits') or []]
        tags_d += d.get('tags_descartados') or []
    decl = {o['ref'] for w in walls for o in w['openings']}
    none = []
    for it in ops:
        r = str(it.get('ref'))
        if r not in decl and r not in {n['ref'] for n in none}:
            none.append({"ref": r, "why": f"not in a new metal-stud wall of this take-off: {it.get('wall') or it.get('note') or it.get('source')}"[:300]})
    sched = {"sources": ["A400", "A401", "A220", "A221", "A111", "A112", "A113", "A150", "S111", "S112", "S121", "M101", "M102", "M103"],
             "sources_info": "A400 door schedule, A220/A221 window frame elevations, plans; S111-S122 swept for lintels / steel headers at stud walls (none: steel framing is structure); M101-M103 swept for ducts through walls (see mep_sweep)",
             "items": [{"ref": r} for r in sorted(decl | {n['ref'] for n in none})], "none": none}
    walls.sort(key=lambda w: (ORDER.index(w['tag']) if w['tag'] in ORDER else 99, w['id']))
    canon = {
        "project": "Grand Kia - 2040 W 104th Ave, Thornton (Denver) CO 80234 - John Mahoney Architect project 2412, "
                   "drawing set issue 7/23/26 - resolved canon (readers A + B, stage 3)",
        "constants": {
            "plan_scale_pt_per_ft": {"value": 9.0, "source": "A111 / A112",
                                     "source_info": "A111/A112 partial plans: printed scale bar reads 1/4\"=1'-0\" but every printed "
                                                    "dimension string measures 9 pt/ft (1/8\"=1'-0\"), checked by readers A and B "
                                                    "on 3-4 strings each; the dimensions govern"},
            "plan_scale_by_sheet": {
                "A131": {"value": 9.0, "source": "A131 1/8\" = 1'-0\" measured: 90 of 120 A111 wall lines (A111 printed dimension strings = 9.0 pt/ft) fall full length at the same coordinates on A131, so the RCP measures the same; the scale bar label prints 1/4\" (Review Item)"},
                "A132": {"value": 9.0, "source": "A132 1/8\" = 1'-0\" measured: 12 of 15 A112 wall lines (A112 printed dimension strings = 9.0 pt/ft) fall full length at the same coordinates on A132; the scale bar label prints 1/4\" (Review Item)"},
                "A200": {"value": 9.0, "source": "A200 exterior elevations 1/8\" = 1'-0\" printed (view titles)"},
                "A220": {"value": 13.5, "source": "A220 window frame elevations 3/16\" = 1'-0\" printed (view titles)"},
                "A111": {"value": 9.0, "source": "A111 1/8\" = 1'-0\" measured on the printed dimension strings: F-Z3-03 8'-0\" = 72.0 pt, B-Z2-02 7'-8 1/2\" = 69.6 pt (9.0 pt/ft); the scale bar label prints 1/4\" and does not match the dimensions (Review Item, COORDINACION 11-nov)"},
                "A112": {"value": 9.0, "source": "A112 1/8\" = 1'-0\" measured on the printed dimension strings (same partial-plan set as A111, 9.0 pt/ft checked by readers A and B on 3-4 strings); the scale bar label prints 1/4\" and does not match the dimensions (Review Item)"},
                "A113": {"value": 6.75, "source": "A113 3/32\"=1'-0\" (bar 0-16' = 109.2 pt)"},
                "A150": {"value": 36.0, "source": "A150 1/2\"=1'-0\""},
                "A108": {"value": 6.75, "source": "A108 3/32\"=1'-0\" (grid H to C = 96'-0\" printed on A301 measures 648 pt)"},
                "A109": {"value": 6.75, "source": "A109 3/32\"=1'-0\" (same grid spacing as A108)"}},
            "slip_track_product": {"value": "T200-68", "source": "13/A540 DEFLECTION TRACK '14 GA. TRACK W/ 2\" DEEP LEGS'"},
            "partition_row_rule": {"value": "wall_id", "source": "U-120 / BE-HF05: one Partition Takeoff row per Wall ID (never two walls or axes in one number); each row matches its Bluebeam markup"},
            "double_row_types": {"value": [], "source": "A550: furring types F/G/H are single-row studs (2-1/2\", 3-5/8\", 6\" @16\" o.c.); no double-row partition type in the set"},
            "north_arrow": {"value": "north arrow on A110 / A111 title", "source": "A111"},
            "bracing_spacing_in": {"value": 48, "source": "8/A540", "source_info": "8/A540 'DIA. BRACE @4'-0\" O.C.'"},
            "sheet_len_ft": {"value": 12, "source": "A550 type sections (board continuous floor to structure, taller than one 4'x12' sheet) + spec 092900 3.x (install per ASTM C840); 12 ft = stock sheet length (no length printed)"},
            "addl_head_track_min_ro_ft": {"value": 4.0, "source": "3/A530 and 12/A530 heads at stud framing (track header over the opening) + spec 054000 (AISI S100 header design): additional head track over openings wider than 4'-0\" (estimator standing criterion)"},
            "header_bearing_ft": {"value": 0.6666666666666666, "source": "3/A530 / 12/A530 head: track header R.O. + 8\" bearing each side (estimator standing criterion, length not dimensioned)"},
        },
        "walls": walls,
        "deck_breaks_none_reason": ("No deck elevation / deck tags are printed on any plan (A111-A113, S111-S122); each wall "
                                    "height was measured per wall on the building / wall sections at their printed scale "
                                    "(A300, A301, A310-A312) at that wall's location, so a wall crossing two roof heights "
                                    "is cut at the section break (resolution files 3_revision/resolucion_Z*.md)"),
        "details": dets,
        "opening_schedule": sched,
        "opening_items_raw": ops,
        "soffits_raw": soff,
        "rfi_candidates_raw": rfi_c,
        "review_items_raw": rev,
        "excluded_walls": desc,
        "excluded_areas": exc,
        "tags_descartados": tags_d,
    }
    TIT = {'A': 'FULL HGT 3 5/8" METAL STUD PARTITION', 'B': 'PARTIAL HEIGHT 3 5/8" METAL STUD PARTITION',
           'C': 'FULL HEIGHT 6" METAL STUD PARTITION', 'D': 'PARTIAL HEIGHT 6" METAL STUD PARTITION',
           'E': 'FULL HGT 8" PART CLG HGT GYP BD 1 SIDE', 'F': '2 1/2" METAL STUD FURRING', 'G': '3 5/8" METAL STUD FURRING',
           'H': '6" METAL STUD FURRING'}
    for t, tt in TIT.items():
        dets[f'{t}/A550'] = dict(dets.get(f'{t}/A550') or {}, source=f'{t}/A550', title=f'TYPE {t} / {t}1: {tt}',
                                 layers_per_face=1,
                                 layers_source=f'{t}/A550 section: one layer of 5/8" gyp wallboard per face drawn (keynote 3)')
    for w in walls:
        if w['detail'] not in dets:
            dets[w['detail']] = {"source": w['detail'], "layers_per_face": 1, "layers_source": w['detail']}
    MG = json.load(open(f'{E}/4_canon/misc_gen.json')) if os.path.exists(f'{E}/4_canon/misc_gen.json') else {"misc_items": []}
    canon['misc_items'] = MG['misc_items']
    canon['ceilings'] = []
    canon['ceilings_info'] = ("Gypsum board ceilings / soffits / coves carried as misc_items (program scripts/misc_gen.py, op visible per "
                              "room from the A131 / A132 RCP polygons; A130 is the overall view of the same rooms); ACT, open to "
                              "structure and existing ceilings = excluded per room (excluded_rooms of the ceilings reading).")
    canon['trim_items'] = []
    canon['trim_none_reason'] = "metal trim carried by program from the nodes and soffit edges (scripts/trim_gen in build_canon)"
    canon['tile_base_none_reason'] = "A140 finish schedule: wall base B-1 rubber / tile base at restrooms is over Dens Shield (no cement board in the set: 2/A001 Dens Shield at all restroom gyp)"
    canon['frp_none_reason'] = "FRP-1 (janitor, A140 finish schedule) = spec 066400 Plastic Paneling (Div. 06) by others - EXCLUDED (not our trade, U-061)"
    canon['atm_recess_none_reason'] = "No ATM / equipment recess in the set (A111, A112, A230, A231)"
    canon['ballistic_jogs_none_reason'] = "No ballistic panels (A550 types A-K only)"
    canon['types_none_reason'] = {"G1": "A550 type G1 (3-5/8\" furring with batt) not tagged on A111-A113", "J / K": "CMU types (not our trade)"}
    canon['fasteners_excluded'] = {"why": "all screws / anchors / shot pins excluded (estimator standing order U-053)", "source": "A550 keynote 4, 10/A540, 13/A540"}
    canon['wood_excluded'] = {"why": "wood blocking / plywood is Div. 06, never carried (U-139)", "source": "061000 / 061600; A540 backing details"}
    canon['deflection_clips'] = {"none_reason": "deflection by 14 GA 2\" deep-leg slotted track (13/A540); no deflection clips called", "source": "13/A540"}
    # detalles: solo llaves N/HOJA; imagen resuelta; sealant (acústico EXCLUDED, U-053 / estimator standing order)
    NH = re.compile(r'^[0-9A-Z]{1,3}/[A-Z]{1,2}\d{3}[A-Z]?$')
    d2, dinfo = {}, {}
    for k, v in dets.items():
        v = dict(v) if isinstance(v, dict) else {"notes": str(v)}
        if not NH.match(k):
            dinfo[k] = v; continue
        v['source'] = k if not NH.search(str(v.get('source') or '')) else v['source']
        im = absimg(v.get('img')) or next((absimg(p) for p in glob.glob(f"{E}/2_lectura/*/img/*/*{k.split('/')[1].lower()}*{k.split('/')[0]}*.png")), None)
        if not im and os.path.exists(f'{W}/burbujas/burbujas_verificadas.json'):
            bd = json.load(open(f'{W}/burbujas/burbujas_verificadas.json')).get('_destinos', {}).get(k) or {}
            p = bd.get('img'); p = str(p).split(' #')[0] if p else None
            im = absimg(f'{W}/burbujas/{p}') if p else None
            if im and bd.get('title'):
                v.setdefault('title', bd['title'])
        if not im and k == '26/A530':
            im = f'{E}/4_canon/img/det/A530_26.png'; v['title'] = '26 ALUM. WINDOW SILL (exterior storefront at CMU wall with metal stud furring: 5/8" gyp bd returns over the furring to the frame)'
        if im:
            v['img'] = im
        v.setdefault('title', v.get('notes', '')[:80] or k)
        v.setdefault('notes', v.get('title'))
        v.setdefault('layers_per_face', 1); v.setdefault('layers_source', k)
        v['sealant_none_reason'] = "acoustical / joint sealant beads at head and base EXCLUDED (estimator standing order: acoustical sealant never carried; 079200 by others)"
        v['sealant'] = {"source": k, "runs": 0, "note": "excluded"}
        d2[k] = v
    dets.clear(); dets.update(d2)
    canon['details_info'] = dinfo
    L5p = f'{E}/2_lectura/A/L5.json'
    if os.path.exists(L5p):
        L5 = json.load(open(L5p))
        canon['constants']['level5_tags'] = {"value": ["WC-1"], "source": "A140",
                                             "source_info": "A140 general note 1 'PROVIDE LEVEL 5 FINISH AT WALLS TO RECEIVE WALL COVERING' + WC-1 schedule row 'DRYWALL SUBSTRATE TO BE FINISHED IN A LEVEL 5 FINISH' (spec 092900 3.6.D lists L1/L2/L4 only: the drawing governs, R-ALC-10)"}
        canon['level5_items'] = [{"ref": x['ref'], "wc_tag": "WC-1", "sf": x['sf'], "estado": "DERIVADO",
                                  "base_ft": {"value": 0, "source": "A142 / 5/A210, 6/A210: WC-1 drawn from the floor; the 4\" B-1 base (A140) is applied over the finished board, no base deduction (conservative)"},
                                  "source": f"{x.get('sheet')} ({x.get('wall')} side {x.get('side')}, {x.get('room')}): {x.get('op')}",
                                  "img": absimg(x.get('img'))} for x in L5['items'] + L5.get('ceiling_items', []) if x.get('sf')]
    canon['mep_sweep'] = {
        "sheets": ["M101", "M102", "M103", "M104", "M105", "M106", "M107", "M201", "M301", "P100", "P101", "P102", "P103", "P104", "P105", "P201", "P202", "P301", "E110", "E111", "E112", "E113", "E114", "E210", "E211", "E212", "E213", "E214"],
        "findings": ["M101-M106: ducts / air devices through walls = EXCLUDED by estimator standing order (R-ALC-03)",
                     "P101-P105 / P201-P202: restroom wet walls (Men 121 / Women 120 / Men 156 / Women 154 / Private RR 141) plumbing inside the stud cavity; no pipe crossing larger than the stud web punch-out drawn",
                     "E110-E214: wall devices / panels / boxes - no framing item drawn"],
        "source": "M101, P101, E111",
        "registro": {"no_usable": {"motivo": "A-sheets carry the text as curves and the M/P/E backgrounds a different lineweight: no automatic plan-to-MEP registration; ducts are EXCLUDED and no pipe crossing exceeds the stud punch-out, so no quantity depends on the crossing", "source": "M101, P101, A111", "img": "/root/gk/work/etapas/7_imagenes/mep_registro_M101.png"}}}
    canon['mep_penetrations'] = []
    canon['accesorios_none'] = [
        {"familia": "extra framing ATM", "why": "no ATM / recessed equipment in the set (A111, A112, A230, A231)", "source": "A111"},
        {"familia": "stud reinforcement MEP", "why": "no pipe / conduit crossing a stud wall larger than the stud web punch-out drawn on P101-P105 / E110-E214; ducts EXCLUDED by standing order", "source": "P101, E111"},
    ]
    AP = f'{E}/2_lectura/A/ACCESS.json'
    if os.path.exists(AP):
        canon['access_panels'] = [{"ref": x.get('ref') or f"AP-{i + 1}", "qty": int(x.get('count') or 1), "size": x.get('size'),
                                   "source": f"{x.get('sheet')} {x.get('location')} ({x.get('source')})", "img": absimg(x.get('img'))}
                                  for i, x in enumerate(json.load(open(AP)).get('access_panels') or []) if (x.get('in') or 'ceiling') in ('ceiling', 'wall')]
    canon['accesorios_none'].append({"familia": "gypsum board jamb return", "source": "26/A530, 12/A530",
        "why": "interior aluminum / HM frames: board stops at the frame with J mold (12/A530, 3/A530) = no jamb return; the 5/8\" gyp bd returns at the exterior windows in furred CMU walls (26/A530) are carried as board rows WR-01..WR-04 (gyp board family, exterior reading)"})
    canon['accesorios_none'].append({"familia": "2-1/2\" CFMF coiling grille head", "source": "15/A530, 18/A530",
        "why": "coiling grille heads: 'HEADER PER STRUCT.' (15/A530, 18/A530) = structural steel by others; the gyp bd soffit at the grille is carried as soffit SOF-12 (A131)"})
    canon['rfis'] = []
    for r in RF['rfis']:
        o = r.get('opciones') or {}
        dl = " | ".join(f"({k}) {v.get('delta')}" for k, v in o.items() if isinstance(v, dict)) or "0"
        b0 = r.get('barrido') or {}
        canon['rfis'].append({"id": r['id'], "status": r.get('status'), "source": r.get('source'), "question": r.get('question'),
                              "loaded": r.get('loaded'), "delta": dl, "img": absimg(r.get('img')),
                              "fuentes_revisadas": b0.get('swept_txt') or b0.get('specs'), "sources_checked": b0.get('sheets'),
                              "barrido": dict(b0, hojas="ALL", terminos=b0.get('terminos') or b0.get('terms') or [], grep=b0.get('swept_txt') or '')})
    GP = f'{E}/4_canon/gaps_ok.json'
    if os.path.exists(GP):
        canon['gaps_ok'] = [{"between": g['between'], "reason": f"{g.get('kind')}: {g.get('reason')}", "img": g.get('img')} for g in json.load(open(GP))]
    # U-175 / U-176: heights = final table of the two blind readings + directed A/B resolution (alturas/FINAL)
    import csv as _csv
    FH = '/root/gk/work/alturas/FINAL/ALTURAS_IMPRESAS.csv'
    HF = {r['Wall ID']: r for r in _csv.DictReader(open(FH, encoding='utf-8-sig'))} if os.path.isfile(FH) else {}
    import re as _re2
    for w in walls:
        r = HF.get(w['id'])
        if not r:
            continue
        h_old, h = float(w['height_ft']), round(float(r['Printed H']), 3)
        w['height_ft_prev_info'] = h_old
        w['height_ft'] = h
        w['height_op'] = r['Operation']
        _src = _re2.sub(r"y~(\d)", r"y \1", r['Source']).replace("~", "about ")   # no approximation sign in the source text (R73.14)
        _src = _src.replace("about 2.6 ft W", "2.6 ft west")
        _hs = sorted(set(_re2.findall(r"\b[A-Z]{1,2}\d{3}\b", r['Source'] + ' ' + r['Operation'])))
        _ch = _re2.search(r"C\.H\.\s*(\d+)-(\d+)\b", r['Operation'])
        w['height_source_info'] = f"{_src} [U-176 final table: blind readings H-A / H-B + directed resolution]"
        _pr = _re2.match(r"\s*(\d+)'-(\d+)\" \+ 0'-6\"", r['Operation'])
        if _pr and not _ch:
            _ch = _pr
        if _ch and abs(int(_ch.group(1)) + int(_ch.group(2)) / 12 + 0.5 - h) < 0.01:
            w['height_source'] = f"{', '.join(_hs) or 'A131'} printed ceiling {_ch.group(1)}'-{_ch.group(2)}\" + 6\" (A550 type: 6\" above ceiling) = {h}"
        else:
            w['height_source'] = f"{', '.join(_hs)}: [DERIVED] measured on the section that cuts the wall at its verified printed scale - operation in height_op (U-176 final table)"
        w['height_status'] = {"DERIVED": "DERIVADO", "CONFIRMED": "CONFIRMADO"}.get(r['Status'].strip().upper(), r['Status'])
        w['height_img'] = r['Image']
        if _re2.search(r"\)\s*/\s*\d+(\.\d+)?\b", r['Operation']) and _re2.search(r"(?i)underside|bottom of|U/S|B\.O\.|deck|joist|beam|truss|structure", r['Source']) \
                and not _re2.search(r"(?i)ceiling[^;]*\+\s*0?'?-?\s*6|\+ 0\.5\b", r['Operation']):
            w['structure_bo_ft'] = h        # the measured height IS the bottom of structure at this wall (BE-GK11)
        for f in w.get('faces') or []:
            fh = float(f.get('height_ft') or h_old)
            f['height_ft'] = round(min(fh, h), 3) if fh < h_old - 0.01 else h
            st = '[CONFIRMED]' if w['height_status'] == 'CONFIRMADO' else '[DERIVED]'
            f['height_source'] = f"{st} {w['height_source']}" if fh >= h_old - 0.01 else f"[DERIVED] {f.get('height_source')} (capped at wall H {h})"
    # face rooms -> printed room number of ALTURAS_CUARTOS (so the room cross-check of U-176 finds each room)
    FC = '/root/gk/work/alturas/FINAL/ALTURAS_CUARTOS.csv'
    ROOMS = [r['Room'].strip() for r in _csv.DictReader(open(FC, encoding='utf-8-sig'))] if os.path.isfile(FC) else []
    for w in walls:
        tt = str(w.get('top_track_info') or '')
        if 'braces to structure' in tt or 'PENDIENTE' in tt:
            w['top_track_info'] = _re2.sub(r"diagonal braces to structure \(A550 kn 7, S detail PENDIENTE\)", "diagonal braces anchored at the structure above (A550 kn 7, 8/A540, 62/S204 view A)", tt).replace('PENDIENTE', 'per 62/S204 view A')
        for f in w.get('faces') or []:
            rm = str(f.get('room') or '')
            if _re2.search(r"\b\d{3}[A-Z]?\b", rm):
                continue
            cand = sorted({x for x in ROOMS if len(x.split()) > 1 and _re2.search(r"\b" + _re2.escape(_re2.sub(r"^\d+[A-Z]?\s+", "", x).lower().rstrip('.')) + r"\b", rm.lower())})
            src = str(w.get('height_source') or '')
            if len(cand) > 1:
                cand = [x for x in cand if x.split()[0] in src] or cand
            if len(cand) == 1:
                f['room'] = f"{rm} {cand[0].split()[0]}"
    # gauge + bridging rows re-computed from the FINAL height of each wall (62/S204 printed table, then SFIA where it stops)
    import math as _m
    TAB = {'3-5/8"': [(13.833, '362S162-19', '62/S204'), (15.333, '362S162-33', '62/S204'), (16.667, '362S162-43', '62/S204'),
                      (20.5, '362S162-54', 'SFIA'), (21.917, '362S162-68', 'SFIA'), (24.167, '362S162-97', 'SFIA')],
           '6"': [(20.5, '600S162-19', '62/S204'), (22.75, '600S162-33', '62/S204'), (28.333, '600S162-43', 'SFIA')],
           '8"': [(32.167, '800S162-33', 'SFIA')],
           '2-1/2"': [(13.25, '250S162-33', 'SFIA'), (14.417, '250S162-43', 'SFIA')]}
    for w in walls:
        tb = TAB.get(str(w.get('stud_size')))
        if not tb or w.get('element', 'wall') != 'wall':
            continue
        h = float(w['height_ft'])
        hit = next((x for x in tb if h <= x[0] + 1e-6), None)
        if hit:
            mem, src = hit[1], hit[2]
            w['gauge'] = f"{mem} ({MILS_GA.get(mem.split('-')[-1], '')})"
            w['gauge_source'] = (f"{'62/S204 ALLOWABLE INTERIOR WALL HEIGHT (printed)' if src == '62/S204' else 'SFIA CCRR-0224 limiting heights, 5 psf, L/240 (A550 GN 1, 2024 IBC 2211; 62/S204 stops below this height)'}: "
                                 f"{w.get('stud_size')} @16\" o.c. at H {h:g} ft <= {hit[0]:g} ft -> {mem} (A550 keynotes 'SEE STRUCTURAL FOR GAUGE PER HEIGHT')")
        else:
            mem = HEAVY.get(w.get('stud_size'))
            w['gauge'] = f"{mem} ({MILS_GA.get(mem.split('-')[-1], '')}) - conservative, wall {h:g} ft taller than 62/S204 and the SFIA limiting heights: RFI-01"
            w['gauge_source'] = "62/S204 'ALLOWABLE INTERIOR WALL HEIGHT' + SFIA table (A550 GN 1, 2024 IBC) end below this height: heaviest member of the drawn stud depth loaded (RFI-01)"
        w['bracing_rows'] = max(1, _m.ceil(h / 5) - 1)
        w['bracing_rows_source'] = ("62/S204 note 2 'BLOCKED AT 5'-0\" O.C. MAX WHERE NOT SHEATHED EACH FACE' + A550 keynote 5 'BRIDGE STUDS AT MID-HEIGHT'"
                                    f": rows = max(1, ROUNDUP({h:g}/5)-1) = {w['bracing_rows']} of 1-1/2\" C.R. channel (A550 keynotes)")
    canon['rfi01_exceeds_info'] = sorted(w['id'] for w in walls if 'RFI-01' in str(w.get('gauge')))
    canon['heights_final_info'] = {"applied": sum(1 for w in walls if w['id'] in HF), "file": FH}
    for w in walls:
        if w['id'] == 'E-Z1-01':      # U-017: A111 prints 47'-4" for this wall (reader B); vector 46.92 (reader A)
            w['length_ft'] = 47.333; w['length_status'] = 'CONFIRMADO'; w['band']['hi'] = 1242.0
            w['length_source'] = "A111 printed dimension 47'-4\" (U-017: printed governs; vector band 815.9-1242.0 pt = 47.37 ft check)"; w['length_op'] = "printed 47'-4\" = 47.333"
        if w['id'] in ('A-Z1-04', 'F-Z1-05', 'C1-Z3-01', 'B-Z2-02'):   # printed strings of OTHER elements next to these walls
            ls = str(w.get('length_source') or '')
            w['length_check_info'] = f"nearby printed strings dimension another element (BE-49): {ls}"
            if '[ticks:' not in str(w.get('length_op')):
                w['length_op'] = f"{w.get('length_op')} [ticks: the nearby strings have SINGLE slash ticks and dimension another element; wall measured in vector, see the circled crop]"
            w['length_source'] = f"{(w.get('band') or {}).get('sheet') or w.get('sheet')} vector band at the printed scale (nearby strings belong to another element, see length_check_info)"
    canon['corners_fixed_info'] = fix_corners(walls, {k: v['value'] for k, v in canon['constants']['plan_scale_by_sheet'].items()})
    # dobles residuales: furring delgado (espesor de la banda <= tolerancia 0.25 ft): el V arranca exactamente en la cara del H
    import esquinas as Q
    co = []
    W_ = {w['id']: w for w in walls}
    for wa in walls:
        for wb in walls:
            ga, gb = Q.geo(wa) if wa.get('band') else None, Q.geo(wb) if wb.get('band') else None
            if not ga or not gb or ga['ori'] != 'H' or gb['ori'] != 'V' or Q.hoja(wa) != Q.hoja(wb):
                continue
            esc = canon['constants']['plan_scale_by_sheet'].get(Q.hoja(wa), {}).get('value', 9.0)
            e = Q._esquina(ga, gb, 0.25 * esc)
            if e and e[0] and e[1] and (abs(gb['lo'] - ga['c1']) < 0.05 or abs(gb['hi'] - ga['c0']) < 0.05):
                co.append({"walls": [wa['id'], wb['id']], "reason": f"single owner {wa['id']}: {wb['id']} starts exactly at the face of {wa['id']} (band edge {gb['lo'] if abs(gb['lo'] - ga['c1']) < 0.05 else gb['hi']} = face {ga['c1'] if abs(gb['lo'] - ga['c1']) < 0.05 else ga['c0']}); the furring thickness ({round(ga['c1'] - ga['c0'], 1)} pt) is inside the 0.25 ft tolerance, so the checker reads both as covering. No length is double counted."})
    for wa in walls:
        for wb in walls:
            ga, gb = Q.geo(wa) if wa.get('band') else None, Q.geo(wb) if wb.get('band') else None
            if not ga or not gb or ga['ori'] != 'H' or gb['ori'] != 'V' or Q.hoja(wa) != Q.hoja(wb):
                continue
            esc = canon['constants']['plan_scale_by_sheet'].get(Q.hoja(wa), {}).get('value', 9.0); tol = 0.25 * esc
            e = Q._esquina(ga, gb, tol)
            if not e or e[0] or e[1]:
                continue
            for wc in walls:
                gc = Q.geo(wc) if wc.get('band') and wc['id'] not in (wa['id'], wb['id']) and Q.hoja(wc) == Q.hoja(wa) else None
                if not gc:
                    continue
                if gc['ori'] == 'V' and abs(gc['c0'] - gb['c0']) <= tol and abs(gc['c1'] - gb['c1']) <= tol \
                        and gc['lo'] <= ga['c0'] + tol and gc['hi'] >= ga['c1'] - tol:
                    co.append({"walls": [wa['id'], wb['id']], "reason": f"corner square owned by {wc['id']} (collinear with {wb['id']}, same stud line, covers the square {ga['c0']}-{ga['c1']} pt); {wa['id']} ends at its face and {wb['id']} starts past it: one owner, nothing missing (R70.2)."})
                    break
                if gc['ori'] == 'H' and abs(gc['c0'] - ga['c0']) <= tol and abs(gc['c1'] - ga['c1']) <= tol \
                        and gc['lo'] <= gb['c0'] + tol and gc['hi'] >= gb['c1'] - tol:
                    co.append({"walls": [wa['id'], wb['id']], "reason": f"corner square owned by {wc['id']} (collinear with {wa['id']}, covers the square {gb['c0']}-{gb['c1']} pt): one owner, nothing missing (R70.2)."})
                    break
    _lk = lambda w: str(w.get('length_status')) == 'CONFIRMADO' or bool(re.search(r"(?i)printed (dim )?\d+'|\bdim \d+'-|2/A150 printed|^printed", str(w.get('length_source')) + ' ' + str(w.get('length_op'))))
    for wa in walls:
        for wb in walls:
            ga, gb = Q.geo(wa) if wa.get('band') else None, Q.geo(wb) if wb.get('band') else None
            if not ga or not gb or ga['ori'] != 'H' or gb['ori'] != 'V' or Q.hoja(wa) != Q.hoja(wb) or not (_lk(wa) and _lk(wb)):
                continue
            esc = canon['constants']['plan_scale_by_sheet'].get(Q.hoja(wa), {}).get('value', 9.0)
            e = Q._esquina(ga, gb, 0.25 * esc)
            if e and not e[0] and not e[1] and not any(set(x['walls']) == {wa['id'], wb['id']} for x in co):
                co.append({"walls": [wa['id'], wb['id']], "reason": f"both lengths are their own printed dimensions ({wa.get('length_source')} / {wb.get('length_source')}); printed dimensions govern (U-017) and run face to face, the corner square is the thickness of the meeting wall"})
    canon['corners_ok'] = co
    FI = json.load(open('/root/gk/work/indep/fichas.json'))
    # every bubble of the trade sheets gets a disposition (U-113 / U-137): what the take-off uses it for, or why it is not ours
    def _uso(dest):
        d = str(dest)
        if d == 'A520': return "sheet A520 is not in the set (README 'Missing sheet A520'); parapet framing from A310-A312 / S121 / S122 / S403 (ALC-03)"
        if d in ('A150',): return "enlarged restroom plans: Z3 / A111 restroom walls taken with these dimensions (ALC-01)"
        if d in ('A210', 'A211'): return "interior elevations: ceiling lines / heights read for the U-176 height table, Level 5 / DensShield extents (ALC-08, ALC-24)"
        if d in ('A220', 'A221'): return "window / frame elevations: openings, heads and sills in stud walls (ALC-05)"
        if d in ('A230', 'A231', 'A560'): return "casework elevations / schedule: casework by others, wood backing Div. 06 EXCLUDED (ALC-16)"
        if d in ('A300', 'A301'): return "building sections: wall and demolition heights (U-176 height table), exterior framing (ALC-02)"
        if d.startswith('A31'): return "wall sections: exterior CFS framing, sheathing, heights (ALC-02, ALC-09, U-176)"
        if d in ('A400', 'A401'): return "door schedule / hardware: openings and heads in stud walls (ALC-05)"
        if d == 'A510': return "floor / slab details: other trade"
        if d == 'A521': return "entry portal / storefront details: entry portal by GC (A111 keynote 41) EXCLUDED; framing at frame heads per 12/A530 (ALC-05)"
        if d in ('A530', 'A531'): return "door / window head, jamb and sill details: header track, J-mold (ALC-05, ALC-18)"
        if d == 'A540': return "interior details: bottom / deflection track, braces, ceilings, soffits, control joints (ALC-04, ALC-06, ALC-11, ALC-13, ALC-18)"
        if d == 'A550': return "wall construction types (ALC-01)"
        if d == 'A551': return "2-hour CMU wall U906: CMU other trade; Type X on the furring over it (ALC-22)"
        if d.startswith(('A11', 'A13', 'A14', 'A12')): return "key plan / match line to the partial plan: walls and ceilings taken on that sheet"
        if d.startswith('S'): return "structural: CFS members / allowable heights / braces used where printed (RFI-01, ALC-02, ALC-06)"
        return "other discipline: not metal framing / drywall"
    _cd = []
    for h_, xs_ in json.load(open('/root/gk/work/burbujas/burbujas_verificadas.json')).items():
        for x_ in xs_ if isinstance(xs_, list) else []:
            if isinstance(x_, dict) and x_.get('n') and x_.get('hoja'):
                ref_ = f"{x_['n']}/{x_['hoja']}"
                if not any(c_['ref'] == ref_ for c_ in _cd):
                    _u = _uso(x_['hoja'])
                    if x_['hoja'] == 'A521':     # callouts fork (eye-verified crops): only 2 / 3 / 6 are the entry portal
                        _u = ("entry portal by GC (A111 keynote 41) EXCLUDED (RI-32)" if str(x_['n']) in ('1', '2', '3', '6') else
                              "furring at expansion joint / material transition (G / F furring walls carried; 15/A521 control joint: RI-37)" if str(x_['n']) in ('8', '9', '14', '15', '18', '20') else
                              "exterior detail: framing at frame heads per 12/A530 (ALC-05), EIFS / sheathing (ALC-09)")
                    _cd.append({"ref": ref_, "from": h_, "use": _u})
    canon['callouts_disposition'] = _cd
    for w in walls:   # U-118: circled evidence crop per wall (scripts/img_walls.py)
        ip = f"/root/gk/work/etapas/7_imagenes/walls/{w['id']}.png"
        if os.path.isfile(ip):
            w['img'] = ip
            if isinstance(w.get('tag_manual'), dict):
                w['tag_manual']['img'] = ip
    _txt = json.dumps(canon, ensure_ascii=False)   # A520 is not in the set: no N/SHEET may point to it (BE-102)
    if '/A520' in _txt:
        canon.update(json.loads(re.sub(r"\b(\d+)/A520\b", r"detail \1 of the missing parapet sheet (README)", _txt)))
        walls = canon['walls']
    # U-168 A4 fixes counted by program from the drawings (revision_independiente/FIX_A4/fix_items.json, every op re-evaluated)
    FX = json.load(open('/root/gk/work/revision_independiente/FIX_A4/fix_items.json'))

    def _trim_img(t):     # evidence crop of each trim item: its own crop, else the door (op_<ref>) / soffit RCP crop, else the printed detail
        if t.get('img') and os.path.isfile(t['img']):
            return t['img']
        loc = str(t.get('location'))
        m = re.match(r"door (\w+)", loc)
        if m:
            for nm in (m.group(1), 'IE_132' if m.group(1) == '132' else ''):
                f = f"/root/gk/work/revision_independiente/FIX_A4/img/op_{nm}.png"
                if nm and os.path.isfile(f):
                    return f
            return "/root/gk/work/burbujas/img_verif/G2_A530_crops.png"
        m = re.match(r"(SOF-\d+)", loc)
        if m and os.path.isfile(f"/root/gk/work/alturas/FINAL/img/{m.group(1)}_A131.png"):
            return f"/root/gk/work/alturas/FINAL/img/{m.group(1)}_A131.png"
        return "/root/gk/work/burbujas/img_verif/G2_A530_crops.png" if 'A530' in str(t.get('source')) + loc else "/root/gk/work/burbujas/img_verif/G2_A540_crops.png"
    canon['trim_items'] = [{"ref": f"TRIM-{i:03d}", "kind": t['kind'], "lf": round(float(t['lf']), 2),
                            "source": f"{t['source']} | {t['location']} | op {t['op']}" + (f" | note: {t['flag']}" if t.get('flag') else ''),
                            "img": _trim_img(t)} for i, t in enumerate([t for t in FX['trim'] if float(t.get('lf') or 0) > 0 and 'NOT in the main total' not in str(t.get('flag'))], 1)]
    canon['trim_flagged_info'] = [f"{t['location']}: {t['lf']} LF ({t['flag']})" for t in FX['trim'] if 'NOT in the main total' in str(t.get('flag'))]
    canon['trim_none_reason'] = ''
    W_ = {w['id']: w for w in walls}
    for j in FX['wall_control_joints']:
        if float(j.get('lf') or 0) > 0:
            canon['misc_items'].append({"ref": f"WCJ-{j['wall']}", "familia": "control joint", "qty": round(float(j['lf']), 2),
                                        "op": j['op'], "source": f"{j.get('source')} | {j['wall']} ({j.get('basis')})", "detail": "7/A540"})
    for k, j in enumerate(FX['ceiling_control_joints'], 1):
        if 'ALREADY CARRIED' in str(j.get('status')) or float(j.get('lf') or 0) <= 0:
            continue
        canon['misc_items'].append({"ref": f"CCJ-{k:02d}", "familia": "control joint", "qty": round(float(j['lf']), 2), "op": j['op'],
                                    "source": f"{j.get('source')} | {j['ceiling']}: {j.get('what')} ({j.get('basis')})", "detail": "24/A540"})
    for o in FX['openings_missing']:
        w = W_.get(o['wall'])
        # door in the gap between two measured bands (the wall continues above the frame to the head of wall): the band of the
        # unlocked wall on the same line whose end touches the printed R.O. is extended across the R.O. (BE-GK17)
        mm = re.search(r"\(([\d.]+)-([\d.]+)\)/[\d.]+ = [\d.]+ at ([xy]) ([\d.]+)-([\d.]+)", o['source'])
        if mm:
            a_, b_ = sorted((float(mm.group(1)), float(mm.group(2)))); ori = 'H' if mm.group(3) == 'y' else 'V'
            c0_ = float(mm.group(4))
            names = re.findall(r"[A-Z]\d?-Z\d-\d+", o['wall'])
            cand = []
            for wid in names:
                x = W_.get(wid); bb = (x or {}).get('band') or {}
                if not x or bb.get('ori') != ori or abs(float(bb.get('c0', -99)) - c0_) > 0.6:
                    continue
                if abs(bb['hi'] - a_) <= 1.5 or abs(bb['lo'] - b_) <= 1.5:
                    cand.append(x)
            cand.sort(key=lambda x: (str(x.get('length_status')) == 'CONFIRMADO' or bool(re.search(r"(?i)printed (dim )?\d+'|\bdim \d+'-|2/A150 printed", str(x.get('length_source')))), not (x.get('tag_ids') or x.get('tag_box_ref_info')), x['length_ft']))
            wb = (w or {}).get('band') or {}
            dentro = bool(wb) and wb.get('ori') == ori and abs(float(wb.get('c0', -99)) - c0_) <= 0.6 and wb['lo'] - 1.5 <= a_ and b_ <= wb['hi'] + 1.5
            if cand and not dentro:
                w = cand[0]; bb = w['band']; esc = 9.0
                old_l = w['length_ft']
                if abs(bb['hi'] - a_) <= 1.5:
                    bb['hi'] = b_
                else:
                    bb['lo'] = a_
                w['length_ft'] = round((bb['hi'] - bb['lo']) / esc, 3)
                w['length_op'] = f"({bb['hi']}-{bb['lo']})/{esc:g} = {w['length_ft']} (band {old_l} ft + door {o['ref']} R.O. {a_}-{b_}: the wall continues above the frame, {o.get('note') or 'A111'})"
                w['length_check_info'] = (w.get('length_check_info') or '') + f" [door {o['ref']} R.O. added to the band: {o['source']}]"
                for y in W_.values():      # collinear wall of another type touching the new band end (R75.5 / R73.10)
                    yb = y.get('band') or {}
                    if y is w or yb.get('ori') != ori or yb.get('sheet') != bb.get('sheet') or abs(float(yb.get('c0', -99)) - c0_) > 0.6 or y.get('tag') == w.get('tag'):
                        continue
                    if abs(yb['lo'] - bb['hi']) <= 1.5 or abs(yb['hi'] - bb['lo']) <= 1.5:
                        dlf = round((b_ - a_) / 9, 2)
                        w['type_change_rfi'] = {"alternativas": [f"wall above door {o['ref']} = type {w.get('tag')} ({w['id']}, its tag box is the one next to the door on this line) - loaded",
                                                                 f"wall above door {o['ref']} = type {y.get('tag')} ({y['id']})"],
                                                "delta_lf": dlf, "source": f"A111 door {o['ref']}: no perpendicular wall drawn at the type change; R.O. {a_}-{b_} pt / 9 = {dlf} LF ({o.get('img') or ''})"}
        if not w or any(str(x.get('ref')) == str(o['ref']) for x in w.get('openings') or []):
            continue
        if float(w['length_ft']) < float(o['width_ft']) + 0.3:
            continue
        src = f"{o['source']}; head {o.get('header_detail')}"
        oc = opening_canon({"ref": o['ref'], "kind": o['kind'], "width_ft": o['width_ft'], "height_ft": o['height_ft'], "source": src,
                            "img": o.get('img'), "sill_ft": 0.0, "sill_source": f"{o['source'].split(';')[0]}: door frame to the floor (A400 frame elevation) = sill 0"}, w)
        w.setdefault('openings', []).append(oc)
    # 13/A540 BLOCKING STUD (one horizontal stud within 1'-0" of the deck on every full-height wall with the deflection head)
    _FAM = {'3-5/8"': '3-5/8" stud (todos los gauges)', '6"': '6" stud (todos los gauges)', '8"': '8" stud (todos los gauges)', '10"': '10" stud (todos los gauges)'}
    _blk = {}
    for w in walls:
        if w.get('tag') in ('A', 'A1', 'C', 'C1', 'E', 'E1') and str(w.get('top_track_kind')) == 'slip' and w.get('stud_size') in _FAM:
            _blk.setdefault(w['stud_size'], []).append(w)
    for sz, ws_ in sorted(_blk.items()):
        q = round(sum(float(x['length_ft']) for x in ws_), 2)
        canon['misc_items'].append({"ref": f"BLK-13A540-{sz.replace(chr(34), 'in')}", "familia": _FAM[sz], "qty": q,
                                    "op": " + ".join(f"{x['length_ft']:g}" for x in ws_) + f" = {q}",
                                    "source": f"13/A540 'BLOCKING STUD' 1'-0\" max. below the deck, 1 row per wall (A550 types A / C / E call 13/A540): {len(ws_)} walls {sz} ({', '.join(x['id'] for x in ws_)})",
                                    "detail": "13/A540"})
    # 7/A540 double framing member at every wall control joint: 2 studs x joint height = the CJ LF counted on both faces
    for m in [m for m in canon['misc_items'] if str(m['ref']).startswith('WCJ-')]:
        w = W_.get(m['ref'][4:])
        sz = (w or {}).get('stud_size')
        if sz in _FAM:
            canon['misc_items'].append({"ref": f"CJS-{m['ref'][4:]}", "familia": _FAM[sz], "qty": m['qty'], "op": f"{m['op']} (2 studs per joint x joint height = joint LF on both faces)",
                                        "source": f"7/A540 control joint: double framing member each side of the joint | {m['ref']} {m['source']}", "detail": "7/A540"})
    canon['corners_fixed_info'] = (canon.get('corners_fixed_info') or []) + (fix_corners(walls, {k: v['value'] for k, v in canon['constants']['plan_scale_by_sheet'].items()}) or [])   # bands extended over door R.O.s re-checked by R70.2
    _added = {str(x.get('ref')) for w in walls for x in w.get('openings') or []}
    _os = canon.get('opening_schedule') or {}
    _mov = [x for x in _os.get('none') or [] if set(re.split(r"[,/ ]+", str(x.get('ref')))) & _added]
    _os['none'] = [x for x in _os.get('none') or [] if x not in _mov]
    _os['items'] = [it for it in _os.get('items') or [] if not any(str(it.get('ref')) == str(x.get('ref')) for x in _mov)]
    for it in _os.get('items') or []:
        m_ = re.fullmatch(r"Door (\d+[A-Z]?)", str(it.get('ref')))
        if m_ and m_.group(1) in _added:
            it['ref'] = m_.group(1)
    _its = {str(it.get('ref')) for it in _os.get('items') or []}
    for r_ in sorted(_added):
        if r_ not in _its and not any(r_ in re.split(r"[,/ ]+", x) for x in _its):
            _os.setdefault('items', []).append({"ref": r_})
    canon['partition_schedule'] = [{"type": t, "source": f"46/A550 WALL CONST. TYPE {t} (independent reading, fichas.json)",
                                    "stud": v.get("stud"), "faces": len(v.get("faces") or [])} for t, v in FI['types'].items()]
    canon['wood_walls_none_reason'] = "A550 types A-H are metal-stud partitions (46/A550 keynotes 5 / 8 / 12 / 13); no wood-framed partition in the set (wood blocking / backing is Div. 06, EXCLUDED)"
    # demolition geometry in the canon (sheet = the demo plan, never the sheet of the height source, BE-CF19) + DETAIL with N/HOJA
    import re as _r
    DG = json.load(open(f'{E}/4_canon/demo_geom.json'))
    for g in DG:
        if g['id'] == 'DEMO-26' and abs(g['polyline'][0][0] - 1141.2) < 0.1:   # keynote 3 run only (keynote 4 window part west of it is another item)
            g['polyline'][0][0] = round(g['polyline'][1][0] - g['lf'] * 6.75, 1)
        if g['id'] in HF:          # U-176 final height table
            g['h_ft'] = round(float(HF[g['id']]['Printed H']), 3); g['sf'] = round(g['lf'] * g['h_ft'], 2)
            g['height_source'] = HF[g['id']]['Source']; g['h_status'] = f"{HF[g['id']]['Status']} - {HF[g['id']]['Operation']}"[:200]
        SEC_SHEET = {"A": "A300", "B": "A300", "C": "A300", "D": "A301", "E": "A301", "F": "A301"}   # section cut marks on A113 / A300 / A301
        sec = [x for x in dict.fromkeys(_r.findall(r"\b([A-F])-\1\b", str(g.get('height_source') or '')))]
        g['detail'] = f"{g.get('keynote') or g['sheet']}; height {', '.join(f'{a}/{SEC_SHEET[a]}' for a in sec) or g['sheet']}"
    json.dump(DG, open(f'{E}/4_canon/demo_geom_out.json', 'w'), indent=1)
    canon['demo_geom'] = DG
    for w in walls:   # F-Z1-12 (0.756 ft): the markup label prints 2 decimals; band end moved 0.04 pt (0.004 ft) so Length = LF label
        if w['id'] == 'F-Z1-12' and abs(float(w['length_ft']) - 0.756) < 1e-6:
            w['band']['hi'] = 322.04; w['length_ft'] = 0.76; w['length_op'] = "(322.04-315.2)/9 = 0.76 (band end 0.04 pt = 0.004 ft past the drawn line, label rounding)"
    canon['nodes'] = nodos(walls, {k: v['value'] for k, v in canon['constants']['plan_scale_by_sheet'].items()})
    byid = {w['id']: w for w in walls}
    for wa, wb, sh, p in TCH:
        byid[wa]['type_change_rfi'] = {
            "alternativas": [f"(A) as drawn: {byid[wa]['tag']} ends and {byid[wb]['tag']} starts at ({p[0]:.1f},{p[1]:.1f}) pt on {sh} (each side carries its own printed tag)",
                             f"(B) move the change to the next perpendicular wall face: 0 LF net (same line, only the stud size of the stretch changes)"],
            "delta_lf": 0.0, "source": f"{sh} tags {byid[wa]['tag']} / {byid[wb]['tag']} on the same line (resolution 3_revision)"}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    # every final length that differs from both blind readings A and B, with its decision (BE-63 / R80e.145)
    try:
        LA = {w['id']: w for w in json.load(open(f'{E}/2_lectura/canon_A.json'))['walls']}
        LB = {w['id']: w for w in json.load(open(f'{E}/2_lectura/canon_B.json'))['walls']}
        Lr = ["# Resolution of final lengths (rev1) - every wall whose final length differs from reading A and reading B", "",
              "| Wall | A | B | Final | Decision |", "|---|---|---|---|---|"]
        for w in walls:
            a, b_ = LA.get(w['id']), LB.get(w['id'])
            la = float(a['length_ft']) if a and a.get('length_ft') is not None else None
            lb = float(b_['length_ft']) if b_ and b_.get('length_ft') is not None else None
            lf_ = float(w['length_ft'])
            if all(x is None or abs(x - lf_) > 0.01 for x in (la, lb)):
                why = str(w.get('length_op') or '') + (' ' + str(w.get('length_check_info')) if 'R.O. added' in str(w.get('length_check_info')) else '')
                if b_ and (b_.get('band') or {}).get('c0') != (w.get('band') or {}).get('c0') and w['id'] == 'A1-Z1-05':
                    why += "; reader B's 'A1-Z1-05' (V band x 988, printed 9'-0\") is the canon wall A1-Z1-06 (9.0 ft printed), not this one"
                Lr.append(f"| {w['id']} | {la} | {lb} | {lf_} | {why[:400]} |")
        Lr += ["", "## Reader ID mapping (same ID, different element)", "",
               "| Wall | Note |", "|---|---|",
               "| A1-Z1-05 | reader B's 'A1-Z1-05' (V band x 988, Warranty 130 east wall, printed 9'-0\") is the canon wall A1-Z1-06 (9.0 ft printed); canon A1-Z1-05 is the Bus Mgr / File Stor wall (reader A 11.389) |"]
        open(f'{E}/3_revision/resolucion_largos_rev1.md', 'w').write("\n".join(Lr) + "\n")
        _rp = f'{E}/3_revision/resolucion.md'        # the gate reads resolucion.md: the final-lengths table goes there too (between markers)
        _rt = open(_rp).read() if os.path.isfile(_rp) else ""
        _rt = re.sub(r"\n<!-- FINAL LENGTHS rev1 -->.*?<!-- /FINAL LENGTHS rev1 -->\n", "\n", _rt, flags=re.S)
        open(_rp, 'w').write(_rt.rstrip() + "\n\n<!-- FINAL LENGTHS rev1 -->\n" + "\n".join(Lr) + "\n<!-- /FINAL LENGTHS rev1 -->\n")
    except (OSError, KeyError, ValueError):
        pass
    # BE-06: the soffits are carried as misc rows (board = developed width: exposed sides + bottom); declared here for the check
    canon['framed_soffits'] = [{"id": m_['ref'][:-6], "element": "soffit (misc rows)", "source": m_['source'][:300], "op": m_['op'],
                                "faces": [{"side": "exposed side(s)", "layers": 1}, {"side": "bottom", "layers": 1}],
                                "detail": str(m_.get('detail') or ''),
                                "note": "board = developed width of every exposed side + bottom (" + str(m_.get('detail') or '') + ")"}
                               for m_ in canon['misc_items'] if re.match(r"(SOF-\d+|EXT-0[78]) board$", m_['ref'])]
    for m_ in canon['misc_items']:      # BE-25: system detail of the exterior infill board (interior face per A310 kn 25)
        if m_['ref'] in ('EXT-02B board', 'EXT-03B board') and not m_.get('detail'):
            m_['detail'] = "2/A310 (kn 25), A200"
    _XM = '/root/gk/work/etapas/6_markups/extra_markups.json'    # DETAIL of the extra markups (verified N/HOJA) = DETAIL of their misc row
    if os.path.isfile(_XM):
        _nh = {x['id']: x.get('nhoja') for x in json.load(open(_XM))}
        for m_ in canon['misc_items']:
            k_ = m_['ref'][:-6] if m_['ref'].endswith(' board') else None
            if k_ in _nh and _nh[k_]:
                m_['detail'] = ", ".join(dict.fromkeys([x.strip() for x in (str(m_.get('detail') or '') + ', ' + _nh[k_]).split(',') if x.strip()]))
                if _nh[k_] not in str(m_.get('source')):
                    m_['source'] = f"{m_['source']} (markup on {_nh[k_]})"
    # U-177 (3): every stud / track misc row names its size + gauge designation with its source (never 'per source')
    _DS = re.compile(r"\d{3,4}[ST]\d{3}-\d{2}")
    _wd = {w['id']: (_DS.search(str(w.get('gauge'))) or [None])[0] for w in walls}
    _ext = {"EXT-01": "1000", "EXT-02": "1000", "EXT-03": "1000", "EXT-04": "600", "EXT-05": "362"}
    def _desig(m_):
        r_, f_ = m_['ref'], m_['familia']
        trk = 'track' in f_
        def T(d):
            return re.sub(r"^(\d{3,4})S(\d{3})-(\d{2})$", r"\1T125-\3", d) if trk else d
        mm = re.match(r"CJS-(.+)$", r_)
        if mm and _wd.get(mm.group(1)):
            return _wd[mm.group(1)], f"designation of wall {mm.group(1)} (gauge_source)"
        mm = re.match(r"(EXT-0[1-5]) (bottom|top) track", r_)
        if mm:
            return f"{_ext[mm.group(1)]}T125-43", f"track of the {_ext[mm.group(1)]}S162-43 studs printed for {mm.group(1)} (S121 / S122 / S403)"
        if r_.startswith(('EXT-02B', 'EXT-03B')):
            return "362S162-68", "gauge not printed (RFI-01): SFIA allowable-height table used for RFI-01, 362S162-68 <= 21'-11\" for H 21.0 ft"
        if r_.startswith(('RI-18', 'WINF-157')):
            return T("250S162-33"), "gauge not printed: 250S162-33 per the SFIA allowable-height table used for RFI-01 (H <= 13'-3\")"
        if r_.startswith(('SOF-', 'EXT-07', 'EXT-08', 'FAS-')):
            return T("362S162-33"), "gauge not printed: 362S162-33 per the 62/S204 allowable interior wall height table (15'-4\" at 16\" o.c. >= the short framing)"
        return None, None
    for m_ in canon['misc_items']:
        if re.search(r"stud|track", m_['familia'], re.I) and float(m_.get('qty') or 0) and not _DS.search(f"{m_['op']} {m_['source']}"):
            d_, why_ = _desig(m_)
            if d_:
                m_['source'] = f"{m_['source']} | {d_} ({why_})"
    # 13/A540 blocking studs: one row per wall designation (the gauge of the walls they brace)
    _nb = []
    for m_ in [x for x in canon['misc_items'] if x['ref'].startswith('BLK-13A540-')]:
        ids_ = re.findall(r"[A-H]1?-Z\d-\d{2}", m_['source'])
        grp = {}
        for i_ in ids_:
            grp.setdefault(_wd.get(i_) or 'none', []).append(i_)
        for d_, ws_ in grp.items():
            q_ = round(sum(float(W_[i_]['length_ft']) for i_ in ws_), 2)
            _nb.append(dict(m_, ref=f"{m_['ref']}-{d_}", qty=q_, op=" + ".join(f"{W_[i_]['length_ft']:g}" for i_ in ws_) + f" = {q_}",
                            source=f"13/A540 'BLOCKING STUD' 1'-0\" max. below the deck, 1 row per wall: {d_} = designation of walls {', '.join(ws_)}"))
    if _nb:
        canon['misc_items'] = [x for x in canon['misc_items'] if not x['ref'].startswith('BLK-13A540-')] + _nb
    # U-176 height protocol: per-wall overrides from the height review (alturas/FINAL/canon_patch.json), applied last
    _cp = '/root/gk/work/alturas/FINAL/canon_patch.json'
    if os.path.isfile(_cp):
        _PW = json.loads(re.sub(r"(?<=y)~(?=\d)", " ", re.sub(r"~(\d+\.?\d*) ft", r"\1 ft (measured)", open(_cp).read())))   # E27: no '~' in a source
        _PW = _PW.get('walls') or {}
        for w in canon['walls']:
            for k_, v_ in (_PW.get(w['id']) or {}).items():
                if k_ == 'faces' and isinstance(v_, dict):
                    for i_, fv in v_.items():
                        if int(i_) < len(w.get('faces') or []):
                            w['faces'][int(i_)].update(fv)
                else:
                    w[k_] = v_
    json.dump(canon, open(OUT, 'w'), indent=1, ensure_ascii=False)
    import collections
    c = collections.Counter(); lf = collections.Counter()
    for w in walls:
        c[w['tag']] += 1; lf[w['tag']] += float(w.get('length_ft') or 0)
    print({k: (c[k], round(lf[k], 1)) for k in sorted(c, key=lambda x: ORDER.index(x) if x in ORDER else 99)})




def nodos(walls, esc_by_sheet):
    """Nodos por geometría de bandas (programa, no lectura). Cada EXTREMO de cada wall queda en UN nodo: dos extremos
    que se tocan = L (perpendiculares) o split (colineales, mismo stud; si cambia el stud = free cada uno); un extremo
    que toca el cuerpo de un wall perpendicular = T (branch / through); si no = free (CMU / existente / storefront /
    remate). Tolerancia 9 pt + medio espesor."""
    def geo(w):
        b = w['band']; c0, c1, lo, hi = (float(b[k]) for k in ('c0', 'c1', 'lo', 'hi'))
        if c1 - c0 > hi - lo:
            c0, c1, lo, hi = lo, hi, c0, c1
        return b.get('ori'), (c0 + c1) / 2, lo, hi, (c1 - c0)
    G, SZ = {}, {w['id']: w.get('stud_size') for w in walls}
    for w in walls:
        if isinstance(w.get('band'), dict) and w['band'].get('ori') in ('H', 'V'):
            G[w['id']] = (w['band'].get('sheet') or w.get('sheet'),) + geo(w)
    def P(g, v):
        sh, o, c, lo, hi, t = g
        return (v, c) if o == 'H' else (c, v)
    E = []
    for wid, g in G.items():
        E.append((wid, 0, P(g, g[3]))); E.append((wid, 1, P(g, g[4])))
    TOL = 9.0
    pares = []
    for a in range(len(E)):
        for b in range(a + 1, len(E)):
            wa, _, pa = E[a]; wb, _, pb = E[b]
            if wa == wb or G[wa][0] != G[wb][0]:
                continue
            ta, tb = G[wa][5], G[wb][5]
            d = max(abs(pa[0] - pb[0]), abs(pa[1] - pb[1]))
            if d <= TOL + (ta + tb) / 2:
                pares.append((d, a, b))
    pares.sort()
    usado, out = set(), []
    global TCH
    TCH = []
    def add(n):
        n.update(id=f"N{len(out) + 1}", source=f"{n.pop('_sh')} vector bands (resolved canon, program build_canon.nodos)")
        out.append(n)
    for d, a, b in pares:
        if a in usado or b in usado:
            continue
        wa, wb = E[a][0], E[b][0]; sh = G[wa][0]
        usado |= {a, b}
        if G[wa][1] != G[wb][1]:
            add({"kind": "L", "walls": [wa, wb], "_sh": sh})
        elif SZ.get(wa) == SZ.get(wb):
            add({"kind": "split", "walls": [wa, wb], "_sh": sh})
        else:
            for w_, o_ in ((wa, wb), (wb, wa)):
                add({"kind": "free", "wall": w_, "_sh": sh, "source_info": f"collinear stud-size change {w_} / {o_}: own end stud"})
            TCH.append((wa, wb, sh, E[a][2]))
    for k, (wid, e, p) in enumerate(E):
        if k in usado:
            continue
        sh, o = G[wid][0], G[wid][1]
        hit = None
        for wid2, g2 in G.items():
            if wid2 == wid or g2[0] != sh or g2[1] == o:
                continue
            _, o2, c2, lo2, hi2, t2 = g2
            x, y = p
            along, perp = (x, y) if o2 == 'H' else (y, x)
            if lo2 - TOL <= along <= hi2 + TOL and abs(perp - c2) <= t2 / 2 + TOL + G[wid][5] / 2:
                hit = wid2; break
        if hit:
            add({"kind": "T", "branch": wid, "through": hit, "_sh": sh})
        else:
            add({"kind": "free", "wall": wid, "_sh": sh, "source_info": f"{sh}: end at ({p[0]:.1f},{p[1]:.1f}) pt meets no other new stud wall (CMU / existing / storefront / open end)"})
    return out

if __name__ == '__main__':
    main()
