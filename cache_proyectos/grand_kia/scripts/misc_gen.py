import math
import re, os
"""Grand Kia - misc_items del canon (programa, op visible): cielos de gyp bd (A131 / A132 / A133), soffits / light coves /
bulkheads, control joints de cielo, demolición (SF), Level 5 (WC-1), trim. Entrada: 2_lectura/A/CEILINGS.json, DEMO.json y
el canon (walls para la altura de estructura por cuarto). Salida: lista misc_items + filas RCP (para markups) en
4_canon/misc_gen.json. Criterios (cada uno con su fuente):
  - Board de cielo: 5/8" gyp bd (12/A540, 14/A540, 25/A540, 8/A530, 9/A530); core no designado -> regular: ASTM C840
    Table 1 permite 5/8" regular perpendicular a framing @24" o.c. (U-162: plano y luego código; sin RFI).
  - SUSPENDED (secciones keynote 4 / 14, 24, 29/A540 'SUSPENDED GYP BD CEILING SYSTEM'): USG drywall suspension, main tee
    @48" o.c. (= hanger line, hangers 12 GA @48" o.c. ASTM C636), cross tee @16" o.c. para 5/8" (fabricante), angle
    molding al perímetro, hanger wire = hangers x caída a estructura.
  - FRAMED (secciones keynote 8 'FRAMED GYP BD CEILING'; 12/A540 'MTL. STUD FRAMING / METAL JOIST WHERE OCCURS'):
    3-5/8" studs como joists @16" o.c. sobre la luz corta + track en los dos extremos (tamaño no impreso: RFI-03).
  - Cuarto sin sección ni burbuja: el criterio de los cuartos iguales cortados por sección (consult / cashier / sales
    mgr <= 300 SF = FRAMED; lounge / delivery / service lounge > 300 SF = SUSPENDED) + RFI-04 con el delta.
  - '8-2 (EXISTING) PGB (NEW)': board directo al cordón inferior de los joists existentes (A300 keynote 26): solo board.
"""
import json, math, re, os
W = '/root/gk/work'
C = json.load(open(f'{W}/etapas/2_lectura/A/CEILINGS.json'))
canon = json.load(open(f'{W}/etapas/4_canon/takeoff_canon.json'))
ESC = 9.0
BOARD = '5/8" gyp board regular (walls + ceilings)'


def ft(h):
    m = re.match(r"\s*(\d+)'-(\d+)", str(h or ''))
    return round(int(m.group(1)) + int(m.group(2)) / 12, 3) if m else None


def perim(poly):
    return sum(math.dist(poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))) / ESC


def bbox(poly):
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    return (max(xs) - min(xs)) / ESC, (max(ys) - min(ys)) / ESC


def estructura(room, num):
    """altura de estructura del cuarto = máx height_ft de los walls full-height que lo tocan (lectura resuelta)."""
    hs = []
    for w in canon['walls']:
        if re.sub(r'1$', '', w.get('tag') or '') not in ('A', 'C', 'E'):
            continue
        for f in w.get('faces') or []:
            r = str(f.get('room') or '').upper()
            if (num and str(num) in r) or (room and room.split()[0].upper() in r):
                hs.append((float(f.get('height_ft') or w.get('height_ft') or 0), w['id']))
    return max(hs) if hs else (None, None)


