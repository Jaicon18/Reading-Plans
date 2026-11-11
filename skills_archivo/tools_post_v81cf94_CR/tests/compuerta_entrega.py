#!/usr/bin/env python3
"""compuerta_entrega.py — BE-121 (usuario 3-nov, INVIOLABLE): COMPUERTA DE ENTREGA por programa.

Toda regla inviolable de categoría "programa" (REGLAS_REGISTRO.json, cuando = "entrega") se revisa AQUÍ, por el FONDO,
antes de entregar. Ninguna entrega sale sin este programa en verde y sin subir_entrega.py (que se niega a subir sin
ENTREGA_OK.json verde y vigente). No hay flag de override.

Uso:
  python3 compuerta_entrega.py <project_workdir> [--entrega entrega.json]
      Busca en <project_workdir> (o lo que diga entrega.json): la carpeta de entrega FINAL_FOR_REVIEW* (Take-off/*.xlsx,
      Planos marcados/*.pdf + *.png, README_REVIEW.md, PARA_REVISAR_EN_LA_MANANA.md, SEGUIMIENTO.md), takeoff_canon.json,
      takeoff.json, TIEMPOS.md, set_texto.json (texto completo del set incl. AutoCAD SHX) y entrega.json
      ({"drive": {"parent_id", "carpeta_proyecto", "carpeta_proyecto_id"}, "escalas": {"A1.1": "1/8"}, ...}).
      Escribe <project_workdir>/ENTREGA_OK.json (PASS / FAIL / AMBER por chequeo con sus reglas y evidencia + sha256 de
      cada archivo entregable). rc 0 = sin FAIL; rc 1 = al menos un FAIL.
  python3 compuerta_entrega.py banco <project_workdir> --cache <raíz del repo Reading-Plans>
      U-130: COMPARATIVA_BANCO.md (familias del Material Summary por LF de partition y por mil SF de piso contra las
      referencias verificadas BANCO_REFS); cada familia OUT OF RANGE se explica en README_REVIEW.md 'Bank comparison'.
  python3 compuerta_entrega.py texto <bidset.pdf> [<otro.pdf> ...] --out <set_texto.json>   (incluye el barrido de burbujas U-137)
  python3 compuerta_entrega.py pdf_editable <pdf> [...]   (U-151 / BE-147: 0 firmas /Sig y Page Labels = hoja)
  python3 compuerta_entrega.py vista_bluebeam <markups.pdf> <excel.xlsx> [--canon c.json] [--csv VISTA_BLUEBEAM.csv]
      (U-153 / BE-149: simula el Markups List de Bluebeam de cada markup y lo cuadra contra el Excel y la etiqueta)
  python3 compuerta_entrega.py burbujas <set_texto.json> <bidset.pdf> [...]   (agrega solo las burbujas a un set_texto ya hecho)
      Extrae por PROGRAMA el texto de cada hoja (texto + contenido de anotaciones, p. ej. "AutoCAD SHX Text") con su
      número de hoja (title block). Lo usa el chequeo BE-120.

Chequeos (id → reglas): ver CHEQUEOS abajo y REGLAS_REGISTRO.json. AMBER no bloquea pero se reporta.
"""
import datetime
import glob
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

VERSION = "compuerta_entrega v3 (BE-121 + biblioteca + CE_CALLOUTS + R80f.29-31, 3-nov-2026)"
DRIVE_RAIZ = "1UReOABlgJPIkGLe8-nRO6U-6i7xpKoIc"          # Shared drives › JC HUNTER PROJECTS › Claude outputs (raíz)
DRIVE_PROHIBIDO = "1rUgu9cFt59LWzuoCUbFPrEjyNXB6ot5h"      # Projects › Claude outputs (PROHIBIDO)
HOJAS6 = ["Inputs", "Partition Takeoff", "Material Summary", "Pending Items", "Review Items", "Scope Checklist"]
CABECERAS = {   # (fila, encabezados) del formato fijo de plantilla_excel.py (idéntico en todas las entregas)
    "Inputs": (4, ["PARAMETER", "VALUE", "NOTE / SOURCE"]),
    "Partition Takeoff": (4, ["Partition / Scope", "Wall #", "Length (LF)", "Height (FT)", "Layers", "Stud Size",
                              "Stud O.C. (in)", "Board (SF)", "Location", "Source (DETAIL/SHEET)", "Status"]),
    "Material Summary": (3, ["Material", "Unit", "Net", "Waste %", "Waste", "Purchase", "Selling unit", "Pieces to buy",
                             "Where it comes from", "Yield check (live formula)"]),
    "Pending Items": (1, ["RFI", "Question / condition", "Delta of each alternative"]),
    "Review Items": (2, ["#", "Phase", "Type / order", "Item", "Sheet + detail", "Image"]),
    "Scope Checklist": (1, ["Scope ID", "Scope", "Status", "Note (quantity, NOT APPLICABLE + sheet, or RFI)"]),
}
PASOS_TIEMPOS = list(range(1, 10))      # pasos 1–9 con hora (10 = subida, ocurre después de esta compuerta)
RX_FT = re.compile(r"\d+\s*'\s*-?\s*\d+(?:\s+\d+/\d+)?\s*\"?|\bEL\.?\s*\d|\d+(?:\.\d+)?\s*(?:ft|FT)\b")
RX_HOJA = re.compile(r"^[A-Z]{1,3}-?\d{1,3}(?:\.\d{1,2})?[A-Z]?$")
# R80f.35: la etiqueta de página "A421.B-RECEPTION ELEVATIONS" -> "A421.B" (sufijo de letra con punto incluido)
RX_HOJA_PREFIJO = re.compile(r"^([A-Z]{1,3}-?\d{1,3}(?:\.(?:\d{1,2}|[A-Z]{1,2}))?[A-Z]?)(?=$|\s*-\s*|\s)")
RX_HOJA_TB = re.compile(r"^[A-Z]{1,3}-?\d{1,3}(?:\.(?:\d{1,2}|[A-Z]{1,2}))?[A-Z]?$")


def hoja_de_etiqueta(lab):
    """R80f.35: número de hoja desde la etiqueta de página: exacto o prefijo antes del título ('A503.C-MILLWORK')."""
    lab = str(lab or "").strip()
    if RX_HOJA_TB.match(lab):
        return lab
    m = RX_HOJA_PREFIJO.match(lab)
    return m.group(1) if m else ""

RX_FASTENER = re.compile(r"(?i)\bscrews?\b|\banchors?\b|titen|tapcon|\bbolts?\b|slab pins?|\bP\.?A\.?F\.?\b|"
                         r"power[- ]driven|\bfasteners?\b|kwik|x-?edni|\bpins?\b")
RX_SLIP = re.compile(r"(?i)slip|deflection|deep[- ]leg|slotted")
RX_TRACK = re.compile(r"(?i)\btrack\b")
RX_CERRADO = re.compile(r"(?i)closed|cerrad|estimator decision|resuelt")
# BE-121 / R-ALC-01/03/05/07 / U-053 / U-061: temas que por orden del usuario NUNCA son RFI
RFI_PROHIBIDOS = [
    ("tornillería (U-053: EXCLUDED sin RFI)", RX_FASTENER),
    ("trade que no hacemos (U-061 / R-ALC-01)", re.compile(
        r"(?i)\bACT\b|acoustical (?:ceiling|tile)|insulation|stucco|roofing|cabinet|casework|millwork|\bwood\b|"
        r"\bFRT\b|plywood|Div\.?\s*0?6\b")),
    ("ductos (R-ALC-03)", re.compile(r"(?i)duct (?:penetration|opening|sleeve)s?|(?:framed )?openings? (?:for|at) ducts?")),
    ("demolición de cielo existente sin tipo (R-ALC-05)", re.compile(r"(?i)existing\s+(?:\w+\s+){0,3}ceilings?.{0,60}(?:demo|remov)|(?:demo|remov)\w*.{0,60}existing\s+(?:\w+\s+){0,3}ceilings?")),
    ("altura de partition existente a demoler (R-ALC-07)", re.compile(r"(?i)(?:demo|remov|existing)\w*[^.]{0,80}\bheights?\b|\bheights?\b[^.]{0,80}(?:demo|to be removed)")),
]


# ----------------------------------------------------------------------------------------------- utilidades
def _sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _leer(p):
    try:
        return open(p, encoding="utf-8").read() if p and os.path.isfile(p) else ""
    except (OSError, UnicodeDecodeError):
        return ""


def _json(p):
    try:
        return json.load(open(p, encoding="utf-8")) if p and os.path.isfile(p) else None
    except (OSError, ValueError):
        return None


def _walk_seguro(base):
    """BE-GK35: os.walk following symlinks (takeoff_work -> work dir) but never entering the same real directory twice:
    two delivery folders each holding a takeoff_work symlink back to the work dir made glob('**') branch exponentially."""
    seen = set()
    for r, ds, fs in os.walk(base, followlinks=True):
        rp = os.path.realpath(r)
        if rp in seen:
            ds[:] = []
            continue
        seen.add(rp)
        ds[:] = sorted(d for d in ds if os.path.realpath(os.path.join(r, d)) not in seen)
        yield r, ds, fs


def _rglob(raiz, pat):
    """BE-GK35: glob with '**' that is loop-safe (see _walk_seguro); without '**' = glob.glob."""
    if "**" not in pat:
        return glob.glob(os.path.join(raiz, pat))
    import fnmatch
    pre, post = pat.split("**", 1)
    post = post.lstrip("/")
    base = os.path.join(raiz, pre) if pre else raiz
    out = []
    for r, _, fs in _walk_seguro(base):
        for f in fs:
            rel = os.path.relpath(os.path.join(r, f), base)
            if fnmatch.fnmatch(rel, post) or fnmatch.fnmatch(rel, "*/" + post):
                out.append(os.path.join(r, f))
    return out


def _ultimo(patrones, raiz):
    for pat in patrones:
        xs = sorted(_rglob(raiz, pat))
        if xs:
            return xs[-1]
    return None


def registro():
    """REGLAS_REGISTRO.json del skill (raíz del skill o $TAKEOFF_SKILL)."""
    for c in (os.environ.get("TAKEOFF_SKILL"), os.path.join(AQUI, ".."),
              os.path.join(AQUI, "..", "take-off-metal-frame-drywall")):
        p = os.path.join(c or "", "REGLAS_REGISTRO.json")
        if c and os.path.isfile(p):
            return _json(p)
    return None


class Ctx:
    def __init__(self, workdir, entrega_json=None):
        self.w = os.path.abspath(workdir)
        self.cfg = _json(entrega_json or os.path.join(self.w, "entrega.json")) or {}
        g = lambda k: (os.path.join(self.w, self.cfg[k]) if self.cfg.get(k) else None)   # noqa: E731
        ed = g("entrega_dir")
        if not ed:
            ds = sorted(d for d in glob.glob(os.path.join(self.w, "FINAL_FOR_REVIEW*")) if os.path.isdir(d))
            ed = ds[-1] if ds else None
        self.entrega = ed
        e = ed or self.w
        self.excel = g("excel") or _ultimo(["Take-off/*.xlsx"], e)
        self.markups = g("markups") or next((p for p in sorted(glob.glob(os.path.join(e, "Planos marcados", "*.pdf")), reverse=True)
                                             if not os.path.basename(p).startswith(("DETALLES_REVISADOS", "SCHEDULES_REVISADOS", "ALTURAS_REVISADAS"))), None)
        self.planos = os.path.join(e, "Planos marcados")
        self.readme = os.path.join(e, "README_REVIEW.md")
        self.para = os.path.join(e, "PARA_REVISAR_EN_LA_MANANA.md")
        self.seg = os.path.join(e, "SEGUIMIENTO.md")
        self.canon_p = g("canon") or _ultimo(["etapas/4_canon/takeoff_canon.json", "takeoff_work/etapas/4_canon/takeoff_canon.json",
                                             "**/4_canon/takeoff_canon.json", "**/takeoff_canon_FINAL*.json"], self.w)
        self.tk_p = g("takeoff") or _ultimo(["proceso_calc/takeoff.json", "**/takeoff.json"], self.w)
        self.tiempos = g("tiempos") or _ultimo(["TIEMPOS.md", "*/TIEMPOS.md"], self.w)
        self.set_p = g("set_texto") or _ultimo(["set_texto.json", "**/set_texto.json"], self.w)
        self.canon = _json(self.canon_p) or {}
        self.tk = _json(self.tk_p) or {}
        self._wb = None

    def wb(self):
        if self._wb is None and self.excel:
            import openpyxl
            self._wb = openpyxl.load_workbook(self.excel, data_only=False)
        return self._wb

    def rfis_abiertos(self):
        """ids de RFI abiertos = renglones de Pending Items (lo que se le entrega al usuario); sin Excel, takeoff.json."""
        wb = self.wb()
        if wb is not None and "Pending Items" in wb.sheetnames:
            out = []
            for r in wb["Pending Items"].iter_rows(min_row=2, values_only=True):
                fila = " | ".join(str(x or "") for x in r[1:])
                if r and r[0] and re.match(r"(?i)\s*[A-Z\-]*RFI", str(r[0])) and not re.search(r"\bCLOSED\b", fila[:300]):
                    out.append((str(r[0]).strip(), fila))
            return out
        return [(str(r.get("id")), str(r.get("pregunta") or "")) for r in self.rfis()
                if not RX_CERRADO.search(str(r.get("estado") or r.get("status") or ""))]

    def rfis(self):
        xs = list(self.tk.get("rfis") or [])
        ids = {str(r.get("id")) for r in xs}
        xs += [r for r in (self.canon.get("rfis") or []) if str(r.get("id")) not in ids]
        return xs

    def rfi(self, rid):
        return next((r for r in self.rfis() if str(r.get("id")) == rid), None)

    def archivos_entrega(self):
        if not self.entrega or not os.path.isdir(self.entrega):
            return []
        return sorted(os.path.join(r, f) for r, _, fs in os.walk(self.entrega) for f in fs)


CHEQUEOS = []


def chequeo(cid, reglas, desc):
    def deco(fn):
        CHEQUEOS.append((cid, reglas, desc, fn))
        return fn
    return deco


def R(estado, *ev):
    return estado, [str(x) for x in ev if x]


# ----------------------------------------------------------------------------------------------- chequeos
@chequeo("CE_ENTREGABLES", ["U-011", "U-048"], "carpeta de entrega completa: Take-off/*.xlsx, Planos marcados/ (PDF + PNG), "
         "README_REVIEW.md, PARA_REVISAR_EN_LA_MANANA.md, SEGUIMIENTO.md")
def ce_entregables(c):
    if not c.entrega:
        return R("FAIL", "no hay carpeta FINAL_FOR_REVIEW* (ni entrega_dir en entrega.json)")
    falta = []
    if not c.excel:
        falta.append("Take-off/*.xlsx")
    if not c.markups:
        falta.append("Planos marcados/*.pdf (markups Bluebeam)")
    if not glob.glob(os.path.join(c.planos, "*.png")):
        falta.append("Planos marcados/*.png (imagen por hoja)")
    for p in (c.readme, c.para, c.seg):
        if not os.path.isfile(p):
            falta.append(os.path.basename(p))
    return R("FAIL", *["falta " + x for x in falta]) if falta else R("PASS", f"{len(c.archivos_entrega())} archivos en {os.path.basename(c.entrega)}")


# U-145 (usuario 5-nov): "Todos los proyectos deberan ser hechos exactamente siguiendo todas las reglas de O'Reilly".
# Estructura de entrega = O'Reilly rev10 FINAL (aprobada "esta perfecto"); cada pieza la exige además su propia compuerta.
ESTANDAR_OREILLY = [
    ("Take-off/*.xlsx", "Excel fijo de 6 hojas"),
    ("Planos marcados/*markups*.pdf", "markups Bluebeam"),
    ("Planos marcados/* - IMAGE ONLY (not editable) - *.png", "imagen por hoja (U-158: '<HOJA> - IMAGE ONLY (not editable) - walls|ceilings revN.png')"),
    ("Planos marcados/DETALLES_REVISADOS.pdf", "detalles circulados (U-141)"),
    ("Planos marcados/SCHEDULES_REVISADOS.pdf", "schedules marcados (U-142)"),
    ("DETALLES_REVISADOS_INDEX.md", "índice de burbujas (U-141)"),
    ("SCHEDULES_MATERIALES.md", "lista de materiales por type (U-142)"),
    ("README_REVIEW.md", "README en inglés con hoja de datos"),
    ("PARA_REVISAR_EN_LA_MANANA.md", "notas en español"),
    ("SEGUIMIENTO.md", "RFI y pendientes"),
    ("GUIA_DE_REVISION_DEL_ESTIMADOR.md", "guía de revisión del estimador (U-148)"),
    ("Auditoria/burbujas/*", "evidencia de burbujas verificadas"),
    ("Auditoria/schedules/*", "lectura independiente del schedule (U-111)"),
]


@chequeo("CE_ESTANDAR_OREILLY", ["U-145"], "entrega con la misma estructura que O'Reilly rev10 FINAL (estándar aprobado por el usuario)")
def ce_estandar_oreilly(c):
    if not c.entrega:
        return R("FAIL", "no hay carpeta de entrega")
    falta = [f"falta {pat} ({que})" for pat, que in ESTANDAR_OREILLY if not glob.glob(os.path.join(c.entrega, pat))]
    return R("FAIL", *falta) if falta else R("PASS", f"{len(ESTANDAR_OREILLY)} piezas del estándar O'Reilly rev10 presentes")


@chequeo("CE_SIN_PROPOSAL", ["U-015"], "sin proposal en la entrega")
def ce_sin_proposal(c):
    # U-150 (usuario 5-nov, Consumer Cellular): la proposal se arma por orden del usuario y vive SOLO en Proposal/ (deja sin
    # efecto U-015 para esa carpeta); un archivo de proposal fuera de Proposal/ sigue siendo FAIL
    xs = [p for p in c.archivos_entrega() if re.search(r"(?i)proposal", os.path.relpath(p, c.entrega))
          and not os.path.relpath(p, c.entrega).split(os.sep)[0] == "Proposal"]
    return R("FAIL", *xs) if xs else R("PASS", "sin archivos de proposal fuera de Proposal/ (U-150)")


def revisar_proposal(xlsx, ms_rows, scope_rows):
    """U-150: -> lista de faltas de una proposal (vacía = OK). ms_rows [(material, net)], scope_rows [(id, scope, estado, nota)]."""
    import openpyxl
    ev = []
    wb = openpyxl.load_workbook(xlsx, data_only=False)
    if "PROPOSAL" not in wb.sheetnames:
        return ["sin hoja PROPOSAL"]
    txt = " ".join(str(c.value) for row in wb["PROPOSAL"].iter_rows() for c in row if c.value is not None)
    norm = lambda t: re.sub(r"\s+", " ", str(t)).strip().lower()
    T = norm(txt)
    if not re.search(r"\bincluded\b", T) or "included (" not in T and "included:" not in T:
        ev.append("PROPOSAL sin sección INCLUDED")
    if "not included" not in T:
        ev.append("PROPOSAL sin sección NOT INCLUDED / EXCLUSIONS")
    for m, net in ms_rows:
        if (net or 0) > 0 and norm(m) not in T:
            ev.append(f"renglón cargado del Material Summary sin INCLUDED: '{m[:70]}'")
    for r in scope_rows:
        t = " ".join(str(x or "") for x in r[1:4])
        if re.search(r"\bEXCLUDED\b", t) and not str(r[0]).startswith(("RFI", "A/B")) and                 not re.search(r"QUANTIFIED|CUANTIFICADO", str(r[2] or "")):
            n = norm(re.sub(r"\s*\(EXCLUDED[^)]*\)", "", str(r[1])))
            if n not in T:
                ev.append(f"EXCLUDED del Scope sin NOT INCLUDED: {r[0]} '{n[:60]}'")
    if "FBM_PRICES" not in wb.sheetnames:
        ev.append("sin hoja FBM_PRICES (fuente y fecha de cada precio de material)")
    else:
        f = wb["FBM_PRICES"]
        codes = set()
        for i, row in enumerate(f.iter_rows(min_row=2, values_only=True), start=2):
            if not row or not row[0]:
                continue
            codes.add(str(row[0]))
            if not isinstance(row[3], (int, float)) or not str(row[8] or "").startswith("https://myfbm.com") or not str(row[9] or "").strip():
                ev.append(f"FBM_PRICES fila {i} {row[0]}: sin precio, link myfbm.com o fecha")
        if "PRICING" in wb.sheetnames:
            for i, row in enumerate(wb["PRICING"].iter_rows(values_only=True), start=1):
                if row and len(row) > 5 and isinstance(row[5], (int, float)) and row[4] and str(row[4]) not in codes:
                    ev.append(f"PRICING fila {i}: precio de material con código {row[4]} que no está en FBM_PRICES")
    return ev


@chequeo("CE_PROPOSAL", ["U-150"], "U-150: la proposal (Proposal/) tiene INCLUDED y NOT INCLUDED, cada renglón cargado del Material "
         "Summary en INCLUDED, cada EXCLUDED del Scope en NOT INCLUDED y cada precio de material con su fuente y fecha FBM")
def ce_proposal(c):
    xs = sorted(glob.glob(os.path.join(c.entrega or "", "Proposal", "*.xlsx"))) if c.entrega else []
    if not xs:
        if c.cfg.get("proposal"):
            return R("FAIL", "entrega.json pide proposal y no hay Proposal/*.xlsx")
        return R("PASS", "sin proposal pedida (U-150 solo con orden del usuario)")
    wb = c.wb()
    if wb is None:
        return R("FAIL", "no hay Excel del take-off para cruzar la proposal")
    ms = [(str(r[0]), r[2]) for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True) if r[0] and isinstance(r[2], (int, float))]
    sc = [r for r in wb["Scope Checklist"].iter_rows(min_row=2, values_only=True) if r and r[0]]
    ev = []
    for x in xs:
        ev += [f"{os.path.basename(x)}: {e}" for e in revisar_proposal(x, ms, sc)]
    return R("FAIL", *ev[:25]) if ev else R("PASS", f"{len(xs)} proposal(s): INCLUDED / NOT INCLUDED completos y precios FBM con fuente")


@chequeo("CE_FORMATO_EXCEL", ["U-003", "U-016", "BE-43"], "Excel de formato fijo: exactamente las 6 hojas visibles en orden "
         "y los encabezados fijos de plantilla_excel.py (sin hojas ni columnas agregadas)")
def ce_formato_excel(c):
    wb = c.wb()
    if wb is None:
        return R("FAIL", "no hay Excel")
    ev, est = [], "PASS"
    vis = [ws.title for ws in wb.worksheets if ws.sheet_state == "visible"]
    ocultas = [ws.title for ws in wb.worksheets if ws.sheet_state != "visible"]
    if vis != HOJAS6:
        est = "FAIL"
        ev.append(f"hojas visibles {vis} != {HOJAS6}")
    for o in ocultas:
        if o == "_reglas":
            est = "AMBER" if est == "PASS" else est
            ev.append("hoja oculta _reglas (sello viejo; desde R80f.5 va en <excel>.sello.json)")
        else:
            est = "FAIL"
            ev.append(f"hoja oculta extra '{o}'")
    for h, (fila, cab) in CABECERAS.items():
        if h not in wb.sheetnames:
            continue
        ws = wb[h]
        real = [str(x).strip() for x in next(ws.iter_rows(min_row=fila, max_row=fila, values_only=True)) if x is not None]
        if real != cab:
            est = "FAIL"
            ev.append(f"{h} fila {fila}: encabezados {real} != {cab}")
    return R(est, *(ev or ["6 hojas + encabezados fijos OK"]))


def _ms_filas(c):
    wb = c.wb()
    if wb is None or "Material Summary" not in wb.sheetnames:
        return []
    out = []
    for i, r in enumerate(wb["Material Summary"].iter_rows(min_row=4, values_only=True), start=4):
        if not r or not r[0] or str(r[0]).upper().startswith(("SUBTOTAL", "TOTAL")):
            continue
        net = r[2] if len(r) > 2 else None
        out.append({"fila": i, "material": str(r[0]), "net": net if isinstance(net, (int, float)) else None,
                    "fuente": str(r[8] or "") if len(r) > 8 else ""})
    return out


@chequeo("CE_TORNILLERIA", ["U-053"], "toda la tornillería (screws, anchors, Titen, pins/PAF, Tapcon, bolts) = 0 con EXCLUDED "
         "en Material Summary y una línea EXCLUDED en Scope Checklist")
def ce_tornilleria(c):
    fs = [f for f in _ms_filas(c) if RX_FASTENER.search(f["material"]) and not re.search(r"(?i)\bclips?\b|angle", f["material"])]
    malos = [f"fila {f['fila']} '{f['material'][:60]}' net {f['net']}" + ("" if "EXCLUDED" in f["fuente"].upper() else " sin EXCLUDED")
             for f in fs if (f["net"] or 0) != 0 or "EXCLUDED" not in f["fuente"].upper()]
    wb = c.wb()
    sc = " ".join(" ".join(str(x or "") for x in r) for r in wb["Scope Checklist"].iter_rows(values_only=True)) \
        if wb is not None and "Scope Checklist" in wb.sheetnames else ""
    if not re.search(r"(?i)(screw|fastener|anchor|tornill)[^|]{0,200}EXCLUDED|EXCLUDED[^|]{0,200}(screw|fastener|anchor)", sc):
        malos.append("Scope Checklist sin la línea EXCLUDED de tornillería")
    return R("FAIL", *malos) if malos else R("PASS", f"{len(fs)} renglones de tornillería en 0 con EXCLUDED")


@chequeo("CE_TRACK_FAMILIAS", ["U-056", "BE-24"], "dos familias de track en renglones separados: estándar (bottom / top) y "
         "slip / deflection; ningún renglón las mezcla; si no hay slip track, Scope Checklist lo declara NOT APPLICABLE")
def ce_track_familias(c):
    fs = [f for f in _ms_filas(c) if RX_TRACK.search(f["material"])]
    est = [f for f in fs if re.search(r"(?i)bottom|top", f["material"]) and not RX_SLIP.search(f["material"])]
    slip = [f for f in fs if RX_SLIP.search(f["material"])]
    mezcla = [f for f in slip if re.search(r"(?i)bottom|standard|top and bottom|&", f["material"])]
    ev = []
    if not est:
        ev.append("sin renglón de track estándar (bottom / top)")
    if mezcla:
        ev += [f"fila {f['fila']} mezcla familias: '{f['material'][:70]}'" for f in mezcla]
    if not [f for f in slip if (f["net"] or 0) > 0]:
        wb = c.wb()
        sc = " ".join(" ".join(str(x or "") for x in r) for r in wb["Scope Checklist"].iter_rows(values_only=True)) if wb else ""
        if not re.search(r"(?i)(slip|deflection)[^|]{0,160}(NOT APPLICABLE|no wall reaches|none reach)", sc):
            ev.append("sin renglón de slip / deflection track > 0 y sin NOT APPLICABLE en Scope Checklist")
    return R("FAIL", *ev) if ev else R("PASS", f"{len(est)} renglones estándar / {len(slip)} slip-deflection, separados")


@chequeo("CE_FUENTES_MS", ["U-025", "BE-40"], "todo renglón del Material Summary con cantidad cita su fuente (N/SHEET, "
         "sección de spec o código del trade)")
def ce_fuentes_ms(c):
    rx = re.compile(r"N/SHEET|[A-Z]{1,3}-?\d{1,3}(?:\.\d{1,2})?\b|\b0[5-9]\s?\d{2}\s?\d{2}\b|ASTM|GA-\d|AISI|UL\b|IBC|SSMA|USG")
    malos = [f"fila {f['fila']} '{f['material'][:60]}'" for f in _ms_filas(c) if (f["net"] or 0) > 0 and not rx.search(f["fuente"])]
    if not _ms_filas(c):
        return R("FAIL", "Material Summary vacío o sin Excel")
    return R("FAIL", *malos) if malos else R("PASS", "todos los renglones con fuente")


def sf_proyecto_fallas(tk):
    """U-170 (usuario 11-nov: 'en los proximos proyectos tambien dime los pies cuadrados del proyecto'): proyecto_datos trae el SF del
    proyecto con número en SF y su HOJA (o BuildingConnected); si es [PENDIENTE], con el barrido anotado (hojas revisadas). -> [fallas]"""
    pd = (tk or {}).get("proyecto_datos") or []
    x = next((x for x in pd if re.search(r"\bsf\b|square f|\barea\b", str(x.get("campo", "")), re.I)), None)
    if not x:
        return ["proyecto_datos sin el campo de SF del proyecto (U-170: 'total building area SF' con su hoja)"]
    v, f = str(x.get("valor") or ""), str(x.get("fuente") or "")
    if "PENDIENTE" in v.upper() or "PENDING" in v.upper():
        if not (re.search(r"(?i)barrid|swept|searched|sweep|revis", v + " " + f) and RX_HOJA_CONCRETA.search(v + " " + f)):
            return [f"SF del proyecto [PENDIENTE] sin el barrido anotado (qué hojas se revisaron, U-170 / U-155): '{v[:80]}'"]
        return []
    ev = []
    if not re.search(r"\d[\d,]*(?:\.\d+)?\s*(?:SF|sq\.?\s*ft|square feet)\b", v, re.I):
        ev.append(f"SF del proyecto sin número en SF: '{v[:80]}' (U-170)")
    if not (RX_HOJA_CONCRETA.search(f + " " + v) or re.search(r"(?i)buildingconnected", f + " " + v)):
        ev.append(f"SF del proyecto sin hoja (N/HOJA / HOJA o BuildingConnected): fuente '{f[:80]}' (U-170)")
    return ev


@chequeo("CE_DATOS_PROYECTO", ["U-077", "R-ALC-09", "BE-114", "U-170"], "hoja de datos del proyecto + hojas obligatorias en takeoff.json, "
         "Inputs del Excel, README_REVIEW y PARA_REVISAR (reglas.datos_proyecto_fallas); U-170: SF del proyecto con número y su hoja, "
         "o [PENDIENTE] con el barrido anotado")
def ce_datos_proyecto(c):
    import reglas
    if not c.tk:
        return R("FAIL", "no hay takeoff.json con proyecto_datos / hojas_revisadas")
    fs = reglas.datos_proyecto_fallas(c.tk, c.excel, [c.readme, c.para])
    fs += [("proyecto_datos", x, "U-170") for x in sf_proyecto_fallas(c.tk)]
    for p in (c.readme, c.para):
        if not os.path.isfile(p):
            fs.append((os.path.basename(p), "no existe", "doc con PROJECT DATA arriba"))
    return R("FAIL", *[" · ".join(map(str, f)) for f in fs]) if fs else R("PASS", "datos del proyecto en las 4 fuentes")


def _pasos_tiempos(txt):
    """{paso: [horas]} de las filas '| 2-3 | ... | 20:33 | 20:53 |' de TIEMPOS.md."""
    out = {}
    for ln in txt.splitlines():
        cs = [x.strip(" *") for x in ln.strip().strip("|").split("|")]
        if len(cs) < 3:
            continue
        m = re.match(r"^(\d{1,2})(?:[a-z])?(?:\s*[-–]\s*(\d{1,2}))?[a-z]?$", cs[0])
        if not m:
            continue
        horas = re.findall(r"\b\d{1,2}:\d{2}\b", " ".join(cs[1:]))
        a, b = int(m.group(1)), int(m.group(2) or m.group(1))
        for k in range(a, b + 1):
            out.setdefault(k, []).extend(horas)
    return out


def tiempos_fallas(txt, anio=2026):
    """U-094 (CR City Hotel 11-nov: filas de rev15-rev17 en UTC con etiqueta PST, encimadas; TOTAL viejo de 2409 min): cada fila con
    inicio y fin 'MM-DD HH:MM' (o 'AAAA-MM-DD HH:MM') -> fin > inicio, Duración = fin - inicio, ninguna fila se encima con otra, y
    el TOTAL (Duración '<N> min') = suma de las filas. -> [fallas]"""
    import datetime as _dt
    rx = re.compile(r"(?:(\d{4})-)?(\d{1,2})-(\d{1,2})\s+(\d{1,2}):(\d{2})")
    filas, total, ev = [], None, []
    for ln in txt.splitlines():
        cs = [x.strip(" *") for x in ln.strip().strip("|").split("|")]
        if len(cs) < 5:
            continue
        if re.match(r"(?i)TOTAL\b", cs[0]):
            m = re.search(r"(\d[\d,]*)\s*min", cs[4])
            total = int(m.group(1).replace(",", "")) if m else None
            continue
        a, b = rx.search(cs[2]), rx.search(cs[3])
        if not a or not b:
            continue
        f = lambda m: _dt.datetime(int(m.group(1) or anio), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)))   # noqa: E731
        i, j = f(a), f(b)
        d = re.search(r"(\d[\d,]*)\s*min", cs[4])
        dur = int(d.group(1).replace(",", "")) if d else None
        filas.append((cs[0], i, j, dur))
        if j <= i:
            ev.append(f"fila {cs[0]}: fin {cs[3]} no es posterior al inicio {cs[2]}")
        elif dur is not None and abs((j - i).total_seconds() / 60 - dur) > 1:
            ev.append(f"fila {cs[0]}: Duración {dur} min != fin - inicio {int((j - i).total_seconds() // 60)} min")
    orden = sorted(filas, key=lambda x: x[1])
    for p, q in zip(orden, orden[1:]):
        if q[1] < p[2]:
            ev.append(f"filas encimadas: {p[0]} termina {p[2]:%m-%d %H:%M} y {q[0]} empieza {q[1]:%m-%d %H:%M} (¿hora UTC con etiqueta PST?)")
    suma = sum(x[3] or 0 for x in filas)
    if filas and total is None:
        ev.append("fila TOTAL sin '<N> min' en Duración")
    elif filas and abs(total - suma) > 1:
        ev.append(f"TOTAL {total} min != suma de las filas {suma} min")
    return ev


@chequeo("CE_TIEMPOS", ["U-094"], "TIEMPOS.md con hora de inicio / fin (hora de California) de cada paso 1–9 y TOTAL; ninguna fila "
         "encimada con otra, Duración = fin - inicio y TOTAL = suma de las filas (CR City Hotel 11-nov)")
def ce_tiempos(c):
    t = _leer(c.tiempos)
    if not t:
        return R("FAIL", "no existe TIEMPOS.md en la carpeta del proyecto (cache_proyectos/<proyecto>/TIEMPOS.md)")
    p = _pasos_tiempos(t)
    falta = [k for k in PASOS_TIEMPOS if not p.get(k)]
    ev = [f"paso {k} sin fila con hora" for k in falta]
    if not re.search(r"(?i)\bTOTAL\b", t):
        ev.append("sin fila TOTAL")
    if not re.search(r"(?i)\bPST\b|\bPDT\b|california|los_angeles", t):
        ev.append("sin zona horaria de California (PST/PDT)")
    ev += tiempos_fallas(t)
    return R("FAIL", *ev) if ev else R("PASS", f"pasos 1–9 con hora, sin filas encimadas, TOTAL = suma; {os.path.relpath(c.tiempos, c.w)}")


@chequeo("CE_HORAS_CALIFORNIA", ["U-045"], "horas al usuario en hora de California: sin UTC en TIEMPOS / README / PARA_REVISAR")
def ce_horas(c):
    ev = []
    for p in (c.tiempos, c.readme, c.para):
        t = _leer(p)
        for m in re.finditer(r"\bUTC\b|\d{2}:\d{2}(?::\d{2})?Z\b|\bGMT\b", t):
            ev.append(f"{os.path.basename(p)}: '{t[max(0, m.start() - 30):m.end() + 10]}'")
    return R("FAIL", *ev[:10]) if ev else R("PASS", "sin horas en UTC")


RX_DOLAR = re.compile(r"\$\s?\d|\bUSD\b|\b\d[\d,.]*\s?(?:dollars|d[oó]lares)\b", re.I)


@chequeo("CE_SIN_DOLARES", ["U-018", "U-123"], "sin costos en dólares en lo entregado: README / PARA_REVISAR / SEGUIMIENTO, "
         "celdas visibles del Excel (no fórmulas) y texto de los markups (U-123, preferencias del día 1)")
def ce_sin_dolares(c):
    ev = []
    for p in (c.readme, c.para, c.seg):
        t = _leer(p)
        for m in RX_DOLAR.finditer(t):
            ev.append(f"{os.path.basename(p)}: '{t[max(0, m.start() - 30):m.end() + 15]}'")
    wb = c.wb()
    for ws in (wb.worksheets if wb is not None else []):
        if ws.sheet_state != "visible":
            continue
        for row in ws.iter_rows():
            for cell in row:
                v = cell.value
                if isinstance(v, str) and not v.startswith("=") and RX_DOLAR.search(v):
                    ev.append(f"{ws.title}!{cell.coordinate}: '{v[:60]}'")
                elif cell.number_format and "$" in str(cell.number_format) and isinstance(v, (int, float)):
                    ev.append(f"{ws.title}!{cell.coordinate}: formato de moneda '{cell.number_format}'")
    if c.markups and os.path.isfile(c.markups):
        import pymupdf
        for pg in pymupdf.open(c.markups):
            for a in pg.annots() or []:
                t = (a.info or {}).get("content") or ""
                if RX_DOLAR.search(t):
                    ev.append(f"markup {pg.get_label() or pg.number + 1}: '{t[:60]}'")
    return R("FAIL", *ev[:10]) if ev else R("PASS", "sin montos en dólares")


@chequeo("CE_DRIVE_PARENT", ["U-090", "U-004", "U-001"], "la carpeta del proyecto en Drive cuelga de Claude outputs de la RAÍZ "
         f"({DRIVE_RAIZ}); nunca de Projects › Claude outputs")
def ce_drive_parent(c):
    d = c.cfg.get("drive") or {}
    pid, nombre = str(d.get("parent_id") or ""), str(d.get("carpeta_proyecto") or "")
    if not pid:
        return R("FAIL", "entrega.json sin drive.parent_id (no se puede verificar el folder de entrega)")
    if pid == DRIVE_PROHIBIDO:
        return R("FAIL", f"parent_id {pid} = Projects › Claude outputs (PROHIBIDO)")
    if pid != DRIVE_RAIZ:
        return R("FAIL", f"parent_id {pid} != {DRIVE_RAIZ} (Claude outputs de la raíz)")
    if not nombre.strip():
        return R("FAIL", "entrega.json sin drive.carpeta_proyecto (un folder por proyecto, nombre = proyecto)")
    return R("PASS", f"parent {pid} › '{nombre}' (subir_entrega.py lo verifica en vivo con gdrive_fetch list)")


