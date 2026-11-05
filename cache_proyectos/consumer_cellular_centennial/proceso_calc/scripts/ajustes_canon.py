"""Input-format / rule fixes of the resolved canon demanded by the tools, each written into the element (_info):
 1. R70.1: restroom C-1 gyp ceiling - 2/A501 (grid suspension) is NOT bubbled on A200 / A402 (bubble sweep:
    A501 is referenced from no sheet) -> field system = furring (hangers + carrying + furring channel, ASTM C754)
    conservative, RFI-07 keeps 2/A501 grid as option A with its delta. Dimensions A402 enlarged plan 7'-8" x 7'-9".
 2. constants.carrying_direction: not printed -> N-S (RFI-07), the room is square (7'-8" x 7'-9", delta < 1 LF).
Use: python3 bitacora.py run scripts/ajustes_canon.py"""
import json
P = '/root/cc/work/etapas/4_canon/takeoff_canon.json'
c = json.load(open(P))
for ce in c['ceilings']:
    if ce['ref'] == 'C-1-RR':
        # rev2 (COORDINACION 5-nov, U-140 'sin burbuja no es no impreso'): 2/A501 INSTALLATION OF SUSPENDED CEILING USING GRID
        # SUSPENSION SYSTEM with 5/8" GYP. BD. is the only gypsum ceiling detail printed in the set and C-1 is the only gypsum
        # ceiling -> the plan governs (option A, estimator decision); delta vs the ASTM C754 furring of rev1 in RFI-06
        ce['system'] = 'usg_grid'
        ce['system_info'] = ("2/A501 grid-type suspension system (ICC ESR 1289), 12 GA. hanger wires max. 4'-0\" o.c., "
                             "2\" x 2\" sheet metal angle perimeter support; 5/8\" gyp bd")
        ce['system_source'] = ("2/A501 INSTALLATION OF SUSPENDED CEILING USING GRID SUSPENSION SYSTEM (5/8\" GYP. BD.); "
                               "A200 C-1 GYP BOARD CEILING at UNISEX RESTROOM H 8'-0\"")
        ce['system_callout'] = {"detail": "2/A501", "printed_only": True, "source": "A501",
                                "why": "2/A501 is the only gypsum board ceiling detail printed in the set (A501 CEILING DETAILS) "
                                       "and C-1 restroom is the only gypsum board ceiling (A200); not bubbled on A200 / A402"}
        ce['main_oc_in'] = {"value": 48, "source": "2/A501 '12 GA. MIN. HANGER WIRES ... MAX. 4'-0\" O.C.' (main tee at "
                                                   "the hanger line); USG drywall suspension system standard 4'-0\" o.c."}
        ce['cross_oc_in'] = {"value": 16, "source": "not printed on 2/A501: USG drywall suspension system standard cross "
                                                    "tee 16\" o.c. for 5/8\" gyp bd (estimator note)"}
        ce['moldings'] = {"value": ["angle"], "source": "2/A501 '2\" X 2\" SHEET METAL ANGLE' perimeter support"}
        ce['ns_ft'] = 7.667; ce['ew_ft'] = 7.75
        ce['dims_source'] = "A402 enlarged unisex restroom 7'-8\" x 7'-9\" (area per A100 vector polygon less the vanity notch)"
        ce['perimeter_ft'] = ce.get('perimeter_lf', 31.75)
        ce['detail'] = '2/A501'
        if '2/A501' not in ce.get('source', ''):
            ce['source'] = '2/A501; ' + ce.get('source', '1/A200, A402')
        ce.pop('detail_none_reason', None)
k = c.setdefault('constants', {})

json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
print('ok')
# 3. end caps of the two mop-sink stub walls (E3-12 / E3-13, free end in the Utility Room): the reading wrote
#    end_cap_sf (not in the schema) -> face side END (PROTOCOLO R72.6) with length = end cap / face height.
c = json.load(open(P))
for w in c['walls']:
    if 'end_cap_sf' in w:
        sf = w.pop('end_cap_sf'); h = w['height_ft']
        w['end_cap_sf_info'] = sf
        if not any(f.get('side') == 'END' for f in w['faces']):
            base = w['faces'][0]
            w['faces'].append({"side": "END", "layers": 1, "board": base['board'], "height_ft": h,
                               "height_source": base['height_source'], "room": base['room'],
                               "length_ft": round(sf / h, 3), "length_source": f"free end of the stub wall (A100 / 1/A504): {sf} SF / {h} ft"})
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
print('end caps ok')
# 4. blocking items (no LF typed by judgment: printed dims or the estimator standing rule R-ALC-02 / U-064):
c = json.load(open(P))
c['wood_excluded'] = {"why": "wood blocking / FRT plywood is Div. 06, never carried (estimator standing order, user decision 5-nov)",
                      "source": "1/A501 (FRT plywood at pendants), 6/A500 (2X4 blocking)"}
NB = []
for b in c['blocking_items']:
    r = b['ref']
    if r == 'BLK-PENDANT':
        b['material'] = 'FRT'; b['lf'] = 8.0
        b['lf_info'] = "8 EA pendant blocking (A200 L-2B x2, L-3A, L-3B, L-3C, L-4 x3) x 1 LF each, computed before the wood exclusion"
    elif r == 'BLK-WOOD-6A500':
        b['material'] = 'wood'; b['lf'] = 0.0
        b['lf_info'] = "2X4 blocking between joists only where the structure runs parallel to the partition (6/A500): wood, EXCLUDED"
    elif r == 'BLK-IPAD':
        b['material'] = 'metal'; b['lf'] = 9.0; b['status'] = 'DERIVADO'
        b['op'] = "(4'-0\" printed 2/A400 + 6\") x 2 rows (rows not printed: estimator standing rule, accessory blocking = 2 rows)"
    elif r == 'BLK-KITCH':
        b['material'] = 'metal'; b['lf'] = 11.33; b['status'] = 'DERIVADO'
        b['op'] = "(5'-2\" A103 key 8 + 6\") x 2 rows (3/A104: one row 3\" above the top and one 3\" below the bottom of the cabinet)"
    elif r == 'BLK-GRAB':
        b['material'] = 'metal'; b['lf'] = 8.0; b['status'] = 'DERIVADO'
        b['op'] = "rear 3'-0\" + vertical 1'-6\" (1/A402 printed) + side 3'-6\" MIN. (2/A402 printed) = 8.0 LF of 20 GA track (5/A402)"
        b['label'] = "grab bar backing: 20 GA. TRACK SECURED TO STUDS (5/A402)"
    elif r == 'BLK-RR-ACC':
        b['material'] = 'metal'; b['lf'] = 36.0; b['status'] = 'DERIVADO'
        b['op'] = ("6 wall-mounted items x 3 ft x 2 rows (estimator standing rule: accessory blocking without printed size = "
                   "3 ft x 2 rows): A402 keys 1 seat cover, 3 hand dryer, 4 toilet tissue, 6 soap, 7 mirror + wall-mounted lavatory")
        b['label'] = "PROVIDE BLOCKING AT ALL WALL MOUNTED FIXTURES AND ACCESSORIES (A402 general note 4)"
    else:
        b['material'] = 'metal'
    NB.append(b)
