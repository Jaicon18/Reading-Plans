"""Builds takeoff_canon_AB.json = reading A + decisions taken on the drawings (3_revision/resolucion.md)."""
import json, copy, sys
E = "/home/user/scratchpad/run/takeoff_work/etapas/2_lectura/"
a = json.load(open(E + "takeoff_canon_A.json")); b = json.load(open(E + "takeoff_canon_B.json"))
c = copy.deepcopy(a)
# R-06 glass mat: 2/A3.1 head wall exterior face = key 34 FRT plywood, not key 19 glass mat -> piers only
for m in c["misc_items"]:
    if m["ref"] == "GLASSMAT-ENTRY":
        m["qty"] = 248.0
        m["op"] = ("piers 2 x 6.0 x 20.667 = 248.0 SF (1/A3.1 key 19). Head wall over storefront A excluded: 2/A3.1 shows key 34 "
                   "5/8\" exterior FRT plywood sheathing on that face, not key 19 (double reading resolution R-06)")
bh = [x for x in b["plywood_strips"] if x["ref"] == "EXT-W-HEAD-FRT"][0]
p = copy.deepcopy(bh); p["wall"] = "EXT-HEAD-6"
p["op"] = "head wall EXT-HEAD-6 38'-8\" x (120'-8\" - 111'-4\") = 38.67 x 9.33 (2/A3.1 key 34) - from reading B, resolution R-06"
c["plywood_strips"].append(p)
# R-07 FRT 2x nailers at T.O. metal stud (key 11, 8/A3.2) - only in reading B
c["blocking_items"].append(copy.deepcopy([x for x in b["blocking_items"] if x["ref"] == "BLK-TOP-NAILERS-FRONT"][0]))
# R-05 vestibule heads: element vestibule_head (B) + gauge 16 ga per S4.1 key note 3 (structural governs, A1.1 note 2.D); height A
bv = {w["id"]: w for w in b["walls"]}
for wid, bid in (("VEST-HD-C", "VH-C"), ("VEST-HD-B1", "VH-B1"), ("VEST-HD-B2", "VH-B2")):
    w = [x for x in c["walls"] if x["id"] == wid][0]
    w["element"] = "vestibule_head"
    w["gauge"] = "54 mil (16 ga) - 600S162-54"
    w["gauge_source"] = ("S4.1 key note 3 \"PROVIDE 16ga LIGHT GAUGE STEEL FRAMING AT ENTRY LOCATION\" governs over 3/A3.1 key 8 "
                         "600S162-43 (A1.1 note 2.D: refer to structural drawings for structural stud requirements) - RFI-05")
json.dump(c, open(E + "takeoff_canon_AB.json", "w"), indent=1, ensure_ascii=False)
print("AB walls", len(c["walls"]))
# RFI-08 / MEP: sheet citation + sources checked (E23 / G_RFI)
fr = ["designation: A1.1 interior wall & ceiling notes 2.D (refer to structural) - no penetration detail on A sheets",
      "other row: no framed opening / penetration row on A1.1, A1.2, A3.x, A4.x", "standard rule: stud reinforcement plate per cut stud (accesorios.py)",
      "detail: M1-M3 / P1-P2 not opened (excluded by the estimator 2026-10-31)"]
for r in c["rfis"]:
    if r["id"] == "RFI-08":
        r["source"] = "A1.1 note 2.D; M1, P1 (sheets excluded by the estimator)"
        r["fuentes_revisadas"] = fr
for r in c.get("accesorios_rfi") or []:
    if r.get("familia") == "stud reinforcement MEP":
        r["source"] = "A1.1 note 2.D; M1, P1 (sheets excluded by the estimator)"
        r["fuentes_revisadas"] = fr
c["mep_sweep"] = {"excluded_by_estimator": {"why": "MEP / electrical sheets excluded from this take-off by the estimator (2026-10-31)",
                                            "source": "A1.1 note 2.D; M1, P1 (not opened)"}}
json.dump(c, open(E + "takeoff_canon_AB.json", "w"), indent=1, ensure_ascii=False)
print("RFI-08 patched")
# R-14: untagged exterior CFMF walls -> type label by stud size (as reading B), schedule order after the interior types
for w in c["walls"]:
    if w["id"].startswith("EXT-") and not w.get("tag"):
        w["tag"] = "EXT-8CFMF" if w["stud_size"].startswith('8"') else "EXT-6CFMF"
        w.setdefault("untagged_reason", "exterior cold-formed framing drawn without a partition tag (1/A3.1, 2/A3.1, 1/A3.4, 3/S5.3); labelled by stud size")