misc, rcp, rfis_ceil = [], [], []
for x in C['ceilings']:
    if x['sheet'] == 'A130' or (x['sheet'] == 'A132' and str(x.get('number')) in ('140', '141', '142', '143')):
        continue   # A130 = vista general de los mismos cuartos; A132 140-143 duplican A131 (lector de cielos)
    room, num = x.get('room'), x.get('number')
    if str(num) in ('108', '109') and str(x.get('height', '')).startswith('PENDIENTE'):
        x = dict(x, height="10-0", height_source="consult row 102-113 shares the single '10-0 PGB P-7' tag (A131); RFI-14 closed at 10'-0\"")
    REFS_USED = globals().setdefault('REFS_USED', set())
    tag = f"{x['sheet']} {num or ''} {room}".strip()
    zonas = x.get('zones') or [{"name": room, "h": x.get('height'), "area_sf": x.get('area_sf'),
                                "area_op": x.get('area_op'), "polys": x.get('polys') or [x.get('poly')]}]
    fr = str(x.get('framing') or '')
    for zi, z in enumerate(zonas):
        a = z.get('area_sf')
        if a in (None, 0):
            rfis_ceil.append({"item": f"{tag} zone {z.get('name')}", "why": "zone area not measured by the ceilings reader"})
            continue
        h = ft(z.get('h') or x.get('height'))
        if room == 'LOUNGE' and 'ring' in str(z.get('name', '')).lower():
            h = 8.0   # RFI-08 closed: ring ceiling '8'-0" PGB P-7' tags inside the 17'-0" well (A131)
            z = dict(z, h="8'-0\" (ring tags '8'-0\" PGB P-7' inside the 17'-0\" well, A131; RFI-08 closed)")
            _o = json.load(open(f'{W}/revision_independiente/FIX_RCP/geom.json'))['polys']['CLG-A131-107-2']['outer']
            _cx = (min(q[0] for q in _o) + max(q[0] for q in _o)) / 2; _cy = (min(q[1] for q in _o) + max(q[1] for q in _o)) / 2
            A_, B_ = 76.5, 58.5      # printed 17'-0" well and 13'-0" cloud at 9 pt/ft (U-017: printed dims govern; drawn cloud 12'-8")
            z = dict(z, polys=[[[_cx - A_, _cy - A_], [_cx + A_, _cy - A_], [_cx + A_, _cy + A_], [_cx - A_, _cy + A_], [_cx - A_, _cy - B_],
                                [_cx - B_, _cy - B_], [_cx - B_, _cy + B_], [_cx + B_, _cy + B_], [_cx + B_, _cy - B_], [_cx - A_, _cy - B_]]])
        ref = f"CLG-{x['sheet']}-{num or re.sub(r'[^A-Z0-9]+', '', str(room).upper())[:12] or 'X'}{'-' + str(zi + 1) if len(zonas) > 1 else ''}"
        k_ = 2
        while ref in REFS_USED:     # two unnumbered rooms with the same printed name: suffix by order of reading
            ref = re.sub(r"-\d+$", "", ref) if k_ > 2 else ref; ref = f"{ref}-{k_}"; k_ += 1
        REFS_USED.add(ref)
        polys = z.get('polys') or [z.get('poly')]
        P = sum(perim(p) for p in polys if p)
        bw, bl = (bbox(polys[0]) if polys and polys[0] else (math.sqrt(a), math.sqrt(a)))
        corto, largo = min(bw, bl), max(bw, bl)
        src = f"{x['sheet']} {tag} [DERIVED] area {a} SF ({z.get('area_op') or x.get('area_op')}) | height {z.get('h') or x.get('height')} ({x.get('height_source')})"
        src = src.replace("PENDIENTE", "not tagged (see height)")
        if 'EXISTING floor joists' in fr or '8-2 (EXISTING)' in fr:
            sistema = 'existing joists'
        elif fr.startswith('SUSPENDED'):
            sistema = 'suspended'
        elif fr.startswith('FRAMED'):
            sistema = 'framed'
        else:
            sistema = 'framed' if a <= 300 else 'suspended'
            rfis_ceil.append({"item": tag, "area": a, "loaded": sistema})
        _rr = re.search(r"\b(MEN|WOMEN|RESTROOM|PRIVATE RR|RR|TOILET)\b", str(room).upper())
        misc.append({"ref": f"{ref} board", "familia": ('5/8" glass mat tile backer (Dens Shield)' if _rr else BOARD), "qty": round(a, 2), "op": f"{a} SF x 1 layer = {round(a, 2)}",
                     "source": src + (" (restroom: A211 GN 13 'ALL GYP. BD. IN RESTROOMS SHALL BE 5/8\" ... DENS SHIELD', 2/A001)" if _rr else "") + {"suspended": " (system 24/A540)", "framed": " (system 12/A540, 64/S204)"}.get(sistema, " (board on existing joists, 24/A540)"), "detail": x.get('detail') and ', '.join(x['detail']) if isinstance(x.get('detail'), list) else (x.get('detail') or '')})
        if sistema == 'suspended':
            hst, wid = estructura(room, num)
            drop = round(hst - h, 2) if hst and h and hst > h else None
            hangers = math.ceil(a / 16)
            misc += [
                {"ref": f"{ref} main tee", "familia": "USG drywall main tee (DGLW26)", "qty": round(a / 4.0, 2),
                 "op": f"{a} SF / 4.0 ft o.c. = {round(a / 4.0, 2)}",
                 "source": f"{tag}: USG drywall suspension, main tees 48 in. o.c. (24/A540 suspended gyp bd ceiling system; spacing per manufacturer / ASTM C636 hangers @48\")"},
                {"ref": f"{ref} cross tee", "familia": "USG drywall cross tee (DGLW424)", "qty": round(a / 1.333, 2),
                 "op": f"{a} SF / 1.333 ft o.c. = {round(a / 1.333, 2)}",
                 "source": f"{tag}: cross tees 16 in. o.c. for 5/8 in. board (manufacturer, 24/A540)"},
                {"ref": f"{ref} angle", "familia": "USG angle molding (DGWM24)", "qty": round(P, 2),
                 "op": f"perimeter of the measured room polygon on {x['sheet']} / 9 pt/ft = {round(P, 2)} LF",
                 "source": f"{tag}: wall angle at perimeter (24/A540)"}]
            if drop:
                misc.append({"ref": f"{ref} hangers", "familia": "hanger wire", "qty": round(hangers * drop, 2),
                             "op": f"ROUNDUP({a}/16) = {hangers} hangers x drop {drop} ft = {round(hangers * drop, 2)}",
                             "source": f"{tag}: 12 ga hanger wire @48\" x 48\" (ASTM C636 / 24/A540); drop = structure {hst} ft (wall {wid} height, sections A300/A301) - ceiling {h} ft"})
            else:
                rfis_ceil.append({"item": f"{tag} hanger drop", "why": "structure height above this room not found in the resolved walls"})
        elif sistema == 'framed':
            n = math.ceil(largo / 1.3333) + 1
            if corto <= 11.17:
                mem, fam, led = '362S162-33', '3-5/8" stud (todos los gauges)', '362T125-33'
            else:
                mem, fam, led = '600S162-33', '6" stud (todos los gauges)', '600T125-33'
            misc += [
                {"ref": f"{ref} joists", "familia": fam, "qty": round(n * corto, 2),
                 "op": f"ROUNDUP({round(largo, 2)}/1.3333)+1 = {n} joists x span {round(corto, 2)} ft = {round(n * corto, 2)}",
                 "source": f"{tag}: FRAMED GYP BD CEILING (section keynote 8; 12/A540 'METAL JOIST WHERE OCCURS - SEE STRUCT'); 64/S204 interior CFS ceiling joist schedule: {mem} @16\" o.c. (span {round(corto, 2)} ft <= {'11\'-2\"' if mem.startswith('362') else '16\'-6\"'}); room bbox {round(bw, 2)} x {round(bl, 2)} ft on {x['sheet']}"},
                {"ref": f"{ref} track", "familia": "track de ceilings / soffits", "qty": round(2 * largo, 2),
                 "op": f"2 lines x {round(largo, 2)} ft (ledger {led} at both bearing walls) = {round(2 * largo, 2)}",
                 "source": f"{tag}: 64/S204 ledger track {led} each end"},
                {"ref": f"{ref} bridging", "familia": '1-5/8" stud', "qty": round(largo, 2),
                 "op": f"1 row at mid-span x {round(largo, 2)} ft = {round(largo, 2)}",
                 "source": f"{tag}: 64/S204 note 5 'continuous flat 162S125-33 bridging at mid-span'"},
                {"ref": f"{ref} clips", "familia": "clip angle (bracing / nested connections)", "qty": 2 * n,
                 "op": f"2 per joist x {n} joists = {2 * n}",
                 "source": f"{tag}: 64/S204 note 6 '3x3x0'-3\" clip angle each joist end' (metal: loaded; screws excluded U-053)"}]
        rcp.append({"ref": ref, "sheet": x['sheet'], "page": x['page'], "room": room, "number": num, "area_sf": a,
                    "height": z.get('h') or x.get('height'), "system": sistema, "polys": polys, "board": '5/8" gyp bd regular'})

