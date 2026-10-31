# Archivo de skills por proyecto (no borrar)
Cada proyecto cerrado guarda aquí la versión exacta del skill con la que terminó. El siguiente proyecto arranca desde la última y la mejora.

| Proyecto | Versión | Fecha | Archivo |
|---|---|---|---|
| Bank of America Broomfield | v80h | 2026-10-27 | take-off-metal-frame-drywall_v80h_FINAL-BOA-Broomfield_2026-10-27.zip |
| Barnes & Noble Colorado Springs | v80s | 2026-10-28 | take-off-metal-frame-drywall_v80s_FINAL-BandN-ColoradoSprings_2026-10-28.zip |
| Barnes & Noble Colorado Springs (runner API) | v80t | 2026-10-31 | take-off-metal-frame-drywall_v80t_runner_2026-10-31.zip |
| O'Reilly Evans #1 (prueba ciega, suscripción) | v80u | 2026-10-31 | take-off-metal-frame-drywall_v80u_OReilly_2026-10-31.zip |

**MEJOR SKILL VIGENTE: v80s** (B&N, resultado final verificado rev13; probado con la cadena completa).
Próximo proyecto: arranca con una COPIA del mejor skill; nunca con una versión no probada.
Nota 29-oct: la prueba API de costeo (28-oct) NO invalida v80s: falló por no usar la cadena completa del skill (R80e.37).

**31-oct: v80t** = v80s + R80e.37–R80e.52 + `runner/` (corrida por API con la cadena completa).
- 148 archivos; suite 5/5 OK; dry-run B&N exacto vs rev13 (materiales y Partition Takeoff; Pending Items cambia a propósito por el formato de RFI R80e.50).
- Para un proyecto nuevo: arrancar con una COPIA de v80t; el runner necesita el bid set limpio, el SHEET_MAP y el inventario de tags del proceso.

**31-oct: v80u** = v80t + R80e.63–R80e.77 (corrida O'Reilly, ver tools/CAMBIOS_tools_v80u.md). Suite 5/5 OK. **El mejor skill para comparar sigue siendo v80s / B&N rev13** (orden del estimador); v80u se valida contra el take-off humano de O'Reilly.
