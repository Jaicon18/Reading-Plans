# ADENDA v35 — 1-oct-2026 (noche)

## El índice se genera, no se escribe (`hoja_indice.py`)

`00_INDICE_DE_ARCHIVOS.md` estaba escrito a mano y mentía en cinco cosas a la vez: 77
elementos cuando eran 78, 58 scripts cuando eran 72, "los seis pasos" cuando ya eran diez,
"la carta de RFIs todavía no existe" cuando ya existía, y seguía pidiendo borrar un plano
ya borrado. Es el documento que se abre PRIMERO: si miente el índice, no sirve nada de lo
que apunta.

Ahora lo genera `hoja_indice.py` — último paso antes de la compuerta de idioma — contando
la carpeta con el sistema de archivos y leyendo el estado de los sellos y del libro.

**`entregar.py` pasa a 10 pasos** y sincroniza los scripts él mismo: sellos → planos
marcados → regenera el Excel → vigencia → estado → carta de RFIs → cobertura de detalles →
copia (libro + manifiesto + 73 scripts) → índice → idioma. El índice va DESPUÉS de la copia
(cuenta la carpeta ya poblada); el idioma va al final (revisa todo lo recién escrito).

Un número cuyo script no viajó con el entregable no se puede volver a producir, así que no
está entregado. Por eso la sincronización es un paso de la compuerta, no un acto manual.

## Tres reglas nuevas, cada una de un error cometido hoy

### 1. Una exclusión por NOMBRE EXACTO se rompe con un rename

`verif_idioma.HISTORICOS` era un dict de nombres exactos. Renombrar `adenda_v27.md` a
`adenda_v27_2026-09-28.md` la volvió a meter a la compuerta y paró la entrega. Se excluye
por CATEGORÍA — `^(SKILL_take-off_v\d+|adenda_v\d+)` — que es lo que el archivo ES: una
versión congelada existe para registrar qué decía el texto ESE día, así que reescribirla
destruye justo lo que vino a guardar.

Misma familia que `'net' in txt` casando con "cabinet" y que parsear la salida de otra
herramienta por posición en vez de por contenido: **nunca identifiques algo por su forma
superficial.** Probado en los dos sentidos: la categoría reconoce el archivo con y sin
fecha en el nombre, y la compuerta sigue cazando una falta real en un archivo vivo.

### 2. No reimplementes un conteo o un lector que ya tiene dueño — PREGÚNTALE

Dos veces en el mismo turno:

| lo que hice | qué dio | quién era el dueño |
|---|---|---|
| conté los sellos adivinando la llave (`_sello`) | **0** | `resumen_total.py` |
| leí Pending Items buscando la columna por nombre | **18 renglones vacíos** | `hoja_rfi.leer_pendientes` |

La hoja de pendientes va por POSICIÓN, no por encabezado. Las dos veces el dueño existía y
las dos veces la segunda implementación dijo otra cosa — que es exactamente el motivo por
el que existe `verif_planos`. Se le pregunta al dueño y su salida se lee **por contenido**.

Y un renglón vacío en el índice es peor que ninguno: parece que el pendiente existe y no
dice cuál.

### 3. Un `.get(llave, default)` sobre un archivo propio esconde el error de tecleo

`mani.get('insumos', {})` dio 0 sin que nada se quejara. La llave era `fuentes`. En un
archivo que yo mismo escribo, la llave se EXIGE y revienta si no está.

## La carpeta de entrega es el espejo, y tiene que estar completa

El índice cuenta la carpeta de entrega, así que un archivo que vive solo en la PC y no en
el espejo hace que el índice subcuente: faltaban `SKILL_take-off_v25`,
`BOA_CIELOS_GWB_cerrado.md` y `BOA_correccion_planos_marcados.md` — 22 contra 25 reales.

Se traen de vuelta con `device_stage_files` desde su PC, nunca se reescriben de memoria.
Al traerlos, la compuerta de idioma cazó dos nombres en español (los términos exactos van
entre marcadores de glosario abajo, porque citarlos es justo lo que la compuerta prohíbe):
<!-- GLOSARIO:INICIO -->
`sellador` y `envolvente de columna`.
<!-- GLOSARIO:FIN -->
documentos escritos antes de que existiera el glosario, y que seguían en español en su PC.
Se traducen con `G.traducir()` comprobando que ningún número se mueva — 154 y 194 números
intactos — y se vuelven a escribir allá.

## Sin shell en su PC, el diff se hace por TAMAÑO

No hay `device_bash` en esta sesión, así que no se pueden comparar hashes allá. Se comparan
los tamaños que da `device_list_dir` contra los locales: de 73 scripts solo **6** diferían.
Y el JSON de los commits se escribe a un archivo, no se imprime: volcar los 73 a la
terminal gasta ~15 KB de contexto para nada.

---
