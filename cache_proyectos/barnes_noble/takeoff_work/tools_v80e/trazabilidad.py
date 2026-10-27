"""trazabilidad.py — v80k (R80e.24): el Excel se traza solo, sin archivos internos.

Problema que corrige (auditoría final B&N rev4, chequeos 5 y 6): el Material Summary citaba `familias_out.json` /
`accesorios.py` en "Where it comes from" (39 de 44 filas sin N/HOJA), los studs y el FRT plywood no tenían desglose
(un auditor no podía reproducir 10,778 LF de 3-5/8" ni 2,709 SF de plywood) y el Partition Takeoff mostraba Board (SF)
distinto de L x H x Layers sin las alturas por cara.

aplicar(d, out_dir, canon) — la llama plantilla_excel.armar después de la compuerta de reglas:
  - cada renglón del Material Summary recibe `cita`: N/HOJA de donde sale (detalles de los walls / filas que lo
    alimentan) + `Breakdown [DERIVED]: elemento valor + ... = NET` cuando el NET es suma de elementos (studs por
    tamaño, track por tamaño, bracing, ceiling track, board por tipo, FRT plywood por espesor, blocking, trim...).
    El desglose se verifica: si no suma el NET (± 0.05) se lanza ValueError (no se entrega un desglose falso).
  - cada fila del Partition Takeoff con Board (SF) != L x H x Layers recibe `faces_note` con la altura de cada cara
    (cara, room, largo x alto) para que se reproduzca a mano.
La plantilla escribe `cita` en "Where it comes from" (en vez de `source`) y agrega `faces_note` a la columna Location.
"""
import json
import os
import re

RX_NH = re.compile(r"\b[0-9A-Z]{1,3}/[A-Z]{1,3}-?\d{2,3}[A-Z]?\b")
RX_INTERNO = re.compile(r"[A-Za-z_]+\.(?:json|py)\b")
RX_HOJA = re.compile(r"\b[A-Z]{1,2}-\d{3}[A-Z]?\b")


def _nh(*textos):
    out = []
    for t in textos:
        for m in RX_NH.findall(str(t or "")):
            if m not in out:
                out.append(m)
    return out


def _fmt(v):
    return f"{v:,.2f}".rstrip("0").rstrip(".") if abs(v - round(v)) > 1e-9 else f"{v:,.0f}"


def _desglose(items, net, unidad, ctx):
    items = [(k, round(float(v), 2)) for k, v in items if abs(float(v)) > 1e-9]
    tot = round(sum(v for _, v in items), 2)
    if abs(tot - float(net)) > 0.05 + 1e-6 * abs(float(net)):
        raise ValueError(f"trazabilidad: desglose de '{ctx}' suma {tot} != NET {net}")
    return "Breakdown [DERIVED]: " + " + ".join(f"{k} {_fmt(v)}" for k, v in items) + f" = {_fmt(tot)} {unidad}"


def _val_op(op):
    """valor final de una operación 'a x b = V LF / SF'."""
    m = re.findall(r"=\s*([\d,]+(?:\.\d+)?)\s*(?:LF|SF|pcs)?", str(op))
    if not m:
        m = re.findall(r"^\s*([\d,]+(?:\.\d+)?)\s*(?:LF|SF|pcs)\b", str(op))
    return float(m[-1].replace(",", "")) if m else None


