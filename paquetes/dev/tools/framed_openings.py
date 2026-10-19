#!/usr/bin/env python3
"""framed_openings.py v64 — LF de framed openings MEP por perímetro, DETERMINISTA (reglas 60.9, 60.10, 58.4).

v64 (decisión del usuario #12, 2026-10-16): ductos / fire dampers / air devices de wall NO se enmarcan como
abertura: sin header ni sill aunque no quepan en el stud bay -> estado NOT_FRAMED, 0 LF, y NO van a
to_header_sill (BOA: -<n> header, -<n> sill). Solo los items de wall que no son de aire (access panel,
other) y no caben en el stud bay siguen a headers.py (TO_HEADER_SILL).

Por qué existe (arbitraje #10, 16-oct-2026): una corrida cargó la medida del catálogo cuando la descripción
y el dibujo daban otra (+64 LF) y contó downlights de 3.5" que caben entre furring (+28 LF); la otra metió
ductos de wall más grandes que el stud bay (van a header/sill, 58.4). Aquí la tool decide con reglas fijas.

ENTRADA (JSON):
{
  "modules": {"wall_stud_bay_in": 14.375,                         # opcional, default 60.10
              "ceiling_furring_oc_in": {"value": 16, "source": "2/A09.31"}},   # obligatorio si hay ceiling
  "items": [{
      "tag": "R-11C", "category": "light",          # light | air_device | access_panel | other
      "location": "ceiling",                        # ceiling | wall
      "shape": "rect",                              # rect | round (round: width_in = diámetro, length no aplica)
      "qty": 4, "width_in": 4.0, "width_source": "E00.01 <código de catálogo>",   # v66 obligatorio
      "length_ft": {"desc": 12.0, "catalog": 20.0, "drawn": 12.0},   # cualquiera de las tres; al menos una
      "length_override": {"value": 12.0, "source": "E02.01", "rfi": "..."},  # solo si el dibujo no resuelve
      "source": "E00.01"}]
}
REGLAS:
  - largo (60.9): si desc y catalog difieren (> 0.01 ft) se carga el que coincide con drawn (tol 0.05 ft)
    + RFI con delta = 2 x (otro - cargado) x qty. Si drawn no coincide con ninguno o no existe ->
    ValueError, salvo length_override con source y texto de RFI. 53.3 NO aplica (la medida sí está impresa).
  - módulo (60.10): max(ancho, largo) <= módulo -> 0 LF (FITS_MODULE). Módulo: wall = stud bay;
    ceiling = ceiling_furring_oc_in.
  - wall que NO cabe en el stud bay -> 0 LF aquí: air_device / duct / fire damper -> NOT_FRAMED (decisión
    usuario #12); el resto -> TO_HEADER_SILL (58.4, va a headers.py).
  - LF = 2 x (largo + ancho) x qty   (round: 4 x diámetro x qty, hueco cuadrado)
  - v62 (arbitraje #12): con items de ceiling, "sweep" es obligatorio: {"sheets": [...] con al menos una
    hoja M (air devices / slot diffusers en GWB) y una E (fixtures)}; si no hay ningún air_device de ceiling
    se exige sweep.no_air_devices_why. #12A no barrió M01.01 y omitió las SD slot diffusers (TBDI-10) de los
    GWB ceilings de 100/101/113/114 (ref v4 <n> LF) -> 818.75 contra 927-952.
  - v65 (arbitraje #14): con fixtures (category light) de ceiling, "tag_counts" es obligatorio = salida de
    contar_tags.py sobre la hoja E ({tag: {"count": n, "sheet": "E02.01"}}). Por tag: Σ qty <= count; si es
    menor, cada item del tag declara excluded_qty_why (p. ej. "4 en ACT, no GWB"); mayor = error. #14B cargó
    UU3 x 5 cuando E02.01 dibuja 9 (+25.66 LF).
  - v66 (arbitraje #15A): width_source obligatorio por item (#15A tomó el ancho del código de catálogo sin
    citarlo): N/HOJA + de dónde sale (cota, schedule, catálogo).
SALIDA: totales_lf {"framed openings MEP"} + renglones con source + rfis (delta LF) + to_header_sill.

Uso:  python3 framed_openings.py entrada.json salida.json
"""
import json
import re
import sys

EPS = 1e-6
TOL_CONFLICTO = 0.01
TOL_DIBUJO = 0.05
STUD_BAY_DEFAULT_IN = 14.375
FAM = "framed openings MEP"
RX_AIRE = re.compile(r"\b(duct|fire ?damper|FD|damper|louver|grille|register|diffuser)\b", re.I)
RX_SRC = re.compile(r"^([A-Za-z0-9.]{1,6}/)*[A-Z]{1,3}-?\d[\w.\-]*$")


