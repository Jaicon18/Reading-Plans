#!/usr/bin/env python3
"""Tests de board_caras.py con datos sintéticos (E24). Correr: python3 test_board_caras.py"""
import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import board_caras as B  # noqa: E402

DET = {"5/A12.01": {"layers_per_face": 2},
       "4/A12.01": {"layers_per_face": 1, "k_panel": {"panel_to_ft": 8.0}}}


def caso():
    return {"details": copy.deepcopy(DET), "walls": [
        {"id": "W45", "tag": "G", "detail": "5/A12.01", "length_printed_ft": 11.5,
         "faces": [{"room": "Office 906", "board": "5/8 regular", "layers": 2, "height_ft": 15.25},
                   {"room": "Office 907", "board": "5/8 regular", "layers": 2, "height_ft": 15.25}]},
        {"id": "W11", "tag": "A1K", "detail": "4/A12.01", "length_vector_ft": 2.57, "length_printed_ft": 3.5,
         "faces": [{"room": "Teller", "board": "5/8 regular", "layers": 1, "height_ft": 15.25},
                   {"room": "Customer", "board": "5/8 regular", "layers": 1, "height_ft": 15.25,
                    "k_customer": True}]},
        {"id": "W26", "tag": "B2K", "detail": "4/A12.01", "length_vector_ft": 1.25,
         "faces": [{"room": "Office 908", "board": "5/8 regular", "layers": 1, "height_ft": 15.25},
                   {"room": "Waiting 904", "board": "5/8 regular", "layers": 1, "height_ft": 15.25,
                    "k_customer": True}]},
    ]}


def test_g_cuatro_layers():
    out = B.calcular(caso())
    g = [c for c in out["caras"] if c["wall"] == "W45"]
    assert abs(sum(c["sf"] for c in g) - 4 * 11.5 * 15.25) < 0.05     # 2 layers por face x 2 faces


def test_k_impresa_manda():
    out = B.calcular(caso())
    assert abs(out["totales_sf"]["ballistic panel"] - (3.5 + 1.25) * 8.0) < 0.01
    assert abs(out["totales_sf"]["3/8 gyp"] - (3.5 + 1.25) * 7.25) < 0.01
    assert any("DISCREPANCIA" in a for a in out["avisos"])


def _falla(d, txt):
    try:
        B.calcular(d)
    except ValueError as e:
        assert txt in str(e), str(e)
        return
    raise AssertionError("debía fallar: " + txt)


def test_dato_malo_g_una_layer_por_face():          # el error de la corrida A
    d = caso()
    for f in d["walls"][0]["faces"]:
        f["layers"] = 1
    _falla(d, "dibuja 2")


def test_dato_malo_layers_total():
    d = caso()
    d["walls"][0]["layers"] = 2
    _falla(d, "prohibido")


def test_dato_malo_k_sin_panel():
    d = caso()
    d["walls"][0]["faces"][0]["k_customer"] = True
    _falla(d, "sin k_panel")


def test_dato_malo_detalle_no_declarado():
    d = caso()
    d["walls"][1]["detail"] = "9/A12.01"
    _falla(d, "no declarado")


def test_v66_face_en_dos_rooms():
    """#15A CC-E1: una face que da a dos rooms con ceilings distintos se cargó con altura ponderada a mano.
    v66: tramos con side + length_ft + length_source; Σ tramos del side = largo del wall."""
    d = {"details": copy.deepcopy(DET), "walls": [
        {"id": "X", "tag": "A1", "detail": "5/A12.01", "length_printed_ft": 10.0,
         "faces": [{"room": "R1", "board": "5/8 regular", "layers": 2, "height_ft": 9.5, "side": "A",
                    "length_ft": 6.0, "length_source": "A02.01"},
                   {"room": "R2", "board": "5/8 regular", "layers": 2, "height_ft": 12.0, "side": "A",
                    "length_ft": 4.0, "length_source": "A02.01"},
                   {"room": "R3", "board": "5/8 regular", "layers": 2, "height_ft": 9.5, "side": "B"}]}]}
    out = B.calcular(copy.deepcopy(d))
    assert abs(out["totales_sf"]["5/8 regular"] - (6 * 9.5 * 2 + 4 * 12.0 * 2 + 10 * 9.5 * 2)) < 0.01
    d["walls"][0]["faces"][1]["length_ft"] = 3.0
    _falla(copy.deepcopy(d), "Σ tramos")
    d["walls"][0]["faces"][1]["length_ft"] = 4.0
    del d["walls"][0]["faces"][0]["length_source"]
    _falla(d, "length_source")


if __name__ == "__main__":
    n = 0
    for k, f in list(globals().items()):
        if k.startswith("test_") and callable(f):
            f()
            n += 1
            print("OK", k)
    print(f"{n} tests OK")
