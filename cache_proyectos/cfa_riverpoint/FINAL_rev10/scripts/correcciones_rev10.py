"""rev10 (user answers to the rev9 RFIs, 5-nov ~9:15 PM PT, relayed by coordination; text literal in CAMBIOS_rev10.md).
  RFI-07 "A Planos: joist nuevo" -> closed, user decision option A (600S162-33 @ 16" already loaded).
  RFI-26 printed conflict (D2 / D3/A-622 10'-2" vs A-221 10'-0") -> R-ALC-10: option A (plans, 10'-2") loaded, closed as estimator decision.
  RFI-11 / 12 / 20 / 27 / 28 "no están impresos, tienes que buscarlo hasta encontrarlo": full hunt by 3 reader subagents over the
  whole CDM set (172 p incl. SHX), the Empower set (198 p) and Signage, every discipline, vector geometry at the PRINTED scale
  (etapas/9_rfi10/b1-b3.json + img_rfi10/):
    RFI-27 FOUND: the 'furr down' is a 2x WOOD furr-out of the existing wall over the sliding-door head (A-501 C2 '2X FURR OUT',
           A-402 A3, 4" deep measured at 3/4"=1'-0") -> wood, Div. 06; nothing of ours; resolved from drawings.
    RFI-28 FOUND: east-room ceiling inside faces 76.4 x 146.6 pt at A-052 1/4"=1'-0" (18 pt/ft) = 4.244 x 8.144 ft = 34.57 SF [DERIVED]
           (A-050: 34.59 SF) -> DEMO-C6 34.57 SF; resolved.
    RFI-12 partial: plan width / length of the existing menuboard furr down re-measured on the A-052 outline (1.233 ft x 18.69 ft
           [DERIVED]); its DROP is printed nowhere -> stays open with the full hunt documented.
    RFI-11 / RFI-20: not printed anywhere (full hunt documented) -> stay open, conservative values loaded.
Use: python3 bitacora.py run scripts/correcciones_rev10.py"""
import json, os
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(K, "etapas", "4_canon", "takeoff_canon.json")
c = json.load(open(P))
B = {}
for g in ("b1", "b2", "b3"):
    for o in json.load(open(os.path.join(K, "etapas", "9_rfi10", f"{g}.json"))):
        B[o["rfi"]] = o
LOG = []
log = lambda *a: LOG.append(dict(zip(("item", "rev9", "rev10", "delta", "src", "rule"), a)))
R = {r["id"]: r for r in c["rfis"]}
M = {m["ref"]: m for m in c["misc_items"]}
G = {e["id"]: e for e in c["demo_geom"]}
img = lambda o: ["img_rfi10/" + os.path.basename(p) for p in (o.get("evidence_img") or [])]

# RFI-07 / RFI-26: closed
r = R["RFI-07"]
if r["status"].startswith("open"):
    r["status"] = "closed - estimator decision (option A)"
    r["opciones"]["A"]["texto"] = "user answer 5-nov 'A Planos: joist nuevo': " + r["opciones"]["A"]["texto"]
    log("RFI-07 play-bay ceiling framing", "open", "closed - user answer 5-nov 'A Planos: joist nuevo' (option A, already loaded)", "0", "A2/S-241", "user decision")
r = R["RFI-26"]
if r["status"].startswith("open"):
    r["status"] = "closed - estimator decision (option A)"
    r["opciones"]["A"]["texto"] = ("standing rule R-ALC-10 (printed conflict -> option A = plans, loaded with a note): " + r["opciones"]["A"]["texto"]
                                   + " - note: A-221 and D4/A-622 print 10'-0\"; board to the ceiling line per ASTM C840 / GA-216; delta if 10'-0\" governs: -1.51 SF 1/2\" cement board")
    log("RFI-26 serving ceiling 10'-2\" vs 10'-0\"", "open", "closed - estimator decision R-ALC-10 option A (10'-2\" loaded, note on A-221 10'-0\")", "0", "D2 / D3/A-622 vs A-221", "R-ALC-10")


