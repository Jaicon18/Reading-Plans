---
name: "take-off-metal-frame-drywall"
description: "Protocolo completo de take-off (cuantificación) de Metal Frame y Drywall, CSI Div. 05 y Div. 09, desde bid sets en PDF. Usar cuando el usuario suba planos de construcción y pida un take-off, cuantificación, o análisis de bid set."
---

# Take-off de Metal Frame y Drywall

Versión FINAL 24-oct-2026 (v80f: §29 corrida B&N; v80 + §0.F decisiones finales del estimador; v80: §28 (R80.1–R80.11) manda sobre §27 y §26 donde se tocan; v79: §27 (R79.1–R79.4); v78: §26 manda: decisiones del usuario W1–W4 y reglas R78.x; §25 (U1–U11) sigue vigente salvo R77.11, RETIRADA en v80 (manda R78.36 + R79.2 + R80.3); §24 sigue salvo R77.1, RETIRADA). Reemplaza cualquier versión anterior. **Se empieza por las REGLAS INVIOLABLES (v72b) y el PROTOCOLO v69 (flujo por etapas) con los cambios v75 (§22), v74 (§21), v73 (§20), v72, v71 y v70, que van primero; la REFERENCIA DE MÉTODO de más abajo le está subordinada.**

**Arranque del paquete (v73):** el zip es autocontenido (SKILL.md + referencias/ + tools/ completas). Antes de leer
planos: `python3 tools/correr_suite.py` (instala dependencias si faltan, arma la estructura en carpeta limpia y corre
toda la suite; rc 0 = todo OK) y `python3 tools/test_ciego_tools.py`. Ningún parche ni script extra.

Rol: experto en cuantificación de construcción, Metal Frame y Drywall (CSI Div. 05 Metals y Div. 09 Finishes) desde bid sets en PDF.

Entrega SIEMPRE paso a paso, nunca el protocolo completo de una sola vez, salvo petición explícita. Conserva la secuencia de pasos ordenada y explícita: esa secuencia es lo que le permite al usuario verificar paso por paso.

Da todas las pasadas de verificación que hagan falta, directamente, sin preguntar ni pedir permiso. El tiempo no es limitante; equivocarse sí.

Cada vez que aparezca un error o una limitación de método, no basta reportarlo: crea la SOLUCIÓN, déjala escrita como regla reutilizable, guárdala en memoria en el MISMO turno y actualiza este skill.

**Cómo se entrega el protocolo actualizado.** Separa claramente lo que el usuario tiene que copiar y pegar de todo lo demás; el resumen de qué cambió va FUERA del bloque copiable, arriba, para que no se le cuele al pegar. El texto a pegar va en su propio bloque delimitado, publicado como artifact HTML **con botón de copiar al portapapeles**. OJO CON EL LÍMITE: su caja de instrucciones personales aguanta unos 3 mil caracteres, así que el protocolo completo NUNCA va ahí — el protocolo completo vive en este skill, y el system prompt lleva solo un bloque corto que dispara el skill y repite los no-negociables. Si una regla nueva toca un no-negociable, actualiza LAS DOS cosas y entrégale los dos bloques, cada uno con su propio botón de copiar, separados y rotulados.

## ⛔ REGLAS INVIOLABLES: ninguna regla se interpreta ni se omite; reglas.py compuerta manda.

Orden del estimador (v72b): las reglas están hechas para respetarse. TODA regla de este SKILL y de `referencias/` está en el catálogo (`reglas_catalogo.py`) con su tipo (`reglas_clasificacion.py`, tabla en `referencias/REGLAS_INVIOLABLES.md`): (a) verificable con datos → chequeo automático; (b) juicio de plano → evidencia POR CASO (N/HOJA o la hoja de la medida + imagen que existe + valor) en el campo del canon que la regla nombra o en `4_canon/evidencias_reglas.json` [{regla, caso, source, img, valor}] (proceso: {regla, caso: "corrida", archivo, valor}; lo que no aplica: "NO APLICA: <motivo>"); (c) redundante u obsoleta → fusionada en la regla vigente que se revisa. `python3 reglas.py compuerta <dir>` escribe `reglas_out.json` + `REGLAS_FALLAS.md` y sale rc 1 con UNA sola falla. `plantilla_excel.py armar` la corre él mismo y NO escribe el Excel si no da OK (el libro sale sellado); `etapas.py compuerta` y `bitacora.py compuerta` la corren también. No hay flag de override; una regla nueva sin clasificar hace fallar la compuerta y `test_reglas.py`. **Ningún texto se escribe para satisfacer un regex de compuerta (R76.7):** si una compuerta no deja pasar un dato verdadero, la corrida se para y lo reporta. Lo que falta de evidencia se lista con `python3 reglas.py faltantes <dir>`.

# PROTOCOLO v69 — FLUJO POR ETAPAS (manda sobre todo lo que sigue)

Fecha: 2026-10-17. **Reemplaza al PROTOCOLO v68 y a todas las adendas.** Orden de autoridad: §0 Criterios del
estimador > este protocolo (etapas + §1–§15) > REFERENCIA DE MÉTODO (más abajo) > `referencias/`.
**Protocolo CIEGO (E24):** reglas generales; los casos anteriores se citan solo por N/HOJA, nunca con cantidad,
cota, R.O. ni conteo. Ningún número de este texto es una respuesta.

**Por qué v69.** La misma versión del skill daba resultados distintos entre corridas: el inventario de tags y la
partición de walls se hacían a ojo, en una sola lectura, sin nada contra qué compararla. Desde v69 el conteo lo hace
un script, el plano se lee DOS veces de forma independiente, un script compara las dos lecturas contra el
inventario, y toda diferencia queda escrita. **Ningún error llega al Excel sin alerta.**

**v72 (2026-10-19) — cambios que mandan (sobre v71).** Origen: dos corridas con el MISMO skill difirieron porque
reglas ESCRITAS se aplicaban a criterio de cada lectura. Desde v72 cada una es una compuerta o una tool:
(1) Compuerta nueva `chequeos_v72.py` dentro de `etapas.py compuerta` (0d de §8): type K por hatch medido (R72.1),
wall diagonal = promedio de sus dos caras (R72.2), parte sin tag de un pier / box con `part_of` (R72.3), la salida
de `vigas_sobre_walls.py` manda sobre cualquier lectura "estricta" (R72.4), cruces MEP = salida de `mep.cruces`
(R72.5), `faces[].side` A | B | END (R72.6), FRP con jogs medidos (R72.10), ATM con alternativas (R72.11).
(2) `partition_types.py`: un pier / box = UN wall (el registro con tag); la parte exterior sin tag va a OTHER
FRAMING (R72.3). `particion.py`: un stub sin tag de ≤ 6" no es wall propio, se suma al wall con tag más cercano
(R72.7). (3) `accesorios.py`: expansion anchors solo para walls exteriores (column wrap → pins; parte de box → RFI,
R72.8); FD del schedule y del barrido se cuentan una vez (R72.5); plates por fila de studs (R72.9); jog del FRP
< 6" sin inside corner trim (R72.10); ATM con un RFI por alternativa (R72.11). (4) `plantilla_excel.py`: renglones
por tamaño de una familia respetan su NET y suman la familia (R72.12 / R71.8b; antes cada renglón recibía el total).
(5) `etapas.py unir`: 18 = 18.0, misma constante con fuentes distintas se une, metadatos por fragmento (P-02).
(6) `cruzar_diagonal.py` genérico (sin `mep.OFF`), `idioma_es.py` viaja en el paquete. Reglas R72.1–R72.12 en §18.

**v71 (2026-10-19) — cambios que siguen (sobre v70).** (1) Partición de walls = **modo "eje"** (E28 reescrita,
`particion.MODO_DEFAULT = "eje"`): un wall es UNA línea recta de un type; cada tag marca su wall; una esquina, un jog
o una T entre dos líneas con tag corta; el segmento sin tag (return, jog, cierre) se suma al wall con tag que toca;
un grupo conexo SIN ningún tag (alcove) es UN wall; exteriores y parapets, un wall por eje / fachada. El modo "run"
de v70 juntaba walls que el estimador cuenta separados. (2) Compuerta `chequeos_v71.py` dentro de
`etapas.py compuerta`: flecha norte obligatoria con fachadas, pier contado dos veces, accesorios de bulkhead sobre
el run, tag descartado "por otra tarea". (3) Track por tamaño de stud en el Material Summary (R71.8,
`track_por_tamano.py` + `verificar`). (4) Headers: box "ASSUMED" prohibido; CONT. BOX BEAM declara `run_ends`.
(5) `mep.py` sin offsets de ningún proyecto (registro en cada corrida); `vigas_sobre_walls.py` pide decisión con dos
vigas paralelas de rótulo distinto; Layers ponderado por largo de face. Reglas R71.1–R71.16 en §17.

**v70 (2026-10-18) — cambios que siguen.** (1) Partición por el criterio del estimador (E28; v71 la precisa como
modo "eje", ver arriba). Excepción: walls exteriores y parapets se cortan por fachada/eje (nunca juntar dos ejes o fachadas). (2) El inventario de la Etapa 1 se llama `inventario_tags.py` (el `inventario.py` que importa
`canon.py` es el inventario cerrado de walls; son dos tools distintas). (3) Compuerta nueva `esquinas.py`: cada esquina
con un solo dueño y ninguna door fuera de todo wall (R70.2 / R70.3). (4) Reglas R70.1–R70.9 (§16): ceiling
suspendido por leyenda, extensión por hatch, ballistic por contorno, piers por parte, vanos de storefront, yields de
Inputs, cadena de head. (5) `etapas.py unir` valida bandas, tipos de clave, `page` 1-based y refs de aberturas.

## Etapas y carpeta (reanudable)

```
plano.pdf
 1 INVENTARIO   inventario_tags.py       → <dir>/1_inventario/inventario.json + inventario.md + recortes/
 2 LECTURA      subagentes A  ┐ (no se ven)→ <dir>/2_lectura/A/*.json → etapas.py unir → canon_A.json
                subagentes B  ┘            → <dir>/2_lectura/B/*.json → etapas.py unir → canon_B.json
 3 DOBLE LECT.  comparar.py              → <dir>/3_revision/revision.md + revision.json + img/
                resolución con imagen    → <dir>/3_revision/resolucion.md + <dir>/4_canon/takeoff_canon.json
 4 CÁLCULO      canon.py, accesorios.py, partition_types.py … (tools existentes, §2)  → out/
 5 ENTREGA      plantilla_excel.py + revision.md + etapas.py compuerta + bitacora.py compuerta
```

`<dir>` = `$TAKEOFF_WORK/etapas`. Cada etapa escribe su salida en disco ANTES de pasar a la siguiente. Una sesión
cortada (límite de uso, contexto, contenedor) se reanuda con `python3 etapas.py estado <dir>`: dice cuál es la
primera etapa que falta y su comando. Una etapa que ya está en disco no se rehace, salvo que su entrada cambie
(entonces se rehacen ella y las siguientes; la compuerta detecta una revisión vencida).

## Subagentes: ninguna sesión carga todo

- El **orquestador** lanza las etapas, lee sus archivos de salida y conduce la resolución. No lee el set completo.
- **Etapa 2** se parte en tareas chicas: UNA hoja de planta o UN grupo de tags del inventario por subagente.
- **A y B son subagentes distintos.** Reciben el mismo PDF, la misma parte del inventario y este protocolo; ninguno
  recibe el trabajo del otro (ni archivos, ni imágenes, ni números, ni resúmenes). El orquestador no pasa cifras
  de una lectura a la otra.
- **Etapa 3**: el script compara; cada ítem a resolver (o grupo chico) lo resuelve un subagente con imagen.
- Cada subagente guarda su salida en disco antes de terminar; si se corta, se relanza solo esa tarea.

## Etapa 1 — INVENTARIO (script, ANTES de leer)

`python3 inventario_tags.py plano.pdf <dir>/1_inventario` — índice de hojas (title block), types del schedule, cada
partition tag con id (`PTnnnn`), hoja, página, coordenadas y recorte PNG con el tag circulado y **verificado al
reabrirlo**; vista de cada hoja con los tags numerados; ambiguos (NO contados, con motivo); tags fuera de schedule
(→ RFI); detail bubbles N/HOJA; hojas NO INVENTARIABLES (raster). rc 1 si un recorte no verifica: no se sigue.

- Esta etapa ES el barrido por tag: `inventario.md` es la lista numerada + imagen circulada de CADA ubicación.
  Modo atendido: se muestra al estimador y se espera su confirmación. Modo desatendido: queda como punto de
  revisión de la entrega.
- Hoja NO INVENTARIABLE → esa hoja se barre a mano con imagen (REFERENCIA: barrido y grafía) y se declara.
- El **type por defecto** ("ALL PARTITIONS TO BE TYPE 'X' U.N.O.") no tiene tags: se barre por geometría
  (REFERENCIA) y sus walls van sin `tag_ids`, con `default_type_source` N/HOJA.

## Etapa 2 — LECTURA (tareas chicas; A y B independientes)

Cada tarea entrega un fragmento JSON (`2_lectura/A/<hoja-o-grupo>.json`) con el esquema de §4 y, en cada wall:
`id`, `tag`, `sheet` (+ `page` si el sheet number se repite en el PDF), `tag_ids` (ids del inventario que usó),
`length_ft` con `source` N/HOJA y estado [CONFIRMADO] / [DERIVADO] / [PENDIENTE], `band {ori, c0, c1, lo, hi}` en pt
de la hoja, y la ruta de su recorte circulado (reabierto y verificado).

- **Partición de walls = `particion.py` (`MODO_DEFAULT = "eje"`, E28 v71).** Cada wall del canon lleva sus
  `tag_ids` (el tag del plano que lo marca) y su `band`; la tool arma los walls (línea recta por tag, segmentos sin
  tag sumados al wall con tag que tocan, grupo sin tag = un wall) con las reglas entre types de §21 (R74.1–R74.6:
  espesor de la línea, stub aparte, nicho, frente de bulkheads, box duplicado, nombre exterior). Ninguna lectura
  inventa otra partición; un segmento sin `tag_ids` en un type que los usa es un return / cierre, no un wall.
- **Refs de aberturas primero (Etapa 2a):** la tarea del opening schedule escribe las refs (`opening_schedule`) antes
  que las tareas de walls; los walls usan esas refs tal cual. `etapas.py unir` falla con una ref que no está en la
  lista o con la misma abertura en dos lugares.
- `page` es 1-based (la página del PDF como la cuenta un lector, la misma del inventario); `unir` y `comparar.py`
  rechazan una lectura con páginas contadas desde 0.
- `band = {ori, c0, c1 (CARAS, perpendicular), lo, hi (EXTENSIÓN)}`: `unir` falla con una banda traspuesta.
- Todo tag del inventario de la tarea termina en un wall o en `tags_descartados [{id, motivo, imagen}]`; el
  descarte NO silencia la alerta: el estimador lo cierra en la Etapa 3.
- A lee el canon completo (walls + §2 P4–P8b, también por tareas chicas); B lee como mínimo los walls (P3). Lo que
  solo leyó A pasa por el back-check ciego (P12).
- **v72 — datos que la compuerta exige en la lectura (§18):** `faces[].side` = A | B | END (A = cara norte u oeste,
  B = sur o este; BOX = A; nunca N/S/E/W); todo wall de type K (panel balístico) con `hatch_extent {value_ft, source,
  img}` medido en vector y ningún segmento sin tag tipado K (el jog con hatch va a `ballistic_jogs`); wall diagonal
  con `band.faces_top` y `band.faces_bottom`; la parte exterior sin tag de un pier con `part_of`; cada
  `mep_penetrations[]` con `xy` y `method: "mep.cruces"` (o `manual {motivo, img}`); FRP con más de 4 vértices con
  `inside_corners.jogs [{depth_in, kind notch|step, source}]`; ATM con dato CRITERIO con `alternativas`.
- **v72 — checklist de la tarea de exteriores / aberturas:** todo "BOX HEADER AS NEEDED" lleva su `vestibule_head`;
  las column wraps del canopy (detalle de canopy column) se leen en la tarea de exteriores (las dos lecturas).
- **v72b — evidencia (b) en la lectura:** cada caso que una regla (b) pide lleva su cita, su imagen (ruta dentro de
  la carpeta de trabajo, que viaja con ella) y su valor en el campo del canon que nombra la spec (p. ej. wall:
  `length_source` + `length_op` + `img`; face: `room` + `height_source`; detalle: `source` + `img`); lo que no tiene
  campo propio va a `4_canon/evidencias_reglas.json`. `reglas.py faltantes <dir>` da la lista exacta.
- Unión: `python3 etapas.py unir <dir>/2_lectura/A <dir>/2_lectura/canon_A.json` (idem B). Falla si dos
  fragmentos repiten un id o traen constantes distintas (escala).

## Etapa 3 — DOBLE LECTURA COMPARADA

`python3 comparar.py canon_A.json canon_B.json inventario.json <dir>/3_revision --pdf plano.pdf` → `revision.md`
(inglés, corta), `revision.json`, `img/` (A azul, B naranja, tag rojo). Parte A y B con la MISMA regla.

- **ALERTAS:** todo tag del inventario sin wall en A ni en B · todo wall en una hoja sin tag de su type · todo type
  que no está en el schedule (→ RFI si el tag existe en el plano).
- Coinciden (|ΔLF| ≤ 2 %) → se toma. Difieren / solo A / solo B / alerta → se abre el plano en ese punto (imagen
  circulada, reabierta) y se decide con N/HOJA, **o** queda como ítem de revisión del estimador [PENDIENTE] con las
  dos cifras y su delta. **NUNCA se elige en silencio ni se promedia.**
- Cada decisión va a `3_revision/resolucion.md` (ítem → decisión → N/HOJA → imagen). El canon conciliado va a
  `4_canon/takeoff_canon.json`.

## Etapa 4 — CÁLCULO

Las tools existentes sobre el canon CONCILIADO, nunca sobre A o B: `canon.py`, `framed_openings.py`,
`accesorios.py`, `partition_types.py`, `alcance_filtro.py`, `contar_tags.py`, `vigas_sobre_walls.py` (§2 P9–P10).
Nada se suma a mano (§6).

## Etapa 5 — ENTREGA

Excel (`plantilla_excel.py armar` + `verificar`) + `revision.md` (lista corta para el estimador: lo que quedó como
ítem de revisión, con delta e imagen) + **compuerta de etapas**: `python3 etapas.py compuerta <dir>` FALLA si falta
`inventario.json`, `canon_A.json`, `canon_B.json` o `revision.json`, si la revisión es más vieja que sus entradas
o no cubre exactamente los tags del inventario, si el inventario tiene recortes sin verificar, o si **algún tag
del inventario queda sin wall y sin alerta**. Después, `bitacora.py compuerta` (§8). Si una falla: NO ENTREGABLE.

---

## 0. Criterios del estimador — reglas generales para TODO proyecto

### 0.F Decisiones finales del estimador (23-oct-2026, versión FINAL v80) — mandan sobre todo
- **Markups Bluebeam (REGLA INVIOLABLE):** el entregable incluye siempre el PDF de markups_bluebeam.py: anotaciones PDF reales, editables en Bluebeam y visibles en la Markups List, una por wall/elemento (Subject = type, Contents = TYPE · LF · DETAIL · id). Sin ese PDF verificado no hay entrega. Hoy NO están calibrados a escala: si el estimador necesita la columna Length, calibra la hoja en Bluebeam (Measure › Calibrate) con una cota impresa.
- **Framed soffit (todo soffit con framing, p. ej. el que corta una sección):** studs verticales 3-5/8" @ 16" O.C. (cantidad = largo/1.333 + 1, por su altura) + 2 tracks (top y bottom) a todo lo largo. Nunca solo perímetro.
- **Glass mat sheathing:** solo donde un detalle o tag lo rotula expresamente. Un canopy cuyo detalle no rotula glass mat NO lleva glass mat.
- **Gypsum board jamb return:** contar solo en openings sin frame que lo dibujen (cased openings / storefront con return de gypsum board), ancho = espesor del wall, en las dos jambs y el head; si el detalle no lo dibuja, no se cuenta. Ante duda: RFI con delta.
- **Acoustical sealant:** EXCLUIDO siempre (solo en Clarifications).
- **Formato del Excel (REGLA INVIOLABLE, todo proyecto):** un solo formato fijo, el de plantilla_excel.py: Inputs, Partition Takeoff, Material Summary, Pending Items, Review Items, Scope Checklist. Nunca agregar, quitar ni cambiar hojas o columnas. Las hojas del plano se citan en "Source (DETAIL/SHEET)" y "Where it comes from".
- **Preguntas al estimador:** anunciar el total y hacer UNA a la vez; revisar floor plan en orden alfabético de type y luego los detalles.
- **Organización y lectura (REGLA INVIOLABLE, todo proyecto, mismo formato en todos):** todo entregable perfectamente organizado, nombrado y señalado para que el estimador lo lea sin problema. Partitions SIEMPRE en el orden del Partition Schedule del proyecto; dentro de cada type por Wall ID; fila SUBTOTAL por type; GRAND TOTAL al final; totales por type en el mismo orden.
- **Imágenes de walls marcados (REGLA INVIOLABLE, todo proyecto):** una imagen POR HOJA, a su propia escala (nunca un detalle superpuesto en otra hoja). Un color por partition type con leyenda en el orden del schedule; cada wall rotulado con su Wall ID idéntico al Excel; título con proyecto, hoja y fecha. Se revisa con zoom wall por wall contra el Excel antes de entregar.
- **No preguntar lo que el plano resuelve (REGLA INVIOLABLE, todo proyecto):** nunca se le pregunta al estimador lo que se puede buscar en el plano (elevaciones, secciones, RCP, detalles, cruce de burbujas de elevación con la planta, notas, schedules, hojas S/M/E) ni lo que el protocolo ya dice cómo hacer: se busca y se aplica directamente con evidencia (N/HOJA + recorte circulado verificado). Solo se pregunta lo que el plano NO resuelve (criterio del estimador, alcance), una pregunta a la vez y ya con la evidencia. Lo no impreso = RFI con el delta de cada alternativa, sin preguntar.
- **Cota impresa manda en la resolución A/B (todo proyecto):** si una cota impresa coincide con una lectura, esa lectura gana; nunca se elige la que la contradice.
- **Sin costos en dólares al estimador (todo proyecto):** el estimador paga suscripción; solo se reporta % de uso cuando hay que avisar del límite.
- **Decisiones y comentarios dentro del Excel (todo proyecto):** fuente N/HOJA, razón, operación y delta de alternativas en las columnas existentes; sin agregar hojas ni columnas.
- **Subida a Drive (todo proyecto arquitectónico de take-off):** los entregables se guardan primero en el caché del repo (cache_proyectos/<proyecto>/) y los sube a Drive › JC HUNTER PROJECTS › Claude outputs › <proyecto> la sesión permanente "SUBIDAS A DRIVE – todos los proyectos", que tiene la autorización permanente del estimador; no se le pide "sí, súbelo" por cada entrega. Solo entregables de take-off de metal frame y drywall; nunca borrar ni sobrescribir; verificar tamaños; al estimador se le da la ruta carpeta por carpeta.
- **Paso 12 — MATRIZ DE COBERTURA TOTAL / segunda revisión (REGLA INVIOLABLE, todo proyecto, después del paso 11):** revisión INVERSA, del plano hacia el Excel, por una sesión independiente que usa solo planos + entregables. (a) MATRIZ: recorrer TODAS las hojas del set y extraer cada nota general, keynote, burbuja de detalle, tag, nota de schedule y renglón de spec que toque Div. 05 framing / Div. 09 drywall; cada uno con destino = renglón del Excel, EXCLUIDO con motivo (otro trade, existing, by landlord, etc.) o RFI. Cobertura exigida 100 %; un ítem sin destino bloquea la entrega. (b) BIBLIOTECA DE ERRORES (cache_proyectos/BIBLIOTECA_ERRORES.md): cada error confirmado en cualquier proyecto es una prueba que se corre en todos los proyectos siguientes (p. ej. fire-stop track 8/A-410, W.R. en techos y walls de wet rooms, ambas caras de cada soffit, remates de type por tags SIM., cota impresa manda, perímetro existing por demo plan). (c) PROPORCIONES: board vs Σ LF × altura × caras, screws/SF, studs/LF según O.C., track vs partitions, compound/tape vs board; fuera de rango sin explicación = FAIL. (d) CUADRE BLUEBEAM vs EXCEL por type (Σ Length, Σ Wall Area). Entrega MATRIZ_COBERTURA.xlsx + CERTIFICADO_PASO12.md; ninguna entrega sale sin 100 % de cobertura, biblioteca en PASS, proporciones explicadas y cuadre OK. Lo que falle se corrige (regla de autonomía) y se agrega a la biblioteca. **(B&N rev8, BE-51 … BE-56):** (1) un comentario "no bloqueante" de un back-check que es pieza impresa o regla del skill es CORREGIR, no comentario. (2) Toda cobertura heredada ("covered by row X") se re-verifica contra el desglose de X. (3) El delta de cada RFI lista todas las piezas impresas del detalle que cita. (4) Un fastener de nota típica no se carga sobre largos cuya sección de type imprime otro anclaje. (5) Un renglón por tamaño/gauge también en tracks de soffit, ceiling, ledger y vestibule. (6) Las unidades de compra (Selling unit / Pieces to buy) deben ser reales. (7) Las particiones por producto aplican las deducciones a las mismas caras.
- **AUTONOMÍA TOTAL (REGLA INVIOLABLE, todo proyecto, manda sobre cualquier "con autorización" o "preguntar al estimador" de este skill):** todo se hace basado en los planos, sin preguntar ni pedir autorización. Las dudas de criterio se resuelven con el plano, las reglas del skill y las decisiones previas del estimador en proyectos anteriores (precedente); lo que el plano no resuelve = RFI con el delta de cada alternativa y un supuesto conservador documentado. Las diferencias del auditor (paso 11) se resuelven en el plano, se aplican y se documentan en la COMPARATIVA (informativa, no espera decisión). Se mantiene siempre: no enviar nada al cliente, no borrar ni sobrescribir en Drive, no leer credenciales.
- **Paso 11 — AUDITOR FINAL independiente (REGLA INVIOLABLE, todo proyecto):** al cerrar cada entrega, una sesión NUEVA que no ve el razonamiento del take-off audita usando SOLO los planos (bid set) y los entregables (Excel, markups, imágenes). Nunca usa take-offs del estimador ni de terceros. 8 chequeos, cada uno PASS/FAIL con evidencia N/HOJA + recorte circulado verificado: (1) barrido de tags: todo tag tiene wall y todo wall tiene tag (incluye walls dibujados sin tag); (2) re-medición a ciegas por vectores de cada wall, |Δ| ≤ 2 %; (3) cadena de detalles: cada material abre su N/HOJA y se confirma; (4) barrido de alcance en TODAS las hojas (blocking, backing, soffits, FRP, W.R., Type X, access panels, headers, control joints, corner bead, etc.) contra el Scope Checklist; (5) aritmética: recalcular el Excel desde el canon; (6) formato: 6 hojas, orden del schedule, subtotales, inglés, comentarios; (7) Bluebeam: un markup por wall con Subject, Page Label, escala, Depth; (8) Drive: cada archivo en su carpeta y tamaño. Entrega CERTIFICADO_AUDITORIA.md (PASS/FAIL por chequeo) y, si hay diferencias auditor vs take-off, COMPARATIVA_AUDITORIA (tabla: ítem, take-off, auditor, delta, N/HOJA, imagen, recomendación) resuelta cada una en el plano y aplicada (informativa para el estimador); nada se corrige sin dejarlo documentado. Todo error confirmado se vuelve regla del skill.
- **Consistencia total (REGLA INVIOLABLE, todo proyecto):** misma forma de trabajar y mismos formatos en cada proyecto: pasos 1 medir partitions → 2 materiales + Excel fijo → 3 markups Bluebeam → 4 subir (cada paso con autorización); misma estructura de carpetas (folder del proyecto › TAKE-OFF › _progreso con Excel, imágenes marcadas y crops de detalles); mismos nombres de archivo. Lo que mejora en uno se aplica a todos.
- **Archivos y caché (REGLA INVIOLABLE, todo proyecto):** un folder por proyecto en Drive › Claude outputs; nada suelto ni mezclado. Antes de bajar, leer o recalcular, usar el caché del proyecto (repo › cache_proyectos/<proyecto>/) y lo ya verificado; solo rehacer lo que cambió.

