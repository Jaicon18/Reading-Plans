# ADENDA v37 — 3-oct-2026 · LOS 42 CALLOUTS, CERRADOS

Rodolfo: *"ya te dije que los termines sin preguntar, puedes o no?"*. Terminados: los 50
callouts que el plano señala quedaron usados o declarados, y `entregar.py` pasa sus 11 pasos.

## 1. El RFI del parapet se CIERRA — el infill de `11/S5.10` SÍ se ubica

La v35 decía que `11/S5.10 PARAPET INFILL FRAMING` "no se ubica en ningún plano" y lo dejó
como RFI contra la lectura arquitectónica de `6" CFMF` corrido. **Estaba mal.** La cadena de
detalles lo resuelve sin preguntar a nadie:

```
S2.20 ROOF FRAMING PLAN
   └─ burbuja 6/S5.10 y 10/S5.10 SECTION AT PERIMETER
         "DEFLECTION TRACK PER LT. GA. MFR. TO ACCOMMODATE
          VERTICAL MOVEMENT OF PERIMETER BEAM +/- 1/2""
         "LT. GA. FRAMING — REF. LT. GA. NOTES"
         "REF. 11/S5.10 FOR INFILL FRAMING"
              └─ 11/S5.10 PARAPET INFILL FRAMING
                    "600S162-54 @ 16" W/ 600T125-54 TOP & BOT."
                    "ONE STUD EA. SIDE OF EA. POST - 5'-0" O.C. MAX."
                    "PAFs SPACED AT 12" O.C. MAX."
   └─ 7/S5.11 ROOF SECTION repite la condición
```

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

| | antes | ahora |
|---|---|---|
| wall exterior | un `600S137-33` de slab a T/STUD | `600S137-33` de slab a **B.O.D. 15'-4 1/2"** |
| tope del wall | top track común | **DEFLECTION TRACK** (6/S5.10, 10/S5.10) |
| parapet | la misma pieza, seguida | **6 walls nuevos**, tag `EXT-PARAPET`, `600S162-54 @16"` con `600T125-54` arriba y abajo |
| studs del parapet | — | + 2 por cada HSS post @ 5'-0" O.C. |
| anchorage del infill | — | **PAFs @ 12" O.C.** a la steel beam |
| `T/ STUD HP 19'-8"` | DERIVADO | **CONFIRMADO** — impreso en `A/A09.21`, hoja que no había abierto |

El B.O.D. queda CONFIRMADO por dos fuentes independientes: `S2.20` lo rotula `B.O.D. EL.
15'-4 1/2" NO SLOPE` y `H/A09.23` lo repite como `T/ STEEL 15'-4 1/2"`.

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

**Las OCHO secciones de wall del set no lo nombran ni una vez.** Son **2,939.76 SF** de
board que no estaban en el take-off.

La extensión se acotó con un barrido de las 95 hojas por `GLASS MAT`/`GLASS-MAT`: solo
aparece en A09.26 y A09.27, y **nunca por encima del deck** — `4/A09.26 @ PARAPET` no la
lleva. Por eso corre de slab a B.O.D. y no sigue al parapet.

> **REGLA.** Antes de dar por completa la composición de un wall, barrer el set por el NOMBRE
> de cada layer que un detalle mencione. Un barrido por término cuesta un minuto y acota la
> extensión de una layer mejor que cualquier lectura.

## 3. Dos bugs de compuerta — las dos miraban menos de lo que creían

**`verif_callouts.citados()` leía solo los cierres agrupados.** El glob era `*_cierre*.json`.
Los cierres que se guardan **uno por wall** (`out/B2/B2_v2_muro_25.json`, `out/A1/…`)
quedaban fuera, así que la compuerta daba por NO CITADOS detalles citados desde hacía días.
Ahora le pregunta a `resumen_global.SRC`, que es el único que sabe dónde vive cada cierre.

> **REGLA.** Una compuerta nunca arma su propia lista de archivos. Le pregunta al módulo que
> ya la tiene. Es el mismo motivo por el que existe `verif_planos`.

