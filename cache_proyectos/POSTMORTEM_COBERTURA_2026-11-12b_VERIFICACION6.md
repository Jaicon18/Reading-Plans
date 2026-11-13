# VERIFICACIÓN INDEPENDIENTE 6 (dirigida): candidato v81cf137 (VIGENTE)

Fecha: 2026-11-12 22:40 PT

(= 2026-11-13 06:40 UTC. La hora del contenedor en California todavía es el 12-nov; se escribe la hora real para que
`revisar_postmortem` no la tome como fecha en el futuro.)

La hizo un revisor independiente que no escribió el código. Fue una verificación DIRIGIDA a los 11 renglones abiertos que reporta
`verificar_version.py`. Son 7 renglones distintos de la tabla, porque NG-3.1 / BE-PM04 y NG-3.3 / BE-PM06 abren tres claves cada uno
(`ng-3.x / be-pm0x`, `causa 3.x` y `be-pm0x`):
- BE-CR40;
- NG-3.1 / BE-PM04;
- NG-3.3 / BE-PM06;
- U-193;
- BE-GK54;
- v120-RETRO;
- v120-FALT.

No se tocó ninguna tool, ni el cache real (salvo este archivo), ni Drive. No se hizo commit.

## Qué se revisó

- **Candidato:** `skills_archivo/take-off-metal-frame-drywall_v81cf137_lecturas-walls-fechas-reales_2026-11-13.zip`.
  - Descomprimido en `/tmp/verif6/take-off-metal-frame-drywall`.
  - Su SKILL.md dice `VERSION: v81cf137`.
- **Cambios desde v120:**
  - `apartados/LEEME_v81cf121.md`, que trae los 7 arreglos estructurales de la verificación 5;
  - los parches `v81cf121…v81cf137_desde_*.patch`, en particular v122 (corridas sin agente antes de v119 = AMBER), v124 / v125 (GK54 casos (a) / (b)) y v126 (GK54 enlace por id de canon, sin agente reemplazado = AMBER, entregas previas fuera de CB_FALTANTES).
- **Órdenes:** `.claude/skills/jc-hunter-ordenes/verificar_version.py`. Es igual a `apartados/ordenes_v137/`.
- **Adversariales nuevos:** en `/tmp/verif6/adv/`, fuera del repo:
  - adv6_cr40.py
  - adv6_pm04.py
  - adv6_pm06.py
  - adv6_u193.py
  - adv6_gk54.py
  - adv6_retro.py

  Todos son sintéticos. Solo adv6_pm04 W4 lee el cache real, y en modo lectura. Los que escriben (bitácora, ALERTA_PRESUPUESTO, tiempos.log) escriben solo en `/tmp/verif6/tmp`.

## Corridas

**Pruebas del candidato**
- Suite `correr_suite.py --skill /tmp/verif6/take-off-metal-frame-drywall` (con TAKEOFF_SKILL = candidato): **47/47 OK**.
- `verificar_version.py --selftest`: **OK**. Incluye adv5_v121 y fechas_be_xf17.

**verificar_version sobre el candidato, con skills_archivo y cache_proyectos reales (antes de este archivo)**
- Faltan 0 reglas.
- POSTMORTEM: 11 WEAK abiertos (la lista de arriba).
- PRUEBA ABIERTOS: `PRUEBA_ABIERTOS_v81cf137.json` no trae grand_kia ni cr_city_hotel_castle_rock.

**adversariales_v120v5 re-corridos sobre el candidato**
- adv5_faltantes:
  - L0 a L3 dan FAIL. Es lo correcto.
  - J0 a J3b dan PASS. Es lo correcto: son faltantes de verdad, contados.
- adv5_gk54:
  - K0, K1 (los 9 sinónimos) y K2 (las 3 disposiciones) dan FAIL.
  - En K3, 'no gap between leaves (1/Z9.11)' sigue rechazado. Es ruidoso, no silencioso.
- adv5_pm04: R0 a R5c correctos. R1 y R2 ya quedan abiertos.
- adv5_pm06: M1 a M4 exigen las 3 corridas --paso, igual que el control M0.
- adv5_proceso: P1, P1b, P3 y P5 ya dan FAIL.
- adv5_u193:
  - Su `judge` quedó viejo: compara `norm_txt` contra ids `norm_agente`, por eso incluso el control V0 sale False.
  - Re-hecho en adv6_u193 con la lógica real de `ce_cobertura`: V0 PASS y V1 a V4 rechazados.

