"""Writes FINAL_FOR_REVIEW/proceso/CAMBIOS_rev2.md: one line per change (item, rev1, rev2, delta, N/SHEET, rule) from
etapas/4_canon/rev2_log.json + the Material Summary NET comparison rev1 vs rev2 read from the two Excel files."""
import json, os, openpyxl
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.dirname(K)
log = json.load(open(os.path.join(K, "etapas", "4_canon", "rev2_log.json")))
def ms(p):
    wb = openpyxl.load_workbook(p, data_only=True)
    return {r[0]: (r[1], r[2]) for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True) if r and r[0]}
r1 = ms(os.path.join(S, "cfa_calc", "etapas", "8_excel", "CFA2284_RiverPoint_Takeoff_FINAL_rev1.xlsx"))
r2 = ms(os.path.join(K, "etapas", "8_excel", "CFA2284_RiverPoint_Takeoff_FINAL_rev2.xlsx"))
L = ["# CAMBIOS rev2 - CFA #2284 River Point (audit step 11 + coverage step 12 corrections)", "",
     "Excel produced by plantilla_excel.py armar (skill v81cf4) with the reglas.py gate passing; every quantity computed by canon.py / accesorios.py from the corrected canon. rev1 files untouched.", "",
     "| # | Item | rev1 | rev2 | Delta | N/SHEET | Rule / decision |", "|---|---|---|---|---|---|---|"]
for i, x in enumerate(log, 1):
    L.append(f"| {i} | {x['item']} | {x['rev1']} | {x['rev2']} | {x['delta']} | {x['src']} | {x['rule']} |")
n = len(log)
extra = [("Bluebeam PDF", "Page Labels 6 / 7 on demo pages; DEMO contents in Spanish; MB-01 Subject M3.5; markup SF = L x H; no area markups",
          "Page Label = A-050 / A-052 / A-202 / A-221; English states; MB-01 Subject INFILL; Excel board SF of every metal wall / soffit side listed on the legend page (verificar keeps the tool's LF x H Contents); polygons for 5 gyp ceilings, 2 soffit bottoms, Level 5, hatch shaft, 2 pin & sleeve recesses",
          "format", "A-050, A-052, A-202, A-221", "decision 19"),
         ("Cement board joints (1,800.27 SF)", "no joint treatment", "alkali-resistant mesh tape 666.1 LF (own row) + setting-type compound 129.62 lb (note on that row: no LB row in the template)", "+666.1 LF mesh tape, +129.62 lb setting compound", "C09250 2.4.B.2 / 2.4.D.2 / 3.5.E (A-909)", "decision 9"),
         ("Joint compound / tape driver", "gyp board only, unexplained", "note: driver = gypsum board SF only; cement board joints in the mesh tape row", "text", "C09250 2.4 / A-909", "decision 9"),
         ("1/2\" gyp row breakdown", "cut off after 3 sources", "full breakdown in proceso/BREAKDOWN_half_inch_gyp_rev2.md (tool cuts the Excel cell at 500 characters)", "-", "-", "decision 17 (tool limit)"),
         ("Joint compound / tape driver after the MR board change", "driver without the 148.02 SF of 1/2\" MR board (tool driver list)", "tool fix BE-CF14 (v81cf4 accesorios.BOARD_DRIVER includes 1/2\" MR and 5/8\" foil-backed): driver = 1/2\" regular + 5/8\" ceiling + 1/2\" MR", "compound 128.43 -> 139.08 lb, tape 659.97 -> 714.74 LF", "C09250 2.4 / A-909", "BE-CF14"),
         ("Partition Takeoff MB-01", "merged in row M3.5-01+MB-01 (type M3.5)", "own type INFILL (6\" metal, D3/A-624)", "row split", "D3/A-624", "decision 4 / 17"),
         ("OTHER FRAMING block subtotal", "no subtotal", "unchanged: the fixed template prints no subtotal for OTHER FRAMING (tool limit, see TOOL_LIMITS)", "-", "-", "decision 17 (tool limit)"),
         ("Hidden sheet _reglas", "present", "kept: it is the plantilla_excel.py seal of the reglas.py gate (same fixed format in every project; bitacora.py rejects a workbook without it); the 6 visible sheets are unchanged", "-", "-", "decision 20"),
         ("Inputs C26 lumber stock note", "precedent of another project (estimator decision 2026-10-27)", "estimator standing input", "text", "-", "decision 18"),
         ("Demolition vs new plan cross table", "missing", "proceso/DEMO_CRUCE.md", "-", "A-050, A-052, A-202", "decision 16"),
         ("Review items 1 / 7 wording", "MB-01 3-5/8\"; M3.5 'A 3-5/8\"'", "MB-01 6\" (RFI-17 closed); M3.5 'A 8\" (as loaded)'", "text", "D3/A-624, A2/A-605", "decision 17")]
