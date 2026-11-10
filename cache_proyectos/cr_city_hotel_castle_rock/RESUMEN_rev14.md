# RESUMEN rev14 — CR City Hotel (Castle Rock, CO)

rev14 reemplaza a rev13. Origen: tu regla U-156 (10-nov): "en estos planos siempre viene toda la información". Re-barrí cada uno de los 9 RFI abiertos en todo el set (todas las disciplinas, SHX + vector, hojas OCR como A7.19, schedules, notas, leyendas, detalles, specs), con imagen circulada de cada respuesta (Auditoria/auditoria_rev13_rev14/).

| RFI | Resultado | N/HOJA | Imagen | Delta |
|---|---|---|---|---|
| RFI-15 | CERRADO (impreso) | A0.06 GN 10 "5/8" GYPSUM BOARD AT ALL OTHER LOCATIONS"; A0.00 "ROOF CONSTRUCTION 0 HR"; A0.10 "UNRATED ROOF ASSEMBLY"; spec 09 29 00 2.3 A (único board 5/8") | RFI-15_A0.06 / _A0.00 / _A0.10 | 0 |
| RFI-22 | CERRADO (impreso, opción A) | A0.00 DEFERRED SUBMITTALS solo cocina y F&B de L4; A7.31 "ENLARGED RCP - LOBBY & BAR"; A5.04 "BAR SUSPENDED GYP CEILING" | RFI-22_A0.00 / _A0.01 / _A7.31 / _A7.45 | 0 |
| RFI-23 | CERRADO (impreso, opción A) | 2/A0.01 "2HR FB" línea sólida en los 4 lados de ELEC / TELE 120; M3.02 keynote 3, fire/smoke damper | RFI-23_A0.01 | 0 (DA-1 retirado) |
| RFI-26 | CERRADO (impreso, opción B) | 1/A2.01 FACP 125 "7 SF"; 1/A6.02 puerta 125.1 en la cara sur, grid 14 a 4'-1 3/8" en el alcove; A8.00 125.1 | RFI-26_A6.02 | −51.24 SF Type X (FI.2-L1-12 fuera; DA-5 retirado) |
| RFI-04 | PARCIAL | Demising "1HR FP" (3/A0.01, 1/A0.02, nota A0.00) = DW.4-1 como estaba. Paredes sur de lobby 217 / 317: "2HR FB" (3/A0.01, 1/A0.02) → W.6-2 | RFI-04_A0.01 / _A0.02 / _A0.00 / _A0.06 | +199.10 SF Type X |
| RFI-04 (resto) | ABIERTO | ver barrido abajo | — | — |
| RFI-13 | ABIERTO | ver barrido | RFI-13_A0.06 / _A0.08 | — |
| RFI-17 | ABIERTO | ver barrido | RFI-17_A3.01 / _E1.01 / _P2.01 / _A8.00 / _A2.02 | — |
| RFI-21 | ABIERTO (tu decisión) | Impreso apunta a B: S1.02 "PRE-FABRICATED ROOF CANOPY BY OTHERS", 3/S3.10 "CANOPY BY OTHERS" | RFI-21_S1.02 / _S3.10 / _A9.05 | si B: −31.48 SF, −16.19 LF |
| RFI-24 | ABIERTO (tu decisión) | Impreso apunta a B: 2/A0.01 sin 2HR FB en 118B, 1/A7.50 "W.6.1 \| 0", A8.00 118.1 sin rating | RFI-24_A0.01 | si B: −414.03 SF (DA-2) |

## RFI que quedan, con su barrido
- **RFI-04 (resto):** tipo de los plumbing furring de baños, muros de ELEC 221 / 321 (sin línea FB alrededor), chase L4 X-L4-02/04/05, X-L4-03, janitor 109 y nichos del lobby (A7.35 solo da acabados).
  - Barrido: 148 hojas + OCR A7 + code plans A0.01 / A0.02 + specs 092216 / 092900 / 092116.23.
  - Términos: DEMISING, 1HR FP, 2HR FB, FIRE PARTITION, PARTITION TYPE, UNLESS NOTED, U.N.O., ALL PARTITIONS, UNTAGGED, TYPICAL WALL, PLUMBING WALL, CHASE, NICHE, TAMBOUR, BUILD-OUT, JANITOR, DW.4, FW.4, FW.6.
  - Opción B: IBC 2018 Section 708.1 / 708.3, 707.3 / 707.5, Table 2508.1, Section 2509.2.
