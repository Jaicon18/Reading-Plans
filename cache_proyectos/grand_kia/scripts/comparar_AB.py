"""Grand Kia - comparación A vs B por programa (geometría de banda + type + LF + H), todas las zonas juntas
(un wall en el borde de zona puede estar en Z1 de un lector y Z2 del otro). Salida 3_revision/comparacion_AB.json + revision.md"""
import json, glob, os
W = '/root/gk/work/etapas'
def carga(l):
    out = []
    for f in sorted(glob.glob(f'{W}/2_lectura/{l}/Z*.json')):
        z = os.path.basename(f)[:-5]
        for w in json.load(open(f))['walls']:
            w['_zona'] = z; out.append(w)
    return out
def nb(b):
    b = dict(b); c0, c1, lo, hi = map(float, (b['c0'], b['c1'], b['lo'], b['hi']))
    if c1 - c0 > hi - lo: c0, c1, lo, hi = lo, hi, c0, c1
    return b.get('ori'), (c0 + c1) / 2, lo, hi
def score(a, b):
    if a.get('page') != b.get('page'): return None
    oa, ca, la, ha = nb(a['band']); ob, cb, lb, hb = nb(b['band'])
    if oa != ob or abs(ca - cb) > 12: return None
    ov = min(ha, hb) - max(la, lb)
    if ov <= 0: return None
    return ov / max(ha - la, hb - lb, 1e-6)
A, B = carga('A'), carga('B')
pares, usadoB = [], set()
cands = sorted(((score(a, b) or 0, i, j) for i, a in enumerate(A) for j, b in enumerate(B)), reverse=True)
usadoA = set()
for s, i, j in cands:
    if s < 0.3: break
    if i in usadoA or j in usadoB: continue
    usadoA.add(i); usadoB.add(j); pares.append((i, j, s))
def f(x):
    try: return float(x)
    except: return None
res = {'coinciden': [], 'difieren': [], 'solo_A': [], 'solo_B': []}
for i, j, s in pares:
    a, b = A[i], B[j]
    la, lb, ha, hb = f(a.get('length_ft')), f(b.get('length_ft')), f(a.get('height_ft')), f(b.get('height_ft'))
    dl = (abs(la - lb) / max(la, lb)) if la and lb else 1
    dh = abs(ha - hb) if ha and hb else 99
    ta, tb = a.get('tag') or a.get('type'), b.get('tag') or b.get('type')
    fa, fb = len(a.get('faces') or []), len(b.get('faces') or [])
    r = dict(A=a['id'], B=b['id'], zonaA=a['_zona'], zonaB=b['_zona'], page=a.get('page'), typeA=ta, typeB=tb,
             LF_A=la, LF_B=lb, dLF_pct=round(dl * 100, 1), H_A=ha, H_B=hb, dH=round(dh, 2), facesA=fa, facesB=fb, overlap=round(s, 2))
    ok = ta == tb and dl <= 0.02 and dh <= 0.5 and fa == fb
    res['coinciden' if ok else 'difieren'].append(r)
for i, a in enumerate(A):
    if i not in usadoA: res['solo_A'].append(dict(A=a['id'], zona=a['_zona'], page=a.get('page'), type=a.get('tag') or a.get('type'), LF=a.get('length_ft'), loc=a.get('location')))
for j, b in enumerate(B):
    if j not in usadoB: res['solo_B'].append(dict(B=b['id'], zona=b['_zona'], page=b.get('page'), type=b.get('tag') or b.get('type'), LF=b.get('length_ft'), loc=b.get('location')))
os.makedirs(f'{W}/3_revision', exist_ok=True)
json.dump(res, open(f'{W}/3_revision/comparacion_AB.json', 'w'), indent=1)
print({k: len(v) for k, v in res.items()}, 'A', len(A), 'B', len(B))
import collections
tA = collections.Counter(); tB = collections.Counter()
for a in A: tA[a.get('tag') or a.get('type')] += f(a.get('length_ft')) or 0
for b in B: tB[b.get('tag') or b.get('type')] += f(b.get('length_ft')) or 0
for t in sorted(set(tA) | set(tB), key=str): print(t, round(tA[t], 1), round(tB[t], 1))
