# Archivo de skills por proyecto (no borrar)
Cada proyecto cerrado guarda aquí la versión exacta del skill con la que terminó. El siguiente proyecto arranca desde la última y la mejora.

| Proyecto | Versión | Fecha | Archivo |
|---|---|---|---|
| Bank of America Broomfield | v80h | 2026-10-27 | take-off-metal-frame-drywall_v80h_FINAL-BOA-Broomfield_2026-10-27.zip |
| Barnes & Noble Colorado Springs | v80s | 2026-10-28 | take-off-metal-frame-drywall_v80s_FINAL-BandN-ColoradoSprings_2026-10-28.zip |
| Barnes & Noble Colorado Springs (runner API) | v80t | 2026-10-31 | take-off-metal-frame-drywall_v80t_runner_2026-10-31.zip |
| O'Reilly Evans #1 (prueba ciega, suscripción) | v80u | 2026-10-31 | take-off-metal-frame-drywall_v80u_OReilly_2026-10-31.zip |
| O'Reilly Evans #1 FINAL (rev4, pendiente de calificación del estimador) | v80u | 2026-11-01 | take-off-metal-frame-drywall_v80u_FINAL-OReilly_2026-11-01.zip |

**VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO: la última unida (hoy v81cf20 = v81cf19 + R80e.137 jambs de furring; antes v81cf19 = v81cf18 + R80e.136 revision_markups.py; antes v81cf18: v81cf17 + parche RCP de Chuze R80f.13–R80f.16; verificada 0 faltantes de 478).** v80s queda como referencia de exactitud (B&N rev13), no como versión de arranque (BE-115).
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