- **RFI-13:** tamaño y espaciado del stud y C-channel del MB-1.
  - Impreso solo: "STEEL STUDS / C-CHANNEL / J-TRACK / BXUV.1516"; A0.06 STUD SCHEDULE C-H 6" 20 GA (cargado). GN 6 "16" O.C." es nota de particiones.
  - Opción B: IBC 2018 Section 703.2 y 703.3 item 1 (diseño listado no reproducido); Table 2508.1.
- **RFI-17:** 128 es el cuarto de fire pump (E1.01, E0.07, P2.01, A8.00 90 MIN); sin tag ni hatch de cielo en 1/A3.01; techo encima (A2.02).
  - Opción B: IBC 2018 Section 913.2.1 + 707.5; techo 0 HR (Table 601). Sin cielo: −188.01 SF, −47.0 LF main tee, −141.01 LF cross tee, −55.57 LF angle, −12.4 hanger.
- **RFI-21 y RFI-24:** lo impreso apunta a la opción B, pero el base mantiene tus decisiones del 6-nov (U-052). Necesitan tu confirmación.


## U-159 / U-160 — cuartos de las hojas RCP (orden del 10-nov)
Barrí cuarto por cuarto A3.02, A3.03, A3.04, A7.45 y A7.50 (A3.01 no imprime números de cuarto; L1 bajo el piso de L2 = membrana FS-1). Tabla completa: Auditoria/…/rcp_cuartos.json, con PNG circulado de cada faltante (U159_*.png).
- **Faltaban 9 cielos, todos en L4 (A3.04), ahora cargados con contorno medido:**
  - stalls 417.4 (33.17 SF) y 417.3 (18.90 SF) de Women, y el WC 418.2 de Men (31.58 SF): GYP-1 como CLG-L4-117;
  - 6 chases con stipple de cielo (405, 403, 404/403, a, b, c = 96.42 SF): RS-1 board en resilient channel, 8.94 ft.
- **Cada cuarto excluido lleva en el PDF de Bluebeam un texto rojo "EXCLUDED - motivo (N/HOJA)" (Subject EXCLUDED) y su contorno gris sin medida:** 24 en total = A3.04 12, A7.45 6, A7.50 6.
  - Ejemplo: 410 / 411 / 419 "Food & Beverage interior not in scope of this permit, future TI permit".
- **Hallazgo corregido:** el markup de Toilet 113 (CLG-L1-17) estaba en A7.31 con coordenadas de A7.50; ahora va en A7.50.
- **Pendiente para ti:** 1/A5.08 imprime "2HR SHAFT CEILING" + "STEEL SUPPORT PLATFORM WITH 2HR RATED FIRE PROOFING" junto a Elec 104. No tiene área ni assembly impresos [PENDIENTE]; Elec 104 ya lleva la membrana MB-1 / GYP-2.
- **Compuertas:** CE_RCP_CUARTOS (cuarto sin renglón o sin texto EXCLUDED = FAIL) y CE_NOMBRES_ENTREGA (U-158).

