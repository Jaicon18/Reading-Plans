# ADENDA v45 — 10-oct-2026 (tarde)
## Cobertura de detalles a cero, atraso de [CONFIRMADO] a cero, y el mapa de adyacencia

Cuatro frentes cerrados. Dos reglas nuevas, las dos del mismo tipo: **sobre qué se puede
afirmar y sobre qué no.**

---

## REGLA 45.1 — UNA CITA QUE PRUEBA QUE EL MATERIAL VA NO PRUEBA CUÁNTO HAY

El trinquete `TOPE_SIN_COTA` bajó de **20 a 0**. Los 19 campos que se pagaron no eran
diecinueve casos: eran **dos clases**.

**(a) Cuatro `alto_stud` de walls exteriores marcados `[CONFIRMADO]` citando el B.O.D.**
La height del stud es esa ELEVACIÓN menos el datum `T/SLAB 0'-0"`. Es una **resta**. Que
las dos cifras coincidan pasa sólo porque el datum vale cero. Es la regla de la adenda
v42, ya aplicada al A1K, que aquí seguía pendiente.

**(b) Quince cantidades que citaban el detalle que establece el ITEM y no el VALOR** — el
sheathing del canopy, sus TEKS, el corner bead / blocking / trim del soffit, el board W.R.
de los baños. La cita prueba que el material va; el número es una cuenta.

> Una cita que prueba QUE el material va no prueba CUÁNTO hay.
> Es la regla de la v42 —*"un detalle de tipo da la REGLA, no el VALOR"*— aplicada a una
> cantidad en vez de a una height.

**El que queda, declarado en vez de escondido.** `CIELO-70 ACCESS_PANEL = 1 ea` no es una
dimensión: es un **conteo leído directo de la hoja** (se recorrieron los 12 key notes de
A04.01 y el único "2' X 2' LOCKING ACCESS PANEL" cae en el Vestíbulo 100). No hay printed
dimension que citar y tampoco hay operación que escribir, así que bajarlo a `[DERIVADO]`
sería tan falso como dejarlo. Va en `CONTEOS_DIRECTOS` con su motivo, y la regla no se
debilita para nadie más.

---

## REGLA 45.2 — UN EXTREMO QUE EL MAPA NO RESUELVE NO ES UN EXTREMO LIBRE

El mapa de adyacencia —qué wall muere contra cuál— **ya existe**: `bandas_v3.py` +
`adyacencia.py`. Y aun así **no se recontó ni un stud.** Por qué importan las dos cosas:

**El impedimento se levantó.** Las fuentes de geometría que había no pasaban ninguna prueba:
`bandas_por_tipo.json` trae geometrías duplicadas, `inventario.json` resultó tener **cinco**
bandas (todas C1) y `wallgeom.py` lleva su propio letrero de que acierta 1 de 3. Se extrajo
de nuevo del vector de A02.01 **y se escribió la prueba antes de mirar el resultado**: cada
wall sellado tiene un length verificado; si la extracción no los reproduce, no sirve.

- Primera versión: **36%**. No servía.
- El defecto no era la extracción, era la **convención de extremos**. Las dos faces de un
  wall no terminan en el mismo punto: en cada encuentro una sigue y la otra se corta.
  Tomando la **unión** en vez de la intersección: **41 de 47 = 87%**.

> Una fuente de geometría no se usa porque exista: se usa porque PASA una prueba, y la
> prueba se escribe antes de mirar el resultado.

**La dirección, que es lo que 5/S5.20 necesita.** La primera versión sólo detectaba
contacto y salían parejas mutuas ("1 muere contra 14 Y 14 muere contra 1"), que es
imposible. Lo que decide es dónde cae la punta: dentro del tramo del otro = **T** (muere,
y los 2 studs van en el pasante); coincidiendo con su extremo = **esquina** (ninguno pasa
de length).

**Lo que el mapa SÍ prueba, medido:** 9 intersecciones en T y 20 esquinas = **29 de los 94
extremos** de los 47 walls de banda simple, o sea **31%**. Sobre ese subconjunto los studs
adicionales pasan de **141 a 103: −38 studs**, y confirma el signo ya declarado — el
take-off está **sobre-contado**.