def _rfi_texto(c, rid, fila):
    r = c.rfi(rid) or {}
    return fila + " " + json.dumps(r, ensure_ascii=False)


RX_NO_IMPRESO = re.compile(r"(?i)\bnot printed\b|\bassum(?:ed|ption)\b|\[PENDING\]|\[PENDIENTE\]")
RX_DECISION_CITADA = re.compile(r"(?i)(?:estimator(?:'s)? decision|decisi[oó]n del estimador)[^|;]{0,40}(?:20\d\d-\d\d-\d\d|\b\d{1,2}-(?:oct|nov|dec)\b)|"
                                r"R-ALC-\d+|\bU-\d{3}\b|standing (?:rule|order)|recommended option")


def no_impreso_sin_rfi(c):
    """U-138 (auditoría 4-nov): todo 'not printed' / 'assumed' / [PENDING] del Excel remite a un RFI ABIERTO de Pending Items
    (con su delta) o a un RFI cerrado con su decisión escrita, o cita la decisión / regla que lo resuelve. Antes CE_RFI_FORMATO
    y CE_RFI_BARRIDO_IMPRESO pasaban en vacío con 0 RFI abiertos aunque el Excel dijera 'not printed - assumed, RFI-xx'."""
    wb = c.wb()
    if wb is None:
        return ["no hay Excel"]
    abiertos = {rid for rid, _ in c.rfis_abiertos()}
    cerr = {str(r.get("id")) for r in c.rfis() if RX_CERRADO.search(str(r.get("estado") or r.get("status") or ""))
            and (r.get("decision") or r.get("decisión") or r.get("motivo"))}
    for ws in wb.worksheets:
        if ws.title != "Pending Items":
            for row in ws.iter_rows(values_only=True):
                t = " ".join(str(x) for x in row if x)
                if re.search(r"(?i)\bCLOSED\b", t):
                    cerr |= set(re.findall(r"\bRFI-\d+\b", t[:40]))
    ev = []
    for ws in wb.worksheets:
        if ws.title == "Pending Items":
            continue
        for row in ws.iter_rows():
            for cell in row:
                v = cell.value
                if not isinstance(v, str) or not RX_NO_IMPRESO.search(v):
                    continue
                ids = set(re.findall(r"\bRFI-\d+\b", v))
                malos = sorted(i for i in ids if i not in abiertos and i not in cerr)
                if malos:
                    ev.append(f"{ws.title}!{cell.coordinate}: cita {', '.join(malos)} que no está abierto en Pending Items ni cerrado con su decisión")
                elif not ids and not RX_DECISION_CITADA.search(v):
                    ev.append(f"{ws.title}!{cell.coordinate}: '{' '.join(v.split())[:90]}' sin RFI abierto ni decisión citada")
    return ev


@chequeo("CE_RFI_FORMATO", ["U-042", "U-048", "U-052"], "cada RFI abierto: (A) planos con N/HOJA y delta · (B) código con "
         "cita y delta · (C) otro, en ese orden, y el valor conservador CARGADO declarado")
def ce_rfi_formato(c):
    ev = []
    for rid, fila in c.rfis_abiertos():
        ia, ib, ic = (fila.find(x) for x in ("(A)", "(B)", "(C)"))
        if min(ia, ib, ic) < 0 or not ia < ib < ic:
            ev.append(f"{rid}: opciones (A)/(B)/(C) faltan o fuera de orden")
        if len(re.findall(r"(?i)delta", fila)) < 2:
            ev.append(f"{rid}: delta en (A) y (B)")
        if not re.search(r"(?i)loaded|carried|cargad", _rfi_texto(c, rid, fila)):
            ev.append(f"{rid}: sin valor conservador cargado declarado (loaded / carried)")
    np_ = no_impreso_sin_rfi(c)
    ev += np_[:20]
    return R("FAIL", *ev) if ev else R("PASS", f"{len(c.rfis_abiertos())} RFI abiertos con A/B/C + delta + valor cargado; "
                                               "todo 'not printed / assumed' del Excel remite a un RFI o a su decisión")


@chequeo("CE_RFI_PROHIBIDOS", ["U-053", "U-061", "U-064", "U-071", "U-075", "R-ALC-01", "R-ALC-03", "R-ALC-05", "R-ALC-07"],
         "ningún RFI abierto sobre lo que el usuario ordenó resolver sin RFI (tornillería, trades ajenos, ductos, cielo "
         "existente sin tipo, altura de partition a demoler)")
def ce_rfi_prohibidos(c):
    ev = []
    for rid, fila in c.rfis_abiertos():
        r = c.rfi(rid) or {}
        tema = str(r.get("pregunta") or fila)
        tema = re.split(r"(?<=[a-z0-9\)\"])\.\s|\s\|\s|:\s", tema, maxsplit=1)[0][:300]   # el tema = antes del 1er '. ' / ' | ' / ': '
        for nombre, rx in RFI_PROHIBIDOS:
            m = rx.search(tema)
            if m and m.start() <= 80 and not re.search(r"(?i)\b(?:no|not|without|sin)\b[^,;]{0,12}$", tema[:m.start()]):
                ev.append(f"{rid}: {nombre} — '{tema[max(0, m.start() - 40):m.end() + 40]}'")
    return R("FAIL", *ev) if ev else R("PASS", "ningún RFI sobre temas con orden fija")


# rev10 (CR City Hotel, auditoría U-138 E1 / E2): sinónimos del barrido y FRASES DE RESPUESTA. Un RFI de cielo / membrana barre
# también DROPPED / SUSPENDED / NOT A COMPONENT ...; junto a un término del RFI, una frase de respuesta impresa (nota 'NOT A COMPONENT OF
# THE RATED ASSEMBLY', rating de puerta 'NN MIN' en su renglón del door schedule) = FAIL salvo descarte que cite esa misma frase.
SINONIMOS_CIELO = ["DROPPED", "DROP", "SUSPENDED", "NOT A COMPONENT", "RATED ASSEMBLY", "MEMBRANE", "CEILING PLANS AND DETAILS"]
RX_TEMA_CIELO = re.compile(r"(?i)ceiling|\bclg\b|gyp-\d|\b[fr]s-\d|membrane|throughout")
FRASES_RESPUESTA = [re.compile(r"(?i)NOT\s+A\s+COMPONENT\s+OF\s+THE\s+RATED\s+ASSEMBLY"),
                    re.compile(r"(?i)(?<![\w.])\d{2,3}\s*MIN\.?(?![\w])")]
RX_CORTE_RENGLON = re.compile(r"(?<![\w.])\d{3}\.\d{1,2}(?![\w.])")     # número de puerta = otro renglón del schedule


def respuestas_cerca(t, txt, ancho=300):
    """frases de respuesta impresas junto a cada aparición de t (mismo renglón del schedule: se corta en el número de puerta vecino)."""
    out = []
    rx = re.compile(r"(?<![A-Za-z0-9])" + re.escape(t) + r"(?![A-Za-z0-9])", re.I)
    for m in rx.finditer(txt):
        a, b = txt[max(0, m.start() - ancho):m.start()], txt[m.end():m.end() + ancho]
        cb = list(RX_CORTE_RENGLON.finditer(b))
        b = b[:cb[0].start()] if cb else b
        ca = list(RX_CORTE_RENGLON.finditer(a))
        a = a[ca[-1].start():] if ca else a
        for fr in FRASES_RESPUESTA:
            for w in (a, b):
                f = fr.search(w)
                if f and (fr is FRASES_RESPUESTA[0] or w is b):
                    out.append(" ".join(f.group(0).split()))
    return sorted(set(out))


def _terminos(r):
    b = r.get("barrido") if isinstance(r.get("barrido"), dict) else {}
    ts = [str(t) for t in (b.get("terminos") or []) if str(t).strip()]
    if any(RX_TEMA_CIELO.search(t) for t in ts + [str(r.get("pregunta") or "")]):
        ts += SINONIMOS_CIELO
    for q in re.findall(r"'([^']{4,40})'|\"([^\"]{4,40})\"", str(r.get("pregunta") or "")):
        q = (q[0] or q[1]).strip()
        if q.upper() == q and re.search(r"[A-Z]{2}", q) and not RX_FT.fullmatch(q):
            ts.append(q)
    return sorted(set(ts), key=str.lower)


def barrido_impreso(rid, r, hojas_txt):
    """BE-120: -> lista de fallas. (1) un término del RFI aparece en una hoja que NO está en su barrido.hojas;
    (2) un término aparece junto a un valor IMPRESO (cota ft-in / EL.) en una hoja y el RFI no registra por qué esa hoja
    no lo contesta (barrido.descartes {hoja: motivo}) — posible respuesta impresa."""
    b = r.get("barrido") if isinstance(r.get("barrido"), dict) else {}
    hojas = b.get("hojas")
    todas = hojas == "ALL"
    lista = set(hojas or []) if isinstance(hojas, list) else set()
    desc = b.get("descartes") if isinstance(b.get("descartes"), dict) else {}
    out = []
    ts = _terminos(r)
    if not ts:
        return [f"{rid}: sin términos de barrido (barrido.terminos)"]
    for hoja, txt in sorted(hojas_txt.items()):
        for t in ts:
            rx = re.compile(r"(?<![A-Za-z0-9])" + re.escape(t) + r"(?![A-Za-z0-9])", re.I)
            ms = list(rx.finditer(txt))
            if not ms:
                continue
            if not todas and hoja not in lista:
                out.append(f"{rid}: '{t}' aparece {len(ms)} vez/veces en {hoja}, que NO está en su barrido.hojas")
                break
            fr_ = [f for f in respuestas_cerca(t, txt) if f.lower() not in str(desc.get(hoja) or "").lower()]
            if fr_:
                out.append(f"{rid}: posible RESPUESTA impresa en {hoja} junto a '{t}': '{fr_[0]}' — se aplica con N/HOJA o el descarte "
                           f"de {hoja} cita esa frase y explica por qué no contesta")
                break
            con_valor = [txt[max(0, m.start() - 40):m.end() + 60] for m in ms if RX_FT.search(txt[max(0, m.start() - 40):m.end() + 60])]
            if con_valor and not str(desc.get(hoja) or "").strip():
                out.append(f"{rid}: posible respuesta IMPRESA en {hoja}: '{' '.join(con_valor[0].split())}' — se aplica "
                           f"con N/HOJA o se registra en barrido.descartes['{hoja}'] por qué no contesta")
                break
    return out


@chequeo("CE_RFI_BARRIDO_IMPRESO", ["U-100", "U-086", "U-052", "BE-120", "BE-CF16", "U-019"], "BE-120: por cada RFI abierto se "
         "buscan sus términos en el TEXTO COMPLETO del set (incl. SHX); falla si aparecen en una hoja fuera de su barrido o "
         "junto a un valor impreso sin descarte escrito")
def ce_rfi_barrido(c):
    abiertos = c.rfis_abiertos()
    if not abiertos:
        np_ = no_impreso_sin_rfi(c)       # U-138: 0 RFI abiertos no es PASS si el Excel tiene supuestos sin RFI
        return R("FAIL", *np_[:20]) if np_ else R("PASS", "0 RFI abiertos y ningún 'not printed / assumed' sin RFI o decisión")
    st = _json(c.set_p)
    hojas_txt = (st or {}).get("hojas") if isinstance(st, dict) else None
    if not hojas_txt:
        return R("FAIL", "no hay set_texto.json (texto completo del set): correr `compuerta_entrega.py texto <bidset.pdf> "
                         "--out <workdir>/set_texto.json`; sin él no se puede probar que la respuesta no está impresa")
    ev = []
    sin = (st or {}).get("sin_texto") or []
    if sin:                                    # R80e.151: barrido ciego en hojas raster sin OCR
        ev.append(f"{len(sin)} hojas sin texto (raster sin OCR): {', '.join(sin[:12])} — instalar tesseract y repetir `texto`")
    for rid, _ in abiertos:
        r = c.rfi(rid)
        if not r:
            ev.append(f"{rid}: sin registro en takeoff.json (barrido no documentado)")
            continue
        ev += barrido_impreso(rid, r, hojas_txt)
    return R("FAIL", *ev) if ev else R("PASS", f"{len(abiertos)} RFI: ningún término en hojas sin barrer ni junto a valores impresos sin descarte")


# CR-R13 (auditoría COORDINACIÓN 9-nov): sinónimos de 'no impreso' (RFI-04 'no partition tag', RFI-13 'does not give', RFI-17 'not labeled')
RX_NO_IMPRESO_RFI = re.compile(r"(?i)\bnot (?:printed|shown|dimensioned|indicated|located|labell?ed|given|stated|specified|tagged|drawn|detailed)\b|"
                               r"\bdoes not (?:give|show|state|specify|indicate|say)\b|\bno (?:partition )?tag\b|\buntagged\b|\bwithout (?:a )?tag\b|"
                               r"\bno impres|\bno (?:se )?muestra|\bsin tag\b")


def busqueda_exhaustiva(rid, r, disciplinas_set):
    """U-140 (usuario 5-nov, CFA rev9): un RFI 'not printed' solo se presenta tras buscarlo HASTA ENCONTRARLO: barrido con
    >= 12 términos (elemento + sinónimos), todas las disciplinas del set, texto SHX, geometría vectorial medida a la escala
    impresa, specs / addenda y los sets de todos los GC. Falta algo = falla (CFA rev9 RFI-11 / 12 / 20: '8 terms')."""
    b = r.get("barrido") if isinstance(r.get("barrido"), dict) else {}
    out = []
    ts = [t for t in (b.get("terminos") or []) if str(t).strip()]
    if len(ts) < 12:
        out.append(f"{rid}: barrido de {len(ts)} términos (U-140: >= 12, con sinónimos del elemento)")
    dis = b.get("disciplinas")
    if dis != "ALL":
        falt = sorted(set(disciplinas_set) - {str(x).upper() for x in (dis or [])})
        if falt:
            out.append(f"{rid}: disciplinas sin barrer {falt} (U-140: todas, G/A/S/M/P/E/FP/F/K/vendor)")
    for k, q in (("shx", "texto SHX"), ("vectorial", "geometría vectorial medida a la escala impresa (o 'raster: ...')"),
                 ("specs", "specs / addenda"), ("otros_sets", "sets de todos los GC / existing / survey")):
        if not str(b.get(k) or "").strip():
            out.append(f"{rid}: barrido.{k} vacío ({q})")
    return out


def nombres_planos(nombres):
    """U-158 (usuario 10-nov, CR City Hotel: abrió 'A3.02_rcp_markups.png' creyendo que eran los markups editables): en Planos marcados/
    cada nombre dice QUÉ ES. PNG sin 'IMAGE ONLY (not editable)' o con 'markups' / 'marked_by_type' / 'pNN_' = FAIL; PDF de markups (no
    DETALLES / SCHEDULES) sin el nombre U-165 '<PROY>_markups_revN - OPEN IN BLUEBEAM.pdf' = FAIL; dos PNG de la misma hoja con el mismo contenido = FAIL. -> [fallas]"""
    ev, vistos = [], {}
    for n in nombres:
        b = os.path.basename(n)
        if b.lower().endswith(".png"):
            if "IMAGE ONLY (not editable)" not in b or re.search(r"(?i)markups|marked_by_type", b) or re.match(r"(?i)p\d+[_ ]", b):
                ev.append(f"{b}: PNG sin 'IMAGE ONLY (not editable)' o con 'markups' / 'marked_by_type' / 'pNN' (U-158)")
            m = re.match(r"(.+?) - IMAGE ONLY \(not editable\) - (walls and ceilings|walls|ceilings) ", b)
            if m:
                if m.group(1) in vistos and vistos[m.group(1)] == m.group(2):
                    ev.append(f"{b}: duplicado de la hoja {m.group(1)} (U-158)")
                vistos[m.group(1)] = m.group(2)
            elif "IMAGE ONLY" in b:
                ev.append(f"{b}: falta ' - walls|ceilings|walls and ceilings revN' (U-158)")
        elif b.lower().endswith(".pdf") and not b.startswith(("DETALLES_REVISADOS", "SCHEDULES_REVISADOS", "ALTURAS_REVISADAS")) and not re.fullmatch(MARKUPS_RE, b):
            ev.append(f"{b}: PDF de markups sin el nombre '<PROY>_markups_revN - OPEN IN BLUEBEAM.pdf' (U-165, reemplaza U-158)")
    return ev


# U-165 / BE-155 (usuario 11-nov, CR City Hotel rev18: 'CR_City_Hotel_markups_rev18 - OPEN THIS IN BLUEBEAM (walls + ceilings, editable), este no
# quiere habrir'): la ruta en Windows medía 264 caracteres y Windows / Bluebeam no abren rutas de más de 260. Margen: 230.
MARKUPS_RE = r"(?<!\w)[A-Z][A-Za-z0-9]{1,5}_markups_rev\d+[a-z]? - OPEN IN BLUEBEAM\.pdf"
RAIZ_WINDOWS = "G:\\Shared drives\\JC HUNTER PROJECTS\\Claude outputs"
MAX_RUTA_WINDOWS = 230


UMBRAL_AUDITORIA_ZIP = 1000     # subir_entrega.empaquetar_auditoria: con más archivos, Auditoria/ se sube como UN Auditoria.zip
MAX_NOMBRE_EN_ZIP = 120         # COORDINACIÓN 11-nov: nombre dentro de Auditoria.zip <= 120 caracteres
CARACTERES_PROHIBIDOS_WINDOWS = '<>:"/\\|?*'
CARPETA_REV_RE = r"rev\d+ FINAL PARA REVISAR"      # U-089 / U-165 (COORDINACIÓN 11-nov): nombre corto de la carpeta de entrega


def rutas_drive(rels, umbral=UMBRAL_AUDITORIA_ZIP):
    """Rutas tal como quedan en Drive (U-165, COORDINACIÓN 11-nov): con > umbral archivos lo de Auditoria/ es un solo Auditoria.zip.
    -> (rutas en Drive, nombres dentro de Auditoria.zip)"""
    rels = sorted(rels)
    if len(rels) <= umbral:
        return rels, []
    aud = [r for r in rels if re.split(r"[\\/]", r)[0] == "Auditoria"]
    if not aud:
        return rels, []
    return [r for r in rels if r not in set(aud)] + ["Auditoria.zip"], aud


def rutas_entrega_fallas(carpeta_proyecto, carpeta_rev, rels, umbral=UMBRAL_AUDITORIA_ZIP):
    """U-165: ruta Windows de cada archivo en Drive <= 230; nombre dentro de Auditoria.zip <= 120. -> [fallas]"""
    drive, zipn = rutas_drive(rels, umbral)
    ev = rutas_windows_fallas(carpeta_proyecto, carpeta_rev, drive)
    ev += [f"nombre dentro de Auditoria.zip de {len(n)} caracteres > {MAX_NOMBRE_EN_ZIP} (U-165): {n}" for n in zipn if len(n) > MAX_NOMBRE_EN_ZIP]
    return ev


def carpeta_rev_fallas(carpeta_rev):
    """U-089 / U-165: desde rev19 la carpeta de entrega es 'revN FINAL PARA REVISAR'; el formato largo 'revN FINAL — ESTA ES ...' = FAIL."""
    if re.match(r"rev\d+ FINAL\b", carpeta_rev or "") and not re.fullmatch(CARPETA_REV_RE, carpeta_rev):
        return [f"carpeta de entrega '{carpeta_rev}': usar 'revN FINAL PARA REVISAR' (U-089 / U-165)"]
    return []


def nombres_prohibidos_fallas(componentes):
    """U-166 punto 3: ningún nombre de carpeta o archivo lleva < > : " / \\ | ? * ni caracteres de control. -> [fallas]"""
    ev = []
    for n in componentes:
        if not n:
            continue
        malos = sorted({ch for ch in n if ch in CARACTERES_PROHIBIDOS_WINDOWS or ord(ch) < 32})
        if malos or n.endswith((" ", ".")):
            ev.append(f"nombre que Windows no acepta {malos or ['espacio / punto final']}: {n} (U-166)")
    return ev


def excel_errores_fallas(xlsx):
    """U-166 punto 4: el Excel abre; ninguna celda con #REF! / #VALUE! / #DIV/0! (valor guardado o fórmula) ni fórmula sin valor. -> [fallas]"""
    import openpyxl
    try:
        f = openpyxl.load_workbook(xlsx, data_only=False)
        v = openpyxl.load_workbook(xlsx, data_only=True)
    except Exception as e:                                              # noqa: BLE001
        return [f"{os.path.basename(xlsx)} no abre: {type(e).__name__}: {e} (U-166)"]
    ev = []
    for ws in f.worksheets:
        wv = v[ws.title]
        for row in ws.iter_rows():
            for cel in row:
                x = cel.value
                y = wv[cel.coordinate].value
                if any(isinstance(z, str) and re.search(r"#(REF!|VALUE!|DIV/0!)", z) for z in (x, y)):
                    ev.append(f"{ws.title}!{cel.coordinate}: {y if isinstance(y, str) and '#' in y else x} (U-166)")
                elif isinstance(x, str) and x.startswith("=") and y is None:
                    ev.append(f"{ws.title}!{cel.coordinate}: fórmula sin valor calculado (U-166)")
    return ev


def pdf_abre_fallas(pdf):
    """U-166 punto 2: el PDF abre sin contraseña, sin firmas digitales, con Page Labels y /VP (pdf_editable). -> [fallas]"""
    import fitz
    try:
        d = fitz.open(pdf)
    except Exception as e:                                              # noqa: BLE001
        return [f"{os.path.basename(pdf)} no abre: {type(e).__name__}: {e} (U-166)"]
    ev = []
    if d.needs_pass or d.is_encrypted:
        ev.append(f"{os.path.basename(pdf)}: pide contraseña / está cifrado (U-166)")
    try:
        fs, _ = pdf_editable(pdf, [])
        ev += [f"{os.path.basename(pdf)}: {x} (U-166)" for x in fs]      # firmas, Page Labels y /VP (pdf_editable, U-151 / U-152)
    except Exception as e:                                              # noqa: BLE001
        ev.append(f"{os.path.basename(pdf)}: no se pudo revisar firmas: {e} (U-166)")
    return ev


def nombre_markups(proy, rev):
    """U-165: nombre único del PDF editable de markups, PROY corto (ej. 'CR'), rev = 'rev19' o 19."""
    rev = str(rev) if str(rev).startswith("rev") else f"rev{rev}"
    return f"{proy}_markups_{rev} - OPEN IN BLUEBEAM.pdf"


def ruta_windows(carpeta_proyecto, carpeta_rev, rel):
    """Ruta que ve el usuario en Windows: G:\\Shared drives\\JC HUNTER PROJECTS\\Claude outputs\\<proyecto>\\<revN ...>\\<subcarpeta>\\<archivo>."""
    return "\\".join([RAIZ_WINDOWS, carpeta_proyecto, carpeta_rev] + [x for x in re.split(r"[\\/]", rel) if x])


def rutas_windows_fallas(carpeta_proyecto, carpeta_rev, rels, limite=MAX_RUTA_WINDOWS):
    """U-165: toda ruta Windows simulada de la entrega > limite caracteres = FAIL (Windows / Bluebeam no abren > 260). -> [fallas]"""
    if not carpeta_proyecto:
        return ["entrega.json sin drive.carpeta_proyecto: no se puede medir la ruta Windows (U-165)"]
    ev = []
    for r in rels:
        p = ruta_windows(carpeta_proyecto, carpeta_rev, r)
        if len(p) > limite:
            ev.append(f"ruta Windows de {len(p)} caracteres > {limite} (U-165): {r}")
    return ev


@chequeo("CE_NOMBRES_ENTREGA", ["U-158", "U-164", "U-165"], "U-165: en Planos marcados/ el PDF de markups se llama '<PROY>_markups_revN - OPEN IN BLUEBEAM.pdf' "
         "(PROY corto) y toda ruta Windows simulada (G:\\Shared drives\\JC HUNTER PROJECTS\\Claude outputs\\<proyecto>\\<revN>\\...) <= 230 caracteres; U-158: cada PNG "
         "'<HOJA> - IMAGE ONLY (not editable) - walls|ceilings|walls and ceilings revN'; '_rcp_markups', '_marked_by_type', 'pNN_' o duplicados = FAIL; "
         "la GUIA_DE_REVISION cita en su primer renglón el PDF que se abre en Bluebeam; U-164: un solo RESUMEN_rev*.md en la raíz")
def ce_nombres_entrega(c):
    pl = getattr(c, "planos", None)
    if not pl or not os.path.isdir(pl):
        return R("FAIL", "sin carpeta Planos marcados/")
    nombres = sorted(os.listdir(pl))
    ev = nombres_planos(nombres)
    g = os.path.join(os.path.dirname(pl), "GUIA_DE_REVISION_DEL_ESTIMADOR.md")
    if os.path.isfile(g):
        l1 = open(g, encoding="utf-8").readline()
        if not re.search(MARKUPS_RE, l1) or "OPEN THIS IN BLUEBEAM" in l1:
            ev.append("GUIA_DE_REVISION_DEL_ESTIMADOR.md: el primer renglón no cita el PDF '<PROY>_markups_revN - OPEN IN BLUEBEAM.pdf' (U-158 / U-165)")
    if not any(n.lower().endswith(".png") for n in nombres):
        ev.append("0 PNG en Planos marcados/ (PASS en vacío prohibido)")
    if os.path.isfile(g):
        ev += guia_cambios_fallas(open(g, encoding="utf-8").read(), os.path.basename(os.path.dirname(pl)))
    ev += resumenes_fallas(os.listdir(os.path.dirname(pl)))
    raiz = os.path.dirname(pl)
    rels = [os.path.relpath(os.path.join(r, f), raiz) for r, _, fs in os.walk(raiz) for f in fs]
    ev += rutas_entrega_fallas(((getattr(c, "cfg", None) or {}).get("drive") or {}).get("carpeta_proyecto"), os.path.basename(raiz), rels)
    ev += carpeta_rev_fallas(os.path.basename(raiz))
    return R("FAIL", *ev[:20]) if ev else R("PASS", f"{len(nombres)} archivos con nombre que dice qué son; rutas Windows <= {MAX_RUTA_WINDOWS}")


@chequeo("CE_USO_REAL", ["U-166", "U-165", "BE-155"], "U-166 (usuario 11-nov: 'si ya sabes que va a pasar si cometes un error, por que no lo "
         "arreglas antes de que yo te lo diga'): simula el uso real del usuario en Windows / Bluebeam / Excel: (1) ruta Windows en Drive <= 230 "
         "(Auditoria.zip = un archivo, nombres dentro <= 120); (2) PDF de markups abre sin contraseña ni firmas y CE_VISTA_BLUEBEAM en PASS; "
         "(3) ningún nombre con < > : \" / \\ | ? *; (4) el Excel abre sin #REF! / #VALUE! / #DIV/0!; (5) test con la ruta de rev18 (264) = FAIL")
def ce_uso_real(c):
    pl = getattr(c, "planos", None)
    if not pl or not os.path.isdir(pl):
        return R("FAIL", "sin carpeta Planos marcados/ (U-137: el chequeo no pasa en vacío)")
    raiz = os.path.dirname(pl)
    proy = ((getattr(c, "cfg", None) or {}).get("drive") or {}).get("carpeta_proyecto")
    rels = [os.path.relpath(os.path.join(r, f), raiz) for r, _, fs in os.walk(raiz) for f in fs]
    ev = rutas_entrega_fallas(proy, os.path.basename(raiz), rels)
    pdfs = [p for p in glob.glob(os.path.join(pl, "*.pdf")) if re.fullmatch(MARKUPS_RE, os.path.basename(p))]
    if not pdfs:
        ev.append("0 PDF '<PROY>_markups_revN - OPEN IN BLUEBEAM.pdf' en Planos marcados/ (U-165)")
    for p in pdfs:
        ev += pdf_abre_fallas(p)
    try:
        vb = ce_vista_bluebeam(c)
        if vb[0] != "PASS":
            ev.append(f"CE_VISTA_BLUEBEAM {vb[0]}: {(vb[1] or [''])[0]} (U-166)")
    except Exception as e:                                              # noqa: BLE001
        ev.append(f"CE_VISTA_BLUEBEAM no corrió: {type(e).__name__}: {e} (U-166)")
    comp = {proy or "", os.path.basename(raiz)} | {x for r in rels for x in re.split(r"[\\/]", r)}
    ev += nombres_prohibidos_fallas(sorted(comp))
    if not c.excel or not os.path.isfile(c.excel):
        ev.append("sin Excel (Take-off/*.xlsx) que abrir (U-166)")
    else:
        ev += excel_errores_fallas(c.excel)
    return R("FAIL", *ev[:20]) if ev else R("PASS", f"{len(rels)} archivos: rutas Windows <= {MAX_RUTA_WINDOWS}, nombres válidos, "
                                                     f"{len(pdfs)} PDF de markups abre sin contraseña ni firmas, vista Bluebeam PASS, Excel sin errores")


# ---------------------------------------------------------------------------------------------------------------------------
# U-168 (usuario 11-nov: "todo esas maneras de revisar y asegurarte que todo este sin errores, los combiertas en reglas inviolables
# para a que no se me ooviden ami tampoco, incluyendo las cvs"): protocolo de verificación final. A1 / A2 los hace la compuerta;
# B1-B5 los recorre el usuario en CHECKLIST_REVISION.xlsx (tools/checklist_revision.py).
A1_N = 10
A1_TOL_FT = 1.0


def filas_partition(xlsx):
    """Renglones de wall del Partition Takeoff: [{wall, lf, h, source, fila}] (valores guardados)."""
    import openpyxl
    wb = openpyxl.load_workbook(xlsx, data_only=True)
    if "Partition Takeoff" not in wb.sheetnames:
        return []
    ws = wb["Partition Takeoff"]
    hdr, out = None, []
    for i, r in enumerate(ws.iter_rows(values_only=True), 1):
        if hdr is None:
            if r and any(str(v or "").strip() == "Wall #" for v in r):
                hdr = {str(v or "").strip(): k for k, v in enumerate(r)}
            continue
        g = lambda k: r[hdr[k]] if k in hdr and hdr[k] < len(r) else None   # noqa: E731
        w = str(g("Wall #") or "").strip()
        try:
            lf, h = float(g("Length (LF)")), float(g("Height (FT)"))
        except (TypeError, ValueError):
            continue
        if w and not w.upper().startswith(("SUBTOTAL", "TOTAL")):
            out.append({"wall": w, "lf": lf, "h": h, "source": str(g("Source (DETAIL/SHEET)") or ""), "fila": i})
    return out


def _markups_por_wall(markups_pdf):
    """{wall id: [(page index, Page Label, [vértices])]} de las PolyLine TO-<id>[~k] del PDF de markups."""
    import pymupdf
    d = pymupdf.open(markups_pdf)
    out = {}
    for i in range(d.page_count):
        for a in d[i].annots() or []:
            nm = _nm_leer(d.xref_get_key(a.xref, "NM")[1].strip("()"))
            if a.type[1] != "PolyLine" or not nm.startswith("TO-") or nm.startswith("TO-LEGEND-"):
                continue
            out.setdefault(re.sub(r"~\d+$", "", nm[3:]), []).append((i, d[i].get_label(), [tuple(p) for p in a.vertices]))
    return out


def _ptft_annot(markups_pdf):
    """{(page, NM): pt por ft} leído con pikepdf (/Measure /X /C = ft por pt)."""
    import pikepdf
    out = {}
    with pikepdf.open(markups_pdf) as d:
        for i, page in enumerate(d.pages):
            for a in page.obj.get("/Annots") or []:
                try:
                    m = a.get("/Measure")
                    if m is None:
                        continue
                    c_ = float(m.get("/X")[0].get("/C"))
                    out[(i, _nm_leer(str(a.get("/NM") or "")))] = 1.0 / c_
                except Exception:                                       # noqa: BLE001
                    continue
    return out


def remedir_wall(legs, S, ptft):
    """A1: re-mide un wall en los vectores del plano limpio. legs = [[vértices en pt]] (tramos rectos del markup); S = segmentos de
    la página. Cada extremo libre de la cadena se lleva a la terminación dibujada más cercana a lo largo del eje (fin de las líneas
    paralelas de la banda o línea perpendicular que la cruza = cara del wall que llega). -> (LF re-medido, cobertura 0..1, nota)."""
    import math as _m
    ext = []          # (punto, dirección hacia afuera)
    pts_all = [p for lg in legs for p in lg]
    tot_pt = sum(_m.dist(lg[k], lg[k + 1]) for lg in legs for k in range(len(lg) - 1))
    for lg in legs:
        for idx, nb in ((0, 1), (len(lg) - 1, len(lg) - 2)):
            p, q = lg[idx], lg[nb]
            if sum(1 for x in pts_all if _m.dist(x, p) < 0.5) > 1:
                continue                                                 # extremo compartido con otro tramo
            L = _m.dist(p, q) or 1.0
            ext.append((p, ((p[0] - q[0]) / L, (p[1] - q[1]) / L)))
    banda, busca = 0.75 * ptft, 2.0 * ptft
    ajuste, cubierto, largo = 0.0, 0.0, 0.0
    for lg in legs:
        for k in range(len(lg) - 1):
            a, b = lg[k], lg[k + 1]
            L = _m.dist(a, b)
            if L < 1e-6:
                continue
            u = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
            iv = []
            for s_ in S:
                dx, dy = s_[2] - s_[0], s_[3] - s_[1]
                Ls = _m.hypot(dx, dy)
                if Ls < 1.0 or abs(dx * u[1] - dy * u[0]) / Ls > 0.1:
                    continue
                if abs((s_[0] - a[0]) * u[1] - (s_[1] - a[1]) * u[0]) > banda:
                    continue
                t0 = (s_[0] - a[0]) * u[0] + (s_[1] - a[1]) * u[1]
                t1 = (s_[2] - a[0]) * u[0] + (s_[3] - a[1]) * u[1]
                lo, hi = max(0.0, min(t0, t1)), min(L, max(t0, t1))
                if hi > lo:
                    iv.append((lo, hi))
            iv.sort()
            c_, fin = 0.0, -1.0
            for lo, hi in iv:
                lo = max(lo, fin)
                if hi > lo:
                    c_ += hi - lo
                    fin = hi
            cubierto += c_
            largo += L
    notas = []
    for p, u in ext:
        cand = []
        for s_ in S:
            dx, dy = s_[2] - s_[0], s_[3] - s_[1]
            Ls = _m.hypot(dx, dy)
            if Ls < 1.0:
                continue
            par = abs(dx * u[1] - dy * u[0]) / Ls <= 0.1
            perp = abs(dx * u[0] + dy * u[1]) / Ls <= 0.1
            if par:
                if abs((s_[0] - p[0]) * u[1] - (s_[1] - p[1]) * u[0]) > banda:
                    continue
                for x, y in ((s_[0], s_[1]), (s_[2], s_[3])):
                    t = (x - p[0]) * u[0] + (y - p[1]) * u[1]
                    if abs(t) <= busca:
                        cand.append(t)
            elif perp:
                t = (s_[0] - p[0]) * u[0] + (s_[1] - p[1]) * u[1]
                off0 = (s_[0] - p[0]) * u[1] - (s_[1] - p[1]) * u[0]
                off1 = (s_[2] - p[0]) * u[1] - (s_[3] - p[1]) * u[0]
                if abs(t) <= busca and min(off0, off1) <= banda and max(off0, off1) >= -banda:
                    cand.append(t)
        if cand:
            t = min(cand, key=abs)
            ajuste += t
            notas.append(f"{t / ptft:+.2f} ft")
        else:
            notas.append("NO drawn end within 2 ft")             # el dibujo sigue (o no hay nada): no se puede confirmar el LF
    cob = cubierto / largo if largo else 0.0
    return round((tot_pt + ajuste) / ptft, 2), round(cob, 2), "; ".join(notas)


def a1_remedir(xlsx, markups_pdf, plano_pdf, n=A1_N, tol=A1_TOL_FT):
    """A1 (U-168): las n walls más largas del Excel re-medidas en los vectores del plano limpio a la escala del markup.
    -> (filas [{wall, sheet, lf, medido, delta, cobertura, nota, ok}], fallas)"""
    import pymupdf
    filas = sorted(filas_partition(xlsx), key=lambda r: -r["lf"])
    mk = _markups_por_wall(markups_pdf)
    esc = _ptft_annot(markups_pdf)
    dp = pymupdf.open(plano_pdf)
    cache, out, fallas, vistos = {}, [], [], set()
    for r in filas:
        if len(out) >= n:
            break
        if r["wall"] in vistos:
            continue
        vistos.add(r["wall"])
        legs = mk.get(r["wall"]) or []
        if not legs:
            out.append(dict(wall=r["wall"], sheet="", lf=r["lf"], medido=None, delta=None, cobertura=0, nota="no markup", ok=False))
            fallas.append(f"A1 {r['wall']}: sin markup TO-{r['wall']} que re-medir")
            continue
        pg, lab = legs[0][0], legs[0][1]
        ptft = next((v for (i, k), v in esc.items() if i == pg and re.sub(r"~\d+$", "", k[3:]) == r["wall"]), None)
        if not ptft:
            fallas.append(f"A1 {r['wall']}: markup sin /Measure (escala)")
            continue
        S = cache.setdefault(pg, _segs_plano(dp[pg]))
        med, cob, nota = remedir_wall([lg[2] for lg in legs if lg[0] == pg], S, ptft)
        dl = round(med - r["lf"], 2)
        ok = abs(dl) <= tol and cob >= 0.5 and "NO drawn end" not in nota
        out.append(dict(wall=r["wall"], sheet=lab, lf=r["lf"], medido=med, delta=dl, cobertura=cob, nota=nota, ok=ok))
        if not ok:
            fallas.append(f"A1 {r['wall']} ({lab}): Excel {r['lf']:.2f} LF, re-medido {med:.2f} LF (delta {dl:+.2f}, cobertura {cob:.0%}) {nota}")
    return out, fallas


