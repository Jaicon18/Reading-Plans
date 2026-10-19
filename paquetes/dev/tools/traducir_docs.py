# -*- coding: utf-8 -*-
"""traducir_docs.py -- pasa a INGLES los terminos del trade en los DOCUMENTOS .md.

INSTRUCCION PERMANENTE DE RODOLFO, 7-oct-2026 (regla inviolable): todo nombre de material,
herramienta, componente, proceso, abreviatura y vocabulario tecnico de drywall y metal frame
va en INGLES; la prosa puede ir en espanol. `traducir_materiales.py` ya lo hace con los
CIERRES; esto lo hace con los documentos, que es donde quedaron 116 apariciones.

TRES SALVAGUARDAS, cada una por una forma distinta de romper un documento:

  1. NO SE TOCA LO QUE ESTA DENTRO DE UN BLOQUE DE CODIGO (``` ... ```) NI UN `inline code`.
     Ahi hay nombres de archivo, nombres de variable y comentarios COPIADOS del .py. Traducir
     un comentario copiado lo desincroniza del codigo real, y entonces el documento cita un
     codigo que no existe. Un documento que miente sobre el codigo es peor que uno en espanol.

  2. NINGUN NUMERO SE MUEVE. Se extraen todos los numeros del documento antes y despues y
     tienen que ser identicos, en el mismo orden. Es la misma prueba de traducir_materiales:
     el glosario toca palabras, y si toco una cifra, no se escribe nada.

  3. LOS DOCUMENTOS CONGELADOS QUEDAN FUERA, con la misma categoria que ya usa verif_idioma:
     una version superada del skill o una adenda ya publicada existe para registrar que decia
     ESE dia. Reescribirla destruye justo lo que vino a guardar.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (por defecto, el directorio actual)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", _os_rutas.getcwd())
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import os, re, sys, glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glosario as G
import vocab_trade as V
import verif_idioma as VI

B = f'{_TW}'
ENTREGA = f'{_TO}/entrega'
# LAS DOS CARPETAS, por defecto. Varios .md viven copiados en la carpeta de entrega sin
# generador que los reescriba, asi que traducir solo el original dejaba la copia en espanol y
# la compuerta la seguia cazando -- y cazaba bien: la copia es la que se manda. Dos copias del
# mismo documento se desincronizan en cuanto se toca una sola.
CARPETAS = [B + '/*.md', ENTREGA + '/*.md']
NUM = re.compile(r'\d+(?:[.,]\d+)?')
# bloque cercado ```...``` y codigo en linea `...`
CODIGO = re.compile(r'```.*?```|`[^`\n]*`', re.S)


def _trozos(t):
    """[(texto, es_codigo)] partiendo el documento en prosa y codigo."""
    out, i = [], 0
    for m in CODIGO.finditer(t):
        if m.start() > i:
            out.append((t[i:m.start()], False))
        out.append((m.group(0), True))
        i = m.end()
    if i < len(t):
        out.append((t[i:], False))
    return out


def traducir_doc(t):
    """Traduce la prosa y deja intactos el codigo y el bloque de glosario.

    El bloque marcado `<!-- GLOSARIO:INICIO/FIN -->` es la tabla espanol->ingles y las citas
    textuales de Rodolfo: un documento que DEFINE la regla tiene que poder escribir las
    palabras que prohibe, y una cita se reproduce como la dijo. Es la misma exencion que ya
    tiene la compuerta, y se respeta aqui para que las dos coincidan.
    """
    partes = []
    for bloque, es_glos in _glosario_fuera(t):
        if es_glos:
            partes.append(bloque)
        else:
            # DOS listas: glosario.py (nombres de material del entregable) y
            # vocab_trade.py (el vocabulario del trade en PROSA). Son distintas a
            # proposito: varias palabras de vocab_trade son CLAVES del cierre y no
            # pueden entrar al glosario sin romper la logica.
            partes.append(''.join(x if cod else V.traducir(G.traducir(x))
                                  for x, cod in _trozos(bloque)))
    return ''.join(partes)


def _glosario_fuera(t):
    """[(bloque, es_bloque_de_glosario)] usando los MISMOS marcadores de verif_idioma."""
    ini, fin = VI.INICIO, VI.FIN
    out, i = [], 0
    while True:
        a = t.find(ini, i)
        if a < 0:
            out.append((t[i:], False)); return out
        b = t.find(fin, a)
        if b < 0:
            out.append((t[i:], False)); return out
        out.append((t[i:a], False))
        out.append((t[a:b + len(fin)], True))
        i = b + len(fin)


def congelado(nombre):
    """Version congelada: se usa EL MISMO detector de la compuerta, nunca una copia.

    `verif_idioma.es_historico` ya define la categoria. Escribir aqui otra regexp parecida es
    el error que ya costo una entrega: un detector y un corrector que no normalizan igual
    dejan faltas que se reportan para siempre y nunca se arreglan -- o peor, se corrige un
    documento que la compuerta considera congelado.
    """
    return VI.es_historico(nombre)


def main(escribir=False, patrones=None):
    fs = sorted(set(sum([glob.glob(p) for p in (patrones or CARPETAS)], [])))
    tot = cam = 0
    for f in fs:
        n = os.path.basename(f)
        if congelado(n):
            continue
        tot += 1
        t = open(f, encoding='utf-8').read()
        nt = traducir_doc(t)
        if nt == t:
            continue
        a, b = NUM.findall(t), NUM.findall(nt)
        if a != b:
            print('*** %s: la traduccion movio numeros -- NO se escribe' % n)
            for x, y in zip(a, b):
                if x != y:
                    print('      %s -> %s' % (x, y)); break
            continue
        # LO QUE QUEDA DENTRO DE CODIGO SE REPORTA, NO SE CALLA. El corrector salta los
        # bloques de codigo a proposito (salvaguarda 1), y la compuerta NO los salta: si no
        # se dice lo que quedo ahi, esa falta se reporta para siempre y nunca se arregla
        # -- el mismo error que ya costo una entrega con `perfileria` / `perfilería`.
        # Se arregla a mano en el documento, o en el .py si el bloque es codigo copiado.
        dentro = sorted({w for x, cod in _trozos(nt) if cod for w in G.faltas(x)}
                        | {e for x, cod in _trozos(nt) if cod for e, _ in V.faltas(x)})
        cam += 1
        print('%-48s %s' % (n, 'escrito' if escribir else 'cambiaria')
              + ('   DENTRO DE CODIGO, a mano: %s' % dentro if dentro else ''))
        if escribir:
            open(f, 'w', encoding='utf-8').write(nt)
    print('documentos revisados %d | con termino traducido %d' % (tot, cam))
    return cam


if __name__ == '__main__':
    sys.exit(0 if main('--aplicar' in sys.argv) is not None else 1)
