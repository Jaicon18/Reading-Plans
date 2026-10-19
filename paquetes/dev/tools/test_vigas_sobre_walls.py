#!/usr/bin/env python3
"""Tests de vigas_sobre_walls.py v66 (E26). Datos SINTÉTICOS. Correr: python3 test_vigas_sobre_walls.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vigas_sobre_walls as V  # noqa: E402


def test_registro_por_grids_alineados():
    """Las burbujas de grid fijan el mapa A -> S; un '1' suelto de un título no es grid."""
    a = [("1", 100, 900), ("2", 300, 900), ("3", 500, 900), ("1", 700, 40),        # '1' suelto (título)
         ("A", 50, 800), ("B", 50, 600), ("C", 50, 400)]
    s = [("1", 150, 950), ("2", 350, 950), ("3", 550, 950), ("A", 90, 790), ("B", 90, 590), ("C", 90, 390)]
    ga, gs = V.burbujas(a), V.burbujas(s)
    assert ga["1"] == (100, 900) and len(ga) == 6, ga
    sx, dx, sy, dy = V.registrar(ga, gs)
    assert abs(sx - 1) < 1e-6 and abs(dx - 50) < 1e-6 and abs(sy - 1) < 1e-6 and abs(dy + 10) < 1e-6
    try:
        V.registrar({"1": (0, 0)}, {"1": (5, 5)})
    except ValueError as e:
        assert "grid" in str(e)
    else:
        raise AssertionError("un solo grid por eje debía fallar")


def test_wall_bajo_viga_y_paralelo_fuera():
    vigas = [{"p0": (200.0, 500.0), "p1": (200.0, 700.0), "lw": 2.16},      # viga V en x = 200
             {"p0": (100.0, 300.0), "p1": (400.0, 300.0), "lw": 2.16}]      # viga H en y = 300
    walls = [{"id": "W1", "tag": "A1", "band": {"ori": "V", "c0": 196.0, "c1": 203.0, "lo": 520.0, "hi": 700.0}},
             {"id": "W2", "tag": "A1", "band": {"ori": "V", "c0": 230.0, "c1": 237.0, "lo": 520.0, "hi": 700.0}},
             {"id": "W3", "tag": "B", "band": {"ori": "H", "c0": 296.0, "c1": 305.0, "lo": 380.0, "hi": 470.0}},
             {"id": "W4", "tag": "B", "band": {"ori": "H", "c0": 296.0, "c1": 305.0, "lo": 405.0, "hi": 470.0}}]
    r = {x["wall"]: x for x in V.cruzar(vigas, walls)}
    assert set(r) == {"W1", "W3"}, r                 # W2 paralelo pero fuera de la band; W4 sin solape
    assert r["W1"]["covered_ft"] == 10.0 and r["W1"]["pct"] == 100.0
    assert abs(r["W3"]["covered_ft"] - 20 / 18) < 0.001


def test_mapa_a_planta():
    assert V.a_planta(((150.0, 940.0), (350.0, 940.0)), (1.0, 50.0, 1.0, -10.0)) == ((100.0, 950.0), (300.0, 950.0))


if __name__ == "__main__":
    n = 0
    for k, f in list(globals().items()):
        if k.startswith("test_") and callable(f):
            f()
            n += 1
            print("OK", k)
    print(f"{n} tests OK")
