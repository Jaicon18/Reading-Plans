#!/usr/bin/env python3
"""Tests de altura_stud.py (reglas 60.3, 59.13). Datos genéricos. Correr: python3 test_altura_stud.py"""
import json
import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import altura_stud as A  # noqa: E402


def v(x, s):
    return {"value": x, "source": s}


def caso():
    return {
        "bod_table": {"source": "S2.20", "points": [{"y_ft": 0.0, "bod_ft": 15.0}, {"y_ft": 40.0, "bod_ft": 13.0}]},
        "beams": {"W12x26": {"d_in": v(12.0, "AISC W12X26")}},
        "walls": [
            {"id": "E1", "type": "exterior", "y_ft": v(0.0, "A02.01"),
             "stops_under_beam": v(True, "10/S5.10"), "beam": "W12x26"},
            {"id": "E2", "type": "exterior", "y_ft": v(0.0, "A02.01"), "y_to_ft": v(40.0, "A02.01"),
             "stops_under_beam": v(True, "10/S5.10"), "beam": "W12x26"},
            {"id": "E3", "type": "exterior", "bod_ft": v(14.0, "3/S2.20"), "stops_under_beam": v(False, "2/S5.10")},
            {"id": "I1", "type": "interior", "y_ft": v(20.0, "A02.01")},
        ]}


def test_exterior_bajo_viga():
    r = {x["id"]: x for x in A.calcular(caso())["renglones"]}
    assert r["E1"]["height_ft"] == 14.0                   # 15.0 - 12/12
    assert "10/S5.10" in r["E1"]["source"] and "AISC W12X26" in r["E1"]["source"]


def test_pendiente_lado_alto_y_promedio():
    r = {x["id"]: x for x in A.calcular(caso())["renglones"]}
    assert r["E2"]["height_ft"] == 14.0 and r["E2"]["height_avg_ft"] == 13.0


def test_interior_a_bod_interpolado():
    r = {x["id"]: x for x in A.calcular(caso())["renglones"]}
    assert r["I1"]["height_ft"] == 14.0                   # interp a y=20 -> 14.0, sin viga
    assert r["E3"]["height_ft"] == 14.0                   # bod directo, detalle no para bajo viga


def test_borde_extremo_de_tabla():
    d = caso()
    d["walls"] = [{"id": "I", "type": "interior", "y_ft": v(40.0, "A02.01")}]
    assert A.calcular(d)["renglones"][0]["height_ft"] == 13.0


def _falla(d, txt):
    try:
        A.calcular(d)
    except ValueError as e:
        assert txt in str(e), str(e)
        return
    raise AssertionError("debía fallar: " + txt)


def test_dato_malo_exterior_sin_declarar_viga():      # el error de una corrida del arbitraje #10
    d = caso()
    del d["walls"][0]["stops_under_beam"]
    _falla(d, "60.3")


def test_dato_malo_numero_sin_fuente():
    d = caso()
    d["walls"][0]["y_ft"] = 0.0
    _falla(d, "número sin fuente")
    d = caso()
    d["beams"]["W12x26"]["d_in"] = {"value": 12.0}
    _falla(d, "falta 'source'")


def test_dato_malo_extrapolar():
    d = caso()
    d["walls"][3]["y_ft"] = v(41.0, "A02.01")
    _falla(d, "no se extrapola")


def test_dato_malo_viga_no_declarada():
    d = caso()
    d["walls"][0]["beam"] = "W14x30"
    _falla(d, "no declarada")


def test_dato_malo_tabla_y_altura():
    d = caso()
    d["bod_table"]["points"] = [{"y_ft": 0.0, "bod_ft": 15.0}]
    _falla(d, ">= 2 puntos")
    d = caso()
    d["beams"]["W12x26"]["d_in"] = v(200.0, "AISC")
    _falla(d, "altura <= 0")


def test_dato_malo_booleano():
    d = caso()
    d["walls"][0]["stops_under_beam"] = v(1, "10/S5.10")
    _falla(d, "true/false")


def test_cli_rc():
    with tempfile.TemporaryDirectory() as t:
        bueno, malo, sal = (os.path.join(t, x) for x in ("b.json", "m.json", "s.json"))
        json.dump(caso(), open(bueno, "w"))
        d = caso()
        del d["walls"][0]["stops_under_beam"]
        json.dump(d, open(malo, "w"))
        p = subprocess.run([sys.executable, os.path.join(AQUI, "altura_stud.py"), bueno, sal], capture_output=True)
        assert p.returncode == 0 and json.load(open(sal))["resumen_por_tipo"]["exterior"]["walls"] == 3
        p = subprocess.run([sys.executable, os.path.join(AQUI, "altura_stud.py"), malo, sal], capture_output=True,
                           text=True)
        assert p.returncode != 0 and "ERROR altura_stud.py" in p.stderr, p.stderr


if __name__ == "__main__":
    n = 0
    for k, f in list(globals().items()):
        if k.startswith("test_") and callable(f):
            f()
            n += 1
            print("OK", k)
    print(f"{n} tests OK")
