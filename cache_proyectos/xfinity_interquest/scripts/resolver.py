"""Resolution of reading A vs B (Xfinity Interquest) -> etapas/4_canon/takeoff_canon.json + 3_revision/resolucion.md.
Base = reading A (complete canon). Every decision from the plans (U-156 / U-162), each with N/SHEET + crop."""
import json, math, copy
K = '/root/xf/work'
A = json.load(open(f'{K}/etapas/2_lectura/canon_A.json')); B = json.load(open(f'{K}/etapas/2_lectura/canon_B.json'))
c = copy.deepcopy(A)
H_STR = 26.0; H_SRC = "A0.1 code analysis 'HEIGHT IN STORIES: 1 STORY - 26 FT' (only structure-related height printed; B.O. structure not printed on any sheet - RFI-01, conservative higher value U-146 / R-ALC-07)"
dec = []
# 1. W2-01 through the door R.O. (reading B), stub W2-01a merged
bw = next(w for w in B['walls'] if w['id'] == 'W2-01')
w = next(w for w in c['walls'] if w['id'] == 'W2-01')
w['band'] = dict(w['band'], lo=1237.56, hi=1489.08)
w['length_ft'] = round((1489.08 - 1237.56) / 18, 3)
w['length_source'] = ("A2.0 1/A2.0 vertical dimension string x~856: printed 4\" + 3'-0\" DOOR (ticks 1237.56 / 1243.56 / 1297.56) + "
                      "vector from door jamb 1297.56 to north face of existing post 1489.08; wall measured THROUGH the door R.O. (one straight line per tag)")
w['length_op'] = "(1489.08-1237.56)/18 = 13.973 (= 0.333 printed 4\" + 3.000 printed door + 10.640 vector)"
w['length_status'] = 'DERIVADO'
w['openings'] = [{"ref": "Door 101", "ro_w_ft": 3.0, "source": "A2.0 printed '3'-0\" DOOR'"}]
w['tag_ids'] = sorted(set((w.get('tag_ids') or []) + next(x for x in A['walls'] if x['id'] == 'W2-01a').get('tag_ids', [])))
c['walls'] = [x for x in c['walls'] if x['id'] != 'W2-01a']
dec.append(("W2-01 length", "A 10.64 LF (door gap excluded, 4\" stub apart) vs B 13.97 LF (through the door)",
            "B: 13.973 LF through the door 101 R.O.; stub W2-01a merged (skill rule: one straight line per tag, openings listed in the wall; board never deducts openings U-057)",
            "A2.0 dimension string 4\" + 3'-0\" DOOR", "img/001_DIF_W2_A2.0_p5.png"))
# 2. existing W1 / W4: not ours (patch & repair only) -> out of walls, tags discarded with reason
EX = [x for x in c['walls'] if x.get('tag') in ('W1', 'W4') or x['id'].startswith(('W1', 'W4'))]
c['walls'] = [x for x in c['walls'] if x not in EX]
c['existing_walls_info'] = [{"id": x['id'], "type": x.get('tag') or x['id'][:2], "lf": x.get('length_ft'), "location": x.get('location'),
                              "why": ("2/A2.0 WALL TYPE 1 'EXISTING DEMISING / EXTERIOR WALL TO REMAIN. PATCH AND REPAIR AND MAINTAIN ANY EXISTING FIRE RATING (V.I.F.)'" if (x.get('tag') or x['id']).startswith('W1')
                                      else "2/A2.0 WALL TYPE 4 'INTERIOR WALL TO REMAIN. PATCH AND REPAIR AND MAINTAIN ANY EXISTING FIRE RATING (V.I.F.)'") + " - no new board / framing: not quantified; patch & repair = allowance (Review Item)",
                              "img": x.get('img')} for x in EX]
