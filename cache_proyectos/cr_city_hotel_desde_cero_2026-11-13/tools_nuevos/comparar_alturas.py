#!/usr/bin/env python3
"""comparar_alturas.py — U-175 (usuario 11-nov: "quiero algo parecido o igual a como haces la comparacion de cvs contra
excel y pdf", para verificar que las alturas estan bien calculadas, TODOS los proyectos).

Comparación a TRES lados de la ALTURA de cada markup, igual que comparar_csv_bluebeam.py hace con los largos:
  1) Bluebeam   : columna Depth del CSV que exporta el usuario (Markups List > Summary > CSV), o Auditoria/VISTA_BLUEBEAM.csv
  2) Excel      : Partition Takeoff > Height (FT) del Wall # (y renglones de ceilings / demo si traen Wall ID)
  3) PLANO      : Auditoria/ALTURAS_IMPRESAS.csv, armado por una lectura INDEPENDIENTE que no ve el Excel (U-099/BE-119):
                  columnas  Wall ID, Printed H (ft o 12'-6"), Source (N/HOJA), Operation, Status, Image
                  Status = CONFIRMED (cota impresa) o DERIVED (con su operación, ej. "C.H. 12'-0 (A3.0) + 6\" (2/A2.0)").
Resultado por markup: OK si los tres coinciden (tolerancia ± 0.02 ft, un cuarto de pulgada); si no, MISMATCH con qué lado difiere.
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


def id_nm(v):
    """BE-COORD01: /NM que escriben las tools ('TO-XW.6.3-L1-02 A', 'TO-L4 401 ... (bedroom%2Fcloset)', 'TO-CF-01~3', 'TO-SOF-01-BOARD')
    -> Wall ID completo (sin TO-, %2F decodificado, sin ~n / -BOARD)."""
    import urllib.parse
    v = urllib.parse.unquote(str(v or "")).strip()
    v = re.sub(r"^(TO-)+", "", v)
    v = re.sub(r"^(DEMO-)+", "DEMO-", v)
    return re.sub(r"(?i)(~\d+|-BOARD|\s+board)$", "", v).strip()


def wall_id(r):
    v = col(r, "Wall ID", "Wall #")
    if v:
        v = re.sub(r"^(DEMO-)+", "DEMO-", v)
        return v
    v = col(r, "ID")                                  # BE-COORD01: CSV del usuario con solo la columna ID (= /NM de la tool)
    if re.match(r"(?i)(TO-|DEMO-)", str(v)):
        return id_nm(v)
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
    sin_cara = re.sub(r"\s+[A-Z]{1,2}$", "", base)      # BE-COORD01: 'XW.6.3-L1-02 A' = cara A del wall XW.6.3-L1-02
    for cand in (base, base.replace("DEMO-", "", 1), sin_cara):
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


# ===================================================================================================================
# U-176 REGLA DE ORO #2 — antes tools/alturas_extremo.py (unido aquí en v81cf87, BE-XF08: el skill queda en 199 archivos).
# Uso: python3 -I comparar_alturas.py extremo <carpeta_entrega_rev> <takeoff_canon.json> <markups.pdf> [--semilla N]
# (antes alturas_extremo.py) — U-176 REGLA DE ORO #2 (usuario 11-nov: "quisiera algo mas extremos, me preocupan mucha las alturas, que esten
# correctas"). Los 6 controles por programa de TODA altura, además de U-175 (comparar_alturas.py, 3 lados):
# 
#  (1) DOBLE LECTURA CIEGA: Auditoria/ALTURAS_IMPRESAS_A.csv y _B.csv (dos lectores que no ven el Excel ni entre sí). Toda diferencia
#      A != B lleva en Auditoria/ALTURAS_AB_RESOLUCION.csv (Wall ID, Resolution, Image) su recorte dirigido; sin resolver = FAIL.
#      La tabla final Auditoria/ALTURAS_IMPRESAS.csv = la que coincide con la cota impresa.
#  (2) CIERRE DIMENSIONAL: cada altura DERIVED se reconstruye con su Operation (cadenas "expr = valor" en ft-in) y debe cerrar
#      (dentro de ± 1/4") y terminar en la Printed H. Cadena que no cierra = FAIL.
#  (3) REGLAS FÍSICAS por wall (canon): H <= B.O. de estructura (constants.deck_heights; deck en pendiente: el canon trae la mayor);
#      "to deck / structure" = B.O. y top track de deflexión (slip); "N in above ceiling" = MAYOR C.H. de los cuartos de ambos lados + N;
#      H >= C.H. de cada cuarto que toca; board de cada cara <= H del wall. Demolición: H <= B.O. (U-075 / U-174).
#  (4) CRUCE POR CUARTO: Auditoria/ALTURAS_CUARTOS.csv (C.H. impresa del RCP, de las dos lecturas): cada cuarto contra todas las walls
#      que lo tocan; mismo type en el mismo cuarto con alturas distintas sin 'height_diff_reason' en el canon = FAIL.
#  (5) EVIDENCIA: Planos marcados/ALTURAS_REVISADAS.pdf (una página por altura distinta con el recorte circulado, la operación y los
#      walls + una página de sección con líneas en cada altura cargada: piso, cielos, tops, B.O.) y capa (OCG) 'HEIGHTS (U-176)' con
#      colores por altura y leyenda en el PDF de markups (contenido de página, NO anotaciones: no entra en la Markups List).
#  (6) MUESTREO: Auditoria/ALTURAS_MUESTRA.json = walls al azar (mínimo 5 o todas; al menos una por altura distinta) con su página de
#      ALTURAS_REVISADAS; checklist_revision.py --b2-muestra lo pone en el CHECKLIST B2.
# 
# Uso:  python3 -I comparar_alturas.py extremo <carpeta_entrega_rev> <takeoff_canon.json> <markups.pdf de Planos marcados> [--semilla N]
#       -> Auditoria/ALTURAS_CONTROLES.json (conteos por control) y los archivos de (5) y (6). Código 1 si algún control falla.
import csv
import io
import json
import os
import random
import re
import sys

TOL_EXT = 1 / 48 + 1e-6          # ± 1/4"
CAPA = "HEIGHTS (U-176)"


# ---------- lectura ----------
def leer_csv(path):
    t = open(path, "rb").read()
    for enc in ("utf-8-sig", "utf-16", "cp1252", "latin-1"):
        try:
            s = t.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    return [{str(k or "").strip(): (v or "").strip() if isinstance(v, str) else v for k, v in r.items()} for r in csv.DictReader(io.StringIO(s))]


def ftin(s):
    """12'-6" / 12'-6 1/2" / 12' / 6" / 12.5 -> pies (float) o None."""
    s = str(s or "").strip().replace("''", '"')
    m = re.fullmatch(r"(-?\d+)'\s*-?\s*(\d+(?:\.\d+)?)?(?:\s+(\d+)/(\d+))?\s*\"?", s)
    if m:
        return int(m.group(1)) + (float(m.group(2) or 0) + (int(m.group(3)) / int(m.group(4)) if m.group(3) else 0)) / 12
    m = re.fullmatch(r"(\d+(?:\.\d+)?)(?:\s+(\d+)/(\d+))?\s*\"", s)
    if m:
        return (float(m.group(1)) + (int(m.group(2)) / int(m.group(3)) if m.group(2) else 0)) / 12
    try:
        return float(s.replace(",", ""))
    except ValueError:
        return None


def sala(nombre):
    """Llave de cuarto: número impreso (101, 112A) o el nombre en minúsculas. BE-CR47 (CR rev20d): el baño de una unidad es su propio
    espacio: '201 Guest Room Type 1 - Bath' / 'bath 201' / 'shower 201' / 'toilet 201' -> '201-bath'; '201 ... - Room' / '201' -> '201'
    (con 'X of / near … Y' mandan las palabras de X: 'corridor south of toilet 911' -> '911')."""
    m = re.search(r"\b(\d{3}[A-Z]?)\b", str(nombre or "").upper())
    if not m:
        return re.sub(r"\s+", " ", str(nombre or "").strip().lower())
    pre = RX_PREP.split(" " + str(nombre or "") + " ", 1)[0]
    return m.group(1) + ("-bath" if _pal(pre) & PAL_HUMEDO else "")


def llaves_ab(la, lb):
    """BE-CR47: las dos lecturas ciegas pueden nombrar distinto el mismo cuarto ('Restroom 913' -> '913-bath', '913' -> '913'); si una
    lectura no tiene la llave '-bath' y sí la del número (y la otra al revés), se comparan como el mismo cuarto ('913')."""
    ka, kb = {k for k, _v in la}, {k for k, _v in lb}
    def norm(lst, mias, otras):
        out = []
        for k, v in lst:
            m = re.fullmatch(r"(\d{3}[A-Z]?)-bath", str(k))
            if m and k not in otras and m.group(1) in otras and m.group(1) not in mias:
                k = m.group(1)
            out.append((k, v))
        return out
    return norm(la, ka, kb), norm(lb, kb, ka)


RX_LLAVE_CUARTO = re.compile(r"\d{3}[A-Z]?(?:-bath)?")


def alias_cuartos(d):
    """BE-CR47: si el CSV no separa el baño ('913' solo, o solo 'Toilet 913'), la llave que falta toma la C.H. de la otra."""
    for k in list(d):
        m = re.fullmatch(r"(\d{3}[A-Z]?)(-bath)?", str(k))
        if m:
            otra = m.group(1) if m.group(2) else m.group(1) + "-bath"
            d.setdefault(otra, d[k])
    return d


RX_NO_CUARTO = re.compile(r"(?i)\bheader\b|\bsoffit\b|\bbulkhead\b|\bSOF-\d")


def leer_cuartos(path):
    """ALTURAS_CUARTOS.csv -> [(llave, C.H.)]; un header / soffit / bulkhead no es el cielo de un cuarto (va como elemento aparte)."""
    return [(sala(r.get("Room")), ftin(r.get("C.H. (ft)"))) for r in leer_csv(path) if not RX_NO_CUARTO.search(str(r.get("Room") or ""))]


def base_id(w):
    w = re.sub(r"^(TO-|DEMO-(?=DEMO-))+", "", str(w or ""))
    return re.sub(r"(~\d+|-BOARD)$", "", w)


# ---------- (1) A / B ----------
def comparar_ab(a, b, resol=None):
    """a, b: [{Wall ID, Printed H}]; resol: {Wall ID: {Resolution, Image}}. -> (filas, fallas)"""
    ha = {r["Wall ID"]: ftin(r.get("Printed H")) for r in a}
    hb = {r["Wall ID"]: ftin(r.get("Printed H")) for r in b}
    resol = resol or {}
    filas, fallas = [], []
    for w in sorted(set(ha) | set(hb)):
        x, y = ha.get(w), hb.get(w)
        if x is not None and y is not None and abs(x - y) <= TOL_EXT:
            filas.append({"Wall ID": w, "H-A": x, "H-B": y, "Result": "MATCH", "Resolution": "", "Image": ""})
            continue
        r = resol.get(w) or {}
        if r.get("Resolution") and r.get("Image"):
            filas.append({"Wall ID": w, "H-A": x, "H-B": y, "Result": "RESOLVED", "Resolution": r["Resolution"], "Image": r["Image"]})
        else:
            filas.append({"Wall ID": w, "H-A": x, "H-B": y, "Result": "UNRESOLVED", "Resolution": "", "Image": ""})
            fallas.append(f"{w}: H-A {x} vs H-B {y} sin resolución con recorte (U-176 control 1)")
    return filas, fallas


RX_NOT_BLIND = re.compile(r"(?i)\bnot\s+blind\b|\bno\s+ciega\b|take-?off\s+detail\s+reading")
RX_ANCHO_DES = re.compile(r"(?i)^(SOF|BW)-|\bsoffit\b|\bbulkhead\b|beam\s*wrap")


def cobertura_ab(a, b, final, depth_ids=()):
    """BE-CR35 (CR rev19, 12-nov: 14 renglones SOF / BW entraron a ALTURAS_IMPRESAS como '[take-off detail reading, not blind]' sin H-A /
    H-B): TODO renglón de la tabla final y TODO markup con Depth (walls, SOF, BW, furring, column wraps) está en ALTURAS_IMPRESAS_A.csv
    Y en _B.csv; un renglón 'not blind' = FAIL. -> [fallas]"""
    def esta(t, w):                                     # estricto: id exacto, sin TO- / ~n / -BOARD o sin la letra de cara (no subcadena)
        b0 = re.sub(r"(~\d+|-BOARD|-FACE-?[A-Z0-9]*)$", "", re.sub(r"^(TO-)+", "", str(w)))
        return any(c in t for c in (w, b0, b0.replace("DEMO-", "", 1), re.sub(r"\s+[A-Z]{1,2}$", "", b0)))
    ta = {r.get("Wall ID"): r for r in a if r.get("Wall ID")}
    tb = {r.get("Wall ID"): r for r in b if r.get("Wall ID")}
    tf = {r.get("Wall ID"): r for r in final if r.get("Wall ID")}
    ev = []
    for r in final:
        if any(RX_NOT_BLIND.search(str(v or "")) for v in r.values()):
            ev.append(f"{r.get('Wall ID')}: renglón 'not blind' en ALTURAS_IMPRESAS (BE-CR35: todo Depth pasa por la doble lectura ciega H-A / H-B)")
    ids = list(dict.fromkeys(list(tf) + [w for w in depth_ids if w and not esta(tf, w)]))
    for w in ids:
        for lado, t in (("A", ta), ("B", tb)):
            if not esta(t, w):
                ev.append(f"{w}: falta en ALTURAS_IMPRESAS_{lado}.csv (BE-CR35 / U-176 (1): todo markup con Depth en las dos lecturas ciegas)")
    return ev


LADOS = ("left", "right", "both", "single")
RX_LADO = re.compile(r"(?i)\b(left|right|both|single|izq(?:uierd[oa])?|der(?:ech[oa])?)\b")
_LADO_ES = {"izq": "left", "izquierdo": "left", "izquierda": "left", "der": "right", "derecho": "right", "derecha": "right"}


def _lado(t):
    m = RX_LADO.search(str(t or ""))
    if not m:
        return None
    v = m.group(1).lower()
    return _LADO_ES.get(v, v)


def lados_fallas(final):
    """BE-CR37 (CR rev19 7/A7.23, usuario 12-nov: Depth 0.917 = fondo 4 1/2" del lado DERECHO + caída 6 1/2" del IZQUIERDO): todo ancho
    desarrollado de SOF / BW lleva 'side' (left / right / both / single) y 'faces' ('cara cota lado; …', una entrada por cara de la suma,
    con su lado o su x del recorte); caras de lados distintos en una misma suma = FAIL; sin side / faces = FAIL. -> [fallas]"""
    ev = []
    for r in final:
        w = str(r.get("Wall ID") or "")
        if not RX_ANCHO_DES.search(w):
            continue
        side = _lado(r.get("side") or r.get("Side"))
        faces = [x.strip() for x in re.split(r"[;|]", str(r.get("faces") or r.get("Faces") or "")) if x.strip()]
        if not side:
            ev.append(f"{w}: ancho desarrollado sin 'side' (left / right / both / single): un ancho POR LADO del corridor (BE-CR37)")
        if not faces:
            ev.append(f"{w}: ancho desarrollado sin 'faces' (cada cara con su cota impresa y su lado, BE-CR37)")
            continue
        lados = [_lado(f) for f in faces]
        sin = [f for f, l in zip(faces, lados) if not l and not re.search(r"(?i)\bx\s*=\s*\d", f)]
        if sin:
            ev.append(f"{w}: cara(s) sin lado ni posición: {'; '.join(sin[:3])} (BE-CR37)")
        distintos = {l for l in lados if l in ("left", "right")}
        if len(distintos) > 1:
            ev.append(f"{w}: la suma mezcla cotas de lados distintos ({'; '.join(faces[:4])}): un ancho desarrollado POR LADO (BE-CR37)")
        elif side in ("left", "right") and distintos and distintos != {side}:
            ev.append(f"{w}: side '{side}' y las caras son del lado {sorted(distintos)[0]} (BE-CR37)")
    return ev


def depth_ids_vista(path):
    """Wall IDs de los markups con Depth > 0 en Auditoria/VISTA_BLUEBEAM.csv (sin la leyenda)."""
    out = []
    for r in leer_csv(path) if path and os.path.isfile(path) else []:
        d = ftin(r.get("Depth (ft)"))
        if d and d > 0 and str(r.get("Subject") or "").upper() != "LEGEND" and r.get("Wall ID"):
            out.append(re.sub(r"^(DEMO-)+", "DEMO-", str(r["Wall ID"])))
    return out


# ---------- (2) cierre dimensional ----------
_RX_FTIN = re.compile(r"(\d+)'\s*-\s*(\d+(?:\.\d+)?)(?:\s+(\d+)/(\d+))?\"|(\d+)'(?![\d-])|(?<![\d'./])(\d+)/(\d+)\"|(?<![\d'./])(\d+(?:\.\d+)?)(?:\s+(\d+)/(\d+))?\"")
# v81cf90 (CR rev19): '1/4"' sola (pulgada en fracción) se leía como '1/' + '4"' -> 14'-0" - 1 1/2" - 1/4" - 3/4" no cerraba


def _a_decimal(txt):
    def rep(m):
        if m.group(1) is not None:
            v = int(m.group(1)) + (float(m.group(2)) + (int(m.group(3)) / int(m.group(4)) if m.group(3) else 0)) / 12
        elif m.group(5) is not None:
            v = float(m.group(5))
        elif m.group(6) is not None:
            v = int(m.group(6)) / int(m.group(7)) / 12
        else:
            v = (float(m.group(8)) + (int(m.group(9)) / int(m.group(10)) if m.group(9) else 0)) / 12
        return f"{v:.6f}"
    return _RX_FTIN.sub(rep, txt)


def _evaluable(parte):
    t = parte.split(":")[-1]
    t = re.sub(r"(?i)\bpt/ft\b|\bpt\b|\bft\b|\bsf\b|\blf\b", " ", t).replace("÷", "/").replace("×", "*")
    t = re.sub(r"(?<=\d)\s*x\s*(?=[\d(])", "*", t)
    t = re.sub(r"(?i)^\s*(total|sum)\b", "", t).strip()
    if not t or not re.fullmatch(r"[\d.+\-*/() ]+", t) or not re.search(r"\d", t):
        return None, False
    try:
        return float(eval(t, {"__builtins__": {}}, {})), bool(re.search(r"\d\s*[-+*/]\s*[\d(]|\)\s*[-+*/]", t))
    except Exception:                                          # noqa: BLE001
        return None, False


def cierre(op, h):
    """-> (ok, detalle). Comentarios en paréntesis con palabras se quitan; cada 'expr = valor' con operador debe cuadrar ± 1/4";
    el último número de la operación = Printed H."""
    s = str(op or "")
    if not s.strip():
        return False, "DERIVED sin Operation"
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r"\([^()]*[A-Za-z=,][^()]*\)", " ", s)
    s = _a_decimal(s)
    malas, ult = [], None
    for cl in s.split(";"):
        partes = cl.split("=")
        vals = [_evaluable(p) for p in partes]
        for (v1, op1), (v2, _o) in zip(vals, vals[1:]):
            if v1 is not None and v2 is not None and op1 and abs(v1 - v2) > TOL_EXT:
                malas.append(f"'{cl.strip()[:90]}': {v1:.4f} != {v2:.4f}")
        for v, _o in vals:
            if v is not None:
                ult = v
    if malas:
        return False, "; ".join(malas)
    if ult is None:
        return False, "operación sin aritmética que re-calcular"
    if h is None or abs(ult - h) > TOL_EXT:
        return False, f"la operación termina en {ult:.4f} y la Printed H es {h}"
    return True, "cierra"


# ---------- (3) / (4) reglas físicas y cruce por cuarto ----------
def _rooms_de_location(loc):
    """CR City Hotel (v81cf90): caras descritas en texto 'L2 Bath 208 north wall | faces: 208 living; corridor 216' -> salas."""
    m = re.search(r"(?i)\bfaces?:\s*(.+)$", str(loc or ""))
    if not m:
        return []
    out = []
    for parte in re.split(r"[;/]", m.group(1)):
        k = sala(parte)
        if RX_LLAVE_CUARTO.fullmatch(k):
            out.append(k)
    return out


def _es_madera(w):
    """wall de madera (board only): sin top track metálico (U-139 / R80f.1); el slip track de U-056 no aplica."""
    t = " ".join(str(w.get(k) or "") for k in ("stud_text", "decision", "type_id", "board"))
    return bool(re.search(r"(?i)wood[- ]framed|board only|WOOD FRAMING EXCLUDED|U-139|R80f\.1", t))


RX_ABV_CEIL = re.compile(r"(?i)(?:(?:MIN(?:IMUM)?|TYP(?:ICAL)?|MAX(?:IMUM)?)\.?\s+)?(?:ABOVE|ABV\.?)\s+(?:THE\s+)?(?:LINE\s+OF\s+(?:THE\s+)?|HIGHEST\s+(?:ADJACENT\s+)?|ADJACENT\s+)?"
                         r"(?:FINISH(?:ED)?\s+|SUSPENDED\s+|ACOUSTICAL\s+)?(?:CEILINGS?|CLG)\b")
RX_TO_DECK = re.compile(r"(?i)\bTO (THE )?(U/S |UNDERSIDE OF |B\.?O\.? (OF )?)?(DECK|STRUCTURE|ROOF|JOIST)")
RX_TOPE_ESTRUCTURA = re.compile(r"(?i)WHICHEVER\s+IS\s+LOWER|\bOR\s+TO\s+(?:THE\s+)?(?:U/S\s+|UNDERSIDE\s+OF\s+|B\.?O\.?\s+(?:OF\s+)?)?(?:DECK|STRUCTURE)")
_IN = r"(?:[\"”″]|''|IN\.?|INCH(?:ES)?)"
_PAL = {"ONE": 1, "TWO": 2, "THREE": 3, "FOUR": 4, "FIVE": 5, "SIX": 6, "SEVEN": 7, "EIGHT": 8, "NINE": 9, "TEN": 10, "ELEVEN": 11, "TWELVE": 12}


def _offset_antes(pre):
    """BE-CR46 (verificación v138e #5 / #6): offset escrito justo antes de 'above ceiling' -> pies: 6" / 6” / 6 IN. / 4 1/2" / 1'-0" / six inches."""
    pre = pre[-40:]
    m = re.search(r"(\d+)\s*['’′]\s*-?\s*(?:(\d+)(?:\s+(\d+)/(\d+))?\s*" + _IN + r")?\s*$", pre, re.I)
    if m:
        return int(m.group(1)) + (int(m.group(2) or 0) + (int(m.group(3)) / int(m.group(4)) if m.group(4) and int(m.group(4)) else 0)) / 12
    m = re.search(r"(\d+)(?:\s+(\d+)/(\d+)|(\.\d+))?\s*" + _IN + r"\s*$", pre, re.I)
    if m:
        v = int(m.group(1)) + (int(m.group(2)) / int(m.group(3)) if m.group(3) and int(m.group(3)) else 0) + float(m.group(4) or 0)
        return v / 12
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:FT\.?|FEET|FOOT)\s*$", pre, re.I)
    if m:
        return float(m.group(1))
    m = re.search(r"\b(" + "|".join(_PAL) + r")\s*(?:\(\d+\)\s*)?INCH(?:ES)?\s*$", pre, re.I)
    if m:
        return _PAL[m.group(1).upper()] / 12
    return None


