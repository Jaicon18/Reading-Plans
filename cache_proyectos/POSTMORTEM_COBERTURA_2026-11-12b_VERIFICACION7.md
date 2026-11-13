# VERIFICACIÓN INDEPENDIENTE 7 (dirigida): candidato v81cf138 (WIP, congelado en el commit 56d5613)

Fecha: 2026-11-13 01:45 PT

(= 2026-11-13 09:45 UTC.)

La hizo un revisor independiente que no escribió el código. Fue una verificación DIRIGIDA a los 7 renglones que la verificación 6 dejó
abiertos (11 claves en `verificar_version.py`):
- BE-CR40;
- NG-3.1 / BE-PM04;
- NG-3.3 / BE-PM06;
- U-193;
- BE-GK54;
- v120-RETRO;
- v120-FALT.

Además se revisaron, como renglones nuevos, los arreglos de v138 que no venían del post-mortem: BE-XF18, CB_BE_83 con 'faces' numérico,
CB_BE_CF04 sin conteo cero, CE_PROTOCOLO_3H solo con los pasos de la rev actual y los filtros de CE_COBERTURA_DIAG.

No se tocó ninguna tool, ni el cache real (salvo este archivo), ni Drive. No se hizo commit.

## Qué se revisó

- **Candidato:** `skills_archivo/take-off-metal-frame-drywall_v81cf137_lecturas-walls-fechas-reales_2026-11-13.zip` + el parche
  `apartados/v81cf138_wip/v81cf138_desde_v81cf137.patch` (`patch -p1`, sin rechazos).
  - Armado en `/tmp/verif7/take-off-metal-frame-drywall`.
  - Su SKILL.md dice `**VERSION: v81cf138**`; tiene 199 archivos.
  - Para comparar, v137 sin parche en `/tmp/verif7/v137/`.
- **Órdenes candidatas:** `apartados/v81cf138_wip/ordenes/` (verificar_version.py, test_verificar_version.py, REGLAS_REGISTRO.json),
  armadas en `/tmp/verif7/ord/.claude/skills/jc-hunter-ordenes` con `.claude/hooks/` copiado.
- **Lo que el autor dice:** `apartados/v81cf138_wip/LEEME.md`, incluida su lista "Lo que NO cierra".
- **Adversariales de la verificación 6:** `apartados/verif6_adversariales/adv6_*.py`, re-corridos sin cambios (solo la carpeta temporal
  pasa a `/tmp/verif7/tmp`). Salida en `/tmp/verif7/adv6_out/`.
- **Adversariales nuevos (esta verificación):** en `/tmp/verif7/adv/`, fuera del repo, cada uno con su `.out`:
  - adv7_falt.py, adv7_falt_b.py (BE-CR40 / v120-FALT);
  - adv7_pm04.py (NG-3.1);
  - adv7_pm06.py (NG-3.3 y CE_PROTOCOLO_3H);
  - adv7_u193.py;
  - adv7_gk54.py;
  - adv7_retro.py;
  - adv7_xf18.py, adv7_be83.py, adv7_cf04.py, adv7_cobdiag.py (renglones nuevos de v138).

  Todos son sintéticos. Solo adv6_pm04 W4 lee el cache real, en modo lectura. Los que escriben (bitácora, ALERTA_PRESUPUESTO,
  tiempos.log, VERSION_PROYECTO, PDF) escriben solo en `/tmp/verif7/tmp`.

## Corridas

**Pruebas del candidato**
- Suite `correr_suite.py --skill /tmp/verif7/take-off-metal-frame-drywall` (TAKEOFF_SKILL = candidato): **47/47 OK**.
- `test_verificar_version.py` de las órdenes candidatas: **OK** (incluye adv6_pm04).

**verificar_version (órdenes candidatas) sobre el candidato, con skills_archivo y cache_proyectos reales (antes de este archivo)** — sale con 1:
- Reglas acumuladas 976, en el candidato 975, faltan 0.
- POSTMORTEM: 11 WEAK abiertos (los 7 renglones de arriba).
- PRUEBA ABIERTOS - BLOQUEA LA PUBLICACIÓN: falta `skills_archivo/PRUEBA_ABIERTOS_v81cf138.json` (solo existe
  `apartados/v81cf138_wip/PRUEBA_ABIERTOS_v81cf138_XF.json`, con xfinity_interquest solamente). Dice "NO PUBLICAR".

**adversariales de la verificación 6 re-corridos sobre el candidato:** la salida es IGUAL a `apartados/v81cf138_wip/adversariales/after/`.
- adv6_cr40: S0 a S6 dan FAIL (arreglado).
- adv6_pm04: W1, W2 (7 formas) y W3 abren el proyecto; W4 = cr_city_hotel_castle_rock, grand_kia, xfinity_interquest (arreglado).
- adv6_pm06: N2, N3 y N4 dan las fallas del 50 % / 100 % (arreglado).
- adv6_u193: V1 a V4g rechazados y V7 da FAIL (arreglado).
- adv6_retro: Z2, Z3 y Z4 dan FAIL (arreglado).
- adv6_gk54: Q1 da FAIL (arreglado). **Q2, Q3 y Q4 siguen pasando en silencio** (Q2 FAIL? False; Q3 aceptado; Q4 FAIL? False). Confirma lo
  que dice el LEEME.

