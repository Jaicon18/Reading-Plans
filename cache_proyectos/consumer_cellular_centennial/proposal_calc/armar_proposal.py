"""Consumer Cellular Centennial proposal (rev4 FINAL quantities, no new take-off pass), from the user's "Proposal Template.xlsx":
sheet PROPOSAL DW (JC Hunter letterhead) + PRICING (material FBM / labor and OH with the template's own rates, formulas) +
FBM_PRICES (every FBM product used: SKU, name, price, unit, stock, link, date, branch). Precedent: B&N armar_proposal.py.
Rates not in the template -> "[RATE TO CONFIRM]" (0 in the totals, listed); FBM SKU not found -> "[PRICE TO CONFIRM]".
Usage: armar_proposal.py <template.xlsx> <rev4 takeoff.xlsx> <canon.json> <fbm_dir> <out.xlsx>"""
import datetime, glob, json, math, os, re, sys
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
# (section, description, quantity, unit, FBM code, units of the FBM price per quantity unit, note)
# BASE_ products: FBM price = 10 ft piece ($/MLF / 100, precios-materiales-fbm) -> $/LF = price / 10
st = {s: 0.0 for s in ("362_20", "362_18", "600_20", "600_16")}
f362 = str(MS['3-5/8" metal stud (LF of material)'][8]); f600 = str(MS['6" metal stud (LF of material)'][8])
st["362_20"] = float(re.search(r"20 ga ([\d,.]+) LF", f362).group(1).replace(",", ""))
st["362_18"] = float(re.search(r"18 ga ([\d,.]+) LF", f362).group(1).replace(",", "")) + \
    float(re.search(r"elements \(gauge in their operation\) ([\d,.]+) LF", f362).group(1).replace(",", ""))