def regla_texto(txt):
    """BE-CR46 (v81cf138e): ("above_ceiling", ext ft) / ("to_deck", 0) / ("fixed", 0) del texto de altura; '6\" above LINE OF ceiling'
    = above_ceiling (antes el regex no tenía 'LINE OF' y caía en fixed); el número above ceiling manda sobre 'to structure'."""
    txt = str(txt or "")
    for m in RX_ABV_CEIL.finditer(txt):
        off = _offset_antes(txt[:m.start()])
        if off is not None:
            return "above_ceiling", off
    if RX_TO_DECK.search(txt) and not re.search(r"(?i)ABOVE (THE )?CEILING", txt):
        return "to_deck", 0.0
    return "fixed", 0.0


def heads_de_fichas(fichas):
    """BE-CR46: {TYPE_ID (mayúsculas): (regla, ext, texto, tope_estructura)} del HEAD de cada type en fichas.json (lectura independiente
    del Partition Type Schedule, BE-122). Solo heads 'N above (line of) ceiling' (el head no llega a estructura). fichas ilegible = ValueError."""
    try:
        fj = json.load(open(fichas, encoding="utf-8")) if isinstance(fichas, str) else (fichas if fichas is not None else {})
    except (OSError, ValueError) as e:
        raise ValueError(f"fichas.json ilegible ({type(e).__name__}: {e})")
    if not isinstance(fj, dict):
        raise ValueError(f"fichas.json: se esperaba un objeto con 'types', llegó {type(fj).__name__}")
    t = fj.get("types") or {}
    it = t.items() if isinstance(t, dict) else [(x.get("id") or x.get("type") or x.get("type_id") or x.get("tag"), x) for x in t if isinstance(x, dict)]
    out = {}
    for k, v in it:
        txt = v.get("height") if isinstance(v, dict) else v
        if isinstance(txt, dict):
            txt = " ".join(str(x) for x in txt.values())
        regla, ext = regla_texto(txt)
        if k and txt:                    # todas las reglas (la familia se decide con todas); solo 'above_ceiling' manda sobre el wall
            out[str(k).strip().upper()] = (regla, ext, str(txt), bool(RX_TOPE_ESTRUCTURA.search(str(txt))))
    return out


