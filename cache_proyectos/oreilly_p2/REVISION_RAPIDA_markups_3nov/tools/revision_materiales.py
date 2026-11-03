#!/usr/bin/env python3
"""revision_materiales.py (O'Reilly 3-nov-2026) — revisión NO circular de materiales contra el Partition Type Schedule.

Entrada 1 = fichas.json de una LECTURA INDEPENDIENTE del schedule (un subagente que no vio el Excel ni el canon): por type,
stud size / designación SSMA / gauge / O.C., board por cara (lado, capas, tipo, espesor), track / slip track, altura que
cubre y extras, cada dato con su N/HOJA. Entrada 2 = el Excel de formato fijo (Partition Takeoff + Material Summary) y el
canon / salidas de canon.py de la entrega.
Por type: VERDE = el Excel cargó lo que dice el schedule; ROJO = no coincide (con el recorte del type del schedule y su
N/HOJA); ÁMBAR = el schedule no lo dice (se anota la fuente que usó el take-off: nota general, spec o detalle).
Suma: cada renglón de board / studs del Material Summary = Σ de walls por type + ítems que no son wall con su fuente;
ROJO todo material sin origen o con diferencia.

Uso: python3 revision_materiales.py fichas.json takeoff.xlsx takeoff_canon.json calc_out_dir out_dir [--title T]
Test: python3 test_revision_materiales.py
"""
import argparse
import json
import os
import re
import shutil
import sys

TOL = 0.01   # 1 % en sumas


def _txt(x):
    return str(x or "").lower()


def tipo_board(s):
    """'5/8" Type X W.R.' -> 'X-WR'; '5/8 type X' -> 'X'; MR / W.R. sin X -> 'WR'; regular -> 'REG'."""
    t = _txt(s)
    wr = bool(re.search(r"\bw\.?r\.?\b|moisture|\bmr\b", t))
    x = bool(re.search(r"type\s*['\"]?x|\btype x\b|\bx\b", t))
    if "glass mat" in t:
        return "GLASSMAT"
    if x and wr:
        return "X-WR"
    if x:
        return "X"
    if wr:
        return "WR"
    return "REG" if t else None


def ft_aff(s):
    m = re.search(r"(\d+)'\s*-?\s*(\d+(?:\.\d+)?)?\"?\s*A\.?F\.?F", str(s or ""), re.I)
    return int(m.group(1)) + float(m.group(2) or 0) / 12 if m else None


def leer_excel(xlsx):
    import openpyxl
    wb = openpyxl.load_workbook(xlsx, data_only=True)
    ws = wb["Partition Takeoff"]
    rows, tipo = [], None
    for r in ws.iter_rows(min_row=5, values_only=True):
        a = str(r[0] or "")
        if a.startswith("TYPE "):
            tipo = a[5:].strip()
            continue
        if r[1] and isinstance(r[2], (int, float)) and not str(r[1]).startswith(("SUBTOTAL", "TOTAL")):
            rows.append({"type": tipo, "wall": str(r[1]), "lf": float(r[2]), "h": float(r[3]), "layers": r[4],
                         "stud": str(r[5] or ""), "oc": r[6], "board_sf": r[7], "location": str(r[8] or ""),
                         "source": r[9]})
    ms = []
    for i, r in enumerate(wb["Material Summary"].iter_rows(min_row=4, values_only=True), start=4):
        if r[0] and isinstance(r[2], (int, float)):
            ms.append({"row": i, "name": str(r[0]), "unit": r[1], "net": float(r[2]), "where": str(r[8] or "")})
    return rows, ms


NO_IMPRESO = re.compile(r"not printed|per arch|sheathing per|see arch", re.I)


def _lados(caras):
    """caras distintas que imprime el schedule: 'each side' / 'both sides' = 2; si no, un lado por texto distinto."""
    if any(re.search(r"each|both", _txt(c.get("side"))) for c in caras):
        return 2
    return len({_txt(c.get("side")).split(" (")[0] for c in caras}) or 1


