# tools_post_v81cf94_CR — parche de CR City Hotel rev19 para la UNIÓN (la hace Xfinity, U-144)

No es una versión publicada. INDICE.md y VERSION_EN_CURSO.md NO se tocaron.

## Contenido
- `parche_v81cf94_a_CR-rev19.patch`: diff unificado v81cf94 (zip publicado) → skill con el que CR rev19 pasó la compuerta (213 PASS / 4 AMBER / 0 FAIL).
- `candidato_v94_mas_CR-rev19.zip`: v81cf94 + este parche, 199 archivos (zip -D). verificar_version: 0 faltantes de 906; suite 47/47; banco 0 familias distintas (HF, B&N, CC, VS rev17: 116 familias c/u; BOA da el mismo error de canon en la ref v81cf94 y en la candidata).
- `tests/`: copia de las 3 tools cambiadas y de sus 3 archivos de test.

## Cambios
1. **U-177 CE_RCP_CONTORNO** (compuerta_entrega.rcp_contorno_fallas): cobertura < 0.5 = FAIL aunque diga [EDGE NOT DRAWN]; pasa solo si el polígono declara `source <HOJA> offset (dx, dy)` y en esa hoja (restando el offset) coincide, o si el borde lo comparte otro polígono de take-off de la misma página. Test: test_compuerta_entrega::test_u177_rcp_contorno_duro.
2. **comparar_alturas multinivel**: constants.deck_heights por nivel = tope físico (H <= B.O. del nivel); lee walls + existing_walls; salas desde `location`; muros de madera sin exigencia de slip track; `1/4"` (pulgada en fracción sola) en el cierre. Test: test_comparar_alturas::test_alturas_multinivel_cr.
3. **BE-CR32** (revision_markups.altura_impresa): "printed <cota>" seguido de cross-check / check / verified = manda la cota impresa (el parser BE-GK28 tomaba la medición vectorial). Test: test_hoja_sufijo::test_be_cr32_impresa_sobre_crosscheck.
4. **BE-CR33** (comparar_alturas): height_diff_reason con hojas con punto / guion (A7.05, 4/A5.05) cuenta como N/HOJA; en el cruce cuarto-type los renglones con motivo impreso quedan explicados (falla si los renglones SIN motivo tienen alturas distintas). Tests: test_comparar_alturas::test_be_cr33_motivo_hoja_con_punto, ::test_be_cr33_cruce_tipo_explicado.
5. **BE-CR34 CE_GAUGE_IMPRESA** (compuerta_entrega.gauge_impreso_fallas / ce_gauge_impreso): "gauge not printed" en un renglón del Material Summary o en un RFI con un STUD SCHEDULE (MIN. GAUGE) impreso en el set = FAIL (U-171). Test: test_compuerta_entrega::test_be_cr34_gauge_impreso.
6. Registro del skill: + BE-CR32, BE-CR33, BE-CR34 (programa, con chequeo + test) y BE-XF10 (conducta, para cerrar verificar_version). SKILL.md: párrafo de versión (dice "v81cf95"; renumerar en la unión).

## Para la biblioteca (BIBLIOTECA_ERRORES.md) y el registro de órdenes — NO se escribieron aquí
- BE-CR32: el parser de altura impresa tomaba la comprobación vectorial en vez de la cota impresa.
- BE-CR33: hojas con punto no se reconocían en height_diff_reason; el cruce exigía motivo a todos los renglones.
- BE-CR34: "gauge not printed" con un STUD SCHEDULE impreso en A0.06; lecciones de la auditoría U-181: altura de una ELEVACIÓN solo si en planta el wall está en ese plano frontal (CR east facade L4); exclusión tenant solo de caras de types NO rated (U-159).

## BE-CR35 — CR City Hotel rev19 (12-nov, usuario revisando ALTURAS_REVISADAS página 0.917)
- Los 14 renglones de soffits / beam wraps (SOF-*, BW-L1-RETAIL; Depth = ancho desarrollado del board, no altura de wall) entraron a ALTURAS_IMPRESAS como "[take-off detail reading, not blind]": NO pasaron por la doble lectura ciega U-176 (1) (H-A / H-B solo leyeron walls), y la imagen de 0.917 solo circulaba una cota del RCP. Regla: TODO renglón con Depth en Bluebeam (walls, soffits, bandas, beam wraps) pasa por H-A / H-B; un renglón "not blind" = FAIL (candado en v98, COORDINACIÓN). La página de cada ancho desarrollado lleva TODAS las cotas de la operación circuladas (RCP + detalle) y el texto "developed width per LF ... Depth in Bluebeam = board strip, not a wall height".

## BE-CR36 — CR City Hotel rev19 (12-nov, U-187 CE_TEXTOS_LEGIBLES sobre el PDF de markups) — carpeta BE-CR36/ (parches contra v81cf98)
- A7.50: dos EXCLUDED de cuartos vecinos (118B DATA / 119 TOILET, mismo texto 'lay-in ACT ceiling (ACT-2)…') se encimaban 0.9 pt: markups_rcp.aplicar esquivaba el texto impreso pero no los FreeText ya puestos. Arreglo: caja_interior también evita los FreeText de la hoja (+2 pt).
- LEGEND: celdas de type largas ('CH.6-2 - SHAFT WALL …') a 10 pt fijos encima de las columnas Walls / LF. Arreglo: markups_bluebeam.celda_legible (baja la letra hasta caber, mínimo 5.5 pt; si no, recorta con '...'; el type completo queda en el Subject).
- Test: test_compuerta_entrega::test_be_cr36_textos_markups (celda larga cabe; dos cuartos vecinos sin FreeText encimados).
- BE-CR36b (12-nov, corrida rev20): celda_legible NO recorta ('...'): markups_bluebeam.verificar exige el type completo en la leyenda ('FALLA leyenda: falta el type CH.6-2 - …'); baja la letra hasta 3.5 pt. Parches contra v81cf100 en BE-CR36/*.v100.patch.
