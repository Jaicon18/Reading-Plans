#!/usr/bin/env python3
"""chequeos_v73.py — reglas v73 que la compuerta (reglas.py) hace cumplir sobre el canon y las salidas.

Por qué existe: en una prueba ciega las reglas R70.5 / R72.1 (ballistic) y R72.5 (MEP) estaban escritas y la
compuerta dio OK, pero el resultado salió fuera de rango. La compuerta v72b revisaba la FORMA (hay hatch_extent,
hay face customer, la penetración tiene method) y no la CONSISTENCIA con el plano:
  - el largo de un wall K se midió en vector con la cota del mismo tramo impresa a su lado, y el tramo vecino del
    mismo contorno se alargó hasta donde empezaba el otro: el contorno ballistic sumó la esquina dos veces;
  - "manual {motivo, img}" dejaba entrar a la familia cualquier cruce que la tool no veía (y pipes y fire dampers),
    así que el número dependía de la lectura.

R73.1  Todo wall K (tag que termina en K o detalle con k_panel) lleva `dim_scan` = salida de cotas_banda.py
       {found: [{text, value_ft}], source}. Si una cota encontrada es compatible con el largo (± 35 %), el
       length_ft ES esa cota (± 0.05 ft) y length_status CONFIRMADO; si no la usa, `dim_scan.no_aplica` explica
       por qué (la cota mide otra cosa) con N/HOJA o HOJA.
R73.2  Contorno K sin dueños dobles: cada `ballistic_jogs[]` trae `band` {ori, c0, c1, lo, hi}; ninguna banda K
       (walls K + jogs) se solapa con otra en los dos ejes más de 1 pt (cada esquina un dueño, R70.2), y dos walls K
       paralelos del mismo contorno (líneas a ≤ 30 pt) no se solapan a lo largo del eje más de 1 pt. Además
       constants.ballistic_contour_ft (si está) = Σ largos K + Σ jogs.
R73.5  stud reinforcement MEP = SOLO los cruces de ducto que da mep.cruces (method "mep.cruces", kind duct /
       duct_sleeve), MAX(1, ROUNDUP(ancho / O.C.)) × rows × qty (o studs_cut con fuente). Lo demás (cruces
       manuales, fire dampers, pipes > 1" del detalle de penetración, aberturas de ducto de otras listas) NO entra
       en la familia: va a RFI con su delta (accesorios.py los escribe). La compuerta recalcula y compara con
       familias_out.

R73.6  El canon declara `deflection_clips`: {note_source, slip_track_source?} si una nota general los pide en walls
       no portantes, o {none_reason, source} si el barrido de notas S / A no los encuentra (P04 de la prueba 21B:
       ninguna tool los contaba y nadie lo decía).

R73.7  Segmento SIN tag tipado por la nota general ("ALL PARTITIONS TO BE TYPE X UNLESS OTHERWISE NOTED",
       `default_type_source`): su espesor medido (`thickness_measured_in` o "= N in" en `thickness_check`) tiene que
       ser el del type de la nota en la partition schedule (± 0.5"); si no, el type es el de la schedule con ese
       espesor (el wall con tag que toca / colineal) o va `default_type_rfi {alternativas, source}` con las dos
       lecturas. Un stub con espesor de otro type nunca entra al type por defecto.

R73.8  La operación escrita cuadra (#0, honestidad dimensional): en walls / openings, un `*_op` con forma
       "<aritmética> = N" (solo números y + - x * / ( )) da N (± 0.01) y N es el valor del campo (length_op ->
       length_ft, height_op -> height_ft, ro_w_op -> ro_w_ft, head_op -> head_ft). Un número tipeado distinto de
       su propia suma (cadena 1'-2 1/2" + ...) = falla.

R73.3  (parte de canon) cada `plywood_strips[]` declara `uso` ∈ substrate / pier / column_wrap / canopy_soffit /
       nailbase: el renglón de compra (nombre de la plantilla) no se infiere del texto de la fuente.

Uso: python3 chequeos_v73.py <takeoff_canon.json> [--familias familias_out.json]
"""
import json
import math
import re
import sys

TOL_FT = 0.05
TOL_PT = 1.0
GAP_PT = 30.0
COMPAT = 0.35
HOJA = re.compile(r"\b[A-Z]{1,3}-?(?:\d{1,3}\.\d{1,3}|\d{3}[A-Z]?(?![\w.]))")
DUCT_KINDS = ("duct", "duct_sleeve")
F_REINF = "stud reinforcement MEP"


def _k_details(canon):
    return {k for k, d in (canon.get("details") or {}).items() if isinstance(d, dict) and d.get("k_panel")}