def _ftin_formas(h):
    """Formas impresas de una altura en ft: 9.2396 -> ["9'-2 7/8\"", "9'-2-7/8\"", ...] (1/16")."""
    tot = round(h * 192) / 16.0          # pulgadas a 1/16
    ft, inch = int(tot // 12), tot - 12 * int(tot // 12)
    ent = int(inch)
    fr = round((inch - ent) * 16)
    fracs = []
    if fr:
        n_, d_ = fr, 16
        while n_ % 2 == 0:
            n_, d_ = n_ // 2, d_ // 2
        fracs = [f"{n_}/{d_}"]
    base = []
    for sep in ("-", " - ", "- ", " -"):
        if fracs:
            base += [f"{ft}'{sep}{ent} {fracs[0]}\"", f"{ft}'{sep}{ent}-{fracs[0]}\""]
        else:
            base.append(f"{ft}'{sep}{ent}\"")
    return base


def _norm_cota(t):
    return re.sub(r"\s+", "", str(t)).replace("′", "'").replace("″", '"').replace("''", '"').upper()


def a2_alturas(xlsx, markups_pdf, plano_pdf, canon=None):
    """A2 (U-168): cada altura distinta (Depth) del Excel contra la cota IMPRESA de la hoja que cita su fila (N/HOJA en Source):
    la cota en ft-in aparece impresa, o la altura es [DERIVED] y cada cota / elevación de su operación aparece impresa en esa hoja.
    -> (filas [{depth, walls, cita, impresa, ok, nota}], fallas)"""
    import pymupdf
    dm, dp = pymupdf.open(markups_pdf), pymupdf.open(plano_pdf)
    pag = {}
    for i in range(dm.page_count):
        pag.setdefault(hoja_de_etiqueta(dm[i].get_label()) if dm[i].get_label() else str(i + 1), i)
    txt = {}
    def texto(h):
        i = pag.get(h)
        if i is None or i >= dp.page_count:
            return None
        if i not in txt:
            txt[i] = _norm_cota(dp[i].get_text())
        return txt[i]
    can = canon if isinstance(canon, dict) else (_json(canon) if canon else None) or {}
    hs = {w["id"]: str(w.get("height_source") or w.get("height_note") or "") for w in (can.get("walls") or []) + (can.get("existing_walls") or [])}
    grupos = {}
    for r in filas_partition(xlsx):
        grupos.setdefault(round(r["h"], 4), []).append(r)
    out, fallas = [], []
    formas_de = {h: {_norm_cota(f) for f in _ftin_formas(h)} for h in grupos}
    for h in sorted(grupos):
        rs = grupos[h]
        src = next((hs.get(r["wall"]) for r in rs if hs.get(r["wall"])), "") or rs[0]["source"]
        hojas = list(dict.fromkeys(re.findall(r"\b([A-Z]{1,2}\d{1,2}\.\d{1,2}[A-Z]?|[A-Z]{1,2}-?\d{3}[A-Z]?)\b", src + " " + rs[0]["source"])))   # BE-XF05; BE-GK25 A131 / A-201
        cita = next(iter(re.findall(r"\b\d{1,2}/(?:[A-Z]{1,2}\d{1,2}\.\d{1,2}|[A-Z]{1,2}-?\d{3})\b", src)), "") or (hojas[0] if hojas else "")
        formas = formas_de[h]
        impresa, nota, estado = "", "", ""
        for hj in hojas:
            t = texto(hj)
            if t and any(f in t for f in formas):
                impresa, estado, nota = _ftin_formas(h)[0], "PRINTED", f"printed on {hj}"
                break
        if not estado:
            antes = src.rsplit("=", 1)[0] if "=" in src else ""
            nums = re.findall(r"\d+'\s*-\s*\d+(?:\s+\d+/\d+)?\"|\b\d{3,5}\.\d{1,2}'|(?:(?<=C\.H\. )|(?<='))\d{1,2}-\d{1,2}\b(?!['\"/])", antes)   # BE-GK25: RCP tag '12-0'
            otras = set().union(*(formas_de[x] for x in grupos if x != h)) if len(grupos) > 1 else set()
            falt = [x for x in nums if _norm_cota(x) not in otras and not any(texto(hj) and _norm_cota(x) in texto(hj) for hj in hojas)]
            vec = [(float(a), float(b), float(k), float(r_)) for a, b, k, r_ in
                   re.findall(r"\((\d+\.?\d*)\s*-\s*(\d+\.?\d*)\)\s*/\s*(\d+\.?\d*)\s*=\s*(\d+\.?\d*)", src)]
            vec_ok = vec and all(abs((a - b) / k - r_) <= 0.01 and k in (4.5, 9, 13.5, 18, 27, 36, 54, 72) for a, b, k, r_ in vec)
            dice = any(abs(float(x) - h) <= 0.01 for x in re.findall(r"\b\d+\.\d+\b", src))
            decs = [float(x) for x in re.findall(r"(?<![\d.'/])\d+\.\d+(?![\d'])", antes)]
            dec_ok = len(decs) >= 2 and all(any(abs(x - g) <= 0.001 for g in grupos if g != h) for x in decs)
            if (nums and not falt) or (not nums and dec_ok):
                estado, impresa = "DERIVED", ", ".join(nums[:4])
                nota = f"[DERIVED] from values printed on {', '.join(hojas[:3])} or other verified heights"
            elif vec_ok and dice:
                estado, impresa = "VECTOR", "not dimensioned"
                nota = (f"[DERIVED] vector measurement at the printed scale on {cita or ', '.join(hojas[:2])} "
                        f"({len(vec)} operation(s) re-computed); verify in Bluebeam")
            else:
                busca = falt[:1] or [_ftin_formas(h)[0]]
                donde = [hoja_de_etiqueta(dm[i].get_label()) for i in range(min(dm.page_count, dp.page_count))
                         if dm[i].get_label() and _norm_cota(busca[0]) in (txt.get(i) or txt.setdefault(i, _norm_cota(dp[i].get_text())))]
                nota = (f"not found printed on {', '.join(hojas[:3]) or 'no sheet cited'}: {', '.join(falt[:3])}" if falt
                        else f"{_ftin_formas(h)[0]} not found printed on {', '.join(hojas[:3]) or 'no sheet cited'} and no checked operation")
                if donde:
                    nota += f"; {busca[0]} IS printed on {', '.join(donde[:6])}: cite that N/SHEET"
        ok = bool(estado)
        out.append(dict(depth=h, ftin=_ftin_formas(h)[0], walls=len(rs), ejemplo=rs[0]["wall"], cita=cita, impresa=impresa, ok=ok,
                        estado=estado or "NOT FOUND", nota=nota))
        if not ok:
            fallas.append(f"A2 Depth {h:g} ft ({_ftin_formas(h)[0]}, {len(rs)} rows, e.g. {rs[0]['wall']}): {nota}")
    return out, fallas


def _a_entrada(c):
    pdfs = [p for p in _pdfs_markups(c) if re.fullmatch(MARKUPS_RE, os.path.basename(p))] or _pdfs_markups(c)
    bs = c.cfg.get("bidset_limpio") or c.cfg.get("bidset")
    return (pdfs[0] if pdfs else None), (bs if bs and os.path.isfile(bs) else None)


@chequeo("CE_A1_REMEDICION", ["U-168"], "U-168 A1: las 10 walls más largas del Excel re-medidas en los vectores del plano limpio a la "
         "escala del markup (cada extremo a la terminación dibujada); |delta| <= 1 ft y la banda dibujada cubre >= 50 % del eje")
def ce_a1_remedicion(c):
    mk, bs = _a_entrada(c)
    if not mk or not bs or not c.excel:
        return R("FAIL", "sin PDF de markups, bid set limpio o Excel (U-137: no pasa en vacío)")
    filas, fs = a1_remedir(c.excel, mk, bs)
    if not filas:
        return R("FAIL", "0 walls re-medidas (U-137)")
    return R("FAIL", *fs) if fs else R("PASS", f"{len(filas)} walls más largas re-medidas en vectores: max |delta| "
                                               f"{max(abs(f['delta']) for f in filas):.2f} ft")


@chequeo("CE_A2_ALTURAS", ["U-168"], "U-168 A2: cada altura distinta (Depth) del Excel contra la cota impresa de la hoja que cita "
         "(o, si es [DERIVED], cada cota / elevación de su operación impresa en esa hoja)")
def ce_a2_alturas(c):
    mk, bs = _a_entrada(c)
    if not mk or not bs or not c.excel:
        return R("FAIL", "sin PDF de markups, bid set limpio o Excel (U-137: no pasa en vacío)")
    # BE-GK25 (Grand Kia): sheets with text as vector curves are read through the OCR copy of the set (entrega.json bidset_texto)
    bt = (c.cfg or {}).get("bidset_texto")
    filas, fs = a2_alturas(c.excel, mk, bt if bt and os.path.isfile(bt) else bs, getattr(c, "canon", None))
    if not filas:
        return R("FAIL", "0 alturas (U-137)")
    return R("FAIL", f"{len(fs)} de {len(filas)} alturas sin cota impresa encontrada", *fs[:25]) if fs else \
        R("PASS", f"{len(filas)} alturas distintas con su cota impresa (o sus valores impresos)")


RX_HOJA_CONCRETA = re.compile(r"\b[A-Z]{1,2}\d{1,2}\.\d{1,2}[A-Z]?\b|\b[A-Z]{1,2}-?\d{3}[A-Z]?\b")   # BE-GK14 (Grand Kia): hojas sin punto (A111, A-201) también son hoja concreta   # BE-XF05 (Xfinity 10-nov): hojas de un decimal (A0.1, A2.0) también son hoja concreta
RX_HOJA_COMODIN = re.compile(r"\b[A-Z]{1,2}\d{0,2}\.?[xX]{1,2}\b|\b[A-Z]{1,2}\d\.\d?[xX]\b")


def cita_altura_fallas(canon):
    """U-168 / A2 (CR City Hotel rev18: 9'-0" de 106 filas citaba 'A7.xx unit RCP'): la fuente de la altura de cada wall cita una hoja
    CONCRETA (N/HOJA o HOJA, p. ej. 7/A7.05 o A7.05); una hoja comodín ('A7.xx', 'A7.x') o ninguna hoja = falla. -> [fallas]"""
    can = canon if isinstance(canon, dict) else (_json(canon) if canon else None) or {}
    comodin, sin = {}, []
    for w in (can.get("walls") or []) + (can.get("existing_walls") or []):
        if not isinstance(w, dict):
            continue
        src = str(w.get("height_source") or w.get("height_note") or "")
        m = RX_HOJA_COMODIN.search(src)
        if m:
            comodin.setdefault(m.group(0), []).append(w.get("id"))
        elif not RX_HOJA_CONCRETA.search(src):
            sin.append(w.get("id"))
    ev = [f"{len(v)} walls con la altura citada a una hoja comodín '{k}' (cite la hoja concreta N/HOJA), ej. {', '.join(map(str, v[:4]))}"
          for k, v in comodin.items()]
    if sin:
        ev.append(f"{len(sin)} walls con fuente de altura sin hoja (N/HOJA o HOJA), ej. {', '.join(map(str, sin[:4]))}")
    return ev


@chequeo("CE_CITA_ALTURA", ["U-168", "U-115", "U-010"], "U-168 / A2: toda fuente de altura (height_source) cita una hoja concreta "
         "(N/HOJA o HOJA); una hoja comodín como 'A7.xx' o ninguna hoja = FAIL (CR City Hotel rev18: 9'-0\" citaba 'A7.xx unit RCP')")
def ce_cita_altura(c):
    can = c.canon if isinstance(getattr(c, "canon", None), dict) else (_json(c.canon) if getattr(c, "canon", None) else {}) or {}
    n = len((can.get("walls") or []) + (can.get("existing_walls") or []))
    if not n:
        return R("FAIL", "canon sin walls (U-137: no pasa en vacío)")
    fs = cita_altura_fallas(can)
    return R("FAIL", *fs) if fs else R("PASS", f"{n} walls con la altura citada a una hoja concreta")


CHECKLIST_RE = r"(?:[A-Z][A-Za-z0-9]{0,5}_)?CHECKLIST_REVISION(?:_rev\d+[a-z]?)?\.xlsx"
CHECKLIST_HOJAS = ("B1 Longest walls", "B2 Heights", "B3 Sheets to walk", "B4 Exclusions & decisions", "B5 Bluebeam CSV")


def checklist_fallas(path, xlsx_takeoff):
    """U-168: CHECKLIST_REVISION.xlsx con las 5 secciones llenas: B1 = las A1_N walls más largas del Excel, B2 = todas las alturas
    distintas, B3 hojas, B4 = todas las exclusiones del Scope y todas las decisiones de Review Items, B5 pasos del CSV. -> [fallas]"""
    import openpyxl
    try:
        wb = openpyxl.load_workbook(path, data_only=True)
    except Exception as e:                                              # noqa: BLE001
        return [f"{os.path.basename(path)} no abre: {e}"]
    ev = [f"falta la hoja '{h}'" for h in CHECKLIST_HOJAS if h not in wb.sheetnames]
    if ev:
        return ev
    col = lambda h, k: [str(r[k]).strip() for r in wb[h].iter_rows(min_row=4, values_only=True) if r and r[k] not in (None, "")]   # noqa: E731
    pt = filas_partition(xlsx_takeoff)
    top = []
    for r in sorted(pt, key=lambda r: -r["lf"]):
        if r["wall"] not in top:
            top.append(r["wall"])
        if len(top) == A1_N:
            break
    b1 = col(CHECKLIST_HOJAS[0], 1)
    if set(top) - set(b1):
        ev.append(f"B1 sin las walls más largas: {sorted(set(top) - set(b1))[:5]}")
    alturas = {f"{round(r['h'], 4):g}" for r in pt}
    b2 = set()
    for v in col(CHECKLIST_HOJAS[1], 0):
        try:
            b2.add(f"{round(float(v), 4):g}")
        except ValueError:
            pass
    if alturas - b2:
        ev.append(f"B2 sin {len(alturas - b2)} altura(s): {sorted(alturas - b2)[:5]}")
    if not col(CHECKLIST_HOJAS[2], 0):
        ev.append("B3 vacía (hojas que recorrer)")
    wt = openpyxl.load_workbook(xlsx_takeoff, data_only=True)
    exc = []
    if "Scope Checklist" in wt.sheetnames:
        exc = [str(r[0]).strip() for r in wt["Scope Checklist"].iter_rows(min_row=2, values_only=True)
               if r and r[0] and (str(r[2] or "").upper() == "NOT APPLICABLE" or str(r[3] or "").upper().startswith("EXCLUDED"))]
    ri = []
    if "Review Items" in wt.sheetnames:
        ri = [str(r[0]).strip() for r in wt["Review Items"].iter_rows(min_row=3, values_only=True) if r and r[0] and "/" in str(r[0])]
    b4 = set(col(CHECKLIST_HOJAS[3], 1))
    falt = [x for x in exc + ri if x not in b4]
    if falt:
        ev.append(f"B4 sin {len(falt)} exclusión(es) / Review Item(s): {falt[:5]}")
    if len(col(CHECKLIST_HOJAS[4], 1)) < 4:
        ev.append("B5 sin los pasos del CSV de Bluebeam")
    return ev


@chequeo("CE_CHECKLIST_USUARIO", ["U-168", "U-157", "U-167"], "U-168: la entrega lleva en su raíz CHECKLIST_REVISION.xlsx (inglés; ayuda "
         "en español solo en las celdas de ayuda) con B1 las 10 walls más largas, B2 todas las alturas, B3 las hojas que recorrer, B4 todas "
         "las exclusiones del Scope y decisiones de Review Items con su delta, B5 los pasos del CSV de Bluebeam")
def ce_checklist_usuario(c):
    pl = getattr(c, "planos", None)
    if not pl or not c.excel:
        return R("FAIL", "sin entrega o sin Excel (U-137)")
    raiz = os.path.dirname(pl)
    cl = [f for f in os.listdir(raiz) if re.fullmatch(CHECKLIST_RE, f)]
    if not cl:
        return R("FAIL", "falta CHECKLIST_REVISION.xlsx en la raíz de la entrega (U-168): python3 -I tools/checklist_revision.py")
    fs = checklist_fallas(os.path.join(raiz, cl[0]), c.excel)
    return R("FAIL", *fs) if fs else R("PASS", f"{cl[0]}: 5 secciones llenas (10 walls, todas las alturas, todas las exclusiones)")


def resumenes_fallas(nombres_raiz):
    """U-164 (usuario 11-nov: 'RESUMEN_rev5 al 17, cual es la reazon de crear tantos'): la raíz de la entrega lleva UN SOLO RESUMEN (el de la
    versión vigente); la historia va en Auditoria/HISTORIAL_CAMBIOS.md. Más de un RESUMEN_rev*.md en la raíz = FAIL."""
    rs = sorted(n for n in nombres_raiz if re.match(r"(?i)RESUMEN_rev\d+.*\.md$", n))
    return [f"U-164: {len(rs)} RESUMEN en la raíz de la entrega ({', '.join(rs[:6])}...): solo el de la versión vigente; los viejos a Auditoria/HISTORIAL_CAMBIOS.md"] if len(rs) > 1 else []


def guia_cambios_fallas(texto, carpeta):
    """rev15 (revisión completa rev14 #18): la PRIMERA sección 'CAMBIOS revN vs revM' de la GUIA es la de la revisión entregada
    (revN = la de la carpeta 'revN FINAL ...') y M = N - 1. rev14 abría con 'CAMBIOS rev7 vs rev6' (bloque insertado al final)."""
    m = re.search(r"(?i)\brev(\d+)\b", carpeta or "")
    c1 = re.search(r"(?m)^##\s*CAMBIOS\s+rev(\d+)\s+vs\s+rev(\d+)", texto or "")
    if not m:
        return []
    n = int(m.group(1))
    if n <= 1:
        return []
    if not c1:
        return [f"GUIA: sin sección 'CAMBIOS rev{n} vs rev{n - 1}'"]
    if (int(c1.group(1)), int(c1.group(2))) != (n, n - 1):
        return [f"GUIA: la primera sección de cambios es 'CAMBIOS rev{c1.group(1)} vs rev{c1.group(2)}', debe ser 'CAMBIOS rev{n} vs rev{n - 1}' (#18)"]
    return []


RX_CUARTO = re.compile(r"^\s*(\d{3}[A-Z]?)\s*$")


def cuartos_rcp(hojas):
    """U-159: {hoja RCP: [números de cuarto impresos]} - hojas cuyo texto dice REFLECTED CEILING / RCP y trae números de cuarto (línea
    sola de 3 dígitos, con letra opcional: 118B); los números de puerta '104.1' no cuentan."""
    out = {}
    for h, t in (hojas or {}).items():
        if not re.match(r"(?i)^A[1-9]", str(h)) or not re.search(r"(?i)REFLECTED\s+CEILING|\bRCP\b", str(t)):
            continue   # solo hojas de arquitectura (los planos E / T citan RCP en otro sentido)
        rs = sorted({m.group(1) for ln in str(t).split("\n") for m in [RX_CUARTO.match(ln)] if m})
        if rs:
            out[h] = rs
    return out


def _en_poly(poly, x, y):
    n, ok = len(poly), False
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / ((y2 - y1) or 1e-9) + x1:
            ok = not ok
    return ok


def frac_en_poly(rect, poly, n=12):
    x0, y0, x1, y1 = rect
    pts = [(x0 + (x1 - x0) * (i + .5) / n, y0 + (y1 - y0) * (j + .5) / n) for i in range(n) for j in range(n)]
    return sum(1 for q in pts if _en_poly(poly, *q)) / float(len(pts))


def rcp_verticales_fallas(tabla):
    """rev16 (revisión dirigida de rev15, U-159 / U-160): las áreas SIN número de un RCP (hoistway, stair, shaft, pasillo) no las encuentra el
    barrido de números. Cada elemento vertical se declara en la tabla con 'vertical' (clave estable: 'hoistway-service', 'stair-W', 'shaft-N'...)
    y debe tener renglón o EXCLUDED en TODA hoja RCP de la tabla (rev15: A3.04 marcaba hoistways y shafts, A3.02 / A3.03 en blanco), salvo
    'not_on': {hoja: motivo impreso} en alguna de sus entradas. -> [fallas]"""
    rooms = (tabla or {}).get("rooms") or []
    hojas = sorted({str(r.get("sheet")) for r in rooms if re.match(r"A3\.0\d$", str(r.get("sheet")))})
    tiene, exento = {}, {}
    for r in rooms:
        v = r.get("vertical")
        if not v:
            continue
        h = str(r.get("draw_sheet") if re.match(r"A3\.0\d$", str(r.get("draw_sheet") or "")) else r.get("sheet"))
        if r.get("disposition") in ("row", "missing_loaded", "exclusion"):
            tiene.setdefault(v, set()).add(h)
        for h2, why in (r.get("not_on") or {}).items():
            if str(why or "").strip():
                exento.setdefault(v, set()).add(h2)
    ev = []
    for v in sorted(tiene):
        for h in hojas:
            if h not in tiene[v] and h not in exento.get(v, set()):
                ev.append(f"{h}: elemento vertical '{v}' sin renglón ni EXCLUDED (está en {sorted(tiene[v])}; U-159 / U-160 áreas sin número)")
    return ev


def rcp_excluded_geom_fallas(tabla, excl_polys, excl_text_full):
    """U-160 endurecida (rev15, revisión completa rev14 F02/F03/F08): por cada exclusión, en su hoja: polígono gris EXCLUDED (obligatorio)
    con el mismo texto, FreeText con >= 90 % de su caja dentro de ese polígono, y sin línea de callout (/CL).
    excl_polys = {hoja: [(content, [[x,y],...])]}; excl_text_full = {hoja: [(rect, content, tiene_CL)]}."""
    ev = []
    for r in (tabla or {}).get("rooms") or []:
        if r.get("disposition") != "exclusion":
            continue
        h, n = str(r.get("draw_sheet") or r.get("sheet")), r.get("room")
        if not r.get("polygon") or len(r.get("polygon")) < 3:
            ev.append(f"{h} {n}: exclusión sin polígono del cuarto en rcp_cuartos.json (U-160: polígono gris obligatorio)")
            continue
        txt = f"EXCLUDED - {str(r.get('reason') or '').strip().rstrip('.')} ({r.get('nhoja')})"
        pols = [v for c_, v in excl_polys.get(h) or [] if c_ == txt or str(c_).startswith(txt + " [EDGE NOT DRAWN:")]
        fts = [(rc, cl) for rc, c_, cl in excl_text_full.get(h) or [] if c_ == txt]
        if not pols:
            ev.append(f"{h} {n}: sin polígono gris EXCLUDED en el PDF (U-160)")
            continue
        if not fts:
            ev.append(f"{h} {n}: sin FreeText EXCLUDED con su motivo en el PDF (U-160)")
            continue
        fr = max(frac_en_poly(rc, pols[0]) for rc, _ in fts)
        if fr < 0.9:
            ev.append(f"{h} {n}: solo {fr:.0%} del texto EXCLUDED dentro del cuarto (>= 90 %, U-160)")
        if any(cl for _, cl in fts):
            ev.append(f"{h} {n}: FreeText EXCLUDED con línea de callout /CL (sale del texto; U-160 / F08)")
    return ev


def rcp_cuartos_fallas(hojas_cuartos, tabla, excluded_text):
    """U-159 / U-160: cada cuarto impreso en una hoja RCP tiene renglón (rows) o exclusión con motivo + N/HOJA; cada exclusión tiene su
    FreeText EXCLUDED en esa hoja (excluded_text = {hoja: [rects / contents]}). -> [fallas]"""
    idx = {(str(r.get("sheet")), str(r.get("room"))): r for r in (tabla or {}).get("rooms") or []}
    ev = []
    for h, rs in sorted(hojas_cuartos.items()):
        for n in rs:
            r = idx.get((h, n))
            if r is None:
                ev.append(f"{h} cuarto {n}: sin renglón de ceiling ni exclusión con motivo (U-159)")
                continue
            dsp = r.get("disposition")
            if dsp in ("row", "missing_loaded"):
                if not r.get("rows"):
                    ev.append(f"{h} cuarto {n}: '{dsp}' sin rows (U-159)")
            elif dsp == "exclusion":
                if not (str(r.get("reason") or "").strip() and str(r.get("nhoja") or "").strip()):
                    ev.append(f"{h} cuarto {n}: exclusión sin motivo impreso o sin N/HOJA (U-159)")
                xy = r.get("label_xy")
                txts = excluded_text.get(str(r.get("draw_sheet") or h)) or []
                if r.get("polygon"):   # rev15: con polígono, la ubicación la revisa rcp_excluded_geom_fallas (texto dentro del cuarto)
                    if not any(str(c_ or "").startswith("EXCLUDED - ") for _, c_ in txts):
                        ev.append(f"{h} cuarto {n}: sin FreeText 'EXCLUDED - motivo (N/HOJA)' en su hoja (U-160)")
                elif not any(xy and rect[0] <= xy[0] <= rect[2] and rect[1] <= xy[1] <= rect[3] for rect, _ in txts):
                    ev.append(f"{h} cuarto {n}: sin FreeText 'EXCLUDED - motivo (N/HOJA)' sobre el cuarto en el PDF de markups (U-160)")
            elif dsp == "not_a_room":   # BE-XF03 (Xfinity 10-nov): número impreso que NO es cuarto (designator de acero '600 S 162', herraje '200D')
                img = str(r.get("img") or "")
                if not (str(r.get("reason") or "").strip() and str(r.get("nhoja") or "").strip() and img and os.path.isfile(img)):
                    ev.append(f"{h} cuarto {n}: 'not_a_room' sin motivo impreso, N/HOJA o imagen existente (U-159)")
            else:
                ev.append(f"{h} cuarto {n}: disposición '{dsp}' desconocida")
    return ev


@chequeo("CE_RCP_CUARTOS", ["U-159", "U-160"], "U-159: todo número de cuarto impreso en una hoja RCP tiene renglón de ceiling o exclusión con el "
         "motivo impreso y su N/HOJA (sentido RCP -> Excel); U-160: cada exclusión lleva sobre el cuarto un FreeText 'EXCLUDED - motivo "
         "(N/HOJA)' Subject EXCLUDED en el PDF de markups; falta uno = FAIL. rev15: polígono gris obligatorio, >= 90 % del texto "
         "dentro del cuarto y sin línea de callout /CL")
def ce_rcp_cuartos(c):
    st = _json(c.set_p) or {}
    hc = cuartos_rcp(st.get("hojas") or {})
    if not hc:
        return R("AMBER", "ninguna hoja RCP con números de cuarto en set_texto.json")
    tp = (sorted(_rglob(c.w, "**/rcp_cuartos.json")) or [None])[0]   # BE-GK35
    if not tp:
        return R("FAIL", f"sin rcp_cuartos.json (tabla de cuartos por hoja RCP, U-159): {sum(len(v) for v in hc.values())} cuartos en {sorted(hc)}")
    tabla = _json(tp) or {}
    ex, exp, ext = {}, {}, {}
    if c.markups and os.path.isfile(c.markups):
        import pymupdf as _f
        _d = _f.open(c.markups)
        for p in _d:
            for a in p.annots() or []:
                if a.info.get("subject") != "EXCLUDED":
                    continue
                hj = (p.get_label() or "").strip()
                if a.type[1] == "FreeText":
                    ex.setdefault(hj, []).append((tuple(a.rect), a.info.get("content")))
                    ext.setdefault(hj, []).append((tuple(a.rect), a.info.get("content"), _d.xref_get_key(a.xref, "CL")[0] != "null"))
                elif a.type[1] == "Polygon":
                    exp.setdefault(hj, []).append((a.info.get("content"), [[q[0], q[1]] for q in a.vertices]))
    ev = rcp_cuartos_fallas(hc, tabla, ex)
    if c.markups and os.path.isfile(c.markups):
        ev += rcp_excluded_geom_fallas(tabla, exp, ext)
    ev += rcp_verticales_fallas(tabla)
    n_ex = sum(1 for r in tabla.get("rooms") or [] if r.get("disposition") == "exclusion")
    return R("FAIL", *ev[:25]) if ev else R("PASS", f"{sum(len(v) for v in hc.values())} cuartos en {len(hc)} hojas RCP: renglón o exclusión; "
                                                     f"{n_ex} exclusiones con su FreeText EXCLUDED ({ {k: len(v) for k, v in ex.items()} })")


def _skill_version():
    """U-177 (1): the skill version the gate ran with (VERSION line of the skill's INDICE / SKILL.md)."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for f in ("VERSION", "INDICE.md", "SKILL.md"):
        p = os.path.join(base, f)
        if os.path.isfile(p):
            m = re.search(r"v\d+cf\d+[a-z]?", open(p, encoding="utf-8", errors="ignore").read()[:20000])
            if m:
                return m.group(0)
    return None


def _segs_pagina(page, min_len=3.0):
    import math as _m
    S = []
    for dr in page.get_drawings():
        for it in dr["items"]:
            if it[0] == "l" and _m.dist(it[1], it[2]) >= min_len:
                S.append((it[1].x, it[1].y, it[2].x, it[2].y))
            elif it[0] == "re":
                r_ = it[1]
                S += [(r_.x0, r_.y0, r_.x1, r_.y0), (r_.x1, r_.y0, r_.x1, r_.y1), (r_.x1, r_.y1, r_.x0, r_.y1), (r_.x0, r_.y1, r_.x0, r_.y0)]
    grid = {}
    for sg in S:
        for gx in range(int(min(sg[0], sg[2]) // 20), int(max(sg[0], sg[2]) // 20) + 1):
            for gy in range(int(min(sg[1], sg[3]) // 20), int(max(sg[1], sg[3]) // 20) + 1):
                grid.setdefault((gx, gy), []).append(sg)
    return grid


def cobertura_borde(grid, poly, tol=2.5, paso=3.0):
    """rev15 (revisión completa rev14 F04 / F05): fracción del perímetro del polígono a <= tol pt de una línea vectorial de la hoja."""
    import math as _m

    def d(px, py, sg):
        x1, y1, x2, y2 = sg; dx, dy = x2 - x1, y2 - y1; L = dx * dx + dy * dy
        t = 0 if L == 0 else max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / L))
        return _m.hypot(px - x1 - t * dx, py - y1 - t * dy)
    def par(sg, ux, uy):   # solo líneas PARALELAS al borde (el hatch / stipple cruza los bordes y no cuenta)
        lx, ly = sg[2] - sg[0], sg[3] - sg[1]; L = _m.hypot(lx, ly)
        return L >= 6.0 and abs(lx * uy - ly * ux) / L <= 0.17
    tot = ok = 0
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        Lab = _m.dist(a, b)
        if Lab < 1e-6:
            continue
        ux, uy = (b[0] - a[0]) / Lab, (b[1] - a[1]) / Lab
        n = max(1, int(Lab / paso))
        for k in range(n):
            px, py = a[0] + (b[0] - a[0]) * (k + .5) / n, a[1] + (b[1] - a[1]) * (k + .5) / n
            tot += 1
            if any(par(sg, ux, uy) and d(px, py, sg) <= tol for sg in grid.get((int(px // 20), int(py // 20)), [])):
                ok += 1
    return ok / tot if tot else 0.0


RX_TITULO_VISTA = re.compile(r"(?i)\b(ENLARGED\s+)?(RCP|REFLECTED\s+CEILING|CEILING\s+PLAN|PLAN)\b")


def vista_de(page, cx, cy):
    """título de vista que corresponde al punto: el título más cercano DEBAJO del punto, alineado a su izquierda (los títulos de vista van
    abajo a la izquierda de la vista). -> texto del título o None."""
    best = None
    for b in page.get_text("blocks"):
        t = " ".join(str(b[4]).split())
        if not re.search(r"\d\s*/\s*\d+\"?\s*=\s*1'-0\"", t) and not re.search(r"(?i)^\s*\d+\s+ENLARGED|ENLARGED (PLAN|RCP)", t):
            continue
        if not RX_TITULO_VISTA.search(t) or b[1] < cy or b[0] > cx + 250:
            continue
        if best is None or b[1] - cy < best[0]:
            best = (b[1] - cy, t)
    return best[1] if best else None


PISO_CONTORNO = 0.50     # U-177 (2) (auditoría U-138 11-nov: CE_RCP_CONTORNO pasaba con min 0.0 por exenciones)


RX_FUENTE_POLI = re.compile(r"source ([A-Z]{1,2}\d{1,2}\.\d{2}[A-Z]?) offset \((-?[\d.]+), (-?[\d.]+)\)")


def rcp_contorno_fallas(doc, umbral=0.60, limpio=None, minimo=PISO_CONTORNO):
    """rev15 + U-177: por cada polígono de cielo (title 'take-off') y cada polígono EXCLUDED: (1) cobertura de borde contra las líneas de
    la hoja >= umbral (CLG-L2-56 con el offset planta->RCP sumado dos veces: 0.28-0.36); un borde que no dibuja la hoja se declara
    '[EDGE NOT DRAWN: motivo]' y entonces basta >= minimo; (2) U-177: por debajo de 'minimo' (0.5) = FAIL siempre, salvo que el texto
    declare la hoja que SÍ dibuja el contorno, 'source <HOJA> offset (dx, dy)', y ahí (restando el offset) la cobertura sea >= minimo;
    el borde compartido con otro polígono del take-off de la misma página cuenta como cubierto (límite entre dos cielos cargados);
    (3) en hojas A6 / A7 su vista es un RCP, no un PLAN. -> (fallas, n, stats)"""
    lab_pag = {(p.get_label() or "").strip(): p.number for p in doc}
    ev, n, covs = [], 0, []
    for p in doc:
        lab = (p.get_label() or "").strip()
        anns = [a for a in p.annots() or [] if a.type[1] == "Polygon" and (a.info.get("title") == "take-off" or a.info.get("subject") == "EXCLUDED")]
        if not anns:
            continue
        base = _segs_pagina(limpio[p.number] if limpio is not None else p)   # líneas del plano LIMPIO (el PDF de markups trae sus propios trazos)
        polis = [[[q[0], q[1]] for q in a.vertices] for a in anns]
        for k, a in enumerate(anns):
            v = polis[k]
            if len(v) < 3:
                continue
            n += 1
            nom = re.search(r"((?:CLG|SOF|RS6|CAN|BW)-[A-Z0-9.-]+)", str(a.info.get("content"))) or re.search(r"(EXCLUDED - .{0,40})", str(a.info.get("content")))
            nom = nom.group(1) if nom else a.info.get("subject")
            grid = {key: list(val) for key, val in base.items()}
            if a.info.get("title") == "take-off":
                for k2, w in enumerate(polis):                   # bordes de los OTROS cielos cargados de la página
                    if k2 == k or anns[k2].info.get("title") != "take-off":
                        continue
                    for i_ in range(len(w)):
                        sg = (w[i_][0], w[i_][1], w[(i_ + 1) % len(w)][0], w[(i_ + 1) % len(w)][1])
                        for gx in range(int(min(sg[0], sg[2]) // 20), int(max(sg[0], sg[2]) // 20) + 1):
                            for gy in range(int(min(sg[1], sg[3]) // 20), int(max(sg[1], sg[3]) // 20) + 1):
                                grid.setdefault((gx, gy), []).append(sg)
            cv = cobertura_borde(grid, v)
            txt = str(a.info.get("content"))
            exento = re.search(r"\[EDGE NOT DRAWN: ([^\]]{12,})\]", txt)   # borde que la hoja no dibuja, con motivo
            fuente = RX_FUENTE_POLI.search(txt)
            cvf = None
            if fuente and fuente.group(1) in lab_pag and limpio is not None:
                dx, dy = float(fuente.group(2)), float(fuente.group(3))
                cvf = cobertura_borde(_segs_pagina(limpio[lab_pag[fuente.group(1)]]), [[x - dx, y - dy] for x, y in v])
            mejor = max(cv, cvf or 0)
            covs.append(mejor)
            if mejor < minimo:                                       # U-177 (2) / BE-AUD02: por debajo del piso ni [EDGE NOT DRAWN] lo salva
                ev.append(f"{lab} {nom}: solo {cv:.0%} del contorno sobre líneas de la hoja"
                          + (f" y {cvf:.0%} sobre {fuente.group(1)} (offset {fuente.group(2)}, {fuente.group(3)})" if cvf is not None else "")
                          + f" (< {minimo:.0%}, piso U-177: ni con EDGE NOT DRAWN; declare 'source <HOJA> offset (dx, dy)' de la hoja que sí lo dibuja)")
            elif cv < umbral and not exento and (cvf is None or cvf < umbral):
                ev.append(f"{lab} {nom}: solo {cv:.0%} del contorno sobre líneas de la hoja (< {umbral:.0%}: ¿offset / vista equivocada?)")
            if re.match(r"A[67]\.", lab):
                cx, cy = sum(q[0] for q in v) / len(v), sum(q[1] for q in v) / len(v)
                t = vista_de(p, cx, cy)
                if t and re.search(r"(?i)\bPLAN\b", t) and not re.search(r"(?i)RCP|REFLECTED|CEILING", t):
                    ev.append(f"{lab} {nom}: dibujado en la vista '{t[:60]}' (PLAN), no en el RCP de la hoja")
    covs.sort()
    st = {"n": n, "min": round(covs[0], 2) if covs else None, "mediana": round(covs[len(covs) // 2], 2) if covs else None}
    return ev, n, st


@chequeo("CE_RCP_CONTORNO", ["U-159", "U-160", "U-177"], "rev15 (revisión completa rev14 F04 / F05): cada polígono de cielo y cada EXCLUDED coincide con las "
         "líneas de su hoja (cobertura de borde >= 60 %) y, en hojas ampliadas A6 / A7, cae en la vista RCP (no en la vista PLAN)")
def ce_rcp_contorno(c):
    if not (c.markups and os.path.isfile(c.markups)):
        return R("AMBER", "sin PDF de markups")
    import pymupdf as _f
    bs = c.cfg.get("bidset_limpio") or c.cfg.get("bidset")
    if not (bs and os.path.isfile(bs)):
        return R("FAIL", "sin bid set limpio (entrega.json bidset_limpio): no se puede medir el contorno contra las líneas de la hoja")
    ev, n, st = rcp_contorno_fallas(_f.open(c.markups), limpio=_f.open(bs))
    if not n:
        return R("AMBER", "sin polígonos de cielo en el PDF de markups")
    return R("FAIL", *ev[:25]) if ev else R("PASS", f"{n} polígonos de cielo / EXCLUDED sobre las líneas de su hoja y en su vista RCP {st}")


@chequeo("CE_RFI_BUSQUEDA_EXHAUSTIVA", ["U-140"], "U-140: un RFI 'not printed' abierto lleva la búsqueda completa: >= 12 términos "
         "con sinónimos, todas las disciplinas, SHX, medida vectorial a escala impresa, specs / addenda y sets de todos los GC")
def ce_rfi_busqueda(c):
    abiertos = c.rfis_abiertos()
    st = _json(c.set_p) or {}
    dis = sorted({re.match(r"[A-Z]+", k).group(0) for k in (st.get("hojas") or {}) if re.match(r"[A-Z]+\d", k)})
    ev, n = [], 0
    for rid, fila in abiertos:
        r = c.rfi(rid) or {}
        if not RX_NO_IMPRESO_RFI.search(fila + " " + str(r.get("pregunta") or "") + " " + str(r.get("motivo") or "")):
            continue
        n += 1
        ev += busqueda_exhaustiva(rid, r, dis)
    if ev:
        return R("FAIL", *ev[:20])
    return R("PASS", f"{n} RFI 'not printed' con búsqueda exhaustiva ({len(abiertos)} abiertos)")


@chequeo("CE_ATRIBUCION_ESTIMADOR", ["U-052"], "toda 'estimator decision' del Excel cita su respuesta escrita o precedente "
         "(R-ALC-NN, R80e.34, U-NNN, respuesta del usuario, standing rule)")
def ce_atribucion(c):
    wb = c.wb()
    if wb is None:
        return R("FAIL", "no hay Excel")
    rx_cita = re.compile(r"(?i)R-ALC-\d+|R80[a-z]\.\d+|U-\d{3}|BE-[A-Z0-9-]+|precedent|standing (?:rule|order)|user answer|"
                         r"respuesta|answered|recommended option|option \(?A\)?|20\d\d-\d\d-\d\d|\b\d{1,2}-(?:oct|nov|dec)\b")
    ev = []
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for cell in row:
                v = cell.value
                if isinstance(v, str) and re.search(r"(?i)estimator(?:'s)? decision|decisi[oó]n del estimador", v) and not rx_cita.search(v):
                    ev.append(f"{ws.title}!{cell.coordinate}: '{v[:90]}'")
    return R("FAIL", *ev[:15]) if ev else R("PASS", "toda decisión del estimador con cita")


@chequeo("CE_DECISIONES_EN_EXCEL", ["U-016", "U-050"], "todo RFI cerrado (por plano o por el estimador) queda escrito en el Excel")
def ce_decisiones(c):
    wb = c.wb()
    if wb is None:
        return R("FAIL", "no hay Excel")
    txt = " ".join(str(x) for ws in wb.worksheets for r in ws.iter_rows(values_only=True) for x in r if x)
    cerrados = [str(r.get("id")) for r in c.rfis() if RX_CERRADO.search(str(r.get("estado") or r.get("status") or ""))]
    cerrados += [str(k) for k in (c.tk.get("rfi_cierre") or {})]
    falta = []
    for k in cerrados:
        partes = [p.strip() for p in re.split(r"/", k) if p.strip()]
        if not any(re.search(r"(?<![\w-])" + re.escape(p) + r"(?![\w-])", txt) or
                   re.search(r"(?<![\w-])" + re.escape(re.sub(r"^[AB]-", "", p)) + r"(?![\w-])", txt) for p in partes):
            falta.append(k)
    return R("FAIL", *[f"{k}: cerrado pero no citado en el Excel" for k in falta]) if falta else \
        R("PASS", f"{len(cerrados)} cierres citados")


@chequeo("CE_SEGUIMIENTO", ["U-048"], "SEGUIMIENTO.md lista cada RFI abierto")
def ce_seguimiento(c):
    t = _leer(c.seg)
    if not t:
        return R("FAIL", "no hay SEGUIMIENTO.md en la entrega")
    falta = [rid for rid, _ in c.rfis_abiertos() if rid not in t]
    return R("FAIL", *[f"{x} no está en SEGUIMIENTO.md" for x in falta]) if falta else R("PASS", "RFI abiertos en SEGUIMIENTO")


def _escalas_pdf(pdf, canon):
    """{hoja: pt/ft} desde el rótulo SCALE IMPRESO de cada hoja marcada (si hay varios, el que coincide con el canon)."""
    import pymupdf
    import verificar_markups_excel as VME
    out, amb = {}, []
    doc = pymupdf.open(pdf)
    for p in doc:
        ans = list(p.annots() or [])
        if not ans or (p.get_label() or "").strip().upper() == "LEGEND" or all(str(a.info.get("subject") or "").upper() == "LEGEND" for a in ans):
            continue                                 # U-177: la hoja de leyenda (Subject LEGEND, BE-XF07) no mide: no pide escala
        lab = p.get_label() or f"p{p.number + 1}"
        imp = VME.escalas_impresas(p.get_text("text").replace("’", "'").replace("”", '"'))
        can, _ = VME.escala_canon(canon, lab)
        if len(imp) == 1:
            out[lab] = imp[0]
        elif can and any(abs(can - x) < 0.01 for x in imp):
            out[lab] = can
        elif can and not imp:
            out[lab] = can
            amb.append(f"{lab}: la hoja del PDF de markups no tiene capa de texto; escala tomada del canon ({can:.3f} pt/ft)")
        else:
            amb.append(f"{lab}: escalas impresas {imp}, canon {can}")
    return out, amb


@chequeo("CE_ALTURA_IMPRESA", ["U-099", "BE-119", "U-010", "U-088"], "BE-119: cada markup re-medido a la escala IMPRESA y su "
         "Depth comparado contra la altura IMPRESA de su fuente (N/HOJA), no contra el Excel. RED = FAIL; sin altura impresa = AMBER")
def ce_altura_impresa(c):
    if not (c.markups and c.excel):
        return R("FAIL", "falta el PDF de markups o el Excel")
    import revision_markups as RM
    sc_cfg = {k: RM.escala_pt_per_ft(v) for k, v in (c.cfg.get("escalas") or {}).items()}
    sc, amb = _escalas_pdf(c.markups, c.canon)
    sc.update(sc_cfg)
    _doc, _mk, res = RM.revisar(c.markups, c.excel, sc, c.canon)
    rojo = [f"{r['wall']}: {'; '.join(r['fallas'])}" for r in res if r["verdict"] == "RED"]
    # U-138 (auditoría 4-nov, Chuze): una altura cuya fuente no cita NINGUNA hoja = FAIL (no AMBER)
    rojo += [f"{r['wall']}: altura sin hoja citada ({'; '.join(a for a in r['amber'] if 'sheets cited none' in a)[:160]})"
             for r in res if r["verdict"] == "AMBER" and any("sheets cited none" in a for a in r["amber"])]
    amb_w = [f"{r['wall']}: {'; '.join(r['amber'])}" for r in res if r["verdict"] == "AMBER"
             and not any("sheets cited none" in a for a in r["amber"])]
    if rojo:
        return R("FAIL", f"{len(rojo)} RED / {len(amb_w)} AMBER de {len(res)}", *rojo, *amb)
    if amb_w or amb:
        return R("AMBER", f"0 RED / {len(amb_w)} AMBER de {len(res)}", *amb_w, *amb)
    return R("PASS", f"{len(res)} filas GREEN contra la altura impresa")


@chequeo("CE_MATERIALES_SCHEDULE", ["U-111", "BE-122"], "BE-122 (j): lectura INDEPENDIENTE del Partition Type Schedule "
         "(fichas.json, subagente que no vio el Excel) vs lo cargado por wall / type (revision_materiales.comparar_type) + cada "
         "renglón del Material Summary = suma de walls por type con origen impreso (revision_materiales.sumas). RED = FAIL")
def ce_materiales_schedule(c):
    import revision_materiales as RV
    fp = (os.path.join(c.w, c.cfg["fichas"]) if c.cfg.get("fichas") else None) or _ultimo(["fichas.json", "**/fichas.json"], c.w)
    fj = _json(fp)
    if not (fj and fj.get("types")):
        return R("FAIL", "no hay fichas.json (lectura independiente del Partition Type Schedule por un subagente que no vio "
                         "el Excel): sin ella no hay revisión de materiales no circular (BE-122)")
    if not (c.excel and c.canon_p):
        return R("FAIL", "falta Excel o canon")
    filas, ms = RV.leer_excel(c.excel)
    cw = {w["id"]: w for w in c.canon.get("walls") or []}
    misc = c.canon.get("misc_items") or []
    mapa = {k: (v if isinstance(v, list) else str(v).split(",")) for k, v in (c.cfg.get("mapa_materiales") or {}).items()}
    sel = lambda t: [f for f in filas if f["type"] in mapa.get(t, [t]) or f["wall"] in mapa.get(t, [])]  # noqa: E731
    res = [RV.comparar_type(t, fj["types"][t], sel(t), cw, misc) for t in fj["types"]]
    tnr = c.canon.get("types_none_reason") or {}
    for r in res:                                    # U-177: type del schedule sin tag en el plano, con motivo N/HOJA en el canon = GREEN
        if r["verdict"] == "AMBER" and [x["field"] for x in r["checks"]] == ["walls"] and RX_HOJA_CONCRETA.search(str(tnr.get(r["type"]) or "")):
            r["checks"][0].update(status="GREEN", note=f"types_none_reason: {str(tnr[r['type']])[:120]}")
            r["verdict"] = "GREEN"
    cub = {id(f) for t in fj["types"] for f in sel(t)}
    calc = c.cfg.get("calc_dir") and os.path.join(c.w, c.cfg["calc_dir"]) or os.path.join(os.path.dirname(c.canon_p), "out")
    sm = RV.sumas(ms, filas, calc)
    rojo = [f"type {r['type']}: " + "; ".join(f"{x['field']} schedule {x['schedule']} / Excel {x['excel']}" for x in r["checks"]
                                               if x["status"] == "RED") for r in res if r["verdict"] == "RED"]
    rojo += [f"Material Summary fila {s['row']} '{s['material'][:50]}': {s['note'][:120]}" for s in sm if s["status"] == "RED"]
    amb = [f"type {r['type']}: AMBER (el schedule no lo dice)" for r in res if r["verdict"] == "AMBER"]
    oa = " ".join(f"{k} {v.get('source', '') if isinstance(v, dict) else v}" for k, v in (fj.get("other_assemblies") or {}).items())
    cubre_oa = lambda f: bool(re.search(r"\b\d+/[A-Z]{1,2}\d{1,2}\.\d{1,2}\b", str((cw.get(f["wall"]) or {}).get("detail") or ""))) and \
        str((cw.get(f["wall"]) or {}).get("detail")) in oa          # noqa: E731  U-177: assembly fuera del schedule leído en other_assemblies (5/A2.0)
    amb += [f"walls fuera del schedule: {f['type']} {f['wall']}" for f in filas if id(f) not in cub and not cubre_oa(f)]
    amb += [f"Material Summary fila {s['row']} AMBER: {s['note'][:100]}" for s in sm if s["status"] == "AMBER"]
    if rojo:
        return R("FAIL", f"{len(rojo)} RED", *rojo[:25], *amb[:10])
    return R("AMBER", *amb[:25]) if amb else R("PASS", f"{len(res)} types y {len(sm)} renglones del Material Summary en verde")


@chequeo("CE_MARKUPS_EXCEL", ["U-010", "BE-117", "BE-44"], "verificar_markups_excel.py: TYPE·LF·H·SF·DETAIL·Wall ID = Excel, "
         "/Measure = escala impresa, Length vs LF <= 0.5 %")
def ce_markups_excel(c):
    if not (c.markups and c.excel and c.canon_p):
        return R("FAIL", "falta PDF de markups, Excel o canon")
    import verificar_markups_excel as VME
    fallas, _l, _r = VME.verificar(c.markups, c.excel, c.canon_p)
    return R("FAIL", f"{len(fallas)} fallas", *fallas[:25]) if fallas else R("PASS", "markups = Excel = escala impresa")


@chequeo("CE_AUDITORIA", ["U-005", "U-007", "U-011", "BE-42"], "auditoria_entrega.py: orden del schedule, SUBTOTAL por type, "
         "GRAND TOTAL, PNG por hoja marcada, PROJECT DATA, RFI abiertos con (A)/(B)/(C)")
def ce_auditoria(c):
    if not (c.markups and c.excel and c.canon_p):
        return R("FAIL", "falta PDF de markups, Excel o canon")
    import auditoria_entrega as AE
    res = AE.auditar(c.excel, c.markups, c.canon_p, imagenes=c.planos, docs=[c.readme, c.para], rfis_abiertos=True)
    malos = [f"{a} · {b} · {d}" for a, b, ok, d in res if not ok]
    return R("FAIL", f"{len(malos)} de {len(res)}", *malos[:25]) if malos else R("PASS", f"{len(res)} revisiones OK")


@chequeo("CE_REGLAS", ["U-009", "U-031", "U-083", "U-085", "R-ALC-11", "R-ALC-12", "BE-116"], "reglas.py compuerta en modo final "
         "(--excel): todas las compuertas A_* del catálogo (etapas, bitácora, no dibujado, strut, barrido, markups, ...)")
def ce_reglas(c):
    if not c.canon_p:
        return R("FAIL", "no hay takeoff_canon.json")
    d = os.path.dirname(os.path.dirname(c.canon_p)) if os.path.basename(os.path.dirname(c.canon_p)) == "4_canon" else os.path.dirname(c.canon_p)
    out = tempfile.mkdtemp(prefix="ce_reglas_")
    env = dict(os.environ)
    bit = _ultimo(["**/bitacora.jsonl"], c.w)
    if bit and not env.get("BITACORA"):
        env["BITACORA"] = bit
    if c.markups and not env.get("TAKEOFF_MARKUPS_PDF"):
        # R80f.31 (Chuze FINAL6): reglas.py A_MARKUPS_EXCEL must check the DELIVERED markups PDF (Planos marcados/), not
        # the newest *.pdf of 6_markups/ (there it took the walls-only intermediate, without the RCP ceilings -> 15 FAIL)
        env["TAKEOFF_MARKUPS_PDF"] = c.markups
    cmd = [sys.executable, os.path.join(AQUI, "reglas.py"), "compuerta", d, "--out", out] + (["--excel", c.excel] if c.excel else [])
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=1800, env=env)
    ro = _json(os.path.join(out, "reglas_out.json")) or {}
    if p.returncode == 0 and ro.get("ok"):
        return R("PASS", f"reglas.py OK ({ro.get('reglas')} reglas)")
    fs = [f"{f.get('regla')} · {f.get('elemento')} · {f.get('valor')}" for f in (ro.get("fallas") or [])[:20]]
    return R("FAIL", f"reglas.py rc {p.returncode}, {ro.get('n_fallas', '?')} fallas", *(fs or [(p.stdout + p.stderr)[-400:]]))



# ----------------------------------------------------------------------------------------------- U-130 comparativa con el banco
BANCO_VERSION = "comparativa_banco v1 (U-130, 4-nov-2026)"
# Referencias verificadas (rutas dentro de la rama claude/gifted-pasteur-x2sfzs; --cache <raíz del repo>). Floor SF = la fila
# 'Total SF' de Inputs del propio Excel (PROJECT DATA, con su hoja); sin ella la referencia solo entra en las razones por LF.
BANCO_REFS = [
    ("B&N Colorado Springs rev13", "cache_proyectos/barnes_noble/FINAL_FOR_REVIEW_2026-10-24_rev13/Take-off/Barnes_Noble_ColoradoSprings_Takeoff_FINAL_rev13.xlsx"),
    ("VS Downey rev17", "cache_proyectos/vs_downey/FINAL_FOR_REVIEW/rev17/Take-off/VS679_Downey_Takeoff_FINAL_rev17.xlsx"),
    ("HFT Loveland rev3", "cache_proyectos/harbor_freight_loveland/FINAL_FOR_REVIEW/Take-off/HFT_Loveland_Takeoff_FINAL_rev3.xlsx"),
    ("CFA River Point rev6", "cache_proyectos/cfa_riverpoint/FINAL_rev6/Take-off/CFA2284_RiverPoint_Takeoff_FINAL_rev6.xlsx"),
    ("O'Reilly Evans rev6", "cache_proyectos/oreilly_p2/REV6_FINAL_4nov/entrega/OReilly_Evans_Takeoff_FINAL_rev6.xlsx"),
]
FAMILIAS_BANCO = [   # (familia, unidad, regex del nombre del renglón del Material Summary, regex que lo excluye)
    ("Studs", "LF", r"(?i)\bstuds?\b", r"(?i)block|backing|header|jamb|kicker"),
    ("Track", "LF", r"(?i)\btrack\b", r"(?i)backing"),
    ("Gypsum / cement board", "SF", r"(?i)gypsum board|cement (?:backer )?board|glass[- ]mat|densarmor|densglass|sheathing", r"(?i)fastener|screw|tape|compound"),
    ("Joint compound", "LB", r"(?i)joint compound|taping compound", None),
    ("Joint tape", "LF", r"(?i)joint tape|\btape\b", r"(?i)mesh tape .*cement|sealant"),
    ("Trim / corner bead", "LF", r"(?i)corner bead|casing bead|\bj[- ]?(?:metal|trim|bead)|l[- ]bead|edge trim|\btrim\b", None),
    ("Bracing / blocking", "LF", r"(?i)bracing|bridging|blocking|C\.R\. channel", None),
]
BANCO_TOL = 0.5          # fuera de rango = razón < min / 1.5 o > max * 1.5 del banco


def _num(x):
    try:
        return float(str(x).replace(",", "")) if x not in (None, "") else None
    except ValueError:
        return None


def banco_leer(xlsx):
    """-> {familias: {fam: net}, lf: LF de partitions (filas de wall), sf_piso: Total SF de Inputs o None}"""
    import openpyxl
    wb = openpyxl.load_workbook(xlsx, data_only=True)
    fam = {f[0]: 0.0 for f in FAMILIAS_BANCO}
    if "Material Summary" in wb.sheetnames:
        for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True):
            if not r or not r[0] or _num(r[2] if len(r) > 2 else None) is None:
                continue
            nm, un, net = str(r[0]), str(r[1] or "").upper(), _num(r[2])
            if re.search(r"(?i)\bdemo(?:lition)?\b", nm):     # demolición: renglón aparte, no es material nuevo
                continue
            for f, u, rx, nx in FAMILIAS_BANCO:
                if u == un and re.search(rx, nm) and not (nx and re.search(nx, nm)):
                    fam[f] += net
                    break
    lf = 0.0
    if "Partition Takeoff" in wb.sheetnames:
        for r in wb["Partition Takeoff"].iter_rows(min_row=5, values_only=True):
            if r and len(r) > 2 and r[1] and isinstance(r[2], (int, float)) and not str(r[1]).upper().startswith(("SUBTOTAL", "TOTAL")):
                lf += float(r[2])
    sf = None
    if "Inputs" in wb.sheetnames:
        for r in wb["Inputs"].iter_rows(values_only=True):
            if r and r[0] and re.match(r"(?i)\s*(total sf|gross (?:floor )?area|square footage|building area)\b", str(r[0])):
                m = re.search(r"\d[\d,]*(?:\.\d+)?", str(r[1] or ""))
                if m:
                    sf = _num(m.group(0))
                    break
    return {"familias": fam, "lf": round(lf, 2), "sf_piso": sf}


def banco_comparar(xlsx, refs):
    """refs [(nombre, ruta)] -> (filas, fuera): por familia, razón por LF de partition y por mil SF de piso contra el rango del banco."""
    p = banco_leer(xlsx)
    rs = []
    for nm, rp in refs:
        if os.path.isfile(rp):
            d = banco_leer(rp)
            if d["lf"] > 0:
                rs.append((nm, d))
    filas, fuera = [], []
    for f, u, _rx, _nx in FAMILIAS_BANCO:
        v = p["familias"][f]
        r_lf = v / p["lf"] if p["lf"] else None
        r_sf = v / p["sf_piso"] * 1000 if p["sf_piso"] else None
        b_lf = [d["familias"][f] / d["lf"] for _, d in rs if d["familias"][f] > 0]
        b_sf = [d["familias"][f] / d["sf_piso"] * 1000 for _, d in rs if d["familias"][f] > 0 and d["sf_piso"]]
        est = "IN RANGE"
        if v > 0 and b_lf and r_lf is not None and (r_lf < min(b_lf) / (1 + BANCO_TOL) or r_lf > max(b_lf) * (1 + BANCO_TOL)):
            est = "OUT OF RANGE"
        elif v == 0 and b_lf:
            est = "OUT OF RANGE"            # el banco siempre lo trae y aquí es 0: explicar (EXCLUDED, no aplica)
        elif not b_lf:
            est = "NO BANK DATA"
        filas.append({"familia": f, "unidad": u, "net": round(v, 2), "por_lf": r_lf, "por_ksf": r_sf,
                      "banco_lf": (min(b_lf), max(b_lf)) if b_lf else None, "banco_ksf": (min(b_sf), max(b_sf)) if b_sf else None,
                      "estado": est})
        if est == "OUT OF RANGE":
            fuera.append(f)
    return p, rs, filas, fuera


def banco_md(xlsx, refs, salida):
    p, rs, filas, fuera = banco_comparar(xlsx, refs)
    f2 = lambda x: "-" if x is None else f"{x:,.3f}"                       # noqa: E731
    rg = lambda t: "-" if not t else f"{t[0]:,.3f} – {t[1]:,.3f}"        # noqa: E731
    L = [f"# COMPARATIVA_BANCO — {os.path.basename(xlsx)}", "",
         f"Program: {BANCO_VERSION}. Excel sha256 {_sha(xlsx)}.",
         f"Project: partition LF {p['lf']:,.2f}; floor SF {p['sf_piso'] if p['sf_piso'] else 'not in Inputs (per-LF ratios only)'}.",
         "Bank (verified FINALs): " + "; ".join(f"{n} (LF {d['lf']:,.0f}, floor SF {d['sf_piso'] or '-'})" for n, d in rs) + ".",
         f"Out of range = ratio per partition LF below bank min / {1 + BANCO_TOL:g} or above bank max x {1 + BANCO_TOL:g}, or 0 where every bank job has it.",
         "Every OUT OF RANGE family must be explained in README_REVIEW.md (section 'Bank comparison'): scope, building type, standing order.", "",
         "| Family | Unit | Net | per partition LF | Bank range per LF | per 1,000 SF floor | Bank range per 1,000 SF | Status |",
         "|---|---|---|---|---|---|---|---|"]
    L += [f"| {r['familia']} | {r['unidad']} | {r['net']:,.2f} | {f2(r['por_lf'])} | {rg(r['banco_lf'])} | {f2(r['por_ksf'])} | {rg(r['banco_ksf'])} | {r['estado']} |"
          for r in filas]
    L += ["", "OUT OF RANGE: " + (", ".join(fuera) if fuera else "none")]
    _escribir(salida, "\n".join(L) + "\n")
    return fuera


def copia_limpia(orig, limpio, dpi=12, tol=0.005):
    """U-051 / BE-CF24 (CFA rev9): la copia limpia (sin markups previos) no pierde CONTENIDO del original: mismas páginas, mismos
    XObjects por página, ningún XObject faltante que el original sí tenga, y el render sin anotaciones igual (<= tol de píxeles
    distintos). Un XObject que falta también en el original es un defecto del archivo del arquitecto, no de la copia.
    -> (fallas, resumen)"""
    import pymupdf
    pymupdf.TOOLS.mupdf_display_errors(False)
    A, B = pymupdf.open(orig), pymupdf.open(limpio)
    fallas = []
    if A.page_count != B.page_count:
        return [f"páginas: original {A.page_count} / copia {B.page_count}"], {}
    falt_o, falt_c = 0, 0
    for i in range(A.page_count):
        pa, pb = A[i], B[i]
        xa, xb = {x[1] for x in pa.get_xobjects()}, {x[1] for x in pb.get_xobjects()}
        if xa - xb:
            fallas.append(f"p{i + 1}: XObjects del original que la copia no tiene: {sorted(xa - xb)[:5]}")
        res = []
        for pg in (pa, pb):
            pymupdf.TOOLS.reset_mupdf_warnings()
            pix = pg.get_pixmap(dpi=dpi, annots=False)
            w = pymupdf.TOOLS.mupdf_warnings()
            res.append((pix, {x.split("'")[1] for x in w.splitlines() if "XObject resource" in x and "'" in x}))
        (ia, wa), (ib, wb) = res
        falt_o += len(wa)
        falt_c += len(wb)
        if wb - wa:
            fallas.append(f"p{i + 1}: XObjects faltantes solo en la copia: {sorted(wb - wa)[:5]}")
        if ia.samples != ib.samples:
            n = sum(1 for a, b in zip(ia.samples, ib.samples) if abs(a - b) > 40)
            if n / max(1, len(ia.samples)) > tol:
                fallas.append(f"p{i + 1}: render distinto del original ({n / len(ia.samples):.2%} de píxeles)")
    return fallas, {"paginas": A.page_count, "xobjects_faltantes_original": falt_o, "xobjects_faltantes_copia": falt_c}


@chequeo("CE_COPIA_LIMPIA", ["U-051", "BE-CF24"], "U-051: la copia limpia del bid set (sin markups previos) tiene el mismo contenido que "
         "el original, hoja por hoja (páginas, XObjects, render sin anotaciones); entrega.json declara bidset_original y bidset_limpio")
def ce_copia_limpia(c):
    o, l_ = c.cfg.get("bidset_original"), c.cfg.get("bidset_limpio")
    if not (o and l_ and os.path.isfile(o) and os.path.isfile(l_)):
        return R("FAIL", "entrega.json sin bidset_original / bidset_limpio (rutas que existan): no se puede probar que la copia limpia no perdió contenido")
    fallas, res = copia_limpia(o, l_)
    if fallas:
        return R("FAIL", f"{len(fallas)} diferencia(s) de contenido", *fallas[:15])
    return R("PASS", f"{res['paginas']} páginas = original (XObjects faltantes: original {res['xobjects_faltantes_original']}, "
                     f"copia {res['xobjects_faltantes_copia']}, todos también en el original)")


@chequeo("CE_COMPARATIVA_BANCO", ["U-130"], "U-130: COMPARATIVA_BANCO.md (compuerta_entrega.py banco) del Excel entregado contra las "
         "referencias verificadas del banco, familias normalizadas por LF de partition y por SF de piso; toda familia OUT OF RANGE "
         "explicada en README_REVIEW.md (sección 'Bank comparison')")
def ce_comparativa_banco(c):
    p = _ultimo(["COMPARATIVA_BANCO.md", "**/COMPARATIVA_BANCO.md"], c.w)
    t = _leer(p)
    if not t:
        return R("FAIL", "no hay COMPARATIVA_BANCO.md: correr `compuerta_entrega.py banco <workdir> --cache <raíz del repo>` (U-130)")
    if not c.excel or _sha(c.excel) not in t:
        return R("FAIL", "COMPARATIVA_BANCO.md es de otro Excel (sha256 distinto): volver a correr `compuerta_entrega.py banco`")
    m = re.search(r"OUT OF RANGE: (.+)", t)
    fuera = [] if not m or m.group(1).strip() == "none" else [x.strip() for x in m.group(1).split(",")]
    rd = _leer(c.readme)
    sec = rd.split("Bank comparison", 1)[1] if "Bank comparison" in rd else ""
    falta = [f for f in fuera if not re.search(re.escape(f.split(" /")[0]), sec, re.I)]
    if falta:
        return R("FAIL", *[f"{f}: OUT OF RANGE sin explicación en README_REVIEW.md 'Bank comparison'" for f in falta])
    return R("PASS", f"{len(fuera)} familia(s) fuera de rango explicadas" if fuera else "todas las familias dentro del rango del banco")


# ----------------------------------------------------------------------------------------------- biblioteca de errores

@chequeo("CE_SUBIDA_PAQUETE", ["BE-CR28", "BE-140"], "BE-CR28: entrega con más de 1,000 archivos = subir_entrega sube Auditoria/ como "
         "Auditoria.zip (desde los archivos verificados) y README_REVIEW.md lo dice; sin esa línea = FAIL")
def ce_subida_paquete(c):
    if not c.entrega:
        return R("FAIL", "no hay carpeta de entrega")
    n = sum(len(fs) for _, _, fs in _walk_seguro(c.entrega))   # BE-GK35
    if n <= 1000:
        return R("PASS", f"{n} archivos: subida archivo por archivo")
    txt = open(c.readme, encoding="utf-8").read() if os.path.isfile(c.readme) else ""
    if "Auditoria.zip" not in txt:
        return R("FAIL", f"{n} archivos (> 1,000): subir_entrega sube Auditoria/ como Auditoria.zip; README_REVIEW.md debe explicarlo (BE-CR28)")
    return R("PASS", f"{n} archivos: Auditoria/ va como Auditoria.zip y README_REVIEW.md lo dice")


# ----------------------------------------------------------------------------------------------- U-151 / BE-147 PDF editable
# U-151 (6-nov, CR City Hotel rev3, BE-147; usuario: "como le hago para hacer los page level, el icono esta desactivado, esta en
# mark up mode y no hay ningun candado"): todo PDF de Planos marcados va SIN firmas digitales (campos /FT /Sig en /Annots y en
# AcroForm, /SigFlags, /Perms) y con Page Labels = hoja, uno por página, únicos, ninguno puramente numérico salvo que la hoja
# lo imprima así (entrega.json "page_labels_numericos_impresos": ["1", ...]). Arreglo: tools/quitar_firmas_labels.py.
# U-152 / BE-148 (v81cf59, CR City Hotel rev3c; usuario: "0.125 es correcto ?"): toda página con markups /Measure lleva /VP
# (escala de PÁGINA) cuyo /Measure /R = el de sus markups; sin /VP Bluebeam mostraba 0.125 en hojas a 1/4". Arreglo:
# tools/escala_pagina.py (markups_bluebeam.escribir ya lo llama solo).
def _es_sig(o, prof=0):
    """campo / widget de firma: /FT /Sig propio o heredado del /Parent."""
    try:
        while o is not None and prof < 20:
            if str(o.get("/FT")) == "/Sig":
                return True
            o, prof = o.get("/Parent"), prof + 1
    except Exception:                                                   # noqa: BLE001
        return False
    return False


def _campos(fields, prof=0):
    for f in list(fields or []):
        yield f
        if prof < 20 and f.get("/Kids") is not None:
            yield from _campos(f.get("/Kids"), prof + 1)


def pdf_editable(path, numericos_ok=()):
    """U-151 -> (faltas, info). faltas vacía = el PDF se puede editar en Bluebeam (Page Labels, insertar / quitar páginas)."""
    import pikepdf
    import pypdf
    faltas, numericos_ok = [], {str(x) for x in numericos_ok or ()}
    pdf = pikepdf.open(path)
    n = len(pdf.pages)
    sig_annots = sum(1 for i, pg in enumerate(pdf.pages) for a in (pg.obj.get("/Annots") or []) if _es_sig(a))
    af = pdf.Root.get("/AcroForm")
    sig_campos = sum(1 for f in _campos(af.get("/Fields") if af is not None else None) if _es_sig(f))
    firmadas = sum(1 for f in _campos(af.get("/Fields") if af is not None else None) if _es_sig(f) and f.get("/V") is not None)
    if sig_annots or sig_campos:
        faltas.append(f"{max(sig_annots, sig_campos)} campo(s) de firma digital /Sig ({sig_annots} en /Annots, {sig_campos} en "
                      f"AcroForm, {firmadas} firmado(s)): Bluebeam bloquea Page Labels y páginas")
    if af is not None and "/SigFlags" in af:
        faltas.append(f"AcroForm /SigFlags {af.get('/SigFlags')}")
    if "/Perms" in pdf.Root:
        faltas.append("/Perms en el catálogo (permisos de firma)")
    tiene_labels = "/PageLabels" in pdf.Root
    pdf.close()
    labs = []
    if not tiene_labels:
        faltas.append(f"sin /PageLabels: las {n} páginas quedan con número de página, no con la hoja")
    else:
        r = pypdf.PdfReader(path)
        labs = [str(r.page_labels[i]).strip() for i in range(n)]
        vac = [i + 1 for i, l in enumerate(labs) if not l]
        if vac:
            faltas.append(f"{len(vac)} página(s) sin Page Label: p{vac[:10]}")
        import collections
        dup = {k: v for k, v in collections.Counter(l for l in labs if l).items() if v > 1}
        if dup:
            faltas.append(f"{sum(dup.values())} páginas con Page Label repetido: {sorted(dup)[:10]}")
        num = [(i + 1, l) for i, l in enumerate(labs) if re.fullmatch(r"\d+", l) and l not in numericos_ok]
        if num:
            faltas.append(f"{len(num)} de {n} páginas con Page Label puramente numérico (no es la hoja): "
                          + ", ".join(f"p{p}='{l}'" for p, l in num[:8]))
    # U-152 / BE-148 (v81cf59): toda página con markups /Measure lleva escala de PÁGINA /VP con el mismo /R que sus markups
    import escala_pagina
    fe, ie = escala_pagina.revisar(path)
    faltas += [f"escala de página (U-152): {x}" for x in fe]
    return faltas, {"paginas": n, "firmas": max(sig_annots, sig_campos), "labels_unicos": len(set(labs)), "labels": labs,
                    "paginas_escala": ie["paginas_con_medida"], "escalas": ie["por_pagina"], "markups_medida": ie["markups_medida"]}


@chequeo("CE_PDF_EDITABLE", ["U-151", "BE-147", "U-152", "BE-148"], "U-151 / BE-147: todo PDF de Planos marcados sin firmas digitales "
         "(/Sig, /SigFlags, /Perms) y con Page Label = hoja en cada página (únicos, no numéricos salvo hoja impresa así); U-152 / "
         "BE-148: toda página con markups /Measure con escala de página /VP del mismo /R que sus markups")
def ce_pdf_editable(c):
    pdfs = sorted(glob.glob(os.path.join(c.planos, "*.pdf"))) if getattr(c, "planos", None) else []
    if not pdfs:
        return R("FAIL", "0 PDF en Planos marcados/ (U-137: el chequeo no pasa en vacío)")
    ok_num = ((getattr(c, "cfg", None) or {}).get("page_labels_numericos_impresos") or [])
    malos, buenos = [], []
    for p in pdfs:
        try:
            fs, info = pdf_editable(p, ok_num)
        except Exception as e:                                          # noqa: BLE001
            fs, info = [f"no se pudo leer: {type(e).__name__}: {e}"], {"paginas": 0}
        if fs:
            malos += [f"{os.path.basename(p)}: {x}" for x in fs]
        else:
            buenos.append(f"{os.path.basename(p)}: {info['paginas']} páginas, 0 firmas, {info['labels_unicos']} Page Labels únicos, "
                          f"{info.get('paginas_escala', 0)} página(s) con markups /Measure y su /VP del mismo /R")
    if malos:
        return R("FAIL", *(malos + ["arreglo: python3 -I tools/quitar_firmas_labels.py <pdf> <salida.pdf> <inventario.json> y "
                                    "python3 -I tools/escala_pagina.py <salida.pdf> <final.pdf>"]))
    return R("PASS", *buenos)


# ----------------------------------------------------------------------------------------------- U-153 / BE-149 vista Bluebeam
# U-153 (6-nov, BE-149; usuario, tras encontrar él mismo en Bluebeam el Wall Area x864: "ya esta, pero yo no puedo cachar todo,
# haz algo para no halla errores please" / "siempre tienes hacerlo en todos los proyectos, regla inviolable"): la compuerta
# SIMULA el Markups List de Bluebeam (Subject, Page Label, Length, Area, Wall Area, Depth) para CADA markup de cada PDF de
# Planos marcados y lo compara contra el Excel y contra su propia etiqueta. Bluebeam: Length = Σ segmentos de /Vertices x
# /Measure /X /C; Area (polígono) = shoelace x C² x /A /C; Depth = /Depth; Wall Area = Length x Depth / DepthUnit /C (con /C
# 1/864 salía x864). Cualquier diferencia = FAIL con lista; 0 markups revisados = FAIL (U-137). Deja VISTA_BLUEBEAM.csv.
VB_TOL = 0.005               # tolerancia relativa de largo y área (BE-117)
VB_ABS = 0.02                # redondeo de Bluebeam (2 decimales)
VB_TOL_H = 0.01 + 1.0 / 192  # 1/8" en ft-in
VB_COLS = ["PDF", "Page", "Page Label", "Subject", "Wall ID", "Markup", "Length (ft)", "Area (sf)", "Wall Area (sf)", "Depth (ft)",
           "DepthUnit C", "Measure R", "Page VP R", "Label LF", "Label H (ft)", "Label SF wall", "Label SF", "Excel row",
           "Expected Page Label", "Expected LF", "Expected H (ft)", "Expected Wall Area LFxH (sf)", "Expected Area (sf)",
           "Status", "Problems"]
RX_SF_WALL = re.compile(r"(?<![\w.])(\d[\d,]*(?:\.\d+)?)\s*SF wall\b")


def _escribir(ruta, texto):
    """BE-157: escribe un archivo nuevo y lo pone en su lugar con os.replace: si la entrega es una copia con hard links de una
    entrega ya subida, el original no cambia (rev18: la simulación reescribió Auditoria/VISTA_BLUEBEAM.csv del original)."""
    tmp = ruta + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(texto)
    os.replace(tmp, ruta)


def _nm_leer(nm):
    """U-167: /NM escrito con markups_bluebeam.nm_seguro (sin '/') -> llave original."""
    for a_, b_ in (("%5C", "\\"), ("%2F", "/"), ("%25", "%")):
        nm = nm.replace(a_, b_)
    return nm


def _vb_f(x):
    try:
        return float(x)
    except Exception:                                                   # noqa: BLE001
        return None


def _vb_c(nf_arr, defecto=None):
    """/C del primer NumberFormat de un arreglo (/X, /A, /DepthUnit)."""
    try:
        return float(nf_arr[0].get("/C"))
    except Exception:                                                   # noqa: BLE001
        return defecto


def _vb_ok(a, b, rel=VB_TOL, ab=VB_ABS):
    return a is not None and b is not None and abs(a - b) <= max(ab, rel * abs(b))


def _vb_hojas_canon(canon):
    """{id: hoja} de la geometría del canon (walls / existing_walls band.sheet, ceilings sheet, demo_geom sheet)."""
    out = {}
    can = canon if isinstance(canon, dict) else (_json(canon) if canon else None) or {}
    rcp = (can.get("constants") or {}).get("rcp_sheet")
    rcp = rcp.get("value") if isinstance(rcp, dict) else rcp
    for k in ("walls", "existing_walls", "demo_geom", "ceilings"):
        for e in can.get(k) or []:
            if not isinstance(e, dict):
                continue
            h = ((e.get("band") or {}).get("sheet") if isinstance(e.get("band"), dict) else None) or e.get("sheet") \
                or (rcp if k == "ceilings" else None)
            for i_ in (e.get("id"), e.get("room") if k == "ceilings" else None):
                if i_ and h:
                    out.setdefault(str(i_), str(h))
    return out


def vista_bluebeam(pdf, xlsx, canon=None):
    """U-153 -> (filas [dict VB_COLS], fallas [str], info). Simula el Markups List de Bluebeam para cada markup con /Measure del
    take-off (TO-* / DEMO-*; la leyenda TO-LEGEND-* no mide) y lo cuadra contra el Excel (Partition Takeoff por Wall #, o el
    desglose 'ID valor' del Material Summary) y contra su etiqueta."""
    import pikepdf
    import pypdf
    import verificar_markups_excel as VME
    ex = VME.leer_excel(xlsx)
    hojas_c = _vb_hojas_canon(canon)
    fallas = [f"Excel: {e}" for e in ex["errores"]]
    labels = []
    try:
        r_ = pypdf.PdfReader(pdf)
        labels = [str(r_.page_labels[i]).strip() for i in range(len(r_.pages))]
    except Exception as e:                                              # noqa: BLE001
        fallas.append(f"Page Labels ilegibles: {type(e).__name__}: {e}")
    import pymupdf
    dtxt = pymupdf.open(pdf)
    doc = pikepdf.open(pdf)
    filas, grupos = [], {}
    for i, page in enumerate(doc.pages):
        vps = []
        for vp in page.obj.get("/VP") or []:
            try:
                vps.append(([float(v) for v in vp.get("/BBox")], str(vp.get("/Measure").get("/R")).strip()))
            except Exception:                                           # noqa: BLE001
                pass
        for a in page.obj.get("/Annots") or []:
            try:
                m = a.get("/Measure")
            except Exception:                                           # noqa: BLE001
                continue
            nm = _nm_leer(str(a.get("/NM") or ""))
            if m is None or nm.startswith("TO-LEGEND-") or not nm.startswith(("TO-", "TOX-", "DEMO-")):
                continue
            st = str(a.get("/Subtype") or "").lstrip("/")
            subj = str(a.get("/Subj") or "").strip()
            cont = str(a.get("/Contents") or "")
            v = [float(x) for x in (a.get("/Vertices") or [])]
            pts = list(zip(v[0::2], v[1::2]))
            xc = _vb_c(m.get("/X"))
            ac = _vb_c(m.get("/A"), 1.0)
            rr = str(m.get("/R") or "").strip()
            prob = []
            if xc is None:
                prob.append("/Measure sin /X /C (Bluebeam no mide)")
                xc = 0.0
            lpt = sum(math.dist(pts[k], pts[k + 1]) for k in range(len(pts) - 1))
            area = None
            if st == "Polygon" and len(pts) >= 3:
                lpt += math.dist(pts[-1], pts[0])
                q = pts + [pts[0]]
                area = abs(sum(q[k][0] * q[k + 1][1] - q[k + 1][0] * q[k][1] for k in range(len(q) - 1))) / 2.0 * xc * xc * ac
            length = lpt * xc
            depth = _vb_f(a.get("/Depth")) if a.get("/Depth") is not None else None
            du = _vb_c(a.get("/DepthUnit"), 1.0) if a.get("/DepthUnit") is not None else (1.0 if depth is not None else None)
            wa = length * depth / du if depth is not None and du else None
            if depth is not None and (du is None or abs(du - 1.0) > 1e-9):
                prob.append(f"DepthUnit /C {du:g}: Bluebeam muestra Wall Area x{1 / du:g} (U-153 / BE-149: tiene que ser /C 1)"
                            if du else "DepthUnit /C 0")
            # escala de página: el ÚLTIMO /VP que contiene el markup (ISO 32000 12.9) tiene que traer la misma /R
            try:
                rc = [float(x) for x in a.get("/Rect")]
                cx, cy = (rc[0] + rc[2]) / 2.0, (rc[1] + rc[3]) / 2.0
            except Exception:                                           # noqa: BLE001
                cx = cy = None
            vpr = next((r for bb, r in reversed(vps) if cx is not None and min(bb[0], bb[2]) <= cx <= max(bb[0], bb[2])
                        and min(bb[1], bb[3]) <= cy <= max(bb[1], bb[3])), None)
            if vpr != rr:
                prob.append(f"escala de página /VP '{vpr}' != /Measure /R '{rr}' (U-152)")
            if not subj:
                prob.append("Subject vacío")
            lab = labels[i] if i < len(labels) else ""
            P = VME.parse_contents(subj, cont, nm)
            wid = P["id"]
            msw = RX_SF_WALL.search(cont)
            sf_wall = float(msw.group(1).replace(",", "")) if msw else None
            es_demo = nm.startswith("DEMO-") or subj.upper() == "DEMO"
            if depth is not None:
                if sf_wall is None and es_demo and P["sf"] is not None:
                    sf_wall = P["sf"]                    # U-143: la demo rotula SF = LF x H del elemento
                if sf_wall is None:
                    prob.append("etiqueta sin '<LF x H> SF wall' (U-153: el Wall Area de Bluebeam no se ve en la etiqueta)")
                elif not _vb_ok(wa, sf_wall):
                    prob.append(f"Wall Area {wa:,.2f} != etiqueta {sf_wall:,.2f} SF wall")
                if P["h"] is not None and abs(depth - P["h"]) > VB_TOL_H:
                    prob.append(f"Depth {depth:g} != etiqueta H {P['h_s']}")
            if P["lf"] is not None and st != "Polygon" and not _vb_ok(length, P["lf"]):
                prob.append(f"Length {length:.2f} != etiqueta {P['lf_s']} LF")
            if area is not None and P["sf"] is not None and depth is None and not _vb_ok(area, P["sf"]):
                prob.append(f"Area {area:,.2f} != etiqueta {P['sf_s']} SF")
            # renglón del Excel
            key, row, exp = None, "", {}
            if wid:
                pt, union = ex["pt"].get(wid), ex.get("union", {}).get(wid)
                if pt:
                    key, f0 = wid, pt[0]
                    row = f"Partition Takeoff fila {f0['fila']}" + (f" (+{len(pt) - 1} renglones con el mismo Wall #)" if len(pt) > 1 else "")
                    exp = {"lf": f0["lf"], "h": f0["h"], "texto": f0["texto"], "pt": True}
                elif union:
                    f0 = ex["pt"][union][0]
                    key, row = union, f"Partition Takeoff fila {f0['fila']} (parte de {union})"
                    exp = {"lf": f0["lf"], "h": f0["h"], "texto": f0["texto"], "pt": True}
                else:
                    hits = VME.buscar_ms(ex, wid)
                    base = wid.split()[0]
                    if not hits and base != wid:
                        hits, wid_k = VME.buscar_ms(ex, base), base
                    else:
                        wid_k = wid
                    if hits:
                        ms_, val = next(((m_, v_) for m_, v_ in hits if VME.tipo_ok(subj, m_["material"])), hits[0])
                        key, row = f"MS:{wid_k}:{ms_['fila']}", f"Material Summary fila {ms_['fila']} ({wid_k} {val} {ms_['unit']})"
                        exp = {"ms_val": val, "unit": ms_["unit"], "texto": ms_["where"], "pt": False}
            if not key:
                prob.append(f"Wall ID {wid or '(sin id)'} sin renglón en el Excel (Partition Takeoff ni Material Summary)")
            # Page Label = hoja del renglón: la del canon; si no, una hoja citada en el renglón; si no, el title block de la página
            esp = hojas_c.get(wid or "") or hojas_c.get((wid or "").split("~")[0]) or hojas_c.get((wid or "").split(" ")[0])
            if esp:
                esp_s = esp
                if lab != esp:
                    prob.append(f"Page Label '{lab}' != hoja del renglón '{esp}' (canon)")
            else:
                txt_ = str(exp.get("texto") or "")
                cit = sorted({x.split("/")[-1] for x in VME.citas(txt_)} | set(VME.PLANO_RX.findall(txt_)))
                tb = dtxt[i].get_text("text") if i < dtxt.page_count else ""
                if lab and lab in cit:
                    esp_s = lab
                elif lab and RX_HOJA_TB.match(lab) and re.search(r"(?<![\w.])" + re.escape(lab) + r"(?![\w.])", tb):
                    esp_s = f"{lab} (title block)"
                else:
                    esp_s = "?"
                    prob.append(f"Page Label '{lab}' no es la hoja impresa de la página ni una hoja del renglón")
            d = {"PDF": os.path.basename(pdf), "Page": i + 1, "Page Label": lab, "Subject": subj, "Wall ID": nm, "Markup": st,
                 "Length (ft)": round(length, 2), "Area (sf)": round(area, 2) if area is not None else "",
                 "Wall Area (sf)": round(wa, 2) if wa is not None else "", "Depth (ft)": depth if depth is not None else "",
                 "DepthUnit C": du if du is not None else "", "Measure R": rr, "Page VP R": vpr or "",
                 "Label LF": P["lf_s"] or "", "Label H (ft)": round(P["h"], 4) if P["h"] is not None else "",
                 "Label SF wall": sf_wall if sf_wall is not None else "", "Label SF": P["sf_s"] or "", "Excel row": row,
                 "Expected Page Label": esp_s, "Expected LF": "", "Expected H (ft)": "", "Expected Wall Area LFxH (sf)": "",
                 "Expected Area (sf)": "", "_prob": prob, "_len": length, "_wa": wa, "_area": area, "_depth": depth, "_exp": exp,
                 "_capas": (int(re.search(r"board = (\d+) layer\(s\) x drawn area", cont).group(1)) if re.search(r"board = (\d+) layer\(s\) x drawn area", cont) else 1)
                 * (float(re.search(r"slope factor (\d+\.?\d*)", cont).group(1)) if re.search(r"slope factor (\d+\.?\d*)", cont) else 1)}
            filas.append(d)
            if key:
                grupos.setdefault(key, []).append(d)
    # cuadre por renglón del Excel (los tramos de un wall y las piezas de un renglón unido se suman)
    for key, ds in grupos.items():
        exp = ds[0]["_exp"]
        L = sum(x["_len"] for x in ds)
        msg = []
        if exp.get("pt"):
            lf_, h_ = exp.get("lf"), exp.get("h")
            if lf_ is not None:
                for x in ds:
                    x["Expected LF"] = lf_
                if not _vb_ok(L, lf_):
                    msg.append(f"Length {L:.2f} != Excel LF {lf_} ({(L / lf_ - 1) * 100 if lf_ else 0:+.2f} %)")
            if h_ is not None:
                for x in ds:
                    x["Expected H (ft)"] = h_
                    if x["_depth"] is not None and abs(x["_depth"] - h_) > VB_TOL_H and len(ds) == 1:
                        msg.append(f"Depth {x['_depth']:g} != Excel H {h_}")
            if len(ds) > 1 and h_ is not None and all(x["_depth"] is not None for x in ds) and L:
                hp = sum(x["_len"] * x["_depth"] for x in ds) / L
                if abs(hp - h_) > VB_TOL_H:
                    msg.append(f"Depth ponderado {hp:.3f} != Excel H {h_}")
            if lf_ is not None and h_ is not None and all(x["_wa"] is not None for x in ds):
                wa_e = lf_ * h_
                wa_s = sum(x["_wa"] for x in ds)
                for x in ds:
                    x["Expected Wall Area LFxH (sf)"] = round(wa_e, 2)
                if not _vb_ok(wa_s, wa_e):
                    msg.append(f"Wall Area {wa_s:,.2f} != Excel LF x H {wa_e:,.2f} (factor {wa_s / wa_e if wa_e else 0:.3f})")
        else:
            val, unit = exp.get("ms_val"), exp.get("unit")
            if unit == "SF":
                # rev7 (v81cf63): un cielo de N capas se dibuja con su área; el renglón del Excel es board SF = área x N capas
                tot = sum(((x["_area"] * x.get("_capas", 1)) if x["_area"] is not None else x["_wa"]) or 0.0 for x in ds)
                for x in ds:
                    x["Expected Area (sf)"] = val
                if not _vb_ok(tot, val):
                    msg.append(f"{'Area' if ds[0]['_area'] is not None else 'Wall Area'} {tot:,.2f} != Excel {val} SF")
            elif unit == "LF":
                for x in ds:
                    x["Expected LF"] = val
                if not _vb_ok(L, val):
                    msg.append(f"Length {L:.2f} != Excel {val} LF")
        for x in ds:
            x["_prob"] += msg
    for d in filas:
        d["Status"] = "FAIL" if d["_prob"] else "OK"
        d["Problems"] = "; ".join(dict.fromkeys(d["_prob"]))
        if d["_prob"]:
            fallas.append(f"{d['PDF']} p.{d['Page']} {d['Page Label']} {d['Wall ID']}: {d['Problems']}")
    if not filas:
        fallas.append(f"{os.path.basename(pdf)}: 0 markups con /Measure revisados (U-137: el chequeo no pasa en vacío)")
    info = {"markups": len(filas), "ok": sum(1 for d in filas if d["Status"] == "OK"), "renglones": len(grupos),
            "paginas": len({d["Page"] for d in filas})}
    doc.close()
    dtxt.close()
    return [{k: d[k] for k in VB_COLS} for d in filas], fallas, info


def vista_csv(filas, salida):
    import csv
    os.makedirs(os.path.dirname(os.path.abspath(salida)), exist_ok=True)
    tmp = salida + ".tmp"                 # BE-157: archivo nuevo + os.replace; nunca se escribe dentro de un inode compartido
    with open(tmp, "w", newline="", encoding="utf-8-sig") as f:   # (una copia con hard links de una entrega ya subida)
        w = csv.DictWriter(f, fieldnames=VB_COLS)
        w.writeheader()
        w.writerows(filas)
    os.replace(tmp, salida)
    return salida


def _pdfs_markups(c):
    """PDF de Planos marcados con markups del take-off (DETALLES_REVISADOS / SCHEDULES_REVISADOS no miden)."""
    return [p for p in sorted(glob.glob(os.path.join(c.planos, "*.pdf"))) if getattr(c, "planos", None)
            and not os.path.basename(p).startswith(("DETALLES_REVISADOS", "SCHEDULES_REVISADOS", "ALTURAS_REVISADAS"))
            and "NO USAR" not in os.path.basename(p)]


def subject_sin_medida_fallas(pdf, xlsx=None, tipos=None):
    """BE-XF07 (Xfinity Interquest rev1, COORDINACIÓN 10-nov): todo markup cuyo Subject es un type del Partition Takeoff o DEMO
    lleva /Measure y cae en una página con /VP; si no, Bluebeam lo suma al grupo del type en la Markups List / CSV (W2 3 en vez
    de 2) sin Length ni Depth. Las muestras de la leyenda van con Subject LEGEND. -> [fallas]"""
    import pymupdf as _f
    ts = set(tipos or [])
    if not ts and xlsx:
        try:
            import openpyxl
            ws = openpyxl.load_workbook(xlsx, data_only=True)["Partition Takeoff"]
            ts = {str(r[0]).strip()[5:].strip() for r in ws.iter_rows(values_only=True) if r and str(r[0] or "").strip().upper().startswith("TYPE ")}
        except Exception:
            ts = set()
    ts |= {"DEMO"}
    ev = []
    d = _f.open(pdf)
    for i, pg in enumerate(d):
        vp = d.xref_get_key(pg.xref, "VP")[0] != "null"
        for a in pg.annots() or []:
            sj = str(a.info.get("subject") or "").strip()
            if sj not in ts and not any(sj.startswith(t + " ") for t in ts):
                continue
            sin_m = d.xref_get_key(a.xref, "Measure")[0] == "null"
            if sin_m or not vp:
                ev.append(f"página {pg.get_label() or i + 1}: markup Subject '{sj}' "
                          f"{'sin /Measure' if sin_m else ''}{' y ' if sin_m and not vp else ''}{'en página sin /VP' if not vp else ''} "
                          f"('{(a.info.get('content') or '')[:50]}') - va con Subject LEGEND / sin medición o aplanado")
    return ev


@chequeo("CE_VISTA_BLUEBEAM", ["U-153", "BE-149", "U-010", "U-121", "U-167", "BE-156"], "U-153 / BE-149: simula el Markups List de Bluebeam de CADA "
         "markup (Length = /Vertices x /Measure C, Area = shoelace x C², Depth, Wall Area = Length x Depth / DepthUnit C, Page Label, "
         "/VP, Subject) y lo cuadra contra el Excel (LF, H, LF x H, SF del cielo, hoja) y contra la etiqueta ('SF wall' = Wall Area); "
         "deja Auditoria/VISTA_BLUEBEAM.csv; U-167: /NM repetido o con '/' o '\\' = FAIL (Bluebeam lo deja fuera del CSV)")
def ce_vista_bluebeam(c):
    pdfs = _pdfs_markups(c) if getattr(c, "planos", None) else []
    if not pdfs:
        return R("FAIL", "0 PDF de markups en Planos marcados/ (U-137: el chequeo no pasa en vacío)")
    if not c.excel:
        return R("FAIL", "sin Excel (Take-off/*.xlsx) contra el cual cuadrar la vista de Bluebeam")
    import markups_bluebeam as MB
    nmf = []
    for p in pdfs:                                   # U-167 / BE-156: /NM repetido o con '/' = el markup no sale en el CSV de Bluebeam
        nmf += [f"{os.path.basename(p)}: {x}" for x in MB.nm_fallas(p)]
    todas, fallas, res = [], [], []
    for p in pdfs:
        fs, fl, info = vista_bluebeam(p, c.excel, c.canon if getattr(c, "canon", None) else None)
        todas += fs
        fallas += fl
        res.append(f"{os.path.basename(p)}: {info['markups']} markups revisados ({info['ok']} OK) en {info['paginas']} hojas, "
                   f"{info['renglones']} renglones del Excel")
    if c.entrega:
        sal = vista_csv(todas, os.path.join(c.entrega, "Auditoria", "VISTA_BLUEBEAM.csv"))
        res.append(f"CSV: {os.path.relpath(sal, c.w)}")
    for p in pdfs:                                   # BE-XF07 (Xfinity 10-nov): muestra de leyenda con Subject = type, sin /Measure
        nmf += [f"{os.path.basename(p)}: {x}" for x in subject_sin_medida_fallas(p, c.excel)]
    fallas = nmf + fallas
    if fallas:
        return R("FAIL", f"{len(fallas)} diferencia(s) en la vista de Bluebeam", *fallas[:30], *res)
    return R("PASS", *res, "/NM único y sin '/' en todo el PDF (U-167)")


RX_B2_3LADOS = re.compile(r"Three-way height check \(U-175\): (\d+)/(\d+) markups OK")


@chequeo("CE_ALTURAS_3LADOS", ["U-175"], "U-175 (usuario 11-nov): ALTURAS a tres lados markup por markup, igual que el CSV: Depth de Bluebeam "
         "(Auditoria/VISTA_BLUEBEAM.csv) = Height del Excel = Auditoria/ALTURAS_IMPRESAS.csv (lectura independiente que NO ve el Excel: "
         "Wall ID, Printed H, Source N/HOJA, Operation, Status CONFIRMED / DERIVED, Image). FAIL: falta ALTURAS_IMPRESAS.csv, MISMATCH, "
         "fila sin Source / Image, DERIVED sin Operation, 0 markups comparados, COMPARACION_ALTURAS.csv que falta o no cuadra, CHECKLIST B2 sin N/N")
def ce_alturas_3lados(c):
    import contextlib, csv, io as _io, tempfile
    import comparar_alturas as CA
    ent = getattr(c, "entrega", None)
    if not ent or not c.excel:
        return R("FAIL", "sin carpeta de entrega o sin Excel (U-137: no pasa en vacío)")
    au = os.path.join(ent, "Auditoria")
    ai, vb, cmp_ = (os.path.join(au, n) for n in ("ALTURAS_IMPRESAS.csv", "VISTA_BLUEBEAM.csv", "COMPARACION_ALTURAS.csv"))
    if not os.path.isfile(ai):
        return R("FAIL", "falta Auditoria/ALTURAS_IMPRESAS.csv (U-175: lectura independiente de las alturas impresas)")
    if not os.path.isfile(vb):
        return R("FAIL", "falta Auditoria/VISTA_BLUEBEAM.csv (lo deja CE_VISTA_BLUEBEAM)")
    tmp = os.path.join(tempfile.mkdtemp(prefix="u175_"), "c.csv"); buf = _io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = CA.main([vb, c.excel, ai, tmp])
    txt = buf.getvalue(); ev = [l.strip() for l in txt.splitlines() if l.startswith("FAIL")]
    m = re.search(r"ALTURAS: (\d+)/(\d+) markups OK", txt)
    ok, n = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
    if not os.path.isfile(cmp_):
        ev.append("falta Auditoria/COMPARACION_ALTURAS.csv (correr comparar_alturas.py antes de la compuerta)")
    else:
        lee = lambda f: [(r.get("Wall ID"), r.get("Result")) for r in csv.DictReader(open(f, encoding="utf-8-sig"))]
        if lee(cmp_) != lee(tmp):
            ev.append("Auditoria/COMPARACION_ALTURAS.csv no cuadra con la comparación de hoy (desactualizado)")
    raiz = os.path.dirname(getattr(c, "planos", "") or ent)
    cl = [f for f in os.listdir(raiz) if re.fullmatch(CHECKLIST_RE, f)] if os.path.isdir(raiz) else []
    if cl:
        import openpyxl
        wb = openpyxl.load_workbook(os.path.join(raiz, cl[0]), data_only=True)
        b2 = " ".join(str(v) for ws in wb.worksheets if ws.title.startswith("B2") for r in ws.iter_rows(values_only=True) for v in r if v)
        mb = RX_B2_3LADOS.search(b2)
        if not mb or (int(mb.group(1)), int(mb.group(2))) != (ok, n):
            ev.append(f"CHECKLIST B2 sin la línea 'Three-way height check (U-175): {ok}/{n} markups OK' (U-175)")
    else:
        ev.append("falta CHECKLIST_REVISION.xlsx para poner el resultado en B2 (U-175)")
    if rc or ev:
        return R("FAIL", *(ev or ["comparar_alturas.py salió con código 1"])[:30])
    return R("PASS", f"{ok}/{n} markups: Depth de Bluebeam = Height del Excel = altura impresa (ALTURAS_IMPRESAS.csv); "
                     "COMPARACION_ALTURAS.csv y CHECKLIST B2 al día (U-175)")


RX_B2_MUESTRA = re.compile(r"Random sample \(U-176\)")


@chequeo("CE_ALTURAS_EXTREMO", ["U-176"], "U-176 REGLA DE ORO #2 (usuario 11-nov: 'me preocupan mucha las alturas'): los 6 controles de "
         "tools/comparar_alturas.py extremo: (1) doble lectura ciega ALTURAS_IMPRESAS_A / _B con toda diferencia resuelta con recorte, (2) cierre "
         "dimensional de cada DERIVED ± 1/4\", (3) reglas físicas por wall (H <= B.O., to deck = B.O. + slip track, above ceiling = MAYOR "
         "C.H. + extensión, H >= C.H. de cada cuarto, board <= H), (4) cruce por cuarto del RCP, (5) ALTURAS_REVISADAS.pdf + capa "
         "'HEIGHTS (U-176)' en el PDF de markups, (6) CHECKLIST B2 con la muestra al azar. Falta uno o 0 alturas = FAIL")
def ce_alturas_extremo(c):
    import comparar_alturas as AE                  # U-176: alturas_extremo unido a comparar_alturas.py (v81cf87)
    ent = getattr(c, "entrega", None)
    if not ent or not getattr(c, "canon_p", None):
        return R("FAIL", "sin carpeta de entrega o sin canon (U-137: no pasa en vacío)")
    pdfs = [p for p in _pdfs_markups(c) if re.fullmatch(MARKUPS_RE, os.path.basename(p))] if getattr(c, "planos", None) else []
    res = AE.controles(ent, c.canon_p, pdfs[0] if pdfs else None, construir=False)
    ev = [f"{k}: {x}" for k, v in res["fallas"].items() for x in v]
    if not pdfs:
        ev.append("0 PDF de markups para la capa HEIGHTS (U-176)")
    raiz = os.path.dirname(getattr(c, "planos", "") or ent)
    cl = [f for f in os.listdir(raiz) if re.fullmatch(CHECKLIST_RE, f)] if os.path.isdir(raiz) else []
    mu = os.path.join(ent, "Auditoria", "ALTURAS_MUESTRA.json")
    if cl and os.path.isfile(mu):
        import openpyxl
        wb = openpyxl.load_workbook(os.path.join(raiz, cl[0]), data_only=True)
        b2 = [r for ws in wb.worksheets if ws.title.startswith("B2") for r in ws.iter_rows(values_only=True)]
        txt = " ".join(str(v) for r in b2 for v in r if v)
        faltan = [m["Wall ID"] for m in _json(mu) or [] if m["Wall ID"] not in txt]
        if not RX_B2_MUESTRA.search(txt) or faltan:
            ev.append(f"CHECKLIST B2 sin la muestra al azar 'Random sample (U-176)' (faltan {faltan[:6]})")
    else:
        ev.append("CHECKLIST B2: falta CHECKLIST_REVISION.xlsx o Auditoria/ALTURAS_MUESTRA.json (U-176 control 6)")
    cont = [f"{k}: {v}" for k, v in res.get("conteos", {}).items()]
    return R("FAIL", *ev[:30], *cont) if ev else R("PASS", *cont)


RX_MS_FRAMING = re.compile(r"(?i)\b(stud|track|header|box beam|brace|runner)\b")
RX_MS_NO_FRAMING = re.compile(r"(?i)screw|fastener|\bbead\b|\btrim\b|\bclip|anchor|\bpins?\b|insulat|reinforcement at MEP|deflection clips")
RX_GAUGE = re.compile(r"(?i)\b\d{3,4}(?:S|T|ZF|F|CR)\d{3}-\d{2}\b|\b\d{2}\s*ga\b|\b\d{2}\s*gauge\b|\b\d{2,3}\s*mil\b")


def filas_ms(xlsx):
    """[{fila, material, net, cita}] del Material Summary (renglones con Net numérico)."""
    import openpyxl
    wb = openpyxl.load_workbook(xlsx, data_only=False)
    if "Material Summary" not in wb.sheetnames:
        return []
    ws, cab, out = wb["Material Summary"], None, []
    for i, r in enumerate(ws.iter_rows(values_only=True), 1):
        cs = [str(x).strip() if x is not None else "" for x in r]
        if "Material" in cs and "Net" in cs:
            cab = (cs.index("Material"), cs.index("Net"), next((k for k, x in enumerate(cs) if x.startswith("Where it comes")), None))
            continue
        if cab and cs[cab[0]]:
            try:
                net = float(r[cab[1]])
            except (TypeError, ValueError):
                continue
            out.append({"fila": i, "material": cs[cab[0]], "net": net, "cita": cs[cab[2]] if cab[2] is not None else ""})
    return out


def ms_gauge_fallas(filas):
    """U-177 (3) (Xfinity: el renglón '3-5/8" metal stud - per source' era de studs de 16 ga sin decir el gauge): todo renglón de stud / track / header /
    brace con Net > 0 dice su tamaño Y gauge (362S162-54, 16 ga, 54 mil) en el nombre y su N/HOJA. -> [fallas]"""
    ev = []
    for f in filas:
        if f["net"] <= 0 or not RX_MS_FRAMING.search(f["material"]) or RX_MS_NO_FRAMING.search(f["material"]):
            continue
        if not RX_GAUGE.search(f["material"]):
            ev.append(f"Material Summary fila {f['fila']} '{f['material'][:70]}' ({f['net']:g}): sin gauge / designación en el renglón (U-177)")
        if not re.search(r"N/SHEET:\s*\S", f["cita"]) or "default (no sheet)" in f["cita"]:
            ev.append(f"Material Summary fila {f['fila']} '{f['material'][:70]}': sin N/HOJA en 'Where it comes from' (U-177)")
    return ev


def ms_producto_fallas(filas, canon):
    """U-177 (4) (Xfinity renglón 15 decía 'metal stud blocking' y A5.0 imprime '6\" sheet metal blocking strapping'): el renglón del
    Material Summary donde cae un item con producto IMPRESO (product) lleva ese producto en su nombre. -> [fallas]"""
    import trazabilidad as TZ
    ev = []
    for k in ("misc_items", "blocking_items", "trim_items"):
        for x in canon.get(k) or []:
            pr = TZ._producto_impreso(x)
            ref = str(x.get("ref") or "")
            if not pr or not ref or not float(x.get("qty") or x.get("lf") or 0):
                continue
            fs = [f for f in filas if re.search(r"(^|[^\w-])" + re.escape(ref) + r"([^\w-]|$)", f["cita"])]
            norm = lambda t: re.sub(r"\s+", " ", t.replace("-", " ").lower())   # noqa: E731
            if fs and not any(norm(pr) in norm(f["material"]) for f in fs):
                ev.append(f"{ref}: producto impreso '{pr}' no está en el nombre del renglón '{fs[0]['material'][:70]}' (fila {fs[0]['fila']}) (U-177)")
    return ev


@chequeo("CE_MS_GAUGE", ["U-177"], "U-177 (3): todo renglón de stud / track / header / brace del Material Summary con cantidad dice su tamaño "
         "y GAUGE (designación SSMA 362S162-54, '16 ga' o mil) y su N/HOJA; 'per source' sin gauge = FAIL (nadie compra 20 ga por 16 ga)")
def ce_ms_gauge(c):
    if not c.excel:
        return R("FAIL", "sin Excel (U-137)")
    fl = filas_ms(c.excel)
    n = sum(1 for f in fl if f["net"] > 0 and RX_MS_FRAMING.search(f["material"]) and not RX_MS_NO_FRAMING.search(f["material"]))
    ev = ms_gauge_fallas(fl)
    return R("FAIL", *ev[:30]) if ev else R("PASS" if n else "AMBER", f"{n} renglones de stud / track / header / brace con gauge y N/HOJA")


RX_GAUGE_NO_IMPRESO = re.compile(r"(?i)gauge (?:is )?not printed|no (?:printed )?gauge|gauge not (?:shown|given|specified)|sin gauge impreso")
RX_STUD_SCHEDULE = re.compile(r"(?is)STUD\s+SCHEDULE.{0,200}?(?:MIN\.?\s*)?GAU?GE")


def gauge_impreso_fallas(filas, rfis, hojas_txt):
    """BE-CR34 (CR City Hotel rev19): el renglón del Material Summary / el RFI decía 'gauge not printed' y A0.06 imprime un STUD SCHEDULE
    ('STUD DEPTH 2 1/2\" MIN. GAUGE 25'): antes de declarar un gauge no impreso se barre el set por STUD SCHEDULE / MIN. GAUGE.
    -> [fallas]"""
    hs = sorted(h for h, t in (hojas_txt or {}).items() if RX_STUD_SCHEDULE.search(str(t)))
    if not hs:
        return []
    ev = [f"Material Summary fila {f['fila']} '{f['material'][:70]}': dice gauge no impreso y {', '.join(hs[:3])} imprime STUD SCHEDULE "
          f"con MIN. GAUGE (cítelo, U-171)" for f in filas if RX_GAUGE_NO_IMPRESO.search(f["material"] + " " + str(f.get("cita") or ""))]
    for r in rfis or []:
        if isinstance(r, dict) and str(r.get("status") or "").lower() != "closed" and RX_GAUGE_NO_IMPRESO.search(
                " ".join(str(r.get(k) or "") for k in ("pregunta", "question", "loaded"))):
            ev.append(f"{r.get('id')}: pregunta un gauge que {', '.join(hs[:3])} imprime en su STUD SCHEDULE (U-171: no se pregunta lo que el plano resuelve)")
    return ev


@chequeo("CE_GAUGE_IMPRESO", ["BE-CR34", "U-171", "U-177"], "BE-CR34: 'gauge not printed' en un renglón o RFI con un STUD SCHEDULE "
         "(MIN. GAUGE) impreso en el set = FAIL")
def ce_gauge_impreso(c):
    if not c.excel:
        return R("FAIL", "sin Excel (U-137)")
    st = _json(c.set_p) if getattr(c, "set_p", None) else None
    hojas_txt = (st or {}).get("hojas") if isinstance(st, dict) else None
    if not hojas_txt:
        return R("FAIL", "sin set_texto.json (U-137)")
    ev = gauge_impreso_fallas(filas_ms(c.excel), [r for r in c.rfis() if isinstance(r, dict)], hojas_txt)
    hs = sorted(h for h, t in hojas_txt.items() if RX_STUD_SCHEDULE.search(str(t)))
    return R("FAIL", *ev[:20]) if ev else R("PASS", f"STUD SCHEDULE impreso en {', '.join(hs) or 'ninguna hoja'}; ningún gauge declarado no impreso")


@chequeo("CE_MS_PRODUCTO_IMPRESO", ["U-177"], "U-177 (4): el renglón del Material Summary donde cae un item con producto impreso "
         "(canon product, p. ej. '6\" sheet metal blocking strapping') lleva ese producto en su nombre")
def ce_ms_producto(c):
    if not (c.excel and c.canon_p):
        return R("FAIL", "sin Excel o canon (U-137)")
    import trazabilidad as TZ
    n = sum(1 for k in ("misc_items", "blocking_items", "trim_items") for x in c.canon.get(k) or [] if TZ._producto_impreso(x))
    ev = ms_producto_fallas(filas_ms(c.excel), c.canon)
    return R("FAIL", *ev[:30]) if ev else R("PASS" if n else "AMBER", f"{n} items con producto impreso: cada uno nombra su renglón")


def vigentes_entrega(entrega):
    """U-177 (1): {"pdf": ruta, "excel": ruta} de los archivos VIGENTES de la entrega (sin 'zz' / 'REPLACED' / 'NO USAR'). -> (dict, fallas)"""
    viejo = lambda n: re.match(r"(?i)zz\b|.*REPLACED|.*NO USAR", n)   # noqa: E731
    pl = os.path.join(entrega, "Planos marcados")
    pdfs = [os.path.join(pl, n) for n in sorted(os.listdir(pl)) if re.fullmatch(MARKUPS_RE, n) and not viejo(n)] if os.path.isdir(pl) else []
    tk = os.path.join(entrega, "Take-off")
    xls = [os.path.join(tk, n) for n in sorted(os.listdir(tk)) if n.endswith(".xlsx") and not viejo(n)] if os.path.isdir(tk) else []
    ev = []
    if len(pdfs) != 1:
        ev.append(f"{len(pdfs)} PDF de markups vigentes en Planos marcados/ (debe haber 1, el resto 'zz NO USAR')")
    if len(xls) != 1:
        ev.append(f"{len(xls)} Excel vigentes en Take-off/ (debe haber 1)")
    return {"pdf": pdfs[0] if len(pdfs) == 1 else None, "excel": xls[0] if len(xls) == 1 else None}, ev


def _md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def vigente_fallas(ok, drive_listado, chequeos_actuales):
    """U-177 (1): ENTREGA_OK vale solo para lo que validó. ok = ENTREGA_OK.json; drive_listado = {nombre: md5} de los archivos VIGENTES en
    Drive (sin zz / REPLACED); chequeos_actuales = ids de CHEQUEOS de la versión vigente del skill. -> [fallas]"""
    ev = []
    if not (ok or {}).get("ok"):
        ev.append("ENTREGA_OK.json no está en verde")
    vg = (ok or {}).get("vigentes") or {}
    if not vg:
        ev.append("ENTREGA_OK.json sin 'vigentes' (hash del PDF de markups y del Excel): correr la compuerta con el skill vigente")
    for k, v in vg.items():
        md = drive_listado.get(v.get("nombre"))
        if md is None:
            ev.append(f"{k} '{v.get('nombre')}' no está vigente en Drive")
        elif md != v.get("md5"):
            ev.append(f"{k} '{v.get('nombre')}': el de Drive (md5 {md[:8]}) no es el que validó la compuerta (md5 {str(v.get('md5'))[:8]})")
    corridos = {r.get("id") for r in (ok or {}).get("chequeos") or []}
    faltan = sorted(set(chequeos_actuales) - corridos)
    if faltan:
        ev.append(f"la compuerta no corrió con el skill vigente: faltan {len(faltan)} chequeos ({', '.join(faltan[:8])})")
    return ev


@chequeo("CE_ENTREGA_VIGENTE", ["U-177"], "U-177 (1): la entrega tiene UN PDF de markups vigente y UN Excel vigente (sin zz / REPLACED / NO USAR); "
         "ENTREGA_OK guarda su nombre + sha256 + md5 y la lista de chequeos; subir_entrega.py y `compuerta_entrega.py vigente` comparan con "
         "Drive (md5) y con los chequeos del skill vigente: otro archivo en Drive o compuerta vieja = la entrega NO está en verde")
def ce_entrega_vigente(c):
    if not c.entrega:
        return R("FAIL", "sin carpeta de entrega (U-137)")
    vg, ev = vigentes_entrega(c.entrega)
    if ev:
        return R("FAIL", *ev)
    return R("PASS", *[f"{k}: {os.path.basename(p)} sha256 {_sha(p)[:12]}" for k, p in vg.items()])


RX_DELTA_MEDIDO = re.compile(r"[-+]?\d[\d,]*(?:\.\d+)?\s*(SF|LF|EA|PCS|LB|ft)\b", re.I)
RX_DELTA_VAGO = re.compile(r"≈|~\s*\d|[-+]\s*\d+(?:\.\d+)?\s*%")


def rfi_listo_fallas(rfis):
    """U-179 (usuario 11-nov: "Siempre que halla errores corrígelos antes de preguntar lo rfi"; Grand Kia RFI-35 presentado con '+10 %' y
    la geometría impresa era un triángulo de -57 SF): cada RFI abierto lleva el delta de CADA opción MEDIDO (número + unidad, sin '≈' ni
    '+x %' sin operación) y su recorte (img). Un RFI 'PENDING - user manual verification' (U-178) ya fue presentado: solo pide valor cargado.
    -> [fallas]"""
    ev = []
    for r in rfis or []:
        if str(r.get("status") or "").lower() != "open":
            continue
        rid = r.get("id")
        if r.get("pending"):
            if not r.get("loaded"):
                ev.append(f"{rid}: PENDING - user manual verification sin valor conservador cargado (U-178)")
            continue
        op = r.get("opciones") or {}
        for k in ("A", "B", "C"):
            v = op.get(k)
            d = (v.get("delta") if isinstance(v, dict) else v) or ""
            if k == "C" and not str(d).strip():
                continue
            if not RX_DELTA_MEDIDO.search(str(d)) and not re.search(r"(?i)\bn/a\b|no change|0 \(", str(d)):
                ev.append(f"{rid} opción {k}: delta sin cantidad medida ('{str(d)[:60]}')")
            elif RX_DELTA_VAGO.search(str(d)) and not re.search(r"=", str(d)):
                ev.append(f"{rid} opción {k}: delta estimado ('{str(d)[:60]}'): medirlo en la geometría impresa con su operación")
        if not (r.get("img") and os.path.isfile(str(r.get("img")))):
            ev.append(f"{rid}: sin recorte (img) de la geometría impresa")
    return ev


@chequeo("CE_RFI_LISTO", ["U-179"], "U-179: un RFI se presenta al usuario solo con la compuerta en VERDE (ningún otro FAIL: los errores se "
         "corrigen ANTES de preguntar) y con el delta de cada opción MEDIDO en la geometría impresa (número + unidad, con operación; '≈' / "
         "'+x %' = FAIL) y su recorte; un RFI 'PENDING - user manual verification' (U-178) solo pide su valor cargado")
def ce_rfi_listo(c):
    rf = [r for r in c.rfis() if isinstance(r, dict)]
    ab = [r for r in rf if str(r.get("status") or "").lower() == "open"]
    ev = rfi_listo_fallas(rf)
    if ev:
        return R("FAIL", *ev[:25])
    return R("PASS", f"{len(ab)} RFI abiertos con cada opción medida y recorte" if ab else "0 RFI abiertos")


FECHA_U184 = "2026-11-11T19:40:00+00:00"     # U-184 registrada: entregas con primera subida anterior = AMBER (U-180 (4) / U-184 (6))
RX_AUDITORIA_U181 = re.compile(r"(?i)auditor[ií]a.*U-?181|U-?181.*auditor|INFORME_AUDITORIA|revision_independiente|INFORME_R\d")
RX_FECHA_ISO = re.compile(r"(20\d\d-\d\d-\d\d)[T ](\d\d:\d\d)(?::\d\d)?\s*(?:([+-]\d\d:?\d\d|Z|UTC)|(PST|PDT|PT))?")


def _iso(txt):
    """primera fecha ISO de un texto -> datetime con zona (PST/PT = -08:00; sin zona = UTC)."""
    m = RX_FECHA_ISO.search(str(txt or ""))
    if not m:
        return None
    z = m.group(3) or ("-08:00" if m.group(4) else "+00:00")
    z = "+00:00" if z in ("Z", "UTC") else (z if ":" in z else z[:3] + ":" + z[3:])
    try:
        return datetime.datetime.fromisoformat(f"{m.group(1)}T{m.group(2)}:00{z}")
    except ValueError:
        return None


def _hashes_cadena(w):
    """sha256 de todo archivo que la cadena tocó (bitácora: 'hashes' de cada corrida)."""
    out = set()
    for p in (os.environ.get("BITACORA"), os.path.join(w, "bitacora.jsonl")):
        if p and os.path.isfile(p):
            for ln in open(p, encoding="utf-8", errors="ignore"):
                try:
                    out |= set((json.loads(ln).get("hashes") or {}).values())
                except ValueError:
                    continue
    return out


def protocolo_3h_fallas(w, entrega, excel, pdf, subida=None, tiempos_txt="", corridas=None, ahora=None):
    """U-184 (usuario 11-nov: '... más de 30 horas ... tienes que terminarlo entre 2 y 3 horas'): (1) auditoría U-181 fechada ANTES de la
    primera subida; (2) H-A / H-B dentro de las lecturas (ALTURAS_IMPRESAS_A / _B + TIEMPOS.md de las lecturas los nombra); (3) Excel y
    PDF de markups con hash PRODUCIDO POR LA CADENA (sello del Excel = su sha256; sha256 en la bitácora): nada editado a mano (CR rev18b);
    (4) corridas finales de compuerta sobre los mismos archivos <= 2; (5) TIEMPOS.md con 'corridas de compuerta: N'. -> (fallas, info)"""
    ev, info = [], []
    au = os.path.join(entrega, "Auditoria") if entrega else ""
    cand = [os.path.join(r, f) for r, _d, fs in os.walk(au) for f in fs if f.endswith((".md", ".txt", ".json"))
            and RX_AUDITORIA_U181.search(os.path.join(r, f))] if au and os.path.isdir(au) else []
    fechas = [(_iso(open(p, encoding="utf-8", errors="ignore").read(4000)), p) for p in cand]
    fechas = [(f, p) for f, p in fechas if f]
    primera = _iso((subida or {}).get("primera_subida_iso") or (subida or {}).get("fecha_iso")) if subida else None
    if not fechas:
        ev.append("(1) sin auditoría independiente U-181 FECHADA en Auditoria/ (informe con 'YYYY-MM-DD HH:MM' en el encabezado)")
    else:
        f0, p0 = min(fechas)
        info.append(f"auditoría U-181 {f0.isoformat()} ({os.path.basename(p0)})")
        if primera and f0 > primera:
            ev.append(f"(1) la auditoría U-181 ({f0.isoformat()}) es DESPUÉS de la primera subida ({primera.isoformat()}): entregado sin revisión de fondo")
    if not (au and all(os.path.isfile(os.path.join(au, n)) for n in ("ALTURAS_IMPRESAS_A.csv", "ALTURAS_IMPRESAS_B.csv"))):
        ev.append("(2) faltan Auditoria/ALTURAS_IMPRESAS_A.csv / _B.csv (doble lectura ciega U-176 dentro de las lecturas A/B)")
    elif not re.search(r"(?im)^.*lectura.*H-A.*H-B.*$|^.*H-A.*H-B.*lectura.*$", tiempos_txt or ""):
        ev.append("(2) TIEMPOS.md no registra H-A / H-B dentro del paso de lecturas (U-184 (1): van con las lecturas A / B, no después)")
    hs = _hashes_cadena(w)
    for nom, f in (("Excel", excel), ("PDF de markups", pdf)):
        if not (f and os.path.isfile(f)):
            ev.append(f"(3) sin {nom} vigente")
            continue
        sh = _sha(f)
        if nom == "Excel":
            sello = _json(f + ".sello.json") or {}
            if sello.get("xlsx_sha256") and sello["xlsx_sha256"] != sh:
                ev.append(f"(3) {os.path.basename(f)} no es el que selló la cadena (sello {sello['xlsx_sha256'][:10]} != {sh[:10]}): editado a mano")
        if hs and sh not in hs:
            ev.append(f"(3) {os.path.basename(f)} (sha {sh[:10]}) no salió de ninguna corrida de la cadena (bitácora): arreglo a mano fuera de la cadena")
    if not hs:
        ev.append("(3) sin bitácora de la cadena (bitacora.jsonl): no se puede probar que los archivos salieron de la cadena")
    if corridas is not None:
        fin = [x for x in corridas if x.get("excel") == (_sha(excel) if excel and os.path.isfile(excel) else None)
               and x.get("pdf") == (_sha(pdf) if pdf and os.path.isfile(pdf) else None)]
        info.append(f"{len(fin)} corrida(s) final(es) sobre estos archivos, {len(corridas)} en la rev")
        if len(fin) > 2:
            ev.append(f"(4) {len(fin)} corridas finales de compuerta sobre los mismos archivos (máximo 2): reportar la causa (compuerta temprana por paso, U-184 (2))")
    m = re.search(r"(?i)corridas de compuerta\s*[:=]\s*(\d+)", tiempos_txt or "")
    if not m:
        ev.append("(5) TIEMPOS.md sin 'corridas de compuerta: N' (U-184 (7))")
    else:
        info.append(f"TIEMPOS.md: corridas de compuerta {m.group(1)}")
    return ev, info


@chequeo("CE_PROTOCOLO_3H", ["U-184"], "U-184 'bien a la primera en 2-3 h': auditoría U-181 fechada antes de la primera subida, H-A / H-B dentro de "
         "las lecturas, Excel / PDF de markups con hash producido por la cadena (sello + bitácora, nada a mano: CR rev18b), <= 2 corridas finales "
         "de compuerta y TIEMPOS.md con las corridas contadas")
def ce_protocolo_3h(c):
    if not c.entrega:
        return R("FAIL", "sin carpeta de entrega (U-137)")
    vg, _ev = vigentes_entrega(c.entrega)
    sub = _json(os.path.join(c.w, "SUBIDA_OK.json"))
    tp = os.path.join(c.entrega, "TIEMPOS.md")
    tt = open(tp, encoding="utf-8", errors="ignore").read() if os.path.isfile(tp) else ""
    actual = {"excel": _sha(vg["excel"]) if vg.get("excel") else None, "pdf": _sha(vg["pdf"]) if vg.get("pdf") else None}
    ev, info = protocolo_3h_fallas(c.w, c.entrega, vg.get("excel"), vg.get("pdf"), sub, tt, corridas_compuerta(c.w, c.entrega) + [actual])
    primera = _iso((sub or {}).get("primera_subida_iso") or (sub or {}).get("fecha_iso")) if sub else None
    if ev and primera and primera < datetime.datetime.fromisoformat(FECHA_U184):
        return R("AMBER", f"entrega con primera subida {primera.isoformat()} anterior a U-184: no se re-abre (U-180 (4) / U-184 (6))", *ev[:10], *info)
    return R("FAIL", *ev[:20], *info) if ev else R("PASS", *info)


def corridas_compuerta(w, entrega):
    """registro de corridas COMPLETAS de la compuerta de esta rev (<workdir>/compuerta_corridas.jsonl, lo escribe main)."""
    p = os.path.join(w, "compuerta_corridas.jsonl")
    ed = os.path.relpath(entrega, w) if entrega else None
    out = []
    if os.path.isfile(p):
        for ln in open(p, encoding="utf-8"):
            try:
                x = json.loads(ln)
            except ValueError:
                continue
            if x.get("entrega_dir") == ed:
                out.append(x)
    return out


def esperados_rcp(canon):
    """rev7 / CR-R7-01: {id: ("area", SF del área) | ("line", LF)} de TODO cielo / soffit cuantificado: ceilings[] con SF > 0 y
    misc_items '<id> board' (el área = qty / capas de la operación; un renglón 'LF x ...' es lineal)."""
    can = canon if isinstance(canon, dict) else (_json(canon) if canon else None) or {}
    out = {}
    for x in can.get("ceilings") or []:
        sf = float(x.get("area_sf") or 0)
        if sf and str(x.get("status") or "").upper() != "EXCLUDED":
            out[str(x.get("id") or x.get("room"))] = ("area", sf)
    for x in can.get("misc_items") or []:
        r = str(x.get("ref") or "")
        if not r.endswith(" board") or not float(x.get("qty") or 0):
            continue
        op = str(x.get("op") or "")
        m = re.match(r"\s*(\d+\.?\d*)\s*LF x", op) or re.match(r"\s*(\d+\.?\d*) x \((\d+\.?\d*) bottom", op)
        if m:
            out[r[:-6]] = ("line", float(m.group(1)))
        else:
            ml = re.search(r"x\s*(\d+)\s*layer", op)
            mf = re.search(r"slope factor (\d+\.?\d*)", op)      # cielo inclinado: markup = planta; board = planta x factor
            out[r[:-6]] = ("area", round(float(x["qty"]) / (int(ml.group(1)) if ml else 1) / (float(mf.group(1)) if mf else 1), 2))
    return out


def rcp_completo(filas, esperado):
    """Excel -> markup: cada id esperado tiene markup(s) TO-<id>[~k] cuya suma (Area o Length) cuadra con lo cargado (_vb_ok)."""
    got = {}
    for d in filas:
        b = re.sub(r"[~.]\d+$", "", re.sub(r"^(TO|TOX)-", "", str(d.get("Wall ID") or "")))
        g = got.setdefault(b, [0.0, 0.0])
        g[0] += float(d.get("Area (sf)") or 0)
        g[1] += float(d.get("Length (ft)") or 0)
    fallas = []
    for i, (k, v) in sorted(esperado.items()):
        if i not in got:
            fallas.append(f"{i}: {v:,.2f} {'SF' if k == 'area' else 'LF'} cargado SIN markup en el PDF")
            continue
        m = got[i][0] if k == "area" else got[i][1]
        if not _vb_ok(m, v):
            fallas.append(f"{i}: markup {m:,.2f} != cargado {v:,.2f} {'SF' if k == 'area' else 'LF'}")
    return fallas


@chequeo("CE_RCP_COMPLETO", ["CR-R7-01", "U-124", "U-137"], "CR-R7-01 (rev7 CR City Hotel, pregunta del usuario en Bluebeam A3.04 'por que "
         "unos tienen markups y otros no'): Excel -> markup: cada cielo / soffit cuantificado (ceilings[] y misc_items '... board') "
         "tiene su markup TO-<id> con el mismo SF (área) o LF (+-0.5 %); falta uno = FAIL")
def ce_rcp_completo(c):
    pdfs = _pdfs_markups(c) if getattr(c, "planos", None) else []
    if not pdfs or not c.excel:
        return R("FAIL", "sin PDF de markups o sin Excel (U-137: no pasa en vacío)")
    esp = esperados_rcp(c.canon if getattr(c, "canon", None) else None)
    if not esp:
        return R("PASS", "N/A: el canon no trae cielos ni soffits cuantificados")
    filas = []
    for p in pdfs:
        filas += vista_bluebeam(p, c.excel, c.canon if getattr(c, "canon", None) else None)[0]
    fs = rcp_completo(filas, esp)
    return R("FAIL", f"{len(fs)} de {len(esp)} cielos / soffits sin markup o con otra cantidad", *fs[:40]) if fs else \
        R("PASS", f"{len(esp)} cielos / soffits cuantificados, todos con su markup (Excel -> markup)")


def _segs_plano(page):
    S = []
    for dr in page.get_drawings():
        if (dr.get("width") or 0) < 0.3:
            continue
        for it in dr["items"]:
            if it[0] == "l":
                S.append((it[1].x, it[1].y, it[2].x, it[2].y))
            elif it[0] == "re":
                r_ = it[1]
                S += [(r_.x0, r_.y0, r_.x1, r_.y0), (r_.x1, r_.y0, r_.x1, r_.y1), (r_.x0, r_.y1, r_.x1, r_.y1), (r_.x0, r_.y0, r_.x0, r_.y1)]
    return S


def _d_seg(px, py, s_):
    x0, y0, x1, y1 = s_
    dx, dy = x1 - x0, y1 - y0
    L2 = dx * dx + dy * dy
    t = 0 if L2 == 0 else max(0, min(1, ((px - x0) * dx + (py - y0) * dy) / L2))
    return math.hypot(px - (x0 + t * dx), py - (y0 + t * dy))


MARKUP_WALL_TOL = 4.6      # pt: medio grosor de un wall de 1/8" (~3.6) + 1


def markups_fuera_de_wall(markups_pdf, plano_pdf, exentos=(), tol=MARKUP_WALL_TOL):
    """CR-R8-W2: cada vértice de cada markup de wall (PolyLine TO-<id>, no cielos / soffits) cae a <= tol pt de una línea dibujada
    en la MISMA página del plano limpio (el PDF de markups es el bid set página por página). -> (n revisados, [fallas])."""
    import pymupdf
    dm, dp = pymupdf.open(markups_pdf), pymupdf.open(plano_pdf)
    n, fallas, cache = 0, [], {}
    for i in range(min(dm.page_count, dp.page_count)):
        for a in dm[i].annots() or []:
            nm = _nm_leer(dm.xref_get_key(a.xref, "NM")[1].strip("()"))
            if a.type[1] != "PolyLine" or not nm.startswith("TO-") or " SOFFIT " in (a.info.get("content") or ""):
                continue
            wid = re.sub(r"~\d+$", "", nm[3:])
            if wid in exentos or wid.split(" ")[0] in exentos:
                continue
            S = cache.setdefault(i, _segs_plano(dp[i]))
            n += 1
            for v in a.vertices:
                d_ = min((_d_seg(v[0], v[1], s_) for s_ in S), default=1e9)
                if d_ > tol:
                    fallas.append(f"{nm} ({dm[i].get_label()}): vértice ({v[0]:.1f}, {v[1]:.1f}) a {d_:.1f} pt de la línea de wall más cercana")
                    break
    return n, fallas


@chequeo("CE_MARKUP_EN_WALL", ["CR-R8-W2", "U-120", "U-137"], "CR-R8-W2 (rev8 CR City Hotel, revisión de todos los walls): cada vértice de "
         "cada markup de wall cae sobre la banda del wall dibujada en el plano limpio (<= 4.6 pt de una línea); un tramo / jog / pieza a cada "
         "lado de un vano es su segmento, nunca una recta del LF total; excepción solo con markup_check_note escrita en el canon")
def ce_markup_en_wall(c):
    pdfs = _pdfs_markups(c) if getattr(c, "planos", None) else []
    bs = c.cfg.get("bidset_limpio") or c.cfg.get("bidset")
    if not pdfs or not bs or not os.path.isfile(bs):
        return R("FAIL", "sin PDF de markups o sin bid set limpio (U-137: no pasa en vacío)")
    can = c.canon if isinstance(getattr(c, "canon", None), dict) else (_json(c.canon) if getattr(c, "canon", None) else {}) or {}
    exentos = {w["id"] for w in (can.get("walls") or []) + (can.get("existing_walls") or []) if w.get("markup_check_note")}
    tot, fs = 0, []
    for p in pdfs:
        n_, f_ = markups_fuera_de_wall(p, bs, exentos)
        tot += n_
        fs += f_
    if not tot:
        return R("FAIL", "0 markups de wall revisados (U-137)")
    return R("FAIL", f"{len(fs)} markups de wall fuera de su banda", *fs[:30]) if fs else \
        R("PASS", f"{tot} markups de wall sobre su banda dibujada ({len(exentos)} con excepción escrita)")


CONTORNO_PROHIBIDO = re.compile(r"\b(bbox|locator|box of the canon walls|floor-plate box|scaled about|scaled to)\b", re.I)
CONTORNO_SIN_GEOMETRIA = "source has no geometry"


def _area_pts(P):
    return abs(sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))) / 2


def _segs_huella(page, minimo=20.0):
    """líneas H / V largas de la página (cualquier grosor: los muros del RCP pueden venir como rellenos), sin tramas cortas."""
    S = []
    for dr in page.get_drawings():
        for it in dr["items"]:
            if it[0] == "l":
                a, b = it[1], it[2]
                if math.hypot(b.x - a.x, b.y - a.y) >= minimo:
                    S.append((a.x, a.y, b.x, b.y))
            elif it[0] == "re":
                r_ = it[1]
                if r_.width >= minimo:
                    S += [(r_.x0, r_.y0, r_.x1, r_.y0), (r_.x0, r_.y1, r_.x1, r_.y1)]
                if r_.height >= minimo:
                    S += [(r_.x0, r_.y0, r_.x0, r_.y1), (r_.x1, r_.y0, r_.x1, r_.y1)]
    return S


def _dentro_huella(S, cx, cy, alcance=1200.0):
    """el punto tiene una línea de wall dibujada en las 4 direcciones a <= alcance pt (dentro de la huella del edificio)."""
    hits = [False] * 4
    for x0, y0, x1, y1 in S:
        if abs(y0 - y1) < 0.5 and min(x0, x1) <= cx <= max(x0, x1):
            d = y0 - cy
            if 0 < d <= alcance: hits[0] = True
            if -alcance <= d < 0: hits[1] = True
        if abs(x0 - x1) < 0.5 and min(y0, y1) <= cy <= max(y0, y1):
            d = x0 - cx
            if 0 < d <= alcance: hits[2] = True
            if -alcance <= d < 0: hits[3] = True
    return all(hits)


def contornos_no_medidos(markups_pdf, plano_pdf):
    """CR-R9-B: markups de cielo / soffit (Polygon o PolyLine TO-<id> con 'CEILING' o 'SOFFIT' en Contents) cuya causa dice que la
    geometría NO es medida (bbox / locator / caja de walls / escalado) -> falla, salvo 'source has no geometry' escrito Y el
    polígono dentro de la huella del edificio. Todo cielo: centroide dentro de la huella. -> (n revisados, [fallas])."""
    import pymupdf
    dm, dp = pymupdf.open(markups_pdf), pymupdf.open(plano_pdf)
    n, fallas, cache = 0, [], {}
    for i in range(min(dm.page_count, dp.page_count)):
        for a in dm[i].annots() or []:
            nm = _nm_leer(dm.xref_get_key(a.xref, "NM")[1].strip("()"))
            ct = a.info.get("content") or ""
            if not nm.startswith("TO-") or not re.search(r"\b(CEILING|SOFFIT)\b", ct):
                continue
            n += 1
            V = [(v[0], v[1]) for v in a.vertices or []]
            if not V:
                continue
            cx, cy = sum(v[0] for v in V) / len(V), sum(v[1] for v in V) / len(V)
            S = cache.setdefault(i, _segs_huella(dp[i]))
            fuera = a.type[1] == "Polygon" and not _dentro_huella(S, cx, cy)
            if CONTORNO_PROHIBIDO.search(ct) and CONTORNO_SIN_GEOMETRIA not in ct:
                fallas.append(f"{nm} ({dm[i].get_label()}): geometría no medida ('{CONTORNO_PROHIBIDO.search(ct).group(0)}' en Contents)")
            elif fuera:
                fallas.append(f"{nm} ({dm[i].get_label()}): centroide ({cx:.0f}, {cy:.0f}) FUERA de la huella del edificio")
    return n, fallas


def contornos_canon(canon, tol=0.02):
    """CR-R9-B: cada ceilings[] con SF lleva 'contorno' medido: area_medida_sf igual a area_sf (tolerancia de medio por ciento) y, si hay SF impreso,
    |medido - impreso| / impreso <= tol contra la definición declarada (cuadra_con), o 'nota' escrita que explica la diferencia."""
    fallas = []
    for x in canon.get("ceilings") or []:
        sf = float(x.get("area_sf") or 0)
        if not sf or str(x.get("status") or "").upper() == "EXCLUDED":
            continue
        k = x.get("contorno")
        cid = x.get("id") or x.get("room")
        if not isinstance(k, dict) or not k.get("area_medida_sf"):
            fallas.append(f"{cid}: sin contorno medido (contorno.area_medida_sf)")
            continue
        am = float(k["area_medida_sf"])
        if abs(am - sf) > max(0.005 * sf, 0.05):
            fallas.append(f"{cid}: cargado {sf} != contorno medido {am}")
        ref = k.get("sf_referencia")
        if ref and abs(float(k.get("comparado_sf") or am) - float(ref)) / float(ref) > tol and not k.get("nota"):
            fallas.append(f"{cid}: medido {k.get('comparado_sf') or am} vs impreso {ref} > {tol:.0%} sin nota")
    return fallas


@chequeo("CE_CONTORNO_REAL", ["CR-R9-B", "U-124", "U-137"], "CR-R9-B (rev9 CR City Hotel, orden vía COORDINACIÓN: cielos con bbox / "
         "localizador / caja / polígono escalado; 406 dibujado fuera del edificio): cada cielo / soffit se dibuja con su contorno MEDIDO "
         "en vectores (caras de los walls); Contents con bbox / locator / box / scaled = FAIL salvo 'source has no geometry' y dentro de la "
         "huella; ceilings[] con contorno.area_medida_sf = SF cargado (+-0.5 %) y chequeo contra el SF impreso (+-2 %) o nota escrita")
def ce_contorno_real(c):
    pdfs = _pdfs_markups(c) if getattr(c, "planos", None) else []
    bs = c.cfg.get("bidset_limpio") or c.cfg.get("bidset")
    if not pdfs or not bs or not os.path.isfile(bs):
        return R("FAIL", "sin PDF de markups o sin bid set limpio (U-137: no pasa en vacío)")
    can = c.canon if isinstance(getattr(c, "canon", None), dict) else (_json(c.canon) if getattr(c, "canon", None) else {}) or {}
    tot, fs = 0, []
    for p in pdfs:
        n_, f_ = contornos_no_medidos(p, bs)
        tot += n_
        fs += f_
    fs += contornos_canon(can)
    if not tot and (can.get("ceilings") or []):
        return R("FAIL", "0 markups de cielo revisados con cielos en el canon (U-137)")
    return R("FAIL", f"{len(fs)} cielos / soffits sin contorno medido", *fs[:40]) if fs else \
        R("PASS", f"{tot} markups de cielo / soffit con contorno medido; {len(can.get('ceilings') or [])} ceilings con contorno == cargado")


RX_PUERTA_RENGLON = re.compile(r"(?<![\w.])(\d{3}\.\d{1,2})(?![\w.])((?:(?!(?<![\w.])\d{3}\.\d{1,2}(?![\w.])).){0,160})", re.S)
RX_MIN = re.compile(r"(?<![\w.])(\d{2,3})\s*MIN\.?(?![\w])")


def ratings_puertas(hojas_txt):
    """{puerta: minutos} de los door schedules impresos (hojas cuyo texto dice DOOR SCHEDULE): renglón = desde el número de puerta
    hasta el siguiente número de puerta."""
    out = {}
    for h, txt in (hojas_txt or {}).items():
        if "DOOR SCHEDULE" not in str(txt).upper():
            continue
        for m in RX_PUERTA_RENGLON.finditer(str(txt)):
            mm = RX_MIN.search(m.group(2))
            out.setdefault(m.group(1), (int(mm.group(1)) if mm else 0, h))     # CR-R11-H1: puerta sin rating = 0
    return out


def puertas_vs_muros(canon, hojas_txt):
    """CR-R10-E2: el muro que contiene una puerta con rating impreso tiene al menos el rating que esa puerta protege (IBC Table
    716.1(2): 90 / 180 MIN -> 2 HR; 45 / 60 MIN -> 1 HR). Muro con 'door NNN.N' en su location y type '-0' / sin rating menor = FAIL,
    salvo door_rating_note escrita en el canon. -> [fallas]."""
    pr = ratings_puertas(hojas_txt)
    fallas = []
    for w in (canon.get("walls") or []) + (canon.get("existing_walls") or []):
        loc = str(w.get("location") or "").split("|")[0]
        for d in re.findall(r"(?i)\bdoors?\s+(\d{3}\.\d{1,2})", loc):
            if d not in pr:
                continue
            mins, h = pr[d]
            req = 2 if mins >= 90 else 1 if mins >= 45 else 0
            mt = re.search(r"-(\d)$", str(w.get("type_id") or ""))
            hr = int(mt.group(1)) if mt else None
            furring = re.match(r"F[A-Z]?\.", str(w.get("type_id") or w["id"])) or re.search(r"(?i)\bCMU\b|masonry|concrete", loc)
            if furring:      # furring sobre el elemento rated (CMU / concreto): el rating de la puerta lo lleva el muro detrás
                continue
            if req and (hr is None or hr < req) and not w.get("door_rating_note"):
                fallas.append(f"{w['id']}: contiene la puerta {d} ({mins} MIN en {h}) -> el muro requiere {req} HR; cargado type {w.get('type_id')}")
            if not mins and hr and not w.get("door_rating_note"):      # CR-R11-H1: puerta SIN rating en un muro cargado rated
                fallas.append(f"{w['id']}: muro cargado {hr} HR contiene la puerta {d} SIN rating en {h} (conflicto: Review Item / RFI con delta y door_rating_note)")
    return fallas


@chequeo("CE_PUERTA_RATING_MURO", ["CR-R10-E2", "U-100", "U-137"], "CR-R10-E2 (rev10 CR City Hotel, auditoría U-138: la puerta 120.1 "
         "'90 MIN' de A8.00 hacía 2 HR el muro sur de ELEC / TELE 120 y el RFI la ignoró): el rating de cada puerta del door schedule "
         "se cruza con el rating del muro que la contiene (IBC Table 716.1(2)); muro con rating menor = FAIL salvo door_rating_note")
def ce_puerta_rating_muro(c):
    st = _json(c.set_p)
    hojas_txt = (st or {}).get("hojas") if isinstance(st, dict) else None
    can = c.canon if isinstance(getattr(c, "canon", None), dict) else (_json(c.canon) if getattr(c, "canon", None) else {}) or {}
    if not hojas_txt:
        return R("FAIL", "sin set_texto.json: no se puede leer el door schedule (U-137)")
    pr = ratings_puertas(hojas_txt)
    if not any(v[0] for v in pr.values()):
        return R("PASS", "N/A: el set no imprime door schedule con rating")
    fs = puertas_vs_muros(can, hojas_txt)
    return R("FAIL", f"{len(fs)} muros con rating menor que su puerta", *fs[:30]) if fs else \
        R("PASS", f"{len(pr)} puertas con rating impreso cruzadas con el rating de su muro")


def _titulo_detalle(hojas_txt, det):
    """título impreso del detalle N/HOJA: la línea que sigue al número N sola en su línea (p. ej. '7\nWALL DETAIL - CORRIDOR CEILING')."""
    n, h = det.split("/")
    t = str((hojas_txt or {}).get(h) or "")
    tit = [m.group(1) for m in re.finditer(r"(?m)^" + re.escape(n) + r"\s*\n\s*([A-Z][A-Z0-9 ,&'\-/]{6,80})$", t)]
    return " / ".join(tit)


def coherencia_r10(canon, hojas_txt=None):
    """CR-R10-R1 / m1 / m2 -> [fallas].
    R1: un muro de shaft (id CH...) cuya location cita el detalle que llama su burbuja '(N/Axx.xx)' lleva stud_text que cita ESE detalle
        (el detalle manda sobre la fila del tipo, U-115).
    m1: un cielo de cuarto (no corridor / lobby / vestíbulo) no deriva su altura del mismo detalle N/HOJA que un cielo de corridor.
    m2: todo muro con renglones CH-STUD / J-RUNNER en misc_items lleva stud_text (el Partition Takeoff no dice 'none (board only)')."""
    out = []
    ws = (canon.get("walls") or []) + (canon.get("existing_walls") or [])
    for w in ws:
        m = re.search(r"\((\d{1,2}/A\d\.\d\d)\)", str(w.get("location") or ""))
        if str(w["id"]).startswith("CH") and m and m.group(1) not in str(w.get("stud_text") or ""):
            out.append(f"R1 {w['id']}: la burbuja llama {m.group(1)} y el stud no lo cita (stud_text: {w.get('stud_text')})")
    det_corr = set()
    for x in canon.get("ceilings") or []:
        if re.search(r"(?i)corridor", str(x.get("room"))):
            mh = re.search(r"height[^|]*", str(x.get("source") or ""))
            det_corr |= set(re.findall(r"\b\d{1,2}/A\d\.\d\d\b", mh.group(0) if mh else ""))
    if hojas_txt:     # solo detalles cuyo TÍTULO impreso es de corridor (una sección de techo sirve a corridor y cuartos)
        det_corr = {d for d in det_corr if "CORRIDOR" in _titulo_detalle(hojas_txt, d).upper()}
    for x in canon.get("ceilings") or []:
        if not re.search(r"(?i)guest room|\bunit\b|bedroom", str(x.get("room"))):
            continue
        mh = re.search(r"height[^|]*", str(x.get("source") or ""))
        com = set(re.findall(r"\b\d{1,2}/A\d\.\d\d\b", mh.group(0) if mh else "")) & det_corr
        if com:
            out.append(f"m1 {x.get('room')}: altura derivada del detalle de corridor {sorted(com)}")
    con_ch = {str(m.get("ref")).split(" ", 1)[1] for m in canon.get("misc_items") or [] if str(m.get("ref")).startswith(("CH-STUD ", "J-RUNNER "))}
    for w in ws:
        if str(w["id"]).split(" ")[0] in con_ch and not w.get("stud_text"):
            out.append(f"m2 {w['id']}: tiene C-H / J-runner en el Material Summary y su fila no dice el stud (stud_text)")
    return out


@chequeo("CE_COHERENCIA_R10", ["CR-R10-R1", "CR-R10-m1", "CR-R10-m2", "U-115"], "CR-R10 (rev10 CR City Hotel, auditoría U-138): "
         "R1 el detalle que llama la burbuja manda sobre la fila del tipo (shaft wall 4 3/4\" = C-H 2 1/2\"); m1 un cuarto no toma la "
         "altura del detalle del corridor; m2 la fila de un shaft wall dice su C-H, no 'none (board only)'")
def ce_coherencia_r10(c):
    can = c.canon if isinstance(getattr(c, "canon", None), dict) else (_json(c.canon) if getattr(c, "canon", None) else {}) or {}
    if not can:
        return R("FAIL", "sin canon (U-137)")
    st = _json(c.set_p) if getattr(c, "set_p", None) else None
    fs = coherencia_r10(can, (st or {}).get("hojas") if isinstance(st, dict) else None)
    return R("FAIL", *fs[:30]) if fs else R("PASS", "shafts con su detalle, alturas de cuarto sin detalle de corridor, filas C-H con su stud")


def coherencia_r11(canon, hojas_txt=None):
    """CR-R11 (revisión A de rev10) -> [fallas].
    F3: C-H stud (renglón CH-STUD <muro>) con la MISMA altura que el board / liner de su shaft wall.
    F4: accesorio de un elemento lineal (trim_items '<id> ...') con el MISMO LF que el elemento (largo de la operación del board).
    F2: si el set imprime 'WATER-RESISTANT GYPSUM BOARD FOR CEILINGS IN SHOWER ROOMS', todo cielo de baño / shower (misc '... board' con
        'bath' o 'shower' en su fuente) es W.R."""
    out = []
    H = {str(w["id"]).split(" ")[0]: float(w.get("height_ft") or 0) for w in (canon.get("existing_walls") or []) + (canon.get("walls") or [])
         if str(w["id"]).startswith("CH")}
    for m in canon.get("misc_items") or []:
        r = str(m.get("ref"))
        mo = re.search(r"studs x ([\d.]+) ft", str(m.get("op") or ""))
        if r.startswith("CH-STUD ") and mo and r.split(" ", 1)[1] in H and abs(float(mo.group(1)) - H[r.split(" ", 1)[1]]) > 0.01:
            out.append(f"F3 {r}: stud {mo.group(1)} ft != board / liner {H[r.split(' ', 1)[1]]} ft del mismo shaft wall")
    lf_el = {}
    for m in canon.get("misc_items") or []:
        r = str(m.get("ref"))
        mo = re.match(r"\s*([\d.]+) (?:LF x|x \()", str(m.get("op") or ""))
        if r.endswith(" board") and mo:
            lf_el[r[:-6]] = float(mo.group(1))
    for t in canon.get("trim_items") or []:
        rid = str(t.get("ref") or "").rsplit(" ", 1)[0]
        if rid in lf_el and t.get("lf") and abs(float(t["lf"]) - lf_el[rid]) > 0.05 and "soffit length" in str(t.get("op") or ""):
            out.append(f"F4 {t['ref']}: {t['lf']} LF != {lf_el[rid]} LF del elemento (accesorio no recalculado)")
    gn = any(re.search(r"WATER-RESISTANT\s+GYPSUM\s+BOARD\s+FOR\s+CEILINGS\s+IN\s+SHOWER", str(t)) for t in (hojas_txt or {}).values())
    if gn:
        for m in canon.get("misc_items") or []:
            r = str(m.get("ref"))
            if r.endswith(" board") and r.startswith("CLG") and re.search(r"(?i)\b(bath|shower)\b", str(m.get("source") or "").split("|")[0]) \
                    and "w.r" not in str(m.get("familia")).lower() and "cement" not in str(m.get("familia")).lower():
                out.append(f"F2 {r}: cielo de baño / shower en '{m.get('familia')}' (la nota general pide W.R. en cielos de shower rooms)")
    return out


def proposal_coherente(xlsx, rev_actual):
    """CR-R11-P: la proposal no usa reglas de plantilla para cantidades (una caja por cierta área de board) y no cita otra
    revisión del take-off que la vigente -> [fallas]."""
    import openpyxl
    out = []
    wb = openpyxl.load_workbook(xlsx, read_only=True, data_only=False)
    for ws in wb.worksheets:
        if ws.title == "FBM_PRICES":
            continue
        for row in ws.iter_rows(values_only=True):
            for v in row:
                t = str(v or "")
                if re.search(r"(?i)template:\s*1 box|per 200 SF of finished board", t):
                    out.append(f"{ws.title}: cantidad por regla de plantilla, no del Material Summary: '{t[:80]}'")
                for mm in re.finditer(r"(?i)\b(?:take-off\s+)?rev\s?(\d+)\b", t):
                    if re.search(r"(?i)take-off|vs rev|rev\s?\d+\s+final", t) and mm.group(1) != str(rev_actual):
                        out.append(f"{ws.title}: cita la revisión {mm.group(0)} (vigente rev{rev_actual}): '{t[:80]}'")
                        break
    return out


@chequeo("CE_COHERENCIA_R11", ["CR-R11-F2", "CR-R11-F3", "CR-R11-F4", "CR-R11-P", "U-150"], "CR-R11 (rev11 CR City Hotel, revisión "
         "independiente A): stud del shaft wall a la altura de su board; accesorio recalculado con el largo del elemento; cielos de shower "
         "room en W.R. cuando la nota general lo pide; proposal con cantidades del Material Summary y textos de la revisión vigente")
def ce_coherencia_r11(c):
    can = c.canon if isinstance(getattr(c, "canon", None), dict) else (_json(c.canon) if getattr(c, "canon", None) else {}) or {}
    if not can:
        return R("FAIL", "sin canon (U-137)")
    st = _json(c.set_p) if getattr(c, "set_p", None) else None
    fs = coherencia_r11(can, (st or {}).get("hojas") if isinstance(st, dict) else None)
    xs = sorted(glob.glob(os.path.join(c.entrega or "", "Proposal", "*.xlsx"))) if c.entrega else []
    for x in xs:
        mrev = re.search(r"rev(\d+)", os.path.basename(x))
        if mrev:
            fs += [f"{os.path.basename(x)}: {e}" for e in proposal_coherente(x, mrev.group(1))]
    return R("FAIL", *fs[:30]) if fs else R("PASS", "shaft walls, accesorios, cielos de shower y proposal coherentes")


# Orden del usuario 3-nov ("haz los programas"): las reglas que eran "programa-pendiente" (127 BE-* + U-017 / U-026 /
# U-034 / U-035 / U-037 / U-043 / U-051 / U-057 / U-058 / U-079 / U-081 / U-082 / R-ALC-02 / R-ALC-04 / R-ALC-10) y
# CE_CALLOUTS (U-113 / BE-124, cadena de burbujas N/HOJA hasta el final) corren aquí, una línea por regla en ENTREGA_OK.json.
import chequeos_biblioteca as CB  # noqa: E402


def _cb(fn):
    def w(c):
        b = CB.B.desde_ctx(c)
        est, ev = fn(b)
        return CB.en_vacio(b, fn.__name__, est, ev)      # BE-CR25: N/A 'sin walls / sin canon' con PT lleno = FAIL
    w.__name__ = fn.__name__
    return w


for _ids, _fn, _desc in CB.CHEQUEOS:
    CHEQUEOS.append(("CE_CALLOUTS" if _fn.__name__ == "ce_callouts" else "CB_" + _fn.__name__.upper(), _ids, _desc, _cb(_fn)))


# ----------------------------------------------------------------------------------------------- auditar_compuerta (U-138)
# Orden del usuario 4-nov ("¿por qué esperas a que te pregunte para darte cuenta que hay algún error?"): un VERDE no basta.
# Por cada chequeo se extrae el conteo de su evidencia (burbujas, walls, tags, hojas, imágenes) y se compara con lo esperado
# del proyecto (hojas del set, walls del canon, tags del inventario, hojas de detalles): conteo 0 o implausible = FAIL de
# PLAUSIBILIDAD aunque el chequeo diga PASS. Origen: CE_CALLOUTS "0 burbujas citadas + declaradas" en CFA y Chuze.
RX_CONTEO = re.compile(r"(?<![\w.])(\d+)\s+(burbujas?|walls?|tags?|hojas?|im[aá]genes|images?|markups?|types?)\b", re.I)
UNIDAD = {"burbuja": "burbujas", "burbujas": "burbujas", "wall": "walls", "walls": "walls", "tag": "tags", "tags": "tags",
          "hoja": "hojas", "hojas": "hojas", "imágenes": "imagenes", "imagenes": "imagenes", "image": "imagenes",
          "images": "imagenes", "markup": "markups", "markups": "markups", "type": "types", "types": "types"}


def esperado_proyecto(c):
    """lo que el set / canon dicen que existe: {burbujas, walls, tags, hojas, imagenes, markups, types} (mínimo esperado > 0)."""
    st = _json(c.set_p) if getattr(c, "set_p", None) else None
    hojas = (st or {}).get("hojas") or {}
    det = sum(1 for t in hojas.values() if re.search(r"\b(?:DETAILS?|SECTIONS?)\b", t or "", re.I))
    can = c.canon if isinstance(getattr(c, "canon", None), dict) else {}
    walls = len(can.get("walls") or [])
    tags = len({w.get("tag") for w in can.get("walls") or [] if w.get("tag")})
    return {"burbujas": det, "walls": walls, "tags": tags, "hojas": len(hojas), "imagenes": walls, "markups": walls,
            "types": tags, "hojas_detalle": det}


def auditar_compuerta(res, esp):
    """U-138: marca PLAUSIBILIDAD por chequeo; un PASS / AMBER con un conteo 0 donde el proyecto sí los tiene (o 0-1
    burbujas con >= 3 hojas de detalles) pasa a FAIL. Devuelve la lista de ids cambiados."""
    cambiados = []
    for r in res:
        if r.get("estado") == "FAIL":
            continue
        malos = []
        for ev in r.get("evidencia") or []:
            for m_ in RX_CONTEO.finditer(str(ev)):
                n, u = m_.group(1), m_.group(2)
                cola, cab = str(ev)[m_.end():m_.end() + 40].lower(), str(ev)[max(0, m_.start() - 25):m_.start()].lower()
                if re.search(r"^\W*(?:\w+\W+){0,3}?(?:sin|without|missing|no |not |fuera|con error|mal|pendiente|faltan|de más|extra|"
                             r"wrong|fail|rojo|red|duplicad)", cola) or re.search(r"(?:faltan|missing|sin|without|error)\W*$", cab):
                    continue                                   # "0 walls sin imagen" = un cero bueno (conteo de faltantes)
                k, n = UNIDAD.get(u.lower()), int(n)
                if not k or not esp.get(k):
                    continue
                if n == 0 or (k == "burbujas" and n <= 1 and esp.get("hojas_detalle", 0) >= 3):
                    malos.append(f"{n} {u} en la evidencia y el proyecto tiene {esp[k]} ({k} esperados > 0)")
        r["plausibilidad"] = "IMPLAUSIBLE" if malos else "OK"
        if malos:
            r["evidencia"] = list(r.get("evidencia") or []) + [f"PLAUSIBILIDAD (U-138): {m}" for m in malos[:5]]
            r["estado"] = "FAIL"
            cambiados.append(r["id"])
    return cambiados


# ----------------------------------------------------------------------------------------------- U-142 schedules marcados
# Orden del usuario 5-nov (literal): "tambien quiero que revices todos lo schedules que nos pertenescan y hagas una lista de
# cada material, y marcar cada partiion type para saber que lo revisaste". Lista SCHEDULES_MATERIALES (README, sin hojas ni
# columnas nuevas en el Excel, U-003) desde las lecturas INDEPENDIENTES (fichas.json = Partition Type Schedule, U-111 / BE-122;
# schedules_indep.json = door / window / finish / ceiling schedules), cada material cruzado con el Material Summary, y cada
# type / renglón marcado (círculo rojo + palomita + número) en Planos marcados/SCHEDULES_REVISADOS.pdf.
SUBJ_SCH = "SCHEDULE REVIEWED"   # U-119: el PDF entregado va en inglés (Subject y Contents)
# Componentes de un material de schedule -> renglón del Material Summary (todas las claves en nombre + fuente) o alcance
# del proyecto (takeoff.json alcances ALC-xx NO APLICA, con su nota) o trade de otra división CSI (motivo explícito).
# Sin ninguno de los tres = NOT FOUND = FAIL (U-142: nada se descarta en silencio).
COMP_SCH = [
    (r"Z-furring|\bZF\d|150ZF", {"ms": ["Z-furring channel"]}),
    (r"runner track", {"ms": ["Z-furring runner track"]}),
    (r"polyiso|\bbatt\b|insulation|R-\d{1,2}\b", {"alc": ["ALC-INSUL", "ALC-19"]}),
    (r"sealant|caulk", {"alc": ["ALC-19"]}),
    (r"\bMR\b|W\.?R\.?\b|moisture|wet (?:locations?|walls?|areas?)", {"ms": ["W.R."]}),
    (r"1/4\"\s*(?:Type\s*\"?X\"?\s*)?(?:gyp|board)", {"ms": ["1/4\" gypsum board"]}),
    (r"5/8\"\s*(?:Type\s*\"?X\"?\s*)?(?:gyp|board)|5/8\"\s*Type\s*\"?X\"?$|Type X (?:board|wraps)", {"ms": ["5/8\" gypsum board, Type X"]}),
    (r"resilient channel|087F125", {"ms": ["Resilient channel"]}),
    (r"fiberglass reinforced sheathing|glass mat|exterior (?:gypsum )?sheathing|sheathing per arch", {"ms": ["glass mat sheathing"]}),
    (r"plywood", {"alc": ["ALC-10"]}),
    (r"nailer", {"alc": ["ALC-FRT-NAILERS", "ALC-16"]}),
    (r"wood blocking|fire treated (?:2x|blocking|wood)|\bFT 2x|\bFRT\b(?! plywood)", {"alc": ["ALC-16"]}),
    (r"box header|box beam", {"ms": ["Header / metal stud box beam"]}),
    (r"stud ties|362S162-43", {"ms": ["362S162-43"]}),
    (r"FCB43|framing clips?", {"ms": ["Framing clips per stud"]}),
    (r"clip angle|L4x4", {"ms": ["Clip angle"]}),
    (r"deflection (?:channel|track)", {"ms": ["Deep-leg slotted deflection track"]}),
    (r"diagonal (?:flat )?str(?:ap|ip)", {"ms": ["Diagonal flat strap"]}),
    (r"diagonal bracing", {"ms": ["6\" metal stud", "VH-DIAG-BRACE"]}),
    (r"600S162-54|ceiling joists", {"ms": ["600S162-54"]}),
    (r"600S162-43", {"ms": ["600S162-43"]}),
    (r"cornice", {"ms": ["600S162-43", "CORN-S"]}),
    (r"8\" (?:and 6\" )?(?:CFMF|cold.form|stud)|and 8\" (?:CFMF|cold.form)", {"ms": ["8\" stud"]}),
    (r"6\" (?:and 8\" )?(?:CFMF|cold.form|stud)", {"ms": ["6\" metal stud"]}),
    (r"362S162-33|3-5/8\" (?:CFMF|cold.form|metal )?stud", {"ms": ["3-5/8\" metal stud", "362S162-33"]}),
    (r"screws?|\bSDS\b|anchors? (?!per jamb)|fasten", {"alc": ["ALC-FASTENERS"]}),
    (r"stucco|\blath\b|stone veneer", {"alc": ["ALC-STUCCO"]}),
    (r"acoustical (?:lay-in|tile|ceiling)|\bACT\b|lay-in|suspended (?:acoust|ceiling)|\bC-1\b", {"alc": ["ALC-ACT"]}),
    (r"W-4|sanitary (?:wall|panel)", {"ms": ["Sanitary wall panel system W-4"]}),
    (r"\bC-3\b|painted ceiling|PAINT ceiling", {"ms": ["gypsum board", "GWB-CLG"], "room": True}),
    (r"\bC-2\b|exposed (?:structure|insulation|steel)", {"div": "C-2 exposed structure: no ceiling board printed, nothing to frame or board (A1.2 finish types)"}),
    (r"additional metal framing or fire treated blocking", {"rfi": "RFI-21"}),
    (r"sheet metal|cladding|flashing", {"div": "sheet metal cladding / flashing, Div. 07 62 (not metal framing / drywall)"}),
    (r"hollow metal|HM frame|anchors per jamb|frame by others", {"div": "hollow metal frame and its anchors, Div. 08 11 (by the frame installer)"}),
    (r"storefront|aluminum", {"div": "aluminum storefront, Div. 08 41 (by the glazing contractor)"}),
    (r"glazing", {"div": "glazing, Div. 08 80"}),
    (r"\bCMU\b|masonry", {"div": "CMU / masonry, Div. 04 (the furring on it is carried as its own material)"}),
    (r"\bpaint", {"div": "painting, Div. 09 91 (separate trade; the board under it is carried by its wall type)"}),
]
RX_SIN_MATERIAL = re.compile(r"(?i)^\s*none\b|no (?:CFMF|cfmf|drywall|trade)|not CFMF|finish only|^not printed|no ceiling board")


def _ms_textos(c):
    wb = c.wb()
    out = []
    if wb is not None and "Material Summary" in wb.sheetnames:
        for r in wb["Material Summary"].iter_rows(min_row=4, values_only=True):
            if r and r[0]:
                out.append((str(r[0]), r[2] if isinstance(r[2], (int, float)) else None, str(r[8] or "")))
    return out


def _en_ms(ms, *claves):
    """¿algún renglón del Material Summary (NET > 0 o EXCLUDED con nota) nombra TODAS las claves? La PRIMERA clave va en el
    nombre del renglón (no en su fuente: 'Bottom track' cita '362S162-33' en su fuente y no es el renglón del stud)."""
    ks = [k for k in claves if k]
    for nom, net, src in ms:
        t = (nom + " " + src).lower()
        if ks and ks[0].lower() in nom.lower() and all(k.lower() in t for k in ks) and ((net or 0) > 0 or "excluded" in t):
            return nom
    return None


def _alcances(c):
    tj = _json(_ultimo(["takeoff_work/takeoff.json", "**/takeoff_work/takeoff.json"], c.w)) or {}
    cerr = set()
    for fuente in (tj.get("rfi_cierre"), tj.get("rfis")):
        if isinstance(fuente, dict):
            cerr |= {k for k, v in fuente.items() if re.search(r"(?i)CLOSED|CERRAD", str(v))}
        elif isinstance(fuente, list):
            cerr |= {x.get("id") for x in fuente if isinstance(x, dict) and re.search(r"(?i)closed|cerrad", str(x.get("status") or x.get("estado")))}
    return {a.get("id"): a for a in tj.get("alcances") or [] if isinstance(a, dict)}, cerr


def resolver_material(valor, ms, alc, rfis_cerr, cfg_ms=None, cfg_fuera=None, room=None):
    """-> [(componente, ms_row | None, fuera | None)] por componente reconocido; [] si el valor no nombra ningún componente."""
    v = str(valor)
    for pat, row in (cfg_ms or {}).items():                 # mapeo explícito del proyecto (entrega.json schedules_ms)
        if re.search(pat, v, re.I):
            return [(pat, _en_ms(ms, row), None)]
    for pat, why in (cfg_fuera or {}).items():              # fuera de alcance explícito con motivo (entrega.json schedules_fuera)
        if re.search(pat, v, re.I):
            return [(pat, None, why)]
    out, vistos = [], set()
    for pat, d in COMP_SCH:
        m = re.search(pat, v, re.I)
        if not m:
            continue
        comp = m.group(0)
        clave = tuple(d.get("ms") or d.get("alc") or [d.get("div") or d.get("rfi")])
        if clave in vistos:
            continue
        vistos.add(clave)
        if d.get("ms"):
            if d.get("room") and room:                      # cielo por cuarto: el renglón cita el número del cuarto en su ID
                hit = _en_ms(ms, *d["ms"], room) or (_en_ms(ms, *d["ms"]) if not room.isdigit() else None)
            else:                                           # el elemento por su ID (VH-B1) si el renglón lo itemiza; si no, el material
                hit = next((_en_ms(ms, *d["ms"], tk) for tk in ([f"-{room} ", f"-{room}-", f"-{room}:", f"Door {room} "] if room else [])
                            if _en_ms(ms, *d["ms"], tk)), None)
                if not hit:
                    h2 = _en_ms(ms, *d["ms"])
                    hit = (h2 + (" [material match: this element is not itemized under its own ID]" if room else "")) if h2 else None
            out.append((comp, hit, None))
        elif d.get("alc"):
            a = next((alc[i] for i in d["alc"] if i in alc and re.search(r"NO APLICA|EXCLU", str(alc[i].get("estado")) + str(alc[i].get("nota")))), None)
            out.append((comp, None, f"{a['id']}: {str(a.get('nota'))[:110]}" if a else None))
        elif d.get("rfi"):
            out.append((comp, None, f"{d['rfi']} closed (estimator decision)" if d["rfi"] in rfis_cerr else None))
        else:
            out.append((comp, None, "not our trade: " + d["div"]))
    return out


def lista_schedules(c):
    """-> [{k, hoja, schedule, id, pos, materiales: [{campo, valor, ms, fuera}]}]"""
    fp = (os.path.join(c.w, c.cfg["fichas"]) if c.cfg.get("fichas") else None) or _ultimo(["fichas.json", "**/fichas.json"], c.w)
    fj = _json(fp) or {}
    sp = _ultimo(["schedules_indep.json", "**/schedules_indep.json"], c.w)
    sj = _json(sp) or {}
    cfg_ms, cfg_fuera = c.cfg.get("schedules_ms") or {}, c.cfg.get("schedules_fuera") or {}
    ms = _ms_textos(c)
    alc, rfis_cerr = _alcances(c)
    out = []
    _cn = c.canon or {}
    usados = {str(w.get("type_id")) for w in (_cn.get("walls") or []) + (_cn.get("existing_walls") or []) if w.get("type_id")}   # BE-CR14

    def mats(campo, valor, room=None, ms_directo=None):
        v = str(valor or "").strip()
        if not v or re.fullmatch(r"(?i)(none|null|n/a|not printed)\.?", v):
            return []
        if ms_directo:
            return [{"campo": campo, "valor": v[:160], "ms": ms_directo, "fuera": None}]
        rs = resolver_material(v, ms, alc, rfis_cerr, cfg_ms, cfg_fuera, room)
        if not rs:
            return [{"campo": campo, "valor": v[:160], "ms": None,
                     "fuera": "no trade material printed in this row" if RX_SIN_MATERIAL.search(v) else None}]
        return [{"campo": f"{campo}: {comp}", "valor": v[:160], "ms": hit, "fuera": f} for comp, hit, f in rs]
    for tid, t in (fj.get("types") or {}).items():
        src = " ".join(str(v) for v in (t.get("sources") or {}).values()) or str(t.get("source") or "")   # BE-CR14
        # BE-CC05 (Consumer Cellular, 5-nov): sheet numbers with 3 digits (A500, A-501) as well as A1.1
        HJ_ = r"([A-Z]{1,2}\d{1,2}\.\d{1,2}|[A-Z]{1,2}-?\d{3})"
        m_ = re.search(r"\b(?:" + re.escape(tid) + r"|\d{1,2})/" + HJ_ + r"\b", src) or re.search(r"\b" + HJ_ + r"\b", src)
        hoja = t.get("hoja") or (m_.group(1) if m_ else None)          # BE-CR14: la ficha puede traer su hoja y su posición
        ms_ = []
        sz = str(t.get("stud_size") or t.get("stud") or "")
        des = str(t.get("stud_designation") or "")
        txt = " ".join(x for x in [sz, des, f"{t['gauge_ga']} ga" if t.get("gauge_ga") else "",
                                   f"@ {t['oc_in']}\" O.C." if t.get("oc_in") else ""] if x)
        if re.search(r"(?i)wood", str(t.get("stud_material") or "")):   # BE-CR14: wood framing = Div. 06 EXCLUDED (U-139)
            ms_.append({"campo": "stud", "valor": f"{sz} wood stud", "ms": None, "fuera": "wood framing EXCLUDED (Div. 06, U-139)"})
        elif re.search(r"(?i)furring", sz):
            ms_ += mats("stud", txt)
        elif not sz.strip() or re.fullmatch(r"\s*(--?|n/?a|none)\s*", sz, re.I):   # BE-CR14: '--' = sin stud impreso
            pass
        else:
            dz = re.search(r"\d{3}S\d{3}-\d{2}", des)
            szk = re.match(r'\s*([\d\-/]+")', sz)
            hit = _en_ms(ms, "stud", dz.group(0)) if dz else None
            hit = hit or (_en_ms(ms, "stud", szk.group(1), tid) if szk else None) or (_en_ms(ms, "stud", szk.group(1)) if szk else None)
            ms_.append({"campo": "stud", "valor": txt, "ms": hit, "fuera": None})
            if szk:
                _jr = _en_ms(ms, "J-runner") if re.match(r"(?i)CH\b|CH\.", tid) else None   # BE-CR14: C-H shaft wall = J-runner
                ms_.append({"campo": "track (bottom / top)", "valor": f"{szk.group(1)} track (type {tid})",
                            "ms": _jr or _en_ms(ms, "track", szk.group(1), tid + "-") or _en_ms(ms, "track", szk.group(1)), "fuera": None})
        if t.get("track"):
            ms_ += mats("track", t["track"])
        if t.get("slip_track"):
            ms_ += mats("slip track", t["slip_track"])
        for f_ in t.get("faces") or []:
            bd = str(f_.get("board") or "")
            if bd and not re.fullmatch(r"(?i)\s*not printed\s*", bd):
                ms_ += mats(f"board ({f_.get('side')}) x{f_.get('layers')}", bd)
        if t.get("height"):
            ms_.append({"campo": "height", "valor": str(t["height"])[:160], "ms": "Partition Takeoff (Height)", "fuera": None})
        for x in t.get("extras") or []:
            ms_ += mats("extra", x)
        if usados and tid not in usados:             # BE-CR14: type del schedule que ningún wall del canon usa
            for m_ in ms_:
                if not m_["ms"] and not m_["fuera"]:
                    m_["fuera"] = "type not used on the plans of this set (A0.06 GN 2 'NOT ALL PARTITION TYPES DELINEATED MAY BE USED')"
        out.append({"hoja": hoja, "schedule": "Partition / wall types", "id": tid, "materiales": ms_, "fuente": src[:160],
                    "pos": tuple(t["pos"]) if t.get("pos") else None})
    for s in sj.get("schedules") or []:
        for r in s.get("rows") or []:
            ms_ = []
            rid = str(r.get("id"))
            for ti in r.get("trade_items") or []:
                ms_ += mats("trade", ti, room=rid)
            if usados and re.match(r"^[A-Z]{1,3}\.\d", rid) and rid not in usados and re.search(r"(?i)assembl|partition|wall", str(s.get("name"))):
                for m_ in ms_:                           # BE-CR14: fila de un type que ningún wall usa
                    if not m_["ms"] and not m_["fuera"]:
                        m_["fuera"] = "type not used on the plans of this set (A0.06 GN 2 'NOT ALL PARTITION TYPES DELINEATED MAY BE USED')"
            out.append({"hoja": s.get("sheet"), "schedule": s.get("name"), "id": rid,
                        "pos": (r.get("x"), r.get("y")) if r.get("x") is not None else None,
                        "materiales": ms_, "fuente": r.get("source") or f"{s.get('name')} {s.get('sheet')}"})
    for i, x in enumerate(out, 1):
        x["k"] = i
    return out, bool(fj.get("types")), bool(sj.get("schedules"))



def _es_annots_pdf(pdf):
    """U-119 en los PDF marcados por programa: Subject / Contents en español -> lista de evidencias."""
    import pymupdf
    import idioma_es
    ev = []
    for p in pymupdf.open(pdf):
        for a in p.annots() or []:
            inf = a.info or {}
            t = f"{inf.get('subject') or ''} | {inf.get('content') or ''}"
            if idioma_es.es_espanol(t) or re.search(r"(?i)\b(revisad[oa]|verificad[oa] a ojo|hoja|citada|fuera de alcance)\b", t):
                ev.append(f"{p.get_label() or p.number + 1}: español en la anotación '{t[:70]}'")
    return ev

def marcar_schedules(workdir, entrega_json=None):
    import pymupdf
    c = Ctx(workdir, entrega_json)
    lst, _, _ = lista_schedules(c)
    st = _json(c.set_p) or {}
    labels = list((st.get("hojas") or {}).keys())
    bs = c.cfg.get("bidset_limpio") or c.cfg.get("bidset")
    src = pymupdf.open(bs)
    pag = {CB.norm_hoja(k): i for i, k in enumerate(labels) if i < src.page_count}
    ocr = {CB.norm_hoja(h) for h in st.get("ocr") or []}
    cache = {}
    pos_cfg = c.cfg.get("schedules_pos") or {}
    cache300 = {}
    for x in lst:
        h = CB.norm_hoja(x["hoja"]) if x["hoja"] else None
        kpos = f"{x['hoja']}:{x['id']}" if f"{x['hoja']}:{x['id']}" in pos_cfg else (x["id"] if x["id"] in pos_cfg else None)
        if kpos:                                   # posición verificada a ojo (entrega.json schedules_pos, "HOJA:ID" o "ID")
            x["pos"], x["pos_fuente"] = tuple(pos_cfg[kpos]), "verified position (entrega.json schedules_pos)"
            continue
        if x.get("pos") and h in pag:
            # posición del lector independiente = aproximada (R80f.49: en O'Reilly su escala en y salió ~0.55): se ajusta al
            # rótulo impreso más cercano en la MISMA columna (OCR 300 dpi o capa de texto); sin rótulo cerca queda la del lector
            if h not in cache300:
                cache300[h] = _palabras_pagina(src[pag[h]], h in ocr, dpi=300)
            cx, cy = x["pos"]
            ws = [w for w in cache300[h] if (w[4] if x["id"].isdigit() else w[4].strip(".:,()").upper().replace("$", "S")) == x["id"].upper()
                  and abs((w[0] + w[2]) / 2 - cx) < 40 and abs((w[1] + w[3]) / 2 - cy) < 40]
            if ws:
                w = min(ws, key=lambda w: abs((w[1] + w[3]) / 2 - cy) + abs((w[0] + w[2]) / 2 - cx))
                x["pos"], x["pos_fuente"] = ((w[0] + w[2]) / 2, (w[1] + w[3]) / 2), "printed label (OCR 300 dpi)"
            else:
                x["pos_fuente"] = "independent reader position (no printed label found nearby)"
            continue
        if x.get("pos") or not h or h not in pag:
            continue
        if h not in cache:
            cache[h] = _palabras_pagina(src[pag[h]], h in ocr)
        ws = [w for w in cache[h] if w[4].strip(".:,()").upper().replace("$", "S") == x["id"].upper()]   # OCR lee S como $
        if ws:                                     # el rótulo del type en el schedule (el más bajo de la hoja = la leyenda)
            w = max(ws, key=lambda w: w[1])
            x["pos"] = ((w[0] + w[2]) / 2, (w[1] + w[3]) / 2)
    hojas_m = sorted({CB.norm_hoja(x["hoja"]) for x in lst if x.get("pos") and x["hoja"]}, key=lambda h: pag.get(h, 9999))
    out = pymupdf.open()
    nueva = {}
    for h in hojas_m:
        if h in pag:
            out.insert_pdf(src, from_page=pag[h], to_page=pag[h])
            nueva[h] = out.page_count - 1
    if nueva:
        # BE-CC10: the Page Label is the printed sheet number (G002), not its normalized key (G2)
        orig = {CB.norm_hoja(k): k for k in labels}
        out.set_page_labels([{"startpage": i, "prefix": orig.get(h, h), "style": "", "firstpagenum": 1} for h, i in sorted(nueva.items(), key=lambda kv: kv[1])])
    rojo = (0.85, 0, 0)
    for x in lst:
        h = CB.norm_hoja(x["hoja"]) if x["hoja"] else None
        if not (x.get("pos") and h in nueva):
            continue
        pg = out[nueva[h]]
        M = pg.derotation_matrix
        cx, cy = x["pos"]
        # alto del círculo según el renglón: con renglones apretados (A1.2 O'Reilly, 18 pt) un círculo de 32 pt tapaba los vecinos
        dy = min([abs(o["pos"][1] - cy) for o in lst if o is not x and o.get("pos") and o["hoja"] == x["hoja"]
                  and abs(o["pos"][0] - cx) < 30 and abs(o["pos"][1] - cy) > 1] or [40])
        hh = max(7.0, min(16.0, dy / 2 - 1))
        x["hh"] = hh
        R_ = pymupdf.Rect(cx - 22, cy - hh, cx + 22, cy + hh) * M
        a = pg.add_circle_annot(R_)
        a.set_colors(stroke=rojo)
        a.set_border(width=2.5)
        a.set_info(title="take-off", subject=SUBJ_SCH, content=f"#{x['k']} {x['id']} on {h} ({x['schedule']}) reviewed")
        a.update()
        ft = pg.add_freetext_annot(pymupdf.Rect(R_.x1 + 2, (R_.y0 + R_.y1) / 2 - 9, R_.x1 + 62, (R_.y0 + R_.y1) / 2 + 9), f"\u2713 {x['k']}", fontsize=12,   # centrado en SU renglón (no arriba: se leía como el de la fila de arriba)
                                   text_color=rojo, fill_color=None)   # sin fondo: el recuadro blanco tapaba el tag vecino (A5.2 D1 / D2)
        ft.set_info(title="take-off", subject=SUBJ_SCH + " #", content=f"#{x['k']}")
        ft.update()
        ink = [[(R_.x0 - 10, R_.y0 + 8), (R_.x0 - 5, R_.y1 - 2), (R_.x0 + 2, R_.y0 - 6)]]    # palomita (CE_SCHEDULES_REVISADOS)
        ck = pg.add_ink_annot(ink)
        ck.set_colors(stroke=rojo)
        ck.set_border(width=2.5)
        ck.set_info(title="take-off", subject=SUBJ_SCH + " CHECK", content=f"#{x['k']}")
        ck.update()
    e = c.entrega or c.w
    os.makedirs(os.path.join(e, "Planos marcados"), exist_ok=True)
    pdf = os.path.join(e, "Planos marcados", "SCHEDULES_REVISADOS.pdf")
    out.save(pdf, garbage=3, deflate=True)
    _sin_firmas(pdf)
    L = ["## SCHEDULES_MATERIALES", "", "Every trade schedule reviewed (U-142): each partition type / row is marked (red circle + "
         "check + number) on its schedule sheet in `Planos marcados/SCHEDULES_REVISADOS.pdf`; each material is matched to its "
         "Material Summary row or declared out of scope with its reason. Read independently from the drawings (fichas.json / "
         "schedules_indep.json, U-111).", "", "| # | Schedule | Type / row | Sheet | Material | Value | Material Summary row / out of scope |",
         "|---|---|---|---|---|---|---|"]
    for x in lst:
        for m in x["materiales"] or [{"campo": "-", "valor": "no trade material printed", "ms": None, "fuera": "noted"}]:
            L.append(f"| {x['k']} | {x['schedule']} | {x['id']} | {x['hoja']} | {m['campo']} | {m['valor']} | "
                     f"{m['ms'] or ('OUT OF SCOPE: ' + str(m['fuera']) if m['fuera'] else 'NOT FOUND')} |")
    md = os.path.join(e, "SCHEDULES_MATERIALES.md")
    _escribir(md, "\n".join(L) + "\n")
    # misma lista en el formato de CE_SCHEDULES_REVISADOS (schedules_materiales.json): un bloque por schedule, en el orden de k
    sch = []
    for x in lst:
        if not sch or (sch[-1]["sheet"], sch[-1]["title"]) != (x["hoja"], x["schedule"]):
            hn = CB.norm_hoja(x["hoja"]) if x["hoja"] else None
            sch.append({"sheet": x["hoja"], "page": (pag[hn] + 1) if hn in pag else None,
                        "title": x["schedule"], "ours": True, "why": "trade schedule (U-142)", "rows": []})
        cx, cy = x.get("pos") or (None, None)
        ms_ = sorted({m["ms"] for m in x["materiales"] if m["ms"]})
        fu = sorted({str(m["fuera"]) for m in x["materiales"] if m["fuera"]})
        sch[-1]["rows"].append({
            "type": x["id"], "bbox": [cx - 22, cy - x.get("hh", 16), cx + 22, cy + x.get("hh", 16)] if cx is not None else None,
            "materials": [{"material": m["campo"], "spec": m["valor"], "source": x["hoja"]} for m in x["materiales"]],
            "in_canon": ("yes: " + "; ".join(ms_)) if ms_ else ("n/a: " + ("; ".join(fu) or "no trade material printed in this row")),
            "out_of_scope": "; ".join(fu)})
    json.dump(sch, open(_schedules_json(c)[0], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    if os.path.isfile(c.readme):
        t = open(c.readme, encoding="utf-8").read()
        partes = re.split(r"\n## SCHEDULES_MATERIALES", t)
        cola = ""
        if len(partes) > 1 and "\n## " in partes[1]:
            cola = "\n## " + partes[1].split("\n## ", 1)[1]
        t = partes[0].rstrip() + "\n\n" + "\n".join(L) + "\n" + cola
        _escribir(c.readme, t)
    return pdf, md, lst


@chequeo("CE_SCHEDULES_MARCADOS", ["U-142", "U-111"], "U-142: todos los schedules del trade revisados desde una lectura "
         "independiente; cada type / renglón marcado en Planos marcados/SCHEDULES_REVISADOS.pdf y en la lista SCHEDULES_MATERIALES; "
         "cada material en el Material Summary o fuera de alcance con motivo; 0 = FAIL")
def ce_schedules_marcados(c):
    import pymupdf
    lst, hay_f, hay_s = lista_schedules(c)
    if not hay_f:
        return R("FAIL", "sin fichas.json (lectura independiente del Partition Type Schedule, U-111): no hay schedules revisados")
    if not hay_s:
        return R("FAIL", "sin schedules_indep.json (lectura independiente de door / window / finish / ceiling schedules, U-142)")
    if not lst:
        return R("FAIL", "0 types / renglones en los schedules (U-138: implausible)")
    pdf = os.path.join(c.planos, "SCHEDULES_REVISADOS.pdf")
    if not os.path.isfile(pdf):
        return R("FAIL", f"no hay Planos marcados/SCHEDULES_REVISADOS.pdf ({len(lst)} types / renglones sin marcar): correr "
                         "`compuerta_entrega.py schedules <carpeta>`")
    marcados = set()
    for p in pymupdf.open(pdf):
        for a in p.annots() or []:
            m = re.match(r"#(\d+) (.+?) on ", (a.info or {}).get("content") or "")   # BE-CC06: row ids with spaces (BACK OF HOUSE)
            if (a.info or {}).get("subject") == SUBJ_SCH and m:
                marcados.add((int(m.group(1)), m.group(2)))
    lista_md = os.path.join(c.entrega or c.w, "SCHEDULES_MATERIALES.md")
    lmd = open(lista_md, encoding="utf-8").read() if os.path.isfile(lista_md) else ""
    ev = []
    for x in lst:
        if (x["k"], x["id"]) not in marcados:
            ev.append(f"#{x['k']} {x['id']} ({x['schedule']}, {x['hoja']}): sin marca en SCHEDULES_REVISADOS.pdf")
        if f"| {x['k']} | " not in lmd:
            ev.append(f"#{x['k']} {x['id']}: no está en la lista SCHEDULES_MATERIALES")
        for m in x["materiales"]:
            if not m["ms"] and not m["fuera"]:
                ev.append(f"#{x['k']} {x['id']} {m['campo']} '{m['valor'][:60]}': no está en el Material Summary ni fuera de alcance con motivo")
    ev += _es_annots_pdf(pdf)[:10]
    nsch = len({(x["schedule"], x["hoja"]) for x in lst})
    nmat = sum(len(x["materiales"]) for x in lst)
    if ev:
        return R("FAIL", f"{len(ev)} faltante(s): {nsch} schedules, {len(lst)} types / renglones, {nmat} materiales", *ev[:30])
    return R("PASS", f"{nsch} schedules, {len(lst)} types / renglones marcados, {nmat} materiales cruzados con el Material Summary")


# ----------------------------------------------------------------------------------------------- U-141 detalles circulados
# Orden del usuario 5-nov (literal): "como regla gernera e inviolable, de este momento en adelante tienes que sircular cada
# detail que revcies, y si en esa hoja te manda a otro detalle tambien tienes que marcalo". marcar_detalles: cada burbuja de
# la cadena (chequeos_biblioteca.cadena_detalles) circulada y numerada en su hoja de ORIGEN y su vista DESTINO (título del
# detalle) en Planos marcados/DETALLES_REVISADOS.pdf + DETALLES_REVISADOS_INDEX.md (también al final del README).
RX_TITULO = re.compile(r"(?i)^(?:DETAILS?|SECTIONS?|PLANS?|ELEVATIONS?|SCHEDULES?|TYPES|FLASHING|SILL|JAMB|HEAD|SCUPPER|COLUMN|"
                       r"LEGEND|VIEW|ENLARGED?|INTERIOR|EXTERIOR|WALL|BUILDING|STAIR|CANOPY|PARAPET|CONDUCTOR|DOOR|WINDOW)\b")
SUBJ_DET = "DETAIL REVIEWED"   # U-119: el PDF entregado va en inglés (Subject y Contents)
# U-119: el índice va en inglés (la disposición interna de cadena_detalles es en español)
COMO_EN = {"verificada a ojo": "verified by eye", "detector": "detector"}
DISP_EN = {"misma hoja": "same sheet", "fuera de alcance": "out of scope", "citada": "cited", "sin disposición": "no disposition"}


def _palabras_pagina(p, raster, dpi=150):
    """[(x0, y0, x1, y1, texto)] en pt de la hoja vista: capa de texto (vector) u OCR tesseract a `dpi` (raster)."""
    if not raster:
        return [(w[0], w[1], w[2], w[3], w[4]) for w in p.get_text("words")]
    import pymupdf
    td = _tessdata()
    if not td or not shutil.which("tesseract"):
        return []
    f = tempfile.mktemp(suffix=".png")
    p.get_pixmap(dpi=dpi, colorspace=pymupdf.csGRAY).save(f)
    r = subprocess.run(["tesseract", f, "-", "--psm", "11", "tsv"], capture_output=True, text=True)
    os.remove(f)
    k, out = 72 / dpi, []
    for l in r.stdout.splitlines()[1:]:
        c = l.split("\t")
        if len(c) > 11 and c[11].strip():
            x, y, w, h = (int(c[i]) * k for i in (6, 7, 8, 9))
            out.append((x, y, x + w, y + h, c[11].strip()))
    return out


def ubicar_titulo(palabras, n):
    """vista destino del detalle n en su hoja: el número del título (letra grande) con una palabra de título a su derecha en
    la misma línea (DETAIL / SECTION / PLAN / ELEVATION ...). -> (x0, y0, x1, y1) o None."""
    if not palabras:
        return None
    hs = sorted(w[3] - w[1] for w in palabras)
    med = hs[len(hs) // 2] or 1
    best = None
    for w in palabras:
        if w[4].strip(".:,()[]").upper() != n.upper() or (w[3] - w[1]) < 1.6 * med:
            continue
        h = w[3] - w[1]
        for v in palabras:
            # la palabra del título también es de letra grande (O'Reilly rev10: la keynote "1 PORTLAND CEMENT ... REFER TO
            # EXTERIOR FINISH" de A2.1 se tomó por el título de la vista 1/A2.1: palabra chica = nota, no título)
            if 0 <= v[0] - w[2] <= 12 * h and abs((v[1] + v[3]) / 2 - (w[1] + w[3]) / 2) <= 0.8 * h and RX_TITULO.search(v[4]) \
                    and (v[3] - v[1]) >= 1.4 * med:
                cand = (w[0], w[1], max(v[2], w[2]), max(v[3], w[3]))
                if best is None or h > best[1]:
                    best = (cand, h)
                break
    return best[0] if best else None


def marcar_detalles(workdir, entrega_json=None):
    """-> (pdf, index_md, registros). Raises si no hay bidset o set_texto."""
    import pymupdf
    c = Ctx(workdir, entrega_json)
    b = CB.B.desde_ctx(c)
    regs = CB.cadena_detalles(b)
    st = _json(c.set_p) or {}
    labels = list((st.get("hojas") or {}).keys())
    bs = c.cfg.get("bidset_limpio") or c.cfg.get("bidset")
    bs = bs if bs and os.path.isabs(bs) else (os.path.join(c.w, bs) if bs else None)
    if not (bs and os.path.isfile(bs)):
        raise RuntimeError("entrega.json sin bidset_limpio / bidset (ruta del set) para marcar los detalles")
    src = pymupdf.open(bs)
    pag = {CB.norm_hoja(k): i for i, k in enumerate(labels) if i < src.page_count}
    ocr = {CB.norm_hoja(h) for h in st.get("ocr") or []}
    ver = b.verificadas if isinstance(b.verificadas, dict) else {}
    cache, dest, no_imp = {}, {}, {}
    for r in regs:
        key = (r["n"], r["t"])
        if key in dest or r["t"] not in pag:
            continue
        vv = next((x for kk, xs in ver.items() if CB.norm_hoja(kk) == r["t"] for x in (xs or [])
                   if isinstance(x, dict) and str(x.get("detalle_existe") or "") == r["n"] and x.get("x") is not None), None)
        if vv:
            dest[key] = (float(vv["x"]) - 20, float(vv["y"]) - 12, float(vv.get("x1") or vv["x"] + 160),
                         float(vv.get("y1") or vv["y"] + 30))
            if str(vv.get("no_impreso") or "").strip():     # BE-CC07: referenced detail not printed: nearest view, said so
                no_imp[key] = str(vv["no_impreso"]).strip()
            continue
        if r["t"] not in cache:
            cache[r["t"]] = _palabras_pagina(src[pag[r["t"]]], r["t"] in ocr)
        dest[key] = ubicar_titulo(cache[r["t"]], r["n"])
    hojas_m = sorted({r["origen"] for r in regs} | {t for (n, t), v in dest.items() if v}, key=lambda h: pag.get(h, 9999))
    out = pymupdf.open()
    nueva = {}
    for h in hojas_m:
        if h in pag:
            out.insert_pdf(src, from_page=pag[h], to_page=pag[h])
            nueva[h] = out.page_count - 1
    if nueva:                                   # Page Label = número de hoja (Bluebeam)
        orig = {CB.norm_hoja(k): k for k in labels}   # BE-CC10
        out.set_page_labels([{"startpage": i, "prefix": orig.get(h, h), "style": "", "firstpagenum": 1} for h, i in sorted(nueva.items(), key=lambda kv: kv[1])])
    rojo = (0.85, 0, 0)

    def poner(h, rect, txt, contenido):
        pg = out[nueva[h]]
        M = pg.derotation_matrix
        R_ = pymupdf.Rect(rect) * M
        a = pg.add_circle_annot(R_) if contenido.startswith("origin") else pg.add_rect_annot(R_)
        a.set_colors(stroke=rojo)
        a.set_border(width=2.5)
        a.set_info(title="take-off", subject=SUBJ_DET, content=f"{txt} {contenido}")
        a.update()
        ft = pg.add_freetext_annot(pymupdf.Rect(R_.x1 + 2, R_.y0 - 14, R_.x1 + 70, R_.y0 + 4), txt, fontsize=11,
                                   text_color=rojo, fill_color=(1, 1, 1))
        ft.set_info(title="take-off", subject=SUBJ_DET + " #", content=txt)
        ft.update()
    for i, r in enumerate(regs, 1):
        r["k"] = i
        if r["origen"] in nueva:
            rr = float(r["r"]) * 1.35
            poner(r["origen"], (r["x"] - rr, r["y"] - rr, r["x"] + rr, r["y"] + rr), f"#{i}",
                  f"origin {r['n']}/{r['t']} on {r['origen']} ({COMO_EN.get(r['como'], r['como'])})")
        d = dest.get((r["n"], r["t"]))
        r["destino_ok"] = bool(d and r["t"] in nueva)
        if r["destino_ok"]:
            poner(r["t"], d, f"#{i}", f"destination {r['n']}/{r['t']} (called from {r['origen']})"
                  + (f" - NOT PRINTED: {no_imp[(r['n'], r['t'])]}" if (r["n"], r["t"]) in no_imp else ""))
    e = c.entrega or c.w
    os.makedirs(os.path.join(e, "Planos marcados"), exist_ok=True)
    pdf = os.path.join(e, "Planos marcados", "DETALLES_REVISADOS.pdf")
    out.save(pdf, garbage=3, deflate=True)
    _sin_firmas(pdf)
    L = ["## DETALLES_REVISADOS_INDEX", "", "Every detail bubble reviewed (U-141), circled and numbered in red on its calling sheet and on "
         "its destination view in `Planos marcados/DETALLES_REVISADOS.pdf`.", "",
         "| # | Bubble | Calling sheet | Destination view | Take-off row / out of scope |", "|---|---|---|---|---|"]
    for r in regs:
        dv = f"{r['n']}/{r['t']}" + ("" if r["destino_ok"] else " (destination title not located: see the sheet)") \
            + (f" - NOT PRINTED: {no_imp[(r['n'], r['t'])]}" if (r["n"], r["t"]) in no_imp else "")
        L.append(f"| {r['k']} | {r['n']}/{r['t']} | {r['origen']} | {dv} | {DISP_EN.get(r['disp'], r['disp'])}: {str(r['motivo'])[:160]} |")
    md = os.path.join(e, "DETALLES_REVISADOS_INDEX.md")
    _escribir(md, "\n".join(L) + "\n")
    if os.path.isfile(c.readme):
        t = open(c.readme, encoding="utf-8").read()
        t = t.split("\n## DETALLES_REVISADOS_INDEX")[0].rstrip() + "\n\n" + "\n".join(L) + "\n"
        _escribir(c.readme, t)
    return pdf, md, regs


RX_FILA_OK = re.compile(r"(?i)^\s*(yes\b|(?:no|n/a)\b[^:]*:\s*\S.{9,})")


def _schedules_json(c):
    p = c.cfg.get("schedules_materiales") or "schedules_materiales.json"
    p = p if os.path.isabs(p) else os.path.join(c.w, p)
    return p, (_json(p) if os.path.isfile(p) else None)


def _fila_estado(r):
    """U-142: la fila de un schedule nuestro queda resuelta si está en el canon ('yes ...'), fuera de alcance con motivo,
    o 'no: / n/a: <motivo>' (no usada en el proyecto, nota general)."""
    return bool(RX_FILA_OK.match(str(r.get("in_canon") or "")) or str(r.get("out_of_scope") or "").strip())


def marcar_schedules_json(workdir, entrega_json=None):
    """U-142 (usuario 5-nov: 'revisa todos los schedules que nos pertenezcan y haz una lista de cada material, y marca cada
    partition type para saber que lo revisaste'): lee schedules_materiales.json [{sheet, page, title, title_bbox, ours, why,
    rows: [{type, bbox, row_text, materials: [{material, spec, source}], in_canon, out_of_scope}]}] y escribe
    Planos marcados/SCHEDULES_REVISADOS.pdf (solo las hojas con schedule, Page Label = hoja): título en rectángulo rojo, cada
    fila circulada en rojo con palomita y número; + SCHEDULES_MATERIALES.md (cada fila -> cada material, N/HOJA, estado)."""
    import pymupdf
    c = Ctx(workdir, entrega_json)
    p, sch = _schedules_json(c)
    if not sch:
        raise RuntimeError(f"no hay {p} (lista de schedules del trade, U-142)")
    bs = c.cfg.get("bidset_limpio") or c.cfg.get("bidset")
    bs = bs if bs and os.path.isabs(bs) else (os.path.join(c.w, bs) if bs else None)
    if not (bs and os.path.isfile(bs)):
        raise RuntimeError("entrega.json sin bidset_limpio / bidset (ruta del set) para marcar los schedules")
    src = pymupdf.open(bs)
    pags = sorted({int(x["page"]) for x in sch if x.get("page")})
    out = pymupdf.open()
    nueva, lab = {}, {}
    for pg in pags:
        out.insert_pdf(src, from_page=pg - 1, to_page=pg - 1)
        nueva[pg] = out.page_count - 1
        lab[pg] = next(str(x["sheet"]) for x in sch if int(x.get("page") or 0) == pg)
    if nueva:
        out.set_page_labels([{"startpage": i, "prefix": lab[pg], "style": "", "firstpagenum": 1} for pg, i in sorted(nueva.items(), key=lambda kv: kv[1])])
    rojo = (1, 0, 0)
    k = 0
    L = ["## SCHEDULES_MATERIALES", "", "Every schedule of our trade reviewed (each row circled, checked and numbered in red in "
         "`Planos marcados/SCHEDULES_REVISADOS.pdf`); each row -> each material, with its sheet and how the take-off uses it.", "",
         "| # | Sheet | Schedule | Row / type | Materials (as printed) | Take-off | Out of scope |", "|---|---|---|---|---|---|---|"]
    for x in sch:
        pg = out[nueva[int(x["page"])]]
        M = pg.derotation_matrix
        if x.get("title_bbox"):
            a = pg.add_rect_annot(pymupdf.Rect(x["title_bbox"]) * M)
            a.set_colors(stroke=rojo)
            a.set_border(width=3)
            a.set_info(title="take-off", subject=SUBJ_SCH + " TITLE",
                       content=f"{x['title']} ({x['sheet']}) - {'ours' if x.get('ours') else 'not ours'}: {str(x.get('why') or '')[:200]}")
            a.update()
        for r in x.get("rows") or []:
            k += 1
            r["k"] = k
            bb = r.get("bbox")
            if bb and len(bb) == 4:
                R_ = pymupdf.Rect(bb) * M
                R_ = pymupdf.Rect(R_.x0 - 6, R_.y0 - 5, R_.x1 + 6, R_.y1 + 5)
                mats = "; ".join(f"{m.get('material')} {m.get('spec') or ''}".strip() for m in r.get("materials") or [])
                a = pg.add_circle_annot(R_)
                a.set_colors(stroke=rojo)
                a.set_border(width=3)
                a.set_info(title="take-off", subject=SUBJ_SCH,
                           content=f"#{k} {r.get('type')} ({x['sheet']}) reviewed: {mats[:600]} | take-off: {str(r.get('in_canon') or '')[:200]}"
                                   + (f" | out of scope: {r['out_of_scope'][:200]}" if r.get("out_of_scope") else ""))
                a.update()
                ink = [[(R_.x1 + 2, R_.y0 + (R_.y1 - R_.y0) * 0.55), (R_.x1 + 6, R_.y1), (R_.x1 + 14, R_.y0 - 2)]]
                ck = pg.add_ink_annot(ink)
                ck.set_colors(stroke=rojo)
                ck.set_border(width=3)
                ck.set_info(title="take-off", subject=SUBJ_SCH + " CHECK", content=f"#{k}")
                ck.update()
                ft = pg.add_freetext_annot(pymupdf.Rect(R_.x1 + 16, R_.y0 - 4, R_.x1 + 56, R_.y0 + 12), f"#{k}", fontsize=10,
                                           text_color=rojo, fill_color=(1, 1, 1))
                ft.set_info(title="take-off", subject=SUBJ_SCH + " #", content=f"#{k}")
                ft.update()
            mats = "<br>".join(f"{m.get('material')} - {m.get('spec') or ''} ({m.get('source') or x['sheet']})" for m in r.get("materials") or [])
            L.append(f"| {k} | {x['sheet']} | {x['title']} | {r.get('type')} | {mats or '-'} | {str(r.get('in_canon') or '-')[:220]} | "
                     f"{str(r.get('out_of_scope') or ('not our schedule: ' + str(x.get('why') or '')[:120] if not x.get('ours') else '-'))[:220]} |")
    e = c.entrega or c.w
    os.makedirs(os.path.join(e, "Planos marcados"), exist_ok=True)
    pdf = os.path.join(e, "Planos marcados", "SCHEDULES_REVISADOS.pdf")
    out.save(pdf, garbage=3, deflate=True)
    _sin_firmas(pdf)
    md = os.path.join(e, "SCHEDULES_MATERIALES.md")
    _escribir(md, "\n".join(L) + "\n")
    return pdf, md, k


@chequeo("CE_SCHEDULES_REVISADOS", ["U-142"], "U-142: todos los schedules del trade revisados: schedules_materiales.json con cada "
         "fila -> materiales y estado (en el take-off / fuera de alcance con motivo / no usada con motivo), y cada fila marcada "
         "(círculo + palomita + número) en Planos marcados/SCHEDULES_REVISADOS.pdf; falta una o 0 = FAIL")
def ce_schedules_revisados(c):
    import pymupdf
    p, sch = _schedules_json(c)
    if not sch:
        return R("FAIL", f"no hay {os.path.basename(p)} (U-142: lista de cada schedule del trade, fila por fila, con sus materiales)")
    k = 0
    for x in sch:                                  # mismo orden que marcar_schedules: el número de la fila
        for r in x.get("rows") or []:
            k += 1
            r["k"] = k
    nuestros = [x for x in sch if x.get("ours")]
    filas = [(x, r) for x in nuestros for r in x.get("rows") or []]
    if not filas:
        return R("FAIL", "0 filas en schedules del trade (U-142: 0 = FAIL)")
    ev = []
    for x, r in filas:
        tag = f"{r.get('type')} ({x.get('sheet')} {x.get('title')})"
        if not (r.get("bbox") and len(r["bbox"]) == 4):
            ev.append(f"{tag}: sin bbox (no se puede marcar)")
        if not r.get("materials") and not str(r.get("in_canon") or "").lower().startswith("n/a"):
            ev.append(f"{tag}: sin lista de materiales")
        if not _fila_estado(r):
            ev.append(f"{tag}: sin estado (en el take-off / fuera de alcance / no usada, con motivo)")
    pdf = os.path.join(c.planos, "SCHEDULES_REVISADOS.pdf")
    if not os.path.isfile(pdf):
        ev.append("no hay Planos marcados/SCHEDULES_REVISADOS.pdf: correr `compuerta_entrega.py schedules <carpeta>`")
    else:
        n = {}
        for pg in pymupdf.open(pdf):
            for a in pg.annots() or []:
                inf = a.info or {}
                if inf.get("subject") in (SUBJ_SCH, SUBJ_SCH + " CHECK"):
                    m = re.match(r"#(\d+)", inf.get("content") or "")
                    if m:
                        n.setdefault(int(m.group(1)), set()).add(inf["subject"])
        for x, r in filas:
            if len(n.get(int(r["k"]), ())) < 2 and r.get("bbox"):
                ev.append(f"{r.get('type')} ({x.get('sheet')}): fila sin círculo + palomita en SCHEDULES_REVISADOS.pdf")
                break
        tot = sum(len(x.get("rows") or []) for x in sch)
        if len(n) < tot:
            ev.append(f"SCHEDULES_REVISADOS.pdf marca {len(n)} de {tot} filas")
    if not os.path.isfile(os.path.join(c.entrega or c.w, "SCHEDULES_MATERIALES.md")):
        ev.append("no hay SCHEDULES_MATERIALES.md (la lista de materiales por fila)")
    if ev:
        return R("FAIL", *ev[:20])
    return R("PASS", f"{len(nuestros)} schedules del trade, {len(filas)} filas revisadas, materiales listados y marcadas")


@chequeo("CE_DETALLES_CIRCULADOS", ["U-141"], "U-141: cada burbuja de la cadena (detector + verificadas a ojo) circulada y "
         "numerada en su hoja de origen y en su vista destino en Planos marcados/DETALLES_REVISADOS.pdf; falta una o 0 = FAIL")
def ce_detalles_circulados(c):
    import pymupdf
    b = CB.B.desde_ctx(c)
    regs = CB.cadena_detalles(b)
    if not regs:
        return R("FAIL", "0 burbujas en la cadena de detalles: no hay nada circulado (U-137 / U-141: 0 = FAIL)")
    pdf = os.path.join(c.planos, "DETALLES_REVISADOS.pdf")
    if not os.path.isfile(pdf):
        return R("FAIL", f"no hay Planos marcados/DETALLES_REVISADOS.pdf ({len(regs)} burbujas en la cadena sin circular): "
                         "correr `compuerta_entrega.py detalles <carpeta>`")
    ori, des = set(), set()
    doc = pymupdf.open(pdf)
    for p in doc:
        for a in p.annots() or []:
            inf = a.info or {}
            if inf.get("subject") != SUBJ_DET:
                continue
            m = re.match(r"#(\d+) (origin|destination) (\S+)", inf.get("content") or "")
            if m:
                (ori if m.group(2) == "origin" else des).add((m.group(3), p.get_label() or ""))
    ev = []
    _en_set = {CB.norm_hoja(h) for h in (b.hojas or {})}
    for i, r in enumerate(regs, 1):
        nt = f"{r['n']}/{r['t']}"
        if not any(k == nt for k, _ in ori):
            ev.append(f"#{i} {nt} (en {r['origen']}): sin círculo en la hoja de origen")
        if not any(k == nt for k, _ in des) and (not _en_set or CB.norm_hoja(r["t"]) in _en_set):   # BE-CR23: hoja que no está en el set = sin destino que marcar
            ev.append(f"#{i} {nt}: sin marca en su vista destino {r['t']} (verificarla a ojo: burbujas_verificadas.json "
                      f"{{hoja: [{{detalle_existe, x, y, img}}]}})")
    sin = [r for r in regs if r["disp"] == "sin disposición"]
    ev += [f"{r['n']}/{r['t']} (en {r['origen']}): sin disposición" for r in sin[:10]]
    # BE-CC07: count against the UNION detector + burbujas_verificadas + CADENA.md, sheet by sheet: a sheet with bubbles and
    # no origin circle = FAIL; fewer origin circles than bubbles on a sheet = FAIL (BE-CC07: the sheets the chain never reached passed)
    lab = {}
    for p in doc:
        for a in p.annots() or []:
            inf = a.info or {}
            if inf.get("subject") == SUBJ_DET and re.match(r"#\d+ origin ", inf.get("content") or ""):
                lab[CB.norm_hoja(p.get_label() or "")] = lab.get(CB.norm_hoja(p.get_label() or ""), 0) + 1
    ev += CB.faltan_circulos(b, lab)
    ev += _es_annots_pdf(pdf)[:10]
    if ev:
        return R("FAIL", f"{len(ev)} faltante(s) de {len(regs)} burbujas", *ev[:30])
    po = {}
    for r in regs:
        po[r["origen"]] = po.get(r["origen"], 0) + 1
    _disc = {}
    for h, n in po.items():
        _disc[str(h)[:1]] = _disc.get(str(h)[:1], 0) + n
    return R("PASS", f"{len(regs)} burbujas circuladas en origen y destino en {doc.page_count} hojas; por hoja de origen: "
             + ", ".join(f"{h} {n}" for h, n in po.items()),
             "conteos (CR-R10-m3): este total = TODAS las burbujas de todas las hojas de origen del set, por disciplina "
             + ", ".join(f"{k} {v}" for k, v in sorted(_disc.items())) + "; CE_CALLOUTS cuenta los destinos N/HOJA únicos citados y las "
             "burbujas de las hojas alcanzadas por la cadena del trade (subconjunto)")


# ----------------------------------------------------------------------------------------------- correr
def correr(workdir, entrega_json=None, solo=None):
    c = Ctx(workdir, entrega_json)
    reg = registro() or {}
    por_chequeo = {}
    for e in reg.get("reglas") or []:
        if e.get("categoria") == "programa" and e.get("cuando") == "entrega":
            for ch in e.get("chequeos") or []:
                nm = ch.split("::")[-1]
                por_chequeo.setdefault("ce_reglas" if nm.startswith("A_") else nm, []).append(e["id"])
    res = []
    for cid, reglas_, desc, fn in CHEQUEOS:
        if solo and cid not in solo:
            continue
        try:
            est, ev = fn(c)
        except Exception as e:                                          # noqa: BLE001 — un chequeo roto = FAIL
            est, ev = "FAIL", [f"el chequeo no corrió: {type(e).__name__}: {e}"]
        ids = sorted(set(reglas_) | set(por_chequeo.get(fn.__name__, [])) | set(por_chequeo.get(cid, [])))
        res.append({"id": cid, "reglas": ids, "descripcion": desc, "estado": est, "evidencia": ev})
    try:
        auditar_compuerta(res, esperado_proyecto(c))
        otros = [r["id"] for r in res if r["estado"] == "FAIL" and r["id"] != "CE_RFI_LISTO"]
        ab = [r for r in c.rfis() if isinstance(r, dict) and str(r.get("status") or "").lower() == "open" and not r.get("pending")]
        for r in res:                                        # U-179: con errores abiertos no se presenta ningún RFI
            if r["id"] == "CE_RFI_LISTO" and otros and ab:
                r["estado"] = "FAIL"
                r["evidencia"] = [f"{len(ab)} RFI abiertos ({', '.join(str(x.get('id')) for x in ab[:6])}) con {len(otros)} chequeo(s) en FAIL "
                                  f"({', '.join(otros[:6])}): corregir los errores ANTES de preguntar (U-179)"] + list(r["evidencia"])
    except Exception as e:                                              # noqa: BLE001
        res.append({"id": "CE_PLAUSIBILIDAD", "reglas": ["U-138"], "descripcion": "auditar_compuerta", "estado": "FAIL",
                    "evidencia": [f"auditar_compuerta no corrió: {type(e).__name__}: {e}"]})
    archivos = {os.path.relpath(p, c.w): _sha(p) for p in c.archivos_entrega()}
    n = {k: sum(r["estado"] == k for r in res) for k in ("PASS", "AMBER", "FAIL")}
    ahora = datetime.datetime.now(datetime.timezone.utc)
    try:
        from zoneinfo import ZoneInfo
        ca = ahora.astimezone(ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d %H:%M %Z")
    except Exception:                                                   # noqa: BLE001
        ca = ""
    out = {"version": VERSION, "fecha_california": ca, "fecha_iso": ahora.isoformat(), "workdir": c.w,
           "entrega_dir": os.path.relpath(c.entrega, c.w) if c.entrega else None, "ok": n["FAIL"] == 0 and not solo,
           "resumen": n, "chequeos": res, "archivos": archivos, "drive": c.cfg.get("drive") or {},
           # U-177 (1) / BE-AUD01: ENTREGA_OK is valid only for the files it validated (name + sha256) and this skill version
           "vigente": {k: ({"nombre": os.path.basename(v), "sha256": _sha(v)} if v and os.path.isfile(v) else None)
                       for k, v in (("markups_pdf", getattr(c, "markups", None)), ("excel", getattr(c, "excel", None)))},
           "skill_version": _skill_version(),
           "registro": (reg.get("version") if reg else None)}
    if c.entrega:                                                      # U-177 (1): hash de lo VIGENTE que validó esta compuerta
        vg, _ev = vigentes_entrega(c.entrega)
        out["vigentes"] = {k: {"nombre": os.path.basename(p), "sha256": _sha(p), "md5": _md5(p)} for k, p in vg.items() if p}
    return out


MIN_TEXTO = 200          # R80e.151 (O'Reilly rev5): una hoja con menos caracteres = raster sin capa de texto -> OCR


def _tessdata():
    for d in (os.environ.get("TESSDATA_PREFIX"), "/usr/share/tesseract-ocr/5/tessdata", "/usr/share/tesseract-ocr/4.00/tessdata",
              "/usr/share/tessdata", "/usr/local/share/tessdata"):
        if d and os.path.isfile(os.path.join(d, "eng.traineddata")):
            return d
    return None


def _en_blanco(p):
    """página sin tinta: < 0.05 % de píxeles oscuros a 20 dpi en gris."""
    import pymupdf
    px = p.get_pixmap(dpi=20, colorspace=pymupdf.csGRAY)
    s_ = px.samples
    return sum(1 for b in s_ if b < 200) < 0.0005 * max(len(s_), 1)


RX_DE_N = re.compile(r"\b([A-Z]{1,3}-?\d{1,3}(?:\.\d{1,2})?[A-Z]?)\s+(?:of|OF)\s+\d{1,3}\b")


def _rotulo_esquina(p, td):
    """R80e.151: número de hoja del title block por OCR de la esquina inferior derecha ('E4 of 4', 'M1 of 3', 'A1.1');
    dos recortes (el title block cambia de proporción entre disciplinas), el primero que lee gana."""
    import pymupdf
    os.environ.setdefault("TESSDATA_PREFIX", td)
    r = p.rect
    for x0, y0, dpi in ((0.90, 0.86, 150), (0.93, 0.88, 150), (0.86, 0.80, 200), (0.93, 0.88, 300)):
        try:
            pix = p.get_pixmap(dpi=dpi, clip=pymupdf.Rect(r.width * x0, r.height * y0, r.width * 0.985, r.height))
            t = pymupdf.open("pdf", pix.pdfocr_tobytes(tessdata=td))[0].get_text("text")
        except Exception:                               # noqa: BLE001
            continue
        m = RX_DE_N.findall(t) or re.findall(r"\b[A-Z]{1,3}-?\d{1,3}\.\d{1,2}[A-Z]?\b", t)
        if m:
            return m[-1]
    return None


RX_HOJA_TRADE = re.compile(r"^(?:A|AD|AE|AS|AF|I|ID|IN|S|D|G|Q|K|F)[-\d]", re.I)   # U-137: disciplinas donde se barren burbujas


def _burbujas_set(pdfs, hojas_lab, solo=None):
    """U-137 / BE-139: burbujas de detalle de dos líneas (número arriba / hoja abajo) por hoja, con palabras_fitz.py (burbujas).
    Se barren las hojas de arquitectura / estructura / interiores / generales (no MEP / civil / paisaje: no son del trade)."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import palabras_fitz as burbujas
    import pymupdf
    lista = sorted({k.split("#")[0] for k in hojas_lab.values() if not k.startswith("p")})
    out = {}
    for pdf in pdfs:
        doc = pymupdf.open(pdf)
        for i, p in enumerate(doc):
            k = hojas_lab.get((os.path.basename(pdf), i))
            if not k or (solo and k not in solo) or (not solo and not RX_HOJA_TRADE.match(k)):
                continue
            try:
                out[k] = burbujas.detectar(p, lista, raster_pag=len(p.get_text("text").strip()) < MIN_TEXTO)
                # BE-CC09 (Consumer Cellular rev2, 5-nov): the detector reads the page UNROTATED (raw drawings / words);
                # the bubble positions are stored in the VISIBLE frame (the frame of burbujas_verificadas and of the
                # DETALLES_REVISADOS circles, which apply derotation_matrix). Before, on a page with rotation 270 every
                # detector circle landed in the wrong place and the same bubble read by eye was counted twice.
                out[k]["frame"] = "visible"
                out[k]["rotation"] = p.rotation
                if p.rotation:
                    for x in out[k].get("burbujas") or []:
                        q = pymupdf.Point(x["x"], x["y"]) * p.rotation_matrix
                        x["x_raw"], x["y_raw"], x["x"], x["y"] = x["x"], x["y"], round(q.x, 1), round(q.y, 1)
            except Exception as e:                      # noqa: BLE001 — una hoja que no se puede barrer queda marcada
                out[k] = {"burbujas": [], "sin_leer": [], "circulos": 0, "error": str(e)[:200]}
    return out


