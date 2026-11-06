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
                "source": f"{sh} run on {'y' if ori == 'H' else 'x'} = {c_ * 3} pt; A0.06 GN 15 + ASTM C840 (precedent R80e.34 #8: <= 30 ft, both faces, wall height)"})
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
                  "(cement board to the tile ceiling + 6\", precedent R80e.34 #15, RFI-11 closed)")
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
d['trim_none_reason'] = "Window returns: wood casing / stool covers the board edge (1-3/A8.02) - no corner bead at windows; outside corners of all floors counted by program from the wall geometry (L junctions + free wall ends; door jambs excluded)"
json.dump(d, open(f'{W}/takeoff_canon.json', 'w'), indent=1)
print('ok', len(d['existing_walls']), len(d['ceilings']), len(d['misc_items']))
