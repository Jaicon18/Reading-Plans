"""RFI-16 delta BY PROGRAM: what metal framing would be added if the NEW interior wood W-type walls (W4, W4.1, W6, W8;
not SW6 exterior, not existing walls) were metal studs @ 16" O.C. (A-201 legend 'METAL STUD WALL' alternative).

1. Reads the reconciled canon (etapas/4_canon/takeoff_canon.json). The new W walls exist there only as board-only
   entries (existing_walls[] with ids W4-*, W4.1-*, W6-*, W8-*, R-W6-*; ids EX-* = existing walls, SW6-* = exterior,
   both left out).
2. Wall LF per wall group (id prefix TYPE-nn) = geometric union of the face paths projected on the wall axis:
   segments of the same orientation whose cross coordinate is within 16 pt (wall thickness <= 2x8 + 2 sheathing)
   form one straight run; LF of the run = union of their intervals along the axis / 18 pt/ft (A-202 1/4" scale).
3. Stud size per the A-202 WALL TYPE SCHEDULE - INTERIOR (printed): W4 / W4.1 / W6 = '2x4 WD STUD @16" O.C.'
   -> 3-5/8"; W8 = '2x8 WD STUD @16" O.C.' -> 8" (W6 prints 2x4, not 2x6: no 6" studs result).
4. Framing height = 10.667 ft for every run: C.1/A-202 framing 6" above ceiling + BOH C.H. 10'-2" (A-221), the same
   height the canon gives the metal walls M2.1 / M3.5 (smoke-partition runs to deck stay in RFI-04).
5. Writes a COPY of the canon with one metal 'wall' per run (faces [] - the board is already in existing_walls) and
   runs canon.py on it through bitacora.py; the delta = familias_out(copy) - familias_out(base) per family.
Out: etapas/4_canon/rfi16/ (canon copy, out/, rfi16_delta.json)
"""
import json, os, subprocess, sys, copy
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = sys.argv[1]
C4 = os.path.join(K, "etapas", "4_canon")
D = os.path.join(C4, "rfi16")
os.makedirs(D, exist_ok=True)
c = json.load(open(os.path.join(C4, "takeoff_canon.json")))
PT = 18.0
STUD = {"W4": "3-5/8\"", "W4.1": "3-5/8\"", "W6": "3-5/8\"", "W8": "8\""}
PRINT = {"W4": "2x4 WD STUD @16\" O.C.", "W4.1": "2x4 WD STUD @16\" O.C.", "W6": "2x4 WD STUD @16\" O.C.",
         "W8": "2x8 WD STUD @16\" O.C."}


def tipo_grupo(eid):
    s = eid[2:] if eid.startswith("R-") else eid
    t = s.split("-")[0]
    if t not in STUD:
        return None, None
    n = s.split("-")[1][:2]
    return t, f"{t}-{n}" + ("R" if eid.startswith("R-") else "")


grupos = {}
for e in c["existing_walls"]:
    t, g = tipo_grupo(e["id"])
    if t:
        grupos.setdefault((t, g), []).append(e)

runs = []
for (t, g), es in sorted(grupos.items(), key=lambda kv: kv[0][1]):
    segs = []
    for e in es:
        p = e["path"]
        for a, b in zip(p, p[1:]):
            if abs(a[1] - b[1]) < 0.5:
                segs.append(("H", (a[1]), min(a[0], b[0]), max(a[0], b[0]), e["id"]))
            elif abs(a[0] - b[0]) < 0.5:
                segs.append(("V", (a[0]), min(a[1], b[1]), max(a[1], b[1]), e["id"]))
            else:
                sys.exit(f"{e['id']}: non orthogonal segment {a}-{b}")
    clus = []
    for s in sorted(segs, key=lambda s: (s[0], s[1])):
        for cl in clus:
            if cl["ori"] == s[0] and abs(cl["c"] - s[1]) <= 16.0:
                cl["segs"].append(s)
                break
        else:
            clus.append({"ori": s[0], "c": s[1], "segs": [s]})
    for k, cl in enumerate(clus, 1):
        iv = sorted((s[2], s[3]) for s in cl["segs"])
        u, cur = [], list(iv[0])
        for lo, hi in iv[1:]:
            if lo <= cur[1] + 0.5:
                cur[1] = max(cur[1], hi)
            else:
                u.append(cur); cur = [lo, hi]
        u.append(cur)
        for j, (lo, hi) in enumerate(u, 1):
            cs = [s[1] for s in cl["segs"]]
            runs.append({"id": f"RFI16-{g}-{k}{'' if len(u) == 1 else chr(96 + j)}", "type": t, "group": g, "ori": cl["ori"],
                         "c0": min(cs), "c1": max(cs) if max(cs) > min(cs) else min(cs) + 4.0, "lo": lo, "hi": hi,
                         "lf": round((hi - lo) / PT, 3), "from": sorted({s[4] for s in cl["segs"]})})

