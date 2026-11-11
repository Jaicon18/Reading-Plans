"""Reading B wrote its two column furrings in its own key 'column_furring' (not in walls[]): the comparison copy
etapas/2_lectura/canon_B.json gets them as walls (element column_wrap, band BOX from B's x0/x1/y0/y1, LF = B's perimeter) so
both readings are compared on the same elements (U-034). B's original file etapas/2_lectura/B/canon_B.json is untouched."""
import json
K = '/root/xf/work'; P = f'{K}/etapas/2_lectura/canon_B.json'
b = json.load(open(P)); ids = {w['id'] for w in b['walls']}
for f in b.get('column_furring') or []:
    if f['ref'] in ids:
        for w in b['walls']:
            if w['id'] == f['ref']: w['element'] = 'column_furring'
        continue
    bd = f['band']
    b["walls"].append({"element": "column_furring", "id": f["ref"], "tag": "CF", "sheet": f['sheet'], "page": 5, "tag_ids": [],
        "band": {"ori": "BOX", "c0": bd['x0'], "c1": bd['x1'], "lo": bd['y0'], "hi": bd['y1'], "sheet": bd['sheet']},
        "length_ft": f['perimeter_lf'], "length_op": f['perimeter_op'], "length_status": f['perimeter_status'], "length_source": f['sides'],
        "height_ft": f['height_ft'], "height_source": f['height_op'], "height_status": f['height_status'], "location": f['location'],
        "faces": [{"side": "A", "room": "Retail 100", "layers": 1, "board": "5/8 type X", "height_ft": f['height_ft']}],
        "stud_size": "2-1/2\"", "detail": "5/A2.0", "normalized_from": "reading B key column_furring"})
json.dump(b, open(P, 'w'), indent=1, ensure_ascii=False); print('B walls', len(b['walls']))
