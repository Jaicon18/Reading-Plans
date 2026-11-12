# VERIFICACIÓN INDEPENDIENTE 3 del candidato v81cf119 (commit e55a8ae)

2026-11-12 13:16 PT. Revisor independiente que no escribió el código. Se verificó leyendo el código, corriéndolo y con entradas adversariales nuevas para cada renglón. No se tocó ninguna tool.

## Qué se revisó

- Base: `skills_archivo/take-off-metal-frame-drywall_v81cf118_U191-excluded-cero_2026-11-12.zip`.
- Parche: `apartados/v81cf119_desde_v81cf118.patch` (e55a8ae), aplicado con `patch -p1`. Resultado: 199 archivos, `VERSION: v81cf119`.
- `apartados/ordenes_v119/*.py` se copiaron a una copia de `.claude/` (el selftest necesita `hooks/` a su lado).
- Scripts:
  - los adversariales anteriores están en `scratchpad/adv119/`;
  - los nuevos están en `scratchpad/adv119v3/`: adv_pm_real.py, adv_pm04.py, adv_pm06.py, adv_u193.py y adv_gk54.py.

## Corridas

- **Suite** `correr_suite.py`: **47/47 OK**.
- **Selftest de verificar_version v119**: **13/13 OK** (test_verificar_version OK).
- **verificar_version sobre el candidato** (con skills_archivo y cache_proyectos reales):
  - reglas: faltan 0 (**BE-GK54 ya está unido**);
  - U-185: 6 abiertos (U-185, causa 3.1, causa 3.3, NG-3.1 / BE-PM04, NG-3.3 / BE-PM06, U-193);
  - falta `skills_archivo/PROYECTOS_ABIERTOS.json`.
- **adv119 re-corridos**:
  - A3b ya da FALLA: una verificación sin tabla es falla y además los WEAK anteriores siguen abiertos.
  - A4 ya da FALLA: un renglón omitido sigue abierto.
  - B1 ya da FALLA: lista de abiertos vacía.
  - adv_cr40 sigue en FAIL en los 4 casos.
  - A2 (un principal más nuevo tapa al anterior) **sigue pasando**.
- **sha_tools**: el que calcula verificar_version es igual al de compuerta_entrega (13bc6d26f5c1). PRUEBA_ABIERTOS de XF trae ese mismo sha. El de GK no trae sha_tools y su clave es `entrega_rev3a`. CR no está.

## Tabla

