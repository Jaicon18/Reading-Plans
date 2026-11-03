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
    ms = {}
    for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True):
        if r[0] and isinstance(r[2], (int, float)):
            ms[str(r[0])] = (r[1], float(r[2]))
    return rows, ms


def comparar_type(t, ficha, filas, cw):
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
        mal = [f["wall"] for f in filas if des.upper() not in f["stud"].upper()]
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
    caras = ficha.get("faces") or []
    if caras:
        n_sch = sum(2 if "each" in _txt(c.get("side")) or "both" in _txt(c.get("side")) else 1 for c in caras)
        bt_sch = {tipo_board(c.get("board")) for c in caras}
        lay_sch = max(int(c.get("layers") or 1) for c in caras)
        for f in filas:
            for wid in f["wall"].split("+"):
                w = cw.get(wid) or {}
                fc = [x for x in w.get("faces") or [] if x.get("board") and float(x.get("height_ft") or 0) > 0]
                lados = {x.get("side") for x in fc}
                bts = {tipo_board(x.get("board")) for x in fc}
                lay = max([int(x.get("layers") or 1) for x in fc] or [0])
                if not fc:
                    add(f"board faces {wid}", f"{n_sch} face(s) {sorted(bt_sch)}", "no board face", "RED")
                    continue
                if len(lados) != n_sch:
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
        if not any(c["field"].startswith("board") for c in checks):
            add("board", f"{n_sch} face(s) {sorted(bt_sch)}, {lay_sch} layer(s)", "same on every wall", "GREEN")
    else:
        add("board", "not printed in the type", "", "AMBER", src.get("board", ""))
    # altura que cubre
    h_sch = ft_aff(ficha.get("height"))
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


def sumas(ms, calc):
    """Renglones de board y studs del Material Summary = Σ caras / walls (board_out, studs_out) + ítems con su fuente."""
    out = []
    fam = json.load(open(os.path.join(calc, "familias_out.json")))
    bo = json.load(open(os.path.join(calc, "board_out.json")))
    so = json.load(open(os.path.join(calc, "studs_out.json")))
    filas = fam.get("filas") or []
    def items(f):
        return [r for r in filas if r.get("familia") == f]
    for nombre, f, clave in (("5/8\" gypsum board, Type X", '5/8" gyp board Type X', "X"),
                             ("5/8\" gypsum board, Type X W.R. (water resistant)", '5/8" gyp Type X W.R.', "X-WR")):
        walls = sum(c["sf"] for c in bo.get("caras") or [] if tipo_board(c["board"]) == clave)
        otros = items(f)
        sin_fuente = [r.get("ref") for r in otros if not r.get("source")]
        net = ms.get(nombre, (None, None))[1]
        tot = fam["familias"].get(f)
        ok = net is not None and tot is not None and abs(net - tot) <= TOL * max(tot, 1) and walls <= tot + 0.01
        out.append({"material": nombre, "net": net, "walls_sf": round(walls, 2), "non_wall_items": [r.get("ref") for r in otros],
                    "family_total": tot, "status": "RED" if (not ok or sin_fuente) else "GREEN",
                    "note": ("items without source: " + ", ".join(sin_fuente)) if sin_fuente else
                    f"walls {walls:,.2f} SF + {len(otros)} non-wall item(s) with source = {tot}"})
    porsize = {}
    for w in so.get("walls") or []:
        porsize[w["stud_size"]] = porsize.get(w["stud_size"], 0) + w["lf"]
    for k, v in sorted(porsize.items()):
        out.append({"material": f"studs {k} (walls)", "net": round(v, 2), "walls_sf": None, "non_wall_items": [],
                    "family_total": None, "status": "GREEN", "note": "sum of studs_out walls by stud size"})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fichas"); ap.add_argument("xlsx"); ap.add_argument("canon"); ap.add_argument("calc"); ap.add_argument("out")
    ap.add_argument("--title", default="Take-off")
    a = ap.parse_args()
    os.makedirs(os.path.join(a.out, "img"), exist_ok=True)
    fichas = json.load(open(a.fichas))["types"]
    filas, ms = leer_excel(a.xlsx)
    cw = {w["id"]: w for w in json.load(open(a.canon)).get("walls") or []}
    res = [comparar_type(t, fichas[t], [f for f in filas if f["type"] == t], cw) for t in fichas]
    for r in res:
        if r["verdict"] == "RED" and r.get("img"):
            src = os.path.join(os.path.dirname(os.path.abspath(a.fichas)), r["img"])
            if os.path.exists(src):
                dst = os.path.join(a.out, "img", f"RED_{r['type']}.png")
                shutil.copy(src, dst)
                r["img_out"] = os.path.relpath(dst, a.out)
    sm = sumas(ms, a.calc)
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
    ws2.append(["Material", "Net (Material Summary)", "Walls", "Non-wall items", "Family total", "Status", "Note"])
    for s in sm:
        ws2.append([s["material"], s["net"], s["walls_sf"], ", ".join(s["non_wall_items"]), s["family_total"], s["status"], s["note"]])
        ws2.cell(ws2.max_row, 6).fill = fill[s["status"]]
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
    L += ["", "## Sums (Material Summary = walls by type + non-wall items with source)", "",
          "| Material | Net | Walls | Non-wall items | Status |", "|---|---|---|---|---|"]
    for s in sm:
        L.append(f"| {s['material']} | {s['net']} | {s['walls_sf']} | {len(s['non_wall_items'])} | {s['status']} |")
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
