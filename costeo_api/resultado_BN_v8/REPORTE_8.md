# B&N corrida #8 (2026-10-31)

- Gasto #8: $10.61 (lectura A $3.86, lectura B $4.34 que no pasó su compuerta, 3 correcciones $2.41). Total del modo automático a la key: ≈ $12.21 de $60.
- Resultado: la corrida se detuvo en canon.py por un error del programa (nodes que citaban walls excluidos, BE-96). Arreglado (R80e.60) y re-armada sin API: canon.py pasa; el Excel no arma sin una corrección de lectura (accesorios PENDIENTE: extra framing ATM, gypsum board jamb return, access panel, Level 5 finish).
- Una sola lectura usable (B no pasó): sin cruce A/B. La #8 sale peor que la #7 en casi todo.

## Banco de regresión (material x lectura, vs rev13; familias_out.json)

| Material | rev13 | r3 | r4 | r5 | r7 | r8 |
|---|---|---|---|---|---|---|
| 5/8" gyp board Type X | 14,267 | -8.9 % | -8.9 % | +7.3 % | +9.3 % | +25.4 % |
| 5/8" gyp Type X W.R. | 1,093 | +15.3 % | +8.0 % | -10.1 % | -13.7 % | -23.3 % |
| 3-5/8" stud (todos los gauges) | 11,663 | -52.6 % | -32.3 % | -8.1 % | -19.7 % | -31.5 % |
| 6" stud (todos los gauges) | 3,162 | -49.4 % | -38.0 % | -46.2 % | -1.4 % | +41.2 % |
| 8" stud (todos los gauges) | 25 | +0.0 % | +0.0 % | +0.0 % | +0.0 % | +0.0 % |
| bottom track (todos) | 641 | -21.5 % | -5.1 % | -9.5 % | -7.0 % | -17.3 % |
| track de ceilings / soffits | 181 | +45.7 % | +55.7 % | +67.8 % | +66.9 % | +66.9 % |
| bracing C.R. channel | 2,884 | -55.5 % | -38.5 % | +0.8 % | -8.0 % | -5.8 % |
| cement board | 434 | -9.3 % | +125.7 % | -29.4 % | -13.8 % | -58.7 % |
| 5/8" cement board | 50 | -100.0 % | -100.0 % | -100.0 % | -100.0 % | -100.0 % |
| FRT plywood (SF) | 3,057 | -36.4 % | +37.6 % | +31.7 % | -18.0 % | -44.2 % |
| FRT blocking | 568 | -2.8 % | -2.8 % | -2.8 % | -2.8 % | -2.8 % |
| FRP | 2,001 | +0.0 % | +0.0 % | +4.4 % | +0.0 % | +0.0 % |
| metal trim (corner bead, casing, shadow molding) | 957 | -29.1 % | -8.0 % | -31.2 % | -3.1 % | -28.5 % |
| metal stud blocking (362CR / STUD BLOCKING) | 0 | — | — | — | — | — |
| nested inner runner (deflection head) | 480 | -100.0 % | -100.0 % | -100.0 % | -100.0 % | +0.0 % |

r4: Excel no armó (sin corrección): FALLA S:etapa-5-entrega | Excel | Partition Takeoff: renglón 'F  #F-01  -  F-01' PENDING (partition_types sin dato obligatorio: se resuelve en el canon antes de

r5: Excel no armó (sin corrección): [bitacora] rc=1 log=/home/user/takeoff_runtime/banco5/r5/takeoff_work/bitacora_logs/plantilla_excel.py_20261031T073352.log

r8: Excel no armó (sin corrección): [bitacora] rc=1 log=/home/user/takeoff_runtime/banco5/r8/takeoff_work/bitacora_logs/plantilla_excel.py_20261031T073633.log

EMPEORA: nada

## LF por type (canon)

| Type | rev13 LF | #7 LF | #7 Δ | #8 LF | #8 Δ |
|---|---|---|---|---|---|
| 1 | 0.0 | 0.0 | — | 54.2 | — |
| 2 | 278.6 | 259.8 | -6.7 % | 230.6 | -17.2 % |
| 3 | 38.7 | 38.7 | +0.0 % | 25.6 | -33.8 % |
| 4 | 83.6 | 64.8 | -22.5 % | 9.0 | -89.2 % |
| 5 | 5.7 | 5.7 | +0.0 % | 8.7 | +53.2 % |
| A | 20.3 | 20.9 | +3.0 % | 16.0 | -21.3 % |
| B | 3.2 | 3.2 | +0.0 % | 2.7 | -14.2 % |
| C | 3.2 | 3.2 | +0.0 % | 2.7 | -14.2 % |
| COLUMN WRAP | 72.0 | 72.0 | +0.0 % | 72.0 | +0.0 % |
| D | 5.1 | 6.2 | +20.0 % | 5.8 | +13.0 % |
| E1 | 27.9 | 24.8 | -10.9 % | 5.3 | -80.8 % |
| E2 | 29.3 | 29.4 | +0.5 % | 29.1 | -0.7 % |
| F | 3.3 | 3.2 | -0.3 % | 3.2 | -0.3 % |
| H1 | 42.1 | 41.7 | -1.1 % | 42.1 | +0.0 % |
| H2A | 12.2 | 4.5 | -63.0 % | 4.5 | -62.9 % |
| H2B | 1.9 | 2.0 | +1.0 % | 1.9 | +0.0 % |
| H3A | 4.1 | 4.0 | -1.2 % | 6.2 | +51.2 % |
| H3B | 6.2 | 6.2 | +0.8 % | 4.1 | -33.9 % |
| I | 4.5 | 5.2 | +15.1 % | 6.0 | +32.9 % |
| SOFFIT SIDE | 65.3 | 39.1 | -40.2 % | 39.1 | -40.2 % |
