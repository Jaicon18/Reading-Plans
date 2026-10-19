# ADENDA v<n> — <n>-sep-<n> · NINGÚN CAMBIO ESTÁ TERMINADO HASTA QUE EL EXCEL SE REGENERA

## De dónde salió

Rodolfo: *"¿ya actualizaste el excel sheet? Si no, hazlo, y crea regla que cada vez que haya cambios el excel sheet se tiene que actualizar también."*

## El riesgo que cubre

Se corrige un cierre — el width de una banda de FRP, la height de un wall, el W.R. gypsum board de una zona húmeda. La corrección queda **sellada**. `resumen_total` dice **<n> sellos OK / <n> rotos**. Todo verde.

Y el único papel que alguien usa para comprar material sigue diciendo lo viejo.

> **Un cierre corregido que no llegó al Excel no existe para quien compra.**

El sello prueba que el cierre es **coherente consigo mismo**. No prueba que el entregable lo refleje. Son dos cosas distintas y hasta ahora sólo una estaba en código.

## REGLA

**Regenerar y entregar son el MISMO acto, y se tiene que poder PROBAR qué estado refleja el archivo.**

No es "acordarse de regenerar": acordarse falla a las dos de la mañana, que es justo cuando se corrige el último cierre.

## COMPUERTA DE VIGENCIA — `verif_vigencia.py`

Al guardar el libro, `excel.py` sella un **manifiesto** al lado del `.xlsx` con el `sha<n>` de **cada insumo**. `verificar()` los vuelve a calcular y compara.

**Por qué hash y no fecha de modificación:** copiar un archivo o hacerle `touch` falsea el mtime. El hash no. Un entregable que se manda a otra computadora y vuelve sigue siendo verificable.

Caza cinco modos de quedarse viejo:


### El modo <n> es el más caro y el más silencioso

Un cierre sellado que el generador no lee no aparece en ningún lado: ni en el Excel, ni como falla, ni como pendiente. Por eso la compuerta barre el directorio y exige que **todo** `*cierre*.json` esté en una de dos listas: o lo lee el generador (`fuentes()`), o está declarado en `SUPERADOS` **con su motivo escrito**. No hay tercera opción. Es la misma compuerta de cobertura del wall inclinado, aplicada a los archivos.

### Los insumos se le preguntan al GENERADOR, no se barren con glob

`fuentes()` recorre las mismas rutas que `resumen_global.SRC` y `dataset.py`. Un glob suelto del directorio metería archivos que el libro no lee (`MEP_cruces.json`, `inventario.json`, versiones superadas como `G_cierres.json` frente a `G_cierres_v<n>.json`) y la compuerta gritaría por cosas que no afectan el entregable.

> **Una compuerta que da falsas alarmas se termina ignorando, y entonces es peor que no tenerla.**

### Probada viéndola fallar

`test_verif_vigencia.py` reinyecta los cinco modos y exige que cada uno sea cazado **por su nombre**, más un caso final que exige que el set real pase limpio: **<n> ok, <n> fallos**.

(ejemplo de una corrida retirado del paquete ciego)

## UNA SOLA PUERTA DE SALIDA — `entregar.py`

(ejemplo de una corrida retirado del paquete ciego)

La copia ocurre **después** de la compuerta y **no hay otra ruta**. No es que esté prohibido entregar un libro viejo: es que no se puede.

## Corolario para el ORDEN PERMANENTE

El paso <n> ("guardarla") ahora incluye **regenerar el entregable**:

1. La solución — corregir el número y volver a sellar.
2. La regla — escrita como regla reusable, no como nota del proyecto.
3. La compuerta — en código, **probada viéndola fallar**.
4. Guardarla en memoria y en el skill — **y regenerar el Excel**.

> Un turno que corrigió un número y no volvió a escribir el Excel **no está cerrado**, aunque la memoria y el skill ya tengan la regla.

## Error de la propia compuerta, cazado en su primer arranque

`entregar.py` leía el resultado de los sellos tomando la **última línea** de `resumen_total.py`. Pero ese script sigue imprimiendo renglones de material después del TOTAL, así que la última línea era `TRIM_CEILING ... [valor retirado E24]` y la compuerta reportó **"SELLO ROTO"** con los <n> sellos intactos. Una falsa alarma en el primer minuto de vida.

> **REGLA — La salida de otra herramienta se parsea por CONTENIDO, nunca por posición.**
> Se busca el renglón que dice `sellos OK`. Si no aparece ninguno, eso también es falla —
> pero es una falla distinta, y se reporta distinto: *"resumen_total no reportó sellos"*,
> que manda a mirar la herramienta, no los cierres.

Vale para todo: leer la última línea, la primera, la línea *n*, o una columna por su número, es acoplarse a un formato que nadie prometió mantener.

---
