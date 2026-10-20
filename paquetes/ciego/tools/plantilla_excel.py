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
 "revisar": [ {"n": 1, "punto": "...", "hoja_detalle": "6/A12.01", "imagen": "R01.jpg"} ],
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


def validar(d):
    err = []
    for k in ("proyecto", "bid_set", "fecha", "inputs", "walls", "materials", "rfis", "revisar", "alcances"):
        if k not in d:
            err.append(f"falta la clave '{k}'")
    if err:
        return err
    for i, w in enumerate(d["walls"]):
        for k in WALL_KEYS:
            if k not in w or w[k] in ("", None):
                err.append(f"walls[{i}] ({w.get('type')} #{w.get('wall')}): falta '{k}'")
        for k in ("length_lf", "height_ft", "board_sf"):
            if k in w and not (isinstance(w[k], (int, float)) and w[k] >= 0):
                err.append(f"walls[{i}]: '{k}' debe ser número >= 0")
        if w.get("status") not in STATUS:
            err.append(f"walls[{i}]: status debe ser {sorted(STATUS)}")
        if w.get("source") and not re.search(r"\b[0-9A-Z]{1,2}/[A-Z]{1,2}\d", str(w["source"])) and w.get("status") != "PENDIENTE":
            err.append(f"walls[{i}]: source debe citar DETALLE/HOJA (ej. 3/A12.01)")
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
        if a.get("estado") not in ("CUANTIFICADO", "NO APLICA", "RFI"):
            err.append(f"alcances[{i}]: estado debe ser CUANTIFICADO / NO APLICA / RFI")
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
    (12, "plan_scale_pt_per_ft", "Floor plan scale (pt/ft)", None, "Project value (canon constants)."),
    (13, "bod_ft", "B.O. Deck (ft)", None, "Project value (canon constants)."),
    (14, "top_parapet_ft", "T.O. Parapet (ft)", None, "Project value (canon constants)."),
    (15, "sealant_lf_per_tube", "Sealant coverage (LF per tube)", 25, "Sealant yield per tube - set your supplier's figure."),
    (16, "crc_stock_ft", "C.R. channel stock length (ft)", 16, "1-1/2\" cold-rolled channel (bracing, carrying channel)."),
    (17, "hat_stock_ft", "Hat / furring channel stock (ft)", 12, "7/8\" hat furring channel."),
    (18, "trim_stick_ft", "Trim stick length (ft)", 10, "Corner bead, casing bead, shadow molding, PVC trim."),
    (19, "hanger_wire_purchase", "Hanger wire purchase", "continuous coil (LF)",
     "Bought by LF from a continuous coil; the hanger count goes on its own PCS row."),
    (20, "drywall_screws_per_sf", "Drywall screws per SF of board", 1.2, "YIELD (GA-216 field / perimeter spacing)."),
    (21, "framing_screws_per_stud", "Framing screws per stud piece", 4, "YIELD: 2 per stud-to-track connection, each end."),
    (22, "slab_pin_spacing_ft", "Power-driven pin spacing (ft)", 1.0, "YIELD: bottom track on slab, interior walls."),
    (23, "joint_compound_lb_per_sf", "Joint compound (lb per SF)", 0.072,
     "YIELD: 72 lb per 1,000 SF, level 4 (estimator criterion)."),
    (24, "joint_tape_lf_per_sf", "Joint tape (LF per SF)", 0.37, "YIELD: 370 LF per 1,000 SF."),
    (25, "anchor_spacing_ft", "Expansion anchor spacing (ft)", 8 / 12, "YIELD: exterior bottom track on slab."),
]
CELDA = {k: f"Inputs!$B${r}" for r, k, *_ in INPUTS_V68 if k}
CELDA["sheet_sf"] = "Inputs!$B$9"
INPUT_ROWS = {r for r, *_ in INPUTS_V68}
# Clase de compra por nombre: (regex, solo metal, selling unit (formato con el stock), clave de Inputs)
COMPRA_V68 = [
    (r"sealant", False, "tube ({v:g} LF per tube)", "sealant_lf_per_tube"),
    (r"hanger wire", False, "continuous coil (LF)", None),
    (r"header|box beam|framed opening|extra framing|cfmf|\bstud\b|studs|kicker|joist|362cr|stud blocking",
     True, "stick {v:g} ft", "stud_stock_ft"),
    (r"bracing|carrying channel|c\.r\. channel|cold[- ]rolled", True, "C.R. channel {v:g} ft", "crc_stock_ft"),
    (r"furring channel|hat channel", True, "hat channel {v:g} ft", "hat_stock_ft"),
    (r"corner bead|casing|shadow|metal trim|pvc trim|l[- ]bead|j[- ]bead|edge trim", False, "trim stick {v:g} ft",
     "trim_stick_ft"),
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
    return "=" + (REF["waste_metal"] if m["metal"] else REF["waste_no"])


def formula_piezas(m, r, d=None):
    """Pieces to buy = ROUNDUP(Purchase / stock) con Purchase = NET x (1 + waste): el desperdicio UNA vez."""
    unit = str(m["unit"]).upper()
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
        return f"=ROUNDUP(F{r},0)"
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
     r"2/S5\.20\?", "openings with their own box (openings_extra) > 4'-0\": do they also take the additional "
                    "head track of 2/S5.20?"),
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


