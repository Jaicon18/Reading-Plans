# ELEMENTO 3 — STUDS por tamaño/gauge y Z-furring (O'Reilly Evans CO #1, pasada 2)
Números: canon + overlay (rev6) → canon.py (studs.py / familias). LF NET sin waste; el conteo por wall es del programa (campo ROUNDUP(L/oc)+1, − dentro de R.O., + jambs, + nodos; cripples aparte). Detalle con operación: ELEMENTO_3_STUDS.json; proceso/rev6_cambios.md, img_rev6/. Tiempo: ~8 min + revisión rev6.
Fuentes de tamaño/gauge/O.C.: INTERIOR WALL TYPES A1.1 (S21 150ZF125-18 @ 24"; S24/S41/S42/S43 362S162-33 @ 24"; S61 600S162-33); 1/S5.3, 3/S5.3 keys 17/18/22 (EXT 800S162-54 + 600S162-54 @ 16"; cornice 600S162-43 min.); 3/A3.1 key 8 + decisión RFI-14 (VH 600S162-43); 7/A4.2 key 5 (joists 600S162-54); 1/2/4/5 S5.1 (header walls S42). S21 gauge corregido: 150ZF125-18 = 18 mil = 25 ga (S1.1 nota 7.A; antes decía 18 ga).

## Totales por tamaño / gauge (LF)
| Tamaño | Gauge | Walls | Miembros misc | Total |
|---|---|---|---|---|
| 1-1/2" Z-furring 150ZF125-18 | 25 ga (18 mil) | 2,517.50 | — | **2,517.50** |
| 8" 800S162-54 | 16 ga | 537.32 | — | **537.32** |
| 6" 600S162-54 | 16 ga | 537.32 (EXT-MS-6, HEAD-A-6) | joists 176.88 (office 56.0, R.R. 47.0 + 47.0, vest. 26.88; 7/A4.2, 3/A3.1; RFI-04 dirección) | 714.20 |
| 6" 600S200-54 | 16 ga | — | CONT S42-03 100.67 (2/S5.1) · PEMB S42-02 70.0 (1/S5.1 @ 24") · PEMB S42-01 55.0 (4/S5.1 @ 48") — largo 5.0 = RFI-19 opción A | 225.67 |
| 6" 600S162-43 | 18 ga | 291.70 (CORN-S 223.13 · VH 68.57) | — | 291.70 |
| 6" 600S162-33 | 20 ga | 68.00 (S61) | — | 68.00 |
| **6" familia** | | 897.02 | 402.55 | **1,299.57** |
| 3-5/8" 362S162-33 | 20 ga | 1,570.19 | kickers 155.54 (22 @ 48" CONFIRMADO; largo RFI-03) · lateral strut 75.79 · angled strut 64.0 (5/S5.1) | **1,865.52** |