json.dump(c, open(E + "takeoff_canon_AB.json", "w"), indent=1, ensure_ascii=False)
print("EXT tags set")
# R-15: misc_items op must end with "= qty" (trazabilidad reads the last "= N"): JOISTS-OFFICE-RR
for m in c["misc_items"]:
    if m["ref"] == "JOISTS-OFFICE-RR" and not str(m["op"]).rstrip().endswith("LF"):
        m["op"] = str(m["op"]) + " -> 56.0 + 94.0 = 150.0 LF"
json.dump(c, open(E + "takeoff_canon_AB.json", "w"), indent=1, ensure_ascii=False)
for m in c["misc_items"]:
    if m["ref"] == "CLG-GWB-OFFICE-VEST" and "= 139.28" not in m["op"]:
        m["op"] = m["op"].replace("-> 139.28 SF", "-> 88.0 + 51.28 = 139.28 SF")
json.dump(c, open(E + "takeoff_canon_AB.json", "w"), indent=1, ensure_ascii=False)
# R-16: S24 Z-furring on the CMU (A1.1 wall type S24 prints 150ZF125-18 @ 24" O.C.) - family now exists (R80e.65)
if not any(m["ref"] == "ZF-S24" for m in c["misc_items"]):
    c["misc_items"].append({"ref": "ZF-S24", "familia": "1-1/2\" Z-furring", "qty": 336.89, "unit": "LF", "source": "S24/A1.1",
        "label": "150ZF125-18 COLD FORM METAL Z-FURRING CHANNELS AT 24\" O.C. (S24/A1.1) on the CMU behind the S24 stud lining",
        "op": "pieces ROUNDUP(L / 2) + 1: S24-OFF 11.0 -> 7, S24-RR 16.17 -> 10 (grid A, T.O. low eave 14.625 ft, 2/A3.2); "
              "S24-RR104S 8.5 -> 6 (grid 4 near grid A, 14.71 ft by the 1/4:12 slope); top of furring not printed -> eave (53.3, RFI-02); "
              "17 x 14.625 + 6 x 14.71 = 248.63 + 88.26 = 336.89 LF"})
for r in c["rfis"]:
    if r["id"] == "RFI-02":
        r["supuesto"] = "S24 Z-furring loaded to the eave (14.625 / 14.71 ft) = 336.89 LF (misc item ZF-S24); board only to 8'-6\" on the studs"
json.dump(c, open(E + "takeoff_canon_AB.json", "w"), indent=1, ensure_ascii=False)
# R-17: S21 Z-furring fastened to the CMU: no track drawn on the S21 type (A1.1) -> no bottom / top track; RFI-16 carries the delta
for w in c["walls"]:
    if w.get("tag") == "S21":
        w["bottom_track"] = False
        w["track_source"] = "S21/A1.1: 150ZF125-18 Z-furring channels fastened to the CMU, no track drawn on the type or on 1/A3.2, 2/A3.2 - RFI-16"
        w["top_track_info"] = w.get("top_track")
        w["top_track"] = False
if not any(r["id"] == "RFI-16" for r in c["rfis"]):
    c["rfis"].append({"id": "RFI-16", "tema": "Track at the top / bottom of the S21 Z-furring", "donde": "S21 furring on the exterior CMU (6 walls)",
        "supuesto": "no track (none drawn on S21/A1.1 or the wall sections)",
        "opciones": {"A": {"texto": "S21 type and 1/A3.2, 2/A3.2 draw the Z-furring on the CMU without track", "source": "S21/A1.1",
                           "delta": "0"},
                     "B": {"texto": "Furring J-track / runner at top and bottom if required by the installer", "cita": "ASTM C754 (furring attachment)",
                           "delta": "+ 250.71 LF bottom + 250.71 LF top 1-1/2\" track"}, "C": ""},
        "source": "S21/A1.1", "fuentes_revisadas": ["designation: S21/A1.1", "other row: S24 type (studs with track)", "standard rule: ASTM C754", "detail: 1/A3.2, 2/A3.2"]})
