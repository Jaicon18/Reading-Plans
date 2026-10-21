---
name: back-check-take-off
description: "Verificación independiente (back-check) de un take-off de metal frame y drywall ya hecho: re-cuantifica a ciegas desde las cotas del plano, verifica por cierre dimensional y cruce entre hojas, compara a tres vías y entrega reporte más Excel corregido."
---

# BACK-CHECK — Verificación independiente de take-off (Metal Frame / Drywall)

Un back-check NO es releer el take-off. Es **rehacerlo a ciegas y después comparar**.
Tu trabajo no es confirmar los números del estimator; es encontrar lo que se le fue.
Un back-check que no encuentra nada es sospechoso: di explícitamente qué revisaste y dónde
no pudiste concluir, nunca "todo correcto" a secas.

## Cuándo usar este skill

Cuando el usuario pida revisar, verificar, auditar, back-checkear o "darle una segunda
pasada" a un take-off ya existente (propio, de otro estimator, o generado por Claude),
con el bid set disponible. Para cuantificar desde cero un proyecto nuevo, el skill que
aplica es `take-off-metal-frame-drywall`; este lo complementa, no lo reemplaza.

## Las tres fuentes y cómo se comparan

El flujo del usuario produce hasta TRES take-offs del mismo proyecto:

| # | Fuente | Método | Independiente del back-check |
|---|---|---|---|
| 1 | **Estimator (Bluebeam)** | medición manual sobre el PDF | **SÍ** — otra persona, otra herramienta, otro criterio |
| 2 | **Take-off de Claude** | el skill `take-off-metal-frame-drywall` | **NO** — mismo modelo, mismo protocolo, mismo plano |
| 3 | **Back-check** | este skill, a ciegas | — |

La comparativa es **a tres vías**, pero los tres números NO valen lo mismo:

- **#1 vs #3** es la única comparación verdaderamente independiente por LECTOR. Ahí es
  donde un acuerdo significa algo y un desacuerdo señala un problema real.
- **#2 vs #3** comparte sesgo: mismo modelo, misma forma de leer el plano. Si coinciden,
  eso NO es confirmación — es la misma lectura hecha dos veces.
- **#1 vs #2** también es independiente y sirve para lo mismo que #1 vs #3.

### REGLA ANTI-MAYORÍA (obligatoria)

**Nunca resolver una discrepancia por conteo de votos.** Dos de las tres fuentes
comparten sesgo, así que "dos contra uno" no es evidencia de nada.

Cuando #2 y #3 coincidan y #1 (Bluebeam) difiera, el resultado NO es "el estimator se
equivocó". Es una **DISCREPANCIA ABIERTA** que se resuelve volviendo al plano y buscando
la dimensión impresa. Si el plano la tiene, gana el plano y se dice quién acertó. Si el
plano NO la tiene — la dimensión es `[DERIVADO]` en los tres — la discrepancia se reporta
sin resolver, con el delta de cada lectura y qué haría falta para cerrarla. Que el
estimator haya medido con Bluebeam sobre geometría real es, si acaso, razón para darle
más peso, no menos.

Matriz de resultado por fila:

| Patrón | Clasificación |
|---|---|
| Los tres coinciden y el número es `[CONFIRMADO]` | **VERIFICADO** — dos métodos distintos sobre dimensión impresa |
| Los tres coinciden pero es `[DERIVADO]` | **COINCIDENCIA NO INDEPENDIENTE** — concuerdan, nadie lo probó |
| #1 difiere, #2 = #3 | **DISCREPANCIA ABIERTA** — al plano, nunca por mayoría |
| #2 difiere, #1 = #3 | hallazgo contra el take-off de Claude (las dos independientes concuerdan) |
| #3 difiere, #1 = #2 | hallazgo contra el back-check — revisa TU lectura primero |
| Los tres difieren | RFI o error de método; reportar las tres lecturas |

Si solo hay una fuente disponible, dílo en la cabecera y trabaja con esa; no inventes las
otras dos ni presentes una comparativa a tres vías incompleta como si estuviera completa.

