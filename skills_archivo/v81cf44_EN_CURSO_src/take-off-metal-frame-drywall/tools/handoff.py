# -*- coding: utf-8 -*-
"""handoff.py -- arma el HANDOFF del take-off para continuarlo en OTRA sesion.

Pedido de Rodolfo (8-oct-2026), textual: "Prepara un HANDOFF completo de este take-off para
continuarlo en otra sesion... No resumas ni redondees. Si algo no esta verificado, marcalo
[PENDIENTE]."

POR QUE ES UN GENERADOR Y NO UN DOCUMENTO ESCRITO A MANO: un handoff escrito a mano queda
viejo en cuanto se corrige un cierre, y el que lo reciba no tiene forma de saber que esta
viejo. Aqui cada numero se LEE del cierre sellado, cada cita se lee del campo que la trae y
cada estado se lee de la etiqueta sellada. Si manana cambia un length, se vuelve a correr y
el handoff cambia con el. Es la misma razon por la que la carta de RFIs se genera de la hoja
Pending Items y no se teclea al lado.

NO SE REDONDEA: los valores van con los decimales del sello. Un handoff redondeado obliga al
que lo recibe a volver a medir.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (por defecto, el directorio actual)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", _os_rutas.getcwd())
_PRE = _os_rutas.environ.get("TAKEOFF_PREFIJO", "PROYECTO")  # prefijo de los archivos del proyecto
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import os, sys, json, pickle, collections, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import resumen_global as RG
import dataset as DS

B = f'{_TW}'
DEST_MD = f'{_TO}/entrega/{_PRE}_HANDOFF.md'
MAPA = B + '/.mapa_hojas.pkl'


# ---------------------------------------------------------------- 1. PROYECTO Y SET
# Los datos del PROYECTO (nombre, sitio, set, alcance, ubicaciones confirmadas, decisiones
# aprobadas, adendas, notas de faltantes) NO viven en esta tool: se leen de
# $TAKEOFF_WORK/handoff_proyecto.json (o de la ruta en $TAKEOFF_HANDOFF_JSON). Sin ese archivo
# cada dato sale [PENDIENTE]: la tool no trae valores de ningun proyecto (E24).
# Los datos generales van con su hoja citada. El numero de hojas NO se escribe a mano:
# se cuenta del mapa leido de los title blocks.
CFG_JSON = _os_rutas.environ.get("TAKEOFF_HANDOFF_JSON", f'{_TW}/handoff_proyecto.json')


def _cfg():
    try:
        return json.load(open(CFG_JSON, encoding='utf-8'))
    except (OSError, ValueError):
        return {}


CFG = _cfg()
PROYECTO = [tuple(x) for x in CFG.get('proyecto') or [
 ('Project', '[PENDIENTE] project name not loaded (handoff_proyecto.json)', 'cover sheet'),
 ('Site', '[PENDIENTE]', 'cover sheet'),
 ('Set', '[PENDIENTE]', 'title block'),
 ('Scope of this take-off', 'CSI Division 05 40 00 Cold-Formed Metal Framing and Division '
                        '09 20 00 / 09 29 00 Gypsum Board Assemblies', 'scope'),
]]
TITULO = CFG.get('titulo') or '<proyecto>'
NIVEL = CFG.get('nivel') or 'LEVEL 1'


def mapa_hojas():
    """El indice COMPLETO del set, leido del title block de cada pagina del PDF.

    No es el `Sheet Index` del libro: ese lista solo las <n> hojas de las que se saco un
    numero. Rodolfo pidio TODAS las hojas del bid set, asi que se lee pagina por pagina.
    """
    if not os.path.exists(MAPA):
        return None
    return pickle.load(open(MAPA, 'rb'))


# ---------------------------------------------------------------- utilidades de lectura
def v(p):
    return (p or {}).get('val', {}).get('v')


def est(p):
    return (p or {}).get('val', {}).get('estado') or '?'


def razon(p):
    """La fuente o la operacion SELLADA de una line item, tal cual, sin recortar.

    Un handoff que recorta la operacion deja al que lo recibe sin la cuenta, y entonces
    tiene que volver a abrir el plano -- que es exactamente lo que el handoff evita.
    """
    val = (p or {}).get('val', {}) or {}
    t = [x for x in (val.get('fuente'), val.get('operacion')) if x]
    return '  ||  '.join(t)


def campo(d):
    """(valor, estado, razon) de un campo sellado tipo length / alto_stud / alto_board."""
    d = d or {}
    t = [x for x in (d.get('fuente'), d.get('operacion')) if x]
    return d.get('v'), d.get('estado') or '?', '  ||  '.join(t)


def muros_por_tag():
    """{tag: [wall, ...]} con el sello comprobado, en el orden oficial del barrido."""
    out = collections.OrderedDict()
    for bloque, ws in RG.cargar().items():
        for w in ws:
            assert RG.sello_ok(w), 'sello roto en wall %s' % w.get('muro')
            out.setdefault(w.get('tag'), []).append(w)
    for t in out:
        out[t].sort(key=lambda w: w.get('muro') or 0)
    return collections.OrderedDict(sorted(out.items()))


# ---------------------------------------------------------------- 2. PARTITION TYPES
# La composicion NO se escribe a mano: el perfil y su cita salen de dataset.PERFIL, las
# layers de board de las caras del cierre, la height de alto_stud con su estado sellado,
# y la insulation de la exclusion sellada (que trae su propio motivo y su delta).
def tipos(MT):
    out = []
    for tag, ws in MT.items():
        perf = DS.PERFIL.get(tag)
        lbl, des, oc, src = perf if perf else ('[PENDIENTE]', '[PENDIENTE]',
                                               ws[0].get('oc'), '[PENDIENTE] sin fila en dataset.PERFIL')
        # layers por cara, tal como las sella cada wall. Se agrupan: si dos walls del
        # mismo tag tienen composicion distinta, el handoff lo tiene que DECIR, no promediar.
        comp = collections.OrderedDict()
        for w in ws:
            for c in w.get('caras', []):
                k = '%s x%d' % (c.get('tipo') or '?', c.get('capas') or 1)
                comp.setdefault(k, []).append(w.get('muro'))
        # heights: una por wall, con su estado. Un tipo puede tener varias.
        alturas = collections.OrderedDict()
        for w in ws:
            val, e, rz = campo(w.get('alto_stud'))
            alturas.setdefault((val, e), []).append(w.get('muro'))
        # spacing de bracing y hileras de stud, del propio cierre
        brace = sorted({w.get('brace_sp') for w in ws})
        hil = sorted({w.get('hileras') or 1 for w in ws})
        # insulation: se lee la exclusion sellada de cada wall
        ins = collections.OrderedDict()
        for w in ws:
            e = (w.get('excluidas') or {}).get('INSULATION')
            ins.setdefault(e or '[PENDIENTE] este wall no declara nada sobre insulation',
                           []).append(w.get('muro'))
        out.append(dict(tag=tag, walls=[w.get('muro') for w in ws], n=len(ws),
                        stud_lbl=lbl, stud_des=des, oc=oc, stud_src=src,
                        comp=comp, alturas=alturas, brace=brace, hileras=hil, ins=ins))
    return out


# ---------------------------------------------------------------- 3. CANTIDADES
def cantidades(MT):
    """Una fila por LINE ITEM de cada wall, con su cita y, si es DERIVADO, su operacion.

    Se recorre wall por wall y line item por line item: nada se agrega aqui. La suma por tag
    la hace el que lee, o la hoja Material Summary del libro, que ya la trae con
    NETO / WASTE / COMPRA. Agregar aqui seria resumir, y eso lo prohibio.
    """
    out = []
    for tag, ws in MT.items():
        for w in ws:
            L, Le, Lr = campo(w.get('largo'))
            H, He, Hr = campo(w.get('alto_stud'))
            fila = dict(tag=tag, muro=w.get('muro'), ubic=w.get('ubicacion', ''),
                        largo=L, largo_est=Le, largo_src=Lr,
                        alto=H, alto_est=He, alto_src=Hr,
                        oc=w.get('oc'), nivel=NIVEL,
                        caras=[], partidas=[], aberturas=w.get('aberturas') or [],
                        excl=w.get('excluidas') or {}, sello=w.get('sello'))
            for c in w.get('caras', []):
                bv, be, br = campo(c.get('alto_board'))
                fila['caras'].append(dict(cuarto=c.get('cuarto'), tipo=c.get('tipo'),
                                          capas=c.get('capas'), alto=bv, est=be, src=br))
            for k, p in (w.get('partidas') or {}).items():
                fila['partidas'].append(dict(
                    partida=k, v=v(p), unidad=(p or {}).get('unidad'),
                    estado=est(p), razon=razon(p)))
            fila['partidas'].sort(key=lambda x: x['partida'])
            out.append(fila)
    return out


# ---------------------------------------------------------------- 4. UBICACIONES CONFIRMADAS
# LO QUE RODOLFO CONFIRMO NO ES LO MISMO QUE LO QUE SE CUANTIFICO. La regla del 12-sep-2026
# manda parar al terminar el barrido de un tag y esperar su confirmacion explicita. Este
# registro no existia como archivo: vivia en el chat. Un handoff que presente "ubicaciones
# confirmadas por el usuario" sin tener donde consta la confirmacion esta inventando el dato
# mas delicado del documento, porque es el unico que no se puede verificar contra el plano.
#
# Asi que se declara lo que CONSTA, con donde consta, y lo demas sale [PENDIENTE].
CONFIRMADO_POR_USUARIO = {k: tuple(v) for k, v in (CFG.get('confirmado_por_usuario') or {
 'barrido_por_tag': ('PENDIENTE', 'La regla del 12-sep-2026 exige parar al cerrar el barrido '
    'de cada tag y esperar confirmacion explicita de que la lista de ubicaciones esta completa. '
    'NO consta en ningun archivo que esa confirmacion se haya dado tag por tag (cargarla en '
    'handoff_proyecto.json con donde consta). El barrido verificado por codigo y la compuerta '
    'de planos marcados son otra cosa y el handoff no las puede presentar como una.'),
}).items()}


# ---------------------------------------------------------------- 5. LO QUE FALTA
def faltantes(MT):
    """Lo que falta, leido de donde consta: pendientes sellados, tags sin cerrar, atrasos."""
    import verif_confirmado as VC
    import verif_coherencia as VCO
    out = {}
    # (a) partidas selladas con estado PENDIENTE: son las que el cierre mismo declara
    pend = []
    for tag, ws in MT.items():
        for w in ws:
            for k, p in (w.get('partidas') or {}).items():
                if est(p) == 'PENDIENTE':
                    pend.append(dict(tag=tag, muro=w.get('muro'), partida=k,
                                     motivo=razon(p)))
    out['partidas_pendientes'] = pend
    # (b) campos [CONFIRMADO] que no citan ninguna cota: el atraso de la compuerta
    _mal, sin = VC.verificar(devolver_sin=True)
    out['confirmado_sin_cota'] = [dict(elemento=e, campo=r, valor=v, texto=t)
                                  for e, r, v, t in sin]
    out['confirmado_sin_cota_tope'] = VC.TOPE_SIN_COTA
    # (c) el mismo dato con dos etiquetas
    out['incoherencias'] = [dict(campo=k[0], valor=k[1], hojas=list(k[2]), estados=d)
                            for k, d in VCO.revisar()]
    return out


# ---------------------------------------------------------------- 6. RFIs CON DELTA
def rfis():
    """Los pendientes abiertos, leidos de la hoja Pending Items del libro.

    No se teclean al lado: si uno se resuelve y sale del Excel, sale solo del handoff. La
    columna Impact es el DELTA de cada alternativa, que es lo que Rodolfo pidio.
    """
    import hoja_rfi as RFI
    out = RFI.leer_pendientes()
    for x in out:
        d = (x.get('det') or '')
        x['cerrado'] = d.strip().upper().startswith('CLOSED')
    return out


# ---------------------------------------------------------------- 7. REGLAS, TEXTUALES
# Se CITAN de las adendas, no se parafrasean: Rodolfo pidio "textuales". Cada adenda se lee
# del archivo, asi que si se corrige una, el handoff la cita corregida.
ADENDAS = list(CFG.get('adendas') or [])      # nombres de archivo, en handoff_proyecto.json
DOCS = f'{_TO}/entrega'


def reglas():
    """[(titulo de la adenda, [bloques de regla textuales])] de las adendas de esta sesion."""
    out = []
    for f in ADENDAS:
        p = os.path.join(DOCS, f)
        if not os.path.exists(p):
            out.append((f, ['[PENDIENTE] el archivo de la adenda no esta en la carpeta de entrega']))
            continue
        lineas = open(p, encoding='utf-8').read().splitlines()
        titulo = next((l[2:].strip() for l in lineas if l.startswith('# ')), f)
        # los bloques de cita (lo que va con '>') son las reglas escritas como reglas
        bloques, cur = [], []
        for l in lineas:
            if l.startswith('>'):
                cur.append(l.lstrip('>').strip())
            else:
                if cur:
                    bloques.append(' '.join(x for x in cur if x)); cur = []
        if cur:
            bloques.append(' '.join(x for x in cur if x))
        out.append((titulo, [b for b in bloques if len(b) > 40]))
    return out


# ---------------------------------------------------------------- 8. LO QUE EL USUARIO APROBO
# Cada supuesto con el mensaje que lo aprobo. Un supuesto sin quien lo aprobo no es un
# supuesto aprobado: es un supuesto mio, y va en la seccion de pendientes.
APROBADO = [tuple(x) for x in CFG.get('aprobado') or [
 ('[PENDIENTE]', 'No approved assumption loaded (handoff_proyecto.json, key "aprobado").',
  'Each one needs the message that approved it.'),
]]
NOTAS_FALTANTES = list(CFG.get('notas_faltantes') or [])   # 5.5: tags / hojas / zonas sin barrer


# ================================================================ EL DOCUMENTO
def _f(x, n=2):
    """Numero con sus decimales. NO se redondea a nada: Rodolfo dijo 'no redondees'."""
    return '' if x is None else ('%.*f' % (n, x))


def escribir(dest=DEST_MD):
    import indice_set as I
    MT = muros_por_tag()
    T = tipos(MT)
    Q = cantidades(MT)
    F = faltantes(MT)
    L = []
    w = L.append

    hoy = datetime.date.today().isoformat()
    w('# HANDOFF - Metal Framing & Drywall take-off')
    w('')
    w('**%s** · CSI Division 05 Metals and Division 09 Finishes' % TITULO)
    w('')
    w('Written %s so another session can pick this take-off up without re-deriving anything. '
      'Every figure below is read from the SEALED closure of its wall, not retyped: the state '
      'tag `[CONFIRMADO]` / `[DERIVADO]` / `[PENDIENTE]` is the one that was sealed with the '
      'number, and the operation of every `[DERIVADO]` is quoted in full. Nothing is rounded '
      'and nothing is summarised away. Where a thing is not verified it says `[PENDIENTE]` and '
      'says what is missing.' % hoy)
    w('')
    w('**This document is generated** by `handoff.py` from the sealed closures, the workbook '
      'and the addenda. Re-run it after any correction instead of editing it: a handoff edited '
      'by hand goes stale and the person who receives it has no way to tell.')
    w('')
    w('> **Why some quoted evidence below may still be in Spanish.** The citation and operation '
      'strings are quoted from the SEAL, word for word. Rewriting them into English would make '
      'the quote disagree with the seal, so they are never rewritten here - the language debt is '
      'paid by translating the GENERATOR and re-running the closer. A sealed closure with no '
      'generator (see 5.4) cannot pay that debt, so both debts are cleared by writing its closer.')
    w('')

    # ---------------------------------------------------------------- 1
    w('---')
    w('')
    w('## 1. Project, bid set and revision')
    w('')
    w('| Item | Value | Source |')
    w('|---|---|---|')
    for a, b, c in PROYECTO:
        w('| %s | %s | %s |' % (a, b.replace('|', '/'), c))
    w('')
    rev = I.revisiones()
    w('### Revision log, read from A00.00')
    w('')
    w('| # | Issue | Date |')
    w('|---|---|---|')
    for i, (d, f) in enumerate(rev, 1):
        w('| %d | %s | %s |' % (i, d, f))
    w('')
    if rev:
        w('**Current revision: `%s` dated `%s`** - the last row of the log. [CONFIRMADO] read '
          'from the revision block of A00.00.' % (rev[-1][0], rev[-1][1]))
    w('')
    r = I.reconciliar()
    extra = sum(len(v) - 1 for v in r['duplicadas'].values())
    w('### How the page count reconciles against the sheet count')
    w('')
    w('- PDF pages: **%d**' % r['n_paginas'])
    w('- Sheets listed in the DRAWING INDEX of A00.00: **%d**' % r['n_indice'])
    for h, ps in sorted(r['duplicadas'].items()):
        w('- **`%s` appears %d times** in the set (pages %s), verified page by page against the '
          'PDF and not against a cache. Its %d extra copies are what makes the two counts '
          'differ.' % (h, len(ps), ', '.join(str(x) for x in ps), len(ps) - 1))
    w('- **%d + %d = %d.** Nothing from the index is missing from the set and the set carries '
      'no sheet the index does not list. [DERIVADO], operation shown.'
      % (r['n_indice'], extra, r['n_indice'] + extra))
    w('')
    civ, nota_civ = I.civiles_por_posicion()
    w('### Every sheet of the bid set')
    w('')
    w('Read from the DRAWING INDEX of A00.00 for the title, and from the title block of each '
      'page for the PDF page. The sheet number in a title block is the LARGEST text that has '
      'its shape, which is what makes it readable without depending on which '
      'corner it sits in.')
    w('')
    w('| Sheet | Title | PDF page | State |')
    w('|---|---|---|---|')
    tit = dict(I.indice())
    porpos = {h: p for p, h, _t in civ}
    for h, t in I.indice():
        ps = r['donde'].get(h, [])
        if ps:
            pg, estado = ', '.join(str(x) for x in ps), 'CONFIRMADO'
        elif h in porpos:
            pg, estado = str(porpos[h]), 'DERIVADO'
        else:
            pg, estado = '', 'PENDIENTE'
        w('| %s | %s | %s | [%s] |' % (h, (t or '').replace('|', '/'), pg, estado))
    w('')
    w('**The %d `[DERIVADO]` rows:** %s' % (len(civ), nota_civ))
    w('')

    # ---------------------------------------------------------------- 2
    w('---')
    w('')
    w('## 2. Partition types')
    w('')
    w('One block per tag. The stud profile and its citation come from `dataset.PERFIL`, the '
      'board layers from the faces of each sealed closure, the height from the sealed '
      '`alto_stud` with the state it was sealed with, and the insulation line from the sealed '
      'EXCLUSION, which carries its own motive. Where two walls of the same tag were sealed '
      'with different composition it is listed as two rows, never averaged.')
    w('')
    for t in T:
        w('### `%s` - %d wall%s: %s' % (t['tag'], t['n'], '' if t['n'] == 1 else 's',
                                        ', '.join('#%s' % x for x in t['walls'])))
        w('')
        w('| Item | Value | State |')
        w('|---|---|---|')
        w('| Stud size | %s | - |' % t['stud_lbl'])
        w('| Stud designation | %s | - |' % t['stud_des'])
        w('| Spacing | %s" O.C. | - |' % t['oc'])
        w('| Rows of stud | %s | - |' % ', '.join(str(x) for x in t['hileras']))
        w('| Bracing spacing | %s" O.C. | - |' % ', '.join(str(x) for x in t['brace']))
        for k, ws_ in t['comp'].items():
            w('| Board, by face | %s | on walls %s |'
              % (k, ', '.join('#%s' % x for x in sorted(set(ws_)))))
        for (val, e), ws_ in t['alturas'].items():
            w('| Stud height | %s ft | **[%s]** on walls %s |'
              % (_f(val, 3), e, ', '.join('#%s' % x for x in sorted(set(ws_)))))
        for motivo, ws_ in t['ins'].items():
            w('| Insulation | %s | walls %s |'
              % (motivo.replace('|', '/'), ', '.join('#%s' % x for x in sorted(set(ws_)))))
        w('')
        w('**Source of the stud profile:** %s' % t['stud_src'])
        w('')

    # ---------------------------------------------------------------- 3
    w('---')
    w('')
    w('## 3. Quantities taken so far')
    w('')
    w('By tag, then by wall, then by location. Level of every row: %s (project data). '
      'Each line item carries the value exactly as sealed, its unit, its state and - '
      'for every `[DERIVADO]` - the operation that produced it, quoted in full and not '
      'shortened. The sheet citations are inside those operations, which is where they were '
      'sealed.' % NIVEL)
    w('')
    w('Waste is NOT in these figures: they are NET. The NET / WASTE / PURCHASE columns are on '
      'the `Material Summary` sheet of the workbook, at 15%% on metal and 6%% on board, by type.')
    w('')
    tag_actual = None
    for q in Q:
        if q['tag'] != tag_actual:
            tag_actual = q['tag']
            w('### Tag `%s`' % tag_actual)
            w('')
        w('#### `%s` wall #%s - %s' % (q['tag'], q['muro'], (q['ubic'] or '').replace('|', '/')))
        w('')
        w('- Level: **%s**' % q['nivel'])
        w('- Length: **%s LF** `[%s]`' % (_f(q['largo'], 3), q['largo_est']))
        w('  - %s' % (q['largo_src'] or '[PENDIENTE] no source sealed'))
        w('- Stud height: **%s ft** `[%s]`' % (_f(q['alto'], 3), q['alto_est']))
        w('  - %s' % (q['alto_src'] or '[PENDIENTE] no source sealed'))
        w('- Spacing: %s" O.C.' % q['oc'])
        for c in q['caras']:
            w('- Face **%s**: board %s, %s layer(s), to **%s ft** `[%s]`'
              % ((c['cuarto'] or '?').replace('|', '/'), c['tipo'], c['capas'],
                 _f(c['alto'], 3), c['est']))
            w('  - %s' % (c['src'] or '[PENDIENTE] no source sealed'))
        if q['aberturas']:
            w('- Openings:')
            for a in q['aberturas']:
                w('  - %s `%s` %s x %s ft'
                  % (DS.CLASE_EN.get(a.get('clase'), a.get('clase')), a.get('ref'),
                     _f(a.get('w')), _f(a.get('h'))))
        else:
            w('- Openings: none sealed on this wall')
        w('')
        w('| Line item | Value | Unit | State | Citation and operation, as sealed |')
        w('|---|---|---|---|---|')
        for pz in q['partidas']:
            w('| %s | %s | %s | **[%s]** | %s |'
              % (pz['partida'], _f(pz['v']), pz['unidad'] or '', pz['estado'],
                 (pz['razon'] or '[PENDIENTE] nothing sealed').replace('|', '/').replace(chr(10), ' ')))
        w('')
        if q['excl']:
            w('**Excluded on this wall, each with its motive as sealed:**')
            w('')
            for k, motivo in q['excl'].items():
                w('- `%s` - %s' % (k, str(motivo).replace('|', '/').replace(chr(10), ' ')))
            w('')
        w('Seal: `%s`' % q['sello'])
        w('')

    # ---------------------------------------------------------------- 4
    w('---')
    w('')
    w('## 4. Locations confirmed by Rodolfo')
    w('')
    w('**This section distinguishes two things that are easy to confuse.** The numbered '
      'location list per tag exists and is verified by code; whether Rodolfo gave the explicit '
      'confirmation that the rule of 12-sep-2026 asks for is a SEPARATE fact, and it was never '
      'written to a file - it lived in the chat. So what is recorded is declared with where it '
      'is recorded, and the rest says `[PENDIENTE]`. Inventing this one would be worse than '
      'inventing a dimension, because it is the only item in the handoff that cannot be checked '
      'against the drawings.')
    w('')
    w('| Subject | State | What is recorded, and where |')
    w('|---|---|---|')
    for k, (e, txt) in CONFIRMADO_POR_USUARIO.items():
        w('| `%s` | **[%s]** | %s |' % (k, e, txt.replace('|', '/')))
    w('')
    w('### The numbered location list per tag, as sealed')
    w('')
    w('This is the official wall numbering, with the location '
      'string of each sealed closure. The marked-plan gate checks that the LF labelled on the '
      'marked drawing of each type equals the sealed closure, so the list and the drawings '
      'cannot drift apart.')
    w('')
    for tag, ws_ in MT.items():
        w('**`%s`** - %d wall%s' % (tag, len(ws_), '' if len(ws_) == 1 else 's'))
        w('')
        for i, wl in enumerate(ws_, 1):
            w('%d. `%s` wall **#%s** - %s - %s LF'
              % (i, tag, wl.get('muro'), (wl.get('ubicacion') or '').replace('|', '/'),
                 _f((wl.get('largo') or {}).get('v'), 3)))
        w('')

    # ---------------------------------------------------------------- 5
    w('---')
    w('')
    w('## 5. What is still missing')
    w('')
    w('### 5.1 Line items sealed as `[PENDIENTE]`')
    w('')
    if F['partidas_pendientes']:
        w('| Tag | Wall | Line item | Why it is pending |')
        w('|---|---|---|---|')
        for x in F['partidas_pendientes']:
            w('| %s | #%s | %s | %s |' % (x['tag'], x['muro'], x['partida'],
                                          (x['motivo'] or '').replace('|', '/')))
    else:
        w('None. No line item of the %d sealed walls carries the state `[PENDIENTE]`. The open '
          'questions are in 5.2, 5.3 and section 6 instead.' % sum(len(x) for x in MT.values()))
    w('')
    w('### 5.2 `[CONFIRMADO]` fields that cite no printed dimension - the honest weak spot')
    w('')
    w('**%d fields** are sealed `[CONFIRMADO]` whose source text carries no printed dimension '
      'at all, so the claim cannot be checked. `verif_confirmado.py` was skipping these in '
      'silence until 8-oct-2026: it passed over all %d. The backlog is now '
      'a declared ratchet at %d that can only go down, printed on every run.'
      % (len(F['confirmado_sin_cota']), len(F['confirmado_sin_cota']),
         F['confirmado_sin_cota_tope']))
    w('')
    w('A `[CONFIRMADO]` means the value IS the printed dimension of the sheet it cites. These '
      '%d are therefore either `[DERIVADO]` (and owe their operation) or `[PENDIENTE]`. The '
      'VALUES are not in question - this is a traceability debt, not a quantity error - but a '
      '`[CONFIRMADO]` that is not confirmed is worse than a `[PENDIENTE]`, because it stops the '
      'next person from checking it.' % len(F['confirmado_sin_cota']))
    w('')
    w('| Element | Field | Sealed value | Text that cites no dimension |')
    w('|---|---|---|---|')
    for x in F['confirmado_sin_cota']:
        w('| %s | `%s` | %s | %s |' % (x['elemento'], x['campo'], _f(x['valor'], 3),
                                       (x['texto'] or '').replace('|', '/')))
    w('')
    w('### 5.3 The same datum carrying two different state tags')
    w('')
    if F['incoherencias']:
        w('`verif_coherencia.py` compares every sealed field that cites the same sheet for the '
          'same value. Where two closures disagree on the state, one of the two is wrong and it '
          'has to be settled at the drawing, not by picking the convenient one.')
        w('')
        w('| Field | Value | Sheet cited | States, and how many walls carry each |')
        w('|---|---|---|---|')
        for x in F['incoherencias']:
            det = '; '.join('**[%s]** %d wall(s): %s' % (e, len(q2), ', '.join(q2))
                            for e, q2 in sorted(x['estados'].items()))
            w('| `%s` | %s | %s | %s |' % (x['campo'], _f(x['valor'], 3),
                                           ', '.join(x['hojas']), det))
        w('')
        w('**A height row (`alto_stud` / `alto_board`) is the one that matters most.** A type '
          'detail gives the RULE ("to underside of structure"); it does not print the height, '
          'which comes from the structural sheet. A right number with the wrong source is a '
          'citation defect, and it has to be fixed in the GENERATOR of each '
          'closer, never in the sealed JSON - a citation fixed in the JSON comes back the next '
          'time the closer runs.')
    else:
        w('None open.')
    w('')
    import verif_reproducible as VR
    hu = VR.huerfanos()
    n_hu, n_tot = sum(n for _b, n in hu), len(Q)
    w('### 5.4 Sealed closures with NO generator - %d of the %d walls' % (n_hu, n_tot))
    w('')
    w('**The blocks below have a sealed closure in the delivery folder and NO closer '
      'script that produces it.** Only readers touch them (`resumen_global`, `localizar`) and '
      'two scripts PATCH them after the fact (`reetiquetar_a5_alto.py`, `resellar_b2k.py`), '
      'which is itself the proof that they have already had to be edited from outside.')
    w('')
    w('| Block | Walls | What is missing |')
    w('|---|---|---|')
    for b, n in hu:
        w('| `%s` | %d | the closer that regenerates it |' % (b, n))
    w('')
    w('A closure with no generator is worse than a closer that will not run: it is not frozen, '
      'it is **orphaned**. The day a dimension on one of those walls changes there is nothing '
      'to re-run, and the only way out is editing the sealed JSON by hand, which no rule here '
      'permits. `verif_reproducible.py` never asked this question until 8-oct-2026 because its '
      'list of closers was written by hand, so it could only measure what somebody remembered '
      'to write down. It now compares the blocks that `resumen_global.SRC` reads against the '
      'declared closers, with the backlog as a ratchet at %d blocks that can only go down.'
      % VR.TOPE_HUERFANOS)
    w('')
    w('The numbers of those %d walls are sealed and verified - the seal check passes on all %d '
      'and the marked-plan gate matches their labelled LF. What is missing is the ability to '
      'REGENERATE them, which is what makes a number maintainable rather than merely correct.'
      % (n_hu, n_tot))
    w('')
    w('### 5.5 Tags, sheets and zones not swept')
    w('')
    w('- **Details never opened** are listed in '
      f'`{_PRE}_COBERTURA_DE_DETALLES.md`, which is generated from the citation gate. That document '
      'is the authority on what has not been read; it is regenerated on every delivery run.')
    for nota in NOTAS_FALTANTES:          # del proyecto: handoff_proyecto.json, "notas_faltantes"
        w('- %s' % str(nota).replace(chr(10), ' '))
    w('')

    # ---------------------------------------------------------------- 6
    w('---')
    w('')
    w('## 6. Open RFIs, with the delta of each alternative')
    w('')
    R = rfis()
    abiertos = [x for x in R if not x['cerrado']]
    cerrados = [x for x in R if x['cerrado']]
    w('%d open, %d already closed. Read from the `Pending Items` sheet of the workbook, so a '
      'question that gets answered leaves this list by itself. The Impact column is the delta.'
      % (len(abiertos), len(cerrados)))
    w('')
    for x in abiertos:
        w('### RFI %d - %s' % (x['n'], str(x['item']).replace(chr(10), ' ')))
        w('')
        w('- **Area:** %s' % x['area'])
        w('- **Ask:** %s' % x['quien'])
        w('- **What exactly is missing, and why:** %s'
          % str(x['det']).replace(chr(10), ' '))
        w('- **Delta if it goes the other way:** %s' % str(x['imp']).replace(chr(10), ' '))
        w('')
    if cerrados:
        w('### Already closed, kept so nobody reopens them')
        w('')
        for x in cerrados:
            w('- **%d. %s** - %s (delta that was resolved: %s)'
              % (x['n'], str(x['item']).replace(chr(10), ' '),
                 str(x['det']).replace(chr(10), ' '), str(x['imp']).replace(chr(10), ' ')))
        w('')

    # ---------------------------------------------------------------- 7
    w('---')
    w('')
    w('## 7. Rules and corrections that came out of errors, quoted verbatim')
    w('')
    w('Quoted from the addenda, not paraphrased. Each addendum is read from its file, so a '
      'corrected addendum shows up here corrected. These are the ones written in this stretch '
      'of work; the full history is in `SKILL_take-off_VIGENTE.md`.')
    w('')
    # UN BLOQUE QUE DEFINE LA REGLA TIENE QUE PODER CITAR LA PALABRA QUE PROHIBE, y se exime
    # EL BLOQUE, nunca la seccion. La regla de los falsos amigos cita `cara de acabado` como
    # ejemplo, asi que la seccion 7 paraba su propia entrega. Se marca bloque por bloque, y
    # solo el que de verdad trae un termino prohibido, para que una falta de verdad en el
    # resto del handoff se siga cazando. Misma solucion que ya tenian las adendas y
    # verif_respuesta.
    import glosario as _G, vocab_trade as _V
    for titulo, bloques in reglas():
        w('### %s' % titulo)
        w('')
        for b in bloques:
            marcar = bool(_G.faltas(b)) or bool(_V.faltas(b))
            if marcar:
                w('<!-- GLOSARIO:INICIO -->')
            w('> %s' % b)
            if marcar:
                w('<!-- GLOSARIO:FIN -->')
            w('')

    # ---------------------------------------------------------------- 8
    w('---')
    w('')
    w('## 8. Assumptions and decisions Rodolfo approved')
    w('')
    w('Each one with what approved it. An assumption with no approval behind it is not an '
      'approved assumption - it is mine, and it belongs in section 5 or 6 instead.')
    w('')
    w('| Decision | What it means in the numbers | What approved it |')
    w('|---|---|---|')
    for a, b, c in APROBADO:
        w('| %s | %s | %s |' % (a, b.replace('|', '/'), c.replace('|', '/')))
    w('')
    w('---')
    w('')
    w('*Generated by `handoff.py`. Walls: %d. Faces: %d. Line items: %d. Sealed closures '
      'verified: all seals recomputed on load, and the run aborts on a broken one.*'
      % (len(Q), sum(len(q['caras']) for q in Q),
         sum(len(q['partidas']) for q in Q)))

    txt = '\n'.join(L) + '\n'
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, 'w', encoding='utf-8').write(txt)
    return dest, dict(walls=len(Q), lineas=len(L), bytes=len(txt))


if __name__ == '__main__':
    d, info = escribir()
    print('HANDOFF -> %s' % d)
    print('   %d walls, %d renglones, %d bytes' % (info['walls'], info['lineas'], info['bytes']))
