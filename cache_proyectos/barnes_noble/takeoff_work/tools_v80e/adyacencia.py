# -*- coding: utf-8 -*-
"""adyacencia.py -- que wall MUERE contra cual, en A02.01, con su prueba.

PARA QUE. El detalle estructural de conexion de walls (N/HOJA) pone los DOS studs extra de una
interseccion en el wall PASANTE; el que muere contra el se atornilla con
3/4"-#10 PAN HEAD TEK @ 24" O.C. y no lleva stud propio por ese extremo. Para aplicar esa
regla hay que saber quien pasa y quien muere, y eso es un MAPA DE ADYACENCIA. Sin el, el
criterio no se puede unificar y el take-off queda con cuatro criterios conviviendo.

POR QUE NO SE PUDO ANTES, Y QUE CAMBIO. Las fuentes de geometria que habia no pasaban
ninguna prueba: `bandas_por_tipo.json` trae geometrias duplicadas, `inventario.json`
resulto tener CINCO bandas (todas C1), y `wallgeom.py` lleva su propio letrero de que
acierta <n> de <n>. Se extrajo de nuevo desde el vector de A02.01 y la primera version
reprodujo <n>% de los largos sellados -- no servia. El defecto no era la extraccion: era
la CONVENCION DE EXTREMOS. Una banda de wall son dos caras paralelas, y las dos caras NO
terminan en el mismo punto: en cada encuentro una sigue y la otra se corta. Tomando la
INTERSECCION de las dos caras el wall sale corto; tomando la UNION sale su largo real.

    Con interseccion: <n> de <n>.   Con union: <n> de <n> walls de banda simple = <n>%.

    Una fuente de geometria no se usa porque exista: se usa porque PASA una prueba, y la
    prueba se escribe antes de mirar el resultado.

QUE QUEDA FUERA, declarado: los walls que no son banda simple de dos caras paralelas
-- exteriores (llevan sheathing, polyiso y plaster, no dos lineas), forros de columna
(lazo cerrado), bulkheads de doble fila de stud (con SOUNDGUARD en medio), walls
inclinados y walls balisticos (NO_BANDA, abajo: lista del proyecto). Para esos la
adyacencia se declara a mano desde su propio cierre, que ya la trae escrita en prosa.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (por defecto, el directorio actual)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", _os_rutas.getcwd())
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import collections
import json
import os
import sys

T = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, T)

PT_FT = 18.0
TOL_LARGO = 0.45      # ft; tolerancia de largo banda vs sellado
TOL_PUNTA = 9.0       # pt; cuanto puede separarse una punta del eje del otro wall
# tags / bloques del PROYECTO que no son banda simple: $ADYACENCIA_NO_BANDA, separados por coma
NO_BANDA = tuple(x.strip() for x in _os_rutas.environ.get('ADYACENCIA_NO_BANDA', '').split(',') if x.strip())


def _bandas_union():
    try:
        import bandas_v3 as BV             # extractor de bandas DEL PROYECTO (su floor plan)
    except ImportError:
        sys.exit("adyacencia: falta bandas_v3.py de ESTE proyecto (vive en "
                 "_herramientas/py/_proyectos/<proyecto>/; no se usa en otro proyecto)")
    segs = BV._segmentos()
    por = collections.defaultdict(list)
    for ori, c, lo, hi in segs:
        por[ori].append((c, lo, hi))
    out = []
    for ori in ('H', 'V'):
        L = sorted(por[ori])
        for i, (c0, lo0, hi0) in enumerate(L):
            for c1, lo1, hi1 in L[i + 1:]:
                d = c1 - c0
                if d <= 0.5:
                    continue
                if d > 13.0:
                    break
                esp = d / BV.PT_IN
                tipos = [t for t, e in BV.ESPESORES.items()
                         if abs(esp - e) <= BV.TOL_ESP / BV.PT_IN]
                if not tipos or min(hi0, hi1) - max(lo0, lo1) < 4:
                    continue
                lo, hi = min(lo0, lo1), max(hi0, hi1)
                if (hi - lo) < BV.MIN_LARGO:
                    continue
                out.append(dict(ori=ori, eje=round((c0 + c1) / 2, 2), lo=round(lo, 2),
                                hi=round(hi, 2), ft=round((hi - lo) / PT_FT, 3),
                                tipos=tuple(sorted(tipos))))
    return out


def mapa():
    """{wall: dict(ori, eje, lo, hi, ft, tag)} para los walls de banda simple."""
    import corpus
    bs = _bandas_union()
    out, sin = {}, []
    for arch, nom, d in corpus.cierres():
        t = d.get('tag')
        L = d.get('largo', {}).get('v') if isinstance(d.get('largo'), dict) else None
        if not t or not L or t in NO_BANDA:
            continue
        cand = [b for b in bs if t in b['tipos'] and abs(b['ft'] - L) <= TOL_LARGO]
        if not cand:
            sin.append((t, nom, L))
            continue
        b = min(cand, key=lambda z: abs(z['ft'] - L))
        out[str(nom)] = dict(b, tag=t, sellado=L)
    return out, sin


def _contacto(a, b):
    """Clasifica el contacto de una punta de `a` con `b`: 'T', 'esquina' o None.

    DIRECCION. La primera version solo detectaba CONTACTO, y por eso salian parejas
    mutuas ("A muere contra B Y B muere contra A"), que es imposible: en una
    interseccion uno pasa y el otro muere. Lo que decide es DONDE cae la punta:

      T       la punta de `a` cae DENTRO del tramo de `b`, lejos de sus dos extremos
              -> `a` MUERE, `b` PASA. Es la condicion del detalle estructural de interseccion
                 (N/HOJA): los dos studs extra van en `b`, y `a` se atornilla sin stud propio.
      esquina las dos puntas coinciden -> ninguno pasa de largo, los dos terminan ahi.
              Es el detalle de esquina interior / exterior (N/HOJA), que es otra cuenta y por eso
              no se mezcla con la anterior.
    """
    if a['ori'] == b['ori']:
        return []
    out = []
    for punta in (a['lo'], a['hi']):
        if abs(punta - b['eje']) > TOL_PUNTA:
            continue
        if not (b['lo'] - TOL_PUNTA <= a['eje'] <= b['hi'] + TOL_PUNTA):
            continue
        en_extremo_de_b = (abs(a['eje'] - b['lo']) <= TOL_PUNTA or
                           abs(a['eje'] - b['hi']) <= TOL_PUNTA)
        out.append('esquina' if en_extremo_de_b else 'T')
    return out


def adyacencia():
    """{wall: dict(muere_contra, reciben, esquinas, libres)} con la direccion resuelta."""
    m, sin = mapa()
    ady = {k: dict(muere_contra=[], reciben=[], esquinas=[], tag=v['tag'], ft=v['sellado'])
           for k, v in m.items()}
    for a, va in m.items():
        for b, vb in m.items():
            if a == b:
                continue
            for clase in _contacto(va, vb):
                if clase == 'T':
                    ady[a]['muere_contra'].append(b)
                    ady[b]['reciben'].append(a)
                else:
                    ady[a]['esquinas'].append(b)
    for k, v in ady.items():
        v['muere_contra'] = sorted(set(v['muere_contra']))
        v['reciben'] = sorted(set(v['reciben']))
        v['esquinas'] = sorted(set(v['esquinas']))
        # un extremo esta RESUELTO si muere en T o cierra en esquina; lo que sobra es libre
        v['libres'] = max(0, 2 - len(v['muere_contra']) - len(v['esquinas']))
    return ady, sin


if __name__ == '__main__':
    ady, sin = adyacencia()
    print('walls de banda simple mapeados: %d' % len(ady))
    if sin:
        print('sin banda que los reproduzca (%d): %s' % (len(sin), sin))
    print()
    print('%-8s %-5s %7s %-18s %-16s %-14s %s'
          % ('wall', 'tag', 'LF', 'muere contra (T)', 'recibe (T)', 'esquina', 'libres'))
    for k in sorted(ady, key=lambda z: (ady[z]['tag'], z)):
        v = ady[k]
        print('%-8s %-5s %7.3f %-18s %-16s %-14s %d'
              % (k, v['tag'], v['ft'], ','.join(v['muere_contra'])[:18],
                 ','.join(v['reciben'])[:16], ','.join(v['esquinas'])[:14], v['libres']))
    json.dump({k: v for k, v in ady.items()},
              open(f'{_TW}/ADYACENCIA.json', 'w'), indent=1)
    print(f'\n-> {_TW}/ADYACENCIA.json')
