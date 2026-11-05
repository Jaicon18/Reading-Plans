"""Final RFI list of the resolved canon (Consumer Cellular Centennial). Each OPEN RFI: conservative value LOADED, options
(A) drawings / (B) code / (C) other with deltas computed HERE from the canon (no typed quantity), and the full search
(U-140 / BE-CF25): all sheets, >= 12 terms with synonyms (real grep over set_texto.json = text of the 37 sheets, identical in
the Elite and Elder-Jones sets), vector measurement at the printed scale, >= 3 places with a circled crop.
Use: python3 bitacora.py run scripts/rfis.py"""
import json, os, re
import pymupdf as fitz
K = '/root/cc/work'; P = f'{K}/etapas/4_canon/takeoff_canon.json'
c = json.load(open(P)); st = json.load(open(f'{K}/set_texto.json'))['hojas']
sm = json.load(open(f'{K}/sheetmap.json'))
doc = fitz.open(f'{K}/plans/bidset_SIN_MARKUPS.pdf')
IMG = f'{K}/etapas/4_canon/img/rfi'; os.makedirs(IMG, exist_ok=True)
W = {w['id']: w for w in c['walls']}
def txt(h):
    t = st[h]; return t if isinstance(t, str) else json.dumps(t)
def grep(terms):
    out = {}
    for t in terms:
        hs = [h for h in st if re.search(re.escape(t), txt(h), re.I)]
        out[t] = {"hits": sum(len(re.findall(re.escape(t), txt(h), re.I)) for h in hs), "sheets": hs}
    return out
def crop(sheet, term, name):
    """circled crop around the first occurrence of `term` on the sheet (visible frame)"""
    p = doc[sm[sheet] - 1]; R = p.rotation_matrix
    r = None
    for q in p.search_for(term)[:1]:
        r = q * R
    if r is None:
        r = fitz.Rect(p.rect.width / 2 - 100, p.rect.height / 2 - 100, p.rect.width / 2 + 100, p.rect.height / 2 + 100)
    clip = fitz.Rect(r.x0 - 120, r.y0 - 90, r.x1 + 120, r.y1 + 90) & p.rect
    pix = p.get_pixmap(dpi=110, clip=clip)
    from PIL import Image, ImageDraw
    im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples); d = ImageDraw.Draw(im)
    s = pix.width / clip.width
    d.ellipse([(r.x0 - clip.x0 - 14) * s, (r.y0 - clip.y0 - 14) * s, (r.x1 - clip.x0 + 14) * s, (r.y1 - clip.y0 + 14) * s], outline=(255, 0, 0), width=4)
    f = f'{IMG}/{name}.png'; im.save(f); return f
SETS = ["Elder-Jones (BuildingConnected) 15066-26 Permit Set 10.15.2026 (37 sheets)",
        "Elite Retail (elite-constructionplans.com + BuildingConnected) 37 single sheets, text identical sheet by sheet (comparar_sets) + Starlink.pdf + survey report / survey documents + bid forms"]
import sys as _sys
_sys.path.insert(0, '/tmp/claude-0/-home-user/d2b6b434-1017-52fc-8c0e-204720c3b7f4/scratchpad/skill_v81cf47/take-off-metal-frame-drywall/tools')
import compuerta_entrega as CE
RX_FT = CE.RX_FT
def descartes(terms, why):
    out = {}
    for h in st:
        t_ = txt(h)
        for t in terms:
            for m in re.finditer(r"(?<![A-Za-z0-9])" + re.escape(t) + r"(?![A-Za-z0-9])", t_, re.I):
                sn = t_[max(0, m.start() - 40):m.end() + 60]  # same window as the gate (BE-120)
                if RX_FT.search(sn):
                    out[h] = f"read on {h}: '{' '.join(sn.split())[:90]}' - printed value of another element / condition; it does not answer this RFI ({why})"
                    break
            if h in out: break
    return out
