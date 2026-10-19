# -*- coding: utf-8 -*-
"""resumen_global.py -- consolida TODOS los cierres sellados del proyecto y saca
NETO / WASTE / COMPRA por line item, mas la verificacion de sellos.
Un numero que no salga de aqui no esta entregado."""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (por defecto, el directorio actual)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", _os_rutas.getcwd())
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import json, glob, collections, hashlib, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from closer import waste

O = f'{_TO}'
B = f'{_TW}'
# BLOQUES DE CIERRES DE WALL, por type. La agrupacion y la numeracion de walls son DEL
# PROYECTO (E24): se leen de $TAKEOFF_WORK/bloques_walls.json, en orden:
#   [["<type> (<rango de walls>)", ["{OUT}/<glob>", "{WORK}/<archivo>.json", ...]], ...]
# {OUT} = TAKEOFF_OUT, {WORK} = TAKEOFF_WORK. Sin el archivo: [] (no se inventa un proyecto).
def _src():
    try:
        filas = json.load(open(os.path.join(B, 'bloques_walls.json'), encoding='utf-8'))
    except (OSError, ValueError):
        filas = []
    return collections.OrderedDict(
        (t, [p.replace('{OUT}', O).replace('{WORK}', B) for p in pats]) for t, pats in filas)


SRC = _src()
UN = {'STUD': 'pz', 'FASTENER_PWR_DRIVEN': 'pz', 'OPENING_DUCT': 'ea'}
SF = {'BOARD', 'NIVEL5', 'FRP', 'FRP WC-3', 'CEMENT_BOARD', 'CEMENT BOARD', 'PLYWOOD_3-4_FRT',
      'SUSTRATO_PLYWOOD', 'PANEL_BALISTICO_3-8_UL752', 'BOARD_3-8',
      'SHEATHING_5-8_FRT_PLYWOOD_2-1-2_POLYISO', 'SHEATHING_5-8_GLASS_MAT'}
METALP = {'STUD', 'STUD_3-5-8', 'TRACK_BOTTOM', 'TRACK_TOP', 'HEADER', 'BRACING', 'ABERTURA_MEP_HEAD_SILL',
          'SILL_TRACK', 'BOX_BEAM', 'CORNER_BEAD', 'SHADOW_MOLDING', 'CASING_BEAD'}
SINW = {'SEALANT', 'BLOCKING', 'FASTENER_PWR_DRIVEN', 'OPENING_DUCT', 'TRIM_CASING',
        'FIBERGLASS_UL752'}


def sello_ok(x):
    d2 = {k: v for k, v in x.items() if k != 'sello'}
    return hashlib.sha256(json.dumps(d2, sort_keys=True, ensure_ascii=False).encode()
                          ).hexdigest()[:16] == x.get('sello')


def cargar():
    tipos = collections.OrderedDict()
    for t, pats in SRC.items():
        walls = []
        for p in pats:
            for f in sorted(glob.glob(p)):
                d = json.load(open(f, encoding='utf-8'))
                ds = ([d] if isinstance(d, dict) and 'muro' in d
                      else [v for v in d.values() if isinstance(v, dict) and 'muro' in v])
                walls += ds
        seen, uniq = set(), []
        for x in walls:
            if x['muro'] in seen: continue
            seen.add(x['muro']); uniq.append(x)
        tipos[t] = uniq
    return tipos


if __name__ == '__main__':
    tipos = cargar()
    GR = collections.defaultdict(float)
    print('%-20s %6s %10s   %s' % ('TIPO', 'muros', 'LF', 'sellos'))
    tot_lf = tot_n = ok = bad = 0
    for t, ws in tipos.items():
        lf = sum(x['largo']['v'] or 0 for x in ws)
        o = sum(1 for x in ws if sello_ok(x)); b = len(ws) - o
        ok += o; bad += b; tot_lf += lf; tot_n += len(ws)
        print('%-20s %6d %10.2f   %d OK / %d rotos' % (t, len(ws), lf, o, b))
        for x in ws:
            for k, v in x['partidas'].items():
                GR[k.split(':', 1)[0].upper()] += v['val']['v'] or 0
    print('%-20s %6d %10.2f   %d OK / %d rotos' % ('TOTAL', tot_n, tot_lf, ok, bad))
    print('\n%-32s %5s %11s %12s %11s' % ('PARTIDA', 'UNID', 'NETO', 'DESPERDICIO', 'COMPRA'))
    for k in sorted(GR):
        v = GR[k]
        u = UN.get(k, 'SF' if k in SF else 'LF')
        if k in SINW:
            print('%-32s %5s %11.2f %12s %11.2f' % (k, u, v, '--', v))
        else:
            cls = 'STUD' if k in METALP else 'BOARD'
            w = waste(v, cls)
            print('%-32s %5s %11.2f %12.2f %11.2f' % (k, u, w['NETO'], w['DESPERDICIO'], w['COMPRA']))
