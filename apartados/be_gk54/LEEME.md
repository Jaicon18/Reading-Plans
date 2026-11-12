# BE-GK54 — chequeo + test (para unir en la próxima versión del skill, tools/)

Error (Grand Kia rev3a, U-193 rojo M-A111-29, 12-nov): A-Z1-20 se metió en `excluded_walls` como
"same single wall as A1-Z1-08". A111 y 1/A150 dibujan dos leaves (x1503.8-1507.6 y x1509.0-1512.8) con un gap de 2" y
dos tags (A y A1). Eso son dos walls, y faltaban 4.00 LF de type A.

Regla: dos bandas paralelas con un gap impreso, o con dos tags, son dos walls. Para meter uno en `excluded_walls` como
"same wall" hay que probar que el gap no existe (`gap_proof` con N/HOJA).

- `be_gk54.py::fallas(canon, filas_COBERTURA, to_canon=...)`: da FAIL cuando una exclusión "same (single) wall as X" sin
  `gap_proof` tiene en el mapa de cobertura una banda ROJA paralela a la de X, en la misma hoja, a no más de 14" más el
  espesor de X y solapada con ella.
- CLI: `python3 be_gk54.py <canon.json> <Auditoria/COBERTURA.csv> [markups.pdf]`. El PDF convierte los puntos
  renderizados a puntos sin rotar con `page.rotation_matrix`.
- Test: `python3 test_be_gk54.py`. Usa el caso real M-A111-29 en coordenadas rotadas 270. También prueba que pasa con
  CUBIERTO, que pasa con `gap_proof` y que no revisa otras exclusiones.

Para unir: copiar ambos archivos a tools/, llamar `fallas` desde compuerta_entrega (después de la cobertura U-193) y
agregar el token del test a test_compuerta_entrega.py.
