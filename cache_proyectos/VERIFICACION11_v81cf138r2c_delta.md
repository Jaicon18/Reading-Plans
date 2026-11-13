# VERIFICACIÓN 11 — delta CE_PROTOCOLO_3H (37f154d → 3aa8703)

Candidato: `/tmp/v138r3/take-off-metal-frame-drywall` (commit 3aa8703)
Baseline v137: `/tmp/v137/take-off-metal-frame-drywall`
Delta revisado: `/tmp/claude-0/r2/delta_37f154d.diff`
Alcance: solo el último delta de CE_PROTOCOLO_3H — `_k0_rev`, `marcas_rev_anterior` (con_tope), `RX_ENTREGA_LOG`, `tiempos_desde` (tope=), `alarma_fallas` (previas=, tope=), `proceso_v119`.

## VEREDICTO: **NO PUBLICAR**

El delta introduce la exención "rev anterior" con `tope` (CR 13:15) y la evidencia por palabra (`RX_ENTREGA_LOG`). Ambos mecanismos aceptan evidencia que NO es evidencia positiva de otra rev, y el `tope` se toma sin exigir que sea ANTERIOR al arranque. Resultado: varios casos donde v137 da FAIL de proceso y el candidato da PASS (o baja a solo-alarma) vía `proceso_v119`. Son regresiones reales de la compuerta.

Los dos casos legítimos siguen funcionando: `test_v138r2_protocolo_tope_evidencia_otra_rev` y `test_v138_protocolo_rev_posterior_solo_sus_pasos` pasan, y la suite completa `test_compuerta_entrega.py` corre `rc=0`. El problema no es que rompa lo legítimo, sino que abre exenciones ilegítimas.

## Script

`/tmp/verif11/adv11_delta.py` (derivado de `apartados/verif10_adversariales/adv10_delta.py`; añade VERSION_PROYECTO.txt con varios renglones y marca REGRESIÓN cuando v137 tiene una falla de PROCESO distinta de `(7)` y el candidato da PASS). Datos sintéticos en `/tmp/verif11/tmp`. Corrida: `python3 -I /tmp/verif11/adv11_delta.py` → salida en `/tmp/verif11/run1.txt`. Reporta **6 REGRESIONES**.

Nota de lectura: v137 siempre añade la falla `(7)` (corre con v137 contra proyecto fijado v138); esa falla se ignora. La regresión está en que el candidato borra las fallas de PROCESO (pasos sin --paso, alarma de presupuesto, TIEMPOS.md/log no cuadran) que v137 sí reporta.

## Hallazgos (regresiones)

Confirmación de los disparadores (RX en el candidato):
```
'recibido A-101 Rev 5'          REV-> 5    ENTREGA-> False
'planos subidos por el GC'      REV-> None ENTREGA-> True
'planos A-101 Rev 5 del arq.'   REV-> 5    ENTREGA-> False
'uploaded plans to Drive'       REV-> None ENTREGA-> True
```

### R1 — F4_alarma_oculta: palabra de entrega FALSA en nota de la rev actual oculta el cruce del presupuesto
`RX_ENTREGA_LOG` matchea "subid"/"upload" en cualquier nota, sin exigir otra rev. Una marca de la propia rev con nota "planos subidos por el GC" (04:50), antes de `inicio rev21` (05:00), se vuelve "evidencia": `alarma_fallas` descarta las marcas hasta ella (incluido `0 Arranque` 02:00), mueve t0 a 05:00 y el cruce del 50 %/100 % desaparece.
- Entrada: log `02:00 | 0 Arranque | inicio` / `04:50 | planos subidos por el GC` / `05:00 | inicio rev21` / `05:30 | 4 fin` / `06:20 | 5 fin`; VP `rev21` 13:00Z; na=10.
- v137: FAIL (cruce 50 % en 04:50 y 100 % en 05:00 sin ALERTA).
- Candidato: **PASS []**.
- Control F4c (misma nota sin palabra, "planos del GC"): candidato FAIL = v137. Confirma que la única diferencia es la palabra suelta.
- Regla violada: 1 (evidencia debe llevar OTRA etiqueta de rev o palabra de entrega como prueba de otra rev) y 4 (la alarma solo debe ignorar marcas con evidencia real).

### R2 — F5_vp_tope_posterior: `tope` de un renglón VERSION_PROYECTO de otra rev POSTERIOR al arranque
Sin marca de evidencia en el log, `marcas_rev_anterior` toma `tope = max(ts)` de los renglones de otras revs en VERSION_PROYECTO.txt, sin comprobar que ese `tope` sea anterior al arranque. Con un renglón `rev20` sellado 11-14 (posterior al arranque de rev21, 11-13 10:00), `tiempos_desde` exime toda fila cerrada antes de 11-14, es decir cualquier fila sin marca propia.
- Entrada: log `0 Arranque` 11-12 / `inicio rev21` 11-13 10:00 / `4 fin` 10:30; VP `rev20` 11-14T00:00Z + `rev21` 11-13T18:00Z; fila `2-3` cierra 11-12 12:00 sin marca ni --paso.
- v137: FAIL (TIEMPOS.md/log no cuadran + paso 2-3 sin --paso + alarma).
- Candidato: **PASS** ("1 paso(s)… son de una rev anterior").
- Control F5c (mismo renglón rev20 sellado 11-01, anterior): candidato FAIL = v137. El signo del `tope` es lo único que cambia.
- Regla violada: 3 (el `tope` debe ser la hora de la evidencia de una rev anterior; un sello posterior al arranque no lo es).