## Cuando no hay Bluebeam: independencia por MÉTODO, no por lector

El objetivo del usuario es que Claude llegue a hacer el take-off **sin Bluebeam**, sacando
las medidas únicamente de las cotas impresas. Eso funciona para medir — una cota impresa
es exacta y le gana a medir con escala — pero **elimina la fuente #1**, que es la única
independiente por lector. Sin ella, take-off y back-check son el mismo lector dos veces y
el back-check se degrada a repetición con cara de confirmación.

En ese escenario la independencia tiene que venir del método: el back-check llega al mismo
número **por otro camino**, no releyendo la misma cota. Tres mecanismos, obligatorios
cuando falte la fuente #1 y recomendables siempre:

**1. CIERRE DIMENSIONAL.** La suma de los tramos acotados de un eje debe igualar la cota
corrida de ese eje. Es aritmética, no lectura, y por eso sí verifica. Si no cierra, hay un
error — aunque las tres fuentes hayan escrito lo mismo. Si no existe cota corrida contra
la cual cerrar, esa cadena **no es verificable**: todo lo que salga de ella queda
`[DERIVADO]`, nunca `[CONFIRMADO]`, y se dice cuál cadena es y por qué.

**2. CRUCE ENTRE HOJAS.** El mismo muro aparece en el construction plan, el RCP, las
interior elevations y las wall sections. Son documentos distintos: si la altura que sale
del RCP no concuerda con la de la wall section o la interior elevation, hay un error, y lo
detectas sin volver a leer la primera hoja. Cada altura y cada tipo de muro que entre al
take-off debe concordar en al menos dos hojas, o se reporta como no verificado.

**3. SANITY CHECK DE MAGNITUD.** Contrasta los totales (SF de board, LF de muro) contra el
área bruta del edificio que viene impresa en la hoja de life safety o en el código. No
atrapa errores finos; atrapa los de orden de magnitud, que son los que matan un bid.

**Lectura de cotas: el error que se repite idéntico.** Las cotas vienen fragmentadas en el
texto del PDF (`57'` `-` `6` `1/2"`). Pegarlas mal produce disparates silenciosos — unir
`6` con `1/2` como `61/2"` convierte 57.54 ft en 62.08 ft. Ese error lo comete el mismo
parser las dos veces, así que ni el back-check lo atrapa por comparación; solo lo atrapan
el cierre dimensional y el sanity check. Reconstruye pies y pulgadas por separado y
verifica cada conversión con código.

**Consejo de transición.** No apagar al estimator de golpe: correr las tres fuentes en
paralelo varios proyectos y llevar la cuenta de quién acierta en cada discrepancia, por
tipo de partida. Claude tiende a ganar en muros acotados y en aritmética, y a perder en
tramos sin cota y en muros sin tag — justo donde el ojo del estimator recorriendo
geometría no tiene sustituto.

## Reglas que heredas y nunca relajas

Todas las reglas del protocolo de take-off del usuario aplican aquí igual. En particular:

- **REGLA #0 — HONESTIDAD DIMENSIONAL.** Cada número que escribas va clasificado:
  `[CONFIRMADO]` dimensión impresa, citando hoja · `[DERIVADO]` calculado con método
  validado, mostrando la operación · `[PENDIENTE]` no acotado. Nunca escalar a ojo.
  Si algo no se distingue con certeza, decirlo y detenerse.
- **EVIDENCIA VISUAL.** Imagen de cada cosa que afirmes o marques como error. Antes de
  entregar una imagen marcada, reabrirla y confirmar que la marca cae sobre el elemento
  correcto. Si el usuario señala algo sobre un archivo que tú generaste, reabre ESE
  archivo antes de contradecirlo.
- **NUMERACIÓN FIJA.** Los muros se numeran una vez y ese número es permanente. Cuando
  existan varias fuentes, la numeración del back-check es la que manda, y el reporte
  incluye la equivalencia con la nomenclatura del estimator.
