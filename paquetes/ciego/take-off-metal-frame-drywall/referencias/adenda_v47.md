# ADENDA v<n> — <n>-oct-<n>

## Lo que se corrigió, y por qué importa

Al subir la carpeta a la PC se metió `SKILL_take-off_VIGENTE.md` a la carpeta de entrega
—donde nunca había estado— y la compuerta de idioma pasó de **<n> a <n>** términos del trade
en español. Al abrir los <n> uno por uno, **<n> de ellos eran CÓDIGO**:

(ejemplo de una corrida retirado del paquete ciego)

y un árbol de chain of details. `capas_cara` y `largo_muro` no son prosa: son los **nombres
de campo del cierre sellado**. Traducirlos para contentar a la compuerta habría dejado la
formula escrita mitad en un idioma y mitad en otro —`layers = Σ(capas_cara × …)`— y, peor,
habría roto la correspondencia con el campo que el closer realmente escribe.

## REGLA 47.1 — UNA COMPUERTA QUE CUENTA POR RENGLÓN NO PUEDE VER LA CERCA

> Un bloque cercado (```) solo se reconoce con el documento **completo** a la vista. Una
> función que recibe UNA línea a la vez alcanza a ver los backticks de `inline code` y nada
> más: para ella la línea de adentro de un bloque cercado es prosa.

Las tres compuertas que cuentan por renglón —`revisar_docs` (nombre de material),
`vocab_pendiente` (vocabulario del trade) y `handoff_pendiente`— llamaban
`faltas(linea)`, una línea cada vez. Las tres contaban código como prosa.

**Solución:** el código se quita en **un solo lugar**, `_fuera_del_glosario`, que ya recibe
el documento completo porque tiene que encontrar los marcadores
`<!-- GLOSARIO:INICIO/FIN -->`. Ahora devuelve la línea **ya sin código**, usando
`vocab_trade.lineas_sin_codigo` —el único normalizador del proyecto, que conserva la
numeración—. Las tres compuertas heredan el arreglo sin tocarlas.

**Es el mismo defecto de siempre, en otro nivel:** cuando el detector y el corrector no
normalizan igual, la falta se reporta para siempre y nunca se arregla. Ya costó una entrega
con `perfileria`; aquí habría costado una fórmula corrompida.

## El test, y la prueba de que falla sin el arreglo

Dos casos nuevos en `test_verif_idioma.py`, y uno más para la otra cuenta:


El tercero está ahí por un motivo: una cerca que se abre y no se cierra eximiría el resto
del documento entero. Se probó que se cierra.

## El caso que casi quedó decorativo (y cómo se cazó)

La primera versión del test usaba la palabra `capas` contra `revisar_docs`. Pasó de
inmediato… porque `revisar_docs` usa el diccionario de **nombres de material**, donde
`capas` no está. **Un test escrito con una palabra que el detector ignora pasa siempre y no
prueba nada** — exactamente la compuerta decorativa del 10-oct-2026
(`verif_blocking_schedule` v1). Se reescribió con `tablero`, que ya está probado arriba en
el mismo archivo como término que la compuerta SÍ caza en prosa, y entonces el caso
empezó a tener valor.

> **REGLA 47.2 — Un caso de prueba se escribe con un dato que el detector YA demostró
> cazar en el camino normal. Si no, el test prueba el diccionario, no la compuerta.**

## Lo que se pagó, no lo que se eximió

El archivo **no se eximió**. De los <n> términos del SKILL, <n> eran código (los quita el
arreglo) y **<n> eran prosa de verdad**: se tradujeron uno por uno. La cuenta de documentos
volvió a **<n> = el tope**, así que el trinquete no subió ni un punto para dejar entrar el
archivo nuevo.

Un término más: `**El bloqueo se levantó**` en el relato del mapa de adyacencia. Ahí
`bloqueo` quería decir *impedimento*, no `blocking`, y la compuerta no tiene cómo saberlo.
Se reescribió como `impedimento`: cuando una palabra en prosa colisiona con un nombre de
material, se cambia **la prosa**, no la compuerta.

## Estado de la entrega

23/23 compuertas en verde. <n> cierres VIGENTES en <n> archivos, <n> elementos sellados,
<n> sellos roto, <n> de <n> detalles del set revisados. Carpeta de la PC sincronizada:
<n> xlsx + <n> marked plans + <n> documentos + <n> scripts.

---
