#!/usr/bin/env python3
"""comparar_alturas.py — U-175 (usuario 11-nov: "quiero algo parecido o igual a como haces la comparacion de cvs contra
excel y pdf", para verificar que las alturas estan bien calculadas, TODOS los proyectos).

Comparación a TRES lados de la ALTURA de cada markup, igual que comparar_csv_bluebeam.py hace con los largos:
  1) Bluebeam   : columna Depth del CSV que exporta el usuario (Markups List > Summary > CSV), o Auditoria/VISTA_BLUEBEAM.csv
  2) Excel      : Partition Takeoff > Height (FT) del Wall # (y renglones de ceilings / demo si traen Wall ID)
  3) PLANO      : Auditoria/ALTURAS_IMPRESAS.csv, armado por una lectura INDEPENDIENTE que no ve el Excel (U-099/BE-119):
                  columnas  Wall ID, Printed H (ft o 12'-6"), Source (N/HOJA), Operation, Status, Image
                  Status = CONFIRMED (cota impresa) o DERIVED (con su operación, ej. "C.H. 12'-0 (A3.0) + 6\" (2/A2.0)").
Resultado por markup: OK si los tres coinciden (tolerancia 0.02 ft = 1/4"); si no, MISMATCH con qué lado difiere.
Además: altura del plano sin Source o sin Image = SIN FUENTE (falla), DERIVED sin Operation = falla.
Sale con código 1 si hay cualquier falla. Escribe COMPARACION_ALTURAS.csv con una fila por markup y un resumen por altura.

Uso:  python3 -I comparar_alturas.py <bluebeam.csv | VISTA_BLUEBEAM.csv> <Takeoff.xlsx> <ALTURAS_IMPRESAS.csv> [salida.csv]
"""
import csv
import io
import re
import sys

TOL = 0.02
RX_ID = re.compile(r"#?\b([A-Z]{1,6}\d*[A-Z]?-\d{1,3}[A-Z]?)\b")
NO_ALTURA = {"EXCLUDED", "LEGEND"}


def num(s):
    s = str(s if s is not None else "").strip().replace(" ft", "")
    if not s:
        return None
    m = re.fullmatch(r"(-?\d+)'\s*-?\s*(\d+(?:\.\d+)?)?(?:\s+(\d+)/(\d+))?\"?", s)
    if m:
        pul = float(m.group(2) or 0) + (float(m.group(3)) / float(m.group(4)) if m.group(3) else 0)
        return float(m.group(1)) + pul / 12.0
    try:
        return float(s.replace(",", ""))
    except ValueError:
        return None


def leer(path):
    t = open(path, "rb").read()
    for enc in ("utf-8-sig", "utf-16", "cp1252", "latin-1"):
        try:
            s = t.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    return [{str(k or "").strip(): (v or "").strip() if isinstance(v, str) else v for k, v in r.items()}
            for r in csv.DictReader(io.StringIO(s))]


def col(r, *nombres):
    for n in nombres:
        if n in r and str(r[n]).strip():
            return r[n]
    return ""


def wall_id(r):
    v = col(r, "Wall ID", "Wall #")
    if v:
        v = re.sub(r"^(DEMO-)+", "DEMO-", v)
        return v
    for campo in ("Comments", "Label", "Contents", "ID"):
        m = RX_ID.search(str(r.get(campo) or ""))
        if m:
            return m.group(1)
    return ""


def buscar(tabla, wid):
    """Empareja el Wall ID del markup con la tabla aunque traiga prefijo / sufijo de la tool (TO-, DEMO-DEMO-, ~3, -BOARD)."""
    if wid in tabla:
        return tabla[wid], wid
    base = re.sub(r"^(TO-)+", "", wid)
    base = re.sub(r"(~\d+|-BOARD|-FACE-?[A-Z0-9]*)$", "", base)
    for cand in (base, base.replace("DEMO-", "", 1)):
        if cand in tabla:
            return tabla[cand], cand
    for k in sorted(tabla, key=len, reverse=True):
        if k and re.search(r"(^|[^A-Z0-9])" + re.escape(k) + r"($|[^A-Z0-9])", wid):
            return tabla[k], k
    return None, base


