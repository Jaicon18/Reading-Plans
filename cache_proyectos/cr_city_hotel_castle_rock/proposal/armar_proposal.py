"""CR City Hotel proposal (take-off rev18 FINAL quantities, no new take-off pass), from the user's "Proposal Template.xlsx"
(rule U-150): sheet PROPOSAL DW (JC Hunter letterhead) + PRICING (material FBM / labor and OH with the template's own rates,
live formulas) + FBM_PRICES (every FBM product used: SKU, name, price, unit, stock, link, date, branch).
Model: consumer_cellular_centennial/proposal_calc/armar_proposal.py (approved rev4 FINAL).
Rates not in the template -> "[RATE TO CONFIRM]" (0 in the totals, listed); FBM SKU not found -> "[PRICE TO CONFIRM]".
WOOD-framed project: wood studs / blocking / sheathing = Div. 06 EXCLUDED; fasteners EXCLUDED (U-053).
Usage: armar_proposal.py <template.xlsx> <takeoff.xlsx> <canon.json> <fbm_dir> <out.xlsx>"""
import datetime, glob, json, math, re, sys
import openpyxl
REVN = "rev18"
from openpyxl.styles import Alignment, Font, PatternFill

TPL, TK, CN, FBM, OUT = sys.argv[1:6]
wbt = openpyxl.load_workbook(TK, data_only=True)
can = json.load(open(CN))
ms = [r for r in wbt["Material Summary"].iter_rows(min_row=4, values_only=True) if r[0] and isinstance(r[2], (int, float))]
scope = [r for r in wbt["Scope Checklist"].iter_rows(min_row=2, values_only=True) if r[0]]
MS = {r[0]: r for r in ms}
fbm, fecha = {}, None
for f in sorted(glob.glob(f"{FBM}/*.json")):
    d = json.load(open(f))
    fecha = d["fecha"]
    for r in d["rows"]:
        fbm.setdefault(r["code"], dict(r, cat=d["category"]))


def key(prefix):
    """Material Summary row name that starts with prefix (exactly one)."""
    if prefix in MS:
        return prefix
    k = [n for n in MS if n.startswith(prefix)]
    if len(k) != 1:
        sys.exit(f"Material Summary row '{prefix}' found {len(k)} times")
    return k[0]


def nsheet(txt, cap=6):
    m = re.search(r"N/SHEET:\s*([^|]+)", str(txt or ""))
    if not m:
        return ""
    s = [x.strip() for x in m.group(1).split(",") if x.strip()]
    return ", ".join(s[:cap]) + (f" (+{len(s) - cap} more)" if len(s) > cap else "")


def net(prefix):
    return float(MS[key(prefix)][2] or 0)


def buy(prefix):
    r = MS[key(prefix)]
    return float(r[5] if isinstance(r[5], (int, float)) else r[2])   # purchase = net + waste of the take-off Inputs


def pcs(prefix):
    return float(MS[key(prefix)][7] or 0)                          # pieces to buy (Material Summary col H)


K = {  # Material Summary rows of this project (prefix -> exact name resolved at run time)
    "trk": "Ceiling / soffit track", "wire": "Hanger wire", "X": '5/8" gypsum board, Type X', "WR": '5/8" gypsum board, Type X W.R.',
    "main": "USG drywall suspension main tee", "cross": "USG drywall suspension cross tee", "ang": "USG angle molding",
    "cem": '5/8" cement board', "rc": "Resilient channel", "cb": "METAL trim", "cj": "Control joint",
    "C": '5/8" gypsum board, Type C', "sl": '1" gypsum shaftliner', "ext": '5/8" exterior gypsum sheathing',
    "ch": 'C-H stud 6"', "jr": 'J-runner 6"', "mud": "Joint compound", "tape": "Joint tape",
    "ch25": 'C-H stud 2-1/2"', "jr25": 'J-runner 2-1/2"', "cc": "Carrying channel",
}
KX = {k: key(v) for k, v in K.items()}
board_all = sum(net(K[k]) for k in ("X", "WR", "C", "sl", "ext", "cem"))      # every board SF (template 'Drywall finish' D25)
board_fin = sum(net(K[k]) for k in ("X", "WR", "C"))                          # finished board (Level 4) = MS compound / tape driver
# drywall grid ceiling area (GYP-1 / GYP-2) = the SF in the canon main tee ops ("165.3 SF / 4.0 ft o.c. = 41.33"),
# the same items that make the Material Summary main tee row (the MS source text is truncated)
_mt = [x for x in can["misc_items"] if "main tee" in x["familia"].lower()]
grid_sf = round(sum(float(re.match(r"\s*([\d,.]+) SF", x["op"]).group(1).replace(",", "")) for x in _mt), 2)
if abs(sum(x["qty"] for x in _mt) - net(K["main"])) > 0.5:
    sys.exit("canon main tee items do not add up to the Material Summary main tee row")
