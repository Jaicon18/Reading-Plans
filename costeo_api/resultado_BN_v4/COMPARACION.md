# B&N — corrida real #4 del runner (2026-10-30): conteos por type (R80e.40)

Sonnet, PDF limpio, overlay `decisiones_BN.json` + reconciliación geométrica, reglas.py encendido, cada llamada en sandbox. Compuerta nueva de completitud por conteos (commit 9f8ec2e). Tope autorizado por el usuario: $15 adicionales.

## Resultado
- **Lecturas mucho más completas.** A trae 56 walls / 633.07 LF y B 50 walls / 653.23 LF; en la #3 eran 27 y 31. La compuerta de conteos obligó a continuar las dos lecturas sobre tags concretos. En el canon final:
  - todos los tags del inventario tienen su wall;
  - las 9 columnas tienen column wrap;
  - las líneas discontinuas de A-221 tienen soffit side o su motivo.
- **LF final: 641.35 contra 707.12 de rev13 (−9.3 %).** La #3 dio −26.1 %.
- **El Excel se armó** (`Takeoff_BN_runner_v4.xlsx`). La compuerta reglas.py que corre dentro del armado dio OK, y alcances.py ya pasa: la corrección cuantificó el metal trim (ALC-18).
- **⚠️ NO ENTREGABLE.** reglas.py después del armado tiene 3 fallas:
  - la del back-check pendiente, que es paso humano y está aceptada;
  - 2 que son la misma: la fila F-01 (type F, F/A-221) del Partition Takeoff queda **PENDING**. Tiene 9.75 LF y 20 ft, pero 0 layers de board.
  - La siguiente corrección se cortó por falta de presupuesto y dejó el canon fuera de esquema. El runner no lo copió: el canon bueno quedó intacto.
- **Cobertura (paso 12): no corrió.** No quedó presupuesto.
- **Costo: $15.0078**, contra un tope de $15.00. El tope de `claude -p --max-budget-usd` no es exacto y la última llamada se pasó $0.008 (BE-75).

## Costo por paso (corrida #4)
| Paso | Llamadas | USD | Output tokens | Cache read | Seg |
|---|---|---|---|---|---|
| Proceso, inventario_tags, comparar, Excel, compuertas (scripts) | — | 0.00 | — | — | — |
| Lectura A | 1 | 4.27 | 94,764 | 20.01 M | 921 |
| Lectura A — continuación (conteos) | 1 | 1.27 | 41,867 | 5.26 M | 354 |
| Lectura B | 1 | 3.58 | 93,302 | 19.13 M | 998 |
| Lectura B — continuaciones (conteos + cruce con A) | 4 | 2.09 | 31,573 | 12.84 M | 402 |
| Resolución (59 diferencias) | 1 | 0.29 | 3,447 | 1.29 M | 47 |
| Corrección dirigida (canon.py, reglas.py, accesorios, ALC-18, ticks) | 12 | 3.51 | 41,099 | 21.20 M | 599 |
| Cobertura | 0 | — (sin presupuesto) | | | |
| **Total corrida #4** | 20 | **15.0078** | | | |

Total histórico: #1 $4.99 + #2 $11.04 + #3 $13.56 + #4 $15.01 = **$44.60**. El detalle por llamada está en `costos_run4.csv`.

## Walls leídos vs inventario (R80e.40)
Partition tags del inventario por hoja y type: canon final contra tags con wall.

| Hoja / type | Tags | Con wall |
|---|---|---|
| A-101 type 2 | 11 | 11 |
| A-101 type 3 | 4 | 4 |
| A-101 type 4 | 1 | 1 |
| A-101 type 5 | 1 | 1 |
| A-221 type A | 3 | 3 |
| A-221 type B | 1 | 1 |
| A-221 type C | 1 | 1 |
| A-221 type D | 1 | 1 |
| A-221 type E1 | 2 | 2 |
| A-221 type E2 | 1 | 1 |
| A-221 type F | 1 | 1 |
| A-221 type H1 | 2 | 2 |
| A-221 type H2A | 1 | 1 |
| A-221 type H2B | 1 | 1 |
| A-221 type H3A | 1 | 1 |
| A-221 type H3B | 1 | 1 |
| A-221 type I | 4 | 4 |

- A: 56 walls; tags sin wall 0, columnas sin column_wrap 0, discontinuas sin soffit_side 0
- B: 50 walls; tags sin wall 0, columnas sin column_wrap 0, discontinuas sin soffit_side 0
- final (AB corregido): 56 walls; tags sin wall 0, columnas sin column_wrap 0, discontinuas sin soffit_side 0

