"""Writes FINAL_FOR_REVIEW/proceso/CAMBIOS_rev2.md: one line per change (item, rev1, rev2, delta, N/SHEET, rule) from
etapas/4_canon/rev4_log.json + the Material Summary NET comparison rev1 vs rev2 read from the two Excel files."""
import json, os, openpyxl
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.dirname(K)
log = json.load(open(os.path.join(K, "etapas", "4_canon", "rev4_log.json")))
def ms(p):
    wb = openpyxl.load_workbook(p, data_only=True)
    return {r[0]: (r[1], r[2]) for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True) if r and r[0]}
r1 = ms(os.path.join(S, "cfa_calc_rev3", "etapas", "8_excel", "CFA2284_RiverPoint_Takeoff_FINAL_rev3.xlsx"))
r2 = ms(os.path.join(K, "etapas", "8_excel", "CFA2284_RiverPoint_Takeoff_FINAL_rev4.xlsx"))
L = ["# CAMBIOS rev4 - CFA #2284 River Point (RFIs answered from the drawings, user order 3-nov)", "",
     "Excel produced by plantilla_excel.py armar (skill v81cf11 = v81cf10 (gate A_RFI_BARRIDO) + gate A_MARKUPS_EXCEL) with the reglas.py gate passing; every quantity computed by canon.py / accesorios.py from the corrected canon. rev1-rev3 files untouched.", "",
     "| # | Item | rev3 | rev4 | Delta | N/SHEET | Rule / decision |", "|---|---|---|---|---|---|---|"]
for i, x in enumerate(log, 1):
    L.append(f"| {i} | {x['item']} | {x['rev3']} | {x['rev4']} | {x['delta']} | {x['src']} | {x['rule']} |")
n = len(log)
extra = [("Pending Items", "17 RFIs history (12 open in rev3)", "open RFIs only, each with its full sweep (sheets / terms / grep); resolved ones listed in the Scope Checklist as 'RESOLVED from drawings'", "list", "-", "user order 3-nov + A_RFI_BARRIDO")]
for j, (a, b, cc, d, e, f) in enumerate(extra, n + 1):
    L.append(f"| {j} | {a} | {b} | {cc} | {d} | {e} | {f} |")
L += ["", "## Material Summary NET rev3 -> rev4", "", "| Row | Unit | rev3 | rev4 | Delta |", "|---|---|---|---|---|"]
for k in list(r1) + [k for k in r2 if k not in r1]:
    a, b = r1.get(k, (None, None)), r2.get(k, (None, None))
    va, vb = a[1] or 0, b[1] or 0
    if (va or vb) and abs(float(va) - float(vb)) > 0.004 or (k not in r1 and vb) or (k not in r2 and va):
        L.append(f"| {k} | {b[0] or a[0]} | {va if k in r1 else '-'} | {vb if k in r2 else '-'} | {round(float(vb) - float(va), 2):+} |")
fd = os.path.join(S, "cfa_final", "FINAL_FOR_REVIEW", "proceso")
open(os.path.join(fd, "CAMBIOS_rev4.md"), "w").write("\n".join(L) + "\n")
open(os.path.join(K, "etapas", "CAMBIOS_rev4.md"), "w").write("\n".join(L) + "\n")
print(len(L), "lines")
# full breakdown of the 1/2" gypsum board row (trazabilidad cuts it at 500 characters: tool limit)
C4 = os.path.join(K, "etapas", "4_canon", "out")
bo = json.load(open(os.path.join(C4, "board_out.json")))
fo = json.load(open(os.path.join(C4, "familias_out.json")))
B = ["# 1/2\" gypsum board regular - full breakdown (rev4)", "", "| Source | SF | Operation |", "|---|---|---|"]
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
open(os.path.join(fd, "BREAKDOWN_half_inch_gyp_rev4.md"), "w").write("\n".join(B) + "\n")
print("breakdown total", round(tot, 2), fo["familias"].get('1/2" gyp board'))
