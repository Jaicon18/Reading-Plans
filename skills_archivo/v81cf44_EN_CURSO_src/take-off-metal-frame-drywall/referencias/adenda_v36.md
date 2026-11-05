# ADENDA v<n> — <n>-oct-<n> · LA CADENA DE DETALLES SE SIGUE HASTA EL FINAL

Orden de Rodolfo, textual:

> "siempre se tiene que usar los detalles que marcan los planos ya que ahí está la
> información que se necesita, nunca saltarse esta regla."
> "nunca dejes de usar los detalles y cita la hoja y los detalles."
> "vas a citar absolutamente todas las páginas y todos los detalles que traiga esa página."
> "tienes que revisar todos y cada uno de los detalles, por ejemplo en el canopy <n> son <n>…
> pero en otros habrá más."
> "en las partitions se tiene que hacer lo mismo, revisar todos los detalles, y hay veces
> que son varios — conviértelo en regla inviolable."

## Las cuatro partes de la regla

**<n>. El detalle que el plano señala ES la fuente de ese elemento.** No la planta, no la
geometría medida, no el criterio de oficio. La burbuja es el arquitecto diciendo "la
información está aquí". Medir en planta lo que un detalle ya define es inventar una segunda
fuente para un dato que ya tenía una.

**<n>. La cadena se sigue hasta el final.** Un detalle llama a otro detalle. Se recorre nivel
por nivel hasta que no quede burbuja, y se abren TODOS los eslabones, no solo el último.

Un canopy, tres niveles:
`soffit plan (burbuja D/A9.22)` → `D/A9.22 SECTION` (burbuja `7/A9.26` sobre la marquesina)
→ `7/A9.26 <título del detalle>`

Y `D/A9.22` sola llama a cinco: `4/A9.26` parapet SIM · `7/A9.26` canopy · `11/A9.27`
storefront head · `10/A9.27` storefront sill · `5/A9.26` ACM base.

**En una partition la cadena típica es:** tag en planta → fila del Partition Schedule →
DETALLE del tipo → los detalles que ESE detalle llama (jamb, head, sill, base, transición,
encuentro, bulkhead). Ninguna partition se cierra hasta abrir la cadena completa.

**<n>. Toda line item cita HOJA + DETALLE, en forma `N/HOJA` legible por máquina.** No solo
CONFIRMADO: también DERIVADO. Una derivación descansa sobre algo dibujado, y eso tiene hoja
y número. "La sección del este" en prosa no sirve — una cita que una máquina no puede leer
no se puede auditar.

**<n>. Al citar una hoja se lista el inventario COMPLETO de sus detalles**, con número y
título, y qué pasa con cada uno: usado, no aplica (con motivo) o pendiente. Así el estimador
va directo a la imagen y ningún detalle de una hoja que ya se está tocando queda escondido.

## Qué lo originó


## Las compuertas

**`verif_callouts.py` — NUEVA, paso <n> de <n> de `entregar.py`.** Barre las burbujas de
sección y detalle y exige que cada una esté citada por un cierre o declarada con motivo.

Se diferencia de `verif_detalles.py`: aquella mira, de las hojas que el take-off YA cita,
cuáles detalles quedaron sin abrir — solo ve donde ya miraste. Ésta mira lo que el PLANO
SEÑALA. Es la que caza `7/A9.26`, porque la burbuja está en `D/A9.22` aunque el take-off no
citara esa hoja.

**Y sigue la cadena:** barría solo las hojas de PLANTA — el primer eslabón — y pasó de ver
**<n>** callouts sin usar a **<n>** al barrer también las hojas de detalle y sección
(`A9.`, `A11.`, `A12.`, `S<n>.`, `S<n>.`, `S<n>.`). Una cadena cortada en el segundo eslabón es
tan ciega como no haber empezado.

**`closer.py` — exigencia nueva.** Antes la hoja se pedía solo a CONFIRMADO. Ahora toda
line item, CONFIRMADO o DERIVADO, lleva su cita `N/HOJA`. Destapó que **una parte grande de las line items
selladas no tiene cita de hoja + detalle**.

## Dos bugs propios al escribir la compuerta, los dos de normalización

1. **Rellenar el número de hoja a dos dígitos** convertía `S5.20` en `S05.20` — una hoja que
   no existe. El estimador la busca y no la encuentra. Se canoniza QUITANDO el cero
   (`A09.<n>` → `A9.<n>`), nunca agregándolo: la serie estructural se escribe con un dígito.
2. **Comparar la burbuja normalizada contra el rótulo SIN normalizar** hizo que la compuerta
   exigiera citar los detalles de la propia hoja. **Los dos lados se normalizan antes de
   comparar.**

---
