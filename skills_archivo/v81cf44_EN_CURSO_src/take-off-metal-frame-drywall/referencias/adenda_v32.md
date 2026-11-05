# ADENDA v<n> — <n>-sep-<n> · TODO NOMBRE DE MATERIAL SE ESCRIBE EN INGLÉS

## De dónde salió

<!-- GLOSARIO:INICIO -->
Rodolfo: *"tablero y metal: vamos a cambiar estas palabras al inglés, cambia todos los materiales al inglés, y crea la regla."*

<!-- GLOSARIO:FIN -->

Extiende la orden anterior de términos de oficio en inglés (jambs, header, sill, track, stud, blocking, bracing, deflection, slip track, furring, soffit, storefront, deck, mullion, HATCH) a **todos los nombres de material**.

## REGLA

**El material se pide, se compra y se instala en inglés.** El proveedor cotiza `5/8" gypsum board`, la orden de compra dice `600S137-33`, el instalador pide *board*. Un renglón en español obliga a traducir mentalmente cada vez, y **en esa traducción es donde se pide lo que no era**.

**Alcance:** se traduce el MATERIAL y sus componentes. La prosa puede seguir en español — *"la face este lleva <n> layers of gypsum board"* está bien. No se traducen los nombres de cuarto del plano (ya vienen en inglés), ni las dimensions, ni la prosa.

## Glosario

<!-- GLOSARIO:INICIO -->

<!-- GLOSARIO:FIN -->

**La frase más larga gana siempre, y el glosario se ordena por longitud EN CÓDIGO.** Ordenarlo a mano es una bomba: <!-- GLOSARIO:INICIO -->
basta meter un término nuevo en el lugar equivocado para que `madera FRT` le gane a `bloqueo de madera FRT` y salga *"bloqueo de FRT wood"*.
<!-- GLOSARIO:FIN -->

## COMPUERTA — `verif_idioma.py`

Paso **<n> de <n>** de `entregar.py`. Revisa **cada celda** del `.xlsx` y **cada línea** de los `.md` de la entrega. Si queda un nombre de material en español, **no se entrega**.

Probada con <n> casos (`test_verif_idioma.py`): sin acento · con acento · plural · frase compuesta · el traductor arregla lo que la compuerta caza · texto en inglés sin falsa alarma · excepción declarada respetada.

## Tres cosas que costaron y no hay que repetir

### 1. El detector y el corrector tienen que normalizar IGUAL

`faltas()` buscaba sin acentos y `traducir()` con acentos. <!-- GLOSARIO:INICIO -->
La compuerta encontraba `perfileria` dentro de `perfilería` y el traductor **no lo cambiaba nunca**.
<!-- GLOSARIO:FIN -->

> Una falta que se reporta para siempre y no se arregla nunca es peor que no detectarla: enseña a ignorar la compuerta.

Ahora los dos usan el mismo patrón, con las vocales como clase de carácter (`a` → `[aáA]`).

### 2. Se arregla el GENERADOR, no la salida

`<PREFIJO>_ESTADO.md` se tradujo y volvió a salir en español en la siguiente run, porque su plantilla seguía en español. Es la misma regla de la v31 — todo resumen se deriva de la fuente — aplicada al idioma.

Y el generador ahora **pasa su salida por el glosario antes de escribir**, así una palabra en español que se cuele en la plantilla se corrige sola en vez de quedarse esperando a que alguien la vea.

### 3. La compuerta que revisa archivos FINALES va AL FINAL

Puesta antes de regenerar el estado, leía el `<PREFIJO>_ESTADO.md` viejo y reportaba una falta que el paso siguiente ya estaba arreglando.

> Una compuerta que revisa el producto terminado corre cuando el producto está terminado. Ponerla antes genera falsas alarmas que se resuelven solas — y ésas son las que enseñan a ignorarla.

## Para tocar un cierre YA SELLADO — `traducir_materiales.py`

Mismo procedimiento que `resellar_b<n>k.py`, que es el único seguro:

1. Se aplica el glosario **solo a las cadenas**, nunca a un número ni al campo `sello`.
2. Se extraen **todos** los números del objeto con su ruta, antes y después, y se exige que sean idénticos. Si uno se movió, **no se escribe nada**.
3. Se recalcula el sello con la misma función del closer.

Resultado en un proyecto anterior: **[valor retirado E24] archivos, [valor retirado E24] con texto traducido, [valor retirado E24] bloques resellados, <n> números movidos.** Todos los sellos siguen verificando.

## Los documentos históricos se CONGELAN, no se traducen

Las versiones v25 a v30 del skill y las adendas ya publicadas se excluyen en `HISTORICOS` **con motivo escrito**, nunca en silencio: traducirlas sería reescribir lo que ya se entregó con esa redacción. La versión **vigente** del skill sí entra a la compuerta.

---
