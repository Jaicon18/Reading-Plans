"""Xfinity Interquest proposal (rev1 FINAL quantities, no new take-off pass), from the user's "Proposal Template.xlsx":
sheet PROPOSAL DW (JC Hunter letterhead) + PRICING (material FBM / labor and OH with the template's own rates, formulas) +
FBM_PRICES (every FBM product used: SKU, name, price, unit, stock, link, date, branch). Precedent: B&N armar_proposal.py.
Rates not in the template -> "[RATE TO CONFIRM]" (0 in the totals, listed); FBM SKU not found -> "[PRICE TO CONFIRM]".
Usage: armar_proposal.py <template.xlsx> <rev1 takeoff.xlsx> <canon.json> <fbm_dir> <out.xlsx>"""
import datetime, glob, json, math, re, sys
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

TPL, TK, CN, FBM, OUT = sys.argv[1:6]
wbt = openpyxl.load_workbook(TK, data_only=True)
can = json.load(open(CN))
ms = [r for r in wbt["Material Summary"].iter_rows(min_row=4, values_only=True) if r[0] and isinstance(r[2], (int, float))]
scope = [r for r in wbt["Scope Checklist"].iter_rows(min_row=2, values_only=True) if r[0]]
MS = {r[0]: r for r in ms}
fbm, fecha = {}, None
for f in glob.glob(f"{FBM}/*.json"):
    d = json.load(open(f))
    fecha = d["fecha"]
    for r in d["rows"]:
        fbm[r["code"]] = dict(r, cat=d["category"])

def nsheet(txt):
    m = re.search(r"N/SHEET:\s*([^|]+)", str(txt or ""))
    return m.group(1).strip() if m else ""

def buy(name):
    r = MS[name]
    return float(r[5] or r[2])      # purchase quantity of the take-off (net + waste of the take-off Inputs)

# ---------------------------------------------------------------------------------------------- material lines
def key(prefix):
    k = [n for n in MS if n.startswith(prefix)]
    if len(k) != 1:
        sys.exit(f"Material Summary row '{prefix}' found {len(k)} times")
    return k[0]
def bk(prefix):
    return buy(key(prefix))
