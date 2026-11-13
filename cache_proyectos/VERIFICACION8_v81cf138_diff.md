# VERIFICACIÓN INDEPENDIENTE 8 (solo el diff v81cf138 vs v81cf137)

Fecha: 2026-11-13 04:30 PT

Revisor independiente (no escribí el código). Candidato: commit 09dd4ce, armado como v137 (zip `skills_archivo/take-off-metal-frame-drywall_v81cf137_lecturas-walls-fechas-reales_2026-11-13.zip`) + `apartados/v81cf138_wip/v81cf138_desde_v81cf137.patch` (sha256 2961b93f…4452) en `/tmp/verif8/take-off-metal-frame-drywall`: `**VERSION: v81cf138**`, 199 archivos. Es idéntico byte a byte a `/tmp/v138n` (compuerta_entrega.py, chequeos_biblioteca.py, runner/completitud.py y SKILL.md). Para comparar, v137 quedó en `/tmp/verif8/v137/`.

## VEREDICTO GLOBAL: NO PUBLICAR

De los 5 arreglos, 3 están en ROJO: BE-XF18, CB_BE_83 y CE_PROTOCOLO_3H tienen regresiones, es decir, casos que v137 marcaba y que el candidato deja pasar en silencio. CE_COBERTURA_DIAG está en ROJO porque 1 de los 15 pares filtrados de la muestra de CR es un muro real. Solo CB_BE_CF04 queda en VERDE.

## Qué se revisó

- `apartados/v81cf138_wip/LEEME.md` y el diff completo. El alcance son solo los 5 arreglos: compuerta_entrega.py, chequeos_biblioteca.py (`be_cf04`) y runner/completitud.py.
- Los adversariales de la verificación 7 (`adv7_xf18`, `adv7_be83`, `adv7_cf04`, `adv7_pm06`, `adv7_cobdiag`), re-corridos contra v137 y contra el candidato.
- Adversariales propios en `/tmp/verif8/adv8/adv8_*.py`, cada uno con su salida `.out`.
- Datos reales:
  - XF: `/root/xf/work/entrega` con `--solo` de los 5 chequeos.
  - 79 canones reales de `cache_proyectos` y `/root/xf`, para CB_BE_83 y CB_BE_CF04.
  - 33 carpetas reales `Planos marcados`, para BE-XF18.
  - El PDF real de markups de CR rev20b `/tmp/claude-0/crmk/CR_mk.pdf`, para CE_COBERTURA_DIAG, hoja por hoja, con imagen de una muestra de 15 pares.

## Corridas