def es_k(w, kd):
    t = str(w.get("tag") or "").upper()
    return bool(re.match(r"^[A-Z]+\d*K$", t)) or str(w.get("detail") or "") in kd


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def r73_1(canon):
    f = []
    kd = _k_details(canon)
    for w in canon.get("walls") or []:
        if not isinstance(w, dict) or not es_k(w, kd) or not [x for x in (w.get("tag_ids") or []) if x]:
            continue
        ds = w.get("dim_scan")
        if not isinstance(ds, dict) or not isinstance(ds.get("found"), list) or not str(ds.get("source") or "").strip():
            f.append(f"R73.1 {w.get('id')} ({w.get('tag')}) sin dim_scan {{found, source}} (salida de cotas_banda.py): "
                     f"la cota impresa del tramo manda sobre el vector")
            continue
        L = _f(w.get("length_ft"))
        if L is None or L <= 0:
            continue
        compat = [c for c in ds["found"] if isinstance(c, dict) and _f(c.get("value_ft")) and
                  abs(_f(c["value_ft"]) - L) <= COMPAT * max(L, _f(c["value_ft"]))]
        if not compat:
            continue
        if any(abs(_f(c["value_ft"]) - L) <= TOL_FT for c in compat):
            if str(w.get("length_status") or "").upper() != "CONFIRMADO":
                f.append(f"R73.1 {w.get('id')}: length_ft = cota impresa {compat[0].get('text')} pero length_status "
                         f"no es CONFIRMADO")
            continue
        na = str(ds.get("no_aplica") or "")
        if na.strip() and HOJA.search(na):
            continue
        f.append(f"R73.1 {w.get('id')} ({w.get('tag')}) length_ft {L} != cota impresa "
                 f"{', '.join(str(c.get('text')) for c in compat)} junto al tramo: el largo es la cota (CONFIRMADO) "
                 f"o dim_scan.no_aplica dice por qué con su hoja")
    return f


def _rect(b):
    if not isinstance(b, dict) or str(b.get("ori", "")).upper() not in ("H", "V"):
        return None
    try:
        c0, c1 = sorted((float(b["c0"]), float(b["c1"])))
        lo, hi = sorted((float(b["lo"]), float(b["hi"])))
    except (KeyError, TypeError, ValueError):
        return None
    return (lo, c0, hi, c1) if str(b["ori"]).upper() == "H" else (c0, lo, c1, hi)


def _solape(a, b):
    return max(0.0, min(a[2], b[2]) - max(a[0], b[0])), max(0.0, min(a[3], b[3]) - max(a[1], b[1]))


def r73_2(canon):
    f = []
    kd = _k_details(canon)
    ks = [w for w in canon.get("walls") or [] if isinstance(w, dict) and es_k(w, kd)
          and [x for x in (w.get("tag_ids") or []) if x]]
    jogs = [j for j in canon.get("ballistic_jogs") or [] if isinstance(j, dict)]
    if not ks and not jogs:
        return f
    elems = []
    for w in ks:
        r = _rect(w.get("band"))
        if r is None:
            f.append(f"R73.2 {w.get('id')}: wall K sin band H|V {{c0, c1, lo, hi}} (contorno sin dueños dobles)")
        else:
            elems.append((w.get("id"), r, w.get("sheet") or (w.get("band") or {}).get("sheet")))
    for j in jogs:
        r = _rect(j.get("band"))
        if r is None:
            f.append(f"R73.2 ballistic_jogs '{j.get('ref')}': sin band {{ori, c0, c1, lo, hi}} medida en vector (sin "
                     f"ella no se puede ver si el jog repite la esquina de un wall K)")
        else:
            elems.append((j.get("ref"), r, (j.get("band") or {}).get("sheet")))
    # walls K paralelos de un mismo contorno (líneas a ≤ GAP_PT): sus tramos no se solapan a lo largo del eje
    for i in range(len(ks)):
        for k in range(i + 1, len(ks)):
            ba, bb = ks[i].get("band") or {}, ks[k].get("band") or {}
            if _rect(ba) is None or _rect(bb) is None or str(ba.get("ori")).upper() != str(bb.get("ori")).upper():
                continue
            a0, a1 = sorted((float(ba["c0"]), float(ba["c1"])))
            b0, b1 = sorted((float(bb["c0"]), float(bb["c1"])))
            if max(a0, b0) - min(a1, b1) > GAP_PT:
                continue
            ov = min(max(ba["lo"], ba["hi"]), max(bb["lo"], bb["hi"])) - max(min(ba["lo"], ba["hi"]), min(bb["lo"], bb["hi"]))
            if ov > TOL_PT:
                f.append(f"R73.2 {ks[i].get('id')} y {ks[k].get('id')} (paralelos del mismo contorno K) se solapan "
                         f"{round(ov, 2)} pt a lo largo del eje: un tramo llega hasta donde empieza el otro y la "
                         f"esquina sale dos veces")
    for i in range(len(elems)):
        for k in range(i + 1, len(elems)):
            a, b = elems[i], elems[k]
            if a[2] and b[2] and a[2] != b[2]:
                continue
            ox, oy = _solape(a[1], b[1])
            if ox > TOL_PT and oy > TOL_PT:
                f.append(f"R73.2 {a[0]} y {b[0]} se solapan {round(ox, 2)} x {round(oy, 2)} pt: la misma esquina del "
                         f"contorno ballistic contada dos veces (cada esquina un dueño, R70.2)")
    bc = (canon.get("constants") or {}).get("ballistic_contour_ft")
    v = _f(bc.get("value")) if isinstance(bc, dict) else _f(bc)
    if v is not None:
        s = sum(_f(w.get("length_ft")) or 0.0 for w in ks) + sum(_f(j.get("length_ft")) or 0.0 for j in jogs)
        if abs(s - v) > TOL_FT:
            f.append(f"R73.2 constants.ballistic_contour_ft {v} != Σ walls K + jogs {round(s, 3)}")
    return f