# braces de walls parciales (62/S204 view A 'BRACE AT TOP OF WALL' + 8/A540): ROUNDUP(L/4)+1 braces por wall, largo = gap / sin 45
for w in canon['walls']:
    bt = re.sub(r'1$', '', w.get('tag') or '')
    if bt not in ('B', 'D'):
        continue
    best = None
    for f in w.get('faces') or []:
        hs, wid = estructura(str(f.get('room') or '').split(' ')[0], re.sub(r'\D', '', str(f.get('room') or '')) or None)
        if hs and (best is None or hs > best[0]):
            best = (hs, wid)
    if not best:
        rfis_ceil.append({"item": f"{w['id']} brace", "why": "structure height above the partial wall not found"})
        continue
    gap = round(best[0] - float(w['height_ft']), 2)
    if gap <= 0:
        continue
    nb = math.ceil(float(w['length_ft']) / 4) + 1
    lb = round(gap / math.sin(math.radians(45)), 2)
    mem = '362S162-43 (62/S204 view A, H <= 6 ft)' if gap <= 6 else '600S162-43 (62/S204 view A, H <= 10 ft)' if gap <= 10 else \
        '600S162-54 (63/S204 BRACE SCHEDULE, L <= 16 ft)' if lb <= 16 else '600S162-68 (63/S204 BRACE SCHEDULE, L <= 22 ft)' 
    misc.append({"ref": f"BRACE {w['id']}", "familia": "metal stud brace to structure (printed)", "qty": round(nb * lb, 2),
                 "op": f"ROUNDUP({w['length_ft']}/4)+1 = {nb} braces x ({gap} ft / sin 45) {lb} ft = {round(nb * lb, 2)}",
                 "source": f"{w['sheet']} {w['id']}: brace at top of wall {mem} @48\" o.c. (gap {gap} ft), alternate directions, 45 deg; 8/A540 'DIA. BRACE @4'-0\" O.C.'; gap = structure {best[0]} ft (wall {best[1]}) - top of wall {w['height_ft']} ft"})

