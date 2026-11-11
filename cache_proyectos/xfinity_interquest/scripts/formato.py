"""Input-format of the resolved canon for canon.py (Xfinity Interquest), by program; each change recorded (_info).
- column furring CF-01/02 -> element column_wrap (5/A2.0), faces_ft from the vector outline;
- SOF-01 (8'-6" gyp header, no system detail) -> misc_items with its framing / board (RFI-02 closed) instead of a
  ceiling (canon.py R70.1 requires a ceiling system callout; the header is a framed box like type W2).
Use: python3 -I scripts/formato.py"""
import json, math
K = '/root/xf/work'; P = f'{K}/etapas/4_canon/takeoff_canon.json'
c = json.load(open(P))
for w in c['walls']:
    if w['id'].startswith('CF'):
        f = w.pop('furring_outline_ft')
        w['element'] = 'column_wrap'; w['stud_size'] = '2-1/2"'
        w['band'] = dict(w['band'], ori='BOX'); w['band_length_ok_reason'] = 'column wrap footprint (BOX): length_ft = exposed perimeter of the 3 furred sides (0.94 + 0.72 + 0.72)'
        w['faces_ft'] = [f['west_face'], f['north_face'], f['south_face']]
        w['faces_ft_source'] = "A2.0 vector furring outline (3 exposed sides; 4th side against the existing storefront pier) - 5/A2.0"
        w['faces'] = [dict(w['faces'][0], side='A')]
        for k in ('column_in', 'sides_furred'):
            if k in w: w[k + '_info'] = w.pop(k)
# SOF-01 -> misc
s = next((x for x in c.get('ceilings', []) if x['ref'] == 'SOF-01'), None)
if s:
    L = 4.247
    n_st = math.ceil(L / (16 / 12)) + 1
    items = [
     {"ref": "SOF-01-TRACK", "familia": "track de ceilings / soffits", "qty": round(4 * L, 3), "unit": "LF", "source": "A3.0 'GYP. BD. 8'-6\" AFF' strip; framing as type W2 (2/A2.0, RFI-02 closed)",
      "op": f"header box: 2 bottom tracks (both faces at 8'-6\") + 2 top tracks = 4 x {L} = {round(4*L,3)} LF 3-5/8\" track", "status": "DERIVADO"},
     {"ref": "SOF-01-STUDS", "familia": "3-5/8\" stud (todos los gauges)", "qty": round(n_st * 2.0 + n_st * 1.0, 3), "unit": "LF", "source": "A3.0; 2/A2.0 W2 framing @16\" o.c.",
      "op": f"ROUNDUP({L}/1.333)+1 = {n_st} studs storage face 8.5->10.5 (2.0 ft) + {n_st} studs hallway face 8.5->9.5 (1.0 ft) = {n_st*3.0} LF", "status": "DERIVADO"},
     {"ref": "SOF-01-BOARD", "familia": "5/8\" gyp board Type X", "qty": round(1.727 + 2.0 * L + 1.0 * L, 2), "unit": "SF", "source": "A3.0 '5/8\" TYPE X GYPSUM BOARD CEILING' legend + A3.0 8'-6\" tag; A2.0 legend 6\" above ceiling",
      "op": f"underside 1.727 (A3.0 vector 76.44 x 7.32 pt / 324) + storage face 2.0 x {L} + hallway face 1.0 x {L} = {round(1.727+3.0*L,2)} SF", "status": "DERIVADO"},
    ]
    c['misc_items'] += items
    c['trim_items'] = [t for t in c.get('trim_items', []) if t['ref'] != 'CB-SOF-01'] + [
     {"ref": "CB-SOF-01", "kind": "corner_bead", "lf": round(2 * L, 3), "label": "SOF-01 header: two bottom edges", "source": "A3.0", "op": f"2 x {L} = {round(2*L,3)}", "status": "DERIVADO"}]
    c['ceilings'] = [x for x in c['ceilings'] if x['ref'] != 'SOF-01']
    c['soffit_header_info'] = {k: s[k] for k in ('ref', 'type', 'room', 'sheet', 'band', 'area_sf', 'area_source', 'area_op', 'height_ft', 'height_source', 'img', 'height_img') if k in s}
    c['ceilings_info'] = (c.get('ceilings_info') or '') + " | SOF-01 8'-6\" gypsum header at the north end of Hallway 102: carried as misc items SOF-01-TRACK / STUDS / BOARD + CB-SOF-01 (framing as type W2, RFI-02 closed)."
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
print('ok', [w['id'] for w in c['walls']], len(c['ceilings']))
# --- wall schema fields (canon.py), W2 walls ---
c = json.load(open(P))
for w in c['walls']:
    for k in ('bracing', 'insulation', 'level_of_finish', 'openings', 'height_img_extra'):
        if k in w: w[k + '_info'] = w.pop(k)
    w.setdefault('status', w.get('length_status', 'DERIVADO'))
    if w['id'].startswith('W2'):
        w['source'] = "W2 (2/A2.0 wall types) on A2.0 1/A2.0"
        w['length_basis'] = "face of existing construction to face (A2.0 dimension strings; wall measured through the door R.O.)"
        w['bracing_rows'] = 0; w['bracing_rows_source'] = "2/A2.0, 3/A2.0, 4/A2.0"
        w['bracing_rows_info'] = "no bridging / C.R. channel row printed; 4/A2.0 kicker braces to structure carried in misc_items BRACE-*"
        w['top_track_kind'] = 'standard'
        w['top_track_kind_source'] = "4/A2.0 'TOP OF TRACK SECURED TO STUDS WITH #8 SHEET METAL SCREW EACH FLANGE' - wall stops 6\" above ceiling, braced to structure (no deflection / slip track printed)"
        w['track_gauge'] = '20 ga'
        w['track_gauge_source'] = "4/A2.0 'MATCH WALL STUD SIZE & GAUGE (3 5/8\" 20 GA. MIN.)' (track = stud gauge)"
    else:
        w['source'] = "5/A2.0 NON-RATED COLUMN FURRING + A2.0 key note 1"
        w['top_track_kind'] = 'standard'; w['top_track_kind_source'] = "5/A2.0 furring to 6\" above ceiling (key note 1)"
        w['bracing_rows'] = 0; w['bracing_rows_source'] = "5/A2.0"
