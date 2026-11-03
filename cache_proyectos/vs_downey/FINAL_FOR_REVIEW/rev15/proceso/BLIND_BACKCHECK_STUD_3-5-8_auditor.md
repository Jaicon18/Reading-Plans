# BACK-CHECK ciego — 3-5/8" metal stud (todos los gauges) — Victoria's Secret #679 Downey CA

Auditor independiente. Fuentes: canon rev14 (`takeoff_canon_rev14.json`, como datos), bid set `VS679_bidset_LIMPIO.pdf` (crops PNG en esta carpeta), convenciones SKILL.md §7 / REGLA 53.2 / E1-E2. No se abrió ningún Excel ni salida del estimador. Cálculo: `recount.py`, `totals.py` (python3 -I).

## Convenciones aplicadas

- Field studs = 1 + Σ ROUNDUP(zona / O.C.) por wall (zonas de O.C. reducido del canon; sin descontar aberturas, SKILL §7 / Paso 7). Stud length = height_ft del wall (T.O. STUD ±12'-0" A/A12.01 y C/A12.01 [CONFIRMADO]; INS walls tight to structure A01.01 K19 @12'-1" / K20 @16'-8" [CONFIRMADO]; STOCK 12'-6"; SF 13'-8 1/2" A/A08.01).
- Nodes: L +1 (dueño = primer wall del node), T +1 (al through wall), free 0. Rows = 1 en todos los walls (no hay double row en el canon).
- Aberturas: 4 jambs (king + jack) a altura completa (REGLA 53.2); cripples FLOOR(R.O./O.C.) × (H − head); header DBL 3 5/8" 20 GA (S01.01 coded note 15, G/S03.01) = 2 × (R.O. + 1'-4") (E1/E2), renglón aparte.
- Diagonal bracing A/S03.01: 48" O.C. (24" donde hay shelving en ambas caras, S01.01 N note), pendiente 1:1 impresa → largo = (B.O. estructura − T.O. stud) × √2; single 3-5/8" 20 GA (todas < 10'-0").
- Compression struts J/A12.02: clusters @12'-0" O.C. ea. way y dentro de 6'-0" del perímetro → n = MAX(1, ROUNDUP(ns/12)) × MAX(1, ROUNDUP(ew/12)); largo = hanger drop.

## 1. Tabla por familia

| Familia | LF back-check | Operación | N/SHEET | Estado |
|---|---:|---|---|---|
| a) Wall field studs (104 walls 3-5/8") | 9,682.57 | Σ (1+ΣROUNDUP(zona/oc)) × H | A02.01, M/A02.01, A/A12.01, C/A12.01, A01.01 | [DERIVADO] |
| a) Nodes / corners (59 L + 49 T) | 1,307.25 | Σ (+1 por L/T) × H del host | A02.01 (nodes canon) | [DERIVADO] |
| a) W001 STOCK extension 6" | 7.50 | (1+ROUNDUP(18.17/1.333)=15) × 0.5 | C/A12.01, A03.01 (canon 7.0 = 14 pcs) | [DERIVADO] |
| b) Jambs king + jack (16 openings) | 768.33 | 16 × 4 × H (12.0; I07 12.083) | G/S03.01, A10.08 A/D/G/J/K/M | [DERIVADO] |
| b) Cripples sobre heads | 143.80 | Σ FLOOR(RO/1.333) × (H − head) | A10.08 heads, A00.02 | [DERIVADO] |
| c) Headers DBL 3-5/8" stud (renglón aparte) | 148.07 | Σ 2 × (RO + 1.333) | S01.01 coded note 15, G/S03.01 | [DERIVADO] |
| d) Diagonal bracing a estructura | 1,414.86 | 256 diag × (estr − T.O.) × √2 − W001 STOCK 5×0.5×√2 | A/S03.01, A01.01, S01.01 N note | [DERIVADO] |
| e) Compression struts (ceiling lateral bracing) | 523.91 | Σ clusters × drop (display windows con clg 11'-2") | J/A12.02, K/A12.02, A03.01, A01.01 | [DERIVADO] |
| f) Storefront piers SP1 + SP2 | 438.66 | 2 × 16 studs × 13.708 (studs por face) | A02.01, A/A08.01, A/S02.01 | [DERIVADO] |
| f) Cashwrap backwrap soffit drop studs SS1 | 46.58 | (1+ROUNDUP(15.125/1.333)=13) × 3.583 | F/A10.05, A02.01 15'-1 1/2" HOLD | [DERIVADO] |
| f) SF built-up box posts (6)+(16) | 328.99 | 12 posts × 2 × 13.708 | A/S02.01, S01.01 CN 6/16, C/S03.01 | [DERIVADO] |
| f) Grille portal head box studs | 96.24 | 2 lines × 15 × 3.208 | B/S02.01, D/A08.10 | [DERIVADO] |
| f) Display window head truss studs | 121.97 | 2 win × 2 lines × 12 × (13.708 − 11.167) | F, K/S02.01, A03.01 11'-2" P-230 | [DERIVADO] |
| f) Head truss diagonals (en canon bajo "storefront structural framing") | 64.00 | 16 × 4.0 (largo supuesto) | F/S02.01, A/S03.01 | [PENDIENTE] |
| f) Display platform joists | 87.74 | 2 × 12 × 3.656 | E/A08.05, F/K/S02.01 | [PENDIENTE] |
| f) Display platform edge box studs | 53.96 | 2 × 2 × 13.49 | F/K/S02.01 | [PENDIENTE] |
| f) Valance top framing members | 122.06 | 63 × 1.9375 | B/A10.03 | [DERIVADO] |
| f) Backwrap soffit top members | 26.55 | 13 × 2.042 | F/A10.05 | [DERIVADO] |
| f) S/S03.01 continuous suspended stud | 85.62 | 15.125+2×18.875+14.125+9.375+2×4.625 | S/S03.01, A02.01 | [CONFIRMADO] |
| f) S03.02 A1 continuous horizontal stud | 28.00 | 8 racks × 3.5 | A/S03.02, A06.01 | [PENDIENTE] |
| f) Water heater shelf jack studs | 16.00 | 2 × 8'-0" | N1/S03.01, D/A13.02 | [CONFIRMADO] |
| f) Cont. hanger studs ceiling transitions | 9.82 | 3.65 + 6.17 | E/A12.02, A/A12.02, S/S03.01 | [DERIVADO] |
| f) Recessed traffic counter stud laid on back | 2.67 | 2 × 1.333 | B/A12.02, J/A08.10 | [DERIVADO] |
| **GRAN TOTAL (incl. headers)** | **15,525.15** | | | |
| **Total sin headers** | **15,377.08** | | | |

