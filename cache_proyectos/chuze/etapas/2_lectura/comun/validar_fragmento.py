#!/usr/bin/env python3
"""validar_fragmento.py <fragmento.json> — copia comun/constants.json + el fragmento a una carpeta temporal y corre
`etapas.py unir ... --inventario` (bandas, ids, páginas 1-based, refs de aberturas, contra el inventario de la Etapa 1).
Imprime UNIR OK o los errores. El canon completo (canon.py / validar_canon) se valida después, ya unido."""
import json, os, shutil, subprocess, sys, tempfile
AQUI = os.path.dirname(os.path.abspath(__file__))
T = '/tmp/chuze/skill/take-off-metal-frame-drywall/tools'
INV = '/tmp/chuze/work/etapas/1_inventario/inventario.json'
frag = json.load(open(sys.argv[1]))
if 'constants' in frag:
    print('ERROR: el fragmento no lleva "constants" (van en comun/constants.json)'); sys.exit(1)
d = tempfile.mkdtemp()
shutil.copy(os.path.join(AQUI, 'constants.json'), os.path.join(d, '00_constants.json'))
shutil.copy(sys.argv[1], os.path.join(d, os.path.basename(sys.argv[1])))
r = subprocess.run([sys.executable, os.path.join(T, 'etapas.py'), 'unir', d, os.path.join(d, 'out.json'),
                    '--inventario', INV], capture_output=True, text=True, cwd=T)
out = '\n'.join(l for l in (r.stdout + r.stderr).splitlines() if 'Warning' not in l and 'warnings.warn' not in l)
print(out.strip()[-4000:]); print('UNIR OK' if r.returncode == 0 else 'UNIR FALLA'); shutil.rmtree(d); sys.exit(r.returncode)
