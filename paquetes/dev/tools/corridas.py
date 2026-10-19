#!/usr/bin/env python3
"""corridas.py v64 — tracks, bracing y purlin DETERMINISTAS sobre la lista completa de corridas.

v64 (decisiones del usuario/estimador, 2026-10-16):
  #10 bottom track NO se descuenta en doors: corre completo. bottom_track_deduct_doors true -> ValueError.
  #8  column_wrap (5/A09.25) lleva bottom + top track (perímetro de faces) y studs a su altura: bottom_track /
      top_track false en column_wrap -> ValueError.
  #9  ceiling_transition (7/A09.33): track arriba (deck) y abajo (ceiling) -> track_lines 2 obligatorio.
  #13 canopy_soffit: track en LOS DOS extremos de los joists (fascia y wall) -> track_lines 2 obligatorio.
      v66: la línea del wall se mide aparte (wall_line_ft {value, source}); track = fascia + wall, nunca L x 2.

Historia:
  v60 (arbitraje #10): 60.6 corridas de un detalle de sección, 60.7 bracing sobre todas las corridas,
      60.8 familia del track POR ORIENTACIÓN.
  v61 (arbitraje #11, 16-oct-2026): la familia POR ORIENTACIÓN fue la causa principal de la bajada de #11A
      y #11B. El canopy fascia box (7/A09.26), los lados del CSR soffit (10/A09.33) y las transiciones de
      ceiling (7/A09.33) TIENEN studs verticales entre dos tracks, pero la referencia (arbitraje #8, regla
      58.2 c) los lleva en "track de ceilings / soffits": bottom/top track es SOLO de walls. #11A movió
      fascia + CSR + transiciones a bottom/top (+<n> LF, ceiling -<n>); #11B movió los drops de room <ref>.
      Ahora la familia sale del ELEMENTO (lista cerrada); la orientación solo decide el bracing.
      Además: bottom y top se reportan POR SEPARADO (cada uno = L x rows), purlin = 0.75 x L de top track
      a deck paralelo al flute (10/A09.33), y el bracing NO cruza el vacío de una abertura.
  v62 (arbitraje #12, 16-oct-2026): (a) purlin = UNA pieza por corrida aunque el wall tenga 2 rows de stud
      (59.1; ref v4 "double-row G counted once: one purlin across >= 2 flutes spans both 1-5/8\" tracks").
      #12A y #12B multiplicaban por rows (+<n> LF en los walls de doble row). (b) bottom track puede descontar el R.O. de las
      doors SOLO si el take-off lo declara con fuente (bottom_track_deduct_doors {value, source}); sin eso
      L x rows y la tool informa el delta como RFI (#12A RFI, -<n> LF).

ENTRADA (JSON):
{
  "bracing": {"spacing_in": 48, "source": "F/1/S5.20"},        # 53.4
  "purlin": {"factor": 0.75, "source": "10/A09.33"},           # opcional (default 0.75 con esa fuente)
  "section_details": [{"source": "4/A02.02", "runs": 3}],      # 60.6
  "ceiling_details": ["7/A09.33", "10/A09.33", "7/A09.26"],    # v61: detalles de ceiling/soffit/canopy; una
                                                               # corrida con esa source NO puede ser WALL
  "runs": [{
      "id": "R1", "element": "wall",                           # ver ELEMENTOS
      "orientation": "vertical",                               # vertical | horizontal (solo bracing)
      "length_ft": <n>, "height_ft": 9.5, "rows": 1,
      "track_lines": 2,                    # opcional: si difiere del default del elemento exige track_lines_source
      "bottom_track": true, "top_track": true,   # solo familia WALL; false exige track_source
      "openings": [{"ro_w_ft": 8.0, "sill_ft": 6.5, "head_ft": 8.5}],   # opcional: el bracing no las cruza
      "purlin": true,                      # top track a deck PARALELO al flute (10/A09.33)
      "bracing_rows": 2, "bracing_rows_source": "3/S5.20",
      "source": "4/A02.02"}]
}
ELEMENTOS -> FAMILIA (lista cerrada, 58.2 c + 60.8 v61):
  WALL  -> "bottom track" + "top / deflection track" (L x rows CADA UNO):
           wall, parapet, roof_step, pier, column_wrap, chase, vestibule_head, grille_head, grille_box,
           door_bulkhead, storefront_cripples (bottom track sobre el steel header + top bajo la viga)
  CEIL  -> "track de ceilings / soffits" (L x track_lines):
           ceiling_perimeter (1), soffit_drop (2), ceiling_transition (2), ceiling_bulkhead (2),
           soffit_side (2), soffit_bottom (2), fascia_box (2), canopy_soffit (2: un track en cada extremo de
           joist, cada uno en SU línea -> declarar 1 por línea si las líneas miden distinto), joist (2)
BRACING: solo corridas verticales. rows = bracing_rows declarado o ROUNDUP(H x 12 / spacing) - 1 (min 0).
  LF = rows x L x rows_stud (53.4 literal, convención de la referencia). Fila k a altura k x spacing: una
  abertura con sill < altura < head no tiene studs; ese R.O. se suma en "rfi_bracing_huecos_lf" (RFI con
  delta; la familia NO cambia hasta que se resuelva). bracing.through_openings=false -> se descuenta.
PURLIN: purlin true -> factor x L (UNA pieza, 59.1; rows NO multiplica) (familia "purlin (track to deck)").
DOORS: openings[].kind == "door" -> delta RFI de bottom track; se descuenta solo con
  "bottom_track_deduct_doors": {"value": true, "source": "N/HOJA"}.
VALIDACIONES (ValueError): id repetido, source sin forma N/HOJA, elemento desconocido, height en vertical,
  track_lines distinto del default sin fuente, bottom/top track en elemento CEIL, purlin en horizontal,
  corridas de un section_detail distintas de las declaradas, R.O. más ancho que la corrida.
SALIDA: totales_lf por familia (nombres del calificador) + renglón por corrida con operación.

Uso:  python3 corridas.py entrada.json salida.json
"""
import json
import math
import re
import sys

