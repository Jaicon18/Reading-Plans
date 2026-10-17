#!/usr/bin/env python3
"""test_ciego_v69.py — E24: el SKILL (y referencias/) no deben traer valores de ningún proyecto.

Chequeo GENÉRICO por patrones (no usa ninguna lista de examen; no lee resultados de pruebas):
  P1  nombre de un proyecto de prueba / examen conocido o ruta de trabajo de un proyecto;
  P2  cantidad con unidad de take-off (LF, SF, PCS, walls, tags, studs, sticks, sheets, ft con decimales);
  P3  número con separador de miles (14,302 · 1,354) — los criterios generales no los usan;
  P4  resultado / calificación de una prueba (NN.N %, "% de materials", "rangos_vN" con números);
  P5  coordenada de un PDF (x=1234.5) o medida en ft con 3 decimales.
Una línea se permite si lleva el marcador `[ciego-ok]` (criterio general que necesita el número, p. ej. una
conversión de unidad de compra) — cada marcador se revisa a mano.

Uso:  python3 test_ciego_v69.py [SKILL.md | carpeta_del_skill] ...   (sin argumentos: prueba sintética propia)
rc 0 = OK; rc 1 = hallazgos (se listan archivo:línea: patrón: texto).
"""
import os
import re
import sys

PATRONES = [
    ("P1 proyecto", re.compile(r"\bBOA\b|Broomfield|Greeley|\bBofA\b|Bank of America|/home/claude/\w+", re.I)),
    ("P2 cantidad", re.compile(r"(?<![\w/'\"-])\d[\d,]*(\.\d+)?\s?(LF|SF|PCS|walls?|tags?|studs|sticks|sheets|anotaciones)\b"
                               r"|\b\d+\.\d+\s?ft\b")),
    ("P3 miles", re.compile(r"(?<![\w.])\d{1,3},\d{3}\b")),
    ("P4 resultado", re.compile(r"\b\d{1,3}\.\d\s?%|%\s*de materials|rangos_v\d[^\n]*\d", re.I)),
    ("P5 coordenada", re.compile(r"\b[xy]\s?=\s?\d{3,}(\.\d+)?|\b\d+\.\d{3}\b")),
]
OK = "[ciego-ok]"


def revisar_texto(texto, nombre="<texto>"):
    out = []
    for n, linea in enumerate(texto.splitlines(), 1):
        if OK in linea:
            continue
        for et, rx in PATRONES:
            m = rx.search(linea)
            if m:
                out.append(f"{nombre}:{n}: {et}: …{linea[max(0, m.start() - 40):m.end() + 40].strip()}…")
    return out


def archivos(rutas):
    for r in rutas:
        if os.path.isdir(r):
            for base, _, fs in os.walk(r):
                for f in sorted(fs):
                    if f.endswith(".md"):
                        yield os.path.join(base, f)
        else:
            yield r


def autoprueba():
    malo = ("Caso real (BOA): 123 LF de blocking.\nPrueba #1: 11.1 % de materials.\n5/8\" board 1,234 vs 5,678\n"
            "length (12.345 ft) en x=1000.5\nrangos_v1: 6\" stud 9,876.54\n")   # cifras SINTÉTICAS
    bueno = ("Header: R.O. + 1'-4\" (8\" de bearing por lado). Waste 15 % en metal. Bracing rows = ROUNDUP(H × 12 / 48)"
             " − 1. Barrido P/M REGISTRADO (≥ 25 coincidencias). Cita N/HOJA (6/A12.01, D/A9.22).\n"
             "\"4x8 sheet\" = 32 SF [ciego-ok]\nUna layer de 5/8\" mide 11.28 pt a 3\"=1'-0\".\n")
    hm, hb = revisar_texto(malo, "malo"), revisar_texto(bueno, "bueno")
    lineas_malas = {h.split(":")[1] for h in hm}
    assert lineas_malas == {"1", "2", "3", "4", "5"}, hm
    assert hb == [], hb
    return "autoprueba OK (5/5 líneas malas detectadas, 0 falsos positivos en criterios generales)"


def main(argv):
    print(autoprueba())
    if len(argv) == 1:
        return 0
    hall = []
    fs = list(archivos(argv[1:]))
    for f in fs:
        with open(f, encoding="utf-8") as fh:
            hall += revisar_texto(fh.read(), f)
    for h in hall:
        print(h)
    print(f"test_ciego_v69: {len(fs)} archivo(s), {len(hall)} hallazgo(s) -> " + ("OK" if not hall else "FALLA"))
    return 0 if not hall else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
