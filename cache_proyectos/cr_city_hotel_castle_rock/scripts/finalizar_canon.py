import re, sys as _sys
_sys.path.insert(0, '/root/skill/take-off-metal-frame-drywall/tools')
import revision_markups as _RM
"""CR City Hotel: takeoff_canon.json = base (build_canon) + campos de proyecto (exclusiones con N/HOJA, wood, tornillería,
MEP, none reasons). Los textos citan la hoja revisada."""
import json
W = '/root/cr/work/etapas/4_canon'
d = json.load(open(f'{W}/takeoff_canon.json.base.json'))
d.pop('ceilings_raw', None)
d['rfis_lectura'] = d.pop('rfis_raw', [])
d['excluded_walls'] = d.pop('discarded_raw', [])
d['constants']['type_order'] = {"value": ["W.4-0", "W.6-0", "W.6-1", "W.6-2", "W.62-1", "FW.1-0", "FW.2-0", "FW.4-0", "FW.6-0", "DW.4-1", "FI.2-0", "FI.6-0", "CH.6-2",
    "XW.6.2-0", "XW.6.2-2", "XW.6.3-0", "XW.6.3-2", "XW.6.4-0", "XW.6.4-2", "XW.6.6-1", "XW.6.6-2"], "source": "A0.06 interior wall assemblies + A0.07 exterior wall assemblies row order"}
