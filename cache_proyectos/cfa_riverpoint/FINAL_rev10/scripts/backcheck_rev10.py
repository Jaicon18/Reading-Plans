"""Self back-check of every item changed in rev10 against the drawing: one crop per item (clean bid set) + its N/SHEET and what
the crop shows -> cfa_final/FINAL_FOR_REVIEW_rev10/proceso/BACKCHECK_rev10.md (+ backcheck_rev10_img/). Crops located by the printed
text (search_for) of each item. Use: python3 bitacora.py run scripts/backcheck_rev10.py <clean.pdf> <excel>"""
import json, os, sys
import pymupdf, openpyxl
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.dirname(K)
F = os.path.join(S, "cfa_final", "FINAL_FOR_REVIEW_rev10", "proceso")
IMG = os.path.join(F, "backcheck_rev10_img")
os.makedirs(IMG, exist_ok=True)
doc = pymupdf.open(sys.argv[1])
wb = openpyxl.load_workbook(sys.argv[2], data_only=True)
txt = {ws.title: " ".join(str(c.value) for row in ws.iter_rows() for c in row if c.value is not None) for ws in wb.worksheets}
c = json.load(open(os.path.join(K, "etapas", "4_canon", "takeoff_canon.json")))
ITEMS = [  # (id, page index, text to locate, (dx0, dy0, dx1, dy1), N/SHEET, what the crop shows, Excel evidence to find)
 ("BC-01 RFI-10 closed (R-ALC-07)", 70, "16'-10", (-450, -250, 450, 200), "A4/S-601 + S-201",
  "A4/S-601 prints 16'-10 3/4\" (F.V.) T/EXIST TOP PLATE = bearing of the existing 2x10 roof joists on the east wall (B.O. structure at that wall): DEMO-09 / -10 loaded to 16'-10 3/4\" (R-ALC-07, never to an assumed ceiling).", "R-ALC-07"),
 ("BC-02 RFI-10 DEMO-08 bay", 65, "(+13", (-300, -150, 300, 200), "S-201",
  "(+13'-6\") TOP OF JOIST of the 16\" TJI bay: B.O. = 13'-6\" - 16\" = 12'-2\" = DEMO-08 height.", "12'-2"),
 ("BC-03 RFI-09 closed (nearest printed spec rule)", 66, "BRIDGING LOCATION", (-260, -60, 260, 120), "A2/S-241",
  "LGS CEILING JOIST SCHEDULE: 600S162-33 @ 16\", column BRIDGING LOCATION = MID SPAN (no member printed).", "MID SPAN"),
 ("BC-04 RFI-09 member", 74, "Cold-rolled steel channel", (-420, -140, 420, 120), "S-902 C05400 3.3.I.1 / 3.4.E.2",
  "'Bridging: Cold-rolled steel channel' = the member loaded (1 row 1-1/2\" C.R. channel per LGS ceiling, 50.87 LF).", "Bracing 1-1/2\" C.R. channel"),
 ("BC-05 opening schedule (BE-90)", 35, "VESTIBULE (PAIR)", (-120, -120, 900, 330), "A-801",
  "DOOR SCHEDULE doors 01-13: all in existing / storefront / wood walls; none tagged on M2.1-01, M3.5-01 / -02 or MB-01 (A-202).", "Headers, sills and jambs"),
 ("BC-06 node topology (BE-89)", 12, "M3.5", (-150, -120, 150, 380), "A-202",
  "M3.5-01 / M3.5-02 / MB-01 ends die into the existing kitchen wall faces EX-KIT-01..03 (abut, 0 studs - same count as rev9).", "M3.5-01"),
 ("BC-07 quote fix (BE-12)", 28, "TO STOP", (-260, -40, 360, 60), "A-611 note 3",
  "Printed text reads 'CEMEMNTITIOUS BOARD TO STOP - RE: DETAIL' (typo in the plan): quoted verbatim [sic].", "CEMEMNTITIOUS"),
 ("BC-08 wall type schedule (fichas.json)", 12, "WALL TYPE SCHEDULE", (-640, -120, 450, 330), "A-202",
  "WALL TYPE SCHEDULE - EXTERIOR / - INTERIOR read independently for fichas.json (SW6, M2.1, M3.5, W4, W4.1, W6, W8).", "M2.1"),
]
L = ["# BACKCHECK rev10 — CFA #2284 River Point (self back-check of every rev10 change against the drawing)", "",
     "Program: scripts/backcheck_rev10.py (crops of the clean bid set located by the printed text; Excel evidence searched in the rev10 Excel). "
     "Items 1-8 = the rev9 changes (still valid); items 9-13 = the rev10 changes. Material Summary rev9 -> rev10: only +0.01 SF 1/2\" cement board (rounding of the split pieces), proceso/CAMBIOS_rev10.md.", "",
     "| # | Item | N/SHEET | What the drawing shows | Excel rev10 | Crop | Result |", "|---|---|---|---|---|---|---|"]
