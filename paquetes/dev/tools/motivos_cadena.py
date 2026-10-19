# -*- coding: utf-8 -*-
"""motivos_cadena.py -- POR QUE la cadena pasa por cada eslabon, y QUE saco de el.

ORIGEN (6-oct-2026). Rodolfo preguntó, desde un chat normal: "dime para que abriste cada uno
en la secuencia y que extrajiste de el", y pegó la cadena del wall A1 #8. La columna
`Detail sequence` del Excel solo traía los NUMEROS. Sin la sesión original, 9 de los 26
eslabones no se pudieron justificar. La cadena existía y no se podía auditar: decía por dónde
pasó la lectura, no qué aportó cada paso.

REGLA QUE IMPONE ESTE MODULO:
    cada eslabón de la cadena se escribe como  N/HOJA -- motivo -- dato extraido,
    y `verif_motivos.py` RECHAZA la entrega si un eslabón de cualquier cadena no tiene
    las dos cosas.

COMO SE REPARTE EL TRABAJO (lo declarado es lo mínimo, lo demás se deriva):

  1. `CONTENIDO[eslabon]` -- lo UNICO que se declara a mano: qué es ese detalle y qué dato
     contiene. Se escribe del TITULO REAL leído del rótulo de la hoja (`titulo_cita.py`),
     nunca de memoria.
  2. El DATO EXTRAIDO **no se declara**: se lee del propio cierre sellado. `rastro()` busca
     en qué campo del cierre está citado el eslabón y devuelve el texto sellado que lo cita.
     Así el "qué extraje" no se puede inventar ni quedar viejo: si el cierre cambia, el
     registro cambia con él.
  3. La CLASE tampoco se declara: sale del campo que lo cita. El mismo eslabón es DATO en un
     wall y EXCLUSION en otro -- `1/A12.01` da el sealant arriba y abajo en un wall B, y en un
     wall A1 solo entra como CONTRASTE para probar que el A1 lleva una sola run. Declarar
     una clase fija habría sido falso en la mitad de los walls.

Esto resuelve además el otro hallazgo de ese día: los eslabones "injustificables" del A1 #8
(A09.01, A00.01, A09.27, A09.33, E02.01, P01.01, P01.02) son todos **fuente de una EXCLUSION**
-- la cadena va ahí para probar que ahí no hay material nuestro, no para sacar una cantidad.
Y `1/A12.01` y `4/A12.01` son detalles de OTRO tipo de partition citados como CONTRASTE. Una
vez que la clase se deriva del campo, eso se lee solo y no hay que recordarlo.
"""
import json, os, sys, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cadena_detalles as CD

# ---------------------------------------------------------------- CLASE, derivada del campo
# El prefijo del campo del cierre que cita el eslabón dice para qué se abrió. Se evalúa de
# prefijo más largo a más corto.
CLASE_CAMPO = (
    ('excluidas',  'EXCLUSION'),   # se abrió para probar que ahí NO hay material nuestro
    ('alcance',    'ALCANCE'),     # se abrió para probar de qué tipo/alcance es el tramo
    ('largo',      'DIMENSION'),
    ('alto_stud',  'DIMENSION'),
    ('alto_aff',   'DIMENSION'),
    ('alto',       'DIMENSION'),
    ('caras',      'DIMENSION'),   # altura de board por cara
    ('aberturas',  'ABERTURA'),    # marco, head, sill de un vano
    ('partidas',   'CANTIDAD'),    # de ahí sale el perfil, el spacing o la cantidad
    ('detalle',    'NOTA'),
    ('resuelto',   'NOTA'),
    ('ubicacion',  'NOTA'),
    ('sf',         'DIMENSION'),
)
ORDEN_CLASE = ('DIMENSION', 'CANTIDAD', 'ABERTURA', 'ALCANCE', 'EXCLUSION', 'NOTA', '?')
# La clase viaja al entregable, asi que se ESCRIBE en ingles. Igual que dataset.CLASE_EN con
# la clase de abertura: el dato se guarda en espanol porque gobierna la logica, y se traduce
# al escribir. Traducir el dato habria roto la logica; traducir la salida no.
CLASE_EN = {'DIMENSION': 'Dimension', 'CANTIDAD': 'Quantity', 'ABERTURA': 'Opening',
            'ALCANCE': 'Scope', 'EXCLUSION': 'Exclusion', 'NOTA': 'Note',
            'DESCARTADO': 'Ruled out', '?': 'Unclassified'}