st["600_20"] = float(re.search(r"20 ga ([\d,.]+) LF", f600).group(1).replace(",", ""))
st["600_16"] = float(re.search(r"elements \(gauge in their operation\) ([\d,.]+) LF", f600).group(1).replace(",", ""))
w362 = buy('3-5/8" metal stud (LF of material)') / MS['3-5/8" metal stud (LF of material)'][2]
w600 = buy('6" metal stud (LF of material)') / MS['6" metal stud (LF of material)'][2]
pvc = {x["ref"]: x for x in can["pvc_trim_items"]}
edge = 2 * 28.417 + 2 * 4.0 + 2 * 8.667 + 2 * 4.0          # PVC-RR edge top+bottom + door 4C jambs; PVC-MOP edge + ends
inside = 5 * 4.0 + 2 * 4.0
L = [  # section M = metal framing, D = drywall & finish, F = FRP & trim
 ("M", '3-5/8" stud 20 ga (33 mil), types A3 (1/A500)', st["362_20"] * w362, "LF", "BASE_S362S125-33", 0.1, "1/A500"),
 ("M", '3-5/8" stud 18 ga (43 mil), types C3 / E3 + door 3C jambs (1/A500, 3/A600)', st["362_18"] * w362, "LF", "BASE_S362S162-43", 0.1, "1/A500"),
 ("M", '6" stud 20 ga (33 mil), type D (1/A500)', st["600_20"] * w600, "LF", "BASE_S600S125-33", 0.1, "1/A500"),
 ("M", '6" stud 16 ga (54 mil), mop sink shelf (1/A504)', st["600_16"] * w600, "LF", "BASE_S600S162-54", 0.1, "1/A504"),
 ("M", 'Bottom track 3-5/8" 20 ga (2/A500)', buy('Bottom track 3-5/8"'), "LF", "BASE_T362T125-33", 0.1, "2/A500"),
 ("M", 'Bottom track 6" 20 ga (2/A500)', buy('Bottom track 6"'), "LF", "BASE_T600T125-33", 0.1, "2/A500"),
 ("M", 'Top slip / deflection track 3-5/8" 20 ga (4/A500)', buy('Top slip / deflection track 3-5/8" (2" deflection leg, walls to structure)'), "LF", "BASE_TS362T250-33", 0.1, "4/A500"),
 ("M", 'Top slip / deflection track 6" 20 ga (4/A500)', buy('Top slip / deflection track 6" (2" deflection leg, walls to structure)'), "LF", "BASE_TS600T250-33", 0.1, "4/A500"),
 ("M", 'Top track 3-5/8" 20 ga, E3 (3/A500)', buy('Top track 3-5/8" - standard (walls not reaching structure)'), "LF", "BASE_T362T125-33", 0.1, "3/A500"),
 ("M", 'Nested 3-5/8" x 20 ga C channel at the deflection head (4/A500)', buy('Nested inner runner at the deflection head (detail per Where it comes from)'), "LF", "BASE_T362T125-33", 0.1, "4/A500"),
 ("M", 'Door / cased opening track headers (2/A600)', buy('Header / metal stud box beam'), "LF", "BASE_T362T125-33", 0.1, "2/A600"),
 ("M", 'Top of wall braces 362S137-33 (3/A500)', buy('Metal stud brace to structure (size / gauge per the detail, see Where it comes from)'), "LF", "BASE_S362S137-33", 0.1, "3/A500"),
 ("M", '3" x 3" x 3" angles at the braces (3/A500, 20 GA. MIN.)', buy('Clips angles' if False else 'Clip angles and framing clips (see Where it comes from)'), "EA", "SIM-RCA333.54-R100", 1.0, "3/A500"),
 ("M", '20 GA. metal strapping at slat / logo walls / kitchenette (1/A104, 2/A104, 3/A104)', buy('Metal stud blocking at wall-mounted items (notes) - 20 GA metal strapping'), "LF", "BASE_FS600-30", 0.1, "1-3/A104"),
 ("M", '20 GA track at the grab bars (5/A402)', buy('Metal stud blocking at wall-mounted items (notes) - 20 GA track'), "LF", "BASE_T362T125-33", 0.1, "5/A402"),
 ("M", 'Stud blocking at restroom accessories / water heater (A402 note 4, 5/P501)', buy('Metal stud blocking at wall-mounted items (notes) - stud blocking (per source)'), "LF", "BASE_S362S125-33", 0.1, "A402, 5/P501"),
 ("M", 'Drywall grid main tee DGLW26, restroom C-1 ceiling (2/A501)', MS['USG drywall suspension main tee DGLW26'][7], "PCS", "CGUDGLW26", 1 / 16, "2/A501"),
 ("M", 'Drywall grid cross tee DGLW424 (2/A501)', MS['USG drywall suspension cross tee DGLW424'][7], "PCS", "CGUDGLW424", 1 / 48, "2/A501"),
 ("M", '2" x 2" sheet metal angle molding DGWM24 (2/A501)', buy('USG angle molding DGWM24'), "LF", None, None, "2/A501"),
 ("M", '12 ga hanger wire (2/A501)', buy('Hanger wire'), "LF", None, None, "2/A501"),
 ("D", '5/8" Type X gypsum board 4x12 (1/A500)', buy('5/8" gypsum board, Type X'), "SF", "D58F12-U", 1 / 48, "1/A500"),
 ("D", '5/8" Type X W.R. gypsum board 4x12 (A100 note 5, restroom ceiling 2/A501)', buy('5/8" gypsum board, Type X W.R. (water resistant)'), "SF", "D58MM12-U", 1 / 48, "A100 n.5"),
 ("D", '5/8" W.R. gypsum board, mop sink shelf (1/A504)', buy('5/8" gypsum board, MOISTURE RESISTANT'), "SF", "D58MM12-U", 1 / 48, "1/A504"),
 ("D", 'Metal corner bead 10 ft', buy('METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim'), "LF", "DWB10-60", 0.1, "A100, A400"),
 ("D", 'Control joint 093 zinc 10 ft (ASTM C840)', buy('Control joint, gypsum board walls (ASTM C840, 30 ft max)'), "LF", "93EXP", 0.1, "1/A500"),
 ("D", 'All-purpose joint compound 3-1/2 gal box (template: 1 box per 200 SF of board)', None, "BOX", "APUB3.5", 1.0, "Level 4"),
 ("D", 'Paper joint tape 500 ft roll', buy('Joint tape, paper'), "LF", "DWT500W", 1 / 500, "Level 4"),
 ("F", 'FRP panel, pebbled white 4x10 (A700 B-3 PEBBLED FRP)', buy('FRP panels'), "SF", "FRPWH-10-MAR", 1 / 40, "A700 B-3"),
 ("F", 'FRP edge / end cap trim (A700 B-3 EDGE M370; equal)', edge, "LF", "FRPWH-CM10-NUD", 0.1, "A700 B-3"),
 ("F", 'FRP inside corner trim (A700 B-3 INSIDE CORNER M350; equal)', inside, "LF", "FRPWH-IC10-NUD", 0.1, "A700 B-3"),
 ("F", 'FRP outside corner trim (A700 B-3 OUTSIDE CORNER M360; equal)', pvc["PVC-RR-OC"]["lf"], "LF", "FRPWH-OC10-NUD", 0.1, "A700 B-3"),
 ("F", 'FRP division bar 10 ft (4 ft panel joints)', pvc["PVC-RR-DIV"]["lf"], "LF", "FRPWH-DB10-NUD", 0.1, "A700 B-3"),
]
board_total = sum(MS[k][2] for k in MS if "gypsum board" in k.lower() and MS[k][1] == "SF" and "Demolition" not in k)
# ---------------------------------------------------------------------------------------------- labor (template rates)
walls = can["walls"]
a362 = round(sum(w["length_ft"] * w["height_ft"] for w in walls if w.get("stud_size") == '3-5/8"'), 2)
a600 = round(sum(w["length_ft"] * w["height_ft"] for w in walls if w.get("stud_size") == '6"'), 2)
clg = can["ceilings"][0]["area_sf"]
sf = {k: MS[k][2] for k in MS}
LAB = [  # section, description, qty, unit, rate or None, rate source
 ("M", 'Framing labor 3-5/8" walls (wall SF = LF x stud height)', a362, "SF", 0.8, "Template 'Metal Framing' col K, 3 5/8\" METAL STUD rows (0.80 / SF)"),
 ("M", 'Framing labor 6" walls (wall SF)', a600, "SF", 1.0, "Template 'Metal Framing' col K, 6\" METAL STUD rows (1.00 / SF)"),
 ("M", 'Drywall grid ceiling labor (ceiling SF x 1.15)', round(clg * 1.15, 2), "SF", 1.0, "Template 'Metal Framing' K43 MAIN RUNNER (1.00 x ceiling SF x 1.15)"),
 ("M", 'Top of wall braces, angles, metal strapping / blocking install', buy('Metal stud brace to structure (size / gauge per the detail, see Where it comes from)'), "LF", None, "not in the template"),
 ("D", 'Hanging 5/8" Type X board', sf['5/8" gypsum board, Type X'], "SF", 0.78, "Template 'Drywall finish' J8 5/8\" GYP BD X (0.78 / SF)"),
 ("D", 'Hanging 5/8" W.R. board (walls + C-1 ceiling + shelf)', sf['5/8" gypsum board, Type X W.R. (water resistant)'] + sf['5/8" gypsum board, MOISTURE RESISTANT'], "SF", 0.5, "Template 'Drywall finish' J5 / J23 5/8\" GYP BD WR (0.50 / SF)"),
 ("D", 'Level 4 finishing (joint tape + mud), all board', board_total, "SF", 0.5, "Template 'Drywall finish' J27 LABOUR FOR FINISHING (0.50 / SF)"),
 ("D", 'Corner bead and control joint install', sf['METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim'] + sf['Control joint, gypsum board walls (ASTM C840, 30 ft max)'], "LF", None, "not in the template"),
 ("F", 'FRP panels and trim install', sf['FRP panels'], "SF", None, "not in the template"),
 ("X", 'Demolition of gypsum board and metal framing (D100 keys 9 / 27)', sf['Demolition - area of the element to demolish (SF = wall length x height / ceiling area, element area only)'], "SF", 1.25, "Template 'Demolition works' F23 wall demolition (1.25 / SF)"),
]
stud_track_lf = sum(MS[k][2] for k in MS if re.search(r"stud|track|runner|Header|brace|strapping", k, re.I) and MS[k][1] == "LF")
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
B.append(["CONSUMER CELLULAR - CENTENNIAL, CO - PRICING (quantities from Take-off rev4 FINAL; no new take-off pass)"])
B.append(["Material: FBM myfbm.com visitor price (guest branch CO-086 Englewood / Denver area), read " + str(fecha) +
          "; contractor account price may differ. Labor / OH / markups: the user's Proposal Template rates (source per row)."])