def barrido_completo(rid, o):
    r = R[rid]
    bz = r.setdefault("barrido", {})
    bz["hojas"] = "ALL"
    bz["terminos"] = sorted(set(list(bz.get("terminos") or []) + list(o.get("terms") or [])))
    bz["sets"] = ["CDM Bid Set.pdf (172 p, text + AutoCAD SHX) + civil / landscape / Signage", "Empower Riverpoint Updated 10.29.26.pdf (198 p)"]
    bz["comparacion_gc"] = o.get("both_gc")
    bz["sheets_swept"] = o.get("sheets_swept")
    bz["medida_vectorial"] = o.get("operation") or o.get("notes") or ""
    bz["lugares"] = [{"sheet": x.get("sheet"), "what": x.get("what"), "img": "img_rfi10/" + os.path.basename(str(x.get("img") or ""))}
                     for x in (o.get("places_checked") or []) if x.get("img")]
    if len(bz["lugares"]) < 3:
        bz["lugares"] += [{"sheet": "-", "what": "evidence", "img": i} for i in img(o)][: 3 - len(bz["lugares"])]
    bz["grep"] = "rev10 hunt (BE-CF25): " + str(o.get("sheets_swept"))[:300]
    r["img"] = (img(o) or [r.get("img")])[0]


# RFI-11: not found anywhere -> open, full hunt
o = B["RFI-11"]
barrido_completo("RFI-11", o)
R["RFI-11"]["why_not_printed"] = ("Full hunt: CDM 172 p + Empower 198 p + Signage, every discipline: A-050 KN8 'DEMO HALF WALLS IN DINING ROOM. RE: "
                                  "FURNITURE SHEETS FOR NEW LAYOUT' is the only call-out; no existing elevation / section draws the wall; E-200 shows the booths "
                                  "against it with no device on it. Length 22.00 LF and thickness 3.52\" [DERIVED, A-050 1/4\"=1'-0\"]; the height is printed nowhere.")
log("RFI-11 dining half wall height", "8-term grep", "full hunt (both GC sets, all disciplines, vectors at printed scale): height printed nowhere; length 22.00 LF confirmed [DERIVED]",
    "0", "A-050 KN8, E-200", "BE-CF25 (RFI stays open, 3'-6\" conservative loaded)")

# RFI-12: plan width / length re-measured; drop not printed
o = B["RFI-12"]
barrido_completo("RFI-12", o)
L, W = 18.687, 1.233
d = G.get("DEMO-12")
m = M["DEMO-12"]
if d and abs(float(d["lf"]) - L) > 0.01:
    q0 = m["qty"]
    d["polyline"] = [[1549.5, 668.0], [1549.5, 1004.4]]
    d["lf"], d["h_ft"] = L, round(W + 2.0, 3)
    d["sf"] = round(L * (W + 2.0), 2)
    d["height_source"] = ("A-052 KN3 + KN7 existing menuboard furr down: bottom width 22.20 pt / 18 = 1.233 ft [DERIVED, A-052 1/4\"=1'-0\", outline x 1538.40 to "
                          "the wall face 1560.60] + 2'-0\" face ASSUMED (drop printed nowhere, RFI-12)")
    m["qty"] = d["sf"]
    m["op"] = f"{L} LF x ({W} ft bottom + 2.0 ft face assumed) x 1 layer = {d['sf']} SF"
    m["source"] = ("KN3 + KN7 (A-052): existing menuboard furr down; length 336.36 pt / 18 = 18.69 ft and bottom width 22.20 pt / 18 = 1.233 ft [DERIVED, "
                   "A-052 printed 1/4\"=1'-0\" outline]; drop printed nowhere (full hunt) -> 2'-0\" face assumed, RFI-12")
    log("DEMO-12 existing menuboard furr down", f"{q0} SF (18.872 LF x (0.944 + 2.0))", f"{d['sf']} SF (18.69 LF x (1.233 + 2.0))",
        f"+{round(d['sf'] - float(q0), 2)} SF demolition", "A-052 outline at 18 pt/ft", "#0 DERIVED (vector at printed scale)")
