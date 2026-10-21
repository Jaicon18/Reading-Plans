#!/usr/bin/env python3
"""chequeos_v72.py — compuerta v72 sobre el canon conciliado (arbitraje #20). Genérico: ningún valor de proyecto.

Por qué existe: dos corridas con el mismo skill difirieron porque reglas ESCRITAS (R70.4, R70.5, R71.14, R71.15) se
aplicaban a criterio de cada lectura. Cada regla que una corrida dejó de aplicar se vuelve aquí una falla de script.

  R72.1  Type K (panel balístico: tag que termina en K, o detalle con `k_panel`): cada wall K trae
         `hatch_extent {value_ft, source, img}` medido en vector (extensión del hatch, R70.4) y su length_ft = ese
         valor (± 0.05 ft) salvo length_status CONFIRMADO (cota impresa). Un segmento SIN tag (tag_ids vacío) nunca
         es wall K: el jog / return con hatch va a `ballistic_jogs` (board) y su framing al type base; sin hatch, al
         type base. Así el LF del type K y el contorno ballistic no dependen de la lectura (R70.4 / R70.5).
  R72.2  Wall diagonal (band ori D): band con `faces_top` y `faces_bottom` (dos segmentos [[x, y], [x, y]] medidos en
         vector) y length_ft = promedio de los dos largos de cara (eje) ± 0.05 ft. Una cara sola o un extremo
         "a ojo" cambia el largo entre corridas.
  R72.3  Pier / box partido en partes (registro exterior sin tag + registro con tag del mismo box, R71.2): la parte
         sin tag lleva `part_of: <id del registro con tag>`; partition_types la saca de la cuenta de walls (un box =
         un wall, el del tag) y accesorios no la mete en expansion anchors (RFI con delta, R71.15).
  R72.4  vigas_sobre_walls manda (R71.14): si se pasa la salida (--vigas vigas_out.json), cada wall que la tool da
         bajo viga con perfil lleva `stops_under_beam` o `beam_override {motivo, source, img}`; un override que
         invoca una lectura "estricta" de la regla sin imagen = falla. La tolerancia es la de la tool, no la del texto.
  R72.5  MEP (6/S5.20): cada `mep_penetrations[]` trae `xy` y `method` = "mep.cruces" (salida de la tool) o
         `manual {motivo, img}`; ref repetida por tamaño contra el opening_schedule (FD / fire damper) = falla (el
         mismo FD contado por el schedule y por el barrido); `studs_cut` solo con source N/HOJA.
  R72.11 (v77b D1) atm_recess sin fórmula sistered + furring (la partición interior completa que contiene el ATM de
         lobby / walk-up); atm_recess en una wall exterior (drive-up) = falla (su framing queda en su type exterior).
  R72.10 tile_base.inside_corners con > 4 vértices trae `jogs` [{depth_in, kind notch|step, source}]: un jog de menos
         de 6" (carrier, espesor de acabado) no lleva inside corner trim (accesorios lo descuenta con RFI).
  R72.6  faces[].side = A | B | END (A = cara norte u oeste, B = sur o este; BOX = A); nunca letras de brújula.

Uso:  python3 chequeos_v72.py takeoff_canon.json [--vigas vigas_out.json]   rc 0 = sin fallas; rc 1 = fallas.
"""
import json
import math
import re
import sys

NHOJA = re.compile(r"\b[0-9A-Z]{1,3}/[A-Z]{1,3}-?\d{1,3}\.\d{1,3}")
HOJA = re.compile(r"\b[A-Z]{1,3}-?\d{1,3}\.\d{1,3}")
ESTRICTO = re.compile(r"strict|estrict", re.I)
TOL_FT = 0.05
SIDES = ("A", "B", "END")
TAMANO = re.compile(r"(\d+)\s*[xX×]\s*(\d+)")


def _esc(canon):
    v = ((canon.get("constants") or {}).get("plan_scale_pt_per_ft"))
    try:
        return float(v.get("value") if isinstance(v, dict) else v) if v is not None else 18.0
    except (TypeError, ValueError):
        return 18.0


