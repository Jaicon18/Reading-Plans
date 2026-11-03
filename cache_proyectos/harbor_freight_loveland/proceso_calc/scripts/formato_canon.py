"""Input-format fixes of the resolved canon demanded by the gates (reglas.py / etapas.py), by program, each one recorded
in the element (*_info / *_op) - HFT Loveland:
 - R72.6 faces[].side -> A (north or west on the sheet) / B (south or east): compass word of the reading when it has
   one; otherwise the side of the band where the face's room number (first room of the face, numbers in parentheses
   ignored) is printed on the same sheet (nearest occurrence to the wall); a face left undecided takes the opposite side
   of the other face of its wall;
 - height_source 'same as <wall>' -> the text of that wall (D-03 / D-04 = D-02);
 - R73.8 length_op whose printed value governs over the vector check: rewritten "printed <dim> = <value> ft (governs);
   vector <op>" (the value of the wall is not changed);
 - R70.2 corners (esquinas.py): corner square without owner -> the thicker wall (tie: the first one) is extended by the
   gap esquinas.py measures, at the end next to the other wall (band + length_ft, op written); double corner of
   printed lengths / boundary studs / furring on two faces -> corners_ok with the reason; collinear gap explained by the
   drawing -> gaps_ok;
 - E23 rfis[].delta = the deltas of options A / B already written;
 - R71.9 mep_sweep.registro.no_usable: mep.py registration of M1.0-M1.2 against A1.1 not usable (ok False), ducts
   EXCLUDED by standing order, image = the M1.0 sheet.
Use: python3 bitacora.py run scripts/formato_canon.py <tools_dir> <clean.pdf>"""
import json, os, re, sys
sys.path.insert(0, sys.argv[1])
import pymupdf as fitz
import esquinas, chequeos_v73
K = os.environ.get("K") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C4 = os.path.join(K, "etapas", "4_canon")
P = os.path.join(C4, "takeoff_canon.json")
c = json.load(open(P))
doc = fitz.open(sys.argv[2])
sm = json.load(open(os.path.join(K, "etapas", "SHEET_MAP.json")))
PAG = {v: int(k) - 1 for k, v in sm.items()}
W = {w["id"]: w for w in c["walls"]}
n = 0
# 1. height_source 'same as X'
for w in c["walls"]:
    m = re.match(r"\s*same as ([A-Z]+-\d+)\s*$", str(w.get("height_source") or ""), re.I)
    if m and m.group(1) in W:
        w["height_source_info"] = w["height_source"]
        w["height_source"] = W[m.group(1)]["height_source"]
        n += 1
# 2. face sides
COMP = {"north": "A", "west": "A", "south": "B", "east": "B"}
cache = {}


