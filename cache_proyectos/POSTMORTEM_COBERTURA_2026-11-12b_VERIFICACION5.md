# VERIFICACIÓN INDEPENDIENTE 5 (dirigida): candidato v81cf120 (commit 056b3a0)

Fecha: 2026-11-12 14:09 PT

La hizo un revisor independiente que no escribió el código. Fue una verificación DIRIGIDA a:
- los 5 STILL-WEAK de la verificación 4: U-185, NG-3.1 / BE-PM04, NG-3.3 / BE-PM06, U-193 y BE-GK54;
- 2 funciones nuevas de la Ampliación 3: el retroactivo de proceso (`proceso_v119`) y CB_FALTANTES_AUDITORIA.

No se tocó ninguna tool.

## Qué se revisó

- **Base:** `skills_archivo/take-off-metal-frame-drywall_v81cf119_U193-cobertura_2026-11-12.zip`.
- **Parche:** `apartados/v81cf120_desde_v81cf119.patch`, aplicado con `patch -p1`.
  - v120 todavía no está publicado como zip.
  - Resultado: 199 archivos y `VERSION: v81cf120`.
- **Órdenes:** `apartados/ordenes_v120/*.py` en una copia de `.claude/skills/jc-hunter-ordenes/`, junto con `.claude/hooks/`.
- **Copia del cache:** copia mínima con los `POSTMORTEM_*`, `SUBIDA_OK*`, `VERSION_PROYECTO.txt` y `CSV_BLUEBEAM_*/RESULTADO.md`.
  - `adv_pm_real.py` y `adv4_pm.py` corrieron SOLO sobre esa copia.
  - El cache real no se modificó.
- **Adversariales nuevos:** en `scratchpad/adv120v5/`, sin commit (salvo este informe):
  - adv5_pm.py
  - adv5_pm04.py
  - adv5_pm06.py
  - adv5_u193.py
  - adv5_gk54.py
  - adv5_proceso.py
  - adv5_faltantes.py

## Corridas

**Pruebas del candidato**
- Suite `correr_suite.py` (con TAKEOFF_SKILL = candidato): **47/47 OK**.
- `verificar_version.py --selftest`: **OK**. Incluye postmortem_u185, tests_llamados, prueba_abiertos_be_pm04, adv4_postmortem y adv4_prueba_abiertos.

**verificar_version sobre el candidato, con skills_archivo y cache_proyectos reales (solo lectura, antes de este archivo)**
- Faltan 0 reglas.
- REGISTRO OK.
- U-185 da 5 fallas:
  - las 4 verificaciones anteriores no tienen 'Fecha:';
  - el 12b tiene 10 renglones abiertos.
- Falta `PRUEBA_ABIERTOS_v81cf120.json`.

**adversariales_v119 (todos re-corridos)**
- adv_pm: A1 a A5 y B1 dan falla.
- adv_pm_real: C1 a C4 dejan los renglones abiertos.
- adv_pm04:
  - P4a a P4e quedan ABIERTOS. Ojo: sin 'Comparado:' hasta el control P4-0 queda abierto, lo cual es conservador.
  - P8 está documentado.
- adv_pm06: C da alerta.
- adv_gk54: G1 a G4 y G6 dan True. G5 sigue siendo un límite documentado.
- adv_cr40: FAIL en los 4 casos.
- adv_u193: ya no corre por la firma de 4 valores; lo cubre adv4_u193.

**adversariales_v120 (todos re-corridos)**
- adv4_pm: D1 a D6 no cierran.
  - El control D7 tampoco cierra, porque esas verificaciones sintéticas no traen 'Fecha:'.
  - El control equivalente con 'Fecha:' cierra: es el E0 de adv5_pm.
- adv4_pm04: Q1 a Q9 quedan abiertos o dan falla.
- adv4_pm06: F0 a F7 se exigen; F8 limpia.
- adv4_u193: U6 a U13 se rechazan; el control U0 se acepta.
- adv4_gk54: H0 a H4 y H7 dan FAIL; H5 no da FAIL, que es lo correcto.