def texto_set(pdfs, salida, dpi=200):
    """Texto de cada hoja del set (texto + anotaciones, p. ej. AutoCAD SHX Text) con su número de hoja.
    R80e.151 (O'Reilly rev5): las hojas RASTER (sin capa de texto: < MIN_TEXTO caracteres) se pasan por OCR (tesseract vía
    pymupdf); si no hay OCR quedan en 'sin_texto' y el chequeo BE-120 FALLA con RFI abiertos (barrido ciego)."""
    import pymupdf
    hojas, fuentes, ocr, sin, blanco = {}, [], [], [], []
    pag_lab = {}
    td = _tessdata()
    for pdf in pdfs:
        doc = pymupdf.open(pdf)
        fuentes.append({"pdf": os.path.basename(pdf), "paginas": doc.page_count})
        for p in doc:
            t = p.get_text("text")
            raster = len(t.strip()) < MIN_TEXTO
            leido = False
            if raster and td:
                try:
                    o = p.get_textpage_ocr(dpi=dpi, full=True, tessdata=td).extractText()
                    t += "\n" + o
                    leido = len(o.strip()) >= 20
                except Exception:                      # noqa: BLE001 — una hoja que no se puede leer queda sin texto
                    pass
            t += "\n" + "\n".join((a.info or {}).get("content") or "" for a in (p.annots() or []))
            lab = hoja_de_etiqueta(p.get_label())
            if not lab:
                W, H = p.rect.width, p.rect.height
                M = p.rotation_matrix          # v81cf24: words vienen en coordenadas SIN rotar; el title block se busca en la hoja vista
                cands = [(r.height, w[4]) for w in p.get_text("words") if RX_HOJA_TB.match(w[4])
                         for r in [pymupdf.Rect(w[:4]) * M] if r.x0 > 0.75 * W and r.y0 > 0.7 * H]
                # v81cf25 (BE-CF05): sin número de hoja en la capa de texto (title block vectorizado / raster) = hoja MARCADA
                lab = max(cands)[1] if cands else f"p{p.number + 1}"
            if lab.startswith("p") and raster:          # rótulo de hoja de la capa OCR (title block, esquina inf. der.)
                m = [x for x in re.findall(r"\b[A-Z]{1,3}-?\d{1,3}\.\d{1,2}[A-Z]?\b", t[-600:])]
                if m:
                    lab = m[-1]
                elif td:
                    lab = _rotulo_esquina(p, td) or lab
            if re.fullmatch(r"p\d+", lab):           # v81cf25 CFA (BE-CF05): sin número de hoja impreso legible = hoja MARCADA
                lab += "-vector"
            k, n = lab, 2
            while k in hojas:
                k, n = f"{lab}#{n}", n + 1
            hojas[k] = t
            pag_lab[(os.path.basename(pdf), p.number)] = k
            if raster:
                if leido:
                    ocr.append(k)
                elif _en_blanco(p):                   # página sin tinta (separador): no hay nada que barrer
                    blanco.append(k)
                else:
                    sin.append(k)
    bub = _burbujas_set(pdfs, pag_lab)
    json.dump({"fuentes": fuentes, "hojas": hojas, "ocr": ocr, "sin_texto": sin, "en_blanco": blanco, "burbujas": bub,
               "burbujas_detector": "palabras_fitz.py (burbujas) U-137"}, open(salida, "w", encoding="utf-8"), ensure_ascii=False)
    return hojas


