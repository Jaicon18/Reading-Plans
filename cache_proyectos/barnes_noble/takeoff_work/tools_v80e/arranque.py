# -*- coding: utf-8 -*-
"""arranque.py - EL PASO 0 DE CUALQUIER BID SET, EN UN SOLO COMANDO.

    python3 arranque.py "/ruta/al/bid_set.pdf"

Hace, sin que nadie se lo diga y sin saber nada del proyecto:
  1. copia del set SIN /Annots (los markups de otro estimador no se leen nunca)
  2. mapa page_index -> numero de hoja + titulo, leido del TITLE BLOCK de cada pagina
  3. clasifica las hojas clave por TITULO (nunca por numero: cambia entre arquitectos)
  4. escala de cada hoja, derivada del rotulo, en pt por pulgada real
  5. CENSO DE TAGS del floor plan por la prueba de CAJA REAL (sin presuponer que tags hay)
  6. el partition schedule en tabla
  7. las Construction Plan Notes alfabeticas, y cual es el TIPO POR DEFECTO

Todo lo que produce es [CONFIRMADO] o no se produce: cada dato sale del texto del PDF,
ninguno se estima. Lo que no encuentra lo dice y no lo inventa.
"""
import os, re, sys, json, collections, importlib, subprocess

# v68 (arbitraje #16B): el arranque NO instalaba pikepdf / pymupdf y la prueba se cayó en limpiar(). Antes de
# tocar el PDF se verifican los módulos y se instalan si faltan (pip --quiet; si el sistema lo bloquea, con
# --break-system-packages). Lo que no se pueda instalar se dice y se para: nunca se sigue sin la copia limpia.
DEPS = (("pikepdf", "pikepdf"), ("fitz", "pymupdf"), ("pdfplumber", "pdfplumber"))


def asegurar_deps(deps=DEPS, run=subprocess.run, imp=importlib.import_module):
    """[] si todos los módulos importan (instalando los que falten); lista de faltantes si no."""
    falta = []
    for mod, pkg in deps:
        try:
            imp(mod)
            continue
        except ImportError:
            pass
        base = [sys.executable, "-m", "pip", "install", "--quiet", pkg]
        for cmd in (base, base + ["--break-system-packages"]):
            if run(cmd, capture_output=True).returncode == 0:
                break
        importlib.invalidate_caches()
        try:
            imp(mod)
        except ImportError:
            falta.append(pkg)
    return falta

PT_FT_A_ESCALA = {  # rotulo -> pt por PULGADA real
    '1/8"': 0.75, '1/4"': 1.5, '3/8"': 2.25, '1/2"': 3.0,
    '3/4"': 4.5, '1"': 6.0, '1 1/2"': 9.0, '3"': 18.0, '1 1/2': 9.0,
}
RE_HOJA = re.compile(r'^[A-Z]{1,2}\d{1,2}\.\d{2}$')
RE_ESCALA = re.compile(r"(?<![\d/])(\d{1,2}(?:\s+\d/\d|/\d)?)\"\s*=\s*1\x27\s*-?\s*0\"")
RE_ESC = RE_ESCALA


# ---------------------------------------------------------------- 1. copia limpia
def limpiar(src, dst=None):
    """Copia del set SIN /Annots. pdftoppm RENDERIZA las anotaciones: sin esto,
    todo recorte trae dibujados encima los markups del otro estimador."""
    dst = dst or os.path.splitext(src)[0] + '_SIN_MARKUPS.pdf'
    if os.path.exists(dst):
        return dst, None
    import pikepdf
    pdf = pikepdf.open(src); n = 0
    for pg in pdf.pages:
        if '/Annots' in pg:
            n += len(pg['/Annots']); del pg['/Annots']
    pdf.save(dst); pdf.close()
    return dst, n


# ------------------------------------------------- 2. mapa de hojas (title block)
BASURA = re.compile(r'(NSRP|PROPERTY ID|BULLETIN|VERSION|Project No|Reviewed By|SCALE|DRAWN)', re.I)

def marco(d):
    """El marco real del dibujo son los WORDS, no page.width/height: una hoja
    rotada tiene las coordenadas fuera de la caja declarada."""
    xs=[(w['x0']+w['x1'])/2 for w in d['ws']]; ys=[(w['top']+w['bottom'])/2 for w in d['ws']]
    if not xs: return 0,d['w'],0,d['h']
    return min(xs), max(xs), min(ys), max(ys)