## Tabla

| id | error / regla | chequeo | test | estado |
|---|---|---|---|---|
| U-185 | Post-mortem de cobertura al cerrar cada proyecto | `verificar_version.revisar_postmortem` | `postmortem_u185` + `adv4_postmortem` | OK — CONFIRMED-CLOSED |
| U-189 | Cielos apilados, detalle cara por cara y COBERTURA | `CB_RCP_APILADOS`, `CB_DETALLE_CARAS`, `cobertura_esperada` | CASOS + `test_v119_postmortem_12b` | OK — CONFIRMED-CLOSED |
| U-190 | REGLA DE ORO #3 doble cielo | `CE_DOBLE_CIELO` + `refs_doble_fallas` | `test_u190_doble_cielo` | OK — CONFIRMED-CLOSED |
| BE-CR39 | rev19 terminado sin el GYP-1 de los corredores | Igual que U-189 / U-190 | `test_v119_postmortem_12b` | OK — CONFIRMED-CLOSED |
| BE-CR40 | Cielo declarado faltante buscando texto | `CB_FALTANTES_AUDITORIA` (`faltantes_auditoria`) | `test_v119_be_cr40_verificacion` | WEAK — STILL-WEAK |
| BE-CR42 | Conflicto plano vs plano sin delta | `conflictos_sin_delta` + `tests_sin_llamar` | `test_be_cr42_…` | OK — CONFIRMED-CLOSED |
| BE-GK47 | '60.0 LF' leído como 'impreso en 0' | CB_BE_HF02 | El mismo test de BE-CR42 | OK — CONFIRMED-CLOSED |
| NG-3.1 / BE-PM04 | Versión nueva no probada sobre los proyectos abiertos | `revisar_prueba_abiertos` + `proyectos_abiertos_cache` | `prueba_abiertos_be_pm04` + `adv4_prueba_abiertos` | WEAK — STILL-WEAK |
| NG-3.2 / BE-PM05 | Versión cambiada a mitad de la compuerta final | `version_proyecto_fallas` | `test_v119_postmortem_12b` | OK — CONFIRMED-CLOSED |
| NG-3.3 / BE-PM06 | Sin alarma de presupuesto mientras se trabaja | `alarma_fallas` + `filas_tiempos` + `pasos_cerrados_tiempos` | `test_v120_adv4` | WEAK — STILL-WEAK |
| U-193 | MAPA DE COBERTURA: revisor distinto del autor | `subagentes_bitacora` + `ce_cobertura` | `test_v119_cobertura` + `test_v120_adv4` | WEAK — STILL-WEAK |
| BE-PM08 | `COBERTURA - IMAGE ONLY.pdf` tomado por PDF de markups | `nombres_planos` | `test_v119_gk_nombres_y_bitacora` | OK — CONFIRMED-CLOSED |
| BE-PM09 | Bitácora de GK en `takeoff_work/` no se leía | `_bitacoras` | `test_v119_gk_nombres_y_bitacora` | OK — CONFIRMED-CLOSED |
| BE-GK54 | Dos leaves con gap = dos walls | `be_gk54_fallas` + `gk54_mismo_muro` + `gap_prueba_ok` | `test_be_gk54` + `test_v120_adv4` | WEAK — STILL-WEAK |
| v120-RETRO | Retroactivo de proceso (CE_PROTOCOLO_3H `proceso_v119`, log viejo) | `proceso_v119` + `inicio_rev` + `marcas_tiempos_log` | `test_v120_retroactivo_proceso` | WEAK — STILL-WEAK |
| v120-FALT | CB_FALTANTES_AUDITORIA (cualquier ref, hoja faltante, DOBLE_CIELO) | `faltantes_auditoria` + `_ref_cargada` + `RX_HOJA_FALTANTE` + `cuartos_doble_cielo` | `test_v119_be_cr40_verificacion` | WEAK — STILL-WEAK |