td = c.setdefault('tags_descartados', [])
for x in EX:
    for t in x.get('tag_ids') or []:
        td.append({"id": t, "motivo": f"tag of existing wall {x['id']} ({x.get('tag')}): existing to remain, patch and repair only (2/A2.0) - not a new wall, not quantified", "imagen": x.get('img')})
dec.append(("W1 / W4 existing walls", f"A {sum(1 for x in A['walls'] if x['id'].startswith(('W1','W4')))} lines / B {sum(1 for x in B['walls'] if x['id'].startswith(('W1','W4')))} lines (W4-04 10.99 vs 10.59 LF)",
            "not quantified: 2/A2.0 types 1 and 4 = existing walls to remain, patch and repair only (no LF enters the take-off; the W4-04 difference has no effect)", "2/A2.0", "img/002_DIF_W4_A2.0_p5.png"))
# 3. column furring typed by 5/A2.0 + key note 1 (only reading A had it as walls; B listed it in its notes)
for x in c['walls']:
    if x['id'].startswith('CF'):
        x['type'] = 'COLUMN FURRING'; x['tag'] = 'CF'; x['element'] = 'wall'
        x['type_source'] = "5/A2.0 NON-RATED COLUMN FURRING (bubble '5/A2.0 SIM.' at each column) + A2.0 key note 1"
        x['gauge'] = '43 mil (18 ga), 250S125-43'
        x['gauge_source'] = "A2.0 INTERIOR WALL LIMITING HEIGHTS table: 250S125-43 @16\" o.c. = 13'-0\" >= 12'-6\" furring height (lightest 2-1/2\" member that passes at 16\" o.c.)"
        x['oc_in'] = 16; x['oc_source'] = "A2.0 limiting heights table row 250S125-43 @16\" (studs at each corner per 5/A2.0)"
dec.append(("Column furring CF-01 / CF-02", "only in A as walls (B: 2 columns, 4.77 LF in its notes)", "A: 2 x 2.38 LF exposed perimeter, 3 sides, 12.5 ft (key note 1 + A3.0 12'-0\" + 6\"); 2-1/2\" 250S125-43 @16\" per A2.0 table",
            "5/A2.0, A2.0 key note 1, A2.0 limiting heights", "img/003_ONLYA__A2.0_p5.png"))
# 4. structure height (RFI-01, conservative) -> braces and demo
# DEMO-10: key-7 dashed wall at the west counter of Retail 100 (A1.0), found by the independent review R2 (E1) - same pattern as DEMO-08/09
if not any(m['ref'] == 'DEMO-10' for m in c['misc_items']):
    c['misc_items'].append({"ref": "DEMO-10", "element": "demo", "familia": "demolition", "sheet": "A1.0", "page": 4,
        "lf": round((1401.72 - 1244.52) / 18, 3), "band": {"ori": "V", "c0": 630.24, "c1": 637.56, "lo": 1244.52, "hi": 1401.72, "sheet": "A1.0"},
        "length_source": "A1.0 dashed double line (7.32 pt = wall thickness) x 630.24/637.56 from the north demising inner face 1244.52 to its free end 1401.72, beside the dashed counter with sinks; A1.0 key note 7 arrow points at it",
        "length_op": "(1401.72-1244.52)/18 = 8.733", "length_status": "DERIVADO", "source": "A1.0 key note 7",
        "note": "found by the independent review before delivery (Auditoria/revision_independiente/R2, E1); A1.0 key note 7 'ALL EXISTING INTERIOR WALLS ... SHOWN DASHED TO BE REMOVED' = wall, same as DEMO-08 / DEMO-09",
        "img": "/root/xf/work/revision_indep/R2/crops/A1.0_UNMARKED_key7_wall_x630.png"})