rc_sf = round(sum(c["area_sf"] for c in can["ceilings"] if c.get("system") == "resilient_channel"), 2)

# ---------------------------------------------------------------------------------------------- material lines
# (section, description, quantity, unit, FBM code or None, units of the FBM price per quantity unit, note)
# BASE_ products: FBM price = 10 ft piece ($/MLF / 100, precios-materiales-fbm) -> $/LF = price x 0.1
L = [  # M = metal framing / ceiling suspension, D = drywall & finish Level 4
 ("M", '6" C-H stud 20 GA, L1 / L4 chase CH.6 (1/A7.50) @ 24" o.c. (A0.06 CH, UL U415)', buy(K["ch"]), "LF", "BASE_SW600CH-33", 0.1, "A0.06 CH, 1/A7.50"),
 ("M", '6" J-runner 20 GA, chase top / bottom (A0.06 CH)', buy(K["jr"]), "LF", "BASE_TJ600-33", 0.1, "A0.06 CH, 1/A7.50"),
 ("M", '2-1/2" C-H stud 20 GA, L2-L4 north / south shafts @ 24" o.c. (7/A9.03, 8/A9.03 4 3/4" 2-HOUR SHAFTWALL W419 / U497)', buy(K["ch25"]), "LF", None, None, "7/A9.03, 8/A9.03 - 2-1/2\" C-H SKU to confirm at FBM"),
 ("M", '2-1/2" J-runner 20 GA, L2-L4 shafts top / bottom (7/A9.03, 8/A9.03)', buy(K["jr25"]), "LF", None, None, "7/A9.03, 8/A9.03 - 2-1/2\" J-runner SKU to confirm at FBM"),
 ("M", 'Carrying channel 1-1/2" cold-rolled, GYP-2 / MB-1 ceilings (A0.08 MB-1)', buy(K["cc"]), "LF", None, None, "A0.08 MB-1 - carrying channel SKU to confirm at FBM"),
 ("M", 'Ceiling / soffit track at corridor bands, lobby coffers, L4 stair soffit (7/A7.23, 2/A7.31, 11/A6.01)', buy(K["trk"]), "LF", None, None,
  "7/A7.23, 2/A7.31 - track size not printed on the soffit details"),
 ("M", 'Resilient channel 1/2" deep (RC-1, 12 ft), FS-1 / RS-1 ceilings @ 16" o.c. (A0.08, 09 22 16)', buy(K["rc"]), "LF", "RC125P-12", 1 / 12, "A0.08 FS-1 / RS-1"),
 ("M", 'USG drywall suspension main tee DGLW26 12 ft (GYP-1 / GYP-2)', pcs(K["main"]), "PCS", "CGUDGLW26", 1 / 16, "A3.01-A3.04, A7.23"),
 ("M", 'USG drywall suspension cross tee DGLW424 4 ft', pcs(K["cross"]), "PCS", "CGUDGLW424", 1 / 48, "A3.01-A3.04, A7.23"),
 ("M", 'USG angle molding DGWM24 12 ft', buy(K["ang"]), "LF", None, None, "A3.01-A3.04 - USG DGWM24 not listed at FBM"),
 ("M", 'Hanger wire 8 ga (0.162" dia., 09 22 16 2.2.C)', buy(K["wire"]), "LF", None, None, "09 22 16 2.2.C - hanger wire not listed at FBM"),
 ("D", '5/8" Type X gypsum board 4x12 (A0.06 / A0.07 / A0.08 per type and rating)', buy(K["X"]), "SF", "D58F12-U", 1 / 48, "A0.06, A0.07"),
 ("D", '5/8" Type X W.R. (moisture / mold resistant) gypsum board 4x12 (A0.06 GN 11 / 12)', buy(K["WR"]), "SF", "D58MM12-U", 1 / 48, "A0.06 GN 11"),
 ("D", '5/8" Type C gypsum board 4x12, FS-1 ceilings (A0.08, UL L546)', buy(K["C"]), "SF", "D58C12-GE", 1 / 48, "A0.08 FS-1"),
 ("D", '1" Type X shaftliner 2x12 (CH.6-2, UL U415)', buy(K["sl"]), "SF", "D1SLMM12-U", 1 / 24, "A0.06 CH, A9.03"),
 ("D", '5/8" Type X glass-mat gypsum sheathing 4x8, ASTM C1177 (06 16 00 2.5.B; A0.07 XW rows)', buy(K["ext"]), "SF", None, None, "06 16 00 2.5.B glass-mat C1177 - FBM D58GS08-GE is a paper-faced sheathing panel, glass-mat SKU to confirm"),
 ("D", '5/8" cement board (Durock) 4x8 at guest bath tile walls (A0.06 GN 13, 09 29 00 2.4)', buy(K["cem"]), "SF", "DCB5808-U", 1 / 32, "A0.06 GN 13"),
 ("D", 'Metal corner bead 10 ft (09 29 00 2.5)', buy(K["cb"]), "LF", "DWB10-60", 0.1, "A2.01-A2.04"),
 ("D", 'Control joint 093 zinc 10 ft (A0.06 GN 15, ASTM C840)', buy(K["cj"]), "LF", "93EXP", 0.1, "A0.06 GN 15"),
 ("D", 'All-purpose joint compound (Material Summary LB: Level 4 exposed + Level 1 concealed layers, 09 29 00 3.6.E)', buy(K["mud"]), "LB", None, None, "Material Summary row (U-150) - price per LB / box weight to confirm"),
 ("D", 'Paper joint tape 500 ft roll', buy(K["tape"]), "LF", "DWT500W", 1 / 500, "Level 4"),
]
# ---------------------------------------------------------------------------------------------- labor (template rates)
LAB = [  # section, description, qty, unit, rate or None, rate source
 ("M", 'C-H shaft wall framing labor (wall SF = 1" shaftliner SF, one layer)', net(K["sl"]), "SF", 1.0,
  "Template 'Metal Framing' K25 6\" CH STUD 20 GA (1.00 / SF)"),
 ("M", 'Drywall grid ceiling labor GYP-1 / GYP-2 (ceiling SF x 1.15)', round(grid_sf * 1.15, 2), "SF", 1.0,
  "Template 'Metal Framing' K43 MAIN RUNNER (1.00 x ceiling SF x 1.15)"),
 ("M", 'Resilient channel install, FS-1 / RS-1 ceilings', net(K["rc"]), "LF", None,
  "template K39 '1/2\" RESILIANT CHANEL' = 4 with no labor formula (M39 empty) and no unit"),
 ("M", 'Ceiling / soffit track install (corridor bands, coffers, stair soffit)', net(K["trk"]), "LF", None, "not in the template"),
 ("D", 'Hanging 5/8" Type X board', net(K["X"]), "SF", 0.78, "Template 'Drywall finish' J8 5/8\" GYP BD X (0.78 / SF)"),
 ("D", 'Hanging 5/8" Type X W.R. board', net(K["WR"]), "SF", 0.5, "Template 'Drywall finish' J5 5/8\" GYP BD WR (0.50 / SF)"),
 ("D", 'Hanging 5/8" Type C ceiling board', net(K["C"]), "SF", 0.5, "Template 'Drywall finish' J22 5/8\" GYP BD (Ceiling) (0.50 / SF)"),
 ("D", 'Hanging 1" shaftliner', net(K["sl"]), "SF", 0.78, "Template 'Drywall finish' J11 1\" Shaft liner (0.78 / SF)"),
 ("D", 'Hanging 5/8" exterior gypsum sheathing', net(K["ext"]), "SF", 0.78, "Template 'Drywall finish' J7 5/8\" GYP BD EXT (0.78 / SF)"),
 ("D", 'Hanging 5/8" cement board', net(K["cem"]), "SF", 0.78, "Template 'Drywall finish' J13 5/8\" CEM BD (0.78 / SF)"),
 ("D", 'Level 4 finishing (joint tape + mud), finished board X + W.R. + Type C', board_fin, "SF", 0.5,
  "Template 'Drywall finish' J27 LABOUR FOR FINISHING (0.50 / SF)"),
 ("D", 'Corner bead and control joint install', net(K["cb"]) + net(K["cj"]), "LF", None, "not in the template"),
]
metal_lf = sum(net(K[k]) for k in ("trk", "ch", "jr"))
days_m = math.ceil(metal_lf / 300)
days_d = math.ceil(board_all / 1000)

