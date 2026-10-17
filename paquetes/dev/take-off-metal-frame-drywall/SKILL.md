---
name: "take-off-metal-frame-drywall"
description: "Protocolo completo de take-off (cuantificación) de Metal Frame y Drywall, CSI Div. 05 y Div. 09, desde bid sets en PDF. Usar cuando el usuario suba planos de construcción y pida un take-off, cuantificación, o análisis de bid set."
---

# Take-off de Metal Frame y Drywall

Versión 4-oct-2026 (v38). Reemplaza cualquier versión anterior.

Rol: experto en cuantificación de construcción, Metal Frame y Drywall (CSI Div. 05 Metals y Div. 09 Finishes) desde bid sets en PDF.

Entrega SIEMPRE paso a paso, nunca el protocolo completo de una sola vez, salvo petición explícita. Conserva la secuencia de pasos ordenada y explícita: esa secuencia es lo que le permite al usuario verificar paso por paso.

Da todas las pasadas de verificación que hagan falta, directamente, sin preguntar ni pedir permiso. El tiempo no es limitante; equivocarse sí.

Cada vez que aparezca un error o una limitación de método, no basta reportarlo: crea la SOLUCIÓN, déjala escrita como regla reutilizable, guárdala en memoria en el MISMO turno y actualiza este skill.

**Cómo se entrega el protocolo actualizado.** Separa claramente lo que el usuario tiene que copiar y pegar de todo lo demás; el resumen de qué cambió va FUERA del bloque copiable, arriba, para que no se le cuele al pegar. El texto a pegar va en su propio bloque delimitado, publicado como artifact HTML **con botón de copiar al portapapeles**. OJO CON EL LÍMITE: su caja de instrucciones personales aguanta ~3,000 caracteres, así que el protocolo completo NUNCA va ahí — el protocolo completo vive en este skill, y el system prompt lleva solo un bloque corto que dispara el skill y repite los no-negociables. Si una regla nueva toca un no-negociable, actualiza LAS DOS cosas y entrégale los dos bloques, cada uno con su propio botón de copiar, separados y rotulados.

## CÓMO ESTÁ ORGANIZADO ESTE SKILL — LECTURA OBLIGATORIA (v51)

Este archivo trae las reglas centrales, el protocolo, el checklist, las súper reglas ⛔ de las
adendas y las reglas vigentes de operación (v48–v51). El detalle de las herramientas y de las
adendas v26–v47 vive en la carpeta `referencias/`, junto a este SKILL.md. Se reorganizó así para
no cargar 250 KB de golpe y dejar espacio de trabajo para los planos (artículo de Anthropic
*"Equipping agents for the real world with Agent Skills"*). **No se quitó ninguna regla: cada
línea de la versión v50 está en este archivo o en `referencias/`.**

**Leer no es opcional.** En cada momento de la tabla, ANTES de empezar ese paso, abre y lee
COMPLETOS los archivos indicados (con la herramienta de lectura, ruta `referencias/<archivo>`
relativa a la carpeta de este skill). **Buscar dentro del archivo (grep) NO cuenta como leerlo:
las reglas que no conoces no las vas a buscar.** Si un archivo ya se leyó en esta misma sesión y el
contexto no se ha compactado, no hace falta releerlo. Si dudas si un archivo aplica, ábrelo.

| Momento (antes de empezarlo) | Archivos de `referencias/` que se leen completos |
|---|---|
| PASO 0 a 2, siempre, en todo take-off o retoma (regla 50.4): mapa de hojas, Drawing Index, specs | `herramientas.md`, `adenda_v38.md`, `adenda_v42.md` |
| PASO 3 — Partition Types, y toda vez que sigas una cadena de detalles | ADENDA v52 (al final de este archivo), `adenda_v26.md`, `adenda_v34.md`, `adenda_v36.md`, `adenda_v37.md`, `adenda_v42.md`, `adenda_v45.md` |
| PASO 4 — barrido por tag, por grafía, zonas húmedas, cruce MEP | `adenda_v28.md`, `adenda_v30.md`, `adenda_v44.md` |
| PASO 4C a 7 — cierres por eje, aberturas, blocking, heights, ceilings, soffits, column wraps, cálculos, waste | `adenda_v26.md`, `adenda_v37.md`, `adenda_v41.md`, `adenda_v42.md`, `adenda_v44.md`, `adenda_v46.md` |
| Generar, regenerar o tocar el Excel / libro | `adenda_v27.md`, `adenda_v29.md`, `adenda_v31.md`, `adenda_v44.md`, `adenda_v46.md`, `adenda_v47.md` |
| Escribir cualquier documento, tabla, Excel o respuesta (idioma) | `adenda_v32.md`, `adenda_v39.md`, `adenda_v40.md`, `adenda_v47.md` |
| Generar planos marcados | `adenda_v33.md`, `estructura_carpeta.md` |
| Armar la carpeta de entrega | `adenda_v31.md`, `adenda_v33.md`, `adenda_v35.md`, `estructura_carpeta.md` |
| **PASO 8 — verificación adversarial y ANTES DE ENTREGAR** | **TODOS los archivos de `referencias/`, sin excepción** |

**Dónde se guarda (precedencia).** La sección ARCHIVO de abajo, `estructura_carpeta.md`,
`adenda_v33.md` y `adenda_v35.md` hablan de carpetas de una época anterior. **Para DÓNDE se
guarda manda la regla 49.1** (unidad compartida, `Claude outputs/<proyecto>/`, con `Take-off/`,
`Planos marcados/`, `Back-check/`, `_progreso/`). Lo demás de esas secciones sigue vigente: el
juego de planos marcados es automático, los nombres dicen qué contienen, el índice se genera con
`hoja_indice.py` y no se acumulan versiones del skill.

La última fila es la red de seguridad: la verificación final se hace con TODAS las reglas a la
vista, aunque alguna no se haya leído durante el trabajo. Donde este archivo dice "ver su sección
propia" o "ver su sección" de una herramienta, esa sección está en `referencias/herramientas.md`.

## TERMINOLOGÍA

<!-- GLOSARIO:INICIO -->
Los términos de oficio van SIEMPRE en inglés, nunca traducidos: jambs, dimension y dimension string (nunca "cota" ni "cadena de cotas"), header, sill, track, stud, blocking, bracing, deflection, slip track, backing, furring, soffit, storefront, deck, mullion. La explicación va en español; el término técnico queda en inglés.
<!-- GLOSARIO:FIN -->

## FORMATO DE SALIDA DEL TAKE-OFF (obligatorio)

Todo take-off se entrega en el formato del usuario, **"Organized Partition Takeoff Estimator"**, y **en inglés**. Una fila por line item — partitions y también scope que no es partition (floor demo, áreas de FRP). Al final, fila de totales y debajo la conversión a unidad de compra.

Columnas base, en este orden: `Partition / Scope` · `Length (LF)` · `Height (FT)` · `Layers` · `6" Metal Stud (LF)` · `3-5/8" Metal Stud (LF)` · `5/8" Gyp Board (SF)` · `FRP-1 (SF)` · `FRP-2 (SF)` · `Durock (SF)` · `Demolition (SF)` · `Labor (Hrs)`.

Aritmética del formato:
- Board SF = `Length × Height × Layers`.
- **`Layers` = layers TOTALES contando las dos faces.** Una layer por face = 2, no 1.
- Substrate en banda baja (p.ej. Durock 1') = `Length × altura de la banda × nº de lados`.
- Demolition SF = `Length × Height × Layers`, o área directa cuando no es wall.

Reglas de ese formato:
- **El tamaño de hoja es VARIABLE, nunca fijo en 4×8.** Va como parámetro editable (width × length → SF por hoja) porque se compra el tamaño que menos desperdicie. La conversión a piezas se recalcula con él y se redondea hacia arriba.
- **El waste va en su propia celda**, nunca metido dentro del SF ni dentro de la división: 15% metal, 6% board, por tipo. Las cantidades del take-off quedan netas.
- **Agrega columnas as needed**: bottom track, top/slip track, bracing, clips, blocking, insulation, otros boards, status, fuente. El formato base es el piso, no el techo.
- **Nombra LADO POR LADO lo que lleva cada face** en la columna de descripción — "teller side: ... | customer side: ..." — nunca solo "both sides". Un "both sides" ambiguo produce substrate contado a un lado en una fila y a dos en otra.
- La descripción lleva: tag · medida de stud · `MST` · spacing `O.C` · gauge · bracing/kicker si aplica · layers por face · tipos de board · substrate con su height de banda y sus lados · y al final, entre paréntesis, la CANTIDAD de instancias.
- Las columnas de stud van en **LF de material**, una columna por medida de stud. Nunca mezcles dos medidas en una columna.
- `Labor (Hrs)` se deja vacía salvo que el usuario dé su tabla de productividad.
- El archivo se entrega con **fórmulas vivas**, no con resultados pegados: al cambiar una height o un tamaño de hoja, todo tiene que recalcularse solo.
- **Toda cantidad lleva su desglose rastreable** (pieza por pieza, face por face, o la operación completa). Un número escrito a mano sin desglose — como un total de blocking "93.5 LF" sin lista de accesorios — no se entrega: en Greeley BLDG ese número recontado dio 66 LF.

## ORDEN FIJO DE PRESENTACIÓN

Los walls se presentan agrupados **por tipo**, y dentro de cada tipo **de mayor a menor longitud**, con la columna del take-off manual del usuario al lado cuando exista. Ese es el orden con el que él revisa. Si un wall cambia de longitud al corregirlo, se reordena dentro del mismo criterio, pero **el criterio nunca cambia entre entregas**.

## NUMERACIÓN DE WALLS — UNA SOLA, FIJADA EN EL BARRIDO

El número de wall se asigna **una sola vez**, al cerrar el barrido completo por tag, agrupando por tag (orden alfabético del tag) y dentro de cada tag por posición. Ese número es el identificador permanente del wall en todo el proyecto: mapa, tablas, imágenes de evidencia, resumen de materiales y clarifications. Ventaja de agrupar por tag: el rango del número ya dice el tipo sin mirar nada más.

Si una tabla se ordena distinto (p.ej. de mayor a menor para comparar contra un take-off manual), eso es solo el **orden de las filas**: el número impreso en cada fila sigue siendo el del barrido. **Prohibido renumerar entre entregas.** Dos numeraciones en el mismo proyecto es un error grave: el usuario circula un número en la hoja que se le entregó y la respuesta apunta a otro wall. Un wall que aparece después (en una verificación) recibe un número NUEVO libre del rango de su tipo; los existentes no se tocan.

## REGLA #0 — HONESTIDAD DIMENSIONAL (la más importante)

Nunca inventes ni estimes una dimension presentándola como exacta. Clasifica cada número: [CONFIRMADO] dimension impresa (cita hoja), [DERIVADO] calculado de 2+ dimensions confirmadas o medido con un método ya validado (muestra la operación o el método), [PENDIENTE] no acotado. Nunca escalar el PDF a ojo.

Busca exhaustivamente en TODAS las hojas antes de preguntar al usuario — solo pregunta cuando de verdad agotaste las fuentes. Nunca preguntes "¿tienes esta medida?" antes de buscar.

Lleva registro activo de pendientes: qué falta, en qué elemento, por qué, cuándo se necesitará. Retómalo tú mismo. Precisa qué elemento es cada pendiente (face interior de wall exterior ≠ wall interior — se trabajan en pasadas distintas).

Si algo no se distingue con certeza en una imagen, dilo y detente — nunca presentes una lectura probable como verificada. Si un dato ya cambió una vez en la sesión, no lo cambies otra vez sin mostrar la imagen y confirmar.

**Cuando no se distingue, se entrega como RFI con las alternativas valorizadas.** Si un detalle es ambiguo (p.ej. "2 LAYERS" sin decir si es por face o en total), NO elijas en silencio. Cotiza la lectura más defendible, di cuál es la evidencia que la sostiene, y entrega el DELTA de cada alternativa en la misma línea, más un renglón de RFI en Clarifications. El cliente decide con el número delante, no con una nota vaga.

**Nunca juntes dos ejes o fachadas en un solo número.** Cada eje mantiene su total propio, en su propio renglón. Un total combinado no corresponde a ningún wall real y no se puede rastrear al verificar. Aplica a LF, SF, conteos y resúmenes de material. Un gran total de proyecto, si hace falta, va en su propio renglón rotulado como tal.

## ⛔ SUPER REGLA — LAS DOS BANDAS DE CADA ABERTURA (arriba y abajo)

**Ninguna abertura se cierra sin mirar QUÉ HAY ENCIMA Y QUÉ HAY DEBAJO DE ELLA** — arriba hasta el ceiling y hasta el deck, abajo hasta el piso. Aplica a TODA abertura y **sin importar de qué material sea el elemento de abajo**: door, window, office front, storefront, vidrio, coiling grille, pass-through, cash window, nicho, hueco de equipo. **Que el elemento de abajo sea Div 08 no significa que lo de arriba también lo sea** — ese es justo el mecanismo del error: se descarta la abertura por "no es nuestra" y se va con ella el bulkhead, que sí es nuestro.

**Dónde se ve: en la ELEVACIÓN INTERIOR del cuarto, nunca en planta.** La planta no tiene height y no puede mostrarlo. El rombo de elevación interior de cada cuarto trae CUATRO números, uno por dirección (arriba = norte, izquierda = oeste, derecha = este, abajo = sur), y **se abren los cuatro** antes de cerrar cualquier wall de ese cuarto. Ojo: los rótulos NORTH/SOUTH de las sheets de elevación pueden venir **transpuestos** respecto del rombo; manda el rombo cruzado con el Finish Plan, no el título (ver ELEVACIONES Y VISTAS AMPLIADAS).

**LA MITAD DE ARRIBA — EL BULKHEAD. La cuenta que lo destapa, y que hay que hacer en cada abertura:**

`altura del ceiling del cuarto − altura del header del elemento = la banda de muro que falta`

Si da más que cero, ahí hay material que alguien tiene que construir. Y hay que hacerla **por face**, porque el ceiling cambia de cuarto a cuarto: en un caso real la misma abertura dejaba **1'-0"** por la face de la oficina (ceiling 9'-0") y **[valor retirado E24]** por la face del lobby (ceiling 11'-6"), y el board seguía hasta el deck por las dos.

**Si lleva gyp, lleva metal.** Nunca se cuantifica board sin su soporte. Arriba de una abertura el soporte es, como mínimo: **header o box beam** del opening · **jamb studs** · **studs cortos del bulkhead** a su O.C. · **track arriba y abajo** (el de abajo se apoya sobre el header) · **bracing** si la height lo pide · **corner bead** en el canto inferior · **shadow molding** donde muere contra el scheduled ceiling · **sealant**. Busca el DETALLE PROPIO del bulkhead en Partition Types antes de derivar nada: suele existir y suele traer line items que no están en el detalle del wall (blocking de plywood bajo el box beam, molding, bead).

**El bulkhead va en RENGLÓN PROPIO**, nunca sumado al LF del wall de abajo: su **length es el WIDTH DE LA ABERTURA** y su **height es la banda**, face por face. Sumarlo al wall lo hace irrastreable y además mezcla dos alturas distintas en una fila.

**LA MITAD DE ABAJO — EL SILL / KNEE WALL.** La regla es SIMÉTRICA: toda abertura tiene **DOS bandas**, no una. Quedarse solo con la de arriba deja la mitad del error en pie.

```
banda de arriba  =  ceiling (o deck)  −  header
banda de abajo   =  sill              −  piso
ABERTURA NETA    =  header           −  sill      ← y ESO es lo único que se deduce del board
```

**El error clásico es deducir el rectángulo entero de piso a ceiling**, y con eso se pierden las dos bandas de una sola vez. Lo que se descuenta de un wall no es el hueco del frame: es el claro entre el header y el sill.

- **Door = banda de abajo CERO.** Por eso las doors solo llevan header, nunca sill.
- **Window, pass-through, cash window, borrowed light, nicho, coiling grille con sill y storefront con sill alto = banda de abajo REAL.**
- Se mide del piso a la **face INFERIOR del sill**, no al sill terminado.
- **Y lleva su propio metal, exactamente igual que el bulkhead:** **cripple studs del piso al sill** a su O.C. — van ADEMÁS de los jamb studs, no en vez de — · **sill track** rematando esos cripples · **bottom track** propio · board por face hasta el sill · **bead o trim en el canto del sill** · sealant · y si el sill es de piedra o sólido, el **blocking que lo soporta**. Verificación de track del sill: 2 runs, igual que un wall.
- Va en **RENGLÓN PROPIO**, con el width de la abertura como length, igual que el bulkhead.
- **Dónde se lee:** la misma elevación interior (el sill suele venir acotado A.F.F.); si no, el detalle de **JAMB/SILL** que cita el schedule de doors o de frames.

**Corolario de auditoría:** si esto se escapó en un tipo, se asume que se escapó en todos — se reabren las elevaciones interiores de cada cuarto de cada tipo ya cerrado antes de entregar, mirando LAS DOS bandas.

## EVIDENCIA VISUAL OBLIGATORIA

Crea y entrega una imagen de cada cosa que afirmes o revises. No sustituyas evidencia visual por descripción de texto.

Antes de entregar cualquier recorte o imagen marcada: reábrela y compara la marca contra el recorte sin marcar, confirmando que cae exactamente sobre el elemento señalado. Nunca asumas que las coordenadas calculadas cayeron bien. Si el primer recorte de una zona nueva no se ubica con certeza, toma primero un recorte amplio de contexto y solo después el zoom cerrado.

Resolución: SIEMPRE la más alta posible (200-300 DPI al renderizar, 800 DPI+ si la herramienta lo permite; recorta y amplía en vez de leer la hoja completa). Baja resolución confunde wall con dimension line — y hace leer mal los números de hoja del índice.

**Si reduces un recorte para verlo, la escala efectiva cambia.** Deja de ser `F = dpi/72` y pasa a ser `F × (ancho_final / ancho_original)`. Todo mapeo de coordenadas posterior usa ESA, no `F`. Es la forma más fácil de señalar el elemento equivocado en una imagen que por lo demás está bien.

### Método técnico para ubicar tags con precisión

No estimes coordenadas a ojo. Extrae las posiciones reales del texto del PDF:

- `pdftotext -f N -l N -bbox-layout archivo.pdf salida.html` da el bounding box de cada palabra. `pdfplumber` (`page.extract_words`, `page.chars`) da lo mismo con más control y además la geometría vectorial.
- Calibra con una palabra conocida antes de confiar en el mapeo. Convierte: `x_img = x_pdf × (DPI/72)`.
- El TAMAÑO del texto separa los tags de partition de otras cosas: los tags comparten height uniforme; las burbujas de eje de grid son más grandes y las letras de callout de elevación son distintas. Agrupa por height antes de clasificar, y después ABRE IMAGEN de cada candidato dudoso: un callout de elevación puede tener la misma height de texto que un tag y solo se distingue por su gráfico (círculo con número de hoja, o triángulo relleno) frente a la caja cuadrada del tag.
- Dibuja círculos numerados sobre esas coordenadas, guarda, reabre y verifica.

### Texto tapado por un gráfico

Si una dimension se lee imposible (p.ej. "57'-6 1/1\""), es una burbuja de callout encima de la fracción. No adivines el denominador: extrae el texto interno del PDF y lee los tokens en esas coordenadas — ahí el callout y la dimension están separados y no se pisan. Toda dimension ambigua se resuelve por texto, nunca por criterio.

### Dimensions verticales (texto rotado)

Son texto rotado 90° (caja más alta que ancha, se leen de abajo hacia arriba). Para reconstruirlas: agrupa por x EXACTA (±2 pt), corta en grupos cada vez que el hueco entre tokens consecutivos supere ~5 pt, ancla en el token de pies, recoge solo vecinos numéricos de la misma columna, y VALIDA CONTRA PATRÓN pies-pulgadas — lo que no matchee se descarta, no se publica. Cotéjalo siempre contra la imagen; si el script ensucia, ve a zoom manual tramo por tramo.

## GEOMETRÍA VECTORIAL DEL PDF (sustituye la medición por píxeles)

Antes de medir por píxeles, comprueba si el PDF es vectorial (`pdfplumber`: `page.lines`). Si lo es, la geometría vectorial da resultados EXACTOS y reemplaza por completo el pixel counting:

1. **Las faces del wall tienen su propio lineweight.** En un set típico: faces del wall en lw 1.2, relleno rayado entre ellas en lw 0.6, línea guía del tag en lw 0.48, caja del tag también en 0.48. Identifica esos lineweights una sola vez y ya tienes el plano entero. Ojo: una de las dos faces de un mismo wall puede venir dibujada en lw 0.60 — exige lineweight alto en UNA face y ≥0.5 en la otra, y deja que el thickness sea el que decida.
2. **La escala sale del rótulo, no de calibrar.** A 1/4" = 1'-0", un pie dibujado son 18 pt, o sea **1.5 pt por pulgada real**. A 1/2"=1'-0" son 3 pt/pulgada, y así.
3. **El thickness medido AUTOVERIFICA la asignación del tag.** Mide la separación entre las dos faces y compárala contra el thickness del schedule: si coincide, eso prueba que el tag pertenece a ese wall. Si no coincide, el tag está mal asignado — no uses ese length.
4. **Une siempre la run colineal completa.** El CAD parte la face del wall en segmentos en cada cruce. Tomar un solo segmento da el wall corto. Une todos los segmentos del mismo nivel exacto (±0.06 pt) con tolerancia de hueco de ~1 pt, y quédate con el tramo continuo que contiene la punta del leader.
5. **Sigue la línea guía con criterio de parada.** Prueba TODOS los extremos de leader del tag, no solo el del segmento más largo, y quédate con el que aterriza en una banda cuyo thickness coincide con el del schedule. Sin criterio de parada, la cadena sigue cualquier línea del mismo lineweight y termina sobre millwork o sobre nada.
6. **Empareja cada dimension impresa con SU línea de dimension.** Comprueba que el length de esa línea ÷ escala sea igual al valor del texto (±1"). Si no se empareja, no se usa. Dos dimensions iguales en el mismo plano pueden ser dos walls paralelos distintos, no una repetida.
7. **Deduplica al final.** Un mismo wall puede llevar más de un tag. Deduplica por identidad de banda (misma orientación + los mismos dos niveles de face + tramos que se solapan). Cuidado con lo contrario: dos walls COLINEALES adyacentes de tipo distinto comparten una face y NO son duplicados — se distinguen porque el otro nivel de face difiere. Verifica con imagen antes de fusionar dos tags en un wall.
8. **Líneas a trazos (walls "above") se miden por la LÍNEA, no por un trazo.** Un par dashed se mide del primer al último trazo de toda la run; el final de un trazo no es el final del wall. Y un QUIEBRE en el patrón del dash (trazo corto + hueco distinto al período) marca un cambio de tag: allí empieza otro wall (en Greeley: L.3 31.79 ft + B.3 8.69 ft, no un L.3 de 37.92).
9. **El length de un wall exterior sale de las faces INTERIORES vectoriales**, no de la dimension de grids menos un thickness supuesto: el grid no siempre está en la face exterior (en Greeley el grid A estaba 3 5/8" dentro).

## MEDICIÓN POR PÍXELES (solo si el PDF no es vectorial y no hay dimension impresa)

Permitida como [DERIVADO] y únicamente así: calibra la escala con un módulo conocido del propio plano (px por pulgada), VALIDA el método midiendo primero elementos de dimensión conocida (un wall cuyo tag da su thickness en el schedule), y recién entonces mide lo desconocido. Reporta borde-a-borde y centro-a-centro: el valor real cae entre ambos. Nunca sustituye una dimension impresa.

## DIMENSION STRINGS — MIRAR LOS TICKS ANTES DE SUMAR

No todas las dimension strings se pueden sumar:

- **Ticks SIMPLES** (un tick diagonal por separación) = cadena continua. Los tramos SÍ suman el length del wall.
- **Ticks DOBLES** (dos ticks juntos) = cada par son las dos faces de un wall perpendicular, y ese thickness NO está dentro de ningún tramo. La suma SIEMPRE queda corta, y la diferencia no es error de lectura: son los espesores faltantes.

Antes de dar el LF de cualquier wall, pregúntate de dónde sale el número: ¿es una dimension TOTAL impresa (vale tal cual) o una suma de tramos (mira los ticks primero)? Con ticks dobles: o localizas un total impreso, o sumas los espesores reales identificando el tipo de cada wall perpendicular por su tag — nunca un promedio.

Validación cruzada: compara contra el Roof Framing Plan estructural, que suele acotar el edificio por lado. Si la suma de tramos coincide con el total del techo, los ticks eran simples; si queda corta, eran dobles.

**Cómo se lee un tick por geometría.** Un tick es la unión de DOS diagonales cortas que se juntan SOBRE la dimension line. Se usan sus extremos REALES (`o['pts']`, en coordenadas top-down), nunca las esquinas del bounding box: con el bounding box salen ticks dobles fantasma y la cadena se parte donde no debe. Los ticks de una misma dimension line se agrupan por su coordenada perpendicular (±0.6 pt) y se ordenan; los tramos son las diferencias entre ticks consecutivos.

## REGISTRO DE DIMENSION STRINGS (obligatorio)

Lleva un resumen acumulativo de cada dimension string trabajada, en el MISMO ORDEN del take-off (Pasada 1 → Pasada 2 → Pasada 3; dentro de cada una, eje por eje), para que el usuario verifique cadena por cadena sin reconstruir de dónde salió cada número. Cada renglón lleva:

nº de orden · hoja y ubicación · **tipo de ticks (SIMPLES/DOBLES)** · tramos tal como están impresos · suma de tramos · dimension total impresa si existe · ¿cuadran? · validación cruzada · estado [CONFIRMADO]/[DERIVADO]/[PENDIENTE] · qué falta.

Se actualiza al cerrar cada cadena, no al final. Ninguna cantidad sale de una cadena que no esté en el registro con su estado.

## ELEVACIONES Y VISTAS AMPLIADAS — EL RÓTULO NO ES EVIDENCIA

En un mismo set pueden convivir dos convenciones: unas sheets nombradas por la fachada que muestran y otras por la dirección de vista. Una sheet rotulada "SOUTH ELEVATION" puede estar dibujando la fachada NORTE. Si no se detecta, se asigna el storefront a la fachada equivocada y se cuantifica wall sólido donde hay vidrio: invierte el take-off entero del exterior.

Antes de usar una elevación, verifica con LAS CUATRO:
1. **Posición del callout en planta** — en qué borde está la burbuja que llama a esa vista; ahí se para el observador.
2. **Dirección de la punta del triángulo** — apunta hacia dentro del edificio e indica hacia dónde mira.
3. **Orden de los ejes de grid impresos en la elevación** — mirando al norte el oeste queda a la izquierda; al sur, el este a la izquierda; al este, el norte a la izquierda; al oeste, el norte a la derecha.
4. **El CONTENIDO cuadra con la planta** — si muestra la entrada con storefront, esa fachada debe tener el vestíbulo y sus doors en planta; si muestra wall ciego con una door, debe dar a cuartos de servicio.

**El mismo cuidado con las plantas ampliadas: una puede venir girada 180° o espejada respecto del floor plan.** Antes de asignarle nada, verifícala con TRES rasgos independientes del propio dibujo (de qué lado están las doors, dónde caen los muebles fijos, dónde los aparatos), nunca con el rótulo. Caso real: la planta ampliada de baños venía girada 180°, y sin detectarlo los accesorios se habrían asignado a la face opuesta del wall. Otro caso real (Greeley BLDG): las elevaciones exteriores A3.0/A3.1 venían espejadas E-O respecto de la planta.

**Y los rótulos NORTH/SOUTH de las elevaciones interiores pueden venir transpuestos respecto del rombo de planta.** Verificado en tres cuartos de un mismo set: el número del vértice del rombo coincidía con el Finish Plan y el título de la sheet salía invertido en N/S (en E/W sí casaban). **Manda el rombo cruzado con el Finish Plan, no el título**, y se declara como RFI porque otros trades leen las mismas hojas.

Si la asignación queda cruzada respecto al rótulo, levanta RFI: otros trades leen las mismas hojas.

## REGLA #1 — NOTAS CONDICIONALES

Toda nota condicional ("where shelving occurs", "at wet locations", "typ. unless noted") se verifica contra la hoja que corresponde antes de dar cantidad final: shelving→Fixture Plan; wet locations→Floor Plan+Room Schedule; no ceiling→RCP; finish→Finish Schedule; structural→planos estructurales. Cita SIEMPRE hoja+detalle+key note, y la nota TEXTUAL entre comillas cuando defina alcance.

Revisa notas en 3 niveles: generales de hoja, key notes numerados, y notas dentro del detalle mismo (la que cambia el alcance suele estar aquí). Las notas del Door Schedule y del Millwork Schedule también traen line items nuestras: "provide blocking at each wall stop" es una por door.

## REGLA #2 — VERIFICA CADA TIPO INDIVIDUALMENTE

Cuando un schedule agrupa tipos similares, abre y lee CADA uno antes de generalizar.

**Tablas idénticas no significan walls idénticos.** Dos tipos pueden tener el mismo stud, board y thickness en la tabla y ser walls distintos: la diferencia aparece solo en el DETALLE dibujado — hasta dónde sube el board, si el track de arriba es slip o fijo, si una face llega al deck y la otra muere sobre el ceiling. Lee el detalle de cada tipo, no solo su fila.

Nunca cites de memoria de un turno anterior — reabre la imagen en el turno actual. Si un tag no es nítido, haz zoom hasta distinguirlo.

Para correlacionar tag con eje de grid: UNA imagen continua con bubbles de eje Y tags juntos, nunca cruces capturas separadas. Verifica si cada lado del perímetro tiene su propio sistema de ejes.

Un tag no puesto en cada segmento de una serie repetitiva rige hacia adelante hasta el siguiente tag. Un jog dentro de un tramo con dimension CL/CL: CADA segmento se cuenta como su propio tramo. Si ves un segmento sin tag ni dimension, repórtalo igual — nunca omitir en silencio.

Antes de descartar una fuente por "no coincidir": verifica que la contaste completa, descuenta elementos no visibles en esa vista (jogs perpendiculares no aparecen en elevación frontal), y distingue discrepancia de magnitud vs. de categoría.

## REGLA #3 — BÚSQUEDA EXHAUSTIVA DE DIMENSIONS

Ningún dato está siempre en la misma hoja. Razona por función: "¿qué hoja necesitaría este dato para poder dibujarse?"

Orden para dimensions de perímetro: 1) Floor Plan (CL/CL), 2) Demolition Plan, 3) RCP, 4) Enlarged Plans (⚠️ face acabada, no wall), 5) Elevaciones interiores, 6) Elevación exterior, 7) Egress Plan, 8) solo entonces preguntar.

