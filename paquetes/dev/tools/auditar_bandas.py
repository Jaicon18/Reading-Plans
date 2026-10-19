# -*- coding: utf-8 -*-
"""auditar_bandas.py -- COROLARIO DE AUDITORIA DE LA SUPER REGLA.

Para cada muro ya cerrado, verifica que el BOARD de cada cara sea
    largo x alto x capas  MENOS  (ancho x alto) de cada abertura,
y NO el rectangulo de piso a deck. Si la deduccion se parece mas al rectangulo
completo que al area real de la abertura, lo marca.

Tambien verifica:
  - que ninguna abertura de tipo ventana/pass-through/hueco haya perdido su SILL
  - que el TRACK siga dando 2 x hileras corridas
  - que cada abertura tenga head citado
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (antes fijas en /home/claude/boa)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", "/home/claude/boa")
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import json, glob, os, sys

def area_ab(a):
    return (a.get('w') or 0) * (a.get('h') or 0)

def audit(path):
    d = json.load(open(path, encoding='utf-8'))
    if 'muro' not in d:
        return None
    out = {'muro': d['muro'], 'tag': d['tag'], 'file': os.path.basename(path), 'flags': []}
    L = (d['largo'] or {}).get('v') or 0
    Hs = (d['alto_stud'] or {}).get('v') or 0
    hil = d.get('hileras', 1)
    abs_ = d.get('aberturas', [])
    A_ab = sum(area_ab(a) for a in abs_)
    caras = {c['cuarto']: c for c in d['caras']}
    for k, v in d['partidas'].items():
        if not k.startswith('BOARD'):
            continue
        val = (v['val'] or {}).get('v')
        if val is None:
            continue
        cuarto = k.split(':', 1)[1] if ':' in k else None
        c = caras.get(cuarto)
        if c is None:
            if len(caras) == 1:
                c = list(caras.values())[0]
            else:
                out['flags'].append('%s: no se pudo emparejar con una cara' % k); continue
        alto = (c['alto_board'] or {}).get('v') or 0
        capas = c.get('capas', 1)
        bruto = L * alto * capas
        esperado = bruto - A_ab * capas
        full = bruto - (sum((a.get('w') or 0) for a in abs_) * alto * capas)
        if abs(val - esperado) > max(0.6, 0.01 * max(1, bruto)):
            if abs_ and abs(val - full) < abs(val - esperado):
                out['flags'].append(
                    '%s = %.2f parece DEDUCIR EL RECTANGULO COMPLETO de la abertura '
                    '(piso a tope). Con la abertura real deberia ser %.2f. Delta %.2f SF'
                    % (k, val, esperado, esperado - val))
            else:
                out['flags'].append(
                    '%s = %.2f, bruto %.2f x%d capas - aberturas %.2f = %.2f (delta %.2f)'
                    % (k, val, bruto, capas, A_ab * capas, esperado, val - esperado))
    for a in abs_:
        if a['clase'] != 'puerta' and not a.get('sill'):
            out['flags'].append('abertura %s (%s) SIN SILL: toda abertura que no es puerta '
                                'tiene antepecho y lleva sill' % (a['ref'], a['clase']))
        if not a.get('head'):
            out['flags'].append('abertura %s sin head citado' % a['ref'])
    tb = d['partidas'].get('TRACK_BOTTOM', {}).get('val', {}).get('v')
    tt = d['partidas'].get('TRACK_TOP', {}).get('val', {}).get('v')
    if tb is not None and tt is not None and L:
        cor = (tb + tt) / L
        if abs(cor - 2.0 * hil) > 0.03:
            out['flags'].append('TRACK %.2f corridas, esperado %.2f' % (cor, 2.0 * hil))
    sl = d['partidas'].get('SEALANT', {}).get('val', {}).get('v')
    if sl is not None and L:
        n = sl / L
        if abs(n - 4.0) > 0.05:
            out['flags'].append('SEALANT %.2f corridas (%.2f LF / %.2f). El perimetro de cada '
                                'pano de board se sella: piso y tope POR CARA = 4 corridas. '
                                'Faltan %.2f LF' % (n, sl, L, L * 4 - sl))
    return out


if __name__ == '__main__':
    pats = sys.argv[1:] or [
        f'{_TO}/A1/A1_muro_*.json',
        f'{_TO}/B/B_muro_*.json',
        f'{_TW}/B_muro_*.json',
        f'{_TO}/B2/B2_muro_*.json',
        f'{_TO}/B2K/B2K_muro_*.json',
        f'{_TO}/C1/C1_*.json',
        f'{_TO}/A5/A5_muro_*.json',
        f'{_TO}/A5_muro_*.json',
    ]
    tot = 0; conf = 0
    for p in pats:
        for f in sorted(glob.glob(p)):
            r = audit(f)
            if not r: continue
            tot += 1
            if r['flags']:
                conf += 1
                print('\n### muro %s (%s)  [%s]' % (r['muro'], r['tag'], r['file']))
                for fl in r['flags']:
                    print('   - ' + fl)
    print('\n%d muros auditados, %d con hallazgos.' % (tot, conf))
