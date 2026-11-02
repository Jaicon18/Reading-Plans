# Archivo de skills por proyecto (no borrar)
Cada proyecto cerrado guarda aquí la versión exacta del skill con la que terminó. El siguiente proyecto arranca desde la última y la mejora.

| Proyecto | Versión | Fecha | Archivo |
|---|---|---|---|
| Bank of America Broomfield | v80h | 2026-10-27 | take-off-metal-frame-drywall_v80h_FINAL-BOA-Broomfield_2026-10-27.zip |
| Barnes & Noble Colorado Springs | v80s | 2026-10-28 | take-off-metal-frame-drywall_v80s_FINAL-BandN-ColoradoSprings_2026-10-28.zip |
| Barnes & Noble Colorado Springs (runner API) | v80t | 2026-10-31 | take-off-metal-frame-drywall_v80t_runner_2026-10-31.zip |
| O'Reilly Evans #1 (prueba ciega, suscripción) | v80u | 2026-10-31 | take-off-metal-frame-drywall_v80u_OReilly_2026-10-31.zip |
| O'Reilly Evans #1 FINAL (rev4, pendiente de calificación del estimador) | v80u | 2026-11-01 | take-off-metal-frame-drywall_v80u_FINAL-OReilly_2026-11-01.zip |

**VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO: la última unida (hoy v81cf3: v81cf2 + compuerta A_BARRIDO_NO_DIBUJADO, verificada 0 reglas faltantes).** v80s queda como referencia de exactitud (B&N rev13), no como versión de arranque (BE-115).
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

**02-nov: v80z2** = v80z + R80e.117 (demo de cielos existentes sin tipo indicado = EXCLUDED por falta de información, R-ALC-05).

| Victoria's Secret #679 Downey rev6 | v80z2 | 2026-11-02 | take-off-metal-frame-drywall_v80z2_VS-Downey-rev6_2026-11-02.zip |

**02-nov: v80wCH** = rama paralela de v80v (no de v80w–v80y de VS) + R80w.1–R80w.40 (corrida Chuze Fitness Austin Bluffs; ver tools/CAMBIOS_tools_v80w.md dentro del zip): arranque / inventario con title blocks de 3 dígitos y sufijo, escala por rótulo de cada hoja, cierre global obligatorio contra la planta general (walls entre plantas ampliadas), MR por nota de wet rooms del set, top track por alcance a estructura, existing walls board-only con markup, tornillería / ductos excluidos en canon. Suite 30/30 OK. **PENDIENTE: unir con v80y (R80e.98–115) en la próxima versión** — los nombres de archivo CAMBIOS_tools_v80w.md coinciden en ambas ramas pero el contenido es distinto.

| Chuze Fitness Austin Bluffs (Hilbers / NNI) FINAL (41 RFI cerrados por decisión del estimador 2-nov, auditor 8/8, cobertura 100 %, REGLAS OK, back-check registrado) | v80wCH | 2026-11-02 | take-off-metal-frame-drywall_v80wCH_FINAL-ChuzeAustinBluffs_2026-11-02.zip |

**02-nov: v80z3** = v80z2 + R80e.118 (demo: markup de línea markups_demo.py, alturas buscadas en todas las hojas, cruce demo vs floor plan; R-ALC-06).

| Victoria's Secret #679 Downey rev7 | v80z3 | 2026-11-02 | take-off-metal-frame-drywall_v80z3_VS-Downey-rev7_2026-11-02.zip |

## Skill de órdenes del usuario (se instala aparte, siempre activo)
| jc-hunter-ordenes | v1 | 2026-11-02 | jc-hunter-ordenes_v1_2026-11-02.zip | Todas las órdenes del usuario desde el día 1 + proceso de mejora continua + verificar_version.py (compuerta: el skill de arranque debe contener todas las reglas acumuladas; v80z3 falla con 168 faltantes). Se actualiza cada vez que se agrega una orden. |

**02-nov: v81cf** = UNIÓN v80wCH (Chuze) + v80z3 (VS) por merge de 3 vías (ancestro v80v; 9 conflictos resueltos a mano) + R80e.124 (CFA #2284: SHX text, types decimales en inventario_tags, 1/2" gyp board, walls de madera board-only). Suite 30/30; verificar_version.py 417/418 (la única "faltante", BE-109, no existe: falso positivo por la frase "BE-109 does not exist" en VS rev2 PASO12). Arranque de Chick-fil-A #2284 River Point. Si la v81 de la sesión de coordinación sale después, se unen las dos el mismo día.

| Chick-fil-A #2284 River Point (arranque) | v81cf | 2026-11-02 | take-off-metal-frame-drywall_v81cf_CFA-RiverPoint-arranque_2026-11-02.zip |
**02-nov: v80z4** = v80z3 + R80e.119-123 (R-ALC-07 altura de demo a estructura, R-ALC-08 specs siempre, R-ALC-09 / R80e.122 hoja de datos del proyecto + compuerta A_PROYECTO_DATOS y `reglas.py datos`, trazabilidad qty del canon manda). Suite 5/5.

| Victoria's Secret #679 Downey rev8 (specs + hoja de datos) | v80z4 | 2026-11-02 | take-off-metal-frame-drywall_v80z4_VS-Downey-rev8_2026-11-02.zip |

**02-nov: v81cf2 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf + delta de v80z4 (VS rev8: compuerta A_PROYECTO_DATOS en reglas.py, barrido de specs, R80e.121/122/123 de VS; 1 conflicto en trazabilidad.py resuelto uniendo las dos líneas) + tools/correr_banco_familias.py (prueba de regresión del banco). La regla CFA pasó a R80e.124 (VS ya usaba R80e.123). Suite 30/30. Banco: B&N rev13, VS rev8, Chuze FINAL y O'Reilly p1 = 0 familias distintas contra la versión con la que se entregaron. verificar_version.py: 418/419; la única "faltante" es BE-109, que NO existe (falso positivo: el texto "BE-109 does not exist" en vs_downey rev2 PASO12_BIBLIOTECA.md).

| Chick-fil-A #2284 River Point (unión total) | v81cf2 | 2026-11-02 | take-off-metal-frame-drywall_v81cf2_CFA-RiverPoint-unida-z4_2026-11-02.zip |

**02-nov: v81cf3 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf2 + R80e.124/125/126: comparar_extra.py (doble lectura de board-only / cielos / misc / demo), compuerta A_BARRIDO_NO_DIBUJADO en reglas.py (R-ALC-11 / BE-116: renglón en 0 / EXCLUDED por "no dibujado" sin barrido registrado en specs + schedule + hojas S = FALLA) con test_barrido_no_dibujado.py. verificar_version.py: 0 faltantes (425 acumuladas). Suite 31/31. Banco B&N rev13 / VS rev8 / Chuze FINAL: 0 familias distintas; la compuerta nueva no marca nada en B&N rev13.

| Chick-fil-A #2284 River Point (vigente) | v81cf3 | 2026-11-02 | take-off-metal-frame-drywall_v81cf3_CFA-RiverPoint_2026-11-02.zip |
**02-nov: v80z5** = v80z4 + R80e.124 (conflicto plano vs spec = manda el plano con nota de verificación, R-ALC-10; usg_grid channel_molding false; ALC-08 acepta 1/2" MR). Suite 5/5.

| Victoria's Secret #679 Downey rev9 (0 RFI abiertos) | v80z5 | 2026-11-02 | take-off-metal-frame-drywall_v80z5_VS-Downey-rev9_2026-11-02.zip |
