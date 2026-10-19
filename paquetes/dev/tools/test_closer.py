# -*- coding: utf-8 -*-
"""Tests obligatorios de closer.py.

El contrato del skill dice: "Si un test no pasa, la herramienta no se usa."
Hasta el 2026-09-27 los tests estaban escritos en el contrato pero NO en el
repositorio, asi que nadie los corria y dos defectos reales vivieron meses:
  - RE_HOJA exigia dos digitos antes del punto -> rechazaba S2.20 / S5.20 / A4.01
  - el chequeo de track estaba fijo en 2.00 corridas -> un muro de DOBLE HILERA
    (4 corridas) era incerrable

Uso:  python3 tools/test_closer.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from closer import Val, Wall, CierreRechazado, waste

H = 'A02.01 banda medida'          # fuente valida (cita hoja)
MOT = 'se busco en A12.01 y en S5.20 y no aplica a este muro por su condicion'


def muro_ok(**kw):
    """Muro completo y valido. Los kwargs permiten romper una sola cosa."""
    hileras = kw.pop('hileras', 1)
    largo = kw.pop('largo', 10.0)
    w = Wall(kw.pop('num', 1), 'G', 'muro de prueba')
    w.base(Val(largo, 'CONFIRMADO', fuente=H),
           Val(15.25, 'CONFIRMADO', fuente='S2.20 marcador B.O.D.'),
           16, 48, hileras=hileras)
    w.cara('Cuarto A', Val(15.25, 'CONFIRMADO', fuente='A12.01 detalle 5'), '5/8 GYP', 2)
    w.cara('Cuarto B', Val(15.25, 'CONFIRMADO', fuente='A12.01 detalle 5'), '5/8 GYP', 2)
    studs = (int(largo * 12 // 16) + 1) * hileras
    w.partida('STUD', Val(studs, 'DERIVADO', operacion='(floor(L*12/16)+1) x %d ; 7/S5.20 METAL STUDS SCHEDULES' % hileras), 'pz')
    w.partida('TRACK_BOTTOM', Val(largo * hileras, 'DERIVADO', operacion='largo x %d hileras ; 3/A12.01 TYPICAL PARTITION' % hileras), 'LF')
    w.partida('TRACK_TOP', Val(largo * hileras, 'DERIVADO', operacion='largo x %d hileras ; 3/A12.01 TYPICAL PARTITION' % hileras), 'LF')
    w.partida('BOARD:Cuarto A', Val(largo * 15.25 * 2, 'DERIVADO', operacion='L x alto x 2 capas ; 3/A12.01 TYPICAL PARTITION'), 'SF')
    w.partida('BOARD:Cuarto B', Val(largo * 15.25 * 2, 'DERIVADO', operacion='L x alto x 2 capas ; 3/A12.01 TYPICAL PARTITION'), 'SF')
    w.partida('BRACING', Val(largo * 3, 'DERIVADO', operacion='3 lineas x largo ; 3/A12.01 TYPICAL PARTITION'), 'LF')
    w.partida('SEALANT', Val(largo * 2, 'DERIVADO', operacion='arriba y abajo ; 3/A12.01 TYPICAL PARTITION'), 'LF')
    for p in ('HEADER', 'CLIPS', 'INSULATION', 'BLOCKING', 'PATCH'):
        w.excluir(p, MOT)
    w.afirmar_alcance('el detalle 5/A12.01 aplica a este muro',
                      ['A02.01 tag G en la banda', '5/A12.01 PARTITION G'])
    return w


RECHAZOS = []


def rechaza(nombre, fn):
    RECHAZOS.append((nombre, fn))


# --- los 14 del contrato ---
def t01():
    Val(1.0, 'CONFIRMADO', fuente='lo vi en el plano')          # sin hoja citada
def t02():
    Val(1.0, 'DERIVADO')                                        # sin operacion
def t03():
    Val(1.0, 'PENDIENTE')                                       # pendiente con valor
def t04():
    w = muro_ok(); w.abertura('puerta', '110', 3.0, 7.0, head='10/A12.02', sill='x'); w.emit()
def t05():
    w = muro_ok(); w.abertura('ventana', 'W1', 8.0, 2.0); w.emit()   # abertura sin head
def t06():
    muro_ok().afirmar_alcance('x', ['A02.01 solo un eslabon'])
def t07():
    muro_ok().afirmar_alcance('x', ['el tag esta ahi', 'el detalle aplica'])
def t08():
    muro_ok().excluir('BLOCKING', 'no hay')
def t09():
    w = muro_ok(); del w.excluidas['BLOCKING']; w.emit()
def t10():
    w = muro_ok(); w.partida('TRACK_TOP', Val(20.0, 'DERIVADO', operacion='x ; 3/A12.01 TYPICAL PARTITION'), 'LF'); w.emit()
def t11():
    w = muro_ok(); w.partida('TRACK', Val(20.0, 'DERIVADO', operacion='x ; 3/A12.01 TYPICAL PARTITION'), 'LF'); w.emit()
def t12():
    w = muro_ok()
    w.caras[1].alto = Val(9.5, 'CONFIRMADO', fuente='A04.01 RCP')
    del w.partidas['BOARD:Cuarto B']
    w.emit()
def t13():
    w = muro_ok(); w.abertura('puerta', '110', 3.0, 7.0, head='10/A12.02'); w.emit()
def t14():
    w = muro_ok(); w.partida('CLIPS', Val(7, 'DERIVADO', operacion='mal ; 3/A12.01 TYPICAL PARTITION'), 'pz'); w.emit()

# --- los dos NUEVOS, uno por defecto corregido ---
def t15():
    """Muro de DOBLE HILERA con solo 2 corridas de track: debe RECHAZARSE."""
    w = muro_ok(hileras=2)
    w.partida('TRACK_BOTTOM', Val(10.0, 'DERIVADO', operacion='una sola corrida ; 3/A12.01 TYPICAL PARTITION'), 'LF')
    w.partida('TRACK_TOP', Val(10.0, 'DERIVADO', operacion='una sola corrida ; 3/A12.01 TYPICAL PARTITION'), 'LF')
    w.emit()
def t16():
    """Muro de doble hilera con studs de una sola hilera: debe RECHAZARSE."""
    w = muro_ok(hileras=2)
    w.partida('STUD', Val(8, 'DERIVADO', operacion='solo una hilera ; 7/S5.20 METAL STUDS SCHEDULES'), 'pz')
    w.emit()

# --- v64: decisiones del usuario #2 (header por piezas) y #12 (ductos sin header/sill) ---
def _muro_header(lf, piezas):
    w = muro_ok()
    del w.excluidas['HEADER']
    studs = (int(10.0 * 12 // 16) + 1) + 4
    w.partida('STUD', Val(studs, 'DERIVADO', operacion='campo + 4 jambs ; 7/S5.20 METAL STUDS SCHEDULES'), 'pz')
    w.abertura('puerta', 'D2', 4.5, 7.0, head='9/S5.20', piezas=piezas)
    w.partida('HEADER', Val(lf, 'DERIVADO', operacion='(4.5 + 1.333) x piezas ; 7/S5.20 DOUBLE TRACK'), 'LF')
    return w
def t17():
    """HEADER con LF de LÍNEA (5.83) cuando el schedule pide DOUBLE TRACK (2 piezas = 11.67)."""
    _muro_header(5.83, 2).emit()
def t18():
    """HEADER cuantificado con una abertura sin piezas declaradas."""
    _muro_header(11.67, None).emit()
def t19():
    """Ducto / fire damper con header (decisión usuario #12)."""
    w = muro_ok(); w.abertura('ducto', 'FD-1', 1.333, 1.333, head='M01.01'); w.emit()

for n, f in [('01 CONFIRMADO sin hoja', t01), ('02 DERIVADO sin operacion', t02),
             ('03 PENDIENTE con valor', t03), ('04 puerta con sill', t04),
             ('05 abertura sin head', t05), ('06 alcance de un eslabon', t06),
             ('07 alcance sin hoja citada', t07), ('08 EXCLUDED con motivo corto', t08),
             ('09 falta BLOCKING', t09), ('10 track da 3 corridas', t10),
             ('11 track combinado', t11), ('12 board en un renglon con caras distintas', t12),
             ('13 abertura con jambs sin sumar', t13), ('14 clips que no cuadran', t14),
             ('15 doble hilera con 2 corridas', t15), ('16 doble hilera con studs de una', t16),
             ('17 v64 header con LF de linea', t17), ('18 v64 header sin piezas', t18),
             ('19 v64 ducto con header', t19)]:
    rechaza(n, f)


def t20_v68_minimo_descuenta_ro():
    """v68 (#16A): wall 10 ft @16 con door 3 ft. Campo floor(120/16)+1 = 8, dentro del R.O. floor(36/16) = 2 ->
    6 + 4 jambs = 10. Antes exigía 8 + 4 = 12 y obligaba a inflar STUD."""
    w = muro_ok()
    w.partida('STUD', Val(10, 'DERIVADO', operacion='campo 8 - 2 dentro de R.O. + 4 jambs ; 7/S5.20'), 'pz')
    w.abertura('puerta', '110', 3.0, 7.0, head='10/A12.02')
    w.emit()


def main():
    fallos = 0
    print('== TESTS QUE DEBEN SER RECHAZADOS ==')
    for nombre, fn in RECHAZOS:
        try:
            fn()
            print('  FALLO  %-45s NO fue rechazado' % nombre); fallos += 1
        except CierreRechazado:
            print('  ok     %-45s rechazado' % nombre)
        except Exception as e:
            print('  FALLO  %-45s excepcion equivocada: %r' % (nombre, e)); fallos += 1

    print('== TESTS QUE DEBEN PASAR ==')
    try:
        t20_v68_minimo_descuenta_ro()
        print('  ok     v68 minimo de STUD descuenta los studs dentro del R.O.')
    except CierreRechazado as e:
        print('  FALLO  v68 minimo de STUD descuenta R.O.: %s' % e); fallos += 1
    try:
        d = muro_ok().emit()
        print('  ok     muro simple completo -> sello %s' % d['sello'])
    except CierreRechazado as e:
        print('  FALLO  muro simple completo: %s' % e); fallos += 1
    try:
        d = muro_ok(hileras=2, num=2).emit()
        assert d['hileras'] == 2
        print('  ok     muro DOBLE HILERA (4 corridas) -> sello %s' % d['sello'])
    except (CierreRechazado, AssertionError) as e:
        print('  FALLO  muro doble hilera: %s' % e); fallos += 1

    print('== v64 HEADER POR PIEZAS Y DUCTOS ==')
    try:
        _muro_header(11.67, 2).emit()
        w = muro_ok(num=5); w.abertura('ducto', 'FD-1', 1.333, 1.333); w.emit()
        print('  ok     header (R.O. + 1\'-4") x 2 piezas = 11.67 y ducto sin header/sill/jambs aceptados')
    except CierreRechazado as e:
        print('  FALLO  v64 header por piezas / ducto: %s' % e); fallos += 1

    print('== v62 TOLERANCIA RELATIVA EN WALLS < 1 FT (#12B) ==')
    # stub G de 0.33 ft doble row: corridas da 0.67 + 0.67 (0.3333 x 2 redondeado) -> 4.06 runs vs 4.00
    try:
        w = muro_ok(hileras=2, num=3, largo=0.33)
        w.partida('TRACK_BOTTOM', Val(0.67, 'DERIVADO', operacion='0.3333 x 2 ; 5/A12.01 PARTITION G'), 'LF')
        w.partida('TRACK_TOP', Val(0.67, 'DERIVADO', operacion='0.3333 x 2 ; 5/A12.01 PARTITION G'), 'LF')
        w.emit()
        print('  ok     stub 0.33 ft doble row con redondeo de 0.01 aceptado')
    except CierreRechazado as e:
        print('  FALLO  stub 0.33 ft rechazado por redondeo: %s' % e); fallos += 1
    try:
        w = muro_ok(hileras=2, num=4, largo=0.33)
        w.partida('TRACK_BOTTOM', Val(0.33, 'DERIVADO', operacion='1 row ; 5/A12.01 PARTITION G'), 'LF')
        w.partida('TRACK_TOP', Val(0.33, 'DERIVADO', operacion='1 row ; 5/A12.01 PARTITION G'), 'LF')
        w.emit()
        print('  FALLO  stub doble row con track de 1 row NO fue rechazado'); fallos += 1
    except CierreRechazado:
        print('  ok     stub doble row con track de 1 row rechazado')

    print('== REGEX DE HOJA ==')
    from closer import RE_HOJA
    debe = ['A02.01', 'A12.01', 'S2.20', 'S5.20', 'S1.10', 'A4.01', 'M01.01',
            'P01.02', 'E02.01', 'A-410', 'A-101', 'S-201']
    nodebe = ['P-15', 'GL-3', 'B-11', 'TS-1', 'CT-12C', 'MW11', 'WC-3', 'FEC-1', 'DFC-1A']
    for s in debe:
        if RE_HOJA.search(s): print('  ok     acepta %s' % s)
        else: print('  FALLO  rechaza la hoja real %s' % s); fallos += 1
    for s in nodebe:
        if not RE_HOJA.search(s): print('  ok     rechaza el codigo de material %s' % s)
        else: print('  FALLO  acepta %s como hoja' % s); fallos += 1

    print('== WASTE ==')
    m = waste(100.0, 'STUD'); b = waste(100.0, 'BOARD')
    if abs(m['COMPRA'] - 115.0) < .01: print('  ok     metal 15%%: %s' % m)
    else: print('  FALLO  metal: %s' % m); fallos += 1
    if abs(b['COMPRA'] - 106.0) < .01: print('  ok     board 6%%: %s' % b)
    else: print('  FALLO  board: %s' % b); fallos += 1

    print()
    print('RESULTADO: %d fallo(s)' % fallos)
    return 1 if fallos else 0


if __name__ == '__main__':
    sys.exit(main())
