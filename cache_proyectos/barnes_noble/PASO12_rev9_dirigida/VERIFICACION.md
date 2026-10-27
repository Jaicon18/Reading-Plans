# PASO 12 rev9: revisión dirigida (verificador independiente, 2026-10-27)

**Objeto:** `FINAL_FOR_REVIEW_2026-10-24_rev9/` (commit 1ba3459), Excel `Barnes_Noble_ColoradoSprings_Takeoff_FINAL_rev9.xlsx`, recalculado con LibreOffice.
**Lista:** `PASO12_rev8/CERTIFICADO_PASO12.md`, ítems C8-01 a C8-08.
**Plano:** bid set de Drive (md5 `c5a07249e01460702f005b298435f939`), A-410 p28, A-210 p13, A-201 p12, renderizado a 300 dpi. Recortes circulados en `img/`; cada uno se reabrió y se revisó.
**Alcance (R80e.30):** solo los 8 ítems, lo que depende de ellos y la biblioteca BE-16, 19, 40, 46, 47, 51 a 56.

## VEREDICTO: NO PASA

- Las cantidades de los 8 ítems están bien: ningún número cambia.
- Hay 3 FAIL de forma y trazabilidad: C8-04 (gauge por renglón), C8-05 (stock length en Inputs) y C8-08 (lista por wall de 485).
- Los tres se corrigen solo con texto o celdas de Inputs. El GRAND TOTAL y el cuadre Bluebeam no se mueven.

| Ítem | Resultado | Evidencia |
|---|---|---|
| C8-01 | **OK** | img/03, img/05 |
| C8-02 | **OK** | img/04 |
| C8-03 | **OK** (775 es defendible; 849 no es una cota impresa) | img/01, img/02 |
| C8-04 | **FAIL** (menor): la separación por tamaño está bien, pero falta el gauge por renglón | img/06, img/07 |
| C8-05 | **FAIL** (menor): las piezas son reales, pero el stock length está escrito en la fórmula y no en Inputs | — |
| C8-06 | **OK** | img/02 |
| C8-07 | **OK** | — |
| C8-08 | **FAIL** (menor): S-12 y Type S están bien, pero falta la lista por wall de las 485 piezas | img/05, img/08 |

## Detalle por ítem

### C8-01 Slab pins: OK
- [CONFIRMADO] 3/A-410 y 4/A-410 imprimen "3 5/8" X 20GA TRACK W/ (2)-1/4"ø X 1 5/8" HILTI KWIK HUSEZ CONCRETE SCREW AND MOMENT CLIP – SEE DETAIL" (img/03).
- [CONFIRMADO] La nota 8.F imprime "X-DNI … 2 ROWS AT 16" O.C." (img/05).
- [DERIVADO] El bottom track suma 640.61 LF (MS A4 450.02 + A5 118.59 + A6 72). Los types 3 y 4 suman 122.32 LF (subtotales del Partition Takeoff: 38.68 + 83.64; Bluebeam igual). (640.61 − 122.32) / 0.6667 = **777.43**, que es lo que tiene MS A56 (H = 778).
- Pending Items RFI-ACC-slab-pins: una fila @ 16" = −388.72; @ 24" = −518.29 ✓.
- Observación (no FAIL): MS I56 cita "9/A-410", pero la fuente del espaciamiento cargado es la nota 8.F. Sugiero "A-410 note 8.F (9/A-410 = alternate)".

### C8-02 #10-16 en RFI-28: OK
- [CONFIRMADO] A/A-410 imprime "(1) #10-16 SCREW @ EACH FLANGE" (img/04).
- El delta de RFI-28 (Pending Items C31) es: +162 moment clips + 324 HUS-EZ + **324 #10-16** (162 × 2) ✓.