**adversariales v119 / v120 re-corridos**
- adv4_gk54: H0 a H7 dan FAIL.
- adv_gk54: G0 a G6 dan FAIL. G5 sigue siendo el límite documentado.
- adv_cr40: FAIL en los 4 casos. Además, 'non-auditoria path' da N/A, que es el hueco S3 de abajo.

## Tabla

| id | error / regla | chequeo | test | estado |
|---|---|---|---|---|
| U-185 | Post-mortem de cobertura al cerrar cada proyecto | `verificar_version.revisar_postmortem` | `postmortem_u185` + `adv4_postmortem` + `adv5_v121` | OK — CONFIRMED-CLOSED |
| U-189 | Cielos apilados, detalle cara por cara y COBERTURA | `CB_RCP_APILADOS`, `CB_DETALLE_CARAS`, `cobertura_esperada` | CASOS + `test_v119_postmortem_12b` | OK — CONFIRMED-CLOSED |
| U-190 | REGLA DE ORO #3 doble cielo | `CE_DOBLE_CIELO` + `refs_doble_fallas` | `test_u190_doble_cielo` | OK — CONFIRMED-CLOSED |
| BE-CR39 | rev19 terminado sin el GYP-1 de los corredores | Igual que U-189 / U-190 | `test_v119_postmortem_12b` | OK — CONFIRMED-CLOSED |
| BE-CR40 | Cielo declarado faltante buscando texto | `CB_FALTANTES_AUDITORIA` (`faltantes_auditoria`, `resolver_faltante`, `RX_HALLAZGO_FALTA`, `es_hallazgo_concreto`) | `test_v121_be_cr40_cierre_explicito` + `test_v119_be_cr40_verificacion` | WEAK — STILL-WEAK |
| BE-CR42 | Conflicto plano vs plano sin delta | `conflictos_sin_delta` + `tests_sin_llamar` | `test_be_cr42_…` | OK — CONFIRMED-CLOSED |
| BE-GK47 | '60.0 LF' leído como 'impreso en 0' | CB_BE_HF02 | El mismo test de BE-CR42 | OK — CONFIRMED-CLOSED |
| NG-3.1 / BE-PM04 | Versión nueva no probada sobre los proyectos abiertos | `revisar_prueba_abiertos` + `proyectos_abiertos_cache` + `csv_cuadra` | `prueba_abiertos_be_pm04` + `adv4_prueba_abiertos` + `adv5_v121` | WEAK — STILL-WEAK |
| NG-3.2 / BE-PM05 | Versión cambiada a mitad de la compuerta final | `version_proyecto_fallas` | `test_v119_postmortem_12b` | OK — CONFIRMED-CLOSED |
| NG-3.3 / BE-PM06 | Sin alarma de presupuesto mientras se trabaja | `alarma_fallas` + `alerta_presupuesto` + `paso_de_celda` | `test_v120_adv4` + `test_v121_estructurales` | WEAK — STILL-WEAK |
| U-193 | MAPA DE COBERTURA: revisor distinto del autor | `subagentes_bitacora` + `norm_agente` + `sin_agente_reemplazadas` + `ce_cobertura` | `test_v119_cobertura` + `test_v121_estructurales` | WEAK — STILL-WEAK |
| BE-PM08 | `COBERTURA - IMAGE ONLY.pdf` tomado por PDF de markups | `nombres_planos` | `test_v119_gk_nombres_y_bitacora` | OK — CONFIRMED-CLOSED |
| BE-PM09 | Bitácora de GK en `takeoff_work/` no se leía | `_bitacoras` | `test_v119_gk_nombres_y_bitacora` | OK — CONFIRMED-CLOSED |
| BE-GK54 | Dos leaves con gap = dos walls | `be_gk54_fallas` + `gap_prueba_ok` + `otro_material_ok` + `es_mismo_muro` | `test_be_gk54` + `test_v121_estructurales` | WEAK — STILL-WEAK |
| v120-RETRO | Retroactivo de proceso (CE_PROTOCOLO_3H `proceso_v119`, log viejo) | `proceso_v119` + `inicio_rev_info` + `_etiqueta_rev` | `test_v121_estructurales` (P1, P1b, P3, P5) | WEAK — STILL-WEAK |
| v120-FALT | CB_FALTANTES_AUDITORIA (cualquier ref, hoja faltante, DOBLE_CIELO) | `faltantes_auditoria` + `cuartos_doble_cielo` + `_seg_cargado` + `RX_HOJA_FALTANTE` | `test_v121_be_cr40_cierre_explicito` + `test_v121_excluded_y_brief` | WEAK — STILL-WEAK |

