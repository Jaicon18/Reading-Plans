# Prueba de costeo vía API — B&N Colorado Springs (referencia: rev13)
Objetivo: costo de un take-off SIN errores y si el servicio vale la pena.
Topes: $45 total (de $50); cada paso con --max-budget-usd propio; al llegar al tope se detiene y se reporta.
Modelo por paso: Sonnet por defecto (lectura, conteo, medición, pasadas de revisión); Opus solo resolución y revisión final, y solo si Sonnet falla contra rev13.
Pasadas: 1, 2, 3… mientras cada pasada encuentre errores nuevos vs rev13 y haya saldo.
Entregables: costos.csv (USD, tokens, tiempo por paso), % por material vs rev13, lista de diferencias, costo por SF/LF, resumen para la landing page.
Pendiente: permiso para correr claude -p con la API key sin preguntas (bloqueado por auto mode).
