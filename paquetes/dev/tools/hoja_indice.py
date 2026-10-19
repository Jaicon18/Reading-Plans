# -*- coding: utf-8 -*-
"""hoja_indice.py -- genera 00_INDICE_DE_ARCHIVOS.md LEYENDO la carpeta de entrega.

Por que existe (error del 01-oct-2026):
    El indice estaba escrito a mano. Decia "77 elementos" cuando ya eran 78, "58 scripts"
    cuando ya eran 72, "la carta de RFIs todavia no existe" cuando ya existia, y seguia
    pidiendo borrar un plano que Rodolfo ya habia borrado. Es el MISMO patron que ya
    habia obligado a generar BOA_ESTADO.md y la carta de RFIs desde el libro: un
    documento escrito a mano se queda viejo y MIENTE, y el indice es justo el documento
    que se abre primero. Si miente el indice, no sirve nada de lo que apunta.

Regla que impone:
    el indice no lista lo que yo creo que hay: lista lo que la carpeta TIENE, contado por
    el sistema de archivos, y lo que el estado sellado DICE, leido de los cierres y del
    libro. Un archivo que esta en la carpeta y no en el indice es imposible, y un archivo
    que esta en el indice y no en la carpeta tambien.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (antes fijas en /home/claude/boa)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", "/home/claude/boa")
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import os, sys, re, glob, json, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
B = f'{_TW}'
ENTREGA = f'{_TO}/entrega'
DEST = os.path.join(ENTREGA, '00_INDICE_DE_ARCHIVOS.md')

# Donde queda cada cosa en la PC. El indice se lee EN la PC, asi que los rotulos de
# carpeta son los de alla, no los del contenedor.
CARPETA = {'.xlsx': 'Excel', '.jpg': 'Planos marcados por tipo', '.md': 'Documentos'}

# Grupos de scripts, en el orden en que importan. El primer patron que casa manda.
GRUPOS = [
    ('COMPUERTAS (verifican y BLOQUEAN si algo no cuadra)',
     lambda n: n.startswith('verif_') or n in ('closer.py', 'auditor.py', 'auditar_bandas.py')),
    ('PRUEBAS de las compuertas (las hacen fallar a proposito)',
     lambda n: n.startswith('test_')),
    ('ENTREGA (la unica puerta de salida) y los documentos que se generan solos',
     lambda n: n in ('entregar.py', 'excel.py', 'dataset.py', 'resumen_total.py',
                     'resumen_global.py') or n.startswith('hoja_')),
    ('CIERRES por tipo de wall y por zona',
     lambda n: n.startswith('cerrar_')),
    ('PLANOS MARCADOS',
     lambda n: n in ('planmark.py', 'hojas_por_tipo.py', 'bandas.py')),
    ('IDIOMA (todo nombre de material en ingles)',
     lambda n: n in ('glosario.py', 'traducir_materiales.py')),
    ('DETALLES del set (que se abrio y que no)',
     lambda n: n in ('cache_detalles.py', 'titulos_detalles.py', 'ver_detalle.py')),
    ('CRUCE con otras hojas (MEP, geometria)',
     lambda n: n in ('mep.py', 'cruzar_mep.py', 'cruzar_diagonal.py', 'geo.py',
                     'wallgeom.py', 'perimetro.py', 'cadena.py', 'endcap.py',
                     'localizar.py', 'tagloc.py', 'cuarto.py', 'zona_cielo.py',
                     'arranque.py')),
    ('COMPARATIVO contra otro take-off',
     lambda n: n == 'comparar_bluebeam.py'),
]

# Descripcion de los .md de respaldo. El que no este aqui toma su propio titulo H1, para
# que un documento nuevo aparezca igual en el indice en vez de desaparecer en silencio.
DOCS = {
 'BOA_ESTADO.md': '**Resumen del estado.** Se genera LEYENDO el Excel, no se escribe a mano',
 'BOA_RFI_al_arquitecto.md': '**La carta de RFIs**, lista para mandar. Se genera de la hoja `Pending Items`',
 'BOA_COBERTURA_DE_DETALLES.md': '**Que detalle del set se abrio y cual no**, con el motivo de cada exclusion. Se genera de la compuerta `verif_detalles.py`',
 'BOA_AUDITORIA_correcciones_2026-09-28.md': 'Los 14 hallazgos de la auditoria adversarial y como se corrigio cada uno',
 'BOA_EXTERIORES_cerrado.md': 'Cierre completo de los walls exteriores, pasadas 1 y 2',
 'BOA_CIELOS_GWB_cerrado.md': 'Cierre de los ceilings de board',
 'BOA_SOFFITS.md': 'Cierre del soffit CSR y la marquesina',
 'BOA_SOFFITS_metal_frame.md': 'La metal framing de los soffits, por separado',
 'BOA_correccion_planos_marcados.md': 'Los 6 errores de dibujo del 27-sep y su correccion',
 'PROMPT_take-off_VIGENTE.md': '**El prompt que va en settings.** Nombre fijo: se REEMPLAZA, no se versiona',
 'SKILL_take-off_VIGENTE.md': '**El protocolo completo**, con el porque de cada regla. Nombre fijo',
}


def _doc1(path):
    """Primera linea de docstring de un .py, para la tabla de herramientas."""
    try:
        txt = open(path, encoding='utf-8').read(4000)
    except Exception:
        return ''
    m = re.search(r'"""(.*?)(?:\n|""")', txt, re.S)
    if not m:
        return ''
    d = m.group(1).strip()
    d = re.sub(r'^[\w./]+\.py\s*[-—]+\s*', '', d).strip()
    return (d[:150] + '...') if len(d) > 150 else d


def _h1(path):
    for l in open(path, encoding='utf-8'):
        if l.startswith('# '):
            return l[2:].strip()
    return ''


def _planos():
    """{archivo: rotulo} -- el rotulo sale del MISMO sitio que el del plano dibujado."""
    import hojas_por_tipo as H
    rot = {}
    for t, tit in H.TIT.items():
        rot['PLANO_' + t] = tit
    rot['PLANO_EXTERIORES'] = ('WALLS EXTERIORES (EXT-6CFMF) -- el storefront va en '
                               'naranja porque es Div 08')
    rot['PLANO_CIELOS_GWB'] = 'CEILINGS DE BOARD (GWB) sobre el RCP'
    rot['PLANO_SOFFITS'] = 'SOFFITS: el CSR y la marquesina, tabla propia'
    out = []
    for f in sorted(os.listdir(ENTREGA)):
        if not f.lower().endswith('.jpg'):
            continue
        clave = re.sub(r'^\d+_', '', os.path.splitext(f)[0])
        out.append((f, rot.get(clave, '(sin rotulo declarado en el generador)')))
    return out


def _estado(xlsx):
    """Numeros del estado leidos del LIBRO y de los sellos, nunca tecleados."""
    import openpyxl
    wb = openpyxl.load_workbook(xlsx, data_only=True)
    hojas = [(ws.title, ws.max_row - 1) for ws in wb.worksheets]
    wb.close()
    # Los pendientes NO se vuelven a leer aqui: su lector es hoja_rfi.leer_pendientes, el
    # mismo que escribe la carta. Leerlos por mi cuenta, buscando la columna por nombre,
    # dio 18 renglones vacios -- la hoja no tiene encabezado 'ask'/'item', va por posicion.
    # Un renglon vacio en el indice es peor que ninguno: parece que el pendiente existe y
    # no dice cual.
    import hoja_rfi as RFI
    pend = [(str(d['item'] or ''), str(d['quien'] or '')) for d in RFI.leer_pendientes(xlsx)]
    return hojas, pend


def main(xlsx=None, dest=DEST):
    import glosario as G
    xlsx = xlsx or os.path.join(ENTREGA, 'BOA_Broomfield_Takeoff.xlsx')
    hojas, pend = _estado(xlsx)

    import verif_planos as VP
    sell = VP.sellados()
    mani = xlsx[:-5] + '.manifiesto.json'
    # La clave es 'fuentes', no 'insumos': leerla con .get() y un default dejaba un 0 en el
    # indice sin que nada se quejara. Un .get() con default sobre un archivo propio esconde
    # el error de tecleo; aqui se exige la clave y se revienta si no esta.
    n_ins = len(json.load(open(mani, encoding='utf-8'))['fuentes'])\
        if os.path.exists(mani) else 0
    # Los elementos sellados no son solo muros: tambien cielos, soffits, marquesina y los
    # cierres sueltos. Decir "57" cuando el sello dice 78 es la clase de numero que luego
    # alguien cita como total del proyecto.
    #
    # Y NO se vuelve a contar aqui: el dueno de ese numero es resumen_total.py, el mismo que
    # usa la compuerta de sellos. Contarlo otra vez por mi cuenta ya dio 0 (adivine la llave
    # del sello) -- dos implementaciones del mismo conteo siempre acaban diciendo cosas
    # distintas, que es exactamente el motivo por el que existe verif_planos. Se le PREGUNTA
    # al dueno y se lee su renglon POR CONTENIDO, nunca por posicion.
    import subprocess
    r = subprocess.run(['python3', B + '/tools/resumen_total.py'],
                       capture_output=True, text=True)
    lin = [l for l in (r.stdout or '').splitlines() if 'sellos OK' in l]
    if not lin:
        raise RuntimeError('resumen_total.py no reporto sellos: el indice no se escribe '
                           'con un total inventado')
    m = re.search(r'(\d+)\s+(\d+) sellos OK / (\d+) rotos', lin[-1])
    if not m:
        raise RuntimeError('no pude leer el renglon de sellos: ' + lin[-1].strip())
    n_sel, n_ok, n_rot = (int(g) for g in m.groups())
    if n_rot or n_ok != n_sel:
        raise RuntimeError('hay %d sellos rotos: el indice no se escribe' % n_rot)

    tools = sorted(os.path.basename(p) for p in glob.glob(ENTREGA + '/Herramientas/*.py'))
    xls = sorted(f for f in os.listdir(ENTREGA) if f.endswith('.xlsx'))
    mds = sorted(f for f in os.listdir(ENTREGA)
                 if f.endswith('.md') and not f.startswith('00_'))

    import verif_detalles as VD
    faltan, uni, cit = VD.verificar()
    n_det = sum(len(v) for v in uni.values())
    n_fal = sum(len(s) for _, s, _ in faltan)

    L = ['# INDICE DE ARCHIVOS -- Take-Off Claude',
         '## Bank of America - Broomfield, CO - Permit Set / Bid Set', '',
         'Generado **%s** por `hoja_indice.py`, el ultimo paso de `entregar.py`. '
         '**No se escribe a mano**: lista lo que la carpeta TIENE, contado por el sistema '
         'de archivos, y lo que el estado sellado DICE, leido de los cierres y del libro. '
         'Por eso no puede quedarse viejo.'
         % datetime.date.today().strftime('%d-%b-%Y'), '',
         '**Estado: %d elementos cerrados y sellados** (%d de ellos walls; el resto ceilings, '
         'soffits, marquesina y cierres sueltos)**, %d insumos bajo sello, %d sellos rotos.** '
         'El take-off usa **unicamente mis mediciones** -- el archivo de Bluebeam queda como '
         'referencia de contraste, no como fuente de ninguna cantidad.'
         % (n_sel, len(sell), n_ins, n_rot), '',
         '| | |', '|---|---|',
         '| Elementos sellados | %d |' % n_sel,
         '| Excel | %d |' % len(xls),
         '| Planos marcados | %d |' % len([f for f in os.listdir(ENTREGA) if f.endswith('.jpg')]),
         '| Documentos de respaldo | %d |' % len(mds),
         '| Herramientas (.py) | %d |' % len(tools),
         '| Detalles del set revisados | %d de %d (%d sin abrir) |' % (n_det - n_fal, n_det, n_fal),
         '', '---', '',
         '# 1. Lo que se usa para cotizar', '', 'Carpeta `Excel\\`', '',
         '| archivo | que es |', '|---|---|']
    for f in xls:
        q = ('**EL ENTREGABLE.** %d hojas, formulas vivas, formato "Organized Partition '
             'Takeoff Estimator". Empezar en `Material Summary`; `Inputs` en amarillo es lo '
             'unico que se toca a mano' % len(hojas)) if 'Takeoff' in f and 'COMPARA' not in f\
            else 'Comparativo contra el take-off de Bluebeam. **Referencia, no fuente**'
        L.append('| **`%s`** | %s |' % (f, q))
    L += ['', '### Las hojas del entregable', '', '| hoja | renglones |', '|---|---|']
    L += ['| `%s` | %d |' % (t, n) for t, n in hojas]

    L += ['', '---', '', '# 2. Planos marcados', '',
          'Carpeta `Planos marcados por tipo\\` -- hoja completa, **un tipo por hoja**, '
          'rectangulo sobre la extension real del wall, rotulado con el numero oficial + '
          'LF. Azul = con tag, rojo = sin tag, naranja = otra division, verde = bulkhead. '
          '300 dpi desde la copia sin markups. El LF de cada rotulo lo verifica '
          '`verif_planos.py` contra el cierre sellado, asi que el plano y el Excel no '
          'pueden decir numeros distintos.', '',
          '| archivo | que contiene |', '|---|---|']
    L += ['| `%s` | %s |' % (f, r) for f, r in _planos()]

    L += ['', '---', '', '# 3. Documentos de respaldo', '', 'Carpeta `Documentos\\`', '',
          '| archivo | que es |', '|---|---|']
    hist = []
    for f in mds:
        if re.match(r'(SKILL_take-off_v\d+|adenda_v\d+)', f):
            hist.append(f)
            continue
        L.append('| `%s` | %s |' % (f, DOCS.get(f) or _h1(os.path.join(ENTREGA, f))))
    if hist:
        L += ['| %s | Historico congelado: por que se agrego cada regla y cuando. '
              'El vigente es el de nombre fijo |' % ' / '.join('`%s`' % h for h in hist)]

    L += ['', '---', '', '# 4. Herramientas', '',
          'Carpeta `Herramientas\\` -- los **%d** scripts que producen y verifican todo lo '
          'anterior. No hace falta abrirlos para cotizar; estan aqui para que el trabajo '
          'sea reproducible y auditable.' % len(tools), '',
          '**El unico comando que importa:** `entregar.py`. Es la unica puerta de salida y '
          'corre los 9 pasos en orden -- sellos -> planos marcados -> regenera el Excel -> '
          'vigencia -> estado -> carta de RFIs -> cobertura de detalles -> idioma -> copia. '
          'Si algo no cuadra, **no entrega nada**.', '']
    visto = set()
    for tit, pred in GRUPOS:
        fs = [n for n in tools if n not in visto and pred(n)]
        visto |= set(fs)
        if not fs:
            continue
        L += ['## ' + tit, '', '| archivo | que hace |', '|---|---|']
        L += ['| `%s` | %s |' % (n, _doc1(ENTREGA + '/Herramientas/' + n)) for n in fs]
        L += ['']
    resto = [n for n in tools if n not in visto]
    if resto:
        L += ['## OTROS', '', '| archivo | que hace |', '|---|---|']
        L += ['| `%s` | %s |' % (n, _doc1(ENTREGA + '/Herramientas/' + n)) for n in resto]
        L += ['']

    L += ['---', '', '# 5. Lo que falta para cerrar el proyecto', '',
          '**%d pendientes**, cada uno con su motivo y a quien pedirselo en la hoja '
          '`Pending Items` del Excel. La carta lista para mandar es '
          '`BOA_RFI_al_arquitecto.md`.' % len(pend), '',
          '| pendiente | a quien |', '|---|---|']
    L += ['| %s | %s |' % (i[:90], a) for i, a in pend]
    L += ['', 'Y **%d detalles del set sin abrir** -- la lista esta en '
          '`BOA_COBERTURA_DE_DETALLES.md`.' % n_fal, '']

    txt = G.traducir('\n'.join(L))
    open(dest, 'w', encoding='utf-8').write(txt)
    print('indice -> %s  (%d xlsx, %d planos, %d docs, %d scripts)'
          % (dest, len(xls), len([f for f in os.listdir(ENTREGA) if f.endswith('.jpg')]),
             len(mds), len(tools)))
    return dest


if __name__ == '__main__':
    main()
