#!/usr/bin/env python3
"""comparar_csv_bluebeam.py — U-167 / BE-156 (CR City Hotel rev18, 11-nov): compara el CSV que exporta Bluebeam (Markups List)
con el PDF de markups y lista lo que falta en cada lado.

Origen: el CSV del usuario traía 1,277 de 1,282 markups; faltaban los 5 cielos de L4 (401-405, 1,910 SF) porque su /NM llevaba
"/" ("bedroom/closet"). Desde U-157 / U-167 esta comparación se hace por programa cada vez que el usuario exporta el CSV.

Emparejamiento: Page Label + Subject + Length / Area / Wall Area (cada número presente en los dos lados, tolerancia 0.02;
uno presente y el otro vacío = no empareja). Primero por ID (= /NM) cuando coincide; después el resto por medidas.

Uso:  python3 -I comparar_csv_bluebeam.py <export_bluebeam.csv> <markups.pdf> [salida.csv]
Sale con código 1 si falta algo en cualquiera de los dos lados.
Medición del PDF = la de Bluebeam: Length = /Vertices (en pt) x /Measure /X /C (polígono: perímetro cerrado),
Area = shoelace x C² x /A /C, Wall Area = Length x /Depth / DepthUnit /C."""
import csv
import io
import math
import re
import sys

TOL = 0.02
NO_MARKUP = ("/Popup", "/Link", "/Widget")


def num(s):
    """'1,091.02' -> 1091.02; "12'-6\"" -> 12.5; '' -> None."""
    s = str(s or "").strip()
    if not s:
        return None
    m = re.fullmatch(r"(-?\d+)'\s*-?\s*(\d+(?:\.\d+)?)?(?:\s+(\d+)/(\d+))?\"?", s)
    if m:
        pie = float(m.group(1))
        pul = float(m.group(2) or 0) + (float(m.group(3)) / float(m.group(4)) if m.group(3) else 0)
        return pie + pul / 12.0
    try:
        return float(s.replace(",", ""))
    except ValueError:
        return None


def leer_csv(path):
    t = open(path, "rb").read()
    for enc in ("utf-8-sig", "utf-16", "cp1252", "latin-1"):
        try:
            s = t.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    filas = []
    for r in csv.DictReader(io.StringIO(s)):
        r = {str(k or "").strip(): v for k, v in r.items()}
        filas.append({"id": str(r.get("ID") or "").strip(), "label": str(r.get("Page Label") or "").strip(),
                      "subject": str(r.get("Subject") or "").strip(), "length": num(r.get("Length")),
                      "area": num(r.get("Area")), "wall_area": num(r.get("Wall Area")), "depth": num(r.get("Depth"))})
    return filas


def _c(arr, defecto=None):
    try:
        return float(arr[0].get("/C"))
    except Exception:                                                   # noqa: BLE001
        return defecto


def leer_pdf(path):
    """-> [dict id, label, subject, length, area, wall_area, depth] de cada markup del PDF (sin Popup / Link / Widget)."""
    import pikepdf
    import pypdf
    try:
        r_ = pypdf.PdfReader(path)
        labels = list(r_.page_labels)
    except Exception:                                                   # noqa: BLE001
        labels = []
    out = []
    with pikepdf.open(path) as d:
        for i, page in enumerate(d.pages):
            for a in page.obj.get("/Annots") or []:
                try:
                    st = str(a.get("/Subtype") or "")
                    if st in NO_MARKUP:
                        continue
                    m = a.get("/Measure")
                    o = {"id": str(a.get("/NM") or ""), "label": labels[i] if i < len(labels) else str(i + 1),
                         "subject": str(a.get("/Subj") or "").strip(), "length": None, "area": None, "wall_area": None,
                         "depth": None, "pagina": i + 1}
                    if m is not None:
                        xc = _c(m.get("/X"), 0.0)
                        ac = _c(m.get("/A"), 1.0)
                        v = [float(x) for x in (a.get("/Vertices") or [])]
                        pts = list(zip(v[0::2], v[1::2]))
                        lpt = sum(math.dist(pts[k], pts[k + 1]) for k in range(len(pts) - 1))
                        if st == "/Polygon" and len(pts) >= 3:
                            lpt += math.dist(pts[-1], pts[0])
                            q = pts + [pts[0]]
                            o["area"] = abs(sum(q[k][0] * q[k + 1][1] - q[k + 1][0] * q[k][1] for k in range(len(q) - 1))) / 2 * xc * xc * ac
                        o["length"] = lpt * xc
                        if a.get("/Depth") is not None:
                            o["depth"] = float(a.get("/Depth"))
                            du = _c(a.get("/DepthUnit"), 1.0) or 1.0
                            o["wall_area"] = o["length"] * o["depth"] / du
                    out.append(o)
                except Exception:                                       # noqa: BLE001
                    continue
    return out