### C8-03 #8 screws de 8/A-410: OK. Punto de criterio resuelto
- [CONFIRMADO] Ninguna cota impresa da 849. El "≈ 849" del certificado rev8 es una estimación del verificador anterior: (2) × 213 studs sobre "≈ 282 LF de walls paralelos".
- [DERIVADO] Esa base no se reproduce. Los walls de altura completa paralelos a los joists (ori V, h ≥ 13.5 ft) son 19 corridas con **217.39 LF**, no 282. Los wall studs @ 16" en esas corridas son **190**, no 213.
- Con la lectura del certificado, el total sería 775 − 282 + 380 = **873**, no 849.
- Cómo leo el plano (img/01): en la vista PARALLEL TO STRUCTURE, las dos flechas de "(2) #8 SCREW AT EACH STUD" terminan en los dos tornillos dibujados en la unión del track con el cross member. El cross member es el "METAL STUD PER SCHEDULE … AT EACH END" que va de joist a joist. Las flechas no llegan a los studs del wall.
- Conclusión: leer "2 por cross member" es **defendible** y está dibujado. La otra lectura queda bien registrada como RFI-41: 2 × 190 = 380, es decir **+98** ✓.
- [DERIVADO] Reproduje 775 = 2 × 141 + 141 + 2 × 141 + 70.
  - 141 cross members = Σ(ROUNDUP(L/2) + 1) sobre los walls paralelos.
  - 70 = Σ(ROUNDUP(L/5) + 1) sobre 262.46 LF de walls perpendiculares.
  - Con joists a 4'-0": 85, es decir +15 ✓ (RFI-41).
- Ya no aparece la frase "+724" en RFI-51, y la nota N-13 quedó corregida (BE-52).

### C8-04 Track de ceilings separado: FAIL (menor)
- Por tamaño está bien: Σ = 281.09 + 144.06 + 12.67 + 180.99 = **618.81** ✓, igual al renglón de rev8.
  - [CONFIRMADO] 8/A-210 imprime "3 5/8"x16 GA" y "6"x16 GA TOP & BOTTOM TRACK" (img/06).
  - [CONFIRMADO] 4/A-210 imprime "8" LEDGER" (img/07).
  - El ceiling perimeter track tiene su RFI-54 ✓.
- **Falta lo que pidió el certificado: "gauge por renglón".** MS A37, A38 y A39 no dicen el gauge. Los renglones de bottom track (A4, A5, A6) sí lo dicen. A37 y A38 mezclan productos de distinto gauge:
  - A37, Track 3-5/8" (281.09): 14 ga SJ **157.81** (fire stop W2-03…W2-09, C-H2a, C-H2b) + 20 ga **118.28** (SS-N, SS-E, SS-IN-N, SS-IN-E) + 16 ga **5.00** (VEST-POSTS-TRACK, 8/A-210).
  - A38, Track 6" (144.06): 20 ga SJ **118.73** (SS-GG 12.33 + fire stop 106.40) + 16 ga **25.33** (VEST-BOX-BEAM-TRACK, 8/A-210).
  - A39, 8" ledger (12.67): 4/A-210 no imprime el gauge. Hay que decir "gauge not printed" y agregarlo a una RFI (por ejemplo a RFI-54) o crear una nueva.
- Corrección: agregar en I37, I38 e I39 "Track gauge = stud gauge (A-410 schedule note 2) / 8/A-210: …" con las cifras de arriba, o separar los renglones por gauge. La cantidad no cambia.

### C8-05 Unidades de compra: FAIL (menor)
- Las piezas son reales ✓: 2x 82 y 3, main tee 19, cross tee 132, moldings 11 y 11. El 16 ga wire y el hanger wire se compran en coil (LF).
- **El stock length no es una celda de Inputs.** El certificado pidió "usar el stock length de Inputs (2x, DGLW26 12 ft, DGLW424 4 ft, molding 12 ft)". Las fórmulas H18 y H42 `/8`, H22 `/12`, H23 `/4`, H24 y H25 `/12` llevan el número escrito.
- Además, el encabezado MS A2 dice "Every stock length, coverage and yield is an Inputs cell", y eso hoy es falso (BE-47).
- Corrección: agregar 4 celdas en Inputs (2x lumber 8 ft, main tee 12 ft, cross tee 4 ft, molding 12 ft) y apuntar las fórmulas a ellas. Las piezas no cambian.
- Observación: G45 (hanger count, PCS) no tiene selling unit. Viene de antes; poner "each".

