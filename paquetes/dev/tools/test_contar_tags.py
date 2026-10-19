#!/usr/bin/env python3
"""Tests de contar_tags.py (v66). Datos sintéticos (E24); el caso real vive en tests_arbitraje/.
Correr: python3 test_contar_tags.py"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import contar_tags as C  # noqa: E402


def W(x, y, t):
    return (x, y, x + 10, y + 5, t, 0, 0, 0)


def test_coincidencia_exacta():
    """UU3 no cuenta 'UU30' ni 'UU3A'; cada ocurrencia exacta suma 1 con su punto."""
    ws = [W(0, 0, "UU3"), W(20, 0, "UU3"), W(40, 0, "UU30"), W(60, 0, "UU3A"), W(80, 0, "UU2"), W(5, 9, " UU3 ")]
    r = C.contar_en_palabras(ws, ["UU3", "UU2", "R-11B"])
    assert r["UU3"]["count"] == 3 and r["UU2"]["count"] == 1 and r["R-11B"]["count"] == 0, r
    assert r["UU3"]["pts"][0] == [5.0, 2.5]


def test_v66_sufijo_de_circuito():
    """#15A/#15B: E02.01 rotula 'R-11C,d' / 'R-11A,b'; la coincidencia exacta daba 0. Normaliza el sufijo ',x' sin
    mezclar tags distintos (R-11CE no es R-11C)."""
    ws = [W(0, 0, "R-11C,d"), W(20, 0, "R-11C"), W(40, 0, "R-11C,"), W(60, 0, "R-11CE,a"), W(80, 0, "R-11A,b"),
          W(100, 0, "R-11C,dd,e")]
    r = C.contar_en_palabras(ws, ["R-11C", "R-11CE", "R-11A"])
    assert r["R-11C"]["count"] == 3 and r["R-11C"]["count_exacto"] == 1, r["R-11C"]
    assert r["R-11C"]["variantes"] == {"R-11C,d": 1, "R-11C": 1, "R-11C,": 1}, r["R-11C"]
    assert r["R-11CE"]["count"] == 1 and r["R-11A"]["count"] == 1
    assert C.normalizar(" UU3 ") == "UU3" and C.normalizar("R-14B,c") == "R-14B"


if __name__ == "__main__":
    n = 0
    for k, f in list(globals().items()):
        if k.startswith("test_") and callable(f):
            f()
            n += 1
            print("OK", k)
    print(f"{n} tests OK")
