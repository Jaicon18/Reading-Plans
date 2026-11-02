"""rev2 correction pass on the reconciled canon (CFA #2284), orchestrator decisions 1-20 (audit step 11 + coverage step 12).
INPUT changes only: every quantity of the Excel is still computed by canon.py / accesorios.py / plantilla_excel.py.
The few counts written here (braces @ 48", cross braces @ 32", perimeters, sums of existing entries) are computed by
THIS program from canon geometry with the operation written in `op`. Idempotent (marker constants.rev2_applied).
Every change is appended to proceso/CAMBIOS_rev2.md by scripts/cambios_rev2.py from rev2_log.json.
Use: python3 bitacora.py run scripts/correcciones_rev2.py"""
import json, math, os, re
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C4 = os.path.join(K, "etapas", "4_canon")
P = os.path.join(C4, "takeoff_canon.json")
# base = the rev1 reconciled canon (frozen, ../cfa_calc); this program re-applies every rev2 change on it (repeatable)
BASE = os.path.join(os.path.dirname(K), "cfa_calc", "etapas", "4_canon", "takeoff_canon.json")
c = json.load(open(BASE))
LOG = []


def log(item, rev1, rev2, delta, src, rule):
    LOG.append({"item": item, "rev1": rev1, "rev2": rev2, "delta": delta, "src": src, "rule": rule})


W = {w["id"]: w for w in c["walls"]}
E = {e["id"]: e for e in c["existing_walls"]}
M = {m["ref"]: m for m in c["misc_items"]}
R2 = math.sqrt(2)
CU = lambda x, d=3: round(x, d)

# ---------------------------------------------------------------- 1. bracing: no C.R. channel on these walls
for wid in ("M2.1-01", "M3.5-01", "M3.5-02", "MB-01"):
    w = W[wid]
    w["bracing_rows"] = 0
    w["bracing_rows_source"] = "A1/A-605, A2/A-605, C2/S-801"
    w["bracing_rows_info"] = ("no C.R. channel bridging drawn on this wall; C09111 3.2.C (A-909) is ceiling sway bracing; wall braces "
                              "per D1/S-801 METAL STUD BRACE SCHEDULE loaded as their own items")
log("C.R. channel 'bracing' on M2.1-01 / M3.5-01 / M3.5-02 / MB-01", "56.79 LF (28.33 + 14.29 + 7.5 + 6.67)", "0 LF",
    "-56.79 LF C.R. channel", "A1/A-605, A2/A-605, C2/S-801; C09111 3.2.C / A-909", "decision 1 (bracing only where printed)")
# D1/S-801 braces @ 48" O.C. (alt sides), H = B.O. truss - top of wall; schedule H <= 6'-0" -> one 362S162-33
BOT = 12.333     # kitchen-bay B.O. truss 12'-4" (S-201, DERIVED in the resolution; RFI-10 zone note)
brc = []
for wid in ("M3.5-01", "M3.5-02", "MB-01"):
    w = W[wid]
    L, top = float(w["length_ft"]), float(w["height_ft"])
    H = round(BOT - top, 3)
    n = math.ceil(L / 4.0) + 1
    size = 1 if H <= 6.0 else 2
    ln = round(H * R2, 3)
    q = round(n * size * ln, 2)
    ref = "BRC-" + wid
    c["misc_items"].append({"ref": ref, "familia": "3-5/8\" stud (todos los gauges)", "qty": q, "unit": "LF", "pcs": n * size,
        "source": f"D1/S-801 TYP. MTL PARTITION WALL BRACING BELOW TRUSS + METAL STUD BRACE SCHEDULE (H <= 6'-0\" -> '362S162-33') at {wid}"
                  + (" + C2/S-801 '362S162-33' brace @ 48\" O.C." if wid == "MB-01" else " + A-202 wall note C.4") +
                  "; C09111 2.3 / A-909; H = B.O. truss 12'-4\" (S-201, DERIVED) - top of wall (A-202 note C.1)",
        "op": f"ROUNDUP({L} / 4.0) + 1 = {n} braces @ 48\" x {size} stud(s) x (H {BOT} - {top} = {H} ft x 1.414 at 1:1 = {ln} ft) = {q} LF",
        "product": {"value": "362S162-33 metal stud brace @ 48\" O.C. (D1/S-801)", "source": "D1/S-801 METAL STUD BRACE SCHEDULE"}})
    brc.append((ref, n * size, q))
