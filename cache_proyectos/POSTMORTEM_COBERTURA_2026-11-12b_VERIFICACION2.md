# VERIFICACIÓN INDEPENDIENTE 2 del candidato v81cf119 (commit 567fe1c, "Ampliación 4")

2026-11-12 12:52 PT. Revisor independiente que no escribió el código. Se verificó leyendo el código, corriéndolo y probando una entrada adversarial por renglón. No se tocó ninguna tool.

## Qué se revisó

- Base: `skills_archivo/take-off-metal-frame-drywall_v81cf118_U191-excluded-cero_2026-11-12.zip`.
- Encima: `apartados/v81cf119_desde_v81cf118.patch` (commit 567fe1c). Se aplica con `-p1` desde la carpeta que contiene `take-off-metal-frame-drywall/` (con `-p2` no aplica: las rutas empiezan con `v118/`). Resultado: 199 archivos, `VERSION: v81cf119`.
- `apartados/ordenes_v119/verificar_version.py` y `test_verificar_version.py` se copiaron a una copia de `.claude/skills/jc-hunter-ordenes/` (el selftest necesita `hooks/registrar_orden.py` a su lado).
- Las pruebas adversariales están en `scratchpad/adv119/` (adv_pm.py, adv_cr40.py, adv_pm06.py, adv_u193.py).

## Resultados de las corridas

- **Suite completa** `correr_suite.py --skill <v119>`: **47/47 OK**.
- **Selftest de verificar_version v119**: **13/13 OK** (incluye `postmortem_u185`, `tests_llamados`, `prueba_abiertos_be_pm04`).
- `tests_sin_llamar` sobre el candidato: 0. Todos los `test_v119_*` se llaman a nivel de módulo (`test_compuerta_entrega.py` 2586 / 2589 / 2641 / 2665 / 2694 / 2724; `test_chequeos_biblioteca.py` 837).
- **verificar_version v119 sobre el candidato con el cache real**: rc 1, con 3 faltas:
  1. **FALTAN: BE-GK54.** Está en `cache_proyectos/BIBLIOTECA_ERRORES.md` (commit 13a8779, GK rev3b), pero el candidato no lo trae (solo vive en `apartados/be_gk54/`). Hay que unirlo antes de publicar (U-078).
  2. POSTMORTEM U-185: 12b + 12b_VERIFICACION, con 10 WEAK y 3 NO GUARD. Es lo esperado. Este archivo pasa a ser la verificación más nueva (12:52 PT > 12:15 PT).
  3. PRUEBA ABIERTOS: falta `skills_archivo/PROYECTOS_ABIERTOS.json`. Además, `apartados/PRUEBA_ABIERTOS_v81cf119.json` solo trae `xfinity_interquest`: faltan GK y CR.

## Tabla

