# Etapas 1 y 3 — inventario por script y doble lectura comparada

Herramientas nuevas, aparte de las tools v68 (no las modifican). Python 3 + pymupdf (+ numpy).
Son GENÉRICAS: ningún tag, hoja, coordenada ni nombre de proyecto vive en el código; todo sale del PDF.

## Por qué

En pruebas ciegas la misma versión del skill dio resultados distintos entre corridas (partition types con
conteos de walls distintos para el mismo type). La causa: el inventario de tags y la partición de walls
los hacía el modelo a ojo. Estas herramientas sacan esa parte del ojo y hacen visible cualquier diferencia.

## Cadena

```
plano.pdf
   │
   ▼
1. inventario.py plano.pdf inv/            → inv/inventario.json + inventario.md + recortes/
   │   (índice de hojas, types del schedule, cada tag con hoja + coordenadas + PNG circulado y verificado)
   │
   ├──────────────────────────────┐
   ▼                              ▼
2A. lectura A (independiente)   2B. lectura B (independiente)
    takeoff_canon_A.json            takeoff_canon_B.json
   │   (cada lectura parte del MISMO inventario; ninguna ve a la otra)
   └──────────────┬───────────────┘
                  ▼
3. comparar.py canon_A.json canon_B.json inv/inventario.json rev/   → rev/revision.md + revision.json + img/
                  │   (usa particion.py con la misma regla para las dos)
                  ▼
   el estimador resuelve cada renglón de revision.md → UN canon final
                  ▼
4. canon.py takeoff_canon.json out/   (tools v68, sin cambios)
                  ▼
5. plantilla_excel.py → Excel
```

## Qué revisa el estimador (y solo eso)

`revision.md` (en inglés) trae:

1. **Matching walls** — una línea por type: walls que coinciden (|ΔLF| ≤ 2 %), walls y LF de A y de B, y
   cuántos tags encontró el inventario. No hay que revisarlas.
2. **Items to review** — lista numerada, cada uno con hoja y su imagen (A = azul, B = naranja):
   - *LF differs*: mismo wall en las dos lecturas con más de 2 % de diferencia (delta en LF y %).
   - *only in reading A / only in reading B*: un wall que una lectura vio y la otra no.
   - "matched by LF only (no geometry)": el wall no trae `band`; el emparejamiento es más débil.
3. **Alerts** (cruce con el inventario):
   - *TAG SIN WALL*: tag del plano que ninguna lectura tomó → falta un wall.
   - *TYPE NO INVENTARIADO*: una lectura usa un type que no está en el schedule (o el tag está en el plano
     pero no en el schedule → RFI).
   - *WALL SIN TAG EN LA HOJA*: wall de un type en una hoja donde el inventario no encontró ese tag.

En el inventario, además: `inventario.md` → tabla type × hoja, lista numerada de cada tag contado con su
recorte, vista de la hoja con todos los tags circulados y numerados, la lista de **ambiguos (NO contados)** con
su motivo, los tags en símbolo que **no están en el schedule**, y las hojas **NO INVENTARIABLES POR SCRIPT**
(raster). Lo ambiguo nunca se cuenta en silencio: se lista para que el estimador decida.

## Herramientas

