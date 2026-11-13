# VERIFICACIÓN 10 — delta v81cf138r2b (CE_PROTOCOLO_3H, 49ef0ac -> v138r3)

**Veredicto: NO PUBLICAR** (un hallazgo, C1. Se arregla con una línea. B1 es un residual de diseño que hay que dejar escrito).

**Alcance:** solo el delta de `/tmp/claude-0/r2/delta_49ef0ac.diff`:
- `GAP_REV_ANTERIOR_H = 12`;
- `tiempos_desde`;
- `alarma_fallas(desde=)`.

El candidato está en `/tmp/v138r3/take-off-metal-frame-drywall/tools/compuerta_entrega.py`. La base es v137, en `/tmp/v137/take-off-metal-frame-drywall/tools`.

**Cómo se juzga:** con `proceso_v119`. Se busca un caso que dé FAIL en v137 por una falla de proceso (sin contar el (7) de versión) y PASS en el candidato.

## Lo que el delta sí cierra
- **Q4res de la verificación 9** (pasos de la misma mañana con `inicio rev21` escrito tarde): ahora da FAIL, igual que v137. Lo comprueban `adv9_protocolo.py` y `adv9_protocolo2.py`.
- **Caso legítimo:** `test_v138_protocolo_rev_posterior_solo_sus_pasos` da OK. La rev anterior es de otro día y hay una marca `inicio revN`.
- **Frontera de 12 h:**
  - El candidato es coherente entre `tiempos_desde`, que exime con `t <= desde-12h`, y `alarma_fallas`, que descarta las marcas con `t <= corte`.
  - Con 11 h 59 min el paso no se exime (FAIL). Con 12 h 00 y con 12 h 01 se exime. El corte en 12 h está dentro del diseño.

## Hallazgos

### C1 (regresión, MEDIA) — marcas de la rev actual con la hora hacia atrás, después de `inicio rev21`
**Entrada** (`adv10_delta.py`, caso `C_cadena_atras`). El `tiempos.log`, en orden de archivo:
```
2026-11-13 10:00 | inicio rev21
2026-11-12 23:00 | 1 fin
2026-11-12 12:00 | 2-3 fin
2026-11-13 10:30 | 4 fin
```
- VERSION_PROYECTO tiene `2026-11-13T18:00:00Z`.
- TIEMPOS.md cierra el paso 1 el 11-12 a las 23:00, el paso 2-3 el 11-12 a las 12:00 y el paso 4 el 11-13 a las 10:30.
- Hay corridas `--paso` de los pasos 1 y 4. **No hay corrida del paso 2-3.**

**Resultado:**

| Base | Resultado |
|---|---|
| v137 | `FAIL`: "paso 2-3 cerrado en TIEMPOS.md sin su corrida … --paso 2-3" |
| Candidato | `PASS`: "1 paso(s) … son de una rev anterior" |

**Causa:**
- `inicio_rev_info` solo marca problema si un salto hacia atrás pasa de 12 h. Una cadena de saltos de 11 h cada uno pasa.
- `tiempos_desde` toma como `previas` las marcas con **hora** anterior a `desde`. No mira el orden del archivo.
- Por eso una marca que el log pone **dentro** de la rev actual (después de `inicio rev21`) exime su paso y además sale de la alarma.

El problema viene de rev2 (49ef0ac). El delta no lo abre, pero tampoco lo cierra.

**Arreglo sugerido:** en `tiempos_desde` (y en el corte de `alarma_fallas`), que cuenten como `previas` solo las marcas que están en el archivo **antes** de la marca de arranque de la rev, es decir `ms[:k0]` de `inicio_rev_info`, además de la condición de hora. Otra opción: dar como "fuera de orden" una caída acumulada de más de 12 h por debajo de `ini`.