### R3 — F5d_vp_rev22: `tope` de un renglón VERSION_PROYECTO de una rev POSTERIOR (rev22)
`marcas_rev_anterior` sólo pide que la etiqueta sea DISTINTA de la actual; una rev MAYOR (rev22) cuenta como "otra rev". Un renglón `rev22` sellado después del arranque exime filas igual que R2, aunque rev22 no es una rev anterior.
- Entrada: VP `rev21` 11-13T18:00Z + `rev22` 11-14T00:00Z; resto como R2.
- v137: FAIL. Candidato: **PASS**.
- Regla violada: 1/3 (evidencia debe ser de otra rev ANTERIOR, no de una posterior).

### R4 — F6_marca_tope_posterior: marca de evidencia con hora POSTERIOR al arranque usada como `tope`
Una marca `rev20 entregada` con fecha 11-14 (errata) colocada en el archivo ANTES de `inicio rev21` (11-13) es evidencia válida para el candidato; `tope = 11-14 09:00` (posterior al arranque) exime la fila 2-3 (11-12 12:00).
- v137: FAIL. Candidato: **PASS** ("son de una rev anterior").
- Regla violada: 3 (el `tope` no se compara contra el arranque; una evidencia fechada después del arranque no debería eximir nada).

### R5 — F7_tope_falso: "Rev 5" de los planos (revisión de dibujo) tomado como evidencia de otra take-off rev
`RX_REV_ETIQ` matchea "Rev 5" en una nota de planos; `5 != 21` → cuenta como evidencia de otra rev. `tope = 11-12 20:00` exime la fila 2-3 (11-12 12:00).
- Entrada: log `0 Arranque` 11-12 / `recibido A-101 Rev 5` 11-12 20:00 / `inicio rev21` 11-13 10:00 / `4 fin`; VP rev21; fila 2-3 sin marca ni --paso.
- v137: FAIL. Candidato: **PASS**.
- Regla violada: 1 (texto "rev" dentro de una nota no es evidencia de otra take-off rev).

### R6 (secundario, de diseño) — F4b_alarma_rev_real: evidencia REAL de otra rev oculta el cruce del trabajo propio de la rev actual
Con evidencia real `rev20 entregada` (04:50) antes de `inicio rev21` (05:00), la regla 4 descarta de la alarma todas las marcas hasta 04:50, incluida `0 Arranque` 02:00 que es trabajo de la rev ACTUAL. El cruce del presupuesto de la propia rev (02:00→05:00) desaparece.
- v137: FAIL. Candidato: **PASS []**.
- Esto es la regla 4 "la alarma ignora las marcas hasta la última de evidencia" aplicada al pie de la letra, pero su efecto es borrar el arranque real de la rev del cálculo de presupuesto. Lo dejo como hallazgo de diseño/soporte, no como la base del veredicto; R1–R5 ya bastan.

## Resumen de regresiones

| Caso | Mecanismo | v137 | Candidato |
|---|---|---|---|
| F4_alarma_oculta | palabra 'subid'/'upload' falsa en nota de la rev actual | FAIL (alarma) | PASS |
| F5_vp_tope_posterior | tope de VP (rev20) posterior al arranque | FAIL | PASS |
| F5d_vp_rev22 | tope de VP de rev POSTERIOR (rev22) | FAIL | PASS |
| F6_marca_tope_posterior | marca de evidencia fechada tras el arranque | FAIL | PASS |
| F7_tope_falso | "Rev 5" de planos = evidencia falsa | FAIL | PASS |
| F4b_alarma_rev_real (dis.) | evidencia real borra el arranque propio de la alarma | FAIL | PASS |

Controles negativos (candidato = v137, sin exención): C0_control_sin_evidencia, F1/F2/F3/F3b/F3c (nota suelta sin marca separada), F4c_control, F5c_vp_tope_anterior, F8_evidencia_post, F9_varias_revs. Confirman que el cambio de comportamiento viene exactamente de los disparadores de arriba.

## Causa raíz (código del delta)

En `marcas_rev_anterior` (tools/compuerta_entrega.py):
- rama de VERSION_PROYECTO: `tope = max(ts)` de otras revs, SIN exigir `tope < arranque` ni que la rev sea anterior → R2/R3.
- rama de log: `RX_ENTREGA_LOG` / `RX_REV_ETIQ` sobre `ms[:k0]` sin validar que la etiqueta sea de una rev ANTERIOR ni que el `tope` sea anterior al arranque → R1/R4/R5.

En `tiempos_desde(..., tope)`: `elif tope is not None and t < tope...: fuera.append(f)` exime por cercanía al `tope` sin volver a comprobar que el `tope` sea anterior al arranque.

En `alarma_fallas(..., previas=, tope=)`: descarta `ms[:len(previas)]` de la alarma, con `previas` producidas por el `marcas_rev_anterior` ya contaminado → R1/F4b.

## Corridas

- `python3 -I /tmp/verif11/adv11_delta.py` → `/tmp/verif11/run1.txt` (6 REGRESIONES).
- Confirmación de RX (snippet arriba) con `python3 -I -c`.
- Suite del candidato: `python3 -I tools/test_compuerta_entrega.py` → rc=0 (legítimos OK: test_v138r2_protocolo_tope_evidencia_otra_rev, test_v138r2_protocolo_marcas_despues_del_arranque, etc.).
