#!/usr/bin/env python3
"""chequeos_v77.py — compuertas de las decisiones del usuario D3 / D4 y del largo de wall a través de doors (R77.10).
Las llama canon.py.

R77.4 (D4, 3/4" FRT plywood en piers de storefront): el detalle del pier rotula el plywood SOLO como strip en cada
  jamb del storefront; las caras del pier (nailbase: AWB on FRT plywood bonded to polyiso, y gypsum board) NO van en
  ese renglón. Cada plywood_strips[] con uso "pier":
    - label = el rótulo impreso del strip (no "BONDED", "POLYISO", "AWB", "GYPSUM": eso es la cara);
    - width_ft medido por vector (D3): width_pt + scale_pt_per_ft (escala impresa del detalle) + scale_check
      {printed_in, measured_pt} (un espesor o una cota impresa del mismo detalle, ±5 %); width_ft = width_pt / escala;
    - jambs (int) y height_ft con height_source (alto impreso del head del storefront): lf = jambs x height_ft;
    - plies (int) y layers_drawn (int): si el dibujo muestra más capas que el rótulo (singular) -> plies del rótulo y
      `rfi` con el delta obligatorio.
  Todo elemento pier declara jamb_strips [refs de plywood_strips] o jamb_strips_none_reason (con N/HOJA).
R77.3 (D3): un dato medido por vector lleva su verificación de escala contra algo impreso (scale_check).
R77.10 (decisión del usuario, largo de wall): el largo de un wall corre A TRAVÉS de sus doors hasta la esquina /
  intersección; el R.O. de una door del wall cae DENTRO del largo del wall. Con constants.plan_scale_pt_per_ft, band
  {p0, p1} y openings[].xy_pt (centro del R.O. en la planta): R.O. fuera de [p0, p1] (± 6") = falla (el wall se cortó
  en la jamb y dejó la door afuera).
"""
import math
import re

NHOJA = re.compile(r"\b[0-9A-Z]{1,2}/[A-Z]{1,2}\d")
RX_CARA = re.compile(r"BONDED|POLYISO|\bAWB\b|GYPSUM|NAILBASE", re.I)


def r77_4(data):
    f = []
    strips = {str(s.get("ref")): s for s in data.get("plywood_strips") or [] if isinstance(s, dict)}
    for ref, s in strips.items():
        uso = s.get("uso") or ("pier" if re.search(r"\bpiers?\b", str(s.get("location") or "") + ref, re.I) else None)
        if uso != "pier":
            continue
        if RX_CARA.search(str(s.get("label") or "")):
            f.append(f"R77.4 {ref}: label '{s.get('label')}' es la cara del pier (nailbase / gypsum board), no el strip "
                     f"de jamb (D4)")
        try:
            w_pt, esc = float(s["width_pt"]), float(s["scale_pt_per_ft"])
            sc = s["scale_check"]
            med = float(sc["measured_pt"]) / esc * 12.0
            imp = float(sc["printed_in"])
            if imp <= 0 or abs(med - imp) / imp > 0.05:
                f.append(f"R77.4 {ref}: scale_check {round(med, 3)}\" medido vs {imp}\" impreso (> 5 %, D3)")
            if abs(w_pt / esc - float(s["width_ft"])) > 0.005:
                f.append(f"R77.4 {ref}: width_ft {s['width_ft']} != width_pt / escala {round(w_pt / esc, 4)} (D3)")
        except (KeyError, TypeError, ValueError):
            f.append(f"R77.4 {ref}: strip de pier sin width_pt + scale_pt_per_ft + scale_check {{printed_in, "
                     f"measured_pt}} (D3/D4: el ancho del strip se mide por vector a la escala impresa del detalle)")
            continue
        try:
            jambs, h = int(s["jambs"]), float(s["height_ft"])
            if not NHOJA.search(str(s.get("height_source") or "")) and not re.search(r"[A-Z]{1,2}\d{1,2}\.\d{2}",
                                                                                  str(s.get("height_source") or "")):
                f.append(f"R77.4 {ref}: height_source sin hoja (alto impreso, D4)")
            if abs(jambs * h - float(s["lf"])) > 0.01:
                f.append(f"R77.4 {ref}: lf {s['lf']} != jambs {jambs} x height_ft {h} (D4)")
        except (KeyError, TypeError, ValueError):
            f.append(f"R77.4 {ref}: strip de pier sin jambs + height_ft + height_source (D4)")
        try:
            plies, capas = int(s["plies"]), int(s["layers_drawn"])
            if capas > plies and not str(s.get("rfi") or "").strip():
                f.append(f"R77.4 {ref}: {capas} capas dibujadas y {plies} ply(s) del rótulo sin rfi con delta (D4)")
        except (KeyError, TypeError, ValueError):
            f.append(f"R77.4 {ref}: strip de pier sin plies + layers_drawn (D4)")
    for w in data.get("walls") or []:
        if w.get("element") != "pier":
            continue
        js = w.get("jamb_strips")
        if isinstance(js, list) and js:
            falta = [x for x in js if str(x) not in strips]
            if falta:
                f.append(f"R77.4 {w.get('id')}: jamb_strips {falta} no están en plywood_strips")
        elif not NHOJA.search(str(w.get("jamb_strips_none_reason") or "")) and \
                not re.search(r"[A-Z]{1,2}\d{1,2}\.\d{2}", str(w.get("jamb_strips_none_reason") or "")):
            f.append(f"R77.4 {w.get('id')}: pier sin jamb_strips ni jamb_strips_none_reason con hoja (D4: el detalle "
                     f"del pier rotula 3/4\" FRT plywood en cada jamb del storefront)")
    return f


def _esc(data):
    e = (data.get("constants") or {}).get("plan_scale_pt_per_ft")
    e = e.get("value") if isinstance(e, dict) else e
    try:
        return float(e) if e else None
    except (TypeError, ValueError):
        return None


def r77_10(data, tol_ft=0.5):
    f, esc = [], _esc(data)
    if not esc:
        return f
    for w in data.get("walls") or []:
        b = w.get("band") or {}
        p0, p1 = b.get("p0"), b.get("p1")
        if not (p0 and p1):
            continue
        dx, dy = float(p1[0]) - float(p0[0]), float(p1[1]) - float(p0[1])
        lp = math.hypot(dx, dy)
        if lp <= 0:
            continue
        import criterios                                 # v80e: escala de la hoja del wall
        esc_w = criterios.escala_wall(data, w, esc)
        largo = lp / esc_w
        for o in w.get("openings") or []:
            xy = o.get("xy_pt") if isinstance(o, dict) else None
            if str(o.get("kind")) != "door" or not xy:
                continue
            t = ((float(xy[0]) - float(p0[0])) * dx + (float(xy[1]) - float(p0[1])) * dy) / lp / esc_w
            r = float(o.get("ro_w_ft") or 0.0) / 2.0
            if t - r < -tol_ft or t + r > largo + tol_ft:
                f.append(f"R77.10 {w.get('id')} {o.get('ref')}: el R.O. ({round(t - r, 2)} a {round(t + r, 2)} ft) "
                         f"cae fuera del largo del wall (0 a {round(largo, 2)} ft): el largo corre a través de la "
                         f"door hasta la esquina / intersección")
    return f


def revisar(data):
    return {"fallas": r77_4(data) + r77_10(data)}


def verificar(data):
    f = revisar(data)["fallas"]
    if f:
        raise ValueError("chequeos_v77: " + " | ".join(f))
    return True