k = c['constants']
k.pop('sheet_len_ft', None)
k['type_order'] = {"value": ["W1", "W2", "W2A", "W3", "W4"], "source": "2/A2.0 WALL TYPES (printed order: 1, 3, 2, 2A, 4 boxes; numbered order used)"}
k['rcp_sheet'] = {"value": "A3.0", "source": "1/A3.0"}
k['partition_row_rule'] = {"value": "wall_id", "source": "A2.0 wall ids: one Partition Takeoff row per wall, the same ids as the markups"}
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# --- opening schedule ---
c = json.load(open(P)); o = c['opening_schedule']
o['sources'] = ["A2.0", "A1.0", "A3.0", "E2.0", "M1.0", "P1.0"]
o['sources_none'] = {"S": "no structural (S) sheet in the set: A0.1 SHEET INDEX lists A0.1-A5.0, E0.0-E3.0, M0.0-M2.0, P1.0 only"}
none = []; items = []
for it in o['items']:
    if it['ref'] == 'Door 101':
        it.update(kind='door', ro_w_ft=3.0, head_ft=7.167, wall='W2-01', in_new_wall=True,
                  head_ft_source="A2.0 door schedule 7'-0\" + 2\" HM frame head (A0.3 hollow metal frames 16 GA; frame head depth 2\" typical) - DERIVADO",
                  ro_status="CONFIRMADO width (A2.0 '3'-0\" DOOR'); head DERIVADO")
        items.append(it)
    else:
        none.append({"ref": it['ref'], "why": it.get('note') or 'existing door in existing construction to remain: no new framing'})
