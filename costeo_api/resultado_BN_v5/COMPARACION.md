# B&N — corrida real #5 del runner (2026-10-31): primer Excel ENTREGABLE por API

Sonnet, PDF limpio, overlay `decisiones_BN.json` con decisiones generales por atributo (R80e.43), reconciliación geométrica, reglas.py encendido, cada llamada en sandbox. Incluye R80e.40 (conteos) y R80e.44 (A-300 / A-400 en el prompt, compuerta de alturas placeholder, comparación A/B de altura y board). Tope autorizado por el usuario: $15 adicionales.

## Resultado
- **El Excel pasa TODAS las compuertas** (`Takeoff_BN_runner_v5.xlsx`): canon.py, inventario, planmark, la compuerta reglas.py dentro del armado, alcances y registro. reglas.py después del armado deja **1 falla: el back-check pendiente**, que es paso humano o agente posterior (R80e.30). Es el primer Excel por API en condición de ir al back-check.
- **Alturas correctas (R80e.44):** los walls a deck salen en 25.0 ft desde "B.O. DECK ABOVE EL. 25'-0" V.I.F." de 1/A-400B, con la RFI de 24'-0" / 25'-7". En la #4 eran 20 ft placeholder.
- **LF: 619.84 contra 707.12 de rev13 (−12.3 %).**
- **Cobertura (paso 12): no corrió**, sin presupuesto.
- **Costo: $14.79 de $15.**

## Costo por paso (corrida #5)
| Paso | Llamadas | USD | Output tokens | Cache read | Seg |
|---|---|---|---|---|---|
| Proceso, inventario_tags, comparar, Excel, compuertas (scripts) | — | 0.00 | — | — | — |
| Lectura A | 1 | 3.50 | 59,842 | 17.80 M | 614 |
| Lectura A — continuaciones (conteos + cruce) | 2 | 2.01 | 40,009 | 12.08 M | 447 |
| Lectura B | 1 | 4.27 | 92,743 | 25.20 M | 942 |
| Lectura B — continuaciones | 2 | 2.19 | 51,450 | 12.11 M | 501 |
| Resolución (45 diferencias) | 1 | 0.47 | 5,824 | 2.56 M | 69 |
| Corrección dirigida (accesorios PENDIENTE, 8 RFIs sin hoja, fila F PENDING) | 7 | 2.36 | 31,040 | 14.36 M | 402 |
| Cobertura | 0 | — (sin presupuesto) | | | |
| **Total corrida #5** | 14 | **14.79** | | | |

Total histórico: #1 $4.99 + #2 $11.04 + #3 $13.56 + #4 $15.01 + #5 $14.79 = **$59.39**. El detalle está en `costos_run5.csv`.

## Walls leídos vs inventario
- A: 43 walls; tags sin wall 0, columnas sin column_wrap 0, discontinuas sin soffit_side 0, alturas placeholder 0
- B: 43 walls; tags sin wall 0, columnas sin column_wrap 0, discontinuas sin soffit_side 0, alturas placeholder 0
- final: 43 walls; tags sin wall 0, columnas sin column_wrap 0, discontinuas sin soffit_side 0, alturas placeholder 0

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

⚠️ **Column wraps: 0 de 9.** La compuerta de conteos dio 0 faltantes porque las dos lecturas declararon `columns_none_reason`:
- **A:** "existing columns to remain exposed (key note C23)".
- **B:** "C25 GWB column surround… quantified as misc_items COL-*".

La resolución partió de A y se perdieron las COL-* de B. Rev13: 9 column wraps C25/A-101 de 8.0 ft. Corregido en el runner con R80e.46: la comparación A/B ahora detecta las 7 COL-* que solo trae B y las manda a la resolución.

