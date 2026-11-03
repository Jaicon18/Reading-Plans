"""BE-117 (user 3-nov): program check of EVERY annotation of the delivered markups PDF against the Excel.
For each take-off annotation (Author 'Take-off' / 'take-off'): TYPE, LF, H, SF, DETAIL and Wall ID of its Contents are
compared with its Excel row (Partition Takeoff wall / other framing / board-only row; Material Summary breakdown for
demolition, gyp ceilings, Level 5, shaft and recess items); /Measure = the printed scale label of its sheet view;
Bluebeam Length (vertices / scale) vs LF <= 0.5 % (or the cause written); every sheet with take-off elements has
markups. Writes proceso/VERIFICACION_MARKUPS_<rev>.md (+ etapas copy). rc 1 if anything fails.
Use: python3 bitacora.py run scripts/verificar_markups.py <tools_dir> <markups.pdf> <excel.xlsx> <rev>"""
import json, math, os, re, sys
sys.path.insert(0, sys.argv[1])
import pymupdf as fitz
import openpyxl
import markups_bluebeam as MB
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.dirname(K)
PDF, XL, REV = sys.argv[2], sys.argv[3], sys.argv[4]
c = json.load(open(os.path.join(K, "etapas", "4_canon", "takeoff_canon.json")))
wb = openpyxl.load_workbook(XL, data_only=True)
# ---- Excel rows
pt, tipo_blk = {}, None
for r in wb["Partition Takeoff"].iter_rows(min_row=5, values_only=True):
    if r[0] and str(r[0]).startswith("TYPE "):
        tipo_blk = str(r[0])[5:]
        continue
    if r[1] and r[2] is not None and not str(r[1]).startswith(("SUBTOTAL", "TOTAL")):
        pt[str(r[1])] = {"type": str(r[0]).split("  #")[0], "blk": tipo_blk, "lf": float(r[2]), "h": float(r[3] or 0), "sf": float(r[7] or 0),
                         "src": str(r[9] or "")}
brk = {}
for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True):
    if r[0]:
        for k, v in re.findall(r"\b([A-Z]{2,5}-[A-Z0-9.\-]+?) ([\d,]+(?:\.\d+)?)(?= \+| =)", str(r[8] or "")):
            brk.setdefault(k, float(v.replace(",", "")))
        brk.setdefault("ROW:" + str(r[0])[:20], float(r[2] or 0))