def _numero_de_hoja(d):
    x0,x1,y0,y1 = marco(d); W,Hh = x1-x0, y1-y0
    best=None
    for w in d['ws']:
        t=w['text'].strip()
        if not RE_HOJA.match(t): continue
        cx,cy=(w['x0']+w['x1'])/2,(w['top']+w['bottom'])/2
        if cx < x0+W*0.55 or cy < y0+Hh*0.80: continue
        if best is None or w['size']>best[0]: best=(w['size'],t,cx,cy)
    return best

def _titulo_de_hoja(d, num):
    if not num: return None
    S,_,ncx,ncy = num
    x0,x1,y0,y1 = marco(d); W,Hh = x1-x0, y1-y0
    filas=collections.defaultdict(list)
    for w in d['ws']:
        cy=(w['top']+w['bottom'])/2; cx=(w['x0']+w['x1'])/2
        if not (ncy-0.20*Hh < cy < ncy-0.07*Hh): continue
        if abs(cx-ncx) > 0.16*W: continue
        filas[round(cy/6)].append(w)
    cand=[]
    for k,ws in sorted(filas.items()):
        ws=sorted(ws,key=lambda z:z['x0'])
        s=max(z['size'] for z in ws)
        t=' '.join(z['text'] for z in ws).strip()
        if BASURA.search(t) or ':' in t: continue
        # quitar tokens de cabeza que no sean palabra de titulo
        tok=t.split()
        while tok and not re.match(r"^[A-Z&/',\.\-]{3,}$", tok[0]): tok.pop(0)
        t=' '.join(tok)
        if len(t)<3 or not re.search(r'[A-Z]{3}',t): continue
        cand.append((k,s,t))
    if not cand: return None
    smax=max(c[1] for c in cand)
    tit=[c for c in cand if c[1] >= smax-0.6]
    if not tit: return None
    out=[tit[0]]
    for c in tit[1:]:
        if c[0]-out[-1][0] <= 6: out.append(c)
    return ' '.join(c[2] for c in out)

def _escala_de_hoja(d, num):
    """La escala se rotula DEBAJO del titulo de cada dibujo, no en el title block.
    Se barre la hoja entera y se devuelven todas las que aparezcan, por frecuencia."""
    filas = collections.defaultdict(list)
    for w in d['ws']:
        filas[round(((w['top'] + w['bottom']) / 2) / 5)].append((w['x0'], w['text']))
    cnt = collections.Counter()
    for k in sorted(filas):
        t = ' '.join(z[1] for z in sorted(filas[k]))
        for m in RE_ESC.finditer(t):
            cnt[m.group(1) + '"'] += 1
    return [e for e, _ in cnt.most_common()]


def _words_de(pdf, cache_path):
    """Extrae los words de TODAS las paginas una sola vez y los cachea: el paso caro
    del arranque. Una segunda corrida sobre el mismo set es instantanea."""
    import pickle
    if cache_path and os.path.exists(cache_path):
        return pickle.load(open(cache_path, 'rb'))
    out, n = [], len(pdf.pages)
    for i, pg in enumerate(pdf.pages):
        if i % 10 == 0:
            print('   ... leyendo title blocks %d/%d' % (i, n), flush=True)
        ws = [{k: w[k] for k in ('text', 'x0', 'x1', 'top', 'bottom', 'size')}
              for w in pg.extract_words(extra_attrs=['size'])]
        out.append(dict(i=i, w=pg.width, h=pg.height, ws=ws))
        pg.flush_cache()
    if cache_path:
        pickle.dump(out, open(cache_path, 'wb'))
    return out


def mapa_hojas(DW, verbose=True):
    filas = []
    for d in DW:
        ni = _numero_de_hoja(d)
        filas.append(dict(page_index=d['i'], hoja=ni[1] if ni else None,
                          titulo=_titulo_de_hoja(d, ni),
                          escalas=_escala_de_hoja(d, ni)))
    if verbose:
        print('MAPA DE HOJAS  (page_index 0-based; pdftoppm nombra el PNG 1-based)')
        sin = []
        for f in filas:
            if not f['hoja']:
                sin.append(f['page_index']); continue
            print('  %3d  %-9s %-52s %s' % (f['page_index'], f['hoja'],
                                            (f['titulo'] or '?')[:52],
                                            ','.join(f['escalas'][:3])))
        if sin:
            print('  SIN NUMERO DE HOJA LEGIBLE (portada, hojas civiles o title block distinto):')
            print('     page_index %s  -> abrir a ojo antes de declarar nada faltante'
                  % ', '.join(str(x) for x in sin))
    return filas