### B1 (residual de diseño, BAJA) — la misma rev trabajada la tarde anterior, con el arranque anotado al día siguiente (12 h o más)
**Entrada** (caso `B_tarde_dia_sig`):
- Pasos 1 y 2-3 cerrados el 11-12 a las 17:30 y a las 18:30, con sus marcas y sin `--paso`.
- `inicio rev21` y VERSION_PROYECTO el 11-13 a las 08:00.
- No hay git.

**Resultado:**

| Base | Resultado |
|---|---|
| v137 | `FAIL` (pasos 1 y 2-3 sin corrida, más la alarma) |
| Candidato | `PASS` (2 pasos exentos) |

Desde los datos, este caso no se distingue del caso legítimo del test: pasos sin etiqueta antes de `inicio revN`, en otro día. El corte de 12 h es justamente esa concesión. Hay que dejar escrito en la regla que **anotar el arranque 12 h o más tarde exime el trabajo anterior**. La defensa es que VERSION_PROYECTO o git se fijen al arrancar.

### Casos sin regresión
| Caso | v137 | Candidato | Nota |
|---|---|---|---|
| A11h59 (Fin 11 h 59 min antes del arranque) | FAIL | FAIL | Correcto. |
| A12h00 / A12h01 | FAIL | PASS | Exento por diseño, igual que el test legítimo. |
| D: paso exento más una marca `5 fin` después del arranque, sin corrida | FAIL | FAIL | La marca nueva se juzga. |
| E: fila sin MM-DD de la rev anterior | FAIL | FAIL | Más estricto: su marca vieja se descarta y no cuadra. Puede dar un FAIL de más a un legítimo sin fecha, pero no es una regresión. |
| F: dos filas idénticas viejas, con marca | FAIL | PASS | Las dos son de la rev anterior (misma Fin y 12 h o más). Es por diseño. |
| G: alarma con una marca de la rev anterior dentro de la ventana de 12 h (00:30 -> 08:00, na=1) | FAIL | FAIL | El cruce se sigue detectando. |
| H: la rev actual cruza el presupuesto sola, sin ALERTA | FAIL | FAIL | |
| I: VERSION_PROYECTO sin zona (se lee como UTC) | FAIL | FAIL | El arranque queda más temprano, así que es más estricto. |
| J: log escrito en hora UTC y VERSION_PROYECTO correcto | FAIL | FAIL | El mínimo usa VERSION_PROYECTO. |

**Zona horaria:** `desde.replace(tzinfo=t.tzinfo)` compara la hora local de PT contra las marcas naive de PT. Funciona porque `marcas_tiempos_log` siempre devuelve datetimes naive. Si algún día devuelve datetimes con zona, `replace` (que no convierte) daría resultados mal sin avisar. Es una nota y no tiene impacto hoy.

## Corridas
Todas con `python3 -I`. Los datos sintéticos están en `/tmp/verif10/tmp`.

- **`/tmp/verif10/adv9_protocolo.py`** (copia de verif9 con `BASE` en `/tmp/verif10/tmp`). Corre los dos árboles por dentro. Q4res, Q4b y CTRL dan FAIL en los dos. No hay regresión.
- **`/tmp/verif10/adv9_protocolo2.py`** (copia de verif9 con `BASE` en `/tmp/verif10/tmp`). Q4res, NoVP y GitEarly dan FAIL en los dos. No hay regresión.
- **`/tmp/verif10/adv8_pm06.py <tools>`** (copia de verif8 con `T` en `/tmp/verif10/tmp`), corrido con v137 y con el candidato. Q1, Q2, Q3, Q4 y Q1b dan FAIL en los dos.
- **`/tmp/verif10/adv10_delta.py`** (nuevo). Tiene los casos A a J de arriba. Las salidas que marca como "REGRESION" son A12h00, A12h01, B y F, todas por diseño, y C, que es el hallazgo C1.
- **`/tmp/verif10/run_test_legit.py`** corre `test_v138_protocolo_rev_posterior_solo_sus_pasos` y los tests `test_v138r2_*` de protocolo. Todos dan OK.