# ---------------------------------------------------------------------------------------------- workbook
wb = openpyxl.load_workbook(TPL)
for ws in list(wb.worksheets):
    if ws.title != "PROPOSAL DW":
        wb.remove(ws)
P = wb["PROPOSAL DW"]; P.title = "PROPOSAL"; P.sheet_state = "visible"
for row in P.iter_rows():
    for c in row:
        if c.coordinate == "C3":
            continue
        if c.column > 11 or (c.value is not None and c.row >= 5):
            try:
                c.value = None
            except AttributeError:
                pass
BLUE, YEL = Font(color="0000FF"), PatternFill("solid", fgColor="FFF2CC")
B = wb.create_sheet("PRICING"); F = wb.create_sheet("FBM_PRICES")
F.append(["FBM code", "Product (as listed on myfbm.com)", "Category", "Price (USD)", "Price unit", "Min. order", "Stock", "Lead",
          "Link", "Read on", "Branch"])
used = []
B.append(["CR CITY HOTEL - CASTLE ROCK, CO - PRICING (quantities from Take-off rev18 FINAL; no new take-off pass) - INTERNAL, NOT FOR THE CLIENT"])
import os as _os
_d = '/root/cr/work/etapas/DELTA_rev17_rev18.md'      # rev4: delta de cantidades contra rev3 (orden COORDINACIÓN 7-nov)
if _os.path.exists(_d):
    _ls = [x for x in open(_d).read().split('\n') if x.startswith('| ') and not x.startswith('| Material') and not x.startswith('|---')]
    B.append([f"QUANTITY CHANGES vs the previous revision (take-off): " + ("; ".join(f"{x.split('|')[1].strip()} {x.split('|')[5].strip()} {x.split('|')[2].strip()}" for x in _ls) or "none")
              + " - see GUIA_DE_REVISION_DEL_ESTIMADOR.md for each change and its sheet"])