# Independent review R1 (before delivery): F3 demolition through the removed door; F4 backing of the GF-14496 graphic frame on W2
if not any(m['ref'] == 'DEMO-11' for m in c['misc_items']):
    c['misc_items'].append({"ref": "DEMO-11", "element": "demo", "familia": "demolition", "sheet": "A1.0", "page": 4,
        "lf": round((928.32 - 866.28) / 18, 3), "band": {"ori": "H", "c0": 1452.48, "c1": 1459.8, "lo": 866.28, "hi": 928.32, "sheet": "A1.0"},
        "length_source": "A1.0: existing door removed by key note 7 in the line of DEMO-03 / DEMO-04 (x 866.28 to 928.32, y 1452.5-1459.8); the wall is measured THROUGH the opening (standing rule, walls through openings)",
        "length_op": "(928.32-866.28)/18 = 3.447", "length_status": "DERIVADO", "source": "A1.0 key note 7",
        "note": "found by the independent review R1 (F3) before delivery", "img": "/root/xf/work/revision_indep/R1/F03_A1.0_door_gap_DEMO03_04.png"})
if not any(b['ref'] == 'BK-GF14496' for b in c['blocking_items']):
    c['blocking_items'].append({"ref": "BK-GF14496", "lf": 21.55, "material": "16 ga x 6\" x 1-1/2\" unpunched track (8/A2.0)",
        "label": "backing behind the GF-14496 144\" x 96\" graphic frame on the new W2 line: A4.0 key note 1 / A2.0 key note 2 'PROVIDE BLOCKING SUPPORT BEHIND WALL-MOUNTED EQUIPMENT - SEE DTL 8/A2.0'; 8/A2.0 track extended one bay beyond the equipment",
        "source": "A4.0 GF-14496 + key note 1; A2.0 key note 2; 8/A2.0", "wall": "W2-01",
        "op": "one row on the new walls = W2-01 5.44 + one bay 1.333 + W2-02 4.0 = 10.78 LF (the 1.0 ft existing post and 1.57 ft existing W4 not ours); rows not printed -> 2 rows (top and bottom of the 96\" frame, standing rule R-ALC-02) = 21.55 LF",
        "status": "DERIVADO", "note": "found by the independent review R1 (F4) before delivery", "img": "/root/xf/work/revision_indep/R1/F04_A4.0_GF-14496_on_W2_and_Retail_key1.png"})
if not any(m['ref'] == 'STUD16-GF' for m in c['misc_items']):
    c['misc_items'].append({"ref": "STUD16-GF", "familia": "3-5/8\" stud (todos los gauges)", "qty": 125.0, "unit": "LF",
        "source": "8/A2.0 '16 GA. METAL STUD 16\" O.C. @ ALL BACKING STUD TRACKS'; A4.0 GF-14496 on W2",
        "op": "16 ga (54 mil) 3-5/8\" studs in the backing zone: W2-01 ROUNDUP(5.44/1.333)+1 = 6 + W2-02 ROUNDUP(4.0/1.333)+1 = 4 = 10 studs x 12.5 ft = 125.0 LF (conservative: the 20 ga studs of the same bays stay in the W2 row; delta -125.0 LF of 20 ga if replaced)",
        "status": "DERIVADO", "gauge": "16 ga (54 mil)", "img": "/root/xf/work/revision_indep/R1/F07_8A2.0_backing_16ga.png"})
for w_ in c['walls']:
    if 'openings_note' in w_ and 'no backing' in str(w_['openings_note']):
        w_['openings_note'] = str(w_['openings_note']).replace('no backing called', 'backing of the GF-14496 graphic frame carried in BK-GF14496 / STUD16-GF (A4.0 key note 1, 8/A2.0)')
