# PASO 12 rev8 — B&N Colorado Springs (3.ª pasada, verificador independiente, 2026-10-27)

**VEREDICTO: NO PASA.** Cobertura 100 % (501 ítems: 254 COVERED, 162 EXCLUDED, 74 RFI, 11 filas CORREGIR = 8 únicos), 0 GAP. Biblioteca 46: 32 PASS · 11 FAIL · 3 N/A. Proporciones OK salvo slab pins. Bluebeam vs Excel OK en 18 types (Δ máx. 0.006 LF type I; 94 annots).

Nota: el verificador no pudo hacer push (sesión sin el repo). MATRIZ_COBERTURA.xlsx e img/ (14 recortes) no llegaron al repo; este certificado es el texto que envió por mensaje. rev9 regenera la evidencia de los ítems corregidos.

rev7 verificado: C7-01..C7-09 y N-01/N-03 bien aplicados; renglones nuevos de rev8 reproducidos.

## CORREGIR
- **C8-01** · rev8: R52 slab pins 960.91, con la nota 8.F X-DNI (2 rows @ 16") sobre los 640.61 LF de bottom track. Plano: 3/A-410 y 4/A-410 "3 5/8" X 20GA TRACK W/ (2)-1/4"ø X 1 5/8" HILTI KWIK HUSEZ CONCRETE SCREW AND MOMENT CLIP – SEE DETAIL" (A/A-410); la sección del type manda sobre la nota típica (BE-19). Corrección: R52 = 777.43 [(640.61 − 122.32) × 1.5], es decir −183.48. HUS-EZ y moment clips siguen en RFI-28. RFI-ACC-slab-pins se recalcula sobre 518.29 LF: −388.72 con una fila @ 16"; −518.29 con el PAF de 9/A-410 @ 24".
- **C8-02** · rev8: el delta de RFI-28 lista 162 moment clips + 324 HUS-EZ. Plano: A/A-410 "(1) #10-16 SCREW @ EACH FLANGE". Corrección: agregar +324 #10-16 [162 × 2].
- **C8-03** · rev8: los #8 de 8/A-410 solo figuran como "about +724" genérico en RFI-51; la nota rev7 N-13 ("covered by framing screws") es falsa, porque R51 y R58 cuentan solo los studs de los walls. Plano: 8/A-410 "ATTACH TO TOP CORD OF EXIST'G STRUCTURE W/ #8 SCREWS"; "(2) #8 SCREW AT EACH STUD"; "ATTACH TO TRACK W/ #8 SCREWS AT 24" O.C.". Corrección: renglón propio de ≈ 849 pcs = top chord 141 × 2 (282) + cross member a track 141 + (2) × 213 studs en ≈ 282 LF de walls paralelos (426). Se suma 1 por cruce de joist en las corridas perpendiculares (espaciamiento no impreso → delta en RFI-41). Reescribir la frase "+724" de RFI-51.
- **C8-04** · rev8: R13 "Track, ceilings / soffits / canopy" 618.81 LF es un solo renglón con 3-5/8", 6", ledger de 8" y track perimetral de ceilings, en 16 / 20 / 14 ga. Plano: 8/A-210 "3 5/8"x16 GA TOP & BOTTOM TRACK" y "6"x16 GA TOP & BOTTOM TRACK"; 4/A-210 "8" LEDGER"; fire stop track del tamaño del stud (3/A-410). Viola BE-46. Corrección (Σ = 618.81): 3-5/8" 281.09 LF (118.28 + 157.81 + 5.00); 6" 144.06 LF (12.33 + 106.40 + 25.33); 8" ledger 12.67 LF; ceiling perimeter track 180.99 LF (tamaño no impreso → RFI); gauge por renglón.
- **C8-05** · rev8: renglones en LF con selling unit "piece" y Pieces to buy = ROUNDUP(LF): R18 (654), R22 (224), R23 (527, cuando RFI-15 dice 124 pcs), R24, R25, R29 (152), R38. Corrección: usar el stock length de Inputs (2x, DGLW26 12 ft, DGLW424 4 ft, molding 12 ft) o vender por LF / coil.
- **C8-06** · rev8: ALC-04 todavía lista "X-EDNI fasteners 8.C" como cuantificado. Debe decir: #8 pan head 291 + P.A.F. 282 (8/A-410), con X-EDNI como alternativa de RFI-51 (BE-47).
- **C8-07** · rev8: códigos internos del plan check en textos al cliente: Material Summary I27 "C7-03", I29 "C7-01", I31 "C-03"; Pending Items C7 y B38 "C-07", C41 "C7-01" (regla R80e.29). Corrección: quitarlos y dejar la cita N/SHEET.
- **C8-08** · rev8: S-12 = 1.2 × 11,143.59 SF (board bruto de los walls de 14 ga), pero la base de cement board se descuenta solo del total; R51 tiene N/SHEET "driver = …" sin hoja; las 485 / 296 piezas no tienen desglose. Plano: 8.E por gauge; la base 1'-2" de 22/A-201 cae en W2-05/06/07 (14 ga). Corrección: S-12 13,328.22 / Type S 6,114.04 (se mueven 36.74 SF × 1.2 = 44.09; el total no cambia). R51: N/SHEET "A-410 note 8.A" + lista por wall (485); R58: lista por wall (296).

GAP: ninguno.