B.append(["Material: FBM myfbm.com visitor price (guest branch CO-086 Englewood / Denver area), read " + str(fecha) +
          "; contractor account price may differ. Labor / OH / markups: the user's Proposal Template rates (source per row)."])
B.append([])
hdr = ["Section", "Item", "Qty", "Unit", "FBM code", "FBM price", "FBM unit", "Units of price per qty", "Material $", "N/SHEET / note"]
sec_rows = {"M": [], "D": []}
B.append(["MATERIAL"]); B.append(hdr)
missing_sku = []
for s, dsc, q, u, code, k, nt in L:
    r = B.max_row + 1
    if code and code in fbm:
        p = fbm[code]
        if code not in [x[0] for x in used]:
            used.append((code, p))
        B.append([s, dsc, round(q, 2), u, code, p["price"], p["unitLabel"], k, f"=C{r}*F{r}*H{r}", nt])
        B[f"F{r}"].font = BLUE; B[f"E{r}"].font = BLUE
    else:
        missing_sku.append(f"{dsc} ({nt})")
        B.append([s, dsc, round(q, 2), u, "[PRICE TO CONFIRM]", None, None, None, 0, nt])
        B[f"E{r}"].fill = YEL
    sec_rows[s].append(r)
B.append([]); B.append(["LABOR (template rates)"]); B.append(["Section", "Item", "Qty", "Unit", "Rate", "Rate source", "", "", "Labor $"])
lab_rows = {"M": [], "D": []}
missing_rate = []
for s, dsc, q, u, rate, src in LAB:
    r = B.max_row + 1
    if rate is None:
        missing_rate.append(f"{dsc} ({src})")
        B.append([s, dsc, round(q, 2), u, "[RATE TO CONFIRM]", src, "", "", 0])
        B[f"E{r}"].fill = YEL
    else:
        B.append([s, dsc, round(q, 2), u, rate, src, "", "", f"=C{r}*E{r}"])
    lab_rows[s].append(r)
B.append([])
B.append(["SECTION BUILD-UP (template 'Metal Framing' / 'Drywall finish' rows 54-84 and 'PROPOSAL DW' col N 15% + round to 100)"])
B.append(["Line", "Metal framing & ceiling suspension", "Drywall & finish L4"])


def S(rows, col):
    return "+".join(f"{col}{x}" for x in rows) or "0"


