"""Builds <K>/takeoff.json (plantilla_excel.py format) for Harbor Freight Tools - Loveland, CO from the resolved canon,
3_revision/review_items.json + resolucion.md (closed reading RFIs) and proceso/proyecto_datos.json. TEXT ONLY: every
quantity of the Excel comes from familias_out.json through plantilla_excel (canon.py / accesorios.py), never from here.
Use: python3 bitacora.py run scripts/takeoff_json.py <tools_dir>"""
import json, os, re, sys
sys.path.insert(0, sys.argv[1])
import plantilla_excel
K = os.environ.get("K") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C4 = os.path.join(K, "etapas", "4_canon")
c = json.load(open(os.path.join(C4, "takeoff_canon.json")))
pd = json.load(open(os.path.join(W, "proceso", "proyecto_datos.json")))
RV = os.path.join(K, "etapas", "3_revision")
rev = json.load(open(os.path.join(RV, "review_items.json"))) if os.path.exists(os.path.join(RV, "review_items.json")) else []
fo = json.load(open(os.path.join(C4, "out", "familias_out.json")))


def fmt(o):
    A, B = o.get("A") or {}, o.get("B") or {}
    C = o.get("C") or "____"
    C = C.get("texto") if isinstance(C, dict) else C
    return (f"(A) Drawings ({A.get('source', '')}): {A.get('texto', '')} - delta {A.get('delta', '')} | "
            f"(B) Code ({B.get('cita', 'n/a')}): {B.get('texto', '')} - delta {B.get('delta', '')} | (C) Other: {C or '____'}")


rfis = []
for r in c["rfis"]:
    o = json.loads(json.dumps(r.get("opciones") or r.get("options") or {}))
    if not o.get("C"):
        o["C"] = "____"
    rfis.append({"id": r["id"], "pregunta": f"{r['question']} - carried: {r.get('loaded') or o.get('A', {}).get('texto', '')} "
                 "(conservative value loaded)", "delta": fmt(o), "opciones": o, "source": r.get("source") or "",
                 "barrido": r.get("barrido") or {}, "img": r.get("img")})

# RFIs of the two readings closed by the resolution with a printed source (resolucion.md, "Closed")
cierre = {
 "A-RFI-02 / B-RFI-08": {"pregunta": "Interior door / window headers 'not called' - CLOSED by the drawings: 2/A5.1 TYP. INTERIOR DOOR HEAD DETAIL and 5/A5.1 INTERIOR WINDOW HEAD DETAIL draw the head track ('steel stud to match wall construction'): metal header 1 piece (R.O. + 1'-4\") by the header program, window 306 with sill track; D08 existing H.M. door in masonry = existing lintel",
                         "delta": "0 (value per the drawings, applied: header / box beam and sill track rows)"},
 "A-RFI-04": {"pregunta": "Receiving enclosure cold-formed framing scope - CLOSED: Div. 05 40 cold-formed metal framing is ours (estimator standing order) and S2.1 / S4.1 print the members (600S162-54 @ 16\", headers H-1 / H-2, box beams BB-1)",
              "delta": "0 (value per the drawings, applied: RE-1..RE-3, RE-BB1, RE-JAMB, headers)"},
 "B-RFI-03": {"pregunta": "West wall furring demolition extent - CLOSED by the drawings: D1.0 keynote 209 dashed extent along the west masonry wall (DEMO-14)",
              "delta": "0 (value per the drawings, applied: DEMO-14)"},
 "B-RFI-05": {"pregunta": "Receiving enclosure header assignment - CLOSED by the drawings: S2.1 roof plan assigns H-2 to the 6'-0\" opening (RE-1) and H-1 to the 10'-0\" opening (RE-3), header schedule pieces on S2.1",
              "delta": "0 (value per the drawings, applied)"},
 "B-RFI-07": {"pregunta": "Slip vs standard top track at type A walls - CLOSED by the drawings: A/A4.1 prints '6\" x 20 GA steel track' at the existing deck = standard top track",
              "delta": "0 (value per the drawings, applied)"},
}

