# ADENDA v<n> — <n>-oct-<n> · UNA ELEVACIÓN NO ES UNA HEIGHT, Y UN `[CONFIRMADO]` TIENE QUE CITAR SU PRINTED DIMENSION

## ⛔ REGLA INVIOLABLE

> **Un `[CONFIRMADO]` tiene que CITAR una printed dimension. Si el texto de su fuente no trae
> ninguna printed dimension, la afirmación no se puede comprobar — y una afirmación que no se puede
> comprobar no es un `[CONFIRMADO]`: es `[DERIVADO]` (y entonces escribe la operación) o
> `[PENDIENTE]`.**

Y la que la destapó:

> **Una ELEVACIÓN no es una HEIGHT.** S2.20 imprime una elevación (`B.O.D. EL. [valor retirado E24]`);
> la height del stud es esa elevación **menos** el datum `T/SLAB 0'-0"`. Que las dos cifras
> coincidan pasa sólo porque el datum vale cero. **Una resta sigue siendo una resta**, así que
> es `[DERIVADO]` y tiene que escribir la cuenta.

## CÓMO SE ENCONTRÓ (armando el HANDOFF, no revisando cantidades)

Rodolfo pidió un handoff completo para continuar el take-off en otra sesión. Un handoff obliga
a mirar la **etiqueta** de cada dato en vez de la cantidad, y ahí salió: el mismo `[valor retirado E24]`
sacado del mismo `B.O.D.` de S2.20 estaba sellado `[CONFIRMADO]` en [valor retirado E24] walls y `[DERIVADO]` en
[valor retirado E24]. El culpable era una línea de `cerrar_A<n>K.py` que etiquetaba **por el valor**:

<!-- GLOSARIO:INICIO -->
(ejemplo de una corrida retirado del paquete ciego)
<!-- GLOSARIO:FIN -->

o sea "si vale [valor retirado E24] es CONFIRMADO". **La etiqueta describe cómo se obtuvo el número, nunca
cuánto vale.**

## POR QUÉ `verif_confirmado` NO LO CAZABA — el hueco más grande que tuvo esa compuerta

La compuerta preguntaba *"¿este `[CONFIRMADO]` vale exactamente la printed dimension que cita?"* y
hacía `if cs and not any(...)`: **si el texto no traía NINGUNA printed dimension, no revisaba nada y el campo
pasaba en silencio.** Medido el día que se encontró:


Verificaba <n> de <n> y su "OK" era casi vacío. El atraso queda como **trinquete declarado en <n>,
que sólo baja**, impreso en cada run: no se bloquea la entrega por una deuda que ya venía,
pero se paga **arreglando el generador**, nunca la salida.

## LA COMPUERTA NUEVA: `verif_coherencia.py`

Distinguir una elevación de una height caso por caso es difícil de revisar, así que la compuerta
no lo juzga — exige **coherencia**:

> **El mismo valor citando la misma hoja no puede llevar dos etiquetas en dos cierres. Si las
> lleva, una de las dos está mal y hay que ir al plano, no elegir la cómoda.**

Es la versión de compuerta de la regla que ya había cazado los ocho `alto_board` del A5 ("dos
tipos con dos etiquetas distintas para la misma cuenta"). Probada **viéndola fallar sobre el dato
real**: se revirtió el sello del A<n>K #n a `CONFIRMADO`, la compuerta lo marcó, y se restauró.
Trinquete declarado en <n>.

Lo que sigue abierto, y va al handoff como pendiente numerado: **<n> `alto_board` citan
`5/A12.01 PARTITION G` para el valor [valor retirado E24], y ese detalle no imprime ese número** — da la REGLA
("to underside of structure"); el valor sale de S2.20. Un número correcto con la fuente
equivocada es el mismo error de `<n>/F de S5.20`.

## UNA NORMALIZACIÓN DUPLICADA SE DESINCRONIZA SOLA

Al pasar el registro de los walls A1 #n/#<n>/#<n> por `verif_respuesta.py` se marcó por `caras` y
`largo` **entre acentos graves** — nombres de CAMPO del cierre. El mismo texto **pasaba** la
compuerta de documentos y **fallaba** la de prosa: había **tres** normalizaciones distintas del
código (`traducir_docs.py` saltaba bloque cercado e `inline code`, `verif_idioma.py` sólo
`inline code` con su propia copia de la regexp, `verif_respuesta.py` ninguna).

> **REGLA: la normalización vive en UN lugar.** `vocab_trade.sin_codigo` y su variante por
> renglón `lineas_sin_codigo`, y `faltas()` la aplica de oficio, así que toda compuerta que la
> llame queda alineada sin acordarse de nada. Es la misma regla que ya regía para el detector de
> documentos congelados, aplicada a los acentos graves.

Los <n> casos nuevos de `test_verif_respuesta.py` (<n> en total) fijan los dos que **no** debe cazar
y los dos que **sí**, con código al lado — una compuerta que se afloja para dejar pasar el código
deja de servir.

## EL MAPA DE HOJAS SE CRUZA CON DOS FUENTES, Y SE DICE DÓNDE NO CUADRAN

El PASO 0 se volvió herramienta (`indice_set.py`), con las dos fuentes que manda el protocolo:
el **DRAWING INDEX de A00.<n>** (<n> hojas) y el **title block de cada página** (<n> páginas).

- **El número de hoja del title block es el texto MÁS GRANDE que tiene su forma** (~<n> pt). El
  detector anterior dejaba <n> de <n> páginas sin número y en A03.<n> tomaba texto de la PLANTA
  como título. Ordenar por tamaño de letra lo resuelve sin depender de en qué esquina esté.
- **El set trae `A02.<n> ROOF PLAN` TRES veces** (páginas <n>, <n> y <n>), verificado página por
  página contra el PDF. Y eso cuadra la aritmética: **<n> hojas del índice + <n> copias = <n>
  páginas.** No falta ninguna hoja del índice y no hay ninguna que el índice no liste.
- Las **<n> páginas sin rótulo legible** son las **<n> hojas civiles y de landscape** (C1.0–C7.4,
  L1.0, L1.1): el title block del consultor civil tiene otro formato. Se asignan **`[DERIVADO]`
  por posición** con la cuenta escrita, nunca `[CONFIRMADO]`, y se dice por qué la
  incertidumbre no cuesta: son Div 02/31/<n>, fuera de Div <n> y Div <n>.
- **Revision log leído, <n> revisiones; la vigente es `IF Permit · 08/26/<n>`.** La carta de RFIs
  traía `<n> hojas` escrito a mano: son **<n> páginas / <n> hojas**. Un número escrito a mano que
  nadie volvió a comprobar.

## EL REGISTRO DE LO QUE EL USUARIO CONFIRMÓ NO EXISTÍA COMO ARCHIVO

La regla del 12-sep-2026 manda parar al cerrar el barrido de cada tag y esperar confirmación
explícita. Ese registro vivía en el chat.

> **REGLA: lo que el usuario confirmó se guarda como DATO, igual que una printed dimension.** Un handoff que
> presente "ubicaciones confirmadas por el usuario" sin tener dónde consta está inventando el
> dato más delicado del documento — el único que no se puede verificar contra el plano. Lo que
> consta se declara con dónde consta; lo demás sale `[PENDIENTE]`, y se distingue del barrido
> verificado por código, que es otra cosa.
