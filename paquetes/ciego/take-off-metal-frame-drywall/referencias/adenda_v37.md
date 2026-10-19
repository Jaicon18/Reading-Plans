# ADENDA v<n> — <n>-oct-<n> · LOS <n> CALLOUTS, CERRADOS

Rodolfo: *"ya te dije que los termines sin preguntar, puedes o no?"*. Terminados: los <n>
callouts que el plano señala quedaron usados o declarados, y `entregar.py` pasa sus <n> pasos.

## 1. El RFI del parapet se CIERRA — el infill de `11/S5.10` SÍ se ubica

La v35 decía que `11/S5.10 PARAPET INFILL FRAMING` "no se ubica en ningún plano" y lo dejó
como RFI contra la lectura arquitectónica de `6" CFMF` corrido. **Estaba mal.** La cadena de
detalles lo resuelve sin preguntar a nadie:

(ejemplo de una corrida retirado del paquete ciego)

El wall ligero **termina en el B.O.D.** con deflection track; de ahí arriba el parapet es
**otro wall**, con otro perfil y otro calibre.

### Por qué la sección arquitectónica no contradice nada

Una sección a `1"=1'-0"` **no dibuja studs**: dibuja la cavidad llena de spray foam. La línea
fina continua que leí como "stud corrido a través del deck" es la face interior del
sheathing. Hay que abrir el zoom antes de concluir.

> **REGLA INVIOLABLE.** Un detalle a 3/4"=1'-0" que rotula perfil y calibre gana sobre una
> línea de sección a 1"=1'-0". **La sección dice QUÉ hay; el detalle dice CÓMO está armado
> y CUÁNTAS layers lleva.** Cuantificar layers desde la sección es cuantificar desde el resumen.

### Lo que cambió


El B.O.D. queda CONFIRMADO por dos fuentes independientes: `S2.20` lo rotula `B.O.D. EL.
[valor retirado E24] NO SLOPE` y `H/A09.23` lo repite como `T/ STEEL [valor retirado E24]`.

### El bridging no cruza el deflection track

> **REGLA INVIOLABLE.** Cuando un eje se parte en dos walls apilados, **cada uno cuenta sus
> rows de bridging sobre SU propia height.** El deflection track existe para que el wall
> se mueva ±1/2" respecto de la viga: una row continua lo anularía. Un parapet de menos
> de 4'-0" no lleva ninguna, y se declara EXCLUDED con esa razón, nunca se omite.

### Y la regla general que esto confirma

> **Un elemento que CAMBIA DE SISTEMA a media height tiene su propio detalle y su propio
> spec.** Antes de correr un stud "de la slab al tope" de corrido, buscar el detalle de la
> banda de arriba: casi siempre existe y casi siempre dice otra cosa. Es la regla de las dos
> bandas de una abertura, aplicada en vertical al edificio entero.

## 2. Una layer que las secciones NO rotulan y los detalles SÍ

`5/A09.26 SECTION DETAIL @ ACM BASE` y `9/A09.27 SECTION DETAIL @ METAL PANEL BASE` rotulan
**`5/8" GLASS MAT SHEATHING`** con la flecha apoyada en la face EXTERIOR del `6" METAL STUD
FRAMING`. `7/A09.26` lo repite a media height.

**Las OCHO secciones de wall del set no lo nombran ni una vez.** Son **[valor retirado E24] SF** de
board que no estaban en el take-off.

La extensión se acotó con un barrido de las <n> hojas por `GLASS MAT`/`GLASS-MAT`: solo
aparece en A09.<n> y A09.<n>, y **nunca por encima del deck** — `4/A09.26 @ PARAPET` no la
lleva. Por eso corre de slab a B.O.D. y no sigue al parapet.

> **REGLA.** Antes de dar por completa la composición de un wall, barrer el set por el NOMBRE
> de cada layer que un detalle mencione. Un barrido por término cuesta un minuto y acota la
> extensión de una layer mejor que cualquier lectura.

## 3. Dos bugs de compuerta — las dos miraban menos de lo que creían