trims = [n for n in MS if n.startswith("METAL trim")]
cb = [n for n in trims if MS[n][2] < 50][0]; lb = [n for n in trims if MS[n][2] >= 50][0]
L = [  # section M = metal framing, D = drywall & finish, F = trim
 ("M", '3-5/8" stud 20 ga (33 mil) 362S125-33 @ 16", type W2 + door 101 jambs + SOF-01 header framing (2/A2.0, A3.0, limiting heights A2.0)', bk('3-5/8" metal stud (LF of material) - 362S125-33'), "LF", "BASE_S362S125-33", 0.1, "2/A2.0"),
 ("M", '3-5/8" stud 16 ga (54 mil) 362S162-54 @ 16" at backing (8/A2.0 "16 GA. METAL STUD"; 1-5/8" flange not printed, confirm)', bk('3-5/8" metal stud (LF of material) - 362S162-54'), "LF", "BASE_S362S162-54", 0.1, "8/A2.0"),
 ("M", '2-1/2" stud 250S125-43 @ 16", column furring (5/A2.0, limiting heights A2.0)', bk('2-1/2" stud'), "LF", "BASE_S250S125-43", 0.1, "5/A2.0"),
 ("M", 'Bottom track 3-5/8" 20 ga (3/A2.0)', bk('Bottom track 3-5/8"'), "LF", "BASE_T362T125-33", 0.1, "3/A2.0"),
 ("M", 'Top track 3-5/8" 20 ga, standard (4/A2.0)', bk('Top track 3-5/8"'), "LF", "BASE_T362T125-33", 0.1, "4/A2.0"),
 ("M", 'Bottom + top track 2-1/2" (5/A2.0)', bk('Bottom track 2-1/2"') + bk('Top track 2-1/2"'), "LF", "BASE_T250T125-43", 0.1, "5/A2.0"),
 ("M", 'Header track SOF-01 (A3.0)', bk('Ceiling / soffit track'), "LF", "BASE_T362T125-33", 0.1, "A3.0"),
 ("M", 'Door 101 track head with nested stud (7/A2.0)', bk('Header / metal stud box beam'), "LF", "BASE_T362T125-33", 0.1, "7/A2.0"),
 ("M", 'Kicker braces to structure 3-5/8" 20 ga @ 8\'-0" (4/A2.0)', bk('Metal stud brace to structure'), "LF", "BASE_S362S125-33", 0.1, "4/A2.0"),
 ("M", '6" sheet metal blocking strapping (A5.0 blocking legend EV-44 / EV-45)', bk('Blocking / backing at wall-mounted items (notes) - 6" sheet metal blocking strapping'), "LF", "BASE_FS600-30", 0.1, "A5.0"),
 ("M", '16 ga 6" x 1-1/2" unpunched track backing: fire extinguishers, GF-14496 graphic frame, drinking fountain (8/A2.0)', bk('Blocking / backing at wall-mounted items (notes) - 16 ga'), "LF", "BASE_T600T150-54", 0.1, "8/A2.0"),
 ("D", '5/8" Type X gypsum board 4x12 (2/A2.0, 5/A2.0, A3.0)', bk('5/8" gypsum board, Type X'), "SF", "D58F12-U", 1 / 48, "2/A2.0"),
 ("D", 'All-purpose joint compound (Material Summary LB; FBM 3-1/2 gal box priced at 1 box per 48 LB [CONVERSION TO CONFIRM])', bk('Joint compound'), "LB", "APUB3.5", 1 / 48, "Level 4 (A2.0 gen. note 3)"),
 ("D", 'Paper joint tape 500 ft roll', bk('Joint tape, paper'), "LF", "DWT500W", 1 / 500, "Level 4"),
 ("F", 'Metal corner bead 10 ft (6/A2.0, SOF-01 edges)', buy(cb), "LF", "DWB10-60", 0.1, "6/A2.0"),
 ("F", 'Metal L bead 5/8" 10 ft, column furring (5/A2.0)', buy(lb), "LF", "DWL5810-60", 0.1, "5/A2.0"),
]
board_total = MS[key('5/8" gypsum board, Type X')][2]
# ---------------------------------------------------------------------------------------------- labor (template rates)
walls = can["walls"]
a362 = round(sum(w["length_ft"] * w["height_ft"] for w in walls if w.get("stud_size") == '3-5/8"'), 2)
a250 = round(sum(w["length_ft"] * w["height_ft"] for w in walls if w.get("stud_size") == '2-1/2"'), 2)
sf = {k: MS[k][2] for k in MS}
LAB = [  # section, description, qty, unit, rate or None, rate source
 ("M", 'Framing labor 3-5/8" walls W2 (wall SF = LF x stud height)', a362, "SF", 0.8, "Template 'Metal Framing' col K, 3 5/8\" METAL STUD rows (0.80 / SF)"),
 ("M", 'Framing labor 2-1/2" column furring (wall SF)', a250, "SF", None, "not in the template"),
 ("M", 'Kicker braces, SOF-01 header framing, blocking / backing install', bk('Metal stud brace to structure'), "LF", None, "not in the template"),
 ("D", 'Hanging 5/8" Type X board', board_total, "SF", 0.78, "Template 'Drywall finish' J8 5/8\" GYP BD X (0.78 / SF)"),
 ("D", 'Level 4 finishing (joint tape + mud), all board', board_total, "SF", 0.5, "Template 'Drywall finish' J27 LABOUR FOR FINISHING (0.50 / SF)"),
 ("F", 'Corner bead and L bead install', sf[cb] + sf[lb], "LF", None, "not in the template"),
 ("X", 'Demolition of gypsum board and metal framing walls (A1.0 key note 7), SF of the element', sf[key('Demolition')], "SF", 1.25, "Template 'Demolition works' F23 wall demolition (1.25 / SF)"),
]
stud_track_lf = sum(MS[k][2] for k in MS if re.search(r"stud|track|Header|brace|strapping|blocking", k, re.I) and MS[k][1] == "LF")
days_m = math.ceil(stud_track_lf / 300)
days_d = math.ceil(board_total / 1000)

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
B.append(["XFINITY - INTERQUEST, COLORADO SPRINGS, CO - PRICING (quantities from Take-off rev1 FINAL; no new take-off pass)"])
B.append(["Material: FBM myfbm.com visitor price (guest branch CO-086 Englewood / Denver area), read " + str(fecha) +
          "; contractor account price may differ. Labor / OH / markups: the user's Proposal Template rates (source per row)."])
