# -*- coding: utf-8 -*-
"""verif_callouts.py -- COMPUERTA: el detalle que el plano SENALA se usa, siempre.

Orden de Rodolfo, 2-oct-2026: "siempre se tiene que usar los detalles que marcan los planos
ya que ahi esta la informacion que se necesita, nunca saltarse esta regla."

QUE LA ORIGINO. La marquesina de la fachada este (CANOPY-84) se cerro con geometria medida
en planta. `D/A9.22` es la seccion que la corta y da su fondo, su framing y sus datums: nunca
se abrio. Y el MISMO dia yo si abri D/A9.22 -- para los datums del parapeto -- sin preguntarme
que mas gobierna. Un detalle no es de quien lo abre: es de TODO lo que corta.

EN QUE SE DIFERENCIA DE `verif_detalles.py`. Aquella mira, de las hojas que el take-off YA
cita, que detalles quedaron sin citar: solo ve donde ya miraste. Esta mira lo que el PLANO
SENALA -- cada burbuja de seccion/detalle dibujada sobre las hojas de planta -- y exige que
este citada o declarada. Es la que habria cazado D/A9.22, porque la burbuja esta en A02.01
aunque el take-off no citara A09.22.

QUE EXIGE. Toda burbuja `<etiqueta>/<hoja>` de una hoja de PLANTA tiene que estar:
  (a) citada por algun cierre sellado, en forma `N/HOJA` legible por maquina, o
  (b) declarada en NO_APLICAN con su motivo escrito.
Lo que no este en ninguna de las dos para la entrega.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (antes fijas en /home/claude/boa)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", "/home/claude/boa")
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import os, sys, re, json, glob, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verif_detalles as VD
import cadena_detalles as _CD   # lector de citas y rotulo REAL de cada hoja

PDF = VD.PDF
CACHE = f'{_TW}/callouts_cache.json'

# LA CADENA SE SIGUE HASTA EL FINAL (orden de Rodolfo, 2-oct-2026: "tienes que revisar todos
# y cada uno de los detalles, por ejemplo en el canopy 84 son 3... pero en otros habra mas").
#
# Un detalle LLAMA A OTRO detalle. El canopy 84 son TRES eslabones:
#   soffit plan (burbuja D/A9.22) -> D/A09.22 SECTION (burbuja 7/A09.26) -> 7/A09.26 SIDE CANOPY
# y la seccion D sola llama a CINCO (4/A09.26, 7/A09.26, 11/A09.27, 10/A09.27, 5/A09.26).
#
# Esta compuerta barria SOLO las hojas de planta, o sea el primer eslabon. Una cadena cortada
# en el segundo eslabon es tan ciega como no haber empezado: por ahi vivia 7/A09.26, que es el
# detalle que de verdad gobierna la marquesina.
#
# Ahora barre TODA hoja de la que el take-off ya depende -- plantas Y hojas de detalle/seccion --
# y se repite hasta que no aparezcan hojas nuevas (cierre transitivo).
# El rotulo de la hoja destino se escribe de dos formas en el mismo set: `A09.22` en el title
# block y `A9.22` dentro de la burbuja. Se canoniza QUITANDO el cero, no agregandolo:
# rellenar a dos digitos convertia `S5.20` en `S05.20`, una hoja que NO EXISTE, y el estimador
# la buscaba y no la encontraba. La serie estructural se escribe con un digito.
HOJA_BURB = re.compile(r'^([A-Z]{1,2})0?(\d{1,2})\.(\d{2})$')
ETIQ = re.compile(r'^(?:\d{1,2}|[A-Z])$')


def norm(h):
    m = HOJA_BURB.match(h.strip())
    return '%s%d.%s' % (m.group(1), int(m.group(2)), m.group(3)) if m else h.strip()


PLANTAS = ('A2.01', 'A2.02', 'A4.01', 'A8.01', 'A8.11')     # en forma canonica (sin cero)
# Series donde viven los detalles a los que las plantas remiten, tambien canonicas.
DETALLES = ('A9.', 'A12.', 'A11.', 'S5.', 'S3.', 'S2.')


def _es_fuente(rot):
    """True si de esa hoja NACEN burbujas que hay que seguir: plantas y hojas de detalle."""
    if not rot:
        return False
    r = norm(rot)
    return r in PLANTAS or any(r.startswith(p) for p in DETALLES)


NO_APLICAN = {
    # hoja -> {etiqueta: motivo}. Se declara MIRANDO el detalle, nunca para callar la
    # compuerta. Cada motivo dice QUE se leyo en ese detalle y por que no deja partida.
    'A12.10': {'1': '24 HR VESTIBULE PLAN: planta de puertas del vestibulo con lectores de '
                    'tarjeta, hojas activas y botones accesibles. Es layout de Div 08 43 13 '
                    '(aluminum storefront) y Div 28 (control de acceso). No rotula ningun '
                    'material de framing ni de board, y los muros del vestibulo ya estan '
                    'cerrados por su tag en A02.01. Contraste: 1/A09.25, que si rotula '
                    '"3 5/8\" METAL STUD" y "5/8\" GYPSUM BOARD", SI deja partida.'},

    # ---- S3.20 FOUNDATION DETAILS -------------------------------------------------
    # Leidos uno por uno con det_region. De los 13 detalles de la hoja, solo 2 y 9
    # rotulan "LT. GA. FRAMING & CONNX REF. LT. GA. NOTES & DETAILS" (base de muro
    # exterior y base de columna de canopy): ESOS DOS SI se citan. Los cinco de abajo
    # no nombran framing ligero en ninguna parte de su cuerpo.
    'S3.20': {
        '3': 'TYP. GRADE BEAM @ ENTRY: viga de cimentacion en la entrada. Rotula '
             '"CL OF PIER", "EXIST. GRADE", "SIDEWALK WHERE ... NOTED ON SITE PLAN", '
             'armado y void forms. Div 03 30 00 (concreto colado en sitio). No rotula '
             'LT. GA. FRAMING, ni track, ni board. Contraste con 2/S3.20, la misma '
             'familia de detalle, que SI pone "LT. GA. FRAMING & CONNX REF. LT. GA. '
             'NOTES & DETAILS" y por eso SI se cita en el bottom track del muro exterior.',
        '5': 'TYPICAL STRUCTURAL STOOP: losa estructural de acceso sobre void forms, '
             '"STRUCTURED SLAB REF. DEPTH", "SIDEWALK WHERE ... NOTED ON SITE PLAN". '
             'Div 03 30 00. Ningun material de Div 05 40 00 ni Div 09 29 00 rotulado.',
        '6': 'TYP. PERIM. GR. BM @ COLUMN: viga perimetral donde aterriza una columna '
             'de acero. Rotula "STEEL COLUMN TYPE & BASEPLATE & ANCHOR BOLTS REF. '
             'SCHEDULE". Es Div 03 30 00 mas Div 05 12 00 (acero estructural y su '
             'placa base con anclas). La columna la instala el montador de acero. '
             'Nuestro stud de 6" corre por fuera y ya esta contado en el muro exterior '
             'como metal corrido (no se deduce por columna).',
        '7': 'TYP. GRADE BEAM AT INTER. COL.: igual que 6 pero en columna interior. '
             '"STEEL COLUMN TYPE & BASEPLATE", "BASEPLATE & ANCHOR BOLTS". Div 03 + '
             'Div 05 12 00. No rotula framing ligero ni board.',
        '8': 'TYP. INTERIOR GRADE BEAM: viga de cimentacion interior con su armado y '
             'la palabra "COLUMN". Div 03 30 00. Los muros interiores arrancan de losa '
             'con bottom track pineado, condicion que ya quedo cerrada por el tipo de '
             'particion; esta hoja no aporta material nuestro.',
    },

    # ---- S5.10 LIGHT GAUGE / STEEL DETAILS ----------------------------------------
    # Leidos uno por uno. 6 y 10 ("SECTION AT PERIMETER") rotulan "DEFLECTION TRACK
    # PER LT. GA. MFR." y 11 es PARAPET INFILL FRAMING: esos SI se citan. Los de abajo
    # son conexiones soldadas y empernadas de acero estructural.
    'S5.10': {
        '4': 'PERIMETER ROOF EDGE: "L3x3x1/4 CONT. (BUTT-WELD SPLICES)" con soldadura '
             '3/16 continua sobre "BEAM REF. PLAN" y "STANDARD SHEAR CONNX". Es el '
             'angulo de borde de losa de techo: Div 05 12 00, lo pone el montador de '
             'acero. Contraste con 6/S5.10, el detalle de al lado, que ademas del '
             'mismo angulo SI rotula "DEFLECTION TRACK PER LT. GA. MFR." y "LT. GA. '
             'FRAMING": ese SI deja partida nuestra.',
        '8': 'CANOPY BM @ DRAIN LOCS: viga de canopy en los puntos de drenaje. Rotula '
             '"1/2\" CAP PLATE", "3/8\" STIFF. PL", soldaduras 5/16 N.S. & F.S., '
             '"STANDARD AISC SHEAR CONNECTION", conexiones MC3/MC5/SC3/SC4 y el '
             'COLUMN BASEPLATE SCHEDULE (CB1..CB6, anclas de 3/4" y 1"). Div 05 12 00 '
             'completo. El drywall del canopy cuelga de esta viga pero el material de '
             'esta lamina es todo acero estructural soldado en taller y en campo.',
        '9': 'ROOF STEP AT GRID B: escalon de techo entre dos vigas de acero. '
             '"PL 1/2 x 5 w/ (4) 3/4\" DIA. A325-X BOLTS TYP. TOP & BOTT.", '
             '"L3x3x1/4 x CONT.", soldadura 1/4. Div 05 12 00. Ningun material nuestro.',
        '12': 'STEEL BMS TO STEEL COL. CONNX: conexiones de viga a columna de acero. '
              'Div 05 12 00 por definicion. No toca framing ligero ni board.',
        '13': 'CANOPY STEP SECTION: escalon entre viga de canopy y viga de techo, '
              '"L3x3x1/4 CONT. (BUTT-WELD SPLICES)", soldadura 3/16, y manda '
              '"REF. 6/S5.10 FOR ADDL INFO.". El material de ESTE detalle es acero '
              'estructural (Div 05 12 00); el framing ligero que menciona por '
              'referencia vive en 6/S5.10, que SI se cita en el deflection track.',
    },

    # ---- S5.30 BRACED FRAME ELEVATIONS --------------------------------------------
    # Los cinco son la misma familia: elevaciones de los marcos arriostrados.
    'S5.30': {
        '2': 'VERT. BRACE ELEVATION - GRID 3: elevacion del marco arriostrado en el '
             'eje 3. Rotula "HSS4x4x1/4" y "HSS5x5x1/4" como diagonales, "COL. REF. '
             'PLAN", "BM REF. PLAN" y "BRACE FRAME FORCES ARE ULTIMATE". Div 05 12 00: '
             'lo fabrica y monta el acerero. Impacto en lo nuestro: ninguno en '
             'cantidad. El stud de 6" del muro exterior y el de 3 5/8" del interior '
             'corren a 16" O.C. como metal corrido sin deducir, y la diagonal queda '
             'dentro del cavity; el recorte de stud en la diagonal no agrega material, '
             'solo mano de obra, y se declara en Clarifications.',
        '3': 'VERT. BRACE ELEVATION - GRID 8: mismo marco arriostrado en el eje 8, '
             'mismas diagonales HSS y mismas fuerzas ultimas. Div 05 12 00.',
        '4': 'VERT. BRACE ELEVATION - GRID A: "HSS5x5x1/4" entre columna y viga de '
             'plano, con los nodos 1A/1C/1D de S5.30. Div 05 12 00.',
        '5': 'VERT. BRACE ELEVATION - GRID G: mismo caso que 4, en el eje G. '
             'Div 05 12 00.',
        '6': 'VERT. BRACE ELEVATION - GRID B: mismo caso, en el eje B. Div 05 12 00.',
    },
}


class CalloutSinUsar(Exception):
    pass


def burbujas_de_planta(ws):
    """[(etiqueta, hoja_destino)] de las burbujas de seccion/detalle de una hoja."""
    out = set()
    for w in ws:
        if not HOJA_BURB.match(w['text'].strip()):
            continue
        cx = (w['x0'] + w['x1']) / 2
        for e in ws:
            t = e['text'].strip()
            if not ETIQ.match(t):
                continue
            dy = w['top'] - e['top']
            dx = abs((e['x0'] + e['x1']) / 2 - cx)
            if 3 < dy < 26 and dx < 22:
                out.add((t, norm(w['text'])))
    return sorted(out)


def universo(pdf_path=PDF):
    """{hoja_destino: {etiquetas}} que las hojas de PLANTA senalan. Cacheado."""
    st = os.stat(pdf_path)
    sello = [st.st_size, int(st.st_mtime)]
    if os.path.exists(CACHE):
        d = json.load(open(CACHE, encoding='utf-8'))
        if d.get('pdf') == sello and 'origen' in d:
            return {h: set(v) for h, v in d['callouts'].items()}
    # Por pdftotext, no pdfplumber: en las hojas de planta pdfplumber tarda MINUTOS cada una
    # y una compuerta que tarda minutos no se corre (misma leccion que el cache de detalles).
    import cache_detalles as C
    out = collections.defaultdict(set)
    origen = collections.defaultdict(set)
    for i in range(95):
        ws = C.palabras_rapidas(i)
        rot = VD.rotulo_de(ws, 3024.0, 2160.0)
        if not _es_fuente(rot):
            continue
        rotn = norm(rot) if rot else rot
        for etiq, hoja in burbujas_de_planta(ws):
            if hoja != rotn:                         # una burbuja apunta a OTRA hoja
                out[hoja].add(etiq)
                origen['%s/%s' % (etiq, hoja)].add(rot)
    out['_origen'] = {k: sorted(v) for k, v in origen.items()}
    org = out.pop('_origen', {})
    json.dump({'pdf': sello, 'callouts': {h: sorted(v) for h, v in out.items()},
               'origen': org}, open(CACHE, 'w', encoding='utf-8'))
    return dict(out)


def origen_de(cita):
    """En que hoja(s) esta dibujada la burbuja que llama a `cita` (p.ej. '7/A09.26')."""
    if not os.path.exists(CACHE):
        return []
    return json.load(open(CACHE, encoding='utf-8')).get('origen', {}).get(cita, [])


def citados():
    """{hoja: {etiquetas}} que los cierres sellados citan, en forma N/HOJA."""
    cit = collections.defaultdict(set)
    import cadena_detalles as _CD   # la compuerta y la cadena usan el MISMO lector de citas
    # BUG CORREGIDO 3-oct-2026: el glob '*_cierre*.json' solo veia los cierres que se
    # guardan agrupados (EXT_cierres.json, G_cierres_v2.json...) y NO los que se guardan
    # uno por muro (out/B2/B2_v2_muro_25.json, out/A1/..., out/C1/...). La compuerta daba
    # por NO CITADOS detalles que si estaban citados -- 11/A12.04 y 7/A12.04 viven en el
    # afirmar_alcance del muro 30 desde hace dias. Ahora se pregunta a resumen_global, que
    # es el unico que sabe donde vive cada cierre sellado del proyecto.
    import resumen_global as _RG
    archivos = []
    for _n, pats in _RG.SRC.items():
        for pat in pats:
            archivos += sorted(glob.glob(pat))
    archivos += sorted(glob.glob(f'{_TW}/*_cierre*.json'))
    for f in sorted(set(archivos)):
        txt = open(f, encoding='utf-8').read()
        for n, h in _CD._citas(txt):
            cit[norm(h)].add(n)
    return dict(cit)


def verificar():
    uni, cit = universo(), citados()
    faltan = []
    for h in sorted(uni):
        sin = sorted(uni[h] - cit.get(h, set()) - set(NO_APLICAN.get(h, ())))
        if sin:
            faltan.append((h, sin, sorted(cit.get(h, set()))))
    return faltan, uni, cit


def exigir():
    f, _u, _c = verificar()
    if f:
        raise CalloutSinUsar(
            'el PLANO senala %d detalle(s) que ningun cierre usa ni declara:\n  - %s'
            % (sum(len(s) for _h, s, _c in f),
               '\n  - '.join('%s: %s' % (h, ', '.join(s)) for h, s, _c in f)))
    return True


if __name__ == '__main__':
    f, uni, cit = verificar()
    print('burbujas que las hojas de planta senalan: %d en %d hoja(s)'
          % (sum(len(v) for v in uni.values()), len(uni)))
    for h in sorted(uni):
        print('   %-8s senala %-28s citados: %s'
              % (_CD.real(h), ','.join(sorted(uni[h])), ','.join(sorted(cit.get(h, set()))) or '-'))
    if f:
        print('\n*** SIN USAR NI DECLARAR (%d):' % sum(len(s) for _h, s, _c in f))
        for h, sin, _c in f:
            print('   %-8s %s' % (h, ', '.join(sin)))
        sys.exit(1)
    print('\nOK: todo detalle que el plano senala esta usado o declarado')
