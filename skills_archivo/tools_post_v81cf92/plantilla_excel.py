#!/usr/bin/env python3
"""plantilla_excel.py — UN SOLO formato de Excel para todo take-off de metal frame y drywall.

Por qué (pruebas de 13/14-oct-2026): cada corrida armó un Excel distinto (hojas, columnas y
nombres diferentes). Así no se puede revisar ni calificar igual. Desde v52, el take-off escribe
sus datos en un JSON y ESTE script arma el Excel, siempre con las mismas hojas y columnas
(las del take-off del usuario: Inputs, Partition Takeoff, Material Summary, ...).

v67 (accesorios y partition types, 17-oct-2026):
  - `armar ... --familias familias_out.json` (salida de canon.py v67) escribe en Material Summary UN renglón por
    familia de accesorios / extras con el nombre EXACTO (accesorios.NOMBRES_EXCEL), reemplaza los renglones a
    mano de esas familias, agrega los RFIs de accesorios y la exclusión de insulation (Alcances). Una familia
    de accesorios PENDIENTE = NO SE ARMA (el agente la resuelve del plano o deja accesorios_rfi con delta).
  - con --familias la hoja Partition Takeoff sale de partition_types (CONVENCION_PARTITION_TYPES): bloques
    "TYPE X", un renglón por wall (R2), jogs en la Location (R3), OTHER FRAMING en su propio bloque y el
    renglón TOTAL con la columna A vacía (texto en la B).
  - un renglón que cita su familia ("familia" o "familias_out.json ... '<familia>'" en source) toma el NET de
    familias_out.json: el Excel no arrastra números de una corrida anterior del canon.
  - waste "none" en un material = sin desperdicio (yields de accesorios). Unidad LB válida.
  - `verificar <excel.xlsx>`: lo usa bitacora.py compuerta (familias de accesorios + convención de types).

v70 (#18A): `verificar` FALLA si un renglón del Material Summary que cita la salida de una tool en "Where it comes
from" (`<tool>_out.json ... '<familia>'`: familias_out.json, framed_openings_out.json, accesorios_out.json…) queda
con Net 0 mientras esa salida da > 0 para la misma familia (#18A: framed openings MEP leído con la clave
equivocada -> 0 LF y ninguna compuerta lo vio). Las salidas se buscan junto al Excel y en `--salidas <dir>`.

Uso:
  plantilla_excel.py validar <takeoff.json>              exit 1 si el JSON no cumple el formato
  plantilla_excel.py armar   <takeoff.json> <salida.xlsx> --familias <work>/out/familias_out.json [--trabajo <work>]
                                                         v72b: corre reglas.py compuerta <work>; si no da OK NO
                                                         escribe el Excel (sin override); el libro sale sellado
  plantilla_excel.py verificar <excel.xlsx> [--salidas dir]  familias de accesorios + hoja Partition Takeoff +
                                                         renglones en 0 contra la salida de la tool que citan
                                                         + R70.8 (yields de drywall screws / compound / tape)
  plantilla_excel.py ejemplo <takeoff.json>              escribe un JSON de ejemplo para copiar

Formato del JSON (todas las cantidades NET, sin waste: el waste lo pone el Excel):
{
 "proyecto": "<project name, city>", "bid_set": "...pdf", "fecha": "2026-10-14",
 "inputs": {"waste_metal": 0.15, "waste_no_metal": 0.06, "sheet_w_ft": 4, "sheet_l_ft": 12,
            "stud_stock_ft": 20, "track_stock_ft": 10},
 "walls": [ {"type": "A1", "wall": "<ref>", "location": "<room> east", "length_lf": <n>,
             "height_ft": <n>, "stud_size": "3-5/8\"", "stud_oc_in": 16, "layers": 2,
             "board_sf": <n>, "source": "3/A12.01", "status": "CONFIRMADO"} ],
 "materials": [ {"material": "3-5/8\" metal stud 362S137-33", "unit": "LF", "net": <n>,
                 "metal": true, "selling_unit": "stick 20 ft", "stock": 20, "cut_ft": <n>,
                 "source": "Partition Takeoff col ...; 3/A12.01"} ],
 Opcionales por material: "cut_ft" (OBLIGATORIO en studs con stock: largo típico de corte),
 "sheet_sf" (si selling_unit no trae AxB), "waste_pct" (fija el waste de esa fila).
 Filas en SF: "4x8 sheet" -> 32 SF por pieza; sin AxB ni "sheet" (batt, Level 5) -> se compran por SF.
 EA/PCS con net <= 20 (piezas de schedule) van sin waste salvo "waste_pct".
 "rfis": [ {"id": "RFI-01", "pregunta": "...", "delta": "..."} ],
 "revisar": [ {"n": 1, "total": N, "fase": "floor_plan" | "detalle", "type": "A1" (floor_plan),
               "orden_plano": 1 (detalle), "punto": "...", "hoja_detalle": "6/A12.01", "imagen": "R01.jpg"} ],
   (v77c U9/U10: orden floor plan por type A-Z, después detalles por orden_plano; ordenar_revisar lo hace)
 "alcances": [ {"id": "ALC-01", "nombre": "...", "estado": "CUANTIFICADO | NO APLICA | RFI", "nota": "..."} ]
}
"""
import json, os, re, shutil, subprocess, sys, tempfile
from collections import Counter

UNITS = {"LF", "SF", "EA", "PCS", "LB"}
STATUS = {"CONFIRMADO", "DERIVADO", "PENDIENTE"}
WALL_KEYS = ["type", "wall", "location", "length_lf", "height_ft", "stud_size", "stud_oc_in",
             "layers", "board_sf", "source", "status"]
MAT_KEYS = ["material", "unit", "net", "metal", "source"]


# v77c (decisiones del usuario U9 / U10, R77.13 / R77.14): preguntas al estimador / PARA REVISAR. Orden OBLIGATORIO:
# 1) FLOOR PLAN: las partitions en orden ALFABÉTICO de type; 2) los DETALLES que marca el floor plan, en el orden en
# que el floor plan los marca. Se anuncia el total ("N preguntas en total, una a la vez") y cada item lleva n/N.
FASES_REV = ("floor_plan", "detalle")
NHOJA_REV = re.compile(r"\b[0-9A-Z]{1,3}/[A-Z]{1,2}(?:\d{1,2}\.\d{1,2}|-?\d{3}[A-Z]?)\b")