| corrida | resultado |
|---|---|
| suite del candidato (`correr_suite.py --skill /tmp/verif8/take-off-metal-frame-drywall`) | **47/47 OK** |
| XF real `--solo CE_PDF_MARKUPS_ELEGIDO,CB_BE_83,CB_BE_CF04,CE_PROTOCOLO_3H,CE_COBERTURA_DIAG` | v137: PASS 3 / AMBER 2 / FAIL 0. Candidato: PASS 4 / AMBER 2 / FAIL 0 (el chequeo nuevo CE_PDF_MARKUPS_ELEGIDO da PASS con `XF_markups_rev1c - OPEN IN BLUEBEAM.pdf`). Los demás mensajes son idénticos: 0 falsos FAIL nuevos. Borré `ENTREGA_RAPIDA.json`. **Ojo:** cada corrida agregó 2 renglones (`inicio`/`fin`, tipo `rapida`, 10:11 UTC) a `/root/xf/work/entrega/compuerta_corridas.jsonl`, 4 en total; el archivo pasó de 21 a 25 líneas. No pude quitarlos (el permiso fue denegado), así que quedan para que COORDINACIÓN decida. |
| adv7_xf18 | v137 no tiene el chequeo. Candidato: X1 ahora da FAIL (bien). X2 sigue dando PASS con el PDF de la rev anterior. **X3 lee el OPEN IN BLUEBEAM de la rev anterior**: es la regresión R1 de abajo. |
| adv7_be83 | v137 da TypeError en F0 (faces = número). Candidato: F1/F3/F5 marcan; F4 ('stair enclosure' solo mencionado) y F6 ('rooms') pasan en silencio. |
| adv7_cf04 | v137 dejaba pasar '2 X 6', '2×6 SPF', 'DF stud' y 'timber'. El candidato los marca todos. |
| adv7_pm06 | P0–P3 dan FAIL en los dos (P2 en el candidato sin la alerta del 100 %, que en v137 venía del log acumulado del 05-nov). |
| adv7_cobdiag | K0–K4 siguen saliendo como no cubiertos en los dos. |
| CR canon rev20b, `caras_sobre_ceiling` | v137: TypeError (las 943 walls tienen `faces` = int). Candidato: 0 caras. Hay 40 caras sobre el cielo, todas justificadas SOLO por la regex nueva (38 'underside of roof framing', 2 'stair enclosure', 3 'floor to floor' de shaft). |
| 79 canones, be_83 / be_cf04 | CF04: el veredicto no cambia en ningún canon; en CR solo cambia el mensaje (sin '0 walls'). BE_83: deja de caerse en CR y CFA. En BoA salen 2 caras nuevas (detalle en el arreglo 2). Ninguna cara de `faces`-lista quedó silenciada en un canon real. |
| 33 carpetas reales de `Planos marcados` | La elección del PDF es igual en v137 y en el candidato en las 33. En `/root/xf/work/cobertura_v119` v137 leía `COBERTURA - IMAGE ONLY.pdf` y el candidato da FAIL con la causa (está bien). |
| CR_mk.pdf, `cob_diag_cortos` | No cubiertos: 478 → 357. Hay 119 pares que v137 daba como no cubiertos y el candidato ya no (todos `muro_corto`), y 1 par nuevo que solo saca el candidato (A6.02 (1369.6, 1322.1)). Los 4 furrings FALTA siguen saliendo a 0.0 ft: A6.00 (1683.1, 297.4), A6.02 (1036.9, 1024.0) y (1036.9, 639.7), A7.50 (1556.4, 907.2). |

## Tabla arreglo → veredicto → evidencia

| arreglo | veredicto | evidencia |
|---|---|---|
| 1 BE-XF18 | **ROJO** | Con un solo 'OPEN IN BLUEBEAM' no se revisa la rev: si es de la rev anterior, el candidato lo lee con PASS en silencio donde v137 leía el de la rev en curso (R1). Si hay dos OPEN IN BLUEBEAM y el Excel más nuevo por mtime es de la rev anterior, también lee el de la rev anterior con PASS (R4). `adv8_xf18.py` |
| 2 CB_BE_83 | **ROJO** | La regex nueva `RX_SUBE_JUSTIFICADO` busca palabras sueltas en TODA la fuente y también se aplica a `faces`-lista, que v137 juzgaba. Una mención de 'underside of floor joists', 'stair enclosure', 'floor to floor' o 'extends to structure' de otro elemento silencia una cara de 11 ft bajo un cielo de 9 ft que v137 marcaba (A1–A4). `adv8_be83.py` |
| 3 CB_BE_CF04 | VERDE | No hay regresión: la regex nueva es un superconjunto de la de v137. No hay silencio nuevo. Hay falsos FAIL solo sintéticos ('framing' con 'wood blocking'), y ningún canon real usa `framing` en walls[]. `adv8_cf04.py`, `adv8_be83_cf04_canones.py` |
| 4 CE_PROTOCOLO_3H | **ROJO** | Tres casos: (Q1b) `tiempos_desde` borra la fila de un paso cerrado DESPUÉS del arranque porque su Inicio coincide con el Fin de un paso exento, y el resultado es PASS donde v137 daba FAIL "paso 1 sin --paso". (Q4) Con una marca tardía en el log y VERSION_PROYECTO fijado al final, todos los pasos de la rev quedan exentos "de una rev anterior" con PASS donde v137 daba FAIL. (Q2) Con el log sin marcas ISO y VERSION_PROYECTO al final da PASS, donde v137 daba FAIL "no se puede fechar". `adv8_pm06.py` |
| 5 CE_COBERTURA_DIAG | **ROJO** | Muestra de 15 de los 119 filtrados en CR: **1 de 15 es un muro real**. Es el #3, A6.00 (404.0, 746.5): `_cob_divisor_tag` lo quita por el borde de la caja del tag 'CM.8 \| 2' pegado al muro. Los 4 FALTA siguen saliendo; XF sin cambio. `adv8_cobdiag_cr.py`, `adv8_cobdiag_muestra.py`, `adv8_cobdiag_m3.py` |

