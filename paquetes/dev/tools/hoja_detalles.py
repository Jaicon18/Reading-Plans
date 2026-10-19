# -*- coding: utf-8 -*-
"""hoja_detalles.py -- genera el registro de COBERTURA DE DETALLES del proyecto.

Se escribe leyendo la compuerta, no a mano: si mañana se abre un detalle o se declara uno
como no aplicable, el documento cambia solo.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (antes fijas en /home/claude/boa)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", "/home/claude/boa")
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import os, sys, json, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verif_detalles as VD
import glosario as G

DEST = f'{_TO}/entrega/BOA_COBERTURA_DE_DETALLES.md'
TIT = f'{_TW}/titulos_cache.json'


def main(dest=DEST):
    faltan, uni, cit = VD.verificar()
    titulos = json.load(open(TIT, encoding='utf-8')) if os.path.exists(TIT) else {}
    n_uni = sum(len(v) for v in uni.values())
    n_cit = sum(len(cit.get(h, set()) & uni[h]) for h in uni)
    n_dec = sum(len(VD.NO_APLICAN.get(h, {})) for h in uni)
    n_bar = sum(len(VD.BARRIDO.get(h, {})) for h in uni)
    n_fal = sum(len(s) for _, s, _ in faltan)

    L = ['# COBERTURA DE DETALLES — BofA Broomfield',
         '',
         'Generado %s por `verif_detalles.py`. **No se escribe a mano**: sale de la '
         'compuerta, así que si se abre un detalle o se declara uno no aplicable, este '
         'documento cambia solo.' % datetime.date.today().strftime('%d-%b-%Y'),
         '',
         '## Por qué existe',
         '',
         'Las demás compuertas cazan aritmética e inconsistencia. Ninguna caza *"nunca '
         'abriste ese detalle"*, porque una compuerta solo revisa lo que a alguien se le '
         'ocurrió revisar. Y ese es justo el patrón de lo que se escapa: **condiciones que '
         'SÍ están dibujadas y que no se sabe que hay que buscar.**',
         '',
         'Esta compuerta arma el universo de detalles de **las hojas que el propio '
         'take-off declara como fuente** y lo compara contra los que los cierres citan. '
         'No decide si un detalle aplica — eso lo decide quien lo lee. Impide cerrar sin '
         'haberlo mirado.',
         '',
         '## Estado',
         '',
         '| | |', '|---|---|',
         '| Hojas que el take-off usa | **%d** |' % len(cit),
         '| Detalles en esas hojas | **%d** |' % n_uni,
         '| Abiertos y citados | **%d** |' % n_cit,
         '| Mirados y declarados NO APLICABLES | **%d** |' % n_dec,
         '| Abiertos en el barrido del 10-oct-2026 y cerrados con motivo | **%d** |' % n_bar,
         '| **Pendientes de abrir** | **%d** |' % n_fal,
         '']

    if faltan:
        L += ['## Pendientes de abrir', '',
              '| hoja | # | título |', '|---|---|---|']
        for h, sin, _ in faltan:
            for n in sin:
                t = (titulos.get(h, {}) or {}).get(str(n)) or\
                    (titulos.get(h, {}) or {}).get(n) or '—'
                L.append('| `%s` | %d | %s |' % (h, n, str(t)[:70]))
        L.append('')

    L += ['## Abiertos en el barrido del 10-oct-2026 y cerrados con motivo', '',
          'No son "no aplicables": son detalles que SI aplican y que RESPALDAN una cantidad '
          'que ya esta en el take-off, o que la VALIDAN por segunda fuente. Declararlos como '
          'no aplicables diria lo contrario de la verdad, asi que van en su propio bloque.',
          '', '| hoja | # | que se vio y por que queda cerrado |', '|---|---|---|']
    for h in sorted(VD.BARRIDO):
        for n, m in sorted(VD.BARRIDO[h].items()):
            L.append('| `%s` | %d | %s |' % (h, n, m.replace('|', '/')))
    L += ['']

    L += ['## Mirados y declarados NO APLICABLES', '',
          'Cada uno con su motivo. Un detalle descartado se declara; no se deja caer en '
          'silencio.', '', '| hoja | # | motivo |', '|---|---|---|']
    for h in sorted(VD.NO_APLICAN):
        for n, m in sorted(VD.NO_APLICAN[h].items()):
            L.append('| `%s` | %d | %s |' % (h, n, m))

    L += ['', '## Lo que encontró en su primera run', '',
          '**`1X1X1 16GA PURLIN` del top track al deck** — A09.33 lo rotula y la palabra '
          'no aparecía ni una vez en el take-off. **139.21 LF agregados.**', '',
          '**`8/A09.33 TYPICAL BULKHEAD DETAIL`** — describe la transición de cielo con '
          '`3 5/8" METAL STUD FRAMING AND TRACK @ 16" O.C.` más bracing @ 48", bastante '
          'más que el *kicker @ 48"* que decía el pendiente del perímetro.', '',
          '**9 falsos positivos** — detalles que sí se leyeron pero citados en prosa '
          '(*"el detalle C1"* en vez de `6/A12.01`). De ahí la regla: **una cita que una '
          'máquina no puede leer no se puede auditar.**']

    txt = G.traducir('\n'.join(L))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, 'w', encoding='utf-8').write(txt)
    print('cobertura de detalles -> %s  (%d sin abrir, %d declarados)' % (dest, n_fal, n_dec))
    return dest


if __name__ == '__main__':
    main()
