"""rev4 (user order 3-nov: the RFIs are answered from the drawings). Applies the answers of cfa_rfi4/g1..g3
(respuestas_g*.json: answer, N/SHEET, status, sheets swept, grep terms, circled crops) to the canon after
correcciones_rev3.py. Input changes only; quantities by canon.py / accesorios.py / plantilla_excel.py (skill v81cf11).
Counts / lengths written here are computed by THIS program with their operation. Log -> etapas/4_canon/rev4_log.json.
Use: python3 bitacora.py run scripts/correcciones_rev4.py"""
import json, math, os, re
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.dirname(K)
P = os.path.join(K, "etapas", "4_canon", "takeoff_canon.json")
c = json.load(open(P))
ANS = {}
for g in ("g1", "g2", "g3"):
    for x in json.load(open(os.path.join(S, "cfa_rfi4", g, f"respuestas_{g}.json"))):
        ANS[x["rfi"]] = x
LOG = []
log = lambda *a: LOG.append(dict(zip(("item", "rev3", "rev4", "delta", "src", "rule"), a)))
W = {w["id"]: w for w in c["walls"]}
E = {e["id"]: e for e in c["existing_walls"]}
M = {m["ref"]: m for m in c["misc_items"]}
R = {r["id"]: r for r in c["rfis"]}
TXT = open(os.path.join(S, "cfa_rfi4", "set_text.txt"), encoding="utf-8", errors="replace").read().upper()


def img(x):
    v = x.get("img")
    v = v[0] if isinstance(v, list) else v
    b = os.path.basename(str(v or ""))
    return "img_rev4/" + b if b and os.path.exists(os.path.join(K, "etapas", "4_canon", "img_rev4", b)) else "img_runner/sheet_A-202.png"


def barrido(x):
    """barrido {hojas, terminos, grep}: sheets and terms of the sweep (respuestas_g*.json); grep = count of each term
    in the full text of the set (set_text.txt: text layer + SHX annotations), computed here."""
    cnt = {t: len(re.findall(re.escape(t.upper()) if not any(ch in t for ch in ".*") else t.upper(), TXT)) for t in x["grep_terms"]}
    return {"hojas": x["sheets_swept"], "terminos": x["grep_terms"],
            "grep": "full text of the 172-page set (text layer + SHX annotations): " + ", ".join(f"'{t}' {n}" for t, n in cnt.items())}


def resolver(rid, extra=""):
    x = ANS[rid]
    r = R[rid]
    r["status"] = "resolved - from drawings"
    r["resolved"] = {"answer": x["answer"] + extra, "status": x["status"], "source": x["source"]}
    r["img"] = img(x)
    r["barrido"] = barrido(x)


def abierto(rid, question, a_texto, a_delta, extra_why=""):
    x = ANS[rid]
    r = R[rid]
    r["status"] = "open - conservative value loaded"
    r["question"] = question
    r["opciones"]["A"]["texto"] = a_texto
    r["opciones"]["A"]["delta"] = a_delta
    r["barrido"] = barrido(x)
    r["img"] = img(x)
    r["why_not_printed"] = x.get("why_not_printed", "") + extra_why


# ---------------- RFI-02: 16" O.C. DERIVED (no change)
resolver("RFI-02")
log("RFI-02 M3.5 stud spacing", "open (16\" loaded)", "RESOLVED from drawings: 16\" O.C. (sistered 1:1 to existing 2x6 @ 16\")", "0",
    "A-202 M3.5 + D.1, S-101 note 4, D1/S-601", "RFI answered from the drawings (3-nov)")
