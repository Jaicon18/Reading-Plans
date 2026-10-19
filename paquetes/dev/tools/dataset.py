# -*- coding: utf-8 -*-
"""dataset.py -- aplana TODOS los cierres sellados a un dataset para el Excel.

No recalcula nada: lee el JSON sellado de cada elemento. Si un sello no cuadra, aborta.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (por defecto, el directorio actual)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", _os_rutas.getcwd())
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import sys, os, re, json, glob, hashlib, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import resumen_global as RG
import cadena_detalles as CD
import motivos_cadena as MC

# SUPER REGLA de Rodolfo (4-oct-2026): el Excel SIEMPRE anota la secuencia completa de
# detalles que se recorrio, en el orden en que se recorrio. La entrada es la PLANTA: floor
# plan para muros y aberturas, RCP para cielos, soffits y marquesinas.
_G = None
_PROF = None


CLASE_EN = {'puerta': 'door', 'hueco': 'framed opening', 'ventana': 'window',
            'pass-through': 'pass-through', 'storefront': 'storefront'}


def _cadena(obj, entrada):
    global _G, _PROF
    if _G is None:
        _G = CD.grafo(); _PROF = CD.profundidad(_G)
    return CD.texto(obj, entrada, _PROF, _G)

B = f'{_TW}'

# perfil de stud por tag, con su fuente. Es DATO DEL PROYECTO (E24): se lee de
# $TAKEOFF_WORK/perfil_tipos.json = {"<tag>": ["<stud size>", "<designacion SSMA>", <oc_in>, "<N/HOJA + texto>"]}.
# Un tag sin fila sale '?' / PENDIENTE (nunca un perfil de otro proyecto).
def _perfil():
    try:
        return {t: tuple(v) for t, v in json.load(open(os.path.join(B, 'perfil_tipos.json'),
                                                       encoding='utf-8')).items()}
    except (OSError, ValueError, TypeError, AttributeError):
        return {}


PERFIL = _perfil()

def v(p):
    return (p or {}).get('val', {}).get('v')


def _agr(P):
    """Suma por prefijo. Un dict comprehension SOBRESCRIBE cuando dos renglones
    comparten prefijo (BOARD_WR:bano 114 y BOARD_WR:bano 113) y se pierde la mitad."""
    out = {}
    for k, p in P.items():
        base = k.split(':', 1)[0]
        out[base] = out.get(base, 0) + (v(p) or 0)
    return out


def _pendientes(P):
    """Line items con estado PENDIENTE. Van APARTE de las sumas: un pendiente NO es un
    cero. Colapsarlo a 0 lo hace desaparecer del entregable y se lee como 'no hay',
    que es lo contrario de lo que dice. (Encontrado el 28-sep-2026:
    RETORNO_BOARD_RANURA salia como 0.00 y en el Excel ni aparecia.)"""
    out = {}
    for k, p in P.items():
        val = (p or {}).get('val', {})
        if val.get('estado') == 'PENDIENTE':
            out[k.split(':', 1)[0]] = {
                'motivo': val.get('operacion') or val.get('fuente') or '',
                'renglon': k}
    return out

def sello_ok(x):
    d2 = {k: val for k, val in x.items() if k != 'sello'}
    return hashlib.sha256(json.dumps(d2, sort_keys=True, ensure_ascii=False)
                          .encode()).hexdigest()[:16] == x.get('sello')

def _stud_lf(p, pz, alto):
    """LF de material de stud. Un wall que cruza el eje B puede tener DOS alturas, y el
    cierre lo escribe en su operacion ("tramo HI <n>ft: ...=<n> a <n>ft; tramo LOW
    <n>ft: ...=<n> a <n>ft"). Multiplicar piezas x una sola height lo falsea."""
    op = ((p or {}).get('val') or {}).get('operacion') or ''
    tr = re.findall(r'=\s*(\d+)\s*a\s*([\d.]+)\s*ft', op)
    if not tr:
        # otra forma del mismo dato: "campo: HI <n>ft=<n> + LOW <n>ft=<n> -> <n>"
        m = re.search(r'HI\s*[\d.]+\s*ft\s*=\s*(\d+).*?LOW\s*[\d.]+\s*ft\s*=\s*(\d+)', op)
        if m:   # v66 (E24): antes traía las alturas de un proyecto fijas en el código
            raise ValueError("operación HI/LOW sin alturas: escribir 'n a H ft' por zona (alturas del proyecto)")
    if tr:
        lf = sum(int(n) * float(h) for n, h in tr)
        extra = pz - sum(int(n) for n, _ in tr)          # terminacion, jambas, cripples
        if extra > 0:
            # los studs adicionales (terminacion, jambas, cripples) van a la altura
            # DECLARADA del muro, no a la mayor de los tramos: en el muro 16 las 4
            # jambas de la puerta 122 estan en la zona baja.
            lf += extra * float(alto or 0)
        return round(lf, 2)
    return round(pz * (alto or 0), 2)


def muros():
    """Una fila por WALL, mas la lista de sus FACES."""
    out = []
    for t, ws in RG.cargar().items():
        for w in ws:
            assert RG.sello_ok(w), 'sello roto en %s' % w.get('muro')
            tag = w.get('tag')
            perf = PERFIL.get(tag, ('?', '?', w.get('oc'), 'PENDIENTE'))
            P = w['partidas']
            ab = w.get('aberturas', []) or []
            A_ab = sum((a.get('w') or 0) * (a.get('h') or 0) for a in ab)
            caras = []
            for c in w.get('caras', []):
                nom = c.get('cuarto', '')
                pp = P.get('BOARD:%s' % nom) or {}
                sf = v(pp) or 0
                cap = c.get('capas') or 1
                H = (c.get('alto_board') or {}).get('v')
                op = (pp.get('val') or {}).get('operacion') or ''
                # L y H de ESA cara: se leen de la operacion del propio cierre y se
                # ACEPTAN solo si reproducen el SF sellado. Una cara puede ser mas corta
                # que el muro (un lado partido en varios cuartos) o mas alta/baja.
                L = Hf = None
                cands = [(float(a), float(b)) for a, b in
                         re.findall(r'(\d+(?:\.\d+)?)\s*(?:LF|ft|pies)?\s*x\s*(\d+(?:\.\d+)?)', op)]
                # deducciones candidatas: ninguna, una abertura sola, o todas
                ded_cand = [0.0, A_ab] + [(a.get('w') or 0) * (a.get('h') or 0) for a in ab]
                # se recorren las parejas EN ORDEN (la primera es la real L x H de la
                # cara) y solo se acepta una deduccion >= 0: una deduccion negativa
                # significa que la pareja elegida era la del vano, no la de la cara.
                for LL, HH in cands:
                    for ded_ab in ded_cand:
                        d = ded_ab * cap
                        if d >= -0.001 and abs(LL * HH * cap - d - sf) <= 0.06:
                            L, Hf, dedf = LL, HH, d
                            break
                    if L is not None:
                        break
                if L is None and H:                      # caso parapeto: L x (a - b)
                    m = re.search(r'(\d+(?:\.\d+)?)\s*LF\s*x\s*\((\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\)', op)
                    if m and abs(float(m.group(1)) * (float(m.group(2)) - float(m.group(3))) * cap - sf) <= 0.06:
                        L, Hf, dedf = float(m.group(1)), round(float(m.group(2)) - float(m.group(3)), 3), 0.0
                if L is None:
                    # patron "bruto - deduccion = neto" sin L x H explicito
                    m2 = re.search(r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*=\s*(\d+(?:\.\d+)?)', op)
                    if m2 and H and abs(float(m2.group(3)) - sf) <= 0.06:
                        bruto, dd = float(m2.group(1)), float(m2.group(2))
                        L, Hf, dedf = round(bruto / (H * cap), 4), H, dd
                if L is None and cands:
                    # el cierre da L x H pero su SF ya trae una deduccion que no es un
                    # vano completo (p.ej. el tramo de officefront). Se toma la primera
                    # pareja y la deduccion QUE EL PROPIO CIERRE aplico, para que la
                    # formula del Excel reproduzca el numero sellado sin inventar nada.
                    LL, HH = cands[0]
                    L, Hf, dedf = LL, HH, round(LL * HH * cap - sf, 2)
                if L is None:
                    L, Hf, dedf = None, H, 0.0
                caras.append({'cara': nom, 'largo': L, 'alto': Hf if Hf else H,
                              'alto_decl': H, 'tipo': c.get('tipo'), 'capas': cap,
                              'ded': round(dedf, 2) if L is not None else 0.0,
                              'sf': sf, 'op': op})
            # La cara "Exterior (sheathing)" de un muro exterior NO es gypsum board
            # regular: H/A09.23 la rotula "5/8\" EXTERIOR GYPSUM SHEATHING" y es la cara
            # INTERIOR DEL PARAPETO, del deck al tope. Va en su propio renglon.
            ext_sheath = round(sum(c['sf'] for c in caras
                                   if 'sheathing' in (c['cara'] or '').lower()), 2)
            caras = [c for c in caras if 'sheathing' not in (c['cara'] or '').lower()]
            # CAPAS = capas TOTALES contando las dos caras, no la suma de las filas.
            # Un lado que da a varios cuartos con cielos distintos se parte en varias
            # filas de cara, y sumarlas da 4 donde solo hay 2 capas (muros 8, 21, 23,
            # 27 y 28). Se calcula por CAPA-PIES / largo del muro, que es lo que la
            # columna Layers del formato quiere decir. Corregido 28-sep-2026.
            _L = w['largo']['v'] or 0
            capas = (round(sum(c['capas'] * (c['largo'] or 0) for c in caras) / _L, 2)
                     if _L and all(c['largo'] is not None for c in caras)
                     else (sum(c['capas'] for c in caras) or 1))
            ded = sum(c['ded'] for c in caras)
            otros = {}
            for k, p in P.items():
                base = k.split(':', 1)[0]
                if base in ('STUD', 'TRACK_BOTTOM', 'TRACK_TOP', 'BRACING', 'BOARD'):
                    continue
                otros[base] = otros.get(base, 0) + (v(p) or 0)
            out.append({
                'bloque': t, 'num': w.get('muro'), 'tag': tag,
                'ubic': w.get('ubicacion', ''),
                'largo': v({'val': w['largo']}), 'alto': v({'val': w['alto_stud']}),
                'oc': w.get('oc'), 'brace_sp': w.get('brace_sp'),
                'hileras': w.get('hileras') or 1,
                'perfil_lbl': perf[0], 'perfil_des': perf[1], 'perfil_src': perf[3],
                'caras': caras, 'capas': capas,
                'aberturas': ab, 'ded_board': round(ded, 2),
                # La CLASE se guarda en espanol porque es la que gobierna las reglas del
                # cierre (puerta = solo header, hueco = header Y sill). Lo que VIAJA AL
                # ENTREGABLE va en ingles, asi que se traduce aqui, al escribir, no en el dato.
                'abert_txt': ' + '.join(
                    '%s %s %.2f x %.2f' % (CLASE_EN.get(a.get('clase'), a.get('clase')),
                                           a.get('ref'), a.get('w') or 0, a.get('h') or 0)
                    for a in ab),
                'studs': v(P.get('STUD')) or 0,
                'stud_lf': _stud_lf(P.get('STUD'), v(P.get('STUD')) or 0,
                                    v({'val': w['alto_stud']})),
                'track_b': v(P.get('TRACK_BOTTOM')) or 0,
                'track_t': v(P.get('TRACK_TOP')) or 0,
                'bracing': v(P.get('BRACING')) or 0,
                'board': round(sum(c['sf'] for c in caras), 2),
                'ext_sheathing': ext_sheath,
                'otros': otros,
                'excl': list((w.get('excluidas') or {}).keys()),
                'cadena': _cadena(w, MC.ENTRADA['muros']),
                'detail_log': MC.log(w, MC.ENTRADA['muros'], _PROF, _G),
                'sello': w['sello'],
            })
    out.sort(key=lambda r: (r['tag'], -(r['largo'] or 0)))
    return out

def superficies():
    """Ceilings, soffits y marquesina: una fila por elemento."""
    out = []
    for grupo, f in [('CEILING GWB', 'CIELOS_cierres.json'),
                     ('SOFFIT', 'SOFFITS_cierres.json'),
                     ('CANOPY', 'CANOPY_cierres.json')]:
        p = os.path.join(B, f)
        if not os.path.exists(p):
            continue
        for k, d in json.load(open(p, encoding='utf-8')).items():
            if not isinstance(d, dict) or 'partidas' not in d:
                continue
            assert sello_ok(d), 'sello roto en %s' % k
            P = d['partidas']
            sf = d.get('sf') or v(P.get('BOARD:%s' % d.get('cuarto', ''))) or 0
            out.append({'grupo': grupo, 'id': k,
                        'nombre': d.get('cuarto') or d.get('zona') or k,
                        'alto': d.get('altura') or d.get('aff'),
                        'sf': sf,
                        'partidas': _agr(P),
                        'pendientes': _pendientes(P),
                        'cadena': _cadena(d, MC.ENTRADA.get(f)),
                        'detail_log': MC.log(d, MC.ENTRADA.get(f), _PROF, _G),
                        'sello': d['sello']})
    return out

def otros_bloques():
    out = []
    for grupo, f in [('MEP PENETRATIONS', 'MEP_cierre.json'),
                     ('RECESSED FIXTURE OPENINGS', 'HUECOS_cierre.json'),
                     ('MISC SCOPE', 'PUNTOS345_cierres.json'),
                     ('WET AREAS', 'HUMEDAS_cierres.json'),
                     # 10-oct-2026: los dos huecos de blocking de millwork que el barrido
                     # wall-por-wall no podia cerrar (un tag huerfano entre varios cierres que
                     # lo nombran para decir que no es suyo, y la 2a instancia de otro).
                     ('MILLWORK BLOCKING', 'MWBLOCKING_cierres.json')]:
        p = os.path.join(B, f)
        if not os.path.exists(p):
            continue
        for k, d in json.load(open(p, encoding='utf-8')).items():
            if not isinstance(d, dict) or 'partidas' not in d:
                continue
            assert sello_ok(d), 'sello roto en %s' % k
            out.append({'grupo': grupo, 'id': k,
                        'nombre': d.get('ubicacion') or d.get('cuarto') or k,
                        'partidas': _agr(d['partidas']),
                        'pendientes': _pendientes(d['partidas']),
                        'sello': d['sello']})
    return out

if __name__ == '__main__':
    M, S, O = muros(), superficies(), otros_bloques()
    print('walls %d   superficies %d   otros %d' % (len(M), len(S), len(O)))
    print('LF total %.2f' % sum(m['largo'] or 0 for m in M))
    print('SF board de walls %.2f' % sum(m['board'] for m in M))
    print('SF superficies %.2f' % sum(s['sf'] for s in S))
    for m in M[:3]:
        print(' ', m['num'], m['tag'], m['largo'], m['perfil_lbl'], len(m['caras']),
              'capas', m['capas'], 'ded', m['ded_board'])
