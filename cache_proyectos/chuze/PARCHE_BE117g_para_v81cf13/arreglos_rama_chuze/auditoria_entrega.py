#!/usr/bin/env python3
"""auditoria_entrega.py — BE-117 / R80f.10 (usuario 3-nov, INVIOLABLE): auditoría de ENTREGA por programa, ANTES de
entregar. Sin rc 0 no se entrega.

Uso: python3 auditoria_entrega.py <excel.xlsx> <markups.pdf> <takeoff_canon.json> [--md salida.md]
                                  [--imagenes <carpeta>] [--docs README.md PARA_REVISAR.md ...] [--primera-linea "texto"]
Chequea:
  1. cada fila de la Partition Takeoff (partitions, OTHER FRAMING, existentes) tiene su(s) annot(s) con TYPE · LF · H ·
     SF · DETAIL · Wall ID iguales al Excel (LF / SF sumados por los ids de la fila; H en ft-in vs ft decimal);
  2. /Measure de cada annot = escala impresa (rótulo SCALE) de su hoja;
  3. Bluebeam Length (vértices / escala) vs LF <= 0.5 %;
  4. toda hoja con elementos del canon tiene markups; una PNG por hoja marcada (si se pasa --imagenes);
  5. Excel: 6 hojas, types en el orden del schedule con SUBTOTAL, GRAND TOTAL, OTHER FRAMING / existentes con
     SUBTOTAL, PROJECT DATA en Inputs, Pending Items sin RFIs abiertos;
  6. docs: PROJECT DATA arriba (y la primera línea pedida).
"""
import json, math, os, re, sys
from fractions import Fraction

TOL_LEN = 0.005
HOJAS6 = ["Inputs", "Partition Takeoff", "Material Summary", "Pending Items", "Review Items", "Scope Checklist"]
RX_SCALE = re.compile(r"(\d+(?:/\d+)?|\d+\s+\d+/\d+)\s*\"\s*=\s*1\s*'\s*-?\s*0\s*\"")


def ftin_a_ft(s):
    m = re.match(r"(\d+)'-([\d.]+)\"", s.strip())
    return int(m.group(1)) + float(m.group(2)) / 12.0 if m else None


def frac(s):
    s = s.strip()
    if " " in s:
        a, b = s.split()
        return Fraction(a) + Fraction(b)
    return Fraction(s)


def escalas_impresas(page):
    """{Fraction pulgadas por pie} de los rótulos SCALE impresos en la hoja (texto)."""
    t = page.get_text("text").replace("’", "'").replace("”", '"').replace("''", '"')
    return {frac(m.group(1)) for m in RX_SCALE.finditer(t)}


def leer_annots(pdf):
    import pymupdf as fitz
    doc = fitz.open(pdf)
    out = []
    for i in range(doc.page_count):
        pg = doc[i]
        for a in pg.annots() or []:
            nm = (a.info or {}).get("id") or ""
            if not nm.startswith("TO-") or nm.startswith("TO-LEGEND-"):
                continue
            ms = doc.xref_get_key(a.xref, "Measure")[1] or ""
            r = re.search(r"/R\((\d+(?:/\d+)?) in = 1 ft\)", ms)
            vs = [tuple(v) for v in (a.vertices or [])]
            lpt = sum(math.dist(vs[k], vs[k + 1]) for k in range(len(vs) - 1))
            out.append({"page": i, "label": pg.get_label(), "id": nm[3:], "content": a.info.get("content") or "",
                        "subject": a.info.get("subject") or "", "escala": Fraction(r.group(1)) if r else None, "lpt": lpt})
    return doc, out


def parse_content(c):
    p = [x.strip() for x in c.split("·")]
    d = {"type": p[0], "id": p[-1]}
    for x in p:
        if x.endswith(" LF") and "lf" not in d:
            d["lf"] = float(x[:-3].replace(",", ""))
        elif x.startswith("H ") and "h" not in d:
            d["h"] = ftin_a_ft(x[2:])
        elif re.search(r"[\d,.]+ SF( board)?$", x) and "sf" not in d:
            d["sf"] = float(x.split()[0].replace(",", ""))
    d["detail"] = p[-2] if len(p) >= 2 else ""
    return d