| id | error / regla | chequeo | test | estado |
|---|---|---|---|---|
| U-185 | Post-mortem de cobertura al cerrar cada proyecto | `verificar_version.revisar_postmortem` | `postmortem_u185` (selftest OK) | WEAK — STILL-WEAK. Lo cerrado (reproducido): una verificación sin tabla = falla; un renglón abierto sigue abierto si la verificación nueva lo omite; las verificaciones se aplican en orden de hora (una verificación con hora vieja no tapa a la VERIFICACION2). Huecos reproducidos: (1) C4: un estado 'WEAK — NOT CONFIRMED' + guion + 'CLOSED' CIERRA el renglón, porque `re.search(CONFIRMED[- ]CLOSED)` busca en cualquier parte del estado (sobre el cache real, una VERIFICACION3 con los 4 renglones así da `[]`). Lo confirmó el primer borrador de este mismo archivo: el texto de este renglón citaba esa palabra y cerró U-185 por error. Por eso aquí va deletreada. (2) C1 / A2: un principal nuevo `POSTMORTEM_COBERTURA_2026-11-12c.md` con un solo renglón OK hace desaparecer los 6 abiertos del 12b (cache real, da `[]`). Arreglo propuesto: el estado tiene que EMPEZAR con `OK` y además traer el token de cierre; los abiertos de principales anteriores se arrastran hasta cerrarse explícitamente. |
| U-189 | Cielos apilados, detalle cara por cara y COBERTURA | `CB_RCP_APILADOS`, `CB_DETALLE_CARAS`, `cobertura_esperada` | CASOS + `test_v119_postmortem_12b` | OK — CONFIRMED-CLOSED. Sin cambios de fondo en e55a8ae; suite OK. |
| U-190 | REGLA DE ORO #3 doble cielo | `CE_DOBLE_CIELO` + `refs_doble_fallas` | `test_v119_postmortem_12b` + `test_u190_doble_cielo` | OK — CONFIRMED-CLOSED. Sin cambios; suite OK. |
| BE-CR39 | rev19 terminado sin el GYP-1 de los corredores | Igual que U-189 / U-190 | `test_v119_postmortem_12b` | OK — CONFIRMED-CLOSED en el código. Pendiente con datos reales: CLG-L2-217F / CLG-L3-317F de CR rev20a. |
| BE-CR40 | Cielo declarado faltante buscando texto | `CB_FALTANTES_AUDITORIA` | `test_v119_be_cr40_verificacion` | OK — CONFIRMED-CLOSED. adv_cr40 re-corrido: FAIL en los 4 casos. |
| BE-CR42 | Conflicto plano vs plano sin delta | `conflictos_sin_delta` + `tests_sin_llamar` | `test_be_cr42_…` (se llama) | OK — CONFIRMED-CLOSED. verificar_version: 0 tests sin llamar. |
| BE-GK47 | '60.0 LF' leído como 'impreso en 0' | CB_BE_HF02 | El mismo test de BE-CR42 | OK — CONFIRMED-CLOSED |
| NG-3.1 / BE-PM04 | Versión nueva no probada sobre los proyectos abiertos | `revisar_prueba_abiertos` + `proyectos_abiertos_cache` + `sha_tools` | `prueba_abiertos_be_pm04` | WEAK — STILL-WEAK. Lo cerrado (reproducido): lista vacía = falla; sha_tools distinto o ausente = falla (P2 / P2b); proyecto abierto en el cache que no está en la lista = falla (P7); un `SUBIDA_OK_rev2` más nuevo que el CSV N/N de rev1 cuenta como ABIERTO (P4a). Huecos reproducidos: (1) **P4b: un proyecto con CSV N/N de rev1 y un `SUBIDA_OK.json` (sin rev) MÁS NUEVO se da por CERRADO.** Si el nombre no trae rev, cualquier `CSV_BLUEBEAM_*` lo cierra, sin comparar fechas. `subir_entrega.py` escribe justamente `SUBIDA_OK.json` sin rev, y XF lo usa así. (2) P4c: una rev nueva en curso (`VERSION_PROYECTO.txt` con rev2 más nuevo que el CSV, sin subida) no cuenta como abierta. (3) P3: las regresiones por proyecto (`proyectos.<p>.regresiones = 5`, `sin_explicar = 5`) no se leen; solo cuenta la lista de arriba, que se puede editar a mano. (4) P8: sin el 3er argumento (cache), `proyectos_abiertos_cache` no corre. Menor: P4d, un RESULTADO con '0 faltantes' y también '3 faltantes' cierra. |
| NG-3.2 / BE-PM05 | Versión cambiada a mitad de la compuerta final | `version_proyecto_fallas` | `test_v119_postmortem_12b` | OK — CONFIRMED-CLOSED. Sin cambios. |
| NG-3.3 / BE-PM06 | Sin alarma de presupuesto mientras se trabaja | `alarma_fallas` (con `tiempos_txt`) + `tiempos_cuadran_fallas` + `sellos_fallas` / `sellar_bitacora` | `test_v119_alarma_verificacion2` + `test_v119_alarma_presupuesto` | WEAK — STILL-WEAK (residual angosto). Lo cerrado (reproducido): una entrega nueva sin tiempos.log = FAIL (E1 / E1b); TIEMPOS.md y el log tienen que cuadrar hora por hora (CE_TIEMPOS además exige el Fin de los pasos 1-9, así que E2 queda cubierto); ALERTA_PRESUPUESTO.json editado a mano = FAIL por sha (E4b). Hueco reproducido: **E3, un tiempos.log con las marcas a las horas de fin pero SIN el texto `N fin`** ('09:00 inventario listo') deja sin exigir las corridas `--paso` (el registro va con 0 corridas y solo sale la alerta del 50 %). Es el punto (2) de la verificación 2, que no se cerró. Arreglo propuesto: `tiempos_cuadran_fallas` exige que la marca de cada paso cerrado diga `N fin`, o que la parte (1) de la alarma use los pasos de TIEMPOS.md. Notas: E5, un SELLO crudo agregado a mano pasa `sellos_fallas` pero rompe la cadena (A_BITACORA_FINAL lo atrapa); E6, llamar `sellar_bitacora()` a mano re-sella, y eso es un límite del diseño. |
| U-193 | MAPA DE COBERTURA: revisor registrado, distinto del autor, rol exacto | `subagentes_bitacora` + `ce_cobertura` | `test_v119_cobertura` + `test_v119_mutacion_cobertura` | WEAK — STILL-WEAK (residual angosto). Lo cerrado (reproducido): sin autores del canon registrados = FAIL (U1); rol `revisor_otro` / `revisor_de_lo_que_sea` no vale (U3); un revisor que corrió una tool de las etapas 2-7 (closer.py con su agente) = FAIL (U4); un revisor también registrado como takeoff = FAIL (U5); FALTA, decisión vacía o nhoja sin N/HOJA no limpian. Huecos reproducidos: (1) **U6: con `bitacora.py subagente canon FAKE-CANON` y canon.py corrido SIN `agente`, el autor real se registra como revisor_cobertura y PASA.** Que el autor sea distinto sigue siendo autodeclarado: nada exige que cada corrida de canon.py (y de las etapas 2-7) traiga su `agente`. (2) U7: la comparación distingue mayúsculas: el agente `author-1` del canon.py y el revisor `AUTHOR-1` pasan. Arreglo propuesto: en entregas nuevas, toda corrida de canon.py / etapas 2-7 sin `agente` = FAIL, y comparar los ids sin distinguir mayúsculas. |
| BE-PM08 | `COBERTURA - IMAGE ONLY.pdf` tomado por PDF de markups | `nombres_planos` | `test_v119_gk_nombres_y_bitacora` | OK — CONFIRMED-CLOSED. Sin cambios. |
| BE-PM09 | Bitácora de GK en `takeoff_work/` no se leía | `_bitacoras` | `test_v119_gk_nombres_y_bitacora` | OK — CONFIRMED-CLOSED. Sin cambios. |
| BE-GK54 | Dos leaves con gap = dos walls ('same wall as X' esconde una leaf) | `be_gk54_fallas` + `_gk54_desde_pdf` dentro de CE_COBERTURA | `test_be_gk54` (se llama, test_compuerta_entrega 2772) | WEAK — STILL-WEAK. Ya unido al candidato: está en SKILL.md y en el registro, y verificar_version dice faltan 0. El caso real de GK (rotación 270) da FAIL. Huecos reproducidos (adv_gk54): (1) G1: `RX_GK54_SAME` solo reconoce ids con el formato de GK (`X-Z9-08`). 'same single wall as TO-W.4-L2-02' (CR) o 'same wall as W-12' quedan en silencio. (2) G2: con un sinónimo ('same as X9-Z9-08', 'duplicate of …', 'part of wall …') no se revisa. (3) G3: `gap_proof` acepta cualquier texto ('n/a'), aunque la regla pide N/HOJA. (4) G6: si el wall X no tiene `band` en el canon, se salta en silencio. (5) G5: el caso de leaves fusionadas no se detecta. Si el detector del mapa empareja las dos leaves como un solo muro cubierto, no hay banda roja aparte y la exclusión pasa. Es un límite del mapa y no está documentado en los límites de la GUÍA. Arreglo propuesto: ids genéricos y sinónimos; gap_proof con RX_NH_TRAZA; X sin band = FAIL; agregar el caso fusionado a los límites o exigir gap_proof en toda exclusión 'same wall'. |