## Detalle por renglón

### U-189, U-190, BE-CR39, BE-CR42, BE-GK47, NG-3.2 / BE-PM05, BE-PM08 y BE-PM09 — OK — CONFIRMED-CLOSED

Ya estaban cerrados en la verificación 5 y no se re-abrieron. La suite del candidato pasa 47/47, y sus tests siguen en ella.

### U-185 — OK — CONFIRMED-CLOSED

Ya estaba cerrado en la verificación 5.

v121 agregó:
- `fecha_git` para verificaciones sin 'Fecha:';
- `**Fecha:**` en negritas;
- la columna 'estado' tomada por su encabezado;
- `CACHE_DEFECTO` cuando no hay 3er argumento.

El selftest `adv5_v121` pasa. Hoy `revisar_postmortem` corre limpio sobre el cache real, salvo por los abiertos: ya no da la falla de 'Fecha:'.

### BE-CR40 — WEAK — STILL-WEAK

**Lo que pedía la verificación 5:** que un renglón que nombra una ref de contexto (L1) o un detalle '(not in canon)' (L2 / L2b) no cierre un cielo CARGADO declarado faltante.

**Estado en v137:** está arreglado. Ahora solo cierra `CERRADO: <ref> (<N/HOJA>)`, y L0 a L3 dan FAIL. Tiene test: `test_v121_be_cr40_cierre_explicito`.

**Por qué sigue abierto:** el error de fondo de BE-CR40 (un cielo cargado declarado faltante) sigue pasando en silencio. El chequeo solo reconoce un hallazgo si su texto cae en listas CERRADAS de palabras y de formatos. Reproducido con adv6_cr40.py (canon con el corridor 901 cargado en `ceilings[0]` y con el tag GYP-9 apuntando ahí):

- **S1, verbo de "falta" fuera de `RX_HALLAZGO_FALTA`.** Todos dan **N/A** ("sin hallazgos"), cuando lo correcto es FAIL:
  - 'corridor 901 ceiling not found in take-off'
  - 'not taken off'
  - 'not counted'
  - 'absent from estimate'
  - 'ceiling GYP-9 is not in the Excel'
  - 'was left out'
  - 'ceilng missing' (con typo)
  - en español: **'no se cargó el cielo del corredor 901'** y **'corredor 901 sin cielo en el take-off'**

  Controles: 'missing' y 'NOT LOADED' sí dan FAIL.
- **S6, palabra de cielo fuera de `RX_CIELO_PALABRA`.** Dan N/A:
  - 'Cuarto 901: falta el techo de tablaroca'
  - 'Room 901 hard lid missing'
  - 'bulkhead missing (7/X9.23)'
  - 'drywall lid not loaded'
- **S2, cuarto sin 3 o 4 dígitos.** `RX_CUARTO_H` y `es_hallazgo_concreto` no lo ven y dan N/A con el cuarto cargado:
  - 'Corridor C-12 ceiling missing'
  - 'Room B12 ceiling missing'
  - 'room 12 ceiling missing'
- **S3, hallazgo fuera de un archivo con nombre AUDITORIA / INFORME / revision_independiente.** Da N/A:
  - `COORDINACION/hallazgos_rev9.md`
  - `REVIEW_rev9.md`
  - `BITACORA.md`
  - `RESUMEN_rev9.md`
  - `Auditoria/hallazgos.csv`

  El error original de BE-CR40 lo cometió COORDINACIÓN, no un archivo AUDITORIA_*.
- **S5.** Una fila de `DOBLE_CIELO.csv` 'upper: EXT-Z9-2; lower: EXT-Z9-2' resuelve el cuarto 901. Esas son refs cargadas pero ajenas al cuarto (una línea de muro exterior). Con eso, el falso 'corridor 901 ceiling missing' da PASS.

**Para cerrarlo:**
- invertir la lógica: todo renglón de cualquier .md / .csv de Auditoria / COORDINACION / informes que nombre un cuarto, un tag o una ref del canon y lleve una negación (lista abierta, también en español: 'sin', 'no se', 'no aparece', 'not found') se resuelve contra el canon, o se declara explícitamente 'NO ES HALLAZGO';
- ids de cuarto alfanuméricos;
- en DOBLE_CIELO, la ref upper / lower tiene que ser del MISMO cuarto (por room o source).