B.append([])
hdr = ["Section", "Item", "Qty", "Unit", "FBM code", "FBM price", "FBM unit", "Units of price per qty", "Material $", "N/SHEET / note"]
sec_rows = {"M": [], "D": [], "F": []}
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
        missing_sku.append(dsc)
        B.append([s, dsc, round(q, 2), u, "[PRICE TO CONFIRM]", None, None, None, 0, nt + " - SKU not listed at FBM"])
        B[f"E{r}"].fill = YEL
    sec_rows[s].append(r)
B.append([]); B.append(["LABOR (template rates)"]); B.append(["Section", "Item", "Qty", "Unit", "Rate", "Rate source", "", "", "Labor $"])
lab_rows = {"M": [], "D": [], "F": [], "X": []}
missing_rate = []
for s, dsc, q, u, rate, src in LAB:
    r = B.max_row + 1
    if rate is None:
        missing_rate.append(dsc)
        B.append([s, dsc, round(q, 2), u, "[RATE TO CONFIRM]", src, "", "", 0])
        B[f"E{r}"].fill = YEL
    else:
        B.append([s, dsc, round(q, 2), u, rate, src, "", "", f"=C{r}*E{r}"])
    lab_rows[s].append(r)
B.append([])
B.append(["SECTION BUILD-UP (template 'Metal Framing' / 'Drywall finish' rows 54-84 and 'PROPOSAL DW' col N 15% + round to 100)"])
B.append(["Line", "Metal framing", "Drywall & finish L4", "Metal trim", "Demolition"])
def S(rows, col):
    return "+".join(f"{col}{x}" for x in rows) or "0"
base = B.max_row + 1
lines = [
 ("Material", f"={S(sec_rows['M'], 'I')}", f"={S(sec_rows['D'], 'I')}", f"={S(sec_rows['F'], 'I')}", 0),
 ("Material markup (template: metal 2% / drywall 5%)", f"=B{base}*0.02", f"=C{base}*0.05", f"=D{base}*0.05", 0),
 ("Labor", f"={S(lab_rows['M'], 'I')}", f"={S(lab_rows['D'], 'I')}", f"={S(lab_rows['F'], 'I')}", f"={S(lab_rows['X'], 'I')}"),
 (f"Supervision 55 x days (metal {days_m} d = stud/track LF / 300; drywall {days_d} d = board SF / 1000)", 55 * days_m, 55 * days_d, 0, 0),
 ("Management 65 x days", 65 * days_m, 65 * days_d, 0, 0),
 ("Safety", 100, 100, 0, 0),
 ("Transportation", 50, 50, 0, 0),
 ("Equipment 100 x weeks", 100 * math.ceil(days_m / 7), 100 * math.ceil(days_d / 7), 0, 0),
 ("Subtotal", *[f"=SUM({c}{base}:{c}{base + 7})" for c in "BCDE"]),
 ("OH 12% (template)", *[f"={c}{base + 8}*0.12" for c in "BCD"], 0),
 ("Allowance 2% (template)", *[f"={c}{base + 8}*0.02" for c in "BCD"], 0),
 ("Profit 12% (template)", *[f"={c}{base + 8}*0.12" for c in "BCD"], 0),
 ("Section total", *[f"=SUM({c}{base + 8}:{c}{base + 11})" for c in "BCDE"]),
 ("Proposal price (x 1.15, rounded up to 100 - template 'PROPOSAL DW' col N / R)", *[f"=ROUNDUP({c}{base + 12}*1.15/100,0)*100" for c in "BCDE"]),
]
for ln in lines:
    B.append(list(ln))