o['items'] = items; o['none'] = none
o['note'] = "Only door 101 is new and sits in new wall W2-01 (wall measured through the R.O.)"
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# --- door 101 in W2-01 (canon.py builds jambs / head / cripples) ---
c = json.load(open(P))
w = next(x for x in c['walls'] if x['id'] == 'W2-01')
w['openings'] = [{"ref": "Door 101", "kind": "door", "ro_w_ft": 3.0, "head_ft": 7.167, "source": "A2.0 door schedule + plan '3'-0\" DOOR'; 7/A2.0",
                  "location": "Storage 101", "header": "metal", "pieces": 2, "pieces_source": "7/A2.0 '3-5/8\" METAL TRACK' + '3-5/8\" METAL STUD NESTED IN METAL TRACK' = 2 pieces",
                  "head_source": "A2.0 door schedule 7'-0\" + 2\" HM frame head (A0.3 hollow metal frames) - DERIVADO",
                  "header_type": "TRACK HEADER", "piece": "track", "header_type_source": "7/A2.0 TYPICAL HEAD DETAIL (JAMB SIM): '3-5/8\" METAL TRACK' + '3-5/8\" METAL STUD NESTED IN METAL TRACK'",
                  "pieces_info": "7/A2.0 one track head with nested stud over the HM frame; F.R.T. wood blocking of the detail = Div. 06 EXCLUDED",
                  "img": "/root/xf/work/etapas/2_lectura/A/img/door_schedule_A2.0.png"}]
c['misc_items'] = [m for m in c['misc_items'] if m['ref'] not in ('JAMB-101', 'HDR-101')]
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
c = json.load(open(P))
for it in c.get('openings_extra') or []:
    c['opening_schedule']['none'].append({"ref": it['ref'], "why": "hallway north opening (A2.0 4'-3 1/8\", DEMO-01 removed): jambs are existing walls (patch only); its 8'-6\" gyp header carried as misc SOF-01 (A3.0)"})
c['openings_extra'] = []
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
c = json.load(open(P))
c['nodes_info'] = "reading A nodes (against existing walls W1 / W4, not quantified) replaced by free ends: every W2 end abuts existing construction"
c['nodes'] = [
 {"id": "N1", "kind": "free", "wall": "W2-01", "source": "A2.0", "source_info": "north end against existing north demising wall W1 (6/A2.0 wall connection at demising, metal corner bead)"},
 {"id": "N2", "kind": "free", "wall": "W2-01", "source": "A2.0", "source_info": "south end against the existing post (W4) at 1489.08 pt"},
 {"id": "N3", "kind": "free", "wall": "W2-02", "source": "A2.0", "source_info": "north end against the existing post at 1506.96 pt"},
 {"id": "N4", "kind": "free", "wall": "W2-02", "source": "A2.0", "source_info": "south end against existing wall W4-06 at 1578.96 pt"}]
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
c = json.load(open(P))
for w in c['walls']:
    w['detail_info'] = w['detail']
    w['detail'] = '2/A2.0' if w['id'].startswith('W2') else '5/A2.0'
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
c = json.load(open(P))
d = c['details']
d['2/A2.0'].update(layers_per_face=1, layers_source="2/A2.0 W2 '5/8\" TYPE 'X' GYP. BD. BOTH SIDES' (one layer per face)",
                   sealant_none_reason="acoustical sealant EXCLUDED in all projects (estimator standing order)", sealant_source="2/A2.0")
d['5/A2.0'].update(layers_per_face=1, layers_source="5/A2.0 '5/8\" TYPE 'X' GYP. BD. ONE SIDE OVER 2 1/2\" METAL STUDS (TYP. ALL SIDES)'",
                   sealant_none_reason="acoustical sealant EXCLUDED in all projects (estimator standing order)", sealant_source="5/A2.0")
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
c = json.load(open(P))
for w in c['walls']:
    for f in w['faces']:
        if 'type x' in str(f.get('board', '')).lower():
            f['board_info'] = f['board']; f['board'] = '5/8 type X'
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
c = json.load(open(P))
c['edge_blocking_none_reason'] = ("2/A2.0 / A2.0 wall legend: board 'TO 6\" ABOVE CEILING' - the only horizontal joint of a 12'-6\" face hung with 4'x12' stock "
                                  "falls at 12'-0\", at / above the finished ACT ceiling (A3.0 12'-0\"): no finished joint; no edge blocking printed on 2/A2.0 - 8/A2.0")
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
c = json.load(open(P))
for b in c['blocking_items']:
    b['material_info'] = b['material']; b['material'] = 'metal'
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
c = json.load(open(P))
for m in c['misc_items']:
    if m['ref'].startswith('BRACE-'):
        m['familia_info'] = m['familia']; m['familia'] = 'metal stud brace to structure (printed)'
        m['pcs'] = m['qty']; m['qty'] = m['lf']; m['unit'] = 'LF'
    if m.get('element') == 'demo':
        m['familia'] = 'demolition - gypsum board and metal framing'; m['unit'] = 'SF'; m['qty'] = m['sf']