| Archivo | Qué hace | Test |
|---|---|---|
| `inventario.py <pdf> <out_dir> [--dpi 150] [--sin-recortes]` | Etapa 1: índice de hojas (title block), types del schedule (títulos "PARTITION TYPE …" + columnas de la hoja de schedule), ocurrencias (partition tags, ambiguos, candidatos fuera de schedule, door / window tags, detail bubbles N/HOJA, referencias N/HOJA en texto, keynotes, cotas), conteo por type y hoja, recorte PNG por ocurrencia con el tag circulado y **verificado al reabrirlo** (anillo rojo en su lugar, tinta del tag en el centro, texto bajo la marca = el tag) y una vista por hoja de planta. Coordenadas en pt de la página ROTADA (como el PNG). Sale con código 1 si algún PNG no verifica. | `test_inventario.py` |
| `particion.py canon.json [--modo run\|tramo] [salida.json]` | Regla de partición de walls como parámetro: **tramo** = un wall por tramo recto (colineales ≤ 3" y contiguos ≤ 6" se unen; jog ≤ 1'-0" se suma al vecino); **run** = un wall por run continuo aunque tenga quiebres (los tramos se encadenan extremo con extremo; una T no encadena). Nunca une hojas ni types distintos. | `test_particion.py` |
| `comparar.py A.json B.json inventario.json out_dir [--modo] [--pdf] [--radio-ft 5]` | Etapa 3 (arriba). | `test_comparar.py` |
| `etapas.py estado\|compuerta <dir>` · `etapas.py unir <carpeta> <canon.json>` (v69) | Dónde quedó la corrida (reanudar); compuerta de etapas (falla si falta inventario / canon A / canon B / revisión, si la revisión está vencida o no cubre el inventario, o si un tag queda sin wall y sin alerta); unión de los fragmentos de una lectura. | `test_etapas.py` |
| `test_ciego_v69.py <SKILL.md\|carpeta>` (v69) | E24 genérico sobre el skill. | autoprueba |

### La regla de partición: una sola constante

`particion.py`: `MODO_DEFAULT = "tramo"`. Mientras el estimador no decida, queda en "tramo". Para cambiarla
se edita esa línea (o se pasa `--modo run` a `particion.py` / `comparar.py`). Las dos lecturas SIEMPRE se
parten con la misma regla dentro de `comparar.py`.

## Campos del canon que usan estas herramientas

Del `takeoff_canon.json` v68, en `walls[]`: `id`, `tag`, `length_ft`, `element` (los no-partition van a
"other framing"), `band {ori, c0, c1, lo, hi}` en pt de la hoja, `constants.plan_scale_pt_per_ft`.
Campos opcionales que conviene escribir en cada lectura:

- `sheet` (sheet number de la planta donde está el wall). Si falta, se toma el primer sheet number de `source`.
- `page` (página del PDF) cuando el set repite un sheet number en varias páginas.
- `tag_ids`: los ids del inventario (`PT0012` …) del tag que la lectura usó para ese wall. Con eso el cruce
  tag ↔ wall es exacto; sin eso se hace por distancia (`--radio-ft`, default 5 ft).

`canon.py` ignora estos campos extra.

## Límites conocidos

- Solo lee texto vectorial. Hojas raster (escaneadas) = "NO INVENTARIABLE POR SCRIPT"; un tag dibujado como
  líneas (texto vectorizado) no se ve.
- El sheet number se busca en el cuadrante inferior derecho; title blocks en otra posición (p. ej. civiles con
  el número vectorizado) quedan "sheet number NO IDENTIFICADO" (se citan por página).
- Types del schedule: hace falta un título "PARTITION [TYPE] …" / "WALL TYPE …" o una hoja de schedule cuyo
  título diga PARTITION / WALL TYPE. Si el schedule es raster o no tiene esos rótulos, no hay types y el
  inventario lo avisa.
- Tags de una sola letra (B, G, F…) se parecen a grid bubbles y letras de sellos: solo cuentan si el tamaño de
  letra y el radio del símbolo coinciden con los tags de varios caracteres de ESA hoja; si no, van a ambiguos.
- Dos tags iguales encimados (dos tags del mismo type a menos de un símbolo) se cuentan los dos y se marcan "SUPERPUESTO":
  ¿duplicado o dos walls? lo decide el estimador.
- Door / window tags, keynotes y cotas son candidatos por patrón (no se cruzan con su schedule salvo doors).
- `comparar.py` empareja por solape de bbox; dos walls distintos del mismo type pegados pueden emparejarse
  cruzados. El delta queda visible en la imagen.
- Sin `band` en un wall: emparejamiento solo por LF (≤ 10 %) y no se puede cruzar contra la posición del tag.