pr = base + 13
B.append([]); B.append(["Total all sections", f"=SUM(B{pr}:E{pr})"]); tot = B.max_row
B.append(["Taxes 8.81% (template rate - [RATE TO CONFIRM] for Colorado Springs, CO)", f"=B{tot}*0.0881"]); tax = B.max_row
B.append(["Total including tax", f"=ROUND(B{tot}+B{tax},0)"]); gt = B.max_row
B.append([]); B.append(["NOT PRICED (0 in the totals until confirmed):"])
for x in missing_rate:
    B.append(["[RATE TO CONFIRM]", x])
for x in missing_sku:
    B.append(["[PRICE TO CONFIRM]", x])
B.append(["[ALLOWANCE TO CONFIRM]", "Patch and repair of existing walls W1 / W4 (2/A2.0) - allowance by the estimator"])
B.append(["[ALLOWANCE TO CONFIRM]", "Temporary non-combustible construction barriers (A1.0 demolition note 18, conditional) - allowance by the estimator"])
for c, w in zip("ABCDEFGHIJ", (14, 62, 10, 6, 20, 11, 10, 10, 12, 30)):
    B.column_dimensions[c].width = w
for code, p in used:
    F.append([code, p["name"], p["cat"], p["price"], p["unitLabel"], p.get("minOrderQuantity"), p.get("stockLevelStatus"),
              p.get("specialMessage"), "https://myfbm.com/all-products/x/p/" + code, fecha, "guest branch CO-086 Englewood (Denver area)"])
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
put("C5", "PROPOSAL SUBMITTED TO:"); put("G5", "PER PLAN & SPECS:")
put("C6", "BCI National Construction & Facilities (Kyle McGee / Morgan Fergus)"); put("G6", "YES - Complete PDF Set 10-08-26 R0 (17 sheets; specs on A0.3)")
put("C7", "PROJECT NAME:"); put("G7", "ARCHITECT:")
put("C8", "XFINITY - INTER QUEST, CO TI IMPROVEMENT PROJECT (Branded Partner, Interquest Commons Lot #11)"); put("G8", "Robert F. Vanney, Architect (comm. 81-2116)")
put("C9", "PROJECT ADDRESS:"); put("G9", "DATE OF PLANS:")
put("C10", "1333 INTERQUEST PKWY., LOT #11, COLORADO SPRINGS, CO 80921"); put("G10", "10-08-2026 (bid / permit issue, 17 sheets)")
put("C11", "DATE OF PROPOSAL:"); put("G11", "ADDENDUM:")
P["C12"].value = datetime.datetime(2026, 11, 11); P["C12"].number_format = "mm-dd-yyyy"
put("G12", "None issued as of 11-10-2026")
put("C13", "PHONE NUMBER:"); put("G13", "E-MAIL:")
put("C14", TBC); put("G14", TBC)
put("C15", "Scope of Work:", bold=True)
put("C16", "We propose to supply the material, labor, and equipment necessary to complete the work in accordance with the plans "
           "and the scope listed below.")