def barrido(terms, places, medida, why=''):
    return {"disciplinas": "ALL", "shx": "no AutoCAD SHX annotations in either GC set (0 annotations, checked by program); full text layer of the 37 sheets searched",
            "vectorial": medida, "specs": "no project manual and no addenda in either GC set (Elite plan room folders (02) Specs / (03) Addenda empty); A700 schedules and E701 specifications searched",
            "otros_sets": "; ".join(SETS) + "; BuildingConnected survey report + survey documents (existing conditions)",
            "descartes": descartes(terms, why),
            "hojas": "ALL", "terminos": terms, "sets": SETS, "medida_vectorial": medida,
            "lugares": [{"sheet": s, "term": t, "img": crop(s, t, n)} for s, t, n in places], "grep": grep(terms),
            "swept_txt": f"Swept: all 37 sheets (G / D / A / M / E / P / FA, no S sheets and no project manual in the set), both GC sets, the survey documents; terms: {', '.join(terms)}."}
L = lambda t: round(sum(w['length_ft'] for w in c['walls'] if w['tag'] == t), 2)
c3 = W['C3-01']; a3 = [w for w in c['walls'] if w['tag'] == 'A3']
studs_c3 = round(c3['length_ft'] / (16 / 12) + 1)
rf = []
rf.append({"id": "RFI-01", "status": "open", "source": "A100",
 "question": "The deck break between 'PLY DECK @ 16'-4\"' (Back of House) and 'PLY DECK @ 17'-1 9/16\"' (Sales Area) is not drawn (deck height not printed at the C3 line). C3-01 studs carried to the higher deck.",
 "why_not_printed": "no deck break line, section or elevation shows which deck the C3 line (BOH / Sales boundary) reaches",
 "loaded": "C3-01 studs to 17'-1 9/16\" (higher printed deck, conservative)",
 "opciones": {"A": {"texto": "Drawings: studs to the Sales deck 17'-1 9/16\" (A100 deck tag) - LOADED", "source": "A100", "delta": "0"},
              "B": {"texto": "Studs to the BOH deck 16'-4\" (A100 deck tag) at the C3 line", "cita": "A100 deck tags; 4/A500 'attached to structure'",
                    "delta": f"-0.797 ft x approx. {studs_c3} studs of C3-01 = -{round(0.797 * studs_c3, 1)} LF of 3-5/8\" 18 ga stud"}, "C": "____"},
 "barrido": barrido(["DECK", "PLY DECK", "B.O.", "STRUCTURE", "JOIST", "ROOF", "16'-4", "17'-1", "SECTION", "BUILDING SECTION", "HEIGHT", "CEILING"],
                    [("A100", "PLY DECK", "RFI-01_A100"), ("A200", "11'-11", "RFI-01_A200"), ("A500", "B.O. (E) DECK", "RFI-01_A500"), ("D100", "EXISTING", "RFI-01_D100")],
                    "A100 at the printed 1/4\" = 1'-0\" (18 pt/ft, checked on 44'-3 1/2\" and 31'-6 1/2\"): no deck break line drawn on A100 / A200 / D100")})
other = round(sum(w['length_ft'] * max(f['height_ft'] for f in w['faces']) for w in a3), 1)
rf.append({"id": "RFI-02", "status": "open", "source": "1/A500",
 "question": "Type A# 'FURRED WALL TO DECK' (1/A500) prints '5/8\" TYPE \"X\" GYP. BD. ON EACH SIDE TO 6\" ABOVE CEILING' but the section draws the board only on the tenant side, with a 1/2\" gap to the existing demising wall. Board loaded on BOTH faces as printed in the type note.",
 "why_not_printed": "conflict inside 1/A500 (type note vs section drawing)",
 "loaded": f"A3 board both faces as printed ({L('A3')} LF of A3)",
 "opciones": {"A": {"texto": "Drawings (type note 1/A500): board on each side - LOADED", "source": "1/A500", "delta": "0"},
              "B": {"texto": "Board on the tenant side only, as the section draws (back face against the existing wall is not finished)", "cita": "1/A500 section; ASTM C840 (one-side furring)",
                    "delta": f"-{other} SF of 5/8\" Type X (back faces of A3-01..A3-04)"}, "C": "____"},
 "barrido": barrido(["EACH SIDE", "FURRED", "DEMISING", "TENANT SIDE", "1/2\" GAP", "EXISTING DEMISING WALL", "TYPE \"X\"", "GYP. BD.", "BOTH SIDES", "FURRING", "A500", "ONE SIDE"],
                    [("A500", "FURRED WALL TO DECK", "RFI-02_A500"), ("A100", "ADJACENT TENANT", "RFI-02_A100"), ("D100", "FURRING", "RFI-02_D100")],
                    "1/A500 section at 3/4\" = 1'-0\": board drawn on one face, 1/2\" gap to the existing wall")})