## Tabla

| id | error / regla | chequeo | test | estado |
|---|---|---|---|---|
| U-185 | Post-mortem de cobertura al cerrar cada proyecto | `verificar_version.revisar_postmortem` | `postmortem_u185` + `adv4_postmortem` + `adv5_v121` | OK — CONFIRMED-CLOSED |
| U-189 | Cielos apilados, detalle cara por cara y COBERTURA | `CB_RCP_APILADOS`, `CB_DETALLE_CARAS`, `cobertura_esperada` | CASOS + `test_v119_postmortem_12b` | OK — CONFIRMED-CLOSED |
| U-190 | REGLA DE ORO #3 doble cielo | `CE_DOBLE_CIELO` + `refs_doble_fallas` | `test_u190_doble_cielo` | OK — CONFIRMED-CLOSED |
| BE-CR39 | rev19 terminado sin el GYP-1 de los corredores | Igual que U-189 / U-190 | `test_v119_postmortem_12b` | OK — CONFIRMED-CLOSED |
| BE-CR40 | Cielo declarado faltante buscando texto | `CB_FALTANTES_AUDITORIA` (`faltantes_auditoria`, `falta_cielo_misma_frase`, `RX_FALTA_V138`, `cuartos_en_linea`, `B.desde_ctx` textos_hallazgos) | `test_v138_faltantes_listas_abiertas` + `test_v138_faltante_misma_frase` + `test_v121_be_cr40_cierre_explicito` | WEAK — STILL-WEAK |
| BE-CR42 | Conflicto plano vs plano sin delta | `conflictos_sin_delta` + `tests_sin_llamar` | `test_be_cr42_…` | OK — CONFIRMED-CLOSED |
| BE-GK47 | '60.0 LF' leído como 'impreso en 0' | CB_BE_HF02 | El mismo test de BE-CR42 | OK — CONFIRMED-CLOSED |
| NG-3.1 / BE-PM04 | Versión nueva no probada sobre los proyectos abiertos | `revisar_prueba_abiertos` + `proyectos_abiertos_cache` + `en_curso_sin_subida` + `csv_cuadra` (DESCUADRE) | `prueba_abiertos_be_pm04` + `adv4_prueba_abiertos` + `adv5_v121` + `adv6_pm04` | WEAK — STILL-WEAK |
| NG-3.2 / BE-PM05 | Versión cambiada a mitad de la compuerta final | `version_proyecto_fallas` | `test_v119_postmortem_12b` | OK — CONFIRMED-CLOSED |
| NG-3.3 / BE-PM06 | Sin alarma de presupuesto mientras se trabaja | `alarma_fallas` + `cierres_pasos` + `tiempos_desde` | `test_v138_alarma_plazo_tiempos` + `test_v121_estructurales` | WEAK — STILL-WEAK |
| U-193 | MAPA DE COBERTURA: revisor distinto del autor | `subagentes_bitacora` + `norm_agente` (ROLES_AGENTE) + `corrida_reemplaza` + `sin_agente_reemplazadas` | `test_v138_reemplazo_corrida_sin_agente` + `test_v121_estructurales` | WEAK — STILL-WEAK |
| BE-PM08 | `COBERTURA - IMAGE ONLY.pdf` tomado por PDF de markups | `nombres_planos` | `test_v119_gk_nombres_y_bitacora` | OK — CONFIRMED-CLOSED |
| BE-PM09 | Bitácora de GK en `takeoff_work/` no se leía | `_bitacoras` | `test_v119_gk_nombres_y_bitacora` | OK — CONFIRMED-CLOSED |
| BE-GK54 | Dos leaves con gap = dos walls | `be_gk54_fallas` + `gap_medido_in` + `gap_prueba_ok` + `otro_material_ok` + `es_mismo_muro` | `test_v138_gk54_gap_medido` + `test_be_gk54` + `test_v121_estructurales` | WEAK — STILL-WEAK |
| v120-RETRO | Retroactivo de proceso (CE_PROTOCOLO_3H `proceso_v119`, log viejo) | `proceso_v119` + `inicio_rev_info` + `inicio_independiente` | `test_v138_retro_fuente_independiente` + `test_v121_estructurales` | WEAK — STILL-WEAK |
| v120-FALT | CB_FALTANTES_AUDITORIA (cualquier ref, hoja faltante, DOBLE_CIELO) | `faltantes_auditoria` + `ref_del_cuarto` + `_seg_cargado(cuartos)` + `cuartos_doble_cielo` | `test_v138_faltantes_listas_abiertas` + `test_v121_be_cr40_cierre_explicito` + `test_v121_excluded_y_brief` | WEAK — STILL-WEAK |
| BE-XF18 | PDF de markups elegido por orden alfabético (mapa IMAGE ONLY leído) | `elegir_pdf_markups` + `CE_PDF_MARKUPS_ELEGIDO` | `test_be_xf18_pdf_markups_por_nombre` | WEAK — STILL-WEAK |
| v138-BE83 | CB_BE_83 con 'faces' numérico (existing_walls de CR) | `runner/completitud.caras_sobre_ceiling` | `test_v138_be83_faces_numero` | WEAK — STILL-WEAK |
| v138-CF04 | CB_BE_CF04 PASS sin conteo cero (red U-138) | `chequeos_biblioteca.be_cf04` + `auditar_compuerta` | `test_v138_cf04_wood_board_only_plausible` | WEAK — STILL-WEAK |
| v138-3H | CE_PROTOCOLO_3H solo con los pasos de la rev actual | `proceso_v119` + `tiempos_desde` + `alarma_fallas(desde=)` | `test_v138_protocolo_rev_posterior_solo_sus_pasos` | WEAK — STILL-WEAK |
| v138-COBDIAG | CE_COBERTURA_DIAG: filtros de falsos (tag, discontinuo, hatch) | `cob_diag_cortos` + `_cob_divisor_tag` + `_cob_discontinua` + `_cob_en_hatch` | `test_v138_cob_diag_familias_cr` | WEAK — STILL-WEAK |

