"""CR City Hotel: takeoff.json (formato plantilla_excel.py) desde el canon resuelto + proceso/proyecto_datos.json.
SOLO TEXTO: toda cantidad del Excel sale de familias_out.json vía plantilla_excel."""
import json, os, sys
sys.path.insert(0, sys.argv[1])
import plantilla_excel
K = '/root/cr/work'
C4 = f'{K}/etapas/4_canon'
c = json.load(open(f'{C4}/takeoff_canon.json'))
pd = json.load(open(f'{K}/proceso/proyecto_datos.json'))["proyecto_datos"]


def fmt(o):
    A, B = o.get("A") or {}, o.get("B") or {}
    return (f"(A) Drawings ({A.get('source', '')}): {A.get('texto', '')} - delta {A.get('delta', '')} | "
            f"(B) Code ({B.get('cita', 'n/a')}): {B.get('texto', '')} - delta {B.get('delta', '')} | (C) Other: ____")


cierre0 = {r["id"]: {"pregunta": r["question"] + " - CLOSED: " + r["resolved"]["answer"], "delta": r.get("delta_applied") or "0"} for r in c["rfis"] if r["status"] != "open"}
rfis = [{"id": r["id"], "pregunta": f"{r['question']} - carried: {r['loaded']} (conservative value loaded). " + r["barrido"]["swept_txt"],
         "delta": fmt(r["opciones"]), "opciones": r["opciones"], "source": r["source"], "barrido": r["barrido"],
         "img": r["barrido"]["lugares"][0]["img"]} for r in c["rfis"] if r["status"] == "open"]
cierre = dict(cierre0, **{
 "A/B-heights": {"pregunta": "Readings A and B used different wall heights - CLOSED by the printed sections of each zone: L2-L3 room zone 9'-2 7/8\" (4/A5.05), corridor 11'-0\" - 1'-1 3/8\" (7/A7.23), L4 8'-11 1/4\" (1/A5.06), grid 8 11'-4 3/4\" (2/A5.01), L1 12'-0\" / 14'-0\" stairs (resolucion_L1..L4)", "delta": "0 (applied)"},
 "A/B-W.6.1": {"pregunta": "Tag 'W.6.1' typed differently by A and B - CLOSED by rule R2 (W.6 with the printed rating) + RFI-01", "delta": "see RFI-01"},
 "A/B-FW rating": {"pregunta": "FW tags printed without rating digit - CLOSED: every FW row of A0.06 has rating '--' (FW.x-0)", "delta": "0"},
})
RI = [
 ("floor_plan", "XW.6.3", None, "A2.01-A2.04 / A0.07", "Exterior walls: interior face(s) and exterior gypsum sheathing layers per A0.07 rating rows; wood studs, LP Flameblock and siding EXCLUDED. Review the exterior gypsum sheathing height per floor (full floor-to-floor 11'-0\" loaded on the exterior face).", "RFI-02.png"),
 ("floor_plan", "W.62", None, "A2.02-A2.04 / A0.06", "Guest-room corridor walls W.62-1 (2 layers each side, 1 HR): board to the underside of the floor framing per zone; verify corridor-side height 9'-10 5/8\" (7/A7.23).", "RFI-01.png"),
 ("floor_plan", "GYP-1", None, "A3.01-A3.04 / A7.23", "GYP-1 dropped ceilings carried on metal suspension (RFI-12); perimeter angle by square-equivalent perimeter (DERIVED).", "RFI-12.png"),
]
revisar = []
for f, t, o, h, txt, img in RI:
    it = {"fase": f, "punto": txt + f" Source {h}.", "hoja_detalle": h, "imagen": img}
    if t: it["type"] = t
    revisar.append(it)
