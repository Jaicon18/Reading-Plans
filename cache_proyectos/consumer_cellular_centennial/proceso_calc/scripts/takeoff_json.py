"""Builds <K>/takeoff.json (plantilla_excel.py format) for Consumer Cellular - Centennial, CO from the resolved canon and
proceso/proyecto_datos.json. TEXT ONLY: every quantity of the Excel comes from familias_out.json through plantilla_excel.
Use: python3 bitacora.py run scripts/takeoff_json.py <tools_dir>"""
import json, os, sys
sys.path.insert(0, sys.argv[1])
import plantilla_excel
K = '/root/cc/work'
C4 = os.path.join(K, "etapas", "4_canon")
c = json.load(open(os.path.join(C4, "takeoff_canon.json")))
pd = json.load(open(os.path.join(K, "proceso", "proyecto_datos.json")))["proyecto_datos"]
for x in pd:
    x["fuente"] = str(x.get("fuente", "")).replace(" (img/a200_seal.png)", "")
    if x["campo"] == "type of project":
        x["valor"] = "Interior tenant improvement of an existing shell: new cell phone store with retail merchandise, new lighting and fixtures, minimal plumbing and mechanical (G003 project description); scope list per G000: FF&E, interior partitions and doors, ceilings, finishes, lighting, restroom, kitchenette and mop sink"
    if x["campo"] == "bid set":
        x["valor"] = "15066-26 Consumer Cellular Centennial CO, 37 sheets G000-FA101, dated 10/14/2026, sealed 10/15/2026; title blocks carry '90% SET / DESIGN INTENT ONLY / NOT FOR CONSTRUCTION'; file name of the Elder-Jones download: 'Permit Set_10.15.2026'"
        x["fuente"] = "G000 title block + drawing index; A200 seal; BuildingConnected file name"
    if x["campo"] == "stories":
        x["valor"] = "1 (single tenant suite, one floor plan A100)"; x["fuente"] = "G003, A100"
    if x["campo"] == "specs":
        x["valor"] = "No project manual in the set: A700 'ARCHITECTURAL SPECIFICATIONS' holds the finish, FF&E, plumbing fixture and lighting schedules; E701 electrical specifications"
        x["fuente"] = "A700, E701, G000 drawing index"
    if x["campo"].startswith("general contractor"):
        x["valor"] = "Elite Retail Services (Vivian Tran) - bid 11/05/2026 4:00 PM CT; Elder-Jones, Inc. (Mason Bender) - bid 11/06/2026"
        x["fuente"] = "GC data: BuildingConnected invitations 10/19 and 10/20/2026 + Elite invitation e-mail 10/16/2026 (G000 names the G.C. role only)"
    if x["campo"].startswith("bid date"):
        x["valor"] = "11/05/2026 4:00 PM CT (Elite Retail Services); 11/06/2026 (Elder-Jones, Inc.)"
        x["fuente"] = "GC data: BuildingConnected invitations; title block DATE 10/14/2026, DATE SIGNED 10/15/2026"
fo = json.load(open(os.path.join(C4, "out", "familias_out.json")))


def fmt(o):
    A, B = o.get("A") or {}, o.get("B") or {}
    C = o.get("C") or "____"
    return (f"(A) Drawings ({A.get('source', '')}): {A.get('texto', '')} - delta {A.get('delta', '')} | "
            f"(B) Code ({B.get('cita', 'n/a')}): {B.get('texto', '')} - delta {B.get('delta', '')} | (C) Other: {C or '____'}")


