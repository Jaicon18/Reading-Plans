#!/usr/bin/env python3
"""CR City Hotel rev2 - shafts 2-HR en L3 y L4 (auditoría U-138 #2, F3 / F13; cierra RFI-09).
7/A9.03 (shaft sur) y 8/A9.03 (shaft norte): '2-HOUR SHAFTWALL ASSEMBLY (W419, U497) MAX. HEIGHT - 54'-0"', 10/A9.03 HEAD OF SHAFT,
11/A9.03 BASE OF NORTH SHAFT = un shaft continuo de L2 a la cubierta. L2 lo carga como CH.6-2 (CH-L2-01..07); en L3 la misma caja
(mismas coordenadas en 1/A2.03) estaba como 'small shaft box' W.4-0 de 1 layer (NULL-L3-11..14, RFI-09) y el norte solo como FW.4
(NULL-L3-15); en L4 el norte solo como FW.4-L4-04 (1 cara W.R.). Se replican los CH de L2 tramo por tramo (mismo path, verificado
contra las líneas del shaft en la hoja), altura del piso: L3 = LEVEL 3 6222.75' a LEVEL 4 6233.75' = 11'-0" (impreso en 4/A5.05);
L4 = 8'-11 1/4" (1/A5.06, igual que el shaft sur de L4 CH.6-L4-01..04). C-H stud 6" @ 24" o.c. + J-runner arriba / abajo como build_canon."""
import json, math, re
import pymupdf as fitz
W = '/root/cr/work'
CP = f'{W}/etapas/4_canon/takeoff_canon.json'
c = json.load(open(CP))
D = fitz.open(f'{W}/plans/bidset_SIN_MARKUPS.pdf')
HS = list(json.load(open(f'{W}/set_texto.json'))['hojas'])
if any(e['id'].startswith('CH-L3-') for e in c['existing_walls']):
    print('ya aplicado'); raise SystemExit
L2 = [e for e in c['existing_walls'] if re.match(r"CH-L2-0[1-7] [AB]$", e['id'])]
PISOS = {"L3": ("A2.03", ["01", "02", "03", "04", "05", "06", "07"], 11.0,
                "6233.75' - 6222.75' = 11'-0\" (LEVEL 3 / LEVEL 4 datums printed on 4/A5.05); shaft wall continuous floor to floor (7/A9.03, 8/A9.03, 10/A9.03)",
                {"05": "314 bath (room side)", "06": "315 Cleaning (room side)", "07": "314 / corridor 316 (room side)"}),
         "L4": ("A2.04", ["05", "06", "07"], 8.9375,
                "1/A5.06 printed 8'-11 1/4\" LEVEL 4 to underside of roof framing (same as the L4 south shaft CH.6-L4-01..04); shaft per 8/A9.03, 10/A9.03",
                {"05": "405 bath (room side)", "06": "406 Cleaning (room side)", "07": "405 / corridor 412 (room side)"})}
QUITA = {"L3": ["NULL-L3-11", "NULL-L3-12", "NULL-L3-13", "NULL-L3-14", "NULL-L3-15"], "L4": ["FW.4-L4-04"]}
_lin = {}


def hay_linea(pg, path):
    if pg not in _lin:
        out = []
        for d in D[pg].get_drawings():
            if (d.get('width') or 0) >= 0.6:
                out += [(it[1], it[2]) for it in d['items'] if it[0] == 'l']
        _lin[pg] = out
    (x0, y0), (x1, y1) = path
    h = abs(y1 - y0) < 1
    tot = 0.0
    for a, b in _lin[pg]:
        if h and abs(a.y - b.y) < 0.3 and abs(a.y - y0) <= 4:
            tot += max(0, min(max(a.x, b.x), max(x0, x1)) - max(min(a.x, b.x), min(x0, x1)))
        if not h and abs(a.x - b.x) < 0.3 and abs(a.x - x0) <= 4:
            tot += max(0, min(max(a.y, b.y), max(y0, y1)) - max(min(a.y, b.y), min(y0, y1)))
    return tot / max(1e-6, math.dist((x0, y0), (x1, y1)))


def _op(p):
    (x0, y0), (x1, y1) = p
    a, b = (sorted([x0, x1]) if abs(y1 - y0) < 1 else sorted([y0, y1]))
    return f"({b}-{a})/9"


