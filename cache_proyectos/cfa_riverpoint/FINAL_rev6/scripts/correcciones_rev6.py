"""rev6 (coordination 3-nov: run the v81cf26+ delivery gate with the day-1 preferences U-114..U-125). Text / status changes only,
after correcciones_rev5.py; no quantity input changes (every quantity recomputed by canon.py / accesorios.py / plantilla_excel.py).
Log -> etapas/4_canon/rev6_log.json.
  1. U-114: every face height carries its #0 status in height_status: [DERIVED] + the operation re-written with the printed
     operands, or [CONFIRMED] + the printed dimension and its sheet (13 faces of the metal walls / soffits).
  2. U-115: N/SHEET form on the board-only sources: '<TYPE>/A-202' (type in the A-202 schedule), '<note>/<sheet>' (A-202 wall
     notes G / H, interior elevation general notes A.x printed on A-601..A-623), '<finish tag>/A-211'.
  5. U-120 (EJES, day-1 order 'nunca juntar dos ejes en un número'): every board-only entry / demo element whose drawn path turns
     (L / U shapes, 22 existing_walls + DEMO-02) is split into one entry per straight axis '<id>-1', '<id>-2', ...: LF of each
     piece = its drawn segment / 18 pt/ft, the < 0.05 ft difference to the loaded total spread by length so the SUM of the pieces
     = the rev5 LF exactly; height, faces, board, source unchanged (tag_ids stay on the first piece).
  3. U-116: resolved-RFI answers no longer say 'not printed' where the value is DERIVED from printed elevations / notes.
Use: python3 bitacora.py run scripts/correcciones_rev6.py"""
import json, math, os, re
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(K, "etapas", "4_canon", "takeoff_canon.json")
c = json.load(open(P))
LOG = []
log = lambda *a: LOG.append(dict(zip(("item", "rev5", "rev6", "delta", "src", "rule"), a)))

# 1. face height status
EST = {
 ("M2.1-01", "A"): "[DERIVED] C.H. 10'-2\" (A-221) + 4\" (G.4/A-202) = 10.5 ft",
 ("M3.5-01", "B"): "[CONFIRMED] full height to the deck: T.O. +14'-8\" printed on S-201 (C4) = 14.667 ft (G.4/A-202 draftstopping exception)",
 ("M3.5-02", "B"): "[DERIVED] C.H. 10'-2\" (A-221) + 4\" (G.4/A-202) = 10.5 ft",
 ("MB-01", "A"): "[DERIVED] deck 14'-8\" (S-201 C4) - B.O. gypsum 7'-0\" A.F.F. (D3/A-624) = 7.667 ft",
 ("MB-01", "B"): "[CONFIRMED] full height to the deck: T.O. +14'-8\" printed on S-201 (C4) = 14.667 ft (G.4/A-202 draftstopping exception)",
}
for w in c["walls"]:
    for f in w.get("faces") or []:
        k = (w["id"], f.get("side"))
        if k in EST:
            v = EST[k]
        elif w["id"].startswith("SS-"):
            m = re.search(r"C\.H\. (\w+) (\d+'-\d+\") - soffit C\.H\. (\d+'-\d+\") \+ 6\" min above ACT \(C4/A-624\) = ([\d.]+) ft",
                          str(f.get("height_source")))
            if not m:
                continue
            v = f"[DERIVED] C.H. {m.group(2)} (A-221 {m.group(1)}) - soffit C.H. {m.group(3)} (A-221) + 6\" above ACT (C4/A-624) = {m.group(4)} ft"
        else:
            continue
        if f.get("height_status") != v:
            log(f"{w['id']} face {f.get('side')} height status", f.get("height_status") or "(none)", v, "0", "per source", "U-114 / BE-131")
            f["height_status"] = v

