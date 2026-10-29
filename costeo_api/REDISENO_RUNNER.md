# Rediseño del runner de costeo por API (sin gasto; para aprobar antes de otra corrida)

## Hallazgo clave
El skill ya está diseñado para que el modelo SOLO LEA y los programas CALCULEN:
plano.pdf → inventario_tags.py (script) → lectura A y lectura B (modelo, JSON canon) → comparar.py (script) → resolución dirigida (modelo, solo diferencias) → canon.py + reglas.py (script: materiales y compuerta de reglas) → plantilla_excel.py (script).
La prueba API saltó esto: el modelo calculó los materiales "a mano" (paso C) y la compuerta reglas.py se apagó ("stubbed"). De ahí salieron los errores de studs, FRP, blocking, screws.

## Runner nuevo (por pasos)
| # | Paso | Quién | Costo |
|---|---|---|---|
| 1 | Inventario de hojas y tags | inventario_tags.py | $0 |
| 2 | Lectura A → takeoff_canon_A.json (walls, types, alturas, caras, detalles por wall) | Sonnet, con SKILL.md completo + reglas R80e.* | ~$4 |
| 3 | Lectura B independiente → takeoff_canon_B.json | Sonnet, mismo contexto, sin ver A | ~$4 |
| 4 | Comparación A vs B + alertas (tag sin wall, etc.) | comparar.py | $0 |
| 5 | Resolución SOLO de las diferencias (recorte por diferencia) | Sonnet | ~$1–2 |
| 6 | Materiales + compuerta de reglas (bloquea si falta FRP de types 3/4, header track, blocking por filas, yields de Inputs) | canon.py + reglas.py | $0 |
| 7 | Excel formato fijo | plantilla_excel.py | $0 |
| 8 | Cobertura (paso 12) reducida: cada nota/detalle del trade con destino | script + Sonnet solo para huecos | ~$1 |
Total estimado: ~$10–12 (vs $14.12 de la prueba fallida), con el método completo.

## Candados nuevos
- Cada llamada recibe SKILL.md completo + reglas generales (R80e.34) como obligatorias.
- Ninguna llamada calcula materiales: solo produce JSON canon; los números salen de los programas.
- La resolución/revisión NO puede cambiar Inputs del estimador (yields, waste, stock) ni contradecir una regla del skill.
- reglas.py nunca se apaga; si falla, el runner se detiene y reporta.
- Validación sin API antes de correr: canon.py sobre el canon de rev13 (cache_proyectos/barnes_noble/takeoff_work/etapas/4_canon/takeoff_canon.json) debe reproducir las cantidades de rev13.
