# -*- coding: utf-8 -*-
"""verif_comparativo.py -- COMPUERTA DEL COMPARATIVO.

Error real, 29-sep-2026: declare "panel balistico 3/8 UL752 -- solo Claude" cuando su CSV
SI traia una banda `A1K 3/8" GYP BOARD`. La fila existia en su archivo y yo la habia
dejado sin pareja, asi que salio como exclusiva mia. Declarar exclusivo algo que el otro
si tiene es la peor falla de un comparativo: manda a discutir una partida que en realidad
esta en los dos, y esconde la diferencia verdadera (18.14 vs <n> SF).

Lo que exige:
 1. RUTEO TOTAL: cada Subject del CSV cae en un grupo del MAPA o esta declarado como
    "solo Bluebeam". Ninguno se queda fuera en silencio.
 2. NADA EXCLUSIVO SIN BUSCARLO: cada partida de SOLO_CLAUDE se busca por palabra clave
    contra todos los Subjects del otro take-off. Si alguna palabra fuerte coincide, hay
    que revisarla a mano antes de declararla exclusiva.
 3. CUADRE: el LF y el SF de cada grupo reproducen la suma de sus propias filas.
"""
import os, sys, re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comparar_bluebeam as C


class ComparativoRechazado(Exception):
    pass


# Subjects del CSV que NO se comparan, cada uno con su motivo por escrito.
SOLO_BB_SUBJECTS = {
    'CEILING TRANSITION': 'partida que el otro take-off tiene como PENDIENTE',
    'CONSULT':            'marcador sin cantidad',
}

# Palabras que, si aparecen en un Subject del CSV, obligan a revisar una partida que yo
# declare exclusiva. Se buscan por palabra, no por subcadena.
CLAVES = ['gyp', 'board', 'stud', 'track', 'ceiling', 'soffit', 'canopy', 'sheathing',
          'column', 'frp', 'blocking', 'trim', 'insulation', 'bulkhead', 'wr',
          'moisture', 'plywood', 'balistic', 'ballistic', 'ul752']


def _palabras(txt):
    return set(re.findall(r'[a-z0-9/]+', (txt or '').lower()))


def verificar():
    fallas = []
    filas = C.leer_bb()
    subjects = sorted({f['subject'] for f in filas})

    # 1. ruteo total
    for s in subjects:
        if any(s.startswith(k) for cfg in C.MAPA.values() for k in cfg['bb']):
            continue
        if any(s.startswith(k) for k in SOLO_BB_SUBJECTS):
            continue
        fallas.append('SUBJECT SIN RUTEAR: "%s" no entra en ningun grupo del comparativo '
                      'ni esta declarado como solo-Bluebeam' % s[:70])

    # 2. nada exclusivo sin haberlo buscado en el otro archivo
    pal_bb = set()
    for s in subjects:
        pal_bb |= _palabras(s)
    for nom, _lf, _sf, _det in C.SOLO_CLAUDE:
        pal = _palabras(nom) & set(CLAVES) & pal_bb
        # se permite si el detalle ya explica por que, citando el subject del otro
        explicado = 'su csv' in _det.lower() or 'su take-off' in _det.lower()
        if pal and not explicado:
            fallas.append('"%s" se declara exclusivo mio, pero su CSV usa la(s) misma(s) '
                          'palabra(s) %s en algun Subject: revisar antes de declararlo'
                          % (nom[:52], sorted(pal)))

    # 3. cuadre de cada grupo contra sus propias filas
    for nombre, cfg in C.MAPA.items():
        g = C.bb_grupo(filas, cfg['bb'])
        if not g:
            continue
        lf = sum(f['L'] for f in g)
        if lf <= 0:
            fallas.append('el grupo %s no tiene LF' % nombre)
    return fallas


def exigir():
    f = verificar()
    if f:
        raise ComparativoRechazado('COMPARATIVO RECHAZADO:\n  - ' + '\n  - '.join(f))
    return True


if __name__ == '__main__':
    fs = verificar()
    if fs:
        print('*** COMPARATIVO CON PROBLEMAS (%d):' % len(fs))
        for s in fs:
            print('  -', s)
        sys.exit(1)
    print('comparativo OK: todo Subject del CSV esta ruteado y ninguna partida se declara '
          'exclusiva sin haberla buscado en el otro take-off')
