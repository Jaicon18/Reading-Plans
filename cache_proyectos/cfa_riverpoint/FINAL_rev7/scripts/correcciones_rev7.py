"""rev7 (coordination 4-nov, delivery gate v81cf33+: every detail / elevation bubble followed to the end of its chain).
Input changes after correcciones_rev6.py; every quantity recomputed by canon.py / accesorios.py / plantilla_excel.py.
Source of every change = the bubble readings in cfa_burbujas/out/ALL.json (101 views read by 3 reader subagents, one circled
crop per view in cfa_burbujas/out/img/) re-checked by the main session against the crops (CAMBIOS_rev7.md).
  1. PRINTED (applied): EX-KIT-02 removed (A3/A-601 'OPEN TO BEYOND' + A-202 10'-0 1/2" CRITICAL CLEAR DIMENSION: no wall);
     restroom cement / gyp transition 2 1/4" (+/-) below T/TILE 6'-8 1/2" (A2/A-604) -> cement 6.521 ft, gyp above +0.1875 ft;
     MB-01 face A gyp from 7'-0" A.F.F. (B.O. gypsum) to 6" min above the serving ACT 10'-0" (D3/A-624 + A-221) = 3.5 ft.
  2. PLAN vs PLAN conflicts -> conservative value loaded + RFI with the delta of each alternative (RFI-22..RFI-26); not printed
     at all -> RFI-27 (nothing loaded, delta per LF).
  3. Citations: every 'governs' view is cited (N/SHEET) in the source of the entries it governs; every 'no_aplica' view is
     written with its motive in callouts_no_aplican.json (CE_CALLOUTS).
Use: python3 bitacora.py run scripts/correcciones_rev7.py"""
import json, math, os, re
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.dirname(K)
P = os.path.join(K, "etapas", "4_canon", "takeoff_canon.json")
c = json.load(open(P))
V = json.load(open(os.path.join(K, "etapas", "8_burbujas", "ALL.json")))
LOG = []
log = lambda *a: LOG.append(dict(zip(("item", "rev6", "rev7", "delta", "src", "rule"), a)))
E = {e["id"]: e for e in c["existing_walls"]}
W = {w["id"]: w for w in c["walls"]}
f3 = lambda x: round(float(x), 3)

# ------------------------------------------------------------------------------------------------ 1. printed values
if "EX-KIT-02" in E:
    e = E.pop("EX-KIT-02")
    c["existing_walls"] = [x for x in c["existing_walls"] if x["id"] != "EX-KIT-02"]
    log("EX-KIT-02 kitchen west cement board base", f"{e['length_ft']} LF x {e['height_ft']} ft = {f3(float(e['length_ft']) * float(e['height_ft']))} SF",
        "removed: no wall there", f"-{f3(float(e['length_ft']) * float(e['height_ft']))} SF 1/2\" cement board",
        "A3/A-601 'OPEN TO BEYOND' + A-202 '10'-0 1/2\" CRITICAL CLEAR DIMENSION' (dashed, opening to the drive-thru)", "#0 printed")

for n in c.get("nodes") or []:          # the ends that died into EX-KIT-02 are the jambs of the open drive-thru opening
    if n.get("into") == "EX-KIT-02":
        n.pop("into")
        n["kind"] = "free"
        n["source"] = ("A-202: end at the 10'-0 1/2\" CRITICAL CLEAR DIMENSION opening to the drive-thru (A3/A-601 'OPEN TO BEYOND'); "
                       "no wall beyond (0 studs, same count as rev6)")
        log(f"node {n['id']} ({n['wall']})", "abut into EX-KIT-02", "free end at the opening", "0 studs", "A-202 + A3/A-601", "BE-89 topology")
