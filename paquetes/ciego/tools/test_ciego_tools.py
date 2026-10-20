#!/usr/bin/env python3
"""test_ciego_tools.py — E24 (protocolo ciego) aplicado a las TOOLS del skill.

Chequeo GENÉRICO por patrones: no usa ninguna lista de valores de examen ni lee resultados de pruebas.
Reusa los patrones P1–P4 de test_ciego_v69 (P5 se omite: el código de las tools usa coordenadas y
decimales de tolerancia legítimos).

  A) comentarios (tokens COMMENT de tokenize) y docstrings (primer statement string de módulo / clase /
     función, vía ast) -> P1 proyecto, P2 cantidad, P3 miles, P4 resultado;
  B) TODO el texto del archivo (código incluido) -> P1 estricto: nombre o ruta de trabajo de un proyecto de
     prueba (prefijos de archivo incluidos), sin confundirlo con palabras del oficio ("BOARD").

Excepciones GENÉRICAS de P2/P4 (no dependen de ningún proyecto; cada una es una regla de forma):
  - umbral / tolerancia: el número va justo después de ±, +/-, >, <, >=, <= o "dentro de" (0.05 ft, 0.5 %);
  - cero: "0 LF", "0 SF"… (un cero no es una cantidad medida de ningún proyecto);
  - parte decimal de un id de regla ("R71.5 tag": el 5 va pegado a un punto);
  - conversión de hoja: "AxB … N SF" con N = A·B en la misma línea ("4x8 sheet = 32 SF").
Una línea con el marcador `[ciego-ok]` se permite (criterio general que necesita el número; se revisa a mano).

v73 (arbitraje #21): también test_*.py y fixtures (antes se saltaban), y sobre los LITERALES de texto y número:
  P6 room real: texto con room / office / restroom / corridor… + número 1xx, o el valor de "room" = 1xx
     (los datos sintéticos usan rooms 9xx);
  P7 wall ID real: literal con forma de id de wall de un type de planta "<type>-<n>", "<type>K-<n>",
     "<type>-<n><letra>", "EXT-<grid>-<n>" (type = letra A–H con dígito opcional; los sintéticos usan X / Y / Z / W);
  P8 cantidad de una referencia: un literal numérico igual (±0.0005) a un valor de la lista EXTERNA de valores de
     examen (`--valores <json>` o $CIEGO_VALORES). La lista vive FUERA del paquete (la arma el árbitro); sin
     lista, P8 solo corre su autoprueba.

v74 (--estricto, sobre SKILL.md + referencias/ + comentarios / docstrings / textos de las tools de producción):
  P17 conteo de una corrida: "<n> sin abrir", "contra <n>", "<n> de <n>", "<n> sellos", "de <n> a <n>";
  P18 porcentaje concreto (no umbral, no 0 / 100 %, no criterio de waste / margen) en una adenda;
  P19 nombre de archivo con prefijo de wall / punto del set ("<LETRAS><nn>_algo"), id "UU<n>", "<type> a <n> deg";
  P20 fecha absoluta (AAAA-MM-DD, D-mes, MM/DD/AAAA) en referencias/;
  P21 coordenada pt con dos decimales (<nnn(n)>.<nn>);
  P22 título de detalle en MAYÚSCULAS (3+ palabras) pegado a una cita N/HOJA (la cita sola es genérica).
Cada patrón nuevo tiene muestra mala (armada en ejecución, números inventados) y buena en la autoprueba.

Uso:  python3 test_ciego_tools.py            autoprueba sintética + barrido de la carpeta de este archivo
      python3 test_ciego_tools.py a.py b.py  solo esos archivos (más la autoprueba)
rc 0 = OK; rc 1 = hallazgos (archivo:línea: patrón: texto).
"""
import ast
import io
import os
import re
import sys
import tokenize

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_ciego_v69 import PATRONES, OK  # noqa: E402

PATRONES_TXT = [(et, rx) for et, rx in PATRONES if not et.startswith("P5")]
P1_ESTRICTO = ("P1 estricto", re.compile(r"BOA(?!RD)|\bBofA\b|Broomfield|Bank of America|Greeley"
                                         r"|/home/claude/boa|/home/user/boa|boa20", re.I))