def main(argv):
    if len(argv) > 1 and argv[1] == "banco":
        a = argv[2:]
        if not a:
            print(__doc__)
            return 2
        cr = a[a.index("--cache") + 1] if "--cache" in a else "."
        c = Ctx(a[0])
        if not c.excel:
            print("sin Excel en la carpeta de entrega")
            return 2
        refs = [(n, os.path.join(cr, r)) for n, r in BANCO_REFS]
        sal = os.path.join(c.w, "COMPARATIVA_BANCO.md")
        fuera = banco_md(c.excel, refs, sal)
        print(f"COMPARATIVA_BANCO.md: {len(fuera)} familia(s) fuera de rango {fuera} -> {sal}")
        return 0
    if len(argv) > 1 and argv[1] == "pdf_editable":
        # compuerta_entrega.py pdf_editable <pdf> [...] : U-151 / BE-147, el mismo chequeo de CE_PDF_EDITABLE sobre PDFs sueltos
        malo = False
        for p in argv[2:]:
            fs, info = pdf_editable(p)
            malo = malo or bool(fs)
            print(("FAIL " if fs else "PASS ") + f"CE_PDF_EDITABLE {os.path.basename(p)}: {info['paginas']} páginas, "
                  f"{info['firmas']} firma(s) /Sig, {info['labels_unicos']} Page Labels únicos, "
                  f"{info.get('paginas_escala', 0)} página(s) con /Measure: /VP {info.get('escalas', {})}")
            for x in fs:
                print("        - " + x[:220])
        return 1 if malo or len(argv) < 3 else 0
    if len(argv) > 1 and argv[1] == "vista_bluebeam":
        # compuerta_entrega.py vista_bluebeam <markups.pdf> <excel.xlsx> [--canon c.json] [--csv VISTA_BLUEBEAM.csv]: U-153 / BE-149
        a = argv[2:]
        cn = a[a.index("--canon") + 1] if "--canon" in a else None
        cs = a[a.index("--csv") + 1] if "--csv" in a else None
        filas, fs, info = vista_bluebeam(a[0], a[1], cn)
        if cs:
            vista_csv(filas, cs)
        print(("FAIL " if fs else "PASS ") + f"CE_VISTA_BLUEBEAM {os.path.basename(a[0])}: {info['markups']} markups revisados "
              f"({info['ok']} OK), {info['paginas']} hojas, {info['renglones']} renglones del Excel" + (f" -> {cs}" if cs else ""))
        for x in fs[:60]:
            print("        - " + x[:260])
        return 1 if fs else 0
    if len(argv) > 1 and argv[1] == "schedules":
        # compuerta_entrega.py schedules <carpeta> : U-142, Planos marcados/SCHEDULES_REVISADOS.pdf + SCHEDULES_MATERIALES (README)
        # con lectura independiente (schedules_indep.json, U-111) = marcar_schedules (cruce con el Material Summary, escribe
        # también schedules_materiales.json); sin ella, la lista escrita a mano schedules_materiales.json = marcar_schedules_json
        if _ultimo(["schedules_indep.json", "**/schedules_indep.json"], argv[2]):
            pdf, md, lst = marcar_schedules(argv[2])
            nm = sum(1 for x in lst if x.get("pos"))
            print(f"schedules: {len({(x['schedule'], x['hoja']) for x in lst})} schedules, {len(lst)} types / renglones, "
                  f"{nm} marcados, {sum(len(x['materiales']) for x in lst)} materiales -> {pdf}")
        else:
            pdf, md, k = marcar_schedules_json(argv[2])
            print(f"schedules: {k} filas marcadas -> {pdf}; lista {md}")
        return 0
    if len(argv) > 1 and argv[1] == "detalles":
        # compuerta_entrega.py detalles <carpeta> : U-141, Planos marcados/DETALLES_REVISADOS.pdf + índice (y README)
        pdf, md, regs = marcar_detalles(argv[2])
        nd = sum(1 for r in regs if r.get("destino_ok"))
        print(f"detalles: {len(regs)} burbujas circuladas en origen, {nd} con su vista destino -> {pdf}; índice {md}")
        return 0
    if len(argv) > 1 and argv[1] == "burbujas":
        # compuerta_entrega.py burbujas <set_texto.json> <bidset.pdf> [...]: agrega el barrido de burbujas (U-137) a un
        # set_texto.json existente, sin repetir el OCR. Las etiquetas de hoja se toman del orden de páginas del set_texto.
        a = argv[2:]
        stp, pdfs = a[0], a[1:]
        st = _json(stp) or {}
        keys = list((st.get("hojas") or {}).keys())
        pag_lab, j = {}, 0
        for pdf in pdfs:
            import pymupdf
            for i in range(pymupdf.open(pdf).page_count):
                if j < len(keys):
                    pag_lab[(os.path.basename(pdf), i)] = keys[j]
                j += 1
        st["burbujas"] = _burbujas_set(pdfs, pag_lab)
        st["burbujas_detector"] = "palabras_fitz.py (burbujas) U-137"
        json.dump(st, open(stp, "w", encoding="utf-8"), ensure_ascii=False)
        nb = sum(len(v["burbujas"]) for v in st["burbujas"].values())
        ns = sum(len(v["sin_leer"]) for v in st["burbujas"].values())
        print(f"burbujas: {len(st['burbujas'])} hojas barridas, {nb} leídas, {ns} sin leer -> {stp}")
        return 0
    if len(argv) > 1 and argv[1] == "texto":
        a = argv[2:]
        if "--out" not in a:
            print(__doc__)
            return 2
        i = a.index("--out")
        sal, pdfs = a[i + 1], a[:i] + a[i + 2:]
        h = texto_set(pdfs, sal)
        st = _json(sal) or {}
        print(f"set_texto: {len(h)} hojas -> {sal} (OCR {len(st.get('ocr') or [])}, sin texto {len(st.get('sin_texto') or [])})")
        return 0
    if len(argv) < 2:
        print(__doc__)
        return 2
    ej = argv[argv.index("--entrega") + 1] if "--entrega" in argv else None
    out = correr(argv[1], ej)
    p = os.path.join(out["workdir"], "ENTREGA_OK.json")
    json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    vg = out.get("vigentes") or {}                                     # U-184 (2)(7): registro de corridas completas de la compuerta
    with open(os.path.join(out["workdir"], "compuerta_corridas.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": out["fecha_iso"], "entrega_dir": out.get("entrega_dir"), "ok": out["ok"], "resumen": out["resumen"],
                            "excel": (vg.get("excel") or {}).get("sha256"), "pdf": (vg.get("pdf") or {}).get("sha256")}) + "\n")
    for r in out["chequeos"]:
        print(f"{r['estado']:5} {r['id']:24} {', '.join(r['reglas'])[:60]}")
        if r["estado"] != "PASS":
            for e in r["evidencia"][:6]:
                print("        - " + e[:220])
    n = out["resumen"]
    print(f"COMPUERTA DE ENTREGA: PASS {n['PASS']} / AMBER {n['AMBER']} / FAIL {n['FAIL']} -> "
          + ("VERDE (se puede subir con subir_entrega.py)" if out["ok"] else "ROJA: NO SE ENTREGA") + f"\n{p}")
    return 0 if out["ok"] else 1



def _sin_firmas(pdf):
    """BE-CR31 (CR City Hotel rev4, v81cf61): DETALLES_REVISADOS / SCHEDULES_REVISADOS se arman con insert_pdf del bid set y heredaban
    su AcroForm de firma (/SigFlags 3): CE_PDF_EDITABLE FAIL. Al guardar se quitan firmas / SigFlags / Perms conservando las Page Labels."""
    import shutil
    import tempfile
    import pymupdf
    import quitar_firmas_labels
    d = pymupdf.open(pdf)
    labs = {i + 1: d[i].get_label() for i in range(d.page_count)}
    d.close()
    fd, tmp = tempfile.mkstemp(suffix=".pdf", dir=os.path.dirname(os.path.abspath(pdf)))
    os.close(fd)
    try:
        quitar_firmas_labels.quitar(pdf, tmp, {k: v for k, v in labs.items() if v})
        shutil.move(tmp, pdf)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