TR = 6 + 6.25 / 12                     # 6'-8 1/2" T/TILE - 2 1/4" = 6'-6 1/4"
for e in c["existing_walls"]:
    base = e.get("split_of") or e["id"]
    if base in ("EX-RRM-01-CB", "EX-RRW-01-CB") and abs(float(e["height_ft"]) - 6.708) < 0.01:
        h0 = e["height_ft"]
        e["height_ft"] = f3(TR)
        e["height_source"] = ("[DERIVED] A2/A-604 TILE TO GYP TRANSITION AT RESTROOM: CEMENT / GYP. TRANSITION 2 1/4\" (+/-) below "
                              "T/TILE AT RR 6'-8 1/2\" (A-611) = 6'-8 1/2\" - 2 1/4\" = 6'-6 1/4\" = 6.521 ft; cement board below (C4/A-604)")
        log(f"{e['id']} cement board height", f"{h0} ft (to T/TILE)", "6.521 ft", f"{f3((TR - float(h0)) * float(e['length_ft']))} SF cement board",
            "A2/A-604 + A-611", "#0 printed")
    if base in ("EX-RRM-01-GB", "EX-RRW-01-GB") and abs(float(e["height_ft"]) - 2.625) < 0.01:
        h0 = e["height_ft"]
        e["height_ft"] = f3(9 + 4 / 12 - TR)
        e["height_source"] = ("[DERIVED] restroom C.H. 9'-4\" (A-611 / A-221) - cement / gyp transition 6'-6 1/4\" (A2/A-604: "
                              "T/TILE 6'-8 1/2\" - 2 1/4\") = 2.8125 ft of 1/2\" moisture-resistant gyp")
        log(f"{e['id']} gyp height above the transition", f"{h0} ft", f"{e['height_ft']} ft", f"+{f3((float(e['height_ft']) - float(h0)) * float(e['length_ft']))} SF 1/2\" MR",
            "A2/A-604 + A-611", "#0 printed")
# DEMO-14 = existing board under the new restroom cement board: follows the cement board height
mi = next((m for m in c["misc_items"] if m["ref"] == "DEMO-14"), None)
if mi:
    parts = [e for e in c["existing_walls"] if (e.get("split_of") or e["id"]) in ("EX-RRM-01-CB", "EX-RRM-02-CB", "EX-RRW-01-CB", "EX-RRW-02-CB")]
    q = round(sum(float(e["length_ft"]) * float(e["height_ft"]) for e in parts), 2)
    if abs(q - float(mi["qty"])) > 0.005:
        log("DEMO-14 existing board under the new restroom cement board", f"{mi['qty']} SF", f"{q} SF", f"{round(q - float(mi['qty']), 2)} SF demolition",
            "A2/A-604 + A-050 KN10", "follows the cement board height")
        mi["qty"] = q
        mi["op"] = " + ".join(f"{e['id']} {e['length_ft']} x {e['height_ft']}" for e in parts) + f" = {q} SF x 1 layer"

mb = W["MB-01"]
for f in mb["faces"]:
    if f.get("side") == "A" and abs(float(f["height_ft"]) - 3.5) > 0.01:
        h0 = f["height_ft"]
        f["height_ft"] = 3.5
        f["height_source"] = ("D3/A-624 MENU BOARD LIGHT BOX DETAIL: 1/2\" GYPSUM BOARD from '7'-0\" A.F.F. BOTT. OF GYPSUM BD.' to '6\" MIN.' "
                              "above the ACT; serving C.H. 10'-0\" (A-221) -> 10'-0\" + 6\" - 7'-0\" = 3.5 ft; C09250 2.1.B / A-909")
        f["height_status"] = "[DERIVED] serving C.H. 10'-0\" (A-221) + 6\" (D3/A-624) - B.O. gypsum 7'-0\" (D3/A-624) = 3.5 ft"
        log("MB-01 face A (serving) 1/2\" gyp height", f"{h0} ft (to the deck)", "3.5 ft", f"{f3((3.5 - float(h0)) * float(mb['length_ft']))} SF 1/2\" gyp",
            "D3/A-624 + A-221", "#0 printed (same as EX-MENU-01 / -02)")

