#!/usr/bin/env python3
"""alcances.py — lista FIJA de alcances (scopes) que todo take-off de metal frame y drywall revisa.

Por qué existe (prueba <proyecto> 13-oct-2026): el registro solo tenía lo que Claude VIO; alcances completos
(ceiling suspension, canopy, exterior FRT plywood) nunca entraron al registro y el take-off se dio por
entregado. Esta lista no depende de lo que se vio: cada alcance entra al registro desde el inicio y
tiene que cerrarse CUANTIFICADO o NO APLICA (con hoja y motivo).

Uso:
  alcances.py escanear   <bid_set.pdf> <escaneo.json>
        Busca en el texto del PDF las palabras clave de cada alcance. Guarda hoja + página de cada hallazgo.
  alcances.py renglones  <escaneo.json> <renglones.json>
        Escribe los renglones ALC-xx para `registro.py agregar` (todos arrancan pendiente).
  alcances.py compuerta  <registro.json> <escaneo.json> <takeoff.xlsx>
        Exit 1 si algún alcance:
          - sigue pendiente;
          - está verificado como "NO APLICA" sin citar hoja, o el PDF lo menciona y la nota no cita
            ninguna de las hojas donde aparece (hay que ir a verlas antes de descartarlo);
          - está verificado como cuantificado pero el Excel no tiene cantidad > 0 de esa familia
            (ALC-12 exige TODAS sus partes: furring, carrying, hanger wire y track), o, si el alcance no
            tiene familia, ningún renglón con el término y una cantidad > 0. Un renglón que diga
            PENDING / ALTERNATE / EXCLUDED no cuenta como cantidad.
        Los pendiente_rfi pasan (salen en la lista PARA REVISAR).
        v77c (U8): ALC-19 (acoustical sealant) está EXCLUIDO en todos los proyectos: se cierra "EXCLUIDO: ..." y el
        Excel con un renglón de acoustical sealant = falla.

Para marcar un alcance:
  registro.py marcar <registro.json> ALC-07 verificado "Takeoff renglones de ceilings GWB; N/HOJA del RCP"
  registro.py marcar <registro.json> ALC-21 verificado "NO APLICA: A02.01 sin shaft walls; S1.14 solo cita shaft de elevador existente"
"""
import json, os, re, subprocess, sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# (id, nombre en inglés, regex de palabras clave en el PDF, familias de eval_takeoff que prueban cantidad, términos en el Excel)
ALCANCES = [
    ("ALC-01", "Interior partition framing (studs + tracks)", r"PARTITION TYPE|STUD", ['6" stud', '3-5/8" stud', '1-5/8" stud'], ["stud"]),
    ("ALC-02", "Exterior wall framing (CFMF)", r"COLD.?FORMED|CFMF|EXTERIOR WALL", ['6" stud'], ["exterior"]),
    ("ALC-03", "Parapet framing", r"PARAPET", ['6" parapet stud'], ["parapet"]),
    ("ALC-04", "Top / deflection and bottom track", r"DEFLECTION|SLIP TRACK|TOP TRACK", ["bottom track", "top / deflection track"], ["track"]),
    ("ALC-05", "Headers, sills and jambs at openings", r"HEADER|SILL|JAMB", ["header / box beam", "sill track"], ["header", "sill"]),
    ("ALC-06", "Bracing / bridging", r"BRIDGING|BRACING", ["bracing C.R. channel"], ["bracing", "bridging"]),
    ("ALC-07", "Gypsum board on walls (layers per type)", r"GYPSUM BOARD|GYP\.? BD|GWB", ['5/8" gyp board regular', '5/8" gyp board Type X', '5/8" gyp Type X W.R.'], ["gypsum"]),  # v80f R80e.18
    ("ALC-08", "Moisture / abuse / special board at wet zones", r"MOISTURE RESIST|ABUSE|IMPACT RESIST|MR GYP", ['5/8" gyp MOISTURE RESISTANT', '5/8" gyp Type X W.R.'], ["moisture", "abuse"]),  # v80f R80e.18
    ("ALC-09", "Exterior gypsum / glass mat sheathing", r"SHEATHING|GLASS MAT|DENSGLASS", ['5/8" EXTERIOR gyp sheathing', '5/8" glass mat sheathing', '1/2" EXTERIOR gyp sheathing'], ["sheathing"]),  # v80f R80e.16
    ("ALC-10", "FRT plywood sheathing / substrate", r"FRT PLYWOOD|FIRE.?RETARDANT.{0,20}PLYWOOD|PLYWOOD", ["FRT plywood (SF)"], ["plywood"]),
    ("ALC-11", "Gypsum board ceilings", r"GYPSUM (WALL)?BOARD CEILING|GYP\.? BD\.? CEILING|GWB CEILING|SUSPENDED GYPSUM", ['5/8" gyp board regular'], ["ceiling"]),
    ("ALC-12", "Ceiling suspension (furring / carrying channel / hanger wire / ceiling track)", r"SUSPENDED GYPSUM|HANGER|CARRYING CHANNEL|FURRING CHANNEL|MAIN RUNNER|GRID SYSTEM", ["furring channel", "carrying channel", "hanger wire", "track de ceilings / soffits"], ["furring", "carrying", "hanger"]),
    ("ALC-13", "Soffits and bulkheads (framing + board)", r"SOFFIT|BULKHEAD", ["track de ceilings / soffits"], ["soffit", "bulkhead"]),
    ("ALC-14", "Canopy / marquee framing and sheathing", r"CANOPY|MARQUEE", [], ["canopy"]),
    ("ALC-15", "Column furring / wraps", r"COLUMN (FURRING|WRAP|ENCLOSURE|COVER)|FURR(ED)? COLUMN", [], ["column"]),
    ("ALC-16", "Blocking (FRT wood / metal) for millwork and accessories", r"BLOCKING", ["FRT blocking"], ["blocking"]),
    ("ALC-17", "Framed openings (MEP, access panels, diffusers)", r"ACCESS PANEL|ACCESS DOOR|FRAMED OPENING", ["framed openings MEP"], ["access panel", "framed opening", "mep"]),
    ("ALC-18", "Trim: corner bead, casing bead, control joints, reveals", r"CORNER BEAD|CASING BEAD|CONTROL JOINT|REVEAL|J-BEAD|L-BEAD", ["metal trim (corner bead, casing, shadow molding)"], ["bead", "control joint", "reveal", "trim"]),
    ("ALC-19", "Acoustical sealant / sound attenuation (EXCLUDED: estimator standing order, all projects)", r"ACOUSTICAL SEALANT|SOUND ATTENUAT|STC", [], ["acoustical sealant"]),
    ("ALC-20", "FRP / cement board / tile backer", r"\bFRP\b|CEMENT BOARD|TILE BACKER|DUROCK", ["FRP", "cement board"], ["frp", "cement"]),
    ("ALC-21", "Shaft walls / area separation walls", r"SHAFT ?WALL|AREA SEPARATION|SHAFTLINER", [], ["shaft"]),
    ("ALC-22", "Rated assemblies (UL designs) and their board type", r"\bUL\s?#?\s?[A-Z]\d{3}|FIRE.?RATED|HOUR RATED|1 HR|2 HR", [], ["rated", "type x"]),
    ("ALC-23", "Special panels (ballistic, lead-lined, abuse)", r"BALLISTIC|BULLET.?RESIST|UL ?752|LEAD.?LINED", ["ballistic panel"], ["ballistic", "lead"]),
    ("ALC-24", "Finish level (Level 4 / Level 5)", r"LEVEL ?[45]\b|LEVEL (FOUR|FIVE)", [], ["level 5", "level 4"]),
]