## Detalle

### 1. BE-XF18: `compuerta_entrega.elegir_pdf_markups` / `_rev_en_curso_markups` / `Ctx` / `CE_PDF_MARKUPS_ELEGIDO`: ROJO

El problema está en `elegir_pdf_markups`, en la rama `if len(ob) == 1: return ob[0], None`: cuando hay un solo OPEN IN BLUEBEAM, se devuelve sin compararlo con la rev en curso. Eso contradice el LEEME ("uno de otra rev nunca").

Reproducción: `python3 -I /tmp/verif8/adv8/adv8_xf18.py /tmp/verif8/take-off-metal-frame-drywall/tools`.

- **R1 (regresión):** `Planos marcados/` = {`CR_markups_rev20b - OPEN IN BLUEBEAM.pdf`, `CR_markups_rev20c.pdf`}, `Take-off/CR_Takeoff_rev20c.xlsx`.
  - v137 lee `CR_markups_rev20c.pdf`.
  - El candidato da PASS y lee `CR_markups_rev20b - OPEN IN BLUEBEAM.pdf`: todos los chequeos de markups corren sobre la rev anterior.
- **R4 (regresión):** dos OPEN IN BLUEBEAM (20b y 20c) y dos Excel, con `CR_Takeoff_rev20b.xlsx` más nuevo por mtime (re-guardado o copiado).
  - v137 lee el de rev20c.
  - El candidato da PASS con el de rev20b. `_rev_en_curso_markups` decide la rev solo por mtime.
- R2: hay un solo OPEN IN BLUEBEAM, de rev20b, y el Excel es rev20c. El candidato da PASS en silencio, igual que v137; no es nuevo, pero el LEEME dice que esto no pasa.
- adv7 X2: `entrega.json 'markups'` apunta al PDF de la rev anterior (existe) y da PASS en los dos.
- Falsos FAIL nuevos, solo sintéticos: R5 (mapa 'IMAGE-ONLY' con guion más el markups sin sufijo) y R6 (markups más `_flattened`) dan FAIL con la causa, donde v137 elegía. No hay ninguno en las 33 carpetas reales.
- Lo bueno: R7–R10 y adv7 X1 dan FAIL con la causa, o eligen bien donde v137 leía el mapa.

### 2. CB_BE_83: `runner/completitud.caras_sobre_ceiling` / `_cara_de_muro` / `RX_SUBE_JUSTIFICADO`: ROJO

`RX_SUBE_JUSTIFICADO` reemplaza a `full height|to deck|above ceiling|hasta deck` también para las caras en lista. Busca la palabra en cualquier parte de `height_source`, aunque hable de otro elemento.

Reproducción: `python3 -I /tmp/verif8/adv8/adv8_be83.py <skill>`, con cuarto 905 de cielo 9 ft y cara de 11 ft. Los cuatro casos devuelven `[('Z9-L9-07','905 GUEST',11.0,9.0)]` en v137 y `[]` en el candidato:

- A1: `"C-2 GWB ceiling hung from underside of floor joists above (A5.1); wall 11'-0\" per section"`.
- A2: `"11'-0\" per 3/A3.1; see stair enclosure detail 5/A6.02 for the other wall"`.
- A3: `"level floor to floor 11'-0\" (A3.01) used as wall height"`.
- A4: `"11'-0\"; duct shaft extends to structure (M2.1)"`.

Otros hallazgos:

- **Falso positivo nuevo (c), sin cambio de veredicto:** `_cara_de_muro` se aplica a todo `faces` que no sea lista, también a `faces` ausente o None, no solo a números como dice el LEEME. Un muro exterior sin `faces` toma como cuarto todo el texto de `location`.
  - En el canon real de BoA (`bank_of_america/FINAL_markups_v80h/takeoff_canon_FINAL_rev1.json`) salen 2 caras nuevas: `R-16-2` y `R-17-2`, pilastras exteriores de storefront con `exterior: true` y `location` "… of VESTIBULE 100 - exterior 6\" CFMF L (faces N+W)".
  - BoA ya daba FAIL con 22 caras en v137, así que el veredicto no cambia, pero ese caso solo daría un FAIL falso.
