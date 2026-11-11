"""rev3 (coordination order, BE-CF16): RFI-01 answered by the drawings. The B.O. DECK callouts printed on A1.2 and A2.0
are located by program along the demising wall D-01 (grid line 3 / lease line on A1.1). Both sheets are registered to
A1.1 through their grid bubbles F..A (x), and D-01 is split into height zones by the grid bays F..A that it crosses.
 - zone = grid bay of A1.1 (west end of D-01 -> F -> E -> D -> C -> B -> A -> east end), limits = grid lines as drawn;
 - deck of the zone = the printed B.O. DECK callout(s) whose label falls in that bay on A1.2 / A2.0 (highest one if two);
   a bay with no callout takes the higher of its two neighbours (conservative);
 - stud height = B.O. deck of the zone - 1" slip gap (10/A4.1, same rule as before); Type X both faces to the stud top
   (D/A4.1 "extend gyp. bd. to 1" below deck");
 - D-01 -> D-01a..D-01g (band sliced at the grid x, length = slice / 6.75 pt/ft), "split" nodes between the pieces (the
   cut stud is counted once, studs_nodos v61); the T of A-01 and the two free ends go to the piece that holds them;
 - each zone gets a circled crop of its callout(s) (etapas/4_canon/img_calc/);
 - riser room D-02 / D-03 / D-04 sit in the bay east of grid A, under the +-18'-3" callout = unchanged;
 - RFI-01 leaves the open list (closed in takeoff.json rfi_cierre); RFI-02..05 get the swept sheets + terms list.
Use: python3 bitacora.py run scripts/rev3_d01_zonas.py <clean.pdf>"""
import json, os, re, sys
import pymupdf as fitz
K = os.environ.get("K") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C4 = os.path.join(K, "etapas", "4_canon")
P = os.path.join(C4, "takeoff_canon.json")
c = json.load(open(P))
doc = fitz.open(sys.argv[1])
sm = json.load(open(os.path.join(K, "etapas", "SHEET_MAP.json")))
PG = {v: int(k) - 1 for k, v in sm.items()}
W = {w["id"]: w for w in c["walls"]}
if "D-01" not in W:
    sys.exit("D-01 already split (canon must be the resolved one)")
D = W["D-01"]
esc = c["constants"]["plan_scale_by_sheet"]["A1.1"]["value"]
LET = list("FEDCBA")


def grid_x(sheet):
    """x of the grid bubbles F..A (letters on one row, ~30 ft apart) of a sheet."""
    sp = []
    for b in doc[PG[sheet]].get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                if s["text"].strip() in LET and 8 < s["size"] < 12:
                    sp.append((s["text"].strip(), (s["bbox"][0] + s["bbox"][2]) / 2, round((s["bbox"][1] + s["bbox"][3]) / 2)))
    rows = {}
    for t, x, y in sp:
        rows.setdefault(y, {})[t] = x
    row = max(rows.values(), key=lambda r: len(r))
    if set(row) != set(LET):
        raise SystemExit(f"{sheet}: grid row F..A not found ({row})")
    return row


G11 = grid_x("A1.1")
RX = re.compile(r"B\.O\. DECK @ ±(\d+)'-(\d+(?: \d/\d)?)\"")


def callouts(sheet):
    g = grid_x(sheet)
    dx = sum(G11[k] - g[k] for k in LET) / len(LET)
    out = []
    pg = doc[PG[sheet]]
    for b in pg.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            t = "".join(s["text"] for s in l["spans"])
            m = RX.search(t)
            if not m:
                # A2.0 prints "B.O. DECK" and "@ +-x" on two lines of the same block
                bt = " ".join("".join(s["text"] for s in ll["spans"]) for ll in b.get("lines", []))
                m = RX.search(bt) if "B.O. DECK" in t and "@" not in t else None
                if not m:
                    continue
                bb = b["bbox"]
            else:
                bb = l["bbox"]
            inch = sum(float(fr.split("/")[0]) / float(fr.split("/")[1]) if "/" in fr else float(fr) for fr in m.group(2).split())
            ft = int(m.group(1)) + inch / 12.0
            out.append({"sheet": sheet, "txt": m.group(0), "ft": round(ft, 4), "bbox": [round(v, 1) for v in bb],
                        "x11": round((bb[0] + bb[2]) / 2 + dx, 1), "dx": round(dx, 1)})
    return out


