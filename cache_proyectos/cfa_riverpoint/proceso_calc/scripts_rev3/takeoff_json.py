"""Builds cfa_calc/takeoff.json (plantilla_excel.py format) from the reconciled canon + project data. TEXT ONLY: every
quantity of the Excel comes from familias_out.json through plantilla_excel.fusionar (canon.py), never from here.
RFI-16 delta text is read from etapas/4_canon/rfi16/rfi16_delta.json (scripts/rfi16_delta.py = canon.py on a copy)."""
import json, os, re, sys
sys.path.insert(0, sys.argv[1])
import plantilla_excel
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C4 = os.path.join(K, "etapas", "4_canon")
c = json.load(open(os.path.join(C4, "takeoff_canon.json")))
pd = json.load(open("/home/user/reading-plans/cache_proyectos/cfa_riverpoint/proceso/proyecto_datos.json"))
r16 = json.load(open(os.path.join(C4, "rfi16", "rfi16_delta.json")))
rev = json.load(open(os.path.join(K, "etapas", "3_revision", "review_items.json")))

d16 = r16["delta_familias"]
lfs = r16["wall_lf_by_stud_size"]
t16 = (f"computed by program (the take-off calculation program re-run on a copy of the reconciled take-off data with the new interior W4 / W4.1 / W6 / W8 "
       f"walls as metal studs @ 16\" O.C., A-202 schedule W4 / W4.1 / W6 '2x4 WD STUD' -> 3-5/8\", W8 '2x8 WD STUD' -> 8\"; "
       f"SW6 exterior and existing walls not included; height 10'-8\" = C.1/A-202 + C.H. 10'-2\"): wall LF "
       f"{r16['wall_lf_total']:.2f} (W4 {r16['wall_lf_by_type']['W4']:.2f}, W4.1 {r16['wall_lf_by_type']['W4.1']:.2f}, "
       f"W6 {r16['wall_lf_by_type']['W6']:.2f}, W8 {r16['wall_lf_by_type']['W8']:.2f}) -> "
       f"+{d16.get(chr(51)+'-5/8\" stud (todos los gauges)', 0):.2f} LF 3-5/8\" studs, +{d16.get('8\" stud (todos los gauges)', 0):.2f} LF 8\" studs, "
       f"+{lfs.get(chr(51)+'-5/8\"', 0):.2f} LF bottom + {lfs.get(chr(51)+'-5/8\"', 0):.2f} LF top 3-5/8\" track, "
       f"+{lfs.get('8\"', 0):.2f} LF bottom + {lfs.get('8\"', 0):.2f} LF top 8\" track, "
       f"+{d16.get('bracing C.R. channel', 0):.2f} LF bracing C.R. channel (C09111 3.2.C @ 48\"); board unchanged")


def fmt(o):
    A, B = o.get("A") or {}, o.get("B") or {}
    return (f"(A) Plans / specs ({A.get('source', '')}): {A.get('texto', '')} - delta {A.get('delta', '')} | "
            f"(B) Trade code ({B.get('cita', 'n/a')}): {B.get('texto', '')} - delta {B.get('delta', '')} | (C) Other: ____")


rfis, cierre = [], {}
for r in c["rfis"]:
    o = json.loads(json.dumps(r.get("opciones") or {}))
    if r["id"] == "RFI-16":
        o["A"]["delta"] = "0 (loaded as wood, board-only); metal alternative: " + t16
        o["B"]["delta"] = "n/a: the trade code does not select wood vs metal framing"
    if str(r.get("status", "")).startswith("closed"):
        cierre[r["id"]] = {"pregunta": f"{r['question']} - CLOSED: estimator decision (option A): {o['A']['texto']}",
                           "delta": o["A"]["delta"]}
        continue
    rfis.append({"id": r["id"], "pregunta": f"{r['question']} - carried: {o['A']['texto']} (conservative value loaded)",
                 "delta": fmt(o), "opciones": o, "source": r.get("source") or o["A"].get("source", "")})