- Silencios sin regresión (v137 se caía en estos casos):
  - B8: el cuarto solo aparece en `rooms`.
  - B6: `location` 'faces: exterior (905 GUEST side n/a)'.
- En CR (rev20b) las 40 caras sobre el cielo quedan justificadas solo por la regex nueva: 'underside of roof framing', 'stair enclosure' y 'floor to floor' de shaft. Leídas, son fuentes coherentes con la regla R80e.48. No es regresión, porque v137 no daba veredicto: se caía.

### 3. CB_BE_CF04: `chequeos_biblioteca.be_cf04`: VERDE

- Sin regresión: `\b2\s*[x×]\s*\d` contiene a `\b2x\d`, `\bwood\b` se mantiene y `fr()` solo agrega detección. 'gauge 2x6' y 'gauge wood' siguen dando FAIL.
- El veredicto no cambia en ningún canon real; en CR solo cambia el mensaje.
- Observaciones que no bloquean:
  - Siguen pasando en silencio, igual que en v137: 'lumber 2-by-6', 'Hem-Fir 2 by 6', 'SYP', 'LVL', y 'framing' con madera más 'excluded' de otra cosa.
  - Falso FAIL sintético nuevo: un muro metálico con `framing` "…w/ 2x6 wood blocking…" o gauge "20 ga (2 x 4 blocking by GC)". Ningún canon real usa `framing` en walls[].

### 4. CE_PROTOCOLO_3H: `proceso_v119` / `arranque_rev_desde` / `tiempos_desde` / `_fin_dt` / `alarma_fallas(desde=)`: ROJO

Reproducción: `python3 -I /tmp/verif8/adv8/adv8_pm06.py <tools>`.

- **Q1b (regresión, bug de `tiempos_desde`):** `filas_tiempos` no devuelve la clave `linea`, así que se usa el fallback que borra TODA línea de tabla que contenga el texto del Fin exento.
  - TIEMPOS.md: `| 9 | Subida rev20 | 11-13 08:00 | 11-13 08:40 |` y `| 1 | Inventario rev21 | 11-13 08:40 | 11-13 09:30 |`; el arranque es 08:45 (log y VERSION_PROYECTO) y el paso 1 no tiene su `--paso`.
  - v137 da FAIL: "paso 1 cerrado en TIEMPOS.md sin su corrida … --paso 1".
  - El candidato da **PASS**: "1 paso(s) … son de una rev anterior". La fila del paso 1 (cerrado a las 09:30, después del arranque) se borró porque su Inicio "11-13 08:40" coincide con el Fin del paso 9.
- **Q4 (regresión):** `tiempos.log` con una sola marca tardía, `2026-11-13 13:50 | inicio rev21`, y VERSION_PROYECTO.txt fijado a las 22:00Z (14:00 PT). Los pasos 1, 2-3 y 4 cerraron entre las 08:30 y las 10:30 sin `--paso`.
  - v137 da FAIL (no cuadran, pasos sin marca).
  - El candidato da **PASS**: "3 paso(s) … son de una rev anterior".
  - "El más temprano de los tres" no protege si las tres fuentes son tardías, y nada comprueba que las filas exentas sean de verdad de otra rev (por ejemplo, su etiqueta revN o una entrega anterior).
- **Q2 (regresión):** el log sin marcas ISO, sin git, y VERSION_PROYECTO fijado al final.
  - v137 da FAIL: "la rev no se puede fechar".
  - El candidato da **PASS**: el sello de VERSION_PROYECTO basta para fechar y deja exentos todos los pasos.
- Q3 (sin tiempos.log) sigue dando FAIL en los dos.

### 5. CE_COBERTURA_DIAG: `cob_diag_cortos` / `_cob_discontinua` / `_cob_divisor_tag` / `_cob_en_hatch` / `_cob_familias` / `_cob_mismo_hatch`: ROJO