CO = callouts("A1.2") + callouts("A2.0")
b = D["band"]
xs = [b["lo"]] + [G11[k] for k in LET] + [b["hi"]]
bays = [(xs[i], xs[i + 1], (["W end"] + LET)[i] + "-" + (LET + ["E end"])[i]) for i in range(len(xs) - 1)]
dk = []
for lo, hi, nm in bays:
    cs = [x for x in CO if (lo <= x["x11"] < hi) or (nm.endswith("E end") and x["x11"] >= lo) or (nm.startswith("W end") and x["x11"] < hi)]
    dk.append(cs)
deck = [max(x["ft"] for x in cs) if cs else None for cs in dk]
for i, v in enumerate(deck):
    if v is None:
        nb = [deck[j] for j in (i - 1, i + 1) if 0 <= j < len(deck) and deck[j] is not None]
        deck[i] = max(nb)
os.makedirs(os.path.join(C4, "img_calc"), exist_ok=True)


def crop(cs, name):
    """circled crop of the callout labels of a zone (first sheet that prints one)."""
    if not cs:
        return None
    x = cs[0]
    pg = fitz.open(sys.argv[1])[PG[x["sheet"]]]      # fresh copy: only this zone's circles
    r = fitz.Rect(x["bbox"]) + (-90, -60, 90, 60)
    sh = pg.new_shape()
    for y in cs:
        if y["sheet"] == x["sheet"]:
            sh.draw_oval(fitz.Rect(y["bbox"]) + (-8, -6, 8, 6))
    sh.finish(color=(1, 0, 0), width=2)
    sh.commit()
    p = os.path.join(C4, "img_calc", f"{name}_{x['sheet']}.png")
    pg.get_pixmap(dpi=150, clip=r).save(p)
    return p


