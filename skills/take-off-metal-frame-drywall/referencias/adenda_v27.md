# ADENDA v27 — 28-sep-2026 · la compuerta de SIGNIFICADO de columna

## De dónde salió

Rodolfo leyó el Excel y preguntó: *"¿por qué este tiene 4 layers?"*

El wall A1 #8 decía **Layers 4**. No tiene 4 layers: tiene **2** (una de 5/8" por face). Lo que tiene son **4 filas de face**, porque su lado este da a tres cuartos con ceilings distintos:

| fila | tramo | alto | por qué |
|---|---|---|---|
| Corridor 111 | 17.06 LF (face oeste completa) | 9.000 | — |
| Break Room 118 | 3.12 LF | 9.000 | ACT-5 a 8'-6" + 6" |
| Electrical 120 | 6.24 LF | 12.830 | A04.01 key note 1 `OPEN TO STRUCTURE ABOVE` |
| NER 121 | 7.70 LF | 12.700 | mismo key note, deck interpolado |

3.12 + 6.24 + 7.70 = **17.06 LF** = el length del wall. El generador sumaba `1+1+1+1`.

**Lo grave no es el 4. Es que nada lo atrapó.** Los sellos prueban que el cierre es coherente consigo mismo. La aserción de sobrantes prueba que ninguna line item se cae. Pero **nada probaba que una columna de resumen significara lo que dice su encabezado**. El board estaba bien (sale face por face), así que ningún control de cantidad lo iba a ver.

## REGLA — Una columna de resumen no se entrega sin una recomputación independiente

**Toda columna que se calcula sumando filas de detalle se recomputa por OTRA VÍA antes de escribir el entregable, y si las dos no coinciden, el entregable NO se genera.**

"Otra vía" quiere decir que no sea la misma suma: si el generador suma filas, la verificación tiene que llegar al mismo número por una ruta distinta. Para *Layers*:

```
capas = Σ(capas_cara × largo_cara) ÷ largo_muro
```

(17.06 + 3.12 + 6.24 + 7.70) ÷ 17.06 = **2.00** ✓

Si un tramo de un lado no lleva board, el resultado da un decimal honesto — el wall 28 da **1.97**, porque 0.33 ft de su lado este (donde muere un wall perpendicular) no lleva board de ese wall. Ese decimal **es información, no un error de redondeo**: no se fuerza a 2.

## La pregunta que hay que hacerle a cada columna

Antes de escribir una columna derivada: **¿la suma de las filas significa lo mismo que el encabezado?**

| encabezado | lo que suman las filas | ¿coinciden? |
|---|---|---|
| `Layers` (layers totales, las dos faces) | número de renglones de face | **NO** — hay que dividir por el length |
| `Board (SF)` | SF de cada face | sí |
| `Length (LF)` (length del wall) | length de cada fila de face | **NO** — un lado partido suma dos veces |
| `Stud (pcs)` | piezas de cada tramo | sí |
| `Stud (LF)` | piezas × una height | **NO** si el wall cruza el eje de cambio de deck |

Las tres que dicen NO son exactamente los tres errores que aparecieron en este proyecto.

## Qué verifica la compuerta (`verif_columnas.py`)

Corre **antes de escribir una sola celda**. Nueve comprobaciones, cada una probada con su error inyectado:

| # | comprueba | caza |
|---|---|---|
| A | `Layers` = layer-pies ÷ length, y `0.9 ≤ capas ≤ 8` | sumar filas de face |
| B | ninguna face pasa del eje más de 5% | una face con el length de otro wall |
| B2 | las faces no cubren más lados de los que el wall tiene | una fila de face de sobra |
| C | board del wall = suma de sus faces | un total escrito a mano |
| D | cada face reproduce `L × H × capas − ded` | una fila que no se recalcula sola |
| D2 | deducción ≥ 0 | pareja `L × H` equivocada al leer la operación |
| D3 | no hay deducción en un wall sin aberturas | **deducción fantasma** — el síntoma del texto de operación desactualizado |
| E | `(bottom + top) ÷ largo` = 2 runs por row | track duplicado o faltante |
| F | `stud LF ÷ pz` dentro de `[0.60, 1.05] × altura` | height aplastada en un wall de dos alturas |

**El margen del 5% en B no es laxitud, es geometría:** un wall inclinado tiene faces de length distinto y el `largo` es el EJE. El wall 40 tipo F tiene faces de 17.458 y 18.067 con eje 17.762 — la face larga pasa del eje un 1.7%, legítimamente. Cero tolerancia lo habría rechazado. Eso lo descubrió la propia compuerta en su primera run.

## REGLA — Una compuerta que nunca se ha visto fallar no sirve

`test_verif_columnas.py` **inyecta cada error a propósito** y exige que la compuerta lo cace, más un caso final que exige que el set real pase limpio. Si se añade una comprobación, se añade su caso.

Una compuerta que solo se ha corrido sobre datos buenos no prueba nada: prueba que no molesta.

## REGLA — El decimal raro se investiga, no se redondea

`1.97` layers no es ruido. Es 0.33 ft de un lado sin board, y la razón está en el cierre. Antes de redondear cualquier resultado que "casi" da redondo, hay que saber de dónde sale la diferencia. Si no se sabe, no se redondea: se investiga.

---
