"""rev9 (coordination adversarial audit of rev8, U-138, 4-nov). Runs after correcciones_rev7.py (the rev8 furr-down step is no longer
in the chain: see 3). Every quantity recomputed by canon.py / accesorios.py / plantilla_excel.py.
  1. #0: the Source of every board-only entry embeds its height text ('| height: ...'); after rev6 / rev7 several kept the OLD text
     (G.3/A-202 1'-0" [CONFIRMED] on rows loaded at 1.25 ft from C3/A-604; restroom 6.708 / 2.625 on rows loaded 6.521 / 2.8125).
     The height part of the Source is rewritten from the entry's current height_source (one source, one number).
  2. W6-09-OUT-1 (same office W6, same corridor / service faces as W6-09-OUT-2) loaded at 1.0 ft: unified to 1'-3" (C3/A-604) like its
     sibling and the rest of the BOH non-kitchen rooms (RFI-23 recomputed).
  3. RFI-27 drive-thru furr down: plan A-202, RCP A-221 (ACT-1 C.H. 10'-2" runs to the drive-thru south wall, no soffit band) and
     sections show no furr down; C1/A-603 draws the wall flat with FRP-2 from 7'-8" to the ceiling; A-501 shows '2X FURR OUT
     EXISTING' (wood) at the sliding door head. The 7'-8" line is the FRP-2 / CT-57A datum on the wall face: no furr-down quantity;
     RFI-27 keeps the framed alternative with its delta.
Use: python3 bitacora.py run scripts/correcciones_rev9.py"""
import json, math, os, re
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(K, "etapas", "4_canon", "takeoff_canon.json")
c = json.load(open(P))
LOG = []
log = lambda *a: LOG.append(dict(zip(("item", "rev8", "rev9", "delta", "src", "rule"), a)))
E = {e["id"]: e for e in c["existing_walls"]}

# 2. W6-09-OUT-1
e = E["W6-09-OUT-1"]
if abs(float(e["height_ft"]) - 1.0) < 0.01:
    e["height_ft"] = 1.25
    e["height_source"] = ("[CONFIRMED] C3/A-604 WALL BASE DETAIL @ BACK OF HOUSE prints 1' - 3\" = 1.25 ft (called by the A-602 / A-603 "
                          "elevations of this room: 'CEMENTITIOUS BOARD RE: C3/A-604'); G.3/A-202 prints 1'-0\" -> RFI-23 (closed, precedent #15)")
    log("W6-09-OUT-1 cement board base (corridor / service faces of the office W6)", "1.0 ft (G.3/A-202)", "1.25 ft (C3/A-604, same as W6-09-OUT-2)",
        f"+{round(float(e['length_ft']) * 0.25, 2)} SF 1/2\" cement board", "C3/A-604", "RFI-23 / one source per wall")
for e in c["existing_walls"]:                      # the BOH 1'-3" rows: CONFIRMED with the sheet that prints it
    if str(e.get("height_source", "")).startswith("C3/A-604 WALL BASE DETAIL"):
        e["height_source"] = "[CONFIRMED] " + e["height_source"].replace(" vs G.3/A-202 1'-0\" -> conservative 1.25 ft + RFI-23",
                                                                         "; G.3/A-202 prints 1'-0\" -> RFI-23 (closed, precedent #15)")
R = {r["id"]: r for r in c["rfis"]}
r = R["RFI-23"]
ids = [x["id"] for x in c["existing_walls"] if "C3/A-604 WALL BASE DETAIL" in str(x.get("height_source"))]
lf = round(sum(float(E[i]["length_ft"]) for i in ids), 3)
r["question"] = re.sub(r"\(multi-purpose, service, office: \d+ wall faces, [\d.]+ LF\)", f"(multi-purpose, service, office: {len(ids)} wall faces, {lf} LF)", r["question"])
r["opciones"]["A"]["texto"] = re.sub(r"on [\d.]+ LF loaded", f"on {lf} LF loaded", r["opciones"]["A"]["texto"])
r["opciones"]["A"]["delta"] = f"0 (loaded); 1'-0\" per G.3/A-202: -{round(lf * 0.25, 2)} SF 1/2\" cement board"
r["delta"] = f"A: {r['opciones']['A']['delta']} | B: {r['opciones']['B']['delta']}"

# 1. Source height text = current height_source
n1 = 0
for e in c["existing_walls"]:
    s = str(e.get("source") or "")
    hs = str(e.get("height_source") or "")
    if " | height: " not in s or not hs:
        continue
    head, tail = s.split(" | height: ", 1)
    rest = tail.split(" | elev ", 1)
    new = head + " | height: " + hs + (" | elev " + rest[1] if len(rest) > 1 else "")
    if new != s:
        e["source"] = new
        n1 += 1
log("Board-only Source height text", "old height text kept in the Source of rows changed in rev6 / rev7 (e.g. G.3 1'-0\" [CONFIRMED] on 1.25 ft rows; 6.708 / 2.625 on the restroom rows)",
    "height part of the Source = the entry's current height_source (one source, one number)", "0", f"{n1} rows", "#0 / U-114")

# 3. RFI-27: no furr down (RCP / plan / sections), alternative with its delta
dt = E["EX-DT-01"]
L = float(dt["length_ft"])
HF = round(10 + 2 / 12 + 4 / 12 - (7 + 8 / 12), 3)
n_st = math.ceil(L * 12 / 16) + 1
n_br = math.ceil(L * 12 / 32) + 1
st = round(n_st * HF + n_st * 2.0 + n_br * math.hypot(2.0, HF), 2)
r = R["RFI-27"]
r["status"] = "open - conservative value loaded"
r["question"] = ("Drive-thru south wall (C1/A-603): '7'-8\" B.O. FURR DOWN' is printed on the elevation, but the RCP A-221 runs ACT-1 (C.H. 10'-2\") to that wall "
                 "with no soffit band, A-202 / sections show none and C1/A-603 draws the wall face flat (FRP-2 from 7'-8\" to the ceiling, CT-57A below). "
                 "Loaded per the RCP: the 7'-8\" line is the finish datum on the wall face. Is a framed furr down intended there (depth / extent)?")
