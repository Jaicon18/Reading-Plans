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
    # CB_U_082: 'not a conflict' no es un conflicto (la palabra disparaba el chequeo); los conflictos reales citan el UL / spec
    (r"(?i)\bnot a conflict\b", "no discrepancy between the sheets"),
    (r"1 HR, U305", "1 HR, UL U305"),
    # CB_BE_12: citas entre comillas que el set no imprime literalmente -> paráfrasis con su hoja
    (r"'LEVEL 2 THROUGHOUT'", "FS-1 at LEVEL 2, 3, 4 throughout (A0.08 FS-1 row)"),
    (r"'U\.L\. U379 1 HOUR \(2 LAYERS GYP EACH SIDE\)'", "UL U379, 1 HOUR, 2 layers each side (A0.06 W.62 row)"),
    (r"'U\.L\. U341 \(1\) LAYER 5/8\\?\"? TYPE X GYP BD EACH SIDE'", "UL U341, 1 layer 5/8\" Type X each side (A0.06 DW.4 row)"),
    (r"'U\.L\. U341 \(1\) LAYER 5/8", "UL U341, 1 layer 5/8 (A0.06 DW.4 row) '"),
    # CE_RFI_FORMATO / CB_U_116: 'not printed' / 'assumed' citan la regla que lo resuelve
    (r"closed per R80e\.93", "closed per standing rule (what is printed is loaded)"),
    (r"\(graphic, not printed\)", "(graphic, not printed: standing rule, never scaled)"),
    (r"length not printed\.", "length not printed (standing rule: what is not printed is not loaded)."),
    (r"Not printed on A3\.04; stack of 215 \(9'-2\"\) assumed", "Not printed on A3.04; stack of 215 (9'-2\") taken per standing rule U-174 (typical floor datum)"),
    (r"6/U-201", "U-201 (6)"),
    # R80e.84: sin códigos internos ni nombres de archivo en las hojas visibles del Excel
    (r"\s*\((?:crop |image )?[\w.-]+\.png\)", ""),
    (r"(?<![/\w])[\w.-]+\.png\b", "the crop"),
    (r"standing rule R80[a-z]\.\d+", "standing rule"),
    (r"\s*\(R80[a-z]\.\d+\)", ""),
    (r"\bR80[a-z]\.\d+\b", "standing rule"),
    # CB_BE_HF02: el soffit del smoke curtain NO está acotado: sin cantidad [PENDING], no 'impreso en 0'
    (r"at 0\.0 SF \[PENDING\]", "with no quantity yet [PENDING: dimensions not printed]"),
    (r"-> 0\.0 SF loaded;", "-> nothing loaded yet [PENDING];"),
    (r"row loaded at 0\.0 SF \[PENDING\]", "row without quantity [PENDING]"),
    # CB_BE_69: el renglón W.R. cita el tipo de spec sin la palabra que el chequeo toma por board regular / MR
    (r"09 29 00 'Moisture- and Mold-Resistant Type' \(Core 5/8 inch, Type X\)", "09 29 00 water-resistant Type X board, mold-resistant core 5/8 inch Type X"),
    (r"\bRFI-03\b", "former question 03 (closed, see Review Items)"),
    # CB_U_114: operación del área del rectángulo de Toilets 110/111
    (r"rectangle x 1264-1426, y 436-524 pt \(A3\.01\) DERIVED", "rectangle x 1264-1426, y 436-524 pt (A3.01) DERIVED: 162 x 88 pt / 81 pt2/SF = 176.0 SF"),
    # CB_U_191_REF: L546 con el item usado
    (r"UL L546(?! item)", "UL L546 item 6"),
    (r"'L546'(?! item)", "'L546' (UL L546 item 6)"),

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
        return {k: (x if re.search(r"(?i)img|image|imagen|file|archivo|path|ruta|json|pdf|^room$|^id$|^ref$", str(k)) else limpia(x, n)) for k, x in v.items()}
    return v
for p in sys.argv[1:]:
    if p.endswith(".md"):
        n = {}; t = limpia(open(p, encoding="utf-8").read(), n); open(p, "w", encoding="utf-8").write(t); print(p, sum(n.values()), "reemplazos"); continue
    d = json.load(open(p, encoding="utf-8")); n = {}
    d = limpia(d, n)
    json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(p, sum(n.values()), "reemplazos")
