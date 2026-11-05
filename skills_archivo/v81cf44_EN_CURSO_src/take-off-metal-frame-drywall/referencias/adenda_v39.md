# ADENDA v<n> — <n>-oct-<n> · EL VOCABULARIO DEL TRADE VA EN INGLÉS, SIEMPRE

## ⛔ REGLA INVIOLABLE

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

## CÓMO SE HACE CUMPLIR, QUE ES LA PARTE QUE NO SE OLVIDA

`glosario.py` pasó de <n> a **<n> entradas**. `traducir_materiales.py` las aplica a los
**cierres sellados** probando que ningún número se movió y resellando. Y se agregó
`traducir_docs.py`, que las aplica a los **documentos .md** con tres salvaguardas:

1. **No se toca nada dentro de un bloque de código ni de `inline code`.** Ahí hay nombres de
   archivo, de variable y comentarios COPIADOS del `.py`. Traducir un comentario copiado lo
   desincroniza del código real, y entonces el documento cita un código que no existe. **Un
   documento que miente sobre el código es peor que uno en español.**
2. **Ningún número se mueve.** Se extraen todos los números antes y después y tienen que ser
   idénticos, en el mismo orden. Si uno cambió, no se escribe nada.
3. **Los documentos CONGELADOS quedan fuera**, con el **mismo detector** de `verif_idioma`
   (`es_historico`), nunca una copia de la regexp.

<!-- GLOSARIO:INICIO -->
Y lo que el corrector **deja dentro de un bloque de código lo IMPRIME**, para arreglarlo a mano
o en el `.py`. Si no se dijera, esa falta se reportaría para siempre sin arreglarse nunca — que
es exactamente el error que ya costó una entrega con `perfilería`/`perfileria`.
<!-- GLOSARIO:FIN -->

---

## LOS TRES ERRORES QUE DESTAPÓ APLICARLA (y las reglas que dejan)

### 1. FALSOS AMIGOS: la misma palabra nombra piezas de divisiones distintas

<!-- GLOSARIO:INICIO -->
<!-- GLOSARIO:FIN -->

<!-- GLOSARIO:INICIO -->
> **REGLA:** antes de traducir un nombre de material, **leer en qué elemento está**. Entra al
> glosario la palabra que en este trade **solo** puede nombrar la pieza; la que fuera del trade
> significa otra cosa entra **como frase** (`cara de acabado` → `face of finish`, pero `acabado`
> suelto NO: "ya acabado" no es un material). **Un glosario que prohíbe una palabra ambigua
> convierte la compuerta en ruido, y una compuerta ruidosa se acaba apagando.**
<!-- GLOSARIO:FIN -->

### 2. `capitalize()` destruye los acrónimos de material

<!-- GLOSARIO:INICIO -->
El reemplazo usaba `ing.capitalize()`, que sube la primera letra y **baja todas las demás**:
`madera FRT` salía **`Frt wood`**, y `F_cierre.json` ya lo tenía **sellado así**. `Frt wood` no
se cotiza.

Ahora son **tres casos, no dos**: TODO EN MAYÚSCULAS → la traducción en mayúsculas (un título
que decía `EL ANTEPECHO / KNEE WALL` salía `EL Sill / KNEE WALL`, con la palabra nueva en otra
caja que su propio renglón); primera en mayúscula → **solo** la primera; todo minúscula → tal
cual. Más una lista `REPARA` que devuelve a mayúsculas lo ya escrito (FRT, W.R., PVC, ACM, GWB,
PAF, DensGlass, Type X…).

> **REGLA:** ninguna función de caso se aplica a un nombre de material sin comprobar qué hace
> con las letras que **no** son la primera.
<!-- GLOSARIO:FIN -->

### 3. Dos copias del mismo documento se desincronizan

Traducir sólo el original dejó la copia de la carpeta de entrega en español — y la compuerta la
siguió cazando, **con razón: la copia es la que se manda**. `traducir_docs.py` corre sobre las
**dos** carpetas por defecto.

> **REGLA:** una compuerta revisa el archivo que SE ENTREGA, no el que se editó.

### Lo que NO entró todavía, con su motivo escrito

- `cielo` → `ceiling`: choca con los **nombres de archivo** del propio proyecto
  (`CIELOS_cierres.json`, `hoja_cielos.py`). Una palabra del glosario que marca un nombre de
  archivo vuelve la compuerta ruido. Entra cuando se declare la excepción de nombres de archivo.
- `desperdicio` → `waste`: `resumen_total.py` imprime la columna `DESPERDICIO` en consola y hay
  que renombrarla en el **mismo** paso, no antes.

**Estado tras la adenda: 14/14 compuertas pasan · <n> sellos OK / <n> rotos · <n> nombres de material
en español en los archivos finales · atraso de prosa <n> (libro) y <n> (hoja de evidencia), los
dos sólo bajan.**

---
