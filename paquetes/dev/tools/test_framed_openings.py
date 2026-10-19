#!/usr/bin/env python3
"""Tests de framed_openings.py (reglas 60.9, 60.10, 58.4). Datos genéricos. Correr: python3 test_framed_openings.py"""
import json
import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import framed_openings as F  # noqa: E402


def caso():
    return {
        "modules": {"ceiling_furring_oc_in": {"value": 16, "source": "2/A09.31"}},
        "sweep": {"sheets": ["E00.01", "M01.01", "A04.01"]},
        "tag_counts": {"SLOT-1": {"count": 4, "sheet": "E02.01"}, "DL-1": {"count": 24, "sheet": "E02.01"}},
        "items": [
            {"tag": "SLOT-1", "category": "light", "location": "ceiling", "qty": 4, "width_in": 6.0, "width_source": "E00.01",
             "length_ft": {"desc": 12.0, "catalog": 20.0, "drawn": 12.0}, "source": "E00.01"},
            {"tag": "DL-1", "category": "light", "location": "ceiling", "shape": "round", "qty": 24,
             "width_in": 3.5, "width_source": "E00.01", "source": "E00.01"},
            {"tag": "SD-1", "category": "air_device", "location": "ceiling", "qty": 10, "width_in": 24.0, "width_source": "E00.01",
             "length_ft": {"catalog": 2.0}, "source": "M0.01"},
            {"tag": "RG-W", "category": "air_device", "location": "wall", "qty": 2, "width_in": 12.0, "width_source": "E00.01",
             "length_ft": {"catalog": 1.0}, "source": "M2.01"},
            {"tag": "TG-W", "category": "air_device", "location": "wall", "qty": 1, "width_in": 12.0, "width_source": "E00.01",
             "length_ft": {"catalog": 2.0}, "source": "M2.01"},
        ]}


def test_totales_y_rfi_de_schedule():
    out = F.calcular(caso())
    # SLOT 2x(12+0.5)x4 = 100 ; SD 2x(2+2)x10 = 80 ; DL cabe ; RG cabe ; TG (air device 24") no se enmarca
    assert abs(out["totales_lf"]["framed openings MEP"] - 180.0) < 0.01, out["totales_lf"]
    assert out["rfis"][0]["delta_lf"] == 64.0                       # 2 x (20-12) x 4
    assert out["to_header_sill"] == [], out["to_header_sill"]      # v64: decisión usuario #12
    assert {r["tag"]: r["estado"] for r in out["renglones"]}["TG-W"] == "NOT_FRAMED"


def test_v64_ducto_fd_wall_no_va_a_header():
    """Decisión usuario #12: 4 FD 14x14 (M01.01) y ductos de wall: ni header ni sill. Access panel grande sí."""
    d = caso()
    d["items"] += [{"tag": "FD 14x14", "category": "other", "location": "wall", "qty": 4, "width_in": 14.0, "width_source": "E00.01",
                    "length_ft": {"catalog": 14 / 12 + 0.1}, "source": "M01.01"},
                   {"tag": "AP-W", "category": "access_panel", "location": "wall", "qty": 1, "width_in": 24.0, "width_source": "E00.01",
                    "length_ft": {"desc": 2.0}, "source": "A09.01"}]
    out = F.calcular(d)
    assert [x["tag"] for x in out["to_header_sill"]] == ["AP-W"], out["to_header_sill"]


def test_borde_modulo_exacto():
    d = caso()
    d["sweep"]["no_air_devices_why"] = "caso de borde: solo el access panel"
    d["items"] = [{"tag": "AP", "category": "access_panel", "location": "ceiling", "qty": 1, "width_in": 16.0, "width_source": "E00.01",
                   "length_ft": {"desc": 16 / 12}, "source": "A09.01"}]
    assert F.calcular(d)["renglones"][0]["estado"] == "FITS_MODULE"        # 16" <= 16"
    d["items"][0]["width_in"] = 16.125
    assert F.calcular(d)["renglones"][0]["estado"] == "FRAMED"


def test_borde_wall_stud_bay_exacto():
    d = caso()
    d["items"] = [{"tag": "X", "location": "wall", "qty": 1, "width_in": 14.375, "width_source": "E00.01",
                   "length_ft": {"drawn": 14.375 / 12}, "source": "M2.01"}]
    assert F.calcular(d)["renglones"][0]["estado"] == "FITS_MODULE"


def test_override_documentado():
    d = caso()
    d["items"][0]["length_ft"]["drawn"] = 16.0
    d["items"][0]["length_override"] = {"value": 12.0, "source": "E02.01", "rfi": "confirm slot length"}
    out = F.calcular(d)
    assert out["rfis"][0]["delta_lf"] == 64.0


def _falla(d, txt):
    try:
        F.calcular(d)
    except ValueError as e:
        assert txt in str(e), str(e)
        return
    raise AssertionError("debía fallar: " + txt)