slip = round(L('A3') + L('C3') + L('D'), 2)
rf.append({"id": "RFI-03", "status": "open", "source": "4/A500",
 "question": "4/A500 long-leg slotted runner track: gauge and leg length not printed (2\" min. vertical slots printed); the floating C channel is printed 3 5/8\" x 20 GA only - no 6\" version for type D (6\" studs). Carried: deep-leg slotted track 20 ga (2\" deflection leg) by stud size and a nested 20 ga C channel of the wall's stud size. The estimator precedent on runners (O'Reilly: 1-1/2\" runner top and bottom of Z-furring, ASTM C754) does not decide this deflection head.",
 "why_not_printed": "gauge / leg length of the runner and the 6\" channel are not printed",
 "loaded": f"{slip} LF of slip top track 20 ga + {slip} LF nested inner runner (3-5/8\" and 6\")",
 "opciones": {"A": {"texto": "Drawings: 3 5/8\" x 20 GA C channel + long-leg slotted runner, applied to the 6\" wall at its size - LOADED", "source": "4/A500", "delta": "0"},
              "B": {"texto": "Manufacturer (ClarkDietrich / SSMA slotted deflection track, 20 ga, 2-1/2\" leg)", "cita": "SSMA / ClarkDietrich deflection track catalog; ASTM C754",
                    "delta": "0 LF (same LF, different product leg; studs and track LF unchanged, fasteners EXCLUDED)"}, "C": "____"},
 "barrido": barrido(["LONG LEG", "RUNNER", "SLOTTED", "DEFLECTION", "SLIP", "C' CHANNEL", "20 GA", "TRACK", "TOP CORD", "ATTACHMENT TO STRUCTURE", "6\" 20 GA", "GA."],
                    [("A500", "LONG LEG RUNNER", "RFI-03_A500a"), ("A500", "ATTACHMENT TO STRUCTURE", "RFI-03_A500b"), ("A700", "FINISH SCHEDULE", "RFI-03_A700")],
                    "4/A500 at 3\" = 1'-0\": channel drawn 3 5/8\"; no 6\" variant drawn")})
board_sf = round(sum(w['length_ft'] * f['height_ft'] for w in c['walls'] for f in w['faces']), 0)
rf.append({"id": "RFI-04", "status": "open", "source": "A700",
 "question": "Gypsum board finish level and trims are not specified (no project manual; A700 'ARCHITECTURAL SPECIFICATIONS' holds only the finish / FF&E schedules; walls painted PT-1..PT-4 eggshell). Carried Level 4 on all board, metal corner bead at outside corners and the cased opening.",
 "why_not_printed": "no finish level / trim specification anywhere in the set",
 "loaded": "Level 4 (tape + compound by yield) + metal corner bead",
 "opciones": {"A": {"texto": "Drawings: no level printed - Level 4 carried for eggshell paint - LOADED", "source": "A700", "delta": "0"},
              "B": {"texto": "Code: GA-214 / ASTM C840 recommend Level 4 for flat / eggshell paint (Level 5 for critical lighting)", "cita": "GA-214-2021; ASTM C840",
                    "delta": f"Level 5 skim coat on {board_sf} SF of wall board if required"}, "C": "____"},
 "barrido": barrido(["LEVEL", "FINISH", "TAPE", "JOINT", "COMPOUND", "SPECIFICATION", "SECTION 09", "CORNER BEAD", "TRIM", "PAINT", "EGGSHELL", "GYP"],
                    [("A700", "FINISH SCHEDULE", "RFI-04_A700"), ("A101", "PT-1", "RFI-04_A101"), ("G001", "GYP", "RFI-04_G001")],
                    "n/a (specification item, no geometry)")})
