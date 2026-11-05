"""TIEMPOS.md (California time, U-094) from work/tiempos.log (stamps written at the start / end of each step) + the end stamp."""
import sys, subprocess
fin = subprocess.run(['date', '+%H:%M'], env={'TZ': 'America/Los_Angeles'}, capture_output=True, text=True).stdout.strip()
L = ["# Consumer Cellular - Centennial, CO — registro de tiempos (hora de California, PST)", "",
     "Horas reales escritas al empezar / terminar cada paso (work/tiempos.log, `TZ=America/Los_Angeles date`). 05-nov-2026.", "",
     "| # | Paso | Inicio | Fin | Duración | Evidencia |", "|---|---|---|---|---|---|"]
rows = [("0", "Arranque (skill v81cf47, órdenes) + descarga BuildingConnected / Elite plan room + comparación de los dos sets", "00:53", "01:06", "set_texto / comparacion_sets.json"),
        ("1", "Inventario (inventario_tags.py) + texto del set y burbujas", "01:06", "01:07", "etapas/1_inventario"),
        ("2-3", "Lecturas A y B independientes (subagentes en paralelo) + lector independiente de schedules + verificación de burbujas", "01:07", "01:21", "etapas/2_lectura, indep/, burbujas/"),
        ("4-5", "Comparación A/B (comparar.py) + resolución con imagen", "01:21", "01:22", "3_revision/revision.md, resolucion.md"),
        ("6", "Cálculo (canon.py y tools, ajustes por programa, RFI)", "01:22", "01:32", "4_canon/out"),
        ("7-8", "Excel fijo + markups Bluebeam (walls, demo, RCP) + imágenes", "01:32", "01:49", "8_excel, 6_markups, 7_imagenes"),
        ("9-10", "Compuertas (reglas, etapas, back-check, compuerta de entrega) + subida", "01:49", fin, "ENTREGA_OK.json, SUBIDA_OK.json")]
def m(a, b):
    h1, m1 = map(int, a.split(':')); h2, m2 = map(int, b.split(':')); return (h2 * 60 + m2) - (h1 * 60 + m1)
for r in rows:
    L.append(f"| {r[0]} | {r[1]} | 05-nov {r[2]} PST | 05-nov {r[3]} PST | {m(r[2], r[3])} min | {r[4]} |")
L.append(f"| **TOTAL** | **Arranque → entrega** | **05-nov 00:53 PST** | **05-nov {fin} PST** | **{m('00:53', fin)} min** | meta U-041: 2 h; referencia O'Reilly ~3 h, VS ~5.5 h, Chuze ~8-9 h |")
open('/root/cc/work/TIEMPOS.md', 'w').write('\n'.join(L) + '\n'); print(L[-1])
