# CAMBIOS tools v77 — decisiones del usuario D1-D6 y compuertas R76.7

- canon.py: `_atm_wall` (D1): la wall del ATM con `atm_recess` pasa completa a "extra framing ATM" (studs de
  studs_nodos + bottom + top runner de corridas) y sale de su familia de stud / track (una vez); `front_line` viaja a
  headers.py; R77.7 `carrying_direction` obligatoria con ceilings suspendidos (joists con span propio siguen con span);
  llama chequeos_v77.
- accesorios.py: `atm_recess_valido` ({source N/HOJA, drawn}); la fórmula sistered + furring y `extra_framing` kind
  atm_recess = error; renglón "Extra framing - ATM wall (full wall framing, floor to deck + bottom and top runner)".
- headers.py (D2 / D5): CONT. BOX BEAM con `front_line` (primera a última jamb, ro_w_ft = jambs / escala, dos runs en
  la misma línea = error, run_ends solo jamb_to_jamb); piezas de cada fila del schedule = su rótulo (SINGLE 1,
  DOUBLE 2, "2-…" 2); door con with_sill = error.
- chequeos_v72.py: R72.11 = compuerta D1 (fórmula vieja o atm_recess fuera de un wall = falla).
- chequeos_v77.py (nuevo, D3 / D4): strips de pier por vector con scale_check, jambs × alto impreso, plies del rótulo
  + rfi; pier con `jamb_strips` o `jamb_strips_none_reason`.
- reglas.py: A_BLOCKING lee "F.R.T." (RX_FRT_ROTULO); A_TRACK_RUNS salta el renglón movido a ATM (`moved_to`).
- plantilla_excel.py: `es_texto_es` quita rutas, archivos, ids y coordenadas (R76.7 b); FRT plywood no se valida
  como repartido cuando se rehace desde `frt_plywood_by_material`.
- vigas_sobre_walls.py: `cruzar(..., hoja=)` solo bands de la hoja de planta (R76.7 c).
- bitacora.py: lock fcntl en `anotar` y realpath en hashes / vigencia (R76.7 d).
- copia_limpia.py (nuevo) + inventario_tags.py + alcances.py + arranque.py: siempre la copia sin /Annots; arranque.json
  en la carpeta de trabajo (R76.7 e).
- test_v77.py (nuevo, 13 casos); tests ATM / CONT / ceilings actualizados al esquema v77.