# rev4 (U-138 audit #11): the Level 5 delta of RFI-04 uses the REAL board total of the Material Summary (all gypsum board
# families of familias_out.json), not the gross wall faces; written back into the canon RFI text (docs read it)
import re as _re
_bt = round(sum(v for k, v in fo["familias"].items() if "gyp" in k.lower() and "EXTERIOR" not in k and "demolition" not in k.lower()), 2)
for r in c["rfis"]:
    if r["id"] == "RFI-04":
        for o_ in (r.get("resolved") or {},):
            if "answer" in o_:
                o_["answer"] = _re.sub(r"skim coat on [\d,.]+ SF", f"skim coat on {_bt:,.2f} SF (total gypsum board, Material Summary)", o_["answer"])
        ob = (r.get("opciones") or {}).get("B") or {}
        if "delta" in ob:
            ob["delta"] = _re.sub(r"skim coat on [\d,.]+ SF[^|]*", f"skim coat on {_bt:,.2f} SF of gypsum board if required", ob["delta"])
        r["delta"] = " | ".join(f"({k}) {v.get('delta')}" for k, v in (r.get("opciones") or {}).items() if isinstance(v, dict))
        if r.get("decision"):
            r["decision"] = r["resolved"]["answer"]
rfis, cierre = [], {}
for r in c["rfis"]:
    if r["status"] != "open":
        cierre[r["id"]] = {"pregunta": r["question"] + " - CLOSED: " + r["resolved"]["answer"], "delta": r.get("delta_applied") or "0 (estimator standing rule applied)"}
        continue
    o = json.loads(json.dumps(r["opciones"]))
    rfis.append({"id": r["id"], "pregunta": f"{r['question']} - carried: {r['loaded']} (conservative value loaded). " + r["barrido"]["swept_txt"],
                 "delta": fmt(o), "opciones": o, "source": r["source"], "barrido": r["barrido"],
                 "img": r["barrido"]["lugares"][0]["img"]})
cierre.update({
 "A/B-1 (door openings)": {"pregunta": "Reading A measured the E3 walls without the door gaps of 4C / 5C / 6C - CLOSED by rule: walls measured through the door R.O. (one straight line per tag), openings listed in the wall", "delta": "0 (applied: +10.0 LF E3)"},
 "A/B-2 (A3 north wall)": {"pregunta": "One wall (B) or two (A) on the north sales wall - CLOSED: two A3 tags on the line broken by the existing column (D100 key 14) = two walls; same 43.24 LF", "delta": "0"},
})
RI = [
 ("floor_plan", "A3", None, "A100 / D100",
  "A3-01 / A3-02 north sales wall stops each side of the existing column (D100 keynote 14, gap ~1'-0\"); the column is not wrapped. A: stop at the column (loaded) / B: wrap the column with the furring; delta about +4 LF of A3 and +100 SF of board.",
  "RFI-01_A100.png"),
 ("floor_plan", "E3", None, "A200 / 1/A500",
  "Type E3 walls between rooms with different ceilings (Office 9'-0\" / BOH 11'-11\", Restroom 8'-0\" / Hallway 11'-11\"): studs to the higher ceiling + 6\" and each face's board to its own ceiling + 6\" (1/A500 'TO 6\" ABOVE CEILING'). A: as loaded / B: board on both faces to the higher ceiling; delta = the lower faces x (higher - lower) ceiling.",
  "RFI-05_A200.png"),
 ("floor_plan", "DEMO", None, "D100 key 7",
  "Existing ceiling demolition of D100 keynote 7 (existing gyp. bd. and ACT ceilings, soffit and framing throughout): the extent of gypsum board vs ACT is not shown - EXCLUDED for lack of information (0 SF, estimator decision: standing rule for existing ceilings without type). Review Item: the lease area is 3,103 SF (G003) if the estimator wants an allowance.",
  "RFI-07_D100.png"),
 ("floor_plan", "EXTERIOR", None, "A300 / A301 note 2",
  "Exterior signage blocking: 'G.C. TO VERIFY AND INSTALL BLOCKING FOR EXTERIOR SIGNAGE AS REQUIRED. COORDINATE WITH LANDLORD AND SIGNAGE VENDOR' - on the existing shell, size not shown on the drawings: Review Item - allowance by the estimator (no quantity drawn).",
  "RFI-04_A101.png"),
 ("detalle", None, 1, "1/A104",
  "Logo wall blocking 1/A104: one 1'-4 1/2\" band of 20 GA metal strapping per logo wall (cleat 10 1/2\" + 3\" above and below), loaded as one LF band per wall. A: one band (loaded) / B: 3 rows of 6\" strap; delta x3 on BLK-LOGO-S / BLK-LOGO-W.",
  "RFI-04_A101.png"),
 ("floor_plan", "EXISTING", None, "D100 / A100",
  "Patch and repair of the existing demising / exterior walls to remain (D100 keynotes 3, 4 'PATCH AND REPAIR AS REQUIRED TO LIKE-NEW CONDITION'): area not measurable from the drawings - allowance by the estimator.",
  "RFI-07_D100.png"),
]
revisar = []
for f, t, o, h, txt, img in RI:
    it = {"fase": f, "punto": txt + f" Source {h}.", "hoja_detalle": h, "imagen": img}
    if t: it["type"] = t
    if o: it["orden_plano"] = o
    revisar.append(it)