# Review items (rev2, back-check F2): estimator-facing sentences with N/SHEET only; floor plan by type A-Z, then details
# in the order the floor plan calls them. Source of each: 3_revision/review_items.json + back-check rev1 (O3, O7).
RI = [
 ("floor_plan", "C", None, "A1.1",
  "C-02 (Support Office 103, east wall inside the type D demising wall, 10.94 LF): A1.1 prints one C tag in Support Office 103 "
  "with the inner line drawn on both the north and east walls; loaded as type C on both walls. A: keep C-02 as type C (loaded) / "
  "B: no inner wall on the east side; delta -10.94 LF of 3-5/8\" wall, about -93 SF of board.",
  "plan crop of A1.1 Support Office 103 (C tag and the inner line on the north and east walls)"),
 ("floor_plan", "D", None, "A1.2 / A2.0",
  "D-01 demising wall loaded at the high point 18'-2\" for its full 209'-1\" (RFI-01). A: one height for the whole wall (loaded) / "
  "B: height zones from the A1.2 B.O. deck spot values; delta see RFI-01.", "no crop (A1.2 clearance chart, A2.0 deck spots)"),
 ("floor_plan", "DEMO", None, "D1.0 / A1.2",
  "West wall furring demolition (D1.0 keynote 209, DEMO-14) loaded all at the Sales B.O. structure 16'-9\". A: all at 16'-9\" "
  "(loaded) / B: the part in Sales Replenishment at 15'-9 1/2\"; delta = 1'-0\" less height on that part, 1 face.",
  "plan crop of D1.0 west wall, keynote 209 dashed extent"),
 ("floor_plan", "RE", None, "S2.1",
  "Receiving enclosure openings: widths not printed on S2.1; measured on the plan 5.94 ft and 9.93 ft, loaded 6'-0\" (RE-1) and "
  "10'-0\" (RE-3). A: 6'-0\" / 10'-0\" (loaded) / B: field-verified widths; delta = width change x header pieces (H-2 4, H-1 5).",
  "plan crop of S2.1 receiving enclosure"),
 ("floor_plan", "VH", None, "A5.2 / A1.1",
  "Vestibule bulkhead side runs VH-02 / VH-03: A5.2 prints 8'-11\"; the plan line measures 8'-7\". A: 8'-11\" printed (loaded) / "
  "B: 8'-7\" measured; delta -0.33 ft on each side run (track, board, box header).", "plan crop of A1.1 vestibule and A5.2"),
 ("detalle", None, 1, "GN/A0.2 (general notes)",
  "A0.2 general note: 'ALL EXISTING GYPSUM BOARD TO BE REPAIRED TO LIKE NEW CONDITION'. Included as patch and repair of existing "
  "gypsum board; the area is not measurable from the drawings: allowance by the estimator (Scope Checklist).",
  "A0.2 general notes"),
 ("detalle", None, 2, "8/A5.3",
  "Bi-parting door box header 8/A5.3: loaded 4 pieces (2 studs + 2 tracks, 12'-0 1/2\" each); the section draws C studs inside the "
  "brake metal. A: 4 pieces (loaded) / B: pieces as drawn in 8/A5.3; delta = one piece length per piece removed.",
  "detail crop of 8/A5.3 and 9/A5.3"),
 ("detalle", None, 3, "2/A5.1",
  "Interior door and window heads: one head track per opening, (R.O. + 1'-4\") long, per 2/A5.1 and 5/A5.1. A: as loaded / B: none; "
  "delta = the interior door / window head lengths of the header row.", "detail crop of 2/A5.1 and 5/A5.1"),
]
revisar = []
for k, (f, t, o, h, txt, img) in enumerate(RI, 1):
    it = {"fase": f, "punto": txt + f" Source {h}.", "hoja_detalle": h, "imagen": img}
    if t:
        it["type"] = t
    if o:
        it["orden_plano"] = o
    revisar.append(it)