def _src(x, ctx):
    if not isinstance(x, str) or not x.strip():
        raise ValueError(f"{ctx}: falta 'source' (N/HOJA)")
    # v71 (arbitraje #19, P6): la PRIMERA parte cita N/HOJA (u HOJA); lo que sigue tras "," / ";" puede ser
    # texto ("spacing not printed - criterion"): antes cada parte tenía que empezar con una hoja.
    p = re.split(r"\s*[,;·]\s*", x.strip())[0]
    tok = p.split()[0].rstrip(":") if p.split() else ""
    if not RX_SRC.match(tok):
        raise ValueError(f"{ctx}: source '{p}' no tiene forma N/HOJA (ej. E00.01, 2/A09.31)")
    return x.strip()


def _pos(v, ctx):
    try:
        f = float(v)
    except (TypeError, ValueError):
        raise ValueError(f"{ctx}: no es número: {v!r}")
    if f <= EPS:
        raise ValueError(f"{ctx}: debe ser > 0 (vino {v})")
    return f


def _largo(it, tag):
    """Devuelve (largo_ft, op, rfi_delta_por_unidad_ft, rfi_txt)."""
    lt = it.get("length_ft")
    if not isinstance(lt, dict) or not lt:
        raise ValueError(f"{tag}: falta length_ft {{desc, catalog, drawn}}")
    c = {k: _pos(lt[k], f"{tag}.length_ft.{k}") for k in ("desc", "catalog", "drawn") if lt.get(k) is not None}
    if not c:
        raise ValueError(f"{tag}: length_ft sin desc/catalog/drawn")
    ov = it.get("length_override")
    impresos = [c[k] for k in ("desc", "catalog") if k in c]
    conflicto = len(impresos) == 2 and abs(impresos[0] - impresos[1]) > TOL_CONFLICTO
    if not conflicto:
        if ov:
            raise ValueError(f"{tag}: length_override sin conflicto que resolver")
        k = "desc" if "desc" in c else "catalog" if "catalog" in c else "drawn"
        if "drawn" in c and k != "drawn" and abs(c["drawn"] - c[k]) > TOL_DIBUJO:
            raise ValueError(f"{tag}: {k} {c[k]} vs drawn {c['drawn']} — no coinciden: RFI, declarar length_override")
        return c[k], f"largo {k} {c[k]}", 0.0, None
    d, k_ = c["desc"], c["catalog"]
    dr = c.get("drawn")
    if dr is not None and abs(dr - d) <= TOL_DIBUJO:
        car, otro, kk = d, k_, "desc = drawn"
    elif dr is not None and abs(dr - k_) <= TOL_DIBUJO:
        car, otro, kk = k_, d, "catalog = drawn"
    elif ov:
        car = _pos(ov.get("value"), f"{tag}.length_override")
        _src(ov.get("source"), f"{tag}.length_override")
        if not ov.get("rfi"):
            raise ValueError(f"{tag}: length_override sin texto de RFI")
        otro = max((d, k_), key=lambda x: abs(x - car))
        kk = f"override [{ov['source']}]"
    else:
        raise ValueError(f"{tag}: descripción {d} vs catálogo {k_} y el dibujo no resuelve "
                         f"(drawn {dr}) — RFI: declarar length_override con source (60.9)")
    rfi = (f"RFI {tag}: schedule description {d} ft vs catalog {k_} ft; carried {car} ft ({kk}); "
           f"alternate {otro} ft")
    return car, f"largo {car} ({kk}; desc {d} / catalog {k_})", otro - car, rfi


