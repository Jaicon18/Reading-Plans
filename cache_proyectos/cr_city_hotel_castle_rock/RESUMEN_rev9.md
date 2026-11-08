# RESUMEN rev9 — CR City Hotel (Castle Rock, CO)

rev9 reemplaza a rev8. Orden vía COORDINACIÓN: (a) contorno real de todos los cielos, cuarto por cuarto, con imagen; (b) los 30 candidatos de A2.01.

## 1. Candidatos A2.01 (30)
- 24 ya medidos en las ampliadas.
- #4/#5 con disposición (PA0006 / RFI-06).
- #7/#29 son marcos de storefront.
- #20 es CMU.
- #19/#30 = FACP 125, que faltaba:
  - FI.2-L1-11: norte, 3.26 ft [DERIVADO] (1/A6.02, tag FI.2 | 0).
  - FI.2-L1-12: sur, 4.27 ft (1/A2.01). Va en el base con RFI-26 / DA-5 (−51.24 SF Type X).
  - Este: XM.0.1 | 2 '.1 NO FINISH', sin gypsum.

## 2. Contorno real de los cielos
- Los 52 ceilings y las 21 claves misc están medidos en vectores a las caras de los walls. Ningún polígono es caja, localizador ni escalado; los huecos (cofres, Stair 1, WS-1, shafts) van como keyhole en un solo anillo.
- Imágenes y JSON: Auditoria/contornos_rev9.

**Hallazgo:** el SF impreso de las unidades NO es consistente.
- 202: contorno 333.27 − bath 64.33 = 268.94 contra 269 impreso, o sea sin bath.
- 212: 389.55 contra 390, o sea con bath.

Por eso la cantidad de cada cielo es el contorno medido [DERIVADO] y el impreso queda como chequeo ±2 %, con su nota cuando no cuadra.

Cambios principales:
- **L2/L3 FS-1:** unidad completa a caras (membrana continua sobre el bath, A0.08 'THROUGHOUT'). RFI-27 / DA-6 = −2,499.67 SF Type C + RC si el FS-1 se corta en los muros del bath.
- **301–304:** el FS-1 se corta en x 1007.35 (A2.03), donde empieza la franja RS-6 bajo la terraza L4.
- **L4 RS-1 'excl. bath':** 403 y 404 restaban el bath dos veces (+86.7 / +96.5 SF). 405 resta su chase y su shaft.
- **Corridors 218/318:** el tramo N-S que faltaba (≈154 SF/piso). Además, los ramales E ya no entran a los vestíbulos de 209/309.
- **Lobby L1:** los fondos de los 10 cofres (538.65 SF) NO se agregan. Son la cara inferior del RATED ASSEMBLY (2/A7.31), o sea la membrana FS-1 de L1 ya cargada; CB_CR_R6_E1 lo detectó.
- **412 field:** contorno 1,237.72 − 3 paneles WS-1 medidos en vectores (146.70) = 1,091.02 SF.
- **Cove 412 (SOF-L4-02):** doble línea dibujada en 1/A3.04 = 343.7 LF (antes 242.72, que era el LF de los walls).
- **Canopy CAN-L1-ENTRY:** rectángulo dibujado 6.0 × 6.49 ft = 38.96 SF (antes 58.2 supuesto, RFI-21).
- **406:** el polígono quedaba fuera del edificio; ahora está dentro del cuarto (119.74 SF).
- **L1 FS-1 placa:** 7,835.81 SF = contorno interior 8,139.26 − 2 escaleras. La placa de L2 cuadra con A0.01 8,587 (−0.09 %).
- **Impresos que no cuadran:**
  - 203: misma caja que 202/204, que imprimen 269; el 255 parece error de hoja.
  - 207 / 307: +2.7 %.
  - 402: +2.5 %, con nube de revisión.
  - 405: el impreso incluye chase y shaft.
  - 412: la etiqueta está impresa dentro de F&B 410.

