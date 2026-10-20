#!/usr/bin/env python3
"""chequeos_v76.py — compuertas v76 (arbitraje #24) sobre el canon. Genéricas: ningún dato de proyecto.

Origen: dos corridas ciegas del mismo set con el mismo paquete dieron familias distintas. No fue una fórmula: una
corrida dejó elementos "para otra tarea" que nadie tomó, otra midió un jog de cara a cara repitiendo el espesor de un
wall, y un box con tag de partition type salió de su type por su `location`. Cada regla de abajo convierte esa
lectura en compuerta: la cantidad ya no depende de quién lea.

R76.1  Canopy completa. (a) Un `fascia_box` en una facade exige un ceiling `canopy_joist` con esa misma facade
       (el soffit bajo la canopy lleva joists y sheathing), o `canopy_soffit_none` [{facade, reason, source N/HOJA}]
       con el texto del detalle que muestra que no hay soffit framed. (b) Un `canopy_joist` exige al menos un run
       `canopy_soffit` (el track de los joists). (c) Un hand-off a otra tarea NO es un estado final: un renglón de
       `otros_ceilings` que describe un soffit / canopy exterior con framing debe quedar consumido por un ceiling
       JOIST_ONLY (`consumed_by` [ids] o un N/HOJA en común) o excluido con `excluded_reason` + N/HOJA.
R76.2  Column wrap con sheathing: todo `column_wrap` sin caras de board declara `sheathing {material, source}`
       (canon.py genera Σ faces_ft x height_ft) o `sheathing_none_reason`. Un plywood_strip a mano para un column
       wrap = error (el SF lo genera la tool, como el de la fascia).
R76.3  Jog del contorno ballistic DERIVADO de las bandas: dos walls K paralelos que se tocan punta con punta con un
       hueco entre sus caras enfrentadas (> 1 pt y <= 2 espesores: un step del contorno) llevan un jog = ese hueco (entre las caras, nunca de cara exterior
       a cara exterior). Falta el jog, sobra el jog o su largo no es el hueco -> error. Ningún jog cruza el espesor
       de un wall K (su banda no se solapa > 1 pt con la de un wall K en el eje del jog).
R76.4  Substrate de aberturas: toda abertura exterior declara `substrate {label, source N/HOJA}` (texto impreso del
       head / jamb: "FRT PLYWOOD", "NONE"...) o `substrate_none_reason`. Con PLYWOOD en el label canon.py genera el
       strip = bordes de la abertura (los mismos del jamb return, sin jambs contra pier) x
       constants.opening_substrate_width_ft {value, source}. Un plywood_strip a mano de head / jamb / sill de
       abertura = error.
R76.6  Perímetro de ceiling sin doble cuenta (R73.16 hecha compuerta): `ceilings[].perimeter_ft` de un ceiling
       suspendido es el perímetro COMPLETO del polígono (geometría: nunca menor que 2·√(π·área)); cada
       `ceiling_transition` declara `edge_of` [rooms de ceilings suspendidos cuyo borde es] (lista vacía si no es
       borde de ninguno). canon.py genera el track de perímetro = perimeter_ft − Σ transiciones de ese room: el
       borde que ya es transición no se carga dos veces, y no depende de que la corrida lo descuente a mano.
R76.5  Box / pier con tag de partition type (letras + dígito, sin EXT) sigue en su type: declara `faces` con board,
       `length_ft` y room interior (el LF del type = esas caras). Sin caras = error: el perímetro de la caja
       (incluye la parte exterior) nunca es el LF del type; `type_lf_basis` no lo reemplaza.
"""
import math
import re