# 2. N/SHEET form
SUBS = [
 (re.compile(r"\bA-202 (W4\.1|W4|W6|W8|SW6) tag(?: tag)?"), r"\1/A-202 tag"),
 (re.compile(r"\b(W4\.1|W4|W6|W8|SW6)(?: type)? A-202\b"), r"\1/A-202"),
 (re.compile(r"\bA-202 note ([A-H]\.\d{1,2})"), r"\1/A-202"),
 (re.compile(r"\bA\.3 interior elevation general notes"), "A.3/A-621 interior elevation general notes (same notes on A-601..A-623)"),
 (re.compile(r"\bA-601\.\.A-623 note (A\.\d{1,2})"), r"\1/A-621 (interior elevation general notes, same on A-601..A-623)"),
 (re.compile(r"\b(FRP-2|PT-31B|WD-3 / CT-73B|WD-3) A-211\b"), lambda m: m.group(1).replace(" / ", ", ") + "/A-211"),
 (re.compile(r"receiving new FRP-2 \(A-211\)"), "receiving new FRP-2/A-211"),
]
n2 = 0
for e in c["existing_walls"]:
    for k in ("source", "height_source", "keynote"):
        v = e.get(k)
        if not isinstance(v, str):
            continue
        s = v
        for rx, t in SUBS:
            s = rx.sub(t, s)
        if s != v:
            e[k] = s
            n2 += 1
log("board-only sources in N/SHEET form", "type / note / finish tag cited next to the sheet ('SW6 A-202')",
    "N/SHEET ('SW6/A-202', 'G.3/A-202', 'A.3/A-621', 'FRP-2/A-211')", "0", f"{n2} fields", "U-115 / BE-131")

# 3. resolved answers that called a DERIVED value 'not printed'
R = {r["id"]: r for r in c["rfis"]}
for r in c["rfis"]:
    rs = r.get("resolved") or {}
    a = str(rs.get("answer") or "")
    b = a.replace(" The walk-in box height itself is not printed.",
                  " The board top does not depend on the walk-in box height (G.11/A-202 measures from the finish ceiling).")
    b = b.replace("The stud height as a single dimension is not printed; it is derived from printed elevations.",
                  "The stud height is [DERIVED] from the printed elevations above.")
    if b != a:
        rs["answer"] = b
        log(f"{r['id']} resolved answer wording", "'... not printed'", "[DERIVED] from the printed values", "0", rs.get("source", ""), "U-116 / BE-131")

SPLIT = {}


def _giro(a, b, q):
    import math as m_
    u, v = (b[0] - a[0], b[1] - a[1]), (q[0] - b[0], q[1] - b[1])
    lu, lv = m_.hypot(*u), m_.hypot(*v)
    if lu < 3 or lv < 3:
        return 0.0
    return m_.degrees(m_.acos(max(-1.0, min(1.0, (u[0] * v[0] + u[1] * v[1]) / (lu * lv)))))


def _tramos(pa):
    out, cur = [], [pa[0]]
    for i in range(1, len(pa)):
        cur.append(pa[i])
        if i < len(pa) - 1 and _giro(pa[i - 1], pa[i], pa[i + 1]) > 60:
            out.append(cur)
            cur = [pa[i]]
    out.append(cur)
    return out


def _reparto(L, segs):
    tot = sum(segs)
    v = [round(x + (L - tot) * x / tot, 3) for x in segs]
    v[-1] = round(L - sum(v[:-1]), 3)
    return v


ESC = 18.0                                             # plan_scale_by_sheet A-202 / A-050 (printed 1/4" = 1'-0", verified)
new_ew = []
for e in c["existing_walls"]:
    tr = _tramos(e["path"])
    if len(tr) == 1 or re.search(r"-\d$", e["id"]) and e.get("split_of"):
        new_ew.append(e)
        continue
    segs = [sum(math.dist(a, b) for a, b in zip(t, t[1:])) / ESC for t in tr]
    lfs = _reparto(float(e["length_ft"]), segs)
    ids = []
    for k, (t, lf) in enumerate(zip(tr, lfs), 1):
        x = json.loads(json.dumps(e))
        x["id"] = f"{e['id']}-{k}"
        x["path"], x["length_ft"], x["split_of"] = t, lf, e["id"]
        x["length_op"] = (f"[DERIVED] axis {k} of {len(tr)} of {e['id']} (rev5 one entry {e['length_ft']} LF on {len(tr)} axes; U-120 one axis "
                          f"per number): drawn {segs[k - 1] * ESC:.1f} pt / 18 pt/ft = {segs[k - 1]:.3f} ft -> {lf} LF (pieces sum = {e['length_ft']} LF)")
        if k > 1:
            x["tag_ids"] = []
        new_ew.append(x)
        ids.append(x["id"])
    SPLIT[e["id"]] = ids
    log(f"{e['id']} split by axis", f"1 entry {e['length_ft']} LF", " + ".join(f"{i} {l}" for i, l in zip(ids, lfs)), "0 LF (sum kept)",
        e.get("sheet", "A-202"), "U-120 / BE-131")
