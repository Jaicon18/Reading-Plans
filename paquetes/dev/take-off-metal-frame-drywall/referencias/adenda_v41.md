# ADENDA v41 — 8-oct-2026 · EL ROOM DE CADA FACE SE VERIFICA, NO SE HEREDA

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

| wall | ubicación decía | faces decían | quién tenía razón | efecto |
|---|---|---|---|---|
| **A1 #4** | "entry from Central Zone" | Corridor 111 / Corridor 111 (face 2) | **las faces** | fiarse de la ubicación habría subido una face a 12.00 ft → **+15 SF que no existen** |
| **A1 #2** | MW01 niche / Calling Cubes 122 | Calling Cubes 122 / **Corridor 111** | **la ubicación** | el nombre, no la cantidad (los dos bands a 8'-6") |
| **A1 #3** | MW01 niche / Calling Cubes 122 | Calling Cubes 122 / **Corridor 111** | **la ubicación** | el nombre, no la cantidad |
| **A1 #7** | Break Room 118 (una sola) | Break Room 118 / **Break Room 118** | **ninguno** | la face ESTE es Cash Window 116, ceiling ACT-4 9'-0" → **faltaban 0.87 SF** |

### Cómo se resolvió cada uno — el método, que es lo reusable

**A1 #4 — la retícula del ceiling cruza el wall.** En A02.01 **no hay ningún wall horizontal**
que cruce la banda x 1134-1224 entre y=1000 y y=1229, y en el RCP **la retícula pasa de largo
sobre el wall**, con un solo tag en esa banda: el `ACT-4 8'-6"` de CORRIDOR 111. El corridor
sigue al norte del wall. Las dos faces son corridor y el sealed estaba bien.

**A1 #2 y #3 — el corridor no llega al nicho.** A02.01 pone el MW01 contra la face OESTE del #2
y el MW07 contra la face SUR del #3, y el corridor queda al oeste del wall vertical de
x=1224-1228, fuera del nicho. Las faces interiores pasan a llamarse **MW01 niche**.
*Pendiente declarado:* el RCP dibuja **tres callouts (1, 2 y 6) justo sobre el nicho**, así que su
ceiling puede tener condición propia; esos detalles no se abrieron.

**A1 #7 — ausencia de wall = continuidad de room.** En la banda y 1324-1356 **no hay ningún wall
vertical entre x=1530.24 y x=1640**, así que el espacio al este del #7 es continuo con el room
tag `CASH WINDOW 116` de x=1739; el room tag `BREAK 118` está en (1533, 1472), al **sur** del
wall A1-6. Y cuadra con el propio A1-6, cuya face norte ya estaba sellada como Cash Window 116.

> **Para saber a qué room da una face: buscar el room tag más cercano EN LÍNEA RECTA sin cruzar
> ningún wall.** Un room tag al otro lado de un wall no es el de esa face, y la ausencia de wall
> entre la face y el tag es la prueba de que sí lo es.

---

## LA COMPUERTA: `verif_caras.py` (paso 12 de 17)

Compara los rooms que nombra la `ubicación` contra los que nombran las `caras`. **No decide quién
tiene razón** — eso exige el plano; lo que hace es impedir que la discrepancia pase inadvertida.

**Cómo se evita que sea ruido**, que es como una compuerta se acaba apagando: sólo se compara
cuando la `ubicación` tiene la forma limpia `<room A> / <room B>`. Se descarta en cuanto el texto
trae coordenadas (`y 1120.68/1128.48`), paréntesis, o una barra dentro de una sigla (`T/STUD`):
ahí la barra no separa rooms. Un primer intento sin ese filtro daba **16 hits de los que 11 eran
artefactos del parser** — habría sido ruido puro.

`test_verif_caras.py` fija los cuatro casos reales **y los falsos positivos que NO debe cazar**,
9 comprobaciones.

---

## EL OTRO HALLAZGO DEL DÍA: A1 #4, `[DERIVADO]` → `[CONFIRMADO]`

El cierre decía *"90.00 pt / 18 = 5.000 ft, **dimensión de diseño limpia**"* — que es otra forma
de decir "el número redondo sugiere que hay una dimensión impresa". La hay: A02.01 imprime
`5'-0"` y sus dos ticks de 45° están en **x=1133.9 y x=1223.9**, exactamente los dos extremos del
wall.

> **Si un length "redondo" te hace pensar que hay una dimensión impresa, búscala y localiza sus
> ticks. O está, y el valor es `[CONFIRMADO]`; o no está, y hay que decirlo. "Dimensión de diseño
> limpia" no es ninguna de las dos.**

Es el caso inverso del A1 #6 (allí el valor venía de píxeles con etiqueta de dimensión; aquí el
valor es la dimensión con etiqueta de derivación). Las dos salen de la misma jerarquía:
**printed dimension > dimension-string sum > pixels**.

**Estado: 17/17 compuertas pasan · 88 sellos OK / 0 rotos · tipo A1 CERRADO, 9 walls, 78.37 LF.**

---