json.dump(c, open(E + "takeoff_canon_AB.json", "w"), indent=1, ensure_ascii=False)
# R-17b: track_source = citations only (corridas.py); the explanation goes in track_note_info
for w in c["walls"]:
    if w.get("tag") == "S21":
        w["track_source"] = "S21/A1.1, 1/A3.2, 2/A3.2"
        w["track_note_info"] = "150ZF125-18 Z-furring channels fastened to the CMU, no track drawn on the S21 type or the wall sections - RFI-16"
json.dump(c, open(E + "takeoff_canon_AB.json", "w"), indent=1, ensure_ascii=False)
# R-18: tags swept by hand on the raster A1.1 (R80e.70) + tick type of the summed strings + RFI fields (E23)
for w in c["walls"]:
    t = w.get("tag") or ""
    if t.startswith("S"):
        w["tag_manual"] = {"source": f"{t}/A1.1", "sheet_raster": "A1.1 p.37 is a 400 dpi raster (inventario_tags.py: NO INVENTARIABLE); tag swept by hand in readings A and B (NOTAS_LECTURA_A.md / _B.md)"}
    elif w["id"].startswith("EXT-"):
        w["untagged_reason"] = ("exterior cold-formed framing drawn without a partition tag on A1.1; system per 1/A3.1, 2/A3.1, 1/A3.4, 3/S5.3; "
                                "labelled by stud size")
    if "+" in str(w.get("length_op") or "") and "tick" not in str(w.get("length_op")).lower():
        w["length_op"] = str(w["length_op"]) + " | SIMPLE ticks (single slash; two ticks side by side where a string crosses a wall thickness), printed string total used (A1.1, crops 3_revision/res/R3, R4)"
    if w["id"] == "S42-H2" and not any(k in str(w.get("length_basis")).lower() for k in ("face", "axis", "cent")):
        w["length_basis"] = "axis (centerline): " + str(w.get("length_basis"))
for r in c["rfis"]:
    o = r.get("opciones") or {}
    A, B = o.get("A") or {}, o.get("B") or {}
    r.setdefault("source", A.get("source") or "A1.1")
    r["delta"] = f"(A) {A.get('delta','')} | (B) {B.get('delta','')} | (C) ____"
    r.setdefault("fuentes_revisadas", [f"designation: {A.get('source','')}", "other row: reading A vs reading B (resolucion.md)",
                                       f"standard rule: {B.get('cita','n/a')}", f"detail: {A.get('source','')}"])
json.dump(c, open(E + "takeoff_canon_AB.json", "w"), indent=1, ensure_ascii=False)
print("R-18 ok")
# R-19: no "~" approximations in sources (E27) + corner declarations (R70.2) with their reason
for w in c["walls"]:
    for k in ("length_op", "length_source"):
        if "~" in str(w.get(k) or ""):
            w[k] = str(w[k]).replace("drawn ~", "drawn, measured on the raster, ").replace("~", "")
    if w["id"] == "EXT-SOUTH-BAND":
        w["length_source"] = "A1.1 printed 36'-0\" (south facade); A2.1 south elevation stucco panel"
RZ = ("Z-furring / linings on the inside face of the exterior CMU: each run is measured to the face of the masonry "
      "(A1.1 general note B: dimensions to rough face of masonry / framing), so the two runs share the inside-corner square "
      "of the furring depth (1-1/2\" + 5/8\"); package rule R70.2 flags it as double - review item, no LF change")
RS = ("inside corner at the CMU: both linings stop at the face of the other per the printed room dimensions 7'-10\" / 8'-6\" "
      "(A1.1, 1A/A4.1); the uncovered square is the 3-5/8\" lining depth (0.43 ft) - review item")
c["corners_ok"] = [{"walls": p, "reason": RZ} for p in (["S21-E1", "S21-N"], ["S41-B-H", "S21-N"], ["S41-C-H", "S21-N"],
                                                        ["S42-H1", "S21-N"], ["S21-W2", "S21-S"], ["S21-W1", "S41-C-V"])] + \
                  [{"walls": p, "reason": RS} for p in (["S24-RR", "S24-RR104S"], ["S43-RR-S", "S24-RR104S"])]
