#!/usr/bin/env python3
"""criterios.py — v80: UN criterio por regla, compartido por todas las tools que la verifican.

Por qué existe (arbitraje #28): canon.py aceptaba un dato verdadero (R79.3: la sección burbujeada en OTRA hoja que
corta el ceiling es su fuente) y reglas.py lo rechazaba (A_CEILING_SYS solo aceptaba la burbuja sobre el RCP): ningún
dato verdadero pasaba las dos compuertas y la corrida quedó sin Excel. Lo mismo pasaba con el purlin (canon R79.4
acepta `purlin_rows_reason` y el tope a acero sin purlin; inventario.py no) y con las filas apiladas (`split_of`:
partition_types sumaba su LF al type y accesorios / reglas les ponían anchors de losa).

Regla R80.1: cuando dos tools verifican la misma regla, las dos llaman a la función de este módulo; ninguna la
reimplementa. `test_consistencia_tools.py` lo comprueba de dos formas: (a) diferencial — el mismo dato bueno / malo da
el mismo veredicto en cada tool; (b) barrido estático — las llaves de CAMPOS_COMPARTIDOS solo se leen aquí (y en las
tools listadas como dueñas de su cálculo).

Solo stdlib. Sin datos de ningún proyecto.
"""
import math
import re

RX_NHOJA = re.compile(r"\b[0-9A-Z]{1,2}/[A-Z]{1,3}-?\d")
RX_A_ACERO = re.compile(r"\bSTEEL\b|\bSLIP CLIP\b|\bBEAMS?\b|T/STEEL", re.I)
RX_TRACK = re.compile(r"\b(TRACK|RUNNER|DEFLECTION)\b", re.I)
RX_COTA = re.compile(r"\d+\s?'\s?-?\s?\d+(?:\s+\d+/\d+)?\s?\"|\d+(?:\s+\d+/\d+)?\s?\"|\d+\s?'")

# llave del canon -> módulos que pueden leerla directamente (además de criterios.py). El resto llama a este módulo.
CAMPOS_COMPARTIDOS = {
    "on_plan": (),
    "cuts_this": ("canon",),       # canon lee además details_checked[].cuts_this (lista de descartes, R79.3)
    "cut_on": (),
    "purlin_rows_reason": (),
    "purlin_detail": (),
    "split_track_detail": (),
}


# ---------------------------------------------------------------------------------------------- R70.1 / R79.3
SIN_CALLOUT = ("", "furring", "suspension", "suspended", "act", "open", "none", "open_to_structure")


def sistema_pide_callout(system):
    """Todo sistema de ceiling que no es el suspendido del campo (furring) ni abierto pide su detalle llamado."""
    return str(system or "").lower() not in SIN_CALLOUT


def system_callout_ok(sc):
    """El sistema de un ceiling que no es furring sale de un detalle LLAMADO sobre él: burbuja sobre ESTE ceiling
    (on_plan true) o la sección / detalle que lo CORTA burbujeada en otra hoja (cuts_this true + cut_on). Siempre con
    detail N/HOJA y source. Devuelve (ok, motivo)."""
    if not isinstance(sc, dict):
        return False, "sin system_callout"
    if not RX_NHOJA.search(str(sc.get("detail") or "")):
        return False, "system_callout.detail sin N/HOJA"
    if not str(sc.get("source") or "").strip():
        return False, "system_callout sin source"
    if sc.get("on_plan") is True:
        return True, "on_plan"
    if sc.get("cuts_this") is True:
        if str(sc.get("cut_on") or "").strip():
            return True, "cuts_this"
        return False, "cuts_this sin cut_on (hojas donde está la burbuja de la sección)"
    return False, "ni on_plan (burbuja sobre este ceiling) ni cuts_this + cut_on (sección que lo corta)"


# ---------------------------------------------------------------------------------------------- R79.4 purlin
def purlin_impreso(w):
    pd = w.get("purlin_detail")
    return isinstance(pd, dict) and bool(re.search(r"\b[0-9A-Z]{1,2}/[A-Z]{1,2}\d{1,2}(?:\.\d{1,2})?\b",
                                                   str(pd.get("source") or ""))) and \
        bool(re.search(r"\bPURLIN", str(pd.get("text") or ""), re.I))


def purlin_detail_mal(w):
    """purlin_detail declarado pero sin N/HOJA o sin el texto PURLIN impreso."""
    return w.get("purlin_detail") is not None and not purlin_impreso(w)


def tope_a_acero(w):
    return bool(RX_A_ACERO.search(str(w.get("to_deck_source") or "")))


