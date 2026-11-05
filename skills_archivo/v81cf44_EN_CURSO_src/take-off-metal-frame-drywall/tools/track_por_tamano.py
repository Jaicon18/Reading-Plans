#!/usr/bin/env python3
"""track_por_tamano.py — R71.8 (v71, arbitraje #19): desglose de bottom track y top / deflection track POR TAMAÑO de
stud (y gauge cuando el wall lo trae) para el Material Summary. La familia total sigue saliendo de canon.py /
corridas.py; esta tool solo la reparte y declara el resto.

Regla: cada wall del canon con track (element wall / chase / pier / column_wrap / door_bulkhead o sin element)
aporta length_ft × rows al tamaño de su `stud_size` (gauge aparte si `gauge` / `stud_gauge` viene, p. ej. el track de
parapet 54 mil). Lo que la familia trae y los walls no explican (track de roof step, vestibule head, cripples sobre
R.O., etc.) va en un renglón "other (see source)" con su operación; un resto NEGATIVO = falla (el desglose excede la
familia: revisar rows / walls duplicados).

Uso:  python3 track_por_tamano.py takeoff_canon.json <bottom_total_LF> [top_total_LF]
"""
import json
import re
import sys
from collections import OrderedDict

CON_TRACK = (None, "wall", "chase", "pier", "column_wrap", "door_bulkhead")
TAM = re.compile(r'(\d+-\d+/\d+"|\d+(?:\.\d+)?")')
GAUGE = re.compile(r"(\d{2})\s?mil|S\d{3}-(\d{2})\b|(\d{2})\s?GA\b", re.I)   # primer gauge legible; texto ambiguo = sin gauge


def tamano(w):
    m = TAM.search(str(w.get("stud_size") or ""))
    t = m.group(1) if m else "?"
    g = w.get("gauge") or w.get("stud_gauge")
    if isinstance(g, dict):
        g = g.get("value")
    m = GAUGE.search(str(g or ""))
    if not m:
        return t
    mil = m.group(1) or m.group(2)
    return f"{t} {mil} mil" if mil else f"{t} {m.group(3)} GA"


def desglose(canon, total):
    filas = OrderedDict()
    for w in canon.get("walls") or []:
        if w.get("element") not in CON_TRACK:
            continue
        lf = float(w.get("length_ft") or 0) * int(w.get("rows", 1) or 1)
        if lf <= 0:
            continue
        k = tamano(w)
        filas[k] = filas.get(k, 0.0) + lf
    s = sum(filas.values())
    resto = round(float(total) - s, 2)
    out = {"por_tamano": {k: round(v, 2) for k, v in filas.items()}, "suma": round(s, 2), "familia": float(total),
           "other": resto, "fallas": []}
    if resto < -0.01:
        out["fallas"].append(f"R71.8 el desglose por tamaño ({round(s, 2)}) excede la familia ({total}): rows o walls "
                             f"duplicados")
    if "?" in filas:
        out["fallas"].append("R71.8 walls con track sin stud_size legible: tamaño '?'")
    return out


def main(argv):
    if len(argv) not in (3, 4):
        print(__doc__)
        return 2
    canon = json.load(open(argv[1]))
    rc = 0
    for nombre, tot in (("bottom track", argv[2]), ("top / deflection track", argv[3] if len(argv) == 4 else argv[2])):
        r = desglose(canon, float(tot))
        print(f"{nombre}: familia {r['familia']}")
        for k, v in r["por_tamano"].items():
            print(f"  {k:14s} {v:10.2f} LF")
        print(f"  {'other':14s} {r['other']:10.2f} LF (track que no es de walls: citar su fuente)")
        for x in r["fallas"]:
            print("FALLA", x)
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