def _nat(t):
    return [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", str(t).upper())]


def clave_revisar(x):
    f = str(x.get("fase") or "")
    if f == "floor_plan":
        return (0, _nat(x.get("type")), 0)
    return (1, [], int(x.get("orden_plano") or 0))


def ordenar_revisar(lst):
    """Ordena (floor plan por type A→Z; después detalles por orden_plano) y numera n = 1..N con total N."""
    out = sorted((dict(x) for x in lst), key=clave_revisar)
    for i, x in enumerate(out, 1):
        x["n"], x["total"] = i, len(out)
    return out


def revisar_err(lst):
    err = []
    for i, x in enumerate(lst or []):
        f = x.get("fase")
        if f not in FASES_REV:
            err.append(f"revisar[{i}]: fase {f!r} (U10: 'floor_plan' con su type, o 'detalle' con orden_plano)")
            continue
        if f == "floor_plan" and not str(x.get("type") or "").strip():
            err.append(f"revisar[{i}]: floor_plan sin type (U10: partitions en orden alfabético de type)")
        if f == "detalle" and (not isinstance(x.get("orden_plano"), int) or x["orden_plano"] < 1 or
                               not NHOJA_REV.search(str(x.get("hoja_detalle") or ""))):
            err.append(f"revisar[{i}]: detalle sin orden_plano (entero >= 1, orden en que el floor plan lo marca) o "
                       f"sin N/HOJA en hoja_detalle (U10)")
    if err:
        return err
    if [clave_revisar(x) for x in lst] != sorted(clave_revisar(x) for x in lst):
        err.append("revisar: fuera del orden obligatorio (U10: floor plan por type A→Z, después los detalles en el "
                   "orden del floor plan); usar ordenar_revisar")
    if [x.get("n") for x in lst] != list(range(1, len(lst) + 1)) or \
            any(x.get("total") != len(lst) for x in lst):
        err.append(f"revisar: numeración n/N incompleta (U9: n = 1..{len(lst)} y total = {len(lst)} en cada item)")
    return err


def validar(d):
    err = []
    for k in ("proyecto", "bid_set", "fecha", "inputs", "walls", "materials", "rfis", "revisar", "alcances"):
        if k not in d:
            err.append(f"falta la clave '{k}'")
    if err:
        return err
    err += acoustical_err(d["materials"])                 # v77c U8 (R77.12)
    err += revisar_err(d["revisar"])                       # v77c U9 / U10 (R77.13 / R77.14)
    for i, w in enumerate(d["walls"]):
        for k in WALL_KEYS:
            if k not in w or w[k] in ("", None):
                err.append(f"walls[{i}] ({w.get('type')} #{w.get('wall')}): falta '{k}'")
        for k in ("length_lf", "height_ft", "board_sf"):
            if k in w and not (isinstance(w[k], (int, float)) and w[k] >= 0):
                err.append(f"walls[{i}]: '{k}' debe ser número >= 0")
        if w.get("status") not in STATUS:
            err.append(f"walls[{i}]: status debe ser {sorted(STATUS)}")
        if w.get("source") and not re.search(r"\b[0-9A-Z]{1,3}/[A-Z]{1,2}-?\d", str(w["source"])) and w.get("status") != "PENDIENTE":
            err.append(f"walls[{i}]: source debe citar DETALLE/HOJA (forma N/HOJA)")
    nombres = set()
    for i, m in enumerate(d["materials"]):
        for k in MAT_KEYS:
            if k not in m or m[k] in ("", None):
                err.append(f"materials[{i}] ({m.get('material')}): falta '{k}'")
        if str(m.get("unit", "")).upper() not in UNITS:
            err.append(f"materials[{i}]: unit debe ser {sorted(UNITS)}")
        if not (isinstance(m.get("net"), (int, float)) and m["net"] >= 0):
            err.append(f"materials[{i}]: net debe ser número >= 0")
        if re.search(r"\b(PENDING|ALTERNATE|EXCLUDED)\b", str(m.get("material", ""))):   # en MAYÚSCULAS = marca de estado
            err.append(f"materials[{i}]: un renglón PENDING/ALTERNATE no va en Material Summary "
                       f"(va en RFIs o en una hoja de alternates aparte)")
        # v68 (#16): 'cut_ft' ya no se usa (cobraba el desperdicio dos veces: 15 % + un stick por corte).
        if re.search(r"plywood", str(m.get("material", "")), re.I) and str(m.get("unit", "")).upper() == "SF":
            err += [f"materials[{i}]: {e}" for e in plywood_err(m.get("material"))]
        if m.get("material") in nombres:
            err.append(f"materials[{i}]: material repetido '{m.get('material')}'")
        nombres.add(m.get("material"))
    for i, x in enumerate(d["rfis"]):
        if x.get("delta") in (None, "", {}, []):
            err.append(f"rfis[{i}] ({x.get('id')}): sin delta (número con unidad, o 'n/a: <motivo>'; v68)")
    for i, a in enumerate(d["alcances"]):
        if a.get("estado") not in ("CUANTIFICADO", "NO APLICA", "RFI", "CLOSED"):     # R80e.96: RFI cerrado por el estimador
            err.append(f"alcances[{i}]: estado debe ser CUANTIFICADO / NO APLICA / RFI (o CLOSED: RFI decidido)")
    return err


# ---- Unidades de compra ----
# 15-oct (#8): 4x8 = 32 SF; batt / Level 5 por SF; sin waste en piezas de schedule.
# v68 (arbitraje #16): el desperdicio se aplica UNA vez: Pieces = ROUNDUP(NET x (1 + waste) / stock). Se retiró
# "un stick por largo de corte" (cut_ft), que sobre el Purchase (ya con 15 %) cobraba el desperdicio dos veces.
# Todo stock / cobertura sale de una celda REAL de la hoja Inputs (INPUTS_V68), igual que el Material Summary del
# estimador; las yields de accesorios también, con su fórmula viva en la columna J.
_DIM = re.compile(r"(\d+(?:\.\d+)?)\s*[x×]\s*(\d+(?:\.\d+)?)", re.I)
CONTADO_MAX = 20      # EA/PCS con net <= esto son piezas de schedule: sin waste salvo waste_pct

# (fila, clave en d["inputs"], parámetro, default, nota) - mismas filas que la hoja Inputs del estimador
INPUTS_V68 = [
    (5, "waste_metal", "Waste - ALL METAL, any type", 0.15, "Estimator standing rule: 15% on everything that is metal."),
    (6, "waste_no_metal", "Waste - EVERYTHING THAT IS NOT METAL", 0.06, "Estimator standing rule: same figure as board."),
    (7, "sheet_w_ft", "Board sheet width (ft)", 4, "Sheet size is a parameter; buy the size that wastes least."),
    (8, "sheet_l_ft", "Board sheet length (ft)", 12, "Change it and every sheet count re-rounds."),
    (9, None, "SF per board sheet", "=B7*B8", "Width x length."),
    (10, "stud_stock_ft", "Stud stock length (ft)", 20, "Stud, header, framed opening and stud blocking: sticks."),
    (11, "track_stock_ft", "Track stock length (ft)", 10, "Track, sill track and purlin: runs."),
    (12, "plan_scale_pt_per_ft", "Floor plan scale (pt/ft)", None, "Project value (not used in this take-off: heights are per wall in the Partition Takeoff)."),
    (13, "bod_ft", "B.O. Deck (ft)", None, "Project value (not used in this take-off: heights are per wall in the Partition Takeoff)."),
    (14, "top_parapet_ft", "T.O. Parapet (ft)", None, "Project value (not used in this take-off: heights are per wall in the Partition Takeoff)."),
    (15, "sealant_lf_per_tube", "Sealant coverage (LF per tube)", 25, "Sealant yield per tube - set your supplier's figure."),
    (16, "crc_stock_ft", "C.R. channel stock length (ft)", 16, "1-1/2\" cold-rolled channel (bracing, carrying channel)."),
    (17, "hat_stock_ft", "Hat / furring / resilient channel stock (ft)", 12, "7/8\" hat furring channel and 087F125 resilient channel."),
    (18, "trim_stick_ft", "Trim stick length (ft)", 10, "Corner bead, casing bead, shadow molding, PVC trim."),
    (19, "hanger_wire_purchase", "Hanger wire purchase", "continuous coil (LF)",
     "Bought by LF from a continuous coil; when the take-off gives the hanger count it goes on its own PCS row."),
    (20, "drywall_screws_per_sf", "Drywall screws per SF of board", 1.2, "YIELD (GA-216 field / perimeter spacing)."),
    (21, "framing_screws_per_stud", "Framing screws per stud piece", 4, "YIELD: 2 per stud-to-track connection, each end."),
    (22, "slab_pin_spacing_ft", "Power-driven pin spacing (ft)", 1.0, "YIELD: bottom track on slab, interior walls."),
    (23, "joint_compound_lb_per_sf", "Joint compound (lb per SF)", 0.072,
     "YIELD: 72 lb per 1,000 SF, level 4 (estimator standing input). Yields carry no waste (estimator rule)."),
    (24, "joint_tape_lf_per_sf", "Joint tape (LF per SF)", 0.37, "YIELD: 370 LF per 1,000 SF (estimator standing input). Yields carry no waste (estimator rule)."),
    (25, "anchor_spacing_ft", "Expansion anchor spacing (ft)", 8 / 12, "YIELD: exterior bottom track on slab."),
    # v80q (R80e.32): largos de fábrica de los renglones LF que no son metal framing (nunca escritos en la fórmula)
    (26, "lumber_stock_ft", "2x lumber stock length (ft)", 16, "2x wood / FRT blocking: 16 ft sticks (precedent: estimator decision 2026-10-27; estimator standing input)."),
    (27, "main_tee_ft", "Drywall grid main tee length (ft)", 12, "USG DGLW26 main tee (manufacturer length)."),
    (28, "cross_tee_ft", "Drywall grid cross tee length (ft)", 4, "USG DGLW424 cross tee (manufacturer length)."),
    (29, "molding_ft", "Grid channel / angle molding length (ft)", 12, "USG DGCM27 / DGWM24 molding (manufacturer length)."),
    (30, "frp_panel_sf", "FRP panel (SF per panel)", 40, "FRP-1 panel 4'x10' (estimator to confirm the panel size)."),   # v80r
]
CELDA = {k: f"Inputs!$B${r}" for r, k, *_ in INPUTS_V68 if k}
CELDA["sheet_sf"] = "Inputs!$B$9"
INPUT_ROWS = {r for r, *_ in INPUTS_V68}
# Clase de compra por nombre: (regex, solo metal, selling unit (formato con el stock), clave de Inputs)
COMPRA_V68 = [
    # v80p (R80e.31): renglones LF que no son metal framing: la pieza de compra es su largo de fábrica, nunca un pie lineal suelto
    (r"\bemt\b", False, "EMT stick 10 ft (standard trade length)", None),   # R80e.127: EMT compression strut (K/A12.02), no C.R. channel
    (r"main tee", False, "main tee {v:g} ft", "main_tee_ft"),
    (r"cross tee", False, "cross tee {v:g} ft", "cross_tee_ft"),
    (r"channel molding|angle molding|wall molding|curved .*molding", False, "molding {v:g} ft", "molding_ft"),
    (r"\bwire\b", False, "continuous coil (LF)", None),
    (r"mesh tape|sealer gasket", False, "roll (LF)", None),   # R80w.41: rollo, no metal
    (r"blocking.*(wood|2x)|(wood|2x).*blocking", False, "2x lumber {v:g} ft", "lumber_stock_ft"),
    (r"sealant", False, "tube ({v:g} LF per tube)", "sealant_lf_per_tube"),
    (r"hanger wire", False, "continuous coil (LF)", None),
    (r"header|box beam|framed opening|extra framing|cfmf|\bstud\b|studs|kicker|joist|362cr|stud blocking",
     True, "stick {v:g} ft", "stud_stock_ft"),
    (r"flat strap|\bstrap\b|\bstrapping\b", True, "coil (LF)", None),   # R80e.86: el strap se compra en rollo (LF); U-177: '6" sheet metal blocking strapping' también
    (r"resilient channel", True, "resilient channel {v:g} ft", "hat_stock_ft"),   # R80e.86: pieza de 12 ft (Inputs)
    (r"bracing|carrying channel|c\.r\. channel|cold[- ]rolled", True, "C.R. channel {v:g} ft", "crc_stock_ft"),
    (r"furring channel|hat channel", True, "hat channel {v:g} ft", "hat_stock_ft"),
    (r"corner bead|casing|shadow|metal trim|metal reveal|reveal trim|frp top / edge trim|pvc trim|l[- ]bead|j[- ]bead|edge trim|edge molding|control joint", False, "trim stick {v:g} ft",   # R80e.86: + W-4 edge molding
     "trim_stick_ft"),
    (r"spacing bar", True, "spacing bar, product length per manufacturer (LF)", None),   # BE-HF12
    (r"track|purlin|\bsill\b|runner", True, "run {v:g} ft", "track_stock_ft"),
]
# Las cinco + dos yields de accesorios: familia -> (clave de Inputs, operación con el driver)
YIELDS = {"drywall screws": "drywall_screws_per_sf", "joint compound": "joint_compound_lb_per_sf",
          "joint tape": "joint_tape_lf_per_sf", "framing screws": "framing_screws_per_stud",
          "slab pins": "slab_pin_spacing_ft", "expansion anchors": "anchor_spacing_ft"}


def _inp(d, k):
    for r, kk, lab, dflt, nota in INPUTS_V68:
        if kk == k:
            return (d.get("inputs") or {}).get(k, dflt)


def clase_compra(m, d=None):
    """(selling_unit, celda de Inputs o None) de un renglón LF por su nombre, o None si no tiene clase."""
    if str(m.get("unit", "")).upper() != "LF":
        return None
    n = str(m.get("material", "")).lower()
    for rx, solo_metal, sel, k in COMPRA_V68:
        if re.search(rx, n) and (m.get("metal") or not solo_metal):
            if k is None:
                return sel, None
            return sel.format(v=float(_inp(d or {}, k))), CELDA[k]
    return None


def sheet_sf(m):
    """SF por pieza de compra de una fila en SF, o None si se compra por SF suelto."""
    if m.get("sheet_sf"):
        return float(m["sheet_sf"])
    g = _DIM.search(str(m.get("selling_unit", "")))
    return float(g.group(1)) * float(g.group(2)) if g else None


def waste_celda(m, REF):
    if m.get("waste") == "none":                       # v67: yields de accesorios sin desperdicio
        return 0
    if m.get("waste_pct") is not None:
        return float(m["waste_pct"])
    if str(m["unit"]).upper() in ("EA", "PCS") and float(m["net"]) <= CONTADO_MAX:
        return 0
    # v80r (rev11, decisión estimador 2026-10-27): el blocking de madera (2x / FRT) es no metal
    if re.search(r"(?i)blocking.*(wood|2x)|(wood|2x).*blocking", str(m.get("material", ""))):
        return "=" + REF["waste_no"]
    return "=" + (REF["waste_metal"] if m["metal"] else REF["waste_no"])


def formula_piezas(m, r, d=None):
    """Pieces to buy = ROUNDUP(Purchase / stock) con Purchase = NET x (1 + waste): el desperdicio UNA vez.
    rev15 (F08): con m['piezas_min'] (studs de largo > stock / 2: un stick por stud) -> =MAX(ROUNDUP(...), piezas_min)."""
    if m.get("piezas_min"):
        base = formula_piezas(dict(m, piezas_min=None), r, d)
        return f"=MAX({base[1:]},{int(m['piezas_min'])})"
    unit = str(m["unit"]).upper()
    if unit == "SF" and re.search(r"\bFRP\b", str(m.get("material", ""))):     # v80r: panel FRP desde Inputs
        return f"=ROUNDUP(F{r}/{CELDA['frp_panel_sf']},0)"
    if unit == "SF":
        sf = sheet_sf(m)
        sel = str(m.get("selling_unit", "")).lower()
        inp = float(_inp(d or {}, "sheet_w_ft")) * float(_inp(d or {}, "sheet_l_ft"))
        if (sf and abs(sf - inp) < 1e-9) or (not sf and ("sheet" in sel or "board" in sel)):
            return f"=ROUNDUP(F{r}/{CELDA['sheet_sf']},0)"
        if sf:
            return f"=ROUNDUP(F{r}/{sf:g},0)"
        return f"=ROUNDUP(F{r},0)"
    c = clase_compra(m, d)
    if c and c[1]:
        return f"=ROUNDUP(F{r}/{c[1]},0)"
    if c:
        g = re.search(r"(\d+(?:\.\d+)?)\s*ft\b", c[0])   # v80p: la clase trae el largo de la pieza
        return f"=ROUNDUP(F{r}/{float(g.group(1)):g},0)" if g else f"=ROUNDUP(F{r},0)"
    if m.get("stock"):
        return f"=ROUNDUP(F{r}/{float(m['stock']):g},0)"
    # v65 (#14A): "piece 8 ft" sin stock daba 820 "pieces" = LF. El largo de la selling unit manda; "LF" = LF.
    g = re.search(r"(\d+(?:\.\d+)?)\s*(?:ft|')", str(m.get("selling_unit", "")), re.I)
    if unit == "LF" and g:
        return f"=ROUNDUP(F{r}/{float(g.group(1)):g},0)"
    return f"=ROUNDUP(F{r},0)"


# ---- v68: FRT plywood por material y espesor ----
FRT_CLASES = [   # (regex sobre el texto del renglón, nombre del renglón con {th})
    (r"polyiso|nailbase|bonded", "{th} FRT plywood nailbase bonded to polyiso (exterior sheathing)"),
    (r"column", "{th} FRT plywood at column wraps"),
    (r"\bpiers?\b", "{th} FRT plywood at piers"),
    (r"canopy|fascia|soffit", "{th} FRT plywood sheathing (canopy, fascia and soffits)"),
    (r"backboard", "{th} FRT plywood backboards"),
    (r"jamb|liner|opening", "{th} FRT plywood at opening jambs"),
    (r"", "{th} FRT plywood substrate"),
]
_TH = re.compile(r"(\d+-\d+/\d+|\d+/\d+)\s*(?:\"|in\b|”)")


def espesor(t):
    ths = sorted(set(_TH.findall(str(t))))
    return ths


def clase_frt(texto):
    """Renglón de compra de una pieza de FRT plywood por su texto (ref / source / operación). ValueError sin
    espesor: un renglón de plywood sin espesor no se compra."""
    t = str(texto)
    ths = [x for x in espesor(t) if x in ("1/2", "5/8", "3/4", "1-1/8", "1-1/4")]
    if not ths:
        raise ValueError(f"FRT plywood sin espesor: '{t[:80]}'")
    th = ths[0] + '"'
    for rx, nom in FRT_CLASES:
        if re.search(rx, t, re.I):
            return nom.format(th=th)


def _usos_frt(n):
    usos = {rx for rx, _ in FRT_CLASES[:-1] if re.search(rx, n, re.I)}
    if "column" in usos:                      # "canopy column wraps" es un solo material
        usos.discard("canopy|fascia|soffit")
    return usos


def plywood_err(nombre):
    n = str(nombre)
    err = []
    if not espesor(n):
        err.append(f"renglón de plywood sin espesor '{n[:60]}' (un renglón por material y espesor; v68)")
    if len({x for x in espesor(n) if x in ("1/2", "5/8", "3/4", "1-1/8", "1-1/4")}) > 1:
        err.append(f"renglón de plywood con dos espesores '{n[:60]}' (separar por espesor; v68)")
    if len(_usos_frt(n)) > 1 or re.search(r"plywood \([^)]*/", n, re.I):
        err.append(f"renglón de plywood que mezcla materiales '{n[:60]}' (separar por material; v68)")
    return err


# ---- v68: Excel íntegro en inglés (texto que generan las tools; el texto del agente lo exige verificar) ----
TRAD = [
    (r"aberturas con box propio \(openings_extra\) > 4'-0\": ¿llevan también el head track adicional de "
     r"([^?]+)\?", "openings with their own box (openings_extra) > 4'-0\": do they also take the additional "
                    "head track of \\1?"),                       # v78 (R78.12): la cita viene del texto, no fija
    (r"spacing del pin: 12\" \(anchorage interior\) vs 16\" \(fastener schedule\) vs 24\" \(caja del tipo K\)",
     "pin spacing: 12\" (interior anchorage) vs 16\" (fastener schedule) vs 24\" (type K box)"),
    (r"ancho del jamb return no acotado", "jamb return width not dimensioned"),
    (r"criterio estimador \(ref v4: ancho del return = profundidad del stud 6\", no acotado; RFI con delta a "
     r"0\.20 ft\)", "estimator criterion (return width = stud depth, not dimensioned; RFI with delta at 0.20 ft)"),
    (r"criterio estimador \(ref v4: 4 inside corners por cuarto rectangular\)",
     "estimator criterion (4 inside corners per rectangular room)"),
    (r"decisión usuario #(\d+): R\.O\. \+ 1'-4\" \(8\" de bearing cada lado\)",
     r"user decision #\1: R.O. + 1'-4\" (8\" bearing each side)"),
    (r"decisi[oó]n (?:del )?usuario", "user decision"), (r"(?<!user )decisi[oó]n #", "user decision #"),
    (r"criterio (?:del )?estimador", "estimator criterion"), (r"\bcriterio\b", "criterion"),
    (r"\(todos los gauges\)", "(all gauges)"), (r"\(todos\)", "(all)"),
    (r"track de ceilings / soffits", "ceiling / soffit track"),
    (r"arriba y abajo", "top and bottom"), (r"\babajo\b", "bottom"), (r"\barriba\b", "top"),
    (r"studs a estructura", "studs to structure"), (r"muro sur de cada office", "south wall of each office"),
    (r"\bsobre cove base\b", "over cove base"), (r"\(no es blocking ni sill\)", "(not blocking or sill)"),
    (r"no acústico; la familia del calificador lo suma", "not acoustical"),
    (r"\bpolígono\b", "polygon"), (r"\bperímetro\b", "perimeter"), (r"\bmuesca\b", "notch"),
    (r"pipes dentro del chase, sin plate", "pipes inside the chase, no plate"),
    (r"\[DERIVADO por tag, ver PARA REVISAR\]", "[DERIVED by tag, see Review Items]"),
    (r"\bCONFIRMADO\b", "CONFIRMED"), (r"\bDERIVADO\b", "DERIVED"), (r"\bPENDIENTE\b", "PENDING"),
    (r"\bCUANTIFICADO\b", "QUANTIFIED"), (r"\bNO APLICA\b", "NOT APPLICABLE"), (r"\bCRITERIO\b", "CRITERION"),
]
ES_SUELTO = re.compile(r"[áéíóúñ¿¡]|\b(criterio|estimador|abajo|arriba|muro|ancho|aberturas|acotad[oa]|"
                       r"cuantificad[oa]|confirmado|derivado|pendiente|cerrad[oa]|segun|según|usuario|"
                       r"hoja|detalle|cara|caras|altura)\b", re.I)


def en(t):
    if not isinstance(t, str):
        return t
    for a, b in TRAD:
        t = re.sub(a, b, t)
    return t


# v77 (R76.7 b): rutas, nombres de archivo, ids de wall, coordenadas "x / y <pt>" y elevaciones "EL." no son texto:
# daban falso español y bloqueaban la entrega. Se quitan antes de buscar español.
NO_TEXTO = [re.compile(x, re.I) for x in (
    r"(?:[A-Za-z]:)?(?:[/\\][\w.\-]+){2,}[/\\]?",               # rutas
    r"\b[\w\-]+\.(?:png|jpe?g|json|jsonl|xlsx|pdf|md|py|txt|csv|zip)\b",  # nombres de archivo
    # R80w.19: coordenadas ANTES que los ids: "y 1813-1875" (rango) perdía el número como id y dejaba la "y" suelta
    r"\b[xy]\s*[=:]?\s*-?\d+(?:\.\d+)?(?:\s*(?:-|->|to)\s*\d+(?:\.\d+)?)?",   # coordenadas x / y (y rangos)
    r"\b[A-Za-z]*\d[\w]*(?:-[\w]+)+\b|\b[A-Za-z]+(?:-[A-Za-z]*\d[\w]*)+\b",  # ids con dígitos y guiones
    r"\bEL\.\s*[\d']?",                                            # elevación EL.
)]


def _sin_ids(t):
    # v78 (R78.3): primero ids SIN dígito y listas "#id+id" (idioma_es.quitar_ids, compartido con verif_idioma)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import idioma_es as IE
    t = IE.quitar_ids(t)
    for rx in NO_TEXTO:
        t = rx.sub(" ", t)
    return t


def es_texto_es(t):
    """[] si el texto está en inglés; motivo si no (función de idioma_es + palabras sueltas y acentos).
    v77: rutas, archivos, ids y coordenadas se quitan antes (R76.7 b)."""
    if not isinstance(t, str) or len(t) < 4:
        return []
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import idioma_es as IE
    t = _sin_ids(t)
    return IE.es_espanol(t) or sorted({m.group(0).lower() for m in ES_SUELTO.finditer(t)})


def _estilos():
    from openpyxl.styles import Font, PatternFill, Alignment
    return {"h": Font(bold=True, color="FFFFFF"), "hf": PatternFill("solid", fgColor="1F4E78"),
            "t": Font(bold=True, size=13), "tipo": Font(bold=True), "tf": PatternFill("solid", fgColor="DDEBF7"),
            "yellow": PatternFill("solid", fgColor="FFF2CC"), "wrap": Alignment(wrap_text=True, vertical="top")}


ESTADO_EN = {"CONFIRMADO": "CONFIRMED", "DERIVADO": "DERIVED", "PENDIENTE": "PENDING", "CUANTIFICADO": "QUANTIFIED",
             "NO APLICA": "NOT APPLICABLE", "RFI": "RFI"}
HOJA_REVISAR, HOJA_ALCANCES = "Review Items", "Scope Checklist"


def sha_familias(fo):
    """v72b: huella del contenido de familias_out.json (la que fusionar deja en el takeoff y armar compara)."""
    import hashlib
    return hashlib.sha256(json.dumps(fo, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def armar(d, salida, trabajo):
    """v72b (REGLAS INVIOLABLES): NO escribe el Excel si `reglas.py compuerta <trabajo>` no da OK. La llama aquí, en
    proceso; no hay parámetro ni flag que la salte. Además: el takeoff tiene que venir de `fusionar` con el
    familias_out.json de ESA carpeta de trabajo (mismo contenido), y el libro sale sellado (hoja oculta _reglas)
    con la huella de la corrida: bitacora.py compuerta rechaza un Excel sin sello o con sello vencido."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import reglas
    if not trabajo or not os.path.isdir(trabajo):
        raise reglas.ReglasNoOK("NO SE ARMA: falta la carpeta de trabajo (reglas.py compuerta corre sobre ella)")
    if not d.get("_familias_sha"):
        raise reglas.ReglasNoOK("NO SE ARMA: el takeoff no pasó por fusionar con familias_out.json (--familias)")
    ctx = reglas.Ctx(trabajo)
    fo_p = os.path.join(ctx.out_dir, "familias_out.json") if ctx.out_dir else None
    if not fo_p or sha_familias(json.load(open(fo_p, encoding="utf-8"))) != d["_familias_sha"]:
        raise reglas.ReglasNoOK("NO SE ARMA: --familias no es el familias_out.json de la carpeta de trabajo "
                                f"({fo_p})")
    out = reglas.exigir(trabajo)                    # lanza ReglasNoOK si una sola regla falla
    import trazabilidad                             # v80k (R80e.24): N/HOJA + desglose en el libro, sin archivos internos
    d = trazabilidad.aplicar(d, ctx.out_dir, reglas.buscar_canon(trabajo))
    return _escribir(d, salida, out)


def _escribir(d, salida, out_reglas):
    import openpyxl
    from openpyxl.utils import get_column_letter as L
    S = _estilos()
    wb = openpyxl.Workbook()

    # ---------- Inputs (v68: mismas filas que la hoja Inputs del estimador; toda cita "Inputs!Bn" existe) ----------
    ws = wb.active; ws.title = "Inputs"
    ws["A1"] = f"{en(d['proyecto'])}   |   METAL FRAMING & DRYWALL TAKEOFF"; ws["A1"].font = S["t"]
    ws["A2"] = f"Bid set: {d['bid_set']}   ·   {d['fecha']}   ·   Edit ONLY the yellow cells."
    for c, v in zip("ABC", ("PARAMETER", "VALUE", "NOTE / SOURCE")):
        ws[f"{c}4"] = v; ws[f"{c}4"].font = S["h"]; ws[f"{c}4"].fill = S["hf"]
    for r, k, lab, dflt, nota in INPUTS_V68:
        v = _inp(d, k) if k else dflt
        nota = resolver_cifras((d.get("inputs_notas") or {}).get(k, nota), d)   # v80n + R80f.43: nota con la cita del proyecto (p. ej. nivel de acabado impreso)
        ws.cell(r, 1, lab); ws.cell(r, 2, "n/a" if v is None else v); ws.cell(r, 3, nota)
        if k and v is not None:
            ws.cell(r, 2).fill = S["yellow"]
    # R80e.121 / R-ALC-09 (usuario, TODOS los proyectos): HOJA DE DATOS DEL PROYECTO como renglones informativos de
    # Inputs, DEBAJO de las filas fijas (no mueve ninguna celda Inputs!Bn citada); cada dato con su hoja o [PENDIENTE]
    pdat = d.get("proyecto_datos") or []
    if pdat:
        r0 = ws.max_row + 2
        ws.cell(r0, 1, "PROJECT DATA (informative - not an input)").font = S["h"]
        for i, x in enumerate(pdat, 1):
            ws.cell(r0 + i, 1, en(str(x.get("campo", "")))); ws.cell(r0 + i, 2, en(str(x.get("valor", ""))))
            ws.cell(r0 + i, 3, en(str(x.get("fuente", ""))))
        hc = d.get("hojas_revisadas") or []
        if hc:
            r1 = r0 + len(pdat) + 2
            ws.cell(r1, 1, "MANDATORY SHEETS REVIEWED").font = S["h"]
            for i, x in enumerate(hc, 1):
                ws.cell(r1 + i, 1, en(str(x.get("categoria", "")))); ws.cell(r1 + i, 2, en(str(x.get("estado", ""))))
                ws.cell(r1 + i, 3, en(str(x.get("hojas", ""))))
    pdat = (d.get("project_data") or []) if not d.get("proyecto_datos") else []   # R80w.44 (si no hay proyecto_datos R80e.121) (R-ALC-09): ficha del proyecto, filas informativas
    if pdat:                                             # debajo de los Inputs, mismas 3 columnas, sin celdas amarillas
        r0 = max(x[0] for x in INPUTS_V68) + 2
        ws.cell(r0, 1, "PROJECT DATA SHEET (informative, not an input)").font = S["h"]
        ws.cell(r0, 2, "VALUE"); ws.cell(r0, 3, "SHEET / SOURCE")
        for c in (1, 2, 3):
            ws.cell(r0, c).fill = S["hf"]
        for i, x in enumerate(pdat, 1):
            ws.cell(r0 + i, 1, en(str(x["campo"]))); ws.cell(r0 + i, 2, en(str(x["valor"])))
            ws.cell(r0 + i, 3, en(str(x.get("hoja") or "[PENDING]")))
    REF = {"waste_metal": CELDA["waste_metal"], "waste_no": CELDA["waste_no_metal"]}

    # ---------- Partition Takeoff ----------
    ws = wb.create_sheet("Partition Takeoff")
    ws.append([f"ORGANIZED PARTITION TAKEOFF - {en(d['proyecto'])}"]); ws["A1"].font = S["t"]
    ws.append(["Grouped by partition type. Every row cites its DETAIL/SHEET and its status."]); ws.append([])
    hdr = ["Partition / Scope", "Wall #", "Length (LF)", "Height (FT)", "Layers", "Stud Size",
           "Stud O.C. (in)", "Board (SF)", "Location", "Source (DETAIL/SHEET)", "Status"]
    ws.append(hdr)
    for c in range(1, len(hdr) + 1):
        ws.cell(4, c).font = S["h"]; ws.cell(4, c).fill = S["hf"]
    orden = []
    for w in d["walls"]:
        if w["type"] not in orden:
            orden.append(w["type"])

    def fila_wall(t, w):
        return [f"{t}  #{w['wall']}  -  {en(w['location'])}", str(w["wall"]), w["length_lf"], w["height_ft"],
                w["layers"], w["stud_size"] + (f" {w['gauge']}" if w.get("gauge") else ""), w["stud_oc_in"], w["board_sf"],
                en(w["location"]) + (f" | {en(w['faces_note'])}" if w.get("faces_note") else ""),   # v80k R80e.24
                en(w["source"]), f"[{ESTADO_EN.get(w['status'], w['status'])}]"]
    if d.get("type_order"):                           # v80e (§0.F): orden del Partition Schedule del proyecto
        rank = {str(t).upper(): i for i, t in enumerate(d["type_order"])}
        orden.sort(key=lambda t: rank.get(str(t).upper(), len(rank)))
    subt = []
    for t in orden:
        ws.append([f"TYPE {t}"]); ws.cell(ws.max_row, 1).font = S["tipo"]; ws.cell(ws.max_row, 1).fill = S["tf"]
        f0 = ws.max_row + 1
        for w in sorted([x for x in d["walls"] if x["type"] == t], key=lambda x: _nat(x["wall"])):   # por Wall ID
            ws.append(fila_wall(t, w))
        f1 = ws.max_row
        # v80e (§0.F): SUBTOTAL por type; texto en la col. B (la A vacía: no es un wall)
        ws.append([None, f"SUBTOTAL TYPE {t}", f"=SUM(C{f0}:C{f1})", None, None, None, None, f"=SUM(H{f0}:H{f1})"])
        ws.cell(ws.max_row, 2).font = S["tipo"]
        subt.append(ws.max_row)
    # v67: texto del total en la col. B (con texto en la A el calificador lo suma como un wall del último TYPE)
    if subt or not d.get("existing_walls"):            # BE-CR19: sin metal y con board-only, el total va al final
        ws.append([None, "TOTAL - PARTITIONS (GRAND TOTAL)", "=" + "+".join(f"C{r}" for r in subt) if subt else 0,
                   None, None, None, None, "=" + "+".join(f"H{r}" for r in subt) if subt else 0])
        ws.cell(ws.max_row, 2).font = S["tipo"]
    if d.get("other_framing"):
        ws.append([]); ws.append([f"TYPE {OTHER_TYPE}"])
        ws.cell(ws.max_row, 1).font = S["tipo"]; ws.cell(ws.max_row, 1).fill = S["tf"]
        f0 = ws.max_row + 1
        for w in d["other_framing"]:
            ws.append(fila_wall(w["type"], w))
        f1 = ws.max_row                                 # v81cf8 (T5): OTHER FRAMING with its own subtotal (LF + board SF)
        ws.append([None, "SUBTOTAL OTHER FRAMING", f"=SUM(C{f0}:C{f1})", None, None, None, None, f"=SUM(H{f0}:H{f1})"])
        ws.cell(ws.max_row, 2).font = S["tipo"]
    # v81cf53 (CR City Hotel, BE-CR08b): set wood-framed -> bloques board-only POR TYPE (type_id) en el orden del
    # schedule (type_order), cada uno con su SUBTOTAL; el título = Subject del markup (markups_bluebeam BE-CR06)
    _ex = d.get("existing_walls") or []
    _grupos = [(None, _ex)]
    if _ex and all(e.get("type_id") for e in _ex):
        _ord = [str(t) for t in d.get("type_order") or []]
        _tids = sorted({e["type_id"] for e in _ex}, key=lambda t: (_ord.index(t) if t in _ord else len(_ord), t))
        _grupos = [(t, [e for e in _ex if e["type_id"] == t]) for t in _tids]
    for _tid, _lst in _grupos:
      _sh_ = False
      if _lst:                                          # R80w.39: bloque propio, después de OTHER FRAMING
        _sh_ = all(e.get("stud_text") for e in _lst)      # CR-R10-m2: shaft wall C-H (studs + J-runner en el Material Summary)
        ws.append([]); ws.append([f"TYPE {_tid + (' - SHAFT WALL (C-H STUDS AND J-RUNNER IN THE MATERIAL SUMMARY)' if _sh_ else ' - BOARD ONLY (WOOD FRAMING EXCLUDED)') if _tid else EXIST_TYPE}"])
        ws.cell(ws.max_row, 1).font = S["tipo"]; ws.cell(ws.max_row, 1).fill = S["tf"]
        f0 = ws.max_row + 1
        _prim = []                                      # BE-CR19: filas de la PRIMERA cara de cada wall (LF físico una vez)
        for e in sorted(_lst, key=lambda x: _nat(x["id"])):
            if not re.search(r" [B-Z]$", str(e["id"])):
                _prim.append(ws.max_row + 1)
            ws.append([f"{('Shaft wall (C-H)' if e.get('stud_text') else 'Wood-framed wall') if _tid else 'Existing wall'} {e.get('keynote') or ''}  #{e['id']}  -  {en(e['location'])}",
                       str(e["id"]), e["lf"], e["height_ft"], e["layers"], e.get("stud_text") or "none (board only; framing not in scope)", None,
                       e["board_sf"], en(e["location"]) + f" | {e['faces']} face(s) x {e['layers']} layer(s), "
                       f"{BOARD_EN.get(e.get('board'), e.get('board'))} | {en(e['decision'])}",
                       en(e["source"]), f"[{ESTADO_EN.get(e['status'], e['status'])}]"])
        f1 = ws.max_row
        _lf = ("=" + "+".join(f"C{r}" for r in _prim)) if _prim and len(_prim) < 200 else f"=SUM(C{f0}:C{f1})"
        ws.append([None, f"SUBTOTAL {_tid} {'SHAFT WALL' if _sh_ else 'BOARD ONLY'} (LF = physical wall length, each wall once; SF = all faces x layers)" if _tid else "SUBTOTAL BOARD-ONLY WALLS",
                   _lf, None, None, None, None, f"=SUM(H{f0}:H{f1})"])
        ws.cell(ws.max_row, 2).font = S["tipo"]
        subt.append(ws.max_row)
    if _ex:                                             # BE-CR19: GRAND TOTAL al final, con los bloques board-only
        ws.append([None, "TOTAL - PARTITIONS (GRAND TOTAL)", "=" + "+".join(f"C{r}" for r in subt) if subt else 0,
                   None, None, None, None, "=" + "+".join(f"H{r}" for r in subt) if subt else 0])
        ws.cell(ws.max_row, 2).font = S["tipo"]

    # ---------- Material Summary ----------
    ws = wb.create_sheet("Material Summary")
    ws.append(["MATERIAL SUMMARY - NET / WASTE / PURCHASE"]); ws["A1"].font = S["t"]
    ws.append(["Waste lives HERE, in its own column, applied ONCE: Pieces = ROUNDUP(Net x (1 + waste) / stock). "
               "Every stock length, coverage and yield is an Inputs cell."])
    hdr = ["Material", "Unit", "Net", "Waste %", "Waste", "Purchase", "Selling unit", "Pieces to buy",
           "Where it comes from", "Yield check (live formula)"]
    ws.append(hdr)
    for c in range(1, len(hdr) + 1):
        ws.cell(3, c).font = S["h"]; ws.cell(3, c).fill = S["hf"]
    for m in d["materials"]:
        r = ws.max_row + 1
        unit = str(m["unit"]).upper()
        c = clase_compra(m, d)
        sel = c[0] if c else m.get("selling_unit", "")
        if unit == "SF" and not sheet_sf(m) and re.search(r"sheet|board", str(sel), re.I):
            sel = f"{_inp(d, 'sheet_w_ft'):g}x{_inp(d, 'sheet_l_ft'):g} ft sheet (Inputs)"
        if unit == "SF" and re.search(r"\bFRP\b", str(m.get("material", ""))):    # v80r
            sel = f"FRP panel {_inp(d, 'frp_panel_sf'):g} SF (Inputs)"
        fu = en(m.get("cita") or m["source"])
        # E3 CR City Hotel rev6 (BE-CF10): cada renglón cita su sección / párrafo de spec o 'no spec section' (d["spec_por_material"]:
        # [[regex del material, cita]] leído del Project Manual del proyecto)
        if d.get("spec_por_material") and not re.search(r"\b0[5-9]\s?\d{2}\s?\d{2}\b|(?i:no spec section)", str(fu)):
            sp = next((ci for rx, ci in d["spec_por_material"] if re.search(rx, str(m["material"]), re.I)), None)
            if sp:
                fu = f"{fu} | Spec: {sp}"
        if m.get("piezas_min") and m.get("piezas_min_op"):   # rev15 F08: la operación de las piezas mínimas, visible
            fu = f"{fu} | Pieces min [DERIVED]: {m['piezas_min_op']}"
        ws.append([en(m["material"]), unit, m["net"], waste_celda(m, REF), f"=C{r}*D{r}", f"=C{r}+E{r}",
                   sel, formula_piezas(m, r, d), fu, m.get("yield_formula")])   # v80k R80e.24

    # ---------- RFIs / Review Items / Scope Checklist ----------
    ws = wb.create_sheet("Pending Items")
    # R80e.50: cada RFI en opciones múltiples, orden fijo, DENTRO de las columnas existentes (formato fijo del Excel:
    # nunca se agregan / quitan hojas ni columnas): "(A) plans / specs | (B) trade code | (C) Other: ____"
    ws.append(["RFI", "Question / condition", "Delta of each alternative"])
    for c in range(1, 4):
        ws.cell(1, c).font = S["h"]; ws.cell(1, c).fill = S["hf"]
    for x in rfis_vigentes(d["rfis"]):
        oa, ob = opciones_rfi(x)
        oc = (x.get("opciones") or {}).get("C") or "____"
        if isinstance(oc, dict):                      # R80e.84: la opción C se escribe como texto, nunca como dict crudo
            oc = " | ".join(str(v) for v in (oc.get("texto"), oc.get("cita") or oc.get("source"),
                                             ("delta " + str(oc["delta"])) if oc.get("delta") else None) if v)
        ws.append([x.get("id"), en(x.get("pregunta")), f"(A) {en(oa)} | (B) {en(ob)} | (C) Other: {en(oc)}"])
    ws = wb.create_sheet(HOJA_REVISAR)
    nrev = len(d["revisar"])
    ws.append([f"{nrev} questions in total, asked ONE at a time in this order: floor plan (partition types A-Z), "
               f"then the details the floor plan calls, in order"])
    ws.append(["#", "Phase", "Type / order", "Item", "Sheet + detail", "Image"])
    for x in d["revisar"]:
        fase = "Floor plan" if x.get("fase") == "floor_plan" else "Detail"
        ws.append([f"{x.get('n')}/{nrev}", fase, x.get("type") if x.get("fase") == "floor_plan" else
                   x.get("orden_plano"), en(resolver_cifras(x.get("punto"), d)), x.get("hoja_detalle"),
                   os.path.basename(str(x.get("imagen"))) if x.get("imagen") else x.get("imagen")])   # R80e.153: nombre, sin ruta
    ws = wb.create_sheet(HOJA_ALCANCES)
    ws.append(["Scope ID", "Scope", "Status", "Note (quantity, NOT APPLICABLE + sheet, or RFI)"])
    for x in d["alcances"]:
        ws.append([x.get("id"), en(x.get("nombre")), ESTADO_EN.get(x.get("estado"), x.get("estado")),
                   en(resolver_cifras(x.get("nota"), d))])          # R80f.43: cifras por programa

    for w in wb.worksheets:
        for i, col in enumerate(w.columns, 1):
            ancho = max((len(str(c.value)) for c in col if c.value is not None), default=8)
            w.column_dimensions[L(i)].width = min(max(10, ancho + 2), 60)
    import reglas
    wb.save(salida)                                     # v81cf8 (T6): no hidden sheet; the seal goes to a sidecar
    r = _recalcular(salida)
    reglas.sellar_sidecar(salida, out_reglas)
    return r


# ---- v68: Pending Items sin duplicados, sin cerrados, con delta vigente ----
CERRADO = re.compile(r"^(cerrad[oa]|closed|resuelt[oa]|resolved|answered)$", re.I)


def fmt_delta(delta, unidad=None):
    if isinstance(delta, dict):
        u = f" {unidad}" if unidad else ""
        return "; ".join(f"{str(k).replace('delta_', '')}: {v}{u}" for k, v in delta.items())
    if isinstance(delta, (int, float)):
        return f"{delta:g}{(' ' + unidad) if unidad else ''}"
    return delta


def _tema(x):
    return re.sub(r"[^a-z0-9]+", " ", en(str(x.get("pregunta") or "")).lower()).strip()


def opciones_rfi(x):
    """R80e.50 -> (texto A, texto B). Usa x["opciones"] {A: {texto, source, delta}, B: {texto, cita, delta}} si viene;
    si no, A sale de la pregunta / fuente / delta del RFI y B declara que no se citó código del trade."""
    op = x.get("opciones") or {}
    def txt(o, k):
        if isinstance(o, str):
            return o
        if isinstance(o, dict):
            return " | ".join(str(v) for v in (o.get("texto"), o.get(k), ("delta " + str(o["delta"])) if o.get("delta") else None) if v)
        return ""
    a = txt(op.get("A"), "source") or ("Plans / specs: " + " | ".join(str(v) for v in (x.get("source"),
                                       ("delta " + str(x["delta"])) if x.get("delta") not in (None, "") else None) if v)
                                       if (x.get("source") or x.get("delta") not in (None, "")) else
                                       "Plans / specs: nothing printed answers it (sheets searched in the question)")
    b = txt(op.get("B"), "cita") or "Trade code: no applicable code provision cited"
    return a, b


def rfis_vigentes(rfis):
    """Quita cerrados, ids repetidos y temas repetidos (gana el primero: fusionar pone primero los de las tools,
    que traen el delta del canon vigente)."""
    out, ids, temas = [], set(), []
    for x in rfis:
        if CERRADO.match(str(x.get("estado") or x.get("status") or "")):
            continue
        tid, tm = str(x.get("id")), _tema(x)
        if tid in ids or any(tm and (tm == t or (min(len(tm), len(t)) > 20 and (tm in t or t in tm)))
                             for t in temas):
            continue
        ids.add(tid); temas.append(tm); out.append(x)
    return out


# ---------------------------------------------------------------- v67: accesorios + partition types
OTHER_TYPE = "OTHER FRAMING (NOT A PARTITION)"
NO_METAL_CANON = ("alkali-resistant mesh tape (printed)", "sealer gasket (printed)", "setting-type joint compound at cement board (printed)")
# v81cf8 (T4, BE-CF17): canon families whose NET is a YIELD x driver (Inputs yields): no waste, like joint compound / tape
YIELD_CANON = ("alkali-resistant mesh tape (printed)", "setting-type joint compound at cement board (printed)")   # R80w.41: waste no metal
EXIST_TYPE = "BOARD ONLY - EXISTING OR WOOD-FRAMED WALLS (FRAMING NOT IN SCOPE)"   # R80w.39; v80wCF: también walls de madera (Div. 06) con nuestro board
BOARD_EN = {"5/8 type X": "5/8\" Type X", "5/8 regular": "5/8\" regular", "5/8 MR": "5/8\" MR", "5/8 type X WR": "5/8\" Type X W.R."}
UNIDAD_XL = {"lf": "LF", "sf": "SF", "pcs": "PCS", "lb": "LB"}
COMPRA = {   # familia -> selling unit cuando el nombre no tiene clase de compra (v68: stock en Inputs, sin cut_ft)
    "gypsum board jamb return": "sheet", "joint compound": "lb", "joint tape": "LF", "Level 5 finish": "SF"}
# renglones a mano que la fusión reemplaza (una familia de accesorios no se escribe dos veces)
REEMPLAZA = [r"^level 5", r"drywall screws", r"framing screws", r"slab pins", r"expansion anchors",
             r"joint compound", r"joint tape", r"jamb return", r"pvc trim", r"duct sleeves", r"power-driven",
             r"^access panel", r"additional head track", r"stud reinforcement", r"extra framing",
             r"coiling grille head"]
TYPES_VIEJOS = {"EXT", "PARAPET", "BULK", "BULKHEAD", "CANOPY", "CANOPY COL", "RS", "ROOF STEP", "TRANS", "VH",
                "VEST", "CSR", "BLKHD", "GRILLE"}


def _sources(fo, fam):
    xs = [en(str(r.get("source"))) for r in fo.get("filas") or [] if r.get("familia") == fam and r.get("source")]
    t = "; ".join(dict.fromkeys(xs))
    return t[:480] or "accesorios.py"   # CR-R12-E4: 240 cortaba la cita del spec a la mitad


def _unidad_familia(fo, fam):
    """Unidad de una familia del canon: accesorios.unidades, o la del calificador (familias.FAMILIAS)."""
    acc = (fo.get("accesorios") or {}).get("unidades") or {}
    if fam in acc:
        return acc[fam]
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import familias
    return next((u for f, u, *_ in familias.FAMILIAS if f == fam), (fo.get("unidades") or {}).get(fam))


_NUM = r"(\d+(?:\.\d+)?)"
_YIELD_RX = {   # familia -> regex sobre la operación de accesorios.py: (yield, driver)
    "drywall screws": re.compile(_NUM + r" x \(.*= " + _NUM + r" SF\)"),
    "joint compound": re.compile(_NUM + r" x \(.*= " + _NUM + r" SF\)"),
    "joint tape": re.compile(_NUM + r" x \(.*= " + _NUM + r" SF\)"),
    "framing screws": re.compile(_NUM + r" x (\d+) (?:piezas|stud pieces)"),
    "slab pins": re.compile(r"(?:sobre losa|on slab) " + _NUM + r" LF.*/ " + _NUM + r" ="),
    "expansion anchors": re.compile(r"(?:sobre losa|on slab) " + _NUM + r" LF.*/ " + _NUM + r" ="),
}
_DIV = ("slab pins", "expansion anchors")      # driver / yield (spacing); el resto yield x driver
_DRIVER_EN = {"drywall screws": "SF of board", "joint compound": "SF of board", "joint tape": "SF of board",
              "framing screws": "stud pieces", "slab pins": "LF of interior bottom track on slab",
              "expansion anchors": "LF of exterior bottom track on slab"}


def yield_de(fo, fam, valor):
    """(yield, driver) de una familia de yield, leído de su operación en familias_out.json; ValueError si la
    operación no reproduce el NET (una cita de yield sin aritmética no se acepta)."""
    y, drv = None, 0.0
    for r in fo.get("filas") or []:
        if r.get("familia") != fam:
            continue
        g = _YIELD_RX[fam].search(str(r.get("operacion", "")))
        if not g:
            continue
        a, b = float(g.group(1)), float(g.group(2))
        yy, dd = (b, a) if fam in _DIV else (a, b)
        if y is not None and abs(yy - y) > 1e-9:
            raise ValueError(f"{fam}: dos yields distintos ({y} y {yy})")
        y, drv = yy, drv + dd
    if y is None:
        return None
    calc = drv / y if fam in _DIV else y * drv
    if abs(calc - float(valor)) > max(0.6, 0.005 * abs(float(valor))):
        raise ValueError(f"{fam}: yield {y} con driver {drv} da {calc:.2f}, no {valor}")
    return y, round(drv, 2)


def desglose_frt(fo, fam="FRT plywood (SF)"):
    """{renglón por material y espesor: SF}. Usa fo['frt_plywood_by_material'] si viene (canon v68); si no, lo
    arma de las filas del canon de la familia, que deben sumar el total (±0.5 %)."""
    tot = float((fo.get("familias") or {}).get(fam, 0) or 0)
    if fo.get("frt_plywood_by_material"):
        out = {}
        for k, v in fo["frt_plywood_by_material"].items():
            e = plywood_err(k)
            if e:
                raise ValueError("; ".join(e))
            out[k] = out.get(k, 0.0) + float(v)
    else:
        out = {}
        for r in fo.get("filas") or []:
            if r.get("familia") != fam:
                continue
            v = r.get("valor")
            if v is None:
                g = re.search(r"=\s*" + _NUM + r"\s*SF", str(r.get("operacion", "")))
                v = float(g.group(1)) if g else None
            if v is None:
                raise ValueError(f"FRT plywood: fila sin SF '{r.get('ref')}'")
            k = clase_frt(" ".join(str(r.get(x) or "") for x in ("ref", "source", "operacion")))
            out[k] = out.get(k, 0.0) + float(v)
    if tot and abs(sum(out.values()) - tot) > max(0.5, 0.005 * tot):
        raise ValueError(f"FRT plywood: el desglose por material suma {sum(out.values()):.2f} SF y la familia "
                         f"{tot:.2f} SF (canon: frt_plywood_by_material o una fila por pieza con su SF)")
    return {k: round(v, 2) for k, v in out.items()}


SEAL_EXT = re.compile(r"base of gyp|exterior", re.I)
SEAL_EXT_NOMBRE = "Sealant at base of gypsum (exterior, not acoustical)"


SEAL_EXT_FAM = "sealant at base of gypsum (exterior)"
EXCLUIDAS_SIEMPRE = {"acoustical sealant": "EXCLUDED in all projects (estimator standing order): no "
                                           "acoustical sealant row and no quantity"}   # v77c U8 (R77.12)


def acoustical_err(materials):
    """v77c (U8, R77.12): un renglón de acoustical sealant (por nombre o por familia) = error: está EXCLUIDO en todos
    los proyectos. El sealant at base of gypsum (exterior, not acoustical) no es acoustical."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import familias
    err = []
    for m in materials:
        n = str(m.get("material") or m.get("name") or "")
        u = str(m.get("unit") or "").lower()
        if (re.search(r"(?<!not )acoustic", n, re.I) and re.search(r"sealant|caulk", n, re.I)) or \
                familias.familia(n, u) == "acoustical sealant":
            err.append(f"renglón '{n[:60]}': acoustical sealant EXCLUIDO en todos los proyectos (U8): sin renglón ni "
                       f"cantidad; va en Clarifications como exclusión")
    return err


def sealant_exterior(fo, fam=SEAL_EXT_FAM):
    if fo.get("sealant_exterior_lf") is not None:
        return float(fo["sealant_exterior_lf"])
    v = 0.0
    for r in fo.get("filas") or []:
        if r.get("familia") == fam and SEAL_EXT.search(f"{r.get('ref', '')} {r.get('wall', '')}"):
            x = r.get("valor")
            if x is None:
                g = re.match(r"\s*" + _NUM + r"\s*LF", str(r.get("operacion", "")))
                x = float(g.group(1)) if g else 0.0
            v += float(x)
    return round(v, 2)


def _slug(t):
    return re.sub(r"[^a-z0-9]+", "-", str(t).lower()).strip("-")[:24]


# v73 (R73.3, arbitraje #21): nombre de renglón de la PLANTILLA del estimador por familia (genérico: ningún dato de
# proyecto; {th} / {oc} salen del canon vía familias_out.nombres_contexto). Un renglón que cita su familia toma este
# nombre aunque la corrida haya escrito otro: el calificador y el estimador leen siempre el mismo renglón.
NOMBRES_PLANTILLA = {
    "6\" stud (todos los gauges)": "6\" metal stud (LF of material)",
    "10\" stud (todos los gauges)": "10\" metal stud (LF of material)",   # BE-GK06
    "3-5/8\" stud (todos los gauges)": "3-5/8\" metal stud (LF of material)",
    "1-5/8\" stud": "1-5/8\" metal stud (LF of material)",
    "1-1/2\" Z-furring": "1-1/2\" Z-furring channel (LF of material)",   # R80e.65
    "6\" parapet stud": "6\" parapet infill stud (LF of material)",
    "track de ceilings / soffits": "Ceiling / soffit track (size per source, see Where it comes from)",   # R80e.112
    "ceiling / soffit track 3-5/8\"": "Track 3-5/8\" ({gauge}) at soffits, fire stop at ceiling line and nested columns",   # v80p
    "ceiling / soffit track 6\"": "Track 6\" ({gauge}) at soffits, fire stop at ceiling line and nested beam",
    "ledger track 8\"": "8\" ledger track ({gauge}) (4/A-210)",
    "moment clip (types 3/4 base)": "Moment clip ClarkDietrich MC series with stiffening plate (A/A-410), one per stud of types 3 / 4",   # v80r
    "Kwik HUS-EZ anchors": "Hilti Kwik HUS-EZ 1/4\" x 1-5/8\" concrete screws at the moment clips (3/A-410, 4/A-410)",   # v80r
    "#10-16 screws at moment clips": "#10-16 screws at the moment clips, (1) at each flange (A/A-410)",   # v80r
    "metal corner guard 2x2x72": "Metal corner guard 2\"x2\"x72\" at outside corners (A-001A)",   # v80r
    "stainless corner guard 48": "Stainless steel corner guard 48\" A.F.F. (C22/A-101)",   # v80r
    "control joint": "Control joint, gypsum board walls and ceilings (ASTM C840: walls 30 ft max, ceilings 50 ft max)",   # v80r
    "#8 screws at brace ends": "#8 screws at diagonal brace ends, 2 per end (manufacturer rule; 3/A-410 prints none)",   # v80r
    "#8 screws, top chord / cross members (typ. connection)": "#8 screws at the top chord, cross members and track (8/A-410)",
    "bracing C.R. channel": "Bracing 1-1/2\" C.R. channel{oc}",
    "header / box beam": "Header / metal stud box beam",
    "sill track": "Sill track",
    "framed openings MEP": "Framed openings - MEP, light slots and diffusers",
    "purlin (track to deck)": "Purlin, top track to deck",
    "furring channel": "Furring channel (ceilings)",
    "carrying channel": "Carrying channel (ceilings)",
    "hanger wire": "Hanger wire",
    "5/8\" gyp board regular (walls + ceilings)": "5/8\" gypsum board, regular",
    "5/8\" gyp MOISTURE RESISTANT": "5/8\" gypsum board, MOISTURE RESISTANT",
    "5/8\" glass mat tile backer (Dens Shield)": "5/8\" glass mat water-resistant tile backer (DensShield, ASTM C1178)",   # BE-GK04
    "5/8\" gyp FOIL-BACKED": "5/8\" gypsum board, FOIL-BACKED",   # R80e.111
    "5/8\" gyp ceiling board SAG-RESISTANT": "5/8\" gypsum ceiling board, SAG-RESISTANT (ceiling type)",   # v81cf8 (T2)
    "setting-type joint compound at cement board (printed)": "Setting-type joint compound at cement board joints - printed product (see Where it comes from)",   # v81cf8 (T3)
    "1/2\" gyp MOISTURE RESISTANT": "1/2\" gypsum board, MOISTURE RESISTANT",   # R80e.111
    "5/8\" gyp board Type X": "5/8\" gypsum board, Type X",   # v80f R80e.18
    "5/8\" gyp board Type C": "5/8\" gypsum board, Type C (ceiling)",   # v81cf53
    "1\" gypsum shaftliner panel": "1\" gypsum shaftliner panel, Type X (C-H shaft wall)",   # v81cf53
    "5/8\" EXTERIOR gyp sheathing Type X": "5/8\" exterior gypsum sheathing, Type X",   # v81cf53
    "C-H stud 2-1/2\" (printed)": "C-H stud 2-1/2\" 20 GA (shaft wall) - printed (see Where it comes from)",
    "C-H stud 4\" (printed)": "C-H stud 4\" 20 GA (shaft wall) - printed (see Where it comes from)",
    "C-H stud 6\" (printed)": "C-H stud 6\" 20 GA (shaft wall) - printed (see Where it comes from)",
    "J-runner 2-1/2\" (printed)": "J-runner 2-1/2\" 20 GA (shaft wall top / bottom) - printed (see Where it comes from)",
    "J-runner 4\" (printed)": "J-runner 4\" 20 GA (shaft wall top / bottom) - printed (see Where it comes from)",
    "J-runner 6\" (printed)": "J-runner 6\" 20 GA (shaft wall top / bottom) - printed (see Where it comes from)",
    "8\" joist": "8\" metal joist (ceiling box)",   # v80f R80e.20
    "USG drywall main tee (DGLW26)": "USG drywall suspension main tee DGLW26",
    "USG drywall cross tee (DGLW424)": "USG drywall suspension cross tee DGLW424",
    "USG channel molding (DGCM27)": "USG channel molding DGCM27",
    "USG angle molding (DGWM24)": "USG angle molding DGWM24",
    "curved perimeter molding (printed)": "Curved perimeter molding - printed product (see Where it comes from)",   # R80w.35
    "track brace at strut splice (printed)": "Track brace at strut splice - printed product (see Where it comes from)",   # R80e.80
    "storefront structural framing (printed)": "Storefront structural framing (box beams, box posts, head boxes) - printed members (see Where it comes from)",   # R80e.100
    "demolition - gypsum board and metal framing": "Demolition - area of the element to demolish (SF = wall length x height / ceiling area, element area only)",   # R80e.116 / U-143
    "metal reveal trim (printed)": "Metal reveal trim - printed product (see Where it comes from)",   # R80e.107
    "sheet metal backing plate (printed)": "Sheet metal backing plate at door strike - printed product (see Where it comes from)",   # R80e.107
    "metal FRP trim (printed)": "Metal FRP top / edge trim - printed product (see Where it comes from)",   # R80e.107
    "EMT compression strut 1.5\" dia x 20 GA, ceiling lateral bracing (printed)": "EMT compression strut 1.5\" dia x 20 GA (drop up to 8'-6\"), ceiling lateral bracing - printed product K/A12.02 (see Where it comes from)",   # R80e.127
    "EMT compression strut 1.25\" dia x 20 GA, ceiling lateral bracing (printed)": "EMT compression strut 1.25\" dia x 20 GA (drop up to 7'-0\"), ceiling lateral bracing - printed product K/A12.02 (see Where it comes from)",   # R80e.127
    "W-4 panel trim and edge molding (printed)": "W-4 panel trim and edge molding - printed (see Where it comes from)",   # R80e.89
    "resilient channel (printed)": "Resilient channel - printed product (see Where it comes from)",   # R80e.78
    "1/4\" gypsum board (printed)": "1/4\" gypsum board - printed (see Where it comes from)",
    "flat strap bracing (printed)": "Diagonal flat strap bracing - printed (see Where it comes from)",
    "Z-furring runner track (printed)": "Z-furring runner track 1-1/2\" top and bottom (see Where it comes from)",
    "sanitary wall panels (printed)": "Sanitary wall panel system W-4 (see Where it comes from)",
    "concrete screw anchors, bottom track (printed)": "Concrete screw anchors at the bottom track - printed product (see Where it comes from)",   # R80e.75
    "#10 framing screws (printed)": "#10 framing screws - printed stud-to-track fastener (see Where it comes from)",
    "deep-leg slotted deflection track (printed)": "Deep-leg slotted deflection track - printed product (see Where it comes from)",
    "alkali-resistant mesh tape (printed)": "Alkali-resistant glass-fiber mesh tape at cement backer board joints - printed product (see Where it comes from)",   # R80w.41
    "sealer gasket (printed)": "Foam sealer gasket under structural base runners - printed product (see Where it comes from)",   # R80w.41
    "sheathing screws (printed)": "Sheathing screws - printed product and spacing (see Where it comes from)",
    "framing clips per stud (printed)": "Framing clips per stud - printed product (see Where it comes from)",
    "clip angle (bracing / nested connections)": "Clip angles and framing clips (see Where it comes from)",   # R80e.72: sin citas de otro proyecto   # v80n R80e.27
    "#8 pan head screws, relief channel to structure": "#8 pan head self-tapping screws, relief channel to structure (8/A-410)",   # v80o
    "Tek screws at clip angles": "#10-16 x 3/4\" Tek screws, pan head, at 16 ga clip angles and nested header / column / beam (5/A-410; 7/A-210; 8/A-210; A-410 note 8.A)",   # v80o
    "16 ga wire (seismic brace points)": "16 ga wire at seismic brace points (5/A-121)",
    "P.A.F. at cross members": "P.A.F. 3/16\" x 3/8\" at cross member ends (8/A-410)",
    "5/8\" cement board": "5/8\" cement board (tile base)",
    "plywood screws (Teks/3)": "Plywood screws #10-24 x 1-1/4\" Teks/3 (A-410 note 8.D)",
    "cement board screws": "Cement board screws 1-1/4\" (manufacturer spacing)",
    "nested inner runner (deflection head)": "Nested inner runner at the deflection head (detail per Where it comes from)",   # BE-CC02: no detail of another project in a row name
    "5/8\" gyp Type X W.R.": "5/8\" gypsum board, Type X W.R. (water resistant)",
    "5/8\" EXTERIOR gyp sheathing": "5/8\" EXTERIOR gypsum sheathing",
    "1/2\" EXTERIOR gyp sheathing": "1/2\" EXTERIOR gypsum sheathing",   # v80f R80e.16
    "5/8\" glass mat sheathing": "5/8\" glass mat sheathing (exterior face of the stud)",
    "ballistic panel": "Ballistic panel {th}UL752",
    "3/8\" gyp board": "3/8\" gypsum board",
    "1/2\" gyp board": "1/2\" gypsum board regular",   # v80wCF
    "FRP": "FRP panels",
    "metal stud brace to structure (printed)": "Metal stud brace to structure (size / gauge per the detail, see Where it comes from)",   # BE-HF12
    "spacing bar at the brace line (printed)": "Spacing bar at the brace line (printed product, see Where it comes from)",
    "cement board": "1/2\" cement board / cementitious backer",   # v80o (BE-46): el 5/8" va en su renglón
    "FRT blocking": "Blocking FRT / 2X FRT wood",
    "metal trim (corner bead, casing, shadow molding)": "METAL trim - corner bead, casing bead, shadow molding, "
                                                        "gypsum edge trim",
    SEAL_EXT_FAM: SEAL_EXT_NOMBRE,                    # v77c U8: el acoustical sealant está EXCLUIDO (sin renglón)
}
WOOD_NOMBRE = "Blocking 2X wood (not labeled FRT)"
def _blk_nombre(k):
    """BE-GK36: 'edge <designation>' -> 'Stud blocking at edge of gypboard (structural detail) - <designation>' (U-177 (3))."""
    if str(k).startswith("edge ") and k != "edge":
        return BLK_NOMBRES["edge"] + " - " + k[5:]
    return BLK_NOMBRES.get(k, k)


BLK_NOMBRES = {"edge": "Stud blocking at edge of gypboard (structural detail)",
               "items": "Blocking / backing at wall-mounted items (notes)"}   # U-177 (4): no "metal stud" si lo impreso es strap / track


def nombre_plantilla(fam, fo):
    pn = (fo.get("nombres_familia") or {}).get(fam)   # R80w.24: producto impreso en el set (canon.product_names)
    if pn:
        return pn
    n = NOMBRES_PLANTILLA.get(fam)
    if not n:
        return None
    c = fo.get("nombres_contexto") or {}
    zs = str(c.get("z_size") or "").strip()
    zk = str(c.get("z_kind") or "").strip()
    if fam == "1-1/2\" Z-furring" and zk == "hat channel":   # BE-HF1: printed product (vertical metal hat channel)
        return f"{zs or '1-1/2\"'} metal hat channel, vertical furring (LF of material)"
    if fam == "1-1/2\" Z-furring" and zk == "Z-furring / hat channel":
        return f"{zs or '1-1/2\"'} Z-furring / metal hat channel, vertical furring (LF of material)"
    if fam == "1-1/2\" Z-furring" and zs and zs != "1-1/2\"":   # v81cf8 (T1): printed Z size in the label
        return f"{zs} Z-furring channel (LF of material)"
    th = str(c.get("ballistic_th") or "")
    oc = c.get("bracing_oc_in")
    gq = ((fo.get("family_splits") or {}).get(fam) or {}).get("gauge") or "gauge per source"   # v80q (R80e.32)
    return n.format(th=(th + " ") if th else "", oc=f" @ {oc:g}\" O.C." if isinstance(oc, (int, float)) else "", gauge=gq)


# familias del canon que tienen su propio armado en fusionar (track por elemento, FRT por material, sealant aparte)
CUBIERTAS_APARTE = ("bottom track (todos)", "top / deflection track (todos)", "FRT plywood (SF)", SEAL_EXT_FAM)


def familias_faltantes(mats, fo, fam_canon, acc, familias):
    """v80 (R80.4): renglones para las familias del canon (NET > 0) que ningún renglón de la corrida cubre, con el
    nombre de la plantilla y la cita de familias_out.json. El blocking de metal sale por origen (edge / items)."""
    cubiertas = set()
    for m in mats:
        f = m.get("familia") or familias.familia(str(m["material"]), str(m["unit"]).lower())
        if f:
            cubiertas.add(f)
        g = re.search(r"familias_out\.json[^']*'([^']+)'", str(m.get("source", "")))
        if g:
            cubiertas.add(g.group(1))
    out = []
    for fam, v in fam_canon.items():
        if fam in cubiertas or fam in (acc.get("familias") or {}) or fam in CUBIERTAS_APARTE:
            continue
        try:
            v = float(v or 0)
        except (TypeError, ValueError):
            continue
        if v <= 1e-9 and not any(r.get("familia") == fam and str(r.get("operacion") or "").startswith("EXCLUDED")
                                 for r in fo.get("filas") or []):
            continue                    # R80w.37 / R80w.38: una familia EXCLUIDA por el estimador sale en 0 con su nota
        uf = str(_unidad_familia(fo, fam) or "lf").upper()
        # v80f (R80e.16): una familia en SF que cae aquí es board / sheathing (waste de board, hoja de Inputs), no metal
        base = {"unit": "PCS" if uf in ("PCS", "EA") else uf, "metal": uf != "SF" and fam not in NO_METAL_CANON, "familia": fam,
                "selling_unit": "4x12 ft sheet (Inputs)" if uf == "SF" else "piece", "source": f"familias_out.json '{fam}' (R80.4: canon family the run did not write)"}
        if fam in YIELD_CANON:                    # v81cf8 (T4): yield rows carry no waste (Inputs C23 / C24)
            base.update({"waste": "none", "waste_pct": 0.0, "metal": False,
                         "selling_unit": "roll (LF)" if uf == "LF" else ("lb (bag / pail)" if uf == "LB" else base["selling_unit"])})
        if fam.startswith("demolition"):          # R80e.116: demolición = trabajo, no compra: SF sin waste
            base.update({"selling_unit": "SF (work, no purchase)", "waste": "none", "waste_pct": 0.0, "metal": False})
        if fam == "metal stud blocking (362CR / STUD BLOCKING)" and fo.get("metal_blocking_by_origin"):
            for k, x in fo["metal_blocking_by_origin"].items():
                if float(x or 0) > 0:
                    out.append(dict(base, material=_blk_nombre(k), net=float(x),
                                    source=f"familias_out.json metal_blocking_by_origin '{fam}' ({k}) (R80.4)"))
            continue
        out.append(dict(base, material=nombre_plantilla(fam, fo) or fam, net=v))
    return out


def etiqueta_elemento(o):
    """R80w.32: rótulo de un elemento de OTHER FRAMING en inglés llano ('Soffit side (16/A502)'), nunca la clave del
    esquema ('soffit_side')."""
    el = str(o.get("element") or "other framing").replace("_", " ").strip()
    el = el[:1].upper() + el[1:]
    m = NHOJA_REV.search(str(o.get("source") or o.get("detail") or ""))
    return f"{el} ({m.group(0)})" if m else el


def fusionar(d, fo):
    """v72b: deja en el takeoff la huella de `fo` (_familias_sha); armar la compara con la carpeta de trabajo.
    Material Summary de accesorios + RFIs + exclusiones + Partition Takeoff desde familias_out.json (v67) y,
    v68: un renglón por material / espesor de FRT plywood, sealant exterior aparte, yields con su celda de Inputs
    y fórmula viva, NET de familia solo en su misma unidad, hanger wire en PCS + LF, RFIs sin duplicados."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import familias
    acc = fo.get("accesorios")
    if not acc:
        raise ValueError("familias_out.json sin 'accesorios' (correr canon.py v67)")
    pend = [f for f, e in acc["estado"].items() if e == "PENDIENTE"]
    if pend:
        raise ValueError(f"familias de accesorios PENDIENTE {pend}: resolver desde el plano (E23) o "
                         f"accesorios_rfi con delta en el canon; nunca se omiten")
    d = dict(d)
    d["inputs"] = dict(d.get("inputs") or {})
    fam_canon = fo.get("familias") or {}
    mats = []
    # v72 (R71.8b, arbitraje #20): una familia citada por >= 2 renglones de su misma unidad está REPARTIDA (track por
    # tamaño): el NET de cada renglón se respeta y la suma tiene que dar la familia (± 0.1); nunca se le pone el total
    # de la familia a cada renglón (antes: 8 renglones x total = track x 8).
    def _fam_de(m):
        return m.get("familia") or (lambda g: g.group(1) if g else None)(
            re.search(r"familias_out\.json[^']*'([^']+)'", str(m.get("source", ""))))
    # v73 (R73.3, arbitraje #21): el track sale con los renglones de la PLANTILLA del estimador (por elemento: parapet,
    # roof step / heads; el resto por tamaño de stud) que da canon.py en track_by_element. Los renglones de track
    # que haya escrito la corrida se reemplazan: el nombre del renglón no depende de la lectura.
    tpe = fo.get("track_by_element") or {}
    if tpe.get("bottom") or tpe.get("top"):
        fams_t = {"bottom": "bottom track (todos)", "top": "top / deflection track (todos)"}
        d = dict(d, materials=[m for m in d["materials"] if _fam_de(m) not in fams_t.values()])
        for k, fam_t in fams_t.items():
            for nombre, v in (tpe.get(k) or {}).items():
                d["materials"].append({"material": nombre, "unit": "LF", "net": float(v), "metal": True,
                                       "selling_unit": "run 10 ft", "stock": 10,
                                       "source": f"familias_out.json track_by_element '{fam_t}' (R73.3)"})
    cuenta = Counter((_fam_de(m), str(m["unit"]).lower()) for m in d["materials"] if _fam_de(m) in fam_canon)
    repartidas = {}
    for m in d["materials"]:
        n = str(m["material"]).lower()
        if any(re.search(rx, n) for rx in REEMPLAZA):
            continue
        if n.startswith("2-1/2\"") and not float(fam_canon.get("2-1/2\" stud", 0) or 0):
            continue                                       # el 2-1/2" del grille lo da accesorios
        fam = _fam_de(m)
        if fam in fam_canon and fam not in acc["familias"] and cuenta[(fam, str(m["unit"]).lower())] > 1:
            repartidas.setdefault(fam, []).append(m)             # v72 R71.8b: renglón parcial, NET propio
            mats.append(m)
            continue
        if fam in fam_canon and fam not in acc["familias"] and nombre_plantilla(fam, fo):
            m = dict(m, material=nombre_plantilla(fam, fo))       # v73 (R73.3): nombre de la plantilla
        if fam == "metal stud blocking (362CR / STUD BLOCKING)" and fo.get("metal_blocking_by_origin") and \
                cuenta[(fam, str(m["unit"]).lower())] == 1:
            for k, v in fo["metal_blocking_by_origin"].items():  # v73: edge del detalle y notas, renglones aparte
                mats.append(dict(m, material=_blk_nombre(k), net=float(v),
                                 source=f"familias_out.json metal_blocking_by_origin '{fam}' ({k})"))
            continue
        if fam in fam_canon and fam not in acc["familias"]:     # v67: el NET sale del canon vigente
            uf = _unidad_familia(fo, fam)
            if uf and uf.lower() != str(m["unit"]).lower():   # v68 (#16A hanger wire): NET en SU unidad
                raise ValueError(f"renglón '{m['material']}' en {m['unit']} cita la familia '{fam}' que va en "
                                 f"{uf.upper()}: el NET de una familia solo va en un renglón de su misma unidad")
            m = dict(m, net=float(fam_canon[fam]))
        mats.append(m)
    for fam, ms in repartidas.items():
        if fam == "FRT plywood (SF)" and fo.get("frt_plywood_by_material"):
            continue      # v77: sus renglones se rehacen abajo desde frt_plywood_by_material (por material y uso)
        tot = sum(float(x.get("net") or 0) for x in ms)
        if abs(tot - float(fam_canon[fam])) > 0.1:
            raise ValueError(f"familia '{fam}' repartida en {len(ms)} renglones suma {round(tot, 2)} != familia "
                             f"{fam_canon[fam]} (R71.8b: los renglones por tamaño suman la familia)")
    # v80 (R80.4): TODA familia del canon con NET > 0 tiene renglón en Material Summary. Antes una familia sin renglón
    # en takeoff.json desaparecía del Excel sin aviso (blocking de metal: el canon la traía y el libro no).
    mats += familias_faltantes(mats, fo, fam_canon, acc, familias)
    # v76 (arbitraje #24): stud por elemento (framed soffit) en su renglón de la plantilla, dentro de su familia: el
    # renglón general baja lo mismo (Σ = familia)
    for fam, dd in (fo.get("stud_by_element") or {}).items():
        tot_e = sum(float(v) for v in dd.values())
        if tot_e <= 0:
            continue
        base = [i for i, m in enumerate(mats) if _fam_de(m) == fam and str(m["unit"]).lower() == "lf"
                or m["material"] == nombre_plantilla(fam, fo)]
        if len(base) != 1:
            raise ValueError(f"stud_by_element '{fam}': {len(base)} renglones base de la familia (se espera 1)")
        mb = mats[base[0]]
        mats[base[0]] = dict(mb, net=round(float(mb["net"]) - tot_e, 2))
        for n, v in dd.items():
            mats.append(dict(mb, material=n, net=float(v), familia=fam,
                             source=f"familias_out.json stud_by_element '{fam}' (v76)"))
    # v76: blocking de madera 2X sin rótulo FRT en su renglón, dentro de la familia de madera (Σ = familia)
    wl = float(fo.get("wood_blocking_lf") or 0)
    if wl > 0:
        bi = [i for i, m in enumerate(mats) if _fam_de(m) == "FRT blocking" or m["material"] ==
              nombre_plantilla("FRT blocking", fo)]
        if len(bi) != 1:
            raise ValueError(f"wood_blocking_lf: {len(bi)} renglones de 'FRT blocking' (se espera 1)")
        mb = mats[bi[0]]
        mats[bi[0]] = dict(mb, net=round(float(mb["net"]) - wl, 2))
        mats.append(dict(mb, material=WOOD_NOMBRE, net=wl, familia="FRT blocking",
                         source="familias_out.json wood_blocking_lf 'FRT blocking' (v76)"))
    # v68: FRT plywood, un renglón por material y espesor
    FRT = "FRT plywood (SF)"
    frt_rows = [m for m in mats if familias.familia(m["material"], str(m["unit"]).lower()) == FRT]
    if float(fam_canon.get(FRT, 0) or 0) > 0 or fo.get("frt_plywood_by_material"):
        des = desglose_frt(fo)
        cit = "; ".join(dict.fromkeys(c for m in frt_rows for c in re.findall(r"\b[0-9A-Z]{1,2}/[A-Z]{1,2}\d+\.\d+",
                                                                              str(m.get("source", "")))))
        mats = [m for m in mats if m not in frt_rows]
        exc = fo.get("frt_plywood_excluded") or {}
        for k, v in des.items():
            mats.append({"material": k, "unit": "SF", "net": v, "metal": False, "selling_unit": "sheet",
                         "source": (f"{exc[k]}; {cit or 'canon rows'}" if k in exc and not v else
                                    f"familias_out.json FRT plywood by material; {cit or 'canon rows'}")})
    # v68: sealant exterior (base of gypsum) en su propio renglón; v77c (U8): el acoustical sealant está EXCLUIDO
    ext = sealant_exterior(fo)
    if ext > 0 and not any(familias.familia(m["material"], str(m["unit"]).lower()) == SEAL_EXT_FAM for m in mats):
        mats.append({"material": SEAL_EXT_NOMBRE, "unit": "LF", "net": ext, "metal": False,
                     "source": "familias_out.json sealant_exterior_lf 'base of gypsum (exterior)'"})
    # v68: hanger wire en PCS además del LF
    hp = (fo.get("hanger_pcs") or {}).get("total_pcs")
    if hp and not any("hanger" in str(m["material"]).lower() and str(m["unit"]).upper() in ("PCS", "EA")
                      for m in mats):
        mats.append({"material": "Hanger wire - hanger count (one per hanger, height per room)",
                     "unit": "PCS", "net": float(hp), "metal": True, "waste": "none", "selling_unit": "each",
                     "source": "familias_out.json hanger_pcs.total_pcs; wire bought on the LF row"})
    for f, v in acc["familias"].items():
        sel = COMPRA.get(f, "each")
        w = acc["waste"].get(f)
        m = {"material": acc["nombres_excel"][f], "unit": UNIDAD_XL[acc["unidades"][f]], "net": float(v),
             "metal": w == "metal", "selling_unit": sel,
             "source": f"accesorios.py [{ESTADO_EN.get(acc['estado'][f], acc['estado'][f])}]: {_sources(fo, f)}"}
        if w is None:
            m["waste"] = "none"
        if f in YIELDS:
            yd = yield_de(fo, f, v)
            if yd is None and abs(float(v)) > 1e-9:
                raise ValueError(f"{f}: NET {v} sin operación 'yield x driver' en familias_out.json (yield no trazable)")
            if yd is None:
                m["yield_formula"] = f"=0*{CELDA[YIELDS[f]]}"
            else:
                y, drv = yd
                k = YIELDS[f]
                d["inputs"][k] = y
                cel = CELDA[k]
                lab = next(x[2] for x in INPUTS_V68 if x[1] == k)
                if f in _DIV:
                    m["yield_formula"] = f"={drv:g}/{cel}"
                    m["source"] = f"{drv:g} {_DRIVER_EN[f]} / {cel.replace('$', '')} ({lab} = {y:g})"
                else:
                    m["yield_formula"] = f"={cel}*{drv:g}"
                    m["source"] = f"{cel.replace('$', '')} ({lab} = {y:g}) x {drv:g} {_DRIVER_EN[f]}"
                m["source"] = f"accesorios.py [{ESTADO_EN.get(acc['estado'][f], acc['estado'][f])}]: " + m["source"]
                _cc_ = re.search(r"(?:Level 1 on )?[\d,.]+ SF concealed layers[^|]*?x 2/3[^|;]*", _sources(fo, f) or "")   # R80e.165: compound por capa
                if _cc_:
                    m["source"] += " | " + _cc_.group(0).strip()
        mats.append(m)
    # rev15 (CR City Hotel revisión completa rev14 F08): piezas mínimas de compra por familia (studs cortados a largo > stock / 2 = un
    # stick por stud; el sobrante no sirve). d["piezas_min"] = {familia: {"n": piezas, "op": operación}} -> Pieces = MAX(LF/stock, n)
    pm = d.get("piezas_min") or {}
    for m in mats:
        f_ = _fam_de(m)
        if f_ in pm:
            m["piezas_min"] = int(pm[f_]["n"]); m["piezas_min_op"] = str(pm[f_]["op"])
    d["materials"] = mats
    # RFIs: primero los de las tools (delta del canon vigente), después los del agente; rfis_vigentes deduplica
    rfis, cuenta = [], {}
    for r in fo.get("rfis_accesorios") or []:
        delta = r.get("delta", {k: v for k, v in r.items() if k.startswith("delta")})
        s = _slug(r["familia"]); cuenta[s] = cuenta.get(s, 0) + 1
        rfis.append({"id": f"RFI-ACC-{s}" + (f"-{cuenta[s]}" if cuenta[s] > 1 else ""),
                     "pregunta": en(f"{r['familia']}: {r.get('tema', '')}"),
                     "delta": fmt_delta(delta, r.get("unidad"))})
    d["rfis"] = rfis_vigentes(rfis + [x for x in d["rfis"] if not str(x.get("id", "")).startswith("RFI-ACC")])
    # v80r (R80e.35): RFI decididos por el estimador -> el renglón queda "CLOSED - estimator decision" con su delta
    # R80e.96: Pending Items = SOLO lo abierto. Un RFI decidido por el estimador (rfi_cierre) no vuelve a Pending Items:
    # queda en el Scope Checklist como "CLOSED" con la decisión y su delta aplicado. Un RFI que sigue en d["rfis"]
    # (abierto en esta corrida, p. ej. una parte que la decisión dejó pendiente) se queda abierto con su texto.
    cz = d.get("rfi_cierre") or {}
    abiertos = {x.get("id") for x in d["rfis"]}
    cerrados = [{"id": k, "nombre": v["pregunta"], "estado": "CLOSED", "nota": f"decision applied: {v['delta']}"}
                for k, v in sorted(cz.items(), key=lambda kv: _nat(kv[0])) if k not in abiertos]
    d["alcances"] = list(d.get("alcances") or []) + cerrados
    d["revisar"] = ordenar_revisar(d.get("revisar") or [])     # v77c U9 / U10
    alc = list(d["alcances"])
    for k, why in EXCLUIDAS_SIEMPRE.items():              # v77c U8: la exclusión manda sobre lo que escribió la corrida
        alc = [dict(a, estado="NO APLICA", nota=f"EXCLUDED: {why}") if k.lower() in str(a.get("nombre", "")).lower()
               else a for a in alc]
    for k, why in list((fo.get("excluidas") or {}).items()) + list(EXCLUIDAS_SIEMPRE.items()):
        if not any(k.lower() in str(a.get("nombre", "")).lower() for a in alc):
            alc.append({"id": f"ALC-X{len(alc) + 1}", "nombre": k, "estado": "NO APLICA", "nota": en(why)})
    d["alcances"] = alc
    pt = fo.get("partition_types")
    if pt:
        def row(t, f):
            return {"type": t, "wall": f["wall"], "location": f["location"], "length_lf": f["lf"],
                    "height_ft": f["height_ft"], "stud_size": f["stud_size"], "stud_oc_in": f["oc_in"],
                    "layers": f["layers"], "board_sf": f["board_sf"], "source": f["source"], "status": f["status"]}
        d["walls"] = [row(t, f) for t, x in pt["types"].items() for f in x["filas"]]
        d["other_framing"] = [row(etiqueta_elemento(o), dict(o, wall=o["id"])) for o in pt.get("other_framing") or []]
    if fo.get("existing_walls"):                          # R80w.39: muros existentes, solo board
        d["existing_walls"] = list(fo["existing_walls"])
    d["_familias_sha"] = sha_familias(fo)
    return d


INPUTS_CITA = re.compile(r"Inputs!?\s*\$?([A-Z])\$?(\d+)")
YIELD_NOMBRES = {"drywall screws": r"^drywall screws", "framing screws": r"^framing screws",
                 "joint compound": r"^joint compound", "joint tape": r"^joint tape",
                 "slab pins": r"slab pins", "expansion anchors": r"^expansion anchors"}


CITA_TOOL = re.compile(r"\b([A-Za-z0-9_]+_out\.json)([^;]*)")


def _norm_fam(t):
    return re.sub(r"[^a-z0-9]+", "", str(en(str(t))).lower())


def _valores_tool(j):
    """(nombre, valor) de todas las familias / totales numéricos que da la salida de una tool."""
    if not isinstance(j, dict):
        return
    fuentes = [j.get("familias"), j.get("totales_lf"), j.get("totales_sf"), j.get("frt_plywood_by_material"),
               (j.get("accesorios") or {}).get("familias") if isinstance(j.get("accesorios"), dict) else None]
    for d in fuentes:
        if isinstance(d, dict):
            for k, v in d.items():
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    yield k, float(v)


R708 = {"drywall screws": r"^drywall screws", "joint compound": r"^joint compound", "joint tape": r"^joint tape"}
RX_YF = re.compile(r"^=\s*(?:Inputs!\$?([A-Z]+)\$?(\d+)\s*([*/])\s*([\d.]+)|([\d.]+)\s*([*/])\s*Inputs!\$?([A-Z]+)\$?(\d+))\s*$")


def verificar_r708(wf, wv=None):
    """R70.8 (v70): el NET de drywall screws / joint compound / joint tape sale del yield de Inputs: fórmula viva que
    cita la celda de Inputs, o igual a yield (celda de Inputs citada en Yield check) x driver dentro de 0.5 %."""
    err = []
    if "Material Summary" not in wf.sheetnames or "Inputs" not in wf.sheetnames:
        return err
    ms, inp = wf["Material Summary"], wf["Inputs"]
    hdr = [str(c.value or "").strip().lower() for c in ms[3]]
    jy = hdr.index("yield check (live formula)") if "yield check (live formula)" in hdr else 9
    for row in ms.iter_rows(min_row=4):
        name = str(row[0].value or "")
        if not any(re.search(rx, name, re.I) for rx in R708.values()):
            continue
        net = row[2].value
        if isinstance(net, str) and net.startswith("=") and "Inputs!" in net:
            continue
        m = RX_YF.match(str(row[jy].value or "")) if len(row) > jy else None
        esperado = None
        if m and isinstance(net, (int, float)):
            col, fila, op, num = (m.group(1), m.group(2), m.group(3), m.group(4)) if m.group(1) else \
                (m.group(7), m.group(8), m.group(6), m.group(5))
            y = inp[f"{col}{fila}"].value
            if isinstance(y, (int, float)) and y:
                n = float(num)
                if m.group(1):
                    esperado = y * n if op == "*" else y / n
                else:
                    esperado = n * y if op == "*" else n / y
        if esperado is None or abs(float(net) - esperado) > 0.005 * abs(esperado):
            err.append(f"Material Summary '{name[:40]}': R70.8 yield must come from Inputs (NET {net} sin fórmula viva "
                       f"a Inputs y distinto de yield de Inputs x driver" + (f" = {round(esperado, 2)})" if esperado
                                                                               is not None else ")"))
    return err


def verificar_salidas(wb, carpetas):
    """v70: renglón del Material Summary con Net 0 que cita '<tool>_out.json ... <familia>' cuando esa salida da
    > 0 para la familia -> error. -> lista de errores."""
    err, cache = [], {}

    def cargar(nombre):
        if nombre not in cache:
            cache[nombre] = None
            for c in carpetas:
                p = os.path.join(c, nombre)
                if os.path.isfile(p):
                    try:
                        cache[nombre] = json.load(open(p, encoding="utf-8"))
                    except ValueError:
                        err.append(f"{p}: JSON inválido")
                    break
        return cache[nombre]
    if "Material Summary" not in wb.sheetnames:
        return err
    for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True):
        if not r or not r[0] or len(r) < 9:
            continue
        net = r[2]
        if not isinstance(net, (int, float)) or isinstance(net, bool) or abs(net) > 1e-9:
            continue
        for nombre, resto in CITA_TOOL.findall(str(r[8] or "")):
            j = cargar(nombre)
            if j is None:
                continue
            citadas = [_norm_fam(x) for x in re.findall(r"'([^']+)'", resto)]
            for k, v in _valores_tool(j):
                if v > 1e-9 and _norm_fam(k) in citadas:
                    err.append(f"Material Summary '{str(r[0])[:50]}': Net 0 pero {nombre} da {round(v, 2)} para "
                               f"'{k}' (¿se leyó la clave equivocada de la salida? v70)")
    return err


# R80f.43 (Chuze FINAL7, auditoría U-138, BE-141): las cifras de material que van en los textos del Excel (Scope Checklist,
# notas de Inputs, Review Items, Pending Items) se escriben POR PROGRAMA al armar: {{MS:<inicio del renglón del Material
# Summary>}} = suma del Net de los renglones que empiezan así; {{EX:board_sf}} = suma Board (SF) de las existing walls.
# Nunca una cifra tecleada que queda vieja después de un recálculo (ALC-07 / ALC-08 de Chuze FINAL7).
RX_CIFRA_PH = re.compile(r"\{\{(MS|EX):([^}]*)\}\}")


def resolver_cifras(t, d):
    if not isinstance(t, str) or "{{" not in t:
        return t

    def rep(m):
        k, a = m.group(1), m.group(2)
        if k == "EX":
            return f"{sum(float(e.get('board_sf') or 0) for e in d.get('existing_walls') or []):,.2f}"
        eq = a.startswith("=")
        a = a.lstrip("=")
        vs = [float(x.get("net") or 0) for x in d.get("materials") or []
              if any((n == a) if eq else n.startswith(a) for n in (str(x.get("material", "")), en(str(x.get("material", "")))))]
        if not vs:
            raise ValueError("cifra {{MS:" + a + "}}: ningún renglón del Material Summary empieza así (R80f.43)")
        return f"{sum(vs):,.2f}"
    return RX_CIFRA_PH.sub(rep, t)


def verificar_cifras(wb):
    """R80f.43 / BE-141: cifra de material escrita en Scope Checklist / Inputs distinta de su renglón = error."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import chequeos_biblioteca as CB
    ms = [(str(r[0]), r[2]) for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True)
          if r and r[0] and isinstance(r[2], (int, float))]
    ex = [r[7] for r in wb["Partition Takeoff"].iter_rows(min_row=5, values_only=True)
          if r and len(r) > 7 and str(r[1] or "").startswith("EX-") and isinstance(r[7], (int, float))]
    tx = [(f"{h}!{c.coordinate}", c.value) for h in (HOJA_ALCANCES, "Inputs") if h in wb.sheetnames
          for row in wb[h].iter_rows() for c in row if isinstance(c.value, str)]
    return CB.cifras_texto_err(tx, ms, sum(ex) if ex else None)


def verificar_excel(xlsx, salidas=None):
    """Lo que bitacora.py compuerta exige del Excel final (v67 + v68: compra, Inputs, idioma, Pending Items).
    v70: + renglones en 0 contra la salida de la tool que citan
                                                         + R70.8 (yields de drywall screws / compound / tape) (junto al Excel y en `salidas`)."""
    import openpyxl
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import accesorios
    err = []
    try:
        wb = openpyxl.load_workbook(xlsx, data_only=True)
        wf = openpyxl.load_workbook(xlsx)
    except Exception as e:                              # noqa: BLE001
        return [f"Excel ilegible: {e}"]
    if "Material Summary" not in wb.sheetnames or "Partition Takeoff" not in wb.sheetnames:
        return ["faltan las hojas Material Summary / Partition Takeoff"]
    nombres = [str(r[0] or "") for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True)]
    ren = {}                                            # R80w.46: renglón renombrado por el canon (acc_nombres) -> su nombre
    for d_ in [os.path.dirname(os.path.abspath(xlsx))] + [str(x) for x in (salidas or [])]:
        pf = os.path.join(d_, "familias_out.json")
        if os.path.isfile(pf):
            try:
                ren = (json.load(open(pf, encoding="utf-8")).get("accesorios") or {}).get("nombres_excel") or {}
            except Exception:                           # noqa: BLE001
                ren = {}
            break
    for r_ in wb["Material Summary"].iter_rows(min_row=4, values_only=True):   # R80w.48: toda fila cita su hoja
        if r_ and r_[0] and len(r_) > 8 and "N/SHEET: default (no sheet)" in str(r_[8] or ""):
            err.append(f"Material Summary '{str(r_[0])[:60]}': N/SHEET: default (no sheet) - la fila debe citar la hoja / "
                       f"spec de donde sale (la hoja va en la fuente del ítem, no solo en el texto)")
    for f, n in accesorios.NOMBRES_EXCEL.items():
        pref = n.split("{")[0].strip()
        if f in ren and "{" not in n and ren[f] != n:
            pref = str(ren[f]).split("{")[0].strip()
        if not any(x.startswith(pref) for x in nombres):
            err.append(f"Material Summary sin la familia de accesorios '{f}' (renglón '{pref}...')")
    ws = wb["Partition Takeoff"]
    tipos, cur = [], None
    for r in ws.iter_rows(min_row=5, values_only=True):
        a = str(r[0] or "").strip()
        if a.upper().startswith("TOTAL"):
            err.append("Partition Takeoff: renglón TOTAL con texto en la columna A (va en la B; R6)")
        if a.startswith("TYPE "):
            cur = a[5:].strip()
            tipos.append(cur)
            if cur.upper() in TYPES_VIEJOS or re.match(r"^\d+/[A-Z]", cur):
                err.append(f"Partition Takeoff: type '{cur}' fuera de la convención (EXT-6CFMF, EXT-PARAPET, "
                           f"BULKHEAD-<tag>, CANOPY-COL, OTHER FRAMING)")
        elif a and cur is None and r[2] is not None:
            err.append(f"Partition Takeoff: renglón '{a[:40]}' fuera de un bloque TYPE")
        if any(re.search(r"\bPENDI(?:ENTE|NG)\b", str(c or "")) for c in r):     # v68 (C-P5): type PENDIENTE no se arma
            err.append(f"Partition Takeoff: renglón '{a[:40] or str(r[1] or '')[:40]}' PENDING (partition_types sin "
                       f"dato obligatorio: se resuelve en el canon antes de entregar)")
    if not tipos:
        err.append("Partition Takeoff sin bloques 'TYPE <nombre>'")
    err += verificar_v77c(wb)
    err += verificar_texto_cliente(wb)                 # R80e.84
    err += verificar_cifras(wb)                        # R80f.43 / BE-141
    err += verificar_v68(wb, wf)
    carpetas = [os.path.dirname(os.path.abspath(xlsx))] + [str(x) for x in (salidas or [])]
    err += verificar_salidas(wb, carpetas)
    err += verificar_r708(wf)
    err += verificar_r71_track(wb, _track_familia(carpetas))
    return err


def cobertura_err(wb, fo):
    """v80 (R80.4): cada familia de familias_out.json con NET > 0 tiene al menos un renglón en Material Summary
    (mismo mapeo de nombres que el calificador, familias.familia). Devuelve la lista de faltantes."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import familias
    if "Material Summary" not in wb.sheetnames:
        return ["sin hoja Material Summary"]
    vistas = set()
    for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True):
        if r and r[0] and len(r) > 2 and isinstance(r[2], (int, float)):
            f = familias.familia(str(r[0]), str(r[1] or "").lower())
            if f:
                vistas.add(f)
    excl = set((fo.get("excluidas") or {}).keys()) | {k for k in EXCLUIDAS_SIEMPRE}
    err = []
    for fam, v in (fo.get("familias") or {}).items():
        try:
            v = float(v or 0)
        except (TypeError, ValueError):
            continue
        if v <= 1e-9 or fam in vistas or any(k.lower() in fam.lower() for k in excl):
            continue
        if not any(f == fam for f, *_ in familias.FAMILIAS):
            continue                                   # familia interna del canon, sin renglón propio en la plantilla
        err.append(f"familia '{fam}' = {round(v, 2)} en familias_out.json sin renglón en Material Summary (R80.4)")
    return err


# R80e.84 (BE-41 / BE-55 / BE-106 / R80e.29 d): el texto de las hojas visibles es del CLIENTE: sin nombres de archivos
# internos ni rutas de imágenes, sin dicts crudos, sin códigos de proceso (revN, pass N, reglas R7x.y / R80e.n, BE-n),
# sin "canon" ni "the other pass", sin hojas de otro proyecto (A-121), sin "estimator criterion" sin fuente.
TEXTO_INTERNO = re.compile(r"[\w.-]+\.(?:md|json|py|png|jpg)\b|\bimg_[a-z0-9_]+/|\{'[a-z_]+':|\brev\d+[a-z]?\b|"
                           r"\bpass \d\b|\bother pass\b|\bR[78]\d\.\d{1,2}b?\b|\bR80e\.\d+\b|\bBE-\d+\b|\bcanon\b|"
                           r"resolution A vs B|directed review|\bA-121\b|estimator criterion(?! \()", re.I)


RX_IMG_REVISAR = re.compile(r"[\w.\-]+\.(?:png|jpe?g)", re.I)
# v81cf28 (U-118 / BE-CF21): la evidencia circulada ENTREGADA (carpeta proceso/review_img o proceso/rfi_img del entregable)
# sí se nombra en la columna Image de Review Items: es la imagen que el estimador abre (U-118 la exige); otra ruta sigue prohibida
IMG_ENTREGADA = re.compile(r"\bproceso/(?:review|rfi)_img/[\w.-]+\.(?:png|jpe?g)\b")


def verificar_texto_cliente(wb):
    err = []
    for ws in wb.worksheets:
        if ws.sheet_state != "visible":
            continue
        col_img = None                                  # R80f.38: la columna "Image" de Review Items nombra la imagen
        if ws.title == HOJA_REVISAR:                    # circulada que el revisor abre (U-118): un nombre de imagen ahí es
            for c in next(ws.iter_rows(min_row=2, max_row=2), []):   # el dato pedido, no texto interno
                if str(c.value or "").strip().lower() == "image":
                    col_img = c.column
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str):
                    # R80e.153 (O'Reilly rev6): la columna Image de Review Items lleva el NOMBRE de su imagen circulada
                    # (U-118 la exige; el formato fijo documenta "R01.jpg"); sin ruta ni carpeta interna
                    if ws.title == HOJA_REVISAR and c.column == 6 and RX_IMG_REVISAR.fullmatch(c.value.strip()):
                        continue
                    # v81cf28 CFA (BE-CF21): o la ruta de la carpeta ENTREGADA proceso/review_img | rfi_img (solo en Review Items)
                    m = TEXTO_INTERNO.search(IMG_ENTREGADA.sub(" ", c.value) if ws.title == HOJA_REVISAR else c.value)
                    if m:
                        err.append(f"{ws.title}!{c.coordinate}: texto interno en hoja visible '{m.group(0)}' (R80e.84)")
    return err[:40]


def verificar_v77c(wb):
    """v77c: U8 (sin renglón de acoustical sealant; exclusión escrita en Scope Checklist) y U9 / U10 (Review Items con
    el total anunciado, n/N consecutivo, floor plan por type A→Z antes que los detalles en su orden)."""
    err = []
    mats = [{"material": r[0], "unit": r[1]} for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True)
            if r and r[0] and len(r) > 2 and isinstance(r[2], (int, float))]
    err += [f"Material Summary: {e}" for e in acoustical_err(mats)]
    if HOJA_ALCANCES in wb.sheetnames:
        filas = [" ".join(str(c or "") for c in r) for r in wb[HOJA_ALCANCES].iter_rows(values_only=True)]
        if not any(re.search(r"acoustical sealant", f, re.I) and re.search(r"EXCLUDED", f) for f in filas):
            err.append("Scope Checklist sin la exclusión de acoustical sealant (U8: EXCLUDED en todos los proyectos)")
    if HOJA_REVISAR in wb.sheetnames:
        rr = [r for r in wb[HOJA_REVISAR].iter_rows(values_only=True)]
        if len(rr) < 2 or [str(c or "") for c in rr[1][:3]] != ["#", "Phase", "Type / order"]:
            err.append("Review Items en formato viejo (U9 / U10: primera fila con el total, columnas #, Phase, Type / order)")
        elif not re.match(r"\d+ questions in total", str(rr[0][0] or "")):
            err.append("Review Items sin el total anunciado en la primera fila (U9: 'N questions in total ...')")
        else:
            n = int(re.match(r"(\d+)", str(rr[0][0])).group(1))
            items = [r for r in rr[2:] if r and r[0]]
            if [str(r[0]) for r in items] != [f"{i}/{n}" for i in range(1, n + 1)]:
                err.append(f"Review Items: numeración n/N no consecutiva o distinta del total {n} (U9)")
            claves = [(0, _nat(r[2]), 0) if r[1] == "Floor plan" else
                      (1, [], int(r[2]) if str(r[2] or "").isdigit() else 10 ** 6) for r in items]
            if claves != sorted(claves):
                err.append("Review Items fuera del orden obligatorio (U10: floor plan por type A-Z, luego detalles)")
    return err


def _track_familia(carpetas):
    """v72 R71.8b: totales de bottom / top track de familias_out.json (si está en las carpetas de salidas)."""
    for c in carpetas:
        p = os.path.join(c, "familias_out.json")
        if os.path.isfile(p):
            try:
                f = (json.load(open(p, encoding="utf-8")) or {}).get("familias") or {}
            except ValueError:
                return None
            out = {}
            for k, v in f.items():
                if re.match(r"^bottom track", k, re.I):
                    out["bottom track"] = float(v)
                elif re.match(r"^top( /)? ?(deflection )?track", k, re.I):
                    out["top / deflection track"] = float(v)
            return out or None
    return None


TAM_STUD = re.compile(r'(\d+-\d+/\d+"|\d+(?:\.\d+)?")')


def verificar_r71_track(wb, fam_total=None):
    """R71.8 (v71, arbitraje #19): bottom track y top / deflection track se compran POR TAMAÑO de stud (un renglón por
    tamaño, más el track de parapet / otro gauge en el suyo); la suma = la familia. Con >= 2 tamaños de stud en
    Partition Takeoff, un renglón único "all sizes" (o faltar un tamaño) = falla.
    v76 (arbitraje #24): (1) un renglón es de bottom / top track si familias.py lo pone en esa familia (la MISMA regla
    que canon.verificar_track_nombres y que el calificador): "Parapet bottom track", "Bottom track - roof step..." y
    "... - other framing" suman; antes solo los que empezaban con "Bottom track" / "Top track" y la Σ no daba la
    familia. (2) Los tamaños que exigen renglón propio salen de las filas de partition types; un tamaño que solo
    aparece en OTHER FRAMING (grille head, cripples...) va en el renglón "other framing" de track_by_element (R75.2)."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import familias
    err = []
    if "Partition Takeoff" not in wb.sheetnames or "Material Summary" not in wb.sheetnames:
        return err
    ws = wb["Partition Takeoff"]
    col, tams, bloque_otro = None, set(), False
    for r in ws.iter_rows(values_only=True):
        if col is None:
            for k, v in enumerate(r):
                if str(v or "").strip().lower() == "stud size":
                    col = k
            continue
        c0 = str(r[0] or "").strip() if r else ""
        if c0.upper().startswith("TYPE "):
            bloque_otro = OTHER_TYPE.upper() in c0.upper()
            continue
        if bloque_otro:
            continue
        if col < len(r) and r[col] and re.search(r"z-furring|\bzf|150zf|hat channel", str(r[col]), re.I):   # BE-HF1
            continue                                # R80e.65: Z-furring sobre CMU no lleva renglón de track por tamaño
        if col < len(r) and r[col]:
            m = TAM_STUD.match(str(r[col]).strip())
            if m:
                tams.add(m.group(1))
    if len(tams) < 2:
        return err
    filas_ms = [(str(r[0] or ""), str(r[1] or "").strip().lower() if len(r) > 1 else "")
                for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True) if r]
    netos = {}
    for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True):
        if r and r[0] and len(r) > 2 and isinstance(r[2], (int, float)) and not isinstance(r[2], bool):
            netos.setdefault(str(r[0]), float(r[2]))
    fam_de = {"bottom track": "bottom track (todos)", "top / deflection track": "top / deflection track (todos)"}
    clases = {clase: [n for n, u in filas_ms if n and u == "lf" and familias.familia(n, u) == f]
              for clase, f in fam_de.items()}            # en su unidad: los pins / anchors del track van en PCS
    if not any(clases.values()):
        return err                                  # sin renglones de track: lo cubre la lista de familias obligatorias
    for clase, filas in clases.items():
        falta = sorted(t for t in tams if not any(t in n for n in filas))
        if falta:
            err.append(f"Material Summary: {clase} sin renglón por tamaño para {', '.join(falta)} (R71.8: un renglón por "
                       f"tamaño de stud; 'all sizes' no basta)")
        # v72 R71.8b: Σ renglones de la familia = familia (familias_out.json de las salidas); el bug de fusión ponía el
        # total de la familia en cada renglón parcial (track x N)
        vals = [round(netos[n], 2) for n in filas if n in netos and netos[n] > 0]
        if fam_total and clase in fam_total and vals:
            if abs(sum(vals) - fam_total[clase]) > 0.1 * max(1, len(vals)):
                err.append(f"Material Summary: Σ {clase} {round(sum(vals), 2)} != familia {fam_total[clase]} (R71.8b)")
    return err


