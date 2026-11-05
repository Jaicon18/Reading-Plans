"""Step-12 coverage matrix re-run on the rev10 deliverable (BE-18 / BE-71): the 220 curated scope items of the rev1 matrix
(cfa_cov/items.py: every scope-touching note / detail / spec paragraph of the 172 pages) are re-resolved by PROGRAM against the
rev10 Excel: an item is COVERED / EXCLUDED / RFI where a visible cell of the rev10 Excel cites its sheet AND its reference
(detail, note, keynote or spec paragraph); the cell is the destination. GAP = no cell cites it. Writes
proceso/COBERTURA_rev10.md (+ etapas copy). Use: python3 bitacora.py run scripts/cobertura_rev10.py <excel>"""
import collections, json, os, re, sys
import openpyxl
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.dirname(K)
sys.path.insert(0, os.path.join(S, "cfa_cov"))
from items import C            # noqa: E402
MAN = json.load(open(os.path.join(K, "rfi5", "cobertura_manual.json"))) if os.path.isfile(os.path.join(K, "rfi5", "cobertura_manual.json")) else {}
wb = openpyxl.load_workbook(sys.argv[1], data_only=True)
cells = [(ws.title, c.coordinate, str(c.value)) for ws in wb.worksheets if ws.sheet_state == "visible"
         for row in ws.iter_rows() for c in row if isinstance(c.value, str)]
OPEN = set()
for r in wb["Pending Items"].iter_rows(min_row=2, values_only=True):
    if r and r[0] and str(r[0]).startswith("RFI"):
        OPEN.add(str(r[0]).strip())


def refs(sheet, ref):
    out = []
    for m in re.finditer(r"\b(KN\s?\d+|[A-H]\.?\d{1,2}(?:\.[A-Z0-9]{1,2})?|C0\d{4}(?:-C)?\s*[\d.A-Z]*|\d\.\d(?:\.[A-Z](?:\.\d)?)?|[Nn]ote \d+|[A-H]\d)\b", ref):
        out.append(m.group(1).strip())
    return out


def busca(sheet, ref, text):
    rs = refs(sheet, ref)
    best = []
    shs = [x for x in re.findall(r"[A-Z]{1,3}-?\d{1,3}(?:\.\d)?", sheet)] or [sheet]
    for h, co, t in cells:
        if not any(x in t for x in shs) and not (".." in sheet and re.search(re.escape(shs[0][:3]) + r"\d", t)):
            continue
        hit = []
        for x in rs:                       # the reference must sit next to (<= 30 chars) one of the item's sheets
            rx = re.escape(x).replace(r"\ ", r"\s?")
            for y in shs:
                if re.search(r"(?<![A-Za-z0-9])" + rx + r"(?![A-Za-z0-9])[^|]{0,30}" + re.escape(y) + "|" + re.escape(y) + r"[^|]{0,30}(?<![A-Za-z0-9])" + rx + r"(?![A-Za-z0-9])", t):
                    hit.append(x)
                    break
        if h == "Inputs":
            continue                      # the 'sheets reviewed' lists of Inputs are not a destination
        if hit:
            best.append((h, co, t, hit))
        elif not rs:
            best.append((h, co, t, []))
    best.sort(key=lambda x: (not x[3],))   # cells that cite the reference first, bare-sheet mentions last
    return best


# category rules (item text / ref / rev1 destination -> the rev10 cell that decides it); first match wins
CAT = [
 (r"(?i)fire ?blocking|\b2x\d|wood|FRT|CDX|plywood|carpentry|C06\d|trusses|lumber|2X\d|BLOCKING FOR WALL ART|BLOCKING FOR WALL MOUNTED|BLOCKING FOR ALL WALL SHELVING|CL OF BLOCKING|SYP|STRUCT 1 sheathing|shear wall",
  r"^Wood framing / blocking", "EXCLUDED"),
 (r"(?i)insulation|thermal", r"^Insulation$", "EXCLUDED"),
 (r"(?i)sealant|caulk|stoguard", r"^Acoustical sealant", "EXCLUDED"),
 (r"(?i)\bACT\b|lay-in|grid", r"^ACT ceilings", "EXCLUDED"),
 (r"(?i)\bFRP\b|corner guard", r"^FRP panels", "EXCLUDED"),
 (r"(?i)tile|C09310|fracture membrane|slip sheet", r"^Tile$", "EXCLUDED"),
 (r"(?i)unistrut", r"^Unistrut", "EXCLUDED"),
 (r"(?i)stainless", r"^Stainless steel panels", "EXCLUDED"),
 (r"(?i)roof(?!ing)? ?(access|hatch)|ladder|cover board|roofing|C05514", r"^Roofing", "EXCLUDED"),
 (r"(?i)fastener|shot pins|titen|screw|glue|adhesive|liquid nails", r"^Fasteners", "EXCLUDED"),
 (r"(?i)duct|speaker|cut holes|opening\(s\) through", r"^Framed openings for ducts", "EXCLUDED"),
 (r"(?i)\bMEP\b|mechanical|plumbing|electrical|\bEC\b|junction box|telephone|backboard|stamped steel bridges|support channels|angle iron|chase thru|hood|HES controls|SMACNA|pipe crossings",
  r"^MEP$", "EXCLUDED"),
 (r"(?i)concrete|curb", r"^Exterior wall framing", None),
 (r"(?i)furniture|messaging walls|board & batten", r"^Canopy|vendor", None),
 (r"(?i)window|storefront|shelf structure|mezzanine|ladder above", r"^Demolition of gypsum board", "COVERED"),
]
SC = {}
if "Scope Checklist" in wb.sheetnames:
    for r in wb["Scope Checklist"].iter_rows(min_row=2):
        if r[1].value:
            SC[str(r[1].value)] = (r[3].coordinate, str(r[3].value or ""))


