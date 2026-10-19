#!/usr/bin/env python3
"""headers.py v65b — header / sill track DETERMINISTA, una vez por abertura, LF POR PIEZAS.

v64 (decisiones del usuario/estimador, 2026-10-16 — mandan sobre ref v4, rangos y arbitrajes):
  #1  largo de cada pieza = R.O. + 1'-4" (8" de bearing a cada lado).
  #2  LF de MATERIAL = (R.O. + 1'-4") x PIEZAS x qty. Las piezas salen del header schedule (7/S5.20: SINGLE
      TRACK = 1, DOUBLE TRACK = 2, 2-362CSJ20 = 2 ...) o del detalle del box (box headers / box beams: TODAS
      las piezas que forman el box, con pieces_source). Antes (v60-v63) se cargaba LF de LÍNEA (x 1): eso
      subcontaba el box.
  #12 ductos y fire dampers en walls NO se enmarcan: kind duct | fire_damper -> NOT_FRAMED, 0 header y 0 sill
      (sin importar el tamaño).
  #16 storefront con lintel estructural (HSS / steel en el plan S*): structure "HSS" | "steel" -> 0 metal stud
      header (steel by others). Storefront exterior exige structure_source + structure.
  sill: sill_rule {double_over_ft, source} (2/S5.20 "INVERT DETAIL FOR SILL CONDITION" + "ADD FULL LENGTH ADDL
      HEAD TRACK @ OPNG >4'-0"") -> sill track 2 piezas si R.O. > double_over_ft; sin regla 1 pieza.

ENTRADA (JSON):
{
  "stud_bay_in": 14.375, "stud_bay_source": "S1.11",          # opcional (60.10)
  "header_schedule": {"source": "7/S5.20",                    # piezas OBLIGATORIAS por fila
      "rows": [{"max_span_ft": 3.333, "type": "SINGLE TRACK 18 GA", "pieces": 1, "piece": "track"},
               {"max_span_ft": 6.0,   "type": "DOUBLE TRACK 18 GA", "pieces": 2, "piece": "track"},
               {"max_span_ft": 8.0,   "type": "2-362CSJ20",         "pieces": 2, "piece": "362CSJ20"}]},
  "sill_rule": {"double_over_ft": 4.0, "source": "2/S5.20"},  # opcional
  "openings": [{
      "ref": "door <ref>", "wall": "W1", "kind": "door",    # door|window|atm|storefront|opening|grille|duct|fire_damper
      "location": "interior", "ro_w_ft": 3.333, "qty": 1, "with_sill": false, "source": "A00.30",
      "header_type": "BOX 2 C", "header_type_source": "9/A12.01",     # opcional; manda sobre el schedule
      "pieces": 2, "pieces_source": "9/A12.01", "piece": "C box",     # obligatorio con header_type
      "beams": 2, "beams_source": "4/A08.21",                         # solo grille
      "structure": "HSS", "structure_source": "S2.20"}]               # storefront exterior
}
v65b (DECISIONES DEL USUARIO #18-#22, 17-oct-2026) — REGLAS fijas, ya no parámetros ("header_params" se rechaza):
  #18 sill: DOUBLE sill track en R.O. > 4'-0" SIEMPRE (2/S5.20 "ADD FULL LENGTH ADDL HEAD TRACK @ OPNG >4'-0""
      + "INVERT DETAIL FOR SILL CONDITION"). Sin sill_rule en la entrada se aplica 4'-0" / 2/S5.20. sill_pieces
      menor que la regla = error.
  #19 "METAL STUD BOX BEAM OR STEEL FRAMING AS REQUIRED" (window head detail): METAL STUD BOX BEAM. Abertura con
      or_steel: true u "OR STEEL" en header_type -> structure HSS / steel = error (v66: sin nombres de un proyecto).
  #20 TODO box beam / box header ("BOX" en header_type) = 4 PIEZAS (2 C + 2 track). pieces != 4 = error.
      Casos típicos: storefront / glazing box, office front, coiling grille, vestibule head, door exterior con
      box, ATM recess.
  R71.10 (v71) header_type "ASSUMED" / "NOT PRINTED" = error: header no llamado = 0 + RFI.
  R71.11 (v71) CONT. BOX BEAM declara run_ends "jamb_to_jamb" | "wall_to_wall" (+ run_ends_source o rfi).
  #21 header_type que no es box no puede bajar las piezas del header schedule (una door cuyo R.O. cae en
      DOUBLE TRACK del schedule = 2 piezas; una nota general "> 4'-0"" no lo baja a 1).
  #22 "CONT." BOX BEAM (office front 8,9/A12.01) = UN run continuo a lo largo de todo el frente: una sola abertura
      con continuous_run: true, qty = 1; wall = línea del frente, ro_w_ft = largo del run medido (source + RFI si
      no hay cota). Por abertura (qty > 1, o varias con el mismo detalle en la misma línea) = error. Dos frentes
      (dos líneas de office front) = dos runs (EJES).

SALIDA: totales_lf {"header", "sill track"}, por_pieza {piece: LF}, renglones (operación en cada uno), avisos.

Uso:  python3 headers.py entrada.json salida.json
"""
import json
import re
import sys