| id | error / regla | chequeo | test | estado |
|---|---|---|---|---|
| U-185 | Post-mortem de cobertura al cerrar cada proyecto | `verificar_version.revisar_postmortem` (RX_PM_PRINCIPAL, tabla obligatoria, acompañantes, `causas_no_guard`) | `test_verificar_version::postmortem_u185` (se llama en `correr()`; selftest OK) | WEAK — STILL-WEAK. Lo que ya está cerrado: (a) un principal sin tabla = FALLA (adversarial A1 reproducido); (b) solo cuentan los nombres `POSTMORTEM_COBERTURA_<fecha>[letra].md` como principal; (c) un `_CIERRE` o una copia no relajan nada; (d) un `NO GUARD` en la tabla de causas queda abierto. Hueco nuevo, reproducido (A3b): de las `_VERIFICACION*` solo se lee la MÁS NUEVA, y si esa no tiene tabla, los WEAK de la verificación anterior **desaparecen**. Ejemplo: principal limpio + `_VERIFICACION` con 2 WEAK da FALLA; al agregar `_VERIFICACION3.md` ("sin tabla, todo bien") da `[]`. Es una pasada en vacío. Lo mismo pasa con una verificación nueva que simplemente omite un renglón (A4: el Q9 omitido se da por cerrado). Notas: (i) un principal nuevo `12c` con un solo renglón OK reemplaza al 12b con 7 WEAK (A2); no se comprueba que la tabla liste los BE / U del proyecto; (ii) sin el 3er argumento (cache), `revisar_postmortem` devuelve `[]`. Arreglo propuesto: una `_VERIFICACION` sin tabla = falla, y un id abierto en una verificación anterior sigue abierto hasta que una más nueva lo marque OK de forma explícita. |
| U-189 | Cielos apilados, detalle cara por cara y COBERTURA | `CB_RCP_APILADOS`, `CB_DETALLE_CARAS`, `cobertura_esperada` | CASOS `rcp_apilados` / `detalle_caras` + `test_v119_postmortem_12b` (se llama, línea 2641) | OK — CONFIRMED-CLOSED. No hubo cambios de fondo desde la verificación anterior y la suite pasa. Siguen las notas de entonces: el borde en vacío cuando el canon no trae cielos ni misc lo para CE_DOBLE_CIELO. |
| U-190 | REGLA DE ORO #3 doble cielo | `CE_DOBLE_CIELO` + `refs_doble_fallas` | `test_v119_postmortem_12b` + `test_u190_doble_cielo` | OK — CONFIRMED-CLOSED. Igual que antes. |
| BE-CR39 | rev19 dado por terminado sin el GYP-1 de los corredores | Igual que U-189 / U-190 | `test_v119_postmortem_12b` (sintético) | OK — CONFIRMED-CLOSED en el código. Pendiente con datos reales: `CLG-L2-217F` / `CLG-L3-317F` de CR rev20a. |
| BE-CR40 | Cielo declarado faltante buscando texto en el JSON | `CB_FALTANTES_AUDITORIA` (`faltantes_auditoria` → `resolver_faltante` → `faltante_por_tag`; cierre por ref con `_ref_cargada`) | `test_v119_be_cr40_verificacion` (se llama, línea 837) + CASOS `faltantes_auditoria` | OK — CONFIRMED-CLOSED. El texto `faltante_por_tag:` ya no se usa como prueba: la compuerta llama a la función. Adversariales: "X9.01 GYP-9 8'-11\" missing … faltante_por_tag: CARGADO" con el cielo cargado = FAIL; "GYP-9 missing (faltante_por_tag: CARGADO)" = FAIL; "Room 901 soffit not loaded" (sin tag, por cuarto) = FAIL; cierre con una ref que no está en el canon = FAIL; sin tag ni cuarto = FAIL (no N/A). Se lee todo `**/Auditoria/**/*.md`. Nota menor: la ref de cierre tiene que existir en el canon, pero no se comprueba que sea del mismo cuarto o tag. |
| BE-CR42 | Conflicto plano vs plano sin delta | `plantilla_excel.conflictos_sin_delta` + CB_U_082 + `tests_sin_llamar` | `test_be_cr42_conflicto_con_delta_y_gk47()` (se llama, línea 1025) + `tests_llamados` | OK — CONFIRMED-CLOSED. Sigue la nota menor: `tests_sin_llamar` también cuenta como llamada un `test_x(` dentro de un comentario. |
| BE-GK47 | '60.0 LF' leído como 'impreso en 0' | CB_BE_HF02 | El mismo test de BE-CR42 | OK — CONFIRMED-CLOSED |
| NG-3.1 / BE-PM04 | Versión nueva no probada sobre los proyectos abiertos | `compuerta_entrega.prueba_abiertos` (une las corridas de cada sesión) + `verificar_version.revisar_prueba_abiertos` (versión del candidato tomada de su SKILL.md) | `prueba_abiertos_be_pm04` (selftest) + `test_v119_prueba_abiertos` (se llama, línea 2694) | WEAK — STILL-WEAK. Ya cerrado: (a) con 1 de 3 proyectos = FALLA; (b) se exige ANTES de publicar (VERSION del candidato, no el INDICE); (c) una regresión sin explicación = FALLA. Huecos reproducidos: (1) **pasa en vacío** cuando `PROYECTOS_ABIERTOS.json` trae `{"proyectos": []}` y el PRUEBA tiene `proyectos: {}` (B1 da `[]`); (2) el PRUEBA se ata solo a la etiqueta de versión: no guarda un hash de las tools candidatas, así que una corrida hecha con un build anterior del mismo `v81cf119` sigue valiendo. Esto pasa hoy: el XF se corrió a las 20:42 UTC y el candidato cambió después. Arreglo propuesto: lista vacía = falla (U-137), y el PRUEBA guarda el sha de `tools/` del candidato y verificar_version lo compara. |
| NG-3.2 / BE-PM05 | Versión cambiada a mitad de la compuerta final | `version_proyecto_fallas` en CE_PROTOCOLO_3H + `fijar_version_proyecto` | `test_v119_postmortem_12b` | OK — CONFIRMED-CLOSED. Sin cambios. |
| NG-3.3 / BE-PM06 | Sin alarma de presupuesto mientras se trabaja | `alarma_fallas` en CE_PROTOCOLO_3H (entregas nuevas) + `alerta_presupuesto` con historial | `test_v119_alarma_presupuesto` (se llama, línea 2724; 4 casos, uno con la alerta escrita tarde) | WEAK — STILL-WEAK. Ya cerrado: un paso cerrado en tiempos.log sin su corrida `--paso` = falla; el cruce del 50 % / 100 % sin alerta a tiempo = falla. Huecos reproducidos (adv_pm06): (1) **sin `tiempos.log` (o con menos de 2 marcas), `alarma_fallas` devuelve `[]`**. Ningún chequeo exige `tiempos.log` (CE_TIEMPOS solo pide TIEMPOS.md), así que si no se escribe el log, la alarma no corre. (2) Un log sin renglones "N fin" deja vacía la parte (1), la de las corridas `--paso`. (3) `ALERTA_PRESUPUESTO.json` y `compuerta_corridas.jsonl` se pueden escribir a mano: no están en la cadena de hashes. Arreglo propuesto: en una entrega nueva, sin `tiempos.log` o sin ningún `N fin` de los pasos 1-9 = FAIL. |
| U-193 | MAPA DE COBERTURA: FALTA no limpia, revisor registrado y distinto del canon, hoja_ciega verificable | `_cob_disp` (RX_COB_DECISION_OK), `ce_cobertura` (hoja_ok, `subagentes_bitacora`, B6, PDF / CSV, ciegas / ciegas_rcp) | `test_v119_cobertura` (se llama, línea 2589) + `test_v119_mutacion_cobertura` (se llama, línea 2586) | WEAK — STILL-WEAK (residual angosto). Cerrado y reproducido: decision FALTA / vacía no limpia un rojo; nhoja sin forma N/HOJA no limpia; un revisor no registrado = FAIL; el mismo id registrado como canon y como revisor = FAIL; hoja_ciega solo vale con CUBIERTO + motivo + N/HOJA + revisor registrado + imagen que exista; sin CHECKLIST / B6 / CSV / PDF = FAIL; detector ciego en planta y en RCP = FAIL; la mutación sintética (dos caras / dos cielos apilados) da ROJO dentro de la suite. Hueco reproducido (adv_u193): **"distinto de los autores del canon" pasa en vacío**. `canon_ids` solo trae los ids registrados con `bitacora.py subagente canon <id>`, y nada exige que los autores del canon / take-off se registren. Una bitácora con un solo renglón `revisor_cobertura "subagente TAKEOFF-AUTHOR"` (el propio autor) pasa. Además, cualquier rol que empiece con `revisor` cuenta, no solo `revisor_cobertura`. Arreglo propuesto: en entregas nuevas, 0 subagentes `canon` / `takeoff` registrados = FAIL, y el rol tiene que ser exactamente `revisor_cobertura`. |
| BE-PM08 | `COBERTURA - IMAGE ONLY.pdf` tomado por un PDF de markups mal nombrado | `nombres_planos`: excepción exacta `b != COB_PDF` | `test_v119_gk_nombres_y_bitacora` (se llama, línea 2665) | OK — CONFIRMED-CLOSED. La excepción es por nombre exacto: la copia "COBERTURA - IMAGE ONLY (1).pdf" sigue fallando, y el test lo prueba. |
| BE-PM09 | La bitácora de GK en `takeoff_work/` no se leía | `_bitacoras`: `$BITACORA`, `<w>/bitacora.jsonl` y `<w>/takeoff_work/bitacora.jsonl`, sin duplicados por realpath | `test_v119_gk_nombres_y_bitacora` | OK — CONFIRMED-CLOSED. Con una bitácora en otra ruta: para los hashes de la cadena el chequeo se vuelve más estricto, nunca más laxo. Para los revisores, ver U-193. |

