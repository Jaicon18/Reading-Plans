#!/usr/bin/env python3
"""Tests de alcance_filtro.py (regla 60.4). Datos genéricos. Correr: python3 test_alcance_filtro.py"""
import json
import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import alcance_filtro as A  # noqa: E402


def caso():
    return {"rows": [
        {"id": "M1", "family": "furring channel", "description": "7/8\" furring channel @ 16\" O.C. at GB ceiling",
         "qty": 700.0, "unit": "LF", "source": "2/A09.10"},
        {"id": "M2", "family": "furring channel", "description": "7/8\" hat channel @ 16\" O.C. at EPS-5 metal panel",
         "qty": 750.0, "unit": "LF", "source": "2/A09.31"},
        {"id": "M3", "family": "other", "description": "Z-girt 1-1/2\" @ 24\" O.C.", "qty": 120.0, "unit": "LF",
         "source": "5/A09.31"},
        {"id": "M4", "family": "other", "description": "Metal lath, 3.4 lb", "qty": 900.0, "unit": "SF",
         "source": "1/A09.40"},
        {"id": "M5", "family": "furring channel", "description": "Hat channel at GB soffit",
         "qty": 50.0, "unit": "LF", "source": "6/A12.10", "substrate_of": "drywall", "substrate_source": "6/A12.10"},
        {"id": "M6", "family": "bracing C.R. channel", "description": "1-1/2\" C.R. channel @ 48\" O.C.",
         "qty": 300.0, "unit": "LF", "source": "F/1/S5.20"},
        {"id": "M7", "family": "furring channel", "description": "Furring at ACM soffit", "qty": 40.0, "unit": "LF",
         "source": "3/A09.32"},
    ]}


def test_clasificacion():
    out = A.calcular(caso())
    est = {r["id"]: r["estado"] for r in out["renglones"]}
    assert est == {"M1": "INCLUDED", "M2": "EXCLUDED", "M3": "EXCLUDED", "M4": "EXCLUDED", "M5": "INCLUDED",
                   "M6": "INCLUDED", "M7": "EXCLUDED"}, est
    assert out["totales_incluidos"]["furring channel [LF]"] == 750.0          # 700 + 50, nunca el EPS
    assert sum(r["delta"] for r in out["rfis"] if r["unit"] == "LF") == 910.0


def test_borde_steps_no_es_eps():
    d = {"rows": [{"id": "X", "family": "other", "description": "framing at stair steps channel", "qty": 1,
                   "unit": "LF", "source": "A05.01"}]}
    assert A.calcular(d)["renglones"][0]["estado"] == "INCLUDED"


def test_borde_declarado_cladding_sin_palabras():
    d = {"rows": [{"id": "Y", "family": "furring channel", "description": "7/8\" channel", "qty": 10, "unit": "LF",
                   "source": "A09.31", "substrate_of": "cladding", "substrate_source": "2/A09.31"}]}
    assert A.calcular(d)["renglones"][0]["estado"] == "EXCLUDED"


def _falla(d, txt):
    try:
        A.calcular(d)
    except ValueError as e:
        assert txt in str(e), str(e)
        return
    raise AssertionError("debía fallar: " + txt)


def test_dato_malo_hat_channel_ambiguo():
    d = caso()
    d["rows"][1]["description"] = "7/8\" hat channel @ 16\" O.C."
    _falla(d, "ambiguo")


def test_dato_malo_zgirt_declarado_drywall():
    d = caso()
    d["rows"][2].update(substrate_of="drywall", substrate_source="5/A09.31")
    _falla(d, "contradice")


def test_dato_malo_declaracion_sin_fuente():
    d = caso()
    d["rows"][4].pop("substrate_source")
    _falla(d, "substrate_of")


def test_dato_malo_qty_y_campos():
    d = caso()
    d["rows"][0]["qty"] = -1
    _falla(d, "negativa")
    d = caso()
    del d["rows"][0]["unit"]
    _falla(d, "unit")
    d = caso()
    d["rows"][1]["id"] = "M1"
    _falla(d, "repetido")


def test_cli_rc():
    with tempfile.TemporaryDirectory() as t:
        bueno, malo, sal = (os.path.join(t, x) for x in ("b.json", "m.json", "s.json"))
        json.dump(caso(), open(bueno, "w"))
        d = caso()
        d["rows"][1]["description"] = "hat channel"
        json.dump(d, open(malo, "w"))
        p = subprocess.run([sys.executable, os.path.join(AQUI, "alcance_filtro.py"), bueno, sal], capture_output=True)
        assert p.returncode == 0 and len(json.load(open(sal))["excluidos"]) == 4
        p = subprocess.run([sys.executable, os.path.join(AQUI, "alcance_filtro.py"), malo, sal], capture_output=True,
                           text=True)
        assert p.returncode != 0 and "ERROR alcance_filtro.py" in p.stderr, p.stderr


if __name__ == "__main__":
    n = 0
    for k, f in list(globals().items()):
        if k.startswith("test_") and callable(f):
            f()
            n += 1
            print("OK", k)
    print(f"{n} tests OK")