## Detalle por renglón

### U-185, U-189, U-190, BE-CR39, BE-CR42, BE-GK47, NG-3.2 / BE-PM05, BE-PM08 y BE-PM09 — OK — CONFIRMED-CLOSED

Ya estaban cerrados en las verificaciones 5 y 6, y no se re-abren. La suite del candidato pasa 47/47 y sus tests siguen en ella.
`revisar_postmortem` corre limpio sobre el cache real, salvo por los abiertos.

### BE-CR40 — WEAK — STILL-WEAK

**Lo que pedía la verificación 6:** S1, S2, S3 y S6 (listas abiertas de "falta" y de "cielo", cuartos alfanuméricos y archivos de
COORDINACIÓN / REVIEW / BITACORA…).

**Estado en v138:** adv6_cr40 S1 a S6 dan FAIL. Tiene test (`test_v138_faltantes_listas_abiertas`, `test_v138_faltante_misma_frase`).

**Por qué sigue abierto:** se reprodujeron casos en la misma dirección del error (un cielo CARGADO declarado faltante, y el chequeo da
N/A = PASS). Canon con el corridor 901 cargado en `ceilings[0]`.

1. **REGRESIÓN de v138 (adv7_falt A1 a A7, adv7_falt_b).** `falta_cielo_misma_frase` corta el renglón por `[.;|]\s+` y por tabulador, y
   exige el faltante y el cielo en el MISMO pedazo. En una tabla de auditoría con columna de estado, el faltante y el cielo quedan en
   celdas distintas, y el renglón se salta. Todos estos dan **PASS 'N/A: sin hallazgos'**:
   - `| 1 | corridor 901 ceiling | MISSING | OPEN |`
   - `| 1 | Corridor 901 ceiling | NOT LOADED |` (tabla con encabezado Item / Status)
   - `| 1 | Room 901 | ceiling | missing |`
   - `| 1 | 901 | Corridor | CLG | FALTA |`
   - `corridor 901 ceiling; status: missing`
   - `1<TAB>corridor 901 ceiling<TAB>MISSING`
   - `- Corridor 901 ceiling. Not loaded in the take-off.`

   **Con v137, los tres primeros daban FAIL.** El arreglo del falso positivo de XF (faltante y cielo en celdas distintas, de una fila
   del Scope) abrió un hueco silencioso para el formato más común de los informes: la tabla con la columna Status.
2. **El descubrimiento de archivos no ve lo que el test dice (adv7_falt C, adv7_falt_b).** Se corrió `CE.Ctx(w)` y luego `B.desde_ctx`
   sobre una carpeta real.
   - `_rglob_seguro(w, "**/COORDINACION/**/*.md")` NO encuentra `COORDINACION/hallazgos.md`: el `fnmatch` de `COORDINACION/**/*.md`
     exige una subcarpeta. Pasa lo mismo con `Auditoria/hallazgos.csv` y `Auditoria/notas.md`, desde v119.
   - El glob distingue mayúsculas: `review_rev9.md`, `Review_rev9.md`, `hallazgos_rev9.md`, `Coordinacion/…`, `COORDINACIÓN/…` (con acento)
     y `COORDINACION/hallazgos_rev9.xlsx.txt` no se leen.
   - Todos esos casos dan **PASS** con el 901 cargado declarado faltante. Solo `REVIEW_rev9.md` e `INFORME_COORDINACION_rev9.md` (que
     ya leía v137) dan FAIL.
   - El test del autor inyecta `textos_hallazgos={"COORDINACION/notas.md": …}` directo en `B(...)`: nunca pasa por el glob.
   - `solo_rev_actual`: con el workdir sin rev en el nombre, un `RESUMEN_rev10_plan.md` deja fuera el `REVIEW_rev9.md` con el hallazgo
     (PASS).