def head_de(heads, tid, tag=None):
    """head 'above ceiling' del type: id exacto (sin importar mayúsculas), luego el tag, luego la familia (FW.4-2 -> FW.4-*) solo si TODOS
    los types de la familia en fichas.json tienen la misma regla (verificación v138e #5)."""
    for k in (tid, tag):
        k = str(k or "").strip().upper()
        if k and k in heads:
            v = heads[k]
            return (v, "type head") if v[0] == "above_ceiling" else (None, None)
    for k in (tid, tag):
        kk = str(k or "").strip().upper()
        fam = re.sub(r"-\d+[A-Z]?$", "", kk)
        if fam and fam != kk:
            hs = [v for x, v in heads.items() if re.sub(r"-\d+[A-Z]?$", "", x) == fam]
            if hs and len({(v[0], v[1], v[3]) for v in hs}) == 1 and hs[0][0] == "above_ceiling":
                return hs[0], f"type head (familia {fam})"
    return None, None


def _caras_de_location(loc):
    """caras del texto 'faces: 208 living; corridor 216 / LOBBY (N part)' -> [(llave, texto)]; sin número la llave es el nombre sin
    paréntesis (verificación v138e-2 #1: LOBBY / PASSAGE también son cuartos)."""
    m = re.search(r"(?i)\bfaces?:\s*(.+)$", str(loc or ""))
    if not m:
        return []
    out = []
    for grupo in re.split(r"[;|]", re.sub(r"\([^)]*\)", " ", m.group(1))):
        partes = []
        for x in grupo.split("/"):            # '/' separa cuartos solo si lo que sigue trae número ('bath/closet' = una cara)
            if partes and not re.search(r"\b\d{3}[A-Z]?\b", x):
                partes[-1] += "/" + x
            else:
                partes.append(x)
        for parte in partes:
            parte = re.sub(r"\s+", " ", parte).strip(" ,")
            if parte:
                out.append((sala(parte), parte))
    return out