# v77c (decisión del usuario U8, R77.12): alcances EXCLUIDOS en todos los proyectos. Se cierran "EXCLUIDO: <motivo>"
# (nunca CUANTIFICADO ni NO APLICA) y el Excel NO puede tener cantidad de su familia (renglón = falla).
EXCLUIDOS = {"ALC-19": ("acoustical sealant", "EXCLUIDO: acoustical sealant excluded in all projects (estimator "
                                               "standing order); sound attenuation insulation excluded (no insulation)")}
SHEET_RE = re.compile(r"\b[A-Z]{1,2}\d{1,2}\.\d{2}\b")
# v80e (R80e.13): las citas de una nota NO APLICA aceptan también hojas con guion (A-410, M-102, A-226A) y la
# página "pN" que escanear() usa cuando la hoja no tiene un ID con punto (bid sets con texto vectorizado).
CITA_RE = re.compile(r"\b(?:[A-Z]{1,2}\d{1,2}\.\d{2}|[A-Z]{1,2}-\d{2,3}[A-Z]?|p\d{1,3})\b")


def _pages(pdf):
    out = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, check=True).stdout
    return out.decode("utf-8", "replace").split("\f")


def _sheet_of(text, n):
    ids = SHEET_RE.findall(text)
    return Counter(ids).most_common(1)[0][0] if ids else f"p{n}"


