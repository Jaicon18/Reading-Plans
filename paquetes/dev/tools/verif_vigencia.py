# -*- coding: utf-8 -*-
"""verif_vigencia.py -- COMPUERTA DE VIGENCIA DEL ENTREGABLE.

Origen del error que esta compuerta impide (2026-09-28):
    Se corrige un cierre (zonas humedas, ancho de FRP, altura de un muro) y la
    correccion queda sellada en su *_cierres.json, pero el Excel se quedo como estaba.
    El sello dice OK, el cierre dice OK, el resumen dice 77/77 -- y el unico papel que
    alguien usa para comprar material esta equivocado. Un cierre corregido que no llega
    al Excel NO EXISTE para quien compra.

Regla que impone:
    Ningun cambio esta terminado hasta que el Excel se regenera. Y no basta con decir
    que se regenero: hay que poder PROBARLO.

Como lo prueba:
    Al guardar el libro, excel.py llama sellar() y se escribe un manifiesto al lado del
    .xlsx con el sha256 de CADA insumo (los cierres sellados Y el codigo que los
    convierte en libro -- si se arregla un bug en dataset.py el libro tambien quedo
    viejo). verificar() vuelve a calcular esos hashes y los compara. Cualquier insumo
    cambiado, agregado, borrado, o el propio .xlsx tocado a mano, y el libro se declara
    DESACTUALIZADO. mtime no basta: copiar un archivo o hacerle touch lo falsea; el
    hash no.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (antes fijas en /home/claude/boa)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", "/home/claude/boa")
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import os, sys, json, glob, time, hashlib, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
B = f'{_TW}'
T = os.path.dirname(os.path.abspath(__file__))
LIBRO = B + '/out/BOA_Broomfield_Takeoff.xlsx'


class LibroDesactualizado(Exception):
    """El entregable no refleja el estado sellado del proyecto."""


# CODIGO QUE FABRICA EL LIBRO. Va en el manifiesto junto con los datos: un cambio aqui
# (un divisor de compra, una columna, el parser de alturas) cambia los numeros del libro
# aunque ningun cierre se haya tocado.
CODIGO = ['dataset.py', 'excel.py', 'closer.py', 'verif_columnas.py', 'verif_libro.py',
          'resumen_global.py']


def fuentes():
    """Todo insumo del libro, por las MISMAS rutas que usa el generador.

    No se usa un glob suelto del directorio: ahi viven archivos que el libro no lee
    (MEP_cruces.json, inventario.json, versiones viejas como G_cierres.json frente a
    G_cierres_v2.json). Un glob los incluiria y la compuerta gritaria por cosas que no
    afectan el entregable. Se pregunta al generador cuales lee de verdad.
    """
    import resumen_global as RG
    out = []
    for _grupo, patrones in RG.SRC.items():          # cierres de MURO
        for p in patrones:
            out.extend(sorted(glob.glob(p)))
    for f in ('CIELOS_cierres.json', 'SOFFITS_cierres.json', 'CANOPY_cierres.json',
              'MEP_cierre.json', 'HUECOS_cierre.json', 'PUNTOS345_cierres.json',
              'HUMEDAS_cierres.json',
              'MWBLOCKING_cierres.json'):           # superficies y otros bloques
        p = os.path.join(B, f)
        if os.path.exists(p):
            out.append(p)
    for f in CODIGO:                                 # el codigo tambien es insumo
        p = os.path.join(T, f)
        if os.path.exists(p):
            out.append(p)
    return sorted(set(out))


# Cierres que EXISTEN en el directorio pero el libro NO lee, cada uno con el motivo.
# Sin esta lista explicita, sellar un bloque nuevo y olvidar conectarlo a dataset.py deja
# el material fuera del Excel sin que nada se queje -- exactamente el error que esta
# compuerta persigue. Un cierre que no este aqui ni en fuentes() es HUERFANO y falla.
SUPERADOS = {
    'G_cierres.json':  'reemplazado por G_cierres_v2.json (resumen_global.SRC lee el v2)',
    'G52_cierre.json': 'reemplazado por G52_cierre_v2.json (resumen_global.SRC lee el v2)',
}
NO_SON_CIERRES = {
    'CIELOS_perimetro.json': 'geometria de apoyo, no lleva partidas',
    'ADYACENCIA.json': 'mapa de que wall muere contra cual, salida de adyacencia.py. Es geometria de apoyo para unificar el criterio de studs adicionales bajo 5/S5.20, no lleva partidas y por eso el Excel no lo lee. Mientras resuelva solo el 31% de los extremos NO se usa para recontar: lo que prueba (-38 studs en los 47 walls de banda simple) va declarado en Clarifications como piso medido del sobre-conteo, no aplicado a ninguna cantidad sellada.',
    'MEP_cruces.json':       'insumo de cerrar_mep.py, no es cierre sellado',
    'bandas_por_tipo.json':  'control del barrido de tags',
    'bandas_restantes.json': 'control del barrido de tags',
    'inventario.json':       'mapa de hojas del PDF',
    'detalles_cache.json':   'cache de verif_detalles: que detalle vive en que hoja',
    'titulos_cache.json':    'cache de titulos_detalles: el rotulo de cada detalle',
    'callouts_cache.json':   'cache de verif_callouts: que burbuja de seccion/detalle dibuja '
                             'cada hoja de planta. Es un indice del PDF, no un cierre.',
    'rotulos_detalle_cache.json': 'cache de verif_citas: que NUMEROS de detalle rotula cada '
                             'hoja, leidos de los propios rotulos del PDF. Sirve para probar '
                             'que una cita existe; no aporta ninguna cantidad y se reconstruye '
                             'solo con verif_citas.rotulos_de_detalle(rehacer=True).',
    'titulos_detalle_cache.json': 'cache de titulo_cita: el TITULO de cada detalle de cada hoja, '
                             'para comprobar que la cita de una partida es del tema correcto. '
                             'Indice del PDF, no cierre; se reconstruye con titulo_cita.titulos().',
    'grafo_callouts.json':   'cache de cadena_detalles: el GRAFO de que hoja senala a que hoja, '
                             'barrido del PDF con el mismo detector de burbujas de la '
                             'compuerta. Solo ORDENA citas que los cierres ya tienen -- no '
                             'aporta ninguna cantidad, y si se borra se reconstruye solo.',
    'numeros_antes.json':    'foto de verif_numeros: todos los numeros ANTES de traducir, '
                             'para probar que la traduccion al ingles no movio ninguna '
                             'cantidad. Es un control, no una fuente de cantidades.',
}


def huerfanos():
    """Cierres sellados que el Excel no lee y que nadie declaro como superados."""
    conocidos = {os.path.basename(p) for p in fuentes()}
    out = []
    for p in sorted(glob.glob(os.path.join(B, '*.json'))):
        n = os.path.basename(p)
        if n in conocidos or n in SUPERADOS or n in NO_SON_CIERRES:
            continue
        out.append(n)
    return out


def _sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 16), b''):
            h.update(b)
    return h.hexdigest()


def _mf_path(xlsx):
    return os.path.splitext(xlsx)[0] + '.manifiesto.json'


def sellar(xlsx=LIBRO):
    """Escribe el manifiesto. Lo llama excel.py INMEDIATAMENTE despues de wb.save()."""
    mf = {'libro': os.path.basename(xlsx),
          'libro_sha': _sha(xlsx),
          'generado': time.strftime('%Y-%m-%d %H:%M:%S'),
          'fuentes': {os.path.relpath(p, B): _sha(p) for p in fuentes()}}
    with open(_mf_path(xlsx), 'w', encoding='utf-8') as fh:
        json.dump(mf, fh, indent=1, ensure_ascii=False, sort_keys=True)
    return mf


def verificar(xlsx=LIBRO):
    """Lista de problemas. Vacia = el libro entregable es el estado sellado de hoy."""
    fallas = []
    if not os.path.exists(xlsx):
        return ['el libro no existe: ' + xlsx]
    mf_p = _mf_path(xlsx)
    if not os.path.exists(mf_p):
        return ['el libro no tiene manifiesto: no hay manera de probar que esta al dia. '
                'Corre tools/excel.py']
    mf = json.load(open(mf_p, encoding='utf-8'))

    if mf.get('libro_sha') != _sha(xlsx):
        fallas.append('el .xlsx se modifico despues de generarse (a mano o por otra '
                      'herramienta): lo que se entrega ya no es lo que el generador produjo')

    viejas = mf.get('fuentes', {})
    hoy = {os.path.relpath(p, B): p for p in fuentes()}

    for rel in sorted(set(hoy) - set(viejas)):
        fallas.append('INSUMO NUEVO que no entro al libro: %s (se cerro algo despues de '
                      'generar el Excel)' % rel)
    for rel in sorted(set(viejas) - set(hoy)):
        fallas.append('INSUMO QUE DESAPARECIO desde que se genero el libro: %s' % rel)
    for n in huerfanos():
        fallas.append('CIERRE HUERFANO: %s esta sellado pero el Excel no lo lee. '
                      'Conectalo en dataset.py/resumen_global.py o declaralo en '
                      'verif_vigencia.SUPERADOS con su motivo' % n)
    for rel in sorted(set(viejas) & set(hoy)):
        if _sha(hoy[rel]) != viejas[rel]:
            que = 'codigo generador' if rel.startswith('tools/') else 'cierre sellado'
            fallas.append('CAMBIO DESPUES DE GENERAR EL LIBRO (%s): %s -- la correccion '
                          'esta sellada pero NO esta en el Excel' % (que, rel))
    return fallas


def exigir(xlsx=LIBRO):
    """Levanta si el entregable no esta al dia. Usar antes de mandar o copiar el libro."""
    f = verificar(xlsx)
    if f:
        raise LibroDesactualizado('EL EXCEL NO ESTA AL DIA -- no se entrega:\n  - ' +
                                  '\n  - '.join(f))
    return True


if __name__ == '__main__':
    x = sys.argv[1] if len(sys.argv) > 1 else LIBRO
    fs = verificar(x)
    if fs:
        print('*** LIBRO DESACTUALIZADO (%d):' % len(fs))
        for s in fs:
            print('  -', s)
        sys.exit(1)
    mf = json.load(open(_mf_path(x), encoding='utf-8'))
    print('vigencia OK: el Excel refleja los %d insumos sellados (generado %s)'
          % (len(mf['fuentes']), mf['generado']))