**`verif_callouts.citados()` leía solo los cierres agrupados.** El glob era `*_cierre*.json`.
Los cierres que se guardan **uno por wall** (`out/B<n>/B<n>_v<n>_muro_<n>.json`, `out/A1/…`)
quedaban fuera, así que la compuerta daba por NO CITADOS detalles citados desde hacía días.
Ahora le pregunta a `resumen_global.SRC`, que es el único que sabe dónde vive cada cierre.

> **REGLA.** Una compuerta nunca arma su propia lista de archivos. Le pregunta al módulo que
> ya la tiene. Es el mismo motivo por el que existe `verif_planos`.

**`idioma_es.HOMOGRAFOS` estaba declarado y nunca se restaba de `PAL`.** El detector contaba
`no` y `exterior` como evidencia de español y marcaba como españolas frases en inglés
(`"S2.20, T/STEEL, NO SLOPE"`). Además `y=<coordenada>` aportaba una "y" y `O.C.` una "o".

> **Un detector que marca inglés como español vuelve inútil el trinquete:** el tope sube por
> falsos positivos y las frases que SÍ están en español se esconden entre ellos.

Corregido con `PAL = set(FUNC.split()) - set(HOMOGRAFOS)` y un `NO_PALABRA` que borra
coordenadas (`x=`, `y=`) y abreviaturas de obra (`O.C.`, `T.O.`, `N.T.S.`, `V.I.F.`, `TYP.`).
195 "celdas en español" → **<n> reales**. `TOPE_ES` <n> → <n>.

## 4. Trampa operativa: `| head` mata el script antes de que escriba

`python<n> cerrar_exterior.py | head -<n>` imprimió los sellos y **no escribió el JSON**: `head`
cierra el pipe, el SIGPIPE mata el proceso y el `json.dump` final nunca corre.

> **REGLA.** Un script que escribe archivos se corre a archivo (`> salida.txt`) y después se
> lee. Nunca con `| head`.

## 5. El furring de columna es un LAZO CERRADO

`verif_columnas` rechazó las cuatro columnas de marquesina (`5/A09.25`) porque la face de
plywood mide más LF que el eje de stud. En un wall eso es un error; en un lazo
cerrado el board **envuelve** el stud y pasa exactamente <n> espesores en cada uno de los
<n> vértices.

Se admitió **con la aritmética, no con una exención**: pasa solo si el exceso cuadra con
`<n> × espesor` dentro de 1". Si el exceso es otro, el fallo se reporta igual.

> **REGLA.** El conteo de studs de un lazo cerrado es `floor(perímetro × <n> / O.C.)` **sin el
> "+1"** — no hay dos terminaciones que cerrar — **más <n> stud de esquina por vértice**. Y el
> board se mide por la face EXTERIOR, no por el FOS.

## 6. Lo que la cadena destapó, en line items


Excluidos con motivo leído de su propio texto, uno por uno y nunca en bloque: estuco PT-nn y
PT-nn (Div <n> <n> <n>, lath y screed del plasterer, citando `6/A09.31`), bollards, HSS posts,
steel columns, y <n> detalles estructurales de S3.20 / S5.10 / S5.30.

### Dos RFIs nuevos, porque no se inventa lo que no se distingue

1. **El BOX del pier de storefront.** Las dimensions impresas de `1/A09.25` salen de los ejes F/G
   y de la face del storefront, **no de las cuatro faces del pier**, y no cierran contra el
   contorno dibujado. En juego: [valor retirado E24] SF de board y [valor retirado E24] studs.
2. **El width de la tira** de `3/4" FRT PLYWOOD` y del retorno de board. Los cinco detalles
   que cortan el marco del opening rotulan el material y **ninguno acota el width**.

> **REGLA.** Cuando las dimensions impresas de un detalle NO cierran contra el contorno dibujado,
> no se elige una lectura: se declara PENDIENTE, se abre el RFI con el tamaño de la pregunta
> (no con una estimación disfrazada) y se cuantifica todo lo demás del elemento.

---