- **EJES SEPARADOS.** Nunca juntar dos ejes o fachadas en un solo número.
- **SOFFITS SEPARADOS.** Nunca mezclados con ceilings ni con muros.
- **AMBIGÜEDAD = RFI** con el DELTA de cada alternativa. Nunca elegir en silencio.
- **Waste:** 15% metal, 6% board, por tipo, en celda aparte.
- **PASADAS.** Dar todas las pasadas de verificación necesarias sin pedir permiso.
- **IDIOMA.** Términos de oficio en inglés: jambs, header, sill, track, stud, blocking,
  bracing, deflection, slip track, furring, soffit, storefront, deck, mullion.
- **SECUENCIA.** Los pasos de abajo se ejecutan en orden y de forma explícita. No
  comprimirlos ni saltarse el orden salvo instrucción del usuario.

## Lo que un chat nuevo SÍ te da y lo que NO

**SÍ da:** cuarentena real del contexto. En un chat nuevo no conoces las cantidades de
ningún take-off previo, así que tu barrido y tu cuantificación no pueden anclarse a ellas.
Esto es lo que atrapa omisiones y números "redondeados hacia lo que ya se había dicho".

**NO da:** independencia de criterio frente al take-off de Claude. Es el mismo modelo con
el mismo protocolo leyendo el mismo plano. Un error de LECTURA — una dimensión mal
interpretada, un detalle leído al revés, un área que el plano dibuja de forma confusa — se
repite idéntico y produce una coincidencia falsa que se siente como confirmación. Por eso
existen la regla anti-mayoría, la verificación por método y la sección COINCIDENCIA NO
INDEPENDIENTE.

## SECUENCIA DEL BACK-CHECK

### PASO 0 — Cuarentena física: el back-check corre en chat nuevo

**El back-check NUNCA corre en el mismo chat donde se hizo el take-off original.** Corre
en un chat nuevo en el que solo está el bid set. La cuarentena tiene que ser física, no
una promesa de "no voy a mirar".

Cómo arranca el chat nuevo:

- El usuario entrega **SOLO el bid set** y dice qué alcance revisar. NO entrega el take-off
  del estimator ni el de Claude todavía.
- Si alguno igual está al alcance (adjunto, en la carpeta conectada del Cowork Project, o
  porque tú mismo lo generaste antes), **no lo abras**. Decláralo en cuarentena y continúa.
- Los marcados de Bluebeam sobre el PDF cuentan como cantidades: si el set que te dan trae
  las mediciones del estimator encima, pídele el set limpio. Si no hay set limpio,
  decláralo como contaminación en la cabecera.
- Metadatos que sí puedes pedir al inicio, en texto, sin abrir los archivos: proyecto,
  revisión y fecha del bid set que usó cada fuente, qué tags y qué áreas dice cubrir cada
  una, qué hojas cita.
- Pides los take-offs **hasta el PASO 5**, no antes. Cuando los pidas, pídelos **los dos
  a la vez**: abrir primero el de Claude y después el del estimator sesga la lectura del
  segundo.

**Fuga por memoria.** Antes de empezar, revisa si tu memoria persistente guarda cantidades
de este proyecto. Si las guarda, las declaras en la cabecera del reporte como
contaminación conocida y dices cuáles. Regla derivada: de un take-off no se guardan
cantidades en memoria — solo alcance, decisiones de método y RFIs.

Si por cualquier razón el back-check termina corriendo en el mismo chat que un take-off,
**empieza el reporte diciendo que viene contaminado** y que solo vale como auditoría de
método y aritmética, no como verificación de alcance.

Declara en la salida: *"Cantidades de los take-offs en cuarentena hasta el PASO 5."*

### PASO 0-B — Herramientas: se toman SIEMPRE de `_herramientas/py/` (regla 48.1)

