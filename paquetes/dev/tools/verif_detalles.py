# -*- coding: utf-8 -*-
"""verif_detalles.py -- COMPUERTA DE COBERTURA DE DETALLES.

El punto ciego que esta compuerta ataca (1-oct-2026, a pregunta de Rodolfo):

    Las otras compuertas cazan aritmetica e inconsistencia -- que una columna signifique
    lo que dice, que los segmentos sumen, que el libro refleje los cierres. Ninguna caza
    "NUNCA ABRISTE EL DETALLE 2/S5.20", porque una compuerta solo revisa lo que a alguien
    se le ocurrio revisar.

    Y ese es justo el patron de lo que se me escapa: condiciones que SI estan dibujadas y
    que no se que tengo que buscar. El head track doble de vanos > 4'-0" (56 LF) estaba
    rotulado en 2/S5.20 desde el principio. Las zonas humedas estaban en la nota F de
    A08.01 y en el key note 6 del Finish Plan. Nadie las escondio: no las abri.

Que hace: arma el UNIVERSO de detalles de las hojas que el propio take-off declara como
fuente -- si un cierre cita A12.01, entonces TODOS los detalles dibujados en A12.01 son
del universo -- y lo compara contra los detalles que los cierres citan de verdad. Lo que
queda sin citar se reporta como SIN ABRIR.

No decide si un detalle aplica o no: eso lo decide quien lo lee. Lo que impide es cerrar
sin haberlo mirado.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (antes fijas en /home/claude/boa)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", "/home/claude/boa")
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import os, sys, re, json, glob, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import resumen_global as RG

PDF = f'{_TW}/BOA_SIN_MARKUPS.pdf'
B = f'{_TW}'
EXTRA = ['CIELOS_cierres.json', 'SOFFITS_cierres.json', 'CANOPY_cierres.json',
         'MEP_cierre.json', 'HUECOS_cierre.json', 'PUNTOS345_cierres.json',
         'HUMEDAS_cierres.json']

# 1-2 digitos antes del punto. Con `\d{2}` fijo, TODA la serie estructural (S2.20, S5.10,
# S5.20) quedaba invisible para la compuerta -- y ahi viven el METAL STUDS SCHEDULE, el
# BRACE SCHEDULE, el HEAD TRACK y el PARAPET INFILL FRAMING, que son nuestros. Error del
# 2-oct-2026: la compuerta nunca pudo ver las hojas S, y no lo decia.
HOJA = re.compile(r'^[A-Z]{1,2}\d{1,2}\.\d{2}$')
NUM = re.compile(r'^\d{1,2}$')
CITA = re.compile(r'(\d{1,2})\s*/\s*([A-Z]{1,2}\d{1,2}\.\d{2})')


class DetalleSinAbrir(Exception):
    pass


# Detalles que se miraron y NO aplican, cada uno con su motivo por escrito. Un detalle
# descartado se declara; no se deja caer en silencio.
NO_APLICAN = {}   # v66 (E24): vaciado — era el barrido de detalles de un proyecto de examen; se llena por proyecto



# ---------------------------------------------------------------------- 10-oct-2026
# BARRIDO COMPLETO. Las 26 hojas que el take-off usa se recorrieron detalle por detalle
# el 10-oct-2026, a 300-900 dpi, y cada uno quedo en uno de dos estados: CITADO por un
# cierre, o declarado aqui con su motivo. El registro largo esta en
# BOA_BARRIDO_DE_DETALLES.md.
#
# Por que este diccionario es DISTINTO de NO_APLICAN: hasta hoy la compuerta contaba 90
# "sin abrir" y la mayoria SI se habian mirado -- lo que faltaba era DECLARARLO. Pero
# muchos de esos 90 no son "no aplicables": son detalles que SI aplican y que RESPALDAN
# una cantidad que ya esta en el take-off, o que la VALIDAN por segunda fuente
# (8/A09.33 confirma el bracing a 48" del bulkhead; 9/S5.10 ROOF STEP AT GRID B confirma
# el escalon de deck en el eje B; 4 y 5/A09.33 confirman la composicion del canopy).
# Meterlos en NO_APLICAN diria que no aplican, y es falso.
#
#     Declarar un detalle que SI aplica como "no aplicable" es mentir en la direccion
#     comoda: la compuerta queda en cero y el documento dice lo contrario de la verdad.
#
# Por eso van en su propio bucket, con su propio renglon en el reporte.
BARRIDO = {}   # v66 (E24): vaciado — era el barrido de detalles de un proyecto de examen; se llena por proyecto


# Las dos listas juntas son lo que la compuerta considera DECLARADO.
def _declarados(hoja):
    return set(NO_APLICAN.get(hoja, ())) | set(BARRIDO.get(hoja, ()))


def _texto_cierres():
    """Todo el texto de los cierres sellados, de una sola pieza."""
    fs = []
    for pats in RG.SRC.values():
        for p in pats:
            fs.extend(sorted(glob.glob(p)))
    fs += [os.path.join(B, f) for f in EXTRA if os.path.exists(os.path.join(B, f))]
    return '\n'.join(open(f, encoding='utf-8').read() for f in sorted(set(fs)))


def citados(txt=None):
    """{hoja: {numeros de detalle citados}} -- lo que el take-off dice haber leido."""
    txt = txt if txt is not None else _texto_cierres()
    out = collections.defaultdict(set)
    for n, h in CITA.findall(txt):
        out[h].add(int(n))
    return out


def burbujas_de(pdf, idx):
    """Los detalles DIBUJADOS en una pagina: un numero justo encima de un numero de hoja."""
    ws = pdf.pages[idx].extract_words() or []
    hojas = [w for w in ws if HOJA.match(w['text'].strip())]
    nums = [w for w in ws if NUM.match(w['text'].strip())]
    out = collections.defaultdict(set)
    for h in hojas:
        for n in nums:
            dy = h['top'] - n['top']
            dx = abs((h['x0'] + h['x1']) / 2 - (n['x0'] + n['x1']) / 2)
            if 4 < dy < 30 and dx < 22:
                out[h['text'].strip()].add(int(n['text']))
    return out


def rotulo_de(ws, ancho, alto):
    """El numero de hoja de una pagina, leido del TITLE BLOCK (esquina inferior derecha).

    Antes salia del token que MAS se repetia, y eso falla justo donde importa: una hoja de
    elevaciones llena de burbujas de seccion tiene mas `A09.21` que `A09.01`, y el cache le
    ponia el rotulo de otra hoja. Error del 2-oct-2026: A09.01 y A09.02 se quedaron sin
    cachear por eso, y son las dos hojas donde estaban los datums del parapeto.

    El title block vive abajo a la derecha, y ahi el numero de hoja va solo, en grande. Se
    toma el candidato mas cercano a esa esquina; el conteo solo desempata.
    """
    cand = [w for w in ws if HOJA.match(w['text'].strip())]
    if not cand:
        return None
    x0, y0 = ancho * 0.78, alto * 0.80          # cuadrante del title block
    tb = [w for w in cand if w['x0'] >= x0 and w['top'] >= y0]
    if tb:
        tb.sort(key=lambda w: -(w['x0'] + w['top']))     # el mas abajo-derecha
        return tb[0]['text'].strip()
    c = collections.Counter(w['text'].strip() for w in cand)
    return c.most_common(1)[0][0]


def rotulo_de_pagina(pdf, idx):
    pg = pdf.pages[idx]
    return rotulo_de(pg.extract_words() or [], pg.width, pg.height)


CACHE = f'{_TW}/detalles_cache.json'


def verificar(pdf_path=PDF, solo=None):
    """Lee el CACHE, no el PDF: barrer 94 hojas tarda minutos y una compuerta que tarda
    minutos no se corre. cache_detalles.py lo llena una vez por proyecto."""
    cit = citados()
    objetivo = set(solo) if solo else set(cit)          # hojas que el take-off usa
    universo = collections.defaultdict(set)
    if not os.path.exists(CACHE):
        raise DetalleSinAbrir('falta el cache de detalles: corre cache_detalles.py')
    d = json.load(open(CACHE, encoding='utf-8'))
    cacheadas = {pg.get('rotulo') for pg in d['paginas'].values() if pg.get('rotulo')}
    for _i, pg in d['paginas'].items():
        rot = pg.get('rotulo')
        if rot not in objetivo:
            continue
        universo[rot] |= set(pg.get('burbujas', {}).get(rot, []))

    # UNA HOJA CITADA QUE NO ESTA EN EL CACHE NO SE PUEDE DAR POR CUBIERTA.
    # Error real del 2-oct-2026: el cierre del exterior citaba A09.21, A09.22, A09.23,
    # A09.26 y S5.10/S5.20, ninguna estaba cacheada, y la compuerta las dejo caer en
    # SILENCIO -- informaba "73 detalles, 20 pendientes" sin haber mirado las hojas donde
    # estaban el T/ STUD LP <n>, el T.O. PARAPET 2 = 20'-0" y el PARAPET INFILL FRAMING.
    # Una compuerta que ignora lo que no cacheo no es una compuerta: es un espejo de lo que
    # ya miraste. Ahora revienta y dice cuales faltan.
    sin_cache = sorted(objetivo - cacheadas)
    if sin_cache:
        raise DetalleSinAbrir(
            'el take-off cita %d hoja(s) que NO estan en el cache de detalles, asi que la '
            'compuerta no puede saber que detalles tienen: %s. Corre cache_detalles.py con '
            'esas hojas antes de entregar.' % (len(sin_cache), ', '.join(sin_cache)))
    faltan = []
    for h in sorted(universo):
        sin = sorted(universo[h] - cit.get(h, set()) - _declarados(h))
        if sin:
            faltan.append((h, sin, sorted(cit.get(h, set()))))
    return faltan, universo, cit


def exigir(pdf_path=PDF):
    f, _, _ = verificar(pdf_path)
    if f:
        raise DetalleSinAbrir(
            'HAY DETALLES SIN ABRIR en hojas que el take-off usa:\n  - ' +
            '\n  - '.join('%s: %s' % (h, ', '.join(str(x) for x in s)) for h, s, _ in f))
    return True


if __name__ == '__main__':
    faltan, uni, cit = verificar()
    print('hojas que el take-off cita como fuente: %d' % len(cit))
    print('%-10s %-28s %s' % ('HOJA', 'DETALLES SIN ABRIR', 'ya citados'))
    print('-' * 86)
    tot = 0
    for h, sin, ya in faltan:
        tot += len(sin)
        print('%-10s %-28s %s' % (h, ', '.join(str(x) for x in sin)[:28],
                                  ', '.join(str(x) for x in ya)[:40]))
    print('-' * 86)
    print('TOTAL sin abrir: %d' % tot)