d.update({
 "deck_breaks_none_reason": "Wood-framed floors: board height per zone from printed sections 4/A5.05, 7/A7.23, 1/A5.06, 2/A5.01 (resolucion_L1..L4); no steel deck breaks",
 "edge_blocking_none_reason": "WOOD type sections A0.06 (1/A0.09 rated intersections): board edges land on wood framing; wood blocking EXCLUDED (Div. 06)",
 "atm_recess_none_reason": "No ATM / equipment recess in the set (A2.01-A2.04, A7.30-A7.55)",
 "tile_base_none_reason": "Tile at guest baths carried as 5/8\" cement board faces (A0.06 GN 13; 09 29 00 2.4.A.2); no separate tile base item (A7.19)",
 "ballistic_jogs_none_reason": "No ballistic panels (A0.06 types W / FW / DW / FI / CH / C / CM only)",
 "trim_none_reason": "Corner bead / L-bead / U-bead per 09 29 00 3.x; quantities by program (window returns + outside corners) in trim_items",
 "frp_none_reason": "No FRP wall finish in A7.19 finish schedules (TF-1 plaster / vinyl wallcovering / P-1 paint); XI.2.7 FRP exterior finish on CMU (A0.07) is not our trade",
 "types_none_reason": {"C.8": "CIP concrete wall (A0.06 C.x): not our trade (U-061), no furring unless FI / FW drawn", "CM.4": "CMU wall (A0.06 CM.x): not our trade (U-061); furring on it read as FW / FI", "CM.8": "CMU wall (A0.06 CM.x): not our trade (U-061); furring on it read as FW / FI", "XM.0.1": "exterior masonry, not in A0.07: not our trade (U-061, RFI-02 closed)", "SFRM": "spray-applied fireproofing (A0.06 / A0.08): not our trade"},
 "deflection_clips": {"none_reason": "Wood-framed structure: no deflection clips; C-H shaft walls use J runner top and bottom (A0.06 CH)", "source": "A0.06"},
 "fasteners_excluded": {"why": "all screws / anchors / pins excluded (estimator standing order U-053)", "source": "A0.06, A0.08"},
 "wood_excluded": {"why": "wood studs, plates, trusses, blocking, FRT plywood, LP Flameblock sheathing = Div. 06, never carried (R-ALC-01 / U-139)", "source": "A0.06 WOOD / FURRED WOOD / DBL. WOOD, A0.07 XW, A0.08 FS-1 / RS-x"},
 "mep_sweep": {"sheets": ["M1.01", "M1.05", "M3.02", "P1.00", "P1.01", "P1.02", "P1.03", "P1.04", "P1.05", "E1.01", "E1.02"], "findings": ["duct penetrations through rated walls / ceilings: EXCLUDED (R-ALC-03); fire dampers / firestopping by others (07 84 13)"], "source": "M1.01"},
 "accesorios_none": [{"familia": "access panel", "why": "none scheduled for our trade (A7.19, A8.00)", "source": "A8.00"},
   {"familia": "stud reinforcement MEP", "why": "no metal stud walls with MEP penetrations: wood framing (Div. 06); duct penetrations EXCLUDED (R-ALC-03)", "source": "A0.06"},
   {"familia": "extra framing ATM", "why": "no ATM / equipment recess in the set", "source": "A2.01"},
   {"familia": "gypsum board jamb return", "why": "window / door jamb returns carried as their own rows from ventanas_trim.json (A8.02 fenestration details) - not by the metal-opening tool (wood openings)", "source": "A8.02"},
   {"familia": "Level 5 finish", "why": "no Level 5 area: 09 29 00 3.6.E.4 Level 4 under plaster / wallcovering and back of house; A7.19 TF-1 plaster or vinyl wallcovering everywhere (U-147 Level 4)", "source": "A7.19"}],
 "accesorios_rfi": [],
 "corners_ok": [], "gaps_ok": [], "nodes": [], "details": {}, "opening_schedule": {"sources": ["A8.00", "A8.01", "S2.01", "S2.02", "S2.03", "S2.04", "M1.01", "M1.05", "P1.01", "E1.02"], "items": [], "items_none_reason": "openings in WOOD-framed walls: headers / jambs / king studs are wood (Div. 06, EXCLUDED); door frames by others (A8.00); window returns carried in trim / misc (window schedule A8.01 + elevations A4.00-A4.03, measured by program)"}, "openings_extra": [],
 "plywood_strips": [], "plywood_strips_none_reason": "plywood / LP Flameblock sheathing = wood Div. 06 EXCLUDED (A0.07)",
 "blocking_items": [], "trim_items": [],
})
import math
vt = json.load(open('/root/cr/work/etapas/2_lectura/ventanas_trim.json'))
trims = []
for fl, x in sorted(vt['floors'].items()):
    if float(x.get('returns_sf') or 0) > 0:
        d['misc_items'].append({"ref": f"WIN-RET-{fl}", "familia": '5/8" gyp board Type X', "qty": round(float(x['returns_sf']), 2),
                                "op": f"{x.get('returns_sf_op')} = {x['returns_sf']} SF (window jamb 8.0 in / head + sill 7.37 in returns, scheduled Type 1 / 2)",
                                "source": f"{fl} window returns 1/A8.02, 2/A8.02, 3/A8.02 (one board layer wraps the opening behind wood trim); A8.01 types; ventanas_trim.json"})
    if False and x.get('corner_bead_corners_lf'):   # reemplazado por esquinas_cb.py (todos los pisos, RFI-19 cerrado)
        trims.append({"ref": f"CB-CORR-{fl}", "kind": "corner_bead", "lf": float(x['corner_bead_corners_lf']),
                      "label": f"{fl} corridor outside corners", "source": f"A2.0{fl[1]} corridor corners; 09 29 00 2.5 / 3.x 'install cornerbead at external corners'",
                      "op": x.get('corner_bead_corners_op'), "status": "DERIVADO", "img": "2_lectura/img_ventanas"})
    for r in []:   # reemplazado por runs del canon (abajo)
        if r.get('status') == 'PENDIENTE' or not r.get('length_ft'):
            continue
        n = math.ceil(float(r['length_ft']) / 30.0 - 1e-9) - 1
        if n > 0:
            h = 9.885
            d['misc_items'].append({"ref": f"CJ-{fl}-{r['id']}", "familia": "control joint", "qty": round(n * h, 2),
                                    "op": f"ROUNDUP({r['length_ft']}/30)-1 = {n} joint(s) x {h} ft = {round(n * h, 2)}",
                                    "source": f"A0.06 GN 15 'CONTROL JOINTS IN ... PARTITIONS ... EXCEEDING 30 FT' + 09 29 00 3.x / ASTM C840; {fl} {r.get('what')} (A2.0{fl[1]} {r.get('line')})"})
d['trim_items'] = trims
# CONTROL JOINTS (precedente R80e.34 #8: ASTM C840 <= 30 ft corridos, AMBAS caras, altura del wall): runs colineales de
# board-only walls por piso en la planta A2.0x (mismo eje +-3 pt, tramos que se tocan o con hueco <= 4 ft de puerta)
import collections
runs = collections.defaultdict(list)
for e in d['existing_walls']:
    if not e['sheet'].startswith('A2.0') or not e['id'].split(' ')[0] or e['id'].endswith((' B', ' C', ' D')):
        continue
    (x0, y0), (x1, y1) = e['path'][0], e['path'][-1]
    ori = 'H' if abs(y0 - y1) < 0.5 else 'V'
    c_ = round((y0 if ori == 'H' else x0) / 3.0)
    lo, hi = sorted((x0, x1) if ori == 'H' else (y0, y1))
    runs[(e['floor'], e['sheet'], ori, c_)].append((lo, hi, e['height_ft'], e['id']))