| Ceiling | rev8 SF | rev9 SF | impreso | cuadra con | N/HOJA |
|---|---|---|---|---|---|
| L2 Guest room 201 (Type 1) | 294.0 | 361.64 | 294.0 | impreso excl. bath | 1/A2.02 |
| L2 Guest room 202 (Type 1) | 269.0 | 333.24 | 269.0 | impreso excl. bath | 1/A2.02 |
| L2 Guest room 203 (Type 1) | 255.0 | 333.48 | 255.0 | NO CUADRA | 1/A2.02 |
| L2 Guest room 204 (Type 1) | 269.0 | 333.48 | 269.0 | impreso excl. bath | 1/A2.02 |
| L2 Guest room 205 (Type 5) | 469.0 | 564.17 | 469.0 | impreso excl. bath | 1/A2.02 |
| L2 Guest room 206 (Type 2) | 259.0 | 342.91 | 259.0 | impreso excl. bath | 1/A2.02 |
| L2 Guest room 207 (Type 2) | 334.0 | 342.91 | 334.0 | NO CUADRA | 1/A2.02 |
| L2 Guest room 208 (Type 3) | 389.0 | 472.69 | 389.0 | impreso excl. bath | 1/A2.02 |
| L2 Guest room 209 (Type 4) | 274.0 | 383.75 | 274.0 | impreso excl. bath | 1/A2.02 |
| L2 Guest room 210 (Type 9) | 295.0 | 383.54 | 295.0 | impreso excl. bath | 1/A2.02 |
| L2 Guest room 211 (Type 8) | 403.0 | 410.7 | 403.0 | impreso incl. bath | 1/A2.02 |
| L2 Guest room 212 (Type 7) | 390.0 | 394.57 | 390.0 | impreso incl. bath | 1/A2.02 |
| L2 Guest room 213 (Type 6) | 427.0 | 432.9 | 427.0 | impreso incl. bath | 1/A2.02 |
| L2 Guest room 214 (Type 13) | 427.0 | 423.36 | 427.0 | impreso incl. bath | 1/A2.02 |
| L2 Corridor 216 | 455.0 | 457.66 | 455.0 | impreso | 1/A2.02 |
| L2 Corridor 218 | 565.3 | 808.38 | – | NO CUADRA | 1/A2.02 |
| L2 Lobby 217 | 66.0 | 66.45 | 66.0 | NO CUADRA | 1/A2.02 |
| L2 Cleaning 215 | 123.0 | 123.41 | 123.0 | impreso | 1/A2.02 |
| L2 Linen 222 | 19.4 | 19.48 | – | cargado | 1/A2.02 |
| L2 Cleaning 223 | 8.7 | 8.71 | – | cargado | 1/A2.02 |
| L2 Elec 221 | 6.0 | 5.62 | – | NO CUADRA | 1/A2.02 |
| L3 Guest room 301 | 181.38 | 275.9 | 296.0 | impreso excl. bath | 1/A2.03 |
| L3 Guest room 302 | 165.45 | 251.24 | 270.0 | impreso excl. bath | 1/A2.03 |
| L3 Guest room 303 | 164.84 | 251.24 | 269.0 | impreso excl. bath | 1/A2.03 |
| L3 Guest room 304 | 164.84 | 251.46 | 269.0 | impreso excl. bath | 1/A2.03 |
| L3 Guest room 305 | 468.0 | 563.92 | 468.0 | impreso excl. bath | 1/A2.03 |
| L3 Guest room 306 | 259.0 | 342.97 | 259.0 | impreso excl. bath | 1/A2.03 |
| L3 Guest room 307 | 334.0 | 342.97 | 334.0 | NO CUADRA | 1/A2.03 |
| L3 Guest room 308 | 388.0 | 472.8 | 388.0 | impreso excl. bath | 1/A2.03 |
| L3 Guest room 309 | 273.0 | 386.77 | 273.0 | impreso excl. bath | 1/A2.03 |
| L3 Guest room 310 | 295.0 | 383.84 | 295.0 | impreso excl. bath | 1/A2.03 |
| L3 Guest room 311 | 279.0 | 410.7 | 279.0 | impreso excl. bath | 1/A2.03 |
| L3 Guest room 312 | 309.0 | 395.56 | 309.0 | impreso excl. bath | 1/A2.03 |
| L3 Guest room 313 | 320.0 | 433.34 | 320.0 | impreso excl. bath | 1/A2.03 |
| L3 Guest room 314 | 425.0 | 423.85 | 425.0 | impreso incl. bath | 1/A2.03 |
| L3 315 Cleaning | 124.0 | 123.69 | 124.0 | impreso | 1/A2.03 |
| L3 Corridor 316 | 455.0 | 458.21 | 455.0 | impreso | 1/A2.03 |
| L3 Lobby 317 | 132.0 | 124.98 | 132.0 | NO CUADRA | 1/A2.03 |
| L3 Corridor 318 | 614.5 | 751.86 | – | NO CUADRA | 1/A2.03 |
| L3 ELEC 321 | 9.7 | 5.86 | – | NO CUADRA | 1/A2.03 |
| L3 322 Linen | 19.4 | 19.51 | – | cargado | 1/A2.03 |
| L3 323 Cleaning | 8.8 | 8.71 | – | cargado | 1/A2.03 |
| L4 401 Guest Room Type 11 (bedroom/closet, excl. bath) | 333.64 | 329.01 | 443 | impreso incl. bath | 1/A2.04 |
| L4 402 Guest Room Type 12 (bedroom/closet, excl. bath) | 461.17 | 461.5 | 556 | NO CUADRA | 1/A2.04 |
| L4 403 Guest Room Type 10 (bedroom/closet, excl. bath) | 426.19 | 512.92 | 521 | impreso excl. bath | 1/A2.04 |
| L4 404 Guest Room Type 6 (bedroom/closet, excl. bath) | 216.86 | 313.34 | 317 | impreso excl. bath | 1/A2.04 |
| L4 405 Guest Room Type 13 (bedroom/closet, excl. bath) | 341.51 | 293.62 | 427 | NO CUADRA | 1/A2.04 |
| L4 406 Cleaning | 124.0 | 119.74 | 124 | NO CUADRA | 1/A2.04 |
| L4 Lobby stair (top floor, under roof; roof hatch + altern | 151.85 | 151.84 | – | cargado | 1/A2.04 |
| L4 SE stair 413 (top floor, under roof) | 151.85 | 151.61 | – | cargado | 1/A2.04 |
| L1 FS-1 membrane under the LEVEL 2 floor (whole floor plat | 7928.8 | 7835.81 | 8587 | cargado | 1/A2.02 |
| L4 412 Corridor (field ceiling) | 1215.4 | 1091.02 | 1350 | NO CUADRA | 1/A2.04 |

## 3. Delta Material Summary (NET) rev8 → rev9
| Material | Unit | rev8 | rev9 | Delta |
|---|---|---|---|---|
| Ceiling / soffit track (size per source, see Where it comes from) | LF | 2,414.06 | 2,616.04 | +201.98 |
| Carrying channel (ceilings) | LF | 168.08 | 167.56 | -0.52 |
| Hanger wire | LF | 470.89 | 476.40 | +5.51 |
| 5/8" gypsum board, Type X | SF | 86,173.29 | 86,539.99 | +366.70 |
| USG drywall suspension main tee DGLW26 | LF | 1,612.51 | 1,658.96 | +46.45 |
| USG drywall suspension cross tee DGLW424 | LF | 4,837.66 | 4,976.97 | +139.31 |
| USG angle molding DGWM24 | LF | 2,814.39 | 2,831.61 | +17.22 |
| Resilient channel - printed product (see Where it comes from) | LF | 17,919.15 | 19,572.37 | +1,653.22 |
| 5/8" gypsum board, Type C (ceiling) | SF | 19,715.57 | 21,917.70 | +2,202.13 |
| 1" gypsum shaftliner panel, Type X (C-H shaft wall) | SF | 1,373.02 | 1,371.66 | -1.36 |
| 5/8" exterior gypsum sheathing, Type X | SF | 17,746.71 | 17,727.47 | -19.24 |
| C-H stud 6" 20 GA (shaft wall) - printed (see Where it comes from) | LF | 1,161.31 | 1,160.49 | -0.82 |
| J-runner 6" 20 GA (shaft wall top / bottom) - printed (see Where it comes from) | LF | 261.56 | 261.30 | -0.26 |
| Joint compound, all purpose | LB | 9,596.03 | 9,780.98 | +184.95 |
| Joint tape, paper | LF | 49,312.92 | 50,263.38 | +950.46 |

## 4. Compuerta y skill
- CE_CONTORNO_REAL (nueva, todos los proyectos): falla con
  - Contents con bbox / locator / box / scaled, salvo 'source has no geometry' dentro de la huella;
  - centroide fuera del edificio;
  - ceilings[] sin contorno medido o con medido ≠ cargado;
  - medido vs impreso > 2 % sin nota.
- Su test repite 406 y 215.
- Skill v81cf65.
- Error corregido en esta rev: el angle molding de los baths tomó el perímetro de toda la unidad (+1,727 LF). Lo detecté en el delta y lo corregí antes de entregar; queda como R80e.163.6.