def test_dato_malo_12a_sin_barrido_m():
    """#12A: solo light fixtures (E00.01) en ceiling, sin air devices del M-plan -> 818.75 (rango 927-952)."""
    d = caso()
    d["items"] = [i for i in d["items"] if i["category"] != "air_device"]
    d["sweep"] = {"sheets": ["E00.01", "A04.01"]}
    _falla(d, "falta hoja M")
    d["sweep"] = {"sheets": ["E00.01", "M01.01"]}
    _falla(d, "ningún air_device")
    d["sweep"]["no_air_devices_why"] = "M01.01: GWB ceilings sin diffusers (solo ACT)"
    F.calcular(d)
    d2 = caso()
    del d2["sweep"]
    _falla(d2, "sweep ausente")


def test_dato_malo_conflicto_sin_dibujo():
    d = caso()
    del d["items"][0]["length_ft"]["drawn"]
    _falla(d, "el dibujo no resuelve")


def test_dato_malo_ceiling_sin_modulo():
    d = caso()
    del d["modules"]["ceiling_furring_oc_in"]
    _falla(d, "60.10")


def test_dato_malo_dibujo_no_coincide():
    d = caso()
    d["items"][2]["length_ft"]["drawn"] = 4.0
    _falla(d, "no coinciden")


def test_dato_malo_override_sin_rfi():
    d = caso()
    d["items"][0]["length_ft"]["drawn"] = 16.0
    d["items"][0]["length_override"] = {"value": 12.0, "source": "E02.01"}
    _falla(d, "sin texto de RFI")


def test_dato_malo_round_con_largo_y_repetido():
    d = caso()
    d["items"][1]["length_ft"] = {"desc": 1.0}
    _falla(d, "round no lleva")
    d = caso()
    d["items"].append(dict(d["items"][0]))
    d["tag_counts"]["SLOT-1"]["count"] = 8
    _falla(d, "repetido")


def test_dato_malo_qty_y_source():
    d = caso()
    d["items"][0]["qty"] = 0
    _falla(d, "qty")
    d = caso()
    d["items"][0]["source"] = ""
    _falla(d, "falta 'source'")


def test_cli_rc():
    with tempfile.TemporaryDirectory() as t:
        bueno, malo, sal = (os.path.join(t, x) for x in ("b.json", "m.json", "s.json"))
        json.dump(caso(), open(bueno, "w"))
        d = caso()
        del d["items"][0]["length_ft"]["drawn"]
        json.dump(d, open(malo, "w"))
        p = subprocess.run([sys.executable, os.path.join(AQUI, "framed_openings.py"), bueno, sal],
                           capture_output=True)
        assert p.returncode == 0 and json.load(open(sal))["totales_lf"]["framed openings MEP"] == 180.0
        p = subprocess.run([sys.executable, os.path.join(AQUI, "framed_openings.py"), malo, sal],
                           capture_output=True, text=True)
        assert p.returncode != 0 and "ERROR framed_openings.py" in p.stderr, p.stderr



def test_v65_qty_contra_tags_dibujados():
    """#14B: UU3 canopy norte cargado x 5; E02.01 dibuja 9 tags UU3 (contar_tags.py) -> +25.66 LF."""
    d = caso()
    d["tag_counts"]["SLOT-1"]["count"] = 9                 # el plano dibuja 9, el item dice 4
    _falla(d, "sin excluded_qty_why")
    d["items"][0]["excluded_qty_why"] = "5 en ACT (A04.01), no GWB"
    calcular_ok = __import__("framed_openings").calcular(d)
    assert calcular_ok["totales_lf"]
    d = caso()
    d["tag_counts"]["DL-1"]["count"] = 20
    _falla(d, "> 20 dibujados")
    d = caso()
    del d["tag_counts"]
    _falla(d, "tag_counts ausente")

def test_v66_width_source_obligatorio():
    """#15A: ancho del fixture sacado del código de catálogo sin citarlo. v66: width_source N/HOJA por item."""
    d = {"modules": {"ceiling_furring_oc_in": {"value": 16, "source": "2/A09.31"}},
         "sweep": {"sheets": ["M01.01", "E02.01"], "no_air_devices_why": "sin air devices en GWB"},
         "tag_counts": {"UX": {"count": 2, "sheet": "E02.01"}},
         "items": [{"tag": "UX", "category": "light", "location": "ceiling", "qty": 2, "width_in": 6.0,
                    "length_ft": {"desc": 4.0, "drawn": 4.0}, "source": "E00.01"}]}
    try:
        F.calcular(d)
    except ValueError as e:
        assert "width_source" in str(e), str(e)
    else:
        raise AssertionError("sin width_source debía fallar")
    d["items"][0]["width_source"] = "E00.01 catálogo"
    assert F.calcular(d)["renglones"][0]["width_source"] == "E00.01 catálogo"


if __name__ == "__main__":
    n = 0
    for k, f in list(globals().items()):
        if k.startswith("test_") and callable(f):
            f()
            n += 1
            print("OK", k)
    print(f"{n} tests OK")