for (fl, sh, ori, c_), segs in sorted(runs.items()):
    segs.sort(); cur = [segs[0]]
    grupos = []
    for sg in segs[1:]:
        if sg[0] - cur[-1][1] <= 4 * 9.0:
            cur.append(sg)
        else:
            grupos.append(cur); cur = [sg]
    grupos.append(cur)
    for g in grupos:
        L = (max(s_[1] for s_ in g) - min(s_[0] for s_ in g)) / 9.0
        n = math.ceil(L / 30.0 - 1e-9) - 1
        if n > 0:
            h = max(s_[2] for s_ in g)
            d['misc_items'].append({"ref": f"CJ-{fl}-{ori}{c_ * 3}", "familia": "control joint", "qty": round(n * h * 2, 2),
                "op": f"run {round(L, 2)} ft ({len(g)} walls {g[0][3]}..{g[-1][3]}): ROUNDUP({round(L, 2)}/30)-1 = {n} joint(s) x {h} ft x 2 faces = {round(n * h * 2, 2)}",
                "source": f"{sh} run on {'vertical coord' if ori == 'H' else 'horizontal coord'} = {c_ * 3} pt; A0.06 GN 15 + ASTM C840 (estimator precedent #8 (B&N): <= 30 ft, both faces, wall height)"})
# RFI-05 cerrado (R-ALC-10 / U-082, opción A = lo impreso): A2.01 '*NOTE: GYPSUM BOARD & FINISH IN RETAIL SPACE BY FUTURE
# TENANT' -> caras retail NO rated fuera; caras retail de assemblies RATED (rating del tag > 0) se quedan: el rating impreso
# del tag exige la capa (listed design), conservador, delta anotado en el RFI.
_ret = []
for w in list(d['existing_walls']):
    f = str(w.get('location') or '').split('faces:')[-1].strip()
    if re.fullmatch(r"RETAIL 124 \(tenant\)", f) and str(w.get('type_id', '')).endswith('-0'):
        d['existing_walls'].remove(w)
        sf = round(w['length_ft'] * w['height_ft'] * w['faces'] * (w.get('layers') or 1), 1)
        _ret.append(sf)
        d['excluded_walls'].append({"id": w['id'], "reader": "AB", "floor": w['floor'], "img": w.get('img'),
            "reason": f"A2.01 '*NOTE: GYPSUM BOARD & FINISH IN RETAIL SPACE BY FUTURE TENANT': non-rated retail face ({w['type_id']}, {sf} SF board) by tenant - RFI-05 closed (option A, the printed note)"})
print('RFI-05 retail non-rated faces excluded:', len(_ret), round(sum(_ret), 1), 'SF')
# U-138 hallazgo 8: mismo criterio en la zona Food & Beverage: A2.04 / A5.07 / A7.45 / A7.50 / A7.55 'INTERIOR OF FOOD AND
# BEVERAGE SPACE IS NOT IN SCOPE OF THIS PERMIT. WILL BE SUBMITTED IN FUTURE TENANT IMPROVEMENT PERMIT.' + A0.00 'THE BAR,
# DINING, AND KITCHEN AREAS ARE BEING PERMITTED AS CORE AND SHELL SPACES' -> caras NO rated hacia F&B fuera; rated se quedan
_FB = re.compile(r"(?i)KITCHEN 100|BAR 107|DINING|\b410\b|\b411\b|\b419\b|F&B|Deck Bar|Warming Kitchen")
_fbx = []
for w in list(d['existing_walls']):
    if not str(w.get('type_id', '')).endswith('-0'):
        continue
    parts = [x.strip() for x in str(w.get('location') or '').split('faces:')[-1].split(';') if x.strip()]
    fb = [x for x in parts if _FB.search(x) and not re.search(r"(?i)lobby|corridor|vestibule|linen|stor", x)]
    if not fb:
        continue
    sf1 = round(w['length_ft'] * w['height_ft'] * (w.get('layers') or 1), 1)
    if len(fb) >= int(w.get('faces') or 1) or len(parts) <= 1:
        d['existing_walls'].remove(w)
        d['excluded_walls'].append({"id": w['id'], "reader": "AB", "floor": w['floor'], "img": w.get('img'),
            "reason": f"non-rated face(s) inside the Food & Beverage space ({'; '.join(fb)}): 'INTERIOR OF FOOD AND BEVERAGE SPACE IS NOT IN SCOPE OF THIS PERMIT' (A2.04, A5.07, A7.45, A7.50, A7.55) - future tenant improvement permit"})
        _fbx.append(sf1 * int(w.get('faces') or 1))
    else:
        w['faces'] = int(w['faces']) - len(fb)
        w['source'] = str(w.get('source') or '') + f" | face(s) {'; '.join(fb)} EXCLUDED: F&B interior NOT IN SCOPE OF THIS PERMIT (A7.45 / A7.50 / A7.55 note)"
        _fbx.append(sf1 * len(fb))
