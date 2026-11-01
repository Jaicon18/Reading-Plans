"""normalizar_union.py <dir> — en los fragmentos copiados para unir, las claves de texto libre (notes_info, notes,
doubts_info, scope_notes_info) pasan a {fragmento: contenido} para que `etapas.py unir` no falle por tipo distinto.
No cambia ningún dato medido."""
import json, os, sys
LIBRES = ('notes_info', 'doubts_info', 'scope_notes_info', 'notes', 'task', 'fragment')
d = sys.argv[1]
for f in sorted(os.listdir(d)):
    if not f.endswith('.json') or f.startswith('00_'): continue
    p = os.path.join(d, f); c = json.load(open(p))
    for k in LIBRES:
        if k in c and not (isinstance(c[k], dict) and list(c[k].keys()) == [f]):
            c[k] = {f: c[k]}
    json.dump(c, open(p, 'w'), indent=1, ensure_ascii=False)
print('normalizado', d)