P6 = re.compile(r"(?i)\b(room|office|restroom|corridor|break ?room|break|storage|janitor|vestibule|lobby|wellness|"
                r"electrical|work ?room|men|women|cash window|teller|calling|calling cubes)\b[^\n\"']{0,15}?\b1\d\d[A-Z]?\b")
# v73b: en los .md (SKILL + referencias/) además: nombre propio de room de un set ("Calling Cubes", "Cash Window") y
# número de wall suelto junto a un type ("A1 #3", "del #2", "este del #7"); los genéricos usan "#n" / "[room]".
P6_MD = re.compile(r"\b(Calling Cubes|CALLING CUBES|Cash Window|CASH WINDOW)\b")   # nombre propio, no el tipo de abertura
P7_MD = re.compile(r"(?:\b[A-H]\d?K?\s*#\d+\b|\b(?:del|al|el|wall|y)\s+#\d+\b)")
# v73c: en español o sin palabra de room delante: baño / puerta / fila / vestíbulo / muro / wall / door + número; un 1xx
# entre comillas o corchetes; un id de cierre del set (PALABRA-nn); cualquier número en un renglón de "Ejemplo real".
P9_MD = re.compile(r"(?i)\b(baño|bano|fila|vest[ií]bulo|cuarto|sala|room)\s+#?1\d\d\b"
                   r"|\b(puerta|muro|wall|door)\s+#?(1\d\d|\d{2})\b"
                   r"|['\"`\[]1\d\d[A-Z]?['\"`\]]|\bCIELO-\d+\b|\bal 1\d\d\b")
# v73d (--estricto, zip ciego): cualquier número junto a wall / muro / door / puerta / room / canopy / cielo / fila / tag;
# ids de cierre PALABRA-nn; nombres BOA_*; [ciego-ok] solo vale en tablas genéricas con fuente de fabricante.
P11_EST = re.compile(r"(?i)\b(walls?|muros?|doors?|puertas?|rooms?|canopy|cielos?|filas?|tags?)\s*#?\[?\d+(?![\w.])|"
                     r"(?<![\w./])(?![1-3]\s+walls\b)\d+\s*(?:walls?|muros?|doors?|puertas?|rooms?|tags?)\b")
P12_EST = re.compile(r"\b(?!RFI-|ALC-|ADV|GA-|LEVEL-|ISO-|ASTM-)[A-Z]{2,}-\d+[A-Z]?\b")
P13_EST = re.compile(r"B" + r"OA_")
# v73e: conteos del set (hojas, detalles, callouts, pendientes, páginas, MB), coordenadas "x / y nnn(.nn)" y floats en
# los textos de ejemplo del código de producción
P14_EST = re.compile(r"(?i)(?<![\w./])\d{2,}(?:\.\d+)?\s*(?:hojas|detalles|callouts|pendientes|p[aá]ginas|pages|sheets|"
                     r"details|MB)\b|\b(?:hojas|detalles|callouts|pendientes|p[aá]ginas?)\s+\d{2,}\b|~\s?\d{2,}\s*hojas")
P15_EST = re.compile(r"\b[xy]\s*=?\s*\d{3,4}\.\d{1,2}\b|\b\d{3,4}\.\d{2}\s*/\s*\d{3,4}\.\d{2}\b")
P16_EST = re.compile(r"(?<![\w./])\d{2,4}\.\d{1,3}(?![\w./])")      # float en un texto de ejemplo (solo textos)
# v74: conteos de una corrida, porcentajes de resultado, nombres / ids / ángulos del set, fechas, coordenadas pt y
# títulos reales de detalle junto a su cita (formas genéricas: ningún número de un set)
P17_EST = re.compile(r"(?i)(?<![\w./])\d+\s*[\"“”']?\s*sin abrir\b|\bcontra\s+\d+(?![\w./\"'%]|\s*(?:pt|ft|in|LF|SF)\b)"
                     r"|(?<![\w./<])\d+\s+de\s+\d+(?![\w./\"'%])|(?<![\w./])\d+\s+sellos\b"
                     r"|\b(?:de|desde)\s+\d{2,}\s+a\s+\d+(?![\w./\"'%])")
