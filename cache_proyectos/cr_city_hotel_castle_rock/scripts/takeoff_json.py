"""CR City Hotel: takeoff.json (formato plantilla_excel.py) desde el canon resuelto + proceso/proyecto_datos.json.
SOLO TEXTO: toda cantidad del Excel sale de familias_out.json vía plantilla_excel."""
import json, os, sys, re
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


cierre0 = {r["id"]: {"pregunta": r["question"] + f" - CLOSED ({r['id']}, decision: {r['resolved']['source']}): " + r["resolved"]["answer"], "delta": r.get("delta_applied") or "0"} for r in c["rfis"] if r["status"] != "open"}
rfis = [{"id": r["id"], "pregunta": f"{r['question']} - carried: {r['loaded']} (conservative value loaded). " + r["barrido"]["swept_txt"],
         "delta": fmt(r["opciones"]), "opciones": r["opciones"], "source": r["source"], "barrido": r["barrido"],
         "img": r["barrido"]["lugares"][0]["img"]} for r in c["rfis"] if r["status"] == "open"]
cierre = dict(cierre0, **{
 "A/B-heights": {"pregunta": "Readings A and B used different wall heights - CLOSED by the printed sections of each zone: L2-L3 room zone 9'-2 7/8\" (4/A5.05), corridor 11'-0\" - 1'-1 3/8\" (7/A7.23), L4 8'-11 1/4\" (1/A5.06), grid 8 11'-4 3/4\" (2/A5.01), L1 12'-0\" / 14'-0\" stairs (resolucion_L1..L4)", "delta": "0 (applied)"},
 "A/B-W.6.1": {"pregunta": "Tag 'W.6.1' typed differently by A and B - CLOSED by rule R2 (W.6 with the printed rating) + RFI-01", "delta": "see RFI-01"},
 "A/B-FW rating": {"pregunta": "FW tags printed without rating digit - CLOSED: every FW row of A0.06 has rating '--' (FW.x-0)", "delta": "0"},
})
def _w(i):
    return next(w for w in c["walls"] + c["existing_walls"] if w["id"] == i)
