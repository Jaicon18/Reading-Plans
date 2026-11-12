# VERIFICACIÓN INDEPENDIENTE 4: candidato v81cf120 (commit fd2c981)

2026-11-12 13:40 PT. La hizo un revisor independiente que no escribió el código. Se leyó el código, se corrió y se probó con entradas adversariales nuevas para cada renglón. No se tocó ninguna tool.

## Qué se revisó

- **Base:** `skills_archivo/take-off-metal-frame-drywall_v81cf119_U193-cobertura_2026-11-12.zip`.
- **Parche:** `apartados/v81cf120_desde_v81cf119.patch`, aplicado con `patch -p1`. Toca 4 archivos: REGLAS_REGISTRO.json, SKILL.md, compuerta_entrega.py y test_compuerta_entrega.py. Resultado: 199 archivos y `VERSION: v81cf120`.
- **Órdenes:** `apartados/ordenes_v120/*.py`, copiadas sobre una copia de `.claude/`.
- **Adversariales nuevos:** `scratchpad/adv120v4/`, con adv4_pm.py, adv4_pm04.py, adv4_pm06.py, adv4_u193.py y adv4_gk54.py. Usan copias reducidas del cache: solo los POSTMORTEM_* y los SUBIDA_OK*.json.
- **Ojo:** `apartados/adversariales_v119/adv_pm_real.py` escribe y BORRA `POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION3.md` dentro del cache que recibe. Al correrlo sobre el cache real, el archivo quedó borrado del árbol de trabajo. Se restauró con `git checkout`. De aquí en adelante, ese script solo se corre sobre una copia.

## Corridas

**Pruebas del candidato**
- Suite `correr_suite.py` (con TAKEOFF_SKILL = candidato): **47/47 OK**.
- Selftest de verificar_version v120: OK (incluye postmortem_u185, prueba_abiertos_be_pm04 y tests_llamados).

**verificar_version sobre el candidato, con skills_archivo y cache_proyectos reales** (antes de este archivo)
- Faltan 0 reglas.
- Tests sin llamar: 0.
- U-185: 7 renglones abiertos (U-185, causa 3.1, causa 3.3, NG-3.1 / BE-PM04, NG-3.3 / BE-PM06, U-193, BE-GK54).
- Falta `PRUEBA_ABIERTOS_v81cf120.json`.

**adversariales_v119 re-corridos contra v120**
- adv_pm: A1, A2, A3a, A3b, A4, A5 y B1 dan falla. A2 ya no pasa.
- adv_pm_real: C1 a C4 dejan los renglones abiertos.
- adv_pm04:
  - P4a, P4b, P4c y P4d quedan ABIERTOS.
  - P8 se resolvió por otro camino: `proyectos_abiertos_cache(None)` sigue dando [], pero `revisar_prueba_abiertos` ahora usa el cache de al lado, y sin él da falla.
- adv_pm06 C: alerta.
- adv_gk54: G1, G2, G3, G4 y G6 dan True. G5 sigue en False y queda documentado como límite en la GUÍA.
- adv_cr40: FAIL en los 4 casos.
- adv_u193 (viejo) ya no corre porque `subagentes_bitacora` devuelve 4 valores. Se reescribió como adv4_u193: U6 y U7 dan falla.

## Tabla

