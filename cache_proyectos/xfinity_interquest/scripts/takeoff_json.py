"""Builds <K>/takeoff.json (plantilla_excel.py format) for Xfinity - Interquest, Colorado Springs, CO (BCI National) from the
resolved canon, proceso/proyecto_datos.json and the escaneo of alcances.py. TEXT ONLY for the Excel: every quantity of the Excel
comes from familias_out.json through plantilla_excel; the few figures quoted in notes are read from the canon here (no typed
quantity). Also writes the circled crop of every Review Item (etapas/4_canon/img/review/RI-0n_*.png, re-opened after writing).
Use: python3 bitacora.py run scripts/takeoff_json.py <tools_dir>"""
import json, os, re, sys
sys.path.insert(0, sys.argv[1])
import plantilla_excel
import pymupdf as fitz
from PIL import Image, ImageDraw
K = os.environ.get("K") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C4 = os.path.join(K, "etapas", "4_canon")
c = json.load(open(os.path.join(C4, "takeoff_canon.json")))
pd = json.load(open(os.path.join(K, "proceso", "proyecto_datos.json")))["proyecto_datos"]
for x in pd:                          # image names are evidence paths, not client text (R80e.84)
    x["fuente"] = re.sub(r"\s*\(?\bimg/[\w.\-]+\.png\)?", "", str(x.get("fuente", ""))).strip()
fo = json.load(open(os.path.join(C4, "out", "familias_out.json")))
esc = json.load(open(os.path.join(K, "escaneo.json")))["alcances"]
reg = json.load(open(os.path.join(K, "registro.json")))
st = json.load(open(os.path.join(K, "set_texto.json")))["hojas"]
sm = json.load(open(os.path.join(K, "etapas", "SHEET_MAP.json")))
PAG = {v: int(k) for k, v in sm.items()}
doc = fitz.open(os.path.join(K, "plans", "bidset_SIN_MARKUPS.pdf"))
IMG = os.path.join(C4, "img", "review")
os.makedirs(IMG, exist_ok=True)


def crop(sheet, term, hint, name, pad=(170, 110)):
    """circled crop of the occurrence of `term` nearest to `hint` (visible frame) on `sheet`; -> file name (no path, R80e.153)."""
    p = doc[PAG[sheet] - 1]
    q = [fitz.Rect(x * p.rotation_matrix) for x in p.search_for(term)]
    for r in q:
        r.normalize()
    if not q:
        raise SystemExit(f"review crop: '{term}' not found on {sheet}")
    r = min(q, key=lambda r: abs(r.x0 - hint[0]) + abs(r.y0 - hint[1]))
    clip = fitz.Rect(r.x0 - pad[0], r.y0 - pad[1], r.x1 + pad[0], r.y1 + pad[1]) & p.rect
    pix = p.get_pixmap(dpi=130, clip=clip)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    s = pix.width / clip.width
    ImageDraw.Draw(im).ellipse([(r.x0 - clip.x0 - 14) * s, (r.y0 - clip.y0 - 10) * s, (r.x1 - clip.x0 + 14) * s,
                                (r.y1 - clip.y0 + 10) * s], outline=(255, 0, 0), width=4)
    f = os.path.join(IMG, name + ".png")
    im.save(f)
    assert Image.open(f).size[0] > 200
    return name + ".png"


def fmt(o):
    A, B = o.get("A") or {}, o.get("B") or {}
    C = o.get("C") or "____"
    return (f"(A) Drawings ({A.get('source', '')}): {A.get('texto', '')} - delta {A.get('delta', '')} | "
            f"(B) Code ({B.get('cita', 'n/a')}): {B.get('texto', '')} - delta {B.get('delta', '')} | (C) Other: {C}")