def verificar_v68(wb, wf):
    """v68 (arbitraje #16): Inputs reales, compra con desperdicio una vez, plywood por material / espesor, sealant
    exterior aparte, yields con fórmula viva, Pending Items sin duplicados ni delta vacío, Excel íntegro en inglés."""
    err = []
    inp = wf["Inputs"] if "Inputs" in wf.sheetnames else None
    if inp is None:
        return ["falta la hoja Inputs"]
    # 1. toda cita a Inputs apunta a una celda con parámetro y valor
    for ws in wf.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str):
                    for col, rr in INPUTS_CITA.findall(c.value):
                        lab, val = inp.cell(int(rr), 1).value, inp[f"{col}{rr}"].value
                        if not lab or val in (None, "", "n/a"):
                            err.append(f"{ws.title}!{c.coordinate}: cita Inputs {col}{rr} que no existe o está vacía")
    ms = wf["Material Summary"]
    hdr = [str(c.value or "").strip().lower() for c in ms[3]]
    ci = {h: i for i, h in enumerate(hdr)}
    seen_ext = False
    for row in ms.iter_rows(min_row=4):
        v = [c.value for c in row]
        name, unit = str(v[0] or ""), str(v[ci.get("unit", 1)] or "").upper()
        if not name:
            continue
        pz = str(v[ci.get("pieces to buy", 7)] or "")
        # 2. desperdicio una vez: Pieces = ROUNDUP(F / stock) sobre el Purchase, nunca piezas por corte
        if pz.count("ROUNDUP") > 1 or "INT(" in pz.upper():
            err.append(f"Material Summary '{name[:40]}': Pieces cobra el desperdicio dos veces ({pz}); "
                       f"usar ROUNDUP(Purchase / stock)")
        # 3. plywood: un material y un espesor por renglón
        if unit == "SF" and re.search(r"plywood", name, re.I):
            err += [f"Material Summary: {e}" for e in plywood_err(name)]
        # 4. sealant exterior aparte del acoustical
        if re.search(r"sealant", name, re.I):
            ext = bool(SEAL_EXT.search(name))
            if ext and re.search(r"acoustic", name, re.I) and not re.search(r"not acoustic", name, re.I):
                err.append(f"Material Summary '{name[:50]}': mezcla sealant acoustical y exterior (renglones aparte)")
            seen_ext |= ext
            sel = str(v[ci.get("selling unit", 6)] or "").lower()
            if "tube" not in sel or "Inputs" not in pz:
                err.append(f"Material Summary '{name[:40]}': sealant se compra en tubes (Purchase / Inputs LF per tube)")
        if re.search(r"hanger wire", name, re.I) and unit == "LF" and "coil" not in str(v[6] or "").lower():
            err.append(f"Material Summary '{name[:40]}': hanger wire LF se compra de continuous coil")
        # 5. yields con fórmula viva que cita Inputs
        for f, rx in YIELD_NOMBRES.items():
            if re.search(rx, name, re.I):
                yf = str(v[ci["yield check (live formula)"]] or "") if "yield check (live formula)" in ci else ""
                if "Inputs!" not in yf:
                    err.append(f"Material Summary '{name[:40]}': yield sin fórmula viva a su celda de Inputs")
    # 6. Pending Items: sin ids / temas repetidos y con delta
    if "Pending Items" in wb.sheetnames:
        filas = [dict(id=r[0], pregunta=r[1], delta=r[2]) for r in wb["Pending Items"].iter_rows(min_row=2, values_only=True)
                 if r and r[0]]
        if len(rfis_vigentes(filas)) != len(filas):
            dup = [x["id"] for x in filas if x not in rfis_vigentes(filas)]
            err.append(f"Pending Items con RFIs repetidos (id o tema): {dup}")
        err += [f"Pending Items {x['id']}: sin delta" for x in filas if x["delta"] in (None, "")]
    # 7. íntegro en inglés (hojas, encabezados, celdas)
    for ws in wb.worksheets:
        if es_texto_es(ws.title):
            err.append(f"hoja '{ws.title}' con nombre en español")
        fpd = None                                      # R80w.46: la ficha del proyecto (R80w.44) copia nombres propios
        if ws.title == "Inputs":                        # impresos (direcciones, 'Camino del Rio'): no es texto nuestro
            fpd = next((c.row for c in ws["A"] if str(c.value or "").startswith("PROJECT DATA")), None)   # R80f.8 (v81cf13, Chuze): también el bloque R80e.121
        for row in ws.iter_rows():
            if fpd and row[0].row > fpd and len(row) > 1:
                row = [row[0]] + list(row[2:])          # se revisan rótulo y hoja, no el valor citado del plano
            for c in row:
                if isinstance(c.value, str) and not c.value.startswith("=") and es_texto_es(c.value):
                    err.append(f"{ws.title}!{c.coordinate} en español {es_texto_es(c.value)}: '{c.value[:60]}'")
    return err