B.append([])
hdr = ["Section", "Item", "Qty", "Unit", "FBM code", "FBM price", "FBM unit", "Units of price per qty", "Material $", "N/SHEET / note"]
sec_rows = {"M": [], "D": [], "F": []}
B.append(["MATERIAL"]); B.append(hdr)
missing_sku = []
for s, dsc, q, u, code, k, nt in L:
    r = B.max_row + 1
    if dsc.startswith("All-purpose joint compound"):
        q = math.ceil(board_total / 200)
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
B.append(["Line", "Metal framing", "Drywall & finish L4", "FRP & trim", "Demolition"])
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
B.append(["Taxes 8.81% (template rate - [RATE TO CONFIRM] for Centennial, CO)", f"=B{tot}*0.0881"]); tax = B.max_row
B.append(["Total including tax", f"=ROUND(B{tot}+B{tax},0)"]); gt = B.max_row
B.append([]); B.append(["NOT PRICED (0 in the totals until confirmed):"])
for x in missing_rate:
    B.append(["[RATE TO CONFIRM]", x])
for x in missing_sku:
    B.append(["[PRICE TO CONFIRM]", x])
B.append(["[ALLOWANCE TO CONFIRM]", "Patch and repair of existing walls (D100 keynotes 3 / 4) - allowance by the estimator"])
B.append(["[ALLOWANCE TO CONFIRM]", "Exterior signage blocking (A300 / A301 note 2) - allowance by the estimator"])
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
put("C6", "Elite Retail Services (Vivian Tran) / Elder-Jones, Inc. (Mason Bender)"); put("G6", "YES - plans listed below (no project manual in the set)")
put("C7", "PROJECT NAME:"); put("G7", "ARCHITECT:")
put("C8", "CONSUMER CELLULAR - YOSEMITE PARK SHOPPING CENTER (store CO2)"); put("G8", "Sargenti Architects (project 15066-26)")
put("C9", "PROJECT ADDRESS:"); put("G9", "DATE OF PLANS:")
put("C10", "8283 S. AKRON ST., SUITE 110, CENTENNIAL, CO 80112"); put("G10", "10-15-2026 (90% set / permit set, 37 sheets)")
put("C11", "DATE OF PROPOSAL:"); put("G11", "ADDENDUM:")
P["C12"].value = datetime.datetime(2026, 11, 5); P["C12"].number_format = "mm-dd-yyyy"
ADD_OK = os.environ.get("ADDENDA_REVIEWED")     # rev4b (U-173): addenda reviewed 11-11-2026, no quantity impact
put("G12", "Rev 2 Permit Set 11-04-2026 (Elite / Elder-Jones addenda 11-05-2026) reviewed - no quantity impact" if ADD_OK else
    "Addenda issued 11-05-2026 (Elite / Elder-Jones) received - not included in this pricing")