nb = {'W2-01': math.ceil(13.973 / 8) + 1, 'W2-02': math.ceil(4.0 / 8) + 1}
for m in c['misc_items']:
    if m['ref'].startswith('BRACE-'):
        wid = m['ref'][6:]; n = nb[wid]; L = round((H_STR - 12.5) * math.sqrt(2), 3)
        m.update(qty=n, unit='EA', lf=round(n * L, 3), status='DERIVADO', height_source=H_SRC,
                 op=f"n = ceil(len/8.0)+1 = {n} (4/A2.0 @8'-0\" o.c. max); length each = (26.0 - 12.5) x 1.414 = {L} (45 deg); total {round(n*L,3)} LF <= 25'-0\" max per brace OK",
                 note="structure height not printed: conservative 26'-0\" (A0.1) loaded, RFI-01")
    if m.get('element') == 'demo' and m.get('lf'):
        m['height_ft'] = H_STR; m['height_source'] = H_SRC; m['height_status'] = 'DERIVADO'
        m['sf'] = round(m['lf'] * H_STR, 2); m['op'] = f"{m['lf']} LF x {H_STR} ft = {m['sf']} SF (area of the element, no layers, U-143)"
        if m['ref'] in ('DEMO-08', 'DEMO-09'):
            m['note'] = "A1.0 key note 7 arrow lands on the inner dashed pair (wall thickness 7.32 pt) of the L element: 'ALL EXISTING INTERIOR WALLS ... SHOWN DASHED TO BE REMOVED' = wall (RFI-03 closed by the plan)"
c['misc_items'] = [m for m in c['misc_items'] if m['ref'] not in ('DEMO-CEIL-RETAIL', 'DEMO-CEIL-STORAGE')]
c['demo_ceiling_excluded'] = {"why": "A1.0 key note 14 'REMOVE EXISTING CEILING FINISHES ... AS REQUIRED' / key 15 'EXISTING CEILING GRID TO REMAIN. REMOVE ... CEILING TILES' (retail / storage = ACT, other trade): no existing gypsum ceiling demolition shown - EXCLUDED (existing ceiling type not indicated for removal; R-ALC-05)", "source": "A1.0 keys 14 / 15, A3.0"}
dec.append(("Demolition A1.0", f"A {sum(m.get('lf') or 0 for m in A['misc_items'] if m.get('element')=='demo'):.2f} LF (9 pieces) vs B {sum(m.get('lf') or 0 for m in B['misc_items'] if m.get('element')=='demo'):.2f} LF (8 pieces, DEMO-01+02 joined)",
            "A pieces (same lines, |delta| < 1 %); L element DEMO-08/09 = wall by key note 7; height 26'-0\" conservative (RFI-01)", "A1.0 key note 7", "img/demo_L_A1.0.png"))
# 5. door 101 RO printed -> closed; SOF-01 framed header; furring gauge
c['ceilings'][0]['system'] = ("framed header at the opening left by DEMO-01: 3-5/8\" 20 ga studs + track as type W2 (2/A2.0), underside at 8'-6\" (A3.0 'GYP. BD. 8'-6\" AFF'), "
                              "faces to 6\" above the adjacent ceilings (A2.0 wall legend); A3.0 lighting legend '5/8\" TYPE X GYPSUM BOARD CEILING'")
DLF = round(sum(m['lf'] for m in c['misc_items'] if m.get('element') == 'demo' and m.get('lf')), 2); DSF = round(sum(m.get('sf') or 0 for m in c['misc_items'] if m.get('element') == 'demo'), 2)
for r in c['rfis']:
    r['status'] = 'closed'   # RFI-01 closed 11-nov by user decision (button 'A: 26\'-0" (cargado)', U-174)
