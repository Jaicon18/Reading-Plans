#!/usr/bin/env python3
"""CR City Hotel rev2 - cement board por shower (auditoría U-138 #2, hallazgos F1 / F2 / F6).
Regla impresa: A0.06 GN 13 'USE CEMENTITIOUS BACKER UNITS ... AT PARTITIONS TO RECEIVE CERAMIC TILE'; 6/A7.02 (Type 1) y 8 / 9/A7.03
(Type 2): TILE-1 SOLO dentro del shower, fuera TF-1 + 4" base. RFI-11 (cerrado): cement board a 9'-0" (bath ceiling 8'-6" + 6");
rated: las capas Type X W.R. del type quedan a altura completa + 1 layer de cement board; NON-rated: cement board EN LUGAR del board
(queda la franja de W.R. sobre el cement board).
Método (vectores, 1/8" = 9 pt/ft):
 1. caja de cada shower de guest bath: detector de las 2 diagonales del shower pan (auditoría tools/showers.py) + los 4 de otro
    formato medidos a mano en vectores (211 / 311 cuadrado, 308 = 208, 402);
 2. lado SÓLIDO = una línea de muro >= 1.0 pt de grosor colineal (<= 4 pt) que cubre >= 70 % del lado; el lado de vidrio / curb no la tiene;
 3. todo cement board existente de L2-L4 se borra; por cada lado sólido se crea 1 entrada de cement board en el wall colineal del canon
    (path a <= 8 pt del lado, solape >= 50 %), largo = el lado del shower [DERIVED], altura min(9'-0", altura del wall);
 4. F6: en un type NON-rated ('-0') la cara W.R. / Type X del cuarto del shower se parte: fuera del shower altura completa; sobre el
    shower altura - 9'-0" (franja).
Salida: canon en su lugar + etapas/4_canon/out/banos_cbu.json (+ log de lo no asignado)."""
import json, re, sys, collections
import pymupdf as fitz
sys.path.insert(0, '/root/cr/work/scripts/lib')
from showers_det import showers
W = '/root/cr/work'
CP = f'{W}/etapas/4_canon/takeoff_canon.json'
c = json.load(open(CP))
D = fitz.open(f'{W}/plans/bidset_SIN_MARKUPS.pdf')
SC = 9.0
PISO = {"L2": ("A2.02", 17), "L3": ("A2.03", 18), "L4": ("A2.04", 19)}
# cuarto de cada caja detectada (orden por (y0, x) de la caja), asignado a ojo sobre la imagen numerada (etapas/4_canon/img/cbu/)
CUARTOS = {"L2": ["201", "213", "202", "214", "203", "212", "210", "204", "207", "208", "205", "206", "209"],
           "L3": ["301", "313", "302", "314", "303", "312", "310", "304", "307", "305", "306", "309"],
           "L4": ["404", "405", "403", "401"]}
MANUAL = {"L2": [("211", 585.4, 612.4, 1109.0, 1136.6)],
          "L3": [("311", 585.4, 612.4, 1109.6, 1136.6), ("308", 1358.5, 1418.5, 1175.0, 1201.4)],
          "L4": [("402", 967.1, 994.6, 924.2, 951.2)]}
_CBU_H = "Bath ceiling GYP-1 8'-6\" (A7.xx unit RCP) + 6\" above line of ceiling (A0.06 furred wood head detail) = 9'-0\" (cement board to the tile ceiling + 6\", estimator precedent #15 (B&N), RFI-11 closed)"


SNAP_LOG = []