_bwn = round(float(next(m for m in c["misc_items"] if m["ref"] == "BW-L1-RETAIL board")["qty"]) - 296.78, 2)
_l25, _h25 = float(_w("W.6-L1-25")["length_ft"]), float(_w("W.6-L1-25")["height_ft"])
_l17, _h17 = float(_w("W.6-L1-17 A")["length_ft"]), float(_w("W.6-L1-17 A")["height_ft"])
_l20, _h20 = float(_w("W.6-L1-20 C")["length_ft"]), float(_w("W.6-L1-20 C")["height_ft"])
RI = [
 ("floor_plan", "W.6", None, "1/A7.50 / A8.00 / A0.00", f"W.6-L1-25 (ELEC/TELE 120 south wall, 2 HR by door 120.1 90 MIN, IBC 2018 Table 716.1(2)): the {_l25}-ft run holds door 120.1 - A8.00 schedule prints 5'-0\" x 8'-0\" while 1/A7.50 dimensions the opening 7'-11\" (two leaves drawn): door-schedule vs plan conflict; loaded GROSS per U-057 (openings not deducted) = {_l25} x {_h25} x 2 faces x 2 layers = {round(_l25 * _h25 * 4, 2)} SF board; delta if the opening is deducted: schedule 5.0 x 8.0 x 4 = -160.00 SF / plan width 7.92 x 8.0 x 4 = -253.44 SF 5/8\" Type X.", "RI_W6-L1-25_door_120_1.png"),
 ("floor_plan", "XW.6.3", None, "A2.01-A2.04 / A0.07", "Exterior walls: interior face(s) and exterior gypsum sheathing layers per A0.07 rating rows; wood studs, LP Flameblock and siding EXCLUDED. Review the exterior gypsum sheathing height per floor (full floor-to-floor 11'-0\" loaded on the exterior face).", "RFI-02.png"),
 ("floor_plan", "W.62", None, "A2.02-A2.04 / A0.06", "Guest-room corridor walls W.62-1 (2 layers each side, 1 HR): board to the underside of the floor framing per zone; verify corridor-side height 9'-10 5/8\" (7/A7.23).", "RFI-01.png"),
 ("floor_plan", "GYP-1", None, "A3.01-A3.04 / A7.23", "GYP-1 dropped ceilings carried on metal suspension (RFI-12); perimeter angle by square-equivalent perimeter (DERIVED).", "RFI-12.png"), ("floor_plan", "GYP-1", None, "1/A7.31 / A5.04 / A0.00", "BAR 107 suspended gyp field CLG-L1-125 125.98 SF at 11'-0\" LOADED (A5.04 'BAR SUSPENDED GYP CEILING' + 3/A7.31 govern A0.00 'core and shell', R-ALC-10); RFI-22 option B delta -125.98 SF board + grid.", "RCPREV_F1_bar107_A731.png"),
 ("floor_plan", "GYP-1", None, "2/A7.50", "L1 lobby south strip (rows 7-8) GYP-1 11'-0\" 119.0 SF added (it had no row).", "RCPREV_F2_lobby_south_A750.png"),
 ("floor_plan", "GYP-1", None, "A3.01 / 1/A7.31 / 1/A2.01", "The GYP-1 11'-0\" band south of the storefront is INSIDE Retail 124 (between grid 7 and 8, RETAIL 124 room and the note '*NOTE: GYPSUM BOARD & FINISH IN RETAIL SPACE BY FUTURE TENANT') = by tenant, not loaded (RFI-05; delta +346.4 SF if ours).", "RCPREV_F3_retail_band_A301.png"),
 ("floor_plan", "GYP-1", None, "1/A3.02 / 2/A7.05", "L2 Cleaning 215 (123.0 SF) and closets 222 / 223 (19.4 + 8.7 SF) GYP-1 9'-2\" were priced only as the FS-1 membrane above; the GYP-1 dropped ceiling (board + suspension) is added, like L3 322 / 323.", "RCPREV_F4_cleaning215_A302.png"),
 ("floor_plan", "GYP-2", None, "3/A7.45 / A3.01", "GENERATOR 103 GYP-2 (MB-1, 3 layers) measured as the L-shaped room to the gate line: 200.4 SF (was 181.7).", "RCPREV_D4_generator103_A745.png"),
 ("floor_plan", "WS-1", None, "1/A7.23 / 1/A7.24 (L2, L3, L4)", "WS-1 wood slat panels (other trade) deducted from the GYP-1 corridor ceilings, measured on the vector slats: N-S corridor 34.5 + 60.3 SF, E-W corridor 39.9 SF per floor (L2 216 / 218, L3 316 / 318, L4 412). At L2 / L3 the FS-1 rated floor / ceiling membrane (A0.08 FS-1, 1 HR) stays full above the WS-1; at L4 the ceiling under the roof is RS-1, unrated (A0.08 RS-1 rating blank, 'CEILING RE: RCP'; A0.00 'ROOF CONSTRUCTION 0 HR'), and the RCP 1/A3.04 prints WS-1 in the three zones -> no gypsum above the WS-1 at L4: the three zones are EXCLUDED on 1/A3.04 (delta if gypsum were required above them: see Scope ALC-E WS-1 L4).", "RCPREV_D2_WS1_A723.png"),
 ("floor_plan", "GYP-1", None, "1/A7.31", "Niche between BAR 107 and toilets 110 / 111 (40.2 SF) was outside CLG-L1-08; added at 11'-0\" (U-146 higher adjacent height, no cut line drawn).", "RCPREV_D6_niche_A731.png"),
 ("floor_plan", "FS-1", None, "S1.02 / A3.01 / A0.08", f"Retail 124 north edge beams (S1.02 '(MF) W27X94', '(MF) W21X50', 'W24X55', 68.8 LF measured on S1.02) are deeper than the 18\" floor trusses: loaded as part of the FS-1 membrane wrap (bottom + inside face, A0.08 FS-1 'GYP AND RESILIENT CHANNELS WRAP STEEL BEAMS WHERE THEY ARE DEEPER THAN TRUSSES'); A3.01 draws them dashed above the GYP-1 11'-0\" storefront band (tenant, RFI-05) and does not tag them 'WRAP'; delta if the band encloses them and no wrap is required: -{_bwn} SF Type C, -137.6 LF RC.", "MISC_BW-L1-RETAIL_N_S102.png"),
 ("floor_plan", "W.6.1", None, "1/A7.50 / A8.00", f"Toilet 112 east wall W.6-L1-17: 1/A7.50 tags it 'W.6.1 | 2' (loaded 2 HR, 2 layers each face) but A8.00 lists door 112.1 TOILET with NO fire rating (a 2 HR fire barrier door would be 90 MIN, A8.00 'FIRE WALLS AND FIRE BARRIES HAVING 2HR RATING: 90 MIN'; CODE: IBC 2018 Table 716.1(2)): plan-vs-plan conflict kept at the printed wall tag; delta if the wall is non-rated: -{round(_l17 * _h17 * 2, 2):.2f} SF Type X [DERIVED {_l17} x {_h17} x 2 faces x 1 layer].", "RI_H7_door_112_1_A800.png"),
 ("floor_plan", "W.6.1", None, "1/A7.50 / A8.00 / A0.00", f"DATA 118B west wall W.6-L1-20 C: loaded 2 HR by the estimator's code review of 2026-11-06 (A0.00 'ELECTRICAL AND IT ROOMS - 2 HR', RFI-24), but 1/A7.50 tags it 'W.6.1 | 0' and A8.00 lists door 118.1 DATA with NO fire rating: confirmed by the user 11-nov (RFI-24 'A: 2 HR (cargado)', U-161); if the west wall is 0 HR: delta -{round(_l20 * _h20 * 2, 2):.2f} SF Type X [DERIVED {_l20} x {_h20} x 2 faces x 1 layer] (not an alternate: user decision).", "RI_H1_door_118_1_A800.png"),
 ("floor_plan", "CH", None, "7/A9.03 / 8/A9.03 / A0.06", "Shaft walls of the L2-L4 north / south shafts (CH-L2/L3/L4-01..07): the bubbles call 7/A9.03 and 8/A9.03, which print a 4 3/4\" 2-HOUR SHAFTWALL (W419, U497) = 2 1/2\" C-H + 1\" liner + 2 x 5/8\"; loaded with 2-1/2\" C-H studs and J-runner (the detail governs, U-115). A0.06 CH.6-2 prints 6\" C-H: if 6\" is required, the same C-H stud and J-runner LF change to 6\" (RFI-07).", "RI_R1_A903_shaftwall.png"),
 ("floor_plan", "RS-1", None, "A0.08 RS-1 / A7.13 / A7.16", "L4 guest rooms 401-405 carry RS-1 under the roof 'excl. bath' while L2 / L3 carry FS-1 continuous: correct as printed - FS-1 is printed for LEVEL 2, 3, 4 with location THROUGHOUT on A0.08 (rated floor membrane, continuous above the dropped bath GYP-1), RS-1 prints no rating / UL (non-rated roof ceiling) so the bath GYP-1 8'-6\" is the only ceiling there. No change.", "RFI-15.png"),
 ("floor_plan", "ACT-1", None, "A3.01 / A7.32", "Vestibule 114 ceiling = ACT-1 (A3.01, other trade) - no gypsum; A7.32 is the glass entry vestibule 108.x (no ceiling of its own). No change.", "RCPREV_V114_A301.png"),
 ("floor_plan", "FS-1", None, "A0.08 FS-1 / 1/A2.01", "The L1 FS-1 membrane (underside of the LEVEL 2 floor) includes Retail 124 (2,373 SF printed) and Kitchen 100 (682.7 SF, flood fill of 1/A2.01): kept because the 1 HR floor assembly is printed (RFI-05 criterion: rated stays); delta -3,055.7 SF Type C + resilient channel if the tenant builds it.", "RFI-05.png"),
 ("floor_plan", "FI.2", None, "1/A2.01", "Walls facing Retail 124 (RFI-05 sweep of every -0 wall): XW.6.4-L1-04 excluded; XW.6.3-L1-01 and FI.2-L1-06 split at the measured tenant boundary - see Excluded walls.", "RCPREV_W_retail_A201_FI2.png"),
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
 ("ALC-14", "CUANTIFICADO", "Entry canopy soffit (08/A9.05 'GYP/METAL SOFFIT PANEL'): 6.49 ft (2/A5.03) x 4.85 ft (08/A9.05) = 31.48 SF exterior gypsum soffit board + 16.19 LF edge trim (CAN-L1-ENTRY, RFI-21); the canopy structure (steel plate / HSS hangers) is by others (S1.02, S3.10)."),
 ("ALC-15", "NO APLICA", "No column furring printed for our trade (A2.01-A2.04). L1 retail steel BEAM wraps = part of the rated FS-1 membrane (A0.08 FS-1 note): carried as BW-L1-RETAIL (Type C + resilient channel, side height RFI-20)."),
 ("ALC-16", "NO APLICA", "Blocking is WOOD (A0.05 accessibility, A0.09, A2.05, A7.32, A9.02, A9.04): EXCLUDED (Div. 06, U-139); no metal blocking printed."),
 ("ALC-17", "NO APLICA", "EXCLUDED - framed openings for ducts / diffusers (standing order); no access panels in gypsum scheduled (A8.00, M1.01, M1.05, P4.00, P4.01, T0.01 legend)."),
 ("ALC-18", "CUANTIFICADO", "Corner bead / L-bead / U-bead per 09 29 00 2.5 and control joints per A0.06 GN 15 (A3.01-A3.04, A7.00): quantities from window returns and outside corners (window schedule A8.01 + elevations A4.00-A4.03, measured by program)."),
 ("ALC-20", "CUANTIFICADO", "5/8\" cement board (CBU) at tile walls of guest baths (A0.06 GN 13; 09 29 00 2.4.A.2 'match adjacent panel thicknesses'; A2.01-A2.04); FRP is exterior XI.2.7 on CMU (A0.07) - not ours; no FRP interior finish (A7.19)."),
 ("ALC-21", "CUANTIFICADO", "C-H shaft walls (A0.06 CH, A9.03, A5.08): L2-L4 north / south shafts (7/A9.03, 8/A9.03 4 3/4\" 2-HOUR SHAFTWALL W419 / U497) 2-1/2\" 20 GA C-H studs + 2-1/2\" J runner; L1 / L4 chase CH.6 (1/A7.50) 6\" 20 GA C-H + 6\" J runner (A0.06 'SHAFT SIDE \"J\" RUNNER CHANNEL'); studs @ 16\" o.c. (A0.06 GN 6 'ALL METAL STUDS TO BE SPACED @ 16\" O.C.') to the height of the liner, 1\" shaftliner + 2 layers 5/8\" Type X; S2.02 elevator pit is concrete."),
 ("ALC-22", "CUANTIFICADO", "Rated assemblies per A0.00-A0.03 code plans and A0.06 / A0.07 / A0.08 UL designs (U379, U301, U341, U415, V337, L546): Type X layers per rating loaded."),
 ("ALC-23", "NO APLICA", "No ballistic / lead-lined / abuse-resistant panels in the set (A0.06, A7.19)."),
 ("ALC-24", "CUANTIFICADO", "Level 4 finish on all board (09 29 00 3.6.E.4: under plaster / wallcovering and back of house); no Level 5 area (A7.19 TF-1 plaster / vinyl wallcovering everywhere); compound and tape by yield (A0.00-A0.04, A0.09 are code text)."),
 ("ALC-25", "CUANTIFICADO", "Roof assemblies A0.08 tagged on the roof plan A2.05 (swept tag by tag): RS-1 x3 -> L4 ceilings 'RS-1' (board on channel, A3.04); RS-2 x3 and RS-3 x2 -> no board in the assembly (ceiling 'RE: REFLECTED CEILING PLANS' = the RCP rows below); RS-4 x1 (Deck Bar 411) 'CEILING ASSEMBLY - TBD' -> not in scope (A7.55 'INTERIOR OF FOOD AND BEVERAGE SPACE IS NOT IN SCOPE OF THIS PERMIT'); RS-5 x2 -> membrane on METAL DECK, no gypsum; RS-6 x2 -> 2 LAYERS 5/8\" TYPE 'X' loaded as RS-6 rows 'RS6-L3 board' (terrace 420 / 421 over 301-304) and 'RS6-L3-309 board' (covered deck over 309); RS-7 x1 -> steel roof tile, no gypsum."),
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
 ("Food & Beverage interiors (L1 Kitchen 100 / Dining, L4 410 / 411 / 419; BAR 107 except its printed ceiling)", "EXCLUDED - 'INTERIOR OF FOOD AND BEVERAGE SPACE IS NOT IN SCOPE OF THIS PERMIT. WILL BE SUBMITTED IN FUTURE TENANT IMPROVEMENT PERMIT.' (1/A2.04, A3.04, A7.45, A7.50, A7.55) + A0.00 'core and shell': non-rated faces and ceilings by the tenant; rated walls and the FS-1 rated floor / ceiling membranes stay (RFI-05 criterion); the RS-1 roof ceiling is unrated (A0.08 RS-1 rating blank, A0.00 'ROOF CONSTRUCTION 0 HR') and is not loaded inside the F&B rooms. Exception, BAR 107 ceiling: A5.04 'BAR SUSPENDED GYP CEILING' / 'CLG 11'-0\"' and 3/A7.31 'SECTION - BAR CEILING' are printed -> loaded by R-ALC-10 (the specific drawing governs A0.00 'core and shell'), CLG-L1-125 125.98 SF; delta if the bar is F&B tenant work: -125.98 SF board + grid (RFI-22)."),
 ("F&B 410 / 411 rated faces kept (U-159)", "LOADED - tenant-side faces of RATED types stay: their layers are part of the rated assembly (U-159: in F&B exclusions the rated membrane is verified): XW.6.6-L4-17 B (XW.6.6-2, 2 HR exterior wall, 2 layers, 502.65 SF), XW.6.6-L4-18 B (XW.6.6-1, 122.85 SF), W.62-L4-05 / -06 (W.62-1, 139.01 + 47.18 SF), X-L4-03 B (DW.4-1, 169.9 SF), FW.4-L4-19 B (FW.4-1 1 HR, 127.1 SF); ratings per the A0.06 / A0.07 type rows and A0.02 code plan, tags on 1/A2.04; the F&B note (1/A2.04, 3/A5.07) excludes only non-rated tenant interior work."),
 ("Retail 124 tenant finishes", "EXCLUDED - A2.01 '*NOTE: GYPSUM BOARD & FINISH IN RETAIL SPACE BY FUTURE TENANT': non-rated retail faces (incl. the sweep of every -0 wall: XW.6.4-L1-04, retail parts of XW.6.3-L1-01 and FI.2-L1-06) and the GYP-1 11'-0\" band inside the retail (RFI-05)."),
 ("Separate-permit areas", "EXCLUDED - grey toned area 'UNDER A SEPARATE PERMIT AND NOT IN SCOPE' (A2.01-A2.04); existing historic building (A0.00)."),
 ("Doors, frames, windows, hardware", "EXCLUDED - A8.00 / A8.01 by others."),
 ("Shaft base steel support platform + fireproofing (1/A5.08)", "EXCLUDED - 'STEEL SUPPORT PLATFORM WITH 2HR RATED FIRE PROOFING' at the base of the north shaft (1/A5.08, 11/A9.03): structural steel and spray fireproofing = other trades (user decision 11-nov, U-163: only gypsum board + metal framing); the 2HR shaft ceiling gypsum + liner + C-H / J-track is loaded (CLG-L1-SHN / SHS)."),
 ("WATER ENTRY 128 ceiling (1/A3.01)", "EXCLUDED - no ceiling tag or hatch printed in 128 on 1/A3.01 and none required by code (IBC 2018 Section 913.2.1 exception 1; Table 601 roof 0 HR): user decision 11-nov (RFI-17, U-162). Delta if a GYP-1 ceiling were added: +188.01 SF Type X + grid."),
 ("WS-1 wood slat ceiling zones L4 (1/A3.04)", "EXCLUDED - the three WS-1 zones of the L4 corridor 412 (N-S corridor, lobby zone, E-W corridor) print WS-1 on the RCP 1/A3.04 (6/A7.23 WOOD SLAT DETAIL 2: slats on their own grid, 5/A7.23 'HANGER WIRE BY OTHERS'); the ceiling under the roof is the RS-1 assembly, unrated (A0.08 RS-1 rating blank, 'CEILING RE: RCP'; A0.00 'ROOF CONSTRUCTION 0 HR'), so nothing requires gypsum above the slats (at L2 / L3 the FS-1 1 HR membrane does continue above them). Delta if gypsum were required above the three zones: +146.70 SF 5/8\" Type X + 110.03 LF resilient channel (34.52 + 72.29 + 39.89 SF measured on 1/A3.04)."),
 ("Stair FCU soffit L4 (11/A6.01) framing", "LOADED metal - 11/A6.01 prints 'GYP BD SOFFIT AT FCU. CONTINUES FULL WIDTH OF STAIR.' and does not draw the framing; standing rule R-ALC-01 / BE-CF11 (framing not chosen by the detail -> the metal option): SOF-L4-01 track 17.44 LF + 2-1/2\" cripples 16.00 LF at 16\" o.c. (A0.06 GN 6). Delta if wood (Div. 06): -17.44 LF track, -16.00 LF cripples."),
 ("Corridor cove framing L2-L4 (7/A7.23)", "EXCLUDED - 7/A7.23 'WALL DETAIL - CORRIDOR CEILING' draws the cove framing members with the wood symbol (box with X, the same as the wall top plates of the detail); the GYP-1 legend 'GYPSUM BOARD ON METAL SUSPENSION SYSTEM, OR WOOD FRAMING' allows either and the specific detail governs (R-ALC-10) -> wood framing, Div. 06 (U-139); the gypsum board of the coves (SOF-L2-01 / L2-02 / L3-316 / L3-318 / L4-02) stays loaded. Delta if the framing is metal: +2,006.94 LF ceiling / soffit track + 411.92 LF 2-1/2\" cripple studs. Lobby coffers (5/A7.31) and the stair FCU soffit (11/A6.01) draw no wood: metal track + cripples loaded."),
 ("Structural steel: kickers, clip angles, L3x3 angles", "EXCLUDED - L3x3x1/4 KICKER at 4'-0\" o.c. (S1.02, 5/S3.08) and CLIP ANGLE with threaded rods into masonry (S3.04, S3.08) are drawn and sized on the STRUCTURAL sheets (S1.02 'L3x3x1/4 KICKER AT 4'-0\" O.C.', 5/S3.08 'L3x3 KICKER, SEE PLAN FOR SPACING' with '(3) 3/4\" A325 BOLTS', S3.02 'L3x3x3/8 BRACE AT 4'-0\" O.C.', S3.04 / S3.06 / S3.08 / S4.02 'CLIP ANGLE ... A36 THREADED RODS') = structural steel members (Div. 05 structural steel), not cold-formed / drywall framing: other trade (standing rule: structural members on S-sheets are not our scope)."),
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
 # E3 rev6: sección / párrafo de spec de cada material (Project Manual Vol 1, specs/*.txt leídos)
 "spec_por_material": [
     [r"shaftliner", "09 21 16.23 2.3.A Gypsum Liner Panels, Type X"],
     [r"exterior gypsum sheathing", "06 16 00 2.5.B Glass-Mat Gypsum Wall Sheathing, ASTM C 1177/1177M, 5/8 inch, Type X where indicated (Project Manual Vol 1 p. 214)"],
     [r"hanger wire", "09 22 16 2.2.C Wire Hangers: ASTM A 641/A 641M, Class 1 zinc coating, soft temper, 0.162-inch diameter (8 ga)"],
     [r"Type X W\.R\.|water resist", "09 29 00 2.3 Interior Gypsum Board (water-resistant core per the partition type, ASTM C 1396)"],
     [r"Type C", "09 29 00 2.3 Interior Gypsum Board (Type C not named in the spec; A0.08 FS-1 / UL L546 name it)"],
     [r"Type X", "09 29 00 2.3.A Gypsum Board, Type X"],
     [r"cement board", "09 29 00 2.4.A Cementitious Backer Units"],
     [r"main tee|cross tee|angle molding", "09 22 16 2.2 Grid Suspension System for Ceilings (ASTM C 645)"],
     [r"carrying channel", "09 22 16 2.2 Carrying Channels"],
     [r"hanger wire", "09 22 16 2.2 Wire Hangers"],
     [r"resilient channel", "09 22 16 2.3 Resilient Furring Channels"],
     [r"track|runner", "09 22 16 2.3 Steel Studs and Runners (ASTM C 645)"],
     [r"^2-1/2\" stud", "09 22 16 2.3 Steel Studs and Runners (ASTM C 645) - soffit cripple studs"],
     [r"control joint|corner bead|casing bead|trim", "09 29 00 2.5 Trim Accessories (ASTM C 1047)"],
     [r"compound|tape", "09 29 00 2.6 Joint Treatment Materials"],
     [r"C-H stud|J-runner|shaft", "09 21 16.23 2.4 Non-Load-Bearing Steel Framing"],
 ],
 "rfis": rfis, "rfi_cierre": cierre, "revisar": plantilla_excel.ordenar_revisar(revisar), "alcances": alcances,
 "proyecto_datos": pd, "hojas_revisadas": hojas, "barrido_no_dibujado": barrido,
}
# rev15 (revisión completa rev14 F08): piezas mínimas de C-H studs - un stud de largo > 10 ft (stock 20 ft / 2) sale de su propio stick
import math as _mt
_pm = {}
for _m in c['misc_items']:
    if not re.search(r"C-H stud", _m.get('familia', '')):
        continue
    _g = re.search(r"= (\d+) (?:cripple )?studs x (?:span )?([\d.]+) ft", str(_m.get('op')))
    if _g:
        _n, _h = int(_g.group(1)), float(_g.group(2))
        _st = _n if _h > 10.0 else _mt.ceil(_n / max(1, int(20.0 // _h)))
        _t = f"{_m['ref']} {_n} studs x {_h} ft -> {_st} sticks"
    else:
        _st = float(_m['qty']) / 20.0; _t = f"{_m['ref']} {_m['qty']} LF / 20 = {round(_st, 2)} sticks"
    _e = _pm.setdefault(_m['familia'], {"s": 0.0, "t": []}); _e["s"] += _st; _e["t"].append(_t)
td["piezas_min"] = {f: {"n": _mt.ceil(round(e["s"] * 1.15, 6)),
                        "op": f"one 20 ft stick per stud longer than 10 ft (the drop is not reusable): {round(e['s'], 2)} sticks x 1.15 waste = "
                              f"{_mt.ceil(round(e['s'] * 1.15, 6))} ({'; '.join(e['t'][:40])})"} for f, e in _pm.items()}
json.dump(td, open(f'{K}/takeoff.json', 'w'), indent=1, ensure_ascii=False)
print("rfis", len(rfis), "alcances", len(alcances))