def purlin_esperado(w, ori, flute):
    """None = la regla no opina (no va a deck); True / False = lo que el purlin debe ser. Purlin = top track a deck
    PARALELO al flute; si el detalle fija el tope a acero estructural, no lleva purlin salvo purlin_detail impreso."""
    if w.get("to_deck") is False:
        return None
    if tope_a_acero(w) and not purlin_impreso(w):
        return False
    return ori == flute


def filas_purlin_ok(a, b):
    """Dos filas apiladas de la misma línea en planta con purlin las dos: solo con purlin_rows_reason en una."""
    return bool(str(a.get("purlin_rows_reason") or "").strip() or str(b.get("purlin_rows_reason") or "").strip())


# ---------------------------------------------------------------------------------------------- R80.2 filas apiladas
def fila_apilada(w):
    """Un wall con split_of es una FILA APILADA sobre otro elemento de la misma huella (arranca sobre acero / otro
    elemento): no suma LF a la lista de walls de su type, no apoya en losa (sin slab pins ni anchors)."""
    return bool(w.get("split_of"))


def split_valido(const_split):
    """canopy_beam_split true solo con un detalle que IMPRIMA el track en la viga (`split_track_detail {source N/HOJA,
    text con TRACK / RUNNER / DEFLECTION}`). La geometría (viga dibujada dentro de la zona del stud) no basta: el wall
    va CONTINUO (una pieza, un bottom y un top track) y el split va a RFI con su delta. Devuelve (ok, motivo)."""
    if not isinstance(const_split, dict) or not const_split.get("value"):
        return True, "continuo"
    td = const_split.get("split_track_detail")
    if not (isinstance(td, dict) and RX_NHOJA.search(str(td.get("source") or "")) and
            RX_TRACK.search(str(td.get("text") or ""))):
        return False, ("canopy_beam_split true sin split_track_detail {source N/HOJA, text literal con TRACK}: una "
                       "viga dibujada dentro de la zona del stud no imprime track; el wall va CONTINUO y el split va "
                       "a RFI con su delta (R80.2)")
    return True, "split impreso"


def huella(w):
    b = w.get("band") or {}
    try:
        lo, hi = sorted((float(b["lo"]), float(b["hi"])))
        return str(b.get("sheet")), str(b.get("ori")), lo, hi
    except (KeyError, TypeError, ValueError):
        return None


def filas_dentro_del_padre(walls, tol_ft=0.5, esc=18.0):
    """Σ de los tramos split_of de un mismo nivel = el wall padre: cada fila apilada cae dentro de la huella de su
    padre y las filas del mismo padre no se solapan entre sí (dos filas sobre el mismo tramo = la misma fila contada
    dos veces). Devuelve la lista de errores."""
    por = {w.get("id"): w for w in walls}
    errores, hijos = [], {}
    for w in walls:
        p = w.get("split_of")
        if not p:
            continue
        pw = por.get(p)
        if pw is None:
            errores.append(f"{w['id']}: split_of {p} no existe")
            continue
        hijos.setdefault(p, []).append(w)
        hw, hp = huella(w), huella(pw)
        if hw and hp:
            if hw[2] < hp[2] - tol_ft * esc or hw[3] > hp[3] + tol_ft * esc:
                errores.append(f"{w['id']}: fila apilada sale de la huella de su padre {p} "
                               f"({round((hw[3] - hw[2]) / esc, 2)} ft vs {round((hp[3] - hp[2]) / esc, 2)} ft)")
        elif float(w.get("length_ft") or 0) > float(pw.get("length_ft") or 0) + tol_ft:
            errores.append(f"{w['id']}: fila apilada más larga que su padre {p}")
    for p, hs in hijos.items():
        for i, a in enumerate(hs):
            for b in hs[i + 1:]:
                ha, hb = huella(a), huella(b)
                if ha and hb and min(ha[3], hb[3]) - max(ha[2], hb[2]) > tol_ft * esc:
                    errores.append(f"{a['id']} y {b['id']}: dos filas split_of del mismo padre {p} sobre el mismo "
                                   f"tramo (declarar la de arriba split_of de la de abajo)")
    return errores


# ---------------------------------------------------------------------------------------------- R80.3 recess ATM
PIEZAS_ATM = ("sistered", "furring")


