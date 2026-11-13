# VERIFICACIÓN 9 — diff v81cf137 → v81cf138 rev2 (commit 49ef0ac)

Revisor adversarial independiente. Alcance: SOLO el diff `v81cf138r2_desde_v81cf137.patch` (3 arreglos).
Scripts en `/tmp/verif9/`, datos sintéticos en `/tmp/verif9/tmp`. `python3 -I`. No se corrió la compuerta sobre entregas reales ni se escribió en /root/xf, /tmp/gk ni carpetas de entrega.

## VEREDICTO: **NO PUBLICAR**

Regresión confirmada en el arreglo 3 (CE_PROTOCOLO_3H): una rev cuya única ancla de arranque es una marca `inicio revN` escrita tarde — con `VERSION_PROYECTO.txt` también sellado tarde y sin un commit git temprano en la carpeta — **exime pasos de la PROPIA rev (de la misma mañana) que cierran en TIEMPOS.md sin su corrida `--paso`**. v137 daba FAIL (BE-PM06); el candidato da PASS en silencio. Es exactamente la clase Q4 ("un arranque tardío exime todo") que el rev2 decía cerrar con el `min()`; el `min()` sólo cierra el hueco cuando existe una señal MÁS temprana (git o VERSION_PROYECTO), y no cuando ambas llegan tarde junto con la marca.

| fix | archivo | veredicto | una frase |
|---|---|---|---|
| 1. CB_BE_CF04 | tools/chequeos_biblioteca.py | **VERDE** | Sólo amplía (madera en más formas + `framing`): todo FAIL de v137 sigue FAIL, ningún canon real nuevo FAIL; dirección segura PASS→FAIL. |
| 2. CB_BE_83 | runner/completitud.py | **VERDE** | La LISTA de caras es idéntica a v137 (A0–A5); `faces` numérico (antes crash) ahora se juzga; ningún caso real donde v137 marcara y el candidato calle. |
| 3. CE_PROTOCOLO_3H | tools/compuerta_entrega.py | **ROJO** | Hueco Q4 residual: con `inicio revN` + VERSION_PROYECTO tardíos y sin ancla git temprana, silencia pasos de la misma rev sin `--paso` → PASS donde v137 daba FAIL. |

---

## Regresión (fix 3)

**Entrada** (`/tmp/verif9/adv9_protocolo2.py`, caso `Q4res`): rev21 que arranca y trabaja el 13-nov. tiempos.log:
```
2026-11-13 08:00 | 1 inicio
2026-11-13 08:30 | 1 fin
2026-11-13 09:30 | 2-3 fin
2026-11-13 10:00 | inicio rev21      <- única marca etiquetada rev21, anotada tarde
2026-11-13 10:30 | 4 fin
```
VERSION_PROYECTO.txt sellado `2026-11-13T18:00:00Z` (= 10:00 PST, tan tarde como la marca). La carpeta NO es repo git. TIEMPOS.md cierra los pasos 1, 2-3 y 4; sólo el paso 4 tiene su corrida `--paso`. Los pasos 1 y 2-3 son de la rev actual y NO tienen su corrida → violación BE-PM06 real.

- **v137**: `FAIL` — `paso 1 … sin su corrida '--paso 1'`, `paso 2-3 … sin su corrida '--paso 2-3'`.
- **candidato**: `PASS` — `"2 paso(s) de TIEMPOS.md cerrados antes del arranque de la rev (2026-11-13T10:00:00-08:00) son de una rev anterior: no se juzgan otra vez (v138)"`.

Causa: `arranque_rev_desde` toma `min(ini, VERSION_PROYECTO, git)`; aquí `ini`=10:00 (primera marca etiquetada rev21, por `inicio_rev_info`), VERSION_PROYECTO=10:00, git ausente → `desde`=10:00. `tiempos_desde` ve los pasos 1/2-3 con Fin < 10:00 y marcas de cierre antes de 10:00, los da por "rev anterior" y los quita; `proceso_v119` recomputa ev sin ellos y, como el paso 4 sí tiene corrida, cae en la rama de PASS temprana. Las marcas 08:00–09:30 están SIN etiqueta de rev y son del mismo día: el candidato las atribuye por error a una rev previa.