# ------------------------------------------------------------------------------------------------ 2. conflicts -> RFIs
R = {r["id"]: r for r in c["rfis"]}
SW = "rev7 sweep (BE-120): set_texto.json (172 pages, text layer + AutoCAD SHX) grepped for the terms; every sheet with a term next to a printed value reviewed and written in descartes."


def rfi(rid, q, A, B, terms, desc, src, img, why):
    if rid in R:
        return
    r = {"id": rid, "status": "open - conservative value loaded", "question": q, "fuentes_revisadas": sorted(desc),
         "opciones": {"A": A, "B": B, "C": ""}, "source": src, "img": img,
         "barrido": {"hojas": "ALL", "terminos": terms, "grep": SW, "descartes": desc}, "why_not_printed": why,
         "delta": f"A: {A['delta']} | B: {B['delta']}"}
    c["rfis"].append(r)
    R[rid] = r


# RFI-22: menu wall serving face below the gyp (tile CT-72)
MENU = [("MB-01-SRV-CB", [[1546.0, 617.0], [1546.0, 677.0]], float(mb["length_ft"]), "Serving - menu board infill MB-01, serving face below the gyp"),
        ("EX-MENU-01-CB", E["EX-MENU-01"]["path"], float(E["EX-MENU-01"]["length_ft"]), "Serving - menu board wall (existing, north of MB-01), below the gyp"),
        ("EX-MENU-02-CB", E["EX-MENU-02"]["path"], float(E["EX-MENU-02"]["length_ft"]), "Serving - menu board wall (existing, south of MB-01), below the gyp")]
lf_m = round(sum(x[2] for x in MENU), 3)
for i, pa, lf, loc in MENU:
    if i in E:
        continue
    lp = sum(math.dist(a, b) for a, b in zip(pa, pa[1:])) / 18.0
    x = {"id": i, "sheet": "A-202", "page": "13", "keynote": "CT-72/A-211", "path": pa, "length_ft": f3(lp), "height_ft": 7.0, "faces": 1, "layers": 1,
         "board": "1/2 cement board", "location": loc,
         "length_op": f"[DERIVED] same path as {('MB-01' if i.startswith('MB') else i[:-3])}: {lp * 18:.1f} pt / 18 pt/ft = {lp:.3f} ft",
         "height_source": "[DERIVED] floor to '7'-0\" A.F.F. BOTT. OF GYPSUM BD.' (D3/A-624) = 7.0 ft; CT-72 wall tile below the bulkhead (C2/A-622, A1/A-621)",
         "source": "CT-72/A-211 wall tile on the serving face (C2/A-622, A1/A-621) + G.2/A-202 (1/2\" cement backer behind wall tile) vs D3/A-624 "
                   "(1/2\" plywood shown behind the WALL TILE) -> conservative cement board + RFI-22; C09250 2.2.B / A-909",
         "decision": "Scope rule R-ALC-01 (user 2026-11-01): gypsum / cement board is our scope on any substrate; conservative value loaded + RFI-22"}
    c["existing_walls"].append(x)
    E[i] = x