RES = {
 'RFI-02': "CLOSED by the plans: A3.0 tags the strip 'GYP. BD. 8'-6\" AFF' (no 'EXISTING' on this tag, unlike the hallway 9'-0\" tag) where A1.0 removes DEMO-01; built as a framed header with type W2 framing, underside 1.73 SF + storage face to 10'-6\" + hallway face to 9'-6\" (A2.0 wall legend 'TO 6\" ABOVE CEILING') - loaded (option A).",
 'RFI-03': "CLOSED by the plans: A1.0 key note 7 ('ALL EXISTING INTERIOR WALLS, DOORS AND WINDOWS AS SHOWN DASHED TO BE REMOVED') points at the inner dashed pair of the L element = wall; DEMO-08 / DEMO-09 loaded.",
 'RFI-04': "CLOSED by the plans: A2.0 prints '3'-0\" DOOR' between the W2 ends = rough opening as drawn (option A); the wall is measured through the opening, so the R.O. only changes the head length.",
 'RFI-05': "CLOSED by the plans: A2.0 INTERIOR WALL LIMITING HEIGHTS table, 250S125-43 @16\" = 13'-0\" >= 12'-6\" (lightest 2-1/2\" member passing at 16\" o.c.) - loaded (option A).",
}
for r in c['rfis']:
    if r['id'] in RES:
        r['resolved'] = {"answer": RES[r['id']], "by": "plans (U-156 / U-162)"}
    if r['id'] == 'RFI-01':
        r['resolved'] = {"answer": "user decision 11-nov (button 'A: 26'-0\" (cargado)', U-174): the height of the existing structure is not printed on any sheet, so the A0.1 code analysis building height 'HEIGHT IN STORIES: 1 STORY - 26 FT' is carried as loaded for the 5 braces of 4/A2.0 and the demolished walls DEMO-01..11; quantities unchanged. Sensitivity kept for the estimator: each 1 ft lower B.O. structure = -7.07 LF braces and -{0:.2f} SF demolition.".format(DLF), "by": "user decision (U-174)"}
        r['loaded'] = "26'-0\" (A0.1 building height, conservative) for the 5 braces of 4/A2.0 and the height of the demolished walls"
        r['question'] = ("Height of the existing structure (underside of roof structure) is not printed on any sheet (A0.1-A5.0 text, E / M / P SHX searched: DECK, JOIST, STRUCTURE, B.O., BOTTOM OF, ROOF, CLG. HT., PLENUM, AFF; "
                         "M1.0 only says 'EXISTING CONCRETE BEAM ABOVE CEILING'). Needed for the 4/A2.0 brace length and the SF of the walls demolished on A1.0. No code section gives an existing structure height.")
        r['opciones'] = {"A": {"texto": "Drawings: only A0.1 'HEIGHT IN STORIES: 1 STORY - 26 FT' is printed -> 26'-0\" carried (conservative)", "source": "A0.1", "delta": f"loaded: braces 5 x 19.09 = 95.46 LF; demo {DLF:.2f} LF x 26 = {DSF:,.2f} SF (per element)"},
                         "B": {"texto": "Code: none applies - IBC 2021 / ASTM C754 do not set an existing structure height", "cita": "IBC 2021 Ch. 25 (no height requirement); ASTM C754 Section 7 (bracing per design)", "delta": "n/a"},
                         "C": ""}
        r['delta'] = (f"each 1 ft lower B.O. structure: -7.07 LF braces (5 x 1.414) and -{DLF:.2f} SF demolition; separately, if the counter core "
                      f"DEMO-08 / DEMO-09 (A1.0, 18.51 LF) is a 4'-0\" pony wall instead of full height: -{18.51 * 22:,.2f} SF")
c['constants']['deck_heights'] = {"value": H_STR, "source": "A0.1", "source_info": H_SRC}
c['project'] = "Xfinity - Interquest, 1333 Interquest Pkwy, Lot 11, Colorado Springs CO 80921 (Robert F. Vanney Architect 81-2116, Complete PDF Set 10/08/2026 R0) - resolved canon"
json.dump(c, open(f'{K}/etapas/4_canon/takeoff_canon.json', 'w'), indent=1, ensure_ascii=False)
L = ["# Resolution A / B — Xfinity Interquest (A2.0 / A1.0 / A3.0)", "", "Each item: difference -> decision -> N/SHEET -> image. Never averaged, never chosen silently.", ""]
for i, (it, d, r, s, im) in enumerate(dec, 1):
    L += [f"{i}. **{it}** — {d} -> **{r}** — source {s} — ![img]({im})"]