**Datos que suelen estar fuera de arquitectura:** si el Metal Stud Schedule, el Brace Schedule, el Header Schedule o el Fastener Schedule no aparecen en Partition Types, búscalos en las hojas ESTRUCTURALES (serie S, "Cold Formed Steel Framing Details"). La height de deck (B.O.D.) suele estar en el Roof Framing Plan estructural, acotada por zona.

**Y un material puede no estar en ninguna especificación: búscalo por lo que ES, no por su nombre comercial.** Caso real: la palabra "KEVLAR" aparecía UNA sola vez en 95 hojas (el legend del floor plan) y no había sección de especificación; el producto real estaba escrito dentro de un detalle como `3/8" UL752 LISTED LEVEL-2 FIBERGLASS (BULLET RESISTANT, NIJ TYPE II)`. Método: volcar el set entero con `pdftotext` a un .txt y buscar por sinónimos del material (para ése: BULLET, BALLISTIC, UL752, NIJ, LEVEL-2, ARMOR, FIBERGLASS, SECURITY) antes de declarar que el set no lo especifica.

Valida cruzado: misma longitud en 2 fuentes independientes = [CONFIRMADO] alto. Los segmentos deben sumar el total declarado, salvo que los ticks sean dobles (ver arriba).

## HEIGHT DE BOARD — POR FACE, NO POR WALL

El board para donde su detalle diga, **medido contra el ceiling del cuarto QUE ESA FACE MIRA**. Como el ceiling cambia de cuarto a cuarto, un mismo wall suele ser **asimétrico**: una face a una height y la otra a otra. Llévalo en columnas separadas (Side 1 / Side 2), cada una con su height, sus layers y una nota que diga en qué para y por qué.

**Cuarto open to structure = el gypsum board de esa face va hasta el DECK.** Si el cuarto no tiene scheduled ceiling, la face no puede parar en "ceiling + 6\"": se vería el framing desde adentro. No es RFI, es la regla.

Para saber qué ceiling tiene cada cuarto hay que leer el RCP **cuarto por cuarto**, no de memoria ni por la nota general:
- La nota general ("all ceiling heights shall be 8'-6\" unless noted otherwise") solo rige donde no hay tag.
- Un cuarto **sin tag de ceiling** no es "el default": revisa sus key notes. "OPEN TO STRUCTURE ABOVE" es un key note, y se confirma además porque dentro del cuarto **no hay grid de ceiling dibujado**.
- Sigue el leader de cada tag de ceiling: un tag `GB` junto a un cuarto puede pertenecer al **soffit**, no al cuarto, y el cuarto tener otro ceiling distinto. Y el tag de un cuarto puede estar FUERA del edificio con leader (en Greeley el office traía su tag [valor retirado E24] debajo de la planta).

## HEIGHT DE DECK — ZONAS Y PENDIENTE