hojas = [
 {"categoria": "cover / index / code", "estado": "reviewed", "hojas": "T0.00 cover + project team, T0.01 index and standards, A0.00 code summary (IBC 2018, Type IIIB, R-1 / M / U / A-2, sprinklered), A0.01-A0.03 code plans / sections"},
 {"categoria": "general notes", "estado": "reviewed", "hojas": "A0.06 partition types general notes 1-25, A2.01-A2.04 floor plan general notes 1-10 (note 4 water resistant board at toilet / lavatory)"},
 {"categoria": "demolition + notes", "estado": "reviewed - none for our trade", "hojas": "C0.00 civil demolition plan (site) only; new building"},
 {"categoria": "specs", "estado": "reviewed", "hojas": "Project Manual Vol 1: 05 40 00, 06 10 00, 07 21 00, 07 84 13, 07 92 00, 09 21 16.23, 09 22 16, 09 29 00 (cited per row); Vol 2 MEP"},
 {"categoria": "partition types + details", "estado": "reviewed", "hojas": "A0.06 interior wall assemblies (W / FW / DW / FI / CH / C / CM + stud schedule), A0.07 exterior wall assemblies (XW / XFW / XI), A0.08 horizontal assemblies (RS-1..7, FS-1, MB-1), A0.09-A0.11 rated intersections"},
 {"categoria": "floor plans", "estado": "reviewed", "hojas": "A2.01 LVL 1, A2.02 LVL 2, A2.03 LVL 3, A2.04 LVL 4, A2.05 roof"},
 {"categoria": "RCP", "estado": "reviewed", "hojas": "A3.01-A3.04 overall RCP, A7.00 / A7.05 / A7.09 / A7.13 / A7.16 unit RCPs, A7.23 / A7.24 corridor RCP + 7/A7.23 corridor ceiling detail, A7.31 lobby RCP, A7.45 / A7.50 / A7.55 RCPs"},
 {"categoria": "elevations / sections", "estado": "reviewed", "hojas": "A4.00-A4.05 elevations / building sections, A5.00-A5.08 enlarged wall sections (4/A5.05 floor zones, 1/A5.06, 2/A5.01, 2/A5.04)"},
 {"categoria": "enlarged / interior elevations", "estado": "reviewed", "hojas": "A6.00-A6.02 elevator / stairs, A7.00-A7.18 unit plans + room elevations (vector-only pages read by image), A7.20-A7.22 corridor elevations, A7.30-A7.35 lobby, A7.45, A7.50, A7.55"},
 {"categoria": "schedules", "estado": "reviewed", "hojas": "A7.19 interior finish schedules (TF-1 plaster / wallcovering, P-1 / P-2 paint), A8.00 door schedules, A8.01 window schedule, A8.02 fenestration details"},
 {"categoria": "structural", "estado": "reviewed", "hojas": "S0.00-S5.02 (wood trusses / joists, steel beams; framing heights and lintels are wood / steel by others)"},
 {"categoria": "MEP", "estado": "reviewed", "hojas": "M1.01, M1.05, M3.02, P0.01-P5.00, E0.00-E3.01 swept for crossings / access panels; ducts EXCLUDED by standing order"},
]
fo = json.load(open(f'{C4}/out/familias_out.json'))["familias"]
A = [
 ("ALC-01", "NO APLICA", "Interior partitions are WOOD framed (A0.06 WOOD / FURRED WOOD / DBL. WOOD / FURRED INSULATION, A2.01-A2.04): framing EXCLUDED (Div. 06, R80f.1 / U-139). Metal framing only at C-H shaft walls (ALC-21)."),
 ("ALC-02", "NO APLICA", "Exterior walls are FRT 2x6 WOOD studs (A0.07 XW types): framing EXCLUDED (Div. 06); interior board and exterior gypsum sheathing carried (ALC-07 / ALC-09)."),
 ("ALC-03", "NO APLICA", "Parapets are wood framed (A2.05, A9.02, A9.05): EXCLUDED (Div. 06); A0.01 / A0.02 / A8.02 parapet mentions are code / flashing."),
 ("ALC-04", "NO APLICA", "No metal stud partitions: A0.06 GN 7 deep-leg deflection track applies to metal studs only (none in the set); C-H shaft walls use J runner (ALC-21)."),
 ("ALC-05", "NO APLICA", "Headers / sills / jambs at openings in wood walls are wood (A0.06, A5.00-A5.05, S2.01-S2.04): EXCLUDED (Div. 06). Gypsum board returns at windows: see trim / returns."),
 ("ALC-06", "NO APLICA", "No metal stud bracing / bridging: wood framing (A5.01, S1.02-S1.05 are wood blocking / bridging, Div. 06); P0.01 is plumbing."),
 ("ALC-07", "CUANTIFICADO", "5/8\" Type X gypsum board per face and layers per type and rating (A0.06, A0.07), board-only on wood walls, L1-L4 by floor (A2.01-A2.04, A0.08, A0.10)."),
 ("ALC-08", "CUANTIFICADO", "5/8\" Type X water resistant board at toilet / lavatory / shower / janitor faces (A0.06 GN 11 / GN 12, A2.01-A2.04 note 4)."),
 ("ALC-09", "CUANTIFICADO", "5/8\" Type X exterior gypsum sheathing per A0.07 XW rows (XW.6.3-2 / XW.6.4-2 2 layers, XW.6.6-x 1 layer) (A0.02, A0.06, A0.08, A0.10, A2.05, A5.04)."),
 ("ALC-10", "NO APLICA", "EXCLUDED - wood (Div. 06): FRT plywood / LP Flameblock sheathing (A0.07, A0.08, A2.05, A7.30, A9.03, S5.01)."),
 ("ALC-11", "CUANTIFICADO", "Gypsum board ceilings: FS-1 5/8\" Type C on resilient channel (A0.08), RS-1 under roof (A0.08, A3.04), GYP-1 / GYP-2 dropped ceilings (A3.01-A3.04, A7.00, A7.23)."),
 ("ALC-12", "CUANTIFICADO", "Ceiling suspension: resilient channel at FS-1 / RS-1 (A0.08) and USG drywall suspension for GYP-1 / GYP-2 (RCP legend 'ON METAL SUSPENSION SYSTEM', RFI-12) with hanger wire (A7.23; P0.01 / S1.02 / S1.05 / S3.02 / S3.04 are other trades)."),
 ("ALC-13", "CUANTIFICADO", "Soffits / coves: corridor perimeter bands 1/A7.23, 1/A7.24, 7/A7.23 (L2-L4), lobby coffers 2/A7.31, L4 stair soffit 11/A6.01 (A0.10, A5.00-A5.02 are wood framing)."),
 ("ALC-14", "NO APLICA", "No canopy / marquee in our trade: A5.03 / A9.05 canopy is steel / wood by others (S1.02, S3.10)."),
 ("ALC-15", "NO APLICA", "No column furring / wraps printed for our trade (A2.01-A2.04); L1 retail steel beam wraps by future tenant (RFI-05 / RFI-18)."),
 ("ALC-16", "NO APLICA", "Blocking is WOOD (A0.05 accessibility, A0.09, A2.05, A7.32, A9.02, A9.04): EXCLUDED (Div. 06, U-139); no metal blocking printed."),
 ("ALC-17", "NO APLICA", "EXCLUDED - framed openings for ducts / diffusers (standing order); no access panels in gypsum scheduled (A8.00, M1.01, M1.05, P4.00, P4.01, T0.01 legend)."),
 ("ALC-18", "CUANTIFICADO", "Corner bead / L-bead / U-bead per 09 29 00 2.5 and control joints per A0.06 GN 15 (A3.01-A3.04, A7.00): quantities from window returns and outside corners (window schedule A8.01 + elevations A4.00-A4.03, measured by program)."),
 ("ALC-20", "CUANTIFICADO", "5/8\" cement board (CBU) at tile walls of guest baths (A0.06 GN 13; 09 29 00 2.4.A.2 'match adjacent panel thicknesses'; A2.01-A2.04); FRP is exterior XI.2.7 on CMU (A0.07) - not ours; no FRP interior finish (A7.19)."),
 ("ALC-21", "CUANTIFICADO", "C-H shaft walls CH.6-2 (A0.06, A9.03, A5.08): 6\" 20 GA C-H studs @ 24\" o.c., J runner (A0.06 'SHAFT SIDE \"J\" RUNNER CHANNEL'), 1\" shaftliner + 2 layers 5/8\" Type X (UL U415); S2.02 elevator pit is concrete."),
 ("ALC-22", "CUANTIFICADO", "Rated assemblies per A0.00-A0.03 code plans and A0.06 / A0.07 / A0.08 UL designs (U379, U301, U341, U415, V337, L546): Type X layers per rating loaded."),
 ("ALC-23", "NO APLICA", "No ballistic / lead-lined / abuse-resistant panels in the set (A0.06, A7.19)."),
 ("ALC-24", "CUANTIFICADO", "Level 4 finish on all board (09 29 00 3.6.E.4: under plaster / wallcovering and back of house); no Level 5 area (A7.19 TF-1 plaster / vinyl wallcovering everywhere); compound and tape by yield (A0.00-A0.04, A0.09 are code text)."),
]
reg = json.load(open(f'{K}/registro.json'))
NOMB = {r["id"]: r.get("ubicacion") for r in reg["renglones"]}
alcances = [{"id": i, "nombre": NOMB.get(i, i), "estado": e, "nota": x} for i, e, x in A]
alcances.append({"id": "ALC-19", "nombre": NOMB.get("ALC-19", "ALC-19"), "estado": "NO APLICA", "nota": "EXCLUDED in all projects (estimator standing order): acoustical sealant (A0.06 GN 18, A2.01-A2.04 double-line partitions) and sound attenuation / batt insulation."})
extra = [
 ("Wood framing / blocking / sheathing (Div. 06)", "EXCLUDED - wood studs, plates, trusses, blocking, FRT plywood, LP Flameblock (A0.06, A0.07, A0.08, S-sheets): Div. 06 (U-139)."),
 ("Fasteners: screws, anchors, PAF", "EXCLUDED - estimator standing order (U-053)."),
 ("Framed openings for ducts / penetrations", "EXCLUDED - estimator standing order (R-ALC-03)."),
 ("ACT / wood slat ceilings", "EXCLUDED - ACT-1 / ACT-2 / ACT-3 lay-in and WS-1 wood slat ceilings (A3.01-A3.04, A7.23, A7.31): other trades."),
 ("Insulation", "EXCLUDED - batt / mineral fiber / rigid insulation (A0.06, A0.07, A0.08)."),
 ("Plaster / wallcovering / paint", "EXCLUDED - TF-1 plaster, vinyl wallcovering, P-1 / P-2 paint (A7.19)."),
 ("CMU / concrete walls", "EXCLUDED - CM.x CMU and C.x cast-in-place concrete walls (A0.06, A6.00-A6.02): masonry / concrete trades."),
 ("Separate-permit areas", "EXCLUDED - grey toned area 'UNDER A SEPARATE PERMIT AND NOT IN SCOPE' (A2.01-A2.04); existing historic building (A0.00)."),
 ("Doors, frames, windows, hardware", "EXCLUDED - A8.00 / A8.01 by others."),
 ("Structural steel: kickers, clip angles, L3x3 angles", "EXCLUDED - L3x3x1/4 KICKER at 4'-0\" o.c. (S1.02, 5/S3.08) and CLIP ANGLE with threaded rods into masonry (S3.04, S3.08) are structural steel (Div. 05 12 00), by the steel fabricator."),
]
for k, (n, x) in enumerate(extra, 1):
    alcances.append({"id": f"ALC-E{k:02d}", "nombre": n, "estado": "NO APLICA", "nota": x})
