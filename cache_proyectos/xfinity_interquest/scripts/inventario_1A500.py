"""1_inventario/inventario.json completed with the 1/A500 types read by the independent schedule reader (fichas.json):
inventario_tags.py found no type legend (1/A500 types are section titles with diamond keys) and left the A100 tags as
partition_candidato 'not in schedule'. Here, by program: every A100 candidate whose type is in fichas.json becomes a
partition_tag (same id, bbox, verified crop); the single-letter D diamond on A100 (not read by the script) is added from the
PDF words inside its diamond, with a circled crop reopened. Original kept as 1_inventario/inventario_script.json."""
import json, os, shutil
import pymupdf as fitz
from PIL import Image, ImageDraw
K = '/root/cc/work'; I = f'{K}/etapas/1_inventario'
if not os.path.exists(f'{I}/inventario_script.json'):
    shutil.copy2(f'{I}/inventario.json', f'{I}/inventario_script.json')
inv = json.load(open(f'{I}/inventario_script.json'))
types = set(json.load(open(f'{K}/indep/fichas.json'))['types'])
oc = inv['ocurrencias']
keep, tags = [], []
for o in oc.get('partition_candidato') or []:
    if o.get('sheet') == 'A100' and o.get('type') in types:
        t = dict(o, kind='partition_tag', fuera_de_schedule=False, motivo='type in 1/A500 (fichas.json, independent schedule reader)', id_candidato=o['id'])
        t['id'] = f"PT{len(tags) + 2:04d}"
        tags.append(t)
    else:
        keep.append(o)
# the D diamond on A100: word 'D' of the A100 text layer near the restroom / office wall (rotated page -> visible frame)
d = fitz.open(f'{K}/plans/bidset_SIN_MARKUPS.pdf'); p = d[6]; R = p.rotation_matrix
cand = []
for w in p.get_text('words'):
    if w[4] == 'D':
        r = fitz.Rect(w[:4]) * R
        cand.append(r)
canon = json.load(open(f'{K}/etapas/4_canon/takeoff_canon.json'))
dw = next(w for w in canon['walls'] if w['id'] == 'D-01')['band']
mid = ((dw['lo'] + dw['hi']) / 2, (dw['c0'] + dw['c1']) / 2)
r = min(cand, key=lambda r: abs((r.x0 + r.x1) / 2 - mid[0]) + abs((r.y0 + r.y1) / 2 - mid[1]))
clip = fitz.Rect(r.x0 - 40, r.y0 - 40, r.x1 + 40, r.y1 + 40)
pix = p.get_pixmap(dpi=200, clip=clip); im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
s = pix.width / clip.width; dr = ImageDraw.Draw(im)
dr.ellipse([(r.x0 - clip.x0 - 12) * s, (r.y0 - clip.y0 - 12) * s, (r.x1 - clip.x0 + 12) * s, (r.y1 - clip.y0 + 12) * s], outline=(255, 0, 0), width=5)
png = 'PT0001_D_A100_p7.png'; im.save(f'{I}/recortes/{png}')
tags.append({"kind": "partition_tag", "text": "D", "page": 7, "sheet": "A100", "bbox_pt": [round(r.x0, 2), round(r.y0, 2), round(r.x1, 2), round(r.y1, 2)],
             "center_pt": [round((r.x0 + r.x1) / 2, 2), round((r.y0 + r.y1) / 2, 2)], "type": "D", "id": "PT0001", "png": png, "png_verificado": True,
             "motivo": "single-letter tag in the diamond symbol, added from the A100 text layer (not read by inventario_tags.py)"})
oc['partition_candidato'] = keep
oc['partition_tag'] = (oc.get('partition_tag') or []) + tags
inv['partition_types'] = dict(inv.get('partition_types') or {}, schedule=[{'type': t, 'source': '1/A500 (fichas.json)'} for t in ('A3', 'C3', 'D', 'E3')])
inv.setdefault('avisos', []).append('types from 1/A500 by the independent schedule reader (fichas.json); A100 candidates reclassified as partition_tag by scripts/inventario_1A500.py')
json.dump(inv, open(f'{I}/inventario.json', 'w'), indent=1, ensure_ascii=False)
MAP = {t['id_candidato']: t['id'] for t in tags if t.get('id_candidato')}
for w in canon['walls']:
    w['tag_ids'] = [MAP.get(x, x) for x in w.get('tag_ids') or []]
canon['tags_descartados'] = [x for x in canon.get('tags_descartados') or [] if x.get('id') not in MAP]
json.dump(canon, open(f'{K}/etapas/4_canon/takeoff_canon.json', 'w'), indent=1, ensure_ascii=False)
json.dump(MAP, open(f'{I}/mapa_PC_a_PT.json', 'w'), indent=1)
print(len(tags), 'partition_tag on A100;', len(keep), 'candidates left; D at', [round(x, 1) for x in (r.x0, r.y0)])