rfi("RFI-22", "Menu board wall, serving face below the gypsum (MB-01 + EX-MENU-01 / -02, 13.683 LF): C2/A-622 and A1/A-621 print CT-72 wall tile up "
    "to the bulkhead and G.2/A-202 calls 1/2\" cementitious backer behind wall tile, but D3/A-624 draws 1/2\" plywood behind the WALL TILE. Which substrate?",
    {"texto": f"Plans: 1/2\" cement board 0 to 7'-0\" on {lf_m} LF = {round(lf_m * 7, 2)} SF loaded (conservative)", "source": "C2/A-622 + G.2/A-202",
     "delta": f"0 (loaded); plywood per D3/A-624 (wood, Div. 06): -{round(lf_m * 7, 2)} SF 1/2\" cement board"},
    {"texto": "Wall tile set on cementitious backer units", "cita": "ANSI A108.11 / TCNA", "delta": "same as A"},
    ["CT-72", "BOTT. OF GYPSUM", "MENU BOARD LIGHT BOX"], {
        "A-211": "finish legend: CT-72 is the wall tile product only (no substrate, no height).",
        "A-621": "A1 dining elevation: CT-72 tile drawn to BULKHEAD 7'-2\" through the serving opening (finish height, no substrate).",
        "A-622": "C2 serving elevation: CT-72 tile field below the PT-31A painted gyp (finish, no substrate).",
        "A-624": "D3/A-624: '7'-0\" A.F.F. BOTT. OF GYPSUM BD.' and 1/2\" plywood + WALL TILE below it - the conflict itself."},
    "C2/A-622, A1/A-621, D3/A-624, G.2/A-202", "img_rev7/D3_A-624.png",
    "The substrate behind the CT-72 wall tile of the menu board wall is printed twice and differently (G.2/A-202 cement backer vs D3/A-624 plywood).")

# RFI-23: BOH non-kitchen base 1'-3" (C3/A-604) vs 1'-0" (G.3/A-202)
base_ids = [e["id"] for e in c["existing_walls"] if e["id"] in {
    "EX-MP-01-1", "EX-MP-01-2", "EX-MP-01-3", "EX-MP-01-4", "EX-MP-01-5", "EX-MP-01-6", "EX-MP-02-1", "EX-MP-02-2", "SW6-02-OFF", "SW6-02-SVC",
    "W6-06W-MP", "W6-08E-SVC", "W6-09-OFF-1", "W6-09-OFF-2", "W6-09-OUT-2", "W6-10N-SVC", "W8-01S-OFF"}]
lf_b = 0.0
for i in base_ids:
    e = E[i]
    if abs(float(e["height_ft"]) - 1.0) < 0.01:
        e["height_ft"] = 1.25
        e["height_source"] = ("C3/A-604 WALL BASE DETAIL @ BACK OF HOUSE (called by the A-602 / A-603 elevations of this room: 'CEMENTITIOUS BOARD RE: C3/A-604') "
                              "prints 1' - 3\" = 1.25 ft vs G.3/A-202 1'-0\" -> conservative 1.25 ft + RFI-23")
        lf_b += float(e["length_ft"])
if lf_b:
    log(f"BOH non-kitchen cement board base ({len(base_ids)} entries, {round(lf_b, 3)} LF)", "1.0 ft (G.3/A-202)", "1.25 ft (C3/A-604, conservative)",
        f"+{round(lf_b * 0.25, 2)} SF 1/2\" cement board", "C3/A-604 vs G.3/A-202", "RFI-23 (plan vs plan, conservative)")
lf_b = round(sum(float(E[i]["length_ft"]) for i in base_ids), 3)
rfi("RFI-23", f"Back-of-house non-kitchen rooms (multi-purpose, service, office: {len(base_ids)} wall faces, {lf_b} LF): the elevations call "
    "'CEMENTITIOUS BOARD RE: C3/A-604' and C3/A-604 prints the base 1' - 3\", while G.3/A-202 prints cement board to 1'-0\" above the slab. "
    "D1/A-602 points to 'B3/A-623', a view that does not exist on A-623. Which base height?",
    {"texto": f"Plans: 1.25 ft per C3/A-604 on {lf_b} LF loaded (conservative)", "source": "C3/A-604",
     "delta": f"0 (loaded); 1'-0\" per G.3/A-202: -{round(lf_b * 0.25, 2)} SF 1/2\" cement board"},
    {"texto": "Cement board base to the height of the wet-zone finish", "cita": "ASTM C1325 / TCNA", "delta": "same as A"},
    ["WALL BASE DETAIL", "B3/A-623", "BACK OF HOUSE"], {
        "A-604": "C3/A-604 WALL BASE DETAIL @ BACK OF HOUSE prints 1' - 3\" - the conflict itself (vs G.3/A-202 1'-0\").",
        "A-202": "wall notes G.3 / G.4 ('... TO 1'-0\" ... RE: TYPICAL WALL BASE DETAIL'): the 1'-0\" side of the conflict; they refer back to the base detail C3/A-604.",
        "A-624": "A2/A-624 WALL BASE AT PLAY AREA: play-area base (dining side 5\" cement board), not the back-of-house rooms.",
        "A-602": "D1/A-602 'RE: B3/A-623' points to a view that A-623 does not have (A-623 views A1-A3, B1-B3, C1-C3 without B3 detail of this wall)."},
    "C3/A-604 vs G.3/A-202; D1/A-602", "img_rev7/C3_A-604.png",
    "Two printed base heights for the same rooms (1'-3\" C3/A-604, 1'-0\" G.3/A-202); the D1/A-602 reference points to a view that does not exist.")