for j, (a, b, cc, d, e, f) in enumerate(extra, n + 1):
    L.append(f"| {j} | {a} | {b} | {cc} | {d} | {e} | {f} |")
L += ["", "## Material Summary NET rev1 -> rev2", "", "| Row | Unit | rev1 | rev2 | Delta |", "|---|---|---|---|---|"]
for k in list(r1) + [k for k in r2 if k not in r1]:
    a, b = r1.get(k, (None, None)), r2.get(k, (None, None))
    va, vb = a[1] or 0, b[1] or 0
    if (va or vb) and abs(float(va) - float(vb)) > 0.004 or (k not in r1 and vb) or (k not in r2 and va):
        L.append(f"| {k} | {b[0] or a[0]} | {va if k in r1 else '-'} | {vb if k in r2 else '-'} | {round(float(vb) - float(va), 2):+} |")
fd = os.path.join(S, "cfa_final", "FINAL_FOR_REVIEW", "proceso")
open(os.path.join(fd, "CAMBIOS_rev2.md"), "w").write("\n".join(L) + "\n")
open(os.path.join(K, "etapas", "CAMBIOS_rev2.md"), "w").write("\n".join(L) + "\n")
print(len(L), "lines")
# full breakdown of the 1/2" gypsum board row (trazabilidad cuts it at 500 characters: tool limit)
C4 = os.path.join(K, "etapas", "4_canon", "out")
bo = json.load(open(os.path.join(C4, "board_out.json")))
fo = json.load(open(os.path.join(C4, "familias_out.json")))
B = ["# 1/2\" gypsum board regular - full breakdown (rev2)", "", "| Source | SF | Operation |", "|---|---|---|"]
tot = 0.0
for f_ in bo["caras"]:
    if f_["board"] == "1/2 regular":
        B.append(f"| {f_['wall']} {f_['room']} | {f_['sf']} | {f_['operacion']} |"); tot += f_["sf"]
for r in fo["filas"]:
    if r.get("familia") == "1/2\" gyp board":
        v = r.get("valor")
        import re as _re
        m = _re.findall(r"=\s*([\d,]+(?:\.\d+)?)\s*SF", str(r.get("operacion")))
        v = float(m[-1].replace(",", "")) if m else 0.0
        B.append(f"| {r.get('ref')} | {v} | {str(r.get('operacion')).split(' (Estimator')[0]} |"); tot += v
can = json.load(open(os.path.join(K, "etapas", "4_canon", "takeoff_canon.json")))
for cl in can["ceilings"]:
    if cl.get("board") == "1/2 regular":
        B.append(f"| soffit bottom {cl['room']} | {cl['area_sf']} | RCP area ({cl['detail']}) |"); tot += cl["area_sf"]
B.append(f"| TOTAL | {round(tot, 2)} | Material Summary NET {fo['familias'].get(chr(49) + '/2\" gyp board')} SF |")
open(os.path.join(fd, "BREAKDOWN_half_inch_gyp_rev2.md"), "w").write("\n".join(B) + "\n")
print("breakdown total", round(tot, 2), fo["familias"].get('1/2" gyp board'))
