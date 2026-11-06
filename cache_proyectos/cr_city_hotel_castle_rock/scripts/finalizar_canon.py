import re, sys as _sys
_sys.path.insert(0, '/root/skill/take-off-metal-frame-drywall/tools')
import revision_markups as _RM
"""CR City Hotel: takeoff_canon.json = base (build_canon) + campos de proyecto (exclusiones con N/HOJA, wood, tornillería,
MEP, none reasons). Los textos citan la hoja revisada."""
import json
W = '/root/cr/work/etapas/4_canon'
d = json.load(open(f'{W}/takeoff_canon.json.base.json'))
# BE-CR26 (rev2, auditoría U-138 #2): vanos_puertas escribía el canon FINAL de la corrida anterior y finalizar leía la base: los
# arreglos de vanos (W.4-L3-44, W.4-L4-22, W.4-L4-21 -> A7.50, recortes) nunca llegaban al canon. Candado: el efecto de cada paso llega.
_vp = json.load(open(f'{W}/out/vanos_puertas.json'))
_ids = {e['id'].split(' ')[0] for e in d['existing_walls']}
_malos = [x['id'].split(' ')[0] for x in _vp.get('eliminados') or [] if x['id'].split(' ')[0] in _ids]
assert not _malos, f"BE-CR26: vanos_puertas no llegó a la base que lee finalizar: {_malos[:5]}"
d.pop('ceilings_raw', None)
d['rfis_lectura'] = d.pop('rfis_raw', [])
d['excluded_walls'] = d.pop('discarded_raw', []) + (d.get('excluded_walls') or [])   # BE-CR26: + exclusiones de vanos_puertas sobre la base
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
        d['excluded_walls'].append({"id": w['id'], "reader": "AB", "floor": w['floor'], "img": w.get('img'), "tag_ids": w.get('tag_ids') or [], "sheet": w.get('sheet'),
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
        d['excluded_walls'].append({"id": w['id'], "reader": "AB", "floor": w['floor'], "img": w.get('img'), "tag_ids": w.get('tag_ids') or [], "sheet": w.get('sheet'),
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
# Decisión del estimador (usuario 6-nov: "yes"): el soffit del ENTRY CANOPY (08/A9.05 'GYP/METAL SOFFIT PANEL', aplicado bajo la
# placa de acero, sin framing dibujado) es nuestro: 5/8" exterior gypsum soffit board Type X + trim en los 3 bordes libres.
# Profundidad 4.85 ft [DERIVED] en 08/A9.05 a 1 1/2" = 1'-0" (108 pt/ft); largo a lo largo del muro NO acotado: 12'-0" (RFI-21)
_cd, _cl = 4.85, 12.0
d['misc_items'] += [
    {"ref": "CAN-L1-ENTRY board", "familia": '5/8" EXTERIOR gyp sheathing Type X', "qty": round(_cd * _cl, 2), "op": f"{_cd} ft x {_cl} ft = {round(_cd * _cl, 2)} SF x 1 layer",
     "source": "08/A9.05 (= 8/A9.05) ROOF DETAIL - ENTRY CANOPY 'GYP/METAL SOFFIT PANEL' under the 1/4\" steel plate canopy (no soffit framing drawn: board applied to the canopy steel); depth 4.85 ft [DERIVED, measured on 08/A9.05 at the printed 1 1/2\" = 1'-0\"]; length 12'-0\" assumed (not dimensioned, RFI-21); estimator decision 6-nov: gypsum soffit = our scope",
     "detail": "08/A9.05"}]
d['trim_items'].append({"ref": "CAN-L1-ENTRY trim", "kind": "corner_bead", "lf": round(2 * _cd + _cl, 2), "label": "entry canopy soffit free edges",
    "source": "08/A9.05: exterior soffit board edges (2 ends + front) - edge trim; length per RFI-21", "op": f"2 x {_cd} + {_cl} = {round(2 * _cd + _cl, 2)} LF",
    "status": "DERIVADO", "img": "/root/cr/work/burbujas/img_verif/DET_08_A9.05.png"})
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
    "08/A9.05": "ENTRY CANOPY (8/A9.05): 'GYP/METAL SOFFIT PANEL' under the steel plate canopy -> CAN-L1-ENTRY exterior soffit board + edge trim (RFI-21 length)",
    "4/A4.03": "BUILDING SECTION: LEVEL 1 6197.75' / LEVEL 2 6211.75' / LEVEL 3 6222.75' / LEVEL 4 6233.75' / ROOF 6247.75' -> floor-to-floor 14'-0\" / 11'-0\" / 11'-0\" / 14'-0\" used in every wall height (Partition Takeoff, Height)",
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
        _cand = sorted(__import__('glob').glob(f"/root/cr/work/burbujas/img_verif/*{_k.split('/')[1]}_overview.png")) or sorted(__import__('glob').glob(f"/root/cr/work/burbujas/img_verif/*{_k.split('/')[1]}*{_k.split('/')[0]}*.png")) or sorted(__import__('glob').glob(f"/root/cr/work/burbujas/img_verif/*{_k.split('/')[1]}*.png"))
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
# BE-03 (rev2, BOTH SIDES por cara): la cara interior de XW.6.3 en 209 (L2) / 309 (L3) cubre dormitorio + baño. Partición del
# baño medida en vectores (A2.02 / A2.03, 1/8" = 9 pt/ft): caras de la partición y = 1133.4 / 1137.0; el baño va de 1137.0 al extremo
# 1230.27 del path. A2.0x GN 4 'PROVIDE WATER RESISTANT GYP BD AT TOILET AND LAVATORY AREAS' -> tramo del baño = Type X W.R.
for wid, cuarto in (("XW.6.3-L2-08 B", "209"), ("XW.6.3-L3-09 B", "309")):
    for w in [x for x in d['existing_walls'] if x['id'] == wid]:
        (x0, y0), (x1, y1) = w['path']
        lo, hi = min(y0, y1), max(y0, y1)
        if hi - 1137.0 < 50:
            continue
        nw = json.loads(json.dumps(w))
        w['path'] = [[x0, lo], [x1, 1133.4]]
        w['length_ft'] = round((1133.4 - lo) / 9.0, 2)
        w['location'] = re.sub(r"faces:.*$", f"faces: guest room {cuarto} (sleeping area, dry)", str(w['location']))
        w['source'] = str(w['source']).replace(f"= {nw['length_ft']}", f"= {nw['length_ft']}; dry part to the bath partition face: (1133.4-{lo})/9 = {w['length_ft']} ft [DERIVED]", 1)
        nw['id'] = wid[:-1] + 'D'
        nw['board'] = '5/8 type X WR'
        nw['path'] = [[x0, 1137.0], [x1, hi]]
        nw['length_ft'] = round((hi - 1137.0) / 9.0, 2)
        nw['location'] = re.sub(r"faces:.*$", f"faces: {cuarto} bath (toilet / lavatory, wet)", str(nw['location']))
        nw['source'] = (f"1/{nw['sheet']} [DERIVED] length: bath part of the grid-Q interior face, from the bath partition face (vector y 1137.0) to the end of the path "
                        f"({hi}-1137.0)/9 = {nw['length_ft']} ft (1/8\" = 9 pt/ft); board W.R. per {nw['sheet']} GN 4 'PROVIDE WATER RESISTANT GYP BD AT TOILET AND LAVATORY AREAS' "
                        "" + (" | height:" + str(nw['source']).split('| height:', 1)[1] if '| height:' in str(nw['source']) else ''))
        nw['img'] = 'etapas/4_canon/img/wet_209_309_east_wall.png'
        d['existing_walls'].insert(d['existing_walls'].index(w) + 1, nw)
# ===================== AUDITORÍA U-138 #2 (rev2): F4 / F5 / F7 / F8 / F9 / F12, verificados en el plano =====================
# F4: L3 cara interior de muros exteriores XW: 4/A5.05 imprime junto al muro exterior la zona de piso SHALLOW 1'-1 1/4" en L2-L3 y en
# L3-L4 (8'-11" + 11 3/4" = 9'-10 3/4") -> 11'-0" - 1'-1 1/4" = 9'-10 3/4" (igual que L2), no 9'-2 7/8" (zona profunda de los cuartos)
_F4 = "11'-0\" - 1'-1 1/4\" = 9'-10 3/4\" (4/A5.05 printed at the exterior wall: shallow floor zone 1'-1 1/4\" at L2-L3 and L3-L4; L3-L4 printed 8'-11\" + 11 3/4\" = 9'-10 3/4\")"
for w in d['existing_walls']:
    if w['floor'] == 'L3' and str(w.get('type_id', '')).startswith('XW') and not re.search(r"(?i)exterior|sheathing|cement", str(w.get('board'))) \
            and abs(float(w['height_ft']) - 9.2396) < 0.001:
        w['height_ft'] = 9.8958; w['height_status'] = 'DERIVADO'; w['height_source'] = _F4
        w['source'] = re.sub(r"\| height:[^|]*", "| height: " + _F4 + " ", str(w['source']), count=1)
# F5: exterior gyp sheathing de L2 = floor to floor como L1 (14'-0") y L3 (11'-0"): 4/A5.06 imprime 11'-0" LEVEL 2 a LEVEL 3 y el
# sheathing pasa por delante del rim (4/A5.05 9'-10 3/4" + 1'-1 1/4" = 11'-0"). L4 queda en 8'-11 1/4" impreso en 1/A5.06.
_F5 = "11'-0\" LEVEL 2 6211.75' -> LEVEL 3 6222.75' printed (4/A5.06; 4/A5.05 9'-10 3/4\" + 1'-1 1/4\" = 11'-0\"): exterior gyp sheathing continuous past the floor zone (per-floor slice = floor to floor, same as L3)"
for w in d['existing_walls']:
    if w['floor'] == 'L2' and re.search(r"(?i)exterior gyp sheathing", str(w.get('board'))) and abs(float(w['height_ft']) - 9.8958) < 0.001:
        w['height_ft'] = 11.0; w['height_status'] = 'DERIVADO'; w['height_source'] = _F5
        w['source'] = re.sub(r"\| height:[^|]*", "| height: " + _F5 + " ", str(w['source']), count=1)
# F7 / F8: demising DW.4 de las unidades sur (L2 205-209, L3 305-308) y 213 / 313: caras por tramo con las particiones del baño
# medidas en vectores (1/A2.02 = 1/A2.03, misma geometría): caras del demising de 1001.2 a 1206.0 = 22.76 ft (no a ejes 997.4-1209.0);
# baños: 205 / 206 / 207 = 1128.0-1206.0, 208 = 1101.7-1206.0 (partición 1098.2 / 1101.7); 213 / 313 = cara sur completa.
_DWF = "1/{sh} [DERIVED] length: {lbl} ({hi}-{lo})/9 = {L} ft (vector faces of the demising and of the bath partition; A2.0x GN 4 water resistant at toilet / lavatory)"


def _rehacer(base, fl, caras):
    es = [x for x in d['existing_walls'] if re.sub(r" [A-Z]$", "", x['id']) == base and x['floor'] == fl]
    if not es:
        print('F7: no existe', base); return
    w = next((x for x in es if 'cement' not in str(x['board'])), es[0])
    i0 = d['existing_walls'].index(es[0])
    for x in es:
        d['existing_walls'].remove(x)
    (x0, y0), (x1, y1) = w['path']
    vert = abs(x1 - x0) < 1.0
    hpart = (" | height:" + str(w['source']).split('| height:', 1)[1]) if '| height:' in str(w['source']) else ''
    k = 0
    for lbl, segs in caras:
        for lo, hi, board in segs:
            nw = json.loads(json.dumps(w))
            nw['id'] = base + ' ' + "ABCDEFGHIJKL"[k]; k += 1
            nw['path'] = [[x0, lo], [x1, hi]] if vert else [[lo, y0], [hi, y1]]
            nw['length_ft'] = round((hi - lo) / 9.0, 2)
            nw['faces'] = 1
            nw['board'] = '5/8 type X WR' if board == 'WR' else '5/8 type X'
            nw['location'] = re.sub(r"faces:.*$", "faces: " + lbl + (' bath (toilet / lavatory)' if board == 'WR' else ' room (dry)'), str(w['location']))
            nw['source'] = _DWF.format(sh=w['sheet'], lbl=lbl, hi=hi, lo=lo, L=nw['length_ft']) + " (auditoria U-138 #2 F7 / F8)" + hpart
            nw['length_status'] = 'DERIVADO'
            d['existing_walls'].insert(i0, nw); i0 += 1


for fl, n in (("L2", "2"), ("L3", "3")):
    _rehacer(f"DW.4-{fl}-0{'7' if fl == 'L2' else '9'}" if False else (f"DW.4-L2-07" if fl == "L2" else "DW.4-L3-09"), fl,
             [(f"{n}05", [(1001.2, 1124.4, 'X'), (1128.0, 1206.0, 'WR')]), (f"{n}06", [(1001.2, 1124.4, 'X'), (1128.0, 1206.0, 'WR')])])
    _rehacer("DW.4-L2-08" if fl == "L2" else "DW.4-L3-10", fl,
             [(f"{n}06", [(1001.2, 1206.0, 'X')]), (f"{n}07", [(1001.2, 1124.4, 'X'), (1128.0, 1206.0, 'WR')])])
    _rehacer("DW.4-L2-09" if fl == "L2" else "DW.4-L3-11", fl,
             [(f"{n}07", [(1001.2, 1206.0, 'X')]), (f"{n}08", [(1001.2, 1098.2, 'X'), (1101.7, 1206.0, 'WR')])])
    _rehacer("DW.4-L2-01" if fl == "L2" else "DW.4-L3-05", fl,
             [(f"{n}14", [(536.9, 703.9, 'X')]), (f"{n}13", [(536.9, 703.9, 'WR')])])
_rehacer("DW.4-L2-10", "L2", [("208", [(1001.2, 1141.6, 'X')]), ("209", [(1001.2, 1141.6, 'X')])])
# F9: XW.6.2-L1-03 (XW.6.2-0 NO rated): cara Retail 124 fuera por RFI-05 (1/A2.01 '*NOTE: GYPSUM BOARD & FINISH IN RETAIL SPACE BY
# FUTURE TENANT'); la cara exterior del type (A0.07 XW.6.2-0: 5/8" outboard of stud, type not labeled) = exterior gyp sheathing Type X
for w in [x for x in d['existing_walls'] if x['id'] == 'XW.6.2-L1-03']:
    sf = round(w['length_ft'] * w['height_ft'], 1)
    d['excluded_walls'].append({"id": "XW.6.2-L1-03 B", "reader": "AB", "floor": "L1", "sheet": w['sheet'], "img": w.get('img'), "tag_ids": w.get('tag_ids') or [],
                                "reason": f"1/A2.01 '*NOTE: GYPSUM BOARD & FINISH IN RETAIL SPACE BY FUTURE TENANT': non-rated retail face (XW.6.2-0, {sf} SF board) by tenant - RFI-05 closed (auditoria U-138 #2 F9)"})
    w['id'] = 'XW.6.2-L1-03 A'; w['faces'] = 1
    w['board'] = '5/8 exterior gyp sheathing type X'
    w['location'] = re.sub(r"faces:.*$", "faces: exterior/grey-area side (5/8\" outboard board of A0.07 XW.6.2-0, type not labeled -> exterior gyp sheathing Type X like the other XW types)", str(w['location']))
    w['faces_none_reason'] = "other face (Retail 124) by tenant: '*NOTE: GYPSUM BOARD & FINISH IN RETAIL SPACE BY FUTURE TENANT' printed in Retail 124 on 1/A2.01 (RFI-05 closed)"
# F12: FW.2-L4-11 termina en la cara del CMU (vector 751.08 en 1/A2.04), no en 765.2
for w in d['existing_walls']:
    if w['id'].split(' ')[0] == 'FW.2-L4-11':
        (x0, y0), (x1, y1) = w['path']
        if max(x0, x1) > 760:
            old = w['length_ft']
            w['path'] = [[min(x0, x1), y0], [751.08, y1]]
            w['length_ft'] = round((751.08 - min(x0, x1)) / 9.0, 2)
            w['length_status'] = 'DERIVADO'
            w['source'] = re.sub(r"^[^|]*", f"1/A2.04 [DERIVED] length: (751.08-{min(x0, x1)})/9 = {w['length_ft']} ft to the CMU face (was {old}, auditoria U-138 #2 F12) ", str(w['source']), count=1)
# U-114 (rev2): una altura [DERIVED] lleva su operación con resultado: 'A + B' / 'A - B' sin '=' -> se agrega '= <resultado>'
# solo si la suma / resta de las cotas impresas del texto da la altura cargada (si no, se informa y no se toca)
_RXV = re.compile(r"(?:(\d{1,2})'\s*-?\s*)?(\d{1,2})(?:\s+(\d{1,2})/(\d{1,2}))?\"")


def _ftin_val(m):
    return float(m.group(1) or 0) + (float(m.group(2)) + (float(m.group(3)) / float(m.group(4)) if m.group(3) else 0)) / 12.0


def _fmt(h):
    ft = int(h + 1e-9); r = round((h - ft) * 12 * 8) / 8
    if r >= 12:
        ft, r = ft + 1, r - 12
    ent = int(r); fr = r - ent
    from fractions import Fraction
    f = Fraction(fr).limit_denominator(8)
    return f"{ft}'-{ent}" + (f" {f.numerator}/{f.denominator}" if f else "") + '"'


_sin_op = []
for w in d['existing_walls']:
    hs = str(w.get('height_source') or '')
    if w.get('height_status') != 'DERIVADO' or '=' in hs or 'vector' in hs:
        continue
    vals = [_ftin_val(m) for m in _RXV.finditer(hs)]
    h = float(w.get('height_ft') or 0)
    par = None
    for i in range(len(vals)):
        for j in range(len(vals)):
            if i != j and par is None:
                if '+' in hs and i < j and abs(vals[i] + vals[j] - h) < 0.01:
                    par = (vals[i], ' + ', vals[j])
                elif re.search(r" - |minus", hs) and abs(vals[i] - vals[j] - h) < 0.01:
                    par = (vals[i], ' - ', vals[j])
    if par:
        w['height_source'] = hs + f" -> {_fmt(par[0])}{par[1]}{_fmt(par[2])} = {_fmt(h)}"
    else:
        _sin_op.append(w['id'])
# U-114 (rev2): un largo [DERIVED] que es la cota impresa tal cual ('printed 10'-0"; 10.000', sin operación) = [CONFIRMED]
_conf = []
for w in d['existing_walls']:
    sx = str(w.get('source') or '').split('| height:')[0]
    if str(w.get('length_status') or 'DERIVADO').upper().startswith('DERIV') and not re.search(r"\+|minus| - |vector|=|\bnet\b|less|(?<!not )(?<!NOT )deduct|portion|part of|split", sx.split('printed', 1)[-1]):
        m = re.search(r"printed (\d{1,2})'-(\d{1,2})(?: (\d)/(\d{1,2}))?\"", sx)
        if m:
            v = int(m.group(1)) + (int(m.group(2)) + (int(m.group(3)) / int(m.group(4)) if m.group(3) else 0)) / 12
            if abs(v - float(w['length_ft'])) < 0.01:
                w['length_status'] = 'CONFIRMADO'
                w['source'] = str(w['source']).replace('[DERIVED] length', '[CONFIRMED] length', 1)
                _conf.append(w['id'])
print('U-114 largos = cota impresa -> CONFIRMADO:', len(_conf), _conf[:6])
print('U-114 alturas DERIVED sin operación cerrada:', len(_sin_op), _sin_op[:8])
# BE-03 / RFI-11 (rev2, barrido de caras con baño cargadas Type X o todo W.R.): tramos por particiones medidas en vectores
# (1/8" = 9 pt/ft). A2.0x GN 4 'PROVIDE WATER RESISTANT GYP BD AT TOILET AND LAVATORY AREAS'; 6/A7.02 (Type 1 bath, pared del
# corridor): TILE-1 solo en el tramo del shower, resto TF-1 -> shower = W.R. + 1 layer cement board a 9'-0" (RFI-11), resto del baño
# = W.R., cuartos secos = Type X. Imágenes etapas/4_canon/img/wet/.
_CBU_H = next((x.get('height_source') for x in d['existing_walls'] if x['id'] == 'W.4-L2-03 A'), "Bath ceiling GYP-1 8'-6\" + 6\" = 9'-0\" (RFI-11)")
_IMGW = 'etapas/4_canon/img/wet/'
_T1 = [(None, 'X', 'entry')]   # placeholder


def _dividir(eid, segs, img, nota):
    ws = [x for x in d['existing_walls'] if x['id'] == eid]
    if not ws:
        return
    w = ws[0]
    (x0, y0), (x1, y1) = w['path']
    vert = abs(x1 - x0) < 1.0
    a0, a1 = (min(y0, y1), max(y0, y1)) if vert else (min(x0, x1), max(x0, x1))
    base = re.sub(r" [A-Z]$", "", eid)
    usadas = {x['id'][-1] for x in d['existing_walls'] if re.sub(r" [A-Z]$", "", x['id']) == base and re.search(r" [A-Z]$", x['id'])}
    libres = [ch for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if ch not in usadas]
    i0 = d['existing_walls'].index(w)
    d['existing_walls'].remove(w)
    hpart = (" | height:" + str(w['source']).split('| height:', 1)[1]) if '| height:' in str(w['source']) else ''
    nuevos, primero = [], True
    for lo, hi, board, label in segs:
        lo, hi = max(lo, a0), min(hi, a1)
        if hi - lo < 1.0:
            continue
        for cbu in ((False, True) if board == 'WR+CBU' else (False,)):
            nw = json.loads(json.dumps(w))
            nw['id'] = eid if primero else base + ' ' + libres.pop(0)
            primero = False
            nw['path'] = [[x0, lo], [x1, hi]] if vert else [[lo, y0], [hi, y1]]
            nw['length_ft'] = round((hi - lo) / 9.0, 2)
            nw['location'] = re.sub(r"faces:.*$", "faces: " + label, str(w['location']))
            nw['img'] = _IMGW + img
            op = f"({hi}-{lo})/9 = {nw['length_ft']} ft"
            if cbu:
                nw.update({"board": "5/8 cement board", "layers": 1, "faces": 1, "height_ft": 9.0, "height_status": "DERIVADO", "height_source": _CBU_H})
                nw['source'] = f"1/{w['sheet']} [DERIVED] length: {label}, shower tile face {op} (vector shower curb / partition lines); {nota} | height: {_CBU_H}"
            else:
                nw['board'] = '5/8 type X WR' if board.startswith('WR') else '5/8 type X'
                nw['source'] = f"1/{w['sheet']} [DERIVED] length: {label} {op} (vector partition faces); {nota}{hpart}"
            nuevos.append(nw)
    for k, nw in enumerate(nuevos):
        d['existing_walls'].insert(i0 + k, nw)


_N1 = "GN 4 water resistant at toilet / lavatory; 6/A7.02 Type 1 bath: TILE-1 at the shower only (RFI-11 cement board rule)"
for fl, eid, a0 in (("L2", "W.62-L2-01 B", 349.8), ("L3", "W.62-L3-03 A", 441.0)):
    n = 2 if fl == "L2" else 3
    segs = ([(a0, 388.7, 'WR+CBU', f"{n}01 shower"), (388.7, 442.6, 'WR', f"{n}01 bath (toilet / lavatory)")] if fl == "L2" else []) + [
        (442.6 if fl == "L2" else a0, 563.4, 'X', f"{n}01 / {n}02 entries"), (563.4, 617.3, 'WR', f"{n}02 bath (toilet / lavatory)"), (617.3, 647.9, 'WR+CBU', f"{n}02 shower"),
        (647.9, 707.3, 'X', f"{n}02 / {n}03 entries"), (707.3, 761.2, 'WR', f"{n}03 bath (toilet / lavatory)"), (761.2, 791.8, 'WR+CBU', f"{n}03 shower"),
        (791.8, 851.2, 'X', f"{n}03 / {n}04 entries"), (851.2, 905.0, 'WR', f"{n}04 bath (toilet / lavatory)"), (905.0, 935.8, 'WR+CBU', f"{n}04 shower"),
        (935.8, 1209.0, 'X', f"{n}04 entry / {n}05")]
    _dividir(eid, segs, "type1_bath_201_202_zoom.png", _N1)
# L3-02 (301 bath, 353.6-441): cement board solo en el shower (353.6-388.7), no en todo el baño
for w in d['existing_walls']:
    if w['id'] == 'W.62-L3-02 A' and 'cement' in str(w['board']):
        w['path'] = [[w['path'][0][0], 353.6], [w['path'][-1][0], 388.7]]
        w['length_ft'] = round((388.7 - 353.6) / 9.0, 2)
        w['location'] = re.sub(r"faces:.*$", "faces: 301 bath", str(w['location']))   # misma cara que W.62-L3-02 C (W.R.)
        w['source'] = f"1/A2.03 [DERIVED] length: 301 shower tile face (388.7-353.6)/9 = {w['length_ft']} ft (vector shower curb); {_N1} | height: " + str(w['source']).split('| height:', 1)[-1]
        w['img'] = _IMGW + "type1_bath_201_202_zoom.png"
for fl in ("L2", "L3"):
    n = 2 if fl == "L2" else 3
    _dividir(f"XW.6.3-{fl}-01 B", [(624.5, 711.4, 'WR', f"{n}14 bath (toilet / lavatory)"), (711.4, 739.9, 'WR+CBU', f"{n}14 shower"),
                                   (739.9, 858.7, 'X', f"{n}15 cleaning"), (858.7, 917.0, 'WR+CBU', f"{n}01 shower (back wall)"), (917.0, 1065.5, 'X', f"{n}01 room")],
             "north_wall_L3.png", _N1 + "; same stack as XW.6.6-L4-03 (405 bath incl. shower 709-740)")
    _dividir(f"XW.6.3-{fl}-04 B", [(394.8, 566.3, 'X', f"{n}14 room"), (566.3, 649.6, 'WR', f"{n}13 bath (toilet / lavatory, shower not on this wall)"),
                                   (649.6, 1046.6, 'X', f"{n}13 / {n}12 / {n}11 rooms"), (1046.6, 1136.6, 'WR', f"{n}11 bath (toilet / lavatory, shower not on this wall)"),
                                   (1136.6, 1275.5, 'X', f"{n}10 room")], f"west_wall_{fl}.png", _N1)
# BE-82 (rev2): FW.1-L1-02 (elevator shaft east face, 8/A6.00) y FW.1-L1-03 (Stair 1 north face, 10/A6.01) son recintos distintos en 1/A2.01
for w in d['existing_walls']:
    if w['id'] == 'FW.1-L1-03' and 'not the same wall' not in str(w.get('source')):
        w['source'] = str(w['source']) + " | not the same wall as FW.1-L1-02: Stair 1 (127) enclosure vs the elevator shaft, two separate boxes on 1/A2.01"
# U-140 (rev2, COORDINACIÓN 6-nov): alturas vectoriales L4 de stair (5/A6.02, 11/A6.01): fuente impresa buscada por piso.
# Impreso: datums LEVEL 4 6233.75 y ROOF 6247.75 (5/A6.02) y la nota 'RATED WALL CONTINUOUS TO UNDERSIDE OF ROOF SHEATHING. TYP.'
# (11/A6.01); la cota LEVEL 4 -> underside of roof sheathing NO está impresa en ninguna de las dos vistas -> queda vectorial (AMBER real)
for w in d['existing_walls']:
    hs = str(w.get('height_source') or '')
    if w['floor'] == 'L4' and 'vector' in hs and ('5/A6.02' in hs or '11/A6.01' in hs) and 'U-140 printed search' not in hs:
        v = '5/A6.02' if '5/A6.02' in hs else '11/A6.01'
        w['height_source'] = hs + (f" | U-140 printed search on {v}: datums LEVEL 4 6233.75 / ROOF 6247.75 and the note 'RATED WALL CONTINUOUS TO UNDERSIDE OF ROOF SHEATHING. TYP.' are printed; "
                                   f"the LEVEL 4 to underside-of-roof-sheathing height is NOT dimensioned in the stair view -> vector measurement kept")
# BE-CR25 (rev2, BOTH SIDES por wall): el wall con UNA cara cargada lleva el motivo de la otra con N/HOJA verificada
# (vistas 1/A2.01, 1/A2.03, 1/A2.04, 1/A7.45, 3/A7.50 leídas en el título impreso de cada vista; nota F&B dentro de Kitchen 100
# en 1/A7.45 y dentro de 419 / 410 en 1/A2.04 y 3/A7.50; nota retail dentro de Retail 124 en 1/A2.01)
_UNA = {
    "W.6-L1-03": "other face (Kitchen 100 / bar passage) inside the Food & Beverage space: 'INTERIOR OF FOOD AND BEVERAGE SPACE IS NOT IN SCOPE OF THIS PERMIT' printed in Kitchen 100 on 1/A7.45 - future tenant improvement permit",
    "W.6-L1-04": "other face (Kitchen 100, F&B) inside the Food & Beverage space: 'INTERIOR OF FOOD AND BEVERAGE SPACE IS NOT IN SCOPE OF THIS PERMIT' printed in Kitchen 100 on 1/A7.45 - future tenant improvement permit",
    "W.6-L1-23": "other face (Retail 124) by tenant: '*NOTE: GYPSUM BOARD & FINISH IN RETAIL SPACE BY FUTURE TENANT' printed in Retail 124 on 1/A2.01 (RFI-05 closed, option A)",
    "W.6-L4-05": "other face (419 Warming Kitchen) inside the Food & Beverage space: 'INTERIOR OF FOOD AND BEVERAGE SPACE IS NOT IN SCOPE OF THIS PERMIT' printed on 1/A2.04 and 3/A7.50",
    "W.6-L4-07": "other face (419 Warming Kitchen) inside the Food & Beverage space: 'INTERIOR OF FOOD AND BEVERAGE SPACE IS NOT IN SCOPE OF THIS PERMIT' printed on 1/A2.04 and 3/A7.50",
    "NULL-L3-11": "inside face is the interior of the small shaft box (no access, no board printed) on 1/A2.03; RFI-09 open, outside face only loaded",
    "NULL-L3-12": "inside face is the interior of the small shaft box (no access, no board printed) on 1/A2.03; RFI-09 open, outside face only loaded",
    "NULL-L3-13": "inside face is the interior of the small shaft box (no access, no board printed) on 1/A2.03; RFI-09 open, outside face only loaded",
    "NULL-L3-14": "inside face is the interior of the small shaft box (no access, no board printed) on 1/A2.03; RFI-09 open, outside face only loaded",
    "DW.4-L3-04b": "DW.4 double wall: this entry is the north (304) leaf; its south side faces the cavity against XW.6.3-L3-06 (no board in a cavity) on 1/A2.03",
}
for w in d['existing_walls']:
    k = re.sub(r" [A-Z]$", "", w['id'])
    if k in _UNA:
        w['faces_none_reason'] = _UNA[k]
json.dump(d, open(f'{W}/takeoff_canon.json', 'w'), indent=1)
print('ok', len(d['existing_walls']), len(d['ceilings']), len(d['misc_items']))
