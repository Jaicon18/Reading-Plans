# CONTRATO DE LAS HERRAMIENTAS

**Las herramientas viven como archivos fijos en `_herramientas/py/`** (Google Drive, `JC HUNTER PROJECTS/_herramientas/py/`), no se regeneran de memoria por proyecto. En cada take-off nuevo: cópialas de ahí y **valídalas contra sus tests antes de usarlas**. Si un test no pasa, la herramienta no se usa. Si aparece un bug o un caso nuevo, se corrige EN ESE archivo (una sola versión, un solo lugar) y se deja el test que lo prueba — nunca se reescribe la herramienta entera desde el contrato de este skill salvo que se haya perdido el archivo. El contrato que sigue es lo que describe qué debe hacer cada una y cómo se prueba; sirve para reconstruirla si hiciera falta, pero el archivo fijo es la fuente normal.

## planmark.py — marcado verificado sobre la hoja

**Qué hace.** Marca walls y tags sobre una página de plano y **hace imposible entregar una marca que cayó sobre papel en blanco**.

**Reglas que encierra:**
- El factor pt→px se DERIVA (`dpi/72`) y se VERIFICA contra el tamaño real del PNG: `ancho_px / ancho_pt` y `alto_px / alto_pt` deben dar ese factor (±0.01). Si no, lanza `ScaleError` y no marca nada. Eso atrapa también el error de usar las dimensiones de página sin rotar.
- **La clave del cache de render incluye la identidad del PDF fuente** (`sha256(path + mtime + tamaño)`), no solo página y dpi. Sin eso se reusa un PNG del PDF CON markups cuando ya se pidió la copia limpia, y la regla de los markups queda anulada en silencio.
- `ink(cx_pt, cy_pt)` mide la fracción de píxeles oscuros (<160) en una window de ~14 pt centrada en el punto, **en espacio píxel** — que es donde ocurre el fallo de escala. La sonda va en **7 puntos** a lo largo del tramo (0.08 a 0.92) y se queda con el de más tinta: probar solo el centro aborta walls correctos con una door al medio.
- `verify(items)` marca fallido todo tag con tinta < 0.04. Si fallan ≥30%, el diagnóstico es **"factor de escala mal"**; si fallan 1 o 2, son **tags puntuales sobre vacío**.
- `overview()` marca la **hoja completa** con un solo tipo a la vez, con RECTÁNGULOS sobre el tramo real de cada wall y etiquetas grandes (número oficial + LF), color por tipo y leyenda que no tape el dibujo. `sheet()` arma contact sheets de recortes.
- **Ni `overview()` ni `sheet()` escriben archivo alguno si `verify` falla**, y el error nombra al culpable.

**Cuidado con la orientación del punto de prueba.** Si la banda se describe como `(c0,c1)` = faces y `(lo,hi)` = extensión, el centro de una banda HORIZONTAL es `(x=(lo+hi)/2, y=(c0+c1)/2)` — al revés de la vertical. Escrito al revés, el auto-test de tinta tira "FACTOR DE ESCALA MAL" y no escribe nada, que es exactamente lo que debe pasar: la compuerta atrapa el bug antes de que salga la imagen.

**Walls con door:** el punto de prueba de un wall con opening puede caer en el hueco; se marca en piezas sólidas a cada lado del opening (p.ej. `<n>` y `<n>1`).

**Tests obligatorios:**
1. Factor correcto sobre un lote de tags reales → todos pasan, tinta típica 0.15–0.40.
2. Inyectar un factor equivocado (p.ej. 3.15 en vez de 2.78) → aborta con diagnóstico "factor de escala mal" y **no escribe archivo**.
3. Un tag con coordenadas inventadas entre tags buenos → aborta, lo nombra, y no marca sistémico.
4. Página con dimensiones sin rotar → `ScaleError`.
5. Una banda horizontal con el punto de prueba transpuesto → aborta.
6. Pedir la misma página y dpi desde dos PDFs distintos → devuelve DOS PNGs distintos, no el cacheado del primero.

## closer.py — compuerta de cierre de wall

**Qué hace.** Recibe el cierre de un wall y **no deja salir ninguna cantidad** si el cierre no cumple. No tiene modo "emitir con advertencias".

