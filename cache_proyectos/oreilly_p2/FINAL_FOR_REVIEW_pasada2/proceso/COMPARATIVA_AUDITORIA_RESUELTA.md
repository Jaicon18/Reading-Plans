# COMPARATIVA AUDITORÍA RESUELTA — O'Reilly Evans CO #1, pasada 2 (ensamble rev2, run7)

Run: `run7` (`--sin-api`, cadena completa). Compuertas: reglas.py = 1 falla (back-check pendiente, paso posterior); registro entregable OK; alcances compuerta OK; cobertura 254/254. Nada escalado (#0). Detalle de cambios: `lect_resolucion/ensamble_cambios.md` (11-22), tools: `skill/.../tools/CAMBIOS_tools_v80v.md` (R80e.83-90).

| # | Hallazgo | Paso | Resolución | N/HOJA | Cambio aplicado |
|---|---|---|---|---|---|
| 1 | S24-OF 11.708 vs 11'-0" (+6.4 %) | 11 (#1) | Documentado: el plano lo soporta. La regla de dueño de esquina (R70.2 / R78.35) toma el wall cuyo hatch llena el cuadrado de la esquina en 1/A1.1. S24 llena las esquinas con S43 (zooms 40x: img_revision/e_A1.1_S24-OF_x_S43-OF-W_corner_40x, e_A1.1_S24-RR_x_S43-RR-W_corner_40x, e_A1.1_S24-RRS_x_S43-RR-S_corner_16x). Por eso S24 = cota libre impresa + espesor del S43 que posee. Los S43 arrancan en la cara de S24 y no se cuentan dos veces (el LF total es la suma de las cotas impresas más una sola vez cada espesor). | 11'-0"/A1.1 + 2 x 4-1/4" | Ninguno (ELEMENTO_1 aprobado) |
| 2 | S24-RR 16.823 (≥ +4.1 %) | 11 (#2) | Igual que 1: 7'-10" + 6" + 7'-10" + S43-RR-W 4-1/4" + S24-RRS 3-5/8" (S24-RR dueño de las 2 esquinas) | A1.1, 1A/A4.1 | Ninguno |
| 3 | S24-RRS 8.854 (+4.2 %) | 11 (#3) | Igual que 1: 8'-6" + 3-5/8" + 5/8" (S24-RRS dueño de la esquina con S43-RR-S) | 1A/A4.1, A1.1 | Ninguno |
| 4 | S42-02: continuación de ≈ 6.77 ft sin cota (#0) | 11 (#4) | Era una medida en pt; se quitó del op. Ahora es supuesto conservador cargado 6.715 + RFI-29 (B −6.715 LF, ≈ −103 SF) | A1.1 | canon length_op / length_source; RFI-29 |
| 5 | Z-furring 2,517.5 vs 2,235.0 (+12.6 %) sin desglose | 11 (#5), 12 (BE-40 / BE-45) | Desglose por wall en el renglón (studs_out). La diferencia con el cálculo del auditor ((ROUNDUP(L/2)+1) x H) son los jambs de las aberturas en CMU (doors 2 / 3 / 7, D1 / D2: +12 en S21-N), los nodos y los cripples (S21-S 20, S21-N 5). El furring sigue detrás de S24 hasta el eave bajo el purlin (estimator decision 2026-11-01 (RFI-02) = A), dentro de S21-E / S21-S y sin doble conteo: S24 lleva solo 362S162-33 a 8'-6". | S21/A1.1, 2/A3.2, 1/A3.2 | trazabilidad (R80e.83) |
| 6 | Compound sin waste (B6 6 %) | 11 (#6) | Regla del skill: "yields sin waste" (yields sin desperdicio). Se deja en 0 % y se escribe en la nota de Inputs B23 / B24 | Inputs B23 | Inputs notes (takeoff.json) + default de la tool |
| 7 | Tape sin waste | 11 (#7) | Igual que 6 | Inputs B24 | igual |
| 8 | Resilient channel: Pieces = LF | 11 (#8), 12 (BE-51) | Pieza de 12 ft (Inputs B17): 120.51 x 1.15 / 12 → 12 pcs | 1/A3.1, 1/A5.2 | plantilla clase de compra (R80e.86) |
| 9 | Flat strap comprado como "C.R. channel 16 ft" | 11 (#9) | Rollo (LF) | A1.1 2.B | plantilla (R80e.86) |
| 10 | Ceiling track cita 1/A-121, 5/A-121 | 11 (#10), 12 (BE-12 / BE-102) | Cita sus propias fuentes: 7/A4.2, 3/A3.1. Se quitaron las hojas fijas de otro proyecto en todas las ramas | 7/A4.2, 3/A3.1 | trazabilidad (R80e.83) |
| 11 | Header 56 LF sin desglose | 11 (#11), 12 (BE-40) | Por door: (3.333 + 1.333) x 4 pcs x 3 = 56.0, con 7/A5.1 | 7/A5.1 | trazabilidad (R80e.83) |
| 12 | Polyiso rígido sin exclusión | 11 (#12) | ALC-INSUL: insulation de todo tipo EXCLUDED (estimator standing order, regla del skill), con sus hojas; a confirmar | A1.1 types, A3.1 keys 10 / 15 / 16 / 36, A4.2 13 / 14 | takeoff alcances; tools canon / accesorios (R80e.88); RFI_PENDIENTES |
| 13 | Acoustical sealant ("standing order") | 11 (#13) | Queda EXCLUDED con su fuente (estimator standing order, skill U8) y A1.1 4.B citada; a confirmar | A1.1 4.B | plantilla EXCLUIDAS_SIEMPRE, alcances, RFI_PENDIENTES |
| 14 | Stucco sin renglón NOT IN SCOPE | 11 (#14) | ALC-STUCCO EXCLUDED (plaster / masonry) | A3.1 13 / 14 / 18, 1/A5.2, A2.1 | takeoff alcances |
| 15 | Español, archivos internos, dict crudo, códigos | 11 (#15), 12 (BE-41 / BE-55 / BE-106) | Textos limpiados en el canon y el overlay; la opción C se escribe como texto; nueva compuerta de texto de cliente (falla si queda algo) | - | limpiar_textos.py; plantilla (R80e.84) |
| 16 | S42 en 2 renglones con alturas ponderadas | 11 (#16) | Documentado: es la convención fija de la plantilla (partition_types: tramos colineales del mismo type en un renglón, con las alturas por cara en "Location"). Markups y Partition Takeoff cuadran por type (122.622 LF) | 5/A4.2, 6/A4.2 | Ninguno |
| 17 | Layers 0.79 en HEAD-A-8 | 11 (format) | Documentado: Layers = Board / (L x H) de un wall con board parcial (cara int. de 8" en 30.667 LF, 1/A5.2). El valor sale del programa | 1/A5.2 | Ninguno |
| 18 | RFI-05 citado y no presente | 12 (gap 9, BE-47) | Renglón cerrado "estimator decision 2026-11-01 (RFI-05)": glass mat en la cornice; el FRT de 11/A5.2 es solo el head de la ventana D | 1/A3.4, 11/A5.2 | takeoff rfi_cierre |
| 19 | RFI-16 citado y no presente | 12 (gap 10, BE-47) | Renglón cerrado (RFI-16 = A, 12'-0") | 1/A3.1 | takeoff rfi_cierre |
| 20 | RFI-11: dice A y carga B | 12 (BE-47 / BE-101) | A = lo cargado (ties de head + pier, FCB 60 + 24); B = solo donde se corta 3/S5.3 | 3/S5.3, 1/A3.1 | canon + overlay patch |
| 21 | RFI-ACC additional head track 40 vs 32.73 | 12 (BE-47) | El storefront A va sobre el wind beam de acero del PEMB (steel by others): no lleva head track ni RFI. Head track solo en Door 3 / D1 / D2 (RFI-21) | 3/S5.3 | accesorios (R80e.87) |
| 22 | RFI-ACC deflection clips cita una nota inexistente + "R73.6" | 12 (BE-12) | La deflexión de 2.C se carga como deep-leg slotted impreso; no hay clip impreso → deflection_clips none_reason y sin RFI | A1.1 2.C, 3/S5.1, 4/S5.1 | canon |
| 23 | RFI-25 cita "decision of the other pass" | 12 (BE-106 / BE-101) | B: "No trade code requires it (plans only)" | 14/A4.1 | canon |
| 24 | Control joints donde cambia de dirección (A1.1 3.A) | 12 (gap 1) | Cargado: 69.71 LF (4 esquinas de S21 + esquina del header S42) + RFI-30 | A1.1 3.A, 6/A4.2 | canon misc CJ-DIR-CHANGE |
| 25 | Seismic bracing del suspended ceiling | 12 (gaps 2 / 3) | ALC-ACT EXCLUDED (instalador del ceiling acústico), con cita; a confirmar | A1.2 GN D, 9/A4.2 | takeoff alcances; RFI_PENDIENTES |
| 26 | 1x4 wood trim A4.2 KN12 / A4.1 KN11 | 12 (gaps 4 / 5) | EXCLUDED Div. 06 (ALC-WOODTRIM) + RFI-33 (B +52.73 LF). CB-7A42-TOP queda (key 7 impreso); 4/A4.2 no tiene key 12 → CB-S41-BOXES no cambia | 7/A4.2, 4/A4.2, A4.1 | canon RFI-33; alcances |
| 27 | Trim / edge molding de W-4 (A4.1 KN8) | 12 (gap 6) | Cargado con el panel: 234.0 LF (renglón propio) + RFI-31 | A4.1 key 8, 1A/A4.1 | canon misc W4-TRIM-EDGE; familia nueva (R80e.89) |
| 28 | Security shutters, support framing | 12 (gap 7) | ALC-SHUTTERS EXCLUDED según la decisión del estimador (respuesta 24), con la nota "support framing to be added if shutters are added" | A5.2 GN H | takeoff alcances |
| 29 | Diagonal bracing del vestibule head | 12 (gap 8, BE-16) | Cargado: 22.14 LF 600S162-43 (3 x 7.38 ft, de cotas impresas) + RFI-32 | 3/A3.1, 3/A5.2 | canon misc VH-DIAG-BRACE |
| 30 | Storm panels GN I sin declarar | 12 (obs.) | ALC-STORM no aplica: G1.1 Vult 108 mph < 120 | A5.2 GN I, G1.1 | takeoff alcances |
| 31 | Varios productos en un renglón | 12 (BE-46) | Un renglón por producto (designación SSMA, tipo de trim, tipo de clip), cada uno con su N/HOJA | - | trazabilidad (R80e.85) |
| 32 | Markups S41 −0.93 %, S43 −0.53 % | 12 (BE-44) | El band se ajustó al LF contado (el dueño de esquina suma el espesor), centrado en el wall dibujado (corrimiento ≤ 0.42 pt). Ahora 0.00 % | A1.1 | canon bands |
| 33 | "N/SHEET: not applicable" en 44 renglones | 11 (#3), 12 (BE-40) | Cada renglón con su N/HOJA real. Los renglones sin hoja (fasteners excluidos, yields, additional head track) dicen "default (no sheet)" | - | trazabilidad (R80e.83) |
| 34 | Jamb return: RFI-ACC de delta 0 | (detectado en rev2) | Sin RFI vacío: el ancho es una decisión del estimador | 12-13/A5.2 | accesorios (R80e.90) |

Resueltos: 34 / 34. 27 se aplicaron como cambio (canon, overlay, takeoff.json o tool). 7 se documentaron sin cambio: 5 porque el plano / la convención los soporta (1-3 dueño de esquina de S24, 16 S42 en un renglón, 17 Layers) y 2 por la regla del skill (6-7 yields sin waste).
