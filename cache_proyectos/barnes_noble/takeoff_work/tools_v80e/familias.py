#!/usr/bin/env python3
"""familias.py — lectura del Excel de un take-off agrupada por FAMILIA de material.

La usan eval_takeoff.py (calificador) y alcances.py (compuerta de alcances). No trae datos de
ningún proyecto ni del take-off de referencia: solo cómo leer la hoja de materiales y a qué
familia pertenece cada renglón.
Cambio v62 (16-oct-2026, arbitraje #12): EXCLUYE plywood|nailbase de 5/8" gyp regular y "framed opening"
de las familias de stud.
Cambio v77c (U8): el sealant exterior (base of gypsum) es familia propia; "acoustical sealant" queda solo para
renglones acoustical, que están EXCLUIDOS en todos los proyectos (el calificador los marca MAL con modo "excluir").
Cambio 15-oct-2026: familia propia para el blocking METÁLICO (362CR / STUD BLOCKING), que ya no se
suma al FRT blocking (arbitraje prueba #4, regla 54.3); y familia propia de purlin antes de las de
track, que se sumaba al top track (arbitraje prueba #5).
"""
import re


def num(v):
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return float(v)
    try:
        return float(str(v).replace(",", "").strip())
    except ValueError:
        return None


def norm_unit(u):
    u = (str(u or "")).strip().lower().rstrip(".")
    return {"pc": "pcs", "ea": "pcs", "each": "pcs", "lbs": "lb", "sqft": "sf", "lf.": "lf"}.get(u, u)


def find_sheet(wb, *needles):
    for ws in wb.worksheets:
        t = ws.title.lower()
        if all(n in t for n in needles):
            return ws
    return None


def read_materials(wb):
    cands = [w for w in (find_sheet(wb, "material"), find_sheet(wb, "purchase")) if w is not None]
    ws = rows = hdr_i = None
    for w in cands:
        rr = list(w.iter_rows(values_only=True))
        hi = next((i for i, r in enumerate(rr)
                   if r and any(str(c or "").strip().lower().startswith("material") for c in r)
                   and any(str(c or "").strip().lower() == "net" for c in r)), None)
        if hi is not None:
            ws, rows, hdr_i = w, rr, hi
            break
    if ws is None:
        return None
    hdr = [str(c or "").strip().lower() for c in rows[hdr_i]]
    ci = next(i for i, h in enumerate(hdr) if h.startswith("material"))
    cu = hdr.index("unit") if "unit" in hdr else None
    cn = hdr.index("net")
    out, section = [], ""
    for r in rows[hdr_i + 1:]:
        name = r[ci] if ci < len(r) else None
        if not name:
            continue
        net = num(r[cn]) if cn < len(r) else None
        unit = norm_unit(r[cu]) if cu is not None and cu < len(r) else ""
        if not unit:
            m_u = re.search(r"\((LF|SF|EA|PCS|LB)\)", str(name), re.I)
            unit = norm_unit(m_u.group(1)) if m_u else ""
        if net is None and not unit:      # encabezado de sección (METAL FRAMING, ...)
            section = str(name).strip()
            continue
        if net is None:
            continue
        out.append({"name": str(name).strip(), "unit": unit, "net": net, "section": section})
    return out