### NG-3.1 / BE-PM04 — WEAK — STILL-WEAK

**Lo que pedía la verificación 5:** R1b (CSV de otra rev), R2 (SUBIDA_OK en una subcarpeta) y R0 ('Comparado:' no en la primera línea).

**Estado en v137:** los tres están arreglados (adv5_pm04: R0 a R5c correctos) y hay test (`adv5_v121`).

**Por qué sigue abierto:**

1. **El candado no impide publicar, y eso ya pasó.** `verificar_version` reporta que a `PRUEBA_ABIERTOS_v81cf137.json` le faltan grand_kia y cr_city_hotel_castle_rock, y aun así v81cf137 se publicó VIGENTE (commit 0a5f40f).
   - Igual con v131, v133, v134, v135 y v136: sus `PRUEBA_ABIERTOS_*.json` traen SOLO xfinity_interquest.
   - Sin embargo, `proyectos_abiertos_cache` sobre el cache real da `['cr_city_hotel_castle_rock', 'grand_kia', 'xfinity_interquest']`.
   - La causa 3.1 del post-mortem era exactamente "una versión nueva marcada vigente sin correr la compuerta sobre los proyectos abiertos". En la práctica sigue sin candado: el hook `arranque_reglas.sh` solo imprime `head -2` y nada bloquea el commit de publicación.
2. **W1, adv6_pm04.** Un proyecto en curso que todavía no tiene su primera subida no cuenta como abierto: `proyectos_abiertos_cache` = [] y `_es_proyecto` = False. Es una carpeta del cache con canon, TIEMPOS.md y tiempos.log, sin SUBIDA_OK. Además, `VERSION_PROYECTO.txt` vive en la carpeta de trabajo, no en el cache, y en el cache real no existe ninguno.
3. **W2.** `csv_cuadra` da True (proyecto CERRADO) con un RESULTADO.md que dice '1351 CSV / 1351 PDF / 1351 emparejados; 0 faltantes' y además alguna de estas:
   - '12 markups no emparejados en el PDF'
   - '12 huérfanos'
   - '12 sin emparejar'
   - '12 extra markups'
   - '12 duplicados'
   - 'diferencias: 12'
   - '12 not matched'

   `RX_FALTAN_N` es una lista cerrada.
4. **W3.** Una rev nueva que arrancó después de cerrar la anterior (su VERSION_PROYECTO.txt en la subcarpeta de la rev) no reabre el proyecto: solo se lee `<proyecto>/VERSION_PROYECTO.txt`.

**Para cerrarlo:**
- que la publicación misma (el commit 'Publica …') quede bloqueada mientras `revisar_prueba_abiertos` tenga fallas, por ejemplo con un hook pre-commit o con una revisión en `revisar_zip`;
- que un proyecto con canon / TIEMPOS sin SUBIDA_OK cuente como abierto;
- que todo número de "no emparejados" distinto de 0 abra el proyecto.

### NG-3.3 / BE-PM06 — WEAK — STILL-WEAK

**Lo que pedía la verificación 5:** que 'Paso 1', '1. Inventario', '1 Inventario' y 'Step 1' (M1 a M4) exigieran sus corridas --paso.

**Estado en v137:** está arreglado con `paso_de_celda` y tiene test (`test_v121_estructurales`).

**Por qué sigue abierto:** la alarma sigue sin ser "en vivo". Reproducido con adv6_pm06.py:
- Escenario: presupuesto de 180 min (5 hojas A) y 240 min trabajados. Las corridas --paso de los pasos 1, 2-3, 4 y 5 están registradas, y TIEMPOS.md cuadra con tiempos.log.
- Se escribe UNA sola alerta, al final (`alerta_presupuesto` corrido una vez después del paso 5, cuando ya iba en 133 %).
- **N1 (control, log con '| N fin'):** FAIL, que es lo correcto.
- **N2:** el mismo caso con las marcas del log en palabras ('inventario cerrado', 'lecturas A/B cerradas'; es el formato E3 que la verificación 3 ya había señalado) da `alarma_fallas` = [].
- **N3:** con '| 4 terminado' en español también da [].