Subtotales: (a) walls 10,997.32 · (b) openings 912.13 · (c) headers 148.07 · (d) diagonals 1,414.86 · (e) struts 523.91 · (f) other framing 1,528.86.

Referencia: con los valores del canon sin mis correcciones (display truss 170.02, struts 527.94, diagonals 1,411.15, W001 ext 7.0, sin los 64.0 LF de head-truss diagonals) el total equivalente sería 15,525.15 − 64.0 + 48.05 + 4.03 − 3.71 − 0.5 ≈ 15,509.0 LF incl. headers.

## 2. Por partition type (walls, field + nodes)

| Type | Walls | Σ L (ft) | Field LF | Nodes LF | Total LF |
|---|---:|---:|---:|---:|---:|
| FUR | 8 | 211.00 | 2028.00 | 288.00 | 2316.00 |
| STD | 82 | 436.23 | 6187.00 | 828.50 | 7015.50 |
| RFID | 4 | 59.81 | 680.50 | 97.00 | 777.50 |
| SF | 2 | 9.64 | 137.08 | 0.00 | 137.08 |
| INS | 8 | 45.05 | 649.99 | 93.75 | 743.74 |

Excluidos: W070 (6" plumbing wall), CW1-CW4 (1-5/8" column wraps R/A10.01), VAL-* (1-5/8" valance faces B/A10.03), demolición (35 misc_items), madera, 6"/8"/10" storefront beams.

## 3. Tabla por wall

| Wall | Type | L (ft) | O.C. | H (ft) | Field pcs | Nodes | Pcs | LF | Op field |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| W001 | FUR | 68.472 | 16" | 12.000 | 53 | 9 | 62 | 744.00 | 1+RU(68.472/16") |
| W007 | FUR | 20.944 | 16" | 12.000 | 17 | 2 | 19 | 228.00 | 1+RU(20.944/16") |
| W008 | FUR | 20.867 | 16" | 12.000 | 17 | 2 | 19 | 228.00 | 1+RU(20.867/16") |
| W009 | STD | 2.028 | 16" | 12.000 | 3 | 1 | 4 | 48.00 | 1+RU(2.028/16") |
| W010 | STD | 4.417 | 16" | 12.000 | 5 | 3 | 8 | 96.00 | 1+RU(4.417/16") |
| W012 | STD | 2.583 | 16" | 12.000 | 3 | 2 | 5 | 60.00 | 1+RU(2.583/16") |
| W013 | STD | 3.539 | 16" | 12.000 | 4 | 1 | 5 | 60.00 | 1+RU(3.539/16") |
| W014 | STD | 36.278 | 16" | 12.000 | 29 | 5 | 34 | 408.00 | 1+RU(36.278/16") |
| W020 | STD | 6.861 | 16" | 12.500 | 7 | 1 | 8 | 100.00 | 1+RU(6.861/16") |
| W021 | STD | 49.694 | 16" | 12.000 | 39 | 4 | 43 | 516.00 | 1+RU(49.694/16") |
| W023 | STD | 1.389 | 16" | 12.000 | 3 | 2 | 5 | 60.00 | 1+RU(1.389/16") |
| W024 | STD | 2.167 | 16" | 12.000 | 3 | 1 | 4 | 48.00 | 1+RU(2.167/16") |
| W025 | STD | 2.167 | 16" | 12.000 | 3 | 1 | 4 | 48.00 | 1+RU(2.167/16") |
| W026 | STD | 2.167 | 16" | 12.000 | 3 | 3 | 6 | 72.00 | 1+RU(2.167/16") |
| W027 | STD | 2.306 | 16" | 12.000 | 3 | 2 | 5 | 60.00 | 1+RU(2.306/16") |
| W028 | STD | 4.400 | 16" | 12.000 | 5 | 1 | 6 | 72.00 | 1+RU(4.400/16") |
| W029 | STD | 1.556 | 16" | 12.000 | 3 | 1 | 4 | 48.00 | 1+RU(1.556/16") |
| W030 | STD | 1.917 | 16" | 12.000 | 3 | 1 | 4 | 48.00 | 1+RU(1.917/16") |
| W031 | STD | 1.639 | 16" | 12.000 | 3 | 0 | 3 | 36.00 | 1+RU(1.639/16") |
| W032 | STD | 3.972 | 16" | 12.000 | 4 | 0 | 4 | 48.00 | 1+RU(3.972/16") |
| W033 | STD | 4.417 | 16" | 12.000 | 5 | 1 | 6 | 72.00 | 1+RU(4.417/16") |
| W034 | STD | 2.056 | 16" | 12.000 | 3 | 0 | 3 | 36.00 | 1+RU(2.056/16") |
| W035 | STD | 10.661 | 16" | 12.000 | 9 | 1 | 10 | 120.00 | 1+RU(10.661/16") |
| W036 | STD | 1.333 | 16" | 12.000 | 2 | 0 | 2 | 24.00 | 1+RU(1.333/16") |
| W037 | STD | 2.056 | 16" | 12.000 | 3 | 1 | 4 | 48.00 | 1+RU(2.056/16") |
| W040 | STD | 10.750 | 16" | 12.000 | 17 | 0 | 17 | 204.00 | 1+RU(0.061/16")+RU(3.739/8")+RU(3.061/16")+RU(2.700/8")+RU(1.189/16") |
| W041 | STD | 4.356 | 16" | 12.000 | 5 | 2 | 7 | 84.00 | 1+RU(4.356/16") |
| W042 | STD | 4.500 | 16" | 12.000 | 5 | 1 | 6 | 72.00 | 1+RU(4.500/16") |
| W043 | STD | 4.417 | 16" | 12.000 | 5 | 1 | 6 | 72.00 | 1+RU(4.417/16") |
| W044 | STD | 1.944 | 16" | 12.000 | 3 | 1 | 4 | 48.00 | 1+RU(1.944/16") |
| W045 | STD | 1.972 | 16" | 12.000 | 3 | 1 | 4 | 48.00 | 1+RU(1.972/16") |
| W046 | STD | 10.944 | 16" | 12.000 | 10 | 1 | 11 | 132.00 | 1+RU(10.944/16") |
| W047 | STD | 2.028 | 16" | 12.000 | 3 | 0 | 3 | 36.00 | 1+RU(2.028/16") |
| W048 | STD | 6.972 | 16" | 12.000 | 7 | 2 | 9 | 108.00 | 1+RU(6.972/16") |
| W049 | STD | 7.028 | 16" | 12.000 | 7 | 1 | 8 | 96.00 | 1+RU(7.028/16") |
| W050 | STD | 4.944 | 16" | 12.000 | 5 | 3 | 8 | 96.00 | 1+RU(4.944/16") |
| W052 | STD | 3.528 | 16" | 12.000 | 4 | 1 | 5 | 60.00 | 1+RU(3.528/16") |
| W053 | STD | 1.611 | 16" | 12.000 | 3 | 0 | 3 | 36.00 | 1+RU(1.611/16") |
| W054 | STD | 1.917 | 16" | 12.000 | 3 | 1 | 4 | 48.00 | 1+RU(1.917/16") |
| W055 | STD | 2.028 | 16" | 12.000 | 3 | 1 | 4 | 48.00 | 1+RU(2.028/16") |
| W056 | STD | 4.444 | 16" | 12.000 | 5 | 3 | 8 | 96.00 | 1+RU(4.444/16") |
| W058 | STD | 4.417 | 16" | 12.000 | 5 | 3 | 8 | 96.00 | 1+RU(4.417/16") |
| W059 | STD | 2.583 | 16" | 12.000 | 3 | 2 | 5 | 60.00 | 1+RU(2.583/16") |
| W061 | FUR | 18.194 | 16" | 12.000 | 15 | 3 | 18 | 216.00 | 1+RU(18.194/16") |
| W063 | FUR | 19.667 | 16" | 12.000 | 16 | 2 | 18 | 216.00 | 1+RU(19.667/16") |
| W064 | FUR | 21.000 | 16" | 12.000 | 17 | 2 | 19 | 228.00 | 1+RU(21.000/16") |
| W065 | FUR | 20.944 | 16" | 12.000 | 17 | 2 | 19 | 228.00 | 1+RU(20.944/16") |
| W066 | FUR | 20.917 | 16" | 12.000 | 17 | 2 | 19 | 228.00 | 1+RU(20.917/16") |
| W067 | STD | 7.006 | 16" | 12.500 | 7 | 0 | 7 | 87.50 | 1+RU(7.006/16") |
| W068 | STD | 1.167 | 16" | 12.000 | 2 | 0 | 2 | 24.00 | 1+RU(1.167/16") |
| W069 | STD | 2.139 | 16" | 12.000 | 3 | 0 | 3 | 36.00 | 1+RU(2.139/16") |
| W072 | STD | 19.889 | 16" | 12.000 | 16 | 3 | 19 | 228.00 | 1+RU(19.889/16") |
| W073 | STD | 1.167 | 16" | 12.000 | 2 | 0 | 2 | 24.00 | 1+RU(1.167/16") |
| W074 | RFID | 13.583 | 16" | 12.500 | 12 | 2 | 14 | 175.00 | 1+RU(13.583/16") |
| W075 | RFID | 4.850 | 16" | 12.500 | 5 | 0 | 5 | 62.50 | 1+RU(4.850/16") |
| W076 | RFID | 24.294 | 16" | 12.000 | 25 | 3 | 28 | 336.00 | 1+RU(0.390/16")+RU(4.833/8")+RU(19.071/16") |
| W077 | RFID | 17.083 | 16" | 12.000 | 14 | 3 | 17 | 204.00 | 1+RU(17.083/16") |
| W080 | STD | 1.528 | 16" | 12.000 | 3 | 0 | 3 | 36.00 | 1+RU(1.528/16") |
| W081 | STD | 1.556 | 16" | 12.000 | 3 | 0 | 3 | 36.00 | 1+RU(1.556/16") |
| W082 | STD | 4.739 | 16" | 12.000 | 5 | 0 | 5 | 60.00 | 1+RU(4.739/16") |
| W083 | STD | 5.122 | 16" | 12.000 | 5 | 0 | 5 | 60.00 | 1+RU(5.122/16") |
| W084 | STD | 5.111 | 16" | 12.000 | 5 | 0 | 5 | 60.00 | 1+RU(5.111/16") |
| W085 | STD | 1.528 | 16" | 12.000 | 3 | 0 | 3 | 36.00 | 1+RU(1.528/16") |
| W086 | STD | 1.556 | 16" | 12.000 | 3 | 0 | 3 | 36.00 | 1+RU(1.556/16") |
| W088 | STD | 0.417 | 16" | 12.000 | 2 | 0 | 2 | 24.00 | 1+RU(0.417/16") |
| W089 | STD | 4.639 | 8" | 12.000 | 8 | 0 | 8 | 96.00 | 1+RU(4.639/8") |
| W090 | STD | 14.944 | 8" | 12.000 | 24 | 1 | 25 | 300.00 | 1+RU(14.944/8") |
| W091 | STD | 5.117 | 16" | 12.000 | 5 | 0 | 5 | 60.00 | 1+RU(5.117/16") |
| W092 | STD | 1.778 | 16" | 12.000 | 3 | 0 | 3 | 36.00 | 1+RU(1.778/16") |
| W093 | STD | 1.806 | 16" | 12.000 | 3 | 0 | 3 | 36.00 | 1+RU(1.806/16") |
| W094 | STD | 5.111 | 16" | 12.000 | 5 | 0 | 5 | 60.00 | 1+RU(5.111/16") |
| W095 | STD | 5.111 | 16" | 12.000 | 5 | 0 | 5 | 60.00 | 1+RU(5.111/16") |
| W096 | STD | 2.389 | 16" | 12.000 | 3 | 0 | 3 | 36.00 | 1+RU(2.389/16") |
| W097 | STD | 1.806 | 16" | 12.000 | 3 | 0 | 3 | 36.00 | 1+RU(1.806/16") |
| W098 | STD | 1.833 | 16" | 12.000 | 3 | 0 | 3 | 36.00 | 1+RU(1.833/16") |
| W099 | STD | 18.694 | 16" | 12.000 | 21 | 3 | 24 | 288.00 | 1+RU(13.400/16")+RU(4.730/8")+RU(0.564/16") |
| W101 | STD | 15.472 | 8" | 12.000 | 25 | 0 | 25 | 300.00 | 1+RU(15.472/8") |
| W102 | STD | 1.833 | 16" | 12.000 | 3 | 0 | 3 | 36.00 | 1+RU(1.833/16") |
| W103 | STD | 1.833 | 16" | 12.000 | 3 | 0 | 3 | 36.00 | 1+RU(1.833/16") |
| W104 | STD | 1.833 | 16" | 12.000 | 3 | 0 | 3 | 36.00 | 1+RU(1.833/16") |
| W105 | STD | 1.833 | 16" | 12.000 | 3 | 0 | 3 | 36.00 | 1+RU(1.833/16") |
| W106 | STD | 15.378 | 8" | 12.000 | 25 | 0 | 25 | 300.00 | 1+RU(15.378/8") |
| W107 | STD | 15.472 | 8" | 12.000 | 25 | 0 | 25 | 300.00 | 1+RU(15.472/8") |
| W108 | STD | 1.833 | 16" | 12.000 | 3 | 0 | 3 | 36.00 | 1+RU(1.833/16") |
| W109 | STD | 1.833 | 16" | 12.000 | 3 | 0 | 3 | 36.00 | 1+RU(1.833/16") |
| W110 | STD | 1.833 | 16" | 12.000 | 3 | 0 | 3 | 36.00 | 1+RU(1.833/16") |
| W111 | STD | 1.833 | 16" | 12.000 | 3 | 0 | 3 | 36.00 | 1+RU(1.833/16") |
| W112 | STD | 12.422 | 16" | 12.000 | 11 | 1 | 12 | 144.00 | 1+RU(12.422/16") |
| W113 | STD | 12.544 | 16" | 12.000 | 11 | 1 | 12 | 144.00 | 1+RU(12.544/16") |
| W114 | SF | 4.861 | 16" | 13.708 | 5 | 0 | 5 | 68.54 | 1+RU(4.861/16") |
| W115 | SF | 4.778 | 16" | 13.708 | 5 | 0 | 5 | 68.54 | 1+RU(4.778/16") |
| I01 | INS | 1.833 | 16" | 16.667 | 3 | 2 | 5 | 83.34 | 1+RU(1.833/16") |
| I02 | INS | 5.150 | 16" | 16.667 | 5 | 0 | 5 | 83.34 | 1+RU(5.150/16") |
| I03 | INS | 20.750 | 12" | 12.083 | 22 | 2 | 24 | 289.99 | 1+RU(20.750/12") |
| I04 | INS | 2.167 | 16" | 12.083 | 3 | 2 | 5 | 60.41 | 1+RU(2.167/16") |
| I05 | INS | 4.333 | 16" | 12.083 | 5 | 0 | 5 | 60.41 | 1+RU(4.333/16") |
| I06 | INS | 2.178 | 16" | 12.083 | 3 | 1 | 4 | 48.33 | 1+RU(2.178/16") |
| I07 | INS | 7.750 | 16" | 12.083 | 7 | 0 | 7 | 84.58 | 1+RU(7.750/16") |
| W116 | STD | 0.833 | 16" | 12.000 | 2 | 1 | 3 | 36.00 | 1+RU(0.833/16") |
| W117 | STD | 0.528 | 16" | 12.000 | 2 | 0 | 2 | 24.00 | 1+RU(0.528/16") |
| W118 | STD | 0.528 | 16" | 12.000 | 2 | 0 | 2 | 24.00 | 1+RU(0.528/16") |
| W119 | STD | 0.861 | 16" | 12.000 | 2 | 1 | 3 | 36.00 | 1+RU(0.861/16") |
| I08 | INS | 0.889 | 16" | 16.667 | 2 | 0 | 2 | 33.33 | 1+RU(0.889/16") |
| W120 | STD | 1.389 | 16" | 12.000 | 3 | 2 | 5 | 60.00 | 1+RU(1.389/16") |
| SP1 | column_wrap | 12.646 | 16" | 13.708 | 16 | 0 | 16 | 219.33 | (1+RU(4.323/1.333))+(1+RU(2.0/1.333))+(1+RU(4.323/1.333))+(1+RU(2.0/1.333)) |
| SP2 | column_wrap | 12.646 | 16" | 13.708 | 16 | 0 | 16 | 219.33 | (1+RU(4.323/1.333))+(1+RU(2.0/1.333))+(1+RU(4.323/1.333))+(1+RU(2.0/1.333)) |
| SS1 | soffit_side | 15.125 | 16" | 3.583 | 13 | 0 | 13 | 46.58 | 1+RU(15.125/1.333) |