| id | error / regla | chequeo | test | estado |
|---|---|---|---|---|
| U-185 | Post-mortem de cobertura al cerrar cada proyecto | `verificar_version.revisar_postmortem` (RX_PM_CERRADO, arrastre desde el 12b) | `postmortem_u185` | WEAK — STILL-WEAK. Cerrado y reproducido: C4 'NOT CONFIRMED…' ya no cierra; C1 / A2, un principal 12c no borra los abiertos; los ids renombrados en un 12c ('U185', 'BE‑GK54' con guion duro) no cierran nada; los guiones raros U+2012, U+2015, U+2212 y U+2E3A no cierran. Huecos reproducidos con adv4_pm.py: (D2) el regex está anclado al inicio pero no al final, así que un estado 'OK — CONFIRMED-CLOSED-NOT, WEAK — STILL-WEAK' CIERRA los 14 renglones; (D4) una verificación SIN hora en sus primeras 12 líneas toma el fin del día (23:59 PT) y le gana a una verificación posterior con hora (22:00 PT) que dice STILL-WEAK: todo queda cerrado; (D5) una verificación con fecha futura ('2099-01-01 00:00 PT') queda para siempre como la última palabra; (D6) un renglón basura 'junk NG-3.1 NG-3.3' en estado OK cierra 'causa 3.1' y 'causa 3.3' aunque su id no sea el de ese renglón. Arreglo propuesto: estado exacto anclado al final; verificación sin hora o con hora futura = falla; las causas se cierran solo con el id exacto. |
| U-189 | Cielos apilados, detalle cara por cara y COBERTURA | `CB_RCP_APILADOS`, `CB_DETALLE_CARAS`, `cobertura_esperada` | CASOS + `test_v119_postmortem_12b` | OK — CONFIRMED-CLOSED |
| U-190 | REGLA DE ORO #3 doble cielo | `CE_DOBLE_CIELO` + `refs_doble_fallas` | `test_v119_postmortem_12b` + `test_u190_doble_cielo` | OK — CONFIRMED-CLOSED |
| BE-CR39 | rev19 terminado sin el GYP-1 de los corredores | Igual que U-189 / U-190 | `test_v119_postmortem_12b` | OK — CONFIRMED-CLOSED |
| BE-CR40 | Cielo declarado faltante buscando texto | `CB_FALTANTES_AUDITORIA` | `test_v119_be_cr40_verificacion` | OK — CONFIRMED-CLOSED |
| BE-CR42 | Conflicto plano vs plano sin delta | `conflictos_sin_delta` + `tests_sin_llamar` | `test_be_cr42_…` | OK — CONFIRMED-CLOSED |
| BE-GK47 | '60.0 LF' leído como 'impreso en 0' | CB_BE_HF02 | El mismo test de BE-CR42 | OK — CONFIRMED-CLOSED |
| NG-3.1 / BE-PM04 | Versión nueva no probada sobre los proyectos abiertos | `revisar_prueba_abiertos` + `proyectos_abiertos_cache` + `sha_tools` | `prueba_abiertos_be_pm04` + `test_v119_prueba_abiertos` | WEAK — STILL-WEAK. Cerrado y reproducido: P4b (SUBIDA_OK.json sin rev más nuevo), P4c (VERSION_PROYECTO más nuevo), RESULTADO sin fecha y '0 + 3 faltantes' = ABIERTO; P3 (regresiones 5, sin explicar 5) = falla; un nombre fantasma de la lista = falla; omitir un proyecto abierto real = falla aunque se liste un directorio existente que no es proyecto. Huecos reproducidos con adv4_pm04.py: (Q2) un RESULTADO.md vacío, '0 CSV / 0 PDF / 0 emparejados; 0 faltantes' con fecha, CIERRA el proyecto (pasa en vacío, U-137); (Q3) `_fecha_resultado` toma la PRIMERA fecha del texto: un RESULTADO comparado a las 09:00 PT, ANTES de la subida de las 20:00Z, que menciona arriba 'Bid due 2026-11-20 14:00' se da por CERRADO; (Q5 / Q5b) un PRUEBA_ABIERTOS escrito a mano con solo `sha_tools` (que cualquiera calcula), o con vigente / candidata en 0 PASS / 0 FAIL, pasa sin faltas: nada exige que la corrida haya ocurrido (conteos > 0, sello o hash del JSON de la compuerta); (Q1) un SUBIDA_OK_rev2.json con la clave 'fecha' en vez de 'fecha_iso' se ignora en silencio. Menor: Q4, un fecha_iso sin zona revienta con TypeError (falla ruidosa). |
| NG-3.2 / BE-PM05 | Versión cambiada a mitad de la compuerta final | `version_proyecto_fallas` | `test_v119_postmortem_12b` | OK — CONFIRMED-CLOSED |
| NG-3.3 / BE-PM06 | Sin alarma de presupuesto mientras se trabaja | `alarma_fallas` + `pasos_cerrados_tiempos` + `tiempos_cuadran_fallas` + `sellos_fallas` | `test_v119_alarma_verificacion2` | WEAK — STILL-WEAK. Cerrado y reproducido: E3 (log sin 'N fin') ahora exige --paso por cada paso de TIEMPOS.md; un '--paso 9' para todo o un '1-9' no cubre los pasos 1 / 2-3 / 4; las corridas correctas limpian. Hueco reproducido con adv4_pm06.py: `pasos_cerrados_tiempos` y `tiempos_cuadran_fallas` usan RX_TIEMPOS_FILA (solo 'N' o 'N-N' con guion ASCII, Fin en la 4.ª columna), pero CE_TIEMPOS (`_pasos_tiempos`) acepta más formatos. TIEMPOS.md que CE_TIEMPOS da por buenos (tiempos_fallas = [], pasos 1-4 con hora) dejan pasos sin exigir: (F1) '2–3' con raya U+2013 omite el paso 2-3; (F2) '**1**' / '**4**' en negrita los omite; (F3) '4a' omite el 4; (F4) una tabla de 3 columnas 'Paso, Inicio, Fin' omite TODOS (0 exigencias --paso y tiempos_cuadran = []); (F5) las columnas en otro orden ('#, Inicio, Fin, Duración, Paso') omiten todos. Arreglo propuesto: usar `_pasos_tiempos` (el mismo parser de CE_TIEMPOS) y ubicar la columna Fin por su encabezado. |
| U-193 | MAPA DE COBERTURA: revisor registrado, distinto del autor, rol exacto | `subagentes_bitacora` + `ce_cobertura` | `test_v119_cobertura` + `test_v119_mutacion_cobertura` | WEAK — STILL-WEAK. Cerrado y reproducido: U6, canon.py sin agente más un 'subagente canon FAKE' = corrida sin agente y sin autores del canon = falla; U7, mayúsculas 'author-1' contra 'AUTHOR-1' = rechazado; un NBSP solo al final se quita con strip. Hueco reproducido con adv4_u193.py: los ids se comparan con `.strip().lower()` y nada más, así que un revisor que difiere SOLO por espacios internos o invisibles se acepta como distinto del autor del canon 'subagente A1': (U8) 'subagente  A1' con doble espacio, (U9) 'subagente A1' con NBSP, (U10) 'subagente A1​' con espacio de ancho cero y (U11) 'subagente\tA1' con tabulador dan rev ⊄ autores, y el reviewer PASA. Arreglo propuesto: normalizar los ids (NFKC, quitar los caracteres de formato Cf y colapsar todo espacio Unicode) en los dos lados y en `bitacora.subagente` / SUBAGENTE_ID. |
| BE-PM08 | `COBERTURA - IMAGE ONLY.pdf` tomado por PDF de markups | `nombres_planos` | `test_v119_gk_nombres_y_bitacora` | OK — CONFIRMED-CLOSED |
| BE-PM09 | Bitácora de GK en `takeoff_work/` no se leía | `_bitacoras` | `test_v119_gk_nombres_y_bitacora` | OK — CONFIRMED-CLOSED |
| BE-GK54 | Dos leaves con gap = dos walls ('same wall as X' esconde una leaf) | `be_gk54_fallas` (RX_GK54_SAME, RX_GK54_DISP_MISMO, RX_NH_TRAZA) dentro de CE_COBERTURA | `test_be_gk54` | WEAK — STILL-WEAK. Cerrado y reproducido: G1, G1b, G2, G2b, G2c, G3, G4 y G6 = FAIL; el wall inexistente da falla; la entrada pedida 'same wall gap n/a A111' (DISPUESTO) da FAIL porque 'A111' no es N/HOJA; 'EXISTING CONSTRUCTION TO REMAIN (2/X9.11)' no se toma por GK54; G5 (leaves fusionadas) queda documentado en la GUÍA y CE_COBERTURA lo exige desde FECHA_V120. Huecos reproducidos con adv4_gk54.py, todos sin gap_proof y con la leaf roja paralela a 4 in: (H1b) un DISPUESTO 'same wall, gap n/a (1/A111)' pasa porque basta la palabra 'gap' más cualquier N/HOJA, aunque diga n/a; (H2) un gap_proof 'n/a (1/A111)' y (H2b) uno 'there IS a 6in gap 3/A111', que prueba lo contrario, pasan; (H3) las razones 'same wall as: X9-Z9-08', "same wall as 'X9-Z9-08'", 'same wall (X9-Z9-08)', 'already counted in …', 'included in …', 'identical to …', 'counted with …', 'dup of …', 'same‑wall as …' (guion U+2011), 'mismo muro que …' y 'see …' no se reconocen y la exclusión pasa en silencio; (H4) un DISPUESTO 'NO ES NUESTRO: part of X9-Z9-08 (1/X9.11)' pasa. Esto es incoherente: RX_GK54_SAME sí acepta 'part of' sin 'wall' y la disposición no. Lo mismo pasa con 'already counted in …', 'same leaf as …', 'same‑wall …' y 'dup of …'. Arreglo propuesto: normalizar guiones y espacios, aceptar puntuación entre 'as' y el id, usar la misma lista de sinónimos en los dos regex (o exigir gap_proof en TODA exclusión cuyo motivo cite un id de wall del canon) y rechazar gap_proof y disposición con 'n/a', 'none' o 'there is a gap'. |

## Resumen

**CONFIRMED-CLOSED (9):** U-189, U-190, BE-CR39, BE-CR40, BE-CR42, BE-GK47, NG-3.2 / BE-PM05, BE-PM08 y BE-PM09.
- No hay regresión: la suite da 47/47, adv_cr40 sigue en FAIL en los 4 casos, hay 0 tests sin llamar y el parche no toca esas funciones.

**STILL-WEAK (5):** U-185, NG-3.1 / BE-PM04, NG-3.3 / BE-PM06, U-193 y BE-GK54.
- Cada uno cerró los huecos de la verificación 3 y tiene huecos nuevos reproducidos (ver la tabla).

**Bloqueos de publicación aparte:**
- Falta `skills_archivo/PRUEBA_ABIERTOS_v81cf120.json`.
- GK y CR todavía no corren con el sha de v120.

**Recomendación:** no publicar v81cf120 como "0 WEAK".