rfis, cierre = [], {}
for r in c["rfis"]:
    q = r.get("question") or r.get("pregunta")
    if r["status"] != "open":
        cierre[r["id"]] = {"pregunta": q + " - CLOSED: " + r["resolved"]["answer"],
                           "delta": ("0 (closed by user decision, option A; resolution loaded in the quantities, U-174)" if "user decision" in str(r["resolved"].get("by", "")) else "0 (closed by the plans; resolution loaded in the quantities)")}
        continue
    o = json.loads(json.dumps(r["opciones"]))
    terms = list(dict.fromkeys((r.get("barrido") or {}).get("terminos", []) + ["DECK", "JOIST", "STRUCTURE", "B.O.", "BOTTOM OF", "ROOF", "CLG. HT", "PLENUM", "HEIGHT", "BEAM", "T.O.", "26 FT"]))
    hits = {t: [h for h in st if re.search(re.escape(t), str(st[h]), re.I)] for t in terms}
    nh = sum(len(re.findall(re.escape(t), str(st[h]), re.I)) for t in terms for h in st)
    barrido = {"hojas": "ALL", "hojas_list": sorted(st), "terminos": terms,
               "grep": f"full text of the {len(st)} sheets (set_texto.json: page text + AutoCAD SHX annotations of E / M / P) - {nh} hits; "
                       + "; ".join(f"{t}: {', '.join(v) or 'none'}" for t, v in hits.items()),
               "result": "no B.O. structure / deck / joist height printed; A0.1 '1 STORY - 26 FT' only; M1.0 'EXISTING CONCRETE BEAM ABOVE CEILING' without height"}
    barrido = dict(r.get("barrido") or {}, **barrido)    # canon search record (disciplines, SHX, specs, other sets, places, discards) + grep per term
    rfis.append({"id": r["id"], "pregunta": f"{q} - carried: {r['loaded']} (conservative value loaded). Searched: {r['source']}",
                 "delta": fmt(o) + f" | sensitivity: {r['delta']}", "opciones": o, "source": r["source"], "barrido": barrido,
                 "img": crop("A0.1", "26 FT", (2281, 1312), "RFI-01_A0.1_26FT")})