print('F&B non-rated faces excluded:', len(_fbx), round(sum(_fbx), 1), 'SF')
d.setdefault('constants', {})['plan_scale_pt_per_ft'] = {"value": 9.0, "source": "A2.01-A2.04 floor plans printed 1/8\" = 1'-0\" (9 pt/ft); per-sheet scales in plan_scale_by_sheet (enlarged plans 1/4\" = 18 pt/ft)"}
# U-114: toda área [DERIVED] con su operación y su resultado ('... /81 = 6.0')
for z in d['ceilings']:
    z['source'] = re.sub(r"(\[DERIVED\] area ([\d.]+) SF \(polygon [^|]*?/\d+(?:\.\d+)?)\)", r"\1 = \2 SF)", str(z.get('source') or ''))
# accesorios en 0 con su porqué y su hoja (U-116: ningún 'default (no sheet)')
d['accesorios_none'] = [x for x in d.get('accesorios_none') or [] if x.get('familia') not in ('additional head track', '2-1/2" CFMF coiling grille head')] + [
    {"familia": "additional head track", "why": "openings are in WOOD-framed walls (A0.06 W / FW / DW, A8.00 door schedule): headers / jambs are wood, Div. 06 EXCLUDED (U-139); no metal-stud opening over 4'-0\"", "source": "A0.06, A8.00"},
    {"familia": "2-1/2\" CFMF coiling grille head", "why": "no coiling grille / overhead door head in a metal-framed wall in the set (A8.00 door schedule: hollow metal / wood doors only)", "source": "A8.00"}]
# tags del inventario descartados con motivo e imagen (U-037 / ONE WALL ONCE): leyendas y límite de permiso aparte
import glob as _g
_td = []
_png = {o['id']: o.get('png') for _k, _v in json.load(open('/root/cr/work/etapas/1_inventario/inventario.json'))['ocurrencias'].items() for o in _v if o.get('id')}
_byid = {}
for _f in ('2_lectura/canon_A.json', '2_lectura/canon_B.json'):
    for _t in json.load(open(f'/root/cr/work/etapas/{_f}')).get('tags_descartados') or []:
        if isinstance(_t, dict) and _t.get('id'):
            x = _byid.setdefault(_t['id'], {"id": _t['id'], "motivo": None, "imagen": None, "floor": _t.get('floor')})
            x['motivo'] = x['motivo'] or _t.get('motivo') or _t.get('reason')
            x['imagen'] = x['imagen'] or _t.get('imagen') or _t.get('img') or None
for x in _byid.values():
    if not re.match(r'^P[A-Z]\d{4}$', str(x['id'])):
        continue   # nota de grupo de la lectura, no un tag del inventario
    if not x['imagen'] and _png.get(x['id']):
        x['imagen'] = f"/root/cr/work/etapas/1_inventario/recortes/{_png[x['id']]}"
    _td.append(x)
for _id in ('PT0264', 'PT0265'):
    _td.append({"id": _id, "motivo": "W.6 | 1 example tag of the A2.01 '1. REFERENCE LEGEND, RE: FLOOR PLANS' (partition type symbol legend), not a wall", "imagen": "1_inventario/recortes/PT0264_PT0265_A2.01_reference_legend.png", "floor": "L1"})
