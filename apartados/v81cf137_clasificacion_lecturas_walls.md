# v137 — clasificación de las 179 lecturas solo de 'walls' (BE-XF16)

Totales: A = 5, B = 119, C = 55 (179). Ninguna A revertida: ninguna movió cantidades.

Criterio: todo lo que corre dentro de canon.py (canon, accesorios, inventario, studs_nodos, board_caras, partition_types, particion, criterios, vigas_sobre_walls, chequeos_v71/72/75/76/77; lista medida con `python3 -X importtime canon.py`) es cálculo: existing_walls ya se procesan aparte en canon._existing_walls (R80w.39, solo board) -> B. Las lecturas de schema metálico (band, openings, faces por cara, stud_size, nodes) -> B. Las A son chequeos/herramientas fuera del cálculo donde los existing_walls tienen el mismo dato (tag_ids, sheet/page, id, *_op).

| archivo:línea original | clase | qué se hizo | motivo |
|---|---|---|---|
| partition_types.py:398 | C | comentario `# campo:` al final de la línea | conteo de walls por type del resultado de la partición |
| partition_types.py:419 | B | comentario `# solo-metal:` al final de la línea | types / LF de la Partition Takeoff de los walls metálicos; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) y plantilla_excel los lista en su bloque |
| partition_types.py:527 | C | comentario `# campo:` al final de la línea | conteo impreso del resultado por type |
| reglas.py:171 | B | comentario `# solo-metal:` al final de la línea | Ctx.walls() = accesor de los walls metálicos (band / element / faces por cara) que usan las reglas; los board-only entran por chequeos_biblioteca.walls_todos / _walls_board_only (BE-CR10 / BE-CR25) |
| reglas.py:1048 | B | comentario `# solo-metal:` al final de la línea | mep_sweep se exige para el refuerzo de studs MEP de walls metálicos; un set board-only (existing_walls) no lleva studs |
| canon.py:375 | B | comentario `# solo-metal:` al final de la línea | mapa de walls / runs metálicos para el cálculo; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| canon.py:376 | B | comentario `# solo-metal:` al final de la línea | mapa de walls / runs metálicos para el cálculo; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| canon.py:534 | B | comentario `# solo-metal:` al final de la línea | generar(): nodos / studs / track de los walls metálicos; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| canon.py:549 | C | comentario `# nodo:` al final de la línea | lista de ids de walls del nodo |
| canon.py:578 | C | comentario `# campo:` al final de la línea | studs_in['walls'] = entrada de studs_nodos armada aquí |
| canon.py:580 | C | comentario `# campo:` al final de la línea | board_in['walls'] = entrada de board_caras armada aquí |
| canon.py:684 | B | comentario `# solo-metal:` al final de la línea | cálculo de framing / accesorios de los walls metálicos; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| canon.py:842 | B | comentario `# solo-metal:` al final de la línea | cálculo de framing / accesorios de los walls metálicos; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| canon.py:872 | B | comentario `# solo-metal:` al final de la línea | cálculo de framing / accesorios de los walls metálicos; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| canon.py:1044 | B | comentario `# solo-metal:` al final de la línea | cálculo de framing / accesorios de los walls metálicos; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| canon.py:1257 | B | comentario `# solo-metal:` al final de la línea | cálculo de framing / accesorios de los walls metálicos; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| canon.py:1295 | C | comentario `# campo:` al final de la línea | st['walls'] = salida de studs_nodos.contar |
| canon.py:1297 | B | comentario `# solo-metal:` al final de la línea | cálculo de framing / accesorios de los walls metálicos; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| canon.py:1322 | B | comentario `# solo-metal:` al final de la línea | cálculo de framing / accesorios de los walls metálicos; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| canon.py:1362 | B | comentario `# solo-metal:` al final de la línea | cálculo de framing / accesorios de los walls metálicos; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| canon.py:1443 | B | comentario `# solo-metal:` al final de la línea | cálculo de framing / accesorios de los walls metálicos; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| canon.py:1787 | B | comentario `# solo-metal:` al final de la línea | cálculo de framing / accesorios de los walls metálicos; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| canon.py:1805 | B | comentario `# solo-metal:` en línea propia arriba (la línea sigue con `\`) | cálculo de framing / accesorios de los walls metálicos; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| canon.py:1821 | B | comentario `# solo-metal:` al final de la línea | cálculo de framing / accesorios de los walls metálicos; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| canon.py:1852 | B | comentario `# solo-metal:` al final de la línea | cálculo de framing / accesorios de los walls metálicos; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| canon.py:2003 | B | comentario `# solo-metal:` al final de la línea | cálculo de framing / accesorios de los walls metálicos; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| canon.py:2079 | B | comentario `# solo-metal:` al final de la línea | cálculo de framing / accesorios de los walls metálicos; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| canon.py:2178 | B | comentario `# solo-metal:` al final de la línea | cálculo de framing / accesorios de los walls metálicos; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| canon.py:2401 | B | comentario `# solo-metal:` al final de la línea | cálculo de framing / accesorios de los walls metálicos; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| canon.py:2520 | B | comentario `# solo-metal:` al final de la línea | cálculo de framing / accesorios de los walls metálicos; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| canon.py:2554 | B | comentario `# solo-metal:` al final de la línea | cálculo de framing / accesorios de los walls metálicos; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| canon.py:2566 | C | comentario `# campo:` al final de la línea | studs_in['walls'] = entrada de studs armada en generar() |
| canon.py:2575 | C | comentario `# campo:` al final de la línea | board_in['walls'] = entrada de board_caras armada en generar() |
| canon.py:2651 | B | comentario `# solo-metal:` al final de la línea | cálculo de framing / accesorios de los walls metálicos; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| canon.py:2666 | B | comentario `# solo-metal:` al final de la línea | cálculo de framing / accesorios de los walls metálicos; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| entregar.py:286 | C | comentario `# campo:` al final de la línea | conteo 'walls' del resultado del handoff |
| chequeos_v73.py:79 | B | comentario `# solo-metal:` al final de la línea | R73.1 / R73.2: walls K (ballistic, metal) con banda; existing_walls no son K |
| chequeos_v73.py:126 | B | comentario `# solo-metal:` al final de la línea | R73.1 / R73.2: walls K (ballistic, metal) con banda; existing_walls no son K |
| chequeos_v73.py:180 | B | comentario `# solo-metal:` al final de la línea | R73.5: rows de los walls metálicos para el refuerzo de stud MEP; existing_walls no llevan studs |
| chequeos_v73.py:239 | B | comentario `# solo-metal:` al final de la línea | R73.7: espesor medido = stud + capas por cara (schema metálico); existing_walls no tienen stud_size |
| chequeos_v73.py:305 | A | for w in walls + existing_walls (expresión inline) | R73.8: aritmética de length_op / height_op; los existing_walls también escriben su operación |
| plantilla_excel.py:162 | C | comentario `# campo:` al final de la línea | d['walls'] = renglones del Excel armados desde la partición (los board-only van en d['existing_walls']) |
| plantilla_excel.py:610 | C | comentario `# campo:` al final de la línea | d['walls'] = renglones del Excel armados desde la partición (los board-only van en d['existing_walls']) |
| plantilla_excel.py:626 | C | comentario `# campo:` al final de la línea | d['walls'] = renglones del Excel armados desde la partición (los board-only van en d['existing_walls']) |
| plantilla_excel.py:1336 | C | comentario `# campo:` al final de la línea | d['walls'] = renglones del Excel armados desde la partición (los board-only van en d['existing_walls']) |
| vigas_sobre_walls.py:291 | B | comentario `# solo-metal:` al final de la línea | vigas sobre walls metálicos (headers / studs); existing_walls son board-only |
| criterios.py:244 | B | comentario `# solo-metal:` al final de la línea | subcanons por hoja para la partición / bandas de los walls metálicos; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| criterios.py:255 | C | comentario `# campo:` al final de la línea | escribe la lista walls del subcanon |
| eval_takeoff.py:76 | C | comentario `# campo:` al final de la línea | conteo 'walls' del dict de types de la evaluación |
| eval_takeoff.py:97 | C | comentario `# campo:` al final de la línea | conteo 'walls' del dict de types de la evaluación |
| eval_takeoff.py:247 | C | comentario `# campo:` al final de la línea | conteo 'walls' del dict de types de la evaluación |
| eval_takeoff.py:251 | C | comentario `# campo:` al final de la línea | conteo 'walls' del dict de types de la evaluación |
| eval_takeoff.py:258 | C | comentario `# campo:` al final de la línea | conteo 'walls' del dict de types de la evaluación |
| eval_takeoff.py:259 | C | comentario `# campo:` al final de la línea | conteo 'walls' del dict de types de la evaluación |
| eval_takeoff.py:265 | C | comentario `# campo:` al final de la línea | conteo 'walls' del dict de types de la evaluación |
| eval_takeoff.py:267 | C | comentario `# campo:` al final de la línea | conteo 'walls' del dict de types de la evaluación |
| eval_takeoff.py:325 | C | comentario `# campo:` al final de la línea | conteo 'walls' del dict de types de la evaluación |
| track_por_tamano.py:39 | B | comentario `# solo-metal:` al final de la línea | desglose de track por tamaño: existing_walls no llevan track |
| chequeos_v72.py:78 | B | comentario `# solo-metal:` al final de la línea | chequeo del cálculo de framing de walls metálicos (lo llama accesorios); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| chequeos_v72.py:119 | B | comentario `# solo-metal:` al final de la línea | chequeo del cálculo de framing de walls metálicos (lo llama accesorios); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| chequeos_v72.py:190 | B | comentario `# solo-metal:` al final de la línea | chequeo del cálculo de framing de walls metálicos (lo llama accesorios); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| chequeos_v72.py:208 | B | comentario `# solo-metal:` al final de la línea | chequeo del cálculo de framing de walls metálicos (lo llama accesorios); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| chequeos_v72.py:266 | B | comentario `# solo-metal:` al final de la línea | chequeo del cálculo de framing de walls metálicos (lo llama accesorios); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| chequeos_v72.py:301 | B | comentario `# solo-metal:` al final de la línea | chequeo del cálculo de framing de walls metálicos (lo llama accesorios); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| altura_stud.py:93 | B | comentario `# solo-metal:` al final de la línea | altura de stud: solo walls con studs; existing_walls son board-only |
| altura_stud.py:149 | C | comentario `# campo:` al final de la línea | conteo del resumen por type |
| inventario.py:71 | B | comentario `# solo-metal:` al final de la línea | inventario del cálculo (bandas / filas / purlin / MR de walls metálicos); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| inventario.py:145 | B | comentario `# solo-metal:` al final de la línea | inventario del cálculo (bandas / filas / purlin / MR de walls metálicos); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| inventario.py:153 | B | comentario `# solo-metal:` al final de la línea | inventario del cálculo (bandas / filas / purlin / MR de walls metálicos); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| inventario.py:157 | B | comentario `# solo-metal:` al final de la línea | inventario del cálculo (bandas / filas / purlin / MR de walls metálicos); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| inventario.py:158 | B | comentario `# solo-metal:` al final de la línea | inventario del cálculo (bandas / filas / purlin / MR de walls metálicos); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| inventario.py:182 | B | comentario `# solo-metal:` al final de la línea | inventario del cálculo (bandas / filas / purlin / MR de walls metálicos); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| inventario.py:196 | B | comentario `# solo-metal:` al final de la línea | inventario del cálculo (bandas / filas / purlin / MR de walls metálicos); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| inventario.py:249 | B | comentario `# solo-metal:` al final de la línea | inventario del cálculo (bandas / filas / purlin / MR de walls metálicos); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| inventario.py:253 | B | comentario `# solo-metal:` al final de la línea | inventario del cálculo (bandas / filas / purlin / MR de walls metálicos); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| inventario.py:263 | B | comentario `# solo-metal:` al final de la línea | inventario del cálculo (bandas / filas / purlin / MR de walls metálicos); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| inventario.py:293 | B | comentario `# solo-metal:` al final de la línea | inventario del cálculo (bandas / filas / purlin / MR de walls metálicos); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| inventario.py:300 | B | comentario `# solo-metal:` al final de la línea | inventario del cálculo (bandas / filas / purlin / MR de walls metálicos); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| inventario.py:301 | B | comentario `# solo-metal:` al final de la línea | inventario del cálculo (bandas / filas / purlin / MR de walls metálicos); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| inventario.py:312 | B | comentario `# solo-metal:` al final de la línea | inventario del cálculo (bandas / filas / purlin / MR de walls metálicos); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| inventario.py:330 | C | comentario `# campo:` al final de la línea | conteo del resultado del inventario |
| esquinas.py:58 | B | comentario `# solo-metal:` al final de la línea | esquinas / huecos entre bandas de walls metálicos; existing_walls tienen path, no band |
| esquinas.py:89 | B | comentario `# solo-metal:` al final de la línea | esquinas / huecos entre bandas de walls metálicos; existing_walls tienen path, no band |
| esquinas.py:137 | C | comentario `# nodo:` al final de la línea | walls del corner_ok |
| studs_nodos.py:85 | C | comentario `# campo:` al final de la línea | data = studs_in armado por canon.generar() (entrada del cálculo, no el canon) |
| studs_nodos.py:86 | C | comentario `# campo:` al final de la línea | data = studs_in armado por canon.generar() (entrada del cálculo, no el canon) |
| studs_nodos.py:101 | C | comentario `# nodo:` al final de la línea | walls del nodo |
| studs_nodos.py:115 | C | comentario `# nodo:` al final de la línea | walls del nodo |
| studs_nodos.py:123 | C | comentario `# nodo:` al final de la línea | walls del nodo |
| accesorios.py:221 | B | comentario `# solo-metal:` al final de la línea | familias de accesorios del framing metálico; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| accesorios.py:274 | B | comentario `# solo-metal:` al final de la línea | familias de accesorios del framing metálico; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| accesorios.py:398 | B | comentario `# solo-metal:` al final de la línea | familias de accesorios del framing metálico; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| accesorios.py:584 | B | comentario `# solo-metal:` al final de la línea | familias de accesorios del framing metálico; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| accesorios.py:625 | B | comentario `# solo-metal:` en línea propia arriba (la línea sigue con `\`) | familias de accesorios del framing metálico; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| accesorios.py:677 | B | comentario `# solo-metal:` al final de la línea | familias de accesorios del framing metálico; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| accesorios.py:734 | B | comentario `# solo-metal:` al final de la línea | familias de accesorios del framing metálico; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| accesorios.py:765 | B | comentario `# solo-metal:` al final de la línea | familias de accesorios del framing metálico; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| accesorios.py:855 | B | comentario `# solo-metal:` al final de la línea | familias de accesorios del framing metálico; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| accesorios.py:858 | B | comentario `# solo-metal:` al final de la línea | familias de accesorios del framing metálico; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| accesorios.py:999 | B | comentario `# solo-metal:` en línea propia arriba (la línea sigue con `\`) | familias de accesorios del framing metálico; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| accesorios.py:1070 | B | comentario `# solo-metal:` al final de la línea | familias de accesorios del framing metálico; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| accesorios.py:1123 | C | comentario `# campo:` al final de la línea | studs_out['walls'] = salida de studs_nodos |
| accesorios.py:1149 | B | comentario `# solo-metal:` al final de la línea | familias de accesorios del framing metálico; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| accesorios.py:1161 | C | comentario `# campo:` al final de la línea | studs_out['walls'] = salida de studs_nodos |
| accesorios.py:1164 | B | comentario `# solo-metal:` al final de la línea | familias de accesorios del framing metálico; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| accesorios.py:1165 | C | comentario `# campo:` al final de la línea | studs_out['walls'] = salida de studs_nodos |
| accesorios.py:1173 | C | comentario `# campo:` al final de la línea | studs_out['walls'] = salida de studs_nodos |
| accesorios.py:1176 | C | comentario `# campo:` al final de la línea | studs_out['walls'] = salida de studs_nodos |
| accesorios.py:1197 | B | comentario `# solo-metal:` al final de la línea | familias de accesorios del framing metálico; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| accesorios.py:1199 | B | comentario `# solo-metal:` al final de la línea | familias de accesorios del framing metálico; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| accesorios.py:1318 | B | comentario `# solo-metal:` al final de la línea | familias de accesorios del framing metálico; existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| accesorios.py:1320 | C | comentario `# campo:` al final de la línea | studs_out['walls'] = salida de studs_nodos |
| board_caras.py:98 | C | comentario `# campo:` al final de la línea | data = board_in armado por canon.generar() (entrada del cálculo, no el canon); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| particion.py:495 | C | comentario `# campo:` al final de la línea | conteo 'walls' del resultado de la partición |
| particion.py:517 | B | comentario `# solo-metal:` al final de la línea | partición por type de los walls metálicos (bandas); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| particion.py:609 | C | comentario `# campo:` al final de la línea | conteo 'walls' del resultado de la partición |
| particion.py:635 | C | comentario `# campo:` al final de la línea | conteo 'walls' del resultado de la partición |
| chequeos_v77.py:66 | B | comentario `# solo-metal:` al final de la línea | R77 del cálculo de walls metálicos (lo llama canon.py); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| chequeos_v77.py:94 | B | comentario `# solo-metal:` al final de la línea | R77 del cálculo de walls metálicos (lo llama canon.py); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| etapas.py:165 | C | comentario `# campo:` al final de la línea | walls del renglón de cobertura de comparar |
| etapas.py:170 | B | comentario `# solo-metal:` al final de la línea | aviso sin sheet / tag_ids de las lecturas; los existing_walls sin tag los cuenta comparar_extra (untagged_A/B) |
| etapas.py:298 | B | comentario `# solo-metal:` al final de la línea | validar_bandas: band H/V; existing_walls tienen path (canon._existing_walls valida sus tramos) |
| etapas.py:354 | B | comentario `# solo-metal:` al final de la línea | openings solo en walls metálicos; existing_walls no llevan openings |
| etapas.py:394 | A | walls + existing_walls inline (id único en las dos listas) | id repetido entre fragmentos: un existing_wall repetido duplicaría su board |
| etapas.py:429 | A | el conteo del print usa walls + existing_walls | mensaje de conteo de muros unidos (en CR decía 0 walls) |
| checklist_revision.py:125 | C | comentario `# campo:` al final de la línea | conteo 'walls' del renglón |
| handoff.py:392 | C | comentario `# campo:` al final de la línea | lista / conteo 'walls' del resultado del handoff |
| handoff.py:693 | C | comentario `# campo:` al final de la línea | lista / conteo 'walls' del resultado del handoff |
| chequeos_v76.py:61 | B | comentario `# solo-metal:` al final de la línea | R76 del cálculo de walls metálicos (lo llama canon.py); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| chequeos_v76.py:113 | B | comentario `# solo-metal:` al final de la línea | R76 del cálculo de walls metálicos (lo llama canon.py); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| chequeos_v76.py:138 | B | comentario `# solo-metal:` al final de la línea | R76 del cálculo de walls metálicos (lo llama canon.py); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| chequeos_v76.py:186 | B | comentario `# solo-metal:` al final de la línea | R76 del cálculo de walls metálicos (lo llama canon.py); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| chequeos_v76.py:233 | B | comentario `# solo-metal:` al final de la línea | R76 del cálculo de walls metálicos (lo llama canon.py); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| chequeos_v76.py:277 | B | comentario `# solo-metal:` al final de la línea | R76 del cálculo de walls metálicos (lo llama canon.py); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| chequeos_v76.py:297 | B | comentario `# solo-metal:` al final de la línea | R76 del cálculo de walls metálicos (lo llama canon.py); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| chequeos_v76.py:323 | B | comentario `# solo-metal:` al final de la línea | R76 del cálculo de walls metálicos (lo llama canon.py); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| cruzar_diagonal.py:116 | B | comentario `# solo-metal:` al final de la línea | wall con band ori D: solo walls metálicos tienen band |
| comparar.py:115 | B | comentario `# solo-metal:` al final de la línea | tag_ids de walls; los de existing_walls los cruza comparar_extra.por_tag (cierra la alerta) |
| comparar.py:139 | A | walls + existing_walls inline; además tag = w.tag or w.type (los existing_walls guardan el type en 'type') | disposición de un ambiguo citado en tag_ids de un existing_wall (CR) también cuenta |
| comparar.py:178 | A | walls + existing_walls inline | page 0-based: los existing_walls también tienen sheet / page |
| comparar.py:262 | C | comentario `# campo:` al final de la línea | walls del resultado de cobertura |
| chequeos_v75.py:65 | B | comentario `# solo-metal:` al final de la línea | R75 del cálculo de walls metálicos (lo llama canon.py); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| chequeos_v75.py:79 | B | comentario `# solo-metal:` al final de la línea | R75 del cálculo de walls metálicos (lo llama canon.py); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| chequeos_v75.py:104 | B | comentario `# solo-metal:` al final de la línea | R75 del cálculo de walls metálicos (lo llama canon.py); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| chequeos_v71.py:68 | B | comentario `# solo-metal:` al final de la línea | R71 del cálculo de walls metálicos (lo llama canon.py); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| chequeos_v71.py:87 | B | comentario `# solo-metal:` al final de la línea | R71 del cálculo de walls metálicos (lo llama canon.py); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| chequeos_v71.py:174 | B | comentario `# solo-metal:` al final de la línea | R71 del cálculo de walls metálicos (lo llama canon.py); existing_walls (board-only) los procesa aparte canon._existing_walls (R80w.39) |
| evidencia.py:156 | B | comentario `# solo-metal:` al final de la línea | evidencia por band de walls metálicos; existing_walls tienen path, no band |
| evidencia.py:196 | B | comentario `# solo-metal:` al final de la línea | evidencia por band de walls metálicos; existing_walls tienen path, no band |
| evidencia.py:214 | B | comentario `# solo-metal:` al final de la línea | evidencia por band de walls metálicos; existing_walls tienen path, no band |
| evidencia.py:230 | B | comentario `# solo-metal:` al final de la línea | evidencia por band de walls metálicos; existing_walls tienen path, no band |
| validar_canon.py:19 | B | comentario `# solo-metal:` al final de la línea | band.sheet: solo walls metálicos tienen band |
| reconcile.py:90 | B | comentario `# solo-metal:` al final de la línea | reconciliación A/B por geometría / openings / faces de walls metálicos |
| reconcile.py:91 | B | comentario `# solo-metal:` al final de la línea | reconciliación A/B por geometría / openings / faces de walls metálicos |
| reconcile.py:134 | B | comentario `# solo-metal:` al final de la línea | reconciliación A/B por geometría / openings / faces de walls metálicos |
| reconcile.py:138 | B | comentario `# solo-metal:` al final de la línea | reconciliación A/B por geometría / openings / faces de walls metálicos |
| reconcile.py:139 | B | comentario `# solo-metal:` al final de la línea | reconciliación A/B por geometría / openings / faces de walls metálicos |
| reconcile.py:162 | B | comentario `# solo-metal:` al final de la línea | reconciliación A/B por geometría / openings / faces de walls metálicos |
| reconcile.py:252 | B | comentario `# solo-metal:` en línea propia arriba (la línea sigue con `\`) | reconciliación A/B por geometría / openings / faces de walls metálicos |
| reconcile.py:253 | C | comentario `# campo:` al final de la línea | items_upsert['walls'] de la decisión |
| reconcile.py:254 | B | comentario `# solo-metal:` al final de la línea | reconciliación A/B por geometría / openings / faces de walls metálicos |
| reconcile.py:258 | C | comentario `# nodo:` al final de la línea | walls del ítem que cuelga |
| reconcile.py:265 | C | comentario `# campo:` al final de la línea | items_patch['walls'] de la decisión |
| reconcile.py:301 | B | comentario `# solo-metal:` en línea propia arriba (la línea sigue con `\`) | reconciliación A/B por geometría / openings / faces de walls metálicos |
| reconcile.py:313 | B | comentario `# solo-metal:` al final de la línea | reconciliación A/B por geometría / openings / faces de walls metálicos |
| reconcile.py:325 | B | comentario `# solo-metal:` al final de la línea | reconciliación A/B por geometría / openings / faces de walls metálicos |
| trim.py:28 | C | comentario `# nodo:` al final de la línea | walls del nodo free |
| trim.py:33 | B | comentario `# solo-metal:` al final de la línea | trim derivado (partial / column_wrap) de walls metálicos: cantidad, existing_walls no llevan ese trim |
| trim.py:50 | B | comentario `# solo-metal:` al final de la línea | trim derivado (partial / column_wrap) de walls metálicos: cantidad, existing_walls no llevan ese trim |
| run_takeoff.py:61 | B | comentario `# solo-metal:` al final de la línea | atributos A/B emparejados por reconcile.emparejar (geometría de walls metálicos) |
| run_takeoff.py:63 | B | comentario `# solo-metal:` al final de la línea | atributos A/B emparejados por reconcile.emparejar (geometría de walls metálicos) |
| run_takeoff.py:341 | C | comentario `# campo:` al final de la línea | lista walls de alturas_placeholder de completitud |
| run_takeoff.py:359 | C | comentario `# campo:` al final de la línea | conteo 'walls' de completitud.revisar (ya une existing_walls) |
| run_takeoff.py:405 | C | comentario `# campo:` al final de la línea | conteo 'walls' de completitud.revisar (ya une existing_walls) |
| run_takeoff.py:407 | C | comentario `# campo:` al final de la línea | conteo 'walls' de completitud.revisar (ya une existing_walls) |
| run_takeoff.py:444 | B | comentario `# solo-metal:` al final de la línea | band.sheet: solo walls metálicos tienen band |
| overlay.py:59 | B | comentario `# solo-metal:` al final de la línea | overlay sobre faces por cara (lista de dicts) de walls metálicos; existing_walls tienen faces = número |
| overlay.py:130 | B | comentario `# solo-metal:` al final de la línea | overlay sobre faces por cara (lista de dicts) de walls metálicos; existing_walls tienen faces = número |
| overlay.py:131 | C | comentario `# campo:` al final de la línea | walls del overlay |

## Validación

1. `CE.lecturas_solo_walls(tools/*.py + runner/*.py sin test_)` -> `[]`.
2. Banco v137 vs v136 (canon.py, familias_out.json): bn, vs, chuze, oreilly, cfa, hf, xf, cr: 116 familias, **0 distintas** cada uno.
3. `ast.parse` OK en los 33 archivos editados; test_op_punto_final.py OK (usa chequeos_v73.r73_8). r73_8 con walls + existing_walls en CR y CFA: 0 fallas nuevas.
4. __pycache__ borrados en /tmp/v137.

Nota: la lista dice 179 líneas (wc -l da 178 porque la última no termina en salto de línea).