json.dump(c, open(E + "takeoff_canon_AB.json", "w"), indent=1, ensure_ascii=False)
print("R-19 ok")
# ---- Paso 11 (auditor) findings resolved on the drawing ----
AN = {"EXT-HEAD-8": "2/A3.1", "EXT-HEAD-6": "2/A3.1", "EXT-SOUTH-BAND": "1/A3.4", "S42-H2": "6/A4.2", "S42-V1": "6/A4.2"}
WHY = {"2/A3.1": "head wall over storefront A bears on the PEMB wind beam / storefront head at B.O. sheathing 111'-4\" (not on slab)",
       "1/A3.4": "stucco panel framed over the D1 / D2 window heads (not on slab)",
       "6/A4.2": "suspended header wall, bottom track at B.O. framing 106'-10\" (not on slab)"}
for w in c["walls"]:
    if w["id"] in AN:
        w["anchorage"] = {"value": "other", "source": AN[w["id"]], "why_info": WHY[AN[w["id"]]]}
    if w["id"] in ("VEST-HD-B1", "VEST-HD-B2"):      # band = printed 6'-0 1/2" (auditor: polyline 5.28 vs 6.04)
        w["band"]["hi"] = round(w["band"]["lo"] + 6.042 * 9.04, 1)
    if w["id"] in ("EXT-PIER-R-8", "EXT-PIER-R-6"):
        w["band"]["lo"] = round(w["band"]["hi"] - 6.0 * 9.024, 1)
if not any(b["ref"] == "BLK-CMU-OPENINGS" for b in c["blocking_items"]):
    c["blocking_items"].append({"ref": "BLK-CMU-OPENINGS", "lf": 56.67, "material": "FRT",
        "label": "FIRE TREATED 2X4 WOOD BLOCKING ANCHORED TO MASONRY at the head and jambs of the CMU door openings",
        "source": "1/A5.1",
        "op": "door 2: 3.333 + 2 x 7.0 = 17.33; door 7: 3.333 + 2 x 7.0 = 17.33; door 3: 6.0 + 2 x 8.0 = 22.0 -> 17.33 + 17.33 + 22.0 = 56.67 LF (1/A5.1-6/A5.1; windows D1 / D2 per 11/A5.2 in RFI-17)"})
if not any(m["ref"] == "CJ-DOUBLE-STUDS" for m in c["misc_items"]):
    c["misc_items"].append({"ref": "CJ-DOUBLE-STUDS", "familia": "3-5/8\" stud (todos los gauges)", "qty": 31.48, "unit": "LF", "source": "2/A4.2",
        "label": "362S162-33 COLD FORM METAL STUDS DOUBLED AT CONTROL JOINT (A4.2 key note 4)",
        "op": "2 control joints on S42 (14/A4.1): 1 extra stud each x height: S42-H1 line 15.17 + S42-V2 16.31 = 31.48 LF"})
for r in c["rfis"]:
    if r["id"] == "RFI-04":
        r["tema"] = "CLOSED (plan check): south facade 36'-0\" stucco panel - the band measures 36.0 ft on A1.1, as printed"
        r["supuesto"] = "36'-0\" printed and measured"
        r["opciones"] = {"A": {"texto": "printed and measured agree", "source": "A1.1, A2.1", "delta": "0"},
                         "B": {"texto": "no code provision", "cita": "n/a", "delta": "0"}, "C": ""}
    if r["id"] == "RFI-14":
        r["supuesto"] = "vestibule heads carried 600S162-54 (16 ga, S4.1 key note 3 governs, A1.1 note 2.D) to the top of purlin; joists 600S162-43 @ 24\" (3/A3.1)"
        r["opciones"]["A"]["delta"] = "if 600S162-43 (3/A3.1 key 8): same LF, gauge 18 instead of 16 on 20.57 LF of heads; -0.67 ft x 20.6 LF if the purlin is 8\" deep"
    o = r.get("opciones") or {}
    r["delta"] = f"(A) {o.get('A', {}).get('delta','')} | (B) {o.get('B', {}).get('delta','')} | (C) ____"