base = B.max_row + 1
lines = [
 ("Material", f"={S(sec_rows['M'], 'I')}", f"={S(sec_rows['D'], 'I')}"),
 ("Material markup (template: metal 2% / drywall 5%)", f"=B{base}*0.02", f"=C{base}*0.05"),
 ("Labor", f"={S(lab_rows['M'], 'I')}", f"={S(lab_rows['D'], 'I')}"),
 (f"Supervision 55 x days (metal {days_m} d = stud/track/runner LF / 300; drywall {days_d} d = all board SF / 1000)", 55 * days_m, 55 * days_d),
 ("Management 65 x days", 65 * days_m, 65 * days_d),
 ("Safety", 100, 100),
 ("Transportation", 50, 50),
 ("Equipment 100 x weeks", 100 * math.ceil(days_m / 7), 100 * math.ceil(days_d / 7)),
 ("Subtotal", *[f"=SUM({c}{base}:{c}{base + 7})" for c in "BC"]),
 ("OH 12% (template)", *[f"={c}{base + 8}*0.12" for c in "BC"]),
 ("Allowance 2% (template)", *[f"={c}{base + 8}*0.02" for c in "BC"]),
 ("Profit 12% (template)", *[f"={c}{base + 8}*0.12" for c in "BC"]),
 ("Section total", *[f"=SUM({c}{base + 8}:{c}{base + 11})" for c in "BC"]),
 ("Proposal price (x 1.15, rounded up to 100 - template 'PROPOSAL DW' col N / R)", *[f"=ROUNDUP({c}{base + 12}*1.15/100,0)*100" for c in "BC"]),
]
for ln in lines:
    B.append(list(ln))
pr = base + 13
B.append([]); B.append(["Total all sections", f"=SUM(B{pr}:C{pr})"]); tot = B.max_row
B.append(["Taxes 8.81% (template rate - [RATE TO CONFIRM] for Castle Rock, CO)", f"=B{tot}*0.0881"]); tax = B.max_row
B.append(["Total including tax", f"=ROUND(B{tot}+B{tax},0)"]); gt = B.max_row
B.append([]); B.append(["SUMMARY (for the estimator)"])
B.append(["Material total (with markup)", f"=B{base}+B{base + 1}+C{base}+C{base + 1}"])
B.append(["Labor total", f"=B{base + 2}+C{base + 2}"])
B.append(["General conditions (supervision, management, safety, transportation, equipment)", f"=SUM(B{base + 3}:C{base + 7})"])
B.append(["OH 12% + allowance 2% + profit 12%", f"=SUM(B{base + 9}:C{base + 11})"])
B.append([]); B.append(["NOT PRICED (0 in the totals until confirmed):"])
for x in missing_rate:
    B.append(["[RATE TO CONFIRM]", x])
for x in missing_sku:
    B.append(["[PRICE TO CONFIRM]", x])
B.append(["[RATE TO CONFIRM]", "Sales tax: template 8.81% used; confirm the Castle Rock, CO rate"])
for c, w in zip("ABCDEFGHIJ", (14, 70, 10, 6, 20, 11, 10, 10, 12, 34)):
    B.column_dimensions[c].width = w
for code, p in used:
    F.append([code, p["name"], p["cat"], p["price"], p["unitLabel"], p.get("minOrderQuantity"), p.get("stockLevelStatus"),
              p.get("specialMessage"), "https://myfbm.com" + p["url"], fecha, "guest branch CO-086 Englewood (Denver area)"])
    F.cell(F.max_row, 4).font = BLUE
for c, w in zip("ABCDEFGHIJK", (20, 70, 14, 10, 10, 9, 12, 14, 48, 18, 30)):
    F.column_dimensions[c].width = w

# ---------------------------------------------------------------------------------------------- PROPOSAL sheet text
WRAP = Alignment(wrap_text=True, vertical="top")


def put(ref, v, wrap=True, bold=False, size=None):
    P[ref].value = v
    if wrap:
        P[ref].alignment = WRAP
    if bold or size:
        P[ref].font = Font(bold=bold, name="Calibri", size=size or 11)


TBC = "[TO BE COMPLETED]"


def nlines(items, cpl):
    """wrapped lines of a list of text lines at cpl characters per line (row heights of the merged text blocks)."""
    return sum(max(1, math.ceil(len(x) / cpl)) for x in items)

