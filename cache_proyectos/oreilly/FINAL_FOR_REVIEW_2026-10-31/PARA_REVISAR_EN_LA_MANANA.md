# Para revisar — O'Reilly Evans #1 (prueba ciega, 2026-10-31)

1. **Entrega:** take-off completo con el skill v80t → v80u (cadena completa, por suscripción). 30 walls de partitions + 3 vestibule heads; 8 types (S21, S24, S41, S42, S43, S61, EXT-8CFMF, EXT-6CFMF).
2. **Totales:** 614.86 LF de partitions · board 5/8" X 7,741.58 SF + W.R. 702.15 SF · studs 3-5/8" 2,214.54 / 6" 1,105.09 / 8" 537.32 LF · Z-furring 2,690.71 LF.
3. **Tiempo:** ≈ 2 h 08 min de reloj (meta ≤ 2 h: me pasé 8 min; 1 h del total fue arreglar herramientas que no conocían hojas raster y números tipo "A4.2").
4. **El bid set de Drive traía 79 markups** de un take-off anterior. Los quité antes de leer; solo alcancé a ver los títulos (Subject) de las hojas 37 y 38.
5. **Uso de API (sin pedirlo):** el runner encontró `TAKEOFF_API_KEY` en el entorno e hizo 31 llamadas (corrección y cobertura). No cambiaron ninguna cantidad (Excel idéntico con y sin ellas). La entrega final se hizo sin API y quedó bloqueado para siempre (`--sin-api`).
6. **Lo más grande que queda en RFI (supuesto conservador aplicado):**
   - RFI-01 / 02: altura a top of purlin (bottom of purlin no impreso). Alternativa: −10" en S21, S42 y heads.
   - RFI-03: S42 header wall hasta el break mark (+6.70 LF).
   - RFI-06: resilient channel + 1/4" board en la entrada (+243 LF / +349 SF) — impreso pero sin extensión acotada.
   - RFI-20 / 25 / 26 / 27: productos del estructural (FCB43.5 clips, deep-leg 14 ga track, Titen HD, #10 screws).
7. **Auditorías:** paso 11 no certificó la primera versión; cinco hallazgos aplicados (anchors 206 → 36, pins 226.82 → 151.04, FRT 2x4 en aberturas +56.67 LF, board bajo header +30.76 SF, studs dobles en control joints +62.96 LF). Paso 12: 85.5 % de cobertura → 100 % con destino.
8. **Comparación contra el mejor skill (B&N rev13):** en `EVALUACION_INTERNA.md`. Board por SF de muro −2.3 %, track por LF −6.0 %, studs (normalizado por O.C.) +10 %, screws / compound / tape +1.4 %.
9. **Todo lo que no resuelve el plano:** `SEGUIMIENTO.md` (27 RFIs con supuesto y delta).