# Review items (8): floor plan by type A-Z, then details in the order the floor plan calls them
FASE = {1: ("floor_plan", "INFILL", None, "A-202 / A-050 KN1 / C2/S-801"),
        2: ("detalle", None, 3, "A2/S-241"),
        3: ("detalle", None, 2, "A1/A-604"),
        4: ("floor_plan", "DEMO", None, "S-201 / A-050"),
        5: ("floor_plan", "DEMO", None, "A-052 KN10"),
        6: ("floor_plan", "W6", None, "A-201 KN25 / G.7/A-202"),
        7: ("detalle", None, 1, "A2/A-605"),
        8: ("floor_plan", "DEMO", None, "A-050")}
revisar = []
FIX = {1: {"item": "MB-01 metal infill at removed Eliason door: loaded 6\" metal @ 16\" per D3/A-624 (RFI-17 closed)", "A": "6\" metal (D3/A-624)", "B": "0 (not loaded)",
           "delta": "3-5/8\" alternative (C2/S-801): MB-01 studs + track move from 6\" to 3-5/8\"; wood: framing Div. 06"},
       7: {"item": "M3.5 stud size: loaded 8\" per A2/A-605 (A-202 schedule prints 3-5/8\" sistered)", "A": "8\" (as loaded)", "B": "3-5/8\" + RFI"}}
for x in rev:
    x = dict(x, **FIX.get(x["n"], {}))
    f, t, o, h = FASE[x["n"]]
    for kk in ("item", "A", "B", "delta", "source"):
        x[kk] = re.sub(r"\bPT\d{4}\b", "tag", re.sub(r"\s*\(?R-ALC-\d+,?\s*", " (", str(x[kk]))).replace("( ", "(").replace(" ()", "")
    it = {"fase": f, "punto": f"{x['item']}: A {x['A']} / B {x['B']}; delta {x['delta']}; source {x['source']}",
          "hoja_detalle": h, "imagen": f"resolution crop {x['n']} (review folder)"}
    if t:
        it["type"] = t
    if o:
        it["orden_plano"] = o
    revisar.append(it)

hojas = [
 {"categoria": "cover / index", "estado": "reviewed", "hojas": "G-000 (sheet index, scope of work, codes), G-002, G-004, G-005"},
 {"categoria": "code analysis / G sheets", "estado": "reviewed", "hojas": "G-003 code summary, egress, occupant load, plumbing count"},
 {"categoria": "general notes", "estado": "reviewed", "hojas": "G-000 general notes; A-202 wall notes B-H; S-001 general structural notes"},
 {"categoria": "demolition + notes", "estado": "reviewed", "hojas": "A-050 demolition plan + keynotes, A-052 RCP demolition + keynotes"},
 {"categoria": "specs", "estado": "reviewed", "hojas": "A-901..A-911 specifications (C09111 non-load-bearing steel framing, C09250 gypsum board, C08306 access doors); S-901 / S-902 structural specs"},
 {"categoria": "partition types + details", "estado": "reviewed", "hojas": "A-202 wall type schedules (interior + exterior) + wall notes; A-401 / A-402 sections; A-50x exterior details; A-604 / A-605 BOH details; A-624 / A-625 FOH details; S-801 typical nonstructural details"},
 {"categoria": "floor plans", "estado": "reviewed", "hojas": "A-201 floor plan + keynotes, A-202 dimensional control plan, A-211 wall & floor finish plan"},
 {"categoria": "RCP", "estado": "reviewed", "hojas": "A-221 reflected ceiling plan + keynotes + legend; S-241 dropped ceiling plan"},
 {"categoria": "elevations / sections", "estado": "reviewed", "hojas": "A-301 / A-302 exterior elevations, A-401 building section, A-402 wall sections"},
 {"categoria": "enlarged / interior elevations", "estado": "reviewed", "hojas": "A-601..A-605 kitchen / BOH elevations, A-611 restroom, A-621..A-625 dining elevations and details, A-701 millwork"},
 {"categoria": "schedules", "estado": "reviewed", "hojas": "A-801 door schedule; A-211 finish legend; A-202 wall type schedules; A2/S-241 ceiling joist schedules"},
 {"categoria": "structural", "estado": "reviewed", "hojas": "S-001, S-101 (note 4 wood shear walls), S-201 roof framing, S-241 dropped ceiling plan, S-600 / S-601 / S-610 typical wood framing, S-801 typical nonstructural details, S-901 / S-902"},
 {"categoria": "MEP", "estado": "reviewed", "hojas": "M-200..M-902, MH-101..MH-103, P-100..P-901 swept for duct / pipe crossings of our metal walls (0 framed openings; ducts EXCLUDED by standing order); E sheets for fixtures in GWB ceilings (6\" D1 fits the joist module)"},
 {"categoria": "vendor / not our trade", "estado": "reviewed - not our trade", "hojas": "A-100 / A-102 site, A-104 / A-105 canopies + OMD vendor sheets p48-63 (prefabricated metal canopies EXCLUDED), K-sheets kitchen equipment, civil / landscape / vapor control p139-172"},
]