def _iguales(x, y, tol=TOL):
    if x["label"] != y["label"] or x["subject"] != y["subject"]:
        return False
    for k in ("length", "area", "wall_area"):
        a, b = x.get(k), y.get(k)
        if (a is None) != (b is None):
            return False
        if a is not None and abs(round(a, 2) - round(b, 2)) > tol + 1e-9:
            return False
    return True


def comparar(filas_csv, filas_pdf, tol=TOL):
    """-> (pares, solo_pdf, solo_csv). Primero por ID (= /NM) con medidas iguales; después por hoja + subject + medidas."""
    libres = list(range(len(filas_pdf)))
    por_id = {}
    for j in libres:
        por_id.setdefault(filas_pdf[j]["id"], []).append(j)
    pares, resto = [], []
    usados = set()
    for c in filas_csv:
        j = next((j for j in por_id.get(c["id"], []) if j not in usados and _iguales(c, filas_pdf[j], tol)), None)
        if j is None:
            resto.append(c)
        else:
            usados.add(j)
            pares.append((c, filas_pdf[j]))
    solo_csv = []
    for c in resto:
        j = next((j for j in libres if j not in usados and _iguales(c, filas_pdf[j], tol)), None)
        if j is None:
            solo_csv.append(c)
        else:
            usados.add(j)
            pares.append((c, filas_pdf[j]))
    solo_pdf = [filas_pdf[j] for j in libres if j not in usados]
    return pares, solo_pdf, solo_csv


def _f(x):
    return "" if x is None else f"{x:,.2f}"


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    fc, fp = leer_csv(argv[1]), leer_pdf(argv[2])
    pares, solo_pdf, solo_csv = comparar(fc, fp)
    print(f"CSV de Bluebeam: {len(fc)} markups · PDF: {len(fp)} markups · emparejados: {len(pares)}")
    print(f"En el PDF y NO en el CSV ({len(solo_pdf)}):")
    for x in solo_pdf:
        nm = x["id"]
        motivo = " <- /NM con '/' o '\\'" if ("/" in nm or "\\" in nm) else ""
        print(f"  p{x['pagina']} {x['label']} | {x['subject']} | L {_f(x['length'])} | A {_f(x['area'])} | WA {_f(x['wall_area'])} | NM {nm}{motivo}")
    print(f"En el CSV y NO en el PDF ({len(solo_csv)}):")
    for x in solo_csv:
        print(f"  {x['label']} | {x['subject']} | L {_f(x['length'])} | A {_f(x['area'])} | WA {_f(x['wall_area'])} | ID {x['id']}")
    for k in ("area", "wall_area", "length"):
        t = sum(x[k] or 0 for x in solo_pdf)
        if t:
            print(f"  total {k} que falta en el CSV: {t:,.2f}")
    if len(argv) > 3:
        with open(argv[3], "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(["side", "page_label", "subject", "length", "area", "wall_area", "id"])
            for x in solo_pdf:
                w.writerow(["PDF only", x["label"], x["subject"], _f(x["length"]), _f(x["area"]), _f(x["wall_area"]), x["id"]])
            for x in solo_csv:
                w.writerow(["CSV only", x["label"], x["subject"], _f(x["length"]), _f(x["area"]), _f(x["wall_area"]), x["id"]])
        print(f"salida: {argv[3]}")
    return 1 if (solo_pdf or solo_csv) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