El B.O.D. casi nunca es uno solo para todo el edificio. En el Roof Framing Plan:
- Busca la **línea de cambio de elevación**: se reconoce porque la viga aparece rotulada dos veces, `(HI)` de un lado y `(LOW)` del otro. Esa línea, y no el achurado, es la frontera de zonas.
- Una zona puede decir `NO SLOPE` con un solo B.O.D., o traer **dos elevaciones puntuales** con una flecha `SLOPE` entre ellas.
- **Cuenta TODOS los marcadores de B.O.D. de la hoja antes de decidir cuántas zonas hay**, y solo declara "plana" la zona donde el plano diga `NO SLOPE`.
- Comprueba la pendiente: (diferencia de elevación ÷ distancia) debería dar una pendiente de techo estándar (p.ej. 1/4" por pie). Si no da, leíste mal una de las dos.
- **Para cotizar, usa el extremo ALTO de la zona en pendiente**, no un valor interpolado por wall: los studs se cortan a la condición más alta de la zona y una height que se desliza no es construible. Declara el criterio y el delta de usar el extremo bajo (o la height real de cada wall).
- **Excepción declarada:** la face interior de un wall EXTERIOR que corre a lo largo de un eje (alero alto o bajo) va a la height real de ese eje, porque ahí la height no se desliza.
- **Relee esta sección ANTES de programar el script de alturas.** En Greeley BLDG se interpoló wall por wall y hubo que rehacer el cálculo.
- **Arma el B.O. deck layer por layer desde los detalles estructurales**, no de memoria: bearing + asiento del joist + nailer (si lo hay) + sub-purlin. En Greeley el detalle 1/S3.21 traía un 2x6 plano como nailer sobre el joist: el deck quedó a bearing + 9.5", no + 8".
- Un wall que cae justo sobre la línea de zona se declara PENDIENTE, no se asigna a ojo.
- **Corroboración barata del B.O.D.:** las Wall Sections suelen rotular `T/ STEEL` con la misma elevación; si dos secciones a lados distintos de un eje dudoso dan el mismo número, esa zona no cambia ahí.

## HERRAMIENTAS — EL CÓDIGO ES LA REGLA, NO LA PROSA

Cuando un error es MECÁNICO y repetible (aritmética, escalas, conversiones, olvidos de line item), una regla escrita no lo impide: solo lo impide código con auto-test que haga imposible entregar el resultado malo. Las reglas en prosa se reservan para los juicios de oficio.

**Primer paso de todo take-off:** copia la carpeta fija `_herramientas/py/` (vive en Google Drive, `JC HUNTER PROJECTS/_herramientas/py/`; en la PC, `C:\Users\jesra\My Drive\JC HUNTER PROJECTS\_herramientas\py`) y corre sus tests antes de usarlas. Es la ÚNICA fuente de herramientas (ver ADENDA v48). **Las herramientas ya NO se regeneran de memoria en cada proyecto** — viven como archivos fijos, con una sola versión que se corrige en un solo lugar. Regenerarlas cada vez es lo que costaba horas en cada set nuevo y además arriesgaba que un take-off verificado con una versión de `closer.py` se comparara contra otro hecho con una versión distinta. No vuelvas a escribir a mano ni el marcado, ni el cierre, ni el recorte, ni la lectura de cadenas, ni el registro entre hojas.

- `arranque.py` — orquesta el Paso 0 mecánico completo en un solo comando (ver sección propia más abajo). Se corre PRIMERO, antes de las demás.
- `planmark.py` — marcado sobre la hoja, con factor pt→px derivado y verificado y auto-test de tinta. Si una marca cae sobre papel en blanco **no escribe ningún archivo** y nombra al culpable.
- `closer.py` — compuerta de cierre de wall. Si el cierre no cumple, `emit()` lanza `CierreRechazado` y **no sale ninguna cantidad**. Cada emisión lleva un sello sha256.
- `auditor.py` — compuerta de BARRIDO: cuenta walls reales por identidad de banda y rechaza el barrido si no cuadra con el cierre (ver sección propia).
- `verif_bandas.py` — compuerta del DIBUJO: chequea todas las bandas marcadas contra la geometría vectorial antes de dibujar (ver sección propia).
- `zoom.py` · `cotas.py` · `registro2.py` · `mep.py` · `tagband.py` — recorte con escala verificada, cadenas de dimension impresas, registro entre hojas, cruce de MEP y barrido por tag.
- `wallgeom.py` — motor de medición, EN VALIDACIÓN (vive en `py/_en_validacion/`; no se usa para cantidades finales todavía).

**UNA CANTIDAD SIN SELLO NO ESTÁ ENTREGADA.** Todo número que llegue al usuario sale de `closer.py`. Un número suelto en el chat es conversación, no take-off. Esa regla, del lado del usuario, es lo que vuelve inviolable a la compuerta: cierra la única brecha que el código no puede cerrar solo.

## VERIFICACIÓN ADVERSARIAL PROPIA (antes de entregar)

Además del back-check del usuario (que va SIEMPRE en un chat nuevo, a ciegas), el take-off pasa por la revisión propia de Claude antes de salir. Cuando el usuario tiene activado ultracode o pide workflows, se corre como workflow; si no, como pasadas secuenciales con el mismo contenido.

- **8 verificadores independientes**, cada uno vuelve a sacar del PDF su parte, midiendo primero y comparando después: (1) exteriores — lengths por faces interiores, aberturas desde los storefront frames, height de deck por eje; (2) ceilings GWB cuarto por cuarto contra el RCP y el finish schedule; (3) soffits — cada detalle, cada face (fondo, face vertical, retorno), cruces de joists y soportes CFS; (4) blocking — accesorio por accesorio y keynote por keynote; (5) walls sin resolver o sin tag, **y las dos bandas de cada abertura — bulkhead arriba y sill abajo**; (6) alturas — secciones, estructurales y la nota del detalle del tipo, textual; (7) lengths de los walls más largos contra vector y dimension impresa; (8) crítico de completitud — barrido de TODAS las hojas por alcance nuestro que falte.
- **A cada agente se le pide REFUTAR, no confirmar**, y con el contexto completo por escrito (ruta del PDF limpio, mapa de hojas, escala, tabla de elementos con coordenadas, reglas de estado). Un "verifica esto" produce asentimiento; un "refuta esto" produce hallazgos.
- **Un refutador por verificador**: toma cada diferencia y trata de demostrar que el take-off estaba bien. Solo se corrige lo que sobrevive.
- **Lo que devuelve un agente NO es una cantidad**: es evidencia citada que el hilo principal recomprueba por geometría antes de aceptarla.
- Lo que queda sin resolver pasa a RFI con delta y a "Revisar en la mañana". Los errores encontrados se guardan en memoria y en este skill el mismo turno.
- Caso real: en un solo edificio la verificación cambió el deck, los lengths E/O, dos aberturas exteriores, el ceiling de sales, el blocking de baños, y encontró 4 walls que faltaban y 6 line items de alcance nuevas.

## LOS MARKUPS AJENOS NO SON FUENTE

Un bid set puede traer **anotaciones de Bluebeam de otro estimador dibujadas encima del plano** — se ven como líneas de colores pegadas a los walls y es facilísimo leerlas como si fueran elementos constructivos. En BofA Broomfield el floor plan traía 117 anotaciones, 57 de un estimador.

**PRIMER PASO DE TODO PROYECTO: generar una copia del set SIN `/Annots` con pikepdf y renderizar SIEMPRE desde esa copia.** `pdftoppm` RENDERIZA las anotaciones, así que un recorte "crudo" del original no es crudo. Filtrar `page.annots` después de mirar la imagen llega tarde: para entonces ya se interpretó.

La geometría de `pdfplumber` (`page.lines`) SÍ está limpia también en el original — las anotaciones no entran en el content stream —, así que el riesgo es exclusivamente de lectura VISUAL.

Y no se usan como fuente de medida **ni siquiera de cruce**. Orden del usuario: está entrenando el método para dejar de depender de Bluebeam. Caso real de por qué importa: un markup ajeno de 7.27 ft sobre un wall que medía 3.71 ft hizo perseguir durante varios pasos una diferencia que no existía — su trazo abarcaba el wall más la door más el arranque del tramo siguiente.

## LAS TRES AUTOVERIFICACIONES DE UNA MEDIDA

Una medida es autosuficiente cuando se verifica sola, sin take-off ajeno:

1. **El thickness medido entre las dos faces coincide con el WALL THICKNESS del schedule.** Prueba que el tag pertenece a ese wall. Si el error pasa de ~0.15", el par de faces está mal elegido — casi siempre porque dos walls adyacentes comparten una face.
2. **El resultado cae en una dimensión de diseño.** 11'-0" clavado es señal de que los dos extremos se identificaron bien; 11'-4.9" es señal de que algo se arrastró.
3. **Si hay dimension impresa, coincide.**

## GRANULARIDAD Y MARCADO

- La unidad de trabajo es el **TIPO de wall completo**, con todas sus instancias juntas — si un tipo tiene 16 walls, se hacen los 16. Nunca todos los tipos de golpe, nunca un wall suelto. Ceilings: por CUARTO. Soffits: uno por uno.
- El marcado va **siempre sobre la hoja completa** (el usuario necesita ver el plano entero para detectar lo que se escapó), con **un solo tipo marcado a la vez**, rotulado con el número oficial de wall. Marcas grandes, legibles a escala de hoja, con leyenda. Los recortes de detalle van ADEMÁS, nunca en vez de.
- **ESTILO DE MARCADO APROBADO POR EL USUARIO (26-sep-2026), se usa igual en cada proyecto:** hoja COMPLETA a 300 dpi desde la copia sin markups · **un solo tipo por imagen** · **rectángulo sobre la extensión real** de cada wall · etiqueta en caja de color con el **número oficial + el LF**, unida al wall por una línea guía corta · **azul para los walls con tag y rojo para los que no lo tienen** · auto-test de tinta en las 7 sondas antes de escribir el archivo. Palabras suyas: "la manera como estás marcando las walls está perfecta y me gusta, así tienes que hacerlo en cada proyecto".
- **Un wall es un TRAMO, no un punto: márcalo con un rectángulo sobre su extensión real**, no con un círculo — un círculo no dice dónde empieza ni dónde acaba el wall, que es justo lo que el usuario necesita revisar. Las aberturas se marcan dentro, en otro color. Si el wall tiene una door, la marca se parte en piezas sólidas a cada lado del opening (el auto-test de tinta aborta si el punto de prueba cae en el opening); la cantidad sigue siendo la del wall completo.
- **El paquete de imágenes de cada tipo, antes de cuantificar y sin que lo pida:** (1) hoja completa marcada con TODAS las ubicaciones y sus números oficiales; (2) recortes de zona con las mismas marcas, uno por agrupación geográfica; (3) recorte cerrado y LIMPIO (sin marcar, alta resolución) de CADA ubicación; (4) el DETALLE del tipo en Partition Types, leído completo y medido por geometría; (5) todo renderizado desde la copia sin `/Annots`, y cada imagen reabierta antes de entregarla. Después del paquete: lista numerada + PAUSA.
- **LA TABLA DE BANDAS DEL DIBUJO SALE DE LOS CIERRES SELLADOS, NUNCA DE LA MEMORIA.** Las coordenadas de cada wall marcado se leen del JSON sellado de ese wall (el campo con la derivación del length, que lleva las faces y el run). Re-teclearlas a mano metió **6 errores de dibujo en un solo proyecto**, con las cantidades intactas. El peor: un wall al que se le puso la banda de OTRO wall porque los dos medían casi lo mismo (3.71 vs 3.69 ft) — la trampa de "que el total coincida numéricamente no prueba que sea ese wall". **Nunca asignes una banda por coincidencia de LF**: siempre por tag+leader o por la geometría que el cierre dejó escrita.
- **VERIFICACIÓN MECÁNICA DE TODAS LAS BANDAS ANTES DE ABRIR UNA SOLA IMAGEN** (`verif_bandas.py`, ver su contrato). Revisar 40-60 bandas a ojo, una por una, es lo que vuelve lento el trabajo y además no atrapa el error. La máquina las chequea todas en segundos contra la geometría vectorial y solo se abre imagen donde ella marca algo. **La verificación visual sigue siendo obligatoria**, pero dirigida: primero la máquina, después los ojos.
- **Hay clases de elemento que NO son un tramo recto, y marcarlas como banda es marcarlas mal:**
  - **Column enclosure / pilastra / chase (tag dentro de una caja cerrada):** se marca como **CAJA**, y el LF rotulado es el **PERÍMETRO FURRADO** (solo las faces expuestas), no el length de una face. El sondeo de tinta va sobre el PERÍMETRO: por dentro la caja está hueca y sondear el centro abortaría un marcado correcto. La caja se localiza por coincidencia EXACTA de dimensión (width × alto en pulgadas del cierre → pt) contra los pares de líneas de lineweight de wall, y se confirma porque la face furrada del cierre queda a un thickness de furring hacia dentro de la arista.
  - **Wall inclinado:** rectángulo ROTADO sobre el eje del wall, nunca degradado a círculo.
  - **Bulkhead o header sobre un opening:** se marca sobre el OPENING, así que **0% de face de wall es correcto por definición**. Sus extremos son las **tapas de jamb** de thickness completo, no las faces de los walls vecinos: tomar las faces mete de más el width de la jamb del officefront (4" en un caso real, openings de [valor retirado E24] en vez de los [valor retirado E24] `HOLD CLEAR FINISHED OPENING`).
- **Una face puede estar dibujada FINA.** Antes de declarar que una banda está mal por falta de face, reintenta con lw ≥ 0.55: hay walls cuya face se dibuja como triple línea fina (acabado / board / stud) mientras la otra va en lineweight de wall. Se confirma con imagen y se anota.
- **Toda corrección de cantidad tiene que llegar TAMBIÉN al dibujo.** Caso real: un wall siguió dibujado con [valor retirado E24] LF un mes después de que la reauditoría lo bajara a [valor retirado E24] LF — la corrección estaba en el cierre y en el documento, pero no en la tabla del plano. Una corrección se aplica el MISMO turno a las cuatro cosas: **cierre sellado · documento del proyecto · tabla de bandas del plano · resumen global**.
- **Verificación visual final, sobre la imagen YA MARCADA.** Se reabre cada hoja entregada y se recorta la zona de las bandas **desde esa hoja marcada**, no desde coordenadas calculadas, confirmando que cada rectángulo cae sobre un wall que lleva el tag de ese tipo. Si un recorte no ubica con certeza: recorte amplio de contexto primero, zoom cerrado después.
- **Si en el barrido faltó una ubicación, faltó el wall.** La hoja marcada de un tipo tiene que mostrar TODAS sus instancias y su total tiene que coincidir con el LF sellado de ese tipo. El título de la hoja lleva el tipo, el nº de walls y el LF total, y ese total se toma del resumen global, no se escribe a mano.
- **Si hay detalles, ábrelos: siempre los hay.** Ningún tipo se cuantifica sin barrer las hojas de detalles buscando todo lo que lo toque. Y la llamada a un detalle no siempre está en el floor plan: los head y jamb de cada door salen del **Door Schedule**, en sus columnas HEAD / JAMB / SILL.

## ARCHIVO — TODO ENTREGABLE SE GUARDA EN LA CARPETA DEL PROYECTO

**Orden permanente del usuario (27-sep-2026): "cada uno de esos planos ya marcados guárdalo en la carpeta donde pertenece ese proyecto".** Un entregable que solo existe en el chat NO está entregado: se escribe también en la carpeta del proyecto, en la PC del usuario, y se le dice dónde quedó en palabras (nombre de carpeta y de archivo, nunca la ruta interna del contenedor).

**Dónde.** Los proyectos viven en su Google Drive en modo espejo ("My Drive", unidad G:):

```
My Drive\JC HUNTER PROJECTS\Projects\<proyecto>\<proyecto>\
```

Ojo: **el nombre de la carpeta del proyecto viene anidado DOS veces.** Dentro ya existen `0 - LCI BID REQUIREMENTS` y `1 - Bid Documents` (ahí está el PDF del bid set). Los entregables del take-off van en una carpeta nueva al lado:

```
2 - Take-Off Claude\
    Planos marcados por tipo\    <- una imagen por tipo de partición
    Cierres\                     <- los JSON sellados
    Excel\                       <- el take-off en el formato del usuario
    Documentos\                  <- cierres escritos, RFIs, clarifications
```

**Cómo se obtiene acceso.** La carpeta NO viene conectada a cada sesión nueva. Se pide con `device_request_folder_access` sobre **la carpeta PADRE** `~/My Drive/JC HUNTER PROJECTS/Projects`. Pedir la carpeta del proyecto directamente FALLA: su nombre lleva espacios que el prompt de aprobación remoto no puede mostrar. Con el padre concedido alcanza para todos los proyectos.

**Cuándo.** Cada entregable se guarda **en cuanto queda verificado**, no al final del proyecto: si la sesión se corta, lo guardado sobrevive. El flujo es `SendUserFile` (para que lo vea en el chat) → `device_commit_files` con el `file_uuid` que devolvió (para que quede en su carpeta) → una línea diciéndole dónde quedó.

**Formato de las imágenes entregadas.** JPG de ~6200 px de width y **≤2.6 MB**. `SendUserFile` rechaza con error 400 los PNG de más de ~4 MB, y una hoja completa a 300 dpi pesa más que eso. Se baja la calidad JPG hasta caber, nunca la resolución.

## TODA AFIRMACIÓN DE ALCANCE VA CON SU CADENA

Decir "este detalle aplica a este wall" sin la cadena es plausibilidad, no evidencia. La cadena mínima tiene dos eslabones citados con hoja: **origen → referencia → destino**. Ejemplo real y correcto: `A02.01 puerta 108 en el muro` → `A00.30 Door Schedule fila 108: HEAD 10/A12.02, JAMB 11/A12.02, SILL –` → `10/A12.02`. Sin cadena, la afirmación no se escribe. `closer.py` lo bloquea.

## EL DATO CENTRAL SON LAS LAYERS POR CADA FACE

Orden del usuario: lo más importante del take-off es **qué board, cuántas layers y hasta qué height, face por face**. El thickness del wall no es un dato entregable — es control interno para verificar que el tag está bien asignado.

## SETS CON WALLS DE Wood

Algunos prototipos (p.ej. 7-Eleven 9350 CST-WOOD) enmarcan las partitions con studs de Wood 2x4/2x6 y los exteriores con 2x8. Ahí el alcance metal se reduce a lo que el plano sí pide en steel: slip track de deflection en el tope de las partitions, los soportes CFS de soffits y walls colgados, y cualquier elemento que un detalle dibuje en CFS (p.ej. el shelf del water heater en 6" 18 GA). Los studs, plates, blocking de deflection y pines X-U del bottom plate de wood se reportan en columnas INFO (Div 06), nunca mezclados en una columna de metal, con un RFI de alcance que pregunte si el drywaller también enmarca wood y el delta en LF. `closer.py` se usa igual: la wood va como STUD con su operación y los plates como TRACK_BOTTOM declarando que son Div 06.

## REGLAS INVIOLABLES (errores reales ya cometidos)

- Cadenas paralelas: nunca sumar 2 cadenas que miden el mismo tramo. Contar dimension lines y ubicar ticks antes de sumar.
- Track: LF total ÷ length del wall = runs, debe dar 2. Si da 3, duplicaste el top track.
- Track: bottom y top/deflection SIEMPRE en renglones o columnas separados, **en TODAS las tablas donde aparezca track**, no solo en el resumen de compra. Nunca combinados en una fila aunque el LF total sea correcto.
- **Condición del top track, declarada por tipo.** Cada tipo de partition lleva su propia columna diciendo qué va arriba, con el detalle citado: slip/deflection track, track fijo ("secure to structure") o cap track de wall parcial. Nunca dejes implícito qué corona un wall que llega al deck. Y comprueba DOS cosas por separado: (a) ¿el detalle pide slip track? (b) ¿algún schedule le da designación de perfil y calibre? Si (a) sí y (b) no, es RFI con el delta de precio declarado — un slip track de ala 2" cuesta bastante más que un track normal de ala 1-1/4".
- **Designación SSMA: el calibre está DENTRO del nombre del perfil — decodifícalo antes de decir que falta.** `362S137-33`: `362` = alma en centésimas (3-5/8") · `S` = stud con lip (`T` track, `U` channel, `F` furring) · `137` = ala (1-3/8") · `-33` = **steel en mils**. 33 = 20 ga · 43 = 18 ga · 54 = 16 ga · 68 = 14 ga · 97 = 12 ga. Nunca abras un RFI de calibre sobre un perfil que ya lo trae en el nombre; y si el schedule solo tiene filas de 3-5/8" y 6", lo que falta es la fila, no el calibre.
- **Calibre que el plano no nombra — EL PLANO MANDA SOBRE LA REGLA.** (1) Si CUALQUIER hoja le da calibre o designación a esa pieza, se usa ESA aunque no coincida con su stud, [CONFIRMADO] con hoja citada. (2) Solo si no aparece en NINGUNA hoja, la pieza toma el calibre del stud de ese wall, con la designación derivada completa (stud `362S137-33` → track `362T125-33`) y marca [DERIVADO]. Aplica a track, bracing, channel, clip y head track. Antes de aplicarla hay que buscar de verdad en todo el set, no solo en el Metal Stud Schedule. Caso real: en un mismo wall de 6" el bottom track es `600T125-33` y el top de deflection `600T200-97` — el plano nombra los dos.
- **Una nota `WALL CONSTRUCTION SHALL INCLUDE` dentro del detalle del tipo MANDA sobre el Metal Stud Schedule general.** Caso real: el schedule estructural daba `INTERIOR WALLS @ 16" O.C.` con 33 mil, y el detalle de los walls balísticos pedía **`14 GA. METAL STUDS @ 24" O.C. MAX`** — eso cambia stud, track, conteo de piezas y precio. El detalle del propio tipo es más específico y gana. Esa misma nota suele traer el anchorage (`POWER DRIVEN FASTENERS @ 2'-0" O.C. ALTERNATING SIDES AND WITHIN 3" OF EACH END OF TRACK`) y el trim (`APPROPRIATE METAL TRIM AND CASING BEADS`), que son line items, no decoración.
- **Un tipo con tag en planta pero SIN renglón en el partition schedule no es RFI automático.** Se deriva si coinciden tres caminos independientes: (a) la aritmética de layers del detalle de su familia, (b) el delta constante de la familia (en un caso real la "K" sumaba exactamente 3/8" en las dos filas que sí existían), (c) el thickness MEDIDO en planta. Con los tres cerrando va [DERIVADO] y se declara en Clarifications; solo si falla uno se abre RFI.
- **Antes de abrir un RFI, agota las cuatro fuentes de derivación.** Un RFI gasta tiempo del cliente y hace ver el take-off incompleto. Solo se abre cuando el dato no sale de: (1) la designación del propio perfil, (2) otra fila del mismo schedule, (3) una regla estándar que el usuario ya dio, (4) el detalle dibujado. Decir "el plano no lo dice" sin haber hecho esas cuatro es un error, no una precaución.
- Gap de deflection: verifica si el detalle acota el hueco entre el tope del stud y el deck. Si no lo acota, el stud LF va a la height completa de B.O.D. y se declara que ese es el lado alto.
- Toda wall lleva bottom Y top track, 2 runs mínimo. Full height=deflection; partial height=cap track aunque no tenga nota propia.
- **Un wall de DOBLE ROW de stud (acústico, con isolator entre rows) lleva DOS juegos de track y DOS rows de studs.** Señal de alarma para detectarlo en planta: el thickness medido de una banda es una fracción limpia del thickness del schedule — entonces hay que buscar el par de faces EXTERIORES. Y en el detalle se reconoce porque hay cuatro layers de board (dos por face) y dos perfiles separados por una banda rotulada.
- Doors: solo header, nunca sill (eso es de windows/pass-through). Y la banda de abajo de una door es CERO, pero la de una window o un pass-through es un SILL real, con su board y su metal (ver la SUPER REGLA).
- Studs adicionales (terminación, intersección, esquina, jambs) se CUENTAN, nunca solo se advierten. Recalcular clips con el total.
- **Jambs:** el número de jamb studs por opening lo decide el Header Schedule DEL PROYECTO, no un supuesto. Si el detalle pide jamb doble solo por encima de cierto width, cuenta sencillo abajo de ese width y declara el delta de la alternativa. Cuenta también los cripple studs sobre el header y los LF de head track del calibre que pida el schedule.
- **Un opening puede morir ENTRE DOS TIPOS de wall**, cuando el tipo cambia justo en la door: una jamb queda en un tipo y la otra en el otro. Ese opening no está "dentro" de ningún wall y se cae entre pasadas sin que nadie lo note. Se carga COMPLETO (header + los 4 jamb studs) a UNO de los dos walls, se escribe en el cierre a cuál y por qué, y la pasada del otro tipo lo EXCLUYE citando ese cierre. El length del wall no cambia: sigue siendo de extremo a extremo de su propio tramo.
- **Aberturas de walls exteriores: salen de los STOREFRONT FRAMES, no del door schedule.** Cada frame trae su R.O. y su sill; una door dentro de un frame no es la abertura, el frame lo es. Un frame con sill alto deja un **knee wall** abajo que se SUMA de vuelta — con su board Y su metal, como cualquier sill (ver la SUPER REGLA). Caso real: se descontó solo una puerta de 24 SF cuando su frame medía 196 SF, y bajo otro frame había un knee wall de 3'-2". El board que "wraps at jambs" alrededor del storefront es line item propia (returns + corner bead).
- Jerarquía de medición: dimension impresa > geometría vectorial del PDF > suma de cadena > píxeles (píxeles solo calibrados y validados, nunca sustituyen).
- Ningún número "de paso": cada dimension escrita responde ¿a qué línea pertenece? ¿qué mide? ¿está completa en la imagen?
- Height por layer: confirma por detalle hasta dónde sube cada layer. Sustrato especial y acabado solo hasta finish height.
- Wall existente: no cuantificar material nuevo sin cruzar 4 fuentes (Construction Legend, Demolition Key Notes, Room Finish Schedule, Code Analysis).
- División CSI: antes de incluir una line item, pregúntate si la instala el drywaller. Si viene de fábrica con otro elemento, o el plano dice que lo instala un vendor (office front, coiling grille, storefront), no es nuestro.
- **Nosotros NO hacemos luminarias** (Div. 26). Lo nuestro es SOLO el FRAMED OPENING: framing continuo a cada lado del pocket, retorno de board y gypsum edge trim. La line item se rotula **"framed opening for recessed fixture"**, nunca "light fixture", y se cuenta por LF de pocket (×2 lados), SF de retorno y LF de edge trim; la luminaria va excluida en Clarifications. Aplica igual si un markup ajeno dice "LIGHT FIXTURE".
- **Lo mismo con GABINETES y cualquier equipo de otro:** el mueble no es nuestro, pero **el BLOCKING dentro de la partition y el board sí lo son**. Se abre el detalle del mueble, se cuenta su blocking y se declara el mueble excluido con su división. No se abre RFI por el tamaño de un gabinete ajeno.
- Partition con block: si el detalle muestra BLOCK PARTITION con furring, el block es Div 04 (no nuestro) y solo el furring — y a menudo en UNA SOLA FACE — es nuestro. Verificar cuántas faces antes de cuantificar.
- Cerrar el wall completo: stud+track+deflection+header/sill+bracing+clips+board+sustrato+BLOCKING (lo más olvidado)+insulation+patch, todo de una vez.
- **Áreas con línea quebrada (dash-dot) = zona ampliada en otra hoja vía burbuja — ábrela siempre.** Se reconoce por geometría: líneas de lineweight alto (3-4) dibujadas a trazos, cerrando un rectángulo alrededor de una zona. Ahí suelen estar las notas de blocking y los finish schedules que no aparecen en el floor plan.
- Línea guía del tag: síguela hasta su punta de flecha — la proximidad visual no basta.
- Un mismo wall puede llevar más de un tag: deduplica por identidad de banda antes de sumar LF.
- No inventar lectura cuando no se distingue: di "no logro distinguir X" y detente.
- Mostrar SIEMPRE la imagen de la zona o detalle que se revisa, sin marcar nada encima, antes de concluir. Si el recorte es la zona equivocada, dilo y muestra el correcto.
- Cuartos con nombre distinto en hojas distintas: comparar FORMA del perímetro antes de asumir que son cuartos diferentes.
- Dimension corta con nota "EQ/EQ TYP" = espaciado de luminarias, NUNCA límite de zona o material.
- Dimension corta en planta (2"-6"): verificar si es thickness de wall o longitud real.
- Exclusión de material: SIEMPRE con razón detallada — qué se buscó y dónde, qué sí dice el detalle, contraste con elemento similar que sí la tiene, o RFI si hay duda real.
- Persistir cada wall/zona CERRADO de inmediato en memoria, no solo en el chat. Antes de cuantificar algo repetido, leer el registro primero.
- Toda orden del usuario sobre método se guarda en memoria en el MISMO turno, y se le entrega el protocolo actualizado.
- Nunca empezar otra zona sin terminar la actual (todo cuantificado o EXCLUDED, registro actualizado).
- Al preguntar "de dónde sacaste X": citar hoja/detalle exacto de cada dato por separado.
- **El wall termina en su END CAP, no en la primera jamb.** Recorre los segmentos dibujados de las dos faces y une un hueco SOLO cuando hay un end cap (línea perpendicular de lineweight de wall que abarca exactamente el thickness) a AMBOS lados: eso es una door opening y el wall sigue. Si falta el end cap de un lado, ahí termina. Una tolerancia ciega de hueco NO sirve: con poca tolerancia el wall sale corto y con mucha se dispara, porque une walls distintos que comparten una face.
- **Una "banda" de wall NO es un par de coordenadas válido para toda la hoja.** Una misma alineación puede llevar tramos de TIPOS DISTINTOS y espesores distintos: en un caso real la alineación `x = 1123.08 / 1133.88` llevaba un B2 de 7.20", un G1 de 8.48" (cuya otra face estaba en `x = 1121.16`) y un officefront de marco de 3.1 pt — unirlo todo inventó walls de 13 y 15 ft que no existen. La banda se re-deriva POR TAG, y solo cuenta el tramo donde EXISTEN LAS DOS FACES con lineweight de wall **y** la separación es igual al WALL THICKNESS del schedule de ESE tipo (±0.35"). Control barato: si las dos faces tienen coberturas muy distintas a lo largo del tramo, la banda está mezclando tipos.
- **Un wall run puede llevar VARIOS TAGS en serie.** Al run completo hay que restarle las porciones que gobiernan los otros tags, usando sus dimensions impresas cuando existan. Nunca asignes el run completo a un solo tag. Si no se distingue dónde termina uno y empieza el otro, decláralo y pregunta.
- **Declara si el LF es face-a-face o centro-a-centro.** Una polilínea de Bluebeam se dibuja hasta el EJE del wall perpendicular; la banda dibujada se mide face to face. Para framing el centro-a-centro es el correcto — el track corre por debajo del wall que cruza — así que suma medio thickness del wall perpendicular en cada extremo que muera contra otro wall. La diferencia es sistemática, de 0.2 a 0.8 ft por wall.
- **El registro entre dos hojas se vota con el FONDO ARQUITECTÓNICO, nunca con las burbujas de eje.** El círculo de la burbuja no siempre cae igual respecto de la línea de eje: en un set real las hojas de plomería tenían 3.6 pt de corrimiento (2.4" a escala de planta), suficiente para inventar un cruce de MEP donde solo estaba la línea del wall exterior. Se votan los SEGMENTOS LENGTHS DE WALL (lw ≥ 1.0, ≥ 50 pt) exigiendo ≥ 25 coincidentes en cada dirección. Si una hoja no llega a ese mínimo (las de piping y los RCP a menudo no), esa hoja NO se usa para cruce geométrico y se revisa a ojo, declarándolo.
- **Un cruce de MEP real SOBRESALE por fuera de las dos faces.** Una línea que TERMINA en la face del wall es fondo arquitectónico, no una penetración: se exige ≥ 3 pt de sobresalir por cada lado y se filtra por lineweight (un hatch de 0.24 no es un ducto). Los ductos vienen en PAREJAS de líneas paralelas y la separación entre la pareja ES el width del ducto. **Ojo con el ducto dibujado partido:** si el CAD corta el ducto en la face y mete un conector flexible, el filtro de "un solo segmento que sobresale" no lo ve — hay que detectar también el corredor, o sea la línea que llega al wall por los DOS lados.
- **Blocking de millwork, por tipo de mueble:** base cabinet o counter contra wall = **1 run horizontal** al rail superior, LF = length del run. Wall/upper cabinet = **2 runs** (rail alto y rail bajo). Standards de shelf ajustable = **vertical por standard**, LF = height × nº de standards. Counter que muere de canto contra el wall = **1 cleat vertical** de la height del counter. Wall stop de door = **2'-0" por tope** cuando el plano no lo ubica (length que garantiza agarre en dos studs a 16" O.C.).
- **El Hardware Group de cada door decide si hay blocking de wall stop.** La nota `PROVIDE BLOCKING AT EACH WALL STOP` no aplica a todas las doors: hay que abrir el Hardware Schedule grupo por grupo y ver cuál lista `1 EA WALL STOP`, cuál lista `FLOOR STOP` y cuál no lleva tope. Verificación cruzada gratis: la door leaf dibujada abierta, medida en planta, debe morir contra un wall en los grupos que sí llevan wall stop.
- **Si el usuario señala algo sobre un entregable que TÚ generaste, reabre ESE archivo** — no el JSON de trabajo, no la memoria del turno anterior — y recorta la zona exacta que él señala. El archivo entregado es la fuente de verdad de lo que él está viendo. Nunca le sugieras que leyó mal antes de haber abierto su hoja y mirado el pixel.
- **La numeración de walls no se vuelve a derivar nunca** (ver arriba). Un segundo sistema de numeración destruye la trazabilidad de todo lo ya revisado.
- **Soffits siempre separados de ceilings y de walls**, y ninguno se cuantifica sin su detalle abierto y citado.
- Cuarto con varias alturas de cielo bajo un mismo room tag: no siempre hace falta mapear el límite exacto en planta — confirma con el usuario si basta SF total + alturas de drop + Div 05 por zona.
- **Una dimension con `EQ` a los lados es un TRAMO ACOTADO, no el length del wall.** Caso real: el wall vertical de una oficina medía [valor retirado E24] (dimension impresa y geometría coincidiendo) y la dimension de 8'-0" con EQ arriba y abajo era el **office front**, con 1'-3" de wall sólido a cada lado. Como el officefront es Div 08, cuantificar el wall completo es cotizar board donde va vidrio. En todo wall con officefront o storefront, separa el tramo ajeno del wall sólido antes de cuantificar board — **y después aplica la SUPER REGLA al tramo ajeno, porque encima de él casi siempre hay bulkhead nuestro**.
- **El B.O.D. varía por zona y el tag de ceiling no define la height.** En el mismo proyecto el ACT-4 estaba a 9'-0" en un cuarto y a [valor retirado E24] en otro: se lee la dimension impresa de cada cuarto, una por una.
- **Una pendiente de techo hecha con TAPERED INSULATION no mueve el B.O.D.** Si el Roof Plan dice `TAPERED INSULATION ON METAL DECK`, el deck está nivelado y la caída va por encima: el B.O.D. es constante en la zona y el stud no varía. La flecha `SLOPE` marca el drenaje, no una inclinación estructural. Compruébalo antes de repartir alturas — pero esa nota tampoco anula dos B.O.D. distintos rotulados en dos líneas de viga: cuenta todos los marcadores de la hoja antes de decidir.
- **Antes de asignar un B.O.D. por posición, verifica que las dos hojas no estén espejadas.** Compara los ejes de grid de la estructural contra los de la arquitectónica: si el orden coincide y la diferencia es un offset constante, no hay espejo. Una nota como `BUILDING FOOTPRINT MIRRORED NORTH-SOUTH` suele referirse al prototipo, no a esa sheet — pero se verifica, no se supone.
- **Un wall que cruza la línea (HI)/(LOW) lleva DOS alturas de stud**, y se parte por esa línea. Los ticks de su dimension impresa dicen dónde arranca y termina el tramo de cada tag: no se deduce desde el extremo del run.
- **Techo de steel joists (OWSJ):** B.O. de la estructura = bearing del joist menos su peralte; B.O. deck = bearing + asiento + nailer (si lo hay) + sub-purlin. Sácalo de las secciones, del Roof Framing Plan y del detalle sub-joist-to-joist, y declara las dos alturas: el detalle del tipo decide a cuál llega el board, la otra va como delta de RFI.
- **Wall colgado "above":** además del stud y el board necesita su soporte CFS — hangers a cada cuerda de joist que cruza y struts entre joists. Cuenta los cruces con el spacing de joists del estructural; si el wall corre PARALELO a los joists (0 cruces), va como allowance + RFI.
- **Top de walk-ins por cuarto, no uno solo.** Un beer cave suele ser más alto que el cooler vault; el wall se parte donde cambia el T.O. del panel.
- **Board detrás de coolers y en cuartos eléctricos: revisa la sección de wall de esa condición** (A4.x) — suele pedir MR detrás de refrigeración y plywood en eléctrico, distinto del board típico del wall exterior.
- **Lo que hay ARRIBA y lo que hay DEBAJO de una abertura es material nuestro hasta que se demuestre lo contrario** (ver la SUPER REGLA). Las dos restas —`ceiling − header` arriba y `sill − piso` abajo— se hacen en TODA abertura, por face, y cada resultado va en renglón propio. Del board solo se deduce la abertura NETA (`header − sill`), nunca el rectángulo de piso a ceiling.
- **La banda de un wall se fija con la pareja de faces de lineweight ALTO (≥1.1), nunca con la primera pareja que cuadre de thickness.** Un detector que acepta lw ≥ 0.5 para no perder tramos puede devolver una banda formada por las líneas INTERIORES del wall: mismo thickness, mismo LF, pero desplazada ~1 pt y anclada donde no es. Se comprueba imprimiendo el lineweight de las dos faces elegidas.
- **Todo cache de render lleva la IDENTIDAD DE LA FUENTE en su clave.** Un cache con clave `pg<pagina>_<dpi>` reusa el PNG del PDF CON markups cuando ya se pidió la copia limpia, y anula en silencio la regla de los markups. La clave lleva `sha256(path + mtime + tamaño)`. Regla general: una regla que depende de "usar el archivo correcto" no está cumplida hasta que el cache también distinga el archivo.
- **Un md5 distinto entre dos copias limpias NO significa contenido distinto**: pikepdf y las librerías de PDF no escriben bytes deterministas. Antes de dar la alarma se compara el CONTENIDO — hash de `page.lines` y de `page.rects` de la hoja de trabajo, y conteo de `annots`. En un caso real las tres copias dieron 79,052 líneas y 1,903 rects con el MISMO hash, y solo el original traía anotaciones; eso además vuelve a probar que la geometría vectorial del original está limpia y que el riesgo de los markups es exclusivamente VISUAL.
- **Verificación con agentes: se les pide REFUTAR, no confirmar.** Si el usuario autoriza subagentes o workflows, cada agente recibe por escrito el contexto completo (ruta del PDF limpio, mapa de hojas, escala, la tabla de elementos con coordenadas y las reglas de estado) y la consigna "por defecto asume que esto está mal hasta que la evidencia te obligue a aceptarlo". Un "verifica esto" produce asentimiento; un "refuta esto" produce hallazgos. **Lo que entrega un agente NO es una cantidad**: es evidencia citada que el hilo principal recomprueba por geometría antes de aceptarla — en un caso real, de dos alarmas de agentes una era una corrección real y la otra era falsa. Y al final va un **crítico de completitud** que no repite el trabajo sino que busca el hueco: qué hoja no abrió nadie, qué afirmación quedó sin atacar, dónde se contradicen dos agentes.
- **Tile: cement board por criterio de oficio aunque el plano diga MR** — se cotiza cement board y se declara el alterno (MR según planos) con su delta en RFI/Clarifications.

## LOS ERRORES Y SU SOLUCIÓN (índice — el desarrollo está en las secciones de arriba)

1. Dimension tapada por un gráfico → extraer texto interno del PDF, nunca adivinar la fracción.
2. Dimensions verticales por script → agrupar por x exacta, cortar por hueco, validar contra patrón, cotejar con imagen.
3. Tablas de schedule idénticas ≠ walls idénticos → leer el DETALLE de cada tipo.
4. Schedules fuera de arquitectura → Metal Stud, Brace, Header y Fastener en la serie S; el B.O.D. en el Roof Framing Plan.
5. Cerrar un tag en su primera aparición → barrido por TAG en todo el plano desde el texto del PDF.
6. **El rótulo de la elevación no es evidencia** (el más caro) → callout + flecha + orden de ejes + contenido, las cuatro.
7. Ticks SIMPLES vs DOBLES → con dobles la suma de tramos no es el wall; faltan los espesores perpendiculares.
8. Medir por píxeles teniendo geometría vectorial → `page.lines`; el thickness contra el schedule autoverifica el tag.
9. Walls dibujados en piezas colineales → unir la run completa, nunca un segmento suelto.
10. Seguir el leader demasiado lejos → probar todos los extremos, parar donde el thickness cuadre con el schedule.
11. Un wall con más de un tag → deduplicar por identidad de banda; dos colineales adyacentes de distinto tipo NO son duplicados.
12. Usar una dimension sin saber qué mide → emparejarla con su propia línea de dimension (length ÷ escala = valor, ±1").
13. Bottom y top track en una sola columna → separados en TODAS las tablas, más la columna "condición del top track".
14. Slip track sin DESIGNACIÓN → comprobar por separado si el detalle lo pide y si algún schedule le da perfil y calibre.
15. **Medir el tramo entre cruces en vez del wall** (55% corto contra un manual) → END CAP a ambos lados, no tolerancia ciega.
16. Face-a-face vs centro-a-centro → diferencia sistemática de 0.2 a 0.8 ft; declarar siempre cuál se usa.
17. Un wall run con varios tags en serie → restarle las porciones de los otros tags con sus dimensions impresas.
18. **Dos numeraciones de wall en el mismo proyecto** → una sola, fijada en el barrido; si ya hay dos, tabla de equivalencia.
19. Contradecir al usuario sobre tu propia hoja sin reabrirla → reabrir ESE archivo entregado y recortar la zona que él señala.
20. Dar por bueno el ceiling de un cuarto sin seguir el leader de su tag → un `GB` junto a un cuarto puede ser del soffit.
21. Confundir una dimension de layout de luminarias con un límite de material → emparejarla con sus ticks.
22. Copiar el rótulo de un markup ajeno → seguir el key note hasta la punta y buscar el código en la leyenda.
23. **Inventar el factor pt→px y entregar imágenes sin abrirlas** → de ahí salió `planmark.py`. Una regla en prosa no impide un error de multiplicación; solo lo impide código con auto-test.
24. **Confundir un markup de Bluebeam con el dibujo** → copia sin `/Annots` como primer paso; `page.annots` antes de interpretar cualquier línea de color.
25. **Confundir un tramo acotado con `EQ` con el length del wall** → la resta lo delata: wall − tramo, entre los dos EQ, da medida redonda.
26. **Tratar una banda como dos coordenadas válidas para toda la hoja** → re-derivar la banda por tag, exigiendo las dos faces y el thickness del schedule.
27. **Registrar dos hojas por las burbujas de eje** → votar el fondo arquitectónico; las burbujas mienten hasta 3.6 pt.
28. **Dar por cruce cualquier línea que toque la banda** → un cruce real sobresale ≥ 3 pt por fuera de las dos faces.
29. **Opening que muere entre dos tipos de wall** → cargarlo completo a uno y excluirlo en la pasada del otro, citando el cierre.
30. **Contar el tipo solo por tag** → contarlo también por su grafía y comparar; la densidad de hatch separa lo real del ruido.
31. **Tomar calibre y spacing del schedule estructural sin leer la nota del detalle** → `WALL CONSTRUCTION SHALL INCLUDE` manda.
32. **Abrir RFI porque un tipo no tiene renglón en el schedule** → derivarlo por aritmética de layers + delta de familia + thickness medido.
33. **Buscar un material por su nombre comercial** → volcar el set con `pdftotext` y buscar por sinónimos de lo que el material ES.
34. **Transponer el punto de prueba en una banda horizontal** → el centro de una banda `H` es `(x=(lo+hi)/2, y=(c0+c1)/2)`; escrito al revés, el auto-test de tinta aborta, que es lo correcto.
35. **Mapear coordenadas sobre un recorte que se redujo para verlo** → la escala efectiva es `F × (ancho_final / ancho_original)`, no `F`.
36. **Tomar un bid set parcial (solo fueling/canopy) como si fuera el edificio** → Paso 0: confirmar qué paquete es; si no hay Partition Types ni RCP, el alcance puede ser CERO y se entrega así, con cada cero justificado.
37. **Herramientas probadas solo con PDFs de prueba cómodos** → el primer set real destapó 3 bugs (rótulo por zona fija, censo sin schedule, track ×2 por renglón).
38. **arranque.py con pdfplumber sobre un set grande** (97 MB, 73 hojas: >20 min sin terminar) → para el mapa de hojas usar `pdftotext -f N -l N -bbox` por página; pdfplumber solo en las hojas de planta.
39. **Marca de planmark sobre un wall con door** → el punto de prueba cae en el opening y el gate aborta (correcto); se marca en piezas a cada lado.
40. **Set con walls de Wood** → el alcance metal se reduce a slip track + soportes CFS de soffits; la wood va INFO Div 06 con RFI.
41. **Tags en rombo/hexágono** → `tagband` no los ve como caja; censo por layer de texto dentro de la hoja de planta + verificación visual.
42. **Soffit escondido en el RCP** → barrer TODAS las llamadas de detalle del RCP y abrir cada una; leer la keynote de cada soffit.
43. **Walls "above" sin cuantificar el soporte** → un wall colgado necesita su soporte CFS: hangers a cada cuerda de joist que cruza + struts.
44. **Interpolar la height wall por wall en un techo en pendiente** → la regla ya existía (extremo ALTO de la zona) y se programó el cálculo sin releerla.
45. **B.O. deck sin el nailer** → armarlo layer por layer desde el detalle sub-joist-to-joist; un 2x6 plano olvidado son +1.5" en todo lo que va al deck.
46. **Aberturas exteriores desde el door schedule** → salen de los storefront frames (R.O. + sill); se dejó de descontar 172 SF de un frame y se omitió un knee wall.
47. **Length exterior = dimension de grid − thickness supuesto** → medir las faces interiores vectoriales (49.81 ft, no 49.42).
48. **Wall a trazos medido hasta el final de un trazo, y quiebre del patrón ignorado** → medir la línea completa; el quiebre del dash marca cambio de tag.
49. **Profundidad de soffit tomada de una dimension del RCP que era de la fila de ACT** → emparejar cada dimension con sus ticks; el detalle del soffit manda.
50. **Cantidad sin desglose** (blocking de baños 93.5 LF escrito a mano) → toda cantidad con su lista pieza por pieza; recontado dio 66 LF.
51. **Soffit sin todas sus faces y backer doble contado** → cada soffit: fondo + face vertical + retorno + tapas; un backer que el detalle pone en la face del wall ya está en ese wall.
52. **Walls pequeños o sin tag que se escapan** (medias walls y furring sin tag) → el barrido por grafía (#30) incluye rectángulos cerrados sin hatch y furring pegado a walls exteriores.
53. **Alcance fuera de las partitions que no se barrió** (shelf de water heater en CFS, returns de storefront, light wells, access panels, cut-outs de chases) → el crítico de completitud barre TODAS las hojas antes de entregar.
54. **Contar solo el wall sólido de una alineación con office front y dejar fuera el BULKHEAD de encima** (el error que motivó la SUPER REGLA) → el office front moría a 8'-0" y el ceiling estaba a 9'-0": 1'-0" de wall continuo sobre los [valor retirado E24] de cada abertura, en seis oficinas, sin contar. Los detalles "OFFICE BULKHEAD @ DOOR" y "@ GLASS PANEL" lo traían entero: `2 LAYERS 5/8" GYPSUM WALL BOARD TO EXTEND TO UNDERSIDE OF DECK`, doble row de stud con isolator, `CONT. SLIP TRACK`, `CONT. BOX BEAM`, `3/4" FRT PLYWOOD BLOCKING`, `CORNER BEAD` y `SHADOW MOLDING`. Eran 1,354 SF de board más su metal. **Y el error tiene su mitad simétrica abajo:** el sill bajo una window o un pass-through es otra banda con su propio board y su propio metal (cripple studs + sill track), y lo único que se deduce del wall es la ABERTURA NETA entre header y sill, no el rectángulo de piso a ceiling.
55. **Fijar la banda con la pareja de faces equivocada** → el detector acepta lw ≥ 0.5 para no perder tramos y puede devolver las líneas INTERIORES del wall: mismo thickness y mismo LF, pero ~1 pt desplazada.
56. **El cache de render anula la regla de los markups en silencio** → la clave del cache lleva la identidad del archivo fuente (`sha256(path+mtime+tamaño)`), no solo página y dpi.
57. **Dar la alarma por un md5 distinto entre dos copias limpias** → comparar CONTENIDO (hash de `page.lines` y `page.rects`, conteo de `annots`), no bytes: las librerías de PDF no escriben salida determinista.
58. **Pedirle a un agente que "verifique"** → se le pide REFUTAR, con contexto completo por escrito, y su salida es evidencia citada que el hilo principal recomprueba, nunca una cantidad.

59. **Re-teclear a mano las coordenadas del dibujo en vez de leerlas del cierre sellado** → 6 bandas mal en un proyecto con las cantidades intactas; la tabla de marcado se deriva de los JSON sellados y se chequea con `verif_bandas.py`.
60. **Asignar una banda por coincidencia de LF** → un wall quedó dibujado encima de otro que medía casi lo mismo (3.71 vs 3.69 ft). La banda se asigna por tag+leader o por la geometría escrita en el cierre, nunca por el número.
61. **Marcar una column enclosure como si fuera un tramo de wall** → se marca como CAJA, con el LF = perímetro furrado, y el sondeo de tinta sobre el perímetro (el centro está hueco).
62. **Marcar un bulkhead con las faces de los walls vecinos** → sus extremos son las tapas de jamb; usar las faces mete de más el width de la jamb del officefront ([valor retirado E24] en vez de [valor retirado E24]).
63. **Descartar una banda buena porque una face no llega al lineweight de wall** → hay faces dibujadas como triple línea fina; reintentar a lw ≥ 0.55 y confirmar con imagen.
64. **Corregir una cantidad y no corregir el dibujo** → un wall siguió dibujado con el valor viejo un mes después de la reauditoría. Toda corrección toca las cuatro cosas el mismo turno: cierre, documento, tabla de bandas y resumen global.
65. **Dejar el entregable solo en el chat** → todo entregable se escribe también en la carpeta del proyecto en la PC del usuario, en cuanto queda verificado (ver ARCHIVO).

## BARRIDO COMPLETO POR TAG + PAUSA OBLIGATORIA

Un mismo tag puede aparecer en varios walls, en zonas no contiguas del plano. Antes de dar por cuantificado un tipo, recorre TODO el floor plan localizando CADA repetición de ese tag y haz lista numerada de ubicaciones. Cerrar un tag tras cuantificar solo su primera aparición deja walls enteros sin cuantificar en silencio.

Verifica además que no exista ningún tag con un nombre que no tengas contemplado: revisa todas las palabras del mismo tamaño de texto dentro del área del plano, no solo los tags que ya conoces. Abre imagen de cada candidato dudoso — las burbujas de callout de elevación pueden compartir height de texto con los tags.

**Un tag de partition es una palabra dentro de una CAJA REAL** — un rectángulo verdadero de 10–26 pt de lado, lineweight ≤ 0.7, con sus dos verticales de igual extensión y sus dos horizontales casando con sus x. Exigir la caja descarta de una vez las burbujas de eje de grid, que comparten el texto (una "B" o una "G" sueltas) pero no la caja. El censo de tags con caja real tiene que reproducir la numeración oficial del proyecto: si no cuadra, falta un tag o sobra un falso positivo. **Si los tags del set son rombos o hexágonos** (no caja), el censo se hace por layer de texto dentro de la hoja de planta, filtrando por el patrón de los tipos del legend (p.ej. `A.3`, `G.6`), y se verifica cada uno en imagen. **Cada tag del censo tiene que terminar en un wall cuantificado.**

**Todo candidato SIN LEADER se abre en IMAGEN antes de descartarlo:** puede ser una burbuja de eje (se descarta) o un tag legítimo cuyo leader el detector no encontró. Toda discrepancia contra la numeración oficial se resuelve mirando, nunca aflojando la tolerancia.

**Y el tipo POR DEFECTO del set no se cuantifica por tags.** Si el floor plan trae una nota tipo `ALL PARTITIONS TO BE TYPE 'X', UNLESS OTHERWISE NOTED`, todo wall sin tag es de ese tipo y hay que encontrarlo por barrido geométrico. El método que funciona: resolver la banda de CADA tag conocido → marcarlas TODAS en una hoja completa → mirar buscando wall SIN marca → medir solo esas zonas. Es marcar la hoja al revés: para ver el hueco, no el wall. Antes de cargarlo al tipo por defecto, **léele el perfil de lineweight**: 4+ líneas finas (lw 0.48–0.60) dentro de 2"–3" es storefront (Div 08), y una sola línea gruesa continua es vidrio — busca texto `R.O.` o `CLEAR FINISHED OPENING` al lado antes de darlo por wall.

Al terminar el barrido, NUNCA pases directo a cuantificar. Muestra la lista numerada Y una imagen circulada de CADA ubicación, y DETENTE a esperar confirmación explícita del usuario de que la lista está completa. El conocimiento que el usuario tiene del plano es el filtro final.

**Modo desatendido (el usuario pidió "hazlo completo sin preguntarme").** Cada pausa obligatoria se convierte en un punto de revisión documentado: la lista y sus imágenes circuladas se entregan igual, cada medida faltante queda [PENDIENTE] con su RFI en vez de preguntarse, y la entrega trae una pestaña "Revisar en la mañana" (en español) con todo lo que él normalmente habría confirmado, cada punto con su delta.

## VERIFICACIÓN CRUZADA DEL BARRIDO — CONTAR TAMBIÉN POR GRAFÍA

El barrido por tag tiene un segundo camino que lo verifica, y es obligatorio usarlo cuando el legend le da a un tipo una **grafía propia** (hatch, patrón de línea, relleno): se barre la hoja entera buscando esa grafía, sin mirar los tags, y se clasifica cada banda encontrada por su thickness medido.

- Si el conteo por grafía coincide con el conteo por tag, la lista está completa por dos caminos independientes.
- Si no coincide, hay un wall sin tag o un tag sin wall, y hay que encontrarlo antes de cuantificar.
- Incluye también rectángulos cerrados SIN hatch (medias walls, stubs) y bandas pegadas a walls exteriores (furring).
- **Un tag puede aterrizar en una CAJA CERRADA y no en un wall corrido** (pilastra, wrap de columna, chase): se cuantifica por PERÍMETRO FURRADO × height, 1 stud por esquina y por borde libre, corner bead vertical en cada arista. Solo las faces EXPUESTAS llevan furring, y se detectan buscando una face paralela a un thickness de furring hacia dentro.

Cómo separar el hatch real del ruido: las diagonales de un hatch van a **paso constante**. Se mide ese paso en una banda conocida y se calcula `densidad = nº de diagonales ÷ (largo ÷ paso + 1)`. En un hatch de verdad da ≈ 1.00; en un falso positivo (las diagonales sueltas de una door leaf, la X de un recuadro, un swing aproximado) baja a 0.4 o menos.

Caso real: 4 bandas con hatch en toda la hoja — una de 7.68" (el tipo con 1 tag) y tres de 5.2" (el tipo con 3 tags); correspondencia 1:1, con densidades de 1.00–1.04 contra 0.11–0.40 de los descartados.

**Todo length NO EXPLICADO se parte por coordenada hasta que cada trozo tenga dueño** — tipo nuestro, otra división, o hueco — y ningún trozo queda sin nombre. Se comprueba leyendo el rótulo dentro del tramo y el perfil de líneas.

## REGISTRO ENTRE HOJAS Y CRUCE DE MEP

Para cruzar una hoja de MEP contra las bandas de wall de la arquitectónica hacen falta dos cosas, en este orden:

1. **Registro.** Se deriva el offset (dx, dy) entre las dos hojas votando los segmentos lengths de wall del fondo arquitectónico (lw ≥ 1.0, ≥ 50 pt), exigiendo ≥ 25 coincidentes en cada dirección. Las burbujas de eje NO sirven (ver reglas inviolables). Si una hoja no alcanza el mínimo, no se usa para cruce geométrico: se declara y se revisa a ojo. **Verifica el SIGNO del offset con 3 rasgos reconocibles antes de usarlo.** Y ojo con las hojas cuyo MediaBox no es nulo (las de plomería suelen tener origen desplazado): para recortar hay que restar el origen en X y en Y, o los recortes salen corridos.
2. **Cruce.** Una línea cuenta como penetración solo si sobresale ≥ 3 pt por FUERA de las dos faces de la banda, y se filtra por lineweight. Después se descarta todo lo que también exista en la arquitectónica en la misma posición: eso es fondo, no MEP. Las líneas de retícula de ACT del RCP van a paso constante (2'-0") y mueren exactas en las dos faces: se descartan.

Cada penetración se evalúa **individualmente** contra el umbral de 1/4 de hoja, nunca sumada con las demás. Debajo del umbral es patch, y aun así se LISTA. Un ducto que cruza por encima del head de una door sí penetra el wall: arriba del header hay framing hasta el deck. Y toda penetración reportada se abre en imagen para leer su rótulo (tamaño, tag, CFM) antes de cuantificarla, cruzándolo contra el schedule mecánico.

**Penetración EN el stud, no solo entre studs.** El detalle estructural limita el diámetro del agujero en el ALMA y prohíbe cortar las ALAS; un ducto mayor obliga a abertura enmarcada o chase, que es line item nuestra. En un wall de DOBLE ROW el ducto atraviesa DOS almas, así que hace falta un juego de studs por row. Los chases de plomería llevan toe-to-toe stud post + cold rolled channel y van separados mínimo 4'-0".

## PROTOCOLO DE EJECUCIÓN

**PASO 0 — ¿Qué paquete es este set?** Lee el índice y confirma que el set contiene el EDIFICIO (floor plan, Partition Types, RCP). Un bid set puede ser un paquete parcial — canopy, site/civil, MEP — sin obra de interior. Si no hay Partition Types, floor plan ni RCP, el alcance Div 05/09 puede ser CERO: dilo en la primera línea, justifica cada cero con su hoja, y NO fabriques un take-off. Caso real (un fueling set de 27 hojas): canopy, deck, gutter y framing del fascia son del fabricante del canopy, el fascia es "by others" y el soffit es pan deck expuesto; lo único posiblemente nuestro eran los column wraps sin detalle → RFI con alterno valorizado, fuera del base. Ojo al contar columnas de canopy: suelen ser 2 por isla, no una. Confirma también el SISTEMA de framing: si el legend dice WOOD STUDS, aplica la sección SETS CON WALLS DE Wood.

**PASO 0 — Mapa de hojas.** Corre primero `arranque.py <pdf>` (ver su sección propia): automatiza la parte mecánica de este paso — copia sin markups, verifica layer vectorial, renderiza, lee el rótulo de cada page_index y arma el mapa, ubica por título el Drawing Index y los schedules, y da un censo preliminar de tags. Se detiene en un punto de control; revísalo antes de seguir. En sets grandes (más de ~40 hojas o ~50 MB) el mapa se arma con `pdftotext` por página. Lee el Drawing Index de la portada a alta resolución. Tabla: título → número → página PDF. Busca por TÍTULO, no por número. Verifica el rótulo real en el title block de cada página — la forma barata de hacerlo es extraer el texto de la esquina inferior derecha de cada página y leer ahí el número de hoja, en vez de contar callouts (si el title block de este set no está ahí, `arranque.py --title-block-zona` se ajusta). **Guarda el mapa page_index → hoja**, y recuerda que `pdftoppm` nombra el PNG con el número 1-based: "...-24.png" es page_index 23. Revisa el Revision Log. Nunca declares una hoja "faltante" sin barrer TODO el PDF por rótulo.

**PASO 0B — Demolition Plan.** Distingue existente que permanece / a demoler / nuevo. Lee las Demolition General Notes completas. "Add GWB/furring as required" casi siempre = patch sobre existente. En obra ground-up no hay demo interior: decláralo y sigue.

**PASO 1 — Building Code Analysis.** SF total, pisos, Construction Classification, Occupancy Group, códigos, occupancy load, tipo de proyecto.

**PASO 2 — Especificaciones Div. 05 y 09.** Tipos de stud/track/bridging/clips, corner guards, reveals, tipo/thickness/marca de cada board, finish level, FRP. Si no hay libro de especificaciones en el set, dilo y deriva de Partition Types + notas generales + hojas estructurales. Lee también la **leyenda de materiales exteriores** de la hoja de elevaciones: ahí se definen los códigos PT-x (thickness real del stucco), SA-x, AF-x, CJ, EPS-x, SS-x, GL-x. Sin esa leyenda no se puede cerrar el thickness de layers de nada que lleve stucco. Ojo con acabados que exigen nivel 5 (wallcovering, felt panels): cambian el costo de acabado — pero comprueba a QUÉ código de wallcovering se refiere esa keynote antes de extrapolarla a todos. Revisa en el Material Schedule la columna de quién suministra/instala (p.ej. FRP "GC / GC"): lo que no está claramente en nuestro alcance va como alterno, no en el base. Si no hay finish level especificado, decláralo como supuesto (Level 4) en Clarifications.

**PASO 3 — Partition Types.** ⛔ Primero la LISTA FIJA DE ALCANCES (regla 52.1, ADENDA v52 al final de este archivo): `alcances.py escanear` + sus 24 renglones al registro. Por cada tipo: height T.O. Wall, stud, layers de board por face (separa regular/W.R./greenboard/FRP/plywood/cement board), Metal Stud Schedule, Brace Schedule, Header Schedule, Stud Notes, Lateral Bracing, Typical Fasteners. Abre el DETALLE de cada tipo, no solo la fila de la tabla, y lee su NOTA DE CONSTRUCCIÓN completa: ahí pueden venir calibre, spacing, anchorage y trim distintos de los del schedule general. **Y barre la hoja de Partition Types entera buscando detalles que NO son de un tipo con tag** — bulkheads sobre office front, sills y sills, jambs, encuentros, transiciones: son line items nuestras que ningún tag del floor plan va a traerte.

**Mide el detalle por geometría, no a ojo.** A 3"=1'-0" son 18 pt por pulgada real: una layer de 5/8" mide 11.28 pt y un stud de 1 5/8" mide 29.25 pt. Así se cuenta cuántas layers hay por face y cuántas rows de stud, que es el dato central.

NUNCA mezcles exteriores con interiores. Orden inviolable: Pasada 1 (exteriores, face afuera) → Pasada 2 (esos mismos exteriores, face adentro; "by future tenant" solo aplica si el wall es NUEVO) → Pasada 3 (interiores). Declara al inicio de cada respuesta qué pasada trabajas.

**PASO 4 — Recorrer el Floor Plan** por cuadrantes, con Construction Legend. Aplica el barrido completo por tag, su verificación cruzada por grafía y su pausa obligatoria.

**PASO 4A — Filtro de alcance.** Clasifica cada tramo: (1) construcción nueva Div05/09 → cuantificar; (2) patch and repair → área SF como allowance, sin waste, citando la nota; (3) fuera de alcance (storefront=Div08, "to remain", mampostería=Div04, vendor) → listar con motivo. Un tramo puede tener varias zonas de alcance distinto — mapéalas, no asumas uniformidad. **Y de todo tramo que salga fuera de alcance, aplica la SUPER REGLA a lo que quede ENCIMA y DEBAJO.**

**PASO 4B — Cruce MEP.** Cruza cada trade contra cada wall y ceiling drywall, con el registro y el criterio de cruce de la sección de arriba. En remodelación: penetración menor a 1/4 hoja = patch (listar, no sumar entre cortes); 1/4 o más = reemplazo nuevo. Umbral NO acumulativo. En obra nueva el impacto no es patch sino aberturas enmarcadas donde el ducto cruza walls que llegan al deck, refuerzo en penetraciones de stud, y chases de plomería con su framing propio (wall chases, sleeves, accesorios empotrados = cut-outs contados por pieza).

**PASO 4C — Cierre formal por eje.** Antes de cuantificar: lista numerada por escrito de los walls de la zona, ubicación por TEXTO. Antes de cada eje nuevo: describe el tramo y confirma con el usuario. Nunca asumas que un eje nuevo tiene las condiciones del anterior. Cierre de cada eje en 8 secciones: 1) datos base con estado; 2) desglose de segmentos con verificación de suma; 3) evaluación de alcance por material; 4) justificación de exclusiones Div05/09; 5) exclusiones de otras divisiones con keynote; 6) conclusión; 7) texto para Clarifications; 8) pendientes. Un eje se cierra por FACE — declara cuál cerraste y qué falta.

**PASO 4D-BIS — Checklist antes de declarar un wall cerrado:** stud, track top+bottom, deflection/slip, header/sill, bracing, clips, board por face y tipo, sustrato especial, acabados nuestros, deducción SOLO de la abertura neta (header − sill), jamb studs, cripple studs, head track, **las DOS bandas de cada abertura con su propio metal** (bulkhead arriba, sill abajo), sealant, BLOCKING (fixtures, grab bars, lavatories, mirrors, shelving, millwork, monitores, wall stops de door, roof hatch, signage/decor, water heater platform, roof ladder brackets), insulation, patch.

**PASO 4D — Fixtures y blocking.** Keynotes del floor plan → Fixture Plan → Fixture Key Notes → detalle de CADA tipo por separado. Distingue blocking SURFACE MOUNTED de blocking DENTRO de la partition. El fixture lo pone el cliente; lo nuestro es el blocking y el board. **La nota ALFABÉTICA de hoja "CONTRACTOR SHALL PROVIDE BLOCKING FOR ALL EQUIPMENT AND ACCESSORIES MOUNTED ON WALLS" no tiene leader ni número**, así que no aparece buscando key notes: obliga blocking en todo aparato dibujado sobre un wall. Es la que más blocking genera y la más fácil de saltarse. Lee también las notas del Door Schedule y del Millwork Schedule: uppers, standards de shelf y counters con supports obligan blocking. En baños, la hoja ampliada trae su propia sheet note de blocking, su finish schedule (wall covering, cove base, height del FRP) y su nota de board resistente a la humedad detrás de inodoro y lavabo: ubica accesorio por accesorio en qué FACE cae, porque casi nunca caen todos en la misma. Las elevaciones interiores traen keynotes de blocking con height — mide su length en la elevación — y líneas punteadas de blocking SIN keynote detrás de shelves. Las hojas de decor/signage también dan blocking.

**PASO 5 — Height de DECK (crítico).** Busca en orden: 1) Building/Wall Sections, 2) Interior Elevations, 3) RCP y detalles, 4) Exterior Elevations, 5) Enlarged plans, 6) Estructurales (Roof Framing Plan: el B.O.D. suele estar acotado por zona ahí; detalles S3.x para el armado joist-nailer-purlin). No asumas una sola height para todo el edificio — puede variar por zona y tener pendiente. Verifica que el datum sea de la estructura PRINCIPAL, no de un soffit o marquesina menor. Sin elevación dedicada, usa la típica como [DERIVADO] explícito, nunca [CONFIRMADO].

