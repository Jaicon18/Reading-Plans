# Reading-Plans

Control de versiones de los skills de take-off de metal frame y drywall.

## Contenido

| Carpeta / archivo | Qué es |
|---|---|
| `paquetes/dev/` | Paquete de desarrollo vigente (v77c): `take-off-metal-frame-drywall/` + `tools/` + `CAMBIOS_*.md` |
| `paquetes/ciego/` | Paquete ciego vigente (v77c), el que se usa en las pruebas automáticas |
| `skills/back-check-take-off/` | Skill de back-check |
| `skills/precios-materiales-fbm/` | Skill de precios FBM |
| `historial/` | Nota de cambios de cada versión (v58 a v77c) |
| `ERRORES.md` | Registro de cada error y su regla, por versión |

Cada versión v58 a v77c es un commit propio, en orden. El contenido de `paquetes/` es idéntico
a los zips de Drive (`JC HUNTER PROJECTS/Claude outputs`).

## Flujo para una versión nueva

1. Poner el contenido del zip nuevo en `paquetes/dev/` y `paquetes/ciego/`.
2. Copiar su `CAMBIOS_vNN.md` a `historial/vNN.md` y agregar la fila en `ERRORES.md`.
3. Commit: `vNN: <cambio en una línea>`.

Para ver qué cambió entre versiones: historial de commits en GitHub.
Para volver a una versión anterior: tomar `paquetes/` de ese commit y volver a armar el zip.

## Nota

El skill instalado en claude.ai es la v57. Las versiones v58 a v77c solo están en Drive y en este repo.