EPS = 1e-6
WALL = {"wall", "parapet", "roof_step", "pier", "column_wrap", "chase", "vestibule_head", "grille_head",
        "grille_box", "door_bulkhead", "storefront_cripples"}
CEIL = {"ceiling_perimeter": 1, "soffit_drop": 2, "ceiling_transition": 2, "ceiling_bulkhead": 2,
        "soffit_side": 2, "soffit_bottom": 2, "fascia_box": 2, "canopy_soffit": 2, "joist": 2}
FIJOS_2 = {"ceiling_transition": "decisión usuario #9: arriba (deck) y abajo (ceiling), 7/A09.33",
           "canopy_soffit": "decisión usuario #13: fascia y wall"}
F_B, F_T = "bottom track (todos)", "top / deflection track (todos)"
F_CT, F_BR, F_PU = "track de ceilings / soffits", "bracing C.R. channel", "purlin (track to deck)"
RX_SRC = re.compile(r"^([A-Za-z0-9.]{1,6}/)*[A-Z]{1,3}-?\d[\w.\-]*$")


def _partes(x):
    """v68 (#16A '"C/A09.21 (6\", 16 ga)"' rechazado): separa por , ; · solo FUERA de paréntesis / corchetes."""
    out, cur, nivel = [], "", 0
    for ch in x:
        if ch in "([":
            nivel += 1
        elif ch in ")]":
            nivel = max(0, nivel - 1)
        if ch in ",;·" and nivel == 0:
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    out.append(cur.strip())
    return [p for p in out if p] or [""]


def _src(x, ctx):
    if not isinstance(x, str) or not x.strip():
        raise ValueError(f"{ctx}: falta 'source' (N/HOJA)")
    for p in _partes(x.strip()):
        tok = p.split()[0] if p.split() else ""
        if not RX_SRC.match(tok):
            raise ValueError(f"{ctx}: source '{p}' no tiene forma N/HOJA (ej. 6/A12.01, F/1/S5.20, A08.01)")
    return x.strip()


def _pos(v, ctx, cero=False):
    try:
        f = float(v)
    except (TypeError, ValueError):
        raise ValueError(f"{ctx}: no es número: {v!r}")
    if f < -EPS or (not cero and f <= EPS):
        raise ValueError(f"{ctx}: debe ser > 0 (vino {v})")
    return f


def _int(v, ctx, minimo):
    if not isinstance(v, int) or isinstance(v, bool) or v < minimo:
        raise ValueError(f"{ctx}: debe ser entero >= {minimo} (vino {v!r})")
    return v


def _bracing(r, rid, L, H, rows, sp, bsrc):
    if "bracing_rows" in r:
        nb = _int(r["bracing_rows"], f"{rid}.bracing_rows", 0)
        txt = f"{nb} rows declaradas ({_src(r.get('bracing_rows_source'), rid + '.bracing_rows')})"
        alturas = [(k + 1) * H / (nb + 1) for k in range(nb)]
    elif sp is not None:
        nb = max(0, int(math.ceil(H * 12.0 / sp - EPS)) - 1)
        txt = f"ROUNDUP({H} x 12 / {sp}) - 1 = {nb} rows ({bsrc})"
        alturas = [(k + 1) * sp / 12.0 for k in range(nb)]
    else:
        raise ValueError(f"{rid}: corrida vertical sin bracing.spacing_in global ni bracing_rows con fuente (53.4)")
    ops = r.get("openings") or []
    lf, det, hueco_tot = 0.0, [], 0.0
    for h in alturas:
        hueco = 0.0
        for o in ops:
            ro = _pos(o.get("ro_w_ft"), f"{rid}.openings.ro_w_ft")
            if ro > L + EPS:
                raise ValueError(f"{rid}: R.O. {ro} más ancho que la corrida {L}")
            s_ = _pos(o.get("sill_ft", 0), f"{rid}.openings.sill_ft", cero=True)
            hd = _pos(o.get("head_ft"), f"{rid}.openings.head_ft")
            if s_ + EPS < h < hd - EPS:
                hueco += ro
        lf += L * rows
        hueco_tot += hueco * rows
        if hueco:
            det.append(f"fila {round(h, 2)} ft cruza {round(hueco, 3)} de vano")
    return nb, lf, hueco_tot, txt + (f" [{'; '.join(det)}]" if det else "")