put("C13", "PHONE NUMBER:"); put("G13", "E-MAIL:")
put("C14", TBC); put("G14", TBC)
put("C15", "Scope of Work:", bold=True)
put("C16", "We propose to supply the material, labor, and equipment necessary to complete the work in accordance with the plans "
           "and the scope listed below.")
put("C17", "(Please take special note of the scope description; we are not required to perform any items or tasks not specifically listed)")
put("C19", "1.-"); put("D19", "Division of work: METAL FRAMING, DRYWALL & DRYWALL FINISH LEVEL 4, FRP (CSI Div. 05 40 00 / 09 21 16 / 09 22 16).", bold=True)
inc = ["INCLUDED (quantities from the take-off rev4 FINAL, net before waste, with their sheet):"]
for r in ms:
    if (r[2] or 0) > 0:
        inc.append(f"• {r[0]}: {r[2]:,.2f} {r[1]}" + (f"  [{nsheet(r[8])}]" if nsheet(r[8]) else ""))
inc.append("• Partition types A3, C3, D, E3 per 1/A500 (A100); Level 4 finish on all gypsum board (rule U-147).")
put("C21", "\n".join(inc), size=9)
for rr in list(range(19, 48)):
    P.row_dimensions[rr].hidden = False
for rr in range(21, 44):                     # C21 spans the template rows 21-43
    P.row_dimensions[rr].height = max(15, 12.5 * len(inc) / 23)
for rr in (44, 45, 46, 47):
    P.row_dimensions[rr].height = 48
put("C44", "1a. Metal framing: interior partitions A3 / C3 / D / E3 (1/A500), 20 ga tracks (2/A500, 3/A500), long-leg slotted "
           "deflection track + nested C channel (4/A500), top of wall braces 3/A500, door / cased opening headers 2/A600, "
           "metal strapping / track / stud blocking (1-4/A104, 5/A402, A402 note 4, 5/P501), drywall grid at the restroom C-1 ceiling (2/A501).")
put("C45", "1b. Drywall & drywall finish Level 4: 5/8\" Type X board per partition type and face, 5/8\" Type X W.R. at the wet "
           "locations (A100 note 5) and the C-1 ceiling, metal corner bead, control joints (ASTM C840), tape and compound.")
put("C46", "1c. FRP B-3 (A700): restroom to 4'-0\" (A402) and mop sink alcove (1/A504) with edge, inside / outside corner and "
           "division bar trim (A700 B-3).")