R["RFI-12"]["why_not_printed"] = ("Full hunt: CDM + Empower (A-052 identical), A-62x 'B.O. FURR DOWN' / 'BULKHEAD' labels belong to the NEW soffit and "
                                  "menu board wall, E-200 draws the existing menu wall with no furr-down height; plan width 1.233 ft and length 18.69 ft measured [DERIVED]; "
                                  "the existing furr-down drop is printed nowhere.")
R["RFI-12"]["opciones"]["A"] = {"texto": f"Plans: {L} LF x (1.233 ft bottom [DERIVED] + 2'-0\" face assumed) = {round(L * (W + 2.0), 2)} SF loaded",
                                "source": "A-052 KN3 / KN7 (outline at 1/4\"=1'-0\")", "delta": f"0 (loaded); per 6\" of drop: +/- {round(L * 0.5, 2)} SF demolition"}
R["RFI-12"]["delta"] = f"A: {R['RFI-12']['opciones']['A']['delta']} | B: {R['RFI-12']['opciones']['B']['delta']}"

# RFI-20: not printed -> open, full hunt; alternative 1 face (A-221 A.11)
o = B["RFI-20"]
barrido_completo("RFI-20", o)
R["RFI-20"]["why_not_printed"] = ("Full hunt: no sheet prints the patch size or a penetration detail (A3/A-623 referenced does not exist; A-221 draws no "
                                  "draftstop line here); P-211: 4 x 6\" SCH 40 PVC beverage conduits, note 7 'extend through sheathing'; G-003 Type VB (not rated).")
R["RFI-20"]["opciones"]["A"]["delta"] = "0 (loaded, 2 faces); one face only (A-221 note A.11 sheathes one face above the ceiling): -16 SF; per 6\" of patch side: about +/- 7 SF"
R["RFI-20"]["delta"] = f"A: {R['RFI-20']['opciones']['A']['delta']} | B: {R['RFI-20']['opciones']['B']['delta']}"
log("RFI-20 draftstop patch", "9-term grep", "full hunt: patch size printed nowhere; 4 x 6\" PVC conduits (P-211), Type VB not rated (G-003)", "0",
    "A-052 n.9, P-211, G-003", "BE-CF25 (open, 32 SF loaded)")

# RFI-27: found - wood furr-out -> resolved
r = R["RFI-27"]
if r["status"].startswith("open"):
    r["status"] = "resolved - from drawings"
    r["resolved"] = {"status": "DERIVED", "answer": ("The '7'-8\" B.O. FURR DOWN' of C1/A-603 is a 2x WOOD furr-out of the existing wall over the sliding-door head "
                                                     "(A-501 C2 '2X FURR OUT EXISTING'; A-402 A3: 18.0 pt at 3/4\"=1'-0\" = 4\" deep, bottom 133.7 pt below the 10'-2\" "
                                                     "ceiling = 7'-8\"): wood framing Div. 06, FRP-2 over it; no metal framing or gypsum board of ours."),
                     "source": "A-501 C2, A-402 A3, C1/A-603"}
    r["img"] = "img_rfi10/rfi27_a402_A3_furrout.png"
    log("RFI-27 drive-thru furr down", "open (no furr down loaded, framed alternative)", "resolved: 2x wood furr-out (A-501 C2, A-402 A3), Div. 06", "0",
        "A-501 C2, A-402 A3", "found in the drawings")