EXC = "EXCLUDED - not in scope (estimator standing order, no RFI): "
alc = [
 ("ALC-01", "Interior partition framing (studs + tracks)", "CUANTIFICADO", "Metal types M2.1 (2\" Z channel @ 24\", A-202 / A1/A-605) and M3.5 (8\" studs at hoods #2 / #3 per A2/A-605, RFI-01 closed) + menu board infill MB-01 6\" @ 16\" (D3/A-624, RFI-17 closed); C09111 2.3 / A-909; gauge per plans 33 mil (RFI-18 closed). Studs, bottom and top track by size in the Material Summary."),
 ("ALC-02", "Exterior wall framing (CFMF)", "NO APLICA", "EXCLUDED - wood framing (Div. 06): SW6 exterior walls are 2x6 SYP @ 16\" (A-202 exterior wall type schedule, S-101 note 4); their interior gypsum / cement board is in the BOARD ONLY block."),
 ("ALC-03", "Parapet framing", "NO APLICA", "Parapets are wood-framed / existing (A-301, A-302, A-402, S-201): no metal parapet framing in the set."),
 ("ALC-04", "Top / deflection and bottom track", "CUANTIFICADO", "Bottom and top track by stud size: 8\" at M3.5 (A2/A-605) and 6\" at the menu board infill MB-01 (D3/A-624), fixed 33 mil top track with braces per D1/S-801; 3\" long-leg slotted continuous track per C1/S-801 where the studs reach the roof framing (roof hatch shaft) in its own row; M2.1 Z channel has no runner (A1/A-605); ceiling / soffit track 3-5/8\", 6\" rim track (A3/S-241), strongback 362T125-54 (C3/S-801) in their own rows."),
 ("ALC-05", "Headers, sills and jambs at openings", "CUANTIFICADO", "No door / window opening in our metal walls (A-202, A-801); 8\" runner (sill / head) at the A2/A-605 pin & sleeve recess loaded as sill track (RFI-13)."),
 ("ALC-06", "Bracing / bridging", "CUANTIFICADO", "Wall braces 362S162-33 @ 48\" per the D1/S-801 METAL STUD BRACE SCHEDULE + 54 mil bent plates at M3.5-01 / M3.5-02 / MB-01 (A-202 note C.4, C2/S-801); soffit cross braces 362S162-33 @ 32\" (C4/A-624, C3/S-801); ceiling bridging: 1 row mid-span C.R. channel per dropped ceiling (A2/S-241, RFI-09). No C.R. channel on the furring / sistered walls (none drawn)."),
 ("ALC-07", "Gypsum board on walls (layers per type)", "CUANTIFICADO", "1/2\" gypsum board and 1/2\" cement board per face (A-202 notes G.1-G.13 / H.1-H.3, A-211, A-60x / A-611 / A-62x; C09250 2.1.B / 2.2.B, A-909) on metal walls and board-only W / existing walls."),
 ("ALC-08", "Moisture / abuse / special board at wet zones", "CUANTIFICADO", "C09250 2.2.A (A-909) water-resistant gypsum backing board at toilets / sinks: restroom gypsum faces above the tile (A-611) loaded as 1/2\" moisture-resistant board (plan thickness, A-202 notes G.1 / H.3); spec 2.2.A.2 5/8\" Type X core = RFI-21 closed, option A (same SF); tile / FRP / stainless substrates are 1/2\" cement board (A-202 notes G.2-G.7)."),
 ("ALC-09", "Exterior gypsum / glass mat sheathing", "NO APLICA", "EXCLUDED - SW6 exterior structural sheathing is wood (E.1/A-202, S-600): Div. 06; no glass mat / exterior gypsum sheathing on A-202, A-30x, A-40x, A-50x."),
 ("ALC-10", "FRT plywood sheathing / substrate", "NO APLICA", "EXCLUDED - wood framing / blocking (Div. 06): 1/2\" and 3/4\" CDX / plywood G.3, G.9, G.10, G.12, G.13 (A-202), A-625 wainscot plywood, A1/A-604 hatch plywood, D-Blaze FRT blocking at the hood (A-501)."),
 ("ALC-11", "Gypsum board ceilings", "CUANTIFICADO", "5/8\" gyp ceilings Entry A / Entry B / Men's / Women's / play bay (A-221 + S-241, C09250 2.1.E / A-909) and 1/2\" gyp soffit bottoms (C4/A-624)."),
 ("ALC-12", "Ceiling suspension (furring / carrying channel / hanger wire / ceiling track)", "NO APLICA", "No suspended gypsum ceiling: the new gyp ceilings are framed wall to wall with 600S162-33 joists @ 16\" (A2/S-241, RFI-08 closed) - 6\" joist + 6\" rim track rows; hung systems of C09111 3.2.B do not apply; ACT grid EXCLUDED (A-221)."),
 ("ALC-13", "Soffits and bulkheads (framing + board)", "CUANTIFICADO", "Serving and gathering-table soffits PT-31A C.H. 9'-8\" (A-221, C4/A-624 3-5/8\" @ 16\", C3/S-801 strongback 362T125-54 @ 48\"); hanger height in RFI-15."),
 ("ALC-14", "Canopy / marquee framing and sheathing", "NO APLICA", EXC + "prefabricated metal order-point / meal-delivery canopies and awnings (A-104, A-105, OMD vendor sheets p48-63, A-221 KN10 / KN11)."),
 ("ALC-15", "Column furring / wraps", "NO APLICA", "No column wrap in our scope on A-201 / A-202 / A-221 (wood-framed existing building, S-201)."),
 ("ALC-16", "Blocking (FRT wood / metal) for millwork and accessories", "CUANTIFICADO", "Metal blocking at hood wall brackets (A2/S-801) and menu board 33 mil blocking T&B = 2 rows (C2/S-801); wood blocking F.1/A-202, S-241 2x4, A4/A-624, A-602 shelving, A1/A-604 ladder = Div. 06 EXCLUDED."),
 ("ALC-17", "Framed openings (MEP, access panels, diffusers)", "NO APLICA", EXC + "framed openings for ducts / air devices; 6\" D1 downlights fit the 16\" joist module (A-221 legend); no access panel on A-221 / C08306 (A-907) for our ceilings; MEP sweep 0 crossings of the metal walls."),
 ("ALC-18", "Trim: corner bead, casing bead, control joints, reveals", "CUANTIFICADO", "Corner bead at all soffit gypsum intersections (C4/A-624); LC / J-bead at the exposed gypsum edge of the menu board wall (D3/A-624) and J trim on top of the play area cement board base (A2/A-624); no control joint / reveal printed for our board."),
 ("ALC-19", "Acoustical sealant / sound attenuation", "NO APLICA", "EXCLUDED in all projects (estimator standing order); insulation / batts B.1-B.5/A-202 and mineral wool A1/A-605 EXCLUDED."),
 ("ALC-20", "FRP / cement board / tile backer", "CUANTIFICADO", "1/2\" cement board (DUROCK, C09250 2.2.B / A-909) behind tile, FRP, stainless and at bases, with alkali-resistant mesh tape + setting-type compound at its joints (C09250 2.4.B.2 / 2.4.D.2 / 3.5.E); FRP panels, Composeal / Kerdi membrane and tile themselves EXCLUDED (other trades)."),
 ("ALC-21", "Shaft walls / area separation walls", "NO APLICA", "No shaft wall / area separation wall in the set (A-202 schedules); roof hatch shaft framing A1/A-604 counted as 3-5/8\" stud + runner (RFI-14)."),
 ("ALC-22", "Rated assemblies (UL designs) and their board type", "NO APLICA", "Type VB, sprinklered (G-003): no UL rated partition or Type X board printed on A-202 / A-221 / A-907 / A-908 for our scope."),
 ("ALC-23", "Special panels (ballistic, lead-lined, abuse)", "NO APLICA", "None in the set (A-202, A-211, A-90x)."),
 ("ALC-24", "Finish level (Level 4 / Level 5)", "CUANTIFICADO", "Level 4 dining (A.4/A-211), Level 3 at tile / FRP substrate (C09250 3.5.D / A-909), Level 1 cooler (G.11/A-202), Level 5 play area WC-1 (A-050 KN12, A-211) as its own row; compound and tape by yield."),
]
alcances = [{"id": i, "nombre": n, "estado": e, "nota": x} for i, n, e, x in alc]
extra = [
 ("Wood framing / blocking / plywood / CDX / sheathing (Div. 06)", "EXCLUDED - wood framing / blocking (Div. 06), not in scope: W4, W4.1, W6, W8 interior wood stud walls (A-202 interior wall type schedule '2x4 / 2x8 WD STUD') and SW6 2x6 exterior walls (A-202 exterior schedule + S-101 note 4 'all perimeter and shear walls are 2x6 SYP @ 16\" O.C.'); wood blocking, 1/2\" / 3/4\" CDX plywood, SW6 structural sheathing; only their interior gypsum / cement board is ours (BOARD ONLY block). Metal alternative of the interior W walls: RFI-16 (closed, delta by program)."),
 ("Fasteners: screws, anchors, PAF", "EXCLUDED - estimator standing order: drywall / framing / cement board screws, anchors, PAF, Tapcon, bolts at 0 (C09250 2.5.B / A-909 noted)."),
 ("Framed openings for ducts", "EXCLUDED - estimator standing order: duct / air device openings in walls and ceilings never quantified (MEP sweep M-/P- sheets: 0 crossings of our metal walls)."),
 ("ACT ceilings and grid", "EXCLUDED - ACT-1 / ACT-2 and grid (A-221) and ACT grid demolition (A-052 KN1)."),
 ("Insulation", "EXCLUDED - batts B.1-B.5/A-202, mineral wool A1/A-605."),
 ("FRP panels", "EXCLUDED - FRP-2 (A-211, G.3 / G.4 / G.5/A-202): finish trade; its cement board substrate is ours."),
 ("Composeal waterproofing membrane", "EXCLUDED - Composeal / Kerdi membrane (G.3 / G.4/A-202, A-211)."),
 ("Tile", "EXCLUDED - CT-45, CT-57A, CT-72, CT-73B, CT-77, KT-6B tile (A-211, A-611, A-622): tile trade; its cement board substrate is ours."),
 ("Stainless steel panels", "EXCLUDED - S-1 stainless panels (A-201 KN25, A-211): other trade; cement board behind (G.6 / G.7) is ours."),
 ("Wallcovering", "EXCLUDED - WC-1 wallcovering (A-211); Level 5 under it is ours."),
 ("Paint", "EXCLUDED - PT-31A / 31B / 41 / 42 paint (A-211, A-221)."),
 ("Millwork", "EXCLUDED - millwork / casework / WD-3 wainscot (A-701, A-625)."),
 ("Prefabricated metal canopies", "EXCLUDED - order-point / meal-delivery canopies (A-104, A-105, OMD vendor sheets p48-63)."),
 ("Walk-in cooler / freezer panels", "EXCLUDED - walk-in panels and metal closure panels (A-221 KN2, A-050 KN22); the G.11 board on the walls around them is ours."),
 ("Signage", "EXCLUDED - signage (Signage.pdf, A-30x)."),
 ("Roof hatch clip angles", "EXCLUDED - 3\"x3\"x1/4\" clip angles @ 48\" at the roof hatch shaft (A1/A-604): structural / miscellaneous steel, not cold-formed framing."),
 ("Unistrut shelving supports", "EXCLUDED - Unistrut for suspended shelving and shrouds (K-001 equipment note 6): kitchen equipment / MEP trade."),
 ("MEP", "EXCLUDED - mechanical, plumbing, electrical work (M-, P-, E- sheets); hood unistrut supports A2/S-801 by MEP / vendor."),
 ("Roofing", "EXCLUDED - roofing and roof hatch unit (A-230, A1/A-604); only the hatch shaft metal framing is ours (RFI-14)."),
 ("Existing ceilings without type", "NO APLICA - every existing ceiling demolished by A-052 KN10 has its type printed ('gyp bd ceiling'); existing gyp ceilings to remain (A-221 legend) are not touched; no ceiling demo excluded for lack of information."),
 ("Demolition of gypsum board and metal framing", "QUANTIFIED - A-050 KN3 / KN4 / KN8 / KN24 walls, A-052 KN3 menu furr-down and KN10 gyp ceilings (DEMO-01..13, DEMO-C1..C6): demolition row in SF; heights RFI-10 / RFI-11 / RFI-12; A-050 KN10 / KN12 / KN29 finish removal and doors / windows not ours."),
]
for k, (n, x) in enumerate(extra, 1):
    alcances.append({"id": f"ALC-E{k:02d}", "nombre": n, "estado": "CUANTIFICADO" if x.startswith("QUANTIFIED") else "NO APLICA", "nota": x})

