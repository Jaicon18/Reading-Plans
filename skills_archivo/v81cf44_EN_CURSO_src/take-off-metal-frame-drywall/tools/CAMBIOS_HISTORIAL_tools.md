# CAMBIOS_HISTORIAL_tools.md — historial de cambios de tools v70 → v81cf21 (unido en v81cf23 para quedar < 200 archivos; texto literal de cada archivo original)

<!-- ===== archivo original: CAMBIOS_HISTORIAL_tools_v70_a_v77.md ===== -->


<!-- ===== CAMBIOS_tools_v70.md ===== -->
# CAMBIOS tools v70

Una línea por cambio: archivo · qué · test (todos sintéticos; cada test falla con el código / dato viejo).

1. particion.py · `MODO_DEFAULT = "run"` (decisión del estimador: run continuo del mismo type con quiebres o esquinas = un solo wall; una T no encadena; "tramo" queda como opción) · test_particion_v70.py `test_default_es_run`, `test_l_de_dos_segmentos_es_un_wall_por_default`, `test_t_no_encadena_por_default`
2. particion.py · `door_bulkhead` tipado `BULKHEAD-<familia>` (familia = letras iniciales, misma convención que partition_types R7; sin tag usa `bulkhead_of`): nunca se une con sus walls G / G1 · test_particion_v70.py `test_bulkhead_entre_dos_stubs_g`, `test_familia_igual_a_partition_types`
3. particion.py · unión de "tramo" por componentes conexas (union-find): el resultado no depende del orden de los walls; aviso "sin band H|V (ori …)" cuando la band no es H / V · test_particion_v70.py `test_tramo_no_depende_del_orden`
4. inventario_tags.py · nombre canónico de la Etapa 1 (antes inventario.py en v69, que tapaba al inventario de walls de canon.py); docstrings y `inventario.md` lo citan así · test_inventario_tags.py (import corregido), test_sin_colisiones.py
5. etapas.py / comparar.py / README_etapas.md · menciones de la Etapa 1 → `inventario_tags.py` ("ETAPA 1: python3 inventario_tags.py …"); README explica que inventario.py es el inventario de walls que usa canon.py; salidas `1_inventario/inventario.json` sin cambio · test_sin_colisiones.py
6. test_sin_colisiones.py (nuevo) · falla si `canon.inventario` no expone `verificar` / `PURLIN_ELEMS`, si `inventario_tags` no expone `inventario()`, o si un módulo de la carpeta no expone los nombres que otros módulos leen de él (choques previos a v70 en tagband / verif_coherencia / zoom quedan como AVISO) · autoprueba
7. inventario_tags.py · prefijo de id propio por lista (`PT` `PA` `PC` `PX` `DW` `DB` `DR` `KN` `CO`): ids únicos en todo `ocurrencias`; candidatos con `type` = texto y recorte PNG propio verificado · test_inventario_tags_v70.py
8. comparar.py / etapas.py · los candidatos `PC####` entran al cruce (`tags_inventario`): sin wall → alerta "tag sin wall"; sin wall y sin alerta → compuerta FALLA · test_etapas_v70.py `test_compuerta_candidato_sin_wall_y_sin_alerta`
9. etapas.py unir · clave lista en un fragmento y dict / escalar en otro → ERROR "<key>: list in X, dict in Y", rc 1, sin crash · test_etapas_v70.py `test_a_lista_vs_dict_sin_crash`
10. etapas.py unir · texto tipo `notes` distinto → `{fragmento: texto}` + aviso; otro escalar distinto → ERROR con los dos fragmentos · test_etapas_v70.py `test_b_notes_por_fragmento_y_escalar_distinto`
11. etapas.py unir · convención de band: caras > 2 ft × escala en partitions, extensión vs length_ft fuera de ±3 % y 1 ft (salvo `band_length_ok_reason`), "banda traspuesta"; column_wrap / pier no se chequean · test_etapas_v70.py `test_c_banda_traspuesta_y_fuera_de_convencion`, `test_c_escala_del_canon`
12. etapas.py unir / comparar.py · `page` 0-based contra el inventario (`../1_inventario`, `../../1_inventario` o `--inventario`) → ERROR "page 0-based"; comparar rechaza (rc 1) · test_etapas_v70.py `test_d_page_0_based`, `test_d_comparar_rechaza_page_0_based`
13. etapas.py unir · refs de `walls[].openings[]` y `openings_extra[]` contra `opening_schedule` / `opening_list` / `openings` (lista o `{items}`): ref desconocida → ERROR (la tarea de openings escribe las refs primero, Etapa 2a) · test_etapas_v70.py `test_e_refs_de_openings`
14. canon.py · `canopy_soffit` en walls → ValueError (va en runs / ceilings) · test_canon_v70.py `test_a_canopy_soffit_en_walls_rechazado`; test_canon.py: los dos tests de canopy soffit pasan a runs
15. canon.py · roof_step, ceiling_transition, soffit_side, ceiling_bulkhead, vestibule_head, grille_head sin faces ni `faces_none_reason` → ValueError · test_canon_v70.py `test_b_elementos_con_board_exigen_faces`; fixtures de test_canon.py / test_canon_v68.py con `faces_none_reason`
16. canon.py · claves de wall fuera de `WALL_KEYS` con números → ValueError que nombra la clave y el campo del esquema (plywood → plywood_strips, blocking → blocking_items…); sin números → aviso; sufijos de traza `_info` `_note` `_check` `_source` `_status` `_img` `_reason` `_basis` `_desc` `_op` aceptados · test_canon_v70.py `test_c_claves_fuera_de_esquema`
17. canon.py · operación de canopy_joist / framed_soffit: "ROUNDUP(<run_ft>/<oc_ft>)+1 = <n> joists x <joist_len_ft> = <LF>" con el RUN que cuenta joists (oc no exacto se escribe "(16/12)") · test_canon_v70.py `test_d_operacion_canopy_joist_imprime_el_run`
18. canon.py · `constants.deck_breaks.value[]` con `sheet`: el quiebre solo se compara con bandas de esa hoja · test_canon_v70.py `test_e_deck_breaks_por_hoja`
19. accesorios.py · `sill_return: false` + `sill_return_source` N/HOJA: jamb return y trim sin el borde del sill; sill track (headers.py) sin cambio; sin fuente → ValueError · test_accesorios_v70.py `test_sill_return_false_omite_borde_del_sill`, `test_sill_return_false_sin_source`, `test_canon_sill_track_igual_return_y_trim_sin_sill`
20. accesorios.py · `atm_recess.*_status = "CRITERIO"` aceptado con `rfi` (o `<dato>_rfi`); sin rfi → ValueError · test_accesorios_v70.py `test_atm_recess_criterio_con_rfi`
21. plantilla_excel.py verificar · renglón del Material Summary que cita `<tool>_out.json … '<familia>'` con Net 0 mientras la salida da > 0 → error (salidas junto al Excel o `--salidas dir`) · test_plantilla_v70.py
22. closer.py · `abertura(..., piezas=0, header="steel_by_others", header_source="N/HOJA")` = header 0 con fuente (se sella); 0 piezas sin eso → rechazo · test_closer_v70.py
23. headers.py `_src` · partes separadas fuera de paréntesis (mismo splitter que corridas.py) y prefijo "N/HOJA:" aceptado · test_headers_v70.py

## Fase 2

24. partition_types.py · criterio E28: agrupa los walls de cada type con `particion.particion` y `particion.MODO_DEFAULT` ("run"); se conservan PT1 (tipado EXT-6CFMF / EXT-PARAPET / BULKHEAD-<familia> / CANOPY-COL), PT4 (door_bulkheads colineales de un frente = un wall), PT5 (OTHER FRAMING), R8 (chase por cara), R9 (LF de wraps / piers interiores) y R10 en `modo="tramo"` · test_partition_types_v70.py; test_partition_types.py: los asserts de conteo por tramo pasan a `modo="tramo"` y se agrega el caso run
25. canon.py R70.1 · ceiling que no es furring sin `system_callout {detail N/HOJA, on_plan: true, source}` → ValueError (con aviso si la leyenda dice SUSPENDED); fixtures de ceilings stud_joist / framed_soffit / canopy_joist con system_callout · test_canon_v70.py `test_r70_1_system_callout`
26. canon.py R70.6 · pier / column_wrap con parts y tag interior: length_ft = perímetro completo de la caja (Σ caras de todas las partes, o `parts[].faces_ft`) → ValueError; debe ser las caras interiores o declarar `type_lf_basis` · test_canon_v70.py `test_r70_6_pier_interior_no_suma_perimetro`
27. canon.py R70.7 · storefront / curtain_wall desde el piso (sill 0 o sin sill) dentro de un wall → ValueError (framing sobre el head = storefront_cripples) salvo `storefront_in_lf_reason`; G / G1 siguen con la regla 59.7 · test_canon_v70.py `test_r70_7_storefront_desde_el_piso`
28. accesorios.py R70.9 · grille head: si `head_chain_source` dice chain / cadena o la fuente cita al menos dos cotas pies-pulgadas, `head_chain_in` lista todos los eslabones (un solo eslabón → ValueError); stud = Σ cadena − n_box × box_depth − board · test_accesorios_v70.py `test_r70_9_cadena_del_head`
29. accesorios.py · storefront_cripples fuera del bottom track sobre losa de pins / anchors (ON_SLAB ya los excluía; queda con test) · test_accesorios_v70.py `test_storefront_cripples_fuera_de_pins_y_anchors`
30. plantilla_excel.py verificar R70.8 · NET de drywall screws / joint compound / joint tape: fórmula viva a Inputs, o igual a yield de Inputs (celda citada en Yield check) × driver dentro de medio por ciento; si no → "R70.8 yield must come from Inputs" · test_plantilla_v70.py `test_r70_8_yield_desde_inputs`
31. etapas.py compuerta · corre `esquinas.revisar` sobre `4_canon/takeoff_canon.json` si existe y falla con sus fallas (prefijo "esquinas:") · test_etapas_v70.py `test_compuerta_corre_esquinas_sobre_el_canon_final`
32. esquinas.py + test_esquinas.py · incluidos en el paquete (sin cambios) · test_esquinas.py

<!-- ===== CAMBIOS_tools_v71.md ===== -->
# CAMBIOS tools v71 (2026-10-19)

Origen: arbitraje de dos pruebas ciegas (fuera del paquete). Todo genérico; cada cambio con test en `test_v71.py`.

| Tool | Cambio | Regla |
|---|---|---|
| particion.py | modo "eje" (nuevo default): línea recta por tag; esquina / jog / T entre dos líneas con tag corta; segmento sin tag se suma al wall con tag que toca; grupo sin tag = un wall; hueco colineal solo se cruza con un R.O. del wall dentro; exteriores por eje; un pier exterior no vuelve exterior a un type interior; sin tag_ids = corte en esquinas + jogs sumados. "run" y "tramo" quedan como opciones | E28 v71 / R71.12 |
| partition_types.py | pasa `tag_ids` y `openings` a particion; exterior por type (no por un wall suelto); Layers = Σ(layers × largo de face) / LF | R71.12 / R71.13 |
| chequeos_v71.py (nuevo) | R71.1 flecha norte con fachadas; R71.2 box contado dos veces; R71.3 accesorios de bulkhead > Σ vanos; R71.5 (un tag descartado "por otra tarea") | compuerta 0c |
| etapas.py | `compuerta` corre chequeos_v71 sobre el canon conciliado | compuerta 0c |
| headers.py | header_type "ASSUMED" / "NOT PRINTED" = error; CONT. BOX BEAM exige `run_ends` | R71.10 / R71.11 |
| canon.py | pasa `run_ends` / `run_ends_source` a headers; docstrings sin casos de proyecto | R71.11 |
| plantilla_excel.py | `verificar_r71_track`: con ≥ 2 tamaños de stud, bottom / top track un renglón por tamaño; ejemplo sin nombre de proyecto | R71.8 |
| track_por_tamano.py (nuevo) | reparte la familia de track por tamaño / gauge; resto "other"; resto negativo = falla | R71.8 |
| mep.py | sin offsets, página ni comentarios de un set; `arq` obligatorio; registro en cada corrida | R71.9 / E24 |
| vigas_sobre_walls.py | eje dentro de la band manda; dos vigas paralelas con rótulo distinto = `candidatas` + decisión; un dueño por rótulo | R71.14 |
| accesorios.py | slab pins también en chase; PAFs ROUNDUP por run de parapet (`_runs_parapet`) | A7 |
| framed_openings.py | `_src`: la primera parte cita N/HOJA, el resto puede ser texto | — |

