"""1_inventario/inventario.json completed with the 2/A2.0 wall types read by the independent schedule reader (fichas.json):
inventario_tags.py found no type legend (2/A2.0 'WALL TYPE 1..4' titles with diamond keys W1..W4) and left the A2.0 tags as
partition_candidato 'not in schedule'. Here, by program: every A2.0 candidate whose type is in fichas.json becomes a
partition_tag (same bbox, verified crop). Original kept as 1_inventario/inventario_script.json."""
import json, os, shutil
K = '/root/xf/work'; I = f'{K}/etapas/1_inventario'
if not os.path.exists(f'{I}/inventario_script.json'):
    shutil.copy2(f'{I}/inventario.json', f'{I}/inventario_script.json')
inv = json.load(open(f'{I}/inventario_script.json'))
fi = json.load(open(f'{K}/indep/fichas.json'))
types = list(fi.get('schedule_order') or fi['types'].keys())
oc = inv['ocurrencias']; keep, tags = [], []
for o in oc.get('partition_candidato') or []:
    if o.get('sheet') == 'A2.0' and o.get('type') in types:
        t = dict(o, kind='partition_tag', fuera_de_schedule=False, motivo='type in 2/A2.0 (fichas.json, independent schedule reader)', id_candidato=o['id'])
        t['id'] = o['id'].replace('PC', 'PT'); tags.append(t)
    else:
        keep.append(o)
oc['partition_candidato'] = keep
oc['partition_tag'] = (oc.get('partition_tag') or []) + tags
inv['partition_types'] = dict(inv.get('partition_types') or {}, schedule=[{'type': t, 'source': '2/A2.0 (fichas.json)'} for t in types])
inv.setdefault('avisos', []).append('types from 2/A2.0 by the independent schedule reader (fichas.json); A2.0 candidates reclassified as partition_tag by scripts/inventario_types.py')
json.dump(inv, open(f'{I}/inventario.json', 'w'), indent=1, ensure_ascii=False)
MAP = {t['id_candidato']: t['id'] for t in tags}
json.dump(MAP, open(f'{I}/mapa_PC_a_PT.json', 'w'), indent=1)
for L in 'AB':
    f = f'{K}/etapas/2_lectura/canon_{L}.json'; c = json.load(open(f))
    for w in c['walls']:
        w['tag_ids'] = [MAP.get(x, x) for x in w.get('tag_ids') or []]
    for x in c.get('tags_descartados') or []:
        x['id'] = MAP.get(x['id'], x['id'])
    json.dump(c, open(f, 'w'), indent=1, ensure_ascii=False)
print(len(tags), 'partition_tag;', len(keep), 'candidates left; types', types)