r["opciones"] = {
    "A": {"texto": "Plans (RCP A-221 + A-202 + C1/A-603 wall face): the 7'-8\" line is the FRP-2 / CT-57A datum on the wall; the cement board below it is loaded "
                   "(EX-DT-01 11.011 LF to 7'-8\", standing precedent #15); above it FRP-2 on the existing wood framing (G.3/A-202 plywood, Div. 06)",
          "source": "A-221 RCP, A-202, C1/A-603, A-501 '2X FURR OUT EXISTING'",
          "delta": f"0 (as loaded); a framed furr down 11.011 LF x 2'-0\" deep (C4/A-624 typical soffit): +{round(L * (HF + 2.0), 2)} SF 1/2\" cement board, "
                   f"+{st} LF 3-5/8\" stud, +{round(3 * L, 2)} LF track, +{L} LF corner bead; per 6\" of depth +/- {round(L * 0.5, 2)} SF"},
    "B": {"texto": "Soffits / furr downs are framed where the RCP shows them", "cita": "ASTM C754 / C840", "delta": "same as A"}, "C": ""}
r["why_not_printed"] = "The RCP shows no furr down at this wall; only the elevation label is printed, without depth or extent."
r["delta"] = f"A: {r['opciones']['A']['delta']} | B: same as A"
r["barrido"]["descartes"]["A-221"] = "RCP: ACT-1 C.H. 10'-2\" runs to the drive-thru south wall, keynotes 13 / 14 at the door; no soffit band (the plan answer used)."
r["barrido"]["descartes"]["A-501"] = "'2X FURR OUT EXISTING' at the aluminum sliding door head: wood furring of the existing opening (Div. 06), not a gyp furr down."
log("RFI-27 drive-thru furr down", "loaded 11.011 LF x (2.833 + 2.0 assumed) + framing (rev8)", "not a furr down: RCP A-221 / A-202 / C1/A-603 show the 7'-8\" line as the wall finish datum",
    f"-{round(L * (HF + 2.0), 2)} SF 1/2\" cement board, -{st} LF 3-5/8\" stud, -{round(3 * L, 2)} LF track, -{L} LF corner bead (vs rev8)",
    "A-221, A-202, C1/A-603, A-501", "U-132: the plan resolves it; RFI-27 keeps the alternative")

# 4. Review Item 5 (DEMO-C6) was [PENDING] without an RFI (CE_RFI_FORMATO, U-042 / U-048): RFI-28 with the conservative value loaded
if "RFI-28" not in R:
    c["rfis"].append({"id": "RFI-28", "status": "open - conservative value loaded",
        "question": "Existing east-room gyp ceiling to demolish (A-052 KN10 'REMOVE EXISTING GYP. BD. CEILING & SUPPORT', DEMO-C6): the A-052 vectors give "
                    "two outlines (38.35 SF and 35.39 SF) and the ceiling hatch outline measures 34.57 SF; the room limit is not dimensioned. Which area?",
        "fuentes_revisadas": ["A-052", "A-050", "A-221"],
        "opciones": {"A": {"texto": "Plans: 38.35 SF loaded (largest A-052 outline, conservative)", "source": "A-052 KN10",
                           "delta": "0 (loaded); 35.39 SF reading: -2.96 SF demolition; 34.57 SF hatch outline: -3.78 SF demolition"},
                     "B": {"texto": "Demolition by the area of the existing ceiling removed", "cita": "per contract documents / ASTM C840 n/a", "delta": "same as the plans value"},
                     "C": ""},
        "source": "A-052 KN10", "img": "img/r05_A052_DEMO-C6_circled.png",
        "barrido": {"hojas": "ALL", "terminos": ["GYP. BD. CEILING", "CEILING & SUPPORT", "REMOVE EXISTING GYP"],
                    "grep": "rev9 sweep (BE-120): set_texto.json (172 pages, text layer + AutoCAD SHX) grepped for the terms.",
                    "descartes": {"A-052": "KN10 'REMOVE EXISTING GYP. BD. CEILING & SUPPORT' tags the rooms only; no dimension of the east-room ceiling (the question)."}},
        "why_not_printed": "The east-room ceiling limits are not dimensioned on A-052; only the hatch and the keynote are drawn.",
        "delta": "A: 0 (loaded); 35.39 SF: -2.96 SF; 34.57 SF: -3.78 SF | B: same"})
    log("Review Item 5 DEMO-C6 (PENDING without RFI)", "Review Item only", "RFI-28 open, 38.35 SF loaded (conservative)", "0", "A-052 KN10", "U-042 / U-048 (CE_RFI_FORMATO)")
    log("Review Item 6 mop chase cement board height", "[PENDING]", "RESOLVED from drawings (E3/A-604 + A-601 / A-602 S-1 to the ceiling, G.7/A-202)", "0", "E3/A-604", "U-132")

json.dump(c, open(P, "w"), ensure_ascii=False, indent=1)
json.dump(LOG, open(os.path.join(K, "etapas", "4_canon", "rev9_log.json"), "w"), ensure_ascii=False, indent=1)
print(f"rev9 corrections: {len(LOG)} log lines")
