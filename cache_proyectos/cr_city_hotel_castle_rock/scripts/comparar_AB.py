"""CR City Hotel - comparación A vs B por programa (paso 4). Empareja walls por hoja + orientación + eje (c) + traslape
(lo/hi). Compara type_id, length_ft (|Δ| <= 2 %), caras con board y capas por cara, altura por cara. Escribe
etapas/3_revision/comparacion_AB.json + .md"""
import json, sys, os
W = '/root/cr/work/etapas'
def load(l, f):
    p = f'{W}/2_lectura/{l}/{f}.json'
    return json.load(open(p)) if os.path.exists(p) else None
def norm(b):
    """banda traspuesta (c0/c1 = extensión, lo/hi = caras) -> se corrige: las caras son el tramo corto"""
    if b and (float(b['c1']) - float(b['c0'])) > (float(b['hi']) - float(b['lo'])):
        b = dict(b, c0=b['lo'], c1=b['hi'], lo=b['c0'], hi=b['c1'], traspuesta_corregida=True)
    return b
def cen(b): return (float(b['c0']) + float(b['c1'])) / 2
def ov(a, b):
    return max(0.0, min(a['hi'], b['hi']) - max(a['lo'], b['lo']))
def bfaces(w):
    return [f for f in (w.get('faces') or []) if int(f.get('layers') or 0) > 0]
res = {}
for fl in ('L1', 'L2', 'L3', 'L4'):
    A, B = load('A', fl), load('B', fl)
    if not A or not B:
        res[fl] = {'falta': 'A' if not A else 'B'}; continue
    wa, wb = A['walls'], B['walls']; usados = set(); pares = []; solo_a = []
    for a in wa:
        ba = norm(a.get('band') or {})
        best, bo = None, 0
        for j, b in enumerate(wb):
            if j in usados: continue
            bb = norm(b.get('band') or {})
            if not ba or not bb or ba.get('ori') != bb.get('ori') or a.get('sheet') != b.get('sheet'): continue
            if abs(cen(ba) - cen(bb)) > 8: continue
            o = ov(ba, bb)
            lmin = min(ba['hi'] - ba['lo'], bb['hi'] - bb['lo'])
            if lmin > 0 and o / lmin > 0.5 and o > bo: best, bo = j, o
        if best is None: solo_a.append(a['id']); continue
        usados.add(best); b = wb[best]
        la, lb = float(a.get('length_ft') or 0), float(b.get('length_ft') or 0)
        fa, fb = bfaces(a), bfaces(b)
        ha = sorted(round(float(f.get('height_ft') or 0), 2) for f in fa); hb = sorted(round(float(f.get('height_ft') or 0), 2) for f in fb)
        ya = sorted(int(f['layers']) for f in fa); yb = sorted(int(f['layers']) for f in fb)
        dif = []
        if a.get('type_id') != b.get('type_id'): dif.append('type')
        if max(la, lb) and abs(la - lb) / max(la, lb) > 0.02: dif.append('length')
        if len(fa) != len(fb) or ya != yb: dif.append('faces/layers')
        if any(abs(x - y) > 0.05 for x, y in zip(ha, hb)): dif.append('height')
        pares.append({'A': a['id'], 'B': b['id'], 'sheet': a.get('sheet'), 'type_A': a.get('type_id'), 'type_B': b.get('type_id'),
                      'lf_A': la, 'lf_B': lb, 'layers_A': ya, 'layers_B': yb, 'h_A': ha, 'h_B': hb, 'dif': dif})
    solo_b = [wb[j]['id'] for j in range(len(wb)) if j not in usados]
    res[fl] = {'pares': pares, 'solo_A': solo_a, 'solo_B': solo_b,
               'coinciden': sum(1 for p in pares if not p['dif']),
               'dif_por_tipo': {k: sum(1 for p in pares if k in p['dif']) for k in ('type', 'length', 'faces/layers', 'height')},
               'lf_A': round(sum(float(w.get('length_ft') or 0) for w in wa), 1), 'lf_B': round(sum(float(w.get('length_ft') or 0) for w in wb), 1)}
os.makedirs(f'{W}/3_revision', exist_ok=True)
json.dump(res, open(f'{W}/3_revision/comparacion_AB.json', 'w'), indent=1)
for fl, r in res.items():
    if 'falta' in r: print(fl, 'falta lectura', r['falta']); continue
    print(fl, 'pares', len(r['pares']), 'coinciden', r['coinciden'], r['dif_por_tipo'], 'soloA', len(r['solo_A']), 'soloB', len(r['solo_B']), 'LF A/B', r['lf_A'], r['lf_B'])