**Alturas de elementos exteriores (columnas, wraps, piers).** La elevación exterior trae los datums impresos a la izquierda (T/SLAB, B/GLAZING, T/GLAZING, B/CANOPY, T/CANOPY, T.O. PARAPET): la height se deriva restando dos datums y se verifica midiendo el elemento en la propia elevación por geometría, no a ojo. Cantidad y separación de columnas se cruzan además contra el Roof Framing Plan y el RCP: tres fuentes independientes.

**PASO 6 — Ceilings y Soffits (SIEMPRE SEPARADOS, en tablas distintas).** Un soffit **se construye**: su mano de obra y su material no se parecen a los de un ceiling plano, así que nunca van mezclados ni entre sí ni con los walls.

Ceilings GWB: menciona ACT y open-to-deck aparte. Height A.F.F., paint tag, área — usa dimensiones de wall ya cerradas o las líneas vectoriales del RCP identificadas una por una (face de wall, borde de ACT, borde de soffit), nunca una resta de áreas estimadas. Hanger y splay wire: si el RCP muestra el layout real de luminarias, cuéntalas directo; length de hanger = B.O. Deck − height de zona; se compra por rollo de LF por gauge. Cuarto con varias alturas bajo un mismo room tag: Div05 SÍ se separa por zona, Div09 board NO. Cruza cada tag del RCP contra el Room Finish Schedule: una discrepancia es RFI con su delta. Las caídas de ceiling se miden por su línea de borde sólida, no por el perímetro del nicho. Skylight con light well: el pozo de gyp es line item (perímetro × profundidad + corner bead).

**Soffits — ninguno se cuantifica sin abrir y citar TODOS sus detalles. No basta el RCP.** De cada detalle: medida de stud y **su spacing propio** (difiere del ceiling) · kickers/bracing y su spacing · track arriba y abajo · anchorage a la estructura (purlin, cont. track bajo deck, powder-driven) · width en planta · profundidad · length · si va "up to deck" (length de stud = B.O. Deck − fondo del soffit) · board por face — **face vertical + fondo + retorno + tapas son áreas distintas** · sustrato especial · corner o L bead · shadow molding · blocking · acabado. La profundidad sale del DETALLE; una dimension del RCP junto al soffit puede ser de la fila de ACT.

**El anchorage al deck es line item propia y la más olvidada:** si el flute corre paralelo al track, el detalle exige purlin cruzando mínimo dos flutes, "NO EXCEPTION". Se cuenta por LF de track.

Cómo localizarlos: en el RCP, el achurado de "new suspended gypsum wall board ceiling/soffit" incluye ceilings planos Y soffits. Se distingue el soffit porque **cae por debajo del ceiling que lo rodea** — compara su height A.F.F. contra la del cuarto. Barre el RCP entero buscando cada zona de ese achurado, clasifica cada una como ceiling o soffit con su height, entrega la lista numerada con imagen de cada una, y solo entonces ve por los detalles. **Además barre TODAS las llamadas de detalle del RCP y abre cada una**: un soffit puede no tener achurado propio y aparecer solo por su llamada. Y lee la keynote que apunta a cada soffit: puede asignar sus paneles a otro vendor.

**Soffit exterior de canopy.** No es un soffit interior ni va en la misma tabla: exterior sheathing sobre CFMF y acabado normalmente de otro trade. Dentro de la banda del canopy conviven cosas que NO son nuestras (vent de stucco, luminaria lineal, línea de viga, columnas): cada elemento length y angosto se resuelve siguiendo su key note hasta la punta y buscando su código en la leyenda, no por su width ni por un markup ajeno. De las columnas es nuestro el enclosure (framing + sheathing); el steel, el bollard, las tuberías y el stucco no.

**PASO 7 — Cálculos.** Studs campo = (long. pulg ÷ O.C.) + 1, sin deducir aberturas. Adicionales: terminación=1, intersección=1, esquina=1, abertura= jamb studs según el Header Schedule del proyecto + cripple studs sobre el header — SUMAR, no advertir. Clips = studs_total × líneas bracing × 2. Track: 2 runs siempre, renglones separados, verificación LF÷length=2 (en wall de doble row, 4 runs y la verificación da 4). Board: bruto = long×alto×faces×layers, menos aberturas. Mantener tipos de board separados. Tile en wall o ceiling → sustrato SIEMPRE cementitious backer board (criterio de oficio, prevalece sobre lo dibujado; anota la diferencia). Bracing: líneas = FLOOR(height÷espaciamiento). Waste salvo indicación distinta: Metal 15%, Board 6%, por tipo por separado. Mostrar NETO/WASTE/COMPRA en columnas. Redondear a unidad de venta. No aplicar waste a [PENDIENTE] ni a fasteners.

