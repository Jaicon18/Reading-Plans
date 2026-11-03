"""Decision 19 (rev2): finishes the Bluebeam PDF written by markups_bluebeam.py + markups_demo.py.
 - Page Label = sheet number on every marked page (A-050, A-052, A-202, A-221) + LEGEND;
 - wall markups: the SF in Contents = the board SF of the Excel (board_out.json, canon.py) instead of LF x H;
 - area markups (Polygon, /Measure 1/4" = 1'-0", area in Contents) for the new gyp ceilings and the soffit bottoms
   (A-221 hatch / soffit extents), the Level 5 play-area walls, the roof hatch shaft (A-221 drawn rectangle) and the
   two pin & sleeve recesses (A-202, position on the M3.5 walls assumed: width / location not printed, RFI-13).
Quantities in Contents come from the canon / canon.py outputs; geometry from the clean PDF vectors.
Use: python3 bitacora.py run scripts/markups_rev2_post.py <tools_dir> <in.pdf> <out.pdf>"""
import json, os, re, sys
sys.path.insert(0, sys.argv[1])
import pymupdf as fitz
import markups_bluebeam as mb
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C4 = os.path.join(K, "etapas", "4_canon")
c = json.load(open(os.path.join(C4, "takeoff_canon.json")))
bo = json.load(open(os.path.join(C4, "out", "board_out.json")))
M = {m["ref"]: m for m in c["misc_items"]}
W = {w["id"]: w for w in c["walls"]}
doc = fitz.open(sys.argv[2])
PG = {"A-050": 5, "A-052": 6, "A-202": 12, "A-221": 14}
# 1. wall SF = board SF of the Excel
bsf = {}
for f in bo["caras"]:
    bsf[f["wall"]] = round(bsf.get(f["wall"], 0) + f["sf"], 2)
n1 = 0
# markups_bluebeam.verificar requires its own Contents (SF = LF x H, v80e): the Excel board SF of every metal wall /
# soffit side is written on the legend page instead (free text, not an annotation)
lp = doc[doc.page_count - 1]
y = 560.0
lp.insert_text((40, y), "BOARD SF PER WALL = Excel Partition Takeoff (the same SF is in each wall markup):", fontsize=9, fontname="hebo")
for wid in sorted(bsf):
    if wid in W:
        y += 11
        lp.insert_text((40 if y < 760 else 380, y if y < 760 else y - 200), f"{wid}: {bsf[wid]:,.2f} SF board ({W[wid].get('tag') or ''})", fontsize=8, fontname="helv")
        n1 += 1
for pno in PG.values():
    for a in doc[pno].annots() or []:        # English states in DEMO contents (markups_demo copies the canon text)
        ct = a.info.get("content", "")
        en = ct.replace("DERIVADO", "DERIVED").replace("PENDIENTE", "PENDING").replace("CONFIRMADO", "CONFIRMED")
        if en != ct:
            a.set_info(content=en); a.update()
# 2. area markups
AREA = []
S_ = 18.0   # 1/4" = 1'-0" (A-221 / A-202 printed scale)
# BE-117: each gyp ceiling polygon is drawn from the printed S-241 dimensions of its take-off SF (same op as the canon),
# anchored at the corner of its A-221 gyp-ceiling hatch; the area of the polygon = the Excel SF
def rect(x0, y0, w, h):
    return [(x0, y0), (x0 + w * S_, y0), (x0 + w * S_, y0 + h * S_), (x0, y0 + h * S_)]
def men(x0, y0):        # 11'-3" x 7'-11 1/4" minus the 6.417 x 0.556 notch at the south-west corner (S-241 / A-221 hatch step)
    W_, H_, nw, nh = 11.25 * S_, 7.9375 * S_, 6.417 * S_, 0.556 * S_
    return [(x0, y0), (x0 + W_, y0), (x0 + W_, y0 + H_), (x0 + nw, y0 + H_), (x0 + nw, y0 + H_ - nh), (x0, y0 + H_ - nh)]
def wom(x0, yb):        # 13.583 x 5.75 (south bay) + 7.972 x 2.139 (north bay, east side) + 2.917 x 0.639 (north notch) - S-241
    W_, h1, w2, h2, w3, h3 = 13.583 * S_, 5.75 * S_, 7.972 * S_, 2.139 * S_, 2.917 * S_, 0.639 * S_
    xr, y1 = x0 + W_, yb - h1
    xl2, y2 = xr - w2, y1 - h2
    return [(x0, yb), (x0, y1), (xl2, y1), (xl2, y2 - h3), (xl2 + w3, y2 - h3), (xl2 + w3, y2), (xr, y2), (xr, yb)]
CL = {"CLG-ENTA-B": rect(1075.7, 277.8, 7.042, 6.583), "CLG-ENTB-B": rect(473.4, 869.5, 7.042, 9.646),
      "CLG-MEN-B": men(1832.9, 295.8), "CLG-WOM-B": wom(1730.0, 596.2), "CLG-PLAY-B": rect(338.6, 599.5, 2.928, 11.958)}