# ---------------- RFI-04: smoke partition to the deck 14'-8"
DECK = 14.667
for wid in ("M3.5-01", "MB-01"):
    w = W[wid]
    h0 = w["height_ft"]
    w["height_ft"] = DECK
    w["height_status"] = "CONFIRMADO"
    w["height_source"] = ("S-201 C4 (+14'-8\") T.O. joist / truss at both ends of the smoke partition line (S-201 note 1) + A-221 note A.11 "
                          "smoke partition + A-202 note C.2 'extend framing to roof deck' = 14.667 ft [CONFIRMED]")
    w["top_track_kind"] = "slip"
    w["top_track_kind_source"] = "C1/S-801 TYP. MTL PARTITION WALL BRACING AT TRUSS '3\" LONG LEGGED SLOTTED CONT. TRACK' (wall reaches the truss)"
    w["to_deck_source"] = "C1/S-801: 3\" long-legged slotted continuous track at the truss, 1\" gap; wall to deck (A-202 note C.2, S-201 +14'-8\")"
    for f in w["faces"]:
        f0 = f["height_ft"]
        if "cement" in f["board"]:
            f["height_ft"] = DECK
            f["height_source"] = ("A-202 note G.4 exception at draftstopping: 1/2\" cementitious board full height to the deck 14'-8\" "
                                  "(S-201 C4); C09250 Gypsum Board 2.2.B (DUROCK) / A-909")
        else:                       # MB-01 serving face: gypsum from B.O. 7'-0" (D3/A-624) to the deck
            f["height_ft"] = round(DECK - 7.0, 3)
            f["height_source"] = ("D3/A-624 B.O. gypsum 7'-0\" A.F.F. to the deck 14'-8\" (S-201 C4, draftstop full height A-202 note G.4) = "
                                  f"{round(DECK - 7.0, 3)} ft; C09250 Gypsum Board 2.1.B / A-909")
        log(f"{wid} face {f.get('room')} board height (smoke partition)", f"{f0} ft", f"{f['height_ft']} ft", f"+{round(f['height_ft'] - f0, 3)} ft x {w['length_ft']} LF",
            "S-201 C4, A-202 notes C.2 / G.4", "RFI-04 resolved")
    log(f"{wid} framing height (smoke partition)", f"{h0} ft", f"{DECK} ft to the deck", f"+{round(DECK - h0, 3)} ft of stud x studs of the wall",
        "S-201 C4 (+14'-8\"), A-202 note C.2", "RFI-04 resolved")
    log(f"{wid} top track", "standard (D1 braces below the truss)", "3\" long-leg slotted track C1/S-801 (own row)", "track kind", "C1/S-801", "RFI-04 resolved")
# walls that now reach the deck do not take the D1 'below truss' braces
drop = [m["ref"] for m in c["misc_items"] if m["ref"] in ("BRC-M3.5-01", "BRC-MB-01")]
q_drop = round(sum(M[r]["qty"] for r in drop), 2)
c["misc_items"] = [m for m in c["misc_items"] if m["ref"] not in drop]
pl = [m for m in c["misc_items"] if m["ref"] == "BRC-PLATES"][0]
n_pl = sum(m.get("pcs", 0) for m in c["misc_items"] if m["ref"].startswith("BRC-") and m["ref"] != "BRC-PLATES")
log("D1/S-801 braces at M3.5-01 / MB-01", f"{q_drop} LF", "0 (walls reach the truss: C1/S-801 applies, not D1)", f"-{q_drop} LF 3-5/8\"", "C1 / D1 S-801", "RFI-04 resolved")
log("54 mil bent plates", f"{pl['qty']} pcs", f"{n_pl} pcs (M3.5-02 braces only)", f"{n_pl - pl['qty']} pcs", "D1/S-801", "RFI-04 resolved")
pl["qty"] = n_pl
pl["op"] = f"BRC-M3.5-02 {n_pl} = {n_pl} plates (one per brace; M3.5-01 / MB-01 reach the truss, C1/S-801)"
# back-check rev4 #1: W6-01N-GB1 is the PUBLIC (dining) face of the W6 on the smoke line: A-221 note A.11 'on public side,
# extend wall sheathing ... to 6" above finish ceiling' -> its rev3 height (10.417 ft) stays; only the BOH face goes to the deck
log("W6-01N-GB1 board height (public face of the smoke partition)", f"{E['W6-01N-GB1']['height_ft']} ft", f"{E['W6-01N-GB1']['height_ft']} ft (unchanged)", "0",
    "A-221 note A.11 (public side: sheathing to 6\" above finish ceiling)", "back-check rev4 #1")
for eid in ("W6-01S-SRV",):
    e = E[eid]
    h0 = e["height_ft"]
    base = 0.417 if eid.endswith("GB1") else 0.0
    e["height_ft"] = round(DECK - base, 3)
    e["height_source"] = (f"smoke partition line (A-221 note A.11): board full height to the deck 14'-8\" (S-201 C4) per A-202 note G.4 "
                          f"draftstop exception" + (" from the 5\" cement board base" if base else "") + f" = {e['height_ft']} ft [CONFIRMED]")
    e["source"] = e["source"] + " | smoke partition: to deck 14'-8\" (S-201 C4)"
    log(f"{eid} board height (smoke partition)", f"{h0} ft", f"{e['height_ft']} ft", f"+{round((e['height_ft'] - h0) * e['length_ft'], 2)} SF",
        "S-201 C4, A-202 note G.4, A-221 note A.11", "RFI-04 resolved")