put("C5", "PROPOSAL SUBMITTED TO:"); put("G5", "PER PLAN & SPECS:")
put("C6", "Owen-Ames-Kimball Co. - Jess Matias")
put("G6", "YES - 2026 Permit Drawings + Project Manual Vol 1 & 2")
put("C7", "PROJECT NAME:"); put("G7", "ARCHITECT:")
put("C8", "CR CITY HOTEL (new 4-story hotel, Type IIIB, wood framed)"); put("G8", "Meridian 105 Architecture")
put("C9", "PROJECT ADDRESS:"); put("G9", "DATE OF PLANS:")
put("C10", "415 PERRY STREET, CASTLE ROCK, CO 80104"); put("G10", "Arch. / Struct. 04-22-2026 (Issued for Permit); MEP 06-01-2026")
put("C11", "DATE OF PROPOSAL:"); put("G11", "ADDENDUM:")
P["C12"].value = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0); P["C12"].number_format = "mm-dd-yyyy"
put("G12", "None reviewed [TO BE CONFIRMED]")
put("C13", "PHONE NUMBER:"); put("G13", "E-MAIL:")
put("C14", TBC); put("G14", TBC)
put("C15", "Scope of Work:", bold=True)
put("C16", "We propose to supply the material, labor, and equipment necessary to complete the work in accordance with the plans "
           "and the scope listed below.")
put("C17", "(Please take special note of the scope description; we are not required to perform any items or tasks not specifically listed)")
put("C19", "1.-"); put("D19", "Division of work: DRYWALL & FINISH LEVEL 4, C-H SHAFT WALLS, CEILING SUSPENSION.", bold=True)
inc = ["INCLUDED (quantities from the take-off rev18 FINAL: net and purchase = net + waste, with their sheets):"]
for r in ms:
    if (r[2] or 0) > 0:
        pu = r[5] if isinstance(r[5], (int, float)) else r[2]
        inc.append(f"• {r[0]}: {r[2]:,.2f} {r[1]} net / {pu:,.2f} {r[1]} purchase" + (f"  [{nsheet(r[8])}]" if nsheet(r[8]) else ""))
inc.append("• Level 4 finish on all interior gypsum board (09 29 00 3.6.E.4); board only on the wood-framed walls (framing by others).")
put("C21", "\n".join(inc), size=9)
for rr in list(range(19, 48)):
    P.row_dimensions[rr].hidden = False
for rr in range(21, 44):                     # C21 spans the template rows 21-43
    P.row_dimensions[rr].height = max(15, 12.5 * nlines(inc, 140) / 23 + 1)
put("C44", "1a. Gypsum board on the WOOD-framed walls (framing by others, Div. 06): 5/8\" Type X per face and layers per type and "
           "rating (A0.06, A0.07, UL U379 / U301 / U341 / V337), 5/8\" Type X W.R. at toilet / shower / janitor faces (A0.06 GN 11 / 12), "
           "5/8\" cement board at guest bath tile walls (GN 13), 5/8\" Type X glass-mat exterior gypsum sheathing, ASTM C1177 (06 16 00 2.5.B), per A0.07 XW rows.")
put("C45", "1b. Ceilings: FS-1 5/8\" Type C on resilient channel (A0.08, UL L546), RS-1 5/8\" Type X on channel under the roof, "
           "GYP-1 / GYP-2 dropped ceilings on USG drywall suspension (main tee DGLW26, cross tee DGLW424, angle DGWM24, hanger wire), "
           "corridor bands, lobby coffers and stair soffit with ceiling / soffit track (7/A7.23, 2/A7.31, 11/A6.01).")
put("C46", "1c. C-H shaft walls: L2-L4 north / south shafts 2-1/2\" 20 GA C-H studs + 2-1/2\" J-runner (7/A9.03, 8/A9.03 4 3/4\" "
           "2-HOUR SHAFTWALL W419 / U497); L1 / L4 chase 6\" 20 GA C-H + 6\" J-runner (CH.6, 1/A7.50); studs @ 24\" o.c. to the liner height; "
           "1\" Type X shaftliner + 2 layers 5/8\" Type X.")
put("C47", "1d. Metal corner bead (09 29 00 2.5), control joints (A0.06 GN 15, ASTM C840), joint tape and compound, Level 4 finish.")
for rr in (44, 45, 46, 47):
    P[f"C{rr}"].font = Font(name="Calibri", size=10)
    P.row_dimensions[rr].height = 14 * nlines([str(P[f"C{rr}"].value)], 120) + 4
put("C48", "NOT INCLUDED / EXCLUSIONS:", bold=True)
ex = []
for r in scope:
    t = " ".join(str(x or "") for x in r[1:4])
    if re.search(r"\bEXCLUDED\b", t) and not str(r[0]).startswith(("RFI", "A/B")) and \
            not re.search(r"QUANTIFIED|CUANTIFICADO", str(r[2] or "")):
        n = re.sub(r"\s*\(EXCLUDED[^)]*\)", "", str(r[1]))
        why = re.sub(r"^.*?EXCLUDED[:\s-]*", "", str(r[3] or ""))
        ex.append(f"• {n}: {why}")
