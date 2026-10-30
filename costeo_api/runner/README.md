# Runner de take-off por API (cadena completa del skill v80s, R80e.37)

El modelo SOLO LEE (canon A y canon B independientes + resolución dirigida); los programas calculan. **No se hizo ninguna llamada real a la API.**

## Archivos
| Archivo | Qué es |
|---|---|
| `run_takeoff.py` | Orquestador (10 pasos, abajo) |
| `overlay.py` | Fusiona el overlay de decisiones del estimador al canon y a takeoff.json. Es genérico e idempotente (upsert / remove por `ref`, set de constants y claves) |
| `decisiones_BN.json` | Overlay de B&N con TODAS las decisiones del estimador, en 4 grupos: G1 2026-10-24 (RFI-01 / 23 / 11 / 27 + preguntas rev1), G2 RI 1–11 + RFI-14 / 16 / 17, G3 34 RFI 2026-10-27, G4 PVC / FRP 2026-10-28, + textos del Excel |
| `build_overlay_BN.py` | Cómo se armó: el canon sin decisiones y los canons intermedios por grupo (build_A con salida redirigida) → `overlay.diff` por grupo |
| `canon_BN_sin_decisiones.json` | Canon de B&N SIN decisiones del estimador (con plan check / auditoría): la prueba del overlay |
| `cobertura.py`, `prompts/cobertura.md`, `cobertura_lista_BN.json` | Paso 12 reducido: la lectura lista los detalles / notas del trade con su destino y el script verifica que el destino exista |
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
11. Cobertura (paso 12 reducido): una llamada (~1 USD) lista los detalles / notas del trade con su destino; `cobertura.py` verifica que cada destino exista. Un "n/a" sin motivo cuenta como hueco.

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
**Resultado: rev13 exacta**, también partiendo del canon SIN decisiones (`--canon-ref canon_BN_sin_decisiones.json`): el overlay de 4 grupos lo lleva al canon final.
- Canon base 94 walls con perímetro → overlay → 77 walls → Excel.
- Inputs, Partition Takeoff, Material Summary, Pending Items, Review Items y Scope Checklist: 0 celdas distintas.
- Material Summary: 67 / 67 renglones, sin diferencias de Net.
- comparar.py: 0 diferencias A / B.
- Cobertura: 478 / 484 (98.76 %). Los 6 huecos son reales: tres "n/a" sin motivo (A-101 tube holder 5/A-413, A-220, A-222A) y tres notas de proceso de rev7.
- Compuertas:
  - reglas.py: solo queda pendiente el back-check;
  - `registro entregable` y `alcances compuerta`: OK.
- Tiempo: ~1.5 min. Costo: $0.

Lo que el dry-run NO prueba:
- **Las llamadas reales:** su formato JSON de salida y que la lectura escriba el canon completo.
- **El overlay sobre una lectura real:** el overlay es un diff por ref / id. Si la lectura real nombra los walls o los ítems con otros ids, la decisión no encuentra su objeto: el reemplazo por id agrega en vez de cambiar. Para una corrida real, las lecturas deben usar los Wall ID y refs del proyecto, o hay que reconciliar ids antes del overlay. Ese es el riesgo principal de la primera corrida.
- **Textos del Excel:** el `takeoff.json` de base (RFIs / Scope del proyecto) se toma del proyecto.
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
| Cobertura (paso 12 reducido) | cache read ~2–3 M + cache write ~0.1 M + output ~30–60 k | ~1.0 | 1.5 |
| **Total** | | **~10.2–11.0** | tope total 20.0 |
