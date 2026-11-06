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
  python3 compuerta_entrega.py burbujas <set_texto.json> <bidset.pdf> [...]   (agrega solo las burbujas a un set_texto ya hecho)
      Extrae por PROGRAMA el texto de cada hoja (texto + contenido de anotaciones, p. ej. "AutoCAD SHX Text") con su
      número de hoja (title block). Lo usa el chequeo BE-120.

Chequeos (id → reglas): ver CHEQUEOS abajo y REGLAS_REGISTRO.json. AMBER no bloquea pero se reporta.
"""
import datetime
import glob
import hashlib
import json
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


def _ultimo(patrones, raiz):
    for pat in patrones:
        xs = sorted(glob.glob(os.path.join(raiz, pat), recursive=True))
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
                                             if not os.path.basename(p).startswith(("DETALLES_REVISADOS", "SCHEDULES_REVISADOS"))), None)
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
    ("Planos marcados/*_type_*.png", "imagen por type"),
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


@chequeo("CE_DATOS_PROYECTO", ["U-077", "R-ALC-09", "BE-114"], "hoja de datos del proyecto + hojas obligatorias en takeoff.json, "
         "Inputs del Excel, README_REVIEW y PARA_REVISAR (reglas.datos_proyecto_fallas)")
def ce_datos_proyecto(c):
    import reglas
    if not c.tk:
        return R("FAIL", "no hay takeoff.json con proyecto_datos / hojas_revisadas")
    fs = reglas.datos_proyecto_fallas(c.tk, c.excel, [c.readme, c.para])
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


@chequeo("CE_TIEMPOS", ["U-094"], "TIEMPOS.md con hora de inicio / fin (hora de California) de cada paso 1–9 y TOTAL")
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
    return R("FAIL", *ev) if ev else R("PASS", f"pasos 1–9 con hora; {os.path.relpath(c.tiempos, c.w)}")


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


def _terminos(r):
    b = r.get("barrido") if isinstance(r.get("barrido"), dict) else {}
    ts = [str(t) for t in (b.get("terminos") or []) if str(t).strip()]
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


RX_NO_IMPRESO_RFI = re.compile(r"(?i)\bnot (?:printed|shown|dimensioned|indicated|located)\b|\bno impres|\bno (?:se )?muestra")


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
        if not list(p.annots() or []):
            continue
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
    cub = {id(f) for t in fj["types"] for f in sel(t)}
    calc = c.cfg.get("calc_dir") and os.path.join(c.w, c.cfg["calc_dir"]) or os.path.join(os.path.dirname(c.canon_p), "out")
    sm = RV.sumas(ms, filas, calc)
    rojo = [f"type {r['type']}: " + "; ".join(f"{x['field']} schedule {x['schedule']} / Excel {x['excel']}" for x in r["checks"]
                                               if x["status"] == "RED") for r in res if r["verdict"] == "RED"]
    rojo += [f"Material Summary fila {s['row']} '{s['material'][:50]}': {s['note'][:120]}" for s in sm if s["status"] == "RED"]
    amb = [f"type {r['type']}: AMBER (el schedule no lo dice)" for r in res if r["verdict"] == "AMBER"]
    amb += [f"walls fuera del schedule: {f['type']} {f['wall']}" for f in filas if id(f) not in cub]
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
    open(salida, "w", encoding="utf-8").write("\n".join(L) + "\n")
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
# Orden del usuario 3-nov ("haz los programas"): las reglas que eran "programa-pendiente" (127 BE-* + U-017 / U-026 /
# U-034 / U-035 / U-037 / U-043 / U-051 / U-057 / U-058 / U-079 / U-081 / U-082 / R-ALC-02 / R-ALC-04 / R-ALC-10) y
# CE_CALLOUTS (U-113 / BE-124, cadena de burbujas N/HOJA hasta el final) corren aquí, una línea por regla en ENTREGA_OK.json.
import chequeos_biblioteca as CB  # noqa: E402


def _cb(fn):
    def w(c):
        return fn(CB.B.desde_ctx(c))
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
    open(md, "w", encoding="utf-8").write("\n".join(L) + "\n")
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
        open(c.readme, "w", encoding="utf-8").write(t)
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
    L = ["## DETALLES_REVISADOS_INDEX", "", "Every detail bubble reviewed (U-141), circled and numbered in red on its calling sheet and on "
         "its destination view in `Planos marcados/DETALLES_REVISADOS.pdf`.", "",
         "| # | Bubble | Calling sheet | Destination view | Take-off row / out of scope |", "|---|---|---|---|---|"]
    for r in regs:
        dv = f"{r['n']}/{r['t']}" + ("" if r["destino_ok"] else " (destination title not located: see the sheet)") \
            + (f" - NOT PRINTED: {no_imp[(r['n'], r['t'])]}" if (r["n"], r["t"]) in no_imp else "")
        L.append(f"| {r['k']} | {r['n']}/{r['t']} | {r['origen']} | {dv} | {DISP_EN.get(r['disp'], r['disp'])}: {str(r['motivo'])[:160]} |")
    md = os.path.join(e, "DETALLES_REVISADOS_INDEX.md")
    open(md, "w", encoding="utf-8").write("\n".join(L) + "\n")
    if os.path.isfile(c.readme):
        t = open(c.readme, encoding="utf-8").read()
        t = t.split("\n## DETALLES_REVISADOS_INDEX")[0].rstrip() + "\n\n" + "\n".join(L) + "\n"
        open(c.readme, "w", encoding="utf-8").write(t)
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
    md = os.path.join(e, "SCHEDULES_MATERIALES.md")
    open(md, "w", encoding="utf-8").write("\n".join(L) + "\n")
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
        if not any(k == nt for k, _ in des) and CB.norm_hoja(r["t"]) in _en_set:   # BE-CR23: hoja que no está en el set = sin destino que marcar
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
    return R("PASS", f"{len(regs)} burbujas circuladas en origen y destino en {doc.page_count} hojas; por hoja de origen: "
             + ", ".join(f"{h} {n}" for h, n in po.items()))


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
           "registro": (reg.get("version") if reg else None)}
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
    for r in out["chequeos"]:
        print(f"{r['estado']:5} {r['id']:24} {', '.join(r['reglas'])[:60]}")
        if r["estado"] != "PASS":
            for e in r["evidencia"][:6]:
                print("        - " + e[:220])
    n = out["resumen"]
    print(f"COMPUERTA DE ENTREGA: PASS {n['PASS']} / AMBER {n['AMBER']} / FAIL {n['FAIL']} -> "
          + ("VERDE (se puede subir con subir_entrega.py)" if out["ok"] else "ROJA: NO SE ENTREGA") + f"\n{p}")
    return 0 if out["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
