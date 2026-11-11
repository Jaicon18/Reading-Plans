"""trazabilidad.py — v80k (R80e.24): el Excel se traza solo, sin archivos internos.

Problema que corrige (auditoría final B&N rev4, chequeos 5 y 6): el Material Summary citaba `familias_out.json` /
`accesorios.py` en "Where it comes from" (39 de 44 filas sin N/HOJA), los studs y el FRT plywood no tenían desglose
(un auditor no podía reproducir <n> LF de 3-5/8" ni <n> SF de plywood) y el Partition Takeoff mostraba Board (SF)
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

# R80w.28 + R80e.109: dotted primero (C/A12.01), con guion 2-3 dígitos, sin guion 3 dígitos (A101), sufijo de letra (A505.B)
RX_NH = re.compile(r"\b[0-9A-Z]{1,3}/(?:[A-Z]{1,2}\d{1,2}\.\d{1,2}|[A-Z]{1,3}-\d{2,3}[A-Z]?(?:\.[A-Z]{1,2}\b)?|[A-Z]{1,3}\d{3}[A-Z]?(?:\.[A-Z]{1,2}\b)?)(?![.\d])")
RX_INTERNO = re.compile(r"(?:\bimg\s+)?(?:[\w.-]+/)*[A-Za-z0-9_.-]+\.(?:json|py|md|png|jpg)\b")   # R80e.83: + .md / imágenes
RX_HOJA = re.compile(r"\b(?:[A-Z]{1,2}-\d{3}[A-Z]?|[A-Z]{1,2}\d{3}(?:\.[A-Z]{1,2})?|[A-Z]{1,2}\d{1,2}\.\d{1,2})\b")   # R80e.83


def _nh(*textos):
    out = []
    for t in textos:
        for m in RX_NH.findall(str(t or "")):
            if m not in out:
                out.append(m)
    return out


def _fmt(v):
    return f"{v:,.2f}".rstrip("0").rstrip(".") if abs(v - round(v)) > 1e-9 else f"{v:,.0f}"


def _fam_stud(sz):
    """Familia de stud de un stud_size con la regla de canon.STUD_FAM (R80w.18)."""
    from canon import STUD_FAM
    t = str(sz or "").lower()
    return next((f for k, f in STUD_FAM if k in t), None)


def _es_fam_stud(fam):
    """R80w.22: familias de stud de canon.STUD_FAM (sin parapet ni Z-furring, que tienen su propio renglón)."""
    from canon import STUD_FAM
    return fam in {f for k, f in STUD_FAM} and "parapet" not in fam and "furring" not in fam.lower()


def _desglose(items, net, unidad, ctx):
    items = [(k, round(float(v), 2)) for k, v in items if abs(float(v)) > 1e-9]
    tot = round(sum(v for _, v in items), 2)
    if abs(tot - float(net)) > 0.05 + 1e-6 * abs(float(net)):
        raise ValueError(f"trazabilidad: desglose de '{ctx}' suma {tot} != NET {net}")
    dif = "" if abs(tot - float(net)) < 0.005 else f" (NET {_fmt(round(float(net), 2))}: difference = rounding of the items)"   # BE-HF16 (OBS-6)
    return "Breakdown [DERIVED]: " + " + ".join(f"{k} {_fmt(v)}" for k, v in items) + f" = {_fmt(tot)} {unidad}{dif}"


def _val_op(op):
    """valor final de una operación 'a x b = V LF / SF'."""
    # R80e.105: primero el "= V <unidad>" (un "= 6\" strip" dentro de una cita no es el resultado)
    m = re.findall(r"=\s*([\d,]+(?:\.\d+)?)\s*(?:LF|SF|pcs)\b", str(op))
    if not m:
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
        return [r for r in filas if r.get("familia") == fam and (material is None or r.get("material") == material
                                                                  # R80e.68: frt_5_8_ext va en el mismo renglón 5/8 in.
                                                                  or str(r.get("material") or "").startswith(str(material) + "_"))]

    mq = {m["ref"]: float(m["qty"]) for m in can.get("misc_items") or []}   # v80n: la cantidad del canon manda

    def items_filas(fam, material=None):
        out = []
        for r in filas_de(fam, material):
            v = r.get("valor") if isinstance(r.get("valor"), (int, float)) else mq.get(r.get("ref"), _val_op(r.get("operacion")))
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
        its = None
        try:
            if name in sbe:                                               # stud por elemento (framed soffit)
                cita = _nh(*[r.get("source") for r in filas_de("ceilings")]) or ["default (no sheet)"]   # R80e.83
                ops_ = [f"{r.get('room')}: {str(r.get('operacion')).split(';')[0]}" for r in filas_de("ceilings")
                        if "framed_soffit" in str(r.get("operacion"))]
                extra = "Breakdown [DERIVED]: " + " + ".join(ops_) + f" = {_fmt(net)} LF (framed soffit joists)" if ops_ else \
                    "framed soffit joists carried in its own row"
            elif fam == "1-1/2\" Z-furring" and unit == "LF":       # R80e.83: desglose del Z-furring por wall (BE-40)
                rows_ = [w for w in so["walls"] if re.search(r"z-furring|\bzf|hat channel", str(w.get("stud_size")).lower()) and w.get("lf")]   # BE-HF1
                its = [(w["id"], w["lf"]) for w in rows_]
                cita = _nh(*[det.get(i, "") for i, _ in its])
                extra = _desglose(its, net, "LF (per wall: field pieces + jambs + nodes, full height; cripples)", name) + \
                    " | " + "; ".join(f"{w['id']}: {_en(str(w.get('operacion')))[:220]}" for w in rows_)
            elif fam == "header / box beam" and unit == "LF":        # R80e.83: desglose del header (BE-40)
                try:
                    hi = L("headers_in.json")
                except (OSError, ValueError):
                    hi = {}
                its = [(f"{o['ref']} ({o.get('wall')})", round((float(o["ro_w_ft"]) + 16.0 / 12.0) * int(o.get("pieces") or 1)
                                                              * int(o.get("qty") or 1), 3)) for o in hi.get("openings") or []]
                its += items_filas("header / box beam")      # BE-HF6: box beams / box headers drawn in a detail (misc_items)
                cita = _nh(*[o.get("header_type_source") for o in hi.get("openings") or []],
                           *[r.get("source") for r in filas_de("header / box beam")])
                extra = _desglose(its, net, "LF ((R.O. + 1'-4\") x pieces of the box header; drawn box beams / box headers)", name) + " | " + "; ".join(
                    f"{o['ref']}: ({o['ro_w_ft']} + 1.333) x {o.get('pieces')} pieces {o.get('header_type')}" for o in hi.get("openings") or [])
            elif fam and _es_fam_stud(fam) and unit == "LF":   # R80w.22: toda familia de stud (2-1/2", 1-5/8"...)
                sz = size_de(fam)
                # R80w.18: el wall va a la familia con la MISMA regla de canon.py (STUD_FAM, primera clave contenida en
                # stud_size): "PENDING - 6\" assumed (RFI)" o "3-5/8\" + 6\"" también son de su familia de stud
                its = [(w["id"], w["lf"]) for w in so["walls"] if _fam_stud(w["stud_size"]) == fam and w["lf"]]
                its += [(r.get("ref"), mq.get(r.get("ref"), _val_op(r.get("operacion")) or 0)) for r in filas_de(fam)]   # R80e.123: qty del canon manda
                cita = _nh(*[det.get(i, "") for i, _ in its], *[r.get("source") for r in filas_de(fam)])
                extra = _desglose(its, net, "LF (per wall: field + jambs + nodes + cripples x height; plus listed elements)", name)
                pg = {}
                for i, v in its:
                    g = walls.get(i, {}).get("gauge") or "elements (gauge in their operation)"
                    pg[g] = pg.get(g, 0) + float(v)
                if len(pg) > 1 or any(walls.get(i, {}).get("gauge") for i, _ in its):
                    extra += " | By gauge (stud gauge of each wall, from its type / stud schedule): " + "; ".join(f"{g} {_fmt(round(v, 2))} LF" for g, v in pg.items())
            elif fam in ("bottom track (todos)", "top / deflection track (todos)"):
                k = "bottom_lf" if fam.startswith("bottom") else "top_lf"
                sz = size_de(name)
                ren = [r for r in co["renglones"] if r.get(k)]
                pt = {f["wall"] for x in fo["partition_types"]["types"].values() for f in x["filas"]} | \
                     {i for x in fo["partition_types"]["types"].values() for f in x["filas"] for i in f["ids"]}
                if "roof step and heads" in name:     # R80e.67: renglón por ELEMENTO (canon.TRACK_HEADS), no todos los walls
                    ren = [r for r in ren if walls.get(r["id"][2:], {}).get("element") in
                           ("roof_step", "vestibule_head", "fascia_box", "ceiling_bulkhead", "soffit_side")]
                elif name.lower().startswith("parapet"):
                    ren = [r for r in ren if walls.get(r["id"][2:], {}).get("element") == "parapet"]
                elif sz:
                    ren = [r for r in ren if tamano_stud(walls.get(r["id"][2:], {}).get("stud_size")) == sz and r["id"][2:] in pt]   # BE-HF7
                    if k == "top_lf" and ("slip" in name.lower() or "standard" in name.lower()):   # R80w.31 / R80w.36
                        from canon import top_track_tramos
                        kk = "slip" if "slip" in name.lower() else "standard"
                        tram = {r["id"][2:]: (top_track_tramos(walls.get(r["id"][2:], {}), can, r[k]) or {}).get(kk) for r in ren}
                        ren = [dict(r, **{k: tram[r["id"][2:]][0]}) for r in ren if tram.get(r["id"][2:])]
                elif "other framing" in name:
                    # R80e.79: mismo criterio que canon.track_by_element: los elementos de TRACK_HEADS / parapet tienen
                    # su propio renglón y no van al de 'other framing' (antes: desglose 97.43 != NET 77.34, O'Reilly p2)
                    from canon import TRACK_HEADS, TRACK_PARAPET
                    ren = [r for r in ren if r["id"][2:] not in pt and r.get("element") not in TRACK_HEADS + TRACK_PARAPET]
                elif "openings between walls" in name:
                    # R80e.104: renglón 'other' de canon.track_by_element = renglones sin tamaño de stud (que no son
                    # heads / parapet / elemento fuera de la Partition Takeoff) + el RESTO de la familia que corridas no
                    # explica (track sobre openings entre walls). Antes no se filtraba: el desglose sumaba toda la familia (VS Downey).
                    from canon import TRACK_HEADS, TRACK_PARAPET
                    def _sz(r):
                        return walls.get(r["id"][2:], {}).get("stud_size") or r.get("stud_size")
                    ren = [r for r in ren if not _sz(r) and r.get("element") not in TRACK_HEADS + TRACK_PARAPET]
                its = [(r["id"][2:], r[k]) for r in ren]
                if "openings between walls" in name:
                    _resto = round(float(net) - sum(float(v) for _, v in its), 2)
                    if _resto > 0.01:
                        its.append(("rest of the family not in any wall row (track across openings between walls) = "
                                    "family total - sum of the per-size / element rows", _resto))
                kk_ = locals().get("kk") if (k == "top_lf" and sz and ("slip" in name.lower() or "standard" in name.lower())) else None
                if kk_:     # R80w.36: la fuente del kind = altura del stud vs B.O. deck (+ la regla del canon)
                    from canon import top_track_tramos
                    fk = [((top_track_tramos(walls.get(i, {}), can, v) or {}).get(kk_) or (0, ""))[1] for i, v in its]
                    cita = _nh(*[det.get(i, "") for i, _ in its], *fk,
                               str(((can.get("constants") or {}).get("slip_track_rule") or {}).get("source") or ""),
                               str((can.get("deck_height") or {}).get("source") or "") if isinstance(can.get("deck_height"), dict) else "")
                else:
                    cita = _nh(*[det.get(i, "") for i, _ in its],
                               *[walls.get(i, {}).get("top_track_kind_source") for i, _ in its if k == "top_lf"])
                if not cita and "openings between walls" in name:   # R80e.127: el resto (track sobre openings) sale del floor plan
                    cita = list(dict.fromkeys(str((w.get("band") or {}).get("sheet")) for w in walls.values()
                                              if isinstance(w.get("band"), dict) and (w.get("band") or {}).get("sheet")))[:3]
                extra = _desglose(its, net, "LF (wall length x rows)", name)
                pg = {}
                tgs = set()
                for i, v in its:
                    # CC-R4 (Consumer Cellular rev4, 5-nov): the printed track gauge (walls[].track_gauge {source}) governs;
                    # without it the track gauge = stud gauge of the wall (before: always the stud gauge, 18 ga where
                    # 2/A500 printed '20 GA' track)
                    g = walls.get(i, {}).get("track_gauge") or walls.get(i, {}).get("gauge")
                    if walls.get(i, {}).get("track_gauge"):
                        tgs.add(str(walls[i].get("track_gauge_source") or ""))
                    if g:
                        pg[g] = pg.get(g, 0) + float(v)
                if pg:
                    extra += (" | Track gauge as printed (" + "; ".join(sorted(t for t in tgs if t)) + "): " if tgs else
                              " | Track gauge = stud gauge of each wall: ") + "; ".join(f"{g} {_fmt(round(v, 2))} LF" for g, v in pg.items())
            elif fam == "bracing C.R. channel":
                its = [(r["id"][2:], r["bracing_lf"]) for r in co["renglones"] if r.get("bracing_lf")]
                its += items_filas(fam)                 # R80w.27: miembros de bracing del canon (misc_items) también
                cita = _nh(*[det.get(i, "") for i, _ in its], *[r.get("source") for r in filas_de(fam)])
                sp_ = ((can.get("constants") or {}).get("bracing_spacing_in") or {})      # BE-HF13: the spacing used
                sp_ = sp_.get("value") if isinstance(sp_, dict) else sp_
                mh_ = ((can.get("constants") or {}).get("bracing_min_height_ft") or {})
                extra = _desglose(its, net, f"LF (rows = ROUNDUP(H x 12 / {float(sp_ or 48):g}) - 1 or the rows declared, x length"
                                  + (f"; walls not higher than {mh_.get('value')} ft: 0 rows" if isinstance(mh_, dict) and mh_.get("value") else "")
                                  + ")", name)
            elif fam == "sill track" and unit == "LF":          # BE-HF16: per opening (R.O. + 1'-4") x pieces (headers.py)
                import headers as _H
                try:
                    hi_ = L("headers_in.json")
                except (OSError, ValueError):
                    hi_ = {}
                rs_ = [x for x in (_H.calcular(hi_).get("renglones") if hi_ else []) if x.get("sill_lf")]
                its = [(f"{x['ref']} ({x.get('wall')})", x["sill_lf"]) for x in rs_]
                its += items_filas(fam)              # v81cf24 (CFA rev5): sill track cargado como misc_item (recess / box) también
                cita = _nh(*[o.get("with_sill_source") or o.get("source") for o in hi_.get("openings") or [] if o.get("with_sill")],
                           *[r.get("source") for r in filas_de(fam)])
                cita += [h for h in dict.fromkeys(RX_HOJA.findall(" ".join(str(x.get("source") or "") for x in rs_))) if h not in cita]
                ops_s = "; ".join([f"{x['ref']}: {str(x.get('operacion')).split('; ')[-1]}" for x in rs_] +
                                  [str(r.get("operacion")) for r in filas_de(fam) if r.get("operacion")])
                extra = _desglose(its, net, "LF (sill track = (R.O. + 1'-4\") x sill pieces per opening"
                                  + ("; drawn sill pieces" if items_filas(fam) else "") + ")", name) + (" | " + ops_s if ops_s else "")
            elif fam == "track de ceilings / soffits" or fam in (fo.get("family_splits") or {}):
                spl = fo.get("family_splits") or {}
                its = [(r["id"].split(":", 1)[-1], r["ceiling_track_lf"]) for r in co["renglones"] if r.get("ceiling_track_lf")]
                its += items_filas("track de ceilings / soffits")
                if fam in spl:                       # v80p (R80e.31): renglón por tamaño = solo sus ítems
                    its = [x for x in its if x[0] in spl[fam]["items"]]
                    its += items_filas(fam)          # R80e.113: + ítems impresos cargados directo en la familia por tamaño
                    cita = _nh(spl[fam]["source"], *[det.get(i, "") for i, _ in its])
                else:
                    fuera = {i for v in spl.values() if v["from"] == fam for i in v["items"]}
                    its = [x for x in its if x[0] not in fuera]
                    cita = _nh(*[det.get(i, "") for i, _ in its], *[r.get("source") for r in filas_de("track de ceilings / soffits")])   # R80e.83
                    if not cita and any(i in {str(r.get("room")) for r in filas_de("ceilings")} for i, _ in its):
                        cita = _nh(*[r.get("source") for r in filas_de("ceilings")])   # BE-CC01: ceiling perimeter track cites its ceilings
                extra = _desglose(its, net, "LF", name)
            elif fam and (fam.startswith("5/8\" gyp") or fam.startswith("5/8\" glass mat tile backer") or fam in ("1/2\" gyp MOISTURE RESISTANT", "1/2\" gyp board", "1/2\" EXTERIOR gyp sheathing")):   # BE-GK34
                # R80e.39: cada familia de board con SU board (antes regular / MR caían en "5/8 type X")
                # BE-117f (v81cf11): 1/2" regular too (before: ops text without a per-ID breakdown, cut at 566 chars)
                bk = ("5/8 glass mat tile backer" if "DENS" in fam.upper() else
                      "1/2 exterior gyp sheathing" if fam == "1/2\" EXTERIOR gyp sheathing" else   # BE-GK34: wall faces in the breakdown   # BE-GK04b: Dens Shield faces (canon BOARD_FAM key)
                      "1/2 regular" if fam == "1/2\" gyp board" else "1/2 MR" if fam.startswith("1/2") else "5/8 foil-backed" if "FOIL" in fam.upper()
                      else "5/8 ceiling sag-resistant" if "SAG" in fam.upper()   # v81cf8 (T2)
                      else "5/8 type C" if "TYPE C" in fam.upper() else "5/8 exterior gyp sheathing type X" if "EXTERIOR" in fam.upper()   # v81cf53 BE-CR07
                      else "5/8 type X WR" if "W.R." in fam else "5/8 MR" if "MOISTURE" in fam.upper()
                      else "5/8 regular" if "regular" in fam else "5/8 type X")   # R80e.111
                pw = {}
                for c in bo["caras"]:
                    if c["board"] == bk:
                        pw[c["wall"]] = pw.get(c["wall"], 0) + c["sf"]
                its = list(pw.items())
                its += [(str(x.get("id") or "ceiling " + x["room"]), x["area_sf"] * (int((x.get("layers") or {}).get("value") or 1)
                         if x.get("system") == "resilient_channel" else 1)) for x in can.get("ceilings") or []   # BE-117f; BE-CR07 capas
                        if x.get("board") == bk and x.get("system") != "canopy_joist"]
                its += items_filas(fam)
                cita = _nh(*[det.get(i, "") for i in pw], *[x.get("detail") for x in can.get("ceilings") or [] if x.get("board") == bk],
                           *[r.get("source") for r in filas_de(fam)])   # R80e.72: sin hoja fija de otro proyecto
                extra = _desglose(its, net, "SF (faces: length x face height x layers - openings; ceilings: RCP area)", name)
            elif fam == "cement board":
                its = [(c["wall"] + " " + c["room"], c["sf"]) for c in bo["caras"] if "cement" in c["board"] and c["sf"]]
                its += items_filas(fam)
                cita = _nh(*[det.get(c["wall"], "") for c in bo["caras"] if "cement" in c["board"]], *[r.get("source") for r in filas_de(fam)])
                if not cita:   # R80e.127: cement board de tile_base / wet areas: la hoja del finish plan / schedule del canon
                    cita = _nh(*[str(t.get("source") or "") + " " + str((t.get("height_ft") or {}).get("source") if isinstance(t.get("height_ft"), dict) else "")
                                 for t in can.get("tile_base") or []],
                               *[str(x.get("source") or "") for x in can.get("wet_fixtures") or []])
                    cita = cita or list(dict.fromkeys(RX_HOJA.findall(" ".join(str(t.get("source") or "") for t in can.get("tile_base") or []))))
                extra = _desglose(its, net, "SF", name)
            elif fam == "FRT plywood (SF)":
                mat = "frt_3_4" if "3/4" in name else "frt_5_8"
                # R80e.39: el renglón es por material Y uso (canon.py PLY_USO_NOMBRE); antes el substrate sumaba también
                # el sheathing de column wraps / piers / canopy de su mismo espesor
                n_l = name.lower()
                uso_r = ("column_wrap" if "column wrap" in n_l else "pier" if "pier" in n_l else "canopy_soffit"
                         if "canopy and soffit" in n_l else "nailbase" if "polyiso" in n_l else "substrate")

                def uso_f(r):
                    t = (str(r.get("uso") or "") + " " + str(r.get("operacion") or "")).lower()
                    return ("column_wrap" if "column_wrap" in t else "pier" if "pier" in t else "canopy_soffit"
                            if "canopy_soffit" in t else "nailbase" if "nailbase" in t else "substrate")
                fil = [r for r in filas_de(fam, mat) if uso_f(r) == uso_r]
                refs = {str(r.get("ref") or r.get("room") or r.get("source")) for r in fil}
                its = [x for x in items_filas(fam, mat) if x[0] in refs]
                cita = _nh(*[r.get("source") for r in fil]) + []
                wx = can.get("wood_excluded")            # U-139: plywood = wood (Div. 06) -> EXCLUDED en 0, sin desglose
                if isinstance(wx, dict) and abs(float(net or 0)) < 1e-9:
                    extra = (f"EXCLUDED - {wx.get('why')} ({wx.get('source')}): "
                             + "; ".join(dict.fromkeys(str(r.get("ref")) for r in filas_de(fam) if r.get("ref"))))[:900]
                else:
                    extra = _desglose(its, net, "SF (strip length x height)", name)
            elif fam in ("FRT blocking", "8\" joist", "8\" stud (todos los gauges)", "curved perimeter molding (printed)") \
                    or fam and fam.startswith("USG") \
                    or fam == "metal trim (corner bead, casing, shadow molding)":
                its = items_filas(fam)
                if fam == "FRT blocking":                   # madera sin rótulo FRT va en su renglón propio (v76)
                    madera = {b["ref"] for b in can.get("blocking_items") or [] if b.get("material") == "wood"}
                    its = [x for x in its if (x[0] in madera) == name.lower().startswith("blocking 2x wood")]
                cita = _nh(*[r.get("source") for r in filas_de(fam)])
                if fam.startswith("USG") or fam in ("8\" joist", "curved perimeter molding (printed)"):
                    extra = "; ".join(str(r.get("operacion")) for r in filas_de(fam))[:600] or \
                        "; ".join(str(r.get("operacion")).split("; hangers")[0] for r in filas_de("ceilings") if "usg_grid" in str(r.get("operacion")))
                    if not cita:                    # R80w.28: el grid cita el detalle / hoja de sus ceilings
                        cita = _nh(*[r.get("source") for r in filas_de("ceilings")])
                    if not cita:
                        cita = ["default (no sheet)"]   # R80e.83: never a sheet of another project
                elif fam == "FRT blocking" and isinstance(can.get("wood_excluded"), dict) and abs(float(net or 0)) < 1e-9:
                    wx = can["wood_excluded"]                # U-139: wood blocking EXCLUDED en 0 (R-ALC-01), sin desglose
                    extra = (f"EXCLUDED - {wx.get('why')} ({wx.get('source')}): "
                             + "; ".join(dict.fromkeys(str(r.get("ref")) for r in filas_de(fam) if r.get("ref"))))[:900]
                else:
                    extra = _desglose(its, net, unit, name)
            elif "hanger" in name.lower():
                hp = fo.get("hanger_pcs") or {}
                its = [(x["room"], x["lf"] if unit == "LF" else x["pcs"]) for x in hp.get("por_room") or []]
                if unit == "LF":
                    its += items_filas("hanger wire")       # v80n: hangers / wires dibujados en el detalle (misc_items)
                cita = _nh(*[r.get("source") for r in filas_de("ceilings")], *[r.get("source") for r in filas_de("hanger wire")]) \
                    or ["default (no sheet)"]   # R80e.83; BE-GK09: the hanger wires drawn in a detail (misc_items) cite their own sheet
                extra = _desglose(its, net, unit + (" (hangers @ 48\" O.C. x drop to deck per room)" if unit == "LF" else " (one per hanger)"), name)
            elif fam in ("furring channel", "carrying channel"):
                k_ = "furring" if fam.startswith("furring") else "carrying"
                its = items_filas(fam) or [(r.get("room") or "ceiling", float(g.group(1)))
                                           for r in filas_de("ceilings")
                                           for g in [re.search(k_ + r" [^;]*?= \d+ x [\d.]+ = ([\d.]+)", str(r.get("operacion")))] if g]
                cita = _nh(*[r.get("source") for r in filas_de("ceilings")]) or ["default (no sheet)"]   # R80e.83
                try:
                    extra = _desglose(its, net, "LF", name)
                except ValueError:
                    extra = "per ceiling: furring @ 24\" O.C., carrying @ 48\" O.C. x RCP extent (see the ceiling rows)"
            elif acc:
                rs = filas_de(fam) if fam else []
                cita = _nh(src0, *[r.get("source") for r in rs]) or \
                    [h for h in dict.fromkeys(RX_HOJA.findall(" ".join([src0] + [str(r.get("source")) for r in rs])))]
                if "Inputs" in src0:
                    # v80p (R80e.31): el yield cita la nota impresa que fija el producto; framing screws lleva su desglose
                    cita = cita or ["driver = the board / stud / bottom track rows of this sheet"]
                    if fam == "slab pins":               # v80q: el espaciamiento cargado es la nota 8.F
                        cita = ["slab pin spacing: see the operation (Inputs yield)"]
                    if fam == "framing screws":
                        try:
                            ao = L("accesorios_out.json")
                            op_ = next((r["operacion"] for r in ao.get("filas") or [] if r.get("familia") == fam), "")
                        except (OSError, ValueError):
                            op_ = ""
                        if op_:
                            extra = "Breakdown [DERIVED]: " + op_
                if not net:                                   # renglón en 0: el porqué con su hoja (canon)
                    why = None
                    for x in can.get("accesorios_none") or []:
                        if x.get("familia") == fam:
                            why = f"none: {x.get('why')} ({x.get('source')})"
                    for x in can.get("accesorios_rfi") or []:
                        if x.get("familia") == fam:
                            why = f"RFI: {x.get('motivo')} Delta: {x.get('delta')}"
                    if not why:   # R80e.127: RFI de la tool (accesorios_out.rfis): el porqué cita la hoja de los ítems del canon
                        try:
                            _ao = L("accesorios_out.json")
                        except (OSError, ValueError):
                            _ao = {}
                        for x in _ao.get("rfis") or []:
                            if x.get("familia") == fam:
                                _refs = set(x.get("items") or [])
                                _src = " ".join(str(o.get("ro_source") or "") + " " + str(o.get("head_source") or "") + " " + str(o.get("source") or "")
                                                for o in can.get("openings_extra") or [] if o.get("ref") in _refs)
                                _h = _nh(_src) or list(dict.fromkeys(RX_HOJA.findall(_src)))
                                why = (f"RFI pending: {x.get('tema')} Delta {x.get('delta')} {x.get('unidad')} "
                                       f"({', '.join(sorted(_refs))}{'; ' + ', '.join(_h) if _h else ''})")
                    if fam == "PVC trim at FRP" and can.get("frp_none_reason"):
                        why = "none: " + can["frp_none_reason"]
                    if fam == "deflection clips" and (can.get("deflection_clips") or {}).get("none_reason"):
                        why = "none: " + can["deflection_clips"]["none_reason"]
                    if fam == "expansion anchors" and not why:      # R80w.29: el motivo del canon (con hoja) manda
                        why = "none: no exterior wall on slab in the set"
                    if fam in ("PAFs and duct sleeves", "2-1/2\" CFMF coiling grille head") and not why:
                        why = "none: no parapet infill, coiling grille or duct sleeve detail in the set"
                    fx = can.get("fasteners_excluded")             # R80e.77: tornillería excluida por el estimador
                    if isinstance(fx, dict) and fam in ("drywall screws", "drywall screws heavy gauge", "framing screws",
                                                        "framing screws heavy gauge", "slab pins", "expansion anchors",
                                                        "PAFs and duct sleeves"):
                        prev = next((str(r.get("operacion")) for r in filas_de(fam) if str(r.get("operacion", "")).startswith("EXCLUDED")), "")
                        why = prev or f"EXCLUDED - {fx.get('why')} ({fx.get('source')})"
                    extra = why or "none in the set"
                    cita = cita or _nh(extra) or list(dict.fromkeys(RX_HOJA.findall(extra)))
                elif "Inputs" not in src0:
                    extra = "; ".join(dict.fromkeys(str(r.get("operacion")) for r in rs if r.get("operacion")))[:3000]   # v80r: sin cortar
            else:
                rs = filas_de(fam) if fam else []
                cita = _nh(src0, *[r.get("source") for r in rs]) or \
                    list(dict.fromkeys(RX_HOJA.findall(" ".join(str(r.get("source")) for r in rs))))
                its = items_filas(fam) if fam else []
                ops = "; ".join(dict.fromkeys(str(r.get("operacion")) for r in rs if r.get("operacion")))
                if its:
                    try:
                        extra = _desglose(its, net, unit, name) + (f" | {ops[:3000]}" if len(its) <= 3 else "")
                    except ValueError:
                        extra = ops[:500]
        except ValueError:
            raise
        # BE-117d (v81cf11): the row cites EVERY sheet of its listed items (same rule as the per-product split below):
        # bare sheets of the item sources that no N/SHEET already covers are added (a markup DETAIL citing A-221 must
        # find A-221 in its Excel row; before, a row with any N/SHEET dropped the bare sheets of its items)
        if its and cita and not any(str(x).startswith(("default", "driver", "slab pin")) for x in cita):
            for h in dict.fromkeys(RX_HOJA.findall(" ".join(_src_item(x_[0], can) for x_ in its if isinstance(x_, (list, tuple)) and x_))):
                if h not in cita and not any(str(x).endswith("/" + h) for x in cita):
                    cita.append(h)
        if not cita and "edge of gypboard" in name.lower():   # BE-GK10: edge blocking (R78.33) cites the source of constants.sheet_len_ft
            _sl = str(((can.get("constants") or {}).get("sheet_len_ft") or {}).get("source") or "")
            cita = _nh(_sl) or list(dict.fromkeys(RX_HOJA.findall(_sl)))
        if not cita:      # BE-HF8 (HFT Loveland): no N/SHEET bubble in the item sources ("A4.1 Wall Type Note 5", a window of
            # A1.1): the bare sheets of the item / family-row sources are the citation, not "default (no sheet)"
            srcs = [_src_item(x_[0], can) for x_ in (its or []) if isinstance(x_, (list, tuple)) and x_]
            srcs += [str(r.get("source") or "") for r in (filas_de(fam) if fam else [])]
            if fam == "sill track":          # the sill track comes from headers.py: openings with_sill + their source
                try:
                    srcs += [str(o.get("with_sill_source") or o.get("source") or "") for o in L("headers_in.json").get("openings") or []
                             if o.get("with_sill")]
                except (OSError, ValueError):
                    pass
            cita = _nh(*srcs) or list(dict.fromkeys(RX_HOJA.findall(" ".join(srcs))))
        src = str(m.get("source") or "")
        estado = re.search(r"\[(DERIVED|CONFIRMED|PENDING|RFI|CRITERION|None)\]", src)
        yld = re.sub(r"^accesorios\.py \[[^\]]*\]:\s*", "", src) if "Inputs" in src else ""
        partes = []
        partes.append(("N/SHEET: " + ", ".join(cita)) if cita else "N/SHEET: default (no sheet)")   # R80e.83
        if yld:
            partes.append(yld)
        if extra:
            partes.append(extra)
        txt = " | ".join(partes)
        if estado and estado.group(1) not in ("None",):
            txt = f"[{estado.group(1)}] " + txt
        txt = RX_INTERNO.sub("", txt).replace("  ", " ").replace("usg_grid:", "drywall suspension grid:")   # R80w.28: sin marca
        # R80e.85 (BE-46): UN producto por renglón. Si el desglose del renglón mezcla productos (designación SSMA
        # del stud / track, tipo de trim, tipo de clip), el renglón se parte en uno por producto con su propio desglose.
        grupos = _por_producto(name, fam, its, walls, can) if its else None
        # R80e.112: guard — se parte solo si los ítems del renglón suman SU NET (dos renglones de una misma familia
        # no reciben cada uno la familia entera: VS Downey duplicaba el blocking)
        if grupos and abs(sum(float(v) for _, v in its) - float(net)) > max(0.5, 0.005 * float(net or 0)):
            grupos = None
        if grupos and len(grupos) == 1 and next(iter(grupos)) not in ("per source",) and not str(name).endswith(" - " + next(iter(grupos))):
            mats.append(dict(m, material=f"{name} - {next(iter(grupos))}", cita=txt + _nota_ms(name, can)))   # U-177 (3) / BE-GK30: gauge / producto también con un solo producto
            continue
        if grupos and len(grupos) > 1:
            for prod, gi in grupos.items():
                nn = round(sum(v for _, v in gi), 2)
                ci = _nh(*[det.get(i, "") for i, _ in gi], *[_src_item(i, can) for i, _ in gi])
                ci += [h for h in dict.fromkeys(RX_HOJA.findall(" ".join(_src_item(i, can) for i, _ in gi)))
                       if not any(x.endswith("/" + h) for x in ci)]
                ci = ci or cita
                tx = ("N/SHEET: " + ", ".join(ci)) if ci else "N/SHEET: default (no sheet)"
                tx += " | " + _desglose(gi, nn, unit, name)
                if estado and estado.group(1) not in ("None",):
                    tx = f"[{estado.group(1)}] " + tx
                tx = RX_INTERNO.sub("", tx).replace("  ", " ")
                mats.append(dict(m, material=f"{name} - {prod}", net=nn, cita=tx + _nota_ms(f"{name} - {prod}", can),
                                 familia=m.get("familia") or fam))
            continue
        mats.append(dict(m, cita=txt + _nota_ms(name, can)))
    d = dict(d, materials=mats)

    # Partition Takeoff: alturas por cara donde Board (SF) != L x H x Layers
    def nota(row):
        ids = [i for i in str(row["wall"]).split("+") if i in walls]
        L_, H_, ly = float(row["length_lf"]), float(row["height_ft"]), float(row["layers"] or 0)
        if abs(float(row["board_sf"] or 0) - L_ * H_ * ly) <= 0.5 and abs(ly - round(ly)) < 0.01 \
                and not any(walls[i].get("faces_note") for i in ids):
            return None                                  # faces_note del canon: la fila dice siempre qué cara lleva board
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
    def gauge(row):                                  # v80n (R80e.27): gauge del schedule en la columna Stud Size
        gs = [walls[i].get("gauge") for i in str(row["wall"]).split("+") if i in walls and walls[i].get("gauge")]
        return " / ".join(dict.fromkeys(str(g) for g in gs)) or None     # un gauge numérico (20) también vale
    for k in ("walls", "other_framing"):
        d[k] = [dict(w, **({"faces_note": nota(w)} if nota(w) else {}), **({"gauge": gauge(w)} if gauge(w) else {}))
                for w in d.get(k) or []]
    return d

def _en(t):
    """texto de una tool en inglés (traducción de plantilla_excel.en, import tardío: plantilla importa este módulo)."""
    try:
        from plantilla_excel import en
        t = en(t)
    except Exception:                                   # noqa: BLE001
        pass
    for a, b in (("sin extras de nodo", "no node extras"), ("dentro de R.O.", "inside R.O."), ("campo", "field"),
                 ("nodos", "nodes"), ("total", "total")):
        t = t.replace(a, b)
    return t


DESIG = re.compile(r"\b\d{3,4}(?:S|T|ZF|F)\d{3}-\d{2}\b")   # BE-GK30: 1000S162-43 (10" studs) too
TRIM_PROD = {"corner_bead": "corner bead", "casing_bead": "casing (J) bead", "j_bead": "J molding",
             "shadow_molding": "reveal molding", "edge_trim": "gypsum edge trim"}


def _item(i, can):
    for k in ("misc_items", "trim_items", "blocking_items", "plywood_strips"):
        for x in can.get(k) or []:
            if x.get("ref") == i:
                return x
    return None


def _src_item(i, can):
    x = _item(i, can)
    return str(x.get("source") or "") if x else ""


def _nota_ms(name, can):
    """R80w.47: nota de decisión / verificación por renglón del Material Summary (constants.ms_notes
    [{match: regex sobre el nombre del renglón, note: texto, source}]): ' | <note>' al final de 'Where it comes from'."""
    out = []
    for x in ((can.get("constants") or {}).get("ms_notes") or []):
        if not (isinstance(x, dict) and x.get("match") and str(x.get("note") or "").strip() and str(x.get("source") or "").strip()):
            raise ValueError(f"constants.ms_notes: {{match, note, source}} obligatorios ({x})")
        if re.search(x["match"], str(name), re.I):
            out.append(str(x["note"]))
    return "".join(" | " + t for t in out)


def tamano_stud(s):
    """BE-HF7 (HFT Loveland): the stud size of a wall for the per-size track breakdown = its leading printed size
    ('6" (600S162-54)' -> '6"'), the same reading canon.track_by_element makes (STUD_FAM 'contains'); the exact-string
    comparison dropped walls whose stud_size carries the designation -> 'desglose suma != NET' and no Excel."""
    m = re.match(r'\s*(\d+(?:-\d+/\d+)?(?:\.\d+)?)\s*"', str(s or ""))
    return (m.group(1) + '"') if m else s


def _producto_impreso(x):
    """U-177 (4): producto impreso de un item ('product' str o {value, source}) sin el comentario entre paréntesis del final
    ('6" sheet metal blocking strapping (metal - included; gauge not printed)' -> '6" sheet metal blocking strapping')."""
    pr = (x or {}).get("product")
    v = pr.get("value") if isinstance(pr, dict) else pr
    v = re.sub(r"\s*\([^()]*\)\s*$", "", str(v or "")).strip()
    v = re.sub(r'(\d) (\d/\d)"', r'\1-\2"', v)                # 1 1/2" == 1-1/2"
    return v or None


def _por_producto(name, fam, its, walls, can):
    """R80e.85: {producto: [(id, valor)]} para los renglones de stud / track / trim / clips; None si no aplica."""
    n = name.lower()
    es_track = "track" in n and fam in ("bottom track (todos)", "top / deflection track (todos)")
    es_stud = bool(fam) and _es_fam_stud(fam)
    es_trim = fam == "metal trim (corner bead, casing, shadow molding)"
    es_clip = fam == "clip angle (bracing / nested connections)"
    es_dlt = fam == "deep-leg slotted deflection track (printed)"      # R80e.85: deep-leg por ancho de web
    es_sf = fam == "storefront structural framing (printed)"           # R80e.110: por miembro impreso
    es_blk = fam == "metal stud blocking (362CR / STUD BLOCKING)" and "wall-mounted" in n   # R80e.112: backing track vs plate impresos (solo el renglón de wall-mounted items)
    # BE-GK30 / U-177 (3): framing families without their own split (ceiling / soffit track, header, sill, additional head track,
    # parapet / 10" studs, brace to structure) are grouped by the designation in the item text or, for an opening, by the gauge of its wall
    es_otro = bool(fam) and bool(re.search(r"track de ceilings|sill track|additional head track|header / box beam|parapet stud|"
                                           r"10\" stud|1-5/8\" stud|brace to structure", str(fam), re.I))
    if not (es_track or es_stud or es_trim or es_sf or es_blk or es_otro):          # R80w.49: misc_items con producto impreso propio (otra compra)
        pr = {i: (_item(i, can) or {}).get("product") for i, _ in its}
        if any(isinstance(x, dict) and str(x.get("value") or "").strip() and str(x.get("source") or "").strip()
               for x in pr.values()):
            out = {}
            for i, v in its:
                x = pr.get(i)
                k = str(x["value"]) if isinstance(x, dict) and str(x.get("value") or "").strip() else "per source"
                out.setdefault(k, []).append((i, v))
            return out
    if es_otro and not (es_track or es_stud):
        out = {}
        for i, v in its:
            x = _item(i, can)
            txt = " ".join(str((x or {}).get(k) or "") for k in ("label", "op", "source")) if x else ""
            g = DESIG.search(txt)
            if not g:
                mw = re.search(r"\(([A-H]1?-Z\d-\d{2})\)", str(i)) or re.search(r"\b([A-H]1?-Z\d-\d{2})\b", str(i)) \
                    or re.search(r"\(([^()]+)\)\s*$", str(i))          # U-177 (3): vano '<ref> (<wall>)' de cualquier proyecto
                w_ = walls.get(mw.group(1)) if mw else None
                g = DESIG.search(str((w_ or {}).get("gauge") or "")) if w_ else None
            prod = g.group(0) if g else "per source"
            if re.search(r"track|sill|header", str(fam), re.I) and "S" in prod and "per source" not in prod:
                prod = re.sub(r"^(\d{3,4})S\d{3}-(\d{2})$", r"\1T125-\2", prod)
            out.setdefault(prod, []).append((i, v))
        return out
    if not (es_track or es_stud or es_trim or es_clip or es_dlt or es_sf or es_blk or es_otro):
        return None
    out = {}
    for i, v in its:
        w, x = walls.get(i), _item(i, can)
        txt = " ".join(str((x or {}).get(k) or "") for k in ("label", "op", "source")) if x else ""
        prod = None
        if es_trim:
            if i == "jamb returns":                       # corner bead + casing por borde (2 x el LF del borde)
                out.setdefault("corner bead", []).append((i + " (corner bead)", round(v / 2, 2)))
                out.setdefault("casing (J) bead", []).append((i + " (casing)", round(v - round(v / 2, 2), 2)))
                continue
            k = (x or {}).get("kind")
            prod = TRIM_PROD.get(k, "metal trim")
            pr = (x or {}).get("product")             # R80w.42: producto impreso en el spec para ese item (otra pieza)
            if isinstance(pr, dict) and str(pr.get("value") or "").strip() and str(pr.get("source") or "").strip():
                out.setdefault(str(pr["value"]), []).append((i, v))
                continue
            lab = str((x or {}).get("label") or "")
            for code in ("JDM-625", "DRMF-625-75"):           # el código del PROPIO rótulo (el op cita los dos)
                if code in lab:
                    prod = f"Fry {code} " + ("J molding" if code.startswith("JDM") else "reveal molding")
                    break
        elif es_dlt:
            g = re.search(r'(\d+(?:-\d+/\d+)?)" web', txt)
            prod = f"{g.group(1)}\" web" if g else "per source"
        elif es_clip:
            prod = "L4x4x3/16 x 1'-0\" clip angle" if re.search(r"L ?4x4", txt) else \
                ("2\"x2\"x14ga clip" if "2\"x2\"x14ga" in txt else None)
            if prod is None:                               # R80e.110: designación del clip en su propio rótulo
                g = re.search(r"(\d+(?:[ -]\d/\d)?\"?\s*x\s*\d+(?:[ -]\d/\d)?\"?\s*x\s*(?:\d+'?-?\d*\"?\s*x\s*)?\d+\s*ga)", txt, re.I)
                if g:                                      # normaliza: 2X2 X 16 GA == 2" x 2" x 16 GA
                    z = re.sub(r'\s*x\s*', ' x ', re.sub(r'"', '', g.group(1)), flags=re.I)
                    z = re.sub(r'\s*ga$', ' ga', z, flags=re.I).strip()
                    parts = z.split(' x ')
                    z = ' x '.join([p.strip() + ('"' if i < len(parts) - 1 and not p.strip().endswith("'") else '') for i, p in enumerate(parts)])
                prod = (z + " clip") if g else "clip (per source)"
        elif es_blk and _producto_impreso(x):              # U-177 (4): el producto IMPRESO del item nombra el renglón
            prod = _producto_impreso(x)
        elif es_blk:                                       # R80e.112: producto impreso del item (product / label)
            p = str((x or {}).get("product") or "") + " " + txt
            g = re.search(r'(\d+(?:-\d/\d)?"\s*x\s*\d+\s*GA\s*backing\s*(?:track|plate))', p, re.I)
            # CC-R6 (Consumer Cellular rev4): the printed product names the row - '20 GA. METAL STRAPPING' (1-3/A104),
            # '20 GA BACKING PLATE' (4/A104), '20 GA. TRACK' (5/A402); never 'stud blocking' for a strap or a plate
            g2 = None if g else re.search(r"\b(\d+)\s*GA\.?\s*(METAL\s+STRAPPING|BACKING\s+PLATE|TRACK)\b", p, re.I)
            prod = g.group(1) if g else (f"{g2.group(1)} GA {' '.join(g2.group(2).lower().split())}" if g2 else
                                         ("stud blocking (per source)" if not re.search(r"backing", p, re.I) else "backing (per source)"))
        elif es_sf:                                        # R80e.110: tamaño + calibre + stud / track del rótulo
            g = re.search(r'(DBL\s+)?(\d+(?:\s\d/\d)?)"\s*(?:DP,?\s*)?,?\s*(\d+)\s*GA', txt, re.I)
            kind = "track" if re.search(r"\btrack\b", str((x or {}).get("label") or (x or {}).get("ref") or ""), re.I) else "stud"
            prod = (f'{(g.group(1) or "").upper()}{g.group(2)}" {g.group(3)} ga {kind}') if g else "per source"
        else:
            if not w and not x:                            # U-177 (3): header de un vano '<ref> (<wall>)' = gauge del wall que lo aloja
                mw = re.search(r"\(([^()]+)\)\s*$", str(i))
                w = walls.get(mw.group(1)) if mw else None
            g = DESIG.search(str((w or {}).get("gauge") or "")) if w else DESIG.search(txt)
            prod = g.group(0) if g else None
            if prod and es_stud and not re.match(r"^\d{3}S\d{3}-\d{2}$", prod):
                prod = None                              # R80w.21: un stud se agrupa solo por designación de STUD (S)
            if prod and (es_track or fam == "track de ceilings / soffits") and "S" in prod:
                prod = re.sub(r"^(\d{3})S\d{3}-(\d{2})$", r"\1T125-\2", prod)
            _stp = ((can.get("constants") or {}).get("slip_track_product") or {})   # BE-GK13: product printed in the deflection detail
            if prod and es_track and re.search(r"slip / deflection", str(n), re.I) and isinstance(_stp, dict) \
                    and re.fullmatch(r"T\d{3}-\d{2}", str(_stp.get("value") or "")) and str(_stp.get("source") or "").strip():
                prod = re.sub(r"^(\d{3})T\d{3}-\d{2}$", r"\1" + _stp["value"], prod)
            prod = prod or "per source"
            ps = ((can.get("constants") or {}).get("product_specs") or {}).get(prod)   # R80w.42: grado / recubrimiento
            if isinstance(ps, dict) and str(ps.get("value") or "").strip() and str(ps.get("source") or "").strip():
                prod = f"{prod} {ps['value']}"
        out.setdefault(prod, []).append((i, v))
    return out