for b in c['blocking_items']:
    b.setdefault('product', b.get('material_info'))
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
c = json.load(open(P))
for t in c['trim_items']:
    if t['kind'] == 'L_bead':
        t['kind_info'] = "L bead (5/A2.0 'FINISH CORNER 'L' BEAD')"; t['kind'] = 'edge_trim'
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
c = json.load(open(P))
MAPA = {'access panels': 'access panel', 'deflection clips / slip track': 'deflection clips'}
keep = []
for a in c['accesorios_none']:
    if a['familia'] in MAPA:
        a['familia'] = MAPA[a['familia']]; keep.append(a)
    else:
        c.setdefault('accesorios_none_info', []).append(a)
keep += [
 {"familia": "extra framing ATM", "why": "no ATM / recessed equipment in the set (A2.0, A5.0)", "source": "A2.0"},
 {"familia": "Level 5 finish", "why": "A2.0 partition plan general note 3: 'TAPED, SANDED SMOOTH TO A LEVEL 4 FINISH' (Level 4 printed)", "source": "A2.0"},
 {"familia": "stud reinforcement MEP", "why": "no MEP equipment hung on the new W2 walls (E2.0, M1.0 and P1.0 swept)", "source": "E2.0, M1.0, P1.0"},
 {"familia": "gypsum board jamb return", "why": "door 101 in a hollow metal frame (A2.0 door schedule, 7/A2.0); hallway opening jambs are existing walls (patch only)", "source": "A2.0, 7/A2.0"},
 {"familia": "additional head track", "why": "7/A2.0 draws one track head with a nested stud over the HM frame (carried by the opening); no additional head track", "source": "7/A2.0"},
 {"familia": "2-1/2\" CFMF coiling grille head", "why": "no coiling grille in the set (A2.0 door schedule, A5.0; security shutters are a deferred submittal by others, A0.1)", "source": "A0.1, A2.0"}]
c['accesorios_none'] = keep
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
c = json.load(open(P))
for w in c['walls']:
    if w['stud_size'].replace('-', ' ').strip() == '3 5/8"':
        w['stud_size_info'] = w['stud_size']; w['stud_size'] = '3-5/8"'
    for k in ('type', 'trims'):
        if k in w: w[k + '_info'] = w.pop(k)
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)

# ---------------------------------------------------------------------------------------------------------------------------
# Stage 6-8 (calculation / Excel) format additions, 11-nov: data the reglas.py gate (plantilla_excel armar) reads in the canon.
# No quantity changes; each change recorded in a *_info key of the element.
#  F1 length_source of W2-01 / W2-02 said 'x~856' / 'x~738' (x of the dimension TEXT on the sheet, not a measure): written
#     'at x 856 pt' (the '~' read as 'approximate' by the gate, E27 / G_LARGO);
#  F2 W2-01 / W2-02 length_op: tick type of the printed A2.0 dimension strings (single diagonal ticks, checked on the zoom
#     etapas/4_canon/img/ticks_W2-01_A2.0.png / ticks_W2-02_A2.0.png rendered here from the clean PDF) - G_CADENA;
#  F3 column wraps CF-01 / CF-02: fos_chain_faces = one entry per faces_ft (5/A2.0 prints no dimension: 'DIMENSIONS OF COLUMN
#     FURRING IN A COMMON AREA ARE TO BE EQUAL'), each with the vector op of its band (A_WRAP_FOS);
#  F4 details[*].sealant_none_reason where missing: program check of the sheet text (set_texto.json) for SEALANT / CAULK on the
#     detail's sheet; acoustical sealant EXCLUDED anyway (estimator standing order) (G_DET_SEALANT).
import re as _re, os as _os
import pymupdf as _fz
c = json.load(open(P))
_doc = _fz.open(f'{K}/plans/bidset_SIN_MARKUPS.pdf')
_img = f'{K}/etapas/4_canon/img'; _os.makedirs(_img, exist_ok=True)
_TK = {'W2-01': ((820, 1225, 900, 1320), "A2.0 dimension string 4\" + 3'-0\" DOOR (ticks 1237.56 / 1243.56 / 1297.56): SINGLE diagonal ticks, chain total 3'-4\""),
       'W2-02': ((700, 1495, 790, 1590), "A2.0 dimension 4'-0\" (ticks 1506.96 / 1578.96): SINGLE diagonal ticks, total 4'-0\"")}
