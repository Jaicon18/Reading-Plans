# Prueba de costeo vía API — B&N Colorado Springs (referencia: rev13)
Objetivo: costo de un take-off SIN errores y si el servicio vale la pena.
Topes: $45 total (de $50); cada paso con --max-budget-usd propio; al llegar al tope se detiene y se reporta.
Modelo por paso: Sonnet por defecto (lectura, conteo, medición, pasadas de revisión); Opus solo resolución y revisión final, y solo si Sonnet falla contra rev13.
Pasadas: EXACTAMENTE 2 (decisión del estimador 28-oct). Después de la 2.ª se detiene y entrega resultados; no hay 3.ª.
Entregables: costos.csv (USD, tokens, tiempo por paso), % por material vs rev13, lista de diferencias, costo por SF/LF, resumen para la landing page.
Pendiente: permiso para correr claude -p con la API key sin preguntas (bloqueado por auto mode).
Reporte: separar diferencias por importancia (framing/board/trim principales vs tornillería y fasteners pequeños), para que el estimador decida si los fasteners se quitan del take-off.
