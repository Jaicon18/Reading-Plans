# -*- coding: utf-8 -*-
"""verif_confirmado.py -- COMPUERTA: [CONFIRMADO] significa que el valor ES la cota impresa.

REGLA #0 DE RODOLFO, su propia definicion: `[CONFIRMADO]` = cota impresa, citando la hoja;
`[DERIVADO]` = calculado de 2 o mas cotas confirmadas, MOSTRANDO la operacion. Entre las dos
no hay terreno intermedio, y la jerarquia que las ordena es: **cota impresa > suma de cadena >
pixeles**; los pixeles sirven para verificar o desambiguar, nunca para sustituir.

ORIGEN (7-oct-2026, verificando un muro). El cierre citaba, correctamente, la cota
impresa de la planta -- ticks comprobados en los dos extremos del muro -- y sellaba la
medicion por geometria (pt / 18 a 1/4"=1'-0") redondeada a 2 decimales, que no era la cota:
o sea, el numero que se sello salio de los PIXELES y llevaba la etiqueta de la COTA. El
error era de milesimas de ft y no habria roto nada; lo
que importa es que la etiqueta decia una cosa y el numero venia de otra, y asi es como un
valor medido se cuela con la autoridad de uno impreso.

QUE EXIGE, sin escapatorias:
    todo numero `[CONFIRMADO]` cuyo texto cite una o mas cotas impresas tiene que ser IGUAL a
    alguna de ellas, con la tolerancia del redondeo a 2 decimales (TOL, abajo).

Un multiplo, una suma, una cota mas el espesor de un detalle -- 4 openings x <n>, o
`<n> del ceiling + 6" del detalle 3/A12.01` -- NO son cota impresa: son un CALCULO, y por la
propia definicion de Rodolfo eso es `[DERIVADO]`, que ademas obliga a escribir la operacion.
Admitir "multiplos" y "sumas" como excepcion vaciaria la etiqueta: cualquier numero es la suma
de algo. Por eso la compuerta no las admite y lo que hace es mandarlos a DERIVADO.

OJO CON LA ESCALA (falso positivo real): el rotulo de escala de un detalle -- `3" = 1'-0"`,
`1 1/2" = 1'-0"` -- trae un `1'-0"` que el lector de cotas leia como una cota impresa de 1.00
ft, y entonces TODA partida que citara un detalle salia marcada. Se descarta el `1'-0"` que
viene inmediatamente despues de un `=`.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (por defecto, el directorio actual)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", _os_rutas.getcwd())
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import resumen_global as RG

B = f'{_TW}'
BLOQUES = ('CIELOS_cierres.json', 'SOFFITS_cierres.json', 'CANOPY_cierres.json',
           'MEP_cierre.json', 'HUECOS_cierre.json', 'PUNTOS345_cierres.json',
           'HUMEDAS_cierres.json')
TOL = 0.005                      # el redondeo a 2 decimales, y nada mas
COTA = re.compile(r"(\d+)\s*'\s*-\s*(\d+)(?:\s+(\d+)\s*/\s*(\d+))?\s*\"")
ESCALA = re.compile(r"=\s*$")    # lo que va justo antes de la cota

# UN [CONFIRMADO] QUE NO CITA NINGUNA COTA ES EL HUECO MAS GRANDE QUE TUVO ESTA COMPUERTA
# (8-oct-2026). La version original hacia `if cs and not any(...)`: si el texto citado no
# traia NINGUNA cota impresa, no se revisaba nada y el campo pasaba en silencio. Medido el
# dia que se encontro: <n> campos citaban cota y cuadraban, y **<n> no citaban ninguna**. O
# sea que la compuerta verificaba <n> de <n> y su "OK" era casi vacio.
#
# > [CONFIRMADO] significa "este valor ES la cota impresa de la hoja que cito". Si el texto
# > no trae ninguna cota, la afirmacion no se puede comprobar, y una afirmacion que no se
# > puede comprobar no es un CONFIRMADO: es DERIVADO (y entonces escribe la operacion) o
# > PENDIENTE.
#
# Se encontro armando el HANDOFF, porque un handoff obliga a mirar la etiqueta de cada dato
# en vez de la cantidad. Lo destapo `verif_coherencia.py` al ver el MISMO <n> de la hoja estructural
# sellado CONFIRMADO en <n> walls y DERIVADO en <n>.
#
# PAGADO <n> -> <n> el mismo dia, arreglando los GENERADORES (closers) de varios types: eran la height de stud etiquetada CONFIRMADO sobre una
# ELEVACION, y el alto_board etiquetado CONFIRMADO citando el detalle de tipo, que da la REGLA
# ("to underside of structure") y no el VALOR. Ahora los dos son DERIVADO con su operacion y la
# cita nombra las DOS hojas: A12.01 la regla, S2.20 el valor.
# TRINQUETE: el atraso se declara en el numero medido y SOLO BAJA. No se bloquea la entrega
# de hoy por una deuda que ya venia, pero el numero se imprime en cada corrida y tiene que
# ir bajando -- igual que TOPE_ES. Se paga ARREGLANDO EL GENERADOR, no la salida.
# ---------------------------------------------------------------------- 10-oct-2026
# ATRASO SALDADO: <n> -> <n>. Los que se pagaron eran DOS clases, no <n> casos:
#
#  (a) <n> campos `alto_stud` de los walls exteriores etiquetados [CONFIRMADO] citando el
#      B.O.D. La height es esa ELEVACION menos el datum T/SLAB 0'-0": una RESTA. Es la
#      regla de la adenda v42 que ya se habia aplicado al A1K y que aqui seguia pendiente.
#  (b) <n> cantidades que citaban el detalle que establece el ITEM y no el VALOR -- el
#      sheathing del canopy, sus TEKS, el corner bead / blocking / trim del soffit, el
#      board W.R. de los banos. La cita prueba que el material VA; el numero es una
#      cuenta. Es la misma regla de la v42 ("un detalle de tipo da la REGLA, no el
#      VALOR") aplicada a una cantidad en vez de a una height.
#
#      Una cita que prueba QUE el material va no prueba CUANTO hay.
#
# EL QUE QUEDA, declarado con su motivo. No es una cota: es un CONTEO leido directo de la
# hoja, y esos no tienen cota que citar. Se deja a la vista en vez de debilitar la regla
# o de inventarle una cota.
# Los conteos directos son DEL PROYECTO (elemento, campo y motivo): se leen de
# $TAKEOFF_WORK/conteos_directos.json = [{"elemento": ..., "campo": ..., "motivo": ...}].
def _conteos_directos():
    p = os.path.join(B, 'conteos_directos.json')
    try:
        return {(d['elemento'], d['campo']): d['motivo'] for d in json.load(open(p, encoding='utf-8'))}
    except (OSError, ValueError, KeyError, TypeError):
        return {}


CONTEOS_DIRECTOS = _conteos_directos()

TOPE_SIN_COTA = 0

# Excepciones DECLARADAS, con su motivo escrito. Nunca se afloja la compuerta en silencio.
DECLARADAS = {}


def _pies(m):
    f = int(m.group(1)); i = int(m.group(2))
    if m.group(3):
        i += int(m.group(3)) / int(m.group(4))
    return f + i / 12.0


def cotas_de(txt):
    """Las cotas impresas que cita un texto, descartando el 1'-0" de un rotulo de escala."""
    out = set()
    for m in COTA.finditer(txt):
        if ESCALA.search(txt[max(0, m.start() - 4):m.start()]):
            continue
        out.add(round(_pies(m), 4))
    return out


