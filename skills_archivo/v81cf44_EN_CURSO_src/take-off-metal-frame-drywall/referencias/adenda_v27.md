# ADENDA v<n> — <n>-sep-<n> · la compuerta de SIGNIFICADO de columna

## De dónde salió

Rodolfo leyó el Excel y preguntó: *"¿por qué este tiene <n> layers?"*

El wall A1 #n decía **Layers <n>**. No tiene <n> layers: tiene **<n>** (una de 5/8" por face). Lo que tiene son **<n> filas de face**, porque su lado este da a tres cuartos con ceilings distintos:


la suma de los tramos = **[valor retirado E24] LF** = el length del wall. El generador sumaba `<n>+<n>+<n>+<n>`.

**Lo grave no es el <n>. Es que nada lo atrapó.** Los sellos prueban que el cierre es coherente consigo mismo. La aserción de sobrantes prueba que ninguna line item se cae. Pero **nada probaba que una columna de resumen significara lo que dice su encabezado**. El board estaba bien (sale face por face), así que ningún control de cantidad lo iba a ver.

## REGLA — Una columna de resumen no se entrega sin una recomputación independiente

**Toda columna que se calcula sumando filas de detalle se recomputa por OTRA VÍA antes de escribir el entregable, y si las dos no coinciden, el entregable NO se genera.**

"Otra vía" quiere decir que no sea la misma suma: si el generador suma filas, la verificación tiene que llegar al mismo número por una ruta distinta. Para *Layers*:

(ejemplo de una corrida retirado del paquete ciego)

([valor retirado E24] + <n> + <n> + <n>) ÷ [valor retirado E24] = **<n>** ✓

Si un tramo de un lado no lleva board, el resultado da un decimal honesto — en un caso real un wall dio **[valor retirado E24]**, porque un tramo de su lado este (donde muere un wall perpendicular) no lleva board de ese wall. Ese decimal **es información, no un error de redondeo**: no se fuerza a <n>.

## La pregunta que hay que hacerle a cada columna

Antes de escribir una columna derivada: **¿la suma de las filas significa lo mismo que el encabezado?**


Las tres que dicen NO son exactamente los tres errores que aparecieron en este proyecto.

## Qué verifica la compuerta (`verif_columnas.py`)

Corre **antes de escribir una sola celda**. Nueve comprobaciones, cada una probada con su error inyectado:


**El margen del 5% en B no es laxitud, es geometría:** un wall inclinado tiene faces de length distinto y el `largo` es el EJE. En un caso real, un wall inclinado tenía faces de [valor retirado E24] y [valor retirado E24] con eje [valor retirado E24] — la face larga pasaba del eje, dentro del margen, legítimamente. Cero tolerancia lo habría rechazado. Eso lo descubrió la propia compuerta en su primera run.

## REGLA — Una compuerta que nunca se ha visto fallar no sirve

`test_verif_columnas.py` **inyecta cada error a propósito** y exige que la compuerta lo cace, más un caso final que exige que el set real pase limpio. Si se añade una comprobación, se añade su caso.

Una compuerta que solo se ha corrido sobre datos buenos no prueba nada: prueba que no molesta.

## REGLA — El decimal raro se investiga, no se redondea

Un número de layers no entero no es ruido. Es un tramo de un lado sin board, y la razón está en el cierre. Antes de redondear cualquier resultado que "casi" da redondo, hay que saber de dónde sale la diferencia. Si no se sabe, no se redondea: se investiga.

---