## Detalle por renglón

### U-185 — OK — CONFIRMED-CLOSED

Siguen cerrados D1 a D6 de la verificación 4.

Entradas nuevas (adv5_pm.py), todas fallan en cerrado:
- **E3:** 'OK — CONFIRMED-CLOSED. (but … WEAK)' no cierra.
- **E4:** 'OK — CONFIRMED-CLOSED (con reserva)' no cierra.
- **E6:** una verificación que omite los renglones WEAK los deja abiertos.
- **E7:** una fecha con typo en el futuro (2026-11-21) da falla.
- **E8:** una columna extra después de 'estado' da "sin tabla" y falla.
- **E9:** una verificación posterior con WEAK reabre el renglón.
- **E1:** '**Fecha:**' en negrita no se reconoce y da falla. Es ruidoso, no silencioso.

Controles:
- **E0:** con 'Fecha:' correcta, la verificación cierra.
- **E5:** con la misma Fecha que la anterior, cierra por el orden de nombre.

Observaciones (no son huecos silenciosos):
1. **Bloqueo de publicación.** Las 4 verificaciones del 12b que ya existen no traen 'Fecha:'.
   - Por eso `revisar_postmortem` da falla PARA SIEMPRE sobre el cache real: E0b muestra 4 fallas aunque exista esta verificación 5 con todo cerrado.
   - COORDINACIÓN tiene que decidir una de dos: un corte (las verificaciones anteriores a v120 quedan exentas del campo) o agregarles la Fecha con la hora de su commit.
   - Hoy el chequeo NO puede quedar verde.
2. `main()` llama `revisar_postmortem(extra[0] if extra else None)`. Si `verificar_version.py` se corre a mano SIN el 3er argumento, U-185 no corre.
   - `revisar_prueba_abiertos` sí usa el cache de al lado.
   - El hook `arranque_reglas.sh` sí pasa `cache_proyectos`.

### BE-CR40 — WEAK — STILL-WEAK (regresión de la Ampliación 3)

adv_cr40 sigue en FAIL en sus 4 casos. Pero los cambios de v120 en `faltantes_auditoria` abren huecos nuevos en la MISMA dirección de BE-CR40: un cielo CARGADO que se declara faltante.

Reproducido con adv5_faltantes.py:
- **Canon:** corridor 901 cargado en `ceilings[0]` y `rcp_tags` GYP-9 con rows ['ceilings[0]'].
- **Control L0:** 'X9.01 GYP-9 8'-11" missing in corridor 901' da FAIL.
- **L1:** el mismo renglón + 'along wall X9-901-01' da **PASS**.
  - Basta que el renglón nombre CUALQUIER ref cargada como contexto (un wall vecino, un soffit) para que `cargadas` lo cuente como cerrado.
- **L2:** el mismo renglón + 'per 7/X9.23 (not in canon)' da **N/A**. `RX_HOJA_FALTANTE` lo toma por "hoja faltante" y salta el renglón.
- **L2b:** 'corridor 901 ceiling per 7/X9.23 not included in take-off' da **N/A**.

### NG-3.1 / BE-PM04 — WEAK — STILL-WEAK

Cerrados de la verificación 4: Q1 a Q9 dan abierto o falla.

Huecos nuevos, reproducidos con adv5_pm04.py:
- **R1b:** CSV viejo vuelto a comparar.
  - SUBIDA_OK_rev19 (11-11) + SUBIDA_OK_rev20 (2026-11-12T18:00Z).
  - Solo existe `CSV_BLUEBEAM_rev19/RESULTADO.md`, re-corrido con 'Comparado: 2026-11-12 12:00 PT' y N/N.
  - El proyecto queda **CERRADO**: no se compara la rev de la carpeta CSV con la rev de la última subida.
