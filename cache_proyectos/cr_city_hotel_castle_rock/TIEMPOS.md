# CR City Hotel - Castle Rock, CO — registro de tiempos (hora de California, PST)

Horas reales (tiempos.log, commits del repo, `TZ=America/Los_Angeles date`). Pausa 05-nov 12:18-18:50 por orden del usuario y espera 06-nov 00:21-02:12 (rev1 entregada, hasta la orden de rev2) fuera del total.

| # | Paso | Inicio | Fin | Duración | Evidencia |
|---|---|---|---|---|---|
| 0 | Arranque (órdenes U-001..U-150, skill v81cf52) + descarga BuildingConnected (19 archivos) + Drive Projects + copia limpia + comparación 2025 / 2026 | 11-05 11:16 PST | 11-05 11:34 PST | 18 min | set_texto.json, comparacion_sets.json |
| 1 | Inventario (inventario_tags.py arreglado BE-CR01) + lector independiente de schedules | 11-05 11:34 PST | 11-05 11:58 PST | 24 min | etapas/1_inventario, indep/ |
| 2-3a | Lecturas A / B por piso (8 subagentes) + burbujas - DETENIDO por orden del usuario a las 12:18 | 11-05 12:04 PST | 11-05 12:18 PST | 14 min | - |
| 2-3b | Lecturas A / B por piso (relanzadas) + burbujas + ventanas / trim | 11-05 18:50 PST | 11-05 19:23 PST | 33 min | etapas/2_lectura, burbujas/ |
| 4-6 | Comparación A / B + resolución por piso + canon + canon.py + RFI | 11-05 19:23 PST | 11-05 19:42 PST | 19 min | 3_revision, 4_canon |
| 7-8 | Excel fijo + markups Bluebeam walls / RCP + imágenes + verificar_markups_excel | 11-05 19:42 PST | 11-05 20:28 PST | 46 min | 8_excel, 6_markups, 7_imagenes |
| 9-10 | rev1: documentos, auditoría U-138 #1, proposal U-150, compuerta, subida rev1 (558 archivos) | 11-05 20:28 PST | 11-06 00:21 PST | 233 min | SUBIDA_OK.json rev1 |
| rev2-a | Orden COORDINACIÓN 02:12 (rev1 pasó en vacío): BE-CR25 + compuerta con walls board-only + BOTH SIDES / U-114 / U-117 / U-118 vivos + caras con baño | 11-06 02:12 PST | 11-06 03:07 PST | 55 min | commit 'compuerta VERDE 169/3/0 con chequeos por wall vivos' |
| rev2-b | Auditoría adversarial U-138 #2 (subagente independiente) | 11-06 03:08 PST | 11-06 03:28 PST | 20 min | auditoria_U138_2/INFORME_AUDITORIA_U138_2.md |
| rev2-c | Hallazgos aplicados y verificados (banos_cbu, shafts L3/L4, F4-F12, BE-CR26 cadena) + compuerta VERDE + skill v81cf56 | 11-06 03:28 PST | 11-06 04:25 PST | 57 min | RESOLUCION_HALLAZGOS_U138_2.md, gate.txt |
| rev2-d | Subida rev2 (2,093 archivos) + aviso REPLACED BY rev2 en rev1 + listado de Drive | 11-06 04:25 PST | 11-06 07:17 PST | 172 min | SUBIDA_OK.json rev2 |
| rev2-e | BE-CR28 (orden de subida, Auditoria.zip) + recheck v81cf57 / BE-CR29 (chequeos en vacío) -> hallazgo XW.6.6-0 | 11-06 07:17 PST | 11-06 07:38 PST | 21 min | ENTREGA_OK_recheck_v81cf57.json |
| rev3 | rev3: sheathing XW.6.6-0 + barrido de ratings + citas coves + compuerta VERDE + skill v81cf57 + subida (Auditoria.zip) + aviso en rev2 + listado | 11-06 07:38 PST | 11-06 07:47 PST | 9 min | ENTREGA_OK.json / SUBIDA_OK.json rev3 |
| **TOTAL** | **rev1 387 min (6 h 27) + rev2/rev3 334 min (5 h 34)** | **11-05 11:16 PST** | **11-06 07:47 PST** | **721 min** | meta U-041 2 h; referencia O'Reilly ~3 h, VS ~5.5 h, Chuze ~8-9 h, Consumer Cellular ~6 h |
