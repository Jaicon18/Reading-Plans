# ADENDA v26 — 28-sep-2026 · lo que salió de la auditoría adversarial de un proyecto anterior

Estas reglas salieron de auditar un take-off **que ya tenía 73 sellos verificando**. La auditoría encontró **14 hallazgos reales**. El sello prueba que el cierre es COHERENTE consigo mismo; no prueba que sea CORRECTO. Por eso la auditoría es un paso del cierre, no un extra.

## LA AUDITORÍA ADVERSARIAL ES UN PASO DEL CIERRE

Antes de entregar, se audita el propio take-off con el encargo explícito de **ENCONTRAR ERRORES, no de confirmarlo**. Informe en tres bloques, en este orden:

1. **HALLAZGOS CONFIRMADOS** — cada uno con qué wall/line item, qué dice el cierre, qué debería decir, y la **operación numérica que lo prueba**.
2. **SOSPECHAS NO CONFIRMADAS** — con lo que haría falta para probarlas.
3. **LO QUE SE REVISÓ Y ESTÁ BIEN** — lista corta, para que se sepa qué quedó cubierto.

Qué buscar, **por orden de cuánto dinero mueve**:

| # | qué | por qué duele |
|---|---|---|
| 1 | perfil de stud mal clasificado | mueve miles de LF de una columna de compra a otra |
| 2 | doble conteo entre dos cierres que tocan el mismo elemento | se cobra dos veces |
| 3 | line items que no llegan al resumen de compra | material cuantificado que nadie compra |
| 4 | materiales distintos metidos en un mismo renglón | se compra el material equivocado |
| 5 | deducciones aplicadas dos veces | falta board |
| 6 | alturas aplastadas | sobra o falta stud |
| 7 | huecos de la propia compuerta | lo que la compuerta no exige, nadie revisa |

## REGLA — El perfil de stud se lee del PARTITION SCHEDULE, nunca de una tabla propia

Error real: A5 y B2 se cuantificaron con stud de 3-5/8" cuando el schedule de A12.01 los da de **6"** — [valor retirado E24] LF mal clasificados. La tabla de perfiles del generador se había escrito a mano y nadie la volvió a mirar.

**Verificación obligatoria: la aritmética del propio schedule tiene que cerrar.**
`stud + capas de board = WALL THICKNESS`
- 6" + 5/8" + 5/8" = **7 1/4"** ✓
- 3 5/8" + 5/8" + 5/8" = **4 7/8"** ✓

Y el thickness medido en planta lo confirma por tercera vez (dos medidas en planta contra el WALL THICKNESS del schedule). Tres fuentes independientes, o no se usa.

## REGLA — Ninguna line item se cae en silencio: el generador FALLA si sobra una

El generador del Excel enruta cada line item a una columna. **Si aparece una line item que ninguna columna recoge, el libro NO se genera** (aserción de sobrantes, con el número de wall y el nombre de la line item en el mensaje).

Sin eso se perdieron, ya cuantificados y sellados: [valor retirado E24] LF de aberturas enmarcadas, [valor retirado E24] LF de gypsum edge trim, [valor retirado E24] LF de blocking del roof hatch, [valor retirado E24] refuerzos de stud y [valor retirado E24] SF de board W.R.

**Corolario:** toda hoja del libro tiene que estar REFERENCIADA por el resumen de materiales. Una hoja huérfana es material que no se cobra. Se comprueba leyendo las fórmulas del resumen y viendo que mencionen todas las hojas.

## REGLA — Sumar por prefijo, nunca sobrescribir

```python
{k.split(':')[0]: v for k, p in P.items()}   # MAL: sobrescribe
```

Cuando dos renglones comparten prefijo (`BOARD_WR:baño [room A]` y `BOARD_WR:baño [room B]`) se pierde la mitad. Siempre acumular.

## REGLA — Cuando se corrige una cantidad, se corrige el TEXTO el mismo turno

Un texto de operación viejo **no es cosmético: hay herramientas que lo LEEN**.

En un wall la reauditoría bajó el length de [valor retirado E24] a [valor retirado E24] ft y reescaló todos los valores sin tocar las cadenas. El generador del Excel, que reconstruye `L × H` de cada face leyendo la operación, tomó el valor viejo, no cuadró con el SF sellado y **le inventó una deducción de [valor retirado E24] SF a un wall sin openings** — la única deducción fantasma de todas las faces.

**Para corregir un cierre ya sellado:** un script que (a) arregla el texto, (b) **verifica line item por line item que ningún valor numérico cambió**, y (c) recalcula el sello. Nunca editar el JSON a mano: eso rompe el sello sin dejar rastro de qué se tocó.

## REGLA — Doble conteo: se elige UNA fuente y la otra lista sin sumar

Cuando dos cierres tocan el mismo elemento, la fuente que manda es la del **WALL** — ahí es donde el wall se cierra completo. La otra **sigue listándolo**, porque el registro tiene que estar completo, pero lo reporta aparte y no lo suma. **Nunca se borra el registro.**