# RFI-24: dining wainscot plywood (A-625) vs A.6 gyp to ceiling
DIN = [i for i in ("W6-01N-GB1", "W6-01N-GB2", "W8-02W-DIN-GB") if i in E]
d24 = round(sum(float(E[i]["length_ft"]) * (6 + 4 / 12 - 5 / 12) for i in DIN), 2)
rfi("RFI-24", "Dining wainscot walls (W6-01N-GB1 / -GB2, W8-02W-DIN-GB; also the narrow dining pier of B4/A-622): C1 / C2 / D1-A / D1-B on A-625 "
    "print 1/2\" PLYWOOD SHEATHING ABOVE CEMENT BOARD BY G.C. to T/PLYWOOD 6'-4\" with gypsum board above, while note A.6 (A-601..A-623) reads "
    "5\" cementitious board then gypsum board to the ceiling. Is the gypsum board from 5\" to 6'-4\" replaced by plywood?",
    {"texto": "Plans: gypsum board from the 5\" cement board base to the ceiling loaded (A.6, conservative)", "source": "A.6/A-621",
     "delta": f"0 (loaded); plywood per A-625 (wood, Div. 06): -{d24} SF 1/2\" gypsum board (5\" to 6'-4\" on {round(sum(float(E[i]['length_ft']) for i in DIN), 3)} LF)"},
    {"texto": "Wainscot substrate per the wainscot manufacturer", "cita": "per mfr / ASTM C840", "delta": "same as A or plywood"},
    ["T/PLYWOOD", "PLYWOOD SHEATHING ABOVE", "WAINSCOTING BASE DETAIL"], {
        "A-625": "C1 / C2 / D1-A / D1-B wainscot details: plywood by G.C. to T/PLYWOOD 6'-4\" - the conflict itself.",
        "A-501": "exterior wall details: plywood sheathing of the wood SW6 exterior wall (Div. 06), not the dining wainscot.",
        "A-624": "A1 / A2 play-area sections: plywood shown at the play-area enclosure / hatch, not the dining wainscot walls.",
        "S-301": "structural shear wall plywood sheathing (Div. 06).", "S-600": "typical wood framing: plywood sheathing (Div. 06)."},
    "C1/A-625, C2/A-625, D1-A/A-625, A.6/A-621", "img_rev7/C1_A-625.png",
    "The dining wainscot substrate is printed twice and differently (A-625 plywood to 6'-4\" vs A.6 gypsum board to the ceiling).")

# RFI-25: R-W6-11-N full-height wall tile CT-58A (A4/A-621)
if "R-W6-11-N-GYP" in E and E["R-W6-11-N-GYP"]["board"] != "1/2 cement board":
    e = E["R-W6-11-N-GYP"]
    e["board"] = "1/2 cement board"
    e["source"] = ("A4/A-621 dining elevation: CT-58A wall tile to CEILING 10'-4\" on this W6 face (W6/A-202 4'-2 1/2\") + G.2/A-202 1/2\" cement backer "
                   "behind wall tile -> cement board above the 5\" base (conservative, RFI-25); C09250 2.2.B / A-909")
    log("R-W6-11-N-GYP (dining face of W6 at the drive-thru)", f"1/2\" regular {e['length_ft']} x {e['height_ft']}", "1/2\" cement board (same SF)",
        f"-{f3(float(e['length_ft']) * float(e['height_ft']))} SF 1/2\" regular, +same SF 1/2\" cement board", "A4/A-621 + G.2/A-202", "RFI-25 (conservative)")
