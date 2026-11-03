"""Writes FINAL_FOR_REVIEW/proceso/CAMBIOS_rev2.md: one line per change (item, rev1, rev2, delta, N/SHEET, rule) from
etapas/4_canon/rev3_log.json + the Material Summary NET comparison rev1 vs rev2 read from the two Excel files."""
import json, os, openpyxl
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.dirname(K)
log = json.load(open(os.path.join(K, "etapas", "4_canon", "rev3_log.json")))
def ms(p):
    wb = openpyxl.load_workbook(p, data_only=True)
    return {r[0]: (r[1], r[2]) for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True) if r and r[0]}
r1 = ms(os.path.join(S, "cfa_calc_rev2", "etapas", "8_excel", "CFA2284_RiverPoint_Takeoff_FINAL_rev2.xlsx"))
r2 = ms(os.path.join(K, "etapas", "8_excel", "CFA2284_RiverPoint_Takeoff_FINAL_rev3.xlsx"))
L = ["# CAMBIOS rev3 - CFA #2284 River Point (back-check of rev2: 6 defects)", "",
     "Excel produced by plantilla_excel.py armar (skill v81cf8 = v81cf7 + tool fixes T1-T6, tools/CAMBIOS_tools_v81cf8.md) with the reglas.py gate passing; every quantity computed by canon.py / accesorios.py from the corrected canon. rev1 / rev2 files untouched.", "",
     "| # | Item | rev2 | rev3 | Delta | N/SHEET | Rule / decision |", "|---|---|---|---|---|---|---|"]
for i, x in enumerate(log, 1):
    L.append(f"| {i} | {x['item']} | {x['rev2']} | {x['rev3']} | {x['delta']} | {x['src']} | {x['rule']} |")
n = len(log)
extra = [("Setting-type compound at cement board joints", "note only (not bought)", "own LB row (family setting-type joint compound at cement board, waste none)", "+129.62 lb in Net / Purchase", "C09250 2.4.D.2 / 3.5.E (A-909)", "T3"),
         ("Mesh tape waste", "6 % (purchase 706.07 LF)", "0 % yield row (purchase 666.10 LF)", "-39.97 LF purchase", "Inputs C23 / C24", "T4"),
         ("OTHER FRAMING block", "no subtotal", "SUBTOTAL OTHER FRAMING row (LF + board SF)", "format", "-", "T5"),
         ("Workbook sheets", "7 (hidden _reglas seal)", "6 fixed sheets; seal in <excel>.sello.json next to the work Excel", "format", "-", "T6"),
         ("Scope Checklist ALC-04", "MB-01 3-5/8\"; 'no deflection track printed'", "MB-01 6\" (D3/A-624); C1/S-801 slotted track loaded; strongback own row", "text", "D3/A-624, C1/S-801", "P2"),
         ("Marked A-221 image", "soffit sides only", "gyp ceilings, soffit bottoms, Level 5, hatch shaft drawn with their take-off labels", "image", "A-221", "P3")]
for j, (a, b, cc, d, e, f) in enumerate(extra, n + 1):
    L.append(f"| {j} | {a} | {b} | {cc} | {d} | {e} | {f} |")
L += ["", "## Material Summary NET rev2 -> rev3", "", "| Row | Unit | rev2 | rev3 | Delta |", "|---|---|---|---|---|"]
for k in list(r1) + [k for k in r2 if k not in r1]:
    a, b = r1.get(k, (None, None)), r2.get(k, (None, None))
    va, vb = a[1] or 0, b[1] or 0
    if (va or vb) and abs(float(va) - float(vb)) > 0.004 or (k not in r1 and vb) or (k not in r2 and va):
        L.append(f"| {k} | {b[0] or a[0]} | {va if k in r1 else '-'} | {vb if k in r2 else '-'} | {round(float(vb) - float(va), 2):+} |")
fd = os.path.join(S, "cfa_final", "FINAL_FOR_REVIEW", "proceso")
open(os.path.join(fd, "CAMBIOS_rev3.md"), "w").write("\n".join(L) + "\n")
open(os.path.join(K, "etapas", "CAMBIOS_rev3.md"), "w").write("\n".join(L) + "\n")
print(len(L), "lines")
# full breakdown of the 1/2" gypsum board row (trazabilidad cuts it at 500 characters: tool limit)
C4 = os.path.join(K, "etapas", "4_canon", "out")
bo = json.load(open(os.path.join(C4, "board_out.json")))
fo = json.load(open(os.path.join(C4, "familias_out.json")))
B = ["# 1/2\" gypsum board regular - full breakdown (rev3)", "", "| Source | SF | Operation |", "|---|---|---|"]
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
open(os.path.join(fd, "BREAKDOWN_half_inch_gyp_rev3.md"), "w").write("\n".join(B) + "\n")
print("breakdown total", round(tot, 2), fo["familias"].get('1/2" gyp board'))
