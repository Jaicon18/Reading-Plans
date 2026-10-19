# -*- coding: utf-8 -*-
"""traducir_materiales.py -- pasa a INGLES los nombres de material de los cierres SELLADOS.

No se edita un cierre a mano. Se aplica el glosario, se VERIFICA partida por partida que
ningun valor numerico se movio, y se recalcula el sello con la misma funcion del closer --
el mismo procedimiento de resellar_b2k.py, que es el unico seguro para tocar un cierre ya
sellado.

Si un solo numero cambia, no se escribe nada.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (antes fijas en /home/claude/boa)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", "/home/claude/boa")
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import os, sys, json, glob, copy, hashlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glosario as G
import resumen_global as RG

B = f'{_TW}'
EXTRA = ['CIELOS_cierres.json', 'SOFFITS_cierres.json', 'CANOPY_cierres.json',
         'MEP_cierre.json', 'HUECOS_cierre.json', 'PUNTOS345_cierres.json',
         'HUMEDAS_cierres.json']


def sello(x):
    d2 = {k: v for k, v in x.items() if k != 'sello'}
    return hashlib.sha256(json.dumps(d2, sort_keys=True, ensure_ascii=False)
                          .encode()).hexdigest()[:16]


def numeros(o, ruta='', out=None):
    """TODOS los numeros del objeto, con su ruta, para probar que nada se movio."""
    if out is None:
        out = {}
    if isinstance(o, dict):
        for k, v in o.items():
            numeros(v, ruta + '/' + str(k), out)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            numeros(v, ruta + '/%d' % i, out)
    elif isinstance(o, (int, float)) and not isinstance(o, bool):
        out[ruta] = o
    return out


def rec(o):
    """Traduce SOLO las cadenas. Nunca toca el campo 'sello' ni un numero."""
    if isinstance(o, dict):
        return {k: (o[k] if k == 'sello' else rec(o[k])) for k in o}
    if isinstance(o, list):
        return [rec(v) for v in o]
    if isinstance(o, str):
        return G.traducir(o)
    return o


def archivos():
    fs = []
    for pats in RG.SRC.values():
        for p in pats:
            fs.extend(sorted(glob.glob(p)))
    fs += [os.path.join(B, f) for f in EXTRA if os.path.exists(os.path.join(B, f))]
    return sorted(set(fs))


def procesar(f, escribir=True):
    d = json.load(open(f, encoding='utf-8'))
    # un archivo puede traer UN cierre o VARIOS por llave
    unico = 'sello' in d
    bloques = {'_': d} if unico else {k: v for k, v in d.items() if isinstance(v, dict)}

    antes = numeros(d)
    nd = rec(copy.deepcopy(d))
    despues = numeros(nd)
    dif = {k: (antes[k], despues[k]) for k in antes if antes.get(k) != despues.get(k)}
    if dif:
        raise AssertionError('%s: la traduccion movio %d numero(s): %s'
                             % (os.path.basename(f), len(dif), list(dif.items())[:3]))
    if set(antes) != set(despues):
        raise AssertionError('%s: la traduccion agrego o quito numeros' % f)

    # resellar cada bloque que traiga sello
    n = 0
    if unico:
        if nd.get('sello'):
            nd['sello'] = sello(nd); n += 1
    else:
        for k, v in nd.items():
            if isinstance(v, dict) and v.get('sello'):
                v['sello'] = sello(v); n += 1
    cambio = json.dumps(d, sort_keys=True, ensure_ascii=False) != \
             json.dumps(nd, sort_keys=True, ensure_ascii=False)
    if escribir and cambio:
        json.dump(nd, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return cambio, n


def main(escribir=True):
    tot = cam = sel = 0
    for f in archivos():
        tot += 1
        c, n = procesar(f, escribir)
        cam += 1 if c else 0
        sel += n
    print('archivos revisados %d | con texto traducido %d | bloques resellados %d'
          % (tot, cam, sel))
    return tot, cam, sel


if __name__ == '__main__':
    main('--dry' not in sys.argv)