**Causa:** el plazo de la alerta (`limite`, "a más tardar al cerrar el paso siguiente") sale de `RX_PASO_FIN` sobre el TEXTO del log. Sin '| N fin' no hay plazo (`datetime.max`), y una alerta escrita al final satisface el 50 % y el 100 %. Los pasos cerrados ya salen de TIEMPOS.md (v120), pero el plazo de la alerta no.

**Para cerrarlo:** tomar `limite` de las horas de Fin de `filas_tiempos(TIEMPOS.md)`, con el mismo parser que la exigencia de --paso.

### U-193 — WEAK — STILL-WEAK

**Lo que pedía la verificación 5:** unificar los separadores (V1 a V4) y documentar que la identidad es declarada.

**Estado en v137:** está arreglado.
- Con la lógica real de `ce_cobertura` (adv6_u193): V0 PASS; V1, V2, V3, V4, 'Subagent_A1' / 'AGENT a1', 'sub-agente A1' / 'A1', 'subagente #1' / 'subagente 1' y el ancho completo 'Ａ１' son rechazados.
- La GUÍA exige 'identity … declared' desde FECHA_V121.

**Por qué sigue abierto:** hay una regresión de v126, reproducida con adv6_u193.py.
- **V7:** el revisor R9 corre `markups_bluebeam.py` (etapa 2-7) SIN SUBAGENTE_ID después de v119. Un minuto después, A1 corre la MISMA tool con `--help` y rc 2 (una corrida trivial, fallida, que no rehace nada).
  - `sin_agente_reemplazadas` empareja solo por nombre de tool y hora, no por args, rc ni salida.
  - Resultado: la corrida sin agente queda "reemplazada", el estado baja de FAIL a **AMBER** y R9 se acepta como revisor independiente.
  - Control V7-0: sin la corrida trivial, da FAIL.
- **V4e / V4f, menor:** 'revisor A1' frente a 'A1', y 'A1 (canon)' frente a 'A1', se toman como agentes distintos y se aceptan.

**Para cerrarlo:** "reemplazada" solo si la corrida con agente tiene los mismos args, rc 0 y produjo los mismos archivos de salida (hashes) que la corrida sin agente.

### BE-GK54 — WEAK — STILL-WEAK

**Lo que pedía la verificación 5:** K1 (lista abierta de sinónimos), K2 (disposición sin exclusión en el canon) y K3 (gap_proof realista rechazado).

**Estado en v137:**
- K1 y K2 están arreglados por la versión ESTRUCTURAL (v121): todo par paralelo a <= 14 in exige prueba, sin depender de sinónimos.
- Tiene test (`test_v121_estructurales`).
- adv5_gk54, adv4_gk54 y adv_gk54 no lo rompen.

**Por qué sigue abierto:** la prueba del gap es solo DECLARADA y el programa no la cruza con su propia medida. Reproducido con adv6_gk54.py, con un wall de band 5 in de espesor a 9 pt/ft y una leaf DISPUESTA 'CUBIERTO: same wall as X9-Z9-08, gap 0" (1/Z9.11)':
- `be_gk54_fallas` = [] con la leaf a **4, 13 y 18 in** del centro de la band.
- A 13 y 18 in, el gap real es de 8 a 13 in, y el programa mismo mide esa distancia (`abs(cross - c_mid)`, que imprime en su mensaje).
- Es el error de BE-GK54 (dos leaves con gap contadas como un muro) pasando con una frase.

Además:
- **K3:** 'no gap between leaves (1/Z9.11)' sigue rechazado. Es ruidoso.
- **Q4, informativo:** el caso (b) de v124 / v126 deja sin juzgar una exclusión 'same wall as X' sin gap_proof cuando la leaf está dispuesta como otro material con gap > 0. No cambia cantidades.

**Para cerrarlo:** en el caso (a) MISMO MURO, FAIL si la distancia medida entre la leaf y la cara de la band (descontado medio espesor de cada una) es mayor que una tolerancia de dibujo (por ejemplo 2 in), aunque el gap_proof diga 0.

### v120-RETRO (`proceso_v119` / `inicio_rev_info`) — WEAK — STILL-WEAK

**Lo que pedía la verificación 5:** P1, P1b, P3 y P5.

**Estado en v137:** dan FAIL. Tiene test (`test_v121_estructurales`).

