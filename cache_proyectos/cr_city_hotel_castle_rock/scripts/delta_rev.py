#!/usr/bin/env python3
"""Delta por material (Material Summary, NET) rev1 -> rev2. Salida: etapas/DELTA_rev1_rev2.md"""
import openpyxl, sys
W = '/root/cr/work'
A = f'{W}/archivo_rev1/8_excel/CR_City_Hotel_Takeoff_FINAL_rev1.xlsx'
B = f'{W}/etapas/8_excel/CR_City_Hotel_Takeoff_FINAL_rev2.xlsx'
def ms(p):
    ws = openpyxl.load_workbook(p, data_only=True)['Material Summary']
    hdr, out = None, {}
    for r in ws.iter_rows(values_only=True):
        if hdr is None:
            if r and any(str(x).strip().lower() == 'net' for x in r if x):
                hdr = [str(x or '').strip().lower() for x in r]
            continue
        if not r or not r[hdr.index('material') if 'material' in hdr else 0]:
            continue
        m = str(r[hdr.index('material') if 'material' in hdr else 0]).strip()
        try:
            out[m] = (float(r[hdr.index('net')] or 0), str(r[hdr.index('unit')] if 'unit' in hdr else ''))
        except (TypeError, ValueError):
            pass
    return out
a, b = ms(A), ms(B)
L = ["# DELTA Material Summary (NET) rev1 -> rev2 - CR City Hotel", "", "| Material | Unit | rev1 | rev2 | Delta |", "|---|---|---|---|---|"]
for m in list(a) + [m for m in b if m not in a]:
    x, y = a.get(m, (0, ''))[0], b.get(m, (0, ''))[0]
    u = (a.get(m) or b.get(m))[1]
    L.append(f"| {m} | {u} | {x:,.2f} | {y:,.2f} | {y - x:+,.2f} |")
open(f'{W}/etapas/DELTA_rev1_rev2.md', 'w').write("\n".join(L) + "\n")
print("\n".join(L))