base = copy.deepcopy(c)
alt = copy.deepcopy(c)
proto = [w for w in c["walls"] if w["id"] == "MB-01"][0]
for r in runs:
    w = copy.deepcopy(proto)
    w.update({"id": r["id"], "tag": "M3.5" if STUD[r["type"]] == "3-5/8\"" else "M3.5",
              "tag_ids": [], "location": f"RFI-16 alternative: {r['type']} wall {r['group']} as metal studs (from {', '.join(r['from'])})",
              "band": {"ori": r["ori"], "c0": r["c0"], "c1": r["c1"], "lo": r["lo"], "hi": r["hi"], "sheet": "A-202"},
              "length_ft": r["lf"], "length_status": "DERIVADO",
              "length_source": f"A-202 board-only face paths of {r['group']} (canon existing_walls) union along the axis [DERIVED]",
              "length_op": f"{r['hi']} - {r['lo']} = {round(r['hi'] - r['lo'], 1)} pt / 18 = {r['lf']} ft",
              "untagged_reason": f"RFI-16 alternative of the {r['type']} wood wall (A-202 schedule '{PRINT[r['type']]}')",
              "default_type_source": f"A-202 WALL TYPE SCHEDULE - INTERIOR {r['type']} '{PRINT[r['type']]}' read as metal per A-201 legend 'METAL STUD WALL' (RFI-16 option)",
              "height_ft": 10.667, "height_source": "C.1/A-202 framing 6\" above ceiling: BOH C.H. 10'-2\" (A-221) + 0.5 = 10.667 ft [DERIVED, RFI-16 alternative]",
              "stud_size": STUD[r["type"]], "stud_source": f"A-202 schedule {r['type']} '{PRINT[r['type']]}' -> metal equivalent {STUD[r['type']]} @ 16\" (RFI-16)",
              "oc_in": 16, "oc_source": f"A-202 schedule {r['type']} '@16\" O.C.'",
              "detail": "C2/S-801", "faces": [],
              "faces_none_reason": "board of this wall is already carried in the board-only entries (existing_walls); RFI-16 delta = framing only",
              "top_track_kind": "standard", "openings": []})
    alt["walls"].append(w)
    for e in (1, 2):
        alt["nodes"].append({"kind": "free", "wall": r["id"], "id": f"N-{r['id']}-{e}",
                             "source": "RFI-16 alternative: end node (free, no corner extras)"})
json.dump(alt, open(os.path.join(D, "takeoff_canon_RFI16_metal.json"), "w"), indent=1, ensure_ascii=False)
env = dict(os.environ)
p = subprocess.run([sys.executable, os.path.join(T, "bitacora.py"), "run", os.path.join(T, "canon.py"),
                    os.path.join(D, "takeoff_canon_RFI16_metal.json"), os.path.join(D, "out")], cwd=K, env=env,
                   capture_output=True, text=True)
if p.returncode != 0:
    print(p.stdout[-3000:], p.stderr[-3000:])
    sys.exit("canon.py failed on the RFI-16 copy")
fb = json.load(open(os.path.join(C4, "out", "familias_out.json")))["familias"]
fa = json.load(open(os.path.join(D, "out", "familias_out.json")))["familias"]
delta = {k: round(fa.get(k, 0) - fb.get(k, 0), 2) for k in sorted(set(fa) | set(fb)) if abs(fa.get(k, 0) - fb.get(k, 0)) > 0.005}
lf_tipo = {}
for r in runs:
    lf_tipo[r["type"]] = round(lf_tipo.get(r["type"], 0) + r["lf"], 3)
lf_size = {}
for r in runs:
    lf_size[STUD[r["type"]]] = round(lf_size.get(STUD[r["type"]], 0) + r["lf"], 2)
# track per stud size = run LF x 1 (bottom) and x 1 (top), the rule canon.py applied (bottom / top = 1 x LF per run)
track_size = {k: {"bottom": v, "top": v} for k, v in lf_size.items()}
out = {"runs": runs, "wall_lf_by_type": lf_tipo, "wall_lf_by_stud_size": lf_size, "track_by_stud_size": track_size, "wall_lf_total": round(sum(lf_tipo.values()), 3),
       "framing_height_ft": 10.667, "delta_familias": delta}
json.dump(out, open(os.path.join(D, "rfi16_delta.json"), "w"), indent=1, ensure_ascii=False)
for r in runs:
    print(r["id"], r["type"], r["ori"], r["lf"], r["from"])
print("LF by type", lf_tipo, "total", out["wall_lf_total"])
print("LF by stud size", lf_size)
print("DELTA", json.dumps(delta, indent=1))
