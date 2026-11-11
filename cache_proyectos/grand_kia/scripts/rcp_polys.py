"""Grand Kia: etapas/6_markups/rcp_polys.json (misc: polígonos de cielos / líneas de soffits de misc_gen) y
etapas/4_canon/rcp_cuartos.json (cada cuarto impreso de cada RCP A130-A133: renglón del take-off o EXCLUDED con su motivo
impreso N/HOJA, U-159 / U-160). Polígonos = los del lector de cielos (vectores del RCP a la escala impresa), sin ajustes."""
import json, os
import re
NH_ = re.compile(r"\b[0-9]{1,2}/[A-Z]{1,2}-?\d{3}\b")


def _nh(s, m):      # DETAIL of a soffit line = its printed N/HOJA (soffit detail, else the framed gyp bd system of the misc row) + sheet
    d = [x for x in (s.get('detail') or []) if NH_.search(x)] or NH_.findall(str(m.get('detail') or '')) or ['12/A540']
    extra = [x for x in (s.get('detail') or []) if not NH_.search(x)]
    return ', '.join(dict.fromkeys(d + extra + [s['sheet']]))



def _tramos(pts):      # CB_U_120: one markup per axis - a drawn run that turns (closed light-cove loop) is split where it turns > 45 deg
    import math
    if len(pts) < 3:
        return [pts]
    out, cur, h0 = [], [pts[0], pts[1]], math.atan2(pts[1][1] - pts[0][1], pts[1][0] - pts[0][0])
    for a, b in zip(pts[1:], pts[2:]):
        h = math.atan2(b[1] - a[1], b[0] - a[0])
        d = abs((h - h0 + math.pi) % (2 * math.pi) - math.pi)
        if d > math.radians(45) and math.dist(a, b) > 0:
            out.append(cur); cur = [a, b]; h0 = h
        else:
            cur.append(b)
    out.append(cur)
    return [t for t in out if sum(math.dist(p, q) for p, q in zip(t, t[1:])) > 0.5]

W = '/root/gk/work'
C = json.load(open(f'{W}/etapas/2_lectura/A/CEILINGS.json'))
MG = json.load(open(f'{W}/etapas/4_canon/misc_gen.json'))
os.makedirs(f'{W}/etapas/6_markups', exist_ok=True)
DENS_ = {m['ref'].replace(' board', '') for m in MG['misc_items'] if m['ref'].endswith(' board') and 'Dens' in m['familia']}
P = []
for r in MG['rcp_rows']:
    P.append({"misc": True, "id": r['ref'], "sheet": r['sheet'], "kind": "area", "polygons": [p for p in r['polys'] if p],
              "sf": r['area_sf'], "layers": 1, "board": ('5/8" glass mat water-resistant tile backer (DensShield, ASTM C1178)' if r['ref'] in DENS_ else '5/8" GYPSUM BOARD'),
              "cause": f"{r['system']} gyp bd ceiling {r.get('height') or ''}", "nhoja": {"suspended": f"24/A540, {r['sheet']}", "framed": f"12/A540, 64/S204, {r['sheet']}"}.get(r['system'], f"{r['sheet']} existing joists (board only), 24/A540")})
DEV = {m['ref'].replace(' board', ''): m for m in MG['misc_items'] if m['ref'].startswith('SOF-') and m['ref'].endswith(' board')}
_GL = json.load(open(f'{W}/revision_independiente/FIX_RCP/geom.json'))
_hd = _GL['polys_tech_parts']['pgb_lines'][0]
C['soffits'].append({"id": "SOF-18", "sheet": "A131", "lf": _hd['lf'], "line": _hd['lines'][0], "line2": _hd['lines'][1], "kind": "gyp bd header", "detail": ["A131 keynote 19"]})
for s in C['soffits']:
    g_ = _GL['lines'].get(s['id'])
    if g_:      # vector re-measure (U-168 A3): drawn line(s) and their LF
        ls_ = g_['lines'] if g_['lines'] and isinstance(g_['lines'][0][0], list) else [g_['lines']]
        if len(ls_) == 2 and all(abs(a - b) < 1.0 for a, b in zip(sorted(q[0] for q in ls_[0]), sorted(q[0] for q in ls_[1]))):
            ls_ = ls_[:1]      # two parallel faces of the same element: the LF is one face (the developed width is in Depth)
        s = dict(s, line=ls_[0], line2=None, lines_all=ls_, lf=g_['lf_measured'])
    m = DEV.get(s['id'])
    if not m or not s.get('line'):
        continue
    lf = float(s['lf']); dep = round(m['qty'] / lf, 3)
    s = dict(s, lines_all=[q for ln in (s.get('lines_all') or [x for x in (s['line'], s.get('line2')) if x]) for q in _tramos(ln)])
    P.append({"misc": True, "id": s['id'], "sheet": s['sheet'], "kind": "line", "lines": s.get('lines_all') or [x for x in (s['line'], s.get('line2')) if x], "lf": lf, "depth_ft": dep,
              "board": '5/8" GYPSUM BOARD', "cause": f"{s.get('kind')} developed width {dep}", "nhoja": _nh(s, m)})