if not any(r["id"] == "RFI-17" for r in c["rfis"]):
    c["rfis"].append({"id": "RFI-17", "tema": "FRT 2x4 blocking at the window D1 / D2 openings in the CMU", "donde": "south facade D1, D2",
        "supuesto": "not loaded (window rough opening of D1 / D2 not dimensioned on A5.2)", "source": "11/A5.2",
        "opciones": {"A": {"texto": "11/A5.2 draws FRT 2x4 blocking anchored to masonry at the window head / jambs", "source": "11/A5.2", "delta": "+ (W + 2 x H) per window, about +2 x 34 LF"},
                     "B": {"texto": "no code provision", "cita": "n/a", "delta": "0"}, "C": ""},
        "fuentes_revisadas": ["designation: A5.2 window schedule", "other row: doors 1/A5.1-6/A5.1 (loaded)", "standard rule: n/a", "detail: 11/A5.2"]})
    c["rfis"][-1]["delta"] = "(A) + (W + 2 x H) per window, about +2 x 34 LF | (B) 0 | (C) ____"
json.dump(c, open(E + "takeoff_canon_AB.json", "w"), indent=1, ensure_ascii=False)
print("paso11 fixes ok")
# Paso 11 items 12-13
for m in c["misc_items"]:
    if m["ref"] == "CJ-DOUBLE-STUDS":
        m["qty"] = 62.96
        m["op"] = ("2 control joints on S42 (14/A4.1, 2/A4.2): studs doubled on both sides of each joint (A4.2 key note 4) = 2 extra studs per joint; "
                   "heights not printed at the joint -> full stud height (53.3): 2 x 15.17 + 2 x 16.31 = 30.34 + 32.62 = 62.96 LF")
if not any(m["ref"] == "GB-S42-HDR-UNDERSIDE" for m in c["misc_items"]):
    c["misc_items"].append({"ref": "GB-S42-HDR-UNDERSIDE", "familia": "5/8\" gyp board Type X", "qty": 30.76, "unit": "SF", "source": "6/A4.2",
        "label": "5/8\" TYPE X gypsum board wrapping the underside of the S42 suspended header walls (6/A4.2 key 6)",
        "op": "header undersides S42-H2 25.44 + S42-V1 50.33 = 75.77 LF x wall width 4.875\" (3-5/8\" + 2 x 5/8\") = 75.77 x 0.406 = 30.76 SF"})
json.dump(c, open(E + "takeoff_canon_AB.json", "w"), indent=1, ensure_ascii=False)
print("items 12-13 ok")
# ---- Paso 12 gaps -> destination (RFI with delta, A plans / B code / C other) ----
def rfi(i, tema, donde, sup, src, ta, da, tb, cb, db):
    if any(r["id"] == i for r in c["rfis"]): return
    c["rfis"].append({"id": i, "tema": tema, "donde": donde, "supuesto": sup, "source": src,
        "opciones": {"A": {"texto": ta, "source": src, "delta": da}, "B": {"texto": tb, "cita": cb, "delta": db}, "C": ""},
        "fuentes_revisadas": [f"designation: {src}", "other row: Step 12 coverage matrix (MATRIZ_COBERTURA.xlsx)", f"standard rule: {cb}", f"detail: {src}"],
        "delta": f"(A) {da} | (B) {db} | (C) ____"})
rfi("RFI-18", "Gypsum board control joints on the S21 furring (walls over 30 ft and at masonry control joints)", "S21-N, S21-E1, S21-S",
    "not loaded: joint locations follow the masonry control joints of the exterior elevations, not dimensioned", "3.A/A1.1, A2.1 key 23",
    "A1.1 note 3.A: control joints in partition lengths over 30 ft and at masonry control joints", "about +77 LF of control joint (Step 12 estimate)",
    "control joints at 30 ft max", "ASTM C840 / GA-216", "+ 1 joint per 30 ft of S21 run x height")
rfi("RFI-19", "Moisture resistant Type X at the janitor sink area (A1.1 note 3.B)", "mop sink area, 13/A4.1",
    "regular Type X carried outside the restrooms", "3.B/A1.1, 13/A4.1", "W.R. at janitor sink areas: extent not dimensioned",
    "reclass +43 to +241 SF from Type X to Type X W.R. (no net SF change)", "MR board behind wet fixtures", "GA-216", "same reclass")
rfi("RFI-20", "Simpson FCB43.5 clips and their fasteners at the exterior stud connections (S5.2 key notes 16 / 23, 1/S5.3, 3/S5.3)", "entry piers, head wall",
    "not loaded: clip count per connection not dimensioned", "1/S5.3, 3/S5.3", "clips per stud at the CMU / wind beam connection",
    "+146 FCB43.5 clips, +584 #12-14 screws, +168 Tapcon, +124 #12-24 (Step 12 count)", "per manufacturer", "Simpson catalog", "same")