for w in c['walls']:
    s = w.get('length_source') or ''
    if '~' in s:
        w['length_source_info'] = 'F1: x of the dimension text written as a coordinate (was "' + _re.search(r'x~\d+', s).group(0) + '")'
        w['length_source'] = _re.sub(r'x~(\d+)', r'at x \1 pt', s)
    if w['id'] in _TK:
        clip, txt = _TK[w['id']]
        f = f"{_img}/ticks_{w['id']}_A2.0.png"
        _doc[4].get_pixmap(dpi=200, clip=_fz.Rect(*clip)).save(f)
        if 'ticks' not in w.get('length_op', ''):
            w['length_op'] = w['length_op'] + ' | ticks: ' + txt
        w['length_op_info'] = f'F2: tick type read on {f}'
    if w.get('element') == 'column_wrap' and not w.get('fos_chain_faces'):
        b = w['band']
        ops = [f"N-S side (hi-lo)/18 = ({b['hi']}-{b['lo']})/18", f"E-W side (c1-c0)/18 = ({b['c1']}-{b['c0']})/18",
               f"E-W side (c1-c0)/18 = ({b['c1']}-{b['c0']})/18"]
        w['fos_chain_faces'] = [{'measured_op': f'{o} = {v}', 'source': 'A2.0 vector furring outline (0.72 pt lines); '
                                 "5/A2.0 prints no dimension ('DIMENSIONS OF COLUMN FURRING IN A COMMON AREA ARE TO BE EQUAL')"}
                                for v, o in zip(w['faces_ft'], ops)]
        w['fos_chain_faces_info'] = 'F3: one entry per faces_ft, vector measure of the band at 18 pt/ft (no printed chain)'