## Por wall
| Type | Wall ID | Stud | Gauge | O.C. | H (ft) | Piezas | LF |
|---|---|---|---|---|---|---|---|
| S21 | S21-N | 1-1/2" Z-furring (150ZF125-18) | 25 ga; 18 mil, 150ZF125-18 | 24 | 14.844 | 52 + 5 cripples | 807.77 |
| S21 | S21-E | 1-1/2" Z-furring (150ZF125-18) | 25 ga; 18 mil, 150ZF125-18 | 24 | 13.958 | 46 + 0 cripples | 642.07 |
| S21 | S21-S | 1-1/2" Z-furring (150ZF125-18) | 25 ga; 18 mil, 150ZF125-18 | 24 | 14.844 | 43 + 20 cripples | 753.08 |
| S21 | S21-W1 | 1-1/2" Z-furring (150ZF125-18) | 25 ga; 18 mil, 150ZF125-18 | 24 | 15.729 | 6 + 0 cripples | 94.37 |
| S21 | S21-W2 | 1-1/2" Z-furring (150ZF125-18) | 25 ga; 18 mil, 150ZF125-18 | 24 | 15.729 | 14 + 0 cripples | 220.21 |
| EXT | EXT-MS1-8 | 8" | 16 ga; 54 mil, 800S162-54 | 16 | 20.667 | 6 + 0 cripples | 124.0 |
| EXT | EXT-MS1-6 | 6" | 16 ga; 54 mil, 600S162-54 | 16 | 20.667 | 6 + 0 cripples | 124.0 |
| EXT | EXT-MS2-8 | 8" | 16 ga; 54 mil, 800S162-54 | 16 | 20.667 | 6 + 0 cripples | 124.0 |
| EXT | EXT-MS2-6 | 6" | 16 ga; 54 mil, 600S162-54 | 16 | 20.667 | 6 + 0 cripples | 124.0 |
| EXT | HEAD-A-8 | 8" | 16 ga; 54 mil, 800S162-54 | 16 | 9.333 | 31 + 0 cripples | 289.32 |
| EXT | HEAD-A-6 | 6" | 16 ga; 54 mil, 600S162-54 | 16 | 9.333 | 31 + 0 cripples | 289.32 |
| EXT | CORN-S | 6" | 18 ga; 43 mil, 600S162-43) minimum | 16 | 7.969 | 28 + 0 cripples | 223.13 |
| S24 | S24-OF | 3-5/8" | 20 ga; 33 mil, 362S162-33 | 24 | 8.5 | 7 + 0 cripples | 59.5 |
| S24 | S24-RR | 3-5/8" | 20 ga; 33 mil, 362S162-33 | 24 | 8.5 | 12 + 0 cripples | 102.0 |
| S24 | S24-RRS | 3-5/8" | 20 ga; 33 mil, 362S162-33 | 24 | 8.5 | 6 + 0 cripples | 51.0 |
| S43 | S43-OF-W | 3-5/8" | 20 ga; 33 mil, 362S162-33 | 24 | 8.5 | 6 + 0 cripples | 51.0 |
| S43 | S43-OF-E | 3-5/8" | 20 ga; 33 mil, 362S162-33 | 24 | 8.5 | 6 + 0 cripples | 51.0 |
| S43 | S43-OF-S | 3-5/8" | 20 ga; 33 mil, 362S162-33 | 24 | 8.5 | 12 + 1 cripples | 103.33 |
| S43 | S43-RR-W | 3-5/8" | 20 ga; 33 mil, 362S162-33 | 24 | 8.5 | 6 + 0 cripples | 51.0 |
| S61 | S61-RR | 6" | 20 ga; 33 mil, 600S162-33 | 24 | 8.5 | 8 + 0 cripples | 68.0 |
| S43 | S43-RR-S | 3-5/8" | 20 ga; 33 mil, 362S162-33 | 24 | 8.5 | 18 + 2 cripples | 155.67 |
| S41 | S41-B1V | 3-5/8" | 20 ga; 33 mil, 362S162-33 | 24 | 12.0 | 5 + 0 cripples | 60.0 |
| S41 | S41-B1H | 3-5/8" | 20 ga; 33 mil, 362S162-33 | 24 | 12.0 | 3 + 0 cripples | 36.0 |
| S41 | S41-B2H | 3-5/8" | 20 ga; 33 mil, 362S162-33 | 24 | 12.0 | 4 + 0 cripples | 48.0 |
| S41 | S41-B2V | 3-5/8" | 20 ga; 33 mil, 362S162-33 | 24 | 12.0 | 3 + 0 cripples | 36.0 |
| S42 | S42-01 | 3-5/8" | 20 ga; 33 mil, 362S162-33 | 24 | 14.505 | 22 + 0 cripples | 319.11 |
| S42 | S42-02 | 3-5/8" | 20 ga; 33 mil, 362S162-33 | 24 | 7.672 | 14 + 0 cripples | 107.41 |
| S42 | S42-03 | 3-5/8" | 20 ga; 33 mil, 362S162-33 | 24 | 8.202 | 28 + 0 cripples | 229.66 |
| S42 | S42-04 | 3-5/8" | 20 ga; 33 mil, 362S162-33 | 24 | 15.644 | 7 + 0 cripples | 109.51 |
| EXT | VH-C | 6" | 18 ga; 43 mil, 600S162-43 | 24 | 4.286 | 8 + 0 cripples | 34.29 |
| EXT | VH-B2 | 6" | 18 ga; 43 mil, 600S162-43 | 24 | 4.286 | 4 + 0 cripples | 17.14 |
| EXT | VH-B1 | 6" | 18 ga; 43 mil, 600S162-43 | 24 | 4.286 | 4 + 0 cripples | 17.14 |