def _caras_wall(wid, cw, misc):
    """caras con board del wall + las del wall pareado (adjacent_to: 6" + 8" lado a lado = un assembly) + el sheathing
    exterior cargado como misc_item del assembly (glass mat), que en el canon no va como cara."""
    w = cw.get(wid) or {}
    ids = [wid] + ([w["adjacent_to"]] if w.get("adjacent_to") else []) + [k for k, v in cw.items() if v.get("adjacent_to") == wid]
    fc = [x for i in ids for x in (cw.get(i) or {}).get("faces") or [] if x.get("board") and float(x.get("height_ft") or 0) > 0]
    pref = re.sub(r"\d*-\d+$", "", wid)
    for m in misc:
        if tipo_board(m.get("familia")) == "GLASSMAT" and len(pref) >= 4 and str(m.get("ref", "")).endswith("-" + pref):
            fc.append({"side": "EXT:" + m["ref"], "board": m["familia"], "layers": 1, "height_ft": 1})
    return fc


def comparar_type(t, ficha, filas, cw, misc=()):
    """-> dict(type, verdict, checks[{campo, schedule, excel, estado, nota}])."""
    checks = []

    def add(campo, sch, exc, estado, nota=""):
        checks.append({"field": campo, "schedule": sch, "excel": exc, "status": estado, "note": nota})

    src = ficha.get("sources") or {}
    if not filas:
        add("walls", f"type {t} in the schedule", "no wall of this type in the Excel", "AMBER",
            "type not used on the plan, or carried under another name")
        return {"type": t, "verdict": "AMBER", "checks": checks, "img": ficha.get("img")}
    # stud designation / gauge / O.C.
    des = ficha.get("stud_designation")
    if des:
        alts = [x.strip().upper() for x in re.split(r"\+|/|,| or ", des) if x.strip()]
        mal = [f["wall"] for f in filas if not any(x in f["stud"].upper() for x in alts)]
        add("stud designation", f"{des} ({src.get('stud', '')})", "; ".join(sorted({f['stud'] for f in filas})),
            "RED" if mal else "GREEN", ("walls: " + ", ".join(mal)) if mal else "")
    else:
        add("stud designation", "not printed in the type", "; ".join(sorted({f['stud'] for f in filas})), "AMBER",
            src.get("stud", ""))
    ga = ficha.get("gauge_ga")
    if ga:
        mal = [f["wall"] for f in filas if not re.search(rf"\b{int(ga)}\s*ga\b", f["stud"])]
        add("gauge", f"{ga} ga", "; ".join(sorted({(re.search(r'\d+\s*ga', f['stud']) or [''])[0] for f in filas})),
            "RED" if mal else "GREEN", ("walls: " + ", ".join(mal)) if mal else "")
    oc = ficha.get("oc_in")
    if oc:
        mal = [f["wall"] for f in filas if f["oc"] and abs(float(f["oc"]) - float(oc)) > 0.01]
        add("stud O.C.", f"{oc}\" O.C.", "; ".join(sorted({str(f['oc']) for f in filas})), "RED" if mal else "GREEN",
            ("walls: " + ", ".join(mal)) if mal else "")
    else:
        add("stud O.C.", "not printed in the type", "; ".join(sorted({str(f['oc']) for f in filas})), "AMBER", src.get("stud", ""))
    # board por cara
    caras_todas = ficha.get("faces") or []
    caras = [c for c in caras_todas if c.get("board") and not NO_IMPRESO.search(c.get("board"))]
    if caras_todas and not caras:
        add("board", "; ".join(f"{c.get('side')}: {c.get('board')}" for c in caras_todas), "see Board by face", "AMBER",
            "board not printed in this detail (refers to architectural)")
    elif caras:
        n_sch = _lados(caras_todas)
        bt_sch = {tipo_board(c.get("board")) for c in caras}
        lay_sch = max(int(c.get("layers") or 1) for c in caras)
        for f in filas:
            for wid in f["wall"].split("+"):
                fc = _caras_wall(wid, cw, misc)
                lados = {x.get("side") for x in fc}
                bts = {tipo_board(x.get("board")) for x in fc}
                lay = max([int(x.get("layers") or 1) for x in fc] or [0])
                if not fc:
                    add(f"board faces {wid}", f"{n_sch} face(s) {sorted(bt_sch)}", "no board face", "RED")
                    continue
                req = n_sch - (len(caras_todas) - len(caras))   # caras "not printed" no se pueden exigir
                if (len(lados) != n_sch) if req == n_sch else (len(lados) < req):
                    add(f"board faces {wid}", f"{n_sch} face(s) ({src.get('board', '')})", f"{len(lados)} face(s)", "RED")
                if lay != lay_sch:
                    add(f"board layers {wid}", f"{lay_sch} layer(s)", f"{lay} layer(s)", "RED")
                for b in bts:
                    if b in bt_sch:
                        continue
                    if b == "X-WR" and "X" in bt_sch:       # W.R. por nota general de wet rooms: no lo dice el type
                        add(f"board type {wid}", f"{sorted(bt_sch)} ({src.get('board', '')})", "Type X W.R. on a wet-room face",
                            "AMBER", "W.R. comes from the general note for wet rooms, not from the type")
                    else:
                        add(f"board type {wid}", f"{sorted(bt_sch)} ({src.get('board', '')})", b, "RED")
        if caras and not any(c["field"].startswith("board") for c in checks):
            add("board", f"{n_sch} face(s) {sorted(bt_sch)}, {lay_sch} layer(s)", "same on every wall", "GREEN")
    else:
        add("board", "not printed in the type", "", "AMBER", src.get("board", ""))
    # altura que cubre
    h_sch = ft_aff(ficha.get("height"))
    if h_sch and re.search(r"roof|structure|deck|framing above", _txt(ficha.get("height"))):
        h_sch = None          # altura mixta (A.F.F. en una zona, a estructura en otra): no se compara un solo número
    if h_sch:
        mal = [f["wall"] for f in filas if abs(f["h"] - h_sch) > 0.01]
        add("height", f"{ficha.get('height')} ({src.get('height', '')})", "; ".join(sorted({f'{f["h"]:.3f}' for f in filas})),
            "RED" if mal else "GREEN", ("walls: " + ", ".join(mal)) if mal else "")
    elif ficha.get("height"):
        add("height", f"{ficha.get('height')} ({src.get('height', '')})", "; ".join(sorted({f'{f["h"]:.3f}' for f in filas})),
            "AMBER", "no printed A.F.F. height in the type (to structure / roof framing): checked against sections, not the type")
    # track / slip track: solo se verifica que el take-off cargó algo donde el schedule lo imprime
    for campo in ("track", "slip_track"):
        if ficha.get(campo):
            add(campo, f"{ficha[campo]} ({src.get('track', '')})", "see Material Summary (track rows)", "AMBER",
                "track is quantified by family, not per type in the Excel")
    for e in ficha.get("extras") or []:
        add("extra", e, "scope", "AMBER", "check the Scope Checklist (insulation / sealant are excluded by estimator order)")
    v = "RED" if any(c["status"] == "RED" for c in checks) else ("AMBER" if any(c["status"] == "AMBER" for c in checks) else "GREEN")
    return {"type": t, "verdict": v, "checks": checks, "img": ficha.get("img")}


