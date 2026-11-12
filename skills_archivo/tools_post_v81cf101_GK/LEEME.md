# Parche Grand Kia para v81cf102 (sobre v81cf101)
- BE-GK39 (U-187): compuerta_entrega.hueco_etiqueta — si ningún candidato está libre de TODA anotación (etiqueta dentro de un Square grande de destino), segunda pasada libre solo de FreeText: nunca texto sobre texto. GK rev2 DETALLES_REVISADOS 345 encimados -> 0.
- BE-GK39 (U-187): markups_rcp.py excluded — la etiqueta EXCLUDED esquiva las FreeText ya puestas; si choca, se desliza dentro de la caja del cuarto y, si no cabe, se reajusta al hueco libre más grande. GK rev2 markups 5 -> 0 (cuartos 145/146/147 con un mismo polígono).
- BE-GK40: pregunta_ciega.py (nuevo) — la pregunta ciega pide la MISMA magnitud que mide el Depth cargado (joist LENGTH, developed width, stud height, face height, return depth), con su definición; `revisar` marca la fila que pide otra cosa (GK EXT-07 pidió 'depth of the joists' con 0.82 = largo).
- Test: test_be_gk39_40.py (test_be_gk39_hueco_dentro_de_square, test_be_gk40_pregunta_misma_magnitud) — OK.
