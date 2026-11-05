# -*- coding: utf-8 -*-
"""verif_coherencia.py -- EL MISMO DATO DE LA MISMA HOJA NO PUEDE TENER DOS ETIQUETAS.

Origen (8-oct-2026, armando el handoff): la height de stud <n> ft sale del B.O.D.
EL. <n> de S2.20 en cuatro tipos distintos. Los closers de A1, A5 y B2 la sellaban
[DERIVADO] escribiendo la resta contra el datum T/SLAB; `cerrar_A1K.py` la sellaba
[CONFIRMADO]. La linea culpable etiquetaba POR EL VALOR:

    alto = Val(bod,'DERIVADO',...) if bod != <n> else Val(bod,'CONFIRMADO',...)

o sea "si vale <n> es CONFIRMADO". La etiqueta describe COMO se obtuvo el numero, nunca
cuanto vale.

POR QUE `verif_confirmado` NO LO CAZA, y por eso hace falta esta compuerta: esa compuerta
pregunta "¿este [CONFIRMADO] vale exactamente la cota impresa que cita?" y la respuesta era
SI -- <n> esta impreso en S2.20. Lo que se escapa es otra cosa:

> UNA ELEVACION NO ES UNA HEIGHT. S2.20 imprime una ELEVACION (B.O.D. EL. <n>);
> la height del stud es esa elevacion MENOS el datum T/SLAB 0'-0". Que las dos cifras
> coincidan pasa solo porque el datum vale cero. Una resta sigue siendo una resta.

Esa distincion es dificil de revisar caso por caso, asi que la compuerta no la juzga: lo que
exige es COHERENCIA. Si el mismo valor citando la misma hoja aparece con dos etiquetas en
dos cierres, una de las dos esta mal y hay que ir al plano. Es la version de compuerta de la
regla que ya cazo los ocho `alto_board` del A5: "dos tipos con dos etiquetas distintas para
la misma cuenta".

TRINQUETE declarado en 0: no queda ninguna incoherencia, asi que cualquiera nueva rompe la
entrega el mismo dia.
"""
import os, sys, re, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import resumen_global as RG

TOPE_INCOHERENTES = 0

# La hoja citada: se saca del texto de la fuente/operacion, no se declara.
RE_HOJA = re.compile(r'\b([ACEFGMPS]\d{2}\.\d{2}|S\d\.\d{2}|[A-Z]\d{3})\b')

# Casos declarados, con la razon escrita. Una declaracion sin razon se lee como verificada,
# que es peor que no decir nada.
DECLARADOS = {}


def _campos(w):
    """(etiqueta_del_campo, valor, estado, texto) de todo campo sellado con estado."""
    out = []
    for nom, d in (('alto_stud', w.get('alto_stud')), ('largo', w.get('largo'))):
        if isinstance(d, dict) and d.get('estado'):
            t = ' '.join(x for x in (d.get('fuente'), d.get('operacion')) if x)
            out.append((nom, d.get('v'), d.get('estado'), t))
    for i, c in enumerate(w.get('caras') or []):
        d = c.get('alto_board')
        if isinstance(d, dict) and d.get('estado'):
            t = ' '.join(x for x in (d.get('fuente'), d.get('operacion')) if x)
            out.append(('caras[%d].alto_board' % i, d.get('v'), d.get('estado'), t))
    return out


def revisar():
    """[(clave, {estado: [quien...]})] de todo (campo, valor, hoja) con dos etiquetas."""
    vistos = collections.defaultdict(lambda: collections.defaultdict(list))
    for bloque, ws in RG.cargar().items():
        for w in ws:
            for nom, val, estado, txt in _campos(w):
                if val is None:
                    continue
                hojas = tuple(sorted(set(RE_HOJA.findall(txt or ''))))
                if not hojas:
                    continue
                # El campo entra por su CLASE (alto_stud, alto_board, largo), no por su
                # indice de cara: comparar cara 0 contra cara 0 dejaria fuera el caso real.
                clase = nom.split('.')[-1]
                clave = (clase, round(float(val), 4), hojas)
                vistos[clave][estado].append('%s #%s' % (w.get('tag'), w.get('muro')))
    return [(k, dict(d)) for k, d in sorted(vistos.items(), key=lambda t: str(t[0]))
            if len(d) > 1 and str(k) not in DECLARADOS]


def main():
    mal = revisar()
    if not mal:
        print('    OK: ningun dato de la misma hoja lleva dos etiquetas distintas '
              '(tope declarado %d, solo baja)' % TOPE_INCOHERENTES)
        return 0
    print('*** %d DATO(S) CON DOS ETIQUETAS PARA LA MISMA FUENTE:' % len(mal))
    for (clase, val, hojas), d in mal:
        print('    %-22s %-10s  hoja(s) %s' % (clase, val, ', '.join(hojas)))
        for estado, quien in sorted(d.items()):
            print('        [%s] %s' % (estado, ', '.join(quien)))
    print('\n    Una de las dos etiquetas esta mal: hay que ABRIR el plano y decidir, no')
    print('    elegir la comoda. Si las dos son correctas por una razon real, se declara')
    print('    en DECLARADOS con esa razon escrita.')
    return 1 if len(mal) > TOPE_INCOHERENTES else 0


if __name__ == '__main__':
    sys.exit(main())
