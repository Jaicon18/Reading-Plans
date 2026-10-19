#!/usr/bin/env python3
"""Tests de particion.py con un canon SINTÉTICO (ningún dato de proyecto). Correr: python3 test_particion.py"""
import copy
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import particion as P  # noqa: E402

E = 18.0   # pt por ft


def w(id_, tag, ori, eje, lo, hi, sheet="Z1.01", esp=4.0):
    return {"id": id_, "tag": tag, "length_ft": round((hi - lo) / E, 4), "sheet": sheet,
            "band": {"ori": ori, "c0": eje - esp / 2, "c1": eje + esp / 2, "lo": lo, "hi": hi}}


def canon():
    return {"constants": {"plan_scale_pt_per_ft": {"value": E, "source": "sintético"}}, "walls": [
        w("S1", "X1", "H", 100, 0, 180),           # 10 ft
        w("S2", "X1", "H", 100, 182, 360),         # colineal y contiguo a S1 (hueco 2 pt)
        w("S3", "X1", "V", 360, 100, 280),         # esquina L al final de S2
        w("S4", "X1", "V", 90, 102, 280),          # T contra el costado de S1
        w("S5", "X1", "V", 0, 100, 114.4),         # jog 0.8 ft en el extremo de S1  [ciego-ok]
        w("S6", "X1", "H", 100, 0, 180, sheet="Z1.02"),   # misma geometría, otra hoja
        {"id": "S7", "tag": "X1", "length_ft": 4.0, "sheet": "Z1.01"},   # sin band
        w("S8", "X2", "H", 100, 362, 400),         # otro type colineal: no se une
        {"id": "F1", "tag": "X1", "element": "soffit_side", "length_ft": 9.0, "sheet": "Z1.01"},
    ]}


def _walls(r, t, sheet):
    return sorted(tuple(sorted(f["ids"])) for f in r["types"][t]["filas"] if f["sheet"] == sheet)


def test_default_es_una_constante():
    assert P.MODO_DEFAULT in P.MODOS
    assert P.particion(canon())["modo"] == P.MODO_DEFAULT


def test_modo_tramo():
    r = P.particion(canon(), "tramo")
    assert _walls(r, "X1", "Z1.01") == sorted([("S1", "S2", "S5"), ("S3",), ("S4",), ("S7",)]), _walls(r, "X1", "Z1.01")
    f = [x for x in r["types"]["X1"]["filas"] if "S1" in x["ids"]][0]
    assert abs(f["lf"] - (10 + 178 / E + 14.4 / E)) < 0.01, f["lf"]
    assert f["jogs"] == [{"ids": ["S5"], "lf": 0.8}]


def test_modo_run():
    r = P.particion(canon(), "run")
    assert _walls(r, "X1", "Z1.01") == sorted([("S1", "S2", "S3", "S5"), ("S4",), ("S7",)]), _walls(r, "X1", "Z1.01")
    f = [x for x in r["types"]["X1"]["filas"] if "S3" in x["ids"]][0]
    assert f["tramos"] == 3, f


def test_nunca_une_entre_hojas_ni_types():
    for modo in P.MODOS:
        r = P.particion(canon(), modo)
        assert _walls(r, "X1", "Z1.02") == [("S6",)]
        assert _walls(r, "X2", "Z1.01") == [("S8",)]
        assert "F1" in r["other_framing"]
        assert any("S7" in a and "sin band" in a for a in r["avisos"])


def test_t_no_encadena_en_run():
    """La T (S4 contra el costado de S1) no es un quiebre del run."""
    c = canon()
    r = P.particion(c, "run")
    assert ("S4",) in _walls(r, "X1", "Z1.01")
    c2 = copy.deepcopy(c)                               # dato malo: si S4 arranca en el extremo de S1, sí encadena
    c2["walls"][3] = w("S4", "X1", "V", 180, 102, 280)
    c2["walls"] = [x for x in c2["walls"] if x["id"] != "S2"]
    r2 = P.particion(c2, "run")
    assert any("S4" in g and "S1" in g for g in _walls(r2, "X1", "Z1.01")), _walls(r2, "X1", "Z1.01")


def test_modo_invalido():
    try:
        P.particion(canon(), "zona")
    except ValueError:
        return
    raise AssertionError("modo inválido aceptado")


def test_hoja_desde_source():
    c = {"walls": [{"id": "A", "tag": "X1", "length_ft": 3, "source": "3/Z9.01; Z1.01 vector"}]}
    r = P.particion(c, "tramo")
    assert r["types"]["X1"]["filas"][0]["sheet"] == "Z9.01"


if __name__ == "__main__":
    fallas = 0
    for k, f in sorted(globals().items()):
        if k.startswith("test_") and callable(f):
            try:
                f()
                print("OK  ", k)
            except AssertionError as e:
                fallas += 1
                print("FALLA", k, e)
    print(f"{'TODOS OK' if not fallas else str(fallas) + ' FALLA(S)'}")
    sys.exit(1 if fallas else 0)
