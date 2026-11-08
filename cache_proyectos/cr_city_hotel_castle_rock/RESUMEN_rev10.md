# RESUMEN rev10 — CR City Hotel (Castle Rock, CO)

rev10 reemplaza a rev9. Origen: auditoría adversarial diaria U-138 de COORDINACIÓN sobre rev9. Cada punto lo verifiqué en el plano con imagen.

## E1. RFI-27 / DA-6 retirados (la respuesta estaba impresa)
- A0.08 FS-1 (LEVEL 2, 3, 4 / THROUGHOUT / 1 HOUR / L546) dibuja la membrana 5/8" Type C continua y, debajo, "DROPPED CEILING IS NOT A COMPONENT OF THE RATED ASSEMBLY. REFER TO CEILING PLANS AND DETAILS FOR MATERIALS."
- Conclusión: la membrana sigue sobre el GYP-1 del bath [CONFIRMADO A0.08], que es la opción que ya estaba cargada. Imagen: Auditoria/contornos_rev9/E1_A008_FS1_dropped.png.
- Regla + compuerta: el barrido de RFIs suma sinónimos de cielo (DROPPED / SUSPENDED / NOT A COMPONENT...). Una frase de respuesta impresa junto a un término del RFI = FAIL, salvo que el descarte cite esa frase. Test: test_cr_r10_barrido_respuesta.

## E2. ELEC/TELE 120: el muro sur es 2 HR por lo impreso
- A8.00 imprime la puerta 120.1 ELEC / TELE "90 MIN" y la nota "DOOR RATING REQUIREMENTS PER TABLE 716.1(2)" + "FIRE WALLS AND FIRE BARRIES HAVING 2HR RATING: 90 MIN" (errata 'BARRIES' del set).
- W.6-L1-25 (sur, contiene la puerta 120.1) queda W.6-2 [CONFIRMADO].
- DA-1 queda solo W y E: −149.52 SF [DERIVADO: 50.16 + 33.12 + 66.24], antes −341.76. RFI-23 pregunta ya solo por W y E.
- Regla + compuerta CE_PUERTA_RATING_MURO: el rating de cada puerta del door schedule se cruza con el del muro que la contiene. Los furrings sobre CMU se exentan porque el rating lo lleva la mampostería. En este proyecto: 70 puertas con rating, 0 fallas. Test: test_cr_r10_puerta_rating_muro.

## R1. Shafts L2–L4: C-H 2-1/2" según el detalle que llama la burbuja
- 7/A9.03 "WALL DETAIL - PLAN OF SOUTH SHAFT" imprime "2-HOUR SHAFTWALL ASSEMBLY (W419, U497)" con muro de 4 3/4". 8/A9.03 "PLAN OF NORTH SHAFT" también imprime 4 3/4". 4 3/4" = C-H 2 1/2" + 1" liner + 2 × 5/8".
- 34 caras CH-L2/L3/L4-01..07 pasan a C-H 2-1/2" (604.31 LF) y J-runner 2-1/2" (121.52 LF). CH.6-L1 y CH.6-L4 (tag CH.6 en 1/A7.50) siguen en 6".
- A0.06 CH.6-2 (6") queda como Review Item y RFI-07, con su delta: mismo LF en 6".

## m1. Altura de los cielos de las unidades L2 201–214
- Antes: 9'-10 5/8", tomado de 7/A7.23 "WALL DETAIL - CORRIDOR CEILING". Ahora: 9'-2 7/8" = 11'-0" − 1'-9 1/8" (4/A5.05, zona del cuarto), igual que L3. No cambia cantidades.

## m2. Filas de shaft wall del Partition Takeoff
- Ahora dicen "Shaft wall (C-H)" con su stud: "C-H 2-1/2" 20 GA @ 24" o.c. + J-runner…" o el de 6" según el caso. El bloque se llama "SHAFT WALL (C-H STUDS AND J-RUNNER IN THE MATERIAL SUMMARY)". Los markups usan la misma etiqueta.

## m3. Conteos de burbujas
- CE_CALLOUTS cuenta destinos N/HOJA únicos (160) y las burbujas de las 87 hojas de la cadena del trade (530).
- CE_DETALLES_CIRCULADOS cuenta todas las burbujas de todas las hojas de origen del set, incluidas S / M / P / E (647).
- Las dos evidencias ahora dicen qué cuenta cada una (test_cr_r10_conteos_explicados).

Compuerta nueva CE_COHERENCIA_R10 para R1 / m1 / m2, con test test_cr_r10_coherencia.

## Delta Material Summary (NET) rev9 → rev10
| Material | Unit | rev9 | rev10 | Delta |
|---|---|---|---|---|
| C-H stud 6" 20 GA (shaft wall) - printed (see Where it comes from) | LF | 1,160.49 | 556.18 | -604.31 |
| J-runner 6" 20 GA (shaft wall top / bottom) - printed (see Where it comes from) | LF | 261.30 | 139.78 | -121.52 |
| C-H stud 2-1/2" 20 GA (shaft wall) - printed (see Where it comes from) | LF | 0.00 | 604.31 | +604.31 |
| J-runner 2-1/2" 20 GA (shaft wall top / bottom) - printed (see Where it comes from) | LF | 0.00 | 121.52 | +121.52 |

Skill v81cf66 (R80e.164).
