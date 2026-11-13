"""CR City Hotel rev20 (12-nov, COORDINACIÓN tras la auditoría U-181): lo DIBUJADO se CARGA (U-052 / U-083), nada queda "anotado" sin número (U-114).
(1) Cara de la caja DERECHA del corredor en el plenum (7/A7.23): gypsum dibujado desde el cielo GYP-1 8'-11" hasta el rated assembly.
    H-A 0.917 (11" sobre el board del campo) / H-B 0.97 (11 5/8" a la línea de 8'-11") -> cota impresa 9 1/2" + 2 1/8" = 11 5/8" = 0.9688 ft
    (la mayor, U-146). Un solo lado por corredor (la caja izquierda = diffuser box no tiene cara arriba del campo): LF = LF de la banda / 2.
(2) Campo GYP-1 8'-11" de los corredores (A7.23 / A7.24): board + USG drywall suspension (main tee 4 ft, cross tee 16"), angle molding,
    hanger wire (drop 9 1/2" + 2 1/8" = 0.969 ft), igual que CLG-L2-39 / CLG-L1-12 -- desde scratchpad corr_field/FIELD.json si existe.
(3) Borde exterior de los coffers SOF-L1-01 (fondo no compartido) -- desde scratchpad coffer_edge/COFFER_EDGE.json si existe.
Idempotente: borra sus propios renglones antes de agregarlos."""
import json
import math
import os

W = '/root/cr/work'
CP = f'{W}/etapas/4_canon/takeoff_canon.json'
SP = '/tmp/claude-0/-home-user/18bfbfac-ecd6-55d5-8e44-1a0e0dafeecf/scratchpad'
C = json.load(open(CP))
CORR = ('SOF-L2-01', 'SOF-L2-02', 'SOF-L3-316', 'SOF-L3-318', 'SOF-L4-02')
H_PLEN = round((9.5 + 2.125) / 12, 4)          # 0.9688
log = []
PROPIOS = lambda r: (r.split(' ')[0].endswith('P') and r.split(' ')[0][:-1] in CORR) or r.startswith(('CLG-L2-216F', 'CLG-L2-218F', 'CLG-L3-316F', 'CLG-L3-318F', 'CLG-L4-412F', 'SOF-L1-01E ')) or r.split(' ')[0] in ('SOF-L2-217V', 'SOF-L2-217B', 'SOF-L3-317V', 'SOF-L3-317B', 'BW-L1-NORTH', 'CLG-L1-129P', 'CLG-L1-219U', 'CLG-L2-217F', 'CLG-L3-317F', 'CLG-L4-106R', 'CLG-L4-108R', 'CLG-L4-110R', 'CLG-L4-112R', 'CLG-L4-114R')
C['misc_items'] = [m for m in C['misc_items'] if not PROPIOS(str(m.get('ref')))]
por = {m['ref']: m for m in C['misc_items']}

# (1) cara en el plenum
for b in CORR:
    p = por[f'{b} board']
    lf_band = float(str(p['op']).split(' LF')[0])
    lf = round(lf_band / 2, 2)
    q = round(lf * H_PLEN, 2)
    C['misc_items'].append({
        "ref": f"{b}P board", "familia": p.get('familia'), "qty": q, "detail": "7/A7.23",
        "op": f"{lf} LF x {H_PLEN} ft = {q}",
        "source": (f"{b} corridor, right-hand soffit box: corridor face drawn as gypsum ABOVE the GYP-1 8'-11\" field up to the underside of the "
                   f"rated assembly (7/A7.23, printed '9 1/2\"' + '2 1/8\"' = 11 5/8\" = {H_PLEN} ft [DERIVED]); one side only (the left box = DIFFUSER "
                   f"BOX side has no face above the field); LF = band LF {lf_band} (both sides) / 2 = {lf} [DERIVED]. U-176 H-A 0.917 / H-B 0.97 -> printed "
                   "11 5/8\" (U-146 larger). Drawn = loaded (U-052 / U-083); Review Item = deduction if the estimator leaves it out")})
    log.append(f"{b}P board: + {q} SF ({lf} LF x {H_PLEN})")
for s in C.get('framed_soffits') or []:
    if s.get('id') in CORR:
        s['plenum_face'] = {"side": "right box only", "height_ft": H_PLEN, "qty_in": f"misc_items '{s['id']}P board'"}