## 4. Aberturas (openings_extra)

| Ref | Jamb wall | R.O. | Head | H | Jambs LF (4×H) | Cripples | Cripple LF | Header LF 2×(RO+1.333) | Fuente R.O. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 5QG-AFR6 | W014 | 3.271 | 7.542 | 12.000 | 48.00 | 2 | 8.92 | 9.21 | D/A10.08 CONFIRMED: 39 1/4" (36" DOOR) R |
| 5QG-FR5 | W014 | 3.271 | 7.542 | 12.000 | 48.00 | 2 | 8.92 | 9.21 | D/A10.08 CONFIRMED: 39 1/4" (36" DOOR) R |
| 5QG-FR4 | W014 | 3.271 | 7.542 | 12.000 | 48.00 | 2 | 8.92 | 9.21 | D/A10.08 CONFIRMED: 39 1/4" (36" DOOR) R |
| 5QG-FR3 | W014 | 3.271 | 7.542 | 12.000 | 48.00 | 2 | 8.92 | 9.21 | D/A10.08 CONFIRMED: 39 1/4" (36" DOOR) R |
| 5QG-FR2 | W014 | 3.271 | 7.542 | 12.000 | 48.00 | 2 | 8.92 | 9.21 | D/A10.08 CONFIRMED: 39 1/4" (36" DOOR) R |
| 5QG-FR1 | W014 | 3.271 | 7.542 | 12.000 | 48.00 | 2 | 8.92 | 9.21 | D/A10.08 CONFIRMED: 39 1/4" (36" DOOR) R |
| 5UG | W096 | 4.500 | 7.542 | 12.000 | 48.00 | 3 | 13.37 | 11.67 | G/A10.08 CONFIRMED: 54" ROUGH OPENING (G |
| 6L-CW1 | W031 | 2.750 | 8.594 | 12.000 | 48.00 | 2 | 6.81 | 8.17 | K/A10.08 CONFIRMED: 2'-9" (28 3/4" DOOR) |
| 6L-CW2 | W037 | 2.750 | 8.594 | 12.000 | 48.00 | 2 | 6.81 | 8.17 | K/A10.08 CONFIRMED: 2'-9" R.O. |
| 6L-DW1 | W112 | 2.750 | 9.094 | 12.000 | 48.00 | 2 | 5.81 | 8.17 | J/A10.08 CONFIRMED: 2'-9" R.O. |
| 7B | W076 | 3.333 | 7.042 | 12.000 | 48.00 | 2 | 9.92 | 9.33 | A/A10.08 DERIVED: A00.02 3'-0" H.M. door |
| 8A-W | W048 | 3.333 | 7.042 | 12.000 | 48.00 | 2 | 9.92 | 9.33 | A/A10.08 DERIVED: A00.02 3'-0" H.M. door |
| 8A-E | W049 | 3.333 | 7.042 | 12.000 | 48.00 | 2 | 9.92 | 9.33 | A/A10.08 DERIVED: A00.02 3'-0" H.M. door |
| 11 | W046 | 3.333 | 7.042 | 12.000 | 48.00 | 2 | 9.92 | 9.33 | A/A10.08 DERIVED: A00.02 3'-0" H.M. door |
| TRANS4 | W021 | 3.667 | 8.125 | 12.000 | 48.00 | 2 | 7.75 | 10.00 | A02.01 3'-8" printed (TRANS #4) |
| 12 | I07 | 3.333 | 7.042 | 12.083 | 48.33 | 2 | 10.08 | 9.33 | DERIVADO: A00.02 3'-0" H.M. door + 2 x ± |

