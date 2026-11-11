"""Grand Kia: paso 12 coverage list = every verified detail bubble of the trade sheets (burbujas_verificadas.json) with its
destination when it is not ours (callouts_no_aplican.json), else checked against the canon / Excel by its N/SHEET."""
import json, os
W = '/root/gk/work'
B = json.load(open(f'{W}/burbujas/burbujas_verificadas.json'))
NA = json.load(open(f'{W}/burbujas/callouts_no_aplican.json'))
na = {}
for h, xs in NA.items():
    if isinstance(xs, dict):
        for n_, why in xs.items():
            na[f"{n_}/{h}"] = str(why)
L, seen = [], set()
for h, xs in B.items():
    if not isinstance(xs, list):
        continue
    for x in xs:
        if not (isinstance(x, dict) and x.get('n') and x.get('hoja')):
            continue
        ref = f"{x['n']}/{x['hoja']}"
        if ref in seen:
            continue
        seen.add(ref)
        it = {"sheet": h, "type": ref, "text": str(x.get('texto') or x.get('titulo') or ref)}
        if x['hoja'] == 'A520':
            it["destination"] = "n/a - sheet A520 is not in the set (README 'Missing sheet A520'); framing taken from A310-A312 / S sheets (ALC-03)"
        elif ref in na:
            it["destination"] = f"n/a - {na[ref]}"
        L.append(it)
os.makedirs(f'{W}/etapas/12_cobertura', exist_ok=True)
json.dump(L, open(f'{W}/etapas/12_cobertura/lista.json', 'w'), indent=1, ensure_ascii=False)
print(len(L))