# (2) campo GYP-1 8'-11"
F = f'{SP}/corr_field/FIELD_FINAL.json'
if os.path.isfile(F):
    for f in json.load(open(F)):
        rid, sf, per, nh, src = f['id'], round(f['sf'], 2), round(f['perimeter_lf'], 2), f['nhoja'], f['source']
        drop = round(9.885 - (8 + 11 / 12), 3)
        nh_ = math.ceil(sf / 16)
        det = f"{nh} (RCP ceiling legend 'GYP-1: GYPSUM BOARD ON METAL SUSPENSION SYSTEM, OR WOOD FRAMING'; 7/A7.23 hanger wire drawn)"
        filas = [("board", "5/8\" gyp board Type X", sf, f"{sf} SF x 1 layer(s) = {sf}", src),
                 ("main tee", "USG drywall main tee (DGLW26)", round(sf / 4.0, 2), f"{sf} SF / 4.0 ft o.c. = {round(sf / 4.0, 2)}",
                  "USG drywall suspension, main tees 48 in. o.c. (manufacturer, not printed); GYP-1 'GYPSUM BOARD ON METAL SUSPENSION SYSTEM': metal suspension (09 22 16 'Grid Suspension System for Ceilings')"),
                 ("cross tee", "USG drywall cross tee (DGLW424)", round(sf / 1.333, 2), f"{sf} SF / 1.333 ft o.c. = {round(sf / 1.333, 2)}",
                  "cross tees 16 in. o.c. for 5/8 in. board (manufacturer, not printed)"),
                 ("angle molding", "USG angle molding (DGWM24)", per, f"perimeter of the measured field polygon on {nh} = {per} LF", "wall angle at the soffit box faces"),
                 ("hanger wire", "hanger wire", round(nh_ * drop, 2), f"ROUNDUP({sf}/16) = {nh_} hangers (4 ft x 4 ft) x drop {drop} ft (9.885 rated assembly - 8.917 ceiling) = {round(nh_ * drop, 2)}",
                  "7/A7.23: hanger wire drawn from the rated assembly to the GYP-1 field; drop = printed '9 1/2\"' + '2 1/8\"' (9'-10 5/8\" - 8'-11\")")]
        for k, fam, q, op, s_ in filas:
            C['misc_items'].append({"ref": f"{rid} {k}", "familia": fam, "qty": q, "op": op, "source": s_, "detail": det})
        log.append(f"{rid}: board {sf} SF, angle {per} LF")

# (3) borde exterior de los coffers
E = f'{SP}/coffer_edge/COFFER_EDGE_FINAL.json'
if os.path.isfile(E):
    e = json.load(open(E))
    q = round(e['outer_lf'] * e['extra_width_ft'], 2)
    C['misc_items'].append({"ref": "SOF-L1-01E board", "familia": por['SOF-L1-01 board'].get('familia'), "qty": q, "detail": "5/A7.31",
                            "op": f"{e['outer_lf']} LF x {e['extra_width_ft']} ft = {q}", "source": e['source']})
    log.append(f"SOF-L1-01E board: + {q} SF")

# (4) L4: la RS-1 (A0.08, roof / ceiling rated, board on channel under the wood roof framing) se cargó "contorno - bath" en 401-405; en L2 / L3
#     la FS-1 SÍ pasa sobre el baño (doble cielo: membrana rated + GYP-1 8'-6" colgado). Misma regla en L4: la membrana RS-1 sobre cada baño.
for b_ in ('CLG-L4-106', 'CLG-L4-108', 'CLG-L4-110', 'CLG-L4-112', 'CLG-L4-114'):
    x_ = por[f'{b_} board']
    sf = x_['qty']; rc = round(sf * 12 / 16, 2)
    base = str(x_['source']).split(' | ')[0]
    nota = (" | double ceiling: RS-1 rated roof / ceiling membrane (A0.08 RS-1, 1 layer on channel 16 in. o.c., UL L546 / RFI-14), the same board "
            "as the L4 RS-1 ceilings[] (5/8\" Type X, A0.08 RS-1 board type per RFI-CR-RS1), continuous ABOVE the dropped bath GYP-1 8'-6\" W.R. "
            "(the exposed shower-room ceiling, A0.06 GN 12) and not exposed; as FS-1 on L2 / L3, whose contours include the bath")
    C['misc_items'].append({"ref": f"{b_}R board", "familia": "5/8\" gyp board Type X", "qty": sf, "detail": "A0.08 RS-1 / 1/A3.04",
                            "op": f"{sf} SF x 1 layer(s) = {sf}", "source": base + nota})
    C['misc_items'].append({"ref": f"{b_}R RC", "familia": "resilient channel (printed)", "qty": rc, "detail": "A0.08 RS-1 / 1/A3.04",
                            "op": f"{sf} SF x 12 / 16 in. o.c. = {rc} LF", "source": base + nota})
    log.append(f"{b_}R: RS-1 over the L4 bath + {sf} SF Type X, {rc} LF RC")