hojas = [
 {"categoria": "cover / index / code", "estado": "reviewed", "hojas": "A0.0 (list of drawings, project scope, code data, occupant load)"},
 {"categoria": "general notes", "estado": "reviewed", "hojas": "A0.2 general notes (metal framing / gypsum board by G.C., 3-coat finish), A0.3 / A0.4 (raster, slab / floor specs)"},
 {"categoria": "site", "estado": "reviewed - not our trade", "hojas": "AS1.0, AS1.1 site plan / details"},
 {"categoria": "demolition + notes", "estado": "reviewed", "hojas": "D1.0 demolition plan + keynotes 200-236 + demo legend"},
 {"categoria": "specs", "estado": "reviewed", "hojas": "no project manual: A0.2 notes, A4.1 wall type notes 1-10, S1.0 / S1.1 cold-formed framing notes"},
 {"categoria": "partition types + details", "estado": "reviewed", "hojas": "A4.1 wall types A-E + details 1-10; A4.0 enlarged plans / interior details; A4.2 / A4.3 receiving enclosure; A5.1 / A5.3 door, window, vestibule and box header details"},
 {"categoria": "floor plans", "estado": "reviewed", "hojas": "A1.1 floor plan + keynotes, A1.1A, A1.2 clearance heights / B.O. deck, A1.3 / A1.3A finish schedule and fixture plan"},
 {"categoria": "RCP", "estado": "reviewed", "hojas": "A2.0 reflected ceiling plan + keynotes 500-520 (ACT ceilings, open to structure, no gyp ceilings)"},
 {"categoria": "elevations / sections", "estado": "reviewed", "hojas": "A3.0 / A3.1 exterior elevations, A4.0 sections"},
 {"categoria": "enlarged / interior elevations", "estado": "reviewed", "hojas": "A4.0 enlarged restroom / break room plans and interior elevations, 1/A4.1 mop sink - shelf detail, A5.2 storefront elevations"},
 {"categoria": "schedules", "estado": "reviewed", "hojas": "A5.0 door schedule + frame types, A5.2 storefront elevations, A1.3 room finish schedule"},
 {"categoria": "structural", "estado": "reviewed", "hojas": "S1.0 / S1.1 notes, S2.0 hybrid renovation plan, S2.1 enlarged receiving enclosure plans (studs, headers, box beams), S3.0 typical details, S4.0 / S4.1 enclosure sections"},
 {"categoria": "MEP", "estado": "reviewed", "hojas": "M1.0-M1.3, P1.0-P1.1, FP1.0 swept for crossings of our walls (ducts EXCLUDED by standing order); E0.1-E2.2, EMS-1..4 (no fixture in gypsum surfaces)"},
]