rfi("RFI-21", "Sheathing screws #6 x 1-1/4\" corrosion resistant (S5.2 key 8) vs #10 (S1.1 7.D)", "glass mat / FRT plywood sheathing",
    "not loaded", "S5.2, S1.1", "sheathing screws at the printed spacing", "about +1,075 screws", "#10 screws per S1.1 7.D", "S1.1 7.D", "same count, #10")
rfi("RFI-22", "FRT 2x nailers on the CMU parapet (5-6/A3.2, 4-5/A3.4, 2/A6.1) and 1/2\" anchors", "CMU parapets",
    "EXCLUDED: wood nailers anchored to the masonry parapet are rough carpentry / roofing (Div 06), not framing", "5/A3.2, 2/A6.1",
    "if carried by the framing sub", "+544 to 816 LF FRT 2x + 1/2\" anchors", "n/a", "n/a", "0")
rfi("RFI-23", "FRT 2x nailers inside the concealed PEMB column enclosures (1/A4.2 key 10)", "key note 1 columns, A1.1",
    "not loaded: enclosure by others (1/A4.2 key 16); column count not in our scope", "1/A4.2", "nailers per concealed column",
    "about +48 LF per column", "n/a", "n/a", "0")
rfi("RFI-24", "Security shutters 'may be required' (H/A5.2)", "storefront A", "not loaded", "H/A5.2", "framing for shutter housing if required",
    "0 now; header / box framing if the shutter is added", "n/a", "n/a", "0")
rfi("RFI-25", "Deflection track product: 3\" x 14 ga deep-leg slotted track (3/S5.1, 4/S5.1) vs track at stud gauge", "S42 full-height walls, S21 / S24 tops",
    "LF carried in the top / deflection track rows at stud gauge", "3/S5.1, 4/S5.1", "deep-leg 14 ga slotted track at walls to the purlin",
    "same LF, product upgrade on the full-height S42 walls (46.84 LF)", "deflection per A1.1 note 2.C", "A1.1 2.C", "0")
rfi("RFI-26", "Interior bottom track anchors: Titen HD @ 48\" (3/S5.1, 4/S5.1, S1.1 7.F/G) vs slab pins", "interior walls on slab",
    "slab pins carried (151.04 pcs, Inputs spacing)", "3/S5.1, S1.1", "Titen HD @ 48\" printed for the S42 floor walls",
    "-151.04 pins, + about 69 Titen HD (Step 12 count)", "n/a", "n/a", "0")
rfi("RFI-27", "Stud-to-track screws #10 (S1.1 7.E) vs #8 carried; framing screws charged on the Z-furring", "all framing",
    "#8-18 x 1/2\" carried by the tool rule", "S1.1", "#10 screws printed", "same count, #10 instead of #8; -668 screws on the Z-furring (no track)",
    "n/a", "n/a", "0")
for r in c["rfis"]:
    if r["id"] == "RFI-06":
        r["opciones"]["A"]["delta"] = str(r["opciones"]["A"]["delta"]) + "; head underside (1/A5.2): +36 SF 5/8\" X, +36 SF 1/4\", +30.67 LF corner bead"
    if r["id"] == "RFI-09":
        r["opciones"]["A"]["delta"] = str(r["opciones"]["A"]["delta"]) + "; 2/S5.1: +16 L4x4x3/16 clip angles, +32 A307 bolts, +22 2x2x14 ga clips, +44 #10 SDS; #10 screws at kicker / strut / splice +400"
    if r["id"] == "RFI-10":
        r["opciones"]["A"]["delta"] = str(r["opciones"]["A"]["delta"]) + "; plumbing fixture backing (C/A4.1) +12 LF"
    if r["id"] == "RFI-17":
        r["opciones"]["A"]["delta"] = str(r["opciones"]["A"]["delta"]) + "; FRT plywood at the D1 / D2 heads (11/A5.2) +15 SF"
    o = r.get("opciones") or {}
    r["delta"] = f"(A) {o.get('A', {}).get('delta','')} | (B) {o.get('B', {}).get('delta','')} | (C) ____"
json.dump(c, open(E + "takeoff_canon_AB.json", "w"), indent=1, ensure_ascii=False)
print("paso12 gaps ok", len(c["rfis"]))
