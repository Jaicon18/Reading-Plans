# ADENDA v40 — 7-oct-2026 · LA REGLA DEL INGLÉS SE VERIFICA, NO SE PROMETE

## ⛔ LO QUE PASÓ, y por eso existe esta adenda

La adenda v39 escribió la regla inviolable: el vocabulario del trade va en inglés en **todas**
las respuestas. Ese mismo día la incumplí. Rodolfo preguntó *"¿seguiste la regla del inglés?"*
y la respuesta honesta era **no**:

<!-- GLOSARIO:INICIO -->
| escribí | debía escribir |
|---|---|
| la **cota** impresa | the printed **dimension** |
| los extremos del **muro** | los extremos del **wall** |
| la **puerta** 118A | el **door** 118A |
| **hoja** de 3'-0" | **leaf** de 3'-0" |
| **abisagrada** en la jamb este | **hinged** en la jamb este |
| el **arco de giro** | el **swing** |
| **partidas** DERIVADO sin cita | **line items** DERIVADO sin cita |
<!-- GLOSARIO:FIN -->

### El motivo de la falla, que es lo único que importa

> **Todas las compuertas del proyecto revisan el ENTREGABLE. Mi prosa del chat no pasaba por
> ninguna.** Era la única salida del proyecto sin compuerta, y fue la que falló.
>
> **Una regla que depende de que yo me acuerde no es una regla: es una intención.**

---

## LA COMPUERTA: `verif_respuesta.py`

**El procedimiento es la regla, no una sugerencia:**

1. La respuesta se **escribe a un archivo** antes de mandarla.
2. Se corre `python3 verif_respuesta.py <archivo>`.
3. Si marca algo, se corrige **en el archivo** y se vuelve a correr.
4. **Sólo cuando pasa limpia se manda.**

Ninguna compuerta puede leer lo que escribo directo en el chat, así que el paso que la hace
posible es el 1: pasar por un archivo. Ese rodeo es el precio de poder verificar, y es el mismo
trato que ya tiene todo lo demás — ningún número se entrega sin sello, ninguna respuesta se
manda sin revisar.

Probada viéndola fallar sobre **mi propio texto**, no sobre un caso inventado: le di la
respuesta que mandé y cazó los seis términos. `test_verif_respuesta.py` los fija como casos
permanentes (15 comprobaciones).

---

## POR QUÉ HACEN FALTA DOS LISTAS, Y NO UNA

Fue el impulso equivocado y hay que dejarlo escrito para no repetirlo:

| | `glosario.py` | `vocab_trade.py` |
|---|---|---|
| **qué revisa** | el DATO: texto dentro del cierre sellado → Excel | la PROSA: chat, documentos, literales de los generadores |
| **ejemplos** | board, stud, track, joint compound, corner bead | wall, door, dimension, line item, swing, hinged |
| **por qué no se fusionan** | — | `muro`, `largo`, `partidas` y `puerta` son **CLAVES del cierre** (<n>, <n> y <n> veces) y `puerta` es un **VALOR que gobierna la lógica** (`clase: puerta` decide si la abertura lleva sólo header o header **y** sill) |

Meterlas en una sola habría **roto la lógica del cierre para arreglar la redacción del chat**.
Es el mismo criterio que ya tenía `dataset.CLASE_EN`: se traduce la salida, nunca el dato.

---

## LOS FALSOS AMIGOS QUE SALIERON AL CORRERLO SOBRE EL TEXTO DE VERDAD

Ninguno se encuentra pensando; todos salieron de aplicar la lista a los 63 documentos:

<!-- GLOSARIO:INICIO -->
- **`puerta de salida / de entrada / de cierre / de idioma`** → es la **compuerta**, no un door.
  En este proyecto `puerta de <algo>` es siempre la metáfora; el door de verdad se escribe con
  su tag (`la puerta 118A`) o con su medida. Se protege la frase, no la palabra.
- **`a lo largo de`** → es *along*, no la medida. Y **`más largo / tan largo / muy largo`** es el
  **adjetivo**: "el colgante más largo" no es "el colgante más length".
- **`cara a cara`** → `face to face`, como frase: traducir palabra por palabra daba "face a face".
- **`hoja`** → es *sheet* (hoja de plano) **y** *leaf* (hoja de puerta) a la vez, y aparece 31
  veces como clave y 31 en nombres de archivo. **Sólo entra como frase.**
<!-- GLOSARIO:FIN -->

> **REGLA:** entra a la lista la palabra que en este trade **sólo** puede nombrar la pieza; la
> que fuera del trade significa otra cosa entra **como frase**, con su excepción declarada. Una
> compuerta que estropea el texto que revisa se acaba apagando.

### Y una corrección a mí mismo, el mismo día

Dejé `largo` y `cara` fuera de la lista "porque son claves del cierre". **Eso era confundir las
dos listas:** `vocab_trade` no toca el dato, toca la prosa — las claves son claves JSON y nunca
pasan por ahí. Se vio al traducir el SKILL, que salía con **"width × length"** y **"una layer por
face"**: media medida en cada idioma, que se lee peor que no traducir nada.

---

## ALCANCE: también el generador, no sólo la salida

`traducir_docs.py` y `traducir_generadores.py` aplican ahora **las dos listas**. 772 literales en
28 generadores. Es la regla de la v39 aplicada un nivel más arriba: **traducir la salida deja el
arreglo colgando del siguiente `python cerrar_*.py`.**

## TERCER TRINQUETE

Al vocabulario del trade se le pone su propio contador, visible y aparte, **que sólo baja**:
**35** términos en documentos (casi todos dentro de bloques de código citados, que el corrector
no toca a propósito) y **290** celdas del libro (la hoja de evidencia cita el texto sellado, y
ese atraso se paga traduciendo el **generador**).

Los otros dos trinquetes bajaron en la misma pasada: libro **<n> → <n>**, evidencia
**970 → 964**.

**Estado: 16/16 compuertas pasan · 88 sellos OK / 0 rotos · 0 nombres de material en español en
los archivos finales.**

---