c['blocking_items'] = NB
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
print('blocking ok')
# 5. wall source (N/SHEET) = tag on the plan + type detail
c = json.load(open(P))
for w in c['walls']:
    if not w.get('source'):
        w['source'] = f"{w['tag']}/A500 (1/A500 partition types) on A100"
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 6. door / cased-opening heads: 2/A600 TYPICAL HEAD DETAIL draws the runner-track head over the HM knockdown frame
c = json.load(open(P))
for w in c['walls']:
    for o in w.get('openings') or []:
        o['header'] = 'metal'; o['pieces'] = 1
        o['pieces_source'] = ("2/A600 TYPICAL HEAD DETAIL (track head over the HM knockdown frame, 2\" min. to ceiling); one piece "
                              "R.O. + 1'-4\" (estimator standing criterion)") if o['kind'] == 'door' else \
                             "2/A400 cased opening T.O. OPENING 8'-0\": one runner-track head, R.O. + 1'-4\" (same criterion as 2/A600)"
        o['head_ft'] = 7.167 if o['kind'] == 'door' else o['head_ft']
        o['head_source'] = "A600 7'-0\" door + 2\" HM frame head (2/A600)" if o['kind'] == 'door' else "2/A400 T.O. OPENING 8'-0\""
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 7. sources (N/SHEET) on ceilings / misc / trim / blocking / openings_extra where the reading wrote area_source only
c = json.load(open(P))
for ce in c['ceilings']:
    ce['source'] = "1/A200, A402"; ce['source_info'] = "1/A200 REFLECTED CEILING PLAN, restroom ceiling tag C-1 H 8'-0\"; A402 enlarged restroom" 
for k in ('misc_items', 'trim_items', 'blocking_items', 'openings_extra', 'plywood_strips'):
    for it in c.get(k) or []:
        if not it.get('source'):
            it['source'] = 'A100'
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 8. no structural sheets in the set (G000 drawing index: G / D / A / M / E / P / FA only)
c = json.load(open(P))
c["opening_schedule"]["sources"] = sorted(set(c["opening_schedule"]["sources"]) | {"M101", "P101", "E101"}); c["opening_schedule"]["sources_none"] = {"S": "no structural (S) sheet in the set: G000 DRAWING INDEX lists G000-G003, D100-D101, A100-A700, M101-M601, E101-E701, P101-P501, FA101 only"}
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 9. opening refs = door schedule refs; existing doors in 'none' with their reason; cased opening listed once (in C3-02)
c = json.load(open(P))
for w in c['walls']:
    for o in w.get('openings') or []:
        if o['kind'] == 'door' and not o['ref'].startswith('Door'):
            o['ref'] = 'Door ' + o['ref']
        if o['kind'] == 'cased_opening':
            o['ref'] = 'CASED-OPEN-HALL'
c['openings_extra'] = [x for x in c.get('openings_extra') or [] if x['ref'] != 'CASED-OPEN-HALL']
sch = c['opening_schedule']
if not any(i['ref'] == 'CASED-OPEN-HALL' for i in sch['items']):
    sch['items'].append({"ref": "CASED-OPEN-HALL", "kind": "cased_opening", "source": "A100 4'-0\"; 2/A400 OPEN TO HALLWAY, T.O. OPENING 8'-0\""})
sch['none'] = [
 {"ref": "Door 1A", "why": "existing exterior main entry in the existing storefront (A600 door 1A (E), A100 'EXISTING DOUBLE ENTRY DOOR'): no new framing"},
 {"ref": "Door 2B", "why": "existing exterior hallway door (A600 door 2B (E)): no new framing"},
 {"ref": "Door 3C", "why": "new door in the EXISTING hallway / utility wall to remain (D100 keynote 17): opening in an existing wall, no new partition framing in our scope (RFI-08 keeps the alternative)"}]
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 10. nodes (studs_nodos: each wall end in exactly one node) generated from the A100 vector bands of the resolved walls:
#     end inside another wall's band -> T (branch = this wall); end meeting another wall's end: collinear same
#     stud/oc -> split, else L; end with no new wall -> free (against existing construction / free end)
c = json.load(open(P))
TOL = 9.0
def ends(w):
    b = w['band']; m = (b['c0'] + b['c1']) / 2
    return [((b['lo'], m) if b['ori'] == 'H' else (m, b['lo'])), ((b['hi'], m) if b['ori'] == 'H' else (m, b['hi']))]
def inside(p, w, tol=TOL):
    b = w['band']; x, y = p
    if b['ori'] == 'H':
        return b['lo'] - tol <= x <= b['hi'] + tol and b['c0'] - tol <= y <= b['c1'] + tol
    return b['lo'] - tol <= y <= b['hi'] + tol and b['c0'] - tol <= x <= b['c1'] + tol
def near_end(p, w):
    return any(abs(p[0] - q[0]) <= TOL and abs(p[1] - q[1]) <= TOL for q in ends(w))
