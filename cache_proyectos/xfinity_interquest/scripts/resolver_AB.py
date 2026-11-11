"""Resolution of the A / B differences (comparar.py revision.json) for Consumer Cellular Centennial: base = reading A
(complete canon); every decision below was made on the comparar.py crop (etapas/3_revision/img) and the A100 vector
geometry, with the rule that governs it. Writes etapas/4_canon/takeoff_canon.json + etapas/3_revision/resolucion.md.
No quantity is typed: lengths / bands are the readings' own values."""
import json, copy, os
K = '/root/cc/work'
A = json.load(open(f'{K}/etapas/2_lectura/A/takeoff_canon_A.json'))
B = json.load(open(f'{K}/etapas/2_lectura/B/takeoff_canon_B.json'))
BW = {w['id']: w for w in B['walls']}
AW = {w['id']: w for w in A['walls']}
c = copy.deepcopy(A)
dec = []
def from_B(bid, newid, replace, why, img):
    b = copy.deepcopy(BW[bid]); base = copy.deepcopy(AW[replace[0]]) if replace[0] in AW else {}
    # keep reading A's field style (A schema), take B's geometry / length / openings
    w = base or b
    for k in ('band', 'length_ft', 'length_source', 'length_op', 'length_status', 'location', 'openings', 'tag_ids'):
        if k in b: w[k] = b[k]
    tid = set(w.get('tag_ids') or [])
    for r in replace:
        tid |= set(AW.get(r, {}).get('tag_ids') or [])
    w['tag_ids'] = sorted(tid)
    w['id'] = newid
    w['resolution'] = f"[resolution A vs B] {why} (crop {img})"
    return w
new = []
skip = set()
# 1. door openings inside the wall run (U-057 / R70 bottom track without door deduction; opening listed in the wall)
for bid, newid, rep, door, img in (('E3-02', 'E3-02', ['E3-02'], '6C', '006_DIF_E3_A100_p7.png'),
                                   ('E3-04', 'E3-04', ['E3-04', 'E3-05'], '4C', '003_DIF_E3_A100_p7.png'),
                                   ('E3-07', 'E3-09', ['E3-09', 'E3-10'], '5C', '005_DIF_E3_A100_p7.png')):
    w = from_B(bid, newid, rep, f"door {door} R.O. 3'-4\" is an opening INSIDE this wall line (one straight line, one tag); "
               "walls are measured through door openings and the opening is listed in the wall (skill U-057 / R70: track and "
               "board without door deduction); reading A had measured only the solid parts", img)
    new.append((rep[0], w)); skip |= set(rep)
    dec.append((f"E3 door {door}", f"A {' + '.join(f'{r} {AW[r][chr(108)+'ength_ft']}' for r in rep)} vs B {bid} {BW[bid]['length_ft']}",
                f"B: {BW[bid]['length_ft']} LF (door R.O. inside the wall line)", "A100 + A600", img))
# 2. 4'-0" cased opening between Hallway and Sales: untagged infill in the C3 line -> C3 (to deck), conservative + RFI
w = from_B('C3-02', 'C3-02', ['E3-14'], "the 4'-0\" x 8'-0\" cased opening (2/A400 T.O. OPENING 8'-0\") sits in the straight "
           "line of the C3 wall (C3 tag at its north end); untagged segment joined to the tagged line it continues, framed to deck "
           "(conservative: C3 to deck, both sides) - RFI-06 keeps the E3 alternative", '002_DIF_C3_A100_p7.png')
for k in ('stud_size', 'stud_source', 'gauge', 'gauge_source', 'oc_in', 'oc_source', 'detail', 'detail_source', 'top_track_info',
          'track_source', 'height_ft', 'height_source', 'height_status', 'faces', 'tag'):
    if k in AW['C3-01']: w[k] = copy.deepcopy(AW['C3-01'][k])
w['tag_ids'] = []
w['untagged_join'] = "segment without tag joined to the C3 line it continues (E28 eje rule); RFI-06"
skip.add('E3-14')
C3EXT = w  # merged into C3-01 below (same straight C3 line, opening inside the wall)
dec.append(("C3 / E3 infill over cased opening", "A E3-14 4.00 LF @ 4.417 ft (E3) vs B C3-02 4.00 LF @ 17.13 ft (C3)",
            "B: C3-02 4.00 LF to deck (conservative), RFI-06 with delta", "A100 / 2/A400", '002_DIF_C3_A100_p7.png'))
# 3. C3 stud height: deck break between BOH 16'-4" and Sales 17'-1 9/16" not drawn on the C3 line -> higher deck (B), RFI-01
for wid in ('C3-01',):
    pass
dec.append(("C3-01 length", "A C3-01 31.542 LF + E3-14 4.0 LF vs B C3-01 31.542 + C3-02 4.0 LF", "C3-01 35.542 LF (31'-6 1/2\" printed + 4'-0\" cased opening inside the C3 line)", "A100", '002_DIF_C3_A100_p7.png'))
dec.append(("C3-01 stud height", "A 16.333 ft (BOH deck) vs B 17.13 ft (Sales deck)",
            "B: 17.13 ft (higher printed deck, conservative); RFI-01 keeps the 16'-4\" alternative with its delta", "A100 deck tags", '002_DIF_C3_A100_p7.png'))
