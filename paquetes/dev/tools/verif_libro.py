# -*- coding: utf-8 -*-
"""verif_libro.py -- AUDITORIA DEL LIBRO YA ESCRITO.

verif_columnas.py revisa los DATOS antes de escribir. Esto revisa el ARCHIVO despues de
escribirlo, que es otra cosa: aqui se cazan los errores que solo existen en el Excel --
una formula que apunta a la columna de al lado, un rango que no llega a la ultima fila,
un criterio de SUMIFS que no coincide con ningun valor, un divisor de compra que no
corresponde a la familia del material, un renglon que no llega al resumen.

Se corre SIEMPRE despues de generar y despues de recalcular.

Hallazgos que originaron cada comprobacion (28-sep-2026):
  - el trim (corner bead, casing bead, shadow molding) salia SIN desperdicio estando
    clasificado como "accesorio", cuando es perfileria metalica cortada a medida
  - el bracing de 1-1/2" C.R. channel se convertia a piezas dividiendo entre el largo de
    TRACK (10 ft), cuando ese canal viene en 16 y 20 ft
  - el furring channel se dividia igual entre 10 ft, cuando viene en 12
  - el trim se dividia entre el largo de STUD (20 ft), cuando viene en 8 y 10
  - un PENDIENTE (RETORNO_BOARD_RANURA) salia como 0.00 y en el Excel ni aparecia
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (por defecto, el directorio actual)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", _os_rutas.getcwd())
_PRE = _os_rutas.environ.get("TAKEOFF_PREFIJO", "PROYECTO")  # prefijo de los archivos del proyecto
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import re, sys, os
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter as CL

# familia del material -> como se reconoce por el nombre del renglon
METAL = ('stud', 'track', 'channel', 'bracing', 'header', 'box beam', 'sill',
         'framed opening', 'furring', 'hanger', 'trim', 'corner bead', 'casing bead',
         'shadow molding', 'clip', 'extra framing', 'reinforcement')
BOARD = ('board', 'sheathing', 'plywood', 'panel', 'gypsum', 'frp', 'cement',
         'durock', 'level 5', 'finish')
MADERA = ('wood', 'blocking')
SIN_WASTE = ('fastener', 'access panel', 'sealant')     # por caja o por pieza

# divisor correcto por familia: (patron del nombre, celda de Inputs esperada)
DIVISOR = [
    ('c.r. channel', 16), ('bracing', 16), ('carrying channel', 16),
    ('furring channel', 17),
    ('trim', 18), ('corner bead', 18),
    ('metal stud', 10), ('header', 10), ('box beam', 10), ('framed opening', 10),
    ('extra framing', 10),
    ('track', 11), ('sill track', 11),
]


class LibroRechazado(Exception):
    pass


def _tiene(n, claves):
    """Busca por PALABRA COMPLETA, no por subcadena.

    Con `in` a secas, "stud reinforcement" matchea BOARD porque "reinfor-CEMENT-" lleva
    "cement" dentro. La propia compuerta lo cazo en su primera corrida. Una clasificacion
    por subcadena siempre termina en un falso positivo de estos.
    """
    return any(re.search(r'(?<![a-z])%s s?(?![a-z])'.replace(' s?', 's?') % re.escape(k), n)
               for k in claves)


def _fam(nom):
    """Familia del material, por el ENCABEZADO del renglon, no por cualquier palabra.

    "Trim - corner bead, casing bead, shadow molding, GYPSUM edge trim" se clasificaba
    como TABLERO por el "gypsum" de la enumeracion, cuando el gypsum edge trim es perfil
    metalico (J-bead). Lo que el renglon ES esta antes del guion; lo de despues es la
    lista de que incluye. Se clasifica por la cabeza y solo si no resuelve se mira todo.
    """
    cab = nom.split(' - ')[0].split('(')[0].lower().strip()
    for cand in (cab, nom.lower()):
        if _tiene(cand, MADERA):
            return 'W'
        if _tiene(cand, SIN_WASTE):
            return None
        if _tiene(cand, BOARD):
            return 'B'
        if _tiene(cand, METAL):
            return 'M'
    return None


def _fam_viejo(nom):
    n = nom.lower()
    if _tiene(n, MADERA):
        return 'W'
    if _tiene(n, SIN_WASTE):
        return None
    if _tiene(n, BOARD):
        return 'B'
    if _tiene(n, METAL):
        return 'M'
    return None


def verificar(path):
    F = []
    wb = load_workbook(path)                      # formulas
    wv = load_workbook(path, data_only=True)      # valores ya recalculados
    P, Pv = wb['Partition Takeoff'], wv['Partition Takeoff']
    R, Rv = wb['Material Summary'], wv['Material Summary']
    C = wb['Ceilings & Soffits']
    O, Ov = wb['Other Scope'], wv['Other Scope']

    # ---- 0. el libro TIENE que estar recalculado ----
    # openpyxl escribe las formulas SIN valor cacheado: hasta que corre recalc.py, toda
    # celda de formula se lee None. Un auditor que no comprueba esto reporta 30 fallos
    # fantasma ("todo sale sin desperdicio") y hace perder el tiempo buscando un error
    # que no existe.
    form = val = 0
    for r in range(5, R.max_row + 1):
        if isinstance(R.cell(r, 4).value, str) and R.cell(r, 4).value.startswith('='):
            form += 1
            if Rv.cell(r, 4).value is not None:
                val += 1
    if form and val == 0:
        raise LibroRechazado(
            'EL LIBRO NO SE HA RECALCULADO: %d celdas de formula y ninguna con valor '
            'cacheado. openpyxl no calcula nada al escribir. Corre '
            'scripts/recalc.py sobre el archivo y vuelve a auditar -- sin eso, esta '
            'auditoria reportaria decenas de fallos que no existen.' % form)

    hdr = {'Partition Takeoff': {CL(c): P.cell(4, c).value for c in range(1, P.max_column + 1)},
           'Ceilings & Soffits': {CL(c): C.cell(4, c).value for c in range(1, C.max_column + 1)}}
    totP = [r for r in range(5, P.max_row + 1)
            if P.cell(r, 1).value == 'TOTAL - PARTITIONS'][0]
    totC = [r for r in range(5, C.max_row + 1) if C.cell(r, 3).value == 'TOTAL'][0]
    ultP = max(r for r in range(5, totP) if P.cell(r, 2).value is not None)

    # ---- 1. todo rango SUM de la fila de totales cubre TODAS las filas de dato ----
    for c in range(1, P.max_column + 1):
        f = P.cell(totP, c).value
        if isinstance(f, str) and f.startswith('=SUM('):
            m = re.match(r'=SUM\([A-Z]+(\d+):[A-Z]+(\d+)\)', f)
            if m and (int(m.group(1)) > 5 or int(m.group(2)) < ultP):
                F.append('Partition Takeoff col %s: el rango %s no cubre las filas 5..%d'
                         % (CL(c), f, ultP))

    # ---- 2. toda referencia cruzada del resumen apunta a una fila de TOTALES ----
    for r in range(5, R.max_row + 1):
        f = R.cell(r, 3).value
        nom = str(R.cell(r, 1).value or '')
        if not isinstance(f, str):
            continue
        for m in re.finditer(r"'(Partition Takeoff|Ceilings & Soffits)'!(\$?)([A-Z]{1,2})\2?(\d+)", f):
            hoja, col, fila = m.group(1), m.group(3), int(m.group(4))
            if '$%s$' % col in f and ':' in f:      # es un rango de SUMIFS, no una celda
                continue
            esp = totP if hoja == 'Partition Takeoff' else totC
            if fila != esp and not re.search(r'\$%s\$%d:' % (col, fila), f):
                F.append('"%s": %s!%s%d no es la fila de TOTALES (%d)'
                         % (nom[:40], hoja, col, fila, esp))
            if hdr[hoja].get(col) is None:
                F.append('"%s": %s!%s no tiene encabezado - columna vacia'
                         % (nom[:40], hoja, col))

    # ---- 3. todo criterio de SUMIFS existe de verdad en su columna ----
    for r in range(5, R.max_row + 1):
        f = R.cell(r, 3).value
        if not isinstance(f, str) or 'SUMIFS' not in f:
            continue
        for crit in re.findall(r"'Other Scope'!\$D:\$D,\"([^\"]+)\"", f):
            if not any(O.cell(x, 4).value == crit for x in range(5, O.max_row + 1)):
                F.append('SUMIFS busca "%s" en Other Scope y ningun renglon se llama asi'
                         % crit)
        for crit in re.findall(r"\$F\$\d+:\$F\$\d+,\"([^\"]*(?:\"\")?[^\"]*)\"", f):
            real = crit.replace('""', '"')
            if not any(P.cell(x, 6).value == real for x in range(5, totP)):
                F.append('SUMIFS busca Stud Size "%s" y ningun muro lo tiene' % real)

    # ---- 4. la familia del material manda sobre el % de desperdicio ----
    for r in range(5, R.max_row + 1):
        nom, un = R.cell(r, 1).value, R.cell(r, 2).value
        if not un or not nom:
            continue
        fam = _fam(str(nom))
        w = Rv.cell(r, 4).value
        if un == 'pcs':
            continue           # las piezas sin largo se declaran en Pending, no llevan %
        if fam == 'M' and not w:
            F.append('"%s" es METAL y sale SIN desperdicio. La regla es 15%% en todo el '
                     'metal, no solo en el stud y el track.' % str(nom)[:52])
        if fam == 'B' and not w:
            F.append('"%s" es TABLERO y sale SIN desperdicio (la regla es 6%%).'
                     % str(nom)[:52])
        if fam is None and w:
            F.append('"%s" lleva desperdicio y no es ni metal ni tablero. Revisar.'
                     % str(nom)[:52])

    # ---- 5. el divisor de compra corresponde a la familia del material ----
    for r in range(5, R.max_row + 1):
        nom, un = R.cell(r, 1).value, R.cell(r, 2).value
        fp = R.cell(r, 8).value
        if not un or not isinstance(fp, str):
            continue
        # El largo de existencia solo aplica a lo que se COMPRA POR LARGO, y eso se mide
        # en LF. Un renglon en piezas o en libras (tornillos, pines, joint compound) no
        # tiene largo de existencia, aunque su nombre mencione "track" porque diga a que
        # va fijado. Sin este filtro, "pines para el bottom track" se rechazaba por no
        # usar el divisor del track -- una falsa alarma, y las falsas alarmas enseñan a
        # ignorar la compuerta.
        if str(un).strip().upper() != 'LF':
            continue
        n = str(nom).lower()
        m = re.search(r'Inputs!\$B\$(\d+)', fp)
        usa = int(m.group(1)) if m else None
        for pat, esp in DIVISOR:
            if _tiene(n, [pat]) or pat in n:
                if usa != esp:
                    F.append('"%s" se convierte a piezas con Inputs!B%s y le corresponde '
                             'B%d: un %s no se compra en el largo de otra familia.'
                             % (str(nom)[:46], usa, esp, pat))
                break

    # ---- 6. un PENDIENTE aparece como PENDING, nunca como 0 ni omitido ----
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import dataset as D
        esperados = set()
        for blk in (D.otros_bloques() + D.superficies()):
            esperados |= set((blk.get('pendientes') or {}).keys())
        escritos = {O.cell(x, 4).value for x in range(5, O.max_row + 1)
                    if str(Ov.cell(x, 5).value).upper() == 'PENDING'}
        falta = esperados - escritos
        if falta:
            F.append('estos PENDIENTES no salen marcados PENDING en Other Scope: %s. '
                     'Un pendiente que sale 0 o que no sale se lee como "no hay".'
                     % sorted(falta))
    except Exception as e:
        F.append('no se pudo comprobar los PENDIENTES: %s' % e)

    # ---- 7. ningun renglon de Other Scope se queda sin destino en silencio ----
    usados = set()
    for r in range(5, R.max_row + 1):
        f = R.cell(r, 3).value
        if isinstance(f, str):
            usados |= set(re.findall(r"'Other Scope'!\$D:\$D,\"([^\"]+)\"", f))
    DECLARADOS = {'DEDUCCION_BOARD_MEP'}      # declarados a proposito, no se aplican
    for x in range(5, O.max_row + 1):
        k = O.cell(x, 4).value
        if not k or k in usados or k in DECLARADOS:
            continue
        if str(Ov.cell(x, 5).value).upper() == 'PENDING':
            continue
        F.append('Other Scope "%s" no llega al resumen de compra y no esta en la lista de '
                 'declarados-sin-aplicar. Material cuantificado que nadie compra.' % k)

    # ---- 8. compra = neto + desperdicio, en todas ----
    for r in range(5, R.max_row + 1):
        if not R.cell(r, 2).value:
            continue
        net, wst, buy = (Rv.cell(r, c).value for c in (3, 5, 6))
        if net is None:
            continue
        if abs((buy or 0) - ((net or 0) + (wst or 0))) > 0.02:
            F.append('"%s": compra %.2f != neto %.2f + desperdicio %.2f'
                     % (str(R.cell(r, 1).value)[:44], buy or 0, net or 0, wst or 0))
    # ---- 9. si se deduce tablero por aberturas, el libro TIENE que decirlo ----
    # Los numeros pueden estar perfectos y el entregable seguir incompleto: quien revisa el
    # bid no puede ver, leyendo Clarifications, si el board va bruto o neto. Dos licitantes
    # con el mismo plano y distinta politica de deduccion no son comparables, y el que
    # deduce parece mas barato sin serlo. Origen: 29-sep-2026, <n> SF deducidos en <n>
    # aberturas y ni un renglon que lo declarara.
    ded_col = None
    for c in range(1, P.max_column + 1):
        h = str(P.cell(4, c).value or '') + str(P.cell(3, c).value or '')
        if 'deduct' in h.lower() or 'deduccion' in h.lower():
            ded_col = c; break
    hay_ded = False
    if ded_col:
        for r in range(5, P.max_row + 1):
            v = Pv.cell(r, ded_col).value
            if isinstance(v, (int, float)) and v > 0:
                hay_ded = True; break
    _sumded = 0.0
    if not hay_ded:                      # tambien cuenta la deduccion metida en Board by Face
        try:
            BF = wv['Board by Face']
            for r in range(1, BF.max_row + 1):
                for c in range(1, BF.max_column + 1):
                    v = BF.cell(r, c).value
                    if isinstance(v, (int, float)) and 0 < v and 'ded' in str(
                            BF.cell(4, c).value or '').lower():
                        hay_ded = True
                        _sumded = sum(x for x in (BF.cell(rr, c).value
                                                  for rr in range(5, BF.max_row + 1))
                                      if isinstance(x, (int, float)))
                        break
                if hay_ded: break
        except KeyError:
            pass
    if hay_ded:
        ws_clar = wb['Clarifications']
        txt = ' '.join(str(ws_clar.cell(r, c).value or '')
                       for r in range(1, ws_clar.max_row + 1)
                       for c in range(1, ws_clar.max_column + 1)).lower()
        # POR PALABRA COMPLETA, no por subcadena: "net" esta dentro de "cabinet" y de
        # "magnetic", y con `in` a secas esta comprobacion pasaba aunque se borrara el
        # renglon. Es el mismo error de subcadena que ya tiene regla propia (reinforCEMENT
        # clasificado como tablero) -- repetido por escribir `in` sin pensar.
        if not (_tiene(txt, ['net']) and _tiene(txt, ['deducted', 'deduction'])):
            F.append('se deduce tablero por aberturas (%.2f SF) pero Clarifications no '
                     'declara la politica: hay que decir que el board va NETO, que el metal '
                     'NO se deduce, y cuanto se dedujo' % _sumded)

    return F


def exigir(path):
    F = verificar(path)
    if F:
        raise LibroRechazado('EL LIBRO TIENE %d PROBLEMA(S):\n  - %s'
                             % (len(F), '\n  - '.join(F)))
    return True


if __name__ == '__main__':
    p = sys.argv[1] if len(sys.argv) > 1 else f'{_TW}/out/{_PRE}_Takeoff.xlsx'
    try:
        F = verificar(p)
    except LibroRechazado as e:
        print(e); sys.exit(2)
    if F:
        print('PROBLEMAS (%d):' % len(F))
        for x in F:
            print('  -', x)
        sys.exit(1)
    print('OK - el libro pasa las 8 comprobaciones')