## LF por type: rev13 vs lecturas A / B y canon final (con decisiones)
| Type | rev13 | A | B | final | vs rev13 |
|---|---|---|---|---|---|
| 2 | 278.57 | 279.38 | 256.1 | 304.38 | +9.3 % |
| 4 | 83.64 | 68.16 | 68.16 | 68.16 | -18.5 % |
| COLUMN WRAP | 72.0 | — | — | — | — |
| SOFFIT SIDE | 65.31 | 39.9 | — | 39.9 | -38.9 % |
| H1 | 42.15 | 42.9 | 41.63 | 42.9 | +1.8 % |
| 3 | 38.68 | 38.68 | 38.68 | 38.68 | +0.0 % |
| E2 | 29.3 | 29.14 | 29.6 | 29.14 | -0.5 % |
| E1 | 27.88 | 22.3 | 23.17 | 22.3 | -20.0 % |
| A | 20.27 | 20.42 | 20.47 | 20.42 | +0.7 % |
| H2A | 12.17 | 4.53 | 9.1 | 4.53 | -62.8 % |
| H3B | 6.17 | 6.69 | 6.17 | 6.69 | +8.4 % |
| 5 | 5.7 | 5.89 | 5.7 | 5.89 | +3.3 % |
| D | 5.14 | 6.15 | 6.15 | 6.15 | +19.6 % |
| I | 4.52 | 5.16 | 6.37 | 5.16 | +14.3 % |
| H3A | 4.08 | 4.04 | 3.58 | 4.04 | -1.0 % |
| F | 3.26 | 13.0 | 5.58 | 13.0 | +298.8 % |
| B | 3.17 | 3.27 | 2.75 | 3.27 | +3.2 % |
| C | 3.17 | 3.27 | 2.75 | 3.27 | +3.2 % |
| H2B | 1.95 | 1.96 | 1.99 | 1.96 | +0.5 % |
| **Total** | **707.12** | **594.84** | **527.95** | **619.84** | **-12.3 %** |