def es_k(w, k_details=()):
    """Type K = tag interior que termina en K (A1K, B2K, A5K) o detalle declarado con k_panel."""
    t = str(w.get("tag") or "").upper().strip()
    if w.get("element", "wall") not in ("wall",):
        return False
    if t.startswith("EXT"):
        return False
    return bool(re.match(r"^[A-Z]+\d*K$", t)) or str(w.get("detail") or "") in k_details


def _k_details(canon):
    out = set()
    for k, d in (canon.get("details") or {}).items():
        if isinstance(d, dict) and d.get("k_panel"):
            out.add(k)
    return out


def r72_1(canon):
    f = []
    kd = _k_details(canon)
    for w in canon.get("walls") or []:
        if not es_k(w, kd):
            continue
        if not [x for x in (w.get("tag_ids") or []) if x]:
            f.append(f"R72.1 {w['id']} ({w.get('tag')}) sin tag: un segmento sin tag no es wall K; con hatch va a "
                     f"ballistic_jogs (board) y su framing al type base; sin hatch, al type base")
            continue
        he = w.get("hatch_extent")
        if not isinstance(he, dict) or he.get("value_ft") is None or not str(he.get("source") or "").strip() \
                or not he.get("img"):
            f.append(f"R72.1 {w['id']} ({w.get('tag')}) sin hatch_extent {{value_ft, source, img}}: el LF del type K "
                     f"es la extensión del hatch medida en vector (R70.4)")
            continue
        if str(w.get("length_status") or "").upper() == "CONFIRMADO":
            continue
        try:
            d = abs(float(w["length_ft"]) - float(he["value_ft"]))
        except (KeyError, TypeError, ValueError):
            f.append(f"R72.1 {w['id']}: length_ft / hatch_extent.value_ft no numéricos")
            continue
        if d > TOL_FT:
            f.append(f"R72.1 {w['id']} ({w.get('tag')}) length_ft {w.get('length_ft')} != hatch_extent "
                     f"{he['value_ft']} (> {TOL_FT} ft): el type K mide el hatch, no la esquina ni el return")
    return f


def _largo(seg):
    (x0, y0), (x1, y1) = seg
    return math.hypot(float(x1) - float(x0), float(y1) - float(y0))


def r72_2(canon):
    f = []
    esc = _esc(canon)
    for w in canon.get("walls") or []:
        b = w.get("band")
        if not isinstance(b, dict) or str(b.get("ori")).upper() != "D":
            continue
        ft, fb = b.get("faces_top"), b.get("faces_bottom")
        try:
            lt, lb = _largo(ft) / esc, _largo(fb) / esc
        except (TypeError, ValueError, IndexError):
            f.append(f"R72.2 {w['id']} diagonal sin band.faces_top y band.faces_bottom ([[x, y], [x, y]] cada una, "
                     f"medidas en vector): el largo de un wall diagonal es el promedio de sus dos caras")
            continue
        eje = (lt + lb) / 2.0
        try:
            d = abs(float(w["length_ft"]) - eje)
        except (KeyError, TypeError, ValueError):
            f.append(f"R72.2 {w['id']}: length_ft no numérico")
            continue
        if d > TOL_FT and str(w.get("length_status") or "").upper() != "CONFIRMADO":
            f.append(f"R72.2 {w['id']} length_ft {w.get('length_ft')} != promedio de caras {round(eje, 3)} "
                     f"({round(lt, 3)} / {round(lb, 3)})")
    return f


def _box(w):
    b = w.get("band")
    if not isinstance(b, dict) or str(b.get("ori")).upper() != "BOX":
        return None
    try:
        x0, x1 = sorted((float(b["c0"]), float(b["c1"])))
        y0, y1 = sorted((float(b["lo"]), float(b["hi"])))
    except (KeyError, TypeError, ValueError):
        return None
    return x0, y0, x1, y1


def _solape(a, b):
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    menor = min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1]))
    return (ix * iy) / menor if menor > 0 else 0.0


