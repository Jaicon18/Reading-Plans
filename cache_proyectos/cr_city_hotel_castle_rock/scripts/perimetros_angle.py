#!/usr/bin/env python3
"""O1 (auditoría COORDINACIÓN 7-nov, rev6; U-114): el angle molding de cada ceiling sobre suspensión = PERÍMETRO REAL del
polígono del cuarto, nunca 4 x sqrt(área).
 (a) área medida como rectángulo(s) en vectores -> perímetro de la UNIÓN de esos rectángulos (raster 0.25 pt, aristas
     ortogonales contadas), escala de la división impresa en la operación (/324 -> 18 pt/ft, /81 -> 9 pt/ft); un rectángulo
     RESTADO (WS-1, stair, coffers) no suma perímetro de muro (ese borde lleva trim, no angle) -> solo el contorno exterior;
 (b) área = SF impreso -> flood fill desde el número del cuarto en el RCP (A3.0x, 1 px = 1 pt, muros dilatados 2 px): se acepta
     si el área del flood cae a +-15 % del SF cargado; perímetro = aristas del contorno + 16 pt (el flood queda 2 pt adentro de
     cada cara: 8 x 2 pt en un contorno ortogonal) / 9 pt/ft;
 (c) nada medible -> FALLA (no se usa sqrt).
Salida: canon en su lugar + etapas/4_canon/out/perimetros_angle.json."""
import json, re, math, sys
import numpy as np
W = '/root/cr/work'
CP = f'{W}/etapas/4_canon/takeoff_canon.json'
c = json.load(open(CP))
RX = re.compile(r"\(\s*(\d+\.?\d*)\s*-\s*(\d+\.?\d*)\s*\)\s*[*x]\s*\(\s*(\d+\.?\d*)\s*-\s*(\d+\.?\d*)\s*\)")
RCP = {'L1': ('A3.01', 21), 'L2': ('A3.02', 22), 'L3': ('A3.03', 23), 'L4': ('A3.04', 24)}
# SOLO contorno exterior: filas cuya operación resta piezas (WS-1, stair, coffers): el primer rectángulo es el cuarto
SOLO_PRIMERO = re.compile(r"(?i)minus|WS-1 oval|deducted|- WS-1")


def per_union(rects, s):
    x0 = min(r[0] for r in rects); y0 = min(r[2] for r in rects)
    q = 0.25
    X = int(math.ceil((max(r[1] for r in rects) - x0) / q)) + 2; Y = int(math.ceil((max(r[3] for r in rects) - y0) / q)) + 2
    g = np.zeros((Y, X), bool)
    for a, b, cc, d in rects:
        g[int(round((cc - y0) / q)) + 1:int(round((d - y0) / q)) + 1, int(round((a - x0) / q)) + 1:int(round((b - x0) / q)) + 1] = True
    e = np.count_nonzero(g[:, 1:] != g[:, :-1]) + np.count_nonzero(g[1:, :] != g[:-1, :])
    return e * q / s


def escala(src):
    m = re.search(r"/\s*(324|81)\b", src)
    return 18.0 if m and m.group(1) == '324' else 9.0


_rast = {}
FLOOD_POLY = {}