**Estructura:** `Val(v, estado, fuente=, operacion=)` para cada número · `Wall(num, tag, ubicacion)` con `.base(largo, alto_stud, oc, brace_sp)`, `.cara(cuarto, alto_board, tipo, capas)`, `.abertura(clase, ref, w, h, head=, sill=)`, `.partida(nombre, val, unidad)`, `.excluir(nombre, motivo)`, `.afirmar_alcance(afirmacion, cadena)` y `.emit()`.

**Lo que BLOQUEA (cada uno lanza `CierreRechazado` y no escribe nada):**

| # | Regla |
|---|---|
| 1 | Valor sin estado CONFIRMADO / DERIVADO / PENDIENTE |
| 2 | CONFIRMADO sin hoja citada. Acepta las dos numeraciones reales: `A02.01` / `A4.01` y `A-410` / `A-101` / `S-201` (regex `\b[A-Z]{1,2}-?\d{1,3}(?:\.\d{1,2})?\b`). Aceptar una sola convención rechaza TODO lo confirmado de un set con la otra. |
| 3 | DERIVADO sin la operación escrita |
| 4 | PENDIENTE con valor — un pendiente no se cuantifica ni se compra |
| 5 | Afirmación de alcance con menos de 2 eslabones citados con hoja |
| 6 | Track combinado en un renglón |
| 7 | Track: cada renglón (bottom y top, separados) = 1.00 run (LF ÷ length ±0.01) y la suma de los dos = 2.00 runs (±0.02) — o 4.00 en wall de doble row, declarándolo. Exigir 2 runs POR renglón duplica todo el track. |
| 8 | Studs de campo por debajo de `floor(largo_in / OC) + 1` |
| 9 | Aberturas presentes con los jamb studs no sumados (4 por opening, o lo que diga el Header Schedule) |
| 10 | `clips ≠ studs × líneas_bracing × 2`, con `líneas = floor(altura_in / espaciamiento)` |
| 11 | Board en un renglón cuando las faces difieren en height o tipo — va **por face**, nombrado `BOARD:<cuarto>` |
| 12 | Sill en una door. Y al revés: una abertura de clase window/pass-through SIN sill declarado, o con sill pero sin los cripple studs del sill sumados. |
| 13 | `EXCLUDED` sin motivo detallado (mínimo: qué se buscó, dónde, y por qué no aplica) |
| 14 | Cualquiera de las **11 line items obligatorias** ausente: STUD · TRACK_BOTTOM · TRACK_TOP · HEADER · BRACING · CLIPS · BOARD · INSULATION · SEALANT · **BLOCKING** · PATCH. Cada una cuantificada o excluida con motivo. |

Cada emisión lleva un **sello sha256** del contenido, que cambia si se toca cualquier número.

**Faces interiores de walls exteriores de otra división** (p.ej. 2x8 de wood): se cierran igual, con STUD / TRACK / HEADER excluidos por ser Div 06, y cada abertura con su head y `marcar_jambs_sumados(ref, 0)`. Un knee wall que se suma de vuelta bajo un storefront va como área negativa en las aberturas, no como abertura de closer.

**Función aparte:** `waste(neto, clase)` → devuelve NETO / WASTE / COMPRA con 15% para metal y 6% para board, por tipo. Nunca sobre pendientes ni sobre fasteners.

**Tests obligatorios — cada uno debe ser RECHAZADO:**
1. CONFIRMADO con fuente que no cita hoja · 2. DERIVADO sin operación · 3. PENDIENTE con valor · 4. door con sill · 5. abertura sin head · 6. alcance de un solo eslabón · 7. alcance de dos eslabones sin hoja citada · 8. EXCLUDED con motivo de tres palabras · 9. cierre al que le falta BLOCKING · 10. track que da 3 runs · 11. track en un renglón combinado · 12. board en un renglón con faces a 9'-0" y 9'-6" · 13. una abertura con los jamb studs sin sumar · 14. clips que no cuadran con studs × líneas × 2.

**Y un test que debe PASAR:** un wall completo, con board por face, aberturas con su head, alcance con cadena de tres eslabones citados, las 11 line items presentes o excluidas con motivo → emite y devuelve sello.