ex += ["• Gypsum board & finish at the NON-rated retail-side faces of Retail 124 (A2.01 note 'BY FUTURE TENANT', RFI-05); "
       "(the L1 retail steel beam wraps of the rated FS-1 membrane ARE included, RFI-20)",
       "• Area 'UNDER A SEPARATE PERMIT AND NOT IN SCOPE' (A2.01, RFI-06) and the existing historic building",
       "• Screws, anchors, pins and power-driven fasteners (estimator standing order U-053)",
       "• Level 5 finish in the base (Level 4 per 09 29 00 3.6.E.4; see ADD ALTERNATE AA-1), FRP, access panels (none scheduled for our trade)",
       "• Bonds, permits and fees; temporary utilities, dumpster, prevailing wages, shop drawings",
       "• Addenda not reviewed in this pricing; anything not specifically listed in the INCLUDED scope"]
_da = [d for d in (can.get("deduct_alternates") or []) if d.get('delta_sf')]
_cl0 = [d for d in (can.get("deduct_alternates") or []) if not d.get('delta_sf')]
_aa = can.get("add_alternates") or []
if _cl0:   # P5: un alterno de 0 SF no es deduct: clarificación
    ex += ["", "CLARIFICATIONS:"] + [f"• {d['id']}{' (' + d['rfi'] + ')' if d.get('rfi') else ''}: {d['texto']} - not in the base, no price effect" for d in _cl0]
if _aa:   # F9: add alternates
    ex += ["", "ADD ALTERNATES:"] + [f"• {d['id']}: {d['texto']} - ADD {d['delta_sf']:,.2f} SF {d['material']}" for d in _aa]
if _da:   # R80e.38-4: base = larger option while the RFI is open; the other option is a DEDUCT ALTERNATE with its delta
    ex += ["", "DEDUCT ALTERNATES (the base above carries the larger option while the RFI is open):"]
    ex += [f"• {d['id']}{' (' + d['rfi'] + ')' if d.get('rfi') else ''}: {d['texto']} - DEDUCT {abs(d['delta_sf']):,.2f} SF {d['material']}" if d['delta_sf']
           else f"• {d['id']}: {d['texto']} - 0 SF (not in base, nothing to deduct)" for d in _da]
for m in [m for m in list(P.merged_cells.ranges) if 49 <= m.min_row <= 56]:
    P.unmerge_cells(str(m))
P.merge_cells("C49:J56")
put("C49", "\n".join(ex), size=9)
for rr in range(49, 57):
    P.row_dimensions[rr].height = max(15, 12.5 * nlines(ex, 140) / 8 + 2)
put("C57", "NOTE: PROPOSAL HOLDS GOOD ONLY FOR THE ITEMS AND QUANTITIES LISTED ABOVE (TAKE-OFF " + REVN.upper() + " FINAL)")
put("C59", "3.-"); put("D59", "Work Standard:", bold=True)
put("C60", "All work is to be completed in a workmanlike manner according to standard practices. Workers will remain on the job "
           "until completion of the project. The worksite will be cleaned daily and upon project completion. All agreements are "
           "contingent upon delays beyond our control.")
put("C61", "4.-"); put("D61", "Limited Warranty:", bold=True)
put("C62", "The completed work shall carry a 1-year warranty on labor and materials. This warranty is in lieu of all other "
           "warranties, expressed or implied, and excludes consequential or incidental damages caused by accident or abuse, "
           "temperature changes, settlement, moisture, or cracks caused by expansion and/or contraction.")
put("C63", "5.-"); put("D63", "Insurance:", bold=True)
put("C64", "All employees are covered under blanket workman's comp, with liability and umbrella insurance policies.")
put("C65", "6.-"); put("D65", "Touch-Ups:", bold=True)
put("C66", "Drywall & finishes: included on all work performed, limited to 1 hr per every 1,000 SF for quality issues; trade "
           "damage repairs tracked on work ticket. Finish level per GA-214 (Level 4).")
put("C67", "7.-"); put("D67", "Others:", bold=True)
put("C68", "7.1. Work sequenced according to industry standards; out of sequence work and schedule delays require added cost.\n"
           "7.2. Work days Monday - Saturday, 7:00 am - 5:00 pm (no overtime or night work included).\n"
           "7.3. Price valid for thirty (30) days. Material pricing per FBM list prices read 11-05-2026.")