def calcular(data):
    mods = data.get("modules") or {}
    bay = _pos(mods.get("wall_stud_bay_in", STUD_BAY_DEFAULT_IN), "modules.wall_stud_bay_in")
    cmod = None
    if mods.get("ceiling_furring_oc_in") is not None:
        o = mods["ceiling_furring_oc_in"]
        if not isinstance(o, dict):
            raise ValueError("modules.ceiling_furring_oc_in debe ser {value, source}")
        cmod = _pos(o.get("value"), "modules.ceiling_furring_oc_in")
        _src(o.get("source"), "modules.ceiling_furring_oc_in")
    items = data.get("items")
    if not isinstance(items, list) or not items:
        raise ValueError("'items' vacío o ausente")
    if any(it.get("location") == "ceiling" for it in items):
        sw = data.get("sweep")
        if not isinstance(sw, dict):
            raise ValueError("sweep ausente: barrer M-plan (air devices) y E-plan (fixtures) de los GWB ceilings (v62)")
        hojas = [str(h) for h in sw.get("sheets") or []]
        if not any(re.match(r"^M\d", h) for h in hojas) or not any(re.match(r"^E\d", h) for h in hojas):
            raise ValueError(f"sweep.sheets {hojas}: falta hoja M (air devices) o E (fixtures) (v62)")
        if not any(it.get("location") == "ceiling" and it.get("category") == "air_device" for it in items) \
                and not str(sw.get("no_air_devices_why") or "").strip():
            raise ValueError("ningún air_device de ceiling: declarar los del M-plan (SD / slot diffusers) o "
                             "sweep.no_air_devices_why (v62, #12A)")
    luces = [it for it in items if it.get("category") == "light" and it.get("location") == "ceiling"]
    if luces:
        tc = data.get("tag_counts")
        if not isinstance(tc, dict) or not tc:
            raise ValueError("tag_counts ausente: contar las fixtures por tag en la hoja E con contar_tags.py "
                             "(v65, #14B UU3 5 vs 9 dibujados)")
        por_tag = {}
        for it in luces:
            por_tag.setdefault(it["tag"], []).append(it)
        for tg, its in por_tag.items():
            c = tc.get(tg)
            if not isinstance(c, dict) or "count" not in c or not str(c.get("sheet") or "").strip():
                raise ValueError(f"{tg}: sin tag_counts[{tg}] {{count, sheet}} (contar_tags.py)")
            q = sum(int(i.get("qty", 0)) for i in its)
            if q > int(c["count"]):
                raise ValueError(f"{tg}: qty {q} > {c['count']} dibujados en {c['sheet']} (contar_tags.py)")
            if q < int(c["count"]) and not all(str(i.get("excluded_qty_why") or "").strip() for i in its):
                raise ValueError(f"{tg}: qty {q} < {c['count']} dibujados en {c['sheet']} sin excluded_qty_why "
                                 f"(v65: #14B UU3 5 de 9)")
    tot, filas, rfis, a_hs, vistos = 0.0, [], [], [], set()
    for it in items:
        tag = it.get("tag")
        if not tag:
            raise ValueError("item sin tag")
        key = (tag, it.get("location"), it.get("width_in"))
        if key in vistos:
            raise ValueError(f"{tag}: item repetido (sumar en qty)")
        vistos.add(key)
        src = _src(it.get("source"), tag)
        loc, shape = it.get("location"), it.get("shape", "rect")
        if loc not in ("ceiling", "wall"):
            raise ValueError(f"{tag}: location debe ser ceiling | wall")
        if shape not in ("rect", "round"):
            raise ValueError(f"{tag}: shape debe ser rect | round")
        qty = it.get("qty")
        if not isinstance(qty, int) or isinstance(qty, bool) or qty < 1:
            raise ValueError(f"{tag}: qty debe ser entero >= 1")
        W = _pos(it.get("width_in"), f"{tag}.width_in") / 12.0
        wsrc = _src(it.get("width_source"), f"{tag}.width_source (v66: de dónde sale el ancho — cota, schedule o "
                                            f"código de catálogo, ej. 'E00.01 <catálogo>')")
        if shape == "round":
            if it.get("length_ft") is not None:
                raise ValueError(f"{tag}: round no lleva length_ft (width_in = diámetro)")
            L, lop, dl, rfi = W, f"round d {round(W * 12, 3)}\" (hueco cuadrado)", 0.0, None
        else:
            L, lop, dl, rfi = _largo(it, tag)
        if loc == "ceiling":
            if cmod is None:
                raise ValueError(f"{tag}: item de ceiling sin modules.ceiling_furring_oc_in (60.10)")
            mod = cmod
        else:
            mod = bay
        base = {"tag": tag, "category": it.get("category"), "location": loc, "qty": qty, "source": src,
                "width_source": wsrc}
        mayor_in = max(L, W) * 12.0
        if mayor_in <= mod + EPS:
            filas.append(dict(base, estado="FITS_MODULE", lf=0.0,
                              operacion=f"{lop}; max {round(mayor_in, 3)}\" <= módulo {mod}\" (60.10) -> 0"))
            continue
        if loc == "wall" and (it.get("category") == "air_device" or RX_AIRE.search(str(tag))):
            filas.append(dict(base, estado="NOT_FRAMED", lf=0.0,
                              operacion=f"{lop}; duct / fire damper / air device de wall: no se enmarca, sin header "
                                        f"ni sill (decisión usuario #12)"))
            continue
        if loc == "wall":
            a_hs.append({"tag": tag, "qty": qty, "source": src, "ro_w_ft": round(max(L, W), 3)})
            filas.append(dict(base, estado="TO_HEADER_SILL", lf=0.0,
                              operacion=f"{lop}; {round(mayor_in, 3)}\" > stud bay {bay}\" -> header/sill (58.4)"))
            continue
        lf = (4 * W if shape == "round" else 2 * (L + W)) * qty
        tot += lf
        filas.append(dict(base, estado="FRAMED", lf=round(lf, 2),
                          operacion=f"{lop}; 2 x ({round(L, 3)} + {round(W, 3)}) x {qty} = {round(lf, 2)}"
                          if shape == "rect" else f"{lop}; 4 x {round(W, 3)} x {qty} = {round(lf, 2)}"))
        if rfi:
            rfis.append({"tag": tag, "source": src, "texto": rfi, "delta_lf": round(2 * dl * qty, 2)})
    return {"totales_lf": {FAM: round(tot, 2)}, "renglones": filas, "rfis": rfis, "to_header_sill": a_hs}


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    try:
        out = calcular(json.load(open(argv[1])))
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as e:
        print(f"ERROR framed_openings.py: {e}", file=sys.stderr)
        return 1
    open(argv[2], "w").write(json.dumps(out, indent=1))
    print(json.dumps(out["totales_lf"]))
    for r in out["rfis"]:
        print("RFI", r["texto"], "delta", r["delta_lf"], "LF")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