P18_EST = re.compile(r"(?<![\w./])\d+(?:[.,]\d+)?\s?%")
_P18_OK = re.compile(r"(?i)waste|merma|margen|tolerancia|umbral|tope|m[aá]ximo|m[ií]nimo|metal|board")
P19_EST = re.compile(r"\b[A-Z]{1,8}\d{2,}_[A-Za-z]\w*|\bUU\d+\b|\b[A-H]\d?K?\s+a\s+\d+\s*(?:deg|°|grados)\b")
P20_EST = re.compile(r"(?i)\b(?:19|20)\d{2}-\d{2}-\d{2}\b|\b\d{1,2}/\d{1,2}/(?:19|20)\d{2}\b"
                     r"|\b\d{1,2}-(?:ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic|jan|apr|aug|dec)[a-z]*\b")
P21_EST = re.compile(r"(?<![\w./])\d{3,4}\.\d{2}(?![\w/])")
P22_EST = re.compile(r"\b\d{1,2}/[A-Z]{1,2}-?\d{1,3}\.\d{1,3}`?\s+(?:@\s+|[A-Z][A-Z0-9/&.,'()-]+\s+){2,}"
                     r"(?:@\s+)?[A-Z][A-Z0-9/&.,'()-]+")
OK_FABRICANTE = re.compile(r"(?i)AISC|GA-216|ASTM|manufacturer|fabricante|SSMA|UL ?\d")
ESTRICTO = [False]
_REGLA_ID = re.compile(r"^(4[4-9]|5\d|60)\.\d{1,2}$")       # REGLA 44.1 … 60.11 (numeración de reglas del SKILL)


def _exento_estricto(et, ln, m):
    """Excepciones GENÉRICAS del modo estricto: número de regla, medida en grilla de 1/8" (constante del oficio) y
    umbral ("~40 hojas", "más de 40 hojas")."""
    t = m.group(0).strip()
    if et.startswith("P16"):
        if _REGLA_ID.match(t) or ln[max(0, m.start() - 6):m.start()].upper().endswith("REGLA "):
            return True
        v = float(t)
        return abs(v * 8 - round(v * 8)) < 1e-6 and v < 100                  # 14.375 = 14 3/8 (genérico)
    if et.startswith("P14"):
        return bool(re.search(r"(~|más de|mas de|>|≥|pasa de)\s*$", ln[max(0, m.start() - 9):m.start()]))
    antes = ln[max(0, m.start() - 12):m.start()]
    if et.startswith("P17") and (re.search(r"(?i)\b(paso|etapa|step)[\s*]*$", antes)
                                 or re.match(r"0\s", t)):
        return True                                             # "paso <n> de <n>" del protocolo; "0 sellos rotos"
    if et.startswith(("P17", "P18")) and re.search(r"(±|\+/-|[<>]=?|≤|≥|dentro de|hasta|más de|mas de|~)\s*$", antes):
        return True                                                            # umbral / tolerancia
    if et.startswith("P18"):
        v = float(re.match(r"[\d.,]+", t).group(0).replace(",", "."))
        return v in (0, 100) or bool(_P18_OK.search(ln))                      # 0 / 100 % o criterio de compra
    if et.startswith("P21"):
        return bool(_REGLA_ID.match(t))
    return False
P10_MD = re.compile(r"(?i)ejemplo real[^\n]*?\b\d{2,}\b")
P6_VALOR = re.compile(r"^1\d\d[A-Z]?$")
P7 = re.compile(r"^(?:[A-H]\d?K?|EXT-\d+)-\d{1,2}[a-z]?$")
_VALORES = None


def valores(path=None):
    """Lista externa de valores de examen (P8); None si no hay."""
    global _VALORES
    path = path or os.environ.get("CIEGO_VALORES")
    if path and os.path.isfile(path):
        import json
        _VALORES = sorted(float(x) for x in json.load(open(path, encoding="utf-8")))
    return _VALORES