Tests viejos ajustados (el default dejó de ser "run"): test_particion_v70, test_partition_types_v70, test_partition_types
(prueban "run" de forma explícita); test_headers y test_canon (fixture CONT. BOX BEAM con `run_ends`); test_plantilla_v68
(fixture con track por tamaño).

<!-- ===== CAMBIOS_tools_v72.md ===== -->
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

<!-- ===== CAMBIOS_tools_v72b.md ===== -->
# CAMBIOS tools v72b (2026-10-19) — reglas inviolables

| Tool | Cambio |
|---|---|
| reglas.py (nuevo) | `compuerta <work_dir> [--excel]`: 67 chequeos (a) + motor de evidencia (b) por caso + catálogo completo; absorbe chequeos_v71, chequeos_v72, esquinas.py y la compuerta de etapas; recalcula las salidas con canon.py (vigencia); sale rc 1 con una falla; `faltantes`, `tabla`; sello del Excel (hoja oculta `_reglas`). Sin flag de override. |
| reglas_catalogo.py (nuevo) | extrae cada regla del SKILL.md y de referencias/ con id estable (ids explícitos E/R/PT/D/A/REGLA nn.n; viñetas por sección + huella del texto). |
| reglas_clasificacion.py (nuevo) | decisión a / b / c de cada regla; 35 specs de evidencia (b); una regla nueva sin decisión = falla. |
| plantilla_excel.py | `armar(d, salida, trabajo)`: corre `reglas.exigir(trabajo)` antes de escribir; exige `--familias` del familias_out.json de la carpeta de trabajo (`_familias_sha` de `fusionar`); sella el libro. CLI: `armar … --familias f [--trabajo d]`. El escritor interno `_escribir` solo lo usan los tests de formato: su libro no trae un sello válido y bitacora / reglas --excel lo rechazan. Ejemplo del docstring sin valores de proyecto. |
| etapas.py | `compuerta(d)` = `estructura(d)` + reglas.py compuerta (fallas "reglas: …"); `estructura` = la compuerta v69–v72. |
| bitacora.py | `compuerta` corre reglas.py en modo final (carpeta de trabajo por $TAKEOFF_WORK o junto al takeoff.json; Excel con sello vigente) y exige `reglas.py compuerta` en la bitácora con rc 0. |
| fixture_reglas.py (nuevo) | proyecto sintético de un wall con todo lo que la compuerta exige (etapas, canon, salidas, registro, bitácora, evidencia). |
| test_reglas.py (nuevo) | un test por regla (668): (a) caso malo / bueno por chequeo; (b) sin evidencia falla, con evidencia pasa, valor "a ojo" contradice; (c) fusión no vacía; armar no escribe con una regla violada. |
| test_ciego_tools.py (nuevo) | E24 sobre las tools (comentarios / docstrings + nombre del proyecto en todo el código). |
| ~50 tools | limpieza ciega: rutas por defecto con el proyecto → $TAKEOFF_WORK; nombres de archivo → $TAKEOFF_PREFIJO; cantidades / refs de proyecto en comentarios → `<n>` / `<ref>`; datos de proyecto en código (handoff, resumen_global, dataset, localizar, verif_*) → JSON de la carpeta de trabajo o variables de entorno. |
| test_etapas.py, test_etapas_v70.py, test_bitacora.py, test_plantilla_v67/v68.py | ajustados al comportamiento nuevo (la compuerta exige reglas OK; casos nuevos 25–28 en test_bitacora y 9 en test_etapas). |

Pendiente conocido (no se tocó para no aflojar compuertas): trinquetes medidos de un proyecto en `verif_idioma.py`
(TOPE_*) y `corpus.TOPE_CIERRES_MIN`, coordenadas de `indice_set.py` y la convención de nombres de bloques de cierre
de las tools v38–v60 (`verif_*`, `dataset`, `resumen_total`): siguen funcionando, pero su genericización completa es
trabajo aparte.

<!-- ===== CAMBIOS_tools_v73.md ===== -->
# CAMBIOS tools v73 (arbitraje #21)

Nuevas: cotas_banda.py, chequeos_v73.py, planmark.py (+ test_planmark), glosario.py, vocab_trade.py,
verif_respuesta.py (+ test_glosario, test_verif_respuesta), correr_suite.py, test_v73.py, test_indice_set.py,
test_registro_v73.py.

Cambiadas:
- reglas.py: v73; chequeos A_R73_1, _2, _5, _6, _7, _8 (consistencia con el plano); fos_chain acepta la forma dict
  de canon.py (P02); regex de anchors / pins aceptan el texto en inglés.
- reglas_clasificacion.py: R73.1–R73.18 clasificadas; R70.5 / R72.5 / R72.9 suman los chequeos v73.
- canon.py: WALL_KEYS + hatch_extent, dim_scan (P01); FRT plywood por material, espesor y USO con nombre de la
  plantilla; track_by_element; metal_blocking_by_origin; nombres_contexto.
- accesorios.py: stud reinforcement MEP solo con ductos de mep.cruces (R73.5; lo demás a RFI con delta); familia
  "deflection clips" (R73.6, P04); todos los textos que llegan al Excel en inglés (P08, R73.9).
- plantilla_excel.py: nombres de renglón de la plantilla (NOMBRES_PLANTILLA, track por elemento, metal blocking por
  origen) (R73.3); regex de yields aceptan el texto en inglés.
- particion.py: R72.7 con límite de distancia (R73.18).
- indice_set.py: genérico, sin coordenadas de un set; arma su propio cache (P05).
- registro.py: `corregir` (F01).
- eval_takeoff.py: rango min == max manda; _partition_types; modo "consistencia" no califica; bloque OTHER no sobra.
- test_ciego_tools.py: revisa test_*.py y fixtures; P6 rooms de tres dígitos, P7 ids de wall de planta, P8 lista externa.
- tests con datos sintéticos (rooms, ids y hojas inventados): test_canon, test_closer, test_headers,
  test_inventario, test_studs_nodos, test_corridas, test_etapas_v70, test_esquinas, test_framed_openings…

<!-- ===== CAMBIOS_tools_v74.md ===== -->
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

<!-- ===== CAMBIOS_tools_v75.md ===== -->
# CAMBIOS tools v75

- canon.py: TRACK_NOMBRES sin "soffit"; renglón "other framing" (R75.2); `ids_partition_takeoff`,
  `verificar_track_nombres` (R75.1); track_by_element después de partition_types; llama chequeos_v75.
- familias.py: EXCLUYE de "track de ceilings / soffits" lo que empieza con bottom / top (R75.1).
- accesorios.py: `_sill_return` sin default cuando hay return y sill; `_label_gyp` (R75.3); `_storefront_de_cripples`
  (R75.4).
- chequeos_v75.py (nuevo): R75.5 `verificar_r75_5`, R75.6 `alcove_con_esquina`, R75.7 `returns_sin_esquina`.
- reglas_clasificacion.py: R75.1–R75.7.
- test_v75.py (nuevo, 7 casos sintéticos); fixtures de test_canon / test_accesorios con jamb_return_label y
  sill_return.
- test_ciego_tools.py: P23 / P24 / P25 (estricto).
- inventario.py, studs_nodos.py, dataset.py: textos genéricos.
- v75b: textos genéricos (canon.py, familias.py, partition_types.py, inventario.py, README_etapas.md); test_ciego_tools P25 con comas y P18 con signo en comentarios.

<!-- ===== CAMBIOS_tools_v76.md ===== -->
# CAMBIOS tools v76

- chequeos_v76.py (nuevo): R76.1 `r76_1` (fascia_box ↔ canopy_joist por facade, canopy_joist → run canopy_soffit,
  hand-off de `otros_ceilings` consumido), R76.2 `r76_2` + `sheathing_column_wraps`, R76.3 `jogs_k` + `r76_3`
  (jog ballistic = hueco entre caras), R76.4 `aberturas_ext` + `r76_4` (substrate de aberturas), R76.5 `r76_5`
  (box con tag), R76.6 `bordes_transicion` + `r76_6_perimetro`.
- canon.py: llama `chequeos_v76.verificar`; `_column_wrap_sheathing` (R76.2); `_opening_substrate` (R76.4); track
  de perímetro de ceiling = perímetro − transiciones con `edge_of` (R76.6); `_polyiso` (nombre del nailbase con el
  espesor impreso); `stud_by_element` (framed soffit en su renglón); blocking material `wood` + `frt_basis`;
  `fos_chain_faces`; R70.6 no exige `type_lf_basis` cuando hay caras interiores con largo; WALL_KEYS con
  `sheathing`, `edge_of`, `beam_override`, `part_of`, `same_box_ok`, `opening_ref`, `type_change_rfi`,
  `anchorage`, `orientation`, `sheets_searched` (las leen otras tools).
- partition_types.py: `TAG_TYPE`; pier / column_wrap con tag de type sigue en su type aunque `location` sea exterior
  (R76.5); parte `part_of` interior de un box con tag suma sus caras al LF del box.
- plantilla_excel.py: `verificar_r71_track` clasifica con familias.py (en su unidad) y toma los tamaños de las filas
  de partition types (no de OTHER FRAMING); renglones `stud_by_element` y "Blocking 2X wood (not labeled FRT)".
- reglas.py: `A_BLOCKING` lee el rótulo (y `frt_basis`), no el source; `A_WRAP_FOS` acepta `fos_chain_faces`.
- reglas_clasificacion.py: R76.1–R76.9.
- bitacora.py: el paso E24 acepta `test_ciego.py` o `test_ciego_tools.py`. armar_ciego.py: `test_ciego.py` viaja.
- test_ciego.py: texto genérico. test_ciego_tools.py: comentario de P18B genérico.
- test_v76.py (nuevo, casos sintéticos por regla).

<!-- ===== CAMBIOS_tools_v77.md ===== -->
# CAMBIOS tools v77 — decisiones del usuario D1-D6 y compuertas R76.7

- canon.py: `_atm_wall` (D1): la wall del ATM con `atm_recess` pasa completa a "extra framing ATM" (studs de
  studs_nodos + bottom + top runner de corridas) y sale de su familia de stud / track (una vez); `front_line` viaja a
  headers.py; R77.7 `carrying_direction` obligatoria con ceilings suspendidos (joists con span propio siguen con span);
  llama chequeos_v77.
- accesorios.py: `atm_recess_valido` ({source N/HOJA, drawn}); la fórmula sistered + furring y `extra_framing` kind
  atm_recess = error; renglón "Extra framing - ATM wall (full wall framing, floor to deck + bottom and top runner)".
- headers.py (D2 / D5): CONT. BOX BEAM con `front_line` (primera a última jamb, ro_w_ft = jambs / escala, dos runs en
  la misma línea = error, run_ends solo jamb_to_jamb); piezas de cada fila del schedule = su rótulo (SINGLE 1,
  DOUBLE 2, "2-…" 2); door con with_sill = error.
