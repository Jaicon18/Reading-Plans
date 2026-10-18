# -*- coding: utf-8 -*-
"""Tests v70 de closer.py (datos sintéticos). Correr: python3 test_closer_v70.py

Header de acero por otros (lintel / HSS estructural): Abertura(..., piezas=0, header="steel_by_others",
header_source="N/HOJA") = header 0 con fuente -> el wall se sella. 0 piezas sin ese header + fuente -> rechazo.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from closer import Val, CierreRechazado  # noqa: E402
from test_closer import muro_ok  # noqa: E402


def _muro(lf, **ab):
    w = muro_ok()
    del w.excluidas['HEADER']
    studs = (int(10.0 * 12 // 16) + 1) + 4
    w.partida('STUD', Val(studs, 'DERIVADO', operacion='campo + 4 jambs ; 7/Z5.20 METAL STUDS SCHEDULES'), 'pz')
    w.abertura('hueco', 'SF-9', 6.0, 8.0, head='3/Z2.20', **ab)
    w.partida('HEADER', Val(lf, 'DERIVADO', operacion='(6.0 + 1.333) x piezas ; 3/Z2.20'), 'LF')
    return w


def _rechazo(fn, txt):
    try:
        fn()
    except CierreRechazado as e:
        assert txt in str(e), str(e)
        return
    raise AssertionError('debía rechazar: ' + txt)


def test_storefront_steel_by_others_sella():
    d = _muro(0.0, piezas=0, header='steel_by_others', header_source='3/Z2.20 HSS lintel').emit()
    ab = d['aberturas'][0]
    assert ab['piezas'] == 0 and ab['header'] == 'steel_by_others' and ab['header_source'].startswith('3/Z2.20'), ab
    d = _muro(0.0, header='steel_by_others', header_source='J/Z9.23').emit()          # piezas omitidas = 0
    assert d['aberturas'][0]['piezas'] == 0


def test_cero_piezas_sin_steel_rechaza():
    _rechazo(lambda: _muro(0.0, piezas=0).emit(), "piezas debe ser entero >= 1")
    _rechazo(lambda: _muro(0.0, piezas=0, header='steel_by_others').emit(), "header_source")
    _rechazo(lambda: _muro(0.0, piezas=0, header='steel_by_others', header_source='por otros').emit(),
             "header_source")
    _rechazo(lambda: _muro(14.67, piezas=2, header='steel_by_others', header_source='3/Z2.20').emit(), "piezas=0")
    _rechazo(lambda: _muro(5.0, piezas=0, header='steel_by_others', header_source='3/Z2.20').emit(), "HEADER 5.0")
    _rechazo(lambda: _muro(0.0, piezas=0, header='wood', header_source='3/Z2.20').emit(), "header debe ser")


if __name__ == '__main__':
    fallas = 0
    for k, f in sorted(globals().items()):
        if k.startswith('test_') and callable(f):
            try:
                f()
                print('OK  ', k)
            except Exception as e:  # noqa: BLE001
                fallas += 1
                print('FALLA', k, type(e).__name__, str(e)[:300])
    print('TODOS OK' if not fallas else f'{fallas} FALLA(S)')
    sys.exit(1 if fallas else 0)