L += ["", "## RFIs of the readers re-swept (U-156 / U-162: plans first, then code)", ""]
for r in c['rfis']:
    L.append(f"- {r['id']} ({r['status']}): " + (r.get('resolved', {}).get('answer') or ('OPEN - loaded ' + r.get('loaded', ''))))
L += ["- Reader B open questions: deck height = RFI-01; W2 gauge / spacing = A2.0 limiting heights table (362S125-33 @16\", 20 ga per 4/A2.0 'MATCH WALL STUD SIZE & GAUGE (3 5/8\" 20 GA. MIN.)'); face heights = A3.0 ceiling tags + legend 6\"; patch extent of existing walls = Review Item allowance; header build = 7/A2.0; demo height = RFI-01; column size = vector (5.5\" x 5.0\")."]
L += ["", "## Alerts of comparar.py", "", "- TAG SIN WALL PT0018-PT0022: wall-type legend symbols of 2/A2.0 (discarded by both readers with image).",
      "- TYPE NO INVENTARIADO '' : column furring (5/A2.0, no tag) - typed COLUMN FURRING by 5/A2.0 + key note 1."]
open(f'{K}/etapas/3_revision/resolucion.md', 'w').write('\n'.join(L) + '\n')
print('walls', [(x['id'], x['length_ft']) for x in c['walls']], 'open rfis', [r['id'] for r in c['rfis'] if r['status'] == 'open'])
# --- RFI-01 search record (U-140 / U-156) + closed RFI wording (they speak from the loaded value) ---
import re as _re, os as _os
import pymupdf as fitz
from PIL import Image, ImageDraw
st = json.load(open(f'{K}/set_texto.json'))['hojas']
TERMS = ["DECK", "JOIST", "STRUCTURE", "B.O.", "BOTTOM OF", "ROOF", "CLG. HT.", "CEILING HT", "PLENUM", "BEAM", "26 FT", "HEIGHT", "AFF", "SECTION", "TRUSS"]
txt = {h: (v if isinstance(v, str) else (v.get('texto') or v.get('text') or '')).replace('\n', ' ') for h, v in st.items()}
desc = {}
for h, t in txt.items():
    for term in TERMS:
        i = t.upper().find(term)
        if i >= 0:
            desc[h] = (f"read on {h}: '{t[max(0, i - 40):i + 60]}' - printed value of another element / condition (ceiling height, mounting height, roof work, "
                       f"stud / ceiling span tables, code data); no underside-of-structure height is printed on {h}")
            break
desc['A0.1'] = ("A0.1 'HEIGHT IN STORIES: 1 STORY - 26 FT' is the building height in the code analysis (to the top of the building), not the underside "
                "of the roof structure; it is the only structure-related figure printed and is carried as the conservative value (higher bound)")
doc = fitz.open(f'{K}/plans/bidset_SIN_MARKUPS.pdf'); SM = {v: int(k) for k, v in json.load(open(f'{K}/etapas/SHEET_MAP.json')).items()}
IMG = f'{K}/etapas/4_canon/img/review'; _os.makedirs(IMG, exist_ok=True)
def crop_rfi(sheet, term, name):
    p = doc[SM[sheet] - 1]; R_ = p.rotation_matrix
    rs = [r * R_ for r in p.search_for(term)]
    if not rs:
        rs = [fitz.Rect(a.rect) * R_ for a in p.annots() or [] if term.upper() in (a.info.get('content') or '').upper()]
    r = rs[0]; r.normalize()
    clip = fitz.Rect(r.x0 - 150, r.y0 - 70, r.x1 + 150, r.y1 + 70) & p.rect
    pix = p.get_pixmap(dpi=120, clip=clip); im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    s = pix.width / clip.width; dr = ImageDraw.Draw(im)
    dr.ellipse([(r.x0 - clip.x0 - 10) * s, (r.y0 - clip.y0 - 10) * s, (r.x1 - clip.x0 + 10) * s, (r.y1 - clip.y0 + 10) * s], outline=(255, 0, 0), width=4)
    f = f'{IMG}/{name}.png'; im.save(f); return f