> Fuente única de herramientas: `JC HUNTER PROJECTS/_herramientas/py/` en Google Drive (PC:
> `C:\Users\jesra\My Drive\JC HUNTER PROJECTS\_herramientas\py`). Antes del PASO 1:
> listar esa carpeta, copiar sus herramientas al área de trabajo, leer
> `_herramientas/00_INDICE_HERRAMIENTAS.md` y correr los `test_*.py`. Si un test no pasa,
> esa herramienta no se usa y se reporta.

Nunca se toma una herramienta de la carpeta de un proyecto, ni de una sesión anterior, ni se
regenera de memoria mientras exista en `py/`.

**Cuarentena de herramientas específicas de proyecto.** Las herramientas genéricas (lectura,
marcado, cierre, auditoría, Excel, `test_*.py`) se usan. Las que se escribieron para un
proyecto en particular —por nombre (`cerrar_A1_v2.py`, `marca_a1_8_*.py`,
`hoja_parapeto.py`, `cerrar_columnas_canopy.py`…) o porque traen cotas, tags o cantidades
del proyecto escritas adentro— **cargan las respuestas del take-off original** y se tratan
igual que los take-offs: en cuarentena hasta el PASO 5. Si el back-check necesita un cierre
de ese tipo, se escribe uno nuevo desde las cotas del plano. Ante la duda sobre si una
herramienta trae datos del proyecto, se abre y se revisa antes de correrla.

**Libro de partidas propio (reglas 50.1 a 50.5).** La re-cuantificación a ciegas del PASO 3
arma su PROPIO `registro.json` con `registro.py`, desde su propio barrido, sin copiar el del
take-off (eso sería heredar sus omisiones). Mismo respaldo en `<proyecto>/Back-check/_progreso/`
y la misma compuerta: no hay reporte con renglones `pendiente`. En el PASO 5, todo renglón que
esté en un registro y no en el otro es un hallazgo de alcance.

**Lo nuevo vuelve a `py/` (regla 48.2).** Toda herramienta nueva o corregida durante el
back-check se sube a `_herramientas/py/` en el MISMO turno, con su `test_*.py`; la versión
anterior se mueve (no se borra) a `_herramientas/py/_anteriores/` con sufijo de fecha, y se
actualiza `00_INDICE_HERRAMIENTAS.md`. Al cerrar, la entrega declara en una línea:
*"Herramientas: N nuevas, M corregidas subidas a `_herramientas/py/`"* (o *"sin cambios"*).

### PASO 1 — Control de revisión del set

Compara la revisión/fecha del bid set contra la que usó CADA fuente. Con varios take-offs,
lo primero que se rompe es que no todos trabajaron el mismo set. Si alguna no coincide,
ÉSE es el primer hallazgo y es crítico: lista cada ASI, bulletin o nube de revisión que
entró después y qué muros toca. Una fuente hecha contra un set viejo no entra en la
comparativa hasta resolverlo; compararla es peor que no tenerla.

Revisa también el bloque de revisiones contra la fecha del sello: una fecha de sello
posterior a la última línea de revisión listada es motivo de pregunta.

### PASO 2 — Barrido ciego de ubicaciones

Recorre TODO el plano por cada repetición de cada tag, sin mirar ninguna lista previa.
Produce tu propia lista numerada de ubicaciones, agrupada por tag, con imagen circulada
de CADA ubicación. Incluye lo que típicamente se omite:

- Muros en mezzanine, plenum, roof screens y áreas de servicio.
- Shafts, chases, furring contra masonry o concrete.
- Columns wraps y pilasters.
- Muros bajo stairs y en landings.
- Soffits y bulkheads (lista aparte).
- Enlarged plans y details que muestran muros no visibles en el floor plan general.

**Método recomendado para el barrido.** Extrae las coordenadas de los tags del texto
vectorial del PDF (`pdftotext -bbox`) en vez de buscarlos a ojo: da la lista completa y
repetible. Después dibuja los números sobre la hoja renderizada y **reabre la imagen
marcada por cuadrantes** para confirmar que cada marca cae sobre su tag y asignarle el
cuarto. Filtra los falsos positivos: letras de eje (grid bubbles), marcas de sección y el
legend usan las mismas letras que los tags de partición.

