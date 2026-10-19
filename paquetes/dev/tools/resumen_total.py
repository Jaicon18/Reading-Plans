# -*- coding: utf-8 -*-
"""resumen_total.py -- TODO el proyecto: walls + ceilings + soffits + marquesina.

resumen_global.py solo entiende cierres de WALL (los que llevan 'length'). Este consolida
ademas los elementos que no son walls -- ceilings, soffits y marquesina -- que se miden en
SF y no en LF, y vuelve a verificar TODOS los sellos.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (por defecto, el directorio actual)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", _os_rutas.getcwd())
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import json, glob, collections, hashlib, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from closer import waste
import resumen_global as RG

B = f'{_TW}'
NOMURO = collections.OrderedDict([
    ('CEILINGS GWB',        B + '/CIELOS_cierres.json'),
    ('SOFFIT',             B + '/SOFFITS_cierres.json'),
    ('MARQUESINA',         B + '/CANOPY_cierres.json'),
])
# Bloques que no son ni muro ni superficie: se cuentan como ELEMENTOS y sus partidas
# entran al gran total igual que las demas. Sus sellos se verifican con el mismo control.
OTROS = collections.OrderedDict([
    ('CRUCE MEP (penetr.)',   B + '/MEP_cierre.json'),
    ('HUECOS de luminaria',   B + '/HUECOS_cierre.json'),
    ('PUNTOS 3-4-5',          B + '/PUNTOS345_cierres.json'),
    ('ZONAS HUMEDAS',         B + '/HUMEDAS_cierres.json'),
])
METALP = {'STUD', 'STUD_3-5-8', 'TRACK_BOTTOM', 'TRACK_TOP', 'TRACK_EXTREMOS_DE_STUD',
          'TRACK_CANTOS_LATERALES', 'HEADER', 'BRACING', 'ABERTURA_MEP_HEAD_SILL',
          'SILL_TRACK', 'BOX_BEAM', 'CORNER_BEAD', 'SHADOW_MOLDING', 'CASING_BEAD',
          'FURRING_CHANNEL', 'CARRYING_CHANNEL', 'HANGER_WIRE'}
SF = {'BOARD', 'NIVEL5', 'FRP', 'FRP WC-3', 'CEMENT_BOARD', 'CEMENT BOARD',
      'PLYWOOD_3-4_FRT', 'SUSTRATO_PLYWOOD', 'PANEL_BALISTICO_3-8_UL752', 'BOARD_3-8',
      'SHEATHING_5-8_FRT_PLYWOOD_2-1-2_POLYISO', 'SHEATHING_5-8_FRT_PLYWOOD',
      'PLYWOOD_FRT', 'BOARD_3_8', 'PLYWOOD_5-8_FRT EN EL NICHO DEL ATM',
      'FRP WC-3',
      'DEDUCCION_BOARD_MEP', 'RETORNO_BOARD_RANURA', 'BOARD_WR',
      'BOARD_REGULAR_A_RESTAR'}
SINW = {'SEALANT', 'BLOCKING', 'FASTENER_PWR_DRIVEN', 'FASTENER_TEKS', 'OPENING_DUCT',
        'TRIM_CASING', 'FIBERGLASS_UL752', 'ACCESS_PANEL', 'TRIM_CEILING'}


def sello_ok(x):
    d2 = {k: v for k, v in x.items() if k != 'sello'}
    return hashlib.sha256(json.dumps(d2, sort_keys=True, ensure_ascii=False)
                          .encode()).hexdigest()[:16] == x.get('sello')


if __name__ == '__main__':
    GR = collections.defaultdict(float)
    UNI = collections.defaultdict(set)
    ok = bad = n = 0
    print('%-24s %7s %12s   %s' % ('BLOQUE', 'elem', 'LF / SF', 'sellos'))
    print('-' * 62)
    tipos = RG.cargar()
    lf_tot = 0.0
    for t, ws in tipos.items():
        lf = sum(x['largo']['v'] or 0 for x in ws)
        o = sum(1 for x in ws if RG.sello_ok(x)); b = len(ws) - o
        ok += o; bad += b; n += len(ws); lf_tot += lf
        print('%-24s %7d %9.2f LF   %d OK / %d rotos' % (t, len(ws), lf, o, b))
        for x in ws:
            for k, v in x['partidas'].items():
                GR[k.split(':', 1)[0]] += v['val']['v'] or 0
                UNI[k.split(':', 1)[0]].add((v.get('unidad') or '').strip())
    print('%-24s %7d %9.2f LF' % ('  subtotal walls', n, lf_tot))
    print('-' * 62)
    sf_tot = 0.0
    for t, f in NOMURO.items():
        if not os.path.exists(f):
            print('%-24s   (sin archivo)' % t); continue
        d = json.load(open(f, encoding='utf-8'))
        els = [v for v in d.values() if isinstance(v, dict)]
        sf = sum(v.get('sf') or (v['partidas'].get('BOARD:%s' % v.get('cuarto', ''), {})
                                 .get('val', {}).get('v') or 0) for v in els)
        o = sum(1 for v in els if sello_ok(v)); b = len(els) - o
        ok += o; bad += b; n += len(els); sf_tot += sf
        print('%-24s %7d %9.2f SF   %d OK / %d rotos' % (t, len(els), sf, o, b))
        for v in els:
            for k, val in v['partidas'].items():
                GR[k.split(':', 1)[0]] += val['val']['v'] or 0
                UNI[k.split(':', 1)[0]].add((val.get('unidad') or '').strip())
    print('%-24s %7s %9.2f SF' % ('  subtotal no-wall', '', sf_tot))
    print('-' * 62)
    for t, f in OTROS.items():
        if not os.path.exists(f):
            print('%-24s   (sin archivo)' % t); continue
        d = json.load(open(f, encoding='utf-8'))
        els = [v for v in d.values() if isinstance(v, dict) and 'partidas' in v]
        o = sum(1 for v in els if sello_ok(v)); b = len(els) - o
        ok += o; bad += b; n += len(els)
        print('%-24s %7d %12s   %d OK / %d rotos' % (t, len(els), '-', o, b))
        for v in els:
            for k, val in v['partidas'].items():
                GR[k.split(':', 1)[0]] += val['val']['v'] or 0
                UNI[k.split(':', 1)[0]].add((val.get('unidad') or '').strip())
    print('-' * 62)
    print('%-24s %7d %22s' % ('TOTAL', n, '%d sellos OK / %d rotos' % (ok, bad)))

    mixtas = {k: sorted(x for x in v if x) for k, v in UNI.items()
              if len({x for x in v if x}) > 1}
    if mixtas:
        print('\n*** UNA MISMA LINE ITEM CON DOS UNIDADES DISTINTAS ENTRE CIERRES:')
        for k, v in sorted(mixtas.items()):
            print('      %-36s %s' % (k, v))

    print('\n%-42s %5s %11s %12s %11s'
          % ('PARTIDA', 'UNID', 'NETO', 'DESPERDICIO', 'COMPRA'))
    for k in sorted(GR):
        v = GR[k]
        # CORREGIDO 6-oct-2026: la unidad se LEE DEL CIERRE, no de una lista escrita a mano.
        # Habia un set `LFBOARD = {'PLYWOOD_FRT', 'BOARD_3_8'}` que imprimia en LF dos partidas
        # que TODOS los cierres sellan en SF: <n> SF de plywood FRT salian rotulados LF.
        # Una unidad mal rotulada en el resumen de materiales se cotiza mal, y el numero de
        # abajo es correcto, asi que nada lo delata.
        us = sorted(x for x in UNI.get(k, set()) if x)
        u = us[0] if len(us) == 1 else ('SF' if k in SF else 'LF')
        if k in SINW:
            print('%-42s %5s %11.2f %12s %11.2f' % (k, u, v, '--', v))
        else:
            cl = 'BOARD' if k in SF else 'STUD'
            w = waste(v, cl)
            print('%-42s %5s %11.2f %12.2f %11.2f'
                  % (k, u, w['NETO'], w['DESPERDICIO'], w['COMPRA']))