piezas, n0 = [], 0
for i, ((lo, hi, nm), cs, dft) in enumerate(zip(bays, dk, deck)):
    sid = f"D-01{'abcdefg'[i]}"
    h = round(dft - 1 / 12.0, 2)
    L = round((hi - lo) / esc, 3)
    img = crop(cs, f"D01_zone_{sid}")
    src_c = "; ".join(f"{x['sheet']} '{x['txt']} A.F.F.' (label at x {x['x11']:.0f} pt on A1.1 after grid registration dx {x['dx']:+.1f} pt)" for x in cs) \
        or f"no callout in bay {nm}: the higher neighbour callout {dft:.4g} ft loaded (conservative)"
    w = json.loads(json.dumps(D))
    w["id"] = sid
    w["band"] = dict(b, lo=round(lo, 1), hi=round(hi, 1))
    w["length_ft"] = L
    w["length_source"] = (f"zone {nm} of D-01 (A1.1 printed +-209'-1\" overall, V.I.F.): band {lo:.1f} -> {hi:.1f} pt between the grid lines "
                          f"as drawn = {hi - lo:.1f} / {esc} = {L} ft [DERIVED]")
    w.pop("length_op", None)
    w["height_ft"] = h
    w["height_source"] = (f"stud = B.O. deck of the zone - 1\" slip gap (10/A4.1 'MTL. STUD CUT 1\" SHORT OF DECK'): {dft:.4g} - 0.08 = {h} ft; "
                          f"deck = {src_c} [DERIVED from the printed callout]")
    w["height_op"] = f"{round(dft, 3)} - 0.083 = {h}"
    w["bracing_rows_source"] = f"A4.1 Wall Type Note 7: partitions higher than 12'-0\": 1-1/2\" 16 GA CRC @ 8'-0\" O.C. vert.: FLOOR({h}/8) = {int(h // 8)} rows [DERIVED]"
    w["bracing_rows"] = int(h // 8)
    for f in w["faces"]:
        f["height_ft"] = h
        f["height_source"] = f"D/A4.1 'EXTEND GYP. BD. TO 1\" BELOW DECK' = stud height of the zone {h} ft [DERIVED]"
    if img:
        w["height_img"] = img
    w["tag_ids"] = [t for t in D.get("tag_ids") or [] if not re.fullmatch(r"P[AC]\d{4}", str(t))] if i else list(D.get("tag_ids") or [])
    if i:      # tag ids stay with the first piece; the others are the same tagged wall
        w["untagged_reason"] = "zone of the tagged demising wall D-01 (A1.1 D tags), split by height zone"
        w["tag_ids"] = []
    piezas.append(w)
# walls that reference D-01 (adjacent_to / part_of / bulkhead_of) point to the piece they sit along
for x in c["walls"]:
    for kk in ("adjacent_to", "part_of", "bulkhead_of"):
        if x.get(kk) == "D-01":
            mx = (x["band"]["lo"] + x["band"]["hi"]) / 2 if x["band"]["ori"] == "H" else (x["band"]["c0"] + x["band"]["c1"]) / 2
            x[kk] = next(p["id"] for p in piezas if p["band"]["lo"] <= mx <= p["band"]["hi"])
c["walls"] = [x for x in c["walls"] if x["id"] != "D-01"]
k = next(i for i, x in enumerate(json.load(open(P))["walls"]) if x["id"] == "D-01")
c["walls"][k:k] = piezas
# nodes
nodes = []
fr = 0
for nd in c["nodes"]:
    if nd.get("through") == "D-01":
        bx = (W[nd["branch"]]["band"]["c0"] + W[nd["branch"]]["band"]["c1"]) / 2
        nd["through"] = next(p["id"] for p in piezas if p["band"]["lo"] <= bx <= p["band"]["hi"])
    if nd.get("wall") == "D-01" and nd.get("kind") == "free":
        nd["wall"] = piezas[0]["id"] if fr == 0 else piezas[-1]["id"]
        fr += 1
    nodes.append(nd)
for a, b2 in zip(piezas, piezas[1:]):
    nodes.append({"id": f"N-SPLIT-{b2['id']}", "kind": "split", "walls": [a["id"], b2["id"]],
                  "why": "height zone change at a grid line (printed B.O. deck callouts A1.2 / A2.0)", "source": "A1.2 / A2.0"})
c["nodes"] = nodes
for m in c.get("misc_items") or []:
    m["op"] = str(m.get("op") or "").replace("D-01 209.10 LF", "D-01 (zones D-01a..g) 209.10 LF")
# RFI-01 resolved by the drawings; swept lists on the open RFIs
r1 = next((r for r in c["rfis"] if r["id"] == "RFI-01"), None)
c["rfis"] = [r for r in c["rfis"] if r["id"] != "RFI-01"]
c["rfi01_resuelto"] = {"zones": [{"id": p["id"], "lf": p["length_ft"], "h": p["height_ft"]} for p in piezas],
                       "question": (r1 or {}).get("question", "")}
SW = ("all 50 sheets (A0.0-A5.3, AS1.0-AS1.1, D1.0, S1.0-S4.1, M1.0-M1.3, P1.0-P1.1, FP1.0, E0.1-E2.2, EMS-1..4, incl. SHX text)")
TERMS = ["B.O. DECK", "B.O. JOIST", "T.O. STEEL", "UNDERSIDE", "KICKER", "BRACE", "BRACING", "LAYER", "EXISTING GYP",
         "EXISTING PARTITION", "EXISTING STUD", "EXISTING WALL", "HEAD", "A.F.F."]
SPEC = {"RFI-02": "D1.0 keynotes 207 / 209 / 211 + demo legend, A1.2", "RFI-03": "S2.1, S4.1, 1/A4.3, 4/A4.3",
        "RFI-04": "1/A5.3, 3/A5.3, A5.2", "RFI-05": "A1.1 wall legend note 1, 2/A4.1, A1.2"}
for r in c["rfis"]:
    r["barrido"] = {"hojas": "ALL", "terminos": TERMS, "swept_txt": f"Swept: {SW}; terms: {', '.join(TERMS)}; specific sheets: {SPEC.get(r['id'], r.get('source', ''))}"}
json.dump(c, open(P, "w"), indent=1, ensure_ascii=False)
for p, cs in zip(piezas, dk):
    print(p["id"], p["length_ft"], "LF", p["height_ft"], "ft", [x["sheet"] + " " + x["txt"] for x in cs] or "(neighbour)")
print("total LF", round(sum(p["length_ft"] for p in piezas), 3))