_st = json.load(open(f'{K}/set_texto.json'))['hojas']
for k, d in c['details'].items():
    if isinstance(d, dict) and not d.get('sealant_none_reason') and not d.get('sealant'):
        sh = k.split('/')[-1]
        hits = len(_re.findall(r'SEALANT|CAULK', str(_st.get(sh, '')), _re.I))
        d['sealant_none_reason'] = (f"no sealant bead drawn or noted in {k} ({sh} text: {hits} 'SEALANT' / 'CAULK' hits); "
                                    "acoustical sealant EXCLUDED anyway (estimator standing order)")
        d['sealant_source'] = d.get('source') or sh
        d['sealant_none_reason_info'] = 'F4: program check of set_texto.json'
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
#  F5 rfis[*].fuentes_revisadas: the four sources checked before each RFI (designation, other row / schedule, standard rule,
#     detail), from the readers' search recorded in rfis[*].source / resolved (G_RFI / E23). Text only.
c = json.load(open(P))
_F = {
 "RFI-01": "designation: no B.O. / T.O. structure, deck or joist height on any tag or note (A1.0, A2.0, A3.0, A4.0, A5.0; E / M / P SHX); "
           "other row: A4.0 room finish schedule gives ceiling heights only (12'-0\" / 10'-0\" / 9'-0\"), A5.0 9 '12'-0\" TO B.O. CEILING'; "
           "standard rule: none - IBC 2021 / ASTM C754 do not set an existing structure height; detail: 4/A2.0 'BRACE TO STRUCTURE' draws no "
           "dimension above the ceiling; only A0.1 'HEIGHT IN STORIES: 1 STORY - 26 FT' is printed (loaded, conservative)",
 "RFI-02": "designation: A3.0 tag 'GYP. BD. 8'-6\" AFF' without 'EXISTING' (the hallway tag says EXISTING 9'-0\"); other row: A4.0 room "
           "finish schedule has no soffit row; standard rule: the A2.0 wall legend 'TO 6\" ABOVE CEILING' for the faces; detail: no soffit / "
           "header detail on A2.0 (3-8/A2.0) or A3.0 (2-4/A3.0) -> framed as type W2 (2/A2.0); closed by the plans",
 "RFI-03": "designation: A1.0 key note 7 leader to the inner dashed pair; other row: A1.0 legend (dashed = to be removed); standard rule: "
           "key note 7 'ALL EXISTING INTERIOR WALLS ... AS SHOWN DASHED TO BE REMOVED'; detail: no section of existing; closed by the plans",
 "RFI-04": "designation: A2.0 plan '3'-0\" DOOR' between the W2 ends; other row: A2.0 door schedule 101 3'-0\" x 7'-0\" HM frame type 1; "
           "standard rule: R.O. as drawn; detail: 7/A2.0 head / jamb; closed by the plans",
 "RFI-05": "designation: 5/A2.0 '2 1/2\" METAL STUDS' (no gauge / spacing); other row: A2.0 interior wall limiting heights table "
           "250S125-43 @ 16\" = 13'-0\" >= 12'-6\"; standard rule: the table governs stud specs (2/A2.0 'REFER TO INTERIOR WALL LIMITING "
           "HEIGHTS'); detail: 5/A2.0; closed by the plans",
}
for r in c['rfis']:
    if r['id'] in _F and not r.get('fuentes_revisadas'):
        r['fuentes_revisadas'] = _F[r['id']]
        r['fuentes_revisadas_info'] = 'F5: four sources checked before the RFI (readers search + resolution)'
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
#  F6 column wraps: length_cause = why the Bluebeam length of the BOX markup differs from the LF (verificar_markups_excel (c)):
#     markups_bluebeam.py draws a BOX band as its closed footprint (4 sides, LF shared over the 4 pieces); the LF is the 3 exposed
#     sides (faces_ft) - the 4th side lies against the existing storefront pier and is not furred.
c = json.load(open(P))
for w in c['walls']:
    if w.get('element') == 'column_wrap' and not w.get('length_cause'):
        b = w['band']
        w['length_cause'] = (f"BOX markup = closed footprint of 4 sides ({round(2 * ((b['hi'] - b['lo']) + (b['c1'] - b['c0'])) / 18, 2)} ft); "
                             f"LF = 3 exposed sides {' + '.join(str(x) for x in w['faces_ft'])} = {w['length_ft']} (4th side against the "
                             "existing storefront pier, not furred, 5/A2.0)")
        w['length_cause_info'] = 'F6: markup length vs LF explained (no quantity change)'
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# --- U-114: every DERIVED height with its operation written (printed ceiling + printed 6" rule = value) ---
c = json.load(open(P))
CEIL = {"retail": ("12'-0\"", 12.0, "A3.0 RETAIL 100 '2x4 ACT 12'-0\" AFF'"), "storage": ("10'-0\"", 10.0, "A3.0 STORAGE 101 '2x4 ACT 10'-0\" AFF'"),
        "hallway": ("9'-0\"", 9.0, "A3.0 HALLWAY 102 'GYP. BD. 9'-0\" AFF' (existing)")}
def op(room, h, rule):
    k = next((k for k in CEIL if k in str(room).lower()), None)
    if not k: return None
    t, v, src = CEIL[k]
    assert abs(v + 0.5 - h) < 1e-6, (room, h)
    return f"{src} + 6\" ({rule}) -> {t} + 0'-6\" = {h} ft [DERIVED]"