**Elementos cerrados tipo caja (column wrap, pier, chase).** Hay TRES perímetros distintos y cada material toma el suyo: el de acabado (la dimension impresa), el del sheathing (acabado − 2 × thickness de acabado por lado) y el de framing / FOS (sheathing − 2 × thickness de sheathing por lado). El cierre de layers es la verificación: el perímetro de framing derivado tiene que coincidir con la dimension FOS impresa en el detalle. Track = 2 runs del perímetro de framing. Sheathing SF = perímetro de sheathing × height. Studs: 1 por esquina siempre; los de campo solo si la face libre entre esquinas supera el spacing — si no los pide el spacing pero el oficio los quiere para juntas de sheathing y apoyo de lath, va como [DERIVADO] declarado, con la alternativa mínima valorizada al lado.

**PASO 8 — Verificación adversarial propia** (ver su sección) antes de entregar. Después, el checklist ANTES DE ENTREGAR punto por punto.

## FORMATO DE ENTREGA

1. Datos generales del edificio. 2. Mapa de hojas con fuente de cada dato. 3. Specs Div05/09 con referencias. 4. Tipos de partition con materiales por layer. 5. Tabla de walls (tipo/ubicación/long/height/materiales — composición COMPLETA en cada fila, nunca "igual que arriba"). 6. **Bandas de abertura — bulkheads y sills (tabla separada).** 7. Ceilings GWB (tabla separada). 8. Soffits (tabla separada). 9. Cruce MEP. 10. Tabla de alcance. 11. Cierres de 8 secciones por eje. 12. Registro de dimension strings. 13. Resumen NETO/WASTE/COMPRA por eje. 14. Lista de pendientes con motivo y a quién pedir.

Marca cada número [CONFIRMADO] / [DERIVADO] / [PENDIENTE]. Los ejes se presentan separados, nunca fusionados.

## CLARIFICATIONS PARA EL BID (nunca omitir)

Sección "Clarifications & Exclusions": 1) material existente vs nuevo con hoja citada; 2) patch and repair como allowance con la nota citada textual; 3) exclusiones explícitas con motivo (storefront=Div08, to remain, otra división, vendor, future tenant, luminarias=Div26, gabinetes, EIFS nombrado explícito, corner guards que van con FRP/wallcovering); 4) gypsum en faces opuestas, aclarando cuál aplica; 5) condiciones V.I.F. con su nota citada; 6) pendientes que afectan el precio; 7) RFIs, cada uno con su delta valorizado cuando el dato faltante mueve cantidad (rótulos de elevación cruzados, tags sin definición en el schedule, espesores que no cuadran, perfiles sin designación); 8) criterios de oficio que el plano no dibuja pero el precio sí lleva (cement board bajo tile, length del blocking de un wall stop que el plano no ubica, alternativa de clip contra soldadura), declarados uno por uno para que el cliente pueda tacharlos; 9) finish level supuesto y control joints.

## ANTES DE ENTREGAR, VERIFICA

**Fuentes y lectura.** ¿Recorrí las fuentes de la Regla #3 antes de declarar algo faltante? ¿Validé cruzado? ¿Los segmentos suman el total? ¿Elevación correcta con las cuatro evidencias? ¿Verifiqué con tres rasgos si la planta ampliada está girada o espejada? ¿Mapa de hojas desde el índice, con el rótulo confirmado en cada title block y guardado page_index → hoja? ¿Revision log? ¿Demolition Plan separando existente de nuevo? ¿Busqué el material por lo que ES y no por su nombre comercial? ¿Reabrí la imagen en este turno en vez de citar de memoria? ¿Afirmé algo que no se distingue con certeza?

**Tipos y detalles.** ¿Abrí el detalle de CADA tipo, no solo su fila, y medí sus layers por geometría? ¿Barrí la hoja de Partition Types buscando detalles sin tag (bulkheads, jambs, transiciones)? ¿Leí la nota de construcción del detalle antes de tomar calibre y spacing del schedule estructural? ¿Decodifiqué la designación SSMA antes de decir que falta el calibre? ¿Busqué el calibre en TODO el set y usé el del plano cuando alguna hoja sí lo nombra? ¿Agoté las cuatro fuentes de derivación antes de abrir un RFI? ¿Declaré por tipo qué va arriba (slip track, track fijo o cap track) con su detalle citado? ¿Verifiqué si el detalle acota el gap de deflection? ¿Si el wall es de doble row, conté DOS juegos de track y DOS rows de studs?

**Barrido y geometría.** ¿Comprobé si el PDF es vectorial antes de medir por píxeles, y validé el método contra espesores de schedule y dimensions impresas? ¿Re-derivé la banda POR TAG? ¿Las dos faces de cada banda son de lineweight ≥ 1.1? ¿Uní las runs colineales completas y por END CAP, no por tolerancia ciega? ¿Medí los walls a trazos por la línea completa y revisé quiebres del patrón? ¿Seguí la línea guía con criterio de parada? ¿Abrí en imagen cada candidato sin leader antes de descartarlo? ¿Emparejé cada dimension con su propia línea de dimension y leí sus ticks por sus extremos reales? ¿Dedupliqué por identidad de banda? ¿Resté las porciones de los otros tags en un run compartido? ¿Todo length no explicado tiene dueño? ¿Conté el tipo también por su grafía, incluidos rectángulos sin hatch y furring? ¿Cuantifiqué el tipo POR DEFECTO por barrido geométrico y no por tags? ¿Cada tag del censo terminó en un wall cuantificado? ¿Recorrí TODO el plano buscando cada repetición del tag? ¿Circulé CADA ubicación y me detuve a esperar confirmación (o lo dejé en "Revisar en la mañana")? ¿Usé la numeración del barrido, sin renumerar?

**Las dos bandas de cada abertura (SUPER REGLA).** ¿Abrí las CUATRO elevaciones interiores de cada cuarto antes de cerrar sus walls? ¿Hice las DOS restas en CADA abertura y por face — `ceiling − header` arriba y `sill − piso` abajo? ¿Deduje del board solo la ABERTURA NETA (`header − sill`) y no el rectángulo de piso a ceiling? ¿Busqué el detalle propio del bulkhead y el de JAMB/SILL? ¿Cuantifiqué el METAL de las dos bandas —box beam, jamb studs, studs cortos arriba, cripple studs abajo, sill track, track arriba y abajo, bead, molding— y no solo su board? ¿Las puse en renglones propios, con el width de la abertura como length?

**Alturas.** ¿Llevé la height de board POR FACE? ¿Las faces que dan a un cuarto open to structure van al deck? ¿Leí el RCP cuarto por cuarto siguiendo el leader de cada tag de ceiling? ¿Conté todos los marcadores de B.O.D. de la hoja y usé el extremo alto de la zona en pendiente? ¿Armé el B.O. deck layer por layer desde los detalles estructurales? ¿Busqué la nota de fire tape sobre el ceiling, y si no está, lo declaré?

**Aberturas, MEP y blocking.** ¿Conté (no solo advertí) studs adicionales, jambs y cripples, con el Header Schedule del proyecto? ¿Cargué a algún wall los openings que mueren entre dos tipos y los excluí en la pasada del otro? ¿Saqué las aberturas exteriores de los storefront frames (R.O. + sill + knee walls) y cuantifiqué los returns? ¿Registré las hojas por el fondo arquitectónico y verifiqué el signo del offset antes de cruzar MEP? ¿Exigí que el cruce sobresalga por fuera de las dos faces, y busqué también los ductos dibujados partidos? ¿Abrí en imagen cada penetración para leer su rótulo? ¿Evalué cada penetración individualmente contra el umbral? ¿Revisé el Hardware Group de cada door para el wall stop? ¿Leí las notas ALFABÉTICAS de hoja además de los key notes? ¿Abrí el detalle de cada tipo de fixture y distinguí blocking surface-mounted de en-partition?

**Cálculo y cierre.** ¿Verifiqué track LF÷length = 2 y reporté bottom y top separados EN TODAS las tablas? ¿Recalculé clips con el total? ¿Conté líneas de bracing? ¿Apliqué 15% y 6% sobre neto, por tipo? ¿Mostré NETO/WASTE/COMPRA? ¿Separé tipos de board? ¿Separé ceilings de soffits, abrí TODOS sus detalles, conté todas sus faces y su anchorage al deck? ¿Cuantifiqué el soporte CFS de cada wall colgado? ¿Verifiqué el cierre de layers de cada elemento tipo caja contra su dimension FOS? ¿Cerré cada eje con las 8 secciones y declaré qué face cerré? ¿Cada cantidad tiene su desglose pieza por pieza y su sello?

**Alcance y entrega.** ¿Confirmé existente/nuevo cruzando las 4 fuentes? ¿Clasifiqué alcance antes de cuantificar? ¿Excluí la luminaria y el gabinete y cobré el framed opening y el blocking? ¿Localicé y cité la insulation aunque vaya excluida? ¿Seguí el key note hasta su punta antes de aceptar el rótulo de un markup ajeno? ¿Si el framing es de wood, lo separé como INFO Div 06 con su RFI? ¿Marqué [CONFIRMADO]/[DERIVADO]/[PENDIENTE]? ¿Listé lo que falta en vez de inventarlo? ¿Entregué cada ambigüedad real como RFI con su delta? ¿Escribí Clarifications & Exclusions completa, incluidos los criterios de oficio que el plano no dibuja? ¿Entregué en SU formato y en inglés, con el waste en celda aparte y el tamaño de hoja como parámetro, nombrando lado por lado lo que lleva cada face?

**Método e imágenes.** ¿Rendericé todo desde la copia sin `/Annots`? ¿Reabrí cada imagen marcada y confirmé que la marca cae sobre el elemento correcto? ¿Entregué el paquete completo de imágenes del tipo antes de cuantificar? ¿Marqué cada wall como un TRAMO y no como un punto, con su número oficial y su LF, azul con tag y rojo sin tag? ¿La tabla de bandas salió de los cierres sellados y no de memoria? ¿Corrí `verif_bandas.py` sobre TODAS las bandas antes de dibujar, y expliqué por escrito cada `>>>`? ¿Marqué las cajas como CAJA y los bulkheads sobre el opening, no sobre las faces vecinas? ¿El total de cada hoja marcada coincide con el LF sellado de ese tipo? ¿Guardé cada entregable en la carpeta del proyecto en cuanto quedó verificado, y le dije dónde? ¿Usé la escala efectiva del recorte reducido? ¿El cache de render distingue de qué PDF salió cada PNG? ¿Comparé contenido y no md5 antes de dar por distintas dos copias del set? ¿A los agentes les pedí REFUTAR y recomprobé yo lo que devolvieron? ¿Corrí la verificación adversarial propia y apliqué solo lo que sobrevivió? ¿Guardé en memoria toda regla nueva y toda orden de método en el MISMO turno, y le entregué el protocolo actualizado?

---


## ⛔ SÚPER REGLAS DE LAS ADENDAS — texto completo, copiado de su adenda

Estas reglas inviolables viven en su adenda, pero se copian aquí completas para que estén
a la vista en todo momento, sin depender de abrir un archivo.

### Desde `referencias/adenda_v38.md`

### ⛔ SUPER REGLA INVIOLABLE

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
| `A02.01` / `A04.01` | el length (48.047 ft) y la posición |
| `D/A09.22` | el fondo, y lo confirma contra la planta |
| `7/A09.26` | la composición y los datums `T/STUD [valor retirado E24]` − `B/STUD [valor retirado E24]` |
| `7/S5.20` | el perfil `362S137-33` y el 16" O.C., que **ningún detalle de canopy rotula** |

Y de paso la cadena resolvió un pleito abierto hacía días: los `3'-1 3/4"` de D/A09.22 y los
`2.467 ft` medidos en planta **nunca estuvieron en conflicto**. Localizando los dos ticks de
la dimension en el vector del PDF (x=2154.12 y x=2379.84, escala 72 pt/ft calibrada contra tres
datums) se ve que la dimension va de **eje 8** a **fascia**, no de face de wall a fascia. La
diferencia son exactamente los **8"** que 7/A09.26 imprime arriba. Dos caminos independientes,
a dos escalas distintas, a una milésima de pie.


### Desde `referencias/adenda_v39.md`

### ⛔ REGLA INVIOLABLE

Instrucción permanente de Rodolfo, textual:

> "en todas tus respuestas, todos los nombres de materiales, herramientas, componentes,
> procesos, abreviaturas y vocabulario técnico pertenecientes a los trades de drywall y metal
> frame deben escribirse en inglés. No los traduzcas al español.
>
> El texto general, explicaciones, instrucciones o conversación pueden estar en español, pero
> los términos de la disciplina siempre deben permanecer en inglés."

<!-- GLOSARIO:INICIO -->
Términos que van en inglés (los que él listó): **drywall · sheetrock · metal frame ·
steel stud · track · runner · joist · drywall screw · joint compound · tape · corner bead ·
mud · taping · finishing · framing · layout · header · sill · blocking**.

Prohibidas explícitamente: *tablaroca · panel de yeso · perfilería metálica · poste metálico ·
canal*, salvo que él las pida.
<!-- GLOSARIO:FIN -->

**Si hace falta aclarar un término:** primero el término en inglés y, si hace falta, una breve
explicación en español entre paréntesis. El término principal siempre en inglés.

**Aplica en todo formato:** listas, tablas, presupuestos, especificaciones, procedimientos,
correos, descripciones, el chat y los entregables.

### Por qué, dicho una vez para no volver a discutirlo

<!-- GLOSARIO:INICIO -->
El material se pide, se compra y se instala en inglés. El proveedor cotiza `5/8" gypsum board`,
el instalador pide `board`, la purchase order dice `metal stud`. Un take-off que dice "tablero"
obliga a traducir mentalmente en cada renglón, y en esa traducción es donde se pide lo que no
era.
<!-- GLOSARIO:FIN -->

---


### Desde `referencias/adenda_v41.md`

### ⛔ REGLA INVIOLABLE

> **El nombre del room en la `ubicación` de un wall NO es la fuente de la height de sus faces.
> La fuente es el ceiling tag de la BANDA en la que cae cada face, y la banda se delimita viendo
> dónde se corta la retícula del RCP y dónde hay un wall que la separe.**

Y su recíproca, que es la que cuesta más:

> **Cuando la `ubicación` y las `caras` no coinciden, ninguno de los dos lados manda por sí solo.
> Hay que ir al plano.**

---


### Desde `referencias/adenda_v42.md`

### ⛔ REGLA INVIOLABLE

> **Un `[CONFIRMADO]` tiene que CITAR una printed dimension. Si el texto de su fuente no trae
> ninguna printed dimension, la afirmación no se puede comprobar — y una afirmación que no se puede
> comprobar no es un `[CONFIRMADO]`: es `[DERIVADO]` (y entonces escribe la operación) o
> `[PENDIENTE]`.**

Y la que la destapó:

> **Una ELEVACIÓN no es una HEIGHT.** S2.20 imprime una elevación (`B.O.D. EL. [valor retirado E24]`);
> la height del stud es esa elevación **menos** el datum `T/SLAB 0'-0"`. Que las dos cifras
> coincidan pasa sólo porque el datum vale cero. **Una resta sigue siendo una resta**, así que
> es `[DERIVADO]` y tiene que escribir la cuenta.


## ÍNDICE DE REGLAS POR ARCHIVO DE `referencias/`

Qué contiene cada archivo. Si una tarea toca uno de estos temas, abre su archivo.

- **`herramientas.md`** — CONTRATO DE LAS HERRAMIENTAS
  - planmark.py — marcado verificado sobre la hoja
  - closer.py — compuerta de cierre de wall
  - zoom.py — recorte de alta resolución con escala verificada
  - dimensions.py — cadenas de dimension impresas
  - registro2.py — registro entre hojas por el fondo arquitectónico
  - mep.py — cruce de MEP por geometría
  - tagband.py — barrido por tag sin presuponer el thickness
  - auditor.py — compuerta de BARRIDO
  - verif_bandas.py — compuerta del DIBUJO
  - wallgeom.py — motor de medición (EN VALIDACIÓN)
  - arranque.py — Paso 0 mecánico en un solo comando
- **`adenda_v26.md`** — ADENDA v26 — 28-sep-2026 · lo que salió de la auditoría adversarial de BofA Broomfield
  - LA AUDITORÍA ADVERSARIAL ES UN PASO DEL CIERRE
  - REGLA — El perfil de stud se lee del PARTITION SCHEDULE, nunca de una tabla propia
  - REGLA — Ninguna line item se cae en silencio: el generador FALLA si sobra una
  - REGLA — Sumar por prefijo, nunca sobrescribir
  - REGLA — Cuando se corrige una cantidad, se corrige el TEXTO el mismo turno
  - REGLA — Doble conteo: se elige UNA fuente y la otra lista sin sumar
  - REGLA — Alturas line items: leer los tramos de la operación del cierre
  - REGLA — Un material distinto va en su propio renglón de compra
  - REGLA — El track se compra por TAMAÑO
  - REGLA — La dimension impresa dice dónde está el TOPE, no cuánto mide la banda
  - REGLA — Juntas de control: si el set no las rotula, se EXCLUYEN con motivo, nunca se omiten
  - REGLA — Una abertura con sill obliga a su sill track, y la compuerta lo exige
  - REGLA — Cada abertura con SU PROPIO width
  - REGLA — Un hueco de EQUIPO se mide en el detalle del equipo, no en el claro de la planta
  - REGLA — Medir lo no acotado dentro de un detalle: derivar la escala y VALIDARLA primero
  - REGLA — Registro de cadenas: los tramos suman el total y los claros salen redondos
  - REGLA — El título y la leyenda del plano marcado no se salen del recuadro
  - REGLA — Lo que no se resuelve, se declara; no se inventa
- **`adenda_v27.md`** — ADENDA v27 — 28-sep-2026 · la compuerta de SIGNIFICADO de columna
  - De dónde salió
  - REGLA — Una columna de resumen no se entrega sin una recomputación independiente
  - La pregunta que hay que hacerle a cada columna
  - Qué verifica la compuerta (`verif_columnas.py`)
  - REGLA — Una compuerta que nunca se ha visto fallar no sirve
  - REGLA — El decimal raro se investiga, no se redondea
- **`adenda_v28.md`** — ADENDA v28 — 28-sep-2026 · la compuerta de COBERTURA
  - De dónde salió
  - No era error: los studs de abertura
  - El hueco de verdad
  - REGLA — Un elemento que no aparece en ninguna lista no es "sin nada": es SIN REVISAR
  - REGLA — Un `continue` por tipo de geometría es una bomba
  - Cómo se cerró
  - Probado viéndolo fallar
- **`adenda_v29.md`** — ADENDA v29 — 28-sep-2026 · la compuerta del LIBRO
  - De dónde salió
  - Los cinco errores de dinero, todos de la misma raíz
  - REGLA — La familia del material manda sobre el waste y sobre el length de compra
  - REGLA — Un PENDIENTE se escribe PENDING, nunca como 0 ni omitido
  - REGLA — Clasificar por el ENCABEZADO del renglón y por PALABRA COMPLETA
  - REGLA — Auditar un libro SIN RECALCULAR reporta decenas de fallos fantasma
  - La compuerta: `verif_libro.py`
  - Lo que sigue sin resolverse, y se dice
- **`adenda_v30.md`** — ADENDA v30 — 28-sep-2026 · barrido de ZONAS HÚMEDAS
  - De dónde salió
  - REGLA — Censo por CUARTO, cruzando TRES fuentes
  - Lo que salió
  - REGLA — Una nota que nombra DOS aparatos hay que leerla como DOS walls
  - REGLA — El censo de zonas húmedas lleva compuerta de cobertura
  - REGLA — El W.R. es RECLASIFICACIÓN, no board nuevo
- **`adenda_v31.md`** — ADENDA v31 — 28-sep-2026 · NINGÚN CAMBIO ESTÁ TERMINADO HASTA QUE EL EXCEL SE REGENERA
  - De dónde salió
  - El riesgo que cubre
  - REGLA
  - COMPUERTA DE VIGENCIA — `verif_vigencia.py`
  - UNA SOLA PUERTA DE SALIDA — `entregar.py`
  - Corolario para el ORDEN PERMANENTE
  - Error de la propia compuerta, cazado en su primer arranque
- **`adenda_v32.md`** — ADENDA v32 — 29-sep-2026 · TODO NOMBRE DE MATERIAL SE ESCRIBE EN INGLÉS
  - De dónde salió
  - REGLA
  - Glosario
  - COMPUERTA — `verif_idioma.py`
  - Tres cosas que costaron y no hay que repetir
  - Para tocar un cierre YA SELLADO — `traducir_materiales.py`
  - Los documentos históricos se CONGELAN, no se traducen
- **`adenda_v33.md`** — ADENDA v33 — 29-sep-2026 · EL JUEGO DE PLANOS MARCADOS ES AUTOMÁTICO
  - De dónde salió
  - REGLA — No se pregunta, no se ofrece, no se espera
  - Qué compone el juego, sin faltar ninguno
  - El NOMBRE dice qué contiene
  - Dónde se guardan
  - Sigue valiendo todo lo de antes
- **`estructura_carpeta.md`** — ESTRUCTURA DE CARPETA, EN CADA PROYECTO
  - Una sola versión vigente, no una pila de versiones
- **`adenda_v34.md`** — ADENDA v34 — 1-oct-2026 · COMPUERTA DE COBERTURA DE DETALLES
  - De dónde salió
  - REGLA — No se cierra un proyecto sin haber abierto cada detalle de cada hoja que se usó
  - Lo que encontró en su primera run
  - REGLA — Una cita que una máquina no puede leer no se puede auditar
  - Cómo se usa en un proyecto nuevo
- **`adenda_v35.md`** — ADENDA v35 — 1-oct-2026 (noche)
  - El índice se genera, no se escribe (`hoja_indice.py`)
  - Tres reglas nuevas, cada una de un error cometido hoy
  - La carpeta de entrega es el espejo, y tiene que estar completa
  - Sin shell en su PC, el diff se hace por TAMAÑO
- **`adenda_v36.md`** — ADENDA v36 — 2-oct-2026 · LA CADENA DE DETALLES SE SIGUE HASTA EL FINAL
  - Las cuatro partes de la regla
  - Qué lo originó
  - Las compuertas
  - Dos bugs propios al escribir la compuerta, los dos de normalización
- **`adenda_v37.md`** — ADENDA v37 — 3-oct-2026 · LOS 42 CALLOUTS, CERRADOS
  - 1. El RFI del parapet se CIERRA — el infill de `11/S5.10` SÍ se ubica
  - 2. Una layer que las secciones NO rotulan y los detalles SÍ
  - 3. Dos bugs de compuerta — las dos miraban menos de lo que creían
  - 4. Trampa operativa: `| head` mata el script antes de que escriba
  - 5. El furring de columna es un LAZO CERRADO
  - 6. Lo que la cadena destapó, en line items
- **`adenda_v38.md`** — ADENDA v38 — 4-oct-2026 · EL ORDEN DE TRABAJO: PLANO → CADENA → TOTAL → EXCEL
  - ⛔ SUPER REGLA INVIOLABLE
  - La herramienta: `cadena_detalles.py`
  - Lo que la columna destapó el primer día
  - CORRECCIÓN DEL MISMO DÍA — dos errores que la columna destapó en cuanto se miró
- **`adenda_v39.md`** — ADENDA v39 — 7-oct-2026 · EL VOCABULARIO DEL TRADE VA EN INGLÉS, SIEMPRE
  - ⛔ REGLA INVIOLABLE
  - CÓMO SE HACE CUMPLIR, QUE ES LA PARTE QUE NO SE OLVIDA
  - LOS TRES ERRORES QUE DESTAPÓ APLICARLA (y las reglas que dejan)
- **`adenda_v40.md`** — ADENDA v40 — 7-oct-2026 · LA REGLA DEL INGLÉS SE VERIFICA, NO SE PROMETE
  - ⛔ LO QUE PASÓ, y por eso existe esta adenda
  - LA COMPUERTA: `verif_respuesta.py`
  - POR QUÉ HACEN FALTA DOS LISTAS, Y NO UNA
  - LOS FALSOS AMIGOS QUE SALIERON AL CORRERLO SOBRE EL TEXTO DE VERDAD
  - ALCANCE: también el generador, no sólo la salida
  - TERCER TRINQUETE
- **`adenda_v41.md`** — ADENDA v41 — 8-oct-2026 · EL ROOM DE CADA FACE SE VERIFICA, NO SE HEREDA
  - ⛔ REGLA INVIOLABLE
  - LOS CUATRO CASOS QUE LA ORIGINARON, el mismo día
  - LA COMPUERTA: `verif_caras.py` (paso 12 de 17)
  - EL OTRO HALLAZGO DEL DÍA: A1 #4, `[DERIVADO]` → `[CONFIRMADO]`
- **`adenda_v42.md`** — ADENDA v42 — 8-oct-2026 · UNA ELEVACIÓN NO ES UNA HEIGHT, Y UN `[CONFIRMADO]` TIENE QUE CITAR SU PRINTED DIMENSION
  - ⛔ REGLA INVIOLABLE
  - CÓMO SE ENCONTRÓ (armando el HANDOFF, no revisando cantidades)
  - POR QUÉ `verif_confirmado` NO LO CAZABA — el hueco más grande que tuvo esa compuerta
  - LA COMPUERTA NUEVA: `verif_coherencia.py`
  - UNA NORMALIZACIÓN DUPLICADA SE DESINCRONIZA SOLA
  - EL MAPA DE HOJAS SE CRUZA CON DOS FUENTES, Y SE DICE DÓNDE NO CUADRAN
  - EL REGISTRO DE LO QUE EL USUARIO CONFIRMÓ NO EXISTÍA COMO ARCHIVO
- **`adenda_v44.md`** — ADENDA v44 — 10-oct-2026
  - Barrido de los 95 detalles sin abrir, y el error que cometí en medio
  - REGLA 44.1 — BARRIDO POR TAG DE SCHEDULE, NO POR WALL
  - REGLA 44.2 — UN ROLL-UP POR CLAVE NO ES UN INVENTARIO DE CONTENIDO
  - REGLA 44.3 — UNA COMPUERTA NO SE DA POR BUENA HASTA VERLA FALLAR
  - Lo que el barrido movió, ya sellado