Límite: el type 4 tiene un solo tag en el inventario (el resto va por nota general), así que su completitud no se mide por conteo; sale −20.6 % de LF.

## LF por type: rev13 vs lecturas A / B y canon final (con decisiones)
| Type | rev13 | A | B | final | vs rev13 |
|---|---|---|---|---|---|
| 2 | 278.57 | 252.81 | 264.43 | 258.21 | -7.3 % |
| 4 | 83.64 | 63.58 | 70.4 | 66.42 | -20.6 % |
| COLUMN WRAP | 72.0 | 81.75 | 80.56 | 81.75 | +13.5 % |
| SOFFIT SIDE | 65.31 | 28.88 | 45.23 | 28.88 | -55.8 % |
| H1 | 42.15 | 38.52 | 41.72 | 38.52 | -8.6 % |
| 3 | 38.68 | 38.68 | 24.2 | 38.68 | +0.0 % |
| E2 | 29.3 | 28.49 | 29.53 | 28.49 | -2.8 % |
| E1 | 27.88 | 23.56 | 23.28 | 23.6 | -15.4 % |
| A | 20.27 | 20.75 | 20.41 | 20.75 | +2.4 % |
| H2A | 12.17 | 4.49 | 12.19 | 4.49 | -63.1 % |
| H3B | 6.17 | 6.76 | 6.14 | 6.76 | +9.6 % |
| 5 | 5.7 | 5.72 | 11.0 | 5.72 | +0.4 % |
| D | 5.14 | 6.15 | 6.2 | 6.15 | +19.6 % |
| I | 4.52 | 7.68 | 5.46 | 7.68 | +70.1 % |
| H3A | 4.08 | 3.99 | 4.15 | 3.99 | -2.2 % |
| F | 3.26 | — | — | — | — |
| B | 3.17 | 2.75 | 3.18 | 2.75 | -13.2 % |
| C | 3.17 | 2.23 | 3.18 | 2.23 | -29.7 % |
| H2B | 1.95 | 2.0 | 1.97 | 2.0 | +2.6 % |
| PART_OF 5-01 | — | 4.22 | — | — | — |
| PART_OF W2-01 | — | — | — | 10.06 | — |
| PART_OF 2-10 | — | 10.06 | — | — | — |
| PART_OF W5-01 | — | — | — | 4.22 | — |
| **Total** | **707.12** | **633.07** | **653.23** | **641.35** | **-9.3 %** |

"PART_OF" son returns sin tag; en el Excel van con el type de su wall (R80e.41).

