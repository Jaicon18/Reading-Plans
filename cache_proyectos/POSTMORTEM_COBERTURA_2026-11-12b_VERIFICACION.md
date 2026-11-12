# VERIFICACIÓN INDEPENDIENTE del cierre v81cf119: POSTMORTEM_COBERTURA_2026-11-12b

2026-11-12 12:15 PT. Lo hizo un revisor independiente que no escribió el código. Se verificó leyendo el código y corriéndolo.

## Qué se revisó

- Base: el skill v118 (`skills_archivo/take-off-metal-frame-drywall_v81cf118_U191-excluded-cero_2026-11-12.zip`).
- Encima de v118 se aplicó `apartados/v81cf119_desde_v81cf118.patch`, del commit 23be32f.
  - Se aplica con `-p1` desde la carpeta que contiene `take-off-metal-frame-drywall/`.
  - Con el patch aplicado quedan 199 archivos y la línea `VERSION: v81cf119`.
- `apartados/ordenes_v119/verificar_version.py` y `test_verificar_version.py` se copiaron a una copia de `.claude/`. Así se pudieron correr.

## Resultados de las corridas

- **Suite completa**: `correr_suite.py --skill <v119>` = **47/47 OK**.
- **Selftest de verificar_version v119**: 12/12 OK, incluidos `postmortem_u185` y `tests_llamados`.
- **verificar_version v119 sobre el candidato**: faltan 0 reglas.
  - Con el `POSTMORTEM_COBERTURA_2026-11-12b.md` actual: rc 1 = FALLA U-185, por 7 WEAK. Es lo esperado.
  - Con el CIERRE propuesto en lugar del 12b: rc 0.

## Aviso: este archivo es el post-mortem más nuevo

Este archivo cumple `RX_POSTMORTEM`, porque el nombre `2026-11-12b_VERIFICACION` va después de `2026-11-12b`. Con v119, entonces, **este archivo es el post-mortem más nuevo y decide U-185**.

- Los renglones `OK — CONFIRMED-CLOSED` cuentan como cerrados.
- Los renglones `WEAK — STILL-WEAK` cuentan como abiertos.

Así, verificar_version v119 va a FALLAR hasta que los STILL-WEAK se cierren. Es intencional: así ningún archivo más viejo tapa lo que sigue abierto.

Con la verificar_version v118 que está en uso hoy, esto no cambia nada: el post-mortem limpio de 2026-11-12 sigue haciendo pasar la verificación.

## Tabla