# (5) COBERTURA RCP U-189 (3) (auditor independiente rev20, 25 hojas RCP): cielos apilados sin renglón
#  GAP-1: 2/A5.04 'GYP BD APPLIED TO B.O. WOOD JOIST' = cara inferior del piso del MECH & WATER HEATER MEZZANINE 219 (cielo de L1 debajo,
#         sobre Kitchen 100 / Toilets 110-111 / Janitor 109 / Bar norte); board directo a la madera (sin suspensión); medido en 1/A3.02.
from shapely.geometry import box as _box
from shapely.ops import unary_union as _uu
_mz = (1142.0, 1366.0, 424.0, 593.0)                       # 1/A3.02 caras interiores del mezzanine (pt, 9 pt/ft)
_sf = round((_mz[1] - _mz[0]) * (_mz[3] - _mz[2]) / 81, 2)
C['misc_items'].append({"ref": "CLG-L1-219U board", "familia": "5/8\" gyp board Type C", "qty": _sf, "detail": "2/A5.04",
                        "op": f"{_sf} SF x 1 layer(s) = {_sf}",
                        "source": f"L1 ceiling = underside of the MECH & WATER HEATER MEZZANINE 219 floor: 2/A5.04 printed 'GYP BD APPLIED TO B.O. WOOD JOIST' "
                                  f"[CONFIRMED]; area = inside faces of the mezzanine on 1/A3.02 ({_mz[1]}-{_mz[0]})*({_mz[3]}-{_mz[2]})/81 = {_sf} SF [DERIVED] "
                                  "(printed '462 SF' on 1/A2.02, net room area); board type (U-172 sweep): A0.03 code plan draws the mezzanine 219 inside the '1 HOUR RATED "
                                  "HORIZONTAL ASSEMBLY' and A0.08 'LEVEL 2, 3, 4 FS-1 THROUGHOUT' = FS-1 '5/8\" TYPE C GYP BD CEILING' (UL L546) -> 5/8\" Type C, 1 layer; "
                                  "applied directly to the wood joists (no metal: U-190 'direct to wood'); rev20 coverage audit GAP-1"})
log.append(f"CLG-L1-219U: + {_sf} SF Type C (2/A5.04 GYP BD APPLIED TO B.O. WOOD JOIST; A0.03 1 HR horizontal assembly, A0.08 FS-1)")
#  GAP-3 / GAP-4: campo GYP-1 colgado de Lobby 217 / 317 + vestíbulo + tramo N-S del corredor entre CLG-L2-56 (termina y 1007.64, smoke
#  curtain) y CLG-L2-58 (empieza y 1212.0); 1/A7.23 / 2/A7.23 (gypsum field, borde 1'-4 1/2" a 8'-0", bandas 1'-0"); menos el panel WS-1 sur
#  13.49 x 4.47 = 60.3 SF (medición del canon, otro oficio), el shaft y el muro S del lobby.
_R = [(709.92, 799.2, 1007.64, 1138.2), (799.2, 852.72, 1007.64, 1212.0)]
# rev20b: geometría MEDIDA (CE_CONTORNO_REAL): unión de los rectángulos - shaft - panel WS-1 (medido por H-A en 1/A7.23 y pasado a A2.02:
# X = 709.92 + (X7 - 2172.96) / 2, Y = 1007.64 + (Y7 - 1223.04) / 2; anclas: cara W del lobby = borde del anillo - 1'-0", cara N = nicho del
# elevador; comprobación: borde E del anillo = cara E del corredor 852.72 - 1'-0" = 843.7)
_G = json.load(open(f'{SP}/blind_lobby/A/geom.json'))
def _a2(x, y, xw):
    return (709.92 + (x - xw) / 2, 1007.64 + (y - 1223.04) / 2)
