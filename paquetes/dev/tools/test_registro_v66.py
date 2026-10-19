#!/usr/bin/env python3
"""Tests de registro.py v66: anexar evidencia a un renglón resuelto (#15B ALC-22 quedó NO ENTREGABLE porque la nota
NO APLICA no citaba las hojas del escaneo y el registro no dejaba completarla). Correr: python3 test_registro_v66.py"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import registro as R  # noqa: E402


def _reg():
    d = tempfile.mkdtemp()
    p = os.path.join(d, "registro.json")
    R.crear(p, [{"id": "ALC-1", "tipo": "otro", "ubicacion": "set", "fuente": "A12.01"},
                {"id": "DET-1", "tipo": "detalle", "ubicacion": "S5.20", "fuente": "9/S5.20"},
                {"id": "W-1", "tipo": "wall", "ubicacion": "A02.01", "fuente": "A02.01"}])
    return p


def test_anexar_a_verificado_no_cambia_estado():
    p = _reg()
    R.marcar(p, "ALC-1", "verificado", "NO APLICA: A12.01 sin fire rating")
    r = R.anexar(p, "ALC-1", "hojas del escaneo revisadas: A02.01, E00.01, M00.01 (genéricas)")
    assert r["estado"] == "verificado" and "ANEXO: hojas del escaneo" in r["nota"]
    assert r["nota"].startswith("NO APLICA: A12.01")                 # la nota anterior queda
    assert r["historial"][-1][1] == r["historial"][-1][2] == "verificado"
    R.leer(p)                                                         # cadena y huellas siguen válidas


def test_anexar_corrige_cita_sin_borrar():
    p = _reg()
    R.marcar(p, "DET-1", "pendiente_rfi", "RFI-3 cita en revisión")
    r = R.anexar(p, "DET-1", "corrección: la regla del sill doble sale del cuerpo de 2/S5.20; 9/S5.20 solo dibuja el head")
    assert r["estado"] == "pendiente_rfi" and "2/S5.20" in r["nota"] and "RFI-3" in r["nota"]


def test_anexar_dato_malo():
    p = _reg()
    for rid, txt, msg in (("W-1", "x", "solo a verificado"), ("NOPE", "x", "no existe"), ("W-1", "  ", "exige texto")):
        try:
            R.anexar(p, rid, txt)
        except R.RegistroRoto as e:
            assert msg in str(e), str(e)
        else:
            raise AssertionError("debía fallar: " + msg)
    try:
        R.marcar(p, "W-1", "verificado", "ok")
        R.marcar(p, "W-1", "pendiente", "volver atrás")
    except R.RegistroRoto as e:
        assert "no está permitido" in str(e)
    else:
        raise AssertionError("verificado -> pendiente debía fallar")


if __name__ == "__main__":
    n = 0
    for k, f in list(globals().items()):
        if k.startswith("test_") and callable(f):
            f()
            n += 1
            print("OK", k)
    print(f"{n} tests OK")