W = {w["id"]: w for w in c["walls"]}
ex = c["existing_walls_info"]
ex_lf = round(sum(e["lf"] for e in ex), 2)
ex_ids = ", ".join(e["id"] for e in ex)
lbp = next(t for t in c["trim_items"] if t["ref"] == "LB-COL-PIER")
blk = [b for b in c["blocking_items"] if "existing" in str(b.get("wall")).lower()]
br = [m for m in c["misc_items"] if m["ref"].startswith("BRACE")]
demo = [m for m in c["misc_items"] if m["ref"].startswith("DEMO")]
sof = c["soffit_header_info"]
RI = [
 ("floor_plan", "W1", None, "2/A2.0", "RI-01_2A2.0_patch_repair", ("A2.0", "PATCH AND REPAIR", (1292, 422)),
  f"Patch and repair of the existing walls to remain: 2/A2.0 WALL TYPE 1 'EXISTING DEMISING / EXTERIOR WALL TO REMAIN. PATCH AND "
  f"REPAIR AND MAINTAIN ANY EXISTING FIRE RATING (V.I.F.)' and WALL TYPE 4 'INTERIOR WALL TO REMAIN. PATCH AND REPAIR' "
  f"({len(ex)} existing walls {ex_ids}, {ex_lf} LF on plan). The area to patch is not drawn and not measurable from the drawings: "
  f"allowance by the estimator; no quantity in the Excel."),
 ("detalle", None, 1, "5/A2.0", "RI-02_5A2.0_L_bead", ("A2.0", "FINISH CORNER 'L' BEAD", (2142, 1269)),
  f"Column furring CF-01 / CF-02 (5/A2.0): 5/A2.0 draws a free-standing column with 'FINISH CORNER 'L' BEAD' at the corners; on the "
  f"plan both columns sit against the storefront pier. Conservative (larger) option loaded: the printed 'FINISH CORNER L BEAD' "
  f"also at the 2 board edges against the existing pier of each column, {lbp['ref']} {lbp['lf']:g} LF. A: as loaded / B: no L bead at the pier edges "
  f"(delta minus {lbp['lf']:g} LF of L bead)."),
 ("floor_plan", "W2", None, "4/A2.0 / A0.1", "RI-03_A0.1_26FT", ("A0.1", "26 FT", (2281, 1312)),
  f"RFI-01 CLOSED by user decision 11-nov (option A, U-174): height of the existing structure is not printed (A0.1 'HEIGHT IN STORIES: 1 STORY - 26 FT' is the only figure). "
  f"26'-0\" carried for the {sum(m.get('pcs', 0) for m in br)} braces to structure of 4/A2.0 "
  f"({round(sum(m['qty'] for m in br), 2)} LF) and for the demolished walls DEMO-01..09 "
  f"({round(sum(m['qty'] for m in demo), 2)} SF). Sensitivity kept for the estimator (RFI-01 delta): {next(r for r in c['rfis'] if r['id'] == 'RFI-01')['delta']}."),
 ("floor_plan", "W1", None, "A5.0 / 8/A2.0", "RI-04_A5.0_blocking_legend", ("A5.0", "BLOCKING LEGEND", (98, 97)),
  "Metal blocking on EXISTING walls: A5.0 blocking legend (EV-44 / EV-45 '6\" SHEET METAL BLOCKING STRAPPING FOR FIXTURE ATTACHMENT') "
  "and A2.0 key notes 5 / 6 + 8/A2.0 backing at the fire extinguishers fall on existing walls W1 to remain: "
  + "; ".join(f"{b['ref']} {b['lf']} LF on {b['wall']}" for b in blk)
  + ". Installing them requires opening and patching the existing board, not detailed (part of the patch and repair allowance)."),
 ("floor_plan", "W2", None, "A0.3 / A2.0 general note 3", "RI-05_A0.3_texture", ("A0.3", "TEXTURE", (2418, 1375)),
  "Finish of the new board: A0.3 PAINTING spec 'GYPSUM BOARD TREATMENT ... ALL PURPOSE TEXTURE FINISH OR EQUAL' vs A2.0 general "
  "note 3 'TAPED, SANDED SMOOTH TO A \"LEVEL 4\" FINISH'. Drawings govern over the specs: Level 4 smooth loaded (compound and tape by "
  "yield); a texture finish, if required, would be an add by the estimator."),
 ("detalle", None, 2, "1/A3.0", "RI-06_A3.0_SOF-01_8-6", ("A3.0", "8'-6\" AFF", (432, 1556)),
  f"SOF-01 gyp. bd. header 8'-6\" AFF at the north end of Hallway 102 (A3.0 tag, where A1.0 removes DEMO-01): no soffit / header "
  f"detail printed; built as a framed box with type W2 framing (2/A2.0), underside {sof['area_sf']} SF + storage face to 10'-6\" + "
  f"hallway face to 9'-6\" (RFI-02 closed by the plans). Estimator to confirm the framing method."),
 ("floor_plan", "DEMO", None, "A1.0 demolition note 18", "RI-07_A1.0_temporary_barriers", ("A1.0", "NON-COMBUSTIBLE", (2300, 930)),
  "A1.0 demolition note 18: temporary non-combustible construction barriers 'where required' by the governing fire authority "
  "(full height floor to ceiling, studs at 24\" o.c. with 5/8\" Type X, non-combustible access door): conditional note, no "
  "location or length drawn on any sheet - nothing loaded; allowance by the estimator if the fire authority asks for barriers."),
 ("detalle", None, 3, "4/A2.0", "RI-08_4A2.0_brace", ("A2.0", "MAXIMUM LENGTH OF BRACE", (1700, 1450)),
  "Kicker braces 4/A2.0: each brace is 19.09 ft long ((26.0 - 12.5) x 1.414, RFI-01) and 4/A2.0 draws no splice: buy one 20 ft "
  "stick per brace (5 sticks). The 'Pieces to buy' column of the Material Summary divides the LF by the stud stick length of the Inputs "
  "(14 ft, chosen for the 12'-6\" wall studs); for the brace row read 5 sticks of 20 ft."),
]
revisar = []
for f, t, o, h, nm, (sh, term, hint), txt in RI:
    it = {"fase": f, "punto": txt + f" Source {h}.", "hoja_detalle": h, "imagen": crop(sh, term, hint, nm)}
    if t:
        it["type"] = t
    if o:
        it["orden_plano"] = o
    revisar.append(it)