put("C17", "(Please take special note of the scope description; we are not required to perform any items or tasks not specifically listed)")
put("C19", "1.-"); put("D19", "Division of work: METAL FRAMING, DRYWALL & DRYWALL FINISH LEVEL 4, DEMOLITION (CSI Div. 05 40 00 / 09 21 16 / 09 22 16). Day work (regular business hours) per the GC invitation.", bold=True)
inc = ["INCLUDED (quantities from the take-off rev1 FINAL, net before waste, with their sheet):"]
for r in ms:
    if (r[2] or 0) > 0:
        inc.append(f"• {r[0]}: {r[2]:,.2f} {r[1]}" + (f"  [{nsheet(r[8])}]" if nsheet(r[8]) else ""))
inc.append("• Partition type W2 per 2/A2.0 (A2.0), column furring 5/A2.0; Level 4 finish on all gypsum board (A2.0 general note 3).")
put("C21", "\n".join(inc), size=9)
for rr in list(range(19, 48)):
    P.row_dimensions[rr].hidden = False
for rr in range(21, 44):                     # C21 spans the template rows 21-43
    P.row_dimensions[rr].height = max(15, 12.5 * len(inc) / 23)
for rr in (44, 45, 46, 47):
    P.row_dimensions[rr].height = 48
put("C44", "1a. Metal framing: type W2 partitions 3-5/8\" 20 ga @ 16\" (2/A2.0, A2.0 limiting heights table) with 20 ga tracks (3/A2.0, 4/A2.0), "
           "kicker braces to structure @ 8'-0\" (4/A2.0), door 101 track head (7/A2.0), column furring 2-1/2\" (5/A2.0), the 8'-6\" gypsum header "
           "framing at Hallway 102 (A3.0), 6\" sheet metal blocking strapping (A5.0) and 16 ga track backing (8/A2.0).")
put("C45", "1b. Drywall & drywall finish Level 4: 5/8\" Type X board both faces of W2, column furring (5/A2.0) and the 8'-6\" header (A3.0), "
           "tape and compound.")
put("C46", "1c. Metal corner bead (6/A2.0, header edges) and L bead at the column furring (5/A2.0).")
put("C47", "1d. Demolition of the existing walls shown dashed on A1.0 (key note 7), by area (SF).")
put("C48", "NOT INCLUDED / EXCLUSIONS:", bold=True)
ex = []
for r in scope:
    t = " ".join(str(x or "") for x in r[1:4])
    if re.search(r"\bEXCLUDED\b", t) and not str(r[0]).startswith(("RFI", "A/B")) and \
            not re.search(r"QUANTIFIED|CUANTIFICADO", str(r[2] or "")):
        n = re.sub(r"\s*\(EXCLUDED[^)]*\)", "", str(r[1]))
        why = re.sub(r"^.*?EXCLUDED[:\s-]*", "", str(r[3] or ""))[:120]
        ex.append(f"• {n}: {why}")
ex += ["• Patch and repair of existing walls W1 / W4 (2/A2.0) - allowance only if requested", "• Existing ceiling demolition (A1.0 keys 14 / 15) - ACT by others / type not indicated",
       "• Bonds, permits and fees", "• Temporary utilities, dumpster, prevailing wages, shop drawings",
       "• Acoustical ceilings and painting (separate bid packages)", "• Anything not specifically listed in the INCLUDED scope"]
for m in [m for m in list(P.merged_cells.ranges) if 49 <= m.min_row <= 56]:
    P.unmerge_cells(str(m))
P.merge_cells("C49:J56")
put("C49", "\n".join(ex), size=9)
for rr in range(49, 57):
    P.row_dimensions[rr].height = max(15, 12.5 * len(ex) / 8 + 2)
put("C57", "NOTE: PROPOSAL HOLDS GOOD ONLY FOR THE ITEMS AND QUANTITIES LISTED ABOVE (TAKE-OFF REV1 FINAL)")
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
           "7.3. Price valid for thirty (30) days. Material pricing per FBM list prices read 11-11-2026 (UTC).")
