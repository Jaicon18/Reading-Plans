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
            tg = w.get('type')
            # etiqueta normalizada con la MISMA regla para A y B (solo formato): 'W.6.1' = W.6 con su rating (RFI-01 cerrado,
            # R-ALC-10); el 2-HOUR SHAFTWALL de 7/8/A9.03 sin tag = 'CH (2-HR shaftwall)' (A lo nombró así, B lo dejó null)
            if str(tg or '').upper().startswith('W.6.1'):
                tg = 'W.6'
            if not tg and str(w.get('id') or '').startswith('CH-'):
                tg = 'CH (2-HR shaftwall)'
            walls.append(dict(w, element='wall', band=b, floor=fl, tag=tg, tag_ids=tids))
        ceil += [dict(c, floor=fl) for c in d.get('ceilings') or []]
        tags += [dict(t, floor=fl) for t in d.get('tags_descartados') or []]
    for t in ('PA0002', 'PA0003'):
        tags.append({"id": t, "motivo": "W.6 legend example on T0.01 (INDEX AND STANDARDS graphic standards), not a wall", "imagen": REC[t], "floor": "T0.01"})
    json.dump({"project": "CR City Hotel", "reader": L, "constants": {"plan_scale_pt_per_ft": {"value": 9.0, "source": "A2.01-A2.04 printed 1/8\" = 1'-0\" (9 pt/ft); enlarged plans A7.xx / A6.xx printed 1/4\" = 1'-0\" (18 pt/ft)"}, "plan_scale_by_sheet": {"A2.01": {"value": 9.0, "source": "A2.01 printed 1/8\" = 1'-0\""}, "A2.02": {"value": 9.0, "source": "A2.02 printed 1/8\" = 1'-0\""}, "A2.03": {"value": 9.0, "source": "A2.03 printed 1/8\" = 1'-0\""}, "A2.04": {"value": 9.0, "source": "A2.04 printed 1/8\" = 1'-0\""}, "A3.01": {"value": 9.0, "source": "A3.01 printed 1/8\" = 1'-0\""}, "A3.02": {"value": 9.0, "source": "A3.02 printed 1/8\" = 1'-0\""}, "A3.03": {"value": 9.0, "source": "A3.03 printed 1/8\" = 1'-0\""}, "A3.04": {"value": 9.0, "source": "A3.04 printed 1/8\" = 1'-0\""}}}, "walls": walls, "ceilings": ceil, "tags_descartados": tags,
               "types_none_reason": {"C.8": "cast-in-place concrete wall (A0.06 C.x): not our trade (U-061)", "CM.4": "CMU wall (A0.06 CM.x): not our trade (U-061); furring drawn on it is read as FW / FI", "CM.8": "CMU wall (A0.06 CM.x): not our trade (U-061); furring drawn on it is read as FW / FI", "XM.0.1": "exterior masonry type, not in A0.07: not our trade (U-061, RFI-02 closed)"}},
              open(f'{W}/2_lectura/canon_{L}.json', 'w'), indent=1)
    print(L, len(walls), len(ceil), len(tags))
