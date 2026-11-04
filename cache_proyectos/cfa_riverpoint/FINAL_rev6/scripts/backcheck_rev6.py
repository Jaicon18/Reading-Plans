"""Self back-check of every item changed in rev6 against the drawing: one crop per item (clean bid set) + its N/SHEET and what
the crop shows -> cfa_final/FINAL_FOR_REVIEW_rev6/proceso/BACKCHECK_rev6.md (+ backcheck_rev6_img/). Crops located by the printed
text (search_for) of each item. Use: python3 bitacora.py run scripts/backcheck_rev6.py <clean.pdf> <excel>"""
import json, os, sys
import pymupdf, openpyxl
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.dirname(K)
F = os.path.join(S, "cfa_final", "FINAL_FOR_REVIEW_rev6", "proceso")
IMG = os.path.join(F, "backcheck_rev6_img")
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
  "M3.5-01 / M3.5-02 / MB-01 ends die into the existing kitchen wall faces EX-KIT-01..03 (abut, 0 studs - same count as rev5).", "M3.5-01"),
 ("BC-07 quote fix (BE-12)", 28, "TO STOP", (-260, -40, 360, 60), "A-611 note 3",
  "Printed text reads 'CEMEMNTITIOUS BOARD TO STOP - RE: DETAIL' (typo in the plan): quoted verbatim [sic].", "CEMEMNTITIOUS"),
 ("BC-08 wall type schedule (fichas.json)", 12, "WALL TYPE SCHEDULE", (-640, -120, 450, 330), "A-202",
  "WALL TYPE SCHEDULE - EXTERIOR / - INTERIOR read independently for fichas.json (SW6, M2.1, M3.5, W4, W4.1, W6, W8).", "M2.1"),
]
L = ["# BACKCHECK rev6 — CFA #2284 River Point (self back-check of every rev6 change against the drawing)", "",
     "Program: scripts/backcheck_rev6.py (crops of the clean bid set located by the printed text; Excel evidence searched in the rev6 Excel). "
     "Items 1-8 = the rev5 changes (still valid); items 9-13 = the rev6 changes. Material Summary rev5 -> rev6: only +0.01 SF 1/2\" cement board (rounding of the split pieces), proceso/CAMBIOS_rev6.md.", "",
     "| # | Item | N/SHEET | What the drawing shows | Excel rev6 | Crop | Result |", "|---|---|---|---|---|---|---|"]
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
    L.append(f"| {i} | {iid} | {nh} | {shows} | {'found in ' + ', '.join(hit) if hit else 'NOT FOUND'} | backcheck_rev6_img/{os.path.basename(f)} | {'PASS' if ok else 'FAIL'} |")
# rev6 items: crop = extent of the canon geometry of the element (pieces by axis drawn in red over the clean sheet)
EW = c["existing_walls"]
DG = {e["id"]: e for e in c["demo_geom"]}
ITEMS6 = [
 ("BC-09 one axis per number: EX-RRM-01-CB", 12, [e["path"] for e in EW if e.get("split_of") == "EX-RRM-01-CB"], "KN10/A-050 + A-611 note A.5 (drawn on A-202)",
  "Men's restroom existing wall: 3 straight axes (west / north / east faces) = EX-RRM-01-CB-1, -2, -3; 7.40 + 11.25 + 8.00 = 26.65 LF = rev5 single entry.", "EX-RRM-01-CB-3"),
 ("BC-10 one axis per number: EX-MP-01", 12, [e["path"] for e in EW if e.get("split_of") == "EX-MP-01"], "FRP-2/A-211 + G.3/A-202 (drawn on A-202)",
  "Multi-purpose room existing walls: 6 straight axes, each its own row; pieces add up to the rev5 33.917 LF.", "EX-MP-01-6"),
 ("BC-11 one axis per number: DEMO-02", 5, [DG[i]["polyline"] for i in ("DEMO-02-1", "DEMO-02-2")], "KN3/A-050",
  "L partition demolished (multi-purpose / mech): 2 axes DEMO-02-1 + DEMO-02-2 = 12.928 LF x 12.167 ft x 2 layers = 314.59 SF (rev5 total).", "DEMO-02-2"),
 ("BC-12 ceiling demo as AREA polygon: DEMO-C6", 6, [[[2264.9, 387.6], [2341.3, 387.6], [2341.3, 534.2], [2264.9, 534.2], [2264.9, 387.6]]], "KN10/A-052",
  "East-room gyp ceiling hatch = 34.57 SF polygon; 38.35 SF reading A loaded (Review Item 5 open, delta -3.78 SF).", "DEMO-C6"),
 ("BC-13 Review Item 6 image = PT0019 mop chase", 12, [e["path"] for e in EW if e["id"] == "W6-05W-MOP" or e.get("split_of") == "EX-MOP-01" or e["id"] == "EX-MOP-01"],
  "G.7/A-202 + KN25/A-201", "W6 tag PT0019 at the mop sink chase (rev5 image showed PT0018 / PT0024).", "W6-05W-MOP"),
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
    L.append(f"| {j} | {iid} | {nh} | {shows} | {'found in ' + ', '.join(hit) if hit else 'NOT FOUND'} | backcheck_rev6_img/{os.path.basename(f)} | {'PASS' if ok else 'FAIL'} |")
ITEMS += ITEMS6
fr = sum(1 for n in c["nodes"] if n.get("kind") == "free")
L += ["", f"Nodes: {fr} free of {len(c['nodes'])} ({fr / len(c['nodes']):.0%}); the 4 free ends are soffit sides on A-221 that die on wood walls (no metal wall there).",
      f"RESULT: {'PASS' if ok_all else 'FAIL'} ({len(ITEMS)} items)"]
open(os.path.join(F, "BACKCHECK_rev6.md"), "w").write("\n".join(L) + "\n")
open(os.path.join(K, "etapas", "BACKCHECK_rev6.md"), "w").write("\n".join(L) + "\n")
print("BACKCHECK", "PASS" if ok_all else "FAIL")
sys.exit(0 if ok_all else 1)