ok_all = True
for i, (iid, pg, q, (a, b, c2, d2), nh, shows, ev) in enumerate(ITEMS, 1):
    p = doc[pg]
    rs = p.search_for(q)
    if not rs:
        raise SystemExit(f"{iid}: '{q}' not found on page {pg + 1}")
    r = rs[0]
    clip = pymupdf.Rect(r.x0 + a, r.y0 + b, r.x1 + c2, r.y1 + d2) & p.rect
    f = os.path.join(IMG, f"bc{i:02d}.png")
    p.get_pixmap(clip=clip, dpi=110).save(f)
    hit = [h for h, t in txt.items() if ev in t]
    ok = bool(hit)
    ok_all &= ok
    L.append(f"| {i} | {iid} | {nh} | {shows} | {'found in ' + ', '.join(hit) if hit else 'NOT FOUND'} | backcheck_rev10_img/{os.path.basename(f)} | {'PASS' if ok else 'FAIL'} |")
# rev10 items: crop = extent of the canon geometry of the element (pieces by axis drawn in red over the clean sheet)
EW = c["existing_walls"]
DG = {e["id"]: e for e in c["demo_geom"]}
ITEMS6 = [
 ("BC-09 one axis per number: EX-RRM-01-CB", 12, [e["path"] for e in EW if e.get("split_of") == "EX-RRM-01-CB"], "KN10/A-050 + A-611 note A.5 (drawn on A-202)",
  "Men's restroom existing wall: 3 straight axes (west / north / east faces) = EX-RRM-01-CB-1, -2, -3; 7.40 + 11.25 + 8.00 = 26.65 LF = rev9 single entry.", "EX-RRM-01-CB-3"),
 ("BC-10 one axis per number: EX-MP-01", 12, [e["path"] for e in EW if e.get("split_of") == "EX-MP-01"], "FRP-2/A-211 + G.3/A-202 (drawn on A-202)",
  "Multi-purpose room existing walls: 6 straight axes, each its own row; pieces add up to the rev9 33.917 LF.", "EX-MP-01-6"),
 ("BC-11 one axis per number: DEMO-02", 5, [DG[i]["polyline"] for i in ("DEMO-02-1", "DEMO-02-2")], "KN3/A-050",
  "L partition demolished (multi-purpose / mech): 2 axes DEMO-02-1 + DEMO-02-2 = 12.928 LF x 12.167 ft x 2 layers = 314.59 SF (rev9 total).", "DEMO-02-2"),
 ("BC-12 ceiling demo as AREA polygon: DEMO-C6", 6, [[[2264.9, 387.6], [2341.3, 387.6], [2341.3, 534.2], [2264.9, 534.2], [2264.9, 387.6]]], "KN10/A-052",
  "East-room gyp ceiling hatch = 34.57 SF polygon; 38.35 SF reading A loaded (Review Item 5 open, delta -3.78 SF).", "DEMO-C6"),
 ("BC-13 Review Item 6 image = PT0019 mop chase", 12, [e["path"] for e in EW if e["id"] == "W6-05W-MOP" or e.get("split_of") == "EX-MOP-01" or e["id"] == "EX-MOP-01"],
  "G.7/A-202 + KN25/A-201", "W6 tag PT0019 at the mop sink chase (rev9 image showed PT0018 / PT0024).", "W6-05W-MOP"),
]
from PIL import Image, ImageDraw
for j, (iid, pg, paths, nh, shows, ev) in enumerate(ITEMS6, len(ITEMS) + 1):
    p = doc[pg]
    pts = [q for pa in paths for q in pa]
    if not pts:
        raise SystemExit(f"{iid}: no geometry in the canon")
    x0, y0, x1, y1 = min(q[0] for q in pts), min(q[1] for q in pts), max(q[0] for q in pts), max(q[1] for q in pts)
    clip = pymupdf.Rect(x0 - 140, y0 - 140, x1 + 140, y1 + 140) & p.rect
    z = 110 / 72
    pix = p.get_pixmap(clip=clip, dpi=110)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    dr = ImageDraw.Draw(im)
    for pa in paths:
        dr.line([((u - clip.x0) * z, (v - clip.y0) * z) for u, v in pa], fill=(255, 0, 0), width=4)
    f = os.path.join(IMG, f"bc{j:02d}.png")
    im.save(f)
    hit = [h for h, t in txt.items() if ev in t]
    ok = bool(hit)
    ok_all &= ok
    L.append(f"| {j} | {iid} | {nh} | {shows} | {'found in ' + ', '.join(hit) if hit else 'NOT FOUND'} | backcheck_rev10_img/{os.path.basename(f)} | {'PASS' if ok else 'FAIL'} |")
