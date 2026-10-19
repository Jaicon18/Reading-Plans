# ADENDA v<n> — <n>-oct-<n> · EL ROOM DE CADA FACE SE VERIFICA, NO SE HEREDA

## ⛔ REGLA INVIOLABLE

> **El nombre del room en la `ubicación` de un wall NO es la fuente de la height de sus faces.
> La fuente es el ceiling tag de la BANDA en la que cae cada face, y la banda se delimita viendo
> dónde se corta la retícula del RCP y dónde hay un wall que la separe.**

Y su recíproca, que es la que cuesta más:

> **Cuando la `ubicación` y las `caras` no coinciden, ninguno de los dos lados manda por sí solo.
> Hay que ir al plano.**

---

## LOS CUATRO CASOS QUE LA ORIGINARON, el mismo día

Cerrando el tipo A1 salieron cuatro walls seguidos con discrepancia entre `ubicación` y `caras`,
y **la razón la tuvo un lado distinto en cada uno**:


### Cómo se resolvió cada uno — el método, que es lo reusable

**A1 #n — la retícula del ceiling cruza el wall.** En la planta **no hay ningún wall horizontal**
que cruce la banda del wall en su tramo, y en el RCP **la retícula pasa de largo
sobre el wall**, con un solo tag en esa banda: el `[ceiling tag]` de CORRIDOR [room]. El corridor
sigue al norte del wall. Las dos faces son corridor y el sealed estaba bien.

**A1 #n y #n — el corridor no llega al nicho.** La planta pone el MWxx contra la face OESTE del #n
y el MWxx contra la face SUR del #n, y el corridor queda al oeste del wall vertical que
lo cierra, fuera del nicho. Las faces interiores pasan a llamarse **MWxx niche**.
*Pendiente declarado:* el RCP dibuja **tres callouts (<n>, <n> y <n>) justo sobre el nicho**, así que su
ceiling puede tener condición propia; esos detalles no se abrieron.

**A1 #n — ausencia de wall = continuidad de room.** En la banda del wall **no hay ningún wall
vertical entre su face y el room tag**, así que el espacio al este del #n es continuo con el room
tag `[room]`; el room tag `BREAK [room]` está al **sur** del
wall A1 #n. Y cuadra con el propio A1 #n, cuya face norte ya estaba sellada como [room].

> **Para saber a qué room da una face: buscar el room tag más cercano EN LÍNEA RECTA sin cruzar
> ningún wall.** Un room tag al otro lado de un wall no es el de esa face, y la ausencia de wall
> entre la face y el tag es la prueba de que sí lo es.

---

## LA COMPUERTA: `verif_caras.py` (paso 12 de 17)

Compara los rooms que nombra la `ubicación` contra los que nombran las `caras`. **No decide quién
tiene razón** — eso exige el plano; lo que hace es impedir que la discrepancia pase inadvertida.

**Cómo se evita que sea ruido**, que es como una compuerta se acaba apagando: sólo se compara
cuando la `ubicación` tiene la forma limpia `<room A> / <room B>`. Se descarta en cuanto el texto
trae coordenadas (`y <n>/<n>`), paréntesis, o una barra dentro de una sigla (`T/STUD`):
ahí la barra no separa rooms. Un primer intento sin ese filtro daba **muchos hits, casi todos
artefactos del parser** — habría sido ruido puro.

`test_verif_caras.py` fija los cuatro casos reales **y los falsos positivos que NO debe cazar**.

---

## EL OTRO HALLAZGO DEL DÍA: A<n> #n, `[DERIVADO]` → `[CONFIRMADO]`

El cierre decía *"<pt> / <escala> = <length redondo>, **dimensión de diseño limpia**"* — que es otra forma
de decir "el número redondo sugiere que hay una dimensión impresa". La hay: A02.<n> imprime
la dimension y sus dos ticks de <n>° caen **exactamente** en los dos extremos del
wall.

> **Si un length "redondo" te hace pensar que hay una dimensión impresa, búscala y localiza sus
> ticks. O está, y el valor es `[CONFIRMADO]`; o no está, y hay que decirlo. "Dimensión de diseño
> limpia" no es ninguna de las dos.**

Es el caso inverso del A1 #n (allí el valor venía de píxeles con etiqueta de dimensión; aquí el
valor es la dimensión con etiqueta de derivación). Las dos salen de la misma jerarquía:
**printed dimension > dimension-string sum > pixels**.

**Estado: todas las compuertas pasan · <n> sellos rotos · tipo A1 CERRADO.**

---