## Resumen

- **CONFIRMED-CLOSED (9):** U-189, U-190, BE-CR39, BE-CR40, BE-CR42, BE-GK47, NG-3.2 / BE-PM05, BE-PM08, BE-PM09.
- **STILL-WEAK (4):**
  - U-185: una verificación más nueva sin tabla, o que omite un renglón, borra los WEAK de la anterior.
  - NG-3.1 / BE-PM04: una lista de abiertos vacía pasa; el PRUEBA no está atado al hash de las tools del candidato.
  - NG-3.3 / BE-PM06: sin `tiempos.log`, o sin renglones `N fin`, la alarma no corre.
  - U-193: "revisor distinto del canon" pasa en vacío si los autores del canon no se registran; cualquier rol `revisor*` vale.
- **Bloqueos de publicación aparte:**
  - BE-GK54 falta en el candidato (verificar_version: FALTAN).
  - Falta `skills_archivo/PROYECTOS_ABIERTOS.json`.
  - PRUEBA_ABIERTOS solo trae XF.
- Corridas: suite 47/47 OK; selftest 13/13 OK; 0 tests sin llamar.
- Recomendación: no publicar v81cf119 como "0 WEAK". Antes hay que:
  - cerrar los 4 STILL-WEAK (son arreglos chicos, cada uno con su test);
  - unir BE-GK54;
  - completar PRUEBA_ABIERTOS con GK y CR, corrido con el candidato final.