barrido = [
 {"item": "header", "specs": "found 06 10 00 (wood headers, Div. 06)", "schedule": "none: no metal header schedule", "estructural": "found S2.01-S2.04 wood / steel headers (by others)"},
 {"item": "deflection clips", "specs": "found 05 40 00 2.x vertical deflection clips (cold-formed framing, none drawn in this set)", "schedule": "none", "estructural": "none: wood framing"},
 {"item": "bracing", "specs": "found 09 22 16 3.x bracing for metal partitions (no metal partitions)", "schedule": "none", "estructural": "found S1.02-S1.05 wood bridging (Div. 06)"},
 {"item": "bridging", "specs": "found 05 40 00 bridging (cold-formed, not used)", "schedule": "none", "estructural": "found S-sheets wood"},
 {"item": "blocking", "specs": "found 06 10 00 wood blocking", "schedule": "none", "estructural": "none: wood blocking A9.02 / A9.04 (Div. 06)"},
 {"item": "backing", "specs": "found 09 22 16 2.x flat strap and backing plate (not drawn)", "schedule": "none", "estructural": "none"},
]
td = {
 "proyecto": "CR City Hotel - 415 Perry Street, Castle Rock, CO 80104 (new 4-story hotel, Type IIIB, wood framed)",
 "bid_set": "2026 Permit Drawings: Architectural 4.22.2026 (86 sheets T0.00-A9.06), Structural 4.22.2026 (26), Mech/Plumb 6.1.2026 (15), Electrical 6.1.2026 (21), Project Manual Vol 1 & 2 4.25.2025; 2025 Full Drawing Set superseded; architect stamps removed in the working copy (no take-off markups)",
 "fecha": "2026-11-05",
 "inputs": {"waste_metal": 0.15, "waste_no_metal": 0.06, "sheet_w_ft": 4, "sheet_l_ft": 12, "stud_stock_ft": 20,
            "track_stock_ft": 10, "plan_scale_pt_per_ft": 9.0, "bod_ft": 11.0},
 "inputs_notas": {"bod_ft": "Floor to floor L2-L4 11'-0\" (4/A5.05); L1-L2 14'-0\"; board heights per zone in the Partition Takeoff.",
                  "plan_scale_pt_per_ft": "A2.01-A2.04 1/8\" = 1'-0\" (9 pt/ft); enlarged plans 1/4\" = 1'-0\" (18 pt/ft).",
                  "drywall_screws_per_sf": "YIELD; fasteners EXCLUDED (estimator standing order)."},
 "type_order": ["W.4-0", "W.6-0", "W.6-1", "W.6-2", "W.62-1", "FW.1-0", "FW.2-0", "FW.4-0", "FW.6-0", "DW.4-1", "FI.2-0", "FI.6-0", "CH.6-2",
                "XW.6.2-0", "XW.6.2-2", "XW.6.3-0", "XW.6.3-2", "XW.6.4-0", "XW.6.4-2", "XW.6.6-1", "XW.6.6-2"],
 "walls": [], "materials": [],
 "rfis": rfis, "rfi_cierre": cierre, "revisar": plantilla_excel.ordenar_revisar(revisar), "alcances": alcances,
 "proyecto_datos": pd, "hojas_revisadas": hojas, "barrido_no_dibujado": barrido,
}
json.dump(td, open(f'{K}/takeoff.json', 'w'), indent=1, ensure_ascii=False)
print("rfis", len(rfis), "alcances", len(alcances))
