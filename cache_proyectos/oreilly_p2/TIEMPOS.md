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
