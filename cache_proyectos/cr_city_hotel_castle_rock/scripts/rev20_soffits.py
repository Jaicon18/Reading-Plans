"""CR City Hotel rev20 (12-nov): doble lectura ciega U-176 (1) de los 14 renglones de soffits / beam wraps (BE-CR35) +
decisiones de COORDINACIÓN 12-nov (U-171 / U-112: las deciden las reglas).
- Banda del corredor 7/A7.23 (SOF-L2-01, SOF-L2-02, SOF-L3-316, SOF-L3-318, SOF-L4-02): H-A = H-B = 23 1/4" por lado =
  cara al corredor 6 1/2" + fondo de caja 4 1/2" + cara de caja hacia el cove 4 1/2" + fondo del cove 7 3/4" = 1.9375 ft
  (cada cara con su cota impresa en 7/A7.23); la cara contra la pared = 'WOOD WALL PANEL RE: ELEVATIONS' (fuera); el LF cargado ya
  suma los dos lados. DIFFUSER BOX 5 1/4": bruto (conservador) + Review Item con su delta (lado izquierdo 1.50 donde hay diffuser).
- Smoke-curtain housing 12/A9.03 (6 renglones SC): sin cotas impresas; H-A 3.06 / H-B 3.02 medidos a 1 1/2" = 1'-0": el mayor 3.06.
- Coffers SOF-L1-01 5/A7.31: manda la cota impresa (U-017): cara '10 3/4"' + la mitad del fondo compartido 8 1/2" (7 1/2" + 2 x 1/2"
  impresos) = 15" = 1.25 ft por LF de perímetro de coffer; la lectura medida (11.24" de cara, 1.29) queda como Review Item.
- Beam wraps BW-L1-RETAIL: resolución viga por viga (scratchpad bw_resol/BW_RESOL.csv), si existe.
"""
import csv
import json
import os
import re

W = '/root/cr/work'
CP = f'{W}/etapas/4_canon/takeoff_canon.json'
C = json.load(open(CP))
IMG = f'{W}/etapas/4_canon/img/rev20'
CORR = ('SOF-L2-01', 'SOF-L2-02', 'SOF-L3-316', 'SOF-L3-318', 'SOF-L4-02')
SC = ('SOF-L2-SCN', 'SOF-L2-SCS', 'SOF-L3-SCN', 'SOF-L3-SCS', 'SOF-L4-SCN', 'SOF-L4-SCS')
W_CORR, W_SC, W_COF = 1.9375, 5.04, 1.25   # SC: U-181 rev20 - la 5a cara (lado shaft, 23.73") que H-A / H-B omitieron
log = []


def lf_de(m):
    g = re.match(r"\s*([\d.]+)\s*LF", str(m.get('op') or ''))
    return float(g.group(1)) if g else None


for m in C['misc_items']:
    ref = str(m.get('ref'))
    base = ref[:-6] if ref.endswith(' board') else None
    if base in CORR:
        L = lf_de(m)
        q = round(L * W_CORR, 2)
        log.append(f"{base}: {m['qty']} -> {q} SF")
        m['qty'] = q
        m['op'] = (f"{L} LF x 1.9375 ft (per side: 6 1/2\" corridor face + 4 1/2\" box bottom + 4 1/2\" box face to cove + 7 3/4\" cove bottom = 23 1/4\") = {q}")
        _viejo = [x for x in str(m.get('source') or '').split(' | rev20')[0].split(' | ')
                  if x.strip() and not re.search(r'0\.375 ft printed|vertical face 2" \+ box bottom|DIFFUSER BOX is HVAC', x)]   # rev19: anchos viejos
        m['source'] = (f"{' | '.join(_viejo)} | rev20 (U-176 double blind reading H-A = H-B): 7/A7.23 WALL DETAIL - "
                       "CORRIDOR CEILING printed '6 1/2\"', '4 1/2\"' (box bottom), '4 1/2\"' (box face, right side; left = 6 1/2\" - '2\"'), "
                       "'7 3/4\"' (cove bottom); face against the wall = 'WOOD WALL PANEL RE: ELEVATIONS' (not drywall); 1/A7.23 RCP '8' - 4 1/2\"' "
                       "= bottom of both boxes (8'-11\" - 6 1/2\"); DIFFUSER BOX 5 1/4\" loaded gross (Review Item)")
    elif base in SC:
        L = lf_de(m)
        q = round(L * W_SC, 2)
        log.append(f"{base}: {m['qty']} -> {q} SF")
        m['qty'] = q
        m['op'] = f"{L} LF x 5.04 ft = {q}"
        m['source'] = ("12/A9.03 'SOFFIT AROUND HOUSING' [DERIVED] developed width measured at the printed scale 1 1/2\" = 1'-0\" (no dimension "
                       "printed): outer face 14.87\" + bottom 4.49\" + inner face 14.37\" + return 3.00\" + shaft-side face 23.73\" (gypsum on wood blocks "
                       "in front of the MASONRY SHAFT WALL, down to the ceiling) = 60.46\" = 5.04 ft | rev20: H-A 3.06 / H-B 3.02 omitted the shaft-side "
                       "face; the U-181 independent audit re-measured it (rev19 loaded it: 5.039)")
    elif base == 'SOF-L1-01':
        L = lf_de(m)
        q = round(L * W_COF, 2)
        log.append(f"{base}: {m['qty']} -> {q} SF")
        m['qty'] = q
        m['op'] = f"{L} LF x 1.25 ft (10 3/4\" printed face + 8 1/2\" shared bottom / 2 = 15\") = {q}"
        m['source'] = (f"{str(m.get('source') or '').split(' | rev20')[0]} | rev20 (U-176 double blind reading, U-017 printed governs): 5/A7.31 "
                       "DETAIL - LOBBY CEILING printed '10 3/4\"' downstand face and bottom '7 1/2\"' + 2 x '1/2\"' = 8 1/2\" shared by two coffers "
                       "(LF = sum of each coffer perimeter, so half the bottom per LF); the measured 11.24\" face (1.29 ft) is a Review Item")
    elif ref == 'SOF-L1-01 cripples':
        g = re.search(r"= (\d+) cripple studs", str(m.get('op')))
        if g:
            n = int(g.group(1)); q = round(n * 0.8958, 2)
            log.append(f"{ref}: {m['qty']} -> {q} LF")
            m['qty'] = q
            m['op'] = re.sub(r"x vertical face [\d.]+ ft = [\d.]+", f"x vertical face 0.8958 ft (5/A7.31 printed '10 3/4\"') = {q}", str(m['op']))