d['tags_descartados'] = _td
# BE-119 / U-099: la fuente IMPRESA de la altura de cada wall en sus campos (la lee revision_markups / CE_ALTURA_IMPRESA)
for w in d['existing_walls']:
    m = re.search(r"\| height: ([^|]*)", str(w.get('source') or ''))
    if m and not w.get('height_source'):
        hs = m.group(1).strip()
        w['height_note'] = hs
        h = float(w.get('height_ft') or 0)
        if 'cement' in str(w.get('board') or '') and abs(h - 9.0) < 0.01 and not hs.lower().startswith('bath ceiling'):
            hs = ("Bath ceiling GYP-1 8'-6\" (A7.xx unit RCP) + 6\" above line of ceiling (A0.06 furred wood head detail) = 9'-0\" "
                  "(cement board to the tile ceiling + 6\", estimator precedent #15 (B&N), RFI-11 closed)")
        elif 'deep floor/ceiling zone' in hs and abs(h - 9.24) < 0.01:
            hs = "11'-0\" - 1'-9 1/8\" = 9'-2 7/8\" (4/A5.05 printed floor-to-floor minus printed deep floor / ceiling zone)"
        elif "1'-1 3/8" in hs and abs(h - 9.885) < 0.01:
            hs = "11'-0\" - 1'-1 3/8\" = 9'-10 5/8\" (4/A5.05 printed floor-to-floor minus the rated corridor assembly printed on 7/A7.23)"
        if 'vector' in hs:   # medida vectorial: la escala impresa no es una altura (BE-121)
            hs = re.sub(r"\(?(\d+/\d+)\"\s*=\s*1'-0\"(,\s*)?", r"(scale \1 in/ft) ", hs).replace("in/ft  pt/ft", "in/ft, pt/ft")
        w['height_source'] = hs
        w['height_status'] = 'DERIVADO' if re.search(r"=|\+| - |minus", hs) else 'CONFIRMADO'
        # U-099: la altura cargada = la cota IMPRESA exacta (8'-11 1/4" = 8.9375, no 8.94 redondeado)
        _hp = _RM.altura_impresa(hs, w['height_status'])[0]
        if _hp is not None and abs(_hp - h) < 0.01:
            w['height_ft'] = round(_hp, 4)
# ---- Auditoría U-138 (6-nov) hallazgos 1-3 -------------------------------------------------------------------------
_FS1 = {"id": "FS-1", "source": "A0.08 FS-1 'LEVEL 2, 3, 4 THROUGHOUT' + 'LEVEL 2 ABOVE PARKING AT ALLEY', 1 HOUR (1/2 HR REQD.), UL L546: 5/8\" TYPE C GYP BD on RESILIENT CHANNELS"}
_RC = {"value": 16, "source": "UL L546 (spacing 'per assembly', not printed): 16 in. o.c. loaded (estimator precedent (O'Reilly #5), ASTM C754)"}
_l1w = [q for w in d['existing_walls'] if w['sheet'] == 'A2.02' for q in w['path']]   # placa del piso L2 (misma posición en A3.01)
_bb = [min(q[0] for q in _l1w), min(q[1] for q in _l1w), max(q[0] for q in _l1w), max(q[1] for q in _l1w)] if _l1w else None
_xwl2 = round(sum(w['length_ft'] for w in d['existing_walls'] if w['floor'] == 'L2' and str(w['type']).startswith('XW') and (w['id'].endswith(' A') or ' ' not in w['id'])), 1)
_band = round(_xwl2 * 0.75, 1)
_fs1_l1 = round(8587 - _band - 2 * 151.85, 1)
d['ceilings'].append({"room": "L1 FS-1 membrane under the LEVEL 2 floor (whole floor plate)", "system": "resilient_channel", "area_sf": _fs1_l1,
    "board": "5/8 type C", "assembly": _FS1, "rc_oc_in": _RC, "layers": {"value": 1, "source": "A0.08 FS-1 1 layer"}, "detail": "A0.08 FS-1",
    "source": (f"A0.08 FS-1 'LEVEL 2, 3, 4 THROUGHOUT' = membrane on the underside of the LEVEL 2 floor (L1 ceiling plane, above the L1 dropped ceilings) | "
               f"[DERIVED] area {_fs1_l1} SF = A0.01 'LEVEL 2 8,587 SQ FT TOTAL GROSS' [CONFIRMED] - exterior wall band {_xwl2} LF x 0.75 ft = {_band} "
               f"- 2 stairs 151.85 SF each (7/A6.01 and 4/A6.02 printed inner dims 8'-8 3/4\" x 17'-4 3/4\") = {_fs1_l1}; elevator hoistways not deducted (conservative, about +90 SF)"),
    "floor": "L1", "img": "/root/cr/work/auditoria_U138/img/A008_FS1.png", "height_ft": 12.0, "sheet": "A3.01", "poly_hint": _bb,
    "height_source": "5/A5.04 L1 12'-0\" B.O. DECK"})