Reproducción: `python3 -I /tmp/verif8/adv8/adv8_cobdiag_cr.py`, con salida en `adv8_cobdiag_cr.out` y los pares en `cobdiag_cr_filtrados.json`.

- **Filtrados por hoja (119):** A2.01 38, A6.00 45, A6.01 20, A6.02 7, A7.30 4, A7.45 1, A7.50 3, A7.55 1.
- **Muestra:** 15 al azar (`random.seed(8)`), con recortes de ±3 ft (`pymupdf get_pixmap(clip)`) en `adv8/muestra_1.png` y `muestra_2.png`:

| # | hoja (x, y) | qué es | ¿muro real? |
|---|---|---|---|
| 1 | A2.01 (1591.4, 1022.6) | marco de la caja del tag XW.6.4 | no |
| 2 | A6.00 (537.2, 1205.2) | borde de la caja del tag CM.8 \| 2 | no |
| **3** | **A6.00 (404.0, 746.5)** | **dos líneas de muro cortado (1.56 pt de grosor, x 401.0 y 408.2, 4.8" entre caras, y 735.7→773, ~2.1 ft) que suben desde el muro del shaft del elevador de servicio (4/A6.00), pegadas a la caja del tag 'CM.8 \| 2'** | **SÍ** |
| 4 | A2.01 (1292.4, 930.6) | caja del tag '2' sobre el hatch de ladrillo | no |
| 5 | A2.01 (1437.1, 989.2) | caja del tag '4 \| 2' | no |
| 6 | A6.01 (799.6, 1110.0) | caja del tag FW.2 | no |
| 7 | A2.01 (1347.1, 885.3) | hatch de ladrillo | no |
| 8 | A2.01 (1544.3, 910.4) | hatch de ladrillo | no |
| 9 | A2.01 (1190.8, 993.0) | marco de la caja del tag XW.6.4 | no |
| 10 | A2.01 (1591.3, 1038.4) | marco de la caja del tag XW.6.2 | no |
| 11 | A6.02 (1188.9, 162.6) | cross-hatch dentro de un muro de CMU largo | no |
| 12 | A6.00 (1756.2, 495.5) | caja del tag FW.2 | no |
| 13 | A2.01 (1138.1, 920.4) | caja del tag '3 \| 0' sobre ladrillo | no |
| 14 | A6.00 (459.7, 746.8) | caja del tag FW.2 | no |
| 15 | A6.00 (1529.5, 1074.8) | cross-hatch en la esquina de un muro de CMU | no |

**Resultado: 1 de 15 es un muro real (#3), así que el arreglo 5 queda en ROJO.**

Cómo se perdió el #3 (`adv8_cobdiag_m3.py`, salida en `adv8_cobdiag_m3.out`):

- `_cob_divisor_tag({'x': 404.0, 'y': 746.5, 'largo_ft': 0.56, 'ang': 90.0, 'd': 8.52}) -> True`, por la regla (2), "palabra encerrada".
- La "línea paralela de largo parecido" que encuentra es el borde derecho de la propia caja del tag, x = 399.7, de y 741.5 a 751.6 (0.56 ft).
- El tag 'CM.8 \| 2' está a la izquierda, pegado al muro (r = 0.6 ft), y el filtro trata las caras del muro como si fueran el divisor de la caja.
- Es justo el caso que el docstring dice que no filtra ("un tag … suelto al lado de un muro real NO filtra"). El adv7 K3 no lo atrapó porque su tag 'F1' no tiene caja.
- `_cob_en_hatch` no tuvo que ver con este par.

Lo que sí está bien: los 4 furrings FALTA y K0–K4 siguen saliendo, y XF queda igual que en v137.

## Pendiente para COORDINACIÓN

- 4 renglones de mis corridas `--solo` en `/root/xf/work/entrega/compuerta_corridas.jsonl` (líneas 22–25, 10:11 UTC, tipo `rapida`, versiones v81cf137 y v81cf138). Son de esta verificación, no del proyecto; quitarlos o dejarlos lo decide COORDINACIÓN.
- No hice commit ni push. Todo el trabajo quedó en `/tmp/verif8/`: adversariales en `adv8/` y re-corridas de la verificación 7 en `adv7/`.