c["existing_walls"] = new_ew
# text references to the split ids (DEMO-14 operation, J-PLAY source)
for k in ("misc_items", "trim_items"):
    for m in c[k]:
        for f in ("op", "source"):
            v = m.get(f)
            if isinstance(v, str):
                for old, ids in SPLIT.items():
                    v = re.sub(re.escape(old) + r"(?![\w.-])", " + ".join(ids) if len(ids) < 4 else f"{ids[0]}..{ids[-1]}", v)
                m[f] = v
# DEMO-02 (L partition on A-050): one demo element per axis
dg = {e["id"]: e for e in c["demo_geom"]}
if "DEMO-02" in dg:
    e = dg["DEMO-02"]
    tr = _tramos(e["polyline"])
    segs = [sum(math.dist(a, b) for a, b in zip(t, t[1:])) / ESC for t in tr]
    lfs = _reparto(float(e["lf"]), segs)
    H, ly = float(e["h_ft"]), int(e["layers"])
    sfs = [round(l * H * ly, 2) for l in lfs]
    mi = next(m for m in c["misc_items"] if m["ref"] == "DEMO-02")
    sfs[-1] = round(float(mi["qty"]) - sum(sfs[:-1]), 2)
    pos = c["demo_geom"].index(e)
    piezas = []
    for k, (t, l, sf) in enumerate(zip(tr, lfs, sfs), 1):
        x = dict(e, id=f"DEMO-02-{k}", polyline=t, lf=l, sf=sf, split_of="DEMO-02")
        piezas.append(x)
    c["demo_geom"][pos:pos + 1] = piezas
    pm = c["misc_items"].index(mi)
    c["misc_items"][pm:pm + 1] = [dict(mi, ref=x["id"], qty=x["sf"], op=f"{x['lf']} LF x {H} ft x {ly} layer(s) = {x['sf']} SF "
                                       f"(axis {k} of {len(piezas)} of the L partition DEMO-02, U-120)") for k, x in enumerate(piezas, 1)]
    log("DEMO-02 split by axis", f"1 element {e['lf']} LF / {mi['qty']} SF", " + ".join(f"{x['id']} {x['lf']} LF / {x['sf']} SF" for x in piezas),
        "0 SF (sum kept)", "KN3 A-050", "U-120 / BE-131")

json.dump(c, open(P, "w"), ensure_ascii=False, indent=1)
json.dump(LOG, open(os.path.join(K, "etapas", "4_canon", "rev6_log.json"), "w"), ensure_ascii=False, indent=1)
print(f"rev6 corrections: {len(LOG)} log lines, {n2} source fields")

# 4. DEMO-C6 (Review Item 5, PENDING): the demo markup is now an AREA polygon (U-121) and the verifier compares its area.
#    The outline drawn on the A-052 ceiling hatch measures 34.57 SF; the loaded 38.35 SF is reading A (A-052 vector 75.8 x 163.9 pt
#    / 324). The cause is written on the element (BE-117 area_cause); the quantity is not changed while Review Item 5 is open.
c = json.load(open(P))
CZ = ("A-052 hatch outline of the east-room gyp ceiling = 34.57 SF (polygon of the markup); loaded 38.35 SF = reading A "
      "(A-052 vector 75.8 x 163.9 pt / 324 pt2/SF) [PENDING] Review Item 5 (A 38.35 SF / B 35.39 SF); delta if the hatch governs -3.78 SF")
for k in ("misc_items", "demo_geom"):
    for e in c[k]:
        if (e.get("ref") or e.get("id")) == "DEMO-C6" and e.get("area_cause") != CZ:
            e["area_cause"] = CZ
            LOG.append({"item": f"DEMO-C6 area cause ({k})", "rev5": "(none)", "rev6": CZ, "delta": "0", "src": "A-052 KN10", "rule": "BE-117 / U-121"})
json.dump(c, open(P, "w"), ensure_ascii=False, indent=1)
json.dump(LOG, open(os.path.join(K, "etapas", "4_canon", "rev6_log.json"), "w"), ensure_ascii=False, indent=1)
