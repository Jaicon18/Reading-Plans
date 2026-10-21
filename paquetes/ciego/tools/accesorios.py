#!/usr/bin/env python3
"""accesorios.py v67 — familias de ACCESORIOS y EXTRAS desde el canon (sin juicio fuera de las reglas escritas).

Por qué existe (pruebas #15A/#15B, skill v65b, 17-oct-2026): canon.py produce las familias de geometría, pero
NINGUNA de las de accesorios / extras que el calificador ya evalúa: additional head track, stud reinforcement MEP,
extra framing ATM, gypsum board jamb return, PVC trim at FRP, PAFs and duct sleeves, access panel, drywall screws,
framing screws, slab pins, expansion anchors, joint compound, joint tape. Además Level 5 y el 2-1/2" CFMF del
coiling grille head salían sin regla común. Reglas: ACCESORIOS_REGLAS.md (una por familia, con fuente).

Criterio del estimador (siempre incluidos, "Accesorios always include trims, taping, drywall screws, framing
screws and track pins"): ningún renglón de accesorios se deja fuera; si falta el dato, la familia sale PENDIENTE
con aviso (nunca un número inventado).

ENTRADA:
  familias_out.json  (salida de canon.py v65b: {familias, filas, ...})
  takeoff_canon.json (esquema canon.py v65b; bloques opcionales nuevos abajo)
  --studs studs_out.json  (opcional, salida de studs_nodos vía canon.py: piezas por wall para framing screws)
  --fo fo_in.json         (opcional, entrada de framed_openings.py: access panels y penetraciones MEP en walls)

Bloques OPCIONALES nuevos en takeoff_canon.json (todos con source):
  constants.<yield> {value, source}  sobrescribe el default del estimador (tabla DEFAULTS).
  constants.level5_tags {value: ["WC-nn", ...], source}  tags del finish schedule que dicen LEVEL 5.
  level5_items[].wc_tag, level5_items[].base_ft {value, source}  (altura neta = h - base, key note de la base).
  walls[grille_head].stud_len_ft {value, source}  o  walls[grille_head].head_build
      {head_ft, box_depth_ft, n_box, board_in, source}  (largo del 2-1/2" entre los dos box beams).
  extra_framing [{ref, lf | pcs+len_ft, kind (mep|other), source}]   (v77c U1: nunca de ATM; el ATM = 0)
  mep_penetrations [{ref, wall, width_in, qty, source}]  (penetraciones en walls, 6/S5.20)
  access_panels [{ref, qty, source}]
  tile_base[].inside_corners {value, vertices, outside_corners, source}  (esquinas interiores del cuarto con FRP;
    v68: inside + outside = vertices e inside - outside = 4)

v67 (integración, 17-oct-2026) — reglas que cierran los huecos de la verificación de integración:
  - stud reinforcement MEP: mep_sweep {sheets: [P*, M*, ...], source} OBLIGATORIO (barrido de pipes / ductos /
    conduit en las hojas P y M contra los walls de studs). Sin barrido = PENDIENTE aunque haya fire dampers.
    mep_penetrations[] acepta dia_in (pipe redondo): <= 1" centrado en el web = 0 plates (6/S5.20).
  - extra framing ATM: si hay una abertura ATM (kind atm o "ATM" en el ref) el canon DEBE declarar
    atm_recess {source N/HOJA, drawn} o atm_recess_none_reason. Si no: ValueError.
    v77c (U1, R77.11): el framing de un recess de ATM / equipo empotrado está en la wall que lo contiene (su type);
    extra framing ATM = 0; lo que un detalle impreso pida explícitamente (atm_recess.extra_printed) sale como RFI.
  - jamb return: toda abertura exterior (wall EXT* / location exterior, storefront, window, ATM) DECLARA
    jamb_return true|false + jamb_return_source (la sección que se leyó); storefront con return declara
    wall_jambs + wall_jambs_source. Si no: ValueError.
  - Level 5: cada item declara base_ft {value, source} (0 con source si no hay base); los tags de
    constants.level5_tags se emparejan EXACTO con wc_tag (no por substring); level5_tags [] con source = 0.
  - framing screws: piezas = campo "pcs" de las filas de canon (conteo actual), regex solo como respaldo.
  - grille head: sin head_build / stud_len_ft = PENDIENTE (nunca height_ft).
  - accesorios_rfi [{familia, motivo, delta, source}]: lo que ningún plano contesta pasa de PENDIENTE a RFI con
    delta. Una familia PENDIENTE bloquea plantilla_excel.py armar.
  - accesorios_none [{familia, why, source}]: el plano contesta que no hay (ej. sin ATM) -> 0 DERIVADO.
  - nombres_excel: renglón EXACTO de Material Summary por familia.

SALIDA: accesorios_out.json {familias: {nombre: valor}, unidades, estado, filas, avisos, rfis, nombres_excel}

Uso:  python3 accesorios.py familias_out.json takeoff_canon.json salida.json [--studs f] [--fo f]
"""
import json
import math
import re
from collections import Counter
import sys

EPS = 1e-6

# Nombres = hoja "Familias" de la referencia (grader). No cambiar sin cambiar el calificador.
F_AHT = "additional head track"
F_REINF = "stud reinforcement MEP"
F_XATM = "extra framing ATM"
F_GRILLE = "2-1/2\" CFMF coiling grille head"
F_JR = "gypsum board jamb return"
F_PVC = "PVC trim at FRP"
F_PAF = "PAFs and duct sleeves"
F_AP = "access panel"
F_DWS = "drywall screws"
F_FS = "framing screws"
F_PINS = "slab pins"
F_ANCH = "expansion anchors"
F_JC = "joint compound"
F_JT = "joint tape"
F_L5 = "Level 5 finish"
F_CLIPS = "deflection clips"

UNIDAD = {F_AHT: "lf", F_REINF: "pcs", F_XATM: "lf", F_GRILLE: "lf", F_JR: "sf", F_PVC: "lf", F_PAF: "pcs",
          F_AP: "pcs", F_DWS: "pcs", F_FS: "pcs", F_PINS: "pcs", F_ANCH: "pcs", F_JC: "lb", F_JT: "lf", F_L5: "sf",
          F_CLIPS: "pcs"}
# Desperdicio que aplica plantilla_excel.py (criterio del estimador: 15 % metal; no-metal = mismo factor que el
# board; yields de accesorios sin desperdicio, igual que la referencia).
WASTE = {F_AHT: "metal", F_XATM: "metal", F_GRILLE: "metal", F_JR: "board", F_PVC: "board", F_L5: "board"}
FAMS = list(UNIDAD)
# Renglón de Material Summary por familia (el calificador empareja por medidas + palabras clave + unidad).
NOMBRES_EXCEL = {
    F_AHT: "Additional head track at openings over 4'-0\" wide",
    F_REINF: "Stud reinforcement at MEP penetrations",
    F_XATM: "Extra framing - ATM recess (0: the recess framing is in the wall that contains it)",
    F_GRILLE: "2-1/2\" CFMF @ 16\" O.C. at coiling grille head ({det})",
    F_JR: "Gypsum board jamb return at openings",
    F_PVC: "PVC trim - edge trim molding and inside corner molding at the FRP",
    F_PAF: "Power-driven fasteners and duct sleeves",
    F_AP: "Access panel {med}",
    F_DWS: "Drywall screws 1-1/4\" bugle head",
    F_FS: "Framing screws, pan head self-drilling",
    F_PINS: "Power-driven fasteners, slab pins for the bottom track",
    F_ANCH: "Expansion anchors Hilti 1/4\" Kwik Bolt II, exterior bottom track @ 8\" O.C.",
    F_JC: "Joint compound, all purpose",
    F_JT: "Joint tape, paper",
    F_L5: "Level 5 finish",
    F_CLIPS: "Deflection clips at non-load-bearing walls to structure",
}
EXCLUIDAS = {"batt insulation": "EXCLUDED (estimator standing order: no insulation)"}
NHOJA = re.compile(r"\b[0-9A-Z]{1,2}/[A-Z]{1,2}\d")
# v68: un barrido MEP "a ojo" no es reproducible (dos pruebas dieron listas distintas): se rechaza.
VISUAL_RE = re.compile(r"(?i)\b(visual|a ojo|by eye|eyeball)")
DUCT_RE = re.compile(r"(?i)\b(duct|FD|fire damper|R-\d|S-\d|grille|register|diffuser)")
ABUTS = ("wall", "pier", "frame", "none")          # v68: remate de cada jamb del storefront
ATM_RE = re.compile(r"\bATM\b", re.I)

