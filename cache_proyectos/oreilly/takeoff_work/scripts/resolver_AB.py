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
