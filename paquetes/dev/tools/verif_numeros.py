# -*- coding: utf-8 -*-
"""verif_numeros.py -- prueba que una traduccion NO movio ninguna cantidad.

Traducir 687 frases dentro de 21 generadores toca los mismos archivos que producen los
numeros. La unica forma de traducir sin miedo es poder DEMOSTRAR que ningun numero cambio.

Metodo (el mismo que ya probo `traducir_materiales.py`, elevado a todo el proyecto): se
fotografia CADA numero de CADA cierre sellado por su RUTA dentro del JSON, se traduce, se
vuelven a generar los cierres, y se compara ruta por ruta. Una ruta que cambia de valor, o
que aparece o desaparece, para la entrega.

No compara textos: los textos SI tienen que cambiar. Compara solo numeros.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (antes fijas en /home/claude/boa)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", "/home/claude/boa")
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import os, sys, json, glob

B = f'{_TW}'
FOTO = os.path.join(B, 'numeros_antes.json')


def numeros(d, ruta=''):
    """{ruta: valor} de todos los numeros del JSON, por su ruta exacta."""
    out = {}
    if isinstance(d, dict):
        for k, v in d.items():
            out.update(numeros(v, ruta + '/' + str(k)))
    elif isinstance(d, list):
        for i, v in enumerate(d):
            out.update(numeros(v, ruta + '[%d]' % i))
    elif isinstance(d, bool):
        pass
    elif isinstance(d, (int, float)):
        out[ruta] = round(float(d), 6)
    return out


def _todos():
    out = {}
    for f in sorted(glob.glob(B + '/*_cierre*.json')):
        out[os.path.basename(f)] = numeros(json.load(open(f, encoding='utf-8')))
    return out


def fotografiar(dest=FOTO):
    t = _todos()
    json.dump(t, open(dest, 'w', encoding='utf-8'))
    print('foto de %d archivos, %d numeros -> %s'
          % (len(t), sum(len(v) for v in t.values()), dest))
    return t


def comparar(foto=FOTO):
    """[] si ningun numero se movio; si no, la lista de diferencias."""
    if not os.path.exists(foto):
        raise RuntimeError('no hay foto previa: corre fotografiar() ANTES de traducir')
    antes = json.load(open(foto, encoding='utf-8'))
    ahora = _todos()
    fallas = []
    # El SELLO cambia a proposito cuando cambia el texto: no es una cantidad.
    def limpio(d):
        return {k: v for k, v in d.items() if not k.endswith('/sello')}
    for f in sorted(set(antes) | set(ahora)):
        a, b = limpio(antes.get(f, {})), limpio(ahora.get(f, {}))
        for r in sorted(set(a) | set(b)):
            if r not in a:
                fallas.append('%s %s: APARECIO un numero (%s)' % (f, r, b[r]))
            elif r not in b:
                fallas.append('%s %s: DESAPARECIO un numero (%s)' % (f, r, a[r]))
            elif abs(a[r] - b[r]) > 1e-6:
                fallas.append('%s %s: %s -> %s' % (f, r, a[r], b[r]))
    return fallas


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'foto':
        fotografiar()
    else:
        fs = comparar()
        if fs:
            print('*** LA TRADUCCION MOVIO %d NUMERO(S):' % len(fs))
            for s in fs[:25]:
                print('   ', s)
            sys.exit(1)
        print('OK: ningun numero se movio')