_NUM = r"-?\d[\d,]*(?:\.\d+)?"


def _n(x):
    return float(x.replace(",", ""))


def sumas(ms, filas, calc):
    """Cada renglón del Material Summary: (1) origen impreso N/SHEET (si Net > 0 y no hay hoja -> ROJO);
    (2) su Breakdown [DERIVED] suma lo que dice y = Net (si no -> ROJO); (3) los términos que son walls se agrupan por
    type (Partition Takeoff) -> subtotal por type; (4) board X / X W.R.: cada término de wall = Σ caras de ese board en
    ese wall (board_out del canon), y joint compound / tape usan como driver el total de board de la hoja."""
    out = []
    tipo_de = {}
    for f in filas:
        for w in f["wall"].split("+"):
            tipo_de[w] = f["type"]
    try:
        caras = json.load(open(os.path.join(calc, "board_out.json"))).get("caras") or []
    except OSError:
        caras = []
    sf_cara = {}
    for c in caras:
        k = (c.get("wall") or c.get("id"), tipo_board(c.get("board")))
        sf_cara[k] = sf_cara.get(k, 0) + float(c.get("sf") or 0)
    board_total = sum(m["net"] for m in ms if m["unit"] == "SF" and re.match(r'5/8" gypsum board, Type X', m["name"]))
    for m in ms:
        w, net = m["where"], m["net"]
        est, notas, por_tipo, items, bsum = "GREEN", [], {}, [], None
        hoja = re.search(r"N/SHEET:\s*([^|]+)", w)
        hoja = hoja.group(1).strip() if hoja else ""
        excl = re.search(r"EXCLUDED|none:", w)
        if net > 0 and (not hoja or hoja.startswith("default")):
            est = "RED"
            notas.append("no printed origin (N/SHEET: default)")
        bd = re.search(r"Breakdown \[DERIVED\]:\s*(.+?)\s*=\s*(" + _NUM + r")\s*[A-Z]{2,3}\b", w)
        if bd:
            terms = re.findall(r"([^+]+?)\s+(" + _NUM + r")\s*(?=\+|$)", bd.group(1))
            bsum = round(sum(_n(q) for _, q in terms), 2)
            if abs(bsum - _n(bd.group(2))) > 0.02 or abs(bsum - net) > max(0.02, 0.001 * net):
                est = "RED"
                notas.append(f"breakdown sums {bsum} vs printed {bd.group(2)} vs Net {net}")
            for ref, q in terms:
                ref = ref.strip()
                t = tipo_de.get(ref)
                if t:
                    por_tipo[t] = round(por_tipo.get(t, 0) + _n(q), 2)
                    clave = tipo_board(m["name"]) if m["unit"] == "SF" and "gypsum board, Type X" in m["name"] else None
                    if clave and sf_cara:
                        calc_sf = sf_cara.get((ref, clave), 0)
                        if abs(calc_sf - _n(q)) > 0.02:
                            est = "RED"
                            notas.append(f"{ref}: {q} SF vs canon faces {calc_sf:.2f} SF")
                else:
                    items.append(ref)
        elif net > 0:
            drv = re.search(r"x\s*(" + _NUM + r")\s*SF of board", w)
            l5 = re.findall(r"[A-Z0-9][\w-]*:\s*(" + _NUM + r")\s*SF;?", w)
            prod = re.search(r"(" + _NUM + r")\s*LF\s*x\s*(" + _NUM + r")\s*ft\s*=\s*(" + _NUM + r")", w)
            if len(l5) >= 2:
                bsum = round(sum(_n(q) for q in l5), 2)
                if abs(bsum - net) > max(0.02, 0.001 * net):
                    est = "RED"
                notas.append(f"{len(l5)} itemized areas sum {bsum} vs Net {net}")
            elif prod:
                v = round(_n(prod.group(1)) * _n(prod.group(2)), 2)
                if abs(v - net) > 0.02:
                    est = "RED"
                notas.append(f"{prod.group(1)} LF x {prod.group(2)} ft = {v} vs Net {net}")
            elif drv:
                if abs(_n(drv.group(1)) - board_total) > 0.02:
                    est = "RED"
                notas.append(f"driver {drv.group(1)} SF vs board rows {board_total:.2f} SF")
            elif est != "RED":
                est = "AMBER"
                notas.append("no itemized breakdown: total computed in the cell text (" + w.split("|", 1)[-1].strip()[:90] + ")")
        elif excl:
            est = "AMBER"
            notas.append("0 - " + w.split("|", 1)[-1].strip()[:90])
        out.append({"row": m["row"], "material": m["name"], "unit": m["unit"], "net": net, "breakdown_sum": bsum,
                    "by_type": por_tipo, "non_wall_items": items, "origin": hoja, "status": est, "note": "; ".join(notas)})
    return out