# Defaults = criterio del estimador (referencia v4 hojas Inputs / Handoff - Approved; decisiones del usuario).
# El canon los sobrescribe con constants.<clave> {value, source}.
DEFAULTS = {
    "drywall_screws_per_sf": (1.2, "Estimator yield, Inputs!B20 (GA-216: field 12\" O.C., perimeter 8\" O.C.)"),
    "joint_compound_lb_per_sf": (0.072, "Estimator yield, Inputs!B23 (72 lb per 1,000 SF, level 4)"),  # [ciego-ok] criterio genérico del estimador
    "joint_tape_lf_per_sf": (0.37, "Estimator yield, Inputs!B24 (370 LF per 1,000 SF)"),  # [ciego-ok] criterio genérico del estimador
    "framing_screws_per_stud": (4, "Estimator yield, Inputs!B21 (2 per stud-to-track connection at each end)"),
    "slab_pin_spacing_ft": (1.0, "Estimator criterion (Handoff - Approved: tightest of the three in the set, "
                                 "SILL TRACK ANCHORAGE interior @ 12\" O.C.)"),
    "anchor_spacing_ft": (8.0 / 12.0, "SILL TRACK ANCHORAGE exterior walls @ 8\" O.C. (stud schedule)"),
    "parapet_paf_spacing_ft": (1.0, "Parapet infill: PAFs SPACED AT 12\" O.C. MAX to the steel beam"),
    "header_bearing_ft": (8.0 / 12.0, "Estimator decision #1: R.O. + 1'-4\" (8\" bearing each side)"),
    "addl_head_track_min_ro_ft": (4.0, "HEAD TRACK @ NON LOAD BRG: ADD FULL LENGTH ADDL HEAD TRACK @ OPNG > 4'-0\""),
    "jamb_return_width_ft": (0.5, "Estimator criterion (return width = 6\" stud depth, not dimensioned; "
                                  "RFI with delta at 0.20 ft)"),  # [ciego-ok] criterio genérico del estimador
    "frp_inside_corners_per_room": (4, "Estimator criterion (4 inside corners per rectangular room)"),
}

BOARD_DRIVER = ("5/8\" gyp board regular (walls + ceilings)", "5/8\" gyp MOISTURE RESISTANT", "3/8\" gyp board")
STUD_FAMS = ("6\" stud", "3-5/8\" stud", "1-5/8\" stud", "6\" parapet stud", "2-1/2\" stud")
PEN_KINDS = ("duct", "fire_damper", "pipe", "mep", "duct_sleeve")
ON_SLAB = ("wall", "column_wrap", "pier", "chase")  # bottom track sobre losa (pins / anchors); v71: chase apoya en losa
NOT_ON_SLAB = ("door_bulkhead", "vestibule_head", "grille_head", "roof_step", "parapet", "fascia_box",
               "ceiling_transition", "ceiling_bulkhead", "soffit_side", "canopy_soffit", "storefront_cripples")


def k(data, key):
    """(valor, fuente) de constants o del default del estimador."""
    c = (data.get("constants") or {}).get(key)
    if isinstance(c, dict) and "value" in c:
        if not str(c.get("source") or "").strip():
            raise ValueError(f"constants.{key} sin source")
        return c["value"], c["source"]
    if key not in DEFAULTS:
        raise KeyError(key)
    return DEFAULTS[key]


def src(o, ctx):
    s = o.get("source")
    if isinstance(s, dict):
        s = s.get("source")
    if not str(s or "").strip():
        raise ValueError(f"{ctx}: sin source (N/HOJA)")
    return s


def es_exterior(w):
    t = str(w.get("tag") or "").upper()
    return t.startswith("EXT") or w.get("location") == "exterior" or w.get("exterior") is True


class Out:
    def __init__(self):
        self.fam = {f: 0.0 for f in FAMS}
        self.estado = {f: None for f in FAMS}
        self.filas, self.avisos, self.rfis = [], [], []

    def add(self, f, v, estado, source, op, **kw):
        self.fam[f] += v
        orden = ("PENDIENTE", "RFI", "CRITERIO", "DERIVADO", "CONFIRMADO")
        cur = self.estado[f]
        if cur is None or orden.index(estado) < orden.index(cur):
            self.estado[f] = estado
        d = {"familia": f, "valor": round(v, 2), "unidad": UNIDAD[f], "estado": estado, "source": source,
             "operacion": op}
        d.update(kw)
        self.filas.append(d)

    def pend(self, f, motivo):
        self.estado[f] = "PENDIENTE"
        self.avisos.append(f"PENDIENTE {f}: {motivo}")
        self.filas.append({"familia": f, "valor": 0.0, "unidad": UNIDAD[f], "estado": "PENDIENTE",
                           "source": "-", "operacion": motivo})


# ---------------------------------------------------------------- reglas por familia

def additional_head_track(data, o):
    """2/S5.20: abertura > 4'-0" en wall de studs = head track adicional a todo lo largo (R.O. + bearing x 2).
    Solo walls[].openings (door/window con jambs en el wall). openings_extra (continuous run, BOX HEADER AS
    NEEDED, grille, storefront, ductos) tienen su propio box detallado: van al RFI con su delta."""
    mn, smn = k(data, "addl_head_track_min_ro_ft")
    b, sb = k(data, "header_bearing_ft")
    n = 0
    for w in data.get("walls") or []:
        for op in w.get("openings") or []:
            if str(op.get("kind", "door")) not in ("door", "window"):
                continue
            ro = float(op["ro_w_ft"])
            if ro <= mn + EPS:
                continue
            q = int(op.get("qty", 1))
            lf = (ro + 2 * b) * q
            n += 1
            o.add(F_AHT, lf, "CRITERIO", f"{smn}; {sb}",
                  f"{op['ref']} ({w['id']}): ({ro} + 2 x {round(b, 3)}) x {q} = {round(lf, 2)}")
    delta = 0.0
    det = []
    for op in data.get("openings_extra") or []:
        if str(op.get("kind")) in PEN_KINDS or str(op.get("structure") or "").upper() in ("HSS", "STEEL"):
            continue
        ro = float(op.get("ro_w_ft") or 0)
        if ro > mn + EPS:
            q = int(op.get("qty") or 1)
            delta += (ro + 2 * b) * q
            det.append(op["ref"])
    if delta > EPS:
        o.rfis.append({"familia": F_AHT, "tema": "openings with their own box (openings_extra) > 4'-0\": do they "
                       "also take the additional head track of 2/S5.20?", "delta": round(delta, 2),
                       "unidad": "lf", "items": det})
    if n == 0 and delta <= EPS:
        o.add(F_AHT, 0.0, "DERIVADO", smn, "no openings > 4'-0\" in stud walls")


def penetraciones(data, fo):
    out = []
    for w in data.get("walls") or []:
        for op in w.get("openings") or []:
            if str(op.get("kind")) in PEN_KINDS:
                out.append({"ref": op["ref"], "wall": w["id"], "oc_in": w.get("oc_in", 16),
                            "width_in": float(op.get("width_in") or float(op["ro_w_ft"]) * 12),
                            "qty": int(op.get("qty", 1)), "source": op.get("source") or "walls[].openings"})
    for op in data.get("openings_extra") or []:
        if str(op.get("kind")) in PEN_KINDS:
            out.append({"ref": op["ref"], "wall": op.get("wall"), "oc_in": 16,
                        "width_in": float(op.get("width_in") or float(op["ro_w_ft"]) * 12),
                        "qty": int(op.get("qty") or 1), "source": op.get("source") or "openings_extra"})
    for p in data.get("mep_penetrations") or []:
        if p.get("width_in") is None and p.get("dia_in") is None:
            raise ValueError(f"mep_penetrations {p.get('ref')}: width_in o dia_in")
        out.append({"ref": p["ref"], "wall": p.get("wall"), "oc_in": p.get("oc_in", 16),
                    "width_in": float(p["width_in"] if p.get("width_in") is not None else p["dia_in"]),
                    "dia_in": p.get("dia_in"), "studs_cut": p.get("studs_cut"), "xy": p.get("xy"),
                    "in_cavity": p.get("in_cavity"), "in_cavity_source": p.get("in_cavity_source"),
                    "method": p.get("method"), "kind": p.get("kind"),
                    "qty": int(p.get("qty", 1)), "source": src(p, p["ref"]), "_mp": True})
    # v72 (R72.5): un FD de walls[].openings / openings_extra que el barrido (mep_penetrations) ya trae con el mismo
    # tamaño WxH es el mismo fire damper: se cuenta una vez (la del barrido, que trae xy).
    fd_mp = Counter(_tam(p["ref"]) for p in data.get("mep_penetrations") or []
                    if re.match(r"(?i)^\s*(FD|fire damper)", str(p.get("ref"))) and _tam(p.get("ref")))
    sal = []
    for p in out:
        t = _tam(p["ref"])
        if not p.get("_mp") and t and fd_mp[t] > 0 and re.match(r"(?i)^\s*(FD|fire damper)", str(p["ref"])):
            fd_mp[t] -= 1
            continue
        sal.append(p)
    out[:] = sal
    vistos = {str(p["ref"]) for p in out}
    # v72 (R72.5, arbitraje #20): el mismo fire damper listado en el opening_schedule ("FD-n ... WxH") y en el
    # barrido (mep_penetrations "FD ... 14x14") se contaba dos veces: se descuenta por tamaño (multiconjunto WxH).
    fd_barrido = Counter(_tam(p["ref"]) for p in out if re.match(r"(?i)^\s*(FD|fire damper)", str(p["ref"])) and _tam(p["ref"]))
    for it in (data.get("opening_schedule") or {}).get("items") or []:
        r = str(it.get("ref"))
        es_fd = it.get("kind") == "fire_damper" or re.match(r"(?i)^\s*(FD|fire damper)", r)
        if r not in vistos and es_fd and (it.get("in_mep_penetrations") or fd_barrido[_tam(r)] > 0):
            if not it.get("in_mep_penetrations"):
                fd_barrido[_tam(r)] -= 1
            continue
        if r not in vistos and (str(it.get("kind")) in PEN_KINDS or re.match(r"(?i)^(FD|fire damper|duct)\b", r)):
            out.append({"ref": r, "wall": it.get("wall"), "oc_in": 16, "width_in": _ancho_ref(it),
                        "qty": int(it.get("qty", 1)), "source": it.get("source") or "opening_schedule"})
    for it in (fo or {}).get("items") or []:
        if it.get("location") == "wall" and it.get("category") not in ("access_panel",):
            out.append({"ref": it.get("tag"), "wall": it.get("wall"), "oc_in": 16,
                        "width_in": float(it.get("width_in") or 0), "qty": int(it.get("qty", 1)),
                        "source": it.get("source") or "fo_in"})
    return out