npl = sum(n for _, n, _ in brc)
c["misc_items"].append({"ref": "BRC-PLATES", "familia": "clip angle (bracing / nested connections)", "qty": npl, "unit": "PCS",
    "source": "D1/S-801 '54 MIL BENT PLATE @ 48\" O.C. W/ (3) #10 S.M.S. EA. LEG TO BRACE & CONT. TRACK'; C09111 2.3 / A-909",
    "op": " + ".join(f"{r} {n}" for r, n, _ in brc) + f" = {npl} plates (one per brace)",
    "product": {"value": "54 mil bent plate at brace (D1/S-801)", "source": "D1/S-801"}})
c["misc_items"].append({"ref": "ANG-MB-01", "familia": "track de ceilings / soffits", "qty": W["MB-01"]["length_ft"], "unit": "LF",
    "source": "C2/S-801 'L1 1/2\"x1 1/2\"x33 MIL CONT. ANGLE W/ #10 S.M.S. EA. JOIST & EA. STUD' at the menu board wall MB-01; C09111 2.3 / A-909",
    "op": f"continuous along MB-01 = {W['MB-01']['length_ft']} LF",
    "product": {"value": "L1-1/2\" x 1-1/2\" x 33 mil continuous angle (C2/S-801)", "source": "C2/S-801"}})
log("Wall braces 362S162-33 @ 48\" (D1/S-801 schedule) at M3.5-01 / M3.5-02 / MB-01", "0", f"{sum(q for *_, q in brc):.2f} LF 3-5/8\" ({sum(n for _, n, _ in brc)} pcs)",
    f"+{sum(q for *_, q in brc):.2f} LF", "D1/S-801, C2/S-801, A-202 note C.4", "decision 1 (printed schedule)")
log("54 mil bent plates at braces", "0", f"{npl} pcs", f"+{npl} pcs", "D1/S-801", "decision 1")
log("L1-1/2x1-1/2x33 mil continuous angle at MB-01", "0", f"{W['MB-01']['length_ft']} LF", f"+{W['MB-01']['length_ft']} LF", "C2/S-801", "decision 1")
b = [x for x in c["blocking_items"] if x["ref"] == "BLK-MENU"][0]
b0 = b["lf"]
b["lf"] = round(W["MB-01"]["length_ft"] * 2, 3)
b["width_source"] = f"C2/S-801 '33 MIL BLKG. T&B AS REQ'D' across MB-01: {W['MB-01']['length_ft']} ft x 2 rows (top + bottom) = {b['lf']} LF"
log("Menu board 33 mil blocking T&B (C2/S-801)", f"{b0} LF (one row)", f"{b['lf']} LF (2 rows)", f"+{round(b['lf'] - b0, 3)} LF", "C2/S-801", "decision 1")

# ---------------------------------------------------------------- 2. soffit cross brace @ 32" (C4/A-624, C3/S-801)
SS = {w["id"]: w for w in c["walls"] if w.get("element") == "soffit_side"}
xb = []
# serving L: west strip (run = SS-SRV-W, width = IV - W), north strip (run = SS-SRV-IH, width = IH - N); gathering box
for ref, run_w, a, b_, ori in (("XBR-SRV-W", "SS-SRV-W", "SS-SRV-W", "SS-SRV-IV", "V"), ("XBR-SRV-N", "SS-SRV-IH", "SS-SRV-N", "SS-SRV-IH", "H"),
                               ("XBR-GT", "SS-GT-W", "SS-GT-W", "SS-GT-E", "V")):
    run = float(SS[run_w]["length_ft"])
    ca = (SS[a]["band"]["c0"] + SS[a]["band"]["c1"]) / 2
    cb = (SS[b_]["band"]["c0"] + SS[b_]["band"]["c1"]) / 2
    wd = round(abs(cb - ca) / 18.0, 3)
    n = math.ceil(run * 12 / 32.0) + 1
    ln = round(wd * R2, 3)
    q = round(n * ln, 2)
    c["misc_items"].append({"ref": ref, "familia": "3-5/8\" stud (todos los gauges)", "qty": q, "unit": "LF", "pcs": n,
        "source": "C4/A-624 '3-5/8\" METAL STUD CROSS BRACE AT 32\" O.C.' + C3/S-801 '362S162-33 @ 32\" O.C.'; C09111 2.3 / A-909; length at the 1:1 slope drawn across the soffit width (A-221 vector), hanger height RFI-15",
        "op": f"ROUNDUP({run} x 12 / 32) + 1 = {n} braces x (width {wd} ft x 1.414) {ln} ft = {q} LF",
        "product": {"value": "362S162-33 soffit cross brace @ 32\" O.C. (C4/A-624, C3/S-801)", "source": "C4/A-624 + C3/S-801"}})
    xb.append((ref, n, q))