- chequeos_v72.py: R72.11 = compuerta D1 (fórmula vieja o atm_recess fuera de un wall = falla).
- chequeos_v77.py (nuevo, D3 / D4): strips de pier por vector con scale_check, jambs × alto impreso, plies del rótulo
  + rfi; pier con `jamb_strips` o `jamb_strips_none_reason`.
- reglas.py: A_BLOCKING lee "F.R.T." (RX_FRT_ROTULO); A_TRACK_RUNS salta el renglón movido a ATM (`moved_to`).
- plantilla_excel.py: `es_texto_es` quita rutas, archivos, ids y coordenadas (R76.7 b); FRT plywood no se valida
  como repartido cuando se rehace desde `frt_plywood_by_material`.
- vigas_sobre_walls.py: `cruzar(..., hoja=)` solo bands de la hoja de planta (R76.7 c).
- bitacora.py: lock fcntl en `anotar` y realpath en hashes / vigencia (R76.7 d).
- copia_limpia.py (nuevo) + inventario_tags.py + alcances.py + arranque.py: siempre la copia sin /Annots; arranque.json
  en la carpeta de trabajo (R76.7 e).
- test_v77.py (nuevo, 13 casos); tests ATM / CONT / ceilings actualizados al esquema v77.

<!-- ===== CAMBIOS_tools_v77b.md ===== -->
# CAMBIOS tools v77b

- canon.py `_atm_wall`: el extra framing del ATM = la partición interior que contiene el ATM de lobby (studs_nodos +
  bottom + top runner de corridas), sin restar de las familias de stud / track; atm_recess en wall exterior = error;
  la wall exige `to_deck: true`; deja `rfi_una_vez` con el delta de contarla una sola vez.
- accesorios.py: suma la wall de `_atm_wall` y emite el RFI "counted once"; mensajes v77b.
- chequeos_v72.py R72.11: atm_recess en una wall exterior (tag EXT*, location exterior) = falla.
- chequeos_v77.py `r77_10`: R.O. de una door fuera del largo del wall (band + xy_pt) = falla.
- reglas.py A_TRACK_RUNS: sin el salto `moved_to`; comentario del rótulo F.R.T. sin N/HOJA de un set.
- reglas_clasificacion.py: R77.10 en vigencia.
- test_v77.py (D1 v77b, R77.10) y test_v72.py (R72.11 v77b) actualizados.

<!-- ===== CAMBIOS_tools_v77c.md ===== -->
# CAMBIOS tools v77c

- canon.py `_atm_wall` (U1, R77.11): el recess de ATM / equipo empotrado está en la wall que lo contiene; esa wall
  tiene que pasar por studs_nodos y corridas (su type lleva el metal); extra framing ATM = 0 (ya no suma la wall,
  ya no exige `to_deck`, ya no rechaza la wall exterior, ya no emite el RFI "counted once").
- accesorios.py (U1): `atm_recess_valido` acepta `extra_printed {source N/HOJA, text impreso, lf, op}` (RFI con
  delta, no suma); `extra_framing` de ATM a mano (kind atm_recess o ref ATM) = error; renglón "Extra framing - ATM
  recess (0: ...)".
- chequeos_v72.py R72.11 (U1): sin falla por wall exterior; extra_framing de ATM a mano = falla.
- canon.py `_sealant` (U8, R77.12): acoustical sealant EXCLUIDO (no calcula details[*].sealant ni sealant_items;
  aviso; `excluidas`); familia propia "sealant at base of gypsum (exterior)" (fuera de OBLIGATORIAS).
- familias.py (U8): familia "sealant at base of gypsum (exterior)" antes de "acoustical sealant".
- eval_takeoff.py (U8): modo "excluir" (sin renglón = EXCLUIDA OK; con renglón = MAL).
- alcances.py (U8): `EXCLUIDOS` (ALC-19 se cierra "EXCLUIDO: ..."; renglón de acoustical sealant en el Excel = falla).
- plantilla_excel.py: `acoustical_err` (U8, en validar y verificar), `EXCLUIDAS_SIEMPRE` (fusionar sobrescribe el
  alcance), `ordenar_revisar` / `revisar_err` / `verificar_v77c` (U9 / U10: fase, type, orden_plano, n/N, total
  anunciado, floor plan A-Z antes que los detalles); hoja Review Items con fila de total y columnas Phase / Type.
- reglas_clasificacion.py: R77.11–R77.16.
- Tests: test_v77.py (U1 reemplaza a D1), test_v77c.py (U7, U8 x3, U9/U10 x2, SKILL), test_v72.py, test_accesorios*.py,
  test_canon*.py, test_plantilla_v68.py actualizados.

<!-- ===== archivo original: CAMBIOS_tools_v80u.md ===== -->

# CAMBIOS v80u (2026-10-31, corrida O'Reilly Evans #1) — sobre v80t

Errores encontrados en la corrida y su solución (regla para todos los proyectos; suite 5/5 OK después de cada cambio):

| Regla | Error | Solución | Tools |
|---|---|---|---|
| R80e.63 | Hojas numeradas "A4.2" / "A2.1" (un decimal) no se reconocían en el runner ni en las compuertas | regex de hoja acepta `[A-Z]{1,2}\d{1,2}\.\d{1,2}`; cita N/HOJA acepta type + hoja ("S21/A1.1") | runner/evidencia.py, completitud.py, cobertura.py, overlay.py; accesorios.py, alcances.py, closer.py |
| R80e.64 | El estimador excluye MEP: canon.py exigía hoja M, accesorios.py exigía barrido P/M, framed_openings / alcance_filtro exigían ítems | `opening_schedule.sources_none.M`, `mep_sweep.excluded_by_estimator {why, source}`, `fo_in.items_none_reason`, `alcance_in.rows_none_reason` | canon.py, accesorios.py, framed_openings.py, alcance_filtro.py |
| R80e.65 | Z-furring (150ZF125-18) sin familia | familia "1-1/2\" Z-furring" (stud_size con ZF / Z-furring); sin renglón de track por tamaño | canon.py, familias.py, plantilla_excel.py, accesorios.py |
| R80e.66 | contar_tags.py fallaba en hoja raster | `HOJA@pN` en página sin texto = NO INVENTARIABLE con rc 0 y JSON con motivo | contar_tags.py |
| R80e.67 | Renglón de track "roof step and heads": el desglose sumaba todos los walls | filtro por elemento (TRACK_HEADS / parapet) | trazabilidad.py |
| R80e.68 | FRT plywood 5/8 ext no entraba al desglose del renglón 5/8 | material `frt_5_8_ext` cae en el renglón 5/8 in. | trazabilidad.py |
| R80e.69 | El runner tomó TAKEOFF_API_KEY del entorno en corrección / cobertura aunque la corrida era por suscripción (31 llamadas) | flag `--sin-api`: claude() nunca llama; correr además con `env -u TAKEOFF_API_KEY` | runner/run_takeoff.py |
| R80e.70 | Tags de hojas raster no tienen tag_ids del inventario | `tag_manual {source "TAG/HOJA", sheet_raster}` cuenta como tag barrido a mano | reglas.py |
| R80e.71 | markups_bluebeam.py no encontraba la hoja raster (sin texto) y no marcaba ningún wall | página declarada en una hoja sin texto se acepta | markups_bluebeam.py |
| R80e.72 | Citas fijas de B&N (A-410 / A-001A / DM-101) se escribían en el Excel de otro proyecto | textos genéricos "default (no sheet)" o la cita del canon; verificación: 0 citas ajenas en el Excel | trazabilidad.py, accesorios.py |

Órdenes del estimador de esta corrida (todas las corridas):
- Solo hojas del trade (las que tengan framing o gypsum board); excluir eléctrico, civil, cabinets, MEP.
- Si el bid set trae markups de otro estimador: copia limpia (copia_limpia.py) y seguir; declarar lo visto.
- Lo que la sesión puede corregir sola, se corrige sin avisar ni pedir nada al estimador.
- Corridas por suscripción: nunca API (R80e.69).
- Comparaciones de calidad solo contra el mejor skill vigente (v80s / B&N rev13).

