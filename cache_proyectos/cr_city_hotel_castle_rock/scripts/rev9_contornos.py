#!/usr/bin/env python3
"""rev9 (COORDINACIÓN, cielos B): aplica los contornos MEDIDOS en vectores (etapas/4_canon/rev9/contornos_*.json, caras de los
walls, imagen por cuarto) a ceilings[] del canon: area_sf = área del contorno [DERIVED] con su operación y N/HOJA, chequeo contra el
SF impreso de la etiqueta del cuarto (contorno.sf_referencia / comparado_sf / cuadra_con), polígono para rcp_polys.py
(contorno_polygon en coords de su hoja). Hallazgo rev9: el SF impreso de las unidades NO es consistente (unas lo cuentan sin el
bath, otras con el bath); por eso la cantidad es el contorno medido y el impreso queda como chequeo."""
import json, glob, re, os
W = '/root/cr/work'
CP = f'{W}/etapas/4_canon/takeoff_canon.json'
c = json.load(open(CP))
K = {}
for f in sorted(glob.glob(f'{W}/etapas/4_canon/rev9/contornos_*.json')):
    for _k, _v in json.load(open(f)).items():
        K.setdefault(_k, {}).update(_v)
for _v in K.values():   # N/HOJA limpia (la primera cita N/HOJA del texto del medidor)
    _m = re.search(r"\b\d{1,2}/A\d\.\d\d\b", str(_v.get('nhoja') or ''))
    _v['nhoja'] = _m.group(0) if _m else _v.get('sheet')

AJ = json.load(open(f'{W}/etapas/4_canon/rev9/ajustes.json')) if os.path.isfile(f'{W}/etapas/4_canon/rev9/ajustes.json') else {}
def _ar(P):
    return sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P))) / 2


def keyhole(O, holes):
    """un solo anillo: exterior + cada hueco por un puente de ancho cero (hueco en sentido inverso al exterior)."""
    R = [list(q) for q in O]
    for H in holes:
        H = [list(q) for q in H]
        if (_ar(H) > 0) == (_ar(R) > 0):
            H = H[::-1]
        i, j = min(((i, j) for i in range(len(R)) for j in range(len(H))), key=lambda t: (R[t[0]][0] - H[t[1]][0]) ** 2 + (R[t[0]][1] - H[t[1]][1]) ** 2)
        R = R[:i + 1] + H[j:] + H[:j + 1] + R[i:]
    return R


def unir(piezas):
    """piezas disjuntas en un anillo: puente de ancho cero, cada pieza en el MISMO sentido (las áreas se suman)."""
    R = [list(q) for q in piezas[0]]
    for H in piezas[1:]:
        H = [list(q) for q in H]
        if (_ar(H) > 0) != (_ar(R) > 0):
            H = H[::-1]
        i, j = min(((i, j) for i in range(len(R)) for j in range(len(H))), key=lambda t: (R[t[0]][0] - H[t[1]][0]) ** 2 + (R[t[0]][1] - H[t[1]][1]) ** 2)
        R = R[:i + 1] + H[j:] + H[:j + 1] + R[i:]
    return R


# misc dibujado con el contorno FS-1 del mismo cuarto (CLG-L3-103 = Linen 322): mismo anillo medido y misma área
for _rid, _room in (("CLG-L3-103", "L3 322 Linen"),):
    if _room in K and _rid not in K:
        _k = K[_room]
        K[_rid] = {"sheet": _k['sheet'], "polygon": _k['polygon'], "area_cargar_sf": _k['area_sf'], "nhoja": _k.get('nhoja'), "cuadra_con": "cargado"}
json.dump({r: K[r] for r in ("CLG-L3-103",) if r in K}, open(f'{W}/etapas/4_canon/rev9/contornos_zDERIV.json', 'w'), indent=1)

