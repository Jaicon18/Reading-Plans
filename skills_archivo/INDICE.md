# Archivo de skills por proyecto (no borrar)
Cada proyecto cerrado guarda aquí la versión exacta del skill con la que terminó. El siguiente proyecto arranca desde la última y la mejora.

| Proyecto | Versión | Fecha | Archivo |
|---|---|---|---|
| Bank of America Broomfield | v80h | 2026-10-27 | take-off-metal-frame-drywall_v80h_FINAL-BOA-Broomfield_2026-10-27.zip |
| Barnes & Noble Colorado Springs | v80s | 2026-10-28 | take-off-metal-frame-drywall_v80s_FINAL-BandN-ColoradoSprings_2026-10-28.zip |
| Barnes & Noble Colorado Springs (runner API) | v80t | 2026-10-31 | take-off-metal-frame-drywall_v80t_runner_2026-10-31.zip |
| O'Reilly Evans #1 (prueba ciega, suscripción) | v80u | 2026-10-31 | take-off-metal-frame-drywall_v80u_OReilly_2026-10-31.zip |
| O'Reilly Evans #1 FINAL (rev4, pendiente de calificación del estimador) | v80u | 2026-11-01 | take-off-metal-frame-drywall_v80u_FINAL-OReilly_2026-11-01.zip |

**VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO: la última unida (hoy v81cf29 = v81cf28 (O'Reilly rev6) + BE-CF21 de CFA rev6 (U-117 / U-120 sin falsos positivos, demo de cielo = Polygon, un eje por número), unida 3-way; antes v81cf28 = v81cf27 (CFA rev5 unida) + R80e.153: imagen del Review Item por nombre, R80e.84 ya no la rechaza (BE-132); barrido de tags visual en hoja raster (BE-133); antes v81cf27 = v81cf26 (COORDINACIÓN) + arreglos CFA rev5 + BE-CF20, unida 3-way; antes v81cf26 = v81cf25 + R80e.152: preferencias del día 1 U-114..U-125 / BE-131 con chequeo de fondo en chequeos_biblioteca.py; antes v81cf25 = v81cf24 + R80e.142–R80e.151, arreglos de tool de O'Reilly rev5 (OCR de hojas raster, head track en furring, runner que arranca, chequeos sin falsos positivos OCR; BE-125..BE-130); antes v81cf24 = v81cf23 + R80e.141: tools/chequeos_biblioteca.py, programa de fondo para las 142 reglas que eran programa-pendiente + CE_CALLOUTS U-113 / BE-124; antes v81cf23 = v81cf22 + R80e.139 / BE-121: compuerta_entrega.py + subir_entrega.py + REGLAS_REGISTRO.json + R80e.140 / BE-122 revision_materiales.py; antes v81cf22 = v81cf21 + R80e.138 altura impresa en revision_markups; antes v81cf21 = v81cf20 + R80f.17–R80f.28 tool fixes de HFT Loveland; antes v81cf20 = v81cf19 + R80e.137 jambs de furring; antes v81cf19 = v81cf18 + R80e.136 revision_markups.py; antes v81cf18: v81cf17 + parche RCP de Chuze R80f.13–R80f.16; verificada 0 faltantes de 478).** v80s queda como referencia de exactitud (B&N rev13), no como versión de arranque (BE-115).
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

| Chick-fil-A #2284 River Point | v81cf3 | 2026-11-02 | take-off-metal-frame-drywall_v81cf3_CFA-RiverPoint_2026-11-02.zip |
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

| Chick-fil-A #2284 River Point rev2 | v81cf7 | 2026-11-02 | take-off-metal-frame-drywall_v81cf7_CFA-RiverPoint-rev2_2026-11-02.zip |

| Victoria's Secret #679 Downey rev13 (0 RFI abiertos; corrido con v81cf7 de CFA: 0 familias distintas, REGLAS OK) | v81cf7 | 2026-11-02 | take-off-metal-frame-drywall_v81cf7_CFA-RiverPoint-rev2_2026-11-02.zip |

**02-nov: v81cf8 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf7 + R80f.5 (BE-CF15: rótulo del Z-furring por tamaño impreso; board key "5/8 ceiling sag-resistant"; setting-type joint compound en LB; yields sin waste; SUBTOTAL OTHER FRAMING; sello en <excel>.sello.json → el libro tiene exactamente las 6 hojas; Excel viejo con hoja _reglas sigue pasando). 4 tests nuevos. verificar_version.py 0 faltantes (451). Suite 42/42. Banco vs v81cf7: B&N rev13, VS rev13, Chuze FINAL3, O'Reilly p1 = 0 diferencias. CFA #2284 FINAL rev3 con REGLAS OK (845, 0 fallas), BITACORA OK (17 tools + back-check), ETAPAS PASA.

| Chick-fil-A #2284 River Point FINAL rev3 | v81cf8 | 2026-11-02 | take-off-metal-frame-drywall_v81cf8_FINAL-CFA-RiverPoint-rev3_2026-11-02.zip |

**02-nov: v81cf9 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf8 + R80e.131 (R-ALC-12: compression struts = metal stud 3-5/8"; compuerta A_STRUT_STUD; test_strut_stud.py) + R80e.127 / R80e.129 con encabezado y clasificación (A_NO_DIBUJADO ahora sí corre; BE-VS-11). Suite 43/43. Banco B&N / Chuze / O'Reilly / CFA: 0 familias distintas. VS rev13 con EMT falla A_STRUT_STUD (prueba); VS rev14 REGLAS OK. verificar_version.py: 0 faltantes (456).

| Victoria's Secret #679 Downey rev14 (vigente; 0 RFI abiertos) | v81cf9 | 2026-11-02 | take-off-metal-frame-drywall_v81cf9_VS-Downey-rev14_2026-11-02.zip |

**03-nov: v81cf10 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf9 (VS rev14) + R80f.6 (BE-CF16, usuario 3-nov: ningún RFI abierto sin barrido completo del set; compuerta A_RFI_BARRIDO en reglas.py + test_rfi_barrido.py). verificar_version.py 0 faltantes (459, incluye BE-117 de la maestra). Suite 44/44. Solo agrega una compuerta (sin cambio de cantidades).

| Chick-fil-A #2284 River Point rev4 | v81cf10 | 2026-11-03 | take-off-metal-frame-drywall_v81cf10_CFA-RiverPoint-rev4_2026-11-03.zip |

**03-nov: v81cf11 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf10 + R80f.7 (BE-117, usuario, INVIOLABLE: compuerta de entrega A_MARKUPS_EXCEL + tools/verificar_markups_excel.py — cada annot TYPE·LF·H·SF·DETAIL·Wall ID = Excel, /Measure = escala impresa de la hoja, Length vs LF ≤ 0.5 % o causa escrita, toda hoja con elementos marcada; test_markups_excel.py). CAMBIOS_tools_v70..v77 unidos en tools/CAMBIOS_HISTORIAL_tools_v70_a_v77.md (191 archivos < 200). verificar_version.py 0 faltantes (460). Suite 45/45. Banco B&N / VS / Chuze / O'Reilly = 0 diferencias.

| Chick-fil-A #2284 River Point rev4 | v81cf11 | 2026-11-03 | take-off-metal-frame-drywall_v81cf11_CFA-RiverPoint-rev4_2026-11-03.zip |

**03-nov: v81cf12 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf11 + BE-117b–f (la v81cf11 archivada no tenía los arreglos de tool que la corrida rev4 de CFA hizo para que la compuerta A_MARKUPS_EXCEL quede en verde: SF del markup = board SF del Excel; slip / deflection track con la pata impresa; cada renglón del Material Summary cita todas sus hojas; breakdown de Level 5 y 1/2" gyp por ID). 195 archivos. Suite 48/48. verificar_version.py 0 faltantes. Banco B&N / VS / Chuze / O'Reilly = 0 diferencias. CFA #2284 rev4: verificar_markups_excel 121/121 OK.

| Chick-fil-A #2284 River Point rev4 FINAL | v81cf12 | 2026-11-03 | take-off-metal-frame-drywall_v81cf12_CFA-RiverPoint-rev4_2026-11-03.zip |

**03-nov: v81cf13 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf12 + parche de Chuze (BE-117g: verificar_markups_excel entiende renglones unidos "A+B"; markups_bluebeam: leyenda por hoja marcada, Length = LF impreso, DETAIL de types con guion, resumen de markups vigente; plantilla_excel: exención de idioma en PROJECT DATA; auditoria_entrega.py) con ids de Chuze renumerados a R80f.8–R80f.11 (merge 3 vías, base = v81cf10 archivada; 2 conflictos en markups_bluebeam resueltos a favor de BE-117b SF = board SF). 198 archivos. Suite 50/50. verificar_version.py 0 faltantes (463). Banco B&N rev13 / VS rev14 / Chuze / O'Reilly / CFA rev4 = 0 diferencias. CFA rev4: verificar_markups_excel 121/121 OK.

| Chick-fil-A #2284 River Point rev4 | v81cf13 | 2026-11-03 | take-off-metal-frame-drywall_v81cf13_CFA-RiverPoint-rev4_2026-11-03.zip |

**03-nov: v81cf14 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf13 (CFA) + R80e.132 (BE-VS-12: framed soffit una sola vez; compuerta A_SOFFIT_DOBLE; test_soffit_doble.py) + R80e.133 (BE-VS-13: markups SF desde board_out = Excel exacto; renglón unido "A+B" cuadra H ponderado por LF). Suite 51/51. Banco B&N / Chuze / O'Reilly / CFA: 0 familias distintas. VS rev15: REGLAS OK, markups 118/118 OK.

| Victoria's Secret #679 Downey rev15 | v81cf14 | 2026-11-03 | take-off-metal-frame-drywall_v81cf14_VS-Downey-rev15_2026-11-03.zip |

**03-nov: v81cf15 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf14 + R80e.134 (BE-VS-14: markups_demo con el formato del verificador, DEMO-<id del Excel>, DETAIL N/HOJA, page label; nota impresa de EQ studs cargada por programa). Suite 51/51. Banco B&N / Chuze / O'Reilly / CFA: 0 familias distintas. VS rev16 FINAL: REGLAS OK, markups 178/178 (A02.01 + A01.01).

| Victoria's Secret #679 Downey rev16 FINAL | v81cf15 | 2026-11-03 | take-off-metal-frame-drywall_v81cf15_VS-Downey-rev16_2026-11-03.zip |

**03-nov: v81cf16 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf15 + R80e.135 (BE-VS-15: verificar_markups_excel FALLA si una hoja con renglones del take-off no tiene markups — ceilings / soffits por rcp_sheet y demolición; tool nueva markups_rcp.py; el runner agrega demo_geom.json y rcp_polys.json del proyecto al PDF de entrega; el verificador elige el renglón del Material Summary cuyo material corresponde al TYPE). Suite 51/51. Banco B&N / Chuze / O'Reilly / CFA: 0 familias distintas. VS rev16 con v81cf16: REGLAS OK, markups 208/208 (A01.01 + A02.01 + A03.01), mismas cantidades. OJO proyectos con ceilings y sin rcp_polys.json: la compuerta ahora falla hasta marcar el RCP.

| Victoria's Secret #679 Downey rev16 FINAL + RCP | v81cf16 | 2026-11-03 | take-off-metal-frame-drywall_v81cf16_VS-Downey-rev16-RCP_2026-11-03.zip |

**03-nov: v81cf17 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf16 (VS rev16) + R80f.12 (BE-CF19: verificar_markups_excel toma la hoja de un renglón de demolición de su demo_geom, no de la hoja que cita su altura — en v81cf16 CFA rev4 daba 2 FALLAS falsas "L65" / "S-601"). Tests de CFA unidos en tools/test_cf_pruebas.py (sin quitar ninguna prueba) → 199 archivos. Suite 50/50. verificar_version.py 0 faltantes (474). Banco B&N / VS / Chuze / O'Reilly / CFA rev4 = 0 diferencias. CFA rev4: 121/121 markups OK, 0 fallas.

| Chick-fil-A #2284 River Point rev4 | v81cf17 | 2026-11-03 | take-off-metal-frame-drywall_v81cf17_CFA-RiverPoint-rev4_2026-11-03.zip |

| Victoria's Secret #679 Downey rev17 FINAL (ceilings corregidos al RCP; markups 208/208) | v81cf16 | 2026-11-03 | take-off-metal-frame-drywall_v81cf16_VS-Downey-rev16-RCP_2026-11-03.zip |

**03-nov: v81cf18 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf17 + parche RCP de Chuze FINAL5 (R80f.13 markups_rcp multi-hoja con id del ceiling, leyenda y PNG por hoja; R80f.14 buscar_pdf sin distinguir mayúsculas; R80f.15 auditoria_entrega valida polígonos de ceiling vs Material Summary; R80f.16 polígono del ceiling = solo el área con hatch, parte sin hatch ≥ 1 SF = rc 1). Merge 3 vías sin conflictos (base v81cf17); BE-CF19 conservado. Tests nuevos dentro de tools/test_chuze_r80f8_11.py (199 archivos). Suite 50/50. verificar_version.py 0 faltantes (478). Banco B&N rev13 / VS rev17 / Chuze / O'Reilly p1 / CFA rev4 = 0 diferencias. CFA rev4: verificar_markups_excel 121/121, 0 fallas.

| Parche RCP Chuze | v81cf18 | 2026-11-03 | take-off-metal-frame-drywall_v81cf18_RCP-Chuze_2026-11-03.zip |

**03-nov: v81cf19 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf18 + R80e.136 (tools/revision_markups.py: revisión rápida de markups vs Excel — LF con escala IMPRESA ±0.5 %, Depth = H exacta, Wall Area, Wall ID / TYPE; tabla VERDE/ROJA en orden del schedule, recorte circulado por fila roja, mapa de alturas por hoja; selftest llamado desde test_markups_excel.py, 200 archivos). Numerada R80e.136 porque R80e.100 ya es de VS (storefront structural framing). + referencias/INDICE_REGLAS_ACUMULADAS.md con BE-118, BE-HF01 y el alias R80e.130 = R80f.4. Suite 50/50. verificar_version.py 0 faltantes (481). Banco B&N / VS / O'Reilly p2 = 0 familias distintas (la tool no toca canon.py). La rama v81cf9a (misma tool sobre v81cf9) se retira del archivo: queda unida aquí.

| O'Reilly Evans #1 revisión rápida de markups | v81cf19 | 2026-11-03 | take-off-metal-frame-drywall_v81cf19_OReilly-revision-rapida_2026-11-03.zip |

**03-nov: v81cf20 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf19 + R80e.137 (BE-113, back-check O'Reilly p2: studs_nodos.py jambs = 0 en walls de furring — Z-furring / hat / furring channel —, el jamb del furring es el blocking FRT del detalle; closer.Wall.furring / operación 'R80e.137'; test en test_project_data.py). Suite 50/50. verificar_version.py 0 faltantes. Banco: B&N rev13, VS rev17, Chuze rev3, CFA rev4 = 0 familias distintas vs v81cf19; O'Reilly: referencia actualizada al FINAL p2 entregado (run15) = 0 distintas (Z-furring 2,220.63 LF = back-check).

| O'Reilly Evans #1 FINAL p2 (jambs de furring) | v81cf20 | 2026-11-03 | take-off-metal-frame-drywall_v81cf20_OReilly-furring-jambs_2026-11-03.zip |

**03-nov: v81cf21 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf20 + tool fixes de Harbor Freight Loveland (BE-HF1..BE-HF17 de TOOL_LIMITS_CALC; errores BE-HF06..BE-HF17 en la biblioteca) como R80f.17–R80f.28: R80f.17 hat channel vertical con rótulo impreso; R80f.18 alias "FRP panels" en misc_items; R80f.19 C.R. bracing según la condición impresa (furring = 0, solo walls > altura mínima, compuerta A_BRACING con el spacing impreso); R80f.20 vigas_sobre_walls --min-size; R80f.21 box beams de misc en A_HEADER_LF y en el desglose; R80f.22 desgloses (track por tamaño con designación, hoja suelta citada, sill por abertura + nota de redondeo); R80f.23 markups (0 SF en walls sin board, demo "2 faces x 1 layer", leyenda en orden del schedule); R80f.24 auditoria_entrega --rfis-abiertos + causas escritas; R80f.25 braces to structure + spacing bar (Spazzer) cargados; R80f.26 track de bulkhead por tamaño / tipo; R80f.27 una fila de Partition Takeoff por Wall ID + bloque BULKHEAD-<tag>; R80f.28 regla BE-HF01 (el brief no resume wall types desde texto extraído). Merge 3 vías sin conflictos (base v81cf18; v81cf20 no tocaba los 10 archivos de HFT). Compuertas registradas en reglas_clasificacion (R80f.19 = A_BRACING, R80f.21 = A_HEADER_LF). Los 11 tests de HFT unidos en tools/test_hft_loveland.py y CAMBIOS_tools_v80x / v81cf8 / v81cf11 unidos en tools/CAMBIOS_HISTORIAL_tools_v80x_a_v81cf21.md (sin quitar nada) → 199 archivos (v81cf20 tenía 200). Suite 51/51. verificar_version.py 0 faltantes (520). Banco B&N rev13 / VS rev17 / Chuze (rev3 y vigente) / O'Reilly p1 / O'Reilly p2 / CFA rev4 = 0 familias distintas vs v81cf20 (las familias nuevas de braces to structure solo se activan con braces_to_structure en el canon). No se crea v81cf19 nueva: ese número ya es de O'Reilly (BE-115, una sola línea).

| Harbor Freight Loveland (tool fixes de la corrida) | v81cf21 | 2026-11-03 | take-off-metal-frame-drywall_v81cf21_HFT-Loveland_2026-11-03.zip |

**03-nov: v81cf22 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** = v81cf21 (HFT) + R80e.138 (BE-119: revision_markups.py compara Depth contra la altura IMPRESA de la fuente — A.F.F., elevaciones, F.F. datum, cota — no contra la H del Excel; sin altura impresa / supuesto de RFI = ÁMBAR con hojas citadas; mapa de alturas con hoja fuente; selftest que falla si la altura impresa difiere) + BE-120 y BE-HF18 en referencias. Suite 51/51. verificar_version.py 0 faltantes. Banco B&N / VS rev17 / Chuze / CFA rev4 / O'Reilly p2 = 0 familias distintas vs v81cf21.

| O'Reilly Evans #1 revisión rápida v2 (altura impresa) | v81cf22 | 2026-11-03 | take-off-metal-frame-drywall_v81cf22_OReilly-altura-impresa_2026-11-03.zip |

**03-nov: v81cf23 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** (COORDINACIÓN, BE-121 "las reglas las hace cumplir un programa") = v81cf22 + tools/compuerta_entrega.py (ENTREGA_OK.json: PASS / FAIL / AMBER por regla; incluye BE-119 altura impresa y BE-120 términos de cada RFI abierto en el texto completo del set) + tools/subir_entrega.py (única subida a Drive; se niega sin ENTREGA_OK.json verde y vigente o con la carpeta fuera de Claude outputs de la raíz) + REGLAS_REGISTRO.json (289 reglas: U-001..U-111, R-ALC-01..12, BE-*; categoría y chequeo + test) + R80e.140 / BE-122 (tools/revision_materiales.py de la sesión O'Reilly = chequeo CE_MATERIALES_SCHEDULE: materiales vs Partition Type Schedule con lectura independiente fichas.json) + tools/test_compuerta_entrega.py (incluye el test de revision_materiales) + arreglo revision_markups (elevación sola != altura). CAMBIOS_* de tools unidos en tools/CAMBIOS_HISTORIAL_tools.md (199 archivos < 200). Registro: 86 programa con chequeo + test / 38 conducta / 23 históricas / 142 programa-pendiente (con motivo). Motivo de VIGENTE: verificar_version.py 0 faltantes + registro sin reglas "programa" sin chequeo/test; suite 52/52; banco B&N / VS rev17 / Chuze / CFA / O'Reilly / HFT = 0 familias distintas (la compuerta no cambia cantidades).

| Compuerta de entrega (COORDINACIÓN, BE-121) | v81cf23 | 2026-11-03 | take-off-metal-frame-drywall_v81cf23_compuerta-entrega_2026-11-03.zip |

**03-nov: v81cf24 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** (COORDINACIÓN, orden del usuario "142 todavía sin programa ... haz los programas" + U-113 / BE-124 CE_CALLOUTS) = v81cf23 + R80e.141: tools/chequeos_biblioteca.py (118 chequeos de fondo que cubren las 142 reglas programa-pendiente: 127 BE + U-017 / U-026 / U-034 / U-035 / U-037 / U-043 / U-051 / U-057 / U-058 / U-079 / U-081 / U-082 / R-ALC-02 / R-ALC-04 / R-ALC-10) + CE_CALLOUTS (toda burbuja N/HOJA de las hojas del trade seguida por cierre transitivo hasta el último detalle, citada o fuera de alcance con motivo; detalle / hoja inexistente reportado), todos cableados en compuerta_entrega.py (una línea por regla en ENTREGA_OK.json); verificar_version.py revisar_skill (BE-87 / BE-VS-11) y revisar_banco (U-043 / BE-94); BE-CF08 = reglas.py A_CATALOGO con test; runner/run_takeoff.py con entorno limpio (BE-91). Test tools/test_chequeos_biblioteca.py: por cada chequeo un caso que reproduce el error original (FAIL) y su arreglo (PASS). test_mr_typex.py y test_coord_rango.py unidos sin cambios en test_chuze_r80f8_11.py (199 archivos). Registro: 230 programa / 40 conducta / 23 históricas / 0 programa-pendiente (+ U-112 / BE-123 conducta, U-113 / BE-124 programa). Suite 51/51. verificar_version.py 0 faltantes. Banco B&N / VS rev17 / HFT / O'Reilly = 0 familias distintas vs v81cf23 (canon.py idéntico; los chequeos solo leen; BOA rev1 falla igual en las dos por su canon viejo). Motivo de VIGENTE: 0 programa-pendiente + suite verde + banco = 0 diferencias.

| Programas de la biblioteca + CE_CALLOUTS (COORDINACIÓN) | v81cf24 | 2026-11-03 | take-off-metal-frame-drywall_v81cf24_programas-biblioteca_2026-11-03.zip |

**03-nov: v81cf25 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** (O'Reilly rev5, orden del usuario U-112 vía COORDINACIÓN) = v81cf24 + R80e.142–R80e.151: texto del set con OCR en hojas raster + número de hoja del title block + páginas en blanco (R80e.151, BE-125); altura_impresa "EL" sin punto / PANEL (R80e.142); revision_markups = BE-117 (SF board, length_cause AMBER, R80e.143); head track adicional = 0 en walls de furring (R80e.144, BE-126); 8 chequeos de la biblioteca sin falsos positivos en sets OCR (R80e.145, BE-129); reconcile / completitud con framing exterior sin tag (R80e.146); runner: comparar_extra.py (R80e.147) y tools/ en el path — v81cf24 no arrancaba (R80e.148, BE-130); sin id interno en el Excel (R80e.149); /Measure de hoja raster = calibración documentada (R80e.150). Motivo de VIGENTE: verificar_version 0 faltantes (cada regla programa con chequeo + test); suite 51/51; banco B&N rev13 / VS / Chuze / CFA / HFT rev3 = 0 familias distintas; O'Reilly p1 y p2 = 1 (additional head track 32.73 -> 0, el arreglo); 199 archivos. Compuerta de entrega O'Reilly rev5: PASS 136 / AMBER 4 / FAIL 0.
| O'Reilly rev5 FINAL — compuerta de entrega en verde | v81cf25 | 2026-11-03 | take-off-metal-frame-drywall_v81cf25_OReilly-rev5_2026-11-03.zip |

**03-nov: v81cf26 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** (COORDINACIÓN, queja del usuario "la regla de las burbujas la di en los primeros días y nunca se hizo cumplir") = v81cf25 (O'Reilly rev5) + R80e.152: las 12 preferencias de cuenta del día 1 = reglas INVIOLABLES U-114..U-125 (BE-131) con chequeo de fondo en tools/chequeos_biblioteca.py, cableados en compuerta_entrega.py: u_114 honestidad dimensional #0 (estado + hoja / operación por número, caras y cielos incluidos), u_115 N/HOJA por partida, u_116 ningún supuesto sin RFI / precedente / código, u_117 barrido por tag (inventario con PNG circulado y verificado, cada ubicación contada), u_118 evidencia circulada (walls, RFI abiertos, Review Items), u_119 inglés, u_120 ejes, u_121 Subject / Page Label / Length / Depth en markups, u_125 términos del trade en inglés; CE_SIN_DOLARES ahora mira también el Excel y los markups (U-123); U-115 / U-121 / U-122 mapeadas además a CE_CALLOUTS / CE_FORMATO_EXCEL / CE_AUDITORIA / CE_MARKUPS_EXCEL / CE_DRIVE_PARENT; U-124 conducta. runner/evidencia.py circula lo citado en la hoja y completa tag_ids con las ubicaciones del inventario. Unida por merge de 3 vías con v81cf25 (chequeos_biblioteca.py / compuerta_entrega.py / test_compuerta_entrega.py sin conflicto). Registro: 246 programa / 43 conducta / 23 históricas / 0 programa-pendiente. Suite 51/51. verificar_version.py 0 faltantes. Banco B&N / CFA / Chuze / HFT / O'Reilly = 0 familias distintas vs v81cf25 (canon.py idéntico; los chequeos solo leen). 199 archivos. Motivo de VIGENTE: preferencias del día 1 con programa + suite verde + banco = 0 diferencias.

| Preferencias del día 1 con programa (COORDINACIÓN) | v81cf26 | 2026-11-03 | take-off-metal-frame-drywall_v81cf26_preferencias-dia1_2026-11-03.zip |

**03-nov: v81cf27 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** (CFA #2284 rev5) = v81cf26 de COORDINACIÓN (preferencias del día 1) + arreglos de la corrida CFA rev5 (texto_set hojas rotadas / pN-vector, trazabilidad sill track, sin id interno R80e.137 en el Excel, canon abut contra existing_walls = 0 studs, revision_markups etiquetas / board SF / altura derivada re-hecha por programa después de las elevaciones impresas R80e.142, revision_materiales driver de compound / tape, chequeos_biblioteca BE-102 / BE-15 / BE-14 sin falsos positivos) + BE-CF20 (verificar_version falla si la versión vigente tiene dos zips). Las CFA v81cf25 / v81cf26 locales nunca se archivaron (chocaban con las de O'Reilly / COORDINACIÓN; su contenido entero está en v81cf27). Suite 51/51. Banco vs v81cf26 COORDINACIÓN: B&N rev13 / VS rev17 / Chuze rev3 / Chuze / O'Reilly p1 / O'Reilly p2 / HFT rev3 / CFA rev4 = 0 familias distintas. Compuerta de entrega CFA rev5 re-corrida con la unión CFA: 137 PASS / 3 AMBER / 0 FAIL = igual.
| CFA #2284 River Point rev5 — compuerta de entrega en verde, unida | v81cf27 | 2026-11-03 | take-off-metal-frame-drywall_v81cf27_CFA-rev5-unida_2026-11-03.zip |

**04-nov: v81cf28 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** (O'Reilly rev6, U-112 vía COORDINACIÓN) = v81cf27 (CFA rev5 unida) + R80e.153 (plantilla_excel: columna Image de Review Items = nombre de la imagen circulada; verificar_texto_cliente la acepta, lo demás sigue igual; BE-132) + BE-133 (barrido visual de tags en hoja raster, formato de inventario_tags). Unida 3-way (base v81cf26). Motivo de VIGENTE: verificar_version 0 faltantes; suite 51/51; banco B&N rev13 / VS / Chuze / CFA / O'Reilly p1 / HFT rev3 / O'Reilly rev6 = 0 familias distintas; 199 archivos. Compuerta de entrega O'Reilly rev6 con v81cf26 y con v81cf28: PASS 145 / AMBER 4 / FAIL 0.
| O'Reilly rev6 FINAL — compuerta en verde (vigente) | v81cf28 | 2026-11-04 | take-off-metal-frame-drywall_v81cf28_OReilly-rev6_2026-11-04.zip |

**04-nov: v81cf29 = VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO** (CFA #2284 rev6) = v81cf28 de O'Reilly rev6 (R80e.153 nombre de la imagen en Review Items) + BE-CF21 de CFA rev6: chequeos_biblioteca u_117 lee existing_walls[].tag_ids y tags_descartados; u_120 mira solo el Wall ID del markup; markups_demo: cielo demolido = Polygon de área, polilínea que dobla > 60° = una pieza por eje; plantilla_excel acepta además la ruta entregada proceso/review_img | rfi_img en Review Items; verificar_markups_excel reconoce un elemento por sus piezas. Regla de datos: un eje por número. La CFA v81cf28 local nunca se archivó en el remoto (chocaba con la de O'Reilly, BE-CF20); su contenido entero está en v81cf29. Test tools/test_cf_pruebas.py::test_cf_rev6_dia1. Suite 51/51, 199 archivos. Banco vs v81cf28 O'Reilly: B&N rev13 / VS rev17 / Chuze rev3 / Chuze / O'Reilly p1 / O'Reilly p2 / HFT rev3 / CFA rev4 = 0 familias distintas. Compuerta CFA rev6 re-corrida con v81cf29: 146 PASS / 3 AMBER / 0 FAIL = igual.
| CFA #2284 River Point rev6 — compuerta de las preferencias del día 1 en verde, unida (vigente) | v81cf29 | 2026-11-04 | take-off-metal-frame-drywall_v81cf29_CFA-rev6-unida_2026-11-04.zip |
