# Runner de take-off por API (cadena completa del skill v80s, R80e.37)

El modelo SOLO LEE (canon A y canon B independientes + resolución dirigida); los programas calculan. **No se hizo ninguna llamada real a la API.**

## Archivos
| Archivo | Qué es |
|---|---|
| `run_takeoff.py` | Orquestador (10 pasos, abajo) |
| `overlay.py` | Fusiona el overlay de decisiones del estimador al canon y a takeoff.json. Es genérico e idempotente (upsert / remove por `ref`, set de constants y claves) |
| `decisiones_BN.json` | Overlay de B&N: 34 RFI (2026-10-27) + PVC / FRP (2026-10-28) |
| `build_overlay_BN.py` | Cómo se armó `decisiones_BN.json` desde el canon y el takeoff.json finales |
| `prompts/lectura.md`, `prompts/resolucion.md` | Prompts de las llamadas `claude -p` (el SKILL.md completo va como system prompt) |
| `dry_run_resultado_BN.json` | Resultado del dry-run de B&N |

## Cadena (cada herramienta por `bitacora.py run`)
1. Workdir nuevo (no pisa nada). La evidencia se enlaza con su ruta relativa (`../../<carpeta>/img`), porque sin eso reglas.py falla.
2. Proceso: `arranque.py`, `alcances.py escanear / renglones`, `registro.py crear`. En dry-run, además, las herramientas de la lectura de referencia (`indice_set`, `contar_tags`, `test_ciego`) se re-ejecutan con las rutas reescritas.
3. `inventario_tags.py`.
4. Lectura A y lectura B: `claude -p` (o el canon de referencia en dry-run). Son independientes y cada una corre en su propio proceso.
5. `comparar.py` (A vs B + inventario).
6. Resolución SOLO de las diferencias (`claude -p`, con el recorte de cada diferencia). Si no hay diferencias, no se llama.
7. Overlay de decisiones del estimador → `takeoff_canon.json` + `takeoff.json`.
8. `canon.py`, `inventario.py`, `framed_openings.py`, `alcance_filtro.py`, sello (`--sealer`: closer.py + planmark.py), `vigas_sobre_walls.py`, `markups_bluebeam.py`.
9. `plantilla_excel.py validar / armar`; la compuerta `reglas.py` va adentro y el runner se detiene si no arma. Después: `registro.py entregable`, `alcances.py compuerta` y `reglas.py compuerta`. El runner se detiene ante cualquier falla, salvo el back-check, que es un paso posterior y queda reportado.
10. Comparación celda por celda contra un Excel de referencia (`--compare-with`).

Llamadas a la API:
- `ANTHROPIC_API_KEY` se toma de `$TAKEOFF_API_KEY`; el runner nunca la imprime ni la guarda.
- Flags: `--model sonnet --max-budget-usd <tope del paso> --output-format json --allowedTools "Read,Write,Glob,Grep,Bash(python3:*)"`. Nunca bypassPermissions.
- Tope total con `--budget` (default 20 USD): el runner se detiene antes de un paso que pueda pasarlo.
- Cada llamada queda registrada en `../costos.csv` (el dry-run no escribe).

## Dry-run B&N (2026-10-30)
```
python3 costeo_api/runner/run_takeoff.py --dry-run --pdf <bidset_SIN_MARKUPS.pdf> --skill <skill v80s> \
  --project-inputs cache_proyectos/barnes_noble/takeoff_work --evidence-root cache_proyectos/barnes_noble \
  --overlay costeo_api/runner/decisiones_BN.json --sealer cache_proyectos/barnes_noble/takeoff_work/scripts/sellar_y_marcar.py \
  --canon-ref cache_proyectos/barnes_noble/takeoff_work/etapas/4_canon/takeoff_canon.json \
  --compare-with cache_proyectos/barnes_noble/FINAL_FOR_REVIEW_2026-10-24_rev13/Take-off/Barnes_Noble_ColoradoSprings_Takeoff_FINAL_rev13.xlsx \
  --work <dir nuevo>
```
**Resultado: rev13 exacta.**
- Inputs, Partition Takeoff, Material Summary, Pending Items, Review Items y Scope Checklist: 0 celdas distintas.
- Material Summary: 67 / 67 renglones, sin diferencias de Net.
- comparar.py: 0 diferencias A / B.
- Compuertas:
  - reglas.py: solo queda pendiente el back-check;
  - `registro entregable` y `alcances compuerta`: OK.
- Tiempo: ~1.5 min. Costo: $0.

Lo que el dry-run NO prueba:
- **Las llamadas reales:** su formato JSON de salida y que la lectura escriba el canon completo.
- **El overlay sobre una lectura sin decisiones:** sobre el canon final es idempotente, así que en el dry-run no cambia nada. Probar sobre un canon sin decisiones queda para la primera corrida real. Si una decisión toca un wall que la lectura no trae, el overlay lo rechaza.
- **Decisiones anteriores a rev12:** las decisiones del estimador rev1–rev9 (DECISIONES_ESTIMADOR.md: deck 25'-0", type 2 de 14 ga, perimeter existing, etc.) no están en `decisiones_BN.json`. Una lectura nueva debe aplicarlas por R80e.34, o hay que agregarlas al overlay.
- **El sello:** `sellar_y_marcar.py` es del proyecto. Su texto de control joint dice "EXCLUDED", desactualizado frente a la decisión de RFI-24. No afecta al Excel; hay que actualizarlo.

## Estimación de costo por paso (Sonnet)
Precio efectivo, despejado de las 4 filas Sonnet de `costos.csv`:
- output $10.0 / MTok;
- cache read $0.10 / MTok;
- cache write $4.0 / MTok.

El input sin cache es de cientos de tokens por llamada y no pesa.

| Paso | Tokens esperados (base: pasada 1) | USD estimado | Tope del paso |
|---|---|---|---|
| Proceso, inventario_tags, comparar, canon.py, tools, plantilla, reglas | — (scripts) | 0.00 | — |
| Lectura A | cache read ~18.6 M + cache write ~0.44 M + output ~42 k | ~4.0 | 6.0 |
| Lectura B | cache read ~17.4 M + cache write ~0.33 M + output ~40–170 k | ~4.0–4.7 | 6.0 |
| Resolución dirigida (solo diferencias) | cache read ~2.8 M + cache write ~0.13 M + output ~43 k | ~1.2 | 2.5 |
| **Total** | | **~9.2–10.0** | tope total 20.0 |

Cobertura reducida del paso 12 (REDISENO_RUNNER.md, paso 8, ~$1): todavía no está en el runner; se agrega antes de la corrida real.