def _tam(ref):
    m = re.search(r"(\d+)\s*[xX×]\s*(\d+)", str(ref))
    return f"{m.group(1)}x{m.group(2)}" if m else None


def _ancho_ref(it):
    """Ancho de una penetración listada solo por ref en opening_schedule ("FD 10x10 ...") -> 10 in."""
    if it.get("width_in"):
        return float(it["width_in"])
    m = re.search(r"(\d+)\s*x\s*(\d+)", str(it.get("ref")))
    return float(m.group(1)) if m else 0.0


def _registro(sw):
    """v68: barrido P/M REGISTRADO (registro2 / mep.py: offset por votación de segmentos de muro, >= 25
    coincidentes). Sin registro, o con fuente "visual", la lista de penetraciones no es reproducible."""
    reg = sw.get("registro")
    if not isinstance(reg, dict):
        return "mep_sweep sin registro {dx_pt, dy_pt, matches, source} (registro2.py / mep.py contra el plano de walls)"
    for kk in ("dx_pt", "dy_pt", "matches"):
        if reg.get(kk) is None:
            return f"mep_sweep.registro sin {kk}"
    if int(reg["matches"]) < 25:
        return f"mep_sweep.registro con {reg['matches']} coincidencias (< 25): sin registro verificado no se cruza"
    if not str(reg.get("source") or "").strip():
        return "mep_sweep.registro sin source"
    return None


def stud_reinforcement(data, fo, o):
    """Detalle estructural de penetración en studs (N/HOJA): plate de refuerzo en cada penetración, flanges no se cortan.
    pcs = Σ qty x studs cortados; studs cortados = MAX(1, ROUNDUP(ancho / O.C.)). Los ductos / fire dampers NO se
    enmarcan (decisión #12: sin header ni sill) pero el stud que cortan sí lleva su plate.
    v68: barrido REGISTRADO obligatorio (mep_sweep.registro); ninguna fuente "visual"; cada penetración una sola vez
    por (wall, xy); pipe que corre DENTRO de la cavidad sin cruzar stud (in_cavity + source) = 0 plates."""
    sw = data.get("mep_sweep")
    if not isinstance(sw, dict) or not str(sw.get("source") or "").strip():
        o.pend(F_REINF, "no mep_sweep {sheets, source, registro}: sweep ALL P and M sheets (pipes, ducts, "
                        "conduit > web hole) against the stud walls and declare mep_penetrations; 6/S5.20")
        return
    hs = [str(h).upper() for h in sw.get("sheets") or []]
    if not any(re.match(r"^(\w+/)?P\d", h) for h in hs) or not any(re.match(r"^(\w+/)?M\d", h) for h in hs):
        raise ValueError("mep_sweep.sheets debe incluir hojas P* y M* (pipes y ductos que cruzan walls; 6/S5.20)")
    if VISUAL_RE.search(str(sw.get("source"))):
        raise ValueError("mep_sweep.source dice lectura visual: el barrido va registrado (registro2.py / mep.py), v68")
    falta = _registro(sw)
    if falta:
        o.pend(F_REINF, falta + "; 6/S5.20")
        return
    pens = penetraciones(data, fo)
    if not pens:
        o.add(F_REINF, 0.0, "DERIVADO", sw["source"], f"registered sweep {hs}: no penetrations in stud walls")
        return
    vistos = set()
    rows_de = {str(w.get("id")): w.get("rows", 1) for w in data.get("walls") or []}
    delta_rows = 0
    fuera = {"manual": [], "pipe": [], "otros": []}      # v73 (R73.5): fuera de la familia, a RFI con su delta
    for p in pens:
        if VISUAL_RE.search(str(p.get("source"))):
            raise ValueError(f"{p['ref']}: penetración con fuente visual; va con xy del barrido registrado (v68)")
        if p.get("xy") is not None:
            key = (str(p.get("wall")), tuple(round(float(v), 1) for v in p["xy"]))
            if key in vistos:
                raise ValueError(f"{p['ref']}: penetración repetida en {key} (una vez por cruce, usar qty)")
            vistos.add(key)
        if p.get("in_cavity"):
            if not str(p.get("in_cavity_source") or "").strip():
                raise ValueError(f"{p['ref']}: in_cavity sin in_cavity_source (detalle que la deja en la cavidad)")
            o.add(F_REINF, 0, "DERIVADO", f"6/S5.20; {p['in_cavity_source']}",
                  f"{p['ref']}: runs inside the wall cavity, crosses no stud = no plate")
            continue
        if p.get("dia_in") is not None and float(p["dia_in"]) <= 1.0 + EPS:
            o.add(F_REINF, 0, "DERIVADO", f"6/S5.20; {p['source']}",
                  f"{p['ref']}: dia {p['dia_in']}\" <= 1\" centered in web = no plate")
            continue
        sc = p.get("studs_cut")
        rows = int((rows_de.get(str(p.get("wall"))) or 1))
        n_alt = int(sc["value"]) * p["qty"] if isinstance(sc, dict) else \
            max(1, math.ceil(p["width_in"] / float(p["oc_in"]) - EPS)) * rows * p["qty"]
        # v73 (R73.5, arbitraje #21): la familia es SOLO cruces de ducto que da mep.cruces. Un cruce manual, un pipe
        # > 1" (plate del detalle de penetración) o un ducto / fire damper de otra lista va a RFI con su delta.
        clase = None
        if not p.get("_mp") or str(p.get("method") or "") != "mep.cruces":
            clase = "manual" if p.get("_mp") else "otros"
        elif str(p.get("kind") or "duct") not in ("duct", "duct_sleeve"):
            clase = "pipe"
        if clase:
            fuera[clase].append((p["ref"], n_alt))
            o.add(F_REINF, 0, "CRITERIO", f"6/S5.20; {p['source']}",
                  f"{p['ref']}: not a duct crossing from mep.cruces = 0 in the family (R73.5); RFI +{n_alt}")
            continue
        if isinstance(sc, dict):
            n = int(sc["value"])
            src(sc, f"{p['ref']}.studs_cut")         # override con su fuente; sin él lo calcula la tool (R72.9)
            v = n * p["qty"]
            op = f"{p['ref']}: {p['qty']} x studs_cut {n} = {v}"
        else:
            # v72 (R72.9): studs cortados = MAX(1, ROUNDUP(ancho / O.C.)) por fila de studs del wall (double row = 2)
            n = max(1, math.ceil(p["width_in"] / float(p["oc_in"]) - EPS))
            v = n * rows * p["qty"]
            delta_rows += n * (rows - 1) * p["qty"]
            op = (f"{p['ref']}: {p['qty']} x MAX(1, ROUNDUP({round(p['width_in'], 2)}/{p['oc_in']})) x {rows} row(s) "
                  f"= {v}")
        o.add(F_REINF, v, "CRITERIO", f"6/S5.20; {p['source']}", op)
    if delta_rows:
        o.rfis.append({"familia": F_REINF, "tema": "plates at double-row stud walls: one per cut row (R72.9) vs one "
                       "per crossing", "delta": -delta_rows, "unidad": "pcs",
                       "alternativa": "one plate per crossing even when the wall has two stud rows"})
    temas = {"manual": "crossings read by hand (not found by mep.cruces): confirm each one on the M / P sheets",
             "pipe": "pipes over 1 in. through the stud web: the penetration detail draws a plate",
             "otros": "duct / fire damper openings listed outside the registered MEP sweep"}
    for k, lst in fuera.items():
        if lst:
            o.rfis.append({"familia": F_REINF, "tema": f"{temas[k]} (R73.5)", "delta": sum(v for _, v in lst),
                           "unidad": "pcs", "items": [r for r, _ in lst][:40],
                           "alternativa": "add them to the stud reinforcement count"})


ATM_VIEJOS = ("width_ft", "width_source", "width_status", "sistered_h_ft", "sistered_h_source", "sistered_h_status",
              "furring_rows", "furring_rows_source", "furring_rows_status", "alternativas")