def partes_de_box(walls):
    """{id parte sin tag: id del registro con tag del mismo box} — por `part_of` o por solape BOX >= 50 %."""
    out = {}
    bs = [(w, _box(w)) for w in walls]
    bs = [(w, b) for w, b in bs if b is not None]
    for w, b in bs:
        if w.get("part_of"):
            out[w["id"]] = str(w["part_of"])
            continue
        if [x for x in (w.get("tag_ids") or []) if x]:
            continue
        for o, ob in bs:
            if o is w or not [x for x in (o.get("tag_ids") or []) if x]:
                continue
            if (o.get("sheet") or "") == (w.get("sheet") or "") and _solape(b, ob) >= 0.5:
                out[w["id"]] = o["id"]
                break
    return out


def r72_3(canon):
    ws = canon.get("walls") or []
    ids = {w["id"] for w in ws}
    f = []
    for w in ws:
        if w.get("part_of") and w["part_of"] not in ids:
            f.append(f"R72.3 {w['id']}.part_of '{w['part_of']}' no existe en el canon")
    pb = partes_de_box(ws)
    for wid, dueño in pb.items():
        w = next(x for x in ws if x["id"] == wid)
        if not w.get("part_of"):
            f.append(f"R72.3 {wid} es parte (sin tag) del box de {dueño}: declarar part_of '{dueño}' (un box = un "
                     f"wall en la cuenta de walls; la parte no entra en expansion anchors sin fuente)")
    return f


def r72_4(canon, vigas):
    if not vigas:
        return []
    por_id = {w["id"]: w for w in canon.get("walls") or []}
    f = []
    for v in vigas.get("walls_bajo_viga") or []:
        w = por_id.get(v.get("wall"))
        if w is None or not v.get("profile"):
            continue
        if w.get("stops_under_beam"):
            continue
        ov = w.get("beam_override")
        if not isinstance(ov, dict) or not str(ov.get("motivo") or "").strip() or not ov.get("img") \
                or not NHOJA.search(str(ov.get("source") or "")):
            f.append(f"R72.4 {w['id']}: vigas_sobre_walls lo da bajo {v.get('profile')} (eje {v.get('beam_axis_pt')}) "
                     f"y el canon no trae stops_under_beam ni beam_override {{motivo, source N/HOJA, img}}")
        elif ESTRICTO.search(str(ov.get("motivo"))):
            f.append(f"R72.4 {w['id']}: beam_override por lectura 'estricta' de la regla: la tolerancia es la de "
                     f"vigas_sobre_walls (manda la tool)")
    return f


def r72_5(canon):
    f = []
    pens = canon.get("mep_penetrations") or []
    for p in pens:
        ref = p.get("ref")
        if p.get("xy") is None:
            f.append(f"R72.5 mep_penetrations {ref}: sin xy (posición del cruce en la planta registrada)")
        if str(p.get("method") or "") != "mep.cruces":
            m = p.get("manual")
            if not isinstance(m, dict) or not str(m.get("motivo") or "").strip() or not m.get("img"):
                f.append(f"R72.5 mep_penetrations {ref}: method '{p.get('method')}' — va la salida de mep.cruces, o "
                         f"manual {{motivo, img}} para un cruce que la tool no ve")
        sc = p.get("studs_cut")
        if sc is not None and not HOJA.search(str((sc or {}).get("source") if isinstance(sc, dict) else "")):
            f.append(f"R72.5 mep_penetrations {ref}: studs_cut sin source con hoja (los studs cortados los calcula "
                     f"accesorios: MAX(1, ROUNDUP(ancho / O.C.)) x rows del wall)")
    fd_pen = [TAMANO.search(str(p.get("ref") or "")) for p in pens if re.match(r"(?i)^\s*(FD|fire damper)", str(p.get("ref") or ""))]
    fd_pen = sorted(f"{m.group(1)}x{m.group(2)}" for m in fd_pen if m)
    sched = [it for it in (canon.get("opening_schedule") or {}).get("items") or []
             if re.match(r"(?i)^\s*(FD|fire damper)", str(it.get("ref") or "")) or it.get("kind") == "fire_damper"]
    refs_pen = {str(p.get("ref")) for p in pens}
    for it in sched:
        if str(it.get("ref")) in refs_pen or it.get("in_mep_penetrations"):
            continue
        m = TAMANO.search(str(it.get("ref") or ""))
        if m and f"{m.group(1)}x{m.group(2)}" in fd_pen:
            f.append(f"R72.5 opening_schedule '{it.get('ref')}' y una mep_penetration FD del mismo tamaño: el mismo "
                     f"fire damper contado dos veces; marcar in_mep_penetrations: true en el schedule (o usar la misma ref)")
    return f


