# Herramientas v61 candidatas (2026-10-16)

Cinco herramientas deterministas para el skill take-off metal frame / drywall. Implementan las reglas 60.3–60.10 de ADENDA_v60 / ARBITRAJE_10.
Son **genéricas**: no llevan datos de ningún proyecto. Los tests usan datos inventados.

Se usan igual que `studs_nodos.py` y `board_caras.py`. **El agente solo declara datos leídos del plano. La tool hace el cálculo.**

## Contrato común (las 5)

- **Uso:** `python3 <tool>.py <entrada.json> <salida.json>`. Solo stdlib.
- **Códigos de salida:**
  - rc 0 = OK. Escribe la salida y muestra los totales en stdout.
  - rc 1 = la entrada viola el contrato. Muestra `ERROR <tool>: <motivo>` en stderr y **no escribe la salida**.
  - rc 2 = uso incorrecto.
- **`source`:** todo renglón lleva `source` con forma N/HOJA. Ejemplos: `6/A12.01`, `D/A9.22`, `F/1/S5.20`, o la hoja sola (`E00.01`). Se aceptan varias fuentes separadas por `,` `;` o `·`. Si falta o está mal → rc 1. La salida copia la `source` tal como vino.
- **Formato de la salida:** totales por familia, más un renglón por elemento con `source` y `operacion` (la fórmula escrita con sus números).
- **Repetidos:** un id o elemento repetido → rc 1. Cada cosa se cuenta una vez.

## 1. headers.py — reglas 60.5 y 60.10

**Entrada:**
- `openings[]`:
  - `ref`, `wall`
  - `kind`: door | window | storefront | opening | duct | recessed_accessory
  - `location`
  - `ro_w_ft`
  - `qty` (entero, aberturas iguales)
  - `with_sill`
  - `header_type` + `header_type_source` (opcionales)
  - `source`
- `header_schedule{source, rows[{max_span_ft, type}]}` — opcional
- `stud_bay_in` — default 14.375; si se cambia, exige `stud_bay_source`