_U = _uu([_box(a, c, b, d) for a, b, c, d in _R]).difference(_box(755.28, 1075.32, 799.2, 1098.48))
GEO = {}
for _lv, _xw in (("L2", 2172.96), ("L3", 2172.96 - 476.64)):
    _ws = _G[_lv]["ws"]; (_x0, _y0), (_x1, _y1) = _a2(_ws[0], _ws[1], _xw), _a2(_ws[2], _ws[3], _xw)
    _P = _U.difference(_box(_x0, _y0, _x1, _y1))
    _poly = list(_P.exterior.coords)[:-1]
    for _h in _P.interiors:                     # keyhole: cada hueco (shaft, panel WS-1) con su puente al vértice más cercano (rev20b: todos)
        _hc = list(_h.coords)[:-1]
        i = min(range(len(_poly)), key=lambda k: min((_poly[k][0] - q[0]) ** 2 + (_poly[k][1] - q[1]) ** 2 for q in _hc))
        j = min(range(len(_hc)), key=lambda k: (_poly[i][0] - _hc[k][0]) ** 2 + (_poly[i][1] - _hc[k][1]) ** 2)
        _poly = _poly[:i + 1] + _hc[j:] + _hc[:j + 1] + _poly[i:]
    from shapely.geometry import Polygon as _Pg
    assert abs(abs(_Pg(_poly).area) - _P.area) < 1.0, (_lv, _Pg(_poly).area, _P.area)   # el keyhole mide lo mismo que el polígono
    _cl = [_a2(x, y, _xw) for x, y in _G[_lv]["cl"]]
    _r = _G[_lv]["ring"]; _rp = [_a2(_r[0], _r[1], _xw), _a2(_r[2], _r[1], _xw), _a2(_r[2], _r[3], _xw), _a2(_r[0], _r[3], _xw), _a2(_r[0], _r[1], _xw)]
    GEO[_lv] = {"area_sf": round(_P.area / 81, 2), "perim_lf": round(_P.length / 9, 2), "poly": [[round(x, 2), round(y, 2)] for x, y in _poly],
                "band": [[list(_cl[k]), list(_cl[k + 1])] for k in range(len(_cl) - 1)], "ring": [[list(_rp[k]), list(_rp[k + 1])] for k in range(4)]}
os.makedirs(f'{W}/etapas/4_canon/rev20', exist_ok=True)
json.dump(GEO, open(f'{W}/etapas/4_canon/rev20/geom_lobby.json', 'w'), indent=1)
for _rid, _lv, _nh, _rm in (("CLG-L2-217F", "L2", "1/A7.23", "217"), ("CLG-L3-317F", "L3", "2/A7.23", "317")):
    _net, _per = GEO[_lv]["area_sf"], GEO[_lv]["perim_lf"]
    _src = (f"{_lv} Lobby {_rm} + vestibule + corridor N-S strip (dropped GYP-1 field between the corridor rows): A3.0{_lv[1]} [DERIVED] "
            f"polygon measured in vectors = lobby + vestibule (709.92 to 799.2 x 1007.64 to 1138.2) + corridor strip (799.2 to 852.72 x 1007.64 to 1212.0) "
            f"minus the shaft (755.28 to 799.2 x 1075.32 to 1098.48) and the WS-1 panel measured on {_nh} (13.12 x 4.47 ft, other trade) = {_net} SF | {_nh} gypsum field with 1'-0\" bands "
            "and 1'-4 1/2\" border at 8'-0\" around WS-1 [CONFIRMED]; FS-1 above loaded (ceilings[]) | rev20 coverage audit GAP-3 / GAP-4 (U-189, U-190)")
    _nhg = math.ceil(_net / 16)
    for k, fam, q, op, s_ in (
            ("board", "5/8\" gyp board Type X", _net, f"{_net} SF x 1 layer(s) = {_net}", _src),
            ("main tee", "USG drywall main tee (DGLW26)", round(_net / 4.0, 2), f"{_net} SF / 4.0 ft o.c. = {round(_net / 4.0, 2)}",
             "USG drywall suspension, main tees 48 in. o.c. (manufacturer, not printed); GYP-1 'GYPSUM BOARD ON METAL SUSPENSION SYSTEM' (1/A7.23 legend)"),
            ("cross tee", "USG drywall cross tee (DGLW424)", round(_net / 1.333, 2), f"{_net} SF / 1.333 ft o.c. = {round(_net / 1.333, 2)}",
             "cross tees 16 in. o.c. for 5/8 in. board (manufacturer, not printed)"),
            ("angle molding", "USG angle molding (DGWM24)", _per, f"perimeter of the measured polygon (incl. the WS-1 opening) / 9 pt/ft = {_per} LF", "wall angle at perimeter"),
            ("hanger wire", "hanger wire", round(_nhg * 0.7917, 2), f"ROUNDUP({_net}/16) = {_nhg} hangers (4 ft x 4 ft) x drop 0.7917 ft = {round(_nhg * 0.7917, 2)}",
             "drop as CLG-L2-56 (7/A7.23 printed 9 1/2\")")):
        C['misc_items'].append({"ref": f"{_rid} {k}", "familia": fam, "qty": q, "op": op, "source": s_, "detail": f"{_nh} (RCP ceiling legend GYP-1)"})
    log.append(f"{_rid}: + {_net} SF Type X + suspension ({_per} LF angle)")

