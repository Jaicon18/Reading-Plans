"""Grand Kia U-142: position of every schedule row / partition type on its printed sheet (for SCHEDULES_REVISADOS).
Sheets A140 / A131 / A400 / A530 / A540 / A550 / A551 / A521 carry text as vector curves (BE-GK02): the gate looks for the row
label on the clean set, which has no text, so the positions come from the OCR layer (GK_set_OCR.pdf) with the same word helper
the gate uses (compuerta_entrega._palabras_pagina, unrotated page coordinates). Sheet field = the printed sheet label
(the '46/A550' style reference is kept in sheet_ref)."""
import json, re, sys
sys.path.insert(0, '/root/gk/skill/take-off-metal-frame-drywall/tools')
import compuerta_entrega as CE, pymupdf
W = '/root/gk/work'
d = pymupdf.open(f'{W}/plans/GK_set_OCR.pdf'); sm = json.load(open(f'{W}/sheetmap.json'))
cache = {}


def words(h):
    if h not in cache:
        cache[h] = CE._palabras_pagina(d[sm[h] - 1], False)
    return cache[h]


def norm(t):
    return t.strip(".:,()").upper().replace("$", "S")


def buscar(h, tok, prev=None):
    ws = words(h)
    for i, w in enumerate(ws):
        if norm(w[4]) == tok.upper() and (prev is None or (i and norm(ws[i - 1][4]) == prev)):
            q = pymupdf.Point((w[0] + w[2]) / 2, (w[1] + w[3]) / 2) * d[sm[h] - 1].rotation_matrix   # visible pt (the gate derotates)
            return (q.x, q.y)
    return None


BV = json.load(open(f'{W}/burbujas/burbujas_verificadas.json'))
POS = json.load(open(f'{W}/indep/schedules_pos_ojo.json')) if __import__('os').path.isfile(f'{W}/indep/schedules_pos_ojo.json') else {}
F = json.load(open(f'{W}/indep/fichas.json'))
nf = 0
BB = {r['type']: r['bbox'] for x in json.load(open(f'{W}/entrega_schedules_materiales.json')) if x['sheet'] == 'A550' for r in x['rows']}
for tid, t in F['types'].items():
    b = BB.get(tid)      # verified 'TYPE X:' label box on A550 (visible pt): the circle sits on the label
    p = ((b[0] + 22, (b[1] + b[3]) / 2)) if b else None
    t['hoja'] = 'A550'
    if p:
        t['pos'] = [round(p[0], 1), round(p[1], 1)]; nf += 1
json.dump(F, open(f'{W}/indep/fichas.json', 'w'), indent=1, ensure_ascii=False)
S = json.load(open(f'{W}/indep/schedules_indep.json'))
ns = nt = 0
for s in S['schedules']:
    ref = s.get('sheet_ref') or s['sheet']
    hs = [h for h in re.findall(r"\b([A-Z]\d{3})\b", ref) if h in sm]
    if not hs:
        continue
    s['sheet_ref'] = ref; s['sheet'] = hs[0]
    for r in s['rows']:
        nt += 1
        toks = [x for x in re.split(r"[ ,;/()+]+", str(r['id'])) if x and x.upper() not in ('ALSO', 'SIM')]
        p = None
        b = BB.get(str(r['id'])) if hs[0] == 'A550' else None
        if f"{hs[0]}:{r['id']}" in POS:
            b = None
        if b:
            p = (b[0] + 22, (b[1] + b[3]) / 2)
        md = re.match(r"(\d+)(?:,[\d,]+)?/(A\d{3})\b", str(r['id']))
        if not p and md:     # detail row: its title bubble (bottom-left of the verified detail box, burbujas_verificadas.json)
            bx = next((x for x in BV.get(md.group(2), []) if str(x.get('detalle_existe')) == md.group(1)), None)
            if bx:
                p = (bx['x'] + 40, bx['y1'] - 28)
        if f"{hs[0]}:{r['id']}" in POS:
            p = tuple(POS[f"{hs[0]}:{r['id']}"])
        for h in ([] if p else hs):
            for tk in toks[:3]:
                p = buscar(h, tk)
                if p:
                    break
            if p:
                break
        if p:
            r['x'], r['y'] = round(p[0], 1), round(p[1], 1); ns += 1
json.dump(S, open(f'{W}/indep/schedules_indep.json', 'w'), indent=1, ensure_ascii=False)
print(f"types {nf}/{len(F['types'])}, schedule rows {ns}/{nt}")