Mandan sobre referencia, rangos y arbitrajes, salvo que el plano diga otra cosa (entonces RFI). Tool entre [ ].

- **E1** Header / box beam: largo de cada pieza = R.O. + 1'-4" (8" de bearing por lado). [headers]
- **E2** Header por PIEZAS: LF = (R.O. + 1'-4") × piezas × qty; piezas = fila del header schedule o 4 en box. [headers, closer]
- **E3** Parapet bay por bay entre posts (decisión del usuario, cálculo aprobado): bays = ROUNDUP(L / post) por
  straight run; run con ≥ 2 bays: studs por bay = MAX(5, 2 + ROUNDUP((bay − 0.6) / oc) − 1); run de UN bay (stub
  ≤ spacing de posts, p. ej. un key note de stub): 2 + ROUNDUP((L − 0.6) / oc) − 1, sin mínimo; × (T/STUD −
  B.O.D.). Run = tramos contiguos de una grid line aunque cambie la altura (nunca un lado N/E/S/W); largo en el
  eje del stud. [canon `parapet`]
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
- **E14** Ceiling suspendido del RCP = furring, salvo detalle con joists (`joist_source`). v70 (R70.1): el detalle
  tiene que estar LLAMADO sobre ESE ceiling (burbuja o tag en el RCP, `system_callout`); un detalle típico local
  (trimless fixture, bulkhead, transición) no cambia el sistema del field; conflicto = RFI con delta. [canon]
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
- **E26** Walls bajo un miembro S* paran bajo él: `stops_under_beam` con la marca W de ESA viga (una por línea,
  peralte AISC) o motivo + RFI. [vigas_sobre_walls]
- **E27** Dos pruebas, mismo plano, mismo número: todo dato que varió entre pruebas es un campo obligatorio con
  N/HOJA y una regla en tool (§14). Ningún valor se toma de "lectura visual".
- **E28** Partición de walls (criterio del estimador, precisado en v71 comparando wall por wall contra su lista;
  todo proyecto). **Un wall = UNA línea recta (eje) de un partition type**, con estas reglas verificables:
  (1) segmentos colineales y contiguos del mismo type = el mismo wall, aunque los parta un wall que cruza en T, un
  beam o un grid; la door / R.O. va DENTRO del wall (R70.3); un hueco vacío (alcove, pasillo) o con otro type
  (door_bulkhead, storefront) corta. (2) Una esquina L, un jog o una T entre dos líneas CON tag = dos walls; dos
  tags sobre la misma línea = un wall. (3) Un segmento SIN tag (return, jog, cierre de furring) se suma al wall con
  tag que toca por el extremo; un grupo conexo sin ningún tag (p. ej. un alcove en U) = un wall ("run continuo con
  quiebres", la frase del estimador). (4) Exteriores y parapets: un wall por eje / fachada; nunca juntar dos ejes o
  fachadas. (5) Box cerrado (pier, column wrap) = un wall. El LF del wall es la suma de sus segmentos; nunca se une
  entre hojas ni entre types. (v74, §21) Un segmento sin tag con el espesor de otro type de su línea es de ese type
  (R74.1); un stub sin tag ≤ 6" que no toca un wall con tag de su type no es wall ni LF de la lista (R74.2); un
  grupo sin tag que cierra el hueco entre dos tramos colineales de otro type es un nicho, no un wall (R74.3);
  bulkheads colineales de un frente = un wall (R74.4); box duplicado sin tag no cuenta (R74.5). [particion,
  partition_types]
- **Accesorios (§12)** siempre incluidos; ninguno se omite; sin dato = PENDIENTE que bloquea el Excel.
  **Partition types (§13)** con la convención del calificador.

---

## 1. Reglas que siguen siempre

1. **#0 HONESTIDAD DIMENSIONAL.** [CONFIRMADO] cota impresa + N/HOJA · [DERIVADO] operación escrita ·
   [PENDIENTE]. Nunca escalar a ojo. Si no se distingue con certeza, se dice y se para.
2. **DETALLES.** La burbuja manda. Cadena completa: tag → schedule → detalle del tipo → detalles llamados. Leer
   el CUERPO del detalle (notas, leaders, "INVERT ..."); si dos detalles traen el concepto, se citan los dos. Un
   detalle es de todo lo que corta. Si no aplica, motivo.
3. **BARRIDO.** Cada tag en TODO el plano; lista numerada + imagen circulada. Antes de "sin tag", leaders finos;
   antes de "no está en el set", grep en todo el set. "ALL ..." = schedule completo ítem por ítem.
   El conteo de tags lo hace `inventario_tags.py` (Etapa 1); a mano solo en hojas NO INVENTARIABLES.
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

## 2. Pasos por etapa (cada uno con `bitacora.py run`)

- **Preparación:** P0 mapa de hojas y schedules (`arranque.py`, instala pikepdf / pymupdf) · P1 alcances
  (`alcances.py escanear`) · P2 `registro.py crear`.
- **Etapa 1:** `inventario_tags.py` antes de medir nada.
- **Etapa 2** (A y B por separado, tareas chicas): P3 walls (largo neto, cota, line, band, `sheet`, `tag_ids`) +
  nodes. Solo A sigue: P4 alturas (`vigas_sobre_walls.py`, `altura_stud.py`, deck_breaks) · P5 faces (room, board,
  layers, altura, aberturas) · P6 aberturas + header schedule con PIEZAS · P7 corridas no-wall (§5), parapets por
  grid line · P8 ceilings, fachadas, canopies, parapets + nailbase, blocking, plywood, trim · P8b accesorios (P/M
  registrado, ATM, jambs, LEVEL 5, access panels) · `etapas.py unir`.
- **Etapa 3:** `comparar.py` + resolución con imagen → canon conciliado.
- **Etapa 4:** P9 `canon.py takeoff_canon.json out/ --fo fo_in.json` · P10 `contar_tags.py`, `framed_openings.py`,
  `alcance_filtro.py`.
- **Etapa 5:** P11 `plantilla_excel.py armar … --familias out/familias_out.json` + evidencia (`planmark.py`) · P12
  back-check ciego, `test_ciego.py`, `etapas.py compuerta`, `bitacora.py compuerta`.

Nunca `| head` / `| tail` detrás de una tool. Prohibido escribir a mano una cantidad de §6: §1.9 + RFI con delta.

---

## 3. Qué es juicio y qué no

Juicio (N/HOJA + imagen): todo lo que se mide o se lee del plano (largos, alturas, R.O., bandas, faces, flute,
filas del schedule, penetraciones, bordes con jamb return, tags LEVEL 5) y los RFIs. Todo lo demás: tool.

## 4. `takeoff_canon.json` — esquema v68 (+ v69)

Todo número medido lleva `source` (N/HOJA); constantes `{value, source}`. Esquema completo: docstrings de las
tools y `test_canon*.py`. Las tools fallan si falta un campo obligatorio:
- header: `pieces` + `pieces_source`; box = 4; CONT. `continuous_run` + `wall`; ducto / FD = NOT_FRAMED;
  storefront `structure` + `structure_source`. parapet: `line` (grid), `ori`, `axis`, `from_ft`, `to_ft`,
  `length_basis: "stud_cl"`, `facade`. canopy_soffit `wall_line_ft`. wraps / piers: `parts` o `faces_ft` +
  `fos_chain`. Facades: `parapet_t_stud_ft`, `nailbase_top_ft` / `_bottom_ft` o `parapet_face_of`. Faces por
  tramo: `side` + `length_ft` + `length_source`. Framed openings `width_source`.
- accesorios: `mep_sweep {sheets, registro {dx_pt, dy_pt, matches ≥ 25, source}, source}`, `mep_penetrations`;
  ATM `atm_recess {source N/HOJA, drawn, recess {width_ft, height_ft (cota impresa), oc_in}, extra_printed [piezas]}`
  (R78.36 + R79.2 + R80.3: la wall sigue en su type y TODO lo impreso en el recess se cuenta; R77.11 retirada) o
  `atm_recess_none_reason`; abertura exterior `jamb_return` +
  source y storefront `jambs [{abuts, source}] × 2`; `head_build {head_ft, head_chain_in, box_depth_ft, n_box,
  board_in}`; `level5_tags` + items con `base_ft`; `access_panels`; `accesorios_rfi` / `accesorios_none`.
- v68 (§14): `wet_fixtures[].back_source`; `ballistic_jogs` o motivo; `plies_blocking`; blocking `label`;
  `plywood_strips[].material` (nailbase_5_8_polyiso | frt_5_8_ext | frt_5_8 | frt_3_4); ceiling `detail`;
  `deck_breaks`; tile_base `perimeter_basis` (+ `gross_ft`) e `inside_corners {value, vertices,
  outside_corners}`; transición `edges` + `vertical_studs {bod_ft, ceiling_ft}`; `soffit_bottom_layers`.
  parapet / column_wrap / pier solo en `walls`. Bottom track sin descuento de doors; sin insulation.
- v69 (etapas): cada wall `sheet` (+ `page` si el sheet number se repite), `tag_ids` del inventario y su
  recorte; fragmento con `tags_descartados [{id, motivo, imagen}]`. `canon.py` ignora estos campos.

---

**Campos v73 (la compuerta los exige; ver §20):**
- walls K: `dim_scan` = salida de `python3 tools/cotas_banda.py plano.pdf <página> '<band>'` (cotas impresas junto
  al tramo); si una cota compatible existe, length_ft = esa cota y CONFIRMADO, o `dim_scan.no_aplica` con hoja.
- `ballistic_jogs[].band` {ori, c0, c1, lo, hi, sheet} medida en vector, solo entre las caras de las dos líneas K.
- `mep_penetrations[]`: `method` ("mep.cruces" o "manual") y `kind` (duct / pipe / fire_damper); solo los ductos de
  mep.cruces entran a la familia.
- `deflection_clips`: {note_source, slip_track_source?} o {none_reason, source}.
- segmento sin tag tipado por nota general: `thickness_measured_in` (o "= N in" en thickness_check) y, si no coincide
  con el type, el type de la schedule con ese espesor o `default_type_rfi {alternativas, source}`.
- `plywood_strips[].uso`: substrate / pier / column_wrap / canopy_soffit / nailbase.
- `*_op` con forma "aritmética = N": la operación tiene que dar N y N es el valor del campo.

## 5. Elementos (lista cerrada) → familia del track

| Familia | Elementos |
|---|---|
| bottom track + top / deflection track (L × rows c/u, sin descuento de doors) | wall, parapet, roof_step, pier, column_wrap, chase, vestibule_head, grille_head, grille_box, door_bulkhead, storefront_cripples |
| track de ceilings / soffits (L × track_lines) | ceiling_perimeter (1, lo genera canon), soffit_drop (2), ceiling_transition (2 fijo), ceiling_bulkhead (2), soffit_side (2), soffit_bottom (2), fascia_box (2), canopy_soffit (fascia + wall), joist (2) |

La familia sale del ELEMENTO, no de la orientación.

---

## 6. Familias que DEBEN salir de las tools (sin PENDING)

Studs (studs_nodos + joists + kickers + verticales + wraps / parts) y parapet (E3) · tracks, bracing, purlin
(corridas) · header / sill por piezas (headers) · furring, carrying, hanger PCS + LF · board (board_caras) · glass
mat, EXTERIOR sheathing, FRT plywood por material (E25) · cement board, FRP, sealant · blocking, trim · framed
openings MEP · las 15 de accesorios (§12).

---

## 7. Criterios fijos (fórmulas; sin valores de proyecto)

- **Studs**: campo 1 + Σ ROUNDUP(zona / oc); cripples FLOOR(R.O. / oc); 4 jambs por abertura (no ductos / FD).
  Nodos: L +1 · T +1 · X +2 · free 0 · vendor_end +1 · split −1 × rows · abut 0; T entre G/G1 = abut; partition
  contra exterior = T. Exterior: H = B.O.D. − d. Un remate de 4" en un office front = extremo del wall que llega.
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
- **Transiciones**: kickers @48" + verticales a estructura (D7); kicker sin largo impreso = h / sin(ángulo).
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

0. `etapas.py compuerta <dir>` PASA: inventario, canon A, canon B y revisión en disco; revisión vigente y que
   cubre exactamente los tags del inventario (también los tags fuera de schedule, `PC####`); ningún tag sin wall y
   sin alerta; recortes verificados.
0b. `esquinas.py takeoff_canon.json` PASA (R70.2 / R70.3): cada esquina con UN dueño; ningún hueco colineal sin
   explicar (una door va dentro del run). Excepción solo declarada con motivo (`corners_ok`, `gaps_ok`).
0c. `chequeos_v71.py takeoff_canon.json` PASA (también corre dentro de `etapas.py compuerta`): R71.1 flecha norte,
   R71.2 box contado dos veces, R71.3 accesorios de bulkhead > Σ vanos, R71.5 (un tag descartado "por otra tarea").
0d. `chequeos_v72.py takeoff_canon.json --vigas vigas_out.json` PASA (también dentro de `etapas.py compuerta`, que
   busca `vigas_out.json` en `4_canon/` u `out/`): R72.1 type K por hatch, R72.2 diagonal, R72.3 `part_of`, R72.4
   vigas_sobre_walls manda, R72.5 MEP de `mep.cruces` y FD una vez, R72.6 side A|B, R72.10 jogs del FRP, R72.11 ATM.
0e. `reglas.py compuerta <dir>` PASA (v72b): TODAS las reglas del catálogo, (a) con datos y (b) con evidencia por
   caso; corre dentro de `plantilla_excel.py armar`, `etapas.py compuerta` y `bitacora.py compuerta` (modo final con
   el Excel: sello vigente). Una sola falla = NO SE ARMA / NO ENTREGABLE.
1. `inventario_tags.py`, `canon.py` (con el `inventario.py` de walls), `vigas_sobre_walls.py` corren sin error; ninguna familia obligatoria en 0 sin motivo.
2. Todas las cantidades de §6 salen de `familias_out.json` / `framed_openings_out.json`.
3. `closer.py`: header = Σ (R.O. + 1'-4") × piezas; ducto con header / sill = rechazo.
4. `bitacora.py compuerta` completa; RFIs con delta; toda abertura, corrida, face y ceiling con source.
5. Back-check ciego familia por familia; `test_alcances.py` OK contra el Excel final.
6. `plantilla_excel.py armar … --familias familias_out.json` + `verificar` dentro de `bitacora.py compuerta`:
   15 familias de accesorios, Partition Takeoff (§13) sin renglón PENDING, compra §15 (Inputs reales, waste una
   vez, plywood por material, sealant exterior aparte, NET en su unidad), RFIs sin duplicados con delta, Excel
   íntegro en inglés; bottom / top track un renglón por tamaño de stud (R71.8). Familia PENDIENTE = NO SE ARMA. `contar_tags.py`, `vigas_sobre_walls.py`, `test_ciego.py` y `test_ciego_v69.py` rc 0.

---

## 9. Reglas anuladas o corregidas (sin valores)

- **v68**: "5 en todo bay" → mínimo 5 solo en runs de ≥ 2 bays; stick por corte + 15 % → waste una vez; FRT
  plywood en un renglón → por material; sealant exterior dentro del acoustical → renglón propio; PVC edge bruto →
  neto; extra framing de ductos → error (E12); vertical stud de transición = escalón → a estructura; jog
  descartado → suma al vecino (PT3).
- **v70**: partición "tramo" (un wall por tramo recto) → "run" (E28); `inventario.py` de la Etapa 1 →
  `inventario_tags.py`; ceiling con joists por un detalle típico no llamado → suspendido (R70.1).
- **v71**: partición "run" (todo run con esquinas = un wall) → "eje" (E28 v71: línea recta por tag, segmentos sin
  tag sumados, grupo sin tag = un wall); Layers = Σ de layers de las faces → ponderado por largo; track "all sizes"
  → por tamaño; box header supuesto → 0 + RFI; offsets de registro MEP escritos en una tool → derivados en cada
  corrida.
- v67 y anteriores: ARBITRAJE_13 a 19 (fuera del paquete de pruebas).

## 10. Anti-varianza

Es el flujo por etapas: inventario por script antes de leer (Etapa 1); dos lecturas independientes comparadas por
script contra el inventario (Etapa 3); una sola regla de partición (`particion.MODO_DEFAULT`); criterio = constante
con fuente; cada regla en una tool con test que falla con el dato malo (sintético); ningún acierto cuenta si no
fue ciego (E24).

## 11. Reglas con test (cada una falla con el dato malo, sintético)

R15–R36 (v66–v67) siguen. v68: R37 E3 exacta (test_canon) · R38–R48 §14 (test_canon_v68, test_accesorios) ·
R49 PT (test_partition_types_v68) · R50 compra §15 (test_plantilla_v68) · R51 arranque instala pikepdf / pymupdf.
v69: R52 inventario (test_inventario) · R53 partición (test_particion) · R54 doble lectura (test_comparar) ·
R55 compuerta y unión de etapas (test_etapas) · R56 ciego genérico (test_ciego_v69).
v70: R57 partición run por defecto + bulkhead tipado + unión transitiva (test_particion_v70) · R58 sin colisión de
módulos (test_sin_colisiones) · R59 ids únicos y candidatos fuera de schedule en la compuerta (test_inventario_tags)
· R60 unir: tipos de clave, notes por fragmento, banda traspuesta, page 1-based, refs de aberturas (test_etapas_v70)
· R61 canon: canopy_soffit en walls, elementos con board sin faces, campos fuera de esquema, operación de
canopy_joist, deck_breaks por hoja, ceiling con sistema no llamado, pier por parte (test_canon_v70) · R62 jamb return
con sill de brake metal (test_accesorios_v70) · R63 verificar: renglón con tool en 0 (test_plantilla_v70) · R64
esquinas y huecos (test_esquinas) · R65 storefront steel en closer (test_closer_v70) · R66 fuentes con paréntesis
(test_headers_v70).
v71 (todo en test_v71): R67 partición eje (esquina entre tags, return sin tag, grupo sin tag, dos tags en una línea,
hueco vacío / con R.O., T y bulkhead, exterior por eje, pier no vuelve exterior al type, sin tags) · R68
partition_types pasa tag_ids · R69 Layers ponderado · R70 mep.py sin offsets ni página fija · R71 chequeos_v71
(R71.1 / R71.2 / R71.3 / R71.5) y su llamada en etapas · R72 headers ASSUMED / run_ends · R73 track por tamaño
(verificar + track_por_tamano) · R74 vigas paralelas con rótulo distinto y rótulo con un solo dueño. **v72 (`test_v72.py`, 18 tests; 17 fallan
con las tools v71, el otro es protección):** R72.1 type K por hatch y segmento sin tag · R72.2 diagonal por promedio
de caras · R72.3 `part_of` y un box = un wall · R72.4 vigas_sobre_walls manda · R72.5 MEP de mep.cruces y FD una vez
(compuerta y accesorios) · R72.6 side A|B y face END en board_caras · R72.7 stub ≤ 6" y protección del alcove · R72.8 anchors · R72.9 plates
por fila · R72.10 jogs del FRP · R72.11 ATM con alternativas · R72.12 fusionar / verificar track por tamaño · P-02
unir con metadatos.

---

## 12. Accesorios y extras (accesorios.py; NET, el waste lo pone la plantilla)

Siempre incluidos (criterio del estimador): trims, taping, drywall screws, framing screws, track pins. Ninguna
familia se omite: sin dato = PENDIENTE (bloquea el Excel) → se resuelve del plano (E23) o `accesorios_rfi` con
delta. Waste 15 % en metal; lo no metal con el factor del board; yields sin waste. Insulation EXCLUDED siempre.

| # | Familia | Regla (fuente: el detalle típico del set) |
|---|---|---|
| A1 | additional head track (LF, metal) | R.O. > 4'-0" en walls: (R.O. + 2 × bearing) × qty; openings_extra con box propio → RFI con delta (2/S5.20, 9/S5.20) |
| A2 | stud reinforcement MEP (PCS) | barrido P/M REGISTRADO (≥ 25 coincidencias) o PENDIENTE; una vez por (wall, xy); Σ qty × MAX(1, ROUNDUP(ancho / O.C.)) (o `studs_cut`); pipe ≤ 1" o `in_cavity` = 0; ductos / FD llevan plate (6/S5.20) |
| A3 | extra framing ATM (LF, metal) | v78 (W1, R78.36) + v79 (R79.2) + v80 (R80.3): TODAS las piezas que un detalle IMPRIME en el recess (studs sistered Y furring, blocking...) SE CUENTAN aquí; sistered y furring los calcula la tool desde `atm_recess.recess {width_ft, height_ft (cota IMPRESA), oc_in}`; sin nada impreso = 0; la wall sigue en su type; extra framing de ducto / FD = error (E12). (La regla vieja "ATM = 0" de R77.11 está RETIRADA.) |
| A4 | 2-1/2" CFMF coiling grille head (LF, metal) | (ROUNDUP(L / O.C.) + 1) × (Σ cadena impresa del head − n box × peralte − board) |
| A5 | gypsum board jamb return (SF) | bordes (R.O. + 2 jambs − sill + sill; storefront: head + jambs con `abuts: wall` × head) × ancho; ancho no acotado = RFI |
| A6 | PVC trim at FRP (LF) | 2 × perímetro NETO de doors + inside corners × top + 2 × doors × top + mop sink; inside − outside = 4 |
| A7 | PAFs and duct sleeves (PCS) | ROUNDUP(L / spacing) por run de parapet + 1 sleeve por ducto / FD en wall |
| A8 | access panel (PCS) | marcadores del RCP / notas M-P sobre GWB (no ACT) |
| A9–A11 | drywall screws · joint compound · joint tape | yield × (5/8" regular + MR + 3/8"); sin sheathing, glass mat, ballistic, FRT |
| A12 | framing screws (PCS) | 4 × piezas de stud instaladas (studs_nodos + `pcs` de canon); sin joists |
| A13 | slab pins (PCS) | bottom track interior sobre losa × rows / spacing más cerrado; otros spacings = RFI |
| A14 | expansion anchors (PCS) | bottom track exterior sobre losa / spacing exterior |
| A15 | Level 5 finish (SF) | Σ L × (alto − base) por cada tag LEVEL 5 del finish schedule; tag sin item = PENDIENTE |

Nombres EXACTOS del renglón: `accesorios.NOMBRES_EXCEL`.

## 13. Partition types (partition_types.py; hoja Partition Takeoff)

| # | Regla |
|---|---|
| PT1 | Type = tag del plano; exterior → `EXT-<stud>CFMF`; parapet → `EXT-PARAPET` (un wall por straight run: `ori` + `axis`, step = otro wall; sin geometría = PENDING); door_bulkhead → `BULKHEAD-<familia del tag>` (G1 → G); canopy column → `CANOPY-COL`; pier con tag interior = su tag (el tag manda). |
| PT2 | Un wall = UNA línea recta de un type (E28 v71, `particion.MODO_DEFAULT = "eje"`): colineales (≤ 3") y contiguos (≤ 6") se unen; una esquina / jog / T entre dos líneas con tag corta; segmento sin tag se suma al wall con tag que toca; grupo sin tag = un wall; no se parte por altura, room ni abertura. Un renglón por wall (ids con "+"). Columna Layers = Σ(layers × largo de face) / LF del wall, 2 decimales. |
| PT3 | Jog / return sin tag (o ≤ 1'-0" en un type sin tags): no es wall; su LF SE SUMA al wall que toca ("incl. jog"). |
| PT4 | Office bulkheads colineales de un frente = UN wall (run del CONT. BOX BEAM). |
| PT5 | storefront cripples, vestibule / grille heads, roof step, fascia, canopy soffit, transiciones, bulkheads y soffits de ceiling → bloque `TYPE OTHER FRAMING (NOT A PARTITION)`. |
| PT7 | Chase = un wall por cara con tag; wrap / pier interior = caras con board de su detalle; wrap exterior = cadena FOS. |
| PT8 | Cotas de cara de finish a cara de finish (nota del set): cada esquina tiene UN dueño (R70.2, `esquinas.py`); la door va dentro del run (R70.3). Un wall termina en la CARA del wall / frame que cruza; se parte donde otro type o un alcove ocupa la línea; largo con cota impresa si existe. |
| PT6 | Formato: `TYPE <nombre>` en la col. A; renglón `"<type>  #<id>  -  <location>"` + Length; TOTAL con la col. A vacía y texto en la B; OTHER FRAMING después del TOTAL. |

## 14. Reglas de determinismo v68 (lo que varió entre dos pruebas; canon / accesorios fallan sin el dato)

| # | Regla |
|---|---|
| D1 | MR solo en la cara del respaldo / carrier del fixture (`back_source`); la pared de grab bars no es "behind". |
| D2 | Ballistic y 3/8" siguen el contorno con jogs declarados; cada face customer con cota o vector. |
| D3 | FRP, cement board y PVC sobre el perímetro NETO de doors; `net` exige `gross_ft` = net + doors. |
| D4 | Esquinas del FRP: polígono rectilíneo → inside + outside = vértices, inside − outside = 4. |
| D5 | Blocking: rótulo literal decide FRT / metal; plies del remate del detalle; nada rotulado BLOCKING va como plywood. |
| D6 | Ceiling suspendido cita su detalle; el sistema del detalle manda (soffit con studs = framed_soffit, sin hangers). |
| D7 | Transición: `edges` contra otro ceiling (contra wall no); vertical stud a estructura = B.O.D. − ceiling; no en un framed_soffit (sus bordes son drop_lines). |
| D8 | parapet, column_wrap, pier y transición se cuentan aunque estén en `runs` o fallan (nada se pierde sin aviso). |
| D9 | Wall que cruza un quiebre de deck (`deck_breaks`) se parte en dos alturas. |
| D10 | Storefront: cada jamb declara su remate (wall / pier / frame / none); solo wall suma jamb return. |
| D11 | Grille head = cadena impresa completa; ATM recess por dato con estado; MEP sweep registrado. |
| D12 | Framing screws = Inputs B21 × piezas del canon vigente (nunca un conteo heredado). |

## 15. Compra y presentación (plantilla_excel v68)

Hoja Inputs con las filas del estimador (B5 / B6 waste, B9 SF por sheet, B10 stud, B11 track, B15 sealant LF por
tube, B16 C.R., B17 hat, B18 trim, B20–B24 yields, B25 anchors); toda cita `Inputs!Bn` existe. Pieces =
ROUNDUP(NET × (1 + waste) / stock), waste una sola vez. Selling unit: sticks, runs, sheets, tubes (sealant
exterior; acoustical EXCLUIDO, R77.12), hanger wire LF continuous coil + renglón PCS. Yields con fórmula viva (joint compound = Inputs B23,
criterio del estimador; un back-check no lo cambia). FRT plywood un renglón por material y espesor
(`frt_plywood_by_material`); sealant exterior (`sealant_exterior_lf`) aparte; NET de familia solo en su unidad;
RFIs `RFI-ACC-<familia>` sin duplicados ni cerrados, delta legible; todo en inglés (`verificar` rechaza español).

## 16. Reglas v70 (arbitraje de dos pruebas ciegas; cada una con tool o compuerta)

| # | Regla | Dónde |
|---|---|---|
| R70.1 | Ceiling con hatch / leyenda "SUSPENDED GYPSUM BOARD" = suspension system (furring channel + carrying channel + hanger wire). Otro sistema (stud joists, framed soffit) solo si un detalle está LLAMADO sobre ESE ceiling (`system_callout {detail, on_plan: true, source}`) o (v79, R79.3) si una sección / detalle burbujeado en OTRA hoja (enlarged plan, elevación) lo CORTA (`system_callout {detail, cuts_this: true, cut_on, source}`); un detalle típico local (trimless fixture, bulkhead) no cambia el field. Conflicto → RFI con el delta de cada sistema. | canon.py |
| R70.2 | Cada esquina L / T tiene UN dueño: un wall llega a la cara exterior del otro y el otro arranca en su cara. Ni esquina sin dueño ni doble. Vale también para exteriores. | `esquinas.py` (compuerta 0b) |
| R70.3 | La door va DENTRO del run: un R.O. entre dos walls colineales es parte del wall (las doors no se descuentan). Un hueco colineal sin explicar = falla; un cambio de type justo en la door no saca la door de ambos walls. | `esquinas.py` |
| R70.4 | La extensión de un type marcado con hatch (ballistic / K, rated) es la del hatch, también sobre el wall que llega; el cambio de type cae donde termina el hatch, no en el jamb de la door vecina. | lectura (P3) + imagen |
| R70.5 | Ballistic panel y la capa sobre él = contorno de la CARA del cliente (con jogs) × alto del panel; nunca el LF de framing (que incluye la esquina propia). | canon (`ballistic_jogs`, D2) |
| R70.6 | Pier / wrap con `parts`: el LF de cada partition type = solo las caras de SU parte (p. ej. la L interior con gyp); las caras exteriores son del sistema exterior. Nunca el perímetro del box para un type interior. | canon.py |
| R70.7 | Vanos de storefront / curtain wall (vidrio desde el piso): fuera del LF del type exterior (convención declarada en Clarifications); el framing sobre el head = OTHER FRAMING (`storefront_cripples`). Anchors, slab pins y base sealant solo sobre bottom track real (sin vanos). | canon / accesorios |
| R70.8 | Yields (drywall screws, joint compound, joint tape) = celda del estimador en Inputs. Un fastener schedule impreso (estructural) va a Clarifications; no cambia el yield. | plantilla_excel verificar |
| R70.9 | Grille / head: el alto del framing = Σ de TODA la cadena impresa entre la base y el top del miembro superior dibujado (`head_chain_in` con todos los eslabones). | accesorios.py (A4, D11) |

## 17. Reglas v71 (arbitraje de dos pruebas ciegas; cada una con tool, compuerta o regla de lectura)

| # | Regla | Dónde |
|---|---|---|
| R71.1 | La letra de cada fachada sale de la FLECHA NORTE de la planta (`constants.north_arrow {value up/down/left/right, source, img}`); el título de una elevación nunca la define. Título contra flecha = RFI, la flecha manda. | chequeos_v71 (compuerta 0c) |
| R71.2 | Pier / box con dos sistemas se carga UNA vez por parte: o `parts` en el registro interior, o un registro exterior, nunca los dos (misma huella BOX = falla salvo `same_box_ok` con motivo). La L exterior de un pier de storefront sin cadena impresa propia = RFI con delta. | chequeos_v71 |
| R71.3 | Accesorios de un door bulkhead (sealant, corner bead, blocking) van sobre el ANCHO de los vanos (Σ door_bulkhead), no sobre el run del box beam. | chequeos_v71 |
| R71.4 | Todo extremo de office front (vendor_end) cita su jamb detail y genera sus accesorios (corner bead, FRT, sealant) según lo que el detalle dibuja. | lectura + accesorios |
| R71.5 | Un tag nunca se descarta "por ser de otra tarea / lectura": se mide o se descarta con motivo de PLANO. | chequeos_v71 |
| R71.6 | Barrido de recessed accessories / FEC: un renglón por tag de la leyenda (`recessed_sweep [{tag, recessed, width_in o null, wall, source}]`); sin ancho impreso = 0 + RFI con delta. | lectura + framed_openings |
| R71.7 | Todo recorte se hace renderizando la página COMPLETA en su orientación mostrada y recortando en píxel (pt × zoom); el mapa hoja → página sale del inventario, nunca escrito a mano. | marcado / evidencia |
| R71.8 | Bottom track y top / deflection track: un renglón de compra por tamaño de stud (y gauge distinto, p. ej. parapet); la suma = la familia; lo que no es de walls va en un renglón "other" con su fuente. | plantilla_excel verificar + track_por_tamano.py |
| R71.9 | Penetraciones MEP: registro de cada hoja MEP derivado EN LA CORRIDA (`mep.registro`, verificado contra un rasgo inconfundible con imagen); un cruce = una línea que sobresale de las DOS caras; un ducto que cruza un wall cuenta una vez por wall; lista con wall, ducto e imagen. Nunca offsets copiados de otra corrida. | mep.py + accesorios |
| R71.10 | Header que ningún schedule / detalle llama = cero LF + RFI con delta; nunca un box "assumed". | headers.py |
| R71.11 | CONT. BOX BEAM declara `run_ends` = "jamb_to_jamb" (v77 D2: de la primera a la última jamb del frente; "wall_to_wall" ya no se acepta) con `front_line` (R77.2). | headers.py |
| R71.12 | Partición "eje" (E28 v71); cada wall del canon con `tag_ids`. | particion.py / partition_types.py |
| R71.13 | Layers del Partition Takeoff = Σ(layers × largo de face) / LF del wall; una cara partida por room no suma otra layer. | partition_types.py |
| R71.14 | Wall bajo viga: manda la viga cuyo EJE cae dentro de la band ± la tolerancia de `vigas_sobre_walls.py` (`--tol`, 3 pt; v72: la tool manda, nunca una lectura "estricta" del texto, R72.4); dos vigas paralelas a ≤ 1 ft con rótulo distinto = decisión con imagen (RFI); cada rótulo tiene un solo dueño (la viga más cercana). | vigas_sobre_walls.py |
| R71.15 | Expansion anchors / slab pins: el driver es el bottom track de los elementos que el detalle de anclaje nombra (p. ej. "exterior walls"); column wraps, piers o cajas que el detalle no nombra van con su fuente o como RFI con delta, nunca mezclados en silencio. | accesorios (lectura) |
| R71.16 | Cripples de door_bulkhead / storefront / vestibule head: la regla de studs del modelo como wall se mantiene (coincide con la convención del estimador); el vendor_end compartido entre bulkhead y stub va a RFI (decide el estimador), no se cambia en silencio. | studs (sin cambio) |

---

## 18. Reglas v72 (arbitraje de dos pruebas ciegas; cada una con tool o compuerta — ninguna depende de la lectura)

| # | Regla | Dónde |
|---|---|---|
| R72.1 | Type K (panel balístico): LF del wall K = extensión del HATCH medida en vector (`hatch_extent {value_ft, source, img}`), no la esquina ni el return. Un segmento SIN tag nunca es wall K: con hatch va a `ballistic_jogs` (board) y su framing al type base; sin hatch, al type base. Contorno ballistic = Σ caras customer de walls K con hatch + `ballistic_jogs` (R70.5). | chequeos_v72 (0d) |
| R72.2 | Wall diagonal (band ori D): `faces_top` y `faces_bottom` medidas en vector; length_ft = promedio de los dos largos de cara (eje). Una sola cara o un extremo a ojo = falla. | chequeos_v72 |
| R72.3 | Pier / box partido en partes: la parte sin tag lleva `part_of` (id del registro con tag). En la cuenta de walls un box = UN wall (el del tag); la parte va a OTHER FRAMING como `pier_part`. Exterior walls = un wall por eje / fachada, sin piers. | chequeos_v72 + partition_types |
| R72.4 | `vigas_sobre_walls.py` manda: un wall que la tool da bajo viga lleva `stops_under_beam` o `beam_override {motivo, source N/HOJA, img}`; ningún adversarial cambia la altura "por lectura estricta" de R71.14. | chequeos_v72 |
| R72.5 | MEP: la lista de cruces es la salida de `mep.cruces` (`method: "mep.cruces"`, con `xy`); un cruce que la tool no ve va `manual {motivo, img}`. El mismo fire damper del opening schedule / openings_extra y del barrido (mismo tamaño WxH) se cuenta UNA vez. | chequeos_v72 + accesorios |
| R72.6 | `faces[].side` = A \| B \| END (A = norte u oeste, B = sur o este, BOX = A; END = cara de extremo / return de un box: `board_caras.py` la acepta con length_ft + length_source, fuera de Σ(side) = L). Nunca letras de brújula. | chequeos_v72 + board_caras |
| R72.7 | Stub sin tag de ≤ 6" (remate de un frente cortado por un bulkhead u otro type) no es wall propio. (v74: su LF ya NO se suma al wall más cercano: va aparte, R74.2.) Un grupo sin tag más largo sigue siendo un wall, salvo nicho (R74.3). | particion.py |
| R72.8 | Expansion anchors = bottom track de element `wall` exterior (lo que nombra el schedule de anclaje). Column wrap / chase exterior → pins (criterio del estimador) salvo `anchorage {value, source N/HOJA}`; parte sin tag de un box → ninguno + RFI con delta. | accesorios.py |
| R72.9 | Stud reinforcement MEP: plates = MAX(1, ROUNDUP(ancho / O.C.)) × filas de studs del wall (double row = 2; regla "REGISTRO ENTRE HOJAS Y CRUCE DE MEP"), con RFI de la alternativa "una por cruce". `studs_cut` solo como override con fuente. | accesorios.py |
| R72.10 | PVC trim del FRP: con más de 4 vértices, `inside_corners.jogs [{depth_in, kind notch|step, source}]`; un jog < 6" (carrier, espesor de acabado) no lleva inside corner trim (se descuenta + RFI con delta). | chequeos_v72 + accesorios |
| R72.11 | ATM: `atm_recess` en la wall que contiene el recess; lo impreso se cuenta (R78.36 / R79.2 / R80.3); la fórmula vieja (width_ft / sistered_h_ft / furring_rows / alternativas) y `extra_framing` de ATM a mano = falla. (Texto v77c "extra framing ATM = 0" RETIRADO en v80.) | chequeos_v72 (llama a accesorios.atm_recess_valido) + accesorios + canon |
| R72.12 | Track por tamaño (R71.8b): los renglones por tamaño de una familia conservan su NET y suman la familia (± 0.1); `fusionar` nunca les pone el total. `verificar` compara Σ contra `familias_out.json` de las salidas. | plantilla_excel.py |

---

## 19. v72b — reglas inviolables (compuerta de reglas; ninguna regla depende de que la corrida se acuerde)

Catálogo: todas las reglas extraídas del texto (SKILL.md + referencias/; cuenta y lista con `python3 reglas_catalogo.py`), cada una con tipo a / b / c y su chequeo o spec de evidencia. Tools: `reglas.py` (compuerta, absorbe `chequeos_v71`, `chequeos_v72`, `esquinas.py` y la compuerta de etapas), `reglas_catalogo.py`, `reglas_clasificacion.py`, `fixture_reglas.py` (proyecto sintético que pasa), `test_reglas.py` (un test por regla: caso que viola falla, caso correcto pasa), `test_ciego_tools.py` (E24 también en las tools). Tabla: `referencias/REGLAS_INVIOLABLES.md` (se regenera con `python3 reglas.py tabla`).

## 20. Reglas v73 (arbitraje de una prueba ciega: la compuerta revisa CONSISTENCIA con el plano, no solo forma)

Por qué: en una prueba ciega la compuerta v72b dio OK y dos familias salieron fuera de rango con la regla escrita
(ballistic / 3/8" y stud reinforcement MEP). La compuerta revisaba que el dato existiera (hatch medido, face customer,
`method` del cruce) y no que fuera el del plano. Desde v73 cada regla de abajo tiene chequeo (a) o evidencia (b).

| Regla | Texto | Tool / compuerta |
|---|---|---|
| R73.1 | Type K: si el plano imprime la cota del tramo, el largo ES esa cota (CONFIRMADO), no la extensión del hatch medida en vector. Todo wall K lleva `dim_scan` = salida de `cotas_banda.py` (cotas paralelas a su banda); una cota compatible (± 35 %) que no se usa = falla, salvo `dim_scan.no_aplica` con hoja. | chequeos_v73 + cotas_banda.py |
| R73.2 | Contorno ballistic sin esquinas dobles: `ballistic_jogs[]` lleva `band`; ninguna banda K (walls + jogs) se solapa con otra en los dos ejes > 1 pt, y dos walls K paralelos del mismo contorno no se solapan a lo largo del eje (un tramo no llega hasta donde empieza el otro). El jog va solo entre las caras de las dos líneas. | chequeos_v73 |
| R73.3 | Nombres de renglón = los de la PLANTILLA del estimador: `plantilla_excel.fusionar` renombra todo renglón que cita su familia (`NOMBRES_PLANTILLA`), arma el track por ELEMENTO (parapet, roof step / heads) y el resto por tamaño de stud desde `track_by_element` de canon.py, el FRT plywood por material, espesor y USO (`plywood_strips[].uso`: substrate / pier / column_wrap / canopy_soffit / nailbase) y el metal blocking por origen (edge del detalle / notas). Nunca un renglón "other framing" que mezcle elementos. | plantilla_excel + canon |
| R73.4 | Registro: un renglón resuelto que se marcó mal se corrige con `registro.py corregir <id> <estado> "<motivo>"` (entrada nueva que manda; el historial guarda la anterior). Antes de marcar un renglón de alcance se corre la misma evidencia que `alcances.py compuerta`. | registro.py |
| R73.5 | Stud reinforcement MEP = SOLO cruces de DUCTO que da `mep.cruces` (`method: "mep.cruces"`, `kind: duct`), plates = MAX(1, ROUNDUP(ancho / O.C.)) × rows. Cruce manual, pipe > 1" (el detalle de penetración le pone plate) y fire damper / ducto de otra lista NO entran: RFI con su delta. | accesorios + chequeos_v73 |
| R73.6 | `deflection_clips` declarado: {note_source, slip_track_source?} si una nota general pide clips en walls no portantes (con slip track dibujado en el type: 0 + RFI con delta = studs completos de walls a estructura), o {none_reason, source} con las hojas barridas. | accesorios + chequeos_v73 |
| R73.7 | Un segmento sin tag tipado por la nota general ("UNLESS OTHERWISE NOTED") tiene que medir el espesor del type de la nota (± 0.5"); si mide otro, es del type de la schedule con ese espesor (el wall con tag que toca) o `default_type_rfi` con las dos lecturas. | chequeos_v73 |
| R73.8 | La operación escrita cuadra: en walls / openings, `*_op` "aritmética = N" da N y N es el valor del campo (una cadena tipeada distinta de su suma = falla). | chequeos_v73 |
| R73.9 | Todo texto que una tool escribe al Excel (RFIs, operaciones, pendientes) va en inglés; `test_accesorios` / `test_v72` corren `plantilla_excel.verificar` sobre los casos que disparan RFIs. | accesorios + plantilla_excel |
| R73.10 | Cambio de type sobre una línea recta: en el nodo dibujado entre los dos tags (T / esquina), nunca en un jamb ni a mitad de una door; sin nodo, PENDIENTE con las dos lecturas (RFI con delta). | evidencia (b) |
| R73.11 | Jamb return por BORDE (head, sill, cada jamb), cada uno con su detalle: suma solo si el detalle dibuja / rotula gypsum board en el retorno; brake metal, solid sill o frame sobre FRT plywood = 0 con la cita. | evidencia (b) |
| R73.12 | Todo detalle cuya nota pide BLOCKING (2X, FRT, plywood, stud blocking) genera su `blocking_items` (o NO APLICA citado); material no impreso = CRITERIO + RFI con el delta de moverlo a la otra familia. | canon (blocking) |
| R73.13 | Corner bead en toda esquina exterior de un box (column wrap, pier, C1 box): vértices convexos expuestos × alto del board. | evidencia (b) |
| R73.14 | Alto de backboard / plywood de elevación: la cota manda desde donde arranca su línea de cota; si arranca en el piso y una nota dice "INSTALL x AFF", el alto es cota − x solo si la cota incluye ese tramo (se cita el arranque). | evidencia (b) |
| R73.15 | Sealant y trim de una misma interfaz con otro trade (head y jambs de un frame de vendor) se cargan iguales en los dos bordes, cada uno con su detalle. | evidencia (b) |
| R73.16 | Un borde de ceiling que ya es `ceiling_transition` / `soffit_side` no se vuelve a cargar como perímetro; la otra lectura va como RFI con delta. | corridas / canon |
| R73.17 | Cotas impresas de returns dentro del contorno de un wall con tag (furring, monitor, nicho) suman a ese wall (`length_op` las nombra). | evidencia (b) |
| R73.18 | (Reemplazada por R74.2 en v74.) Stub sin tag ≤ 6": no es wall propio; su type se revisa por espesor (R73.7 / R74.1). | particion.py |

Tools nuevas v73: `cotas_banda.py`, `chequeos_v73.py`, `planmark.py` (contrato de referencias/herramientas.md),
`glosario.py`, `vocab_trade.py`, `verif_respuesta.py`, `indice_set.py` genérico (arma su cache con pymupdf).
`test_ciego_tools.py` revisa también test_*.py y fixtures (rooms de tres dígitos, ids de wall de planta, cantidades de una lista
externa de examen que NO viaja en el paquete).

## 21. Reglas v74 (estudio de partición: wall por wall contra la lista del estimador, dos lecturas)

Origen: dos lecturas del mismo plano daban un número de walls por type distinto al de la lista del estimador en
varios types (y una sacaba un wall exterior de más). Se alinearon los walls de la lista con los segmentos de cada canon, uno por uno; cada
diferencia de CONTEO se explicó con una de estas reglas genéricas (ningún número, conteo ni wall de un proyecto).
Las diferencias de LF que quedan son de lectura (cota, cara, esquina) y van como RFI con delta, no como regla.
Tools: `particion.py` (modo "eje") y `partition_types.py` dan lo mismo (test_particion_v74.py); `inventario.py`
avisa R74.1 / R74.5 para que la lectura corrija el canon.

| Regla | Texto | Dónde |
|---|---|---|
| R74.1 | Type por espesor en la LÍNEA: un segmento sin tag (tipado por la nota general) cuyo espesor de band no es el de su type (± 1/2" contra la mediana de los walls con tag de ese type en la hoja) toma el type de los walls con tag de su misma línea (colineales y encadenados sin hueco vacío, de cualquier type) que tienen su espesor. Es el return / remate de un frente, no un wall del type por defecto. Con dos candidatos o ninguno: no se retipa (y R73.7 pide la lectura). | particion.py / partition_types.py / inventario.py |
| R74.2 | Stub aparte: un grupo sin tag ≤ 6" que no toca por el extremo a un wall con tag de su type no es wall de la lista ni suma LF al type (la lista mide cada wall de cara a cara sin el stub); va a `stubs` / OTHER FRAMING "stub" y su material sigue en el canon. Si toca por el extremo a un wall con tag, es su return y se suma. | particion.py / partition_types.py |
| R74.3 | Nicho / alcove: un grupo sin tag (más de un tramo) cuyos dos extremos libres caen sobre dos tramos colineales distintos de una línea de OTRO type, cerrando el hueco entre ellos, es un nicho de esa línea: no es wall de la lista; va a `anexos` / OTHER FRAMING "alcove" con su LF (material en el canon). Un grupo sin tag que no abre en otra línea sigue siendo UN wall. | particion.py / partition_types.py |
| R74.4 | Frente de bulkheads: door_bulkheads colineales cuyos huecos cubren tramos colineales de otros types (returns del frente) o son cortos (≤ el hueco de abertura del modo eje) = UN wall por frente; un hueco largo y vacío separa dos frentes. | particion.py / partition_types.py |
| R74.5 | Box duplicado: un box / pier sin tag con la misma huella (solape ≥ 50 %) que un registro con tag es el mismo elemento leído dos veces: no cuenta (el tag del plano manda). El inventario lo avisa para declarar `part_of`. | particion.py / inventario.py |
| R74.6 | Nombre exterior único: wall / pier exterior con stud conocido → `EXT-<stud>CFMF`; parapet → `EXT-PARAPET`; canopy column → `CANOPY-COL` (los mismos nombres en particion.py y partition_types.py). | particion.py |

Lo que NO se convirtió en regla (queda RFI con delta en cada take-off): esquina L entre types distintos medida libre
entre caras (sin dueño) contra R70.2 (un dueño); fin de un wall K en la caja del hatch contra el jog; door que la
lista descuenta contra R70.3 (va dentro del wall).

## 22. Reglas v75 (arbitraje de dos pruebas ciegas: clasificación del track, jamb return por borde, cambios de type)

Origen: dos pruebas ciegas limpias. El track salía bien en total pero un renglón caía en la familia equivocada por
una palabra de su nombre; el jamb return variaba entre corridas porque el sill se asumía y un storefront no se
declaraba; tres types quedaban CERCA por dónde se cortaba el type (jamb contra nodo), quién era dueño de una esquina
de alcove y desde qué cara se medía un return. Cada una es compuerta: canon.py no termina si no se cumple.

| Regla | Texto | Dónde |
|---|---|---|
| R75.1 | El nombre de un renglón de track nunca lleva "ceiling" ni "soffit" salvo el track de ceilings: el calificador y el estimador clasifican por el nombre. Todo renglón de `track_by_element` cae en SU familia (bottom / top) con familias.py; un renglón que empieza con "Bottom" / "Top" nunca es track de ceilings. | canon.py `verificar_track_nombres`; familias.py |
| R75.2 | "Bottom / Top track {size}" = track de los walls de la Partition Takeoff (con tag o sin tag: alcove, stub) + elementos que son fila de un type (column wrap, bulkhead, pier de un type). Un ELEMENTO que no es fila de la Partition Takeoff (cripples, grille head, parte de pier sin type) va al renglón "other framing" por elemento; roof step / heads a su renglón. La suma sigue siendo la familia. | canon.py `track_by_element(…, pt)` |
| R75.3 | Jamb return por BORDE con su texto impreso: abertura con return declara `jamb_return_label` (lo que rotula el detalle) y suma solo si dice gypsum / GYP / GWB; "LINE OF JAMB RETURN BEYOND" sin gypsum no basta (frame sobre FRT plywood = false con la cita). Con sill, `sill_return` true / false + `sill_return_source` es obligatorio (brake metal / solid sill / FRT plywood = false); true lleva `sill_return_label` con gypsum. Nunca se asume. | accesorios.py `_sill_return`, `_label_gyp` |
| R75.4 | Framing de storefront (`storefront_cripples`) implica su abertura: cada uno se empareja con un storefront declarado (`opening_ref` o el mismo ancho dentro de la tolerancia de cota) con su jamb return; si no, el storefront no se barrió. | accesorios.py `_storefront_de_cripples` |
| R75.5 | R73.10 hecha compuerta: dos walls de type distinto en la misma banda que se tocan cambian de type en un nodo dibujado (cara de un wall perpendicular que llega a la línea); en un jamb o a mitad de door es error salvo `type_change_rfi {alternativas, delta_lf, source}`. La door queda dentro del wall cuyo tag la comparte en la línea. | chequeos_v75.py `verificar_r75_5` |
| R75.6 | Un alcove (R74.3) nunca es dueño de la esquina con el wall de su línea: sus lados terminan en la cara de ese wall y el wall de la línea llega a la cara exterior del alcove. | chequeos_v75.py `alcove_con_esquina` |
| R75.7 | Return corto (≤ 2 ft) que sale de un tramo largo del mismo wall con tag se mide desde la cara EXTERIOR del tramo (= la cota impresa del return, de cara a cara del contorno); medirlo desde la cara interior le quita un espesor por return. Si el plano lo acota distinto: `return_basis {value: "inner_face", source}`. Un box chico (todos sus tramos ≤ 2 ft) no aplica. | chequeos_v75.py `returns_sin_esquina` |

Los cuatro pendientes del estimador (extra framing ATM, header / box beam, 3/4" FRT plywood en piers, sill track)
quedaron DECIDIDOS en v77: ver §24 (D1-D6).

## 23. Reglas v76 (arbitraje de dos pruebas ciegas: hand-off entre tareas, jogs entre caras, box con tag)

Origen: dos pruebas ciegas del mismo set con el mismo paquete dieron familias distintas sin que ninguna fórmula
cambiara. Una corrida dejó la canopy "para otra tarea" y nadie la tomó (joists, sheathing y track del soffit), otra
midió un jog del contorno ballistic de cara exterior a cara exterior, un box con tag de type salió de su type por su
`location`, un borde de ceiling se cargó dos veces y la compuerta de la entrega se contradecía con canon.py. Cada
regla es compuerta: canon.py (o la tool que se nombra) no termina si no se cumple.

| Regla | Texto | Dónde |
|---|---|---|
| R76.1 | Canopy completa. Un `fascia_box` en una facade exige un ceiling `canopy_joist` de esa facade (o `canopy_soffit_none` con reason + N/HOJA del texto que muestra que no hay soffit framed); un `canopy_joist` exige su run `canopy_soffit` (track). Un hand-off a otra tarea NO es estado final: un renglón de `otros_ceilings` que describe un soffit / canopy con framing queda consumido por un ceiling JOIST_ONLY (`consumed_by` o un N/HOJA en común) o excluido con `excluded_reason` + N/HOJA. | chequeos_v76.py `r76_1` |
| R76.2 | Column wrap sin caras de board declara `sheathing {material, source N/HOJA}` (canon.py genera Σ faces_ft × height_ft, uso column_wrap) o `sheathing_none_reason`. Un plywood_strip a mano de column wrap = error. | chequeos_v76.py `r76_2`; canon.py `_column_wrap_sheathing` |
| R76.3 | El jog del contorno ballistic sale de las bandas: dos walls K paralelos que se tocan punta con punta con un hueco entre sus caras enfrentadas (> 1 pt y ≤ 2 espesores) llevan UN jog = ese hueco, medido entre las caras; ningún jog cruza el espesor de un wall K; falta, sobra o largo distinto = error. | chequeos_v76.py `r76_3` |
| R76.4 | Toda abertura exterior declara `substrate {label (texto impreso del head / jamb), source N/HOJA, material, sill}` o `substrate_none_reason`. Con plywood en el label canon.py genera el strip: storefront = R.O. + jambs contra wall × head; ventana / door / ATM = R.O. + 2 × (head − sill) (+ R.O. si `sill`); × `constants.opening_substrate_width_ft {value, source}`. Strip a mano de head / jamb / sill de abertura = error (el de piers es otra decisión). | chequeos_v76.py `r76_4`; canon.py `_opening_substrate` |
| R76.5 | Un pier / column_wrap con tag de partition type (letras + dígito, sin EXT) es fila de ESE type aunque su `location` sea exterior; su LF = caras interiores con board y `length_ft` (sin caras = error; `type_lf_basis` no las reemplaza). Una parte `part_of` interior de ese box suma sus caras al LF del box (sigue siendo un wall). | partition_types.py `tipo`, `_lf`; chequeos_v76.py `r76_5` |
| R76.6 | R73.16 hecha compuerta: `ceilings[].perimeter_ft` de un ceiling suspendido es el perímetro COMPLETO (nunca menor que 2·√(π·área), el de un círculo); cada `ceiling_transition` declara `edge_of` [rooms de ceilings suspendidos cuyo borde es]; canon.py genera el track de perímetro = perímetro − transiciones. | chequeos_v76.py `r76_6_perimetro`, `bordes_transicion`; canon.py `generar` |
| R76.7 | Ningún texto se escribe para satisfacer un regex de compuerta. Un campo dice lo que el plano imprime o lo que se leyó; si una compuerta no deja pasar un dato verdadero, se para y se reporta (PARA REVISAR), nunca se redacta el source / label para que el regex pase. Por eso los chequeos de material leen el RÓTULO (label) y no el source: blocking 2X / WOOD sin FRT impreso = material `wood` (su renglón, en la familia de madera) o `frt_basis {source N/HOJA}` con la nota que hace FRT toda la madera. | canon.py (blocking), reglas.py `A_BLOCKING` |
| R76.8 | Entrega coherente entre tools: `plantilla_excel.py verificar` clasifica los renglones de track con familias.py (la misma regla de canon.py y del calificador: parapet, heads y other framing suman), y los tamaños que exigen renglón propio salen de las filas de partition types (un tamaño solo de OTHER FRAMING va en "other framing"). `test_ciego.py` viaja en el paquete ciego; bitácora acepta `test_ciego.py` o `test_ciego_tools.py`. | plantilla_excel.py `verificar_r71_track`; bitacora.py; armar_ciego.py |
| R76.9 | Nombres de renglón de la plantilla: el nailbase lleva el espesor IMPRESO del polyiso (`constants.nailbase_polyiso_in {value, source N/HOJA}`, obligatoria con nailbase); los joists de un framed soffit van en su renglón "3-5/8" stud, framed soffit <detalle> (LF)" dentro de su familia (`stud_by_element`). Caja parcial: `fos_chain_faces` (una cadena impresa o medida en vector por face) en lugar de `fos_chain`. | canon.py `_polyiso`, `STUD_ELEM`; plantilla_excel.py; reglas.py `A_WRAP_FOS` |

Sin cambio (decisión del arbitraje, con motivo): clips de bridging (la plantilla del estimador no los compra;
closer.py los usa como control) y bracing de parapets (cada tramo usa su altura: un tramo bajo da 0 filas).
Pendientes del estimador: decididos en v77 (§24); el borde de transición quedó confirmado (D6: sin track de
perímetro del ceiling en ese borde).

## 24. Reglas v77 (decisiones del usuario D1-D6 en Bluebeam; mandan sobre cualquier criterio anterior)

Origen: el estimador revisó en Bluebeam los cuatro pendientes de §22 y el borde de transición. Cada decisión es regla
GENÉRICA con compuerta y test sintético (test_v77.py). R77.3 es la regla del usuario y es inviolable.

| Regla | Texto | Dónde |
|---|---|---|
| R77.1 | RETIRADA (v77c / v80). No se aplica: manda R78.36 + R79.2 + R80.3 (A3). | — |
| R77.2 | (D2) Todo box beam / box header = 4 piezas × (R.O. + 1'-4"). El CONT. BOX BEAM de un office front es UN run continuo de la PRIMERA a la ÚLTIMA jamb del frente + 1'-4", × 4 (nunca por abertura): declara `front_line {sheet, ori, c_pt, jambs_pt [primera, última], scale_pt_per_ft, source}`, ro_w_ft = jambs / escala; `run_ends` = jamb_to_jamb; dos runs sobre la misma línea = error. Los demás headers llevan las piezas del HEADER SCHEDULE impreso; las piezas de cada fila = su rótulo (SINGLE 1, DOUBLE 2, "2-…" 2); largo = R.O. + 1'-4". | headers.py `_front_line`, `_piezas_rotulo`, `_reglas_v65b` |
| R77.3 | (D3, inviolable) "Léelo y haz lo que ellos te dicen": si un schedule o detalle impreso contesta, se aplica sin RFI ni pregunta. Si el dato no está impreso, se mide por geometría vectorial a la escala impresa del detalle, verificada contra una cota o un espesor impreso del mismo detalle (`scale_check`), con imagen marcada y [DERIVADO]. | chequeos_v77.py (strips); headers.py (schedule) |
| R77.4 | (D4) 3/4" FRT plywood en piers de storefront: el detalle lo rotula SOLO como strip en cada jamb del storefront; las caras del pier (nailbase: AWB on FRT plywood bonded to polyiso, y gypsum board) NO van en ese renglón. Cada strip `uso: pier` declara `width_pt` + `scale_pt_per_ft` + `scale_check {printed_in, measured_pt}` (D3), `width_ft` = width_pt / escala, `jambs` × `height_ft` (alto impreso, `height_source`) = `lf`, `plies` del rótulo y `layers_drawn`; más capas dibujadas que el rótulo singular = plies del rótulo + `rfi` con delta. Todo pier declara `jamb_strips [refs]` o `jamb_strips_none_reason` con hoja. | chequeos_v77.py `r77_4` (lo llama canon.py) |
| R77.5 | (D5) Sill track: "ADD FULL LENGTH ADDL HEAD TRACK @ OPNG > 4'-0"" + "INVERT DETAIL FOR SILL CONDITION" → R.O. > 4'-0" = (R.O. + 1'-4") × 2; ≤ 4'-0" × 1; solo aberturas con sill (una door con `with_sill` = error). Una abertura cuyo detalle acota el R.O. desde una línea de sill (cota de sill impresa) lleva `with_sill: true`. | headers.py |
| R77.6 | (D6) En un borde de transición el ceiling NO lleva track de perímetro propio (el detalle de la transición lo remata con shadow molding): canon.py resta del perímetro los bordes `edge_of` (R73.16 / R76.6 confirmadas). | chequeos_v76.py `bordes_transicion`; canon.py `generar` |
| R77.7 | Un ceiling suspendido exige `constants.carrying_direction {value N-S \| E-W, source}` (UNA dirección para el proyecto, impresa o RFI con el delta de la otra) y cada room `ns_ft` / `ew_ft`; sin ella cada corrida tomaba el lado largo por room. | canon.py `_ceil_dims` |
| R77.8 | R76.7 sin falsos bloqueos: A_BLOCKING reconoce el rótulo con puntos (F\.?R\.?T\.?); el detector de español del Excel quita rutas, nombres de archivo, ids y coordenadas antes de buscar; vigas_sobre_walls solo cruza bands de la hoja de planta pedida (band.sheet); bitácora escribe con lock y resuelve symlinks (realpath); inventario_tags.py y alcances.py leen siempre la copia limpia del bid set (copia_limpia.py, sin /Annots). | reglas.py; plantilla_excel.py; vigas_sobre_walls.py; bitacora.py; copia_limpia.py |
| R77.9 | Millwork empotrado en una partición (la elevación / sección del cabinet dibuja la partición arriba: "SCHED. PARTITION") = abertura enmarcada: header del schedule por su R.O. impreso; el tramo de partición acotado frente al cabinet es de su type (un tramo acotado sin dueño = falta de inventario). | lectura (inventario + headers.py) |
| R77.10 | (decisión del usuario, v77b) El largo de un wall corre A TRAVÉS de sus doors hasta la esquina o la intersección donde termina: el R.O. de la door queda DENTRO del largo del wall (confirma R70.3 / E10); nunca se corta el wall en la jamb dejando el tramo de la door sin dueño, aunque la door esté pegada a la esquina. Con `band {p0, p1}` y `openings[].xy_pt` (centro del R.O. en planta) un R.O. fuera del largo del wall (± 6") = falla. | chequeos_v77.py `r77_10` (lo llama canon.py); particion.py (R70.3) |


## 25. Reglas v77c (decisiones del usuario U1–U11 en Bluebeam; mandan sobre §24 y todo lo anterior)

Origen: el estimador revisó en Bluebeam las pruebas y la referencia. Cada decisión es regla GENÉRICA con compuerta y
test sintético (test_v77.py U1, test_v77c.py). Los valores del proyecto viven solo en la referencia y en los rangos
del árbitro; aquí no hay ningún número de un proyecto.

| Regla | Texto | Dónde |
|---|---|---|
| R77.11 | RETIRADA en v80. No se aplica ("extra framing ATM = 0", sistered / furring en 0 o a RFI): manda R78.36 + R79.2 + R80.3 — todo lo IMPRESO en el recess se cuenta con la regla de la tool. | accesorios.py `atm_recess_valido` (rechaza SISTERED / FURRING en `drawn_not_counted`) |
| R77.12 | (U8) ACOUSTICAL SEALANT EXCLUIDO EN TODOS LOS PROYECTOS: sin renglón, sin cálculo, sin RFI de cantidad; va en Clarifications / Scope Checklist como exclusión ("EXCLUDED in all projects, estimator standing order"). El "sealant at base of gypsum" exterior NO es acoustical: sigue, en su renglón y su familia propia. Compuertas: canon.py no calcula `details[*].sealant` ni `sealant_items` (aviso con lo que se dejó fuera) y pone la exclusión en `excluidas`; alcances.py ALC-19 se cierra "EXCLUIDO: ..." y un Excel con renglón de acoustical sealant = falla; plantilla_excel `validar` / `verificar` rechazan el renglón; el calificador usa el modo "excluir". Anula 54.4, 55.5 y 53.9 punto 2. | canon.py `_sealant`; alcances.py `EXCLUIDOS`; plantilla_excel.py `acoustical_err`, `verificar_v77c`; familias.py; eval_takeoff.py |
| R77.13 | (U9) Preguntas al estimador: primero se anuncia el total ("tengo N preguntas en total, te las haré una a la vez") y se hace UNA pregunta por turno, corta. En una corrida automática las preguntas van a PARA REVISAR numeradas n/N con el total anunciado en la primera fila. Compuerta: `revisar_err` (n = 1..N, total en cada item) y `verificar_v77c` (primera fila "N questions in total", columna # = n/N). | plantilla_excel.py `ordenar_revisar`, `revisar_err`, `verificar_v77c` |
| R77.14 | (U10) Procedimiento OBLIGATORIO de revisión con el estimador (orden de las preguntas y de PARA REVISAR): 1) FLOOR PLAN, las partitions en orden ALFABÉTICO de type (orden natural: A2 antes que A10); 2) al terminar el floor plan, los DETALLES que marca el floor plan, en el orden en que el floor plan los marca. Cada item declara `fase` ("floor_plan" con `type`, o "detalle" con `orden_plano` y N/HOJA). Compuerta: item sin fase / type / orden_plano = error; fuera de orden = error (`ordenar_revisar` lo ordena y numera). | plantilla_excel.py |
| R77.15 | (U11) Mensajes al usuario cortos, sin tablas largas: un paso, una pregunta, lo esencial; el detalle va en los archivos. | lectura (proceso) |
| R77.16 | (U7) Studs de una wall = posiciones @ O.C. + 1 + los extras de nodo: +1 en cada esquina L y +1 al branch en cada intersección T (R60.1, studs_nodos); nunca a ojo ni por promedio. | studs_nodos.py (test_v77c U7) |

Sin regla nueva (con motivo): U2 ya es R77.10 (el largo de un wall corre a través de sus doors hasta la esquina /
intersección). U3–U6 son medidas del proyecto (largos de walls y returns sin tag): se leen con R77.10 + R77.3 (lo
impreso manda; lo no impreso, por vector verificado) y viven solo en la referencia del árbitro.

# REFERENCIA DE MÉTODO (v38–v68) — subordinada al PROTOCOLO v69

## CÓMO ESTÁ ORGANIZADO ESTE SKILL — LECTURA OBLIGATORIA (v51; v69: el PROTOCOLO v69 va primero)

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

Columnas base, en este orden: `Partition / Scope` · `Length (LF)` · `Height (FT)` · `Layers` · `6" Metal Stud (LF)` · `3-5/8" Metal Stud (LF)` · `5/8" Gyp Board (SF)` · `FRP-n (SF)` · `Durock (SF)` · `Demolition (SF)` · `Labor (Hrs)`.

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
- **Toda cantidad lleva su desglose rastreable** (pieza por pieza, face por face, o la operación completa). Un número escrito a mano sin desglose — como un total de blocking escrito sin lista de accesorios — no se entrega: en un proyecto anterior ese número, recontado pieza por pieza, salió muy distinto.

## ORDEN FIJO DE PRESENTACIÓN

Los walls se presentan agrupados **por tipo**, y dentro de cada tipo **de mayor a menor longitud**, con la columna del take-off manual del usuario al lado cuando exista. Ese es el orden con el que él revisa. Si un wall cambia de longitud al corregirlo, se reordena dentro del mismo criterio, pero **el criterio nunca cambia entre entregas**.

## NUMERACIÓN DE WALLS — UNA SOLA, FIJADA EN EL BARRIDO

El número de wall se asigna **una sola vez**, al cerrar la Etapa 3 (canon conciliado), agrupando por tag (orden alfabético del tag) y dentro de cada tag por posición. Ese número es el identificador permanente del wall en todo el proyecto: mapa, tablas, imágenes de evidencia, resumen de materiales y clarifications. Ventaja de agrupar por tag: el rango del número ya dice el tipo sin mirar nada más.

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

Si da más que cero, ahí hay material que alguien tiene que construir. Y hay que hacerla **por face**, porque el ceiling cambia de cuarto a cuarto: en un caso real la misma abertura dejaba una banda distinta por la face de la oficina y por la face del lobby (ceilings a alturas distintas), y el board seguía hasta el deck por las dos.

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
8. **Líneas a trazos (walls "above") se miden por la LÍNEA, no por un trazo.** Un par dashed se mide del primer al último trazo de toda la run; el final de un trazo no es el final del wall. Y un QUIEBRE en el patrón del dash (trazo corto + hueco distinto al período) marca un cambio de tag: allí empieza otro wall (en un proyecto anterior un solo tramo eran en realidad dos walls de tags distintos).
9. **El length de un wall exterior sale de las faces INTERIORES vectoriales**, no de la dimension de grids menos un thickness supuesto: el grid no siempre está en la face exterior (en un proyecto anterior el grid caía dentro del wall).

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

**El mismo cuidado con las plantas ampliadas: una puede venir girada 180° o espejada respecto del floor plan.** Antes de asignarle nada, verifícala con TRES rasgos independientes del propio dibujo (de qué lado están las doors, dónde caen los muebles fijos, dónde los aparatos), nunca con el rótulo. Caso real: la planta ampliada de baños venía girada 180°, y sin detectarlo los accesorios se habrían asignado a la face opuesta del wall. Otro caso real: un par de elevaciones exteriores venía espejado E-O respecto de la planta.

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

**Y un material puede no estar en ninguna especificación: búscalo por lo que ES, no por su nombre comercial.** Caso real: la palabra "KEVLAR" aparecía UNA sola vez en todo el set (el legend del floor plan) y no había sección de especificación; el producto real estaba escrito dentro de un detalle como `3/8" UL752 LISTED LEVEL-2 FIBERGLASS (BULLET RESISTANT, NIJ TYPE II)`. Método: volcar el set entero con `pdftotext` a un .txt y buscar por sinónimos del material (para ése: BULLET, BALLISTIC, UL752, NIJ, LEVEL-2, ARMOR, FIBERGLASS, SECURITY) antes de declarar que el set no lo especifica.

Valida cruzado: misma longitud en 2 fuentes independientes = [CONFIRMADO] alto. Los segmentos deben sumar el total declarado, salvo que los ticks sean dobles (ver arriba).

## HEIGHT DE BOARD — POR FACE, NO POR WALL

El board para donde su detalle diga, **medido contra el ceiling del cuarto QUE ESA FACE MIRA**. Como el ceiling cambia de cuarto a cuarto, un mismo wall suele ser **asimétrico**: una face a una height y la otra a otra. Llévalo en columnas separadas (Side 1 / Side 2), cada una con su height, sus layers y una nota que diga en qué para y por qué.

**Cuarto open to structure = el gypsum board de esa face va hasta el DECK.** Si el cuarto no tiene scheduled ceiling, la face no puede parar en "ceiling + 6\"": se vería el framing desde adentro. No es RFI, es la regla.

Para saber qué ceiling tiene cada cuarto hay que leer el RCP **cuarto por cuarto**, no de memoria ni por la nota general:
- La nota general ("all ceiling heights shall be 8'-6\" unless noted otherwise") solo rige donde no hay tag.
- Un cuarto **sin tag de ceiling** no es "el default": revisa sus key notes. "OPEN TO STRUCTURE ABOVE" es un key note, y se confirma además porque dentro del cuarto **no hay grid de ceiling dibujado**.
- Sigue el leader de cada tag de ceiling: un tag `GB` junto a un cuarto puede pertenecer al **soffit**, no al cuarto, y el cuarto tener otro ceiling distinto. Y el tag de un cuarto puede estar FUERA del edificio con leader (en un proyecto anterior el office traía su tag debajo de la planta).

## HEIGHT DE DECK — ZONAS Y PENDIENTE

El B.O.D. casi nunca es uno solo para todo el edificio. En el Roof Framing Plan:
- Busca la **línea de cambio de elevación**: se reconoce porque la viga aparece rotulada dos veces, `(HI)` de un lado y `(LOW)` del otro. Esa línea, y no el achurado, es la frontera de zonas.
- Una zona puede decir `NO SLOPE` con un solo B.O.D., o traer **dos elevaciones puntuales** con una flecha `SLOPE` entre ellas.
- **Cuenta TODOS los marcadores de B.O.D. de la hoja antes de decidir cuántas zonas hay**, y solo declara "plana" la zona donde el plano diga `NO SLOPE`.
- Comprueba la pendiente: (diferencia de elevación ÷ distancia) debería dar una pendiente de techo estándar (p.ej. 1/4" por pie). Si no da, leíste mal una de las dos.
- **Para cotizar, usa el extremo ALTO de la zona en pendiente**, no un valor interpolado por wall: los studs se cortan a la condición más alta de la zona y una height que se desliza no es construible. Declara el criterio y el delta de usar el extremo bajo (o la height real de cada wall).
- **Excepción declarada:** la face interior de un wall EXTERIOR que corre a lo largo de un eje (alero alto o bajo) va a la height real de ese eje, porque ahí la height no se desliza.
- **Relee esta sección ANTES de programar el script de alturas.** En un proyecto anterior se interpoló wall por wall y hubo que rehacer el cálculo.
- **Arma el B.O. deck layer por layer desde los detalles estructurales**, no de memoria: bearing + asiento del joist + nailer (si lo hay) + sub-purlin. Ej.: un detalle de tipo 1/S3.21 traía un 2x6 plano como nailer sobre el joist, y el deck quedaba más alto que bearing + asiento.
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
- Caso real: en un solo edificio la verificación cambió el deck, los lengths E/O, dos aberturas exteriores, el ceiling de sales, el blocking de baños, y encontró walls que faltaban y line items de alcance nuevas.

## LOS MARKUPS AJENOS NO SON FUENTE

Un bid set puede traer **anotaciones de Bluebeam de otro estimador dibujadas encima del plano** — se ven como líneas de colores pegadas a los walls y es facilísimo leerlas como si fueran elementos constructivos. En un proyecto anterior el floor plan traía decenas de anotaciones de otro estimador.

**PRIMER PASO DE TODO PROYECTO: generar una copia del set SIN `/Annots` con pikepdf y renderizar SIEMPRE desde esa copia.** `pdftoppm` RENDERIZA las anotaciones, así que un recorte "crudo" del original no es crudo. Filtrar `page.annots` después de mirar la imagen llega tarde: para entonces ya se interpretó.

La geometría de `pdfplumber` (`page.lines`) SÍ está limpia también en el original — las anotaciones no entran en el content stream —, así que el riesgo es exclusivamente de lectura VISUAL.

Y no se usan como fuente de medida **ni siquiera de cruce**. Orden del usuario: está entrenando el método para dejar de depender de Bluebeam. Caso real de por qué importa: un markup ajeno de casi el doble del largo real del wall hizo perseguir durante varios pasos una diferencia que no existía — su trazo abarcaba el wall más la door más el arranque del tramo siguiente.

## LAS TRES AUTOVERIFICACIONES DE UNA MEDIDA

Una medida es autosuficiente cuando se verifica sola, sin take-off ajeno:

1. **El thickness medido entre las dos faces coincide con el WALL THICKNESS del schedule.** Prueba que el tag pertenece a ese wall. Si el error pasa de ~0.15", el par de faces está mal elegido — casi siempre porque dos walls adyacentes comparten una face.
2. **El resultado cae en una dimensión de diseño.** 11'-0" clavado es señal de que los dos extremos se identificaron bien; 11'-4.9" es señal de que algo se arrastró.
3. **Si hay dimension impresa, coincide.**

## GRANULARIDAD Y MARCADO

- La unidad de trabajo es el **TIPO de wall completo**, con todas sus instancias juntas — si un tipo tiene N walls, se hacen los N. Nunca todos los tipos de golpe, nunca un wall suelto. Ceilings: por CUARTO. Soffits: uno por uno.
- El marcado va **siempre sobre la hoja completa** (el usuario necesita ver el plano entero para detectar lo que se escapó), con **un solo tipo marcado a la vez**, rotulado con el número oficial de wall. Marcas grandes, legibles a escala de hoja, con leyenda. Los recortes de detalle van ADEMÁS, nunca en vez de.
- **ESTILO DE MARCADO APROBADO POR EL USUARIO (26-sep-2026), se usa igual en cada proyecto:** hoja COMPLETA a 300 dpi desde la copia sin markups · **un solo tipo por imagen** · **rectángulo sobre la extensión real** de cada wall · etiqueta en caja de color con el **número oficial + el LF**, unida al wall por una línea guía corta · **azul para los walls con tag y rojo para los que no lo tienen** · auto-test de tinta en las 7 sondas antes de escribir el archivo. Palabras suyas: "la manera como estás marcando las walls está perfecta y me gusta, así tienes que hacerlo en cada proyecto".
- **Un wall es un TRAMO, no un punto: márcalo con un rectángulo sobre su extensión real**, no con un círculo — un círculo no dice dónde empieza ni dónde acaba el wall, que es justo lo que el usuario necesita revisar. Las aberturas se marcan dentro, en otro color. Si el wall tiene una door, la marca se parte en piezas sólidas a cada lado del opening (el auto-test de tinta aborta si el punto de prueba cae en el opening); la cantidad sigue siendo la del wall completo.
- **El paquete de imágenes de cada tipo, antes de cuantificar y sin que lo pida:** (1) hoja completa marcada con TODAS las ubicaciones y sus números oficiales; (2) recortes de zona con las mismas marcas, uno por agrupación geográfica; (3) recorte cerrado y LIMPIO (sin marcar, alta resolución) de CADA ubicación; (4) el DETALLE del tipo en Partition Types, leído completo y medido por geometría; (5) todo renderizado desde la copia sin `/Annots`, y cada imagen reabierta antes de entregarla. Después del paquete: lista numerada + PAUSA.
- **LA TABLA DE BANDAS DEL DIBUJO SALE DE LOS CIERRES SELLADOS, NUNCA DE LA MEMORIA.** Las coordenadas de cada wall marcado se leen del JSON sellado de ese wall (el campo con la derivación del length, que lleva las faces y el run). Re-teclearlas a mano metió **varios errores de dibujo en un solo proyecto**, con las cantidades intactas. El peor: un wall al que se le puso la banda de OTRO wall porque los dos medían casi lo mismo (diferencia de centésimas de pie) — la trampa de "que el total coincida numéricamente no prueba que sea ese wall". **Nunca asignes una banda por coincidencia de LF**: siempre por tag+leader o por la geometría que el cierre dejó escrita.
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

Decir "este detalle aplica a este wall" sin la cadena es plausibilidad, no evidencia. La cadena mínima tiene dos eslabones citados con hoja: **origen → referencia → destino**. Ejemplo correcto (genérico): `<planta> door [door n] en el wall` → `<hoja del Door Schedule> fila [door n]: HEAD N/HOJA, JAMB N/HOJA, SILL –` → `N/HOJA del head`. Sin cadena, la afirmación no se escribe. `closer.py` lo bloquea.

## EL DATO CENTRAL SON LAS LAYERS POR CADA FACE

Orden del usuario: lo más importante del take-off es **qué board, cuántas layers y hasta qué height, face por face**. El thickness del wall no es un dato entregable — es control interno para verificar que el tag está bien asignado.

## SETS CON WALLS DE Wood

Algunos prototipos (p.ej. 7-Eleven 9350 CST-WOOD) enmarcan las partitions con studs de Wood 2x4/2x6 y los exteriores con 2x8. Ahí el alcance metal se reduce a lo que el plano sí pide en steel: slip track de deflection en el tope de las partitions, los soportes CFS de soffits y walls colgados, y cualquier elemento que un detalle dibuje en CFS (p.ej. el shelf del water heater en 6" 18 GA). Los studs, plates, blocking de deflection y pines X-U del bottom plate de wood se reportan en columnas INFO (Div 06), nunca mezclados en una columna de metal, con un RFI de alcance que pregunte si el drywaller también enmarca wood y el delta en LF. `closer.py` se usa igual: la wood va como STUD con su operación y los plates como TRACK_BOTTOM declarando que son Div 06.

## REGLAS INVIOLABLES (errores reales ya cometidos)

- Cadenas paralelas: nunca sumar 2 cadenas que miden el mismo tramo. Contar dimension lines y ubicar ticks antes de sumar.
- Track: LF total ÷ length del wall = runs, debe dar 2. Si da 3, duplicaste el top track.
- Track: bottom y top/deflection SIEMPRE en renglones o columnas separados, **en TODAS las tablas donde aparezca track**, no solo en el resumen de compra. Nunca combinados en una fila aunque el LF total sea correcto.
- **Condición del top track, declarada por tipo.** Cada tipo de partition lleva su propia columna diciendo qué va arriba, con el detalle citado: slip/deflection track, track fijo ("secure to structure") o cap track de wall parcial. Nunca dejes implícito qué corona un wall que llega al deck. Y comprueba DOS cosas por separado: (a) ¿el detalle pide slip track? (b) ¿algún schedule le da designación de perfil y calibre? Si (a) sí y (b) no, es RFI con el delta de precio declarado — un slip track de ala 2" cuesta bastante más que un track normal de ala 1-1/4".
- **Designación SSMA: el calibre está DENTRO del nombre del perfil — decodifícalo antes de decir que falta.** `362S137-33`: `362` = alma en centésimas (3-5/8") · `S` = stud con lip (`T` track, `U` channel, `F` furring) · `137` = ala (1-3/8") · `-33` = **steel en mils**. 33 = 20 ga · 43 = 18 ga · 54 = 16 ga · 68 = 14 ga · 97 = 12 ga. Nunca abras un RFI de calibre sobre un perfil que ya lo trae en el nombre; y si el schedule solo tiene filas de 3-5/8" y 6", lo que falta es la fila, no el calibre. <!-- [ciego-ok] designación de stud genérica -->
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
- **Aberturas de walls exteriores: salen de los STOREFRONT FRAMES, no del door schedule.** Cada frame trae su R.O. y su sill; una door dentro de un frame no es la abertura, el frame lo es. Un frame con sill alto deja un **knee wall** abajo que se SUMA de vuelta — con su board Y su metal, como cualquier sill (ver la SUPER REGLA). Caso real: se descontó solo el área de la puerta cuando el frame completo era varias veces mayor, y bajo otro frame había un knee wall sin contar. El board que "wraps at jambs" alrededor del storefront es line item propia (returns + corner bead).
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
- **Una "banda" de wall NO es un par de coordenadas válido para toda la hoja.** Una misma alineación puede llevar tramos de TIPOS DISTINTOS y espesores distintos: en un caso real una sola alineación llevaba dos types de espesor distinto y un officefront de marco delgado — unirlo todo inventó walls que no existen. La banda se re-deriva POR TAG, y solo cuenta el tramo donde EXISTEN LAS DOS FACES con lineweight de wall **y** la separación es igual al WALL THICKNESS del schedule de ESE tipo (±0.35"). Control barato: si las dos faces tienen coberturas muy distintas a lo largo del tramo, la banda está mezclando tipos.
- **Un wall run puede llevar VARIOS TAGS en serie.** Al run completo hay que restarle las porciones que gobiernan los otros tags, usando sus dimensions impresas cuando existan. Nunca asignes el run completo a un solo tag. Si no se distingue dónde termina uno y empieza el otro, decláralo y pregunta.
- **Declara si el LF es face-a-face o centro-a-centro.** Una polilínea de Bluebeam se dibuja hasta el EJE del wall perpendicular; la banda dibujada se mide face to face. Para framing el centro-a-centro es el correcto — el track corre por debajo del wall que cruza — así que suma medio thickness del wall perpendicular en cada extremo que muera contra otro wall. La diferencia es sistemática: medio thickness del wall perpendicular por cada extremo.
- **El registro entre dos hojas se vota con el FONDO ARQUITECTÓNICO, nunca con las burbujas de eje.** El círculo de la burbuja no siempre cae igual respecto de la línea de eje: en un set real las hojas de plomería tenían unos pocos pt de corrimiento (varias pulgadas a escala de planta), suficiente para inventar un cruce de MEP donde solo estaba la línea del wall exterior. Se votan los SEGMENTOS LENGTHS DE WALL (lw ≥ 1.0, ≥ 50 pt) exigiendo ≥ 25 coincidentes en cada dirección. Si una hoja no llega a ese mínimo (las de piping y los RCP a menudo no), esa hoja NO se usa para cruce geométrico y se revisa a ojo, declarándolo.
- **Un cruce de MEP real SOBRESALE por fuera de las dos faces.** Una línea que TERMINA en la face del wall es fondo arquitectónico, no una penetración: se exige ≥ 3 pt de sobresalir por cada lado y se filtra por lineweight (un hatch de 0.24 no es un ducto). Los ductos vienen en PAREJAS de líneas paralelas y la separación entre la pareja ES el width del ducto. **Ojo con el ducto dibujado partido:** si el CAD corta el ducto en la face y mete un conector flexible, el filtro de "un solo segmento que sobresale" no lo ve — hay que detectar también el corredor, o sea la línea que llega al wall por los DOS lados.
- **Blocking de millwork, por tipo de mueble:** base cabinet o counter contra wall = **1 run horizontal** al rail superior, LF = length del run. Wall/upper cabinet = **2 runs** (rail alto y rail bajo). Standards de shelf ajustable = **vertical por standard**, LF = height × nº de standards. Counter que muere de canto contra el wall = **1 cleat vertical** de la height del counter. Wall stop de door = **2'-0" por tope** cuando el plano no lo ubica (length que garantiza agarre en dos studs a 16" O.C.).
- **El Hardware Group de cada door decide si hay blocking de wall stop.** La nota `PROVIDE BLOCKING AT EACH WALL STOP` no aplica a todas las doors: hay que abrir el Hardware Schedule grupo por grupo y ver cuál lista `1 EA WALL STOP`, cuál lista `FLOOR STOP` y cuál no lleva tope. Verificación cruzada gratis: la door leaf dibujada abierta, medida en planta, debe morir contra un wall en los grupos que sí llevan wall stop.
- **Si el usuario señala algo sobre un entregable que TÚ generaste, reabre ESE archivo** — no el JSON de trabajo, no la memoria del turno anterior — y recorta la zona exacta que él señala. El archivo entregado es la fuente de verdad de lo que él está viendo. Nunca le sugieras que leyó mal antes de haber abierto su hoja y mirado el pixel.
- **La numeración de walls no se vuelve a derivar nunca** (ver arriba). Un segundo sistema de numeración destruye la trazabilidad de todo lo ya revisado.
- **Soffits siempre separados de ceilings y de walls**, y ninguno se cuantifica sin su detalle abierto y citado.
- Cuarto con varias alturas de cielo bajo un mismo room tag: no siempre hace falta mapear el límite exacto en planta — confirma con el usuario si basta SF total + alturas de drop + Div 05 por zona.
- **Una dimension con `EQ` a los lados es un TRAMO ACOTADO, no el length del wall.** Caso real: el wall vertical de una oficina tenía su dimension impresa (coincidiendo con la geometría) y la dimension con EQ arriba y abajo era el **office front**, con un tramo de wall sólido a cada lado. Como el officefront es Div 08, cuantificar el wall completo es cotizar board donde va vidrio. En todo wall con officefront o storefront, separa el tramo ajeno del wall sólido antes de cuantificar board — **y después aplica la SUPER REGLA al tramo ajeno, porque encima de él casi siempre hay bulkhead nuestro**.
- **El B.O.D. varía por zona y el tag de ceiling no define la height.** En un mismo proyecto un mismo tag de ACT estaba a una altura en un cuarto y a otra en otro: se lee la dimension impresa de cada cuarto, una por una.
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
- **Un md5 distinto entre dos copias limpias NO significa contenido distinto**: pikepdf y las librerías de PDF no escriben bytes deterministas. Antes de dar la alarma se compara el CONTENIDO — hash de `page.lines` y de `page.rects` de la hoja de trabajo, y conteo de `annots`. En un caso real las tres copias dieron el MISMO hash de líneas y rects, y solo el original traía anotaciones; eso además vuelve a probar que la geometría vectorial del original está limpia y que el riesgo de los markups es exclusivamente VISUAL.
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
15. **Medir el tramo entre cruces en vez del wall** (muy corto contra un manual) → END CAP a ambos lados, no tolerancia ciega.
16. Face-a-face vs centro-a-centro → diferencia sistemática de medio thickness por extremo; declarar siempre cuál se usa.
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
27. **Registrar dos hojas por las burbujas de eje** → votar el fondo arquitectónico; las burbujas pueden mentir varios pt.
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
38. **arranque.py con pdfplumber sobre un set grande** (un set grande en MB y hojas: >20 min sin terminar) → para el mapa de hojas usar `pdftotext -f N -l N -bbox` por página; pdfplumber solo en las hojas de planta.
39. **Marca de planmark sobre un wall con door** → el punto de prueba cae en el opening y el gate aborta (correcto); se marca en piezas a cada lado.
40. **Set con walls de Wood** → el alcance metal se reduce a slip track + soportes CFS de soffits; la wood va INFO Div 06 con RFI.
41. **Tags en rombo/hexágono** → `tagband` no los ve como caja; censo por layer de texto dentro de la hoja de planta + verificación visual.
42. **Soffit escondido en el RCP** → barrer TODAS las llamadas de detalle del RCP y abrir cada una; leer la keynote de cada soffit.
43. **Walls "above" sin cuantificar el soporte** → un wall colgado necesita su soporte CFS: hangers a cada cuerda de joist que cruza + struts.
44. **Interpolar la height wall por wall en un techo en pendiente** → la regla ya existía (extremo ALTO de la zona) y se programó el cálculo sin releerla.
45. **B.O. deck sin el nailer** → armarlo layer por layer desde el detalle sub-joist-to-joist; un 2x6 plano olvidado son +1.5" en todo lo que va al deck.
46. **Aberturas exteriores desde el door schedule** → salen de los storefront frames (R.O. + sill); se dejó de descontar casi todo un frame y se omitió un knee wall.
47. **Length exterior = dimension de grid − thickness supuesto** → medir las faces interiores vectoriales.
48. **Wall a trazos medido hasta el final de un trazo, y quiebre del patrón ignorado** → medir la línea completa; el quiebre del dash marca cambio de tag.
49. **Profundidad de soffit tomada de una dimension del RCP que era de la fila de ACT** → emparejar cada dimension con sus ticks; el detalle del soffit manda.
50. **Cantidad sin desglose** (blocking de baños escrito a mano) → toda cantidad con su lista pieza por pieza; recontado salió muy distinto.
51. **Soffit sin todas sus faces y backer doble contado** → cada soffit: fondo + face vertical + retorno + tapas; un backer que el detalle pone en la face del wall ya está en ese wall.
52. **Walls pequeños o sin tag que se escapan** (medias walls y furring sin tag) → el barrido por grafía (#30) incluye rectángulos cerrados sin hatch y furring pegado a walls exteriores.
53. **Alcance fuera de las partitions que no se barrió** (shelf de water heater en CFS, returns de storefront, light wells, access panels, cut-outs de chases) → el crítico de completitud barre TODAS las hojas antes de entregar.
54. **Contar solo el wall sólido de una alineación con office front y dejar fuera el BULKHEAD de encima** (el error que motivó la SUPER REGLA) → el office front moría bajo el ceiling: una banda de wall continuo sobre cada abertura, en todas las oficinas, sin contar. Los detalles "OFFICE BULKHEAD @ DOOR" y "@ GLASS PANEL" lo traían entero: `2 LAYERS 5/8" GYPSUM WALL BOARD TO EXTEND TO UNDERSIDE OF DECK`, doble row de stud con isolator, `CONT. SLIP TRACK`, `CONT. BOX BEAM`, `3/4" FRT PLYWOOD BLOCKING`, `CORNER BEAD` y `SHADOW MOLDING`. Era mucho board más su metal. **Y el error tiene su mitad simétrica abajo:** el sill bajo una window o un pass-through es otra banda con su propio board y su propio metal (cripple studs + sill track), y lo único que se deduce del wall es la ABERTURA NETA entre header y sill, no el rectángulo de piso a ceiling.
55. **Fijar la banda con la pareja de faces equivocada** → el detector acepta lw ≥ 0.5 para no perder tramos y puede devolver las líneas INTERIORES del wall: mismo thickness y mismo LF, pero ~1 pt desplazada.
56. **El cache de render anula la regla de los markups en silencio** → la clave del cache lleva la identidad del archivo fuente (`sha256(path+mtime+tamaño)`), no solo página y dpi.
57. **Dar la alarma por un md5 distinto entre dos copias limpias** → comparar CONTENIDO (hash de `page.lines` y `page.rects`, conteo de `annots`), no bytes: las librerías de PDF no escriben salida determinista.
58. **Pedirle a un agente que "verifique"** → se le pide REFUTAR, con contexto completo por escrito, y su salida es evidencia citada que el hilo principal recomprueba, nunca una cantidad.

59. **Re-teclear a mano las coordenadas del dibujo en vez de leerlas del cierre sellado** → 6 bandas mal en un proyecto con las cantidades intactas; la tabla de marcado se deriva de los JSON sellados y se chequea con `verif_bandas.py`.
60. **Asignar una banda por coincidencia de LF** → un wall quedó dibujado encima de otro que medía casi lo mismo (diferencia de centésimas de pie). La banda se asigna por tag+leader o por la geometría escrita en el cierre, nunca por el número.
61. **Marcar una column enclosure como si fuera un tramo de wall** → se marca como CAJA, con el LF = perímetro furrado, y el sondeo de tinta sobre el perímetro (el centro está hueco).
62. **Marcar un bulkhead con las faces de los walls vecinos** → sus extremos son las tapas de jamb; usar las faces mete de más el width de la jamb del officefront ([valor retirado E24] en vez de [valor retirado E24]).
63. **Descartar una banda buena porque una face no llega al lineweight de wall** → hay faces dibujadas como triple línea fina; reintentar a lw ≥ 0.55 y confirmar con imagen.
64. **Corregir una cantidad y no corregir el dibujo** → un wall siguió dibujado con el valor viejo un mes después de la reauditoría. Toda corrección toca las cuatro cosas el mismo turno: cierre, documento, tabla de bandas y resumen global.
65. **Dejar el entregable solo en el chat** → todo entregable se escribe también en la carpeta del proyecto en la PC del usuario, en cuanto queda verificado (ver ARCHIVO).

## BARRIDO COMPLETO POR TAG + PAUSA OBLIGATORIA

**v69:** el censo de tags (cada repetición, tags no contemplados, caja real / rombo / hexágono, candidatos sin
leader, falsos positivos de grid bubbles) lo hace `inventario_tags.py` en la Etapa 1, con lista numerada, recorte
circulado verificado y ambiguos NO contados con su motivo. A mano, solo en hojas NO INVENTARIABLES, con el mismo
criterio: un tag es una palabra dentro de su símbolo real, todo candidato dudoso se abre en imagen, y **cada tag
del censo tiene que terminar en un wall cuantificado** (Etapa 3 lo alerta si no).

**Y el tipo POR DEFECTO del set no se cuantifica por tags.** Si el floor plan trae una nota tipo `ALL PARTITIONS TO BE TYPE 'X', UNLESS OTHERWISE NOTED`, todo wall sin tag es de ese tipo y hay que encontrarlo por barrido geométrico. El método que funciona: resolver la banda de CADA tag conocido → marcarlas TODAS en una hoja completa → mirar buscando wall SIN marca → medir solo esas zonas. Es marcar la hoja al revés: para ver el hueco, no el wall. Antes de cargarlo al tipo por defecto, **léele el perfil de lineweight**: 4+ líneas finas (lw 0.48–0.60) dentro de 2"–3" es storefront (Div 08), y una sola línea gruesa continua es vidrio — busca texto `R.O.` o `CLEAR FINISHED OPENING` al lado antes de darlo por wall.

Al terminar el barrido (Etapa 1), NUNCA pases directo a cuantificar. Muestra la lista numerada Y una imagen circulada de CADA ubicación (`inventario.md`), y DETENTE a esperar confirmación explícita del usuario de que la lista está completa. El conocimiento que el usuario tiene del plano es el filtro final.

**Modo desatendido (el usuario pidió "hazlo completo sin preguntarme").** Cada pausa obligatoria se convierte en un punto de revisión documentado: la lista y sus imágenes circuladas se entregan igual, cada medida faltante queda [PENDIENTE] con su RFI en vez de preguntarse, y la entrega trae una pestaña "Revisar en la mañana" (en español) con todo lo que él normalmente habría confirmado, cada punto con su delta.

## VERIFICACIÓN CRUZADA DEL BARRIDO — CONTAR TAMBIÉN POR GRAFÍA

El barrido por tag tiene un segundo camino que lo verifica, y es obligatorio usarlo cuando el legend le da a un tipo una **grafía propia** (hatch, patrón de línea, relleno): se barre la hoja entera buscando esa grafía, sin mirar los tags, y se clasifica cada banda encontrada por su thickness medido.

- Si el conteo por grafía coincide con el conteo por tag, la lista está completa por dos caminos independientes.
- Si no coincide, hay un wall sin tag o un tag sin wall, y hay que encontrarlo antes de cuantificar.
- Incluye también rectángulos cerrados SIN hatch (medias walls, stubs) y bandas pegadas a walls exteriores (furring).
- **Un tag puede aterrizar en una CAJA CERRADA y no en un wall corrido** (pilastra, wrap de columna, chase): se cuantifica por PERÍMETRO FURRADO × height, 1 stud por esquina y por borde libre, corner bead vertical en cada arista. Solo las faces EXPUESTAS llevan furring, y se detectan buscando una face paralela a un thickness de furring hacia dentro.

Cómo separar el hatch real del ruido: las diagonales de un hatch van a **paso constante**. Se mide ese paso en una banda conocida y se calcula `densidad = nº de diagonales ÷ (largo ÷ paso + 1)`. En un hatch de verdad da ≈ 1.00; en un falso positivo (las diagonales sueltas de una door leaf, la X de un recuadro, un swing aproximado) baja a 0.4 o menos.

Caso real: las bandas con hatch de la hoja correspondieron 1:1 con los tags de sus types (clasificadas por espesor), con densidad ≈ 1.00 contra ≤ 0.4 de los descartados.

**Todo length NO EXPLICADO se parte por coordenada hasta que cada trozo tenga dueño** — tipo nuestro, otra división, o hueco — y ningún trozo queda sin nombre. Se comprueba leyendo el rótulo dentro del tramo y el perfil de líneas.

## REGISTRO ENTRE HOJAS Y CRUCE DE MEP

Para cruzar una hoja de MEP contra las bandas de wall de la arquitectónica hacen falta dos cosas, en este orden:

1. **Registro.** Se deriva el offset (dx, dy) entre las dos hojas votando los segmentos lengths de wall del fondo arquitectónico (lw ≥ 1.0, ≥ 50 pt), exigiendo ≥ 25 coincidentes en cada dirección. Las burbujas de eje NO sirven (ver reglas inviolables). Si una hoja no alcanza el mínimo, no se usa para cruce geométrico: se declara y se revisa a ojo. **Verifica el SIGNO del offset con 3 rasgos reconocibles antes de usarlo.** Y ojo con las hojas cuyo MediaBox no es nulo (las de plomería suelen tener origen desplazado): para recortar hay que restar el origen en X y en Y, o los recortes salen corridos.
2. **Cruce.** Una línea cuenta como penetración solo si sobresale ≥ 3 pt por FUERA de las dos faces de la banda, y se filtra por lineweight. Después se descarta todo lo que también exista en la arquitectónica en la misma posición: eso es fondo, no MEP. Las líneas de retícula de ACT del RCP van a paso constante (2'-0") y mueren exactas en las dos faces: se descartan.

Cada penetración se evalúa **individualmente** contra el umbral de 1/4 de hoja, nunca sumada con las demás. Debajo del umbral es patch, y aun así se LISTA. Un ducto que cruza por encima del head de una door sí penetra el wall: arriba del header hay framing hasta el deck. Y toda penetración reportada se abre en imagen para leer su rótulo (tamaño, tag, CFM) antes de cuantificarla, cruzándolo contra el schedule mecánico.

**Penetración EN el stud, no solo entre studs.** El detalle estructural limita el diámetro del agujero en el ALMA y prohíbe cortar las ALAS; un ducto mayor obliga a abertura enmarcada o chase, que es line item nuestra. En un wall de DOBLE ROW el ducto atraviesa DOS almas, así que hace falta un juego de studs por row. Los chases de plomería llevan toe-to-toe stud post + cold rolled channel y van separados mínimo 4'-0".

## PROTOCOLO DE EJECUCIÓN

**PASO 0 — ¿Qué paquete es este set?** Lee el índice y confirma que el set contiene el EDIFICIO (floor plan, Partition Types, RCP). Un bid set puede ser un paquete parcial — canopy, site/civil, MEP — sin obra de interior. Si no hay Partition Types, floor plan ni RCP, el alcance Div 05/09 puede ser CERO: dilo en la primera línea, justifica cada cero con su hoja, y NO fabriques un take-off. Caso real (un set de otro proyecto): canopy, deck, gutter y framing del fascia son del fabricante del canopy, el fascia es "by others" y el soffit es pan deck expuesto; lo único posiblemente nuestro eran los column wraps sin detalle → RFI con alterno valorizado, fuera del base. Ojo al contar columnas de canopy: suelen ser 2 por isla, no una. Confirma también el SISTEMA de framing: si el legend dice WOOD STUDS, aplica la sección SETS CON WALLS DE Wood.

**PASO 0 — Mapa de hojas.** Corre primero `arranque.py <pdf>` (ver su sección propia): automatiza la parte mecánica de este paso — copia sin markups, verifica layer vectorial, renderiza, lee el rótulo de cada page_index y arma el mapa, ubica por título el Drawing Index y los schedules, y da un censo preliminar de tags. Se detiene en un punto de control; revísalo antes de seguir. En sets grandes (más de ~40 hojas o ~50 MB) el mapa se arma con `pdftotext` por página. Lee el Drawing Index de la portada a alta resolución. Tabla: título → número → página PDF. Busca por TÍTULO, no por número. Verifica el rótulo real en el title block de cada página — la forma barata de hacerlo es extraer el texto de la esquina inferior derecha de cada página y leer ahí el número de hoja, en vez de contar callouts (si el title block de este set no está ahí, `arranque.py --title-block-zona` se ajusta). **Guarda el mapa page_index → hoja**, y recuerda que `pdftoppm` nombra el PNG con el número 1-based: "...-24.png" es page_index 23. Revisa el Revision Log. Nunca declares una hoja "faltante" sin barrer TODO el PDF por rótulo.

**PASO 0B — Demolition Plan.** Distingue existente que permanece / a demoler / nuevo. Lee las Demolition General Notes completas. "Add GWB/furring as required" casi siempre = patch sobre existente. En obra ground-up no hay demo interior: decláralo y sigue.

**PASO 1 — Building Code Analysis.** SF total, pisos, Construction Classification, Occupancy Group, códigos, occupancy load, tipo de proyecto.

**PASO 2 — Especificaciones Div. 05 y 09.** Tipos de stud/track/bridging/clips, corner guards, reveals, tipo/thickness/marca de cada board, finish level, FRP. Si no hay libro de especificaciones en el set, dilo y deriva de Partition Types + notas generales + hojas estructurales. Lee también la **leyenda de materiales exteriores** de la hoja de elevaciones: ahí se definen los códigos PT-x (thickness real del stucco), SA-x, AF-x, CJ, EPS-x, SS-x, GL-x. Sin esa leyenda no se puede cerrar el thickness de layers de nada que lleve stucco. Ojo con acabados que exigen nivel 5 (wallcovering, felt panels): cambian el costo de acabado — pero comprueba a QUÉ código de wallcovering se refiere esa keynote antes de extrapolarla a todos. Revisa en el Material Schedule la columna de quién suministra/instala (p.ej. FRP "GC / GC"): lo que no está claramente en nuestro alcance va como alterno, no en el base. Si no hay finish level especificado, decláralo como supuesto (Level 4) en Clarifications.

**PASO 3 — Partition Types.** ⛔ Primero la LISTA FIJA DE ALCANCES (regla 52.1, ADENDA v52 al final de este archivo): `alcances.py escanear` + sus 24 renglones al registro. Por cada tipo: height T.O. Wall, stud, layers de board por face (separa regular/W.R./greenboard/FRP/plywood/cement board), Metal Stud Schedule, Brace Schedule, Header Schedule, Stud Notes, Lateral Bracing, Typical Fasteners. Abre el DETALLE de cada tipo, no solo la fila de la tabla, y lee su NOTA DE CONSTRUCCIÓN completa: ahí pueden venir calibre, spacing, anchorage y trim distintos de los del schedule general. **Y barre la hoja de Partition Types entera buscando detalles que NO son de un tipo con tag** — bulkheads sobre office front, sills y sills, jambs, encuentros, transiciones: son line items nuestras que ningún tag del floor plan va a traerte.

**Mide el detalle por geometría, no a ojo.** A 3"=1'-0" son 18 pt por pulgada real: una layer de 5/8" mide 11.28 pt y un stud de 1 5/8" mide 29.25 pt. Así se cuenta cuántas layers hay por face y cuántas rows de stud, que es el dato central.

NUNCA mezcles exteriores con interiores. Orden inviolable: Pasada 1 (exteriores, face afuera) → Pasada 2 (esos mismos exteriores, face adentro; "by future tenant" solo aplica si el wall es NUEVO) → Pasada 3 (interiores). Declara al inicio de cada respuesta qué pasada trabajas.

**PASO 4 — Recorrer el Floor Plan** por cuadrantes, con Construction Legend. El barrido por tag es la Etapa 1 (`inventario_tags.py`); la verificación cruzada por grafía y la pausa obligatoria siguen.

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

### El ejemplo que la originó — un canopy

```
A04.01 (RCP)
   └─ D/A09.22 <título de la sección>   largo en planta, y el fondo
         └─ 7/A09.26 <título del detalle>   composición y datums de la fascia
               └─ 7/S5.20 <título del detalle>   perfil y 16" O.C.
```

**Ningún eslabón da la cantidad solo:**

| eslabón | qué aporta |
|---|---|
| `A02.01` / `A04.01` | el length y la posición |
| `D/A09.22` | el fondo, y lo confirma contra la planta |
| `7/A09.26` | la composición y los datums `T/STUD [valor retirado E24]` − `B/STUD [valor retirado E24]` |
| `7/S5.20` | el perfil `362S137-33` y el 16" O.C., que **ningún detalle de canopy rotula** |

Y de paso la cadena resolvió un pleito abierto hacía días: la dimension de D/A09.22 y el largo
medido en planta **nunca estuvieron en conflicto**. Localizando los dos ticks de la dimension en
el vector del PDF (escala calibrada contra tres datums) se ve que la dimension va del **eje** a la
**fascia**, no de face de wall a fascia; la diferencia es exactamente el offset que 7/A09.26
imprime arriba. Dos caminos independientes, a dos escalas distintas, cerrando.


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
- **`adenda_v26.md`** — ADENDA v<n> — <n>-sep-<n> · lo que salió de la auditoría adversarial de un proyecto anterior
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
- **`adenda_v27.md`** — ADENDA v<n> — <n>-sep-<n> · la compuerta de SIGNIFICADO de columna
  - De dónde salió
  - REGLA — Una columna de resumen no se entrega sin una recomputación independiente
  - La pregunta que hay que hacerle a cada columna
  - Qué verifica la compuerta (`verif_columnas.py`)
  - REGLA — Una compuerta que nunca se ha visto fallar no sirve
  - REGLA — El decimal raro se investiga, no se redondea
- **`adenda_v28.md`** — ADENDA v<n> — <n>-sep-<n> · la compuerta de COBERTURA
  - De dónde salió
  - No era error: los studs de abertura
  - El hueco de verdad
  - REGLA — Un elemento que no aparece en ninguna lista no es "sin nada": es SIN REVISAR
  - REGLA — Un `continue` por tipo de geometría es una bomba
  - Cómo se cerró
  - Probado viéndolo fallar
- **`adenda_v29.md`** — ADENDA v<n> — <n>-sep-<n> · la compuerta del LIBRO
  - De dónde salió
  - Los cinco errores de dinero, todos de la misma raíz
  - REGLA — La familia del material manda sobre el waste y sobre el length de compra
  - REGLA — Un PENDIENTE se escribe PENDING, nunca como 0 ni omitido
  - REGLA — Clasificar por el ENCABEZADO del renglón y por PALABRA COMPLETA
  - REGLA — Auditar un libro SIN RECALCULAR reporta decenas de fallos fantasma
  - La compuerta: `verif_libro.py`
  - Lo que sigue sin resolverse, y se dice
- **`adenda_v30.md`** — ADENDA v<n> — <n>-sep-<n> · barrido de ZONAS HÚMEDAS
  - De dónde salió
  - REGLA — Censo por CUARTO, cruzando TRES fuentes
  - Lo que salió
  - REGLA — Una nota que nombra DOS aparatos hay que leerla como DOS walls
  - REGLA — El censo de zonas húmedas lleva compuerta de cobertura
  - REGLA — El W.R. es RECLASIFICACIÓN, no board nuevo
- **`adenda_v31.md`** — ADENDA v<n> — <n>-sep-<n> · NINGÚN CAMBIO ESTÁ TERMINADO HASTA QUE EL EXCEL SE REGENERA
  - De dónde salió
  - El riesgo que cubre
  - REGLA
  - COMPUERTA DE VIGENCIA — `verif_vigencia.py`
  - UNA SOLA PUERTA DE SALIDA — `entregar.py`
  - Corolario para el ORDEN PERMANENTE
  - Error de la propia compuerta, cazado en su primer arranque
- **`adenda_v32.md`** — ADENDA v<n> — <n>-sep-<n> · TODO NOMBRE DE MATERIAL SE ESCRIBE EN INGLÉS
  - De dónde salió
  - REGLA
  - Glosario
  - COMPUERTA — `verif_idioma.py`
  - Tres cosas que costaron y no hay que repetir
  - Para tocar un cierre YA SELLADO — `traducir_materiales.py`
  - Los documentos históricos se CONGELAN, no se traducen
- **`adenda_v33.md`** — ADENDA v<n> — <n>-sep-<n> · EL JUEGO DE PLANOS MARCADOS ES AUTOMÁTICO
  - De dónde salió
  - REGLA — No se pregunta, no se ofrece, no se espera
  - Qué compone el juego, sin faltar ninguno
  - El NOMBRE dice qué contiene
  - Dónde se guardan
  - Sigue valiendo todo lo de antes
- **`estructura_carpeta.md`** — ESTRUCTURA DE CARPETA, EN CADA PROYECTO
  - Una sola versión vigente, no una pila de versiones
- **`adenda_v34.md`** — ADENDA v<n> — <n>-oct-<n> · COMPUERTA DE COBERTURA DE DETALLES
  - De dónde salió
  - REGLA — No se cierra un proyecto sin haber abierto cada detalle de cada hoja que se usó
  - Lo que encontró en su primera run
  - REGLA — Una cita que una máquina no puede leer no se puede auditar
  - Cómo se usa en un proyecto nuevo
- **`adenda_v35.md`** — ADENDA v<n> — <n>-oct-<n> (noche)
  - El índice se genera, no se escribe (`hoja_indice.py`)
  - Tres reglas nuevas, cada una de un error cometido hoy
  - La carpeta de entrega es el espejo, y tiene que estar completa
  - Sin shell en su PC, el diff se hace por TAMAÑO
- **`adenda_v36.md`** — ADENDA v<n> — <n>-oct-<n> · LA CADENA DE DETALLES SE SIGUE HASTA EL FINAL
  - Las cuatro partes de la regla
  - Qué lo originó
  - Las compuertas
  - Dos bugs propios al escribir la compuerta, los dos de normalización
- **`adenda_v37.md`** — ADENDA v<n> — <n>-oct-<n> · LOS <n> CALLOUTS, CERRADOS
  - 1. El RFI del parapet se CIERRA — el infill de `11/S5.10` SÍ se ubica
  - 2. Una layer que las secciones NO rotulan y los detalles SÍ
  - 3. Dos bugs de compuerta — las dos miraban menos de lo que creían
  - 4. Trampa operativa: `| head` mata el script antes de que escriba
  - 5. El furring de columna es un LAZO CERRADO
  - 6. Lo que la cadena destapó, en line items
- **`adenda_v38.md`** — ADENDA v<n> — <n>-oct-<n> · EL ORDEN DE TRABAJO: PLANO → CADENA → TOTAL → EXCEL
  - ⛔ SUPER REGLA INVIOLABLE
  - La herramienta: `cadena_detalles.py`
  - Lo que la columna destapó el primer día
  - CORRECCIÓN DEL MISMO DÍA — dos errores que la columna destapó en cuanto se miró
- **`adenda_v39.md`** — ADENDA v<n> — <n>-oct-<n> · EL VOCABULARIO DEL TRADE VA EN INGLÉS, SIEMPRE
  - ⛔ REGLA INVIOLABLE
  - CÓMO SE HACE CUMPLIR, QUE ES LA PARTE QUE NO SE OLVIDA
  - LOS TRES ERRORES QUE DESTAPÓ APLICARLA (y las reglas que dejan)
- **`adenda_v40.md`** — ADENDA v<n> — <n>-oct-<n> · LA REGLA DEL INGLÉS SE VERIFICA, NO SE PROMETE
  - ⛔ LO QUE PASÓ, y por eso existe esta adenda
  - LA COMPUERTA: `verif_respuesta.py`
  - POR QUÉ HACEN FALTA DOS LISTAS, Y NO UNA
  - LOS FALSOS AMIGOS QUE SALIERON AL CORRERLO SOBRE EL TEXTO DE VERDAD
  - ALCANCE: también el generador, no sólo la salida
  - TERCER TRINQUETE
- **`adenda_v41.md`** — ADENDA v<n> — <n>-oct-<n> · EL ROOM DE CADA FACE SE VERIFICA, NO SE HEREDA
  - ⛔ REGLA INVIOLABLE
  - LOS CUATRO CASOS QUE LA ORIGINARON, el mismo día
  - LA COMPUERTA: `verif_caras.py` (paso 12 de 17)
  - EL OTRO HALLAZGO DEL DÍA: A1 #n, `[DERIVADO]` → `[CONFIRMADO]`
- **`adenda_v42.md`** — ADENDA v<n> — <n>-oct-<n> · UNA ELEVACIÓN NO ES UNA HEIGHT, Y UN `[CONFIRMADO]` TIENE QUE CITAR SU PRINTED DIMENSION
  - ⛔ REGLA INVIOLABLE
  - CÓMO SE ENCONTRÓ (armando el HANDOFF, no revisando cantidades)
  - POR QUÉ `verif_confirmado` NO LO CAZABA — el hueco más grande que tuvo esa compuerta
  - LA COMPUERTA NUEVA: `verif_coherencia.py`
  - UNA NORMALIZACIÓN DUPLICADA SE DESINCRONIZA SOLA
  - EL MAPA DE HOJAS SE CRUZA CON DOS FUENTES, Y SE DICE DÓNDE NO CUADRAN
  - EL REGISTRO DE LO QUE EL USUARIO CONFIRMÓ NO EXISTÍA COMO ARCHIVO
- **`adenda_v44.md`** — ADENDA v<n> — <n>-oct-<n>
  - Barrido de los detalles sin abrir, y el error que cometí en medio
  - REGLA 44.1 — BARRIDO POR TAG DE SCHEDULE, NO POR WALL
  - REGLA 44.2 — UN ROLL-UP POR CLAVE NO ES UN INVENTARIO DE CONTENIDO
  - REGLA 44.3 — UNA COMPUERTA NO SE DA POR BUENA HASTA VERLA FALLAR
  - Lo que el barrido movió, ya sellado
- **`adenda_v45.md`** — ADENDA v<n> — <n>-oct-<n> (tarde)
  - Cobertura de detalles a cero, atraso de [CONFIRMADO] a cero, y el mapa de adyacencia
  - REGLA 45.1 — UNA CITA QUE PRUEBA QUE EL MATERIAL VA NO PRUEBA CUÁNTO HAY
  - REGLA 45.2 — UN EXTREMO QUE EL MAPA NO RESUELVE NO ES UN EXTREMO LIBRE
  - COBERTURA DE DETALLES: <n> PENDIENTES → 0
  - Estado al cierre
- **`adenda_v46.md`** — ADENDA v<n> — <n>-oct-<n>
  - La regla de waste, ampliada, y los tres renglones que destapó
  - REGLA 46.1 — UNA REGLA ESCRITA COMO DOS LISTAS DEJA HUECOS; ESCRITA COMO PARTITION, NO
  - REGLA 46.2 — DOS CELDAS QUE SIGNIFICAN LO MISMO SON DOS FUENTES DE VERDAD
  - Lo que NO lleva waste, y por qué — explícito para no volver a preguntarlo
  - RFIs
- **`adenda_v47.md`** — ADENDA v<n> — <n>-oct-<n>
  - Lo que se corrigió, y por qué importa
  - REGLA 47.1 — UNA COMPUERTA QUE CUENTA POR RENGLÓN NO PUEDE VER LA CERCA
  - El test, y la prueba de que falla sin el arreglo
  - El caso que casi quedó decorativo (y cómo se cazó)
  - Lo que se pagó, no lo que se eximió
  - Estado de la entrega

# ADENDAS v48–v60 (historia; sus reglas siguen salvo que el PROTOCOLO v69 diga otra cosa)

> **v61 → v69:** desde v61 el agente solo mide el plano y lo escribe en `takeoff_canon.json`; las cantidades de
> toda familia con tool salen de las tools. Los protocolos v61–v68 se retiraron de este archivo; los reemplaza el
> PROTOCOLO v69 del inicio. Cualquier regla 50.x–60.x que choque con él queda ANULADA (§9).

# ADENDA v48 — 11-oct-2026 · UNA SOLA CARPETA DE HERRAMIENTAS, Y TODO LO NUEVO VUELVE A ELLA

## Lo que se corrigió, y por qué importa

Las herramientas vigentes no vivían en `_herramientas/`: estaban dentro de la carpeta de
un proyecto (`<proyecto>/.../2 - Take-Off Claude/Herramientas`), y en
`_herramientas/_herramientas_py/` quedaba un kit viejo del 26-sep con versiones distintas de
`closer.py`, `arranque.py` y `planmark.py`. Un take-off nuevo que siguiera la regla al pie de
la letra habría copiado las versiones viejas. Se consolidó todo en **`_herramientas/py/`**
(las del proyecto + `zoom.py`, `registro2.py`, `cotas.py`, `tagband.py` rescatados del
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
(la vieja ya tenía archivos de un proyecto mezclados de distintas fechas). Con la automatización corriendo
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

El SKILL.md pasó de un archivo único de más de 250 KB a un archivo central más `referencias/` con 23
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

## Por qué (error real, prueba automática 13-oct-2026)

La prueba automática se entregó con `registro.py entregable` en 0 y aun así le faltaban alcances
COMPLETOS: ceiling suspension (furring channel, carrying channel, hanger wire, ceiling track), el
canopy (soffit, fascia, CANOPY-COL) y el exterior FRT plywood sheathing (dejado como "alternate").
El back-check confirmó con hoja+detalle que la
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

## REGLA 52.2 — CARPETA DE TRABAJO POR VARIABLE, NUNCA UNA RUTA FIJA

Las herramientas de `py/` leen su carpeta de trabajo de `TAKEOFF_WORK` y la de salida de
`TAKEOFF_OUT` (antes estaban fijas en una carpeta de un proyecto y en `/mnt/user-data/outputs`, que en la nube
no existen o traen datos de otro proyecto). Al empezar cada take-off: `export TAKEOFF_WORK=<carpeta del
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

Origen: el arbitraje de una prueba (ARBITRAJE.md, 14-oct) encontró partidas donde el plano
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
planta (ej.: nota A de A02.01). Las caras de un chase húmedo se miden cara por cara.

## REGLA 53.9 — HALLAZGOS DEL ARBITRAJE (protocolo)
1. FRP: la altura impresa se mide SOBRE el cove base (ej.: A-D/A08.01).
2. (ANULADO en v77c por R77.12 / U8: acoustical sealant EXCLUIDO) Acoustical sealant sigue el detalle de CADA partition type (2×, 4× o 0 lados); el exterior y el
   parapet NO llevan acoustical sealant salvo que su detalle lo diga.
3. "SEALANT AT BASE OF GYPSUM" exterior es su PROPIO renglón (no acoustical).
4. Glass mat sheathing y FRT plywood de column wraps / piers salen de sus detalles de pared exterior:
   se buscan siempre (una prueba los omitió).
5. Moisture resistant board va donde lo diga la nota (ej.: chase detrás de toilet y lavatory).

# ADENDA v54 — 15-oct-2026 · ERRORES DEL ARBITRAJE DE LA PRUEBA #4

Origen: el árbitro de la prueba #4 (ARBITRAJE.md, 15-oct) revisó familias contra el plano. Cada error es ahora una regla. OBLIGATORIAS en todo
take-off y back-check.

## ⛔ REGLA 54.1 — FRAMED OPENINGS DE FIXTURES
Todo recessed fixture dentro de framing (GWB ceiling, soffit, canopy de CFMF exterior) lleva framed
opening = 2 × largo del schedule + 2 ends por fixture. El ancho de los ends sale del cutsheet; si no
está impreso, queda [PENDIENTE] + RFI. Largo: luminaire schedule (ej.: E00.01). Conteo: tags del
lighting plan (ej.: E02.01). PROHIBIDO medir el largo en el RCP. Antes de cerrar, barrer TODOS los tipos
de la familia (todos los tipos del luminaire schedule) y listar cada tag con su imagen circulada.
Error que la originó: una prueba midió el canopy en el RCP y le faltaron tipos del schedule, que
daba bastante más.

## ⛔ REGLA 54.2 — TRACK POR POSICIÓN + DUPLICADOS
Bottom, top y deflection track van en renglones SEPARADOS. Un callout "TOP & BOT." genera DOS renglones,
nunca uno dentro de la familia bottom track (ej.: 11/S5.10).
54.2b: dos renglones de la misma familia con el mismo neto y la misma cita = duplicado. Se corrige
antes de entregar (ej.: un canopy track contado dos veces con 7/A09.26).

## ⛔ REGLA 54.3 — MATERIAL DEL BLOCKING
El material lo dice el detalle. "STUD BLOCKING 362CR22" / blocking at edge of gypboard (ej.: 4/S5.20)
= METAL, renglón propio "Stud blocking 362CR22". FRT / FRTW solo donde el detalle lo rotule. Barrer
también las elevaciones interiores (artwork, monitores, TV) y las notas de hoja (millwork, toilet
accessories, wall stops). Ej.: parapet blocking = 4/A09.26.

## ⛔ REGLA 54.4 — ACOUSTICAL SEALANT CORRIDA POR CORRIDA
**ANULADA en v77c por R77.12 (U8): acoustical sealant EXCLUIDO en todos los proyectos.** Texto histórico:
Tabla por partition type: corridas top / bottom × caras, leída de CADA detalle. Cantidad = Σ largo ×
corridas. PROHIBIDO usar el punto medio de un rango. Línea dibujada sin rótulo = RFI con su delta
(ej.: base de un type sin rótulo; "SEALANT" del office front 9/A12.01).

## ⛔ REGLA 54.5 — SHEATHING SOLO DONDE SE ROTULA
Cada capa de sheathing (glass mat, exterior gyp, FRT plywood) va solo donde un detalle la rotule.
Sobre storefront manda el head detail (ej.: 2/A09.26 = steel header, SIN glass mat). Los descuentos de
aberturas del Material Summary deben ser IGUALES a los del Partition Takeoff, renglón por renglón; se
comparan antes de entregar. Deck con pendiente → B.O.D. promedio del tramo, por fachada (nunca juntar
dos fachadas en un número). Nota: 53.5 (parapet exterior gyp sheathing sobre storefront) sigue igual;
54.5 solo quita el glass mat donde el head detail no lo rotula.

## ⛔ REGLA 54.6 — LA CITA DEBE SER EL DETALLE QUE TIENE LA NOTA
Cada N/HOJA debe coincidir con el título del detalle que contiene la nota citada. Antes de entregar se
abre cada cita y se confirma. Errores encontrados: 6/A09.26 (STOREFRONT BASE) citado para el parapet
blocking (correcto 4/A09.26); 7/A09.26 (SIDE CANOPY) citado para el glass mat (correcto 5 y 3/A09.26).

# ADENDA v55 — 15-oct-2026 · ERRORES DE LA PRUEBA #5 Y DE SU ARBITRAJE

Origen: (a) los agentes adversariales de la prueba #5 encontraron errores y alcances sin cuantificar;
(b) el árbitro de la prueba #5 (ARBITRAJE.md, 15-oct) revisó familias contra el plano. Cada error es
ahora una regla. OBLIGATORIAS en todo take-off y back-check. Los criterios 53.x aprobados por el usuario
siguen mandando: si una regla de aquí choca con un 53.x, gana el 53.x.

## ⛔ REGLA 55.1 — EL CRÍTICO DE COMPLETITUD SE CORRE SIEMPRE
Antes de entregar, un agente revisa hoja por hoja (incluidas las que nadie citó) buscando alcances sin
cuantificar. En una prueba encontró alcances completos fuera: roof step (4/A02.02), coiling grille
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
  (ej.: una torre que corre entre dos grids).
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
**ANULADA en v77c por R77.12 (U8): acoustical sealant EXCLUIDO.** Texto histórico:
Las corridas de abajo se descuentan en cada door R.O. (no hay sealant cruzando el vano).

## ⛔ REGLA 55.6 — MOISTURE RESISTANT BOARD
Va solo en las caras donde se apoya un toilet o lavatory según el plano ampliado y su nota (ej.: nota
F/A08.01 = solo el chase C1). Se desglosa muro por muro.

## REGLA 55.7 — HERRAMIENTAS (ya corregidas)
- alcances.py ahora rotula cada página con el número del title block (letra más grande). Antes salía la
  hoja más citada (A02.01 salía "A9.22").
- familias.py (calificador) ahora tiene familia propia de purlin y de stud blocking metálico.

## NOTA — PROPUESTA NO APLICADA
El árbitro propuso "studs extra solo si un detalle los pide". Choca con el criterio 53.2 aprobado por el
usuario (+1 por esquina/T, +2 por jamb). No se aplica; queda para que el usuario decida.

# ADENDA v56 — 15-oct-2026 · ERRORES DE LA PRUEBA #6 Y DE SU ARBITRAJE

Origen: prueba #6 (skill v55) y su árbitro (ARBITRAJE.md, 15-oct). Cada error es ahora una
regla. OBLIGATORIAS en todo take-off y back-check. Los criterios 53.x aprobados por el usuario siguen
mandando. Decisiones del usuario del 15-oct ("haz lo mejor para el proyecto") quedan anotadas.

## ⛔ REGLA 56.1 — REGISTRO ANTES DEL PRIMER NÚMERO
La medición exploratoria se permite, pero `registro.py crear` se corre al terminar el PASO 3 y ANTES de
escribir el primer número al modelo (refuerza 50.1; la #4 y la #6 lo hicieron al revés).

## ⛔ REGLA 56.2 — NOTAS GENERALES ESTRUCTURALES ANTES DE LOS DETALLES S5
Antes de S5.xx se leen las notas generales S1.xx ("LIGHT GAUGE STEEL FRAMING"): gauge mínimo, O.C. en
esquinas, deflection clips. Si S1.xx y un detalle o schedule NO coinciden en gauge / O.C., va a RFI con
las DOS cantidades; el take-off lleva la de MÁS material (53.3) marcada [DERIVADO] (ej.: S1.11 nota 5
vs 7/S5.20).

## ⛔ REGLA 56.3 — UNA CAPA DE DETALLE DE BASE O BANDA VA SOLO DONDE SE DIBUJA
Una capa que solo aparece en un detalle de base o de banda se cuenta solo donde ese detalle la dibuja.
Antes de extenderla a todo el muro, se revisa el detalle con zoom de 300 dpi o más y se circula la
evidencia. Ej. (decidido 15-oct): 5/8" glass mat solo en la banda de base que dibuja su detalle (5/A09.26, 9/A09.27) y en
la banda del canopy (3 y 7/A09.26); arriba, el FRT plywood bonded polyiso va directo al stud.

## ⛔ REGLA 56.4 — DONDE TERMINA EL STUD DEL MURO
Si el detalle estructural (ej. 10/S5.10) corta el muro en un deflection track bajo la viga, los studs del
muro terminan ahí. El parapet es infill aparte (11/S5.10) en TODO el perímetro.

## ⛔ REGLA 56.5 — UN MURO NUEVO SE UBICA CON IMAGEN ANTES DE SUMARLO
Un muro nuevo que mide lo mismo que uno ya contado es el mismo muro. Todo muro nuevo (sobre todo de torre o
parapet) se ubica con imagen circulada en la planta o el roof plan antes de sumarlo (ej.: una prueba sumó
sheathing en muros de torre que no existen).

## ⛔ REGLA 56.6 — SEALANT = BEADS DIBUJADOS
Las corridas de sealant son los beads dibujados en cada detalle. Un símbolo igual al que tiene rótulo en
otro detalle del mismo set SÍ es sealant (ej.: G/G1 en 5/A12.01). El sealant de base exterior no cruza
storefronts ni doors. Un tipo cuyo detalle no dibuja bead no lleva sealant (ej.: F, 12/A12.01).

## ⛔ REGLA 56.7 — BULKHEAD DE OFFICE FRONT
La altura sale del HOLD impreso en la elevación interior (ej. 2/A11.01 "… HOLD TYP. FROM SLAB"),
no del ceiling de la oficina.

## REGLA 56.8 — STUD BLOCKING SIN UBICACIÓN
Si el detalle de blocking es NTS y no da ubicación (ej. 4/S5.20 "PROVIDE BLOCKING AT THE EDGE OF
GYPBOARD"), se lleva una fila en la junta horizontal del board donde el muro es más alto que el largo del
board, + RFI con las opciones (ej.: exteriores + types de doble capa).

## REGLA 56.9 — TRIMS SIN CALLOUT
El metal trim que no tiene callout en ningún detalle pero que pide el criterio 53.1 va en su propio renglón
"metal trim (criterio 53.1)". El gypsum edge trim se nombra "metal trim - gypsum edge trim" para que entre
en su familia.

## REGLA 56.10 — HERRAMIENTAS (corregidas)
`plantilla_excel.py validar` ya acepta citas con letra (C/A09.21, H/A09.23).

# ADENDA v57 — 15-oct-2026 · 4a COMPUERTA: BITÁCORA DE TOOLS OBLIGATORIAS

## De dónde salió
En las primeras pruebas la sesión a veces NO corrió las tools que el skill exige (registro creado
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
Prueba #8 (v57): varias familias seguían MAL. El arbitraje
contra el plano (carpeta "ARBITRAJE prueba 8 (2026-10-15)", ARBITRAJE_8.md, imágenes circuladas)
decidió cada una. Las reglas siguientes son generales; los detalles citados son solo ejemplos de tipo.

## ⛔ REGLA 58.0 — UNIDADES DE COMPRA (plantilla_excel.py corregido)
`plantilla_excel.py` (py/, test_plantilla 18/18) ya no compra mal:
- todo stud vendido por stick lleva `"cut_ft"` (largo típico de corte) en takeoff.json; sin él NO valida.
  Piezas = studs de ese largo ÷ INT(stock / cut_ft). Un stud de 12–15 ft sale 1 por stick de 20 ft;
- las hojas se cuentan por el AxB de `selling_unit` (A × B = SF por hoja: "4x8 sheet", "4x12");
- batt, Level 5 y todo lo que se compra por SF: `selling_unit` "SF" (sin AxB, sin "sheet");
- piezas de schedule (EA/PCS con net <= 20, p. ej. access panels) van sin waste; `"waste_pct"` lo fija si hace falta;
- sealant se vende por tubo/LF, nunca "piece 10 ft".

## ⛔ REGLA 58.1 — UN STUD POR POSICIÓN
Nunca stud completo y cripple en la misma posición. Dentro del R.O. de una door: 0 field studs (solo
king + jack + cripples arriba). Bajo un storefront de slab a head: NO hay studs; sobre un steel header
van cripples a largo real (ej. 2/A09.26). Los field studs dentro de un R.O. se restan.

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
Prueba #9 (v58): familias MAL y CERCA. El arbitraje contra el plano
(carpeta "ARBITRAJE prueba 9 (2026-10-16)", ARBITRAJE_9.md, imágenes) encontró 3 causas generales:
(a) largos de muro que entran en el muro perpendicular, en el door frame o se duplican;
(b) reglas de conteo que el agente interpreta a su manera (parapet, esquinas a 12", extremos de doble fila);
(c) un revisor adversarial que contradijo una regla ⛔ y se aplicó.
Las reglas son generales; los detalles citados son solo ejemplos de tipo.

## ⛔ REGLA 59.1 — PURLIN / ANCLAJE AL DECK ES REGLA DE TRACK, NO DE SOFFIT
Todo track que se fija al deck (top track de partitions a deck, soffits, bulkheads, roof step, heads) se clasifica
por su dirección contra el flute. Dirección del flute = perpendicular a los miembros que soportan el deck en el roof
framing plan, por zona. Donde corre paralelo y el set dibuja purlin/anclaje especial (ej. 10/A09.33), cantidad =
LF de track × (largo de pieza ÷ spacing de fasteners impreso) [DERIVADO]. Doble fila =
una pieza. Detalle VIF → CRITERIO + RFI con la otra dirección. (En v58 esta regla estaba en el párrafo de Soffits y
la #9 solo la aplicó al soffit.)

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
su jamb detail (ej. 10/A12.01: un METAL STUD de cierre por muro, no uno por fila).

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

# ADENDA v60 — 16-oct-2026 · ESTABILIDAD: HERRAMIENTAS DETERMINISTAS (studs por nodo, board por face) + reglas 60.x

## De dónde salió
Pruebas paralelas #10A y #10B con el MISMO skill v59: la misma calificación, pero varias familias salieron muy distintas
entre sí (5/8" board, 6" stud, furring). Causa (ARBITRAJE_10.md):
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
Cada face lleva sus layers, validadas contra el detalle del tipo (ej. 5/A12.01). La cota impresa
manda sobre el vector; diferencia > 3" = DISCREPANCIA anotada. Prohibido un campo "layers" total.

## ⛔ REGLA 60.3 — ALTURA DE STUD EXTERIOR
= B.O.D. del wall (59.13) − peralte (d) de la perimeter beam de S2.xx cuando el detalle para el stud en un
deflection track bajo la viga (ej. 10/S5.10). Nunca B.O.D.

## ⛔ REGLA 60.4 — SUSTRATO DE CLADDING NO ES FURRING
Hat channel / Z-girt / furring del metal panel, ACM o stucco es del instalador del cladding: renglón EXCLUDED +
RFI con delta; nunca en la familia furring channel (ej. un panel EPS-n).

## ⛔ REGLA 60.5 — HEADER LF UNA VEZ POR ABERTURA
Header = (R.O. + 1'-4") × 1. El tipo del header schedule (single/double track, 2-CSJ, box) va en la descripción;
el número de members NO multiplica el LF. Recessed accessories no son header.

## ⛔ REGLA 60.6 — CORRIDAS DE UN DETALLE DE SECCIÓN
En cada detalle de sección (roof step, parapet, soffit, bulkhead) se cuentan las corridas de stud
independientes; cada una lleva su bottom y top track y su bracing (ej. 4/A02.02 roof step).

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

## 26. Reglas v78 (decisiones del usuario W1–W4 y arbitraje #26; mandan sobre §25 y todo lo anterior)

Decisiones del usuario (autoridad): **W1** lo que un detalle IMPRIME en un recess de ATM (studs sistered / furring) se
cuenta como extra framing; sin nada impreso, 0; la wall que contiene el ATM sigue solo en su type (R78.36).
**W2** el parapet sigue el largo de la wall exterior de su fachada, salvo detalle que diga otra cosa (R78.37).
**W3** MARKUPS BLUEBEAM: entregable FIJO en todos los proyectos (R78.20–R78.24): `markups_bluebeam.py` escribe una copia
del bid set con una anotación PDF real por wall (Line / PolyLine sobre el eje, color por partition type, Subject = type,
Contents = "TYPE · LF · N/HOJA · id", Author "Take-off") y una página de leyenda al final con totales por type; sin el
PDF verificado contra el canon vigente la entrega es NO ENTREGABLE (bitacora compuerta, entregar.py paso 19b).
**W4** siguen U1–U11 (§25): acoustical sealant excluido; preguntas con el total anunciado y una a la vez; revisión
por floor plan en orden alfabético de type y luego detalles; mensajes cortos.

### 26.1 Bugs de tools (arbitraje #26), cada uno con compuerta y test (test_v78_g1.py, test_v78_g2.py)
| R78.x | regla | compuerta |
|---|---|---|
| R78.1 | El descuento de una abertura en una face de board va en TODAS las layers de esa face: declarar `deduct_opening_sf` = área NETA de la abertura (head − sill); la tool resta `deduct_opening_sf × layers`. El campo viejo `deduct_sf` solo vale en una face de 1 layer (ahí "por layer" y "total" coinciden). | board_caras.py: `deduct_sf` en face de >1 layer = ValueError (ambiguo: declarar `deduct_opening_sf`); `deduct_sf` y `deduct_opening_sf` a la vez = ValueError (doble descuento). |
| R78.2 | En `trim_items`, `lf` es el TOTAL del renglón y `qty` es solo informativo (conteo de piezas / esquinas). Si se mide por pieza: `lf_each` + `qty` (entero ≥ 1) y total = `lf_each × qty`; si vienen `lf` y `lf_each`, deben cuadrar. | canon.py `_trim` / `_trim_lf`: nunca `lf × qty`; `lf_each` sin `qty` entero, `lf ≠ lf_each × qty` (tol 0.01) o sin `lf` ni `lf_each` = ValueError. |
| R78.3 | El detector de idioma del entregable quita antes los ids de wall/elemento SIN dígito (3+ segmentos en MAYÚSCULAS de 1–5 caracteres unidos por guion, p. ej. un sufijo de zona HI/LO) y las listas `#id+id`; no se renombran ids para esquivar el detector. El español real (minúsculas o palabras largas) se sigue detectando. | idioma_es.quitar_ids dentro de idioma_es.es_espanol (lo usan plantilla_excel.verificar vía es_texto_es y verif_idioma). |
| R78.4 | Una face `side: "END"` (jamb return) lleva las layers que dibuja el DETALLE DE LA JAMB, no las del wall (p. ej. solo la layer exterior envuelve la jamb y las interiores mueren contra otro material): `details[d].end_layers {value, source N/HOJA}` (si existe, toda END de ese detalle debe cuadrar) o `face.layers_source` N/HOJA del detalle de la jamb. | board_caras.py: END con layers ≠ layers_per_face sin fuente = ValueError; `end_layers` sin source o que no cuadra = ValueError; las faces no-END siguen exigiendo layers_per_face. |
| R78.5 | Un tag cuyo texto es un partition type del schedule pero cuyo símbolo difiere (radio / forma / tamaño de letra, o hoja sin referencia) es un CANDIDATO (`partition_ambiguo`, `exige_disposicion: true`): se cuenta (su id `PA####` en `tag_ids` de un wall de ESE type) o se descarta en `tags_descartados` {id \| ids, motivo de plano, imagen}. Nunca desaparece en silencio. | comparar.ambiguos_sin_disposicion + etapas.py compuerta: ambiguo sin disposición, citado en un wall de otro type, o descartado sin motivo / imagen = FALLA (antes solo aviso). |
| R78.10 | Un elemento que para bajo una viga pero arranca SOBRE otro (cripples sobre el lintel / box header, vestibule head sobre el box) declara su arranque: `stops_under_beam.base_ft {value, source}`. Altura = B.O.D. − d − base; sin `base_ft` el elemento arranca del piso (B.O.D. − d). Nunca se mueve el bloque a `*_info` ni se usa `beam_override` para esquivar la compuerta. | canon.py `_v68_checks` §6 (E26): `height_ft` ≠ B.O.D. − d − base (± 0.02) = error; `base_ft` sin source o < 0 = error. |
| R78.11 | El espesor medido entre las dos faces es UN campo: `walls[].thickness_measured_in` (número, in). Lo leen canon, R73.7 (segmento sin tag con `default_type_source`) y la spec G_THICK. `thickness_measured_info` es solo un alias de traza y no puede contradecirlo; nunca se escribe el número como texto para pasar una compuerta. Toda clave de wall que lea un chequeo está en el esquema de canon. | canon.py `WALL_KEYS` + `_r78_espesor` (texto o contradicción con `_info` = error); chequeos_v73 `r73_7`; reglas_clasificacion G_THICK. |
| R78.12 | Ninguna cadena de salida de una tool (source, operación, RFI, mensaje) lleva una N/HOJA fija de un set. La fuente sale del canon (`constants.*_source` o el `source` del dato); un default de oficio se escribe `default (no sheet)` y lo pone solo la tool (un canon que lo escribe como fuente = error). Las N/HOJA en comentarios / docstrings son EJEMPLOS y se marcan como tales; los ejemplos de formato usan hojas sintéticas (X / Z). | Tools: headers `SILL_RULE_DEFAULT`, corridas `PURLIN_DEFAULT` / bracing `default_de_oficio`, canon bracing / fascia / mensajes, accesorios stud reinforcement (`mep_sweep.detail_source`) y RFI del head track. Barrido en test_v78_g2 (literal N/HOJA fuera de comentarios / docstrings = falla). |
| R78.13 | La banda de canopy lleva glass mat por defecto. Si el detalle de ESA banda no rotula sheathing, la banda se declara igual (descuenta la nailbase) con `canopies[].band.sheathing: "none"` (o `band.sheathing` para todas) y `{source N/HOJA, img}` del detalle que no lo rotula: no carga glass mat. | canon.py `_banda_sin_sheathing` / `_exterior`: `sheathing` ≠ "none", o "none" sin source N/HOJA o sin img = error. |
| R78.14 | El plywood del FONDO del fascia box (el detalle lo dibuja bajo los studs) se declara `walls[fascia_box].sheathing_bottom_ft {value, source N/HOJA, op}`; canon suma L × value al MISMO material del sheathing de la fascia. Nunca un plywood_strip "fascia" a mano. | canon.py `_fascia_sheathing`: value ≤ 0, sin source N/HOJA o sin op = error. |
| R78.15 | Todo tag descartado o grupo / segmento sin tag cuyo motivo lo remite a otra tarea u otro elemento ("otra tarea", "counted in", "adds to", "es roof_step"…) nombra su `owner`: id del canon (wall / run / ceiling / ítem / tag_id de un wall / tarea del canon) que lo cuantifica; `part_of` vale como owner de un wall. Sin owner, o con un owner que no existe en el canon (o es él mismo) = el grupo quedó sin dueño. | chequeos_v71 `r71_5` (otra tarea sin owner) + `r78_15`; canon.py `_v70_checks` los corre y falla ("sin dueño"). |

### 26.2 Bluebeam markups (W3) y framed openings sin ancho impreso (test_v78_mk.py)
| R78.x | regla | compuerta |
|---|---|---|
| R78.20 | Todo take-off entrega un PDF de MARKUPS: copia del bid set con UNA anotación PDF real (Line / PolyLine, editable, nunca imagen) por wall del canon, sobre el EJE del wall en la hoja de planta donde se midió (`band` H/V: eje (c0+c1)/2 de lo a hi, o p0/p1; D: p0→p1; BOX: huella cerrada), en pt de la página MOSTRADA. Se genera con `markups_bluebeam.py <bid_set.pdf> <takeoff_canon.json> <salida.pdf>` (escribe además `<salida>.json` con annots por hoja / por type y walls sin geometría). Página = `page` 1-based del canon si imprime la hoja de la banda; si no, la del title block (una `page` 0-based se detecta y se avisa). Coordenadas en px o en el mediabox sin rotar solo se convierten si el canon lo declara (`band.units: px` + `dpi`, `band.frame` / `constants.coord_system`) o si caen fuera de la página mostrada y dentro del mediabox sin rotar (aviso en `conversiones`). Un wall sin band / sin coordenadas válidas / sin hoja va a "sin geometría" (leyenda + JSON); nunca se inventa la posición. | `markups_bluebeam.verificar(pdf, canon)`: wall con geometría sin su annot (/NM `TO-<id>`) o en otra página = falla. |
| R78.21 | Cada annot es un markup de Bluebeam: tipo Line / PolyLine (no Stamp, no imagen, no rectángulo), Subject = partition type (convención de la hoja Partition Takeoff; no-partition = `OTHER FRAMING`), Contents = `TYPE · LF · N/HOJA · id` (N/HOJA = el detalle que trae el canon; sin detalle, la hoja), Author `Take-off`. | `verificar`: tipo, Subject, Contents y Author distintos = falla. |
| R78.22 | Color por type con PALETA FIJA y determinista: types ordenados alfabéticamente → paleta de 16 colores (más types = se repite el color con punteado corto); OTHER FRAMING = lavanda con punteado largo. El color identifica el type en el plano y en la leyenda. | `verificar`: color (tol 0.02) o punteado que no es el del type = falla. |
| R78.23 | Los vértices de la annot caen sobre el eje del wall del canon (≤ 3 pt, tolerancia `--tol`) y cubren sus dos extremos: un markup corrido, más corto o más largo que el wall medido no se entrega. | `verificar`: vértice a > tol del eje o extremo sin cubrir = falla. |
| R78.24 | La leyenda va en una página NUEVA AL FINAL del PDF (las páginas del bid set conservan su número = `page` del canon): totales por type (walls, LF, marcados, sin geometría) como texto, una annot Line de muestra por color (Author `Take-off legend`) y la lista de walls sin geometría. Sin PDF de markups verificado contra el canon VIGENTE (sha del canon en el JSON resumen) no hay entrega. | `bitacora.py compuerta` → `bitacora.markups_fallas` (resumen JSON con el sha del canon vigente + `verificar` = []); `entregar.py` paso 19b (y copia el PDF a la entrega). Sin él: NO ENTREGABLE. |
| R78.25 | Framed opening de ceiling (rect) cuyo ancho de hueco NO está impreso (el detalle remite a coordinar con el cutsheet de la fixture): `width_in: null` + `width_status: "PENDIENTE"` + `rfi` (texto) + `width_source` (N/HOJA que lo dice) → estado SIDES_ONLY: LF = 2 × L × qty a la familia framed openings, y RFI de los ends con delta 2 × W × qty (`delta_txt`, `delta_lf_por_in_w`). Si L cabe en el módulo, FITS_MODULE (W ≤ L en una fixture lineal). Nunca se deja la fixture fuera de la tool por no tener ancho. | framed_openings.py `calcular`: PENDIENTE sin rfi, con width_in, en wall o round = ValueError; width_status fuera de CONFIRMADO / DERIVADO / PENDIENTE = ValueError; ancho null sin PENDIENTE = ValueError (`_pos`). |
| R78.26 | Si el detalle da el largo del hueco como largo de la fixture + un agregado impreso (el detalle da la medida como largo de la fixture más una holgura impresa): `length_add_in {value (in), source N/HOJA}` en el item; se suma al largo antes del módulo y del LF. | framed_openings.py: `length_add_in` que no es {value > 0, source N/HOJA} = ValueError. |

### 26.3 Lectura del plano, W1, W2 y blocking (test_v78_w.py)
| R78.x | regla | compuerta |
|---|---|---|
| R78.30 | **Cadena de cotas completa.** La altura / el largo de un elemento en un detalle sale de TODA la cadena de cotas impresa entre sus dos extremos, nunca de un tramo parcial. Ejemplo genérico: un detalle imprime 4" + 2'-2" entre T/SLAB y B/BOX -> el elemento mide 2'-6", no 2'-2". Un stud entre dos box beams = cadena completa entre las caras exteriores − altura de las cajas − capas de acabado que caen dentro de esa cadena. Escribir la cadena entera en la `op` (cada tramo con su cota impresa). v79: SOLO los tramos entre los dos extremos del elemento (R79.1). | lectura; v79: `accesorios._r79_cadena_stud` (rótulo por eslabón + vector) en heads con box beams |
| R78.31 | **Largo de wall = nodo a nodo.** El largo de un wall corre entre sus nodos (corner / T / jamb, R77.10), nunca hasta donde termina el rayado (poché / hatch) del wall corto que llega: en una T el rayado del wall que llega se corta en la cara del wall pasante, pero su largo va hasta el nodo. | lectura (sin tool); R77.10 (band hasta la esquina) |
| R78.32 | **Plies del blocking del parapet** = número de capas que DIBUJA el detalle del remate (capas rayadas, contadas una por una), no la costumbre ni "1 por defecto". `parapets[].plies_blocking` = `{value (entero), source N/HOJA}` obligatorio. | `canon._plies_blocking`: int suelto, sin value, value no entero, sin source N/HOJA o campo ausente = ValueError |
| R78.33 | **Stud blocking en el borde del gypboard** (`constants.sheet_len_ft`): (i) LF = largo de la(s) face(s) cuya PIEZA de board es más alta que la hoja, por stud row (face parcial -> su `length_ft`, no el largo completo del wall; 1 row = el lado más largo; N rows = los N lados más largos); (ii) la altura que cuenta es la de la pieza: si la face arranca sobre el piso (`faces[].board_base_ft`, o el head de la abertura en un `door_bulkhead`) la pieza = `height_ft − base`. Ejemplo: bulkhead sobre una door, face medida 13 ft desde el piso con head 7'-2" -> pieza 5'-10" < hoja -> sin junta, 0. | `canon._edge_blocking_wall`; door_bulkhead con face > hoja sin `board_base_ft` ni head = ValueError |
| R78.34 | **Key notes de acabado se barren como tags.** Una key note de un finish plan / RCP que ordena un acabado (p. ej. "PROVIDE LEVEL 5 FINISH") se trata como un tag: cada círculo de esa key note dibujado en planta ubica una face que se cuenta (room + wall + face), igual que un partition tag; la nota en la leyenda sola no da cantidad. | lectura (sin tool); inventario de círculos por hoja en la `op` |
| R78.35 | **Esquinas por vector.** El dueño de una esquina (qué wall corre de largo y cuál muere contra él) es el wall cuyo CORE (relleno del stud, no el acabado) atraviesa el cuadrado de la esquina en el vector del plano. | lectura (sin tool); esquinas.py / nodos L-T usan ese dueño |
| R78.36 | **(Decisión del usuario W1, reemplaza la parte de R77.11 que mandaba a RFI) ATM / equipo empotrado.** La wall que contiene el recess sigue solo en su partition type (nada se resta ni se mueve). Si un detalle IMPRIME framing adicional en el recess (studs sistered, furring, blocking...), eso SE CUENTA en el renglón "Extra framing - ATM recess": `atm_recess.extra_printed {source N/HOJA, text (literal impreso), lf, op}`. Si el detalle no imprime nada, 0. | `accesorios.atm_recess_valido` / `extra_framing`: sin texto impreso o sin N/HOJA = ValueError; `extra_framing[]` de ATM a mano = ValueError; `chequeos_v72` R72.11 lo mismo |
| R78.37 | **(Decisión del usuario W2) Parapet sigue la wall exterior de su fachada.** Cada `parapets[]` declara `base_walls` [ids de las walls exteriores sobre las que corre, mismo eje] y su `facade`; su `lf` = suma de `length_ft` de esas walls. Solo un detalle que diga otra cosa lo cambia: `lf_override {value (= lf), source N/HOJA, motivo}`. | `canon._parapet_lf_base`: sin base_walls, wall inexistente, base = el propio parapet, facade distinta, o lf ≠ suma (tolerancia de la tool) sin lf_override = ValueError |

### 26.4 Calificador
| R78.38 | El calificador (eval_takeoff / familias.py) califica también las familias de accesorios (no solo stud / track / board). Una familia en modo "excluir" con renglón = MAL. | familias.FAMILIAS (van primero) |

## 27. Reglas v79 (arbitraje #27; mandan sobre §26 donde se tocan)

Cuatro errores de lectura que pasaban las compuertas v78: (a) sumar a la cadena de un head un eslabón que queda fuera
del stud, (b) contar una sola de varias piezas impresas en un recess, (c) cargar como ceiling suspendido un soffit que
una sección de OTRA hoja arma con studs, y (d) poner purlin en filas apiladas que el detalle fija a acero. Cada regla tiene compuerta en tool y test (`tools/test_v79.py`, malo / bueno).

| R79.x | regla | compuerta |
|---|---|---|
| R79.1 | **Cadena del head = la que corre ENTRE los extremos del stud.** En un head con box beams (coiling grille, vestibule, storefront), el stud mide la cadena de cotas impresa desde la cara superior del box de arriba hasta el fondo terminado, menos boxes y board (R78.30). Un eslabón de la MISMA línea de cotas que queda fuera de esos extremos (la zona del spool / motor sobre el box, hasta el soporte o la estructura) no es del stud. Cada eslabón se rotula (`head_build.head_chain_spans`, uno por eslabón: qué cubre) y el stud se mide además en el vector a la escala impresa verificada (`head_build.stud_vector_ft {value, measured_op}`). Ejemplo genérico: línea de cotas 3'-0" + 4" + 2'-2" donde el 3'-0" va del box al soporte → el stud sale de 4" + 2'-2", no de 3'-0" + 2'-2". | `accesorios._r79_cadena_stud`: sin rótulos, rótulo de zona fuera del stud (spool / motor / support / structure / steel / above the box…), sin vector o \|cadena − vector\| > 1/2" = error |
| R79.2 | **ATM / recess: TODAS las piezas impresas, cada una con su operación.** `atm_recess.extra_printed` es una pieza o una LISTA de piezas `{source N/HOJA, text literal, lf, op}`; se suman todas. Toda palabra de pieza adicional que el detalle rotula en el recess (`drawn`: SISTERED, FURRING, BLOCKING, BACKING, CHANNEL) queda cubierta por una pieza cuyo `text` la contenga, o va en `drawn_not_counted [{text, reason}]` con su motivo (p. ej. es del vendor). Contar una y dejar otra rotulada fuera = error. Lo que el detalle no acota (orientación / espaciado del furring) se escribe en la `op` como criterio con su RFI. | `accesorios._r79_cobertura` (dentro de `atm_recess_valido`); chequeos_v72 R72.11 acepta lista |
| R79.3 | **Un detalle es de TODO lo que corta.** El sistema de un ceiling / soffit sale de su detalle aunque la burbuja esté en OTRA hoja: una sección burbujeada en un enlarged plan o en una elevación que corta el ceiling (`system_callout {detail, cuts_this: true, cut_on: hojas de la burbuja, source}`), o un detalle cuyo título nombra el elemento. Un ceiling suspendido sin `detail` no despacha con un `detail_none_reason` que CITA esos detalles: o los usa, o declara `details_checked [{ref N/HOJA, cuts_this: false, why}]` por cada uno. Un elemento cuya ubicación lo nombra SOFFIT no va como ceiling suspendido (furring / carrying / hangers) sin un detalle que dibuje la suspensión (`soffit_suspended_source`); si su sección dibuja studs → `framed_soffit` (sin hangers, sin carrying, sin kickers de transición). | canon `_r79_ceiling_detalle` (en §4 de `_v68_checks`) y `_r70_1` (acepta `cuts_this` + `cut_on`) |
| R79.4 | **Purlin solo donde el top track apoya en el DECK.** Un top track que el detalle fija a acero estructural (slip clip a viga, T/STEEL, "framing to structural steel") no lleva purlin salvo que un detalle lo imprima (`purlin_detail {source N/HOJA, text con PURLIN}`). Las filas apiladas de una misma línea en planta (misma banda) llevan purlin a lo más en UNA (la que toca deck), salvo `purlin_rows_reason`. | canon `_r79_purlin`: purlin con `to_deck_source` de acero sin `purlin_detail` = error; dos filas de la misma banda con purlin = error |

Protocolo de error v79 (corto, para el system prompt):
```
v79: la cadena de un head es la que corre ENTRE los extremos del stud (rotula cada eslabón y mide el stud en el vector); en un recess se cuentan TODAS las piezas impresas (sistered Y furring), cada una con su operación; un detalle es de todo lo que corta: una sección burbujeada en otra hoja ES la fuente del ceiling / soffit que corta, y un soffit no va suspendido sin detalle; purlin solo donde el top track apoya en el deck (no en tope a acero, una sola fila por línea apilada).
```

## 28. Reglas v80 (arbitraje #28; mandan sobre §27 y §26 donde se tocan)

Origen: una corrida quedó NO ENTREGABLE porque dos tools del paquete verificaban la misma regla con criterios
distintos (un dato verdadero no pasaba las dos); otra infló el LF de su type exterior y su track contando filas
apiladas en una viga que ningún detalle parte; el extra framing de un recess salió de tramos medidos en vector en vez
de la cota impresa; y una familia calculada por el canon desapareció del Excel sin aviso. Cada regla tiene compuerta en
tool y test (`tools/test_v80.py`, malo / bueno; `tools/test_consistencia_tools.py`).

| R80.x | regla | compuerta |
|---|---|---|
| R80.1 | **Un criterio por regla, compartido.** Cuando dos tools verifican la misma regla (la que calcula y su espejo en `reglas.py` / `chequeos_v7x.py` / `inventario.py`), las dos llaman a la función de `tools/criterios.py`; ninguna la reimplementa. Una regla nueva de canon.py entra con su espejo (o el espejo la llama). Si una compuerta rechaza un dato que otra acepta, es bug del paquete: se para y se reporta con el dato verdadero (nunca se maquilla el dato). | `test_consistencia_tools.py`: pares tool / espejo con los mismos casos malo / bueno (system_callout, purlin, anchors, ATM, filas apiladas), barrido estático de `criterios.CAMPOS_COMPARTIDOS` y clasificación de R79.x / R80.x con su espejo |
| R80.2 | **Viga dentro de la zona del stud: el wall va CONTINUO.** Una viga (canopy, lintel) dibujada dentro de la cavidad del stud no parte el wall por sí sola: una pieza, un bottom y un top track, alto hasta la viga de arriba, y el split va a RFI con su delta (+track, −stud). `constants.canopy_beam_split true` solo con un detalle que IMPRIMA el track en esa viga (`split_track_detail {source N/HOJA, text con TRACK / RUNNER / DEFLECTION}`). Una fila apilada (`split_of`) cae dentro de la huella de su padre (Σ de los tramos de un nivel = el wall padre; dos filas sobre el mismo tramo = error), NO suma LF a la lista de walls de su type (va a OTHER FRAMING como `stacked_row`) y NO apoya en losa (sin slab pins ni expansion anchors). | `inventario._apilados` (criterios.split_valido + filas_dentro_del_padre); `partition_types` (stacked_row); `accesorios.track_slab` y `reglas.A_ANCHORS` (criterios.fila_apilada) |
| R80.3 | **Recess de ATM / equipo: lo IMPRESO se cuenta con la regla de la tool.** Studs sistered y furring rotulados en el detalle del recess: `atm_recess.recess {width_ft {value, source} (huella del recess en planta), height_ft {value, source, printed: texto de la cota IMPRESA del detalle}, oc_in {value, source} (16" por defecto, criterio con RFI)}`; la tool calcula sistered = ROUNDUP(ancho / O.C.) piezas × alto impreso y furring = ROUNDUP(alto / O.C.) filas × ancho. Un tramo medido en vector no reemplaza la cota impresa (#0); contar a través del R.O. en vez del ancho del recess = error; SISTERED / FURRING en `drawn_not_counted` (p. ej. "alcance del instalador del cladding") = error. Las otras piezas (blocking, backing) siguen con `lf` + `op`. | `accesorios.atm_recess_valido` (criterios.recess_valido / pieza_atm_lf); `chequeos_v72` R72.11 la llama |
| R80.4 | **Toda familia del canon llega al Excel.** `plantilla_excel.fusionar` agrega el renglón de plantilla de cada familia de `familias_out.json` con NET > 0 que la corrida no escribió (el blocking de metal por origen: edge / items). Una familia calculada que no aparece en Material Summary = error. | `plantilla_excel.familias_faltantes`; `reglas.A_COBERTURA` (modo final) |
| R80.5 | **La bitácora es de la corrida.** `bitacora.py run / compuerta / backcheck` sin `$BITACORA` y con la bitácora dentro de la carpeta de las tools = error (rc 2): se define `BITACORA=<carpeta de trabajo>/bitacora.jsonl` o se corre desde la carpeta de trabajo. | `bitacora.bit_fuera_de_tools` |
| R80.6 | **El PDF de geometría se da explícito.** `mep.py ... --pdf <copia SIN /Annots>` o `$TAKEOFF_PDF`; si el PDF no existe, error claro con los PDFs de la carpeta (nunca un nombre por defecto inexistente). | `geo._pdf_ok`, `mep.py --pdf` |
| R80.7 | **"PENDIENTE" no es evidencia.** En `evidencias_reglas.json` un valor que empieza con PENDIENTE / PENDING / TODO no cumple la regla: antes del modo final se lista en `reglas_out.pendientes_entrega`; en modo final (`--excel`) es falla. | `reglas.revisar_b` |
| R80.8 | **Ducto por su kind.** Un cruce MEP declarado `kind: duct / fire_damper / duct_sleeve` es ducto (lleva sleeve) aunque su ref no lo diga; `kind: pipe` no. El texto del ref solo decide cuando no hay kind. | `accesorios._es_ducto` |
| R80.9 | **Marcado de walls gruesos de núcleo blanco.** La sonda de tinta de `planmark.py` prueba el eje y las dos caras de la banda; vale si el eje tiene tinta o si las DOS caras la tienen (parapet dibujado con dos líneas). | `planmark.Hoja.sondas` |
| R80.10 | **Type K: manda el HATCH sobre el nodo.** En un wall K el LF es la extensión del hatch (R72.1) aunque la línea siga hasta el nodo (R78.31); en la Etapa 3 la lectura que cumple R72.1 es la propuesta por defecto. `length_basis` / `length_op` / `hatch_extent` de un wall K que cita nodo a nodo o R78.31 = error. | `chequeos_v72.r72_1` |
| R80.11 | **El stud blocking de borde no se omite en silencio.** El canon declara `constants.sheet_len_ft {value, source}` (largo de hoja del estimador, con el detalle de blocking que lo pide) o `edge_blocking_none_reason` que cite el N/HOJA del detalle de blocking revisado y por qué no aplica. Sin ninguno = error (antes la familia salía 0 sin aviso). | `canon._r80_11_edge` |

Protocolo de error v80 (corto, para el system prompt):
```
v80: un criterio por regla en tools/criterios.py (si dos compuertas se contradicen, es bug del paquete: parar y reportar, nunca maquillar el dato); una viga dentro de la cavidad del stud NO parte el wall (continuo + RFI) salvo track impreso en la viga, y una fila apilada no suma LF a su type ni lleva anchors de losa; en un recess de ATM sistered y furring salen de la cota IMPRESA y del ancho del recess (la tool calcula); toda familia del canon llega al Excel y el blocking de borde se declara o se descarta con N/HOJA; PENDIENTE no es evidencia; en un wall K manda el hatch sobre el nodo.
```

## 29. Reglas v80e (corrida Barnes & Noble Colorado Springs, 2026-10-24; cada una con su tool corregida)

Origen: un set con texto vectorizado, sheet numbers sin decimal ("A-101", "M-102"), dos plantas de escala distinta
(1/8" y 1/2"), sin hojas S y sin header schedule hizo fallar compuertas con datos verdaderos. Cada falla se corrigió en
la tool (no en el dato) y queda como regla genérica (sin números de proyecto).

| Regla | Texto | Tool |
|---|---|---|
| R80e.1 | Sheet number con o sin decimal: toda regex de hoja acepta `A12.01` y `A-101` / `A-400A` (3 dígitos + letra). Una cita "2/A-410" es N/HOJA válida. | reglas, chequeos_v71/72/73/76, markups_bluebeam, contar_tags, plantilla_excel, accesorios, canon, framed_openings |
| R80e.2 | Escala por hoja: `constants.plan_scale_by_sheet {hoja: {value, source}}`; toda tool que pasa pt <-> ft de una band usa `criterios.escala_hoja` (R80.1). Sin la llave, nada cambia. | criterios, particion, partition_types, comparar, etapas, esquinas, inventario, chequeos_v72/77 |
| R80e.3 | Stud de 8" = familia propia (opcional); "8\"" se busca DESPUÉS de "3-5/8\"" (está contenido en él). | canon |
| R80e.4 | Caras de cement board y de 1/2" exterior gyp sheathing en walls (`board`: "1/2 cement board", "1/2 exterior gyp sheathing"). | canon |
| R80e.5 | Header que ningún schedule / detalle llama: `header: "not_called"` + `header_source` + `header_rfi` -> 0 LF + RFI (R71.10 expresable). | canon |
| R80e.6 | Set sin hojas S: `opening_schedule.sources_none.S` con el motivo del índice; `vigas_sobre_walls.py ... NONE ...` da resultado vacío con motivo. | canon, vigas_sobre_walls |
| R80e.7 | Registro MEP < 25: `mep_sweep.registro.no_usable {motivo, source, img}` -> la hoja no se usa para cruces (mep.py) y stud reinforcement va a RFI. | reglas A_MEP_SWEEP |
| R80e.8 | Types comparados normalizados (H2a = H2A) en comparar.py. Column wrap sin tag de partition = OTHER FRAMING. | comparar, partition_types |
| R80e.9 | §0.F hecho tool: Partition Takeoff en el orden del schedule (`type_order` del takeoff.json), por Wall ID dentro del type, SUBTOTAL por type (texto en col. B) y GRAND TOTAL = suma de subtotales. | plantilla_excel |
| R80e.10 | Hoja con texto vectorizado: barrido de tags por símbolo en vector (rombo / hexágono) + lectura visual en hoja de contactos, declarado como barrido manual en el inventario (mismo esquema, recortes verificados con anillo + tinta). | inventario (proceso) |
| R80e.11 | Inconsistencia conocida (reportada, no maquillada): R75.7 (return corto desde la cara exterior) hace que R70.2 vea la esquina doble; se declara `corners_ok` con el motivo R75.7. Pendiente de unificar en criterios.py. | esquinas / chequeos_v75 |
| R80e.12 | Walls curvos: cada arco va en cuerdas D (una fila por cuerda en la Partition Takeoff); pendiente: band "ARC" para un wall por arco. | partition_types (pendiente) |
| R80e.13 | `alcances.py compuerta`: una nota NO APLICA cita hojas con guion (A-410, A-226A) o la página `pN` del escaneo; antes solo aceptaba A21.10 y ningún NO APLICA de un set con guion podía cerrar. El escaneo de alcances es CIEGO a hojas con texto vectorizado: los alcances se cierran leyendo las hojas A (key notes, schedules), no solo lo que el escaneo encontró. | alcances.py (CITA_RE) |
| R80e.14 | `closer.py`: RE_HOJA / RE_DET / RE_NHOJA aceptan letra final (A-400A) y RE_CITA acepta N/HOJA con guion (2/A-410, 1A/A-410, G/A-221). Toda key note del floor plan que diga BLOCKING / PATCH / FURRING se sigue hasta su detalle (C12 -> 12/A-412, C16 -> 8/A-413) antes de excluir esa partida en el cierre. | closer.py; regla de cadena |
| R80e.15 | `markups_bluebeam.py`: la escala /Measure sale de `constants.plan_scale_by_sheet[hoja]` cuando existe (planta 1/8" + ampliada 1/2" en el mismo set); una sola escala medía la ampliada 4x larga. | markups_bluebeam.py (escala(canon, sheet)) |
| R80e.16 | Familia `1/2" EXTERIOR gyp sheathing`: en familias.py (antes que la de 5/8", el regex "exterior" la tragaba), en el nombre del Excel y en ALC-09; y toda familia en SF que cae al respaldo R80.4 de plantilla_excel es board (6 %, hoja de Inputs), no metal (15 %, piece). | familias.py, plantilla_excel.py, alcances.py |
| R80e.17 | `bitacora.py compuerta` busca el resumen de markups también en `<work>/6_markups` (carpeta de etapas.py); antes daba "no hay PDF de markups" con el PDF verificado ahí. Correr con `TAKEOFF_WORK=<work>/etapas` cuando takeoff.json vive un nivel arriba. | bitacora.py (markups_fallas) |
| R80e.18 | Walls EXISTING excluidos por decisión del estimador: se sacan del canon, sus tags van a `tags_descartados` con el motivo y la cita (DM legend / key note, legend de la planta, responsibility schedule); todo node que los toca pasa a `free` en el wall nuevo (stud de cierre); sus puertas van a `opening_schedule.none`; en los markups se agregan aparte con Subject "EXISTING - EXCLUDED" (NM `TOX-`, sin contar). Familias opcionales `5/8" gyp board Type X` y `5/8" gyp Type X W.R.` (canon BOARD_FAM "5/8 type X" / "5/8 type X WR", familias.py, plantilla, accesorios BOARD_DRIVER, ALC-07 / ALC-08). El plano manda sobre D1 cuando pide W.R. en TODAS las caras. | canon.py, familias.py, plantilla_excel.py, accesorios.py, alcances.py; scripts/markups_existing.py |
| R80e.19 | Un ceiling suspendido / framed soffit puede declarar `board` (p. ej. "5/8 type X"): canon.py suma su área a esa familia de BOARD_FAM en vez de fijarla en 5/8" regular. ALC-11 acepta Type X. | canon.py, alcances.py |
| R80e.20 | canon.py: sistema de ceiling `usg_grid` (USG drywall suspension del RCP: main tee / cross tee con spacing {value, source}, channel + angle molding = perímetro, hangers en los mains, sin furring / carrying / ceiling track) y `misc_items` ({ref, familia de FAMS, qty, source N/HOJA, op}) para miembros que un detalle dibuja (braces, box beam, joists de un ceiling box). Familias opcionales 8" joist y USG grid (familias.py + plantilla). Un arco con promedio de caras elegido por el estimador escala cuerda y caras juntas (R72.2) con `arc_note`. | canon.py, familias.py, plantilla_excel.py |
| R80e.21 | Imágenes de evidencia: las etiquetas de wall se colocan con `etiquetas.colocar` (anillos x 16 direcciones, primero hacia afuera de la zona densa; sin tocar otra etiqueta ni otra línea marcada; leader line, fondo blanco, borde del color del type); el título y la leyenda son zona reservada con fondo blanco. La etiqueta es el "Wall #" del Excel completo (nunca recortado). Usado por planmark.overview y por el script de imágenes por hoja. Revisar con zoom wall por wall antes de entregar. | etiquetas.py (nuevo), planmark.py |
| R80e.22 | Regex N/HOJA de chequeos_v77.py y accesorios.py aceptan hojas con guion (I/A-221, 11/A-200): `[0-9A-Z]{1,2}/[A-Z]{1,2}-?\d`. Mismo error que R80e.13 en otras tools: toda regex de cita nueva se prueba con una hoja con guion. | chequeos_v77.py, accesorios.py |
| R80e.23 | Cara de remate con tag ("I SIM." en el extremo de un wall): es un renglón del type (su LF = espesor impreso del wall) con acabado SOLO. Se declara como element `pier` con `parts [{stud_size, studs_drawn {value: 0, source}}]` (el framing es el stud de extremo del wall anfitrión), `bottom_track: false`, `top_track: false` + `track_source` N/HOJA, `bracing_rows: 0` + `bracing_rows_source`, `type_lf_basis`, `jamb_strips_none_reason`. canon.py pasa estas claves a corridas; corridas, reglas (E10, §7, A13) y accesorios (slab pins) respetan la ausencia declarada. Nunca descartar un tag "SIM." como "solo acabado": lleva su acabado en el take-off. | canon.py, corridas.py, reglas.py, accesorios.py |
| R80e.24 | Trazabilidad del Excel (auditoría final B&N rev4, chequeos 5 y 6): `trazabilidad.py`, llamado por plantilla_excel.armar, escribe en "Where it comes from" la N/HOJA de cada renglón (nunca nombres de archivos internos .json / .py) y el `Breakdown [DERIVED]` por wall / elemento que suma el NET (studs por tamaño, track por tamaño, bracing, ceiling track, board por tipo, cement board, FRT plywood por espesor, blocking, trim, hangers, furring, carrying); si el desglose no suma el NET, no se arma. Los renglones en 0 dicen por qué, con su hoja (accesorios_none / accesorios_rfi del canon). En el Partition Takeoff, toda fila con Board (SF) != L x H x Layers lleva en Location "Board by face: lado room largo x alto (board)". | trazabilidad.py (nuevo), plantilla_excel.py |
| R80e.25 | Lecciones del auditor final (B&N rev4), reglas de barrido: (a) una partition note que dice "FOR WALL AND CEILING CONSTRUCTION" pone W.R. también en los GWB ceilings de esos rooms; (b) la nota "*" de A-410 que nombra KITCHEN y 2/A-410 "RESTROOM/CAFE WALLS" ponen W.R. en las caras del Cafe Work Room; (c) un detalle típico con "TYP." (8/A-410 "METAL STUD/TRACK FIRE STOP AT CEILING LINE, TYP.") aplica a todo wall a deck con ceiling en una cara: se cuantifica (LF por wall y tamaño) + RFI de confirmación; (d) una cota "HOLD" en la planta + la altura del RCP + la sección del soffit definen el soffit: nunca "not priced"; lo no impreso (T.O. WD-1) = RFI con supuesto conservador; (e) un área rotulada en una planta ampliada ("AREA OF 3/4\" FIRE RESISTANT PLYWOOD") entra como plywood (SF) en la cota superior + RFI de extensión; (f) un criterio por defecto del skill (constants de accesorios.py) nunca se cita como nota impresa: su source dice "not printed / skill default" y va a RFI; (g) el desglose de cada material permite al auditor reproducir el NET (R80e.24). | build (lectura), excel_json, accesorios.py |
| R80e.26 | Capas por cara en una sección de wall (error B&N rev0-rev5, G/A-221): las capas se cuentan en el DIBUJO, lado por lado (relleno punteado = gypsum board, rayado cruzado = plywood), y cada leader se sigue hasta la capa que toca (un leader puede cruzar el stud hasta el otro lado). Una nota "X = A, B" con dos flechas es una capa por lado, no las dos capas en cada lado. Una nota de W.R. ("*", "WET SIDE(S)") solo cambia gypsum board que exista en esa cara: si la cara es plywood + FRP no hay W.R. que cargar. Antes de cambiar el board de una cara, abrir la sección del type y confirmar que esa cara lleva gypsum. | build (lectura), canon faces / plywood_strips |

### R80e.30 — Gasto de tokens (usuario 27-oct, todos los proyectos)
Nunca repetir trabajo sin provecho. Pasos 11/12: una pasada completa por revisión; los hallazgos se corrigen y se verifican SOLO los ítems cambiados (revisión dirigida), no otra pasada completa. No releer ni recalcular lo que está en caché. Reportes cortos.

### R80e.33 — Código del trade cuando el plano no responde (usuario 27-oct, REGLA INVIOLABLE, todos los proyectos)
ORDEN DE FUENTES: 1) planos, 2) spec sheets — si plano y spec difieren pero pueden convivir, se aplican LAS DOS, cada una en su alcance (B&N: corner guards C22 stainless 48" en stock room + spec A-001A 2x2x72 en el resto); 3) solo si no encuentran nada, el código. Si el plano y la spec no dan la respuesta: aplicar SIEMPRE el código/norma del trade (drywall ASTM C840 / GA-216 / UL; metal frame AISI S220/S240, ASTM C754, fabricante; IBC/ASCE 7 sísmico; NFPA/UL firestop). Se carga con cita del código; RFI solo si el código no lo cubre o hay conflicto. Al cerrar la revisión de RFI de un proyecto, cada decisión del estimador pasa a regla general del skill.