def calcular(data):
    runs = data.get("runs")
    if not isinstance(runs, list) or not runs:
        raise ValueError("'runs' vacío o ausente")
    br = data.get("bracing")
    sp = bsrc = None
    descontar = bool(br) and br.get("through_openings") is False
    if br:
        sp = _pos(br.get("spacing_in"), "bracing.spacing_in")
        bsrc = _src(br.get("source"), "bracing")
    pu = data.get("purlin") or {"factor": 0.75, "source": "10/A09.33"}
    pf = _pos(pu.get("factor"), "purlin.factor")
    psrc = _src(pu.get("source"), "purlin")
    ceil_det = {_src(x, "ceiling_details") for x in (data.get("ceiling_details") or [])}
    ded = data.get("bottom_track_deduct_doors")
    deducir = False
    if ded is not None:
        if not isinstance(ded, dict) or "value" not in ded:
            raise ValueError("bottom_track_deduct_doors debe ser {value, source}")
        deducir = bool(ded["value"])
        if deducir:
            raise ValueError("bottom_track_deduct_doors true: el bottom track NO se descuenta en doors, corre "
                             "completo (decisión usuario #10, 2026-10-16)")
    doors_tot = 0.0
    ids, por_src = set(), {}
    tot = {F_B: 0.0, F_T: 0.0, F_CT: 0.0, F_BR: 0.0, F_PU: 0.0}
    huecos = 0.0
    filas = []
    for r in runs:
        rid = r.get("id")
        if not rid or rid in ids:
            raise ValueError(f"corrida sin id o id repetido: {rid!r}")
        ids.add(rid)
        src = _src(r.get("source"), rid)
        por_src[src] = por_src.get(src, 0) + 1
        el, ori = r.get("element"), r.get("orientation")
        if ori not in ("vertical", "horizontal"):
            raise ValueError(f"{rid}: orientation debe ser vertical u horizontal")
        if el not in WALL and el not in CEIL:
            raise ValueError(f"{rid}: element '{el}' desconocido (WALL: {sorted(WALL)}; CEIL: {sorted(CEIL)})")
        if el in WALL and ori != "vertical":
            raise ValueError(f"{rid}: '{el}' es de la familia WALL (studs verticales)")
        if el in WALL and src in ceil_det:
            raise ValueError(f"{rid}: source {src} es un detalle de ceiling/soffit -> elemento CEIL "
                             f"({sorted(CEIL)}), no '{el}' (58.2 c)")
        L = _pos(r.get("length_ft"), f"{rid}.length_ft")
        rows = _int(r.get("rows", 1), f"{rid}.rows", 1)
        fila = {"id": rid, "element": el, "orientation": ori, "source": src, "bottom_lf": 0.0, "top_lf": 0.0,
                "ceiling_track_lf": 0.0, "bracing_lf": 0.0, "purlin_lf": 0.0}
        ops = []
        if el in WALL:
            if "track_lines" in r:
                raise ValueError(f"{rid}: track_lines es solo para elementos CEIL; en WALL usar bottom_track/top_track")
            b = bool(r.get("bottom_track", True))
            t = bool(r.get("top_track", True))
            if el == "column_wrap" and not (b and t):
                raise ValueError(f"{rid}: column_wrap lleva bottom + top track (decisión usuario #8, 5/A09.25)")
            if not (b and t):
                _src(r.get("track_source"), f"{rid}: sin bottom o top track")
            dw = sum(_pos(o.get("ro_w_ft"), f"{rid}.door") for o in r.get("openings") or []
                     if o.get("kind") == "door")
            doors_tot += dw * rows if b else 0.0
            fila["bottom_lf"] = ((L - dw) if deducir else L) * rows if b else 0.0
            fila["top_lf"] = L * rows if t else 0.0
            ops.append(f"bottom {('(' + str(L) + ' - doors ' + str(round(dw, 3)) + ')') if deducir and dw else L} x "
                       f"{rows} = {round(fila['bottom_lf'], 2)}; top {L} x {rows} = {round(fila['top_lf'], 2)}")
        else:
            if "bottom_track" in r or "top_track" in r:
                raise ValueError(f"{rid}: '{el}' lleva track de ceilings / soffits (58.2 c), no bottom/top")
            dflt = CEIL[el]
            tl = _int(r.get("track_lines", dflt), f"{rid}.track_lines", 1)
            if el in FIJOS_2 and tl != 2:
                raise ValueError(f"{rid}: {el} lleva track en los DOS extremos ({FIJOS_2[el]}) — track_lines 2")
            if tl != dflt:
                _src(r.get("track_lines_source"), f"{rid}: track_lines {tl} distinto del default {dflt} de '{el}'")
            if el == "canopy_soffit":                 # v66: fascia y wall se miden por separado (#15B L x 2)
                wl = r.get("wall_line_ft")
                if not isinstance(wl, dict) or not str(wl.get("source") or "").strip() or float(wl.get("value", 0)) <= 0:
                    raise ValueError(f"{rid}: canopy_soffit sin wall_line_ft {{value, source}} — el track va en la "
                                     f"línea de fascia (length_ft) Y en la línea del wall, medidas por separado: en "
                                     f"esquinas no son iguales (v66, decisión usuario #13)")
                fila["ceiling_track_lf"] = L + float(wl["value"])
                ops.append(f"canopy soffit track fascia {L} + wall {wl['value']} = {round(L + float(wl['value']), 2)} "
                           f"({wl['source']})")
            else:
                fila["ceiling_track_lf"] = L * tl
                ops.append(f"ceiling/soffit track {L} x {tl} lines = {round(L * tl, 2)}")
        if ori == "vertical":
            H = _pos(r.get("height_ft"), f"{rid}.height_ft")
            nb, bl, hu, bop = _bracing(r, rid, L, H, rows, sp, bsrc)
            huecos += hu
            if descontar:
                bl -= hu
            fila.update(height_ft=H, rows=rows, bracing_rows=nb, bracing_lf=round(bl, 2))
            ops.append(f"bracing {bop} -> {round(bl, 2)}")
        else:
            if "bracing_rows" in r or r.get("openings"):
                raise ValueError(f"{rid}: bracing/openings en framing horizontal (53.4 es de studs verticales)")
            bl = 0.0
        if r.get("purlin"):
            if ori != "vertical":
                raise ValueError(f"{rid}: purlin solo en top track de corrida vertical a deck")
            fila["purlin_lf"] = pf * L
            ops.append(f"purlin {pf} x {L} (1 pieza, {rows} row(s), 59.1) = {round(fila['purlin_lf'], 2)} ({psrc})")
        tot[F_B] += fila["bottom_lf"]
        tot[F_T] += fila["top_lf"]
        tot[F_CT] += fila["ceiling_track_lf"]
        tot[F_BR] += bl
        tot[F_PU] += fila["purlin_lf"]
        for k in ("bottom_lf", "top_lf", "ceiling_track_lf", "purlin_lf"):
            fila[k] = round(fila[k], 2)
        fila["operacion"] = "; ".join(ops)
        filas.append(fila)
    for sd in data.get("section_details") or []:
        s = _src(sd.get("source"), "section_details")
        n = _int(sd.get("runs"), f"section_details {s}.runs", 1)
        if por_src.get(s, 0) != n:
            raise ValueError(f"{s}: el detalle dibuja {n} corridas independientes y hay {por_src.get(s, 0)} con esa "
                             f"source (60.6)")
    rfi = (f"RFI bracing: {round(huecos, 2)} LF de C.R. channel cruzan vanos sin studs (53.4 literal). "
           f"Delta si no se cruzan: -{round(huecos, 2)} LF") if huecos > EPS and not descontar else None
    rfi_doors = None
    if doors_tot > EPS:
        rfi_doors = (f"RFI bottom track: {round(doors_tot, 2)} LF de R.O. de doors "
                     + ("DESCONTADOS (bottom_track_deduct_doors)" if deducir else
                        f"NO descontados. Delta si se descuentan: -{round(doors_tot, 2)} LF"))
    return {"totales_lf": {k: round(v, 2) for k, v in tot.items()}, "renglones": filas,
            "rfi_bracing_huecos_lf": round(huecos, 2), "rfi": rfi,
            "doors_ro_lf": round(doors_tot, 2), "rfi_doors": rfi_doors}


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    try:
        out = calcular(json.load(open(argv[1])))
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as e:
        print(f"ERROR corridas.py: {e}", file=sys.stderr)
        return 1
    open(argv[2], "w").write(json.dumps(out, indent=1))
    print(json.dumps(out["totales_lf"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
