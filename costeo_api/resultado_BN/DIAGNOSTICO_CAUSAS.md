# Diagnóstico de causas — prueba API B&N (pasadas 1 y 2) vs rev2 (skill, antes de decisiones) y rev13 (final)
Sin gasto adicional de API: análisis sobre los Excel ya generados.

| Material | rev2 | rev13 | Pasada 1 | Pasada 2 |
|---|---|---|---|---|
| Stud 3-5/8" LF | 10,120 | 11,663 | 7,858 | 7,858 |
| Stud 6" LF | 2,900 | 3,162 | 2,227 | 2,227 |
| Blocking LF | 552 | 568 | 104 | 173 |
| W.R. SF | 1,024 | 1,093 | 874 | 874 |
| Plywood 5/8 SF | 2,528 | 2,686 | 1,409 | 1,350 |
| FRP SF | — | 2,001 | 998 | 959 |
| Drywall screws | 19,875 | 18,431 | 17,936 | 7,397 |
| Pins | 634 | 389 | 393 | 786 |

Causas (de mayor a menor peso):
1. Las corridas por API NO aplicaron las reglas del skill v80s ni los precedentes (R80e.34): "where shelving occurs" una cara todo el largo (FRP/plywood types 3/4 ≈ 937 SF c/u), header track en toda puerta (la pasada 2 lo QUITÓ), blocking por filas del detalle (stock room 7/A-413 ≈ 387 LF no contado), W.R. en todas las caras de wet rooms, deck 25'-0". → el skill no se le pasó completo a cada llamada `claude -p` (cada paso recibió contexto parcial).
2. La pasada 2 (revisión) introdujo regresiones: drywall screws 1.2/SF → 0.46/SF (pisó el yield del estimador), pins a 2 hileras (pisó la decisión de 1 hilera). Una revisión no debe contradecir reglas del skill ni decisiones del estimador.
3. Cadenas de detalles no seguidas → elementos de framing faltantes: diagonal braces 3/A-410 (~512 LF), cross members 8/A-410 (~550 LF), nested bracing (~129 LF), soffit cross bracing (90 LF).
4. Alturas 23'-0"/23'-8" en vez de 25'-0" (decisión de deck) → −6 a −8 % en studs y board de type 2.
Conclusión: el problema no es el modelo ni la lectura del board (−0.2 %); es cómo se armó la corrida (skill y reglas no cargadas en cada paso + revisión sin candados). Corregir antes de gastar en otra prueba.
