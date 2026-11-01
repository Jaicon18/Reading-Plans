# Regla 0 — fuente de planos (2026-11-01)

Decisión del usuario, regla general para todos los proyectos:
- Los proyectos se bajan siempre de BuildingConnected.
- Si ahí no hay nada, se busca en el correo estimating@jchunter.us (algunos clientes mandan los planos solo por correo).
- Nunca se acepta ni se declina nada en BuildingConnected.

Error que la originó: el zip de "Download Selected" de BuildingConnected no arrancó en 10 min; se perdió tiempo esperando.
Solución: `tools/bc_descarga.js` (solo lectura, baja archivo por archivo por la API y verifica bytes).
Primer uso: Chuze Fitness Austin Bluffs (Hilbers + NNI Construction).

Nota: el repo tiene la v77c; la versión vigente en Drive es la v80h. Esta regla se agregó al SKILL.md del repo
y [PENDIENTE] hay que pasarla también al paquete v80h cuando ese paquete se suba al repo.