log("Soffit cross brace 362S162-33 @ 32\" (serving L + gathering)", "0", f"{sum(q for *_, q in xb):.2f} LF ({sum(n for _, n, _ in xb)} pcs)",
    f"+{sum(q for *_, q in xb):.2f} LF 3-5/8\"", "C4/A-624, C3/S-801", "decision 2")

# ---------------------------------------------------------------- 3. play-bay rim track
pb = M["CLG-PLAY-J"]
per = round(2 * (2.928 + 11.958), 2)
c["misc_items"].append({"ref": "CLG-PLAY-R", "familia": "ceiling / soffit track 6\"", "qty": per, "unit": "LF",
    "source": "S-241 legend 'dropped ceiling and RIM JOISTS' + A3/S-241 rim joist (to match C.J.) at the play-bay gyp ceiling A-221 PT-41 (framing assumed, RFI-07); C09111 2.3 / A-909",
    "op": f"rim track = ceiling perimeter 2 x (2.928 + 11.958) = {per} LF"})
log("Play-bay gyp ceiling 6\" rim track", "0", f"{per} LF", f"+{per} LF 6\" track", "A3/S-241, A-221", "decision 3")

# ---------------------------------------------------------------- 4. MB-01 = 6" metal (D3/A-624 '2X6 WOOD OR 6" METAL')
mb = W["MB-01"]
mb["stud_size"] = "6\""
mb["stud_source"] = ("D3/A-624 MENU BOARD LIGHT BOX DETAIL '2X6 WOOD FRAMING OR 6\" METAL FRAMING AT 16\" O.C.' -> metal (metal-or-wood "
                     "standing order); C09111 2.3.B.1 (0.0312 in min) / A-909")
mb["oc_source"] = "D3/A-624 '@ 16\" O.C.'"
mb["detail"] = "D3/A-624"
mb["detail_source"] = "D3/A-624 menu board wall (6\" metal @ 16\") + C2/S-801 (braces, blocking T&B, continuous angle)"
mb["gauge"] = "33 mil (20 ga)"
mb["gauge_source"] = "C2/S-801 '362S162-33' (33 mil) - gauge of the 6\" member not printed on D3/A-624; S-902 C05000-C 2.5.A.1 note in RFI-18"
mb["tag"] = "INFILL"
c["details"]["D3/A-624"] = {"source": "D3/A-624", "title": "MENU BOARD LIGHT BOX DETAIL - NON LC STORE",
    "layers_per_face": 1, "layers_source": "D3/A-624 1/2\" gypsum board (serving) / 1/2\" cementitious board (kitchen)",
    "notes": "2X6 wood framing or 6\" metal framing at 16\" O.C.; 1/2\" gypsum board stops at B.O. 7'-0\" (exposed edge); 1/2\" plywood (Div. 06, excluded)",
    "sealant_none_reason": "none printed", "sealant_source": "D3/A-624", "img": "img_rev2/S801_D1_schedule.png"}
mb["untagged_reason"] = ("no partition tag: infill of the removed Eliason door (A-050 KN1) drawn with the new-wall outline on A-202; "
                         "framing printed on D3/A-624 (6\" metal @ 16\")")
mb["default_type_source"] = "D3/A-624 '2X6 WOOD FRAMING OR 6\" METAL FRAMING AT 16\" O.C.'"
log("MB-01 stud size (menu board infill)", "3-5/8\" (C2/S-801)", "6\" @ 16\" (D3/A-624)", "studs + tracks of MB-01 move from 3-5/8\" to 6\"", "D3/A-624",
    "decision 4 (metal-or-wood = metal)")