def atm_recess_valido(op, ctx=None):
    """v77c (decisión del usuario U1, R77.11): el framing de un recess de ATM / equipo empotrado está en la wall que
    lo contiene (su partition type lleva todo su metal); el renglón "extra framing ATM" = 0. El bloque atm_recess
    declara la fuente impresa {source N/HOJA del detalle que llama el ATM sobre esa wall, drawn: texto rotulado}.
    Si un detalle impreso pide EXPLÍCITAMENTE framing adicional en el recess (studs sistered, furring, blocking...),
    se declara extra_printed {source N/HOJA, text (lo impreso, literal), lf, op}: NO se suma en silencio, sale como
    RFI con su delta para el estimador. La fórmula vieja (width_ft / sistered_h_ft / furring_rows / alternativas) es
    error."""
    ar = op.get("atm_recess")
    ctx = ctx or str(op.get("ref"))
    viejos = [k for k in ATM_VIEJOS if k in (ar or {})]
    if viejos:
        raise ValueError(f"{ctx}.atm_recess: {', '.join(viejos)} ya no existen (U1 v77c: el framing del recess está en "
                         f"la wall que lo contiene; extra framing ATM = 0). Declarar atm_recess {{source N/HOJA, drawn}} "
                         f"y, solo si un detalle impreso lo pide, extra_printed {{source, text, lf, op}}")
    s = src(ar, f"{ctx}.atm_recess")
    if not NHOJA.search(str(s)):
        raise ValueError(f"{ctx}.atm_recess.source debe citar el detalle N/HOJA del ATM")
    if not str(ar.get("drawn") or "").strip():
        raise ValueError(f"{ctx}.atm_recess.drawn: el texto que el detalle rotula en el recess (U1 v77c)")
    ep = ar.get("extra_printed")
    if ep is not None:
        if not isinstance(ep, dict) or not NHOJA.search(str(ep.get("source") or "")):
            raise ValueError(f"{ctx}.atm_recess.extra_printed: source N/HOJA del detalle impreso que lo pide (U1)")
        if not EXTRA_IMPRESO.search(str(ep.get("text") or "")):
            raise ValueError(f"{ctx}.atm_recess.extra_printed.text: el texto impreso literal que pide framing adicional "
                             f"(STUD / SISTERED / FURRING / BLOCKING / TRACK...); sin texto impreso no hay extra (U1)")
        if not isinstance(ep.get("lf"), (int, float)) or float(ep["lf"]) <= 0 or not str(ep.get("op") or "").strip():
            raise ValueError(f"{ctx}.atm_recess.extra_printed: lf > 0 con su operación escrita (op) (U1)")
    return s


EXTRA_IMPRESO = re.compile(r"\b(STUDS?|SISTERED|FURRING|BLOCKING|TRACK|RUNNER|CHANNEL|FRAMING|BACKING|KING|JACK)\b",
                           re.I)


def extra_framing(data, o):
    """Extra framing ATM (v77c, decisión del usuario U1, R77.11): el framing de un recess de ATM / equipo empotrado
    está en la wall que lo contiene; el renglón vale 0 (DERIVADO, con la fuente del detalle). canon.py verifica que
    esa wall esté en studs_nodos y corridas (su type lleva el metal) y deja data["_atm_wall"]. Lo que un detalle
    impreso pida explícitamente (extra_printed) sale como RFI con su delta; nunca se suma en silencio.
    extra_framing kind "atm_recess" o con ref ATM = error; kind "mep" de un ducto / FD = error (E12)."""
    hubo = False
    _atm_obligatorio(data)
    vistos = {str(x["ref"]): x for x in data.get("_atm_wall") or []}
    for w in data.get("walls") or []:
        for op in w.get("openings") or []:
            if not op.get("atm_recess"):
                continue
            s = atm_recess_valido(op, f"{w.get('id')} {op['ref']}")
            m = vistos.get(str(op["ref"]))
            if m is None:
                raise ValueError(f"{op['ref']}: atm_recess sin la verificación de canon.py (U1 v77c: accesorios.py corre "
                                 f"dentro de canon.calcular, que comprueba que la wall {w.get('id')} lleve su metal "
                                 f"en su type)")
            o.add(F_XATM, 0.0, "DERIVADO", s + "; " + str(w.get("source") or w.get("detail") or ""), m["op"])
            ep = op["atm_recess"].get("extra_printed")
            if ep:
                o.rfis.append({"familia": F_XATM, "tema": f"{op['ref']}: extra framing printed at the recess (U1)",
                               "delta": round(float(ep["lf"]), 2), "unidad": "lf",
                               "items": [f"{ep['source']}: \"{ep['text']}\"", str(ep["op"])],
                               "alternativa": "carry the printed extra framing (estimator decides; default 0)"})
            hubo = True
    for op in data.get("openings_extra") or []:
        if op.get("atm_recess"):
            raise ValueError(f"{op.get('ref')}: atm_recess en openings_extra: el ATM va en la wall que lo contiene "
                             f"(U1 v77c: su framing está en esa wall)")
    for it in data.get("extra_framing") or []:
        s = src(it, it.get("ref", "extra_framing"))
        if it.get("kind") == "atm_recess" or ATM_RE.search(str(it.get("ref"))):
            raise ValueError(f"{it.get('ref')}: extra_framing de ATM a mano (U1 v77c: el framing del recess está en "
                             f"la wall que lo contiene, extra framing ATM = 0; lo impreso va en "
                             f"atm_recess.extra_printed y sale como RFI)")
        if it.get("kind") == "mep" and DUCT_RE.search(str(it.get("ref"))):
            raise ValueError(f"{it.get('ref')}: extra framing de un ducto / FD (E12: no se enmarca; el plate va a "
                             f"stud reinforcement MEP), v68")
        lf = float(it["lf"]) if "lf" in it else int(it["pcs"]) * float(it["len_ft"])
        o.add(F_XATM, lf, it.get("estado", "DERIVADO"), s, f"{it['ref']} ({it.get('kind', 'other')}): "
              f"{round(lf, 2)} LF")
        hubo = True
    if not hubo:
        o.pend(F_XATM, "no atm_recess at the ATM opening and no extra_framing[]: declare atm_recess {source, drawn} "
                       "(U1: the recess framing is in the wall that contains it, extra = 0) or accesorios_none")


def _atm_obligatorio(data):
    """v67: una abertura ATM sin bloque de su recess = error (la familia salía PENDIENTE en silencio)."""
    ef = {str(x.get("ref")) for x in data.get("extra_framing") or [] if x.get("kind") == "atm_recess"}
    ops = [op for w in data.get("walls") or [] for op in w.get("openings") or []] + \
        list(data.get("openings_extra") or [])
    for op in ops:
        if not (str(op.get("kind")) == "atm" or ATM_RE.search(str(op.get("ref")))):
            continue
        if op.get("atm_recess") or str(op["ref"]) in ef:
            continue
        if str(op.get("atm_recess_none_reason") or "").strip():
            continue
        raise ValueError(f"{op['ref']}: abertura ATM sin atm_recess {{source N/HOJA, drawn}} ni atm_recess_none_reason "
                         f"(U1 v77c: el framing del recess está en la wall que lo contiene; extra framing ATM = 0)")


RX_CADENA = re.compile(r"\b(chain|cadena)\b", re.I)
RX_COTA_FT = re.compile(r"\d+'\s?-\s?\d+(?:\s+\d+/\d+)?\"")


def grille_head(data, o):
    """Coiling grille head: 2-1/2" CFMF @ O.C. ENTRE dos 6" CFMF BOX BEAM HEADER. Piezas = ROUNDUP(L/oc)+1;
    largo de cada stud = espacio libre entre los dos box beams = head impreso - box beams - board del soffit,
    NUNCA el alto total del head ni un "entre box beams" sin restar el board del soffit."""
    gh = [w for w in data.get("walls") or [] if w.get("element") == "grille_head"]
    if not gh:
        return
    for w in gh:
        oc = float(w.get("oc_in", 16)) / 12.0
        L = float(w["length_ft"])
        n = math.ceil(L / oc - EPS) + 1
        if isinstance(w.get("stud_len_ft"), dict):
            sl = float(w["stud_len_ft"]["value"])
            s = src(w["stud_len_ft"], f"{w['id']}.stud_len_ft")
            op = f"stud_len {sl}"
            est = "DERIVADO"
        elif isinstance(w.get("head_build"), dict):
            hb = w["head_build"]
            s = src(hb, f"{w['id']}.head_build")
            ch = hb.get("head_chain_in")
            if not isinstance(ch, list) or not ch or not all(isinstance(x, (int, float)) and x > 0 for x in ch):
                raise ValueError(f"{w['id']}.head_build sin head_chain_in [pulgadas]: TODOS los eslabones de la cadena "
                                 f"impresa del head (sobre y bajo el ceiling), no uno solo (v68)")
            # R70.9 (v70): si el detalle acota el head como CADENA (head_chain_source dice chain / cadena, o la fuente
            # cita >= 2 cotas pies-pulgadas), head_chain_in lista TODOS los eslabones (>= 2); uno solo = error
            txt = f"{hb.get('head_chain_source', '')} {hb.get('source', '')} {hb.get('note', '')}"
            cotas = set(RX_COTA_FT.findall(txt))
            if len(ch) < 2 and (RX_CADENA.search(str(hb.get("head_chain_source") or "")) or len(cotas) >= 2):
                raise ValueError(f"{w['id']}.head_build: el detalle acota el head como cadena "
                                 f"({', '.join(sorted(cotas)) or hb.get('head_chain_source')}) y head_chain_in trae un "
                                 f"solo eslabón {ch} — R70.9: listar todos los eslabones (stud = Σ cadena − n_box x "
                                 f"box_depth − board)")
            if abs(sum(ch) / 12.0 - float(hb["head_ft"])) > 1.0 / 192:
                raise ValueError(f"{w['id']}.head_build.head_ft {hb['head_ft']} != suma de head_chain_in {ch} = "
                                 f"{round(sum(ch) / 12.0, 4)} ft (v68)")
            sl = sum(ch) / 12.0 - int(hb.get("n_box", 2)) * float(hb["box_depth_ft"]) - \
                float(hb.get("board_in", 0)) / 12.0
            if sl <= EPS:
                raise ValueError(f"{w['id']}: stud del grille head <= 0 (head {hb['head_ft']} - box beams - board)")
            op = (f"stud_len = ({' + '.join(str(x) for x in ch)})/12 = {hb['head_ft']} - {hb.get('n_box', 2)} x "
                  f"{hb['box_depth_ft']} - {hb.get('board_in', 0)}/12 = {round(sl, 3)}")
            est = "DERIVADO"
        else:
            o.pend(F_GRILLE, f"{w['id']}: grille head without head_build {{head_ft, head_chain_in, box_depth_ft, n_box, "
                             f"board_in, source}} or stud_len_ft: the 2-1/2\" goes BETWEEN the two box beams (printed "
                             f"dimensions of the head detail; never height_ft)")
            continue
        lf = n * sl
        o.add(F_GRILLE, lf, est, s, f"{w['id']}: (ROUNDUP({L}/{round(oc, 3)})+1) = {n} x {op} = {round(lf, 2)}")