def escanear(pdf):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import copia_limpia                       # v77 (R76.7 e): siempre sobre la copia SIN /Annots
    pdf, _ = copia_limpia.copia_limpia(pdf)
    pages = _pages(pdf)
    res = {"pdf": os.path.basename(pdf), "paginas": len(pages), "alcances": {}}
    for aid, nombre, rx, _, _ in ALCANCES:
        r = re.compile(rx, re.I)
        hits = []
        for i, p in enumerate(pages):
            m = r.search(p)
            if m:
                s = max(0, m.start() - 40)
                hits.append({"hoja": _sheet_of(p, i + 1), "pagina": i + 1,
                             "texto": re.sub(r"\s+", " ", p[s:m.end() + 40]).strip()})
        res["alcances"][aid] = {"nombre": nombre, "hallazgos": hits}
    return res


def renglones(esc):
    rows = []
    for aid, nombre, *_ in ALCANCES:
        hits = esc["alcances"][aid]["hallazgos"]
        hojas = sorted({h["hoja"] for h in hits})
        fuente = "alcances.py (lista fija)" + (f"; el PDF lo menciona en {', '.join(hojas[:12])}" if hojas
                                                 else "; el PDF no lo menciona")
        rows.append({"id": aid, "tipo": "alcance", "ubicacion": nombre, "fuente": fuente})
    return rows


NO_CUENTA = re.compile(r"PENDING|PENDIENTE|ALTERNATE|EXCLUDED|EXCLUIDO|BY OTHERS|NIC\b|N\.I\.C", re.I)


def _excel_evidencia(xlsx):
    """Renglones del Excel que SÍ cuantifican: tienen un número > 0 y no dicen PENDING/ALTERNATE/excluded."""
    import openpyxl
    import eval_takeoff as E
    wb = openpyxl.load_workbook(xlsx, data_only=True)
    filas = []
    for ws in wb.worksheets:
        if "revisar" in ws.title.lower() or "rfi" in ws.title.lower():
            continue                                  # las listas de pendientes no cuentan como cantidad
        for row in ws.iter_rows(values_only=True):
            txt = " ".join(str(c) for c in row if isinstance(c, str))
            if not txt or NO_CUENTA.search(txt):
                continue
            if any(isinstance(c, (int, float)) and c > 0 for c in row):
                filas.append(txt.lower())
    mats = [m for m in (E.read_materials(wb) or []) if not NO_CUENTA.search(m["name"])]
    fams = {f: d["net"] for f, d in E.por_familia(mats).items()}
    return filas, fams


