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
            tid = w.get('type_id'); typ = w.get('type')
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
                if k == '5/8 cement board' and not str(tid or '').endswith('-0'):
                    # rated face with tile: keep the rated Type X layers + add 1 layer CBU (RFI-CR-TILE)
                    g = grupos.setdefault(('5/8 type X WR', ly, round(h, 3)), {'faces': 0, 'src': [], 'rooms': []})
                    g['faces'] += 1; g['src'].append(fc.get('height_source') or ''); g['rooms'].append(fc.get('room') or '')
                    ly = 1
                g = grupos.setdefault((k, ly, round(h, 3)), {'faces': 0, 'src': [], 'rooms': []})
                g['faces'] += 1; g['src'].append(fc.get('height_source') or ''); g['rooms'].append(fc.get('room') or '')
            for n, ((k, ly, h), g) in enumerate(sorted(grupos.items())):
                eid = f"{w['id']}{'' if len(grupos) == 1 else ' ' + 'ABCDEFG'[n]}"
                ex.append({"id": eid, "type_id": tid, "type": typ, "floor": fl, "sheet": sh, "page": w.get('page'),
                           "path": path, "length_ft": round(L, 3), "height_ft": h, "faces": g['faces'], "layers": ly,
                           "board": k, "location": f"{fl} {w.get('location', '')} | faces: {'; '.join(r for r in g['rooms'] if r)}"[:300],
                           "source": f"{sh} ({w.get('length_source', '')}; {w.get('length_op', '')}) | H: {g['src'][0][:220]} | type: {w.get('type_source', '')} | detail: {w.get('detail', '')}"[:900],
                           "decision": DEC if w.get('framing') != 'metal' else "C-H shaft wall (A0.06 CH, UL U415): board / liner here, C-H studs + J-runner in misc_items",
                           "tag_ids": w.get('tag_ids') or [], "length_status": w.get('length_status'),
                           "img": w.get('img'), "height_img": w.get('height_img')})
            if w.get('framing') == 'metal' and str(typ or '').startswith('CH'):
                size = {'CH.2': '2-1/2"', 'CH.4': '4"', 'CH.6': '6"'}.get(typ, '6"')
                H = max([float(fc.get('height_ft') or 0) for fc in w.get('faces') or []] + [0])
                n_st = math.ceil(L / 2.0 - 1e-6) + 1
                misc.append({"ref": f"CH-STUD {w['id']}", "familia": f"C-H stud {size} (printed)", "lf": round(n_st * H, 2),
                             "op": f"ROUNDUP({L}/2.0)+1 = {n_st} studs x {H} ft = {round(n_st * H, 2)}",
                             "source": f"{sh} {w['id']}; A0.06 CH '{size} 20GA METAL C-H STUD' (UL U415); spacing 24 in. o.c. per UL U415 (not printed on A0.06)"})
                misc.append({"ref": f"J-RUNNER {w['id']}", "familia": f"J-runner {size} (printed)", "lf": round(2 * L, 2),
                             "op": f"2 x {L} (top + bottom 'J' RUNNER CHANNEL) = {round(2 * L, 2)}",
                             "source": f"{sh} {w['id']}; A0.06 CH '\"J\" RUNNER CHANNEL'"})
        for c in d.get('ceilings') or []:
            ceil.append(dict(c, floor=fl))
        rfis += [dict(r, floor=fl) for r in d.get('rfis') or []]
        desc += [dict(x, floor=fl) for x in d.get('discarded') or []]
    ex.sort(key=lambda e: (ORDER.index(e['type']) if e['type'] in ORDER else len(ORDER), e['floor'], e['id']))
    canon = {"project": "CR City Hotel - 415 Perry Street, Castle Rock CO 80104 (Meridian 105, Permit 4.22.2026)",
             "constants": {"plan_scale_by_sheet": escala},
             "walls": [], "existing_walls": ex, "misc_items": misc, "ceilings_raw": ceil, "rfis_raw": rfis,
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
