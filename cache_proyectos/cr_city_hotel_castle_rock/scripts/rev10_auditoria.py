#!/usr/bin/env python3
"""rev10 (auditoría adversarial U-138 de COORDINACIÓN sobre rev9):
R1  shafts L2-L4 que llaman 7/A9.03 ('WALL DETAIL - PLAN OF SOUTH SHAFT': 2-HOUR SHAFTWALL ASSEMBLY (W419, U497)) y 8/A9.03 (PLAN OF
    NORTH SHAFT): muro de 4 3/4" impreso = C-H 2 1/2" + 1" liner + 2 x 5/8" -> C-H / J-runner 2-1/2" (la burbuja es la fuente, U-115);
    A0.06 CH.6-2 (6") queda como Review Item con su delta. CH.6-L1 / CH.6-L4 (tag CH.6 en 1/A7.50) siguen en 6".
m1  cielos de las unidades L2 201-214: altura de la zona del cuarto 4/A5.05 (11'-0" - 1'-9 1/8" = 9'-2 7/8"), como L3; el 1'-1 3/8"
    RATED ASSEMBLY de 7/A7.23 es del corridor.
m2  filas CH del Partition Takeoff: 'Shaft wall (C-H)' con su stud (stud_text), no 'wood-framed / none'."""
import json, re
W = '/root/cr/work'
CP = f'{W}/etapas/4_canon/takeoff_canon.json'
c = json.load(open(CP))
SHAFT = re.compile(r"\((7|8)/A9\.03\)")
n1 = 0
for w in c['existing_walls']:
    if not w['id'].startswith('CH'):
        continue
    m = SHAFT.search(str(w.get('location') or ''))
    if m:
        d = f"{m.group(1)}/A9.03"
        w['stud_text'] = (f"C-H 2-1/2\" 20 GA @ 24\" o.c. + J-runner 2-1/2\" ({d}: 4 3/4\" shaft wall = 2 1/2\" C-H + 1\" liner + 2 x 5/8\"; "
                          f"7/A9.03 '2-HOUR SHAFTWALL ASSEMBLY (W419, U497)'; 20 GA = spec 09 21 16.23 min. base-metal 0.0329 inch)")
        w['source'] = str(w['source']) + (f" | framing per the detail the bubble calls ({d}, U-115): 4 3/4\" overall = 2 1/2\" C-H; A0.06 CH.6-2 (6\") "
                                          f"is the conflicting row -> Review Item with the delta; spec 09 21 16.23 Studs 'Depth: As indicated on Drawings', "
                                          f"'Minimum Base-Metal Thickness: 0.0329 inch' (20 GA)")
        n1 += 1
    else:
        w['stud_text'] = "C-H 6\" 20 GA @ 24\" o.c. + J-runner 6\" (A0.06 CH.6-2, tag CH.6 on 1/A7.50)"
ids25 = {w['id'].split(' ')[0] for w in c['existing_walls'] if w['id'].startswith('CH') and SHAFT.search(str(w.get('location') or ''))}
lf_st = lf_jr = 0.0
for mi in c['misc_items']:
    r = str(mi['ref'])
    k = r.split(' ', 1)[1] if ' ' in r else ''
    if r.startswith(('CH-STUD ', 'J-RUNNER ')) and k in ids25:
        mi['familia'] = mi['familia'].replace('6" (printed)', '2-1/2" (printed)')
        mi['source'] = re.sub(r"A0\.06 CH '6\" 20GA METAL C-H STUD'", "7/A9.03 / 8/A9.03 4 3/4\" 2-HOUR SHAFTWALL (W419, U497) = 2-1/2\" C-H STUD (gauge 20GA per A0.06 CH)", str(mi['source']))
        if r.startswith('CH-STUD'):
            lf_st += float(mi['qty'])
        else:
            lf_jr += float(mi['qty'])
c['rev10_R1'] = {"walls": sorted(ids25), "cH_stud_lf": round(lf_st, 2), "j_runner_lf": round(lf_jr, 2)}
# m1
n2 = 0
for x in c.get('ceilings') or []:
    if re.match(r"L2 Guest room 2(0[1-9]|1[0-4])\b", x['room']):
        x['height_ft'] = 9.24
        x['source'] = re.sub(r"height 9\.885 \(DERIVADO:[^)]*\)[^|]*", "height 9.24 (DERIVADO: 4/A5.05 room zone 11'-0\" (L2 -> L3) - 1'-9 1/8\" floor zone = 9'-2 7/8\"; "
                             "UNIT GENERAL NOTE 1 (A7.00): ceilings shown = bottom of floor/ceiling assembly; as L3)", str(x['source']))
        n2 += 1
json.dump(c, open(CP, 'w'), indent=1)
print('R1 shaft walls', n1, 'C-H 2-1/2 LF', round(lf_st, 2), 'J-runner LF', round(lf_jr, 2), '| m1 L2 units', n2)