resolver("RFI-04")
# ---------------- RFI-06: G.11 gyp to 10'-8" (loaded 1.0 + 9.667 = 10.667: no change)
resolver("RFI-06")
log("RFI-06 walk-in G.11 board height", "open (10'-8\" loaded)", "RESOLVED from drawings: 10'-2\" C.H. + 6\" = 10'-8\" AFF", "0", "A-202 G.11, A-221 KN2 + C.H.", "RFI answered")
# ---------------- RFI-10: demolition heights per bay
HN = {"DEMO-04": (12.25, "CONFIRMADO", "B/existing 5-1/4\"x18\" PSL 12'-3\" F.V. (A4/S-601)"),
      "DEMO-13": (12.979, "CONFIRMADO", "cut at T/new LVL 12'-11 3/4\" (A4/S-601 'CUT EXISTING STUD WALL TO SIT ON NEW BEAM'); wall above stays"),
      "DEMO-08": (12.167, "PENDIENTE", "B.O. 16\" TJI = 13'-6\" - 16\" = 12'-2\" (A3/S-601 + S-201) loaded; KN24 cased opening: opening / header height printed nowhere (RFI-10)"),
      "DEMO-09": (16.896, "PENDIENTE", "B.O. 2x10 roof joists 16'-6 1/4\"..16'-10 3/4\" (A4/S-601, S-201): 16'-10 3/4\" loaded; KN24 cased opening: opening / header height printed nowhere (RFI-10)"),
      "DEMO-10": (16.896, "PENDIENTE", "B.O. 2x10 roof joists 16'-6 1/4\"..16'-10 3/4\" (A4/S-601, S-201): 16'-10 3/4\" loaded; KN24 cased opening: opening / header height printed nowhere (RFI-10)")}
G = {g["id"]: g for g in c["demo_geom"]}
for ref, (h, st, why) in HN.items():
    m, g = M[ref], G[ref]
    lf, ly = float(g["lf"]), int(g["layers"])
    sf = round(lf * h * ly, 2)
    log(f"{ref} demolition height", f"{g['h_ft']} ft / {m['qty']} SF", f"{h} ft / {sf} SF", f"{round(sf - m['qty'], 2):+} SF", "A4/S-601, A3/S-601, S-201",
        "RFI-10 " + ("resolved" if st == "CONFIRMADO" else "partial (opening height still open)"))
    m["qty"] = sf
    m["op"] = f"{lf} LF x {h} ft x {ly} layer(s) = {sf} SF ({why})"
    m["source"] = re.sub(r"\[PENDING[^\]]*\]", "", m["source"]) + f" | height: {why}"
    g.update(h_ft=h, sf=sf, h_status=("CONFIRMED" if st == "CONFIRMADO" else "PENDING (opening height, RFI-10)"))
abierto("RFI-10", "Demolition at the KN24 cased openings (DEMO-08, -09, -10, existing east wall): the height of the wall portion removed = the "
        "opening / (3)2x12 header height, printed nowhere (A-602 shows 'OPEN TO BEYOND' without a dimension). The other demolition heights "
        "are resolved from A4/S-601, A3/S-601 and S-201.",
        "Plans: removed to the B.O. structure printed: DEMO-08 12'-2\" (16\" TJI bay), DEMO-09 / -10 16'-10 3/4\" (2x10 bay) loaded",
        "0 (loaded); per ft of header height below the B.O. structure: -1.83 SF (DEMO-08), -4.5 SF each (DEMO-09 / -10)")