rfi("RFI-25", "Dining face of the W6 wall at the drive-thru (R-W6-11-N, 4'-2 1/2\"): A4/A-621 draws CT-58A wall tile to the CEILING 10'-4\" (identified from the "
    "A-621 marker looking south + the 4'-2 1/2\" W6 segment); note A.6 reads 5\" cement board then gypsum board. Full-height tile -> cement board?",
    {"texto": f"Plans: 1/2\" cement board full height (G.2/A-202 behind wall tile) loaded (conservative)", "source": "A4/A-621 + G.2/A-202",
     "delta": f"0 (loaded); gypsum per A.6: same {f3(float(E['R-W6-11-N-GYP']['length_ft']) * float(E['R-W6-11-N-GYP']['height_ft']))} SF as 1/2\" regular"},
    {"texto": "Wall tile set on cementitious backer units", "cita": "ANSI A108.11 / TCNA", "delta": "same as A"},
    ["CT-58A", "DINNING ELEVATION", "DINING ELEVATION"], {
        "A-211": "finish legend: CT-58A wall tile product only.",
        "A-621": "A4/A-621: CT-58A to CEILING 10'-4\" - the condition loaded.",
        "A-622": "C2/A-622: CT-58A full height around the opening on the same tiled zone."},
    "A4/A-621, G.2/A-202, A.6/A-621", "img_rev7/A4_A-621.png",
    "Full-height tile is drawn on the elevation; the substrate under it is not called out on this wall (A.6 is the general wainscot note).")

# RFI-26: serving ceiling 10'-2" (D2 / D3/A-622) vs 10'-0" (A-221, D4/A-622)
d26 = 0.0
for i in ("W4-01W-SRV", "W6-02N-SRV"):
    e = E.get(i)
    if e and abs(float(e["height_ft"]) - 10.0) < 0.01:
        e["height_ft"] = f3(10 + 2 / 12)
        e["height_source"] = ("D2 / D3/A-622 SERVING ELEVATION print CEILING 10'-2\" (tile CT-45 to the ceiling) vs A-221 serving C.H. 10'-0\" "
                              "(and D4/A-622 10'-0\") -> conservative 10'-2\" = 10.167 ft + RFI-26")
        d26 += float(e["length_ft"]) * (2 / 12)
if d26:
    log("Serving cement board W4-01W-SRV / W6-02N-SRV height", "10.0 ft", "10.167 ft (D2 / D3/A-622, conservative)", f"+{round(d26, 2)} SF 1/2\" cement board",
        "D2/A-622, D3/A-622 vs A-221", "RFI-26")
rfi("RFI-26", "Serving room tile walls W4-01W-SRV / W6-02N-SRV: D2 and D3/A-622 print CEILING 10'-2\", while A-221 and D4/A-622 print the serving ceiling 10'-0\". Which ceiling height?",
    {"texto": "Plans: 10'-2\" per D2 / D3/A-622 loaded (conservative)", "source": "D2/A-622, D3/A-622",
     "delta": f"0 (loaded); 10'-0\" per A-221: -{round((float(E['W4-01W-SRV']['length_ft']) + float(E['W6-02N-SRV']['length_ft'])) * 2 / 12, 2)} SF 1/2\" cement board"},
    {"texto": "Board to the ceiling line per the RCP", "cita": "ASTM C840 / GA-216", "delta": "same as the plans value"},
    ["SERVING ELEVATION", "CT-45", "SERVING CEILING"], {"A-622": "D2 / D3 / D4 SERVING ELEVATION: 10'-2\" (D2, D3) and 10'-0\" (D4) - the conflict itself."},
    "D2/A-622, D3/A-622, D4/A-622, A-221", "img_rev7/D3_A-622.png",
    None)