FAMILIAS = [
    # v78: grader completo = también las familias de accesorios (antes caían en "sin familia" y no se
    # calificaban). Van primero: sus renglones no son de stud / track.
    ("extra framing ATM", "lf", r'extra framing', r'atm'),
    ("2-1/2\" CFMF coiling grille head", "lf", r'coiling|grille head', r''),
    ("additional head track", "lf", r'additional head track|add(itiona)?l\.? head track', r''),
    ("stud reinforcement MEP", "pcs", r'reinforcement', r'mep|penetration'),
    ("Level 5 finish", "sf", r'level 5', r''),
    ("gypsum board jamb return", "sf", r'jamb return', r''),
    ("PVC trim at FRP", "lf", r'\bpvc\b', r'trim|molding'),
    ("6\" parapet stud", "lf", r'parapet', r'stud'),
    ("6\" stud (todos los gauges)", "lf", r'^\s*6"', r'stud'),
    ("3-5/8\" stud (todos los gauges)", "lf", r'3-5/8"', r'stud'),
    ("1-5/8\" stud", "lf", r'1-5/8"', r'stud'),
    ("purlin (track to deck)", "lf", r'purlin', r''),
    ("track de ceilings / soffits", "lf", r'track', r'ceiling|soffit'),
    ("bottom track (todos)", "lf", r'bottom', r'track'),
    ("top / deflection track (todos)", "lf", r'\btop\b', r'track'),
    ("header / box beam", "lf", r'header', r''),
    ("sill track", "lf", r'\bsill\b', r''),
    ("bracing C.R. channel", "lf", r'bracing', r'channel'),
    ("framed openings MEP", "lf", r'mep|framed opening', r'opening|track'),
    ("furring channel", "lf", r'furring', r'channel'),
    ("carrying channel", "lf", r'carrying', r'channel'),
    ("hanger wire", "lf", r'hanger', r'wire'),
    ("5/8\" gyp MOISTURE RESISTANT", "sf", r'moisture', r'gyp|board'),
    ("5/8\" EXTERIOR gyp sheathing", "sf", r'exterior', r'gyp.*sheath|sheath.*gyp'),
    ("5/8\" glass mat sheathing", "sf", r'glass mat', r''),
    ("3/8\" gyp board", "sf", r'3/8"', r'gyp'),
    ("ballistic panel", "sf", r'ballistic', r''),
    ("5/8\" gyp board regular (walls + ceilings)", "sf", r'5/8"', r'gyp(sum)? board|board'),
    ("cement board", "sf", r'cement', r''),
    ("FRP", "sf", r'\bfrp\b', r''),
    ("FRT plywood (SF)", "sf", r'plywood', r''),
    ("metal trim (corner bead, casing, shadow molding)", "lf", r'corner bead|casing|shadow|metal trim', r''),
    ("sealant at base of gypsum (exterior)", "lf", r'sealant', r'base of gyp|exterior'),   # v77c U8: familia propia
    ("acoustical sealant", "lf", r'sealant', r''),            # v77c U8: EXCLUIDA (rangos modo "excluir")
    ("metal stud blocking (362CR / STUD BLOCKING)", "lf", r'blocking', r'362cr|stud blocking|metal'),
    ("FRT blocking", "lf", r'blocking', r''),
]


# v61 (arbitraje #11): un renglón de FRT plywood que menciona "jambs/head/sill" no es sill track ni header
# (#11B: <n> LF de "FRT plywood 3/4\" opening liner (jambs/head/sill)" contaron como sill track).
# v62 (arbitraje #12): el calificador clasificaba "5/8\" FRT plywood ... backboards" como 5/8" gyp regular y
# "Framed opening ... (3-5/8\" metal stud)" como 3-5/8" stud (#12A/#12B). Un renglón de plywood / nailbase
# nunca es gyp board; un framed opening nunca es una familia de stud (va a "framed openings MEP").
_FO = r"framed opening"
# v75 (R75.1, arbitraje #23): "Bottom / Top track - ... (vestibule / soffit)" caía en el track de ceilings (primera familia
# que casa) y la familia bottom / top quedaba baja. Un renglón que EMPIEZA con bottom / top es de su familia.
EXCLUYE = {"sill track": r"plywood|liner", "header / box beam": r"plywood|liner",
           "track de ceilings / soffits": r"^\s*(bottom|top)\b",
           "5/8\" gyp board regular (walls + ceilings)": r"plywood|nailbase",
           "6\" parapet stud": _FO, "6\" stud (todos los gauges)": _FO,
           "3-5/8\" stud (todos los gauges)": _FO, "1-5/8\" stud": _FO}


def familia(name, unit):
    n = str(name).lower().replace("”", '"').replace("″", '"')
    u = (unit or "").lower()
    for fam, fu, a, b in FAMILIAS:
        if u == fu and re.search(a, n) and (not b or re.search(b, n)):
            if fam in EXCLUYE and re.search(EXCLUYE[fam], n):
                continue
            return fam
    return None


def por_familia(mats):
    out = {}
    for m in mats:
        f = familia(m["name"], m["unit"])
        if f:
            d = out.setdefault(f, {"net": 0.0, "renglones": []})
            d["net"] += m["net"]
            d["renglones"].append(m["name"])
    return out
