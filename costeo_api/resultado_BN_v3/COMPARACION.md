# B&N — corrida real #3 del runner (2026-10-30): primer Excel por API

Sonnet, PDF limpio, overlay `decisiones_BN.json` + reconciliación geométrica, reglas.py encendido, cada llamada en sandbox. Tope autorizado por el usuario: $15 adicionales.

## Resultado
- **El runner terminó la cadena completa (EXIT 0) y armó el Excel:** `Takeoff_BN_runner_v3.xlsx`.
  - reglas.py quedó con **0 fallas**, salvo el back-check pendiente, que es paso humano o agente posterior (R80e.30).
  - Pasaron las compuertas de canon.py, inventario, planmark, alcances y registro.
- **Cobertura (paso 12 reducido):** 102/109 (93.58 %). Los 7 huecos están en `cobertura.md`: 6/A-121, 8/A-221, A-222A, A-223, 12/A-412, 13/A-412 y 14/A-412.
- **El Excel queda muy por debajo de rev13: −26.1 % de LF** (522.74 contra 707.12). Las dos lecturas de esta corrida fueron cortas: A 27 walls, B 31 walls; la lectura A de la #2 había tenido 50. Ver la tabla de types.
- **Las cantidades salen de los programas.** El modelo solo leyó: dos lecturas, resolución, 6 correcciones dirigidas por las compuertas y cobertura.
  - La evidencia visual (recortes con la band marcada) la genera `evidencia.py`.
  - El registro MEP lo hace `mep.py`.

## Costo por paso (corrida #3)
| Paso | Llamadas | USD | Output tokens | Cache read | Seg |
|---|---|---|---|---|---|
| Proceso, inventario_tags, comparar, Excel, compuertas (scripts) | — | 0.00 | — | — | — |
| Lectura A | 1 | 4.09 | 84,464 | 20.24 M | 846 |
| Lectura A — continuación (cruce con B) | 1 | 0.80 | 18,291 | 4.16 M | 176 |
| Lectura B | 1 | 3.52 | 78,990 | 21.00 M | 815 |
| Resolución (23 diferencias) | 2 (la 1.ª no escribió el archivo) | 0.66 | 6,978 | 3.53 M | 101 |
| Corrección dirigida (soffit sides, carrying direction, reglas.py, ALC-18 trim) | 6 | 2.79 | 42,702 | 16.80 M | 535 |
| Cobertura (la 1.ª agotó su tope de $1: el permiso le negó la escritura) | 2 | 1.70 | 54,084 | 4.52 M | 409 |
| **Total corrida #3** | 13 | **13.56 de 15** | | | |

Total histórico: #1 $4.99 + #2 $11.04 + #3 $13.56 = **$29.59**. El detalle por llamada está en `costos_run3.csv`.

## LF por type: rev13 vs lecturas A / B y canon final (con decisiones)
| Type | rev13 | A | B | final | vs rev13 |
|---|---|---|---|---|---|
| 2 | 278.57 | 157.73 | 262.35 | 267.33 | −4.0 % |
| 4 | 83.64 | 48.56 | 50.16 | 50.16 | −40.0 % |
| COLUMN WRAP | 72.00 | 9.17 | 13.00 | 13.00 | −81.9 % |
| SOFFIT SIDE | 65.31 | — | — | 19.85 | −69.6 % |
| H1 | 42.15 | 42.23 | 42.00 | 42.00 | −0.4 % |
| 3 | 38.68 | — | 24.00 | 24.00 | −38.0 % |
| E2 | 29.30 | 29.90 | 28.99 | 28.99 | −1.1 % |
| E1 | 27.88 | 19.00 | — | 19.00 | −31.9 % |
| A | 20.27 | 20.48 | 21.02 | 21.02 | +3.7 % |
| H2A | 12.17 | 12.17 | 4.50 | 4.50 | −63.0 % |
| H3B | 6.17 | 6.17 | 6.17 | 6.17 | 0.0 % |
| 5 | 5.70 | 9.74 | 5.72 | 5.72 | +0.4 % |
| D | 5.14 | 6.15 | 6.15 | 6.15 | +19.6 % |
| I | 4.52 | — | 3.64 | 3.64 | −19.4 % |
| H3A | 4.08 | 4.08 | 4.04 | 4.04 | −1.0 % |
| F | 3.26 | — | — | — | falta |
| B | 3.17 | 2.75 | 2.75 | 2.75 | −13.2 % |
| C | 3.17 | 2.75 | 2.75 | 2.75 | −13.2 % |
| H2B | 1.95 | 1.95 | 1.67 | 1.67 | −14.4 % |
| **Total** | **707.12** | **372.82** | **478.91** | **522.74** | **−26.1 %** |

