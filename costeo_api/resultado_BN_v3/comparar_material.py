#!/usr/bin/env python3
"""Material Summary del Excel del runner vs rev13: % por material, principales y fasteners por separado.
Uso: python3 comparar_material.py <excel_runner> <excel_rev13>   -> tablas markdown en stdout"""
import re
import sys

import openpyxl

FAST = re.compile(r"screw|pin\b|pins|anchor|P\.A\.F|fastener|wire|tek|nail|clip|sealant|tape|compound|mud|adhesive|"
                  r"powder|bolt|HUS", re.I)


def ms(p):
    ws = openpyxl.load_workbook(p, data_only=True)["Material Summary"]
    out = {}
    for r in list(ws.iter_rows(values_only=True))[3:]:
        if r and r[0] and isinstance(r[2], (int, float)):
            out[str(r[0]).strip()] = (r[2], r[1])
    return out


def main(a, b):
    x, y = ms(a), ms(b)
    for titulo, es in (("Principales", False), ("Fasteners y consumibles", True)):
        print(f"### {titulo}\n| Material | Unit | rev13 | corrida #3 | Δ |\n|---|---|---|---|---|")
        ty = tx = 0
        for k in sorted(set(x) | set(y), key=lambda k: -(y.get(k, (0,))[0] or 0)):
            if bool(FAST.search(k)) != es:
                continue
            vy, vx = (y.get(k) or (None, None))[0], (x.get(k) or (None, None))[0]
            u = (y.get(k) or x.get(k))[1]
            if vx is not None and vy:
                d = f"{(vx - vy) / vy * 100:+.1f} %"
            elif not vx and not vy:
                d = "0 = 0" if vx is not None and vy is not None else ("falta (0 en rev13)" if vy is not None else "0")
            else:
                d = "new" if vx else "−100 % (falta)"
            print(f"| {k[:90]} | {u} | {vy if vy is not None else '—'} | {vx if vx is not None else '—'} | {d} |")
        print()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