# ---------------- RFI-13: 24" box (loaded 2'-0")
resolver("RFI-13")
log("RFI-13 pin & sleeve recess width", "open (2'-0\" loaded)", "RESOLVED from drawings: L = 24\" double pin & sleeve (MH-102)", "0", "MH-102, A2/A-605", "RFI answered")
# ---------------- RFI-14: hatch 2'-6" x 3'-0", shaft 5'-4"
sh = M["RH-SHAFT-S"]
a, b, H = 3.0, 2.5, 5.333
na, nb = math.ceil(a / (16 / 12)) + 1, math.ceil(b / (16 / 12)) + 1
pcs = 2 * (na + nb) - 4
per = 2 * (a + b)
q0 = (sh["qty"], M["RH-SHAFT-T"]["qty"], M["RH-SHAFT-TT"]["qty"])
sh.update(qty=round(pcs * H, 2), pcs=pcs, op=f"2'-6\" x 3'-0\" shaft: 2 x ({na} + {nb}) - 4 shared corners = {pcs} studs (ROUNDUP(side / 1.333) + 1) x {H} ft = {round(pcs * H, 2)} LF")
sh["source"] = re.sub(r"\[PENDING[^\]]*\]", "", sh["source"]) + " | hatch 2'-6\" x 3'-0\" (A-230 legend + KN3, C07740 / A-906); shaft 13'-6\" deck (S-201) - (10'-2\" - 2'-0\") = 5'-4\" DERIVED"
for ref in ("RH-SHAFT-T", "RH-SHAFT-TT"):
    M[ref]["qty"] = per
    M[ref]["op"] = f"shaft perimeter 2 x (3.0 + 2.5) = {per} LF (" + ("bottom runner 24\" below ceiling, A1/A-604)" if ref == "RH-SHAFT-T" else "3-5/8\" web: top runner at the roof framing, C1/S-801)")
log("Roof hatch shaft studs", f"{q0[0]} LF (3'-0\" x 3'-0\" x 4.0 ft assumed)", f"{sh['qty']} LF ({pcs} studs x 5'-4\")", f"{round(sh['qty'] - q0[0], 2):+} LF 3-5/8\"",
    "A-230, C07740 / A-906, A1/A-604, S-201", "RFI-14 resolved")
log("Roof hatch shaft runner + slotted top track", f"{q0[1]} + {q0[2]} LF", f"{per} + {per} LF", f"{per - q0[1]:+} LF each", "A-230, A1/A-604, C1/S-801", "RFI-14 resolved")
resolver("RFI-14")
# ---------------- RFI-15: soffit hanger studs 3'-0"
for w in c["walls"]:
    if w.get("element") == "soffit_side":
        h0 = w["height_ft"]
        w["height_ft"] = 3.0
        w["height_status"] = "DERIVADO"
        w["height_source"] = ("hanger studs from the soffit bottom C.H. 9'-8\" (A-221) to the B.O. structure 12'-8\" (S-201 C4: T.O. 14'-8\" - 24\" TJS) "
                              "= 3'-0\" [DERIVED] (2'-8 1/2\" at the PSL; 3'-0\" loaded); C4/A-624, C3/S-801")
log("Soffit side hanger stud height (8 sides, 73.44 LF)", "1.167 / 0.833 ft (board side height)", "3.0 ft", "studs x (3.0 - side height)", "S-201 C4, A-221, C4/A-624", "RFI-15 resolved")
SS = {w["id"]: w for w in c["walls"] if w.get("element") == "soffit_side"}
for ref, run_w, a_, b_ in (("XBR-SRV-W", "SS-SRV-W", "SS-SRV-W", "SS-SRV-IV"), ("XBR-SRV-N", "SS-SRV-IH", "SS-SRV-N", "SS-SRV-IH"), ("XBR-GT", "SS-GT-W", "SS-GT-W", "SS-GT-E")):
    m = M[ref]
    run = float(SS[run_w]["length_ft"])
    wd = round(abs((SS[b_]["band"]["c0"] + SS[b_]["band"]["c1"]) / 2 - (SS[a_]["band"]["c0"] + SS[a_]["band"]["c1"]) / 2) / 18.0, 3)
    n = math.ceil(run * 12 / 32.0) + 1
    rise = min(wd, 3.0)
    ln = round(math.hypot(wd, rise), 3)
    q0 = m["qty"]
    m.update(qty=round(n * ln, 2), pcs=n, op=f"ROUNDUP({run} x 12 / 32) + 1 = {n} braces x sqrt(width {wd}^2 + rise {rise}^2) = {ln} ft "
                                             f"(1:1 as drawn in C4/A-624, rise limited by the 3'-0\" hanger studs) = {round(n * ln, 2)} LF")
    log(f"{ref} soffit cross braces", f"{q0} LF", f"{m['qty']} LF", f"{round(m['qty'] - q0, 2):+} LF", "C4/A-624, C3/S-801, S-201", "RFI-15 resolved")
