# ADENDA v38 — 4-oct-2026 · EL ORDEN DE TRABAJO: PLANO → CADENA → TOTAL → EXCEL

## ⛔ SUPER REGLA INVIOLABLE

Orden de Rodolfo, textual:

> "desde este momento así será la secuencia: 1.- se hace primero el **first floor plan**, una
> vez terminado se continúa con la secuencia de los detalles tal como lo hiciste en este
> momento, y seguir la secuencia hasta obtener el total de la cantidad de material que estamos
> cuantificando. Y una vez teniendo los resultados, en el excel sheet siempre anotar toda la
> secuencia de detalles que se cuantificó."

Lo repitió IGUAL para el **reflected ceiling plan (RCP)**. Son **dos puertas de entrada**, una
por familia de elemento, y de ahí la misma cadena hasta el total.

### Los cuatro pasos, en orden, sin saltarse ninguno

**1. Se empieza por el PLANO, y se TERMINA el plano antes de abrir un detalle.**
Floor plan para walls, partitions y aberturas. RCP para ceilings, soffits y marquesinas.
*Terminar* = tener la lista completa de instancias, con su geometría y sus burbujas
localizadas. Nunca arrancar por un detalle suelto ni por el schedule.

**2. Desde el plano se sigue la CADENA de detalles**, eslabón por eslabón, abriendo cada
burbuja y cada detalle que ese detalle llama.

**3. Se sigue la cadena HASTA OBTENER EL TOTAL** del material que se cuantifica. No se para en
el detalle que dio el dato que se fue a buscar: se para cuando la cantidad está completa.

**4. En el Excel se anota SIEMPRE la secuencia completa**, en el renglón de ese elemento y
**en el orden en que se recorrió** — plano → sección → detalle → detalle del detalle → cruce
MEP → schedule. No basta citar el último detalle: va el camino entero, para que el estimador
abra las imágenes en el mismo orden en que se leyeron.

### El ejemplo que la originó — canopy 84

```
A04.01 (RCP)
   └─ D/A09.22 SECTION D          largo en planta, y el fondo
         └─ 7/A09.26 @ SIDE CANOPY   composición y datums de la fascia
               └─ 7/S5.20 METAL STUD PROPERTIES   perfil y 16" O.C.
```

**Ningún eslabón da la cantidad solo:**

| eslabón | qué aporta |
|---|---|
| `A02.01` / `A04.01` | el length y la posición |
| `D/A09.22` | el fondo, y lo confirma contra la planta |
| `7/A09.26` | la composición y los datums `T/STUD [valor retirado E24]` − `B/STUD [valor retirado E24]` |
| `7/S5.20` | el perfil `362S137-33` y el 16" O.C., que **ningún detalle de canopy rotula** |

Y de paso la cadena resolvió un pleito abierto hacía días: la dimension de D/A09.22 y los
`[valor retirado E24] ft` medidos en planta **nunca estuvieron en conflicto**. Localizando los dos ticks de
la dimension en el vector del PDF (coordenada x de cada tick, escala en pt/ft calibrada contra tres
datums) se ve que la dimension va de **eje 8** a **fascia**, no de face de wall a fascia. La
diferencia son exactamente los **8"** que 7/A09.26 imprime arriba. Dos caminos independientes,
a dos escalas distintas, a una milésima de pie.

## La herramienta: `cadena_detalles.py`

La secuencia **no se teclea a mano**: se deriva.

1. **Grafo de burbujas** del set — qué hoja dibuja una burbuja hacia qué hoja.
2. **Profundidad** de cada hoja = su distancia BFS desde las hojas de planta.
3. Los **schedules** van siempre al final: no son un eslabón de la cadena, son la tabla donde
   se mira el perfil una vez que ya se sabe qué elemento es.
4. Dentro de un nivel se ordena por hoja y etiqueta, para que dos runs den la misma cadena.

No inventa eslabones: **solo ordena los que el cierre ya cita.** Si un cierre cita poco, la
cadena sale corta — y eso es justamente lo que hay que ver.

### Tres cosas que costaron