**`idioma_es.HOMOGRAFOS` estaba declarado y nunca se restaba de `PAL`.** El detector contaba
`no` y `exterior` como evidencia de español y marcaba como españolas frases en inglés
(`"S2.20, T/STEEL, NO SLOPE"`). Además `y=283.8` aportaba una "y" y `O.C.` una "o".

> **Un detector que marca inglés como español vuelve inútil el trinquete:** el tope sube por
> falsos positivos y las frases que SÍ están en español se esconden entre ellos.

Corregido con `PAL = set(FUNC.split()) - set(HOMOGRAFOS)` y un `NO_PALABRA` que borra
coordenadas (`x=`, `y=`) y abreviaturas de obra (`O.C.`, `T.O.`, `N.T.S.`, `V.I.F.`, `TYP.`).
195 "celdas en español" → **161 reales**. `TOPE_ES` 188 → 161.

## 4. Trampa operativa: `| head` mata el script antes de que escriba

`python3 cerrar_exterior.py | head -12` imprimió los sellos y **no escribió el JSON**: `head`
cierra el pipe, el SIGPIPE mata el proceso y el `json.dump` final nunca corre.

> **REGLA.** Un script que escribe archivos se corre a archivo (`> salida.txt`) y después se
> lee. Nunca con `| head`.

## 5. El furring de columna es un LAZO CERRADO

`verif_columnas` rechazó las cuatro columnas de marquesina (`5/A09.25`) porque la face de
plywood mide 6.08 LF contra 5.67 LF de eje de stud. En un wall eso es un error; en un lazo
cerrado el board **envuelve** el stud y pasa exactamente 2 espesores en cada uno de los
4 vértices.

Se admitió **con la aritmética, no con una exención**: pasa solo si el exceso cuadra con
`8 × espesor` dentro de 1". Si el exceso es otro, el fallo se reporta igual.

> **REGLA.** El conteo de studs de un lazo cerrado es `floor(perímetro × 12 / O.C.)` **sin el
> "+1"** — no hay dos terminaciones que cerrar — **más 1 stud de esquina por vértice**. Y el
> board se mide por la face EXTERIOR, no por el FOS.

## 6. Lo que la cadena destapó, en line items

| line item | fuente |
|---|---|
| `5/8" GLASS MAT SHEATHING` face exterior del stud | 5/A09.26, 9/A09.27, 7/A09.26 |
| `PARAPET INFILL` `600S162-54` + `600T125-54` top & bot + PAFs | 11/S5.10 |
| Furring de las columnas de marquesina | 5/A09.25 |
| `METAL STUD BOX BEAM` sobre storefront | 11/A09.27, 2/A09.26 |
| `3/4" FRT PLYWOOD` perímetro de openings | 11/A09.27, 10/A09.27, 1·2·3/A09.25 |
| `GYPSUM BOARD JAMB RETURN` | 11/A09.27, 2/A09.26 |

Excluidos con motivo leído de su propio texto, uno por uno y nunca en bloque: estuco PT-3 y
PT-03 (Div 09 24 00, lath y screed del plasterer, citando `6/A09.31`), bollards, HSS posts,
steel columns, y 15 detalles estructurales de S3.20 / S5.10 / S5.30.

### Dos RFIs nuevos, porque no se inventa lo que no se distingue

1. **El BOX del pier de storefront.** Las dimensions impresas de `1/A09.25` salen de los ejes F/G
   y de la face del storefront, **no de las cuatro faces del pier**, y no cierran contra el
   contorno dibujado. En juego: ~170 SF de board y ~20 studs.
2. **El width de la tira** de `3/4" FRT PLYWOOD` y del retorno de board. Los cinco detalles
   que cortan el marco del opening rotulan el material y **ninguno acota el width**.

> **REGLA.** Cuando las dimensions impresas de un detalle NO cierran contra el contorno dibujado,
> no se elige una lectura: se declara PENDIENTE, se abre el RFI con el tamaño de la pregunta
> (no con una estimación disfrazada) y se cuantifica todo lo demás del elemento.

---