RX_PAL_CUARTO = re.compile(r"[a-z]{2,}")
NO_PAL = {"the", "and", "side", "face", "part", "room", "wall", "north", "south", "east", "west", "verify", "with", "of", "to", "at", "in", "on"}
SINON = {"shower": "bath", "toilet": "bath", "wc": "bath", "vanity": "bath", "restroom": "bath", "lav": "bath", "lavatory": "bath",
         "bathroom": "bath", "hall": "corridor", "hallway": "corridor", "corr": "corridor"}


def _sing(w):
    return w[:-1] if len(w) > 4 and w.endswith("s") and not w.endswith("ss") else w      # 'toilets' / 'showers' / 'restrooms'


def _pal(s):
    return {SINON.get(_sing(w), _sing(w)) for w in RX_PAL_CUARTO.findall(str(s).lower())} - NO_PAL


RX_PREP = re.compile(r"(?i)\s(?:(?:north|south|east|west)\s+)?(?:of|near|behind|beside|next to|at|by|to|toward|towards|in front of)\s")
PAL_HUMEDO = {"bath"}


def ch_cara(det, k, texto):
    """BE-CR46: C.H. del cuarto de UNA cara, o None si no se sabe con certeza (el wall no se juzga, nunca un FAIL falso).
    Filas de ALTURAS_CUARTOS con la misma llave ('Bath 212' / 'Guest room 212' -> 212) se distinguen por el nombre (shower / toilet /
    WC = bath). 'corridor south of toilet 212' = el corridor (lo que va antes de 'of / near / behind' manda); 'guest room 212 bath' = el
    baño (empate con una palabra de cuarto húmedo); empate sin cuarto húmedo o cara que nombra otro cuarto = None."""
    rows = (det or {}).get(k) or []
    if not rows:
        return None
    if len(rows) == 1 and not _pal(texto):
        return rows[0][1]
    antes = RX_PREP.split(" " + str(texto) + " ", 1)
    prep = len(antes) > 1 and bool(_pal(antes[0]))
    for txt in ((antes[0],) if prep else (str(texto),)):    # verificación e-3 #1: con 'X of Y' manda X; si X no está en las filas = None
        pal = _pal(txt)
        if not pal:
            continue
        sc = [(len(pal & _pal(n)), ch, n) for n, ch in rows]
        mejor = max(s for s, _c, _n in sc)
        if mejor == 0:
            return None if prep else None
        cand = [(ch, n) for s, ch, n in sc if s == mejor]
        if len({ch for ch, _n in cand}) == 1:
            return cand[0][0]
        if pal & PAL_HUMEDO:
            hum = {ch for ch, n in cand if _pal(n) & PAL_HUMEDO}
            return hum.pop() if len(hum) == 1 else None
        seco = {ch for ch, n in cand if not _pal(n) & PAL_HUMEDO}       # CR rev20d: '201 guest room' = la habitación, no el baño
        return seco.pop() if len(seco) == 1 else None
    if len({ch for _n, ch in rows}) == 1 and not any(_pal(n) for n, _c in rows):
        return rows[0][1]
    return None


def walls_de_canon(canon, heads=None):
    """walls[] + existing_walls[] (CR City Hotel: los walls de madera board-only viven en existing_walls).
    heads (BE-CR46): {type_id: (regla, ext, texto)} de heads_de_fichas; el head del type manda sobre el texto del wall."""
    heads = heads or {}
    out = []
    for w in (canon.get("walls") or []) + (canon.get("existing_walls") or []):
        if str(w.get("element") or "wall") not in ("wall", "column_wrap", "furring", "shaft_wall", "chase"):
            continue
        h = ftin(w.get("height_ft"))
        if h is None:
            continue
        txt = " ".join(str(w.get(k) or "") for k in ("height_op", "height_source", "height_source_info", "top_track_info"))
        regla, ext = regla_texto(txt)
        tid = str(w.get("type_id") or w.get("tag") or "")
        conflicto, fuente, tope_est = None, "wall", False
        hd_, fuente_h = head_de(heads, w.get("type_id"), w.get("tag"))
        if hd_:                                             # BE-CR46: el HEAD del type manda sobre la cota / texto del wall
            hr, he, htxt, tope_est = hd_
            if (regla == "to_deck" and not tope_est) or (regla == "above_ceiling" and abs(ext - he) > 1e-6):
                conflicto = f"texto del wall '{regla}' vs head del type {tid} '{htxt[:80]}'"
            regla, ext, fuente = hr, he, fuente_h
        caras = w.get("faces") if isinstance(w.get("faces"), list) else []      # CR: faces = número; las salas van en location
        rooms = [sala(f.get("room")) for f in caras if isinstance(f, dict) and f.get("room")] or _rooms_de_location(w.get("location"))
        out.append({"id": w.get("id"), "tipo": w.get("tag") or w.get("type_id"), "h": h, "regla": regla, "ext": ext,
                    "rooms": rooms, "floor": w.get("floor"), "madera": _es_madera(w),
                    "board": [(f.get("side"), ftin(f.get("height_ft"))) for f in caras if isinstance(f, dict) and ftin(f.get("height_ft")) is not None],
                    "top": str(w.get("top_track_kind") or ""), "motivo": w.get("height_diff_reason"),
                    "bo": ftin(w.get("structure_bo_ft")), "fuente": fuente, "conflicto": conflicto,
                    "caras": [(sala(f.get("room")), str(f.get("room"))) for f in caras if isinstance(f, dict) and f.get("room")] or _caras_de_location(w.get("location"))})   # BE-GK11: B.O. of structure AT this wall (sloped / stepped deck)
    return out


def demo_de_canon(canon):
    out = []
    for m in canon.get("misc_items") or []:
        if m.get("element") != "demo":
            continue
        lf, sf = float(m.get("lf") or 0), float(m.get("sf") or m.get("qty") or 0)
        h = ftin(m.get("h_ft") or m.get("height_ft")) or (sf / lf if lf else None)
        if h is not None:
            out.append({"id": m.get("ref"), "h": round(h, 4)})
    return out


RX_HOJA_MOTIVO = re.compile(r"\b[0-9A-Z]{1,3}/[A-Z]{1,2}-?\d{1,2}(?:\.\d{1,2})?\d*[A-Z]?\b|\b[A-Z]{1,2}-?\d{3}\b|\b[A-Z]{1,2}\d\.\d{2}[A-Z]?\b")


def reglas_fisicas(walls, cuartos, bo, demo=(), cuartos_det=None):
    """walls: [{id, h, regla, ext, rooms, board, top}]; cuartos: {sala: C.H.}; bo: B.O. estructura (None = no impreso). -> (n, fallas)"""
    fallas, n = [], 0
    bo_global = bo
    por_nivel = isinstance(bo_global, dict)        # CR (v81cf92): edificio de varios niveles -> tope físico por nivel {L1: ft, ...}
    for w in walls:
        n += 1
        bo = w.get("bo") if w.get("bo") is not None else (bo_global.get(w.get("floor")) if por_nivel else bo_global)   # BE-GK11
        chr_ = w.get("ch_room") or {}                  # BE-CR47: C.H. del sub-espacio de CADA cara (Bath / Room del mismo número)
        chs = [(r, chr_[r]) if r in chr_ else (r, cuartos[r]) for r in w["rooms"]
               if (r in chr_ and chr_[r] is not None) or (r not in chr_ and cuartos.get(r) is not None)]
        if bo is not None and w["h"] > bo + TOL_EXT:
            fallas.append(f"{w['id']}: H {w['h']:.3f} > B.O. estructura {bo:.3f}")
        # BE-GK12 (Grand Kia): a wall whose height is explained by a printed reason (height_diff_reason with N/HOJA:
        # the room ceiling does not reach the wall line - open showroom side, cloud / well away from the wall) is not
        # failed against that room's C.H.
        # BE-CR33 (CR City Hotel rev19): hojas con punto / guion (A7.05, 4/A5.05, A-101) también son N/HOJA
        expl = bool(w.get("motivo") and RX_HOJA_MOTIVO.search(str(w.get("motivo"))))
        for r, ch in chs:
            if w["h"] + TOL_EXT < ch and not expl:
                fallas.append(f"{w['id']}: H {w['h']:.3f} < C.H. {ch:.3f} del cuarto {r}")
        if w.get("conflicto") and not expl:
            fallas.append(f"{w['id']}: BE-CR46 {w['conflicto']} (el head del type manda; corregir la altura o citar el N/HOJA que lo cambia)")
        if w["regla"] == "above_ceiling" and str(w.get("fuente", "wall")).startswith("type head") and not expl:
            caras_w = w.get("caras") or []
            chh = [ch_cara(cuartos_det, k, txt) if cuartos_det else cuartos.get(k) for k, txt in caras_w]
            if not caras_w or any(c is None for c in chh):
                w["head_sin_ch"] = True          # BE-CR46: una cara sin C.H. cierta = no se juzga (conteo), nunca FAIL falso
            else:
                tope = max(chh) + w["ext"]
                tope = min(tope, bo) if bo is not None else tope
                w["head_juzgado"] = True
                if w["h"] > tope + TOL_EXT:      # BE-CR46 / CB_HEAD_TYPE: H <= C.H. de la cara + offset del head, tope estructura
                    fallas.append(f"{w['id']}: BE-CR46 head del type '{w['ext'] * 12:g}\" above ceiling' = C.H. {max(chh):.3f} + "
                                  f"{w['ext'] * 12:g}\" = {tope:.3f} (tope estructura), cargado {w['h']:.3f}")
        if w["regla"] == "above_ceiling" and w.get("fuente", "wall") == "wall" and not expl:
            if not chs:
                fallas.append(f"{w['id']}: 'above ceiling' sin C.H. impresa de ningún cuarto que toca (ALTURAS_CUARTOS.csv)")
            else:
                esp = max(ch for _r, ch in chs) + w["ext"]
                if w.get("bo") is not None and esp > w["bo"] + TOL_EXT:
                    esp = w["bo"]          # BE-GK12: capped by the structure at the wall (H <= B.O. governs, U-176 control 3)
                if abs(w["h"] - esp) > TOL_EXT:
                    fallas.append(f"{w['id']}: 'above ceiling' = MAYOR C.H. {max(ch for _r, ch in chs):.3f} + {w['ext'] * 12:g}\" = {esp:.3f}, cargado {w['h']:.3f}")
        if w["regla"] == "to_deck":
            exacto = w.get("bo") if w.get("bo") is not None else (None if por_nivel else bo)   # por nivel = tope, no igualdad
            if bo is None:
                fallas.append(f"{w['id']}: 'to deck' sin B.O. de estructura en el canon")
            elif exacto is not None and abs(w["h"] - exacto) > TOL_EXT:
                fallas.append(f"{w['id']}: 'to deck' = B.O. {exacto:.3f}, cargado {w['h']:.3f}")
            if not w.get("madera") and not re.search(r"(?i)slip|deflect|DTR|double", w.get("top") or ""):
                fallas.append(f"{w['id']}: 'to deck' sin slip / deflection track (U-056)")
        for lado, hb in w["board"]:
            if hb > w["h"] + TOL_EXT:
                fallas.append(f"{w['id']}: board de la cara {lado} {hb:.3f} > H del wall {w['h']:.3f}")
    bo = bo_global
    for d in demo:
        n += 1
        bo_d = max((v for v in bo_global.values() if v is not None), default=None) if por_nivel else bo_global
        if bo_d is not None and d["h"] > bo_d + TOL_EXT:
            fallas.append(f"{d['id']}: demolición H {d['h']:.3f} > B.O. / altura de estructura {bo_d:.3f}")
    return n, fallas