# ---------------------------------------------------------------- 5. C1/S-801 slotted long-leg track at the roof hatch shaft top
t = M["RH-SHAFT-T"]
t["qty"] = 12.0
t["op"] = "perimeter 12.0 LF x 1 (bottom runner at 24\" below finish ceiling, A1/A-604) = 12.0 LF"
c["misc_items"].append({"ref": "RH-SHAFT-TT", "familia": "deep-leg slotted deflection track (printed)", "qty": 12.0, "unit": "LF",
    "source": "C1/S-801 TYP. MTL PARTITION WALL BRACING AT TRUSS '3\" LONG LEGGED SLOTTED CONT. TRACK TO MATCH STUD DEPTH & THICKNESS' at the roof hatch shaft studs that reach the roof framing (A1/A-604); C09111 2.3 / A-909",
    "op": "3-5/8\" web: top runner at the roof framing = shaft perimeter 12.0 LF (RFI-14 shaft size)"})
log("Roof hatch shaft top runner", "24 LF standard track (top + bottom)", "12 LF standard (bottom) + 12 LF 3\" long-leg slotted (top, C1/S-801)",
    "-12 LF standard track, +12 LF slotted track", "C1/S-801, A1/A-604", "decision 5 (two track kinds in separate rows)")
c["deflection_clips"] = {"none_reason": "no deflection clip printed for our walls (A-202, A-605, A-624, S-801 swept); C1/S-801 prints a 3\" long-legged slotted continuous track instead, loaded where studs reach the roof framing (roof hatch shaft)",
                         "source": "C1/S-801 + A-202"}

# ---------------------------------------------------------------- 6. gauge: plans (33 mil) vs S-902 C05000-C 2.5.A.1 (0.0538 in)
c["rfis"].append({"id": "RFI-18", "status": "closed - estimator decision (option A)",
    "question": "Stud / joist / track gauge: S-801 and S-241 print 362S162-33 / 600S162-33 / 33 mil track (0.0346 in) while S-902 C05000-C 2.5.A.1 requires min. base-metal thickness 0.0538 in. NOTE: loaded the plans (33 mil); investigate S-902 C05000-C 2.5.A.1 vs S-801 / S-241.",
    "fuentes_revisadas": ["S-801", "S-241", "S-902", "A-909"],
    "opciones": {"A": {"texto": "Plans: 33 mil members as printed on S-801 / S-241 (loaded)", "source": "C2/S-801, D1/S-801, A2/S-241",
                       "delta": "0 (loaded); 54 mil alternative: same LF of every 33 mil stud / joist / track of the Material Summary in 0.0538 in (heavier gauge, price change only)"},
                 "B": {"texto": "Spec governs gauge where the plans are silent; here the plans print the member", "cita": "S-902 C05000-C 2.5.A.1 / AISI S220", "delta": "same LF, 54 mil"}, "C": ""},
    "source": "S-801, S-241, S-902"})
log("Gauge plans 33 mil vs S-902 C05000-C 2.5.A.1 0.0538 in", "no note", "RFI-18 closed (option A = plans 33 mil)", "0 LF (gauge alternative = same LF at 54 mil)",
    "S-902, S-801, S-241", "decision 6 (plan-vs-spec conflict)")

# ---------------------------------------------------------------- 7. ceiling board = sag-resistant (C09250 2.1.E)
for r in ("CLG-ENTA-B", "CLG-ENTB-B", "CLG-MEN-B", "CLG-WOM-B", "CLG-PLAY-B"):
    M[r]["product"] = {"value": "5/8\" sag-resistant gypsum ceiling board (C09250 2.1.E)", "source": "C09250 2.1.E + 3.2.A.3 / A-909"}
log("Ceiling board product (332.06 SF)", "5/8\" gypsum board, regular", "5/8\" sag-resistant gypsum ceiling board (C09250 2.1.E)", "0 SF (product)", "C09250 2.1.E / A-909", "decision 7")

# ---------------------------------------------------------------- 8. wet areas: water-resistant board, PLAN thickness (plan-vs-spec conflict)
wr = 0.0
for eid in ("EX-RRM-01-GB", "EX-RRW-01-GB"):
    e = E[eid]
    e["board"] = "1/2 MR"
    e["source"] += (" | C09250 2.2.A water-resistant gypsum backing board at toilets / sinks (A-909); thickness per plan 1/2\" "
                    "(A-202 notes G.1 / H.3); spec 2.2.A.2 calls 5/8\" Type X W.R. (RFI-21 closed, option A)")
    wr += float(e["length_ft"]) * float(e["height_ft"])