## Material Summary: Excel del runner vs rev13
### Principales
| Material | Unit | rev13 | runner | Δ |
|---|---|---|---|---|
| 5/8" gypsum board, Type X | SF | 14266.95 | 8266.72 | -42.1 % |
| 3-5/8" metal stud (LF of material) | LF | 11601.59 | 7811.19 | -32.7 % |
| 6" metal stud (LF of material) | LF | 3162.5 | 1960 | -38.0 % |
| Bracing 1-1/2" C.R. channel @ 48" O.C. | LF | 2883.65 | — | −100 % (falta) |
| FRT plywood substrate (5/8 in.) | SF | 2686.45 | 3634.8 | +35.3 % |
| FRP panels | SF | 2001.38 | 2001.38 | +0.0 % |
| 5/8" gypsum board, Type X W.R. (water resistant) | SF | 1092.59 | 940.87 | -13.9 % |
| METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim | LF | 957.03 | 328 | -65.7 % |
| PVC trim - edge trim molding and inside corner molding at the FRP, incl. outside corners,  | LF | 887.62 | 887.62 | +0.0 % |
| Blocking FRT / 2X FRT wood | LF | 568.27 | 552.27 | -2.8 % |
| Nested inner runner at the deflection head (3/A-410) | LF | 479.85 | — | −100 % (falta) |
| USG drywall suspension cross tee DGLW424 | LF | 457.96 | 457.96 | +0.0 % |
| Top / deflection track 3-5/8" | LF | 450.02 | 425.16 | -5.5 % |
| Bottom track 3-5/8" | LF | 450.02 | 425.16 | -5.5 % |
| 1/2" cement board / cementitious backer | SF | 434.28 | 980.19 | +125.7 % |
| FRT plywood substrate (3/4 in.) | SF | 370.46 | 376.32 | +1.6 % |
| Track 3-5/8" (14 ga 157.81 LF + 16 ga 5.00 LF + 20 ga 118.28 LF) at soffits, fire stop at  | LF | 281.09 | — | −100 % (falta) |
| Control joint, gypsum board walls (ASTM C840, 30 ft max) | LF | 250 | 250 | +0.0 % |
| Furring channel (ceilings) | LF | 207.45 | 286.44 | +38.1 % |
| USG drywall suspension main tee DGLW26 | LF | 194.16 | 194.16 | +0.0 % |
| Ceiling perimeter track at GWB ceilings (size not printed, RFI) | LF | 180.99 | 281.75 | +55.7 % |
| Carrying channel (ceilings) | LF | 159.16 | 159.16 | +0.0 % |
| Track 6" (16 ga 25.33 LF + 20 ga 118.73 LF) at soffits, fire stop at ceiling line and nest | LF | 144.06 | — | −100 % (falta) |
| Top / deflection track 6" | LF | 118.59 | 111.09 | -6.3 % |
| Bottom track 6" | LF | 118.59 | 111.09 | -6.3 % |
| USG angle molding DGWM24 | LF | 107.21 | 107.21 | +0.0 % |
| USG channel molding DGCM27 | LF | 107.21 | 107.21 | +0.0 % |
| 8" metal joist (ceiling box) | LF | 88 | 88 | +0.0 % |
| Additional head track at openings over 4'-0" wide - extended to every door as a 2-piece tr | LF | 83.32 | 62.67 | -24.8 % |
| Top / deflection track - other framing (not a partition type, see source) | LF | 72 | 72 | +0.0 % |
| Metal corner guard 2"x2"x72" at outside corners (A-001A) | PCS | 72 | 72 | +0.0 % |
| Bottom track - other framing (not a partition type, see source) | LF | 72 | 72 | +0.0 % |
| 3-5/8" stud, framed soffit 2/A-221 (LF) | LF | 61.31 | 89.61 | +46.2 % |
| 5/8" cement board (tile base) | SF | 50.04 | — | −100 % (falta) |
| 8" stud (all gauges) | LF | 25.33 | 25.33 | +0.0 % |
| 8" ledger track (gauge not printed, RFI-54) (4/A-210) | LF | 12.67 | — | −100 % (falta) |
| Stud reinforcement at MEP penetrations | PCS | 10 | 10 | +0.0 % |
| Stainless steel corner guard 48" A.F.F. (C22/A-101) | PCS | 1 | 1 | +0.0 % |
| 5/8" FRT plywood at canopy column wraps | SF | — | 195 | new |
| 5/8" gypsum board, MOISTURE RESISTANT | SF | — | 75.96 | new |
| Level 5 finish | SF | 0 | 0 | 0 = 0 |
| Bracing 1-1/2" C.R. channel | LF | — | 1774.18 | new |
| 2-1/2" CFMF @ 16" O.C. at coiling grille head (detail per plans) | LF | 0 | 0 | 0 = 0 |
| Access panel | PCS | 0 | 0 | 0 = 0 |
| Extra framing - ATM recess (only what a detail prints at the recess; the wall stays in its | LF | 0 | 0 | 0 = 0 |
| Gypsum board jamb return at openings | SF | 0 | 0 | 0 = 0 |
| Header / metal stud box beam | LF | — | 62.67 | new |
| 5/8" gypsum board, regular | SF | — | 4896.74 | new |

### Fasteners y consumibles
| Material | Unit | rev13 | runner | Δ |
|---|---|---|---|---|
| Type S-12 drywall screws #6 x 1-1/4" (board on 18/16/14 ga studs) | PCS | 13328.22 | 0 | -100.0 % |
| #10-16 x 3/4" Tek screws, pan head, at 16 ga clip angles and nested header / column / beam | PCS | 10668 | — | −100 % (falta) |
| Joint tape, paper | LF | 5683.03 | 5246.71 | -7.7 % |
| Drywall screws #7 x 1-1/4" Type S bugle head (board on 25/20 ga studs) | PCS | 5103.23 | 17016.35 | +233.4 % |
| Hanger wire | LF | 2689.79 | 1545.5 | -42.5 % |
| Clip angle 16 ga (5/A-410 bracing clips + 7/A-210 nested header clips) | PCS | 2522 | — | −100 % (falta) |
| Plywood screws #10-24 x 1-1/4" Teks/3 (A-410 note 8.D) | PCS | 2331 | — | −100 % (falta) |
| Framing screws #8-18 x 1/2" pan head (25/20 ga studs) | PCS | 1940 | 2580 | +33.0 % |
| Heavy-gauge framing screws #10-16 x 3/4" pan head (18/16/14 ga studs) | PCS | 1776 | 0 | -100.0 % |
| Cement board screws 1-1/4" (manufacturer spacing) | PCS | 1686 | — | −100 % (falta) |
| Joint compound, all purpose | LB | 1105.89 | 1020.98 | -7.7 % |
| #8 screws at the top chord, cross members and track (8/A-410) | PCS | 775 | — | −100 % (falta) |
| #8 screws at diagonal brace ends, 2 per end (manufacturer rule; 3/A-410 prints none) | PCS | 512 | 512 | +0.0 % |
| Power-driven fasteners, slab pins for the bottom track | PCS | 388.72 | 456.19 | +17.4 % |
| Hilti Kwik HUS-EZ 1/4" x 1-5/8" concrete screws at the moment clips (3/A-410, 4/A-410) | PCS | 324 | 324 | +0.0 % |
| #10-16 screws at the moment clips, (1) at each flange (A/A-410) | PCS | 324 | 324 | +0.0 % |
| #8 pan head self-tapping screws, relief channel to structure (8/A-410) | PCS | 291 | — | −100 % (falta) |
| P.A.F. 3/16" x 3/8" at cross member ends (8/A-410) | PCS | 282 | — | −100 % (falta) |
| Moment clip ClarkDietrich MC series with stiffening plate (A/A-410), one per stud of types | PCS | 162 | 162 | +0.0 % |
| 16 ga wire at seismic brace points (5/A-121) | LF | 131.42 | — | −100 % (falta) |
| Hanger wire 12 ga - hanger count (one per hanger, height per room) | PCS | 109 | 109 | +0.0 % |
| Power-driven fasteners and duct sleeves - duct sleeves at the duct crossings (M-102) | PCS | 8 | 8 | +0.0 % |
| Deflection clips at non-load-bearing walls to structure | PCS | 0 | 0 | 0 = 0 |
| Expansion anchors Hilti 1/4" Kwik Bolt II, exterior bottom track @ 8" O.C. | PCS | 0 | 0 | 0 = 0 |


Cómo leer estas tablas:
- **Principales.** Caen menos que en la #3: 3-5/8" stud −32.7 % (era −53 %), 6" stud −38 % (era −50 %) y tracks −5.5 %. Siguen exactos: FRP, PVC trim, USG grid, control joint y carrying channel.
- **5/8" Type X −42.1 %.** Hay board regular en los walls que no se emparejaron, a los que no llegó la decisión RFI-27 (A-001A Div 09 A.2). Ver `takeoff_canon_con_decisiones.json`.
- **Cement board +125.7 %.** La lectura pone cement board en más caras que rev13. N/HOJA PENDIENTE: va al back-check.
- **Fasteners.** Tape y compound −7.7 %; moment clips, HUS-EZ y brace-end screws exactos. Los −100 % (Tek screws, clip angles, plywood screws, relief channel, P.A.F., 16 ga wire) son decisiones del estimador **sin objeto**: no se aplicaron y están listadas en el canon. No son diferencias de plano.

## Errores nuevos y su regla (mismo turno)
- **R80e.41** (`partition_types.py`): un return sin tag con part_of va en el type de su wall.
- **R80e.42** (reconciliación):
  - un node se identifica por sus walls, no por su id;
  - las aberturas de la lectura que la lista de la decisión no trae se conservan;
  - los supuestos del estimador con RFI (carrying_direction) viajan con la decisión de ceilings.
- **Sealer:** un return sin tag toma el type de `part_of`.
- **Runner:**
  - Edit permitido en el sandbox de corrección (la escritura del canon se negaba);
  - un id con punto (C-E1-P.2) se traduce completo;
  - todo "NO SE ARMA" va a la corrección.
- **BE-73..75** en BIBLIOTECA_ERRORES.

## Archivos
- `Takeoff_BN_runner_v4.xlsx` (no entregable: F-01 PENDING)
- `costos.csv` (histórico) y `costos_run4.csv`
- `REGLAS_FALLAS.md`
- `takeoff_canon_con_decisiones.json`
- `takeoff_canon_AB_leido.json`
- `lectura_A.json`, `lectura_B.json`
- `revision_AB.md`
- `comparar_material.py`