## zoom.py — recorte de alta resolución con escala verificada

**Qué hace.** Recorta una zona de una hoja en coordenadas pt (top-down) al DPI que se le pida, derivando `F = dpi/72` y **verificando** que el PNG que salió mide exactamente `(x1-x0)*F` × `(y1-y0)*F`. Renderiza SIEMPRE desde la copia sin `/Annots`; `con_markups=True` es la única forma de ver el original y solo se usa para inspeccionar markups a propósito.

**Qué bloquea.** Si el PNG no mide lo esperado, aborta y no entrega recorte: un recorte con escala no verificada es un recorte que no sabes dónde cae. Y si el recorte se reduce para verlo, la escala efectiva pasa a ser `F × (ancho_final / ancho_original)` — todo mapeo posterior usa esa. **En hojas con MediaBox no nula hay que restar el origen en X y en Y** antes de recortar.

**Tests obligatorios.** (a) Un recorte de 60×40 pt a 1600 dpi devuelve 1333×888 px. (b) La coordenada de un elemento conocido, convertida a píxel del recorte, cae sobre tinta. (c) Un recorte de una hoja con MediaBox desplazada cae sobre el elemento esperado.

## dimensions.py — cadenas de dimension impresas

**Qué hace.** Encuentra las dimension lines de una zona (lw ~0.48), sus **ticks** y el texto asociado, y devuelve la cadena ordenada con el valor de cada tramo en pies-pulgadas al 1/16.

**Qué bloquea.** Un tick es la unión de DOS diagonales que se juntan SOBRE la dimension line: se usan sus extremos reales (`o['pts']`, top-down), nunca las esquinas del bounding box — con el bounding box los ticks salen dobles y la cadena se parte donde no debe.

**Tests obligatorios.** (a) La suma de los tramos de una cadena es igual a la distancia entre su primer y su último tick. (b) Cada valor calculado coincide con el texto impreso de esa dimension, ±1/16".

## registro2.py — registro entre hojas por el fondo arquitectónico

**Qué hace.** Deriva el offset (dx, dy) entre dos hojas votando los segmentos lengths de wall (lw ≥ 1.0, ≥ 50 pt) que existen en las dos.

**Qué bloquea.** Devuelve `None` si no junta ≥ 25 coincidentes en cada dirección. Sin registro verificado no se cruza nada. El SIGNO se verifica con al menos 3 rasgos reconocibles antes de usar el offset.

**Tests obligatorios.** (a) El offset derivado lleva una línea conocida de la hoja destino sobre su gemela de la arquitectónica, ±0.5 pt. (b) Cruzar las bandas con ese offset no devuelve penetraciones sobre líneas que existen idénticas en las dos hojas. (c) Invertir el signo del offset devuelve cero coincidencias.

## mep.py — cruce de MEP por geometría

**Qué hace.** Con el offset de `registro2.py`, lista las líneas de una hoja de MEP que atraviesan una banda de wall, filtrando las que también existen en la arquitectónica.

**Qué bloquea.** Un cruce solo cuenta si sobresale ≥ 3 pt por FUERA de las dos faces, y con lineweight ≥ 0.5. **Además detecta el CORREDOR** — la línea que llega al wall por los dos lados aunque el dibujo la corte en la face y meta un conector flexible; sin eso se pierden los cruces dibujados partidos.

**Tests obligatorios.** (a) Con el offset correcto, el nº de penetraciones sobre una banda sin MEP es cero. (b) Un ducto dibujado partido con conector flexible se detecta igual. (c) Cada penetración reportada se abre en imagen y se lee su rótulo (tamaño, tag, CFM) antes de cuantificarla.

## tagband.py — barrido por tag sin presuponer el thickness

**Qué hace.** Por cada tag: caja real (rectángulo verdadero, lw ≤ 0.7 — reconstruida también desde 4 líneas sueltas, que es como la exporta el CAD casi siempre; buscar solo rectángulos cerrados deja el censo vacío) → leader (segmento que arranca a ras de un borde de la caja) → **todos** los pares de faces con lineweight de wall que encierran la punta, con su thickness medido.