# 4. A3 north wall: two A3 tags split by the existing column -> two walls (E28 eje: each tag marks its wall)
dec.append(("A3 north sales wall", "A A3-01 14.41 + A3-02 28.83 LF vs B A3-01 43.24 LF", "A: two walls (two A3 tags, line broken by the existing column, D100 key 14); same total 43.24 LF", "A100 / D100", '001_DIF_A3_A100_p7.png'))
# 5. small returns / stubs only in A (E3-06, E3-08, E3-04 0.58, E3-09 0.75): B had them inside joined walls (B E3-06 joins two axes)
dec.append(("E3 alcove returns E3-06 / E3-08", "A two returns 1.083 LF each vs B E3-06 2.167 LF (two axes in one number)", "A: one wall per axis (U-120), same total 2.17 LF", "A100", '009_ONLYA_E3_A100_p7.png'))
walls = []
for w in c['walls']:
    rep = [x for x in new if x[0] == w['id']]
    if rep:
        walls.append(rep[0][1]); continue
    if w['id'] in skip: continue
    if w['id'] == 'C3-01':
        w['height_ft'] = 17.13
        w['height_source'] = "A100 'PLY DECK @ 17'-1 9/16\"' (Sales Area deck tag) - the deck break between BOH (16'-4\") and Sales is not drawn on the C3 line: higher printed deck carried (conservative), RFI-01"
        w['height_status'] = 'DERIVADO'
        w['resolution'] = "[resolution A vs B] height 17.13 ft (B) instead of 16.333 (A): higher printed deck, RFI-01; " + C3EXT['resolution'] + "; merged here: one straight C3 line with the 4'-0\" cased opening inside the wall"
        w['band']['hi'] = C3EXT['band']['hi']
        w['length_ft'] = round(w['length_ft'] + C3EXT['length_ft'], 3)
        w['length_op'] = "31'-6 1/2\" printed (A100) + 4'-0\" printed cased opening (A100) = 35.542"
        w['length_source'] = "A100 31'-6 1/2\" + 4'-0\" (cased opening 2/A400 inside the C3 line)"
        w['length_status'] = 'DERIVADO'
        w['openings'] = copy.deepcopy(C3EXT.get('openings') or [])
    walls.append(w)
c['walls'] = walls
c['excluded_walls'] = [{"id": 'E3-05', "why": 'reading A piece merged into E3-04 (door 4C inside the wall line)'}, {"id": 'E3-10', "why": 'reading A piece merged into E3-09 (door 5C inside the wall line)'}, {"id": 'E3-14', "why": 'reading A infill over the cased opening merged into C3-01 (same C3 line, RFI-05)'}]
# openings: point to the resolved walls
for it in c['opening_schedule']['items']:
    m = {'Door 4C': 'E3-04', 'Door 5C': 'E3-09', 'Door 6C': 'E3-02'}
    if it['ref'] in m: it['wall'] = m[it['ref']]
for o in c.get('openings_extra') or []:
    if o['ref'] == 'CASED-OPEN-HALL': o['header'] = 'C3-02 infill (RFI-06)'; o['wall'] = 'C3-02'
os.makedirs(f'{K}/etapas/4_canon', exist_ok=True)
json.dump(c, open(f'{K}/etapas/4_canon/takeoff_canon.json', 'w'), indent=1, ensure_ascii=False)
L = ['# Resolution of reading A vs reading B - Consumer Cellular Centennial (A100)', '',
     'Base: reading A. Each item decided on the comparar.py crop (blue = A, orange = B) and the A100 vector geometry.', '',
     '| # | Item | A vs B | Decision | N/SHEET | Image |', '|---|---|---|---|---|---|']
for i, (a, b2, d, s, im) in enumerate(dec, 1):
    L.append(f'| {i} | {a} | {b2} | {d} | {s} | img/{im} |')
L += ['', 'Alerts: 19 CO2 / TC1 / TC2 symbols = store number and electrical tags (tags_descartados of both readings); '
      'TYPE NO INVENTARIADO A3 / C3 / D / E3 = inventario_tags.py did not read the 1/A500 legend (types are section titles '
      'with a diamond A#, C#, D, E#, H; # = stud size code of the plan-view key, 3 = 3-5/8"); the 5 types are verified on the '
      '1/A500 crop by the independent schedule reader (fichas.json). Type D tag (single letter) located by both readings '
      'at A100 (D-01).', '', f"Totals after resolution: " + ", ".join(
      f"{t} {round(sum(w['length_ft'] for w in walls if w['tag']==t),2)} LF / {sum(1 for w in walls if w['tag']==t)} walls" for t in ('A3','C3','D','E3'))]
open(f'{K}/etapas/3_revision/resolucion.md', 'w').write('\n'.join(L) + '\n')
print(L[-1])