# Retail 124: GYP-1 (franja 11'-0") = falso plafón del tenant (A2.01 note) -> fuera; la membrana rated FS-1 queda en el renglón de arriba
_ret = [m for m in d['misc_items'] if 'RETAIL 124' in str(m.get('source')) and str(m.get('ref', '')).startswith('CLG-L1')]
for m in _ret:
    d['misc_items'].remove(m)
d.setdefault('excluded_items', []).append({"refs": sorted({m['ref'].rsplit(' ', 1)[0] for m in _ret}), "reason": "Retail 124 GYP-1 dropped ceiling (A3.01 11'-0\" strip): A2.01 '*NOTE: GYPSUM BOARD & FINISH IN RETAIL SPACE BY FUTURE TENANT' (non-rated, tenant); the rated FS-1 membrane above it is carried in 'L1 FS-1 membrane under the LEVEL 2 floor'"})
# Retail: wrap de vigas (A0.08 FS-1 note 'GYP AND RESILIENT CHANNELS WRAP STEEL BEAMS WHERE THEY ARE DEEPER THAN TRUSSES'; A3.01 'ASSEMBLY TO WRAP BOTTOM OF STEEL BEAMS. TYP.')
_blf = round(22.35 + 22.32 + 22.35 + 20.29 + 19.49 + 31.67 + 15.76, 2)
_dev = round(0.59 + 2 * 1.0, 2)
_bsrc = (f"A3.01 retail 124 steel beams measured on the vector lines at the printed 1/8\" = 9 pt/ft: verticals 22.35 + 22.32 + 22.35 + 20.29 + 19.49 + horizontals 31.67 + 15.76 = {_blf} LF [DERIVED]; "
         f"wrap developed = bottom flange 0.59 ft (drawn) + 2 sides x 1'-0\" (drop below trusses NOT printed: RFI-20) = {_dev} ft; A0.08 FS-1 note; A3.01 'ASSEMBLY TO WRAP BOTTOM OF STEEL BEAMS. TYP.'")
d['misc_items'] += [
    {"ref": "BW-L1-RETAIL board", "familia": '5/8" gyp board Type C', "qty": round(_blf * _dev, 2), "op": f"{_blf} LF x {_dev} ft = {round(_blf * _dev, 2)} SF", "source": _bsrc, "detail": "A0.08 FS-1"},
    {"ref": "BW-L1-RETAIL RC", "familia": "resilient channel (printed)", "qty": round(_blf * 3, 2), "op": f"{_blf} LF x 3 lines (bottom + 2 sides) = {round(_blf * 3, 2)}", "source": _bsrc, "detail": "A0.08 FS-1"}]
# L4 corridor 412: cielo de campo (A2.04 '1350 SF', A3.04 stipple gyp) = RS-1 bajo el techo, como los cuartos de L4
d['ceilings'].append({"room": "L4 412 Corridor (field ceiling)", "system": "resilient_channel", "area_sf": 1350.0, "board": "5/8 type X",
    "assembly": {"id": "RS-1", "source": "A0.08 RS-1 (ceiling under the roof framing) - board type not printed: 5/8\" Type X loaded (RFI-15)"},
    "rc_oc_in": _RC, "layers": {"value": 1, "source": "A0.08 RS-1 1 layer drawn"}, "detail": "1/A5.06",
    "source": "A0.08 / RCP A3.04: A3.04 [CONFIRMED] area 1350 SF (A2.04 '1350 SF CORRIDOR 412') | A3.04 gyp stipple + perimeter cove (cove carried in SOF-L4-02) | [CONFIRMED] height 8.94 (1/A5.06 8'-11 1/4\")",
    "floor": "L4", "img": "/root/cr/work/auditoria_U138/img/A304_corr412_419.png", "height_ft": 8.9375, "sheet": "A3.04"})
# U-138 hallazgo 5: franja de L3 (301-304) bajo las terrazas 420 / 421 de L4 = techo RS-6 (A0.08 RS-6 '2 LAYERS, 5/8" TYPE 'X' GYP
# BOARD', WOOD FRAMING, roof RE: A2.05), no FS-1: ancho (1065.5 - 1007.35)/9 = 6.46 ft (fachada E de L3 vs de L4, A2.03 / A2.04) x 66.17 ft
_strip = round(6.46 * 66.17, 1)
_rs = [x for x in d['ceilings'] if x['floor'] == 'L3' and re.search(r"Guest room 30[1-4]\b", x['room'])]
_tot = sum(float(x['area_sf']) for x in _rs)
for x in _rs:
    sh_ = round(_strip * float(x['area_sf']) / _tot, 2)
    x['area_sf'] = round(float(x['area_sf']) - sh_, 2)
    x['source'] = str(x['source']) + f" | minus {sh_} SF under the L4 terrace (RS-6 strip, see RS6-L3 row)"
