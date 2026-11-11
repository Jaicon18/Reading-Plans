"""BE-GK15: compuerta_entrega.py texto takes sheet numbers from the OCR of the title block ('A51', 'A350' on curve-text sheets).
Relabel every per-sheet dict of set_texto.json (hojas, burbujas) with the verified sheet map, by page order."""
import json, sys
p, smp = sys.argv[1], sys.argv[2]
t = json.load(open(p)); sm = json.load(open(smp))
inv = {}
for k, v in sm.items():
    if isinstance(v, int) and ' ' not in k:
        inv.setdefault(v, k)
inv[41] = 'A521-DUP'
old = list(t['hojas'].keys())
mp = {k: inv.get(i, k) for i, k in enumerate(old, start=1)}
t['hojas'] = {mp[k]: v for k, v in t['hojas'].items()}
if isinstance(t.get('burbujas'), dict):
    t['burbujas'] = {mp.get(k, k): v for k, v in t['burbujas'].items()}
t['sheetmap_relabel'] = {k: v for k, v in mp.items() if k != v}
json.dump(t, open(p, 'w'), ensure_ascii=False)
print(len(t['sheetmap_relabel']), 'labels fixed:', t['sheetmap_relabel'])