n = 0
for x in c.get('ceilings') or []:
    k = K.get(x['room'])
    if not k or not (k.get('polygon') or k.get('polygons')):
        continue
    aj = AJ.get(x['room'], {})
    A = round(float(aj.get('area_sf', k['area_sf'])), 2)
    old = x['area_sf']
    ref = k.get('sf_impreso')
    cq = k.get('cuadra_con') or ''
    if aj.get('polygon') and k.get('sf_impreso'):
        cq = cq or 'impreso excl. bath'
    comp = (k.get('contorno_menos_bath_sf') if cq == 'impreso excl. bath' else
            (k.get('contorno_sf') or k['area_sf']) if cq == 'impreso incl. bath' else k['area_sf'])
    x['contorno'] = {"area_medida_sf": A, "sheet": k['sheet'], "nhoja": k.get('nhoja'), "metodo": k.get('metodo'),
                     "sf_referencia": ref, "comparado_sf": comp if ref else None, "cuadra_con": k.get('cuadra_con'),
                     "img": k.get('img'), "nota": (aj.get('nota') or k.get('nota')) if (cq in ('NO CUADRA', 'cargado') or aj) else None,
                     "cargado_rev8": old}
    x['contorno_polygon'] = aj.get('polygon') or k.get('polygon') or k.get('polygons')
    if k.get('hueco_restado') and not aj.get('polygon'):
        x['contorno_polygon'] = keyhole(k['polygon'], [k['hueco_restado']])
    if k.get('polygons') and not k.get('polygon') and len(k['polygons']) > 1:
        x['contorno_polygon'] = unir(k['polygons'])
    if k.get('polygon_A3_01') and k.get('holes_restados'):
        dx, dy = k['offset_A2_02_a_A3_01']
        hs_ = [[[q[0] + dx, q[1] + dy] for q in H] for H in k['holes_restados'].values()]
        x['contorno_polygon'] = keyhole(k['polygon_A3_01'], hs_); x['contorno']['sheet'] = 'A3.01'
    x['area_sf'] = A
    op = aj.get('op') or f"contour measured in vectors on {str(k.get('nhoja')).split(' (')[0]} at the wall faces = {k['area_sf']} SF"
    _cq = {'impreso excl. bath': 'printed SF matches the contour less the bath', 'impreso incl. bath': 'printed SF matches the contour incl. the bath',
           'NO CUADRA': 'printed SF does not match (see Review notes)', 'cargado': 'matches the previous quantity', 'impreso': 'matches the printed SF'}.get(k.get('cuadra_con'), '')
    chk = (f"; printed room SF {ref}: {_cq} ({k.get('err_pct')} %)" if ref else "")
    x['source'] = re.sub(r"\[CONFIRMED\] area [\d.]+ SF \([^|]*\)|\[DERIVED\] area [\d.]+ SF \([^|]*\)",
                         f"[DERIVED] area {A} SF ({op}{chk}; previous quantity {old} SF)", x['source'], count=1)
    if f"area {A} SF" not in x['source']:
        x['source'] = f"[DERIVED] area {A} SF ({op}{chk}; previous quantity {old} SF) | " + x['source']
    n += 1
# misc (CLG / CAN / SOF / BW): cantidad = contorno / recorrido MEDIDO (area_cargar_sf o lf); todas las familias del renglón se
# reescalan con la misma razón (board, tees, RC, hanger, track); la operación queda escrita con la medición y el valor rev8.
MISC = {}
for m in c['misc_items']:
    MISC.setdefault(str(m['ref']).rsplit(' ', 1)[0] if ' ' in str(m['ref']) else m['ref'], []).append(m)
def _rid(ref):
    return re.match(r"((?:CLG|SOF|CAN|BW)-[A-Z0-9]+-[A-Z0-9]+)", ref)
nm = 0
for rid, k in K.items():
    if not re.match(r"(CLG|SOF|CAN|BW)-", rid):
        continue
    rows = [m for m in c['misc_items'] if str(m['ref']).startswith(rid + ' ')]
    bd = next((m for m in rows if m['ref'] == rid + ' board'), None)
    if not bd:
        continue
    lay = 1
    ml = re.search(r"x\s*(\d+)\s*layer", str(bd['op']))
    if ml: lay = int(ml.group(1))
    if k.get('lines'):
        import math as _mm
        _e = 18.0 if k['sheet'].startswith(('A6', 'A7')) else 9.0
        mo = re.match(r"\s*(\d+\.?\d*)", str(bd['op'])); old = float(mo.group(1)); u = 'LF'
        new = round(sum(_mm.dist(a, b) for a, b in k['lines']) / _e, 2)
    else:
        if 'area_cargar_sf' not in k: continue
        old = round(float(bd['qty']) / lay, 2); new = round(float(k['area_cargar_sf']) * float(k.get('factor_pendiente') or 1), 2); u = 'SF'
    if abs(new - old) < 0.005 and not k.get('factor_pendiente'):
        continue
    f = new / old
    for m in rows:
        if 'angle' in m['familia'].lower():
            continue
        m['qty'] = round(float(m['qty']) * f, 2)
        nota = (f"{'run' if u == 'LF' else 'contour'} measured in vectors on {str(k.get('nhoja')).split(' (')[0]} = {new} {u}"
                + (f" (plan {k['area_cargar_sf']} SF x slope factor {k['factor_pendiente']})" if k.get('factor_pendiente') else "") + f"; previous quantity {old} {u}")
        if u == 'LF':     # rev11 (F4): se reemplaza el LF viejo donde esté (no el primer número: '2 lines x LF')
            op = str(m['op']).replace(f"{old} LF", f"{new} LF", 1) if f"{old} LF" in str(m['op']) else re.sub(r"^\s*[\d.]+", f"{new}", str(m['op']), count=1)
            op = re.sub(r"=\s*[\d.,]+", f"= {m['qty']}", op, count=1)
        elif m is bd:
            op = f"{new} SF x {lay} layer(s) = {m['qty']}"
        else:
            op = f"{new} SF x {round(float(m['qty']) / new, 4)} = {m['qty']}"
        m['op'] = f"{op} | {nota}"
    # rev11 (F4): los accesorios del mismo elemento (trim_items '<id> ...': corner bead, trim) se recalculan con el largo nuevo
    if u == 'LF':
        for t_ in c.get('trim_items') or []:
            if str(t_.get('ref', '')).startswith(rid + ' ') and t_.get('lf'):
                t_['lf'] = round(float(t_['lf']) * f, 2)
                t_['op'] = f"{t_['lf']} LF soffit length x 1 edge = {t_['lf']} (run measured in vectors on {k.get('nhoja')}; previous quantity {old} LF)"
    nm += 1
