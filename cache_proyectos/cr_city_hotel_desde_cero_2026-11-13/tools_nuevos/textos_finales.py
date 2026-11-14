#!/usr/bin/env python3
"""Limpieza final de textos (canon tras los parches y takeoff.json tras armar): citas a RFIs que no existen (0 abiertos),
'estimator decision' sin regla citada (CE_ATRIBUCION_ESTIMADOR / U-052: las decisiones de este take-off citan su regla),
nombres de archivo / script en textos del entregable (CB_BE_41) y 'approx' viejo ya superado por el polígono. Uso: textos_finales.py <json>..."""
import json, re, sys
SUST = [
    (r"closed by estimator decision: loaded as printed type, see Review Items\)", "closed per R80e.93 (what is printed is loaded: the type prints the board), see Review Items)"),
    (r"Closed by estimator decision \(", "Closed per R80e.93 / U-161 ("),
    (r"Question withdrawn by estimator decision \(printed UL design governs\)\.", "Question withdrawn per U-191 (the printed UL design governs)."),
    (r"noted; estimator decision: excluded per the printed note\)", "noted; excluded per the printed note, R80e.93)"),
    (r"the sheets do not print it; estimator decision: taken from the bid folder name", "not printed on the sheets; estimator decision 13-nov (user order: bid folder name of the project)"),
    (r"unless RFI-06 says otherwise", "unless a future RFI says otherwise"),
    (r"the old 'RFI-05' citation removed \(no such open RFI\)", "an old citation to a nonexistent RFI removed"),
    (r"'RFI-05' citation removed", "old citation to a nonexistent RFI removed"),
    (r"\bRFI-(0\d|1\d)\b(?! *\()", r"former question \1 (closed, see Review Items)"),
    (r"rcp_polys\.json area_poly_sf must read", "the RCP polygon area reads"),
    (r"\bcanon\.py has no", "the take-off engine has no"),
    (r"(?<![/\w])[A-Za-z_]+\.(?:py|json)\b", "the take-off tool"),
    (r"minus elevator shaft approx (\d+) SF \(DERIVED\)", r"minus elevator shaft (superseded: the area is the RCP polygon, see below)"),
    (r"delta approx -", "delta -"),
    # CH.2 L2/L3: la altura máxima del listing (54'-0") no es la altura cargada (CE_ALTURA_IMPRESA / U-191: no citar el listing sin Item)
    (r"\(7/A9\.03 assembly max\. height 54'-0\"; 10/A9\.03 head above LEVEL 4\)", "(7/A9.03 shaftwall; 10/A9.03 head above LEVEL 4)"),
    (r"\('2-HOUR SHAFTWALL ASSEMBLY \(W419, U497\) max\. height - 54'-0\"' 7/A9\.03;", "('2-HOUR SHAFTWALL ASSEMBLY' 7/A9.03;"),
    (r"\(A0\.06 C-H detail / W419\)", "(A0.06 C-H detail)"),
    # walls agregados por un parche posterior al normalizador: la fuente de la altura L2/L3 sin la hoja comodín A5.0x (CE_CITA_ALTURA)
    (r"DERIVED 9'-3 1/2\" = 11'-0\" L2 floor-to-floor \(LEVEL 2 6211\.75' / LEVEL 3 6222\.75', A4\.00/A5\.01\) - 1'-8 1/2\" floor assembly \(1 3/4\" topping \+ 3/4\" sheathing \+ 18\" trusses, A5\.0x\)",
     "DERIVED 9'-3 1/2\" = 11'-0\" (LEVEL 2 6211.75' / LEVEL 3 6222.75', 2/A4.03, 1/A5.06) - 20.5\" floor structure (1 1/2\" topping + 1/4\" acoustic underlayment A0.08, 3/4\" sheathing + 18\" trusses S1.02)"),
]
def limpia(v, n):
    if isinstance(v, str):
        for a, b in SUST:
            v2 = re.sub(a, b, v)
            if v2 != v:
                n[a] = n.get(a, 0) + 1; v = v2
        return v
    if isinstance(v, list):
        return [limpia(x, n) for x in v]
    if isinstance(v, dict):
        return {k: (x if re.search(r"(?i)img|image|imagen|file|archivo|path|ruta|json|pdf", str(k)) else limpia(x, n)) for k, x in v.items()}
    return v
for p in sys.argv[1:]:
    d = json.load(open(p, encoding="utf-8")); n = {}
    d = limpia(d, n)
    json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(p, sum(n.values()), "reemplazos")