- **R2:** subida dentro de una subcarpeta.
  - El proyecto guarda su `SUBIDA_OK.json` en una subcarpeta de la rev (`proj/REV3_FINAL/SUBIDA_OK.json`, el layout que usa `oreilly_p2`).
  - `_es_proyecto` = False y `proyectos_abiertos_cache` = [].
  - El proyecto abierto se omite en silencio y no hay error.

Defecto que falla en cerrado (no hace pasar nada, pero el chequeo es inútil para cerrar):
- `_fecha_resultado` aplica `RX_COMPARADO` (con `^`, multilínea) sobre `norm_txt(tx)`, que junta TODAS las líneas en una.
- Resultado: 'Comparado:' solo se reconoce si es lo PRIMERO del archivo. R0: un RESULTADO.md con una línea de título antes, como el real de CR, nunca cierra.
- El caso Q3 del test pasa por este defecto, no por la comparación de horas.

### NG-3.3 / BE-PM06 — WEAK — STILL-WEAK

Cerrados de la verificación 4: F1 a F7.

Hueco nuevo, reproducido con adv5_pm06.py:
- Se usa el formato común de la columna paso con texto: 'Paso 1' / '1. Inventario' / '1 Inventario' / 'Step 1' (M1 a M4).
- `RX_PASO_CELDA` (`^\d…$`) no los reconoce, así que `filas_tiempos` deja `nums = []` y `pasos_cerrados_tiempos` = [].
- Si además tiempos.log no trae el texto 'N fin' (caso E3 de la verificación 3), el resultado es:
  - `alarma_fallas` = [] SIN ninguna corrida --paso;
  - CE_TIEMPOS = [];
  - `tiempos_cuadran` = [].
- Control M0 ('1', '2-3', '4'): exige los 3 --paso.

### U-193 — WEAK — STILL-WEAK

Cerrados de la verificación 4: U6 a U13. El rol mal escrito 'revisor-cobertura' (V5) se rechaza.

Hueco nuevo, reproducido con adv5_u193.py: `norm_txt` no unifica los separadores. Un revisor que difiere del autor del canon solo en el separador se acepta como distinto:
- **V1:** autor 'subagente A1' y revisor 'subagente_A1'.
- **V2:** 'subagente-A1'.
- **V4:** 'lectura-A' / 'lectura A'.
- **V3:** prefijo: autor `SUBAGENTE_ID=A1` y revisor 'subagente A1'.

Es realista: SUBAGENTE_ID va en una variable de entorno, que se escribe sin espacios ('subagente_A1'), y la columna reviewer del CSV se escribe con espacio.

Límite inherente que hay que documentar: los ids se declaran a sí mismos. Ninguna normalización prueba la identidad.

### BE-GK54 — WEAK — STILL-WEAK

Cerrados de la verificación 4: H0 a H4 y H7.

Huecos nuevos, reproducidos con adv5_gk54.py (leaf roja paralela a 4 in, sin gap_proof):

- **K1, razones de exclusión fuera de la lista de sinónimos.** Pasan en silencio:
  - 'covered by X9-Z9-08'
  - 'accounted for in …'
  - 'merged with …'
  - 'carried in …'
  - 'taken off with …'
  - 'other leaf of …'
  - 'double leaf - …'
  - 'furring side of … (one wall)'

  La lista de sinónimos es abierta. Sigue sin aplicarse la alternativa propuesta en la verificación 4: exigir gap_proof en TODA exclusión cuya razón cite un id de wall del canon.

- **K2, disposición sin exclusión en el canon.** Si el canon NO trae una exclusión (`excluded_walls` vacío) y el revisor dispone el rojo como 'NO ES NUESTRO: same wall as X9-Z9-08 (1/Z9.11)', 'part of …' o 'counted in …':
  - `be_gk54_fallas` no lo evalúa, porque solo recorre las exclusiones del canon;
  - el rojo DISPUESTO como "el mismo muro" pasa sin la prueba del gap.