1A (rolling grille 18'-1") y SF glazing sin metal-stud header: header = SF beams (3)/(4) y grille head box (A/S02.01, B/S02.01) [CONFIRMADO en canon `opening_schedule.none`].

## 5. Diagonal bracing por wall

| Wall | L | H | Diag (mío) | Diag canon | B.O. estructura (A01.01) | Rise | LF |
|---|---:|---:|---:|---:|---:|---:|---:|
| W001 | 68.47 | 12.00 | 18 | 18 | 16.667 | 4.667 | 118.80 |
| W007 | 20.94 | 12.00 | 6 | 6 | 16.333 | 4.333 | 36.77 |
| W008 | 20.87 | 12.00 | 6 | 6 | 15.292 | 3.292 | 27.93 |
| W009 | 2.03 | 12.00 | 1 | 1 | 16.333 | 4.333 | 6.13 |
| W010 | 4.42 | 12.00 | 2 | 2 | 15.292 | 3.292 | 9.31 |
| W012 | 2.58 | 12.00 | 1 | 1 | 15.292 | 3.292 | 4.66 |
| W013 | 3.54 | 12.00 | 1 | 1 | 15.292 | 3.292 | 4.66 |
| W014 | 36.28 | 12.00 | 10 | 10 | 16.667 | 4.667 | 66.00 |
| W020 | 6.86 | 12.50 | 2 | 2 | 16.667 | 4.167 | 11.79 |
| W021 | 49.69 | 12.00 | 13 | 13 | 16.667 | 4.667 | 85.80 |
| W023 | 1.39 | 12.00 | 1 | 1 | 16.333 | 4.333 | 6.13 |
| W024 | 2.17 | 12.00 | 1 | 1 | 16.333 | 4.333 | 6.13 |
| W025 | 2.17 | 12.00 | 1 | 1 | 16.333 | 4.333 | 6.13 |
| W026 | 2.17 | 12.00 | 1 | 1 | 16.667 | 4.667 | 6.60 |
| W027 | 2.31 | 12.00 | 1 | 1 | 16.333 | 4.333 | 6.13 |
| W028 | 4.40 | 12.00 | 2 | 2 | 15.292 | 3.292 | 9.31 |
| W029 | 1.56 | 12.00 | 1 | 1 | 16.667 | 4.667 | 6.60 |
| W030 | 1.92 | 12.00 | 1 | 1 | 16.333 | 4.333 | 6.13 |
| W031 | 1.64 | 12.00 | 1 | 1 | 16.667 | 4.667 | 6.60 |
| W032 | 3.97 | 12.00 | 1 | 1 | 16.333 | 4.333 | 6.13 |
| W033 | 4.42 | 12.00 | 2 | 2 | 16.333 | 4.333 | 12.26 |
| W034 | 2.06 | 12.00 | 1 | 1 | 14.958 | 2.958 | 4.18 |
| W035 | 10.66 | 12.00 | 3 | 3 | 14.958 | 2.958 | 12.55 |
| W036 | 1.33 | 12.00 | 1 | 1 | 14.958 | 2.958 | 4.18 |
| W037 | 2.06 | 12.00 | 1 | 1 | 14.958 | 2.958 | 4.18 |
| W040 | 10.75 | 12.00 | 6 | 5 | 14.958 | 2.958 | 25.10 |
| W041 | 4.36 | 12.00 | 2 | 2 | 16.333 | 4.333 | 12.26 |
| W042 | 4.50 | 12.00 | 2 | 2 | 16.333 | 4.333 | 12.26 |
| W043 | 4.42 | 12.00 | 2 | 2 | 15.542 | 3.542 | 10.02 |
| W044 | 1.94 | 12.00 | 1 | 1 | 16.333 | 4.333 | 6.13 |
| W045 | 1.97 | 12.00 | 1 | 1 | 14.958 | 2.958 | 4.18 |
| W046 | 10.94 | 12.00 | 3 | 3 | 14.958 | 2.958 | 12.55 |
| W047 | 2.03 | 12.00 | 1 | 1 | 14.958 | 2.958 | 4.18 |
| W048 | 6.97 | 12.00 | 2 | 2 | 14.958 | 2.958 | 8.37 |
| W049 | 7.03 | 12.00 | 2 | 2 | 14.958 | 2.958 | 8.37 |
| W050 | 4.94 | 12.00 | 2 | 2 | 14.958 | 2.958 | 8.37 |
| W052 | 3.53 | 12.00 | 1 | 1 | 15.542 | 3.542 | 5.01 |
| W053 | 1.61 | 12.00 | 1 | 1 | 14.958 | 2.958 | 4.18 |
| W054 | 1.92 | 12.00 | 1 | 1 | 16.333 | 4.333 | 6.13 |
| W055 | 2.03 | 12.00 | 1 | 1 | 16.333 | 4.333 | 6.13 |
| W056 | 4.44 | 12.00 | 2 | 2 | 16.333 | 4.333 | 12.26 |
| W058 | 4.42 | 12.00 | 2 | 2 | 15.542 | 3.542 | 10.02 |
| W059 | 2.58 | 12.00 | 1 | 1 | 15.542 | 3.542 | 5.01 |
| W061 | 18.19 | 12.00 | 5 | 5 | 14.958 | 2.958 | 20.92 |
| W063 | 19.67 | 12.00 | 5 | 5 | 14.958 | 2.958 | 20.92 |
| W064 | 21.00 | 12.00 | 6 | 6 | 16.333 | 4.333 | 36.77 |
| W065 | 20.94 | 12.00 | 6 | 6 | 15.542 | 3.542 | 30.05 |
| W066 | 20.92 | 12.00 | 6 | 6 | 15.542 | 3.542 | 30.05 |
| W067 | 7.01 | 12.50 | 2 | 2 | 16.667 | 4.167 | 11.79 |
| W068 | 1.17 | 12.00 | 1 | 1 | 14.958 | 2.958 | 4.18 |
| W069 | 2.14 | 12.00 | 1 | 1 | 14.958 | 2.958 | 4.18 |
| W070 | 5.56 | 12.00 | 2 | 2 | 14.958 | 2.958 | 8.37 |
| W072 | 19.89 | 12.00 | 5 | 5 | 14.958 | 2.958 | 20.92 |
| W073 | 1.17 | 12.00 | 1 | 1 | 14.958 | 2.958 | 4.18 |
| W074 | 13.58 | 12.50 | 4 | 4 | 16.667 | 4.167 | 23.57 |
| W075 | 4.85 | 12.50 | 2 | 2 | 16.667 | 4.167 | 11.79 |
| W076 | 24.29 | 12.00 | 8 | 8 | 16.667 | 4.667 | 52.80 |
| W077 | 17.08 | 12.00 | 5 | 5 | 14.958 | 2.958 | 20.92 |
| W080 | 1.53 | 12.00 | 1 | 1 | 16.667 | 4.667 | 6.60 |
| W081 | 1.56 | 12.00 | 1 | 1 | 14.958 | 2.958 | 4.18 |
| W082 | 4.74 | 12.00 | 2 | 2 | 16.667 | 4.667 | 13.20 |
| W083 | 5.12 | 12.00 | 2 | 2 | 16.667 | 4.667 | 13.20 |
| W084 | 5.11 | 12.00 | 2 | 2 | 16.333 | 4.333 | 12.26 |
| W085 | 1.53 | 12.00 | 1 | 1 | 16.333 | 4.333 | 6.13 |
| W086 | 1.56 | 12.00 | 1 | 1 | 16.333 | 4.333 | 6.13 |
| W088 | 0.42 | 12.00 | 1 | 1 | 16.333 | 4.333 | 6.13 |
| W089 | 4.64 | 12.00 | 3 | 3 | 16.333 | 4.333 | 18.38 |
| W090 | 14.94 | 12.00 | 8 | 8 | 16.333 | 4.333 | 49.02 |
| W091 | 5.12 | 12.00 | 2 | 2 | 16.333 | 4.333 | 12.26 |
| W092 | 1.78 | 12.00 | 1 | 1 | 16.333 | 4.333 | 6.13 |
| W093 | 1.81 | 12.00 | 1 | 1 | 16.333 | 4.333 | 6.13 |
| W094 | 5.11 | 12.00 | 2 | 2 | 16.333 | 4.333 | 12.26 |
| W095 | 5.11 | 12.00 | 2 | 2 | 16.333 | 4.333 | 12.26 |
| W096 | 2.39 | 12.00 | 1 | 1 | 16.333 | 4.333 | 6.13 |
| W097 | 1.81 | 12.00 | 1 | 1 | 16.333 | 4.333 | 6.13 |
| W098 | 1.83 | 12.00 | 1 | 1 | 16.333 | 4.333 | 6.13 |
| W099 | 18.69 | 12.00 | 7 | 6 | 16.333 | 4.333 | 42.89 |
| W101 | 15.47 | 12.00 | 8 | 8 | 16.333 | 4.333 | 49.02 |
| W102 | 1.83 | 12.00 | 1 | 1 | 16.333 | 4.333 | 6.13 |
| W103 | 1.83 | 12.00 | 1 | 1 | 16.333 | 4.333 | 6.13 |
| W104 | 1.83 | 12.00 | 1 | 1 | 15.292 | 3.292 | 4.66 |
| W105 | 1.83 | 12.00 | 1 | 1 | 15.542 | 3.542 | 5.01 |
| W106 | 15.38 | 12.00 | 8 | 8 | 15.292 | 3.292 | 37.24 |
| W107 | 15.47 | 12.00 | 8 | 8 | 15.542 | 3.542 | 40.07 |
| W108 | 1.83 | 12.00 | 1 | 1 | 15.292 | 3.292 | 4.66 |
| W109 | 1.83 | 12.00 | 1 | 1 | 15.542 | 3.542 | 5.01 |
| W110 | 1.83 | 12.00 | 1 | 1 | 15.292 | 3.292 | 4.66 |
| W111 | 1.83 | 12.00 | 1 | 1 | 15.542 | 3.542 | 5.01 |
| W112 | 12.42 | 12.00 | 4 | 4 | 15.292 | 3.292 | 18.62 |
| W113 | 12.54 | 12.00 | 4 | 4 | 15.542 | 3.542 | 20.04 |
| W116 | 0.83 | 12.00 | 1 | 1 | 14.958 | 2.958 | 4.18 |
| W117 | 0.53 | 12.00 | 1 | 1 | 16.333 | 4.333 | 6.13 |
| W118 | 0.53 | 12.00 | 1 | 1 | 16.667 | 4.667 | 6.60 |
| W119 | 0.86 | 12.00 | 1 | 1 | 16.333 | 4.333 | 6.13 |
| W120 | 1.39 | 12.00 | 1 | 1 | 16.667 | 4.667 | 6.60 |

## 6. Compression struts por ceiling

| Room | NS | EW | SF | Clusters | Drop | LF |
|---|---:|---:|---:|---:|---:|---:|
| MGR OFFICE | 12.93 | 6.67 | 81 | 2 | 6.958 | 13.92 |
| CORRIDOR (E of BREAK ROOM) | 6.17 | 17.33 | 107 | 2 | 6.958 | 13.92 |
| HALLWAY | 17.31 | 4.89 | 85 | 2 | 5.958 | 11.92 |
| RESTROOM W | 8.76 | 7.31 | 64 | 1 | 6.958 | 6.96 |
| RESTROOM E | 8.75 | 7.31 | 64 | 1 | 6.958 | 6.96 |
| AFR6 | 11.36 | 5.17 | 59 | 1 | 7.667 | 7.67 |
| FR5 | 4.50 | 5.17 | 23 | 1 | 7.667 | 7.67 |
| FR4 | 4.50 | 5.17 | 23 | 1 | 7.667 | 7.67 |
| FR3 | 4.50 | 5.17 | 23 | 1 | 7.333 | 7.33 |
| FR2 | 4.50 | 5.17 | 23 | 1 | 7.333 | 7.33 |
| FR1 | 4.50 | 5.17 | 23 | 1 | 7.333 | 7.33 |
| FR ALCOVE | 37.98 | 4.58 | 174 | 4 | 7.667 | 30.67 |
| FR LOUNGE | 13.28 | 10.17 | 125 | 2 | 7.333 | 14.67 |
| GO-BACK | 5.00 | 2.00 | 10 | 1 | 7.333 | 7.33 |
| CW CLOSET 1 | 2.08 | 4.83 | 10 | 1 | 5.791 | 5.79 |
| CW CLOSET 2 | 2.08 | 4.15 | 9 | 1 | 5.791 | 5.79 |
| ROOM 4 BEAUTY 3 | 24.44 | 48.33 | 995 | 15 | 6.167 | 92.50 |
| ROOM 3 VSL 3 | 24.31 | 48.33 | 1175 | 15 | 5.333 | 80.00 |
| ROOM 2 VSL 2 | 24.31 | 58.89 | 1431 | 15 | 5.333 | 80.00 |
| ROOM 1 VSL 1 | 24.44 | 58.89 | 1440 | 15 | 5.250 | 78.75 |
| VS DISPLAY WINDOW 1 | 3.56 | 13.49 | 48 | 2 | 4.750 | 9.50 |
| VS DISPLAY WINDOW 2 | 3.56 | 13.49 | 48 | 2 | 4.375 | 8.75 |
| DISPLAY BLIND VESTIBULES 1+2 | 3.56 | 13.49 | 26 | 2 | 5.750 | 11.50 |

Clusters re-derivados = canon en las 23 rooms (Σ canon 527.94 LF; mío 523.91 por la corrección de drop en display windows).

## 7. Spot-checks contra el plano

| Item | Canon | Plano | Resultado | Crop |
|---|---|---|---|---|
| W001 FUR (N demising) | 68.47 ft | ±18'-0 7/8" + RFID 4 7/8" + 49'-7" = 68.06 ft (A02.01) | Δ 0.6 % OK [CONFIRMADO] | W001_W021_A0201.png |
| W021 STD (FR alcove/lounge S) | 49.69 ft | 37'-11 3/4" + TRANS4 3'-8" + 7'-11 3/8" = 49.59 ft (A02.01) | Δ 0.2 % OK [CONFIRMADO] | W014_W021_A0201.png |
| W014 STD (FR front) | 36.28 ft | 11'-4 5/8" + 5 × 4'-6" HOLD + 5 partitions ≈ 35.92 ft; banda incluye el R.O. de AFR6 | Δ 1.0 % OK | W014_W021_A0201.png |
| W076 RFID | 24.29 ft | 4'-10" + 15'-1 1/2" HOLD + 4'-1 3/4" + partitions ≈ 24.1-24.3 | OK; cross-hatch RFID confirmado | W076_A0201.png |
| W007 FUR (Garcy niche N) | 20.94 ft | 20'-3" (19'-3" OVERALL + 2 × 6") + 2 returns 4 1/4" = 20.96 | OK (H wall dueño de L corners) | W007_W008_A0201.png |
| W064/W065 FUR | 21.0 / 20.94 | niches simétricos a W007/W008, 2'-2" profundidad | OK visual | W064_W065_A0201.png |
| Altura STD/FUR/RFID | 12.0 | A/A12.01 "±12'-0" A.F.F. T.O. STUD" | [CONFIRMADO] | A_A1201.png |
| Altura INS I03-I07 | 12.083 | A01.01 keynote 19 "@12'-1"" sobre el demising W | [CONFIRMADO] | A0101_west.png |
| Header | DBL 3-5/8" 20 GA + track | S01.01 coded note 15 "HEADER: DOUBLE 3 5/8", 20 GA WITH 3 5/8", 20 GA TRACK AT BOTTOM"; G/S03.01 king + jack | [CONFIRMADO] | G_S0301.png |
| Diagonal bracing | 48" O.C., 1:1, single 3-5/8" 20 GA ≤ 10'-0" | A/S03.01 impreso igual (interior partitions y storefront framing 48" O.C.) | [CONFIRMADO] | A_S0301.png |
| Struts | @12' ea. way, 6' perímetro | J/A12.02 "COMPRESSION STRUT @ 12'-0" O.C. EA. WAY AND WITHIN 6'-0" OF PERIMETER"; K chart EMT | [CONFIRMADO] regla; ver hallazgo 3 | J_A1202.png, K_A1202.png, N_A1202.png |
| SF box posts | 12 posts | A/S02.01: 4 posts por pier (tags 6 y 16) × 2 piers + posts en extremos de display windows | OK 12 | A_S0201_piers.png |
| Display head truss | 2 lines @16", alto 3.542 | F/S02.01 a 1"=1'-0": truss ≈ 2.5 ft; A03.01 display window = 11'-2" P-230 | **Error de altura** (hallazgo 1) | F_S0201.png, DW_A0301.png |
| Grille portal head box | 2 stud lines | B/S02.01 dibuja 3 líneas verticales de 3-5/8" (frente, centro, fondo) | posible faltante (hallazgo 4) | B_S0201.png |