# RFI-23: break room 157 window F (A220 F 8'-0" wide, sill 3'-4", head 8'-0")
misc += [{"ref": "RI-18A furring board", "familia": BOARD, "qty": 3.9, "op": "3.33 LF x 1.17 ft over door 154 (4/A211 at 18 pt/ft: door head to the 9'-0\" ceiling line, RFI-07 value) = 3.9", "source": "4/A211 / A112: type F furring above door 154 (Women 154) (R-ALC-11, review item RI-18)", "detail": "F/A550 (type F furring), 4/A211"},
         {"ref": "RI-18B furring board", "familia": BOARD, "qty": 7.82, "op": "0.92 LF x 8.5 ft at the kn 6 roof-drain corner of Break Room 157 (ceiling 8'-0\" + 6\") = 7.82", "source": "A112: type F furring at the kn 6 roof-drain corner of Break Room 157 (R-ALC-11, review item RI-18)", "detail": "F/A550 (type F furring)"},
         {"ref": "RI-18 furring studs", "familia": '2-1/2" stud', "qty": 20.51, "op": "3 x 1.17 + 2 x 8.5 = 20.51", "source": "A112 / A150 type F 2-1/2\" furring (A550 F) above door 154 and at the kn 6 drain corner"}]
# grid 2.1 fascias above the consult boxes (A111 keynote 1 'FACE OF FASCIA/SOFFIT ABOVE', drawn on 1/A210 with keynote 3 control joints,
# A300 C-C keynote 11 metal stud framed wall above glass): loaded by estimator precedent (a fascia drawn in a detail is carried with its measured size)
for fid, lf_, y_, x0_, x1_ in (("FAS-Z1-01", 48.72, 889.3, 803.5, 1242.0), ("FAS-Z2-01", 48.59, 846.2, 1480.1, 1917.4)):
    n_ = math.ceil(lf_ / 1.3333) + 1
    misc += [{"ref": f"{fid} board", "familia": BOARD, "qty": round(lf_ * 11.0, 2), "op": f"{lf_} LF x 11.0 ft = {round(lf_ * 11.0, 2)} (showroom face from the 10'-0\" consult ceiling to the 21'-0\" showroom ceiling, A131)",
              "source": f"A111 keynote 1 fascia at grid 2.1 ({x1_}-{x0_})/9 = {lf_} LF; 1/A210 elevation 21'-0\" - 10'-0\" = 11.0; A300 C-C keynote 11 (estimator precedent (a fascia drawn in a detail is carried with its measured size))", "detail": "1/A210, A300, A111"},
             {"ref": f"{fid} studs", "familia": '3-5/8" stud (todos los gauges)', "qty": round(n_ * 11.0, 2), "op": f"ROUNDUP({lf_}/1.3333)+1 = {n_} studs x 11.0 ft = {round(n_ * 11.0, 2)}",
              "source": f"{fid}: 362S162-33 @16\" o.c. (62/S204 allowable interior wall height table: 15'-4\" >= 11.0 ft; member size not printed on A300 C-C keynote 11)", "detail": "62/S204"},
             {"ref": f"{fid} track", "familia": "track de ceilings / soffits", "qty": round(2 * lf_, 2), "op": f"2 x {lf_} = {round(2 * lf_, 2)}", "source": f"{fid}: top + bottom track (62/S204)", "detail": "62/S204"}]