def cajas(fl):
    sh, pg = PISO[fl]
    det = [s for s in showers(pg) if 2.5 * 9 <= s[3] - s[2] <= 4.2 * 9 and abs(s[1] - (s[4] if s[0] == 'V' else s[5])) >= 4.5 * 9]
    ded = {}
    for s in det:
        ded.setdefault((s[0], round(s[1] / 2), round(s[2] / 3)), s)
    out = []
    for s in sorted(ded.values(), key=lambda s: (s[2], s[1])):
        if s[0] == 'V':
            x0, x1 = sorted([s[1], s[4]]); y0, y1 = s[2], s[3]
        else:
            y0, y1 = sorted([s[1], s[5]]); x0, x1 = s[2], s[3]
        out.append([x0, x1, y0, y1])
    assert len(out) == len(CUARTOS[fl]), (fl, len(out))
    cajas_ = [(CUARTOS[fl][i],) + tuple(b) for i, b in enumerate(out)] + MANUAL[fl]
    # E2 (auditoría COORDINACIÓN 7-nov, rev6): cada lado a la CARA DEL WALL, no al extremo de las diagonales del pan
    from snap_caja import snap
    res = []
    for r, x0, x1, y0, y1 in cajas_:
        s = snap(D[pg], x0, x1, y0, y1)
        if any(abs(a - b) > 0.3 for a, b in zip(s, (x0, x1, y0, y1))):
            SNAP_LOG.append({"piso": fl, "cuarto": r, "antes": [round(v, 1) for v in (x0, x1, y0, y1)], "cara_del_wall": [round(v, 1) for v in s]})
        res.append((r,) + tuple(s))
    return res


_lin = {}


def _fmt(h):
    from fractions import Fraction
    ft = int(h + 1e-9); r = round((h - ft) * 12 * 8) / 8
    if r >= 12:
        ft, r = ft + 1, r - 12
    ent = int(r); f = Fraction(r - ent).limit_denominator(8)
    return f"{ft}'-{ent}" + (f" {f.numerator}/{f.denominator}" if f else "") + '"'


def lineas(pg):
    if pg not in _lin:
        H, V = [], []
        for d in D[pg].get_drawings():
            if (d.get('width') or 0) < 1.0:
                continue
            for it in d['items']:
                if it[0] == 'l':
                    a, b = it[1], it[2]
                    if abs(a.y - b.y) < 0.3:
                        H.append((a.y, min(a.x, b.x), max(a.x, b.x)))
                    elif abs(a.x - b.x) < 0.3:
                        V.append((a.x, min(a.y, b.y), max(a.y, b.y)))
        _lin[pg] = (H, V)
    return _lin[pg]


def solido(pg, ori, coord, lo, hi):
    H, V = lineas(pg)
    ls = H if ori == 'H' else V
    iv = sorted((max(l, lo), min(h, hi)) for c0, l, h in ls if abs(c0 - coord) <= 5.0 and min(h, hi) > max(l, lo))
    cov, p = 0.0, lo
    for a, b in iv:
        if b > p:
            cov += b - max(a, p); p = b
    return cov / (hi - lo) >= 0.70


def lados(fl, x0, x1, y0, y1):
    pg = PISO[fl][1]
    out = []
    for nom, ori, coord, lo, hi in (("N", 'H', y0, x0, x1), ("S", 'H', y1, x0, x1), ("W", 'V', x0, y0, y1), ("E", 'V', x1, y0, y1)):
        if solido(pg, ori, coord, lo, hi):
            out.append((nom, ori, coord, lo, hi))
    return out


def eje(e):
    (a, b), (cc, dd) = e['path'][0], e['path'][-1]
    if abs(b - dd) < 1.0:
        return 'H', (b + dd) / 2, min(a, cc), max(a, cc)
    if abs(a - cc) < 1.0:
        return 'V', (a + cc) / 2, min(b, dd), max(b, dd)
    return None, None, None, None


def es_cbu(e):
    return 'cement' in str(e.get('board') or '')


# 1. borrar el cement board existente de L2-L4
quitados = [e for e in c['existing_walls'] if e['floor'] in PISO and es_cbu(e)]
sf_old = collections.Counter()
for e in quitados:
    sf_old[e['floor']] += e['length_ft'] * min(e['height_ft'], 9.0) * int(e.get('layers') or 1) * int(e.get('faces') or 1)
    c['existing_walls'].remove(e)
res = {"quitado_sf": {k: round(v, 1) for k, v in sf_old.items()}, "quitados": [e['id'] for e in quitados], "showers": [], "sin_wall": [], "f6": []}

