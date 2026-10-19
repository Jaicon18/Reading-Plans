# CAMBIOS v71 (2026-10-19)

Origen: arbitraje de las pruebas ciegas #19A / #19B (ARBITRAJE_19.md, fuera del paquete) + PARA REVISAR de las dos
pruebas + criterio del estimador. Paquete CIEGO: SKILL.md, referencias/ y tools/ sin valores de ningún proyecto
(`test_ciego_v69.py` OK sobre SKILL y referencias; tools revisadas y limpiadas de casos de proyecto).

## SKILL.md
- Versión v71; bloque "v71 — cambios que mandan" al inicio.
- §0 **E28 reescrita** (modo "eje"): un wall = una línea recta de un type; corta en esquina / jog / T entre dos líneas
  con tag, cambio de type, hueco vacío o con otro type; no corta en door, wall que cruza, beam, grid, altura ni room;
  segmento sin tag se suma; grupo sin tag = un wall; exteriores por eje.
- Etapa 2: cada wall del canon con `tag_ids`. §8 compuerta 0c (chequeos_v71) y track por tamaño en `verificar`.
- §9 anuladas v71; §11 R67–R74 con test; §13 PT2 / PT3 (eje, Layers ponderado); §17 nuevo: R71.1–R71.16.
- referencias/herramientas.md: particion (eje), chequeos_v71, track_por_tamano, mep, vigas_sobre_walls.

## Tools
Ver tools/CAMBIOS_tools_v71.md (particion, partition_types, chequeos_v71 nuevo, etapas, headers, canon, plantilla_excel,
track_por_tamano nuevo, mep, vigas_sobre_walls, accesorios, framed_openings).

## Tests
- `test_v71.py`: 28 tests, todos OK; 24 fallan con las tools v70c (los otros 4 son protecciones que ya cumplía "run").
- Suite completa del stack (v66 + v68 + v70c + v71): 28 de 29 rc 0; `test_plantilla.py` pide argumentos (igual que en
  v70). Los test_plantilla_v67 / v68 / v70 necesitan `idioma_es.py` del entorno de la prueba (no está en las capas de
  tools): con ese módulo presente pasan.
- `test_ciego_v69.py` sobre SKILL.md + referencias/: OK.

## Pendiente conocido
- RFIs abiertos: partición run vs eje (RFI-ARB19-W1), anchors en column wraps / piers, CONT. BOX BEAM run_ends,
  ATM sistered, B2K, L exterior de piers, vendor_end compartido.
- Yields con fórmula viva en NET, RFIs de accesorios en inglés con signo, studs_nodos T contra caja, E26 base_ft: v72.