3. **Otras formas de "falta" (adv7_falt B).** Dan PASS:
   - "isn't loaded";
   - "wasn't counted";
   - "never added to the take-off";
   - "not in the take off" (con espacio);
   - "forgotten";
   - "se olvidó el cielo";
   - "needs to be added";
   - "pendiente de cargar";
   - "no hay cielo en el corredor 901";
   - "ceiling: 0 SF in the Excel";
   - "TBD, not in TO".

   Sigue siendo una lista cerrada, más larga.

**Para cerrarlo:**
- juzgar la FILA completa de una tabla (o el renglón completo cuando no hay un tag ni una altura de cielo); el caso XF ('above ceiling'
  es altura) se resuelve quitando la frase de altura, no partiendo la fila;
- el glob de las carpetas tiene que incluir a los hijos directos (`COORDINACION/*.md`, `Auditoria/*.csv`) y no distinguir mayúsculas ni
  acentos;
- un test que arme la carpeta en disco y pase por `Ctx` + `B.desde_ctx`;
- negación abierta: `n't`, never, forgot / olvid, pendiente, 'no hay', 0 SF.

### NG-3.1 / BE-PM04 — WEAK — STILL-WEAK

**Lo que pedía la verificación 6:** candado en la publicación; W1 (proyecto en curso sin SUBIDA_OK); W2 (todo "no emparejados" > 0);
W3 (rev nueva en una subcarpeta).

**Estado en v138:**
- W1, W2 y W3 están arreglados (adv6_pm04), con test (`adv6_pm04` en test_verificar_version).
- `main` sale con 1 y dice "NO PUBLICAR".

**Por qué sigue abierto:**
1. **Sigue sin candado.** El mismo LEEME lo dice. adv7_pm04 X3: `.claude/settings.json` solo tiene los hooks SessionStart y
   UserPromptSubmit, y no hay `.git/hooks/pre-commit`. Hoy se puede hacer el commit 'Publica v81cf138' con `PRUEBA_ABIERTOS_v81cf138.json`
   faltante, que es exactamente lo que pasó 6 veces (v131 y v133 a v137).
2. **`csv_cuadra` sigue siendo una lista cerrada (adv7_pm04 X1).** Con '1351 CSV / 1351 PDF / 1351 emparejados; 0 faltantes' más
   cualquiera de estas, da `cuadra: True` y el proyecto CERRADO:
   - '12 markups unpaired' / 'unpaired: 12';
   - '12 sin par';
   - '12 no encontrados en el CSV';
   - '12 left over in the PDF';
   - 'el PDF tiene 12 markups más que el CSV' / 'PDF has 12 more markups…';
   - '12 sin coincidencia';
   - 'Markups en el PDF (total real): 1363';
   - '12 not paired';
   - '12 markups solo en el PDF' / '12 only in PDF';
   - '12 no aparecen en el CSV'.
3. **Una rev en curso no reabre el proyecto (adv7_pm04 X2).** Es un proyecto cerrado (subida rev20 + CSV rev20 N/N) con una rev21 EN CURSO
   en una subcarpeta: canon, TIEMPOS.md y tiempos.log del 13-nov, sin VERSION_PROYECTO.txt (que vive en el workdir).
   `proyectos_abiertos_cache` = [], porque solo `_versiones_proyecto` mueve la fecha de corte; `en_curso_sin_subida` solo aplica sin
   ninguna SUBIDA_OK.

**Para cerrarlo:**
- un hook (pre-commit, o PreToolUse sobre `git commit` con 'Publica') que corra `verificar_version` y aborte con salida 1;
- cerrar el proyecto solo con una forma POSITIVA ('0 sin pareja en cada lado' y los totales del PDF y del CSV iguales), no buscando
  palabras de descuadre;
- canon / TIEMPOS / tiempos.log de una subcarpeta con fecha posterior a la última subida = abierto.

### NG-3.3 / BE-PM06 — WEAK — STILL-WEAK

**Lo que pedía la verificación 6:** que el plazo de la alerta salga de TIEMPOS.md y no del texto '| N fin' del log (N2, N3).

**Estado en v138:** está arreglado con `cierres_pasos`. adv6_pm06 N2, N3 y N4 dan las fallas del 50 % / 100 %. Tiene test
(`test_v138_alarma_plazo_tiempos`).

**Por qué sigue abierto:** v138 agregó `alarma_fallas(..., desde=ini)`, y `ini` es la marca de arranque ESCRITA A MANO en tiempos.log
(`inicio_rev_info`). Todo lo que cerró antes de esa marca queda fuera de la alarma y de la exigencia de `--paso`.

Reproducido con adv7_pm06:
- **P1:** rev21 completa del 13-nov, después de v119. VERSION_PROYECTO.txt fijado a las 08:00 PT. TIEMPOS.md cierra el paso 1 a las 08:30
  y el 2-3 a las 09:30, sin corridas --paso y sin marcas en el log. tiempos.log arranca recién a las 10:00 ('inicio rev21').
  - `proceso_v119` = **PASS**, con '2 paso(s) … son de una rev anterior'.
  - El control P0 (mismo caso con el log completo) da FAIL por los pasos 1 y 2-3 y por la alerta del 50 %.