print(nm, 'misc reescalados a la medición')
# CLG-L1-COFRES: NO se carga (CB_CR_R6_E1 / R80e.160 E1: el fondo del cofre = cara inferior del RATED ASSEMBLY 2/A7.31 = la membrana
# FS-1 de L1 ya cargada en 'L1 FS-1 membrane'). Era: fondos de los 10 cofres del lobby GYP-1 12'-0 3/4" (tag 1/A7.31, cotas 2/A7.31,
# 7/A7.31) no tenían renglón; solo sus caras verticales (SOF-L1-01). Board + suspensión como el campo CLG-L1-12; angle = perímetro de
# los fondos medidos; hanger wire no se carga: el fondo queda a la cara inferior de la estructura del lobby (2/A7.31 / 7/A7.31).
kc = K.get('CLG-L1-COFRES')
if False and kc and not any(str(m['ref']).startswith('CLG-L1-COFRES ') for m in c['misc_items']):
    import math as _m
    A = round(float(kc['area_cargar_sf']), 2)
    per = round(sum(sum(_m.dist(P[i], P[(i + 1) % len(P)]) for i in range(len(P))) for P in kc['polygons_final']) / 18.0, 2)
    base = {m['ref'].split(' ', 1)[1]: m for m in c['misc_items'] if str(m['ref']).startswith('CLG-L1-12 ')}
    src = (f"L1 LOBBY - coffer bottoms (10): A7.31 [DERIVED] area {A} SF (inner rectangles of the 10 coffers measured in vectors on "
           f"1/A7.31, /324) | GYP-1 | [CONFIRMED] height 12.0625 (GYP-1 12'-0 3/4\" tag 1/A7.31; 2/A7.31, 7/A7.31)")
    det = "1/A7.31, 2/A7.31, 7/A7.31 (GYP-1 12'-0 3/4\" coffer bottoms)"
    for fam, q, op in (("board", A, f"{A} SF x 1 layer(s) = {A}"), ("main tee", round(A / 4.0, 2), f"{A} SF / 4.0 ft o.c. = {round(A / 4.0, 2)}"),
                       ("cross tee", round(A / 1.333, 2), f"{A} SF / 1.333 ft o.c. = {round(A / 1.333, 2)}"),
                       ("angle molding", per, f"perimeter of the 10 measured coffer bottoms on 1/A7.31 / 18 pt/ft = {per} LF")):
        b = base.get(fam)
        if b:
            c['misc_items'].append(dict(b, ref=f"CLG-L1-COFRES {fam}", qty=q, op=op, detail=det,
                                        source=src + (" | hanger wire not loaded: the coffer bottom sits at the underside of the lobby structure (2/A7.31, 7/A7.31)" if fam == 'board' else "")))
    print('CLG-L1-COFRES agregado', A, 'SF', per, 'LF')
# rev10 (auditoría U-138, E1): RFI-27 / DA-6 retirados - A0.08 FS-1 'LEVEL 2, 3, 4 / THROUGHOUT / L546' dibuja la membrana Type C
# continua y debajo 'DROPPED CEILING IS NOT A COMPONENT OF THE RATED ASSEMBLY. REFER TO CEILING PLANS AND DETAILS FOR MATERIALS.'
for x in c.get('ceilings') or []:
    if x.get('contorno') and x['room'][:2] in ('L2', 'L3') and (x.get('assembly') or {}).get('id') == 'FS-1':
        x['source'] = str(x['source']) + (" | [CONFIRMED] membrane continuous over the bath dropped GYP-1: A0.08 FS-1 detail (LEVEL 2, 3, 4 THROUGHOUT, L546) "
                                          "draws the 5/8\" Type C ceiling with the dropped ceiling below it and the note 'DROPPED CEILING IS NOT A COMPONENT OF THE RATED ASSEMBLY'")
c['deduct_alternates'] = [d for d in c.get('deduct_alternates') or [] if d.get('id') != 'DA-6']
json.dump(c, open(CP, 'w'), indent=1)
print(n, 'ceilings con contorno medido de', len(c.get('ceilings') or []))