barrido = [
 {"item": "header", "specs": "found C09111 3.3.C.3 / A-909 (framed openings per drawings) - no opening in our metal walls", "schedule": "none: A-801 door schedule has no door in M2.1 / M3.5 / MB-01; A-202 schedules print no header", "estructural": "none: S-801 / S-201 show no header for our metal walls (wood headers Div. 06)"},
 {"item": "deflection clips", "specs": "none: C09111 / A-909 has no deflection clip requirement for these non-load-bearing walls", "schedule": "none: A-202 wall type schedule prints no deflection head", "estructural": "none: S-801 C2 / C3 show standard track / strongback, no clip"},
 {"item": "bracing", "specs": "found C09111 3.2.C / A-909 (bracing) -> bracing C.R. channel @ 48\" loaded", "schedule": "found A2/S-241 'BRIDGING LOCATION: MID SPAN' -> 1 row per dropped ceiling (RFI-09)", "estructural": "found C2/S-801 brace 362S162-33 @ 48\" (length not printed)"},
 {"item": "bridging", "specs": "found C09111 3.2.C / A-909", "schedule": "found A2/S-241 mid-span bridging", "estructural": "found S-241 (member not printed, RFI-09)"},
 {"item": "blocking", "specs": "none: C09111 / C09250 / A-909 print no metal backing plate requirement", "schedule": "none: no accessory / blocking schedule in the A sheets (F.1/A-202 wood blocking = Div. 06)", "estructural": "found A2/S-801 'cont. blkg. @ wall bracket typ.' and C2/S-801 '33 mil blkg. T&B' -> metal blocking loaded"},
 {"item": "backing", "specs": "none: no metal backing plate in A-90x", "schedule": "none", "estructural": "none: wood backing / blocking S-241, A4/A-624, A-602, A1/A-604 = Div. 06 EXCLUDED"},
]