# 2. reconstruir por shower
for fl in PISO:
    sh = PISO[fl][0]
    for room, x0, x1, y0, y1 in cajas(fl):
        lado = lados(fl, x0, x1, y0, y1)
        rec = {"floor": fl, "room": room, "box": [round(x0, 1), round(x1, 1), round(y0, 1), round(y1, 1)], "solid": [l[0] for l in lado], "cbu": []}
        for nom, ori, coord, lo, hi in lado:
            cand = []
            for e in c['existing_walls']:
                if e['sheet'] != sh or e['floor'] != fl or es_cbu(e) or re.search(r"(?i)exterior|sheathing", str(e.get('board'))):
                    continue
                o, cc, a, b = eje(e)
                if o != ori or abs(cc - coord) > 10.0:
                    continue
                sol = min(b, hi) - max(a, lo)
                if sol >= 0.5 * (hi - lo):
                    cand.append((sol, e))
            if not cand:
                res['sin_wall'].append(f"{fl} {room} {nom} {ori}={coord:.1f} {lo:.1f}-{hi:.1f}")
                continue
            cand.sort(key=lambda t: -t[0])
            base = re.sub(r" [A-Z]$", "", cand[0][1]['id'])
            hermanos = [e for s_, e in cand if re.sub(r" [A-Z]$", "", e['id']) == base]
            def _lab(e):
                return str(e.get('location', '')).split('faces:')[-1]
            cara = (next((e for e in hermanos if re.search(rf"\b{room}\b", _lab(e)) and re.search(r"(?i)shower", _lab(e))), None)
                    or next((e for e in hermanos if re.search(rf"\b{room}\b", _lab(e)) and re.search(r"(?i)bath|toilet|wc", _lab(e))), None)
                    or next((e for e in hermanos if re.search(rf"\b{room}\b", _lab(e)) and not re.search(r"(?i)closet|room|bedroom|entry|corridor", _lab(e))), None))
            w0 = cara or hermanos[0]
            usadas = {x['id'][-1] for x in c['existing_walls'] if re.sub(r" [A-Z]$", "", x['id']) == base and re.search(r" [A-Z]$", x['id'])}
            libre = next(ch for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if ch not in usadas)
            o, cc, a, b = eje(w0)
            lo2, hi2 = max(lo, a), min(hi, b)
            nw = json.loads(json.dumps(w0))
            if not re.search(r" [A-Z]$", w0['id']):
                for x in c['existing_walls']:          # el wall sin sufijo pasa a ser 'A'
                    if x is w0:
                        x['id'] = base + ' A'
                libre = next(ch for ch in "BCDEFGHIJKLMNOPQRSTUVWXYZ" if ch not in usadas)
            nw['id'] = base + ' ' + libre
            nw['path'] = [[lo2, cc], [hi2, cc]] if ori == 'H' else [[cc, lo2], [cc, hi2]]
            nw['length_ft'] = round((hi2 - lo2) / SC, 2)
            hh = min(9.0, float(w0['height_ft']))
            if cara:
                _pp = [x.strip() for x in _lab(cara).split(';') if x.strip()]
                lbl = next((x for x in _pp if re.search(r"(?i)shower", x)), None) or next((x for x in _pp if re.search(rf"\b{room}\b", x)), _pp[0] if _pp else f"{room} shower")
            else:
                lbl = f"{room} shower"
            nw.update({"board": "5/8 cement board", "layers": 1, "faces": 1, "height_ft": hh, "height_status": "DERIVADO",
                       "height_source": _CBU_H if hh == 9.0 else f"{w0.get('height_source')} (cement board to the top of this wall: the RFI-11 tile line is above the wall top)",
                       "location": re.sub(r"faces:.*$", f"faces: {lbl}", str(w0.get('location', ''))), "img": w0.get("img"),
                       "length_status": "DERIVADO"})
            nw['source'] = (f"1/{sh} [DERIVED] length: {room} shower {nom} side, shower box from the vector shower pan to the wall face (sides at the wall line, not at the pan diagonals) "
                            f"({hi2:.1f}-{lo2:.1f})/9 = {nw['length_ft']} ft; tile at the shower only (6/A7.02, 8/A7.03, 9/A7.03), A0.06 GN 13 | height: {nw['height_source']}")
            nw.pop('faces_none_reason', None)
            c['existing_walls'].insert(c['existing_walls'].index(w0) + 1, nw)
            rec['cbu'].append({"id": nw['id'], "side": nom, "lf": nw['length_ft'], "h": hh, "on": w0['id'], "face_match": bool(cara)})
            # 4. F6: type NON-rated -> la cara del shower lleva cement board EN LUGAR del board (franja arriba)
            if cara and str(cara.get('type_id', '')).endswith('-0') and float(cara['height_ft']) > 0:
                H0 = float(cara['height_ft'])
                oc, cc2, a2, b2 = eje(cara)
                segs = [(a2, lo2, H0), (lo2, hi2, round(H0 - hh, 4)), (hi2, b2, H0)]
                segs = [(p, q, h) for p, q, h in segs if q - p >= 1.0 and h > 0.01]
                i0 = c['existing_walls'].index(cara)
                nf = int(cara.get('faces') or 1)
                plantilla = json.loads(json.dumps(cara)); plantilla['faces'] = 1
                if nf > 1:          # la entrada representa 2 caras: solo la cara del shower se parte, la otra queda entera
                    partes = [x.strip() for x in str(cara['location']).split('faces:')[-1].split(';') if x.strip()]
                    ps = next((x for x in partes if re.search(r"(?i)shower", x)), None) or next((x for x in partes if re.search(rf"\b{room}\b", x)), partes[0] if partes else room)
                    otras = [x for x in partes if x != ps] or partes
                    cara['faces'] = nf - 1; i0 += 1
                    cara['location'] = re.sub(r"faces:.*$", "faces: " + "; ".join(otras), str(cara['location']))
                    plantilla['location'] = re.sub(r"faces:.*$", "faces: " + ps, str(plantilla['location']))
                else:
                    c['existing_walls'].remove(cara)
                usadas = {x['id'][-1] for x in c['existing_walls'] if re.sub(r" [A-Z]$", "", x['id']) == base} | {cara['id'][-1]}
                letras = [ch for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if ch not in usadas]
                primero = nf == 1
                for p, q, h in segs:
                    s2 = json.loads(json.dumps(plantilla))
                    s2['id'] = cara['id'] if primero else base + ' ' + letras.pop(0)
                    primero = False
                    s2['path'] = [[p, cc2], [q, cc2]] if oc == 'H' else [[cc2, p], [cc2, q]]
                    s2['length_ft'] = round((q - p) / SC, 2)
                    s2['source'] = (f"1/{sh} [DERIVED] length: ({q:.1f}-{p:.1f})/9 = {s2['length_ft']} ft"
                                    + (f" over the {room} shower: non-rated type, cement board in place of board (RFI-11), board strip above it {H0} - 9.0 = {h} ft"
                                       if abs(h - H0) > 0.01 else " (face outside the shower)") + " | height:" + str(cara['source']).split('| height:', 1)[-1])
                    if abs(h - H0) > 0.01:
                        s2['height_ft'] = h
                        s2['height_status'] = 'DERIVADO'
                        s2['height_source'] = f"{_fmt(H0)} - 9'-0\" = {_fmt(h)} (board strip above the cement board: wall height minus the RFI-11 cement board height; non-rated type, cement board in place of board)"
                    c['existing_walls'].insert(i0, s2); i0 += 1
                res['f6'].append({"wall": cara['id'], "room": room, "lf": round((hi2 - lo2) / SC, 2), "h_strip": round(H0 - hh, 4)})
        res['showers'].append(rec)
sf_new = collections.Counter()
for e in c['existing_walls']:
    if e['floor'] in PISO and es_cbu(e):
        sf_new[e['floor']] += e['length_ft'] * e['height_ft']
res['nuevo_sf'] = {k: round(v, 1) for k, v in sf_new.items()}
json.dump(c, open(CP, 'w'), indent=1)
res = {"filas": res, "cara_del_wall": SNAP_LOG} if isinstance(res, list) else dict(res, cara_del_wall=SNAP_LOG)
json.dump(res, open(f'{W}/etapas/4_canon/out/banos_cbu.json', 'w'), indent=1)
print('CBU antes', res['quitado_sf'], '| después', res['nuevo_sf'], '| showers', len(res['showers']), '| lados sin wall', len(res['sin_wall']), '| F6', len(res['f6']))
for s in res['sin_wall']:
    print('  sin wall:', s)
for s in res['showers']:
    print('  ', s['floor'], s['room'], s['solid'], [(x['side'], x['lf'], x['on'], 'cara' if x['face_match'] else 'SIN CARA') for x in s['cbu']])