def _walk(o, et, out, sin, ruta=''):
    if isinstance(o, dict):
        if o.get('estado') == 'CONFIRMADO' and isinstance(o.get('v'), (int, float)):
            txt = ' '.join(str(o.get(k) or '') for k in ('fuente', 'operacion'))
            cs = cotas_de(txt)
            clave = '%s %s' % (et, ruta)
            if clave not in DECLARADAS:
                if not cs:
                    # No cita NINGUNA cota: la afirmacion no se puede comprobar.
                    if (et, ruta) not in CONTEOS_DIRECTOS:
                        sin.append((et, ruta, float(o['v']), txt[:150]))
                elif not any(abs(float(o['v']) - c) <= TOL for c in cs):
                    out.append((et, ruta, float(o['v']), sorted(cs), txt[:150]))
        for k, v in o.items():
            if k != 'sello':
                _walk(v, et, out, sin, (ruta + '.' + k) if ruta else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            _walk(v, et, out, sin, '%s[%d]' % (ruta, i))


def verificar(devolver_sin=False):
    """[(elemento, ruta, valor sellado, cotas citadas, texto)] que no cuadran.

    Con devolver_sin=True devuelve ADEMAS la lista de los [CONFIRMADO] que no citan
    ninguna cota, que es el atraso del trinquete.
    """
    out, sin = [], []
    for t, ws in RG.cargar().items():
        for w in ws:
            _walk(w, '%s #%s' % (w.get('tag') or t, w.get('muro')), out, sin)
    for f in BLOQUES:
        p = os.path.join(B, f)
        if not os.path.exists(p):
            continue
        for k, v in json.load(open(p, encoding='utf-8')).items():
            if isinstance(v, dict) and 'partidas' in v:
                _walk(v, '%s %s' % (f.split('_')[0], k), out, sin)
    return (out, sin) if devolver_sin else out


if __name__ == '__main__':
    mal, sin = verificar(devolver_sin=True)
    if sin:
        print('    atraso de [CONFIRMADO] que no cita ninguna cota: %d campos '
              '(tope %d, solo baja)' % (len(sin), TOPE_SIN_COTA))
        import collections
        for r, n in collections.Counter(x[1] for x in sin).most_common(6):
            print('        %-30s %d' % (r[:30], n))
    if len(sin) > TOPE_SIN_COTA:
        print('*** EL ATRASO SUBIO: %d > tope %d. Un [CONFIRMADO] nuevo tiene que citar su '
              'cota impresa.' % (len(sin), TOPE_SIN_COTA))
        sys.exit(1)
    if not mal:
        print('OK: todo [CONFIRMADO] que cita cota vale exactamente esa cota impresa')
        sys.exit(0)
    print('*** [CONFIRMADO] QUE NO VALE LA COTA QUE CITA (%d):' % len(mal))
    for et, r, v, cs, t in mal:
        print('    %-18s %-26s sellado %-10s cota(s) citada(s) %s' % (et, r[:26], v, cs))
        print('         %s' % t[:140])
    sys.exit(1)