WS = [w for w in c['walls'] if w.get('band')]
nodes, used = [], set()
n = 0
for w in WS:
    for i, p in enumerate(ends(w)):
        key = (w['id'], i)
        if key in used: continue
        others = [o for o in WS if o['id'] != w['id'] and inside(p, o)]
        endm = [o for o in others if near_end(p, o)]
        thru = [o for o in others if not near_end(p, o)]
        n += 1; nid = f"N{n}"
        if thru:
            nodes.append({"id": nid, "kind": "T", "branch": w['id'], "through": thru[0]['id'], "source": "A100 vector bands (resolved canon)"})
            used.add(key); continue
        free_end = [o for o in endm if not any(u[0] == o['id'] for u in used if near_end(p, o) and ends(o)[u[1]] and abs(ends(o)[u[1]][0]-p[0])<=TOL and abs(ends(o)[u[1]][1]-p[1])<=TOL)]
        if free_end:
            o = free_end[0]
            j = 0 if abs(ends(o)[0][0]-p[0]) <= TOL and abs(ends(o)[0][1]-p[1]) <= TOL else 1
            same = o['band']['ori'] == w['band']['ori'] and o.get('stud_size') == w.get('stud_size') and o.get('oc_in') == w.get('oc_in')
            nodes.append({"id": nid, "kind": "split" if same else "L", "walls": [w['id'], o['id']], "source": "A100 vector bands (resolved canon)"})
            used.add(key); used.add((o['id'], j))
            # any third wall ending here = T branch through w
            for o2 in endm[1:]:
                j2 = 0 if abs(ends(o2)[0][0]-p[0]) <= TOL and abs(ends(o2)[0][1]-p[1]) <= TOL else 1
                if (o2['id'], j2) not in used:
                    n += 1; nodes.append({"id": f"N{n}", "kind": "T", "branch": o2['id'], "through": w['id'], "source": "A100 vector bands (resolved canon)"})
                    used.add((o2['id'], j2))
            continue
        nodes.append({"id": nid, "kind": "free", "wall": w['id'], "source": "A100: end against existing construction / free end"})
        used.add(key)
c['nodes_info'] = "nodes generated by scripts/ajustes_canon.py step 10 from the A100 bands; reading A nodes replaced (walls re-cut by the resolution)"
c['nodes'] = nodes
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
print('nodes', len(nodes), {k: sum(1 for x in nodes if x['kind'] == k) for k in ('T', 'L', 'split', 'free')})
# 11. wall detail = the type key N/SHEET (A3/A500 ...) declared in details; full text kept in detail_info.
#     A600: 2/A600 = TYPICAL HEAD DETAIL, 3/A600 = TYPICAL JAMB DETAIL (eye-verified titles, burbujas_verificadas.json)
c = json.load(open(P))
TT = {"A3": "type A# FURRED WALL TO DECK", "C3": "type C# WALL TO DECK WITH GYPSUM BOARD ON BOTH SIDES",
      "D": "type D WALL WITH GYPSUM BOARD ON BOTH SIDES (6\" studs, batt, to deck)", "E3": "type E# WALL WITH GYPSUM BOARD ON BOTH SIDES (to 6\" above ceiling)"}
for w in c['walls']:
    k = f"{w['tag']}/A500"
    if w['detail'] != k:
        w['detail_info'] = w['detail']; w['detail'] = k
    c['details'].setdefault(k, {"source": "1/A500", "title": f"1/A500 partition types - {TT[w['tag']]}", "notes": "fichas.json (independent reader) + LECTURA_A_notas.md"})