def _png_fila(x, ms, png):
    """imagen del renglón del Material Summary en rojo (el Excel no tiene hoja de plano que circular: ese es el hallazgo)."""
    from PIL import Image, ImageDraw
    import textwrap
    m = next(r for r in ms if r["row"] == x["row"])
    lineas = [f"Material Summary row {x['row']}  |  {m['name']}  |  {m['net']} {m['unit']}", ""]
    lineas += textwrap.wrap("Where it comes from: " + m["where"], 110) + ["", "RED: " + x["note"]]
    img = Image.new("RGB", (1400, 40 + 26 * len(lineas)), "white")
    d = ImageDraw.Draw(img)
    for i, t in enumerate(lineas):
        d.text((24, 20 + 26 * i), t, fill=(200, 0, 0) if t.startswith(("RED", "Where")) else (0, 0, 0))
    d.ellipse((8, 8, 1392, 32 + 26 * len(lineas)), outline=(255, 0, 0), width=4)
    img.save(png)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fichas"); ap.add_argument("xlsx"); ap.add_argument("canon"); ap.add_argument("calc"); ap.add_argument("out")
    ap.add_argument("--title", default="Take-off")
    ap.add_argument("--map", action="append", default=[],
                    help="KEY=TYPE1,TYPE2: schedule key carried in the Excel under other type names (e.g. EXT)")
    a = ap.parse_args()
    os.makedirs(os.path.join(a.out, "img"), exist_ok=True)
    fichas = json.load(open(a.fichas))["types"]
    filas, ms = leer_excel(a.xlsx)
    cw = {w["id"]: w for w in json.load(open(a.canon)).get("walls") or []}
    mapa = {k: v.split(",") for k, v in (m.split("=", 1) for m in a.map)}
    misc = json.load(open(a.canon)).get("misc_items") or []
    sel = lambda t: [f for f in filas if f["type"] in mapa.get(t, [t]) or f["wall"] in mapa.get(t, [])]  # noqa: E731
    res = [comparar_type(t, fichas[t], sel(t), cw, misc) for t in fichas]
    cubiertos = {id(f) for t in fichas for f in sel(t)}
    sueltos = [f for f in filas if id(f) not in cubiertos]
    if sueltos:
        res.append({"type": "NOT IN SCHEDULE", "verdict": "AMBER", "img": None, "checks": [
            {"field": f"walls {f['type']} {f['wall']}", "schedule": "no ficha (not a schedule type)", "excel": f["stud"],
             "status": "AMBER", "note": "source " + (f["source"] or "")[:160]} for f in sueltos]})
    for r in res:
        if r["verdict"] == "RED" and r.get("img"):
            src = os.path.join(os.path.dirname(os.path.abspath(a.fichas)), r["img"])
            if os.path.exists(src):
                dst = os.path.join(a.out, "img", f"RED_{r['type']}.png")
                shutil.copy(src, dst)
                r["img_out"] = os.path.relpath(dst, a.out)
    sm = sumas(ms, filas, a.calc)
    import openpyxl
    from openpyxl.styles import PatternFill, Font
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Materials review"
    ws.append([f"{a.title} - materials vs partition type schedule (program: revision_materiales.py)"])
    ws.append(["Independent reading of the schedule (fichas.json) vs the Excel; GREEN = matches, RED = differs, AMBER = the schedule does not say it"])
    ws.append(["Type", "Field", "Schedule (printed)", "Excel / take-off", "Status", "Note", "Image"])
    for c in ws[3]:
        c.font = Font(bold=True)
    fill = {"GREEN": PatternFill("solid", fgColor="C6EFCE"), "RED": PatternFill("solid", fgColor="FFC7CE"),
            "AMBER": PatternFill("solid", fgColor="FFEB9C")}
    for r in res:
        for c in r["checks"]:
            ws.append([r["type"], c["field"], str(c["schedule"]), str(c["excel"]), c["status"], c["note"], r.get("img_out", "")])
            ws.cell(ws.max_row, 5).fill = fill[c["status"]]
    ws2 = wb.create_sheet("Sums")
    ws2.append(["Row", "Material", "Unit", "Net (Material Summary)", "Breakdown sum", "Walls by type", "Non-wall items",
                "Origin (N/SHEET)", "Status", "Note"])
    for c in ws2[1]:
        c.font = Font(bold=True)
    for s in sm:
        ws2.append([s["row"], s["material"], s["unit"], s["net"], s["breakdown_sum"],
                    ", ".join(f"{k} {v}" for k, v in s["by_type"].items()), ", ".join(s["non_wall_items"]), s["origin"],
                    s["status"], s["note"]])
        ws2.cell(ws2.max_row, 9).fill = fill[s["status"]]
    wb.save(os.path.join(a.out, "materials_review.xlsx"))
    cnt = {k: sum(r["verdict"] == k for r in res) for k in ("GREEN", "AMBER", "RED")}
    L = [f"# {a.title} — materials vs partition type schedule", "",
         f"Independent reading of the schedule vs the Excel · by type: GREEN {cnt['GREEN']} / AMBER {cnt['AMBER']} / RED {cnt['RED']}", "",
         "| Type | Verdict | Stud | Board | Height | Notes |", "|---|---|---|---|---|---|"]
    for r in res:
        def st(pfx):
            xs = [c for c in r["checks"] if c["field"].startswith(pfx)]
            return "RED" if any(c["status"] == "RED" for c in xs) else ("AMBER" if any(c["status"] == "AMBER" for c in xs) else ("GREEN" if xs else "-"))
        notas = "; ".join(f"{c['field']}: schedule {c['schedule']} / Excel {c['excel']}" for c in r["checks"] if c["status"] == "RED")
        L.append(f"| {r['type']} | {r['verdict']} | {st('stud')} | {st('board')} | {st('height')} | {notas} |")
    cs = {k: sum(x["status"] == k for x in sm) for k in ("GREEN", "AMBER", "RED")}
    L += ["", f"## Sums - every Material Summary row ({len(sm)}): GREEN {cs['GREEN']} / AMBER {cs['AMBER']} / RED {cs['RED']}", "",
          "Origin = printed N/SHEET; breakdown terms add up to the Net; wall terms grouped by partition type.", "",
          "| Row | Material | Net | Walls by type | Non-wall items | Status | Note |", "|---|---|---|---|---|---|---|"]
    for s in sm:
        L.append(f"| {s['row']} | {s['material'][:70]} | {s['net']} {s['unit']} | "
                 f"{', '.join(f'{k} {v}' for k, v in s['by_type'].items())} | {len(s['non_wall_items'])} | {s['status']} | {s['note'][:120]} |")
    open(os.path.join(a.out, "materials_review.md"), "w").write("\n".join(L) + "\n")
    rojos = [x for x in sm if x["status"] == "RED"]
    if rojos:
        L += ["", "## RED sums (one image each in img/)", ""]
    for x in rojos:
        png = os.path.join(a.out, "img", f"RED_sum_row{x['row']}.png")
        _png_fila(x, ms, png)
        x["img_out"] = os.path.relpath(png, a.out)
        L.append(f"- Material Summary row {x['row']} - {x['material']}: {x['note']} ({x['img_out']})")
    open(os.path.join(a.out, "materials_review.md"), "w").write("\n".join(L) + "\n")
    json.dump({"types": res, "sums": sm}, open(os.path.join(a.out, "materials_review.json"), "w"), indent=1)
    print(f"GREEN {cnt['GREEN']} / AMBER {cnt['AMBER']} / RED {cnt['RED']}")
    for r in res:
        for c in r["checks"]:
            if c["status"] == "RED":
                print(f"RED {r['type']} {c['field']}: schedule {c['schedule']} / Excel {c['excel']}")
    for s in sm:
        if s["status"] == "RED":
            print(f"RED sum {s['material']}: {s['note']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