c["rfis"].append({"id": "RFI-21", "status": "closed - estimator decision (option A)",
    "question": "Restroom gypsum faces above the tile: A-202 notes G.1 / H.3 print 1/2\" gypsum board; C09250 2.2.A.2 (A-909) calls the water-resistant backing board with a 5/8\" Type X core. NOTE: loaded 1/2\" water-resistant (plan thickness, spec product); investigate A-202 G.1 / H.3 vs C09250 2.2.A.2.",
    "fuentes_revisadas": ["A-202", "A-611", "A-909"],
    "opciones": {"A": {"texto": f"Plans: 1/2\" moisture-resistant gypsum board {wr:.2f} SF (loaded)", "source": "A-202 notes G.1 / H.3 + A-611",
                       "delta": f"0 (loaded); spec alternative: same {wr:.2f} SF as 5/8\" Type X W.R. (C09250 2.2.A.2)"},
                 "B": {"texto": "Water-resistant backing board at wet areas", "cita": "C09250 2.2.A / ASTM C1396", "delta": f"same {wr:.2f} SF, 5/8\" Type X W.R."}, "C": ""},
    "source": "A-202, C09250 / A-909", "img": "img_runner/sheet_A-202.png"})
log("Restroom gyp faces above tile (EX-RRM-01-GB, EX-RRW-01-GB)", f"1/2\" regular {wr:.2f} SF", f"1/2\" moisture resistant {wr:.2f} SF (plan thickness, spec product) + RFI-21 closed",
    f"-{wr:.2f} SF 1/2\" regular, +{wr:.2f} SF 1/2\" MR; spec alternative same {wr:.2f} SF as 5/8\" Type X W.R.", "A-202 notes G.1 / H.3, C09250 2.2.A.2 / A-909, A-611",
    "decision 8 rev (plan-vs-spec conflict: plan thickness, spec product, RFI-21 closed)")

# ---------------------------------------------------------------- 10. printed trims (J-bead)
jm = round(E["EX-MENU-01"]["length_ft"] + W["MB-01"]["length_ft"] + E["EX-MENU-02"]["length_ft"], 3)
c["trim_items"].append({"ref": "J-MENU", "kind": "j_bead", "lf": jm,
    "source": f"D3/A-624 1/2\" gypsum board stops at B.O. 7'-0\" A.F.F. on the menu board wall (exposed edge) + C09250 2.3 LC-bead (J) / A-909: EX-MENU-01 + MB-01 + EX-MENU-02 = {jm} LF",
    "product": {"value": "LC-bead (J) at exposed gypsum edge (D3/A-624)", "source": "D3/A-624 + C09250 / A-909"}})
l5 = c["level5_items"][0]
c["trim_items"].append({"ref": "J-PLAY", "kind": "j_bead", "lf": l5["l_ft"],
    "source": f"A2/A-624 WALL BASE AT PLAY AREA '\"J\" TRIM' on top of the 1/2\" cement board base = play area solid wall perimeter {l5['l_ft']} LF (A-202 vector, same run as Level 5)",
    "product": {"value": "J trim at top of cement board base (A2/A-624)", "source": "A2/A-624"}})
log("J-bead at menu board exposed gyp edge", "0", f"{jm} LF", f"+{jm} LF", "D3/A-624", "decision 10")
log("J trim at play area wall base", "0", f"{l5['l_ft']} LF", f"+{l5['l_ft']} LF", "A2/A-624", "decision 10")

# ---------------------------------------------------------------- 12. beverage chases (A-052 general note 9)
c["misc_items"].append({"ref": "PATCH-BEV", "familia": "1/2\" gyp board", "qty": 16.0, "unit": "SF",
    "source": "A-052 general note 9 'PATCH EXISTING DRAFTSTOP WALL BETWEEN KITCHEN AND SERVICE AT NEW BEVERAGE CHASES' + P-211 beverage conduit piping plan (conduit bundle above ceiling crossing the kitchen / service line); chase size and count not printed (RFI-20); C09250 2.1.B / A-909",
    "op": "2 chases (6\" beverage conduit bundle + CO2 conduit, P-211) x 2.0 ft x 2.0 ft patch x 2 faces = 16.0 SF [conservative allowance, RFI-20]"})