#  COBERTURA de detalles GAP-2: 5/A5.04 'CEILING APPLIED TO UNDERSIDE OF DECK' (franja 7'-3" de grid M a la fire wall, B.O. DECK 11'-2 5/8")
#  = pasaje desde el nicho CLG-L1-127 hasta la puerta 129.1; medido en 1/A7.31 (18 pt/ft).
_q = round((2406.24 - 2295.5) * (677.28 - 572.4) / 324, 2)
C['misc_items'].append({"ref": "CLG-L1-129P board", "familia": "5/8\" gyp board Type X", "qty": _q, "detail": "5/A5.04",
                        "op": f"{_q} SF x 1 layer(s) = {_q}",
                        "source": f"L1 passage from the CLG-L1-127 niche to the fire wall (door 129.1): 1/A7.31 [DERIVED] area {_q} SF "
                                  f"((2406.24-2295.5)*(677.28-572.4)/324 on 1/A7.31) | 5/A5.04 printed 'CEILING APPLIED TO UNDERSIDE OF DECK' "
                                  "(7'-3\" strip grid M to the fire wall, B.O. DECK 11'-2 5/8\") [CONFIRMED]; material not named: 5/8\" Type X "
                                  "(A0.01 706.6 1-HR rated roof assembly at the fire wall, conservative); applied to the deck, no metal printed (U-190) | "
                                  "rev20 coverage audit (details) GAP-2"})
log.append(f"CLG-L1-129P: + {_q} SF Type X (5/A5.04 CEILING APPLIED TO UNDERSIDE OF DECK)")

