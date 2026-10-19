# -*- coding: utf-8 -*-
"""corpus.py -- EL UNICO lugar donde se pregunta "¿cuales son los cierres?".

ORIGEN (10-oct-2026). Durante el barrido de detalles hice un roll-up de las partidas de
blocking para ver si faltaba el de millwork. Leia `$TAKEOFF_WORK/*_cierres.json` y nada
mas. Los cierres por wall de varios tipos NO viven ahi: viven en
`/mnt/user-data/outputs/**`. Crei que el proyecto tenia <n> renglones de blocking y <n> LF
cuando tiene <n> y <n> LF, declare que faltaba TODO el blocking de millwork, y cuantifique
<n> LF que en su mayoria ya estaban -- la mayoria de las unidades ya cerradas, varias con mejor
metodo que el mio.

    Un inventario que no declara su alcance no es un inventario, es una muestra.
    Y una muestra parcial no prueba que algo FALTE: prueba que no estaba donde mire.

SEGUNDA LECCION, de la primera version de ESTE archivo. Al arreglarlo escribi aqui una lista
de globs nueva. Mal: ya existia la lista buena, `resumen_global.SRC` mas `verif_vigencia`,
que es la que de verdad alimenta el Excel y que ya distingue los cierres SUPERADOS (los
G_cierres.json contra G_cierres_v2.json). Mi lista nueva leia <n> cierres incluyendo los
superados y daba <n> SF de board donde el entregable tiene <n>.

    Crear una segunda fuente de verdad para arreglar un error de alcance
    es volver a cometerlo, con mas pasos.

Asi que este modulo no declara nada propio: le pregunta a `verif_vigencia.fuentes()`. Lo
unico que agrega es la DISTINCION que al roll-up le faltaba, y que son dos preguntas
distintas que nunca hay que confundir:

    cierres()              -> los VIGENTES. Para SUMAR. Es lo que va al Excel.
    cierres(todos=True)    -> todos, superados incluidos. Para preguntar COBERTURA
                              ("¿algun cierre, el que sea, nombra el tag <ref>?").

Sumar con el conjunto de cobertura infla el total. Preguntar cobertura con el conjunto
vigente deja fuera cierres reales. Las dos equivocaciones se cometieron el mismo dia.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (por defecto, el directorio actual)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", _os_rutas.getcwd())
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import glob
import json
import os

RAIZ = f'{_TW}'
SALIDAS = f'{_TO}'
AQUI = os.path.dirname(os.path.abspath(__file__))

# Solo para `todos=True`: el barrido ancho, que a proposito incluye los superados.
PATRONES_ANCHOS = (
    os.path.join(RAIZ, '*_cierres.json'),
    os.path.join(RAIZ, '*_cierre.json'),
    os.path.join(SALIDAS, '**', '*.json'),
)
NO_SON_CIERRES = ('dataset', 'handoff', 'indice', 'resumen', 'numeros_antes')

# TRINQUETE: hoy hay estos cierres vigentes y SOLO PUEDE CRECER. Si una herramienta ve
# menos, esta leyendo un subconjunto y lo que concluya sobre lo que "falta" no vale.
TOPE_CIERRES_MIN = 88


def archivos(todos=False):
    """Rutas de los archivos de cierre. Por defecto, los VIGENTES que lee el entregable."""
    if not todos:
        import sys
        if AQUI not in sys.path:
            sys.path.insert(0, AQUI)
        import verif_vigencia as VV
        return [f for f in VV.fuentes() if f.endswith('.json')]
    out, vistos = [], set()
    for pat in PATRONES_ANCHOS:
        for f in sorted(glob.glob(pat, recursive=True)):
            b = os.path.basename(f).lower()
            if f in vistos or any(x in b for x in NO_SON_CIERRES):
                continue
            vistos.add(f)
            out.append(f)
    return out


def cierres(todos=False):
    """[(archivo, nombre_del_cierre, dict)]."""
    out = []
    for f in archivos(todos):
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


def partidas(prefijo=None, todos=False):
    """[(archivo, cierre, clave, dict_de_la_partida)]; `prefijo` filtra por clave."""
    out = []
    for arch, nom, d in cierres(todos):
        for k, v in (d.get('partidas') or {}).items():
            if prefijo and not k.upper().startswith(prefijo.upper()):
                continue
            out.append((arch, nom, k, v))
    return out


def total(prefijo):
    """Suma de las partidas VIGENTES cuya clave empieza con `prefijo`. Nunca con todos=True."""
    vis, t = set(), 0.0
    for arch, nom, k, v in partidas(prefijo):
        key = (str(nom), k, v['val']['v'])
        if key in vis:
            continue
        vis.add(key)
        if isinstance(v['val']['v'], (int, float)):
            t += v['val']['v']
    return round(t, 2)


if __name__ == '__main__':
    v, t = cierres(), cierres(todos=True)
    print('corpus de cierres')
    print('  VIGENTES (para sumar)      : %3d cierres en %d archivos   (tope minimo %d)'
          % (len(v), len(archivos()), TOPE_CIERRES_MIN))
    print('  TODOS    (para cobertura)  : %3d cierres en %d archivos'
          % (len(t), len(archivos(todos=True))))
    print()
    print('  %-16s %9s %12s' % ('partida', 'renglones', 'total vigente'))
    for p in ('BLOCKING', 'STUD', 'TRACK_BOTTOM', 'TRACK_TOP', 'BOARD', 'BRACING', 'SEALANT'):
        n = len(set((str(x[1]), x[2], x[3]['val']['v']) for x in partidas(p)))
        print('  %-16s %9d %12.2f' % (p, n, total(p)))