resolver("RFI-15")
# ---------------- RFI-19 confirmed (617.08 SF demo stands)
resolver("RFI-19")
M["DEMO-14"]["op"] = M["DEMO-14"]["op"].replace("[conservative, RFI-19]", "[CONFIRMED A2/A-604 + A-202 note G.2]")
log("RFI-19 existing board under restroom cement board", "open (617.08 SF loaded)", "RESOLVED from drawings: removed (A2/A-604, A-202 G.2)", "0", "A2/A-604, A-202 G.2, A-050 KN10", "RFI answered")
# ---------------- RFI-20: 4 sleeves -> 4 patches; size stays open
pb = M["PATCH-BEV"]
q0 = pb["qty"]
pb["qty"] = 32.0
pb["op"] = "4 chases (4 new 6\" beverage conduits crossing the kitchen / service wall, P-211 + K-611 '6\" PVC sleeve penetrations') x 2.0 ft x 2.0 ft patch x 2 faces = 32.0 SF [patch size RFI-20]"
log("Draftstop patch at beverage chases", f"{q0} SF (2 chases)", "32.0 SF (4 chases, P-211 + K-611)", f"+{32.0 - q0} SF 1/2\" gyp", "A-052 note 9, P-211, K-611", "RFI-20 partial")
abierto("RFI-20", "A-052 general note 9: patch the existing draftstop wall between kitchen and service at the 4 new 6\" beverage chases (P-211, K-611): the patch size around each chase is printed nowhere.",
        "Plans: 4 chases x 2'-0\" x 2'-0\" patch x 2 faces = 32 SF of 1/2\" gypsum board loaded",
        "0 (loaded); per 6\" of patch side: about +/- 7 SF over the 4 chases; if the draftstop board is 5/8\" Type X: same SF in 5/8\" Type X")
# ---------------- still open: barrido attached
for rid in ("RFI-07", "RFI-09", "RFI-11", "RFI-12"):
    x = ANS[rid]
    R[rid]["barrido"] = barrido(x)
    R[rid]["img"] = img(x)
    R[rid]["why_not_printed"] = x.get("why_not_printed", "")
    log(f"{rid} still open", "open", "open with full sweep (sheets / terms / grep of the set)", "0", x["source"], "A_RFI_BARRIDO")
# ---------------- BE-117 (coordinator 3-nov): every markup carries an ID that exists in the Excel; causes written
# where a markup outline is not the measured quantity. Quantities unchanged.
for cl, cid in zip(c["ceilings"][:2], ("SOF-SRV-B", "SOF-GT-B")):
    assert "soffit" in cl["room"].lower(), cl["room"]
    cl["id"] = cid
mi = c["misc_items"]
for base, n_ in (("PS-RECESS-S", 2), ("PS-RECESS-T", 2)):
    k = next(i for i, m in enumerate(mi) if m["ref"] == base)
    m = mi.pop(k)
    for j, wid in enumerate(("M3.5-01", "M3.5-02"), 1):
        x = dict(m, ref=f"{base}{j}", qty=round(m["qty"] / n_, 3))
        if "pcs" in x:
            x["pcs"] = m["pcs"] // n_
        x["op"] = (f"1 recess on {wid} x 2 jamb studs x 10.667 ft = {x['qty']} LF" if base.endswith("S")
                   else f"1 recess on {wid} x (head + sill) x 2.0 ft = {x['qty']} LF")
        x["source"] = (m["source"].replace("box width not printed -> 2 jamb studs per recess assumed (RFI-13 open)",
                                           "box L = 24\" double pin & sleeve (MH-102; RFI-13 resolved from drawings) -> 2 jamb studs per recess")
                       .replace("width 2'-0\" assumed (RFI-13 open)", "width 2'-0\" = the 24\" box (MH-102; RFI-13 resolved)")
                       + f"; recess {j} of 2 on {wid} (A-201 hood #{j + 1} bubble)")
        assert "RFI-13 open" not in x["source"], x["source"]
        if base.endswith("S"):
            x["length_cause"] = ("markup = recess outline on the wall in plan (24\" box, MH-102); the LF is the 2 jamb "
                                 "studs x 10'-8\" stud height of A2/A-605, a vertical quantity, not a plan length")
        mi.insert(k + j - 1, x)
    log(f"{base} split per recess (BE-117 markup ID)", f"{m['qty']} LF in 1 item", f"2 items x {round(m['qty'] / n_, 3)} LF", "0", "A2/A-605", "BE-117")
