# v81cf138 ANGOSTA (candidato, sin publicar): solo lo que necesita CR rev20c

Orden de COORDINACIÓN 13-nov 09:50: v138 = v137 + 5 arreglos, nada más. Los 7 STILL-WEAK del post-mortem y la base ancha van a v139 (apartados/v81cf139_wip/).

Parche: `v81cf138_desde_v81cf137.patch`. Archivos que cambian: compuerta_entrega.py, test_compuerta_entrega.py, chequeos_biblioteca.py (SOLO be_cf04), runner/completitud.py, REGLAS_REGISTRO.json, SKILL.md. verificar_version y las órdenes: igual que v137 (más la entrada BE-XF18 del registro).

| arreglo | qué | test |
|---|---|---|
| BE-XF18 | PDF de markups por nombre (entrega.json 'markups' o el '… - OPEN IN BLUEBEAM.pdf' de la rev en curso, la del Excel de Take-off/ más nuevo); nunca 'IMAGE ONLY' / mapa; 'markups' inexistente, ninguno de la rev en curso o ambigüedad = FAIL con la causa (CE_PDF_MARKUPS_ELEGIDO) | test_be_xf18_pdf_markups_por_nombre |
| CB_BE_83 | existing_walls con 'faces' numérico = una cara (cuarto del location); 'faces: exterior; 905 GUEST' juzga la cara interior; 'underside of ceiling' no justifica, sí roof / floor / structure / deck / sheathing / joist / framing, 'floor to floor', 'stair enclosure' | test_v138_be83_faces_numero |
| CB_BE_CF04 | PASS sin '0 walls' (red U-138); madera: '2 X 6', '2x6', '2×6', '2 x 4', 'DF stud', 'Douglas fir', 'SPF', 'timber', 'wood' = FAIL | test_v138_cf04_wood_board_only_plausible |
| CE_PROTOCOLO_3H | rev que arrancó después de v119: solo se juzgan sus pasos; arranque = el MÁS TEMPRANO de la marca del log, el sello de VERSION_PROYECTO y git (arranque_rev_desde) | test_v138_protocolo_rev_posterior_solo_sus_pasos |
| CE_COBERTURA_DIAG | discontinuos fuera; hatch solo si es el MISMO a los dos lados (ángulo, estilo, espaciado) o cross-hatch dentro de la banda; tag solo con la palabra encerrada en caja o palabras a los dos lados | test_v138_cob_diag_familias_cr (+ K2-K4 de la verificación 7) |

Medidas: CR rev20b no cubiertos 478 → 357; los 4 furrings FALTA contra CMU siguen saliendo; XF: el caso real de la puerta 103 sigue saliendo.
Validación: suite 47/47 · banco 0 distintas (8) · XF 0 regresiones (231 / 12 / 0) · reglas 0 sin clasificar · 199 archivos.
Pendiente: verificación 8 (solo el diff), PRUEBA_ABIERTOS de GK y de CR, aprobación de COORDINACIÓN.