put("C47", "1d. Demolition of existing gypsum board and metal framing (D100 keynotes 9 / 27), by area (SF).")
put("C48", "NOT INCLUDED / EXCLUSIONS:", bold=True)
ex = []
for r in scope:
    t = " ".join(str(x or "") for x in r[1:4])
    if re.search(r"\bEXCLUDED\b", t) and not str(r[0]).startswith(("RFI", "A/B")) and \
            not re.search(r"QUANTIFIED|CUANTIFICADO", str(r[2] or "")):
        n = re.sub(r"\s*\(EXCLUDED[^)]*\)", "", str(r[1]))
        why = re.sub(r"^.*?EXCLUDED[:\s-]*", "", str(r[3] or ""))[:120]
        ex.append(f"• {n}: {why}")
ex += ["• iPad backing plate 4/A104 ('BACKING PLATE BY G.C.')", "• Existing ceiling demolition (D100 keynote 7) - for lack of information",
       "• Bonds, permits and fees", "• Temporary utilities, dumpster, prevailing wages, shop drawings",
       ("• Work at the existing 3-hour fire-rated demising wall: rated assembly, firestopping and permanent identification above the ceiling (A100, A200, G003 Rev 2)"
        if ADD_OK else "• Addenda issued 11-05-2026 (not reviewed in this pricing)"), "• Anything not specifically listed in the INCLUDED scope"]
for m in [m for m in list(P.merged_cells.ranges) if 49 <= m.min_row <= 56]:
    P.unmerge_cells(str(m))
P.merge_cells("C49:J56")
put("C49", "\n".join(ex), size=9)
for rr in range(49, 57):
    P.row_dimensions[rr].height = max(15, 12.5 * len(ex) / 8 + 2)
put("C57", "NOTE: PROPOSAL HOLDS GOOD ONLY FOR THE ITEMS AND QUANTITIES LISTED ABOVE (TAKE-OFF REV4 FINAL)")
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
rows_p = [(69, "8.-", "Demolition works:", "I70", f"=PRICING!E{pr}"), (71, "9.-", "Metal framing:", "I72", f"=PRICING!B{pr}"),
          (73, "9.a-", "Drywall & drywall finish Level 4:", "I74", f"=PRICING!C{pr}"),
          (75, "9.b-", "FRP panels & trim:", "I76", f"=PRICING!D{pr}")]
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
put("D85", "Taxes (8.81% template rate - to confirm for Centennial):", wrap=False); P["I86"].value = f"=PRICING!B{tax}"
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
cl = ["RFI-01 (user decision 2026-11-05, option A, rule U-146): two printed deck heights and no drawn break - C3-01 studs to the higher printed deck 17'-1 9/16\" (A100).",
      "RFI-04 (user decision 2026-11-05, option A, rule U-147): no finish level printed - Level 4 on all gypsum board.",
      "RFI-02 (rule BOTH SIDES): type A# '5/8\" TYPE X ON EACH SIDE' (1/A500) - board on both faces.",
      "RFI-06: restroom C-1 ceiling on the 2/A501 drywall grid suspension system (ICC ESR 1289).",
      "RFI-03 / RFI-05 / RFI-07 / RFI-08: resolved with what the sheets print (2/A500, 3/A500, 4/A500, A100, 2/A400, A600 door 3C, 1/A504).",
      "Demolition is priced by area (SF); existing walls to demolish carried to the printed B.O. structure (D100, A100).",
      "Wood blocking / FRT plywood (Div. 06), fasteners, insulation, ACT, paint and MEP are excluded (see exclusions).",
      "Material prices: FBM (myfbm.com) list prices read 11-05-2026; FRP trim priced with equal products (Marlite M370 / M360 / M350 not listed)."]
if ADD_OK:
    cl += ["Addenda: Rev 2 Permit Set 11-04-2026 (city comments) and the architect / MEP response letters reviewed sheet by sheet - no change to partitions, board, ceilings or demolition; pricing unchanged.",
           "Patch and repair at the removed electrical panels (D100 keynote 12, Rev 2) is inside the patch & repair allowance."]
for x in cl:
    r += 1
    P.merge_cells(f"C{r}:J{r}")
    put(f"C{r}", x)
    P.row_dimensions[r].height = 30
P.print_area = f"A1:K{r}"
wb.save(OUT)
print("OK", OUT, "| missing rates:", len(missing_rate), "| missing SKUs:", len(missing_sku), "| FBM used:", len(used))
print("RATES:", missing_rate); print("SKUS:", missing_sku)