# ------------------------------------------------------ 3. clasificar por TITULO
CLAVES = [
 ('FLOOR_PLAN',      ('CONSTRUCTION PLAN', 'FLOOR PLAN')),
 ('PARTITION_TYPES', ('PARTITION TYPE', 'PARTITION DETAIL')),
 ('RCP',             ('REFLECTED CEILING',)),
 ('DOOR_SCHEDULE',   ('DOOR SCHEDULE', 'DOOR,', 'DOOR/FRAME', 'HARDWARE', 'DOOR AND FRAME')),
 ('ROOF_FRAMING',    ('ROOF FRAMING',)),
 ('CFS_DETAILS',     ('COLD FORMED', 'FRAMING DETAIL', 'METAL STUD')),
 ('DEMOLITION',      ('DEMOLITION',)),
 ('ENLARGED',        ('ENLARGED',)),
 ('INT_ELEV',        ('INTERIOR ELEVATION', 'SALES ELEVATION')),
 ('EXT_ELEV',        ('EXTERIOR ELEVATION', 'BUILDING ELEVATION')),
 ('SECTIONS',        ('BUILDING SECTION', 'WALL SECTION')),
 ('CODE',            ('CODE ANALYSIS', 'LIFE SAFETY')),
 ('FINISH',          ('FINISH SCHEDULE', 'FINISH PLAN', 'MATERIAL')),
 ('MILLWORK',        ('MILLWORK',)),
 ('MECANICA',       ('MECHANICAL',)),
 ('PLOMERIA',       ('PLUMBING',)),
 ('ELECTRICA',      ('POWER', 'LIGHTING', 'ELECTRICAL')),
]


def clasificar(filas, verbose=True):
    out = collections.OrderedDict((k, []) for k, _ in CLAVES)
    for f in filas:
        t = (f['titulo'] or '').upper()
        for k, kws in CLAVES:
            if any(kw in t for kw in kws):
                out[k].append((f['page_index'], f['hoja'], f['titulo']))
    for k in out:   # la hoja ARQUITECTONICA manda como principal de cada grupo
        out[k].sort(key=lambda z: (0 if (z[1] or '').startswith('A') else 1, z[0]))
    if verbose:
        print('\nHOJAS CLAVE, localizadas por TITULO (nunca por numero)')
        for k in out:
            v = out[k]
            print('  %-16s %s' % (k, ' · '.join('%s(%d)' % (h or '?', p) for p, h, _ in v[:8])
                                  or 'NO ENCONTRADA — barrer el PDF a mano antes de declararla faltante'))
    return out


# --------------------------------------------- 4. censo de tags por CAJA REAL
def _geom(pdf, page_index):
    if True:
        pg = pdf.pages[page_index]
        H, V = [], []

        def add(x0, y0, x1, y1, lw):
            x0, x1 = min(x0, x1), max(x0, x1)
            y0, y1 = min(y0, y1), max(y0, y1)
            if abs(y1 - y0) < 0.3 and abs(x1 - x0) >= 0.3:
                H.append((round((y0 + y1) / 2, 2), x0, x1, lw))
            elif abs(x1 - x0) < 0.3 and abs(y1 - y0) >= 0.3:
                V.append((round((x0 + x1) / 2, 2), y0, y1, lw))

        for o in pg.lines:
            add(o['x0'], o['top'], o['x1'], o['bottom'], o.get('linewidth') or 0.0)
        for o in pg.rects:
            lw = o.get('linewidth') or 0.0
            x0, x1, y0, y1 = o['x0'], o['x1'], o['top'], o['bottom']
            if abs(y1 - y0) < 0.3 or abs(x1 - x0) < 0.3:
                add(x0, y0, x1, y1, lw)
            else:
                add(x0, y0, x1, y0, lw); add(x0, y1, x1, y1, lw)
                add(x0, y0, x0, y1, lw); add(x1, y0, x1, y1, lw)
        words = pg.extract_words()
        size = (pg.width, pg.height)
    return H, V, words, size