hojas = [
 {"categoria": "cover / index", "estado": "reviewed", "hojas": "A0.1 title sheet + sheet index (17 sheets A0.1-A5.0, E0.0-E3.0, M0.0-M2.0, P1.0), A0.2 ADA accessibility details (mounting heights; no framing detail)"},
 {"categoria": "code analysis", "estado": "reviewed", "hojas": "A0.1 project information / building data / applicable codes: 2021 IBC, V-B fully sprinklered (existing), use group M (existing A-2), 1,798 SF leased, 1 story - 26 ft, 24 occupants"},
 {"categoria": "general notes", "estado": "reviewed", "hojas": "A0.1 general notes 1-7 (note 7 access doors / panels as required), A1.0 general demolition notes 1-25, A2.0 partition plan general notes 1-3 (Level 4), A3.0 RCP general notes 1-4 (no access hatches in gyp. bd. ceilings)"},
 {"categoria": "demolition + notes", "estado": "reviewed", "hojas": "A1.0 demolition floor plan + key notes (key 7 dashed walls removed = DEMO-01..09; keys 14 / 15 ceiling finishes / tiles; key 16 existing gyp. bd. ceiling to remain; note 18 temporary barriers)"},
 {"categoria": "specs", "estado": "reviewed", "hojas": "A0.3 specifications: lightgage framing (metal studs as shown), gypsum board 5/8\" Type X, joint sealants, hollow metal frames (3 anchors per jamb), painting / board treatment (texture finish), acoustical ceilings; no project manual"},
 {"categoria": "partition types + details", "estado": "reviewed", "hojas": "A2.0 2/A2.0 wall types W1 / W2 / W2A / W3 / W4, wall legend, interior wall limiting heights table, 3/A2.0 base, 4/A2.0 top / brace to structure, 5/A2.0 column furring, 6/A2.0 connection at demising, 7/A2.0 door head / jamb, 8/A2.0 backing"},
 {"categoria": "floor plans", "estado": "reviewed", "hojas": "A2.0 1/A2.0 partition plan (tags W1, W2, W4; dimensions; key notes 1-13), A4.0 fixture & finish plan"},
 {"categoria": "RCP", "estado": "reviewed", "hojas": "A3.0 reflected ceiling plan 1/A3.0 (Retail 2x4 ACT 12'-0\", Storage 2x4 ACT 10'-0\", Hallway / Toilets existing gyp. bd. 9'-0\", gyp. bd. 8'-6\" header, Landlord Room N.I.C.), legend, 2/A3.0 ceiling spans, 3/A3.0 suspended acoustical ceiling, 4/A3.0 light fixture at suspended ceiling"},
 {"categoria": "elevations / sections", "estado": "reviewed", "hojas": "A5.0 interior elevations (9/A5.0 retail west wall = W2 line '12'-0\" TO B.O. CEILING'); no building / wall sections in the set besides the A2.0 / A3.0 details"},
 {"categoria": "enlarged / interior elevations", "estado": "reviewed", "hojas": "A5.0 interior elevations & enlarged toilet plan, blocking legend (EV-44 / EV-45 6\" sheet metal strapping, EV-10-6 3/4\" plywood)"},
 {"categoria": "schedules", "estado": "reviewed", "hojas": "A2.0 door schedule + hardware groups, A4.0 room finish schedule (ceiling heights), A2.0 interior wall limiting heights table"},
 {"categoria": "structural", "estado": "reviewed - none in the set", "hojas": "no S sheets in the set (A0.1 sheet index); structure height not printed (RFI-01 closed by user decision, option A 26'-0\", U-174)"},
 {"categoria": "MEP", "estado": "reviewed", "hojas": "E0.0 symbols, E1.0 lighting, E2.0 power / low voltage, E2.1 fixture elevations, E3.0 electrical specifications (access panel 'as appropriate', none located); M0.0, M1.0 HVAC plan (lay-in devices in ACT, existing concrete beam above ceiling), M2.0; P1.0 plumbing ('no plumbing allowed within tenant demising walls'): no framed opening or backing in our scope; ducts EXCLUDED by standing order"},
]


def cita(alc):
    s = sorted({h["hoja"] for h in esc[alc]["hallazgos"]})
    return ("PDF mentions: " + ", ".join(s) + ". ") if s else ""