En un proyecto anterior, [valor retirado E24] penetraciones de MEP estaban en el cierre de su wall (renglón `ABERTURA_MEP_HEAD_SILL` + studs dentro de `STUD`) y otra vez en el cierre del cruce MEP: `FRAMED_OPENING_MEP` bajó de [valor retirado E24] a [valor retirado E24] LF y `REFUERZO_STUD_MEP` de [valor retirado E24] a [valor retirado E24] pz.

**Señal de alarma:** un cierre que excluye HEADER diciendo "este wall no tiene opening" mientras su propio `STUD` suma studs de abertura y lleva renglón de head/sill. Esa contradicción interna es la huella del doble conteo.

## REGLA — Alturas line items: leer los tramos de la operación del cierre

Un wall que cruza un eje de cambio de deck tiene **DOS alturas de stud**, y el cierre ya lo escribe:

> `tramo HI [valor retirado E24] ft: floor([valor retirado E24]/16)+1 = [valor retirado E24] a [valor retirado E24] ft; tramo LOW [valor retirado E24] ft: floor([valor retirado E24]/16)+1 = [valor retirado E24] a [valor retirado E24] ft`

Multiplicar piezas × una sola height lo falsea (en un caso real: [valor retirado E24] contra [valor retirado E24] LF reales). El LF de material se calcula **tramo por tramo**, y los studs adicionales (terminación, jambs, cripples) van a la **height declarada del wall**, no a la mayor de los tramos.

## REGLA — Un material distinto va en su propio renglón de compra

El `5/8" EXTERIOR GYPSUM SHEATHING` de la face interior del parapet **no** es gypsum board interior: es otro material, a otro precio, y además **solo existe del deck al tope**. Iban [valor retirado E24] SF mezclados con el board interior.

**Regla general: si el cierre le puso un label textual distinto, es otro renglón de compra.** El label del plano es el criterio, no el prefijo de la clave.

## REGLA — El track se compra por TAMAÑO

Un solo renglón de "bottom track" que mezcla 1-5/8", 3-5/8" y 6" no sirve para comprar. El track sigue al stud de su wall: se desglosa con un `SUMIFS` sobre la columna de tamaño de stud, y la verificación `(bottom + top) / largo = 2 corridas por hilera` se mantiene por wall.

## REGLA — La dimension impresa dice dónde está el TOPE, no cuánto mide la banda

`5'-0" TO TOP OF FRP` con un cove base de 6" debajo da una banda de FRP de **4'-6"**, no de 5'-0".

Lo que lo prueba es el **ORDEN DE LAYERS del detalle**. En `8/A08.01 RESTROOM FRP/TILE DETAIL`, de arriba abajo:
`PVC EDGE TRIM MOLDING` · `FRP PANEL` · `ADHESIVE` · `PVC EDGE TRIM MOLDING` · `CLEAR SEALANT` · `CERAMIC TILE COVE BASE` · `CERAMIC TILE FLOOR TILE`

El FRP **apoya** sobre el cove base con su propio edge trim y sealant; no corre por detrás. Para el alto de cualquier banda de acabado hay que **restar lo que va debajo**, y el detalle es lo que dice si va encima o por detrás.

## REGLA — Juntas de control: si el set no las rotula, se EXCLUYEN con motivo, nunca se omiten

Barrer el set completo por `CONTROL JOINT` y `EXPANSION JOINT`. Si solo aparecen en la hoja civil de pavimentos y en la leyenda del estuco (`CJ CONTROL JOINT; PAINT TO MATCH STUCCO FINISH COLOR` = Div 09 24 00, del plasterer), entonces **no hay junta de gypsum especificada**. Se declara EXCLUDED con:

1. el barrido citado (dónde se buscó y qué sí apareció),
2. el **contraste** (los detalles SÍ rotulan corner bead, casing bead y shadow molding uno por uno, así que la omisión no es descuido de rotulación),
3. el **RFI con la norma**: ASTM C840 y GA-216 piden junta en paños corridos de más de 30 ft y en ceilings de más de 2,500 SF; si ningún wall ni cielo llega, por norma podría no hacer falta ninguna, y se pide confirmación por escrito antes del award. [ciego-ok]

**`CONTROL_JOINT` es line item OBLIGATORIA de la compuerta.**

## REGLA — Una abertura con sill obliga a su sill track, y la compuerta lo exige