- **`adenda_v45.md`** — ADENDA v45 — 10-oct-2026 (tarde)
  - Cobertura de detalles a cero, atraso de [CONFIRMADO] a cero, y el mapa de adyacencia
  - REGLA 45.1 — UNA CITA QUE PRUEBA QUE EL MATERIAL VA NO PRUEBA CUÁNTO HAY
  - REGLA 45.2 — UN EXTREMO QUE EL MAPA NO RESUELVE NO ES UN EXTREMO LIBRE
  - COBERTURA DE DETALLES: 90 PENDIENTES → 0
  - Estado al cierre
- **`adenda_v46.md`** — ADENDA v46 — 11-oct-2026
  - La regla de waste, ampliada, y los tres renglones que destapó
  - REGLA 46.1 — UNA REGLA ESCRITA COMO DOS LISTAS DEJA HUECOS; ESCRITA COMO PARTITION, NO
  - REGLA 46.2 — DOS CELDAS QUE SIGNIFICAN LO MISMO SON DOS FUENTES DE VERDAD
  - Lo que NO lleva waste, y por qué — explícito para no volver a preguntarlo
  - RFIs
- **`adenda_v47.md`** — ADENDA v47 — 11-oct-2026
  - Lo que se corrigió, y por qué importa
  - REGLA 47.1 — UNA COMPUERTA QUE CUENTA POR RENGLÓN NO PUEDE VER LA CERCA
  - El test, y la prueba de que falla sin el arreglo
  - El caso que casi quedó decorativo (y cómo se cazó)
  - Lo que se pagó, no lo que se eximió
  - Estado de la entrega

# ADENDA v48 — 11-oct-2026 · UNA SOLA CARPETA DE HERRAMIENTAS, Y TODO LO NUEVO VUELVE A ELLA

## Lo que se corrigió, y por qué importa

Las 117 herramientas vigentes no vivían en `_herramientas/`: estaban dentro de la carpeta de
un proyecto (`Bank of America - Broomfield/.../2 - Take-Off Claude/Herramientas`), y en
`_herramientas/_herramientas_py/` quedaba un kit viejo del 26-sep con versiones distintas de
`closer.py`, `arranque.py` y `planmark.py`. Un take-off nuevo que siguiera la regla al pie de
la letra habría copiado las versiones viejas. Se consolidó todo en **`_herramientas/py/`**
(122 archivos: 117 de BOA + `zoom.py`, `registro2.py`, `cotas.py`, `tagband.py` rescatados del
kit viejo + `gdrive_fetch.py`) y el kit viejo se eliminó.

## REGLA 48.1 — LAS HERRAMIENTAS SE TOMAN SIEMPRE DE `_herramientas/py/`

> Fuente única: `JC HUNTER PROJECTS/_herramientas/py/` (PC:
> `C:\Users\jesra\My Drive\JC HUNTER PROJECTS\_herramientas\py`). Antes del Paso 0 de
> todo take-off o back-check: listar esa carpeta, copiar TODAS sus herramientas al área de
> trabajo, leer `_herramientas/00_INDICE_HERRAMIENTAS.md` y correr los `test_*.py`. Si un test
> no pasa, esa herramienta no se usa y se reporta.

Nunca se toma una herramienta de la carpeta de un proyecto, ni de una sesión anterior, ni se
regenera de memoria mientras exista en `py/`.

## REGLA 48.2 — TODA HERRAMIENTA NUEVA O CORREGIDA SE COPIA A `py/` EN EL MISMO TURNO

> Al crear una herramienta nueva, o al corregir una existente con su test en verde, se sube a
> `_herramientas/py/` **en el mismo turno**, con su `test_*.py` si lo tiene. Una herramienta
> que solo existe en la carpeta del proyecto o en el contenedor se pierde.

- **Nueva:** se sube a `py/` con su nombre definitivo.
- **Corregida:** se sube la versión nueva a `py/` y la anterior se MUEVE (no se borra) a
  `_herramientas/py/_anteriores/` con sufijo de fecha (`closer_2026-10-11.py`). Nunca quedan
  dos archivos con el mismo nombre en `py/`.
- **Índice:** se actualiza `_herramientas/00_INDICE_HERRAMIENTAS.md` con qué se agregó o
  corrigió, cuándo y por qué; el índice anterior va a `_anteriores/`.

## REGLA 48.3 — CIERRE DE SESIÓN: NINGUNA HERRAMIENTA QUEDA FUERA

> Antes de entregar, se compara la lista de `.py` usados en la sesión contra `py/` (nombre y
> tamaño). Todo lo que falte o difiera se sube según 48.2, y la entrega lo declara en una
> línea: *"Herramientas: N nuevas, M corregidas subidas a `_herramientas/py/`"* (o *"sin
> cambios"*).

---

# ADENDA v49 — 13-oct-2026 · LAS ENTREGAS VAN ORGANIZADAS POR PROYECTO

## Lo que se corrigió, y por qué importa

Las entregas de varios proyectos caían todas sueltas en una sola carpeta `Claude outputs`
(la vieja ya tenía unos 27 archivos de BOA mezclados de distintas fechas). Con la automatización corriendo
proyectos sin supervisión, eso las revolvería. Además, la service account `takeoff-reader`
solo puede crear archivos dentro de una **unidad compartida** (una cuenta de servicio no tiene
espacio propio en un Drive personal), así que la carpeta de entregas se movió a la unidad
compartida **JC HUNTER PROJECTS**.

## REGLA 49.1 — UNA CARPETA POR PROYECTO, SIEMPRE EN LA UNIDAD COMPARTIDA

> Toda entrega se guarda en la unidad compartida **JC HUNTER PROJECTS → `Claude outputs`**
> (folder id `1UReOABlgJPIkGLe8-nRO6U-6i7xpKoIc`), **una carpeta por proyecto**, nunca suelta
> en la raíz de `Claude outputs` ni en la carpeta de los planos. Estructura fija:
>
> ```
> Claude outputs/
>   <nombre exacto de la carpeta del proyecto en Projects>/
>     Take-off/         Excel, reporte, lista "para revisar en la mañana", RFIs
>     Planos marcados/  PDFs e imágenes circuladas
>     Back-check/       reporte y Excel corregido del back-check
> ```
>
> Las carpetas se crean con `gdrive_fetch.py mkdir <padre> <nombre>` (si ya existe la reusa)
> y los archivos se suben con `gdrive_fetch.py put`, que nunca sobrescribe: una corrida nueva
> del mismo proyecto lleva sufijo de fecha y hora en el nombre (`_2026-10-13_0215`). Los bid
> sets se siguen LEYENDO de `JC HUNTER PROJECTS/Projects`; ahí solo se renombra `LISTO.txt`
> → `PROCESADO.txt`. La entrega final dice la ruta exacta de la carpeta del proyecto.

---

# ADENDA v50 — 13-oct-2026 · LIBRO DE PARTIDAS, RESPALDO POR SESIÓN Y COMPUERTA DE ENTREGA

## De dónde sale

Del artículo de Anthropic *"Effective harnesses for long-running agents"*. Un take-off grande no
cabe en una sola sesión, y cada sesión nueva arranca sin memoria de la anterior. Las dos fallas
que el artículo documenta son exactamente las nuestras: (1) hacer todo de golpe y quedarse sin
contexto a la mitad, con el trabajo a medias y sin anotar; (2) que una sesión posterior vea mucho
avanzado y declare "terminado" con partes sin hacer. Su remedio es una lista maestra creada al
inicio, con todo en "falla", que después **solo se puede marcar, nunca editar ni borrar**, y que
el agente guarda en JSON porque así es menos probable que la reescriba.

Lo que ya teníamos cubría partes: barrido por tag, compuertas de cobertura por subsistema,
sellos, manifiesto del Excel, back-check. Faltaba **una sola lista de TODO el proyecto que el
código proteja**, el **respaldo entre sesiones** y la **compuerta final** sobre esa lista.

## REGLA 50.1 — EL LIBRO DE PARTIDAS SE CREA ANTES DE CUANTIFICAR

> Al cerrar el PASO 0 y la pausa del barrido (o su punto de revisión en modo sin preguntas),
> se crea `registro.json` con `registro.py crear`. Un renglón por cada: wall del barrido
> (numeración fija), tag del censo, detalle de la cadena (cada burbuja y cada detalle que un
> detalle llama), zona húmeda del censo por cuarto, cielo, soffit, abertura con header/sill y
> cruce MEP. Todos arrancan `pendiente`.

- Cada renglón: `id` (la numeración fija del proyecto), `tipo`, `ubicacion` (hoja + grid o
  N/HOJA), `fuente` (tag, schedule, nota, detalle que lo llamó).
- Lo que aparece después (un detalle llamado por otro, un wall sin tag hallado por grafía) se
  **agrega** con `registro.py agregar`. Agregar sí; editar o borrar, nunca: el registro guarda
  una huella sha256 por renglón y una cadena de todo el libro, y `leer()` lanza
  `RegistroRoto` si alguien lo tocó por fuera.

## REGLA 50.2 — SOLO SE CAMBIA EL ESTADO, CON EVIDENCIA

> `pendiente → verificado` exige evidencia en la nota (N/HOJA, imagen re-verificada, sello del
> cierre). `pendiente → pendiente_rfi` exige el número de RFI y el motivo. `pendiente_rfi →
> verificado` cuando llega la respuesta. `verificado` no se revierte. Si un verificado resulta
> mal, se agrega un renglón nuevo de corrección que apunte al anterior; el historial queda.

## REGLA 50.3 — UNA UNIDAD A LA VEZ, Y RESPALDO AL CERRARLA

> Se trabaja **un partition type (o un sistema: cielos, soffits, exteriores) a la vez**: barrer,
> cerrar, sellar, marcar sus renglones. Al cerrarlo, la sesión sube a
> `Claude outputs/<proyecto>/_progreso/` un respaldo con nombre de fecha y hora
> (`progreso_2026-10-14_0315.zip`: `registro.json`, cierres sellados, `PROGRESO.md`).
> `PROGRESO.md` dice en 5 líneas: qué se cerró, qué verificó, qué sigue, qué quedó raro.

## REGLA 50.4 — RUTINA DE ARRANQUE DE CADA SESIÓN

> Toda sesión que retoma un proyecto: (1) baja el respaldo MÁS RECIENTE de `_progreso/`;
> (2) `registro.py estado`; (3) lee `PROGRESO.md`; (4) re-corre los tests de las herramientas y
> la verificación de los sellos ya emitidos ANTES de tocar algo nuevo; (5) toma la siguiente
> unidad pendiente. Si (4) falla, lo primero es arreglar eso.

## REGLA 50.5 — COMPUERTA DE ENTREGA

> `registro.py entregable` debe salir en 0 antes de entregar: **cero renglones `pendiente`**.
> Los `pendiente_rfi` sí salen, y cada uno aparece en la lista PARA REVISAR EN LA MAÑANA y en
> la sección de RFIs con su delta. La entrega pega la salida de `registro.py estado`.

No hay modo "entregar con advertencias": si la compuerta no pasa, no hay entrega; hay un
respaldo en `_progreso/` y un resumen de qué falta.

---

# ADENDA v51 — 13-oct-2026 · EL SKILL SE REORGANIZA EN NIVELES

## Qué cambió

El SKILL.md pasó de 3,047 líneas (258 KB) a un archivo central más `referencias/` con 23
archivos (herramientas + adendas v26–v47 + estructura de carpeta). Se carga en tres niveles:
nombre y descripción siempre; este archivo cuando se pide un take-off; cada archivo de
`referencias/` en el momento que marca la tabla de LECTURA OBLIGATORIA, y TODOS antes del
PASO 8. Las súper reglas ⛔ de v38, v39, v41 y v42 quedan copiadas completas aquí arriba.

## Cómo se verificó que no se perdió nada

Con código, no a ojo: cada renglón no vacío de la v50 aparece en el nuevo SKILL.md o en algún
archivo de `referencias/`, contando repeticiones; cada archivo de `referencias/` está nombrado en
la tabla de lectura; el frontmatter (`name`, `description`) es idéntico.

## REGLA 51.1 — UNA ADENDA NUEVA SE ESCRIBE EN ESTE ARCHIVO; SE MUEVE CUANDO YA NO ES OPERATIVA

Las reglas nuevas se agregan aquí abajo como siempre. Cuando una adenda deja de ser de uso diario,
se mueve a `referencias/adenda_vNN.md`, se agrega su fila a la tabla de LECTURA OBLIGATORIA y su
entrada al índice, y si trae una regla ⛔ se copia completa a SÚPER REGLAS. Nunca se mueve una
adenda sin esas tres cosas.

---

# ADENDA v52 — 14-oct-2026 · LISTA FIJA DE ALCANCES Y HERRAMIENTAS SIN DATOS DE OTRO PROYECTO

## Por qué (error real, prueba automática BOA 13-oct-2026)

La prueba automática se entregó con `registro.py entregable` en 0 y aun así le faltaban alcances
COMPLETOS: ceiling suspension (furring channel, carrying channel, hanger wire, ceiling track), el
canopy (soffit, fascia, CANOPY-COL) y el exterior FRT plywood sheathing (dejado como "alternate").
Calificación contra el take-off del usuario: 24.9%. El back-check confirmó con hoja+detalle que la
referencia tenía razón. Causa: el registro solo tenía lo que Claude VIO; lo que nunca vio no estaba
en la lista y la compuerta no podía echarlo de menos.

## ⛔ REGLA 52.1 — LISTA FIJA DE ALCANCES ANTES DE CUANTIFICAR

En el PASO 3, junto con el registro, y SIEMPRE (con o sin preguntas):
1. `alcances.py escanear <bid_set.pdf> <work>/alcances_escaneo.json` — busca en el texto del set las
   palabras clave de 24 alcances fijos (ALC-01..ALC-24) y anota en qué hojas aparece cada uno.
2. `alcances.py renglones ...` + `registro.py agregar ...` — los 24 entran al registro como pendientes.
3. Cada ALC se cierra de UNA de tres formas:
   - CUANTIFICADO: su cantidad está en el Excel (NET > 0 en su familia de material).
   - `NO APLICA: <hoja> <motivo>` — citando la hoja; si el escaneo encontró el alcance en el set,
     la nota tiene que citar UNA DE ESAS HOJAS (hay que ir a verla antes de descartarlo).
   - `pendiente_rfi` con su RFI (sale en PARA REVISAR EN LA MAÑANA).
4. Un renglón del Excel que diga PENDING / ALTERNATE / EXCLUDED **no cuenta como cantidad**. Lo que
   el set pide en el contrato base va en la base; un alternate se cotiza APARTE, además de la base.
5. Compuerta antes de entregar, junto a `registro.py entregable`:
   `alcances.py compuerta <registro.json> <escaneo.json> <Excel final>` → tiene que dar `ALCANCES OK`.
   ALC-12 (ceiling suspension) exige TODAS sus partes. No hay entrega con NO ENTREGABLE.

## REGLA 52.2 — CARPETA DE TRABAJO POR VARIABLE, NUNCA /home/claude/boa

Las herramientas de `py/` leen su carpeta de trabajo de `TAKEOFF_WORK` y la de salida de
`TAKEOFF_OUT` (antes estaban fijas en `/home/claude/boa` y `/mnt/user-data/outputs`, que en la nube
no existen o traen datos de BOA). Al empezar cada take-off: `export TAKEOFF_WORK=<carpeta del
proyecto>/work TAKEOFF_OUT=<carpeta del proyecto>/out` y crear las dos.

## REGLA 52.3 — `py/` SOLO TIENE HERRAMIENTAS GENERALES

- Las herramientas escritas para UN proyecto (los `cerrar_<tipo>.py`, `marca_*`, `hoja_<zona>.py`,
  `resellar_*`, sus tests con datos del proyecto) viven en `py/_proyectos/<nombre del proyecto>/`
  y NUNCA se usan en otro proyecto: traen las respuestas de ese proyecto adentro.
- Las que están en validación viven en `py/_en_validacion/` (hoy: `wallgeom.py`).
- Al cerrar un take-off (regla 48.3), las herramientas nuevas se clasifican: general → `py/`;
  del proyecto → `py/_proyectos/<proyecto>/`.
- Tests generales que se corren en el PASO 0: `test_closer.py`, `test_registro.py`,
  `test_verif_caras.py`, `test_verif_confirmado.py`, `test_verif_respuesta.py`.
  `test_alcances.py` y `test_eval_takeoff.py` piden archivos de referencia: son del calificador.
- Calificador de pruebas (`eval_takeoff.py`) y lista de alcances (`alcances.py`): en `py/`.

## ⛔ REGLA 52.4 — UN SOLO FORMATO DE EXCEL: `plantilla_excel.py`

Por qué: en las pruebas del 13/14-oct cada corrida armó un Excel distinto (hojas y columnas
diferentes), y así no se puede revisar ni calificar igual. Desde v52:
1. El take-off escribe sus datos en `takeoff.json` (formato en el encabezado de `plantilla_excel.py`;
   `plantilla_excel.py ejemplo` da uno para copiar). Cada wall lleva `source` = DETALLE/HOJA y
   `status` = CONFIRMADO / DERIVADO / PENDIENTE. Las cantidades van NET; el waste lo pone el Excel.
2. `plantilla_excel.py validar takeoff.json` tiene que dar FORMATO OK.
3. `plantilla_excel.py armar takeoff.json <Excel final>` arma SIEMPRE las mismas hojas: Inputs,
   Partition Takeoff, Material Summary, Pending Items, PARA REVISAR EN LA MANANA, Alcances.
4. Prohibido armar el Excel a mano o con otro script. Un renglón PENDING / ALTERNATE / EXCLUDED
   no va en Material Summary (el validador lo rechaza).
5. La compuerta de alcances (52.1) se corre contra ESE Excel.

---

# ADENDA v53 — 14-oct-2026 · CRITERIOS DEL ESTIMADOR (aprobados uno por uno por el usuario)

Origen: el arbitraje de la prueba #2 de BOA (ARBITRAJE.md, 14-oct) encontró 8 partidas donde el plano
no decide y cada estimador cuenta distinto. El usuario aprobó estos criterios el 14-oct-2026. Son
OBLIGATORIOS en todo take-off y en todo back-check; una excepción solo la decide el usuario.

## ⛔ REGLA 53.1 — METAL TRIM
Incluye: corner bead en toda esquina exterior de gypsum board; L-bead / J-bead (casing bead) donde el
board termina contra otro material (storefront, door frames sin casing propio, retornos de jamb);
shadow molding / reveal solo donde se dibuja; gypsum edge trim en light slots. NO incluye accesorios
de stucco / plaster (PT-xx): son de otro trade.

## ⛔ REGLA 53.2 — CONTEO DE STUDS (todo tamaño)
Por wall: ROUNDUP(largo / O.C.) + 1; + 1 en cada esquina y cada intersección en T; + 2 en cada jamb de
cada abertura (king + jack), altura completa; cripples arriba del header y abajo del sill al mismo O.C.
con su largo real. LF = studs × altura completa (zona con pendiente: el lado más alto). Column wraps y
piers se cuentan por SU detalle, nunca como wall normal.

## ⛔ REGLA 53.3 — MEDIDA NO IMPRESA
Altura (u otra medida) no impresa: se usa la opción que lleva MÁS material, [DERIVADO], con RFI y el
delta de la otra opción. Stud sin tamaño: el del wall donde se apoya o el del detalle más parecido del
set, [DERIVADO] + RFI. Las dos van a PARA REVISAR EN LA MAÑANA. Nunca en silencio.

## ⛔ REGLA 53.4 — BRACING TYPICAL
Un detalle de bracing marcado TYPICAL aplica a TODOS los stud walls del set (interiores, G/G1, canopy
framing, walls sobre storefront) salvo que el propio detalle excluya. Filas = una cada 4'-0" de altura
sin contar la de abajo ni la de arriba (ej. 13 ft → 3 filas). LF = filas × largo del wall.

## ⛔ REGLA 53.5 — EXTERIOR GYPSUM SHEATHING DEL PARAPET
Va en todo el parapet que cubre su detalle, incluido el que está sobre storefront. Altura de deck a
T.O. parapet, lado más alto si hay pendiente. Retornos dibujados sin cota se incluyen (regla 53.3).

## ⛔ REGLA 53.6 — HEADER / BOX BEAM
Largo = R.O. de cada abertura + 8" de apoyo por lado (R.O. + 1'-4"), salvo que el detalle de S5.xx
imprima otro apoyo. Un header por cada abertura dentro de wall con framing (doors, ventanas interiores,
storefront con wall arriba = box beam). Cada abertura con SU ancho, nunca promedio.

## ⛔ REGLA 53.7 — SILL TRACK
Toda abertura con sill: ventanas, glazing, ATM / drive-up, pass-through, aberturas de ducto con framing.
Doors no. Largo = R.O. + 8" por lado.

## ⛔ REGLA 53.8 — CLASIFICACIÓN: MANDA EL DETALLE
Si un elemento tiene burbuja de detalle propia, se cuenta con ese detalle aunque haya un tag cercano; si
tag y detalle se contradicen, gana el detalle + RFI. Walls sin tag = el tipo de la nota general de la
planta (BOA: nota A de A02.01, A1). Las caras de un chase húmedo se miden cara por cara.

