# CAMBIOS v74 (2026-10-20) — estudio de partición de walls + limpieza del paquete ciego

Origen: alineación wall por wall de la lista del estimador contra dos lecturas del mismo plano. Cada diferencia de
CONTEO se explicó con una regla genérica; ningún número, conteo ni wall de un proyecto entra al skill. Las
diferencias de LF que quedan son de lectura (cota, cara, esquina, door) y van como RFI con delta.

## Partición (particion.py modo "eje" = partition_types.py; SKILL §21)
- R74.1 type por espesor en la línea: segmento sin tag con el espesor de los walls con tag de su línea toma ese type
  (no el de la nota general).
- R74.2 stub aparte: grupo sin tag ≤ 6" que no toca un wall con tag de su type no es wall ni LF de la lista
  (reemplaza R72.7 / R73.18; va a `stubs` / OTHER FRAMING "stub", material en el canon).
- R74.3 nicho / alcove: grupo sin tag que cierra el hueco entre dos tramos colineales de otro type no es wall de la
  lista (va a `anexos` / OTHER FRAMING "alcove").
- R74.4 frente de bulkheads también en particion.py (comparar.py y partition_types dan lo mismo).
- R74.5 box sin tag con la huella de uno con tag = duplicado (no cuenta).
- R74.6 nombres exteriores únicos (EXT-<stud>CFMF, EXT-PARAPET, CANOPY-COL) en particion.py.
- inventario.py avisa R74.1 / R74.5. reglas_clasificacion: R74.1–R74.6.
- Tests: test_particion_v74.py (13 casos, datos inventados); test_v72 actualizado a R74.2.

## Limpieza ciega
- Fugas menores de adendas (v26, v30, v31, v34, v36, v37, v38, v42, v44, v45, v47), herramientas.md, SKILL y
  tools de producción (entregar, traducir_docs, verif_idioma, framed_openings, verif_planos, adyacencia,
  inventario, verif_blocking_schedule, vigas_sobre_walls, handoff, accesorios, headers, contar_tags): conteos,
  coordenadas pt, fechas, ids y títulos de detalle reales pasan a forma genérica.
- Archivos de cierre con nombre genérico: EJEMPLO_cierre.json, PUNTOS_cierres.json (un proyecto con el nombre viejo
  debe renombrarlo).
- test_ciego_tools.py --estricto: P17 conteos de corrida, P18 % de resultado en adendas, P19 nombres / ids / ángulos,
  P20 fechas en referencias/, P21 coordenadas pt, P22 título de detalle junto a N/HOJA.

## Sin cambio (decisiones del usuario)
- Conteo de 3-5/8" stud de las pruebas: aceptado. MEP fuera de calificación.
