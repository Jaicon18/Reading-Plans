# ADENDA v<n> — <n>-oct-<n> (tarde)
## Cobertura de detalles a cero, atraso de [CONFIRMADO] a cero, y el mapa de adyacencia

Cuatro frentes cerrados. Dos reglas nuevas, las dos del mismo tipo: **sobre qué se puede
afirmar y sobre qué no.**

---

## REGLA 45.1 — UNA CITA QUE PRUEBA QUE EL MATERIAL VA NO PRUEBA CUÁNTO HAY

El trinquete `TOPE_SIN_COTA` bajó de **<n> a <n>**. Los <n> campos que se pagaron no eran
diecinueve casos: eran **dos clases**.

**(a) Cuatro `alto_stud` de walls exteriores marcados `[CONFIRMADO]` citando el B.O.D.**
La height del stud es esa ELEVACIÓN menos el datum `T/SLAB 0'-0"`. Es una **resta**. Que
las dos cifras coincidan pasa sólo porque el datum vale cero. Es la regla de la adenda
v42, ya aplicada al A<n>K, que aquí seguía pendiente.

**(b) Quince cantidades que citaban el detalle que establece el ITEM y no el VALOR** — el
sheathing del canopy, sus TEKS, el corner bead / blocking / trim del soffit, el board W.R.
de los baños. La cita prueba que el material va; el número es una cuenta.

> Una cita que prueba QUE el material va no prueba CUÁNTO hay.
> Es la regla de la v42 —*"un detalle de tipo da la REGLA, no el VALOR"*— aplicada a una
> cantidad en vez de a una height.

**El que queda, declarado en vez de escondido.** `CIELO-nn ACCESS_PANEL = [valor retirado E24]` no es una
dimensión: es un **conteo leído directo de la hoja** (se recorrieron todos los key notes del
RCP y el único "LOCKING ACCESS PANEL" cae en un [room]). No hay printed
dimension que citar y tampoco hay operación que escribir, así que bajarlo a `[DERIVADO]`
sería tan falso como dejarlo. Va en `CONTEOS_DIRECTOS` con su motivo, y la regla no se
debilita para nadie más.

---

## REGLA 45.2 — UN EXTREMO QUE EL MAPA NO RESUELVE NO ES UN EXTREMO LIBRE

El mapa de adyacencia —qué wall muere contra cuál— **ya existe**: `bandas_v<n>.py` +
`adyacencia.py`. Y aun así **no se recontó ni un stud.** Por qué importan las dos cosas:

**El impedimento se levantó.** Las fuentes de geometría que había no pasaban ninguna prueba:
`bandas_por_tipo.json` trae geometrías duplicadas, `inventario.json` resultó tener **cinco**
bandas (todas C<n>) y `wallgeom.py` lleva su propio letrero de que acierta <n> de <n>. Se extrajo
de nuevo del vector de A02.<n> **y se escribió la prueba antes de mirar el resultado**: cada
wall sellado tiene un length verificado; si la extracción no los reproduce, no sirve.

- Primera versión: **36%**. No servía.
- El defecto no era la extracción, era la **convención de extremos**. Las dos faces de un
  wall no terminan en el mismo punto: en cada encuentro una sigue y la otra se corta.
  Tomando la **unión** en vez de la intersección: **<n> de <n> = 87%**.

> Una fuente de geometría no se usa porque exista: se usa porque PASA una prueba, y la
> prueba se escribe antes de mirar el resultado.

**La dirección, que es lo que 5/S5.20 necesita.** La primera versión sólo detectaba
contacto y salían parejas mutuas ("<n> muere contra <n> Y <n> muere contra 1"), que es
imposible. Lo que decide es dónde cae la punta: dentro del tramo del otro = **T** (muere,
y los dos studs van en el pasante); coincidiendo con su extremo = **esquina** (ninguno pasa
de length).

**Lo que el mapa SÍ prueba, medido:** [valor retirado E24] intersecciones en T y [valor retirado E24] esquinas = **[valor retirado E24] de los [valor retirado E24]
extremos** de los walls de banda simple, o sea **una minoría**. Sobre ese subconjunto los studs
adicionales pasan de **[valor retirado E24] a [valor retirado E24] studs**, y confirma el signo ya declarado — el
take-off está **sobre-contado**.

**Lo que NO prueba, y por eso no se aplica:** el resto. La mayoría de los walls
interiores muere contra un wall **exterior**, y los exteriores no son banda simple de
dos faces paralelas (llevan sheathing, polyiso y plaster), igual que los forros de
columna del canopy, los bulkheads, el F #n y el B<n>K #n. El mapa los deja fuera y por eso
marca "libre" un extremo que en obra muere contra algo.

> Un extremo que el mapa no resuelve NO es un extremo libre: es un extremo **desconocido**.
> Convertir "no lo sé" en "+<n> stud de terminación" es inventar en la dirección cómoda.

Recontar todos los studs sobre un mapa que resuelve una minoría de extremos cambiaría un sobre-conteo **conocido**
por una mezcla desconocida. Lo que falta está acotado y escrito: **meter el perímetro
exterior al mapa.** Hasta entonces los trinquetes se quedan donde están y el −<n> va en
Clarifications como lo que es, el piso medido del sobre-conteo.

---

## COBERTURA DE DETALLES: <n> PENDIENTES → <n>

Los <n> detalles de las <n> hojas que el take-off usa quedaron, cada uno, citado por un
cierre o **declarado con su motivo**. Hasta hoy la compuerta contaba 90 "sin abrir" y la
mayoría **sí** se habían mirado: lo que faltaba era declararlo.

> Un detalle mirado y no declarado se ve igual que uno nunca abierto. Eso vacía la
> compuerta en las dos direcciones: no distingue lo que falta de lo que ya se resolvió.

Y el bucket es **nuevo, no `NO_APLICAN`**: muchos de esos <n> sí aplican y respaldan una
cantidad que ya está, o la validan por segunda fuente.

> Declarar un detalle que SÍ aplica como "no aplicable" es mentir en la dirección cómoda:
> la compuerta queda en cero y el documento dice lo contrario de la verdad.

### Lo que el barrido movió


---

## Estado al cierre

`entregar.py` **todo en verde** · <n> sellos rotos · cierres vigentes con sus eslabones
justificados · **todos los detalles
cubiertos**.

Trinquetes bajados hoy: `TOPE_SIN_COTA` **<n> → <n>** · `TOPE_ES_LOG` <n> → **<n>** ·
`TOPE_ES_HANDOFF_XLSX` <n> → **<n>** · `TOPE_VOCAB_DOCS` <n> → **<n>** ·
`TOPE_VOCAB_HANDOFF_XLSX` <n> → **<n>** · `TOPE_VOCAB_HANDOFF` <n> → **<n>**.
Nuevos: `TOPE_CIERRES_MIN` <n> · `TOPE_TAGS_SIN_RENGLON` <n>.
Sin bajar, con su motivo escrito: `TOPE_CRITERIOS` <n> y `TOPE_SIN_UNIFICAR` <n> — esperan el
perímetro exterior en el mapa de adyacencia.