for s in C.get('framed_soffits') or []:
    sid = s.get('id')
    w = W_CORR if sid in CORR else W_SC if sid in SC else W_COF if sid == 'SOF-L1-01' else None
    if w:
        s['developed_width_ft'] = w
        s['developed_width_source'] = 'rev20 U-176 double blind reading (H-A / H-B), see the board misc_items op'

# beam wraps: resolución viga por viga (si ya está)
BW = '/tmp/claude-0/-home-user/18bfbfac-ecd6-55d5-8e44-1a0e0dafeecf/scratchpad/bw_resol/BW_RESOL.json'
if os.path.isfile(BW):
    r = json.load(open(BW))
    # U-181 rev20 (COORDINACIÓN: decide por la regla): la franja norte (vigas de borde, 68.8 LF) con la MISMA base que las interiores
    # (AISC d / bf exactos; UNA cara interior d - 19.25" + 1 1/8" (el otro lado es el muro exterior) + fondo bf + 2 1/4")
    AISC = {"W27X94": (26.92, 9.99), "W21X50": (20.83, 6.53), "W24X55": (23.57, 7.005)}
    NORTE = (("W27X94", 32.58), ("W21X50", 19.37), ("W24X55", 16.85))
    pn, sn = [], 0.0
    for b_, lf_ in NORTE:
        d_, bf_ = AISC[b_]; w_ = round(((d_ - 19.25 + 1.125) + (bf_ + 2.25)) / 12, 3); sn += lf_ * w_
        pn.append(f"{b_} {lf_} x {w_}")
    sn = round(sn, 2)
    sint = 282.85
    sf = round(sint + sn, 2); fin = round(sf / 223.03, 4)
    r['sf'], r['final'] = sf, fin
    r['op'] = r['op'].split('; + north edge')[0] + f"; + north edge beams 68.8 LF (one inside face d - 19.25\" + 1 1/8\" + bottom bf + 2 1/4\", AISC): {' + '.join(pn)} = {sn} = {sf}"
    r['op_alturas'] = f"{sf} / 223.03 = {fin}"
    json.dump(r, open(BW, 'w'), indent=1)
    for m in C['misc_items']:
        if m['ref'] == 'BW-L1-RETAIL board':
            log.append(f"BW-L1-RETAIL board: {m['qty']} -> {r['sf']} SF")
            m['qty'] = r['sf']
            m['op'] = f"223.03 LF x {r['final']} ft ({r['op']})"
            m['source'] = r['source']

C['rev20_cambios'] = log
json.dump(C, open(CP, 'w'), indent=1)
print("rev20 soffits:", *log, sep="\n  ")

# v81cf100 reglas.py 53.1: la imagen de un trim es un ARCHIVO que exista (CB-WIN-L2/3/4 apuntaban a la carpeta 2_lectura/img_ventanas)
C = json.load(open(CP))
nimg = 0
for t in C.get('trim_items') or []:
    if str(t.get('img') or '').rstrip('/') == '2_lectura/img_ventanas':
        t['img'] = '2_lectura/img_ventanas/A8.02_det1-2-3_RO_wrap_and_wood_trim.png'
        nimg += 1
json.dump(C, open(CP, 'w'), indent=1)
print(f"trim img -> archivo: {nimg}")

# U-181 rev20 (AMBER): el texto de SOF-L4-02 citaba el LF viejo 242.72 (LF de walls hacia 412); el cargado es el recorrido MEDIDO 343.67 LF
C = json.load(open(CP))
for m in C['misc_items']:
    if m['ref'] == 'SOF-L4-02 board':
        m['source'] = str(m['source']).replace(
            "LF NOT dimensioned on L4 RCP: loaded = corridor 412 wall LF 242.72 (resuelto_L4 walls facing 412), RFI-18",
            "LF NOT dimensioned on L4 RCP: loaded = run MEASURED in vectors on 1/A3.04 along the drawn soffit double line = 343.67 LF "
            "(contornos_MISC; replaces the earlier 242.72 wall-LF estimate), RFI-18")
json.dump(C, open(CP, 'w'), indent=1)
print("SOF-L4-02 source LF 343.67:", '242.72 (resuelto' not in json.dumps([m for m in C['misc_items'] if m['ref'] == 'SOF-L4-02 board']))
