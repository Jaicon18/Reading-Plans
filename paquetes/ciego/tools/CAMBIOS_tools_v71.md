# CAMBIOS tools v71 (2026-10-19)

Origen: arbitraje de dos pruebas ciegas (fuera del paquete). Todo genérico; cada cambio con test en `test_v71.py`.

| Tool | Cambio | Regla |
|---|---|---|
| particion.py | modo "eje" (nuevo default): línea recta por tag; esquina / jog / T entre dos líneas con tag corta; segmento sin tag se suma al wall con tag que toca; grupo sin tag = un wall; hueco colineal solo se cruza con un R.O. del wall dentro; exteriores por eje; un pier exterior no vuelve exterior a un type interior; sin tag_ids = corte en esquinas + jogs sumados. "run" y "tramo" quedan como opciones | E28 v71 / R71.12 |
| partition_types.py | pasa `tag_ids` y `openings` a particion; exterior por type (no por un wall suelto); Layers = Σ(layers × largo de face) / LF | R71.12 / R71.13 |
| chequeos_v71.py (nuevo) | R71.1 flecha norte con fachadas; R71.2 box contado dos veces; R71.3 accesorios de bulkhead > Σ vanos; R71.5 (un tag descartado "por otra tarea") | compuerta 0c |
| etapas.py | `compuerta` corre chequeos_v71 sobre el canon conciliado | compuerta 0c |
| headers.py | header_type "ASSUMED" / "NOT PRINTED" = error; CONT. BOX BEAM exige `run_ends` | R71.10 / R71.11 |
| canon.py | pasa `run_ends` / `run_ends_source` a headers; docstrings sin casos de proyecto | R71.11 |
| plantilla_excel.py | `verificar_r71_track`: con ≥ 2 tamaños de stud, bottom / top track un renglón por tamaño; ejemplo sin nombre de proyecto | R71.8 |
| track_por_tamano.py (nuevo) | reparte la familia de track por tamaño / gauge; resto "other"; resto negativo = falla | R71.8 |
| mep.py | sin offsets, página ni comentarios de un set; `arq` obligatorio; registro en cada corrida | R71.9 / E24 |
| vigas_sobre_walls.py | eje dentro de la band manda; dos vigas paralelas con rótulo distinto = `candidatas` + decisión; un dueño por rótulo | R71.14 |
| accesorios.py | slab pins también en chase; PAFs ROUNDUP por run de parapet (`_runs_parapet`) | A7 |
| framed_openings.py | `_src`: la primera parte cita N/HOJA, el resto puede ser texto | — |

Tests viejos ajustados (el default dejó de ser "run"): test_particion_v70, test_partition_types_v70, test_partition_types
(prueban "run" de forma explícita); test_headers y test_canon (fixture CONT. BOX BEAM con `run_ends`); test_plantilla_v68
(fixture con track por tamaño).