def _recalcular(xlsx):
    """Pide a LibreOffice recalcular para que las fórmulas tengan valor guardado (lo leen el
    calificador y las compuertas). Si no hay LibreOffice, el Excel queda igual de válido."""
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        return "sin LibreOffice: fórmulas sin valor guardado (Excel las calcula al abrir)"
    d = tempfile.mkdtemp()
    r = subprocess.run([soffice, "--headless", "--calc", "--convert-to", "xlsx", "--outdir", d, xlsx],
                       capture_output=True, timeout=180)
    out = os.path.join(d, os.path.basename(xlsx))
    if r.returncode == 0 and os.path.exists(out):
        shutil.move(out, xlsx)
        return "fórmulas recalculadas"
    return "LibreOffice no pudo recalcular: " + r.stderr.decode()[:200]


EJEMPLO = {
    "proyecto": "Proyecto de ejemplo", "bid_set": "bid_set.pdf", "fecha": "2026-10-14",
    "inputs": {"waste_metal": 0.15, "waste_no_metal": 0.06, "sheet_w_ft": 4, "sheet_l_ft": 12,
               "stud_stock_ft": 20, "track_stock_ft": 10},
    "walls": [{"type": "A1", "wall": "1", "location": "Corridor 901 north", "length_lf": 20.0,
               "height_ft": 12.0, "stud_size": "3-5/8\"", "stud_oc_in": 16, "layers": 2, "board_sf": 480.0,
               "source": "3/X9.01", "status": "CONFIRMADO"}],
    "materials": [{"material": "3-5/8\" metal stud 362S137-33", "unit": "LF", "net": 300.0, "metal": True,
                   "selling_unit": "stick 20 ft", "stock": 20, "cut_ft": 12.0, "source": "Partition Takeoff; 3/X9.01"},
                  {"material": "5/8\" gypsum board, regular", "unit": "SF", "net": 480.0, "metal": False,
                   "selling_unit": "4x12 ft sheet", "source": "Partition Takeoff col Board"}],
    "rfis": [{"id": "RFI-01", "pregunta": "Height of wall W1 not dimensioned", "delta": "+/- 24 SF"}],
    "revisar": [{"n": 1, "total": 1, "fase": "floor_plan", "type": "A1", "punto": "Confirm height of wall W1",
                 "hoja_detalle": "3/X9.01", "imagen": "R01.jpg"}],
    "alcances": [{"id": "ALC-01", "nombre": "Interior partition framing", "estado": "CUANTIFICADO",
                  "nota": "Partition Takeoff"}],
}