**El barrido por tags no cierra el alcance.** Cuando la hoja diga algo como *"ALL
PARTITIONS TO BE TYPE X UNLESS OTHERWISE NOTED"*, todo tramo SIN tag es de ese tipo por
default y no aparece en una lista construida desde los tags. Dílo explícitamente y trata
el recorrido de la geometría tramo por tramo como una pasada aparte — y ojo: un take-off
de Claude construido recorriendo tags hereda exactamente el mismo hueco, así que ahí #2
y #3 van a coincidir por la misma razón equivocada. Es la fuente #1 (Bluebeam) la que
probablemente sí los tenga; sin ella, el recorrido de geometría es obligatorio.

**PAUSA OBLIGATORIA.** Entrega la lista numerada + imágenes y espera confirmación del
usuario antes de cuantificar. No avances por tu cuenta.

### PASO 3 — Re-cuantificación independiente

Cuantifica tu propia lista aplicando el protocolo completo de take-off:

- **Altura por cara.** El board va hasta donde diga su detalle, medido contra el ceiling
  del cuarto QUE ESA CARA MIRA. Cuarto open to structure = board al deck. Un muro puede
  ser asimétrico: caras distintas, alturas distintas, capas distintas. Arma la tabla de
  alturas de ceiling por cuarto desde el RCP ANTES de cuantificar, y marca los muros que
  separan cuartos con ceiling distinto — esos son los que más se erran.