NHOJA = re.compile(r"\b[0-9A-Z]{1,2}/[A-Z]{1,2}-?\d{1,3}\.\d{1,3}\b")
TAG_TYPE = re.compile(r"^[A-Z]{1,3}\d{1,2}[A-Z]?$")
RX_EXT_SOFFIT = re.compile(r"(?i)\b(canopy|soffit)")
RX_FRAMING = re.compile(r"(?i)\b(CFMF|STUDS?|JOISTS?|FRAMING|SHEATHING|PLYWOOD)\b")
RX_DIFERIDO = re.compile(r"(?i)not quantified|another task|other task|otra tarea|exterior task|read by")
RX_PLY = re.compile(r"(?i)PLYWOOD|\bPLY\b")
RX_OPENING = re.compile(r"(?i)\b(windows?|storefronts?|doors?|openings?)\b[^;]{0,60}\b(heads?|jambs?|sills?)\b"
                        r"|\b(heads?|jambs?|sills?)\b[^;]{0,60}\b(windows?|storefronts?|doors?|openings?)\b")
RX_EXT_ROOM = re.compile(r"EXTERIOR|NO\s+GYP|OUTSIDE", re.I)     # la misma de canon.py / partition_types.py
TOL = 1.0     # pt


def _txt(o, keys=("room", "ref", "source", "note", "tag", "legend")):
    return " ".join(str(o.get(k) or "") for k in keys)


def _tag(w):
    return str(w.get("tag") or "").strip().upper()


# ----------------------------------------------------------------------------------------------- R76.1 canopy
def r76_1(data):
    walls = data.get("walls") or []
    ceil = data.get("ceilings") or []
    cj = [c for c in ceil if c.get("system") == "canopy_joist"]
    none = {}
    for x in data.get("canopy_soffit_none") or []:
        if not str(x.get("reason") or "").strip() or not NHOJA.search(str(x.get("source") or "")):
            raise ValueError(f"canopy_soffit_none {x.get('facade')}: reason + source N/HOJA (texto del detalle que "
                             f"muestra que bajo esa canopy no hay soffit framed; R76.1)")
        none[str(x.get("facade"))] = x
    fac_cj = {str(c.get("facade")) for c in cj}
    for c in cj:
        if c.get("facade") is None:
            raise ValueError(f"{c.get('id', c.get('room'))}: canopy_joist sin facade (R76.1: se empareja con la "
                             f"fascia_box de su facade)")
    falta = sorted({str(w.get("facade")) for w in walls + (data.get("runs") or [])
                    if w.get("element") == "fascia_box"} - fac_cj - set(none))
    if falta:
        raise ValueError(f"R76.1: fascia_box en facade(s) {falta} sin ceiling canopy_joist de esa facade: el soffit "
                         f"bajo la canopy lleva joists 3-5/8\" + sheathing + track (o canopy_soffit_none con la cita)")
    if cj and not any(r.get("element") == "canopy_soffit" for r in (data.get("runs") or []) + walls):
        raise ValueError("R76.1: canopy_joist sin run canopy_soffit: el track de los joists (fascia + wall) sale del "
                         "run; sin él el track de ceilings / soffits pierde la canopy")
    ids_j = {str(c.get("id")) for c in ceil if c.get("system") in ("canopy_joist", "framed_soffit")}
    det_j = set()
    for c in ceil:
        if c.get("system") in ("canopy_joist", "framed_soffit"):
            det_j |= set(NHOJA.findall(_txt(c, ("source", "detail", "joist_source"))))
    for o in data.get("otros_ceilings") or []:
        t = _txt(o)
        if not (RX_EXT_SOFFIT.search(t) and RX_FRAMING.search(t)):
            continue
        if str(o.get("excluded_reason") or "").strip() and NHOJA.search(str(o.get("excluded_reason")) + " " +
                                                                         str(o.get("source") or "")):
            continue
        cb = [str(x) for x in o.get("consumed_by") or []]
        if cb and all(x in ids_j for x in cb):
            continue
        if not cb and set(NHOJA.findall(t)) & det_j:
            continue
        dif = " (nota de hand-off a otra tarea)" if RX_DIFERIDO.search(t) else ""
        raise ValueError(f"R76.1: otros_ceilings '{o.get('room')}' describe un soffit / canopy con framing{dif} y "
                         f"ningún ceiling canopy_joist / framed_soffit lo consume: un hand-off no es estado final "
                         f"(consumed_by [ids], o excluded_reason con N/HOJA)")
    return True