misc += [{"ref": "WINF-157 window F furring board", "familia": BOARD, "qty": 26.67, "op": "8.0 x 3.33 below the sill = 26.67", "source": "A220 F (8'-0\" wide, sill 3'-4\") at Break Room 157: furring below the window sill to the floor", "detail": "F/A550 (type F furring)"},
         {"ref": "WINF-157 head furring board", "familia": BOARD, "qty": 4.0, "op": "8.0 LF x 0.5 ft above the head (head 8'-0\" to the furring top 8'-6\" = ceiling 8'-0\" + 6\") = 4.0", "source": "A220 F (8'-0\" wide, head 8'-0\") at Break Room 157; furring top 8.5 ft", "detail": "F/A550 (type F furring)"},
         {"ref": "WINF-157 window F cripples", "familia": '2-1/2" stud', "qty": 26.8, "op": "7 cripples x 3.83 ft = 26.8", "source": "A220 F; F type 2-1/2\" furring @16\" o.c. (A550)"},
         {"ref": "WINF-157 window F track", "familia": "bottom track (todos)", "qty": 16.0, "op": "sill + head track 2 x 8.0 = 16.0", "source": "A220 F"}]

# soffits / coves / bulkheads (lector de cielos), op visible
GEO = json.load(open(f'{W}/revision_independiente/FIX_RCP/geom.json'))      # vector re-measure of the review (U-168 A3)
for s in C['soffits']:
    g_ = GEO['lines'].get(s['id'])
    if g_ and abs(float(g_['lf_measured']) - float(s.get('lf') or 0)) > 0.05:
        s['lf_op'] = f"vector re-measure {g_['length_pt']} pt / 9 = {g_['lf_measured']} (reading {s.get('lf')}: {g_.get('note', '')[:120]})"
        s['lf'] = g_['lf_measured']
_h = GEO['polys_tech_parts']['pgb_lines'][0]
C['soffits'].append({"id": "SOF-18", "sheet": "A131", "page": 14, "kind": "gyp bd header (keynote 19)", "line": _h['lines'][0], "line2": _h['lines'][1],
                     "lf": _h['lf'], "lf_op": f"{_h['length_pt']} pt / 9 = {_h['lf']} (2 pieces, column between)", "drop_ft": 2.0,
                     "detail": ["A131 keynote 19"], "source": "A131 'PGB P-7' + keynote 19 'NEW HEADER HEIGHT TO MATCH EXISTING' at TECH PARTS 134 south line"})