**Lo que NO prueba, y por eso no se aplica:** el 69% restante. La mayoría de los walls
interiores muere contra un wall **exterior**, y los 12 exteriores no son banda simple de
dos faces paralelas (llevan sheathing, polyiso y plaster), igual que los 4 forros de
columna del canopy, los 2 bulkhead, el F #40 y el B2K #31. El mapa los deja fuera y por eso
marca "libre" un extremo que en obra muere contra algo.

> Un extremo que el mapa no resuelve NO es un extremo libre: es un extremo **desconocido**.
> Convertir "no lo sé" en "+1 stud de terminación" es inventar en la dirección cómoda.

Recontar 2,690 studs sobre un mapa que resuelve el 31% cambiaría un sobre-conteo **conocido**
por una mezcla desconocida. Lo que falta está acotado y escrito: **meter el perímetro
exterior al mapa.** Hasta entonces los trinquetes se quedan donde están y el −38 va en
Clarifications como lo que es, el piso medido del sobre-conteo.

---

## COBERTURA DE DETALLES: 90 PENDIENTES → 0

Los 203 detalles de las 26 hojas que el take-off usa quedaron, cada uno, citado por un
cierre o **declarado con su motivo**. Hasta hoy la compuerta contaba 90 "sin abrir" y la
mayoría **sí** se habían mirado: lo que faltaba era declararlo.

> Un detalle mirado y no declarado se ve igual que uno nunca abierto. Eso vacía la
> compuerta en las dos direcciones: no distingue lo que falta de lo que ya se resolvió.

Y el bucket es **nuevo, no `NO_APLICAN`**: muchos de esos 90 sí aplican y respaldan una
cantidad que ya está, o la validan por segunda fuente.

> Declarar un detalle que SÍ aplica como "no aplicable" es mentir en la dirección cómoda:
> la compuerta queda en cero y el documento dice lo contrario de la verdad.

### Lo que el barrido movió

| hallazgo | fuente |
|---|---|
| **B2 #26 y #27: FRP de 4.50 → 5.00 ft de banda** (+2.00 SF). Dos criterios convivían para la misma banda del mismo baño: los cierres del 52 y del exterior oeste ya usaban 5.00 | geometría vectorial de A08.01: floor y=1100.16, tope del cove base y=1082.16 (18.00 pt = 6" exactos), tope del FRP y=902.16 → **180.00 pt = 5'-0" exactos** |
| **El FRP va pegado con ADHESIVE directo al board, sin backer** — cierra el RFI del sustrato detrás del FRP | `3/A08.01 RESTROOM FRP/TILE DETAIL`, que lo dibuja y lo rotula |
| `1/A11.03 NER ELEVATION` y `7/A11.03` llevan 3/4" FRT PLYWOOD y **se dejan fuera a propósito** | la corrección del 6-oct dejó escrito que las que corresponden son `3/A11.03` (210.00 pt = 5'-10" exactos) y `5/A11.03` (270.00 pt = [valor retirado E24] exactos), identificadas por **width medido** contra la dimensión impresa de la planta |
| `4/A09.31 DETAIL AT VERTICAL CONTROL JOINT` es un **cuarto** sitio donde aparece CONTROL JOINT, y también es del estuco | la exclusión de proyecto decía "tres sitios"; su conclusión aguanta, su lista de evidencia no estaba completa |

---

## Estado al cierre

`entregar.py` **23/23 en verde** · 88 sellos OK / 0 rotos · 90 cierres vigentes · 67 walls
/ 111 faces / 11 superficies · 1,279 eslabones justificados · **203 de 203 detalles
cubiertos**.

Trinquetes bajados hoy: `TOPE_SIN_COTA` **20 → 0** · `TOPE_ES_LOG` 884 → **877** ·
`TOPE_ES_HANDOFF_XLSX` 34 → **24** · `TOPE_VOCAB_DOCS` 36 → **25** ·
`TOPE_VOCAB_HANDOFF_XLSX` 17 → **0** · `TOPE_VOCAB_HANDOFF` 9 → **8**.
Nuevos: `TOPE_CIERRES_MIN` 88 · `TOPE_TAGS_SIN_RENGLON` 0.
Sin bajar, con su motivo escrito: `TOPE_CRITERIOS` 4 y `TOPE_SIN_UNIFICAR` 10 — esperan el
perímetro exterior en el mapa de adyacencia.