La compuerta verificaba que una door **no** llevara sill, pero no exigía que una abertura **con** sill declarado trajera su `SILL_TRACK`. Faltaba uno (el framed opening de un ducto de 8" con marco cerrado en los cuatro lados por `6/S5.20 WEB PENETRATION`).

`SILL_TRACK` es line item obligatoria; se auto-excluye con motivo preciso **solo** cuando ninguna abertura del wall declara sill.

## REGLA — Cada abertura con SU PROPIO width

El header y el sill se calculan con el **width propio de cada abertura**, nunca con el de la window típica. Error real: `header = n × (<width típico> + 1'-4")` aplicado a una puerta de [valor retirado E24] y a un R.O. de ATM de [valor retirado E24]. La fórmula correcta suma abertura por abertura: `sum(ancho_propio_i + 1'-4")`. Lo mismo para sill y para cripples.

## REGLA — Un hueco de EQUIPO se mide en el detalle del equipo, no en el claro de la planta

El claro grueso que se ve en planta puede ser el **NICHO** (zona engrosada donde se aloja el equipo), no el hueco. Los dos conviven y se parecen: en un proyecto anterior el nicho del ATM drive-up medía [valor retirado E24] y el R.O. sólo **[valor retirado E24]**.

Procedimiento: buscar el detalle de **ELEVACIÓN** del equipo (ahí va el R.O. acotado) y cruzarlo contra el claro en la **face** del wall en planta. Si coinciden, es el hueco; si el claro de planta es mucho mayor, lo que se midió fue el nicho.

**Y un nicho de equipo NO es storefront.** Antes de clasificar un tramo de perímetro como vidrio hay que mirar cómo está DIBUJADO: wall grueso y achurado con el sleeve perforado = wall; banda delgada con studs = storefront.

El detalle del equipo además trae **line items propias que no están en el partition schedule** y hay que repartir por división: `METAL STUD BOX BEAM` (nuestro, y SUSTITUYE al header genérico ahí), `2 1/2" METAL STUD SISTERED` (nuestro), `FURRING ON 5/8" FRT PLYWOOD` (nuestro, el sustrato), `FIBER CEMENT PANEL` (Div 07), `ATM SURROUND` (viene con el equipo — aparece en el PURCHASE ORDER FORM con su número de surround), `(2) LAYERS 3/4" FRT PLYWOOD PLINTH` y el `2X4 / 4X4 FRT FRAMING` (Div 06 rough carpentry), `STEEL BOLLARD` (metales misceláneos).

Si el nicho lleva un sustrato distinto al de la fachada, hay que **RESTAR esa área del renglón general de sheathing** para no cobrarla dos veces — y restar el área **NETA**, porque la fórmula general ya descontó el R.O.

## REGLA — Medir lo no acotado dentro de un detalle: derivar la escala y VALIDARLA primero

Un detalle a 3/4"=1'-0" son **54 pt/ft**; a 1½"=1'-0", **108**; a 3"=1'-0", **216**.

Antes de usar la escala para medir algo NO acotado, hay que **reproducir con ella una dimension IMPRESA del mismo detalle**. Ej. de un proyecto anterior: el R.O. medido (pt ÷ escala del detalle) reprodujo la dimension impresa del R.O. — eso valida la escala; recién entonces se midió la height del nicho, que además coincidía con su dimension impresa. Sin esa validación previa, la medición no es [DERIVADO]: es adivinanza.

## REGLA — Registro de cadenas: los tramos suman el total y los claros salen redondos

Todo eje o fachada se cierra con la **lista de tramos** (de → a, en pt y en ft) que suma **exactamente** el total declarado. Los quiebres se leen de los extremos de las faces de lineweight de wall; los huecos son los **claros entre esas faces**.

**Control:** un claro de abertura tiene que dar cifra redonda — 144.00 pt = 8'-0" de window, 60.00 pt = [valor retirado E24] de door. Si un claro no da redondo, el quiebre está mal leído: no se redondea, se vuelve a leer.

Y las dimensions impresas del perímetro se cruzan contra lo medido (p. ej. la total de face exterior a face exterior y la del paño de storefront, cada una contra pt ÷ escala); la diferencia tiene que quedar en fracciones de pulgada.

## REGLA — El título y la leyenda del plano marcado no se salen del recuadro

El título se **envuelve por palabras** dentro del width del recuadro. Cada entrada de leyenda va en **su propio renglón, con su color real** — dos entradas en el mismo renglón se encabalgan, y una leyenda con el color por defecto no dice nada. Si una entrada no cabe, se recorta con puntos suspensivos. **Reabrir siempre el recuadro ya generado y leerlo antes de entregar la hoja.**

## REGLA — Lo que no se resuelve, se declara; no se inventa

`7/A09.33 TYPICAL CEILING TRANSITION DETAIL` pide una transición vertical de 6" con `3 5/8" METAL STUD KICKER AT 48" O.C.`, board por dos faces, dos corner beads y shadow molding, donde un cielo de gyp muere contra un cielo programado a otra height.

Se corrió una prueba mecánica para separar las aristas que mueren contra wall de las que mueren contra ACT, y **no resuelve** las aristas de los baños (cobertura muy baja en aristas que son claramente wall). Antes que inventar el número, la line item quedó en la lista de pendientes **con lo que costaría por LF** ([valor retirado E24] SF de board, un kicker cada 4 ft, dos runs de corner bead y una de shadow molding) y con el perímetro total de los ceilings ([valor retirado E24] LF) como dimension superior.

Una prueba mecánica que no resuelve no se "ajusta hasta que dé": se declara que no resuelve.

---