for s in C['soffits']:
    if not s.get('lf'):
        continue
    lf, d = float(s['lf']), s.get('drop_ft')
    det = ', '.join(s.get('detail') or [])
    if s['id'] == 'SOF-01':
        faces_sf, desc = lf * 1.0, '1 angled face 1\'-0" (14/A540)'
    elif s['id'].startswith('SOF-0') and s['id'] in ('SOF-02', 'SOF-03', 'SOF-04', 'SOF-05', 'SOF-06', 'SOF-07'):
        faces_sf, desc = lf * 1.5, 'cove pocket 6" horiz + 6" vert + 6" return = 1.5 ft developed (23/A540)'
    elif s['id'] == 'SOF-08':
        faces_sf, desc = lf * 1.5, 'light-well pocket per 28/A540 = 1.5 ft developed (as 23/A540)'
    elif s['id'] in ('SOF-09', 'SOF-10'):
        faces_sf, desc = lf * (2 * 2.0 + 1.13), '2 faces 2\'-0" + bottom 1.13 ft'
    elif s['id'] == 'SOF-11':
        faces_sf, desc = lf * (2.0 + 1.89), 'north face 2\'-0" + bottom 1.89 ft'
    elif s['id'] == 'SOF-17':
        faces_sf, desc = lf * (2 * 1.0 + 0.67), '2 faces (height not printed: 1\'-0" loaded, RFI-05) + bottom 0.67 ft'
    elif s['id'] == 'SOF-12':
        faces_sf, desc = lf * 1.91, 'bottom 1.91 ft measured (A131); side faces not dimensioned: review item (15/A530 GYP. BD. SOFFIT)'
    elif s['id'] == 'SOF-18':
        faces_sf, desc = lf * (2 * 2.0 + 0.42), "2 faces 2'-0\" (depth not printed: 8/A530 fascia depth used, conservative; Review Item) + bottom 0.42 ft (5\" drawn)"
    elif s['id'] == 'SOF-14':
        faces_sf, desc = lf * 11.0, "1 fascia face 11'-0\" (showroom 21'-0\" ceiling to sales 10'-0\" ceiling, A131 tags; 12/A540 mtl stud + 5/8\" gyp bd)"
    elif s['id'] == 'SOF-15':
        d = round(13.97 - 10.0, 2)
        faces_sf, desc = lf * d, f"1 fascia face {d} ft = structure 13.97 ft at grid J (D-D/A301, U-176 height table F-Z1-11..17) - ceiling 10'-0\" (A131); 12/A540"
    else:
        continue      # SOF-13 vestibule box = vestibule walls (B-B/A300); SOF-16 = EXT-08 (8/A530, Delivery 115 door heads)
    misc.append({"ref": f"{s['id']} board", "familia": BOARD, "qty": round(faces_sf, 2),
                 "op": f"{lf} LF x developed {round(faces_sf / lf, 3)} ft = {round(faces_sf, 2)}",
                 "source": f"{s['sheet']} {s['id']} {s.get('kind')}: {desc}; {det or 'A131'} ({s.get('lf_op', '')})",
                 "detail": det or "12/A540 (framed gyp bd system; no soffit-specific detail printed for this element)"})
    n = math.ceil(lf / 1.3333) + 1
    misc.append({"ref": f"{s['id']} framing", "familia": '3-5/8" stud (todos los gauges)', "qty": round(n * max(float(d or 1.0), 1.0), 2),
                 "op": f"ROUNDUP({lf}/1.3333)+1 = {n} cripples x {max(float(d or 1.0), 1.0)} ft = {round(n * max(float(d or 1.0), 1.0), 2)}",
                 "source": f"{s['sheet']} {s['id']}: metal stud framing of the soffit / cove ({det or 'A131'}; 16\" o.c. per A550 keynotes)"})
    misc.append({"ref": f"{s['id']} track", "familia": "track de ceilings / soffits", "qty": round(2 * lf, 2),
                 "op": f"2 lines x {lf} LF = {round(2 * lf, 2)}", "source": f"{s['sheet']} {s['id']}: top + bottom track of the soffit framing ({det or 'A131'})"})

# control joints de cielo (24/A540)
for j in C.get('control_joints') or []:
    if j.get('lf'):
        misc.append({"ref": j['id'], "familia": "control joint", "qty": round(float(j['lf']), 2),
                     "op": f"{j.get('lf_op')} = {j['lf']}", "source": f"{j.get('sheet')} {j.get('location')}; {j.get('detail')}"})

# demolición: solo SF (U-143)
D = json.load(open(f'{W}/etapas/2_lectura/A/DEMO.json'))
import csv as _csv
_FH = f'{W}/alturas/FINAL/ALTURAS_IMPRESAS.csv'
HF = {r['Wall ID']: r for r in _csv.DictReader(open(_FH, encoding='utf-8-sig'))} if os.path.isfile(_FH) else {}
for d in D['demo_walls']:
    if d['id'] in HF:          # U-176 final height table (blind readings + directed resolution)
        r = HF[d['id']]
        d['height_ft'] = round(float(r['Printed H']), 3); d['height_source'] = f"{r['Source']} | op: {r['Operation']}"
    sf = round(float(d['length_ft']) * float(d['height_ft']), 2)
    misc.append({"ref": d['id'], "element": "demo", "familia": "demolition - gypsum board and metal framing",
                 "sheet": d.get('sheet'), "page": d.get('page'), "qty": round(float(sf), 2),
                 "op": f"{d['length_ft']} LF x {d['height_ft']} ft = {sf} SF",
                 "source": f"{d.get('sheet')} {d.get('keynote', '')}; height " + (", ".join(f"{a}/{ {'A': 'A300', 'B': 'A300', 'C': 'A300'}.get(a, 'A301')}" for a in dict.fromkeys(re.findall(r"\b([A-F])-\1\b", str(d.get('height_source') or '')))) or d.get('sheet')) + f" {str(d.get('h_source') or d.get('height_source') or '')[:150]}"})