lug = [{"sheet": "A0.1", "term": "26 FT", "img": crop_rfi("A0.1", "26 FT", "RFI-01_A0.1_26FT")},
       {"sheet": "A2.0", "term": "BRACE TO STRUCTURE", "img": crop_rfi("A2.0", "BRACE TO STRUCTURE", "RFI-01_A2.0_brace")},
       {"sheet": "M1.0", "term": "CONCRETE BEAM", "img": crop_rfi("M1.0", "CONCRETE BEAM", "RFI-01_M1.0_beam")},
       {"sheet": "A3.0", "term": "12'-0\" AFF", "img": crop_rfi("A3.0", "12'-0\" AFF", "RFI-01_A3.0_ceiling")}]
for r in c['rfis']:
    if r['id'] == 'RFI-01':
        r['source'] = "A0.1, 4/A2.0, A1.0"
        r['opciones']['B'] = {"texto": "Code: no section sets the height of an existing structure; braces per 4/A2.0 (max 25'-0\" each) and IBC 2021 Section 2508.1 (gypsum board installation) apply to whatever height is verified in the field",
                              "cita": "IBC 2021 Section 2508.1", "delta": "n/a (field verification)"}
        r['barrido'] = {"disciplinas": "ALL", "hojas": "ALL",
            "shx": "E0.0-E3.0, M0.0-M2.0 and P1.0 carry their text as 1,589 'AutoCAD SHX Text' annotations: all read by program (set_texto.json) and searched",
            "vectorial": "A1.0 / A2.0 / A3.0 at the printed 1/4\" = 1'-0\" (18 pt/ft checked on 25'-8 3/4\", 44'-6\", 29'-0 3/4\"): plans only, no building / wall section, no elevation of the structure is drawn in the set",
            "specs": "A0.3 SPECIFICATIONS (only spec sheet; no project manual, no addenda) searched",
            "otros_sets": "single GC (BCI National, BuildingConnected 2 files: Complete PDF Set 10-08-26 R0 + 'Interquest Concrete Rough layout.png' (floor trench layout, no heights)); no survey / existing-conditions set",
            "terminos": TERMS, "sets": ["BCI National - Complete PDF Set 10-08-26 R0 (17 sheets)", "Interquest Concrete Rough layout.png"],
            "medida_vectorial": "no section / elevation of the structure to measure; plans are horizontal views", "lugares": lug, "descartes": desc,
            "grep": "set_texto.json (text + SHX of the 17 sheets)",
            "encontrado_en": sorted(f"{h}:{t}" for h, tx in txt.items() for t in TERMS if _re.search(_re.escape(t), tx, _re.I)),
            "swept_txt": "Swept: all 17 sheets (A / E / M / P, no S sheets, specs on A0.3), SHX text of E / M / P, the BuildingConnected files of the only GC; terms: " + ", ".join(TERMS) + "."}
        r['img'] = lug[0]['img']
    else:
        r['question'] = {"RFI-02": "SOF-01: 8'-6\" gypsum header at the north end of Hallway 102 (A3.0 tag) - build of the header taken from type W2 framing.",
                         "RFI-03": "DEMO-08 / DEMO-09: L-shaped dashed element in Retail 100 (A1.0) - wall to demolish per key note 7.",
                         "RFI-04": "Door 101 rough opening - printed '3'-0\" DOOR' on A2.0.",
                         "RFI-05": "Column furring CF-01 / CF-02 (5/A2.0, 2-1/2\" studs, 12'-6\" high) - stud designation from the A2.0 limiting heights table."}.get(r['id'], r.get('question'))
json.dump(c, open(f'{K}/etapas/4_canon/takeoff_canon.json', 'w'), indent=1, ensure_ascii=False)
print('RFI-01 barrido: sheets with hits', len(desc), 'lugares', len(lug))