# (6) COORDINACIÓN 12-nov (lo dibujado se carga): lobby 217 / 317 - lazo de banda del vestíbulo y caja de borde del WS-1 (1/A7.23, 2/A7.23),
#     doble lectura ciega H-A / H-B (scratchpad blind_lobby): banda LF A 27.35 / B 26.98 -> 27.35, ancho = sección de 7/A7.23 (A 1.94 /
#     B 1.46 sin el fondo del cove) -> 1.9375; borde LF 38.16 (A = B), ancho A 1.29 (cara + fondo) / B 2.21 (las dos caras + fondo, como
#     dibujan 5/A7.23 y 6/A7.23) -> 2.2083.
import math as _m
for _lv, _rm, _nh in (("L2", "217", "1/A7.23"), ("L3", "317", "2/A7.23")):
    _lfb = round(sum(_m.dist(a, b) for a, b in GEO[_lv]["band"]) / 9, 2)     # LF medido del nivel (= el markup)
    _lfr = round(sum(_m.dist(a, b) for a, b in GEO[_lv]["ring"]) / 9, 2)
    _qb, _qr = round(_lfb * 1.9375, 2), round(_lfr * 2.2083, 2)
    C['misc_items'].append({"ref": f"SOF-{_lv}-{_rm}V board", "familia": "5/8\" gyp board Type X", "qty": _qb, "detail": "7/A7.23",
                            "op": f"{_lfb} LF x 1.9375 ft (one side: 7 3/4\" cove bottom + 4 1/2\" box face + 4 1/2\" box bottom + 6 1/2\" field face = 23 1/4\") = {_qb}",
                            "source": f"{_lv} Lobby {_rm} vestibule 1'-0\" band loop (U-run, corridor bands excluded): centreline measured in vectors on {_nh} "
                                      f"(1/4\" = 1'-0\", 18 pt/ft) = {_lfb} LF [MEASURED]; printed 1'-0\", 1'-0\", 1'-1 1/2\" wall to band [CONFIRMED 1/A7.23]; "
                                      "section = 7/A7.23 corridor band (printed 7 3/4\", 4 1/2\", 4 1/2\", 6 1/2\") | rev20 U-176 H-A 1.94 / H-B 1.46 -> 1.9375"})
    C['misc_items'].append({"ref": f"SOF-{_lv}-{_rm}B board", "familia": "5/8\" gyp board Type X", "qty": _qr, "detail": "5/A7.23",
                            "op": f"{_lfr} LF x 2.2083 ft (box around WS-1: outer face 11\" + bottom 4 1/2\" + inner face 11\" = 26 1/2\") = {_qr}",
                            "source": f"{_lv} Lobby {_rm} gypsum border box around the WS-1 panel: outer edge perimeter measured on {_nh} = {_lfr} LF [MEASURED]; "
                                      "border tags '8' - 0\"' and field 'GYP-1 8' - 11\"' [CONFIRMED 1/A7.23] -> step 11\" [DERIVED]; bottom 4 1/2\" and board on both "
                                      "faces full height [CONFIRMED 5/A7.23, 6/A7.23] | rev20 U-176 H-A 1.29 / H-B 2.21 -> 2.2083 (drawn both faces)"})
    log.append(f"SOF-{_lv}-{_rm}V / B: + {_qb} + {_qr} SF Type X")
#     beam wrap FS-1 de las vigas de borde norte (grid 1) sobre Kitchen 100 / Linen 105 / Elec 104 (auditor de detalles N3; H-A / H-B blind_bwk):
#     W24X68 (MF) D-H 29.06 LF, W24X55 (MF) B-D 17.06 LF; una cara (sur) + fondo + build-up 1 1/8" (A5.00), oculto 16 1/2" sobre el fondo de truss.
_bw = [("W24X68", 29.06, 1.54), ("W24X55", 17.06, 1.36)]
_q = round(sum(l * w for _b, l, w in _bw), 2); _lf = round(sum(l for _b, l, _w in _bw), 2); _w = round(_q / _lf, 4)
C['misc_items'].append({"ref": "BW-L1-NORTH board", "familia": "5/8\" gyp board Type C", "qty": _q, "detail": "4/S3.08",
                        "op": f"{_lf} LF x {_w} ft (W24X68 29.06 x 1.54 + W24X55 17.06 x 1.36 = {_q})",
                        "source": "A0.08 FS-1 'GYP AND RESILIENT CHANNELS WRAP STEEL BEAMS WHERE THEY ARE DEEPER THAN TRUSSES' [CONFIRMED]; S1.02 grid 1 "
                                  "W24X68 (MF) D-H and W24X55 (MF) B-D [CONFIRMED], LF measured column to column at 9 pt/ft; 4/S3.08: top of steel 13'-8\", "
                                  "18\" trusses + 2 1/2\" -> 16 1/2\" hidden above the truss bottom (12'-3 1/2\") [DERIVED]; one exposed side (south; north = "
                                  "exterior wall sheathing per 4/S3.08) + bottom + 1 1/8\" build-up (A5.00 'GYPSUM BD. & RESILIENT CHANNEL'); AISC d / bf "
                                  "(W24X68 23.73 / 8.965, W24X55 23.57 / 7.005) | rev20 U-176 H-A 67.9 SF (1.54 / 1.36) / H-B 63.6 SF -> the larger"})
_rc = round(_lf * 2, 2)
C['misc_items'].append({"ref": "BW-L1-NORTH RC", "familia": "resilient channel (printed)", "qty": _rc, "detail": "4/S3.08",
                        "op": f"{_lf} LF x 2 lines (bottom + south face) = {_rc}", "source": "as BW-L1-RETAIL north edge (A0.08 FS-1 wrap, UL L546)"})
log.append(f"BW-L1-NORTH: + {_q} SF Type C, {_rc} LF RC")

C['rev20_campo'] = log
json.dump(C, open(CP, 'w'), indent=1)
print("rev20 campo:", *log, sep="\n  ")