**1. El grafo del cache venía INCOMPLETO y no daba error.** `detalles_cache.json` traía
`A2.01 → A9.02, A9.25` pero **no** `A9.21/A9.22/A9.23`, y `A4.01` no aparecía señalando nada
cuando dibuja **ocho** burbujas de sección. Con ese grafo la cadena del wall exterior empezaba
por el detalle en vez de por el plano.
> **Un grafo incompleto no falla: devuelve una cadena más corta y plausible.** Se rebarre con
> el MISMO detector de burbujas de la compuerta, hoja por hoja, y se cachea aparte.

**2. No todo enlace del set es una burbuja.** La planta remite a las elevaciones interiores por
el **rombo** y al Partition Schedule por el **tag**: dos símbolos que el detector de burbujas no
ve. Sin un nivel de reserva por serie de hoja, esas hojas caen al fondo y la cadena sale
**ordenada alfabéticamente**, que es exactamente lo que la regla prohíbe.

**3. Ordenar hojas como texto pone `A12.01` antes que `A9.02`**, porque "1" < "9". La hoja se
ordena por `(serie, número, subnúmero)`, nunca por su cadena de caracteres.

## Lo que la columna destapó el primer día

Los **cinco ceilings GWB** (`CIELO-70` a `CIELO-74`) terminan su cadena en `A04.01` y **no citan
ni un detalle**: se cerraron con el tag del RCP y la geometría del cuarto. El área y el
perímetro no cambian por eso; lo que **no está verificado** es la suspensión (calibre y
espaciamiento de hanger, carrying y furring channel) y la condición de borde de cada cuarto.
Queda escrito como Pending Item, no se adivina.

> **Una columna nueva que no destapa nada el primer día probablemente no está midiendo nada.**


## CORRECCIÓN DEL MISMO DÍA — dos errores que la columna destapó en cuanto se miró

Rodolfo pidió la imagen de `01/A9.02` y de ahí salieron **dos bugs**, los dos del mismo
tipo: *escribir una forma de número de hoja que el plano no usa*.

### 1. `01/A9.02` no existe — era la cola del número de hoja anterior

Escribir dos números de hoja separados por barra —`"la leyenda de A09.01/A09.02"`,
`"A02.01 / M01.01"`, `"sheet note D de A12.04/A12.05"`— hacía que el patrón de citas leyera
la **cola del primer número** como etiqueta de detalle:

| falsa | de dónde salía | veces |
|---|---|---|
| `01/A09.02` | `A09.01/A09.02` | **75** |
| `27/A09.33` | `A09.27/A09.33` | 1 |
| `01/M01.01` | `A02.01 / M01.01` | 4 |
| `01/P01.02` | `A02.01 / P01.01 / P01.02` | 2 |
| `01/A12.01` | `A02.01/A12.01` | 1 |
| `01/P01.01` | `A02.01 / P01.01` | 1 |
| `04/A12.05` | `A12.04/A12.05` | 1 |

Iban **impresas en la columna `Detail sequence`**, mandando al estimador a buscar una imagen
que no está.

**Defensa doble:** si justo antes de la etiqueta hay cola de número de hoja, se descarta; y
ninguna etiqueta real lleva **cero a la izquierda** — un detalle es `1`, `11`, `D`, nunca
`01`. Y `verif_callouts.py` dejó de tener su propia copia del patrón: **la compuerta y la
cadena usan el MISMO lector de citas.**

### 2. `A4.01` no existe — la forma canónica no se escribe

> [stated] Rodolfo: *"no existe la A4.01, rectifícalo"*.

Tenía razón. La forma canónica **quita** el cero para poder comparar `A09.22` con `A9.22`
(y para no convertir `S5.20` en `S05.20`, que fue el bug de la v36). Pero esa forma es
**interna**. Escribirla manda a buscar una hoja que no existe: en este set las series
**A, E, M y P se imprimen con DOS dígitos** (`A04.01`, `M01.01`) y **solo la serie S va con
uno** (`S5.10`).

> **El rótulo de display no se deduce con una regla: se LEE del title block de cada hoja.**
> `cadena_detalles.real()` devuelve el número tal como está impreso, y es lo único que se
> escribe en el Excel, en los documentos y en la salida de la compuerta.

**El par de reglas, que son una sola:** hay DOS formas del número de hoja y no se mezclan —
la **canónica**, para comparar, que quita el cero; y la **real**, para escribir, que se lee
del title block. Un número de hoja que el estimador no puede buscar no es una cita.

---
