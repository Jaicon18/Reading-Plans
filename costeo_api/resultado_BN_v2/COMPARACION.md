# B&N — corrida real del runner (2026-10-30): resultado y comparación contra rev13

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