### C8-06 ALC-04: OK
- Scope Checklist ALC-04 dice: "8/A-410 #8 pan head screws + P.A.F. + #8 screws (own rows); X-EDNI 8.C = alternative in RFI-51". Ya no da X-EDNI como cuantificado ✓.
- [CONFIRMADO] img/02 y img/01: relief channel con "#8 PAN HEAD … AT 24" O.C." y P.A.F. at each end. Las cantidades son MS A27 = 291 y MS A30 = 282.

### C8-07 Códigos internos: OK
- Busqué con regex `C\d?-0\d`, `C[78]-\d\d`, `N-\d\d`, `BE-`, `R80`, "plan check" en todas las hojas: **0 coincidencias**.
- Las celdas I27, I29 e I31 y Pending Items C7, B38 y C41 ahora citan N/SHEET ✓.
- Observación: Pending Items B49 dice "(estimator decision RI 7)". "RI 7" es una referencia a Review Item, no un código del plan check. Sugiero cambiarlo por "estimator decision 2026-10-26".
- Observación: README_REVIEW.md lista C8-0x y N-13 a propósito, porque es el mapa para el revisor. No debe ir al cliente.

### C8-08 Screws por gauge: FAIL (menor)
- [CONFIRMADO] 22/A-201 imprime "5/8" CEMENT BOARD" y "1'-2" CEMENT BOARD BASE" (img/08).
- [DERIVADO] La base sobre los walls de 14 ga es (49.55 − W5-01 11.40 − doors 8 y 9 6.66) = 31.49 LF × 14/12 = **36.74 SF** ✓.
  - S-12 = 1.2 × (11,143.59 − 36.74) = **13,328.22** ✓.
  - Type S = 1.2 × 5,095.03 = **6,114.04** ✓.
  - El total, 19,442.26 = 1.2 × 16,201.88 SF de board (A19 + A20), no cambia ✓.
- R58 (MS A62, 1776 = 6 × 296) tiene la lista por wall ✓. R51 (MS A55) cita "A-410 note 8.A" ✓ (img/05).
- **Falta la lista por wall de las 485 piezas, que el certificado pidió.** A55 dice "partition walls (per-wall stud pieces) 673" como un solo número, más 108 de column wraps y menos 296. El 673 no se puede reproducir desde el Excel, porque el Partition Takeoff no tiene una columna de stud pieces.
- Corrección: listar en I55 las piezas por wall de 25/20 ga, igual que en I62. La cantidad no cambia.

## Lo que no se rompió
- **Partition Takeoff:** 0 celdas distintas entre rev8 y rev9. GRAND TOTAL **569.816 LF / 14,881.32 SF**, igual que en rev8 ✓.
- **Material Summary rev8 → rev9:** solo cambian los renglones de los C8.
  - Slab pins, Type S, S-12, #8 screws (nuevo).
  - Track separado en 4 renglones (Σ 618.81).
  - Piezas de 2x, tees y moldings.
  - Ningún otro renglón se movió.
- **Bluebeam vs Excel:** 77 measurements, 17 types de partition, Δ máximo 0.006 LF (type I). Los types 3 y 4, que toca C8-01, cuadran exacto: 38.68 y 83.64 ✓.

## Biblioteca (BE-16, 19, 40, 46, 47, 51 a 56)
| Prueba | Resultado | Nota |
|---|---|---|
| BE-16 | PASS | #8 de 8/A-410, P.A.F., #8 pan head y #10-16 de A/A-410: cada uno tiene renglón o RFI |
| BE-19 | PASS | Slab pins por 8.F impreso con la alternativa 9/A-410 en RFI. #8 @ 24" impreso. El espaciamiento de joists no está impreso y va en RFI-41 |
| BE-40 | PASS | Los desgloses suman el NET (I19 15,109.23 vs C19 15,109.29, Δ 0.06 ≤ 0.1). La falta de lista del 673 se cuenta en C8-08 |
| BE-46 | **FAIL** | A37 mezcla 14, 20 y 16 ga, y A38 mezcla 20 y 16 ga, sin desglose (C8-04) |
| BE-47 | **FAIL** | MS A2 dice "every stock length is an Inputs cell", pero H18, H22, H23, H24, H25 y H42 lo tienen escrito (C8-05). El resto de las cifras cruzadas coincide: 775, 380 y +98, +15, 324, 720, 781, 512, 518.29, 388.72, 132 y 124, RFI-54 |
| BE-51 | **FAIL** | Stock length fuera de Inputs (C8-05) |
| BE-52 | PASS | N-13 y "+724" quedaron corregidos |
| BE-53 | PASS | El delta de RFI-28 incluye clip, HUS-EZ y #10-16 |
| BE-54 | PASS | La deducción de 36.74 SF se aplica a las mismas caras de 14 ga |
| BE-55 | PASS | 0 códigos en las hojas. Observaciones: "RI 7" y el README interno |
| BE-56 | PASS | Los 122.32 LF de los types 3 y 4 no llevan slab pins |

