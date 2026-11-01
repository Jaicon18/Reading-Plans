# Monitor de BuildingConnected

Vigila cada hora los proyectos de `proyectos.json`: addenda, planos revisados, archivos quitados e invitaciones
nuevas de otros GC para el mismo proyecto. SOLO LECTURA en BuildingConnected (nunca acepta, declina ni manda nada).

- `monitor.js` — una corrida (un solo login). rc 0 sin cambios · rc 3 con cambios · rc 1 error.
- `proyectos.json` — lista de proyectos e invitaciones (opp id, foto, carpeta de Drive).
- `fotos/` — último árbol conocido de cada invitación (nombre, tamaño, fecha).
- `ultimo_reporte.md` / `historial.md` — resultado de la última corrida y bitácora.

Lo nuevo se baja y se sube a la carpeta del proyecto en Drive (`JC HUNTER PROJECTS › Projects › <proyecto>`);
un archivo cambiado se sube como `REV <fecha> <nombre>` (nunca se sobrescribe). La carpeta Photos solo se reporta.

**Agregar un proyecto:** un objeto más en `proyectos.json` con `buscar` (texto del nombre en BC), `trades`,
`drive_folder_id`, y sus invitaciones; la foto base se toma con `node paquetes/dev/tools/bc_descarga.js foto <opp> monitor_bc/fotos/<x>.json`.
**Dejar de vigilar uno:** `"activo": false`.