c["rfis"].append({"id": "RFI-20", "status": "open - conservative value loaded",
    "question": "A-052 general note 9: patch the existing draftstop wall between kitchen and service at the new beverage chases: number and size of the chases printed nowhere (P-211 shows the conduit routing only).",
    "fuentes_revisadas": ["A-052", "A-221", "P-211", "M-201"],
    "opciones": {"A": {"texto": "Plans: 2 chases x 2'-0\" x 2'-0\" patch x 2 faces = 16 SF of 1/2\" gypsum board loaded", "source": "A-052 note 9 + P-211",
                       "delta": "0 (loaded); per extra chase +8 SF; if the draftstop board is 5/8\" Type X: same SF in 5/8\" Type X"},
                 "B": {"texto": "Draftstop penetrations restored with the same construction", "cita": "IBC 718.3 / ASTM C840", "delta": "same"}, "C": ""},
    "source": "A-052, P-211"})
log("Patch of existing draftstop wall at new beverage chases", "not addressed", "16 SF 1/2\" gyp (allowance) + RFI-20", "+16 SF", "A-052 note 9, P-211", "decision 12")

# ---------------------------------------------------------------- 13. existing board under new restroom cement board (A-050 KN10)
rr = [("EX-RRM-01-CB"), ("EX-RRM-02-CB"), ("EX-RRW-01-CB"), ("EX-RRW-02-CB")]
dsf = round(sum(float(E[i]["length_ft"]) * float(E[i]["height_ft"]) for i in rr), 2)
c["misc_items"].append({"ref": "DEMO-14", "familia": "demolition - gypsum board and metal framing", "qty": dsf, "unit": "SF",
    "source": "A-050 KN10 'remove existing wall finishes and prepare for new' at the restrooms + new 1/2\" cement board behind CT-57A / CT-77 (A-611): existing gypsum board under the new cement board removed (RFI-19)",
    "op": " + ".join(f"{i} {E[i]['length_ft']} x {E[i]['height_ft']}" for i in rr) + f" = {dsf} SF x 1 layer [conservative, RFI-19]"})
c["rfis"].append({"id": "RFI-19", "status": "open - conservative value loaded",
    "question": "Restrooms (A-050 KN10, A-611): is the existing gypsum board removed before the new 1/2\" cement board, or does the cement board go over it? Printed nowhere.",
    "fuentes_revisadas": ["A-050", "A-611", "A-202"],
    "opciones": {"A": {"texto": f"Plans: existing board removed under the new cement board: {dsf} SF demolition loaded", "source": "A-050 KN10 + A-611", "delta": f"0 (loaded); over existing board: -{dsf} SF demolition"},
                 "B": {"texto": "Cementitious backer units are fastened to framing, not over gypsum, at wet tile walls", "cita": "ASTM C840 / ANSI A108.11 / TCNA", "delta": "same as A"}, "C": ""},
    "source": "A-050, A-611"})
log("Demolition of existing board under new restroom cement board (DEMO-14)", "0 SF", f"{dsf} SF + RFI-19", f"+{dsf} SF demolition", "A-050 KN10, A-611", "decision 13")

# ---------------------------------------------------------------- 15. W6-04-KIT printed 2'-2 3/4"
e = E["W6-04-KIT"]
l0 = e["length_ft"]
e["length_ft"] = 2.229
(x0, y0), (x1, y1) = e["path"][0], e["path"][-1]
e["path"][-1] = [round(x0 + 2.229 * 18.0, 1), y1]
e["length_op"] = "A-202 printed 2'-2 3/4\" = 2.229 ft (path adjusted to the printed dimension: 40.1 pt / 18)"
log("W6-04-KIT length", f"{l0} LF", "2.229 LF (printed 2'-2 3/4\")", f"{round(2.229 - l0, 3)} LF x 1.5 ft x 2 faces = {round((2.229 - l0) * 3, 2)} SF cement board", "A-202", "decision 15")

