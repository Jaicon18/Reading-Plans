#!/usr/bin/env python3
"""test_esquinas.py — tests sintéticos de esquinas.py (R70.2 / R70.3). Sin datos de ningún proyecto."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import esquinas as E  # noqa: E402

ESC = {"plan_scale_pt_per_ft": {"value": 18}}


def W(i, ori, c0, c1, lo, hi, tag="X", element="wall"):
    return {"id": i, "tag": tag, "element": element, "length_ft": abs(hi - lo) / 18.0,
            "band": {"sheet": "S1", "ori": ori, "c0": c0, "c1": c1, "lo": lo, "hi": hi}}


def canon(*ws, gaps_ok=None):
    c = {"constants": ESC, "walls": list(ws)}
    if gaps_ok:
        c["gaps_ok"] = gaps_ok
    return c


def test_L_un_dueno_ok():
    # H de x 100 a 300 (llega a la cara exterior del V), V de y 107 (cara sur del H) a 400
    r = E.revisar(canon(W("h", "H", 100, 107, 100, 300), W("v", "V", 293, 300, 107, 400)))
    assert not r["fallas"], r["fallas"]
    assert r["esquinas"][0]["dueno"] == "h"


def test_L_sin_dueno_falla():
    # H termina en la cara interior del V (293) y V empieza en la cara sur del H (107): cuadrado sin dueño
    r = E.revisar(canon(W("h", "H", 100, 107, 100, 293), W("v", "V", 293, 300, 107, 400)))
    assert any("sin dueño" in x for x in r["fallas"]), r


def test_corners_ok_con_motivo_explica_y_sin_motivo_no():
    h, v = W("h", "H", 100, 107, 100, 293), W("v", "V", 293, 300, 107, 400)
    assert not E.revisar(canon(h, v, gaps_ok=None) | {"corners_ok": [{"walls": ["h", "v"], "reason": "x"}]})["fallas"]
    assert E.revisar(canon(h, v) | {"corners_ok": [{"walls": ["h", "v"]}]})["fallas"]


def test_L_doble_falla():
    r = E.revisar(canon(W("h", "H", 100, 107, 100, 300), W("v", "V", 293, 300, 100, 400)))
    assert any("doble" in x for x in r["fallas"]), r


def test_T_ok():
    # V pasa de largo; H llega a su cara
    r = E.revisar(canon(W("v", "V", 293, 300, 0, 400), W("h", "H", 100, 107, 100, 293)))
    assert not r["fallas"], r["fallas"]


def test_cruce_no_es_esquina():
    r = E.revisar(canon(W("v", "V", 200, 207, 0, 400), W("h", "H", 100, 107, 0, 400)))
    assert not r["esquinas"] and not r["fallas"]


def test_hueco_colineal_de_door_falla_y_gaps_ok_lo_explica():
    a = W("a", "H", 100, 107, 0, 100)
    b = W("b", "H", 100, 107, 160, 300, tag="Y")     # hueco 60 pt = 3.333 ft (una door)  [ciego-ok]
    r = E.revisar(canon(a, b))
    assert any("hueco colineal 3.333" in x for x in r["fallas"]), r
    r2 = E.revisar(canon(a, b, gaps_ok=[{"between": ["a", "b"], "reason": "corridor opening without frame"}]))
    assert not r2["fallas"], r2


def test_hueco_cubierto_por_bulkhead_no_falla():
    a = W("a", "V", 100, 112, 0, 100)
    bh = W("bh", "V", 100, 112, 100, 235, element="door_bulkhead")
    b = W("b", "V", 100, 112, 235, 300)
    assert not E.revisar(canon(a, bh, b))["fallas"]


def test_hueco_cortado_por_wall_perpendicular_no_falla():
    a = W("a", "H", 100, 107, 0, 100)
    x = W("x", "V", 140, 147, 50, 200)          # cruza la línea dentro del hueco
    b = W("b", "H", 100, 107, 180, 300)
    r = E.revisar(canon(a, x, b))
    assert not any("hueco" in f for f in r["fallas"]), r["fallas"]


def test_otra_hoja_no_se_compara():
    a = W("a", "H", 100, 107, 100, 293)
    b = W("b", "V", 293, 300, 107, 400)
    b["band"]["sheet"] = "S2"
    assert not E.revisar(canon(a, b))["fallas"]


def test_no_partition_se_ignora():
    r = E.revisar(canon(W("h", "H", 100, 107, 100, 293),
                        W("v", "V", 293, 300, 107, 400, element="ceiling_transition")))
    assert not r["fallas"]


if __name__ == "__main__":
    n = 0
    for k, f in list(globals().items()):
        if k.startswith("test_"):
            f()
            print("OK  ", k)
            n += 1
    print(f"TODOS OK ({n})")