EXC = "EXCLUDED - not in scope (estimator standing order, no RFI): "
alc = [
 ("ALC-01", "CUANTIFICADO", "Partition types A (6\" @ 16\"), B (2-1/2\"), C (3-5/8\"), D (6\" 1-hr demising, UL U419), E (1-1/2\" metal hat channel @ 24\" O.C. vertical over the existing masonry) per A4.1; vestibule bulkhead studs 1/A5.3; studs, bottom and top track by size in the Material Summary."),
 ("ALC-02", "CUANTIFICADO", "Receiving enclosure cold-formed walls RE-1..RE-3 600S162-54 @ 16\" (S2.1, 1/A4.3, 4/A4.3; Div. 05 40 cold-formed framing = ours); no other exterior CFMF (existing masonry building, A3.0 / A3.1)."),
 ("ALC-03", "NO APLICA", "No metal parapet framing in the set: existing masonry parapets (A3.0, A3.1, S1.0)."),
 ("ALC-04", "CUANTIFICADO", "Bottom and top track by stud size; deflection / slip track 10/A4.1 at type D (studs cut 1\" short of deck) and 3/A5.3 at the vestibule bulkhead, standard 6\" x 20 GA track at type A (A/A4.1), standard track at the enclosure (S4.1); type E hat channel has no runner (E/A4.1); slip and standard tracks on separate rows."),
 ("ALC-05", "CUANTIFICADO", "Interior door / window heads 2/A5.1 and 5/A5.1 (1 head track, R.O. + 1'-4\"), window sill track, vestibule box header 2/A5.3, bi-parting door box header 8/A5.3 / 9/A5.3, enclosure headers H-1 / H-2 and box beams BB-1 (S2.1) in the header / box beam row."),
 ("ALC-06", "CUANTIFICADO", "1-1/2\" 16 GA C.R. channel @ 8'-0\" O.C. vertically at partitions higher than 12'-0\" (A4.1 note 7); vestibule bulkhead kickers 3-5/8\" x 18 GA @ 4'-0\" (1/A5.3, RFI-04); no C.R. bracing on walls of 12'-0\" or less nor on the hat channel furring; walls braced to structure @ 4'-0\" O.C. (A1.1 wall legend note 1, 2/A4.1): 6\" x 20 GA metal stud braces + Trade Ready Spazzer 9200 spacing bar, brace length RFI-05."),
 ("ALC-07", "CUANTIFICADO", "5/8\" gypsum board per face and layer per A4.1 types (A both sides, B / C one side, D 5/8\" Type X each side to 1\" below deck, E one face) and the vestibule bulkhead faces (1/A5.3)."),
 ("ALC-08", "CUANTIFICADO", "5/8\" moisture-resistant (green) board at restrooms 107 / 108, break room sink wall and mop sink (A4.0 keynotes 717 / 723, 1/A4.1) and the mop shelf underside (1/A4.1)."),
 ("ALC-09", "NO APLICA", "No exterior gypsum / glass mat sheathing: the receiving enclosure carries FRT exterior grade plywood (A4.3) = Div. 06 EXCLUDED; metal wall panels by others."),
 ("ALC-10", "NO APLICA", "EXCLUDED - wood (Div. 06): FRT plywood blocking at accessories (A4.0 722 / 723, 8/A4.0), electrical backboard (A1.1 325), OSB wainscot (A1.3), enclosure FRT plywood (A4.3), mop shelf plywood top (1/A4.1)."),
 ("ALC-11", "NO APLICA", "No gypsum board ceiling: A2.0 ceilings are ACT-1 / ACT-2 lay-in (EXCLUDED) or open to structure; the mop shelf board is in the MR row."),
 ("ALC-12", "NO APLICA", "No suspended gypsum ceiling (A2.0); ACT grid EXCLUDED."),
 ("ALC-13", "CUANTIFICADO", "Vestibule bulkhead over the storefront (1/A5.3): 3-5/8\" x 20 GA studs @ 16\" on a 6\" x 18 GA box header (2/A5.3), slip track 3/A5.3, kickers @ 4'-0\" (RFI-04), 5/8\" gyp both faces."),
 ("ALC-14", "NO APLICA", "No canopy / marquee framing in our scope (A3.0 / A3.1 storefront and existing facade; S2.0)."),
 ("ALC-15", "NO APLICA", "No column furring / wrap printed (A1.1, A4.1)."),
 ("ALC-16", "NO APLICA", "No metal blocking printed: accessory / fixture blocking is FRT wood / plywood (A1.3, 1/A1.3A, 8/A4.0) = Div. 06 EXCLUDED."),
 ("ALC-17", "NO APLICA", EXC + "framed openings for ducts / air devices; access panels are in ACT ceilings (A2.0 note 5); no access panel in gypsum surfaces."),
 ("ALC-18", "CUANTIFICADO", "Metal corner beads at all gypsum board returns (A4.1 note 5) and control joints @ 30'-0\" O.C. (A4.1 note 6, 7/A4.1, 9/A4.1 rated) on D-01 and E-01, in their own rows."),
 ("ALC-19", "NO APLICA", "EXCLUDED in all projects (estimator standing order): acoustical sealant and sound attenuation; batt insulation of the A4.1 types EXCLUDED."),
 ("ALC-20", "CUANTIFICADO", "FRP panels WC-1 'fiber reinforced plastic to ceiling' at restrooms 107 / 108 and the mop alcove (A1.3 finish schedule, 1/A4.1): FRP carried per A1.3 finish schedule (G.C. scope); no cement board / tile backer in the set (base VB-1 vinyl)."),
 ("ALC-21", "NO APLICA", "No shaft wall / area separation wall in the set (A4.1)."),
 ("ALC-22", "CUANTIFICADO", "Type D 1-hour demising wall UL U419 (A4.1 note 10): 5/8\" Type X each side to 1\" below deck, rated control joint 9/A4.1."),
 ("ALC-23", "NO APLICA", "None in the set (A4.1, A1.3)."),
 ("ALC-24", "CUANTIFICADO", "A0.2 'fire taped and spackled three (3) coats, sanded and ready to receive paint' = Level 4 on all board; no Level 5 printed; compound and tape by yield."),
]
reg = json.load(open(os.path.join(K, "registro.json")))
NOMB = {r["id"]: r.get("ubicacion") for r in reg["renglones"]}
alcances = [{"id": i, "nombre": NOMB.get(i, i), "estado": e, "nota": x} for i, e, x in alc]
extra = [
 ("Wood framing / blocking / plywood (Div. 06)", "EXCLUDED - wood framing / blocking (Div. 06), not in scope: " + "; ".join(x.split("not in scope: ")[-1] for x in c.get("exclusions_info") or [] if "Div. 06" in x)),
 ("Fasteners: screws, anchors, PAF", "EXCLUDED - estimator standing order: drywall / framing screws, anchors, PAF, slab pins at 0 (rows kept with their source)."),
 ("Framed openings for ducts", "EXCLUDED - estimator standing order: duct / air device openings never quantified (M1.0-M1.3 / P1.0-P1.1 swept)."),
 ("ACT ceilings and grid", "EXCLUDED - ACT-1 / ACT-2 lay-in ceilings and grid (A1.3, A2.0 keynote 502), adjacent tenant grid reinstallation (A2.0 519, D1.0 236)."),
 ("Existing lay-in ceiling demolition", "EXCLUDED - D1.0 keynote 210: no ceiling type shown, excluded for lack of information (0 SF)."),
 ("Insulation", "EXCLUDED - batt / rigid insulation of the A4.1 wall types and 1/A5.3."),
 ("Paint", "EXCLUDED - paint (A1.3)."),
 ("Storefront, doors, frames, hardware", "EXCLUDED - storefront (A5.2), doors / H.M. frames (A5.0): other trades."),
 ("Masonry, roofing, structural steel", "EXCLUDED - masonry and its demolition (D1.0 218 / 219 / 220 / 224), roofing, structural steel, lintels."),
 ("MEP", "EXCLUDED - mechanical, plumbing, fire protection, electrical (M / P / FP / E sheets)."),
 ("Patch and repair of existing gypsum board", "INCLUDED (allowance) - patch and repair: A0.2 general note 'ALL EXISTING GYPSUM BOARD TO BE REPAIRED TO LIKE NEW CONDITION'; quantity not measurable from the drawings: allowance by the estimator (Review Item)."),
 ("Bar stock at top of the furred wall", "EXCLUDED - E/A4.1 note 'G.C. to provide and install bar stock' @ 16'-0\" A.F.F. at the west wall (A2.0 keynote 520): by G.C., not cold-formed framing."),
 ("FRP panels", "QUANTIFIED - FRP carried per A1.3 finish schedule (G.C. scope): WC-1 restrooms 107 / 108 + mop alcove (1/A4.1); PVC trim part of the FRP install (A1.3 WC-1 remarks)."),
 ("Demolition of gypsum board and metal framing", "QUANTIFIED - D1.0 keynotes 207 / 208 / 209 / 211 (DEMO-01..14): SF = L x H x layers, heights = B.O. structure of the bay (A1.2, standing order), layers RFI-02."),
]
for k, (n, x) in enumerate(extra, 1):
    alcances.append({"id": f"ALC-E{k:02d}", "nombre": n, "estado": "CUANTIFICADO" if x.startswith(("QUANTIFIED", "INCLUDED")) else "NO APLICA", "nota": x})