**Resultado: 8 PASS · 3 FAIL · 0 N/A.** Los 3 FAIL son los mismos 3 ítems C8 y ninguno cambia cantidades.

## Para rev10 (solo texto o Inputs, sin cambio de cantidades)
1. I37, I38, I39: desglose por gauge con las cifras de arriba. Ledger 8": "gauge not printed (4/A-210)" más RFI.
2. Inputs: 4 celdas de stock length (2x 8 ft, DGLW26 12 ft, DGLW424 4 ft, molding 12 ft). Apuntar a ellas H18, H22, H23, H24, H25 y H42.
3. I55: lista por wall de las 485 piezas de 25/20 ga.
4. Opcionales: I56 citar 8.F; G45 "each"; B49 quitar "RI 7".

---

## Recheck rev10 (commit b77163b), solo C8-04, C8-05 y C8-08 (R80e.30)

**VEREDICTO rev10: PASA.**
- Los 3 FAIL de rev9 quedaron corregidos.
- Net, piezas y GRAND TOTAL son iguales a rev9.
- BE-46, BE-47 y BE-51 dan PASS.

| Ítem | Resultado | Lo que hay en rev10 |
|---|---|---|
| C8-04 | **OK** | MS A37 "Track 3-5/8" (14 ga 157.81 + 16 ga 5.00 + 20 ga 118.28)", que suma 281.09 ✓. A38 "Track 6" (16 ga 25.33 + 20 ga 118.73)", que suma 144.06 ✓. A39 "8" ledger track (gauge not printed, RFI-54)", y RFI-54 agrega el delta del ledger (12.67 LF; si es 16 ga como 8/A-210, solo cambia el precio) ✓. Las cifras coinciden con las que calculé en rev9 (img/06, img/07) |
| C8-05 | **OK** | Inputs B26 2x 8 ft, B27 main tee 12 ft, B28 cross tee 4 ft, B29 molding 12 ft. H18 y H42 usan `Inputs!$B$26`; H22, H23 y H24/H25 usan B27, B28 y B29. Las piezas son 82, 19, 132, 11, 11 y 3, iguales a rev9 ✓. Ahora sí es verdad lo que dice MS A2. G45 = "each" ✓ |
| C8-08 | **OK** | I55 trae la lista por wall de 25/20 ga: 50 walls que suman 377, más 9 column wraps × 12 = 108, total **485** ✓. Ningún wall de 14 ga (W2-xx, C-H2a/b, C-F) está en la lista ✓. 4 × 485 = 1,940 ✓ |

**Lo que no cambió:**
- Material Summary: Net y piezas iguales a rev9 en todos los renglones. Solo cambia el nombre de A37, A38 y A39.
- Partition Takeoff: 0 celdas distintas. GRAND TOTAL 569.816 LF / 14,881.32 SF ✓.
- También se aplicaron los opcionales: I56 cita "A-410 note 8.F (9/A-410 = alternate)" y ya no aparece "RI 7". El regex de códigos internos da 0 coincidencias.

| Prueba | rev10 |
|---|---|
| BE-46 | PASS: cada renglón de track tiene su gauge, y el que no está impreso va a RFI |
| BE-47 | PASS: lo que dice MS A2 es verdad. RFI-54 coincide con A39. 377 + 108 = 485 coincide con A55 |
| BE-51 | PASS: stock lengths en Inputs B26 a B29 |