hojas = [
 {"categoria": "cover / index / code", "estado": "reviewed", "hojas": "G000 cover (index, scope, project team, general notes), G001 responsibility schedule, G002 accessibility details, G003 code analysis / egress (IBC 2021, II-B, M, 3,103 SF, not sprinklered)"},
 {"categoria": "general notes", "estado": "reviewed", "hojas": "G000 general notes 1-15, A100 general notes 1-11 (note 11 water resistant board at wet areas), A102 / A103 notes (blocking as required)"},
 {"categoria": "demolition + notes", "estado": "reviewed", "hojas": "D100 existing conditions and demolition plan + keynotes 1-31 + general demolition notes; D101 trenching (not our trade)"},
 {"categoria": "specs", "estado": "reviewed", "hojas": "no project manual in the set; A700 'ARCHITECTURAL SPECIFICATIONS' = finish / FF&E / plumbing fixture / lighting schedules (no Div. 05 / 09 sections); E701 electrical specifications"},
 {"categoria": "partition types + details", "estado": "reviewed", "hojas": "A500 1/A500 partition types A#, C#, D, E#, H + details 2-6 (floor connection, top of wall bracing, attachment to structure)"},
 {"categoria": "floor plans", "estado": "reviewed", "hojas": "A100 construction floor plan (tags, dimensions, deck heights), A101 finish plan, A102 furniture plan, A103 millwork plan, A104 millwork blocking details"},
 {"categoria": "RCP", "estado": "reviewed", "hojas": "A200 reflected ceiling plan (C-1 gyp bd at the restroom 8'-0\", C-2 ACT, existing soffit 11'-9\"), A501 ceiling details"},
 {"categoria": "elevations / sections", "estado": "reviewed", "hojas": "A300 / A301 exterior elevations (existing storefront, signage blocking note)"},
 {"categoria": "enlarged / interior elevations", "estado": "reviewed", "hojas": "A400 / A401 interior elevations, A402 enlarged unisex restroom (accessories, FRP 4'-0\"), A504 mop sink details"},
 {"categoria": "schedules", "estado": "reviewed", "hojas": "A600 door schedule + head 2/A600 / jamb 3/A600, A700 finish schedule, A200 ceiling tags, A502 flooring / base, A503 slab details"},
 {"categoria": "structural", "estado": "reviewed - none in set", "hojas": "no S sheets in the set (G000 drawing index); deck heights from A100 tags"},
 {"categoria": "MEP", "estado": "reviewed", "hojas": "M101 / M102 / M501 / M601, P101 / 5/P501 (water heater blocking), E101 / E111 / E112 / E301 / E601 / E701, FA101 swept for crossings / access panels (none in gypsum); ducts EXCLUDED by standing order"},
]
EXC = "EXCLUDED - not in scope (estimator standing order, no RFI): "
alc = [
 ("ALC-01", "CUANTIFICADO", "Partition types A3 (3-5/8\" 20 ga furred wall to deck), C3 (3-5/8\" 18 ga to deck, both sides), D (6\" 20 ga to deck, both sides), E3 (3-5/8\" 18 ga to 6\" above ceiling, both sides) per 1/A500, all @ 16\" o.c.; type H not tagged on A100."),
 ("ALC-02", "NO APLICA", "No exterior wall framing: existing shell (A300 / A301, D100 keynote 4)."),
 ("ALC-03", "NO APLICA", "No parapet framing (A300 / A301 existing)."),
 ("ALC-04", "CUANTIFICADO", "Bottom track 20 ga (2/A500) by stud size; top track in two families: long-leg slotted runner track (4/A500) at A3 / C3 / D to deck + nested 3-5/8\" / 6\" x 20 ga C channel, and standard 20 ga top track (3/A500) at E3."),
 ("ALC-05", "CUANTIFICADO", "Door heads 2/A600 (track head, R.O. + 1'-4\") at doors 4C / 5C / 6C and the 4'-0\" cased opening (2/A400); door 3C in the existing wall (RFI-07); double jamb studs 3/A600 by the stud program."),
 ("ALC-06", "NO APLICA", "No bridging / C.R. channel bracing rows printed (1/A500 - 6/A500). The 3/A500 top of wall braces of type E3 (362S137-33 @ 48\" o.c. to structure, doubled for walls to 15'-0\", 3x3x3 20 ga angles) are carried in their own row (Metal stud brace to structure, see the braces row below)."),
 ("ALC-07", "CUANTIFICADO", "5/8\" Type X gypsum board per face (1/A500: each side on A#, C#, D, E#; A# both faces per its type note, RFI-02)."),
 ("ALC-08", "CUANTIFICADO", "5/8\" Type X water resistant board at the restroom, EWC niche, mop sink alcove and kitchenette faces (A100 general note 11, 1/A500 'PROVIDE WATER RESISTANT GYP. BD. AT WET LOCATIONS'); 5/8\" WR board at the mop sink shelf (1/A504)."),
 ("ALC-09", "NO APLICA", "No exterior gypsum / glass mat sheathing in the set: existing shell and storefront (A300, A301, D100 keynote 4); A100 general note 11 'or an equivalent waterproof sheathing material' refers to the water resistant board at wet areas (carried in the W.R. row)."),
 ("ALC-10", "NO APLICA", "EXCLUDED - wood (Div. 06): FRT plywood blocking at pendant lights (1/A501), 2X4 blocking between joists (6/A500), 3/4\" FRT plywood on the mop sink shelf (1/A504)."),
 ("ALC-11", "CUANTIFICADO", "C-1 gypsum board ceiling at the Unisex Restroom 8'-0\" (A200, A402), 5/8\" water resistant (A100 note 11)."),
 ("ALC-12", "CUANTIFICADO", "Restroom C-1 ceiling: 2/A501 drywall grid suspension system (ICC ESR 1289) - main tee, cross tee @ 16\" o.c., 2\" x 2\" sheet metal angle perimeter, 12 ga hanger wire @ 4'-0\" o.c. (2/A501, A200; RFI-06 closed, U-140)."),
 ("ALC-13", "NO APLICA", "No new soffit / bulkhead: storefront soffit is existing to remain (A200 'SOFFIT EXIST' 11'-9\")."),
 ("ALC-14", "NO APLICA", "No canopy / marquee framing (A300 / A301)."),
 ("ALC-15", "NO APLICA", "No column furring / wrap printed (A100, D100 keynote 14 existing column); see Review Items."),
 ("ALC-16", "CUANTIFICADO", "Metal blocking: 20 GA. metal strapping at the slat wall 2/A104, logo walls 1/A104 and kitchenette 3/A104; 20 GA track at the grab bars 5/A402; stud blocking at the restroom accessories (A402 note 4) and water heater (5/P501). iPad backing plate 4/A104 'BACKING PLATE BY G.C.' EXCLUDED (by G.C., estimator standing precedent); wood blocking EXCLUDED."),
 ("ALC-17", "NO APLICA", EXC + "framed openings for ducts / air devices; no access panel in gypsum surfaces (E701: no junction box access panels in drywall ceilings; M101 / P501 none)."),
 ("ALC-18", "CUANTIFICADO", "Metal corner bead at outside corners, the cased opening and the stub ends (no trim spec printed, RFI-04); control joints not printed: carried per ASTM C840 at runs over 30'-0\" (A3-03 44.83 LF, C3-01 35.54 LF), 49.66 LF (estimator standing precedent)."),
 ("ALC-19", "NO APLICA", "EXCLUDED in all projects (estimator standing order): acoustical sealant (2/A500) and sound attenuation; batt insulation of type D (1/A500) EXCLUDED."),
 ("ALC-20", "CUANTIFICADO", "FRP B-3 (A700) carried: restroom to T.O. FRP 4'-0\" (A402) and mop sink alcove (1/A504), 148.33 SF, with its PVC trim (A700 B-3 edge M370, inside corner M350, outside corner M360, division bars); G001 'FRP IN RESTROOMS AND MOP SINK AREA - GC'. No cement board / tile backer in the set."),
 ("ALC-21", "NO APLICA", "No shaft wall / area separation wall in the set (1/A500 types A#, C#, D, E#, H only; A100)."),
 ("ALC-22", "NO APLICA", "No new rated partition assembly: G003 (II-B, M, not sprinklered), A100 note 4 maintain the rating of the existing demising walls; G001 labeling of fire rated walls by G.C.; A503 UL D700 / D800 / D900 is a floor-ceiling penetration note for slab work; E112 'plenum rated' is lighting; G000 F.R. abbreviation only. Type X board as printed in every type (1/A500)."),
 ("ALC-23", "NO APLICA", "No ballistic, lead-lined or abuse-resistant panel in the set (1/A500, A700 finish schedule)."),
 ("ALC-24", "CUANTIFICADO", "No finish level printed: Level 4 carried on all board for eggshell paint (A700 PT-1..PT-4), RFI-04; compound and tape by yield."),
]
reg = json.load(open(os.path.join(K, "registro.json")))
NOMB = {r["id"]: r.get("ubicacion") for r in reg["renglones"]}
alcances = [{"id": i, "nombre": NOMB.get(i, i), "estado": e, "nota": x} for i, e, x in alc]
extra = [
 ("Wood framing / blocking / plywood (Div. 06)", "EXCLUDED - wood framing / blocking (Div. 06), not in scope: FRT plywood pendant blocking 1/A501, 2X4 blocking 6/A500, 3/4\" FRT plywood mop shelf 1/A504."),
 ("Fasteners: screws, anchors, PAF", "EXCLUDED - estimator standing order: drywall / framing screws, Hilti X-U shot pins (2/A500), #10 / #12-24 Tek screws (4/A500), anchors at 0 (rows kept with their source)."),
 ("Framed openings for ducts", "EXCLUDED - estimator standing order: duct / air device openings never quantified (M101 / M501 swept)."),
 ("ACT ceilings and grid", "EXCLUDED - C-2 ACT lay-in ceilings and grid (A200, A700)."),
 ("Existing ceiling demolition", "EXCLUDED - D100 keynote 7 gypsum / ACT ceilings 'throughout': extent of each type not shown, excluded for lack of information (0 SF, estimator decision: standing rule for existing ceilings without type)."),
 ("Insulation", "EXCLUDED - batt insulation of type D (1/A500) and A100 note 7 insulation patching."),
 ("Paint", "EXCLUDED - paint PT-1..PT-4 (A700)."),
 ("Storefront, doors, frames, hardware", "EXCLUDED - existing storefront (A300), doors / HM knockdown frames / hardware (A600): other trades."),
 ("Millwork, slat wall, fixtures", "EXCLUDED - millwork and fixtures by the millworker / owner (G001, A103); only the metal blocking behind them is ours."),
 ("MEP and fire alarm", "EXCLUDED - mechanical, plumbing, electrical, fire alarm / Starlink (M / P / E / FA sheets)."),
 ("Patch and repair of existing walls", "INCLUDED (allowance) - D100 keynotes 3 / 4 'PATCH AND REPAIR AS REQUIRED TO LIKE-NEW CONDITION' on the existing walls to remain; area not measurable: allowance by the estimator (Review Item)."),
 ("Exterior signage blocking", "INCLUDED (allowance) - A300 / A301 note 2 'G.C. TO VERIFY AND INSTALL BLOCKING FOR EXTERIOR SIGNAGE AS REQUIRED': size not shown, allowance by the estimator (Review Item)."),
 ("Top of wall bracing to structure (3/A500)", "QUANTIFIED - type E3 braces 362S137-33 @ 48\" o.c. max. to structure, doubled for walls to 15'-0\", 3x3x3 20 ga angle per member (3/A500); brace length = B.O. deck 16'-4\" (A100) - top of wall, at 45 deg."),
 ("Demolition of gypsum board and metal framing", "QUANTIFIED - D100 keynotes 9 / 27 (DEMO-01..06): SF = L x H (one area per element, no layers), H = printed B.O. structure 17'-1 9/16\" (estimator standing rule)."),
]
for k, (n, x) in enumerate(extra, 1):
    alcances.append({"id": f"ALC-E{k:02d}", "nombre": n, "estado": "CUANTIFICADO" if x.startswith(("QUANTIFIED", "INCLUDED")) else "NO APLICA", "nota": x})