d['misc_items'].append({"ref": "RS6-L3 board", "familia": '5/8" gyp board Type X', "qty": round(_strip * 2, 2), "op": f"6.46 ft x 66.17 ft = {_strip} SF x 2 layers = {round(_strip * 2, 2)}",
    "source": "A0.08 RS-6 (ROOF, RE: A2.05): '2 LAYERS, 5/8\" TYPE 'X' GYP BOARD' on wood framing, under the L4 terraces 420 / 421 (A2.05 RS-6) above L3 rooms 301-304; strip width = (1065.5 - 1007.35)/9 = 6.46 ft (L3 vs L4 east facade lines, A2.03 / A2.04 at 9 pt/ft), length 66.17 ft [DERIVED]",
    "detail": "A0.08 RS-6"})
# U-138 hallazgo 11: mezzanine 219 bajo techo inclinado (sin tag ni cielo en A3.02): board siguiendo la pendiente sobre RC (RS-1, RFI-15)
_mz = [m for m in d['misc_items'] if str(m.get('ref', '')).startswith('CLG-L2-64 ')]
if _mz:
    for m in _mz:
        d['misc_items'].remove(m)
    _src = "L2 Mech & water heater mezzanine 219 under the sloped roof (A3.02 shows no ceiling, roof type not tagged): RS-1 board on resilient channel following the roof slope = 2 x 10.85 ft x 24.73 ft = 536.7 SF [DERIVED, 1/A4.04 vector at the printed scale] (RFI-15; flat plan area 462 SF printed on A2.02)"
    d['misc_items'] += [{"ref": "CLG-L2-64 board", "familia": '5/8" gyp board Type X', "qty": 536.7, "op": "2 x 10.85 x 24.73 = 536.7 SF x 1 layer", "source": _src, "detail": "1/A4.04"},
                        {"ref": "CLG-L2-64 RC", "familia": "resilient channel (printed)", "qty": round(536.7 / (16 / 12.0), 2), "op": "536.7 SF / 1.333 ft o.c. = 402.53", "source": _src, "detail": "1/A4.04"}]
# U-137 / U-141: detalles que gobiernan renglones nuestros (verificados a ojo, burbujas/img_verif)
_xw = "XW exterior wall rows (interior Type X layers continuous at the rated floor line, exterior gyp sheathing; FRT wood EXCLUDED)"
d['details'] = dict(d.get('details') or {}, **{f"{n}/A0.09": f"FIRE RATED INTERSECTIONS: 2 layers 5/8\" Type X continuous at the 2 HR exterior wall / floor intersection -> {_xw}" for n in (3, 5, 6, 7, 8, 9, 10, 11, 12, 13)})
d['details'].update({
    "2/A5.02": _xw, "3/A5.02": _xw, "1/A5.03": _xw, "1/A5.07": _xw, "7/A9.02": _xw,
    "2/A5.00": _xw + "; FS-1 resilient channel ceiling at the floor line",
    "3/A5.08": "CH.6-2 C-H shaft wall rows (6\" 20 GA C-H, J-runner, 1\" shaftliner + 2 layers 5/8\" Type X)",
    "2/A7.23": "L3 corridor ceiling / soffit rows (enlarged RCP N-S, same corridor cove as 7/A7.23)",
    "7/A7.23": "corridor soffit / cove rows (framed soffit, ceiling track)",
    "12/A9.03": "smoke-curtain gypsum soffit at the elevator lobby (soffit rows)",
})
# formato G_DETALLE: {N/HOJA: {source (con N/HOJA), img (existe), title, notes}} desde los destinos verificados a ojo
_bv = json.load(open('/root/cr/work/burbujas/burbujas_verificadas.json')).get('_destinos') or {}
import os as _os
for _k, _txt in list(d['details'].items()):
    if isinstance(_txt, dict):
        continue
    _x = _bv.get(_k) or {}
    _im = str(_x.get('img') or '').split(' #')[0]
    _im = _im if _im.startswith('/') else f"/root/cr/work/burbujas/{_im}" if _im else ''
    if not (_im and _os.path.exists(_im)) and _os.path.exists(f"/root/cr/work/burbujas/img_verif/DET_{_k.split('/')[0]}_{_k.split('/')[1]}.png"):
        _im = f"/root/cr/work/burbujas/img_verif/DET_{_k.split('/')[0]}_{_k.split('/')[1]}.png"
    if not (_im and _os.path.exists(_im)):
        _cand = sorted(__import__('glob').glob(f"/root/cr/work/burbujas/img_verif/*{_k.split('/')[1]}*{_k.split('/')[0]}*.png")) or sorted(__import__('glob').glob(f"/root/cr/work/burbujas/img_verif/*{_k.split('/')[1]}*.png"))
        _im = _cand[0] if _cand else ''
    d["details"][_k] = {"source": f"{_k} (detail read: body, notes and the bubbles it calls; CADENA.md)", "img": _im, "title": _x.get("title") or _k, "notes": _txt, "sealant_none_reason": "acoustical / joint sealant EXCLUDED in all projects by estimator standing order (ALC-19)"}
