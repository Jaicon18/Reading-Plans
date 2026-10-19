# -*- coding: utf-8 -*-
"""verif_callouts.py -- COMPUERTA: el detalle que el plano SENALA se usa, siempre.

Orden de Rodolfo, 2-oct-2026: "siempre se tiene que usar los detalles que marcan los planos
ya que ahi esta la informacion que se necesita, nunca saltarse esta regla."

QUE LA ORIGINO. La marquesina de una fachada se cerro con geometria medida
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
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (por defecto, el directorio actual)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", _os_rutas.getcwd())
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


# Hojas de PLANTA del set (forma canonica, sin cero). Default = numeracion AIA usual (floor plan,
# roof plan, RCP, enlarged plans); el set real se declara en $TAKEOFF_PLANTAS ("A2.01,A4.01,...").
PLANTAS = tuple(x.strip() for x in (_os_rutas.environ.get('TAKEOFF_PLANTAS') or 'A2.01,A2.02,A4.01,A8.01').split(',')
                if x.strip())
# Series donde viven los detalles a los que las plantas remiten, tambien canonicas.
DETALLES = ('A9.', 'A12.', 'A11.', 'S5.', 'S3.', 'S2.')


def _es_fuente(rot):
    """True si de esa hoja NACEN burbujas que hay que seguir: plantas y hojas de detalle."""
    if not rot:
        return False
    r = norm(rot)
    return r in PLANTAS or any(r.startswith(p) for p in DETALLES)


# hoja -> {etiqueta: motivo}. Se declara MIRANDO el detalle, nunca para callar la
# compuerta. Cada motivo dice QUE se leyo en ese detalle y por que no deja partida.
# Es DATO DEL PROYECTO (E24): vive en $TAKEOFF_WORK/callouts_no_aplican.json, no aqui.
def _no_aplican():
    try:
        d = json.load(open(os.path.join(_TW, 'callouts_no_aplican.json'), encoding='utf-8'))
        return {h: dict(v) for h, v in d.items()}
    except (OSError, ValueError, TypeError, AttributeError):
        return {}


NO_APLICAN = _no_aplican()


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