- **K3, menor y fail-closed.** Un gap_proof real como '0" gap, 3-5/8" studs back to back (1/Z9.11)' se rechaza: toda medida tiene que ser 0. Es ruidoso, no silencioso.

### v120-RETRO (`proceso_v119`) — WEAK — STILL-WEAK

Controles:
- P0: una rev con su propio log del 13-nov da FAIL.
- P2: formato viejo '12-nov 14:30 PST' (después de FECHA_V119) da FAIL.
- P4: sin log y sin git da FAIL.

Huecos (adv5_proceso.py):
- **P1 / P1b:** tiempos.log es POR PROYECTO y se acumula entre revs. Así está en el cache real: `cr_city_hotel_castle_rock/tiempos.log` empieza el 05-nov y `xfinity_interquest/tiempos.log` el 2026-11-10.
  - `_tiempos_log` busca en la carpeta de trabajo y en la de arriba.
  - `inicio_rev` toma la PRIMERA marca del log.
  - Resultado: una rev21 que arranca el 13-nov y se anota en el log del proyecto da **AMBER** ("arrancó 2026-11-05"), no FAIL. Todo CR / XF / GK futuro queda exento para siempre.
- **P3:** una línea de encabezado copiada de la rev anterior ('10-nov 21:01 PST | (copiado de rev3)') da AMBER.
- **P5:** un typo de año en la primera línea ('2025-11-13') da AMBER.

Arreglo sugerido: tomar como arranque la marca de inicio de ESTA rev (por ejemplo VERSION_PROYECTO.txt o la línea 'rev N inicio'), no la primera línea del log.

Además, `minutos_tiempos_log` (el que escribe la alerta) solo lee ISO, y `marcas_tiempos_log` (el que la exige) lee también el formato viejo. Con un log viejo, la alerta nunca se escribe, pero se exige. Falla en cerrado.

### v120-FALT (CB_FALTANTES_AUDITORIA) — WEAK — STILL-WEAK

Son los mismos huecos L1, L2 y L2b de BE-CR40:
- el cierre "con cualquier ref cargada" toma como cierre una ref que solo es contexto;
- `RX_HOJA_FALTANTE` se come renglones de cielo que citan un detalle con '(not in …' o 'not included'.

DOBLE_CIELO, menor:
- la tabla resuelve un hallazgo con solo que su columna 'Row / reason' contenga las palabras 'upper' y 'lower';
- no se verifica que las refs citadas existan en el canon;
- J3 y J3b: 'lower: GYP-9 MISSING' o 'lower: CLG-Z9-216 (no existe)' resuelven el hallazgo.

## Resumen

**CONFIRMED-CLOSED (9):** U-185, U-189, U-190, BE-CR39, BE-CR42, BE-GK47, NG-3.2 / BE-PM05, BE-PM08 y BE-PM09.
- U-185 sale de STILL-WEAK, con el bloqueo de publicación de la Fecha en las verificaciones 1 a 4.

**STILL-WEAK (7):**
- BE-CR40, regresión de v120 Ampliación 3;
- NG-3.1 / BE-PM04;
- NG-3.3 / BE-PM06;
- U-193;
- BE-GK54;
- v120-RETRO;
- v120-FALT.

**Bloqueos de publicación:**
1. U-185 nunca queda verde con el cache real mientras las verificaciones 1 a 4 no tengan 'Fecha:' o no exista un corte.
2. Falta `skills_archivo/PRUEBA_ABIERTOS_v81cf120.json` (hoy solo trae XF; faltan GK y CR).
3. Por el defecto de `_fecha_resultado`, el RESULTADO.md real de CR nunca cierra aunque traiga 'Comparado:', salvo que vaya en la primera línea.

**Recomendación:** no publicar v81cf120 como "0 WEAK".
