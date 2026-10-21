# CAMBIOS v77b — corrección corta de v77 (D1 sobre la wall correcta, largo de wall a través de doors)

Origen: el estimador revisó en Bluebeam la decisión D1 de v77 y la regla del largo de wall. Cada cambio es genérico
(ningún número, wall ni room de un proyecto) y tiene test sintético (test_v77.py, test_v72.py).

## D1 corregida (R77.1, manda sobre v77)
- Extra framing ATM = la PARTICIÓN INTERIOR que CONTIENE la unidad ATM de lobby (walk-up), la que el detalle del ATM
  llama sobre esa wall: la wall completa, studs @ O.C. impreso de piso a deck (`to_deck: true`) + bottom runner + top
  runner. Nada de sistered ni furring aparte.
- La wall exterior de un drive-up NO es este renglón: su framing queda en su type exterior; ese ATM declara
  `atm_recess_none_reason`. `atm_recess` en una wall exterior = error (canon.py y chequeos_v72 R72.11).
- Convención del estimador: la partición SIGUE en su partition type y en sus familias de stud / track (v77 la restaba:
  revertido); canon.py emite un RFI con el delta de contarla una sola vez.
- Compuertas: wall interior con studs_nodos y corridas, `to_deck: true`, `atm_recess {source N/HOJA, drawn}`; fórmula
  vieja, `extra_framing` kind atm_recess a mano o atm_recess fuera de un wall = error. A_TRACK_RUNS ya no salta walls
  `moved_to` (ninguna wall se mueve).

## R77.10 (decisión del usuario): largo de wall a través de doors
- El largo de un wall corre A TRAVÉS de sus doors hasta la esquina o la intersección donde termina; el R.O. de la
  door queda dentro del largo (confirma R70.3 / E10). Compuerta: con `band {p0, p1}` y `openings[].xy_pt` un R.O.
  fuera del largo del wall (± 6") = falla (chequeos_v77 `r77_10`, lo llama canon.py).

## Paquete ciego
- Sin menciones de un proyecto en tools (ejemplos de rótulo, N/HOJA de un set, número de arbitraje).
