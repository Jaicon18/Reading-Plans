#!/usr/bin/env python3
"""Tests v70 de headers.py _src (datos sintéticos). Correr: python3 test_headers_v70.py

Las fuentes se parten por , ; · solo FUERA de paréntesis (como corridas.py) y aceptan el prefijo "N/HOJA:".
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import headers as H  # noqa: E402
import corridas  # noqa: E402

BUENAS = ["7/Z5.20 HEADER SCHEDULE - WALLS (rows NON LOAD BRG., INTERIOR, ALL FLOORS)",
          "6/Z8.11: recess framing at the vendor unit",
          "3/Z9.27 (6\", 16 ga); Z2.01 vector, 1/Z9.25",
          "F/1/Z5.20"]
MALAS = ["según plano", "7/Z5.20, ver nota general", "header (7/Z5.20)"]


def test_src_respeta_parentesis_y_dos_puntos():
    for s in BUENAS:
        assert H._src(s, "t") == s.strip(), s


def test_src_sigue_rechazando_lo_que_no_es_fuente():
    for s in MALAS:
        try:
            H._src(s, "t")
            raise AssertionError(f"aceptó '{s}'")
        except ValueError as e:
            assert "N/HOJA" in str(e), e


def test_mismo_splitter_que_corridas():
    for s in BUENAS + MALAS:
        assert H._partes(s) == corridas._partes(s), s


def test_calcular_con_fuente_entre_parentesis():
    d = {"header_schedule": {"source": BUENAS[0], "rows": [{"max_span_ft": 8.0, "type": "DOUBLE TRACK",
                                                             "pieces": 2, "piece": "track"}]},
         "openings": [{"ref": "d1", "kind": "door", "location": "interior", "ro_w_ft": 3.0, "qty": 1,
                       "with_sill": False, "source": "6/Z8.11: door in the vendor wall"}]}
    out = H.calcular(d)
    assert abs(out["totales_lf"]["header"] - 2 * (3.0 + 16 / 12)) < 0.01, out["totales_lf"]


if __name__ == "__main__":
    fallas = 0
    for k, f in sorted(globals().items()):
        if k.startswith("test_") and callable(f):
            try:
                f()
                print("OK  ", k)
            except Exception as e:  # noqa: BLE001
                fallas += 1
                print("FALLA", k, type(e).__name__, str(e)[:300])
    print("TODOS OK" if not fallas else f"{fallas} FALLA(S)")
    sys.exit(1 if fallas else 0)
