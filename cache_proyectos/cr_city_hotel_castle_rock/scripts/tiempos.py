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
        ("rev4", "rev4 (orden COORDINACIÓN 16:56 PST: revisión de RCP + walls -0 hacia Retail 124): medición de F1-F5 / D1-D6 en vectores, barrido de los 35 tags GYP de RCP (BE-CR30, skill v81cf61), cadena + compuerta VERDE + subida + aviso en rev3", "2026-11-06 16:56", "2026-11-06 17:37", "ENTREGA_OK.json / SUBIDA_OK.json rev4"),
        ("rev4-b", "Revisión de código post-rev4 (6 puntos, verif_codigo.py, RFIs) + reglas del skill", "2026-11-06 20:54", "2026-11-06 21:26", "Revision de codigo 2026-11-06 (file times: arch.pdf download 20:55, RESUMEN v2 21:26)"),
        ("rev5", "rev5: cambios de código en el base (L4 a roof sheathing, 120 / 118B 2 HR, FW.4-L4-19 1 HR) + deduct alternates + RFI-23/24/25 + compuerta + subida", "2026-11-06 21:35", "2026-11-06 22:28", "ENTREGA_OK.json / SUBIDA_OK.json rev5"),
        ("rev6", "rev6: auditoría COORDINACIÓN (E1 coffers del lobby, E2 cement board a la cara del wall, E3 CB_BE_CF10 lee specs, O1 angle = perímetro real, O2 cove L2 4 1/2\") + compuerta + subida", "2026-11-07 06:34", "2026-11-07 07:20", "ENTREGA_OK.json / SUBIDA_OK.json rev6"),
        ("rev7", "rev7: markup de todo cielo / soffit cuantificado (73 renglones de misc_items) + compuerta CE_RCP_COMPLETO + skill v81cf63", "2026-11-07 14:33", "2026-11-07 15:05", "ENTREGA_OK.json / SUBIDA_OK.json rev7"),
        ("rev8", "rev8: revisión de walls (W.4-L4-21, W.6-L1-32 nuevo, markups a tramos medidos, tags, vanos A7) + CLG 0'-0\" + compuertas CE_MARKUP_EN_WALL / CR-R8-C", "2026-11-07 15:10", "2026-11-07 16:00", "ENTREGA_OK.json / SUBIDA_OK.json rev8"),
        ("rev9", "rev9: FACP 125 + contorno real de todos los cielos (52 ceilings + 22 misc medidos en vectores) + RFI-27 / DA-6 + compuerta CE_CONTORNO_REAL", "2026-11-07 16:00", "2026-11-07 18:42", "ENTREGA_OK.json / SUBIDA_OK.json rev9"),
        ("rev10", "rev10: auditoría U-138 sobre rev9 (E1 RFI-27 impreso en A0.08, E2 puerta 120.1 90 MIN, R1 shafts 2-1/2\" C-H, m1 altura L2, m2 filas C-H, m3 conteos) + 3 compuertas", "2026-11-08 06:34", "2026-11-08 07:54", "ENTREGA_OK.json / SUBIDA_OK.json rev10"),
        ("rev11", "rev11: revisiones independientes A (materiales / specs / exterior / proposal) y B (RFI / alturas / ratings / detalles) sobre rev10 + 3 compuertas (CB_CR_R11_F12, CB_U_155)", "2026-11-08 12:33", "2026-11-08 14:33", "ENTREGA_OK.json / SUBIDA_OK.json rev11"),
        ("rev12", "rev12: U-155 (buscar hasta encontrar; si no, IBC citado) sobre todos los RFI abiertos y valores assumed: RFI-28 / RFI-25 cerrados, DA-7 retirado", "2026-11-08 14:40", "2026-11-08 15:35", "ENTREGA_OK.json / SUBIDA_OK.json rev12"),
        ("rev13", "rev13: auditoría U-138 de rev12 (E1 caras exteriores con altura de la interior, E2 citas de norma con sección / tabla, detector no impreso, RS-1..RS-7 de A2.05)", "2026-11-09 06:38", "2026-11-09 07:45", "ENTREGA_OK.json / SUBIDA_OK.json rev13"),
        ("rev14", "rev14: U-156 re-barrido de los 9 RFI abiertos (RFI-15 / 22 / 23 / 26 cerrados por lo impreso, RFI-04 parcial: lobby 217 / 317 2HR FB)", "2026-11-10 10:55", "2026-11-10 13:12", "ENTREGA_OK.json / SUBIDA_OK.json rev14")]
L = ["# CR City Hotel - Castle Rock, CO — registro de tiempos (hora de California, PST)", "",
     "Horas reales (tiempos.log, commits del repo, `TZ=America/Los_Angeles date`). Pausa 05-nov 12:18-18:50 por orden del usuario y espera 06-nov 00:21-02:12 (rev1 entregada, hasta la orden de rev2) fuera del total.", "",
     "| # | Paso | Inicio | Fin | Duración | Evidencia |", "|---|---|---|---|---|---|"]
tot = 0
for r in rows:
    d = int((F(r[3]) - F(r[2])).total_seconds() // 60); tot += d
    L.append(f"| {r[0]} | {r[1]} | {r[2][5:]} PST | {r[3][5:]} PST | {d} min | {r[4]} |")
r1 = sum(int((F(r[3]) - F(r[2])).total_seconds() // 60) for r in rows if not r[0].startswith('rev'))
L.append(f"| **TOTAL** | **rev1 {r1} min ({r1 // 60} h {r1 % 60:02d}) + rev2-rev8 {tot - r1} min ({(tot - r1) // 60} h {(tot - r1) % 60:02d})** | **11-05 11:16 PST** | **{fin[5:]} PST** | **{tot} min** | meta U-041 2 h; referencia O'Reilly ~3 h, VS ~5.5 h, Chuze ~8-9 h, Consumer Cellular ~6 h |")
open('/root/cr/work/TIEMPOS.md', 'w').write('\n'.join(L) + '\n'); print(L[-1])