## rev2 (2026-10-31, misma corrida)
| Regla | Error | Solución | Tools |
|---|---|---|---|
| R80e.73 | Los defaults de accesorios citaban textos impresos de otro set ("SILL TRACK ANCHORAGE…", "Handoff - Approved") y "estimator decision" de otro proyecto como si fueran de este | todo default sale como "default (no sheet): skill standing criterion / precedent of a previous project, not printed in this set [texto original]" | accesorios.py k(), plantilla_excel.py (Inputs lumber) |
| R80e.74 | Framing screws stud-to-track contados en el Z-furring sin track | walls sin bottom ni top track no cuentan tornillos stud-to-track | accesorios.py framing_screws |
| R80e.75 | Productos impresos (anchors, #10 screws, deep-leg track, sheathing screws, clips) quedaban como RFI por falta de familia | familias "printed" (misc_items) + `acc_nombres` conserva el nombre de plantilla y agrega "-> printed product: …"; spacing impreso en constants | canon.py, familias.py, plantilla_excel.py |
| R80e.76 | ORDEN DE FUENTES: lo impreso se carga; el RFI queda solo por la dimensión o el producto en conflicto | lectura dirigida de notas S (S1.1 nota 7, S5.x key notes, secciones) antes de cerrar accesorios | proceso (lectura) |
| R80e.77 | Orden del estimador "excluye toda la tornillería" (O'Reilly, 2026-10-31) | canon `fasteners_excluded {why, source}` → drywall / framing / heavy-gauge screws, slab pins / PAF, expansion anchors en 0 con nota EXCLUDED y la cantidad calculada en la operación; misc de sheathing screws en 0; RFIs solo de tornillería cerrados; clips, angles, track y blocking se quedan. Solo cuando el estimador lo ordena en ese proyecto | accesorios.py, trazabilidad.py |
| R80e.78 | rev4: precedente O'Reilly (24 respuestas del estimador) + familias resilient channel, 1/4" gypsum, flat strap, Z-furring runner, sanitary wall panels; nombre genérico del renglón de clip angles | ver cache_proyectos/SKILL_working.md R80e.78 | canon.py, familias.py, plantilla_excel.py |

<!-- ===== archivo original: CAMBIOS_tools_v80v.md ===== -->

# CAMBIOS tools v80v — assembly O'Reilly Evans CO #1, pass 2 (runner steps 7-11, --sin-api)

| Rule | Error | Solution | Tool |
|---|---|---|---|
| R80e.79 | plantilla_excel armar crashed in trazabilidad.aplicar: "desglose de 'Bottom track - other framing (not a partition type, see source)' suma 97.43 != NET 77.34". The 'other framing' breakdown took every element that is not a Partition Takeoff row, including vestibule heads (VH-B1 / VH-B2 / VH-C, element vestibule_head) that canon.track_by_element puts in their own row 'roof step and heads' (TRACK_HEADS). | The 'other framing' filter now excludes TRACK_HEADS and TRACK_PARAPET elements, the same rule as canon.track_by_element (imported from canon.py). The breakdown sums its NET; no quantity changes. | tools/trazabilidad.py |
| R80e.80 | A printed product (5/S5.1 "2'-0" LONG 3-5/8"x20ga TRACK BRACE AT STRUT SPLICE (362T162-33)") had no family: canon.py rejects misc_items with a familia outside FAMS, so the printed item could not be carried (coverage gap). | New printed family "track brace at strut splice (printed)" (same pattern as R80e.75 / R80e.78): canon.F_PRINTED, familias.FAMILIAS (regex "track brace at strut splice", placed before the track families), plantilla_excel name "Track brace at strut splice - printed product (see Where it comes from)". | tools/canon.py, tools/familias.py, tools/plantilla_excel.py |
| R80e.81 | With --sin-api the runner reaches step 11 (coverage) and raises Alto in claude(): the subscription run never writes runner_resultado.json, although the session is the one that writes the coverage list (prompts/cobertura.md). | In --sin-api mode, --cobertura-lista (until now dry-run only) takes the list written by the session; cobertura.py verifies it the same way and the runner finishes and writes runner_resultado.json. Without --cobertura-lista it still stops as before. | runner/run_takeoff.py (cobertura) |
| R80e.82 | markups.json (resumen of markups_bluebeam.py) gave only counts / totals per type: the per-wall Bluebeam markup list (Subject, Page Label, Length, Depth, Wall Area) asked for the delivery could not be checked without opening the PDF in Revu. | escribir() adds "walls": one row per wall with id, Subject, Page Label, Length (vertex length / sheet scale = what Revu measures), LF takeoff, Depth (wall height = /Depth of the annotation) and Wall Area = Length x Depth. PDF unchanged. | tools/markups_bluebeam.py |

## rev2 (post-audit steps 11 / 12)
| Rule | Error | Solution | Tool |
|---|---|---|---|
| R80e.83 | 44 / 51 Material Summary rows said "N/SHEET: not applicable": trazabilidad's N/SHEET regex only took 3-digit sheets (A-121), never dotted sheets (S21/A1.1, 7/A4.2, 3/S5.3); the ceiling track (and hangers / furring / USG / framed soffit branches) cited fixed sheets of ANOTHER project (1/A-121, 5/A-121, 2/A-221); Z-furring and header rows had no breakdown. | RX_NH / RX_HOJA accept dotted sheet ids; fixed sheets of other projects removed (the item sources are cited, else "default (no sheet)"); new breakdowns: Z-furring per wall (studs_out operation, translated) and header ((R.O. + 1'-4") x pieces from headers_in.json); internal file names / image paths stripped from the citation text. | tools/trazabilidad.py |
| R80e.84 | Visible sheets carried internal text (RESPUESTAS_RFI_ESTIMADOR.md x11, img_* paths, a raw dict {'texto','cita'} in Pending Items C, rev9 / rev4 / pass 2 / R73.6 / "canon" / "the other pass" / A-121 / "estimator criterion" without source) and no gate caught it. | Pending Items option C (dict) is written as text; new gate verificar_texto_cliente (inside verificar_excel -> bitacora / reglas compuerta) fails on internal file names, image paths, raw dicts, process codes (revN, pass N, R7x.y, R80e.n, BE-n), "canon", "the other pass", sheets of other projects and "estimator criterion" without source. Tool texts reworded ("in the set"). | tools/plantilla_excel.py, tools/accesorios.py, tools/trazabilidad.py |
| R80e.85 | One row mixed several products (BE-46): 6" studs (600S162-54 / -43 / -33 + 600S200-54), 3-5/8" studs (-33 / -43 ties), 6" and other-framing tracks (600T125-54 / -43 / -33, 800T125-54), metal trim (corner bead + casing + J + Fry JDM + Fry DRMF), clips (2x2x14ga + L4x4). | trazabilidad splits a stud / track / trim / clip row into one row per product (SSMA designation of the wall gauge or of the item label; track = stud designation S -> T125; trim by kind and Fry code of its own label; clips by label), each with its own N/SHEET and breakdown; the family total is unchanged. | tools/trazabilidad.py |
| R80e.86 | Purchase units: resilient channel sold "by piece" with Pieces = LF; 3"x16ga flat strap bought as "C.R. channel 16 ft"; W-4 edge molding by piece = LF. | Purchase classes: resilient channel -> 12 ft piece (Inputs B17, label updated), flat strap -> coil (LF), edge molding -> trim stick (Inputs B18). Compound / tape keep 0 % waste: SKILL rule "yields sin waste" (method notes, line "Waste 15 % en metal; lo no metal con el factor del board; yields sin waste"), now written in the Inputs notes. | tools/plantilla_excel.py |
| R80e.87 | additional head track raised an RFI (+40 LF) for storefront A, whose head sits on a steel PEMB wind beam (steel by others), contradicting RFI-21 / row 32.73. | An opening on steel by others (header steel_by_others or structure text with "steel") takes no additional head track and no RFI. | tools/accesorios.py |
| R80e.88 | Insulation exclusion read "criterio del estimador: no insulation" (Spanish, no source) and covered "batt" only (polyiso R-9 printed in S21 / S24). | Exclusion key "insulation (batt, sound batt, rigid polyiso, rigid board)" with the written source "estimator standing order (skill standing rule: insulation always EXCLUDED)". | tools/canon.py, tools/accesorios.py |
| R80e.89 | A printed scope (A4.1 key 8: W-4 "provide trim and edge molding around perimeter") had no family. | New printed family "W-4 panel trim and edge molding (printed)" (canon.F_PRINTED, familias, plantilla name). | tools/canon.py, tools/familias.py, tools/plantilla_excel.py |
| R80e.90 | accesorios.py always added an RFI "jamb return width not dimensioned" even with a delta of 0 and the width decided by the estimator. | No RFI when the alternative's delta is 0 or the width source is an estimator decision. | tools/accesorios.py |

## final (respuestas del estimador 2026-11-01)
| Rule | Error | Solution | Tool |
|---|---|---|---|
| R80e.96 | Pending Items mixed the open RFIs with every decided RFI ("CLOSED - ..." rows from rfi_cierre): with the answers in, the estimator could not see what was still open. | rfi_cierre decisions no longer go to Pending Items: they go to the Scope Checklist as "CLOSED" rows with the applied decision (validar accepts estado CLOSED). An RFI still listed as open in takeoff.json keeps its open text even when an earlier decision closed part of it (RFI-01 purlin depth). | tools/plantilla_excel.py |
| R80e.85 (ext.) | Once RFI-20 = B moved the 6" VH tops to deep-leg, the deep-leg row mixed 3-5/8" and 6" web products. | The product split also covers "deep-leg slotted deflection track (printed)", by web size from the item label. | tools/trazabilidad.py |
| (catalog) | SKILL.md section "R80e.91–R80e.95 lecciones O'Reilly pasada 2" was unclassified (reglas.py: rule with no check). | Classified as c (fusion of the existing checks G_LARGO / G_ALTO, board_caras.py, lectura.md, corridas.py + DLT per wall and the R80e.79-90 / R80e.96 tools). | tools/reglas_clasificacion.py |

| R80e.97 | Regla del usuario (01-nov, todos los proyectos): NUNCA crear RFI ni preguntar por trades que no hacemos (ACT + grid / seismic, insulation, stucco, roofing, wood trim Div. 06, MEP, eléctrico, civil, cabinets): se excluyen directo con nota EXCLUDED en Scope Checklist. La exclusión fija de acoustical sealant decía "to be confirmed by the estimator" | texto de exclusión directo, sin "to be confirmed"; RFI-33 (wood trim) retirado como RFI y dejado como exclusión | plantilla_excel.py |

<!-- ===== archivo original: CAMBIOS_tools_v80w.md ===== -->

# CAMBIOS tools v80w (Chuze Fitness Austin Bluffs, 2026-11-01) — sobre v80v

| # | Tool | Error encontrado | Solución | Prueba |
|---|---|---|---|---|
| R80w.1 | arranque.py `_words_de` | pdfplumber abre el set una vez y acumula memoria: 10 GB y > 1 h en 106 hojas vectoriales grandes; la corrida se arrastra | El caché `<pdf>_titleblocks.pkl` se arma antes: `titleblocks_por_hoja.py` (un proceso por hoja, en serie) y `palabras_fitz.py` (PyMuPDF) en hojas lentas; el método por hoja queda en `proceso/titleblocks_metodo.json`; el mapa se verifica contra el índice de hojas | mapa 106/106 = índice |
| R80w.2 | arranque.py `RE_HOJA` | Solo aceptaba `A2.10`; hojas `A101`, `AD101`, `A421.B`, `G001` → mapa vacío | Regex acepta los dos formatos | asserts sintéticos (ok / bad) |
| R80w.3 | arranque.py `_titulo_de_hoja` | Banda del título 7–20 % arriba del número; este title block lo pone a ~3 % → títulos de revisiones | Banda 1.5–20 % + BASURA con AUTHOR / CHECKER / ISSUE / COMMENTS / OWNER CHANGES / STAMP | 75/75 hojas A/G/S con título correcto o legible |
| R80w.4 | arranque.py `clasificar` | DEMOLITION FLOOR PLAN tomado como floor plan principal; "WALL TYPES" no reconocido; door schedule "DOOR AND WINDOW SCHEDULES" no | Demo nunca es FLOOR_PLAN / RCP; WALL TYPE → PARTITION_TYPES; DOOR AND WINDOW SCHEDULE; EGRESS PLAN → CODE; ELEVATIONS → INT_ELEV salvo EXTERIOR | corrida Chuze: A101 / A301 / A601 / G003 |
| R80w.5 | inventario_tags.py `TAG_DIGIT_RE`, `TYPE_RE` | Tag con guion de variante (`A2-3D`) no reconocido | `[A-Z]{1,2}\d{1,2}(?:-\d{1,2})?[A-Z]{0,2}` | asserts sintéticos |
| R80w.6 | inventario_tags.py `types_schedule` | Tabla de partition type de UNA fila (furring 'B': B2E; rated 'X': X6D) no entraba al schedule (exigía ≥ 2 tokens alineados) → tags en planta sin type | Token con dígito bajo el encabezado TYPE de su columna cuenta como "fila única bajo encabezado TYPE" | corrida Chuze: B2E y X6D en el schedule |
| R80w.7 | alcances.py `_sheet_of` | Hoja = ID más repetido del texto → keynotes (A1.11) citados como hojas en el Scope Checklist | Número de hoja del índice del title block (`etapas/1_inventario/inventario.json`); el método viejo solo como respaldo; CITA_RE acepta A101 / A421.B | corrida Chuze |
| R80w.8 | inventario_tags.py `SHEET_RE`, `DETAIL_TXT_RE` | Hojas con sufijo de letra (A421.B, A000.A) leídas como "P-2", "L11"; burbujas a esas hojas perdidas | Sufijo `.X` / `.XX` aceptado | asserts sintéticos |
| R80w.9 | orquestación (constants.plan_scale_by_sheet) | Escala de las plantas ampliadas supuesta igual para todas (1/4"); A432 / A434 son 3/16" | La escala de CADA hoja sale de su rótulo "SCALE:" leído del texto de esa hoja (y se verifica con cota o grid); nunca se copia de otra hoja | corrida Chuze |
| R80w.10 | orquestación (lecturas por zona) | Walls que cruzan dos plantas ampliadas: con la regla "hoja menor" cada lector decide sin ver la otra zona → dobles conteos (mismo wall en A423 y A424; muro norte A426/A435) y huecos (D3G de lockers que cada zona dejó a otra) dentro de UNA misma lectura | Cierre global obligatorio: un lector independiente mide TODOS los walls nuevos en la planta general por type y hoja ampliada (`3_revision/cierre_A101.json`); Σ zonas vs cierre por type y hoja; toda diferencia se abre en imagen antes de conciliar. El registro geométrico entre hojas por líneas / burbujas de grid NO es confiable (key plan y mobiliario contaminan) | corrida Chuze |
| R80w.11 | inventario.py `_mr`, canon.py `_v68_checks` | La compuerta de MR (criterio "solo detrás de toilet / lavatory" de otro set) obligó a cambiar 36 caras de wet rooms a type X aunque la nota del set (A111 nota 3) pide MR en locker rooms / restrooms / pool → dato cambiado para pasar una compuerta (prohibido, R76.7) | `constants.mr_rooms_note {value: [palabras de cuarto], source}` = la nota de wet areas DEL SET habilita MR en esos cuartos; o `mr_source` por face (ya aceptado por reglas.py). Sin nota, manda la regla de fixtures | `test_mr_rooms_note.py` (falla con v80v) |
| R80w.12 | reglas.py `HOJA` / `NHOJA`; runner/evidencia.py `HOJA` | Una hoja con sufijo de letra (RCP / elevaciones de la misma planta: X421.A, X000.B) no era HOJA: cientos de evidencias (b) "falta HOJA" con la hoja citada, y evidencia.py asignaba la imagen de la planta (X421) a una cita del RCP (X421.A) | Sufijo `.X` / `.XX` aceptado en los tres regex (mismo criterio que R80w.8 en inventario_tags) | `test_hoja_sufijo.py` (falla con v80v) |
| R80w.13 | chequeos_v73.py `r73_8` | Una operación escrita que termina la frase con punto ("... / 18 = N. Texto") daba `float('N.')` → ValueError y TODAS las reglas A_R73_* fallaban por excepción, sin decir qué wall | El número inicial se lee con `\d+(\.\d+)?` (el punto final de frase no es parte del número); la regla sigue detectando la operación que no cuadra | `test_op_punto_final.py` (falla con v80v) |
| R80w.14 | chequeos_v72.py `r72_2` | Un elemento CURVO (band D con `curved`, p. ej. el lado de un soffit circular) se medía contra el promedio de sus caras rectas (la cuerda): el gate rechazaba el largo verdadero del arco | Band con `curved`: R72.2 exige la operación del arco en length_op (arc = r x theta) en lugar de la cuerda; la diagonal recta sigue igual | `test_curvo_arco.py` (falla con v80v) |
| R80w.15 | alcances.py `compuerta` ALC-12 | ALC-12 exigía furring + carrying channel + hanger + track: un ceiling con drywall suspension grid (main tee + cross tee + hanger wire, sin furring ni carrying) no podía cerrarse cuantificado aunque el Excel trae el grid | `alc12_ok`: vale UNO de los dos sistemas completos (hat channel o grid); un sistema incompleto sigue fallando | `test_alc12_grid.py` (falla con v80v) |
| R80w.16 | closer.py `RE_HOJA` / `RE_DET` / `RE_NHOJA` / `RE_CITA` | Solo aceptaba X12.01 / X-410: en un set numerado X301 / X602 / S200 (sin guion) ninguna partida podía sellarse (toda cita N/HOJA rechazada) | Numeración de 3 dígitos sin guion y sufijo de letra aceptados (mismo criterio que R80w.2 en arranque) | `test_closer_hoja3.py` (falla con v80v) |
| R80w.17 | test_mr_rooms_note.py (test de R80w.11) | El test traía nombres de cuarto y hoja reales del proyecto ("... ROOM <n>", "LOBBY <n>", hoja A111): test_ciego_tools.py (P6) fallaba y el paquete de tools no era ciego (E24) | Cuartos y hoja sintéticos (X1 / X2 / X111); la lógica probada es la misma | `test_ciego_tools.py` rc 0; `test_mr_rooms_note.py` OK |
| R80w.18 | trazabilidad.py `aplicar` (desglose de studs) | Wall con stud_size no literal ("PENDING - 6\" assumed (RFI)", "3-5/8\" + 6\"") quedaba fuera del desglose de su familia (igualdad exacta) mientras canon.py sí lo suma: desglose corto -> ValueError y el Excel no se armaba | `_fam_stud`: misma regla que canon.STUD_FAM (primera clave contenida) | `test_traza_stud_fam.py` (falla con v80v) |
| R80w.19 | plantilla_excel.py `NO_TEXTO` (verificar idioma) | Una coordenada con rango ("y 1813-1875") en una Location: el regex de ids se comía el rango antes que el de coordenadas y quedaba una "y" suelta leída como español -> verificar rechazaba el Excel | Coordenadas (con rango "a-b", "a -> b") se quitan ANTES que los ids | `test_coord_rango.py` (falla con v80v; desde v81cf24 dentro de test_chuze_r80f8_11.py) |
| R80w.20 | canon.py `out["excluidas"]` (insulation) | El texto de exclusión que canon.py escribe en el Scope Checklist citaba un archivo interno del skill: plantilla_excel.verificar (R80e.84, texto interno en hoja visible) rechazaba el Excel en todo proyecto | Texto sin nombre de archivo ("skill method notes") | `test_excluidas_texto.py` (falla con v80v) |
| R80w.21 | trazabilidad.py `_por_producto` | El renglón de STUDS se partía por cualquier designación SSMA del gauge del wall, incluso la de su TRACK ("track 600T250-54"): salía "6\" metal stud - 600T250-54" (un stud rotulado como track) | Studs se agrupan solo por designación de stud (S); el track sigue por la suya | `test_traza_desig_stud.py` (falla con v80v) |
| R80w.22 | trazabilidad.py `aplicar` / `_por_producto` | Solo las familias "<n> stud (todos los gauges)" tenían desglose por wall y N/HOJA: el renglón 2-1/2" stud salía "default (no sheet)" sin desglose | `_es_fam_stud`: toda familia de stud de canon.STUD_FAM (sin parapet / Z-furring) | `test_traza_stud25.py` (falla con v80v) |
| R80w.23 | canon.py `_ceilings` (usg_grid) | El drywall grid cargaba SIEMPRE channel molding + angle molding en todo el perímetro (2x) aunque el spec imprima una sola molding | Campo `moldings {value: [angle / channel], source}` por ceiling; sin el campo, las dos (comportamiento anterior) | `test_grid_moldings.py` (falla con v80v) |
| R80w.24 | canon.py `out["nombres_familia"]`; plantilla_excel.py `nombre_plantilla` | El nombre del renglón era fijo de la plantilla (marca de otro proyecto) aunque el spec del set imprima otro producto | `constants.product_names {familia: {value, source}}` -> familias_out.nombres_familia -> nombre del renglón | `test_grid_moldings.py` (falla con v80v) |
| R80w.25 | markups_bluebeam.py `eje_canon` | Un soffit curvo se dibujaba como su cuerda (2 puntos) y una caja de 3 caras como rectángulo cerrado: Bluebeam medía otro largo que el cargado | `band.path [[x, y], ...]` = eje dibujado explícito (abierto salvo que cierre); sin path, como antes | `test_markups_path.py` (falla con v80v) |
| R80w.26 | markups_bluebeam.py `escribir` | Metadata del PDF entregable con keywords / creator = nombre de la herramienta (R80e.29 f) | keywords y creator vacíos; verificar ya no depende de keywords (leyenda = última página) | `test_markups_path.py` (falla con v80v) |
| R80w.27 | trazabilidad.py `aplicar` (bracing C.R. channel) | El desglose del bracing solo sumaba las filas de corridas: un miembro de bracing declarado en misc_items (filas extra de un tramo más alto) dejaba el desglose corto -> ValueError, sin Excel | El desglose suma también los misc_items de la familia (y cita sus N/HOJA) | `test_traza_bracing_misc.py` (falla con v80v) |
| R80w.28 | trazabilidad.py `RX_NH` / `RX_HOJA` / grid | "Where it comes from" perdía hojas de 3 dígitos sin guion (A101) y con sufijo (10/A505.B -> 10/A505), y el grid de drywall citaba "default (no sheet)" aunque sus ceilings citan C-5/A121 | Regex aceptan los dos formatos; el grid cita las fuentes de sus ceilings | `test_traza_hojas.py` (falla con v80v) |
| R80w.29 | trazabilidad.py (renglones en 0) | Expansion anchors / PAFs / coiling grille en 0 llevaban un texto fijo que pisaba el motivo del canon (accesorios_none con su hoja): el renglón salía "default (no sheet)" | El texto fijo solo si el canon no trae motivo | `test_traza_none_canon.py` (falla con v80v) |
| R80w.30 | alcances.py ALCANCES ALC-16 | ALC-16 (blocking) solo contaba "FRT blocking": con la madera excluida, el backing METÁLICO impreso (6 x 16 ga track, straps) no podía cerrarse cuantificado | ALC-16 acepta FRT blocking o metal stud blocking > 0 | `test_alc16_metal.py` (falla con v80v) |
| R80w.31 | canon.py `track_by_element`; trazabilidad.py (top track) | Un solo renglón "Top / deflection track" por tamaño mezclaba el top track estándar (walls que no llegan a estructura) con el slip / deflection track de 2" (walls a estructura): dos productos en un renglón (BE-46) | `walls[].top_track_kind` (slip / standard + fuente del head detail) -> dos renglones por tamaño con su desglose y N/HOJA; sin el campo, como antes | `test_track_kind_label.py` (falla con v80v) |
| R80w.32 | plantilla_excel.py OTHER FRAMING | Las filas de OTHER FRAMING se rotulaban con la clave del esquema ("soffit_side #id") en una hoja del cliente | `etiqueta_elemento`: inglés llano + detalle ("Soffit side (16/A502)") | `test_track_kind_label.py` (falla con v80v) |
| R80w.33 | plantilla_excel.py Inputs / exclusiones; canon.py / accesorios.py insulation | Celdas visibles con "skill standing input / rule" (texto interno del método) | Textos de cliente: "estimator standing input / order" | `test_track_kind_label.py` (falla con v80v) |
| R80w.34 | canon.py misc_items | Un miembro de stud del canon (box header, kicker, brace) sumaba LF pero 0 piezas: el driver de framing screws (4 por pieza) no lo veía | `misc_items[].pcs` (entero) pasa a la fila -> accesorios.piezas lo suma | `test_misc_pcs.py` (falla con v80v) |
| R80w.35 | canon.py usg_grid `moldings.curved`; familias.py; plantilla_excel.py; trazabilidad.py | El tramo curvo de un perímetro de drywall grid (molding curva impresa en el spec) se cargaba con la molding recta | `moldings.curved {ft, source}` -> familia "curved perimeter molding (printed)" (sale de la recta), con regex de familia, clase de compra (molding por pieza) y desglose | `test_curved_molding.py` (falla con v80v) |
| R80w.36 | canon.py `top_track_tramos` / `track_by_element`; trazabilidad.py | El split slip / standard del top track (R80w.31) salía de la letra del head detail: walls de head C con studs al deck quedaban en "standard (walls not reaching structure)" (auditoría rev2 check 3) | La familia sale de si los studs llegan a estructura en el canon: `height_ft >= deck_height` -> slip / deflection; por debajo -> standard; una zona de altura al deck (`height_zones[_info]` from_x / to_x + `plan_scale_by_sheet`, o `length_ft`) pasa su parte a slip; fuente = altura vs B.O. deck + `constants.slip_track_rule` (opcional); sin deck / altura: `top_track_kind` declarado | `test_track_por_estructura.py` (falla con v80w.35) |
| R80w.37 | canon.py misc_items (`es_fastener`, `RX_FASTENER`) | La decisión del estimador "excluye toda la tornillería" (`fasteners_excluded`, R80e.77) solo ponía en 0 las familias de accesorios.py: los fasteners del canon (TEK impresos, cement board screws, P.A.F., anchors de detalle) seguían cargados | Con `fasteners_excluded {why, source}` cada misc_item de una familia de tornillería / anclajes queda en 0 con la fila "EXCLUDED - ... ; computed before the exclusion = X"; clips, angles, track y demás materiales siguen cargados | `test_fasteners_canon.py` (falla con v80w.36) |
| R80w.38 | plantilla_excel.py `familias_faltantes` | Una familia del canon que el estimador excluye quedaba en 0 y su renglón desaparecía del Material Summary (la exclusión no se veía) | Una familia en 0 con fila "EXCLUDED - ..." sale con NET 0 y su nota en "Where it comes from"; una familia en 0 sin exclusión sigue sin renglón | `test_excluded_zero_row.py` (falla con v80w.36) |
| R80w.39 | canon.py `_existing_walls`; plantilla_excel.py (bloque EXIST_TYPE); markups_bluebeam.py (`walls`, `tipo`, `contenido`) | El board de cara completa en muros EXISTENTES (decisión del estimador sobre keynotes de demolición "remove existing finish ... where required" / "repair") entraba como misc_items: no salía en la Partition Takeoff ni tenía markup en Bluebeam (auditoría FINAL) | `existing_walls[] {id, sheet, page, keynote, path (tramos rectos H / V), length_ft = path / escala de la hoja, height_ft, faces, layers, board, location, source, decision}`: canon suma el board y lo valida; la Partition Takeoff los lista en el bloque "EXISTING WALLS TO REMAIN - BOARD ONLY" con SUBTOTAL; markups: una PolyLine por muro (Subject "EXISTING - BOARD ONLY", Depth = altura, Contents LF / H / caras / SF / keynote / id) | `test_existing_walls.py` (falla con v80w.38) |
| R80w.40 | accesorios.py (R80e.77) | Con la tornillería excluida, la fila en 0 de cada familia perdía la hoja de donde salía el item ("N/SHEET: default (no sheet)") | La fila excluida conserva las hojas del cálculo / none-reason + la regla del estimador | `test_fastener_sheet.py` (falla con v80w.39) |
| R80w.41 | canon.py F_PRINTED; familias.py; plantilla_excel.py (nombre, COMPRA_V68, NO_METAL_CANON) | Ítems impresos en el spec sin familia: malla álcali-resistente en juntas de cement backer (09 29 00 2.7.B.4 / 09 30 13 3.3.K) y sealer gasket bajo runners de 05 40 00 (2.9.E) caían en 'joint tape' / 'cement board' / track o no tenían renglón | Familias impresas "alkali-resistant mesh tape (printed)" y "sealer gasket (printed)" (misc_items con source + op), con su regex antes de cement board / tape / track, compra en rollo (LF) y waste no metal | `test_spec_items.py` (falla con v80w.40) |
| R80w.42 | trazabilidad.py `_por_producto` | El producto que el spec pide para una pieza (curved-edge cornerbead en el arco) y el grado / recubrimiento de un miembro 05 40 00 (A1003, G60) no se veían en el renglón | `trim_items[].product {value, source}` parte el renglón de trim por producto; `constants.product_specs {designación: {value, source}}` agrega el grado al renglón de esa designación | `test_spec_items.py` (falla con v80w.40) |
| R80w.43 | canon.py `_bracing_top_row` | La regla de bracing ROUNDUP(H x 12 / spacing) - 1 no pone una fila a <= 12" del tope; el spec (09 22 16 2.2.C.1) la pide en los walls con slip track | `constants.bracing_top_row_at_structure {value, source}`: +1 fila x LF de slip track de cada wall que llega a estructura (R80w.36), filas con ref "<wall> top row" en el desglose | `test_spec_items.py` (falla con v80w.40) |
| R80w.44 | plantilla_excel.py Inputs | La ficha del proyecto (R-ALC-09: nombre, dirección, tipo, owner / tenant, arquitecto, GC / bidders, bid set, SF, pisos, construction type, occupancy, códigos, occupant load, sprinklers, demo, specs) no tenía lugar en el Excel | `project_data [{campo, valor, hoja}]` en takeoff.json -> filas informativas debajo de los Inputs (mismas 3 columnas, sin celdas amarillas, [PENDING] sin hoja); no se agregan hojas ni columnas | `test_project_data.py` (falla con v80w.43) |
| R80w.45 | familias.py EXCLUYE | Un renglón "5/8 Type X MR" (MR con núcleo Type X, 09 29 00 2.3.E) caía en la familia Type X (regex "type x" antes que "moisture") | EXCLUYE de Type X: "moisture" -> el renglón va a la familia MR | `test_mr_typex.py` (falla con v80w.44; desde v81cf24 dentro de test_chuze_r80f8_11.py) |
| R80w.46 | plantilla_excel.py `verificar_excel`; bitacora.py compuerta (pasa la carpeta del `--familias` de armar) | (1) Un renglón de accesorios renombrado por el canon (acc_nombres: joint compound setting-type, 09 29 00 2.7.C) fallaba "sin la familia de accesorios"; (2) la ficha del proyecto (R80w.44) cita nombres propios del plano ("Camino del Rio") y el chequeo de idioma los marcaba en español | (1) el nombre esperado sale de familias_out.json (accesorios.nombres_excel) cuando está junto al Excel / en --salidas; (2) en las filas de la ficha se revisan rótulo (A) y hoja (C), no el valor citado (B) | `test_verificar_renombre.py` (falla con v80w.45) |
| R80w.47 | trazabilidad.py `_nota_ms` | Una decisión del estimador sobre un RFI (opción elegida, alternativa con su delta, dónde verificar) no tenía lugar en el renglón del Material Summary que cambia | `constants.ms_notes [{match (regex del nombre del renglón), note, source}]` -> " \| <note>" al final de "Where it comes from" del renglón (y de los renglones partidos por producto) | `test_ms_notes.py` (falla con v80w.46) |
| R80w.48 | plantilla_excel.py `verificar_excel` | Una fila nueva del Material Summary volvió a salir con "N/SHEET: default (no sheet)" (jamb return FINAL3) aunque las hojas estaban en el texto: ninguna compuerta lo detectaba | verificar falla toda fila cuyo "Where it comes from" diga "N/SHEET: default (no sheet)" (la hoja va en la fuente del ítem) | `test_no_sheet_and_misc_product.py` (falla con v80w.47) |
| R80w.49 | trazabilidad.py `_por_producto` | Una familia impresa con dos productos de compra (sill sealer gasket 1/4" vs isolation strip felt / 1/8" vinyl) salía en un solo renglón | `misc_items[].product {value, source}` parte el renglón de esa familia por producto (como trim_items, R80w.42) | `test_no_sheet_and_misc_product.py` (falla con v80w.47) |

<!-- ===== archivo original: CAMBIOS_tools_v80w_VS.md ===== -->

# CAMBIOS tools v80w — Victoria's Secret #679 Downey (runner --sin-api, 2026-11-01)
| Regla | Error | Solución | Tool |
|---|---|---|---|
| R80e.98 | Lectura listó RTU support de madera con cantidades + RFI | Madera EXCLUIDA directo (Scope Checklist), sin cantidad ni RFI | SKILL.md, reglas_clasificacion |
| R80e.99 | completitud.py se caía con types_none_reason en lista | acepta lista [{type, why, source}] | runner/completitud.py |
| R80e.100 | Storefront estructural dentro de "header / box beam" (A_HEADER_LF 963 vs 208) | familia "storefront structural framing (printed)" | canon, familias, plantilla_excel |
| R80e.101 | "no dimension string read" disparaba G_CADENA | la negación no dispara | reglas.py |
| R80e.102 | R73.7 falso en sets por hatch (board un lado) y en cajas | espesor = stud + capas por LADO; cajas fuera | chequeos_v73.py |
| R80e.103 | Lecturas no leyeron el demolition plan (deck 17'-0" / structure 12'-1") | lectura.md: demolition plan obligatorio antes de "no impreso" | runner/prompts/lectura.md |
| R80e.104 | trazabilidad "track - other": 809.46 != 49.36 | filtra sin tamaño + resto de familia | trazabilidad.py |
| R80e.105 | _val_op tomaba "= 6\" strip" de una cita | prefiere "= V <unidad>" | trazabilidad.py |
| R80e.106 | ALC-12 exigía furring/carrying con drywall grid; ALC-16 solo FRT | grid y blocking metálico cierran | alcances.py |
| R80e.107 | Productos impresos sin familia (reveal P-224, plate 24x24 20 ga, metal FRP trim) | 3 familias impresas | canon, familias, plantilla_excel |
| R80e.108 | markups_bluebeam: 0 anotaciones (sheet number en curvas) | usa la página del canon | markups_bluebeam.py |
Suite correr_suite.py: 5/5 OK.

<!-- ===== archivo original: CAMBIOS_HISTORIAL_tools_v80x_a_v81cf21.md ===== -->

# CAMBIOS de tools v80x, v81cf8, v81cf11 y v81cf21 (unidos en v81cf21 para quedar < 200 archivos; texto original sin cambios)

<!-- archivo original: tools/CAMBIOS_tools_v80x.md -->
# CAMBIOS tools v80x — VS #679 Downey rev2 (paso 11 auditor + paso 12 biblioteca)
| Regla | Error (paso 12) | Solución | Tool |
|---|---|---|---|
| R80e.109 | BE-102 citas truncadas (C/A12) y ids de wall leídos como hojas | RX_NH: punto primero; sin guion 3 dígitos | trazabilidad.py |
| R80e.110 | BE-46 storefront y clips mezclaban productos | split por miembro / designación de clip | trazabilidad.py |
| R80e.111 | BE-46 foil-backed como "regular", 1/2" MR como "exterior sheathing" | boards "5/8 foil-backed" y "1/2 MR" con familia / renglón | canon, familias, plantilla, trazabilidad, inventario |
| R80e.112 | BE-15 blocking como stud 3-5/8"; split duplicaba familia | split backing track / plate + guard NET | trazabilidad, plantilla |
| R80e.113 | track de soffits por tamaño no sumaba sus ítems | + items_filas | trazabilidad |
| compra | BE-51 reveal: piezas = LF | trim stick 10 ft | plantilla_excel |
Suite 5/5 OK.

<!-- archivo original: tools/CAMBIOS_tools_v81cf8.md -->
# CAMBIOS tools v81cf8 (02-nov-2026, CFA #2284 River Point back-check rev2) — generic, all projects

| Id | Tool | Problem | Fix | Test (fails with v81cf7) |
|---|---|---|---|---|
| T1 / BE-CF16 | canon.py `nombres_contexto.z_size`; plantilla_excel.py `nombre_plantilla` | The Z-furring row was always labelled "1-1/2\" Z-furring channel" even when the set prints a 2" Z channel | z size from `constants.z_furring_size {value, source}` or from the stud_size of the walls in the Z-furring family; the row label shows it; absent / 1-1/2" = old label | `test_z_size_label.py` |
| T2 / BE-CF15 | canon.py (F_SAG, BOARD_FAM, FAMS, optional); familias.py; plantilla_excel.py name; accesorios.BOARD_DRIVER; trazabilidad.py board key; alcances.py ALC-11 (+ 1/2" families in ALC-07) | A spec "Ceiling Type" (sag-resistant) board had no board key: carried as "5/8 regular" with a note | board key "5/8 ceiling sag-resistant" -> family '5/8" gyp ceiling board SAG-RESISTANT', row "5/8\" gypsum ceiling board, SAG-RESISTANT (ceiling type)", in the finishing driver and in ALC-11 | `test_sag_board.py` |
| T3 / BE-CF17 | canon.py F_PRINTED; familias.py; plantilla_excel.py name / NO_METAL_CANON | Setting-type compound at cement board joints had no LB family (note only, not bought) | printed family "setting-type joint compound at cement board (printed)" in LB (misc_items, yield x cement board SF) | `test_setting_compound_yield.py` |
| T4 / BE-CF17 | plantilla_excel.py `YIELD_CANON` in `familias_faltantes` | Yield-based canon rows (mesh tape) got the 6 % non-metal waste against the Inputs rule "yields carry no waste" | mesh tape and setting compound rows: waste none (0 %), roll (LF) / lb | `test_setting_compound_yield.py` |
| T5 | plantilla_excel.py `_escribir` | OTHER FRAMING block of the Partition Takeoff had no SUBTOTAL | "SUBTOTAL OTHER FRAMING" row (LF and board SF), text in col. B | `test_other_framing_subtotal_seal.py` |
| T6 / BE-CF18 | reglas.py `sello_path` / `sellar_sidecar` / `leer_sello`; plantilla_excel.py `_escribir` | The seal was a 7th hidden sheet `_reglas` (in Spanish) inside the delivered workbook | the workbook has exactly the 6 fixed sheets; the seal (huella + sha256 of the saved workbook) goes to `<excel>.sello.json`, read by reglas.A_EXCEL / bitacora; an Excel with the old hidden sheet is still read (backward compatible); a workbook edited after the seal is no longer sealed | `test_other_framing_subtotal_seal.py` |

<!-- archivo original: tools/CAMBIOS_tools_v81cf11.md -->
# CAMBIOS tools v81cf11 (03-nov-2026, CFA #2284 River Point rev4)

| Id | Tool | Problem | Fix | Test |
|---|---|---|---|---|
| BE-117 | markups_bluebeam.py `contenido` / `board_sf` (verificar uses the same function) | The SF in each wall markup was LF x H (framing area) and did not equal the Board (SF) of its Excel row | SF = sum of the wall faces (length x height x layers) - openings, written "X SF board"; walls without faces keep LF x H | `test_markups_board_sf.py` (fails with v81cf10 as delivered) |
| BE-117b | markups_bluebeam.py `contenido` (board-only walls) | board-only SF written with 1 decimal (16.1) vs the Excel 16.14 | 2 decimals, identical to the Excel row (test_existing_walls.py updated: 300.00 SF) | `test_existing_walls.py` |
| BE-117c | canon.py TRACK_NOMBRES["slip"] / track_by_element | The slip / deflection top track row always said "2\" deflection leg" even when the head detail prints a 3" long-legged slotted track | leg from walls[].top_track_leg or parsed from top_track_kind_source ("3\" LONG LEGGED"); default 2" | `test_slip_leg_label.py` |
| BE-117d | trazabilidad.py `aplicar` (N/SHEET of every Material Summary row) | A row with any N/SHEET dropped the bare sheets of its items (gyp ceiling row cited C3/S-241, A2/S-241 but not A-221 where the ceilings are drawn): verificar_markups_excel found DETAIL A-221 not in the row | the bare sheets of the item sources not covered by an N/SHEET are added (same rule as the per-product split) | `test_be117_excel_ids.py` |
| BE-117e | accesorios.py `level5` | op "<ref>: L x (h - base) = SF": the markup checker read <ref> = L (59.69) instead of the SF | op "<ref> <SF> SF = L x (h - base)" | `test_be117_excel_ids.py` |
| BE-117f | trazabilidad.py board rows | 1/2" regular board row had no per-ID breakdown (op text cut at 566 chars), so soffit bottoms / walls of that board could not be matched; ceilings were named "ceiling <room>" | 1/2" gyp board joins the per-board branch (faces + ceilings + items); a ceiling with `id` is listed by its id | `test_be117_excel_ids.py` |


# CAMBIOS tools v81cf13 (03-nov-2026, merge of Chuze FINAL4 patch PARCHE_BE117g_para_v81cf13) — generic, all projects

On top of v81cf12 (BE-115: one cumulative line). Chuze-branch ids R80f.7–R80f.10 renumbered to R80f.8–R80f.11 (R80f.7 = A_MARKUPS_EXCEL in the main line). Chuze files were merged as 3-way diffs (base v81cf10 archive, ours v81cf12); BE-117b–f kept (markup SF = board SF from the canon faces, 2 decimals).

| Id | Tool | Problem | Fix | Test |
|---|---|---|---|---|
| BE-117g | verificar_markups_excel.py `leer_excel` / union | A joined Partition Takeoff row "A+B" (PT2: wall + return): each piece was looked up alone (row "without annotation", TYPE vs a Material Summary row, duplicate Wall ID) — Chuze FINAL4 16 FAIL | `union` {piece -> row}; each piece checked for TYPE / H against its row; LF / SF of the pieces summed and squared against the row (±0.5 %); pieces are not duplicates | `test_markups_excel_union.py` |
| R80f.8 | plantilla_excel.py `verificar_excel`; markups_bluebeam.py `resumen_vigente` | language check failed on a quoted proper name in the R80e.121 "PROJECT DATA" block; with two summaries of the same canon the oldest was verified | exemption for any "PROJECT DATA" block; most recent summary verified | `test_chuze_r80f8_11.py` |
| R80f.9 | markups_bluebeam.py `ajustar_a_lf`, `cargar_board`, `NHOJA_RX` | Bluebeam Length vs printed LF up to 1 %; DETAIL "3D/A301" for A2-3D/A301 | run with diff < TOL_PT drawn at LF length; board_out.json SF only for walls without faces (BE-117b first); hyphenated types whole | `test_chuze_r80f8_11.py` |
| R80f.10 | markups_bluebeam.py `leyendas_por_hoja`, `orden_types` | legend only on a last page | legend box on every marked sheet in schedule order | `test_chuze_r80f8_11.py` |
| R80f.11 | auditoria_entrega.py (new) | delivery audit by eye | delivery audit by program, rc 1 = not deliverable | `test_chuze_r80f8_11.py` |


# CAMBIOS tools v81cf18 (03-nov-2026, Chuze Fitness Austin Bluffs FINAL5) — generic, all projects

On top of v81cf17 (BE-115). Origin: Chuze FINAL5 (RCP ceilings with no markups; orchestrator decision #0: drawn geometry wins over hatch-stroke extents).

| Id | Tool | Problem | Fix | Test (fails with v81cf17) |
|---|---|---|---|---|
| R80f.13 | markups_rcp.py `escribir`, `_pagina`, `_bracing_on`, `_label` | One RCP sheet per project (constants.rcp_sheet): a set with ceilings / soffits on several enlarged RCP sheets (Chuze: A421.A ... A426) got no ceiling markups; ID = room text; lateral-bracing clusters drawn even when the set has none; project-specific legend text (J/A12.02); legend at a fixed corner | every ceiling on ITS sheet (ceilings[].sheet, else rcp_sheet; page by Page Label, title block or rcp_page); polygon found by ceilings[].id or room; NM / ID = id; Contents carries "GWB CEILING <ceiling_tag>"; clusters only unless constants.ceiling_lateral_bracing = false; legend per sheet in the corner with the least ink; one PNG per sheet (<sheet>_rcp_markups.png) | `test_rcp_multihoja.py` |
| R80f.14 | verificar_markups_excel.py `buscar_pdf` | The delivery PDF next to the Excel was looked up with the case-sensitive glob "*markup*": "Proj_Markups_X.pdf" was missed and the older walls-only PDF of 6_markups was verified (A_MARKUPS_EXCEL false failures) | any PDF next to the Excel whose name contains "markup" (case-insensitive) | `test_rcp_multihoja.py` |
| R80f.15 | auditoria_entrega.py | Area annotations (RCP polygons) were reported as "annot without Partition Takeoff row"; ceiling sheets were not in the marked-sheets check | an area annot is squared against the "ID SF" breakdown of the Material Summary and its drawn area vs SF (<= 0.5 %); ceilings[].sheet counted as sheets with elements | `test_rcp_multihoja.py` |
| R80f.16 | markups_rcp.py `sin_hatch`, `_color_hatch` | Rule (Chuze FINAL5 audit): the GWB ceiling = the HATCHED area only, bounded by the faces. A ceiling polygon taken from the room region included parts with no C-5 hatch (white display boxes of the storefront soffit, the corner beyond an L-shaped wall in the shower) | every ceiling polygon is checked against the hatch strokes of its sheet (constants.rcp_hatch_color or the commonest thin stroke color): a part without hatch that touches the polygon boundary (>= 1 SF) is reported and markups_rcp exits rc 1 (polygon must follow the hatch boundary; a closed white sub-region without hatch is a hole); a small interior hole (< 4 SF, device / fan) is an opening and is not deducted; `hatch_check_cause` / polygon `cause` documents an exception | `test_rcp_hatch.py` |

Note (v81cf18 merge): test_rcp_multihoja.py and test_rcp_hatch.py are carried as blocks inside `test_chuze_r80f8_11.py` (package limit of 200 files); every assertion is kept.


<!-- v81cf21 -->
## v81cf21 (HFT Loveland, 03-nov-2026) — R80f.17–R80f.28

Tool fixes de la corrida Harbor Freight Loveland (TOOL_LIMITS_CALC / BACKCHECK_rev2_cierre):
- BE-HF1 / BE-HF1b: hat channel vertical -> familia vertical furring, rótulo impreso, familias.py (R80f.17)
- BE-HF2: canon.MISC_ALIAS 'FRP panels' (R80f.18)
- BE-HF3: furring sin C.R. bracing (R80f.19)
- BE-HF4: vigas_sobre_walls --min-size (R80f.20)
- BE-HF5: A_BRACING con spacing impreso (R80f.19)
- BE-HF6 / BE-HF6b: box beams de misc en A_HEADER_LF y desglose (R80f.21)
- BE-HF7: tamano_stud con designación (R80f.22)
- BE-HF8: cita de hoja suelta (R80f.22)
- BE-HF9: 0 SF en markup de wall sin board (R80f.23)
- BE-HF10: auditoria_entrega --rfis-abiertos + causas (R80f.24)
- BE-HF11: head de Partition Takeoff por tamaño / tipo (R80f.26)
- BE-HF12: braces to structure + spacing bar (R80f.25)
- BE-HF13: bracing solo > altura mínima impresa (R80f.19)
- BE-HF14: una fila por Wall ID + BULKHEAD-<tag> (R80f.27)
- BE-HF15: demo 'faces x layer' (R80f.23)
- BE-HF16: desglose de sill + nota de redondeo (R80f.22)
- BE-HF17: leyenda en orden del schedule (R80f.23)


## CAMBIOS_tools_v81cf25 (03-nov-2026, O'Reilly rev5 — compuerta de entrega en verde)
Errores de la biblioteca: BE-125 (set raster sin OCR: barrido BE-120 ciego), BE-126 (head track adicional cargado en walls de
furring sobre CMU, 32.73 LF sin hoja impresa), BE-127 (cita no literal: "FLAT STRAP" donde A1.1 2.B imprime "FLAT STRIP"),
BE-128 (copia de insumos sin conservar fechas: revisión "vencida" falsa), BE-129 (dos compuertas que se contradicen y
chequeos con falsos positivos sobre texto OCR), BE-130 (runner de v81cf24 no arrancaba: import sin tools/ en el path).
| Regla | Archivo | Cambio |
|---|---|---|
| R80e.151 | compuerta_entrega.py | texto_set: OCR de hojas raster (< 200 caracteres), número de hoja del title block por OCR de la esquina, `ocr` / `sin_texto` / `en_blanco`; CE_RFI_BARRIDO_IMPRESO falla si quedan hojas sin texto |
| R80e.142 | revision_markups.py | altura_impresa: `EL 111'-4"` sin punto = elevación; `PANEL 8'-0"` no es elevación |
| R80e.143 | revision_markups.py | SF del markup = board SF del Excel o LF x H; LF medido con length_cause escrita = AMBER (como verificar_markups_excel) |
| R80e.144 | accesorios.py | additional_head_track: aberturas en walls de furring no llevan head track; fuente del 0 en constants.addl_head_track_none_source |
| R80e.145 | chequeos_biblioteca.py | U-057, BE-12, BE-15, BE-21, BE-50, BE-63, BE-102, BE-CF05 sin falsos positivos (cada error real sigue fallando en el test) |
| R80e.146 | runner/reconcile.py, runner/completitud.py | clase_ext: framing exterior sin tag (EXT / EXT-CFS, wall / storefront_cripples) = una familia |
| R80e.147 | runner/run_takeoff.py | comparar_extra.py después de comparar.py (U-081) |
| R80e.148 | runner/run_takeoff.py | tools/ en sys.path antes de importar chequeos_biblioteca |
| R80e.149 | studs_nodos.py, closer.py | "(furring: 0 jamb studs, ...)" en vez del id interno R80e.137 en el texto que llega al Excel |
| R80e.150 | auditoria_entrega.py | calibracion_raster: /Measure de hoja escaneada = calibración del canon que cita rótulo + medición, <= 1 % del rótulo |
Tests: tools/test_compuerta_entrega.py::test_oreilly_rev5 (bloques test_texto_set_ocr, test_altura_el_sin_punto,
test_revision_markups_be117, test_head_track_furring, test_chequeos_ocr_oreilly, test_reconcile_ext,
test_runner_comparar_extra, test_auditoria_raster).
<!-- ===== CAMBIOS v81cf26 (R80e.152, BE-131, preferencias del día 1) ===== -->
# CAMBIOS tools v81cf26
1. chequeos_biblioteca.py · u_114 / u_115 / u_116 / u_117 / u_118 / u_119 / u_120 / u_121 / u_125 (U-114..U-125) + B lee 1_inventario/inventario.json (inv_full), raíz de la corrida para resolver imágenes, y del PDF de markups tipo / NM / Depth / vértices · test_chequeos_biblioteca (CASOS + test_u118_evidencia_circula)
2. compuerta_entrega.py · CE_SIN_DOLARES (U-018 / U-123) también en celdas visibles del Excel (no fórmulas), formato de moneda y Contents de markups · test_compuerta_entrega (test_entregables_y_docs)
3. runner/evidencia.py · Evidencia.hoja circula en rojo lo citado entre comillas y las cotas ft-in encontradas en la hoja (sin hallazgo = página sin marca: u_118 lo reporta); tags_a_walls agrega a tag_ids de la lectura las ubicaciones del inventario más cercanas del mismo type (nunca quita) · test_u118_evidencia_circula
4. reglas_clasificacion.py · S:r80e-152 clasificada


## CAMBIOS_tools_v81cf28 (04-nov-2026, O'Reilly rev6 — compuerta v81cf26 en verde; sobre v81cf27 CFA)
| Regla | Archivo | Cambio |
|---|---|---|
| R80e.153 | plantilla_excel.py | Review Items, columna Image = nombre de la imagen circulada (os.path.basename); verificar_texto_cliente la acepta (RX_IMG_REVISAR) y sigue rechazando rutas / nombres de archivo en las demás celdas (BE-132) |
Errores: BE-132 (R80e.84 contra U-118: el runner no armaba el Excel), BE-133 (hoja raster: el barrido de tags por programa da
0 ocurrencias; se hace visual por cuadrantes con recortes circulados reabiertos y se escribe en el formato de inventario_tags).
Test: tools/test_compuerta_entrega.py::test_oreilly_rev5 (bloque test_review_image_name).
## v81cf27 (= COORDINACIÓN v81cf26 + CFA #2284 River Point rev5 fixes; originally archived as CFA v81cf25, 03-nov-2026) — archived v81cf24 + delivery-gate fixes (CAMBIOS_tools_v81cf11.md is merged in this file)
- compuerta_entrega.texto_set: sheet number of ROTATED pages (/Rotate 90 / 270, M / P / E / F sheets) read in the displayed page (rotation_matrix); page without a sheet number in the text layer keyed `pN-vector` (BE-CF05 "marked"). Test: test_compuerta_entrega.test_texto_hoja_rotada.
- trazabilidad.aplicar: sill track loaded as misc_items (recess / box runner) joins the BE-HF16 headers.py breakdown (before: 'desglose suma 0 != NET' stopped plantilla_excel armar). Test: same file test_materiales_cfa_rev5 neighbourhood / scratch t_sill reproduced.
- studs_nodos / closer: furring operation text without the internal id 'R80e.137' (plantilla_excel verificar R80e.84 rejected the visible Excel); closer still recognises it. Test: test_project_data.py.
- canon.generar: node 'abut' INTO an existing_walls id (end dies into existing construction, by geometry) = 0 studs like 'free', source required (BE-89 topology). Test: test_project_data.py.
- revision_markups (BE-119): labels with 'N face(s)' / 'N layer(s)' / keynote suffix parsed (SF = the field with SF, id = last token without spaces); 'SF board' compared with the Excel Board (SF); BOARD ONLY / OTHER FRAMING groups; existing_walls height sources read; DERIVED heights re-computed from the printed operands (_derivada) and accepted only when they give the written result; 'to 18" A.F.F.' in inches; no O'Reilly 'RFI-01 purlin' text. Tests: test_markups_excel.py.
- revision_materiales.sumas: compound / tape driver = all gypsum board rows (not only 5/8" Type X); breakdown 'item: op = a LF + item: op = b LF = total LF'. Test: test_compuerta_entrega.test_materiales_cfa_rev5.
- chequeos_biblioteca: RX_DET no longer matches inside 'A-050/A-052' or '2.5.B/A-909'; BE-15 skips keynotes 'KN7/A-201'; BE-102 only treats tokens shaped like the set's sheets (or X-NNN) as sheet citations; BE-14 looks only at the sentence that says 'not printed'; lecturas A / B saved as 2_lectura/canon_A.json / canon_B.json found; DEMO_CRUCE.md found. Tests: test_chequeos_biblioteca.test_cfa_rev5_falsos.

## v81cf28 (CFA #2284 River Point rev6, 03-nov-2026) — v81cf27 + BE-CF21
- chequeos_biblioteca.u_117: existing_walls[].tag_ids and canon tags_descartados (motivo >= 8 chars) dispose of an inventory tag.
- chequeos_biblioteca.u_120: RX_JUNTA only on the last Contents field (Wall ID); keynotes 'KN3 + KN4' / notes 'A.6 + H.2' stripped (RX_NOTA_REF).
- markups_demo: es_area -> Polygon /PolygonDimension (MeasurementTypes 129); piezas_por_eje -> one PolyLine per axis ('<xid> k'), LF / SF by drawn length.
- plantilla_excel.verificar_texto_cliente: IMG_ENTREGADA (proceso/review_img|rfi_img/*.png) allowed in Review Items only.
- verificar_markups_excel: an element whose markups are pieces '<id> k' counts as marked.
Test: tools/test_cf_pruebas.py::test_cf_rev6_dia1 (fails with v81cf27).

## v81cf33 (04-nov-2026, O'Reilly rev7) — R80e.154 / U-137 / BE-139
- tools/palabras_fitz.py (detector de burbujas) (nuevo): detector de burbujas de dos líneas (raster + vector + SHX + marca de elevación + N/HOJA) y conteo independiente.
- compuerta_entrega.py: texto_set guarda `burbujas` por hoja (RX_HOJA_TRADE); comando `burbujas` para un set_texto existente.
- chequeos_biblioteca.ce_callouts: une las burbujas del detector a la cadena; FAIL sin barrido / vacío / sin leer sin verificar; burbujas_verificadas.json.
Test: tools/test_compuerta_entrega.py bloque test_burbujas_oreilly (fails with v81cf32) + test_chequeos_biblioteca.test_callouts_extra.
- compuerta_entrega.auditar_compuerta (U-138): PLAUSIBILIDAD por chequeo (conteo de la evidencia vs esperado_proyecto); test bloque test_auditar_compuerta.

## v81cf34 (04-nov-2026) — chequeos_biblioteca._detalle_verificado: detalle verificado a ojo (detalle_existe + img) en la hoja destino cierra el AMBER del OCR (O'Reilly 10/A5.2). Test: test_callouts_extra.

## v81cf36 (CFA #2284 River Point rev7, 04-nov-2026) — v81cf35 + BE-CF22
- chequeos_biblioteca.CALLOUT: label ([1-9]\d?|[A-Z](\d{1,2}(-[A-Z])?)?) -> 'A3/A-601', 'D1-A/A-625'.
- chequeos_biblioteca.ce_callouts: missing view declared in callouts_no_aplican with an RFI id -> AMBER.
- revision_materiales.tipo_board: 'SHEATHING' (no material) -> AMBER 'material per the wall notes'.
- chequeos_biblioteca.be_vs_13: Subject DEMO markups skipped.
Test: tools/test_cf_pruebas.py::test_cf_rev7_burbujas (fails with v81cf34).

## v81cf37 (CFA #2284 River Point rev8, 04-nov-2026) — v81cf36 + BE-CF23
- chequeos_biblioteca.u_116: open RFI with 'nothing loaded / not loaded / not carried / no cargado' -> FAIL (U-048).
Test: tools/test_cf_pruebas.py::test_cf_rev8_no_cargado (fails with v81cf36).

## v81cf38 (04-nov-2026) — auditoría U-138 sobre v81cf37: u_037 / u_117 (inventario), revision_markups.HOJA_RX + altura sin hoja (CE_ALTURA_IMPRESA, be_78 por cara, u_114), be_25 (GWB-CLG misc / soffits / set), no_impreso_sin_rfi (CE_RFI_FORMATO / CE_RFI_BARRIDO_IMPRESO), be_vs_15 (demo), be_15 (_ref_verificada). Tests: test_auditoria_u138, test_no_impreso_rfi.
- u_116 (BE-CF23): estado del RFI en 'status' o 'estado'; CLOSED / estimator decision = no abierto (falso FAIL en O'Reilly rev7 con v81cf37).
## v81cf39 (CFA #2284 River Point rev9, 04-nov-2026) — v81cf38 (COORDINACIÓN) + BE-CF24
- compuerta_entrega.copia_limpia + CE_COPIA_LIMPIA (U-051).
- chequeos_biblioteca.be_cf24 (Source height text = loaded height) and r_alc_06 (DEMO markups only on DEMOLITION sheets).
Test: tools/test_cf_pruebas.py::test_cf_rev9_auditoria.

## v81cf42 (05-nov-2026, O'Reilly rev8) — U-139: canon.py wood_excluded (blocking FRT / wood + plywood strips = EXCLUDED en 0), trazabilidad (sin desglose para el wood excluido), plantilla_excel (renglón de plywood en 0 con su nota), chequeos_biblioteca.u_139 (wood > 0 = FAIL, caso u_139 en test_chequeos_biblioteca); reglas_clasificacion R80f.45.

## v81cf44 (CFA #2284 River Point rev10, 05-nov-2026) — v81cf43 (O'Reilly) + BE-CF25 + BE-CF26 + BE-CF27 + U-142 + U-143 (3-way, BE-115)
- chequeos_biblioteca.be_cf25 (open 'not printed' RFI needs the full hunt); case in test_chequeos_biblioteca.
Test: tools/test_cf_pruebas.py::test_cf_rev10_busqueda (repeats rev9 RFI-11 / 12 / 20).
- chequeos_biblioteca.be_cf26 (BE-CF26): a resolved / closed RFI speaks from the loaded value (RFI-28: option A said '38.35 SF loaded' after the 34.57 SF resolution). Case in test_chequeos_biblioteca; test tools/test_cf_pruebas.py::test_cf_rev10_rfi_resuelto.
- U-142: compuerta_entrega.marcar_schedules + command `schedules` + CE_SCHEDULES_REVISADOS (test_u142 in test_compuerta_entrega).
- U-143: chequeos_biblioteca.u_143; markups_demo contents without layers; plantilla_excel demolition family text = element area (test_cf_rev11_demo_sf).
- BE-CF27: subir_entrega.candado_ordenes (remote user orders must be in the skill registry before uploading; test_be_cf27).

## v81cf43 (05-nov-2026, O'Reilly rev9) — U-141: compuerta_entrega.marcar_detalles + comando detalles + CE_DETALLES_CIRCULADOS, chequeos_biblioteca.cadena_detalles / _burbujas_pos; markups ignora DETALLES_REVISADOS.pdf. U-140: CE_RFI_BUSQUEDA_EXHAUSTIVA (busqueda_exhaustiva). Test test_u140_u141.