def jamb_return(data, o):
    """GYPSUM BOARD JAMB RETURN BEYOND (secciones de head / sill / jamb de ventanas y storefront). LF de bordes =
    la MISMA regla que el trim de canon.py (R.O. + 2 x head - 2 x sill + R.O. si hay sill); SF = LF x ancho del
    return (no acotado: criterio del estimador con RFI)."""
    wd, swd = k(data, "jamb_return_width_ft")
    _jr_declarado(data)
    _storefront_de_cripples(data)
    lf = 0.0
    det = []
    for w in data.get("walls") or []:
        for op in w.get("openings") or []:
            _sill_return(op)                              # v70: valida sill_return / source en toda abertura
            if op.get("jamb_return"):
                _label_gyp(op, "jamb_return_source", "jamb_return_label", "jamb / head")   # v75 R75.3
                e = _edge(op)
                lf += e
                det.append(f"{op['ref']} {round(e, 2)} [{op.get('jamb_return_source', '-')}]")
    for op in data.get("openings_extra") or []:
        _sill_return(op)
        if op.get("jamb_return"):
            _label_gyp(op, "jamb_return_source", "jamb_return_label", "jamb / head")   # v75 R75.3
            e = _edge(op)
            lf += e
            det.append(f"{op['ref']} {round(e, 2)} [{op.get('jamb_return_source', '-')}]")
    if lf <= EPS:
        o.pend(F_JR, "no opening with jamb_return: sweep the head / sill / jamb sections (GYPSUM BOARD "
                     "JAMB RETURN BEYOND) and mark jamb_return + jamb_return_source")
        return
    sf = lf * float(wd)
    o.add(F_JR, sf, "CRITERIO", swd, f"edges {round(lf, 2)} LF x {wd} ft = {round(sf, 2)} SF [{'; '.join(det)}]")
    o.rfis.append({"familia": F_JR, "tema": "jamb return width not dimensioned", "delta": round(lf * (0.2 - wd), 2),
                   "unidad": "sf", "alternativa": "0.20 ft (frame at mid-wall)"})  # [ciego-ok] criterio genérico del estimador


def _jr_declarado(data):
    """v67: toda abertura exterior declara si su sección dibuja GYPSUM BOARD JAMB RETURN (true / false + la
    sección leída). Así un borde no se pierde en silencio (ATM, storefront heads, jambs contra wall)."""
    ext = []
    for w in data.get("walls") or []:
        for op in w.get("openings") or []:
            if str(op.get("kind", "door")) in PEN_KINDS:
                continue
            if es_exterior(w) or op.get("location") == "exterior" or str(op.get("kind")) in ("window", "storefront",
                                                                                             "atm"):
                ext.append(op)
    for op in data.get("openings_extra") or []:
        if str(op.get("kind")) in ("storefront", "window", "atm") or op.get("location") == "exterior" or \
                ATM_RE.search(str(op.get("ref"))):
            ext.append(op)
    falta = [op["ref"] for op in ext if "jamb_return" not in op or not str(op.get("jamb_return_source") or "").strip()]
    if falta:
        raise ValueError(f"jamb return sin declarar en abertura(s) exterior(es) {falta}: jamb_return true|false + "
                         f"jamb_return_source (sección de head / sill / jamb que se leyó; v67)")
    for op in ext:
        if op.get("jamb_return") and str(op.get("kind")) == "storefront":
            if "wall_jambs" not in op and "jambs" not in op:
                raise ValueError(f"{op['ref']}: storefront con jamb return declara jambs [{{abuts: "
                                 f"{'|'.join(ABUTS)}, source}}] x 2 (v68; en un pier = 0)")
            if _wall_jambs(op) and op.get("head_ft") is None:
                raise ValueError(f"{op['ref']}: storefront con wall_jambs > 0 sin head_ft (alto del jamb = head de la "
                                 f"sección del storefront; v67)")


def _wall_jambs(op):
    """v68: cada uno de los DOS jambs del storefront declara contra qué remata (wall de gyp / pier / frame / none)
    con su N/HOJA; wall_jambs = cuántos rematan contra un wall de gyp. Una fuente que dice "wall/pier" no decide."""
    js = op.get("jambs")
    if js is None:
        raise ValueError(f"{op['ref']}: wall_jambs sin jambs [{{abuts, source}}] x 2 — cada jamb se lee por separado "
                         f"(v68: 'jambs contra wall/pier' no distingue)")
    if not isinstance(js, list) or len(js) != 2:
        raise ValueError(f"{op['ref']}: jambs debe listar los 2 jambs del storefront")
    for j in js:
        if j.get("abuts") not in ABUTS:
            raise ValueError(f"{op['ref']}: jamb abuts debe ser {'|'.join(ABUTS)}")
        if not NHOJA.search(str(j.get("source") or "")) and not re.search(r"[A-Z]\d{1,2}\.\d{2}", str(j.get("source"))):
            raise ValueError(f"{op['ref']}: jamb sin source (hoja / detalle donde se ve el remate)")
        if re.search(r"(?i)wall\s*/\s*pier|pier\s*/\s*wall", str(j.get("source"))):
            raise ValueError(f"{op['ref']}: source 'wall/pier' no decide el remate del jamb")
    n = sum(1 for j in js if j["abuts"] == "wall")
    if "wall_jambs" in op and int(op["wall_jambs"]) != n:
        raise ValueError(f"{op['ref']}: wall_jambs {op['wall_jambs']} != jambs contra wall {n}")
    return n


def _sill_return(op):
    """v70 (#18A): `sill_return: false` + `sill_return_source` N/HOJA = el detalle dibuja otra cosa en el sill
    (p. ej. brake metal): el return y su trim no llevan el borde del sill. El double sill track (headers.py) NO
    cambia: depende de with_sill. -> True si el sill lleva return."""
    if "sill_return" not in op:
        if op.get("jamb_return") and op.get("with_sill"):   # v75 (R75.3, #23A / #23B): nunca se asume el sill
            raise ValueError(f"{op.get('ref')}: jamb return con sill sin sill_return true|false + sill_return_source "
                             f"(lee el detalle del SILL: brake metal / solid sill / FRT plywood = false; R75.3)")
        return True
    v = op["sill_return"]
    if not isinstance(v, bool):
        raise ValueError(f"{op.get('ref')}: sill_return true|false (vino {v!r})")
    if v is False and not NHOJA.search(str(op.get("sill_return_source") or "")):
        raise ValueError(f"{op.get('ref')}: sill_return false sin sill_return_source N/HOJA (el detalle del sill que "
                         f"dibuja otro remate; v70)")
    if v is True and op.get("jamb_return"):
        _label_gyp(op, "sill_return_source", "sill_return_label", "sill")
    return v


GYP_RX = re.compile(r"\bGYP|\bGWB\b|GYPSUM", re.I)


def _label_gyp(op, k_src, k_lab, borde):
    """v75 (R75.3, arbitraje #23): un borde de jamb return suma solo si su detalle ROTULA gypsum board en el retorno.
    Se declara el texto impreso leído (label) y su N/HOJA; "LINE OF JAMB RETURN BEYOND" sin la palabra gypsum no
    basta (el borde puede ser frame sobre FRT plywood o brake metal)."""
    if not NHOJA.search(str(op.get(k_src) or "")):
        raise ValueError(f"{op.get('ref')}: {borde} con return de gyp sin {k_src} N/HOJA (R75.3)")
    lab = str(op.get(k_lab) or "").strip()
    if not lab:
        raise ValueError(f"{op.get('ref')}: {borde} con return de gyp sin {k_lab} (texto impreso del detalle que "
                         f"rotula el retorno; R75.3)")
    if not GYP_RX.search(lab):
        raise ValueError(f"{op.get('ref')}: {k_lab} '{lab[:60]}' no rotula gypsum board: ese borde no lleva return "
                         f"de gyp (jamb_return / sill_return false con la cita; R75.3)")