def _caja_de(w, H, V):
    cx, cy = (w['x0'] + w['x1']) / 2, (w['top'] + w['bottom']) / 2
    cand = [v for v in V if v[3] <= 0.7 and abs(v[0] - cx) <= 18
            and v[1] <= cy + 3 and v[2] >= cy - 3 and 8 <= (v[2] - v[1]) <= 28]
    best = None
    for a in cand:
        for b in cand:
            if not (10 <= b[0] - a[0] <= 30) or not (a[0] < cx < b[0]):
                continue
            if abs(a[1] - b[1]) > 0.8 or abs(a[2] - b[2]) > 0.8:
                continue
            y0, y1 = (a[1] + b[1]) / 2, (a[2] + b[2]) / 2
            ok = 0
            for yy in (y0, y1):
                for (y, sx0, sx1, lw) in H:
                    if lw <= 0.7 and abs(y - yy) <= 0.8 and sx0 <= a[0] + 1.0 and sx1 >= b[0] - 1.0:
                        ok += 1
                        break
            if ok == 2:
                ar = (b[0] - a[0]) * (y1 - y0)
                if best is None or ar < best[0]:
                    best = (ar, (round(a[0], 2), round(y0, 2), round(b[0], 2), round(y1, 2)))
    return best[1] if best else None


def censo_tags(pdf, page_index, verbose=True):
    """TODA palabra corta con CAJA REAL dentro del area del dibujo. No presupone
    que tags existen: los descubre. Los room tags se separan porque son numericos."""
    H, V, words, (W, Hh) = _geom(pdf, page_index)
    cnt = collections.defaultdict(list)
    for w in words:
        t = w['text'].strip()
        if not (1 <= len(t) <= 5) or not re.match(r'^[A-Z0-9][A-Z0-9\.\-]*$', t):
            continue
        cx, cy = (w['x0'] + w['x1']) / 2, (w['top'] + w['bottom']) / 2
        if cx > W * 0.72:
            continue                    # fuera del sidebar de notas
        c = _caja_de(w, H, V)
        if c:
            cnt[t].append((round(cx, 1), round(cy, 1)))
    part = {k: v for k, v in cnt.items() if not k.isdigit()}
    cuartos = {k: v for k, v in cnt.items() if k.isdigit()}
    if verbose:
        print('\nCENSO DE TAGS del page_index %d  (prueba de CAJA REAL)' % page_index)
        print('  CANDIDATOS A TAG DE PARTICION, por frecuencia:')
        for k, v in sorted(part.items(), key=lambda z: (-len(z[1]), z[0])):
            print('     %-6s %3d' % (k, len(v)))
        print('  (numericos = room tags, %d distintos)' % len(cuartos))
        print('  >>> Este censo es el que la NUMERACION OFICIAL tiene que reproducir.')
        print('  >>> Todo candidato dudoso se ABRE EN IMAGEN antes de aceptarlo o descartarlo.')
    return part, cuartos


# ------------------------------------------------- 5. schedule de particiones
def schedule_particiones(pdf, page_index, verbose=True):
    """Filas del partition schedule. No busca la cabecera (viene partida en 3
    renglones en casi todos los sets): busca FILAS DE DATOS — un tag corto seguido
    de dos o mas medidas en pulgadas. Eso es una fila de schedule y nada mas lo es."""
    ws = pdf.pages[page_index].extract_words()
    filas = collections.defaultdict(list)
    for w in ws:
        filas[round(((w['top'] + w['bottom']) / 2) / 6)].append(w)
    # Una fila de la tabla puede traer DOS registros pegados (las dos mitades del
    # schedule caen al mismo y). Un registro empieza donde un TAG va seguido de una
    # medida en pulgadas: eso, y solo eso, es una fila de partition schedule.
    RE_REG = re.compile(r'\b([A-Z]{1,2}\d{0,2}[A-Z]?)\s+(\d+(?:\s+\d+/\d+)?")')
    RE_MED = re.compile(r'\d+(?:\s+\d+/\d+)?"')
    out = []
    for k in sorted(filas):
        g = sorted(filas[k], key=lambda z: z['x0'])
        t = ' '.join(z['text'] for z in g)
        for m in RE_REG.finditer(t):
            tramo = t[m.start():m.start() + 120]
            sig = RE_REG.search(tramo, 1)
            if sig:
                tramo = tramo[:sig.start()]
            med = RE_MED.findall(tramo)
            if len(med) < 2:
                continue
            out.append(dict(tag=m.group(1), stud=med[0], espesor=med[-1],
                            medidas=med, fila=tramo.strip()[:110], y=round(k * 6, 1)))
    vistos, únicos = set(), []
    for r in out:
        if r['tag'] in vistos:
            continue
        vistos.add(r['tag']); únicos.append(r)
    out = únicos
    # la columna WALL THICKNESS es la ultima medida de la fila en casi todos los sets
    if verbose:
        print('\nPARTITION SCHEDULE (page_index %d)' % page_index)
        if not out:
            print('  no se pudo tabular -> ABRIR IMAGEN del schedule. Nunca inventarlo.')
        print('   %-6s %-10s %-12s  %s' % ('TAG', 'STUD', 'ESPESOR', 'fila leida'))
        for r in out:
            print('   %-6s %-10s %-12s  %s' % (r['tag'], r['stud'], r['espesor'], r['fila'][:66]))
        if out:
            print('  >>> El schedule da MATERIALES. Las ALTURAS salen del DETALLE dibujado')
            print('      de cada tipo, que hay que abrir uno por uno (regla: tablas identicas')
            print('      no son muros identicos).')
    return None, out


