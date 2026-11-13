# VERIFICACIÓN 13: CE_PROTOCOLO_3H completo, candidato v81cf139 (9897cf6)

**Veredicto: NO PUBLICAR.** Hay 1 hallazgo medio (W2) y 3 bajos (X1, G, Y).

- Candidato: /tmp/v139p/take-off-metal-frame-drywall.
- Base: v81cf138 publicada, en /tmp/v138fb/take-off-metal-frame-drywall. No tiene ninguna exención (igual que v137).
- Todo se compara vía `proceso_v119`.
- Los datos son sintéticos y están en /tmp/verif13/tmp. Los scripts están en /tmp/verif13.
- Se corrió con python3 -I. No se hizo commit y no se tocaron /root/xf, /root/cr, /tmp/gk ni ninguna entrega.

Nota de lectura: v138 trae además un "(7) versión distinta". Es un artefacto del script, porque el VERSION_PROYECTO sintético fija la versión v81cf139. El contador lo ignora. Todos los "v138: FAIL" de abajo tienen también fallas de proceso reales.

## Hallazgos

### W2 (MEDIO): variante de W1 por VERSION_PROYECTO. 'inicio rev21', el arranque de la rev en curso, vuelve a contar como evidencia
- **Entrada.**
  - Excel de la entrega sin etiqueta: `Take-off/Z9_Takeoff.xlsx`.
  - VERSION_PROYECTO, último renglón con un typo en `--rev`: `2026-11-13T18:00:00Z | rev22`.
  - tiempos.log: `11-12 17:00 0 Arranque / 11-12 17:30 1 fin / 11-12 18:30 2-3 fin / 11-13 08:00 inicio rev21 / 11-13 08:30 4 fin`.
  - TIEMPOS.md cierra los pasos 1, 2-3 y 4. Solo existe la corrida `--paso 4`.
- **v138:** FAIL (pasos 1 y 2-3 sin su corrida, más la alarma).
- **Candidato:** **PASS**, con el mensaje "2 paso(s) … son de una rev anterior".
- **Mecanismo** (traza en /tmp/verif13/run_w2_trace.txt):
  1. `_etiqueta_rev` cae a VERSION_PROYECTO y da 22.
  2. `_k0_rev` no encuentra ninguna marca 'rev22' y corta DESPUÉS de 'inicio rev21' (k0=4).
  3. `_rev_actual_proyecto` no ve el conflicto: ms[k0] ya no es 'inicio', así que del_log=None y del_vp=22, de donde et=22.
  4. 'inicio rev21' cumple las condiciones de evidencia: 21<22, hora < arranque y antes de k0.
  5. Resultado: tope = arranque - 12 h e idx=[0,1,2,3]. Se eximen los pasos propios de rev21 y además se quita de la alarma la marca de arranque de rev21, lo que contradice R6.
- **Otros casos con el mismo resultado:**
  - W2b: VERSION_PROYECTO con `rev21` y luego `rev22`. Candidato PASS.
  - W2e: igual, con además un PDF de markups `_rev22` más nuevo. Candidato PASS.
- **Controles:**
  - W2c (Excel `_rev21` + VERSION_PROYECTO rev22): FAIL. El conflicto se detecta.
  - W2d (Excel sin etiqueta + VERSION_PROYECTO rev21): FAIL.
- **Causa raíz:** el chequeo W1 solo compara con `ms[k0]`. Cuando k0 sale del respaldo "después de la última marca de otra rev", la marca 'inicio revN' de la rev en curso queda ANTES de k0 y no se compara con nada.
- **Arreglo sugerido.** Cualquiera de estos dos:
  - exigir que k0 venga de `propias`, es decir, que el log tenga la etiqueta de la rev actual; si no, no se exime nada;
  - o comparar la rev de la ÚLTIMA 'inicio revN' anterior a k0 con et, y si no coinciden no se exime nada.
- **Script:** /tmp/verif13/adv13_full.py (casos W2, W2b, W2c, W2d y W2e).

### X1 (BAJO): el campo 'linea' quita por TEXTO, y se puede quitar la fila equivocada
- **Entrada.** Dos tablas en TIEMPOS.md:
  - Tabla A, con encabezado `Inicio | Fin`: tiene la fila de rev21 `| 5 | Rev | 11-12 19:40 | 11-13 09:00 | x |`, cuyo Fin es 11-13 09:00 y no tiene marca en el log.
  - Tabla "rev20 (tabla vieja)", con encabezado `Fin | Inicio` (columnas invertidas): tiene la MISMA línea de texto, que ahí se lee con Fin 11-12 19:40.
  - Evidencia en el log: `rev20 entregada` a las 11-12 19:45. Corridas: pasos 4 y 5.
- **v138:** FAIL.
- **Candidato:** **PASS**.
- **Mecanismo:** `tiempos_desde` exime la fila de la tabla vieja (antes del tope) pero borra la PRIMERA línea con ese texto, que es la de rev21 en la tabla A. Queda la fila vieja, que cuadra con su marca. La traza está en run_w2_trace.txt, con el texto filtrado.
- **Controles:**
  - X1c (sin la tabla vieja): FAIL.
  - X1d (tabla vieja con texto distinto): FAIL.