def cruce_cuartos(walls, cuartos):
    """-> (n_cuartos_con_walls, fallas, filas)"""
    fallas, filas = [], []
    for r, ch in sorted(cuartos.items()):
        ws = [w for w in walls if r in w["rooms"] and not (r in (w.get("ch_room") or {}) and w["ch_room"][r] is None)]
        if not ws or ch is None:
            continue
        for w in ws:
            chw = (w.get("ch_room") or {}).get(r, ch)       # BE-CR47: 'bath 201' contra el baño 201, no contra la habitación 201
            filas.append({"Room": r, "C.H.": chw, "Wall": w["id"], "H": w["h"], "OK": w["h"] + TOL_EXT >= chw})
            # BE-GK24 (Grand Kia): a wall below the room C.H. whose printed reason (height_diff_reason with N/HOJA) names an open
            # RFI or Review Item is a declared print conflict, not a silent error
            declarado = re.search(r"\bRFI-\d+|\bReview Item\b|\bRI-\d+", str(w.get("motivo") or "")) and \
                RX_HOJA_MOTIVO.search(str(w.get("motivo") or ""))
            if w["h"] + TOL_EXT < chw and not declarado:
                fallas.append(f"cuarto {r} (C.H. {chw:.3f}): {w['id']} H {w['h']:.3f} por debajo del cielo")
        por_tipo = {}
        for w in ws:                                        # BE-CR47: el type se compara dentro del MISMO sub-espacio (misma C.H.)
            por_tipo.setdefault((w["tipo"], (w.get("ch_room") or {}).get(r, ch)), set()).add(round(w["h"], 3))
        for (t, _chs), hs in por_tipo.items():
            # BE-CR33: los renglones con motivo impreso (height_diff_reason con N/HOJA) ya están explicados; el type falla si los
            # renglones SIN motivo tienen alturas distintas entre sí, o si alguna altura distinta queda sin ningún renglón explicado
            sin = {round(w["h"], 3) for w in ws if w["tipo"] == t and (w.get("ch_room") or {}).get(r, ch) == _chs
                   and not (w.get("motivo") and RX_HOJA_MOTIVO.search(str(w.get("motivo"))))}
            if len(hs) > 1 and len(sin) > 1:
                fallas.append(f"cuarto {r}: type {t} con alturas distintas {sorted(hs)} sin motivo impreso (height_diff_reason)")
    n = len({f["Room"] for f in filas})
    return n, fallas, filas


# ---------- (5) evidencia ----------
def _color(i):
    pal = [(0.85, 0.10, 0.10), (0.10, 0.45, 0.85), (0.10, 0.60, 0.20), (0.85, 0.50, 0.00), (0.55, 0.20, 0.70), (0.00, 0.60, 0.60)]
    return pal[i % len(pal)]



FS_SEC, LH_SEC, X_LAB, W_LAB = 7, 10.0, 470, 300


def _envolver(texto, ancho, fs):
    """parte el texto en renglones que caben en 'ancho' pt (Helvetica fs)."""
    import pymupdf
    out, cur = [], ""
    for pal in re.split(r"(?<=[ |,])", texto):
        if cur and pymupdf.get_text_length(cur + pal, fontsize=fs) > ancho:
            out.append(cur.rstrip())
            cur = pal
        else:
            cur += pal
    if cur.strip():
        out.append(cur.rstrip())
    return out or [""]


def seccion_sin_encimar(doc, niveles, titulo):
    """BE-COORD02 (usuario 12-nov, "aqui tiene datos ensimados, arreglalo"): página de sección donde NINGÚN texto se encima.
    Las líneas van a la escala real; cada etiqueta (valor + texto) va en su propio hueco a la derecha, separada al menos un
    renglón de la anterior, unida a su línea con una guía. La página crece en alto lo que haga falta. -> página"""
    import pymupdf
    bloques = []
    for v, lab, col in niveles:
        rs = _envolver(f"{v:.3f} ft  -  {lab}", W_LAB, FS_SEC)
        bloques.append([v, rs, col, len(rs) * LH_SEC + 3])
    alto_txt = sum(b[3] for b in bloques)
    H = max(612, alto_txt + 140)
    pg = doc.new_page(width=792, height=H)
    pg.insert_text((36, 40), titulo, fontsize=13)
    y0, y1 = H - 42, 70
    top = max(v for v, _r, _c, _h in bloques) or 1
    ys = [y0 - (y0 - y1) * b[0] / top for b in bloques]          # y real de cada línea (abajo = piso)
    # pasada 1 (de abajo hacia arriba): cada etiqueta centrada en su línea, pero nunca encima de la de abajo
    G = 1.5
    pos = []
    for i, (b, y) in enumerate(zip(bloques, ys)):
        p = y - b[3] / 2
        if i and p + b[3] + G > pos[-1]:
            p = pos[-1] - b[3] - G
        pos.append(min(p, y0 + 4 - b[3]))
    # pasada 2 (de arriba hacia abajo): si la de arriba se salió del margen, se baja y empuja a las de abajo
    if pos and pos[-1] < y1:
        pos[-1] = y1
        for i in range(len(pos) - 2, -1, -1):
            pos[i] = max(pos[i], pos[i + 1] + bloques[i + 1][3] + G)
    cajas = []
    for b, y, top_lab in zip(bloques, ys, pos):
        v, rs, col, h = b
        pg.draw_line((80, y), (430, y), color=col, width=1.2)
        ym = top_lab + h / 2
        pg.draw_line((430, y), (X_LAB - 6, ym), color=col, width=0.5)
        for k, r in enumerate(rs):
            pg.insert_text((X_LAB, top_lab + (k + 1) * LH_SEC - 1.5), r, fontsize=FS_SEC, color=col)
        cajas.append((top_lab, top_lab + h))
    pg.draw_line((80, y0), (80, y1), color=(0, 0, 0), width=0.8)
    return pg


def textos_encimados(pdf, pagina=-1, tol=0.5):
    """chequeo BE-COORD02: renglones de texto de una página cuyas cajas se enciman. -> [(t1, t2)]"""
    import pymupdf
    pg = pymupdf.open(pdf)[pagina]
    lin = []
    for bl in pg.get_text("dict")["blocks"]:
        for l in bl.get("lines", []):
            t = "".join(s["text"] for s in l["spans"]).strip()
            if t:
                lin.append((pymupdf.Rect(l["bbox"]), t))
    malos = []
    for i in range(len(lin)):
        for j in range(i + 1, len(lin)):
            r = lin[i][0] & lin[j][0]
            if not r.is_empty and r.width > tol and r.height > tol:
                malos.append((lin[i][1][:40], lin[j][1][:40]))
    return malos

def paginas_de_alturas(paginas):
    """v81cf106 (CR rev20 con v81cf105: 'could not convert string to float: double_ceiling'): {altura: página} solo de las llaves numéricas;
    las páginas especiales ('section', 'double_ceiling', las que vengan) no son alturas."""
    out = {}
    for k, v in (paginas or {}).items():
        try:
            out[float(k)] = v
        except (TypeError, ValueError):
            continue
    return out


FS_DC, LH_DC = 6.0, 8.0


