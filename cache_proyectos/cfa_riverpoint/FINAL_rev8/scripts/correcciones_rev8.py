"""rev8 (coordination 4-nov, U-048 / U-116): RFI-27 said 'nothing loaded'. The drive-thru furr down is printed (C1/A-603
'7'-8" B.O. FURR DOWN', FRP-2 on its face, CEILING 10'-2"); only its depth is not printed. It is loaded with the conservative
assumption + RFI-27 with the delta of each alternative. Every quantity recomputed by canon.py / accesorios.py / plantilla_excel.py.
  Run = the drive-thru south wall EX-DT-01, 11.011 LF (A-202 vector, same path).
  Face: B.O. 7'-8" [CONFIRMED C1/A-603] to CEILING 10'-2" [CONFIRMED C1/A-603] + 4" (G.4/A-202: cement board to 4" above the
        ceiling behind FRP on metal studs) = 2.833 ft of 1/2" cement board (FRP-2 face, G.4/A-202).
  Bottom: depth NOT printed -> 2'-0" assumed [PENDING RFI-27], 1/2" cement board (same finish as the face, conservative).
  Framing as the typical soffit C4/A-624 (3-5/8" metal studs @ 16" O.C., cross brace @ 32" O.C.): face studs + bottom joists +
        braces, 3 runs of 3-5/8" track (face top, face bottom / corner, bottom at the wall); corner bead at the outside corner.
Use: python3 bitacora.py run scripts/correcciones_rev8.py"""
import json, math, os
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(K, "etapas", "4_canon", "takeoff_canon.json")
c = json.load(open(P))
LOG = []
log = lambda *a: LOG.append(dict(zip(("item", "rev7", "rev8", "delta", "src", "rule"), a)))
E = {e["id"]: e for e in c["existing_walls"]}
dt = E["EX-DT-01"]
L = float(dt["length_ft"])
HF = round(10 + 2 / 12 + 4 / 12 - (7 + 8 / 12), 3)      # 2.833
D = 2.0                                                   # assumed depth (RFI-27)
OC = 16
n_st = math.ceil(L * 12 / OC) + 1
n_br = math.ceil(L * 12 / 32) + 1
br = round(math.hypot(D, HF), 3)
f3 = lambda x: round(float(x), 3)
SRC = ("C1/A-603 DRIVE-THRU ELEVATION '7'-8\" B.O. FURR DOWN', FRP-2 above, CEILING 10'-2\"; framing as the typical soffit C4/A-624 "
       "(3-5/8\" metal studs @ 16\" O.C., cross brace @ 32\" O.C.); depth not printed -> 2'-0\" assumed (RFI-27)")