**Qué bloquea.** No presupone thickness: devuelve los candidatos para que el thickness del schedule los desempate. Un tag sin caja real no es tag de partition (así se descartan las burbujas de eje). Límite conocido: no ve tags en rombo o hexágono — en esos sets el censo va por layer de texto.

**Tests obligatorios.** (a) El censo de tags con caja real reproduce la numeración oficial del proyecto, con la caja dibujada tanto como rectángulo cerrado como con 4 líneas sueltas. (b) Para cada tag, el thickness del candidato elegido coincide con el WALL THICKNESS de ese tipo, ±0.35". (c) Las faces devueltas son la pareja de lineweight alto, no las líneas interiores.

## auditor.py — compuerta de BARRIDO

**Qué hace.** Antes de cuantificar un tipo, cuenta los WALLS REALES de ese tipo (no los tags) y compara contra lo que el cierre declara. `auditar(page_index, tag, espesor_del_schedule, esperados)`.

**La regla que hace cumplir.** Dos tags son el MISMO wall solo si su leader aterriza en **LA MISMA BANDA** — misma orientación Y los mismos dos niveles de face (±0.06 pt). **Distinta orientación = walls distintos, por cerca que estén los tags.** Nace de un error real: dos tags muy cercanos uno del otro se dieron por el mismo wall y se perdió un wall entero, porque uno apuntaba a un wall vertical y el otro a uno horizontal.

**Qué bloquea.** Lanza `BarridoRechazado` si el nº de bandas distintas no coincide con el que declara el cierre, o si algún tag se queda sin banda. No hay modo "seguir con advertencias". Elige la banda por CERCANÍA DE LA PUNTA del leader y solo desempata por error de thickness: al revés es como se pierde un wall. Mide cada wall por el TRAMO que contiene la punta, nunca por la extensión de la face en toda la hoja, puenteando huecos solo con end cap a los dos lados.

**LÍMITE HONESTO, comprobado: el auditor FLAGEA, NO DECIDE.** En su reauditoría real acertó **una minoría** de los casos. Falla cuando (a) el leader real no se detecta o se detecta al revés, (b) dos lecturas de la misma face difieren ~1 pt y parten una banda en dos, (c) el tag está en una envolvente cerrada y no en una banda. Por eso **cada bandera se resuelve ABRIENDO LA IMAGEN**, nunca aflojando tolerancias, y sus números NO sustituyen al cierre: lo que decide es reconstruir la derivación escrita y contrastarla con el dibujo.

**Tests obligatorios.** (a) Dos tags perpendiculares cercanos → devuelve DOS bandas, no una. (b) Un tag cuyo leader apunta a una envolvente cerrada → lo reporta sin banda en vez de inventarle una. (c) El nº de bandas de un tipo ya cerrado y verificado coincide con el cierre.

## verif_bandas.py — compuerta del DIBUJO

**Qué hace.** Antes de dibujar una sola hoja marcada, chequea TODAS las bandas de la tabla de marcado contra la geometría vectorial de la hoja. Es el equivalente de `closer.py` para las imágenes: `closer.py` impide entregar una cantidad mal cerrada, `verif_bandas.py` impide entregar un plano que señala el wall equivocado.