def esperado_mep(canon):
    """(valor, renglones) de stud reinforcement MEP según R73.5."""
    rows = {str(w.get("id")): int(w.get("rows", 1) or 1) for w in canon.get("walls") or [] if isinstance(w, dict)}
    tot, det = 0, []
    for p in canon.get("mep_penetrations") or []:
        if not isinstance(p, dict):
            continue
        if str(p.get("method") or "") != "mep.cruces" or str(p.get("kind") or "duct") not in DUCT_KINDS:
            continue
        if p.get("in_cavity"):
            continue
        sc = p.get("studs_cut")
        q = int(p.get("qty", 1) or 1)
        if isinstance(sc, dict) and sc.get("value") is not None:
            v = int(sc["value"]) * q
        else:
            wd = _f(p.get("width_in") if p.get("width_in") is not None else p.get("dia_in")) or 0.0
            oc = _f(p.get("oc_in")) or 16.0
            v = max(1, math.ceil(wd / oc - 1e-9)) * rows.get(str(p.get("wall")), 1) * q
        tot += v
        det.append((p.get("ref"), v))
    return tot, det


def r73_5(canon, familias=None):
    f = []
    if not isinstance(familias, dict):
        return f
    fam = familias.get("familias") if isinstance(familias.get("familias"), dict) else familias
    if F_REINF not in fam or not (canon.get("mep_penetrations") or []):
        return f
    v = _f(fam.get(F_REINF))
    e, _ = esperado_mep(canon)
    if v is None or abs(v - e) > 0.5:
        otros = [p.get("ref") for p in canon.get("mep_penetrations") or [] if isinstance(p, dict) and
                 (str(p.get("method") or "") != "mep.cruces" or str(p.get("kind") or "duct") not in DUCT_KINDS)]
        f.append(f"R73.5 {F_REINF} {v} != {e} (solo cruces de ducto de mep.cruces × rows); fuera de la familia y a "
                 f"RFI: {len(otros)} ítems manuales / pipes / fire dampers")
    return f


def r73_6(canon):
    dc = canon.get("deflection_clips")
    if not isinstance(dc, dict):
        return ["R73.6 deflection_clips sin declarar: {note_source, slip_track_source?} o {none_reason, source} "
                "(barrido de las notas generales S / A)"]
    if str(dc.get("none_reason") or "").strip():
        return [] if HOJA.search(str(dc.get("source") or "")) else \
            ["R73.6 deflection_clips.none_reason sin source con hoja (qué notas se barrieron)"]
    if not HOJA.search(str(dc.get("note_source") or "")):
        return ["R73.6 deflection_clips.note_source sin hoja (la nota que pide los clips)"]
    return []


_ESP = re.compile(r"=\s*([\d.]+)\s*in\b")


