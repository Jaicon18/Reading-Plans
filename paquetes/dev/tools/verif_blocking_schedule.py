# -*- coding: utf-8 -*-
"""verif_blocking_schedule.py -- COMPUERTA: cada tag de un schedule que se monta en wall
tiene que aparecer en el take-off, con cantidad de BLOCKING o con exclusion que lo NOMBRE.

ORIGEN (10-oct-2026, barrido de los detalles sin abrir). El take-off tenia blocking en
<n> renglones y ninguno era de millwork, salvo una unidad (<n> LF) dentro del cierre de un
wall. Faltaban <n> LF: <n> unidades de millwork apoyadas contra partition, cada una con
su length impreso en su propio plan de millwork.

NO FALTO LA FUENTE. La fuente estaba citada TEXTUAL dentro del cierre de un wall desde
hacia semanas -- general note C de A02.01, "CONTRACTOR SHALL PROVIDE BLOCKING FOR ALL
EQUIPMENT AND ACCESSORIES MOUNTED ON WALLS" -- y ademas repetida en la SHEET NOTE D de tres
hojas de millwork: "PROVIDE FRTW BLOCKING AT ALL MILLWORK VERTICAL SURFACE CLEATS AND
MOUNTING LOCATIONS".

LO QUE FALLO FUE LA DIRECCION DEL BARRIDO:

    Se barrio WALL POR WALL -- "¿hay un tag MW a 42 pt de ESTA banda?" --
    y nunca TAG POR TAG     -- "¿contra que wall apoya CADA MW del schedule?"

Un barrido por wall solo puede encontrar lo que cae cerca del wall que uno esta cerrando,
y hereda todos los errores de la geometria con la que mide esa cercania. Un barrido por tag
no puede saltarse nada, porque la lista de tags es FINITA y esta IMPRESA en un schedule.
Ademas el barrido por tag encuentra las repeticiones: un tag listado UNA vez en el
MILLWORK SCHEDULE y dibujado DOS veces en el mismo room.

    Un schedule es una lista cerrada. Si el take-off no tiene un renglon por cada
    linea de esa lista, el que falta no se ve -- no hay nada que lo delate.

Esta compuerta es esa lista cerrada, en codigo. Para cada tag: o hay una partida de
BLOCKING que lo nombra, o hay una exclusion que lo nombra. Callarse no es una opcion.

TOPE = 0 desde el primer dia. Un schedule nuevo se declara aqui, no se olvida.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (por defecto, el directorio actual)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", _os_rutas.getcwd())
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import glob
import json
import os
import re

RAIZ = f'{_TW}'
SALIDAS = f'{_TO}'

# LOS DATOS SON DEL PROYECTO y se leen de $TAKEOFF_WORK/blocking_schedules.json (E24):
#   {"schedules": {"<SCHEDULE (hoja)>": ["<tag>", ...]},     lista EXACTA que publica la hoja
#    "instancias": {"<tag>": n},                              tags dibujados mas de una vez
#    "excluidos": {"<tag>": "<motivo>"}}                      sin blocking en ningun wall
# Se leen de la hoja, no de memoria. Sin el archivo no hay schedule declarado y la compuerta
# lo dice (0 schedules) en vez de pasar en silencio con una lista de otro proyecto.
def _datos():
    try:
        return json.load(open(os.path.join(_TW, 'blocking_schedules.json'), encoding='utf-8'))
    except (OSError, ValueError):
        return {}


_D = _datos()
SCHEDULES = dict(_D.get('schedules') or {})

# Tags con mas de una instancia dibujada en planta. El schedule los lista una sola vez.
# Se declara para que la compuerta exija una partida POR INSTANCIA.
INSTANCIAS = dict(_D.get('instancias') or {})

TOPE_TAGS_SIN_RENGLON = 0


# --------------------------------------------------------------------------------------
# PRIMERA VERSION DE ESTA COMPUERTA: DECORATIVA. Hay que dejarlo escrito.
# Contaba una mencion del tag dentro de una ventana de 2500 caracteres que tuviera la
# palabra BLOCK. Con esa regla, la compuerta PASABA con los <n> LF todavia faltando: los
# cierres de otros walls ya traian exclusiones de BLOCKING que NOMBRAN tags de millwork
# para decir que estan lejos de ESE wall, y esas mismas frases la satisfacian. Se
# probo quitando MWBLOCKING_cierres.json: dio "tags sin renglon: 0" y EXIT 0.
#
#     Una compuerta que pasa con el defecto presente no es una compuerta.
#     Antes de confiar en una hay que BORRAR lo que arreglo y verla fallar.
#
# La version buena no busca texto suelto: recorre la ESTRUCTURA de cada cierre y solo
# acepta dos cosas, las dos verificables una por una:
#   (1) una PARTIDA cuya clave empieza con BLOCKING y cuyo texto NOMBRA el tag, o
#   (2) el tag esta en EXCLUIDOS_PROYECTO de este archivo, con motivo escrito.
# Una nota per-wall del estilo "<tag> esta a <n> pt de este muro" ya NO resuelve el tag:
# dice donde NO va, no donde SI va, y es justo la frase que hacia pasar la version mala.

# Tags que de verdad no llevan blocking en ningun wall del proyecto. Lista cerrada, con
# motivo escrito (blocking_schedules.json, "excluidos").
EXCLUIDOS_PROYECTO = dict(_D.get('excluidos') or {})


def _cierres():
    """[(archivo, nombre_cierre, dict)] de todos los cierres sellados."""
    out = []
    pats = [os.path.join(RAIZ, '*_cierres.json'), os.path.join(RAIZ, '*_cierre.json'),
            os.path.join(SALIDAS, '**', '*.json')]
    vistos = set()
    for pat in pats:
        for f in glob.glob(pat, recursive=True):
            if f in vistos:
                continue
            vistos.add(f)
            try:
                d = json.load(open(f, encoding='utf-8'))
            except Exception:
                continue
            b = os.path.basename(f)
            if isinstance(d, dict) and 'partidas' in d:
                out.append((b, d.get('muro', d.get('num', b)), d))
            elif isinstance(d, dict):
                for k, v in d.items():
                    if isinstance(v, dict) and 'partidas' in v:
                        out.append((b, k, v))
    return out


def _renglones_blocking(cierres):
    """[(archivo, cierre, clave, texto)] de cada PARTIDA cuya clave es de blocking."""
    out = []
    for arch, nom, d in cierres:
        for k, v in (d.get('partidas') or {}).items():
            if k.upper().startswith('BLOCKING'):
                out.append((arch, nom, k, json.dumps(v, ensure_ascii=False)))
    return out


def _cuenta(tag, renglones):
    """n de PARTIDAS de blocking cuyo propio texto nombra este tag."""
    rx = re.compile(r'\b%s\b' % re.escape(tag))
    return sum(1 for _, _, _, t in renglones if rx.search(t))


def faltantes():
    """[(schedule, tag, instancias, partidas_encontradas)] de los tags sin resolver."""
    ren = _renglones_blocking(_cierres())
    out = []
    for sched, tags in SCHEDULES.items():
        for t in tags:
            if t in EXCLUIDOS_PROYECTO:
                continue
            n = INSTANCIAS.get(t, 1)
            hay = _cuenta(t, ren)
            if hay < n:
                out.append((sched, t, n, hay))
    return out


def verificar(verbose=True):
    f = faltantes()
    if verbose:
        ren = _renglones_blocking(_cierres())
        print('COMPUERTA  blocking por tag de schedule')
        print('  %d schedule(s), %d tags; %d renglones de BLOCKING en los cierres sellados'
              % (len(SCHEDULES), sum(len(v) for v in SCHEDULES.values()), len(ren)))
        print()
        print('  %-10s %-6s %-9s %s' % ('tag', 'inst.', 'renglones', 'estado'))
        for sched, tags in SCHEDULES.items():
            for t in tags:
                n = INSTANCIAS.get(t, 1)
                if t in EXCLUIDOS_PROYECTO:
                    print('  %-10s %-6d %-9s EXCLUIDO DE PROYECTO, con motivo' % (t, n, '--'))
                    continue
                hay = _cuenta(t, ren)
                print('  %-10s %-6d %-9d %s'
                      % (t, n, hay, 'OK' if hay >= n else '*** FALTA BLOCKING ***'))
        print()
        print('  tags sin resolver: %d   (tope %d)' % (len(f), TOPE_TAGS_SIN_RENGLON))
    return f


if __name__ == '__main__':
    import sys
    f = verificar()
    if len(f) > TOPE_TAGS_SIN_RENGLON:
        print('\nRECHAZADO: %d tag(s) del schedule sin partida de BLOCKING que los nombre, '
              'y sin exclusion de proyecto con motivo.' % len(f))
        for s, t, n, hay in f:
            print('   %-34s %-8s  %d instancia(s) dibujada(s), %d renglon(es)'
                  % (s, t, n, hay))
        sys.exit(1)
    print('\n  PASA.')
