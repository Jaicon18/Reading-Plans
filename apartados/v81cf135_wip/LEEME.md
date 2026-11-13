# v81cf135 WIP: U-199 (13 controles contra elementos omitidos) + BE-XF16

Estado: EN DESARROLLO (APARTADA, no publicada). La vigente es v81cf134.

## Cómo correrlo sobre un canon

```
python3 -I apartados/v81cf135_wip/tools/compuerta_entrega.py u199 <canon.json> [set_texto.json]
```

Imprime cada control con evaluados / hallazgos. Sale con código 1 si hay hallazgos.
- Lee walls + existing_walls (muros_canon, BE-XF16).
- set_texto.json es opcional. Con él, los controles que dependen del set (keynotes, code plan, secciones, finish schedule, specs, tercer lector) exigen su lista; sin él, no.

## Qué hay

- tools/compuerta_entrega.py:
  - u199_fallas y U199_CONTROLES (1..13);
  - CE_U199_OMITIDOS (AMBER para entregas anteriores a v81cf135);
  - CE_COBERTURA_DIAG (5b): muros diagonales / cortos en el mapa de cobertura, con filtros de texto, remate en otro muro y estilos aprendidos por pares.
- tools/chequeos_biblioteca.py: muros_canon (sin cambios desde v81cf134).
- tools/test_compuerta_entrega.py:
  - test_u199_cierre_por_cuarto_mutacion (quitar una cara = FAIL);
  - test_u199_pisos_gemelos, test_u199_rated_y_excluded, test_u199_resto_controles, test_u199_cobertura_diag_cortos;
  - test_u199_casos_reales_replica (esquema CR: faces = número, cuartos en location).
- LISTA_CR_rev20b.txt: los 14 de pisos gemelos y los 2 EXCLUDED de CR rev20b (mandada a CR).
- ../u199_proto/: prototipo de (6) rated lines desde el code plan raster (A0.01), registrado contra A2.01 por correlación. Atrapa RFI-31: 23 puntos rated sin muro en el canon viejo contra 3 en rev20b. Todavía no está en la compuerta: tiene demasiados falsos en L1 (perímetro CMU).

## Casos reales

| Control | Caso | Canon viejo (takeoff_canon.json) | rev20b |
|---|---|---|---|
| (2) pisos gemelos | UNTYPED-L2-12 (LINEN 222 stub) sin gemelo en L3 | FAIL (lo atrapa) | resuelto (existe UNTYPED-L3-12) |
| (13) EXCLUDED | XW.6.6-L4-16 (F&B 410) sin cara exterior | FAIL (lo atrapa) | resuelto (XW.6.6-L4-16 B contada) |
| (6) rated | Stair 2 exit passage (RFI-31) | prototipo raster: 23 pts sin muro | 3 pts |
| (1) cierre | mutación quitar una cara | FAIL (test) | — |

## Falsos positivos medidos (solo canon, sin set)

- CR rev20b: (2) 14 de 582; (13) 2 de 48 (+ 46 sin 'reverificado', dato que falta); (10) 1; (1) / (5) piden canon.u199.rooms.
- GK rev3b: (3) 26 de 36 puertas sin wall ni center_pt (no verificables); (13) 16 sin 'reverificado'.
- XF: (13) 13 sin 'reverificado'; 5b en A2.0: 3 tramos sin markup (1 real en la jamba de la puerta 103, 1 dudoso, 1 falso por un mop sink).