def es_texto_es(t):
    """[] si el texto está en inglés; motivo si no (función de idioma_es + palabras sueltas y acentos)."""
    if not isinstance(t, str) or len(t) < 4:
        return []
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import idioma_es as IE
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
        ws.cell(r, 1, lab); ws.cell(r, 2, "n/a" if v is None else v); ws.cell(r, 3, nota)
        if k and v is not None:
            ws.cell(r, 2).fill = S["yellow"]
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
                w["layers"], w["stud_size"], w["stud_oc_in"], w["board_sf"], en(w["location"]),
                en(w["source"]), f"[{ESTADO_EN.get(w['status'], w['status'])}]"]
    first_data = ws.max_row + 1
    for t in orden:
        ws.append([f"TYPE {t}"]); ws.cell(ws.max_row, 1).font = S["tipo"]; ws.cell(ws.max_row, 1).fill = S["tf"]
        for w in [x for x in d["walls"] if x["type"] == t]:
            ws.append(fila_wall(t, w))
    last = ws.max_row
    # v67: texto del total en la col. B (con texto en la A el calificador lo suma como un wall del último TYPE)
    ws.append([None, "TOTAL - PARTITIONS", f"=SUM(C{first_data}:C{last})", None, None, None, None,
               f"=SUM(H{first_data}:H{last})"])
    ws.cell(ws.max_row, 2).font = S["tipo"]
    if d.get("other_framing"):
        ws.append([]); ws.append([f"TYPE {OTHER_TYPE}"])
        ws.cell(ws.max_row, 1).font = S["tipo"]; ws.cell(ws.max_row, 1).fill = S["tf"]
        for w in d["other_framing"]:
            ws.append(fila_wall(w["type"], w))

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
        ws.append([en(m["material"]), unit, m["net"], waste_celda(m, REF), f"=C{r}*D{r}", f"=C{r}+E{r}",
                   sel, formula_piezas(m, r, d), en(m["source"]), m.get("yield_formula")])

    # ---------- RFIs / Review Items / Scope Checklist ----------
    ws = wb.create_sheet("Pending Items")
    ws.append(["RFI", "Question / condition", "Delta of each alternative"])
    for c in range(1, 4):
        ws.cell(1, c).font = S["h"]; ws.cell(1, c).fill = S["hf"]
    for x in rfis_vigentes(d["rfis"]):
        ws.append([x.get("id"), en(x.get("pregunta")), en(fmt_delta(x.get("delta"), x.get("unidad")))])
    ws = wb.create_sheet(HOJA_REVISAR)
    ws.append(["#", "Item", "Sheet + detail", "Image"])
    for x in d["revisar"]:
        ws.append([x.get("n"), en(x.get("punto")), x.get("hoja_detalle"), x.get("imagen")])
    ws = wb.create_sheet(HOJA_ALCANCES)
    ws.append(["Scope ID", "Scope", "Status", "Note (quantity, NOT APPLICABLE + sheet, or RFI)"])
    for x in d["alcances"]:
        ws.append([x.get("id"), en(x.get("nombre")), ESTADO_EN.get(x.get("estado"), x.get("estado")),
                   en(x.get("nota"))])

    for w in wb.worksheets:
        for i, col in enumerate(w.columns, 1):
            ancho = max((len(str(c.value)) for c in col if c.value is not None), default=8)
            w.column_dimensions[L(i)].width = min(max(10, ancho + 2), 60)
    import reglas
    reglas.sellar(wb, out_reglas)
    wb.save(salida)
    return _recalcular(salida)


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
    return t[:240] or "accesorios.py"


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