# ------------------------------------------------------------------------------------------ R76.2 column wrap
def _caras_board(w):
    return [f for f in w.get("faces") or [] if f.get("board") and float(f.get("height_ft") or 0) > 0]


def r76_2(data):
    for w in data.get("walls") or []:
        if w.get("element") != "column_wrap" or w.get("part_of"):
            continue                                  # un pier sin board lleva el sheathing de su facade (nailbase)
        if _caras_board(w):
            continue
        sh, nr = w.get("sheathing"), str(w.get("sheathing_none_reason") or "").strip()
        if sh is None and not nr:
            raise ValueError(f"{w['id']}: {w['element']} sin caras de board declara sheathing {{material, source}} "
                             f"(canon.py genera Σ faces_ft x height_ft) o sheathing_none_reason (R76.2)")
        if sh is not None:
            if not isinstance(sh, dict) or not sh.get("material") or not NHOJA.search(str(sh.get("source") or "")):
                raise ValueError(f"{w['id']}: sheathing {{material, source N/HOJA}} (R76.2)")
            if not w.get("faces_ft"):
                raise ValueError(f"{w['id']}: sheathing sin faces_ft (el SF = Σ caras x alto; R76.2)")
    for s in data.get("plywood_strips") or []:
        t = _txt(s, ("ref", "source", "location", "label"))
        if s.get("uso") == "column_wrap" or re.search(r"(?i)\bcolumn\s*wraps?\b", t):
            raise ValueError(f"plywood_strip '{s.get('ref')}': el sheathing de un column wrap lo genera canon.py desde "
                             f"walls[].sheathing (R76.2)")
    return True


def sheathing_column_wraps(data):
    """[(wall, material, sf, op)] del sheathing generado (R76.2)."""
    out = []
    for w in data.get("walls") or []:
        sh = w.get("sheathing")
        if w.get("element") not in ("column_wrap", "pier") or not isinstance(sh, dict):
            continue
        fs = [float(x) for x in w.get("faces_ft") or []]
        h = float(sh.get("height_ft", w["height_ft"]))
        sf = sum(fs) * h * int(sh.get("wraps", 1))
        out.append((w, sh["material"], sf, f"Σ faces {fs} = {round(sum(fs), 3)} x {round(h, 4)} = {round(sf, 2)} SF"))
    return out


# --------------------------------------------------------------------------------------------- R76.3 ballistic
def _band(x):
    b = x.get("band")
    if not isinstance(b, dict) or b.get("ori") not in ("H", "V"):
        return None
    try:
        return {"ori": b["ori"], "sheet": b.get("sheet"), **{k: float(b[k]) for k in ("c0", "c1", "lo", "hi")}}
    except (KeyError, TypeError, ValueError):
        return None


def jogs_k(walls):
    """[(id_a, id_b, ori_del_jog, coord, lo, hi)] jogs que exigen las bandas K: paralelos que se tocan punta con
    punta (≤ TOL) con hueco > TOL entre las caras enfrentadas. El jog va de c1 del primero a c0 del segundo."""
    ks = [(w, _band(w)) for w in walls if w.get("element", "wall") == "wall" and _tag(w).endswith("K")]
    ks = [(w, b) for w, b in ks if b]
    out = []
    for i, (w1, b1) in enumerate(ks):
        for w2, b2 in ks[i + 1:]:
            if b1["ori"] != b2["ori"] or b1["sheet"] != b2["sheet"]:
                continue
            if abs(b1["hi"] - b2["lo"]) <= TOL:
                p = (b1["hi"] + b2["lo"]) / 2
            elif abs(b2["hi"] - b1["lo"]) <= TOL:
                p = (b2["hi"] + b1["lo"]) / 2
            else:
                continue
            lo_c, hi_c = (b1, b2) if b1["c0"] <= b2["c0"] else (b2, b1)
            gap = hi_c["c0"] - lo_c["c1"]
            esp = max(b1["c1"] - b1["c0"], b2["c1"] - b2["c0"])
            if TOL < gap <= 2 * esp:                      # un step del contorno, no dos walls de lados opuestos
                out.append((w1["id"], w2["id"], "V" if b1["ori"] == "H" else "H", round(p, 2),
                            round(lo_c["c1"], 2), round(hi_c["c0"], 2)))
    return out


