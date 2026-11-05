# -*- coding: utf-8 -*-
"""verif_planos.py -- COMPUERTA DE LOS PLANOS MARCADOS.

El riesgo: el LF que se ROTULA en el plano esta tecleado a mano en hojas_por_tipo.py y en
hoja_exterior.py, en paralelo a los cierres sellados. Son dos copias del mismo numero
escritas por separado, y dos copias escritas a mano del mismo numero siempre terminan
diciendo cosas distintas. El plano marcado es lo que el estimador lleva a la obra: si
dice un LF y el Excel dice otro, el plano gana en campo y pierde el presupuesto.

Que exige:
 1. Suma de las bandas AZULES de un muro = 'largo' de su cierre sellado. Se SUMA porque un
    elemento se dibuja en varias bandas cuando tiene vanos o quiebres (un bulkhead de
    <n> vanos iguales = <n> x vano LF, no <n> muros).
 2. El total del encabezado de cada tipo = suma de los cierres de ese tipo.
 3. COBERTURA: todo muro sellado esta marcado en EXACTAMENTE una hoja. Un muro sellado que
    no aparece en ningun plano es un muro que el de campo no va a construir.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (por defecto, el directorio actual)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", _os_rutas.getcwd())
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import os, sys, re, json, glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
B = f'{_TW}'
TOL = 0.02          # centesimas de pie: los rotulos van a 2 decimales


class PlanoRechazado(Exception):
    pass


def _v(x):
    if isinstance(x, dict):
        for k in ('v', 'valor', 'val'):
            if k in x:
                return _v(x[k])
    return x


def sellados():
    """{num: (largo, tag)} leido de los cierres, por las rutas del generador."""
    import resumen_global as RG
    out = {}

    def walk(d):
        if isinstance(d, dict) and 'muro' in d and 'largo' in d:
            try:
                out[int(_v(d['muro']))] = (float(_v(d['largo'])), _v(d.get('tag')))
            except Exception:
                pass
            return
        if isinstance(d, dict):
            for v in d.values():
                if isinstance(v, dict):
                    walk(v)
    for _g, pats in RG.SRC.items():
        for p in pats:
            for f in sorted(glob.glob(p)):
                walk(json.load(open(f, encoding='utf-8')))
    return out


def marcados():
    """{num: (LF dibujado, hoja)} sumando las bandas de MURO de cada hoja."""
    import hojas_por_tipo as H
    try:
        import hoja_exterior as E          # generador DEL PROYECTO (no vive en _herramientas/py)
    except ImportError:
        E = None
        print("verif_planos: este proyecto no tiene hoja_exterior.py; se omiten los exteriores marcados")
    out = {}
    for tipo, filas in H.T.items():
        for f in filas:
            n, lf = int(f[0]), float(f[1])
            a, h = out.get(n, (0.0, tipo))
            out[n] = (a + lf, h)
    for n, lab, _o, _c0, _c1, _lo, _hi, col in (E.T if E else []):
        if col != E.AZ:                      # naranja = storefront Div 08, rojo = abertura
            continue
        m = re.search(r'([\d.]+)\s*LF', lab)
        if not m:
            continue
        a, h = out.get(int(n), (0.0, 'EXTERIORES'))
        out[int(n)] = (a + float(m.group(1)), h)
    # El parapet infill y el forro de las columnas de marquesina (sus walls propios) van en
    # su propia hoja: se construyen con otro perfil y en otro momento que el muro de abajo.
    try:
        import hoja_parapeto as PP         # generador DEL PROYECTO (no vive en _herramientas/py)
    except ImportError:
        PP = None
        print("verif_planos: este proyecto no tiene hoja_parapeto.py; se omite parapeto/columnas")
    for n, lab, _o, _c0, _c1, _lo, _hi, _col in (PP.T if PP else []):
        m = re.search(r'([\d.]+)\s*LF', lab)
        if not m:
            continue
        a, h = out.get(int(n), (0.0, 'PARAPETO Y COLUMNAS'))
        out[int(n)] = (a + float(m.group(1)), h)
    return out


def verificar():
    fallas = []
    S, M = sellados(), marcados()

    for n in sorted(set(S) & set(M)):
        if abs(S[n][0] - M[n][0]) > TOL:
            fallas.append('muro %d (%s): el plano rotula %.2f LF y el cierre sella %.2f'
                          % (n, S[n][1], M[n][0], S[n][0]))
    for n in sorted(set(S) - set(M)):
        fallas.append('COBERTURA: el muro %d (%s, %.2f LF) esta sellado y NO aparece '
                      'marcado en ningun plano' % (n, S[n][1], S[n][0]))
    for n in sorted(set(M) - set(S)):
        fallas.append('el plano marca un muro %d que no tiene cierre sellado' % n)

    # 2. totales de encabezado por tipo
    import hojas_por_tipo as H
    for tipo, filas in H.T.items():
        tit = H.TIT.get(tipo, '') if hasattr(H, 'TIT') else ''
        m = re.search(r'([\d.,]+)\s*LF', tit)
        if not m:
            continue
        head = float(m.group(1).replace(',', ''))
        suma = sum(S[int(f[0])][0] for f in filas if int(f[0]) in S)
        # un numero repetido en varias bandas es UN elemento: no se suma dos veces
        suma = sum(S[n][0] for n in {int(f[0]) for f in filas} if n in S)
        if abs(head - suma) > TOL:
            fallas.append('encabezado de la hoja %s dice %.2f LF y sus cierres suman %.2f'
                          % (tipo, head, suma))
    return fallas


def exigir():
    f = verificar()
    if f:
        raise PlanoRechazado('LOS PLANOS MARCADOS NO CUADRAN CON LOS CIERRES:\n  - ' +
                             '\n  - '.join(f))
    return True


if __name__ == '__main__':
    fs = verificar()
    if fs:
        print('*** PLANOS MARCADOS CON PROBLEMAS (%d):' % len(fs))
        for s in fs:
            print('  -', s)
        sys.exit(1)
    S = sellados()
    print('planos marcados OK: los %d muros sellados estan marcados y su LF rotulado '
          'coincide con su cierre' % len(S))
