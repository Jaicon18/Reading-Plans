# Archivo de skills por proyecto (no borrar)
Cada proyecto cerrado guarda aquí la versión exacta del skill con la que terminó. El siguiente proyecto arranca desde la última y la mejora.

| Proyecto | Versión | Fecha | Archivo |
|---|---|---|---|
| Bank of America Broomfield | v80h | 2026-10-27 | take-off-metal-frame-drywall_v80h_FINAL-BOA-Broomfield_2026-10-27.zip |
| Barnes & Noble Colorado Springs | v80s | 2026-10-28 | take-off-metal-frame-drywall_v80s_FINAL-BandN-ColoradoSprings_2026-10-28.zip |
| Barnes & Noble Colorado Springs (runner API) | v80t | 2026-10-31 | take-off-metal-frame-drywall_v80t_runner_2026-10-31.zip |
| O'Reilly Evans #1 (prueba ciega, suscripción) | v80u | 2026-10-31 | take-off-metal-frame-drywall_v80u_OReilly_2026-10-31.zip |
| O'Reilly Evans #1 FINAL (rev4, pendiente de calificación del estimador) | v80u | 2026-11-01 | take-off-metal-frame-drywall_v80u_FINAL-OReilly_2026-11-01.zip |

**MEJOR SKILL VIGENTE: v80s** (B&N, resultado final verificado rev13; probado con la cadena completa).
Próximo proyecto: arranca con una COPIA del mejor skill; nunca con una versión no probada.
Nota 29-oct: la prueba API de costeo (28-oct) NO invalida v80s: falló por no usar la cadena completa del skill (R80e.37).

**31-oct: v80t** = v80s + R80e.37–R80e.52 + `runner/` (corrida por API con la cadena completa).
- 148 archivos; suite 5/5 OK; dry-run B&N exacto vs rev13 (materiales y Partition Takeoff; Pending Items cambia a propósito por el formato de RFI R80e.50).
- Para un proyecto nuevo: arrancar con una COPIA de v80t; el runner necesita el bid set limpio, el SHEET_MAP y el inventario de tags del proceso.

**31-oct: v80u** = v80t + R80e.63–R80e.78 (corrida O'Reilly, ver tools/CAMBIOS_tools_v80u.md). Suite 5/5 OK. **El mejor skill para comparar sigue siendo v80s / B&N rev13** (orden del estimador); v80u se valida contra el take-off humano de O'Reilly.

**01-nov: v80w** = v80v + R80e.98–R80e.108 (corrida Victoria's Secret #679 Downey, ver tools/CAMBIOS_tools_v80w.md). Suite 5/5 OK. Incluye: madera excluida directo (orden del usuario), demolition plan obligatorio en la lectura, familias impresas nuevas, fixes de trazabilidad / alcances / markups con texto en curvas.

| Victoria's Secret #679 Downey (rev1, pendiente de revisión del estimador) | v80w | 2026-11-01 | take-off-metal-frame-drywall_v80w_VS-Downey_2026-11-01.zip |

**01-nov: v80x** = v80w + R80e.109–R80e.113 (VS Downey rev2: paso 11 auditor a ciegas + paso 12 biblioteca 17 FAIL resueltos; ver tools/CAMBIOS_tools_v80x.md). Suite 5/5 OK.

| Victoria's Secret #679 Downey rev2 (REGLAS OK, back-check registrado; pendiente del estimador) | v80x | 2026-11-01 | take-off-metal-frame-drywall_v80x_VS-Downey-rev2_2026-11-01.zip |

**02-nov: v80y** = v80x + R80e.114 (blocking de accesorio 3' x 2 filas) + R80e.115 (ductos siempre EXCLUDED), reglas del usuario (cache_proyectos/REGLAS_ALCANCE.md R-ALC-02/03).

| Victoria's Secret #679 Downey rev4 FINAL (0 RFI abiertos) | v80y | 2026-11-02 | take-off-metal-frame-drywall_v80y_VS-Downey-rev4_2026-11-02.zip |

**02-nov: v80z** = v80y + R80e.116 (demolición de gyp bd / metal framing = nuestro alcance, familia de demolición SF sin waste; regla R-ALC-04).

| Victoria's Secret #679 Downey rev5 (demo incluida) | v80z | 2026-11-02 | take-off-metal-frame-drywall_v80z_VS-Downey-rev5_2026-11-02.zip |