def area_ft(pts):
    q = pts + [pts[0]]
    return abs(sum(q[i][0] * q[i + 1][1] - q[i + 1][0] * q[i][1] for i in range(len(q) - 1))) / 2 / S_ ** 2
for ref, pts in CL.items():
    assert abs(area_ft(pts) / M[ref]["qty"] - 1) < 0.005, (ref, area_ft(pts), M[ref]["qty"])
    AREA.append(("A-221", "GYP CEILING", pts,
                 f"GYP CEILING · {ref[4:-2]} · {M[ref]['qty']:.2f} SF · 5/8\" sag-resistant (C09250 2.1.E) · outline from the S-241 printed dims at the A-221 gyp ceiling hatch · {ref}"))
srv = [(1225.6, 440.2), (1405.4, 440.2), (1405.4, 482.2), (1276.6, 482.2), (1276.6, 766.4), (1225.6, 766.4)]
gt = [(814.6, 584.8), (886.6, 584.8), (886.6, 728.8), (814.6, 728.8)]
SB = '1/2" GYPSUM BOARD REGULAR'
for pts, cl in ((srv, c["ceilings"][0]), (gt, c["ceilings"][1])):
    AREA.append(("A-221", SB, pts, f"{SB} · soffit bottom · {cl['room']} · {cl['area_sf']:.2f} SF · {cl['detail']} · {cl['id']}"))
l5 = c["level5_items"][0]
sf5 = round(l5["l_ft"] * (l5["h_ft"] - l5["base_ft"]["value"]), 2)
AREA.append(("A-221", "LEVEL 5", [(401.0, 529.8), (652.7, 529.8), (652.7, 857.2), (401.0, 857.2)],
             f"LEVEL 5 · play area walls WC-1 · {l5['l_ft']} LF x ({l5['h_ft']} - base {l5['base_ft']['value']}) = {sf5:.2f} SF · outline = play area room, LF = A-202 solid walls (cause in canon) · A-211 / A-050 KN12 · {l5['ref']}"))
ST = '3-5/8" METAL STUD'
AREA.append(("A-221", ST, rect(2047.7, 393.2, 3.0, 2.5),
             f"{ST} · roof hatch shaft 2'-6\" x 3'-0\" · {M['RH-SHAFT-S']['qty']} LF studs · {M['RH-SHAFT-T']['qty']} LF runner + {M['RH-SHAFT-TT']['qty']} LF slotted track (C1/S-801) · A1/A-604 · RH-SHAFT-S"))
RS = '8" STUD'
for j, wid in enumerate(("M3.5-01", "M3.5-02"), 1):
    b = W[wid]["band"]
    ym = (b["lo"] + b["hi"]) / 2
    ref = f"PS-RECESS-S{j}"
    AREA.append(("A-202", RS, [(b["c0"], ym - 18), (b["c1"], ym - 18), (b["c1"], ym + 18), (b["c0"], ym + 18)],
                 f"{RS} · pin & sleeve recess on {wid} (24\" box, MH-102: RFI-13 resolved) · {M[ref]['qty']:.2f} LF jamb studs + {M[f'PS-RECESS-T{j}']['qty']} LF head/sill runner · A2/A-605 · {ref}"))
json.dump([{"sheet": a, "subject": b, "pts": p_, "contents": t_} for a, b, p_, t_ in AREA],
          open(os.path.join(K, "etapas", "6_markups", "areas.json"), "w"), indent=1)
n2 = 0
for sh, subj, pts, ct in AREA:
    page = doc[PG[sh]]
    q = [fitz.Point(x, y) * page.derotation_matrix for x, y in pts]
    a = page.add_polygon_annot(q)
    a.set_info(title=mb.AUTOR, subject=subj, content=ct)
    a.set_colors(stroke=(0.1, 0.5, 0.1), fill=(0.6, 0.9, 0.6))
    a.set_border(width=2.0)
    a.set_opacity(0.45)
    a.update()
    mb._nm(doc, a, f"TOX-{subj}-{n2}")
    mb._measure(doc, a, 18.0)
    doc.xref_set_key(a.xref, "IT", "/PolygonDimension")
    n2 += 1
# 3. page labels = sheet numbers
labels = {v: k for k, v in PG.items()}
labels[doc.page_count - 1] = "LEGEND"
rules = []
for i in range(doc.page_count):
    if i in labels:
        rules.append({"startpage": i, "prefix": labels[i], "style": "", "firstpagenum": 1})
    elif i == 0 or (i - 1) in labels:
        rules.append({"startpage": i, "prefix": "", "style": "D", "firstpagenum": i + 1})
doc.set_page_labels(rules)
doc.save(sys.argv[3], garbage=1, deflate=True)
print(json.dumps({"wall_sf_updated": n1, "area_markups": n2, "page_labels": {labels[k]: k + 1 for k in sorted(labels)}}))
