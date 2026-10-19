# -*- coding: utf-8 -*-
"""auditor.py - Compuerta de BARRIDO: cuenta MUROS REALES por tipo, no tags.

Nace del error del 24-sep-2026 en el tipo B: dos tags a 35 pt uno del otro se
dieron por el mismo muro y se perdio un muro entero de 11.83 LF. Uno apuntaba a
un muro VERTICAL y el otro a uno HORIZONTAL.

LA REGLA QUE HACE CUMPLIR: dos tags son el MISMO muro solo si su leader aterriza
en LA MISMA BANDA — misma orientacion Y los mismos dos niveles de cara (±0.06 pt).
Distinta orientacion = muros distintos, por cerca que esten los tags.

Uso:
    from auditor import auditar
    auditar(page_index=23, tag='B', espesor_in=4.875, esperados=6)

Lanza BarridoRechazado si el numero de bandas distintas no coincide con lo que
dice el cierre. No hay modo "seguir con advertencias".
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (antes fijas en /home/claude/boa)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", "/home/claude/boa")
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import sys, itertools, collections
sys.path.insert(0, f'{_TW}')
import tagband

PT_IN, PT_FT = 1.5, 18.0


class BarridoRechazado(Exception):
    """El barrido no cierra. No se cuantifica nada."""


def _corridas(c, pool, hueco=1.5):
    segs = sorted((s[1], s[2]) for s in pool if abs(s[0] - c) <= 0.06 and s[3] >= 0.5)
    m = []
    for a, b in segs:
        if m and a - m[-1][1] <= hueco:
            m[-1][1] = max(m[-1][1], b)
        else:
            m.append([a, b])
    return [tuple(x) for x in m if x[1] - x[0] > 4]


def _tramo_con_punta(a, b, pool, perp, pos):
    """Tramo continuo donde EXISTEN LAS DOS CARAS y que contiene la punta del leader,
    puenteando un hueco SOLO con end cap a los dos lados (regla del END CAP)."""
    f0, f1 = _corridas(a, pool), _corridas(b, pool)
    inter = []
    for a0, a1 in f0:
        for b0, b1 in f1:
            lo, hi = max(a0, b0), min(a1, b1)
            if hi - lo > 4:
                inter.append([lo, hi])
    if not inter:
        return None
    inter.sort()
    caps = sorted({round(s[0], 2) for s in perp
                   if s[3] >= 1.0 and s[1] <= a + 0.5 and s[2] >= b - 0.5})
    fin = [inter[0][:]]
    for lo, hi in inter[1:]:
        g0, g1 = fin[-1][1], lo
        if any(abs(x - g0) <= 0.8 for x in caps) and any(abs(x - g1) <= 0.8 for x in caps):
            fin[-1][1] = hi
        else:
            fin.append([lo, hi])
    for lo, hi in fin:
        if lo - 16 <= pos <= hi + 16:
            return (round(lo, 2), round(hi, 2))
    return None


def _bandas(px, py, H, V, obj, r=30, tol=0.30):
    """Bandas del espesor del schedule cuyo TRAMO contiene la punta del leader."""
    out = []
    for ori, pool, perp in (('V', V, H), ('H', H, V)):
        c = px if ori == 'V' else py
        pos = py if ori == 'V' else px
        lv = sorted({round(s[0], 2) for s in pool
                     if s[3] >= 0.5 and abs(s[0] - c) <= r and s[1] - 16 <= pos <= s[2] + 16})
        for a, b in itertools.combinations(lv, 2):
            esp = (b - a) / PT_IN
            if abs(esp - obj) > tol:
                continue
            t = _tramo_con_punta(a, b, pool, perp, pos)
            if not t:
                continue
            out.append(dict(ori=ori, c0=round(a, 2), c1=round(b, 2), esp=round(esp, 3),
                            ext=t, largo_ft=round((t[1] - t[0]) / PT_FT, 2),
                            err=abs(esp - obj), d=abs((a + b) / 2 - c)))
    # el ganador es el que ENCIERRA la punta (menor distancia del centro a la punta),
    # y solo en empate se desempata por error de espesor. Nunca al reves.
    out.sort(key=lambda z: (z['d'], z['err']))
    return out


def auditar(page_index, tag, espesor_in, esperados=None, verbose=True):
    """Devuelve {clave_de_banda: {...}} — UNA entrada por muro real."""
    H, V, _ = tagband.geom(page_index)
    tags = tagband.barrido(page_index, {tag})[tag]
    porbanda = collections.OrderedDict()
    sin_banda = []
    for e in tags:
        ld = e.get('leader')
        if not ld:
            sin_banda.append((e['cx'], e['cy'], 'SIN LEADER'))
            continue
        cand = _bandas(ld['px'], ld['py'], H, V, espesor_in)
        if not cand:
            sin_banda.append((e['cx'], e['cy'], 'SIN BANDA DEL ESPESOR %.3f"' % espesor_in))
            continue
        b = cand[0]
        k = (b['ori'], b['c0'], b['c1'])          # IDENTIDAD DE BANDA
        porbanda.setdefault(k, dict(**b, tags=[]))['tags'].append((e['cx'], e['cy']))

    if verbose:
        print('TIPO %s  espesor de schedule %.3f"' % (tag, espesor_in))
        print('  tags con caja real: %d   bandas distintas: %d' % (len(tags), len(porbanda)))
        for k, b in porbanda.items():
            print('   %s %8.2f/%8.2f  esp %5.2f"  %7.2f ft  <- %d tag(s) %s'
                  % (b['ori'], b['c0'], b['c1'], b['esp'], b['largo_ft'], len(b['tags']),
                     ['(%.0f,%.0f)' % t for t in b['tags']]))
        for cx, cy, why in sin_banda:
            print('   !! tag (%.1f,%.1f): %s  -> ABRIR IMAGEN' % (cx, cy, why))
        print('   LF cara-a-cara del tipo: %.2f' % sum(b['largo_ft'] for b in porbanda.values()))

    if sin_banda:
        raise BarridoRechazado(
            'TIPO %s: %d tag(s) sin banda resuelta. Cada uno se abre en IMAGEN antes de '
            'descartarlo o aceptarlo: puede ser una burbuja de eje (se descarta) o un tag real '
            'cuyo leader el detector no encontro (se resuelve a mano). %s'
            % (tag, len(sin_banda), sin_banda))
    if esperados is not None and len(porbanda) != esperados:
        raise BarridoRechazado(
            'TIPO %s: el barrido da %d muros reales y el cierre declara %d. NO se cuantifica '
            'hasta resolverlo. Bandas: %s'
            % (tag, len(porbanda), esperados, list(porbanda)))
    return porbanda


if __name__ == '__main__':
    ESQ = {'A5': 7.25, 'B': 4.875, 'B2': 7.25, 'B2K': 7.625, 'C1': 4.25,
           'G': 6.125, 'G1': 8.0, 'A1': 4.875, 'A1K': 5.25}
    t = sys.argv[1]
    try:
        auditar(23, t, ESQ[t], int(sys.argv[2]) if len(sys.argv) > 2 else None)
    except BarridoRechazado as ex:
        print('\nBARRIDO RECHAZADO:', ex)
