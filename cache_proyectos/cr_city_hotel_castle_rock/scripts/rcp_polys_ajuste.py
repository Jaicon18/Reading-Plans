"""Itera markups_rcp.py: cada caja 'SF without hatch at (x0, y0, x1, y1)' que reporta (hatch de gyp del RCP fuera del
polígono) se incorpora a la envolvente del polígono del ceiling (el hatch DIBUJADO manda). Máx. 4 vueltas."""
import json, re, subprocess, sys
W = '/root/cr/work/etapas'; T = '/root/skill/take-off-metal-frame-drywall/tools'
for it in range(4):
    p = subprocess.run([sys.executable, f'{T}/markups_rcp.py', f'{W}/6_markups/markups.pdf', f'{W}/4_canon/takeoff_canon.json',
                        f'{W}/6_markups/rcp_polys.json', f'{W}/6_markups/markups_con_rcp.pdf', f'{W}/6_markups/rcp_png'], capture_output=True, text=True)
    txt = p.stdout + p.stderr
    m = re.search(r'\{"hojas".*\}', txt)
    res = json.loads(m.group(0)) if m else {}
    falt = res.get('sin_hatch') or []
    print('vuelta', it, 'rc', p.returncode, 'sin_hatch', len(falt))
    if p.returncode == 0 or not falt:
        break
    polys = {x['room']: x for x in json.load(open(f'{W}/6_markups/rcp_polys.json'))}
    for f in falt:
        room = f.split(':')[0]
        if room not in polys:
            continue
        xs = [q[0] for q in polys[room]['polygon']]; ys = [q[1] for q in polys[room]['polygon']]
        for b in re.findall(r'at \((\d+), (\d+), (\d+), (\d+)\)', f):
            x0, y0, x1, y1 = map(float, b); xs += [x0, x1]; ys += [y0, y1]
        polys[room]['polygon'] = [[min(xs), min(ys)], [max(xs), min(ys)], [max(xs), max(ys)], [min(xs), max(ys)]]
        polys[room]['ajuste'] = 'envelope extended to the drawn gyp hatch reported by markups_rcp'
    json.dump(list(polys.values()), open(f'{W}/6_markups/rcp_polys.json', 'w'), indent=1)
sys.exit(p.returncode)