json.dump({"misc_items": misc, "rcp_rows": rcp, "rfi_ceil": rfis_ceil}, open(f'{W}/etapas/4_canon/misc_gen.json', 'w'), indent=1)
import collections
t = collections.Counter()
for m in misc:
    t[m['familia']] += m['qty']
print({k: round(v, 1) for k, v in t.items()}, len(rcp), len(rfis_ceil))

# ------------------------------------------------------------------ exterior / CFS (lectura EXTERIOR.json, programa)
XP = f'{W}/etapas/2_lectura/A/EXTERIOR.json'
if os.path.exists(XP):
    X = {e['id']: e for e in json.load(open(XP))['elements']}
    def studs(L, oc=1.3333):
        return math.ceil(L / oc) + 1
    add = misc.append
    for eid in ('EXT-01', 'EXT-02', 'EXT-03'):
        e = X[eid]; L, H = float(e['length_ft']), float(e['height_ft']); n = studs(L)
        src = f"{e['sheet']} {eid} {e['location']}: {e['member']['stud']} ({e['member'].get('stud_source')}); H {H} ft ({e['height_source']}); L ({e['length_source']})"
        add({"ref": f"{eid} 10in studs", "familia": '10" stud (todos los gauges)', "qty": round(n * H, 2), "op": f"ROUNDUP({L}/1.3333)+1 = {n} studs x {H} ft = {round(n * H, 2)}", "source": src + " | 1000S162-43 = 43 mil (18 ga, S001 table)"})
        add({"ref": f"{eid} 6in studs", "familia": ('6" parapet stud' if e.get('element') == 'parapet' else '6" stud (todos los gauges)'), "qty": round(n * H, 2), "op": f"{n} (one 600S162-43 at each 10\" stud, A310 kn 11) x {H} ft = {round(n * H, 2)}", "source": src + " | 600S162-43 = 43 mil (18 ga)"})
        for fam, lines in (("bottom track (todos)", 2), ("top / deflection track (todos)", 2)):
            add({"ref": f"{eid} {fam.split()[0]} track", "familia": fam, "qty": round(L * lines, 2), "op": f"{lines} lines (10\" + 6\" stud rows) x {L} = {round(L * lines, 2)}", "source": f"{eid}: CFS track (S403 241 kn 8 / 242)"})
    for eid in ('EXT-02B', 'EXT-03B'):
        e = X[eid]; L = float(e['length_ft']); A = 46.81; havg = round(A / L, 3); n = studs(L)
        add({"ref": f"{eid} studs", "familia": '3-5/8" stud (todos los gauges)', "qty": round(n * havg, 2), "op": f"ROUNDUP({L}/1.3333)+1 = {n} studs x average height {havg} ft (triangle {A} SF / {L} ft) = {round(n * havg, 2)}", "source": f"{e['sheet']} {eid}: 3-5/8\" metal stud framing (A310 kn 33); gauge not printed (RFI-01); {e['height_source']}"})
        add({"ref": f"{eid} sheathing", "familia": '1/2" EXTERIOR gyp sheathing', "qty": A, "op": f"triangle {A} SF x 1 layer = {A}", "source": f"{eid}: 1/2\" glass mat gypsum sheathing ASTM C1177 (A310 kn 22; spec 061600 2.5.D) under EIFS"})
        add({"ref": f"{eid} board", "familia": BOARD, "qty": A, "op": f"triangle {A} SF x 1 layer = {A}", "source": f"{eid}: 5/8\" gyp board interior face (A310 kn 25)"})
    for eid, fam, mem in (('EXT-04', '6" stud (todos los gauges)', '600S162-43'), ('EXT-05', '3-5/8" stud (todos los gauges)', '362S162-43')):
        e = X[eid]; L, H = float(e['length_ft']), float(e['height_ft']); n = studs(L)
        add({"ref": f"{eid} studs", "familia": fam, "qty": round(n * H, 2), "op": f"ROUNDUP({L}/1.3333)+1 = {n} studs x {H} ft = {round(n * H, 2)}", "source": f"{e['sheet']} {eid} {e['location']}: {mem} @16\" o.c. (43 mil, {e['member']['stud']}); H ({e['height_source']}); {', '.join(e.get('detail') or [])}"})
        add({"ref": f"{eid} bottom track", "familia": "bottom track (todos)", "qty": L, "op": f"1 line x {L}", "source": f"{eid}: {e['member'].get('track')}"})
        add({"ref": f"{eid} top track", "familia": "top / deflection track (todos)", "qty": L, "op": f"1 line x {L}", "source": f"{eid}: {e['member'].get('track')}"})
        for s in e.get('sheathing') or []:
            if s.get('sf'):
                add({"ref": f"{eid} sheathing", "familia": '1/2" EXTERIOR gyp sheathing', "qty": float(s['sf']), "op": f"{s.get('sf_op')} = {s['sf']}", "source": f"{eid} {s['face']}: {s['type']}"})
    e = X['EXT-07']; L = 125.667; n = studs(L)
    add({"ref": "EXT-07 joists", "familia": '3-5/8" stud (todos los gauges)', "qty": round(n * 0.82, 2), "op": f"ROUNDUP({L}/1.3333)+1 = {n} joists x 0.82 ft = {round(n * 0.82, 2)}", "source": "EXT-07 grid 1 curtain-wall head pocket soffit: 362S162-33 CFS joist w/ 3 #10 to each stud (S403 241 kn 16); depth 0.82 ft (2/A310)"})
    add({"ref": "EXT-07 board", "familia": BOARD, "qty": round(L * 0.82, 2), "op": f"{L} LF x 0.82 ft = {round(L * 0.82, 2)}", "source": "EXT-07: suspended hard lid at the curtain-wall head (S403 241 kn 13; 2/A310)"})
    add({"ref": "EXT-07 track", "familia": "track de ceilings / soffits", "qty": round(2 * L, 2), "op": f"2 lines x {L} = {round(2 * L, 2)}", "source": "EXT-07: joist end tracks (S403 241)"})
    e = X['EXT-08']; L = 30.0; n = studs(L)
    add({"ref": "EXT-08 board", "familia": BOARD, "qty": 60.0, "op": "30.0 LF x 2.0 ft vertical face (8/A530 printed 2'-0\") = 60.0", "source": "EXT-08 Delivery 115 overhead doors 115B/C/D (A400 10'-0\" each): 8/A530 gyp bd bulkhead"})
    add({"ref": "EXT-08 framing", "familia": '3-5/8" stud (todos los gauges)', "qty": round(n * 2.0, 2), "op": f"ROUNDUP(30/1.3333)+1 = {n} cripples x 2.0 ft = {round(n * 2.0, 2)}", "source": "EXT-08: metal stud framing bulkhead (8/A530 'SEE STRUCT')"})
    add({"ref": "EXT-08 track", "familia": "track de ceilings / soffits", "qty": 60.0, "op": "2 lines x 30.0 = 60.0", "source": "EXT-08: bulkhead top / bottom track (8/A530)"})
    for wid in ('WR-01', 'WR-02', 'WR-03', 'WR-04'):
        e = X[wid]
        add({"ref": f"{wid} board", "familia": BOARD, "qty": round(float(e['lf_total']) * float(e['return_depth_ft']), 2), "op": f"{e['lf_total']} LF x {e['return_depth_ft']} ft return depth = {round(float(e['lf_total']) * float(e['return_depth_ft']), 2)} SF (returns {e['lf']}; depth {str(e.get('return_depth_op'))[:120]})", "source": f"{e.get('sheet', 'A111')} {wid} {e['location']}: 5/8\" gyp bd return over the furring to the window frame (26/A530 sill; head / jambs same condition)"})
    json.dump({"misc_items": misc, "rcp_rows": rcp, "rfi_ceil": rfis_ceil}, open(f'{W}/etapas/4_canon/misc_gen.json', 'w'), indent=1)
    print('exterior added', sum(1 for m in misc if m['ref'].startswith(('EXT', 'WR'))))