def _envolver_celda(texto, ancho, fs):
    """BE-GK41: renglones de `texto` que caben en `ancho` pt a `fs` pt (por palabra; una palabra más larga se parte por letras). Nunca recorta."""
    import pymupdf
    L = lambda t: pymupdf.get_text_length(t, fontname="helv", fontsize=fs)   # noqa: E731
    out, cur = [], ""
    for pal in str(texto or "").split():
        while L(pal) > ancho:                            # palabra más ancha que la columna
            i = max(1, int(len(pal) * ancho / max(L(pal), 1)))
            while i > 1 and L(pal[:i]) > ancho:
                i -= 1
            if cur:
                out.append(cur)
                cur = ""
            out.append(pal[:i])
            pal = pal[i:]
        prueba = (cur + " " + pal).strip()
        if L(prueba) <= ancho:
            cur = prueba
        else:
            out.append(cur)
            cur = pal
    if cur or not out:
        out.append(cur)
    return out


def paginas_doble_cielo(doc, csv_path, paginas=None):
    """U-190 ⭐ REGLA DE ORO #3: página(s) 'DOUBLE CEILING' de ALTURAS_REVISADAS con la tabla Auditoria/DOBLE_CIELO.csv, un renglón por
    cuarto (single / double), sin textos encimados (renglón fijo de 12 pt, página nueva cuando se llena; U-187)."""
    import pymupdf
    if not (csv_path and os.path.isfile(csv_path)):
        return 0
    filas = leer_csv(csv_path)
    cols = [("Room", 100), ("Level", 30), ("Type", 36), ("Upper ceiling", 85), ("Lower ceiling", 85), ("Heights", 70), ("N/SHEET", 60),
            ("Framing", 120), ("Row / reason", 130)]
    alias = {"Room": "Cuarto", "Level": "Piso", "Type": "Tipo", "Upper ceiling": "Cielo superior", "Lower ceiling": "Cielo inferior",
             "Heights": "Alturas", "N/SHEET": "N/HOJA", "Framing": "Metal", "Row / reason": "Renglón / motivo"}

    def celda(r, c):
        return str(r.get(c) or r.get(alias[c]) or "")
    k, n = 0, 0
    while k < len(filas) or n == 0:
        pg = doc.new_page(width=792, height=612)
        n += 1
        if paginas is not None and n == 1:
            paginas["double_ceiling"] = len(doc)
        nd = sum(1 for r in filas if celda(r, "Type").lower() == "double")
        pg.insert_text((36, 36), f"DOUBLE CEILING - every RCP space checked (U-190): {len(filas)} rooms, {nd} double" + (f" (page {n})" if n > 1 else ""),
                       fontsize=12)
        x, y = 36, 56
        for c, w in cols:
            pg.insert_text((x, y), c, fontsize=7.5, fontname="hebo")
            x += w
        y += 12
        while k < len(filas):                            # BE-GK41: la celda se parte en renglones dentro de su columna (nunca invade ni recorta)
            celdas = [(c, w, _envolver_celda(celda(filas[k], c), w - 4, FS_DC)) for c, w in cols]
            alto = max(len(ls) for _c, _w, ls in celdas) * LH_DC + 3
            if y + alto > 590 and y > 70:
                break                                    # no cabe: página nueva
            x = 36
            col = (0.8, 0, 0) if celda(filas[k], "Type").lower() == "double" else (0, 0, 0)
            for _c, w, ls in celdas:
                for i, ln in enumerate(ls):
                    pg.insert_text((x, y + i * LH_DC), ln, fontsize=FS_DC, color=col)
                x += w
            y += alto
            k += 1
        if not filas:
            break
    return n


def alturas_revisadas(final, entrega, salida, bo, cuartos):
    """Una página por altura distinta (recorte circulado + operación + walls) + página de sección con líneas. -> {altura: página}"""
    import pymupdf
    doc = pymupdf.open()
    grupos = {}
    for r in final:
        grupos.setdefault(round(ftin(r["Printed H"]), 3), []).append(r)
    paginas, labs = {}, []                     # BE-CR0-06: un Page Label por página creada (incluidas las de continuación)
    for i, (h, rs) in enumerate(sorted(grupos.items())):
        pg = doc.new_page(width=792, height=612)
        paginas[h] = len(doc)
        labs.append(f"HEIGHT {h:.3f}")
        ft, inch = int(h), (h - int(h)) * 12
        pg.insert_text((36, 40), f"HEIGHT {h:.3f} ft ({ft}'-{inch:.2f}\")  -  {len(rs)} element(s)", fontsize=15, color=_color(i))
        y = 62
        nota = ([f"{', '.join(r['Wall ID'] for r in rs if RX_ANCHO_DES.search(r['Wall ID']))}: developed board width per LF, not a wall height "
                 "(Depth in Bluebeam = board strip; every dimension of the operation circled, RCP + detail - BE-CR35)"]
                if any(RX_ANCHO_DES.search(r["Wall ID"]) for r in rs) else [])
        for linea in [f"Walls: {', '.join(r['Wall ID'] for r in rs)}", *nota, f"Source: {rs[0].get('Source', '')}",
                      f"Operation: {rs[0].get('Operation', '') or 'CONFIRMED (printed dimension as is)'}", f"Status: {rs[0].get('Status', '')}"]:
            for k in range(0, len(linea), 150):
                pg.insert_text((36, y), linea[k:k + 150], fontsize=8)
                y += 11
        img = rs[0].get("Image") or ""
        p = img if os.path.isabs(img) else os.path.join(entrega, img)
        if os.path.isfile(p):
            if y + 6 > 540:                    # BE-CR0-05: la lista de walls llenó la página -> imagen en página de continuación (U-187)
                pg = doc.new_page(width=792, height=612)
                pg.insert_text((36, 40), f"HEIGHT {h:.3f} ft (continued) - image", fontsize=12, color=_color(i))
                labs.append(f"HEIGHT {h:.3f} (continued)")
                y = 52
            pg.insert_image(pymupdf.Rect(36, y + 6, 756, 590), filename=p, keep_proportion=True)
    niveles = [(0.0, "FLOOR (F.F. 0'-0\")", (0, 0, 0))]
    niveles += [(ch, f"C.H. {r} {ch:.3f}", (0.4, 0.4, 0.4)) for r, ch in sorted(((k, v) for k, v in cuartos.items() if v is not None), key=lambda x: x[1])]
    corto = lambda ids: ", ".join(ids) if len(ids) <= 4 else f"{ids[0]}..{ids[-1]} ({len(ids)})"
    niveles += [(h, f"LOADED H {h:.3f}: {corto([x['Wall ID'] for x in rs])}", _color(i)) for i, (h, rs) in enumerate(sorted(grupos.items()))]
    if bo is not None:
        if isinstance(bo, dict):                                   # v81cf90: B.O. por nivel (edificio de varios niveles)
            niveles += [(v_, f"B.O. {k_} {v_:.3f}", (0.6, 0.0, 0.0)) for k_, v_ in sorted(bo.items()) if v_ is not None]
        else:
            niveles.append((bo, f"B.O. STRUCTURE {bo:.3f}", (0.6, 0.0, 0.0)))
    junt = {}
    for v, lab, col in niveles:                                     # un renglón por valor
        k = round(v, 3)
        junt[k] = (k, (junt[k][1] + " | " + lab) if k in junt else lab, col if k not in junt else junt[k][2])
    niveles = sorted(junt.values())
    seccion_sin_encimar(doc, niveles, "SECTION - every loaded height drawn as a horizontal line (U-176 control 5)")
    paginas["section"] = len(doc)
    ndc = paginas_doble_cielo(doc, os.path.join(entrega, "Auditoria", "DOBLE_CIELO.csv"), paginas)   # U-190 REGLA DE ORO #3
    n_sec = paginas["section"] - len(labs)                                 # páginas de sección (seccion_sin_encimar puede usar varias)
    labs += ["SECTION" if n_sec == 1 else f"SECTION {k + 1}" for k in range(n_sec)]
    labs += [f"DOUBLE CEILING {k + 1}" if ndc > 1 else "DOUBLE CEILING" for k in range(ndc)]
    assert len(labs) == len(doc), f"BE-CR0-06: {len(labs)} Page Labels para {len(doc)} páginas"
    doc.set_page_labels([{"startpage": k, "prefix": lab, "style": "", "firstpagenum": 1} for k, lab in enumerate(labs)])   # Page Labels (U-151): una por página
    doc.save(salida)
    return paginas


