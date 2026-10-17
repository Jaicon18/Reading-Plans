# ADENDA v44 — 10-oct-2026
## Barrido de los 95 detalles sin abrir, y el error que cometí en medio

Tres reglas nuevas. Las tres salieron del mismo día y **dos de las tres salieron de un
error mío, no de un hallazgo.** La más importante es la segunda.

---

## REGLA 44.1 — BARRIDO POR TAG DE SCHEDULE, NO POR WALL

Cuando un schedule publica una lista **finita e impresa** de elementos que se montan en
wall —MILLWORK SCHEDULE, FIXTURE SCHEDULE, EQUIPMENT SCHEDULE, TOILET ACCESSORY
SCHEDULE— el blocking se barre **recorriendo esa lista, tag por tag**, preguntando contra
qué wall apoya cada uno. Nunca al revés.

Un barrido wall-por-wall —*"¿hay un tag MW a 42 pt de esta banda?"*— sólo encuentra lo que
cae cerca del wall que uno está cerrando, y hereda todos los errores de la geometría con
la que mide esa cercanía.

**La prueba de que no basta: MWxx.** Los cierres A1K-nn, A1K-nn, A1K-nn y G-nn a G-nn lo
NOMBRAN nueve veces, todas para decir que no apoya en ellos —*"MWxx está contra la face
OESTE del wall exterior, a más de [valor retirado E24] pt al este"*, *"MWxx está a [valor retirado E24] pt = [valor retirado E24] ft de G-nn,
no contra él"*. **Las nueve tienen razón y ninguna lo recoge.** Un huérfano perfecto: cada
wall acierta al decir que no es suyo, y el elemento se cae por la grieta.

**Segunda prueba: MWxx.** El MILLWORK SCHEDULE de A00.30 lo lista UNA vez; 8/A08.01 lo
dibuja DOS veces dentro de JANITOR CLOSET 112. Un tag de schedule es una línea; una
instancia dibujada es otra cosa. **El barrido cuenta instancias, no líneas de schedule.**

> Un schedule es una lista cerrada. Si el take-off no tiene un renglón por cada línea de
> esa lista, el que falta no se ve: no hay nada que lo delate.

**COMPUERTA `verif_blocking_schedule.py`.** Para cada tag de un schedule declarado tiene
que existir una LINE ITEM cuya clave empiece con `BLOCKING` y cuyo **propio texto** nombre
ese tag, una por instancia dibujada; o el tag está en `EXCLUIDOS_PROYECTO` con motivo
escrito. Tope 0.

---

## REGLA 44.2 — UN ROLL-UP POR CLAVE NO ES UN INVENTARIO DE CONTENIDO
### (el error de este día, y el más caro de los tres)

**Qué hice.** A mitad del barrido quise saber si faltaba el blocking de millwork. Hice un
roll-up de las **claves** de line item de los cierres, vi once renglones llamados `BLOCKING`,
ninguno con un tag MW en la clave, y concluí: *"ninguno es de millwork"*. Cuantifiqué
**[valor retirado E24] LF nuevos para [valor retirado E24] unidades** y lo escribí como el hallazgo mayor del barrido.

**Era falso.** Casi todas ya estaban cuantificadas, y con mejor método que el mío:

| MW | ya estaba en | método |
|---|---|---|
| MWxx | A1 #n, A1 #n | free edge + backing del printer cabinet, con el #3 razonando que el gabinete apoya en el #2 |
| MWxx | B #n | standards × height de cada uno |
| MWxx | B #n | standards × height de cada uno |
| MWxx | A5 #n | line item propia `BLOCKING:millwork`, runs × length |
| MWxx, MWxx, MWxx | B2 #n, A1 #n | |
| MWxx | F #n | [valor retirado E24] LF |
| MWxx | A1 #n | |

Mi método era «1 run × length» para todo. El del take-off ya distinguía standards de
cleats de runs. **Habría empeorado el take-off y habría inflado el bid.**

**Dos errores en una sola operación:**

1. **La clave no es el contenido.** `BLOCKING` a secas puede ser blocking de millwork: lo
   dice la OPERACIÓN, no la clave. Es el mismo error que ya había retractado en este
   proyecto con el A5 #n —leer el campo que NOMBRA en vez del que CUANTIFICA— disfrazado
   de otra cosa: ahora era leer la clave en vez del texto.
2. **El roll-up no leía todos los archivos.** Sólo `$TAKEOFF_WORK/*_cierres.json`. Los
   cierres por wall de A1, A5, B, B2, B2K y C1 viven en `/mnt/user-data/outputs/**`. No
   son [valor retirado E24] renglones y [valor retirado E24] LF: son **[valor retirado E24] renglones y [valor retirado E24] LF**.