for w in c['walls']:
    rule = "A2.0 wall legend / 2/A2.0 W2 'TO 6\" ABOVE CEILING'" if w['id'].startswith('W2') else "A2.0 key note 1 'TO 6\" ABOVE CEILING'"
    o = op('retail', w['height_ft'], rule)
    if o:
        w['height_source_info'] = w['height_source']; w['height_source'] = o; w['height_op'] = o
    for f in w['faces']:
        o = op(f.get('room'), f['height_ft'], rule)
        if o:
            f['height_source_info'] = f['height_source']; f['height_source'] = o; f['height_op'] = o
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# --- gate data: scales by sheet (printed), SOF-01 as a framed soffit record (no quantity), no wood walls, existing walls excluded, W2-02 printed ---
c = json.load(open(P))
c['constants']['plan_scale_by_sheet'] = {h: {"value": 18.0, "source": f"1/{h} view title 1/4\" = 1'-0\" (vector check on printed dimensions)"} for h in ("A1.0", "A2.0", "A3.0")}
s = c.get('soffit_header_info') or {}
c['framed_soffits'] = [{"id": "SOF-01", "ref": "SOF-01", "source": "A3.0 'GYP. BD. 8'-6\" AFF' + A2.0 wall legend 6\" above ceiling; framing as type W2 (2/A2.0)",
    "faces": [{"side": "bottom", "layers": 1, "board": "5/8 type X", "sf": s.get('area_sf')},
              {"side": "storage face (8'-6\" to 10'-6\")", "layers": 1, "board": "5/8 type X"},
              {"side": "hallway face (8'-6\" to 9'-6\")", "layers": 1, "board": "5/8 type X"}],
    "quantities": "misc_items SOF-01-TRACK / SOF-01-STUDS / SOF-01-BOARD + trim CB-SOF-01 (this record carries no quantity)"}]
c['wood_walls_none_reason'] = "no wood-framed wall in the set: new walls are metal (2/A2.0 W2 3-5/8\" metal studs, 5/A2.0 2-1/2\" metal studs); W1 / W4 existing to remain (2/A2.0, not quantified)"
c['excluded_walls'] = [{"id": e['id'], "why": e['why']} for e in c.get('existing_walls_info') or []] + [{"id": "W2-01a", "why": "reading A 4\" stub merged into W2-01 (wall measured through the door 101 R.O., resolution item 1)"}]
for w in c['walls']:
    if w['id'] == 'W2-02':
        w['status'] = 'CONFIRMADO'; w['length_status'] = 'CONFIRMADO'
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# --- detail / schedule chain data (bubble + schedule reviewer): type_id, blocking sources 6/A5.0 + 8/A5.0, hi-lo fountain backing ---
c = json.load(open(P))
for w in c['walls']:
    w['type_id'] = 'W2' if w['id'].startswith('W2') else 'CF'
for b in c['blocking_items']:
    if b['ref'].startswith('BK-EV44'):
        b['source'] = "8/A5.0, 6/A5.0 (EV-44 / EV-45 elevations); A5.0 blocking legend; A4.0 key 4; A2.0 key 2"
if not any(b['ref'] == 'BK-DF' for b in c['blocking_items']):
    c['blocking_items'].append({"ref": "BK-DF", "lf": 6.0, "material": "metal", "product": "16 ga x 6\" x 1-1/2\" unpunched track (8/A2.0)",
        "label": "backing for the ADA high-low drinking fountain on the existing wall (11/A5.0 DRINKING FOUNTAIN ELEVATION; A2.0 key note 2 / 8/A2.0)",
        "source": "11/A5.0; A5.0 'ADA HIGH LOW DRINKING FOUNTAIN - SEE PLUMBING'; A2.0 key note 2; 8/A2.0", "wall": "W4 (existing)",
        "op": "width not printed -> standing rule R-ALC-02: 3'-0\" x 2 rows = 6.0 LF", "status": "DERIVADO",
        "note": "on an existing wall, like BK-FE: installation requires opening and patching the existing board (Review Item 2)"})
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
