# -*- coding: utf-8 -*-
"""cadena_detalles.py -- ordena las citas de un cierre en la CADENA que se recorrio.

SUPER REGLA INVIOLABLE de Rodolfo, 4-oct-2026, textual:

    "desde este momento asi sera la secuencia: 1.- se hace primero el first floor plan, una
     vez terminado se continua con la secuencia de los detalles tal como lo hiciste en este
     momento, y seguir la secuencia hasta obtener el total de la cantidad de material que
     estamos cuantificando. Y una vez teniendo los resultados, en el excel sheet SIEMPRE
     anotar toda la secuencia de detalles que se cuantifico."

Lo repitio igual para el REFLECTED CEILING PLAN. O sea: dos puertas de entrada, una por
familia de elemento, y de ahi la cadena hasta el total.

Este modulo resuelve el paso 4 -- que la secuencia quede ESCRITA en el Excel, en el orden en
que se recorrio y no en orden alfabetico, para que el estimador abra las imagenes en el mismo
orden en que se leyeron.

COMO SE DERIVA EL ORDEN, sin teclearlo a mano:
  1. Se arma el GRAFO de burbujas del set: que hoja dibuja una burbuja hacia que hoja.
     Sale de `detalles_cache.json`, que ya lo tiene barrido hoja por hoja.
  2. La PROFUNDIDAD de cada hoja es su distancia (BFS) desde las hojas de PLANTA.
     Floor plan y roof plan y RCP = nivel 0. Una seccion que la planta senala = nivel 1.
     El detalle que esa seccion llama = nivel 2. Y asi.
  3. Los SCHEDULES (S5.20, A12.01, A00.30...) van SIEMPRE al final aunque el grafo les de
     poca profundidad: no son un eslabon de la cadena, son la tabla donde se mira el perfil
     despues de saber que elemento es. El canopy 84 lo muestra: 7/A09.26 no rotula spacing,
     asi que el ultimo eslabon real es 7/S5.20 y ahi termina.
  4. Dentro de un mismo nivel se ordena por hoja y por etiqueta, para que dos runs del
     generador den exactamente la misma cadena.

No inventa eslabones: solo ORDENA los que el cierre ya cita. Si un cierre cita poco, la
cadena sale corta -- y eso es justamente lo que hay que ver.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (antes fijas en /home/claude/boa)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", "/home/claude/boa")
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import json, os, re, sys, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

CACHE = f'{_TW}/detalles_cache.json'
# OJO CON EL FALSO POSITIVO (corregido 4-oct-2026): escribir DOS numeros de hoja separados
# por barra -- "la leyenda de A09.01/A09.02", "A02.01 / M01.01", "sheet note D de
# A12.04/A12.05" -- hace que el patron lea la COLA del primer numero de hoja como si fuera
# una etiqueta de detalle: `01/A09.02`, `04/A12.05`. Son detalles que NO EXISTEN, y acababan
# impresos en la cadena del Excel mandando al estimador a buscar una imagen que no esta.
# 75 apariciones de `01/A09.02` solo en BofA. Defensa doble: (1) si justo antes de la
# etiqueta hay cola de numero de hoja, se descarta; (2) ninguna etiqueta real lleva CERO A
# LA IZQUIERDA -- un detalle es 1, 11, D; nunca 01.
CITA = re.compile(r'([A-Z]{1,2}\d{1,2}\.)?\b([0-9]{1,2}|[A-Z])\s*/\s*([A-Z]{1,2}\d{1,2}\.\d{2})\b')
_CERO = re.compile(r'^0\d$')
# Rotulo de hoja citado SIN vineta de detalle delante (no precedido de "N/").
SOLO_HOJA = re.compile(r'(?<![/\w.])([A-Z]{1,2}\d{1,2}\.\d{2})\b')


def _citas(txt):
    """[(etiqueta, hoja)] validas: sin cola de hoja delante y sin cero a la izquierda."""
    return [(n, h) for cola, n, h in CITA.findall(txt) if not cola and not _CERO.match(n)]
HOJA = re.compile(r'^([A-Z]{1,2})(\d{1,2})\.(\d{2})$')

# Hojas de PLANTA: las dos puertas de entrada que Rodolfo fijo, mas los planos que son
# planta de pleno derecho (roof plan, plantas ampliadas).
PLANTAS = ('A2.01', 'A2.02', 'A4.01', 'A8.01', 'A8.11', 'A12.10')
# Schedules y tablas: el ultimo eslabon, nunca un paso intermedio.
SCHEDULES = ('S5.20', 'S5.21', 'A0.30', 'A0.21', 'A0.40')

# Nivel de reserva por SERIE, para la hoja a la que el grafo de burbujas no llega.
# No todo enlace del set es una burbuja: la planta remite a las elevaciones interiores por el
# ROMBO (otro simbolo) y al Partition Schedule por el TAG del muro. Sin este respaldo esas
# hojas caen al fondo y la cadena sale ordenada alfabeticamente, que es justo lo que la regla
# prohibe. Se evalua de prefijo mas largo a mas corto: 'A12.01' le gana a 'A12.'.
NIVEL_SERIE = (
    ('A12.01', 1),                                    # Partition Types: se llega por el TAG
    ('A2.', 0), ('A3.', 0), ('A4.', 0), ('A8.0', 0), ('A8.1', 0), ('S2.', 0),   # plantas
    ('A9.0', 1), ('A11.', 1),                         # elevaciones exteriores e interiores
    ('A9.2', 2), ('A9.3', 2), ('A12.', 2), ('A0.', 2),            # secciones y detalles
    ('S3.', 1), ('S5.', 1),                                       # detalles estructurales
    ('M', 3), ('P', 3), ('E', 3),                                 # cruce MEP, al final
)


def nivel_serie(h):
    """Nivel de reserva por serie de hoja. None si la serie no esta contemplada."""
    for pre, niv in sorted(NIVEL_SERIE, key=lambda x: -len(x[0])):
        if h.startswith(pre):
            return niv
    return None


def norm(h):
    """Forma CANONICA, solo para comparar: A09.22 -> A9.22.

    Se QUITA el cero, nunca se agrega: rellenar a dos digitos convertiria S5.20 en S05.20,
    una hoja que no existe. OJO: esta forma es INTERNA. Para ESCRIBIR se usa `real()`.
    """
    m = HOJA.match((h or '').strip())
    return '%s%d.%s' % (m.group(1), int(m.group(2)), m.group(3)) if m else (h or '').strip()


_ROTULOS = None


def rotulos(cache=CACHE):
    """{forma canonica: rotulo REAL del title block}. A4.01 -> A04.01, S5.10 -> S5.10."""
    global _ROTULOS
    if _ROTULOS is None:
        d = json.load(open(cache, encoding='utf-8'))
        _ROTULOS = {}
        for pg in d['paginas'].values():
            r = (pg.get('rotulo') or '').strip()
            if r:
                _ROTULOS[norm(r)] = r
    return _ROTULOS


def real(h):
    """El numero de hoja TAL COMO ESTA IMPRESO en el title block.

    CORREGIDO 4-oct-2026, Rodolfo: "no existe la A4.01". Tenia razon. La forma canonica
    quita el cero para poder comparar `A09.22` con `A9.22`, pero ESCRIBIR esa forma manda al
    estimador a buscar una hoja que no existe: en este set las series A, E, M y P se imprimen
    con DOS digitos (`A04.01`, `M01.01`) y solo la serie S va con uno (`S5.10`). El rotulo de
    display no se deduce con una regla: se LEE del title block de cada hoja.
    """
    return rotulos().get(norm(h), (h or '').strip())


GRAFO = f'{_TW}/grafo_callouts.json'


def grafo(cache=CACHE, rehacer=False):
    """{hoja: set(hojas que senala)} con los rotulos ya normalizados.

    Se barre con el MISMO detector de burbujas de la compuerta (`verif_callouts`), hoja por
    hoja, no con el campo `burbujas` de `detalles_cache.json`.

    POR QUE: ese campo solo trae lo que el cacheador guardo cuando se construyo, y venia
    INCOMPLETO justo donde mas duele -- A2.01 aparecia senalando A9.02 y A9.25 pero no
    A9.21/A9.22/A9.23, y A4.01 no aparecia senalando NADA cuando dibuja ocho burbujas de
    seccion (A, B, C/A09.21 · D, E, F/A09.22 · H, J/A09.23). Con ese grafo, la cadena del
    wall exterior empezaba por el detalle en vez de por el plano. Un grafo incompleto no da
    error: da una cadena mas corta y plausible.
    """
    if not rehacer and os.path.exists(GRAFO):
        d = json.load(open(GRAFO, encoding='utf-8'))
        return collections.defaultdict(set, {k: set(v) for k, v in d.items()})
    import cache_detalles as C
    import verif_callouts as V
    idx = json.load(open(cache, encoding='utf-8'))['paginas']
    g = collections.defaultdict(set)
    for k, pg in sorted(idx.items(), key=lambda x: int(x[0])):
        rot = norm(pg.get('rotulo'))
        if not rot:
            continue
        try:
            ws = C.palabras_rapidas(int(k))
        except Exception:
            continue
        for _et, dest in V.burbujas_de_planta(ws):
            dn = norm(dest)
            if dn and dn != rot:
                g[rot].add(dn)
    json.dump({k: sorted(v) for k, v in g.items()}, open(GRAFO, 'w'), indent=1)
    return g


def profundidad(g=None):
    """BFS desde las hojas de planta. La que no alcanza el BFS queda al fondo."""
    g = g if g is not None else grafo()
    prof, cola = {}, collections.deque()
    for p in PLANTAS:
        prof[p] = 0
        cola.append(p)
    while cola:
        h = cola.popleft()
        for dest in sorted(g.get(h, ())):
            if dest not in prof:
                prof[dest] = prof[h] + 1
                cola.append(dest)
    for h in set(list(g) + [d for v in g.values() for d in v]):
        ns = nivel_serie(h)
        prof.setdefault(h, ns if ns is not None else 90)
    return prof


def citas_de(obj):
    """Todas las citas N/HOJA que hay dentro de un cierre, sin repetir."""
    txt = obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False)
    return {(n, norm(h)) for n, h in _citas(txt)}


def cadena(obj, entrada=None, prof=None, g=None):
    """Las citas ORDENADAS por la cadena: planta -> seccion -> detalle -> MEP -> schedule.

    `entrada` es la hoja de PLANTA por la que se entro (A02.01 para walls y aberturas,
    A04.01 para ceilings, soffits y marquesinas). Va SIEMPRE primero, porque el paso 1 de la
    regla es el plano, y el plano no se cita como `N/HOJA`: se cita como hoja.
    """
    prof = prof if prof is not None else profundidad(g)
    FONDO = 90

    def orden_hoja(h):
        # OJO: ordenar hojas como texto pone "A12.01" ANTES que "A9.02", porque "1" < "9".
        # La hoja se ordena por (serie, numero, subnumero), nunca por su cadena.
        m = HOJA.match(h)
        return (m.group(1), int(m.group(2)), int(m.group(3))) if m else (h, 0, 0)

    def clave(c):
        n, h = c
        niv = 99 if h in SCHEDULES else prof.get(h, nivel_serie(h))
        if niv is None:
            niv = FONDO
        et = (0, int(n)) if n.isdigit() else (1, n)
        return (niv, orden_hoja(h), et)

    out = ['%s/%s' % (n, real(h)) for n, h in sorted(citas_de(obj), key=clave)]

    # HOJAS CITADAS SIN NUMERO DE DETALLE (agregado 5-oct-2026, verificando el muro A1 #8).
    # Una fuente puede ser la HOJA ENTERA y no un detalle: la altura de stud sale del B.O.D.
    # de S2.20, que es un marcador de elevacion sin vineta, y la altura de board sale del tag
    # de cielo de A04.01, que tampoco es un detalle. La secuencia las omitia y el renglon del
    # Excel mentia por omision: decia de donde salio el material pero no de donde salio la
    # altura. Se insertan en su nivel de la cadena, escritas como hoja suelta.
    txt = json.dumps(obj, ensure_ascii=False) if not isinstance(obj, str) else obj
    ya = {c.split('/')[-1] for c in out}
    sueltas = []
    for h in sorted(set(SOLO_HOJA.findall(txt)), key=orden_hoja):
        hr = real(h)
        if hr in ya or (entrada and hr == real(entrada)):
            continue
        # OJO con el cero: `x or FONDO` manda al fondo todo lo de NIVEL 0, que es justo el
        # nivel de las hojas de PLANTA (A04.01, S2.20). Hay que comparar contra None.
        niv = prof.get(norm(h))
        if niv is None:
            niv = nivel_serie(norm(h))
        sueltas.append((FONDO if niv is None else niv, orden_hoja(hr), hr))
    if sueltas:
        for niv, oh, hr in sorted(sueltas):
            # se mete delante de la primera cita cuyo nivel sea mayor
            pos = len(out)
            for i, c in enumerate(out):
                hc = c.split('/')[-1]
                nc = prof.get(norm(hc))
                if nc is None:
                    nc = nivel_serie(norm(hc))
                if (FONDO if nc is None else nc) > niv:
                    pos = i
                    break
            out.insert(pos, hr)

    if entrada:
        er = real(entrada)
        if not any(c.endswith('/' + er) for c in out):
            out.insert(0, er)
    return out


def texto(obj, entrada=None, prof=None, g=None, sep=' \u2192 ', exigir=True):
    """La cadena lista para escribir en una celda del Excel.

    `exigir=True` (lo normal): RECHAZA la cadena si algun eslabon no trae motivo declarado en
    `motivos_cadena.CONTENIDO` ni dato rastreable en el propio cierre.

    ORDEN DE RODOLFO (6-oct-2026): "cada eslabon de la secuencia se escribe como N/HOJA --
    motivo -- dato extraido, y cadena_detalles debe RECHAZAR un eslabon sin motivo y sin
    dato/no-aplica". Se levanta excepcion aqui, en el punto donde la cadena se vuelve texto
    del Excel, para que un eslabon injustificado no pueda llegar a una celda: la columna
    `Detail sequence` crecia y el libro PARECIA mejor documentado cuando en realidad quedaba
    menos auditable.
    """
    c = cadena(obj, entrada, prof, g)
    if exigir and c:
        import motivos_cadena as MC
        cs = MC.campos(obj)
        malos = []
        for e in c:
            m = (MC.CONTENIDO.get(e) or '').strip()
            if len(m) < MC.MIN_MOTIVO:
                malos.append('%s (sin motivo declarado)' % e)
            elif not MC.rastro(obj, e, cs):
                malos.append('%s (ningun campo del cierre lo cita)' % e)
        if malos:
            raise AssertionError(
                'cadena RECHAZADA: %s. Declarar el motivo en motivos_cadena.CONTENIDO o '
                'sacar el eslabon de la cadena.' % '; '.join(malos))
    return sep.join(c) if c else ''


if __name__ == '__main__':
    import resumen_global as RG
    g = grafo(); prof = profundidad(g)
    print('hojas en el grafo: %d · con profundidad: %d' % (len(g), len(prof)))
    for h in sorted(prof, key=lambda x: (prof[x], x)):
        print('   nivel %d  %s' % (prof[h], h))
    print()
    for t, ws in RG.cargar().items():
        for w in ws:
            print('#%-4s %-12s %s' % (w.get('muro'), w.get('tag'), texto(w, 'A02.01', prof, g)))