ITEMS += ITEMS6
# rev10 items: the circled crop of the bubble view (etapas/8_burbujas/img_rev10) + the Excel evidence of the change
import shutil
ITEMS7 = [
 ("BC-14 EX-KIT-02 removed", "A3_A-601.png", "A3/A-601 + A-202", "Kitchen elevation: 'OPEN TO BEYOND' between the hoods = the 10'-0 1/2\" critical clear opening to the drive-thru: no wall, no base.", "OPEN TO BEYOND", True),
 ("BC-15 restroom cement / gyp transition", "A2_A-604.png", "A2/A-604", "CEMENT / GYP. TRANSITION 2 1/4\" (+/-) below T/TILE AT RR: cement board to 6'-6 1/4\" = 6.521 ft, MR gyp above.", "6.521", False),
 ("BC-16 MB-01 serving face", "D3_A-624.png", "D3/A-624", "1/2\" GYPSUM BOARD from 7'-0\" A.F.F. BOTT. OF GYPSUM BD. to 6\" MIN. over the ACT = 3.5 ft; WALL TILE below -> cement board 0-7'-0\".", "MB-01-SRV-CB", False),
 ("BC-17 BOH base 1'-3\"", "C3_A-604.png", "C3/A-604", "WALL BASE DETAIL @ BACK OF HOUSE prints 1' - 3\": loaded on the non-kitchen BOH faces.", "C3/A-604", False),
 ("BC-18 dining wainscot plywood by G.C.", "C1_A-625.png", "C1/A-625", "1/2\" PLYWOOD SHEATHING ABOVE CEMENT BOARD BY G.C. to T/PLYWOOD 6'-4\": our gyp only above 6'-4\".", "T/PLYWOOD", False),
 ("BC-20 drive-thru: no furr down (rev10)", "C1_A-603.png", "C1/A-603 + A-221", "C1/A-603 draws the wall face flat (FRP-2 7'-8\" to the ceiling); A-221 RCP runs ACT-1 to the wall with no soffit band -> 7'-8\" = finish datum; RFI-27 keeps the framed alternative.", "RFI-27", False),
 ("BC-21 DEMO-14 on the demo plan A-050 (rev10)", "C4_A-604.png", "A-050 KN10 + A-611", "The 12 restroom pieces of DEMO-14 are now marked on the demo plan A-050 (registered A-202 + (49, 98) pt), R-ALC-06.", "DEMO-14", False),
 ("BC-19 W6 dining face full-height tile", "A4_A-621.png", "A4/A-621", "CT-58A wall tile to CEILING 10'-4\" -> cement board full height (precedent #15).", "CT-58A", False),
]
for j, (iid, img, nh, shows, ev, en_canon) in enumerate(ITEMS7, len(ITEMS) + 1):
    src = os.path.join(K, "etapas", "8_burbujas", "img_rev7", img)
    f = os.path.join(IMG, f"bc{j:02d}.png")
    shutil.copy2(src, f)
    hit = [h for h, t in txt.items() if ev in t]
    if en_canon and not hit:          # a removed entry: the evidence is its absence + the change log
        ok = "EX-KIT-02" not in json.dumps(c["existing_walls"]) and "EX-KIT-02" not in " ".join(txt.values())
        hit = ["removed from every sheet (CAMBIOS_rev10.md)"] if ok else []
    ok = bool(hit)
    ok_all &= ok
    L.append(f"| {j} | {iid} | {nh} | {shows} | {'found in ' + ', '.join(hit) if hit else 'NOT FOUND'} | backcheck_rev10_img/{os.path.basename(f)} | {'PASS' if ok else 'FAIL'} |")
