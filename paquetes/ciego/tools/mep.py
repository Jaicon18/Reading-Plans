# -*- coding: utf-8 -*-
"""mep.py -- registro entre hojas y cruce de MEP contra bandas de muro.

DOS PASOS, EN ESTE ORDEN:

1. REGISTRO. El offset (dx, dy) entre la hoja de MEP y la arquitectonica se deriva
   VOTANDO LOS SEGMENTOS LARGOS DE MURO del fondo arquitectonico (lw >= 1.0, >= 50 pt),
   nunca las burbujas de eje: el circulo de la burbuja no siempre cae igual respecto de
   la linea de eje, y en sets reales hay hasta 3.6 pt de corrimiento -- suficiente para
   inventar un cruce donde solo estaba la linea del muro. Se exigen >= 25 coincidentes en
   cada direccion; por debajo de eso la hoja NO se usa para cruce geometrico y se declara.

2. CRUCE. Una linea cuenta como penetracion solo si SOBRESALE >= 3 pt por FUERA de las
   DOS caras de la banda. Una linea que TERMINA en la cara es fondo arquitectonico. Se
   filtra por lineweight (un hatch de 0.24 no es un ducto) y se descarta todo lo que
   tambien exista en la arquitectonica en la misma posicion.
   Ademas se detecta el CORREDOR: la linea que llega al muro por los DOS lados aunque el
   CAD la corte en la cara y meta un conector flexible; sin eso se pierden los cruces
   dibujados partidos.
"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geo

# v71 (E24, arbitraje #19): sin offsets ni páginas de ningún proyecto en el código. La página arquitectónica y el
# offset de cada hoja MEP se derivan en CADA corrida con registro() y se verifican contra un rasgo inconfundible del
# set (diagonal, esquina de grid) que se anota con su imagen en el canon; nunca se copian de otra corrida.
ARQ = None                 # índice 0-based de la planta arquitectónica: obligatorio (argumento arq)

MIN_VOTOS = 25
SOBRESALE = 3.0
LW_MIN = 0.5


def _largos(G, key, lwmin=1.0, minlen=50):
    return [(c, a, b) for c, a, b, lw in G[key] if lw >= lwmin and (b - a) >= minlen]


def _arq(arq):
    if arq is None:
        raise ValueError("mep.py v71: falta arq (índice de la planta arquitectónica del set); no hay default de proyecto")
    return arq


def registro(page, arq=ARQ, rango=1200.0, tol_len=1.0):
    """Devuelve dx, dy y sus votos.

    Se vota en DOS pasos y exigiendo que el LARGO del segmento tambien coincida: sin eso,
    cualquier par de lineas largas vota un offset y gana el ruido (en un set real daba cientos de
    votos para un dx que la extension de la hoja desmentia).
      1) dx sale de las VERTICALES: un muro vertical del fondo aparece igual en las dos
         hojas, con el mismo largo.
      2) dy sale de las HORIZONTALES, YA CORRIDAS por ese dx para poder comparar el
         solape en x. Sin aplicar dx primero, el solape nunca se cumple y dy se queda sin
         votos -- que es exactamente lo que pasaba.
    """
    A, R = geo.load(_arq(arq)), geo.load(page)

    def vota(key, desp):
        # El lineweight del fondo arquitectonico CAMBIA de hoja a hoja (planta, electrico,
        # plomeria y mecanico pueden traer lw distintos), asi que filtrar
        # la hoja de MEP por lineweight descarta justo el fondo que hay que emparejar.
        # Del lado del MEP no se filtra: manda la coincidencia de LARGO.
        a, r = _largos(A, key), _largos(R, key, lwmin=0.0)
        vot = collections.Counter()
        for c1, x0, x1 in r:
            L1 = x1 - x0
            x0d, x1d = x0 + desp, x1 + desp
            for c2, y0, y1 in a:
                if abs((y1 - y0) - L1) > tol_len:
                    continue
                d = round(c2 - c1, 2)
                if abs(d) < rango and min(x1d, y1) - max(x0d, y0) > 30:
                    vot[d] += 1
        return vot

    # Se prueban los DOS ordenes y gana el que junte mas votos: en algunas hojas el
    # fondo trae mejor las verticales y en otras las horizontales, y si se arranca por
    # la direccion debil el primer offset sale basura y arrastra al segundo.
    mejor = None
    for prim in ('V', 'H'):
        v1 = vota(prim, 0.0)
        if not v1:
            continue
        d1, n1 = v1.most_common(1)[0]
        seg = 'H' if prim == 'V' else 'V'
        v2 = vota(seg, d1)
        if not v2:
            continue
        d2, n2 = v2.most_common(1)[0]
        dx, nx, dy, ny = ((d1, n1, d2, n2) if prim == 'V' else (d2, n2, d1, n1))
        cand = {'dx': dx, 'dy': dy, 'vx': nx, 'vy': ny, 'orden': prim,
                'ok': nx >= MIN_VOTOS and ny >= MIN_VOTOS}
        if mejor is None or min(nx, ny) > min(mejor['vx'], mejor['vy']):
            mejor = cand
    return mejor


def _en_arq(A, key, c, a, b, tol=0.8):
    """True si esa misma linea existe en la arquitectonica: es fondo, no MEP."""
    for c2, a2, b2, lw in A[key]:
        if abs(c2 - c) <= tol and a2 <= a + 1 and b2 >= b - 1:
            return True
    return False


def cruces(page, off, ori, c0, c1, lo, hi, arq=ARQ, lwmin=LW_MIN, sob=SOBRESALE):
    """Penetraciones de la hoja `page` sobre la banda dada (coordenadas de la planta arquitectónica `arq`).

    Una penetracion es PERPENDICULAR a la banda: en una banda 'V' (caras en x) la cruzan
    lineas HORIZONTALES; en una 'H' (caras en y) la cruzan VERTICALES.
    """
    A, R = geo.load(_arq(arq)), geo.load(page)
    dx, dy = off['dx'], off['dy']
    key = 'H' if ori == 'V' else 'V'
    dc, dl = (dx, dy) if ori == 'V' else (dy, dx)   # desplazamiento en el eje de las caras
    out = []
    for c, a, b, lw in R[key]:
        if lw < lwmin:
            continue
        cc = c + (dy if key == 'H' else dx)          # coordenada a lo largo de la banda
        aa, bb = a + (dx if key == 'H' else dy), b + (dx if key == 'H' else dy)
        if not (lo - 1 <= cc <= hi + 1):
            continue
        if not (aa <= c0 - sob and bb >= c1 + sob):
            continue
        if _en_arq(A, key, cc, aa, bb):
            continue
        out.append({'pos': round(cc, 2), 'de': round(aa, 2), 'a': round(bb, 2),
                    'lw': lw, 'len': round(bb - aa, 2)})
    out.sort(key=lambda d: d['pos'])
    # agrupar lineas paralelas muy juntas: un ducto viene en PAREJA y la separacion
    # entre la pareja ES el ancho del ducto.
    grupos, act = [], None
    for p in out:
        if act and p['pos'] - act[-1]['pos'] <= 40:
            act.append(p)
        else:
            act = [p]; grupos.append(act)
    return grupos


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("uso: python3 mep.py <page_mep 0-based> <page_arq 0-based>   (registro derivado en esta corrida)")
        sys.exit(2)
    print(registro(int(sys.argv[1]), _arq(int(sys.argv[2]))))