def leer_excel(path):
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb["Partition Takeoff"]
    h = {}
    cab = None
    for fila in ws.iter_rows(values_only=True):
        celdas = [str(c).strip() if c is not None else "" for c in fila]
        if "Wall #" in celdas and any(c.startswith("Height") for c in celdas):
            cab = (celdas.index("Wall #"), next(i for i, c in enumerate(celdas) if c.startswith("Height")))
            continue
        if cab and celdas[cab[0]]:
            v = num(fila[cab[1]])
            if v is not None:
                h[celdas[cab[0]]] = v
    return h


def main(a):
    if len(a) < 3:
        print(__doc__)
        return 2
    bb = leer(a[0])
    xl = leer_excel(a[1])
    pl = {}
    fallas_plano = []
    for r in leer(a[2]):
        wid = wall_id(r)
        h = num(col(r, "Printed H", "Printed H (ft)"))
        src, img = col(r, "Source", "Source (N/SHEET)"), col(r, "Image")
        st, op = col(r, "Status").upper(), col(r, "Operation")
        pl[wid] = dict(h=h, src=src, img=img, st=st, op=op)
        if h is None or not src or not img:
            fallas_plano.append(f"{wid}: printed height without value / Source / Image")
        if st == "DERIVED" and not op:
            fallas_plano.append(f"{wid}: DERIVED without Operation")
        if st not in ("CONFIRMED", "DERIVED"):
            fallas_plano.append(f"{wid}: Status must be CONFIRMED or DERIVED (got '{st}')")
    salida, fallas = [], list(fallas_plano)
    for r in bb:
        subj = col(r, "Subject").upper()
        d = num(col(r, "Depth", "Depth (ft)"))
        if subj in NO_ALTURA or d is None:
            continue
        wid = wall_id(r)
        lbl = col(r, "Page Label")
        x, _ = buscar(xl, wid)
        p, wid_n = buscar(pl, wid)
        wid = wid_n if p else wid
        veredicto, nota = "OK", []
        if not wid:
            veredicto, nota = "NO WALL ID", ["markup without Wall ID in Comments/Label"]
        elif p is None or p["h"] is None:
            veredicto, nota = "NO PRINTED SOURCE", ["wall missing in ALTURAS_IMPRESAS.csv"]
        else:
            if abs(d - p["h"]) > TOL:
                nota.append(f"Bluebeam {d:.3f} vs printed {p['h']:.3f}")
            if x is not None and abs(x - p["h"]) > TOL:
                nota.append(f"Excel {x:.3f} vs printed {p['h']:.3f}")
            if nota:
                veredicto = "MISMATCH"
            if x is None:
                nota.append("Excel: no Partition Takeoff row (ceiling / soffit / demo) - checked Bluebeam vs printed only")
        if veredicto != "OK":
            fallas.append(f"{lbl} {wid}: {veredicto} " + "; ".join(nota))
        salida.append({"Page Label": lbl, "Subject": col(r, "Subject"), "Wall ID": wid,
                       "Bluebeam Depth (ft)": d, "Excel H (ft)": x,
                       "Printed H (ft)": p["h"] if p else None, "Printed source (N/SHEET)": p["src"] if p else "",
                       "Status": p["st"] if p else "", "Operation": p["op"] if p else "",
                       "Image": p["img"] if p else "", "Result": veredicto, "Notes": "; ".join(nota)})
    out = a[3] if len(a) > 3 else "COMPARACION_ALTURAS.csv"
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(salida[0].keys()) if salida else ["Result"])
        w.writeheader()
        w.writerows(salida)
    ok = sum(1 for s in salida if s["Result"] == "OK")
    print(f"ALTURAS: {ok}/{len(salida)} markups OK (Bluebeam = Excel = plano impreso)")
    resumen = {}
    for s in salida:
        k = (round(s["Printed H (ft)"] or -1, 3), s["Printed source (N/SHEET)"])
        resumen.setdefault(k, []).append(s["Wall ID"])
    for (h, src), ws in sorted(resumen.items()):
        print(f"  H {h:>7} ft  {src:<30} {len(ws)} markups")
    if len(salida) == 0:
        fallas.append("0 markups with Depth compared (U-137: an empty check is a FAIL)")
    for f in fallas:
        print("FAIL", f)
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