## Material Summary: Excel del runner vs rev13
### Principales
| Material | Unit | rev13 | runner | Δ |
|---|---|---|---|---|
| 5/8" gypsum board, Type X | SF | 14266.95 | 16130 | +13.1 % |
| 3-5/8" metal stud (LF of material) | LF | 11601.59 | 10633.91 | -8.3 % |
| 6" metal stud (LF of material) | LF | 3162.5 | 1700 | -46.2 % |
| Bracing 1-1/2" C.R. channel @ 48" O.C. | LF | 2883.65 | — | −100 % (falta) |
| FRT plywood substrate (5/8 in.) | SF | 2686.45 | 3410.95 | +27.0 % |
| FRP panels | SF | 2001.38 | 2089.78 | +4.4 % |
| 5/8" gypsum board, Type X W.R. (water resistant) | SF | 1092.59 | 1580.55 | +44.7 % |
| METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim | LF | 957.03 | 42 | -95.6 % |
| PVC trim - edge trim molding and inside corner molding at the FRP, incl. outside corners,  | LF | 887.62 | 887.62 | +0.0 % |
| Blocking FRT / 2X FRT wood | LF | 568.27 | 552.27 | -2.8 % |
| Nested inner runner at the deflection head (3/A-410) | LF | 479.85 | — | −100 % (falta) |
| USG drywall suspension cross tee DGLW424 | LF | 457.96 | 457.96 | +0.0 % |
| Bottom track 3-5/8" | LF | 450.02 | 515.26 | +14.5 % |
| Top / deflection track 3-5/8" | LF | 450.02 | 515.26 | +14.5 % |
| 1/2" cement board / cementitious backer | SF | 434.28 | 306.39 | -29.4 % |
| FRT plywood substrate (3/4 in.) | SF | 370.46 | 289.99 | -21.7 % |
| Track 3-5/8" (14 ga 157.81 LF + 16 ga 5.00 LF + 20 ga 118.28 LF) at soffits, fire stop at  | LF | 281.09 | — | −100 % (falta) |
| Control joint, gypsum board walls (ASTM C840, 30 ft max) | LF | 250 | 250 | +0.0 % |
| Furring channel (ceilings) | LF | 207.45 | 286.44 | +38.1 % |
| USG drywall suspension main tee DGLW26 | LF | 194.16 | 194.16 | +0.0 % |
| Ceiling perimeter track at GWB ceilings (size not printed, RFI) | LF | 180.99 | 303.79 | +67.8 % |
| Carrying channel (ceilings) | LF | 159.16 | 159.16 | +0.0 % |
| Track 6" (16 ga 25.33 LF + 20 ga 118.73 LF) at soffits, fire stop at ceiling line and nest | LF | 144.06 | — | −100 % (falta) |
| Bottom track 6" | LF | 118.59 | 64.68 | -45.5 % |
| Top / deflection track 6" | LF | 118.59 | 64.68 | -45.5 % |
| USG channel molding DGCM27 | LF | 107.21 | 107.21 | +0.0 % |
| USG angle molding DGWM24 | LF | 107.21 | 107.21 | +0.0 % |
| 8" metal joist (ceiling box) | LF | 88 | 88 | +0.0 % |
| Additional head track at openings over 4'-0" wide - extended to every door as a 2-piece tr | LF | 83.32 | 70.67 | -15.2 % |
| Top / deflection track - other framing (not a partition type, see source) | LF | 72 | — | −100 % (falta) |
| Metal corner guard 2"x2"x72" at outside corners (A-001A) | PCS | 72 | 72 | +0.0 % |
| Bottom track - other framing (not a partition type, see source) | LF | 72 | — | −100 % (falta) |
| 3-5/8" stud, framed soffit 2/A-221 (LF) | LF | 61.31 | 89.61 | +46.2 % |
| 5/8" cement board (tile base) | SF | 50.04 | — | −100 % (falta) |
| 8" stud (all gauges) | LF | 25.33 | 25.33 | +0.0 % |
| 8" ledger track (gauge not printed, RFI-54) (4/A-210) | LF | 12.67 | — | −100 % (falta) |
| Stud reinforcement at MEP penetrations | PCS | 10 | 10 | +0.0 % |
| Stainless steel corner guard 48" A.F.F. (C22/A-101) | PCS | 1 | 1 | +0.0 % |
| Level 5 finish | SF | 0 | 0 | 0 = 0 |
| 5/8" FRT plywood at canopy column wraps | SF | — | 325 | new |
| Gypsum board jamb return at openings | SF | 0 | 0 | 0 = 0 |
| Extra framing - ATM recess (only what a detail prints at the recess; the wall stays in its | LF | 0 | 0 | 0 = 0 |
| 2-1/2" CFMF @ 16" O.C. at coiling grille head (detail per plans) | LF | 0 | 0 | 0 = 0 |
| Bracing 1-1/2" C.R. channel | LF | — | 2906.38 | new |
| Header / metal stud box beam | LF | — | 70.67 | new |
| Access panel | PCS | 0 | 0 | 0 = 0 |

### Fasteners y consumibles
| Material | Unit | rev13 | runner | Δ |
|---|---|---|---|---|
| Type S-12 drywall screws #6 x 1-1/4" (board on 18/16/14 ga studs) | PCS | 13328.22 | 0 | -100.0 % |
| #10-16 x 3/4" Tek screws, pan head, at 16 ga clip angles and nested header / column / beam | PCS | 10668 | — | −100 % (falta) |
| Joint tape, paper | LF | 5683.03 | 6552.9 | +15.3 % |
| Drywall screws #7 x 1-1/4" Type S bugle head (board on 25/20 ga studs) | PCS | 5103.23 | 21252.66 | +316.5 % |
| Hanger wire | LF | 2689.79 | 1545.5 | -42.5 % |
| Clip angle 16 ga (5/A-410 bracing clips + 7/A-210 nested header clips) | PCS | 2522 | — | −100 % (falta) |
| Plywood screws #10-24 x 1-1/4" Teks/3 (A-410 note 8.D) | PCS | 2331 | — | −100 % (falta) |
| Framing screws #8-18 x 1/2" pan head (25/20 ga studs) | PCS | 1940 | 2356 | +21.4 % |
| Heavy-gauge framing screws #10-16 x 3/4" pan head (18/16/14 ga studs) | PCS | 1776 | 0 | -100.0 % |
| Cement board screws 1-1/4" (manufacturer spacing) | PCS | 1686 | — | −100 % (falta) |
| Joint compound, all purpose | LB | 1105.89 | 1275.16 | +15.3 % |
| #8 screws at the top chord, cross members and track (8/A-410) | PCS | 775 | — | −100 % (falta) |
| #8 screws at diagonal brace ends, 2 per end (manufacturer rule; 3/A-410 prints none) | PCS | 512 | 512 | +0.0 % |
| Power-driven fasteners, slab pins for the bottom track | PCS | 388.72 | 434.96 | +11.9 % |
| #10-16 screws at the moment clips, (1) at each flange (A/A-410) | PCS | 324 | 324 | +0.0 % |
| Hilti Kwik HUS-EZ 1/4" x 1-5/8" concrete screws at the moment clips (3/A-410, 4/A-410) | PCS | 324 | 324 | +0.0 % |
| #8 pan head self-tapping screws, relief channel to structure (8/A-410) | PCS | 291 | — | −100 % (falta) |
| P.A.F. 3/16" x 3/8" at cross member ends (8/A-410) | PCS | 282 | — | −100 % (falta) |
| Moment clip ClarkDietrich MC series with stiffening plate (A/A-410), one per stud of types | PCS | 162 | 162 | +0.0 % |
| 16 ga wire at seismic brace points (5/A-121) | LF | 131.42 | — | −100 % (falta) |
| Hanger wire 12 ga - hanger count (one per hanger, height per room) | PCS | 109 | 109 | +0.0 % |
| Power-driven fasteners and duct sleeves - duct sleeves at the duct crossings (M-102) | PCS | 8 | 8 | +0.0 % |
| Deflection clips at non-load-bearing walls to structure | PCS | 0 | 0 | 0 = 0 |
| Expansion anchors Hilti 1/4" Kwik Bolt II, exterior bottom track @ 8" O.C. | PCS | 0 | 0 | 0 = 0 |


Cómo leer estas tablas:
- **Principales.**
  - **3-5/8" stud −8.3 %** (era −32.7 % en la #4): las alturas de A-400B funcionaron.
  - **6" stud −46 % y tracks de 6" −45 %:** faltan los column wraps (C25) y parte de H2A y E1.
  - **Type X +13.1 % y W.R. +44.7 %:** las decisiones generales llegan a todos los walls, y el type 2 sale +9.3 % de LF.
  - **Exactos:** PVC trim, USG grid, control joint, carrying channel y corner guards.
  - **Metal trim −95.6 %:** la corrección dejó solo 42 LF (ALC-18 marcado con cantidad > 0). Queda para el back-check.
- **Fasteners.**
  - **Tape y compound +15.3 %:** siguen al board.
  - **Moment clips, HUS-EZ y brace screws:** exactos.
  - **Los −100 % (Tek screws, clip angles, plywood screws, relief channel, P.A.F., 16 ga wire):** decisiones del estimador sin objeto (`misc_items` de walls no emparejados). No son diferencias de plano.

## Errores nuevos y su regla (mismo turno)
- **R80e.45 (overlay):** un parche PARCIAL de una decisión sobre un ítem que la lectura no trae (una face con otro `side`) no crea un ítem a medias. Antes quedaban faces sin `layers` y canon.py se caía con `KeyError: 'layers'`, que ninguna corrección podía arreglar.
- **R80e.46 (comparación A/B):**
  - también se comparan las razones "none" de nivel canon y los `misc_items` que solo trae una lectura (caso de los column wraps C23 / C25);
  - una fila PENDING de la Partition Takeoff manda a la corrección el motivo exacto de partition_types. El type F era un box sin `fos_chain`; con ese motivo se cerró en una ronda.
- **BE-79..81.**

## Archivos
- `Takeoff_BN_runner_v5.xlsx` (todas las compuertas; back-check pendiente)
- `costos.csv` y `costos_run5.csv`
- `REGLAS_FALLAS.md` (1 = back-check)
- `takeoff_canon_con_decisiones.json`
- `takeoff_canon_AB_leido.json`
- `lectura_A.json`, `lectura_B.json`
- `revision_AB.md`
- `comparar_material.py`