def _storefront_de_cripples(data):
    """v75 (R75.4, #23A): framing sobre / bajo un storefront (cripples, head) implica la abertura. Cada elemento
    storefront_cripples se empareja con un storefront declarado (opening_ref o mismo ancho ± 0.1 ft); si no, el
    storefront no se barrió y su jamb return / trim se pierde en silencio."""
    sf = [op for op in (data.get("openings_extra") or []) if str(op.get("kind")) == "storefront"] + \
         [op for w in data.get("walls") or [] for op in w.get("openings") or [] if str(op.get("kind")) == "storefront"]
    refs = {str(op.get("ref")) for op in sf}
    falta = []
    for w in (data.get("walls") or []) + (data.get("runs") or []):
        if w.get("element") != "storefront_cripples":
            continue
        if w.get("opening_ref") is not None:
            if str(w["opening_ref"]) not in refs:
                falta.append(f"{w.get('id')} (opening_ref {w['opening_ref']} no declarado)")
            continue
        lf = w.get("length_ft", w.get("lf"))
        if lf is None or not any(abs(float(op.get("ro_w_ft") or 0) - float(lf)) <= 0.1 for op in sf):
            falta.append(str(w.get("id")))
    if falta:
        raise ValueError(f"storefront_cripples sin storefront declarado {falta}: declara la abertura en openings_extra "
                         f"(kind storefront, ro_w_ft, head_ft, jamb_return + jamb_return_source + jambs) o "
                         f"opening_ref; R75.4")


def _edge(op):
    """Bordes del return. Ventana / door: R.O. + 2 jambs (head - sill) + sill si lo hay. Storefront: el return
    está en el HEAD (sección del head: "GYPSUM BOARD JAMB RETURN BEYOND") + solo los jambs que mueren contra un
    wall de gyp (wall_jambs); en un pier el board muere en el frame (detalles de plan del pier) -> 0.
    v70: with_sill + sill_return false (con sill_return_source) -> sin el borde del sill."""
    if str(op.get("kind")) == "storefront":
        nj = _wall_jambs(op)
        return float(op["ro_w_ft"]) + (nj * float(op["head_ft"]) if nj else 0.0)
    e = float(op["ro_w_ft"]) + 2 * float(op["head_ft"]) - 2 * float(op.get("sill_ft", 0) or 0)
    return e + (float(op["ro_w_ft"]) if op.get("with_sill") and _sill_return(op) else 0.0)


def pvc_trim(data, o):
    """FRP con PVC trim (detalles del toilet room): edge trim arriba + edge trim abajo (sobre el cove base) a todo
    el perímetro neto (el MISMO de tile_base / FRP) + inside corner molding (esquinas x top) + edge trim vertical
    donde el FRP muere en cada door frame (2 por door x top) + mop sink (inside corner, top edge, 2 vertical ends)."""
    fr = data.get("frp")
    if not fr:
        if str(data.get("frp_none_reason") or "").strip():
            o.add(F_PVC, 0.0, "DERIVADO", "frp_none_reason", data["frp_none_reason"])
        else:
            o.pend(F_PVC, "no frp block in the canon")
        return
    top = float(fr["top_ft"]["value"])
    ic_def, sic = k(data, "frp_inside_corners_per_room")
    tb = {str(t["room"]): t for t in data.get("tile_base") or []}
    for r in fr.get("rooms") or []:
        t = tb.get(str(r))
        if t is None:
            raise ValueError(f"frp room {r} sin tile_base")
        per = float(t["perimeter_ft"])
        if t.get("perimeter_basis") == "gross":       # v68: el mismo perímetro NETO que el FRP (canon _perim_neto)
            per = round(per - sum(float(x["ro_w_ft"]) for x in t.get("doors") or []), 3)
        ic = t.get("inside_corners")
        if isinstance(ic, dict):
            nic, sc, est = int(ic["value"]), src(ic, f"tile_base {r}.inside_corners"), "DERIVADO"
            # v68 (#16A y #16B contaron distinto el mismo cuarto con notch): polígono rectilíneo del FRP -> inside (90°) +
            # outside (270°) = vértices e inside - outside = 4. Un outside corner NO es inside corner trim.
            nv, no_ = ic.get("vertices"), ic.get("outside_corners")
            if nv is None or no_ is None:
                raise ValueError(f"tile_base {r}.inside_corners sin vertices / outside_corners del polígono (v68)")
            if nic + int(no_) != int(nv) or nic - int(no_) != 4:
                raise ValueError(f"tile_base {r}: inside {nic} + outside {no_} != vertices {nv} o inside - outside "
                                 f"!= 4 (polígono rectilíneo; v68)")
            nic, sc = _jogs_frp(r, ic, nic, int(nv), sc, top, o)
        else:
            nic, sc, est = int(ic_def), sic, "CRITERIO"
        nd = len(t.get("doors") or [])
        lf = 2 * per + nic * top + 2 * nd * top
        o.add(F_PVC, lf, est, f"{fr['top_ft']['source']}; {sc}",
              f"room {r}: edge top+bottom 2 x {per} + inside corners {nic} x {top} + door jambs 2 x {nd} x {top} "
              f"= {round(lf, 2)}")
    ms = fr.get("mop_sink")
    if ms:
        s = src(ms, "frp.mop_sink")
        sides, wdt, h = int(ms["sides"]), float(ms["width_ft"]), float(ms["height_ft"])
        lf = max(0, sides - 1) * h + sides * wdt + 2 * h
        o.add(F_PVC, lf, "DERIVADO", s, f"mop sink: inside corner {max(0, sides - 1)} x {h} + top edge {sides} x "
              f"{wdt} + vertical ends 2 x {h} = {round(lf, 2)}")


JOG_TRIM_MIN_IN = 6.0     # v72 (R72.10): un jog del polígono del FRP de menos de 6" no lleva inside corner trim


def _jogs_frp(r, ic, nic, nv, sc, top, o):
    """v72 (R72.10, arbitraje #20: dos corridas contaron 4 y 7 inside corners en el mismo cuarto): con más de 4
    vértices, inside_corners.jogs [{depth_in, kind: notch|step, source}] es obligatorio (notch = 4 vértices: 2 inside
    + 2 outside; step = 2 vértices: 1 + 1). Un jog con depth_in < JOG_TRIM_MIN_IN (carrier, espesor de acabado) no
    agrega inside corners: se descuenta y queda RFI con el delta. -> (inside corners, fuente)."""
    if nv <= 4:
        return nic, sc
    jogs = ic.get("jogs")
    if not isinstance(jogs, list) or not jogs:
        o.avisos.append(f"tile_base {r}.inside_corners con {nv} vértices sin jogs [{{depth_in, kind, source}}] "
                        f"(R72.10: la compuerta chequeos_v72 lo rechaza)")
        return nic, sc
    extra = 0
    for j in jogs:
        kind = str(j.get("kind"))
        if kind not in ("notch", "step") or j.get("depth_in") is None:
            raise ValueError(f"tile_base {r}.inside_corners.jogs: kind notch|step y depth_in obligatorios ({j})")
        src(j, f"tile_base {r}.inside_corners.jogs")
        extra += 4 if kind == "notch" else 2
    if 4 + extra != nv:
        raise ValueError(f"tile_base {r}: 4 + vértices de los jogs ({extra}) != vertices {nv} (R72.10)")
    quita = sum(2 if j["kind"] == "notch" else 1 for j in jogs if float(j["depth_in"]) < JOG_TRIM_MIN_IN)
    if quita:
        o.rfis.append({"familia": F_PVC, "tema": f"room {r}: {quita} inside corner(s) at jogs < {JOG_TRIM_MIN_IN:g}\" "
                       f"without PVC trim (R72.10)", "delta": round(quita * top, 2), "unidad": "lf",
                       "alternativa": "trim at every vertex of the polygon"})
    return nic - quita, f"{sc}; jogs < {JOG_TRIM_MIN_IN:g}\" without trim (R72.10)" if quita else sc


def _runs_parapet(par):
    """v71 (A7, arbitraje #19): los walls de parapet del mismo run (misma `run` / `run_id`, o colineales y contiguos
    por `band`) suman su largo antes del ROUNDUP; sin dato de run, cada wall es su run. -> [(ids, L)]."""
    import particion
    grupos, sueltos = {}, []
    for w in par:
        rid = w.get("run") or w.get("run_id")
        if rid:
            grupos.setdefault(("R", str(rid)), []).append(w)
        else:
            sueltos.append(w)
    out = [([str(x.get("id", x.get("ref"))) for x in ws], sum(float(x["length_ft"]) for x in ws))
           for ws in grupos.values()]
    con_band = [dict(w, id=str(w.get("id", w.get("ref")))) for w in sueltos if particion.geo(w) is not None]
    sin_band = [w for w in sueltos if particion.geo(w) is None]
    if con_band:
        for t in particion._tramos(con_band, 18.0, particion.TOL_LINE_FT, particion.TOL_GAP_FT):
            out.append((t["ids"], t["lf"]))
    out += [([str(w.get("id", w.get("ref")))], float(w["length_ft"])) for w in sin_band]
    return out