def r76_3(data, esc=None):
    walls = data.get("walls") or []
    esc = esc or float(((data.get("constants") or {}).get("plan_scale_pt_per_ft") or {}).get("value") or 18.0)
    req = jogs_k(walls)
    js = data.get("ballistic_jogs") or []
    jb = [(j, _band(j)) for j in js]
    ks = [(w, _band(w)) for w in walls if w.get("element", "wall") == "wall" and _tag(w).endswith("K")]
    err = []
    for j, b in jb:
        if b is None:
            err.append(f"{j.get('ref')}: ballistic_jog sin band {{ori, c0, c1, lo, hi, sheet}}")
            continue
        for w, bw in ks:
            if not bw or bw["sheet"] != b["sheet"] or bw["ori"] == b["ori"]:
                continue
            # el eje largo del jog (lo..hi) no cruza el espesor (c0..c1) del wall K perpendicular
            sol = min(b["hi"], bw["c1"]) - max(b["lo"], bw["c0"])
            cruza = min(b["c1"], bw["hi"]) - max(b["c0"], bw["lo"]) >= -TOL
            if sol > TOL and cruza:
                err.append(f"{j.get('ref')}: el jog cruza {round(sol, 2)} pt el espesor de {w['id']} (va solo entre "
                           f"las caras enfrentadas)")
    usados = set()
    for a, bb, ori, p, lo, hi in req:
        L = (hi - lo) / esc
        ok = None
        for k, (j, b) in enumerate(jb):
            if b and b["ori"] == ori and abs(b["lo"] - lo) <= TOL and abs(b["hi"] - hi) <= TOL:
                ok = k
                break
        if ok is None:
            err.append(f"falta el jog entre {a} y {bb}: hueco entre caras {lo}-{hi} pt = {round(L, 4)} ft")
            continue
        usados.add(ok)
        if abs(float(jb[ok][0].get("length_ft") or 0) - L) > 0.02:
            err.append(f"{jb[ok][0].get('ref')}: length_ft {jb[ok][0].get('length_ft')} != hueco entre caras "
                       f"{round(L, 4)} ft")
    for k, (j, b) in enumerate(jb):
        if k not in usados and b is not None:
            err.append(f"{j.get('ref')}: jog que no une dos walls K con hueco entre caras (sobra o va de cara "
                       f"exterior a cara exterior)")
    if err:
        raise ValueError("R76.3 contorno ballistic: " + "; ".join(err))
    return True


# ------------------------------------------------------------------------------------- R76.4 opening substrate
def aberturas_ext(data, es_ext):
    out = []
    for w in data.get("walls") or []:
        for op in w.get("openings") or []:
            if str(op.get("kind", "door")) in ("duct", "fire_damper", "penetration"):
                continue
            if es_ext(w) or op.get("location") == "exterior" or str(op.get("kind")) in ("window", "storefront", "atm"):
                out.append(op)
    for op in data.get("openings_extra") or []:
        if str(op.get("kind")) in ("storefront", "window", "atm") or op.get("location") == "exterior":
            out.append(op)
    return out