res = {"agregados": [], "quitados": [], "misc": []}
for fl, (sh, nums, H, hsrc, cuartos) in PISOS.items():
    pg = HS.index(sh)
    for e in [x for x in c['existing_walls'] if x['id'] in QUITA[fl] or re.sub(r" [A-Z]$", "", x['id']) in QUITA[fl]]:
        c['existing_walls'].remove(e)
        c['excluded_walls'].append({"id": e['id'], "reader": "AB", "floor": fl, "sheet": e['sheet'], "img": e.get('img'), "tag_ids": e.get('tag_ids') or [],
                                    "reason": f"replaced by the 2-HR shaft wall CH.6-2 (7/A9.03 / 8/A9.03 '2-HOUR SHAFTWALL ASSEMBLY (W419, U497)', same shaft as CH-L2): this entry was the shaft box read as a 1-layer partition (auditoria U-138 #2 F3; RFI-09 closed)"})
        res['quitados'].append(e['id'])
    for n in nums:
        for lado in ("A", "B"):
            src = next(x for x in L2 if x['id'] == f"CH-L2-{n} {lado}")
            cov = hay_linea(pg, src['path'])
            nw = json.loads(json.dumps(src))
            nw.update({"id": f"CH-L{fl[1]}-{n} {lado}", "floor": fl, "sheet": sh, "page": pg + 1, "height_ft": H, "height_status": "DERIVADO" if fl == "L3" else "CONFIRMADO",
                       "height_source": hsrc, "tag_ids": []})
            if lado == "B" and n in cuartos:
                nw['location'] = re.sub(r"faces:.*$", f"faces: {cuartos[n]}", str(nw['location']))
            nw['location'] = re.sub(r"^L2", fl, str(nw['location']))
            nw['source'] = (f"7/A9.03, 8/A9.03; 1/{sh} [DERIVED] length: same shaft and same path as CH-L2-{n} (the shaft box is drawn at the same coordinates on 1/{sh}, "
                            f"wall lines cover {cov:.0%} of the path): {_op(nw['path'])} = {nw['length_ft']} ft; 2-HOUR SHAFTWALL ASSEMBLY (W419, U497) MAX. HEIGHT 54'-0\" (7/A9.03), A0.06 CH (UL U415) | height: {hsrc}")
            nw['decision'] = "C-H shaft wall (A0.06 CH; 7/A9.03 W419 / U497; UL U415): board / liner here, C-H studs + J-runner in misc_items (auditoria U-138 #2 F3)"
            c['existing_walls'].append(nw)
            res['agregados'].append({"id": nw['id'], "lf": nw['length_ft'], "h": H, "board": nw['board'], "cobertura_lineas": round(cov, 2)})
        L = next(x for x in L2 if x['id'] == f"CH-L2-{n} A")['length_ft']
        n_st = math.ceil(L / 2.0 - 1e-6) + 1
        wid = f"CH-L{fl[1]}-{n}"
        c['misc_items'].append({"ref": f"CH-STUD {wid}", "familia": 'C-H stud 6" (printed)', "qty": round(n_st * H, 2), "floor": fl,
                                "op": f"ROUNDUP({L}/2.0)+1 = {n_st} studs x {H} ft = {round(n_st * H, 2)}",
                                "source": f"1/{sh} {wid}; A0.06 CH '6\" 20GA METAL C-H STUD'; 7/A9.03 2-HOUR SHAFTWALL ASSEMBLY (W419, U497); spacing 24 in. o.c. per UL U415"})
        c['misc_items'].append({"ref": f"J-RUNNER {wid}", "familia": 'J-runner 6" (printed)', "qty": round(2 * L, 2), "floor": fl,
                                "op": f"2 x {L} (top + bottom 'J' RUNNER CHANNEL) = {round(2 * L, 2)}", "source": f"1/{sh} {wid}; A0.06 CH '\"J\" RUNNER CHANNEL'"})
        res['misc'].append((wid, round(n_st * H, 2), round(2 * L, 2)))
# F13: la cita del shaft incluye W419 / U497 (7/A9.03) además de UL U415 (A0.06 CH)
for e in c['existing_walls']:
    if str(e.get('type_id', '')).startswith('CH') and 'W419' not in str(e.get('source')):
        e['source'] = str(e['source']) + " | 7/A9.03 '2-HOUR SHAFTWALL ASSEMBLY (W419, U497)'"
for r in c.get('rfis') or []:
    if r['id'] == 'RFI-09':
        r['status'] = 'closed'
        r['resolved'] = {"answer": "Printed (option A, U-140): the small box south of lobby 317 is the SOUTH 2-HR SHAFT of 7/A9.03 '2-HOUR SHAFTWALL ASSEMBLY (W419, U497) MAX. HEIGHT 54'-0\"' (continuous from L2, 10/A9.03 HEAD OF SHAFT): loaded as CH.6-2 on L3 like CH-L2-01..04 (shaftliner + 2 layers 5/8\" Type X + C-H studs + J-runner); the north shaft (8/A9.03) on L3 and L4 too (auditoria U-138 #2 F3)",
                         "source": "7/A9.03, 8/A9.03, 10/A9.03, 1/A2.02, 1/A2.03, 1/A2.04"}
        r['delta_applied'] = "see Material Summary: shaftliner / Type X / C-H stud / J-runner of CH-L3-01..07 and CH-L4-05..07"
json.dump(c, open(CP, 'w'), indent=1)
json.dump(res, open(f'{W}/etapas/4_canon/out/shafts_l3l4.json', 'w'), indent=1)
print('agregados', len(res['agregados']), 'quitados', res['quitados'], 'misc', res['misc'])
print('cobertura mínima de líneas', min(x['cobertura_lineas'] for x in res['agregados']))