**Por qué sigue abierto:** el arreglo depende de que la línea vieja traiga una etiqueta 'revN' u otro año. Reproducido con adv6_retro.py (log PROPIO de la rev21, VERSION_PROYECTO.txt faltante, por eso hay fallas de proceso). Todos dan **AMBER**, cuando lo correcto es FAIL, y la rev queda exenta de BE-PM05 / BE-PM06:
- **Z2:** una línea de encabezado copiada SIN etiqueta ('10-nov 21:01 PST | arranque proyecto') antes de las marcas del 13-nov. Es el mismo P3 de la verificación 5, solo que sin '(copiado de rev3)'.
- **Z3:** una nota de planeación del día anterior a v119 ('2026-11-11 18:00 | nota: plan de la rev').
- **Z4:** un typo de DÍA ('2026-11-03 09:00 | 1 inicio rev21' en vez de 13). P5 solo cubría el año. El salto de 10 días no supera el tope de 60 días.

Control Z1: con log acumulado y la etiqueta de la rev siguiente en una línea vieja, da FAIL. Es correcto.

**Para cerrarlo:** fechar el arranque con una fuente que el agente no escribe a mano: el timestamp UTC de `VERSION_PROYECTO.txt` (lo escribe `fijar_version_proyecto`) o el primer sello de la bitácora de la rev. Sin esa fuente = FAIL, como pedía la verificación 5 ("la marca de inicio de ESTA rev, VERSION_PROYECTO.txt").

### v120-FALT (CB_FALTANTES_AUDITORIA) — WEAK — STILL-WEAK

**Lo que pedía la verificación 5:** L1, L2 y L2b, más J3 / J3b de DOBLE_CIELO ('lower: GYP-9 MISSING', ref inexistente).

**Estado en v137:** está arreglado.
- Cierre solo con `CERRADO: <ref> (<N/HOJA>)` y cantidad > 0.
- `RX_HOJA_FALTANTE` solo se salta sin palabra de cielo.
- `_seg_cargado` exige que la ref exista con cantidad > 0.
- Tiene tests (`test_v121_be_cr40_cierre_explicito`, `test_v121_excluded_y_brief`).

**Por qué sigue abierto:** la función sigue SALTANDO renglones que son hallazgos de cielo (S1, S2, S3, S6 de BE-CR40: dan N/A). Además, DOBLE_CIELO resuelve un cuarto con refs cargadas que no son del cuarto (S5: 'upper: EXT-Z9-2; lower: EXT-Z9-2').

El test mismo fija como correcto que `CERRADO: EXT-Z9-2 (1/X9.31)` (una línea de muro exterior) cierre 'corridor 216 ceiling missing' (S4). La ref del cierre no tiene que ser un cielo / soffit del cuarto.

**Para cerrarlo:**
- usar las mismas listas abiertas de BE-CR40;
- la ref de `CERRADO:` y de upper / lower tiene que ser un cielo / soffit / misc de cielo cuyo room / ref / source contenga el cuarto del hallazgo (o EXCLUDED con N/HOJA).

## Resumen

**CONFIRMED-CLOSED (9):** U-185, U-189, U-190, BE-CR39, BE-CR42, BE-GK47, NG-3.2 / BE-PM05, BE-PM08 y BE-PM09. Sin cambios respecto a la verificación 5.

**STILL-WEAK (7 renglones = 11 claves abiertas en verificar_version):**
- BE-CR40;
- NG-3.1 / BE-PM04;
- NG-3.3 / BE-PM06;
- U-193 (regresión de v126);
- BE-GK54;
- v120-RETRO;
- v120-FALT.

**Lo que pedía la verificación 5:** los casos que ella reproducía (L1, L2, L2b, J3, J3b, R0, R1b, R2, M1 a M4, V1 a V4, K1, K2, P1, P1b, P3, P5) están TODOS arreglados en v137 y tienen test.

**Lo que mantiene los renglones abiertos:** casos nuevos, en la misma dirección del error original. La mayoría vienen de que se siguen usando listas CERRADAS de palabras o formatos, o de que una declaración no se cruza con lo que el programa ya mide (gap, arranque de la rev). Hay dos excepciones:
- **U-193** se reabrió por una regresión de v126 (`sin_agente_reemplazadas`).
- **NG-3.1** se publicó 6 veces (v131 y v133 a v137) con su propio chequeo en rojo.

**Bloqueo de publicación vigente:** `PRUEBA_ABIERTOS_v81cf137.json` sin grand_kia ni cr_city_hotel_castle_rock.

**Recomendación:** no declarar "0 WEAK". El post-mortem 12b sigue abierto hasta una verificación 7.