def carpeta_de(familias_p):
    """v72b: carpeta de trabajo de un familias_out.json (out/ → la carpeta con el canon conciliado)."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import reglas
    base = os.path.dirname(os.path.abspath(familias_p))
    for c in (os.environ.get("TAKEOFF_WORK"), os.path.join(base, ".."), os.path.join(base, "..", "etapas"), base):
        if c and os.path.isdir(c) and reglas.buscar_canon(c):
            return os.path.abspath(c)
    return None


def main():
    a = sys.argv[1:]
    if len(a) == 2 and a[0] == "validar":
        err = validar(json.load(open(a[1], encoding="utf-8")))
        for e in err:
            print("ERROR ", e)
        print("FORMATO OK" if not err else f"FORMATO CON {len(err)} ERRORES")
        sys.exit(1 if err else 0)
    elif len(a) in (3, 5, 7) and a[0] == "armar":
        d = json.load(open(a[1], encoding="utf-8"))
        op = dict(zip(a[3::2], a[4::2]))
        if set(op) - {"--familias", "--trabajo"}:
            sys.exit(__doc__)
        if "--familias" not in op:
            sys.exit("NO SE ARMA: armar exige --familias familias_out.json (§8.6, 52.4) y la compuerta de reglas")
        try:
            d = fusionar(d, json.load(open(op["--familias"], encoding="utf-8")))
        except ValueError as e:
            sys.exit(f"NO SE ARMA: {e}")
        err = validar(d)
        if err:
            for e in err:
                print("ERROR ", e)
            sys.exit(f"NO SE ARMA: {len(err)} errores de formato")
        import reglas
        trabajo = op.get("--trabajo") or carpeta_de(op["--familias"])
        try:
            print("OK", a[2], "-", armar(d, a[2], trabajo))
        except reglas.ReglasNoOK as e:
            sys.exit(f"NO SE ARMA: {e}")
    elif len(a) in (2, 4) and a[0] == "verificar":
        if len(a) == 4 and a[2] != "--salidas":
            sys.exit(__doc__)
        err = verificar_excel(a[1], a[3:4])
        for e in err:
            print("ERROR ", e)
        print("EXCEL v67 OK" if not err else f"EXCEL CON {len(err)} ERRORES")
        sys.exit(1 if err else 0)
    elif len(a) == 2 and a[0] == "ejemplo":
        json.dump(EJEMPLO, open(a[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("OK ejemplo ->", a[1])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
