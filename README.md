# Reading-Plans

Control de versiones de los skills de take-off de metal frame y drywall.

## Contenido

| Carpeta / archivo | Qué es |
|---|---|
| `skills/take-off-metal-frame-drywall/` | Skill principal de take-off (Div. 05 / Div. 09) |
| `skills/back-check-take-off/` | Skill de back-check independiente |
| `skills/precios-materiales-fbm/` | Skill de precios FBM |
| `ERRORES.md` | Registro de cada error y su regla, por versión |

## Flujo para actualizar un skill

1. Editar el skill en `skills/`.
2. Agregar la fila en `ERRORES.md`.
3. Commit: `vNN: <regla en una línea>`.
4. Subir el skill actualizado a claude.ai (Settings → Capabilities → Skills).

Para ver qué cambió entre versiones: historial de commits en GitHub.
Para volver a una versión anterior: tomar el skill de ese commit y subirlo otra vez.

## Nota

Las herramientas (`_herramientas/py/`) viven en Google Drive y no están en este repo todavía.