**Qué comprueba en cada banda `(nº, LF, orientación, c0, c1, lo, hi)`:**
1. Existe face con lineweight de wall en `c0` y en `c1` (lw ≥ 1.1; **reintenta a lw ≥ 0.55** antes de marcar error, porque una face puede venir dibujada fina).
2. La cobertura de esas faces a lo largo del tramo es ≥ 45%. Menos que eso es legítimo solo si el cierre documentó END CAP a los dos lados de cada hueco (doors), y se revisa a ojo.
3. El thickness `c1 − c0` corresponde a un tipo del partition schedule (±0.55").
4. El length declarado coincide con `(hi − lo) / (pt por pie de la escala)`.
5. Para una **CAJA** (`ori='BOX'`) comprueba las **cuatro aristas** en vez del par de faces, y no compara LF (el LF rotulado es el perímetro furrado).

**Qué bloquea.** Toda banda marcada se lista con OK o con `>>>`, y ninguna hoja se dibuja mientras quede un `>>>` sin explicación escrita. Las excepciones legítimas — tramos con door, bandas de bulkhead sobre opening, cajas, espesores derivados que ya vienen declarados en el cierre — se anotan una por una en el reporte; lo que no está anotado, se abre en imagen.

**Tests obligatorios.** (a) Una banda con las coordenadas transpuestas (orientación escrita al revés) sale marcada. (b) Una banda a la que se le cambia el `lo/hi` por el de otro wall de length casi igual sale marcada, aunque el LF coincida. (c) Un tipo ya cerrado y verificado pasa las N bandas en OK, con las excepciones conocidas anotadas.

## wallgeom.py — motor de medición (EN VALIDACIÓN)

Encierra el procedimiento de medición desde `page.lines`: escala derivada del rótulo, filtro de lineweight para faces de wall, pares de faces candidatos ordenados por error de thickness contra el schedule, selección del run por la punta del leader, puenteo de aberturas solo con end cap a ambos lados, y corte del run donde empieza el dominio de otro tag.

**No usar para cantidades hasta que acierte TODOS los casos contra un patrón que NO haya salido de Claude** — mediciones del usuario o dimensions impresas. En su última validación falló la mayoría: falla al desempatar dos pares de faces con errores de thickness casi iguales. Mientras tanto, la medición se hace con el procedimiento manual del skill y cada wall se verifica con imagen.

## arranque.py — Paso 0 mecánico en un solo comando

**Qué resuelve.** Abrir un bid set nuevo costaba horas de tareas mecánicas repetidas en cada proyecto: copia sin markups, mapa de page_index leyendo title blocks, ubicar Partition Types y schedules, censo de tags, y volver a escribir las herramientas a disco. Nada de eso es criterio de oficio — por eso se automatiza, y por eso además las herramientas pasaron a vivir en `_herramientas/py/` como archivos fijos en vez de regenerarse (ver arriba).

```
python3 arranque.py /ruta/al/bid_set.pdf --dpi 300 [--title-block-zona x0,y0,x1,y1] [--paginas-planta i,j,k]
```

**Qué hace, en orden:**
1. Corre los tests obligatorios de las herramientas listas (no `wallgeom.py`, que sigue EN VALIDACIÓN) — aborta si alguna falla.
2. Copia el PDF sin las anotaciones/markups de otros estimadores.
3. Verifica que el PDF tenga layer de texto vectorial en al menos la mitad de sus páginas — si no, **aborta** y pide OCR primero: nunca sigue a ciegas sobre un PDF probablemente escaneado.
4. Renderiza todas las páginas a PNG a alta resolución.
5. Lee el rótulo real de cada hoja buscando la ETIQUETA del title block ("SHEET:", "SHEET NO.", "DWG. NO.") más cercana a la esquina inferior derecha y tomando el número junto a ella; solo si no hay etiqueta usa la zona configurable. **El marco real de la hoja se deriva del bounding box de las palabras**, no del page box: las hojas rotadas (las de plomería suelen estarlo) tienen coordenadas fuera del box declarado. Una zona fija falló en el primer set real: muchas hojas sin rótulo y varios números basura de callouts. Construye el mapa `page_index → número de hoja` y compáralo contra el índice. Una hoja sin rótulo legible se marca **`SIN RÓTULO LEGIBLE`**, nunca "faltante".
6. Ubica por TÍTULO las hojas candidatas a Drawing Index, Partition/Wall Schedule, Door Schedule, Demolition Plan, RCP y las series M/P/E. Nunca por número de hoja.
7. Lee la ESCALA barriendo la hoja entera, no el title block: va impresa bajo el título de cada dibujo.
8. Tabula el partition schedule buscando **FILAS DE DATOS** (tag seguido de una medida), no el encabezado: el header suele venir partido en varios renglones y dos mitades de tabla pueden compartir la misma y.
9. Lee las notas ALFABÉTICAS de la hoja de planta y detecta el **TIPO POR DEFECTO** (`ALL PARTITIONS TO BE TYPE 'X' UNLESS OTHERWISE NOTED`).
10. Corre un censo **preliminar** de tags con caja real sobre las hojas de planta y lo cruza contra el schedule: tipos con tag y con fila · con tag y sin fila (no es RFI automático, ver regla) · con fila y sin tag (no se cuantifican).

Las palabras de todas las páginas se extraen UNA vez y se cachean: la primera run tarda minutos, las siguientes son instantáneas.

**Dónde se detiene, y por qué.** `arranque.py` se detiene ahí, en un punto de control con toda esa evidencia (reporte + PNGs + PDF sin markups). NO cruza los tags contra el detalle de cada tipo, no decide patch vs. reemplazo, no cuantifica nada: eso exige criterio de oficio, y sigue siendo el resto del protocolo (PASO 1 en adelante), paso a paso, con el usuario revisando. **Lo que no resuelve lo REPORTA en vez de callarlo:** candidatos de más en el censo (una burbuja de eje puede pasar la prueba de caja) y hojas sin rótulo legible se listan para abrir a ojo.

**Sets grandes:** si el set pasa de ~40 hojas o ~50 MB, el mapa de hojas se construye con `pdftotext` por página (segundos) en vez de pdfplumber (más de 20 min en un set real).

**Los tests sintéticos tienen que imitar cómo exporta el CAD real** (cajas en 4 líneas, las dos numeraciones de hoja, hojas rotadas, headers de schedule partidos), no la forma más cómoda de generar el PDF de prueba: así se escaparon los primeros bugs de estas herramientas.

**Prueba de aceptación:** correrlo sobre un set YA hecho a mano y comparar mapa de hojas y censo de tags contra lo que salió entonces. Si no cuadra exacto, no reemplaza el Paso 0 — solo ayuda a revisarlo.
---

## Herramientas de etapas (v69)

Flujo completo en el PROTOCOLO v69 de SKILL.md. Todas genéricas (nada de un proyecto en el código), con test.

| Tool | Etapa | Qué hace | Test |
|---|---|---|---|
| `inventario_tags.py <pdf> <out_dir>` (v70; antes `inventario.py`, que ahora es solo el inventario de walls de `canon.py`) | 1 | índice de hojas, types del schedule, cada partition tag con id único (PT / PA / PC…), hoja, coordenadas y recorte circulado verificado; ambiguos sin contar; candidatos fuera de schedule entran en la compuerta; hojas no inventariables | `test_inventario_tags.py`, `test_inventario_tags_v70.py` |
| `particion.py canon.json [--modo eje\|run\|tramo]` | 2–3 | regla única de partición de walls; `MODO_DEFAULT` = "eje" (v71, E28: línea recta por tag, segmentos sin tag sumados, grupo sin tag = un wall, exteriores por eje); "run" y "tramo" quedan como opciones; door_bulkhead = BULKHEAD-<familia>; unión transitiva | `test_particion.py`, `test_particion_v70.py`, `test_v71.py` |
| `chequeos_v71.py canon.json` (v71) | 4–5 | R71.1 flecha norte con fachadas, R71.2 box contado dos veces, R71.3 accesorios de bulkhead > Σ vanos, R71.5 (un tag descartado "por otra tarea"); corre dentro de `etapas.py compuerta` | `test_v71.py` |
| `track_por_tamano.py canon.json <bottom> [<top>]` (v71) | 4 | R71.8: reparte la familia de bottom / top track por tamaño (y gauge) de stud; resto "other" con fuente; resto negativo = falla | `test_v71.py` |
| `mep.py <page_mep> <page_arq>` (v71) | 2 | registro MEP ↔ planta derivado en la corrida (sin offsets ni página fija) y cruces que sobresalen de las dos caras | `test_v71.py` |
| `chequeos_v72.py canon.json [--vigas vigas_out.json]` (v72) | 4–5 | compuerta 0d: R72.1 type K por hatch (`hatch_extent`, ningún segmento sin tag tipado K), R72.2 diagonal = promedio de caras, R72.3 `part_of` de la parte sin tag de un box, R72.4 la salida de vigas_sobre_walls manda, R72.5 cruces MEP de `mep.cruces` y FD una vez, R72.6 side A\|B\|END, R72.10 jogs del FRP, R72.11 ATM con alternativas; corre dentro de `etapas.py compuerta`; `partes_de_box()` la usan partition_types y accesorios | `test_v72.py` |
| `cruzar_diagonal.py canon.json <wall_id> <pág MEP> <pág arq> --dx --dy` (v72) | 2 | cruce MEP sobre un wall diagonal (band D del canon) con el mismo criterio de `mep.cruces`; offset de `mep.registro` en la corrida; sin geometría ni offsets de un proyecto | `test_sin_colisiones.py` |
| `idioma_es.py` (v72) | 5 | `es_espanol(texto)` → marcas de español del entregable (lo usan plantilla_excel y verif_idioma); antes venía del entorno | `test_plantilla_v67/v68/v70.py` |
| `vigas_sobre_walls.py` (v71) | 2 | walls bajo viga; dos vigas paralelas con rótulo distinto = `candidatas` + decisión; un dueño por rótulo | `test_v71.py` |
| `esquinas.py canon.json` (v70) | 4–5 | R70.2 cada esquina con un dueño; R70.3 hueco colineal = door fuera del run; excepciones `corners_ok` / `gaps_ok` con motivo | `test_esquinas.py` |
| `comparar.py A.json B.json inventario.json out_dir --pdf plano.pdf` | 3 | empareja las dos lecturas, cruza contra el inventario y escribe `revision.md` / `revision.json` / `img/` con alertas | `test_comparar.py` |
| `etapas.py estado\|compuerta <dir>` · `etapas.py unir <carpeta> <canon.json>` | 1–5 | dónde quedó la corrida (reanudar), compuerta de etapas, unión de fragmentos de una lectura | `test_etapas.py` |
| `test_ciego_v69.py <SKILL.md\|carpeta>` | 5 | E24 genérico: sin nombres de proyecto, cantidades, miles, resultados ni coordenadas | autoprueba incluida |

## reglas.py — compuerta de reglas inviolables (v72b)

`python3 reglas.py compuerta <work_dir> [--excel <final.xlsx>]` revisa TODAS las reglas del catálogo (a: datos del
canon, de las salidas recalculadas con canon.py, de la bitácora y del Excel; b: evidencia por caso con cita, imagen
que existe y valor; c: fusionadas). Escribe `reglas_out.json` y `REGLAS_FALLAS.md`; rc 1 con una sola falla.
`plantilla_excel.py armar` la llama en proceso y no escribe el Excel sin OK; `etapas.py compuerta` y
`bitacora.py compuerta` también. `reglas.py faltantes <dir>` = plantilla de la evidencia que falta;
`reglas.py tabla` = tabla regla → tipo → chequeo → test.

## v73 — tools nuevas (contratos)

- **cotas_banda.py** — `dim_scan(pdf, pagina_1based, band, win=72)` → `{found: [{text, value_ft, center, dist_pt}],
  source}`: cotas pies-pulgadas impresas PARALELAS a la banda de un wall, a ≤ `win` pt y con centro dentro del tramo.
  Coordenadas de la página mostrada (rotada), las del canon. Lo exige R73.1 en todo wall K. Test: test_v73.
- **chequeos_v73.py** — R73.1 (cota impresa del type K), R73.2 (contorno K sin esquinas dobles), R73.5 (MEP solo
  de mep.cruces), R73.6 (deflection clips declarados), R73.7 (type por espesor de segmentos sin tag), R73.8
  (operación escrita cuadra). `reglas.py compuerta` los corre (A_R73_x). Test: test_v73 + test_reglas.
- **planmark.py** — el contrato de arriba (marcado verificado, `overview()` y `sheet()`); test_planmark sobre un PDF
  sintético con los 6 tests obligatorios.
- **glosario.py / vocab_trade.py** — `traducir(t)`, `faltas(t)` (dato y prosa; la normalización del código vive en
  `vocab_trade.sin_codigo`). **verif_respuesta.py** — compuerta de la respuesta final (adenda v40). Tests:
  test_glosario, test_verif_respuesta.
- **indice_set.py** — genérico: arma su cache de palabras con pymupdf si no está; página del índice por el texto
  "DRAWING / SHEET INDEX"; columnas por la x de los números de hoja. Test: test_indice_set (PDF sintético).
- **registro.py corregir** — corrección de un renglón resuelto (la última entrada manda; historial). Test:
  test_registro_v73.
- **correr_suite.py** — dependencias + estructura + suite completa desde carpeta limpia.