barrido = [
 {"item": "header", "specs": "found A4.1 notes / 2/A5.1, 5/A5.1 (head track at interior openings), 2/A5.3, 8/A5.3 box headers", "schedule": "found S2.1 cold formed header schedule H-1 / H-2", "estructural": "found S2.1 (headers, box beams BB-1), S4.1"},
 {"item": "deflection clips", "specs": "none: A4.1 notes / 10/A4.1 slip track (studs cut 1\" short), no clip", "schedule": "none: A4.1 wall types print slip track, no clip", "estructural": "none: S3.0 / S4.1 typical details print no deflection clip for interior partitions"},
 {"item": "bracing", "specs": "found A4.1 note 7 (1-1/2\" 16 GA CRC @ 8'-0\" O.C. above 12'-0\"), A1.1 wall legend note 1 + 2/A4.1 bracing to structure (carried, RFI-05)", "schedule": "none: no bracing schedule", "estructural": "found 1/A5.3 kickers @ 4'-0\" (RFI-04); S2.1 / S4.1 enclosure bracing by sheathing (plywood Div. 06)"},
 {"item": "bridging", "specs": "found A4.1 note 7 (CRC rows)", "schedule": "none", "estructural": "none: S1.0 notes, no bridging detail for interior partitions"},
 {"item": "blocking", "specs": "none: A0.2 / A4.1 print no metal blocking", "schedule": "none: A1.3 / 1/A1.3A blocking is FRT wood (Div. 06)", "estructural": "none: S sheets print no metal blocking"},
 {"item": "backing", "specs": "none: no metal backing plate printed", "schedule": "none", "estructural": "none: accessory backing = FRT plywood (A4.0 722 / 723) Div. 06 EXCLUDED"},
]

