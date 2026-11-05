#!/usr/bin/env python3
"""alturas_exactas.py — R80f.32 (Chuze FINAL6, 3-nov-2026): alturas ft-in EXACTAS en el canon.

Problema: los lectores escribían alturas redondeadas a 2-3 decimales (22'-10" = 22.83, 14'-5" = 14.42, 12'-1" = 12.083);
la compuerta BE-119 (Depth vs altura IMPRESA, ±0.001 ft) las marca RED y el material se calcula con la altura truncada.
Regla: toda altura del canon (height_ft / head_ft / sill_ft en walls, faces, height_zones, openings, ceilings, soffits)
que es el redondeo de un valor en pulgadas enteras (o 1/2", o 1/8") se reemplaza por el valor exacto (4 decimales).
También el "value" de una altura guardada como {value, source} (deck_height, hanger_drop_ft) y se reportan los
misc_items cuya operación escrita usa una altura redondeada (su qty se recalcula en el take-off).
Un número que no es el redondeo de ninguna de esas rejillas no se toca (se reporta).

Uso: python3 alturas_exactas.py <takeoff_canon.json> [--check]   (--check: no escribe; rc 1 si hay alturas redondeadas)
Escribe <canon>.alturas_exactas.json (cada cambio: ruta, antes, después, ft-in). Test: test_chuze_r80f8_11.py (test_alturas_exactas)
"""
import json
import os
import re
import sys

CLAVES = ("height_ft", "head_ft", "sill_ft")
REJILLAS = (12, 24, 96)          # pulgada, 1/2", 1/8"


def _dec(v):
    s = repr(float(v))
    return len(s.split(".")[1]) if "." in s and "e" not in s else 0


def exacta(v):
    """-> valor exacto (4 dec) si v es el redondeo de una altura en la rejilla más gruesa posible; si no, None."""
    v = float(v)
    n = _dec(v)
    if n == 0 or n > 3:
        return None
    for g in REJILLAS:
        e = round(v * g) / g
        if abs(e - v) > 1e-9 and round(e, n) == v:
            return round(e, 4)
        if abs(e - v) <= 1e-9:
            return None              # ya es exacta
    return None


def ftin(v):
    t = round(v * 96)
    pies, oct_ = divmod(t, 96)
    pul = oct_ / 8
    return f"{pies}'-{pul:g}\""


PADRES = re.compile(r"(?i)height|drop|deck|stud_h")      # {"value": n} de una altura (deck_height, hanger_drop_ft)


def recorrer(o, ruta="", padre=""):
    if isinstance(o, dict):
        for k, v in o.items():
            num = isinstance(v, (int, float)) and not isinstance(v, bool)
            if num and (k in CLAVES or (k == "value" and PADRES.search(padre))):
                yield o, k, f"{ruta}.{k}"
            else:
                yield from recorrer(v, f"{ruta}.{k}", k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from recorrer(v, f"{ruta}[{i}]", padre)


def corregir(canon):
    cambios = []
    for d, k, ruta in recorrer(canon):
        e = exacta(d[k])
        if e is not None:
            cambios.append({"ruta": ruta, "antes": d[k], "despues": e, "ft_in": ftin(e)})
            d[k] = e
    return cambios


def ops_redondeadas(canon):
    """misc_items cuya operación escrita usa una altura redondeada (p. ej. 'deck H - top of wall T' con H, T redondeados): su qty es
    un número precalculado que esta tool no recalcula -> se reportan; el take-off los recalcula con su fórmula."""
    out = []
    for i, m in enumerate(canon.get("misc_items") or []):
        op = str(m.get("op") or "")
        for x in re.findall(r"(?i)(?:deck|top of wall|face height|height per face \(|(?<!ROUNDUP)\(|\+)\s*(\d{1,2}\.\d{2,3})(?![\d])", op):
            if exacta(float(x)) is not None:
                out.append({"i": i, "ref": m.get("ref"), "valor": float(x), "exacta": exacta(float(x))})
                break
    return out


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    p = argv[1]
    c = json.load(open(p, encoding="utf-8"))
    cambios = corregir(c)
    ops = ops_redondeadas(c)
    print(f"alturas_exactas: {len(cambios)} alturas redondeadas -> exactas; {len(ops)} misc_items con operación sobre una "
          f"altura redondeada (recalcular su qty)")
    for x in ops[:20]:
        print(f"  misc_items[{x['i']}] {x['ref']}: usa {x['valor']} (exacta {x['exacta']})")
    for x in cambios[:15]:
        print(f"  {x['ruta']}: {x['antes']} -> {x['despues']} ({x['ft_in']})")
    if "--check" in argv:
        return 1 if (cambios or ops) else 0
    if cambios:
        json.dump(c, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        lp = p + ".alturas_exactas.json"          # se AGREGA al registro de corridas anteriores (no se pisa)
        prev = json.load(open(lp, encoding="utf-8")) if os.path.isfile(lp) else []
        json.dump(prev + cambios, open(lp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