## RFIs del elemento
- RFI-19 (nuevo): purlin spacing / largo de miembro por shop drawing PEMB, no impreso (revisadas 1/2/4/5 S5.1, S4.1, S1.1 n.7/9, S5.2, S5.3, A3.1, A3.2 "T.O. PURLIN EL. (VARIES)"). Cargado A (5'-0"± de 2/S5.1 como sustituto): PEMB S42-02 70.0 LF (B 140.0, +70.0) · PEMB S42-01 55.0 LF (B 110.0, +55.0) · L4x4 12 pcs (B 14, +2). El 5.0 escalado se quitó.
- 2/S5.1 imprime una 3.ª línea continua 600S200-54 en el tope de kickers de S42-03 (+50.33 LF), NO cargada → para el estimador.
- RFI-03: largo de kicker no impreso: A 155.54 LF cargado / B 121.58 LF (−33.96) por elevaciones impresas (1'-0"± sobre ceiling 111'-6" a purlin RFI-01).
- RFI-04: dirección de joists de office / R.R. no impresa. RFI-01: alturas S21 / S42 con purlin 8" supuesto.

## rev2 (rev7 del canon) — cambios
- 3.ª línea CONT 600S200-54 en el tope de kickers de S42-03, IMPRESA en 2/S5.1: + 50.33 LF (6"). RFI-19 = A y RFI-03 = A cerrados (usuario).
- Stud ties 3/S5.3 key 19 (362S162-43 @ 48", 1'-2" sobre el par 6"+8"): head storefront A (S4.1 corta 3/S5.3 dos veces) = 30 pares × 4 filas × 1'-2" = + 140.0 LF; piers EXT-MS1/MS2 no cortados ni dibujados (1/A3.1) → supuesto conservador cargado RFI-11 B = + 98.0 LF (84 ties × 1'-2"), A = 0.
- Studs dobles en control joints: impresos en A4.2 key 4 ("362S162-33 studs doubled at control joint", 2/A4.2) → +1 stud por lado en las 2 juntas de S42 a la altura de cada wall = 14.505 + 7.672 + 8.202 + 15.644 = + 46.02 LF. S21 / piers: nada impreso (7/A3.2 solo vee joint; S21 = Z-furring).
- Z-furring detrás de S24: confirmado sin cambio. Sube al eave bajo purlin (E 13.958 = low eave 114'-7 1/2" − 8"; S zona R.R. 104 14.055 local, promedio de rake 14.844 exacto para el wall). Sin doble conteo: el Z-furring está en S21-E/S; S24 solo 362S162-33 a 8'-6" (212.5 LF). Total Z-furring 2,517.50 (zonas S24 ≈ 265 LF dentro). La cifra 321.55 de la otra lectura reinicia el conteo 1+ROUNDUP por zona aunque el furring es continuo.
- Totales nuevos: 3-5/8" 2,149.54 LF (+284.02: ties 140.0 + 98.0, dobles CJ 46.02) · 6" 1,349.90 LF (+50.33) · 8" 537.32 · Z-furring 2,517.50.
- Nota: HEAD-A tiene 31 studs por programa (38.667 redondeado); la R.O. impresa 38'-8" da 30 pares (usado en ties).