Los soffit sides (19.85 LF) los agregó la corrección: ninguna de las dos lecturas los trajo.

## Material Summary: Excel del runner vs rev13
### Principales
| Material | Unit | rev13 | corrida #3 | Δ |
|---|---|---|---|---|
| 5/8" gypsum board, Type X | SF | 14266.95 | 11510.35 | -19.3 % |
| 3-5/8" metal stud (LF of material) | LF | 11601.59 | 5454.8 | -53.0 % |
| 6" metal stud (LF of material) | LF | 3162.5 | 1584 | -49.9 % |
| Bracing 1-1/2" C.R. channel @ 48" O.C. | LF | 2883.65 | — | −100 % (falta) |
| FRT plywood substrate (5/8 in.) | SF | 2686.45 | 1445.04 | -46.2 % |
| FRP panels | SF | 2001.38 | 2001.38 | +0.0 % |
| 5/8" gypsum board, Type X W.R. (water resistant) | SF | 1092.59 | 1052.87 | -3.6 % |
| METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim | LF | 957.03 | 192 | -79.9 % |
| PVC trim - edge trim molding and inside corner molding at the FRP, incl. outside corners,  | LF | 887.62 | 887.62 | +0.0 % |
| Blocking FRT / 2X FRT wood | LF | 568.27 | 552.27 | -2.8 % |
| Nested inner runner at the deflection head (3/A-410) | LF | 479.85 | — | −100 % (falta) |
| USG drywall suspension cross tee DGLW424 | LF | 457.96 | 457.96 | +0.0 % |
| Top / deflection track 3-5/8" | LF | 450.02 | 393.33 | -12.6 % |
| Bottom track 3-5/8" | LF | 450.02 | 393.33 | -12.6 % |
| 1/2" cement board / cementitious backer | SF | 434.28 | 393.74 | -9.3 % |
| FRT plywood substrate (3/4 in.) | SF | 370.46 | 289.99 | -21.7 % |
| Track 3-5/8" (14 ga 157.81 LF + 16 ga 5.00 LF + 20 ga 118.28 LF) at soffits, fire stop at  | LF | 281.09 | — | −100 % (falta) |
| Control joint, gypsum board walls (ASTM C840, 30 ft max) | LF | 250 | 250 | +0.0 % |
| Furring channel (ceilings) | LF | 207.45 | 334.63 | +61.3 % |
| USG drywall suspension main tee DGLW26 | LF | 194.16 | 194.16 | +0.0 % |
| Ceiling perimeter track at GWB ceilings (size not printed, RFI) | LF | 180.99 | 263.69 | +45.7 % |
| Carrying channel (ceilings) | LF | 159.16 | 108.19 | -32.0 % |
| Track 6" (16 ga 25.33 LF + 20 ga 118.73 LF) at soffits, fire stop at ceiling line and nest | LF | 144.06 | — | −100 % (falta) |
| Bottom track 6" | LF | 118.59 | 109.56 | -7.6 % |
| Top / deflection track 6" | LF | 118.59 | 109.56 | -7.6 % |
| USG channel molding DGCM27 | LF | 107.21 | 107.21 | +0.0 % |
| USG angle molding DGWM24 | LF | 107.21 | 107.21 | +0.0 % |
| 8" metal joist (ceiling box) | LF | 88 | 88 | +0.0 % |
| Additional head track at openings over 4'-0" wide - extended to every door as a 2-piece tr | LF | 83.32 | 44.33 | -46.8 % |
| Metal corner guard 2"x2"x72" at outside corners (A-001A) | PCS | 72 | 72 | +0.0 % |
| Bottom track - other framing (not a partition type, see source) | LF | 72 | — | −100 % (falta) |
| Top / deflection track - other framing (not a partition type, see source) | LF | 72 | — | −100 % (falta) |
| 3-5/8" stud, framed soffit 2/A-221 (LF) | LF | 61.31 | 97.64 | +59.3 % |
| 5/8" cement board (tile base) | SF | 50.04 | — | −100 % (falta) |
| 8" stud (all gauges) | LF | 25.33 | 25.33 | +0.0 % |
| 8" ledger track (gauge not printed, RFI-54) (4/A-210) | LF | 12.67 | — | −100 % (falta) |
| Stud reinforcement at MEP penetrations | PCS | 10 | 10 | +0.0 % |
| Stainless steel corner guard 48" A.F.F. (C22/A-101) | PCS | 1 | 1 | +0.0 % |
| Gypsum board jamb return at openings | SF | 0 | 0 | 0 = 0 |
| Header / metal stud box beam | LF | — | 44.33 | new |
| 5/8" gypsum board, regular | SF | — | 1693.89 | new |
| Level 5 finish | SF | 0 | 0 | 0 = 0 |
| Access panel | PCS | 0 | 0 | 0 = 0 |
| 5/8" FRT plywood at canopy column wraps | SF | — | 208 | new |
| Extra framing - ATM recess (only what a detail prints at the recess; the wall stays in its | LF | 0 | 0 | 0 = 0 |
| 2-1/2" CFMF @ 16" O.C. at coiling grille head (detail per plans) | LF | 0 | 0 | 0 = 0 |
| Bracing 1-1/2" C.R. channel | LF | — | 1282.19 | new |

### Fasteners y consumibles
| Material | Unit | rev13 | corrida #3 | Δ |
|---|---|---|---|---|
| Type S-12 drywall screws #6 x 1-1/4" (board on 18/16/14 ga studs) | PCS | 13328.22 | 0 | -100.0 % |
| #10-16 x 3/4" Tek screws, pan head, at 16 ga clip angles and nested header / column / beam | PCS | 10668 | — | −100 % (falta) |
| Joint tape, paper | LF | 5683.03 | 5275.13 | -7.2 % |
| Drywall screws #7 x 1-1/4" Type S bugle head (board on 25/20 ga studs) | PCS | 5103.23 | 17108.53 | +235.2 % |
| Hanger wire | LF | 2689.79 | 1545.5 | -42.5 % |
| Clip angle 16 ga (5/A-410 bracing clips + 7/A-210 nested header clips) | PCS | 2522 | — | −100 % (falta) |
| Plywood screws #10-24 x 1-1/4" Teks/3 (A-410 note 8.D) | PCS | 2331 | — | −100 % (falta) |
| Framing screws #8-18 x 1/2" pan head (25/20 ga studs) | PCS | 1940 | 1936 | -0.2 % |
| Heavy-gauge framing screws #10-16 x 3/4" pan head (18/16/14 ga studs) | PCS | 1776 | 0 | -100.0 % |
| Cement board screws 1-1/4" (manufacturer spacing) | PCS | 1686 | — | −100 % (falta) |
| Joint compound, all purpose | LB | 1105.89 | 1026.51 | -7.2 % |
| #8 screws at the top chord, cross members and track (8/A-410) | PCS | 775 | — | −100 % (falta) |
| #8 screws at diagonal brace ends, 2 per end (manufacturer rule; 3/A-410 prints none) | PCS | 512 | 512 | +0.0 % |
| Power-driven fasteners, slab pins for the bottom track | PCS | 388.72 | 377.17 | -3.0 % |
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
- **Principales.** Donde la lectura trae los walls, el resultado queda cerca de rev13: H1, E2, type 2 (−4 %), Type X W.R. (−3.6 %), FRP, PVC trim, USG grid y corner guards (0 %). Las grandes faltas siguen las faltas de LF:
  - 3-5/8" stud −53 % y 6" stud −50 %: faltan walls de type 2, 3 y 4 y column wraps;
  - board Type X −19.3 %.
- **Board "regular" (1693.89 SF, nuevo).** Son faces de walls que no se emparejaron con la referencia, así que la decisión RFI-27 (Type X en todos los walls nuevos, A-001A Div 09 A.2) no les llegó.
- **Bracing C.R. channel.** Sale en un renglón con otro nombre: 1282.19 LF contra 2883.65 de rev13.
- **Fasteners.** Los −100 % de Tek screws, clip angles, plywood screws, cement board screws, relief channel, P.A.F. y 16 ga wire vienen de decisiones del estimador (`misc_items`) que quedaron **sin objeto**, porque sus walls no están en la lectura. No son diferencias de plano.
- **Drywall screws.** La partición entre heavy gauge y light gauge difiere: S-12 queda en 0 y #7 en +235 %, porque la lectura no trae los gauges 18/16/14 de rev13.

## Diferencias principales con su fuente
1. **Column wraps −81.9 %** (C25, 1/A-410 y planta A-101): las lecturas solo trajeron F-BOX (F/A-221). Faltan CW-01..CW-09.
2. **Type 4 −40 %** (4/A-410): la lectura trae 2 de los walls largos (50.16 LF).
3. **Type 3 −38 %** (3/A-410): 24.0 LF contra 38.68.
4. **SOFFIT SIDE −69.6 %** (2/A-221): faltan SS-IN-N, SS-IN-E y SS-GG.
5. **H2A −63 %** (A-221): B midió 4.50 contra 12.17. La resolución partió de B.
6. **Type F falta** (F/A-221).
7. **Board regular:** ver la nota arriba (RFI-27).

## Reconciliación y decisiones
- 28 walls emparejados con la referencia.
- 137 decisiones del estimador "sin objeto", **no aplicadas**. Además hay 106 derivados: nodes, tramos reescalados y wet_fixtures.
- Todo está en `runner_resultado.json`.

## Qué cambió en el runner para llegar al Excel
- **`evidencia.py`:** recortes por wall con la band marcada, `tag_ids` por coordenadas, thickness desde la band y estados #0. Con eso reglas.py bajó de 3881 a 335 fallas en la lectura de la #2.
- **`mep.py`:** registro por programa; M-102 = 14, igual que rev13.
- **planmark:** sondas densas para líneas discontinuas (SOFFIT ABOVE).
- **Corrección dirigida:** las fallas de canon.py, reglas.py y alcances.py vuelven al modelo, en ids de la lectura.
- **Skill, `trazabilidad.py` (R80e.39):**
  - el board regular y el MR se desglosaban como Type X;
  - el FRT substrate se mezclaba con el sheathing de column wraps;
  - un gauge numérico rompía la tool.
  - Los diffs están en `../runner/skill_patches/`.

## Archivos
- `Takeoff_BN_runner_v3.xlsx`
- `costos.csv` (histórico) y `costos_run3.csv`
- `runner_resultado.json`
- `takeoff_canon_con_decisiones.json`
- `takeoff_canon_AB_leido.json`
- `lectura_A.json`, `lectura_B.json`
- `revision_AB.md`
- `cobertura.md`
- `REGLAS_FALLAS.md`
- `comparar_material.py`