c['details']['2/A600'] = {"source": "2/A600", "title": "TYPICAL HEAD DETAIL", "notes": "HM knockdown frame head, 2\" min. to finished ceiling; runner-track head over the opening"}
c['details']['3/A600'] = {"source": "3/A600", "title": "TYPICAL JAMB DETAIL", "notes": "HM knockdown frame, double studs at jambs, 3 jamb anchors per jamb"}
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 12. layers_per_face of each type (1/A500: one layer 5/8" per face on every type)
c = json.load(open(P))
for k in ('A3/A500', 'C3/A500', 'D/A500', 'E3/A500'):
    c['details'][k]['layers_per_face'] = 1
    c['details'][k]['layers_source'] = "1/A500 (5/8\" TYPE \"X\" GYP. BD. - one layer per face)"
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 13. board family names (board_caras families): 5/8" Type X -> '5/8 type X'; water resistant faces (A100 general note 11,
#     1/A500 'PROVIDE WATER RESISTANT GYP. BD. AT WET LOCATIONS') -> '5/8 type X WR'; ceiling C-1 restroom -> '5/8 type X WR'
import re as _re
c = json.load(open(P))
def fam(b):
    s = str(b)
    wr = bool(_re.search(r'water|WR|green|moist', s, _re.I))
    return '5/8 type X WR' if wr else '5/8 type X'
for w in c['walls']:
    for f in w['faces']:
        if f['board'] not in ('5/8 type X', '5/8 type X WR'):
            f['board_info'] = f['board']; f['board'] = fam(f['board'])
for ce in c['ceilings']:
    if ce['board'] not in ('5/8 type X', '5/8 type X WR', '5/8 ceiling sag-resistant'):
        ce['board_info'] = ce['board']; ce['board'] = '5/8 type X WR'
for k in ('A3/A500', 'C3/A500', 'D/A500', 'E3/A500'):
    c['details'][k]['sealant_none_reason'] = "Acoustical sealant (2/A500 'at all acoustical partitions') EXCLUDED in all projects (estimator standing order)"
    c['details'][k]['sealant_source'] = "2/A500"
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 14. bracing_rows source in N/SHEET form
c = json.load(open(P))
for w in c['walls']:
    if 'bracing_rows' in w and not str(w.get('bracing_rows_source')).startswith('1/A500, 4'):
        w['bracing_rows_source_info'] = w.get('bracing_rows_source')
        w['bracing_rows_source'] = "1/A500, 4/A500"; w["bracing_rows_info"] = "no stud bridging / C.R. channel row drawn or noted in 1/A500 - 6/A500"
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 15. every 'source' field in N/SHEET form (tools' RX_SRC): the readings' prose goes to source_info, the source keeps
#     the N/SHEET / sheet tokens of that prose in order (nothing invented: tokens are taken from the text itself)
RX_SRC = _re.compile(r"^([A-Za-z0-9.]{1,6}/)*[A-Z]{1,3}-?\d[\w.\-]*$")
RX_TOK = _re.compile(r"\b(?:[0-9A-Z]{1,3}/)?(?:G|D|A|M|E|P|FA)\d{3}\b")
c = json.load(open(P))
def ok(s):
    return all(RX_SRC.match((p.split() or [''])[0]) for p in _re.split(r"\s*[,;·]\s*", s.strip()))
def fix(o):
    if isinstance(o, dict):
        for k, v in list(o.items()):
            if k == 'source' and isinstance(v, str) and v.strip() and not ok(v):
                toks = list(dict.fromkeys(RX_TOK.findall(v)))
                if toks:
                    o['source_info'] = v; o['source'] = ', '.join(toks)
            else:
                fix(v)
    elif isinstance(o, list):
        for x in o: fix(x)
fix(c)
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 16. cased opening kind = 'opening' (tool list)
c = json.load(open(P))
for w in c['walls']:
    for o in w.get('openings') or []:
        if o['kind'] == 'cased_opening': o['kind'] = 'opening'; o['kind_info'] = 'cased opening (2/A400), no door / frame'
for i in c['opening_schedule']['items']:
    if i.get('kind') == 'cased_opening': i['kind'] = 'opening'
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 17. header_type printed on the head detail
c = json.load(open(P))
for w in c['walls']:
    for o in w.get('openings') or []:
        o['header_type'] = 'TRACK HEADER'; o['piece'] = 'track'
        o['header_type_source'] = '2/A600' if o['kind'] == 'door' else '2/A400'
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 18. pieces_source as N/SHEET, prose to pieces_info
c = json.load(open(P))
for w in c['walls']:
    for o in w.get('openings') or []:
        o['pieces_info'] = o['pieces_source']; o['pieces_source'] = o['header_type_source']
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 19. restroom ceiling hanger drop = B.O. deck of the back-of-house zone (A100 'PLY DECK @ 16'-4"') - ceiling 8'-0" (A200)
c = json.load(open(P))
for ce in c['ceilings']:
    if ce['ref'] == 'C-1-RR':
        ce['hanger_drop_ft'] = {"value": 8.333, "source": "A100, A200", "op": "16'-4\" (A100 BACK OF HOUSE PLY DECK) - 8'-0\" (A200 restroom H) = 8'-4\""}
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 20. misc_items rebuilt by program on the RESOLVED walls (the reading's brace / header / jamb rows were cut on its own walls):
#   - 3/A500 braces (type E only): positions n = ceil(L / 4 ft) + 1 (362S137-33 @ 48" o.c.); members per position 2 when the wall
#     is over 10'-0" ("FOR WALLS TO 15'-0" - BRACE WITH DOUBLED 362S137-33"), else 1; member = (B.O. deck of the zone - top of wall) x 1.414 (45 deg)
#   - 3x3x3 20 ga angle: one per brace member (3/A500 "3" X 3" X 3" ANGLE ... FASTENED TO TRACK AND BRACE")
#   - headers / jamb studs: computed by headers.py / studs_nodos.py from the wall openings (no misc row: no double count)
#   - insulation (1/A500 batt) and acoustical sealant (2/A500): EXCLUDED, not our trade / standing order (Scope Checklist)
#   - restroom ceiling 2x2 angle: carried by canon.py usg_grid moldings (2/A501, step 1)
#   - demolition: SF only (L x H); H = printed B.O. structure (A100 'PLY DECK @ 17'-1 9/16"', higher bay: the deck break is not
#     drawn) per the estimator standing rule (existing partitions to demolish without printed height = B.O. structure);
#     existing ceilings 'GYP. BD. & ACT ... THROUGHOUT' (D100 key 7) without the extent of each type = EXCLUDED for lack of information
import math as _m
c = json.load(open(P))
DECK = 16.333
keep, out = [], []
for m in c['misc_items']:
    r = m['ref']
    if r.startswith(('BRACE-', 'JAMB-', 'HDR-', 'INSUL-', 'SEAL-', 'CEIL-C1-ANGLE')):
        continue
    if r.startswith('DEMO-'):
        if r == 'DEMO-07':
            continue
        m['familia'] = 'demolition - gypsum board and metal framing'
        m['height_status'] = 'DERIVADO'
        m['height_source'] = ("A100 'PLY DECK @ 17'-1 9/16\"' (printed B.O. structure; the deck break is not drawn: higher bay) - "
                              "estimator standing rule: existing partitions to demolish without printed height go to the printed B.O. structure")
        m['op'] = f"{m['lf']} LF x {m['height_ft']} ft = {round(m['lf'] * m['height_ft'], 2)} SF (one wall area, no layers)"
        m['qty'] = round(m['lf'] * m['height_ft'], 2)
        m['status'] = 'DERIVADO'
    keep.append(m)
nb = 0
for w in c['walls']:
    if w['tag'] != 'E3':
        continue
    n = _m.ceil(w['length_ft'] / 4.0 - 1e-9) + 1
    mem = 2 if w['height_ft'] > 10.0 else 1
    ln = round((DECK - w['height_ft']) * 1.414, 3)
    q = round(n * mem * ln, 2)
    nb += n * mem
    keep.append({"ref": f"BRACE-{w['id']}", "familia": "metal stud brace to structure (printed)", "qty": q, "unit": "LF", "pcs": n * mem,
                 "source": "3/A500", "label": "362S137-33 brace @ 48\" o.c. max., 45 deg to structure (3/A500)" + (" DOUBLED (walls to 15'-0\")" if mem == 2 else ""),
                 "op": f"n = ceil({w['length_ft']} / 4) + 1 = {n} x {mem} member(s) x ({DECK} B.O. deck A100 - {w['height_ft']} top) x 1.414 = {q}",
                 "status": "DERIVADO", "wall": w['id']})
keep.append({"ref": "BRACE-ANGLES", "familia": "clip angle (bracing / nested connections)", "qty": nb, "unit": "EA", "source": "3/A500",
             "label": "3\" X 3\" X 3\" ANGLE (20 GA. MIN.), FASTENED TO TRACK AND BRACE (3/A500)", "op": f"one per brace member = {nb}", "status": "DERIVADO"})
c['misc_items'] = keep
c['demo_ceiling_excluded'] = {"why": "D100 key 7 'REMOVE EXISTING GYP. BD. & ACT CEILINGS ... THROUGHOUT': the extent of the gypsum board vs ACT existing ceiling is not shown - EXCLUDED for lack of information (estimator standing rule)", "source": "D100"}
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
print('misc', len(keep), 'brace members', nb)
# 21. accesorios_none with the accesorios.py family names
c = json.load(open(P))
an = []
for r in c.get('accesorios_none') or []:
    if r['familia'] == 'access panels': r['familia'] = 'access panel'
    if r['familia'] == 'control joints':
        c['control_joints_none'] = r; continue
    an.append(r)
if not any(r['familia'] == 'deflection clips' for r in an):
    an.append({"familia": "deflection clips", "why": "4/A500 / 5/A500 draw a long-leg slotted runner track with a floating C channel (no deflection clip)", "source": "4/A500, 5/A500"})
c['accesorios_none'] = an
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 22. R73.10: collinear type change C3 -> E3 at the south jamb of the cased opening (no drawn node) = RFI-06
c = json.load(open(P))
for w in c['walls']:
    if w['id'] == 'C3-01':
        w['type_change_rfi'] = {"alternativas": ["C3 to deck over the 4'-0\" cased opening (loaded, conservative)",
                                                 "E3 to 6\" above ceiling over the opening (cut at the C3 tag end)"],
                                "delta_lf": 4.0, "source": "A100", "rfi": "RFI-06"}
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 23. accessories closed with what the set answers; MEP registration result of THIS run (mep.py M101 p25 / P101 p35 vs A100 p7: None)
import os as _os, pymupdf as _f
c = json.load(open(P))
an = c['accesorios_none']
def add(f, why, src):
    if not any(r['familia'] == f for r in an): an.append({"familia": f, "why": why, "source": src})
add('extra framing ATM', "no ATM / recessed equipment in the set (A100, A103, A400, A401)", "A100")
add('Level 5 finish', "no Level 5 printed: A700 finish schedule PT-1..PT-4 eggshell paint, no wallcovering / Level 5 note", "A700")
add('PVC trim at FRP', "FRP B-3 (A700, A402 T.O. FRP 4'-0\") is a finish product, not metal framing / gypsum board: EXCLUDED with the FRP", "A700, A402")
add('stud reinforcement MEP', "no pipe / conduit crossing a stud wall larger than the stud web punch-out drawn on P101 / P501 / E101 (plumbing in the restroom wet walls runs inside the stud cavity); ducts EXCLUDED by standing order", "P101, P501, E101")
for w in c['walls']:
    for o in w.get('openings') or []:
        if o['ref'] == 'CASED-OPEN-HALL':
            o['jamb_return'] = True; o['jamb_return_source'] = '2/A400'
            o['jamb_return_info'] = "cased opening 'OPEN TO HALLWAY' without frame: gypsum board returns at both jambs and the head (2/A400)"
sw = c['mep_sweep']
img = '/root/cc/work/etapas/4_canon/img_runner/sheet_M101.png'
_os.makedirs(_os.path.dirname(img), exist_ok=True)
if not _os.path.exists(img):
    _f.open('/root/cc/work/plans/bidset_SIN_MARKUPS.pdf')[24].get_pixmap(dpi=40).save(img)
sw['source'] = 'M101, M102, M501, P101, P501, E101, E111, FA101'
sw['registro'] = {"no_usable": {"motivo": "mep.py registration of M101 (p.25) and P101 (p.35) against A100 (p.7) returned None in this run (< 25 matching wall segments: the M / P sheets carry the architectural background at another lineweight); ducts / air devices EXCLUDED by estimator standing order and no pipe crossing larger than the stud punch-out is drawn, so no quantity depends on the crossing", "source": "M101, P101, A100", "img": img}}
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 24. R75.3: no printed jamb-return label at the cased opening (2/A400 prints only 'OPEN TO HALLWAY' / T.O. OPENING 8'-0")
c = json.load(open(P))
for w in c['walls']:
    for o in w.get('openings') or []:
        for k in ('jamb_return', 'jamb_return_source'):
            o.pop(k, None)
an = c['accesorios_none']
if not any(r['familia'] == 'gypsum board jamb return' for r in an):
    an.append({"familia": "gypsum board jamb return", "why": "no jamb-return label printed: 2/A400 cased opening prints only 'OPEN TO HALLWAY' / 'T.O. OPENING 8'-0\"'; HM knockdown frames at doors 4C-6C (2/A600, 3/A600) have no return; the cased opening edges carry corner bead (trim row)", "source": "2/A400, 2/A600, 3/A600"})
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 25. stud_size label with hyphen (canon.py family parser reads '3 5/8"' as 8"): '3 5/8"' -> '3-5/8"'
c = json.load(open(P))
for w in c['walls']:
    s = str(w.get('stud_size'))
    if _re.match(r'^\s*3\s+5/8', s):
        w['stud_size_info'] = s; w['stud_size'] = '3-5/8"'
    elif _re.match(r'^\s*6"', s):
        w['stud_size'] = '6"'
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 26. two track families (U-056): E3 to 6" above ceiling = standard top track (3/A500 '20 GA. MIN. TRACK', studs cut 1/2"
#     short); A3 / C3 / D to deck = long-leg slotted runner track (4/A500 'LONG LEG RUNNER TRACK W/ 2" MIN. VERT. SLOTTED HOLES')
c = json.load(open(P))
for w in c['walls']:
    if w['tag'] == 'E3':
        w['top_track_kind'] = 'standard'; w['top_track_kind_source'] = "3/A500 - 20 GA. MIN. TRACK (PER ES REPORT ESR-1042), METAL STUDS CUT 1/2\" SHORT FOR 1/2\" DEFLECTION"
    else:
        w['top_track_kind'] = 'slip'; w['top_track_kind_source'] = "4/A500 - LONG LEG RUNNER TRACK W/ 2\" MIN. VERT. SLOTTED HOLES ATTACHED TO STRUCTURE (+ 3 5/8\" X 20 GA. 'C' CHANNEL TRACK FLOATING 1\" BELOW TOP CORD)"
c['fasteners_excluded'] = {"why": "all screws / anchors / shot pins excluded (estimator standing order)", "source": "2/A500, 3/A500, 4/A500"}
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 27. U-127 BOTH SIDES: type A# note '5/8" TYPE "X" GYP. BD. ON EACH SIDE TO 6" ABOVE CEILING' (1/A500) -> second face on
#     every A3 wall (back face toward the existing demising / exterior wall), same height as the tenant face; RFI-02 option B
c = json.load(open(P))
for w in c['walls']:
    if w['tag'] == 'A3' and len([f for f in w['faces'] if f['side'] in ('A', 'B')]) == 1:
        f0 = [f for f in w['faces'] if f['side'] in ('A', 'B')][0]
        w['faces'].append({"side": 'A' if f0['side'] == 'B' else 'B', "layers": 1, "board": f0['board'], "height_ft": f0['height_ft'],
                           "height_source": f0['height_source'] + " (back face: 1/A500 type A# '5/8\" TYPE \"X\" GYP. BD. ON EACH SIDE TO 6\" ABOVE CEILING', RFI-02)",
                           "room": "back face toward the existing demising / exterior wall (1/2\" gap, 1/A500)"})
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 28. blocking wall = the wall id the item is fixed to (first wall id in the reading's text); items on a ceiling -> 'ceiling'
c = json.load(open(P))
ids = [w['id'] for w in c['walls']]
WALLOF = {"BLK-GRAB": "E3-03", "BLK-RR-ACC": "E3-03", "BLK-PENDANT": "ceiling", "BLK-WOOD-6A500": "ceiling"}
for b in c['blocking_items']:
    t = str(b.get('wall') or '')
    m = [i for i in ids if i in t]
    b['wall_info'] = t or None
    b['wall'] = m[0] if m else WALLOF.get(b['ref'], 'ceiling')
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 29. schedule order of the types (1/A500 left to right: A#, C#, D, E#, H; H not used on A100)
c = json.load(open(P))
c['partition_schedule'] = [{"type": t, "source": "1/A500"} for t in ("A3", "C3", "D", "E3")]
c['constants']['type_order'] = {"value": ["A3", "C3", "D", "E3"], "source": "1/A500 (A#, C#, D, E#, H left to right; H not tagged on A100)"}
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 30. evidence fields the rules ask per element (texts only, from the readings' own sources):
#   - every detail: sealant_none_reason (acoustical sealant EXCLUDED, standing order); detail keys in N/SHEET form
#   - 'same as <wall>' / 'as <wall>' length / height sources -> the text of that wall
#   - length_basis (face to face) and the dimension-string tick type of A100 (single slash ticks) in length_op
c = json.load(open(P))
if '1-4/A104' in c['details']:
    d = c['details'].pop('1-4/A104')
    for n in ('1', '2', '3', '4'):
        c['details'][f'{n}/A104'] = dict(d, source=f'{n}/A104')
for k, d in c['details'].items():
    d.setdefault('sealant_none_reason', "no sealant bead in our scope: acoustical sealant (2/A500) EXCLUDED in all projects (estimator standing order)")
    d.setdefault('sealant_source', '2/A500')
WW = {w['id']: w for w in c['walls']}
for w in c['walls']:
    for k in ('length_source', 'height_source'):
        m = _re.match(r'\s*(?:same )?as ([A-Z0-9]+-\w+)\s*$', str(w.get(k) or ''), _re.I)
        if m and m.group(1) in WW:
            w[k + '_info'] = w[k]; w[k] = WW[m.group(1)][k]
    w.setdefault('length_basis', 'face of gypsum board to face of gypsum board (A100 general note 9: dimensions from face of gypsum board)')
    if 'tick' not in str(w.get('length_op', '')).lower():
        w['length_op'] = str(w.get('length_op', '')) + ' [A100 dimension strings: SIMPLE slash ticks; total of the string as printed]'
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 31. gate items: sill band of the cased opening, BLK-PENDANT in LF, discarded tags with motivo + inventory crop,
#     R70.2 corner E3-03 / E3-07a (E3-03 owns the square: +0.417 ft = 7.5 pt measured by esquinas.py), EWC niche mouth gap,
#     D-01 tag read by the two readings (single letter, not by inventario_tags.py)
c = json.load(open(P))
inv = json.load(open('/root/cc/work/etapas/1_inventario/inventario.json'))
rec = {x['id']: x for v in inv['ocurrencias'].values() for x in v if x.get('id')}
for k in ():
    for x in inv.get(k) or []:
        if isinstance(x, dict) and x.get('id'): rec[x['id']] = x
def walk(o):
    if isinstance(o, dict):
        if str(o.get('id', '')).startswith(('PC', 'PA', 'PT')): rec.setdefault(o['id'], o)
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
walk(inv)
for t in c.get('tags_descartados') or []:
    x = rec.get(t.get('id'), {})
    t.setdefault('motivo', t.get('reason') or t.get('why') or 'not a partition tag')
    if not t.get('motivo'): t['motivo'] = 'not a partition tag'
    if x.get('png'):
        t['imagen'] = '1_inventario/recortes/' + x['png']
    txt = str(x.get('text') or x.get('tag') or '')
    if 'CO2' in txt or 'CO2' in str(t.get('motivo')):
        t['motivo'] = f"store number 'CO2' in the title block (sheet {x.get('sheet', '')}), not a partition tag"
    elif txt.startswith('TC') or 'TC' in str(t.get('motivo'))[:6]:
        t['motivo'] = f"electrical tag {txt} (sheet {x.get('sheet', '')}): telecom / circuit symbol, not a partition tag"
for w in c['walls']:
    for o in w.get('openings') or []:
        if o['ref'] == 'CASED-OPEN-HALL':
            o['sill_ft'] = 0.0; o['sill_source'] = '2/A400 (opening to the floor, OPEN TO HALLWAY)'
    if False:
        w['band']['hi'] = round(w['band']['hi'] + 7.5, 1); w['length_ft'] = round(w['length_ft'] + 0.417, 3)
        w['length_op'] = str(w['length_op']) + ' + 0.417 (R70.2: E3-03 owns the corner square with E3-07a, 7.5 pt measured by esquinas.py)'
        w['r70_2'] = True
    if w['id'] == 'D-01' and not w.get('tag_ids'):
        w['tag_read_info'] = "the D diamond is printed on A100 at the restroom / office wall; single-letter tag not counted by inventario_tags.py; located by readings A and B (crop img_runner/wall_D-01.png)"
        w['default_type_source'] = 'D/A100'
for b in c['blocking_items']:
    if b['ref'] == 'BLK-PENDANT':
        b.pop('unit', None); b.pop('qty', None)
c['gaps_ok'] = [x for x in c.get('gaps_ok') or [] if not ({'E3-05', 'E3-10', 'E3-14'} & set(x.get('between') or [])) and set(x.get('between') or []) != {'E3-02', 'E3-03'} and set(x.get('between') or []) != {'E3-06', 'E3-08'}]
g = c['gaps_ok']
if not any(set(x.get('between') or []) == {'E3-04', 'E3-09'} for x in g):
    g.append({"between": ["E3-04", "E3-09"], "reason": "open mouth of the EWC niche to the hallway (A100, P101 EWC): returns E3-06 / E3-08 frame the niche; no wall in the gap"})
co = c.setdefault('corners_ok', [])
if not any(set(x.get('walls') or []) == {'E3-07a', 'E3-03'} for x in co):
    co.append({"walls": ["E3-07a", "E3-03"], "reason": "the corner square is covered by E3-07b, the collinear continuation of E3-07a (T of E3-03 on the E3-07a | E3-07b line, A100)"})
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 32. names / sources that reach the Excel: product names printed in this set, ceiling detail sheet, accessory rows
#     without opening wider than 4'-0" / coiling grille, internal file names out of visible texts, FRP product code
c = json.load(open(P))
pn = c['constants'].setdefault('product_names', {})
pn.pop('nested inner runner (deflection head)', None)
pn['track de ceilings / soffits'] = {"value": "Ceiling perimeter track 20 GA (restroom C-1 ceiling)", "source": "1/A200"}
for ce in c['ceilings']:
    ce['detail'] = '2/A501' if ce.get('system') == 'usg_grid' else '1/A200'
an = c['accesorios_none']
for f, why, src in (("additional head track", "no opening wider than 4'-0\": doors 4C / 5C / 6C R.O. 3'-4\" (A600), cased opening 4'-0\" (2/A400)", "A600, 2/A400"),
                    ("2-1/2\" CFMF coiling grille head", "no coiling grille / overhead door in the set (A600 door schedule, A100)", "A600")):
    if not any(r['familia'] == f for r in an): an.append({"familia": f, "why": why, "source": src})
c['frp_none_reason'] = "FRP B-3 (A700, Marlite pebbled FRP) in the restroom and mop sink area to 4'-0\" (A402, 1/A504): finish product, EXCLUDED (not metal framing / gypsum board); WR gypsum board behind it is in the wall faces"
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 33. RCP sheet of the ceilings; demolition items cite the demolition plan drawing 1/D100 (title '1 EXISTING CONDITIONS AND DEMOLITION PLAN')
c = json.load(open(P))
c['constants']['rcp_sheet'] = {"value": "A200", "source": "1/A200"}
for ce in c['ceilings']:
    ce['sheet'] = 'A200'
for m in c['misc_items']:
    if m['ref'].startswith('DEMO') and not str(m.get('source', '')).startswith('1/D100'):
        m['source_info'] = m.get('source_info') or m.get('source'); m['source'] = '1/D100'
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 34. hatch check: the A200 legend draws C-1 GYP BOARD CEILING as a plain (unhatched) square; the polygon follows the
#     restroom walls (inside faces, registered A200 vs A100) -> hatch_check_cause with the legend citation
c = json.load(open(P))
for ce in c['ceilings']:
    ce['hatch_check_cause'] = "1/A200 SHEET SYMBOLS: 'C-1 GYP BOARD CEILING' is a plain square (no hatch, only the ACT C-2 / C-3 are gridded); polygon = inside faces of the restroom walls (rcp_check.png)"
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 35. gate fixes (compuerta de entrega, first pass):
#   - D-01 tag = PT0001 (inventory completed by scripts/inventario_1A500.py)
#   - one Partition Takeoff row per wall id (= the markups), U-120
#   - wall detail = 1/A500 (the partition types drawing; the diamond keys A# / C# / D / E# are not detail numbers)
#   - face heights with their state; demo heights cite 1/A100 (A100 drawing 1 CONSTRUCTION FLOOR PLAN deck tags)
#   - control joints on walls over 30'-0" (ASTM C840; precedent R80e.34 #8): one full-height joint per face
#   - FRP B-3 of the finish schedule carried (precedents R80e.34 #5 / R80e.78 #6, standard O'Reilly U-145): restroom to 4'-0"
#     (A402) and mop sink alcove to 4'-0" (1/A504)
c = json.load(open(P))
c['constants']['partition_row_rule'] = {"value": "wall_id", "source": "A100 wall ids: one Partition Takeoff row per wall, the same ids as the markups"}
for w in c['walls']:
    if w['id'] == 'D-01': w['tag_ids'] = ['PT0001']
    w['detail_type_info'] = f"{w['tag']} key of 1/A500"
    w['detail'] = '1/A500'
    for f in w['faces']:
        f.setdefault('height_status', 'DERIVADO')
        if '[DERIVED]' not in f['height_source'] and '[CONFIRMED]' not in f['height_source']:
            f['height_source'] = f['height_source'] + ' [DERIVED]'
    for k in ('location', 'length_source'):
        if _re.search(r'(?i)\bto remain\b', str(w.get(k, ''))):
            w[k] = _re.sub(r'(?i)\bto remain\b', 'that stays', w[k]) + ' [NEW wall of this take-off]'
c['details'].setdefault('1/A500', {})
c['details']['1/A500'].update({"source": "1/A500", "title": "PARTITION TYPES (A#, C#, D, E#, H)", "layers_per_face": 1,
    "layers_source": "1/A500 (one layer 5/8\" TYPE X per face on every type)",
    "sealant_none_reason": "acoustical sealant (2/A500) EXCLUDED in all projects (estimator standing order)", "sealant_source": "2/A500"})
for m in c['misc_items']:
    if m['ref'].startswith('DEMO'):
        m['height_source'] = "1/A100 'PLY DECK @ 17'-1 9/16\"' (printed B.O. structure; the deck break is not drawn: higher bay) - estimator standing rule: existing partitions to demolish without printed height go to the printed B.O. structure"
W = {w['id']: w for w in c['walls']}
c['misc_items'] = [m for m in c['misc_items'] if not m['ref'].startswith(('CJ-', 'FRP-'))]
for wid in ('A3-03', 'C3-01'):
    w = W[wid]; fs = [f for f in w['faces'] if f['side'] in ('A', 'B')]
    q = round(sum(f['height_ft'] for f in fs), 2)
    c['misc_items'].append({"ref": f"CJ-{wid}", "familia": "control joint", "qty": q, "unit": "LF", "source": "1/A500",
        "op": f"{wid} {w['length_ft']} LF > 30'-0\": 1 control joint per face x full board height = " + " + ".join(str(f['height_ft']) for f in fs) + f" = {q} LF (ASTM C840 / GA-216; estimator standing precedent: control joints on runs over 30 ft)", "status": "DERIVADO"})
c.pop('control_joints_none', None)
rr = 31.75 - 3.333; ms = 4.0 + 2 * 2.333
c['misc_items'] += [
 {"ref": "FRP-RR", "familia": "FRP", "qty": round(rr * 4.0, 2), "unit": "SF", "source": "A402", "op": f"restroom perimeter 31.75 LF (A100 polygon) - door 4C 3.333 = {round(rr, 2)} LF x T.O. FRP 4'-0\" (A402) = {round(rr * 4.0, 2)} SF (A700 B-3; estimator standing precedent: FRP of the finish schedule is carried)", "status": "DERIVADO"},
 {"ref": "FRP-MOP", "familia": "FRP", "qty": round(ms * 4.0, 2), "unit": "SF", "source": "1/A504", "op": f"mop sink alcove back 4.0 + 2 sides x 2.333 = {round(ms, 2)} LF x 4'-0\" FRP (1/A504) = {round(ms * 4.0, 2)} SF", "status": "DERIVADO",
  "inside_corners": {"value": 2, "vertices": 4, "outside_corners": 0, "source": "1/A504"}}]
c.pop('frp_none_reason', None)
c['accesorios_none'] = [r for r in c['accesorios_none'] if r['familia'] != 'PVC trim at FRP']
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 36. frp block (canon schema): top 4'-0" (A402 'T.O. FRP 4'-0"'); areas carried as misc FRP-RR / FRP-MOP (the restroom
#     perimeter is the A100 polygon of the C-1 ceiling, the mop alcove from 1/A504), no tile_base in the set (base per A502)
c = json.load(open(P))
c['frp'] = {"top_ft": {"value": 4.0, "source": "A402"}, "rooms": [],
            "rooms_info": "restroom and mop sink alcove FRP carried as misc items FRP-RR (A402) and FRP-MOP (1/A504)"}
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 37. FRP as misc items -> canon frp block replaced by its reason text + pvc_trim_items (accesorios R80e.35 path), back-check
#     BC-D5: braces of E3-11a / E3-11b (on the C3 line) to the 17'-1 9/16" deck; BC-D6: untagged niche returns joined
c = json.load(open(P))
c.pop('frp', None)
c['frp_none_reason'] = "FRP B-3 (A700) carried as misc items FRP-RR (restroom to T.O. FRP 4'-0\", A402) and FRP-MOP (mop sink alcove, 1/A504); no tile_base in the set"
per = round(31.75 - 3.333, 3)
c['pvc_trim_items'] = [
 {"ref": "PVC-RR", "lf": round(2 * per + 5 * 4.0 + 2 * 1 * 4.0, 2), "source": "A402",
  "op": f"restroom: edge top + bottom 2 x {per} + inside corners 5 x 4.0 (A100 polygon: 6 vertices, 5 inside / 1 outside) + door 4C jambs 2 x 4.0 = {round(2 * per + 28.0, 2)} LF"},
 {"ref": "PVC-MOP", "lf": round(2 * 8.667 + 2 * 4.0 + 2 * 4.0, 2), "source": "1/A504",
  "op": "mop sink alcove: edge top + bottom 2 x 8.667 + 2 inside corners x 4.0 + 2 vertical ends x 4.0 = 33.33 LF"}]
for m in c['misc_items']:
    if m['ref'] in ('BRACE-E3-11a', 'BRACE-E3-11b') and '17.13 B.O.' not in m['op']:
        w = next(x for x in c['walls'] if x['id'] == m['wall'])
        n = m['pcs'] // 2 if m['pcs'] % 2 == 0 else m['pcs']
        mem = 2 if w['height_ft'] > 10 else 1
        ln = round((17.13 - w['height_ft']) * 1.414, 3); q = round(n * mem * ln, 2)
        m['qty'] = q; m['op'] = f"n = ceil({w['length_ft']} / 4) + 1 = {n} x {mem} member(s) x (17.13 B.O. deck on the C3 line A100 - {w['height_ft']} top) x 1.414 = {q} (back-check D5)"
for w in c['walls']:
    if w['id'] in ('E3-06', 'E3-08'):
        w['untagged_join'] = "EWC niche return without its own tag: carried as the adjoining tagged E3 walls (E3-04 / E3-09 line), same type (E28 eje rule)"
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 38. U-114 states: printed deck tag heights = CONFIRMED (the choice between the two printed decks is RFI-01); E3-08 op
c = json.load(open(P))
for w in c['walls']:
    if _re.match(r"\s*A100 'PLY DECK @", str(w.get('height_source'))) and w['height_ft'] in (16.333, 17.13):
        w['height_status'] = 'CONFIRMADO'
    if w['id'] in ('E3-06', 'E3-08') and '1.5 - 7.5/18' not in str(w.get('length_op')):
        w['length_op'] = "1'-6\" printed (A100) - back wall 7.5 pt / 18 = 1.5 - 7.5/18 = 1.083 " + str(w.get('length_op'))
for ce in c['ceilings']:
    ce['height_status'] = 'CONFIRMADO'; ce['height_source'] = "1/A200 restroom tag H 8'-0\" [CONFIRMED]; A402 CEILING 8'-0\""
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
# 39. rev2 (BE-CC07): bubbles that govern carried rows are cited in their rows (U-141): 6/A502 RESTROOM COVE BASE = the FRP bottom
#     edge J-mold over the cove base (PVC-RR 'edge top + bottom'); 1/A400 = slat wall elevation (BLK-SLAT-N 'A400 1');
#     3/A400 = logo wall S elevation (BLK-LOGO-S 'A400 3')
c = json.load(open(P))
for x in c.get('pvc_trim_items') or []:
    if x['ref'] == 'PVC-RR' and '6/A502' not in x['source']:
        x['source'] += '; 6/A502 (FRP bottom edge J-mold over the cove base)'
for x in c.get('blocking_items') or []:
    if x['ref'] == 'BLK-SLAT-N' and '1/A400' not in x['source']:
        x['source'] += '; 1/A400 (slat wall elevation)'
    if x['ref'] == 'BLK-LOGO-S' and '3/A400' not in x['source']:
        x['source'] += '; 3/A400 (logo wall elevation)'
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
print('39 ok')
# 40. rev2: the restroom grid ceiling cites its system detail 2/A501 in its source (Excel row N/SHEET)
c = json.load(open(P))
for ce in c['ceilings']:
    if ce.get('system') == 'usg_grid' and '2/A501' not in ce.get('source', ''):
        ce['source'] = '2/A501; ' + ce.get('source', '1/A200, A402')
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
print('40 ok')