proyecto_datos = list(pd)
td = {
 "proyecto": "Chick-fil-A #2284 River Point FSU Remodel, Sheridan, CO",
 "bid_set": "Bid Set.pdf (172 sheets, plotted 7/22-7/27/2026, rev. 3 PDC Reduction 2/4/2026; clean copy without markups)",
 "fecha": "2026-11-02",
 "inputs": {"waste_metal": 0.15, "waste_no_metal": 0.06, "sheet_w_ft": 4, "sheet_l_ft": 12, "stud_stock_ft": 20,
            "track_stock_ft": 10, "plan_scale_pt_per_ft": 18.0},
 "inputs_notas": {"drywall_screws_per_sf": "YIELD (Gypsum Association field / perimeter screw spacing); fasteners EXCLUDED in this project.", "lumber_stock_ft": "2x wood / FRT blocking: 16 ft sticks (estimator standing input; not used: wood is Div. 06 excluded).", "plan_scale_pt_per_ft": "A-202 / A-221 / A-050 / A-052 1/4\" = 1'-0\" (18 pt/ft), checked on A-202 M2.1 printed 14'-2\"."},
 "type_order": ["M2.1", "M3.5", "INFILL", "W4", "W4.1", "W6", "W8", "SW6"],
 "walls": [], "materials": [],
 "rfis": rfis, "rfi_cierre": cierre, "revisar": plantilla_excel.ordenar_revisar(revisar), "alcances": alcances,
 "proyecto_datos": proyecto_datos, "hojas_revisadas": hojas, "barrido_no_dibujado": barrido,
}
json.dump(td, open(os.path.join(K, "takeoff.json"), "w"), indent=1, ensure_ascii=False)
print("rfis open", len(rfis), "closed", len(cierre), "revisar", len(revisar), "alcances", len(alcances))
print(cierre["RFI-16"]["delta"])