if "FD-DT-FACE-CB" not in E:
    for i, h, hs, loc in (
        ("FD-DT-FACE-CB", HF, f"[DERIVED] CEILING 10'-2\" (C1/A-603) + 4\" (G.4/A-202 cement board to 4\" above the ceiling behind FRP) - B.O. FURR DOWN 7'-8\" (C1/A-603) = {HF} ft",
         "Drive thru - furr down face over the sliding door (FRP-2)"),
        ("FD-DT-BOT-CB", D, "[PENDING] furr down depth not printed (C1/A-603 prints only B.O. 7'-8\"): 2'-0\" assumed, RFI-27",
         "Drive thru - furr down bottom (horizontal, B.O. 7'-8\")")):
        c["existing_walls"].append({
            "id": i, "sheet": "A-202", "page": "13", "keynote": "C1/A-603", "path": dt["path"], "length_ft": L,
            "length_op": f"[DERIVED] same run as EX-DT-01: {dt['length_op']}", "height_ft": h, "height_source": hs,
            "faces": 1, "layers": 1, "board": "1/2 cement board", "location": loc,
            "source": SRC + "; FRP-2/A-211 on metal framing -> G.4/A-202 1/2\" cement board; C09250 2.2.B / A-909",
            "decision": "Scope rule R-ALC-01 (user 2026-11-01): gypsum / cement board is our scope; conservative value loaded + RFI-27 (U-048)"})
    st = round(n_st * HF + n_st * D + n_br * br, 2)
    c["misc_items"] += [
        {"ref": "FD-DT-STUDS", "familia": '3-5/8" stud (todos los gauges)', "qty": st, "unit": "LF", "pcs": 2 * n_st + n_br,
         "source": SRC, "op": f"face studs ROUNDUP({L} x 12 / 16) + 1 = {n_st} x {HF} ft + bottom joists {n_st} x {D} ft (assumed depth) + "
                             f"cross braces ROUNDUP({L} x 12 / 32) + 1 = {n_br} x sqrt({D}^2 + {HF}^2) = {br} ft = {st} LF",
         "product": {"value": "362S125-33 furr down framing (as C4/A-624 typical soffit)", "source": "C4/A-624"}, "img": "img_rev8/C1_A-603.png"},
        {"ref": "FD-DT-TRACK", "familia": "track de ceilings / soffits", "qty": round(3 * L, 2), "unit": "LF", "source": SRC,
         "op": f"3 runs (face top at the ceiling, face bottom / corner, bottom at the wall) x {L} LF = {round(3 * L, 2)} LF",
         "product": {"value": "362T125-33 track (as C4/A-624)", "source": "C4/A-624"}, "img": "img_rev8/C1_A-603.png"}]
    c["trim_items"].append({"ref": "CB-FD-DT", "kind": "corner_bead", "lf": L,
                            "source": "C4/A-624 'PROVIDE CORNER BEADS AT ALL GYPSUM BOARD INTERSECTIONS' (typical soffit) at the outside corner of the C1/A-603 furr down",
                            "product": {"value": "corner bead at the furr down outside corner (C4/A-624)", "source": "C4/A-624"}, "img": "img_rev8/C1_A-603.png"})
    log("Drive-thru furr down (C1/A-603)", "not loaded (RFI-27)",
        f"face {L} x {HF} + bottom {L} x {D} (assumed) 1/2\" cement board; {st} LF 3-5/8\" studs; {round(3 * L, 2)} LF track; {L} LF corner bead",
        f"+{round(L * (HF + D), 2)} SF 1/2\" cement board, +{st} LF 3-5/8\" stud, +{round(3 * L, 2)} LF track, +{L} LF corner bead",
        "C1/A-603 + C4/A-624 + G.4/A-202", "U-048 / U-116: conservative value loaded + RFI")
R = {r["id"]: r for r in c["rfis"]}
r = R["RFI-27"]
r["status"] = "open - conservative value loaded"
r["question"] = ("Drive-thru south wall (C1/A-603): '7'-8\" B.O. FURR DOWN' with FRP-2 above, CEILING 10'-2\"; A-221 shows no soffit there and no "
                 "sheet prints the furr down depth. Loaded: furr down 11.011 LF, 2'-0\" deep (assumed), framed as the typical soffit C4/A-624. Confirm the depth.")
dsf = round(L * 0.5, 2)
r["opciones"] = {
    "A": {"texto": f"Plans: furr down {L} LF x (face {HF} ft + bottom 2'-0\" assumed) 1/2\" cement board, 3-5/8\" studs @ 16\" + braces @ 32\" (C4/A-624), "
                   f"3 track runs, corner bead (loaded, conservative); the board is decided by G.4/A-202 + standing precedent #15 (cement board behind the FRP finish) - only the depth is asked", "source": "C1/A-603 + C4/A-624 + G.4/A-202",
          "delta": f"0 (loaded); per 6\" of depth: +/- {dsf} SF 1/2\" cement board and +/- {round(n_st * 0.5, 2)} LF stud; no furr down (7'-8\" only a datum): "
                   f"-{round(L * (HF + D), 2)} SF cement board, -{round(n_st * HF + n_st * D + n_br * br, 2)} LF stud, -{round(3 * L, 2)} LF track, -{L} LF corner bead"},
    "B": {"texto": "Furr-down framing and board per ASTM C754 / C840 with the depth on the drawings", "cita": "ASTM C754 / C840", "delta": "same as A"},
    "C": ""}
r["why_not_printed"] = "Only the bottom elevation of the furr down (7'-8\") and the ceiling (10'-2\") are printed; its depth is printed nowhere."
r["delta"] = f"A: {r['opciones']['A']['delta']} | B: same as A"
json.dump(c, open(P, "w"), ensure_ascii=False, indent=1)
json.dump(LOG, open(os.path.join(K, "etapas", "4_canon", "rev8_log.json"), "w"), ensure_ascii=False, indent=1)
print(f"rev8 corrections: {len(LOG)} log lines")