**Reproduce**: `python3 -I /tmp/verif9/adv9_protocolo2.py` (caso `Q4res`, sin ruido de versión). También en `/tmp/verif9/adv9_protocolo.py` (caso Q4res, con una línea extra `(7)` artefacto de versión).

**Alcance / calibración** (mismo script, variantes):
- VERSION_PROYECTO sellado TEMPRANO (07:50) → candidato `FAIL` (ancla temprana cierra el hueco). Caso `Q4b`.
- Sin VERSION_PROYECTO → candidato `FAIL`, pero por la falla "(7) sin VERSION_PROYECTO.txt", no por los `--paso` (que SIGUEN silenciados). No es regresión limpia pero el hueco de `--paso` está presente.
- Carpeta ES repo git con commit a las 08:00 → candidato `FAIL` correcto (git ancla `desde` temprano). Caso `GitEarly`.

Es decir: el hueco necesita (VERSION_PROYECTO tardío O ausente-con-sello) **y** ausencia de commit git temprano en la carpeta de la rev. Es más estrecho que el Q4 de la verificación 8, pero sigue siendo un FAIL→PASS real sobre el candado de proceso (el que existe por el incidente de 838 min sin alarma). Un sellado tardío de VERSION_PROYECTO coincide de forma natural con escribir `inicio revN` tarde.

---

## Hallazgos previos — verificados cerrados

- **(a) palabras sueltas en LISTA de caras silenciando (A1–A4)**: CERRADO. `adv8_be83.py` contra el candidato: A1–A4 siguen marcando en v137 y en el candidato (lista usa `RX_SUBE_V137`, idéntica a v137). A0–A5 idénticos entre árboles.
- **(b) `_cara_de_muro` aplicado a muros sin faces**: CERRADO. `faces` ausente/dict → `[]` (como v137); `_cara_de_muro` sólo corre con `faces` numérico. B2/B10 = `[]` en ambos.
- **(c) `tiempos_desde` borrando filas por coincidencia de hora (Q1b)**: CERRADO para coincidencia pura (quita la línea exacta; `test_v138r2_verif8_tiempos_desde_pruebas` pasa). El problema remanente del fix 3 NO es coincidencia de hora sino mala atribución del arranque.
- **(d) arranque tardío eximiendo todo (Q4)**: **PARCIALMENTE abierto** — ver regresión arriba.
- **(e) log sin marcas ISO dando PASS (Q2)**: CERRADO. `test_v138r2_protocolo_log_sin_fecha_como_v137` pasa; log sin fecha = FAIL.

## Observación menor (no regresión)
CB_BE_CF04: un muro de metal con "wood blocking" o "2 x 4 blocking by GC" dentro de `framing`/`gauge` ahora da FAIL (antes PASS) — `adv8_cf04.py` casos (c). Es dirección segura (PASS→FAIL) y ningún canon real la dispara (`adv9_canones.py`: todos IGUAL en cf04, sólo cambia el texto "0 walls"→"ningún wall"). No bloquea.

## Corridas
- `adv8_cf04.py` v137 vs candidato: candidato FAIL en más casos (ampliación); todos los FAIL de v137 siguen FAIL. OK.
- `adv8_be83.py` v137 vs candidato: A0–A5 idénticos; B1/B3–B8 pasan de crash a juicio/[] razonable; sin FAIL→silencio. OK.
- `adv9_canones.py` (todos los canones reales, read-only): cf04 todos IGUAL; be83 sólo 2 CR DISTINTO = v137 crasheaba (TypeError) y el candidato ahora marca 3 caras. Sin silencios nuevos. OK.
- Suite `test_compuerta_entrega.py` del candidato: EXIT 0 (todos los tests OK, incluidos los 7 nuevos de v138/r2).
- `adv9_protocolo.py` / `adv9_protocolo2.py`: regresión Q4res reproducida (arriba).
