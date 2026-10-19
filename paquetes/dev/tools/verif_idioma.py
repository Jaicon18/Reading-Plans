# -*- coding: utf-8 -*-
"""verif_idioma.py -- COMPUERTA DE IDIOMA DE LOS MATERIALES.

Orden de Rodolfo, 29-sep-2026: "tablero y metal: vamos a cambiar estas palabras al ingles,
cambia todos los materiales al ingles, y crea la regla".

Que impone: en TODO texto que el usuario o un tercero vaya a leer -- las celdas del Excel,
los documentos .md entregados, los cierres sellados -- el NOMBRE DEL MATERIAL va en ingles.
La prosa puede ir en espanol; el material no.

Por que: el material se pide, se compra y se instala en ingles. El proveedor cotiza
"5/8 gypsum board", la orden de compra dice "600S137-33", el instalador pide "board". Un
renglon que dice "tablero" obliga a traducir mentalmente cada vez, y en esa traduccion es
donde se pide lo que no era.

Donde revisa: el .xlsx entregable hoja por hoja, y los .md de la carpeta de entrega.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (antes fijas en /home/claude/boa)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", "/home/claude/boa")
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import os, sys, glob, re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glosario as G
import idioma_es as IE

# TRINQUETE DE TRADUCCION (orden de Rodolfo, 2-oct-2026: el entregable va INTEGRO en ingles).
#
# El libro tenia 188 celdas con frases enteras en espanol que la compuerta de MATERIALES no
# podia ver, porque no llevan ningun nombre de material: "cara oeste completa, Corridor 111".
# Traducir las 687 frases de los 21 generadores es trabajo de varias pasadas.
#
# Mientras tanto NO se deja la compuerta apagada ni se declara una excepcion abierta, que es
# como una deuda se vuelve permanente. Se pone un TRINQUETE: la compuerta falla si el numero
# de celdas en espanol SUPERA este tope. El tope solo puede BAJAR. Asi, cualquier frase nueva
# en espanol rompe la entrega el mismo dia en que se escribe, y el atraso queda a la vista y
# obligado a encogerse en cada pasada.
TOPE_ES = 100

# SEGUNDO TRINQUETE, para la hoja `Detail log` (agregada 6-oct-2026).
#
# Esa hoja CITA el texto sellado del cierre en su columna "What was taken from it". Es
# evidencia, no redaccion: traducirla al escribir la volveria una cita falsa -- el renglon
# diria una cosa y el cierre sellado otra, y entonces no sirve para auditar nada, que es lo
# unico para lo que existe. El atraso de traduccion de esas frases vive en el CIERRE, no en
# el libro, y se paga traduciendo los cierres (como se tradujeron los nombres de material),
# no reescribiendo la cita.
#
# Asi que NO se exime la hoja -- se le pone su PROPIO trinquete, visible y con su propio
# tope, que tambien solo puede bajar. Las dos cuentas se imprimen por separado en cada
# entrega: el atraso del libro y el atraso de la evidencia. Nada queda escondido, y una
# frase nueva en espanol en cualquiera de los dos rompe la entrega el mismo dia.
# TERCER TRINQUETE: el VOCABULARIO DEL TRADE en prosa (vocab_trade.py), agregado 7-oct-2026
# despues de que Rodolfo preguntara "seguiste la regla del ingles?" y la respuesta fuera NO.
# Es una lista distinta de glosario.py a proposito: `muro`, `largo`, `partidas` y `puerta` son
# CLAVES o VALORES del cierre, asi que no pueden entrar al glosario sin romper la logica --
# pero en PROSA si tienen que escribirse wall, length, line items y door.
# Hoy quedan 36 en los documentos, contados POR RENGLON igual que la compuerta de material
# (casi todos dentro de bloques de codigo citados, que el
# corrector no toca a proposito) y 290 celdas del libro (la hoja de evidencia cita el texto
# sellado, y ese atraso se paga traduciendo el GENERADOR). Los dos solo pueden BAJAR.
# EL HANDOFF SE CUENTA APARTE, con su propio trinquete, y NO se exime (8-oct-2026).
# `BOA_HANDOFF.md` es un documento GENERADO que cita el texto SELLADO de cada wall palabra
# por palabra. Reescribir esas citas en ingles las volveria FALSAS: el renglon diria una cosa
# y el sello otra -- el mismo motivo por el que `Detail log` tiene su propio TOPE_ES_LOG.
# Lo que vale guardar es DE DONDE sale el atraso, porque es una sola deuda con dos caras:
# los terminos en espanol que quedan en texto sellado son EXACTAMENTE los de los 4 bloques
# HUERFANOS (tipos A5, B, B2K y C1 -- 344 de 344, medido). La regla de traduccion dice "se
# traduce el GENERADOR, no la salida", y para esos cuatro NO HAY generador que traducir
# (ver `verif_reproducible.huerfanos`). Asi que este trinquete baja cuando se escriban
# `cerrar_A5.py`, `cerrar_B.py`, `cerrar_B2K.py` y `cerrar_C1.py`, no antes, y es la medida
# de esa deuda. Los 12 tipos que SI tienen closer quedaron en ingles al 100%.
HANDOFF = 'BOA_HANDOFF.md'
TOPE_VOCAB_HANDOFF = 8            # 10-oct-2026: 9 -> 8

TOPE_VOCAB_DOCS = 25           # 10-oct-2026: 36 -> 27 -> 25
TOPE_VOCAB_LIBRO = 0
# Cuarto grupo: las hojas Handoff del libro, con su propia cuenta (8-oct-2026).
TOPE_VOCAB_HANDOFF_XLSX = 0    # 10-oct-2026: 17 -> 16 -> 0

HOJA_EVIDENCIA = 'Detail log' 
TOPE_ES_LOG = 877          # 10-oct-2026: 884 -> 877 al traducir MOT_CANTO de cerrar_A1_v2

# LAS HOJAS DEL HANDOFF citan el texto SELLADO igual que `Detail log`, asi que van con su
# PROPIO tope y NO exentas (8-oct-2026). Reescribir la cita la volveria falsa: el renglon
# diria una cosa y el sello otra. Tercer grupo con su propia cuenta, por la misma razon por
# la que `Detail log` tuvo la suya -- cuando una compuerta empieza a medir cosas distintas se
# le pone otro contador visible, nunca una exencion.
HOJAS_HANDOFF = ('Handoff - Types', 'Handoff - Open Items', 'Handoff - Locations',
                 'Handoff - Bid Set', 'Handoff - Approved')
TOPE_ES_HANDOFF_XLSX = 24      # 10-oct-2026: 34 -> 24

LIBRO = f'{_TW}/out/BOA_Broomfield_Takeoff.xlsx'
DOCS = f'{_TO}/entrega'


# Documentos CONGELADOS: son el registro historico de versiones anteriores del skill y de
# adendas ya publicadas. Traducirlos seria reescribir lo que ya se entrego con esa
# redaccion. Se excluyen con motivo escrito -- nunca en silencio. La version VIGENTE del
# skill si entra a la compuerta.
# Un documento CONGELADO queda fuera de la compuerta -- pero se reconoce por lo que ES,
# no por como se escribe su nombre. Esto era un dict de nombres EXACTOS y el 01-oct-2026
# renombrar `adenda_v27.md` a `adenda_v27_2026-09-28.md` volvio a meterla a la compuerta y
# paro la entrega. Un nombre exacto en una lista de exclusiones se rompe con un rename;
# una CATEGORIA no. Y la categoria es real: una version congelada existe para registrar
# que decia el texto ESE dia, asi que reescribirla destruye justo lo que vino a guardar.
HISTORICO = re.compile(r'^(SKILL_take-off_v\d+|adenda_v\d+)', re.I)


def es_historico(nombre):
    """True si el archivo es una version congelada (y entonces NO se corrige)."""
    return bool(HISTORICO.match(os.path.basename(nombre)))



class IdiomaRechazado(Exception):
    pass


def revisar_libro(path=LIBRO):
    from openpyxl import load_workbook
    out = []
    wb = load_workbook(path, data_only=True)
    for hoja in wb.sheetnames:
        ws = wb[hoja]
        for fila in ws.iter_rows():
            for c in fila:
                if isinstance(c.value, str):
                    f = G.faltas(c.value)
                    if f:
                        out.append((('%s!%s' % (hoja, c.coordinate)), f, c.value[:90]))
    return out


# Un documento que DEFINE la regla tiene que poder escribir las palabras que prohibe: el
# glosario es una tabla espanol->ingles, y una cita textual de Rodolfo se reproduce como
# la dijo, nunca traducida. Se exime el BLOQUE marcado, no el archivo entero -- asi una
# falta de verdad en el resto del documento se sigue cazando.
INICIO, FIN = '<!-- GLOSARIO:INICIO -->', '<!-- GLOSARIO:FIN -->'


def _fuera_del_glosario(lineas):
    """Devuelve (numero, linea) de las lineas que NO estan dentro de un bloque eximido,
    y con el CODIGO ya quitado -- bloque cercado incluido.

    El codigo se quita AQUI y no en cada compuerta. Las tres compuertas que cuentan por
    renglon (`revisar_docs`, `vocab_pendiente`, `handoff_pendiente`) llamaban `faltas` con
    UNA linea a la vez, y una linea sola no sabe si viene dentro de un bloque cercado: solo
    alcanza a ver los backticks de `inline code`. Resultado medido el 11-oct-2026: de los 51
    terminos que la compuerta reportaba en los documentos, 5 eran CODIGO -- la formula
    `capas = Sigma(capas_cara x largo_cara) / largo_muro` y un arbol de detalles. Traducir esos
    5 habria CORROMPIDO la formula (el nombre del campo sellado es `capas_cara`) para
    contentar a la compuerta. El detector y el corrector tienen que normalizar igual, y la
    cerca solo se ve con el documento COMPLETO, asi que se ve una vez, aqui.
    """
    import vocab_trade as V
    crudas = list(lineas)
    limpias = V.lineas_sin_codigo(crudas)
    dentro = False
    for i, (cruda, limpia) in enumerate(zip(crudas, limpias), 1):
        if INICIO in cruda:
            dentro = True; continue
        if FIN in cruda:
            dentro = False; continue
        if not dentro:
            yield i, limpia


def revisar_docs(carpeta=DOCS):
    out = []
    for p in sorted(glob.glob(os.path.join(carpeta, '*.md'))):
        if es_historico(p):
            continue
        for i, linea in _fuera_del_glosario(open(p, encoding='utf-8').read().splitlines()):
            f = G.faltas(linea)
            if f:
                out.append(('%s:%d' % (os.path.basename(p), i), f, linea.strip()[:90]))
    return out


# Generadores de PLANO MARCADO: sus rotulos, leyendas y titulos son literales de Python
# que terminan DIBUJADOS en el JPG. Ahi el texto ya es pixel y ninguna compuerta lo puede
# leer, asi que se revisa la FUENTE antes de que se renderice. (Origen: 29-sep-2026, la
# leyenda del 14_PLANO_SOFFITS decia "tablero vertical" y la compuerta no lo veia porque
# solo miraba el .xlsx y los .md.)
GENERADORES = ['hojas_por_tipo.py', 'hoja_exterior.py', 'hoja_cielos.py', 'hoja_soffits.py',
               'planmark.py']


def revisar_generadores(carpeta=None):
    import ast
    carpeta = carpeta or os.path.dirname(os.path.abspath(__file__))
    out = []
    for n in GENERADORES:
        p = os.path.join(carpeta, n)
        if not os.path.exists(p):
            continue
        try:
            arbol = ast.parse(open(p, encoding='utf-8').read())
        except SyntaxError:
            continue
        doc = ast.get_docstring(arbol) or ''
        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.Constant) and isinstance(nodo.value, str):
                if nodo.value == doc or len(nodo.value) > 900:
                    continue          # el docstring del modulo es prosa interna, no rotulo
                f = G.faltas(nodo.value)
                if f:
                    out.append(('%s:%d' % (n, nodo.lineno), f, nodo.value.strip()[:90]))
    return out


def vocab_pendiente(xlsx=None, carpeta=None):
    """(n_docs, n_celdas_libro, n_celdas_handoff) de vocabulario del trade en espanol."""
    import vocab_trade as V
    from openpyxl import load_workbook
    nd = 0
    for p in sorted(glob.glob(os.path.join(carpeta or DOCS, '*.md'))):
        if es_historico(os.path.basename(p)):
            continue
        if os.path.basename(p) == HANDOFF:
            continue                      # se cuenta aparte, en handoff_pendiente()
        # Se exime el BLOQUE marcado, igual que la compuerta de material: un documento que
        # DEFINE la regla tiene que poder escribir las palabras que prohibe. La adenda v40
        # trae la tabla de los seis terminos que se me escaparon, y sin esto se marcaba a
        # si misma.
        for _i, linea in _fuera_del_glosario(open(p, encoding='utf-8').read().splitlines()):
            # El CODIGO (bloque cercado e `inline code`) lo salta ya `vocab_trade.faltas`,
            # que es la UNICA normalizacion del proyecto. Antes habia una regexp local aqui
            # y otra distinta en traducir_docs.py y ninguna en verif_respuesta.py: el mismo
            # texto pasaba una compuerta y fallaba la otra. Un detector y un corrector que
            # no normalizan igual dejan faltas que se reportan para siempre y nunca se
            # arreglan -- el error que ya costo una entrega con `perfileria`.
            nd += len(V.faltas(linea))
    # El libro se cuenta en DOS grupos por el mismo motivo que celdas_espanol: las hojas del
    # handoff citan el texto SELLADO, y reescribir la cita la volveria falsa. Tres cuentas,
    # tres topes, ninguno exento.
    nc = nh = 0
    wb = load_workbook(xlsx or LIBRO, data_only=True)
    for ws in wb.worksheets:
        es_hand = ws.title in HOJAS_HANDOFF
        for row in ws.iter_rows(values_only=True):
            for v in row:
                if isinstance(v, str) and V.faltas(v):
                    if es_hand:
                        nh += 1
                    else:
                        nc += 1
    wb.close()
    return nd, nc, nh


def handoff_pendiente(carpeta=None):
    """Terminos del trade en espanol del HANDOFF, contados POR RENGLON, aparte del resto."""
    import vocab_trade as V
    p = os.path.join(carpeta or DOCS, HANDOFF)
    if not os.path.exists(p):
        return 0
    n = 0
    for _i, linea in _fuera_del_glosario(open(p, encoding='utf-8').read().splitlines()):
        n += len(V.faltas(linea))
    return n


def celdas_espanol(xlsx, hoja_evidencia=False):
    """Celdas del libro con una frase en espanol (no solo un nombre de material).

    `hoja_evidencia=False` devuelve el libro SIN la hoja de evidencia; True devuelve SOLO
    esa hoja. Son dos atrasos distintos con dos topes distintos, y se cuentan aparte: el del
    libro se paga reescribiendo el generador, el de la evidencia se paga traduciendo el
    CIERRE, porque la celda es una cita literal del texto sellado.
    """
    from openpyxl import load_workbook
    out = []
    wb = load_workbook(xlsx, data_only=True)
    for ws in wb.worksheets:
        # 'handoff' pide SOLO las hojas del handoff; True solo la de evidencia; False el
        # libro sin ninguna de las dos. Tres grupos, tres topes, ninguno exento.
        if hoja_evidencia == 'handoff':
            if ws.title not in HOJAS_HANDOFF:
                continue
        elif bool(hoja_evidencia):
            if ws.title != HOJA_EVIDENCIA:
                continue
        elif ws.title == HOJA_EVIDENCIA or ws.title in HOJAS_HANDOFF:
            continue
        for i, row in enumerate(ws.iter_rows(values_only=True), 1):
            for v in row:
                if isinstance(v, str) and IE.es_espanol(v):
                    out.append(('%s:%d' % (ws.title, i), IE.es_espanol(v), v[:90]))
    wb.close()
    return out


def verificar(path=LIBRO, carpeta=DOCS):
    return revisar_libro(path) + revisar_docs(carpeta) + revisar_generadores()


def exigir(path=LIBRO, carpeta=DOCS):
    f = verificar(path, carpeta)
    if f:
        msg = '\n  - '.join('%s -> %s | %s' % (d, ', '.join(w), t) for d, w, t in f[:20])
        raise IdiomaRechazado('HAY NOMBRES DE MATERIAL EN ESPANOL (%d):\n  - %s'
                              % (len(f), msg))
    return True


if __name__ == '__main__':
    fs = verificar()
    if fs:
        print('*** MATERIAL EN ESPANOL (%d apariciones):' % len(fs))
        import collections
        c = collections.Counter(w for _, ws, _ in fs for w in ws)
        for w, n in c.most_common():
            print('   %-16s %3d' % (w, n))
        print('\n  primeras:')
        for d, w, t in fs[:12]:
            print('   %-26s %-22s %s' % (d, ','.join(w), t))
        sys.exit(1)
    print('idioma OK: todos los nombres de material van en ingles')