# LA RAMA "NO APLICA" DE LA REGLA DE RODOLFO: un eslabon se escribe como
# `N/HOJA -- motivo -- dato extraido (o "no aplica: motivo")`. Estos son los eslabones que se
# ABRIERON y se DESCARTARON: estan en la cadena porque hubo que abrirlos para saber que no
# eran la fuente, y dejarlos sin marcar los hace parecer fuente de algo.
# Se DECLARAN uno por uno. Cada uno tiene que traer su motivo en CONTENIDO diciendo por que
# se descarto, y `verif_motivos` lo comprueba: un descarte sin motivo es peor que no
# declararlo, porque parece verificado.
DESCARTADOS = {
            '7/A11.03': 'abierta y descartada: es la elevacion del rack TECH 1/TECH 2 y no dibuja '
                'plywood; la del plywood es 5/A11.03',
    '9/A00.41': 'no es cita del take-off: es la referencia del propio plano (key note 1 de '
                'A02.01)',
}


def clase_de(campo):
    for pre, cl in CLASE_CAMPO:
        if campo == pre or campo.startswith(pre + '.') or campo.startswith(pre + '['):
            return cl
    return '?'


# ----------------------------------------------- HOJA DE ENTRADA, declarada por familia
# La SUPER REGLA de Rodolfo fija la puerta de entrada de cada familia: floor plan para muros
# y aberturas, RCP para cielos, soffits y marquesinas. Pero la entrada no se puede ASUMIR por
# familia: tiene que ser una hoja que el propio cierre nombre, o la cadena encabeza con un
# eslabon que nadie puede comprobar.
#
# `None` = ese bloque NO se entra por una planta, y decirlo es parte de la honestidad de la
# cadena. Los cuatro bloques con None no son take-off geometrico: son cruces y correcciones
# que trabajan sobre cierres ya cerrados (MEP contra las hojas M/P/E, los puntos sueltos
# contra el detalle que los origina, las zonas humedas contra A08.01). Ponerles A02.01 de
# oficio ponia al frente de su cadena una hoja que su texto nunca nombra -- que es justo lo
# que cazo verif_motivos el primer dia que corrio.
ENTRADA = {}   # v66 (E24): vaciado — eran notas de detalle de un proyecto de examen; se llena por proyecto


# ------------------------------------------------------- CONTENIDO: lo unico escrito a mano
# Formato: eslabon -> que es y que dato contiene.  El titulo entre comillas es el ROTULO REAL
# leido de la hoja por titulo_cita.py; lo de despues es el dato que ese eslabon aporta.
CONTENIDO = {}   # v66 (E24): vaciado — eran notas de detalle de un proyecto de examen; se llena por proyecto


PLACEHOLDER = ('tbd', 'pendiente de justificar', 'por definir', '?', 'xxx', 'ver arriba',
               'igual que arriba', 'idem')
MIN_MOTIVO = 40