# --------------------------------- 6. notas alfabeticas + TIPO POR DEFECTO
def notas_de_hoja(pdf, page_index, verbose=True):
    pg = pdf.pages[page_index]
    ws = pg.extract_words()
    W = pg.width
    filas = collections.defaultdict(list)
    for w in ws:
        if (w['x0'] + w['x1']) / 2 < W * 0.70:
            continue                      # las notas viven en el sidebar derecho
        filas[round(((w['top'] + w['bottom']) / 2) / 6)].append(w)
    lineas = []
    for k in sorted(filas):
        ws2 = sorted(filas[k], key=lambda z: z['x0'])
        lineas.append((round(k * 6, 1), ' '.join(z['text'] for z in ws2)))
    # una nota alfabetica arranca con "A." "B." ... y se continua en las lineas siguientes
    notas, act = [], None
    for y, t in lineas:
        m = re.match(r'^([A-Z])\.\s+(.*)$', t)
        if m:
            if act: notas.append(act)
            act = [m.group(1), m.group(2)]
        elif act and t and not re.match(r'^[A-Z ]{6,}:?$', t):
            act[1] += ' ' + t
        elif act and re.match(r'^[A-Z ]{6,}:?$', t):
            notas.append(act); act = None
    if act: notas.append(act)
    defecto = None
    for L, t in notas:
        m = re.search(r"ALL PARTITIONS?\s+(?:TO BE|SHALL BE)\s+TYPE\s*['\"]?([A-Z0-9]+)['\"]?", t.upper())
        if m:
            defecto = (L, m.group(1), t)
    if verbose:
        print('\nCONSTRUCTION PLAN NOTES alfabeticas (page_index %d)' % page_index)
        for L, t in notas:
            print('   %s. %s' % (L, t[:150]))
        print('\n  >>> TIPO POR DEFECTO: %s' % (
            ('**%s**  (nota %s)  -> TODO muro SIN TAG es de este tipo y se cuantifica igual'
             % (defecto[1], defecto[0])) if defecto
            else 'NO se encontro nota de tipo por defecto — leerla a ojo antes de planear las pasadas'))
    return notas, defecto


def _plausibles(tags):
    """De todo el censo, los que TIENEN PINTA de tag de particion: una o dos letras
    con digitos opcionales. Filtra room tags, millwork (MW..) y callouts de hoja."""
    import re as _re
    return {t for t in tags
            if _re.match(r'^[A-Z]{1,2}\d{0,2}[A-Z]?$', t)
            and not t.startswith('MW') and not t[0].isdigit()}


