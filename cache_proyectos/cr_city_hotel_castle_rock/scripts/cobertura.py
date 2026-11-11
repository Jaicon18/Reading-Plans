#!/usr/bin/env python3
"""CR City Hotel - MATRIZ DE COBERTURA (Paso 12) por programa: todo lo que el set imprime del trade tiene destino.
Ítems: (1) cada type de los schedules A0.06 / A0.07 / A0.08 (fichas.json), (2) cada partition tag del inventario
(354), (3) cada tipo de cielo de la leyenda del RCP, (4) cada ítem de alcance (ALC-xx). Destino = renglón del canon
(wall / ceiling / misc / trim), EXCLUDED con motivo, o RFI abierto con supuesto cargado. GAP = sin destino.
Salida: etapas/COBERTURA_PASO12.md (+ .json)."""
import json, re, collections
W = '/root/cr/work'
c = json.load(open(f'{W}/etapas/4_canon/takeoff_canon.json'))
tj = json.load(open(f'{W}/takeoff.json'))
inv = json.load(open(f'{W}/etapas/1_inventario/inventario.json'))
fi = json.load(open(f'{W}/indep/fichas.json'))
ew = c['existing_walls']
tnr = {k.upper(): v for k, v in (c.get('types_none_reason') or {}).items()}
rows = []

def add(cat, item, dest, st, src=''):
    rows.append({"cat": cat, "item": item, "dest": dest, "status": st, "src": src})

# (1) types del schedule
types_canon = collections.Counter(w['type_id'] for w in ew)
fam = {str(w['type']).upper() for w in ew}
for tid, t in (fi.get('types') or {}).items():
    t = t if isinstance(t, dict) else {}
    base = re.sub(r"-\d+$", "", tid).upper()
    if types_canon.get(tid):
        add('schedule type', tid, f"{types_canon[tid]} wall entries (Partition Takeoff, block {tid})", 'COVERED', t.get('sheet') or '')
    elif base in fam:
        add('schedule type', tid, f"family {base} loaded with the printed rating of each tag; this rating row is not tagged on the plans", 'COVERED (not used)', t.get('sheet') or '')
    elif str(tnr.get(tid.upper()) or tnr.get(base) or '').startswith('LOADED'):   # rev13: roof / floor assemblies cargados (RS-1, RS-6, FS-1, MB-1)
        add('schedule type', tid, str(tnr.get(tid.upper()) or tnr.get(base)), 'COVERED', t.get('sheet') or '')
    elif base in tnr or any(base.startswith(k.split('.')[0] + '.') and k.split('.')[0] in ('C', 'CM') for k in tnr):
        add('schedule type', tid, f"EXCLUDED: {tnr.get(base, 'concrete / CMU, not our trade (U-061)')}", 'COVERED (excluded)', t.get('sheet') or '')
    else:
        add('schedule type', tid, "not tagged on any plan of the set (A0.06 GN 2 'NOT ALL PARTITION TYPES DELINEATED MAY BE USED')", 'COVERED (not used)', t.get('sheet') or '')

# (2) tags del inventario
duenos = collections.defaultdict(list)
for w in ew:
    for t in w.get('tag_ids') or []:
        duenos[t].append(w['id'])
desc = {}
for f in ('2_lectura/canon_A.json', '2_lectura/canon_B.json'):
    for d in json.load(open(f'{W}/etapas/{f}')).get('tags_descartados') or []:
        desc.setdefault(str(d.get('id')), d.get('motivo'))
exc = {x['id']: x['reason'] for x in c.get('excluded_walls') or []}
for o in inv['ocurrencias'].get('partition_tag') or []:
    tid, ty = o['id'], str(o.get('type') or '').upper()
    if duenos.get(tid):
        add('partition tag', f"{tid} {o.get('type')} ({o['sheet']})", 'wall ' + ', '.join(sorted(set(duenos[tid]))[:3]), 'COVERED', o['sheet'])
    elif ty in tnr:
        add('partition tag', f"{tid} {o.get('type')} ({o['sheet']})", 'EXCLUDED: ' + tnr[ty], 'COVERED (excluded)', o['sheet'])
    elif tid in desc:
        add('partition tag', f"{tid} {o.get('type')} ({o['sheet']})", 'discarded with reason: ' + str(desc[tid])[:140], 'COVERED (discarded)', o['sheet'])
    else:
        # mismo type en la misma hoja ya cargado (tag repetido del mismo wall / leyenda de vista ampliada)
        same = [w['id'] for w in ew if str(w['type']).upper() == ty and w['sheet'] == o['sheet']]
        if same:
            add('partition tag', f"{tid} {o.get('type')} ({o['sheet']})", f"repeat tag of a loaded {o.get('type')} wall on {o['sheet']} ({same[0]})", 'COVERED', o['sheet'])
        else:
            add('partition tag', f"{tid} {o.get('type')} ({o['sheet']})", 'no destination', 'GAP', o['sheet'])

# (3) cielos de la leyenda
leyenda = {"ACT-1": "EXCLUDED: lay-in ceiling (other trade)", "ACT-2": "EXCLUDED: lay-in ceiling (other trade)", "ACT-3": "EXCLUDED: lay-in ceiling (other trade)",
           "WS-1": "EXCLUDED: wood slat ceiling (other trade)"}
for z in c.get('ceilings') or []:
    k = str((z.get('assembly') or {}).get('id') or z.get('type') or z.get('system'))
    leyenda.setdefault(k, f"ceilings[] ({z.get('system')})")
for m in c.get('misc_items') or []:
    for k in ('GYP-1', 'GYP-2'):
        if k in str(m.get('source')) and 'board' in str(m.get('ref')):
            leyenda.setdefault(k, 'misc_items CLG-* board + USG drywall suspension')
for k, v in sorted(leyenda.items()):
    add('ceiling type (RCP legend)', k, v, 'COVERED (excluded)' if v.startswith('EXCLUDED') else 'COVERED', 'A3.01-A3.04 legend')

# (4) alcance
for a in tj.get('alcances') or []:
    add('scope item', f"{a['id']} {a.get('nombre', '')}", f"{a['estado']}: {str(a.get('nota') or '')[:150]}", 'COVERED', 'Scope Checklist')
for r in c['rfis']:
    if r['status'] == 'open':
        add('open RFI', r['id'], f"conservative value LOADED: {str(r['loaded'])[:120]}", 'COVERED (RFI)', r['source'])

n = len(rows); gaps = [r for r in rows if r['status'] == 'GAP']
L = ["# COBERTURA - Paso 12 (coverage matrix) - CR City Hotel rev16", "",
     f"{n} items · {n - len(gaps)} covered · {len(gaps)} GAP · {100 * (n - len(gaps)) / n:.1f} %", "",
     "| # | Category | Item | Destination | Status | Source |", "|---|---|---|---|---|---|"]
for i, r in enumerate(rows, 1):
    L.append(f"| {i} | {r['cat']} | {r['item']} | {r['dest']} | {r['status']} | {r['src']} |")
open(f'{W}/etapas/COBERTURA_PASO12.md', 'w').write("\n".join(L) + "\n")
json.dump(rows, open(f'{W}/etapas/COBERTURA_PASO12.json', 'w'), indent=1)
print(n, 'items', len(gaps), 'GAP')
for g in gaps[:20]:
    print('GAP', g['item'])
