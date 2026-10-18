# CAMBIOS v70 (2026-10-18)

Origen: arbitraje #18A / #18B (ARBITRAJE_18.md, fuera del paquete) + PARA REVISAR de las dos pruebas + criterio del
estimador (partición "run"). Paquete CIEGO: SKILL.md, referencias/ y tools/ sin valores de ningún proyecto
(`test_ciego_v69.py` OK sobre SKILL, referencias y los .md de tools).

## SKILL.md
- Versión v70; bloque "v70 — cambios que mandan" al inicio del protocolo.
- §0 **E28**: "un run continuo del mismo partition type con quiebres o esquinas = 1 wall" (LF = suma de tramos; T no
  encadena; nunca entre hojas ni types). E14 afinado (R70.1: el detalle tiene que estar llamado sobre ESE ceiling).
- Etapa 1 = `inventario_tags.py`; Etapa 2: partición run, refs de aberturas primero (2a), `page` 1-based, banda
  `{c0,c1 = caras; lo,hi = extensión}`.
- §8 compuerta 0b `esquinas.py`; candidatos fuera de schedule (`PC####`) en la compuerta 0.
- §9, §11 (R57–R66), §13 PT2 (run) / PT3 / PT8 (cara de finish, un dueño por esquina, door dentro del run).
- §16 nuevo: R70.1–R70.9.
- Las líneas del criterio E28 llevan `[ciego-ok]` (el texto del estimador trae "1 wall"; revisado a mano).
- referencias/herramientas.md: inventario_tags.py, particion.py (run), esquinas.py.

## Tools (tools/; detalle por línea en tools/CAMBIOS_tools_v70.md)
- particion.py: MODO_DEFAULT = "run"; door_bulkhead → BULKHEAD-<familia>; unión transitiva (union-find).
- inventario.py (v69, Etapa 1) → **inventario_tags.py**; ids únicos (PC#### para candidatos, prefijos sin choque) con
  recorte propio; candidatos dentro de la compuerta. test_sin_colisiones.py (canon sigue importando el inventario de walls).
- etapas.py: `unir` no se cae con claves de tipo distinto (ERROR), notes por fragmento como dict, banda traspuesta,
  `page` 0-based, refs de aberturas contra `opening_schedule`; `compuerta` corre esquinas.py sobre 4_canon.
- comparar.py: rechaza `page` 0-based; docstrings con inventario_tags.
- canon.py: rechaza canopy_soffit en walls; roof_step / ceiling_transition / soffit_side / ceiling_bulkhead /
  vestibule_head / grille_head sin `faces` ni `faces_none_reason`; claves fuera de esquema con números
  (`canon.WALL_KEYS`); operación de canopy_joist con el RUN; deck_breaks por hoja; R70.1 `system_callout`; R70.6
  pier por parte; R70.7 storefront desde el piso fuera del wall.
- accesorios.py: `sill_return: false` + source (jamb return sin borde del sill; sill track igual); atm `*_status`
  CRITERIO con rfi; R70.9 cadena completa del head.
- plantilla_excel.py `verificar`: renglón con tool en 0 cuando la tool da > 0 = falla; R70.8 yields desde Inputs.
- closer.py: header `steel_by_others` con source; headers.py: fuentes con paréntesis y "N/HOJA:".
- partition_types.py: agrupa con particion (run); PT4 / PT5 / BULKHEAD se mantienen.
- **esquinas.py** nuevo (R70.2 / R70.3).

## Tests
- Suite completa del stack + v70: 45 de 45 rc 0 (sin contar test_alcances / test_eval_takeoff / test_plantilla, que
  piden argumentos). Cada test v70 falla con el código viejo (salvo el de storefront_cripples en pins: protección).
- test_ciego_v69.py: OK.

## Pendiente conocido
- Los canons reales de 18A/18B ya no cargan con canon.py v70 (las nuevas reglas los rechazan con motivo): es lo
  esperado; ver ARBITRAJE_18 para qué marca cada regla.
- 3-5/8" stud: después de Waiting [room] quedan +315 (18A) / +141 (18B) sobre el rango sin arbitrar con plano.