def pafs(data, fo, o):
    """Parapet infill: bottom track al steel beam con PAFs @ 12" O.C. MAX -> por run ROUNDUP(L / sp); + duct
    sleeves = una por penetración de ducto / fire damper en wall."""
    sp, ssp = k(data, "parapet_paf_spacing_ft")
    par = [w for w in data.get("walls") or [] if w.get("element") == "parapet"] + \
          [r for r in data.get("runs") or [] if r.get("element") == "parapet"]
    tot = 0
    det = []
    for ids, L in _runs_parapet(par):                # v71 (A7): ROUNDUP por RUN, no por wall
        n = math.ceil(L / float(sp) - EPS)
        tot += n
        det.append(f"{'+'.join(ids)} ROUNDUP({round(L, 3)}/{sp})={n}")
    if par:
        o.add(F_PAF, tot, "DERIVADO", ssp, f"PAFs parapet: {'; '.join(det)} = {tot}")
    duc = [p for p in penetraciones(data, fo) if _es_ducto(p)]
    ns = sum(p["qty"] for p in duc)
    if ns:
        o.add(F_PAF, ns, "DERIVADO", "; ".join(sorted({str(p["source"]) for p in duc})),
              "duct sleeves = " + " + ".join(f"{p['ref']} x{p['qty']}" for p in duc) + f" = {ns}")
    if not par and not ns:
        o.add(F_PAF, 0.0, "DERIVADO", "-", "no parapet and no ducts in walls")


def _es_ducto(p):
    r = str(p["ref"]).lower()
    return any(x in r for x in ("fd", "duct", "damper", "sleeve"))


def access_panels(data, fo, o):
    """Access panels = access_panels[] del canon (key note del RCP / notas M-P). v68: si el canon los declara, los
    items fo_in category access_panel son el MISMO panel visto desde framed_openings (su framing) y no se suman otra
    vez; solo si el canon no declara ninguno se cuentan los de fo_in. Diferencia de conteo = aviso."""
    n = 0
    canon_ap = data.get("access_panels") or []
    for it in canon_ap:
        o.add(F_AP, int(it.get("qty", 1)), "CONFIRMADO", src(it, it["ref"]), it["ref"])
        n += int(it.get("qty", 1))
    fo_ap = [it for it in (fo or {}).get("items") or [] if it.get("category") == "access_panel"]
    nfo = sum(int(it.get("qty", 1)) for it in fo_ap)
    if canon_ap:
        if fo_ap and nfo != n:
            o.avisos.append(f"access panel: canon {n} vs fo_in {nfo} (cuenta el canon; revisar el barrido)")
    else:
        for it in fo_ap:
            o.add(F_AP, int(it.get("qty", 1)), "CONFIRMADO", it.get("source", "fo_in"), f"{it.get('tag')}")
            n += int(it.get("qty", 1))
    if n == 0:
        o.pend(F_AP, "no access panels declared (access_panels[] or fo_in category access_panel): sweep the RCP "
                     "key notes and the M / P notes for access panels in GWB")


def board_yields(data, fam, o):
    """Drywall screws, joint compound, joint tape = yield x board driver (5/8" regular + MR + 3/8"), igual que la
    referencia (sin exterior sheathing, glass mat, ballistic, FRT, jamb return)."""
    drv = sum(float(fam.get(b, 0) or 0) for b in BOARD_DRIVER)
    if drv <= EPS:
        for f in (F_DWS, F_JC, F_JT):
            o.pend(f, "board driver = 0")
        return
    det = " + ".join(f"{round(float(fam.get(b, 0) or 0), 2)}" for b in BOARD_DRIVER)
    for f, key in ((F_DWS, "drywall_screws_per_sf"), (F_JC, "joint_compound_lb_per_sf"),
                   (F_JT, "joint_tape_lf_per_sf")):
        y, s = k(data, key)
        v = float(y) * drv
        o.add(f, v, "DERIVADO", s, f"{y} x ({det} = {round(drv, 2)} SF) = {round(v, 2)}")


PIEZAS_RE = (re.compile(r"=\s*(\d+)\s+studs"), re.compile(r"=\s*(\d+)\s+x\s+H"),
             re.compile(r"(\d+)\s+studs\s+dibujados"), re.compile(r"^(\d+)\s+jambs\s+x"),
             re.compile(r"cripples FLOOR\([^)]*\)\s*=\s*(\d+)\s+x"))


def piezas(fam_out, studs_out):
    """Piezas de stud instaladas: studs_nodos (pcs_full + cripples por wall) + filas de canon (parapet por bay,
    column wraps, jambs / cripples entre walls, studs verticales de transición). Joists de ceilings / canopy NO
    (mismo driver que la referencia)."""
    n = 0
    det = []
    if studs_out:
        for w in studs_out.get("walls") or []:
            n += int(w.get("pcs_full", 0)) + int(w.get("cripples", 0))
        det.append(f"studs_nodos {n}")
    for r in fam_out.get("filas") or []:
        fl = str(r.get("familia"))
        if not (any(fl.startswith(s) for s in STUD_FAMS) or fl.startswith("vertical studs")):
            continue
        if r.get("pcs") is not None:                  # v67: conteo explícito de canon.py
            n += int(r["pcs"])
            det.append(f"{r.get('ref') or r.get('run') or r.get('wall')} {int(r['pcs'])}")
            continue
        op = str(r.get("operacion") or "")
        for rx in PIEZAS_RE:
            m = rx.search(op)
            if m:
                n += int(m.group(1))
                det.append(f"{r.get('ref') or r.get('run') or r.get('wall')} {m.group(1)}")
                break
    return n, det


def framing_screws(data, fam_out, studs_out, o):
    y, s = k(data, "framing_screws_per_stud")
    if not studs_out:
        o.avisos.append("framing screws sin studs_out.json: faltan las piezas de walls de studs_nodos")
    n, det = piezas(fam_out, studs_out)
    if n == 0:
        o.pend(F_FS, "no stud pieces (pass --studs studs_out.json)")
        return
    v = int(y) * n
    o.add(F_FS, v, "DERIVADO", s, f"{y} x {n} stud pieces [{'; '.join(det[:12])}{' ...' if len(det) > 12 else ''}]"
          f" = {v}")


def track_slab(data, sin_fuente=None):
    """Bottom track sobre losa por wall (sin descuento de doors, decisión #10): L x rows.
    v72 (R72.8 = R71.15 como tool, arbitraje #20): expansion anchors solo para element "wall" exterior (lo que nombra
    el schedule de anclaje: "exterior walls"). Un column_wrap / chase exterior va con los pins (criterio del
    estimador) salvo `anchorage {value: anchors|pins, source N/HOJA}`; la parte sin tag de un box (R72.3) no entra en
    ninguno sin `anchorage`: va a `sin_fuente` (RFI con delta)."""
    import chequeos_v72
    partes = chequeos_v72.partes_de_box(data.get("walls") or [])
    inte, ext = [], []
    for w in data.get("walls") or []:
        el = w.get("element", "wall")
        if el in NOT_ON_SLAB or el not in ON_SLAB:
            continue
        lf = float(w["length_ft"]) * int(w.get("rows", 1))
        an = w.get("anchorage")
        if isinstance(an, dict) and an.get("value") in ("anchors", "pins"):
            if not NHOJA.search(str(an.get("source") or "")):
                raise ValueError(f"{w['id']}.anchorage sin source N/HOJA")
            (ext if an["value"] == "anchors" else inte).append((w["id"], lf))
            continue
        if w["id"] in partes:
            if sin_fuente is not None:
                sin_fuente.append((w["id"], lf))
            continue
        (ext if es_exterior(w) and el == "wall" else inte).append((w["id"], lf))
    return inte, ext


def pins_anchors(data, o):
    sp, ssp = k(data, "slab_pin_spacing_ft")
    sa, ssa = k(data, "anchor_spacing_ft")
    sinf = []
    inte, ext = track_slab(data, sinf)
    if sinf:
        lsf = sum(x[1] for x in sinf)
        o.rfis.append({"familia": F_ANCH, "tema": "untagged parts of piers / boxes (" + ", ".join(x[0] for x in sinf)
                       + ") without anchorage in the schedule (R72.8)", "delta": round(lsf / float(sa), 2), "unidad": "pcs",
                       "alternativa": "carry them as exterior walls (expansion anchors)"})
    li = sum(x[1] for x in inte)
    le = sum(x[1] for x in ext)
    if li > EPS:
        v = li / float(sp)
        o.add(F_PINS, v, "DERIVADO", ssp, f"interior bottom track on slab {round(li, 2)} LF ({len(inte)} walls, "
              f"x rows) / {sp} = {round(v, 2)}")
        o.rfis.append({"familia": F_PINS, "tema": "pin spacing: 12\" (interior anchorage) vs 16\" (fastener "
                       "schedule) vs 24\" (type K box)", "delta_16in": round(li / (16 / 12) - v, 2),
                       "delta_24in": round(li / 2.0 - v, 2), "unidad": "pcs"})
    else:
        o.pend(F_PINS, "no interior bottom track on slab")
    if le > EPS:
        v = le / float(sa)
        o.add(F_ANCH, v, "DERIVADO", ssa, f"exterior bottom track on slab {round(le, 2)} LF ({len(ext)} walls) "
              f"/ {round(float(sa), 4)} = {round(v, 2)}")
    else:
        o.add(F_ANCH, 0.0, "DERIVADO", ssa, "no exterior walls on slab")