def filas_excel(xlsx):
    import openpyxl
    wb = openpyxl.load_workbook(xlsx, data_only=True)
    ws = wb["Partition Takeoff"]
    filas, bloques, cur = [], [], None
    for r in ws.iter_rows(min_row=5, values_only=True):
        a = str(r[0] or "")
        if a.startswith("TYPE "):
            cur = a[5:].strip(); bloques.append({"type": cur, "rows": 0, "subtotal": False}); continue
        b = str(r[1] or "")
        if b.startswith("SUBTOTAL") and bloques:
            bloques[-1]["subtotal"] = True; continue
        if b.startswith("TOTAL"):
            bloques.append({"type": "GRAND TOTAL", "rows": 0, "subtotal": True}); continue
        if r[1] and isinstance(r[2], (int, float)) and cur:
            filas.append({"type": cur, "ids": str(r[1]).split("+"), "lf": float(r[2]), "h": float(r[3] or 0),
                          "sf": float(r[7] or 0), "source": str(r[9] or ""), "label": a})
            bloques[-1]["rows"] += 1
    return wb, filas, bloques


def auditar(xlsx, pdf, canon_p, imagenes=None, docs=(), primera=None):
    can = json.load(open(canon_p, encoding="utf-8"))
    res = []                                                       # (check, item, ok, detalle)
    doc, an = leer_annots(pdf)
    A = {}
    for x in an:
        A.setdefault(x["id"], []).append(x)
    wb, filas, bloques = filas_excel(xlsx)
    # 1. fila del Excel <-> annots
    for f in filas:
        ps = [parse_content(A[i][0]["content"]) for i in f["ids"] if i in A]
        falt = [i for i in f["ids"] if i not in A]
        if falt:
            res.append(("1 annot = Excel row", f["label"][:60], False, f"sin annot: {falt}")); continue
        lf = round(sum(p.get("lf", 0) for p in ps), 2)
        sf = round(sum(p.get("sf", 0) for p in ps), 1)
        h = ps[0].get("h")
        tp = ps[0]["type"]
        t_ok = tp == f["type"] or (f["type"].startswith("OTHER FRAMING") and tp.startswith("OTHER FRAMING")) or \
            ("BOARD ONLY" in f["type"] and "BOARD ONLY" in tp)
        det = ps[0]["detail"]
        d_ok = det in f["source"] or det in f["label"]
        ok = t_ok and abs(lf - f["lf"]) <= 0.011 and abs(sf - f["sf"]) <= 0.15 and h is not None and abs(h - f["h"]) <= 0.06 and d_ok
        res.append(("1 annot = Excel row", "+".join(f["ids"]), ok,
                    f"TYPE {tp} / {f['type']}; LF {lf} / {f['lf']}; H {round(h or 0, 3)} / {f['h']}; SF {sf} / {f['sf']}; DETAIL {det} in source: {d_ok}"))
    ids_x = {i for f in filas for i in f["ids"]}
    for i in A:
        if i not in ids_x:
            res.append(("1 annot = Excel row", i, False, "annot sin fila en la Partition Takeoff"))
    # 2. escala = rótulo impreso;  3. Length vs LF
    impresas = {}
    for x in an:
        if x["page"] not in impresas:
            impresas[x["page"]] = escalas_impresas(doc[x["page"]])
        sc = impresas[x["page"]]
        ok = x["escala"] is not None and (x["escala"] in sc)
        res.append(("2 /Measure = printed SCALE", f"{x['id']} ({x['label']})", ok,
                    f"annot {x['escala']} in = 1 ft; printed on the sheet: {sorted(str(s) for s in sc) or 'none'}"))
        p = parse_content(x["content"])
        if x["escala"] and p.get("lf"):
            L = x["lpt"] / float(x["escala"] * 72)
            dv = abs(L - p["lf"]) / p["lf"]
            res.append(("3 Length vs LF <= 0.5 %", x["id"], dv <= TOL_LEN, f"Length {L:.2f} / LF {p['lf']:.2f} ({dv * 100:.2f} %)"))
    # 4. hojas con elementos tienen markups (+ PNG)
    hojas_can = {str(w.get("sheet")) for w in can.get("walls") or []} | {str(e.get("sheet")) for e in can.get("existing_walls") or []}
    marcadas = {x["label"] for x in an}
    for h in sorted(hojas_can):
        res.append(("4 sheet with elements has markups", h, h in marcadas, "marked" if h in marcadas else "NO markups on this sheet"))
    if imagenes:
        pngs = os.listdir(imagenes) if os.path.isdir(imagenes) else []
        for h in sorted(marcadas):
            ok = any(n.startswith(h + "_") and n.endswith(".png") for n in pngs)
            res.append(("4 PNG per marked sheet", h, ok, "png present" if ok else "no PNG for this sheet"))
    # 5. Excel
    res.append(("5 Excel 6 sheets", "sheetnames", wb.sheetnames == HOJAS6, str(wb.sheetnames)))
    tipos = [b["type"] for b in bloques if b["type"] not in ("GRAND TOTAL",) and not b["type"].startswith(("OTHER", "EXISTING", "BOARD"))]
    k = (can.get("constants") or {}).get("type_order") or {}
    k = k.get("value") if isinstance(k, dict) else k
    if k:
        rank = {t: i for i, t in enumerate(k)}
        res.append(("5 types in schedule order", ", ".join(tipos), [rank.get(t, 999) for t in tipos] == sorted(rank.get(t, 999) for t in tipos), "A301 schedule order"))
    for b in bloques:
        if b["type"] != "GRAND TOTAL":
            res.append(("5 SUBTOTAL per block", b["type"], b["subtotal"], f"{b['rows']} rows"))
    res.append(("5 GRAND TOTAL", "Partition Takeoff", any(b["type"] == "GRAND TOTAL" for b in bloques), ""))
    inp = " ".join(str(r[0]) for r in wb["Inputs"].iter_rows(values_only=True) if r and r[0])
    res.append(("5 PROJECT DATA in Inputs", "Inputs", "PROJECT DATA" in inp, ""))
    pend = [r[0] for r in wb["Pending Items"].iter_rows(min_row=2, values_only=True) if r and r[0]]
    res.append(("5 Pending Items empty (0 RFIs open)", "Pending Items", not pend, str(pend)))
    # 6. docs
    for d in docs:
        t = open(d, encoding="utf-8").read() if os.path.isfile(d) else ""
        res.append(("6 PROJECT DATA on top", os.path.basename(d), "PROJECT DATA" in t[:4000].upper() or "DATOS DEL PROYECTO" in t[:4000].upper(), ""))
        if primera and os.path.basename(d).upper().startswith("README"):
            res.append(("6 first line", os.path.basename(d), t.splitlines()[0].strip() == primera if t else False, t.splitlines()[0][:80] if t else ""))
    return res


