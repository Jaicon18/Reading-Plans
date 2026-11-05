# O'Reilly Auto Parts, 23rd Ave., Evans, CO #1 — registro de tiempos (hora de California)
Pasada 2 (base de la rev5). Reconstruido el 03-nov a partir de horas REALES, nunca estimadas: hora de modificación de los
archivos de cada etapa (`TZ=America/Los_Angeles date -r <archivo>`) y hora de cada commit de git (convertida a hora de
California). 31-oct = PDT (horario de verano); 01-nov en adelante = PST. "~" = la hora sale del archivo que cierra la
etapa, no de un registro de inicio.

| # | Paso | Inicio | Fin | Duración | Evidencia |
|---|---|---|---|---|---|
| 0 | Arranque: copia limpia del set sin markups + reglas + skill | 31-oct 10:26 PDT | 31-oct 10:28 PDT | 2 min | plans/bidset_con_markups_SIN_MARKUPS.pdf, etapas/0_mapa/SHEET_MAP.md |
| 1 | Inventario: mapa de hojas + inventario de tags | 31-oct 10:28 PDT | 31-oct 10:30 PDT | 2 min | etapas/1_inventario/inventario.json |
| 2 | Lectura A (independiente) | 31-oct 10:30 PDT | ~31-oct 11:16 PDT | ~46 min | lect_resolucion/takeoff_canon_A.json |
| 3 | Lectura B (independiente, en paralelo a A) | 31-oct 10:30 PDT | ~31-oct 11:16 PDT | ~46 min | lect_resolucion/takeoff_canon_B.json |
| 4 | Comparación A/B (comparar.py) | ~31-oct 11:16 PDT | 31-oct 11:16 PDT | < 1 min | etapas/3_revision/revision.md |
| 5 | Resolución dirigida de las diferencias + revisiones por elemento (rev2–rev10, ELEMENTO 1–6) | 31-oct 11:16 PDT | 31-oct 15:39 PDT | 4 h 23 min | resolucion.md 11:30; commits ELEMENTO 1 11:32 … ELEMENTO 6 15:39 |
| 6 | Cálculo (canon.py + tools) — ensamble run1–run4 | 31-oct 15:46 PDT | 31-oct 16:19 PDT | 33 min | run1, run4 |
| 7 | Markups Bluebeam + imágenes marcadas — run7 post-auditoría | 31-oct 16:19 PDT | 31-oct 16:54 PDT | 35 min | run7; commit rev2 post-auditoría 16:58 |
| 8 | Excel formato fijo (plantilla_excel.py) con respuestas del usuario — run12 | 31-oct 16:58 PDT | 31-oct 18:44 PDT | 1 h 46 min | run12, ensamble/run12.log |
| 9 | Compuertas + back-check independiente + run15 FINAL (RFI-01/29 cerrados) | 02-nov 09:48 PST | 02-nov 10:05 PST | 17 min | backcheck/BACKCHECK_INFORME.md 10:05, run15 |
| 10 | Subida a Drive (pasada 2 FINAL) | 02-nov 10:05 PST | 02-nov 10:07 PST | 2 min | UPLOAD_FINAL 10:06; commit 10:07 |
| 11 | Revisión rápida de markups (v1 LF / v2 altura impresa) | 02-nov 21:01 PST | 03-nov 10:28 PST | — (dos sesiones) | commits 21:01 y 10:28 |
| 12 | Revisión de materiales vs Partition Type Schedule (v3) | 03-nov 10:47 PST | 03-nov 10:57 PST | 10 min | commits 10:51 y 10:57 |
| R5 | rev5: compuerta de entrega en verde (datos del proyecto, TIEMPOS, set_texto con OCR, fichas, head track del plano, arreglos de tool, cadena re-corrida con v81cf25) + subida con subir_entrega.py + skill v81cf25 | 03-nov 14:04 PST | 03-nov 15:15 PST | 70 min (incl. reinicio de contenedor) | t_rev5_start, SUBIDA_OK.json |
| **TOTAL** | **Arranque → pasada 2 FINAL en Drive (pasos 0–10, horas de trabajo)** | **31-oct 10:26 PDT** | **02-nov 10:07 PST** | **8 h 37 min de trabajo** (31-oct 10:26–18:44 = 8 h 18 min + 02-nov 09:48–10:07 = 19 min) | |
| R6 | rev6: compuerta v81cf26 (preferencias del día 1) en verde: estado [CONFIRMED]/[DERIVED] por cara, barrido de tags A1.1 (29, subagente + asignación por programa), imagen de altura circulada por wall, Review Items con imagen, arreglo R80e.153; subida con subir_entrega.py + aviso en rev5; skill v81cf28 | 03-Nov 15:20 PST | 03-Nov 16:17 PST | 56 min | t_rev6_start, SUBIDA_OK.json (rev6) |
| R7 | rev7: detector de burbujas de dos líneas (U-137 / BE-139) + U-138 auditar_compuerta; barrido de burbujas de las 21 hojas del trade, 120 círculos verificados a ojo, cadena seguida hasta el final (13 eslabones: 4 citados, 8 fuera de alcance con motivo (1/A4.2 FRT nailers Div. 06 R-ALC-01), 8/A5.4 = OCR de 8/A5.1), RFI-34 con supuesto cargado, cadena re-corrida con v81cf33 (run28d) | 03-nov 23:29 PST | 04-nov 02:04 PST (subida a Drive, SUBIDA_OK.json) | 2 h 35 min | orden de COORDINACIÓN 03-nov 23:29 PST (registro de la sesión); run28d 01:51 PST |
| R8 | rev8: respuestas del usuario 5-nov (RFI-34 = A; wood EXCLUDED, R-ALC-01 / U-139: FRT 2X blocking y FRT plywood en 0 con nota, RFI-12 / 24 / 25 reemplazados), chequeo U-139 + wood_excluded en canon.py, cadena re-corrida con v81cf42 (run29g) | 04-nov 21:05 PST | 04-nov 21:35 PST (subida a Drive, SUBIDA_OK.json) | 35 min | orden de COORDINACIÓN 04-nov 21:05 PST (registro de la sesión) |
| R9 | rev9: U-141 detalles circulados (marcar_detalles + CE_DETALLES_CIRCULADOS: 138 burbujas en origen y destino, 12 destinos verificados a ojo) + U-140 (CE_RFI_BUSQUEDA_EXHAUSTIVA), skill v81cf43; cantidades = rev8 | 04-nov 21:49 PST | 04-nov 22:07 PST (subida a Drive, SUBIDA_OK.json) | | orden de COORDINACIÓN 04-nov 21:49 PST (registro de la sesión) |