- **P2:** igual, con un log acumulado del proyecto: marcas de la rev21 de 08:00 a 09:30 sin etiqueta, y la etiqueta 'inicio rev21' a las
  10:00. Da **PASS**.

En los dos casos la fuente independiente (VERSION_PROYECTO.txt, 08:00 PT de la rev21) contradice el arranque, y el programa no la mira en
esa rama. Ver también v138-3H.

**Para cerrarlo:** el `desde` de la rev actual sale del MÍNIMO entre la marca del log y `inicio_independiente` (VERSION_PROYECTO.txt de
ESA rev / bitácora / git), y una fila de TIEMPOS.md solo es "de una rev anterior" si además cierra antes del sello de VERSION_PROYECTO.txt
de esta rev.

### U-193 — WEAK — STILL-WEAK

**Lo que pedía la verificación 6:** la regresión V7 (corrida trivial que "reemplaza") y, menor, V4e / V4f.

**Estado en v138:**
- `corrida_reemplaza` exige rc 0, los mismos args, los mismos hashes y nada de --help / --dry-run. V7 da FAIL.
- adv7_u193 Y2 (rehecha de verdad = AMBER), Y3 (hashes distintos = FAIL) e Y4 (--dry-run = FAIL) están bien.
- `norm_agente` quita la palabra de rol DELANTE y los paréntesis, así que V4e y V4f quedan rechazados.
- Tiene test (`test_v138_reemplazo_corrida_sin_agente`).

**Por qué sigue abierto:** el mismo caso de V4e con la palabra de rol DETRÁS (adv7_u193 Y1). El autor del canon es 'A1' y el revisor
declarado es cualquiera de estos; todos se aceptan como revisor distinto (PASS):
- 'A1 revisor'
- 'A1-reviewer'
- 'A1_rev'
- 'agente A1 revisor'
- 'A1 bis'
- 'A01'

`norm_agente` solo quita el rol de la cabeza (`while toks[0] in ROLES_AGENTE`).

Menor: `corrida_reemplaza` pide "log no vacío", pero `log` es la RUTA del log, que nunca está vacía.

**Para cerrarlo:**
- quitar las palabras de rol en cualquier posición y los ceros a la izquierda, o comparar con "el id del autor contenido en el id del
  revisor";
- leer el tamaño del archivo de log, no la ruta.

### BE-GK54 — WEAK — STILL-WEAK

**Lo que pedía la verificación 6:** cruzar 'gap 0' con la distancia medida (Q1).

**Estado en v138:**
- Arreglado con `gap_medido_in` y `GK54_TOL_DIBUJO_IN` = 2 in. adv6_gk54 Q1 da FAIL.
- adv7_gk54 G1: a 13 in, todas las variantes de la prueba ('gap 0', 'no gap', 'flush', 'touching', 'abutting', 'gap 1/2"', 'gap: none',
  'sin gap', 'gap = 0 in') dan FAIL.
- Tiene test (`test_v138_gk54_gap_medido`).

**Por qué sigue abierto:** confirmado con adversarial lo que el LEEME dice que NO cierra. Los tres pasan en silencio:
- **Q2 (adv6_gk54 Q2, adv7_gk54 G5 / G6):** una hoja a 1/4" sin escala en `escalas` (o sin el argumento `escalas`) usa 9 pt/ft. Una leaf a
  10 in (15 pt) queda fuera de la ventana: `be_gk54_fallas` = [], FAIL? False. El control Q2-0, con `{'Z9.11': 18}`, da FAIL.
- **Q3 (adv6_gk54 Q3, adv7_gk54 G4):** 'NO ES NUESTRO: existing, gap 4 in (1/Z9.11)' se acepta como "otro material" con una leaf de metal
  dibujada a 4 in del centro (gap real ~1.5 in). `otro_material_ok` acepta 'existing' como material.
- **Q4 (adv6_gk54 Q4, adv7_gk54 G7):** una exclusión del canon 'same wall as X9-Z9-08' SIN gap_proof, con la leaf dispuesta como caso
  (b) 'CMU, gap 4 in'. Da FAIL? False: la exclusión 'same wall' nunca se juzga (v126 juzga la disposición sola).

Además:
- **G2, menor:** la leaf toma `espesor_in` de la fila del mapa CSV, que es editable. Con `espesor_in=20`, la leaf a 13 in con 'gap 0"'
  pasa.
- **K3:** 'no gap between leaves' sigue rechazado. Es ruidoso, no silencioso.

**Para cerrarlo:**
- hoja sin escala en `escalas` = FAIL (no 9 por omisión);
- 'existing' no es un material impreso distinto: exige el material leído en la hoja y que la leaf no sea metal del canon;
- toda exclusión 'same wall' sin gap_proof = FAIL, aunque la leaf esté dispuesta por otro camino;
- `espesor_in` medido de nuevo, no leído del CSV.