# ------------------------------------------------------------------- arranque
def arrancar(src, floor_plan=None, partition=None):
    falta = asegurar_deps()
    if falta:
        sys.exit('ARRANQUE DETENIDO: no se pudieron instalar %s (pip install %s)' % (falta, ' '.join(falta)))
    import pdfplumber
    print('=' * 78)
    print('ARRANQUE  ·  %s' % os.path.basename(src))
    print('=' * 78)
    limpio, n = limpiar(src)
    print('PDF limpio: %s%s' % (limpio,
          ('   (%d anotaciones eliminadas)' % n) if n is not None else '   (ya existia)'))
    print('TODO recorte sale de aqui. El original solo para mirar los markups a proposito.\n')

    pdf = pdfplumber.open(limpio)
    DW = _words_de(pdf, os.path.splitext(limpio)[0] + '_titleblocks.pkl')
    filas = mapa_hojas(DW)
    cls = clasificar(filas)

    fp = floor_plan if floor_plan is not None else (cls['FLOOR_PLAN'][0][0] if cls['FLOOR_PLAN'] else None)
    pt = partition if partition is not None else (cls['PARTITION_TYPES'][0][0] if cls['PARTITION_TYPES'] else None)

    res = dict(pdf_limpio=limpio, anotaciones=n, hojas=filas,
               clave={k: v for k, v in cls.items()}, floor_plan=fp, partition_types=pt)
    if fp is not None:
        esc = filas[fp]['escalas']
        print('\nESCALA del floor plan: %s' % (', '.join(esc) or '?'))
        for e in esc:
            if e in PT_FT_A_ESCALA:
                print('   -> %s = 1\'-0\"  =  %.2f pt por PULGADA real  =  %.1f pt por pie'
                      % (e, PT_FT_A_ESCALA[e], PT_FT_A_ESCALA[e] * 12))
                res['pt_por_pulgada'] = PT_FT_A_ESCALA[e]
                break
        part, cuartos = censo_tags(pdf, fp)
        res['censo_tags'] = {k: len(v) for k, v in part.items()}
        res['room_tags'] = len(cuartos)
        notas, defecto = notas_de_hoja(pdf, fp)
        res['notas'] = notas
        res['tipo_por_defecto'] = defecto[1] if defecto else None
    if pt is not None:
        cab, sch = schedule_particiones(pdf, pt)
        res['schedule'] = sch
        # --- cruce automatico censo x schedule -------------------------------
        if sch and res.get('censo_tags'):
            enplano = set(res['censo_tags'])
            enschedule = {r['tag'] for r in sch}
            sin_fila = sorted(t for t in enplano & _plausibles(enplano) if t not in enschedule)
            sin_plano = sorted(t for t in enschedule if t not in enplano)
            print('\nCRUCE  censo del plano  x  partition schedule')
            print('  Tipos CON tag en planta y CON fila de schedule:')
            for r in sch:
                if r['tag'] in enplano:
                    print('     %-5s %-9s espesor %-8s  %d tag(s) en planta'
                          % (r['tag'], r['stud'], r['espesor'], res['censo_tags'][r['tag']]))
            print('  Tipos CON tag en planta y SIN fila de schedule  -> NO es RFI automatico:')
            print('     %s' % (', '.join(sin_fila) or '(ninguno)'))
            if sin_fila:
                print('     se derivan por aritmetica de capas del detalle + delta de familia +')
                print('     espesor MEDIDO en planta; los tres tienen que cerrar.')
            print('  Tipos CON fila de schedule y SIN tag en planta (no se cuantifican):')
            print('     %s' % (', '.join(sin_plano) or '(ninguno)'))
            res['sin_fila'] = sin_fila; res['sin_plano'] = sin_plano
    pdf.close()
    print('\n' + '=' * 78)
    print('LO QUE SIGUE, A MANO: abrir el DETALLE de cada tipo (el schedule da materiales,')
    print('el detalle da alturas), y el barrido por tag con su paquete de imagenes y su pausa.')
    print('=' * 78)
    return res


if __name__ == '__main__':
    r = arrancar(sys.argv[1],
                 int(sys.argv[2]) if len(sys.argv) > 2 else None,
                 int(sys.argv[3]) if len(sys.argv) > 3 else None)
    # v77 (R76.7 e): arranque.json en la carpeta de trabajo (antes una ruta fija) y las tools siguientes sobre la copia limpia
    salida = os.path.join(os.environ.get('TAKEOFF_WORK') or os.getcwd(), 'arranque.json')
    json.dump({k: v for k, v in r.items() if k != 'hojas'}, open(salida, 'w'), indent=1, ensure_ascii=False)
    print('arranque.json -> %s' % salida)
    print('SIGUIENTE (copia limpia): alcances.py escanear "%s" alcances.json ; inventario_tags.py "%s" <dir>/1_inventario'
          % (r['pdf_limpio'], r['pdf_limpio']))
