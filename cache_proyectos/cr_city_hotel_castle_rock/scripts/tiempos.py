"""TIEMPOS.md (hora de California, U-094) desde cache_proyectos/cr_city_hotel_castle_rock/tiempos.log + commits del repo + hora de fin.
rev2: maneja el cambio de día (fechas completas), pausa por orden del usuario fuera del total."""
import subprocess, datetime as dt
fin = subprocess.run(['date', '+%Y-%m-%d %H:%M'], env={'TZ': 'America/Los_Angeles'}, capture_output=True, text=True).stdout.strip()
F = lambda s: dt.datetime.strptime(s, '%Y-%m-%d %H:%M')
rows = [("0", "Arranque (órdenes U-001..U-150, skill v81cf52) + descarga BuildingConnected (19 archivos) + Drive Projects + copia limpia + comparación 2025 / 2026", "2026-11-05 11:16", "2026-11-05 11:34", "set_texto.json, comparacion_sets.json"),
        ("1", "Inventario (inventario_tags.py arreglado BE-CR01) + lector independiente de schedules", "2026-11-05 11:34", "2026-11-05 11:58", "etapas/1_inventario, indep/"),
        ("2-3a", "Lecturas A / B por piso (8 subagentes) + burbujas - DETENIDO por orden del usuario a las 12:18", "2026-11-05 12:04", "2026-11-05 12:18", "-"),
        ("2-3b", "Lecturas A / B por piso (relanzadas) + burbujas + ventanas / trim", "2026-11-05 18:50", "2026-11-05 19:23", "etapas/2_lectura, burbujas/"),
        ("4-6", "Comparación A / B + resolución por piso + canon + canon.py + RFI", "2026-11-05 19:23", "2026-11-05 19:42", "3_revision, 4_canon"),
        ("7-8", "Excel fijo + markups Bluebeam walls / RCP + imágenes + verificar_markups_excel", "2026-11-05 19:42", "2026-11-05 20:28", "8_excel, 6_markups, 7_imagenes"),
        ("9-10", "rev1: documentos, auditoría U-138 #1, proposal U-150, compuerta, subida rev1 (558 archivos)", "2026-11-05 20:28", "2026-11-06 00:21", "SUBIDA_OK.json rev1"),
        ("rev2-a", "Orden COORDINACIÓN 02:12 (rev1 pasó en vacío): BE-CR25 + compuerta con walls board-only + BOTH SIDES / U-114 / U-117 / U-118 vivos + caras con baño", "2026-11-06 02:12", "2026-11-06 03:07", "commit 'compuerta VERDE 169/3/0 con chequeos por wall vivos'"),
        ("rev2-b", "Auditoría adversarial U-138 #2 (subagente independiente)", "2026-11-06 03:08", "2026-11-06 03:28", "auditoria_U138_2/INFORME_AUDITORIA_U138_2.md"),
        ("rev2-c", "Hallazgos aplicados y verificados (banos_cbu, shafts L3/L4, F4-F12, BE-CR26 cadena) + compuerta VERDE + skill v81cf56", "2026-11-06 03:28", "2026-11-06 04:25", "RESOLUCION_HALLAZGOS_U138_2.md, gate.txt"),
        ("rev2-d", "Subida rev2 (2,093 archivos) + aviso REPLACED BY rev2 en rev1 + listado de Drive", "2026-11-06 04:25", "2026-11-06 07:17", "SUBIDA_OK.json rev2"),
        ("rev2-e", "BE-CR28 (orden de subida, Auditoria.zip) + recheck v81cf57 / BE-CR29 (chequeos en vacío) -> hallazgo XW.6.6-0", "2026-11-06 07:17", "2026-11-06 07:38", "ENTREGA_OK_recheck_v81cf57.json"),
        ("rev3", "rev3: sheathing XW.6.6-0 + barrido de ratings + citas coves + compuerta VERDE + skill v81cf57 + subida (Auditoria.zip) + aviso en rev2 + listado", "2026-11-06 07:38", "2026-11-06 07:57", "ENTREGA_OK.json / SUBIDA_OK.json rev3"),
        ("rev4", "rev4 (orden COORDINACIÓN 16:56 PST: revisión de RCP + walls -0 hacia Retail 124): medición de F1-F5 / D1-D6 en vectores, barrido de los 35 tags GYP de RCP (BE-CR30, skill v81cf61), cadena + compuerta VERDE + subida + aviso en rev3", "2026-11-06 16:56", fin, "ENTREGA_OK.json / SUBIDA_OK.json rev4")]
L = ["# CR City Hotel - Castle Rock, CO — registro de tiempos (hora de California, PST)", "",
     "Horas reales (tiempos.log, commits del repo, `TZ=America/Los_Angeles date`). Pausa 05-nov 12:18-18:50 por orden del usuario y espera 06-nov 00:21-02:12 (rev1 entregada, hasta la orden de rev2) fuera del total.", "",
     "| # | Paso | Inicio | Fin | Duración | Evidencia |", "|---|---|---|---|---|---|"]
tot = 0
for r in rows:
    d = int((F(r[3]) - F(r[2])).total_seconds() // 60); tot += d
    L.append(f"| {r[0]} | {r[1]} | {r[2][5:]} PST | {r[3][5:]} PST | {d} min | {r[4]} |")
r1 = sum(int((F(r[3]) - F(r[2])).total_seconds() // 60) for r in rows if not r[0].startswith('rev'))
L.append(f"| **TOTAL** | **rev1 {r1} min ({r1 // 60} h {r1 % 60:02d}) + rev2/rev3/rev4 {tot - r1} min ({(tot - r1) // 60} h {(tot - r1) % 60:02d})** | **11-05 11:16 PST** | **{fin[5:]} PST** | **{tot} min** | meta U-041 2 h; referencia O'Reilly ~3 h, VS ~5.5 h, Chuze ~8-9 h, Consumer Cellular ~6 h |")
open('/root/cr/work/TIEMPOS.md', 'w').write('\n'.join(L) + '\n'); print(L[-1])