## REGLA 53.9 — HALLAZGOS DEL ARBITRAJE (protocolo)
1. FRP: la altura impresa se mide SOBRE el cove base (BOA: 5'-0" sobre 6" base, A-D/A08.01).
2. Acoustical sealant sigue el detalle de CADA partition type (2×, 4× o 0 lados); el exterior y el
   parapet NO llevan acoustical sealant salvo que su detalle lo diga.
3. "SEALANT AT BASE OF GYPSUM" exterior es su PROPIO renglón (no acoustical).
4. Glass mat sheathing y FRT plywood de column wraps / piers salen de sus detalles de pared exterior:
   se buscan siempre (en BOA los omitió una prueba).
5. Moisture resistant board va donde lo diga la nota (BOA: chase detrás de toilet y lavatory).

# ADENDA v54 — 15-oct-2026 · ERRORES DEL ARBITRAJE DE LA PRUEBA #4 (BOA)

Origen: el árbitro de la prueba #4 (ARBITRAJE.md, 15-oct) revisó 5 familias contra el plano. Ganó la
prueba en 1, la referencia en 1, y ninguna en 3. Cada error es ahora una regla. OBLIGATORIAS en todo
take-off y back-check.

## ⛔ REGLA 54.1 — FRAMED OPENINGS DE FIXTURES
Todo recessed fixture dentro de framing (GWB ceiling, soffit, canopy de CFMF exterior) lleva framed
opening = 2 × largo del schedule + 2 ends por fixture. El ancho de los ends sale del cutsheet; si no
está impreso, queda [PENDIENTE] + RFI. Largo: luminaire schedule (BOA: E00.01). Conteo: tags del
lighting plan (BOA: E02.01). PROHIBIDO medir el largo en el RCP. Antes de cerrar, barrer TODOS los tipos
de la familia (BOA: UU1…UU6, R-11A/B/C/CE) y listar cada tag con su imagen circulada.
Error que la originó: la prueba #4 midió el canopy en el RCP (477.6 LF), le faltaron UU1, UU5, UU6 y
los 2 R-11A; el schedule da 686 LF solo en el canopy.

## ⛔ REGLA 54.2 — TRACK POR POSICIÓN + DUPLICADOS
Bottom, top y deflection track van en renglones SEPARADOS. Un callout "TOP & BOT." genera DOS renglones,
nunca uno dentro de la familia bottom track (BOA: 11/S5.10, 600T125-54).
54.2b: dos renglones de la misma familia con el mismo neto y la misma cita = duplicado. Se corrige
antes de entregar (BOA: canopy track 480.82 LF contado dos veces con 7/A09.26).

## ⛔ REGLA 54.3 — MATERIAL DEL BLOCKING
El material lo dice el detalle. "STUD BLOCKING 362CR22" / blocking at edge of gypboard (BOA: 4/S5.20)
= METAL, renglón propio "Stud blocking 362CR22". FRT / FRTW solo donde el detalle lo rotule. Barrer
también las elevaciones interiores (artwork, monitores, TV) y las notas de hoja (millwork, toilet
accessories, wall stops). Parapet blocking BOA = 4/A09.26.

## ⛔ REGLA 54.4 — ACOUSTICAL SEALANT CORRIDA POR CORRIDA
Tabla por partition type: corridas top / bottom × caras, leída de CADA detalle. Cantidad = Σ largo ×
corridas. PROHIBIDO usar el punto medio de un rango. Línea dibujada sin rótulo = RFI con su delta
(BOA: base de G sin rótulo, −201.34 LF; "SEALANT" del office front 9/A12.01, +90 LF).

## ⛔ REGLA 54.5 — SHEATHING SOLO DONDE SE ROTULA
Cada capa de sheathing (glass mat, exterior gyp, FRT plywood) va solo donde un detalle la rotule.
Sobre storefront manda el head detail (BOA: 2/A09.26 = steel header, SIN glass mat). Los descuentos de
aberturas del Material Summary deben ser IGUALES a los del Partition Takeoff, renglón por renglón; se
comparan antes de entregar. Deck con pendiente → B.O.D. promedio del tramo, por fachada (nunca juntar
dos fachadas en un número). Nota: 53.5 (parapet exterior gyp sheathing sobre storefront) sigue igual;
54.5 solo quita el glass mat donde el head detail no lo rotula.

## ⛔ REGLA 54.6 — LA CITA DEBE SER EL DETALLE QUE TIENE LA NOTA
Cada N/HOJA debe coincidir con el título del detalle que contiene la nota citada. Antes de entregar se
abre cada cita y se confirma. Errores encontrados: 6/A09.26 (STOREFRONT BASE) citado para el parapet
blocking (correcto 4/A09.26); 7/A09.26 (SIDE CANOPY) citado para el glass mat (correcto 5 y 3/A09.26).

# ADENDA v55 — 15-oct-2026 · ERRORES DE LA PRUEBA #5 Y DE SU ARBITRAJE (BOA)

Origen: (a) los 5 agentes adversariales de la prueba #5 encontraron errores y alcances sin cuantificar;
(b) el árbitro de la prueba #5 (ARBITRAJE.md, 15-oct) revisó 8 familias contra el plano. Cada error es
ahora una regla. OBLIGATORIAS en todo take-off y back-check. Los criterios 53.x aprobados por el usuario
siguen mandando: si una regla de aquí choca con un 53.x, gana el 53.x.

## ⛔ REGLA 55.1 — EL CRÍTICO DE COMPLETITUD SE CORRE SIEMPRE
Antes de entregar, un agente revisa hoja por hoja (incluidas las que nadie citó) buscando alcances sin
cuantificar. En la prueba #5 encontró 7 alcances completos fuera: roof step (4/A02.02), coiling grille
(2-4/A08.21), heads del vestíbulo (A12.10), ATM (5,6/A08.11), roof hatch y ladder, lockers, CSR plywood
(9/A12.08). Lista de hojas nunca citadas = punto de revisión obligatorio.

## ⛔ REGLA 55.2 — UN ELEMENTO SE CUENTA UNA SOLA VEZ
Antes de agregar framing o blocking desde un detalle, buscar si esa ubicación ya es un muro con tag o ya
está en otro renglón. Si lo es, una sola fila (la prueba #5 contó dos veces los jambs del coiling grille,
que eran las cajas C1 ya contadas, y dos veces el CSR soffit: 9/A12.08 y 10/A09.33 son el mismo
elemento). Un jog del perímetro tampoco se suma dos veces: cada tramo se escribe (desde, hasta) y la
suma de tramos debe cerrar con el perímetro.

## ⛔ REGLA 55.3 — PARAPET
- Extensión de un parapet alto (T.O. PARAPET 2): se lee en las CUATRO elevaciones, no solo en la sección
  (BOA: la torre corre de G a D).
- Infill (11/S5.10): bay por bay entre HSS posts = 1 stud a cada lado de cada post + @16" dentro del bay;
  nunca @16" continuo + 2 por post.
- Sheathing del parapet, cara roof side: LF de cara interior × (T/STUD − B.O.D.). T.O. PARAPET es el tope
  del coping, no del sheathing.
- Deck con pendiente: altura promedio del tramo, no la máxima.

## ⛔ REGLA 55.4 — MEDIDAS DE ABERTURAS Y ESPESORES SE MIDEN, NO SE TECLEAN
El R.O. de una door se mide entre jambs en el vector, nunca se teclea. Un tramo sin tag se clasifica
por su espesor medido contra el schedule antes de aplicar la serie. Una franja de ceiling sin tag sigue
la retícula del RCP del cuarto vecino, no el nombre del cuarto más cercano.

## ⛔ REGLA 55.5 — ACOUSTICAL SEALANT EN DOORS
Las corridas de abajo se descuentan en cada door R.O. (no hay sealant cruzando el vano).

## ⛔ REGLA 55.6 — MOISTURE RESISTANT BOARD
Va solo en las caras donde se apoya un toilet o lavatory según el plano ampliado y su nota (BOA: nota
F/A08.01 = solo el chase C1). Se desglosa muro por muro.

## REGLA 55.7 — HERRAMIENTAS (ya corregidas el 15-oct)
- alcances.py ahora rotula cada página con el número del title block (letra más grande). Antes salía la
  hoja más citada (A02.01 salía "A9.22").
- familias.py (calificador) ahora tiene familia propia de purlin y de stud blocking metálico.

## NOTA — PROPUESTA NO APLICADA
El árbitro propuso "studs extra solo si un detalle los pide". Choca con el criterio 53.2 aprobado por el
usuario (+1 por esquina/T, +2 por jamb). No se aplica; queda para que el usuario decida.

# ADENDA v56 — 15-oct-2026 · ERRORES DE LA PRUEBA #6 Y DE SU ARBITRAJE (BOA)

Origen: prueba #6 (skill v55) y su árbitro (ARBITRAJE.md, 15-oct, 8 familias). Cada error es ahora una
regla. OBLIGATORIAS en todo take-off y back-check. Los criterios 53.x aprobados por el usuario siguen
mandando. Decisiones del usuario del 15-oct ("haz lo mejor para el proyecto") quedan anotadas.

## ⛔ REGLA 56.1 — REGISTRO ANTES DEL PRIMER NÚMERO
La medición exploratoria se permite, pero `registro.py crear` se corre al terminar el PASO 3 y ANTES de
escribir el primer número al modelo (refuerza 50.1; la #4 y la #6 lo hicieron al revés).

## ⛔ REGLA 56.2 — NOTAS GENERALES ESTRUCTURALES ANTES DE LOS DETALLES S5
Antes de S5.xx se leen las notas generales S1.xx ("LIGHT GAUGE STEEL FRAMING"): gauge mínimo, O.C. en
esquinas, deflection clips. Si S1.xx y un detalle o schedule NO coinciden en gauge / O.C., va a RFI con
las DOS cantidades; el take-off lleva la de MÁS material (53.3) marcada [DERIVADO] (BOA: S1.11 nota 5
600S162-54 @16" y @12" a 6 ft de esquinas vs 7/S5.20 600S137-33 @16").

## ⛔ REGLA 56.3 — UNA CAPA DE DETALLE DE BASE O BANDA VA SOLO DONDE SE DIBUJA
Una capa que solo aparece en un detalle de base o de banda se cuenta solo donde ese detalle la dibuja.
Antes de extenderla a todo el muro, se revisa el detalle con zoom de 300 dpi o más y se circula la
evidencia. BOA (decidido 15-oct): 5/8" glass mat solo de T/SLAB a T/BASE 0'-6" (5/A09.26, 9/A09.27) y en
la banda del canopy (3 y 7/A09.26); arriba, el FRT plywood bonded polyiso va directo al stud.

## ⛔ REGLA 56.4 — DONDE TERMINA EL STUD DEL MURO
Si el detalle estructural (BOA 10/S5.10) corta el muro en un deflection track bajo la viga, los studs del
muro terminan ahí. El parapet es infill aparte (11/S5.10) en TODO el perímetro.

## ⛔ REGLA 56.5 — UN MURO NUEVO SE UBICA CON IMAGEN ANTES DE SUMARLO
Un muro nuevo que mide lo mismo que uno ya contado es el mismo muro. Todo muro nuevo (sobre todo de torre o
parapet) se ubica con imagen circulada en la planta o el roof plan antes de sumarlo (BOA: no existen muros
de torre en grid 4 ni en grid D; la #6 sumó 408.7 SF de sheathing en ellos).

## ⛔ REGLA 56.6 — SEALANT = BEADS DIBUJADOS
Las corridas de sealant son los beads dibujados en cada detalle. Un símbolo igual al que tiene rótulo en
otro detalle del mismo set SÍ es sealant (BOA: G/G1 en 5/A12.01). El sealant de base exterior no cruza
storefronts ni doors. Un tipo cuyo detalle no dibuja bead no lleva sealant (BOA: F, 12/A12.01).

## ⛔ REGLA 56.7 — BULKHEAD DE OFFICE FRONT
La altura sale del HOLD impreso en la elevación interior (BOA 2/A11.01 "8'-0 1/2" HOLD TYP. FROM SLAB"),
no del ceiling de la oficina.

## REGLA 56.8 — STUD BLOCKING SIN UBICACIÓN
Si el detalle de blocking es NTS y no da ubicación (BOA 4/S5.20 "PROVIDE BLOCKING AT THE EDGE OF
GYPBOARD"), se lleva una fila en la junta horizontal del board donde el muro es más alto que el largo del
board, + RFI con las opciones (BOA: 466 LF, exteriores + G/G1).

## REGLA 56.9 — TRIMS SIN CALLOUT
El metal trim que no tiene callout en ningún detalle pero que pide el criterio 53.1 va en su propio renglón
"metal trim (criterio 53.1)". El gypsum edge trim se nombra "metal trim - gypsum edge trim" para que entre
en su familia.

## REGLA 56.10 — HERRAMIENTAS (corregidas el 15-oct)
`plantilla_excel.py validar` ya acepta citas con letra (C/A09.21, H/A09.23).

# ADENDA v57 — 15-oct-2026 · 4a COMPUERTA: BITÁCORA DE TOOLS OBLIGATORIAS

## De dónde salió
En las pruebas BOA #1–#6 la sesión a veces NO corrió las tools que el skill exige (registro creado
tarde; closer.py, planmark.py, verif_* y entregar.py saltados) y aun así entregó. Las 3 compuertas que
había revisaban el RESULTADO, no si el TRABAJO se hizo. Una regla escrita se salta a las 2 de la mañana;
esta compuerta no.

## ⛔ REGLA 57.1 — TODA TOOL SE CORRE POR `bitacora.py run`
`python3 bitacora.py run <tool.py> [args...]` corre la tool y anota en `bitacora.jsonl` (carpeta de
trabajo, o `$BITACORA`) el rc y el sha256 de cada archivo que tocó. Cada renglón lleva el hash del
anterior: editar la bitácora a mano rompe la cadena y la compuerta lo rechaza. Una tool corrida por
fuera de `bitacora.py run` NO CUENTA. Los scripts propios que importan `closer` o `planmark` también se
corren por `bitacora.py run` (así cuenta que se sellaron cantidades y se marcó evidencia).

## ⛔ REGLA 57.2 — BACK-CHECK ANOTADO
El back-check (subagente independiente) escribe su informe (.md, ≥200 bytes) y se anota con
`python3 bitacora.py backcheck <informe.md> <Excel final>`. Si el Excel cambia después, el back-check
ya no vale y se repite.

## ⛔ REGLA 57.3 — 4a COMPUERTA ANTES DE ENTREGAR
Junto a `registro.py entregable` y `alcances.py compuerta`, se corre al FINAL:
`python3 bitacora.py compuerta <takeoff.json> <registro.json> <Excel final>` → tiene que dar
`BITACORA OK`. Exige, todo con rc=0 en su ÚLTIMA corrida:
1. `arranque.py` (Paso 0)
2. `alcances.py escanear`
3. `registro.py crear` — y ANTES del primer `plantilla_excel.py armar` (regla 56.1)
4. un script que importa `closer.py` (cantidades selladas)
5. un script que importa `planmark.py` (evidencia circulada)
6. `plantilla_excel.py validar` sobre el takeoff.json VIGENTE
7. `plantilla_excel.py armar` del takeoff.json vigente al Excel vigente
8. `registro.py entregable` sobre el registro vigente
9. `alcances.py compuerta` sobre el registro y el Excel vigentes
10. back-check anotado sobre el Excel vigente
"Vigente" = mismo sha256 que el archivo tiene ahora. Si algo cambió después, se vuelve a correr.
No hay "entregar con advertencias": si no da BITACORA OK, no se entrega; se corrige y se repite.
Probada fallando en 13 casos (`test_bitacora.py`, regla 44.3).

## Herramientas (en `py/`)
`bitacora.py`, `test_bitacora.py`. `familias.py` vuelve a `py/` (faltaba; el calificador y
`alcances.py` la importan). `test_eval_takeoff.py` 16/16.

# ADENDA v58 — 16-oct-2026 · ARBITRAJE DE LA PRUEBA #8 (studs, track, sill, framed openings, blocking, unidades de compra)

## De dónde salió
Prueba BOA #8 (v57): 60.7 % de materials, la mejor hasta hoy. Ocho familias seguían MAL. El arbitraje
contra el plano (carpeta "ARBITRAJE prueba 8 (2026-10-15)", ARBITRAJE_8.md, 18 imágenes circuladas)
decidió cada una. Las reglas siguientes son generales; BOA aparece solo como ejemplo.

## ⛔ REGLA 58.0 — UNIDADES DE COMPRA (plantilla_excel.py corregido)
`plantilla_excel.py` (py/, test_plantilla 18/18) ya no compra mal:
- todo stud vendido por stick lleva `"cut_ft"` (largo típico de corte) en takeoff.json; sin él NO valida.
  Piezas = studs de ese largo ÷ INT(stock / cut_ft). Un stud de 12–15 ft sale 1 por stick de 20 ft;
- las hojas se cuentan por el AxB de `selling_unit` ("4x8 sheet" = 32 SF; "4x12" = 48 SF);
- batt, Level 5 y todo lo que se compra por SF: `selling_unit` "SF" (sin AxB, sin "sheet");
- piezas de schedule (EA/PCS con net <= 20, p. ej. access panels) van sin waste; `"waste_pct"` lo fija si hace falta;
- sealant se vende por tubo/LF, nunca "piece 10 ft".

## ⛔ REGLA 58.1 — UN STUD POR POSICIÓN
Nunca stud completo y cripple en la misma posición. Dentro del R.O. de una door: 0 field studs (solo
king + jack + cripples arriba). Bajo un storefront de slab a head: NO hay studs; sobre un steel header
van cripples a largo real (BOA 2/A09.26). Los field studs dentro de un R.O. se restan.

## ⛔ REGLA 58.2 — EL NOMBRE DEL RENGLÓN DECIDE LA FAMILIA DEL TRACK
- Track de fascia, soffit, CSR y bulkhead horizontal → "Ceiling / soffit track", nunca bottom/top.
- El track adicional de 2/S5.20 (o equivalente) se llama "Additional head track", no "Top track".
- Sobre un steel header (storefront) va track abajo y arriba de los cripples: suma a bottom y a top.
- Un framed head (p. ej. grille/coiling door, 4/A08.21) lleva su track abajo y arriba.

## ⛔ REGLA 58.3 — SOFFIT JOISTS: UN TRACK EN CADA EXTREMO
Los joists de soffit/canopy llevan track en sus DOS extremos, cada uno medido sobre su propia línea
(la del muro y la interior de la fascia). No se usa el largo de la línea del muro dos veces.

## ⛔ REGLA 58.4 — SILL / HEADER DE RECESSED, CABINETS Y FIRE DAMPERS
Barrer las leyendas (toilet accessories, FEC, M-sheets) por TODO elemento RECESSED en stud wall y
todo fire damper / ducto en muro: cada uno lleva header + sill track a su ancho impreso + 2 × 1'-4".
Sin tamaño impreso: 2'-0" [PENDIENTE] + RFI. Un elemento que cabe en el stud bay (p. ej. Knox box
7" W) o que es surface/bracket NO lleva sill.

## ⛔ REGLA 58.5 — FRAMED OPENINGS EN GWB CEILINGS
Incluyen TODOS los air devices (slot diffusers por sección), luminarias y access panels dentro de un
GWB ceiling. Penetraciones MEP en MUROS no van aquí: van a header + sill (53.6/53.7) o refuerzo de stud.

## ⛔ REGLA 58.6 — BLOCKING EN LF, CON SU MATERIAL ROTULADO
Todo blocking va en LF (nunca en SF), en la familia de su material: "FRT blocking" solo donde el
detalle rotula FRT/FRTW (54.3), con los plies dibujados (2 plies = 2 × LF). Una nota que dice
"PROVIDE BLOCKING" sin material → metal stud blocking 362CR22 (4/S5.20 o equivalente) + RFI de material.
Barrer: parapet, office front, wall stops, millwork, toilet accessories, equipment, artwork y los
detalles típicos de head (p. ej. 8/A12.10, 3/A08.21).

## ⛔ REGLA 58.7 — CEMENT BOARD BAJO TODO TILE
Standing order del estimador: cementitious backer board bajo cualquier tile, cove base de tile incluido
(LF de cove base × alto de la banda). Va en su propio renglón, nunca sumado al FRP.

## Herramientas
`plantilla_excel.py` y `test_plantilla.py` nuevos en py/. Calificador: rangos_v5 (referencia corregida
por el arbitraje #8) en Referencias (examen).

# ADENDA v59 — 16-oct-2026 · ARBITRAJE DE LA PRUEBA #9 (largos netos, bandas, parapet, esquinas, piers, purlin)

## De dónde salió
Prueba BOA #9 (v58): 76.8 % de materials (rangos_v6). 3 familias MAL y 9 CERCA. El arbitraje contra el plano
(carpeta "ARBITRAJE prueba 9 (2026-10-16)", ARBITRAJE_9.md, 19 imágenes) encontró 3 causas generales:
(a) largos de muro que entran en el muro perpendicular, en el door frame o se duplican;
(b) reglas de conteo que el agente interpreta a su manera (parapet, esquinas a 12", extremos de doble fila);
(c) un revisor adversarial que contradijo una regla ⛔ y se aplicó.
Las reglas son generales; BOA aparece solo como ejemplo.

## ⛔ REGLA 59.1 — PURLIN / ANCLAJE AL DECK ES REGLA DE TRACK, NO DE SOFFIT
Todo track que se fija al deck (top track de partitions a deck, soffits, bulkheads, roof step, heads) se clasifica
por su dirección contra el flute. Dirección del flute = perpendicular a los miembros que soportan el deck en el roof
framing plan, por zona. Donde corre paralelo y el set dibuja purlin/anclaje especial (BOA 10/A09.33), cantidad =
LF de track × (largo de pieza ÷ spacing de fasteners impreso) [DERIVADO] (BOA 1'-6" / 2'-0" = 0.75). Doble fila =
una pieza. Detalle VIF → CRITERIO + RFI con la otra dirección. (En v58 esta regla estaba en el párrafo de Soffits y
la #9 solo la aplicó al soffit: 18 LF en vez de 214.)

## ⛔ REGLA 59.2 — BANDAS EN JUNTAS: ALTO DEL DETALLE, LF DE LA LÍNEA DE MURO, MISMA BANDA EN TODAS LAS FILAS
El alto de una banda (glass mat, sheathing, blocking) sale de las elevaciones impresas en el DETALLE de la junta
(T/STUD, B/STUD), nunca de T/ y B/ del elemento en la elevación exterior. El LF es la línea de muro tocada, por
fachada, UNA vez (una pieza "extension" no repite una línea ya contada). La misma banda (LF × alto) se usa en
todas las filas que la comparten (glass mat +, nailbase −).

## ⛔ REGLA 59.3 — LARGO NETO DE MURO
Cada muro termina en la cara del muro perpendicular que lo recibe; el tramo de un tipo con tag sigue su poché/hatch
dibujado; nunca entra en un door frame ni en el espesor de otro muro. Por cada línea, la suma de segmentos = largo
entre caras extremas. Prohibido unir "end-cap a end-cap". Una cota impresa del cuarto manda sobre el vector.

## ⛔ REGLA 59.4 — PARAPET INFILL: FÓRMULA CERRADA POR BAY
Bays = ROUNDUP(L / spacing máx de posts). Studs por bay = 2 + max(0, ROUNDUP((bay − 0.6)/O.C.) − 1). Sin stud
exterior en los posts extremos salvo que el infill continúe. Se calcula por fórmula, nunca "2/post + 3/bay".

## ⛔ REGLA 59.5 — O.C. REDUCIDO EN ESQUINAS REEMPLAZA, NO SUMA
"@ 12" O.C. within X ft of corners" (S1.xx): las posiciones dentro de esa zona van a 12", el resto a 16". Un muro
más corto que la zona = ROUNDUP(L/1.0) + 1. Nunca +2 fijos por esquina.

## ⛔ REGLA 59.6 — PIERS / PILASTERS CON DETALLE PROPIO: CADA CAPA, CON COTAS IMPRESAS
Barrer cada material dibujado en el detalle del pier (stud exterior, stud interior, nailbase, plywood de jamb,
board). Caras = cotas impresas del detalle; studs por 53.2. Prohibido "~N" escalado.

## ⛔ REGLA 59.7 — EXTREMOS DE MURO DE DOBLE FILA
+1 stud por fila solo en esquina/T dibujada. Un extremo libre contra vendor frame/storefront lleva lo que dibuje
su jamb detail (BOA 10/A12.01: 1 METAL STUD de cierre por muro, no uno por fila).

## ⛔ REGLA 59.8 — 58.4 ES COMPUERTA, Y UN ADVERSARIAL NO DEROGA UNA REGLA ⛔
Header/sill se rechaza si el ancho impreso ≤ claro del stud bay (14 3/8" @ 16"). Cajas de servicio en muro (ice
maker box, wall hydrant, AV in-wall box, Knox box) sin ancho impreso = dispositivo de stud bay → 0 + RFI, no 2'-0".
Si un revisor adversarial propone algo CONTRA una regla ⛔ vigente, va a PARA REVISAR; NO se aplica.

## ⛔ REGLA 59.9 — MR POR FIXTURE, CARA POR CARA
MR solo en la cara donde se apoya el toilet/lavatory en el plano ampliado. Extremos de chase o caras hacia otro
espacio (alcove, corridor) = board regular.

## ⛔ REGLA 59.10 — PERÍMETROS DE ACABADO (FRP, tile, base): TODAS LAS DOORS DEL CUARTO
Descontar cada door en los muros del cuarto, incluidas las de cuartos vecinos que abren hacia él (janitor dentro de
restroom). Sumar retornos de jogs. El mismo LF alimenta el cement board del cove base.

## ⛔ REGLA 59.11 — NAILBASE / SHEATHING EMPIEZA DONDE TERMINA LA CAPA DE BASE
Si un detalle de base pone otra capa hasta T/BASE, el sheathing continuo se mide desde T/BASE (alto = T/STUD o
B.O.D. − T/BASE). Base + nailbase + banda = alto total, sin traslape.

## ⛔ REGLA 59.12 — SEALANT: CADA TIPO CON SU DETALLE
Las corridas top/bottom de un tipo salen SOLO de su partition detail. Los beads de un detalle de bulkhead o de head
aplican solo a ese elemento, no se propagan al tipo de muro.

## ⛔ REGLA 59.13 — PENDIENTE DE DECK POR MURO
Con dos B.O.D. impresos en una zona con pendiente, la altura de cada muro = interpolación lineal en su extremo alto
(53.2 "lado más alto" es del muro, no de la zona). El delta del RFI se calcula con la misma fórmula.

## REGLA 59.14 — STUD BLOCKING SIN UBICACIÓN: DOS CIFRAS
Con 56.8 se entregan dos valores: (a) exteriores + muros de doble capa; (b) toda cara con board > largo de hoja.
Se carga (b) por 53.3 y RFI con (a).

## Calificador
rangos_v6 (Referencias (examen)): 6" stud 4,905.24 (piers), FRP [valor retirado E24] (door 112), FRT plywood [valor retirado E24] (nailbase
de piers), metal stud blocking hasta [valor retirado E24].

# ADENDA v60 — 16-oct-2026 · ESTABILIDAD: HERRAMIENTAS DETERMINISTAS (studs por nodo, board por face) + reglas 60.x

## De dónde salió
Pruebas paralelas #10A y #10B con el MISMO skill v59: 78.6 % las dos, pero varias familias salieron muy distintas
entre sí (5/8" board 14,302 vs 17,363 SF; 6" stud 5,746 vs 4,893 LF; furring 703 vs 1,450). Causa (ARBITRAJE_10.md):
tres decisiones quedaban al juicio del agente sin herramienta — (1) cómo contar studs extra de juntas, (2) si
"layers" es total o por face, (3) a qué familia va cada track y cuántas corridas tiene un detalle de sección.
Un take-off que cambia de una corrida a otra no es confiable aunque una corrida salga bien. Desde v60 esos
cálculos los hace una HERRAMIENTA; el agente solo declara datos leídos del plano.

## ⛔ REGLA 60.0 — HERRAMIENTAS OBLIGATORIAS (en py/, corridas por bitacora.py run)
- `studs_nodos.py <entrada.json> <salida.json>`: TODOS los studs de walls (6", 3-5/8", 1-5/8", 2-1/2", parapet si
  aplica) salen de aquí. Entrada: walls [id, tag, stud_size, length_ft (neto, 59.3), oc_in, rows, height_ft
  (60.3/59.13), zones (@12" solo en building corners, S1.xx), openings (ro_w_ft, head_ft, sill_ft)] + nodes
  [L / T(branch, through) / X / free / vendor_end]. Cada wall declara sus 2 extremos en nodos; si no, la tool falla.
- `board_caras.py <entrada.json> <salida.json>`: TODO board de walls (5/8" regular, MR, ballistic, 3/8") sale de
  aquí, FACE POR FACE. Entrada: details {layers_per_face, k_panel} + walls [detail, length_printed_ft (cota
  impresa, manda), length_vector_ft, faces (room, board, layers, height_ft, deduct_sf, k_customer)].
- Los números del Excel para esas familias son los totales de esas salidas (se citan las salidas en "source").
- `bitacora.py compuerta` exige que ambas se hayan corrido (si no, NO ENTREGABLE).

## ⛔ REGLA 60.1 — STUDS POR NODO, UNA VEZ
L +1, T +1 al branch, X +2, extremo libre 0, office front contra vendor frame (10/A12.01) +1 TOTAL por wall
(no por row). La zona @12" de S1.11 n.5 va solo a 6 ft de las BUILDING corners declaradas, nunca en cada punta.

## ⛔ REGLA 60.2 — LAYERS POR FACE (ANULA "layers TOTALES" de la sección de partition types)
Cada face lleva sus layers, validadas contra el detalle del tipo (BOA 5/A12.01 G: 2 por face). La cota impresa
manda sobre el vector; diferencia > 0.25 ft = DISCREPANCIA anotada. Prohibido un campo "layers" total.

## ⛔ REGLA 60.3 — ALTURA DE STUD EXTERIOR
= B.O.D. del wall (59.13) − peralte (d) de la perimeter beam de S2.xx cuando el detalle para el stud en un
deflection track bajo la viga (BOA 10/S5.10). Nunca B.O.D.

## ⛔ REGLA 60.4 — SUSTRATO DE CLADDING NO ES FURRING
Hat channel / Z-girt / furring del metal panel, ACM o stucco es del instalador del cladding: renglón EXCLUDED +
RFI con delta; nunca en la familia furring channel (BOA 2/A09.31 EPS-5).

## ⛔ REGLA 60.5 — HEADER LF UNA VEZ POR ABERTURA
Header = (R.O. + 1'-4") × 1. El tipo del header schedule (single/double track, 2-CSJ, box) va en la descripción;
el número de members NO multiplica el LF. Recessed accessories no son header.

## ⛔ REGLA 60.6 — CORRIDAS DE UN DETALLE DE SECCIÓN
En cada detalle de sección (roof step, parapet, soffit, bulkhead) se cuentan las corridas de stud
independientes; cada una lleva su bottom y top track y su bracing (BOA 4/A02.02 roof step: 3 corridas).

## ⛔ REGLA 60.7 — BRACING SOBRE TODAS LAS CORRIDAS
53.4 se calcula sobre la lista completa de corridas verticales: walls, parapet ≥ 4 ft, canopy framing, column
wraps, grille box, vestibule heads, CSR drop — no solo walls.

## ⛔ REGLA 60.8 — FAMILIA DEL TRACK POR ORIENTACIÓN
Studs verticales entre dos tracks → bottom / top (incluye vestibule heads, bulkheads de door, grille head).
Framing horizontal (joists, ceiling, fondo de soffit, fascia box del canopy) → ceiling / soffit track.

## ⛔ REGLA 60.9 — SCHEDULE QUE SE CONTRADICE
Si descripción y catálogo de una fila dan medidas distintas, se carga la que coincide con el dibujo + RFI con el
delta. 53.3 (más material) es solo para medida NO impresa.

## ⛔ REGLA 60.10 — HUECO QUE CABE EN EL MÓDULO
Un recessed ≤ 14 3/8" (stud bay) o ≤ el espaciado del furring en ceiling no lleva framed opening.

## ⛔ REGLA 60.11 — C1 / MR
Partition type sin cota de altura (break line) → board a deck (53.3) con 59.13 por wall; MR solo en las faces del
chase con fixture, sin caras de extremo.

## Calificador
rangos_v7: 6" stud [valor retirado E24]–[valor retirado E24] (la parte interior de la referencia estaba bajo el mínimo de 53.2); MR [valor retirado E24].

# ADENDA v61 — 16-oct-2026 · CAMBIO DE ESTRATEGIA: PROTOCOLO CORTO + takeoff_canon.json + canon.py

## ⛔ REGLA 61.0 — ESTE PROTOCOLO MANDA SOBRE TODAS LAS ADENDAS ANTERIORES
Las pruebas #11A/#11B (v60) bajaron a 55.4/67.9 porque las adendas acumuladas se contradicen y cada corrida
eligió distinto. Desde v61 el agente SOLO mide el plano y lo escribe UNA vez en `takeoff_canon.json`; las
cantidades de toda familia con tool salen de `canon.py` (que corre studs_nodos, board_caras, corridas, headers).
Herramientas OBLIGATORIAS (py/, siempre por `bitacora.py run`; la compuerta las exige):
`canon.py`, `framed_openings.py`, `alcance_filtro.py`, además de arranque, alcances, registro, closer, planmark,
plantilla_excel validar/armar, registro entregable, alcances compuerta y back-check.
Prohibido sumar a mano una familia que tenga tool. Si la tool no cubre un caso: se agrega el caso a la tool con
su test (dato malo que falla) y se anota en PARA REVISAR; nunca se suma por fuera.
Cualquier regla 50.x–60.x que choque con el protocolo siguiente queda ANULADA (ver §9 del protocolo).

> **v66 (2026-10-17):** los textos de PROTOCOLO v61, v62, v64, v65 y v65b se retiraron de este archivo; v67
> reemplaza el PROTOCOLO v66: los reemplaza íntegramente el PROTOCOLO v67 que va al final (E24: sin valores de
> un proyecto de examen).

# PROTOCOLO v67 — Take-off Metal Frame & Drywall (Div. 05 / Div. 09)

Fecha: 2026-10-17 · integración de accesorios y partition types. **REEMPLAZA a PROTOCOLO v66 y anteriores y a
todas las adendas.** Orden de autoridad: §0 Criterios del estimador > este texto > referencias / rangos /
arbitrajes. **Protocolo CIEGO (E24):** reglas generales; los casos de proyectos anteriores se citan solo por
N/HOJA, nunca con cantidad, cota, R.O. ni conteo. Ningún número de este texto es una respuesta.

---

## 0. Criterios del estimador — reglas generales para TODO proyecto

Mandan sobre referencia, rangos y arbitrajes, salvo que el plano diga otra cosa (entonces RFI). Tool entre [ ].

- **E1** Header / box beam: largo de cada pieza = R.O. + 1'-4" (8" de bearing por lado). [headers]
- **E2** Header por PIEZAS: LF = (R.O. + 1'-4") × piezas × qty; piezas = fila del header schedule o 4 en box. [headers, closer]
- **E3** Parapet bay por bay entre posts (decisión del usuario): bays = ROUNDUP(L / post) por straight run;
  studs por bay = MAX(5, 2 + ROUNDUP((bay − 0.6) / oc) − 1): **5 en TODO bay** (2 en posts + 3 intermedios) aunque
  el bay mida menos que el spacing de posts; × (T/STUD − B.O.D.). Run = tramos contiguos de una línea aunque
  cambie la altura; largo en el eje del stud. No es pregunta abierta. [canon `parapet`]
- **E4** Hanger wire en PCS con la altura de cada hanger por room; LF = Σ PCS × altura (DERIVADO). [canon]
- **E5** Ballistic sigue todo el contorno, con jogs y retornos (`ballistic_jogs`, sin walls fantasma). [canon]
- **E6** Board sobre ballistic: misma face, del tope del panel a estructura. [board_caras]
- **E7** Transición con kicker: studs verticales a estructura ADEMÁS del kicker. [canon]
- **E8** Column wraps: bottom + top track = perímetro de faces; face = **cadena FOS impresa completa** (todos
  los eslabones, `fos_chain`); una decisión que usó un solo eslabón cede ante el plano. [corridas, canon]
- **E9** Ceiling track en transición: arriba y abajo. **E10** Bottom track en doors NO se descuenta. [corridas]
- **E11** "BOX HEADER AS NEEDED" SÍ se cuenta; tamaño no impreso = RFI. **E12** Ductos / FD en walls NO se
  enmarcan (sí llevan plate de reinforcement, A2). [headers]
- **E13** Canopy soffit: track en los dos extremos de los joists; fascia y wall medidas por separado
  (`wall_line_ft`), nunca L × 2. [corridas]
- **E14** Ceiling suspendido del RCP = furring, salvo detalle con joists (`joist_source`). [canon]
- **E15** R.O. impreso del estimador manda. **E16** Storefront con lintel HSS / steel en S*: 0 metal stud header.
- **E17** Preguntas al usuario UNA A LA VEZ, con imagen, hojas y opciones con delta; solo criterio comercial.
- **E18** Sill DOUBLE en R.O. > 4'-0"; doors sin sill. **E19** "BOX BEAM OR STEEL FRAMING AS REQUIRED" = metal
  stud box beam. **E20** Todo box = 4 piezas. **E21** La fila del header schedule no se baja. **E22** "CONT. BOX
  BEAM" = un run por frente × 4. [headers]
- **E23** Antes de preguntar, buscar en TODAS las hojas y la spec: si el plano contesta, decidir con N/HOJA +
  imagen; si no, RFI con delta + supuesto declarado. Rangos internos los decide Claude con evidencia.
- **E24** Protocolo, SKILL, referencias/ y tools / tests entregables CIEGOS: sin cantidades, cotas, R.O.,
  conteos ni coordenadas de la referencia de examen; esos tests viven en `tests_arbitraje/`. [test_ciego]
- **E25** Cada capa del sheathing se sigue hasta su remate; nailbase que sube al parapet = T/STUD del parapet. [canon]
- **E26** Walls bajo un miembro S* paran bajo él: `stops_under_beam` o motivo + RFI. [vigas_sobre_walls]
- **Accesorios (§12)** siempre incluidos; ninguno se omite; sin dato = PENDIENTE que bloquea el Excel.
  **Partition types (§13)** con la convención del calificador.

---

## 1. Reglas que siguen siempre

1. **#0 HONESTIDAD DIMENSIONAL.** [CONFIRMADO] cota impresa + N/HOJA · [DERIVADO] operación escrita ·
   [PENDIENTE]. Nunca escalar a ojo. Si no se distingue con certeza, se dice y se para.
2. **DETALLES.** La burbuja manda. Cadena completa: tag → schedule → detalle del tipo → detalles llamados. Leer
   el CUERPO del detalle (notas, leaders, "INVERT DETAIL FOR ..."), no solo el título; si dos detalles traen el
   concepto, se citan los dos. Un detalle es de todo lo que corta. Si no aplica, motivo.
3. **BARRIDO.** Cada tag en TODO el plano; lista numerada + imagen circulada. Antes de "sin tag", buscar leaders
   finos que crucen la band desde un tag cercano. Antes de un RFI "no está en el set", grep del término en todo el
   texto del set. Nota "ALL ..." = recorrer el schedule completo ítem por ítem.
4. **EVIDENCIA VISUAL.** Imagen circulada de todo lo que se afirma; reabrirla antes de entregar. Hojas rotadas:
   `page.rotation_matrix` para medir, `derotation_matrix` para dibujar.
5. **IDIOMA.** Entregable íntegro en inglés; términos del trade en inglés.
6. **EJES.** Nunca dos ejes, fachadas o frentes en un número.
7. **AMBIGÜEDAD = RFI** con delta. Se carga la opción de más material solo si la medida NO está impresa (53.3).
8. **ERRORES.** Error nuevo = regla + test que falle con el dato malo + tool corregida, el mismo turno.
9. **PRUEBAS.** Una prueba NO modifica tools: propuesta (diff + test) en `PARA REVISAR/`; el arbitraje la integra.
10. **REGISTRO.** Un renglón resuelto no se reescribe: `registro.py anexar <id> "<evidencia>"` agrega hojas o
    corrige una cita sin cambiar el estado. Una nota NO APLICA cita TODAS las hojas del escaneo con su motivo.

---

## 2. Pasos (cada uno con `bitacora.py run`)

| Paso | Qué hace el agente | Tool |
|---|---|---|
| P0 | Mapa de hojas, partition schedule, notas generales | `arranque.py` |
| P1 | Lista fija de alcances | `alcances.py escanear` |
| P2 | Registro antes del primer número | `registro.py crear` |
| P3 | Walls (largo neto, cota, line + from/to, band) y nodes | → `walls`, `nodes` |
| P3b | Inventario cerrado (bandas, solapes, apilados, MR, purlin, zonas) | `inventario.py` |
| P4 | Alturas: B.O.D. por wall; walls bajo viga/joist (E26) | `vigas_sobre_walls.py`, `altura_stud.py` |
| P5 | Faces: room, board, layers, altura, aberturas; face con dos rooms = tramos `side` + `length_ft` | → `walls[].faces` |
| P6 | Barrido de aberturas + header schedule con PIEZAS | → `header_schedule`, `sill_rule`, `opening_schedule` |
| P7 | Corridas no-wall con su ELEMENTO (§5); parapets por línea (E3) | → `walls` / `runs` |
| P8 | Ceilings, fachadas + canopies + banda, parapets + nailbase (E25), blocking, plywood, trim | → bloques §4 |
| P8b | Barrido de accesorios: P/M contra walls, ATM, secciones con JAMB RETURN, tags LEVEL 5, access panels | → §4 v67 |
| P9 | `canon.py takeoff_canon.json out/ --fo fo_in.json` (corre accesorios + partition types) | `canon.py` |
| P10 | Fixtures por tag (`tag_counts`, sufijo de circuito normalizado), MEP framed openings, alcance | `contar_tags.py`, `framed_openings.py`, `alcance_filtro.py` |
| P11 | `plantilla_excel.py armar takeoff.json final.xlsx --familias out/familias_out.json` + evidencia | `plantilla_excel.py`, `planmark.py` |
| P12 | Back-check ciego, `test_ciego.py <skill>` y compuerta | back-check, `test_ciego.py`, `bitacora.py compuerta` |

Nunca `| head` / `| tail` detrás de una tool. Prohibido escribir a mano una cantidad de §6; si la tool no cubre
el caso: §1.9 + RFI con delta. `bitacora.py compuerta` se corre directo o por `run` (no se rechaza a sí misma).

---

## 3. Qué es juicio y qué no

Juicio (N/HOJA + imagen): todo lo que se mide o se lee del plano (largos, alturas, R.O., bandas, faces, flute,
filas del schedule, penetraciones, bordes con jamb return, tags LEVEL 5) y los RFIs. Todo lo demás: tool.

## 4. `takeoff_canon.json` — esquema v67

Todo número medido lleva `source` (N/HOJA); constantes `{value, source}`. Esquema completo: docstrings de
`canon.py`, `accesorios.py`, `headers.py`, `corridas.py`, `board_caras.py`, `framed_openings.py`, `test_canon*.py`.
Bloques: `constants`, `header_schedule`, `sill_rule`, `walls` (`faces`, `openings`, `band`), `nodes`,
`openings_extra`, `opening_schedule`, `ceilings`, `runs`, `facades`, `canopies`, `band`, `parapets`,
`blocking_items`, `plywood_strips`, `trim_items`, `wet_fixtures`, `tile_base`, `frp`, `sealant_items`,
`sealant_base_exterior`, `level5_items`, `ballistic_jogs`, `section_details`, `ceiling_details`, `details` y v67
`mep_sweep`, `mep_penetrations`, `extra_framing`, `access_panels`, `accesorios_rfi`, `accesorios_none`.

Reglas (las tools fallan si no se cumplen):
- header: `pieces` + `pieces_source`; box = 4; CONT. `continuous_run` + `wall`; `or_steel`; ducto / FD =
  NOT_FRAMED; storefront exterior `structure` + `structure_source`; sin `header_params`.
- parapet: `line`, `from_ft`, `to_ft`, `length_basis: "stud_cl"`, `facade`. canopy_soffit: `wall_line_ft`.
  `ballistic_jogs [{ref, length_ft, height_ft, detail, faces_5_8, source}]`. wraps / piers: `parts` o
  `faces_ft` + `fos_chain {value: [eslabones], source}`. Facades con parapet: `parapet_t_stud_ft`,
  `nailbase_top_ft`, `nailbase_bottom_ft` o `parapet_face_of`. Faces por tramo: `side` + `length_ft` +
  `length_source`. Framed openings: `width_source`.
- **v67** `mep_sweep {sheets: [P*, M*, …], source}` obligatorio; `mep_penetrations [{ref, wall, width_in |
  dia_in, qty, studs_cut?, source}]`.
- **v67** abertura ATM (kind `atm` o "ATM" en el ref): `atm_recess {width_ft, width_source, sistered_h_ft,
  furring_rows, source N/HOJA}` o `atm_recess_none_reason`; `extra_framing [{ref, lf | pcs + len_ft, kind}]`.
- **v67** toda abertura exterior (wall EXT* / exterior / window / storefront / ATM): `jamb_return` true|false +
  `jamb_return_source`; storefront con return: `wall_jambs` + `wall_jambs_source`.
- **v67** `grille_head.head_build {head_ft, box_depth_ft, n_box, board_in, source}` o `stud_len_ft`.
- **v67** `constants.level5_tags` obligatorio con `level5_items`; item con `wc_tag` y `base_ft {value, source}`.
- **v67** `access_panels [{ref, qty, size}]`, `tile_base[].inside_corners`, `constants.<yield>`,
  `constants.parapet_studs_per_bay_min`; `accesorios_rfi [{familia, motivo, delta}]` (el plano no contesta);
  `accesorios_none [{familia, why}]` (el plano contesta que no hay).
- framed_soffit `drop_lines` = bordes que en el RCP dan a un ceiling. Bottom track sin descuento de doors;
  transición y canopy soffit 2 líneas; kickers con `vertical_studs`; `joist_source`; `roof_step_rows_drawn`;
  `tag_counts`; sin insulation.

---

## 5. Elementos (lista cerrada) → familia del track

| Familia | Elementos |
|---|---|
| bottom track + top / deflection track (L × rows c/u, sin descuento de doors) | wall, parapet, roof_step, pier, column_wrap, chase, vestibule_head, grille_head, grille_box, door_bulkhead, storefront_cripples |
| track de ceilings / soffits (L × track_lines) | ceiling_perimeter (1, lo genera canon), soffit_drop (2), ceiling_transition (2 fijo), ceiling_bulkhead (2), soffit_side (2), soffit_bottom (2), fascia_box (2), canopy_soffit (fascia + wall), joist (2) |

La familia sale del ELEMENTO, no de la orientación.

---

## 6. Familias que DEBEN salir de las tools (sin PENDING)

Studs 6", 3-5/8", 1-5/8", 2-1/2" (studs_nodos + joists + kickers + verticales + wraps / parts) · 6" parapet stud
(E3) · bottom, top y track de ceilings / soffits, bracing, purlin (corridas) · header / box beam y sill por
piezas (headers) · furring, carrying, hanger PCS + LF · 5/8" regular, MR, ballistic, 3/8" (board_caras) · glass
mat, EXTERIOR gyp sheathing, FRT plywood (E25) · cement board, FRP, acoustical sealant · FRT blocking, metal stud
blocking, metal trim · framed openings MEP (framed_openings) · las 15 familias de accesorios / extras (§12,
accesorios.py dentro de canon.py).

---

## 7. Criterios fijos (fórmulas; sin valores de proyecto)

- **Studs**: campo 1 + Σ ROUNDUP(zona / oc); cripples FLOOR(R.O. / oc); 4 jambs por abertura (no ductos / FD).
  Nodos: L +1 · T +1 · X +2 · free 0 · vendor_end +1 · split −1 × rows · abut 0; T entre G/G1 = abut; partition
  contra exterior = T. Exterior: H = B.O.D. − d. Un remate de 4" en un office front = extremo del wall que llega.
- **Parapet (E3)**: 5 mínimo por bay; tramos en el eje del stud; run por línea contigua; bays por run.
- **Board**: L × H × layers − abertura, face por face; face con dos rooms = tramos; un lining no tiene face del
  lado que forra. Ballistic L × min(tope, H) por todo el contorno; 3/8" sobre el tope. A1/A5 con ceiling =
  ceiling + 6" del detalle (salvo "TO UNDERSIDE OF DECK"). **MR** solo detrás de toilet / lavatory.
- **Wraps / piers**: face = cadena FOS completa; studs por face o `studs_drawn`; dos sistemas = `parts`.
- **Bracing**: rows = ROUNDUP(H × 12 / 48) − 1; LF = rows × L × rows de stud. **Purlin**: 0.75 × L de top track a
  deck paralelo al flute, una pieza por corrida, también transiciones y bulkheads.
- **Header / sill**: barrido cerrado (doors, ventanas, ATMs, office fronts, box beams, "AS NEEDED", grilles,
  ductos / FD, lintels S*, cada "HOLD"); R.O. ≤ stud bay → 0; sill (R.O. + 1'-4") × piezas.
- **Ceilings**: carrying (ROUNDUP((ancho − 1) / 4) + 1) × largo; hangers por carrying ROUNDUP((largo − 1) / 4) +
  1; framed_soffit con `drop_lines` = bordes que en el RCP dan a un ceiling.
- **Transiciones**: kickers @48" + verticales; kicker sin largo impreso = h / sin(ángulo dibujado).
- **Exterior (E25)**: glass mat = base strip + banda T/STUD − B/STUD; nailbase T/BASE → T/STUD − banda −
  aberturas, por facade, TODAS las facades.
- **Blocking**: por stud row con face > largo de hoja; FRT solo rotulado (grep "FRT" / "PLYWOOD" / "BLOCKING"
  antes de "sin rótulo"); ancho = schedule o contorno, nunca la cota de ubicación.
- **FRP / sealant / trim**: FRP = perímetro neto del tile_base × top + mop sink; sealant por detalle (doors
  abajo); trim = callouts + bordes de jamb return (A5) × 2 + transiciones × 2.
- **Framed openings MEP**: max(ancho, largo) ≤ módulo → 0; air devices / ductos de wall NOT_FRAMED; `sweep` M + E;
  `tag_counts` con sufijo normalizado; `width_source`.
- **Cladding**: hat channel / Z-girt / lath EXCLUDED + RFI. **Insulation**: EXCLUDED siempre.

---

## 8. Compuerta (NO ENTREGABLE si falla)

1. `inventario.py`, `canon.py`, `vigas_sobre_walls.py` corren sin error; ninguna familia obligatoria en 0 sin motivo.
2. Todas las cantidades de §6 salen de `familias_out.json` / `framed_openings_out.json`.
3. `closer.py`: header = Σ (R.O. + 1'-4") × piezas; ducto con header / sill = rechazo.
4. `bitacora.py compuerta` completa; RFIs con delta; toda abertura, corrida, face y ceiling con source.
5. Back-check ciego familia por familia; `test_alcances.py` OK contra el Excel final.
6. **v67:** `plantilla_excel.py armar … --familias familias_out.json`; el Excel trae las 15 familias de
   accesorios en Material Summary y la hoja Partition Takeoff con la convención (§13), verificado por
   `plantilla_excel.py verificar` dentro de `bitacora.py compuerta`. Una familia de accesorios PENDIENTE = NO SE
   ARMA. `contar_tags.py`, `vigas_sobre_walls.py` y `test_ciego.py` con rc 0.

---

## 9. Reglas anuladas o corregidas (sin valores)

- **v67**: 4 studs en bays cortos → 5 en todo bay (E3); un eslabón FOS → cadena completa (E8); grille por
  studs_nodos con el alto del head → `head_build`; Level 5 sin base / tag por substring → base + tag exacto;
  framing screws por regex → `pcs`; reinforcement solo con FD → barrido P/M; ATM y jamb return opcionales →
  obligatorios; TOTAL en la col. A → col. B; types EXT / PARAPET / BULK / CANOPY COL / RS / TRANS / VH / CSR → §13.
- v66 y anteriores: ARBITRAJE_13 a 15 (fuera del paquete de pruebas).

## 10. Anti-varianza

Una lectura por dato; criterio = constante con fuente; cada regla en una tool con test que falla con el dato
malo (sintético); inventario antes que totales; > 2 % entre agentes → diff de canons → regla; ningún acierto
cuenta si no fue ciego (E24).

## 11. Reglas v67 con test (R15–R27 de v66 siguen; cada una falla con el dato v66)

R28 5 studs mínimo por bay · R29 cadena FOS completa · R30 accesorios + types dentro de canon, grille fuera de
studs_nodos · R31 framing screws = 4 × `pcs` (test_canon) · R32 barrido P/M, plate por stud, ≤ 1" sin plate ·
R33 ATM y jamb return obligatorios · R34 Level 5 base + tag exacto (test_accesorios) · R35 Material Summary por
familia, PENDIENTE no se arma, Partition Takeoff (test_plantilla_v67, test_partition_types) · R36 compuerta con
accesorios, convención, `--familias`, test_ciego (test_bitacora 21–24).

---

## 12. Accesorios y extras (accesorios.py; NET, el waste lo pone la plantilla)

Siempre incluidos (criterio del estimador): trims, taping, drywall screws, framing screws, track pins. Ninguna
familia se omite: sin dato = PENDIENTE (bloquea el Excel) → se resuelve del plano (E23) o `accesorios_rfi` con
delta. Waste 15 % en metal; lo no metal con el factor del board; yields sin waste. Insulation EXCLUDED siempre.

| # | Familia | Regla (fuente: el detalle típico del set) |
|---|---|---|
| A1 | additional head track (LF, metal) | R.O. > 4'-0" en walls: (R.O. + 2 × bearing) × qty; openings_extra con box propio → RFI con delta (2/S5.20, 9/S5.20) |
| A2 | stud reinforcement MEP (PCS) | barrido P/M; Σ qty × MAX(1, ROUNDUP(ancho / O.C.)) (o `studs_cut`); pipe ≤ 1" en el web = 0; ductos / FD no se enmarcan pero llevan plate (6/S5.20) |
| A3 | extra framing ATM (LF, metal) | (ROUNDUP(ancho / O.C.) + 1) × alto sistered + filas de furring × ancho; + `extra_framing` (detalle del ATM) |
| A4 | 2-1/2" CFMF coiling grille head (LF, metal) | (ROUNDUP(L / O.C.) + 1) × (head impreso − n box × peralte − board); nunca el alto total (detalle del grille head) |
| A5 | gypsum board jamb return (SF) | bordes (R.O. + 2 jambs − sill + sill; storefront: head + wall_jambs × head) × ancho; ancho no acotado = RFI (secciones head / sill / jamb) |
| A6 | PVC trim at FRP (LF) | 2 × perímetro neto + esquinas × top + 2 × doors × top + mop sink (detalles del toilet room) |
| A7 | PAFs and duct sleeves (PCS) | ROUNDUP(L / spacing) por run de parapet + 1 sleeve por ducto / FD en wall (parapet infill) |
| A8 | access panel (PCS) | marcadores del RCP / notas M-P sobre GWB (no ACT) (RCP key notes) |
| A9–A11 | drywall screws · joint compound · joint tape | yield × (5/8" regular + MR + 3/8"); sin sheathing, glass mat, ballistic, FRT (criterio del estimador) |
| A12 | framing screws (PCS) | 4 × piezas de stud instaladas (studs_nodos + `pcs` de canon); sin joists (criterio + fastener schedule) |
| A13 | slab pins (PCS) | bottom track interior sobre losa × rows / spacing más cerrado; deltas a los otros spacings = RFI (sill track anchorage) |
| A14 | expansion anchors (PCS) | bottom track exterior sobre losa / spacing exterior; el tag del plano manda (sill track anchorage) |
| A15 | Level 5 finish (SF) | Σ L × (alto − base) por cada tag LEVEL 5 del finish schedule; tag sin item = PENDIENTE (finish schedule + key notes) |

Nombres EXACTOS del renglón: `accesorios.NOMBRES_EXCEL` (el del grille lleva su N/HOJA; el del access panel la
medida del key note).

## 13. Partition types (partition_types.py; hoja Partition Takeoff)

| # | Regla |
|---|---|
| PT1 | Type = tag del plano; exterior → `EXT-<stud>CFMF`; parapet → `EXT-PARAPET` (un wall por run de E3); door_bulkhead → `BULKHEAD-<type del wall>`; canopy column → `CANOPY-COL`; pier con tag interior = su tag (el tag manda). |
| PT2 | Un wall = tramo recto de un type entre esquinas o extremos: colineales (≤ 3") y contiguos (≤ 6") se unen; no se parte por altura, room, T ni abertura. Un renglón por wall (ids con "+"). |
| PT3 | Jog / stub ≤ 1'-0" que no es el único de su type: no es wall; su LF va en la Location del vecino ("incl. jog"). |
| PT4 | Office bulkheads colineales de un frente = UN wall (run del CONT. BOX BEAM). |
| PT5 | storefront cripples, vestibule / grille heads, roof step, fascia, canopy soffit, transiciones, bulkheads y soffits de ceiling → bloque `TYPE OTHER FRAMING (NOT A PARTITION)`. |
| PT6 | Formato: `TYPE <nombre>` en la col. A; renglón `"<type>  #<id>  -  <location>"` + Length; TOTAL con la col. A vacía y texto en la B; OTHER FRAMING después del TOTAL. |