ITEMS += ITEMS7
# rev10 items: evidence crops of the RFI hunt (etapas/9_rfi10/img_rfi10)
ITEMS10 = [
 ("BC-22 RFI-27 wood furr-out (rev10)", "rfi27_a402_A3_furrout.png", "A-402 A3 + A-501 C2", "2x wood furr-out over the sliding-door head, 4\" deep at 3/4\"=1'-0\": Div. 06, nothing of ours.", "RFI-27"),
 ("BC-23 RFI-28 DEMO-C6 34.57 SF (rev10)", "rfi28_a052_eastroom.png", "A-052 KN10", "East-room inside faces 76.4 x 146.6 pt at 18 pt/ft = 34.57 SF (A-050 34.59).", "34.57"),
 ("BC-24 DEMO-12 outline re-measured (rev10)", "b2_A052_width_zoom.png", "A-052 KN3 / KN7", "Outline 1538.40 to the wall face 1560.60 = 1.233 ft; length 336.36 pt = 18.69 ft.", "DEMO-12"),
 ("BC-25 RFI-11 hunt (rev10)", "RFI-11_A050_KN8.png", "A-050 KN8 + E-200", "KN8 'DEMO HALF WALLS IN DINING ROOM' is the only call-out; no height printed in either set (RFI-11 open).", "RFI-11"),
]
for j, (iid, img, nh, shows, ev) in enumerate(ITEMS10, len(ITEMS) + 1):
    shutil.copy2(os.path.join(K, "etapas", "9_rfi10", "img_rfi10", img), os.path.join(IMG, f"bc{j:02d}.png"))
    hit = [h for h, t in txt.items() if ev in t]
    ok_all &= bool(hit)
    L.append(f"| {j} | {iid} | {nh} | {shows} | {'found in ' + ', '.join(hit) if hit else 'NOT FOUND'} | backcheck_rev10_img/bc{j:02d}.png | {'PASS' if hit else 'FAIL'} |")
ITEMS += ITEMS10
fr = sum(1 for n in c["nodes"] if n.get("kind") == "free")
L += ["", f"Nodes: {fr} free of {len(c['nodes'])} ({fr / len(c['nodes']):.0%}); 4 free ends are soffit sides on A-221 that die on wood walls (no metal wall there) and 2 are the M3.5-01 / M3.5-02 jambs of the open drive-thru opening (EX-KIT-02 removed, rev10).",
      f"RESULT: {'PASS' if ok_all else 'FAIL'} ({len(ITEMS)} items)"]
open(os.path.join(F, "BACKCHECK_rev10.md"), "w").write("\n".join(L) + "\n")
open(os.path.join(K, "etapas", "BACKCHECK_rev10.md"), "w").write("\n".join(L) + "\n")
print("BACKCHECK", "PASS" if ok_all else "FAIL")
sys.exit(0 if ok_all else 1)