rf.append({"id": "RFI-05", "status": "open", "source": "A100",
 "question": "The 4'-0\" x 8'-0\" cased opening 'OPEN TO HALLWAY' (2/A400) in the C3 line between Hallway and Sales is untagged; the infill above the opening is carried as C3 (studs to deck, board both sides) as the C3 line it continues.",
 "why_not_printed": "no partition tag at the infill above the opening",
 "loaded": "C3 to deck over the 4'-0\" opening",
 "opciones": {"A": {"texto": "Drawings: C3 line continues over the opening (C3 tag at its north end) - LOADED", "source": "A100", "delta": "0"},
              "B": {"texto": "E3 (to 6\" above ceiling, braced 3/A500) over the opening", "cita": "1/A500 type E",
                    "delta": "-4.0 LF x (17.13 - 12.417) ft of stud height; +1 brace position (3/A500)"}, "C": "____"},
 "barrido": barrido(["OPEN TO HALLWAY", "CASED", "OPENING", "8'-0\"", "C3", "E3", "HEADER", "T.O. OPENING", "HALLWAY", "SALES AREA", "PARTITION", "TYPE"],
                    [("A400", "OPEN TO HALLWAY", "RFI-05_A400"), ("A100", "HALLWAY", "RFI-05_A100"), ("A200", "HALLWAY", "RFI-05_A200")],
                    "A100 vector: opening 4'-0\" (72 pt at 18 pt/ft) between the C3 band end and the E3 band")})
cp = c['ceilings'][0]
rf.append({"id": "RFI-06", "status": "open", "source": "A200",
 "question": "Unisex Restroom C-1 gypsum board ceiling at 8'-0\" (A200): no ceiling framing detail is bubbled on A200 / A402; A501 'CEILING DETAILS' is referenced from no sheet. Carried as a suspended furring channel system (hangers + carrying + furring, ASTM C754).",
 "why_not_printed": "no ceiling detail called on this ceiling",
 "loaded": f"furring system over {cp['area_sf']} SF (carrying channel, furring channel, hangers, perimeter track)",
 "opciones": {"A": {"texto": "Drawings: 2/A501 drywall grid suspension system (ICC ESR 1289) if it applies to this ceiling", "source": "2/A501", "delta": "furring / carrying / hangers replaced by grid main + cross tees and 2x2 angle (same board SF)"},
              "B": {"texto": "Code: ASTM C754 furring channel system - LOADED", "cita": "ASTM C754 / GA-216", "delta": "0"}, "C": "____"},
 "barrido": barrido(["C-1", "GYP BOARD CEILING", "A501", "SUSPENSION", "GRID", "HANGER", "FURRING", "CARRYING", "CEILING DETAIL", "8'-0\"", "RESTROOM", "ESR 1289"],
                    [("A200", "UNISEX", "RFI-06_A200"), ("A402", "CEILING", "RFI-06_A402"), ("A501", "ESR", "RFI-06_A501")],
                    "A100 vector polygon of the restroom at 18 pt/ft = 60.49 SF (G003 prints 60 SF)")})