EPS = 1e-6
EXTRA_FT = 16.0 / 12.0          # 1'-4"
SPAN_TOL = 1.0 / 192.0          # 1/16": el redondeo de la cota no cambia la fila del schedule
STUD_BAY_DEFAULT_IN = 14.375    # 60.10
KINDS = {"door", "window", "storefront", "opening", "duct", "fire_damper", "grille", "atm"}  # v68: atm = window
NOT_FRAMED = {"duct", "fire_damper"}     # decisión usuario #12
STRUCT = {"HSS", "steel", "none"}        # decisión usuario #16
RX_RECESSED = re.compile(r"\b(recess(ed)?|hand ?dryer|TA-\d+|FEC(-\d+)?|fire extinguisher|cabinet|niche)\b", re.I)
PROHIBIDOS = ("members", "multiplier", "plies", "x_members")
RX_SRC = re.compile(r"^([A-Za-z0-9.]{1,6}/)*[A-Z]{1,3}-?\d[\w.\-]*$")


def _partes(x):
    """v70 (#18A): separa por , ; · solo FUERA de paréntesis / corchetes (el mismo splitter que corridas.py)."""
    try:
        import corridas
        return corridas._partes(x)
    except (ImportError, AttributeError):
        out, cur, nivel = [], "", 0
        for ch in x:
            nivel += (ch in "([") - (ch in ")]" and nivel > 0)
            if ch in ",;·" and nivel == 0:
                out.append(cur.strip())
                cur = ""
            else:
                cur += ch
        out.append(cur.strip())
        return [p for p in out if p] or [""]


def _src(x, ctx):
    """Cada parte (separada fuera de paréntesis) empieza con N/HOJA u HOJA; v70 acepta "N/HOJA:" (con dos puntos)."""
    if not isinstance(x, str) or not x.strip():
        raise ValueError(f"{ctx}: falta 'source' (N/HOJA)")
    for p in _partes(x.strip()):
        tok = p.split()[0].rstrip(":") if p.split() else ""
        if not RX_SRC.match(tok):
            raise ValueError(f"{ctx}: source '{p}' no tiene forma N/HOJA (ej. 6/A12.01, F/1/S5.20, A08.01)")
    return x.strip()


def _pos(v, ctx):
    try:
        f = float(v)
    except (TypeError, ValueError):
        raise ValueError(f"{ctx}: no es número: {v!r}")
    if f <= EPS:
        raise ValueError(f"{ctx}: debe ser > 0 (vino {v})")
    return f


def _int1(v, ctx):
    if not isinstance(v, int) or isinstance(v, bool) or v < 1:
        raise ValueError(f"{ctx}: debe ser entero >= 1 (vino {v!r})")
    return v