> Un inventario que no declara su alcance no es un inventario, es una muestra.
> Y una muestra parcial no prueba que algo FALTE: prueba que no estaba donde miré.
>
> Antes de declarar que una line item falta, hay que leer el TEXTO de las que SÍ están,
> en TODOS los archivos de cierre.

**COMPUERTA `corpus.py` + paso 15/23.** Un único lugar donde se pregunta *"¿cuáles son los
cierres?"*, con trinquete: [valor retirado E24] vigentes como mínimo, y sólo puede crecer. Si una
herramienta ve menos, está leyendo un subconjunto y lo que concluya sobre lo que falta no
vale.

**Y una tercera lección, de la primera versión de `corpus.py`.** Al arreglarlo escribí ahí
una lista de globs **nueva**. Mal: ya existía la buena —`resumen_global.SRC` más
`verif_vigencia`— que además distingue los cierres SUPERADOS. Mi lista nueva leía
cierres incluyendo los superados y daba [valor retirado E24] SF de board donde el entregable tiene
[valor retirado E24].

> Crear una segunda fuente de verdad para arreglar un error de alcance
> es volver a cometerlo, con más pasos.

`corpus.py` ahora no declara nada propio: le pregunta a `verif_vigencia.fuentes()`. Lo
único que agrega es la distinción que al roll-up le faltaba, y son **dos preguntas
distintas que nunca hay que confundir**:

```
cierres()            -> los VIGENTES.  Para SUMAR.      Es lo que va al Excel.
cierres(todos=True)  -> todos.         Para COBERTURA.  "¿algún cierre nombra el MWxx?"
```

Sumar con el conjunto de cobertura infla el total. Preguntar cobertura con el conjunto
vigente deja fuera cierres reales. **Las dos equivocaciones se cometieron el mismo día.**

---

## REGLA 44.3 — UNA COMPUERTA NO SE DA POR BUENA HASTA VERLA FALLAR

La primera versión de `verif_blocking_schedule.py` contaba cualquier mención del tag
dentro de una franja de 2500 caracteres que tuviera la palabra `BLOCK`. Con esa regla
**pasaba con el defecto presente**: las exclusiones de los walls G y A1K nombran "MWxx"
para decir que está lejos, y esas frases la satisfacían.

Lo probé borrando el archivo que arreglaba el problema. Dio `tags sin renglón: 0`, `EXIT 0`.

> Una compuerta que pasa con el defecto presente no es una compuerta.
> Antes de confiar en una, hay que BORRAR lo que arregló y verla fallar.

La versión buena recorre la **estructura** del cierre, no texto suelto. Probada: con el
archivo en su lugar, EXIT 0; sin él, rechaza nombrando MWxx y MWxx.

**Esto se aplica a toda compuerta nueva, sin excepción: no se declara su trinquete hasta
haber reintroducido el defecto y haberla visto rechazar.**

---

## Lo que el barrido movió, ya sellado

| concepto | antes | después | fuente |
|---|---|---|---|
| BLOCKING millwork | MWxx huérfano, 1 de 2 MWxx | **+[valor retirado E24] LF** ([valor retirado E24] total) | nota C de A02.01 + SHEET NOTE D de A12.04/05/06 + 8/A08.01 |
| C1 #n length | [valor retirado E24] LF **[CONFIRMADO sin dimension]** | **[valor retirado E24] LF [DERIVADO]**, operación escrita | printed dimensions en A02.01 |
| C1 #n y #39: studs | [valor retirado E24] pz c/u | **[valor retirado E24] pz c/u** (toe-to-toe stud post) | 8/S5.20 MECH. CHASE FRAMING IN WALL |
| ceilings: CORNER_BEAD, PERIMETER_ANGLE, SHADOW_MOLDING, BRACING_SÍSMICO | **sin renglón** (ni cantidad ni exclusión) | exclusiones con motivo verificado + alterno [valor retirado E24] LF | 7/A09.33 y 3/A09.33 |
| C1 board 6" sobre ceiling | supuesto escondido en una operación | exclusión declarada, delta [valor retirado E24] SF | 6/A12.01 contra 2, 3 y 12/A12.01 |
| eje B como línea de zona B.O.D. | [DERIVADO] del par de vigas de S2.20 | confirmado por hoja propia | **9/S5.10 ROOF STEP AT GRID B** |
| A6 y A8 | tipo sin revisar | fuera de alcance, cero tags en A02.01 | barrido de tags |

Y una corrección de Regla #0 que atrapó una compuerta el mismo día: C1 #n se selló
primero como **[valor retirado E24] [CONFIRMADO]**, y ese valor no es ninguna printed dimension: es la SUMA de
tres. `verif_confirmado` lo rechazó. **Una cuenta sobre una printed dimension es [DERIVADO] con
su operación escrita**, aunque cada sumando sea [CONFIRMADO].
