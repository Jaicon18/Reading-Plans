# ADENDA v<n> — <n>-sep-<n> · la compuerta del LIBRO

## De dónde salió

Rodolfo pidió revisar el Excel entero otra vez. Esta pasada **no miró los cierres: miró el archivo** — a qué celda apunta cada fórmula, hasta dónde llega cada rango, qué divisor usa cada conversión a piezas. Salieron **cinco errores de dinero** y tres de representación.

## Los cinco errores de dinero, todos de la misma raíz

**La clase de waste y el length de existencia se asignaban A MANO renglón por renglón, no se derivaban del material.**


El corner bead es **metal framing cortada a medida**, igual que el track. Estar bajo un encabezado que dice "accesorios" no lo convierte en otra cosa.

Y el modelo sólo tenía **dos** lengths de existencia — stud <n> ft y track <n> ft — así que todo lo demás se forzaba a uno de los dos.

## REGLA — La familia del material manda sobre el waste y sobre el length de compra

**El % de waste y el length de existencia los determina la FAMILIA del material, no la sección del resumen donde uno puso el renglón.**

Cada familia lleva **su propio length de existencia como input editable**:


Nunca reusar el length de otra familia porque "es lo que había".

**El blocking de FRT wood no es ni metal ni board**, así que la regla 15/6 no lo cubre. Se le dio su propia celda de input, **en 0%**, con la decisión declarada en Pending: no se le cambia el precio al estimador sin preguntarle, pero tampoco se esconde que le falta un criterio.

## REGLA — Un PENDIENTE se escribe PENDING, nunca como 0 ni omitido

`RETORNO_BOARD_RANURA` tenía estado PENDIENTE y valor `None`. El agregador lo colapsaba a `<n>` y la hoja lo saltaba con `if v in (None, <n>): continue`.

**Un pendiente desaparecido se lee como "no hay" — lo contrario de lo que dice.**

Ahora los pendientes viajan aparte de las sumas y se escriben con la palabra **PENDING** en amarillo, en la celda de cantidad. Un cero y un pendiente no son lo mismo y nunca se representan igual.

## REGLA — Clasificar por el ENCABEZADO del renglón y por PALABRA COMPLETA

Dos falsos positivos que **se cazó la propia compuerta al escribirla**:

- `stud rein·for·CEMENT` matcheaba la familia Board por la subcadena **"cement"**.
- `Trim - corner bead, casing bead, shadow molding, GYPSUM edge trim` matcheaba Board por el **"gypsum"** de la enumeración — cuando el gypsum edge trim es perfil metálico (J-bead).

Lo que va **antes del guion es lo que el renglón ES**; lo de después es la lista de qué incluye. Se clasifica por la cabeza, y se busca por palabra completa con límites, nunca con `in` a secas. Una clasificación por subcadena siempre termina en un falso positivo de éstos.

## REGLA — Auditar un libro SIN RECALCULAR reporta decenas de fallos fantasma

openpyxl escribe las fórmulas **sin valor cacheado**: hasta que corre `recalc.py`, toda celda de fórmula se lee `None`.

El auditor, sin comprobarlo, reportó **<n> fallos inexistentes** ("todo sale sin waste") y me hizo perder el tiempo buscando un error que no existía.

El auditor ahora comprueba **primero** que haya valores cacheados donde hay fórmulas, y si no, se niega a auditar con un mensaje claro. El orden es siempre **generar → recalcular → auditar**, encadenado en el mismo comando para que no se pueda saltar.

## La compuerta: `verif_libro.py`

`verif_columnas.py` revisa los **datos** antes de escribir. `verif_libro.py` revisa el **archivo** después. Son cosas distintas: aquí se cazan los errores que **sólo existen en el Excel**.

Ocho comprobaciones:

1. el libro está recalculado
2. todo rango `SUM` de la fila de totales cubre todas las filas de dato
3. toda referencia cruzada apunta a una fila de **totales** y a una columna **con encabezado**
4. todo criterio de `SUMIFS` existe de verdad en su columna
5. la familia del material manda sobre el % de waste
6. el divisor de compra corresponde a la familia
7. todo PENDIENTE sale marcado PENDING
8. ningún renglón auxiliar se queda sin llegar al resumen, salvo los declarados-sin-aplicar

Probada con las regresiones reinyectadas: quitándole el waste al trim y devolviéndole el divisor de stud, las caza las dos.

## Lo que sigue sin resolverse, y se dice

**Dos renglones van en PIEZAS y no tienen length**, así que nunca se convierten en LF de stud para comprar: las <n> piezas del framing del soffit CSR y los <n> refuerzos de stud de las penetraciones de MEP. Las piezas están bien y se van a instalar; lo que falta es el length de cada una.

Se listan en piezas para que se vean, **no se doblan dentro de un LF inventado**. Están en Pending Items.

---
