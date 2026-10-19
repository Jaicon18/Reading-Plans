# -*- coding: utf-8 -*-
"""verif_citas.py -- COMPUERTA: toda cita N/HOJA que ESCRIBE el take-off existe de verdad.

QUE LA ORIGINO (5-oct-2026, verificando el muro A1 #8 paso a paso con Rodolfo).
El bracing de TODOS los muros se citaba como "5/F de S5.20". En S5.20 el detalle 5 es
`TYPICAL WALL FRAMING CONNX`; el sub-detalle `F. BRIDGING AND BRACING - CONTINUOUS BRIDGING`
esta dentro del detalle 1 `TYPICAL WALL FRAMING DETAILS`. La cita mandaba al estimador y al
revisor a un detalle que no dice nada de bracing. 73 archivos la arrastraban.

verif_callouts mira el sentido PLANO -> take-off (todo detalle senalado se usa).
Esta mira el sentido contrario, take-off -> hoja: todo numero que yo escribo tiene que
existir como rotulo de detalle en esa hoja. Son compuertas distintas y las dos hacen falta.

COMO SABE QUE DETALLES EXISTEN. No por el grafo de burbujas (una burbuja puede faltar), sino
por los ROTULOS DE DETALLE de la propia hoja: renglon con numero + titulo en mayusculas +
escala (NTS, 3" = 1'-0", 1/4" = 1'-0"...).  Es el mismo renglon que lee un humano.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (antes fijas en /home/claude/boa)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", "/home/claude/boa")
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import os, sys, re, json, glob, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cadena_detalles as CD

PDF = f'{_TW}/BOA_SIN_MARKUPS.pdf'
CACHE = f'{_TW}/rotulos_detalle_cache.json'
ESCALA = re.compile(r'\bNTS\b|\d\s*(?:\d/\d)?\s*"\s*=\s*\d', re.I)
NUM = re.compile(r'^\d{1,2}$')

# Citas que NO son detalles de hoja y por eso no se buscan en ningun rotulo.
# Cada una con su motivo, leido de la propia fuente.
NO_SON_DETALLE = {
    '9/A00.41': ('No es cita del take-off: es la referencia TEXTUAL del propio plano. '
                 'CONSTRUCTION KEY NOTE 1 de A02.01: "TACTILE EXIT SIGNAGE. SEE 9/A00.41". '
                 'Se transcribe tal cual, no se inventa.'),
}

# Citas que el lector NO encuentra pero que SI existen, comprobadas a ojo en la hoja.
# Cada una lleva la evidencia; sin evidencia escrita no entra aqui.
VERIFICADAS = {
    '6/A11.01': ('Comprobado a 600 dpi el 5-oct-2026 (recorte x 400-1100, y 1530-1600 de la '
                 'pagina 46): la hoja SI rotula la vineta 6 sobre A11.01, titulo "OFFICE 2 - '
                 'SOUTH", escala 1/2" = 1\'-0". El lector no la saca porque el rotulo de hoja '
                 'bajo esa burbuja no se extrae como palabra suelta.'),
}


def de_pagina(ws, rot):
    """Numeros de detalle rotulados en UNA pagina.  Dos formatos conviven en el mismo set:

      serie A  burbuja = numero ARRIBA del rotulo de la hoja, titulo a la derecha, escala debajo
               (A09.25:  '4' sobre 'A09.25', titulo 'DETAIL @ DOOR JAMB', escala 1 1/2" = 1'-0")
      serie S  burbuja = numero + titulo + escala en el MISMO renglon, sin rotulo de hoja debajo
               (S5.20:  '1 TYPICAL WALL FRAMING DETAILS   NTS')

    Un solo detector deja fuera la mitad de las hojas, asi que se corren los dos y se unen.
    """
    out = set()
    # formato serie A: numero encima del rotulo de la hoja
    hojas = [w for w in ws if w['text'].strip() == rot]
    nums = [w for w in ws if NUM.match(w['text'].strip())]
    for h in hojas:
        for n in nums:
            dy = h['top'] - n['top']
            dx = abs((h['x0'] + h['x1']) / 2.0 - (n['x0'] + n['x1']) / 2.0)
            if 4 < dy < 30 and dx < 22:
                out.add(int(n['text']))
    # formato serie S: numero + titulo + escala en el mismo renglon
    filas = collections.defaultdict(list)
    for w in ws:
        filas[round(w['top'] / 6)].append(w)
    for g in filas.values():
        g = sorted(g, key=lambda w: w['x0'])
        if not ESCALA.search(' '.join(w['text'] for w in g)):
            continue
        for j, w in enumerate(g):
            if not NUM.match(w['text'].strip()):
                continue
            tit = ' '.join(x['text'] for x in g[j + 1:] if x['x0'] - w['x1'] < 500)[:60]
            if sum(1 for c in tit if c.isupper()) >= 6:
                out.add(int(w['text']))
    return out


def rotulos_de_detalle(rehacer=False):
    """{hoja REAL: set(numeros de detalle que la hoja rotula)}."""
    if os.path.exists(CACHE) and not rehacer:
        return {h: set(v) for h, v in json.load(open(CACHE, encoding='utf-8')).items()}
    import pdfplumber, warnings
    warnings.filterwarnings('ignore')
    out = collections.defaultdict(set)
    cache = json.load(open(CD.CACHE, encoding='utf-8'))
    with pdfplumber.open(PDF) as pdf:
        for i, pg in cache['paginas'].items():
            rot = (pg.get('rotulo') or '').strip()
            if rot:
                out[rot] |= de_pagina(pdf.pages[int(i)].extract_words(x_tolerance=1.5) or [], rot)
    json.dump({h: sorted(v) for h, v in out.items()}, open(CACHE, 'w', encoding='utf-8'), indent=0)
    return {h: set(v) for h, v in out.items()}


def citas_del_takeoff():
    """[(cita, archivo)] de todo cierre sellado y de las herramientas que lo generan."""
    import resumen_global as RG
    fuentes = []
    for pats in RG.SRC.values():
        for p in pats:
            fuentes += glob.glob(p)
    fuentes += glob.glob(f'{_TW}/tools/cerrar_*.py')
    out = []
    for p in sorted(set(fuentes)):
        try:
            s = open(p, encoding='utf-8').read()
        except Exception:
            continue
        for n, h in CD._citas(s):
            if n.isdigit():
                out.append((('%s/%s' % (n, h)), p))
    return out


def verificar():
    real = rotulos_de_detalle()
    malas = collections.defaultdict(set)
    for cita, p in citas_del_takeoff():
        if cita in NO_SON_DETALLE or cita in VERIFICADAS:
            continue
        n, h = cita.split('/')
        hr = CD.real(h)
        tiene = real.get(hr) or real.get(h)
        if tiene is None:          # hoja sin rotulos detectados: no se puede juzgar
            continue
        if int(n) not in tiene:
            malas[cita].add(os.path.basename(p))
    return malas, real


def main():
    malas, real = verificar()
    if not malas:
        print('OK: toda cita N/HOJA del take-off existe como detalle rotulado en esa hoja')
        return 0
    print('CITAS QUE NO EXISTEN EN SU HOJA:')
    for cita in sorted(malas):
        h = cita.split('/')[1]
        hay = sorted(real.get(CD.real(h)) or real.get(h) or [])
        print('  %-12s  la hoja %s solo rotula %s' % (cita, CD.real(h), hay))
        for f in sorted(malas[cita])[:6]:
            print('       <- %s' % f)
    return 1


if __name__ == '__main__':
    sys.exit(main())
