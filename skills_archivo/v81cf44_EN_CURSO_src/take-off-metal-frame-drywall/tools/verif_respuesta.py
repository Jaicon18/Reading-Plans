#!/usr/bin/env python3
"""verif_respuesta.py — v73 (adenda v40): compuerta de la RESPUESTA final antes de mandarla.

Procedimiento (la regla, no una sugerencia): 1) la respuesta se escribe a un archivo; 2) se corre
`python3 verif_respuesta.py <archivo>`; 3) si marca algo se corrige en el archivo y se vuelve a correr; 4) solo
cuando pasa limpia se manda. Revisa: términos del trade en español (glosario.faltas: el dato; vocab_trade.faltas: la
prosa), fuera de bloques de código (la normalización vive en vocab_trade.sin_codigo). El texto general puede ir en
español; los términos del trade, no.
Uso: python3 verif_respuesta.py <archivo.md>   rc 0 = limpia; rc 1 = marcas (renglón: término -> inglés)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glosario as G  # noqa: E402
import vocab_trade as V  # noqa: E402


def revisar(texto):
    marcas = []
    for n, ln in V.lineas_sin_codigo(texto):
        for t in G.faltas(ln):
            marcas.append((n, t, G.traducir(t)))
        for t, en in V.faltas(ln):
            marcas.append((n, t, en))
    return marcas


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    m = revisar(open(argv[1], encoding="utf-8").read())
    for n, t, en in m:
        print(f"renglón {n}: '{t}' -> {en}")
    print("RESPUESTA LIMPIA" if not m else f"{len(m)} término(s) del trade en español: corregir y volver a correr")
    return 1 if m else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