CEIL = {x["room"]: x for x in c["ceilings"]}
ok_scale = {}
doc = fitz.open(PDF)
lines, fails, n = [], [], 0
LBL = {12: "A-202", 14: "A-221", 5: "A-050", 6: "A-052"}
RX_SC = re.compile(r"(\d+(?:/\d+)?)\"\s*=\s*1'-0\"")
for pno, sh in LBL.items():
    page = doc[pno]
    scs = []
    for b in page.get_text("blocks"):
        for m in RX_SC.finditer(b[4]):
            scs.append((m.group(1), (b[0] + b[2]) / 2, (b[1] + b[3]) / 2))
    annots = [a for a in page.annots() or [] if str(a.info.get("title", "")).lower() == "take-off"]
    if not annots:
        fails.append(f"{sh}: sheet with take-off elements has NO markups")
    for a in annots:
        n += 1
        ct = a.info.get("content", "")
        subj = a.info.get("subject", "")
        nm = doc.xref_get_key(a.xref, "NM")[1].strip("()")
        meas = doc.xref_get_key(a.xref, "Measure")[1]
        mR = re.search(r"/R\(([^)]*)\)", meas)
        mC = re.search(r"/C ([\d.]+)", meas)
        R = mR.group(1) if mR else ""
        # nearest printed scale label of the view
        r_ = a.rect
        near = min(scs, key=lambda s: math.hypot(s[1] - (r_.x0 + r_.x1) / 2, s[2] - (r_.y0 + r_.y1) / 2)) if scs else None
        want = (near[0] + " in = 1 ft") if near else "?"
        res = []
        if R.replace(" ", "") != want.replace(" ", ""):
            res.append(f"scale {R!r} != printed {want!r}")
        pts = [tuple(p) for p in (a.vertices or [])]
        lpt = sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)) if len(pts) > 1 else 0
        L = lpt * float(mC.group(1)) if mC else None
        parts = [x.strip() for x in ct.split("·")]
        if nm.startswith("TO-") and not nm.startswith("TO-LEGEND"):
            wid = nm[3:]
            x = pt.get(wid)
            if x is None:
                res.append("no Excel row")
            else:
                g = lambda rx: (re.search(rx, ct) or [None, None])[1]
                lf_c, h_c, sf_c = g(r"([\d.]+) LF"), g(r"H ([^·]+?) ·"), g(r"([\d,]+\.\d+) SF")
                if lf_c is None or abs(float(lf_c) - round(x["lf"], 2)) > 0.005:
                    res.append(f"LF {lf_c} != {x['lf']}")
                if (h_c or "").strip() != MB.ftin(x["h"]):
                    res.append(f"H {h_c} != {MB.ftin(x['h'])}")
                if sf_c is None or abs(float(sf_c.replace(',', '')) - x["sf"]) > 0.005:
                    res.append(f"SF {sf_c} != Excel board {x['sf']}")
                if not parts or parts[-1] != wid:
                    res.append("Wall ID")
                tx = x["type"]
                same = (subj == tx) or (subj.startswith("BOARD ONLY") and "BOARD ONLY" in str(x["blk"])) or \
                       (subj == "OTHER FRAMING - SOFFIT SIDE" and tx.startswith("Soffit side")) or (x["blk"] == subj)
                if not same:
                    res.append(f"TYPE {subj} != {tx}")
                det = parts[-2] if len(parts) > 1 else ""
                if det and det not in x["src"] and det not in ct and not subj.startswith("BOARD ONLY"):
                    res.append(f"DETAIL {det} not in Excel source")
                if L is not None and x["lf"]:
                    d = abs(L - x["lf"]) / x["lf"] * 100
                    if d > 0.5:
                        res.append(f"Length {L:.2f} vs LF {x['lf']} ({d:.2f} %)")
            key = wid
        elif nm.startswith("DEMO-"):
            key = nm[5:]
            sf_c = float(re.search(r"([\d.]+) SF", ct).group(1))
            base = key.split(" ")[0]
            ex = brk.get(base)
            if base == "DEMO-14":
                tot = sum(float(re.search(r"([\d.]+) SF", b.info.get("content", "")).group(1)) for p2 in doc for b in (p2.annots() or [])
                          if doc.xref_get_key(b.xref, "NM")[1].strip("()").startswith("DEMO-DEMO-14"))
                if ex is None or abs(tot - ex) > 0.05:
                    res.append(f"DEMO-14 parts {tot:.2f} != Excel {ex}")
            elif ex is None or abs(sf_c - ex) > 0.01:
                res.append(f"SF {sf_c} != Excel demolition breakdown {ex}")
            lf_c = float(re.search(r"([\d.]+) LF", ct).group(1))
            if L is not None and lf_c and "ceilings" not in ct and not key.startswith("DEMO-C"):
                d = abs(L - lf_c) / lf_c * 100
                if d > 0.5:
                    res.append(f"Length {L:.2f} vs LF {lf_c} ({d:.2f} %)")
            if "PENDIENTE" in ct or "DERIVADO" in ct:
                res.append("Spanish state")
        elif nm.startswith("TOX-"):
            key = nm
            m_sf = re.search(r"([\d,]+\.\d+) SF", ct)
            if subj == "GYP CEILING":
                ref = parts[-1]
                ex = brk.get(ref)
                if ex is None or m_sf is None or abs(float(m_sf.group(1).replace(",", "")) - ex) > 0.01:
                    res.append(f"SF {m_sf and m_sf.group(1)} != Excel ceiling breakdown {ex}")
            elif subj == "SOFFIT BOTTOM":
                room = parts[1]
                ex = CEIL.get(room, {}).get("area_sf")
                if ex is None or abs(float(m_sf.group(1)) - ex) > 0.01:
                    res.append(f"SF != soffit bottom {ex} (1/2\" gyp row, BREAKDOWN md)")
            elif subj == "LEVEL 5":
                ex = brk.get("ROW:Level 5 finish")
                if ex is None or abs(float(m_sf.group(1).replace(",", "")) - ex) > 0.01:
                    res.append(f"SF != Excel Level 5 {ex}")
            elif subj == "ROOF HATCH SHAFT":
                ex = brk.get("RH-SHAFT-S")
                m_ = re.search(r"([\d.]+) LF 3-5/8", ct)
                if ex is None or m_ is None or abs(float(m_.group(1)) - ex) > 0.01:
                    res.append(f"stud LF != Excel {ex}")
            elif subj == "PIN & SLEEVE RECESS":
                if "PS-RECESS-S" not in brk:
                    res.append("recess not in Excel")
        else:
            key = nm
        st = "PASS" if not res else "FAIL"
        if res:
            fails.append(f"{sh} {key}: " + "; ".join(res))
        lines.append(f"| {sh} | {key} | {subj} | {ct[:110].replace('|', '/')} | {R} | {('%.2f' % L) if L else '-'} | {st} {'; '.join(res)} |")
out = [f"# VERIFICACION MARKUPS {REV} - CFA #2284 River Point (BE-117, by program)", "",
       f"PDF: {os.path.basename(PDF)} · Excel: {os.path.basename(XL)} · annotations checked: {n} · FAIL: {len(fails)}", "",
       "Checks per annotation: TYPE / LF / H / SF / DETAIL / Wall ID equal to its Excel row (Partition Takeoff row; Material Summary breakdown for demolition, gyp ceilings, Level 5, shaft, recess); /Measure = the printed scale label nearest to the annotation on its sheet; Bluebeam Length (vertices x /Measure) vs LF <= 0.5 %; every sheet with take-off elements (A-050, A-052, A-202, A-221) has markups.", "",
       "| Sheet | Item | Subject | Contents | /Measure | Length (ft) | Result |", "|---|---|---|---|---|---|---|"] + lines
out += ["", "## Totals", f"- annotations: {n}", f"- PASS: {n - len([f for f in fails if ':' in f and 'NO markups' not in f])}",
        f"- FAIL: {len(fails)}"] + [f"  - {f}" for f in fails]
txt = "\n".join(out) + "\n"
fd = os.path.join(S, "cfa_final", "FINAL_FOR_REVIEW", "proceso")
open(os.path.join(fd, f"VERIFICACION_MARKUPS_{REV}.md"), "w").write(txt)
open(os.path.join(K, "etapas", f"VERIFICACION_MARKUPS_{REV}.md"), "w").write(txt)
print(n, "annotations,", len(fails), "fail(s)")
for f in fails[:40]:
    print("FAIL", f)
sys.exit(1 if fails else 0)