def main(a):
    if len(a) < 3:
        print(__doc__); return 2
    md = a[a.index("--md") + 1] if "--md" in a else None
    img = a[a.index("--imagenes") + 1] if "--imagenes" in a else None
    pl = a[a.index("--primera-linea") + 1] if "--primera-linea" in a else None
    docs = []
    if "--docs" in a:
        for x in a[a.index("--docs") + 1:]:
            if x.startswith("--"):
                break
            docs.append(x)
    res = auditar(a[0], a[1], a[2], img, docs, pl)
    malos = [r for r in res if not r[2]]
    if md:
        L = ["# BE-117 delivery audit (auditoria_entrega.py)", "", f"Excel: {os.path.basename(a[0])} · Markups: {os.path.basename(a[1])}", "",
             f"**{len(res)} checks, {len(malos)} failures -> {'OK' if not malos else 'NOT DELIVERABLE'}**", "",
             "## Summary per check", "", "| Check | Items | Failures |", "|---|---|---|"]
        ck = {}
        for c, _, ok, _ in res:
            d = ck.setdefault(c, [0, 0]); d[0] += 1; d[1] += (not ok)
        L += [f"| {c} | {v[0]} | {v[1]} |" for c, v in ck.items()]
        L += ["", "## Failures", ""] + ([f"- {c} · {i} · {d}" for c, i, ok, d in malos] or ["none"])
        L += ["", "## All items", "", "| Check | Item | OK | Detail |", "|---|---|---|---|"]
        L += [f"| {c} | {i} | {'OK' if ok else 'FAIL'} | {d} |" for c, i, ok, d in res]
        open(md, "w").write("\n".join(L) + "\n")
    for c, i, ok, d in malos:
        print("FALLA", c, "|", i, "|", d)
    print(f"AUDITORIA ENTREGA: {len(res)} checks, {len(malos)} fallas -> {'OK' if not malos else 'NO ENTREGABLE'}")
    return 0 if not malos else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
