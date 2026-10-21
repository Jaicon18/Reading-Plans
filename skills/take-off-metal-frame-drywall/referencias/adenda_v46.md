# ADENDA v46 — 11-oct-2026
## La regla de waste, ampliada, y los tres renglones que destapó

Rodolfo, textual:

> *"a todo lo que sea metal sin importar qué tipo, es el 15 %; a todo lo demás es el mismo
> porcentaje que el de drywall or gypsum board"*

---

## REGLA 46.1 — UNA REGLA ESCRITA COMO DOS LISTAS DEJA HUECOS; ESCRITA COMO PARTITION, NO

La regla vieja era **"15 % metal / 6 % board, por tipo"**. Suena igual que la nueva y no lo es:
dos listas sólo cubren lo que alguien se acordó de meter en una lista. La nueva es una
**partition** — *metal* y **todo lo demás** — y no deja hueco posible.

Al aplicarla aparecieron **tres renglones que estaban comprando exactamente su neto**:

| renglón | antes | ahora |
|---|---|---|
| **Blocking FRT / 2X FRT wood** | 748.00 LF, **0 % de waste** | 6 % → compra **792.88 LF** |
| **Acoustical sealant** | 2,652.66 LF, **sin waste** | 6 % → compra **2,811.82 LF** (113 tubos, eran 107) |
| **PVC trim del FRP** | iba **dentro del renglón de metal trim, a 15 %** | renglón propio a **6 %** |

El wood blocking llevaba semanas en **0 esperando su número** — era un PENDIENTE declarado del
libro — justamente porque "no es metal ni board" y la regla vieja no tenía renglón para él.

El sealant era el **único material medido del plano en todo el libro que compraba su neto
exacto**. Es una longitud medida run por run, no un yield, así que entra en "todo lo demás".

El PVC trim estaba escondido dentro del renglón de metal trim tomando 15 %. Hoy son 4.00 LF y la
diferencia son centavos — pero el run del mop sink sigue **PENDIENTE**, y el día que entre, el
error crece solo.

> Mezclar dos clases de waste en un renglón no se ve mientras una de las dos vale casi
> cero. Se separa cuando se descubre, no cuando empieza a costar.

---

## REGLA 46.2 — DOS CELDAS QUE SIGNIFICAN LO MISMO SON DOS FUENTES DE VERDAD

La celda `Inputs!B19` «Wood blocking waste» **se retira** en vez de ponerle 0.06. La clase `W`
(wood) ahora lee la **misma celda** del 6 % que la clase `B` (board).

> Dos celdas que significan lo mismo son dos fuentes de verdad, y así es como los números se
> separan sin que nadie se entere.

Tercera vez de esta misma regla en dos días: `corpus.py` (una segunda lista de globs cuando ya
existía la buena) y la normalización de `vocab_trade` (tres copias de la misma regexp) fueron las
otras dos.

Las dos celdas que quedan en Inputs se llaman ahora por lo que de verdad hacen:

- **`Waste - ALL METAL, any type`** = 15 %
- **`Waste - EVERYTHING THAT IS NOT METAL`** = 6 %

---

## Lo que NO lleva waste, y por qué — explícito para no volver a preguntarlo

| renglón | motivo |
|---|---|
| Stud reinforcement at MEP penetrations · 3-5/8" stud del CSR soffit | van en **piezas sin length**: son PENDIENTE, y un PENDIENTE no recibe waste |
| Access panel 2'x2' | **pieza contada**, no material a granel |
| Power-driven fasteners and duct sleeves | van **por caja** |
| Drywall screws · framing screws · pines · joint compound · joint tape | son **RENDIMIENTOS** por SF, no cantidades del plano; el yield ya trae su propia holgura |

---

## RFIs

Instrucción de Rodolfo: **él habla con los arquitectos.** Los RFIs se siguen escribiendo y
declarando dentro del take-off, con su delta cada uno, pero dejan de reportarse como pendiente
de Claude y dejan de listarse como trabajo que falta.


---