ALC = [
 ("ALC-01", "CUANTIFICADO", "Type W2 (2/A2.0): 5/8\" Type X both sides over 3-5/8\" studs from slab to 6\" above ceiling, 362S125-33 (20 ga) @ 16\" o.c. per the A2.0 interior wall limiting heights table (W2-01, W2-02); column furring CF-01 / CF-02 2-1/2\" studs 250S125-43 @ 16\" (5/A2.0, table); A0.3 lightgage framing. W1 / W4 existing to remain (not quantified); W2A / W3 legend only. A1.0 demolition note 18 temporary non-combustible construction barriers (studs @ 24\" o.c. with 5/8\" Type X): conditional note with no location or extent drawn on any sheet - not quantified, Review Item 7 (allowance by the estimator). " + cita("ALC-01")),
 ("ALC-02", "NO APLICA", "No exterior wall framing: A2.0 'EXTERIOR WALL TO REMAIN' is the 2/A2.0 WALL TYPE 1 existing demising / exterior wall (existing shell). " + cita("ALC-02")),
 ("ALC-03", "NO APLICA", "No parapet framing in the set (existing 1-story shell, A0.1; interior tenant finish only)."),
 ("ALC-04", "CUANTIFICADO", "Bottom track (3/A2.0) and standard top track screwed to the studs each flange (4/A2.0: wall stops 6\" above ceiling, braced to structure) by stud size 3-5/8\" / 2-1/2\"; slip / deflection track NOT APPLICABLE: no wall reaches the structure (A2.0 'DEFLECTION CHECKS' is a note of the limiting heights table). " + cita("ALC-04")),
 ("ALC-05", "CUANTIFICADO", "Door 101 (3'-0\" x 7'-0\", HM frame by others) in W2-01: 7/A2.0 track head with nested 3-5/8\" stud; jambs by the stud program. A0.3 'ANCHORS PER JAMB' = HM frame anchors (by others); A0.1 / A2.0 hits are hardware / contact text. " + cita("ALC-05")),
 ("ALC-06", "NO APLICA", "No bridging / C.R. channel rows: the A2.0 limiting heights table assumes walls 'FULLY SHEATHED WITH GYPSUM BOARD ... ON BOTH SIDES' (W2 both sides), continuous bridging at 60\" o.c. only as an OPTION; A0.1 erection bracing and A1.0 note 16 shoring are temporary (GC); A3.0 lateral force bracing belongs to the ACT grid (other bid package). The 4/A2.0 kicker braces to structure are carried in their own row (metal stud brace to structure). " + cita("ALC-06")),
 ("ALC-07", "CUANTIFICADO", "5/8\" Type X gypsum board: W2 both sides, each face to its own ceiling + 6\" (2/A2.0, A2.0 wall legend, A3.0 heights); CF one side over 2-1/2\" studs (5/A2.0); SOF-01 header (A3.0); A0.3 GYPSUM BOARD 5/8\" Type X. " + cita("ALC-07")),
 ("ALC-08", "NO APLICA", "No moisture-resistant board in new work: A2.0 key note 4 (water resistant board at wet areas) applies to the restrooms, all walls existing (W4); A1.0 note 24 'moisture resistant elements' refers to existing weather-exposed elements / warranties. " + cita("ALC-08")),
 ("ALC-09", "NO APLICA", "No exterior sheathing: existing shell (A0.1); the A2.0 hit is the limiting heights table note 'without the contribution of sheathing'. " + cita("ALC-09")),
 ("ALC-10", "NO APLICA", "EXCLUDED - wood (Div. 06), no RFI: A2.0 key note 10 server racks on 3/4\" FRT plywood (and 7/A2.0 / 8/A2.0 F.R.T. wood blocking), A4.0 / A5.0 EV-10-6 3/4\" plywood, A0.1 abbreviation PLYWD; the heading of the A2.0 limiting heights table ('... SHEATHED WITH GYPSUM BOARD OR PLYWOOD ON BOTH SIDES') is the design basis of the table, not a material of this project. " + cita("ALC-10")),
 ("ALC-11", "CUANTIFICADO", f"Only new gypsum board ceiling element = the SOF-01 header underside {sof['area_sf']} SF (A3.0 'GYP. BD. 8'-6\" AFF', no 'EXISTING'), carried with SOF-01; A3.0 legend '5/8\" TYPE X GYPSUM BOARD CEILING'. Hallway 102 / Toilets 103-104 tagged EXISTING with 'GYP. BD. 9'-0\" AFF' on A3.0, to remain (A1.0 key 16): EXCLUDED markups on A3.0. " + cita("ALC-11")),
 ("ALC-12", "NO APLICA", "No gypsum ceiling suspension system: A0.3 12 ga hanger wires and A3.0 3/A3.0 / 4/A3.0 belong to the suspended acoustical ceilings (ACT, other bid package); A4.0 'HANGERS' = file folders. " + cita("ALC-12")),
 ("ALC-13", "CUANTIFICADO", "SOF-01 gyp. bd. header 8'-6\" AFF at the north end of Hallway 102 (A3.0), framed as type W2 (2/A2.0, RFI-02 closed): track, studs and 5/8\" Type X board rows + corner bead. A1.0 key 13 storefront bulkhead is existing to remain. " + cita("ALC-13")),
 ("ALC-14", "NO APLICA", "No canopy / marquee in the set (A0.1-A5.0)."),
 ("ALC-15", "CUANTIFICADO", "Column furring CF-01 / CF-02 at the two existing columns at the storefront (5/A2.0 NON-RATED COLUMN FURRING, A2.0 key note 1): 2-1/2\" studs, 5/8\" Type X, L bead at the corners. " + cita("ALC-15")),
 ("ALC-16", "CUANTIFICADO", "Metal blocking: A5.0 blocking legend EV-44 / EV-45 6\" sheet metal blocking strapping (A4.0 locations) and A2.0 key notes 5 / 6 + 8/A2.0 backing at the fire extinguishers, the GF-14496 graphic frame on W2 (A4.0 key note 1, 8/A2.0 16 ga track + 16 ga studs) and the high-low drinking fountain (11/A5.0, R-ALC-02); items: " + "; ".join(f"{b['ref']} {b['lf']} LF" for b in c['blocking_items']) + ". F.R.T. wood blocking (7/A2.0, A4.0 key 13) and plywood EXCLUDED (Div. 06); A2.0 table 'bridging / blocking' is a design option. " + cita("ALC-16")),
 ("ALC-17", "NO APLICA", "No framed opening: A0.1 general note 7 'provide and locate access doors / panels ... as required' - none located on the drawings; A3.0 general note 4 no access hatches in gyp. bd. ceilings without owner approval; A1.0 note 18c is the access door of a temporary barrier; ducts / air devices EXCLUDED (estimator standing order). " + cita("ALC-17")),
 ("ALC-18", "CUANTIFICADO", "Metal corner bead 6/A2.0 (W2 / demising junction) and at the SOF-01 header edges; L bead 5/A2.0 at the column furring; A0.3 TRIM manufacturer standard beaded metal trim. No control joint drawn ('CJ' abbreviation only, A0.1); longest new run 10.64 ft. " + cita("ALC-18")),
 ("ALC-19", "NO APLICA", "EXCLUDED - acoustical sealant and sound attenuation (estimator standing order, all projects); W2 drawn with the plain hatch (no sound batt)."),
 ("ALC-20", "NO APLICA", "No FRP / cement board in our scope: FRP-1 (A4.0 / A5.0) at the existing toilet rooms and storage existing walls = finish trade. " + cita("ALC-20")),
 ("ALC-21", "NO APLICA", "No shaft wall / area separation wall in the set (2/A2.0 types W1-W4 only)."),
 ("ALC-22", "NO APLICA", "No new rated assembly: W2 is non-rated (2/A2.0); W1 'maintain any existing fire rating (V.I.F.)' = existing; A1.0 note 21 abandoned penetrations of existing fire rated walls (patch, allowance). Type X board as printed. " + cita("ALC-22")),
 ("ALC-23", "NO APLICA", "No ballistic, lead-lined or abuse-resistant panel in the set (2/A2.0 wall types, A0.3 specifications)."),
 ("ALC-24", "CUANTIFICADO", "Level 4 finish printed: A2.0 general note 3 'TAPED, SANDED SMOOTH TO A \"LEVEL 4\" FINISH'; joint compound and tape by yield (Review Item: A0.3 texture finish vs Level 4). " + cita("ALC-24")),
]
NOMB = {r["id"]: r.get("ubicacion") for r in reg["renglones"]}
alcances = [{"id": i, "nombre": NOMB.get(i, i), "estado": e, "nota": x.strip()} for i, e, x in ALC]
extra = [
 ("ACT ceilings and grid", "EXCLUDED - 2x4 ACT ceilings, new grid / existing grid and tiles (A3.0, A0.3), seismic / lateral bracing of the grid (3/A3.0, 4/A3.0): other bid package."),
 ("Painting", "EXCLUDED - painting (A0.3 painting spec, A4.0 finish schedule): other bid package."),
 ("Insulation", "EXCLUDED - insulation not in scope (estimator standing order); W2 drawn with the plain hatch (no sound batt, A2.0 wall legend)."),
 ("Wood / F.R.T. blocking and plywood (Div. 06)", "EXCLUDED - Div. 06: 3/4\" FRT plywood for the server racks (A2.0 key note 10), F.R.T. wood blocking 7/A2.0 and 8/A2.0, A4.0 key 13 F.R. blocking, A5.0 EV-10-6 3/4\" plywood."),
 ("Fasteners", "EXCLUDED - all fasteners (estimator standing order): 3/A2.0 power-driven fasteners, 4/A2.0 #8 sheet metal screws, 8/A2.0 screws, drywall / framing screws."),
 ("Acoustical sealant", "EXCLUDED - acoustical sealant (estimator standing order, all projects)."),
 ("Doors, frames and hardware", "EXCLUDED - doors, hollow metal frames and hardware (A2.0 door schedule / hardware groups, A0.3): other trades."),
 ("Storefront", "EXCLUDED - existing aluminum storefront and door 100 (A2.0 door schedule): other trade."),
 ("MEP", "EXCLUDED - electrical, mechanical, plumbing work (E / M / P sheets); recessed boxes in W2 by the electrician."),
 ("Ducts and air devices", "EXCLUDED - ducts and framed openings for air devices (estimator standing order; M1.0 devices are lay-in in ACT)."),
 ("Existing ceiling demolition", "EXCLUDED - " + c["demo_ceiling_excluded"]["why"].replace("R-ALC-05", "estimator standing rule for existing ceilings without type") + "."),
 ("Existing walls patch and repair (allowance)", f"EXCLUDED from the quantities - allowance by the estimator (Review Item): 2/A2.0 W1 / W4 'PATCH AND REPAIR' on {len(ex)} existing walls, area not measurable."),
 ("Existing walls W1 / W4 to remain (not quantified)", f"NOT QUANTIFIED - existing construction to remain (2/A2.0 WALL TYPE 1 / WALL TYPE 4, A2.0 wall legend grey): " + "; ".join(f"{e['id']} {e['lf']} LF" for e in ex) + f" (total {ex_lf} LF on plan)."),
 ("Landlord room", "EXCLUDED - Landlord room (N.I.C.) not in contract (A1.0 / A2.0 / A3.0 label '(N.I.C.)')."),
 ("Braces to structure (4/A2.0)", f"QUANTIFIED - 4/A2.0 'BRACE TO STRUCTURE, ALTERNATE SIDES ... METAL STUDS AT 8'-0\" O.C. MAX ... 3 5/8\" 20 GA. MIN.': " + "; ".join(f"{m['ref']} {m['qty']} LF ({m['pcs']} pcs)" for m in br) + "; length at 45 deg to the 26'-0\" carried (RFI-01 closed by user decision, U-174)."),
 ("Demolition of gypsum board and metal framing", f"QUANTIFIED - A1.0 key 7 dashed walls DEMO-01..09: SF = LF x H per element (no layers), H = 26'-0\" conservative (A0.1; RFI-01 closed by user decision 11-nov, option A, U-174), total {round(sum(m['qty'] for m in demo), 2)} SF."),
]
for k, (n, x) in enumerate(extra, 1):
    alcances.append({"id": f"ALC-E{k:02d}", "nombre": n, "estado": "CUANTIFICADO" if x.startswith(("QUANTIFIED", "INCLUDED")) else "NO APLICA", "nota": x})