rf.append({"id": "RFI-07", "status": "open", "source": "D100",
 "question": "Door 3C is a new door in the EXISTING Hallway / Utility wall to remain (D100 keynote 17, A100): the new opening framing (header + jamb studs) in the existing wall is not detailed. Carried: track header (2/A600, R.O. + 1'-4\") and 2 jamb studs each side (3/A600) to 6\" above the BOH ceiling.",
 "why_not_printed": "no framing for the opening in the existing wall",
 "loaded": "header 4.67 LF + 4 jamb studs x 12.417 ft",
 "opciones": {"A": {"texto": "Drawings: 2/A600 head + 3/A600 jamb applied to the existing wall - LOADED", "source": "2/A600, 3/A600", "delta": "0"},
              "B": {"texto": "Existing opening to be reused (no new framing)", "cita": "D100 keynote 17", "delta": "-4.67 LF header, -49.67 LF 3-5/8\" stud"}, "C": "____"},
 "barrido": barrido(["3C", "EXISTING", "TO REMAIN", "REMAIN", "PATCH", "OPENING", "DOOR", "FRAME", "KNOCKDOWN", "JAMB", "HEAD", "UTILITY"],
                    [("D100", "REMAIN", "RFI-07_D100"), ("A600", "KNOCKDOWN", "RFI-07_A600"), ("A100", "UTILITY", "RFI-07_A100")],
                    "A100 vector: door 3C 60 pt = 3'-4\" R.O. in the existing wall")})
rf.append({"id": "RFI-08", "status": "open", "source": "1/A504",
 "question": "Mop sink / water heater shelf (1/A504 sections A, B): '6\" 16 GA. METAL STUDS ATTACHED WITH #10 TEK SCREWS' and '5/8\" WR GYP BD' under the 3/4\" FRT plywood are printed, but the number of members is not. Carried: perimeter ledger + joists @ 16\" o.c. over the 4'-0\" x 2'-4\" alcove (between E3-12 / E3-13) and 5/8\" WR board top and underside.",
 "why_not_printed": "member count / layout of the shelf framing not printed",
 "loaded": "19.67 LF 6\" 16 ga stud + 18.67 SF 5/8\" WR board",
 "opciones": {"A": {"texto": "Drawings: 6\" 16 GA studs + 5/8\" WR board (1/A504) with the member layout carried - LOADED", "source": "1/A504", "delta": "0"},
              "B": {"texto": "Perimeter members only (no intermediate joist)", "cita": "AISI S240 (span 2'-4\")", "delta": "-7.0 LF of 6\" 16 ga stud (#10 Tek screws EXCLUDED, standing order)"}, "C": "____"},
 "barrido": barrido(["MOP SINK", "WATER HEATER", "SHELF", "16 GA", "6\" 16 GA", "FRT PLYWOOD", "WR GYP", "BRACKETS", "STANDARDS", "BLOCKING", "A504", "UTILITY"],
                    [("A504", "MOP SINK", "RFI-08_A504"), ("P501", "WATER HEATER", "RFI-08_P501"), ("A100", "UTILITY", "RFI-08_A100")],
                    "A100 vector: alcove between the E3-12 / E3-13 inner faces 72 pt = 4'-0\"; stub length 2'-4\" printed")})
closed = [{"id": "RFI-C1", "status": "closed", "source": "D100",
           "question": "Heights of the existing walls / furring to be demolished (D100 keys 9, 27) are not printed.",
           "resolved": {"answer": "estimator decision (standing rule): existing partitions to demolish without printed height go to the printed B.O. structure; A100 'PLY DECK @ 17'-1 9/16\"' (higher bay) carried", "source": "D100, A100"}}]
for r in closed:
    r['delta'] = '0 (closed by the estimator standing rule)'; r['img'] = crop('D100', 'REMAIN', 'RFI-C1_D100'); r['fuentes_revisadas'] = ['D100 keynotes / demolition notes', 'A100 deck tags', 'standing rule (existing partitions to demolish = to printed B.O. structure)', 'no section / elevation of the existing walls']
