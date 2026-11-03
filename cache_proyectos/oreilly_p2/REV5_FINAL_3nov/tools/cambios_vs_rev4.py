#!/usr/bin/env python3
"""Delta por material rev4 (pasada 1) -> rev5 (pasada 2 FINAL + v81cf25), NET antes de waste, leído de los dos Excel
(nada tecleado). Las filas se agrupan por familia con reglas de nombre (los dos Excel usan nombres distintos).
Uso: cambios_vs_rev4.py <rev4.xlsx> <rev5.xlsx> <salida.md>"""
import re
import sys

import openpyxl

FAM = [  # (familia, regex sobre el nombre del renglón)
    ("Bottom track 3-5/8\"", r"^Bottom track 3-5/8"), ("Bottom track 6\" (all)", r"^Bottom track 6"),
    ("Bottom track 8\" (all)", r"^Bottom track 8|^Bottom track - other framing.*800T"),
    ("Bottom track 6\" other framing (600T)", r"^Bottom track - other framing.*600T"),
    ("Bottom track roof step / heads", r"^Bottom track - roof step"),
    ("Top track 3-5/8\"", r"^Top / deflection track 3-5/8"), ("Top track 6\" (all)", r"^Top / deflection track 6"),
    ("Top track 8\" (all)", r"^Top / deflection track 8|^Top / deflection track - other framing.*800T"),
    ("Top track 6\" other framing (600T)", r"^Top / deflection track - other framing.*600T"),
    ("Top track roof step / heads", r"^Top track - roof step"), ("Deep-leg slotted deflection track", r"^Deep-leg slotted"),
    ("Z-furring 1-1/2\"", r"Z-furring channel"), ("8\" stud", r"^8\" stud"), ("6\" stud (all)", r"^6\" metal stud"),
    ("3-5/8\" stud (all)", r"^3-5/8\" metal stud"), ("Ceiling / soffit track", r"^Ceiling"),
    ("Bracing C.R. channel", r"^Bracing"), ("Header / box beam", r"^Header"), ("Glass mat sheathing", r"glass mat"),
    ("FRT blocking", r"^Blocking FRT"), ("Metal stud blocking", r"^Metal stud blocking"),
    ("5/8\" Type X", r"Type X$"), ("5/8\" Type X W.R.", r"Type X W\.R\."), ("Clips + clip angles", r"^Clip angles"),
    ("FCB43.5 framing clips", r"^Framing clips per stud"), ("Resilient channel", r"^Resilient channel"),
    ("1/4\" gypsum board", r"^1/4\" gypsum"), ("Flat strap bracing", r"flat strap"), ("Z-furring runner", r"^Z-furring runner"),
    ("W-4 panels", r"^Sanitary wall panel"), ("W-4 trim", r"^W-4 panel trim"), ("Track brace strut splice", r"^Track brace"),
    ("Metal trim (all)", r"^METAL trim"), ("Control joints", r"^Control joint"), ("FRT plywood", r"^FRT plywood"),
    ("Additional head track", r"^Additional head track"), ("Jamb return", r"jamb return"),
    ("Joint compound", r"^Joint compound"), ("Joint tape", r"^Joint tape"), ("Level 5", r"^Level 5")]


def fams(p):
    wb = openpyxl.load_workbook(p, data_only=True)
    out = {}
    for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True):
        if not (r[0] and isinstance(r[2], (int, float))):
            continue
        f = next((k for k, rx in FAM if re.search(rx, str(r[0]), re.I)), None)
        if f:
            out[f] = (r[1], round(out.get(f, (r[1], 0))[1] + r[2], 2))
    return out


a, b = fams(sys.argv[1]), fams(sys.argv[2])
L = ["| Material | Unit | rev4 | rev5 | Delta | Delta % |", "|---|---|---|---|---|---|"]
for f, _ in FAM:
    if f not in a and f not in b:
        continue
    u = (a.get(f) or b.get(f))[0]
    x, y = (a.get(f) or (u, 0))[1], (b.get(f) or (u, 0))[1]
    if abs(x) < 1e-9 and abs(y) < 1e-9:
        continue
    d = round(y - x, 2)
    L.append(f"| {f} | {u} | {x:,.2f} | {y:,.2f} | {d:+,.2f} | {(d / x * 100):+.1f} % |" if x else
             f"| {f} | {u} | {x:,.2f} | {y:,.2f} | {d:+,.2f} | new |")
open(sys.argv[3], "w", encoding="utf-8").write("\n".join(L) + "\n")
print("\n".join(L))