td = {
 "proyecto": "Harbor Freight Tools - Loveland, CO (1325 E. Eisenhower Blvd., Loveland, CO 80537)",
 "bid_set": "Harbor Freight Tools - Loveland CO.pdf (50 sheets, issue 10/07/26, job 26041, no addenda; clean copy without annotations)",
 "fecha": "2026-11-03",
 "inputs": {"waste_metal": 0.15, "waste_no_metal": 0.06, "sheet_w_ft": 4, "sheet_l_ft": 12, "stud_stock_ft": 20,
            "track_stock_ft": 10, "plan_scale_pt_per_ft": 6.75, "bod_ft": 18.25},
 "inputs_notas": {"bod_ft": "A1.2 clearance heights chart: SALES B.O. deck +-18'-3\" high / +-17'-4\" low, B.O. structure +-16'-9\"; SALES REPLENISHMENT B.O. deck +-17'-4\" / +-16'-11\", B.O. structure +-15'-9 1/2\" / +-15'-5\" (heights per wall in the Partition Takeoff).",
                  "plan_scale_pt_per_ft": "A1.1 / D1.0 / A2.0 3/32\" = 1'-0\" (6.75 pt/ft, checked on the printed 209'-1\" demising wall); A4.0 3/8\" = 1'-0\"; S2.1 1/4\" = 1'-0\".",
                  "drywall_screws_per_sf": "YIELD; fasteners EXCLUDED in this project (estimator standing order)."},
 "type_order": ((c.get("constants") or {}).get("type_order") or {}).get("value") or ([p["type"] for p in c.get("partition_schedule") or []] + sorted(set(fo["partition_types"]["types"]) - {p["type"] for p in c.get("partition_schedule") or []})),
 "walls": [], "materials": [],
 "rfis": rfis, "rfi_cierre": cierre, "revisar": plantilla_excel.ordenar_revisar(revisar), "alcances": alcances,
 "proyecto_datos": list(pd), "hojas_revisadas": hojas, "barrido_no_dibujado": barrido,
}
json.dump(td, open(os.path.join(K, "takeoff.json"), "w"), indent=1, ensure_ascii=False)
print("rfis open", len(rfis), "closed", len(cierre), "revisar", len(revisar), "alcances", len(alcances))