- **Descripción lado por lado.** Qué lleva cada cara, nombrada.
- **Detalles de soffit completos** antes de cuantificar cualquiera: framing y spacing
  propio, kickers, track, anclaje, ancho, caída, board por cara, bead, blocking, acabado.
  El bracing y los kickers (típicamente @ 48" o.c. contra estructura) son metal que se
  compra y es lo primero que se omite.
- **Exterior no es interior.** Un canopy o soffit exterior suele ser sheathing sobre CFMF
  más cement plaster, no gypsum board — aunque el RCP lo dibuje con el mismo hatch que
  los GWB ceilings interiores. Abre su detalle antes de asignarle material.
- **Tamaño de hoja variable**, nunca fijo en 4x8.
- **Notas condicionales verificadas contra la hoja que corresponde** (p. ej. "where
  shelving occurs" se cruza contra el Fixture Plan antes de aplicarse). Cuando dos hojas
  describan el mismo elemento (una nota de arquitectura y una de electricidad sobre el
  mismo plywood backboard, por ejemplo), reconcilia las dos antes de cuantificar.
- **Cross-check de trades.** Revisa demolition y new work de mechanical, plumbing,
  electrical y cualquier trade correlacionado contra las ubicaciones de drywall: donde
  ese trade pasa por o dentro de un muro o GWB ceiling, ese board se destruye y se cuenta
  como board NUEVO de reemplazo, más su framing. Umbral: si el trade solo requiere cortes
  pequeños que suman menos de 1/4 de hoja, se clasifica como "patch and repair". Los
  cortes de patch NO se suman entre sí — cada corte se evalúa individualmente contra el
  umbral — pero cada patch individual sí se lista en el take-off. En obra nueva (ground
  up, sin plano de demolición) esta regla no aplica en su forma de remodelación: dílo, y
  en su lugar cuenta el blocking y los cortes por equipo empotrado en muro.

### PASO 4 — Auditoría aritmética, cierre dimensional y cruce entre hojas

Antes de comparar contra nadie, verifica tu propia hoja por método:

**4a. Aritmética pura.**

- Recalcula toda fórmula con código (python), no mentalmente. Muestra la operación.
- Unidades consistentes: LF vs SF vs EA; pies-pulgadas convertidos correctamente, con
  pies y pulgadas reconstruidos por separado (ver la advertencia de lectura de cotas).
- Waste aplicado una sola vez y en celda aparte (15% metal, 6% board).
- Stud count por muro: `(LF / spacing) + 1` más studs de jambs y ends; verifica que el
  spacing usado sea el del detalle, no un default.
- Track: 2x LF salvo que el detalle diga otra cosa; slip/deflection track contabilizado
  donde el detalle lo pida.
- Board SF por cara y por capa, no por muro.
- Rangos de suma que no dejen filas fuera ni incluyan el header.

**4b. Cierre dimensional.** Para cada eje y cada fachada: suma los tramos acotados y
compáralos con la cota corrida impresa. Reporta el residuo. Cierra dentro de 1/8" → los
tramos de esa cadena son `[CONFIRMADO]`. No cierra → hay un error que hay que encontrar
antes de seguir, y se dice en qué cadena. No hay cota corrida → la cadena no es
verificable, sus tramos quedan `[DERIVADO]`, y eso se lista como limitación del
back-check, no se esconde.

**4c. Cruce entre hojas.** Cada altura y cada tipo de muro debe concordar en al menos dos
hojas distintas (construction plan, RCP, interior elevations, wall sections, partition
schedule). Lo que solo aparece en una hoja se marca como no cruzado. Las discordancias
entre hojas son hallazgo contra el bid set, no contra el estimator: van a RFI.

**4d. Sanity check de magnitud.** Totales de board y de LF contra el área bruta impresa
del edificio. Si el orden de magnitud no cuadra, hay un error estructural; búscalo antes
de entregar nada.

La misma auditoría se les corre a las hojas de las otras fuentes, pero **hasta el PASO 5**
— abrirlas aquí rompería la cuarentena.

### PASO 5 — Comparación a tres vías

Pide las hojas a la vez, corre sobre cada una la auditoría del PASO 4, y compara contra
tus números. Aplica la matriz y la REGLA ANTI-MAYORÍA de arriba. Clasifica cada
diferencia:

| Clase | Qué es |
|---|---|
| **OMISIÓN** | Existe en el plano, no existe en esa fuente |
| **FANTASMA** | Existe en esa fuente, no lo encuentras en el plano |
| **DIMENSIÓN** | Misma ubicación, largo o altura distinta |
| **ESPECIFICACIÓN** | Gauge, spacing, tipo o capas de board distintas al detalle |
| **ARITMÉTICA** | Fórmula, unidad o waste mal aplicado |
| **MÉTODO** | Regla del protocolo no aplicada (soffit mezclado, ejes juntos, altura contra el ceiling equivocado, trade no cruzado, cadena sin cerrar) |
| **RFI** | El plano no permite decidir; hay dos lecturas válidas |

Cada hallazgo dice **contra qué fuente** va. Severidad por impacto en cantidad, no por lo
llamativo del error: **CRÍTICO** (cambia el bid materialmente o es una omisión de alcance)
· **MAYOR** (error real acotado) · **MENOR** (redondeo, formato, nomenclatura).

Las coincidencias se separan según la matriz: **VERIFICADO**, **COINCIDENCIA NO
INDEPENDIENTE**, **DISCREPANCIA ABIERTA**. Una fila coincidente cuyo número pasó el
cierre dimensional del 4b sí sube a VERIFICADO aunque falte la fuente #1: ahí la
independencia la puso el método.

### PASO 6 — Entregables

**A. Reporte de hallazgos** (en inglés, como el resto de tus entregables de take-off):

- Encabezado: proyecto, revisión del set que usó cada fuente, alcance revisado, fecha,
  estado de cuarentena (limpia / contaminada y por qué) y qué fuentes entraron.
- Tabla de hallazgos ordenada por severidad: `#` · wall no. (numeración fija) · hoja ·
  clase · **contra quién** · estimator · Claude · back-check · delta · evidencia.
- Una imagen recortada y marcada por hallazgo, re-verificada antes de entregar.
- Cada número con su etiqueta [CONFIRMADO] / [DERIVADO] / [PENDIENTE].
- **Tabla de cierre dimensional**: por eje, suma de tramos, cota corrida, residuo.
- Sección de RFIs con el DELTA de cada alternativa.
- Secciones VERIFICADO, COINCIDENCIA NO INDEPENDIENTE y DISCREPANCIA ABIERTA, separadas.

**B. Excel corregido**: el "Organized Partition Takeoff Estimator" del usuario, en
inglés, con fórmulas vivas, waste en celda aparte, columnas añadidas según se necesite y
**Labor (Hrs) vacía**. Con varias fuentes, lleva una columna por fuente más la columna
adoptada y el delta; las celdas cambiadas van resaltadas y con nota que apunte al `#` del
hallazgo. No borres las filas originales. Usa el skill `xlsx` para construirlo.

**C. Dónde se guarda (regla 49.1).** El reporte y el Excel del back-check van en
`Claude outputs/<proyecto>/Back-check/`:

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

### PASO 7 — Pasada final de auto-verificación

Antes de entregar, sin pedir permiso:

1. Reabre cada imagen marcada y confirma que la marca cae sobre el elemento correcto.
2. Recalcula con código cada delta del reporte contra la hoja corregida.
3. Verifica que ningún wall no. cambió de significado entre el barrido y el reporte.
4. Confirma que cada ubicación del PASO 2 aparece resuelta en el reporte: verificada,
   con hallazgo, en coincidencia no independiente, en discrepancia abierta, o en RFI.
   Ninguna puede quedar sin mencionar.
5. Confirma que no quedó ningún número sin etiqueta de honestidad dimensional.
6. Confirma que el estado de cuarentena declarado en la cabecera es el real.
7. Confirma que ninguna discrepancia se resolvió por mayoría: cada una adoptada apunta a
   una dimensión impresa o a un cierre dimensional, o está marcada como abierta.
8. Confirma que toda cadena reportada como cerrada tiene su residuo calculado con código
   y mostrado, y que toda conversión de pies-pulgadas fue verificada.

Si algo de esto falla, arréglalo y repite la pasada. No entregues con la pasada incompleta.

## Errores conocidos que este back-check existe para atrapar

- Muro contado con la altura del ceiling equivocado (la cara mira a otro cuarto).
- Área open to structure cuantificada a ceiling height en vez de al deck.
- Soffit metido dentro de la línea de ceiling o de muro.
- Canopy o soffit exterior cuantificado como gypsum board cuando su detalle pide
  sheathing sobre CFMF más cement plaster.
- Bracing y kickers de soffit/bulkhead no contados.
- Dos ejes o fachadas sumados en un solo número.
- Nota condicional aplicada a todo el elemento sin cruzarla contra su hoja; dos hojas que
  describen el mismo elemento sin reconciliar.
- Tag usado en el plano que no tiene fila en el partition schedule.
- Muros sin tag no contados, cuando la hoja los define por default.
- Cadena de cotas que no cierra contra la cota corrida y nadie lo notó.
- Pies-pulgadas mal reconstruidos al leer la cota (6 + 1/2 leído como 61/2).
- Altura tomada de una sola hoja, sin cruzar contra RCP, sección o elevación interior.
- Board destruido por MEP contado como sobreviviente.
- Patch & repair sumados entre sí hasta "justificar" hoja completa, o patches
  individuales no listados.
- Waste aplicado dos veces, o dentro de la cantidad en vez de en celda aparte.
- Tamaño de hoja asumido 4x8.
- Spacing default en vez del spacing del detalle.
- Take-off hecho contra una revisión vieja del set.
- Back-check corrido en el mismo chat que el take-off: confirma en vez de verificar.
- Discrepancia resuelta por mayoría entre fuentes que comparten sesgo.

## REGLAS NUEVAS

Cada vez que el back-check descubra un modo de error no cubierto aquí: crear la solución,
guardarla en memoria el MISMO turno, actualizar este skill, y entregar el protocolo
DIVIDIDO en dos bloques con su propio botón de copiar: (1) bloque corto para el system
prompt; (2) protocolo completo para el skill. El resumen de qué cambió va fuera de los dos.