### v120-RETRO (`proceso_v119` / `inicio_independiente`) — WEAK — STILL-WEAK

**Lo que pedía la verificación 6:** fechar el arranque con una fuente que el agente no escribe a mano (Z2, Z3 y Z4).

**Estado en v138:**
- Arreglado con `inicio_independiente` y `TOL_INICIO_REV_H` = 24 h. adv6_retro Z2, Z3 y Z4 dan FAIL.
- adv7_retro R0 (Z2 sin fuente) da FAIL.
- Tiene test (`test_v138_retro_fuente_independiente`).

**Por qué sigue abierto:** la "fuente independiente" se puede COPIAR de la rev anterior, que es lo normal al copiar la carpeta de trabajo.
Reproducido con adv7_retro: carpeta rev21 del 13-nov con el encabezado copiado '05-nov 11:26 PST | arranque proyecto' (el mismo Z2). Todos
dan **AMBER** ("confirmado por …"), cuando lo correcto es FAIL:
- **R1:** VERSION_PROYECTO.txt copiado de la rev20, con un solo renglón '2026-11-05T19:30:00+00:00 | rev20 | v81cf110'.
  `inicio_independiente` filtra los renglones de la rev (`propias`), y si no hay ninguno usa TODOS (`or vp`): toma el renglón de la rev20.
- **R1b:** igual, con el Excel `Z9_Takeoff_rev21.xlsx` (la etiqueta de la rev es 21 y aun así se usa el renglón rev20).
- **R2:** sin VERSION_PROYECTO.txt, con `bitacora.jsonl` copiada de la rev20 (primer ts 05-nov).

Así la rev21 queda exenta de BE-PM05 (le falta su propio renglón de VERSION_PROYECTO) y de BE-PM06.

**Para cerrarlo:** solo vale el renglón de VERSION_PROYECTO.txt con la etiqueta de ESTA rev (sin el `or vp`), y la bitácora solo vale si
su primer renglón es de una tool que corrió sobre los archivos de esta rev (o la mtime / el git de la carpeta de la rev). Una fuente de
otra rev = FAIL.

### v120-FALT (CB_FALTANTES_AUDITORIA) — WEAK — STILL-WEAK

**Lo que pedía la verificación 6:** S4 y S5 (que `CERRADO:` y upper / lower de DOBLE_CIELO sean una ref DEL cuarto y de cielo).

**Estado en v138:**
- Arreglado con `ref_del_cuarto`. adv6_cr40 S4 y S5 dan FAIL.
- Tiene test (`test_v138_faltantes_listas_abiertas`).

**Por qué sigue abierto:** `ref_del_cuarto` acepta CUALQUIER item que no sea muro (misc_items / trim_items / blocking_items) cuyo
room / location nombre el cuarto. No exige que sea un cielo / soffit / misc de cielo, que es lo que pedía la verificación 6.

Reproducido con adv7_falt D / E. El corridor 216 de verdad NO tiene cielo en el canon:
- **D1:** `corridor 216 ceiling missing | CERRADO: BLK-216 (1/X9.31)`, donde BLK-216 es un misc de blocking del corridor 216. Da
  **PASS** ('1 hallazgo(s) … verificados').
- **D2:** `CERRADO: CB-216 (1/X9.31)`, con CB-216 un corner bead (trim_items) del 216. Da **PASS**.
- **E1:** DOBLE_CIELO 'upper: BLK-901; lower: BLK-901' resuelve el cuarto 901 con su blocking. Da **PASS**.

A esto se suma la regresión A1 a A7 de BE-CR40 (misma función).

**Para cerrarlo:** en `ref_del_cuarto`, cuando hay cuartos, exigir también lista `ceilings` / `framed_soffits` o un misc con ref CLG- /
SOF- / descripción de cielo; nunca trim_items ni blocking_items.

### BE-XF18 (`elegir_pdf_markups` / CE_PDF_MARKUPS_ELEGIDO) — WEAK — STILL-WEAK

**Estado en v138:**
- Elige por nombre. El mapa 'IMAGE ONLY' / COBERTURA nunca se toma.
- Dos 'OPEN IN BLUEBEAM' = FAIL.
- adv7_xf18 X0 está bien. X4 y X5 (mapas con otro nombre y dos candidatos) dan FAIL, que es ruidoso y correcto.

**Por qué no cierra (adv7_xf18):**
- **X3:** en Planos marcados/ hay un 'CR_markups_rev20b - OPEN IN BLUEBEAM.pdf' viejo y el 'CR_markups_rev20c.pdf' actual sin sufijo. Se
  elige el de la rev20b y el chequeo da **PASS** 'PDF de markups leído'. La rev del nombre no se cruza con la del Excel / la entrega.
- **X1:** `entrega.json 'markups'` apunta a un archivo que NO existe. Da **PASS** 'PDF de markups leído' (el docstring dice "si existe";
  el código no lo comprueba).
