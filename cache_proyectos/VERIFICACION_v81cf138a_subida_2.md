# Verificación v81cf138a (subir_entrega.py, fixes de H1-H5): segunda ronda

**Veredicto: VERDE.** Ninguna entrada encontrada deja subir un FAIL distinto del nombrado, una corrida incompleta, una excepción no autorizada por "usuario" o una excepción sin texto en README. Quedan observaciones de severidad baja (R1-R4), que conviene corregir en otra versión.

Árboles: candidato `/tmp/v1381/take-off-metal-frame-drywall/tools` (v1381) y base publicada `/tmp/v138fb/take-off-metal-frame-drywall/tools` (v138).
Scripts y salidas: `/tmp/v1381rev2/` (r2.py, vv.py, e2e.py, out_*.txt, out2_*.txt).

## 1. Re-ejecución de los scripts anteriores (/tmp/v1381rev)
- **casos.py**: v138 bloquea todos los casos (con `check int` da TypeError, o sea que también bloquea). v1381 bloquea todos los casos y da la causa U-201 (6). El caso "base valida" ahora bloquea porque la corrida está incompleta, ya que el fixture no tiene `vigentes` ni todos los chequeos. Eso es correcto según H2/H3.
- **vigente.py**: v1381 da PASS en "completa + excepción" y FAIL en "sin excepción", en "parcial" y en "otro 'fail'". v138 da FAIL en los 4 casos.
- **candados_otros.py**: los dos árboles bloquean los 4 casos. En v1381 bloquean antes, por la corrida incompleta. "gate --solo" no escribe ENTREGA_OK en ninguno de los dos.

## 2. Camino positivo con fixture completo (r2.py, vv.py)
Fixture: todos los ids de CE.CHEQUEOS en PASS menos CE_PROTOCOLO_3H en FAIL, `vigentes` con el Excel, la excepción válida y README `## Process exception\nCE_PROTOCOLO_3H: <texto>`.

| Caso | v138 | v1381 |
|---|---|---|
| completo + excepción válida (candados) | BLOQUEA | SUBE |
| completo sin excepción | BLOQUEA | BLOQUEA ("sin excepcion_usuario autorizada") |
| verificar_vigente, excepción válida, md5 de Drive = el validado | n/a | PASS |
| verificar_vigente, excepción válida, md5 de Drive distinto | n/a | FAIL (md5) |
| verificar_vigente, sin excepción | n/a | FAIL ("compuerta no verde sin excepción…") |
| ok=true + 1 FAIL + excepción válida | BLOQUEA | SUBE (coherente con la regla) |

No se pudo hacer el e2e completo de `subir()` con el gdrive falso. Pasa candados y luego bloquea en la verificación de la carpeta padre de Drive (`FOLDER123 NO es hija de Claude outputs`), porque el falso no la simula. Por eso el registro de `excepcion_usuario` en SUBIDA_OK solo se revisó leyendo el código (línea 446). Ese código lo escribe solo cuando la compuerta no es verde.

## 3. Intentos de bypass (r2.py). Resultado en v138 / v1381
En v138 todos estos casos BLOQUEAN, porque no hay excepción posible.

| Entrada | v1381 | Correcto |
|---|---|---|
| vigentes = {} | BLOQUEA (corrida no completa) | sí |
| vigentes ausente | BLOQUEA | sí |
| otro chequeo con estado 'Amber' | BLOQUEA (no verde) | sí |
| el FAIL con estado 'Fail' | BLOQUEA (tiene que ser exactamente 'FAIL') | sí |
| otro chequeo con estado None | BLOQUEA | sí |
| check con '\n' final (`$` de la regex) | BLOQUEA (no coincide con el id) | sí |
| autorizado_por 'usuario​' | BLOQUEA | sí |
| look-alike cirílico (Е) en el README | BLOQUEA | sí |
| check y texto en secciones '#' distintas | BLOQUEA | sí |
| '#' a mitad de línea | SUBE (no parte la sección) | sí |
| **R1a** check y texto separados por un heading indentado `   ## B` | SUBE | no: en Markdown son dos secciones |
| **R1b** check y texto separados por un heading setext (`B\n===`) | SUBE | no |
| **R1c** check y texto solo en un comentario HTML `<!-- … -->` | SUBE | dudoso: no se ve al renderizar |
| **R1d** check y texto solo en el preámbulo, antes del primer '#' | SUBE | dudoso: no es una sección '#' |
| **R1e** `# CE_… texto` dentro de un bloque de código ``` | SUBE | dudoso: el `#` del código se toma como heading |
| **R2a** texto = 30 × U+200B (zero-width space), también en README | SUBE | no: el texto es invisible y vacío |
| **R2b** texto = 30 puntos / 'a'+28 espacios+'b' | SUBE | cumple el ">= 30" literal, pero el texto no explica nada |
| **R3a** fecha con dígitos fullwidth '２０２６-１１-１３' (`\d` unicode) | SUBE | no |
| **R3b** fecha '2026-99-99' | SUBE | no: no es una fecha válida |
| **R4** CE_PROTOCOLO_3H repetido como PASS y como FAIL / otro id repetido en PASS | SUBE | la compuerta real no lo produce, es informativo |

## Hallazgos
- **R1 (baja)**: `re.split(r"(?m)^(?=#)")` no reconoce como límite los headings ATX indentados 1 a 3 espacios ni los setext. Además acepta comentarios HTML, el preámbulo y '#' dentro de bloques de código. La excepción puede quedar invisible o fuera de una sección '#'. Sugerencia: partir con `^\s{0,3}#{1,6}\s` y con setext, ignorar los bloques de código, quitar los `<!-- -->` antes de buscar y exigir que el texto esté en una sección con heading.
- **R2 (baja)**: `len(texto.strip()) >= 30` cuenta caracteres invisibles (U+200B, U+200C, U+200D, U+2060, U+FEFF) y relleno. Sugerencia: contar solo caracteres visibles, quitar los invisibles y exigir un mínimo de letras (por ejemplo `len(re.findall(r"\w", t)) >= 20`).
- **R3 (baja)**: `RX_EXC_FECHA` usa `\d` unicode y no valida la fecha. Sugerencia: usar `[0-9]` o `re.ASCII` y además `datetime.fromisoformat`.
- **R4 (informativo)**: no se rechazan ids repetidos en `chequeos`.
- **Sin excepción** el comportamiento es igual al de v138, con una sola diferencia: v1381 también bloquea `ok=true` con un estado no verde que no es 'FAIL' ('ERROR', 'fail', vacío), y v138 lo dejaba pasar. Es la corrección intencional de H1 y va en dirección segura.
