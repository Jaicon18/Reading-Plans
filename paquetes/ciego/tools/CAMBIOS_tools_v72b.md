# CAMBIOS tools v72b (2026-10-19) — reglas inviolables

| Tool | Cambio |
|---|---|
| reglas.py (nuevo) | `compuerta <work_dir> [--excel]`: 67 chequeos (a) + motor de evidencia (b) por caso + catálogo completo; absorbe chequeos_v71, chequeos_v72, esquinas.py y la compuerta de etapas; recalcula las salidas con canon.py (vigencia); sale rc 1 con una falla; `faltantes`, `tabla`; sello del Excel (hoja oculta `_reglas`). Sin flag de override. |
| reglas_catalogo.py (nuevo) | extrae cada regla del SKILL.md y de referencias/ con id estable (ids explícitos E/R/PT/D/A/REGLA nn.n; viñetas por sección + huella del texto). |
| reglas_clasificacion.py (nuevo) | decisión a / b / c de cada regla; 35 specs de evidencia (b); una regla nueva sin decisión = falla. |
| plantilla_excel.py | `armar(d, salida, trabajo)`: corre `reglas.exigir(trabajo)` antes de escribir; exige `--familias` del familias_out.json de la carpeta de trabajo (`_familias_sha` de `fusionar`); sella el libro. CLI: `armar … --familias f [--trabajo d]`. El escritor interno `_escribir` solo lo usan los tests de formato: su libro no trae un sello válido y bitacora / reglas --excel lo rechazan. Ejemplo del docstring sin valores de proyecto. |
| etapas.py | `compuerta(d)` = `estructura(d)` + reglas.py compuerta (fallas "reglas: …"); `estructura` = la compuerta v69–v72. |
| bitacora.py | `compuerta` corre reglas.py en modo final (carpeta de trabajo por $TAKEOFF_WORK o junto al takeoff.json; Excel con sello vigente) y exige `reglas.py compuerta` en la bitácora con rc 0. |
| fixture_reglas.py (nuevo) | proyecto sintético de un wall con todo lo que la compuerta exige (etapas, canon, salidas, registro, bitácora, evidencia). |
| test_reglas.py (nuevo) | un test por regla (668): (a) caso malo / bueno por chequeo; (b) sin evidencia falla, con evidencia pasa, valor "a ojo" contradice; (c) fusión no vacía; armar no escribe con una regla violada. |
| test_ciego_tools.py (nuevo) | E24 sobre las tools (comentarios / docstrings + nombre del proyecto en todo el código). |
| ~50 tools | limpieza ciega: rutas por defecto con el proyecto → $TAKEOFF_WORK; nombres de archivo → $TAKEOFF_PREFIJO; cantidades / refs de proyecto en comentarios → `<n>` / `<ref>`; datos de proyecto en código (handoff, resumen_global, dataset, localizar, verif_*) → JSON de la carpeta de trabajo o variables de entorno. |
| test_etapas.py, test_etapas_v70.py, test_bitacora.py, test_plantilla_v67/v68.py | ajustados al comportamiento nuevo (la compuerta exige reglas OK; casos nuevos 25–28 en test_bitacora y 9 en test_etapas). |

Pendiente conocido (no se tocó para no aflojar compuertas): trinquetes medidos de un proyecto en `verif_idioma.py`
(TOPE_*) y `corpus.TOPE_CIERRES_MIN`, coordenadas de `indice_set.py` y la convención de nombres de bloques de cierre
de las tools v38–v60 (`verif_*`, `dataset`, `resumen_total`): siguen funcionando, pero su genericización completa es
trabajo aparte.