barrido = [
 {"item": "header", "specs": "found 2/A600 TYPICAL HEAD DETAIL (track head over HM knockdown frames)", "schedule": "found A600 door schedule HEAD = 2/A600", "estructural": "none: no S sheets in the set"},
 {"item": "deflection clips", "specs": "none: 4/A500 / 5/A500 long-leg slotted runner + floating C channel (no clip)", "schedule": "none", "estructural": "none: no S sheets"},
 {"item": "bracing", "specs": "found 3/A500 top of wall bracing (362S137-33 @ 48\", doubled to 15'-0\")", "schedule": "none: no bracing schedule", "estructural": "none: no S sheets; 6/A500 brace to joist (2X4 wood EXCLUDED)"},
 {"item": "bridging", "specs": "none: 1/A500 - 6/A500 print no bridging / C.R. channel rows", "schedule": "none", "estructural": "none"},
 {"item": "blocking", "specs": "found A104 (1-4), 5/A402, A402 note 4, P501, 1/A504", "schedule": "found A700 / A103 millwork items", "estructural": "none"},
 {"item": "backing", "specs": "found 4/A104 20 GA backing plate (iPad)", "schedule": "none", "estructural": "none"},
]
td = {
 "proyecto": "Consumer Cellular - Yosemite Park Shopping Center, 8283 S. Akron St., Suite 110, Centennial, CO 80112 (store CO2)",
 "bid_set": "15066-26 Consumer Cellular Centennial CO, 37 sheets, dated 10/14/2026, sealed 10/15/2026 ('90% SET / DESIGN INTENT ONLY' in the title block); identical in the Elite Retail and Elder-Jones sets; no addenda; no annotations",
 "fecha": "2026-11-05",
 "inputs": {"waste_metal": 0.15, "waste_no_metal": 0.06, "sheet_w_ft": 4, "sheet_l_ft": 12, "stud_stock_ft": 20,
            "track_stock_ft": 10, "plan_scale_pt_per_ft": 18.0, "bod_ft": 17.13},
 "inputs_notas": {"bod_ft": "A100 deck tags: 'PLY DECK @ 17'-1 9/16\"' (Sales Area) and 'PLY DECK @ 16'-4\"' (Back of House); break not drawn (RFI-01). Heights per wall in the Partition Takeoff.",
                  "plan_scale_pt_per_ft": "A100 / A200 / D100 1/4\" = 1'-0\" (18 pt/ft, checked on the printed 44'-3 1/2\", 31'-6 1/2\" and 66'-10\").",
                  "drywall_screws_per_sf": "YIELD; fasteners EXCLUDED in this project (estimator standing order)."},
 "type_order": ["A3", "C3", "D", "E3"],
 "walls": [], "materials": [],
 "rfis": rfis, "rfi_cierre": cierre, "revisar": plantilla_excel.ordenar_revisar(revisar), "alcances": alcances,
 "proyecto_datos": pd, "hojas_revisadas": hojas, "barrido_no_dibujado": barrido,
}
json.dump(td, open(os.path.join(K, "takeoff.json"), "w"), indent=1, ensure_ascii=False)
print("rfis open", len(rfis), "closed", len(cierre), "revisar", len(revisar), "alcances", len(alcances))