| id | error / regla | chequeo | test | estado |
|---|---|---|---|---|
| U-185 | Post-mortem de cobertura al cerrar cada proyecto | `verificar_version.revisar_postmortem` (v119) | `test_verificar_version::postmortem_u185` (sí se llama) | WEAK — STILL-WEAK (residual). Lo que se arregló sí está cerrado y probado: (a) el cierre se toma de `fecha_iso` de todos los `SUBIDA_OK*.json`; (b) se compara con hora completa; (c) solo cuenta el post-mortem más nuevo. Huecos que siguen: (1) **pasa en vacío**: un post-mortem más nuevo SIN tabla devuelve `abiertos=[]` y la verificación pasa (reproducido: un archivo `..._12b_X.md` sin tabla da `[]` aunque el 12b tenga 7 WEAK); (2) cualquier archivo `POSTMORTEM_COBERTURA_<fecha>*.md` se vuelve "el más nuevo", aunque sea una verificación o una copia; (3) la tabla de la sección 3 tiene encabezado `#`, no `id`, y **nunca se evalúa**: el CIERRE pasa aunque sus 3 renglones sigan diciendo `**NO GUARD**`. Arreglo propuesto: exigir que haya tabla (0 renglones = falla) y evaluar también la tabla de causas. |
| U-189 | Cielos apilados, detalle cara por cara y COBERTURA | `CB_RCP_APILADOS` (`dobles_declarados` + `refs_doble_fallas`), `CB_DETALLE_CARAS` (ref exacta), `cobertura_esperada` (burbujas de letra) | `test_v119_postmortem_12b` + CASOS `rcp_apilados` / `detalle_caras` | OK — CONFIRMED-CLOSED. Los cuartos 'double' de DOBLE_CIELO se evalúan contra el canon. Si hay 'double' declarados y 0 evaluados, FALLA. 'loaded' se valida como ref exacta: el test hace que "SOF-Z9-01 side" falle. Se reconocen burbujas de letra (D/X9.31). Notas: (i) `refs_doble_fallas` devuelve `[]` si el canon no trae ningún cielo ni misc, y en ese caso los 'double' cuentan como evaluados (borde en vacío); (ii) un Row en texto libre o con una sola parte pasa CB_RCP_APILADOS, pero lo para CE_DOBLE_CIELO (`doble_cielo_fallas` exige `upper:` y `lower:`). |
| U-190 | REGLA DE ORO #3 doble cielo | `CE_DOBLE_CIELO` + `refs_doble_fallas` | `test_v119_postmortem_12b` (renglón inventado, el mismo arriba y abajo, cantidad 0) + `test_u190_doble_cielo` | OK — CONFIRMED-CLOSED. Nota: un `EXCLUDED` pasa con la columna N/SHEET de la propia fila, que siempre viene llena. No se exige que el motivo tenga su propia N/HOJA. |
| BE-CR39 | rev19 dado por terminado sin el GYP-1 de los corredores, etc. | Igual que U-189 / U-190 | `test_v119_postmortem_12b` (sintético, cuarto Z9 901 con FS + GYP) | OK — CONFIRMED-CLOSED, en código y con el caso sintético. Falta hacerlo con datos reales: el LEEME dice que sobre el DOBLE_CIELO real de CR rev20a quedan 2 renglones sin resolver (`CLG-L2-217F`, `CLG-L3-317F`). Hay que confirmarlos con el canon de rev20a. CR no pasó por prueba_abiertos. |
| BE-CR40 | Un cielo declarado faltante buscando texto en el JSON | `CB_FALTANTES_AUDITORIA` (`faltantes_auditoria` → `faltante_por_tag`) + CLI `chequeos_biblioteca.py faltante` | CASOS `faltantes_auditoria` (el caso malo da FAIL y el bueno PASS; está en el loop CASOS) | WEAK — STILL-WEAK. (1) **Se puede pasar con una auto-declaración**: si el renglón trae la cadena `faltante_por_tag:` no se verifica nada. Reproducido: "X9.01 GYP-9 8'-11\" missing … faltante_por_tag: CARGADO" da PASS, que es justo el error BE-CR40. (2) Un hallazgo sin tag con forma GYP/FS/RS…, por ejemplo "corridor 901 ceiling missing", da N/A. (3) Solo se leen archivos con AUDITORIA, INFORME o revision_independiente en el nombre. Arreglo propuesto: aceptar solo `faltante_por_tag: FALTA`, y FALLAR si la salida dice CARGADO. |
| BE-CR42 | Conflicto plano vs plano sin delta | `plantilla_excel.conflictos_sin_delta` + CB_U_082 | `test_be_cr42_conflicto_con_delta_y_gk47()` ya se llama (línea 995) + `verificar_version.tests_sin_llamar` (probado en `tests_llamados`; 0 tests sin llamar en el candidato) | OK — CONFIRMED-CLOSED. Nota menor: `tests_sin_llamar` toma como llamada cualquier `test_x(` en el archivo, también dentro de un comentario o un docstring. |
| BE-GK47 | '60.0 LF' leído como 'impreso en 0' | CB_BE_HF02 | El mismo test de BE-CR42, que ahora sí se llama | OK — CONFIRMED-CLOSED |
| NG-3.1 / BE-PM04 | Versión nueva no probada sobre los proyectos abiertos | `compuerta_entrega.prueba_abiertos` + `verificar_version.revisar_prueba_abiertos` | Ninguno: grep de `prueba_abiertos` en `tools/test_*.py` y en `test_verificar_version.py` = 0 | WEAK — STILL-WEAK. (1) No hay test de ninguna de las dos funciones. (2) `revisar_prueba_abiertos` solo mira `ok: true`: no exige que estén TODOS los proyectos abiertos. `apartados/PRUEBA_ABIERTOS_v81cf119_XF.json` trae un solo proyecto ("entrega" = Xfinity), sin CR ni GK, y con eso pasaría. (3) Solo se exige cuando INDICE ya marca v119 como vigente, es decir, después de publicar. |
| NG-3.2 / BE-PM05 | Versión cambiada a mitad de la compuerta final | `version_proyecto_fallas` dentro de CE_PROTOCOLO_3H para entregas nuevas + `fijar_version_proyecto` (cambio sin `--causa` = error) | `test_v119_postmortem_12b`: sin archivo, otra versión, cambio sin causa y causa sin 'causa:' en TIEMPOS dan falla; con todo, pasa | OK — CONFIRMED-CLOSED. El test es de la función, no corre CE_PROTOCOLO_3H completo. |
| NG-3.3 / BE-PM06 | Sin alarma de presupuesto mientras se trabaja | `alerta_presupuesto` (solo con `--paso`) + `presupuesto_fallas(exigir_plan)` | `test_v119_postmortem_12b` (`alerta_presupuesto` 50 %; con más del 100 % hacen falta causa y plan) | WEAK — STILL-WEAK. La alarma es opcional: solo salta si la sesión corre `--paso`. Ningún chequeo exige corridas `--paso` por paso, y ninguno lee `ALERTA_PRESUPUESTO.json`. Lo único que se exige es 'causa:' + 'plan:' en la compuerta FINAL, o sea después del hecho. Arreglo propuesto: que CE_PROTOCOLO_3H exija corridas `--paso` en el registro y `ALERTA_PRESUPUESTO.json` cuando TOTAL > 50 %. |
| U-193 | MAPA DE COBERTURA: rojos con recorte, revisor, motivo y N/HOJA; detector ciego; mutación | `mapa_cobertura`, `_cob_disp`, `ce_cobertura` (CE_COBERTURA) | `test_v119_cobertura` (sintético: un muro sin markup da ROJO; los cuartos 902/901/903 dan ROJO/CUBIERTO/EXCLUDED; un PNG por rojo; una disposición sin N/HOJA, sin revisor o sin imagen no vale) | WEAK — STILL-WEAK. (1) `_cob_disp` no lee la columna `decision`: una disposición con decision=FALTA borra el rojo igual que una NO ES NUESTRO. (2) `ce_cobertura` no tiene ningún test: ni el FAIL por detector ciego (`ciegas`), ni el PDF/CSV faltante, ni la falta de B6. (3) Un RCP con 0 cuartos detectados no se marca como detector ciego (solo se revisan plantas con 0 muros). (4) La mutación sobre CR (TO-W.4-L2-02 y el corredor 216) se hizo a mano: no está en la suite, que solo tiene la mutación sintética. (5) 'revisor' es texto libre: no se comprueba que sea un revisor distinto del que hizo el take-off. |

## Resumen

- CONFIRMED-CLOSED: U-189, U-190, BE-CR39, BE-CR42, BE-GK47 y NG-3.2.
- STILL-WEAK: U-185 (residual), BE-CR40, NG-3.1, NG-3.3 y U-193.
- Suite 47/47 OK. verificar_version v119 da OK con el CIERRE y FALLA con el 12b actual, como se esperaba.
- Recomendación: no publicar el CIERRE como "0 WEAK" ni declarar cerrados los NO GUARD 3.1 y 3.3 hasta arreglar los STILL-WEAK. Lo mismo para U-193 como compuerta "falta = no se entrega".