- **Arreglo sugerido:** quitar por número de línea (que filas_tiempos guarde el índice), no por texto.
- **Script:** /tmp/verif13/adv13_full.py (casos X1, X1c y X1d).

### G (BAJO): RX_EVID_NEGACION no cubre negaciones ni dudas que el LEEME excluye
- Todos los casos siguientes dan v138 FAIL y candidato **PASS**:
  - G3 `¡rev20 entregada! nunca`: "nunca" es una negación;
  - G4 `¿rev20 entregada`: signo de pregunta de apertura, el único que trae la línea. El LEEME dice "no … question mark on the line" y la regex solo busca `?`;
  - semánticamente negativas: G0 `rev20 subida fallida`, G1 `rev20 subida: error 403`, G2 `rev20 entregada (falso)`, G5 `rev20 entregada -> rechazada`, G7 `rev20 entregada [cancelada]`;
  - futuro: G6 `rev20 subida mañana`.
- Controles que siguen en FAIL: G8 `rev20 entregada NO` y G9 `rev20 entregada ?`.
- G3 y G4 violan la regla tal como está escrita. Los demás son negación semántica. Las mismas marcas sin la palabra serían evidencia válida, así que la gravedad es baja.
- **Arreglo sugerido:**
  - añadir `¿`, `nunca`, `never` y `ni` a la negación;
  - añadir una lista de fallo / anulación: `fall[oóiae]`, `error`, `falso`, `rechazad`, `cancelad`, `anulad`, `mañana`, `pending`, `failed`.
- **Script:** /tmp/verif13/adv13_full.py (casos G0 a G9).

### Y (BAJO, falla cerrada): OverflowError en código nuevo
- Y1: VERSION_PROYECTO rev21 con sello `0001-01-01T00:00:00Z`. `arranque_rev_desde` hace `min(cand).astimezone(PT)` y salta OverflowError.
- Y2: el mismo sello en un renglón rev20. Pasa por la rama de VERSION_PROYECTO de `marcas_rev_anterior` (`t.astimezone(pt)`) y también salta OverflowError.
- v138 da FAIL normal. En el candidato, `proceso_v119` lanza excepción. `correr_con_tope` la convierte en FAIL "el chequeo no corrió", así que la falla es cerrada y no hay PASS, pero es un crash nuevo.
- **Arreglo sugerido:** atrapar `OverflowError` en `_dt_utc`, o descartar años menores que 1900.
- Comparación: Y6 (log `2026-13-45 08:00`) revienta con ValueError en LOS DOS árboles (`marcas_tiempos_log`, que es código anterior). No es una regresión.

## Observaciones (conforme a la regla escrita, no bloquean)
- Z1: una fila de rev21 con Fin falso `11-03 09:00` (sin marca y sin --paso), con evidencia `rev20 entregada` a las 11-11 18:00. Candidato PASS, porque la regla exime por "cierra antes del tope" sin exigir marca (CR 13:15). El control sin evidencia da FAIL. La fecha de la fila no se valida contra nada.
- Z2: pasos de rev21 sin etiqueta a las 11-11, seguidos de una re-subida `rev20 subida` a las 11-12 19:00 y de `inicio rev21` a las 11-13. Candidato PASS: con la regla, los pasos anteriores a una entrega de rev20 son de rev20.
- Y9: `inicio rev0` vale como evidencia (0 < 21). Candidato PASS.

## Lo que se comporta bien
- Siguen en FAIL: Y3 (sello basura), Y4 (fila sin MM-DD), Y5 (fecha 02-30), Y7 (zona +14:00), Y8 (evidencia del año anterior), W2c, W2d, X1c, X1d, G8 y G9.
- PASS legítimo: C1.

## Corridas (todas rc=0)
| script | resultado |
|---|---|
| /tmp/verif13/r_adv8_rerun.py <árbol>/tools (verif8) | única diferencia: `tiempos_desde` existe en el candidato (Q1: 0 exentas) |
| /tmp/verif13/r_adv9_rerun.py y r_adv9b_rerun.py (verif9) | 0 regresiones |
| /tmp/verif13/r_adv10_rerun.py (verif10) | 0 regresiones |
| /tmp/verif13/r_adv11_rerun.py (verif11) | REGRESIONES: 0 |
| /tmp/verif13/r_adv12_delta.py (verif12) | el contador marca 7 PASS, todos legítimos (C1, N1, N4, T2, T3, T5, D1c). W1, D1, D2 y O1-O3 ya dan FAIL |
| /tmp/verif13/run_test_legit.py (todos los tests test_v138_protocolo*, test_v138r2_protocolo* y test_v139_protocolo* del candidato) | todos OK, incluidos rev_posterior_solo_sus_pasos, tope_evidencia_otra_rev, evidencia_estricta_r1_r6 y w1_d1_negaciones |
| /tmp/verif13/adv13_full.py (nuevo, 31 casos) | salida en run_adv13_full.txt. El contador marca 16 PASS; clasificados arriba. Reales: W2, W2b, W2e, X1, G0-G7. Observaciones: Z1, Z2, Y9. Legítimo: C1 |
| /tmp/verif13/w2_trace.py | traza de W2, W2c y X1 en run_w2_trace.txt |

Las salidas son los archivos /tmp/verif13/run_*.txt.
