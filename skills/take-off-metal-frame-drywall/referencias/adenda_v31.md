# ADENDA v31 — 28-sep-2026 · NINGÚN CAMBIO ESTÁ TERMINADO HASTA QUE EL EXCEL SE REGENERA

## De dónde salió

Rodolfo: *"¿ya actualizaste el excel sheet? Si no, hazlo, y crea regla que cada vez que haya cambios el excel sheet se tiene que actualizar también."*

## El riesgo que cubre

Se corrige un cierre — el width de una banda de FRP, la height de un wall, el W.R. gypsum board de una zona húmeda. La corrección queda **sellada**. `resumen_total` dice **77 sellos OK / 0 rotos**. Todo verde.

Y el único papel que alguien usa para comprar material sigue diciendo lo viejo.

> **Un cierre corregido que no llegó al Excel no existe para quien compra.**

El sello prueba que el cierre es **coherente consigo mismo**. No prueba que el entregable lo refleje. Son dos cosas distintas y hasta ahora sólo una estaba en código.

## REGLA

**Regenerar y entregar son el MISMO acto, y se tiene que poder PROBAR qué estado refleja el archivo.**

No es "acordarse de regenerar": acordarse falla a las dos de la mañana, que es justo cuando se corrige el último cierre.

## COMPUERTA DE VIGENCIA — `verif_vigencia.py`

Al guardar el libro, `excel.py` sella un **manifiesto** al lado del `.xlsx` con el `sha256` de **cada insumo**. `verificar()` los vuelve a calcular y compara.

**Por qué hash y no fecha de modificación:** copiar un archivo o hacerle `touch` falsea el mtime. El hash no. Un entregable que se manda a otra computadora y vuelve sigue siendo verificable.

Caza cinco modos de quedarse viejo:

| # | modo | por qué importa |
|---|---|---|
| 1 | **libro sin manifiesto** | no hay manera de probar que está al día — y no poder probarlo cuenta como falla |
| 2 | **cierre corregido después de generar** | el error original: la corrección está sellada pero no en el Excel |
| 3 | **código del generador cambiado** | un bug arreglado en `dataset.py` mueve los números **aunque ningún cierre se haya tocado**. El código es insumo igual que los datos |
| 4 | **cierre huérfano** | sellado pero el Excel **no lo lee**. Un bloque nuevo que nadie conectó a `dataset.py` es material que no se cobra |
| 5 | **`.xlsx` tocado a mano** | lo que se entrega ya no es lo que el generador produjo |

### El modo 4 es el más caro y el más silencioso

Un cierre sellado que el generador no lee no aparece en ningún lado: ni en el Excel, ni como falla, ni como pendiente. Por eso la compuerta barre el directorio y exige que **todo** `*cierre*.json` esté en una de dos listas: o lo lee el generador (`fuentes()`), o está declarado en `SUPERADOS` **con su motivo escrito**. No hay tercera opción. Es la misma compuerta de cobertura del wall inclinado, aplicada a los archivos.

### Los insumos se le preguntan al GENERADOR, no se barren con glob

`fuentes()` recorre las mismas rutas que `resumen_global.SRC` y `dataset.py`. Un glob suelto del directorio metería archivos que el libro no lee (`MEP_cruces.json`, `inventario.json`, versiones superadas como `G_cierres.json` frente a `G_cierres_v2.json`) y la compuerta gritaría por cosas que no afectan el entregable.

> **Una compuerta que da falsas alarmas se termina ignorando, y entonces es peor que no tenerla.**

### Probada viéndola fallar

`test_verif_vigencia.py` reinyecta los cinco modos y exige que cada uno sea cazado **por su nombre**, más un caso final que exige que el set real pase limpio: **6 ok, 0 fallos**.

```
  libro sin manifiesto                           CAZADO
  cierre corregido despues de generar            CAZADO
  codigo generador cambiado                      CAZADO
  cierre sellado que el Excel no lee             CAZADO
  .xlsx modificado a mano                        CAZADO
  set real intacto (no debe quejarse)            OK
```

## UNA SOLA PUERTA DE SALIDA — `entregar.py`

```
1/4  SELLOS      -> resumen_total, 77/77. Un sello roto para todo aquí.
2/4  REGENERA    -> excel.main() SIEMPRE, aunque "no haya cambiado nada".
                    Genera -> recalcula -> audita el libro -> sella el manifiesto.
3/4  VIGENCIA    -> prueba por hash que el .xlsx refleja todos los insumos de hoy.
4/4  COPIA       -> y sólo entonces se copia a la carpeta de entrega.
```

La copia ocurre **después** de la compuerta y **no hay otra ruta**. No es que esté prohibido entregar un libro viejo: es que no se puede.

## Corolario para el ORDEN PERMANENTE

El paso 4 ("guardarla") ahora incluye **regenerar el entregable**:

1. La solución — corregir el número y volver a sellar.
2. La regla — escrita como regla reusable, no como nota del proyecto.
3. La compuerta — en código, **probada viéndola fallar**.
4. Guardarla en memoria y en el skill — **y regenerar el Excel**.

> Un turno que corrigió un número y no volvió a escribir el Excel **no está cerrado**, aunque la memoria y el skill ya tengan la regla.

## Error de la propia compuerta, cazado en su primer arranque

`entregar.py` leía el resultado de los sellos tomando la **última línea** de `resumen_total.py`. Pero ese script sigue imprimiendo renglones de material después del TOTAL, así que la última línea era `TRIM_CEILING ... 12.01` y la compuerta reportó **"SELLO ROTO"** con los 77 sellos intactos. Una falsa alarma en el primer minuto de vida.

> **REGLA — La salida de otra herramienta se parsea por CONTENIDO, nunca por posición.**
> Se busca el renglón que dice `sellos OK`. Si no aparece ninguno, eso también es falla —
> pero es una falla distinta, y se reporta distinto: *"resumen_total no reportó sellos"*,
> que manda a mirar la herramienta, no los cierres.

Vale para todo: leer la última línea, la primera, la línea *n*, o una columna por su número, es acoplarse a un formato que nadie prometió mantener.

---