def pieza_atm_lf(piece, recess):
    """LF de una pieza impresa del recess con la regla del estimador: studs sistered = ROUNDUP(ancho / O.C.) piezas ×
    alto impreso; furring = ROUNDUP(alto / O.C.) filas × ancho. Devuelve (lf, op)."""
    w = float(recess["width_ft"]["value"])
    h = float(recess["height_ft"]["value"])
    oc = float((recess.get("oc_in") or {}).get("value") or 16) / 12.0
    if piece == "sistered":
        n = math.ceil(w / oc - 1e-9)
        return n * h, f"ROUNDUP({round(w, 3)} / {round(oc, 4)}) = {n} studs x {round(h, 3)} ft = {round(n * h, 2)}"
    if piece == "furring":
        n = math.ceil(h / oc - 1e-9)
        return n * w, f"ROUNDUP({round(h, 3)} / {round(oc, 4)}) = {n} rows x {round(w, 3)} ft = {round(n * w, 2)}"
    raise ValueError(f"pieza {piece}: sin regla de cálculo (usar lf + op con su cita)")


def recess_valido(recess):
    """width_ft {value, source} (huella del recess en planta) y height_ft {value, source, printed (texto de la cota
    impresa)}: el alto de las piezas es la COTA impresa del detalle, nunca un tramo medido en vector."""
    if not isinstance(recess, dict):
        return "atm_recess.recess {width_ft, height_ft, oc_in?} obligatorio con piezas sistered / furring (R80.3)"
    for k in ("width_ft", "height_ft"):
        v = recess.get(k)
        if not (isinstance(v, dict) and isinstance(v.get("value"), (int, float)) and float(v["value"]) > 0 and
                str(v.get("source") or "").strip()):
            return f"atm_recess.recess.{k} {{value > 0, source}} (R80.3)"
    if not RX_COTA.search(str(recess["height_ft"].get("printed") or "")):
        return ("atm_recess.recess.height_ft.printed: el texto de la cota IMPRESA del detalle (p. ej. 0'-0\"); un "
                "tramo medido en vector no reemplaza una cota impresa (R80.3, #0)")
    return None


# ---------------------------------------------------------------------------------------------- v80e escala por hoja
# Un set puede medir walls en hojas de escala distinta (floor plan 1/8" y enlarged plan 1/2"). La escala global
# `constants.plan_scale_pt_per_ft` vale para toda hoja que no esté en `constants.plan_scale_by_sheet`
# {"<hoja>": {value, source}}. Todas las tools que convierten pt <-> ft de una band llaman a escala_hoja (R80.1).
def _val(v, dflt):
    try:
        return float(v.get("value") if isinstance(v, dict) else v) if v is not None else dflt
    except (TypeError, ValueError):
        return dflt


def escala_global(canon, dflt=18.0):
    return _val((canon.get("constants") or {}).get("plan_scale_pt_per_ft"), dflt)


def escala_hoja(canon, sheet, dflt=18.0):
    """pt por ft de la hoja `sheet` (band.sheet / sheet del wall)."""
    por = (canon.get("constants") or {}).get("plan_scale_by_sheet") or {}
    if sheet is not None and str(sheet) in por:
        return _val(por[str(sheet)], escala_global(canon, dflt))
    return escala_global(canon, dflt)


def hoja_de(w):
    b = w.get("band") if isinstance(w.get("band"), dict) else {}
    return b.get("sheet") or w.get("sheet") or w.get("plan_sheet")


def escala_wall(canon, w, dflt=18.0):
    return escala_hoja(canon, hoja_de(w), dflt)


def multi_escala(canon):
    return bool((canon.get("constants") or {}).get("plan_scale_by_sheet"))


def subcanons_por_hoja(canon):
    """[(hoja, subcanon)]: el canon partido por hoja de band (walls), con plan_scale_pt_per_ft = la de esa hoja.
    Las demás llaves se copian tal cual. Sin plan_scale_by_sheet devuelve [(None, canon)]."""
    if not multi_escala(canon):
        return [(None, canon)]
    from collections import OrderedDict
    g = OrderedDict()
    for w in canon.get("walls") or []:
        g.setdefault(hoja_de(w), []).append(w)
    out = []
    for sh, ws in g.items():
        c = dict(canon)
        k = dict(canon.get("constants") or {})
        k["plan_scale_pt_per_ft"] = {"value": escala_hoja(canon, sh),
                                     "source": "plan_scale_by_sheet" if sh in (k.get("plan_scale_by_sheet") or {})
                                     else (k.get("plan_scale_pt_per_ft") or {}).get("source", "")}
        k.pop("plan_scale_by_sheet", None)
        c["constants"] = k
        c["walls"] = ws
        out.append((sh, c))
    return out