def compuerta(registro_path, esc, xlsx):
    import registro as R
    reg = R.leer(registro_path)
    filas = {r["id"]: r for r in reg["renglones"]}
    filas_xl, fams = _excel_evidencia(xlsx)
    fallas, rfi = [], []
    for aid, nombre, _, familias, terminos in ALCANCES:
        r = filas.get(aid)
        if r is None:
            fallas.append(f"{aid} {nombre}: no está en el registro (corre `alcances.py renglones` + `registro.py agregar`)")
            continue
        if r["estado"] == "pendiente":
            fallas.append(f"{aid} {nombre}: sigue PENDIENTE")
            continue
        if r["estado"] == "pendiente_rfi":
            rfi.append(f"{aid} {nombre}: {r['nota']}")
            continue
        nota = r["nota"]
        if aid in EXCLUIDOS:
            fam_x = EXCLUIDOS[aid][0]
            if not re.match(r"\s*(EXCLUIDO|EXCLUDED)\b", nota, re.I):
                fallas.append(f"{aid} {nombre}: alcance EXCLUIDO en todos los proyectos (U8); cerrar con "
                              f"'{EXCLUIDOS[aid][1]}'")
            if fams.get(fam_x, 0) > 0 or any(fam_x in f for f in filas_xl):
                fallas.append(f"{aid}: el Excel trae renglón de {fam_x} (U8: EXCLUIDO, sin renglón ni cantidad)")
            continue
        hojas_pdf = sorted({h["hoja"] for h in esc["alcances"][aid]["hallazgos"]})
        if nota.strip().upper().startswith("NO APLICA"):
            citadas = set(CITA_RE.findall(nota))
            if not citadas:
                fallas.append(f"{aid} {nombre}: NO APLICA sin citar hoja")
            elif hojas_pdf and not (citadas & set(hojas_pdf)):
                fallas.append(f"{aid} {nombre}: NO APLICA, pero el PDF lo menciona en {', '.join(hojas_pdf[:8])} "
                              f"y la nota no cita ninguna de esas hojas: hay que ir a verlas")
            continue
        if familias:      # con familia de material: tiene que haber cantidad NET > 0 en esa familia
            ok = all(any(f.startswith(want) and fams[f] > 0 for f in fams) for want in familias) \
                if aid == "ALC-12" else any(f.startswith(want) and fams[f] > 0 for f in fams for want in familias)
        else:             # sin familia: un renglón con el término Y una cantidad > 0, que no diga PENDING
            ok = any(t in fila for fila in filas_xl for t in terminos)
        if not ok:
            fallas.append(f"{aid} {nombre}: marcado como cuantificado, pero el Excel no tiene cantidad > 0 de "
                          f"{familias or terminos} (un texto PENDING/ALTERNATE no cuenta)")
    return fallas, rfi


def main():
    a = sys.argv[1:]
    if len(a) == 3 and a[0] == "escanear":
        esc = escanear(a[1])
        json.dump(esc, open(a[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        for aid, d in esc["alcances"].items():
            hojas = sorted({h["hoja"] for h in d["hallazgos"]})
            print(f"{aid} {d['nombre'][:55]:55s} {len(hojas):3d} hojas  {', '.join(hojas[:6])}")
    elif len(a) == 3 and a[0] == "renglones":
        rows = renglones(json.load(open(a[1], encoding="utf-8")))
        json.dump(rows, open(a[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"OK {len(rows)} renglones de alcance -> {a[2]}")
    elif len(a) == 4 and a[0] == "compuerta":
        fallas, rfi = compuerta(a[1], json.load(open(a[2], encoding="utf-8")), a[3])
        for x in rfi:
            print("RFI   ", x)
        for x in fallas:
            print("FALLA ", x)
        if fallas:
            print(f"NO ENTREGABLE: {len(fallas)} alcances sin cerrar")
            sys.exit(1)
        print(f"ALCANCES OK: {len(ALCANCES)} revisados, {len(rfi)} con RFI")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
