#!/usr/bin/env python3
"""alcance_filtro.py — clasifica renglones del Material Summary por alcance, DETERMINISTA (regla 60.4).

Por qué existe (arbitraje #10, 16-oct-2026): una corrida sumó <n> LF de "7/8\" hat channel @16\" O.C." del
sistema de metal panel a la familia furring channel (+<n> LF). El sustrato del cladding (hat channel /
Z-girt / furring del metal panel, ACM, stucco, lath) es del instalador del cladding: EXCLUDED + RFI.
Ojo: el furring channel de drywall TAMBIÉN es un hat channel 7/8"; por eso "hat channel" solo no basta:
sin contexto de cladding la tool exige que el agente declare de qué es sustrato (no adivina).

ENTRADA (JSON):
{
  "rows": [{
      "id": "M12", "family": "furring channel",
      "description": "7/8\" hat channel @ 16\" O.C. at EPS-n metal panel",
      "qty": 120.0, "unit": "LF", "source": "2/A09.31",
      "substrate_of": "cladding",                     # opcional: drywall | cladding (obligatorio si ambiguo)
      "substrate_source": "2/A09.31"}]                # obligatorio con substrate_of
}
CLASIFICACIÓN (texto = family + description, sin mayúsculas):
  - SIEMPRE cladding: Z-girt / zee girt / girt, metal lath / stucco lath / diamond lath.
  - Furring-like (hat channel, furring, sub-girt, channel) + contexto cladding (metal panel, ACM, aluminum
    composite, stucco, EIFS, EPS-n, cladding, rainscreen, siding, fiber cement) -> cladding.
  - hat channel SIN contexto y sin substrate_of -> ValueError (ambigüedad: declarar con fuente).
  - substrate_of declarado manda (con substrate_source; p. ej. furring de un GB ceiling junto a stucco);
    si dice drywall pero hay palabra de "SIEMPRE cladding" -> ValueError (contradicción).
  - cladding -> estado EXCLUDED, qty fuera de su familia, RFI con delta = qty. Nunca queda en furring channel.
  - resto -> INCLUDED.
SALIDA: totales por familia (solo INCLUDED, por unidad) + excluidos + rfis + renglones con source.

Uso:  python3 alcance_filtro.py entrada.json salida.json
"""
import json
import re
import sys

RX_SRC = re.compile(r"^([A-Za-z0-9.]{1,6}/)*[A-Z]{1,3}-?\d[\w.\-]*$")
SIEMPRE = re.compile(r"\b(z[\s\-]?girts?|zee[\s\-]?girts?|girts?|(metal|stucco|diamond|expanded)[\s\-]+lath|lath)\b")
FURRING = re.compile(r"\b(hat[\s\-]?(channel|section)s?|furring|sub[\s\-]?girts?|channels?)\b")
HAT = re.compile(r"\bhat[\s\-]?(channel|section)s?\b")
CONTEXTO = re.compile(r"\b(metal[\s\-]+(wall[\s\-]+)?panels?|acm|aluminum[\s\-]+composite|stucco|eifs|eps[\s\-]?\d+|"
                      r"cladding|rain[\s\-]?screen|siding|fiber[\s\-]+cement)\b")


def _src(x, ctx):
    if not isinstance(x, str) or not x.strip():
        raise ValueError(f"{ctx}: falta 'source' (N/HOJA)")
    for p in re.split(r"\s*[,;·]\s*", x.strip()):
        tok = p.split()[0] if p.split() else ""
        if not RX_SRC.match(tok):
            raise ValueError(f"{ctx}: source '{p}' no tiene forma N/HOJA (ej. 2/X9.31)")
    return x.strip()


def clasificar(r):
    rid = r.get("id")
    txt = f"{r.get('family', '')} {r.get('description', '')}".lower()
    siempre = SIEMPRE.search(txt)
    furr = FURRING.search(txt)
    ctx = CONTEXTO.search(txt)
    decl = r.get("substrate_of")
    if decl is not None:
        if decl not in ("drywall", "cladding"):
            raise ValueError(f"{rid}: substrate_of debe ser drywall | cladding")
        _src(r.get("substrate_source"), f"{rid}.substrate_of")
        if decl == "drywall" and siempre:
            raise ValueError(f"{rid}: substrate_of=drywall contradice '{siempre.group(0)}' (60.4) — corregir dato o RFI")
        return decl == "cladding", f"declarado {decl} [{r['substrate_source']}]"
    if siempre:
        return True, f"'{siempre.group(0)}' = sustrato de cladding (60.4)"
    if furr and ctx:
        return True, f"'{furr.group(0)}' + contexto '{ctx.group(0)}' = sustrato de cladding (60.4)"
    if HAT.search(txt):
        raise ValueError(f"{rid}: 'hat channel' sin contexto — ambiguo (furring de drywall o sustrato de cladding): "
                         f"declarar substrate_of + substrate_source")
    return False, "alcance drywall / metal frame"


def calcular(data):
    rows = data.get("rows")
    if not isinstance(rows, list) or not rows:
        raise ValueError("'rows' vacío o ausente")
    tot, excl, rfis, filas, ids = {}, [], [], [], set()
    for r in rows:
        rid = r.get("id")
        if not rid or rid in ids:
            raise ValueError(f"renglón sin id o repetido: {rid!r}")
        ids.add(rid)
        src = _src(r.get("source"), rid)
        if not r.get("family") or not r.get("unit"):
            raise ValueError(f"{rid}: falta family o unit")
        try:
            q = float(r.get("qty"))
        except (TypeError, ValueError):
            raise ValueError(f"{rid}: qty no es número")
        if q < 0:
            raise ValueError(f"{rid}: qty negativa")
        clad, motivo = clasificar(r)
        est = "EXCLUDED" if clad else "INCLUDED"
        filas.append({"id": rid, "family": r["family"], "description": r.get("description"), "qty": q,
                      "unit": r["unit"], "estado": est, "motivo": motivo, "source": src})
        if clad:
            excl.append({"id": rid, "family_original": r["family"], "qty": q, "unit": r["unit"], "source": src})
            rfis.append({"id": rid, "source": src, "delta": q, "unit": r["unit"],
                         "texto": f"RFI: confirm {r.get('description') or r['family']} ({src}) is cladding substrate "
                                  f"by the cladding installer, excluded from metal frame / drywall scope; "
                                  f"add {round(q, 2)} {r['unit']} if included."})
        else:
            k = f"{r['family']} [{r['unit']}]"
            tot[k] = round(tot.get(k, 0.0) + q, 2)
    return {"totales_incluidos": tot, "excluidos": excl, "rfis": rfis, "renglones": filas}


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    try:
        out = calcular(json.load(open(argv[1])))
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as e:
        print(f"ERROR alcance_filtro.py: {e}", file=sys.stderr)
        return 1
    open(argv[2], "w").write(json.dumps(out, indent=1))
    print(json.dumps(out["totales_incluidos"]))
    for r in out["rfis"]:
        print(r["texto"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