def revisar_literales(texto, nombre="<texto>", vals=None):
    """P6 / P7 sobre literales de texto y P8 sobre literales numéricos (ast)."""
    hall = []
    lineas = texto.splitlines()
    try:
        arbol = ast.parse(texto)
    except SyntaxError:
        return hall
    claves_room = set()
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Dict):
            for k, v in zip(nodo.keys, nodo.values):
                if isinstance(k, ast.Constant) and k.value in ("room", "rooms") and isinstance(v, ast.Constant):
                    claves_room.add(id(v))
    for nodo in ast.walk(arbol):
        if not isinstance(nodo, ast.Constant) or OK in lineas[nodo.lineno - 1]:
            continue
        v = nodo.value
        if isinstance(v, str):
            m = P6.search(v)
            if m or (id(nodo) in claves_room and P6_VALOR.match(v.strip())):
                hall.append(f"{nombre}:{nodo.lineno}: P6 room real: {v[:60]!r}")
            elif P7.match(v.strip()):
                hall.append(f"{nombre}:{nodo.lineno}: P7 wall ID real: {v!r}")
        elif isinstance(v, float) and vals:
            import bisect
            i = bisect.bisect_left(vals, v - 0.0005)
            en_grilla = abs(v * 48 - round(v * 48)) / 48 <= 0.0035     # cota de pies-pulgadas a 1/4" (genérica)
            if i < len(vals) and abs(vals[i] - v) <= 0.0005 and not en_grilla:
                hall.append(f"{nombre}:{nodo.lineno}: P8 cantidad de la referencia: {v}")
    return hall


_UMBRAL = re.compile(r"(±|\+/-|[<>]=?|≤|≥|dentro de)\s*$")
_HOJA = re.compile(r"\b(\d{1,2})\s?x\s?(\d{1,2})\b")


def _generico(et, frag, m):
    """True si el hallazgo P2/P4 es una de las excepciones genéricas (ver docstring)."""
    if not (et.startswith("P2") or et.startswith("P4")):
        return False
    txt = m.group(0)
    num = re.match(r"[\d.,]+", txt)
    if _UMBRAL.search(frag[max(0, m.start() - 12):m.start()]):
        return True
    if num and re.fullmatch(r"0+(\.0+)?", num.group(0).rstrip(",")):
        return True
    if m.start() > 0 and frag[m.start() - 1] == ".":
        return True
    if num and re.search(r"walls?\b", txt) and float(num.group(0).rstrip(",") or 9) <= 3:
        return True                                   # regla de corte ("= 1 wall", "2 walls"), no un conteo de obra
    if num and re.search(r"\bSF\b", txt):
        n = float(num.group(0).replace(",", ""))
        if any(int(a) * int(b) == n for a, b in _HOJA.findall(frag)):
            return True
    return False


def _p1_estricto_ok(linea, m):
    # "board", "Board", "BOARD"… ya excluidos por (?!RD) en mayúsculas; con re.I hay que excluir el resto
    return m.group(0).lower() == "boa" and linea[m.end():m.end() + 2].lower() == "rd"


