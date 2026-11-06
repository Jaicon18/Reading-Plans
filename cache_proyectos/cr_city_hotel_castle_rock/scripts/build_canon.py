"""CR City Hotel - paso 6: resuelto_L1..L4.json -> etapas/4_canon/takeoff_canon.json (canon v68/v69).
Proyecto WOOD-FRAMED: todo wall de wood = existing_walls (board only, framing EXCLUDED Div. 06, R80f.1 / U-139).
C-H shaft walls (metal): board / liner en existing_walls + C-H studs y J-runner en misc_items (programa, op visible).
Ceilings: FS-1 = resilient_channel (BE-CR03); GYP-1 / GYP-2 = USG drywall suspension (usg_grid) por área (RFI-CR-GYP1).
Nada se suma a mano: las cantidades las calcula canon.py / accesorios / plantilla."""
import json, math, os, re, sys, glob
W = '/root/cr/work/etapas'
OUT = f'{W}/4_canon/takeoff_canon.json'
ORDER = ['W.4', 'W.6', 'W.62', 'FW.1', 'FW.2', 'FW.4', 'FW.6', 'DW.4', 'FI.2', 'FI.6', 'CH.2', 'CH.4', 'CH.6',
         'XW.6.2', 'XW.6.3', 'XW.6.4', 'XW.6.6', 'XI.2.7', 'X.6.3', 'X.2.6', None]
RX_TILE = re.compile(r'cement|cbu|tile', re.I)
DEC = "R80f.1 / U-139 (user 2026-11-01 / 2026-11-05): wood-framed wall - gypsum board is our scope, wood framing EXCLUDED (Div. 06)"


GN21 = "A0.06 GN 21 'FIRE PARTITIONS SHALL EXTEND FROM THE TOP OF THE FOUNDATION OR FLOOR/ CEILING ASSEMBLY BELOW TO THE UNDERSIDE OF THE FLOOR OR ROOF SHEATHING'"


def limpia(t, rfi=None):
    """texto de la lectura -> texto del Excel: N/HOJA sin ceros falsos (00/A7.05), sin nombres de archivo internos, la
    coordenada 'y' en mayúscula (no es la conjunción en español), cita parafraseada reemplazada por el texto impreso."""
    t = str(t or '')
    t = re.sub(r"(?i)'?rated wall continuous to underside of roof sheathing'?", GN21, t)
    t = re.sub(r"\b0\d/(A\d\.\d\d)", r"\1", t)
    t = re.sub(r"[\w./-]*\.json\b", "the reading file", t)
    t = re.sub(r"\by\b", "Y", t)
    if rfi and re.search(r"(?i)not printed|assum|blank|empty", t) and 'RFI-' not in t:
        t += f" ({rfi})"
    return t


def board_key(face, wall):
    b = str(face.get('board') or '')
    tid = str(wall.get('type_id') or '')
    if re.search(r'shaft\s*(wall)?\s*liner|shaftliner', b, re.I):
        return '1 shaftliner'
    if re.search(r'exterior', b, re.I):
        return '5/8 exterior gyp sheathing type X'
    if RX_TILE.search(b):
        return '5/8 cement board'
    # RFI-CR-GN10: WOOD / FW / DW / FI type sections A0.06 print '5/8" TYPE X GYP BD TYP.'; GN10 says plain 5/8" at
    # non-rated walls -> conservative Type X loaded everywhere (consistent), delta to regular in the RFI
    wet = bool(face.get('wet'))
    return '5/8 type X WR' if wet else '5/8 type X'


def norm_band(b):
    b = dict(b)
    if float(b['c1']) - float(b['c0']) > float(b['hi']) - float(b['lo']):
        b.update(c0=b['lo'], c1=b['hi'], lo=b['c0'], hi=b['c1'])
    return b