## Resumen

- **CONFIRMED-CLOSED (9):** U-189, U-190, BE-CR39, BE-CR40, BE-CR42, BE-GK47, NG-3.2 / BE-PM05, BE-PM08, BE-PM09.
- **STILL-WEAK (5):**
  - U-185: un estado WEAK que menciona el token de cierre ('NOT CONFIRMED' + guion + 'CLOSED') cierra el renglón; un principal nuevo tapa los abiertos del anterior.
  - NG-3.1 / BE-PM04: un `SUBIDA_OK.json` sin rev, más nuevo que el CSV N/N, se da por cerrado; una rev en curso con VERSION_PROYECTO no cuenta; las regresiones por proyecto no se leen.
  - NG-3.3 / BE-PM06: las marcas del log sin 'N fin' saltan la exigencia de las corridas `--paso`.
  - U-193: el autor del canon sigue siendo autodeclarado (canon.py sin agente + canon falso registrado = PASS); la comparación distingue mayúsculas.
  - BE-GK54: el regex es solo para ids de GK; sin sinónimos; gap_proof sin N/HOJA; X sin band se salta; leaves fusionadas.
- **Pregunta explícita de COORDINACIÓN** (CSV N/N con una rev más nueva en curso):
  - con un `SUBIDA_OK_revN.json` más nuevo, sí cuenta como ABIERTO;
  - con un `SUBIDA_OK.json` sin rev más nuevo, NO cuenta (P4b);
  - con un `VERSION_PROYECTO.txt` más nuevo, NO cuenta (P4c).
- **Bloqueos de publicación aparte:**
  - falta `skills_archivo/PROYECTOS_ABIERTOS.json`;
  - el PRUEBA_ABIERTOS de GK no trae sha_tools y su clave es `entrega_rev3a` (no `grand_kia`);
  - falta CR (COORDINACIÓN lo lista como abierto; `proyectos_abiertos_cache` lo da por cerrado con el CSV rev20a).
- Corridas: suite 47/47; selftest 13/13; 0 tests sin llamar; BE-GK54 unido.
- Recomendación: no publicar v81cf119 como "0 WEAK".