def r73_7(canon):
    f = []
    sch = {str(x.get("type")): _f(x.get("thickness_in")) for x in canon.get("partition_schedule") or []
           if isinstance(x, dict)}
    for w in canon.get("walls") or []:
        if not isinstance(w, dict) or [x for x in (w.get("tag_ids") or []) if x]:
            continue
        if not str(w.get("default_type_source") or "").strip():
            continue
        t = str(w.get("tag") or "")
        esp = _f(w.get("thickness_measured_in"))
        if esp is None:                                   # v78 (R78.11): alias de traza del mismo campo
            esp = _f(w.get("thickness_measured_info"))
        if esp is None:
            m = _ESP.search(str(w.get("thickness_check") or ""))
            esp = _f(m.group(1)) if m else None
        if esp is None:
            f.append(f"R73.7 {w.get('id')} ({t} por nota general) sin espesor medido (thickness_measured_in): sin él "
                     f"no se sabe si el segmento es del type por defecto")
            continue
        ref = sch.get(t)
        if ref is None or abs(esp - ref) <= 0.5:
            continue
        rf = w.get("default_type_rfi")
        if isinstance(rf, dict) and isinstance(rf.get("alternativas"), list) and rf["alternativas"] and \
                HOJA.search(str(rf.get("source") or "")):
            continue
        otros = [k for k, v in sch.items() if v is not None and abs(v - esp) <= 0.5]
        f.append(f"R73.7 {w.get('id')} tipado {t} por la nota general mide {esp} in y el type {t} es {ref} in: es "
                 f"del type con ese espesor ({', '.join(otros) or 'ninguno en la schedule'}) o default_type_rfi con "
                 f"las dos lecturas")
    return f


_ARIT = re.compile(r"^[\d\s.+\-*/x×()]+$")
_OPS = {"length_op": "length_ft", "height_op": "height_ft", "ro_w_op": "ro_w_ft", "head_op": "head_ft"}


def _evaluar(expr):
    e = expr.replace("×", "*").replace("x", "*")
    if not _ARIT.match(expr) or not re.search(r"\d", e):
        return None
    import warnings
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return float(eval(compile(e, "<op>", "eval"), {"__builtins__": {}}, {}))  # solo dígitos y operadores
    except (SyntaxError, ZeroDivisionError, TypeError, ValueError):
        return None


def r73_8(canon):
    f = []
    objs = []
    for w in canon.get("walls") or []:
        if isinstance(w, dict):
            objs.append((w.get("id"), w))
            objs += [(f"{w.get('id')}/{o.get('ref')}", o) for o in w.get("openings") or [] if isinstance(o, dict)]
    objs += [(o.get("ref"), o) for o in canon.get("openings_extra") or [] if isinstance(o, dict)]
    for nombre, o in objs:
        for k_op, k_v in _OPS.items():
            op = o.get(k_op)
            if not isinstance(op, str) or "=" not in op:
                continue
            partes = [x.strip() for x in op.split("=")]

            def val_parte(x):
                m = re.match(r"^([\d.]+)(?![\d.])", x)
                lead = float(m.group(1)) if m else None
                v = _evaluar(x)
                return (v if v is not None else lead), v is not None, lead
            vals = [val_parte(x) for x in partes]
            for i in range(len(vals) - 1):
                (a, ar, _), (b, _, blead) = vals[i], vals[i + 1]
                if a is None or b is None or not ar:
                    continue
                tol = 0.01 + 0.0005 * abs(a)
                if abs(a - b) > tol and (blead is None or abs(a - blead) > tol):
                    f.append(f"R73.8 {nombre}.{k_op}: '{partes[i][:40]}' da {round(a, 4)}, no {b} (la operación "
                             f"escrita no cuadra)")
            ult = vals[-1][0] if vals[-1][1] or len(vals) == 1 else vals[-1][2]
            val = _f(o.get(k_v))
            if ult is not None and val is not None and len(vals) > 1 and vals[-2][1] and \
                    abs(ult - val) > 0.01 + 0.0005 * abs(val):
                f.append(f"R73.8 {nombre}: {k_op} da {ult} y {k_v} es {val} (el valor no es el de su operación)")
    return f


USOS = ("substrate", "pier", "column_wrap", "canopy_soffit", "nailbase")


def r73_3(canon):
    return [f"R73.3 plywood_strips '{s_.get('ref')}': sin uso ({' / '.join(USOS)}); el renglón de la plantilla sale del uso"
            for s_ in canon.get("plywood_strips") or [] if isinstance(s_, dict) and s_.get("uso") not in USOS]


def revisar(canon, familias=None):
    return {"fallas": r73_1(canon) + r73_2(canon) + r73_3(canon) + r73_5(canon, familias) + r73_6(canon) + r73_7(canon) +
            r73_8(canon), "avisos": []}


def main(argv):
    a = list(argv[1:])
    fam = None
    if "--familias" in a:
        i = a.index("--familias")
        fam = json.load(open(a[i + 1], encoding="utf-8"))
        del a[i:i + 2]
    if len(a) != 1:
        print(__doc__)
        return 2
    r = revisar(json.load(open(a[0], encoding="utf-8")), fam)
    for x in r["fallas"]:
        print("FALLA", x)
    print("OK" if not r["fallas"] else f"{len(r['fallas'])} falla(s)")
    return 1 if r["fallas"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
