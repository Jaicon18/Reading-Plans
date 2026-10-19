# -*- coding: utf-8 -*-
"""localizar.py -- reconstruye la BANDA (coordenadas) de cada muro ya cerrado, para poder
marcarlo sobre la hoja. Barre todas las bandas del espesor del tipo y le asigna a cada muro
la banda cuyo largo coincide con su LF, usando como desempate las coordenadas que el propio
cierre dejo escritas en su campo `operacion`.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (antes fijas en /home/claude/boa)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", "/home/claude/boa")
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import sys, os, json, glob, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bandas

ESP = {'A1': 7.32, 'B': 7.32, 'A5': 10.92, 'B2': 10.86, 'B2K': 11.52,
       'C1': 6.36, 'G': 9.24, 'G1': 12.72, 'A1K': 7.80}


def coords_del_texto(d):
    op = ' '.join(str(d['largo'].get(k) or '') for k in ('operacion', 'fuente'))
    return [float(v) for v in re.findall(r'\d{3,4}\.\d{2}', op)]


def localizar(tipo, files, tol_ft=0.60):
    esp = ESP[tipo]
    bs = bandas.bandas(23, esp, tol=0.55, min_len=5.0)
    out, sobran = [], []
    for f in files:
        d = json.load(open(f, encoding='utf-8'))
        lf = d['largo']['v']
        cc = coords_del_texto(d)
        best = None
        for b in bs:
            L = (b[4] - b[3]) / 18.0
            if abs(L - lf) > tol_ft:
                continue
            # puntaje: cuantas coordenadas del texto caen sobre esta banda
            sc = sum(1 for v in cc if min(abs(v - b[1]), abs(v - b[2]), abs(v - b[3]), abs(v - b[4])) < 0.6)
            sc = sc * 100 - abs(L - lf)
            if best is None or sc > best[0]:
                best = (sc, b, L)
        if best:
            out.append((d['muro'], lf, best[1], round(best[2], 2)))
        else:
            sobran.append((d['muro'], lf))
    return out, sobran


TIPOS = {
 'A1':  [f'{_TO}/A1/A1_v2_muro_*.json'],
 'A5':  [f'{_TO}/A5_muro_*.json'],
 'B':   [f'{_TO}/B_muro_*.json', f'{_TO}/B/B_muro_*.json'],
 'B2':  [f'{_TO}/B2/B2_v2_muro_*.json'],
 'B2K': [f'{_TO}/B2K/B2K_muro_*.json'],
 'C1':  [f'{_TO}/C1/C1_env_*.json', f'{_TO}/C1/C1_muro_*.json'],
}

if __name__ == '__main__':
    todo = {}
    for t, pats in TIPOS.items():
        fs = []
        for p in pats:
            fs += sorted(glob.glob(p))
        seen, ff = set(), []
        for f in fs:
            n = json.load(open(f, encoding='utf-8'))['muro']
            if n in seen: continue
            seen.add(n); ff.append(f)
        ok, bad = localizar(t, ff)
        print('=== %s : %d/%d localizados ===' % (t, len(ok), len(ff)))
        for num, lf, b, L in sorted(ok):
            print('   #%-3d %6.2f LF  banda %s %8.2f/%8.2f  tramo %8.2f->%8.2f (%.2f ft)'
                  % (num, lf, b[0], b[1], b[2], b[3], b[4], L))
        for num, lf in bad:
            print('   #%-3d %6.2f LF  >> SIN BANDA que coincida' % (num, lf))
        todo[t] = [(n, lf, b) for n, lf, b, L in ok]
        print()
    json.dump({t: [[n, lf, list(b)] for n, lf, b in v] for t, v in todo.items()},
              open(f'{_TW}/bandas_por_tipo.json', 'w'), indent=1)
    print('-> bandas_por_tipo.json')