rows_p = [(69, "8.-", "Demolition works:", "I70", f"=PRICING!E{pr}"), (71, "9.-", "Metal framing:", "I72", f"=PRICING!B{pr}"),
          (73, "9.a-", "Drywall & drywall finish Level 4:", "I74", f"=PRICING!C{pr}"),
          (75, "9.b-", "Metal trim (corner bead, L bead):", "I76", f"=PRICING!D{pr}")]
for rr, n_, t, b_, f in rows_p:
    for m in [m for m in list(P.merged_cells.ranges) if m.min_row == rr]:
        P.unmerge_cells(str(m))
    put(f"C{rr}", n_, wrap=False, bold=True); put(f"D{rr}", t, wrap=False, bold=True)
    P.merge_cells(f"D{rr}:H{rr}")
    for x in (rr, rr + 1):
        P.row_dimensions[x].hidden = False
        P.row_dimensions[x].height = 18
    P[b_].value = f; P[b_].number_format = '"$"#,##0'
for rr in range(77, 83):
    P.row_dimensions[rr].hidden = True
put("D83", "Total all trades:", wrap=False); P["I84"].value = f"=PRICING!B{tot}"
put("D85", "Taxes (8.81% template rate - to confirm for Colorado Springs):", wrap=False); P["I86"].value = f"=PRICING!B{tax}"
put("D87", "Total including tax:", wrap=False); P["I88"].value = f"=PRICING!B{gt}"
for x in ("I84", "I86", "I88"):
    P[x].number_format = '"$"#,##0'
P.merge_cells("C89:J89")
put("C89", "**NOTE: items marked [RATE TO CONFIRM] / [PRICE TO CONFIRM] / allowances in the PRICING sheet are not in the totals.")
put("C91", "Acceptance of proposal:", bold=True)
put("C92", "The prices, specifications and conditions are satisfactory and are hereby accepted. You are authorized to do the work as specified.")
put("G93", "Signature:"); put("G95", "Date of acceptance:")
r = 98
P.merge_cells(f"C{r}:J{r}")
put(f"C{r}", "CLARIFICATIONS (decisions applied in the quantities):", bold=True)
rf_ = can["rfis"]
r1 = next(x for x in rf_ if x["id"] == "RFI-01")
cl = ["RFI-01 (user decision 2026-11-11, option A, rule U-174): height of the existing structure not printed - 26'-0\" (A0.1 building height) carried for the 4/A2.0 kicker braces and the demolished wall height; " + r1["delta"] + ".",
      "Board measured through door 101 without deducting the opening (estimator standing rule).",
      *[f"{x['id']} (open, conservative value included): {x['loaded']}; alternatives: {x['delta']}." for x in rf_ if x["status"] == "open"],
      "Level 4 finish per A2.0 general note 3 (the A0.3 'texture finish' line is superseded by the drawings).",
      "Closed by the drawings: " + "; ".join(x["resolved"]["answer"][:110] for x in rf_ if x["status"] != "open" and x["id"] != "RFI-01") + ".",
      "Demolition is priced by area (SF of each dashed wall of A1.0, key note 7), no layers.",
      "Wood / F.R.T. blocking and 3/4\" FRT plywood (Div. 06), fasteners, insulation, ACT, paint, doors / frames and MEP are excluded (see exclusions).",
      "Material prices: FBM (myfbm.com) list prices read " + str(fecha) + "; 250S125-43 stud not listed on FBM ([PRICE TO CONFIRM])."]
for x in cl:
    r += 1
    P.merge_cells(f"C{r}:J{r}")
    put(f"C{r}", x)
    P.row_dimensions[r].height = 30
P.print_area = f"A1:K{r}"
wb.save(OUT)
print("OK", OUT, "| missing rates:", len(missing_rate), "| missing SKUs:", len(missing_sku), "| FBM used:", len(used))
print("RATES:", missing_rate); print("SKUS:", missing_sku)