def sealant_exterior(fo, fam="acoustical sealant"):
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
    "3-5/8\" stud (todos los gauges)": "3-5/8\" metal stud (LF of material)",
    "1-5/8\" stud": "1-5/8\" metal stud (LF of material)",
    "6\" parapet stud": "6\" parapet infill stud (LF of material)",
    "track de ceilings / soffits": "Track, ceilings / soffits / canopy",
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
    "5/8\" EXTERIOR gyp sheathing": "5/8\" EXTERIOR gypsum sheathing",
    "5/8\" glass mat sheathing": "5/8\" glass mat sheathing (exterior face of the stud)",
    "ballistic panel": "Ballistic panel {th}UL752",
    "3/8\" gyp board": "3/8\" gypsum board",
    "FRP": "FRP panels",
    "cement board": "Cement board (substrate under the FRP cove base band)",
    "FRT blocking": "Blocking FRT / 2X FRT wood",
    "metal trim (corner bead, casing, shadow molding)": "METAL trim - corner bead, casing bead, shadow molding, "
                                                        "gypsum edge trim",
    "acoustical sealant": "Acoustical sealant",
}
WOOD_NOMBRE = "Blocking 2X wood (not labeled FRT)"
BLK_NOMBRES = {"edge": "Stud blocking at edge of gypboard (structural detail)",
               "items": "Metal stud blocking at wall-mounted items (notes)"}


def nombre_plantilla(fam, fo):
    n = NOMBRES_PLANTILLA.get(fam)
    if not n:
        return None
    c = fo.get("nombres_contexto") or {}
    th = str(c.get("ballistic_th") or "")
    oc = c.get("bracing_oc_in")
    return n.format(th=(th + " ") if th else "", oc=f" @ {oc:g}\" O.C." if isinstance(oc, (int, float)) else "")


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
                mats.append(dict(m, material=BLK_NOMBRES.get(k, k), net=float(v),
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
        tot = sum(float(x.get("net") or 0) for x in ms)
        if abs(tot - float(fam_canon[fam])) > 0.1:
            raise ValueError(f"familia '{fam}' repartida en {len(ms)} renglones suma {round(tot, 2)} != familia "
                             f"{fam_canon[fam]} (R71.8b: los renglones por tamaño suman la familia)")
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
        for k, v in des.items():
            mats.append({"material": k, "unit": "SF", "net": v, "metal": False, "selling_unit": "sheet",
                         "source": f"familias_out.json FRT plywood by material; {cit or 'canon rows'}"})
    # v68: sealant exterior (base of gypsum) en su propio renglón
    ext = sealant_exterior(fo)
    if ext > 0 and not any(SEAL_EXT.search(str(m["material"])) and "sealant" in str(m["material"]).lower()
                           and not re.search(r"(?<!not )acoustic", str(m["material"]), re.I) for m in mats):
        for i, m in enumerate(mats):
            if familias.familia(m["material"], str(m["unit"]).lower()) == "acoustical sealant":
                nom = "Acoustical sealant" if SEAL_EXT.search(str(m["material"])) else m["material"]
                mats[i] = dict(m, material=nom, net=round(float(m["net"]) - ext, 2))   # (#16A: el nombre mezclaba)
                break
        mats.append({"material": SEAL_EXT_NOMBRE, "unit": "LF", "net": ext, "metal": False,
                     "source": "familias_out.json acoustical sealant rows 'base of gypsum (exterior)'"})
    # v68: hanger wire en PCS además del LF
    hp = (fo.get("hanger_pcs") or {}).get("total_pcs")
    if hp and not any("hanger" in str(m["material"]).lower() and str(m["unit"]).upper() in ("PCS", "EA")
                      for m in mats):
        mats.append({"material": "Hanger wire 12 ga - hanger count (one per hanger, height per room)",
                     "unit": "PCS", "net": float(hp), "metal": True, "waste": "none",
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
        mats.append(m)
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
    alc = list(d["alcances"])
    for k, why in (fo.get("excluidas") or {}).items():
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
        d["other_framing"] = [row(str(o.get("element")), dict(o, wall=o["id"])) for o in pt.get("other_framing") or []]
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
    for f, n in accesorios.NOMBRES_EXCEL.items():
        pref = n.split("{")[0].strip()
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
    err += verificar_v68(wb, wf)
    carpetas = [os.path.dirname(os.path.abspath(xlsx))] + [str(x) for x in (salidas or [])]
    err += verificar_salidas(wb, carpetas)
    err += verificar_r708(wf)
    err += verificar_r71_track(wb, _track_familia(carpetas))
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
        for row in ws.iter_rows():
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
               "source": "3/A12.01", "status": "CONFIRMADO"}],
    "materials": [{"material": "3-5/8\" metal stud 362S137-33", "unit": "LF", "net": 300.0, "metal": True,
                   "selling_unit": "stick 20 ft", "stock": 20, "cut_ft": 12.0, "source": "Partition Takeoff; 3/A12.01"},
                  {"material": "5/8\" gypsum board, regular", "unit": "SF", "net": 480.0, "metal": False,
                   "selling_unit": "4x12 ft sheet", "source": "Partition Takeoff col Board"}],
    "rfis": [{"id": "RFI-01", "pregunta": "Height of wall W1 not dimensioned", "delta": "+/- 24 SF"}],
    "revisar": [{"n": 1, "punto": "Confirm height of wall W1", "hoja_detalle": "3/A12.01", "imagen": "R01.jpg"}],
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
