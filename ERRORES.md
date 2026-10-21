# Registro de errores

Cada error real deja una fila aquí, en el MISMO turno en que se crea su regla.
El desarrollo completo de cada regla vive en el skill (`paquetes/dev/take-off-metal-frame-drywall/`).
El texto completo de los cambios v58 en adelante está en `historial/`.

**Cómo agregar una fila nueva:**
1. Escribir la regla en el skill (adenda nueva).
2. Agregar la fila al final de esta tabla.
3. Commit con el mensaje: `vNN: <regla en una línea>`.

| Versión | Fecha | Proyecto | Error / origen | Regla | Dónde vive |
|---|---|---|---|---|---|
| v26 | 2026-09-28 | BOA Broomfield | Auditoría adversarial | Hallazgos de la auditoría | `referencias/adenda_v26.md` |
| v27 | 2026-09-28 | BOA | Columna con significado equivocado | Compuerta de SIGNIFICADO de columna | `referencias/adenda_v27.md` |
| v28 | 2026-09-28 | BOA | Partidas sin cubrir | Compuerta de COBERTURA | `referencias/adenda_v28.md` |
| v29 | 2026-09-28 | BOA | Libro inconsistente | Compuerta del LIBRO | `referencias/adenda_v29.md` |
| v30 | 2026-09-28 | BOA | Zonas húmedas omitidas | Barrido de ZONAS HÚMEDAS | `referencias/adenda_v30.md` |
| v31 | 2026-09-28 | BOA | Cambio sin regenerar Excel | Ningún cambio termina hasta regenerar el Excel | `referencias/adenda_v31.md` |
| v32 | 2026-09-29 | BOA | Materiales traducidos | Todo material se escribe en inglés | `referencias/adenda_v32.md` |
| v33 | 2026-09-29 | BOA | Planos marcados a mano | El juego de planos marcados es automático | `referencias/adenda_v33.md` |
| v34 | 2026-10-01 | BOA | Detalles sin abrir | Compuerta de cobertura de detalles | `referencias/adenda_v34.md` |
| v35 | 2026-10-01 | BOA | Índice escrito a mano | El índice se genera (`hoja_indice.py`) | `referencias/adenda_v35.md` |
| v36 | 2026-10-02 | BOA | Cadena de detalles cortada | La cadena de detalles se sigue hasta el final | `referencias/adenda_v36.md` |
| v37 | 2026-10-03 | BOA | 42 callouts abiertos | Los 42 callouts, cerrados | `referencias/adenda_v37.md` |
| v38 | 2026-10-04 | BOA (canopy 84) | Orden de trabajo invertido | Plano → cadena → total → Excel | `referencias/adenda_v38.md` |
| v39 | 2026-10-07 | BOA | Vocabulario traducido | El vocabulario del trade va en inglés | `referencias/adenda_v39.md` |
| v40 | 2026-10-07 | BOA | Regla del inglés no verificada | La regla del inglés se verifica | `referencias/adenda_v40.md` |
| v41 | 2026-10-08 | BOA | Room heredado | El room de cada face se verifica | `referencias/adenda_v41.md` |
| v42 | 2026-10-08 | BOA | Elevación tomada como height | `[CONFIRMADO]` cita su printed dimension | `referencias/adenda_v42.md` |
| v44 | 2026-10-10 | BOA | 95 detalles sin abrir | Barrido por tag de schedule, no por wall | `referencias/adenda_v44.md` |
| v45 | 2026-10-10 | BOA | Cita que no prueba cantidad | Una cita de material no prueba cuánto hay | `referencias/adenda_v45.md` |
| v46 | 2026-10-11 | BOA | Huecos en la regla de waste | Reglas escritas como partition | `referencias/adenda_v46.md` |
| v47 | 2026-10-11 | BOA | Compuerta por renglón ciega | Compuerta que ve la cerca | `referencias/adenda_v47.md` |
| v48 | 2026-10-11 | — | Herramientas dispersas | Una sola carpeta `_herramientas/py/` | `SKILL.md` |
| v49 | 2026-10-13 | — | Entregas mezcladas | Una carpeta por proyecto en la unidad compartida | `SKILL.md` |
| v50 | 2026-10-13 | — | Trabajo perdido entre sesiones | Libro de partidas, respaldo y compuerta | `SKILL.md` |
| v51 | 2026-10-13 | — | Skill demasiado grande | Skill en niveles (`referencias/`) | `SKILL.md` |
| v52 | 2026-10-14 | BOA prueba auto | Alcances completos omitidos (24.9%) | Lista fija de 24 alcances + `plantilla_excel.py` | `SKILL.md` |
| v53 | 2026-10-14 | BOA prueba #2 | Criterios distintos por estimador | Criterios del estimador aprobados | `SKILL.md` |
| v54 | 2026-10-15 | BOA prueba #4 | Framed openings omitidos | Framed openings de fixtures | `SKILL.md` |
| v55 | 2026-10-15 | BOA prueba #5 | Partidas incompletas | El crítico de completitud se corre siempre | `SKILL.md` |
| v56 | 2026-10-15 | BOA prueba #6 | Números antes del registro | Registro antes del primer número | `SKILL.md` |
| v57 | 2026-10-15 | BOA | Tools no corridas | Toda tool se corre por `bitacora.py run` | `SKILL.md` |
| v58 | — | BOA | ver historial | ADENDA v58 — 16-oct-2026 · ARBITRAJE DE LA PRUEBA #8 (studs, track, sill, framed openings, blocking, unidades de compra) | `historial/v58.md` |
| v59 | — | BOA | ver historial | ADENDA v59 — 16-oct-2026 · ARBITRAJE DE LA PRUEBA #9 (largos netos, bandas, parapet, esquinas, piers, purlin) | `historial/v59.md` |
| v60 | — | BOA | ver historial | ADENDA v60 — 16-oct-2026 · ESTABILIDAD: HERRAMIENTAS DETERMINISTAS (studs por nodo, board por face) + reglas 60.x | `historial/v60.md` |
| v61 | — | BOA | ver historial | ADENDA v61 — 16-oct-2026 · CAMBIO DE ESTRATEGIA: PROTOCOLO CORTO + takeoff_canon.json + canon.py | `historial/v61.md` |
| v67 | — | BOA | ver historial | INTEGRACIÓN HECHA — PAQUETE v67 (2026-10-17) | `historial/v67.md` |
| v69 | — | BOA | ver historial | CAMBIOS v69 (2026-10-17) — flujo por etapas | `historial/v69.md` |
| v70 | — | BOA | ver historial | CAMBIOS v70 (2026-10-18) | `historial/v70.md` |
| v71 | — | BOA | ver historial | CAMBIOS v71 (2026-10-19) | `historial/v71.md` |
| v72 | — | BOA | ver historial | CAMBIOS v72 (2026-10-19) | `historial/v72.md` |
| v72b | — | BOA | ver historial | CAMBIOS v72b (2026-10-19) — REGLAS INVIOLABLES | `historial/v72b.md` |
| v73 | — | BOA | ver historial | CAMBIOS v73 (2026-10-19) — la compuerta revisa consistencia con el plano | `historial/v73.md` |
| v73b | — | BOA | ver historial | CAMBIOS v73 / v73b (2026-10-19) — la compuerta revisa consistencia con el plano | `historial/v73b.md` |
| v73c | — | BOA | ver historial | CAMBIOS v73 / v73b / v73c (2026-10-19) — la compuerta revisa consistencia con el plano | `historial/v73c.md` |
| v73d | — | BOA | ver historial | CAMBIOS v73 / v73b / v73c / v73d (2026-10-19) — la compuerta revisa consistencia con el plano | `historial/v73d.md` |
| v73e | — | BOA | ver historial | CAMBIOS v73 / v73b / v73c / v73d / v73e (2026-10-19) — la compuerta revisa consistencia con el plano | `historial/v73e.md` |
| v74 | — | BOA | ver historial | CAMBIOS v74 (2026-10-20) — estudio de partición de walls + limpieza del paquete ciego | `historial/v74.md` |
| v75 | — | BOA | ver historial | CAMBIOS v75 — clasificación del track, jamb return por borde, cambios de type (arbitraje de dos pruebas ciegas) | `historial/v75.md` |
| v75b | — | BOA | ver historial | CAMBIOS v75 — clasificación del track, jamb return por borde, cambios de type (arbitraje de dos pruebas ciegas) | `historial/v75b.md` |
| v76 | — | BOA | ver historial | CAMBIOS v76 — hand-off entre tareas, jogs entre caras, box con tag, entrega coherente (arbitraje de dos pruebas ciegas) | `historial/v76.md` |
| v77 | — | BOA | ver historial | CAMBIOS v77 — decisiones del usuario D1-D6 (Bluebeam) hechas reglas, compuertas R76.7 sin falsos bloqueos | `historial/v77.md` |
| v77b | — | BOA | ver historial | CAMBIOS v77b — corrección corta de v77 (D1 sobre la wall correcta, largo de wall a través de doors) | `historial/v77b.md` |
| v77c | — | BOA | ver historial | CAMBIOS v77c — decisiones del usuario U1–U11 (Bluebeam, 2026-10-20) | `historial/v77c.md` |
| v62, v64, v65b, v66, v68, v69b, v70b, v70c | — | — | — | Paquete sin nota de cambios en Drive; ver el diff del commit | `paquetes/dev/` |

**Huecos:** v43, v63 y v65 no están en Drive. [PENDIENTE] confirmar si existieron.
