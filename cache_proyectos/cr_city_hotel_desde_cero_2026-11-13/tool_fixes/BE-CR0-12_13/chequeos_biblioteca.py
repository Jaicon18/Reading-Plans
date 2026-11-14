#!/usr/bin/env python3
"""chequeos_biblioteca.py — BE-121 / orden del usuario 3-nov ("142 todavía sin programa ... haz los programas").

Un chequeo de PROGRAMA por cada regla que estaba "programa-pendiente" en REGLAS_REGISTRO.json (127 BE-* de la biblioteca de
errores + U-017 / U-026 / U-034 / U-035 / U-037 / U-051 / U-057 / U-058 / U-079 / U-081 / U-082 / R-ALC-02 / R-ALC-04 /
R-ALC-10). Cada chequeo mira el FONDO (canon, Excel, texto del set incl. SHX, markups, lecturas A/B, archivos de la
corrida) con el criterio "PASS si…" de BIBLIOTECA_ERRORES.md y devuelve (PASS | FAIL | AMBER, evidencia):
  - PASS "N/A: …" cuando la condición del error no existe en el proyecto (p. ej. no hay ballistic);
  - AMBER cuando falta el dato para probarlo (p. ej. sin set_texto.json) — se reporta, no bloquea;
  - FAIL = el error original está presente: la entrega no sale (compuerta_entrega.py los corre todos).
Los chequeos NO cambian cantidades: solo leen.
Test: tools/test_chequeos_biblioteca.py (cada chequeo con el caso que REPRODUCE el error original -> FAIL y el arreglo -> PASS).

Uso directo:  python3 chequeos_biblioteca.py <project_workdir>     (lo mismo que hace compuerta_entrega.py)
"""
import csv
import glob
import json
import math
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
for _r in (os.path.join(AQUI, "..", "runner"), os.path.join(AQUI, "..", "take-off-metal-frame-drywall", "runner"),
           os.path.join(os.environ.get("TAKEOFF_SKILL") or AQUI, "runner")):
    if os.path.isdir(_r) and _r not in sys.path:
        sys.path.append(_r)

LISTAS_MUROS = ("walls", "existing_walls")             # toda lista de muros del esquema del canon (COORDINACIÓN 13-nov, BE-XF16)


def muros_canon(c):
    """BE-XF16: TODOS los muros del canon = walls + existing_walls (CR guarda sus ~943 muros board-only en existing_walls y deja
    walls = []; un chequeo que lee solo 'walls' pasa en vacío, U-137). Acepta el canon (dict) o un contexto con .canon."""
    can = getattr(c, "canon", c)
    can = can if isinstance(can, dict) else {}
    return [w for k in LISTAS_MUROS for w in (can.get(k) or []) if isinstance(w, dict)]


RX_HOJA_CITA = re.compile(r"\b([A-Z]{1,3}-?\d{1,3}(?:\.\d{1,2})?[A-Z]?)\b")
RX_DET = re.compile(r"(?<![\w.\-/])([A-Z0-9]{1,3}(?:\.[A-Z0-9]{1,2})?)\s*/\s*([A-Z]{1,3}-?\d{1,3}(?:\.(?:\d{1,2}|[A-Z](?![A-Za-z0-9])))?[A-Z]?)\b")   # R80f.35: 12/A503.C -> A503.C (no A503); R80f.36: '-15 / A6C', 'RFI-06 / RFI-30', '3.5.G / S100' no son N/HOJA
RX_KEYNOTE = re.compile(r"[A-Z]{1,2}\d\.\d{2}")    # R80f.36: keynote (A1.11, D0.07), nunca un número de detalle
RX_FTIN = re.compile(r"(\d{1,3})\s*'\s*-?\s*(\d{1,2})?(?:\s+(\d{1,2})/(\d{1,2}))?\s*\"?")
RX_ESTADO = re.compile(r"(?i)CONFIRM|DERIV|\bRFI\b|ASSUM|PENDING|PENDIENTE|SUPUEST|ESTIMATOR")
RX_WET = re.compile(r"(?i)rest ?room|toilet|\bR\.?R\.?\b|janitor|\bjan\.?\b|shower|lavator|\bmop\b|\bwet\b|\bwomen'?s\b|\bmen'?s\b|\bunisex\b")
RX_WR = re.compile(r"(?i)\bW\.?R\.?\b|water[- ]?resist|moisture[- ]?resist|\bMR\b|mold|abuse|cement|glass[- ]?mat|dens|tile backer|\bFRP\b")
RX_FASTENER = re.compile(r"(?i)\bscrews?\b|\banchors?\b|titen|tapcon|\bbolts?\b|slab pins?|\bP\.?A\.?F\.?\b|power[- ]driven|"
                         r"\bfasteners?\b|kwik|x-?edni|hus-?ez")
RX_SLIP = re.compile(r"(?i)slip|deflection|deep[- ]leg|slotted")
RX_INTERNO = re.compile(r"(?i)\.json\b|\.py\b|\.jsonl\b|takeoff_work|proceso_calc|/etapas/|etapas/\d|scratchpad|takeoff_canon|familias_out")
RX_PLAN_CHECK = re.compile(r"\bC7-0\d\b|\bC-0\d\b|\bN-0\d\b|(?i:(?<![a-z0-9])rev\d+[a-z]? plan check\b|\bplan check\b)")
RX_ESPANOL = re.compile(r"\b(?:DISCREPANCIA|PENDIENTE|DERIVADO|CONFIRMADO|SUPUESTO|cara(?:s)?|altura|hoja|muro|techo|"
                        r"tornillos|cantidad|falta|revisar)\b", re.I)


def R(estado, *ev):
    return estado, [str(x) for x in ev if x not in (None, "")]


NA = lambda motivo: R("PASS", "N/A: " + motivo)      # noqa: E731
SIN = lambda dato: R("AMBER", "sin " + dato + ": no se puede probar")      # noqa: E731


def ftin(m):
    """match de RX_FTIN -> pies."""
    f = float(m.group(1)) + float(m.group(2) or 0) / 12.0
    if m.group(3) and m.group(4) and float(m.group(4)):
        f += float(m.group(3)) / float(m.group(4)) / 12.0
    return f


def _n(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _norm(t):
    return " ".join(re.sub(r"[^A-Z0-9]+", " ", str(t or "").upper()).split())


# ============================================================================================== contexto

def _rev_carpeta(nombre):
    m = re.search(r"(?i)(?<![a-z0-9])rev[_-]?(\d{1,3}[a-z]?)(?![a-z0-9])", nombre or "")
    return m.group(1).lower() if m and re.match(r"(?i)(?:entrega|final_for_review)", nombre or "") else None


def texto_de_otra_rev(w, p, entrega=None):
    """v126 (COORDINACIÓN 12-nov 23:13, GK / CR): un .md bajo una carpeta entrega_rev<N> / FINAL_FOR_REVIEW_rev<N> que NO es la rev actual
    (la de `entrega`), o bajo un symlink que apunta a una entrega previa, no se audita (CB_FALTANTES / auditorías)."""
    actual = _rev_carpeta(os.path.basename(os.path.normpath(entrega))) if entrega else None
    real_act = os.path.realpath(entrega) if entrega else None
    rel = os.path.relpath(p, w).split(os.sep)
    cur = w
    for comp in rel[:-1]:
        cur = os.path.join(cur, comp)
        r = _rev_carpeta(comp)
        if r and actual and r != actual:                 # sin entrega actual conocida no se descarta por nombre
            return True
        if os.path.islink(cur):
            dest = os.path.realpath(cur)
            rd = _rev_carpeta(os.path.basename(dest))
            if rd and real_act and dest != real_act and not real_act.startswith(dest + os.sep):
                return True
    return False


def _rglob_seguro(raiz, pat):
    """BE-GK35 (post-mortem 11-nov): glob con '**' a prueba de ciclos de symlinks (takeoff_work -> work dir): glob.glob(recursive=True)
    sigue los symlinks de directorio y no termina. Recorre con os.walk(followlinks) sin entrar dos veces al mismo directorio real."""
    import fnmatch
    if "**" not in pat:
        return sorted(glob.glob(os.path.join(raiz, pat)))
    pre, post = pat.split("**", 1)
    post = post.lstrip("/")
    base = os.path.join(raiz, pre) if pre else raiz
    seen, out = set(), []
    for r, ds, fs in os.walk(base, followlinks=True):
        rp = os.path.realpath(r)
        if rp in seen:
            ds[:] = []
            continue
        seen.add(rp)
        ds[:] = sorted(d for d in ds if os.path.realpath(os.path.join(r, d)) not in seen and not d.startswith("."))
        for f in fs:
            rel = os.path.relpath(os.path.join(r, f), base)
            if fnmatch.fnmatch(rel, post) or fnmatch.fnmatch(rel, "*/" + post):
                out.append(os.path.join(r, f))
    return sorted(out)

class B:
    """Todo lo que miran los chequeos; se arma desde compuerta_entrega.Ctx (desde_ctx) o directo (tests)."""

    def __init__(self, **kw):
        self.canon = kw.get("canon") or {}
        self.canon_a = kw.get("canon_a")
        self.canon_b = kw.get("canon_b")
        self.canon_ab = kw.get("canon_ab")
        self.tk = kw.get("tk") or {}
        self.ms = kw.get("ms") or []            # [{fila, material, unit, net, waste, purchase, selling, pieces, fuente}]
        self.pt = kw.get("pt") or []            # [{fila, partition, wall, lf, h, layers, stud, oc, board, loc, source, status}]
        self.inputs = kw.get("inputs") or []    # [(fila, parametro, valor, nota)]
        self.pend = kw.get("pend") or []        # [(rfi, pregunta, delta, *extra)]
        self.review = kw.get("review") or []    # [tuplas]
        self.scope = kw.get("scope") or []      # [(id, scope, status, nota)]
        self.celdas = kw.get("celdas")          # [(hoja, coord, texto)] de las hojas visibles
        self.hojas = kw.get("hojas")            # set_texto: {hoja: texto} (incl. AutoCAD SHX)
        self.set_meta = kw.get("set_meta") or {}  # R80e.151: {"ocr": [hojas leídas por OCR], "en_blanco": [...]}
        self.docs = kw.get("docs") or {}        # {nombre: texto} README / PARA_REVISAR / SEGUIMIENTO
        self.annots = kw.get("annots")          # [{label, subject, contents, measure}] del PDF de markups
        self.pag_texto = kw.get("pag_texto") or {}  # {label: texto de la página del PDF de markups}
        self.textos = kw.get("textos") or {}    # {nombre: texto} de la corrida (resolucion.md, revision_extra.md, …)
        self.revision = kw.get("revision")      # revision.json de comparar.py
        self.costos = kw.get("costos")          # filas de costos.csv
        self.bitacora = kw.get("bitacora")      # [dict] de bitacora.jsonl
        self.inventario = kw.get("inventario")  # [{type, sheet}] de inventario_tags
        self.familias = kw.get("familias")      # familias_out.json {familia: net}
        self.sello = kw.get("sello")            # <excel>.sello.json
        self.bidset_annots = kw.get("bidset_annots")   # [{title, subject}] del bid set copiado a la sesión
        self.bidset_original_shx = kw.get("bidset_original_shx")   # n anotaciones SHX del original
        self.demo = kw.get("demo")              # demo_geom.json
        self.env = kw.get("env")                # entorno del claude -p del runner
        self.no_aplican = kw.get("no_aplican")
        self.cadena_md = kw.get("cadena_md")  # BE-CC07: text of burbujas/CADENA.md
        self.verificadas = kw.get("verificadas")  # U-137: burbujas_verificadas.json {hoja: [{x, y, n, hoja} | {x, y, no_es_burbuja}]}
        self.inv_full = kw.get("inv_full")      # inventario.json de inventario_tags.py (ocurrencias con png / png_verificado)
        self.inv_dir = kw.get("inv_dir")        # carpeta de ese inventario.json (recortes/)
        self.raiz = kw.get("raiz")              # carpeta de la corrida (para resolver imágenes)
        self.canon_dir = kw.get("canon_dir")  # callouts_no_aplican.json {hoja: {etiqueta: motivo}} o {"N/HOJA": motivo}
        self.fichas = kw.get("fichas")          # U-127: fichas.json de la lectura independiente del schedule (BE-122)
        self.mapa_materiales = kw.get("mapa_materiales") or {}   # entrega.json {clave del schedule: [types / Wall IDs]}
        self.esquinas = kw.get("esquinas")      # R80f.36: esquinas_out.json de esquinas.py {fallas, esquinas, huecos}
        self.specs = kw.get("specs")            # E3 CR City Hotel rev6: {sección: texto} del Project Manual (entrega.json specs_dir)
        if self.celdas is None:
            self.celdas = self._celdas_de_filas()

    # ------------------------------------------------------------------ armado desde una carpeta de proyecto
    @classmethod
    def desde_ctx(cls, c):
        if getattr(c, "_cb", None) is not None:
            return c._cb
        kw = {"canon": c.canon, "tk": c.tk, "raiz": c.w, "canon_dir": os.path.dirname(c.canon_p) if c.canon_p else None}
        w = c.w

        def ult(pats):
            for p in pats:
                xs = _rglob_seguro(w, p)                     # BE-GK35: sin glob recursivo (ciclos de symlinks)
                if xs:
                    return xs[-1]
            return None

        def js(p):
            try:
                return json.load(open(p, encoding="utf-8")) if p and os.path.isfile(p) else None
            except (OSError, ValueError):
                return None
        kw["canon_a"] = js(ult(["**/2_lectura/takeoff_canon_A.json", "**/takeoff_canon_A.json", "**/2_lectura/canon_A.json"]))   # v81cf25
        kw["canon_b"] = js(ult(["**/2_lectura/takeoff_canon_B.json", "**/takeoff_canon_B.json", "**/2_lectura/canon_B.json"]))
        kw["canon_ab"] = js(ult(["**/takeoff_canon_AB.json"])) or (c.canon if kw["canon_a"] else None)
        kw["revision"] = js(ult(["**/2_lectura/revision.json", "**/revision.json"]))
        kw["demo"] = js(ult(["**/4_canon/demo_geom.json", "**/demo_geom.json"]))
        kw["familias"] = js(ult(["**/familias_out.json"]))
        kw["esquinas"] = js(ult(["**/4_canon/out/esquinas_out.json", "**/esquinas_out.json"]))
        kw["mapa_materiales"] = c.cfg.get("mapa_materiales") or {}
        kw["fichas"] = js((c.cfg.get("fichas") and os.path.join(w, c.cfg["fichas"])) or ult(["fichas.json", "**/fichas.json"]))   # U-127
        inv = js(ult(["**/inventario_tags*.json", "**/1_inventario/tags.json"]))
        ip = ult(["**/1_inventario/inventario.json"])
        full = js(ip)
        if isinstance(full, dict) and isinstance(full.get("ocurrencias"), dict):
            kw["inv_full"], kw["inv_dir"] = full, os.path.dirname(ip)      # U-117 (conteo por ubicación, no por hoja)
        if isinstance(inv, dict):
            inv = inv.get("tags") or inv.get("items")
        kw["inventario"] = inv if isinstance(inv, list) else None
        textos = {}
        for pat in ("**/resolucion.md", "**/revision_extra.md", "**/revision.md", "**/demo_cruce.md", "**/DEMO_CRUCE*.md", "**/*cobertura*.md",   # v81cf25: DEMO_CRUCE.md (demo_cruce.py)
                    "**/*COBERTURA*.md", "**/PASO12*.md", "**/DOBLE_CIELO.csv", "**/AUDITORIA*.md", "**/INFORME*.md",
                    "**/revision_independiente/**/*.md", "**/auditoria_U138*/**/*.md", "**/Auditoria/**/*.md"):   # verificación 12b: TODO .md de Auditoria/   # v81cf119: hallazgos de la auditoría (BE-CR40)     # BE-AUD06: DOBLE_CIELO.csv para CB_RCP_APILADOS
            for p in _rglob_seguro(w, pat):                 # BE-GK35
                if texto_de_otra_rev(w, p, getattr(c, "entrega", None)):    # v126 (GK / CR): entregas previas no se auditan
                    continue
                try:
                    textos[os.path.relpath(p, w)] = open(p, encoding="utf-8", errors="ignore").read()
                except OSError:
                    pass
        kw["textos"] = textos
        cp = ult(["costos.csv", "**/costos.csv"])
        if cp:
            try:
                kw["costos"] = list(csv.DictReader(open(cp, encoding="utf-8")))
            except (OSError, csv.Error):
                kw["costos"] = None
        bp = ult(["**/bitacora.jsonl"])
        if bp:
            kw["bitacora"] = []
            for l in open(bp, encoding="utf-8", errors="ignore"):
                try:
                    kw["bitacora"].append(json.loads(l))
                except ValueError:
                    pass
        st = js(c.set_p)
        kw["hojas"] = st.get("hojas") if isinstance(st, dict) else None
        sd = c.cfg.get("specs_dir")
        sd = sd if not sd or os.path.isabs(sd) else os.path.join(w, sd)
        sp = sorted(glob.glob(os.path.join(sd, "*.txt"))) if sd else _rglob_seguro(w, "**/specs/*.txt")
        kw["specs"] = {os.path.basename(p)[:-4]: open(p, encoding="utf-8", errors="ignore").read() for p in sp} or None
        kw["set_meta"] = {k: st.get(k) for k in ("ocr", "en_blanco", "sin_texto", "burbujas", "fuentes")} if isinstance(st, dict) else {}
        kw["verificadas"] = js((c.cfg.get("burbujas_verificadas") and os.path.join(w, c.cfg["burbujas_verificadas"]))
                               or ult(["burbujas_verificadas.json", "**/burbujas_verificadas.json"]))
        kw["docs"] = {os.path.basename(p): open(p, encoding="utf-8", errors="ignore").read()
                      for p in (c.readme, c.para, c.seg) if p and os.path.isfile(p)}
        if c.excel:
            kw["sello"] = js(c.excel + ".sello.json")
        wb = c.wb()
        if wb is not None:
            kw.update(cls._leer_excel(wb))
        if c.markups and os.path.isfile(c.markups):
            kw["annots"], kw["pag_texto"] = cls._leer_markups(c.markups)
        bs = (c.cfg.get("bidset") and os.path.join(w, c.cfg["bidset"])) or ult(["**/copia_limpia*.pdf", "bidset/*.pdf", "planos/*.pdf"])
        if bs and os.path.isfile(bs):
            kw["bidset_annots"] = cls._annots_pdf(bs)
        kw["env"] = None
        cm = ult(["burbujas/CADENA.md", "**/CADENA.md"])     # BE-CC07: the eye-read reference chain of the project
        kw["cadena_md"] = open(cm, encoding="utf-8", errors="ignore").read() if cm and os.path.isfile(cm) else None
        kw["no_aplican"] = js((c.cfg.get("callouts_no_aplican") and os.path.join(w, c.cfg["callouts_no_aplican"]))
                              or ult(["callouts_no_aplican.json", "**/callouts_no_aplican.json"]))
        b = cls(**kw)
        c._cb = b
        return b

    @staticmethod
    def _leer_excel(wb):
        out = {"ms": [], "pt": [], "inputs": [], "pend": [], "review": [], "scope": [], "celdas": []}
        for ws in wb.worksheets:
            if ws.sheet_state != "visible":
                continue
            for row in ws.iter_rows():
                for cell in row:
                    if isinstance(cell.value, str) and cell.value.strip():
                        out["celdas"].append((ws.title, cell.coordinate, cell.value))
        g = lambda h: wb[h] if h in wb.sheetnames else None      # noqa: E731
        ws = g("Material Summary")
        if ws is not None:
            for i, r in enumerate(ws.iter_rows(min_row=4, values_only=True), start=4):
                r = list(r) + [None] * 11
                if not r[0] or str(r[0]).upper().startswith(("SUBTOTAL", "TOTAL", "GRAND")):
                    continue
                out["ms"].append({"fila": i, "material": str(r[0]), "unit": str(r[1] or ""), "net": _n(r[2]),
                                  "waste": str(r[3] or ""), "purchase": r[5], "selling": str(r[6] or ""),
                                  "pieces": r[7], "fuente": str(r[8] or "")})
        ws = g("Partition Takeoff")
        if ws is not None:
            for i, r in enumerate(ws.iter_rows(min_row=5, values_only=True), start=5):
                r = list(r) + [None] * 11
                if not any(r[:11]):
                    continue
                out["pt"].append({"fila": i, "partition": r[0], "wall": r[1], "lf": _n(r[2]), "h": _n(r[3]),
                                  "layers": r[4], "stud": r[5], "oc": r[6], "board": _n(r[7]), "loc": r[8],
                                  "source": r[9], "status": r[10]})
        ws = g("Inputs")
        if ws is not None:
            for i, r in enumerate(ws.iter_rows(min_row=5, values_only=True), start=5):
                r = list(r) + [None] * 3
                if r[0]:
                    out["inputs"].append((i, str(r[0]), r[1], str(r[2] or "")))
        for h, k, f0 in (("Pending Items", "pend", 2), ("Review Items", "review", 3), ("Scope Checklist", "scope", 2)):
            ws = g(h)
            if ws is not None:
                out[k] = [tuple("" if x is None else x for x in r) for r in ws.iter_rows(min_row=f0, values_only=True)
                          if r and any(x is not None for x in r)]
        return out

    @staticmethod
    def _leer_markups(pdf):
        import pymupdf
        an, txt = [], {}
        doc = pymupdf.open(pdf)
        for p in doc:
            lab = p.get_label() or f"p{p.number + 1}"
            txt[lab] = p.get_text("text")
            for a in p.annots() or []:
                inf = a.info or {}
                t, v = doc.xref_get_key(a.xref, "Measure")
                td, dv = doc.xref_get_key(a.xref, "Depth")
                an.append({"label": lab, "subject": inf.get("subject") or "", "contents": inf.get("content") or "",
                           "title": inf.get("title") or "", "measure": t not in ("null", None) and bool(v),
                           "tipo": a.type[1], "nm": inf.get("id") or "", "depth": _n(dv) if td not in ("null", None) else None,
                           "verts": [tuple(x) for x in (a.vertices or []) if isinstance(x, (tuple, list)) and len(x) == 2]})
        return an, txt

    @staticmethod
    def _annots_pdf(pdf):
        import pymupdf
        out = []
        for p in pymupdf.open(pdf):
            for a in p.annots() or []:
                inf = a.info or {}
                out.append({"title": inf.get("title") or "", "subject": inf.get("subject") or ""})
        return out

    def _celdas_de_filas(self):
        out = []
        for f in self.ms:
            out += [("Material Summary", f"A{f.get('fila', 0)}", f.get("material", "")),
                    ("Material Summary", f"I{f.get('fila', 0)}", f.get("fuente", ""))]
        for f in self.pt:
            out += [("Partition Takeoff", f"A{f.get('fila', 0)}", str(f.get("partition") or "")),
                    ("Partition Takeoff", f"J{f.get('fila', 0)}", str(f.get("source") or ""))]
        for h, rows in (("Pending Items", self.pend), ("Review Items", self.review), ("Scope Checklist", self.scope)):
            for i, r in enumerate(rows):
                out += [(h, f"{chr(65 + j)}{i + 2}", str(x)) for j, x in enumerate(r) if str(x).strip()]
        for i, p, v, n in self.inputs:
            out += [("Inputs", f"A{i}", p), ("Inputs", f"C{i}", n)]
        return out

    # ------------------------------------------------------------------ accesos
    def walls(self, c=None):
        cc = c if c is not None else self.canon
        ws = [w for w in (cc.get("walls") or []) if isinstance(w, dict)]   # solo-metal: board-only entra por el respaldo de abajo (BE-CR10)
        if ws or c is not None:
            return ws
        return self._walls_board_only()

    def _walls_board_only(self):
        """BE-CR25 (CR City Hotel rev1, COORDINACIÓN 6-nov: la compuerta pasó EN VACÍO con walls = 0 y 755 board-only en
        existing_walls): en un set wood-framed (framing EXCLUDED, R80f.1 / U-139) cada wall físico de existing_walls se presenta
        a los chequeos como un wall con sus caras (side, board, layers, height_ft, source), así BOTH SIDES, alturas por cara,
        U-114, BE-05 / 08 / 68 / 78 / 83 / 103 y los demás corren de verdad. existing walls 'to remain' (sin wood_excluded) no."""
        if getattr(self, "_wbo", None) is not None:
            return self._wbo
        ex = [e for e in (self.canon.get("existing_walls") or []) if isinstance(e, dict)]
        if not ex or not (self.canon.get("wood_excluded") or any(re.search(r"(?i)wood fram", str(e.get("decision") or "")) for e in ex)):
            self._wbo = []
            return self._wbo
        grupos = {}
        for e in ex:
            base = re.sub(r" [A-Z]$", "", str(e.get("id")))
            grupos.setdefault((base, e.get("sheet")), []).append(e)
        out = []
        for (base, sh), es in grupos.items():
            e0 = es[0]
            caras, k, por_cuarto = [], 0, {}
            for e in sorted(es, key=lambda x: "cement" in str(x.get("board") or "").lower()):   # overlays de cement board al final
                loc = str(e.get("location") or "")
                partes = [x.strip() for x in loc.split("faces:")[-1].split(";")] if "faces:" in loc else []
                for i in range(int(e.get("faces") or 1)):
                    cuarto = partes[i] if i < len(partes) else ""
                    ck = re.sub(r"\W+", " ", cuarto.lower()).strip()
                    # BE-CR25: dos entradas sobre la MISMA cara (p. ej. cement board + Type X W.R. detrás del tile) = una cara
                    # con las capas sumadas, no dos caras de una capa
                    # BE-CR25 / RFI-11: el cement board del shower es un overlay sobre una cara (tile backer), nunca una cara propia
                    if "cement" in str(e.get("board") or "").lower():
                        f = por_cuarto.get(ck)
                        if f:
                            f["layers"] += int(e.get("layers") or 1); f["boards"].append(e.get("board")); f["entry"] += " + " + str(e.get("id"))
                            continue
                        # sin cara del mismo cuarto: el cement board ES la cara (non-rated, RFI-11 'cement board in place of board')
                    if ck and ck in por_cuarto and por_cuarto[ck]["entry"].split(" + ")[-1] != str(e.get("id")):
                        f = por_cuarto[ck]
                        f["layers"] += int(e.get("layers") or 1)
                        f["boards"].append(e.get("board"))
                        f["entry"] += " + " + str(e.get("id"))
                        continue
                    lado = "AB"[k] if k < 2 else chr(65 + k)
                    k += 1
                    f = {"side": lado, "board": e.get("board"), "boards": [e.get("board")], "layers": int(e.get("layers") or 1),
                         "length_ft": e.get("length_ft"),     # BE-CR0-12: cada cara con SU largo (no el de la primera entrada del grupo)
                         "height_ft": e.get("height_ft"), "height_status": e.get("height_status"), "room": cuarto, "img": e.get("img"),
                         "height_img": e.get("height_img") or e.get("img"),
                         "source": e.get("source"), "height_source": e.get("height_source"), "entry": e.get("id")}
                    caras.append(f)
                    if ck:
                        por_cuarto[ck] = f
            w = {"id": base, "element": "wall", "tag": e0.get("type_id"), "type": e0.get("type"), "type_id": e0.get("type_id"),
                 "floor": e0.get("floor"), "sheet": sh, "page": e0.get("page"), "path": e0.get("path"),
                 "length_ft": e0.get("length_ft"), "length_status": e0.get("length_status"),
                 "length_source": re.split(r"\s*\|\s*height\s*:", str(e0.get("source") or ""))[0],   # BE-CR25: la cota de altura no es largo
                 "height_ft": max(float(x.get("height_ft") or 0) for x in es), "height_status": e0.get("height_status"),
                 "height_source": e0.get("height_source"), "source": e0.get("source"), "faces": caras,
                 "framing": "wood (Div. 06, EXCLUDED)", "board_only": True, "tag_ids": sorted({t for x in es for t in (x.get("tag_ids") or [])}),
                 "location": e0.get("location"), "keynote": e0.get("keynote"), "img": e0.get("img"), "height_img": e0.get("height_img"),
                 "faces_none_reason": " ".join(str(x.get("faces_none_reason") or "") for x in es).strip()}
            (x0, y0), (x1, y1) = (e0.get("path") or [[0, 0], [0, 0]])[0], (e0.get("path") or [[0, 0], [0, 0]])[-1]
            if abs(y1 - y0) <= 1.5:
                w["band"] = {"ori": "H", "lo": min(x0, x1), "hi": max(x0, x1), "c0": y0 - 2.5, "c1": y0 + 2.5, "sheet": sh}
            elif abs(x1 - x0) <= 1.5:
                w["band"] = {"ori": "V", "lo": min(y0, y1), "hi": max(y0, y1), "c0": x0 - 2.5, "c1": x0 + 2.5, "sheet": sh}
            else:
                w["band"] = {"ori": "D", "p0": [x0, y0], "p1": [x1, y1], "sheet": sh}
            out.append(w)
        self._wbo = out
        return out

    def schedule(self):
        """BE-CR29: el Partition Type Schedule del canon (partition_schedule) o, si el canon no lo trae, el de la lectura independiente
        (fichas.json, BE-122): un chequeo de schedule nunca da N/A 'sin partition_schedule' con el schedule leído."""
        ps = [p for p in self.canon.get("partition_schedule") or [] if isinstance(p, dict)]
        if ps:
            return ps
        fj = self.fichas if isinstance(self.fichas, dict) else {}
        return [{"type": k, "source": f"fichas.json ({(v or {}).get('sheet') or 'schedule'})" if isinstance(v, dict) else "fichas.json"}
                for k, v in (fj.get("types") or {}).items()]

    def walls_todos(self, c=None):
        """BE-CR10: walls + existing_walls (proyecto wood-framed: todo board-only vive en existing_walls)."""
        c = c if c is not None else self.canon
        return muros_canon(c)

    def faces(self, c=None):
        return [(w, f) for w in self.walls(c) for f in (w.get("faces") or []) if isinstance(f, dict)]

    def ceilings(self):
        return [z for z in self.canon.get("ceilings") or [] if isinstance(z, dict)]

    def excel_txt(self, hojas=None):
        return "\n".join(t for h, _, t in self.celdas if hojas is None or h in hojas)

    def set_txt(self, pref=None):
        if not self.hojas:
            return ""
        return "\n".join(t for h, t in self.hojas.items() if pref is None or re.match(pref, h))

    def rfis_abiertos(self):
        out = []
        for r in self.pend:
            if r and re.match(r"(?i)\s*[A-Z\-]*RFI", str(r[0])) and not re.search(r"\bCLOSED\b", " ".join(map(str, r[1:]))[:300]):
                out.append(r)
        return out

    def rfi_canon(self, rid):
        for r in list(self.tk.get("rfis") or []) + list(self.canon.get("rfis") or []):
            if isinstance(r, dict) and str(r.get("id")) == str(rid):
                return r
        return {}

    def ms_txt(self, f):
        return f"{f.get('material', '')} {f.get('fuente', '')}"


def _tiene_fila(b, rx, net=True):
    return [f for f in b.ms if rx.search(f["material"]) and (not net or (f["net"] or 0) > 0)]


def _destino(b, rx):
    """el ítem tiene destino en el Excel: renglón, EXCLUDED / NOT APPLICABLE con motivo o RFI que lo nombra."""
    if [f for f in b.ms if rx.search(b.ms_txt(f))]:
        return True
    return bool(rx.search(b.excel_txt(("Scope Checklist", "Pending Items", "Review Items"))))


def _hojas_con(b, rx, pref=None):
    return sorted(h for h, t in (b.hojas or {}).items() if (pref is None or re.match(pref, h)) and rx.search(t))


# ============================================================================================== registro de chequeos
CHEQUEOS = []          # (id_regla, fn, desc)


def chk(*ids, desc=""):
    def deco(fn):
        CHEQUEOS.append((list(ids), fn, desc or (fn.__doc__ or "").strip().split("\n")[0]))
        return fn
    return deco


# ---------------------------------------------------------------------------------------------- U / R-ALC
def _cota_impresa(src):
    """Cota IMPRESA citada en una fuente de largo: "printed '12'-4\"'" / "'12'-4\"' [CONFIRMED]" -> pies o None."""
    s = str(src or "")
    m = re.search(r"(?i)printed\s*(?:dim(?:ension)?\s*)?['\"“]?\s*±?\s*" + RX_FTIN.pattern, s)
    if not m:   # CC-R4d (Consumer Cellular rev3 audit): "A100 dim 7'-3\" (ticks ...)" = printed dimension (before N/A in vacuum)
        m = re.search(r"(?i)\bdim(?:ension)?\.?\s+['\"“]?\s*" + RX_FTIN.pattern, s)
    if not m:
        m = re.search(r"['\"“]\s*±?\s*" + RX_FTIN.pattern + r"[^\[]{0,30}\[(?:CONFIRMED|CONFIRMADO)\]", s)
    if not m:
        return None
    g = m.groups()[-4:]
    f = float(g[0]) + float(g[1] or 0) / 12.0
    if g[2] and g[3] and float(g[3]):
        f += float(g[2]) / float(g[3]) / 12.0
    return f


RX_JUSTIFICA = re.compile(r"(?i)estimator|R-ALC-\d|R80e\.\d|RFI-\d|net of|minus|less |deduct|- \d|\bto face\b|face to|"
                          r"overall|centerline|c\.?l\.?|portion|segment|part of|tramo|split|"
                          r"\d\"\s*\+\s*\d")      # BE-CR25: suma de cotas impresas (5'-9" + 7 5/8" + 7 5/8" = 7.02) = operación derivada


@chk("U-017", desc="U-017: una cota IMPRESA que coincide con una lectura manda: la resolución AB nunca toma la otra lectura")
def u_017(b):
    """U-017: resolución A/B que contradice la cota impresa (CONFIRMADO > DERIVADO)."""
    if not (b.canon_a and b.canon_b):
        return NA("sin lecturas A y B en la carpeta (proyecto sin resolución A/B guardada)")
    ab = b.canon_ab or b.canon
    ia = {w.get("id"): w for w in b.walls(b.canon_a)}
    ib = {w.get("id"): w for w in b.walls(b.canon_b)}
    ev = []
    for w in b.walls(ab):
        a, bb = ia.get(w.get("id")), ib.get(w.get("id"))
        if not (a and bb):
            continue
        for lado, x, y in (("A", a, bb), ("B", bb, a)):
            imp = _cota_impresa(x.get("length_source"))
            lx, ly, lw = _n(x.get("length_ft")), _n(y.get("length_ft")), _n(w.get("length_ft"))
            if imp is None or None in (lx, ly, lw) or min(lx, ly) <= 0 or min(lx, ly) / max(lx, ly) < 0.5:
                continue                      # ids iguales pero elementos distintos (otra partición de tramos)
            if abs(lx - imp) <= 1 / 12 and abs(ly - imp) > 1 / 12 and abs(lw - ly) <= 0.01 and abs(lw - imp) > 1 / 12:
                # BE-GK26 (Grand Kia): the written A/B resolution says the reader's same-ID wall is ANOTHER canon wall
                # ("reader B's 'A1-Z1-05' ... is the canon wall A1-Z1-06"): different elements, not a resolution against the print
                res_txt = " ".join(v for k, v in (b.textos or {}).items() if "resoluc" in k.lower())
                if re.search(r"(?i)reader " + lado + r"'s '" + re.escape(str(w.get("id"))) + r"'[^|\n]{0,160}is the canon wall [A-Z]", res_txt):
                    continue
                ev.append(f"{w.get('id')}: lectura {lado} = cota impresa {imp:.2f} ft; la resolución tomó la otra ({lw:.2f})")
    return R("FAIL", *ev) if ev else R("PASS", "ninguna resolución contra una cota impresa")


@chk("BE-08", desc="BE-08: todo LF con cota impresa coincide (± 1\") o la diferencia está explicada / es decisión citada")
def be_08(b):
    """BE-08: LF contra la cota impresa que cita su propia fuente."""
    ev, n = [], 0
    for w in b.walls():
        imp = _cota_impresa(w.get("length_source"))
        lf = _n(w.get("length_ft"))
        if imp is None or lf is None:
            continue
        n += 1
        if abs(lf - imp) > 1 / 12 + 1e-6 and not RX_JUSTIFICA.search(str(w.get("length_source"))):
            ev.append(f"{w.get('id')}: length_ft {lf:.2f} != cota impresa {imp:.2f} ft citada en su fuente")
    if not n:
        return NA("ningún wall cita una cota impresa en length_source") if b.walls() else SIN("canon")
    return R("FAIL", *ev) if ev else R("PASS", f"{n} walls con cota impresa = LF")


PRECEDENTES = [   # R80e.34 (B&N, 18 decisiones + 19) y R80e.78 (O'Reilly, BE-108): tema -> precedente que lo decide
    (r"spacing[^.]{0,60}(fastener|pin|screw|anchor)|(fastener|pin|screw|anchor)[^.]{0,60}spacing", "R80e.34 #1 / #17"),
    (r"\bducts?\b", "R80e.34 #2 / R-ALC-03"),
    (r"slop(e|ed|ing)[^.]{0,60}deck|deck[^.]{0,60}slop|V\.I\.F\.?[^.]{0,40}(deck|height)", "R80e.34 #3"),
    (r"header[^.]{0,60}(schedule|not (shown|scheduled))", "R80e.34 #4"),
    (r"\bFRP\b[^.]{0,60}(scope|by others|who)|PVC trim", "R80e.34 #5 / #19"),
    (r"\bfascia\b|GWB edges?", "R80e.34 #6"),
    (r"where shelving occurs|shelving", "R80e.34 #7"),
    (r"control joints?", "R80e.34 #8"),
    (r"moment clips?|partial(?:[- ]height)? walls?[^.]{0,40}anchor", "R80e.34 #9"),
    (r"corner guards?", "R80e.34 #10"),
    (r"by (?:the )?G\.?C\.?\b|by fixture installer|GC shall install", "R80e.34 #11"),
    (r"fire ?stop[^.]{0,40}(track|ceiling)|nested runner", "R80e.34 #12"),
    (r"seismic brac", "R80e.34 #13"),
    (r"cement board|backer board", "R80e.34 #15"),
    (r"orphan|not referenced|no (?:detail )?bubble", "R80e.34 #16"),
    (r"\bwaste\b", "R80e.34 #18"),
    (r"J[- ]?mold|division bars?", "R80e.34 #19"),
    (r"resilient channel|\bR\.?C\.? channel|\bRC\b", "R80e.78 (O'Reilly RFI: RC)"),
    (r"corner bead[^.]{0,40}header|header[^.]{0,40}corner bead", "R80e.78 (O'Reilly: corner bead del header)"),
    (r"\bstraps?\b", "R80e.78 (O'Reilly: strap)"),
    (r"\brunners?\b", "R80e.78 (O'Reilly: runner)"),
]


@chk("U-026", "BE-108", desc="U-026 / BE-108: ningún RFI abierto sobre un tema que un precedente del estimador (R80e.34 / "
     "R80e.78) ya decidió, salvo que lo cite")
def u_026(b):
    """U-026 / BE-108: RFI abierto con precedente decidido."""
    ev = []
    for r in b.rfis_abiertos():
        tema = str(r[1]) if len(r) > 1 else ""
        todo = " ".join(map(str, r))
        for rx, prec in PRECEDENTES:
            if re.search(rx, tema, re.I) and not re.search(r"R80e\.(34|78)|precedent", todo, re.I):
                ev.append(f"{r[0]}: el tema '{re.search(rx, tema, re.I).group(0)}' ya lo decidió {prec}: se carga como "
                          f"precedente (U-026) en vez de preguntar")
                break
    return R("FAIL", *ev) if ev else R("PASS", f"{len(b.rfis_abiertos())} RFI abiertos sin precedente decidido")


RX_ITEM_ID = re.compile(r"\b[A-Z][A-Z0-9]*-[A-Z0-9][A-Z0-9-]*\b")
RX_VAL_LF = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)\s*(?:LF|SF)\b")


@chk("CC-R1", desc="CC-R1 (Consumer Cellular rev3 audit): un renglón del Material Summary cuyo desglose lista valores SIN el ID "
     "de su ítem y esos valores son los ítems de otros renglones = renglón duplicado = FAIL")
def cc_r1(b):
    vals = {}
    for m in b.ms:
        f = str(m.get("fuente") or "")
        vals[m["fila"]] = (RX_ITEM_ID.findall(f), [float(x) for x in RX_VAL_LF.findall(f)])
    ev = []
    for m in b.ms:
        ids, vs = vals[m["fila"]]
        if (m.get("net") or 0) <= 0 or len(vs) < 3 or ids:
            continue
        otros = [v for k, (i_, v_) in vals.items() if k != m["fila"] and i_ for v in v_]
        if all(any(abs(v - o) < 0.005 for o in otros) for v in vs):
            ev.append(f"fila {m['fila']} '{m['material'][:60]}': {len(vs)} valores sin ID, todos son ítems de otros renglones")
    return R("FAIL", *ev) if ev else R("PASS", f"{len(b.ms)} renglones sin desglose duplicado")


@chk("CC-R5", desc="CC-R5 (Consumer Cellular rev3 audit): un renglón con 0 < net < 0.5 sin ítem que lo justifique compra piezas "
     "por redondeo = FAIL")
def cc_r5(b):
    ev = [f"fila {m['fila']} '{m['material'][:60]}': net {m['net']} (residuo de redondeo que compra piezas)" for m in b.ms
          if m.get("net") is not None and 0 < m["net"] < 0.5 and str(m.get("unit")).upper() in ("LF", "SF")
          and not RX_ITEM_ID.search(str(m.get("fuente") or ""))]
    return R("FAIL", *ev) if ev else R("PASS", "ningún renglón de residuo de redondeo")


@chk("CC-R7", desc="CC-R7 (Consumer Cellular rev3 audit): el Scope Checklist dice EXCLUDED de un material (sigla FRP / PVC / ACT ...) "
     "que el Material Summary carga con cantidad > 0 = FAIL")
def cc_r7(b):
    cargados = {}
    for m in b.ms:
        t = re.match(r"\s*([A-Z]{3,})\b", m["material"])
        if t and (m.get("net") or 0) > 0:
            cargados[t.group(1)] = m["material"]
    ev = []
    for r in b.scope:
        txt = " ".join(str(x or "") for x in r)
        if not re.search(r"\bEXCLUDED\b", txt):
            continue
        for k, mat in cargados.items():
            if re.search(r"EXCLUDED\W{1,4}(?:[^.;]{0,30})\b" + k + r"\b", txt) or re.search(r"\b" + k + r"\b[^.;]{0,60}\bEXCLUDED\b", txt):
                ev.append(f"{r[0]}: EXCLUDED sobre '{k}' y el Material Summary carga '{mat[:50]}'")
    return R("FAIL", *ev) if ev else R("PASS", "ningún EXCLUDED sobre un material cargado")


@chk("CC-R12", desc="CC-R12 / U-114 (Consumer Cellular rev3 audit): un wall cuyo largo es la cota impresa (length_status CONFIRMADO) "
     "va [CONFIRMED] en la Partition Takeoff, no [DERIVED]")
def cc_r12(b):
    # BE-CR25: la fila lleva el estado más débil de sus números: largo Y altura impresos -> [CONFIRMED]; una entrada board-only
    # cuenta por su id de cara (W.6-L1-03 A)
    conf = {w.get("id") for w in b.walls_todos() if str(w.get("length_status") or "").upper() == "CONFIRMADO"
            and str(w.get("height_status") or "CONFIRMADO").upper() == "CONFIRMADO"}
    ev = [f"{r['wall']}: largo = cota impresa (CONFIRMADO en el canon) y la Partition Takeoff dice {r['status']}" for r in b.pt
          if r.get("wall") in conf and "DERIVED" in str(r.get("status") or "")]
    if not ev and not conf:   # BE-XF06 (Xfinity 10-nov): ningún wall con largo Y altura impresos -> se declara con los walls de largo impreso
        lc = [w.get("id") for w in b.walls_todos() if str(w.get("length_status") or "").upper() == "CONFIRMADO"]
        return R("PASS", f"N/A: ningún wall con largo Y altura impresos a la vez; largo impreso con altura derivada: {', '.join(map(str, lc)) or 'ninguno'}")
    return R("FAIL", *ev) if ev else R("PASS", f"{len(conf)} walls con cota impresa en [CONFIRMED]")


RX_U146 = re.compile(r"(?i)deck break|deck heights?.{0,40}not (?:drawn|printed)|corte de deck|two (?:printed )?deck heights")
RX_U147 = re.compile(r"(?i)(?:finish|finishing) level|level of finish|nivel de acabado|\blevel [45]\b.{0,60}not (?:specified|printed)")


@chk("U-146", desc="U-146 (usuario 5-nov): deck con dos alturas impresas y el corte no dibujado = se carga la altura MAYOR impresa, "
     "sin RFI (criterios.deck_sin_corte); un RFI abierto sobre ese tema = FAIL")
def u_146(b):
    ev = [f"{r[0]}: corte de deck no dibujado = altura MAYOR impresa (U-146, criterios.deck_sin_corte), sin RFI"
          for r in b.rfis_abiertos() if RX_U146.search(" ".join(map(str, r[1:3])))]
    return R("FAIL", *ev) if ev else R("PASS", "ningún RFI abierto sobre el corte de deck (U-146)")


@chk("U-147", desc="U-147 (usuario 5-nov): level of finish no especificado = Level 4, sin RFI (criterios.level_of_finish); "
     "un RFI abierto sobre ese tema = FAIL")
def u_147(b):
    ev = [f"{r[0]}: level of finish no especificado = Level 4 (U-147, criterios.level_of_finish), sin RFI"
          for r in b.rfis_abiertos() if RX_U147.search(" ".join(map(str, r[1:3])))]
    return R("FAIL", *ev) if ev else R("PASS", "ningún RFI abierto sobre el level of finish (U-147)")


def _plan_sheets(*cs):
    out = set()
    for c in cs:
        for w in muros_canon(c or {}):
            if isinstance(w, dict) and w.get("sheet"):
                out.add(w["sheet"])
    return sorted(out)


def _hoja_leida_vacia(b, c, h):
    """R80f.39: una hoja que la lectura declara leída (sheets / sheets_read de sus fragmentos) sin walls propios está completa
    si cada tag del inventario de esa hoja quedó dispuesto en ella (tag_ids o tags_descartados con motivo); la diferencia con
    la otra lectura (un wall que solo la otra trae) es una discrepancia A/B para la resolución, no una hoja sin leer."""
    sh = c.get("sheets_read") or c.get("sheets") or []
    sh = [x for v in sh.values() for x in (v if isinstance(v, list) else [v])] if isinstance(sh, dict) else list(sh)
    if h not in sh:
        return False
    occ = [o for o in _inv_ocurrencias(b) if o.get("sheet") == h]
    disp = {str(d.get("id")) for d in c.get("tags_descartados") or [] if isinstance(d, dict) and len(str(d.get("motivo") or "")) >= 8}
    disp |= {str(t) for w in muros_canon(c) for t in w.get("tag_ids") or []}
    return all(str(o.get("id")) in disp for o in occ)


def _misma_cosa(x, c, o):
    """R80f.39: lo que la otra lectura trae y esta 'no' es el mismo elemento con otra etiqueta: un column_wrap / pier / chase
    de la otra cuyo tag de schedule esta lectura tiene como wall en la misma hoja (B leyó el C3C box como wall C3C), o una
    pseudo-etiqueta de keynote ('A2.25-INFILL') cuyo keynote nombra un wall de esta lectura en la misma hoja."""
    ws, wo = muros_canon(c or {}), muros_canon(o or {})
    if x in ("column_wrap", "pier", "chase"):
        els = [w for w in wo if w.get("element") == x]
        return bool(els) and all(any(str(v.get("tag") or "").upper() == str(e.get("tag") or "").upper() and
                                     v.get("sheet") == e.get("sheet") for v in ws) for e in els)
    els = [w for w in wo if str(w.get("tag") or "").upper() == str(x).upper() and w.get("element", "wall") == "wall"]
    if els and all(any(str(v.get("tag") or "").upper() == str(x).upper() and v.get("sheet") == e.get("sheet") for v in ws)
                   for e in els):
        return True                       # la otra lo lee como wall; esta lo tiene con el mismo tag como column_wrap / pier
    m = re.match(r"^([A-Z]\d\.\d{1,3})\b", str(x))
    if m:
        els = [w for w in wo if str(w.get("tag") or "").upper() == str(x).upper()]
        return bool(els) and all(any(v.get("sheet") == e.get("sheet") and re.search(r"(?<![\w.])" + re.escape(m.group(1)) + r"(?![\d])",
                                                                                  json.dumps(v)) for v in ws) for e in els)
    return False


@chk("U-034", "BE-59", desc="U-034 / BE-59: compuerta de completitud (runner/completitud.revisar) en A y en B: todas las hojas "
     "de planta y types del schedule presentes, y nada que la otra lectura trae falta")
def u_034(b):
    """U-034 / BE-59: completitud de cada lectura."""
    if not (b.canon_a and b.canon_b):
        return NA("sin lecturas A / B guardadas en la carpeta")
    import completitud
    hojas = _plan_sheets(b.canon_a, b.canon_b)
    ev = []
    for lado, c, o in (("A", b.canon_a, b.canon_b), ("B", b.canon_b, b.canon_a)):
        r = completitud.revisar(c, hojas, o)
        r["faltan_vs_otra"] = [x for x in r["faltan_vs_otra"] if not _misma_cosa(x, c, o)]   # R80f.39
        r["faltan_hojas"] = [h for h in r["faltan_hojas"] if not _hoja_leida_vacia(b, c, h)]       # R80f.39
        r["ok"] = not (r["faltan_hojas"] or r["faltan_types"] or r["faltan_vs_otra"])
        if not r["ok"]:
            ev.append(f"lectura {lado} incompleta: hojas sin walls {r['faltan_hojas']}, types sin walls {r['faltan_types']}, "
                      f"falta vs la otra {r['faltan_vs_otra']} ({r['walls']} walls / {r['lf']} LF)")   # campo: conteo del resultado
    return R("FAIL", *ev) if ev else R("PASS", f"A y B completas sobre {hojas}")


@chk("U-035", "BE-65", desc="U-035: escala (plan_scale_pt_per_ft), band.sheet y barrido MEP con hojas M / P en el canon: la evidencia "
     "la generan los programas desde coordenadas")
def u_035(b):
    """U-035: datos que los programas necesitan para generar la evidencia."""
    if not b.walls():
        return SIN("canon")
    ev = []
    k = b.canon.get("constants") or {}
    if not (k.get("plan_scale_pt_per_ft") or k.get("plan_scale_by_sheet")):
        ev.append("constants.plan_scale_pt_per_ft ausente: sin escala no hay recorte ni cruce band vs LF")
    sin = [w.get("id") for w in b.walls() if isinstance(w.get("band"), dict) and not w["band"].get("sheet") and not w.get("sheet")]
    if sin:
        ev.append(f"band sin sheet: {sin[:8]}")
    mp = [h for h in (b.hojas or {}) if re.match(r"^(M|P|MP|FP)-?\d", h)]
    ms = b.canon.get("mep_sweep")
    if mp and not ms and not b.canon.get("mep_sweep_excluded_info") and not b.canon.get("mep_penetrations_none_reason"):
        ev.append(f"el set tiene hojas M/P ({', '.join(mp[:4])}) y el canon no trae mep_sweep")
    return R("FAIL", *ev) if ev else R("PASS", "escala + band.sheet + barrido MEP presentes")


def _tipo_de(w):
    el = str(w.get("element") or "wall")
    return str(w.get("tag") or w.get("type") or "").upper() if el == "wall" else el   # BE-CR10: board-only usa 'type'


@chk("U-037", "BE-72", desc="U-037 / BE-72: conteos por type y hoja contra el inventario de tags (y columnas): ningún tag del "
     "inventario sin wall de su type en su hoja")
def u_037(b):
    """U-037 / BE-72: conteos por type vs inventario_tags. U-138 (auditoría 4-nov): sin la salida de inventario_tags se usa el
    inventario.json de la corrida (mismas ocurrencias que cuenta U-117); sin ninguno de los dos y con walls = FAIL (antes AMBER
    mientras U-117 daba PASS con el inventario.json: dos chequeos del mismo barrido que se contradecían)."""
    if not b.inventario:
        occ = _inv_ocurrencias(b)
        if occ:
            b.inventario = [{"type": o.get("type"), "sheet": o.get("sheet"), "kind": o.get("kind"), "id": o.get("id")} for o in occ]
        elif b.walls():
            return R("FAIL", "sin inventario de tags (inventario_tags *.json ni 1_inventario/inventario.json): no hay barrido "
                             "por tag contra el cual contar los walls")
        else:
            return NA("sin walls ni inventario")
    have = {}
    for w in b.walls_todos():                     # BE-CR10: + existing_walls (board-only)
        have.setdefault((_tipo_de(w), w.get("sheet") or (w.get("band") or {}).get("sheet")), 0)
        have[(_tipo_de(w), w.get("sheet") or (w.get("band") or {}).get("sheet"))] += 1
    none = b.canon.get("types_none_reason") or {}
    none = {str(x.get("type") if isinstance(x, dict) else x).upper() for x in (none if isinstance(none, list) else none.keys())}
    # R80f.44 (Chuze FINAL8, BE-142): ONE WALL ONCE - un tag del inventario que el canon descarta con motivo (tags_descartados:
    # 'shown on the enlarged plan, counted there') o que un wall de otra hoja reclama en tag_ids ya tiene su wall: no falta
    duenos = {str(x) for w in b.walls_todos() for x in (w.get("tag_ids") or [])}
    duenos |= {str(x.get("id")) for x in (b.canon.get("tags_descartados") or [])
               if isinstance(x, dict) and len(str(x.get("motivo") or "").strip()) >= 8}
    falta = {}
    for t in b.inventario:
        if not isinstance(t, dict):
            continue
        if t.get("id") and str(t["id"]) in duenos:
            continue
        ty, sh = str(t.get("type") or "").upper(), t.get("sheet") or t.get("hoja")
        if ty and ty not in none and not have.get((ty, sh)):
            falta.setdefault((ty, sh), 0)
            falta[(ty, sh)] += 1
    ncol = sum(1 for t in b.inventario if isinstance(t, dict) and t.get("kind") == "column")
    ncw = sum(1 for w in b.walls() if str(w.get("element")) == "column_wrap")
    ev = [f"type {k[0]} en {k[1]}: {v} tag(s) del inventario y 0 walls" for k, v in sorted(falta.items())]
    if ncol and ncw < ncol and not b.canon.get("columns_none_reason"):
        ev.append(f"{ncol} columnas en el inventario y {ncw} column wraps (sin columns_none_reason)")
    return R("FAIL", *ev) if ev else R("PASS", f"{len(b.inventario)} tags del inventario con wall de su type")


@chk("U-043", "BE-94", desc="U-043 / BE-94: la versión vigente del INDICE registra la prueba del BANCO (todas las lecturas "
     "guardadas) con 0 familias que empeoran")
def u_043(b, indice_txt=None):
    """U-043 / BE-94: banco de regresión registrado para la versión vigente (se corre también en verificar_version)."""
    t = indice_txt if indice_txt is not None else b.textos.get("INDICE.md")
    if t is None:
        return NA("se revisa al armar la versión (verificar_version.py revisar_banco)")
    return banco_vigente(t)


def banco_vigente(indice_txt):
    bloques = re.split(r"\n(?=\*\*\d{2}-[a-z]{3}: )", indice_txt)
    vig = [x for x in bloques if re.search(r"VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO\*\*", x)]
    if not vig:
        return R("FAIL", "INDICE.md sin bloque VERSIÓN VIGENTE")
    v = vig[-1]
    if not re.search(r"(?i)banco", v):
        return R("FAIL", "la versión vigente no registra la prueba del banco (U-043: todo arreglo validado contra TODAS las lecturas)")
    if not re.search(r"(?i)= ?0 (familias )?(distintas|diferencias)|0 familias distintas|0 diferencias", v):
        return R("FAIL", "el banco de la versión vigente no dice 0 familias distintas / 0 diferencias")
    return R("PASS", "banco registrado con 0 diferencias")


@chk("U-051", "BE-100", desc="U-051 / BE-100: el bid set que recibe la sesión no trae markups de otro take-off (solo se "
     "conservan las anotaciones 'AutoCAD SHX Text')")
def u_051(b):
    """U-051 / BE-100: copia limpia del bid set."""
    if b.bidset_annots is None:
        return NA("sin copia del bid set en la carpeta (entrega.json bidset / copia_limpia*.pdf)")
    malas = [a for a in b.bidset_annots if not re.search(r"(?i)SHX", (a.get("title") or "") + " " + (a.get("subject") or ""))]
    if malas:
        return R("FAIL", f"{len(malas)} anotaciones que no son AutoCAD SHX Text en el bid set (markups de otro take-off): "
                 "correr copia_limpia.py antes de dárselo a la sesión")
    return R("PASS", f"bid set limpio ({len(b.bidset_annots)} anotaciones SHX conservadas)")


@chk("U-057", "BE-110", desc="U-057 / BE-110: criterios fijos por programa: ninguna altura medida a escala sin RFI y board "
     "sin descontar aberturas")
def u_057(b):
    """U-057 / BE-110: criterios fijados por el programa."""
    if not b.walls():
        return SIN("canon")
    ev = []
    rx_esc = re.compile(r"(?i)scaled|measured (?:at|to) scale|by scale|a escala|escalad")
    for w in b.walls():
        for k, src in (("height", w.get("height_source")),) + tuple(("face " + str(f.get("side")), f.get("height_source"))
                                                                    for f in w.get("faces") or [] if isinstance(f, dict)):
            if rx_esc.search(str(src or "")) and not re.search(r"(?i)\bRFI-?\d|supuesto|assum", str(src)):
                ev.append(f"{w.get('id')} {k}: altura medida a escala sin supuesto rotulado + RFI ('{str(src)[:70]}')")
        for f in w.get("faces") or []:
            txt_ = re.sub(r"(?i)(?:no longer|not|never|without|sin)\s+(?:be\s+)?deduct\w*|(?:never|not|no|without)\s+deduct\w*|"
                          r"sin descontar", " ",
                          " ".join(str(v) for v in (f.values() if isinstance(f, dict) else [f])) + " " + str(w.get("board_op") or ""))   # R80e.145: valores, no claves
            if isinstance(f, dict) and re.search(r"(?i)(deduct|less|minus|net of)[^.]{0,30}(opening|door|window)|"
                                                  r"(opening|door|window)s?[^.]{0,30}deducted", txt_):
                ev.append(f"{w.get('id')} face {f.get('side')}: board con aberturas descontadas (criterio fijo: sin descontar)")
    return R("FAIL", *ev) if ev else R("PASS", "sin alturas a escala ni aberturas descontadas")


RX_EXT = re.compile(r"(?i)exterior (?:elevation|face|side|dim)|\bext(?:\.|erior)? elev|building elevation|"
                    r"T\.?O\.? (?:parapet|(?:low |high )?eave)|fa[cç]ade")


@chk("U-058", "BE-111", desc="U-058 / BE-111: la altura de una cara INTERIOR no sale de una cota de fachada exterior")
def u_058(b):
    """U-058 / BE-111: cota de la misma cara."""
    if not b.walls():
        return SIN("canon")
    ev = []
    for w, f in b.faces():
        lado = f"{f.get('side') or ''} {f.get('room') or ''}"
        if re.search(r"(?i)exterior|outside|\bext\b", lado) or re.search(r"(?i)exterior|sheathing", str(f.get("board") or "")):
            continue                     # BE-CR25: la cara de exterior gyp sheathing toma su altura de la fachada (floor to floor)
        src = str(f.get("height_source") or "")
        if RX_EXT.search(src) and not re.search(r"(?i)interior face|same face|inside face|misma cara|estimator decision|R-ALC-\d", src):
            ev.append(f"{w.get('id')} cara '{lado.strip()[:40]}': altura de board desde una cota exterior ('{RX_EXT.search(src).group(0)}')")
    return R("FAIL", *ev) if ev else R("PASS", "ninguna cara interior con altura de cota exterior")


@chk("U-079", "BE-CF01", desc="U-079 / BE-CF01: el texto SHX de las hojas M / P / E sigue en el set (la copia limpia no lo borró)")
def be_cf01(b):
    """BE-CF01: SHX conservado."""
    if b.hojas is None:
        return SIN("set_texto.json")
    mpe = {h: t for h, t in b.hojas.items() if re.match(r"^(M|P|E|MP|FP|EP)-?\d", h)}
    if not mpe:
        return NA("el set no trae hojas M / P / E")
    vacias = [h for h, t in mpe.items() if len(re.findall(r"[A-Za-z]{3,}", t)) < 15]
    if b.bidset_original_shx and b.bidset_annots is not None:
        shx = sum(1 for a in b.bidset_annots if "SHX" in (a.get("title") or "") + (a.get("subject") or ""))
        if shx < b.bidset_original_shx:
            vacias.append(f"la copia tiene {shx} SHX de {b.bidset_original_shx} del original")
    if len(vacias) >= max(1, len(mpe) // 2):
        return R("FAIL", f"hojas M/P/E sin texto (SHX borrado por la copia limpia): {vacias[:8]}")
    return R("PASS", f"{len(mpe) - len(vacias)} / {len(mpe)} hojas M/P/E con texto")


@chk("U-081", "BE-CF06", desc="U-081 / BE-CF06: comparar_extra.py corrió: revision_extra con A vs B de board-only, cielos, misc y demo")
def u_081(b):
    """U-081 / BE-CF06: comparar_extra después de comparar."""
    if not (b.canon_a and b.canon_b):
        return NA("sin lecturas A / B guardadas")
    fam = [k for k in ("existing_walls", "ceilings", "misc_items", "demolition") if (b.canon_a.get(k) or b.canon_b.get(k))]
    if not fam:
        return NA("las lecturas no traen board-only, cielos, misc ni demo")
    t = " ".join(v for k, v in b.textos.items() if "revision_extra" in k)
    if not t:
        return R("FAIL", f"las lecturas traen {fam} y no hay revision_extra.md (comparar_extra.py no corrió)")
    claves = {"existing_walls": r"(?i)board[- ]only|existing", "ceilings": r"(?i)ceiling|cielo", "misc_items": r"(?i)misc",
              "demolition": r"(?i)demo"}
    falta = [k for k in fam if not re.search(claves[k], t)]
    return R("FAIL", f"revision_extra.md sin A vs B de {falta}") if falta else R("PASS", f"A vs B de {fam}")


RX_CONFLICTO = re.compile(r"(?i)conflict|contradict|differs? from (?:the )?spec|spec (?:says|calls)|plan vs\.? spec|"
                          r"drawings? vs\.? spec|vs\.? code|code (?:says|requires)[^.]{0,40}(?:but|while)")
RX_SPEC = re.compile(r"\b0[5-9]\s?\d{2}\s?\d{2}\b|\bSection\s+\d|\bASTM\b|\bGA-\d|\bIBC\b|\bCBC\b|\bAISI\b|\bUL\b|¶")


RX_POR_CODIGO = re.compile(r"(?i)\bper (?:the )?code\b|\bby code\b|\bCODE:|\bcode requires\b|\brequired by (?:the )?code\b|\(B\) Code \(")
# CR-R13 E2: nombre de norma suelto dentro de la cita por código (GA-216 / ASTM C1396 / ANSI A108 / TCNA / NFPA 80) sin sección / tabla
RX_NORMA = re.compile(r"\b(?:GA-\d{3}|ASTM\s+[A-Z]\s?\d{2,4}(?:/[A-Z]\d+M?)?|ANSI\s+[A-Z]\d{3}(?:\.\d+)*|TCNA|NFPA\s+\d+)")
RX_NORMA_SEC = re.compile(r"^[^.;|()]{0,30}?(?:Section|Table|§|Sec\.|\b\d+(?:\.\d+)+\b|\b[A-Z]\d{3}\b)")
# CR-R13 E2 (auditoría COORDINACIÓN 9-nov): el NOMBRE de una norma ('GA-216', 'ASTM C1396') sin sección / tabla no es cita
RX_CITA_CODIGO = re.compile(r"\b(?:IBC|CBC)\b(?: 20\d\d)?\s+(?:Section\s+|Table\s+|§\s?)?\d{3,4}(?:\.\d+)*|\bSection\s+\d|\bTable\s+\d|§\s?\d|"
                            r"\bUL\s+(?:design\s+)?[A-Z]{1,2}\d{3}")   # CR-R14 (U-156): 'none applies' sin sección ya no es cita


@chk("U-155", desc="U-155 (usuario 8-nov): 'buscar hasta encontrar las respuestas en los planos; si no, usa los códigos del IBC y cita su "
     "referencia': todo valor / opción 'per code / by code / CODE:' del Excel cita sección o tabla (IBC / CBC / ASTM / GA / UL / NFPA) "
     "o declara 'none applies'; sin cita = FAIL (la respuesta impresa la vigila CE_RFI_BARRIDO_IMPRESO)")
def u_155(b):
    ev, n = [], 0
    for h, coord, t in b.celdas:
        for m in RX_POR_CODIGO.finditer(str(t)):
            n += 1
            win = str(t)[m.start():m.end() + 250]
            if not RX_CITA_CODIGO.search(win):
                ev.append(f"{h}!{coord}: '{str(t)[m.start():m.end() + 90]}' sin sección / tabla del código")
                break
            suelta = [x.group(0) for x in RX_NORMA.finditer(win) if not RX_NORMA_SEC.search(str(t)[m.start() + x.end():])]   # la sección puede caer después de la ventana
            if suelta:
                ev.append(f"{h}!{coord}: norma sin sección / tabla {suelta[:3]} en '{win[:90]}'")
                break
    return R("FAIL", *ev) if ev else R("PASS", f"{n} valores por código con su sección / tabla")


@chk("U-082", "R-ALC-10", desc="U-082 / R-ALC-10: todo conflicto plano vs spec / código cargado con la opción A (plano) lleva "
     "NOTA con N/HOJA, la sección de spec / código y el delta")
def u_082(b):
    """U-082 / R-ALC-10: nota completa del conflicto."""
    ev, n = [], 0
    for h, coord, t in b.celdas:
        if not RX_CONFLICTO.search(t):
            continue
        n += 1
        falta = [x for x, rx in (("N/HOJA", RX_DET), ("sección de spec / código", RX_SPEC), ("delta", re.compile(r"(?i)delta|Δ")))
                 if not rx.search(t)]
        if falta:
            ev.append(f"{h}!{coord}: conflicto sin {', '.join(falta)}: '{t[:90]}'")
    if not n:
        return NA("ningún conflicto plano vs spec / código en el Excel")
    return R("FAIL", *ev[:15]) if ev else R("PASS", f"{n} conflictos con N/HOJA + sección + delta")


@chk("R-ALC-02", desc="R-ALC-02: blocking de accesorio sin medida impresa = 3 ft x 2 filas por accesorio, sin RFI")
def r_alc_02(b):
    """R-ALC-02: blocking de accesorios sin medida impresa."""
    ev, n = [], 0
    for it in b.canon.get("blocking_items") or []:
        if not isinstance(it, dict):
            continue
        src = " ".join(str(it.get(k) or "") for k in ("source", "lf_op", "label", "ref"))
        if not re.search(r"(?i)not printed|no (?:printed )?dimension|not dimensioned|sin medida|R-ALC-02", src):
            continue
        n += 1
        rows, lfe = _n(it.get("rows")), _n(it.get("lf_each"))
        if rows is not None and lfe is not None and not (rows == 2 and abs(lfe - 3.0) < 0.01):
            ev.append(f"{it.get('ref')}: sin medida impresa y cargado {rows:g} filas x {lfe:g} ft (regla: 2 x 3 ft)")
    for r in b.rfis_abiertos():
        if re.search(r"(?i)blocking[^.]{0,80}(accessor|grab bar|toilet accessor|fixture|mirror|dispenser|shelf)", str(r[1])):
            ev.append(f"{r[0]}: RFI de blocking de accesorio (R-ALC-02 lo decide: 3 ft x 2 filas)")
    if not n and not ev:
        return NA("ningún blocking de accesorio sin medida impresa")
    return R("FAIL", *ev) if ev else R("PASS", f"{n} blocking sin medida = 2 x 3 ft")


@chk("R-ALC-04", desc="R-ALC-04: si el set tiene demolición de gyp / metal frame, la demolición está cuantificada (nuestro alcance)")
def r_alc_04(b):
    """R-ALC-04: demolición de drywall / metal frame en alcance."""
    if b.hojas is None:
        return SIN("set_texto.json")
    rx = re.compile(r"(?i)(remove|demo\w*)[^.\n]{0,60}(gyp\w*|drywall|partition|stud|metal fram\w*|soffit|furring)|"
                    r"(partition|stud|gyp\w*|drywall)[^.\n]{0,40}to be (removed|demolished)")
    hs = [h for h, t in b.hojas.items() if (re.match(r"^D-?\d|^AD|^DM", h) or re.search(r"(?i)demolition plan", t)) and rx.search(t)]
    if not hs:
        return NA("el set no tiene demolición de gyp / metal")
    dem = [f for f in b.ms if re.search(r"(?i)demo", f["material"]) and (f["net"] or 0) > 0]
    if dem or b.canon.get("demolition") or b.canon.get("demo_items") or (b.demo or {}).get("items"):
        return R("PASS", f"demolición cuantificada ({len(dem)} renglones) para {hs[:4]}")
    sc = b.excel_txt(("Scope Checklist",))
    if re.search(r"(?i)demo\w*[^\n]{0,120}EXCLUDED", sc):
        return R("FAIL", f"demolición de gyp / metal EXCLUDED pero es nuestro alcance (hojas {hs[:4]})")
    return R("FAIL", f"el set demuele gyp / metal ({hs[:4]}) y no hay renglón de demolición")


# ---------------------------------------------------------------------------------------------- A. lectura del plano
@chk("BE-01", desc="BE-01: detalle 'FIRE STOP AT CEILING LINE' impreso -> renglón de fire-stop track (o destino)")
def be_01(b):
    if b.hojas is None:
        return SIN("set_texto.json")
    hs = _hojas_con(b, re.compile(r"(?i)fire ?stop[^.\n]{0,40}(ceiling line|track)|(track|stud)[^.\n]{0,40}fire ?stop"))
    if not hs:
        return NA("el set no imprime fire stop en la línea de cielo")
    if _tiene_fila(b, re.compile(r"(?i)fire ?stop")) or _destino(b, re.compile(r"(?i)fire ?stop")):
        return R("PASS", f"fire-stop track con destino ({hs[:3]})")
    return R("FAIL", f"fire stop impreso en {hs[:4]} sin renglón / EXCLUDED / RFI")


def _wet_rooms_wr(b):
    if b.hojas is None:
        return None
    return bool(re.search(r"(?i)\bW\.?R\.?\b|water[- ]resist\w*|moisture[- ]resist\w*|\bMR (gyp|board)", b.set_txt()))


@chk("BE-02", desc="BE-02: nota W.R. 'for wall AND ceiling' -> los cielos GWB de los wet rooms van en W.R.")
def be_02(b):
    if b.hojas is None:
        return SIN("set_texto.json")
    # CC-R4c (Consumer Cellular rev3 audit): 'WATER RESISTANT GYPSUM BOARD AT ALL WET LOCATIONS (... TOILET ROOM ...)' (A100
    # note 5) covers the gypsum ceiling of the wet room too; before only '... ceiling' notes counted -> N/A in vacuum
    if not re.search(r"(?i)(W\.?R\.?|water[- ]resist\w*|moisture[- ]resist\w*)[^.\n]{0,80}(ceiling|wet locations?|wet areas?)", b.set_txt()):
        return NA("ninguna nota W.R. para cielos ni para wet locations")
    ev = [f"ceiling {z.get('room')}: '{z.get('board')}' (wet room, nota W.R. de cielos)" for z in b.ceilings()
          if RX_WET.search(str(z.get("room") or "")) and z.get("board") and not re.search(r"(?i)act|grid|acoust|tile", str(z.get("system") or ""))
          and not RX_WR.search(str(z.get("board")))
          # BE-CR0-10b: la membrana rated SUPERIOR oculta sobre un cielo colgado del cuarto (doble cielo, 'above GYP-1 / ACT') no es el
          # cielo expuesto del wet room (mismo criterio que BE-XF13 en CE_COHERENCIA_R11 F2)
          and not re.search(r"(?i)\babove\b", str(z.get("room") or "")) and not z.get("stacked")]
    return R("FAIL", *ev) if ev else R("PASS", "cielos GWB de wet rooms en W.R.")


@chk("BE-03", desc="BE-03: toda cara con gypsum de un wet room va en W.R. (ninguna en Type X / regular)")
def be_03(b):
    w = _wet_rooms_wr(b)
    if w is None and not b.walls():
        return SIN("set_texto.json y canon")
    if w is False:
        return NA("el set no pide W.R. / MR")
    ev = [f"{x.get('id')} cara {f.get('side')} ({f.get('room')}): '{f.get('board')}'" for x, f in b.faces()
          if f.get("room") and all(RX_WET.search(x) for x in str(f.get("room")).split("/")) and f.get("board") and re.search(r"(?i)gyp|type ?x|regular|5/8|1/2", str(f.get("board")))
          and not RX_WR.search(str(f.get("board"))) and (f.get("layers") or 1)]
    return R("FAIL", *ev[:20]) if ev else R("PASS", "caras de wet rooms en W.R.")


@chk("BE-04", desc="BE-04: ninguna cara cuya sección dice SOLO plywood / FRT (sin gypsum) lleva board")
def be_04(b):
    if not b.walls():
        return SIN("canon")
    ev = []
    for x, f in b.faces():
        src = " ".join(str(f.get(k) or "") for k in ("board_source", "height_source", "source", "note"))
        if re.search(r"(?i)(plywood|FRT)[^.]{0,40}\bonly\b|no gyp|without gyp|sin gyp", src) and f.get("board") and \
                re.search(r"(?i)gyp|W\.?R|type ?x|regular|5/8", str(f.get("board"))) and (f.get("layers") or 0):
            ev.append(f"{x.get('id')} cara {f.get('side')}: la fuente dice solo plywood / FRT y carga '{f.get('board')}'")
    return R("FAIL", *ev) if ev else R("PASS", "ninguna cara sin gypsum con board")


@chk("BE-05", desc="BE-05: capas por cara = las del dibujo: una fuente que dice 1 LAYER no carga 2 capas")
def be_05(b):
    if not b.walls():
        return SIN("canon")
    ev = []
    for x, f in b.faces():
        src = str(f.get("board_source") or "") + " " + str(f.get("height_source") or "")
        if re.search(r"(?i)\(1\) layer|\b1 layer|one layer|single layer", src) and (_n(f.get("layers")) or 0) > 1:
            ev.append(f"{x.get('id')} cara {f.get('side')}: fuente '1 layer' y layers = {f.get('layers')}")
        if re.search(r"(?i)\(2\) layers|\b2 layers|two layers|double layer", src) and (_n(f.get("layers")) or 0) == 1:
            ev.append(f"{x.get('id')} cara {f.get('side')}: fuente '2 layers' y layers = 1")
    return R("FAIL", *ev) if ev else R("PASS", "capas por cara = fuente")


def _soffits(b):
    return [w for w in b.walls() if re.search(r"(?i)soffit|bulkhead", str(w.get("element") or "") + " " + str(w.get("tag") or ""))] + \
        [x for x in b.canon.get("framed_soffits") or [] if isinstance(x, dict)]


@chk("BE-06", desc="BE-06: todo soffit con cada lado expuesto + su fondo (no una sola cara)")
def be_06(b):
    ss = _soffits(b)
    if not ss:
        return NA("sin soffits en el canon") if b.walls() else SIN("canon")
    ev = []
    grupos = {}
    for s in ss:
        if re.search(r"(?i)side", str(s.get("element") or "")):      # soffit_side: un lado por elemento, se agrupan
            grupos.setdefault(re.sub(r"-[A-Z0-9]{1,3}$", "", str(s.get("id"))), []).append(s)
    for g, xs in grupos.items():
        if len(xs) < 2 and not re.search(r"one side|single side|against (wall|structure)", json.dumps(xs).lower()):
            ev.append(f"{g}: soffit con un solo lado ({xs[0].get('id')}) y sin motivo")
    for s in ss:
        if re.search(r"(?i)side", str(s.get("element") or "")):
            continue
        fs = [f for f in s.get("faces") or [] if isinstance(f, dict) and (f.get("layers") or 0)]
        txt = json.dumps(s).lower()
        if s.get("faces") is not None and len(fs) < 2 and not re.search(r"one side|single side|against (wall|structure)|bottom", txt):
            ev.append(f"{s.get('id') or s.get('ref')}: soffit con {len(fs)} cara(s) con board (faltan lado / fondo)")
    return R("FAIL", *ev) if ev else R("PASS", f"{len(ss)} soffits con lados + fondo")


@chk("BE-07", desc="BE-07: cada tag '<type> SIM.' de la planta tiene su fila de remate")
def be_07(b):
    if b.hojas is None:
        return SIN("set_texto.json")
    types = {str(t.get("type") if isinstance(t, dict) else t).upper() for t in b.schedule()} - {"", "NONE"}
    if not types:
        return NA("sin partition_schedule en el canon")
    rx = re.compile(r"(?<![A-Z0-9])(" + "|".join(re.escape(t) for t in sorted(types, key=len, reverse=True)) + r")\s+SIM\.?(?![A-Z])")
    hits = {(h, m.group(1)) for h, t in b.hojas.items() if re.match(r"^A", h) for m in rx.finditer(t)}
    if not hits:
        return NA("ningún tag '<type> SIM.' en las plantas")
    txt = json.dumps(muros_canon(b.canon)) + b.excel_txt(("Partition Takeoff",))
    if re.search(r"(?i)\bSIM\b|remate|return|end face", txt):
        return R("PASS", f"{len(hits)} tags SIM. con fila de remate")
    return R("FAIL", f"tags SIM. sin fila de remate: {sorted(hits)[:6]}")


@chk("BE-09", desc="BE-09: ningún wall EXISTING / to remain cuantificado como nuevo")
def be_09(b):
    if not b.walls():
        return SIN("canon")
    ev = []
    for w in b.walls():
        t = " ".join(str(w.get(k) or "") for k in ("id", "tag", "status", "length_source", "source", "note"))
        if re.search(r"(?i)existing (wall|partition)s? to remain|\bto remain\b|\(E\) (wall|partition)|existing partition", t) and \
                not re.search(r"(?i)new|replace|repair|board[- ]only", t) and (w.get("faces") or []):
            ev.append(f"{w.get('id')}: existing / to remain en walls[] (va EXCLUDED o board-only)")
    return R("FAIL", *ev) if ev else R("PASS", "sin walls existing como nuevos")


@chk("BE-10", desc="BE-10: soffit con cota 'HOLD' cuantificado + RFI, nunca 'not priced'")
def be_10(b):
    t = b.excel_txt(("Scope Checklist", "Review Items", "Pending Items", "Material Summary"))
    m = re.search(r"(?i)[^\n]{0,80}\bHOLD\b[^\n]{0,80}(not priced|not carried|no price|not quantified)[^\n]{0,40}|"
                  r"(not priced|not carried|not quantified)[^\n]{0,80}\bHOLD\b", t)
    return R("FAIL", f"cota HOLD dejada sin precio: '{m.group(0)[:140]}'") if m else R("PASS", "ninguna cota HOLD sin cuantificar")


@chk("BE-11", desc="BE-11: área rotulada 'AREA OF … PLYWOOD / BACKING / BLOCKING' con SF cargados")
def be_11(b):
    if b.hojas is None:
        return SIN("set_texto.json")
    hs = _hojas_con(b, re.compile(r"(?i)AREA OF[^.\n]{0,50}(PLYWOOD|BACKING|BLOCKING)"))
    if not hs:
        return NA("ningún área rotulada de plywood / backing")
    if _tiene_fila(b, re.compile(r"(?i)plywood|backing|blocking")) or _destino(b, re.compile(r"(?i)plywood|backing")):
        return R("PASS", f"área rotulada con renglón ({hs[:3]})")
    return R("FAIL", f"'AREA OF … PLYWOOD' impreso en {hs[:4]} sin renglón")


RX_CITA = re.compile(r"(?<![A-Za-z0-9])[\"“']([A-Z0-9][A-Z0-9 \-/.,#@()&:]{17,}?)[\"”']")


@chk("BE-12", desc="BE-12: toda cita textual (entre comillas) del Excel existe impresa en el set")
def be_12(b):
    if b.hojas is None:
        return SIN("set_texto.json")
    todo = " " + _norm(b.set_txt()) + " "
    ev, n = [], 0
    for h, coord, t in b.celdas:
        for m in RX_CITA.finditer(t):
            q = _norm(m.group(1))
            if len(q.split()) < 3 or re.fullmatch(r"[\d ]+", q):
                continue
            n += 1
            partes = [_norm(x) for x in re.split(r"\.\.\.|…", m.group(1)) if len(_norm(x).split()) >= 2]   # R80e.145: elipsis
            if partes and len(partes) > 1 and all(x in todo for x in partes):
                continue
            if " " + q + " " not in todo and q not in todo:
                ev.append(f"{h}!{coord}: cita '{m.group(1)[:70]}' no está impresa en el set (default del skill citado como nota)")
    if not n:
        return NA("sin citas textuales en el Excel")
    return R("FAIL", *ev[:15]) if ev else R("PASS", f"{n} citas textuales impresas")


@chk("BE-13", desc="BE-13: backboard / plywood / backing de hojas E / M / P con destino")
def be_13(b):
    if b.hojas is None:
        return SIN("set_texto.json")
    hs = _hojas_con(b, re.compile(r"(?i)backboard|plywood|\bbacking\b"), r"^(E|M|P|T|EP|FP)-?\d")
    if not hs:
        return NA("ninguna hoja E/M/P pide backboard / plywood")
    if _destino(b, re.compile(r"(?i)backboard|plywood|backing")):
        return R("PASS", f"backboard de {hs[:3]} con destino")
    return R("FAIL", f"backboard / plywood en {hs[:5]} sin renglón, EXCLUDED ni RFI")


RX_NO_IMPRESO = re.compile(r"(?i)not printed|not specified|not dimensioned|not shown|no impreso|not noted")


@chk("BE-14", desc="BE-14: ninguna afirmación 'not printed / not specified' cuyo término aparece impreso con su valor en el set")
def be_14(b):
    if b.hojas is None:
        return SIN("set_texto.json")
    ev, n = [], 0
    for h, coord, t in b.celdas:
        if h not in ("Pending Items", "Scope Checklist", "Review Items") or not RX_NO_IMPRESO.search(t):
            continue
        n += 1
        # v81cf25 (CFA rev5): solo los términos de la MISMA frase que dice 'not printed' (una frase vecina que cita la C.H.
        # impresa que sí se usó no es la afirmación)
        fr = " ".join(x for x in re.split(r"(?<=[.;])\s+|\s\|\s|\s-\s(?=[a-z])", t) if RX_NO_IMPRESO.search(x))
        ts = set(re.findall(r"\b(?:T\.O\.|B\.O\.)\s?[A-Z0-9\-]+|\b[A-Z]{2,}-\d+\b", fr))
        for q in ts:
            for hh, tt in b.hojas.items():
                for m in re.finditer(re.escape(q), tt):
                    if RX_FTIN.search(tt[m.end():m.end() + 40]):
                        ev.append(f"{h}!{coord}: dice no impreso pero '{q}' está en {hh} con valor '{' '.join(tt[m.start():m.end() + 30].split())}'")
                        break
    if not n:
        return NA("sin afirmaciones 'not printed'")
    return R("FAIL", *ev[:10]) if ev else R("PASS", f"{n} afirmaciones 'not printed' sin valor impreso en el set")


@chk("BE-15", desc="BE-15: el miembro del renglón = el rotulado en su detalle (un JOIST / horizontal no se carga como poste)")
def be_15(b):
    ev = []
    for it in list(b.canon.get("misc_items") or []) + list(b.canon.get("blocking_items") or []):
        if not isinstance(it, dict):
            continue
        src = " ".join(str(it.get(k) or "") for k in ("source", "label"))
        fam = " ".join(str(it.get(k) or "") for k in ("familia", "ref", "op"))
        if re.search(r"(?i)\bjoists?\b|horizontal", src) and re.search(r"(?i)\bpost\b|vertical|\bjamb\b", fam) and \
                not re.search(r"(?i)joist|horizontal", fam):
            ev.append(f"{it.get('ref')}: el detalle rotula joist / horizontal y el renglón lo carga como '{fam[:50]}'")
    amb = []
    ocr = set(b.set_meta.get("ocr") or [])
    if b.hojas:
        for f in b.ms:
            hn = {norm_hoja(k): k for k in b.hojas}         # R80f.35
            for n_, sh in RX_DET.findall(f["fuente"]):
                if n_.startswith("KN"):          # v81cf25: 'KN7/A-201' = keynote 7 de la hoja (el plano imprime el número), no una burbuja
                    continue
                sh = hn.get(norm_hoja(sh), sh)
                if sh in b.hojas and not re.search(r"(?<![A-Z0-9])" + re.escape(n_) + r"(?![A-Z0-9])", b.hojas[sh]) and \
                        not _ref_verificada(b, n_, sh):
                    msg = f"MS fila {f['fila']}: cita {n_}/{sh} y la hoja {sh} no tiene el detalle {n_}"
                    # R80e.145: hoja raster leída por OCR: una burbuja / tag en hexágono no siempre sale en el OCR ->
                    # AMBER (verificar en la imagen), no FAIL; con capa de texto real sigue siendo FAIL
                    (amb if sh in ocr else ev).append(msg + (" (hoja OCR: verificar en la imagen)" if sh in ocr else ""))
                    break
    if ev:
        return R("FAIL", *ev[:15], *amb[:5])
    return R("AMBER", *amb[:15]) if amb else R("PASS", "miembros y burbujas citadas coinciden")


def _ref_verificada(b, n, sh):
    """U-138 (O'Reilly rev7, CB_BE_15 AMBER resuelto a ojo): la referencia n/sh existe aunque el OCR de la hoja raster no la
    lea: (1) detalle / nota verificado a ojo con imagen (burbujas_verificadas.json detalle_existe), o (2) tag de partition
    del inventario de ESA hoja con recorte circulado y reabierto (png_verificado)."""
    if _detalle_verificado(b, n, norm_hoja(sh)):
        return True
    return any(str(o.get("type") or "").upper() == n.upper() and norm_hoja(o.get("sheet")) == norm_hoja(sh) and o.get("png")
               and o.get("png_verificado") is True for o in _inv_ocurrencias(b))


RX_ACC = re.compile(r"(?i)\b(clip angles?|deflection clips?|slide clips?|bridging clips?|relief channel|runner channel|flat straps?|"
                    r"L\s?\d{1,2}\s?[xX]\s?\d{1,2}|kicker|spazzer|stud kicker|moment clips?|"
                    # CC-R4e (Consumer Cellular rev3 audit): 'METAL STRAPPING' (A104), 'BACKING PLATE' (A104), 'SHEET METAL
                    # ANGLE' (A501) were invisible -> N/A in vacuum
                    r"metal strapping|backing plate|sheet metal angle)\b")


@chk("BE-16", desc="BE-16: cada accesorio impreso en los detalles del trade (clips, angles, kickers, straps) tiene destino")
def be_16(b):
    if b.hojas is None:
        return SIN("set_texto.json")
    pr = {}
    for h, t in b.hojas.items():
        if re.match(r"^(A|S)", h):
            for m in RX_ACC.finditer(t):
                pr.setdefault(_norm(m.group(1)).rstrip("S"), h)
    if not pr:
        return NA("ningún accesorio impreso en hojas A / S")
    ex = _norm(b.excel_txt())
    falta = [f"'{k}' ({h})" for k, h in pr.items() if k not in ex and k.replace(" ", "") not in ex.replace(" ", "")]
    return R("FAIL", "accesorios impresos sin renglón / EXCLUDED / RFI: " + ", ".join(falta[:12])) if falta else \
        R("PASS", f"{len(pr)} accesorios impresos con destino")


def _fasteners_cargados(b):
    return [f for f in b.ms if RX_FASTENER.search(f["material"]) and not re.search(r"(?i)clips?|angle", f["material"]) and (f["net"] or 0) > 0]


@chk("BE-17", desc="BE-17: fasteners por gauge: con varios gauges cada producto dependiente sale por gauge (o todo EXCLUDED, U-053)")
def be_17(b):
    fs = _fasteners_cargados(b)
    if not fs:
        return NA("tornillería EXCLUDED (U-053) o sin fasteners cargados")
    gs = {str(w.get("gauge")).upper() for w in b.walls() if w.get("gauge")}
    if len(gs) > 1 and not any(re.search(r"(?i)\d{2}\s?GA|gauge", f["material"]) for f in fs):
        return R("FAIL", f"{len(gs)} gauges en los walls y los fasteners no se separan por gauge")
    return R("PASS", "fasteners por gauge")


def _cobertura(b):
    return {k: v for k, v in b.textos.items() if re.search(r"(?i)cobertura|PASO12", k)}


@chk("BE-18", "BE-VS-03", desc="BE-18 / BE-VS-03: matriz de cobertura (Paso 12) con 0 GAP")
def be_18(b):
    cs = _cobertura(b)
    if not cs:
        return SIN("matriz de cobertura (Paso 12) en la carpeta")
    ev = []
    for k, t in cs.items():
        for l in t.splitlines():
            if re.search(r"\|\s*GAP\s*\|", l) and not re.search(r"(?i)\b0\s*GAP|resuelto|resolved|closed", l):
                ev.append(f"{k}: {l.strip()[:120]}")
    return R("FAIL", *ev[:15]) if ev else R("PASS", "cobertura sin GAP")


@chk("BE-19", "BE-56", desc="BE-19 / BE-56: fastener cargado con un espaciamiento impreso (no default) — o tornillería EXCLUDED")
def be_19(b):
    fs = _fasteners_cargados(b)
    if not fs:
        return NA("tornillería EXCLUDED (U-053) o sin fasteners cargados")
    if b.hojas is None:
        return SIN("set_texto.json")
    todo = b.set_txt()
    ev = []
    for f in fs:
        for esp in re.findall(r"@\s*(\d{1,2})\"", b.ms_txt(f)):
            if not re.search(r"@\s*" + esp + r"\"", todo):
                ev.append(f"MS fila {f['fila']}: espaciamiento @ {esp}\" no impreso en el set")
    return R("FAIL", *ev) if ev else R("PASS", "espaciamientos de fasteners impresos")


@chk("BE-20", desc="BE-20: framed soffit con studs Y 2 tracks (no solo perímetro)")
def be_20(b):
    ss = _soffits(b)
    if not ss:
        return NA("sin soffits")
    t = " ".join(b.ms_txt(f) for f in b.ms if re.search(r"(?i)track", f["material"]))
    s = " ".join(b.ms_txt(f) for f in b.ms if re.search(r"(?i)stud", f["material"]))
    rx = re.compile(r"(?i)soffit|bulkhead")
    # R80f.36: el desglose nombra cada soffit por su Wall ID (A-A421.A-1 ...): todos los ids presentes = cargado
    ids = [str(x.get("id")) for x in ss if x.get("id")]
    con_id = lambda y: bool(ids) and all(re.search(r"(?<![\w.\-])" + re.escape(i) + r"(?![\w.])", y) for i in ids)   # noqa: E731
    madera = all(re.search(r"(?i)\bwood\b|\b2x|suspension", str(x.get("framing") or "")) for x in ss)   # BE-CR29: stud de madera = Div. 06 EXCLUDED; suspension = sin studs
    solo_madera = all(re.search(r"(?i)\bwood\b|\b2x", str(x.get("framing") or "")) and not re.search(r"(?i)metal|track|stud|cfmf|channel", str(x.get("framing") or "").replace("wood stud", "")) for x in ss)
    # BE-CR0-10: soffit armado SOLO en madera (Div. 06 EXCLUDED) no lleva track metálico tampoco
    falta = [x for x, y in (("track", t), ("stud", s)) if not rx.search(y) and not con_id(y) and not (x == "stud" and madera) and not (x == "track" and solo_madera)]
    if falta:
        return R("FAIL", f"soffits sin {falta} en el desglose del Material Summary")
    return R("PASS", "soffits con tracks; studs: framing de madera (Div. 06 EXCLUDED) / suspension, sin studs metálicos" if madera else "soffits con studs + tracks")


def _fila_con_cita(b, rx_mat, rx_set, nombre):
    fs = _tiene_fila(b, rx_mat)
    if not fs:
        return NA(f"sin renglón de {nombre}")
    if b.hojas is None:
        return SIN("set_texto.json")
    if _hojas_con(b, rx_set):
        return R("PASS", f"{nombre} rotulado en {_hojas_con(b, rx_set)[:3]}")
    return R("FAIL", *[f"MS fila {f['fila']} '{f['material'][:50]}': {nombre} sin rótulo impreso en el set" for f in fs])


@chk("BE-21", desc="BE-21: glass mat solo donde un detalle / tag lo rotula")
def be_21(b):
    return _fila_con_cita(b, re.compile(r"(?i)glass[- ]?mat|dens[- ]?(glass|shield|armor)"),
                          re.compile(r"(?i)glass[- ]?mat|dens[- ]?(glass|shield|armor)|fiber[- ]?glass[- ]reinforced\s+(?:gypsum\s+)?"
                                     r"sheathing|glass[- ]fiber[- ]faced"), "glass mat")   # R80e.145: rótulo impreso equivalente


@chk("BE-22", desc="BE-22: jamb return solo con detalle que lo dibuja")
def be_22(b):
    return _fila_con_cita(b, re.compile(r"(?i)jamb return|return at jamb"), re.compile(r"(?i)\breturn\b"), "jamb return")


@chk("BE-23", desc="BE-23: acoustical sealant EXCLUDED (sin renglón con cantidad)")
def be_23(b):
    fs = _tiene_fila(b, re.compile(r"(?i)acoustic\w* seal|sealant"))
    return R("FAIL", *[f"MS fila {f['fila']} '{f['material']}' net {f['net']}" for f in fs]) if fs else R("PASS", "sin acoustical sealant cargado")


RX_GYP_CLG = re.compile(r"(?i)\b(?:GWB|gyp(?:sum)?\.? ?(?:bd|board))\b.{0,40}\b(?:ceiling|clg|hard lid|soffit)|"
                        r"\b(?:ceiling|clg|hard lid|soffit)\b.{0,40}\b(?:GWB|gyp(?:sum)?\.? ?(?:bd|board))\b|^GWB-CLG")


@chk("BE-25", desc="BE-25: cada ceiling de gypsum cita el detalle de su sistema de suspensión")
def be_25(b):
    # CC-R4b (Consumer Cellular rev3 audit): a drywall suspension grid (usg_grid) with gypsum board IS a gypsum ceiling;
    # only ACT / lay-in / tile / none / existing are not (before: 'grid' excluded the C-1 gyp ceiling -> N/A in vacuum)
    zs = [z for z in b.ceilings() if not re.search(r"(?i)\bact\b|acoust|lay-?in|tile|none|existing", str(z.get("system") or ""))
          and not (re.search(r"(?i)grid", str(z.get("system") or "")) and not re.search(r"(?i)usg_grid|drywall|gyp", str(z.get("system") or "") + " " + str(z.get("board") or "")))]
    # U-138 (auditoría 4-nov): los cielos / hard lids de gypsum cargados como misc_items (O'Reilly GWB-CLG-* de 7/A4.2) y los
    # soffits también son cielos de gypsum: "N/A sin cielos" cuando el canon los tiene (o el set los imprime, BE-70) = FAIL
    zs += [dict(m, room=m.get("ref"), system=m.get("label") or m.get("familia")) for m in b.canon.get("misc_items") or []
           if isinstance(m, dict) and RX_GYP_CLG.search(" ".join(str(m.get(k) or "") for k in ("ref", "label", "familia")))]
    zs += [dict(s, room=s.get("id"), system=s.get("element")) for s in _soffits(b)]
    if not zs:
        if b.hojas is not None and _hojas_con(b, re.compile(r"(?i)gyp(sum)?\.? ?(bd|board)\.?[^.\n]{0,30}(ceiling|clg|soffit)|"
                                                            r"(ceiling|soffit)[^.\n]{0,30}gyp(sum)?\.? ?(bd|board)")) \
                and not (b.canon.get("ceilings_none_reason") or b.canon.get("ceilings_info")):
            return R("FAIL", "el set imprime cielos / soffits de gypsum (BE-70) y el canon no trae ninguno ni ceilings_none_reason")
        return NA("sin cielos de gypsum")
    ev = [f"ceiling {z.get('room')}: sistema '{z.get('system')}' sin detalle N/HOJA" for z in zs
          if not RX_DET.search(" ".join(str(z.get(k) or "") for k in ("system_callout", "system_source", "detail", "source", "height_source",
                                                                       "detail_source")))]
    return R("FAIL", *ev[:15]) if ev else R("PASS", f"{len(zs)} cielos con su detalle de sistema")


@chk("BE-26", desc="BE-26: type K / ballistic medido al hatch / cota, no a nodos")
def be_26(b):
    ws = [w for w in b.walls() if re.search(r"(?i)ballistic", json.dumps(w)) or str(w.get("tag")).upper() == "K"]
    if not ws:
        return NA("sin ballistic")
    ev = [f"{w.get('id')}: ballistic medido a nodo" for w in ws if re.search(r"(?i)\bnode", str(w.get("length_source")))
          and not re.search(r"(?i)hatch|printed|cota", str(w.get("length_source")))]
    return R("FAIL", *ev) if ev else R("PASS", f"{len(ws)} walls ballistic al hatch / cota")


@chk("BE-27", desc="BE-27: recess de ATM / equipo con sus piezas o razón none")
def be_27(b):
    if b.hojas is None:
        return SIN("set_texto.json")
    hs = _hojas_con(b, re.compile(r"\bATM\b|(?i:equipment recess|recessed (?:cabinet|equipment))"), r"^A")
    if not hs:
        return NA("sin ATM / recess")
    if b.canon.get("atm_recess_none_reason") or re.search(r"(?i)\bATM\b|recess", json.dumps(b.canon.get("misc_items") or [])) or \
            _destino(b, re.compile(r"(?i)\bATM\b|recess")):
        return R("PASS", f"ATM / recess con destino ({hs[:3]})")
    return R("FAIL", f"ATM / recess impreso en {hs[:4]} sin piezas ni razón")


@chk("BE-28", desc="BE-28: canopy / parapet nuevo con su framing o destino")
def be_28(b):
    if b.hojas is None:
        return SIN("set_texto.json")
    hs = _hojas_con(b, re.compile(r"(?i)(canopy|parapet)[^.\n]{0,60}(stud|framing|track|sheathing)|(stud|framing)[^.\n]{0,40}(canopy|parapet)"), r"^A")
    if not hs:
        return NA("sin canopy / parapet de framing")
    if _destino(b, re.compile(r"(?i)canopy|parapet")):
        return R("PASS", f"canopy / parapet con destino ({hs[:3]})")
    return R("FAIL", f"canopy / parapet con framing en {hs[:4]} sin renglón / NOT APPLICABLE / RFI")


@chk("BE-29", desc="BE-29: header 'assumed' sin schedule = 0 LF + RFI con delta (o precedente R80e.34 #4)")
def be_29(b):
    ev = [f"MS fila {f['fila']} '{f['material'][:40]}': header supuesto sin schedule ni RFI / precedente" for f in b.ms
          if re.search(r"(?i)header", f["material"]) and (f["net"] or 0) > 0 and re.search(r"(?i)assum|supuest", f["fuente"])
          and not re.search(r"(?i)RFI-?\d|R80e\.34|schedule", f["fuente"])]
    return R("FAIL", *ev) if ev else R("PASS", "headers con schedule, RFI o precedente")


# ---------------------------------------------------------------------------------------------- B / C. Excel y textos
def _celdas_rx(b, rx, hojas=None):
    return [f"{h}!{c}: '{rx.search(t).group(0)}' en '{t[:80]}'" for h, c, t in b.celdas if (hojas is None or h in hojas) and rx.search(t)]


@chk("BE-41", desc="BE-41: ningún nombre de archivo interno (.json / .py / carpetas de trabajo) en las hojas visibles del Excel")
def be_41(b):
    ev = _celdas_rx(b, RX_INTERNO)
    return R("FAIL", *ev[:15]) if ev else R("PASS", "sin nombres internos en el Excel")


@chk("BE-45", desc="BE-45: proporciones en rango (board del Material Summary vs Σ Board SF del Partition Takeoff) o explicadas")
def be_45(b):
    pt = sum(f["board"] or 0 for f in b.pt if f.get("wall"))
    ms = sum(f["net"] or 0 for f in b.ms if re.search(r"(?i)gyp|gypsum|board", f["material"]) and f["unit"].upper().startswith("SF")
             and not re.search(r"(?i)cement|plywood|demo|ceiling|FRP", f["material"]))
    if pt <= 0 or ms <= 0:
        return NA("sin board en el Partition Takeoff o en el Material Summary")
    r = ms / pt
    if 0.6 <= r <= 1.6 or re.search(r"(?i)ratio|proporci", b.excel_txt(("Material Summary", "Review Items"))):
        return R("PASS", f"board MS / PT = {r:.2f}")
    return R("FAIL", f"board del Material Summary {ms:.0f} SF vs Partition Takeoff {pt:.0f} SF (x{r:.2f}) sin explicación")


RX_ESP = re.compile(r"(?<![\d/-])(1/4|3/8|1/2|5/8|3/4)\s?\"")
RX_STUD = re.compile(r"(?<![\d/-])(1-5/8|2-1/2|3-1/2|3-5/8|4|6|8|10|12)\s?\"")


@chk("BE-46", desc="BE-46: un espesor y un producto por renglón (no 1/2\" + 5/8\" ni 3-5/8\" + 6\" en el mismo)")
def be_46(b):
    ev = []
    for f in b.ms:
        m = f["material"]
        if not (f["net"] or 0) or RX_FASTENER.search(m):
            continue
        e = set(RX_ESP.findall(m)) if re.search(r"(?i)gyp|board|plywood|sheathing|backer", m) else set()
        s = set(RX_STUD.findall(m)) if re.search(r"(?i)stud|track|runner", m) else set()
        if len(e) > 1 and not re.search(r"(?i)\bx\b|\bwith\b", m):
            ev.append(f"MS fila {f['fila']} '{m[:60]}': {sorted(e)}")
        elif len(s) > 1:
            ev.append(f"MS fila {f['fila']} '{m[:60]}': {sorted(s)}")
    return R("FAIL", *ev) if ev else R("PASS", "un espesor / tamaño por renglón")


@chk("BE-47", desc="BE-47: todo ID ALC- / RFI- citado en textos existe como renglón")
def be_47(b):
    ids = {str(r[0]).strip() for r in b.scope + b.pend if r and str(r[0]).strip()}
    ids |= {str(r.get("id")) for r in list(b.tk.get("rfis") or []) + list(b.canon.get("rfis") or []) if isinstance(r, dict)}
    ids |= {str(k) for k in (b.tk.get("rfi_cierre") or {})}
    if not ids:
        return NA("sin Scope / Pending")
    ev = []
    textos = [(h, c, t) for h, c, t in b.celdas] + [(n, "", t) for n, t in b.docs.items()]
    for h, c, t in textos:
        for x in re.findall(r"\b(ALC-[A-Z]?\d+|RFI-\d+)\b", t):
            if x not in ids and not any(i.startswith(x + " ") or i == x for i in ids):
                ev.append(f"{h}{'!' + c if c else ''}: cita {x}, que no existe en Scope / Pending")
    return R("FAIL", *sorted(set(ev))[:15]) if ev else R("PASS", "IDs citados existen")


@chk("BE-48", desc="BE-48: ningún nombre de archivo interno en el PDF de markups (Contents / Subject / texto agregado)")
def be_48(b):
    if b.annots is None:
        return SIN("PDF de markups")
    ev = [f"{a['label']}: '{(a['contents'] + ' ' + a['subject'])[:80]}'" for a in b.annots if RX_INTERNO.search(a["contents"] + " " + a["subject"])]
    ev += [f"{k}: texto de página con nombre interno" for k, t in b.pag_texto.items() if RX_INTERNO.search(t)]
    return R("FAIL", *ev[:15]) if ev else R("PASS", "markups sin nombres internos")


def _escala_hoja(b, sh):
    k = b.canon.get("constants") or {}
    v = (k.get("plan_scale_by_sheet") or {}).get(sh) or k.get("plan_scale_pt_per_ft")
    v = v.get("value") if isinstance(v, dict) else v
    return _n(v)


@chk("BE-49", desc="BE-49: la cota impresa usada pertenece al elemento: LF = cota y el dibujo (band / escala) confirma (± 10 %)")
def be_49(b):
    ev, n = [], 0
    for w in b.walls():
        imp = _cota_impresa(w.get("length_source"))
        bd = w.get("band") or {}
        sc = _escala_hoja(b, bd.get("sheet") or w.get("sheet"))
        if imp is None or not sc or bd.get("ori") not in ("H", "V") or _n(bd.get("hi")) is None or _n(bd.get("lo")) is None:
            continue
        n += 1
        dib = (float(bd["hi"]) - float(bd["lo"])) / sc
        if imp > 3 and abs(dib - imp) / imp > 0.10 and not RX_JUSTIFICA.search(str(w.get("length_source"))):
            ev.append(f"{w.get('id')}: cota {imp:.2f} ft y el dibujo mide {dib:.2f} ft: la cota es de otro elemento")
    if not n:
        return NA("sin walls con cota impresa y band")
    return R("FAIL", *ev[:15]) if ev else R("PASS", f"{n} cotas confirmadas por el dibujo")


@chk("BE-50", desc="BE-50: lo que una hoja / spec E / M / P asigna a otro contratista dentro de nuestro alcance tiene RFI o nota")
def be_50(b):
    if b.hojas is None:
        return SIN("set_texto.json")
    # R80e.145: palabra completa; 'wire' solo como hanger / tie wire (un 'FAN SHALL BE WIRED BY THE ELECTRICAL CONTRACTOR' es
    # cableado eléctrico, no alcance de framing / drywall)
    rx = re.compile(r"(?i)\b(supports?|blocking|backing|(?:hanger|tie) wire|framing|hangers?)\b[^.\n]{0,60}by (the )?(E\.?C\.?|electrical contractor|"
                    r"mechanical contractor|M\.?C\.?|others)")
    hs = _hojas_con(b, rx, r"^(E|M|P|FP|EP)-?\d")
    if not hs:
        return NA("sin asignaciones a otro contratista en E/M/P")
    t = b.excel_txt(("Pending Items", "Scope Checklist", "Review Items"))
    falta = [h for h in hs if h not in t and not re.search(r"(?i)by (the )?(E\.?C|others|electrical|mechanical)", t)]
    return R("FAIL", f"traslape con otro contratista en {falta[:5]} sin RFI / nota") if falta else R("PASS", f"traslapes {hs[:3]} con nota")


@chk("BE-51", desc="BE-51: renglón en LF con venta por pieza = piezas por stock length (no ROUNDUP del LF)")
def be_51(b):
    ev = []
    for f in b.ms:
        if f["unit"].upper() != "LF" or not re.search(r"(?i)piece|\bpcs?\b|each", f["selling"]):
            continue
        p = str(f["pieces"] or "")
        if re.fullmatch(r"=ROUNDUP\(\s*[CF]\d+\s*,\s*0\s*\)", p.replace(" ", "")) or \
                (_n(p) is not None and f["net"] and abs(_n(p) - math.ceil(f["net"])) < 0.5 and f["net"] > 12):
            ev.append(f"MS fila {f['fila']} '{f['material'][:50]}': Pieces to buy = ROUNDUP(LF) con venta por pieza")
    return R("FAIL", *ev) if ev else R("PASS", "piezas por stock length")


@chk("BE-52", desc="BE-52: todo 'covered by / included in row N' apunta a un renglón que existe y tiene cantidad")
def be_52(b):
    filas = {f["fila"]: f for f in b.ms}
    ev, n = [], 0
    for h, c, t in b.celdas:
        for m in re.finditer(r"(?i)(?:covered by|included in|see|inside|within)\s+(?:Material Summary\s*!?\s*)?(?:row|R)\s?(\d{1,3})\b", t):
            n += 1
            r = filas.get(int(m.group(1)))
            if not r or not (r["net"] or 0):
                ev.append(f"{h}!{c}: '{m.group(0)}' y la fila {m.group(1)} " + ("no existe" if not r else "está en 0"))
    if not n:
        return NA("sin coberturas heredadas")
    return R("FAIL", *ev) if ev else R("PASS", f"{n} coberturas apuntan a renglones con cantidad")


@chk("BE-53", desc="BE-53: el delta de un RFI incluye cada pieza impresa que su propia pregunta cita del detalle")
def be_53(b):
    ev = []
    for r in b.rfis_abiertos():
        q, d = str(r[1]) if len(r) > 1 else "", " ".join(map(str, r[2:]))
        for m in re.finditer(r"[\"']([^\"']{6,120})[\"']", q):
            for pz in re.findall(r"(?i)\b(screws?|clips?|track|studs?|angles?|straps?|anchors?|runners?|plates?)\b", m.group(1)):
                if not re.search(r"(?i)" + pz.rstrip("s") + r"|fasten|EXCLUDED", d):
                    ev.append(f"{r[0]}: la pregunta cita '{pz}' impreso y el delta no lo incluye")
                    break
    return R("FAIL", *ev) if ev else R("PASS", "deltas con las piezas citadas")


@chk("BE-54", desc="BE-54: la partición por producto aplica cada deducción a sus caras, no al total")
def be_54(b):
    ev = [f"MS fila {f['fila']} '{f['material'][:50]}': deducción aplicada al total" for f in b.ms
          if re.search(r"(?i)total[^|]{0,40}(minus|less|- deduct|deduct)|(minus|less)[^|]{0,20}from (the )?total", f["fuente"])]
    return R("FAIL", *ev) if ev else R("PASS", "deducciones por cara")


@chk("BE-55", desc="BE-55: ningún código interno del plan check (C7-0x, C-0x, N-0x, 'rev7 plan check') en textos al cliente")
def be_55(b):
    ids = {str(w.get("id")) for w in b.walls()} | {str(f.get("wall")) for f in b.pt}
    ev = [f"{h}!{c}: '{RX_PLAN_CHECK.search(t).group(0)}' en '{t[:80]}'" for h, c, t in b.celdas
          if h != "Partition Takeoff" and RX_PLAN_CHECK.search(t) and RX_PLAN_CHECK.search(t).group(0) not in ids] + [f"{n}: '{RX_PLAN_CHECK.search(t).group(0)}'" for n, t in b.docs.items()
                                          if n.startswith("README") and RX_PLAN_CHECK.search(t)]
    return R("FAIL", *ev[:15]) if ev else R("PASS", "sin códigos internos")


@chk("BE-57", desc="BE-57: madera / board / plywood / cement board / FRP con el waste NO metal de Inputs")
def be_57(b):
    met = [i for i, p, v, n in b.inputs if re.search(r"(?i)waste", p) and re.search(r"(?i)metal", p) and not re.search(r"(?i)not metal|non[- ]metal", p)]
    if not met:
        return NA("Inputs sin fila de waste de metal")
    ref = re.compile(r"\$?B\$?" + str(met[0]) + r"\b")
    ev = [f"MS fila {f['fila']} '{f['material'][:50]}': waste {f['waste']} = el de METAL" for f in b.ms
          if re.search(r"(?i)wood|\b2x|plywood|gyp|gypsum|board|cement|FRP|OSB", f["material"])
          and not re.search(r"(?i)stud|track|channel|angle|clip|metal|bead|trim|furring|joint|reveal|J[- ]?mold", f["material"]) and ref.search(f["waste"])]
    return R("FAIL", *ev) if ev else R("PASS", "waste no metal en no metálicos")


# ---------------------------------------------------------------------------------------------- D. corrida (runner / cadena)
@chk("BE-58", desc="BE-58: el Excel lo generó la cadena (canon.py + reglas.py + plantilla_excel.py) — bitácora o sello del Excel")
def be_58(b):
    if b.sello:
        return R("PASS", "Excel con sello de la cadena (<excel>.sello.json)")
    if b.bitacora:
        pasos = " ".join(json.dumps(x) for x in b.bitacora)
        falta = [p for p in ("canon", "reglas", "plantilla") if p not in pasos]
        if falta:
            return R("FAIL", f"la bitácora no registra {falta}: materiales fuera de los programas")
        if re.search(r"(?i)stub|skip(ped)? reglas|reglas[^\"]{0,20}off", pasos):
            return R("FAIL", "reglas.py apagado / stub en la bitácora")
        return R("PASS", "bitácora con canon + reglas + plantilla")
    return R("AMBER", "sin sello ni bitácora: no se puede probar que los números salen de los programas")


@chk("BE-60", desc="BE-60: canon A / B / AB dentro del esquema (validar_canon: escala, band.sheet; sin claves inventadas)")
def be_60(b):
    cs = [(k, c) for k, c in (("A", b.canon_a), ("B", b.canon_b)) if c]
    if not cs:
        return NA("sin lecturas A / B guardadas")
    ref = set(b.canon) | set((b.canon_ab or {}))
    ev = []
    for k, c in cs:
        raras = [x for x in c if re.search(r"[A-Z]{2}\d|\.", x) and x not in ref]
        if raras:
            ev.append(f"lectura {k}: claves fuera del esquema {raras[:6]}")
        if not (c.get("constants") or {}).get("plan_scale_pt_per_ft"):
            ev.append(f"lectura {k}: sin constants.plan_scale_pt_per_ft")
    return R("FAIL", *ev) if ev else R("PASS", "A y B dentro del esquema")


@chk("BE-61", desc="BE-61: la resolución parte de la lectura más completa (AB no tiene menos walls que la más completa sin motivo)")
def be_61(b):
    if not (b.canon_a and b.canon_b and b.canon_ab):
        return NA("sin A / B / AB guardados")
    na, nb, nab = len(b.walls(b.canon_a)), len(b.walls(b.canon_b)), len(b.walls_todos(b.canon_ab))  # BE-CR10
    exc = len(b.canon_ab.get("excluded_walls") or b.canon_ab.get("walls_excluded") or [])
    if nab + exc < max(na, nb) * 0.95:
        return R("FAIL", f"AB {nab} walls (+{exc} excluidos) < lectura más completa {max(na, nb)}")
    return R("PASS", f"AB {nab} walls vs A {na} / B {nb}")


@chk("BE-62", desc="BE-62: element / type normalizados (un BOX o tag de columna es column_wrap, no wall) y >= 80 % emparejado")
def be_62(b):
    ev = [f"{w.get('id')}: band BOX con element wall (es column_wrap)" for w in b.walls()
          if (w.get("band") or {}).get("ori") == "BOX" and str(w.get("element") or "wall") == "wall"]
    if b.canon_a and b.canon_b:
        import reconcile
        m = reconcile.emparejar(b.canon_b, b.canon_a)
        n = max(1, min(len(b.walls(b.canon_a)), len(b.walls(b.canon_b))))
        if len(m) / n < 0.8:
            ev.append(f"reconciliación A/B: {len(m)} de {n} walls emparejados (< 80 %)")
    return R("FAIL", *ev[:15]) if ev else R("PASS", "elements normalizados")


@chk("BE-63", desc="BE-63: el overlay no mete largos / bands de otra referencia: todo wall del AB conserva el largo de A o de B "
     "(o lo cambia una decisión citada)")
def be_63(b):
    if not (b.canon_a and b.canon_b and b.canon_ab):
        return NA("sin A / B / AB guardados")
    ia = {w.get("id"): w for w in b.walls(b.canon_a)}
    ib = {w.get("id"): w for w in b.walls(b.canon_b)}
    ev = []
    # R80e.145: la resolución dirigida escrita (3_revision/resolucion.md) que lista el wall con su largo resuelto ES la
    # decisión citada (el AB es su salida); sin esa fila, sigue fallando
    res_txt = " ".join(v for k, v in (b.textos or {}).items() if "resoluc" in k.lower())
    for w in b.walls(b.canon_ab):
        xs = [x for x in (ia.get(w.get("id")), ib.get(w.get("id"))) if x]
        if not xs or _n(w.get("length_ft")) is None:
            continue
        if all(abs((_n(x.get("length_ft")) or 0) - _n(w["length_ft"])) > 0.05 for x in xs) and \
                not re.search(r"(?i)estimator|decision|RFI-|R-ALC|resol", str(w.get("length_source"))):
            ids_ = [str(w.get("id"))]
            tg = str(w.get("tag") or "")
            if tg and sum(1 for x in b.walls(b.canon_ab) if str(x.get("tag") or "") == tg) == 1:
                ids_.append(tg)                     # la resolución nombra el type ("S61 length") si es su único wall
            fila = next((m for i_ in ids_ for m in [re.search(r"(?m)^\|[^\n]*\b" + re.escape(i_) + r"\b[^\n]*\b" +
                         re.escape(f"{_n(w['length_ft']):g}") + r"\b", res_txt)] if m), None) if res_txt else None
            if fila:
                continue
            ev.append(f"{w.get('id')}: largo {w['length_ft']} distinto de A y B sin decisión citada")
    return R("FAIL", *ev[:15]) if ev else R("PASS", "walls del AB con largos de la lectura")


@chk("BE-64", desc="BE-64: las lecturas no ven respuestas del proyecto (rev anteriores, RFI respondidos, Excel final)")
def be_64(b):
    cs = [(k, c) for k, c in (("A", b.canon_a), ("B", b.canon_b)) if c]
    if not cs:
        return NA("sin lecturas guardadas")
    rx = re.compile(r"(?i)FINAL_FOR_REVIEW|RESPUESTAS_RFI|takeoff_canon_FINAL|_rev\d+[a-z]?\.(xlsx|json)|rev13")
    ev = [f"lectura {k}: cita '{rx.search(json.dumps(c)).group(0)}' (contaminación)" for k, c in cs if rx.search(json.dumps(c))]
    return R("FAIL", *ev) if ev else R("PASS", "lecturas sin rutas de respuestas")


@chk("BE-66", "BE-75", desc="BE-66 / BE-75: costos.csv registra toda llamada (también las fallidas) y ninguna pasa su tope")
def be_66(b):
    if b.costos is None:
        return NA("corrida por suscripción (sin costos.csv)")
    ev = []
    for r in b.costos:
        u, t = _n(r.get("usd")), _n(r.get("tope"))
        if u is None:
            ev.append(f"fila sin usd: {r}")
        elif t is not None and u > t:
            ev.append(f"{r.get('paso')}: {u} > tope {t}")
    return R("FAIL", *ev[:10]) if ev else R("PASS", f"{len(b.costos)} llamadas registradas")


def integridad(c):
    ids = {w.get("id") for w in muros_canon(c or {})}
    ev = []
    for n in (c or {}).get("nodes") or []:
        if isinstance(n, dict):
            for x in n.get("walls") or []:   # nodo: sus walls (no el canon)
                if x not in ids:
                    ev.append(f"node {n.get('id')}: wall {x} no existe")
    for w in muros_canon(c or {}):
        for o in (w.get("openings") or []) if isinstance(w, dict) else []:
            if isinstance(o, dict) and o.get("wall") and o["wall"] not in ids:
                ev.append(f"opening {o.get('ref') or o.get('id')}: wall {o['wall']} no existe")
    return ev


@chk("BE-67", "BE-74", "BE-96", desc="BE-67 / BE-74 / BE-96: referencias del canon íntegras (nodes y openings apuntan a walls que existen)")
def be_67(b):
    if not b.walls():
        return SIN("canon")
    ev = integridad(b.canon)
    return R("FAIL", *ev[:15]) if ev else R("PASS", "referencias íntegras")


@chk("BE-68", "BE-86", desc="BE-68 / BE-86: cada wall con evidencia por programa: estado #0 en altura / largo y HOJA en length_source")
def be_68(b):
    if not b.walls():
        return SIN("canon")
    ev = []
    for w in b.walls():
        if not RX_ESTADO.search(str(w.get("height_source") or "") + str(w.get("height_status") or "")):
            ev.append(f"{w.get('id')}: height_source sin estado #0 (CONFIRMED / DERIVED / RFI)")
        if w.get("length_ft") and not RX_HOJA_CITA.search(str(w.get("length_source") or "")):
            ev.append(f"{w.get('id')}: length_source sin HOJA")
    return R("FAIL", *ev[:20]) if ev else R("PASS", "evidencia con estado y hoja")


@chk("BE-69", desc="BE-69: el renglón de Type X no suma caras regular / MR (renglón = board + uso)")
def be_69(b):
    ev = [f"MS fila {f['fila']} '{f['material'][:40]}': desglose con board regular / MR" for f in b.ms
          if re.search(r"(?i)type ?x", f["material"]) and re.search(r"(?i)5/8\"? (regular|MR)\b|\bregular board|moisture", f["fuente"])]
    return R("FAIL", *ev) if ev else R("PASS", "Type X sin regular / MR")


@chk("BE-70", desc="BE-70: el RCP imprime cielos / soffits de gypsum -> el canon los trae")
def be_70(b):
    if b.hojas is None:
        return SIN("set_texto.json")
    hs = _hojas_con(b, re.compile(r"(?i)gyp(sum)?\.? ?(bd|board)\.?[^.\n]{0,30}(ceiling|clg|soffit)|(ceiling|soffit)[^.\n]{0,30}gyp(sum)?\.? ?(bd|board)"))
    if not hs:
        return NA("el set no imprime cielos de gypsum")
    if b.ceilings() or _soffits(b) or b.canon.get("ceilings_info"):
        return R("PASS", f"cielos en el canon ({hs[:3]})")
    return R("FAIL", f"cielos / soffits de gypsum impresos en {hs[:4]} y el canon no trae ceilings ni soffits")


@chk("BE-71", desc="BE-71: la resolución y la cobertura quedaron escritas (resolucion.md + matriz de cobertura)")
def be_71(b):
    if not (b.canon_a and b.canon_b):
        return NA("sin lecturas A / B (no hubo resolución)")
    falta = [n for n, rx in (("resolucion.md", r"resolucion"), ("cobertura", r"(?i)cobertura|PASO12")) if not
             [k for k, v in b.textos.items() if re.search(rx, k) and v.strip()]]
    return R("FAIL", f"no quedaron escritos: {falta}") if falta else R("PASS", "resolución y cobertura escritas")


@chk("BE-73", desc="BE-73: toda fila del Partition Takeoff con Wall # tiene su type (un return va en el type de su wall)")
def be_73(b):
    ev = [f"Partition Takeoff fila {f['fila']}: wall {f['wall']} sin type" for f in b.pt
          if f.get("wall") and (f.get("lf") or 0) > 0 and str(f.get("partition") or "").strip() in ("", "None", "TYPE None", "None #")]
    return R("FAIL", *ev) if ev else R("PASS", "filas con type")


@chk("BE-76", desc="BE-76: decisión general por atributo aplicada a TODAS las caras (ninguna cara queda con el board viejo)")
def be_76(b):
    g = b.canon.get("generales") or {}
    nuevo = g.get("board") if isinstance(g, dict) else None
    viejo = g.get("board_reemplaza") if isinstance(g, dict) else None
    if not (nuevo and viejo):
        return NA("ninguna decisión general de board tomada (generales.board vacío)")
    ev = [f"{w.get('id')} cara {f.get('side')}: '{f.get('board')}' (la decisión general lo cambia a '{nuevo}')" for w, f in b.faces()
          if str(f.get("board")) == str(viejo)]
    return R("FAIL", *ev[:15]) if ev else R("PASS", "decisión general aplicada a todas las caras")


@chk("BE-77", desc="BE-77: la comparación A/B detecta diferencias de atributos (board por cara, altura) y las manda a la resolución")
def be_77(b):
    if not (b.canon_a and b.canon_b):
        return NA("sin lecturas A / B")
    ib = {w.get("id"): w for w in b.walls(b.canon_b)}
    t = json.dumps(b.revision or {}) + " ".join(v for k, v in b.textos.items() if re.search(r"revision|resolucion", k))
    ev = []
    for a in b.walls(b.canon_a):
        x = ib.get(a.get("id"))
        if not x:
            continue
        ba = sorted(str(f.get("board")) for f in a.get("faces") or [] if isinstance(f, dict))
        bb = sorted(str(f.get("board")) for f in x.get("faces") or [] if isinstance(f, dict))
        ha, hb = _n(a.get("height_ft")), _n(x.get("height_ft"))
        if (ba != bb or (ha is not None and hb is not None and abs(ha - hb) > 0.1)) and \
                not re.search(r"(?<![\w-])" + re.escape(str(a.get("id"))) + r"(?![\w-])", t):
            ev.append(f"{a.get('id')}: A y B difieren en board / altura y la revisión no lo lista")
    return R("FAIL", *ev[:15]) if ev else R("PASS", "diferencias de atributos listadas")


@chk("BE-78", desc="BE-78: ninguna altura placeholder sin hoja de sección / elevación citada (completitud.alturas_placeholder)")
def be_78(b):
    if not b.walls():
        return SIN("canon")
    ev = [f"{w.get('id')}: altura placeholder / sin hoja ('{str(w.get('height_source'))[:60]}')" for w in b.walls()
          if w.get("height_ft") is not None and (re.search(r"(?i)placeholder", str(w.get("height_source")))
                                                 or not RX_HOJA_CITA.search(str(w.get("height_source") or "")))]
    # U-138 (auditoría 4-nov): también la altura de cada CARA (la que va al board) cita su hoja
    ev += [f"{w.get('id')} cara {f.get('side')}: altura de cara sin hoja ('{str(f.get('height_source'))[:60]}')"
           for w in b.walls() for f in (w.get("faces") or []) if isinstance(f, dict) and f.get("height_ft") is not None
           and f.get("height_source") is not None and not RX_HOJA_CITA.search(str(f.get("height_source") or ""))]
    return R("FAIL", *ev[:20]) if ev else R("PASS", "alturas con hoja impresa")


@chk("BE-79", desc="BE-79: ninguna cara a medias (board sin layers / side / room)")
def be_79(b):
    ev = [f"{w.get('id')}: cara {f} incompleta" for w, f in b.faces()
          if f.get("board") and (f.get("layers") is None or not (f.get("side") or f.get("room")))]
    return R("FAIL", *[e[:150] for e in ev[:15]]) if ev else R("PASS", "caras completas")


@chk("BE-80", desc="BE-80: un 'none' de una lectura contradicho por la otra (column wraps, misc) queda en la comparación")
def be_80(b):
    if not (b.canon_a and b.canon_b):
        return NA("sin lecturas A / B")
    t = json.dumps(b.revision or {}) + " ".join(b.textos.values())
    ev = []
    for x, y, lx in ((b.canon_a, b.canon_b, "A"), (b.canon_b, b.canon_a, "B")):
        if x.get("columns_none_reason") and (any(str(w.get("element")) == "column_wrap" for w in b.walls(y)) or
                                             re.search(r"\bCOL-", json.dumps(y.get("misc_items") or []))):
            if not re.search(r"(?i)column", t):
                ev.append(f"lectura {lx} dice sin columnas y la otra trae column wraps: la comparación no lo lista")
    return R("FAIL", *ev) if ev else R("PASS", "nones contradichos listados")


@chk("BE-81", desc="BE-81: partition_types / schedule con dato obligatorio (fuente) y todo type usado en walls está en el schedule")
def be_81(b):
    ps = b.schedule()
    if not ps:
        return NA("sin partition_schedule en el canon")
    ev = [f"type {p.get('type')}: sin source" for p in ps if not p.get("source")]
    tys = {str(p.get("type")).upper() for p in ps}
    usados = {str(w.get("tag")).upper() for w in b.walls() if str(w.get("element") or "wall") == "wall" and w.get("tag")}
    fuera = [t for t in sorted(usados - tys) if not any(t in x.replace(" ", "").split("/") for x in tys)]
    fam = {re.sub(r"-\d+$", "", t) for t in tys}
    amb = [f"type {t}: la fila de rating no está impresa; la familia {re.sub(r'-[0-9]+$', '', t)} sí (construcción de la familia)" for t in fuera
           if re.sub(r"-\d+$", "", t) in fam]
    ev += [f"type {t} usado en walls y fuera del schedule" for t in fuera if re.sub(r"-\d+$", "", t) not in fam]
    if ev:
        return R("FAIL", *ev[:15])
    return R("AMBER", *amb[:15]) if amb else R("PASS", "schedule completo")


@chk("BE-82", "BE-CH02", desc="BE-82 / BE-CH02: sin doble conteo entre hojas / plantas ampliadas (mismo type, mismo cuarto, mismo tramo)")
def be_82(b):
    ws = [w for w in b.walls() if w.get("faces")]
    ev = []
    for i, x in enumerate(ws):
        for y in ws[i + 1:]:
            if _tipo_de(x) != _tipo_de(y) or not _tipo_de(x):
                continue
            rx = {str(f.get("room")).strip().upper() for f in x.get("faces") or [] if isinstance(f, dict) and f.get("room")}
            ry = {str(f.get("room")).strip().upper() for f in y.get("faces") or [] if isinstance(f, dict) and f.get("room")}
            lx, ly = _n(x.get("length_ft")) or 0, _n(y.get("length_ft")) or 0
            txt = json.dumps(x) + json.dumps(y)
            if x.get("sheet") != y.get("sheet") and rx and rx == ry and min(lx, ly) > 4 and min(lx, ly) / max(lx, ly) > 0.8 and \
                    not re.search(r"(?i)counted once|same wall|not counted|also on|cont\. on|continu", txt):
                ev.append(f"{x.get('id')} ({x.get('sheet')}) y {y.get('id')} ({y.get('sheet')}): mismo type, mismos cuartos, "
                          f"{lx:.1f} / {ly:.1f} ft")
            bx, by = x.get("band") or {}, y.get("band") or {}
            if x.get("sheet") == y.get("sheet") and bx.get("ori") in ("H", "V") and bx.get("ori") == by.get("ori"):
                try:
                    lo, hi = max(bx["lo"], by["lo"]), min(bx["hi"], by["hi"])
                    corto = min(bx["hi"] - bx["lo"], by["hi"] - by["lo"])
                    dc = abs((bx["c0"] + bx["c1"]) / 2 - (by["c0"] + by["c1"]) / 2)
                    if corto > 0 and (hi - lo) / corto > 0.5 and dc < 2:
                        ev.append(f"{x.get('id')} y {y.get('id')}: misma línea en {x.get('sheet')} ({(hi - lo) / corto:.0%} traslape)")
                except (KeyError, TypeError):
                    pass
    return R("FAIL", *ev[:15]) if ev else R("PASS", "sin dobles conteos")


@chk("BE-83", "BE-93", desc="BE-83 / BE-93: ninguna cara (W.R. incluida) sube a deck en un cuarto con cielo sin fuente 'full height / "
     "to deck' (completitud.caras_sobre_ceiling)")
def be_83(b):
    if not b.walls():
        return SIN("canon")
    import completitud
    xs = completitud.caras_sobre_ceiling(b.canon)
    return R("FAIL", *[f"{w} cara {r}: {h} ft con cielo {c} ft" for w, r, h, c in xs[:20]]) if xs else R("PASS", "caras topadas al cielo")


@chk("BE-84", desc="BE-84: con column wraps / soffits / esquinas exteriores hay corner bead (trim) cargado")
def be_84(b):
    n = sum(1 for w in b.walls() if str(w.get("element")) == "column_wrap") + len(_soffits(b))
    if not n:
        return NA("sin column wraps ni soffits")
    if _tiene_fila(b, re.compile(r"(?i)corner bead|corner trim|metal trim|\bbead\b|L-?bead|trim")) or b.canon.get("trim_items"):
        return R("PASS", "trim cargado")
    return R("FAIL", f"{n} column wraps / soffits y 0 corner bead")


@chk("BE-85", desc="BE-85: ningún accesorios_none / *_none_reason contradice un ítem cargado")
def be_85(b):
    an = b.canon.get("accesorios_none")
    nombres = []
    if isinstance(an, dict):
        nombres = list(an.keys())
    elif isinstance(an, list):
        nombres = [str(x.get("item") if isinstance(x, dict) else x) for x in an]
    elif isinstance(an, str):
        nombres = [an]
    ev = []
    for nm in nombres:
        for pal in re.findall(r"(?i)\b(PAFs?|duct sleeves?|clips?|angles?|kickers?|straps?)\b", nm):
            if _tiene_fila(b, re.compile(r"(?i)" + pal.rstrip("sS"))):
                ev.append(f"accesorios_none dice '{pal}' y hay renglón cargado")
    return R("FAIL", *ev) if ev else R("PASS", "nones sin contradicción")


@chk("BE-88", desc="BE-88: Pending Items sin datos fuera de las 3 columnas fijas (las opciones van en 'Delta of each alternative')")
def be_88(b):
    ev = [f"Pending Items {r[0]}: datos en columna {chr(65 + j)}" for r in b.pend for j, x in enumerate(r) if j >= 3 and str(x).strip()]
    return R("FAIL", *ev[:10]) if ev else R("PASS", "Pending Items en 3 columnas")


@chk("BE-89", desc="BE-89: nodes derivados: no más de 60 % 'free' (faltan L / T)")
def be_89(b):
    ns = [n for n in b.canon.get("nodes") or [] if isinstance(n, dict)]
    if len(ns) < 5:
        return NA("sin nodes suficientes")
    fr = sum(1 for n in ns if str(n.get("kind")).lower() == "free") / len(ns)
    # R80f.36: con esquinas.py (geometría de bands) la prueba es directa: toda esquina / T entre dos walls del canon
    # tiene su node L / T / X / abut / split. Los free que quedan son extremos contra construcción existente (TI) o
    # libres, no faltantes. Sin esquinas_out se usa el umbral del 60 %.
    es = (b.esquinas or {}).get("esquinas") if isinstance(b.esquinas, dict) else None
    if es is not None:
        pares = set()
        for n in ns:
            if str(n.get("kind")).lower() == "free":
                continue
            # nodo: sus walls (no el canon)
            ws = n.get("walls") or [x for x in (n.get("branch"), n.get("through"), n.get("wall"), n.get("into")) if x]
            if len(ws) >= 2:
                pares.add(frozenset(map(str, ws[:2])))
        falta = [e.get("walls") for e in es if isinstance(e, dict) and frozenset(map(str, e.get("walls") or [])) not in pares]   # nodo: esquina
        fallas = (b.esquinas or {}).get("fallas") or []
        if falta or fallas:
            return R("FAIL", f"{fr:.0%} free; {len(falta)} esquina(s) de esquinas.py sin node L / T: {falta[:8]}", *fallas[:5])
        return R("PASS", f"{fr:.0%} free; las {len(es)} esquinas / T de esquinas.py tienen su node L / T (los free son extremos "
                         "contra construcción existente o libres)")
    return R("FAIL", f"{fr:.0%} de los nodes son free (faltan L / T)") if fr > 0.6 else R("PASS", f"{fr:.0%} free")


@chk("BE-90", desc="BE-90: con DOOR SCHEDULE en el set, el canon declara openings (jambs, header, cripples)")
def be_90(b):
    if b.hojas is None:
        return SIN("set_texto.json")
    if not _hojas_con(b, re.compile(r"(?i)door schedule")):
        return NA("sin door schedule")
    os_ = b.canon.get("opening_schedule")
    items = (os_.get("items") if isinstance(os_, dict) else os_) or []
    if items or any(w.get("openings") for w in b.walls()):
        return R("PASS", "openings declarados")
    # BE-CR10: proyecto wood-framed (0 walls metálicos, todo board-only): los openings son de madera (Div. 06, EXCLUDED);
    # vale si el canon lo declara en opening_schedule.items_none_reason
    nr = str((os_ or {}).get("items_none_reason") or "") if isinstance(os_, dict) else ""
    # solo-metal: 0 metálicos a propósito (BE-CR10)
    if not (b.canon.get("walls") or []) and b.walls_todos() and re.search(r"(?i)wood", nr):
        return R("PASS", f"0 metal walls; openings en wood framing EXCLUDED: {nr[:120]}")
    return R("FAIL", "el set trae DOOR SCHEDULE y el canon no declara ningún opening")


def env_api(base):
    """BE-91: entorno limpio para `claude -p` del runner: sin ANTHROPIC_BASE_URL / CLAUDE_CODE_* / CLAUDECODE de la sesión."""
    return {k: v for k, v in (base or {}).items() if not (k == "ANTHROPIC_BASE_URL" or k.startswith("CLAUDE_CODE_")
                                                          or k == "CLAUDECODE" or k == "ANTHROPIC_AUTH_TOKEN")}


@chk("BE-91", desc="BE-91: el claude -p del runner no hereda ANTHROPIC_BASE_URL / CLAUDE_CODE_* de la sesión")
def be_91(b):
    if b.env is None:
        return NA("corrida por suscripción (sin claude -p)")
    malas = [k for k in b.env if k == "ANTHROPIC_BASE_URL" or k.startswith("CLAUDE_CODE_") or k == "CLAUDECODE"]
    return R("FAIL", f"entorno heredado: {malas}") if malas else R("PASS", "entorno limpio")


@chk("BE-92", desc="BE-92: ninguna decisión del estimador queda sin objeto (apunta a un ítem que la lectura no trae)")
def be_92(b):
    ds = b.canon.get("decisiones_sin_objeto") or b.tk.get("decisiones_sin_objeto") or []
    return R("FAIL", f"{len(ds)} decisiones sin objeto: {[str(x)[:40] for x in ds[:6]]}") if ds else R("PASS", "decisiones con objeto")


@chk("BE-95", desc="BE-95: figura curva medida por arco (no cuerdas / piezas sueltas)")
def be_95(b):
    ev = [f"{w.get('id')}: wall curvo medido por cuerda" for w in b.walls()
          if re.search(r"(?i)curv|\barc\b|radius", json.dumps(w)) and re.search(r"(?i)\bchord", str(w.get("length_source")))
          and not re.search(r"(?i)arc length|arco", str(w.get("length_source")))]
    return R("FAIL", *ev) if ev else R("PASS", "curvos por arco")


@chk("BE-97", desc="BE-97: dos caras del mismo cuarto con alturas distintas van con su side (no se juntan en un renglón)")
def be_97(b):
    ev = []
    for w in b.walls():
        fs = [f for f in w.get("faces") or [] if isinstance(f, dict)]
        for i, f in enumerate(fs):
            for g in fs[i + 1:]:
                if f.get("room") == g.get("room") and f.get("side") == g.get("side") and f.get("height_ft") != g.get("height_ft"):
                    ev.append(f"{w.get('id')}: dos caras '{f.get('room')}' mismo side con alturas {f.get('height_ft')} / {g.get('height_ft')}")
    return R("FAIL", *ev) if ev else R("PASS", "caras con side")


@chk("BE-98", desc="BE-98: una exclusión general por type (existentes) se aplica: ningún wall de ese type queda con board / framing")
def be_98(b):
    ex = b.canon.get("excluded_types") or b.canon.get("types_excluded") or b.canon.get("types_none_reason") or {}   # BE-CR29
    tys = {str(k).upper() for k in (ex if isinstance(ex, (dict, list)) else [])}
    if not tys:
        return NA("sin exclusión general por type")
    ev = [f"{w.get('id')}: type {w.get('tag')} excluido y sigue en walls[]" for w in b.walls() if str(w.get("tag")).upper() in tys]
    return R("FAIL", *ev[:15]) if ev else R("PASS", "exclusión por type aplicada")


@chk("BE-102", desc="BE-102: el Excel solo cita hojas que existen en el set")
def be_102(b):
    if not b.hojas:
        return SIN("set_texto.json")
    hs = set(b.hojas)
    base = {norm_hoja(h) for h in hs}          # R80f.35: A503.C = A503C, A-101 = A101
    tags = {str(w.get("tag") or "").upper() for w in b.walls()} - {""}
    # R80e.145: 'S21/S24', 'D1/D2', 'E/S21' son listas de types / aberturas / caras, no N/HOJA
    no_hoja = {str(w.get("tag") or "") for w in b.walls()} | {str(w.get("id") or "") for w in b.walls()}
    no_hoja |= {str(x) for x in (b.canon.get("type_order") or b.tk.get("type_order") or [])}
    for w in b.walls():
        for op in w.get("openings") or []:
            no_hoja |= set(re.findall(r"\b[A-Z]{1,2}\d{1,2}\b", str(op.get("ref") or "")))
    no_hoja |= {re.sub(r"^.*?([A-Z]+\d+)$", r"\1", x) for x in list(no_hoja)}
    # v81cf25 (CFA rev5): solo es cita de HOJA un token con la forma de las hojas del set (prefijo + formato del número) o con
    # forma de hoja inequívoca 'X-NNN': 'A2/A3' (dos detalles), 'M2.1/M3.5' (types), '3/CT-73B' (acabado), 'KN3/KN7', 'MB-01' no
    forma = lambda h: (re.match(r"[A-Z]+", h).group(0), re.sub(r"\d", "9", re.sub(r"^[A-Z]+", "", h)))   # noqa: E731
    formas = {forma(h) for h in base if re.match(r"[A-Z]+", h)}
    ev = set()
    for h, c, t in b.celdas:
        if h not in ("Material Summary", "Partition Takeoff", "Scope Checklist", "Pending Items"):
            continue
        for n_, sh in RX_DET.findall(t):
            if (sh in no_hoja or re.sub(r"^\d+", "", sh) in no_hoja or n_ in no_hoja and re.fullmatch(r"[A-Z]{1,2}\d{1,2}", sh)) \
                    or (forma(sh) not in formas and not re.fullmatch(r"[A-Z]{1,2}-\d{3}[A-Z]?", sh)):   # R80e.145 + v81cf25 CFA
                continue
            if RX_KEYNOTE.fullmatch(n_):                # R80f.36: par de keynotes 'A1.11/A1.13', no un detalle N/HOJA
                continue
            if sh.upper() in tags and n_.upper() in tags:   # R80f.36: par de wall types 'A6D / X6D', no un N/HOJA
                continue
            if norm_hoja(sh) not in base:
                ev.add(f"{h}: cita {n_}/{sh}, hoja que no existe en este set")
    return R("FAIL", *sorted(ev)[:15]) if ev else R("PASS", "hojas citadas existen")


@chk("BE-103", desc="BE-103: todo wall con LF tiene geometría (band) para su markup; markups = walls")
def be_103(b):
    if not b.walls():
        return SIN("canon")
    ev = [f"{w.get('id')}: sin band (markup sin geometría)" for w in b.walls() if (w.get("length_ft") or 0) and not w.get("band")]
    return R("FAIL", *ev[:15]) if ev else R("PASS", "walls con geometría")


@chk("BE-104", desc="BE-104: type que imprime dos sistemas (furring + studs) carga los dos")
def be_104(b):
    ev = []
    for p in b.canon.get("partition_schedule") or []:
        if not isinstance(p, dict):
            continue
        s = str(p.get("source") or "") + " " + str(p.get("description") or "")
        if re.search(r"(?i)z[- ]?furr|hat channel|furring channel", s) and re.search(r"(?i)\bstuds?\b", s):
            t = str(p.get("type"))
            fur = [f for f in b.ms if re.search(r"(?i)furr|hat|z[- ]", f["material"]) and (f["net"] or 0) > 0]
            if not fur and not re.search(r"(?i)furr", json.dumps(b.canon.get("misc_items") or [])):
                ev.append(f"type {t}: imprime furring + studs y no hay furring cargado")
    return R("FAIL", *ev) if ev else R("PASS", "sistemas dobles cargados")


@chk("BE-105", desc="BE-105: ningún producto impreso queda solo en RFI con el default de la tool")
def be_105(b):
    ev = [f"{r[0]}: producto impreso con default en RFI" for r in b.rfis_abiertos()
          if re.search(r"(?i)\bprinted\b[^.]{0,80}(titen|screw|clip|track|stud|anchor|deep[- ]leg|angle|strap)", str(r[1]))
          and re.search(r"(?i)default", " ".join(map(str, r)))]
    return R("FAIL", *ev) if ev else R("PASS", "lo impreso cargado")


@chk("BE-106", desc="BE-106: sin 'Estimator criterion / Handoff - Approved' de otro proyecto sin cita")
def be_106(b):
    rx = re.compile(r"(?i)handoff\s*-\s*approved|estimator criterion")
    ev = [f"{h}!{c}: '{t[:80]}'" for h, c, t in b.celdas if rx.search(t) and not re.search(r"R-ALC-\d|R80e\.\d|U-\d{3}", t)]
    return R("FAIL", *ev[:10]) if ev else R("PASS", "sin criterios heredados sin cita")


@chk("BE-107", desc="BE-107: con la orden U-053 el canon declara fasteners_excluded y todo fastener queda en 0")
def be_107(b):
    if not b.walls():
        return SIN("canon")
    fs = _fasteners_cargados(b)
    if fs:
        return R("FAIL", *[f"MS fila {f['fila']} '{f['material'][:40]}' net {f['net']}" for f in fs[:10]])
    if not (b.canon.get("fasteners_excluded") or b.tk.get("fasteners_excluded")) and \
            not re.search(r"(?i)(screw|fastener)[^\n]{0,120}EXCLUDED", b.excel_txt(("Scope Checklist", "Material Summary"))):
        return R("FAIL", "canon sin fasteners_excluded y sin EXCLUDED de tornillería (U-053)")
    return R("PASS", "tornillería EXCLUDED")


RX_DEMO = re.compile(r"(?i)\bdemo(?:lition|lish|lished)?\b|\bremov(?:e|al|ed)\b")
RX_DEMO_DESGLOSE = re.compile(r"(?i)\blayers?\b|\bplies\b|\bper face\b|\bboth faces\b|\b\d\s*faces?\b|\bstuds?\b|\btracks?\b|"
                              r"\bboard\b|\bgyp(?:sum)?\b|\bcomposition\b|\bcapas?\b")


@chk("U-143", desc="U-143 (usuario 5-nov, HFT RFI-02): en demolición solo se marcan los SF de lo que se demuele; los materiales "
     "no importan (van a la basura): renglón de demo en otra unidad que SF, con desglose por capa / cara / material, o un RFI "
     "sobre capas o composición de la demo = FAIL; canon: demo_geom con layers > 1 (LF x H x 2 layers) = FAIL")
def u_143(b):
    """U-143, una sola implementación (O'Reilly v81cf44 + CFA v81cf44_EN_CURSO): Material Summary / Pending Items (texto) y
    canon (misc_items de demo, demo_geom con layers > 1 = LF x H x capas, RFI de capas)."""
    canon = b.canon or {}
    if not b.ms and not b.pend and not canon:
        return SIN("Material Summary / Pending Items / canon")
    ev = []
    for f in b.ms:
        m = str(f.get("material") or "")
        if not RX_DEMO.search(m):
            continue
        if str(f.get("unit") or "").upper() != "SF":
            ev.append(f"MS fila {f['fila']} '{m[:50]}': demolición en {f.get('unit')} (U-143: solo SF)")
        if RX_DEMO_DESGLOSE.search(m):
            ev.append(f"MS fila {f['fila']} '{m[:50]}': demolición desglosada por capa / cara / material (U-143: solo el SF del elemento)")
    for r in b.pend or []:
        t = " ".join(str(x or "") for x in r)
        if RX_DEMO.search(t) and re.search(r"(?i)\blayers?\b|\bplies\b|composition|capas|faces?", t):
            ev.append(f"{r[0]}: RFI sobre capas / composición de la demolición (U-143: la demo es solo SF, sin RFI)")
    for m in list(canon.get("misc_items") or []):
        if not isinstance(m, dict):
            continue
        if not (str(m.get("familia") or "").lower().startswith("demolition") or str(m.get("ref") or "").upper().startswith("DEMO")):
            continue
        if str(m.get("unit") or "SF").upper() != "SF":
            ev.append(f"{m.get('ref')}: demolición en {m.get('unit')} (solo SF)")
        if RX_DEMO_CAPAS.search(str(m.get("op") or "")):
            ev.append(f"{m.get('ref')}: la operación desglosa capas / caras: {str(m.get('op'))[:90]}")
    dm = (b.demo or {}).get("items") if isinstance(b.demo, dict) else (b.demo if isinstance(b.demo, list) else [])
    for d in list(dm or []) + list(canon.get("demo_geom") or []):
        if isinstance(d, dict) and float(d.get("layers") or 1) > 1:
            ev.append(f"{d.get('xid') or d.get('id')}: demo_geom con layers = {d.get('layers')} (SF del elemento, sin capas)")
    for r in list(canon.get("rfis") or []):
        q = str((r or {}).get("question") or "")
        if re.search(r"(?i)demo|demolish|remove existing", q) and RX_RFI_CAPAS.search(q):
            ev.append(f"{r.get('id')}: RFI sobre capas / composición de lo que se demuele (U-143: nunca)")
    ev = list(dict.fromkeys(ev))
    return R("FAIL", *ev[:20]) if ev else R("PASS", "demolición solo en SF del elemento, sin capas ni RFI de composición")


RX_WOOD = re.compile(r"(?i)\bFRT\b|\bwood\b|plywood|\bnailers?\b|lumber|fire[- ]treated|\bOSB\b|\b2X\b(?!\s*\d)")


RX_DEMO_CAPAS = re.compile(r"(?i)\bx\s*\d+\s*(?:layers?|faces?|caras?|capas?)\b|\blayer\(s\)|\bface\(s\)")
RX_RFI_CAPAS = re.compile(r"(?i)layers?|capas?|composition|composición|faces? of|caras?")


@chk("U-139", "R-ALC-01", desc="U-139 (usuario 5-nov, O'Reilly 'B Excluir wood'): wood (FRT 2X blocking, plywood, nailers) "
     "NUNCA se carga aunque una decisión vieja lo haya cargado: toda fila de wood del Material Summary con NET > 0 = FAIL")
def u_139(b):
    if not b.ms:
        return SIN("Material Summary")
    ev = [f"MS fila {f['fila']} '{str(f['material'])[:50]}' net {f['net']}: wood cargado (R-ALC-01 / U-139: va 0 con nota EXCLUDED)"
          for f in b.ms if RX_WOOD.search(str(f.get("material") or "")) and isinstance(f.get("net"), (int, float)) and f["net"] > 1e-9]
    return R("FAIL", *ev[:15]) if ev else R("PASS", "ningún wood con cantidad en el Material Summary")


@chk("BE-112", desc="BE-112: framing colgado de la estructura con deep-leg / slip y control joints a ≤ 30 ft (respuestas O'Reilly)")
def be_112(b):
    ev = []
    for w in b.walls():
        t = str(w.get("top_track") or "") + " " + str(w.get("to_deck_source") or "")
        if re.search(r"(?i)hung|suspended from (the )?structure|hangs? from", t) and not RX_SLIP.search(t):
            ev.append(f"{w.get('id')}: colgado de la estructura con top track estándar (va deep-leg / slip)")
    largos = [w for w in b.walls() if (_n(w.get("length_ft")) or 0) > 30 and w.get("faces")]
    if largos and b.ms and not _tiene_fila(b, re.compile(r"(?i)control joint")) and \
            not re.search(r"(?i)control joint[^\n]{0,120}(NOT APPLICABLE|EXCLUDED|by others)", b.excel_txt(("Scope Checklist",))):
        ev.append(f"{len(largos)} walls > 30 ft y sin control joints (ASTM C840 / R80e.34 #8)")
    return R("FAIL", *ev[:10]) if ev else R("PASS", "deep-leg en colgados y control joints")


@chk("BE-CF02", desc="BE-CF02: types con decimal del schedule (W4.1) tienen walls o razón none; inventario_tags acepta decimales")
def be_cf02(b):
    try:
        import inventario_tags as IT
        rx = getattr(IT, "TYPE_RE", None)
        if rx is not None and not re.search(rx if isinstance(rx, str) else rx.pattern, "W4.1"):
            return R("FAIL", "inventario_tags.TYPE_RE no acepta types con decimal (W4.1)")
    except ImportError:
        pass
    ds = [str(p.get("type")) for p in b.schedule() if "." in str(p.get("type"))]
    if not ds:
        return NA("sin types con decimal")
    usados = {str(w.get("tag")) for w in b.walls()}
    tnr = b.canon.get("types_none_reason") or {}
    def _razon(t):      # BE-CR29: la razón de la familia (C.8) cubre sus filas de rating (C.8-1)
        return t in tnr or re.sub(r"-[0-9A-Z.]+$", "", t) in tnr or any(t.startswith(str(k) + "-") for k in tnr)
    ev = [f"type {t}: sin walls ni razón" for t in ds if t not in usados and not _razon(t)]
    return R("FAIL", *ev) if ev else R("PASS", f"{len(ds)} types con decimal leídos")


@chk("BE-CF03", desc="BE-CF03: caras con 1/2\" gyp regular salen en su propio renglón 1/2\"")
def be_cf03(b):
    fs = [f for w, f in b.faces() if re.search(r"1/2\"?\s*(regular|gyp)", str(f.get("board")))] + \
        [x for x in b.canon.get("existing_walls") or [] if isinstance(x, dict) and re.search(r"1/2\"?\s*regular", json.dumps(x))]
    if not fs:
        return NA("sin board 1/2\" regular")
    if _tiene_fila(b, re.compile(r"1/2\"?[^|]{0,20}(gyp|gypsum|board)")):
        return R("PASS", "renglón 1/2\" gyp")
    return R("FAIL", f"{len(fs)} caras 1/2\" regular y sin renglón 1/2\" gypsum board")


@chk("BE-CF04", desc="BE-CF04: walls de madera = board only con framing EXCLUDED (bloque BOARD ONLY - … WOOD-FRAMED)")
def be_cf04(b):
    crudos = [w for w in (b.canon.get("walls") or []) if isinstance(w, dict)]   # solo-metal: madera en walls[] (los board-only van aparte abajo)
    # v138: madera escrita de cualquier forma ('2 X 6', '2×6', 'DF stud', 'Douglas fir', 'SPF', 'timber', 'wood') en stud_size / gauge /
    # framing (framing solo si el wall no es board-only con la madera EXCLUDED)
    rx = re.compile(r"(?i)\bwood\b|\b2\s*[x×]\s*\d|\bDF[\s-]*(?:L\b[\s-]*)?(?:stud|#\s*\d)|douglas[\s-]+fir|\bSPF\b|\btimber\b")
    def fr(w):
        f = w.get("framing")
        f = f if isinstance(f, str) else (json.dumps(f) if f is not None else "")
        return "" if (w.get("board_only") or re.search(r"(?i)exclu", f)) else f
    ws = [w for w in crudos if rx.search(str(w.get("stud_size")) + " " + str(w.get("gauge")) + " " + fr(w))]
    if ws:
        return R("FAIL", *[f"{w.get('id')}: wall de madera con framing en walls[] (va board-only)" for w in ws[:10]])
    # BE-CR29: los walls de madera board-only (existing_walls de un set wood-framed) se cuentan: framing EXCLUDED en cada uno
    bo = [w for w in b.walls() if w.get("board_only")]
    if bo:
        malos = [w["id"] for w in bo if not re.search(r"(?i)wood.*exclu|exclu.*wood|R80f\.1|U-139", json.dumps(w.get("framing")) + json.dumps(w.get("location")) +
                                                    " ".join(str(e.get("decision")) for e in b.canon.get("existing_walls") or [] if str(e.get("id", "")).startswith(w["id"])))]
        if malos:
            return R("FAIL", f"{len(malos)} walls board-only sin la decisión 'wood framing EXCLUDED'", *malos[:10])
        return R("PASS", f"{len(bo)} walls de madera board-only con framing EXCLUDED; ningún wall de madera con framing en walls[]")   # v138: sin '0 walls' (U-138)
    wn = str(b.canon.get("wood_walls_none_reason") or "")   # BE-XF04 (Xfinity 10-nov): set metal-framed / existing only, declared with its sheet
    if wn and re.search(r"[A-Z]{1,2}-?\d", wn):
        return R("PASS", f"walls de madera: ninguno en el set ({wn[:160]})")   # BE-GK27: sin '0 walls' (U-138 lo leía como conteo vacío)
    return NA("sin walls de madera en walls[]")


@chk("BE-CF05", desc="BE-CF05: toda hoja del set con número de hoja leído (no 'pN') o marcada vectorizada")
def be_cf05(b):
    if b.hojas is None:
        return SIN("set_texto.json")
    blanco = set((b.set_meta or {}).get("en_blanco") or []) if hasattr(b, "set_meta") else set()
    sin = [h for h in b.hojas if re.fullmatch(r"p\d+", h) and h not in blanco]   # R80e.151: página en blanco no cuenta
    if sin and len(sin) > len(b.hojas) * 0.2:
        return R("FAIL", f"{len(sin)} de {len(b.hojas)} hojas sin número leído ({sin[:6]})")
    return R("PASS", f"{len(b.hojas) - len(sin)} / {len(b.hojas)} hojas con número")


@chk("BE-CF07", desc="BE-CF07: el rótulo del renglón = el tamaño impreso de su fuente (misc_items)")
def be_cf07(b):
    ev = []
    for it in b.canon.get("misc_items") or []:
        if not isinstance(it, dict):
            continue
        fam, src = str(it.get("familia") or ""), str(it.get("source") or "") + " " + str(it.get("label") or "")
        sf, ss = set(RX_STUD.findall(fam)), set(RX_STUD.findall(src))
        if sf and ss and not (sf & ss) and re.search(r"(?i)stud|joist|track", fam):
            ev.append(f"{it.get('ref')}: rótulo {sorted(sf)} y la fuente imprime {sorted(ss)}")
    return R("FAIL", *ev[:10]) if ev else R("PASS", "rótulos = tamaño impreso")


@chk("BE-CF09", "BE-CF12", desc="BE-CF09 / BE-CF12: bracing solo donde un detalle lo dibuja (nunca C.R. por defecto en furring); "
     "markups con Subject = type")
def be_cf09(b):
    ev = []
    for w in b.walls():
        if re.search(r"(?i)furr|hat|z[- ]", str(w.get("stud_size")) + str(w.get("element"))) and (_n(w.get("bracing_rows")) or 0) > 0 \
                and not RX_DET.search(str(w.get("bracing_rows_source") or "")):
            ev.append(f"{w.get('id')}: bracing en furring sin detalle N/HOJA")
    ev += [f"MS fila {f['fila']} '{f['material'][:40]}': bracing sin N/HOJA" for f in b.ms
           if re.search(r"(?i)bracing|C\.?R\.? channel", f["material"]) and (f["net"] or 0) > 0 and not RX_DET.search(f["fuente"])]
    if b.annots:
        ev += [f"{a['label']}: Subject genérico '{a['subject']}'" for a in b.annots
               if re.fullmatch(r"(?i)\s*(wall|board only|board-only|polyline|line|measurement)?\s*", a["subject"] or "")][:5]
    return R("FAIL", *ev[:15]) if ev else R("PASS", "bracing con detalle; Subjects por type")


@chk("BE-CF10", "BE-VS-09", desc="BE-CF10 / BE-VS-09: si el set trae specs, cada renglón con cantidad cita su sección / párrafo de "
     "spec o 'no spec section'")
def be_cf10(b):
    if b.hojas is None:
        return SIN("set_texto.json")
    RX_SEC = r"\b0[59]\s?\d{2}\s?\d{2}\b"
    citadas = sorted(set(re.findall(RX_SEC, b.excel_txt() + "\n".join(b.docs.values()))))
    hay = bool(b.specs) or re.search(r"\b09\s?2[0-9]\s?\d{2}\b|\b05\s?4[0-1]\s?00\b|SECTION 09", b.set_txt())
    if not hay:
        # E3 (auditoría COORDINACIÓN 7-nov): N/A solo si la entrega TAMPOCO cita secciones de spec; si las cita, la compuerta
        # tiene que haberlas leído (entrega.json specs_dir) -> FAIL (PASS en vacío prohibido, U-137)
        if citadas:
            return R("FAIL", f"la entrega cita specs {', '.join(citadas[:6])} pero la compuerta no leyó el Project Manual "
                             "(entrega.json 'specs_dir' con las secciones en .txt)")
        return NA("el set no trae specs del trade y la entrega no cita ninguna sección")
    if b.specs:
        nums = {re.sub(r"\D", "", k)[:6] for k in b.specs}
        falta = [s_ for s_ in citadas if re.sub(r"\D", "", s_)[:6] not in nums]
        if falta:
            return R("FAIL", *[f"sección {s_} citada en la entrega y no está en specs_dir ({len(nums)} secciones leídas)" for s_ in falta[:10]])
    ev = [f"MS fila {f['fila']} '{f['material'][:45]}': sin sección de spec" for f in b.ms if (f["net"] or 0) > 0
          and not re.search(r"\b0[5-9]\s?\d{2}\s?\d{2}\b|(?i:no spec section|spec section|section \d)", f["fuente"])]
    return R("FAIL", *ev[:15]) if ev else R("PASS", f"renglones cruzados con la spec ({len(b.specs or {})} secciones leídas: "
                                              f"{', '.join(sorted(b.specs or {})[:8])})")


@chk("CR-R8-C", desc="CR-R8-C (rev8 CR City Hotel, cielos punto C): todo ceiling con área cargada lleva altura (CLG 0'-0\" en la etiqueta = FAIL)")
def cr_r8_c(b):
    ev = [f"{x.get('room')}: sin altura (etiqueta CLG 0'-0\")" for x in b.canon.get("ceilings") or []
          if float(x.get("area_sf") or 0) > 0 and not float(x.get("height_ft") or 0) and str(x.get("status") or "").upper() != "EXCLUDED"]
    return R("FAIL", *ev) if ev else R("PASS", "todos los ceilings con altura")


@chk("CR-R6-O1", desc="CR-R6-O1 (U-114, auditoría COORDINACIÓN 7-nov): el angle molding / wall angle de un ceiling = perímetro REAL del "
     "polígono del cuarto; '4 x sqrt(área)' (perímetro de cuadrado equivalente) = FAIL")
def cr_r6_o1(b):
    ev = [f"{x.get('ref')}: {str(x.get('op'))[:90]}" for x in (b.canon.get("misc_items") or [])
          if re.search(r"(?i)angle|wall molding", str(x.get("ref", "")) + str(x.get("familia", ""))) and re.search(r"(?i)sqrt|square-equivalent", str(x.get("op", "")))]
    return R("FAIL", f"{len(ev)} renglones con perímetro de cuadrado equivalente", *ev[:12]) if ev else R("PASS", "angle molding = perímetro medido")


@chk("CR-R6-O2", desc="CR-R6-O2 (auditoría COORDINACIÓN 7-nov): un mismo detalle típico (soffit / cove) se carga con el MISMO ancho impreso en "
     "todos los pisos; anchos distintos para el mismo detalle sin 'width_reason' = FAIL")
def cr_r6_o2(b):
    por = {}
    for s_ in b.canon.get("framed_soffits") or []:
        det = re.match(r"\s*(\d+/[A-Z]+\d*\.?\d+)", str(s_.get("detail") or ""))
        f = next((f for f in s_.get("faces") or [] if f.get("side") == "bottom" and f.get("width_ft") is not None), None)
        if det and f and not s_.get("width_reason"):
            por.setdefault(det.group(1), set()).add((round(float(f["width_ft"]), 3), s_.get("floor")))
    ev = [f"{d}: anchos {sorted({w for w, _ in v})} en pisos {sorted({fl for _, fl in v if fl})}" for d, v in por.items() if len({w for w, _ in v}) > 1]
    return R("FAIL", *ev) if ev else R("PASS", f"{len(por)} detalles típicos con un solo ancho")


@chk("CR-R6-E1", desc="CR-R6-E1 (auditoría COORDINACIÓN 7-nov): un ceiling del mismo piso a la altura del underside de la membrana rated "
     "(+-0.1 ft) es la MEMBRANA (ya cargada), no un cielo aparte; sin 'membrane_reason' = FAIL")
def cr_r6_e1(b):
    mem = {}
    for x in b.canon.get("ceilings") or []:
        if re.search(r"(?i)membrane", str(x.get("room", ""))) and _n(x.get("height_ft")):
            mem[str(x.get("room", ""))[:2]] = _n(x.get("height_ft"))
    ev = []
    for x in b.canon.get("misc_items") or []:
        r = str(x.get("ref", ""))
        if not (r.startswith("CLG-") and r.endswith(" board")) or x.get("membrane_reason"):
            continue
        fl = r.split("-")[1] if r.count("-") >= 2 else ""
        m = re.search(r"\[CONFIRMED\] height (\d+\.?\d*)", str(x.get("source", "")))
        if fl in mem and m and abs(float(m.group(1)) - mem[fl]) <= 0.1:
            ev.append(f"{r}: height {m.group(1)} ft = underside of the {fl} rated membrane ({mem[fl]} ft) -> double count")
    return R("FAIL", *ev) if ev else R("PASS", f"{len(mem)} membranas sin cielo duplicado")


@chk("CR-R11-F12", desc="CR-R11-F12 (CR City Hotel rev11): la cara de exterior sheathing de un wall llega al menos a la altura de sus "
     "caras interiores (el sheathing pasa el top plate); sheathing más bajo que una cara interior del mismo wall = la altura de una de "
     "las dos salió de un corte que no pasa por ese cuarto -> FAIL salvo 'height_reason'")
def cr_r11_f12(b):
    grupos = {}
    for w in muros_canon(b.canon):
        base = str(w.get("id", "")).split(" ")[0]
        h = _n(w.get("height_ft"))
        if base and h:
            grupos.setdefault(base, []).append((w, h))
    ev, n = [], 0
    for base, ws in grupos.items():
        ext = [(w, h) for w, h in ws if re.search(r"(?i)sheathing", str(w.get("board", "")))]
        inn = [(w, h) for w, h in ws if not re.search(r"(?i)sheathing", str(w.get("board", "")))]
        for we, he in ext:
            n += 1
            for wi, hi in inn:
                if hi - he > 0.1 and not (we.get("height_reason") or wi.get("height_reason")):
                    ev.append(f"{we['id']}: exterior sheathing {he} ft < interior face {wi['id']} {hi} ft "
                              f"({str(wi.get('height_source') or '')[:90]})")
    return R("FAIL", *ev) if ev else R("PASS", f"{n} caras de sheathing >= sus caras interiores")


RX_DELTA_OP = re.compile(r"(\d+(?:\.\d+)?) x (\d+(?:\.\d+)?) x (\d) faces? x (\d) layers?")


@chk("CR-R12-E1", desc="CR-R12-E1 (CR City Hotel rev12, COORDINACIÓN): todo delta de RFI / DEDUCT ALTERNATE / Review Item se recalcula desde "
     "las filas ACTUALES del canon (mismo ID): DA con 'filas' = suma L x H x caras x capas (+-0.5 %); una operación 'L x H x n faces x n layers' "
     "de una celda que cita un wall usa el L y la H actuales de ese wall; otro número (altura vieja) = FAIL")
def cr_r12_e1(b):
    idx = {str(w.get("id")): w for w in muros_canon(b.canon)}
    ev, n = [], 0
    for d in b.canon.get("deduct_alternates") or []:
        if not d.get("filas"):
            continue
        n += 1
        try:
            tot = sum(float(idx[f["id"]]["length_ft"]) * float(idx[f["id"]]["height_ft"]) * int(f["faces"]) * int(f["layers"]) for f in d["filas"])
        except KeyError as e:
            ev.append(f"{d.get('id')}: fila {e} no existe en el canon")
            continue
        if abs(abs(float(d.get("delta_sf") or 0)) - tot) > 0.005 * max(tot, 1):
            ev.append(f"{d.get('id')}: delta {d.get('delta_sf')} SF vs filas actuales {tot:.2f} SF")
    ids = sorted(idx, key=len, reverse=True)
    for h, coord, t in b.celdas:
        t = str(t)
        ops = list(RX_DELTA_OP.finditer(t))
        if not ops:
            continue
        cit = [i for i in ids if len(i) > 4 and i in t]
        if not cit:
            continue
        for m in ops:
            n += 1
            L, H = float(m.group(1)), float(m.group(2))
            if not any(abs(float(idx[i].get("length_ft") or 0) - L) <= 0.005 * max(L, 1) and
                       abs(float(idx[i].get("height_ft") or 0) - H) <= 0.005 * max(H, 1) for i in cit):
                ev.append(f"{h}!{coord}: '{m.group(0)}' no cuadra con L / H actuales de {', '.join(cit[:3])} "
                          f"({', '.join(str(idx[i].get('length_ft')) + ' x ' + str(idx[i].get('height_ft')) for i in cit[:3])})")
    return R("FAIL", *ev) if ev else R("PASS", f"{n} deltas recalculados desde las filas actuales")


@chk("CR-R13-E1", desc="CR-R13-E1 (CR City Hotel rev13, U-058): una cara de exterior sheathing y una cara interior del MISMO wall con la "
     "misma altura tomada de la MISMA línea (height_source idéntica) = la cara exterior copió la altura del board interior -> FAIL salvo "
     "'height_both_reason' (cota que vale para ambas)")
def cr_r13_e1(b):
    grupos = {}
    for w in muros_canon(b.canon):
        grupos.setdefault(str(w.get("id", "")).split(" ")[0], []).append(w)
    ev, n = [], 0
    for base, ws in grupos.items():
        ext = [w for w in ws if re.search(r"(?i)sheathing", str(w.get("board", "")))]
        inn = [w for w in ws if not re.search(r"(?i)sheathing", str(w.get("board", "")))]
        for e in ext:
            n += 1
            for i in inn:
                if (_n(e.get("height_ft")) is not None and _n(e.get("height_ft")) == _n(i.get("height_ft"))
                        and str(e.get("height_source") or "").strip() and str(e.get("height_source")) == str(i.get("height_source"))
                        and not (e.get("height_both_reason") or i.get("height_both_reason"))):
                    ev.append(f"{e['id']}: exterior sheathing H {e.get('height_ft')} = interior face {i['id']} from the same line "
                              f"({str(e.get('height_source'))[:80]})")
                    break
    return R("FAIL", *ev) if ev else R("PASS", f"{n} caras de sheathing con su propia altura")


@chk("CR-R15-BARRIDO", desc="CR-R15 (CR City Hotel revisión completa rev14 F02, U-137): el barrido de un RFI lista TODA hoja donde aparece "
     "cada término (sheet:term). Antes los hits se ordenaban y se cortaban a 60 / 12: A5.08 '2HR SHAFT CEILING' quedó fuera del corte y el "
     "RFI-13 se dio por 'no impreso'. Un (hoja, término) presente en set_texto y ausente de barrido.encontrado_en = FAIL")
def cr_r15_barrido(b):
    if b.hojas is None:
        return SIN("set_texto.json")
    ev, n = [], 0
    for r in b.canon.get("rfis") or []:
        br = r.get("barrido") or {}
        if not isinstance(br, dict) or not br.get("terminos"):
            continue
        hits = set(br.get("encontrado_en") or [])
        for term in br["terminos"]:
            for h, v in b.hojas.items():
                t = v if isinstance(v, str) else (v.get("texto") or v.get("text") or "")
                if re.search(re.escape(term), str(t), re.I):
                    n += 1
                    if f"{h}:{term}" not in hits:
                        ev.append(f"{r.get('id')}: '{term}' impreso en {h} y ausente del barrido (hits cortados)")
    return R("FAIL", *ev[:25]) if ev else R("PASS", f"{n} (hoja, término) de los barridos de RFI listados completos")


RX_RI_DELTA = re.compile(r"(?i)delta[^0-9|]{0,40}?[-−]\s*([\d,]+(?:\.\d+)?)\s*SF")


@chk("CR-R16-RI", desc="CR-R16-RI (CR City Hotel revisión dirigida de rev15 #4): un Review Item que cita un RFI y da un 'delta -N SF' usa el MISMO "
     "número que ese RFI en Pending Items (rev15: Review Items fila 9 'delta -121.6 SF' del BAR con RFI-22 ya en -125.98)")
def cr_r16_ri(b):
    if not b.celdas:
        return SIN("celdas del Excel")
    pend = {}
    for h, coord, t in b.celdas:
        if str(h).startswith("Pending"):
            for rid in set(re.findall(r"RFI-\d+", str(t))):
                pend[rid] = pend.get(rid, "") + " " + str(t)
    ev, n = [], 0
    for h, coord, t in b.celdas:
        if not str(h).startswith("Review"):
            continue
        rids = set(re.findall(r"RFI-\d+", str(t)))
        for m in RX_RI_DELTA.finditer(str(t)):
            if "[DERIVED" in str(t)[m.end():m.end() + 40]:
                continue   # delta con su operación de filas: lo recalcula CB_CR_R12_E1
            for rid in rids:
                if rid in pend:
                    n += 1
                    v = m.group(1).replace(",", "")
                    nums = {x.replace(",", "") for x in re.findall(r"[\d,]+\.\d+|[\d,]{2,}", pend[rid])}
                    if v not in nums:
                        ev.append(f"{h}!{coord}: delta -{v} SF citando {rid}, que en Pending Items no lleva ese número")
    return R("FAIL", *ev[:20]) if ev else R("PASS", f"{n} deltas de Review Items iguales a su RFI")


@chk("CR-R16-T509", desc="CR-R16-T509 (revisión dirigida de rev15 #5): IBC 2018 Table 509 SÍ tiene la fila 'Electrical installations and "
     "transformers' (remite a NFPA 70 110.26-110.34 / 450.8-450.48); decir que no lista los cuartos eléctricos = FAIL")
def cr_r16_t509(b):
    ev = [f"{h}!{coord}: '{re.search(r'(?i)Table 509[^.;]{0,80}', str(t)).group(0)[:90]}'" for h, coord, t in (b.celdas or [])
          if re.search(r"(?i)Table 509[^.;]{0,60}(do(es)? not list|not listed)[^.;]{0,30}electric|Table 509 \(electrical rooms not listed\)", str(t))]
    return R("FAIL", *ev[:10]) if ev else R("PASS", "Table 509 citada con su fila de electrical installations")


@chk("CR-R16-MADERA", desc="CR-R16-MADERA (revisión dirigida de rev15 #2): un framing metálico (stud / track / cripple) cuya fuente dice que el "
     "detalle dibuja el símbolo de madera = el detalle específico manda (R-ALC-10): madera, Div. 06 EXCLUDED (U-139); cargarlo metálico = FAIL")
def cr_r16_madera(b):
    ev = [f"{m.get('ref')}: {m.get('familia')} con fuente 'wood symbol' -> Div. 06 EXCLUDED" for m in b.canon.get("misc_items") or []
          if re.search(r"(?i)stud|track|cripple|runner", str(m.get("familia"))) and re.search(r"(?i)wood ['\"]?X['\"]? symbol|wood symbol", str(m.get("source")))
          and float(m.get("qty") or 0) > 0]
    return R("FAIL", *ev[:10]) if ev else R("PASS", "sin framing metálico donde el detalle dibuja madera")


@chk("CR-R17-SILENCIO", desc="CR-R17-SILENCIO (CR City Hotel revisión dirigida de rev16 F5, U-116): un renglón cargado como supuesto conservador "
     "('conservative' / U-048 en su fuente) tiene que estar citado por su id en Pending Items, Review Items o Scope Checklist (rev16: CLG-L4-412WS "
     "+34.52 SF sobre el WS-1 sin RFI ni Review ni Scope = elección en silencio)")
def cr_r17_silencio(b):
    if not b.celdas:
        return SIN("celdas del Excel")
    txt = " ".join(str(t) for h, coord, t in b.celdas if re.match(r"(?i)(Pending|Review|Scope)", str(h)))
    ev, n = [], 0
    for m in b.canon.get("misc_items") or []:
        src = str(m.get("source") or "")
        if not re.search(r"(?i)conservative", src) or not re.search(r"U-048", src) or float(m.get("qty") or 0) <= 0:
            continue
        rid = str(m.get("ref")).rsplit(" ", 1)[0]
        n += 1
        if rid not in txt and not any(x in txt for x in re.findall(r"RFI-\d+", src)):
            ev.append(f"{m.get('ref')}: supuesto conservador sin RFI / Review Item / Scope que lo cite (U-116)")
    return R("FAIL", *sorted(set(ev))[:15]) if ev else R("PASS", f"{n} renglones conservadores citados en Pending / Review / Scope")


@chk("U-161", desc="U-161 (usuario 11-nov, CR City Hotel): cuarto eléctrico / IT con un rating en la tabla de código y otro en el code plan = se carga "
     "el MAYOR sin RFI; soffit de gypsum de un detalle de arquitectura dentro de un canopy 'by others' = nuestro, sin RFI. RFI abierto de esos temas = FAIL")
def u_161(b):
    ev = [f"{r[0]}: RFI abierto de rating de cuarto eléctrico / IT o de soffit de canopy (U-161: se carga sin RFI)" for r in b.rfis_abiertos()
          if re.search(r"(?i)ELECTRICAL AND IT ROOMS|ELEC(TRICAL)? ROOM|DATA \d|IT ROOM|CANOPY[^.]{0,80}(BY OTHERS|SOFFIT)", str(r[1]))]
    return R("FAIL", *ev[:10]) if ev else R("PASS", "sin RFI de rating eléctrico / canopy (U-161)")


@chk("U-178", desc="U-178 (usuario 11-nov, Grand Kia RFI-01/05/07/34/35 + Xfinity RFI-06): decisiones = regla, SIN RFI: wall más alto que la "
     "tabla de limiting heights = gauge SFIA conservador; wall sin tag = type del wall que conecta; C.H. distinta entre hojas = la MAYOR; wall "
     "bajo el cielo = C.H. + 6\"; wall inclinado / VARIES = largo inclinado real. RFI abierto de esos temas = FAIL; 'Verificar a mano' = PENDING")
def u_178(b):
    rx = (r"(?i)limiting height[^.]{0,80}(exceed|above|higher|no member)|without (a )?(type )?tag|no type tag|untagged wall|"
          r"ceiling height[^.]{0,60}(differ|conflict|mismatch)|(below|under) the ceiling|sloped wall|inclined wall|\bVARIES\b")
    ev = [f"{r[0]}: RFI abierto de un tema que U-178 resuelve sin RFI" for r in b.rfis_abiertos()
          if re.search(rx, " ".join(map(str, r[1:]))) and not re.search(r"PENDING - user manual verification", " ".join(map(str, r[1:])))]
    return R("FAIL", *ev[:10]) if ev else R("PASS", "sin RFI de los temas que U-178 resuelve por regla")


@chk("U-184-ELEV", desc="U-184 (4) (CR rev19 east eave): una altura tomada de una ELEVACIÓN vale solo si en PLANTA se comprueba que el wall está "
     "en ese plano frontal: wall con height_source / height_op que cita una elevación sin 'height_plan_check' (N/HOJA de planta) = FAIL")
def u_184_elev(b):
    rx = r"(?i)\belev(?:ation)?s?\b|\bEAVE\b"
    todos = b.walls_todos()                                   # post-mortem: walls + existing_walls (CR wood-framed vive en existing_walls)
    ws = [w for w in todos if re.search(rx, " ".join(str(w.get(k) or "") for k in ("height_source", "height_op")))]
    ev = [f"{w.get('id')}: altura de una elevación sin comprobación en planta (height_plan_check con N/HOJA)" for w in ws
          if not re.search(r"\b[A-Z]{1,2}\d{1,2}\.\d{1,2}", str(w.get("height_plan_check") or ""))]
    n = len(todos)
    return R("FAIL", *ev[:15]) if ev else R("PASS", f"{n} walls revisados: alturas tomadas de elevación ({len(ws)}) comprobadas en planta")


@chk("U-184-EXCL", desc="U-184 (4) / U-159: una exclusión de ALCANCE (F&B / tenant / N.I.C. / by others / owner) vale solo para caras NO "
     "rated: su motivo dice 'non-rated' (o que la membrana rated se carga aparte); exclusión de alcance sin revisar el rating = FAIL")
def u_184_excl(b):
    rx_alc = r"(?i)\bF\s*&\s*B\b|\btenant\b|N\.?\s?I\.?\s?C\b|not in contract|by others|\bowner\b"
    rx_ok = r"(?i)non[- ]?rated|not rated|no (fire )?rating|unrated|rated [^.;]{0,60}(carried|included|loaded|quantified)|rating (reviewed|checked)"
    xs = [("excluded_items", x, x.get("reason")) for x in b.canon.get("excluded_items") or []] + \
         [("excluded_walls", x, x.get("reason")) for x in b.canon.get("excluded_walls") or []] + \
         [("ceilings", x, x.get("excluded_reason") or x.get("reason")) for x in b.canon.get("ceilings") or [] if str(x.get("status") or "").upper() == "EXCLUDED"]
    ev = [f"{k} {x.get('id') or x.get('refs') or x.get('room')}: exclusión de alcance sin decir que no es rated (U-159)" for k, x, r in xs
          if re.search(rx_alc, str(r or "")) and not re.search(rx_ok, str(r or ""))]
    return R("FAIL", *ev[:15]) if ev else R("PASS", "exclusiones de alcance con el rating revisado")


@chk("U-174", desc="U-174 (usuario 11-nov, Xfinity Interquest RFI-01 botón 'A: 26\'-0\" (cargado)'): altura de la estructura existente no "
     "impresa en ninguna hoja = se carga la altura del edificio del code analysis (ej. A0.1 'HEIGHT IN STORIES: 1 STORY - 26 FT') SIN RFI, con "
     "N/HOJA y delta por pie. RFI abierto de altura de estructura / deck / B.O. con altura del edificio impresa en el set (o en el propio RFI) = FAIL")
def u_174(b):
    rx_q = r"(?i)(height of (the )?(existing )?(structure|deck|roof)|B\.?O\.? (of )?(structure|deck)|underside of (the )?(roof|structure|deck)|structure height|deck height)"
    rx_h = r"(?i)(BUILDING HEIGHT|HEIGHT IN STORIES|HEIGHT)[^.\n]{0,40}?\d+\s*(FT|FEET|')"
    imp = [h for h, t in (b.hojas or {}).items() if re.search(rx_h, str(t))]
    ev = [f"{r[0]}: RFI abierto de altura de estructura con la altura del edificio impresa ({', '.join(imp[:3]) or 'en el RFI'}) - U-174: se carga sin RFI"
          for r in b.rfis_abiertos() if re.search(rx_q, " ".join(map(str, r[1:]))) and (imp or re.search(rx_h, " ".join(map(str, r[1:]))))]
    return R("FAIL", *ev[:10]) if ev else R("PASS", "sin RFI de altura de estructura con altura del edificio impresa (U-174)")


@chk("U-163", desc="U-163 (usuario 11-nov): en assemblies rated horizontales / de shaft se carga SOLO gypsum board (incl. shaftliner) y metal framing; "
     "fireproofing, plataformas de acero, concreto, madera = EXCLUDED. Un renglón de esas familias cargado en un CLG / shaft ceiling = FAIL")
def u_163(b):
    ev = [f"{m.get('ref')}: '{m.get('familia')}' cargado en un assembly (U-163: solo gypsum + metal)" for m in b.canon.get("misc_items") or []
          if re.match(r"(CLG|SH|MB)", str(m.get("ref"))) and re.search(r"(?i)fire ?proof|spray|steel (support )?platform|concrete|plywood|wood|lumber",
                                                                        str(m.get("familia"))) and float(m.get("qty") or 0) > 0]
    return R("FAIL", *ev[:10]) if ev else R("PASS", "assemblies con solo gypsum board + metal framing (U-163)")


# ---------------------------------------------------------------------------------------------- post-mortem 11-nov (fondo)
def _txt_h(v):
    return v if isinstance(v, str) else str((v or {}).get("texto") or (v or {}).get("text") or "") if isinstance(v, dict) else str(v or "")


def _walls_y_bo(b):
    """walls metálicos + board-only de existing_walls presentados como walls (BE-CR10 / BE-CR25)."""
    return b.walls() + (b._walls_board_only() if b.canon.get("walls") else [])   # solo-metal: sin metálicos b.walls() ya trae los board-only


def _nivel(x, *campos):
    """nivel de un elemento del canon: floor / level ('L2', 'LEVEL 2', 2) o '-L2-' / 'L2 ' en id / ref / room -> int o None."""
    for k in ("floor", "level"):
        v = x.get(k)
        if v not in (None, ""):
            m = re.search(r"(\d+)", str(v))
            if m:
                return int(m.group(1))
    for k in campos or ("id", "ref", "room"):
        m = re.search(r"(?i)(?:^|[\s\-_(])(?:L|LEVEL\s*)(\d{1,2})(?=[\s\-_)]|$)", str(x.get(k) or ""))
        if m:
            return int(m.group(1))
    return None


@chk("BE-CR20", desc="BE-CR20 (CR City Hotel, auditoría U-138, ALTA): un floor/ceiling assembly rated listado por LEVEL N "
     "(rated_floor_assemblies {id, levels, source}) = membrana en el cielo del nivel N-1; nivel N-1 sin renglón de membrana "
     "(ceilings / misc_items con el id del assembly o 'membrane') ni below_none_reason = FAIL")
def be_cr20_membrana(b):
    asms = [a for a in b.canon.get("rated_floor_assemblies") or [] if isinstance(a, dict) and a.get("levels")]
    if not asms:
        return NA("sin floor/ceiling assembly rated listado por nivel (rated_floor_assemblies)")
    filas = [("ceiling", x, " ".join(str(x.get(k) or "") for k in ("room", "ref", "source", "system")) + " " +
              str((x.get("assembly") or {}).get("id") if isinstance(x.get("assembly"), dict) else x.get("assembly") or ""))
             for x in b.ceilings()] + \
            [("misc", x, " ".join(str(x.get(k) or "") for k in ("ref", "familia", "source", "op"))) for x in b.canon.get("misc_items") or []
             if isinstance(x, dict) and float(x.get("qty") or 0) > 0]
    ev, n = [], 0
    for a in asms:
        aid = str(a.get("id") or "").strip()
        nr = a.get("below_none_reason") or {}
        for lv in a.get("levels") or []:
            m = re.search(r"(\d+)", str(lv))
            if not m or int(m.group(1)) < 2:
                continue
            N = int(m.group(1))
            n += 1
            abajo = [t for k, x, t in filas if _nivel(x) == N - 1 and float(x.get("area_sf") or x.get("qty") or 0) > 0
                     and ((aid and re.search(r"(?<![\w.])" + re.escape(aid) + r"(?![\w.])", t)) or re.search(r"(?i)membrane", t))]
            if not abajo and not str((nr.get(str(N - 1)) or nr.get(f"L{N - 1}") or "") if isinstance(nr, dict) else nr).strip():
                ev.append(f"{aid or 'assembly'} LEVEL {N} ({str(a.get('source') or '')[:60]}): el cielo del nivel {N - 1} no tiene "
                          f"renglón de membrana (BE-CR20: la cara inferior del piso {N} es el cielo de {N - 1})")
    return R("FAIL", *ev[:15]) if ev else R("PASS", f"{n} niveles de {len(asms)} floor/ceiling assemblies rated con su membrana en el nivel de abajo")


def _cubre(band, x, y, tol=3.0):
    """(x, y) en pt dentro de la banda del wall (ori H / V) -> coordenada a lo largo del wall, o None."""
    try:
        c0, c1, lo, hi = (float(band[k]) for k in ("c0", "c1", "lo", "hi"))
    except (KeyError, TypeError, ValueError):
        return None
    a, p = (x, y) if band.get("ori") == "H" else (y, x) if band.get("ori") == "V" else (None, None)
    if a is None or not (min(c0, c1) - tol <= p <= max(c0, c1) + tol) or not (min(lo, hi) - tol <= a <= max(lo, hi) + tol):
        return None
    return a


@chk("BE-CR22", desc="BE-CR22 (CR City Hotel, auditoría U-138): un wall cuya banda es SOLO el vano de una puerta del opening_schedule "
     "(misma hoja, >= 80 % del largo dentro del R.O.) = wall fantasma; una puerta dentro del LF de un wall sin citarla (openings[].ref / "
     "door_reason) = FAIL. Head / infill del vano no cuenta")
def be_cr22_vanos(b):
    os_ = b.canon.get("opening_schedule")
    items = (os_.get("items") if isinstance(os_, dict) else os_) or []
    puertas = [i for i in items if isinstance(i, dict) and str(i.get("kind") or "door").lower() == "door"]
    if not puertas:
        return NA("sin puertas en opening_schedule.items")
    ubic = [i for i in puertas if i.get("sheet") and isinstance(i.get("center_pt"), (list, tuple)) and len(i["center_pt"]) == 2]
    if not ubic:
        return SIN(f"posición (sheet + center_pt) de las {len(puertas)} puertas del opening_schedule")
    ws = b.walls()
    if not ws:
        return NA("sin walls")
    esc = _n(((b.canon.get("constants") or {}).get("plan_scale_pt_per_ft") or {}).get("value")) or 0
    ev, n = [], 0
    for w in ws:
        bd = w.get("band") or {}
        if bd.get("ori") not in ("H", "V") or re.search(r"(?i)head|infill|header", f"{w.get('element') or ''} {w.get('id') or ''}"):
            continue
        n += 1
        lo, hi = sorted((float(bd.get("lo") or 0), float(bd.get("hi") or 0)))
        largo = hi - lo
        refs = {str(o.get("ref")) for o in w.get("openings") or [] if isinstance(o, dict)}
        for d in ubic:
            if norm_hoja(d.get("sheet")) != norm_hoja(bd.get("sheet") or w.get("sheet")):
                continue
            a = _cubre(bd, float(d["center_pt"][0]), float(d["center_pt"][1]))
            if a is None:
                continue
            ro = (float(d.get("ro_w_ft") or 0) * esc) if esc else 0.0
            sol = max(0.0, min(hi, a + ro / 2) - max(lo, a - ro / 2))
            if largo > 0 and sol >= 0.8 * largo:
                ev.append(f"{w.get('id')}: la banda ({largo / esc if esc else largo:.2f} {'ft' if esc else 'pt'}) es el vano de la puerta "
                          f"{d.get('ref')} ({bd.get('sheet') or w.get('sheet')}) = wall fantasma")
            elif str(d.get("ref")) not in refs and not str(w.get("door_reason") or "").strip():
                ev.append(f"{w.get('id')}: la puerta {d.get('ref')} cae dentro de su LF y el wall no la cita (openings / door_reason)")
    return R("FAIL", *ev[:20]) if ev else R("PASS", f"{n} walls contra {len(ubic)} puertas ubicadas: ningún wall fantasma ni puerta sin citar")


def _fam_board(t):
    t = str(t or "").lower()
    for k, rx in (("cement board", r"cement"), ("shaftliner", r"shaft ?liner|liner"), ("tile backer", r"dens|tile ?backer"),
                  ("sheathing", r"sheathing"), ("type c", r"type ?c\b"), ("type x", r"type ?x|\bx\b"), ("abuse / impact", r"abuse|impact"),
                  ("moisture res.", r"w\.?r\.?|moisture|mr\b")):
        if re.search(rx, t):
            return k
    return "regular" if t.strip() else ""


@chk("BE-CR27", desc="BE-CR27 (CR City Hotel rev2, auditoría U-138 #2): pisos típicos (mismo patrón de números de cuarto por nivel, o "
     "typical_floors) = misma carga: SF de board por familia con |delta| > 10 % contra la mediana de los típicos sin stack_reasons = FAIL")
def be_cr27_stack(b):
    import statistics
    ws = _walls_y_bo(b)
    sf, cuartos = {}, {}
    for w in ws:
        lv = _nivel(w, "id")
        L = _n(w.get("length_ft")) or 0
        for f in w.get("faces") or []:
            if not isinstance(f, dict):
                continue
            fl = lv if lv is not None else _nivel(f, "room")
            if fl is None:
                continue
            fam = _fam_board(f.get("board"))
            h = _n(f.get("height_ft")) or _n(w.get("height_ft")) or 0
            if fam:
                sf.setdefault(fl, {}).setdefault(fam, 0.0)
                sf[fl][fam] += (_n(f.get("length_ft")) or L) * h * int(f.get("layers") or 1)   # BE-CR0-12
            for m in re.finditer(r"\b(\d)(\d{2})[A-Z]?\b", str(f.get("room") or "")):
                if int(m.group(1)) == fl:
                    cuartos.setdefault(fl, set()).add(m.group(2))
    for z in b.ceilings():
        fl, fam = _nivel(z), _fam_board(z.get("board"))
        if fl is not None and fam and str(z.get("status") or "").upper() != "EXCLUDED":
            sf.setdefault(fl, {}).setdefault("clg " + fam, 0.0)
            sf[fl]["clg " + fam] += float(z.get("area_sf") or 0) * int((z.get("layers") or {}).get("value", 1) if isinstance(z.get("layers"), dict) else z.get("layers") or 1)
    tip = [int(re.search(r"\d+", str(x)).group(0)) for x in b.canon.get("typical_floors") or [] if re.search(r"\d+", str(x))]
    if not tip:
        nv = sorted(k for k, v in cuartos.items() if len(v) >= 3)
        for i in nv:
            par = [j for j in nv if len(cuartos[i] & cuartos[j]) / len(cuartos[i] | cuartos[j]) >= 0.6]
            if len(par) >= 2 and len(par) > len(tip):
                tip = par
    tip = sorted(set(t for t in tip if t in sf))
    if len(tip) < 2:
        return NA(f"sin pisos típicos (mismo patrón de cuartos en 2+ niveles; {len(sf)} niveles con board)")
    razones = b.canon.get("stack_reasons") or {}
    ev, n = [], 0
    for fam in sorted({k for t in tip for k in sf[t]}):
        vals = {t: sf[t].get(fam, 0.0) for t in tip}
        med = statistics.median(vals.values())
        for t, v in vals.items():
            n += 1
            den = med if med > 0 else v
            if den > 0 and abs(v - med) / den > 0.10:
                if not str(razones.get(f"L{t} {fam}") or razones.get(f"L{t}") or razones.get(str(t)) or "").strip():
                    ev.append(f"L{t} {fam}: {v:.1f} SF vs mediana de los típicos {med:.1f} SF ({'+' if v >= med else ''}"
                              f"{(v - med) / med * 100 if med else 100:.0f} %) sin stack_reasons")
    if ev and not b.canon.get("typical_floors"):        # pisos típicos INFERIDOS por el patrón de cuartos: aviso; declarados: FAIL
        return R("AMBER", f"pisos típicos inferidos {tip} (sin typical_floors en el canon): declarar typical_floors o stack_reasons", *ev[:20])
    return R("FAIL", *ev[:20]) if ev else R("PASS", f"{n} (piso, familia) de {len(tip)} pisos típicos dentro de 10 % de la mediana")


RX_EXTERIOR = re.compile(r"(?i)exterior|\bEIFS\b|sheathing|\bglass[- ]?mat sheathing|weather|stucco|\bEXT\b")
RX_TILE_BACKER = re.compile(r"(?i)dens ?shield|tile ?backer|\bC\s?1178\b")


@chk("BE-GK32", desc="BE-GK32 (Grand Kia rev2, auditoría U-181 F1): una cara exterior / EIFS / sheathing cargada con la familia tile "
     "backer (Dens Shield, ASTM C1178) = FAIL: el glass mat sheathing exterior es su propia familia (exterior sheathing)")
def be_gk32_sheathing_exterior(b):
    caras = [(w, f) for w in _walls_y_bo(b) for f in w.get("faces") or [] if isinstance(f, dict)]
    if not caras:
        return NA("sin walls")
    ext, ev = 0, []
    for w, f in caras:
        lugar = " ".join(str(f.get(k) or "") for k in ("side", "room", "location", "board_source", "keynote"))
        if not RX_EXTERIOR.search(lugar):
            continue
        ext += 1
        boards = " ".join(str(x or "") for x in (f.get("boards") or [f.get("board")]))
        if RX_TILE_BACKER.search(boards):
            ev.append(f"{w.get('id')} cara {f.get('side') or ''}: '{lugar.strip()[:60]}' cargada como '{boards[:50]}' (tile backer) "
                      f"- el sheathing exterior no es tile backer (BE-GK32)")
    if not ext:
        return NA(f"sin caras exteriores / EIFS / sheathing ({len(caras)} caras revisadas)")
    return R("FAIL", *ev[:15]) if ev else R("PASS", f"{ext} caras exteriores / EIFS / sheathing de {len(caras)} sin familia tile backer")


RX_TEXTO_VIEJO = re.compile(r"\(open\)|\[scale check\]|\[TBD\]|…\s*$", re.I)
RX_DELTA_VAGO = re.compile(r"[+±]\s*\d+(?:\.\d+)?\s*%|≈")


def _strings(x, ruta=""):
    if isinstance(x, str):
        yield ruta, x
    elif isinstance(x, dict):
        for k, v in x.items():
            yield from _strings(v, f"{ruta}.{k}" if ruta else str(k))
    elif isinstance(x, (list, tuple)):
        for i, v in enumerate(x):
            yield from _strings(v, f"{ruta}[{i}]")


@chk("BE-GK33", "BE-GK33b", desc="BE-GK33 / 33b (Grand Kia rev2, auditoría U-181 F2/F3 y re-verificación): barrido GLOBAL de todo string del "
     "canon (walls, caras, misc, rfis): '(open)' de un RFI cerrado, '[scale check]', '[TBD]' o texto cortado ('…') = FAIL; un RFI cerrado "
     "(status != open) cuyo loaded / opciones conserva '+x %' o '≈' = FAIL")
def be_gk33_textos_viejos(b):
    if not b.canon:
        return NA("sin canon")
    rf = {}
    for r in list(b.tk.get("rfis") or []) + list(b.canon.get("rfis") or []):
        if isinstance(r, dict) and r.get("id"):
            rf[str(r["id"])] = str(r.get("status") or r.get("estado") or "").strip().lower()
    abiertos = {str(r[0]).strip() for r in b.rfis_abiertos()}
    ev, n = [], 0
    for ruta, s in _strings(b.canon):
        n += 1
        for m in RX_TEXTO_VIEJO.finditer(s):
            if m.group(0).lower() == "(open)":
                rid = re.search(r"(RFI-\d+)\W{0,3}$", s[:m.start()])
                if rid and ((rid.group(1) in rf and rf[rid.group(1)] in ("open", "abierto", "")) or rid.group(1) in abiertos):
                    continue                     # RFI de verdad abierto: el estado es vigente
            ev.append(f"{ruta}: '{m.group(0).strip()}' en '{s[max(0, m.start() - 50):m.end()][:90]}'")
    cerr = 0
    for r in list(b.tk.get("rfis") or []) + list(b.canon.get("rfis") or []):
        if not isinstance(r, dict) or str(r.get("status") or r.get("estado") or "open").strip().lower() in ("open", "abierto"):
            continue
        cerr += 1
        for ruta, s in _strings({"loaded": r.get("loaded"), "opciones": r.get("opciones")}):
            m = RX_DELTA_VAGO.search(s)
            if m:
                ev.append(f"{r.get('id')} ({r.get('status') or r.get('estado')}): {ruta} conserva '{m.group(0)}' - al cerrar se reescribe con el delta medido")
    return R("FAIL", *ev[:25]) if ev else R("PASS", f"{n} strings del canon barridos y {cerr} RFI cerrados sin textos viejos ni deltas vagos")


@chk("BE-GK37", desc="BE-GK37 (Grand Kia re-verificación U-181 3/4): un track / runner de misc_items cuya fuente cita un detalle N/HOJA cuya hoja "
     "(set_texto) no tiene TRACK / RUNNER = FAIL (la fila lleva solo lo que su detalle dibuja); una conexión ('clip' / 'angle') citada como "
     "motivo sin renglón con qty > 0, o un renglón clip / angle con qty 0 sin none_reason = FAIL")
def be_gk37_fila_detalle(b):
    mis = [m for m in b.canon.get("misc_items") or [] if isinstance(m, dict)]
    if not mis:
        return NA("sin misc_items")
    if b.hojas is None:
        return SIN("set_texto.json")
    hn = {norm_hoja(h): _txt_h(v) for h, v in b.hojas.items()}
    ev, n = [], 0
    for m in mis:
        fam = f"{m.get('familia') or ''} {m.get('ref') or ''}"
        if not re.search(r"(?i)track|runner", fam) or float(m.get("qty") or 0) <= 0:
            continue
        if re.match(r"(?i)(SOF|CLG)-", str(m.get("ref") or "")) or re.search(r"(?i)ceiling|soffit", str(m.get("familia") or "")):
            continue                                    # cielo / soffit: el framing sale del dibujo del detalle, no de su texto
        src = str(m.get("source") or "")
        citas = [norm_hoja(h) for _, h in RX_DET.findall(src)]
        citas = [h for h in citas if h in hn and hn[h].strip()]
        if not citas:
            continue
        otras = [h for h in hn if re.search(r"(?<![\w.])" + re.escape(h) + r"(?![\w])", src)]   # toda hoja nombrada en la fuente
        if re.search(r"['\"“][^'\"”]{0,80}\b(?:TRACK|RUNNER)\b", src, re.I) or any(
                re.search(r"(?i)\bTRACK|\bRUNNER|\b\d{3,4}T\d{2,3}", hn[h]) for h in otras):
            n += 1
            continue                                    # la fuente cita el texto impreso del track o una hoja que lo dice
        n += 1
        if not any(re.search(r"(?i)\bTRACK|\bRUNNER|\b\d{3,4}T\d{2,3}", hn[h]) for h in citas):
            ev.append(f"{m.get('ref')}: {m.get('familia')} citando {', '.join(sorted(set(citas)))}: la hoja no dibuja TRACK / RUNNER (BE-GK37)")
    con = {k: sum(float(m.get("qty") or 0) for m in mis if re.search(r"(?i)\b" + k + r"s?\b", f"{m.get('familia') or ''} {m.get('ref') or ''}"))
           for k in ("clip", "angle")}
    for m in mis:
        fam = f"{m.get('familia') or ''} {m.get('ref') or ''}"
        motivo = " ".join(str(m.get(k) or "") for k in ("reason", "qty_reason", "removed_reason", "none_reason", "motivo"))
        for k in ("clip", "angle"):
            if re.search(r"(?i)\b" + k + r"s?\b", fam):
                n += 1
                if float(m.get("qty") or 0) <= 0 and not str(m.get("none_reason") or "").strip():
                    ev.append(f"{m.get('ref')}: conexión '{k}' con qty 0 sin none_reason (BE-GK37)")
            elif re.search(r"(?i)\b" + k + r"s?\b", motivo):
                n += 1
                if con[k] <= 0:
                    ev.append(f"{m.get('ref')}: el motivo cita un {k} ('{motivo.strip()[:70]}') y ningún renglón {k} tiene qty > 0 (BE-GK37)")
    if not n:
        return NA(f"sin track / runner con detalle citado ni conexiones clip / angle ({len(mis)} misc_items revisados)")
    return R("FAIL", *ev[:20]) if ev else R("PASS", f"{n} renglones de track / conexión de {len(mis)} misc_items contra su detalle")


RX_ELEC_IT = re.compile(r"(?i)\bELEC(?:TRICAL)?\b|\bIT\b|\bDATA\b|TELECOM|\bIDF\b|\bMDF\b")
RX_RATING_ELEC = re.compile(r"(?i)(?:\b(?:ELECTRICAL|ELEC\.?|IT|DATA|TELECOM)\b[^\n]{0,80}?\b(\d)\s*-?\s*(?:HR|HOUR)S?\b"
                            r"|\b(\d)\s*-?\s*(?:HR|HOUR)S?\b[^\n]{0,40}?\b(?:ELECTRICAL|ELEC\.?|IT ROOMS?|DATA|TELECOM)\b)")


def _rating(x):
    for k in ("rating_hr", "rating"):
        m = re.search(r"(\d+(?:\.\d+)?)", str(x.get(k) or ""))
        if m:
            return float(m.group(1))
    return None


@chk("U-161-VALOR", desc="U-161 (valor cargado; post-mortem 11-nov #8): cuarto ELEC / IT con DOS ratings impresos en set_texto (tabla de código "
     "vs code plan) = se carga el MAYOR; wall / ceiling de ese cuarto con rating_hr menor que el mayor impreso = FAIL")
def u_161_valor(b):
    if b.hojas is None:
        return SIN("set_texto.json")
    imp = sorted({int(g) for t in b.hojas.values() for m in RX_RATING_ELEC.finditer(_txt_h(t)) for g in m.groups() if g})
    els = [(w, f) for w, f in b.faces() if RX_ELEC_IT.search(str(f.get("room") or ""))] + \
          [(z, z) for z in b.ceilings() if RX_ELEC_IT.search(str(z.get("room") or ""))]
    if not els:
        return NA("sin caras / ceilings de cuartos ELEC / IT")
    if len(imp) < 2:
        return R("PASS", f"{len(els)} caras / ceilings ELEC / IT; ratings impresos {imp or 'ninguno'}: sin doble rating (U-161)")
    mx = max(imp)
    ev, n = [], 0
    for w, f in els:
        r = _rating(f) if f is not w and _rating(f) is not None else _rating(w)
        if r is None:
            ps = next((p for p in b.schedule() if str(p.get("type")) == str(w.get("tag") or w.get("type_id") or "")), {})
            r = _rating(ps)
        if r is None:
            continue
        n += 1
        if r < mx:
            ev.append(f"{w.get('id') or w.get('room')} ({f.get('room')}): {r:g} HR cargado; impresos {imp} HR -> el MAYOR ({mx} HR) manda (U-161)")
    if not n:
        return SIN(f"rating cargado (rating_hr) en las {len(els)} caras / ceilings ELEC / IT con ratings impresos {imp}")
    return R("FAIL", *ev[:15]) if ev else R("PASS", f"{n} caras / ceilings ELEC / IT con el rating MAYOR impreso ({mx} HR)")


RX_SIN_ESTRUCTURA = re.compile(r"(?i)(structure|deck|roof)[^.;|]{0,40}not printed|no (printed )?(structure|deck) (height|elevation)|"
                               r"structure height not printed|U-174")
RX_ALTURA_EDIF = re.compile(r"(?i)(?:BUILDING HEIGHT|HEIGHT IN STORIES|HEIGHT)[^.\n]{0,40}?(\d+)\s*(?:FT|FEET|')")


@chk("U-174-VALOR", desc="U-174 (valor cargado; post-mortem 11-nov #8): wall cuya altura dice 'structure height not printed' se carga con la "
     "altura del edificio del code analysis (A0.x 'HEIGHT ... N FT'); otra altura = FAIL")
def u_174_valor(b):
    ws = [w for w in b.walls_todos() if RX_SIN_ESTRUCTURA.search(" ".join(str(w.get(k) or "") for k in ("height_source", "height_op", "height_status")))]
    if not ws:
        return NA(f"ningún wall con altura de estructura no impresa ({len(b.walls_todos())} walls revisados)")
    if b.hojas is None:
        return SIN("set_texto.json")
    alt = sorted({int(m.group(1)) for h, t in b.hojas.items() if re.match(r"(?i)[A-Z]{1,2}-?0", str(h))
                  for m in RX_ALTURA_EDIF.finditer(_txt_h(t))})
    if not alt:
        return SIN(f"altura del edificio impresa (A0.x 'HEIGHT ... N FT') para {len(ws)} walls sin estructura impresa")
    H = max(alt)
    ev = [f"{w.get('id')}: altura {w.get('height_ft')} ft con estructura no impresa; el code analysis imprime {H} FT (U-174)"
          for w in ws if _n(w.get("height_ft")) is None or abs(_n(w.get("height_ft")) - H) > 0.01]
    return R("FAIL", *ev[:15]) if ev else R("PASS", f"{len(ws)} walls sin estructura impresa cargados con la altura del edificio ({H} FT)")


RX_INCLINADO = re.compile(r"(?i)\bVARIES\b|\bslop(?:ed|ing|e)\b|\binclined\b|\braked?\b")
RX_GEOM_INCL = re.compile(r"(?i)sqrt|√|hypot|\^2|²|incline|slope|pitch|\bavg\b|average|\(\s*[\d.]+\s*\+\s*[\d.]+\s*\)\s*/\s*2"
                          r"|/\s*[\d.]+\s*x\s*[\d.(]|interpol")     # interpolación lineal entre aleros (O'Reilly S42)


@chk("U-178-LARGO", desc="U-178 (5) (valor cargado; post-mortem 11-nov #8): wall con 'VARIES' / 'sloped' en su fuente = largo inclinado real: "
     "sin length_op (o height_op para la altura) con la geometría inclinada (sqrt / pendiente / promedio) = FAIL")
def u_178_largo(b):
    ws = b.walls_todos()
    if not ws:
        return NA("sin walls")
    ev, n = [], 0
    for w in ws:
        for src, op in (("length_source", "length_op"), ("source", "length_op"), ("height_source", "height_op")):
            tx = str(w.get(src) or "")
            if src == "source":                         # en la fuente combinada solo cuenta la parte del LARGO (antes de '| height')
                tx = re.split(r"(?i)\|\s*height\b", tx)[0]
            tx = re.sub(r"(?i)\bslope\s+\d[\d\s/\"']*(?:/|:)\s*1'?", " ", tx)       # pendiente de techo impresa (3\"/1'-0\")
            hit = [m for m in RX_INCLINADO.finditer(tx)                 # banco v81cf96: contextos que NO son un largo / alto inclinado
                   if not re.match(r"(?i)\s*(ceiling|roof|soffit|clg|-?\s*see plan|[\d\s/\"']+(max|min)\b)", tx[m.end():m.end() + 16])
                   and not re.search(r"(?i)\b(no|roof|deck)\s*$", tx[max(0, m.start() - 6):m.start()])
                   and not re.search(r"(?i)\b(roof|deck|purlin|eave)\b", tx[max(0, m.start() - 40):m.end() + 40])]   # pendiente de la estructura de arriba
            if hit and re.search(r"(?i)\bhigh (point|side)\b[^|]{0,60}(loaded|conservative)|\bHP\b", tx):
                hit = []                                # estructura inclinada con el punto alto cargado (conservador, con RFI)
            if hit:
                n += 1
                if not (RX_GEOM_INCL.search(str(w.get(op) or "")) or RX_GEOM_INCL.search(tx[hit[0].end():])
                        or str(w.get(op + "_none_reason") or "").strip()):   # op aparte, en la misma fuente o none_reason (v81cf97)
                    ev.append(f"{w.get('id')}: {src} '{hit[0].group(0)}' sin {op} de geometría inclinada (U-178 (5))")
                break
    return R("FAIL", *ev[:15]) if ev else R("PASS", f"{len(ws)} walls revisados; {n} inclinados / VARIES con su operación de geometría")


@chk("BE-CF11", desc="BE-CF11: un detalle 'wood OR metal' se carga con la opción metálica (no RFI)")
def be_cf11(b):
    ev = [f"{r[0]}: RFI de 'wood OR metal' (R-ALC-01: va la metálica)" for r in b.rfis_abiertos()
          if re.search(r"(?i)(wood|2x\d)[^.]{0,30}\bOR\b[^.]{0,30}(metal|stud)|(metal|stud)[^.]{0,30}\bOR\b[^.]{0,30}(wood|2x\d)", str(r[1]))]
    return R("FAIL", *ev) if ev else R("PASS", "sin RFI de opción wood / metal")


@chk("BE-CF13", desc="BE-CF13: markups con Page Label = número de hoja e idioma inglés")
def be_cf13(b):
    if b.annots is None:
        return SIN("PDF de markups")
    ev = sorted({f"página '{a['label']}': Page Label no es número de hoja" for a in b.annots if re.fullmatch(r"p?\d+", a["label"])})
    ev += [f"{a['label']}: texto en español '{RX_ESPANOL.search(a['contents']).group(0)}'" for a in b.annots if RX_ESPANOL.search(a["contents"])][:6]
    return R("FAIL", *ev[:15]) if ev else R("PASS", "markups en inglés con número de hoja")


@chk("BE-CH03", desc="BE-CH03: la escala de cada hoja = la del rótulo SCALE impreso en ESA hoja")
def be_ch03(b):
    if b.hojas is None:
        return SIN("set_texto.json")
    import verificar_markups_excel as VME
    sb = (b.canon.get("constants") or {}).get("plan_scale_by_sheet") or {}
    if not sb:
        return NA("sin escalas por hoja en el canon")
    ev = []
    for h, v in sb.items():
        v = _n(v.get("value") if isinstance(v, dict) else v)
        imp = VME.escalas_impresas((b.hojas.get(h) or "").replace("’", "'").replace("”", '"'))
        if v and imp and not any(abs(v - x) < 0.02 for x in imp):
            ev.append(f"{h}: escala del canon {v} pt/ft y la hoja imprime {imp}")
    return R("FAIL", *ev) if ev else R("PASS", f"{len(sb)} escalas = rótulo impreso")


@chk("BE-HF02", desc="BE-HF02: ningún Review Item con un elemento IMPRESO en cantidad 0 (BE-GK47: el 0 decimal de un entero con '.0' no cuenta)")
def be_hf02(b):
    ev = [f"Review {r[0]}: '{' '.join(map(str, r))[:100]}'" for r in b.review
          if re.search(r"(?i)\bprinted\b|impreso", " ".join(map(str, r))) and
          re.search(r"(?i)\b(qty|quantity)\s*(=|:)?\s*0\b|(?<![\d.,])0(\.0+)?\s*(LF|SF|EA|PCS)\b|carried at 0|loaded 0", " ".join(map(str, r)))]
    return R("FAIL", *ev) if ev else R("PASS", "nada impreso en 0")


@chk("BE-HF03", desc="BE-HF03: el top track de bulkhead / soffit va en estándar o slip, nunca en el renglón de heads")
def be_hf03(b):
    ev = [f"MS fila {f['fila']} '{f['material'][:40]}': top track de bulkhead en heads" for f in b.ms
          if re.search(r"(?i)head", f["material"]) and re.search(r"(?i)track", f["material"]) and re.search(r"(?i)bulkhead|soffit|top track", f["fuente"])]
    return R("FAIL", *ev) if ev else R("PASS", "top track en sus familias")


@chk("BE-HF04", desc="BE-HF04: bracing solo en walls más altos que la altura mínima impresa")
def be_hf04(b):
    ev = []
    for w in b.walls():
        src = str(w.get("bracing_rows_source") or "")
        m = re.search(r"(?i)(?:higher than|taller than|over|>|exceeding)\s*" + RX_FTIN.pattern, src)
        if m and (_n(w.get("bracing_rows")) or 0) > 0:
            g = m.groups()[-4:]
            hmin = float(g[0]) + float(g[1] or 0) / 12
            if (_n(w.get("height_ft")) or 0) <= hmin:
                ev.append(f"{w.get('id')}: {w.get('height_ft')} ft <= {hmin:.2f} ft y lleva bracing")
    return R("FAIL", *ev[:15]) if ev else R("PASS", "bracing según la condición impresa")


@chk("BE-HF05", desc="BE-HF05: una fila por Wall ID (sin 'A-14+A-12') y 0 textos en español en el Excel")
def be_hf05(b):
    ev = [f"Partition Takeoff fila {f['fila']}: filas agrupadas '{f['wall']}'" for f in b.pt if re.search(r"\+", str(f.get("wall") or ""))]
    ev += [f"{h}!{c}: español '{RX_ESPANOL.search(t).group(0)}'" for h, c, t in b.celdas if RX_ESPANOL.search(t)][:10]
    return R("FAIL", *ev[:15]) if ev else R("PASS", "una fila por Wall ID; inglés")


@chk("BE-VS-01", desc="BE-VS-01: todo RFI de altura de estructura barrió las hojas que imprimen B.O. DECK / LOWEST POINT (incl. demo)")
def be_vs_01(b):
    if b.hojas is None:
        return SIN("set_texto.json")
    hs = _hojas_con(b, re.compile(r"(?i)lowest point|B\.?O\.? (?:OF )?DECK|bottom of deck|heights? noted|B\.?O\.? STRUCT"))
    ev = []
    for r in b.rfis_abiertos():
        if not re.search(r"(?i)height|B\.O\.|deck|structure", str(r[1])):
            continue
        rc = b.rfi_canon(r[0])
        bar = rc.get("barrido") if isinstance(rc.get("barrido"), dict) else {}
        lista = bar.get("hojas") or rc.get("fuentes_revisadas") or []
        if lista == "ALL":
            continue
        txt = " ".join(map(str, lista))
        falta = [h for h in hs if h not in txt]
        if falta:
            ev.append(f"{r[0]}: RFI de altura sin barrer {falta[:6]} (imprimen B.O. DECK / LOWEST POINT)")
    return R("FAIL", *ev) if ev else R("PASS", "RFI de altura con barrido completo")


@chk("BE-VS-02", desc="BE-VS-02: spec 'fire resistant board THROUGHOUT' -> cielos de gypsum en Type X")
def be_vs_02(b):
    if b.hojas is None:
        return SIN("set_texto.json")
    if not re.search(r"(?i)(fire[- ]resist\w*|type ['\"]?x['\"]?)[^.\n]{0,60}throughout", b.set_txt()):
        return NA("la spec no pide Type X en todo")
    ev = [f"ceiling {z.get('room')}: '{z.get('board')}'" for z in b.ceilings() if z.get("board") and
          not re.search(r"(?i)type ?x|fire|\bX\b|C\b", str(z.get("board"))) and not RX_WR.search(str(z.get("board")))]
    return R("FAIL", *ev[:15]) if ev else R("PASS", "cielos en Type X")


@chk("BE-VS-04", "BE-VS-05", desc="BE-VS-04 / BE-VS-05: ningún producto en dos renglones (sin doble conteo; Σ renglones = familia)")
def be_vs_04(b):
    vis = {}
    ev = []
    for f in b.ms:
        if not (f["net"] or 0):
            continue
        k = _norm(f["material"])
        if k in vis:
            ev.append(f"MS filas {vis[k]} y {f['fila']}: mismo producto '{f['material'][:50]}'")
        vis[k] = f["fila"]
    br = [f for f in b.ms if re.search(r"(?i)bridging", f["fuente"]) and re.search(r"(?i)C\.?R\.? channel|cold[- ]rolled", f["material"]) and (f["net"] or 0) > 0]
    if len(br) > 1:
        ev.append(f"bridging de C.R. channel en {len(br)} renglones: {[f['fila'] for f in br]}")
    if b.familias:
        fam = b.familias.get("familias") if isinstance(b.familias.get("familias"), dict) else b.familias
        for f in b.ms:
            v = fam.get(f["material"])
            if isinstance(v, (int, float)) and f["net"] is not None and abs(v - f["net"]) > 0.05 and \
                    sum((g["net"] or 0) for g in b.ms if g["material"] == f["material"]) != v:
                ev.append(f"MS fila {f['fila']} '{f['material'][:40]}': {f['net']} != familia {v}")
    return R("FAIL", *ev[:15]) if ev else R("PASS", "sin productos duplicados")


@chk("BE-VS-06", desc="BE-VS-06: el producto del renglón = el impreso en su detalle (backing track / plate no se compra como stud)")
def be_vs_06(b):
    ev = []
    for it in b.canon.get("blocking_items") or []:
        if not isinstance(it, dict):
            continue
        lab = str(it.get("label") or "")
        fam = " ".join(str(it.get(k) or "") for k in ("familia", "product", "material_name"))
        for pal in ("BACKING TRACK", "PLATE", "FOIL", "FLAT STRAP"):
            if pal in lab.upper() and fam.strip() and pal.split()[-1].lower() not in fam.lower():
                ev.append(f"{it.get('ref')}: imprime '{pal}' y se compra como '{fam[:40]}'")
    return R("FAIL", *ev) if ev else R("PASS", "productos impresos")


@chk("BE-VS-07", desc="BE-VS-07: bridging solo donde no hay board en las dos caras (si la nota lo excluye)")
def be_vs_07(b):
    if b.hojas is not None and not re.search(r"(?i)bridging[^.\n]{0,120}(both sides|each side|not required|omit)", b.set_txt()):
        return NA("sin nota de bridging que excluya walls con board en las dos caras")
    ev = [f"{w.get('id')}: bridging con board en las dos caras" for w in b.walls()
          if (_n(w.get("bridging_rows")) or 0) > 0 and len([f for f in w.get("faces") or [] if isinstance(f, dict) and (f.get("layers") or 0)]) >= 2]
    return R("FAIL", *ev[:15]) if ev else R("PASS", "bridging según la nota")


@chk("BE-VS-08", desc="BE-VS-08: demo con altura N/HOJA, cruce demo vs floor plan nuevo y markup DEMO por elemento")
def be_vs_08(b):
    items = (b.demo or {}).get("items") if isinstance(b.demo, dict) else (b.demo if isinstance(b.demo, list) else None)
    items = items or [x for x in b.canon.get("demolition") or [] if isinstance(x, dict)]
    if not items:
        return NA("sin demolición")
    ev = [f"demo {d.get('id') or d.get('ref')}: altura sin N/HOJA" for d in items if isinstance(d, dict)
          and not RX_HOJA_CITA.search(str(d.get("height_source") or d.get("h_source") or ""))]
    if not [k for k in b.textos if "demo_cruce" in k.lower()]:      # v81cf25: DEMO_CRUCE.md (demo_cruce.py)
        ev.append("sin demo_cruce.md (cruce demo vs floor plan nuevo)")
    if b.annots is not None:
        nd = sum(1 for a in b.annots if re.search(r"(?i)demo", a["subject"] + " " + a["contents"]))
        if nd < len(items):
            ev.append(f"{nd} markups DEMO para {len(items)} elementos de demolición")
    return R("FAIL", *ev[:15]) if ev else R("PASS", f"{len(items)} elementos de demo completos")


@chk("BE-VS-10", desc="BE-VS-10: ningún cierre 'not carried … not drawn' (lo no dibujado se busca y se carga, R-ALC-11)")
def be_vs_10(b):
    rx = re.compile(r"(?i)not (carried|loaded|included)[^.\n]{0,80}not (drawn|shown|dibujad)|not (drawn|shown)[^.\n]{0,60}not (carried|loaded)")
    ev = _celdas_rx(b, rx)
    return R("FAIL", *ev[:10]) if ev else R("PASS", "sin cierres por 'no dibujado'")


@chk("BE-VS-13", desc="BE-VS-13: SF de cada markup = Board (SF) de su fila del Excel (no LF x H)")
def be_vs_13(b):
    if b.annots is None:
        return SIN("PDF de markups")
    sf, area = {}, {}
    for f in b.pt:
        if f.get("wall") and f.get("board") is not None and "+" not in str(f["wall"]):   # agrupadas: las caza BE-HF05
            for wid in [str(f["wall"])]:
                sf[wid.strip()] = f["board"]
                if f.get("lf") and f.get("h"):
                    area[wid.strip()] = f["lf"] * f["h"]     # U-010: el markup puede rotular SF = LF x H (Wall Area)
    ev, por_wid = [], {}
    for a in b.annots:
        if str(a.get("subject") or "").strip().upper() == "DEMO" or str(a.get("contents") or "").startswith("DEMO "):
            continue    # v81cf34 (BE-CF22): la DEMO del board existente (DEMO-14 <wall>) es otra cantidad, no el board del wall
        m = re.search(r"(?i)()([\d,]+(?:\.\d+)?)\s*SF board\b", a["contents"]) or \
            re.search(r"(?i)\bSF\s*[:=]?\s*([\d,]+(?:\.\d+)?)()", a["contents"]) or \
            re.search(r"(?i)()([\d,]+(?:\.\d+)?)\s*SF\b", a["contents"])
        wid = next((w for w in sorted(sf, key=len, reverse=True) if re.search(_rx_wid_exacto(w, sf), a["contents"])), None)   # v129
        if m and wid and sf[wid]:
            x_ = por_wid.setdefault(wid, [0.0, a["label"]])
            x_[0] += float((m.group(1) or m.group(2)).replace(",", ""))   # R80f.37: los tramos de un wall (U-120) se suman
    for wid, (v, lab) in por_wid.items():
        ok = [x for x in (sf[wid], area.get(wid)) if x and abs(v - x) <= max(1.0, 0.01 * x)]
        if not ok:
            ev.append(f"markup {wid} ({lab}): {round(v, 2)} SF vs Excel {sf[wid]} SF")
    return R("FAIL", *ev[:15]) if ev else R("PASS", "SF de markups = Excel")


def _rx_wid_exacto(w, ids):
    """v129 (CR, BE-VS-13): el id w en un texto de markup sin que lo siga ' <sufijo de cara>' de otro id más largo ('XW.6.3-L1-01' no toma
    'XW.6.3-L1-01 S ...') ni un sufijo de cara suelto (N / S / E / W / A / B / INT / EXT / IN / OUT)."""
    suf = sorted({k[len(w):].strip() for k in ids if k != w and k.startswith(w) and k[len(w):len(w) + 1] in " _-."}, key=len, reverse=True)
    alt = "|".join(re.escape(x) for x in suf if x)
    cara = r"(?:[NSEW]|[AB]|INT|EXT|IN|OUT|NORTH|SOUTH|EAST|WEST)"
    no_sigue = (r"(?![ _\-.]?(?:" + alt + r")(?![\w-]))" if alt else "") + r"(?!\s+" + cara + r"(?![\w-]))"
    return r"(?<![\w-])" + re.escape(w) + r"(?![\w-])" + no_sigue


@chk("BE-VS-14", desc="BE-VS-14: un RFI abierto no pregunta por una nota que el set imprime textual (se carga)")
def be_vs_14(b):
    if b.hojas is None:
        return SIN("set_texto.json")
    todo = " " + _norm(b.set_txt()) + " "
    ev = []
    for r in b.rfis_abiertos():
        for m in RX_CITA.finditer(str(r[1])):
            q = _norm(m.group(1))
            if len(q.split()) >= 4 and q in todo and not re.search(r"(?i)loaded|carried|cargad", " ".join(map(str, r))):
                ev.append(f"{r[0]}: pregunta por la nota impresa '{m.group(1)[:60]}' sin cargarla")
    return R("FAIL", *ev) if ev else R("PASS", "notas impresas cargadas")


@chk("BE-CF24", desc="BE-CF24 (CFA rev9, #0): la altura escrita en la Source de un renglón board-only ('| height: ... = N ft') es la "
     "altura CARGADA; un texto de altura viejo (otra fuente / otro número) en la Source = FAIL")
def be_cf24(b):
    ev = []
    for e in b.canon.get("existing_walls") or []:
        if not isinstance(e, dict) or " | height: " not in str(e.get("source") or ""):
            continue
        t = str(e["source"]).split(" | height: ", 1)[1].split(" | elev ", 1)[0]
        ns = re.findall(r"=\s*(\d+(?:\.\d+)?)\s*ft\b", t)
        try:
            h = float(e.get("height_ft"))
        except (TypeError, ValueError):
            continue
        if ns and abs(float(ns[-1]) - h) > 0.01:
            ev.append(f"{e.get('id')}: Source dice height = {ns[-1]} ft, cargado {h} ft ('{t[:70]}')")
    return R("FAIL", f"{len(ev)} renglón(es) con altura vieja en la Source", *ev[:20]) if ev else R("PASS", "altura de la Source = altura cargada")


@chk("R-ALC-06", desc="R-ALC-06: todo markup de DEMOLICIÓN (Subject DEMO) va en una hoja de demolition plan (título con DEMOLITION)")
def r_alc_06(b):
    if b.annots is None or b.hojas is None:
        return SIN("PDF de markups / set_texto.json")
    demo = [a for a in b.annots if str(a.get("subject") or "").strip().upper() == "DEMO"]
    if not demo:
        return NA("sin markups de demolición")
    mal = sorted({a["label"] for a in demo if not re.search(r"DEMOLITION", str(b.hojas.get(a["label"]) or ""), re.I)})
    n = {h: sum(1 for a in demo if a["label"] == h) for h in mal}
    return R("FAIL", *[f"{n[h]} markup(s) DEMO en {h}, que no es un demolition plan" for h in mal]) if mal else \
        R("PASS", f"{len(demo)} markups DEMO en demolition plans")


RX_NO_IMPRESO = re.compile(r"(?i)not printed|printed nowhere|not dimensioned|no (?:printed )?dimension|not shown|not found|no se encontr|no impres")


@chk("BE-CF25", desc="BE-CF25 (CFA rev10, usuario 5-nov 'no están impresos, tienes que buscarlo hasta encontrarlo'): un RFI ABIERTO "
     "'not printed' solo vale con la búsqueda completa: barrido.hojas = ALL, >= 12 términos (con sinónimos), los sets de los dos GC "
     "comparados (barrido.sets >= 2 o barrido.un_solo_gc con motivo), la medida vectorial a la escala impresa intentada "
     "(barrido.medida_vectorial) y >= 3 lugares revisados con imagen (barrido.lugares [{sheet, what, img}])")
def be_cf25(b):
    ev = []
    for r in list(b.canon.get("rfis") or []):
        if not isinstance(r, dict) or not str(r.get("status") or "open").lower().startswith("open"):
            continue
        txt = " ".join(str(r.get(k) or "") for k in ("question", "why_not_printed"))
        if not RX_NO_IMPRESO.search(txt):
            continue                       # un conflicto impreso / una pregunta de criterio no es "not printed"
        bz = r.get("barrido") if isinstance(r.get("barrido"), dict) else {}
        falta = []
        if bz.get("hojas") != "ALL":
            falta.append("hojas != ALL")
        ts = bz.get("terminos") or []
        if isinstance(ts, str):
            ts = [x for x in re.split(r"[,;]", ts) if x.strip()]
        if len(ts) < 12:
            falta.append(f"{len(ts)} términos (< 12)")
        if len(bz.get("sets") or []) < 2 and len(str(bz.get("un_solo_gc") or "").strip()) < 8:
            falta.append("sin los sets de los dos GC")
        if len(str(bz.get("medida_vectorial") or "").strip()) < 8:
            falta.append("sin medida vectorial a escala impresa")
        lug = [x for x in bz.get("lugares") or [] if isinstance(x, dict) and x.get("img")]
        if len(lug) < 3:
            falta.append(f"{len(lug)} lugares revisados con imagen (< 3)")
        if falta:
            ev.append(f"{r.get('id')}: 'not printed' sin búsqueda completa: " + ", ".join(falta))
    return R("FAIL", *ev[:20]) if ev else R("PASS", "todo RFI 'not printed' con búsqueda completa")


RX_VALOR_FINAL = re.compile(r"=\s*([\d]+(?:\.\d+)?)\s*(SF|LF)\b")


@chk("BE-CF26", desc="BE-CF26 (CFA rev10): un RFI RESUELTO / CERRADO cuyo valor final está en resolved.answer ('= N SF|LF') debe hablar "
     "desde ese valor: la opción A no puede decir 'M SF loaded' con M != N ni presentar N como alternativa con delta ('N SF ...: -x')")
def be_cf26(b):
    ev = []
    for r in list(b.canon.get("rfis") or []):
        if not isinstance(r, dict) or str(r.get("status") or "open").lower().startswith("open"):
            continue
        res = r.get("resolved") if isinstance(r.get("resolved"), dict) else {}
        m = RX_VALOR_FINAL.findall(str(res.get("answer") or ""))
        if not m:
            continue
        n, u = float(m[-1][0]), m[-1][1]
        a = ((r.get("opciones") or {}).get("A") or {}) if isinstance(r.get("opciones"), dict) else {}
        a = a if isinstance(a, dict) else {}
        txt = " ".join(str(x or "") for x in (a.get("texto"), a.get("delta"), r.get("delta")))
        for v in re.findall(r"([\d]+(?:\.\d+)?)\s*" + u + r"\s+loaded", txt):
            if abs(float(v) - n) > 0.01:
                ev.append(f"{r.get('id')}: resuelto en {n} {u} pero la opción A dice '{v} {u} loaded'")
        for v in re.findall(r"([\d]+(?:\.\d+)?)\s*" + u + r"[^:|;]{0,30}:\s*[-+]", txt):
            if abs(float(v) - n) < 0.01:
                ev.append(f"{r.get('id')}: el valor resuelto {n} {u} aparece como alternativa con delta")
    return R("FAIL", *ev[:20]) if ev else R("PASS", "todo RFI resuelto habla desde el valor cargado")


@chk("BE-VS-15", desc="BE-VS-15: toda hoja con renglones (walls, cielos por rcp_sheet, demo) tiene página de markups")
def be_vs_15(b):
    if b.annots is None:
        return SIN("PDF de markups")
    pags = {a["label"] for a in b.annots}
    hs = {w.get("sheet") for w in b.walls_todos() if w.get("sheet") and (w.get("length_ft") or 0)}  # BE-CR10
    hs |= {z.get("rcp_sheet") for z in b.ceilings() if z.get("rcp_sheet")}
    falta = sorted(h for h in hs if h and h not in pags)
    # U-138 (auditoría 4-nov): con demolición, se cuentan los markups DEMO contra los elementos de demo (no las hojas):
    # cada elemento de demo_geom.json (id / xid) con su markup Subject DEMO (piezas '<xid> k' cuentan)
    dm = (b.demo or {}).get("items") if isinstance(b.demo, dict) else (b.demo if isinstance(b.demo, list) else [])
    dm = [d for d in dm or [] if isinstance(d, dict) and (d.get("xid") or d.get("id"))]
    ev = [f"hojas con renglones sin markups: {falta}"] if falta else []
    if dm:
        txt_demo = [str(a.get("contents") or "") for a in b.annots if str(a.get("subject") or "").upper() == "DEMO"]
        sin = [str(d.get("xid") or d.get("id")) for d in dm
               if not any(re.search(r"(?:^|·\s)" + re.escape(str(d.get("xid") or d.get("id"))) + r"(?:\s\d+)?\s·", t) for t in txt_demo)]
        if sin:
            ev.append(f"{len(sin)} de {len(dm)} elementos de demo sin markup DEMO: {', '.join(sin[:12])}")
    if ev:
        return R("FAIL", *ev)
    return R("PASS", f"{len(hs)} hojas con markups" + (f"; {len(dm)} elementos de demo con su markup DEMO" if dm else ""))


# ============================================================================================== CE_CALLOUTS (U-113 / BE-124)
# Orden del usuario 3-nov: "toda burbuja de detalle / sección (N/HOJA, p. ej. 1/A3.2) de CADA hoja del set se sigue hasta
# el final de su cadena". Generaliza verif_callouts.py (2-oct, D/A9.22 de la marquesina nunca abierto; cierre transitivo
# 7/A09.26) y cadena_detalles.py (la secuencia de detalles queda escrita) al texto completo del set (set_texto.json, incl.
# AutoCAD SHX) — esas dos tools dependían de un PDF / caché del workdir viejo y compuerta_entrega.py nunca las llamaba.
# Defensa de falsos positivos de cadena_detalles._citas: una etiqueta nunca lleva cero a la izquierda ("01/A09.02" es la
# cola de otro número de hoja) y no puede ir pegada a la cola de un número de hoja.
# v81cf35 (BE-CF22, CFA rev7): etiqueta letra+número de la grilla de detalles / interior elevations ("A3/A-601", "C4/A-624",
# "D1-A/A-625"): antes solo "1" o "A" -> el chequeo no veía la cita y daba "sin disposición" a burbujas citadas
CALLOUT = re.compile(r"(?<![\w.\-/])([1-9]\d?|[A-Z](?:\d{1,2}(?:-[A-Z])?)?)\s*/\s*([A-Z]{1,3}-?\d{1,3}(?:\.(?:\d{1,2}|[A-Z]))?[A-Z]?)(?![\w.\-/])")   # R80f.35: 4/A503.C


def norm_hoja(h):
    """A09.22 -> A9.22, A-101 -> A101, A1.10 se queda (se QUITA el cero de la serie, nunca se agrega)."""
    h = str(h or "").strip().upper().replace("-", "").replace(" ", "")
    h = re.sub(r"#\d+$", "", h)
    m = re.match(r"^([A-Z]{1,3})0*(\d+)(\.\d{1,2})?\.?([A-Z]?)$", h)      # R80f.35: A503.C = A503C (punto antes de la letra)
    return f"{m.group(1)}{int(m.group(2))}{m.group(3) or ''}{m.group(4)}" if m else h


def callouts_de(txt):
    return sorted({(n, norm_hoja(h)) for n, h in CALLOUT.findall(txt or "")})


def _hojas_entrada(b):
    """hojas de nuestro trade donde nacen las cadenas: plantas con walls, RCP con cielos, demo, soffits."""
    hs = {w.get("sheet") or (w.get("band") or {}).get("sheet") for w in b.walls()}
    hs |= {z.get("rcp_sheet") or z.get("sheet") for z in b.ceilings()}
    dm = (b.demo or {}).get("items") if isinstance(b.demo, dict) else (b.demo if isinstance(b.demo, list) else [])
    hs |= {d.get("sheet") for d in dm or [] if isinstance(d, dict)}
    hs |= {x.get("sheet") for x in b.canon.get("existing_walls") or [] if isinstance(x, dict)}
    return {norm_hoja(h) for h in hs if h}


def _no_aplica(b, n, h):
    na = b.no_aplican or b.canon.get("callouts_no_aplican") or {}
    if not isinstance(na, dict):
        return None
    for k, v in na.items():
        if isinstance(v, dict) and norm_hoja(k) == h and str(v.get(n) or "").strip():
            return str(v[n])
        if not isinstance(v, dict) and re.fullmatch(r"\s*" + re.escape(n) + r"\s*/\s*(.+)", str(k)) and \
                norm_hoja(str(k).split("/", 1)[1]) == h and str(v).strip():
            return str(v)
    return None


def _burbujas_hoja(b, h):
    """U-137: burbujas de dos líneas de la hoja h (detector + verificadas a ojo) y círculos con divisoria sin leer ni verificar."""
    bub = (b.set_meta or {}).get("burbujas") or {}
    ver = b.verificadas if isinstance(b.verificadas, dict) else {}
    leidas, pend = set(), []
    for k, v in bub.items():
        if norm_hoja(k) != h:
            continue
        vv = [x for kk, xs in ver.items() if norm_hoja(kk) == h for x in (xs or []) if isinstance(x, dict)]
        for x in v.get("burbujas") or []:
            leidas.add((str(x["n"]), norm_hoja(x["hoja"])))
        for x in (v.get("sin_leer") or []) + (v.get("indep_no_detectados") or []):
            m = next((y for y in vv if abs(float(y.get("x", -1e9)) - x["x"]) <= 6 and abs(float(y.get("y", -1e9)) - x["y"]) <= 6), None)
            if m is None:
                pend.append(f"({x['x']:.0f}, {x['y']:.0f})")
            elif m.get("n") and m.get("hoja"):
                leidas.add((str(m["n"]), norm_hoja(m["hoja"])))
            elif len(str(m.get("no_es_burbuja") or "").strip()) < 8:
                pend.append(f"({x['x']:.0f}, {x['y']:.0f}) verificada sin lectura ni motivo 'no_es_burbuja'")
    # BE-CC03 (Consumer Cellular, 5-nov): a bubble found and read BY EYE (burbujas_verificadas.json {x, y, n, hoja, img})
    # that no detector ring saw is a read bubble of that sheet too (before: only eye readings of detector rings counted)
    for kk, xs in ver.items():
        if norm_hoja(kk) == h:
            for y in xs or []:
                if isinstance(y, dict) and y.get("n") and y.get("hoja") and str(y.get("img") or "").strip():
                    leidas.add((str(y["n"]), norm_hoja(y["hoja"])))
    return leidas, pend


def _detalle_verificado(b, n, t):
    """U-137 (O'Reilly rev7, 10/A5.2): el título del detalle no es un círculo (rótulo en rectángulo redondeado) y el OCR de la
    hoja raster no lee su número: verificado a ojo en burbujas_verificadas.json {hoja: [{detalle_existe: N, img}]} con imagen."""
    ver = b.verificadas if isinstance(b.verificadas, dict) else {}
    return any(str(x.get("detalle_existe") or "").strip() == n and str(x.get("img") or "").strip()
               for kk, xs in ver.items() if norm_hoja(kk) == t for x in (xs or []) if isinstance(x, dict))


def _burbujas_pos(b, h):
    """U-141: burbujas de la hoja h CON posición (detector + verificadas a ojo con lectura): [{n, t, x, y, r, como}]."""
    bub = (b.set_meta or {}).get("burbujas") or {}
    ver = b.verificadas if isinstance(b.verificadas, dict) else {}
    out = []
    for k, v in bub.items():
        if norm_hoja(k) != h:
            continue
        for x in v.get("burbujas") or []:
            out.append({"n": str(x["n"]), "t": norm_hoja(x["hoja"]), "x": x["x"], "y": x["y"], "r": x.get("r") or 14,
                        "como": "detector"})
    for kk, xs in ver.items():
        if norm_hoja(kk) != h:
            continue
        for x in xs or []:
            if isinstance(x, dict) and x.get("n") and x.get("hoja") and x.get("x") is not None:
                n_, t_, x_, y_ = str(x["n"]), norm_hoja(x["hoja"]), float(x["x"]), float(x["y"])
                # BE-CC07: the same bubble seen by the detector and read by eye counts once (within 6 pt)
                if any(o["n"] == n_ and o["t"] == t_ and abs(float(o["x"]) - x_) <= 6 and abs(float(o["y"]) - y_) <= 6
                       for o in out):
                    continue
                out.append({"n": n_, "t": t_, "x": x_, "y": y_, "r": float(x.get("r") or 14), "como": "verificada a ojo"})
    return out


def cadena_detalles(b):
    """U-141 (usuario 5-nov): la cadena completa de burbujas revisadas, con posición en la hoja de ORIGEN y su disposición,
    siguiendo la misma regla de CE_CALLOUTS (hojas de entrada -> detalles citados -> sus burbujas -> ...). Las burbujas
    declaradas fuera de alcance se marcan también (se revisaron) pero su cadena no se sigue.
    -> [{n, t, origen, x, y, r, como, disp, motivo}] (orden de recorrido)."""
    if b.hojas is None:
        return []
    txt_h = {}
    for h, t in b.hojas.items():
        txt_h[norm_hoja(h)] = txt_h.get(norm_hoja(h), "") + "\n" + t
    entrada = _hojas_entrada(b) & set(txt_h)
    # CR-R11-H6: 'citada' exige la CELDA del Excel que la cita (hoja!celda); el texto del canon (índices, barridos) ya no cuenta
    citas_en = {}
    for hj_, cc_, t_ in b.celdas:
        for n, h in CALLOUT.findall(str(t_)):
            citas_en.setdefault((n.lstrip('0') or n, norm_hoja(h)), f"{hj_}!{cc_}")
    citas = set(citas_en)   # BE-CR24: '08' = '8'
    out, visitadas, cola = [], set(), sorted(entrada)
    while cola:
        h = cola.pop(0)
        if h in visitadas:
            if not cola:                     # BE-CR18: la última hoja ya visitada no salta el re-sembrado de BE-CC07
                cola = [x for x in hojas_con_burbujas(b) if x not in visitadas]
            continue
        visitadas.add(h)
        for p in sorted(_burbujas_pos(b, h), key=lambda p: (p["y"], p["x"])):
            n, t = p["n"], p["t"]
            m = _no_aplica(b, n, t)
            if t == h:
                disp, mot = "misma hoja", "references another view of the same sheet"
            elif m:                         # declarada fuera de alcance: se revisó (se marca y se sigue), con su motivo
                disp, mot = "fuera de alcance", m
                if t not in visitadas:
                    cola.append(t)
            elif (n.lstrip('0') or n, t) in citas:
                disp, mot = "citada", f"cited in the Excel row {citas_en.get((n.lstrip('0') or n, t), '?')}"
                if t not in visitadas:
                    cola.append(t)
            else:
                disp, mot = "sin disposición", ""
            out.append(dict(p, origen=h, disp=disp, motivo=mot))
        if not cola:
            # BE-CC07 (Consumer Cellular rev1, 5-nov): the chain only started at the entrance sheets, so the bubbles of every
            # sheet the chain never reached (A101, A102, A402, A501, A700) were never circled and the gate passed blind.
            # Every sheet with a bubble (detector + burbujas_verificadas + CADENA.md) seeds the queue.
            cola = [x for x in hojas_con_burbujas(b) if x not in visitadas]
    return out


def faltan_circulos(b, circulos_por_hoja):
    """BE-CC07: per-sheet count against the UNION (detector + burbujas_verificadas + CADENA.md). circulos_por_hoja =
    {sheet: number of 'origin' circles in DETALLES_REVISADOS.pdf}. -> list of failures (empty = OK)."""
    cm, ev = cadena_md(b), []
    lab = {norm_hoja(k): v for k, v in (circulos_por_hoja or {}).items()}
    for h in hojas_con_burbujas(b):
        nb = len(_burbujas_pos(b, h))
        if not lab.get(h):
            ev.append(f"{h}: {max(nb, cm.get(h, 0))} burbuja(s) (detector + verificadas + CADENA.md) y 0 círculos de origen (BE-CC07)")
        elif lab[h] < nb:
            ev.append(f"{h}: {lab[h]} círculo(s) de origen para {nb} burbujas (BE-CC07)")
    return ev


RX_CADENA_ITEM = re.compile(r"^\s*\d+(?:\s*-\s*\d+)?\.\s+\*\*([A-Z]{1,2}-?\d{3}(?:\.\d{1,2})?)\b", re.M)


def cadena_md(b):
    """BE-CC07: origin sheets of the items of the project's CADENA.md (numbered '**SHEET N/SHEET**' items) -> {sheet: n_items}."""
    out = {}
    for t in (getattr(b, "cadena_md", None) or "",):
        for h in RX_CADENA_ITEM.findall(t):
            out[norm_hoja(h)] = out.get(norm_hoja(h), 0) + 1
    return out


def hojas_con_burbujas(b):
    """BE-CC07: UNION of the sheets with bubbles: detector (set_texto burbujas), burbujas_verificadas.json (n + hoja) and the
    origin sheets of CADENA.md, in sheet order."""
    hs = set()
    for k, v in ((b.set_meta or {}).get("burbujas") or {}).items():
        if isinstance(v, dict) and v.get("burbujas"):
            hs.add(norm_hoja(k))
    ver = b.verificadas if isinstance(b.verificadas, dict) else {}
    for k, xs in ver.items():
        if isinstance(xs, list) and any(isinstance(x, dict) and x.get("n") and x.get("hoja") for x in xs):
            hs.add(norm_hoja(k))
    hs |= set(cadena_md(b))
    orden = [norm_hoja(h) for h in (b.hojas or {})]
    return sorted(hs, key=lambda h: (orden.index(h) if h in orden else 9999, h))


RX_HOJA_DET = re.compile(r"\b(?:DETAILS?|SECTIONS?)\b", re.I)


@chk("U-113", "BE-124", desc="U-113 / BE-124 CE_CALLOUTS: toda burbuja N/HOJA de las hojas de nuestro trade (y de cada detalle "
     "que la cadena alcanza) está citada como fuente en el Excel / canon o declarada fuera de alcance con motivo; la cadena "
     "se sigue hasta el último detalle; un detalle / hoja citado que no existe en el set se reporta; U-137 / BE-139: las burbujas de DOS líneas (número arriba / hoja abajo) del detector palabras_fitz.py (burbujas) entran a la cadena, 0 burbujas con hojas de detalles en el set = FAIL (PASS en vacío prohibido) y todo círculo con divisoria sin leer se verifica a ojo")
def ce_callouts(b):
    """U-113 / BE-124 + U-137 / BE-139: cadena de callouts completa, con las burbujas de dos líneas del detector."""
    if b.hojas is None:
        return R("FAIL", "sin set_texto.json: no se pueden seguir las burbujas del set (correr compuerta_entrega.py texto)")
    bub = (b.set_meta or {}).get("burbujas")
    if bub is None:
        return R("FAIL", "set_texto.json sin barrido de burbujas de dos líneas (U-137): correr `compuerta_entrega.py burbujas "
                         "<set_texto.json> <bidset.pdf>`; el texto solo ve 'N/HOJA' en una línea y pasa en vacío")
    txt_h = {}
    for h, t in b.hojas.items():
        txt_h[norm_hoja(h)] = txt_h.get(norm_hoja(h), "") + "\n" + t
    ocr = {norm_hoja(h) for h in (b.set_meta or {}).get("ocr") or []}
    entrada = _hojas_entrada(b) & set(txt_h)
    if not entrada:
        return R("FAIL", "ninguna hoja del canon (walls / cielos / demo) está en set_texto.json: no hay de dónde seguir las cadenas")
    # CR-R11-H6: 'citada' exige la CELDA del Excel que la cita (hoja!celda); el texto del canon (índices, barridos) ya no cuenta
    citas_en = {}
    for hj_, cc_, t_ in b.celdas:
        for n, h in CALLOUT.findall(str(t_)):
            citas_en.setdefault((n.lstrip('0') or n, norm_hoja(h)), f"{hj_}!{cc_}")
    citas = set(citas_en)   # BE-CR24: '08' = '8'
    ev_sin, ev_corta, ev_no_existe, ev_motivo, ev_pend, amb = [], [], [], [], [], []
    # CC-R10 (Consumer Cellular rev3 audit): CE_CALLOUTS counts against the same UNION as CE_DETALLES_CIRCULADOS (BE-CC07):
    # every sheet with bubbles (detector + burbujas_verificadas + CADENA.md) enters the chain (before: '2 cited / 10' with 49)
    visitadas, cola = set(), [(h, 0, None) for h in sorted(entrada)] + \
        [(h, 1, "union BE-CC07") for h in hojas_con_burbujas(b) if h not in entrada and h in txt_h]
    usados, n_bub_entrada = 0, 0
    burb_de = {}
    while cola:
        h, d, desde = cola.pop(0)
        if h in visitadas:
            continue
        visitadas.add(h)
        leidas, pend = _burbujas_hoja(b, h)
        burb_de[h] = leidas
        if d == 0:
            n_bub_entrada += len(leidas) + len(pend) + len(callouts_de(txt_h.get(h)))
        ev_pend += [f"{h} {x}: círculo con divisoria sin leer — verificar a ojo en burbujas_verificadas.json" for x in pend]
        for n, t in sorted(set(callouts_de(txt_h.get(h))) | leidas):
            if t == h:
                continue                      # el rótulo del propio detalle en su hoja (1/A5.1 dentro de A5.1)
            if t not in txt_h:
                if h in ocr and (n, t) not in leidas and _no_aplica(b, n, t) is None:
                    # texto OCR de una hoja raster: '8/A5.4' = '8/A5.1' mal leído (O'Reilly A5.1 door schedule) -> a ojo
                    amb.append(f"{n}/{t} (texto OCR de {h}): la hoja {t} no existe — verificar a ojo la lectura del OCR")
                elif _no_aplica(b, n, t) is None:
                    ev_no_existe.append(f"{n}/{t} (en {h}): la hoja {t} no existe en el set")
                continue
            if not re.search(r"(?<![\w./\-])" + re.escape(n) + r"(?![\w./\-])", txt_h[t]) and \
                    (n, t) not in _burbujas_hoja(b, t)[0] and not _detalle_verificado(b, n, t):
                if t in ocr:                  # hoja raster: el OCR no siempre lee el número del título del detalle
                    amb.append(f"{n}/{t} (en {h}): el OCR de {t} no muestra el detalle {n} — verificar a ojo")
                elif _no_aplica(b, n, t) and re.search(r"\bRFI-?\d+|\bNOT printed\b", _no_aplica(b, n, t)):
                    # v81cf35 (BE-CF22): referencia impresa a una vista que no existe, ya reportada en su RFI -> AMBER (reportada)
                    amb.append(f"{n}/{t} (en {h}): la hoja {t} no tiene el detalle {n} — reportado: {_no_aplica(b, n, t)[:80]}")
                    continue
                else:
                    ev_no_existe.append(f"{n}/{t} (en {h}): la hoja {t} no tiene el detalle {n}")
                    continue
            if (n.lstrip('0') or n, t) in citas:
                usados += 1
                if t not in visitadas:
                    cola.append((t, d + 1, f"{n}/{t}"))
                continue
            motivo = _no_aplica(b, n, t)
            if motivo is not None:
                if len(motivo.strip()) < 8:
                    ev_motivo.append(f"{n}/{t}: fuera de alcance sin motivo escrito")
                continue
            (ev_sin if d == 0 else ev_corta).append(
                f"{n}/{t} (burbuja en {h}" + (f", alcanzada por {desde}" if desde else "") + "): sin cita N/HOJA en el Excel / "
                "canon ni declaración fuera de alcance" + ("" if d == 0 else " — cadena cortada antes del final"))
    ev = []
    n_det = sum(1 for k, t in txt_h.items() if k not in entrada and RX_HOJA_DET.search(t or ""))
    ver_ = b.verificadas if isinstance(b.verificadas, dict) else {}
    barridas_ojo = bool(entrada) and all(any(norm_hoja(k) == h for k in ver_) for h in entrada)
    if ((n_bub_entrada == 0 and n_det >= 1) or (n_bub_entrada <= 1 and n_det >= 3)) and barridas_ojo:
        # BE-CC03 (Consumer Cellular, 5-nov): plantas con 0-1 burbujas REALES, cada hoja de entrada barrida a ojo
        # (burbujas_verificadas.json con su lista): el conteo bajo es del set, no del detector -> AMBER reportado
        amb.append(f"{n_bub_entrada} burbuja(s) en las hojas de entrada {sorted(entrada)}: conteo bajo del set, cada hoja "
                   "barrida a ojo en burbujas_verificadas.json (BE-CC03)")
    elif (n_bub_entrada == 0 and n_det >= 1) or (n_bub_entrada <= 1 and n_det >= 3):   # 0 o casi 0 (U-137)
        ev.append(f"{n_bub_entrada} burbujas de detalle en las hojas de entrada {sorted(entrada)} y el set tiene hojas de detalles / "
                  "secciones: PASS en vacío prohibido (U-137) — el detector no ve las burbujas de este set")
    if ev_sin:
        ev.append(f"{len(ev_sin)} burbuja(s) sin disposición en las hojas del trade")
        ev += ev_sin[:20]
    if ev_corta:
        ev.append(f"{len(ev_corta)} eslabón(es) de cadena sin seguir")
        ev += ev_corta[:20]
    if ev_no_existe:
        ev.append(f"{len(ev_no_existe)} detalle(s) / hoja(s) referidos que no existen")
        ev += ev_no_existe[:15]
    if ev_pend:
        ev.append(f"{len(ev_pend)} círculo(s) con divisoria sin leer ni verificar (detector o conteo independiente)")
        ev += ev_pend[:15]
    ev += ev_motivo[:10]
    if ev:
        return R("FAIL", *ev)
    nb = sum(len(v) for v in burb_de.values())
    if amb:
        return R("AMBER", f"{usados} burbujas citadas ({nb} burbujas de dos líneas en {len(visitadas)} hojas)", *amb[:15])
    return R("PASS", f"{usados} burbujas citadas + declaradas ({nb} burbujas de dos líneas), cadenas seguidas por "
                     f"{len(visitadas)} hojas",
             f"conteos (CR-R10-m3): {usados} = destinos N/HOJA ÚNICOS citados en el Excel / canon o declarados; {nb} = burbujas (instancias) "
             f"en las {len(visitadas)} hojas que alcanza la cadena del trade; CE_DETALLES_CIRCULADOS cuenta en cambio TODAS las burbujas de "
             f"todas las hojas de origen del set (también S / M / P / E fuera de la cadena)")


# ============================================================================================== PREFERENCIAS DEL DÍA 1
# Orden del usuario 3-nov (BE-131): las preferencias que dio "en los primeros días" (honestidad dimensional #0, detalles,
# no preguntar / no elegir en silencio, barrido por tag, evidencia visual, idioma, ejes, formato, costos, términos del
# trade) quedan como reglas INVIOLABLES U-114..U-125 con chequeo de FONDO aquí (compuerta_entrega.py los corre).
RX_CONF = re.compile(r"(?i)\bCONFIRM(?:ED|ADO)\b")
RX_DERIV = re.compile(r"(?i)\bDERIV(?:ED|ADO)\b")
RX_PEND = re.compile(r"(?i)\bPENDI(?:NG|ENTE)\b|\bRFI-?\d+")
# operación visible: "a - b = c", "x 6.75", "= 18.17", "FLOOR(", "sum of", "Σ", "->" con número
RX_OPERACION = re.compile(r"=\s*[-\d(A-Za-z]|\d\s*[x×*+]\s*\(?\d|\d\s+[-−]\s+\d|\b(?:FLOOR|ROUNDUP|CEILING|MAX|MIN)\(|"
                          r"(?i:\bsum of\b|Σ|\bminus\b|\bplus\b|\btimes\b)|(?:->|→)\s*\d")
RX_A_OJO = re.compile(r"(?i)\bscaled\b|\bby scale\b|measured (?:at|to) scale|\bestimated?\b|\bapprox(?:\.|imately)?\b|"
                      r"\beyeball|\bby eye\b|\ba ojo\b|\ba escala\b|\bescalad[oa]\b|\baproximad")
RX_DECIDIDO = re.compile(r"(?i)\bRFI-?\d+|R80e\.34|R-ALC-\d+|\bU-\d{3}\b|estimator decision|\bASTM\b|\bGA-\d|\bAISI\b|"
                         r"\bIBC\b|\bCBC\b|\bUL\s?[A-Z]?\d|\bSSMA\b|\bASCE\b|\bNFPA\b|\b0[5-9]\s?\d{2}\s?\d{2}\b|"
                         r"\bper (?:mfr|manufacturer)\b|ClarkDietrich|\bUSG\b|\bReview Item\b")   # R80f.38
RX_SUPUESTO = re.compile(r"(?i)\bassum(?:ed|ption|e)\b|\bdefault\b|\bsupuest[oa]\b|not printed|not shown|not dimensioned|"
                         r"not specified|not called out|no (?:printed )?dimension|\bwe chose\b|\bchosen\b|\bjudg(?:e)?ment\b")
RX_NHOJA = re.compile(r"(?<![\w.\-/])(?:[A-Z]{1,2}\d\.\d{2}|[A-Z]{0,3}\.?\d{1,3}[A-Z]?|[A-Z]{1,2})\s*/\s*[A-Z]{1,3}-?\d{1,3}(?:\.\d{1,2})?[A-Z]?\b")
RX_SPEC_CODE = re.compile(r"\b0[5-9]\s?\d{2}\s?\d{2}\b|\bASTM\b|\bGA-\d|\bAISI\b|\bIBC\b|\bCBC\b|\bUL\s?[A-Z]?\d|\bSSMA\b|"
                          r"\bASCE\b|\bNFPA\b|R80e\.34|R-ALC-\d+|\bU-\d{3}\b")
RX_IMG = re.compile(r"[\w./\\ \-]+\.(?:png|jpe?g)\b", re.I)
RX_JUNTA = re.compile(r"[A-Z0-9][\w.\-]*\d[a-z]?\s*(?:\+|&|\band\b)\s*[A-Z0-9][\w.\-]*\d")
RX_NOTA_REF = re.compile(r"\bKN\s?\d{1,3}\b|(?<![\w.])[A-H]\.\d{1,2}(?![\w.])")
RX_DOS_FACHADAS = re.compile(r"(?i)\b(north|south|east|west|front|rear|left|right)\b\s*(?:\+|&|and|/)\s*"
                             r"(north|south|east|west|front|rear|left|right)\b")
# términos del trade en español prohibidos (orden del usuario día 1: "tablaroca", "poste metálico", "canal")
TRADE_ES = re.compile(r"(?i)(?<![\w-])(?:tabla\s*roca|panel(?:es)? de yeso|placas? de yeso|l[aá]minas? de yeso|yeso laminado|"
                      r"perfiler[ií]a met[aá]lica|postes?(?: met[aá]licos?)?|montantes?|canal(?:es)?|rieles?|esquineros?|"
                      r"triplay|contrachapado|viguetas?|dinteles?|compuesto (?:para|de) juntas|cinta (?:de papel|para juntas))(?![\w-])")


def _fuentes_cantidad(b):
    """[(etiqueta, cantidad, fuente)] de cada número del canon: largo / altura del wall, altura de cada cara, cielos."""
    out = []
    for w in b.walls():
        if not str(w.get("element") or "wall").startswith(("wall", "soffit", "column", "furring", "bulkhead", "demo")) \
                and w.get("length_ft") is None:
            continue
        for k in ("length", "height"):
            if w.get(f"{k}_ft") not in (None, 0):
                out.append((f"{w.get('id')} {k}", w.get(f"{k}_ft"),
                            " ".join(str(w.get(x) or "") for x in (f"{k}_source", f"{k}_status", f"{k}_op"))))
        for f in w.get("faces") or []:
            if isinstance(f, dict) and f.get("height_ft") not in (None, 0):
                out.append((f"{w.get('id')} face {f.get('side')} height", f.get("height_ft"),
                            " ".join(str(f.get(x) or "") for x in ("height_source", "height_status", "height_op"))))
    for z in b.ceilings():
        for k in ("area_sf", "height_ft"):
            if z.get(k) not in (None, 0):
                s = k.split("_")[0]
                out.append((f"{z.get('id')} {s}", z.get(k), " ".join(str(z.get(x) or "") for x in
                                                                     (f"{s}_source", f"{s}_status", f"{s}_op", "source"))))
    return out


@chk("U-114", desc="U-114 (día 1, #0 HONESTIDAD DIMENSIONAL): cada número del canon lleva estado: [CONFIRMED] = cota impresa "
     "citando HOJA · [DERIVED] = con su operación visible · [PENDING] = no acotado + RFI; nada escalado / estimado a ojo sin "
     "PENDING + RFI; los renglones del Partition Takeoff llevan su estado")
def u_114(b):
    """U-114: honestidad dimensional por número."""
    fs = _fuentes_cantidad(b)
    if not fs and not b.pt:
        return SIN("canon y Partition Takeoff")
    ev = []
    ids = {str(w.get("id")) for w in b.walls()}
    for et, v, src in fs:
        conf, der, pen = RX_CONF.search(src), RX_DERIV.search(src), RX_PEND.search(src)
        m = re.search(r"(?i)\bsame as\s+([\w.\-]+)", src)
        if m and m.group(1).rstrip(".") in ids and not (conf or der or pen):
            continue                     # hereda el estado del wall citado (DERIVED por referencia)
        if not (conf or der or pen):
            ev.append(f"{et} = {v}: sin estado [CONFIRMED] / [DERIVED] / [PENDING] ('{src[:70]}')")
            continue
        if conf and not der and not RX_HOJA_CITA.search(src):
            ev.append(f"{et} = {v}: [CONFIRMED] sin la HOJA de la cota impresa ('{src[:70]}')")
        if re.search(r"(?i)height|altura", str(et)) and not RX_HOJA_CITA.search(src):
            ev.append(f"{et} = {v}: altura sin hoja citada ('{src[:70]}') (U-138)")
        if der and not conf and not RX_OPERACION.search(re.sub(r"\d+/\d+", "", src)):
            ev.append(f"{et} = {v}: [DERIVED] sin su operación ('{src[:90]}')")
        if RX_A_OJO.search(src) and not pen:
            ev.append(f"{et} = {v}: valor escalado / estimado ('{RX_A_OJO.search(src).group(0)}') sin [PENDING] + RFI")
    for f in b.pt:
        if f.get("wall") and f.get("lf") and not RX_ESTADO.search(str(f.get("status") or "") + " " + str(f.get("source") or "")):
            ev.append(f"Partition Takeoff fila {f['fila']} ({f['wall']}): Status sin [CONFIRMED] / [DERIVED] / [PENDING]")
    return R("FAIL", f"{len(ev)} número(s) sin honestidad dimensional", *ev[:25]) if ev else \
        R("PASS", f"{len(fs)} números con estado, hoja u operación")


@chk("U-115", desc="U-115 (día 1, DETALLES): toda partida cita N/HOJA: cada renglón de wall del Partition Takeoff con su "
     "detalle N/HOJA (6/A-410) y cada renglón con cantidad del Material Summary con N/HOJA o sección de spec / código "
     "(la cadena de burbujas la sigue CE_CALLOUTS)")
def u_115(b):
    """U-115: N/HOJA en cada partida."""
    if not b.pt and not b.ms:
        return SIN("Excel")
    ev = [f"Partition Takeoff fila {f['fila']} ({f['wall']}): Source '{str(f.get('source') or '')[:40]}' sin N/HOJA"
          for f in b.pt if f.get("wall") and (f.get("lf") or f.get("board")) and not RX_NHOJA.search(str(f.get("source") or ""))]
    # Material Summary: N/HOJA, hoja de planta (cantidad medida en planta), spec / código, o derivado de otros renglones
    ev += [f"Material Summary fila {f['fila']} '{f['material'][:40]}': sin N/HOJA, hoja, spec / código ni renglón de origen"
           for f in b.ms if (f["net"] or 0) > 0 and not (RX_NHOJA.search(f["fuente"]) or RX_SPEC_CODE.search(f["fuente"])
                                                          or RX_HOJA_CITA.search(re.sub(r"(?i)N/SHEET", "", f["fuente"]))
                                                          or re.search(r"(?i)\bdriver\b|Inputs!B\d+|rows? of this sheet", f["fuente"]))]
    return R("FAIL", f"{len(ev)} partida(s) sin N/HOJA", *ev[:25]) if ev else R("PASS", "toda partida cita N/HOJA")


@chk("U-116", desc="U-116 (día 1, NO PREGUNTAR / NO ELEGIR EN SILENCIO): todo supuesto / default / 'not printed' del Excel o "
     "del canon remite a su RFI (con delta de cada alternativa), a un precedente escrito (R80e.34 / R-ALC / U-NNN) o al "
     "código citado; ningún supuesto queda sin RFI")
def u_116(b):
    """U-116: ningún supuesto en silencio."""
    textos = [(f"{h}!{c}", t) for h, c, t in b.celdas if h in ("Partition Takeoff", "Material Summary", "Scope Checklist",
                                                                 "Inputs", "Review Items")]
    rfi_wall = {}
    for w in b.walls():
        for k in ("length_source", "height_source", "stud_source", "gauge_source", "board_source", "top_track"):
            if w.get(k):
                textos.append((f"canon {w.get('id')}.{k}", str(w[k])))
        for f in w.get("faces") or []:
            if isinstance(f, dict):
                for k in ("height_source", "board_source"):
                    if f.get(k):
                        textos.append((f"canon {w.get('id')} face {f.get('side')}.{k}", str(f[k])))
        m = re.search(r"\bRFI-?\d+", json.dumps(w, ensure_ascii=False))
        if m:
            rfi_wall[str(w.get("id"))] = m.group(0)      # una cara que remite al height_source de su wall hereda su RFI
    if not textos:
        return SIN("Excel / canon")
    ids = {str(r[0]).strip() for r in b.pend if r} | {str(r.get("id")) for r in (b.canon.get("rfis") or []) if isinstance(r, dict)}
    ev = []
    for et, t in textos:
        if t.startswith("=") or not RX_SUPUESTO.search(t):
            continue
        m = RX_DECIDIDO.search(t)
        wid = et[6:].split(" ")[0].split(".")[0] if et.startswith("canon ") else None
        if not m and wid in rfi_wall and re.search(r"(?i)see (?:the )?wall|wall height_source|per wall", t):
            continue
        if not m:
            ev.append(f"{et}: supuesto sin RFI / precedente / código ('{t[max(0, RX_SUPUESTO.search(t).start() - 30):][:90]}')")
            continue
        for rid in re.findall(r"\bRFI-?\d+", t):
            if ids and rid not in ids and rid.replace("RFI", "RFI-").replace("--", "-") not in ids \
                    and not re.search(re.escape(rid) + r"[^|]{0,40}(?i:closed|cerrad|estimator decision)", b.excel_txt()):
                ev.append(f"{et}: el supuesto remite a {rid}, que no está en Pending Items ni cerrado")
    # v81cf37 (BE-CF23, CFA rev7 RFI-27): U-048 — un RFI ABIERTO lleva el supuesto conservador CARGADO con su delta, nunca
    # "nothing loaded" / "not loaded" / "not carried" (eso es elegir 0 en silencio)
    rx_0 = re.compile(r"(?i)\bnothing (?:is )?(?:loaded|carried|included)\b|\bnot (?:loaded|carried|included)\b|\bno se carg|\bsin cargar\b|\bno cargad")
    for r in list(b.tk.get("rfis") or []) + list(b.canon.get("rfis") or []):
        # v81cf38 (O'Reilly rev7): el estado va en 'status' (CFA) o en 'estado' (O'Reilly: "CLOSED"); cerrado / decidido = no aplica
        est = str(r.get("status") or r.get("estado") or "open")
        if not isinstance(r, dict) or not est.lower().startswith("open") or re.search(r"(?i)closed|cerrad|estimator decision", est):
            continue
        a = (r.get("opciones") or {}).get("A") or {}
        t = " ".join(str(x) for x in (a.get("texto"), r.get("pregunta"), r.get("question")) if x)
        if rx_0.search(t):
            ev.append(f"{r.get('id')}: RFI abierto 'no cargado' ('{rx_0.search(t).group(0)}'): U-048 exige el supuesto conservador cargado con su delta")
    ev = list(dict.fromkeys(ev))
    return R("FAIL", f"{len(ev)} supuesto(s) en silencio", *ev[:25]) if ev else R("PASS", "todo supuesto con su RFI / precedente / código")


def _inv_ocurrencias(b):
    inv = b.inv_full if isinstance(b.inv_full, dict) else {}
    oc = inv.get("ocurrencias") or {}
    return [o for k in ("partition_tag", "partition_ambiguo") for o in (oc.get(k) or []) if isinstance(o, dict)]


@chk("U-117", desc="U-117 (día 1, BARRIDO): cada tag recorrido en TODO el plano antes de cerrarlo: lista numerada por "
     "programa (inventario_tags) con imagen circulada y reabierta (png_verificado) de cada ubicación, y el conteo por type "
     "del canon (tag_ids) = conteo del inventario")
def u_117(b):
    """U-117: barrido completo por tag."""
    walls = [w for w in b.walls() if str(w.get("element") or "wall") == "wall"]
    if not walls:
        return NA("sin walls en el canon")
    occ = _inv_ocurrencias(b)
    if not occ:
        return R("FAIL", "sin inventario de tags (1_inventario/inventario.json de inventario_tags.py): el barrido por tag no se hizo")
    ev = []
    # U-138 (auditoría 4-nov): el inventario debe ser de ESTE set (no copiado de otro proyecto): páginas = páginas del set y
    # cada ubicación en una hoja del set
    inv = b.inv_full if isinstance(b.inv_full, dict) else {}
    pag_set = sum(int(f.get("paginas") or 0) for f in ((b.set_meta or {}).get("fuentes") or []) if isinstance(f, dict))
    # BE-CR0-08 (CR desde cero 13-nov): set_texto junta varios PDF (A + S); el inventario de tags es del PDF de arquitectura.
    # Vale si sus páginas = las del set completo o las de UNO de los PDF fuente (los demás no traen partition tags).
    pag_fuentes = {int(f.get("paginas") or 0) for f in ((b.set_meta or {}).get("fuentes") or []) if isinstance(f, dict)}
    if pag_set and inv.get("pages") and int(inv["pages"]) != pag_set and int(inv["pages"]) not in pag_fuentes:
        ev.append(f"inventario.json de {inv['pages']} páginas y el set de {pag_set}: inventario de otro set")
    if b.hojas:
        hs = {norm_hoja(h) for h in b.hojas}
        fuera = sorted({str(o.get("sheet")) for o in occ if o.get("sheet") and norm_hoja(o.get("sheet")) not in hs})
        if fuera:
            ev.append(f"ubicaciones del inventario en hojas que no están en el set: {', '.join(fuera[:6])}")
    for i, o in enumerate(occ, 1):
        oid = o.get("id") or f"#{i}"
        if not o.get("png"):
            ev.append(f"{oid} ({o.get('type')} en {o.get('sheet')}): ubicación sin imagen circulada")
            continue
        ok, mot = _img_ok(b, o["png"], marca=False)
        if not ok:
            ev.append(f"{oid}: imagen {o['png']} {mot}")
        elif o.get("png_verificado") is not True:
            ev.append(f"{oid}: imagen sin reabrir / verificar (png_verificado != true)")
    # R80f.38: un tags_descartados del canon (id + motivo >= 8 + imagen circulada) también es disposición (U-117: "en un
    # tag_ids o en tags_descartados con motivo e imagen circulada")
    desc = {}
    for d in b.canon.get("tags_descartados") or []:
        if isinstance(d, dict) and d.get("id") and len(str(d.get("motivo") or "")) >= 8:
            ok, mot = _img_ok(b, d.get("imagen") or d.get("img") or d.get("png"))
            if not ok:   # v81cf30: sin imagen propia vale la imagen circulada y verificada de esa ubicación en el inventario
                oi = next((o for o in occ if str(o.get("id")) == str(d["id"])), None)
                if oi and oi.get("png") and oi.get("png_verificado") is True and _img_ok(b, oi["png"], marca=False)[0]:
                    ok = True
            if ok:
                desc[str(d["id"])] = True
            else:
                ev.append(f"{d['id']}: descarte sin imagen circulada ({mot})")
    usados = {}
    # v81cf28 (CFA rev6, BE-CF21): los walls board-only (existing_walls[]: wood / existing con board nuestro) también
    # disponen de su tag (tag_ids), y un tag del canon en tags_descartados [{id, motivo, imagen}] con motivo es descarte
    for w in list(b.walls()) + [x for x in (b.canon.get("existing_walls") or []) if isinstance(x, dict)]:
        for t in w.get("tag_ids") or []:
            for pid in re.findall(r"\bP[TA]\d{3,}\b", str(t)):
                usados[pid] = str(w.get("tag") or w.get("type") or "").upper()
    for x in b.canon.get("tags_descartados") or []:
        if isinstance(x, dict) and len(str(x.get("motivo") or "")) >= 8 and re.match(r"P[TA]\d{3,}$", str(x.get("id") or "")):
            usados[str(x["id"])] = "DESCARTADO"
    # BE-CR25: un wall EXCLUDED con motivo (tenant / F&B / door opening) también dispone de su tag (destino = EXCLUDED)
    for x in b.canon.get("excluded_walls") or []:
        if isinstance(x, dict) and len(str(x.get("reason") or "")) >= 8:
            for t in x.get("tag_ids") or []:
                for pid in re.findall(r"\bP[TA]\d{3,}\b", str(t)):
                    usados.setdefault(pid, "EXCLUDED")
    por_type = {}
    for o in occ:
        tp = str(o.get("type") or "").upper()
        n_inv, n_ok = por_type.get(tp, (0, 0))
        dispuesto = o.get("id") in usados or o.get("id") in desc or (o.get("kind") == "partition_ambiguo" and len(str(o.get("descartado") or o.get("motivo") or "")) >= 8)
        por_type[tp] = (n_inv + 1, n_ok + (1 if dispuesto else 0))
        if not dispuesto:
            ev.append(f"{o.get('id')} (type {tp} en {o.get('sheet')}): ubicación del inventario sin wall (tag_ids) ni descarte con motivo")
    for tp, (n_inv, n_ok) in sorted(por_type.items()):
        if n_ok != n_inv:
            ev.insert(0, f"type {tp}: inventario {n_inv} ubicación(es), canon {n_ok} -> conteo distinto")
    return R("FAIL", *ev[:30]) if ev else R("PASS", f"{len(occ)} ubicaciones numeradas, circuladas, verificadas y contadas")


_IMG_IDX = {}


def _img_ok(b, p, marca=True):
    """(ok, motivo): la imagen existe (ruta, relativa a la corrida o mismo nombre debajo), no está vacía y, con marca=True,
    tiene la marca circulada roja (>= 15 px rojo puro, como dibujan planmark / evidencia / inventario_tags)."""
    p = str(p or "").strip()
    if not p:
        return False, "sin imagen"
    cands = [p] + [os.path.join(d, p) for d in (b.raiz, b.canon_dir, b.inv_dir) if d]
    ruta = next((c for c in cands if os.path.isfile(c)), None)
    if ruta is None and b.raiz:
        if b.raiz not in _IMG_IDX:
            idx = {}
            for r, _, fs in os.walk(b.raiz):
                for f in fs:
                    if f.lower().endswith((".png", ".jpg", ".jpeg")):
                        idx.setdefault(f, os.path.join(r, f))
            _IMG_IDX[b.raiz] = idx
        ruta = _IMG_IDX[b.raiz].get(os.path.basename(p))
    if ruta is None:
        return False, "no existe"
    if os.path.getsize(ruta) == 0:
        return False, "vacía (0 bytes)"
    if not marca:
        return True, ""
    try:
        from PIL import Image
        im = Image.open(ruta).convert("RGB")
        try:
            import numpy as np
            a = np.asarray(im)
            n = int(((a[..., 0] > 190) & (a[..., 1] < 80) & (a[..., 2] < 80)).sum())
        except ImportError:
            n = sum(1 for r, g, bb in im.getdata() if r > 190 and g < 80 and bb < 80)
    except Exception as e:                       # noqa: BLE001
        return False, f"no abre ({type(e).__name__})"
    return (True, "") if n >= 15 else (False, "sin marca circulada (0 px rojos)" if n == 0 else f"sin marca circulada ({n} px rojos)")


@chk("U-118", desc="U-118 (día 1, EVIDENCIA VISUAL): imagen de todo lo que se afirma, reabierta antes de entregar: cada wall "
     "con imagen de largo y de altura que existe, no está vacía y trae la marca circulada; cada RFI abierto y cada Review "
     "Item con su imagen circulada")
def u_118(b):
    """U-118: evidencia visual que existe y está circulada."""
    walls = [w for w in b.walls() if w.get("length_ft")]
    if not walls and not b.pend and not b.review:
        return SIN("canon / Pending / Review")
    ev = []
    for w in walls:
        for k in ("img", "height_img"):
            v = w.get(k)
            v = v[0] if isinstance(v, list) and v else v
            ok, mot = _img_ok(b, v)
            if not ok:
                ev.append(f"{w.get('id')}.{k}: {mot}" + (f" ({v})" if v else ""))
        for k in ("detail_img", "stud_img"):
            if w.get(k):
                ok, mot = _img_ok(b, w[k], marca=False)
                if not ok:
                    ev.append(f"{w.get('id')}.{k}: {mot} ({w[k]})")
    for r in b.rfis_abiertos():
        rid = str(r[0]).strip()
        rc = b.rfi_canon(rid)
        v = rc.get("img") or rc.get("imagen") or rc.get("evidencia") or (RX_IMG.search(" ".join(map(str, r))) or [None])[0]
        v = v[0] if isinstance(v, list) and v else v
        ok, mot = _img_ok(b, v)
        if not ok:
            ev.append(f"{rid}: evidencia {mot}" + (f" ({v})" if v else ""))
    for r in b.review:
        if not r or not re.match(r"\s*\d", str(r[0])):
            continue
        celda = str(r[5]) if len(r) > 5 else ""
        m = RX_IMG.search(celda)
        ok, mot = _img_ok(b, m.group(0).strip() if m else None)
        if not ok:
            ev.append(f"Review Item {r[0]}: Image '{celda[:50]}' {mot}")
    return R("FAIL", f"{len(ev)} afirmación(es) sin imagen circulada", *ev[:30]) if ev else R("PASS", "toda afirmación con imagen circulada")


@chk("U-119", desc="U-119 (día 1, IDIOMA): el entregable va íntegro en inglés: Excel (todas las celdas visibles), "
     "README_REVIEW.md y markups sin español (PARA_REVISAR_EN_LA_MANANA.md y SEGUIMIENTO.md son las notas en español para "
     "el usuario)")
def u_119(b):
    """U-119: entregable en inglés."""
    import idioma_es
    ev = []
    # "EL." / "EL 108'-6\"" = elevation, no el artículo (O'Reilly rev10: "B.O. framing EL 108'-6\"" en SCHEDULES_MATERIALES)
    sin_el = lambda t: re.sub(r"\bEL\.?(?=\s*\d)|\bEL\.(?=[\s\d;,.)+]|$)", "", str(t))      # noqa: E731
    for h, c, t in b.celdas:
        if not str(t).startswith("=") and idioma_es.es_espanol(sin_el(t)):
            ev.append(f"{h}!{c}: español ({', '.join(idioma_es.es_espanol(sin_el(t))[:3])}) '{str(t)[:60]}'")
    rd = next((t for n, t in b.docs.items() if n.upper().startswith("README")), None)
    if rd:
        rd = re.sub(r"(?i)ESTA ES LA VERSI[OÓ]N FINAL PARA REVISAR|(?<![a-z0-9])rev\d+[a-z]? FINAL PARA REVISAR", "", rd)   # v128      # rótulo obligatorio U-089 (corto desde U-165)
        for i, l in enumerate(rd.splitlines(), 1):
            if idioma_es.es_espanol(sin_el(l)):
                ev.append(f"README_REVIEW.md línea {i}: español '{l[:60]}'")
    for a in b.annots or []:
        if idioma_es.es_espanol(sin_el(a.get("contents") or "")):
            ev.append(f"markup {a.get('label')}: español '{(a.get('contents') or '')[:60]}'")
    if not b.celdas and rd is None and not b.annots:
        return SIN("Excel / README / markups")
    return R("FAIL", f"{len(ev)} texto(s) en español en el entregable", *ev[:25]) if ev else R("PASS", "entregable en inglés")


def _giro_max(vs, min_seg=3.0):
    """mayor giro (grados) entre tramos consecutivos de una polilínea (tramos < min_seg pt no cuentan: curvas / arcos)."""
    segs = [(vs[i + 1][0] - vs[i][0], vs[i + 1][1] - vs[i][1]) for i in range(len(vs) - 1)]
    segs = [s for s in segs if math.hypot(*s) >= min_seg]
    g = 0.0
    for (ax, ay), (bx, by) in zip(segs, segs[1:]):
        c = (ax * bx + ay * by) / (math.hypot(ax, ay) * math.hypot(bx, by))
        g = max(g, math.degrees(math.acos(max(-1.0, min(1.0, c)))))
    return g


@chk("U-120", desc="U-120 (día 1, EJES): nunca dos ejes / fachadas / walls en un número: ningún Wall # ni id del canon "
     "unido ('A-14+A-12', 'W1 & W2'), ningún wall con dos fachadas, ninguna polilínea de markup que dobla de eje (giro > 60°)")
def u_120(b):
    """U-120: un eje / fachada por número."""
    if not b.pt and not b.walls() and b.annots is None:
        return SIN("Excel / canon / markups")
    ev = [f"Partition Takeoff fila {f['fila']}: Wall # '{f['wall']}' junta dos walls / ejes" for f in b.pt if RX_JUNTA.search(str(f.get("wall") or ""))]
    for w in b.walls():
        if RX_JUNTA.search(str(w.get("id") or "")):
            ev.append(f"canon {w.get('id')}: id junta dos walls / ejes")
        for k in ("facade", "elevation", "axis", "grid", "grid_line"):
            if RX_DOS_FACHADAS.search(str(w.get(k) or "")) or (isinstance(w.get(k), list) and len(w[k]) > 1):
                ev.append(f"canon {w.get('id')}.{k} = '{w.get(k)}': dos ejes / fachadas en un wall")
        if isinstance(w.get("bands"), list) and len({(x or {}).get("ori") for x in w["bands"]}) > 1:
            ev.append(f"canon {w.get('id')}: bands en dos orientaciones (dos ejes en un número)")
    for a in b.annots or []:
        # v81cf28 (BE-CF21): keynotes y notas ('KN3 + KN4', 'A.6 + H.2', 'G.3 / H.1') citan la FUENTE de un wall, no juntan walls
        # el Wall ID es el ÚLTIMO campo del Contents ('... · DETAIL N/HOJA · <Wall ID>'): los campos de fuente / detalle citan
        # hojas y notas ('A-202 + A-622', 'KN3 + KN4') y no juntan walls
        _cid = str(a.get("contents") or "").split("|")[0].split("·")[-1]
        if RX_JUNTA.search(RX_NOTA_REF.sub(" ", _cid) + " " + str(a.get("subject") or "")) and \
                re.search(r"(?i)\bLF\b", str(a.get("contents") or "")):
            ev.append(f"markup {a.get('label')}: '{str(a.get('contents'))[:50]}' junta dos walls")
        vs = a.get("verts") or []
        if str(a.get("tipo") or "") in ("PolyLine", "Line") and len(vs) >= 3 and not re.search(r"(?i)\bcurv|\barc\b|radius",
                                                                                                str(a.get("contents") or "")):
            g = _giro_max(vs)
            if g > 60:
                ev.append(f"markup {a.get('label')} '{str(a.get('contents'))[:40]}': polilínea dobla {g:.0f}° (dos ejes en un markup)")
    return R("FAIL", *ev[:25]) if ev else R("PASS", "un eje / fachada por número")


@chk("U-121", desc="U-121 (día 1, FORMATO de markups): todo markup de wall / demo (PolyLine) con Subject, Page Label = número "
     "de hoja, /Measure (Length), /Depth = altura (> 0) y por lo tanto Wall Area = Length x Depth en Bluebeam")
def u_121(b):
    """U-121: campos de Bluebeam en cada markup."""
    if b.annots is None:
        return SIN("PDF de markups")
    ws = [a for a in b.annots if str(a.get("tipo") or "PolyLine") in ("PolyLine", "Line")
          and not str(a.get("nm") or "").startswith("TO-LEGEND-") and "LEGEND" not in str(a.get("subject") or "").upper()]
    if not ws:
        return R("FAIL", "el PDF de markups no trae ningún markup de wall (PolyLine)")
    ev = []
    for a in ws:
        falta = []
        if not str(a.get("subject") or "").strip():
            falta.append("Subject")
        if not re.match(r"^[A-Z]{1,3}-?\d{1,3}(?:\.(?:\d{1,2}|[A-Z]))?[A-Z]?$", str(a.get("label") or "")):   # R80f.38: A421.A
            falta.append(f"Page Label (= '{a.get('label')}')")
        if not a.get("measure"):
            falta.append("/Measure (Length)")
        d = _n(a.get("depth"))
        if not d or d <= 0:
            falta.append("/Depth (altura -> Wall Area)")
        if falta:
            ev.append(f"{a.get('label')} '{str(a.get('contents') or a.get('subject'))[:40]}': falta " + ", ".join(falta))
    return R("FAIL", f"{len(ev)} de {len(ws)} markups sin campos de Bluebeam", *ev[:25]) if ev else \
        R("PASS", f"{len(ws)} markups con Subject, Page Label, Length, Depth y Wall Area")


@chk("U-125", desc="U-125 (día 1): términos del trade siempre en inglés, nunca traducidos ('tablaroca', 'panel de yeso', "
     "'poste metálico', 'canal', 'riel', 'montante'…) en Excel, README, PARA_REVISAR, SEGUIMIENTO y markups")
def u_125(b):
    """U-125: términos del trade en inglés también en los textos en español."""
    textos = [(f"{h}!{c}", t) for h, c, t in b.celdas] + [(n, t) for n, t in b.docs.items()] + \
             [(f"markup {a.get('label')}", a.get("contents") or "") for a in (b.annots or [])]
    if not textos:
        return SIN("Excel / documentos / markups")
    ev = []
    for et, t in textos:
        for i, l in enumerate(str(t).splitlines() or [""], 1):
            m = TRADE_ES.search(l)
            if m:
                ev.append(f"{et}{(' línea ' + str(i)) if '!' not in et else ''}: '{m.group(0)}' (término del trade traducido)")
    return R("FAIL", *ev[:25]) if ev else R("PASS", "términos del trade en inglés")


# ---------------------------------------------------------------------------------------------- U-127 BOTH SIDES
RX_LINER = re.compile(r"(?i)liner|shaft ?wall|shaftliner")
RX_NHOJA_MOTIVO = re.compile(r"\b[0-9A-Z]{1,3}/[A-Z]{1,3}-?\d{1,4}(?:\.[0-9A-Z]{1,2})?\b|\b[A-Z]{1,2}-?\d{3}(?:\.[A-Z0-9]{1,2})?\b")


@chk("U-127", "BE-138", desc="U-127 / BE-138 (BOTH SIDES): cada wall de un type cuyo schedule / sección imprime board en las dos "
     "caras lleva board en sus DOS caras, con las capas por cara que imprime el type (lectura independiente fichas.json, "
     "BE-122); cara o capa faltante = FAIL; una cara sin board solo con board_none_reason que cite N/HOJA = AMBER")
def both_sides(b):
    """U-127: caras con board y capas por cara = schedule (fichas.json), por wall."""
    import revision_materiales as RV
    fj = b.fichas
    walls = [w for w in b.walls() if str(w.get("element") or "wall") == "wall"]
    if not walls:
        return NA("sin walls en el canon")
    if not (isinstance(fj, dict) and isinstance(fj.get("types"), dict) and fj["types"]):
        return R("FAIL", "sin fichas.json (lectura independiente del Partition Type Schedule, BE-122): no se puede probar BOTH SIDES")
    cw = {w["id"]: w for w in b.walls() if w.get("id")}
    misc = b.canon.get("misc_items") or []
    ev, amb, n = [], [], 0
    for w in walls:
        f = fj["types"].get(str(w.get("tag") or ""))
        if not isinstance(f, dict):         # clave del schedule cargada con otro nombre (entrega.json mapa_materiales)
            k = next((k for k, v in (b.mapa_materiales or {}).items() if k in fj["types"] and
                      (w.get("id") in (v if isinstance(v, list) else str(v).split(",")) or
                       str(w.get("tag")) in (v if isinstance(v, list) else str(v).split(",")))), None)
            f = fj["types"].get(k) if k else None
        if not isinstance(f, dict):
            # BE-CR29: tag con una fila de rating que el schedule no imprime (XW.6.6 | 0 con filas -1 / -2): la construcción de la familia
            # (fila de menor rating) define las caras; saltar el wall dejaba BOTH SIDES ciego
            fam = re.sub(r"-\d+$", "", str(w.get("tag") or ""))
            filas = sorted(k for k in fj["types"] if re.sub(r"-\d+$", "", k) == fam)
            f = fj["types"].get(filas[0]) if fam and filas else None
        if not isinstance(f, dict):
            continue
        todas = [x for x in f.get("faces") or [] if isinstance(x, dict)]
        caras = [x for x in todas if x.get("board") and not RV.NO_IMPRESO.search(str(x.get("board")))]
        if not caras:
            continue
        n_sch = RV._lados(todas)
        lays = [int(x["layers"]) for x in caras if str(x.get("layers") or "").isdigit() and not RX_LINER.search(str(x.get("board")))] or \
               [int(x["layers"]) for x in caras if str(x.get("layers") or "").isdigit()]
        lay = max(lays) if lays else None
        fc = [x for x in RV._caras_wall(w["id"], cw, misc) if str(x.get("side") or "").upper() != "END"]
        lados = {str(x.get("side")) for x in fc}
        n += 1
        src = (f.get("sources") or {}).get("board", "")
        if len(lados) < n_sch:
            mot = " ".join(str(x.get("board_none_reason") or "") for x in w.get("faces") or []) + " " + str(w.get("faces_none_reason") or "")
            msg = f"{w['id']} ({w.get('tag')}): {len(lados)} cara(s) con board; el type imprime {n_sch} ({src})"
            (amb if RX_NHOJA_MOTIVO.search(mot) else ev).append(msg + (f" - motivo: {mot.strip()[:80]}" if mot.strip() else ""))
        if lay:
            def _clase(t):
                t = str(t)
                return "LINER" if RX_LINER.search(t) else ("EXT" if re.search(r"(?i)exterior|sheathing|glass ?mat", t) else "INT")
            por_clase = {}
            for x in caras:
                if str(x.get("layers") or "").isdigit():
                    por_clase[_clase(x.get("board"))] = max(por_clase.get(_clase(x.get("board")), 0), int(x["layers"]))
            for x in fc:
                # BE-CR25: la cara shaft-side (1" liner panel) / exterior (sheathing) se compara con la cara de su misma clase
                # en el schedule, no con el room side
                cl = {_clase(y) for y in (x.get("boards") or [x.get("board")])}
                cl = "LINER" if "LINER" in cl else ("EXT" if cl == {"EXT"} else "INT")
                obj = por_clase.get(cl) or lay
                if int(x.get("layers") or 1) < obj:
                    ev.append(f"{w['id']} cara {x.get('side')}: {x.get('layers') or 1} capa(s); el type imprime {obj} ({src})")
    if ev:
        return R("FAIL", f"{len(ev)} falta(s) de cara / capa en {n} walls con board impreso", *ev[:30])
    if amb:
        return R("AMBER", *amb[:20])
    return R("PASS", f"{n} walls: caras y capas = schedule") if n else NA("ningún wall de un type con board impreso en fichas.json")


# R80f.43 (Chuze FINAL7, auditoría adversarial U-138, BE-141): las cifras escritas en el Scope Checklist / Inputs / README
# (board por tipo, SF de existing walls) son las del Material Summary / bloque EXISTING del MISMO
# Excel. Una cifra tecleada que quedó vieja después de un recálculo = FAIL. plantilla_excel.resolver_cifras las escribe por
# programa ({{MS:<renglón>}} / {{EX:board_sf}}); esta tabla las vuelve a leer en el texto entregado.
CIFRAS_TEXTO = [
    (r'5/8" (?:gypsum board, )?Type X MR ([\d,]+\.\d+) SF', '5/8" gypsum board, Type X MR'),
    (r'5/8" (?:gypsum board, )?MR ([\d,]+\.\d+) SF', '5/8" gypsum board, Type X MR'),
    (r'5/8" (?:gypsum board, )?Type X ([\d,]+\.\d+) SF', '=5/8" gypsum board, Type X'),
    (r'Type X W\.R\.(?: / DensArmor Plus)? ([\d,]+\.\d+) SF', '5/8" gypsum board, Type X W.R.'),
    (r'cement backer board behind tile ([\d,]+\.\d+) SF', '5/8" cement backer'),
    (r'studs 6" ([\d,]+\.\d+) LF', '6" metal stud'),
    (r'studs 6" [\d,]+\.\d+ LF, 3-5/8" ([\d,]+\.\d+) LF', '3-5/8" metal stud'),
    (r'3-5/8" [\d,]+\.\d+ LF, 2-1/2" ([\d,]+\.\d+) LF', '2-1/2" stud'),
    (r'(?i)(?<!" )\bbottom track ([\d,]+\.\d+) LF', 'Bottom track'),    # '2-1/2" bottom track' = un renglón, no el total
    (r'(?i)(?<!" )\btop track ([\d,]+\.\d+) LF', 'Top'),
    (r'(?i)bracing 1-1/2" C\.R\. channel ([\d,]+\.\d+) LF', 'Bracing 1-1/2" C.R. channel'),
    (r'(?i)\bhanger wire ([\d,]+\.\d+) LF', '=Hanger wire'),
    (r'(?i)ceiling / soffit track ([\d,]+\.\d+) LF', 'Ceiling / soffit track'),
    (r'(?i)\bcontrol joints ([\d,]+\.\d+) LF', 'Control joint'),
    (r'(?i)\bmetal trim ([\d,]+\.\d+) LF', 'METAL trim'),
    (r'HD8906 main tee ([\d,]+\.\d+) LF', 'Armstrong HD8906'),
    (r'XL8945P cross tee ([\d,]+\.\d+) LF', 'Armstrong XL8945P'),
    (r'KAM151220E angle molding ([\d,]+\.\d+) LF', 'Armstrong KAM151220E'),
    (r'SC151220EQ curved molding ([\d,]+\.\d+) LF', 'Armstrong SC151220EQ'),
    (r'([\d,]+\.\d+) SF in the Material Summary row .Demolition', 'Demolition'),
    (r'10/A505\.B horizontal studs = ([\d,]+\.\d+) LF', 'Metal stud blocking'),
    (r'([\d,]+\.\d+) SF inside the Type X row', 'EX:'),
]


def cifras_texto_err(textos, ms, ex_sf=None):
    """textos [(dónde, texto)], ms [(material, net)], ex_sf = suma Board (SF) de los renglones EX- -> [errores]."""
    err = []
    for donde, t in textos:
        for rx, sel in CIFRAS_TEXTO:
            for m in re.finditer(rx, str(t or "")):
                v = float(m.group(1).replace(",", ""))
                if sel == "EX:":
                    real, nom = ex_sf, "suma Board (SF) de los renglones EX- (EXISTING WALLS TO REMAIN)"
                else:
                    ok = (lambda n: n == sel[1:]) if sel.startswith("=") else (lambda n: n.startswith(sel))
                    vs = [float(n_ or 0) for x, n_ in ms if ok(str(x))]
                    real, nom = (sum(vs) if vs else None), f"Material Summary '{sel.lstrip('=')}'"
                if real is None:
                    continue
                if abs(v - real) > 0.005:
                    err.append(f"{donde}: '{m.group(0)[:70]}' = {v:,.2f} pero {nom} = {real:,.2f} (cifra tecleada vieja; "
                               "escribirla por programa {{MS:...}} / {{EX:board_sf}})")
    return err


@chk("BE-141", "U-138", desc="BE-141 (Chuze FINAL7 auditoría U-138): toda cifra de material escrita en el Scope Checklist / Inputs / "
     "README = su renglón del Material Summary (o la suma de los renglones EX-) del Excel entregado")
def cifras_texto(b):
    if not b.ms:
        return SIN("Excel (Material Summary)")
    ms = [(x["material"], x["net"]) for x in b.ms]
    ex = [x["board"] or 0 for x in b.pt if str(x.get("wall") or "").startswith("EX-")]
    tx = [(f"{h}!{c}", t) for h, c, t in b.celdas if h in ("Scope Checklist", "Inputs")]
    tx += [(k, v) for k, v in (b.docs or {}).items() if k.upper().startswith("README")]
    ev = cifras_texto_err(tx, ms, sum(ex) if ex else None)
    return R("FAIL", f"{len(ev)} cifra(s) de texto distintas del Material Summary", *ev[:25]) if ev else \
        R("PASS", "cifras del Scope Checklist / Inputs / README = Material Summary")


# BE-CR30 (CR City Hotel rev3, el usuario: "revisa los rcp por que creo que hay algunas areas que no tomaste en cuenta"): campos de
# gypsum tagueados en los RCP ampliados (BAR, franja del lobby, Cleaning 215) no tenían renglón. Cada tag de ceiling de gypsum impreso en
# una hoja de RCP (GYP-n / GWB-n / GB-n, no la leyenda 'GYP-n:') = un renglón cargado del canon o none_reason con N/HOJA.
RX_TAG_GYP = re.compile(r"\b(?:GYP|GWB|GB)-\d{1,2}\b(?!\s*:)")
PREF_CLG = ("GYP", "GWB", "GB", "FS", "RS", "ACT", "WS", "MB", "CLG", "SOF")   # v81cf104: todo tag de cielo, no solo gypsum
RX_PLAN_RCP = re.compile(r"(?i)(?<!RE:\s)REFLECTED\s+CEILING\s+PLAN(?!S)|ENLARGED\s+RCP|\bRCP\s*[-–]\s*\w|\bRCP\s+(?:LEVEL|LVL|L\d)")   # 'RE: REFLECTED CEILING PLANS' (nota) no   # plano RCP (no un schedule de assemblies)
RX_LEYENDA_CLG = re.compile(r"(?i)CEILING\s+(?:LEGEND|TYPES?)|FLOOR\s*/\s*CEILING\s+ASSEMBL")


def tags_cielo(t):
    """v81cf104 / U-189: {tag: veces impreso como instancia} en el texto de una hoja RCP. Prefijos = PREF_CLG + los que define la
    leyenda de cielos de la hoja ('XX-n:' después de 'CEILING LEGEND / TYPES'); la definición de la leyenda ('ACT-1: …') no cuenta."""
    t = t if isinstance(t, str) else str(t or "")
    pref = set(PREF_CLG)
    for m in RX_LEYENDA_CLG.finditer(t):
        pref |= {x.upper() for x in re.findall(r"\b([A-Z]{2,4})-\d{1,2}\s*:", t[m.end():m.end() + 3000])}
    out = {}
    for m in re.finditer(r"\b([A-Z]{2,4})-(\d{1,2})\b(?!\s*:)", t):
        if m.group(1) in pref:
            k = f"{m.group(1)}-{m.group(2)}"
            out[k] = out.get(k, 0) + 1
    return out
RX_HOJA_RCP = re.compile(r"(?i)REFLECTED CEILING|\bRCP\b")


@chk("BE-CR30", "U-124", desc="BE-CR30 / U-124 / U-189 (v81cf104): cada tag de cielo impreso en una hoja de RCP (GYP / FS / RS / ACT / WS / MB y todo prefijo de la leyenda de la hoja; la definición de la leyenda no cuenta) tiene su "
     "renglón cargado (ceilings[] / misc '... board') o none_reason con N/HOJA; rcp_tags del canon cuenta lo mismo que el texto de cada hoja")
def rcp_tags(b):
    imp, por_tag = {}, {}
    for h, t in (b.hojas or {}).items():
        t = t if isinstance(t, str) else str(t or "")
        if RX_HOJA_RCP.search(t):
            tc = tags_cielo(t) if RX_PLAN_RCP.search(t) else {k: v for k, v in tags_cielo(t).items() if RX_TAG_GYP.match(k)}   # v81cf104
            if tc:
                imp[h] = sum(tc.values())
                por_tag[h] = tc
    if not imp:
        return NA("ninguna hoja de RCP con tags de cielo impresos")
    tg = b.canon.get("rcp_tags") or []
    if not tg:
        return R("FAIL", f"{sum(imp.values())} tags de gypsum impresos en {len(imp)} hojas de RCP ({', '.join(sorted(imp))}) y el canon no trae "
                         "rcp_tags: barrer tag por tag y dar a cada uno su renglón o su motivo N/HOJA")
    misc = {str(m.get("ref")) for m in b.canon.get("misc_items") or []}
    nce = len(b.canon.get("ceilings") or [])
    err = []
    cnt = {}
    for x in tg:
        cnt[x.get("sheet")] = cnt.get(x.get("sheet"), 0) + 1
    cnt_t = {}
    for x in tg:
        k = (x.get("sheet"), re.sub(r"\s+", "", str(x.get("tag") or "")).upper())
        cnt_t[k] = cnt_t.get(k, 0) + 1
    for h, tc in sorted(por_tag.items()):
        for tag, n in sorted(tc.items()):
            if cnt_t.get((h, tag), 0) < n:
                err.append(f"{h}: {tag} impreso {n} vez/veces y {cnt_t.get((h, tag), 0)} en rcp_tags: tag de cielo sin renglón ni motivo (barrido incompleto, U-189)")
    for x in tg:
        rows = x.get("rows") or []
        malos = [r for r in rows if r not in misc and not (re.match(r"ceilings\[(\d+)\]", str(r)) and int(re.match(r"ceilings\[(\d+)\]", str(r)).group(1)) < nce)]
        donde = f"{x.get('sheet')} {x.get('tag')} {x.get('height') or ''} @ {x.get('xy')}"
        if rows and malos:
            err.append(f"{donde}: renglón citado que no está en el canon: {malos[:3]}")
        elif not rows and not RX_NHOJA_MOTIVO.search(str(x.get("none_reason") or "")):
            err.append(f"{donde}: sin renglón cargado ni none_reason con N/HOJA")
    if err:
        return R("FAIL", f"{len(err)} tag(s) de RCP sin cubrir", *err[:25])
    exc = sum(1 for x in tg if not x.get("rows"))
    return R("PASS", f"{len(tg)} tags de gypsum en {len(imp)} hojas de RCP: {len(tg) - exc} con renglón, {exc} con motivo N/HOJA")


def faltante_por_tag(canon, sheet, tag, height):
    """BE-CR40 (CR rev20, 12-nov: se reportó como faltante un cielo que estaba cargado porque se buscó TEXTO en el JSON del canon, con la
    comilla escapada): un cielo se declara faltante SOLO buscando por hoja / tag / altura en canon.rcp_tags (rows existentes o
    none_reason), nunca por texto libre. -> (faltante: bool, motivo)"""
    refs = {str(m.get("ref")) for m in canon.get("misc_items") or []}
    nce = len(canon.get("ceilings") or [])
    norm = lambda h: re.sub(r"\s+", "", str(h))                                   # noqa: E731
    xs = [x for x in canon.get("rcp_tags") or [] if x.get("sheet") == sheet and x.get("tag") == tag and norm(x.get("height")) == norm(height)]
    if not xs:
        return True, "tag sin entrada en rcp_tags (barrido incompleto)"
    for x in xs:
        if str(x.get("none_reason") or "").strip():
            return False, "none_reason: " + x["none_reason"]
        ok = [r for r in x.get("rows") or [] if r in refs or (re.match(r"ceilings\[(\d+)\]", r) and int(re.match(r"ceilings\[(\d+)\]", r).group(1)) < nce)]
        if ok:
            return False, "cargado en " + ", ".join(ok)
    return True, "rows del tag no existen en el canon"


RX_HALLAZGO_FALTA = re.compile(r"(?i)\b(?:falta|faltante|missing|not loaded|no cargad[oa]|sin renglón|no está cargad[oa]|not\s+included|"
                               r"not\s+in\s+(?:the\s+)?(?:canon|take-?off|estimate)|omitted|no\s+incluid[oa])\b")
RX_TAG_CIELO_H = re.compile(r"\b((?:GYP|FS|RS|ACT|WS|MB|CLG)-?\d+[A-Z]?)\b")
RX_HOJA_H = re.compile(r"\b([A-Z]{1,2}-?\d{1,2}\.\d{1,2}|[A-Z]{1,2}-?\d{3})\b")
RX_ALTURA_H = re.compile(r"(\d{1,2}'\s*-?\s*\d{1,2}(?:\s+\d/\d)?(?:\.\d+)?\"?)")


@chk("BE-CR40", desc="BE-CR40 (CR rev20: un cielo cargado se declaró faltante buscando texto en el JSON): todo hallazgo de cielo faltante de "
     "cualquier .md de Auditoria/ se resuelve AQUÍ contra el canon (faltante_por_tag por hoja / tag / altura; sin tag, por número de "
     "cuarto); el texto 'faltante_por_tag:' del renglón no es prueba; cargado declarado faltante = FAIL; sin forma de resolverlo = FAIL; "
     "v121: solo 'CERRADO: <ref> (<N/HOJA>)' con la ref cargada (cantidad > 0) cierra; DOBLE_CIELO.csv solo con refs upper / lower cargadas")
def faltantes_auditoria(b):
    """BE-CR40 (+ verificación 12b): todo hallazgo de cielo faltante de CUALQUIER .md de Auditoria/ (y de los informes / auditorías) se
    resuelve contra el canon llamando a faltante_por_tag; el texto 'faltante_por_tag: …' del renglón NO es prueba. Sin tag: por número de
    cuarto contra ceilings / misc del canon. Lo que no se puede resolver = FAIL (no N/A); algo cargado declarado faltante = FAIL."""
    ev, n, ok = [], 0, 0
    canon = b.canon or {}
    dc = cuartos_doble_cielo(b)                          # v120 (GK H-04): cuartos ya cubiertos en Auditoria/DOBLE_CIELO.csv
    for k, t in sorted((b.textos or {}).items()):
        if not (re.search(r"(?i)AUDITORIA|INFORME|revision_independiente|auditoria_U138", k) and k.lower().endswith((".md", ".txt"))):
            continue
        if re.match(r"(?i)(?:BRIEF|LEEME|README)", os.path.basename(k)):   # v121 (CR): instrucciones de los revisores, no hallazgos
            continue
        for ln in t.splitlines():
            tg = RX_TAG_CIELO_H.search(ln)
            if not (RX_HALLAZGO_FALTA.search(ln) and (tg or RX_CIELO_PALABRA.search(ln))):
                continue
            if not es_hallazgo_concreto(ln):            # v121 (CR): definición de categoría ('- FALTA — a wall / ceiling …') no es hallazgo
                continue
            if RX_HOJA_FALTANTE.search(ln) and not RX_PALABRA_CIELO_V121.search(ln):   # v121: 'N/HOJA (missing)' sin palabra de cielo = HOJA
                continue
            n += 1
            nom, txt = os.path.basename(k), ln.strip()[:100]
            cex = RX_CERRADO_EXCL.search(ln)
            if cex:                                      # v121 (GK H-04): 'CERRADO: EXCLUDED - <motivo impreso> (<N/HOJA>)'
                if len(cex.group(1).strip(" -—–:")) >= 3 and cex.group(2):
                    ok += 1
                else:
                    ev.append(f"{nom}: '{txt}' cierra como EXCLUDED sin motivo impreso o sin (N/HOJA) (BE-CR40)")
                continue
            cie = RX_CERRADO_V121.search(ln)
            if cie:                                      # v121: SOLO 'CERRADO: <ref> (<N/HOJA>)' cierra; la ref con cantidad > 0
                ref, nh = cie.group(1), cie.group(2)
                if _cant_ref(canon, ref) > 0 and nh:
                    ok += 1
                    continue
                ev.append(f"{nom}: '{txt}' cierra con '{cie.group(0).strip()}': " + ("la ref no está en el canon con cantidad > 0"
                          if _cant_ref(canon, ref) <= 0 else "falta el N/HOJA entre paréntesis") + " (BE-CR40)")
                continue
            cs = {m.group(1) for m in RX_CUARTO_H.finditer(RX_HOJA_H.sub(" ", ln))}
            if cs and dc and cs <= dc:                   # todos los cuartos del renglón están en DOBLE_CIELO.csv: resuelto por la tabla
                ok += 1
                continue
            # v121 (GK H-04): cuarto por cuarto; los resueltos por DOBLE_CIELO.csv (cargados o EXCLUDED) no se vuelven a buscar
            falta, motivo = resolver_faltante(canon, ln, cuartos=(cs - dc) if cs and dc and not tg else None)
            if falta is None:
                ev.append(f"{nom}: '{txt}' declara un cielo faltante que no se puede resolver contra el canon ({motivo}); escribir hoja + "
                          "tag + altura o el número de cuarto (BE-CR40)")
            elif not falta:
                ev.append(f"{nom}: '{txt}' declara faltante algo CARGADO ({motivo}; si se corrigió después, el renglón cita la ref que "
                          "lo cargó; BE-CR40)")
            else:
                ok += 1
    if not n:
        return NA("sin hallazgos de cielo faltante en los .md de Auditoria/")
    return R("FAIL", *ev[:20]) if ev else R("PASS", f"{ok} hallazgo(s) de cielo faltante verificados contra el canon (faltante_por_tag / cuarto)")


RX_REF_CANON = re.compile(r"\b([A-Z][A-Z0-9]{1,5}-[A-Z0-9][\w.]*(?:-[\w.]+)*)")      # v120: cualquier ref (EXT-, SOF-, CLG-, BW-, misc…)
RX_HOJA_FALTANTE = re.compile(r"(?i)\b\d{1,2}/[A-Z]{1,2}-?\d{1,3}(?:\.\d{1,2})?\s*\(?\s*(?:missing|falta(?:nte)?|not\s+(?:in|included)|"
                              r"no\s+est[aá])|\b(?:sheet|hoja|drawing|dibujo|plano)\s+[A-Z]{1,2}-?\d{1,3}(?:\.\d{1,2})?\s+(?:is\s+)?(?:missing|falta)")


def cuartos_doble_cielo(b):
    """v120 (GK H-04) / v121: números de cuarto de Auditoria/DOBLE_CIELO.csv (columna Room) cuyo 'upper: …' Y 'lower: …' citan cada uno
    una ref que EXISTE en el canon con cantidad > 0 (ref de renglón, ceilings[N] o [N] = ceilings[N]). 'GYP-9 MISSING', '(none)' o una
    ref que no existe = el cuarto NO queda resuelto."""
    import csv as _csv
    import io as _io
    canon = b.canon or {}
    out = set()
    for k, t in (b.textos or {}).items():
        if os.path.basename(k) != "DOBLE_CIELO.csv":
            continue
        for r in _csv.DictReader(_io.StringIO(t.lstrip("\ufeff"))):
            room = str(r.get("Room") or r.get("room") or "")
            fila = str(r.get("Row / reason") or r.get("row") or "")
            segs = {m.group(1).lower(): m.group(2) for m in re.finditer(r"(?i)\b(upper|lower)\s*:\s*([^;|]*)", fila)}
            nh = str(r.get("N/SHEET") or r.get("N/HOJA") or "") + " " + fila
            excl = bool(re.search(r"(?i)\bEXCLUDED\b", fila) and RX_NH_CB.search(nh))   # v121 (GK H-04): EXCLUDED + N/HOJA, cualquier fila
            if excl or all(_seg_cargado(canon, segs.get(lado, "")) for lado in ("upper", "lower")):
                out |= {m.group(1) for m in RX_CUARTO_H.finditer(RX_HOJA_H.sub(" ", room))}
    return out


def _seg_cargado(canon, seg):
    """v121: el segmento 'upper: …' / 'lower: …' cita al menos una ref con cantidad > 0 y no dice missing / none / falta."""
    if not seg.strip() or re.search(r"(?i)\b(?:missing|none|falta\w*|n/?a|not\s+loaded|does\s+not\s+exist|no\s+existe)\b", seg):
        return False
    refs = [r for r in RX_REF_CANON.findall(seg) if not RX_TAG_CIELO_H.fullmatch(r)]
    refs += ["ceilings[%s]" % m.group(1) for m in re.finditer(r"(?:ceilings)?\[(\d+)\]", seg)]
    return any(_cant_ref(canon, r) > 0 for r in refs)


def _cant_ref(canon, ref):
    """v121 (BE-CR40): cantidad cargada de la ref en el canon (0 si no existe). ceilings[N] = area_sf; misc 'ref' o 'ref <cara>' = qty;
    walls / trim / blocking / soffits = length_ft / lf / qty / quantities."""
    ref = str(ref).strip()
    m = re.fullmatch(r"ceilings\[(\d+)\]", ref)
    if m:
        cs = canon.get("ceilings") or []
        i = int(m.group(1))
        return float((cs[i] or {}).get("area_sf") or 0) if i < len(cs) and isinstance(cs[i], dict) else 0.0
    tot = 0.0

    def num(x):
        try:
            return float(x)
        except (TypeError, ValueError):
            return 0.0
    for lst in ("walls", "existing_walls", "trim_items", "blocking_items", "framed_soffits", "ceilings"):
        for x in canon.get(lst) or []:
            if isinstance(x, dict) and ref in (str(x.get("id") or ""), str(x.get("ref") or "")):
                q = max(num(x.get(c)) for c in ("qty", "area_sf", "lf", "length_ft", "sf", "pcs"))
                if isinstance(x.get("quantities"), dict):
                    q = max([q] + [num(v) for v in x["quantities"].values()])
                tot += q
    for x in canon.get("misc_items") or []:
        r = str(x.get("ref") or "") if isinstance(x, dict) else ""
        if r == ref or r.startswith(ref + " "):
            tot += num(x.get("qty"))
    return tot


RX_CERRADO_V121 = re.compile(r"(?i)\b(?:CERRADO|CLOSED)\s*:\s*([A-Za-z][\w.]*-[\w.\-]+|ceilings\[\d+\])\s*"
                             r"(?:\(\s*(\d{1,2}/[A-Z]{1,2}-?\d{1,3}(?:\.\d{1,2})?)\s*\))?")
RX_NH_CB = re.compile(r"\b\d{1,2}[A-Z]?/[A-Z]{1,2}-?\d{1,3}(?:\.\d{1,2})?\b")
RX_CERRADO_EXCL = re.compile(r"(?i)\b(?:CERRADO|CLOSED)\s*:\s*EXCLUDED\b\s*[-—–:]?\s*([^()|]*?)\s*(?:\(\s*(\d{1,2}[A-Z]?/[A-Z]{1,2}-?\d{1,3}"
                             r"(?:\.\d{1,2})?)\s*\))?(?=\s*(?:\||$))")


def es_hallazgo_concreto(ln):
    """v121 (CR): un hallazgo nombra un cuarto (número), un tag de cielo o una ref concreta; una definición de categoría ('- FALTA — a wall
    / ceiling in OUR scope … that is not loaded') no."""
    sin_hojas = RX_HOJA_H.sub(" ", ln)
    return bool(RX_CUARTO_H.search(sin_hojas) or RX_TAG_CIELO_H.search(ln) or RX_HOJA_H.search(ln)
                or [r for r in RX_REF_CANON.findall(ln) if not RX_TAG_CIELO_H.fullmatch(r)])


RX_PALABRA_CIELO_V121 = re.compile(r"(?i)\b(?:ceilings?|cielos?|clg|gyp-?\d+[a-z]?|soffits?|plafond)\b")


RX_REF_CIERRE = re.compile(r"\b((?:CLG|SOF|BW|CW)-[A-Z0-9]+(?:-[A-Z0-9]+)+)\b")    # ref de renglón del canon (no un tag GYP-1)


def _ref_cargada(canon, ref):
    """v120 (GK): la ref existe CARGADA en el canon: misc_items (ref o 'ref <cara>' con qty > 0), ceilings (ref / id con área), walls /
    existing_walls / trim / blocking (id o ref)."""
    for lst in ("walls", "existing_walls", "trim_items", "blocking_items", "framed_soffits"):
        for x in canon.get(lst) or []:
            if isinstance(x, dict) and ref in (str(x.get("id") or ""), str(x.get("ref") or "")):
                return True
    for m in canon.get("misc_items") or []:
        r = str(m.get("ref") or "") if isinstance(m, dict) else ""
        if (r == ref or r.startswith(ref + " ")) and float(m.get("qty") or 0) > 0:
            return True
    return any(isinstance(x, dict) and ref in (str(x.get("ref") or ""), str(x.get("id") or "")) and float(x.get("area_sf") or 0) > 0
               for x in canon.get("ceilings") or [])


RX_CIELO_PALABRA = re.compile(r"(?i)\b(?:ceilings?|cielos?|clg|soffits?|plafond)\b")
RX_CUARTO_H = re.compile(r"(?<![\w.'/-])(\d{3,4}[A-Z]?)(?![\w.'\"/-])")


def resolver_faltante(canon, ln, cuartos=None):
    """BE-CR40: -> (True = de verdad falta | False = está cargado | None = no se puede resolver, motivo). Con tag: faltante_por_tag con
    hoja / altura del renglón; si faltan, cada entrada de rcp_tags con ese tag (y hoja si la trae) — una cargada = no se puede afirmar
    'falta'. Sin tag: número de cuarto contra canon.ceilings (room) y misc_items de cielo (ref CLG / SOF con el cuarto en ref / source)."""
    tg, hj, al = RX_TAG_CIELO_H.search(ln), RX_HOJA_H.search(ln), RX_ALTURA_H.search(ln)
    if tg:
        tag = tg.group(1)
        if hj and al:
            return faltante_por_tag(canon, hj.group(1), tag, al.group(1))
        cands = [x for x in canon.get("rcp_tags") or [] if x.get("tag") == tag and (not hj or x.get("sheet") == hj.group(1))]
        if not cands:
            return True, f"{tag} sin entrada en rcp_tags"
        res = [faltante_por_tag(canon, x.get("sheet"), tag, x.get("height")) for x in cands]
        if all(f for f, _m in res):
            return True, f"{len(res)} entrada(s) de {tag} sin renglón cargado"
        if len(res) == 1:
            return res[0]
        return None, f"{tag} tiene {len(res)} entradas en rcp_tags y {sum(1 for f, _m in res if not f)} están cargadas"
    sin_hojas = RX_HOJA_H.sub(" ", ln)
    cuartos = set(cuartos) if cuartos else {m.group(1) for m in RX_CUARTO_H.finditer(sin_hojas)}
    if not cuartos:
        return None, "sin tag de cielo ni número de cuarto"
    sof = bool(re.search(r"(?i)\bsoffits?\b|\bSOF-", ln))           # v121: un soffit no es el cielo del cuarto (y al revés)
    cie = bool(re.search(r"(?i)\b(?:ceilings?|cielos?|clg|plafond)\b", ln)) or not sof
    pref = "|".join((["CLG"] if cie else []) + (["SOF"] if sof else []))
    for c in sorted(cuartos):
        rx = re.compile(rf"(?<![\w.]){re.escape(c)}(?![\w])")
        cargados = [f"ceilings[{i}]" for i, x in enumerate(canon.get("ceilings") or [])
                    if isinstance(x, dict) and rx.search(str(x.get("room") or "")) and float(x.get("area_sf") or x.get("qty") or 0) > 0]
        cargados += [str(m.get("ref")) for m in canon.get("misc_items") or [] if isinstance(m, dict)
                     and re.match(rf"(?i)({pref})", str(m.get("ref") or "")) and float(m.get("qty") or 0) > 0
                     and (rx.search(str(m.get("ref") or "")) or rx.search(str(m.get("source") or "")))]
        if cargados:
            return False, f"cuarto {c} cargado en " + ", ".join(cargados[:4])
    return True, "cuarto(s) " + ", ".join(sorted(cuartos)) + " sin cielo en el canon"


RX_REF_EXT = re.compile(r"(?i:\bper\s+(?:the\s+)?(?:assembly|UL\b|manufacturer|mfr\.?)|\bsee\s+spec(?:ification)?s?\b)"
                        r"|\b(?:UL|U\.L\.)\s*(?:[Dd]esign\s*)?[A-Z]?\d{3}\b|\bGA[- ](?:[Ff]ile\s*)?(?:[Nn]o\.?\s*)?[A-Z]{0,3}\s?\d{3,}")   # GA solo en mayúsculas
RX_CITA_ITEM = re.compile(r"(?i)\bitem\s*\d+|\bpara(?:graph)?\.?\s*\d|§\s*\d|\bsection\s*\d|\bpart\s*\d|\bart(?:icle)?\.?\s*\d|\b\d{2}\s\d{2}\s\d{2}(?:\.\d+)?\s*[-–]?\s*\d|\btable\s*\d|\bfig(?:ure)?\.?\s*\d")
RX_UL_SUELTO = re.compile(r"(?<![\w./-])[LUV]\d{3}(?![\w./-]|\.\d)")    # BE-AUD05: 'L546' sin 'UL' delante también es un listing UL
RX_UL_ITEM = re.compile(r"(?i)\bitem\s*\d+")
RX_RC_CTX = re.compile(r"(?i)\bresilient|\bRC\b|\bfurring\b|\bhat\s+channel|\bchannels?\b")
RX_OC = re.compile(r"(?i)\d+(?:\.\d+)?\s*(?:in\.?|\"|”|'')\s*o\.?\s*c\.?|\d+(?:\.\d+)?\s*(?:in\.?|\")\s*(?:on\s+center|spacing)")


def falta_cita_u191(seg):
    """U-191 / BE-AUD05: qué le falta a un segmento que cita un documento. Un listing UL ('UL L546' o 'L546' suelto) exige 'Item N';
    si además es un renglón de RC / furring / channel exige el espaciamiento 'N in. o.c.'. Otras referencias: ítem / párrafo / sección."""
    ul = bool(RX_UL_SUELTO.search(seg)) or bool(re.search(r"(?i)\bUL\b|U\.L\.", seg))
    if not (RX_REF_EXT.search(seg) or RX_UL_SUELTO.search(seg)):
        return None
    if ul:
        f = [] if RX_UL_ITEM.search(seg) else ["'Item N' del listing"]
        if RX_RC_CTX.search(seg) and not RX_OC.search(seg):
            f.append("espaciamiento 'N in. o.c.'")
        return f
    return [] if RX_CITA_ITEM.search(seg) else ["ítem / párrafo"]


def _textos_u191(canon):
    """(dónde, texto) de toda fuente / operación / pregunta / supuesto del canon donde un dato puede venir de un documento citado."""
    out = []
    for k in ("misc_items", "walls", "existing_walls", "ceilings", "trim_items"):
        for x in canon.get(k) or []:
            if isinstance(x, dict):
                for c in ("source", "op", "assumption", "note", "height_source", "length_source"):
                    if x.get(c):
                        out.append((f"{k}:{x.get('ref') or x.get('id') or x.get('room')}.{c}", str(x[c])))
                for c in ("rc_oc_in", "layers", "assembly"):
                    v = x.get(c)
                    if isinstance(v, dict) and v.get("source"):
                        out.append((f"{k}:{x.get('ref') or x.get('id') or x.get('room')}.{c}", str(v["source"])))
    for r in canon.get("rfis") or []:
        if isinstance(r, dict):
            for c in ("question", "pregunta", "loaded", "basis", "opciones"):
                if r.get(c):
                    out.append((f"rfis:{r.get('id')}.{c}", json.dumps(r[c], ensure_ascii=False) if not isinstance(r[c], str) else r[c]))
    for x in canon.get("assumptions") or []:
        out.append(("assumptions", json.dumps(x, ensure_ascii=False) if not isinstance(x, str) else x))
    return out


def ms_excluido_cero(f):
    """v81cf118 (GK fila de drywall screws, U-053): renglón del Material Summary con cantidad 0 y EXCLUDED en su texto = no carga nada,
    no necesita cita (CB_U_191 lo salta). Con cantidad > 0 se revisa como siempre."""
    def _v(v):
        try:
            return float(str(v).replace(",", ""))
        except (TypeError, ValueError):
            return None                                  # vacío / fórmula sin valor: no cuenta
    net = _v(f.get("net"))
    cero = net is not None and abs(net) < 1e-9 and all((_v(f.get(k)) or 0) == 0 for k in ("purchase", "pieces"))
    return cero and bool(re.search(r"\bEXCLUDED\b", " ".join(str(f.get(k) or "") for k in ("material", "fuente", "nota", "status"))))


@chk("U-191", "BE-CR41", desc="U-191 / BE-CR41 (usuario 12-nov: 'toda la información biene en los planos'; CR RFI-14: RC 'spacing per assembly' "
     "dejado a 16 in. sin abrir UL L546, cuyo Item 6 imprime 12 in.): todo renglón / RFI / supuesto cuya fuente dice 'per assembly', 'per "
     "UL', 'per manufacturer', 'see spec' o cita un UL / GA lleva la cita del ítem / párrafo / sección del documento referido; sin ella = FAIL")
def u_191_ref(b):
    ts = _textos_u191(b.canon) + [(f"MS fila {f.get('fila')} '{str(f.get('material'))[:30]}'.fuente", str(f.get("fuente")))
                                  for f in (getattr(b, "ms", None) or []) if isinstance(f, dict) and f.get("fuente") and not ms_excluido_cero(f)]   # BE-AUD05: también el Excel
    if not ts:
        return NA("sin renglones / RFI con fuente en el canon")
    ev, n = [], 0
    for donde, t in ts:
        for seg in re.split(r"\s*(?:\||;|\n)\s*", t):
            f = falta_cita_u191(seg)
            if f is not None:
                n += 1
                if f:
                    ev.append(f"{donde}: '{seg[:110]}' cita un documento por referencia sin {' ni '.join(f)} (U-191 / BE-AUD05: abrirlo y citarlo)")
    if not n:
        return NA(f"{len(ts)} textos del canon sin referencias a assembly / UL / spec / fabricante")
    return R("FAIL", *ev[:20]) if ev else R("PASS", f"{n} referencias a documentos citados, cada una con su ítem / párrafo")


RX_RATED_CLG = re.compile(r"(?i)^(FS|RS)-\d")


def _fila_clg(r, nce):
    m = re.match(r"ceilings\[(\d+)\]", str(r))
    return int(m.group(1)) if m and int(m.group(1)) < nce else None


def dobles_declarados(b):
    """v81cf119: renglones 'double' de Auditoria/DOBLE_CIELO.csv (dicts con sus columnas)."""
    import io
    out = []
    for k, t in (b.textos or {}).items():
        if os.path.basename(k) == "DOBLE_CIELO.csv":
            for r in csv.DictReader(io.StringIO(t.lstrip("\ufeff"))):
                r = {str(a or "").strip(): v for a, v in r.items()}
                if str(r.get("Type") or r.get("Tipo") or "").strip().lower() == "double":
                    out.append(r)
    return out


def filas_doble_cielo(b):
    """BE-AUD06: renglones de datos de Auditoria/DOBLE_CIELO.csv (U-190) que trae la corrida."""
    return sum(max(0, len([ln for ln in t.splitlines() if ln.strip()]) - 1) for k, t in (b.textos or {}).items()
               if os.path.basename(k) == "DOBLE_CIELO.csv")


@chk("U-189", "BE-CR39", desc="U-189 (1) / BE-CR39 (CR rev19 corredor 216: FS-1 rated cargado y el GYP-1 8'-11\" colgado debajo faltante): en "
     "cada cuarto, cada cielo dibujado a distinta altura (rated FS / RS arriba + GYP / ACT / WS abajo) tiene SU renglón; dos tags de "
     "cielo distintos del mismo cuarto cubiertos por un solo renglón, o un cuarto con cielo rated y un tag colgado sin renglón ni motivo = FAIL")
def rcp_apilados(b):
    tg = [x for x in b.canon.get("rcp_tags") or [] if isinstance(x, dict)]
    cl = b.ceilings()
    cm = [x for x in b.canon.get("ceilings_misc") or [] if isinstance(x, dict)]   # v81cf117 (GK): cielos llevados como misc CLG-… (solo traza)
    misc = {str(m.get("ref")) for m in b.canon.get("misc_items") or [] if isinstance(m, dict)}
    sin_misc = [str(x.get("ref")) for x in cm if str(x.get("ref")) not in misc]
    if sin_misc:
        return R("FAIL", f"ceilings_misc cita {len(sin_misc)} ref(s) que no están en misc_items (v81cf117): {sin_misc[:10]}")
    room_ref = {str(x.get("ref")): str(x.get("room") or x.get("ref")) for x in cm}
    nd = filas_doble_cielo(b)
    if not tg and nd:
        return R("FAIL", f"en vacío (U-137 / BE-AUD06): DOBLE_CIELO.csv tiene {nd} renglones y el canon no trae rcp_tags: 0 cuartos evaluados")
    if not tg:
        n_ = len(cl) + len(cm)
        return NA("sin rcp_tags (lo exige CB_RCP_TAGS cuando hay RCP)") if not n_ else NA(f"sin rcp_tags; {n_} cielos sin tags que cruzar")
    nce = len(cl)
    cuartos_todos = [str(z.get("room") or z.get("id")) for z in cl] + list(room_ref.values())
    cuarto = {}                                          # cuarto -> [(tag, altura, filas, none_reason)]
    for x in tg:
        rows = x.get("rows") or []
        filas = [k for k in (_fila_clg(r, nce) for r in rows) if k is not None] + [f"misc:{r}" for r in rows if str(r) in room_ref]
        cuartos = {str(cl[k].get("room") or cl[k].get("id")) if isinstance(k, int) else room_ref[k[5:]] for k in filas}
        if not cuartos and x.get("match"):
            cuartos = {c for c in cuartos_todos if re.search(str(x["match"]), c)}
        for c in cuartos:
            cuarto.setdefault(c, []).append((str(x.get("tag") or ""), str(x.get("height") or ""), tuple(filas), x.get("none_reason")))
    ev, n2 = [], 0
    for c, xs in sorted(cuarto.items()):
        distintos = {(t, h) for t, h, _f, _n in xs}
        if len(distintos) < 2:
            continue
        n2 += 1
        usados = {}
        for t, h, f, nr in xs:
            if not f and not str(nr or "").strip():
                ev.append(f"{c}: tag {t} {h} dibujado y sin renglón ni none_reason (cielo apilado, U-189 (1))")
            for k in f:
                usados.setdefault(k, set()).add((t, h))
        for k, ts in usados.items():
            if len(ts) > 1:
                nom = f"ceilings[{k}]" if isinstance(k, int) else k[5:]
                ev.append(f"{c}: un solo renglón ({nom}) cubre {len(ts)} cielos dibujados a distinta altura "
                          f"({', '.join(f'{t} {h}' for t, h in sorted(ts))}): cada cielo apilado lleva su renglón (BE-CR39)")
    dob = dobles_declarados(b)                           # v81cf119 (CR rev20a: 54 'double' en DOBLE_CIELO y "7 cuartos, 0 apilados")
    n_dob_ok = 0
    if dob:
        import compuerta_entrega as _CE
        malos = _CE.refs_doble_fallas(dob, b.canon)     # la pila de DOBLE_CIELO (membrana FS / RS + GYP) se evalúa aunque no sea tag del RCP
        ev += [f"DOBLE_CIELO {x}" for x in malos]
        n_dob_ok = len(dob) - len({x.split(":")[0] for x in malos})
        if n2 == 0 and n_dob_ok == 0:
            ev.append(f"en vacío (U-137): DOBLE_CIELO declara {len(dob)} cuarto(s) 'double' y se evaluaron 0 cuartos apilados")
    if not cuarto:                                       # BE-AUD06 (GK rev3: '0 cuartos' con tags y DOBLE_CIELO lleno = pasaba en vacío)
        return R("FAIL", f"en vacío (U-137 / BE-AUD06): {len(tg)} rcp_tags y {nd} renglones de DOBLE_CIELO.csv, pero 0 cuartos evaluados "
                 "(ningún tag con rows 'ceilings[k]' / ref de ceilings_misc ni match a un cuarto del canon)")
    via = f" ({len(cm)} vía ceilings_misc)" if cm else ""        # v130 (CR): el TOTAL primero; '(0 … vía …)' no se escribe
    return R("FAIL", *ev[:20]) if ev else R("PASS", f"{nce + len(cm)} cielos evaluados{via}; {len(cuarto)} cuartos con tags de RCP; {n2} con "
                                            f"cielos apilados por tags + {n_dob_ok} de {len(dob)} 'double' de DOBLE_CIELO, cada cielo con su renglón")


RX_ELEM_DET = re.compile(r"(?i)^(SOF|BW)-")


@chk("U-189", "BE-CR39", desc="U-189 (2) / BE-CR39 (CR rev19: 2 caras de la banda 7/A7.23 y la caja en plenum sin cargar; 12/A9.03 cara del "
     "shaft): todo detalle que gobierna un soffit / banda / caja (SOF-, BW-) tiene su revisión cara por cara en detail_faces del canon "
     "(TODAS las caras dibujadas, incluidas las que suben al plenum); cara dibujada sin renglón cargado ni none_reason = FAIL")
def detalle_caras(b):
    elems = [(str(m.get("ref") or ""), f"{m.get('source') or ''} {m.get('op') or ''}") for m in b.canon.get("misc_items") or []
             if isinstance(m, dict) and RX_ELEM_DET.search(str(m.get("ref") or ""))]
    elems += [(str(w.get("id") or ""), f"{w.get('source') or ''} {w.get('detail') or ''}") for w in b.walls_todos()
              if RX_ELEM_DET.search(str(w.get("id") or ""))]
    if not elems:
        return NA("sin soffits / bandas / cajas (SOF-, BW-) en el canon")
    df = {str(d.get("detail") or "").replace(" ", "").lstrip("0"): d for d in b.canon.get("detail_faces") or [] if isinstance(d, dict)}
    refs_ok = {str(m.get("ref")) for m in b.canon.get("misc_items") or [] if isinstance(m, dict) and m.get("ref")}   # v81cf119: ref EXACTA
    refs_ok |= {str(w.get("id")) for w in b.walls_todos() if w.get("id")}
    refs_ok |= {f"ceilings[{k}]" for k in range(len(b.canon.get("ceilings") or []))}
    refs_ok |= {str(x.get(f)) for x in b.canon.get("ceilings") or [] if isinstance(x, dict) for f in ("id", "ref") if x.get(f)}
    ev, dets = [], set()
    for ref, src in elems:
        for n, h in RX_DET.findall(src):
            dets.add(f"{int(n)}/{h}" if str(n).isdigit() else f"{n}/{h}")
    for d in sorted(dets):
        reg = df.get(d) or next((v for k, v in df.items() if k.upper() == d.upper()), None)
        if reg is None:
            ev.append(f"{d}: gobierna un SOF / BW y no tiene revisión cara por cara en detail_faces (U-189 (2))")
            continue
        for f in reg.get("faces") or []:
            nom = f"{d} {f.get('face') or '?'} {f.get('dim') or ''}".strip()
            ld = str(f.get("loaded") or "").strip()
            lds = [x.strip() for x in re.split(r"\s*[,;+]\s*", ld) if x.strip()]
            if ld and not all(x in refs_ok for x in lds):
                ev.append(f"{nom}: 'loaded' {ld} no es un renglón del canon (ref exacta de misc_items / walls / ceilings; post-mortem 12b)")
            elif not ld and not str(f.get("none_reason") or "").strip():
                ev.append(f"{nom}: cara dibujada sin cargar ni none_reason (BE-CR39)")
    return R("FAIL", *ev[:20]) if ev else R("PASS", f"{len(dets)} detalles de SOF / BW revisados cara por cara contra {len(elems)} elementos")


# ============================================================================================== correr
# BE-CR25 (CR City Hotel rev1, COORDINACIÓN 6-nov): la compuerta pasó EN VACÍO: canon con walls = 0, Partition Takeoff con 778
# filas, BOTH SIDES dio N/A y 14 chequeos 'sin canon'. Un canon sin walls frente a un Partition Takeoff con filas = FAIL.
RX_VACIO = re.compile(r"(?i)sin walls|(?:^|N/A: )sin canon\b|no hay walls|\ben el canon\b|en walls\[\]")   # BE-CR29: toda ausencia de una estructura del canon


RX_CEMENT = re.compile(r"(?i)cement|\bCBU\b|durock|wonderboard|hardie\s*backer|tile\s*backer|backer\s*board")


def _showers_cbu(b):
    """BE-CR45: lista de showers {floor, room, box [x0, x1, y0, y1], cbu [{side W/E/N/S, id}]} del canon (showers) o de banos_cbu.json."""
    sh = b.canon.get("showers")
    if isinstance(sh, list):
        return sh, "canon.showers"
    for raiz in (b.canon_dir, b.raiz):
        if raiz and os.path.isdir(raiz):
            ps = _rglob_seguro(raiz, "**/banos_cbu.json")
            if ps:
                try:
                    return json.load(open(ps[0], encoding="utf-8")).get("showers") or [], ps[0]
                except (OSError, ValueError, AttributeError):
                    return None, ps[0]
    return None, None


def ducha_cbu_fallas(canon, showers):
    """BE-CR45 (CR rev20d, test de CR test_ducha_cbu.py hecho genérico): sobre el canon FINAL (toda cara cargada, también las tardías).
    (a) DOBLE CONTEO: fila de board NO cement de un type NON-rated (type_id '-0') en la cara del shower (<= 10 pt de la caja con 'shower' en
    'faces:', o furring <= 3.5 pt) con > 1 LF (9 pt) sobre el tramo del shower = FAIL (el cement board REEMPLAZA el board en NON-rated);
    (b) MARKUP EN LA CARA: el cement board está en la línea más cercana a la caja del shower pan (no en la línea de atrás)."""
    rows = [w for w in (canon.get("existing_walls") or []) + (canon.get("walls") or []) if isinstance(w, dict) and w.get("path")]
    byid = {w.get("id"): w for w in rows}
    es_cem = lambda r: bool(RX_CEMENT.search(str(r.get("board", ""))))      # noqa: E731
    segs = lambda w: [p for p in (w.get("paths") or [w["path"]]) if len(p) >= 2]      # noqa: E731
    fallas = []
    for s in showers:
        fl, room = s.get("floor"), s.get("room")
        x0, x1, y0, y1 = s["box"]
        for cb in s.get("cbu") or []:
            side = str(cb["side"]).strip().upper()
            vert = side in ("W", "E")
            lado = (x0 if side == "W" else x1) if vert else (y0 if side == "N" else y1)
            lo_b, hi_b = (y0, y1) if vert else (x0, x1)
            k = 0 if vert else 1
            w = byid.get(cb.get("id"))
            if w:
                lc = w["path"][0][k]
                for r in rows:
                    if r.get("floor") != fl or es_cem(r) or r.get("id") == cb.get("id"):
                        continue
                    for p in segs(r):
                        if abs(p[0][k] - p[-1][k]) > 0.5:
                            continue
                        lr = p[0][k]
                        if not (min(lc, lado) + 0.3 < lr <= max(lc, lado) + 0.3 or (abs(lr - lado) < abs(lc - lado) - 0.3 and abs(lr - lado) <= 3.5)):
                            continue
                        q = 1 - k
                        ov = min(max(p[0][q], p[-1][q]), hi_b) - max(min(p[0][q], p[-1][q]), lo_b)
                        if ov > 9 and abs(lr - lado) < abs(lc - lado):
                            fallas.append(f"(b) {fl} {room} {side}: cement board {cb.get('id')} drawn at {lc} but the shower face is {r.get('id')} at {lr} (line behind, not the shower face)")
                            break
            else:
                fallas.append(f"(b) {fl} {room} {side}: cement board {cb.get('id')} of the showers list is not in the canon")
            for r in rows:
                if r.get("floor") != fl or es_cem(r) or float(r.get("height_ft") or 0) <= 0.5:
                    continue
                hc = float((w or {}).get("height_ft") or 0)
                if hc and float(r.get("height_ft") or 0) <= hc - 0.5:
                    continue        # verificación f #1: la franja H - altura del cement board (más baja que el cement board) es legítima
                if not str(r.get("type_id", "")).endswith("-0"):
                    continue
                caras = str(r.get("location", "")).split("faces:")[-1].lower()
                dist = min(abs(p[0][k] - lado) for p in segs(r))
                furring = str(r.get("type", "")).startswith("F")
                if not (("shower" in caras and dist <= 10) or (furring and dist <= 3.5)):
                    continue
                for p in segs(r):
                    (a, bb), (c, d2) = p[0], p[-1]
                    if vert and abs(a - c) < 0.5 and abs(a - lado) <= 10:
                        ov = min(max(bb, d2), hi_b) - max(min(bb, d2), lo_b)
                    elif not vert and abs(bb - d2) < 0.5 and abs(bb - lado) <= 10:
                        ov = min(max(a, c), hi_b) - max(min(a, c), lo_b)
                    else:
                        continue
                    if ov > 9:
                        fallas.append(f"(a) {fl} {room} {side}: {r.get('id')} ({r.get('board')}, {r.get('type_id')}) {ov / 9:.2f} LF x {r.get('height_ft')} ft over the shower "
                                      f"+ cement board {cb.get('id')} = double count on a NON-rated face")
    return fallas


@chk("BE-CR45", desc="BE-CR45 (CR rev20d, v81cf138f): cement board / tile del shower por programa sobre el canon FINAL: en una cara NON-rated el "
     "cement board REEMPLAZA el board (fila de board no cement sobre el tramo del shower = doble conteo, FAIL) y el markup del cement board va en "
     "la cara real del shower (línea más cercana a la caja del shower pan). Lista de showers: canon.showers o banos_cbu.json; canon con cement "
     "board y sin lista de showers = AMBER (no se puede probar)")
def ducha_cbu(b):
    ws = [w for w in (b.canon.get("existing_walls") or []) + (b.canon.get("walls") or []) if isinstance(w, dict)]
    cem = [w for w in ws if RX_CEMENT.search(str(w.get("board") or ""))]
    if not ws:
        return NA("canon sin walls (no hay filas que revisar)")
    if not cem:
        return R("PASS", f"{len(ws)} filas del canon revisadas: ninguna lleva cement board (no hay cara de shower que revisar)")
    sh, fuente = _showers_cbu(b)
    if sh is None:
        return R("AMBER", f"{len(cem)} filas de cement board y ninguna lista de showers (canon.showers o banos_cbu.json): no se puede probar") \
            if not fuente else R("FAIL", f"{fuente}: no se pudo leer")
    if not sh:
        return R("AMBER", f"{len(cem)} filas de cement board y {fuente} trae una lista de showers vacía: no se puede probar")
    f = ducha_cbu_fallas(b.canon, sh)
    if f:
        return R("FAIL", *f[:30], f"{len(f)} fallas en {len(sh)} showers ({fuente})")
    return R("PASS", f"{len(sh)} showers ({fuente}): 0 dobles conteos, cada cement board en la cara del shower")


RX_DESIG_STUD = re.compile(r"\b(\d{3})S(\d{3})-(\d{2,3})\b")


def _desig_misc(m):
    d = RX_DESIG_STUD.search(str(m.get("designation") or ""))
    if not d:
        s = str(m.get("source") or "")
        d = RX_DESIG_STUD.search(s.split("|", 1)[1]) if "|" in s else None
    return d


def stud_zona_fallas(canon):
    """BE-XF20 (Xfinity rev1c, auditoría 13-nov E-1): fila misc de STUDS de otro gauge (misma medida) en los bays de un wall del canon
    (su texto nombra el wall o su type) = los studs de esa zona REEMPLAZAN los del wall: hace falta una fila de deducción (qty < 0) del stud
    del wall que cite el mismo N/HOJA por la misma cantidad, o un campo 'decision' con N/HOJA que diga por qué se SUMAN. -> [fallas]"""
    walls = [w for w in muros_canon(canon) if isinstance(w, dict)]       # BE-XF16: walls + existing_walls
    ids_w = {str(w.get("id") or "") for w in walls} - {""}
    st = {}
    for w in walls:
        d = RX_DESIG_STUD.search(" ".join(str(w.get(k) or "") for k in ("stud_size", "stud", "designation", "gauge")))
        if d:
            for k in {str(w.get("id") or ""), str(w.get("type_id") or w.get("tag") or "")} - {""}:
                st[k] = d
    misc = [m for m in canon.get("misc_items") or [] if isinstance(m, dict)]
    fallas = []
    for m in misc:
        q = _n(m.get("qty"))
        d = _desig_misc(m)
        if not d or q is None or q <= 0 or d.group(2) == "000":
            continue
        txt = " ".join(str(m.get(k) or "") for k in ("source", "op", "label", "note"))
        if re.search(r"(?i)\bbrace|kicker|header|\bjamb|\bking\b|soffit|bulkhead|\btrack\b", str(m.get("familia") or "") + " " + str(m.get("label") or "")):
            continue
        zona = re.search(r"(?i)backing|\bzone|\bbays?\b|in lieu|replac|instead of", txt)
        hits = sorted({k for k in st if                                  # verificación g #1 (Grand Kia): un type citado solo por su tamaño /
            (k in ids_w and len(k) >= 2 and re.search(r"(?<![\w.-])" + re.escape(k) + r"(?![\w.])", txt))      # ejes 'A' / 'H' no cuentan
            or (zona and re.search(r"(?i)\b(?:type|wall|tipo)\s+" + re.escape(k) + r"(?![\w.])|(?<![\w.-])" + re.escape(k) + r"\s+(?:walls?|studs?|types?)\b"
                                   + (r"|(?<![\w.-])" + re.escape(k) + r"(?![\w.])" if len(k) >= 2 and re.search(r"[0-9]", k) else ""), txt))})
        otros = [st[k] for k in hits if st[k].group(1) == d.group(1) and st[k].group(3) != d.group(3)]
        if not otros:
            continue
        wd = otros[0].group(0)
        hojas = set(RX_NHOJA.findall(str(m.get("source") or "")))
        if set(RX_NHOJA.findall(str(m.get("decision") or ""))) & (hojas or set(RX_NHOJA.findall(str(m.get("decision") or "")))):
            continue                     # verificación g #3: la 'decision' cita el MISMO N/HOJA de la zona
        ded = [x for x in misc if (_n(x.get("qty")) or 0) < 0 and wd in json.dumps(x) and (not hojas or hojas & set(RX_NHOJA.findall(json.dumps(x))))]
        tot = -sum(_n(x.get("qty")) or 0 for x in ded)
        if not ded:
            fallas.append(f"{m.get('ref') or m.get('id')}: {q:g} {m.get('unit') or ''} of {d.group(0)} in the bays of {', '.join(hits)} (wall stud {wd}) and no "
                          f"deduction row of {wd} citing {', '.join(sorted(hojas)) or 'the same N/SHEET'}: zone studs REPLACE the wall studs (double count) "
                          f"or write 'decision' with the N/SHEET that adds them")
        elif abs(tot - q) > max(0.5, 0.01 * q):
            fallas.append(f"{m.get('ref') or m.get('id')}: zone {q:g} of {d.group(0)} vs deduction {tot:g} of {wd} ({', '.join(str(x.get('ref')) for x in ded)}): "
                          f"same positions = same quantity, or 'decision' with N/SHEET")
    return fallas


@chk("BE-XF20", desc="BE-XF20 (Xfinity rev1c, auditoría 13-nov E-1, v81cf138g): studs de otro gauge impresos para una zona (8/A2.0 backing studs "
     "16 ga) en los bays de un wall REEMPLAZAN los studs del wall: fila misc de stud de otro gauge que nombra un wall / type del canon sin fila "
     "de deducción del stud del wall (qty < 0, mismo N/HOJA, misma cantidad) ni 'decision' con N/HOJA = FAIL (doble conteo)")
def stud_zona_reemplaza(b):
    f = stud_zona_fallas(b.canon)
    if f:
        return R("FAIL", *f[:20])
    n = sum(1 for m in b.canon.get("misc_items") or [] if isinstance(m, dict) and _desig_misc(m))
    return R("PASS", f"{n} filas misc con designation de stud: 0 zonas de otro gauge sin su deducción")


RX_STUD_EN_HEAD = re.compile(r"(?i)\bSTUDS?\s+NESTED\b|\bNESTED\s+(?:METAL\s+)?STUDS?\b|\bSTUDS?\s+(?:INSIDE|IN|INSERTED\s+(?:IN|INTO))\s+(?:THE\s+)?(?:METAL\s+)?TRACK\b")


def head_piezas_fallas(canon):
    """BE-XF21 (Xfinity rev1c, auditoría 13-nov E-2): el producto de CADA pieza de un head detail es el impreso (U-177 (4)): si el texto
    del head de una abertura imprime un STUD (anidado en el track: '3-5/8" METAL STUD NESTED IN METAL TRACK'), el canon lleva una fila de
    stud (designation S / familia stud, no track) que cite esa abertura; cargar las dos piezas como track = FAIL. -> [fallas]"""
    ops = []
    for w in muros_canon(canon):                                        # BE-XF16
        if isinstance(w, dict):
            ops += [o for o in w.get("openings") or [] if isinstance(o, dict)]
    osch = canon.get("opening_schedule")
    ops += [o for o in ((osch or {}).get("items") if isinstance(osch, dict) else osch) or [] if isinstance(o, dict)] if isinstance(osch, (dict, list)) else []
    ops += [o for o in canon.get("openings_extra") or [] if isinstance(o, dict)] if isinstance(canon.get("openings_extra"), list) else []
    misc = [m for m in canon.get("misc_items") or [] if isinstance(m, dict)]
    fallas, vistos = [], set()
    for o in ops:
        ref = str(o.get("ref") or o.get("id") or "")
        if not ref or ref in vistos:
            continue
        txt = " ".join(str(o.get(k) or "") for k in ("header_type_source", "header", "pieces_source", "header_source", "head_detail", "head", "head_source"))
        if not RX_STUD_EN_HEAD.search(txt) or re.search(r"(?i)\bstud\b", str(o.get("piece") or "")):
            continue
        vistos.add(ref)
        num = re.findall(r"\d+[A-Z]?", ref)
        def cita(m):
            s = json.dumps(m)
            return (ref.lower() in s.lower()) or any(re.search(r"(?i)\b(?:door|opening|window|DR\.?)\s*#?\s*" + re.escape(n) + r"\b", s) for n in num)
        hh = set(RX_NHOJA.findall(txt))
        def de_head(m):                  # verificación h #1: la fila es la pieza del HEAD (nested / head / header o el mismo N/HOJA), no un jamb
            s = json.dumps(m)
            return bool(re.search(r"(?i)nested|\bhead|header", s) or (hh & set(RX_NHOJA.findall(s))))
        studs = [m for m in misc if cita(m) and de_head(m) and (re.search(r"\d{3}S\d{3}-\d{2}", str(m.get("designation") or m.get("source") or ""))
                                                  or re.search(r"(?i)\bstud", str(m.get("familia") or "") + " " + str(m.get("ref") or "")))
                 and not re.search(r"(?i)\btrack\b", str(m.get("familia") or ""))]
        if not studs:
            fallas.append(f"{ref}: the head detail prints a STUD piece ('{RX_STUD_EN_HEAD.search(txt).group(0)}', {', '.join(sorted(set(RX_NHOJA.findall(txt)))) or 'no N/SHEET'}) "
                          f"and the canon carries piece '{o.get('piece') or '?'}' x {o.get('pieces') or '?'} with no stud row citing {ref}: the product of each "
                          f"printed piece is the printed one (U-177 (4))")
    return fallas


@chk("BE-XF21", "U-177", desc="BE-XF21 (Xfinity rev1c, auditoría 13-nov E-2, v81cf138h): el producto de cada pieza de un head detail es el impreso: "
     "head con 'STUD NESTED IN TRACK' cargado como 2 piezas de track sin fila de stud que cite la abertura = FAIL")
def head_piezas(b):
    f = head_piezas_fallas(b.canon)
    return R("FAIL", *f[:20]) if f else R("PASS", "0 heads con una pieza de stud impresa cargada como track")


U201_TEMAS = {
    1: ("rating distinto entre code plan y tag de planta = se carga el MAYOR + DEDUCT alternate con el delta del menor (RFI-32 'A', U-161)",
        re.compile(r"(?i)(?:fire[- ]?)?rating (?:conflict|discrepanc)|code plan[^.]{0,250}\b(?:\d\s*HR|rat(?:ed|ing))|(?:life safety|code) plan shows \d\s*HR|"
                   r"\b\d\s*HR\b[^.]{0,200}\btag(?:ged| shows| reads)\b|\b\d\s*HR\s+vs\.?\s+\d\s*HR\b")),
    2: ("elemento dibujado sin tag ni tipo impreso = tipo del muro con el que conecta + rating del code plan, cargado (RFI-33 'A', U-178(2))",
        re.compile(r"(?i)\buntagged (?:wall|element|lining|furring|partition|build-?out|chase)|\bwalls?\b[^.]{0,80}\b(?:untagged|not tagged|has no tag|carr(?:y|ies) no (?:wall )?(?:tag|type))|"
                   r"carr(?:y|ies) no (?:wall )?type|(?:wall|partition) type (?:not shown|not printed|not indicated)|no (?:wall |partition )type (?:shown|printed|indicated)|"
                   r"without (?:a )?(?:wall |partition )(?:tag|type)|sin tag")),
    3: ("column wrap / beam wrap donde los detalles solo marcan SFRM = gypsum cargado (conservador) + DEDUCT alternate con el delta (RFI-34 'A')",
        re.compile(r"(?i)(?:\bSFRM\b|spray(?:ed)?[- ]applied fire|spray(?:ed)? fire(?:proofing)?|sprayed fire-resistive)[^.]{0,200}\b(?:wrap|gyp|enclos|board)|"
                   r"\b(?:wrap|gyp\w*|enclos\w*)\b[^.]{0,200}(?:\bSFRM\b|spray(?:ed)?[- ]applied fire|spray(?:ed)? fire)")),
}
U201_CON_DA = {1, 3}


def u201_fallas(canon):
    """U-201 (usuario 13-nov, CR, botones 'A' de RFI-32 / 33 / 34; TODOS los proyectos): las decisiones son REGLA, sin RFI de aquí en
    adelante. (a) un RFI ABIERTO sobre uno de esos temas = FAIL (se aplica la regla y se cierra citando U-201 (n)); (b) un RFI cerrado
    de los temas (1) / (3) lleva su DEDUCT alternate (rfi = el id, delta ≠ 0). (4) / (5) [RATE TO CONFIRM] los revisan U-192 /
    revisar_proposal. -> [fallas]"""
    lst = lambda v: list(v.values()) if isinstance(v, dict) else (v if isinstance(v, list) else [])      # noqa: E731
    das = [x for x in lst(canon.get("deduct_alternates")) + lst(canon.get("decisiones_usuario_da")) if isinstance(x, dict)]
    def delta(x):
        m = re.search(r"-?\d[\d,]*(?:\.\d+)?", str(x.get("delta_sf") if x.get("delta_sf") is not None else x.get("delta") or ""))
        return float(m.group(0).replace(",", "")) if m else 0.0
    out = []
    for r in lst(canon.get("rfis")):
        if not isinstance(r, dict):
            continue
        txt = " ".join(str(r.get(k) or "") for k in ("question", "pregunta", "titulo", "title", "texto", "tema", "donde", "supuesto"))
        temas = [n for n, (_d, rx) in U201_TEMAS.items() if rx.search(txt)]
        if not temas:
            continue
        rid = str(r.get("id") or "")
        abierto = not re.match(r"(?i)\s*(?:clos|cerr|resol|resuel|answer|respond|exclu|void|supersed|withdrawn|n/?a\b)", str(r.get("status") or "open"))
        if abierto:
            out.append(f"{rid}: RFI abierto sobre un tema que el usuario ya decidió (U-201 ({', '.join(map(str, temas))}): "
                       f"{U201_TEMAS[temas[0]][0]}): se aplica la regla y se cierra citando U-201, sin RFI")
            continue
        for n in temas:
            if n in U201_CON_DA and not any(rid and str(x.get("rfi") or "") == rid and abs(delta(x)) > 0 for x in das):
                out.append(f"{rid}: U-201 ({n}) cerrado sin DEDUCT alternate con delta (rfi = {rid}): {U201_TEMAS[n][0]}")
    return out


@chk("U-201", desc="U-201 (usuario 13-nov, CR City Hotel; v81cf138k): las decisiones del usuario son REGLA en todos los proyectos: RFI abierto sobre "
     "(1) rating code plan vs tag, (2) elemento sin tag ni tipo, (3) wrap con solo SFRM = FAIL; (1) / (3) cerrados sin DEDUCT alternate con delta = FAIL")
def u201_decisiones(b):
    f = u201_fallas(b.canon)
    if f:
        return R("FAIL", *f[:20])
    n = sum(1 for r in b.canon.get("rfis") or [] if isinstance(r, dict))
    return R("PASS", f"{n} RFI revisados: ninguno abierto sobre un tema decidido por el usuario (U-201 (1)-(3)); los cerrados (1) / (3) con su DEDUCT")


@chk("BE-CR25", "U-124", desc="BE-CR25 / U-124: canon con 0 walls (ni walls[] ni board-only de existing_walls) y Partition "
     "Takeoff con > 0 filas = FAIL (la compuerta no puede pasar en vacío)")
def canon_no_vacio(b):
    filas = [r for r in b.pt if isinstance(r, dict) and (r.get("wall") or r.get("partition"))]
    if not filas:
        return NA("Partition Takeoff sin filas")
    if not b.walls():
        # solo-metal: el mensaje cuenta walls[] a propósito
        return R("FAIL", f"canon sin walls (walls[] = {len(b.canon.get('walls') or [])}, board-only = 0) y el Partition Takeoff "
                         f"tiene {len(filas)} filas: los chequeos por wall correrían en vacío")
    return R("PASS", f"{len(b.walls())} walls en el canon frente a {len(filas)} filas del Partition Takeoff")


def en_vacio(b, nombre, est, ev):
    """BE-CR25: con filas en el Partition Takeoff, un chequeo que se declara N/A / 'sin walls / sin canon' = FAIL."""
    if est == "FAIL" or nombre == "canon_no_vacio" or not any(isinstance(r, dict) and (r.get("wall") or r.get("partition")) for r in b.pt):
        return est, ev
    # NA() = PASS 'N/A: …'; SIN() = AMBER 'sin …: no se puede probar'. Un PASS que dice 'sin walls existing como nuevos' es un resultado.
    if any(RX_VACIO.search(e) and ((est == "PASS" and e.startswith("N/A")) or (est == "AMBER" and e.startswith("sin "))) for e in ev[:2]):
        return "FAIL", [f"BE-CR25: '{ev[0][:120]}' con {len(b.pt)} filas en el Partition Takeoff = chequeo en vacío"] + list(ev)
    return est, ev


def correr(b):
    out = []
    for ids, fn, desc in CHEQUEOS:
        try:
            est, ev = fn(b)
        except Exception as e:          # noqa: BLE001 — un chequeo roto = FAIL
            est, ev = "FAIL", [f"el chequeo no corrió: {type(e).__name__}: {e}"]
        out.append({"id": fn.__name__, "reglas": ids, "descripcion": desc, "estado": est, "evidencia": ev})
    for r in out:
        r["estado"], r["evidencia"] = en_vacio(b, r["id"], r["estado"], r["evidencia"])
    return out


def main(argv):
    if len(argv) >= 6 and argv[1] == "faltante":                  # BE-CR40: el auditor verifica cada 'falta' así, no buscando texto
        falta, motivo = faltante_por_tag(json.load(open(argv[2], encoding="utf-8")), argv[3], argv[4], argv[5])
        print(f"faltante_por_tag: {'FALTA' if falta else 'CARGADO'} ({argv[3]} {argv[4]} {argv[5]}: {motivo})")
        return 0 if falta else 1
    if len(argv) < 2:
        print(__doc__)
        return 2
    import compuerta_entrega as CE
    b = B.desde_ctx(CE.Ctx(argv[1]))
    res = correr(b)
    for r in res:
        print(f"{r['estado']:5} {r['id']:10} {', '.join(r['reglas'])[:40]}")
        if r["estado"] == "FAIL":
            for e in r["evidencia"][:4]:
                print("        - " + e[:200])
    n = {k: sum(r["estado"] == k for r in res) for k in ("PASS", "AMBER", "FAIL")}
    print(n)
    return 1 if n["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
