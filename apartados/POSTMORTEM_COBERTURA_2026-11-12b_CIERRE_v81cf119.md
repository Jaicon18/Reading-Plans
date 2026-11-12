# POSTMORTEM DE COBERTURA — CR City Hotel rev20a (cierre 12-nov-2026, U-185)

Revisor independiente (no hizo el trabajo de CR). Leído el código del skill vigente **v81cf118**
(`take-off-metal-frame-drywall_v81cf118_U191-excluded-cero_2026-11-12.zip`: tools/compuerta_entrega.py, chequeos_biblioteca.py,
comparar_alturas.py, plantilla_excel.py, subir_entrega.py, tests) + `.claude/skills/jc-hunter-ordenes/verificar_version.py`
+ `cache_proyectos/herramientas/barrido_drive.py`. Evidencia del proyecto: `cache_proyectos/cr_city_hotel_castle_rock/`
(ENTREGA_OK_rev20a.json, TIEMPOS.md, compuerta_corridas_rev20.jsonl, canon/takeoff_canon.json, RESUMEN_rev20.md).
Suite corrida en limpio: `correr_suite.py --solo test_compuerta_entrega.py test_chequeos_biblioteca.py` = 2/2 OK.

Alcance: todo lo creado / cambiado el 12-nov que no cubre `POSTMORTEM_COBERTURA_2026-11-12.md` (que llegaba hasta U-185 / BE-CR34 /
BE-AUD04): U-185..U-192, BE-CR35..BE-CR43 (+ BE-CR36b), BE-AUD05..09, BE-COORD02, BE-PM01..03. En la sección 2, los BE-XF / BE-GK
del 12-nov que tocaron la corrida de CR.

## Resumen

- **Tabla principal (27 renglones): 20 OK · 6 WEAK · 0 MISSING · 1 conducta**
- **Tabla secundaria (19 renglones, XF / GK del 12-nov): 7 OK · 1 WEAK · 0 MISSING · 11 conducta**
- **Causas de horas perdidas (sección 3): 12 causas · 9 con candado · 3 NO GUARD**

WEAK: U-185, U-189, U-190, BE-CR39, BE-CR40, BE-CR42 (+ BE-GK47 en la secundaria). NO GUARD: versión nueva no probada contra
los proyectos abiertos antes de publicarla; versión cambiada a mitad de la compuerta final; alarma de presupuesto en vivo.

## 1. Tabla error / regla → chequeo → test → estado