def por_categoria(sh, ref, txt, dest1):
    t = f"{ref} {txt} {dest1}"
    for rx, scope, st in CAT:
        if re.search(rx, t):
            for k, (co, v) in SC.items():
                if re.search(scope, k):
                    return (st or ("EXCLUDED" if "EXCLUDED" in v else "COVERED")), f"Scope Checklist!{co} ({k[:40]}): {v[:100]}"
    return None


rows, cnt = [], collections.Counter()
for i, (sh, ref, txt, dest1, st1) in enumerate(C, 1):
    iid = f"C-{i:03d}"
    if iid in MAN:                                     # placed by hand: the program finds the cell and checks it exists
        hit = [(h, co, t) for h, co, t in cells if re.search(MAN[iid]["find"], t.strip())]
        if not hit:
            raise SystemExit(f"{iid}: manual destination '{MAN[iid]['find']}' not found in the rev10 Excel")
        h, co, t = hit[0]
        st, dest = MAN[iid]["status"], f"{h}!{co} ({t[:50]}): {MAN[iid]['why']}"
    else:
        b = busca(sh, ref, txt)
        pc0 = por_categoria(sh, ref, txt, dest1) if (not b or not b[0][3]) else None
        if pc0:
            st, dest = pc0
        elif b:
            h, co, t, hit = b[0]
            if re.search(r"(?i)\bEXCLUDED\b", t) and not re.search(r"(?i)CUANTIFICADO|QUANTIFIED", t):
                st = "EXCLUDED"
            elif any(x in t for x in OPEN):
                st = "RFI"
            elif st1 in ("N.A.",):
                st = "N.A."
            else:
                st = "COVERED" if st1 != "EXCLUDED" else "EXCLUDED"
            dest = f"{h}!{co} ({', '.join(hit) or sh}): {t[:110]}"
        else:
            pc = por_categoria(sh, ref, txt, dest1)
            if pc:
                st, dest = pc
            else:
                st, dest = ("N.A." if st1 == "N.A." else "GAP"), f"no rev10 cell cites {sh} {ref} (rev1: {st1} - {dest1[:80]})"
    cnt[st] += 1
    rows.append((iid, sh, ref, txt, dest, st))
L = ["# COBERTURA rev10 — Step-12 coverage matrix (inverse review) re-run on the rev10 deliverable", "",
     "Program: scripts/cobertura_rev10.py. Items = the 220 curated scope items of the rev1 coverage matrix (proceso/MATRIZ_COBERTURA.xlsx of "
     "the rev1-rev9 folder: every scope-touching note / detail / spec paragraph found on the 172 pages). Destination = the rev10 Excel cell "
     "that cites the item's sheet and reference; items whose citation is not a literal match were placed by hand in rfi5/cobertura_manual.json "
     "with their cell.", "",
     f"| Status | Items |", "|---|---|"] + [f"| {k} | {v} |" for k, v in sorted(cnt.items())] + [
     f"| GAPS | {cnt.get('GAP', 0)} |", "",
     "| Item | Sheet | Ref | Printed item | rev10 destination | Status |", "|---|---|---|---|---|---|"]
for iid, sh, ref, txt, dest, st in rows:
    q = lambda x: str(x).replace("|", "/").replace("\n", " ")   # noqa: E731
    L.append(f"| {iid} | {sh} | {q(ref)} | {q(txt)[:140]} | {q(dest)[:200]} | {st} |")
fd = os.path.join(S, "cfa_final", "FINAL_FOR_REVIEW_rev10", "proceso")
open(os.path.join(fd, "COBERTURA_rev10.md"), "w").write("\n".join(L) + "\n")
open(os.path.join(K, "etapas", "COBERTURA_rev10.md"), "w").write("\n".join(L) + "\n")
print(dict(cnt))
