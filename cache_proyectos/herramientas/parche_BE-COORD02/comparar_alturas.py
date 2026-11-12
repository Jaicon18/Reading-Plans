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
    """Llave de cuarto: número impreso (101, 112A) o el nombre en minúsculas."""
    m = re.search(r"\b(\d{3}[A-Z]?)\b", str(nombre or "").upper())
    return m.group(1) if m else re.sub(r"\s+", " ", str(nombre or "").strip().lower())


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
        if re.fullmatch(r"\d{3}[A-Z]?", k):
            out.append(k)
    return out


def _es_madera(w):
    """wall de madera (board only): sin top track metálico (U-139 / R80f.1); el slip track de U-056 no aplica."""
    t = " ".join(str(w.get(k) or "") for k in ("stud_text", "decision", "type_id", "board"))
    return bool(re.search(r"(?i)wood[- ]framed|board only|WOOD FRAMING EXCLUDED|U-139|R80f\.1", t))


def walls_de_canon(canon):
    """walls[] + existing_walls[] (CR City Hotel: los walls de madera board-only viven en existing_walls)."""
    out = []
    for w in (canon.get("walls") or []) + (canon.get("existing_walls") or []):
        if str(w.get("element") or "wall") not in ("wall", "column_wrap", "furring", "shaft_wall", "chase"):
            continue
        h = ftin(w.get("height_ft"))
        if h is None:
            continue
        txt = " ".join(str(w.get(k) or "") for k in ("height_op", "height_source", "height_source_info", "top_track_info"))
        if re.search(r"(?i)\bTO (THE )?(U/S |UNDERSIDE OF |B\.?O\.? (OF )?)?(DECK|STRUCTURE|ROOF|JOIST)", txt) and not re.search(r"(?i)ABOVE (THE )?CEILING", txt):
            regla, ext = "to_deck", 0.0
        else:
            m = re.search(r"(?i)(\d+(?:\.\d+)?)\s*(?:\"|IN\.?|INCH(?:ES)?)\s*ABOVE (THE )?(HIGHEST )?CEILING", txt)
            regla, ext = ("above_ceiling", float(m.group(1)) / 12) if m else ("fixed", 0.0)
        caras = w.get("faces") if isinstance(w.get("faces"), list) else []      # CR: faces = número; las salas van en location
        rooms = [sala(f.get("room")) for f in caras if isinstance(f, dict) and f.get("room")] or _rooms_de_location(w.get("location"))
        out.append({"id": w.get("id"), "tipo": w.get("tag") or w.get("type_id"), "h": h, "regla": regla, "ext": ext,
                    "rooms": rooms, "floor": w.get("floor"), "madera": _es_madera(w),
                    "board": [(f.get("side"), ftin(f.get("height_ft"))) for f in caras if isinstance(f, dict) and ftin(f.get("height_ft")) is not None],
                    "top": str(w.get("top_track_kind") or ""), "motivo": w.get("height_diff_reason"),
                    "bo": ftin(w.get("structure_bo_ft"))})   # BE-GK11: B.O. of structure AT this wall (sloped / stepped deck)
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


def reglas_fisicas(walls, cuartos, bo, demo=()):
    """walls: [{id, h, regla, ext, rooms, board, top}]; cuartos: {sala: C.H.}; bo: B.O. estructura (None = no impreso). -> (n, fallas)"""
    fallas, n = [], 0
    bo_global = bo
    por_nivel = isinstance(bo_global, dict)        # CR (v81cf92): edificio de varios niveles -> tope físico por nivel {L1: ft, ...}
    for w in walls:
        n += 1
        bo = w.get("bo") if w.get("bo") is not None else (bo_global.get(w.get("floor")) if por_nivel else bo_global)   # BE-GK11
        chs = [(r, cuartos[r]) for r in w["rooms"] if cuartos.get(r) is not None]
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
        if w["regla"] == "above_ceiling" and not expl:
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
        ws = [w for w in walls if r in w["rooms"]]
        if not ws or ch is None:
            continue
        for w in ws:
            filas.append({"Room": r, "C.H.": ch, "Wall": w["id"], "H": w["h"], "OK": w["h"] + TOL_EXT >= ch})
            # BE-GK24 (Grand Kia): a wall below the room C.H. whose printed reason (height_diff_reason with N/HOJA) names an open
            # RFI or Review Item is a declared print conflict, not a silent error
            declarado = re.search(r"\bRFI-\d+|\bReview Item\b|\bRI-\d+", str(w.get("motivo") or "")) and \
                RX_HOJA_MOTIVO.search(str(w.get("motivo") or ""))
            if w["h"] + TOL_EXT < ch and not declarado:
                fallas.append(f"cuarto {r} (C.H. {ch:.3f}): {w['id']} H {w['h']:.3f} por debajo del cielo")
        por_tipo = {}
        for w in ws:
            por_tipo.setdefault(w["tipo"], set()).add(round(w["h"], 3))
        for t, hs in por_tipo.items():
            # BE-CR33: los renglones con motivo impreso (height_diff_reason con N/HOJA) ya están explicados; el type falla si los
            # renglones SIN motivo tienen alturas distintas entre sí, o si alguna altura distinta queda sin ningún renglón explicado
            sin = {round(w["h"], 3) for w in ws if w["tipo"] == t and not (w.get("motivo") and RX_HOJA_MOTIVO.search(str(w.get("motivo"))))}
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