- **X2:** `entrega.json 'markups'` apunta al PDF de la rev anterior. Da PASS.

**Para cerrarlo:**
- el archivo elegido tiene que existir;
- su etiqueta revN tiene que ser la de `_etiqueta_rev` (Excel / entrega);
- con annots > 0.

### v138-BE83 (CB_BE_83 con 'faces' numérico) — WEAK — STILL-WEAK

**Estado en v138:** ya no revienta con `faces` = número. Un muro interior a 11 ft en un cuarto con cielo a 9 ft, sin fuente, sale
(adv7_be83 F0). Tiene test (`test_v138_be83_faces_numero`).

**Por qué no cierra (adv7_be83).** Muro de 11 ft con cielo de 9 ft en el 905, sin justificación real. Estos casos dan `caras_sobre_ceiling`
= [], cuando la cara debería salir:
- **F1:** muro exterior con cara INTERIOR al cuarto: `location: 'L9 | faces: exterior; 905 GUEST'` (el formato de CR). El regex
  `faces?:\s*(?:exterior|outside)` salta el MURO ENTERO, no solo la cara exterior.
- **F2:** board '5/8 Type X (905 side) + 1/2 exterior gyp sheathing'. Igual: se salta todo el muro.
- **F3:** fuente 'GWB to extend to underside of ceiling (6/Z9.21)'. La fuente dice que la cara PARA en el cielo, pero
  `extends?\s+to\s+(?:the\s+)?(?:underside…)` la toma como justificación para subir.
- **F4 / F5:** una mención incidental ('see stair enclosure note…', 'top track anchored to structure') también justifica.
- **F6, menor:** el cuarto solo se busca en `location`.

**Para cerrarlo:**
- con faces numérico y una cara exterior, la cara INTERIOR (el cuarto del location) se sigue comparando;
- 'underside of ceiling' no es justificación;
- las justificaciones nuevas exigen el verbo de altura del muro ('partition extends to …', 'full height to …') y su N/HOJA.

### v138-CF04 (CB_BE_CF04 sin conteo cero) — WEAK — STILL-WEAK

**Estado en v138:** el PASS dice 'ningún wall de madera con framing en walls[]' en vez de '0 walls …', y la red U-138
(`auditar_compuerta`) ya no lo vuelve FAIL en un set wood-framed correcto. Tiene test (`test_v138_cf04_wood_board_only_plausible`).

**Por qué no cierra (adv7_cf04).** La afirmación 'ningún wall de madera con framing' depende del regex `\bwood\b|\b2x\d` sobre
stud_size / gauge. Con un muro de madera con framing en walls[], estos casos dan **PASS** y siguen en PASS después de U-138:
- stud_size '2 X 6' / gauge 'DF-L #2';
- '2×6' (signo ×) / 'SPF';
- '5-1/2" DF stud' / 'lumber';
- '6" timber stud'.

Con v137 los mismos daban FAIL, aunque solo de rebote por la red U-138 (que también tumbaba el caso correcto de CR). v138 quitó el
falso, y con él la única red que tapaba este hueco.

**Para cerrarlo:** detectar madera con una lista abierta (2 x N, ×, DF, SPF, HF, lumber, timber, stud de madera sin calibre) o, al revés,
exigir que todo muro de walls[] tenga un calibre de metal (ga / mil / CFS).

### v138-3H (CE_PROTOCOLO_3H solo pasos de la rev actual) — WEAK — STILL-WEAK

**Estado en v138:**
- `tiempos_desde` y `alarma_fallas(desde=)` dejan fuera los pasos de la rev original de CR (5-6 nov).
- Un paso de la rev actual sin --paso sigue dando FAIL cuando su Fin es posterior a la marca 'inicio revN'.
- Tiene test (`test_v138_protocolo_rev_posterior_solo_sus_pasos`).

**Por qué no cierra:** es el mismo caso P1 / P2 de NG-3.3. "Rev anterior" se decide por la marca de arranque escrita a mano, sin cruzarla
con `inicio_independiente`. Los pasos 1 y 2-3 de la MISMA rev21 (13-nov 08:00-09:30, después de v119, VERSION_PROYECTO.txt rev21
fijado 08:00 PT) quedan exentos si la marca 'inicio rev21' se escribe a las 10:00. Da **PASS**, sin --paso y sin la alerta del 50 %.

**Para cerrarlo:** lo mismo que en NG-3.3 (el `desde` = el mínimo con la fuente independiente de ESTA rev). Además, toda fila exenta tiene
que tener su Fin antes del sello de VERSION_PROYECTO.txt de la rev actual.

### v138-COBDIAG (filtros de CE_COBERTURA_DIAG) — WEAK — STILL-WEAK

**Estado en v138:**
- Arreglado: el stub real sale.
- El furring contra CMU, con el hatch de UN lado, sale (control del autor, adv7_cobdiag K1).
- El tag, el discontinuo y el hatch de los dos lados se filtran.
- Tiene test (`test_v138_cob_diag_familias_cr`).

