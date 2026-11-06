"""canon_A.json / canon_B.json (2_lectura) = cada lectura convertida con la MISMA regla (build_canon) para comparar.py /
etapas.py. Solo formato: los walls de cada lectura con sus bandas normalizadas; sin cálculo."""
import json, os, glob
REC = {"PA0002": "1_inventario/recortes/PA0002_W_6_T0.01_p2.png", "PA0003": "1_inventario/recortes/PA0003_W_6_T0.01_p2.png", "PA0006": "1_inventario/recortes/PA0006_XW_6_3_A2.01_p17.png", "PA0007": "1_inventario/recortes/PA0007_XW_6_4_A2.01_p17.png"}
W = '/root/cr/work/etapas'
for L in 'AB':
    walls, ceil, tags = [], [], []
    for f in sorted(glob.glob(f'{W}/2_lectura/{L}/L*.json')):
        d = json.load(open(f)); fl = os.path.basename(f)[:2]
        for w in d['walls']:
            b = dict(w.get('band') or {})
            if b and float(b['c1']) - float(b['c0']) > float(b['hi']) - float(b['lo']):
                b.update(c0=b['lo'], c1=b['hi'], lo=b['c0'], hi=b['c1'])
            tids = list(w.get('tag_ids') or [])
            if fl == 'L1' and any(t in ('PA0006', 'PA0007') for t in tids):   # resolution L1: RFI-06 separate-permit boundary
                tids = [t for t in tids if t not in ('PA0006', 'PA0007')]
                tags += [{"id": t, "motivo": "tag of another type pointing to the short wall on the separate-permit boundary east of door 107.1 - not loaded (resolucion_L1, RFI-06)", "imagen": REC[t], "floor": fl} for t in ('PA0006', 'PA0007')]
            walls.append(dict(w, element='wall', band=b, floor=fl, tag=w.get('type'), tag_ids=tids))
        ceil += [dict(c, floor=fl) for c in d.get('ceilings') or []]
        tags += [dict(t, floor=fl) for t in d.get('tags_descartados') or []]
    for t in ('PA0002', 'PA0003'):
        tags.append({"id": t, "motivo": "W.6 legend example on T0.01 (INDEX AND STANDARDS graphic standards), not a wall", "imagen": REC[t], "floor": "T0.01"})
    json.dump({"project": "CR City Hotel", "reader": L, "walls": walls, "ceilings": ceil, "tags_descartados": tags},
              open(f'{W}/2_lectura/canon_{L}.json', 'w'), indent=1)
    print(L, len(walls), len(ceil), len(tags))