def main():
    floors = {}
    for f in sorted(glob.glob(f'{W}/4_canon/resuelto_L*.json')):
        d = json.load(open(f)); floors[d.get('floor') or os.path.basename(f)[9:11]] = d
    escala = {}
    for fl in ('L1', 'L2', 'L3', 'L4'):
        for l in ('A', 'B'):
            p = f'{W}/2_lectura/{l}/{fl}.json'
            if os.path.exists(p):
                for s in json.load(open(p)).get('scale') or []:
                    try:
                        escala.setdefault(s['sheet'], {"value": float(s['pt_per_ft']), "source": f"{s['sheet']} {s.get('view','')} printed {s.get('printed','')}".strip()})
                    except Exception:
                        pass
    ex, misc, ceil, rfis, desc, tags_desc = [], [], [], [], [], []
    for fl, d in sorted(floors.items()):
        for w in d['walls']:
            tid = w.get('type_id'); typ = w.get('type'); asum = None
            if not tid:   # untagged wall loaded with the analogous type (RFI-04): the loaded type names its row / markup
                asum = str(w.get('type_assumed') or w.get('assumed_type') or w.get('type_id_loaded') or '').split(' ')[0] or None
                tid = asum; typ = tid.rsplit('-', 1)[0] if tid else None
            L = float(w.get('length_ft') or 0)
            if L <= 0:
                continue
            sh = w.get('sheet'); b = norm_band(w['band'])
            sc = escala.get(sh)
            if not sc:
                sc = {"value": 18.0 if sh.startswith('A7') or sh.startswith('A6') else 9.0, "source": f"{sh} printed scale (reader)"}
                escala[sh] = sc
            s = float(sc['value']); c = (float(b['c0']) + float(b['c1'])) / 2; lo = float(b['lo'])
            path = [[lo, c], [lo + L * s, c]] if b['ori'] == 'H' else [[c, lo], [c, lo + L * s]]
            path = [[round(x, 3), round(y, 3)] for x, y in path]
            grupos = {}
            for fc in w.get('faces') or []:
                ly = int(fc.get('layers') or 0); h = float(fc.get('height_ft') or 0)
                if ly <= 0 or h <= 0:
                    continue
                k = board_key(fc, w)
                if fc.get('tile') and k != '1 shaftliner' and k != '5/8 exterior gyp sheathing type X':
                    k = '5/8 cement board'
                if k == '5/8 cement board':
                    # Type X W.R. layers of the type stay full height (UL design / A0.06 GN 11) + 1 layer CBU over them
                    g = grupos.setdefault(('5/8 type X WR', ly, round(h, 3)), {'faces': 0, 'src': [], 'rooms': []})
                    g['faces'] += 1; g['src'].append(fc.get('height_source') or ''); g['rooms'].append(fc.get('room') or '')
                    ly = 1
                    if fl in ('L2', 'L3', 'L4') and h > 9.0:
                        h = 9.0   # precedent R80e.34 #15: CBU to the highest printed finish + 6" = bath ceiling GYP-1 8'-6" (unit RCP) + 6"
                g = grupos.setdefault((k, ly, round(h, 3)), {'faces': 0, 'src': [], 'rooms': []})
                g['faces'] += 1; g['src'].append(fc.get('height_source') or ''); g['rooms'].append(fc.get('room') or '')
            for n, ((k, ly, h), g) in enumerate(sorted(grupos.items())):
                eid = f"{w['id']}{'' if len(grupos) == 1 else ' ' + 'ABCDEFG'[n]}"
                ex.append({"id": eid, "type_id": tid, "type": typ, "floor": fl, "sheet": sh, "page": w.get('page'),
                           "path": path, "length_ft": round(L, 3), "height_ft": h, "faces": g['faces'], "layers": ly,
                           "board": k, "location": f"{fl} {'[TYPE ASSUMED - RFI-04] ' if asum else ''}{w.get('location', '')} | faces: {'; '.join(r for r in g['rooms'] if r)}"[:300],
                           "source": None,
                           "decision": DEC if w.get('framing') != 'metal' else "C-H shaft wall (A0.06 CH, UL U415): board / liner here, C-H studs + J-runner in misc_items",
                           "keynote": (re.search(r"\b[0-9A-Z]{1,3}/A\d\.\d{2}\b", str(w.get('detail') or '')) or re.search(r"\b[0-9A-Z]{1,3}/A\d\.\d{2}\b", g['src'][0] or '') or
                                       type('m', (), {'group': lambda self, i=0: {'L1': '5/A5.04', 'L2': '4/A5.05', 'L3': '4/A5.05', 'L4': '1/A5.06'}[fl]})()).group(0),
                           "tag_ids": w.get('tag_ids') or [], "length_status": w.get('length_status'), "_src": (w, g['src'][0], asum),
                           "img": w.get('img'), "height_img": w.get('height_img')})
            if w.get('framing') == 'metal' and str(typ or '').startswith('CH'):
                size = {'CH.2': '2-1/2"', 'CH.4': '4"', 'CH.6': '6"'}.get(typ, '6"')
                H = max([float(fc.get('height_ft') or 0) for fc in w.get('faces') or []] + [0])
                n_st = math.ceil(L / 2.0 - 1e-6) + 1
                misc.append({"ref": f"CH-STUD {w['id']}", "familia": f"C-H stud {size} (printed)", "qty": round(n_st * H, 2),
                             "op": f"ROUNDUP({L}/2.0)+1 = {n_st} studs x {H} ft = {round(n_st * H, 2)}",
                             "source": f"{sh} {w['id']}; A0.06 CH '{size} 20GA METAL C-H STUD' (UL U415); spacing 24 in. o.c. per UL U415 (not printed on A0.06)"})
                misc.append({"ref": f"J-RUNNER {w['id']}", "familia": f"J-runner {size} (printed)", "qty": round(2 * L, 2),
                             "op": f"2 x {L} (top + bottom 'J' RUNNER CHANNEL) = {round(2 * L, 2)}",
                             "source": f"{sh} {w['id']}; A0.06 CH '\"J\" RUNNER CHANNEL'"})
        for c in d.get('ceilings') or []:
            ceil.append(dict(c, floor=fl))
        rfis += [dict(r, floor=fl) for r in d.get('rfis') or []]
        desc += [dict(x, floor=fl) for x in d.get('discarded') or []]
    ceilings = []
    RCP = {'L1': 'A3.01', 'L2': 'A3.02', 'L3': 'A3.03', 'L4': 'A3.04'}
    STRUCT = {'L1': (12.0, "L1 ceilings: 12'-0\" B.O. structure (5/A5.04, resolucion_L1)"),
              'L2': (9.24, "4/A5.05 room zone 9'-2 7/8\" (11'-0\" - 1'-9 1/8\" floor zone)"),
              'L3': (9.24, "4/A5.05 room zone 9'-2 7/8\" (11'-0\" - 1'-9 1/8\" floor zone)"),
              'L4': (8.94, "1/A5.06 8'-11 1/4\" roof ceiling line")}
    def area_of(c):
        a = c.get('area_sf')
        if isinstance(a, dict):
            a = sum(float(v) for v in a.values())
        try:
            return float(a or 0)
        except Exception:
            return 0.0
    def cls(c):
        a = str(c.get('assembly') or '')
        if a.startswith('RS-') or 'roof RS-1' in a or 'underside of roof' in a:
            return 'RS'
        if 'FS-1' in a:
            return 'FS-1'
        if 'GYP-2' in a:
            return 'GYP-2'
        if 'ACT' in a or 'WS-1' in a:
            return 'notours'
        if 'GYP' in a.upper() or 'gyp' in str(c.get('board') or ''):
            return 'GYP-1'
        return 'other'
    for i, c in enumerate(ceil):
        A = area_of(c); k = cls(c); fl = c['floor']; room = f"{fl} {c.get('room')}"[:120]
        ast_ = '[CONFIRMED]' if str(c.get('area_status')).upper().startswith('CONFIRM') else '[DERIVED]'
        hst_ = '[CONFIRMED]' if str(c.get('height_status')).upper().startswith('CONFIRM') else '[DERIVED]'
        src = limpia(f"{RCP.get(c['floor'], '')} {ast_} area {c.get('area_sf') if not isinstance(c.get('area_sf'), dict) else ''} SF ({c.get('area_source') or ''} {c.get('area_op') or ''}) | {c.get('assembly')} | {hst_} height {c.get('height_ft')} ({c.get('height_source') or ''})")[:700]
        if A <= 0 or k == 'notours':
            continue
        wet = bool(c.get('wet'))
        if k in ('FS-1', 'RS'):
            bd = '5/8 type C' if k == 'FS-1' else '5/8 type X'
            ceilings.append({"room": room, "system": "resilient_channel", "area_sf": round(A, 2), "board": bd,
                             "assembly": {"id": 'FS-1' if k == 'FS-1' else 'RS-1',
                                          "source": "A0.08 FS-1 (5/8\" TYPE C GYP BD CEILING, RESILIENT CHANNELS 'SPACING PER ASSEMBLY', UL L546)" if k == 'FS-1'
                                          else "A0.08 RS-1 (ceiling 'RE: REFLECTED CEILING PLANS', board on channel under wood framing drawn) - board type not printed: 5/8\" Type X loaded (RFI-CR-RS1)"},
                             "rc_oc_in": {"value": 16, "source": "UL L546 / RS-1 (spacing 'per assembly', not printed): 16 in. o.c. loaded (RFI-CR-RC, alt 12 in. o.c.)"},
                             "layers": {"value": 1, "source": "A0.08 " + ('FS-1 1 layer' if k == 'FS-1' else 'RS-1 1 layer drawn')},
                             "detail": ('4/A5.05' if k == 'FS-1' else '1/A5.06'),
                             "source": f"A0.08 / RCP {RCP.get(fl, '')}: {src}", "floor": fl, "img": c.get('img'), "height_ft": c.get('height_ft')})
            continue
        # GYP-1 / GYP-2 / other: metal suspension (USG drywall suspension) - legend 'ON METAL SUSPENSION SYSTEM, OR WOOD FRAMING'
        ly = 2 if k == 'GYP-2' else 1
        bdf = '5/8" gyp Type X W.R.' if wet else '5/8" gyp board Type X'
        h = float(c.get('height_ft') or 0); st, sts = STRUCT.get(fl, (h + 1, 'n/a'))
        drop = round(max(0.5, st - h), 3) if h else 1.0
        per = round(4 * math.sqrt(A), 2)
        ref = f"CLG-{fl}-{i:02d}"
        nota = ("GYP-2 'GYPSUM BOARD CEILING, RATED 2-HOURS, AER-09038' (layers not printed): 2 layers 5/8\" Type X loaded (RFI-CR-GYP2)" if k == 'GYP-2'
                else "GYP-1 'GYPSUM BOARD ON METAL SUSPENSION SYSTEM, OR WOOD FRAMING': metal suspension loaded (conservative, RFI-CR-GYP1)")
        if k == 'other':
            nota = "ceiling type not labeled (A3.0x): GYP-1 metal suspension loaded as the adjacent typical (RFI-CR-CLG)"
        det = f"1/{RCP.get(fl, 'A3.01').split()[0]} (RCP ceiling legend '{k if k != 'other' else 'GYP-1'}: GYPSUM BOARD ON METAL SUSPENSION SYSTEM, OR WOOD FRAMING'; no suspension detail printed - RFI-CR-GYP1)"
        misc += [
            {"detail": det, "ref": f"{ref} board", "familia": bdf, "qty": round(A * ly, 2), "op": f"{A} SF x {ly} layer(s) = {round(A * ly, 2)}", "source": f"{room}: {src}; {nota}"},
            {"detail": det, "ref": f"{ref} main tee", "familia": "USG drywall main tee (DGLW26)", "qty": round(A / 4.0, 2), "op": f"{A} SF / 4.0 ft o.c. = {round(A / 4.0, 2)}", "source": f"{room}: USG drywall suspension, main tees 48 in. o.c. (manufacturer, not printed); {nota}"},
            {"detail": det, "ref": f"{ref} cross tee", "familia": "USG drywall cross tee (DGLW424)", "qty": round(A / (16 / 12.0), 2), "op": f"{A} SF / 1.333 ft o.c. = {round(A / (16 / 12.0), 2)}", "source": f"{room}: cross tees 16 in. o.c. for 5/8 in. board (manufacturer, not printed)"},
            {"detail": det, "ref": f"{ref} angle molding", "familia": "USG angle molding (DGWM24)", "qty": per, "op": f"4 x sqrt({A}) = {per} (square-equivalent perimeter, DERIVED: room polygon perimeter not read)", "source": f"{room}: wall angle at perimeter"},
            {"detail": det, "ref": f"{ref} hanger wire", "familia": "hanger wire", "qty": round(math.ceil(A / 16.0) * drop, 2), "op": f"ROUNDUP({A}/16) = {math.ceil(A / 16.0)} hangers (4 ft x 4 ft) x drop {drop} ft ({st} structure - {h} ceiling) = {round(math.ceil(A / 16.0) * drop, 2)}", "source": f"{room}: structure {sts}; ceiling {c.get('height_source') or ''}"[:500]}]
    # SOFFITS / corridor cove bands (readers' soffits[]): board = LF x (bottom width + vertical face) per layer; framing
    # = 2 lines of ceiling / soffit track per LF (7/A7.23 framed soffit). LF not printed = RFI-18 (load per rule below).
    for fl, d in sorted(floors.items()):
        corr_lf = sum(float(w.get('length_ft') or 0) for w in d['walls'] if re.search(r'\b412\b|CORRIDOR 412', str(w.get('location') or ''), re.I))
        for si, s in enumerate(d.get('soffits') or []):
            sid = s.get('id') or f"SOF-{fl}-{si + 1:02d}"
            lf = s.get('lf') if s.get('lf') is not None else s.get('length_ft')
            loc = str(s.get('location') or s.get('where') or s.get('room') or '')
            src0 = f"{fl} {loc}: {s.get('lf_op') or s.get('length_source') or ''} | {s.get('height_source') or s.get('bottom_source') or ''} | {s.get('detail') or s.get('note_printed') or ''}"[:600]
            if lf is None and fl == 'L4' and 'Corridor 412' in loc and corr_lf:
                lf = round(corr_lf, 2); src0 += f" | LF NOT dimensioned on L4 RCP: loaded = corridor 412 wall LF {lf} (resuelto_L4 walls facing 412), RFI-18"
            if lf is None:
                rfis.append({"id": "RFI-18", "item": sid, "floor": fl, "assumption_loaded": "not loaded (LF not dimensioned)", "delta": "LF x height"}); continue
            lf = float(lf)
            if 'coffer' in loc.lower():
                bsf = lf * float(s.get('height_ft') or 0); op = f"{lf} LF x {s.get('height_ft')} ft vertical face = {round(bsf, 2)}"
            elif s.get('depth_ft'):
                bsf = lf * (float(s['depth_ft']) + float(s.get('drop_ft') or 0)); op = f"{lf} x ({s['depth_ft']} bottom + {s.get('drop_ft') or 0} face) = {round(bsf, 2)}"
            else:
                wdt = float(s.get('width_ft') or 0.375); vf = float(s.get('vertical_face_ft') or 0.542)
                bsf = lf * (wdt + vf); op = f"{lf} LF x ({wdt} bottom + {vf} vertical) = {round(bsf, 2)}"
            misc.append({"ref": f"{sid} board", "familia": '5/8" gyp board Type X', "qty": round(bsf, 2), "op": op, "source": src0})
            misc.append({"ref": f"{sid} track", "familia": "track de ceilings / soffits", "qty": round(2 * lf, 2), "op": f"2 lines x {lf} LF = {round(2 * lf, 2)} (framed soffit 7/A7.23 / 2/A7.31)", "source": src0})
    for e in ex:
        w_, hs_, asum_ = e.pop('_src')
        ts_ = str(w_.get('type_source') or '')
        rfi_ = ('RFI-04' if asum_ else 'RFI-01' if 'W.6.1' in ts_ else 'RFI-03' if e['type_id'] in ('W.6-0',) else 'RFI-02' if e['type_id'] in ('XW.6.6-0', 'FW.4-1', 'FW.4-2', 'XW.6.3-1', 'XW.6.4-1', 'FW.1-0') else 'RFI-04')
        st_ = '[CONFIRMED]' if str(w_.get('length_status')).upper().startswith('CONFIRM') else '[DERIVED]'
        e['source'] = limpia(f"{e['keynote']}; {e['sheet']} {st_} length ({w_.get('length_source', '')}; {w_.get('length_op', '')}) | height: {hs_[:220]} | type: {ts_} | detail: {w_.get('detail', '')}", rfi_)[:900]
        e['location'] = limpia(e['location'])
    ex.sort(key=lambda e: (ORDER.index(e['type']) if e['type'] in ORDER else len(ORDER), e['floor'], e['id']))
    canon = {"project": "CR City Hotel - 415 Perry Street, Castle Rock CO 80104 (Meridian 105, Permit 4.22.2026)",
             "constants": {"plan_scale_by_sheet": escala},
             "walls": [], "existing_walls": ex, "ceilings": ceilings, "misc_items": misc, "ceilings_raw": ceil, "rfis_raw": rfis,
             "discarded_raw": desc}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(canon, open(OUT + '.base.json', 'w'), indent=1)
    import collections
    t = collections.defaultdict(float)
    for e in ex:
        t[(e['floor'], e['type_id'], e['board'])] += e['length_ft'] * e['height_ft'] * e['faces'] * e['layers']
    print(len(ex), 'existing_walls;', len(misc), 'misc;', len(ceil), 'ceilings;', len(rfis), 'rfis; floors', list(floors))
    tb = collections.defaultdict(float)
    for (f, ti, bd), v in t.items():
        tb[bd] += v
    print({k: round(v) for k, v in tb.items()})


if __name__ == '__main__':
    main()