def campos(obj, pre=''):
    """[(ruta, texto)] de todo texto citable dentro de un cierre."""
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == 'sello':
                continue
            out += campos(v, '%s.%s' % (pre, k) if pre else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out += campos(v, '%s[%d]' % (pre, i))
    elif isinstance(obj, str) and len(obj) > 2:
        out.append((pre, obj))
    return out


def _cita_en(txt, esl):
    """True si ESE texto cita ESE eslabon (etiqueta + hoja, u hoja suelta)."""
    n, _, h = esl.rpartition('/')
    hn = CD.norm(h)
    for cola, nn, hh in CD.CITA.findall(txt):
        if not cola and CD.norm(hh) == hn and (not n or nn == n):
            return True
    if not n:
        return any(CD.norm(x) == hn for x in CD.SOLO_HOJA.findall(txt))
    return False


# La ruta del campo viaja al entregable en la columna `Cited in`, asi que se ESCRIBE en
# ingles. Las CLAVES del cierre se quedan en espanol porque gobiernan la logica -- el mismo
# criterio de dataset.CLASE_EN: se traduce la salida, nunca el dato.
RUTA_EN = [('caras[', 'face['), ('alcance[', 'scope['), ('aberturas[', 'openings['),
           ('excluidas.', 'excluded.'), ('.cadena[', '.chain['), ('alto_board', 'board_height'),
           ('alto_stud', 'stud_height'), ('alto_aff', 'height_aff'), ('.fuente', '.source'),
           ('largo', 'length'), ('detalle', 'detail'), ('ubicacion', 'location'),
           ('resuelto', 'resolved'), ('penetraciones[', 'penetrations['), ('hojas[', 'sheets[')]


def _corto(r):
    """La ruta del campo, legible y en ingles: line items.STUD.val.operacion -> STUD."""
    r = r.replace('partidas.', '').replace('.val.operacion', '').replace('.operacion', '')
    r = r.replace('.val.fuente', '.fuente')
    for a, b in RUTA_EN:
        r = r.replace(a, b)
    return r.split(':')[0]


def _frase(txt, esl, ancho=320):
    """El trozo del texto SELLADO que contiene la cita. Es el 'dato extraido'."""
    n, _, h = esl.rpartition('/')
    hr = CD.real(h)
    for cand in ([('%s/%s' % (n, hr)) if n else None, hr] if n else [hr]):
        if not cand:
            continue
        i = txt.find(cand)
        if i < 0:
            continue
        # la oracion que lo contiene: del punto-espacio anterior al siguiente.
        # OJO con el -1: si no hay punto antes, rfind devuelve -1 y `-1+2` = 1 se come la
        # PRIMERA LETRA del texto -- "A02.01 geometria..." salia como "02.01 geometria...",
        # o sea un numero de hoja que no existe, justo el error que verif_citas persigue.
        j = txt.rfind('. ', 0, i)
        a = 0 if j < 0 else j + 2
        b = txt.find('. ', i)
        b = len(txt) if b < 0 else b + 1
        s = txt[a:b].strip()
        return s if len(s) <= ancho else s[:ancho - 1].rstrip() + '…'
    return txt[:ancho].strip()


def rastro(obj, esl, cs=None):
    """[(clase, campo, frase)] de DONDE sale ese eslabon dentro de ESE cierre.

    El 'dato extraido' no se declara en ningun lado: se lee del cierre sellado. Si el cierre
    cambia, el registro cambia solo -- que es toda la diferencia entre un registro y un
    comentario que se queda viejo.
    """
    cs = cs if cs is not None else campos(obj)
    out = []
    for r, x in cs:
        if _cita_en(x, esl):
            # OJO: la CLASE se saca de la ruta COMPLETA, no de la abreviada. `_corto` quita
            # el prefijo `partidas.` y vuelve `caras[` en `cara[`, asi que clasificar sobre
            # la abreviada dejaba sin clase 274 de 1137 renglones -- toda partida y toda
            # altura de board salian con '?'. La abreviada es solo para MOSTRAR.
            out.append((clase_de(r), _corto(r), _frase(x, esl)))
    out.sort(key=lambda t: (ORDEN_CLASE.index(t[0]) if t[0] in ORDEN_CLASE else 9, t[1]))
    return out


def log(obj, entrada=None, prof=None, g=None):
    """[(eslabon, clase, contenido, campos, dato)] -- la cadena JUSTIFICADA de un cierre.

    Es lo que se escribe en la hoja `Detail log` del Excel: un renglon por eslabon, con el
    motivo por el que la cadena pasa por ahi y el dato que de ahi salio.
    """
    cs = campos(obj)
    filas = []
    for e in CD.cadena(obj, entrada, prof, g):
        r = rastro(obj, e, cs)
        cl = 'DESCARTADO' if e in DESCARTADOS else (r[0][0] if r else '?')
        campos_ = ', '.join(sorted({x[1] for x in r}))
        dato = r[0][2] if r else ''
        filas.append((e, cl, CONTENIDO.get(e, ''), campos_, dato))
    return filas


if __name__ == '__main__':
    import resumen_global as RG
    g = CD.grafo(); prof = CD.profundidad(g)
    tipo = sys.argv[1] if len(sys.argv) > 1 else 'A1'
    num = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    for t, ws in RG.cargar().items():
        if not t.startswith(tipo):
            continue
        for w in ws:
            if w.get('muro') != num:
                continue
            print('WALL %s #%s  %s' % (w.get('tag'), w.get('muro'), w.get('ubicacion'))[:110])
            print('=' * 104)
            for e, cl, cont, cam, dato in log(w, 'A02.01', prof, g):
                print('\n%-12s [%s]  campos: %s' % (e, cl, cam[:70]))
                print('   que es:  %s' % (cont or '*** SIN MOTIVO DECLARADO ***')[:300])
                print('   dato:    %s' % dato[:300])
