# B&N — corrida real #2 del runner (2026-10-30)

Sonnet, PDF limpio, overlay `decisiones_BN.json` + reconciliación geométrica. Tope del usuario: $20 en total.

## Resultado
- **No hay Excel.** El runner se detuvo correctamente (R80e.37) en el paso 8: planmark rechazó la band de SS-N (2/A-221) porque cae sobre papel en blanco.
- **canon.py, inventario, framed_openings y alcance_filtro pasaron** sobre la lectura real. Las cantidades de abajo salen de `familias_out.json` de canon.py, no del Material Summary.
- **Lectura B:** agotó su tope de $5.50 sin dar un canon válido (`mep_sweep` sin hojas P* / M*). No se usó.
  - Por eso no hubo cruce A/B ni resolución: la corrida quedó con **una sola lectura** (A).
- **Lectura A:** 50 walls, 646.91 LF; pasó la compuerta después de 2 continuaciones.
  - Su versión original había pasado `validar_canon` solo porque no traía `plan_scale_pt_per_ft`. Sin esa escala, canon.py no compara band contra length_ft.
  - Con la escala, saltaron W2-01 (band 50.0 ft vs 48'-4" impreso en A-101) y T2-07 (band 4.367 vs 4.7). Las continuaciones lo corrigieron.
- **Después de planmark** viene la compuerta reglas.py. En un diagnóstico (copia de prueba con la band de SS-N corregida, **no entregable**) dio **3881 fallas**:
  - E27: 100 cantidades sin estado CONFIRMADO / DERIVADO / PENDIENTE;
  - 86 faces sin imagen de evidencia;
  - 50 heights sin imagen de su cadena (B.O.D.).
  - La lectura por API **no produce la evidencia visual** que exige el skill. Ese es el bloqueo real para obtener un Excel por API.
- **No gasté el resto ($3.96):** con ese monto no se cierran 50 walls de evidencia + imágenes.

## Costo por paso (corrida #2)
| Paso | Modelo | USD | Output tokens | Cache read | Seg |
|---|---|---|---|---|---|
| Proceso, inventario_tags (scripts) | — | 0.00 | — | — | — |
| Lectura A | sonnet | 4.82 | 101,749 | 28.45 M | 1080 |
| Lectura B (tope agotado, sin canon válido) | sonnet | 5.50 | n/d (el log se truncó) | n/d | 1130 |
| Lectura A — continuación 1 | sonnet | 0.18 | 2,168 | 1.05 M | 30 |
| Lectura A — continuación 2 | sonnet | 0.55 | 7,315 | 4.05 M | 92 |
| comparar / resolución / cobertura | — | 0.00 (no aplican: una lectura / no llegó) | | | |
| **Total corrida #2** | | **11.04** | | | |
| **Total corridas #1 + #2** | | **16.04 de 20** | | | |

## LF por type: rev13 vs lectura A (con decisiones)
| Type | rev13 | A leída | A + decisiones | vs rev13 |
|---|---|---|---|---|
| 2 | 278.57 | 265.82 | 270.67 | −2.8 % |
| 4 | 83.64 | 68.16 | 68.16 | −18.5 % |
| COLUMN WRAP | 72.00 | 85.00 | 85.00 | +18.1 % |
| SOFFIT SIDE | 65.31 | 28.78 | 28.78 | −55.9 % |
| H1 | 42.15 | 41.84 | 41.84 | −0.7 % |
| 3 | 38.68 | 38.68 | 38.68 | 0.0 % |
| E2 | 29.30 | 28.49 | 28.49 | −2.8 % |
| E1 | 27.88 | 21.65 | 21.65 | −22.3 % |
| A | 20.27 | 21.12 | 21.12 | +4.2 % |
| H2A | 12.17 | 12.17 | 12.17 | 0.0 % |
| H3B | 6.17 | 4.10 | 4.10 | −33.5 % |
| 5 | 5.70 | 10.50 | 10.50 | +84.2 % |
| D | 5.14 | 5.15 | 5.15 | +0.2 % |
| I | 4.52 | — | — | falta |
| H3A | 4.08 | 6.75 | 6.75 | +65.4 % |
| F | 3.26 | — | — | falta |
| C | 3.17 | 3.15 | 3.15 | −0.6 % |
| B | 3.17 | 3.15 | 3.15 | −0.6 % |
| H2B | 1.95 | 2.40 | 2.40 (tag C-H2B) | +23.1 % |
| **Total** | **707.12** | **646.91** | **651.76** | **−7.8 %** |

Mejora contra la corrida #1: la resuelta de la #1 quedó en −24.4 %; esta en −7.8 %.

## Materiales vs rev13 (canon.py `familias`; unidades de la tool)
### Principales
| Material | rev13 | corrida #2 | Δ |
|---|---|---|---|
| 3-5/8" stud (todos los gauges) | 11662.9 | 10189.22 | -12.6 % |
| 5/8" cement board | 50.04 | 0.0 | -100.0 % |
| 5/8" gyp MOISTURE RESISTANT | 0.0 | 202.46 | new |
| 5/8" gyp Type X W.R. | 1092.59 | 946.93 | -13.3 % |
| 5/8" gyp board Type X | 14266.95 | 13358.78 | -6.4 % |
| 5/8" gyp board regular (walls + ceilings) | 0.0 | 2239.11 | new |
| 6" stud (todos los gauges) | 3162.5 | 2731.32 | -13.6 % |
| 8" joist | 88.0 | 134.0 | +52.3 % |
| 8" stud (todos los gauges) | 25.33 | 25.33 | +0.0 % |
| FRP | 2001.38 | 2001.38 | +0.0 % |
| FRT blocking | 568.27 | 586.77 | +3.3 % |
| FRT plywood (SF) | 3056.92 | 2186.94 | -28.5 % |
| PAFs and duct sleeves | 8.0 | 8.0 | +0.0 % |
| PVC trim at FRP | 887.62 | 887.62 | +0.0 % |
| USG angle molding (DGWM24) | 107.21 | 107.21 | +0.0 % |
| USG channel molding (DGCM27) | 107.21 | 107.21 | +0.0 % |
| USG drywall cross tee (DGLW424) | 457.96 | 457.96 | +0.0 % |
| USG drywall main tee (DGLW26) | 194.16 | 194.16 | +0.0 % |
| additional head track | 83.32 | 82.0 | -1.6 % |
| bottom track (todos) | 640.61 | 622.98 | -2.8 % |
| bracing C.R. channel | 2883.65 | 2734.6 | -5.2 % |
| carrying channel | 159.16 | 108.19 | -32.0 % |
| ceiling / soffit track 3-5/8" | 281.09 | 0.0 | -100.0 % |
| ceiling / soffit track 6" | 144.06 | 0.0 | -100.0 % |
| cement board | 434.28 | 447.49 | +3.0 % |
| control joint | 250.0 | 250.0 | +0.0 % |
| furring channel | 207.45 | 334.63 | +61.3 % |
| header / box beam | 0.0 | 82.0 | new |
| ledger track 8" | 12.67 | 12.0 | -5.3 % |
| metal corner guard 2x2x72 | 72.0 | 72.0 | +0.0 % |
| metal stud blocking (362CR / STUD BLOCKING) | 0.0 | 304.44 | new |
| metal trim (corner bead, casing, shadow molding) | 957.03 | 288.0 | -69.9 % |
| nested inner runner (deflection head) | 479.85 | 0.0 | -100.0 % |
| stainless corner guard 48 | 1.0 | 1.0 | +0.0 % |
| stud reinforcement MEP | 10.0 | 10.0 | +0.0 % |
| top / deflection track (todos) | 640.61 | 622.98 | -2.8 % |
| track de ceilings / soffits | 180.99 | 281.55 | +55.6 % |

### Fasteners y consumibles
| Material | rev13 | corrida #2 | Δ |
|---|---|---|---|
| #10-16 screws at moment clips | 324.0 | 324.0 | +0.0 % |
| #8 pan head screws, relief channel to structure | 291.0 | 0.0 | -100.0 % |
| #8 screws at brace ends | 512.0 | 512.0 | +0.0 % |
| #8 screws, top chord / cross members (typ. connection) | 775.0 | 0.0 | -100.0 % |
| 16 ga wire (seismic brace points) | 131.42 | 0.0 | -100.0 % |
| Kwik HUS-EZ anchors | 324.0 | 324.0 | +0.0 % |
| P.A.F. at cross members | 282.0 | 0.0 | -100.0 % |
| Tek screws at clip angles | 10668.0 | 0.0 | -100.0 % |
| cement board screws | 1686.0 | 0.0 | -100.0 % |
| clip angle (bracing / nested connections) | 2522.0 | 0.0 | -100.0 % |
| drywall screws | 5103.23 | 20096.74 | +293.8 % |
| drywall screws heavy gauge | 13328.22 | 0.0 | -100.0 % |
| framing screws | 1940.0 | 2680.0 | +38.1 % |
| framing screws heavy gauge | 1776.0 | 0.0 | -100.0 % |
| hanger wire | 2689.79 | 1545.5 | -42.5 % |
| joint compound | 1105.89 | 1205.8 | +9.0 % |
| joint tape | 5683.03 | 6196.49 | +9.0 % |
| moment clip (types 3/4 base) | 162.0 | 162.0 | +0.0 % |
| plywood screws (Teks/3) | 2331.0 | 0.0 | -100.0 % |
| slab pins | 388.72 | 467.24 | +20.2 % |

Notas de lectura de la tabla:
- En rev13, varios fasteners (Tek screws, clip angles, heavy gauge, plywood screws) salen de `misc_items` y de decisiones. En esta corrida quedaron "sin objeto" porque la lectura no trae esos walls o ids. Su −100 % es un hueco de la corrida, no una diferencia de plano.
- "5/8 gyp board regular" (2239.11) y "MOISTURE RESISTANT" (202.46) aparecen porque los walls que **no** se emparejaron conservan el board de la lectura. La decisión RFI-27 (5/8" Type X en todos los walls nuevos, A-001A Div 09 A.2) solo se aplicó a los 42 walls emparejados.

## Diferencias principales con su fuente
1. **SOFFIT SIDE −55.9 %** (2/A-221): la lectura trae SS-N y SS-E; faltan SS-IN-N, SS-IN-E y SS-GG. La band de SS-N cae sobre papel en blanco (planmark). Por eso no hay soffit track 3-5/8" / 6".
2. **Type 4 −18.5 %** y **E1 −22.3 %**: N/HOJA PENDIENTE (no se trazó en esta corrida, porque no hubo resolución A/B).
3. **COLUMN WRAP +18.1 %** (85 vs 72 LF): N/HOJA PENDIENTE. La lectura agregó CW-F.
4. **Types I y F faltan** (A-410 schedule): `types_none_reason` no los justifica. Lo aceptó la compuerta porque B no existía para el cruce.
5. **W2-01**: 48'-4" impreso en A-101, CONFIRMADO. La band original de la lectura medía 50.0 ft y se corrigió en la continuación.
6. **Board**: RFI-27 (A-001A Div 09 A.2) en 42 de 50 walls. Ver la nota de board regular arriba.

## Reconciliación (corrida #2)
- 42 walls emparejados de 50.
- 110 decisiones del estimador "sin objeto", **no aplicadas**: G1 46 walls + 9 misc; G2 14 walls + 13 misc + 2 plywood strips; G3 23 walls + 2 strips + 1 blocking.
- Además, 101 nodes, 4 tramos reescalados y 8 wet_fixtures derivados.
- Todo está listado en `run2_reconciliacion.json`.
- Reglas nuevas del runner en esta corrida:
  - rooms de ceilings: mismo número + mismo system;
  - refs de openings: mismos dígitos en el wall o en el que lo contiene;
  - nodes que cuelgan de walls ausentes = sin objeto;
  - tramos de una decisión reescalados al largo de la lectura (`[DERIVED]` con su operación);
  - wet_fixtures sin face MR tras una decisión de board.

## Archivos
- `run2_takeoff_canon_A.json`: lectura A final (después de las continuaciones).
- `run2_takeoff_canon_A_before_continuation.json`
- `run2_takeoff_canon_B_INVALID.json`: lectura B incompleta, no usada.
- `run2_takeoff_canon_con_decisiones.json`
- `run2_familias_out.json`
- `run2_reconciliacion.json`
- `costos.csv`

---

# Corrida real #1 (2026-10-30): resultado y comparación contra rev13

Autorizada por el usuario en la sesión (tope $20). Sonnet, PDF limpio (69 páginas, 0 anotaciones, sin LEGEND), overlay `decisiones_BN.json` (4 grupos) con reconciliación geométrica de ids, reglas.py encendido. Cada llamada corrió en un sandbox aislado.

## Resultado: el runner se DETUVO en canon.py (R80e.37). No hay Excel.
`canon.py` rechazó el canon: "2 clave(s) de walls fuera del esquema CON números: HG1.curved, HG2.curved". Es correcto que se detenga: corregir el canon a mano sería saltarse la cadena. Por eso no hay Material Summary contra el cual sacar % por material (principales / fasteners). La comparación posible es por type, en LF del canon leído.

## Costo por paso
| Paso | Modelo | USD | Output tokens | Cache read | Cache write | Seg |
|---|---|---|---|---|---|---|
| Proceso, inventario_tags, comparar | scripts | 0.00 | — | — | — | — |
| Lectura A | sonnet | 1.50 | 26,922 | 2.73 M | 0.24 M | 247 |
| Lectura B | sonnet | 2.98 | 90,849 | 12.89 M | 0.20 M | 850 |
| Resolución (41 diferencias) | sonnet | 0.51 | 12,279 | 1.91 M | 0.05 M | 123 |
| Cobertura | — | no llegó | | | | |
| **Total** | | **4.99** (de 20) | | | | |

## LF por type: lecturas A, B y resuelta (AB) contra rev13
| Type | rev13 | A | B | AB | AB vs rev13 |
|---|---|---|---|---|---|
| 2 | 278.57 | 134.72 | 279.18 | 191.61 | -31.2 % |
| 5 | 5.70 | 12.92 | — | 6.11 | +7.2 % |
| 3 | 38.68 | — | 38.66 | 38.66 | -0.1 % |
| 4 | 83.64 | — | 68.59 | 67.33 | -19.5 % |
| H1 | 42.15 | 28.49 | 42.85 | 42.85 | +1.7 % |
| H2A | 12.17 | 12.17 | 8.50 | 8.50 | -30.2 % |
| H2B | 1.95 | — | 4.30 | 4.30 | +120.5 % |
| H3A | 4.08 | — | 4.10 | 4.10 | +0.5 % |
| H3B | 6.17 | — | 6.75 | 6.75 | +9.4 % |
| E2 | 29.30 | — | 29.50 | 29.50 | +0.7 % |
| E1 | 27.88 | — | 23.25 | 23.25 | -16.6 % |
| F | 3.26 | — | — | — | — |
| I | 4.52 | — | 3.74 | 3.74 | -17.2 % |
| A | 20.27 | — | 24.30 | 24.30 | +19.9 % |
| B | 3.17 | — | 2.75 | 2.75 | -13.2 % |
| D | 5.14 | — | 6.15 | 6.15 | +19.6 % |
| C | 3.17 | — | 2.75 | 2.75 | -13.2 % |
| COLUMN WRAP | 72.00 | — | 72.00 | 72.00 | +0.0 % |
| SOFFIT SIDE | 65.31 | — | — | — | — |
| **Total** | **707.13** | **188.30** | **617.37** | **534.65** | **−24.4 %** |

Notas:
- La lectura **B** se acerca bastante en los types principales:
  - type 2: 279.18 vs 278.57 (+0.2 %);
  - type 3: −0.1 %;
  - H1: +1.7 %;
  - E2: +0.7 %;
  - column wraps: 72.0 = 72.0.
- Le faltan los soffit sides (65.31 LF) y el type F, y el type 4 queda en −18 % porque toma los arcos del hourglass como "curved".
- La lectura **A** quedó incompleta: solo 11 walls, todos en A-101 (188 LF, .50). El modelo terminó antes de leer todo el set, con presupuesto de sobra.
- La **resolución** partió del canon A (como pedía el prompt) y bajó el total a 534.65. Por ejemplo, type 2 quedó en 191.61, cuando B tenía 279.18.

## Reconciliación de ids
- Emparejó 19 walls de 42. La geometría coincide: el W01 de B está a menos de 2 pt de W2-03.
- No emparejó más por tres razones:
  - otros nombres de type (column wraps como tag "C25", no como `element: column_wrap`);
  - otra partición de los tramos;
  - ids de nodes distintos.
- Decisiones "sin objeto": 229, todas listadas en `reconciliacion.json` y NO aplicadas:
  - G1: 62 walls (los perimeter walls, que la lectura ya no trae: es correcto), 28 nodes, 9 misc;
  - G2: 72 nodes, 16 walls, 13 misc;
  - G3: 26 walls, 2 strips, 1 blocking.

## Causas y arreglos antes de otra corrida (sin gastar)
1. **Lectura incompleta (A).** Agregar una compuerta de script después de cada lectura: el canon debe cubrir todas las hojas de planta y todos los types del schedule (inventario + schedule leído). Si falta algo, la misma llamada continúa sobre lo faltante en vez de pasar a comparar.
2. **Esquema.**
   - Dar al modelo en su sandbox el validador de esquema de canon.py (`canon.py` en modo validación) y exigir que el canon lo pase antes de responder "OK".
   - Fijar en el prompt los nombres de `element` (column_wrap, soffit_side) y la representación de walls curvos.
3. **Resolución.** Que parta de la lectura más completa, o de la unión, y resuelva por diferencia. Hoy parte siempre de A.
4. **Reconciliación.**
   - Normalizar type / element antes de emparejar (por ejemplo "C25" → column_wrap).
   - Emparejar también por eje / tramo (por ejemplo, un wall de la referencia contra varios tramos de la lectura).
   - Excluir los nodes del overlay: se regeneran desde los walls.

Estado: no se relanzó. Una segunda corrida costaría otros ~$5–10, y con estos cuatro arreglos pendientes repetiría el mismo tope. Queda a decisión del usuario.
