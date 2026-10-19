# CAMBIOS tools v72 (2026-10-19)

Origen: arbitraje de dos pruebas ciegas con el mismo skill (fuera del paquete). Todo genérico; cada cambio con test
en `test_v72.py` (18 tests; 17 fallan con las tools v71, el otro es protección).

| Tool | Cambio | Regla |
|---|---|---|
| chequeos_v72.py (nuevo) | compuerta 0d: type K por hatch y sin segmentos sin tag (R72.1); diagonal = promedio de caras (R72.2); `part_of` de la parte sin tag de un box (R72.3); vigas_sobre_walls manda (R72.4); MEP de mep.cruces y FD una vez (R72.5); side A\|B\|END (R72.6); jogs del FRP (R72.10); ATM con alternativas (R72.11). `partes_de_box()` compartida | §18 |
| etapas.py | `compuerta` corre chequeos_v72 (con vigas_out.json si está en 4_canon/ u out/); `unir`: 18 = 18.0, misma constante con fuentes distintas se une, metadatos de primer nivel por fragmento | 0d / P-02 |
| partition_types.py | la parte sin tag de un box va a OTHER FRAMING (`pier_part`): un box = un wall | R72.3 |
| particion.py | `STUB_MAX_FT` = 0.5: grupo suelto sin tag ≤ 6" se suma al wall con tag más cercano | R72.7 |
| accesorios.py | anchors solo element wall exterior; column wrap → pins; parte de box → RFI (R72.8); FD de openings / schedule y del barrido con el mismo WxH una vez (R72.5); plates × filas de studs + RFI (R72.9); jogs del FRP < 6" sin inside corner + RFI (R72.10); ATM: un RFI por alternativa (R72.11) | §18 |
| plantilla_excel.py | `fusionar`: familia citada por ≥ 2 renglones = repartida, conserva NET y Σ = familia; `verificar_r71_track` compara Σ con familias_out.json | R72.12 / R71.8b |
| vigas_sobre_walls.py | docstring: la salida manda (R72.4) | R72.4 |
| board_caras.py | `side: "END"` (return de un box): largo + fuente, fuera de Σ(side) = L, suma board (propuesta de una prueba) | R72.6 |
| cruzar_diagonal.py | genérico: muro desde la band D del canon, offset de mep.registro; sin geometría de un proyecto ni `mep.OFF` (test_sin_colisiones pasa) | R71.9 |
| idioma_es.py (nuevo en el paquete) | `es_espanol(texto)`; antes solo existía en el entorno de la prueba | — |

Tests viejos: ninguno cambiado. Fuera del zip (pedían argumentos o datos externos, ya fallaban así en el stack v71):
test_plantilla.py, test_alcances.py, test_eval_takeoff.py. inventario.py / test_inventario.py de las capas
etapas13 / v69 (inventario de TAGS, renombrado a inventario_tags.py en v70) no viajan: tapaban al inventario de walls.
