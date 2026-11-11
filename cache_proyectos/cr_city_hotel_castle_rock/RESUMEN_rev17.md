# RESUMEN rev17 — CR City Hotel (Castle Rock, CO)

rev17 reemplaza a rev16. Origen: revisión dirigida independiente de rev16 (orden tuya "revisa todo otra vez"): 5 de 7 puntos OK; 5 hallazgos. Imágenes en `Auditoria/revision_dirigida_rev17/` (REV_* = revisor, M17_* = mediciones en vectores, AFTER_* = cómo quedó).

| # | Punto | Resultado | N/HOJA | Imagen | Delta |
|---|---|---|---|---|---|
| 1 | ELEC 221: muro equivocado | **CORREGIDO**. UNTYPED-L2-12 está al ESTE del corridor 216 junto a LINEN 222; ELEC 221 es el closet al OESTE tras la puerta 221.1. Sus caras W / N / E son W.62-1 (ya 2 capas por cara, nada que agregar); falta la S (muro norte del bath 210, W.4-L2-15): 0.92 ft medido en vectores, ambas caras | 1/A2.02 | REV_A2.02_UNTYPED-L2-12_vs_ELEC221, M17_A2.02_ELEC221_S_face, AFTER_A2.02_ELEC221 | −41.76 SF (L2-12) + 17.00 SF (221 S: 8.50 Type X + 8.50 W.R. bajo el CBU del bath) |
| 2 | Tramos faltantes de 321 / 421 | **CARGADOS**. 321 S (W.4-L3-26) 0.96 ft (la E son las puertas 321.1, sin muro); 421 N (W.6-L4-03) y S (W.6-L4-08): ancho real 1.31 ft (no 1.23), cada uno en UNA fila de 2 caras | 1/A2.03, 3/A7.50 | REV_A7.50_ELEC421_m16, REV_A2.03_ELEC321_m16, M17_A2.03_…, M17_A7.50_ELEC421_N_tramo, AFTER_A7.50_ELEC421_N_S | 321: +17.74 SF; 421 N: +23.42; 421 S: +1.67 (1.23 → 1.31) |
| 3 | Leyenda W.6-1 (C + D) | **CORREGIDO**: el tramo sur de 421 es una fila W.6-L4-08 C de 2 caras | 3/A7.50 | — | 0 |
| 4 | WS-1 de L4 | **UN criterio para las 3 zonas: EXCLUDED** (polígono gris + texto). El RCP 1/A3.04 imprime WS-1; el RS-1 bajo el roof es SIN rating (A0.08 RS-1 rating en blanco, "CEILING RE: RCP"; A0.00 "ROOF CONSTRUCTION 0 HR") → nada impreso pide gypsum arriba de las slats (en L2 / L3 la FS-1 1 HR sí sigue). CLG-L4-412WS retirado. Delta si se pidiera gypsum arriba de las 3 zonas: +146.70 SF Type X + 110.03 LF RC (Scope Checklist). Chequeo nuevo CB_CR_R17_SILENCIO | 1/A3.04; A0.08 RS-1; 6/A7.23; 5/A7.23 | REV_A3.04_WS1_*, REV_A0.08_RS1_top, M17_A3.04_WS1_*, AFTER_A3.04_WS1_lobby_excluded | −34.52 SF Type X, −25.89 LF RC |
| 5 | Textos FS-1 / RS-1 | **CORREGIDOS**: Review Item WS-1 separa L2 / L3 (FS-1 1 HR sigue arriba) de L4 (RS-1 sin rating); ALC-E08 ya no dice "RS-1 rated" | A0.08, A0.00 | — | 0 |
| 6 | Soffit FCU 11/A6.01 | **CITADO**: framing no dibujado → regla fija R-ALC-01 / BE-CF11 (opción metálica), renglón de Scope con delta si fuera madera (−17.44 LF track, −16.00 LF cripples) | 11/A6.01 | REV_A6.01_11_FCU_soffit | 0 |

DA-6 (ELEC 1 HR por code plans) = −576.76 SF con las 13 filas reales.

## Delta rev16 → rev17 (NET)

| Material | Unit | rev16 | rev17 | Delta |
|---|---|---|---|---|
| 5/8" gypsum board, Type X | SF | 88,165.61 | 88,131.78 | −33.83 |
| 5/8" gypsum board, Type X W.R. | SF | 28,151.88 | 28,169.25 | +17.37 |
| Resilient channel | LF | 19,624.20 | 19,598.31 | −25.89 |
| Joint compound, all purpose | LB | 8,524.90 | 8,523.71 | −1.19 |
| Joint tape, paper | LF | 51,046.00 | 51,039.91 | −6.09 |

Cuadre Type X [DERIVADO]: −41.76 + 8.50 + 8.87 + 23.42 + 1.67 − 34.52 = −33.82 (redondeo −0.01).

Observación (no cambia cantidades del bid): CLG-L4-119 (cielo de ELEC 421) está en 10.8 SF medido en 1/A2.04; con el ancho medido en 3/A7.50 (1.31 × 8.77) daría 11.49 SF (+0.69 SF).