def capa_colores(pdf, alturas_por_id, salida):
    """Capa OCG 'HEIGHTS (U-176)': cada markup con Wall ID conocido re-trazado en el color de su altura + leyenda en cada página.
    Contenido de página dentro de la capa (Shape.finish(oc=...)), NO anotaciones: no entra en la Markups List. -> n trazos"""
    import pymupdf
    doc = pymupdf.open(pdf)
    if any(v.get("name") == CAPA for v in (doc.get_ocgs() or {}).values()):
        doc.save(salida, garbage=0)                                   # ya tiene la capa: no se duplica
        return 0
    oc = doc.add_ocg(CAPA, on=True)
    hs = sorted(set(alturas_por_id.values()))
    n = 0
    for pg in doc:
        usadas = set()
        sh = pg.new_shape()
        for a in pg.annots() or []:
            m = re.search(r"(DEMO-\d+|[A-Z]{1,4}\d*-\d{1,3}[A-Z]?)", base_id(a.info.get("id") or ""))
            h = alturas_por_id.get(m.group(1)) if m else None
            if h is None or not a.vertices or len(a.vertices) < 2:
                continue
            sh.draw_polyline([pymupdf.Point(v) for v in a.vertices])
            sh.finish(color=_color(hs.index(h)), width=3, stroke_opacity=0.55, closePath=a.type[1] == "Polygon", oc=oc)
            n += 1
            usadas.add(h)
        D = pg.derotation_matrix                                      # leyenda en coordenadas VISIBLES (hojas rotadas)
        y = 40
        for h in sorted(usadas):
            sh.draw_line(pymupdf.Point(40, y) * D, pymupdf.Point(80, y) * D)
            sh.finish(color=_color(hs.index(h)), width=4, oc=oc)
            y += 16
        sh.commit(overlay=True)
        y = 44
        if usadas:
            pg.insert_text(pymupdf.Point(40, 28) * D, "HEIGHTS (U-176) - board / wall height per markup", fontsize=9,
                           rotate=pg.rotation, color=(0, 0, 0), oc=oc)
        for h in sorted(usadas):
            pg.insert_text(pymupdf.Point(86, y) * D, f"H {h:.3f} ft", fontsize=9, rotate=pg.rotation, color=_color(hs.index(h)), oc=oc)
            y += 16
    doc.save(salida, garbage=0)
    _bitacora("comparar_alturas.capa_colores", [pdf, salida])        # U-184 (3): la salida queda como producida por la cadena
    return n


def _bitacora(tool, archivos):
    """registra en $BITACORA (si existe) el sha256 de lo que produjo esta herramienta, como bitacora.py run."""
    import datetime
    import hashlib
    p = os.environ.get("BITACORA")
    if not p:
        return
    hs = {}
    for f in archivos:
        if f and os.path.isfile(f):
            hs[os.path.abspath(f)] = hashlib.sha256(open(f, "rb").read()).hexdigest()
    try:                                    # BE-GK38: same hash chain as bitacora.py run (a row without 'prev' broke it)
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import bitacora as _B
        if os.path.realpath(_B.BIT) == os.path.realpath(p):
            _B.anotar({"tool": tool, "args": list(archivos), "rc": 0, "hashes": hs})
            return
    except ImportError:
        pass
    with open(p, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"tool": tool, "args": list(archivos), "rc": 0, "hashes": hs, "ts": datetime.datetime.now().isoformat(timespec="seconds")}) + "\n")


def tiene_capa(pdf):
    import pymupdf
    d = pymupdf.open(pdf)
    return any(v.get("name") == CAPA for v in (d.get_ocgs() or {}).values())


# ---------- (6) muestreo ----------
def muestra(final, paginas, semilla=176, minimo=5):
    rnd = random.Random(semilla)
    grupos = {}
    for r in final:
        grupos.setdefault(round(ftin(r["Printed H"]), 3), []).append(r["Wall ID"])
    elegidos = [rnd.choice(sorted(ws)) for _h, ws in sorted(grupos.items())]
    resto = [r["Wall ID"] for r in final if r["Wall ID"] not in elegidos]
    rnd.shuffle(resto)
    elegidos += resto[:max(0, minimo - len(elegidos))]
    h_de = {r["Wall ID"]: round(ftin(r["Printed H"]), 3) for r in final}
    return [{"Wall ID": w, "H (ft)": h_de[w], "ALTURAS_REVISADAS page": paginas.get(h_de[w])} for w in elegidos]


def muestra_fallas(filas, final):
    hs = {round(ftin(r["Printed H"]), 3) for r in final}
    cub = {round(float(f["H (ft)"]), 3) for f in filas}
    ev = []
    if len(filas) < min(5, len(final)):
        ev.append(f"muestra de {len(filas)} walls (mínimo {min(5, len(final))})")
    if hs - cub:
        ev.append(f"alturas sin wall en la muestra: {sorted(hs - cub)}")
    if any(not f.get("ALTURAS_REVISADAS page") for f in filas):
        ev.append("muestra sin página de ALTURAS_REVISADAS")
    return ev