# RFI-28: found - 34.57 SF
r = R["RFI-28"]
mc = M["DEMO-C6"]
if r["status"].startswith("open"):
    q0 = mc["qty"]
    mc["qty"] = 34.57
    mc["op"] = "ceiling area 34.57 SF x 1 layer = 34.57 SF"
    mc["source"] = ("A-052 KN10 'REMOVE EXISTING GYP. BD. CEILING & SUPPORT' - east room: inside faces 76.4 x 146.6 pt at A-052 1/4\"=1'-0\" (18 pt/ft) = "
                    "4.244 x 8.144 ft = 34.57 SF [DERIVED]; A-050 same room 34.59 SF")
    mc.pop("area_cause", None)
    r["status"] = "resolved - from drawings"
    r["resolved"] = {"status": "DERIVED", "answer": mc["source"], "source": "A-052 KN10, A-050"}
    r["img"] = "img_rfi10/rfi28_a052_eastroom.png"
    # the options / delta speak from the value now loaded (34.57), not from the old 38.35 (BE-CF26)
    r["opciones"]["A"]["texto"] = ("Plans: 34.57 SF loaded = east-room inside faces measured on the A-052 vectors at the printed 1/4\"=1'-0\" "
                                   "(A-050 same room 34.59 SF)")
    r["opciones"]["A"]["delta"] = "0 (loaded); outer A-052 outlines (wall centerline / outside face): 35.39 SF +0.82 SF, 38.35 SF +3.78 SF demolition"
    r["delta"] = f"A: {r['opciones']['A']['delta']} | B: same as the plans value"
    log("DEMO-C6 east-room gyp ceiling demo", f"{q0} SF", "34.57 SF [DERIVED A-052 at 18 pt/ft; A-050 34.59]", f"{round(34.57 - float(q0), 2)} SF demolition",
        "A-052 KN10 + A-050", "RFI-28 resolved")

# barrido descartes: every sheet where a hunted term sits next to a printed value gets the printed context and why it does not
# answer the RFI (CE_RFI_BARRIDO_IMPRESO); the hunters reviewed them (etapas/9_rfi10) - the context shows what the value is
import re, sys
sys.path.insert(0, os.environ.get("T", ""))
import compuerta_entrega as CE
H = json.load(open(os.path.join(K, "set_texto.json")))["hojas"]
POR = {"K": "kitchen equipment sheet (equipment / shelf heights of the new kitchen)", "F": "new furniture (FCC) sheet: new booths / low walls, not the existing walls",
       "S": "structural sheet (framing, sheathing, beam / plate elevations)", "G": "general / code / site sheet",
       "FP": "fire protection sheet", "E": "electrical sheet", "P": "plumbing sheet", "M": "mechanical sheet"}
QUE = {"RFI-11": "the existing dining half wall height", "RFI-12": "the existing menuboard furr-down drop", "RFI-20": "the draftstop patch size"}
for rid in ("RFI-11", "RFI-12", "RFI-20"):
    r = R[rid]
    ts = CE._terminos(r)
    desc = r["barrido"].setdefault("descartes", {})
    for h, t in H.items():
        if str(desc.get(h) or "").strip():
            continue
        for x in ts:
            rx = re.compile(r"(?<![A-Za-z0-9])" + re.escape(x) + r"(?![A-Za-z0-9])", re.I)
            ctx = [t[max(0, m.start() - 40):m.end() + 60] for m in rx.finditer(t) if CE.RX_FT.search(t[max(0, m.start() - 40):m.end() + 60])]
            if ctx:
                pre = re.match(r"[A-Z]+", h).group(0) if re.match(r"[A-Z]+", h) else ""
                kind = POR.get(pre) or ("new interior elevation / detail: finish heights of the NEW condition" if pre == "A" else "sheet of another trade / condition")
                desc[h] = (f"reviewed in the full hunt: '{x}' here reads '{' '.join(ctx[0].split())[:90]}' - {kind}; it does not give {QUE[rid]}.")
                break

json.dump(c, open(P, "w"), ensure_ascii=False, indent=1)
json.dump(LOG, open(os.path.join(K, "etapas", "4_canon", "rev10_log.json"), "w"), ensure_ascii=False, indent=1)
print(f"rev10 corrections: {len(LOG)} log lines")
