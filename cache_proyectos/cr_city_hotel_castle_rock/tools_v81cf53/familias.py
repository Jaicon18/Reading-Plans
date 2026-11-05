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
    ("metal stud brace to structure (printed)", "lf", r"brace to structure", r""),   # BE-HF12
    ("spacing bar at the brace line (printed)", "lf", r"spacing bar", r""),
    # v78: grader completo = también las familias de accesorios (antes caían en "sin familia" y no se
    # calificaban). Van primero: sus renglones no son de stud / track.
    ("Kwik HUS-EZ anchors", "pcs", r"hus-?ez", r""),   # v80r
    ("#10-16 screws at moment clips", "pcs", r"#10-16 screws at the moment", r""),   # v80r
    ("moment clip (types 3/4 base)", "pcs", r"moment clip", r""),   # v80r
    ("metal corner guard 2x2x72", "pcs", r"metal corner guard", r""),   # v80r
    ("stainless corner guard 48", "pcs", r"stainless steel corner guard", r""),   # v80r
    ("control joint", "lf", r"control joint", r""),   # v80r
    ("#8 screws at brace ends", "pcs", r"#8 screws at diagonal brace", r""),   # v80r
    ("Tek screws at clip angles", "pcs", r"tek screws.*clip angle", r""),   # v80o (BE-16 / BE-46)
    ("track brace at strut splice (printed)", "lf", r"track brace at strut splice", r""),   # R80e.80
    ("storefront structural framing (printed)", "lf", r"storefront structural framing", r""),   # R80e.100
    ("demolition - gypsum board and metal framing", "sf", r"demolition", r"gyp|board|stud|framing|partition|ceiling|soffit|furring"),   # R80e.116
    ("metal reveal trim (printed)", "lf", r"metal reveal trim", r""),   # R80e.107
    ("sheet metal backing plate (printed)", "pcs", r"sheet metal backing plate", r""),   # R80e.107
    ("metal FRP trim (printed)", "lf", r"metal frp (?:top|trim)", r""),   # R80e.107
    ("EMT compression strut 1.5\" dia x 20 GA, ceiling lateral bracing (printed)", "lf", r"emt compression strut 1\.5", r""),   # R80e.127
    ("EMT compression strut 1.25\" dia x 20 GA, ceiling lateral bracing (printed)", "lf", r"emt compression strut 1\.25", r""),   # R80e.127
    ("W-4 panel trim and edge molding (printed)", "lf", r"w-4 panel trim", r""),   # R80e.89
    ("resilient channel (printed)", "lf", r"resilient channel", r""),   # R80e.78
    ("1/4\" gypsum board (printed)", "sf", r"1/4\" gypsum board", r""),
    ("flat strap bracing (printed)", "lf", r"flat strap", r""),
    ("Z-furring runner track (printed)", "lf", r"z-furring runner", r""),
    ("sanitary wall panels (printed)", "sf", r"sanitary wall", r""),
    ("concrete screw anchors, bottom track (printed)", "pcs", r"concrete screw anchors", r""),   # R80e.75
    ("#10 framing screws (printed)", "pcs", r"#10 framing screws", r""),
    ("deep-leg slotted deflection track (printed)", "lf", r"deep-leg slotted", r""),
    ("alkali-resistant mesh tape (printed)", "lf", r"alkali-resistant .*mesh tape", r""),   # R80w.41
    ("setting-type joint compound at cement board (printed)", "lb", r"setting-type joint compound at cement", r""),   # v81cf8 (T3)
    ("sealer gasket (printed)", "lf", r"sealer gasket", r""),   # R80w.41
    ("sheathing screws (printed)", "pcs", r"sheathing screws", r""),
    ("framing clips per stud (printed)", "pcs", r"framing clips per stud", r""),
    ("clip angle (bracing / nested connections)", "pcs", r"clip angle", r""),   # v80n R80e.27
    ("16 ga wire (seismic brace points)", "lf", r"16 ga wire", r""),   # v80o (BE-16 / BE-46)
    ("#8 pan head screws, relief channel to structure", "pcs", r"#8 pan head", r""),   # v80o (BE-16/19): 8/A-410 manda sobre 8.C
    ("P.A.F. at cross members", "pcs", r"p\.a\.f\.", r"cross member"),   # v80o
    ("5/8\" cement board", "sf", r"5/8\" cement board", r""),   # v80o (BE-46): un espesor por renglón
    ("plywood screws (Teks/3)", "pcs", r"plywood screw", r""),   # v80n R80e.27
    ("cement board screws", "pcs", r"cement board screw", r""),   # v80n R80e.27
    ("nested inner runner (deflection head)", "lf", r"nested inner runner", r""),   # v80n R80e.27
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
    ("1-1/2\" Z-furring", "lf", r'z-furring|\bzf\b|150zf|hat channel, vertical furring', r''),   # R80e.65 (antes de "furring channel"); BE-HF1 hat channel label
    ("purlin (track to deck)", "lf", r'purlin', r''),
    ("ceiling / soffit track 3-5/8\"", "lf", r'^track 3-5/8"', r''),   # v80p (R80e.31): track de ceilings por tamaño
    ("ceiling / soffit track 6\"", "lf", r'^track 6"', r''),
    ("ledger track 8\"", "lf", r'^8" ledger track', r''),
    ("#8 screws, top chord / cross members (typ. connection)", "pcs", r'#8 screws.*top chord', r''),
    ("track de ceilings / soffits", "lf", r'track', r'ceiling|soffit'),
    ("bottom track (todos)", "lf", r'bottom', r'track'),
    ("top / deflection track (todos)", "lf", r'\btop\b', r'track'),
    ("header / box beam", "lf", r'header', r''),
    ("sill track", "lf", r'\bsill\b', r''),
    ("bracing C.R. channel", "lf", r'bracing', r'channel'),
    ("8\" joist", "lf", r'8" (metal )?joist', r''),   # v80f R80e.20
    ("USG drywall main tee (DGLW26)", "lf", r'main tee', r''),
    ("USG drywall cross tee (DGLW424)", "lf", r'cross tee', r''),
    ("curved perimeter molding (printed)", "lf", r'curved .*molding', r''),   # R80w.35
    ("USG channel molding (DGCM27)", "lf", r'channel molding', r''),
    ("USG angle molding (DGWM24)", "lf", r'angle molding', r''),
    ("framed openings MEP", "lf", r'mep|framed opening', r'opening|track'),
    ("furring channel", "lf", r'furring', r'channel'),
    ("carrying channel", "lf", r'carrying', r'channel'),
    ("hanger wire", "lf", r'hanger', r'wire'),
    ("5/8\" EXTERIOR gyp sheathing Type X", "sf", r'exterior', r'type x'),   # v81cf53 (antes de Type X)
    ("1\" gypsum shaftliner panel", "sf", r'shaftliner|shaft liner', r''),   # v81cf53
    ("5/8\" gyp board Type C", "sf", r'type c\b', r'gyp|board'),   # v81cf53
    ("C-H stud 2-1/2\" (printed)", "lf", r'c-h stud 2-1/2', r''), ("C-H stud 4\" (printed)", "lf", r'c-h stud 4"', r''),
    ("C-H stud 6\" (printed)", "lf", r'c-h stud 6"', r''), ("J-runner 2-1/2\" (printed)", "lf", r'j-runner 2-1/2', r''),
    ("J-runner 4\" (printed)", "lf", r'j-runner 4"', r''), ("J-runner 6\" (printed)", "lf", r'j-runner 6"', r''),
    ("5/8\" gyp Type X W.R.", "sf", r'type x', r'w\.r\.|water'),   # v80f R80e.18
    ("5/8\" gyp board Type X", "sf", r'type x', r'gyp|board'),
    ("1/2\" gyp MOISTURE RESISTANT", "sf", r'1/2"', r'moisture'),   # R80e.111
    ("5/8\" gyp FOIL-BACKED", "sf", r'foil', r'gyp|board'),   # R80e.111
    ("5/8\" gyp ceiling board SAG-RESISTANT", "sf", r'sag[- ]resistant', r'gyp|board'),   # v81cf8 (T2)
    ("5/8\" gyp MOISTURE RESISTANT", "sf", r'moisture', r'gyp|board'),
    ("1/2\" EXTERIOR gyp sheathing", "sf", r'1/2"', r'exterior.*sheath|sheath.*exterior'),   # v80f R80e.16
    ("5/8\" EXTERIOR gyp sheathing", "sf", r'exterior', r'gyp.*sheath|sheath.*gyp'),
    ("5/8\" glass mat sheathing", "sf", r'glass mat', r''),
    ("3/8\" gyp board", "sf", r'3/8"', r'gyp'),
    ("1/2\" gyp board", "sf", r'1/2"\s*(?:regular\s*)?(?:gyp|gypsum)(?!.*(?:exterior|sheathing))', r''),   # v80wCF
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
           "3-5/8\" stud (todos los gauges)": _FO, "1-5/8\" stud": _FO, "1-1/2\" Z-furring": _FO,
           "5/8\" gyp board Type X": r"moisture"}   # R80w.45: "Type X MR (moisture resistant)" es la familia MR


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
