# Grand Kia - Thornton (Denver), CO - registro de tiempos (hora de California, PST)

Horas reales escritas al empezar / terminar cada paso (work/tiempos.log, `TZ=America/Los_Angeles date`). Filas consecutivas; lo que corrió en paralelo va dentro de la fila con la que se encimó.

| # | Paso | Inicio | Fin | Duración | Evidencia |
|---|---|---|---|---|---|
| 0 | Arranque (skill v81cf79, órdenes U-001..U-170) + descarga BuildingConnected de los 2 GC + comparación de sets + Drive Projects | 10-nov 21:01 PST | 10-nov 21:06 PST | 5 min | comparacion_sets.json, Drive Projects |
| 1 | Inventario: capa OCR de las 48 hojas A (texto en curvas, BE-GK02) + inventario_tags.py (BE-GK03); en paralelo schedules independientes (21:12-21:19) y skill v81cf81 | 10-nov 21:06 PST | 10-nov 21:14 PST | 8 min | etapas/1_inventario, indep/ |
| 2-3 | Lecturas A y B independientes por zona (8 subagentes) + cielos + demolición + exterior + Level 5 + burbujas; inventario OCR termina en paralelo (21:33) | 10-nov 21:14 PST | 10-nov 21:54 PST | 40 min | etapas/2_lectura, burbujas/ |
| 4-5 | Comparación A/B por programa + resolución con imagen por zona + barrido de RFI (U-172) | 10-nov 21:54 PST | 10-nov 22:05 PST | 11 min | 3_revision/revision.md, resolucion.md, 4_canon/rfis_final.json |
| 6 | Canon + cálculo (build_canon / misc_gen / canon.py), reglas R70.2 de esquinas por programa, evidencias | 10-nov 22:05 PST | 10-nov 23:45 PST | 100 min | 4_canon/out, REGLAS_FALLAS.md |
| 6b | Alturas U-175 / U-176: 8 lecturas ciegas A/B + 2 resoluciones dirigidas, tabla final, cierre dimensional, reglas físicas | 10-nov 23:45 PST | 11-nov 01:09 PST | 84 min | alturas/FINAL, ALTURAS_IMPRESAS.csv |
| 6c | Revisión independiente U-168 (A1-A5) + integración: trims, control joints, 13 openings, Dens, Type X, deflection track, RCP excluded; BE-GK12..BE-GK19 | 11-nov 01:09 PST | 11-nov 03:20 PST | 131 min | revision_independiente/, BIBLIOTECA_ERRORES |
| 7-10 | Excel fijo + markups Bluebeam (walls, demo, RCP, EXCLUDED) + sello closer / planmark + proposal + documentos + compuerta de entrega + subida | 11-nov 03:20 PST | 11-nov 07:20 PST | 240 min | ENTREGA_OK.json, SUBIDA_OK.json |
| 7-10b | Subida rev1 terminada (SUBIDA_OK 15:32 UTC) | 11-nov 07:20 PST | 11-nov 07:32 PST | 12 min | entrega/SUBIDA_OK.json |
| R2.1 | rev2: aplicación de los RFI U-178 (RFI-01/05/07/34/35: A-Z1-08 10.5 ft, G-Z2-12 43.25 SF) + U-179 + 4 corridas de cadena (canon 08:22 / 08:28 / 08:31 / 08:40, CHAIN-OK 08:48) | 11-nov 07:32 PST | 11-nov 08:48 PST | 76 min | bitacora.jsonl, rfis_final.json |
| R2.2 | Proposal + armar + compuerta corrida 1 (v81cf92; cortada al llegar la auditoría) en paralelo con la auditoría independiente U-181 (informe 09:29: 36 ítems, 3 LOW) | 11-nov 08:48 PST | 11-nov 09:29 PST | 41 min | auditoria_U181/AUDIT.md |
| R2.3 | Corrección F1-F3 (sheathing C-Z3, campos RFI, textos) + cadenas 09:34-09:42 y 09:44-09:52 (fix trazabilidad BE-GK34) + re-verificación 1 (09:56: F1/F3 abiertos en texto, N1) | 11-nov 09:29 PST | 11-nov 09:56 PST | 27 min | auditoria_U181/REVERIF.md |
| R2.4 | Barrido global de texto (BE-GK33b) + cadena 09:58-10:06 | 11-nov 09:56 PST | 11-nov 10:06 PST | 10 min | cadena_rev2d.log |
| R2.5 | armar: compuerta corrida 2 COLGADA 43 min en `detalles` (glob ** con 2 symlinks en ciclo, BE-GK35); cortada y diagnosticada | 11-nov 10:06 PST | 11-nov 10:53 PST | 47 min | BIBLIOTECA_ERRORES BE-GK35 |
| R2.6 | Arreglo de ciclos + armar: compuerta corrida 3 ROJA (4 FAIL: Proposal rev1, GUIA sin CAMBIOS, altura G-Z2-12, gauge U-177); en paralelo re-verificación 2 (10:58: 0 abiertos) | 11-nov 10:53 PST | 11-nov 11:10 PST | 17 min | auditoria_U181/REVERIF2.md |
| R2.7 | Correcciones BE-GK36 + cadena 11:10-11:18 + armar: compuerta corrida 4 ROJA (2 FAIL: A2 G-Z2-12, head track) | 11-nov 11:10 PST | 11-nov 11:27 PST | 17 min | cadena_rev2e.log |
| R2.8 | Cadena 11:27-11:35 + armar: compuerta corrida 5 VERDE + re-armado de la GUIA (corrida 6, cortada); en paralelo re-verificación 3 (11:49: 3 LOW R3-N1..N3) | 11-nov 11:27 PST | 11-nov 11:49 PST | 22 min | auditoria_U181/REVERIF3.md |
| R2.9 | Corrección R3 (600T bottom track -168.21 LF, etiquetas G-Z2-12, desglose blocking) + cadena 11:51-11:59 + armar: corrida 7 VERDE + re-verificación 4 (12:09: 1 LOW R4-N1) | 11-nov 11:49 PST | 11-nov 12:09 PST | 20 min | auditoria_U181/REVERIF4.md |
| R2.10 | Clips L2x2x18 GA +131 PCS (R4-N1) + cadena 12:10-12:18 + armar: corrida 8 VERDE + re-verificación 5 (12:27: 0 abiertos) | 11-nov 12:09 PST | 11-nov 12:27 PST | 18 min | auditoria_U181/REVERIF5.md |
| R2.11 | Subida bloqueada (BE-CF27: skill sin U-180..U-184) -> skill v81cf94 + cadena 12:28-12:36 + armar: corrida 9 ROJA (3 FAIL: bitácora BE-GK38, U-184 protocolo, exclusiones) | 11-nov 12:27 PST | 11-nov 12:46 PST | 19 min | cadena_rev2i.log |
| R2.12 | Correcciones BE-GK38 / U-184 / not rated + cadena 12:49-12:57 + armar: corrida 10 VERDE (13:05, 213/3/0) + re-verificación 6 (13:07: 0 abiertos) | 11-nov 12:46 PST | 11-nov 13:07 PST | 21 min | entrega_rev2/ENTREGA_OK.json, REVERIF6.md |
| R2.13 | Subida tramo 1 (--auditoria-carpeta): cortada por el límite de 2 h de la tarea, ~1,350 de 2,502 archivos de Auditoria/ | 11-nov 13:07 PST | 11-nov 15:08 PST | 121 min | subida_rev2.log |
| R2.14 | Subida tramo 2 (retoma R80f.42) - EN CURSO | 11-nov 15:08 PST | 11-nov 15:19 PST | 11 min | subida_rev2_t2.log |
| **TOTAL rev1** | Arranque -> entrega rev1 (incl. subida 07:20-07:32) | 10-nov 21:01 PST | 11-nov 07:32 PST | **631 min** | 10.52 h |
| **TOTAL rev2** | 07:32 -> 15:19 (subida aún en curso) | 11-nov 07:32 PST | 11-nov 15:19 PST | **467 min** | |
| **TOTAL rev1 + rev2** | | 10-nov 21:01 PST | 11-nov 15:19 PST | **1098 min** | 18.30 h; 0.443 h por 1,000 SF (41,287 SF, A000) |

- corridas de compuerta rev2: 10 (1 cortada al llegar la auditoría, 1 colgada 43 min, 1 cortada por re-armado de la GUIA; 3 ROJAS; 4 VERDES). El TIEMPOS.md dentro de la entrega rev2 dice 9: no contó la corrida 1 cortada (08:48-09:29).
- Presupuesto U-180 (<= 2 h por ronda de corrección): rev2 lo pasó; causas: cuelgue de 43 min (BE-GK35), 6 re-verificaciones de la auditoría con hallazgos reales, 2 cambios de versión del skill (v81cf92 -> v81cf94) y la subida de 2,502 archivos sueltos de Auditoria/ (~13 por minuto).
- NOTA: TIEMPOS.md de la entrega rev2 dice 9 corridas; real = 10 (corrida 1 cortada 08:48-09:29). No se re-arma rev2 (COORDINACIÓN, U-180 (4) / U-177); va a Auditoria/HISTORIAL_CAMBIOS solo si hay una revisión siguiente.