R["RFI-26"]["conflicto"] = "Two ceiling heights are printed for the same room (D2 / D3/A-622 10'-2\" vs A-221 and D4/A-622 10'-0\")."

# RFI-27: drive-thru furr down B.O. 7'-8" (C1/A-603), not loaded
rfi("RFI-27", "Drive-thru south wall (C1/A-603 DRIVE-THRU ELEVATION): '7'-8\" B.O. FURR DOWN' with FRP-2 above, A-221 shows no soffit there. Is there a "
    "furr down (its depth and extent), or is 7'-8\" only the tile / door-head datum?",
    {"texto": "Plans: nothing loaded (no depth, framing or board printed; A-221 shows no soffit)", "source": "C1/A-603 + A-221",
     "delta": "0 (as loaded); a framed furr down: per LF of wall, about 2 x 2.5 ft of 1/2\" board (face + bottom) + 2 runner tracks + studs @ 16\" - depth not printed"},
    {"texto": "Furr-down framing per ASTM C754 with a printed depth", "cita": "ASTM C754 / C840", "delta": "same as the furr-down alternative"},
    ["FURR DOWN", "FURRDOWN", "B.O. FURR"], {
        "A-052": "A-052 KN3 'remove existing menuboard furr down' - the existing serving furr down (RFI-12), not the drive-thru.",
        "A-603": "C1/A-603: '7'-8\" B.O. FURR DOWN' - the question itself (no depth / framing printed).",
        "A-622": "serving elevations: existing menu board furr down removed (KN3), not the drive-thru."},
    "C1/A-603, A-221", "img_rev7/C1_A-603.png", "Only the bottom elevation of the furr down is printed.")

# ------------------------------------------------------------------------------------------------ 2b. standing precedents (U-026)
# R80e.34 #15 (estimator decision B&N, general rule): cement board / backer up to the highest printed finish -> RFI-22 / -23 / -25 are
# decided by the precedent (loaded values above stay); R80e.34 #11: "BY G.C." -> EXCLUDED with a note -> RFI-24: the plywood by G.C.
# of the A-625 wainscot is not ours, our gypsum board on those dining walls starts at T/PLYWOOD 6'-4".
PREC = {"RFI-22": "standing estimator precedent #15 of 27-oct (cement board behind the highest printed finish): 1/2\" cement board behind the CT-72 tile, 0 to 7'-0\" (B.O. gypsum D3/A-624)",
        "RFI-23": "standing estimator precedent #15 of 27-oct (cement board to the highest printed finish height): 1'-3\" per C3/A-604, the highest printed base",
        "RFI-25": "standing estimator precedent #15 of 27-oct (cement board behind the highest printed finish): CT-58A to the ceiling -> cement board full height"}
for rid, t in PREC.items():
    r = R[rid]
    r["status"] = "closed - estimator decision (option A)"
    r["opciones"]["A"]["texto"] = t + " - " + r["opciones"]["A"]["texto"]
    r["opciones"]["A"]["source"] = r["opciones"]["A"]["source"] + "; standing estimator precedent #15"
