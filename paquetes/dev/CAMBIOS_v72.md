# CAMBIOS v72 (2026-10-19)

Origen: arbitraje de las pruebas ciegas #20A / #20B (ARBITRAJE_20.md, fuera del paquete). Paquete CIEGO: SKILL.md y
referencias/ sin valores de ningún proyecto (`test_ciego_v69.py` OK: 24 archivos, 0 hallazgos).

## Idea central
Las dos corridas difirieron 6.5 puntos con el mismo skill porque reglas ESCRITAS (R70.4, R70.5, R71.2, R71.14,
R71.15, la regla de double row del MEP) se aplicaban a criterio de cada lectura. v72 las vuelve compuertas o tools.

## SKILL.md
- Versión v72; bloque "v72 — cambios que mandan" al inicio.
- Etapa 2: datos que la compuerta exige (side A|B|END, hatch_extent de walls K, faces de diagonales, part_of, MEP
  con method mep.cruces, jogs del FRP, alternativas del ATM) + checklist de exteriores (BOX HEADER AS NEEDED →
  vestibule_head; column wraps del canopy en las dos lecturas).
- §8 compuerta 0d (`chequeos_v72.py`). §11 tests v72. R71.14 aclarada (la tool manda). §18 nuevo: R72.1–R72.12.
- referencias/herramientas.md: chequeos_v72, cruzar_diagonal v72, idioma_es.

## Tools
Ver tools/CAMBIOS_tools_v72.md. El zip trae TODAS las tools de nivel superior (capas de Drive en orden + v70c + v72):
una prueba baja solo este zip.

## Tests
- `test_v72.py`: 18 tests OK; con las tools v71 fallan 17 (el otro es protección del alcove).
- Suite completa del zip: 43 de 43 rc 0 (incluye test_sin_colisiones, que fallaba en v71).
- Sin el stub del entorno: `idioma_es.py` ahora viaja.
- No localizados en Drive desde este entorno (sus tools sí van): test_registro.py, test_verif_caras.py,
  test_verif_confirmado.py, test_verif_respuesta.py.

## Pendiente conocido (RFIs del arbitraje)
ATM sistered (alto / ancho / furring), B2K (1.26 vs hatch 1.50 vs 1.773), L exterior de piers, CONT. BOX BEAM
run_ends, vendor_end compartido, G1 stubs del frente oeste (no impresos).
