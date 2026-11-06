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
 "trim_none_reason": "Corner bead / L-bead / U-bead per 09 29 00 3.x; quantities from ventanas_trim.json (window returns + outside corners) in trim_items",
 "frp_none_reason": "No FRP wall finish in A7.19 finish schedules (TF-1 plaster / vinyl wallcovering / P-1 paint); XI.2.7 FRP exterior finish on CMU (A0.07) is not our trade",
 "types_none_reason": {"C.8-x / CM.8-x": "CIP concrete and CMU (A0.06): not our trade, no furring unless FI / FW drawn", "SFRM": "spray-applied fireproofing (A0.06 / A0.08): not our trade"},
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
 "corners_ok": [], "gaps_ok": [], "nodes": [], "details": {}, "opening_schedule": {"sources": ["A8.00", "A8.01", "S2.01", "S2.02", "S2.03", "S2.04", "M1.01", "M1.05", "P1.01", "E1.02"], "items": [], "items_none_reason": "openings in WOOD-framed walls: headers / jambs / king studs are wood (Div. 06, EXCLUDED); door frames by others (A8.00); window returns carried in trim / misc (ventanas_trim.json)"}, "openings_extra": [],
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
    if x.get('corner_bead_corners_lf'):
        trims.append({"ref": f"CB-CORR-{fl}", "kind": "corner_bead", "lf": float(x['corner_bead_corners_lf']),
                      "label": f"{fl} corridor outside corners", "source": f"A2.0{fl[1]} corridor corners; 09 29 00 2.5 / 3.x 'install cornerbead at external corners'",
                      "op": x.get('corner_bead_corners_op'), "status": "DERIVADO", "img": "2_lectura/img_ventanas"})
    for r in x.get('runs_over_30ft') or []:
        if r.get('status') == 'PENDIENTE' or not r.get('length_ft'):
            continue
        n = math.ceil(float(r['length_ft']) / 30.0 - 1e-9) - 1
        if n > 0:
            h = 9.885
            d['misc_items'].append({"ref": f"CJ-{fl}-{r['id']}", "familia": "control joint", "qty": round(n * h, 2),
                                    "op": f"ROUNDUP({r['length_ft']}/30)-1 = {n} joint(s) x {h} ft = {round(n * h, 2)}",
                                    "source": f"A0.06 GN 15 'CONTROL JOINTS IN ... PARTITIONS ... EXCEEDING 30 FT' + 09 29 00 3.x / ASTM C840; {fl} {r.get('what')} (A2.0{fl[1]} {r.get('line')})"})
d['trim_items'] = trims
d['trim_none_reason'] = "Window returns: wood casing / stool covers the board edge (1-3/A8.02) - no corner bead at windows; corridor outside corners L2 / L3 counted; L1 / L4 / guest-unit outside corners not counted (RFI-19)"
json.dump(d, open(f'{W}/takeoff_canon.json', 'w'), indent=1)
print('ok', len(d['existing_walls']), len(d['ceilings']), len(d['misc_items']))
