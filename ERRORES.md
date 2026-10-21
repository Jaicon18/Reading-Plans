# Registro de errores

Cada error real deja una fila aquí, en el MISMO turno en que se crea su regla.
El desarrollo completo de cada regla vive en el skill (`skills/take-off-metal-frame-drywall/`).

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

> v43 no aparece en el skill actual. [PENDIENTE] confirmar si existió.
