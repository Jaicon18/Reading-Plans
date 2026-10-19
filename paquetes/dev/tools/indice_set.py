# -*- coding: utf-8 -*-
"""indice_set.py -- EL INDICE COMPLETO DEL BID SET, leido del propio PDF.

PASO 0 del protocolo, hecho con las DOS fuentes que manda el protocolo y cotejando una
contra la otra:
  1. el DRAWING INDEX de A00.00 -- la lista oficial de hojas del set;
  2. el TITLE BLOCK de cada pagina -- el rotulo real, que puede no coincidir con el indice.

Por que las dos: el protocolo dice "verifica el rotulo real en el title block de cada pagina
(el indice puede estar desfasado)" y tambien "nunca declares una hoja faltante sin haber
barrido TODO el PDF por rotulo". Ninguna de las dos fuentes sola alcanza:
  - el indice trae hojas que el set puede no incluir (las civiles C*, por ejemplo);
  - el lector de title block se equivoca donde el rotulo tiene otra forma: leyo la misma hoja en
    varias paginas seguidas y en A03.01 tomo texto de la PLANTA como titulo.
Asi que el indice manda para el TITULO y el title block manda para QUE PAGINA del PDF es, y
donde se contradicen el handoff lo DICE en vez de elegir.

El indice de A00.00 esta en COLUMNAS. Reconstruir por renglon completo mezcla la columna de
consultores y la de revisiones con el titulo ("<hoja> WALL SECTIONS Tel: <telefono>").
La columna vecina empieza en X_FIN_TITULO, asi que el titulo se corta ahi.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (por defecto, el directorio actual)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", _os_rutas.getcwd())
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import os, sys, re, pickle, json, collections

B = f'{_TW}'
WORDS = B + '/.words_titleblock.pkl'
MAPA = B + '/.mapa_hojas.pkl'
PAG_INDICE = 1                   # page_index de A00.00
X_NUM = (2350, 2390)             # columna de los numeros de hoja del indice
X_FIN_TITULO = 2754              # donde empieza la columna de consultores/revisiones

RE_HOJA = re.compile(r'^([A-Z]{1,2}\d{2}\.\d{2}|[A-Z]\d\.\d{1,2})$')
RE_REV = re.compile(r'^(IF\s+.+?)\s+(\d{2}/\d{2}/\d{4})$')


def _words(i):
    DW = pickle.load(open(WORDS, 'rb'))
    return [x for x in DW if x['i'] == i][0]['ws']


def indice():
    """[(hoja, titulo)] del DRAWING INDEX de A00.00, en el orden impreso."""
    ws = _words(PAG_INDICE)
    nums = [w for w in ws if RE_HOJA.match(w['text']) and X_NUM[0] <= w['x0'] <= X_NUM[1]]
    nums.sort(key=lambda w: w['top'])
    out = []
    for w in nums:
        yc = (w['top'] + w['bottom']) / 2
        t = [x for x in ws if w['x1'] < x['x0'] < X_FIN_TITULO
             and abs((x['top'] + x['bottom']) / 2 - yc) <= 5]
        t.sort(key=lambda x: x['x0'])
        out.append((w['text'], ' '.join(x['text'] for x in t).strip()))
    return out


def revisiones():
    """[(descripcion, fecha)] del REVISION LOG de A00.00, en el orden impreso.

    Es el dato que contesta "revision/fecha" del handoff. La ULTIMA es la vigente.
    """
    ws = _words(PAG_INDICE)
    filas = collections.defaultdict(list)
    for w in ws:
        if w['x0'] >= X_FIN_TITULO - 4:
            filas[round(((w['top'] + w['bottom']) / 2) / 4)].append((w['x0'], w['text']))
    out = []
    for k in sorted(filas):
        t = ' '.join(z[1] for z in sorted(filas[k])).strip()
        m = RE_REV.match(t)
        if m:
            out.append((m.group(1).strip(), m.group(2)))
    return out


def paginas():
    """[(page_index, hoja_leida_del_title_block, titulo_leido)] de todas las paginas."""
    f = pickle.load(open(MAPA, 'rb'))
    return [(x['page_index'], x['hoja'], x['titulo']) for x in f]


def cotejo():
    """El indice y las paginas, cruzados, diciendo lo que NO cuadra.

    Devuelve (filas, avisos). Cada fila: hoja, titulo del indice, pagina(s) del PDF donde el
    title block la rotula, y el estado del cruce.
    """
    idx = indice()
    pag = paginas()
    donde = collections.defaultdict(list)
    for i, h, t in pag:
        if h:
            donde[h].append(i)
    filas, avisos = [], []
    for h, t in idx:
        ps = donde.get(h, [])
        if len(ps) == 1:
            estado = 'CONFIRMADO'
        elif not ps:
            estado = 'PENDIENTE'
            avisos.append('%s esta en el Drawing Index pero NINGUNA pagina la rotula en su '
                          'title block con el lector automatico; hay que abrirla a ojo antes '
                          'de declararla faltante' % h)
        else:
            estado = 'PENDIENTE'
            avisos.append('%s sale rotulada en %d paginas (%s): el lector de title block se '
                          'equivoco en al menos una; hay que abrirlas a ojo'
                          % (h, len(ps), ', '.join(str(x + 1) for x in ps)))
        filas.append(dict(hoja=h, titulo=t, paginas=[p + 1 for p in ps], estado=estado))
    # paginas con rotulo que el indice NO lista, y paginas sin rotulo legible
    listadas = {h for h, _ in idx}
    for i, h, t in pag:
        if h and h not in listadas:
            avisos.append('la pagina %d se rotula %s y el Drawing Index no la lista' % (i + 1, h))
    sin = [i + 1 for i, h, t in pag if not h]
    if sin:
        avisos.append('%d paginas sin numero de hoja legible para el lector automatico '
                      '(paginas %s): son portada y hojas con otro formato de title block. '
                      'Quedan [PENDIENTE] de abrir a ojo; NO se declaran faltantes.'
                      % (len(sin), ', '.join(str(x) for x in sin)))
    return filas, avisos


# ---------------------------------------------------------------------------------------
# EL NUMERO DE HOJA DEL TITLE BLOCK ES EL TEXTO MAS GRANDE QUE TIENE SU FORMA (8-oct-2026).
# El detector de `arranque.py` dejo <n> paginas sin numero y leyo mal otras: en A03.01
# tomo texto de la PLANTA como titulo. El rotulo del title block se imprime a ~37 pt y nada
# mas en la hoja se le acerca, asi que ordenar por TAMANO DE LETRA lo resuelve sin depender
# de en que esquina este. Comprobado: con esta regla salen hojas M que el otro
# detector no leia.
RE_NUM_TB = re.compile(r'^([A-Z]{1,2}\d{2}\.\d{2}|[A-Z]\d\.\d{1,2})$')
SIZE_MIN = 20.0                  # el rotulo va a ~37 pt; las referencias internas a ~12


def numero_de_title_block(ws):
    """(hoja, tamano) leido del title block: el token MAS GRANDE con forma de numero de hoja."""
    c = [((w.get('size') or 0), w['text']) for w in ws if RE_NUM_TB.match(w['text'])]
    c = [x for x in c if x[0] >= SIZE_MIN]
    if not c:
        return None, 0.0
    c.sort(reverse=True)
    return c[0][1], round(c[0][0], 2)


def paginas_por_tamano():
    """[(page_index, hoja, tamano)] de todas las paginas, con el detector por tamano."""
    DW = pickle.load(open(WORDS, 'rb'))
    out = []
    for d in sorted(DW, key=lambda x: x['i']):
        h, sz = numero_de_title_block(d['ws'])
        out.append((d['i'], h, sz))
    return out


def reconciliar():
    """Cuadra las paginas del PDF contra las hojas del indice, y DICE con que las cuadra.

    Caso tipico: paginas = hojas del Drawing Index + copias extra de una hoja que el PDF trae
    repetida (verificadas una por una contra el PDF, no contra el cache). indice + extras =
    paginas: el set no le falta ninguna hoja del indice y no trae ninguna que el indice no liste.
    """
    idx = dict(indice())
    pag = paginas_por_tamano()
    donde = collections.defaultdict(list)
    for i, h, sz in pag:
        if h:
            donde[h].append(i + 1)
    sin = [i + 1 for i, h, sz in pag if not h]
    extra = {h: ps for h, ps in donde.items() if len(ps) > 1}
    falta = [h for h in idx if h not in donde]
    nolista = [h for h in donde if h not in idx]
    return dict(n_paginas=len(pag), n_indice=len(idx), donde=dict(donde), sin_numero=sin,
                duplicadas=extra, sin_pagina=falta, fuera_del_indice=nolista)


# LAS N PAGINAS SIN ROTULO LEGIBLE SON LAS N HOJAS CIVILES Y DE LANDSCAPE -- por CUENTA,
# no por lectura. El title block del consultor civil tiene otro formato y el lector no saca
# su numero. La asignacion es una DERIVACION y se entrega como tal:
#   N paginas sin rotulo y exactamente N hojas del indice sin pagina
#   (civiles C* y de landscape L*), en el MISMO orden del indice.
# No se declara CONFIRMADO porque nadie leyo esos title blocks. Lo que hace que la
# incertidumbre no cueste nada es otra cosa, y se dice: son hojas CIVILES y de LANDSCAPE,
# fuera de Div 05 y Div 09 por completo, asi que ninguna cantidad del take-off las cita.
# Si alguna vez hiciera falta una, se abre esa pagina y se lee -- no se usa esta cuenta.
def civiles_por_posicion():
    """[(pagina, hoja, titulo)] DERIVADO por posicion para las civiles y de landscape."""
    r = reconciliar()
    sin = r['sin_numero']
    falta = [h for h, _ in indice() if h in set(r['sin_pagina'])]   # en orden del indice
    if len(sin) != len(falta):
        return [], ('PENDIENTE: %d paginas sin rotulo contra %d hojas sin pagina -- la cuenta '
                    'no cuadra, asi que NO se asigna ninguna por posicion'
                    % (len(sin), len(falta)))
    tit = dict(indice())
    return ([(p, h, tit.get(h, '')) for p, h in zip(sin, falta)],
            'DERIVADO por posicion: %d paginas sin rotulo legible y %d hojas del Drawing '
            'Index sin pagina, en el mismo orden del indice. Son hojas civiles y de '
            'landscape (Div 02/31/32), fuera de Div 05 y Div 09: ninguna cantidad del '
            'take-off cita una de ellas.' % (len(sin), len(falta)))


if __name__ == '__main__':
    idx = indice()
    rev = revisiones()
    filas, avisos = cotejo()
    print('DRAWING INDEX de A00.00: %d hojas' % len(idx))
    print('paginas del PDF: %d' % len(paginas()))
    print()
    print('REVISION LOG:')
    for a, b in rev:
        print('   %-42s %s' % (a, b))
    print()
    ok = sum(1 for f in filas if f['estado'] == 'CONFIRMADO')
    print('cruce indice <-> title block: %d CONFIRMADO, %d PENDIENTE' % (ok, len(filas) - ok))
    for a in avisos:
        print('   - %s' % a)