def _ftin(ft):
    tot = round(ft * 12 * 8) / 8.0
    f, i = int(tot // 12), tot - 12 * int(tot // 12)
    return f"{f}'-{i:g}\""


SILL_RULE_DEFAULT = {"double_over_ft": 4.0, "source": "2/S5.20"}     # decisión usuario #18
BOX_PIECES = 4                                                          # decisión usuario #20: 2 C + 2 track



def _sill_pz(o, regla, ref):
    n = _int1(o["sill_pieces"], f"{ref}.sill_pieces")
    if n < regla:
        raise ValueError(f"{ref}: sill_pieces {n} < {regla} — DOUBLE sill track en R.O. > 4'-0\" (decisión usuario "
                         f"#18, 2/S5.20 INVERT DETAIL FOR SILL CONDITION)")
    return n


def _reglas_v65b(data):
    """Decisiones del usuario #18-#22: reglas fijas, se valida cada abertura antes de calcular."""
    if data.get("header_params") is not None:
        raise ValueError("header_params ya no existe (v65b): las decisiones del usuario #18-#22 son reglas fijas "
                         "(sill double > 4'-0\", glazing metal box, box = 4 piezas, door en DOUBLE TRACK, office front "
                         "continuo)")
    cont = {}
    for o in data.get("openings") or []:
        ref = str(o.get("ref", ""))
        ht = str(o.get("header_type") or "").upper()
        if (o.get("or_steel") or "OR STEEL" in ht) and \
                o.get("structure") in ("HSS", "steel"):
            raise ValueError(f"{ref}: 'METAL STUD BOX BEAM OR STEEL FRAMING AS REQUIRED' = METAL STUD BOX BEAM "
                             f"(decisión usuario #19, 11/A09.27) — no es steel by others")
        if re.search(r"ASSUM|NOT PRINTED|NO IMPRESO|SUPUEST|TYPICAL ASSUMED", ht):
            raise ValueError(f"{ref}: header_type '{o.get('header_type')}' no impreso (R71.10, arbitraje #19): un header "
                             f"que ningún schedule / detalle llama = 0 LF + RFI con el delta; nunca un box supuesto")
        if "CONT" in ht and o.get("run_ends") not in ("jamb_to_jamb", "wall_to_wall"):
            raise ValueError(f"{ref}: CONT. BOX BEAM sin run_ends 'jamb_to_jamb' | 'wall_to_wall' (+ run_ends_source): "
                             f"el largo del run (del primer al último jamb, o hasta los walls de los extremos) se "
                             f"declara; si el detalle no lo dibuja, RFI con el delta de las dos (R71.11)")
        if "BOX" in ht and o.get("pieces") != BOX_PIECES:
            raise ValueError(f"{ref}: box beam / box header = {BOX_PIECES} piezas (2 C + 2 track, decisión usuario "
                             f"#20); vino pieces {o.get('pieces')!r}")
        if "CONT" in ht:
            if not o.get("continuous_run") or o.get("qty", 1) != 1:
                raise ValueError(f"{ref}: CONT. BOX BEAM = UN run continuo a lo largo de todo el frente (decisión "
                                 f"usuario #22): continuous_run true, qty 1, ro_w_ft = largo del run (no por abertura)")
            if not str(o.get("wall") or "").strip():
                raise ValueError(f"{ref}: CONT. BOX BEAM sin 'wall' (línea del frente) — un run por frente; dos "
                                 f"frentes = dos runs, nunca un número para dos líneas (decisión usuario #22, EJES)")
            k = (str(o.get("header_type_source") or ""), str(o["wall"]))
            if k in cont:
                raise ValueError(f"{ref}: CONT. BOX BEAM {k[0]} en {k[1]} ya declarado en '{cont[k]}' — un solo run "
                                 f"continuo por frente (decisión usuario #22)")
            cont[k] = ref
        elif o.get("continuous_run"):
            raise ValueError(f"{ref}: continuous_run solo con header_type CONT. BOX BEAM")


def calcular(data):
    _reglas_v65b(data)
    bay = STUD_BAY_DEFAULT_IN
    if "stud_bay_in" in data:
        bay = _pos(data["stud_bay_in"], "stud_bay_in")
        if abs(bay - STUD_BAY_DEFAULT_IN) > EPS:
            _src(data.get("stud_bay_source"), "stud_bay_in distinto de 14.375")
    sch = data.get("header_schedule")
    filas_sch = []
    if sch:
        ssrc = _src(sch.get("source"), "header_schedule")
        for r in sch.get("rows") or []:
            if "pieces" not in r:
                raise ValueError(f"header_schedule fila {r.get('type')}: falta 'pieces' (decisión usuario #2: el LF "
                                 f"es por piezas: SINGLE TRACK 1, DOUBLE TRACK 2, 2-362CSJ20 2)")
            filas_sch.append((_pos(r["max_span_ft"], "header_schedule.max_span_ft"), str(r["type"]),
                              _int1(r["pieces"], f"header_schedule {r.get('type')}.pieces"),
                              str(r.get("piece") or r["type"])))
        filas_sch.sort()
    sr = data.get("sill_rule") or SILL_RULE_DEFAULT                      # decisión usuario #18
    dbl_sill = None
    if sr is not None:
        dbl_sill = _pos(sr.get("double_over_ft"), "sill_rule.double_over_ft")
        srsrc = _src(sr.get("source"), "sill_rule")
    ops = data.get("openings")
    if not isinstance(ops, list) or not ops:
        raise ValueError("'openings' vacío o ausente")
    tot = {"header": 0.0, "sill track": 0.0}
    por_pieza = {}
    filas, avisos, vistos = [], [], set()
    for o in ops:
        ref = o.get("ref")
        if not ref:
            raise ValueError("abertura sin 'ref'")
        key = (ref, o.get("wall"))
        if key in vistos:
            raise ValueError(f"{ref}: abertura repetida en el mismo wall (usar qty, una vez por abertura)")
        vistos.add(key)
        src = _src(o.get("source"), ref)
        for p in PROHIBIDOS:
            if p in o:
                raise ValueError(f"{ref}: campo '{p}' prohibido — usar 'pieces' + 'pieces_source' (decisión "
                                 f"usuario #2: piezas del header schedule o del detalle del box)")
        kind = o.get("kind")
        if kind != "recessed_accessory" and RX_RECESSED.search(str(ref)):
            raise ValueError(f"{ref}: es un recessed accessory por su nombre — no es header (60.5); "
                             f"va a framed_openings.py (R.O. <= stud bay -> 0; mayor -> RFI)")
        if kind != "grille" and re.search(r"grille", str(ref), re.I):
            raise ValueError(f"{ref}: coiling grille -> kind 'grille' con beams + beams_source (4/A08.21)")
        if kind == "recessed_accessory":
            raise ValueError(f"{ref}: recessed accessory no es header (60.5) -> framed_openings.py")
        if kind not in KINDS:
            raise ValueError(f"{ref}: kind '{kind}' desconocido ({', '.join(sorted(KINDS))}, recessed_accessory)")
        ro = _pos(o.get("ro_w_ft"), f"{ref}.ro_w_ft")
        qty = o.get("qty", 1)
        if not isinstance(qty, int) or isinstance(qty, bool) or qty < 1:
            raise ValueError(f"{ref}: qty debe ser entero >= 1")
        beams = 1
        if kind == "grille":
            if "beams" not in o:
                raise ValueError(f"{ref}: grille sin 'beams' — contar los box beam headers que dibuja el detalle "
                                 f"(4/A08.21: DOS)")
            beams = o["beams"]
            if not isinstance(beams, int) or isinstance(beams, bool) or beams < 1:
                raise ValueError(f"{ref}: beams debe ser entero >= 1")
            _src(o.get("beams_source"), f"{ref}.beams")
        elif "beams" in o:
            raise ValueError(f"{ref}: 'beams' solo para kind grille (las piezas van en 'pieces')")
        base = {"ref": ref, "wall": o.get("wall"), "kind": kind, "qty": qty, "source": src}
        if kind in NOT_FRAMED:
            filas.append(dict(base, estado="NOT_FRAMED", header_lf=0.0, sill_lf=0.0,
                              operacion="duct / fire damper: no se enmarca (decisión usuario #12) -> 0 header, 0 sill",
                              description=f"{kind} {ref}: not framed (no header, no sill)"))
            continue
        if kind == "storefront" and o.get("location") == "exterior":
            _src(o.get("structure_source"), f"{ref}: storefront exterior sin structure_source (barrer el plan "
                                            f"estructural por lintels HSS antes de cargar header metal)")
        if o.get("structure_source") is not None or o.get("structure") is not None:
            st = o.get("structure")
            if st not in STRUCT:
                raise ValueError(f"{ref}: structure debe ser {' | '.join(sorted(STRUCT))} (lo que dibuja "
                                 f"{o.get('structure_source')})")
            _src(o.get("structure_source"), f"{ref}.structure")
            if st != "none":
                slf = 0.0                                  # v65: el lintel de acero no quita el sill de la abertura
                if o.get("with_sill"):
                    spz = 2 if (dbl_sill is not None and ro > dbl_sill + EPS) else 1
                    if "sill_pieces" in o:
                        spz = _sill_pz(o, spz, ref)
                    slf = (ro + EXTRA_FT) * spz * qty
                    tot["sill track"] += slf
                filas.append(dict(base, estado="STEEL_BY_OTHERS", header_lf=0.0, sill_lf=round(slf, 2),
                                  operacion=f"{st} lintel ({o['structure_source']}) -> steel by others, 0 metal stud "
                                            f"header (decisión usuario #16)",
                                  description=f"{kind} {ref}: steel header by others ({o['structure_source']})"))
                continue
        sill = bool(o.get("with_sill", False))
        if ro * 12 <= bay + EPS:
            filas.append(dict(base, estado="FITS_MODULE", header_lf=0.0, sill_lf=0.0,
                              operacion=f"R.O. {round(ro * 12, 3)}\" <= stud bay {bay}\" (60.10) -> no header/sill",
                              description=f"{kind} {ref}: fits within stud bay, no framed opening"))
            continue
        if o.get("header_type"):
            tipo = str(o["header_type"])
            tsrc = _src(o.get("header_type_source"), f"{ref}.header_type")
            if "pieces" not in o:
                raise ValueError(f"{ref}: header_type sin 'pieces' — contar TODAS las piezas del box / header en el "
                                 f"detalle (decisión usuario #2)")
            pz = _int1(o["pieces"], f"{ref}.pieces")
            _src(o.get("pieces_source"), f"{ref}.pieces")
            pieza = str(o.get("piece") or tipo)
            if "BOX" not in tipo.upper():                                   # decisión usuario #21
                for mx, t, n, pc in filas_sch:
                    if ro <= mx + SPAN_TOL:
                        if pz < n:
                            raise ValueError(f"{ref}: {pz} pieza(s) < {n} del header schedule ({t}, {ssrc}) para "
                                             f"R.O. {_ftin(ro)} — el schedule manda (decisión usuario #21)")
                        break
        elif "pieces" in o:
            raise ValueError(f"{ref}: 'pieces' sin header_type + header_type_source")
        else:
            tipo = None
            for mx, t, n, pc in filas_sch:
                if ro <= mx + SPAN_TOL:
                    tipo, tsrc, pz, pieza = t, ssrc, n, pc
                    break
            if tipo is None:
                raise ValueError(f"{ref}: R.O. {_ftin(ro)} sin fila en el header schedule y sin header_type + pieces "
                                 f"— no hay piezas: RFI y declarar header_type/pieces con su detalle (decisión #2)")
        lf = (ro + EXTRA_FT) * pz * beams * qty
        spz = 0
        if sill:
            spz = 2 if (dbl_sill is not None and ro > dbl_sill + EPS) else 1
            if "sill_pieces" in o:
                spz = _sill_pz(o, spz, ref)
                _src(o.get("sill_pieces_source"), f"{ref}.sill_pieces")
        slf = (ro + EXTRA_FT) * spz * qty
        tot["header"] += lf
        tot["sill track"] += slf
        por_pieza[pieza] = por_pieza.get(pieza, 0.0) + lf
        desc = (f"Header, {tipo} ({tsrc}), {pz} piece(s), {o.get('location', '')} {kind} {ref}: "
                f"R.O. {_ftin(ro)} + 1'-4\"").replace("  ", " ")
        op = f"({ro} + 1.333) x {pz} piece(s) x {beams} beam(s) x {qty} = {round(lf, 2)}"
        if sill:
            regla = f" ({srsrc}: > {dbl_sill} ft)" if spz == 2 and sr is not None and "sill_pieces" not in o else ""
            op += f"; sill ({ro} + 1.333) x {spz} piece(s) x {qty} = {round(slf, 2)}{regla}"
        filas.append(dict(base, estado="HEADER", header_type=tipo, pieces=pz, piece=pieza, sill_pieces=spz,
                          header_lf=round(lf, 2), sill_lf=round(slf, 2), operacion=op, description=desc))
    return {"totales_lf": {k: round(v, 2) for k, v in tot.items()}, "reglas": "v65b #18-#22",
            "por_pieza": {k: round(v, 2) for k, v in por_pieza.items()}, "renglones": filas, "avisos": avisos}


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    try:
        out = calcular(json.load(open(argv[1])))
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as e:
        print(f"ERROR headers.py: {e}", file=sys.stderr)
        return 1
    open(argv[2], "w").write(json.dumps(out, indent=1))
    print(json.dumps(out["totales_lf"]))
    for a in out["avisos"]:
        print("AVISO", a)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