## 8. Faltantes, doble conteo y tamaños dudosos (con evidencia)

1. **Display window head truss studs con altura equivocada (−48.05 LF) [CONFIRMADO].** El canon usa 13'-8 1/2" − 10'-2" = 3.542. A03.01 imprime "VS DISPLAY WINDOW #1 11'-2" P-230" (el tag 10'-2" es la franja del display blind vestibule). F/S02.01 a escala 1"=1'-0" da un truss de ≈2.5 ft. Correcto: 2 × 2 × 12 × 2.541 = 121.97 LF (canon 170.02). El mismo campo del canon está inconsistente: `ceilings[VS DISPLAY WINDOW].height_ft` = 11.167 pero `height_source` dice 10'-2".
2. **Struts de display windows (−4.03 LF) [DERIVADO].** Drop con clg 11'-2": DW1 15.917 − 11.167 = 4.75 (canon 5.75), DW2 15.542 − 11.167 = 4.375 (canon 5.375).
3. **Compression struts: alcance dudoso (hasta −285 LF) [PENDIENTE / RFI].** J y K/A12.02 son detalles de ACOUSTICAL CEILING TILE high seismic; los P-230 son gyp board on suspension grid (N/A12.02), y N/A12.02 no dibuja splay wires ni struts. K/A12.02 note 3: "CEILING AREA > 1000 SQ FT TO HAVE HORIZONTAL RESTRAINT WIRE AND RIGID BRACING" → solo ROOM 1, 2, 3 (1,175-1,440 SF) califican = 238.74 LF; ROOM 4 = 995 SF (< 1000) y todas las rooms pequeñas quedan fuera. Además el chart de K pide EMT (1.25"/1.5" dia), no metal stud (decisión del estimador R-ALC-12). Llevo los 523.91 como conservador.
4. **Grille portal head box: tercera línea de studs no contada (+48.12 LF) [PENDIENTE].** B/S02.01 dibuja una línea vertical central de 3 5/8" además de las de frente y fondo ("3 5/8", 20 GA. (MIN) METAL STUDS @ 16" O.C. TYP UNLESS NOTED"): 15 × 3.208 = 48.12 LF.
5. **Diagonal braces del storefront a estructura no contadas (≈ +53 LF) [PENDIENTE].** P, K, F y B/S02.01 rotulan "3 5/8" DIAG BRACE. SEE DETAIL A/S03.01" desde el top track del storefront / head truss a los joists; A/S03.01 "STOREFRONT FRAMING – 48" O.C. MAX". DIAG-BRACE del canon solo cubre partitions interiores (W114/W115 y los heads no están en `diag_brace_bays_info`). Estimado: W114 2 + W115 2 + grille 5 + display 2 × 4 = 17 diag × (15.917 − 13.708) × √2 = 17 × 3.12 ≈ 53 LF (B.O. estructura en la fachada no impreso: RFI).
6. **"ADDITIONAL STUD REQ'D AT EQ. STUDS. REFER TO STRUCT. DWGS." (A/A12.01 y C/A12.01) — no tratado en el canon (hasta +3,077 LF) [PENDIENTE / RFI].** Si significa un stud adicional en cada stud que recibe diagonal: 256 diag × H del wall = 3,077 LF. A/S03.01 solo pide "CENTER DIAGONAL OVER VERTICAL STUD" y (2)-#8 extra, sin stud adicional, por eso no lo sumo; pero la nota arquitectónica existe y no tiene destino en el canon (ningún campo la cita).
7. **Posible doble conteo SP1/SP2 vs SF box posts (hasta −219.3 LF) [PENDIENTE].** Las faces de SP1/SP2 se cuentan con 1 + ROUNDUP por face (4 corners × 2 end studs por pier) y además los 8 posts de las esquinas de los piers (tags 6/16, A/S02.01, C/S03.01 box columns) se cuentan en "SF built-up box posts". Si el post ES el stud de esquina: −16 studs × 13.708 = −219.3 LF.
8. **Field studs dentro del R.O. (−168 LF alternativa) [CRITERIO].** 7 aberturas dentro del run (6 × 5QG en W014 y TRANS4 en W021) no descuentan field studs (SKILL §7 "sin deducir aberturas"); REGLA 58.1 ("Nunca stud completo y cripple en la misma posición... Los field studs dentro de un R.O. se restan") daría −7 × 2 × 12 = −168 LF. Contradicción interna del SKILL: el estimador debe fijar una.
9. **Jack studs a altura completa (−139.34 LF alternativa) [CRITERIO].** REGLA 53.2 cuenta king + jack a altura completa (768.33); G/S03.01 dibuja el jack hasta el head: 2 × H + 2 × head = 628.99.
10. **Head truss diagonals (64.0 LF) mal clasificadas.** Son "3 5/8", 20 GA DIAGONAL" (F/S02.01) = material 3-5/8" stud, pero el canon las pone en la familia "storefront structural framing (printed)". Además el largo 4.0 ft es supuesto; a escala F/S02.01 ≈ 3.3 ft (16 × 3.3 ≈ 53 LF).
11. **W001 STOCK extension:** canon 14 pcs (ROUNDUP sin +1); convención 1 + ROUNDUP = 15 → 7.5 LF (+0.5).
12. **Diagonals:** mi conteo por zonas da W040 6 (canon 5) y W099 7 (canon 6); el canon suma "+1 not located per wall" sin ubicación. Neto mío 1,414.86 vs canon 1,411.15 (+3.71).
13. **S03.02 A1 "CONTINUOUS HORIZONTAL STUD" = 28 LF por rack (8 × 3.5).** "Continuous" podría pedir el largo completo de los stock walls con racks (W001 STOCK 18.17 + W067 7.01 + W074/W075/W076): delta posible +20 a +40 LF [PENDIENTE].
14. **Sin hallazgo:** todos los clusters de struts (23 rooms), box posts, grille head (2 líneas), valance/backwrap top members, suspended stud y platform re-derivan exactos desde sus op. Ningún node cae sobre un wall que no sea 3-5/8". No hay double row ni walls de 3-5/8" con openings internos en `walls[].openings` (todas las aberturas están en `openings_extra`).

## 9. Confianza

- Walls (a): alta (±1 %): largos spot-checked contra cotas impresas (W001, W021, W014, W076, W007), alturas confirmadas en A/A12.01 y A01.01; la regla de nodes es la del SKILL.
- Openings (b/c): alta en cantidad (R.O. impresos A10.08); media en convención (hallazgos 8-9).
- Diagonals (d): media-alta: regla impresa A/S03.01; las alturas de estructura por bay vienen de la lectura A01.01 del canon (spot-check K19 @12'-1" y @12'-8" OK).
- Struts (e): baja en alcance (hallazgo 3), alta en aritmética.
- Other framing (f): media; tres partidas PENDIENTE del estimador (platform, edge box, A1) y hallazgos 1, 4, 5, 7.
- Rango razonable del total 3-5/8" stud: ≈ 14,850 LF (aplicando 3, 7 y 8 a la baja) a ≈ 15,670 LF (sumando 4, 5, 13), sin la nota "ADDITIONAL STUD" (hallazgo 6), que por sí sola podría sumar ~3,077 LF.
