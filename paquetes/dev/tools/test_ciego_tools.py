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
    return "autoprueba OK (4/4 líneas malas detectadas, 0 falsos positivos en una fuente genérica)"


def archivos(argv):
    if argv:
        return argv
    d = os.path.dirname(os.path.abspath(__file__))
    return [os.path.join(d, f) for f in sorted(os.listdir(d))
            if f.endswith(".py") and not f.startswith("test_")]


def main(argv):
    print(autoprueba())
    fs = archivos(argv[1:])
    hall = []
    for f in fs:
        with open(f, encoding="utf-8") as fh:
            hall += revisar_fuente(fh.read(), os.path.basename(f))
    for h in hall:
        print(h)
    print(f"test_ciego_tools: {len(fs)} archivo(s), {len(hall)} hallazgo(s) -> " + ("OK" if not hall else "FALLA"))
    return 0 if not hall else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
