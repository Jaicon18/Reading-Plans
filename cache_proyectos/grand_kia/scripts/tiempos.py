"""TIEMPOS.md (California time, U-094 / U-045) from work/tiempos.log stamps. Rows are consecutive (no overlap): work that ran in
parallel is named inside the row it overlapped. The last row ends at the moment this script runs (gate + upload)."""
import subprocess, json
fin = subprocess.run(['date', '+%d-%b %H:%M'], env={'TZ': 'America/Los_Angeles'}, capture_output=True, text=True).stdout.strip().lower()
P = json.load(open('/root/gk/work/tiempos_pasos.json'))
rows = P['rows'] + [[P['ultimo'][0], P['ultimo'][1], P['ultimo'][2], fin, P['ultimo'][3]]]
def mins(s):
    d, hm = s.split(' '); h, m = map(int, hm.split(':')); return int(d.split('-')[0]) * 1440 + h * 60 + m
L = ["# Grand Kia - Thornton (Denver), CO - registro de tiempos (hora de California, PST)", "",
     "Horas reales escritas al empezar / terminar cada paso (work/tiempos.log, `TZ=America/Los_Angeles date`). Filas consecutivas; lo que corrió en paralelo va dentro de la fila con la que se encimó.", "",
     "| # | Paso | Inicio | Fin | Duración | Evidencia |", "|---|---|---|---|---|---|"]
tot = 0
for k, name, a, b, ev in rows:
    d = mins(b) - mins(a); tot += d
    L.append(f"| {k} | {name} | {a} PST | {b} PST | {d} min | {ev} |")
L.append(f"| **TOTAL** | **Arranque -> entrega** | **{rows[0][2]} PST** | **{rows[-1][3]} PST** | **{tot} min** | {tot / 60:.2f} h; {tot / 60 / 41.287:.3f} h por 1,000 SF (41,287 SF, A000) |")
open('/root/gk/work/TIEMPOS.md', 'w').write('\n'.join(L) + '\n'); print(L[-1])