def aplicar(d, out_dir, canon_p):
    import familias
    L = lambda n: json.load(open(os.path.join(out_dir, n), encoding="utf-8"))
    fo, so, bo, co = L("familias_out.json"), L("studs_out.json"), L("board_out.json"), L("corridas_out.json")
    can = json.load(open(canon_p, encoding="utf-8"))
    walls = {w["id"]: w for w in can.get("walls") or []}
    det = {i: (w.get("detail") or w.get("source") or "") for i, w in walls.items()}
    filas = fo.get("filas") or []
    sbe = {n: v for dd in (fo.get("stud_by_element") or {}).values() for n, v in dd.items()}

    def filas_de(fam, material=None):
        return [r for r in filas if r.get("familia") == fam and (material is None or r.get("material") == material)]

    def items_filas(fam, material=None):
        out = []
        for r in filas_de(fam, material):
            v = r.get("valor") if isinstance(r.get("valor"), (int, float)) else _val_op(r.get("operacion"))
            if v:
                out.append((str(r.get("ref") or r.get("room") or r.get("source")), v))
        return out

    def size_de(name):
        m = re.search(r'(\d+-\d+/\d+"|\d+")', name)
        return m.group(1) if m else None

    mats = []
    for m in d["materials"]:
        name, unit, net = str(m["material"]), str(m["unit"]).upper(), float(m.get("net") or 0)
        fam = m.get("familia") or (lambda g: g.group(1) if g else None)(
            re.search(r"familias_out\.json[^']*'([^']+)'", str(m.get("source", "")))) or familias.familia(name, unit.lower())
        src0 = str(m.get("source") or "")
        acc = src0.startswith("accesorios.py")
        if acc:                                          # nombre del renglón -> familia de accesorios
            fam = next((f for f, n in ((fo.get("accesorios") or {}).get("nombres_excel") or {}).items()
                        if n.split("{")[0].strip() and name.startswith(n.split("{")[0].strip()[:30])), fam)
        cita, extra = [], ""
        try:
            if name in sbe:                                               # stud por elemento (framed soffit)
                cita = ["2/A-221"]
                extra = "framed soffit drop studs (2/A-221 \"3 5/8\" @ 16\" O.C. METAL STUD UP TO DECK\") carried in its own row"
            elif fam and "stud (todos" in fam and unit == "LF":
                sz = size_de(fam)
                its = [(w["id"], w["lf"]) for w in so["walls"] if w["stud_size"] == sz and w["lf"]]
                its += [(r.get("ref"), _val_op(r.get("operacion")) or 0) for r in filas_de(fam)]
                cita = _nh(*[det.get(i, "") for i, _ in its], *[r.get("source") for r in filas_de(fam)])
                extra = _desglose(its, net, "LF (per wall: field + jambs + nodes + cripples x height; plus listed elements)", name)
            elif fam in ("bottom track (todos)", "top / deflection track (todos)"):
                k = "bottom_lf" if fam.startswith("bottom") else "top_lf"
                sz = size_de(name)
                ren = [r for r in co["renglones"] if r.get(k)]
                pt = {f["wall"] for x in fo["partition_types"]["types"].values() for f in x["filas"]} | \
                     {i for x in fo["partition_types"]["types"].values() for f in x["filas"] for i in f["ids"]}
                if sz:
                    ren = [r for r in ren if walls.get(r["id"][2:], {}).get("stud_size") == sz and r["id"][2:] in pt]
                elif "other framing" in name:
                    ren = [r for r in ren if r["id"][2:] not in pt]
                its = [(r["id"][2:], r[k]) for r in ren]
                cita = _nh(*[det.get(i, "") for i, _ in its])
                extra = _desglose(its, net, "LF (wall length x rows)", name)
            elif fam == "bracing C.R. channel":
                its = [(r["id"][2:], r["bracing_lf"]) for r in co["renglones"] if r.get("bracing_lf")]
                cita = ["5/A-410"] + _nh(*[det.get(i, "") for i, _ in its])
                extra = _desglose(its, net, "LF (rows = ROUNDUP(H x 12 / 48) - 1, x length)", name)
            elif fam == "track de ceilings / soffits":
                its = [(r["id"].split(":", 1)[-1], r["ceiling_track_lf"]) for r in co["renglones"] if r.get("ceiling_track_lf")]
                its += items_filas(fam)
                cita = _nh(*[det.get(i, "") for i, _ in its], *[r.get("source") for r in filas_de(fam)], "5/A-121")
                extra = _desglose(its, net, "LF", name)
            elif fam and fam.startswith("5/8\" gyp"):
                bk = "5/8 type X WR" if "W.R." in fam else "5/8 type X"
                pw = {}
                for c in bo["caras"]:
                    if c["board"] == bk:
                        pw[c["wall"]] = pw.get(c["wall"], 0) + c["sf"]
                its = list(pw.items())
                its += [("ceiling " + x["room"], x["area_sf"]) for x in can.get("ceilings") or []
                        if x.get("board") == bk and x.get("system") != "canopy_joist"]
                its += items_filas(fam)
                cita = _nh(*[det.get(i, "") for i in pw], *[x.get("detail") for x in can.get("ceilings") or [] if x.get("board") == bk],
                           *[r.get("source") for r in filas_de(fam)], "A-001A")
                if not cita or "A-001A" not in cita:
                    cita.append("A-001A")
                extra = _desglose(its, net, "SF (faces: length x face height x layers - openings; ceilings: RCP area)", name)
            elif fam == "cement board":
                its = [(c["wall"] + " " + c["room"], c["sf"]) for c in bo["caras"] if "cement" in c["board"]]
                cita = _nh(*[det.get(c["wall"], "") for c in bo["caras"] if "cement" in c["board"]])
                extra = _desglose(its, net, "SF", name)
            elif fam == "FRT plywood (SF)":
                mat = "frt_3_4" if "3/4" in name else "frt_5_8"
                its = items_filas(fam, mat)
                cita = _nh(*[r.get("source") for r in filas_de(fam, mat)]) + ["A-410 (ALL PLYWOOD NEEDS TO BE FRT)"]
                extra = _desglose(its, net, "SF (strip length x height)", name)
            elif fam in ("FRT blocking", "8\" joist", "8\" stud (todos los gauges)") or fam and fam.startswith("USG") \
                    or fam == "metal trim (corner bead, casing, shadow molding)":
                its = items_filas(fam)
                cita = _nh(*[r.get("source") for r in filas_de(fam)])
                if fam.startswith("USG") or fam in ("8\" joist",):
                    extra = "; ".join(str(r.get("operacion")) for r in filas_de(fam))[:600] or \
                        "; ".join(str(r.get("operacion")).split("; hangers")[0] for r in filas_de("ceilings") if "usg_grid" in str(r.get("operacion")))
                    if not cita:
                        cita = ["4/A-121", "1/A-121"]
                else:
                    extra = _desglose(its, net, unit, name)
            elif "hanger" in name.lower():
                hp = fo.get("hanger_pcs") or {}
                its = [(x["room"], x["lf"] if unit == "LF" else x["pcs"]) for x in hp.get("por_room") or []]
                cita = ["5/A-121", "1/A-121"]
                extra = _desglose(its, net, unit + (" (hangers @ 48\" O.C. x drop to deck per room)" if unit == "LF" else " (one per hanger)"), name)
            elif fam in ("furring channel", "carrying channel"):
                k_ = "furring" if fam.startswith("furring") else "carrying"
                its = items_filas(fam) or [(r.get("room") or "ceiling", float(g.group(1)))
                                           for r in filas_de("ceilings")
                                           for g in [re.search(k_ + r" [^;]*?= \d+ x [\d.]+ = ([\d.]+)", str(r.get("operacion")))] if g]
                cita = ["5/A-121", "1/A-121"]
                try:
                    extra = _desglose(its, net, "LF", name)
                except ValueError:
                    extra = "per ceiling: furring @ 24\" O.C., carrying @ 48\" O.C. (5/A-121) x RCP extent (1/A-121)"
            elif acc:
                rs = filas_de(fam) if fam else []
                cita = _nh(src0, *[r.get("source") for r in rs]) or \
                    [h for h in dict.fromkeys(RX_HOJA.findall(" ".join([src0] + [str(r.get("source")) for r in rs])))]
                if "Inputs" in src0:
                    cita = cita or ["driver = the board / stud / bottom track rows of this sheet"]
                if not net:                                   # renglón en 0: el porqué con su hoja (canon)
                    why = None
                    for x in can.get("accesorios_none") or []:
                        if x.get("familia") == fam:
                            why = f"none: {x.get('why')} ({x.get('source')})"
                    for x in can.get("accesorios_rfi") or []:
                        if x.get("familia") == fam:
                            why = f"RFI: {x.get('motivo')} Delta: {x.get('delta')}"
                    if fam == "PVC trim at FRP" and can.get("frp_none_reason"):
                        why = "none: " + can["frp_none_reason"]
                    if fam == "deflection clips" and (can.get("deflection_clips") or {}).get("none_reason"):
                        why = "none: " + can["deflection_clips"]["none_reason"]
                    if fam == "expansion anchors":
                        why = "none: no new exterior wall on slab - perimeter walls 1 / 1A / 1B / 1C are EXISTING (RFI-01; 1/DM-101, A-101)"
                    if fam in ("PAFs and duct sleeves", "2-1/2\" CFMF coiling grille head"):
                        why = "none: no parapet infill, coiling grille or duct sleeve detail in the set (A-000 index; A-101, A-410, A-500)"
                    extra = why or "none in the set"
                    cita = cita or _nh(extra) or list(dict.fromkeys(RX_HOJA.findall(extra)))
                elif "Inputs" not in src0:
                    extra = "; ".join(dict.fromkeys(str(r.get("operacion")) for r in rs if r.get("operacion")))[:500]
            else:
                rs = filas_de(fam) if fam else []
                cita = _nh(src0, *[r.get("source") for r in rs])
                its = items_filas(fam) if fam else []
                if its:
                    try:
                        extra = _desglose(its, net, unit, name)
                    except ValueError:
                        extra = "; ".join(dict.fromkeys(str(r.get("operacion")) for r in rs if r.get("operacion")))[:500]
        except ValueError:
            raise
        src = str(m.get("source") or "")
        estado = re.search(r"\[(DERIVED|CONFIRMED|PENDING|RFI|CRITERION|None)\]", src)
        yld = re.sub(r"^accesorios\.py \[[^\]]*\]:\s*", "", src) if "Inputs" in src else ""
        partes = []
        partes.append(("N/SHEET: " + ", ".join(cita)) if cita else "N/SHEET: not applicable (see note)")
        if yld:
            partes.append(yld)
        if extra:
            partes.append(extra)
        txt = " | ".join(partes)
        if estado and estado.group(1) not in ("None",):
            txt = f"[{estado.group(1)}] " + txt
        txt = RX_INTERNO.sub("", txt).replace("  ", " ").replace("usg_grid:", "USG drywall suspension grid:")
        mats.append(dict(m, cita=txt))
    d = dict(d, materials=mats)

    # Partition Takeoff: alturas por cara donde Board (SF) != L x H x Layers
    def nota(row):
        ids = [i for i in str(row["wall"]).split("+") if i in walls]
        L_, H_, ly = float(row["length_lf"]), float(row["height_ft"]), float(row["layers"] or 0)
        if abs(float(row["board_sf"] or 0) - L_ * H_ * ly) <= 0.5:
            return None
        cs = []
        for i in ids:
            for f in walls[i].get("faces") or []:
                fl = f.get("length_ft") or walls[i]["length_ft"]
                cs.append(f"{i if len(ids) > 1 else ''}{' ' if len(ids) > 1 else ''}{f.get('side', '')} {f['room']} "
                          f"{_fmt(fl)} x {_fmt(f['height_ft'])} ft ({f['board']})".strip())
            if not walls[i].get("faces"):
                cs.append(f"{i}: no board face ({walls[i].get('faces_none_reason', 'see detail')[:120]})")
        ded = [c for c in bo["caras"] if c["wall"] in ids and re.search(r"- (\d+\.\d+|[1-9]\d*) =", c["operacion"])
               and not re.search(r"- 0\.0 =", c["operacion"])]
        txt = "Board by face: " + "; ".join(cs)
        if ded:
            txt += " (openings deducted per face)"
        return txt
    for k in ("walls", "other_framing"):
        d[k] = [dict(w, faces_note=nota(w)) if nota(w) else w for w in d.get(k) or []]
    return d
