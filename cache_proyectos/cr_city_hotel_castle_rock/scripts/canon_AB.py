"""canon_A.json / canon_B.json (2_lectura) = cada lectura convertida con la MISMA regla (build_canon) para comparar.py /
etapas.py. Solo formato: los walls de cada lectura con sus bandas normalizadas; sin cálculo."""
import json, os, glob
W = '/root/cr/work/etapas'
for L in 'AB':
    walls, ceil, tags = [], [], []
    for f in sorted(glob.glob(f'{W}/2_lectura/{L}/L*.json')):
        d = json.load(open(f)); fl = os.path.basename(f)[:2]
        for w in d['walls']:
            b = dict(w.get('band') or {})
            if b and float(b['c1']) - float(b['c0']) > float(b['hi']) - float(b['lo']):
                b.update(c0=b['lo'], c1=b['hi'], lo=b['c0'], hi=b['c1'])
            walls.append(dict(w, element='wall', band=b, floor=fl, tag=w.get('type')))
        ceil += [dict(c, floor=fl) for c in d.get('ceilings') or []]
        tags += [dict(t, floor=fl) for t in d.get('tags_descartados') or []]
    json.dump({"project": "CR City Hotel", "reader": L, "walls": walls, "ceilings": ceil, "tags_descartados": tags},
              open(f'{W}/2_lectura/canon_{L}.json', 'w'), indent=1)
    print(L, len(walls), len(ceil), len(tags))