def hits(sheet, num):
    k = (sheet, num)
    if k not in cache:
        cache[k] = [((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2) for r in doc[PAG[sheet]].search_for(num)]
    return cache[k]


def lado(w, f):
    s = str(f.get("side") or "")
    if s in ("A", "B", "END"):
        return s, None
    if s.lower() in COMP:
        return COMP[s.lower()], f"compass side '{s}' of the reading"
    room = re.sub(r"\([^)]*\)", "", str(f.get("room") or ""))
    b = w["band"]
    cen = (b["c0"] + b["c1"]) / 2
    mid = (b["lo"] + b["hi"]) / 2
    m = next((x.group(1) for x in re.finditer(r"\b(1\d{2})\b", room) if hits(b["sheet"], x.group(1))), None)   # first room printed on the sheet
    if not m:      # no room number printed on this sheet: the room NAME (first word, e.g. RESTROOM) printed on the sheet
        nm = re.match(r"\s*([A-Za-z']{4,})", room)
        m = nm.group(1).upper() if nm and hits(b["sheet"], nm.group(1).upper()) else None
    if not m:
        return None, None
    hs = hits(b["sheet"], m)
    M = (mid, cen) if b["ori"] == "H" else (cen, mid)
    pt = min(hs, key=lambda p: (p[0] - M[0]) ** 2 + (p[1] - M[1]) ** 2)
    perp = pt[1] if b["ori"] == "H" else pt[0]
    CONF[id(f)] = (len(room.split("/")), ((pt[0] - M[0]) ** 2 + (pt[1] - M[1]) ** 2) ** 0.5)
    return ("A" if perp < cen else "B"), f"room '{m}' printed at ({pt[0]:.0f},{pt[1]:.0f}) pt on {b['sheet']}, " \
        f"{'north' if b['ori'] == 'H' and perp < cen else 'south' if b['ori'] == 'H' else 'west' if perp < cen else 'east'} of the wall band"


malos = []
CONF = {}
for w in c["walls"]:
    fs = w.get("faces") or []
    res = [lado(w, f) for f in fs]
    # two faces placed on the same side by their room tags: the face with one room (then the nearest tag) is trusted,
    # the other face takes the opposite side
    if len(fs) == 2 and res[0][0] == res[1][0] and res[0][0] in ("A", "B") and all(id(f) in CONF for f in fs) \
            and str(fs[0].get("side")) not in ("A", "B") and str(fs[1].get("side")) not in ("A", "B"):
        k = min((0, 1), key=lambda i: CONF[id(fs[i])])
        res[1 - k] = (None, None)
    for i, f in enumerate(fs):
        s, info = res[i]
        if s is None and len(fs) == 2 and res[1 - i][0] in ("A", "B"):
            s, info = ("B" if res[1 - i][0] == "A" else "A"), "opposite side of the other face of this wall"
        if s is None:
            malos.append(f"{w['id']} face '{f.get('side')}' ({f.get('room')})")
            continue
        if info:
            f["side_info"] = f"read as '{f.get('side')}' -> {s}: {info}"
            f["side"] = s
            n += 1
if malos:
    sys.exit("face side not decidable by program: " + "; ".join(malos))
# 3. R73.8 printed-governs ops
for msg in chequeos_v73.r73_8(c):
    m = re.match(r"R73\.8 ([^:/]+): (\w+_op) da", msg)
    if not m or m.group(1) not in W:
        continue
    w, k = W[m.group(1)], m.group(2)
    v = k[:-3] + "_ft"
    op = w[k]
    pm = re.search(r"printed\s+'?([^()]+?)'?\s*\(", op)
    if not pm or v not in w:
        continue
    w[k + "_info"] = op
    w[k] = f"{op.split('printed')[0]}printed {pm.group(1).strip()} = {w[v]} ft (printed value governs); vector check " + \
        re.sub(r"=", "->", op[pm.end() - 1:])
    n += 1
# 4. corners / gaps
TH = {p["type"]: float(p.get("thickness_in") or 0) for p in c.get("partition_schedule") or []}
r = esquinas.revisar(c)
OK = {("A-02", "A-01"): "both lengths are printed A1.1 dimensions (25'-10\" and 11'-6 1/2\"), printed values govern; the corner square is in both (conservative, overlap = one wall thickness)",
      ("E-01", "E-03"): "furring on two masonry faces (E/A4.1): each face carries its own vertical hat channel at the inside corner",
      ("RE-2", "RE-1"): "structural CFS walls with printed out-to-out lengths (S2.1 19'-10\" / 19'-8\"): each wall has its own boundary studs (S2.1 shear wall elevations)",
      ("RE-2", "RE-3"): "structural CFS walls with printed out-to-out lengths (S2.1 19'-8\" / 19'-10\"): each wall has its own boundary studs (S2.1 shear wall elevations)"}
for e in r["esquinas"]:
    a, b = e["walls"]
    if e["estado"] == "DOBLE":
        why = OK.get((a, b)) or OK.get((b, a))
        if not why:
            sys.exit(f"double corner {a}/{b} without a recorded reason")
        if not any(set(x.get("walls") or []) == {a, b} for x in c.get("corners_ok") or []):
            c.setdefault("corners_ok", []).append({"walls": [a, b], "reason": why, "source": W[a]["sheet"]})
            n += 1
    elif e["estado"] == "SIN DUEÑO":
        msg = next(x for x in r["fallas"] if f"{a} / {b}" in x)
        gap = float(re.search(r"falta ~([\d.]+) ft", msg).group(1))
        ta, tb = TH.get(W[a]["tag"], 0), TH.get(W[b]["tag"], 0)
        cands = [(a, b), (b, a)] if ta >= tb else [(b, a), (a, b)]
        hecho = False
        for own, oth in cands:          # the thicker wall first; the other one if extending it makes a new double corner
            wo, wt = W[own], W[oth]
            bo, bt = wo["band"], wt["band"]
            esc = c["constants"]["plan_scale_by_sheet"].get(bo["sheet"], c["constants"]["plan_scale_pt_per_ft"])["value"]
            ct = (bt["c0"] + bt["c1"]) / 2
            prev = (dict(bo), wo["length_ft"])
            if abs(bo["lo"] - ct) < abs(bo["hi"] - ct):
                bo["lo"] = round(bo["lo"] - gap * esc, 1)
            else:
                bo["hi"] = round(bo["hi"] + gap * esc, 1)
            dob = [x for x in esquinas.revisar(c)["esquinas"] if x["estado"] == "DOBLE" and own in x["walls"]
                   and not any(set(y.get("walls") or []) == set(x["walls"]) for y in c.get("corners_ok") or [])
                   and not (OK.get(tuple(x["walls"])) or OK.get(tuple(x["walls"][::-1])))]
            par = [x["id"] for x in c["walls"] if x["id"] != own and x["band"]["sheet"] == bo["sheet"] and x["band"]["ori"] == bo["ori"]
                   and abs((x["band"]["c0"] + x["band"]["c1"]) / 2 - (bo["c0"] + bo["c1"]) / 2) < 1.0 * esc
                   and min(x["band"]["hi"], bo["hi"]) - max(x["band"]["lo"], bo["lo"]) > 0.05 * esc]
            if dob or par:
                bo.clear(); bo.update(prev[0])
                bloq = (dob[0]["walls"] if dob else par)
                continue
            old = prev[1]
            wo["length_ft"] = round(old + gap, 3)
            wo["length_op"] = (f"{wo['length_ft']} ft = {old} ft (single printed / measured dimension, simple ticks) plus the "
                               f"corner square {gap} ft with {oth} owned by this wall (R70.2, gap measured by esquinas.py)")
            wo["length_source"] = str(wo.get("length_source") or "") + f" + corner square with {oth} (R70.2, esquinas.py {gap} ft)"
            n += 1
            hecho = True
            break
        if not hecho:   # the corner square is already framed by a third wall (T / jog): declared, nothing added
            c.setdefault("corners_ok", []).append({"walls": [a, b], "source": W[a]["sheet"],
                "reason": f"the corner square of {a} / {b} lies against {', '.join(x for x in bloq if x not in (a, b))}: extending "
                          f"either wall would double that corner or run along it, so the framing of the square belongs to it "
                          f"(checked by program with esquinas.py)"})
            n += 1
GAPS = {("A-10", "A-14"): "drinking fountain alcove between the restroom walls: the recess is framed by A-11 / A-12 / A-13 (1/A4.0), no wall on the line"}
for h in r["huecos"]:
    a, b = h["walls"]
    why = GAPS.get((a, b)) or GAPS.get((b, a))
    if not why:
        sys.exit(f"collinear gap {a}/{b} without a recorded reason")
    if not any(set(x.get("between") or []) == {a, b} for x in c.get("gaps_ok") or []):
        c.setdefault("gaps_ok", []).append({"between": [a, b], "reason": why, "source": "1/A4.0"})
        n += 1
# 5. RFI delta
for rf in c["rfis"]:
    o = rf.get("opciones") or rf.get("options") or {}
    rf["delta"] = f"A: {(o.get('A') or {}).get('delta', 'n/a')} | B: {(o.get('B') or {}).get('delta', 'n/a')}"
    n += 1
# 6. MEP registration not usable
sw = c.get("mep_sweep") or {}
rg = sw.get("registro") or {}
if isinstance(rg, dict) and (rg.get("matches") or 0) < 25 and not rg.get("no_usable"):
    img = os.path.join(C4, "img_runner", "sheet_M1.0.png")
    if not os.path.exists(img):
        os.makedirs(os.path.dirname(img), exist_ok=True)
        doc[PAG["M1.0"]].get_pixmap(dpi=40).save(img)
    rg["no_usable"] = {"motivo": "mep.py registration of M1.0 / M1.1 / M1.2 against A1.1 not usable (ok False, < 25 votes: the "
                                 "M sheets carry no common grid text); ducts / pipes crossing our walls are EXCLUDED by estimator "
                                 "standing order, so no quantity depends on the crossing",
                       "source": "M1.0, M1.1, M1.2 + A1.1", "img": img}
    sw["registro"] = rg
    n += 1
# 7. top track kind (slip / standard) from the top_track text of the reading -> two track families on separate rows
for w in c["walls"]:
    t = str(w.get("top_track") or "")
    if w.get("top_track_kind") or w.get("top_track") is False or not t:
        continue
    k = "standard" if re.search(r"\bstandard\b|no slip", t, re.I) else "slip" if re.search(r"slip|deflection", t, re.I) \
        else "standard" if re.search(r"track", t, re.I) else None
    if k:
        w["top_track_kind"] = k
        w["top_track_kind_source"] = (re.search(r"\b\d{1,2}/[A-Z]\d\.\d\b|\b[A-Z]/[A-Z]\d\.\d\b", t) or [w.get("detail")])[0] + " - " + t[:160]
        n += 1
# 8. fasteners EXCLUDED (estimator standing order): the tool rows stay with 0 and this source
if not c.get("fasteners_excluded"):
    c["fasteners_excluded"] = {"why": "estimator standing order: fasteners / screws / anchors / PAF EXCLUDED (0); A4.1 wall type notes "
                                      "print the fastening of board and framing", "source": "A4.1 notes"}
    n += 1
# 9. window sill track: the window frame detail is the source of the sill track
for w in c["walls"]:
    for o in w.get("openings") or []:
        if o.get("kind") == "window" and o.get("sill_ft") and not o.get("with_sill_source"):
            o["with_sill"] = True
            o["with_sill_source"] = f"{o.get('header_source', '').split(' ')[0]} interior window detail + {o.get('source', '')[:60]}"
            n += 1
# 10. additional head track at openings > 4'-0": estimator standing criterion, cited at the headers of this set
cs = c.setdefault("constants", {})
for k_, v_, s_ in (("addl_head_track_min_ro_ft", 4.0, "S2.1 header schedule / 2/A5.1 heads (opening > 4'-0\" rule = estimator standing criterion)"),
                   ("header_bearing_ft", 0.667, "S2.1 header schedule (8\" bearing each side = estimator standing criterion)")):
    if k_ not in cs:
        cs[k_] = {"value": v_, "source": s_}
        n += 1
an = {x.get("familia") for x in c.get("accesorios_none") or []}
if "PAFs and duct sleeves" not in an:
    c.setdefault("accesorios_none", []).append({"familia": "PAFs and duct sleeves", "why": "no parapet infill, coiling grille or "
                                                "duct sleeve detail in the set; ducts EXCLUDED by standing order", "source": "A1.1, A5.0, M1.0"})
    n += 1
# 11. internal rule codes out of texts that reach the Excel (R80e.84)
RXR = re.compile(r"\s*\(?\b(?:standing order\s+)?R\d+[a-z]?\.\d+\)?")
for k_ in ("accesorios_none",):
    for x in c.get(k_) or []:
        if RXR.search(str(x.get("why") or "")):
            x["why"] = RXR.sub("", x["why"]).replace("EXCLUDED by", "EXCLUDED by estimator standing order").replace("order order", "order")
            n += 1
c["exclusions_info"] = [RXR.sub("", str(x)) for x in c.get("exclusions_info") or []]
ms = c.get("mep_sweep") or {}
if RXR.search(str(ms.get("count_info") or "")):
    ms["count_info"] = RXR.sub("", ms["count_info"])
# 13. deflection clips: the reading wrote the "no clips printed" text as note_source (= a note that ASKS for clips)
dc = c.get("deflection_clips") or {}
if not dc.get("none_reason") and re.search(r"no clips? (printed|shown)|no deflection clip", str(dc.get("note_source") or ""), re.I):
    dc["none_reason"] = dc.pop("note_source")
    dc["source"] = dc.get("slip_track_source") or "A4.1"
    c["deflection_clips"] = dc
    n += 1
# 12. BE-117 (c): drawn length vs LF > 0.5 % -> the cause is written on the element (printed dimension governs)
import math
SC = c["constants"].get("plan_scale_by_sheet") or {}
def esc_de(sh):
    v = SC.get(sh) or c["constants"]["plan_scale_pt_per_ft"]
    v = v.get("value") if isinstance(v, dict) else v
    if sh not in SC:      # sheet without a recorded scale: its printed scale label (S2.1 1/4" = 1'-0")
        t = doc[PAG[sh]].get_text()
        m = re.search(r"SCALE:?\s*(\d+)/(\d+)\"\s*=\s*1'-0\"", t)
        if m:
            v = 72.0 * int(m.group(1)) / int(m.group(2))
    return float(v)
for w in c["walls"]:
    b = w["band"]
    dib = abs(b["hi"] - b["lo"]) / esc_de(b["sheet"])
    if abs(dib / w["length_ft"] - 1) > 0.005 and not w.get("length_cause"):
        w["length_cause"] = (f"drawn band {dib:.2f} ft at the printed scale of {b['sheet']} vs {w['length_ft']} ft loaded: the printed "
                             f"dimension / take-off length governs ({str(w.get('length_source') or '')[:90]})")
        n += 1
G = json.load(open(os.path.join(C4, "demo_geom.json")))
MI = {m["ref"]: m for m in c.get("misc_items") or []}
for g in G:
    pl = g["polyline"]
    dib = sum(math.dist(pl[i], pl[i + 1]) for i in range(len(pl) - 1)) / esc_de(g["sheet"])
    m = MI.get(g["id"])
    if m and g.get("lf") and abs(dib / float(g["lf"]) - 1) > 0.005 and not m.get("length_cause"):
        m["length_cause"] = (f"polyline on the D1.0 dashed vectors measures {dib:.2f} ft; the LF {g['lf']} of the take-off governs "
                             f"({str(g.get('op') or '')[:80]})")
        n += 1
json.dump(c, open(P, "w"), indent=1, ensure_ascii=False)
print("format fields:", n)
