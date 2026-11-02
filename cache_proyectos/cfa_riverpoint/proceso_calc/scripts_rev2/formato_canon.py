"""Input-format fixes of the reconciled canon demanded by the gates (no quantity changes):
 - R72.6 faces[].side N/S/E/W/out -> A (north or west) / B (south or east), outward direction of each soffit side
   from its position in the A-221 L / box (resolucion.md section 2);
 - R70.3 gaps_ok between M3.5-01 and M3.5-02: the 10.083 ft between them is the existing kitchen wall with board only
   (EX-KIT-02, A-202 path 816-998 pt), no M3.5 sister there (A-202 tags only at hoods #2 / #3, A2/A-605);
 - E23 rfis[].delta = the delta of each alternative (A / B) already written in rfis[].opciones; RFI-16 with the program
   delta of etapas/4_canon/rfi16/rfi16_delta.json.
Use: python3 bitacora.py run scripts/formato_canon.py"""
import json, os
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C4 = os.path.join(K, "etapas", "4_canon")
P = os.path.join(C4, "takeoff_canon.json")
c = json.load(open(P))
SIDE = {"N": "A", "W": "A", "S": "B", "E": "B"}
OUT = {"SS-SRV-W": "A", "SS-SRV-N": "A", "SS-SRV-IV": "B", "SS-SRV-IH": "B",
       "SS-GT-N": "A", "SS-GT-S": "B", "SS-GT-W": "A", "SS-GT-E": "B"}
n = 0
for w in c["walls"]:
    for f in w.get("faces") or []:
        s = f.get("side")
        if s in ("A", "B", "END"):
            continue
        new = OUT[w["id"]] if s == "out" else SIDE[s]
        f["side_info"] = f"read as '{s}' (" + ("outward face of the soffit side, A-221" if s == "out" else "compass side") + ")"
        f["side"] = new
        n += 1
if not any(set(g.get("between") or []) == {"M3.5-01", "M3.5-02"} for g in c.get("gaps_ok") or []):
    c.setdefault("gaps_ok", []).append({"between": ["M3.5-01", "M3.5-02"],
        "reason": "existing kitchen wall between hood #2 and hood #3: no M3.5 tag / sister framing there (A-202 tags PT0003 / "
                  "PT0004 only at the hoods, A2/A-605 at the hoods); only its 1/2\" cement board base is new (board-only entry "
                  "EX-KIT-02, A-202 path 816-998 pt = 10.083 LF, KN16)",
        "source": "A-202 + A2/A-605 + EX-KIT-02"})
    n += 1
r16 = json.load(open(os.path.join(C4, "rfi16", "rfi16_delta.json")))
d16, lfs = r16["delta_familias"], r16["wall_lf_by_stud_size"]
s36 = '3-5/8"'
prog = (f"computed by program (the take-off calculation program re-run on a copy of the reconciled take-off data with the new interior W4 / W4.1 / W6 / W8 walls as metal "
        f"studs @ 16\"): {r16['wall_lf_total']:.2f} LF of wall -> +{d16.get(s36 + ' stud (todos los gauges)', 0):.2f} LF 3-5/8\" "
        f"studs, +{d16.get('8\" stud (todos los gauges)', 0):.2f} LF 8\" studs, +{lfs.get(s36, 0):.2f} LF bottom + "
        f"{lfs.get(s36, 0):.2f} LF top 3-5/8\" track, +{lfs.get('8\"', 0):.2f} LF bottom + {lfs.get('8\"', 0):.2f} LF top 8\" "
        f"track, +{d16.get('bracing C.R. channel', 0):.2f} LF bracing C.R. channel")
for r in c["rfis"]:
    o = r.get("opciones") or {}
    if r["id"] == "RFI-16":
        o["A"]["delta"] = "0 (loaded as wood, board-only); metal alternative: " + prog
    r["delta"] = f"A: {(o.get('A') or {}).get('delta', 'n/a')} | B: {(o.get('B') or {}).get('delta', 'n/a')}"
    n += 1
# R80e.84: no internal file names in text that reaches the client's sheets: path -> 'crop <stem>' (+ img_refs keeps the file)
import re
RXF = re.compile(r"(?:etapas/)?(?:[\w.-]+/)*([\w.-]+)\.png")
IMGK = {"img", "height_img", "detail_img", "stud_img", "img_refs"}
for k in ("walls", "existing_walls", "misc_items"):
    for e in c[k]:
        for f in list(e):
            v = e[f]
            if f not in IMGK and isinstance(v, str) and RXF.search(v):
                e.setdefault("img_refs", []).extend(m.group(0) for m in RXF.finditer(v))
                e[f] = RXF.sub(lambda m: "crop " + m.group(1), v)
                n += 1
RXC = [(re.compile(r"crop [\w.-]+"), "resolution crop"), (re.compile(r"\bPT\d{4}\b"), "tag")]
for k in ("walls", "existing_walls", "misc_items", "rfis"):
    for e in c[k]:
        for f in list(e):
            v = e[f]
            if f not in IMGK | {"id", "tag_ids", "tag", "ref"} and isinstance(v, str):
                s2 = v
                for rx, t in RXC:
                    s2 = rx.sub(t, s2)
                if s2 != v:
                    e[f] = s2; n += 1
# trazabilidad cites N/SHEET bubbles only: the dropped gyp ceilings carry the S-241 plan bubble / schedule they come from
CLGS = {"CLG-ENTA-B": "C3/S-241", "CLG-ENTB-B": "C3/S-241", "CLG-MEN-B": "C3/S-241", "CLG-WOM-B": "C3/S-241",
        "CLG-PLAY-B": "A2/S-241 (framing assumed, RFI-07)"}
for m in c["misc_items"]:
    if m["ref"] in CLGS and "/S-241" not in m["source"]:
        m["source"] += "; framing per " + CLGS[m["ref"]] + " dropped ceiling plan / LGS ceiling joist schedule"
        n += 1
an = {x["familia"] for x in c.get("accesorios_none") or []}
for fam, why, src in (("additional head track", "no opening in our metal walls (M2.1 / M3.5 / MB-01 have no door or window: A-202, A-801 door schedule)", "A-202 + A-801"),
                      ("2-1/2\" CFMF coiling grille head", "no coiling grille in the set (A-801 door schedule, A-201 / A-202)", "A-801 + A-202")):
    if fam not in an:
        c.setdefault("accesorios_none", []).append({"familia": fam, "why": why, "source": src}); n += 1
json.dump(c, open(P, "w"), indent=1, ensure_ascii=False)
print("format fields:", n)