_XM = f'{W}/etapas/6_markups/extra_markups.json'     # board items off the RCP (elevations, furring, returns): geometry fork, crops verified
if os.path.isfile(_XM):
    P += json.load(open(_XM))
json.dump(P, open(f'{W}/etapas/6_markups/rcp_polys.json', 'w'), indent=1)
refs = {(r['sheet'], str(r['number']), r['room']): r['ref'] for r in MG['rcp_rows']}
rooms = []
for x in C['ceilings']:
    sh = x['sheet']; key_sheet = x.get('source_row_sheet') or sh
    ref = refs.get((key_sheet, str(x.get('number')), x['room'])) or refs.get(('A131', str(x.get('number')), x['room'])) \
        or refs.get(('A132', str(x.get('number')), x['room']))
    rooms.append({"sheet": sh, "room": str(x.get('number') or x['room']), "name": x['room'], "disposition": "row",
                  "rows": [ref] if ref else [], "polygon": x.get('poly'), "area_sf": x.get('area_sf'),
                  "note": "A130 = overall view of the same room (row counted once on the partial RCP)" if sh == 'A130' else ""})
for x in C['excluded_rooms']:
    reason = str(x.get('excluded_reason') or '')
    R = reason.upper()
    txt = ("ACT acoustical ceiling tile and grid per RCP tag - not our trade" if R.startswith("ACT") else
           "open to structure, no ceiling per RCP" if "OPEN TO STRUCTURE" in R else
           "no ceiling tag or ceiling hatch printed in this room = no ceiling (U-162)" if "NO CEILING TAG" in R else
           "existing ceiling to remain, no new ceiling tag" if "EXISTING" in R else reason)
    rooms.append({"sheet": x['sheet'], "room": str(x.get('number') or x['room']), "name": x['room'], "disposition": "exclusion",
                  "rows": [], "reason": txt or reason, "nhoja": (x.get('excluded_source') or x['sheet'])[:120],
                  "polygon": x.get('poly'), "area_sf": x.get('area_sf')})
# 146 EV REPAIR / 147 EV BAY: labels inside SERVICE 145 (no enclosing walls): EXCLUDED box around the printed label
# (label position from the OCR text layer converted to the visible frame)
LBL = {('A130', '147'): (1016.6, 1241.4), ('A130', '146'): (1016.8, 1323.4), ('A132', '147'): (936.2, 813.6), ('A132', '146'): (936.4, 922.6)}
for r in rooms:
    k = (r['sheet'], r['room'])
    if k in LBL and not r.get('polygon'):
        cx, cy = LBL[k]
        r['polygon'] = [[cx - 45, cy - 30], [cx + 45, cy - 30], [cx + 45, cy + 30], [cx - 45, cy + 30]]
        r['note'] = 'label inside SERVICE 145 (open to structure, A132 tag EXP. STRUCT. P-1): box around the printed room label'
json.dump({"rooms": rooms, "meta": {"source": "2_lectura/A/CEILINGS.json (every printed room of A130-A133)"}},
          open(f'{W}/etapas/4_canon/rcp_cuartos.json', 'w'), indent=1)
print(len(P), 'misc polys;', len(rooms), 'rooms;', sum(1 for r in rooms if r['disposition'] == 'exclusion'), 'exclusions;',
      [r['room'] for r in rooms if r['disposition'] == 'row' and not r['rows']])

# exclusions measured by the review (U-168 A3, FIX_RCP/geom.json): Tech Parts 134 (ACT + exposed structure) and the open A132 areas
_G = json.load(open(f'{W}/revision_independiente/FIX_RCP/geom.json'))
for e in _G['excluded']:
    rid = {'EX-A131-134S': '134', 'EX-A131-134N': '134-N'}.get(e['id'], e['id'].replace('EX-', ''))
    rooms = [r for r in rooms if not (r['sheet'] == e['sheet'] and r['room'] == rid)]
    rooms.append({"sheet": e['sheet'], "room": rid, "name": e['area'][:60], "disposition": "exclusion", "rows": [],
                  "reason": (("ACT acoustical ceiling tile and grid per RCP tag - not our trade / " if 'ACT' in e['tag'] else '') +
                             ("open to structure, no ceiling per RCP ('EXP. STRUCT. P-1')" if 'EXP' in e['tag'] else
                              "no ceiling tag or ceiling hatch printed in this area = no ceiling (U-162)")),
                  "nhoja": e['sheet'], "polygon": e['poly'], "area_sf": e['area_sf']})
for r in rooms:      # A130 overall RCP: Tech Parts 134 is the A131 exclusion (drawn on A131)
    if r['sheet'] == 'A130' and r['room'] == '134' and not r.get('rows'):
        b_ = next(x for x in rooms if x['sheet'] == 'A131' and x['room'] == '134')
        r.update({k: v for k, v in b_.items() if k not in ('sheet',)}, draw_sheet='A131', note='A130 overall view: exclusion drawn on the partial RCP A131')