# ---------------------------------------------------------------- 17. split strongback; RFI-17 closed; text claims
M["SOF-STRONGBACK"]["product"] = {"value": "362T125-54 strongback to each truss @ 48\" (C3/S-801)", "source": "C3/S-801"}
log("Strongback 362T125-54 (26.51 LF)", "inside the ceiling / soffit track row", "own row (product split)", "0 LF", "C3/S-801", "decision 17")
for r in c["rfis"]:
    if r["id"] == "RFI-17":
        r["status"] = "closed - estimator decision (option A)"
        r["question"] = ("Untagged new infill MB-01 at the removed Eliason door (A-050 KN1): D3/A-624 prints '2X6 WOOD FRAMING OR 6\" METAL FRAMING AT 16\" O.C.'; "
                         "NOTE: loaded 6\" metal (metal-or-wood standing order); investigate D3/A-624 vs C2/S-801 '362S162-33'.")
        r["opciones"] = {"A": {"texto": "Plans: 6\" metal studs @ 16\" per D3/A-624 (loaded)", "source": "D3/A-624 + C2/S-801",
                               "delta": "0 (loaded); 3-5/8\" alternative (C2/S-801 362S162-33): the same MB-01 studs and 2 x 3.33 LF track move from the 6\" to the 3-5/8\" family; 2x6 wood alternative: framing Div. 06 (excluded), board unchanged"},
                         "B": {"texto": "n/a", "cita": "ASTM C754", "delta": "n/a"}, "C": ""}
        r["fuentes_revisadas"] = ["A-050", "A-202", "D3/A-624", "C2/S-801"]
log("RFI-17 (MB-01 type)", "open - 'printed nowhere'", "closed - D3/A-624 prints 2x6 wood or 6\" metal -> 6\" metal", "see MB-01", "D3/A-624", "decision 4 / 17")
for e in c["existing_walls"]:
    for k in ("height_source", "source"):
        if isinstance(e.get(k), str) and "-> RFI-02" in e[k]:
            e[k] = e[k].replace("-> RFI-02", "-> RFI-03 (closed, estimator decision option A)")
log("Kitchen base rows RFI reference", "-> RFI-02", "-> RFI-03 (closed)", "text", "A-050 KN16", "decision 17")

# ---------------------------------------------------------------- 11, 14 exclusions
c["scope_notes_info"] += [
    "EXCLUDED - 3\"x3\"x1/4\" clip angles @ 48\" at the roof hatch shaft (A1/A-604): structural / miscellaneous steel, not cold-formed framing",
    "EXCLUDED - Unistrut for suspended shelving and shrouds (K-001 equipment note 6): kitchen equipment / MEP trade"]
log("Roof hatch 3x3x1/4 clip angles", "not addressed", "EXCLUDED note (misc steel)", "0", "A1/A-604", "decision 11")
log("K-001 note 6 Unistrut", "not addressed", "EXCLUDED note", "0", "K-001", "decision 14")

# ---------------------------------------------------------------- 9 / 17 / 18: notes on the Material Summary rows (constants.ms_notes)
cs = c["constants"]
cs["ms_notes"] = [
    {"match": r"stud|track|joist|brace|Z-furring", "note": "Spec: C09111 Non-load-bearing steel framing 2.3 (A-909); gauge per plans 33 mil (S-801 / S-241) - S-902 C05000-C 2.5.A.1 asks 0.0538 in: RFI-18 closed, estimator decision option A (54 mil alternative = same LF)", "source": "C09111 / A-909, S-902"},
    {"match": r"Z-furring", "note": "PRODUCT: 2\" metal Z channel @ 24\" O.C. (A-202 M2.1 schedule, A1/A-605); the row label is the template family name", "source": "A-202 M2.1, A1/A-605"},
    {"match": r"5/8\" gypsum board, regular", "note": "PRODUCT: 5/8\" sag-resistant gypsum ceiling board (C09250 2.1.E / 3.2.A.3, A-909) - all 332.06 SF are ceilings; the row label is the template family name", "source": "C09250 2.1.E / A-909"},
    {"match": r"gypsum board|cement board|cementitious", "note": "Spec: C09250 Gypsum Board 2.1 / 2.2 (A-909)", "source": "C09250 / A-909"},
    {"match": r"^Joint compound|^Joint tape", "note": "Driver = gypsum board SF only: 1/2\" regular + 5/8\" sag-resistant ceiling board + 1/2\" moisture resistant; the 1/2\" cement board joints take alkali-resistant mesh tape + setting-type compound (C09250 2.4.B.2 / 2.4.D.2 / 3.5.E, manufacturer) in their own row; W.R. board joints setting-type compound (2.4.D.1)", "source": "C09250 2.4 / A-909"},
    {"match": r"1/2\" gypsum board, MOISTURE RESISTANT", "note": "Spec C09250 2.2.A.2 calls 5/8\" Type X W.R.; plan A-202 notes G.1 / H.3 print 1/2\": plan thickness loaded (RFI-21 closed, option A); delta = same 148.02 SF as 5/8\" Type X W.R.", "source": "C09250 2.2.A.2 / A-909, A-202"},
    {"match": r"Demolition", "note": "Includes DEMO-14 existing board under the new restroom cement board (RFI-19, conservative)", "source": "A-050 KN10"},
]
log("Spec section on every framing / board row; notes on Z channel, ceiling board, compound / tape driver", "missing", "constants.ms_notes", "text", "C09111 / C09250 / A-909, S-902", "decisions 7, 9, 17, 18")