# corner bead por programa (scripts/esquinas_cb.py): outside corners de L junctions + extremos libres que no son door jambs
cbj = json.load(open('/root/cr/work/etapas/4_canon/out/corner_bead.json'))
for k, v in sorted(cbj['por_hoja'].items()):
    if not v['lf']:
        continue
    sh, fl = k.split()
    nL, nE = v['L_corners'], v['free_ends']
    hs = sorted({c['h'] for c in v['corners']})
    d['trim_items'].append({"ref": f"CB-{fl}-{sh}", "kind": "corner_bead", "lf": v['lf'], "label": f"{fl} outside corners on {sh}",
        "source": f"{sh} [DERIVED] wall geometry at printed scale {v['scale_pt_per_ft']} pt/ft; 09 29 00 3.x 'install cornerbead at external corners' (ASTM C840)",
        "op": f"{nL} L corner(s) x 1 + {nE} free wall end(s) x 2 (door jambs at printed door tags excluded) = {nL + 2 * nE} corners x wall height ({', '.join(str(h) for h in hs)} ft) = {v['lf']} LF",
        "status": "DERIVADO", "img": f"4_canon/img/cb/CB_{sh}_{fl}.png"})
# U-138 hallazgo 4: corner bead en el perímetro de los window returns (A8.02 dibuja solo el lado exterior: no hay casing / stool
# interior impreso que tape el canto) y en el canto inferior de cada soffit / cove
for fl, x in sorted(vt['floors'].items()):
    m_ = re.search(r"If trim deleted: ([\d.]+) LF \(([^)]*)\)", str(x.get('corner_bead_windows_note') or ''))
    if m_ and float(m_.group(1)) > 0:
        d['trim_items'].append({"ref": f"CB-WIN-{fl}", "kind": "corner_bead", "lf": float(m_.group(1)), "label": f"{fl} window return perimeters",
            "source": f"{fl} window returns (1/A8.02, 2/A8.02, 3/A8.02 detail only the EXTERIOR side: no interior casing / stool printed) - outside corner of the 5/8\" board return at every window, 09 29 00 3.x 'install cornerbead at external corners'; windows per A8.01 + elevations A4.00-A4.03",
            "op": f"window perimeters {m_.group(2)} = {m_.group(1)} LF", "status": "DERIVADO", "img": "2_lectura/img_ventanas"})
for m in [m for m in d['misc_items'] if str(m.get('ref', '')).startswith('SOF-') and str(m.get('ref', '')).endswith('board')]:
    m_ = re.match(r"\s*([\d.]+) LF", str(m.get('op') or ''))
    if m_:
        d['trim_items'].append({"ref": m['ref'].replace(' board', ' CB'), "kind": "corner_bead", "lf": float(m_.group(1)), "label": "soffit / cove bottom edge",
            "source": f"{m['ref'].replace(' board', '')}: outside corner between the soffit bottom and its vertical face (1 line per soffit LF); {str(m.get('source'))[:160]}",
            "op": f"{m_.group(1)} LF soffit length x 1 edge = {m_.group(1)}", "status": "DERIVADO",
            "img": "/root/cr/work/burbujas/img_verif/" + ("G2_A7.31_det.png" if 'L1' in m['ref'] else "G2_A9.03_det.png" if 'smoke' in str(m.get('source')).lower() else "G2_A7.23_det.png")})
d['trim_none_reason'] = "Corner bead: outside corners of all floors by program (L junctions between interior 2-face walls + free wall ends, door jambs and exterior-wall corners excluded), window return perimeters and soffit / cove bottom edges"
json.dump(d, open(f'{W}/takeoff_canon.json', 'w'), indent=1)
print('ok', len(d['existing_walls']), len(d['ceilings']), len(d['misc_items']))