| id | error / regla | chequeo | test | estado |
|---|---|---|---|---|
| U-185 | post-mortem de cobertura al cerrar cada proyecto | verificar_version.revisar_postmortem | test_verificar_version 'postmortem_u185' | OK — cerrado en v81cf119: verificar_version.revisar_postmortem (cierre = última subida, hora completa; solo el post-mortem más nuevo) + test postmortem_u185 |
| U-186 | lo que ya no se ocupa en Drive = 'BORRAR (NO USAR) - …' | subir_entrega.nombre_borrar / borrar_fallas (llamado por herramientas/barrido_drive.py borrar) | test_compuerta_entrega::test_u186_borrar | OK |
| U-187 | ningún texto que generamos se encima | CE_TEXTOS_LEGIBLES (textos_legibles_fallas, hueco_etiqueta, comparar_alturas.seccion_sin_encimar / textos_encimados) | test_u187_textos_legibles (repite la sección de CR con 20+ alturas pegadas) | OK |
| U-188 | contestar solo lo que se pregunta, corto | — | — | conducta: forma de contestarle al usuario en el chat, no hay archivo que un programa pueda leer |
| U-189 | cielos apilados + detalle cara por cara + 'terminado' con COBERTURA | CB_RCP_APILADOS (rcp_apilados), CB_DETALLE_CARAS (detalle_caras), CE_PROTOCOLO_3H cobertura_fallas / cobertura_esperada | CASOS rcp_apilados / detalle_caras + test_u189_cobertura_y_gating | OK — cerrado en v81cf119: rcp_apilados (dobles de DOBLE_CIELO, pila desde DOBLE_CIELO), detalle_caras ref exacta, cobertura_esperada con burbujas de letra + test_v119_postmortem_12b |
| U-190 | ⭐ REGLA DE ORO #3 doble cielo | CE_DOBLE_CIELO (doble_cielo_fallas, niveles_membrana, cuartos_rcp) | test_u190_doble_cielo (CR L4 401 sin RS-1) | OK — cerrado en v81cf119: refs_doble_fallas en CE_DOBLE_CIELO (renglón inventado / borrado / repetido / cantidad 0) + test_v119_postmortem_12b y test_u190_doble_cielo |
| U-191 | lo que el plano cita por referencia se abre y se cita con ítem | CB_U_191_REF (u_191_ref + falta_cita_u191, también filas del Material Summary) | CASOS u_191_ref + test_v109_u191 (RFI-14 RC 16 in 'per assembly' sin Item = FAIL) | OK |
| U-192 | tasas de la Proposal decididas por el usuario | CE_PROPOSAL / revisar_proposal / u192_fallas | test_chequeos_biblioteca::test_u192_tasas_decididas (corre a nivel de módulo) | OK |
| BE-CR35 | SOF / BW con Depth 'not blind' | comparar_alturas.cobertura_ab + depth_ids_vista, CE_ALTURAS_EXTREMO | test_be_cr35_not_blind | OK |
| BE-CR36 | FreeText de markups encimados / recortados | markups_bluebeam.celda_legible, markups_rcp.aplicar, CE_TEXTOS_LEGIBLES | test_be_cr36_textos_markups | OK |
| BE-CR36b | celda_legible recortaba el type | markups_bluebeam.celda_legible (sin recorte, hasta 3.5 pt) | test_be_cr36_textos_markups | OK |
| BE-CR37 | ancho desarrollado mezclando lados (7/A7.23) | comparar_alturas.lados_fallas en CE_ALTURAS_EXTREMO | test_be_cr37_un_lado (en CR rev20a: 24 anchos con side / faces) | OK |
| BE-CR38 | renglones partidos borrados al reemplazar un bloque | comparar_alturas.cobertura_ab | test_be_cr38_renglones_partidos | OK |
| BE-CR39 | rev19 'terminado' sin GYP-1 de corredores, 2 caras de banda y caja en plenum | CB_RCP_APILADOS + CB_DETALLE_CARAS | CASOS rcp_apilados / detalle_caras (corredor 916 sintético) | OK — cerrado en v81cf119: igual que U-189 (rcp_apilados evalúa la pila FS / RS + GYP desde DOBLE_CIELO) + test_v119_postmortem_12b |
| BE-CR40 | faltante declarado por búsqueda de texto en el JSON | chequeos_biblioteca.faltante_por_tag | test_u190b_framing_y_be_cr40 | OK — cerrado en v81cf119: CB_FALTANTES_AUDITORIA llama faltante_por_tag sobre cada hallazgo 'falta' de la auditoría + CLI chequeos_biblioteca.py faltante + CASOS faltantes_auditoria |
| BE-CR41 | RC 'spacing per assembly' sin abrir UL L546 | CB_U_191_REF | test_v109_u191 | OK |
| BE-CR42 | conflicto plano vs plano sin 'delta' (CB_U_082 roja en corrida #2) | plantilla_excel.conflictos_sin_delta (al armar) + conflict_note + CB_U_082 | test_chequeos_biblioteca::test_be_cr42_conflicto_con_delta_y_gk47 | OK — cerrado en v81cf119: test_be_cr42_conflicto_con_delta_y_gk47() se llama a nivel de módulo + verificar_version.tests_sin_llamar (BE-PM07) |
| BE-CR43 | armado borraba compuerta_corridas.jsonl / gate.txt | compuerta_entrega.armar_carpeta / guardar_registro / restaurar_registro, protocolo_3h_fallas + causas_sin_registro | test_v111_registro_y_tope | OK |
| BE-AUD05 | 'L546' sin 'Item N' pasaba U-191 | falta_cita_u191 (RX_UL_SUELTO), u_191_ref sobre el Material Summary, trazabilidad._listings | test_v116_listing | OK |
| BE-AUD06 | CB_RCP_APILADOS pasaba con 0 cuartos | rcp_apilados (tags o DOBLE_CIELO con filas y 0 evaluados = FAIL) + filas_doble_cielo | test_v117_ceilings_misc | OK (su caso — 0 cuartos — queda cubierto; el caso '7 evaluados vs 54 dobles' es el WEAK de U-189) |
| BE-AUD07 | CE_RCP_COMPLETO 'N/A sin cielos' con SOF en el Excel | ce_rcp_completo + cielos_en_excel + contar_contornos_rcp | test_v114_auditoria_u138 | OK |
| BE-AUD08 | RESUMEN con cifra de RC distinta del Material Summary | CE_RESUMEN_EXCEL (resumen_excel_fallas) | test_v114_auditoria_u138 (tabla RESUMEN_rev9 sintética, mismo caso) | OK (compara tablas con columna Material; las cifras en prosa / columna Delta no se comparan) |
| BE-AUD09 | ENTREGA_OK con otra versión que la compuerta | _skill_version + version_fallas + CE_VERSION_ENTREGA + rev_vigente | test_v114_auditoria_u138 (incluye la historia de TIEMPOS de CR rev20a) | OK |
| BE-COORD02 | 74 textos encimados en SECTION de ALTURAS_REVISADAS | CE_TEXTOS_LEGIBLES + seccion_sin_encimar | test_u187_textos_legibles | OK |
| BE-PM01 | corridas de compuerta sin registro / watchdog | registro_corridas + correr_con_tope | test_p3_registro_corridas | OK |
| BE-PM02 | chequeos v96 en N/A sin campos del canon | CE_CAMPOS_CANON (campos_canon_fallas, entrega_nueva) | test_v97_campos_canon | OK |
| BE-PM03 | CB_RCP_TAGS contaba solo GYP-n | rcp_tags + tags_cielo | test_v104_rcp_todos_los_tags | OK |

## 2. Otros BE del 12-nov que tocaron la corrida de CR (XF / GK)

| id | error / regla | chequeo | test | estado |
|---|---|---|---|---|
| BE-XF11 | hash de commit tipeado en un reporte | — | — | conducta: el reporte al usuario lo escribe el agente copiando git log |
| BE-XF12 | v105 tumbó CE_ALTURAS_EXTREMO / CHECKLIST / 3LADOS en CR (página double_ceiling) | comparar_alturas.paginas_de_alturas + tope_chequeo + contar_markups | test_v106_paginas_y_watchdog | OK |
| BE-XF12b | versión publicada con verificar_version en rojo (pipe con tail) | — | — | conducta: publicar el zip es un paso manual de COORDINACIÓN fuera de la cadena |
| BE-XF13 | F2 marcaba la membrana rated superior de un baño con doble cielo | coherencia_r11 / ce_coherencia_r11 | test_v108_f2_membrana_superior | OK |
| BE-XF14 | timeout de CE_MARKUP_EN_WALL (corrida #3 de CR) | contar_markups + tope_chequeo + markups_fuera_de_wall (rejilla) | test_v111_registro_y_tope | OK |
| BE-GK39 | etiquetas sobre otras dentro de un Square | hueco_etiqueta + markups_rcp.aplicar | test_be_gk39_hueco_dentro_de_square | OK |
| BE-GK40 | pregunta ciega con otra magnitud que el Depth | comparar_alturas.pregunta_fallas | test_be_gk40_pregunta_misma_magnitud | OK |
| BE-GK41 | celdas de DOUBLE CEILING encimadas | _envolver_celda + paginas_doble_cielo + CE_TEXTOS_LEGIBLES | test_be_gk41_celdas_doble_cielo | OK |
| BE-GK42 | versión nueva a mitad de rev: correr --solo los chequeos nuevos | — | — | conducta: elegir qué chequeos correr con --solo lo decide la sesión (ver NO GUARD 3.2) |
| BE-GK43 | lectura ciega agregada sin su resolución A/B | — | — | conducta: escribir la resolución en el mismo script es disciplina del agente; CE_ALTURAS_EXTREMO ya exige toda diferencia A≠B resuelta |
| BE-GK44 | Review Item 'not printed' resuelto antes con el plano | — | — | conducta: la lectura del plano la hace el lector; CE_RFI_BARRIDO_IMPRESO cubre el texto impreso |
| BE-GK45 | citas reescritas sin forma de burbuja | — | — | conducta: redacción del renglón por el agente; CE_CALLOUTS ya exige la burbuja citada |
| BE-GK46 | armado borraba compuerta_corridas.jsonl | armar_carpeta / restaurar_registro (= BE-CR43) | test_v111_registro_y_tope | OK |
| BE-GK47 | '60.0 LF' leído como 'impreso en 0' por CB_BE_HF02 | CB_BE_HF02 (be_hf02) | dentro de test_be_cr42_conflicto_con_delta_y_gk47 | OK — cerrado en v81cf119: cubierto por la llamada del test de BE-CR42 + tests_sin_llamar |
| BE-GK48 | después de corregir textos correr --solo TODOS los chequeos | — | — | conducta: secuencia de corridas que decide la sesión antes de la final |
| BE-GK49 | entrega rev3 con la Proposal de rev2 | — | — | conducta: script del proyecto (armar_entrega.sh), fuera del skill |
| BE-GK50 | scripts del proyecto no aceptaban 'rev3a' | — | — | conducta: scripts del proyecto fuera del skill |
| BE-GK51 | 'loaded' del RFI sin actualizar al cerrarlo | — | — | conducta: redacción del RFI por el agente al cerrarlo |
| BE-GK52 | editar un .sh mientras corre | — | — | conducta: operación del agente sobre un proceso en curso |

## 3. Causas de horas perdidas en CR (11-12 nov) y su candado

Fuente: TIEMPOS.md (rev19 541 min, 9 corridas finales; rev20 838 min, 6 corridas; total del proyecto 3258 min = 452 % del
presupuesto de 720 min), compuerta_corridas_rev20.jsonl, git log 12-nov (22 versiones del skill: v97 → v118 entre 00:00 y 15:48 PT,
4 de ellas — v115, v116, v117, v118 — 'urgente CR / GK' para quitar falsos positivos o huecos de chequeos recién publicados).

| # | causa | candado | estado |
|---|---|---|---|
| 3.1 | Versiones nuevas del skill con falsos positivos / bugs sobre el proyecto abierto: v105 tumbó 3 chequeos (corrida #1 roja), v114 CE_VERSION_ENTREGA leía la historia de TIEMPOS (v115), U_191 marcaba tornillería EXCLUDED en 0 (v118), RCP_APILADOS sin ceilings_misc (v117) | ninguno de programa: verificar_version solo exige que INDICE diga "banco 0 distintas" (texto); no hay paso que corra la compuerta de la versión candidata sobre los canons / entregas de los proyectos ABIERTOS antes de marcarla vigente | candado OK: BE-PM04 (prueba_abiertos con todos los proyectos de PROYECTOS_ABIERTOS.json, verificar_version; tests prueba_abiertos_be_pm04 / test_v119_prueba_abiertos) |
| 3.2 | Versión cambiada a mitad de la compuerta final (corrida #5 cortada: v113 → v114) y re-corridas por cada versión | 'congelado' de versiones y BE-GK42 son conducta; nada impide publicar una versión mientras un proyecto tiene compuerta final en curso, ni fija la versión del proyecto hasta su entrega | candado OK: BE-PM05 (VERSION_PROYECTO.txt en CE_PROTOCOLO_3H; test_v119_postmortem_12b) |
| 3.3 | Presupuesto 452 %: rev20 sola 838 min sin alarma durante el trabajo | CE_TIEMPOS / presupuesto_fallas solo al correr la compuerta, y > 100 % pasa como AMBER con cualquier 'causa:' escrita; el reporte cada 30 min (U-180 (2)) es conducta | candado OK: BE-PM06 (alarma_fallas en CE_PROTOCOLO_3H: --paso por paso cerrado + alerta en el momento; test_v119_alarma_presupuesto) |
| 3.4 | Registro jsonl borrado por el re-armado (#1, #2 sin registro; #3 roja) | BE-CR43 restaurar_registro + causas_sin_registro | candado OK |
| 3.5 | Timeout de CE_MARKUP_EN_WALL (#3) | BE-XF14 tope por markups + rejilla | candado OK |
| 3.6 | Review Item D15 sin 'delta' (corrida #2 roja) | BE-CR42 conflictos_sin_delta al armar + CB_U_082 | candado OK en código; test sin cablear (WEAK, tabla 1) |
| 3.7 | RESUMEN / BITACORA con cifras de otra corrida (RC 20,054 vs 27,124.98) | BE-AUD08 CE_RESUMEN_EXCEL | candado OK (solo tablas con columna Material) |
| 3.8 | Versión declarada en los documentos ≠ versión de la compuerta | BE-AUD09 CE_VERSION_ENTREGA | candado OK |
| 3.9 | Hallazgos de fondo después de 'terminado' (rev19: GYP-1 de corredores, caras de banda 7/A7.23, RS-1 de L4) → rev20 completa | U-189 / U-190 (CB_RCP_APILADOS, CB_DETALLE_CARAS, CE_DOBLE_CIELO, cobertura U-181) | candado parcial (WEAK, tabla 1) |
| 3.10 | RFI-14 RC 'not printed' → +7,070 LF encontrados al final en UL L546 Item 6 | U-191 / BE-AUD05 CB_U_191_REF | candado OK |
| 3.11 | Faltante falso reportado por búsqueda de texto (COORDINACIÓN) | BE-CR40 faltante_por_tag | candado sin cablear (WEAK, tabla 1) |
| 3.12 | rev19: 9 corridas finales por hallazgos de la auditoría independiente después del armado y cambios de alcance F&B a mitad de trabajo | CE_PROTOCOLO_3H (auditoría fechada antes de la subida, corridas contadas, tope 4 / 2 rojas con causa) | candado OK (cuenta y exige causa; no impide) |

## 4. Observaciones del revisor (sin cambiar código)

- CR rev20a se cerró (CSV 1351/1351, SKILL FINAL v118) con ENTREGA_OK de **v81cf116**; v117 (ceilings_misc en RCP_APILADOS) y v118
  (U_191 salta EXCLUDED en 0) no se corrieron sobre esa entrega. Por el diseño de CE_ENTREGA_VIGENTE (U-177 (1)) la próxima corrida
  pediría re-correr; los dos cambios solo relajan / amplían chequeos que ya pasaban en CR, sin efecto en cantidades.
- Por el hueco de U-185 (c), `verificar_version.py` seguirá pasando aunque este archivo tenga WEAK abiertos, porque
  `POSTMORTEM_COBERTURA_2026-11-12.md` (limpio) también tiene fecha >= cierre. Los WEAK de aquí se cierran en la versión siguiente
  del skill antes del próximo proyecto (U-185), no por la compuerta.
- Todos los tests registrados para los renglones OK existen, se llaman en su archivo y pasan (`correr_suite` 2/2 OK sobre v81cf118).

## Cierre en v81cf119 (propuesto por Xfinity, a confirmar por COORDINACIÓN al publicar)

NO GUARD 3.1 -> BE-PM04 (prueba_abiertos + PRUEBA_ABIERTOS_vN.json exigido por verificar_version); 3.2 -> BE-PM05 (VERSION_PROYECTO.txt en CE_PROTOCOLO_3H); 3.3 -> BE-PM06 (ALERTA_PRESUPUESTO.json con --paso; > 100 % exige causa: + plan:).