**02-nov: v81cf** = UNIÓN v80wCH (Chuze) + v80z3 (VS) por merge de 3 vías (ancestro v80v; 9 conflictos resueltos a mano) + R80f.1 (CFA #2284: SHX text, types decimales en inventario_tags, 1/2" gyp board, walls de madera board-only). Suite 30/30; verificar_version.py 417/418 (la única "faltante", BE-109, no existe: falso positivo por la frase "BE-109 does not exist" en VS rev2 PASO12). Arranque de Chick-fil-A #2284 River Point. Si la v81 de la sesión de coordinación sale después, se unen las dos el mismo día.

| Chick-fil-A #2284 River Point (arranque) | v81cf | 2026-11-02 | take-off-metal-frame-drywall_v81cf_CFA-RiverPoint-arranque_2026-11-02.zip |
**02-nov: v80z4** = v80z3 + R80e.119-123 (R-ALC-07 altura de demo a estructura, R-ALC-08 specs siempre, R-ALC-09 / R80e.122 hoja de datos del proyecto + compuerta A_PROYECTO_DATOS y `reglas.py datos`, trazabilidad qty del canon manda). Suite 5/5.

| Victoria's Secret #679 Downey rev8 (specs + hoja de datos) | v80z4 | 2026-11-02 | take-off-metal-frame-drywall_v80z4_VS-Downey-rev8_2026-11-02.zip |

**02-nov: v81cf2 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf + delta de v80z4 (VS rev8: compuerta A_PROYECTO_DATOS en reglas.py, barrido de specs, R80e.121/122/123 de VS; 1 conflicto en trazabilidad.py resuelto uniendo las dos líneas) + tools/correr_banco_familias.py (prueba de regresión del banco). La regla CFA pasó a R80f.1 (espacio propio de CFA; VS usa R80e.123+). Suite 30/30. Banco: B&N rev13, VS rev8, Chuze FINAL y O'Reilly p1 = 0 familias distintas contra la versión con la que se entregaron. verificar_version.py: 418/419; la única "faltante" es BE-109, que NO existe (falso positivo: el texto "BE-109 does not exist" en vs_downey rev2 PASO12_BIBLIOTECA.md).

| Chick-fil-A #2284 River Point (unión total) | v81cf2 | 2026-11-02 | take-off-metal-frame-drywall_v81cf2_CFA-RiverPoint-unida-z4_2026-11-02.zip |

**02-nov: v81cf3 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf2 + R80f.1/2/3: comparar_extra.py (doble lectura de board-only / cielos / misc / demo), compuerta A_BARRIDO_NO_DIBUJADO en reglas.py (R-ALC-11 / BE-116: renglón en 0 / EXCLUDED por "no dibujado" sin barrido registrado en specs + schedule + hojas S = FALLA) con test_barrido_no_dibujado.py. verificar_version.py: 0 faltantes (425 acumuladas). Suite 31/31. Banco B&N rev13 / VS rev8 / Chuze FINAL: 0 familias distintas; la compuerta nueva no marca nada en B&N rev13.

| Chick-fil-A #2284 River Point (vigente) | v81cf3 | 2026-11-02 | take-off-metal-frame-drywall_v81cf3_CFA-RiverPoint_2026-11-02.zip |
**02-nov: v80z5** = v80z4 + R80e.124 (conflicto plano vs spec = manda el plano con nota de verificación, R-ALC-10; usg_grid channel_molding false; ALC-08 acepta 1/2" MR). Suite 5/5.

| Victoria's Secret #679 Downey rev9 (0 RFI abiertos) | v80z5 | 2026-11-02 | take-off-metal-frame-drywall_v80z5_VS-Downey-rev9_2026-11-02.zip |

**02-nov (tarde): v80wCH2** = v80wCH + R80w.41–R80w.49 (barrido de specs R-ALC-08, hoja de datos R-ALC-09, no-dibujado R-ALC-11, notas de decisión por renglón, renglón sin hoja = falla). Suite 36/36 OK. Misma nota: rama paralela de v80v, PENDIENTE unir con v80y.

| Chuze Fitness Austin Bluffs FINAL3 (RFI-S01..S03 opción A; specs aplicadas; auditor 8/8; REGLAS OK; back-check registrado) | v80wCH2 | 2026-11-02 | take-off-metal-frame-drywall_v80wCH2_FINAL3-ChuzeAustinBluffs_2026-11-02.zip |

**02-nov: v81cf4 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf3 + v80wCH2 (Chuze FINAL3: R80w.41–49, merge de 3 vías con ancestro v80wCH; 5 conflictos) + v80z5 (VS rev9: R80e.124 de VS, R-ALC-10, usg_grid channel_molding; ancestro v80z4; 2 conflictos). Las reglas de CFA pasan a su espacio propio R80f.1–3 (antes R80e.124/125/126; alias en referencias/INDICE_REGLAS_ACUMULADAS.md). verificar_version.py: 0 faltantes (438). Suite 37/37. Banco: B&N rev13, VS rev9, Chuze FINAL3, O'Reilly p1 = 0 familias distintas.

| Chick-fil-A #2284 River Point | v81cf4 | 2026-11-02 | take-off-metal-frame-drywall_v81cf4_CFA-RiverPoint_2026-11-02.zip |

**02-nov: v81cf5 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf4 + VS rev10 R80e.127 (R-ALC-11 / BE-VS-10: lateral bracing de ceilings cargado; compuerta A_NO_DIBUJADO sobre cierres de RFI; familias EMT compression strut 1.5" / 1.25" dia x 20 GA (K/A12.02), compra stick 10 ft; trazabilidad: track 'other', cement board y renglón en 0 con RFI de la tool citan su hoja — pasa R80w.48) + arreglo: referencias/INDICE_REGLAS_ACUMULADAS.md sin encabezado (con encabezado hacía fallar reglas.py compuerta: 'regla sin clasificar'). Suite 37/37. Banco B&N rev13 / Chuze / O'Reilly / CFA / VS rev9: 0 familias distintas contra v81cf4. VS rev10 corrido con v81cf5: REGLAS OK, cobertura 334/334.

| Victoria's Secret #679 Downey rev10 | v81cf5 | 2026-11-02 | take-off-metal-frame-drywall_v81cf5_VS-Downey-rev10_2026-11-02.zip |

**02-nov: v81cf6 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf5 + R80e.129 (constants.addl_head_track_openings_extra: head track de openings_extra sin fuente = supuesto conservador CARGADO, R-ALC-11). Suite 37/37. Banco B&N / Chuze / O'Reilly / CFA / VS rev9: 0 familias distintas. verificar_version.py: 0 faltantes (447).

| Victoria's Secret #679 Downey rev11 (vigente; 0 RFI abiertos) | v81cf6 | 2026-11-02 | take-off-metal-frame-drywall_v81cf6_VS-Downey-rev11_2026-11-02.zip |

**02-nov: v81cf7 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf6 (VS rev11) + R80f.4 (BE-CF14: accesorios.BOARD_DRIVER con 1/2" gyp MR y 5/8" foil-backed; test_board_driver.py). verificar_version.py 0 faltantes (449). Suite 38/38. Banco vs v81cf6: B&N rev13 / Chuze FINAL3 / O'Reilly p1 = 0 diferencias; VS rev12 y CFA rev2 cambian SOLO joint compound / joint tape (corrección BE-CF14: VS +76.10 lb / +391.09 LF). CFA #2284 rev2 armado con v81cf7.

| Chick-fil-A #2284 River Point rev2 (vigente) | v81cf7 | 2026-11-02 | take-off-metal-frame-drywall_v81cf7_CFA-RiverPoint-rev2_2026-11-02.zip |

| Victoria's Secret #679 Downey rev13 (0 RFI abiertos; corrido con v81cf7 de CFA: 0 familias distintas, REGLAS OK) | v81cf7 | 2026-11-02 | take-off-metal-frame-drywall_v81cf7_CFA-RiverPoint-rev2_2026-11-02.zip |

**02-nov: v81cf8 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf7 + R80f.5 (BE-CF15: rótulo del Z-furring por tamaño impreso; board key "5/8 ceiling sag-resistant"; setting-type joint compound en LB; yields sin waste; SUBTOTAL OTHER FRAMING; sello en <excel>.sello.json → el libro tiene exactamente las 6 hojas; Excel viejo con hoja _reglas sigue pasando). 4 tests nuevos. verificar_version.py 0 faltantes (451). Suite 42/42. Banco vs v81cf7: B&N rev13, VS rev13, Chuze FINAL3, O'Reilly p1 = 0 diferencias. CFA #2284 FINAL rev3 con REGLAS OK (845, 0 fallas), BITACORA OK (17 tools + back-check), ETAPAS PASA.

| Chick-fil-A #2284 River Point FINAL rev3 (vigente) | v81cf8 | 2026-11-02 | take-off-metal-frame-drywall_v81cf8_FINAL-CFA-RiverPoint-rev3_2026-11-02.zip |

**02-nov: v81cf9 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf8 + R80e.131 (R-ALC-12: compression struts = metal stud 3-5/8"; compuerta A_STRUT_STUD; test_strut_stud.py) + R80e.127 / R80e.129 con encabezado y clasificación (A_NO_DIBUJADO ahora sí corre; BE-VS-11). Suite 43/43. Banco B&N / Chuze / O'Reilly / CFA: 0 familias distintas. VS rev13 con EMT falla A_STRUT_STUD (prueba); VS rev14 REGLAS OK. verificar_version.py: 0 faltantes (456).

| Victoria's Secret #679 Downey rev14 (vigente; 0 RFI abiertos) | v81cf9 | 2026-11-02 | take-off-metal-frame-drywall_v81cf9_VS-Downey-rev14_2026-11-02.zip |

**03-nov: v81cf10 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf9 (VS rev14) + R80f.6 (BE-CF16, usuario 3-nov: ningún RFI abierto sin barrido completo del set; compuerta A_RFI_BARRIDO en reglas.py + test_rfi_barrido.py). verificar_version.py 0 faltantes (459, incluye BE-117 de la maestra). Suite 44/44. Solo agrega una compuerta (sin cambio de cantidades).

| Chick-fil-A #2284 River Point rev4 (vigente) | v81cf10 | 2026-11-03 | take-off-metal-frame-drywall_v81cf10_CFA-RiverPoint-rev4_2026-11-03.zip |

**03-nov: v81cf11 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf10 + R80f.7 (BE-117, usuario, INVIOLABLE: compuerta de entrega A_MARKUPS_EXCEL + tools/verificar_markups_excel.py — cada annot TYPE·LF·H·SF·DETAIL·Wall ID = Excel, /Measure = escala impresa de la hoja, Length vs LF ≤ 0.5 % o causa escrita, toda hoja con elementos marcada; test_markups_excel.py). CAMBIOS_tools_v70..v77 unidos en tools/CAMBIOS_HISTORIAL_tools_v70_a_v77.md (191 archivos < 200). verificar_version.py 0 faltantes (460). Suite 45/45. Banco B&N / VS / Chuze / O'Reilly = 0 diferencias.

| Chick-fil-A #2284 River Point rev4 (vigente) | v81cf11 | 2026-11-03 | take-off-metal-frame-drywall_v81cf11_CFA-RiverPoint-rev4_2026-11-03.zip |

**03-nov: v81cf12 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf11 + BE-117b–f (la v81cf11 archivada no tenía los arreglos de tool que la corrida rev4 de CFA hizo para que la compuerta A_MARKUPS_EXCEL quede en verde: SF del markup = board SF del Excel; slip / deflection track con la pata impresa; cada renglón del Material Summary cita todas sus hojas; breakdown de Level 5 y 1/2" gyp por ID). 195 archivos. Suite 48/48. verificar_version.py 0 faltantes. Banco B&N / VS / Chuze / O'Reilly = 0 diferencias. CFA #2284 rev4: verificar_markups_excel 121/121 OK.

| Chick-fil-A #2284 River Point rev4 FINAL (vigente) | v81cf12 | 2026-11-03 | take-off-metal-frame-drywall_v81cf12_CFA-RiverPoint-rev4_2026-11-03.zip |

**03-nov: v81cf13 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf12 + parche de Chuze (BE-117g: verificar_markups_excel entiende renglones unidos "A+B"; markups_bluebeam: leyenda por hoja marcada, Length = LF impreso, DETAIL de types con guion, resumen de markups vigente; plantilla_excel: exención de idioma en PROJECT DATA; auditoria_entrega.py) con ids de Chuze renumerados a R80f.8–R80f.11 (merge 3 vías, base = v81cf10 archivada; 2 conflictos en markups_bluebeam resueltos a favor de BE-117b SF = board SF). 198 archivos. Suite 50/50. verificar_version.py 0 faltantes (463). Banco B&N rev13 / VS rev14 / Chuze / O'Reilly / CFA rev4 = 0 diferencias. CFA rev4: verificar_markups_excel 121/121 OK.

| Chick-fil-A #2284 River Point rev4 | v81cf13 | 2026-11-03 | take-off-metal-frame-drywall_v81cf13_CFA-RiverPoint-rev4_2026-11-03.zip |

**03-nov: v81cf14 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf13 (CFA) + R80e.132 (BE-VS-12: framed soffit una sola vez; compuerta A_SOFFIT_DOBLE; test_soffit_doble.py) + R80e.133 (BE-VS-13: markups SF desde board_out = Excel exacto; renglón unido "A+B" cuadra H ponderado por LF). Suite 51/51. Banco B&N / Chuze / O'Reilly / CFA: 0 familias distintas. VS rev15: REGLAS OK, markups 118/118 OK.

| Victoria's Secret #679 Downey rev15 | v81cf14 | 2026-11-03 | take-off-metal-frame-drywall_v81cf14_VS-Downey-rev15_2026-11-03.zip |

**03-nov: v81cf15 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf14 + R80e.134 (BE-VS-14: markups_demo con el formato del verificador, DEMO-<id del Excel>, DETAIL N/HOJA, page label; nota impresa de EQ studs cargada por programa). Suite 51/51. Banco B&N / Chuze / O'Reilly / CFA: 0 familias distintas. VS rev16 FINAL: REGLAS OK, markups 178/178 (A02.01 + A01.01).

| Victoria's Secret #679 Downey rev16 FINAL | v81cf15 | 2026-11-03 | take-off-metal-frame-drywall_v81cf15_VS-Downey-rev16_2026-11-03.zip |

**03-nov: v81cf16 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf15 + R80e.135 (BE-VS-15: verificar_markups_excel FALLA si una hoja con renglones del take-off no tiene markups — ceilings / soffits por rcp_sheet y demolición; tool nueva markups_rcp.py; el runner agrega demo_geom.json y rcp_polys.json del proyecto al PDF de entrega; el verificador elige el renglón del Material Summary cuyo material corresponde al TYPE). Suite 51/51. Banco B&N / Chuze / O'Reilly / CFA: 0 familias distintas. VS rev16 con v81cf16: REGLAS OK, markups 208/208 (A01.01 + A02.01 + A03.01), mismas cantidades. OJO proyectos con ceilings y sin rcp_polys.json: la compuerta ahora falla hasta marcar el RCP.

| Victoria's Secret #679 Downey rev16 FINAL + RCP (vigente) | v81cf16 | 2026-11-03 | take-off-metal-frame-drywall_v81cf16_VS-Downey-rev16-RCP_2026-11-03.zip |

**03-nov: v81cf17 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf16 (VS rev16) + R80f.12 (BE-CF19: verificar_markups_excel toma la hoja de un renglón de demolición de su demo_geom, no de la hoja que cita su altura — en v81cf16 CFA rev4 daba 2 FALLAS falsas "L65" / "S-601"). Tests de CFA unidos en tools/test_cf_pruebas.py (sin quitar ninguna prueba) → 199 archivos. Suite 50/50. verificar_version.py 0 faltantes (474). Banco B&N / VS / Chuze / O'Reilly / CFA rev4 = 0 diferencias. CFA rev4: 121/121 markups OK, 0 fallas.

| Chick-fil-A #2284 River Point rev4 (vigente) | v81cf17 | 2026-11-03 | take-off-metal-frame-drywall_v81cf17_CFA-RiverPoint-rev4_2026-11-03.zip |

| Victoria's Secret #679 Downey rev17 FINAL (ceilings corregidos al RCP; markups 208/208) | v81cf16 | 2026-11-03 | take-off-metal-frame-drywall_v81cf16_VS-Downey-rev16-RCP_2026-11-03.zip |

**03-nov: v81cf18 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf17 + parche RCP de Chuze FINAL5 (R80f.13 markups_rcp multi-hoja con id del ceiling, leyenda y PNG por hoja; R80f.14 buscar_pdf sin distinguir mayúsculas; R80f.15 auditoria_entrega valida polígonos de ceiling vs Material Summary; R80f.16 polígono del ceiling = solo el área con hatch, parte sin hatch ≥ 1 SF = rc 1). Merge 3 vías sin conflictos (base v81cf17); BE-CF19 conservado. Tests nuevos dentro de tools/test_chuze_r80f8_11.py (199 archivos). Suite 50/50. verificar_version.py 0 faltantes (478). Banco B&N rev13 / VS rev17 / Chuze / O'Reilly p1 / CFA rev4 = 0 diferencias. CFA rev4: verificar_markups_excel 121/121, 0 fallas.

| Parche RCP Chuze (vigente) | v81cf18 | 2026-11-03 | take-off-metal-frame-drywall_v81cf18_RCP-Chuze_2026-11-03.zip |

**03-nov: v81cf19 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf18 + R80e.136 (tools/revision_markups.py: revisión rápida de markups vs Excel — LF con escala IMPRESA ±0.5 %, Depth = H exacta, Wall Area, Wall ID / TYPE; tabla VERDE/ROJA en orden del schedule, recorte circulado por fila roja, mapa de alturas por hoja; selftest llamado desde test_markups_excel.py, 200 archivos). Numerada R80e.136 porque R80e.100 ya es de VS (storefront structural framing). + referencias/INDICE_REGLAS_ACUMULADAS.md con BE-118, BE-HF01 y el alias R80e.130 = R80f.4. Suite 50/50. verificar_version.py 0 faltantes (481). Banco B&N / VS / O'Reilly p2 = 0 familias distintas (la tool no toca canon.py). La rama v81cf9a (misma tool sobre v81cf9) se retira del archivo: queda unida aquí.

| O'Reilly Evans #1 revisión rápida de markups (vigente) | v81cf19 | 2026-11-03 | take-off-metal-frame-drywall_v81cf19_OReilly-revision-rapida_2026-11-03.zip |

**03-nov: v81cf20 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf19 + R80e.137 (BE-113, back-check O'Reilly p2: studs_nodos.py jambs = 0 en walls de furring — Z-furring / hat / furring channel —, el jamb del furring es el blocking FRT del detalle; closer.Wall.furring / operación 'R80e.137'; test en test_project_data.py). Suite 50/50. verificar_version.py 0 faltantes. Banco: B&N rev13, VS rev17, Chuze rev3, CFA rev4 = 0 familias distintas vs v81cf19; O'Reilly: referencia actualizada al FINAL p2 entregado (run15) = 0 distintas (Z-furring 2,220.63 LF = back-check).

| O'Reilly Evans #1 FINAL p2 (jambs de furring) (vigente) | v81cf20 | 2026-11-03 | take-off-metal-frame-drywall_v81cf20_OReilly-furring-jambs_2026-11-03.zip |