barrido = [
 {"item": "header", "specs": "found 7/A2.0 TYPICAL HEAD DETAIL (JAMB SIM): 3-5/8\" metal track + nested 3-5/8\" stud over the HM frame (door 101)", "schedule": "found A2.0 door schedule (door 101 new in W2-01; 100 / 102-104 existing)", "estructural": "none: no S sheets in the set"},
 {"item": "deflection clips", "specs": "none: 4/A2.0 wall to 6\" above ceiling, top track screwed to studs, braced to structure (no slip / deflection track)", "schedule": "none", "estructural": "none: no S sheets"},
 {"item": "bracing", "specs": "found 4/A2.0 brace to structure, alternate sides, metal studs @ 8'-0\" o.c. max, 3 5/8\" 20 ga min, max length 25'-0\"", "schedule": "none: no bracing schedule", "estructural": "none: no S sheets; structure height not printed (RFI-01 closed by user decision, option A 26'-0\", U-174)"},
 {"item": "bridging", "specs": "none: A2.0 limiting heights table - fully sheathed both sides, bridging at 60\" only as an option; 2/A2.0-8/A2.0 print no bridging row", "schedule": "none", "estructural": "none"},
 {"item": "blocking", "specs": "found A5.0 blocking legend (EV-44 / EV-45 6\" sheet metal strapping) + 8/A2.0; F.R.T. wood blocking 7/A2.0 / 8/A2.0 EXCLUDED", "schedule": "found A4.0 EV fixture tags / A5.0 legend", "estructural": "none"},
 {"item": "backing", "specs": "found 8/A2.0 backing at the fire extinguishers (A2.0 key notes 5 / 6)", "schedule": "none", "estructural": "none"},
]
td = {
 "proyecto": "Xfinity - Interquest (Branded Partner), 1333 Interquest Pkwy., Lot #11, Colorado Springs, CO 80921 - GC BCI National",
 "bid_set": "Robert F. Vanney, Architect - Comm. 81-2116 'Complete PDF Set 10-08-26 R0': 17 sheets A0.1-A5.0, E0.0-E3.0, M0.0-M2.0, P1.0, Bid / Landlord / Permit Issue 10/08/2026; no addenda; clean copy without annotations",
 "fecha": "2026-11-11",
 "inputs": {"waste_metal": 0.15, "waste_no_metal": 0.06, "sheet_w_ft": 4, "sheet_l_ft": 12, "stud_stock_ft": 14,
            "track_stock_ft": 10, "plan_scale_pt_per_ft": c["constants"]["plan_scale_pt_per_ft"]["value"],
            "bod_ft": c["constants"]["deck_heights"]["value"]},
 "inputs_notas": {"bod_ft": "Structure height NOT printed on any sheet: 26'-0\" = A0.1 'HEIGHT IN STORIES: 1 STORY - 26 FT' carried as the conservative value for the 4/A2.0 braces and the demolished wall height (RFI-01 closed by user decision 11-nov, option A, U-174). Wall heights per wall in the Partition Takeoff (ceiling + 6\", 2/A2.0).",
                  "plan_scale_pt_per_ft": "A1.0 / A2.0 / A3.0 1/4\" = 1'-0\" (18 pt/ft, checked on the printed 25'-8 3/4\", 18'-6 3/4\", 44'-6\" and 29'-0 3/4\" of A2.0).",
                  "stud_stock_ft": "14 ft sticks: the W2 / CF studs are 12'-6\" long (ceiling 12'-0\" + 6\", 2/A2.0) and do not come out of a 12 ft stick.",
                  "drywall_screws_per_sf": "YIELD; fasteners EXCLUDED in this project (estimator standing order)."},
 "type_order": ["W2", "CF"],
 "walls": [], "materials": [],
 "rfis": rfis, "rfi_cierre": cierre, "revisar": plantilla_excel.ordenar_revisar(revisar), "alcances": alcances,
 "proyecto_datos": pd, "hojas_revisadas": hojas, "barrido_no_dibujado": barrido,
}
json.dump(td, open(os.path.join(K, "takeoff.json"), "w"), indent=1, ensure_ascii=False)
print("rfis open", len(rfis), "closed", len(cierre), "revisar", len(revisar), "alcances", len(alcances))