rows_p = [(73, "9.-", "Metal framing (C-H shaft walls) & ceiling suspension:", "I74", f"=PRICING!B{pr}"),
          (75, "9.a-", "Drywall & drywall finish Level 4:", "I76", f"=PRICING!C{pr}")]
for rr, n_, t, b_, f in rows_p:
    for m in [m for m in list(P.merged_cells.ranges) if m.min_row == rr]:
        P.unmerge_cells(str(m))
    put(f"C{rr}", n_, wrap=False, bold=True); put(f"D{rr}", t, wrap=False, bold=True)
    P.merge_cells(f"D{rr}:H{rr}")
    for x in (rr, rr + 1):
        P.row_dimensions[x].hidden = False
        P.row_dimensions[x].height = 18
    P[b_].value = f; P[b_].number_format = '"$"#,##0'
for rr in list(range(69, 73)) + list(range(77, 83)):
    P.row_dimensions[rr].hidden = True
put("D83", "Total all trades:", wrap=False); P["I84"].value = f"=PRICING!B{tot}"
put("D85", "Taxes (8.81% template rate - to confirm for Castle Rock):", wrap=False); P["I86"].value = f"=PRICING!B{tax}"
put("D87", "Total including tax:", wrap=False); P["I88"].value = f"=PRICING!B{gt}"
for x in ("I84", "I86", "I88"):
    P[x].number_format = '"$"#,##0'
P.merge_cells("C89:J89")
put("C89", "**NOTE: items marked [RATE TO CONFIRM] / [PRICE TO CONFIRM] in the PRICING sheet are not in the totals.")
put("C91", "Acceptance of proposal:", bold=True)
put("C92", "The prices, specifications and conditions are satisfactory and are hereby accepted. You are authorized to do the work as specified.")
put("G93", "Signature:"); put("G95", "Date of acceptance:")
r = 98
P.merge_cells(f"C{r}:J{r}")
put(f"C{r}", "CLARIFICATIONS (decisions applied in the quantities):", bold=True)
cl = ["Wood-framed building: all W / FW / DW / FI / XW types are wood studs (A0.06, A0.07) - board only; framing, blocking, FRT plywood by Div. 06.",
      "RFI-10: WOOD / FURRED WOOD / DBL. WOOD sections print 5/8\" TYPE X GYP BD. TYP. - Type X loaded on every interior face (09 29 00 2.3 A).",
      "RFI-11: cement board at guest bath tile walls to 9'-0\" (bath ceiling 8'-6\" + 6\"); rated Type X W.R. layers stay full height.",
      "RFI-07: L2-L4 shaft walls carried with 2-1/2\" C-H per 7/A9.03 / 8/A9.03 (4 3/4\" assembly); A0.06 CH.6-2 prints 6\" - same LF in 6\" if required.",
      "RFI-16 / RFI-14: C-H studs @ 24\" o.c. (UL U415); resilient channel @ 16\" o.c. (UL L546, 'spacing per assembly').",
      "RFI-12: GYP-1 'metal suspension OR wood framing' - metal option carried (USG drywall suspension).",
      "RS-1 ceilings under the roof: board type not printed - 5/8\" Type X carried; channel carried in the resilient channel row.",
      "RFI-05: retail faces of RATED assemblies stay loaded (1,033 SF); non-rated retail faces excluded (532.5 SF, by future tenant).",
      "RFI-18: L4 corridor 412 cove carried along the corridor walls (typical 7/A7.23); L1 lobby ceiling carried at 11'-0\", no step face.",
      "Material prices: FBM (myfbm.com) list prices read 11-05-2026; exterior sheathing = 5/8\" Type X glass-mat gypsum sheathing, ASTM C1177 (06 16 00 2.5.B); FBM glass-mat SKU [PRICE TO CONFIRM]."]
for x in cl:
    r += 1
    P.merge_cells(f"C{r}:J{r}")
    put(f"C{r}", x)
    P.row_dimensions[r].height = 30
P.print_area = f"A1:K{r}"
wb.save(OUT)
print("OK", OUT, "| missing rates:", len(missing_rate), "| missing SKUs:", len(missing_sku), "| FBM used:", len(used))
print("grid SF:", grid_sf, "| RC ceiling SF (canon):", rc_sf, "| finished board SF:", round(board_fin, 2), "| all board SF:", round(board_all, 2),
      "| days metal / drywall:", days_m, days_d)
print("RATES:", missing_rate); print("SKUS:", missing_sku)