def alturas_revisadas(final, entrega, salida, bo, cuartos):
    """Una página por altura distinta (recorte circulado + operación + walls) + página de sección con líneas. -> {altura: página}"""
    import pymupdf
    doc = pymupdf.open()
    grupos = {}
    for r in final:
        grupos.setdefault(round(ftin(r["Printed H"]), 3), []).append(r)
    paginas = {}
    for i, (h, rs) in enumerate(sorted(grupos.items())):
        pg = doc.new_page(width=792, height=612)
        paginas[h] = i + 1
        ft, inch = int(h), (h - int(h)) * 12
        pg.insert_text((36, 40), f"HEIGHT {h:.3f} ft ({ft}'-{inch:.2f}\")  -  {len(rs)} element(s)", fontsize=15, color=_color(i))
        y = 62
        for linea in [f"Walls: {', '.join(r['Wall ID'] for r in rs)}", f"Source: {rs[0].get('Source', '')}",
                      f"Operation: {rs[0].get('Operation', '') or 'CONFIRMED (printed dimension as is)'}", f"Status: {rs[0].get('Status', '')}"]:
            for k in range(0, len(linea), 150):
                pg.insert_text((36, y), linea[k:k + 150], fontsize=8)
                y += 11
        img = rs[0].get("Image") or ""
        p = img if os.path.isabs(img) else os.path.join(entrega, img)
        if os.path.isfile(p):
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
    labs = [f"HEIGHT {h:.3f}" for h in sorted(grupos)] + ["SECTION"]          # Page Labels (U-151): una etiqueta por página
    doc.set_page_labels([{"startpage": k, "prefix": lab, "style": "", "firstpagenum": 1} for k, lab in enumerate(labs)])
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
def controles(entrega, canon, markups_pdf=None, construir=True, semilla=176):
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
    if os.path.isfile(P("ALTURAS_CUARTOS_A.csv")) and os.path.isfile(P("ALTURAS_CUARTOS_B.csv")):      # C.H. de cuartos también A / B
        ca = [{"Wall ID": "ROOM " + k, "Printed H": v} for k, v in leer_cuartos(P("ALTURAS_CUARTOS_A.csv"))]
        cb = [{"Wall ID": "ROOM " + k, "Printed H": v} for k, v in leer_cuartos(P("ALTURAS_CUARTOS_B.csv"))]
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
    can = json.load(open(canon)) if isinstance(canon, str) else canon
    dh = ((can.get("constants") or {}).get("deck_heights") or {}).get("value")
    bo = {k: ftin(v) for k, v in dh.items()} if isinstance(dh, dict) else ftin(dh)    # v81cf90: por nivel {L1: 14'-0", ...}
    ws = walls_de_canon(can)
    n3, f3 = reglas_fisicas(ws, cuartos, bo, demo_de_canon(can))
    res["conteos"]["3_reglas_fisicas"] = f"{n3 - len({x.split(':')[0] for x in f3})}/{n3} elementos sin violación"
    res["fallas"]["3_reglas_fisicas"] = f3 + ([] if n3 else ["0 walls con altura en el canon"])
    n4, f4, filas4 = cruce_cuartos(ws, cuartos)
    res["conteos"]["4_cruce_cuartos"] = f"{n4} cuartos, {len(filas4)} pares cuarto-wall, {len(f4)} fallas"
    res["fallas"]["4_cruce_cuartos"] = f4 + ([] if n4 else ["0 cuartos del RCP cruzados con sus walls"])
    pdf_rev = os.path.join(entrega, "Planos marcados", "ALTURAS_REVISADAS.pdf")
    hs = sorted({round(ftin(r["Printed H"]), 3) for r in final})
    if construir:
        paginas = alturas_revisadas(final, entrega, pdf_rev, bo, cuartos)
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
        pag = {float(k): v for k, v in json.load(open(P("ALTURAS_REVISADAS_PAGINAS.json"))).items() if k != "section"}
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


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "extremo":
        sys.exit(main_extremo(sys.argv[1:]))
    sys.exit(main(sys.argv[1:]))