M = {m["ref"]: m for m in mi}
M["RH-SHAFT-S"]["length_cause"] = ("markup = the 2'-6\" x 3'-0\" roof hatch opening (A-230 KN3 / A-906) drawn on A-221, perimeter 11.0 LF "
                                   "(= runner RH-SHAFT-T); the 53.33 LF is 10 studs x 5'-4\" shaft height (A1/A-604, S-201), not a plan length")
c["level5_items"][0]["length_cause"] = ("markup = play area room outline on A-221; the 59.69 LF is the solid-wall perimeter measured on A-202 "
                                        "(length_op, bay glazing excluded), so the outline perimeter is not the LF")
if "A-202" not in M["DEMO-14"]["source"]:
    M["DEMO-14"]["source"] += "; the 4 parts are the existing restroom walls EX-RRM-01/-02, EX-RRW-01/-02 drawn on A-202"
log("BE-117 markup IDs", "soffit bottoms / recesses / Level 5 / shaft without Excel ID", "SOF-SRV-B, SOF-GT-B, PS-RECESS-S1/S2, L5-PLAY, RH-SHAFT-S + causes", "0", "A-221, A-202, A2/A-605, A1/A-604", "BE-117")
# back-check rev4 #2: RFI-20 'why not printed' sentence from the answer file still said 2 chases loaded
r20 = R["RFI-20"]
r20["why_not_printed"] = r20["why_not_printed"].replace(
    "The current load is 2 chases at 2'-0\" x 2'-0\". Per P-211 the count should be 4 chases at 6\" dia conduits.",
    "Loaded: 4 chases (P-211, 4 x 6\" dia beverage conduits) x 2'-0\" x 2'-0\" x 2 faces = 32 SF.")
assert "2 chases" not in json.dumps(r20), "RFI-20 still says 2 chases"
log("RFI-20 Pending Items text", "'current load is 2 chases'", "4 chases / 32 SF loaded (P-211); only the patch size is open", "0 (text)", "A-052 note 9, P-211", "back-check rev4 #2")
# coordinator (rev4 back-check): ceiling bridging cites A2/S-241 'BRIDGING LOCATION: MID SPAN' + S-902 C05400 bridging by analogy,
# not C09111 3.2.C (suspended-ceiling sway bracing)
OLD = "C09111 3.2.C 'sway-brace suspension systems' / 3.1.A ASTM C754 (A-909)"
NEW = "S-902 C05400 3.4.E.2 bridging = cold-rolled steel channel (wall studs; used by analogy for the joist bridging member)"
nb = 0
for m in c["misc_items"]:
    if m["ref"].endswith("-BRG") and OLD in m["source"]:
        m["source"] = m["source"].replace(OLD, NEW); nb += 1
assert nb == 5, nb
for n in c["constants"]["ms_notes"]:
    if n.get("match") == r"^Bracing":
        n["note"] = "Spec: A2/S-241 'BRIDGING LOCATION: MID SPAN' (printed); member by analogy with S-902 C05400 3.4.E.2 bridging (cold-rolled channel)"
        n["source"] = "A2/S-241 + S-902 C05400"
r9 = R["RFI-09"]
r9["question"] = "A2/S-241 LGS schedule prints 'BRIDGING LOCATION: MID SPAN' but no bridging member (S-902 C05400 3.4.E.2 lists cold-rolled channel bridging for wall studs only)."
r9["opciones"]["A"]["source"] = r9["source"] = "A2/S-241 + S-902 C05400 3.4.E.2 (by analogy)"
r9["opciones"]["B"]["cita"] = "AISI S240 / S-902 C05400 3.4.E.2"
assert "3.2.C" not in json.dumps(r9) and not any("3.2.C" in m["source"] for m in c["misc_items"] if m["ref"].endswith("-BRG"))
log("Ceiling bridging citation (C.R. channel row, RFI-09)", "C09111 3.2.C (A-909)", "A2/S-241 MID SPAN + S-902 C05400 3.4.E.2 by analogy", "0 (text)", "A2/S-241, S-902", "back-check rev4 #3")
json.dump(c, open(P, "w"), indent=1, ensure_ascii=False)
json.dump(LOG, open(os.path.join(K, "etapas", "4_canon", "rev4_log.json"), "w"), indent=1, ensure_ascii=False)
print(len(LOG), "rev4 changes")