r = R["RFI-24"]
if r["status"].startswith("open"):
    din = 0.0
    for i in DIN:
        e = E[i]
        h0 = float(e["height_ft"])
        h1 = f3(h0 - (6 + 4 / 12 - 5 / 12))
        e["height_ft"] = h1
        op = ("DINING C.H. 10'-4\" (A-221) + 6\" (sheathing to 6\" over the ceiling, A-221 note A.11) - T/PLYWOOD 6'-4\" (C1/A-625) = 4.5 ft" if abs(h1 - 4.5) < 0.01
              else "DINING C.H. 10'-4\" (A-221 / A-623) - T/PLYWOOD 6'-4\" (C1/A-625) = 4.0 ft")
        e["height_source"] = ("[DERIVED] " + op + "; 1/2\" PLYWOOD SHEATHING ABOVE CEMENT BOARD BY G.C. from the 5\" base to 6'-4\" (C1 / C2 / D1-A/A-625) "
                              "is not ours (standing estimator precedent #11: 'BY G.C.')")
        din += float(e["length_ft"]) * (h0 - h1)
        log(f"{i} dining gyp above the wainscot", f"{h0} ft", f"{h1} ft", f"-{f3(float(e['length_ft']) * (h0 - h1))} SF 1/2\" gyp",
            "C1/A-625, C2/A-625, D1-A/A-625", "R80e.34 #11 (BY G.C.)")
    r["status"] = "closed - estimator decision (option A)"
    r["opciones"]["A"] = {"texto": "standing estimator precedent #11 of 27-oct ('BY G.C.' = not ours): plywood by G.C. 5\" to 6'-4\" (A-625), our gypsum board only above T/PLYWOOD 6'-4\" (loaded)",
                          "source": "C1/A-625, C2/A-625, D1-A/A-625; standing estimator precedent #11", "delta": f"0 (loaded); gypsum to the ceiling per A.6: +{round(din, 2)} SF 1/2\" gyp"}
    r["delta"] = f"A: {r['opciones']['A']['delta']} | B: {r['opciones']['B']['delta']}"

# ------------------------------------------------------------------------------------------------ 3. citations + no_aplica
by_id = {}
for k in ("walls", "existing_walls", "ceilings", "misc_items", "trim_items"):
    for e in c[k]:
        by_id[e.get("id") or e.get("ref")] = e
na, n_cit = {}, 0
V = V + [{"view": "D1/A-604", "disposition": "no_aplica", "canon_ids": [], "motivo": ""}]
for v in V:
    view = v["view"]
    if v["disposition"] == "no_aplica" or not [i for i in v.get("canon_ids") or [] if i in by_id or i.split(" ")[0] in by_id]:
        mot = (v.get("motivo") or "").strip() or ("; ".join(v.get("printed") or [])[:300])
        if view == "B3/A-623":
            mot = "Printed reference on D1/A-602 ('RE: B3/A-623') to a view that A-623 does not have; the base height of that wall is RFI-23."
        if view == "D1/A-604":
            mot = ("CORNER GUARD detail: corner guard by the finish trade over the outside corner; interior sheathing and finish 'RE: ... WALL & "
                   "PARTITION TYPE NOTES' (no board type, height or trim of ours printed).")
        if view == "B4/A-622":
            mot = ("Narrow dining pier with WD-3 wainscot to 6'-5\" and CT-73B base: its board is covered by RFI-24 (dining wainscot substrate); "
                   "the pier is not drawn as a separate wall on A-202.")
        na[view] = mot if len(mot) >= 8 else f"{view}: shows nothing of our scope ({mot})"
        continue
    for i in v["canon_ids"]:
        e = by_id.get(i) or by_id.get(i.split(" ")[0])
        if e is None:
            continue
        key = "source"
        if view not in str(e.get(key) or ""):
            e[key] = (str(e.get(key) or "") + f" | elev {view}").strip(" |")
            n_cit += 1
json.dump(na, open(os.path.join(K, "callouts_no_aplican.json"), "w"), ensure_ascii=False, indent=1)
log("Detail / elevation bubbles followed (CE_CALLOUTS)", "78 without disposition", f"{len(V) - len(na)} views cited in their rows ({n_cit} citations), "
    f"{len(na)} declared not applicable with motive (callouts_no_aplican.json)", "0", "101 views, cfa_burbujas/out/img", "U-113 / U-137")

json.dump(c, open(P, "w"), ensure_ascii=False, indent=1)
json.dump(LOG, open(os.path.join(K, "etapas", "4_canon", "rev7_log.json"), "w"), ensure_ascii=False, indent=1)
print(f"rev7 corrections: {len(LOG)} log lines")