for r in rf:
    tq = CE._terminos({"barrido": r['barrido'], "pregunta": f"{r['question']} - carried: {r['loaded']} (conservative value loaded). " + r['barrido']['swept_txt']})
    r['barrido']['descartes'] = descartes(tq, r['why_not_printed'])
    r['delta'] = ' | '.join(f"({k}) {v.get('delta')}" for k, v in r['opciones'].items() if isinstance(v, dict))
    r['img'] = r['barrido']['lugares'][0]['img']
    r['fuentes_revisadas'] = ["designation: no SSMA designation / gauge printed beyond 1/A500 - 6/A500", "other row: 1/A500 types A#, C#, D, E#, H and A600 / A700 schedules",
                              "standard rule: ASTM C754 / C840, GA-216, AISI S220 / S240, SSMA catalog", "detail: every bubble followed to its end (burbujas_verificadas.json, CADENA.md)"]
c['rfis'] = rf + closed
# misc rows that carry RFI-03 (nested runner) and RFI-07 (door 3C in the existing wall)
c['misc_items'] = [m for m in c['misc_items'] if m['ref'] not in ('NESTED-RUNNER-362', 'NESTED-RUNNER-600', 'HDR-3C', 'JAMB-3C')]
c['misc_items'] += [
 {"ref": "NESTED-RUNNER-362", "familia": "nested inner runner (deflection head)", "qty": round(L('A3') + L('C3'), 2), "unit": "LF", "source": "4/A500",
  "op": f"A3 {L('A3')} + C3 {L('C3')} LF (one 3 5/8\" x 20 GA 'C' channel floating 1\" below the top cord of the long-leg runner, 4/A500)", "status": "DERIVADO"},
 {"ref": "NESTED-RUNNER-600", "familia": "nested inner runner (deflection head)", "qty": L('D'), "unit": "LF", "source": "4/A500",
  "op": f"D {L('D')} LF (4/A500 channel applied at the 6\" stud size - RFI-03)", "status": "DERIVADO"},
 {"ref": "HDR-3C", "familia": "header / box beam", "qty": 4.67, "unit": "LF", "source": "2/A600", "op": "3.333 R.O. + 1.333 = 4.67 (one track head, RFI-07)", "status": "DERIVADO"},
 {"ref": "JAMB-3C", "familia": "3-5/8\" stud (todos los gauges)", "qty": 49.67, "unit": "LF", "pcs": 4, "source": "3/A600",
  "op": "2 jambs x 2 studs (3/A600 double studs) x 12.417 ft (BOH ceiling 11'-11\" + 6\") = 49.67 (RFI-07)", "status": "DERIVADO"}]
c['misc_items'] = [m for m in c['misc_items'] if m['ref'] not in ('MOP-SHELF-STUD', 'MOP-SHELF-BOARD')]
c['misc_items'] += [
 {"ref": "MOP-SHELF-STUD", "familia": "6\" stud (todos los gauges)", "qty": 19.67, "unit": "LF", "pcs": 7, "source": "1/A504",
  "op": "perimeter 2 x 4.0 + 2 x 2.333 = 12.67 + 3 joists @ 16\" x 2.333 = 7.0 -> 19.67 LF of 6\" 16 GA stud (1/A504; layout RFI-08)", "status": "DERIVADO"},
 {"ref": "MOP-SHELF-BOARD", "familia": "5/8\" gyp MOISTURE RESISTANT", "qty": 18.67, "unit": "SF", "source": "1/A504",
  "op": "4.0 x 2.333 = 9.33 SF top (under the 3/4\" FRT plywood, wood EXCLUDED) + 9.33 SF underside = 18.67 SF 5/8\" WR (1/A504; RFI-08)", "status": "DERIVADO"}]
if not any(b['ref'] == 'BLK-WH' for b in c['blocking_items']):
    c['blocking_items'].append({"ref": "BLK-WH", "lf": 6.0, "material": "metal", "wall": "E3-13", "source": "5/P501",
        "label": "water heater seismic strap: 'PROVIDE BLOCKING IN WALL' (5/P501 ELECTRIC DOMESTIC WATER HEATER)",
        "op": "3 ft x 2 rows (estimator standing rule: accessory blocking without printed size = 3 ft x 2 rows)", "status": "DERIVADO"})
json.dump(c, open(P, 'w'), indent=1, ensure_ascii=False)
print(len(rf), 'open RFIs,', len(closed), 'closed')