def level5(data, o):
    """Level 5 = Σ caras con wall covering cuyo schedule dice LEVEL 5: L x (alto del acabado - base). Si el canon
    declara constants.level5_tags, cada tag debe tener al menos un item (si no -> aviso FALTA)."""
    items = data.get("level5_items") or []
    for it in items:
        s = src(it, it.get("ref", "level 5"))
        if "sf" in it:
            sf = float(it["sf"])
            op = f"{sf} SF"
        else:
            h = float(it["h_ft"])
            b = it.get("base_ft")
            if not isinstance(b, dict):
                raise ValueError(f"Level 5 {it.get('ref')}: base_ft {{value, source}} obligatorio (key note de la "
                                 f"base, ej. 'bottom of WC above wall base'; 0 con source si no hay base; v67)")
            src(b, f"{it.get('ref')}.base_ft")
            bv = float(b["value"])
            sf = float(it["l_ft"]) * (h - bv)
            op = f"{it['l_ft']} x ({h} - base {bv}) = {round(sf, 2)}"
        o.add(F_L5, sf, it.get("estado", "DERIVADO"), s, f"{it.get('ref')}: {op}")
    tags = (data.get("constants") or {}).get("level5_tags")
    if isinstance(tags, dict):
        src(tags, "constants.level5_tags")
        have = set()
        for it in items:
            have |= {x.strip().upper() for x in re.split(r"[/,+]", str(it.get("wc_tag") or "")) if x.strip()}
        if not tags.get("value") and not items:
            o.add(F_L5, 0.0, "DERIVADO", tags["source"], "finish schedule without LEVEL 5")
            return
        for t in tags.get("value") or []:
            if str(t).strip().upper() not in have:
                o.avisos.append(f"FALTA Level 5 {t}: el schedule ({tags.get('source')}) lo pide y no hay "
                                f"level5_items con ese tag")
                o.estado[F_L5] = "PENDIENTE"
    else:
        o.avisos.append("Level 5 sin constants.level5_tags (tags del finish schedule con 'LEVEL 5'): cobertura "
                        "no verificable")
    if not items:
        o.pend(F_L5, "no level5_items")


def deflection_clips(data, studs_out, o):
    """v73 (P04 de la prueba 21B): una nota general que pide DEFLECTION CLIPS en walls no portantes no tenía familia.
    canon `deflection_clips`:
      {note_source, slip_track_source?}  nota que los pide (+ detalle de type que dibuja slip track, si lo hay);
      {none_reason, source}               el set no los pide (barrido de notas S / A citado).
    pcs = Σ studs completos (pcs_full de studs_out) de los walls con to_deck. Si la nota los pide Y el detalle del
    type dibuja slip / deflection track, las dos lecturas existen: 0 en la familia + RFI con el delta (n)."""
    dc = data.get("deflection_clips")
    if not isinstance(dc, dict):
        # la compuerta (chequeos_v73 R73.6) exige el bloque en el canon; aquí no se inventa una cantidad
        o.add(F_CLIPS, 0.0, "CRITERIO", "-", "deflection_clips not declared in the canon (R73.6 gate requires it)")
        o.avisos.append("deflection_clips sin declarar: R73.6 lo rechaza en la compuerta")
        return
    if str(dc.get("none_reason") or "").strip():
        o.add(F_CLIPS, 0.0, "DERIVADO", src(dc, "deflection_clips"), f"not applicable: {dc['none_reason']}")
        return
    note = str(dc.get("note_source") or "").strip()
    if not note:
        raise ValueError("deflection_clips: note_source (nota que pide los clips) o none_reason + source")
    to_deck = {str(w.get("id")) for w in data.get("walls") or [] if w.get("to_deck")}
    n, k = 0, 0
    for w in (studs_out or {}).get("walls") or []:
        if str(w.get("id")) in to_deck:
            n += int(w.get("pcs_full") or 0)
            k += 1
    if not studs_out:
        o.pend(F_CLIPS, "deflection clips need studs_out.json (pcs_full of walls to structure)")
        return
    slip = str(dc.get("slip_track_source") or "").strip()
    if slip:
        o.add(F_CLIPS, 0.0, "CRITERIO", f"{note}; {slip}",
              f"general note asks for deflection clips and the type details draw a slip track: 0 carried, "
              f"RFI +{n} ({k} walls to structure)")
        o.rfis.append({"familia": F_CLIPS, "tema": "deflection clips: the general note asks for them at "
                       "non-load-bearing walls and the partition details draw a slip / deflection track (R73.6)",
                       "delta": n, "unidad": "pcs",
                       "alternativa": f"one clip per full-height stud of the {k} walls to structure"})
        return
    o.add(F_CLIPS, float(n), "DERIVADO", note, f"{n} full-height studs of {k} walls to structure")


def calcular(fam_out, data, studs_out=None, fo=None):
    o = Out()
    fam = fam_out.get("familias") or {}
    additional_head_track(data, o)
    stud_reinforcement(data, fo, o)
    extra_framing(data, o)
    grille_head(data, o)
    jamb_return(data, o)
    pvc_trim(data, o)
    pafs(data, fo, o)
    access_panels(data, fo, o)
    board_yields(data, fam, o)
    framing_screws(data, fam_out, studs_out, o)
    pins_anchors(data, o)
    level5(data, o)
    deflection_clips(data, studs_out, o)
    for r in data.get("accesorios_rfi") or []:          # lo que ningún plano contesta: RFI con delta
        f = r.get("familia")
        if f not in FAMS:
            raise ValueError(f"accesorios_rfi: familia '{f}' desconocida")
        for kk in ("motivo", "delta"):
            if r.get(kk) in (None, ""):
                raise ValueError(f"accesorios_rfi {f}: falta {kk}")
        src(r, f"accesorios_rfi {f}")
        o.rfis.append({"familia": f, "tema": r["motivo"], "delta": r["delta"], "source": r["source"]})
        if o.estado[f] == "PENDIENTE":
            o.estado[f] = "RFI"
    for r in data.get("accesorios_none") or []:         # el plano contesta que no hay (ej. proyecto sin ATM)
        f = r.get("familia")
        if f not in FAMS or not str(r.get("why") or "").strip():
            raise ValueError(f"accesorios_none: familia conocida + why (motivo) obligatorios: {r}")
        src(r, f"accesorios_none {f}")
        if o.estado[f] == "PENDIENTE" and o.fam[f] <= EPS:
            o.estado[f] = "DERIVADO"
            o.filas.append({"familia": f, "valor": 0.0, "unidad": UNIDAD[f], "estado": "DERIVADO",
                            "source": r["source"], "operacion": f"no aplica: {r['why']}"})
        elif o.fam[f] > EPS:
            raise ValueError(f"accesorios_none {f}: la familia tiene cantidad declarada; quitar el none")
    return {"familias": {f: round(v, 2) for f, v in o.fam.items()}, "unidades": UNIDAD, "waste": WASTE,
            "estado": o.estado, "filas": o.filas, "avisos": o.avisos, "rfis": o.rfis,
            "nombres_excel": nombres_excel(data, o), "excluidas": EXCLUIDAS}


def nombres_excel(data, o):
    """Renglón de Material Summary por familia; el del grille lleva el N/HOJA de su detalle y el del access
    panel la medida del key note (access_panels[].size o fo_in size)."""
    out = dict(NOMBRES_EXCEL)
    det = sorted({m.group(0) for r in o.filas if r["familia"] == F_GRILLE
                  for m in re.finditer(r"\b\d{1,2}/[A-Z]{1,2}\d{1,2}\.\d{1,2}", str(r["source"]))})
    out[F_GRILLE] = out[F_GRILLE].format(det=", ".join(det) or "detail per plans")
    med = next((str(x.get("size")) for x in data.get("access_panels") or [] if x.get("size")), "")
    out[F_AP] = out[F_AP].format(med=med).strip()
    return out


def main(argv):
    args = argv[1:]
    opt = {}
    for flag in ("--studs", "--fo"):
        if flag in args:
            i = args.index(flag)
            opt[flag] = json.load(open(args[i + 1]))
            del args[i:i + 2]
    if len(args) != 3:
        print(__doc__)
        return 2
    try:
        out = calcular(json.load(open(args[0])), json.load(open(args[1])), opt.get("--studs"), opt.get("--fo"))
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as e:
        print(f"ERROR accesorios.py: {e}", file=sys.stderr)
        return 1
    open(args[2], "w").write(json.dumps(out, indent=1, ensure_ascii=False))
    for f, v in out["familias"].items():
        print(f"{f:36s} {v:>12} {UNIDAD[f]:4s} {out['estado'][f]}")
    for a in out["avisos"]:
        print("AVISO", a)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
