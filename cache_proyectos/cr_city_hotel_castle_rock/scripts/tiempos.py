"""TIEMPOS.md (hora de California, U-094) desde cache_proyectos/cr_city_hotel_castle_rock/tiempos.log + hora de fin."""
import subprocess
fin = subprocess.run(['date', '+%H:%M'], env={'TZ': 'America/Los_Angeles'}, capture_output=True, text=True).stdout.strip()
def m(a, b):
    h1, m1 = map(int, a.split(':')); h2, m2 = map(int, b.split(':')); return (h2 * 60 + m2) - (h1 * 60 + m1)
rows = [("0", "Arranque (órdenes U-001..U-150, skill v81cf52) + descarga BuildingConnected (19 archivos) + Drive Projects + copia limpia + comparación 2025 / 2026", "11:16", "11:34", "set_texto.json, comparacion_sets.json"),
        ("1", "Inventario (inventario_tags.py arreglado BE-CR01) + lector independiente de schedules", "11:34", "11:58", "etapas/1_inventario, indep/"),
        ("2-3a", "Lecturas A / B por piso (8 subagentes) + burbujas G1 / G2 - DETENIDO por orden del usuario a las 12:18", "12:04", "12:18", "-"),
        ("2-3b", "Lecturas A / B por piso (relanzadas tras la orden 'ya puedes continuar') + burbujas + ventanas / trim", "18:50", "19:23", "etapas/2_lectura, burbujas/"),
        ("4-6", "Comparación A / B por programa + resolución por piso (4 subagentes) + canon + canon.py + RFI", "19:23", "19:42", "3_revision, 4_canon"),
        ("7-8", "Excel fijo (reglas.py OK) + markups Bluebeam walls / RCP + imágenes + verificar_markups_excel (819 / 819)", "19:42", "20:28", "8_excel, 6_markups, 7_imagenes"),
        ("9-10", "Documentos, auditoría adversarial U-138, proposal U-150, compuerta de entrega, subida", "20:28", fin, "ENTREGA_OK.json, SUBIDA_OK.json")]
L = ["# CR City Hotel - Castle Rock, CO — registro de tiempos (hora de California, PST)", "",
     "Horas reales de cache_proyectos/cr_city_hotel_castle_rock/tiempos.log (`TZ=America/Los_Angeles date`). 05-nov-2026. Pausa 12:18-18:50 por orden del usuario (no cuenta).", "",
     "| # | Paso | Inicio | Fin | Duración | Evidencia |", "|---|---|---|---|---|---|"]
tot = 0
for r in rows:
    d = m(r[2], r[3]); tot += d
    L.append(f"| {r[0]} | {r[1]} | 05-nov {r[2]} PST | 05-nov {r[3]} PST | {d} min | {r[4]} |")
L.append(f"| **TOTAL** | **Arranque → entrega (sin la pausa)** | **05-nov 11:16 PST** | **05-nov {fin} PST** | **{tot} min** | meta U-041 2 h; referencia O'Reilly ~3 h, VS ~5.5 h, Chuze ~8-9 h, Consumer Cellular ~6 h |")
open('/root/cr/work/TIEMPOS.md', 'w').write('\n'.join(L) + '\n'); print(L[-1])