def _docstring_lineas(arbol):
    out = set()
    for nodo in ast.walk(arbol):
        if isinstance(nodo, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            cuerpo = getattr(nodo, "body", [])
            if cuerpo and isinstance(cuerpo[0], ast.Expr) and isinstance(cuerpo[0].value, ast.Constant) \
                    and isinstance(cuerpo[0].value.value, str):
                d = cuerpo[0]
                out.update(range(d.lineno, (d.end_lineno or d.lineno) + 1))
    return out


def revisar_fuente(texto, nombre="<texto>"):
    hall = []
    lineas = texto.splitlines()

    def cita(n, et, frag, m):
        hall.append(f"{nombre}:{n}: {et}: …{frag[max(0, m.start() - 40):m.end() + 40].strip()}…")

    # A) comentarios + docstrings
    fragmentos = []                                    # (línea, texto)
    try:
        for tok in tokenize.generate_tokens(io.StringIO(texto).readline):
            if tok.type == tokenize.COMMENT:
                fragmentos.append((tok.start[0], tok.string))
    except (tokenize.TokenError, IndentationError) as e:
        hall.append(f"{nombre}:0: tokenize: {e}")
    try:
        for n in sorted(_docstring_lineas(ast.parse(texto))):
            fragmentos.append((n, lineas[n - 1]))
    except SyntaxError as e:
        hall.append(f"{nombre}:{e.lineno}: ast: {e.msg}")
    vistos = set()
    for n, frag in fragmentos:
        if OK in lineas[n - 1]:
            continue
        for et, rx in PATRONES_TXT:
            for m in rx.finditer(frag):
                if (n, et) in vistos or _generico(et, frag, m):
                    continue
                vistos.add((n, et))
                cita(n, et, frag, m)
    # B) P1 estricto en todo el archivo
    et, rx = P1_ESTRICTO
    for n, linea in enumerate(lineas, 1):
        if OK in linea:
            continue
        for m in rx.finditer(linea):
            if not _p1_estricto_ok(linea, m):
                cita(n, et, linea, m)
                break
    return hall


def autoprueba():
    malo = ('# caso real: 123 LF de blocking en el proyecto\n'          # cifras SINTÉTICAS
            'def f():\n'
            '    """Prueba #1: 11.1 % de materials; 1,234 SF."""\n'
            '    return 0\n'
            'PDF = "/home/claude/boa/x.pdf"\n'
            'X = "BOA_SIN_MARKUPS.pdf"\n')
    bueno = ('# Header: R.O. + 1\'-4" (8" de bearing por lado), 16" O.C., cita 2/S5.20\n'
             'def g():\n'
             '    """Escala 1/4"=1\'-0" -> 18 pt/ft. Barrido de BOARD por cara."""\n'
             '    return {"x": 1234.5, "tol": 0.005, "BOARD": "5/8 board"}\n'
             'Y = "4x8 sheet = 32 SF"  # [ciego-ok] conversión de unidad de compra\n'
             '# tolerancia ± 0.05 ft; si difiere > 0.25 ft, RFI; sumas dentro de 0.5 %; NOT_FRAMED -> 0 LF\n'
             '# regla R71.5 tag descartado; "4x8 sheet" -> 32 SF por pieza\n')
    hm, hb = revisar_fuente(malo, "malo"), revisar_fuente(bueno, "bueno")
    lineas_malas = {h.split(":")[1] for h in hm}
    assert lineas_malas == {"1", "3", "5", "6"}, hm
    assert any("P3" in h for h in hm) and any("P4" in h for h in hm), hm
    assert hb == [], hb
    n1, n2 = "1" + "97", "1" + "98"              # números INVENTADOS armados en ejecución (no son de ningún set)
    lit_malo = ('W = {"id": "' + "D" + '7-4", "room": "' + n1 + '", "location": "Office ' + n2 + ' north"}\n'
                'L = 12.345\n')
    lit_bueno = ('W = {"id": "X1-5", "room": "913", "location": "Office 908 north", "ref": "RFI-1", "s": "R-1"}\n'
                 'L = 12.5\nAISC = 7.5  # [ciego-ok] tabla\n')
    hl = revisar_literales(lit_malo, "lm", [12.345])
    assert {h.split(": ")[1] for h in hl} >= {"P6 room real", "P7 wall ID real", "P8 cantidad de la referencia"}, hl
    assert revisar_literales(lit_bueno, "lb", [12.345]) == [], revisar_literales(lit_bueno, "lb", [12.345])
    md_malo = ("La face ESTE es " + "Cash " + "Window 9" + "08.\nD7 #" + "8 contra la face OESTE del #" + "9.\nBreak "
               + n1 + " al sur.\nBOARD_WR:baño " + n2 + ".\nEjemplo real: puerta " + n1 + ".\n['" + n2
               + "'] sin resolver.\n")
    md_bueno = "La face ESTE es [room].\nA1 #n contra la face OESTE del #n. Ver 6/A12.01 y §4; regla #0.\n"
    assert len(revisar_md(md_malo, "m")) == 6, revisar_md(md_malo, "m")
    assert revisar_md(md_bueno, "b") == [], revisar_md(md_bueno, "b")
    # P7: las cuatro formas de id de wall de un set, armadas en ejecución (type inventado, números inventados)
    for forma in ("G" + "4-7", "G" + "4K-7", "G" + "4-7b", "EXT-" + "6-2"):
        assert P7.match(forma), forma
    assert not any(P7.match(x) for x in ("X1-1", "WZ", "RFI-1")), "P7 falso positivo"
    # v74: P17–P22 (modo estricto), una muestra mala y una buena por patrón; números armados en ejecución
    a, b, c = "6" + "3", "1" + "7", "2" + "9"
    malos = {
        "P17": ["la compuerta contaba " + a + ' "sin abrir"', "salía " + b + " muere contra " + c,
                "leía " + b + " de " + c + " renglones", "los " + a + " sellos intactos", "bajó de " + a + "1 a " + b],
        "P18": ["selladas (" + a + "%) sin cita", "primera versión: **" + c + "%**"],
        "P19": ["G" + b + "_cierre.json", "PUNTOS" + a + "_cierres.json", "UU" + b[0] + " dibujados",
                "wall diagonal (F a " + c + " deg)"],
        "P20": ["la regla del " + b + "-sep-20" + c, "vigente al 20" + c + "-0" + b[1] + "-" + b, "IF Permit 0"
                + b[1] + "/" + c + "/20" + b],
        "P21": ["burbuja en " + a + b + "." + c + " pt"],
        "P22": ["ver `" + b[0] + "/A" + c + ".0" + b[1] + " TYPICAL BULKHEAD TRANSITION DETAIL` arriba"],
    }
    buenos = ["cada tag en su wall; la compuerta revisa contra el plano",           # P17
              "margen del 5% en B; dentro de 0.5 %; tolerancia ± 2 %; en 0%",      # P18
              "MEP_cierre.json y PUNTOS_cierres.json; tag XX3; wall diagonal (ni H ni V)",  # P19
              "versión v74 del protocolo; ver regla R74.2 y REGLA 55.7",            # P20
              "a 1/4\"=1'-0\" son 18 pt/ft; 5/8\" = 11.25 pt; hoja A12.01; REGLA 56.10",    # P21
              "cita 7/A09.26 y 5/S5.20; detalle `N/HOJA <título del detalle>`; 5/8\" GYP. BD. @ 16\" O.C.",  # P22
              "LA COMPUERTA: verif_caras.py (paso 12 de 17); hasta 3 de 5 casos"]
    ESTRICTO[0], previo = True, ESTRICTO[0]
    try:
        for et, muestras in malos.items():
            for s in muestras:
                h = revisar_md(s, "referencias/adenda_v99.md")
                assert any(et in x for x in h), (et, s, h)
        for s in buenos:
            h = revisar_md(s, "referencias/adenda_v99.md")
            assert h == [], (s, h)
    finally:
        ESTRICTO[0] = previo
    return ("autoprueba OK (4/4 líneas malas detectadas, P6/P7/P8 en literales, P17–P22 estrictos, "
            "0 falsos positivos)")


def revisar_md(texto, nombre="<md>"):
    """v73b: P6 / P7 / P8 sobre el texto de SKILL.md y referencias/*.md (antes solo lo revisaba test_ciego_v69, que no
    tiene rooms ni números de wall)."""
    hall = []
    for n, ln in enumerate(texto.splitlines(), 1):
        if OK in ln and not (ESTRICTO[0] and not OK_FABRICANTE.search(ln)):
            continue
        if ESTRICTO[0]:
            pats = [("P11 número junto a wall/door/room/tag", P11_EST), ("P12 id de cierre del set", P12_EST),
                    ("P13 nombre con prefijo de proyecto", P13_EST), ("P14 conteo del set", P14_EST),
                    ("P15 coordenada", P15_EST), ("P17 conteo de una corrida", P17_EST),
                    ("P19 nombre / id / ángulo del set", P19_EST), ("P21 coordenada pt", P21_EST),
                    ("P22 título de detalle junto a su cita", P22_EST)]
            if "adenda_v" in nombre:
                pats.append(("P18 porcentaje de resultado", P18_EST))
            if "referencias" in nombre:
                pats.append(("P20 fecha absoluta", P20_EST))
            if nombre.endswith("(textos)") and not OK_FABRICANTE.search(ln):
                pats.append(("P16 float en texto de ejemplo", P16_EST))
            for et, rx in pats:
                m = next((x for x in rx.finditer(ln) if not _exento_estricto(et, ln, x)), None)
                if m:
                    hall.append(f"{nombre}:{n}: {et}: …{ln[max(0, m.start() - 30):m.end() + 30].strip()}…")
                    break
        for et, rx in (("P6 room real", P6), ("P6 room real", P6_MD), ("P7 wall ID real", P7_MD),
                       ("P9 room / door / wall real", P9_MD), ("P10 ejemplo real con número", P10_MD)):
            m = rx.search(ln)
            if m:
                hall.append(f"{nombre}:{n}: {et}: …{ln[max(0, m.start() - 30):m.end() + 30].strip()}…")
                break
        if _VALORES:
            import bisect
            for m in re.finditer(r"(?<![\d.])\d+\.\d{2,3}(?![\d])", ln):
                v = float(m.group(0))
                if re.search(r"(?i)(regla|\()\s*$", ln[max(0, m.start() - 7):m.start()]) or \
                        ln[max(0, m.start() - 4):m.start()].rstrip().endswith(("/A", "A", "S", "/S")) or \
                        re.search(r"[A-Z]\d{0,2}$", ln[max(0, m.start() - 3):m.start()]):
                    continue                                   # número de hoja (A12.01, S5.20)
                i = bisect.bisect_left(_VALORES, v - 0.0005)
                if i < len(_VALORES) and abs(_VALORES[i] - v) <= 0.0005 and \
                        abs(v * 48 - round(v * 48)) / 48 > 0.0035:
                    hall.append(f"{nombre}:{n}: P8 cantidad de la referencia: {m.group(0)}")
    return hall


def _comentarios(texto):
    """Texto de comentarios y docstrings (los renglones que no lo son quedan vacíos: los números de línea se conservan)."""
    lineas = texto.splitlines()
    keep = set()
    try:
        for tok in tokenize.generate_tokens(io.StringIO(texto).readline):
            if tok.type == tokenize.COMMENT:
                keep.add(tok.start[0])
        keep |= _docstring_lineas(ast.parse(texto))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return ""
    return "\n".join(ln if i + 1 in keep else "" for i, ln in enumerate(lineas))


def _literales(texto):
    """Cada literal de texto del código en su propio renglón (sin docstrings, que ya revisa _comentarios)."""
    try:
        arbol = ast.parse(texto)
    except SyntaxError:
        return ""
    doc = _docstring_lineas(arbol)
    out = []
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Constant) and isinstance(nodo.value, str) and nodo.lineno not in doc:
            out.append(nodo.value.replace("\n", " "))
    return "\n".join(out)