def r72_7(canon):
    """R72.11 (ATM), v77b (decisión del usuario D1, corregida): el extra framing del ATM = la partición interior
    completa que contiene el ATM de lobby / walk-up (studs piso a deck + bottom + top runner). atm_recess solo lleva
    {source N/HOJA, drawn}; la fórmula vieja (width_ft, sistered_h_ft, furring_rows, alternativas, *_status) es
    falla; atm_recess fuera de un wall o en una wall exterior (drive-up) también."""
    f = []
    viejos = ("width_ft", "sistered_h_ft", "furring_rows", "alternativas", "width_status", "sistered_h_status",
              "furring_rows_status")
    for w in canon.get("walls") or []:
        for op in w.get("openings") or []:
            ar = op.get("atm_recess") if isinstance(op, dict) else None
            if isinstance(ar, dict) and any(k in ar for k in viejos):
                f.append(f"R72.11 {op.get('ref')}: atm_recess con la fórmula sistered + furring (D1 v77b: el extra "
                         f"framing del ATM es la partición completa {w.get('id')}, studs piso a deck + bottom + top "
                         f"runner)")
            ext = str(w.get("tag") or "").upper().startswith("EXT") or w.get("location") == "exterior" or \
                w.get("exterior") is True or (isinstance(op, dict) and op.get("location") == "exterior")
            if ar and ext:
                f.append(f"R72.11 {op.get('ref')}: atm_recess en la wall exterior {w.get('id')} (D1 v77b: el drive-up "
                         f"queda en su type exterior; el extra framing es la partición interior del walk-up)")
    for op in canon.get("openings_extra") or []:
        if isinstance(op, dict) and op.get("atm_recess"):
            f.append(f"R72.11 {op.get('ref')}: atm_recess fuera de un wall (D1 v77b: va en la partición que contiene el ATM)")
    return f


def r72_10(canon):
    """R72.10 (FRP): tile_base.inside_corners con más de 4 vértices trae jogs [{depth_in, kind notch|step, source}]."""
    f = []
    for t in canon.get("tile_base") or []:
        ic = t.get("inside_corners")
        if isinstance(ic, dict) and int(ic.get("vertices") or 4) > 4:
            js = ic.get("jogs")
            if not isinstance(js, list) or not js or not all(isinstance(j, dict) and j.get("kind") in ("notch", "step")
                                                             and j.get("depth_in") is not None for j in js):
                f.append(f"R72.10 tile_base {t.get('room')}: {ic.get('vertices')} vértices sin jogs [{{depth_in, kind "
                         f"notch|step, source}}] (un jog < 6\" no lleva inside corner trim; se mide)")
    return f


def r72_6(canon):
    f = []
    for w in canon.get("walls") or []:
        for c in w.get("faces") or []:
            s = c.get("side")
            if s is not None and str(s).upper() not in SIDES:
                f.append(f"R72.6 {w['id']} face side '{s}': A | B | END (A = norte u oeste, B = sur o este; BOX = A)")
                break
    return f


def revisar(canon, vigas=None):
    fallas = r72_1(canon) + r72_2(canon) + r72_3(canon) + r72_4(canon, vigas) + r72_5(canon) + r72_6(canon) + r72_7(canon) + r72_10(canon)
    return {"fallas": fallas, "avisos": []}


def main(argv):
    a = list(argv[1:])
    vig = None
    if "--vigas" in a:
        i = a.index("--vigas")
        vig = json.load(open(a[i + 1]))
        del a[i:i + 2]
    if len(a) != 1:
        print(__doc__)
        return 2
    r = revisar(json.load(open(a[0])), vig)
    for x in r["fallas"]:
        print("FALLA", x)
    print("OK" if not r["fallas"] else f"{len(r['fallas'])} falla(s)")
    return 1 if r["fallas"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