**Por qué no cierra (adv7_cobdiag, PDF sintético a 18 pt/ft, mismo dibujo que el test del autor).** Furrings REALES no cubiertos que v137
reportaba y v138 se traga (`cob_diag_cortos` ya no los devuelve):
- **K2:** furring contra un CMU con cross-hatch Y piso de loseta a 45 grados del lado del cuarto. Es el caso típico de un baño. El hatch
  queda "a los dos lados" y `_cob_en_hatch` lo filtra. Es justo el riesgo que el LEEME anota como pendiente ("un furring real pegado a un
  CMU con cross-hatch").
- **K3:** el furring con su propio tag 'F1' escrito al lado (a 0.17 ft, dentro de su largo). `_cob_divisor_tag` lo toma por el marco de
  la caja de un tag.
- **K4:** el furring con su cota corta '3'-0"' al lado. Igual.

Con v137 los tres salían: `salen (x): [304, 504, 704, 904, 1104]` en v137, y `[304, 504]` en v138.

**Para cerrarlo:**
- `_cob_divisor_tag` solo con un MARCO cerrado alrededor de la palabra (las 4 líneas del rectángulo del tag), no con cualquier palabra
  pegada;
- `_cob_en_hatch` de los dos lados solo si el hatch es del MISMO patrón y estilo a los dos lados (la loseta del cuarto no es el CMU);
- medición de CR sobre rev20c (15 / 15 FALTA), que el LEEME deja pendiente.

## Resumen

**CONFIRMED-CLOSED (9):** U-185, U-189, U-190, BE-CR39, BE-CR42, BE-GK47, NG-3.2 / BE-PM05, BE-PM08 y BE-PM09. Sin cambios.

**STILL-WEAK (7 renglones del post-mortem = 11 claves):**
- BE-CR40;
- NG-3.1 / BE-PM04;
- NG-3.3 / BE-PM06;
- U-193;
- BE-GK54;
- v120-RETRO;
- v120-FALT.

**Renglones nuevos de v138, WEAK (5):** BE-XF18, v138-BE83, v138-CF04, v138-3H y v138-COBDIAG.

**Lo que pedía la verificación 6:** los casos que ella reproducía (S1 a S6, W1 a W3, N2 / N3, V7, V4e / V4f, Q1, Z2 a Z4) están TODOS
arreglados en v138 y tienen test. adv6_* da exactamente la salida 'after' del autor.

**Lo que mantiene los renglones abiertos:** casos nuevos en la misma dirección del error original, más los tres de BE-GK54 que el propio
autor declara (Q2, Q3, Q4).

**Lo más grave (pasa en silencio):**
1. **Regresión de v138 en CB_FALTANTES_AUDITORIA.** Una tabla '| corridor 901 ceiling | MISSING |' (faltante y cielo en celdas
   distintas) daba FAIL en v137 y da PASS N/A en v138 (`falta_cielo_misma_frase`).
2. **`COORDINACION/*.md` (hijos directos) no se lee nunca.** Tampoco `Auditoria/*.csv` / `Auditoria/*.md`, ni los nombres en minúsculas.
   El test lo tapa inyectando `textos_hallazgos`.
3. **CE_PROTOCOLO_3H / BE-PM06.** Los pasos de la rev ACTUAL quedan exentos como "de una rev anterior" si la marca 'inicio revN' del log se
   escribe tarde, aunque VERSION_PROYECTO.txt de esa rev diga otra cosa.
4. **CE_COBERTURA_DIAG.** Furrings reales con loseta del lado del cuarto, o con su tag / cota al lado, ya no salen.

**Bloqueo de publicación vigente:**
- no existe `skills_archivo/PRUEBA_ABIERTOS_v81cf138.json` (solo el `_XF` del WIP, sin grand_kia ni cr_city_hotel_castle_rock);
- `verificar_version` dice NO PUBLICAR y sale con 1;
- sigue sin haber un candado automático en el commit.

**Recomendación:** no publicar v81cf138 como está, y no declarar "0 WEAK". Primero hay que arreglar al menos la regresión (1) y el glob
(2), que hacen al candidato PEOR que v137 en BE-CR40. El post-mortem 12b sigue abierto hasta una verificación 8.

## verificar_version después de escribir este archivo

`python3 -I …/jc-hunter-ordenes/verificar_version.py /tmp/verif7/take-off-metal-frame-drywall skills_archivo cache_proyectos` (órdenes
candidatas, solo lectura), salida 1:
- **POSTMORTEM (U-185):** 16 WEAK / 0 MISSING / 0 NO GUARD abiertos (16 claves):
  - las 11 de antes;
  - más BE-XF18, v138-BE83, v138-CF04, v138-3H y v138-COBDIAG.
  - El archivo se leyó con su 'Fecha:' y la columna 'estado'.
- **PRUEBA ABIERTOS - BLOQUEA LA PUBLICACIÓN:** falta `skills_archivo/PRUEBA_ABIERTOS_v81cf138.json`. Dice "NO PUBLICAR".