**Fórmula:**
- header LF = (R.O. + 1'-4") × 1 × qty
- sill track LF = (R.O. + 1'-4") × qty, solo si `with_sill`

**Tipo de header:**
- Sale de `header_type` o de la primera fila del schedule con `max_span_ft` ≥ R.O.
- **Va solo en la descripción.**
- Si no hay tipo → `TYPE PENDING` + RFI en `avisos`. El LF no cambia.

**Rechazos (rc 1):**
- Campo `members`, `multiplier`, `plies` o `x_members` (los members no multiplican el LF).
- `kind` = `recessed_accessory` (va a framed_openings.py).

**60.10:** si R.O. ≤ stud bay → `FITS_MODULE`, 0 LF.

**Salida:** `totales_lf{header, sill track}`, `renglones[]`, `avisos[]`.

## 2. corridas.py — reglas 60.6, 60.7, 60.8 y 53.4

**Entrada:**
- `runs[]`:
  - `id`, `element`
  - `orientation`: vertical | horizontal
  - `length_ft`
  - `height_ft` (en vertical)
  - `rows`
  - `track_lines` (solo en horizontal)
  - `bottom_track` / `top_track` + `track_source`
  - `bracing_rows` + `bracing_rows_source` (opcional)
  - `source`
- `bracing{spacing_in, source}`
- `section_details[{source, runs}]`

**Elementos permitidos por orientación (60.8):**
- Solo vertical: wall, parapet, column_wrap, canopy_framing, vestibule_head, grille_head, grille_box, door_bulkhead, soffit_drop, chase.
- Solo horizontal: ceiling, soffit_bottom, joist, fascia_box, canopy_soffit.
- Los dos: bulkhead, other.
- Un elemento con la orientación equivocada → rc 1.

**Fórmulas:**
- Vertical:
  - bottom/top track = L × rows × 2
  - bracing rows = `bracing_rows` declarado, o si no ROUNDUP(H × 12 / spacing_in) − 1, mínimo 0
  - bracing C.R. channel = bracing rows × L × rows
- Horizontal:
  - ceiling/soffit track = L × track_lines
  - sin bracing

**60.6:** el número de corridas que citan un `section_details.source` debe ser igual a `runs`. Si no → rc 1.

**60.7:** una corrida vertical sin `bracing.spacing_in` y sin `bracing_rows` con fuente → rc 1. Así, ninguna corrida queda sin bracing por olvido.

**Salida:** `totales_lf{bottom/top track, ceiling/soffit track, bracing C.R. channel}`, `renglones[]`.

## 3. altura_stud.py — reglas 60.3 y 59.13

**Formato de los números:** todo número va como `{"value", "source"}`. Si no → rc 1.

**Entrada:**
- `bod_table{source, points[{y_ft, bod_ft}]}`
- `beams{nombre: {d_in{value, source}}}`. La fuente del peralte puede ser texto libre, por ejemplo `AISC W12X26`.
- `walls[]`:
  - `id`
  - `type`: exterior | interior
  - `y_ft`, y opcional `y_to_ft` (wall con pendiente), **o** `bod_ft`
  - `stops_under_beam{value: bool, source}` — obligatorio en exterior
  - `beam`

**Fórmula:**
- B.O.D.(y) = interpolación lineal en la tabla. No extrapola.
- H = B.O.D. − d/12, si `stops_under_beam`.
- H = B.O.D., si no.
- Wall con pendiente: `height_ft` = lado alto (53.2) y `height_avg_ft` = promedio.

**Salida:** `resumen_por_tipo{exterior|interior: walls, min_ft, max_ft}`, `renglones[]` (con todas las fuentes usadas). El `height_ft` de la salida es el que se le pasa a studs_nodos.py.

## 4. framed_openings.py — reglas 60.9, 60.10 y 58.4

**Entrada:**
- `modules`:
  - `wall_stud_bay_in` — default 14.375
  - `ceiling_furring_oc_in{value, source}` — obligatorio si hay items de ceiling
- `items[]`:
  - `tag`, `category`
  - `location`: ceiling | wall
  - `shape`: rect | round
  - `qty`
  - `width_in`
  - `length_ft{desc, catalog, drawn}`
  - `length_override{value, source, rfi}`
  - `source`

**Largo (60.9):**
- Si desc ≠ catalog, se carga el que coincide con drawn.
- Se agrega un RFI con delta = 2 × (otro − cargado) × qty.
- Si el dibujo no lo resuelve → rc 1, salvo que venga `length_override` con fuente y texto de RFI.

**Módulo (60.10):** si max(ancho, largo) ≤ módulo → `FITS_MODULE`, 0 LF.

**Wall que no cabe en el stud bay:** queda en `TO_HEADER_SILL` (58.4) con 0 LF aquí, y aparece en la lista `to_header_sill` para pasarla a headers.py.

**Fórmula:**
- rect: LF = 2 × (L + W) × qty
- round: LF = 4 × d × qty

**Salida:** `totales_lf{framed openings MEP}`, `renglones[]`, `rfis[]`, `to_header_sill[]`.

## 5. alcance_filtro.py — regla 60.4

**Entrada:**
- `rows[]`:
  - `id`, `family`, `description`, `qty`, `unit`, `source`
  - `substrate_of` (drywall | cladding) + `substrate_source` — opcionales

**Clasificación:**
- **Siempre cladding:** Z-girt, girt, lath. Va a EXCLUDED.
- **Cladding por contexto:** hat channel / furring / channel + metal panel / ACM / stucco / EIFS / EPS-n / cladding / rainscreen / siding / fiber cement. Va a EXCLUDED.
- **hat channel sin contexto:** rc 1. El agente tiene que declarar `substrate_of` con fuente, porque el furring channel 7/8" de drywall también es un hat channel.
- **Declaración que contradice:** `substrate_of: drywall` en un Z-girt o lath → rc 1.

**EXCLUDED:**
- La qty sale de los totales de su familia, así que nunca queda en furring channel.
- Lleva un RFI en inglés con delta = qty.

**Salida:** `totales_incluidos{"family [unit]"}`, `excluidos[]`, `rfis[]`, `renglones[]`.

## Resultado de tests (2026-10-16)

| Tool | Tests | Resultado |
|---|---|---|
| headers.py | 12 | OK |
| corridas.py | 13 | OK |
| altura_stud.py | 11 | OK |
| framed_openings.py | 11 | OK |
| alcance_filtro.py | 8 | OK |

**Total: 55/55 OK.** El detalle está en `tests.log`.

**Cómo prueban los tests:**
- Cada suite tiene casos con datos buenos, casos de borde y casos con datos malos.
- Casos de borde: R.O. exactamente igual al stud bay, H múltiplo exacto de 48", y y en el extremo de la tabla.
- Los casos con datos malos tienen que dar ValueError y rc ≠ 0 por CLI.

**Mutaciones (`mutaciones.log`):** rompí cada regla clave de cada tool y la suite falló las 10 veces de 10:
- header × 2 members
- sin 60.10
- sin 60.6
- bracing sin el −1
- sin 60.8
- stud a B.O.D.
- exterior sin declarar viga
- framed sin 60.10
- framed carga el catálogo
- cladding sin contexto

## Puntos de ARBITRAJE_10 que no son fórmula exacta

1. **Purlin "0.75 × L si track paralelo al flute"** (tabla de herramientas, corridas.py). Ni ARBITRAJE_10 ni la adenda definen de dónde sale el 0.75, en qué unidad está, ni a qué familia va. **No se implementó.** Hace falta que lo defina la regla.
2. **"bottom+top = L × rows".** Se tomó así: cada corrida lleva bottom **y** top, y cada uno vale L × rows, o sea 2 × L × rows (60.6: "cada una lleva su bottom y top track"). Si la referencia quería decir L × rows en total, el número de la familia sale a la mitad. Hay que confirmarlo con una corrida conocida.
3. **Ceiling/soffit track de framing horizontal.** El ARBITRAJE no da fórmula. La tool exige `track_lines`, declarado por el agente con su fuente.
4. **53.4 bracing.** Se usó la fórmula de la tabla del ARBITRAJE: ROUNDUP(H/4) − 1. El espaciado (48") no se fija en la tool: viene de `bracing.spacing_in` con su fuente, porque cambia según el proyecto. La adenda no trae un umbral aparte para el "parapet ≥ 4 ft": con H = 4 ft la fórmula ya da 0 rows.
5. **60.10 en ceiling.** "Cabe en el módulo" se tomó como max(largo, ancho) ≤ espaciado del furring. Por eso un slot largo y angosto sí lleva framed opening. Esto coincide con el veredicto del arbitraje: slots contados, downlights de 3.5" no.

## v72b — compuerta de reglas inviolables

`reglas.py compuerta <work_dir> [--excel <final.xlsx>]` revisa TODAS las reglas del skill (catálogo de
`reglas_catalogo.py`, tipo en `reglas_clasificacion.py`). `plantilla_excel.py armar` la corre y no escribe el Excel
sin OK; `etapas.py compuerta` y `bitacora.py compuerta` también. Tests: `test_reglas.py` (un test por regla),
`test_ciego_tools.py` (E24 en las tools). `fixture_reglas.py` = proyecto sintético mínimo que pasa la compuerta.