# ---------------------------------------------------------------- 18. citations / internal codes in client text
RX = [(re.compile(r"\b([A-H])\.(\d{1,2})/(A-\d{3})(\.\.A-\d{3})?"), lambda m: f"{m.group(3)}{m.group(4) or ''} note {m.group(1)}.{m.group(2)}"),
      (re.compile(r"\bWD-3/CT-73B"), lambda m: "WD-3 / CT-73B"),
      (re.compile(r"Scope rule R-ALC-01 \(user 2026-11-01\): "), lambda m: "Estimator standing order: "),
      (re.compile(r"\s*\(?R-ALC-\d+\)?"), lambda m: ""),
      (re.compile(r"\bresolver\b:?"), lambda m: "double-reading resolution:"),
      (re.compile(r"\bPT\d{4}\b"), lambda m: "tag")]
SKIP = {"id", "tag_ids", "img", "height_img", "detail_img", "stud_img", "img_refs", "wall", "ref", "path", "band", "tag"}
n18 = [0]


def limpia(o):
    if isinstance(o, dict):
        for k, v in list(o.items()):
            if k in SKIP:
                continue
            if isinstance(v, str):
                s = v
                for rx, f in RX:
                    s = rx.sub(f, s)
                if s != v:
                    o[k] = s; n18[0] += 1
            else:
                limpia(v)
    elif isinstance(o, list):
        for x in o:
            limpia(x)


for k in ("walls", "existing_walls", "misc_items", "ceilings", "details", "trim_items", "blocking_items", "level5_items",
          "rfis", "accesorios_none", "scope_notes_info", "deflection_clips", "ceilings_info"):
    if k == "scope_notes_info":
        c[k] = [s if not isinstance(s, str) else re.sub(r"\s*\(?R-ALC-\d+\)?", "", s) for s in c[k]]
    else:
        limpia(c.get(k))
log("Citations / internal codes in client text", "G.2/A-202 style, WD-3/CT-73B, R-ALC-xx, resolver, PT00xx", "A-202 note G.2, sheet + note, no internal codes",
    f"{n18[0]} text fields", "all", "decision 18")
for r in c["rfis"]:
    r.setdefault("img", {"RFI-18": "img_rev2/S801_D1_schedule.png", "RFI-19": "img_runner/sheet_A-050.png",
                         "RFI-20": "img_runner/sheet_A-052.png"}.get(r["id"], "img_runner/sheet_A-202.png"))
for t_ in c["trim_items"]:
    t_.setdefault("img", "img_runner/sheet_A-624.png")
for wid in ("M3.5-01", "M3.5-02"):
    W[wid]["to_deck_source"] = ("D1/S-801 TYP. MTL PARTITION WALL BRACING BELOW TRUSS: 33 mil continuous (fixed) top track, braces "
                                "@ 48\" to the truss, no slip track / gap; wall stops 6\" above ceiling (A-202 note C.1); RFI-04 if extended to deck")
for r in c["rfis"]:
    if r["id"] == "RFI-14":
        r["opciones"]["A"]["texto"] = "Plans: 3'-0\" x 3'-0\" x 4.0 ft metal shaft loaded (48 LF stud + 12 LF bottom runner + 12 LF 3\" long-leg slotted top track per C1/S-801)"
        r["question"] += " The 3\"x3\"x1/4\" clip angles @ 48\" of A1/A-604 are miscellaneous steel (EXCLUDED)."
cs["drywall_screws_per_sf"] = {"value": 1.2, "source": "estimator standing input (Gypsum Association field / perimeter screw spacing); fasteners EXCLUDED (C09250 2.5.B / A-909)"}
cs["rev2_applied"] = {"value": "2026-11-02", "source": "proceso/CAMBIOS_rev2.md"}
json.dump(c, open(P, "w"), indent=1, ensure_ascii=False)
json.dump(LOG, open(os.path.join(C4, "rev2_log.json"), "w"), indent=1, ensure_ascii=False)
print(len(LOG), "changes")