def flood(fl, room_txt, sf):
    import fitz
    from scipy import ndimage
    sh, pg = RCP[fl]
    if sh not in _rast:
        d = fitz.open(f'{W}/plans/bidset_SIN_MARKUPS.pdf'); p = d[pg]
        pix = p.get_pixmap(matrix=fitz.Matrix(1, 1), colorspace=fitz.csGRAY)
        a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width).copy()
        for w in p.get_text('words'):
            x0, y0, x1, y1 = [int(round(v)) for v in w[:4]]
            a[max(0, y0 - 1):y1 + 1, max(0, x0 - 1):x1 + 1] = 255
        dark = ndimage.binary_dilation(a < 160, iterations=2)
        lab, _ = ndimage.label(~dark)
        _rast[sh] = (p, lab)
    p, lab = _rast[sh]
    from scipy import ndimage
    best = None
    for r in p.search_for(room_txt):
        for cy in (int(r.y1 + 3), int(r.y0 - 3), int((r.y0 + r.y1) / 2)):
            cx = int((r.x0 + r.x1) / 2)
            L = lab[cy, cx]
            if not L:
                continue
            reg = ndimage.binary_fill_holes(lab == L)
            a_sf = reg.sum() / 81.0
            if a_sf > 3000:
                continue
            e = abs(a_sf - sf) / sf
            if best is None or e < best[0]:
                best = (e, reg, a_sf, (round(r.x0, 1), round(r.y0, 1)))
    if not best or best[0] > 0.15:
        return None, (best[0] if best else None)
    e, reg, a_sf, at = best
    import cv2
    cs, _ = cv2.findContours(reg.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnt = max(cs, key=cv2.contourArea)
    poly = cv2.approxPolyDP(cnt, 2.0, True)          # quita el serrucho del raster (tolerancia 2 pt)
    edges = round(cv2.arcLength(poly, True), 1)
    FLOOD_POLY[(sh, room_txt)] = poly.reshape(-1, 2).tolist()
    return {"perim_ft": round((edges + 16) / 9.0, 2), "flood_sf": round(a_sf, 1), "err": round(e, 3), "sheet": sh, "at": at,
            "op": f"flood fill on {sh} from room number '{room_txt}' at {at}: area {round(a_sf, 1)} SF vs loaded {sf} SF "
                  f"(err {round(e * 100, 1)} %); outer contour simplified to 2 pt {edges} pt + 16 pt (2 pt inside each face) = {edges + 16} pt / 9 pt/ft"}, e


# cuartos con área = SF impreso: rectángulos leídos en vectores, verificados con imagen (etapas/4_canon/img/rev6/O1_*.png)
MANUAL = {
    "CLG-L1-10": ("A2.01", [(1253.9, 1395.3, 316.7, 425.3)], 182.0, "WATER ENTRY 128: inside faces W / E / N wall and the toilets' N wall"),
    "CLG-L2-56": ("A3.02", [(812.8, 865.2, 466.0, 999.0), (724.0, 812.8, 544.0, 635.8)], 455.0,
                  "CORRIDOR 216: strip between the two SMOKE CURTAINS + the jog at the room tag"),
    "CLG-L3-87": ("A3.03", [(812.6, 866.0, 466.0, 999.0), (724.0, 812.6, 544.0, 635.8)], 455.0,
                  "CORRIDOR 316: same layout as 216 (455 SF printed on both floors)"),
    "CLG-L2-122": ("A3.02", [(759.0, 865.7, 373.4, 463.4)], 123.0, "CLEANING 215: N wall to the elevator front (smoke curtain is not a wall)"),
    "CLG-L4-117": ("A2.04", [(539.6, 704.7, 1077.5, 1140.9)], 129.0, "WOMEN 417 anteroom (the printed 129 SF; stalls 417.3 / 417.4 apart)"),
    "CLG-L4-118": ("A2.04", [(683.5, 784.0, 1143.4, 1221.7)], 94.0, "MEN 418 (stall 418.2 apart)"),
    "CLG-L4-119": ("A2.04", [(784.4, 797.0, 1142.4, 1224.0)], 11.0, "ELEC 421 (door 421.1)"),
}
import glob as _gl, math
KM = {}
for _f in sorted(_gl.glob('/root/cr/work/etapas/4_canon/rev9/contornos_*.json')):
    for _k, _v in json.load(open(_f)).items():
        KM.setdefault(_k, {}).update(_v)
for _v in KM.values():   # N/HOJA limpia (la primera cita N/HOJA del texto del medidor)
    _m = re.search(r"\b\d{1,2}/A\d\.\d\d\b", str(_v.get('nhoja') or ''))
    _v['nhoja'] = _m.group(0) if _m else _v.get('sheet')

board = {x['ref'][:-6]: x for x in c['misc_items'] if x.get('ref', '').startswith('CLG') and x['ref'].endswith(' board')}
LOG, FALLA = [], []
for x in c['misc_items']:
    if not (x.get('ref', '').endswith(' angle molding') and 'sqrt' in x.get('op', '')):
        continue
    ref = x['ref'][:-len(' angle molding')]
    b = board.get(ref)
    src = (b or {}).get('source', '')
    rects = [tuple(sorted((float(a), float(bb)))) + tuple(sorted((float(cc), float(d)))) for a, bb, cc, d in RX.findall(src)]
    rects = [(r[0], r[1], r[2], r[3]) for r in rects]
    mL = re.search(r"x(\d+\.?\d*)-(\d+\.?\d*), vertical coord (\d+\.?\d*)-(\d+\.?\d*)", src)
    if mL and not rects:
        rects = [tuple(float(v) for v in mL.groups())]
    rec = {"ref": ref, "antes": x['qty'], "op_antes": x['op']}
    de_fs1 = False
    # rev9: contorno MEDIDO (anillo exterior a caras de los walls; los huecos WS-1 / shaft llevan trim, no wall angle)
    _k = KM.get(ref)
    _pp = None
    if _k:
        _pp = ([_k['polygon']] if _k.get('polygon') else _k.get('polygons_final') or _k.get('polygons')); _sh = _k['sheet']
    elif not RX.findall(src) and not re.search(r"x(\d+\.?\d*)-(\d+\.?\d*), vertical coord", src) and ref not in MANUAL:
        # solo la fila que se dibujaba con la entrada FS-1 del MISMO cuarto (no un bath / closet dentro de la unidad)
        _nums = re.findall(r"\b([1-4]\d\d)\b", src.split('|')[0]); _fl = ref.split('-')[1]
        for cx in c.get('ceilings') or []:
            if (cx.get('contorno_polygon') and cx.get('floor', cx['room'][:2]) == _fl and _nums and re.search(rf"\b{_nums[0]}\b", cx['room'])
                    and not re.search(r"(?i)\b(bath|shower|toilet|closet)\b", src.split('|')[0])):
                _P = cx['contorno_polygon']; _pp = [_P] if isinstance(_P[0][0], (int, float)) else _P; _sh = cx['contorno']['sheet']; break
    if _pp:
        _s = 18.0 if _sh.startswith(('A6', 'A7')) else 9.0
        P = round(sum(sum(math.dist(Q[i], Q[(i + 1) % len(Q)]) for i in range(len(Q))) for Q in _pp) / _s, 2)
        x['qty'] = P
        x['op'] = f"perimeter of the contour measured in vectors on {(_k or {}).get('nhoja') or _sh} (wall faces, outer ring) / {_s:g} pt/ft = {P} LF"
        rec.update(despues=P, metodo="contorno", op=x['op']); LOG.append(rec)
        continue
    if not rects:   # polígono medido en la entrada FS-1 del mismo cuarto (218 / 318 / 322 / 323)
        nums = re.findall(r"\b([1-4]\d\d)\b", src.split('|')[0])
        fl_ = ref.split('-')[1]
        for cx in c.get('ceilings') or []:
            if cx.get('floor', cx['room'][:2]) == fl_ and nums and re.search(rf"\b{nums[0]}\b", cx['room']):
                rr = [tuple(sorted((float(a), float(bb)))) + tuple(sorted((float(cc), float(d)))) for a, bb, cc, d in RX.findall(cx.get('source', ''))]
                if rr:
                    rects = rr; de_fs1 = True; src = src + " | polygon of the FS-1 entry '" + cx['room'] + "': " + cx['source'][:160]
                    break
    if not rects and ref in MANUAL:
        sh_, rr, sf_, que = MANUAL[ref]
        a_ = sum((r[1] - r[0]) * (r[3] - r[2]) for r in rr) / 81.0
        P = round(per_union(rr, 9.0), 2)
        x['qty'] = P
        x['op'] = (f"perimeter of the room read in vectors on {sh_} ({que}): union of {'; '.join(f'({r[1]}-{r[0]}) x ({r[3]}-{r[2]})' for r in rr)} pt "
                   f"/ 9 pt/ft = {P} LF (check: polygon {round(a_, 1)} SF vs printed {sf_} SF)")
        rec.update(despues=P, metodo="vector", op=x['op'], area_chk=[round(a_, 1), sf_], hoja=sh_, rects=rr)
        LOG.append(rec)
        continue
    if rects:
        s = escala(src)
        usa = rects[:1] if (SOLO_PRIMERO.search(src) and not de_fs1) else rects
        P = round(per_union(usa, s), 2)
        nota = (" (outer room rectangle only: the deducted piece's edge takes a trim, not wall angle)" if len(usa) < len(rects) or (SOLO_PRIMERO.search(src) and not de_fs1) else
                " (the WS-1 panel edge inside the corridor takes a trim, not wall angle)" if de_fs1 and SOLO_PRIMERO.search(src) else "")
        x['qty'] = P
        x['op'] = (f"perimeter of the measured room polygon = union of {len(usa)} rectangle(s) "
                   f"{'; '.join(f'({r[1]}-{r[0]}) x ({r[3]}-{r[2]})' for r in usa)} pt / {s:g} pt/ft = {P} LF{nota}")
        rec.update(despues=P, metodo="rect", op=x['op'])
    else:
        fl = ref.split('-')[1]
        m = re.findall(r"\b([1-4]\d\d)\b", src.split('|')[0])
        sf = float(b['qty'] / max(1, int(str(b.get('op', '')).split('x')[1].split('layer')[0]) if 'layer' in str(b.get('op', '')) else 1)) if b else None
        sf = float(re.search(r"area (\d+\.?\d*) SF", src).group(1)) if re.search(r"area (\d+\.?\d*) SF", src) else sf
        mt = re.search(r"area \d+\.?\d* SF \(\s*(\d+\.?\d*) SF", src)      # corridor: polygon / printed SF before the WS-1 deduction
        sf = float(mt.group(1)) if mt else sf
        res = None
        for room in m[:2]:
            res, e = flood(fl, room, sf)
            if res:
                break
        if res:
            x['qty'] = res['perim_ft']; x['op'] = f"perimeter of the room polygon: {res['op']} = {res['perim_ft']} LF"
            rec.update(despues=res['perim_ft'], metodo="flood", op=x['op'], flood=res)
        else:
            rec.update(despues=None, metodo="FALLA", sala=m)
            FALLA.append(ref)
    LOG.append(rec)
json.dump({"filas": LOG, "falla": FALLA, "flood_poly": {f'{k[0]} {k[1]}': v for k, v in FLOOD_POLY.items()}}, open(f'{W}/etapas/4_canon/out/perimetros_angle.json', 'w'), indent=1)
if '--dry' not in sys.argv:
    json.dump(c, open(CP, 'w'), indent=1)
for r in LOG:
    print(r['ref'], r['antes'], '->', r['despues'], r['metodo'], (r.get('flood') or {}).get('err', ''))
print('FALLA', FALLA)