def r76_4(data, ops):
    falta = []
    for op in ops:
        s = op.get("substrate")
        if s is None:
            if not str(op.get("substrate_none_reason") or "").strip():
                falta.append(str(op.get("ref")))
            continue
        if not isinstance(s, dict) or not str(s.get("label") or "").strip() or \
                not NHOJA.search(str(s.get("source") or "")):
            raise ValueError(f"{op.get('ref')}: substrate {{label (texto impreso), source N/HOJA}} (R76.4)")
    if falta:
        raise ValueError(f"R76.4: abertura(s) exterior(es) sin substrate {{label, source}} ni substrate_none_reason: "
                         f"{falta} (lee el head / jamb: FRT plywood u otro; el strip lo genera canon.py)")
    if any(isinstance(op.get("substrate"), dict) and RX_PLY.search(str(op["substrate"].get("label")))
           for op in ops):
        c = (data.get("constants") or {}).get("opening_substrate_width_ft")
        if not isinstance(c, dict) or c.get("value") is None or not str(c.get("source") or "").strip():
            raise ValueError("constants.opening_substrate_width_ft {value, source} obligatoria con substrate de "
                             "plywood en aberturas (ancho del strip; una vez para el proyecto; R76.4)")
    for s in data.get("plywood_strips") or []:
        t = _txt(s, ("ref", "location", "label"))
        if s.get("uso") == "pier" or re.search(r"(?i)\bpiers?\b", t):
            continue                                      # el plywood de piers es otra decisión (no es abertura)
        if s.get("opening_ref") or RX_OPENING.search(t):
            raise ValueError(f"plywood_strip '{s.get('ref')}': substrate de head / jamb / sill de abertura -> "
                             f"openings[].substrate (canon.py genera el strip; R76.4)")
    return True


# ------------------------------------------------------------------------------------------- R76.5 box con tag
def r76_5(data):
    for w in data.get("walls") or []:
        if w.get("element") not in ("pier", "column_wrap") or w.get("part_of"):
            continue
        t = _tag(w)
        if not TAG_TYPE.match(t) or t.startswith("EXT"):
            continue
        caras = [f for f in _caras_board(w) if f.get("length_ft") is not None and
                 not RX_EXT_ROOM.search(str(f.get("room") or ""))]
        if not caras:
            raise ValueError(f"{w['id']}: {w['element']} con tag {t} sin caras de board interiores con length_ft: el LF "
                             f"del type = esas caras (R76.5; type_lf_basis no las reemplaza; el perímetro de la caja "
                             f"incluye la parte exterior)")
    return True


# --------------------------------------------------------------------------------- R76.6 perímetro de ceiling
def bordes_transicion(data, susp=("furring", "stud_joist")):
    """{room: LF de ceiling_transition que son borde de ese ceiling suspendido} (R76.6)."""
    rooms = {str(c.get("room")) for c in data.get("ceilings") or [] if c.get("system") in susp}
    out = {}
    for w in (data.get("walls") or []) + (data.get("runs") or []):
        if w.get("element") != "ceiling_transition":
            continue
        eo = w.get("edge_of")
        if not isinstance(eo, list):
            raise ValueError(f"{w.get('id')}: ceiling_transition sin edge_of [rooms de ceilings suspendidos cuyo borde "
                             f"es; [] si ninguno] (R76.6: su track no se vuelve a cargar como perímetro)")
        for r in eo:
            if str(r) not in rooms:
                raise ValueError(f"{w.get('id')}: edge_of '{r}' no es un ceiling suspendido declarado {sorted(rooms)}")
            out[str(r)] = out.get(str(r), 0.0) + float(w["length_ft"])
    return out


def r76_6_perimetro(c):
    P, A = float(c["perimeter_ft"]), float(c.get("area_sf") or 0)
    lim = 2 * (math.pi * A) ** 0.5                # ninguna figura de esa área tiene menos perímetro (círculo)
    if A > 0 and P < 0.99 * lim:
        raise ValueError(f"{c.get('room')}: perimeter_ft {P} < 2·√(π·área) {round(lim, 2)}: es el perímetro "
                         f"COMPLETO del polígono; los bordes que son ceiling_transition los descuenta canon.py (R76.6)")
    return True


def verificar(data, es_ext):
    r76_1(data)
    r76_2(data)
    if data.get("ballistic_jogs") is not None or any(_tag(w).endswith("K") for w in data.get("walls") or []):
        r76_3(data)
    r76_4(data, aberturas_ext(data, es_ext))
    r76_5(data)
    return True
