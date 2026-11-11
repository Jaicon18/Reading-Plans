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
| **TOTAL** | **Arranque -> entrega** | **10-nov 21:01 PST** | **11-nov 07:20 PST** | **619 min** | 10.32 h; 0.250 h por 1,000 SF (41,287 SF, A000) |