# U-159 on every sheet the gate reads as RCP-related (A sheets citing the RCP): each printed room number either maps to its
# RCP disposition (same row / same exclusion drawn on the RCP sheet = draw_sheet) or is declared not_a_room with the printed
# context and a circled crop (title-block address 850, keynote / dimension numbers).
import sys, re
sys.path.insert(0, '/root/gk/skill/take-off-metal-frame-drywall/tools')
import compuerta_entrega as _CE, pymupdf as _f
from PIL import Image as _I, ImageDraw as _D
_H = json.load(open(f'{W}/set_texto.json'))['hojas']
_hc = _CE.cuartos_rcp(_H)
_sm = json.load(open(f'{W}/sheetmap.json'))
_doc = _f.open(f'{W}/plans/GK_set_OCR.pdf')
_by = {}
for r in rooms:
    if r['sheet'] in ('A131', 'A132', 'A133'):
        _by.setdefault(r['room'], r)
_have = {(r['sheet'], r['room']) for r in rooms}
os.makedirs(f'{W}/etapas/7_imagenes/no_room', exist_ok=True)
_add = 0
for h, rs in _hc.items():
    for n in rs:
        if (h, n) in _have:
            continue
        base = _by.get(n)
        if base and h not in ('A131', 'A132', 'A133', 'A130'):
            x = dict(base, sheet=h, draw_sheet=base.get('draw_sheet') or base['sheet'],
                     note=f"room {n} printed on {h}; its ceiling is taken on RCP {base['sheet']} ({base.get('disposition')})")
            rooms.append(x); _add += 1
            continue
        pg = _doc[_sm[h] - 1]
        ws = [_f.Rect(w[:4]) * pg.rotation_matrix for w in pg.get_text('words') if w[4].strip('.,()') == n]
        txt = str(_H.get(h) or '')
        i = txt.find(n)
        ctx = ' '.join(txt[max(0, i - 60):i + 60].split()) if i >= 0 else ''
        img = ''
        if ws:
            r_ = ws[0]; clip = _f.Rect(r_.x0 - 80, r_.y0 - 50, r_.x1 + 80, r_.y1 + 50) & pg.rect
            pix = _f.open(f'{W}/plans/GK_set_SIN_MARKUPS.pdf')[_sm[h] - 1].get_pixmap(clip=clip, matrix=_f.Matrix(2, 2))
            im = _I.frombytes("RGB", (pix.width, pix.height), pix.samples); d = _D.Draw(im)
            d.ellipse([(r_.x0 - clip.x0 - 12) * 2, (r_.y0 - clip.y0 - 12) * 2, (r_.x1 - clip.x0 + 12) * 2, (r_.y1 - clip.y0 + 12) * 2], outline=(255, 0, 0), width=4)
            img = f'{W}/etapas/7_imagenes/no_room/{h}_{n}.png'; im.save(img)
        why = ("title block: architect address '850 W. ELLIOT RD' (John Mahoney Architect), not a room" if n == '850' else
               f"printed number '{n}' is not a room label on {h} (context: '{ctx[:110]}')")
        rooms.append({"sheet": h, "room": n, "name": "", "disposition": "not_a_room", "reason": why, "nhoja": h, "img": img, "rows": []}); _add += 1
# CR-R15-CONTORNO: outlines whose edge the sheet does not draw, with the printed reason (eye-checked crops, 11-nov)
_EDGE = {'146': "open bay inside SERVICE 145, no wall or ceiling line drawn around it; box drawn around the printed room label",
         '147': "open bay inside SERVICE 145, no wall or ceiling line drawn around it; box drawn around the printed room label",
         '159': "the RCP draws the room walls dashed / double; the outline follows their inner face",
         '134': "the EXP. STRUCT. zone of TECH PARTS 134 is bounded by the PGB ceiling lines N / S and open to the rest of the room E / W"}
_P145 = {r_['sheet']: r_.get('polygon') for r_ in rooms if str(r_.get('room')) == '145' and r_.get('polygon')}
for r_ in rooms:      # U-177 (2): EV REPAIR 146 / EV BAY 147 are open bays INSIDE SERVICE 145: their outline = the drawn walls of 145
    if str(r_.get('room')) in ('146', '147') and r_.get('disposition') == 'exclusion' and _P145.get(r_['sheet']):
        r_['polygon'] = _P145[r_['sheet']]
        r_['note'] = "open bay inside SERVICE 145 (no own walls): excluded outline = the SERVICE 145 walls (A132 'EXP. STRUCT. P-1')"
_EDGE.pop('146', None); _EDGE.pop('147', None)
for r_ in rooms:
    k_ = str(r_.get('room'))
    if r_.get('disposition') == 'exclusion' and k_ in _EDGE and '[EDGE NOT DRAWN' not in str(r_.get('reason')):
        r_['reason'] = f"{r_['reason']} [EDGE NOT DRAWN: {_EDGE[k_]}]"
json.dump({"rooms": rooms, "meta": {"source": "2_lectura/A/CEILINGS.json + every A sheet citing the RCP (U-159)"}}, open(f'{W}/etapas/4_canon/rcp_cuartos.json', 'w'), indent=1)
print(_add, 'room entries added for RCP-citing sheets')