| Hoja | Cuarto | Disposición | Renglón / motivo | N/HOJA |
|---|---|---|---|---|
| A3.04 | 401 | row | L4 401 Guest Room Type 11 (bedroom/closet, excl. bath), CLG-L4-106 board (bath, GYP-1 8'-6", W.R.) |  |
| A3.04 | 402 | row | L4 402 Guest Room Type 12 (bedroom/closet, excl. bath), CLG-L4-108 board (bath) |  |
| A3.04 | 403 | row | L4 403 Guest Room Type 10 (bedroom/closet, excl. bath), CLG-L4-110 board (bath) |  |
| A3.04 | 404 | row | L4 404 Guest Room Type 6 (bedroom/closet, excl. bath), CLG-L4-112 board (bath) |  |
| A3.04 | 405 | row | L4 405 Guest Room Type 13 (bedroom/closet, excl. bath), CLG-L4-114 board (bath) |  |
| A3.04 | 406 | row | L4 406 Cleaning |  |
| A3.04 | 412 | row | L4 412 Corridor (field ceiling) |  |
| A3.04 | 417 | row | CLG-L4-117 board (+ main tee, cross tee, angle, hanger wire) |  |
| A3.04 | 418 | row | CLG-L4-118 board |  |
| A3.04 | 421 (ELEC) | row | CLG-L4-119 board |  |
| A3.04 | (stair, no number) | row | L4 Lobby stair (top floor, under roof; roof hatch + alternating tread device) |  |
| A3.04 | 413 (stair, number not printed on A3.04) | row | L4 SE stair 413 (top floor, under roof) |  |
| A3.04 | 417.4 (stall) | missing_loaded | CLG-L4-117A board |  |
| A3.04 | 417.3 (stall) | missing_loaded | CLG-L4-117B board |  |
| A3.04 | 418.2 (WC compartment) | missing_loaded | CLG-L4-118A board |  |
| A3.04 | (405 chase strip, no number) | missing_loaded | CLG-L4-405C board |  |
| A3.04 | (403 SW chase, no number) | missing_loaded | CLG-L4-403C board |  |
| A3.04 | (404/403 W chase, no number) | missing_loaded | CLG-L4-404C board |  |
| A3.04 | (chase a, no number) | missing_loaded | CLG-L4-412A board |  |
| A3.04 | (chase b, no number) | missing_loaded | CLG-L4-412B board |  |
| A3.04 | (chase c, no number) | missing_loaded | CLG-L4-412C board |  |
| A3.04 | 410 | exclusion | EXCLUDED - Food & Beverage interior not in scope of this permit, future TI permit | 1/A2.04 (note inside 410); also 1/A7.55 and 2/A7.55 (ENLARGED RCP - SPEAKEASY & BAR) |
| A3.04 | 411 | exclusion | EXCLUDED - Food & Beverage interior not in scope of this permit, future TI permit | 1/A2.04 (note inside 411); also 1/A7.55 and 2/A7.55 |
| A3.04 | 419 | exclusion | EXCLUDED - Food & Beverage interior not in scope of this permit, future TI permit | 3/A7.50 (note printed inside 419) |
| A3.04 | (410.3 vestibule, no number) | exclusion | EXCLUDED - Food & Beverage interior not in scope of this permit, future TI permit | 1/A2.04 (410 note; door 410.3 belongs to 410) |
| A3.04 | 420 | exclusion | EXCLUDED - exterior roof terrace, no ceiling | 1/A2.04 |
| A3.04 | 421 (terrace) | exclusion | EXCLUDED - exterior roof terrace, no ceiling | 1/A2.04 |
| A3.04 | (service elevator hoistway) | exclusion | EXCLUDED - elevator hoistway, no ceiling | 5/A6.00; 2/A0.02 |
| A3.04 | (lobby elevator hoistway) | exclusion | EXCLUDED - elevator hoistway, no ceiling | 9/A6.00; 2/A0.02 |
| A3.04 | (north shaft, no number) | exclusion | EXCLUDED - 2-hour shaft, walls continuous to underside of roof sheathing, no ceiling | 1/A5.08; 8/A9.03 |
| A3.04 | (south shaft, no number) | exclusion | EXCLUDED - 2-hour shaft, walls continuous to underside of roof sheathing, no ceiling | 7/A9.03; 10/A9.03 |
| A3.04 | (401 NE duct chase, no number) | exclusion | EXCLUDED - duct chase, no ceiling drawn on the RCP | 1/A3.04 (graphic only) |
| A3.04 | (401/402 duct chase, no number) | exclusion | EXCLUDED - duct chase, no ceiling drawn on the RCP | 1/A3.04 (graphic only) |
| A7.50 | 112 | row | CLG-L1-16 board |  |
| A7.50 | 113 | row | CLG-L1-17 board |  |
| A7.50 | 115 | exclusion | EXCLUDED - lay-in ACT ceiling (ACT-2), not drywall scope; FS-1 rated membrane above is loaded | 2/A7.50 |
| A7.50 | 116 | row | CLG-L1-18 board, CLG-L1-18 liner |  |
| A7.50 | 117 | exclusion | EXCLUDED - lay-in ACT ceiling (ACT-2), not drywall scope; FS-1 rated membrane above is loaded | 2/A7.50 |
| A7.50 | 118B | exclusion | EXCLUDED - lay-in ACT ceiling (ACT-2), not drywall scope; FS-1 rated membrane above is loaded | 2/A7.50 |
| A7.50 | 119 | exclusion | EXCLUDED - lay-in ACT ceiling (ACT-2), not drywall scope; FS-1 rated membrane above is loaded | 2/A7.50 |
| A7.50 | (120, number not printed on A7.50) | row | L1 FS-1 membrane under the LEVEL 2 floor (whole floor plate) |  |
| A7.50 | (passage, no number) | row | CLG-L1-14 board |  |
| A7.50 | (hall, no number) | row | CLG-L1-15 board |  |
| A7.50 | (CH.6 shaft, no number) | exclusion | EXCLUDED - 2-hour shaft, walls continuous to underside of roof sheathing, no ceiling | 1/A7.50; 2/A7.50 |
| A7.50 | 412 | row | L4 412 Corridor (field ceiling) |  |
| A7.50 | 417 | row | CLG-L4-117 board |  |
| A7.50 | 417.4 (stall) | missing_loaded |  |  |
| A7.50 | 417.3 (stall) | missing_loaded |  |  |
| A7.50 | 418.2 (WC compartment) | missing_loaded |  |  |
| A7.50 | 418 | row | CLG-L4-118 board |  |
| A7.50 | 419 | exclusion | EXCLUDED - Food & Beverage interior not in scope of this permit, future TI permit | 3/A7.50 |
| A7.50 | 421 | row | CLG-L4-119 board |  |
| A7.45 | 100 | exclusion | EXCLUDED - Food & Beverage interior not in scope of this permit, future TI permit | 1/A7.45 (note inside 100) |
| A7.45 | 101 | exclusion | EXCLUDED - lay-in ACT ceiling (ACT-2), not drywall scope; FS-1 rated membrane above is loaded | 4/A7.45 |
| A7.45 | 105 | exclusion | EXCLUDED - lay-in ACT ceiling (ACT-2), not drywall scope; FS-1 rated membrane above is loaded | 4/A7.45 |
| A7.45 | 102 | exclusion | EXCLUDED - lay-in ACT ceiling (ACT-1), not drywall scope; FS-1 rated membrane above is loaded | 1/A3.01 |
| A7.45 | 103 | row | CLG-L1-01 board, CLG-L1-01 liner |  |
| A7.45 | 104 | row | CLG-L1-00 board, CLG-L1-00 liner |  |
| A7.45 | 122 | exclusion | EXCLUDED - lay-in ACT ceiling (ACT-1), not drywall scope; FS-1 rated membrane above is loaded | 1/A3.01 |
| A7.45 | (NW box, no number) | exclusion | EXCLUDED - enclosed box, no ceiling drawn on the RCP | 3/A7.45 |

## Delta Material Summary (NET) rev13 → rev14
| Material | Unit | rev13 | rev14 | Delta |
|---|---|---|---|---|
| Hanger wire | LF | 476.40 | 483.40 | +7.00 |
| 5/8" gypsum board, Type X | SF | 87,189.73 | 87,517.65 | +327.92 |
| USG drywall suspension main tee DGLW26 | LF | 1,658.96 | 1,679.86 | +20.90 |
| USG drywall suspension cross tee DGLW424 | LF | 4,976.97 | 5,039.70 | +62.73 |
| USG angle molding DGWM24 | LF | 2,831.61 | 2,895.16 | +63.55 |
| Resilient channel - printed product (see Where it comes from) | LF | 19,479.22 | 19,551.54 | +72.32 |
| Joint compound, all purpose | LB | 8,445.78 | 8,469.39 | +23.61 |
| Joint tape, paper | LF | 50,639.42 | 50,760.75 | +121.33 |