# ---------- todo junto ----------
def controles(entrega, canon, markups_pdf=None, construir=True, semilla=176, fichas=None):
    au = os.path.join(entrega, "Auditoria")
    P = lambda n: os.path.join(au, n)
    res = {"fallas": {}, "conteos": {}}
    falta = [n for n in ("ALTURAS_IMPRESAS_A.csv", "ALTURAS_IMPRESAS_B.csv", "ALTURAS_IMPRESAS.csv", "ALTURAS_CUARTOS.csv") if not os.path.isfile(P(n))]
    if falta:
        res["fallas"]["archivos"] = [f"falta Auditoria/{n}" for n in falta]
        return res
    a, b, final = leer_csv(P("ALTURAS_IMPRESAS_A.csv")), leer_csv(P("ALTURAS_IMPRESAS_B.csv")), leer_csv(P("ALTURAS_IMPRESAS.csv"))
    resol = {r["Wall ID"]: r for r in leer_csv(P("ALTURAS_AB_RESOLUCION.csv"))} if os.path.isfile(P("ALTURAS_AB_RESOLUCION.csv")) else {}
    filas_ab, f1 = comparar_ab(a, b, resol)
    f1 += cobertura_ab(a, b, final, depth_ids_vista(P("VISTA_BLUEBEAM.csv")))     # BE-CR35
    res["fallas"]["7_lados"] = lados_fallas(final)                               # BE-CR37
    res["conteos"]["7_lados"] = f"{sum(1 for r in final if RX_ANCHO_DES.search(str(r.get('Wall ID') or '')))} anchos desarrollados con side / faces"
    if os.path.isfile(P("ALTURAS_CUARTOS_A.csv")) and os.path.isfile(P("ALTURAS_CUARTOS_B.csv")):      # C.H. de cuartos también A / B
        la, lb = leer_cuartos(P("ALTURAS_CUARTOS_A.csv")), leer_cuartos(P("ALTURAS_CUARTOS_B.csv"))
        la, lb = llaves_ab(la, lb)                        # verificación i #2: 'Restroom 913' (A) y '913' (B) = el mismo cuarto
        ca = [{"Wall ID": "ROOM " + k, "Printed H": v} for k, v in la]
        cb = [{"Wall ID": "ROOM " + k, "Printed H": v} for k, v in lb]
        fc, ff = comparar_ab([x for x in ca if x["Printed H"] is not None], [x for x in cb if x["Printed H"] is not None], resol)
        filas_ab += fc
        f1 += ff
    else:
        f1.append("faltan Auditoria/ALTURAS_CUARTOS_A.csv / _B.csv (C.H. de los cuartos por las dos lecturas)")
    if construir:
        with open(P("ALTURAS_AB.csv"), "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(filas_ab[0]) if filas_ab else ["Wall ID"]); w.writeheader(); w.writerows(filas_ab)
    res["conteos"]["1_doble_lectura"] = f"{sum(r['Result'] == 'MATCH' for r in filas_ab)} iguales + {sum(r['Result'] == 'RESOLVED' for r in filas_ab)} resueltas de {len(filas_ab)}"
    res["fallas"]["1_doble_lectura"] = f1 + ([] if filas_ab else ["0 alturas comparadas A / B"])
    f2, nd = [], 0
    for r in final:
        if r.get("Status", "").upper() == "DERIVED":
            nd += 1
            ok, det = cierre(r.get("Operation"), ftin(r.get("Printed H")))
            if not ok:
                f2.append(f"{r['Wall ID']}: {det}")
    res["conteos"]["2_cierre"] = f"{nd - len(f2)}/{nd} DERIVED cierran"
    res["fallas"]["2_cierre"] = f2
    cuartos = {}
    for k, v in leer_cuartos(P("ALTURAS_CUARTOS.csv")):
        cuartos[k] = v
    cuartos_pdf = dict(cuartos)                           # verificación i #1: el PDF lista solo los cuartos impresos (sin alias)
    alias_cuartos(cuartos)                                # BE-CR47
    can = json.load(open(canon)) if isinstance(canon, str) else canon
    dh = ((can.get("constants") or {}).get("deck_heights") or {}).get("value")
    bo = {k: ftin(v) for k, v in dh.items()} if isinstance(dh, dict) else ftin(dh)    # v81cf90: por nivel {L1: 14'-0", ...}
    hd, fh = {}, []
    if fichas and (not isinstance(fichas, str) or os.path.isfile(fichas)):
        try:
            hd = heads_de_fichas(fichas)                     # BE-CR46
        except ValueError as e:
            fh = [f"BE-CR46: {e}"]
    det = {}
    for r in leer_csv(P("ALTURAS_CUARTOS.csv")):
        if not RX_NO_CUARTO.search(str(r.get("Room") or "")) and ftin(r.get("C.H. (ft)")) is not None:
            det.setdefault(sala(r.get("Room")), []).append((str(r.get("Room") or "").lower(), ftin(r.get("C.H. (ft)"))))
    for k in list(det):                                   # BE-CR47: alias baño / unidad cuando el CSV no los separa
        m = re.fullmatch(r"(\d{3}[A-Z]?)(-bath)?", str(k))
        if m:
            det.setdefault(m.group(1) if m.group(2) else m.group(1) + "-bath", det[k])
    ws = walls_de_canon(can, hd)
    for w in ws:                                          # BE-CR47 (CR rev20d): sub-espacios del mismo número (Bath / Room / Closet)
        w["ch_room"] = {k: ch_cara(det, k, txt) for k, txt in w.get("caras") or [] if len({c for _n, c in det.get(k) or []}) > 1}
    res["conteos"]["3b_head_type"] = (f"type heads 'N in above ceiling' en fichas.json: {sum(1 for v in hd.values() if v[0] == 'above_ceiling')}; "
                                     f"walls regidos por el head: {sum(1 for w in ws if str(w['fuente']).startswith('type head'))}")
    n3, f3 = reglas_fisicas(ws, cuartos, bo, demo_de_canon(can), det)
    nh = [w for w in ws if str(w.get("fuente")).startswith("type head")]
    nj, ns = sum(1 for w in nh if w.get("head_juzgado")), [w["id"] for w in nh if w.get("head_sin_ch")]
    res["conteos"]["3c_head_juzgados"] = f"walls con head juzgados contra la C.H. de su cara: {nj} de {len(nh)}" + (
        f"; sin C.H. cierta de alguna cara (no juzgados, revisar a mano, {len(ns)}): {', '.join(map(str, ns))}" if ns else "")
    if nh and not nj:
        fh.append(f"BE-CR46: {len(nh)} walls con head 'above ceiling' y ninguno se pudo juzgar contra la C.H. de su cara (ALTURAS_CUARTOS.csv "
                  f"sin las filas de esos cuartos o 'faces:' sin nombre de cuarto): chequeo en vacío (U-137)")
    f3 = fh + f3
    res["conteos"]["3_reglas_fisicas"] = f"{n3 - len({x.split(':')[0] for x in f3})}/{n3} elementos sin violación"
    res["fallas"]["3_reglas_fisicas"] = f3 + ([] if n3 else ["0 walls con altura en el canon"])
    n4, f4, filas4 = cruce_cuartos(ws, cuartos)
    res["conteos"]["4_cruce_cuartos"] = f"{n4} cuartos, {len(filas4)} pares cuarto-wall, {len(f4)} fallas"
    res["fallas"]["4_cruce_cuartos"] = f4 + ([] if n4 else ["0 cuartos del RCP cruzados con sus walls"])
    pdf_rev = os.path.join(entrega, "Planos marcados", "ALTURAS_REVISADAS.pdf")
    hs = sorted({round(ftin(r["Printed H"]), 3) for r in final})
    if construir:
        paginas = alturas_revisadas(final, entrega, pdf_rev, bo, cuartos_pdf)
        json.dump({str(k): v for k, v in paginas.items()}, open(P("ALTURAS_REVISADAS_PAGINAS.json"), "w"), indent=1)
        if markups_pdf:
            capa_colores(markups_pdf, {r["Wall ID"]: round(ftin(r["Printed H"]), 3) for r in final}, markups_pdf + ".tmp.pdf")
            os.replace(markups_pdf + ".tmp.pdf", markups_pdf)
    f5 = []
    if not os.path.isfile(pdf_rev):
        f5.append("falta Planos marcados/ALTURAS_REVISADAS.pdf")
    else:
        import pymupdf
        npag = len(pymupdf.open(pdf_rev))
        if npag < len(hs) + 1:
            f5.append(f"ALTURAS_REVISADAS.pdf con {npag} páginas para {len(hs)} alturas distintas + sección")
    if markups_pdf and not tiene_capa(markups_pdf):
        f5.append(f"el PDF de markups no tiene la capa '{CAPA}'")
    res["conteos"]["5_evidencia"] = f"{len(hs)} alturas distintas -> {len(hs)} páginas + sección; capa '{CAPA}'"
    res["fallas"]["5_evidencia"] = f5
    pag = {}
    if os.path.isfile(P("ALTURAS_REVISADAS_PAGINAS.json")):
        pag = paginas_de_alturas(json.load(open(P("ALTURAS_REVISADAS_PAGINAS.json"))))   # v81cf106: solo llaves numéricas
    if construir:
        json.dump(muestra(final, pag, semilla), open(P("ALTURAS_MUESTRA.json"), "w"), indent=1)
    fil6 = json.load(open(P("ALTURAS_MUESTRA.json"))) if os.path.isfile(P("ALTURAS_MUESTRA.json")) else []
    res["conteos"]["6_muestreo"] = f"{len(fil6)} walls al azar, {len({f['H (ft)'] for f in fil6})}/{len(hs)} alturas"
    res["fallas"]["6_muestreo"] = muestra_fallas(fil6, final) if fil6 else ["falta Auditoria/ALTURAS_MUESTRA.json"]
    if construir:
        json.dump(res, open(P("ALTURAS_CONTROLES.json"), "w"), indent=1, ensure_ascii=False)
    return res


def main_extremo(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    sem = int(argv[argv.index("--semilla") + 1]) if "--semilla" in argv else 176
    pos = [x for x in argv[1:] if not x.startswith("--") and not x.isdigit()]
    res = controles(pos[0], pos[1], pos[2] if len(pos) > 2 else None, True, sem)
    for k, v in res["conteos"].items():
        print(f"{k}: {v} - {'FAIL' if res['fallas'].get(k) else 'PASS'}")
    for k, v in res["fallas"].items():
        for x in v:
            print(f"FAIL {k}: {x}")
    return 1 if any(res["fallas"].values()) else 0


# ---------- BE-GK40: pregunta ciega = misma magnitud del Depth cargado (antes tools/pregunta_ciega.py de Grand Kia; unido en v81cf102) ----------
# BE-GK40 (Grand Kia rev2, BE-CR35 blind A/B of every Depth): the blind question asks the SAME magnitude the loaded Depth measures,
# with its definition. GK asked the joist DEPTH while the loaded value was the joist LENGTH (pocket width): both
# blind readers measured another thing (the stud web) and the comparison was void.
# 
#   magnitud(op)                 -> (key, definition) of the Depth from the item's operation text
#   tareas(canon)                -> [{id, magnitude, definition}] for every misc item with a Depth (no loaded value is written)
#   pregunta_fallas(tareas_md, canon) -> [fallas]: a blind task row whose 'what to read' does not name the magnitude of its Depth
# Uso: python3 comparar_alturas.py pregunta tareas <canon.json>  |  python3 comparar_alturas.py pregunta revisar <TAREAS.md> <canon.json>

MAGNITUDES = (   # (key, regex on the operation, definition for the blind reader, words the question must contain)
    ("joist_length", r"\bjoists?\s*x\s*\d", "LENGTH of each joist piece (= width of the pocket / soffit it spans), ft", ("length",)),
    ("developed", r"developed\s*\d", "DEVELOPED board width of the section = sum of every face with board, per side, ft", ("developed",)),
    ("return_depth", r"return depth", "DEPTH of the board return from the wall face to the frame, ft", ("return",)),
    ("stud_height", r"\bstuds?\s*x\s*(average height\s*)?\d", "HEIGHT of each stud (bottom track to top track), ft", ("h", "height")),
    ("face_height", r"\bLF\s*x\s*\d", "HEIGHT of the board face, ft", ("h", "height")),
)


def magnitud(op):
    t = str(op or "")
    for k, rx, d, _w in MAGNITUDES:
        if re.search(rx, t, re.I):
            return k, d
    return None, None


def _id_pc(ref):
    return str(ref).split()[0]


def tareas(canon):
    out, vistos = [], set()
    for m in canon.get("misc_items") or []:
        k, d = magnitud(m.get("op"))
        i = _id_pc(m.get("ref"))
        if k and (i, k) not in vistos:
            vistos.add((i, k))
            out.append({"id": i, "magnitude": k, "definition": d})
    return out


def pregunta_fallas(tareas_md, canon):
    filas = {}
    for ln in str(tareas_md or "").splitlines():
        cs = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cs) >= 3 and re.match(r"^[A-Z]{2,4}-[\w.-]+", cs[0]):
            for i in re.findall(r"[A-Z]{2,4}-[\w-]+", cs[0]):
                filas[i] = cs[-1].lower()
    ev = []
    for t in tareas(canon):
        q = filas.get(t["id"])
        if q is None:
            continue
        w = next(w for k, _rx, _d, w in MAGNITUDES if k == t["magnitude"])
        if not any(re.search(r"\b" + re.escape(x) + r"\b", q) for x in w):
            ev.append(f"{t['id']}: the blind question '{q[:60]}' does not ask the loaded magnitude ({t['definition']}) (BE-GK40)")
    return ev


def main_pregunta(argv):
    """comparar_alturas.py pregunta tareas <canon.json> | pregunta revisar <TAREAS.md> <canon.json>"""
    if len(argv) >= 2 and argv[0] == "tareas":
        for t in tareas(json.load(open(argv[1]))):
            print(f"| {t['id']} | {t['definition']} |")
        return 0
    if len(argv) >= 3 and argv[0] == "revisar":
        ev = pregunta_fallas(open(argv[1], encoding="utf-8").read(), json.load(open(argv[2])))
        print("\n".join(ev) or "OK: every blind question asks the loaded magnitude")
        return 1 if ev else 0
    print(main_pregunta.__doc__)
    return 2


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "pregunta":
        sys.exit(main_pregunta(sys.argv[2:]))
    if len(sys.argv) > 1 and sys.argv[1] == "extremo":
        sys.exit(main_extremo(sys.argv[1:]))
    sys.exit(main(sys.argv[1:]))