def archivos_md(d):
    out = []
    sk = None
    for c in (os.environ.get("TAKEOFF_SKILL"), os.path.join(d, "..", "take-off-metal-frame-drywall")):
        if c and os.path.isfile(os.path.join(c, "SKILL.md")):
            sk = c
            break
    if sk:
        for base, _, fs in os.walk(sk):
            out += [os.path.join(base, f) for f in sorted(fs) if f.endswith(".md")]
    out += [os.path.join(d, f) for f in sorted(os.listdir(d)) if f.endswith(".md")]
    raiz = os.path.join(d, "..")                     # v74: también los .md de la raíz del zip (CAMBIOS_*.md)
    if sk and os.path.abspath(os.path.join(sk, "..")) == os.path.abspath(raiz):
        out += [os.path.join(raiz, f) for f in sorted(os.listdir(raiz)) if f.endswith(".md")]
    return out


def archivos(argv):
    if argv:
        return argv
    d = os.path.dirname(os.path.abspath(__file__))
    return [os.path.join(d, f) for f in sorted(os.listdir(d)) if f.endswith(".py")]


def main(argv):
    print(autoprueba())
    a = list(argv[1:])
    if "--estricto" in a:
        ESTRICTO[0] = True
        a.remove("--estricto")
    if "--valores" in a:
        i = a.index("--valores")
        valores(a[i + 1])
        del a[i:i + 2]
    else:
        valores()
    fs = archivos(a)
    hall = []
    for f in fs:
        with open(f, encoding="utf-8") as fh:
            t = fh.read()
        b = os.path.basename(f)
        # los patrones de texto de los tests de ciego son sus casos malos a propósito
        if b not in ("test_ciego.py", "test_ciego_v69.py", "test_ciego_tools.py"):
            hall += revisar_fuente(t, b)
            if not b.startswith("test_"):              # v73c: P6–P10 en comentarios y docstrings de las tools
                hall += revisar_md(_comentarios(t), b)
                if ESTRICTO[0]:                           # v73d: y en los textos (mensajes, nombres) del código
                    hall += revisar_md(_literales(t), b + "(textos)")
        hall += revisar_literales(t, b, _VALORES) if b != "test_ciego_tools.py" else []
    if not a:                                        # v73b: también SKILL.md, referencias/*.md y los .md de tools
        for f in archivos_md(os.path.dirname(os.path.abspath(__file__))):
            hall += revisar_md(open(f, encoding="utf-8").read(), os.path.relpath(f))
    for h in hall:
        print(h)
    print(f"test_ciego_tools: {len(fs)} archivo(s) (tests y fixtures incluidos), P8 con "
          f"{len(_VALORES) if _VALORES else 0} valores externos, {len(hall)} hallazgo(s) -> " + ("OK" if not hall else "FALLA"))
    return 0 if not hall else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
