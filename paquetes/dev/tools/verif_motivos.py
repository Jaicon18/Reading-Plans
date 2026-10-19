# -*- coding: utf-8 -*-
"""verif_motivos.py -- COMPUERTA: ningun eslabon de la cadena sin motivo y sin dato.

ORDEN DE RODOLFO (6-oct-2026, tras preguntar por la cadena del muro A1 #8): cada eslabon de
la secuencia se escribe como `N/HOJA -- motivo -- dato extraido (o "no aplica: motivo")`, y
`cadena_detalles` RECHAZA un eslabon sin motivo y sin dato.

Que exige, eslabon por eslabon, en TODAS las cadenas (muros, cielos, soffits, marquesina y
los bloques sueltos):

  1. MOTIVO DECLARADO. Tiene que existir `motivos_cadena.CONTENIDO[eslabon]`: que es ese
     detalle y que dato contiene, escrito del ROTULO REAL de la hoja. Sin eso, el renglon del
     Excel manda al estimador a una imagen sin decirle que va a encontrar.
  2. MOTIVO DE VERDAD. No vale un placeholder ('TBD', 'idem', 'ver arriba') ni un motivo de
     menos de 40 caracteres: eso es un hueco disfrazado.
  3. DATO RASTREABLE. El eslabon tiene que estar citado en algun campo del cierre y la cita
     tiene que devolver una frase. Un eslabon que la cadena lista y que ningun campo cita es
     justo el candidato a "cita que existe pero es la equivocada": o aporta algo y se dice
     cual, o sale de la cadena.

POR QUE ES UNA COMPUERTA Y NO UNA REGLA ESCRITA: la cadena se genera sola de las citas del
cierre, asi que un eslabon nuevo entra sin que nadie lo decida. Si entra sin motivo, la
columna `Detail sequence` crece y el Excel parece mas documentado cuando en realidad quedo
menos auditable. Esta compuerta vuelve imposible ese crecimiento silencioso.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (antes fijas en /home/claude/boa)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", "/home/claude/boa")
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import json, os, sys, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cadena_detalles as CD
import motivos_cadena as MC

B = f'{_TW}'
# La hoja de entrada de cada familia se DECLARA en motivos_cadena.ENTRADA, no aqui: asi el
# Excel y la compuerta leen la misma declaracion y no se pueden desfasar.
BLOQUES = [f for f in MC.ENTRADA if f.endswith('.json')]


def cierres():
    """[(etiqueta, cierre, hoja de entrada)] de TODO lo sellado."""
    import resumen_global as RG
    out = []
    for t, ws in RG.cargar().items():
        for w in ws:
            out.append(('%s #%s' % (w.get('tag') or t, w.get('muro')), w,
                        MC.ENTRADA['muros']))
    for f in BLOQUES:
        ent = MC.ENTRADA.get(f)
        p = os.path.join(B, f)
        if not os.path.exists(p):
            continue
        d = json.load(open(p, encoding='utf-8'))
        for k, v in d.items():
            if isinstance(v, dict) and 'partidas' in v:
                out.append(('%s %s' % (f.split('_')[0], k), v, ent))
    return out


def verificar():
    """(sin_motivo, motivo_flojo, sin_dato) -- cada uno [(eslabon, [donde])]."""
    g = CD.grafo(); prof = CD.profundidad(g)
    sinm = collections.defaultdict(list)
    flojo = collections.defaultdict(list)
    sind = collections.defaultdict(list)
    for et, w, ent in cierres():
        cs = MC.campos(w)
        for e in CD.cadena(w, ent, prof, g):
            m = MC.CONTENIDO.get(e)
            if not m:
                sinm[e].append(et)
                continue
            ml = m.strip().lower()
            if len(m.strip()) < MC.MIN_MOTIVO or any(p == ml or ml.startswith(p)
                                                     for p in MC.PLACEHOLDER):
                flojo[e].append(et)
            r = MC.rastro(w, e, cs)
            if not r or not (r[0][2] or '').strip():
                sind[e].append(et)
    # Un eslabon DESCARTADO tiene que decir en su motivo por que se descarto. Si no, el
    # renglon dice "Ruled out" sin prueba, que es peor que no decir nada: parece verificado.
    for e, por in MC.DESCARTADOS.items():
        m = (MC.CONTENIDO.get(e) or '')
        if not m:
            sinm[e].append('DESCARTADO sin motivo')
        elif not any(p in m.upper() for p in ('NO ', 'NOT ', 'RULE', 'VERIFIED', 'DRAWS NO')):
            flojo[e].append('DESCARTADO cuyo motivo no dice por que se descarto')
    return (sorted(sinm.items()), sorted(flojo.items()), sorted(sind.items()))


if __name__ == '__main__':
    sinm, flojo, sind = verificar()
    if not (sinm or flojo or sind):
        print('OK: todo eslabon de toda cadena tiene motivo declarado y dato rastreable')
        sys.exit(0)
    if sinm:
        print('*** ESLABONES SIN MOTIVO DECLARADO (%d):' % len(sinm))
        for e, d in sinm:
            print('    %-12s en %d cierre(s): %s' % (e, len(d), ', '.join(d[:6])))
    if flojo:
        print('*** MOTIVOS QUE NO DICEN NADA (%d):' % len(flojo))
        for e, d in flojo:
            print('    %-12s %s' % (e, MC.CONTENIDO.get(e, '')[:60]))
    if sind:
        print('*** ESLABONES EN LA CADENA QUE NINGUN CAMPO CITA (%d):' % len(sind))
        for e, d in sind:
            print('    %-12s en %d cierre(s): %s' % (e, len(d), ', '.join(d[:6])))
    sys.exit(1)
