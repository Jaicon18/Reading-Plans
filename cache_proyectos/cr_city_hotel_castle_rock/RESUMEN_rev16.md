# RESUMEN rev16 — CR City Hotel (Castle Rock, CO)

rev16 reemplaza a rev15. Origen: revisión dirigida independiente de rev15 por orden tuya del 10-nov ("revisa todo otra vez"): 13 de 18 puntos OK; 7 hallazgos nuevos. Cada uno: cargado / refutado / decidido con N/HOJA e imagen en `Auditoria/revision_dirigida_rev16/` (REV_* = lo que vio el revisor, AFTER_* = cómo quedó, BL_* / SOF_* = mediciones).

| # | Punto | Resultado | N/HOJA | Imagen | Delta |
|---|---|---|---|---|---|
| 1 | ELEC 221 / 321 / 421 | **CARGADO (base = opción mayor) + DEDUCT ALTERNATE DA-6**. No era refutación: A0.00 imprime "ELECTRICAL AND IT ROOMS" "2 HR" (tabla de fire barriers) e "INCIDENTIAL USE AREAS (TABLE 509):" "ELECTRICAL ROOMS" y los code plans 1HR FP = conflicto plano-plano; mismo criterio que DATA 118B (RFI-24). +1 capa por cara medida en su línea: la cara del corridor de W.6-L4-09 es 9.89 ft (no 8.77) y el tramo de 421 dentro de W.6-L4-08 (1.23 ft = CLG-L4-119 10.8 SF / 8.77) va por las dos caras | A0.00; 3/A0.01, 1/A0.02, 2/A0.02 | REV_A0.00_codetable, REV_A0.00_incidental_Table509_ELEC, REV_A0.02_L4_ELEC421 | +558.70 SF (Type X +480.32, W.R. +78.38 en la cara de 418 Men); DA-6 −558.70 |
| 2 | Cove de corridor 7/A7.23 | **DECIDIDO: madera (R-ALC-10), Div. 06 EXCLUDED (U-139)**. El detalle dibuja las piezas con la caja con X (igual que los top plates); el legend GYP-1 permite metal O madera y el detalle específico elige. Board de los coves sigue. Revisé cada soffit con su detalle: lobby coffers 5/A7.31 y stair FCU 11/A6.01 no dibujan madera → siguen metálicos | 7/A7.23; legend GYP-1; 5/A7.31; 11/A6.01 | REV_A7.23_7_cove_woodX, SOF_A7.31_5_lobby_coffer_no_wood, SOF_A6.01_11_stair_FCU_soffit | −2,006.94 LF track, −411.92 LF cripples (Scope: delta si fuera metal) |
| 3 | Áreas sin número del RCP | **ARREGLADO**: 18 EXCLUDED nuevos con polígono y texto dentro — hoistways y stairs W/E en A3.01-A3.03, shafts N/S en A3.02-A3.03 (motivo impreso: 1-12/A6.00, 7-11/A6.01, 1-5/A6.02, 1/A5.08, 7-8/A9.03); ELEC/TELE 120 en 2/A7.50 (grid ACT); pasillo 410/411 (73.02 SF, F&B: solo se entra desde 410 / 411, 1/A2.04). WS-1 de L4: el RS-1 del corridor 412 tenía un hueco ahí → **CARGADO RS-1 continuo** (supuesto conservador, como la FS-1 sobre el WS-1 en L2 / L3). Hallazgo extra: la membrana FS-1 de L1 cubría los 2 hoistways (que atraviesan el piso de L2) y las bases de shaft → **recortada**. Compuerta CE_RCP_CUARTOS con elementos verticales (test_rev16_verticales_rcp) | A3.01-A3.04, 2/A7.50, 1/A2.04, 6/A7.23 | REV_BLANK_*, BL_*, AFTER_A3.02_core_excluded, AFTER_A3.01_core_shaft_bases, AFTER_A7.50_120_excluded, AFTER_A3.04_passage_410_411, AFTER_A3.04_WS1_RS1 | WS-1: +34.52 SF Type X, +25.89 LF RC; FS-1 L1: −124.31 SF Type C, −93.23 LF RC |
| 4 | Review Items BAR | **CORREGIDO**: CLG-L1-125 125.98 SF, delta −125.98 (= RFI-22). Chequeo nuevo CB_CR_R16_RI (Review Items = Pending Items) | — | — | 0 |
| 5 | Table 509 | **CORREGIDO** en RFI-04 B, RFI-23 y RFI-24 B: "IBC 2018 Table 509 row 'Electrical installations and transformers' gives no hourly rating (it refers to NFPA 70 Sections 110.26-110.34 and 450.8-450.48)". Chequeo CB_CR_R16_T509 | IBC 2018 Table 509 | — | 0 |
| 6 | 2HR SHAFT CEILING | **MOVIDO** a A3.01 (plenum de L1, 1/A5.08), ids CLG-L1-SHN / SHS; en A3.02 / A3.03 los shafts quedan EXCLUDED | 1/A5.08 | AFTER_A3.01_core_shaft_bases | 0 |
| 7 | Base CBU | **UNIFICADA** = 3,694.36 SF (familia del Material Summary) | 09 29 00 2.6.E.3 | — | mesh −0.01 LF, compound −0.01 LB |

## Delta total rev15 → rev16 (NET)

| Material | Unit | rev15 | rev16 | Delta |
|---|---|---|---|---|
| 5/8" gypsum board, Type X | SF | 87,650.77 | 88,165.61 | +514.84 |
| 5/8" gypsum board, Type X W.R. | SF | 28,073.50 | 28,151.88 | +78.38 |
| 5/8" gypsum board, Type C | SF | 21,768.98 | 21,644.66 | −124.32 |
| Ceiling / soffit track | LF | 2,616.04 | 609.10 | −2,006.94 |
| 2-1/2" stud (soffit cripples) | LF | 664.97 | 253.05 | −411.92 |
| Resilient channel | LF | 19,691.55 | 19,624.20 | −67.35 |
| Joint compound, all purpose | LB | 8,491.14 | 8,524.90 | +33.76 |
| Joint tape, paper | LF | 50,872.50 | 51,046.00 | +173.50 |
| Mesh tape (CBU) | LF | 1,366.92 | 1,366.91 | −0.01 |
| Setting compound (CBU) | LB | 266.00 | 265.99 | −0.01 |

Cuadre Type X + W.R. (+593.22 SF) [DERIVADO] = ELEC 558.70 + WS-1 34.52.

## RFI abiertos
RFI-04 (furring / chases / nichos; ELEC 2 HR vs code plans → DA-6), RFI-13 (stud / C-channel MB-1), RFI-17 (cielo 128), RFI-29 (ensamble del 2HR shaft ceiling), RFI-21 y RFI-24 (tus decisiones, U-052).
