# REGLAS FIJAS DE ALCANCE (todos los proyectos)

## R-ALC-01 — Solo metal frame y gypsum board (usuario, 2026-11-01, VS #679 Downey)
- El alcance es SOLO cold-formed metal framing (studs, track, headers, bracing, blocking METÁLICO, clips) y gypsum board
  (board, trim, taping/finishing).
- MADERA = EXCLUIDA SIEMPRE (Div. 06): 2x joists / blocking / curbs (incluido RTU support en madera), FRT wood blocking,
  plywood, nailers, wood trim. Nunca se carga, nunca se lista con cantidad para decidir, nunca se hace RFI.
  Solo una nota directa en Scope Checklist: "EXCLUDED - wood framing / blocking (Div. 06), not in scope: <item> <N/HOJA>".
- Si un detalle da opción "metal o madera", se carga la opción metálica.
- Un RFI de estructura (p. ej. tipo de techo) solo si cambia una cantidad de metal o gypsum.
- Se suma a R80e.97 (trades que no hacemos: ACT, insulation, stucco, roofing, MEP, cabinets → EXCLUDED directo).

## R-ALC-02 — Blocking de accesorios sin medida impresa (usuario, 2026-11-01, VS #679 Downey)
- Blocking en wall para un accesorio cuyo ancho no está impreso: **3'-0" por accesorio × 2 filas (arriba y abajo) = 6 LF por accesorio**.
- Si el detalle imprime el número de filas (p. ej. "(3) ROWS"), manda el impreso: 3'-0" × filas impresas.
- Si el plano imprime el largo, manda el impreso.
- Aplica a accesorios sueltos (lavatory, TP, seat cover, towel, mirror, hooks, signage, coat rack…). Las corridas (cabinetry, shelving) van por su largo de corrida.
- Se carga directo, sin RFI.

## R-ALC-03 — Ductos siempre excluidos (usuario, 2026-11-02, VS #679 Downey)
- Framed openings / framing para ductos que cruzan walls o cielos: **EXCLUDED siempre**, en todos los proyectos.
- Nunca RFI: nota directa en Scope Checklist "EXCLUDED - framed openings for ducts (by others)".

## R-ALC-04 — Demolición de drywall y metal frame = NUESTRO alcance (usuario, 2026-11-02, VS #679 Downey)
- Corrige el error de excluir "demolición" completa: **la demolición de gypsum board y metal framing la hacemos nosotros** (por eso se leen los demo plans).
- Se cuantifica desde el Demolition Plan (keynotes + general notes): partitions a demoler (dashed), gyp bd ceilings / soffits, enclosures de columnas, furring a retirar, board existente a retirar para replace. Demolition SF = Length × Height × Layers (o área directa en cielos).
- Lo que no es nuestro trade (ACT, storefront, MEP, flooring, fixtures) sigue fuera; si una keynote mezcla ("gyp bd OR acoustical tile ceilings"), se carga lo de gyp / metal y se pregunta el resto.

## R-ALC-05 — Demolición de cielos existentes sin tipo indicado (usuario, 2026-11-02, VS #679 Downey)
- Si el demo plan pide retirar cielos existentes ("gyp bd OR acoustical tile") y no indica cuál es cuál (sin RCP existente ni tags): **EXCLUDED por falta de información**, con clarification "Existing ceiling demolition excluded – existing ceiling type not indicated; excluded for lack of information". Sin RFI; documentar el delta (área bruta).

## R-ALC-06 — Demolición: markup de línea, alturas buscadas y cruce demo vs floor plan (usuario, 2026-11-02, VS #679 Downey)
Para TODOS los proyectos:
1. **Markup de línea a escala:** cada elemento de demo (partition, column enclosure, furring, board de demising, cielo) se marca en el demo plan con una LÍNEA (PolyLine Bluebeam con /Measure calibrado y Depth = altura), Subject "DEMO", color propio en la leyenda, etiqueta DEMO ID · LF · H · SF · keynote/hoja. PNG por hoja + markups PDF (tool markups_demo.py).
2. **Alturas buscadas antes de suponer:** la altura de cada elemento demolido se busca en TODAS las hojas (notas generales y de demo, callouts de estructura / joists / beams, secciones y elevaciones existentes, RCP existente y nuevo, wall schedule (E), deck / bottom of structure, hojas S). Cada altura con #0: [CONFIRMADO N/HOJA] / [DERIVADO operación] / [PENDIENTE]. Solo si ninguna hoja la imprime: supuesto conservador + SEGUIMIENTO.
3. **Cruce demo plan vs floor plan nuevo** wall por wall: existe y queda / se demuele / nuevo / diferencias (walls demolidas sin marcar, existentes que no aparecen en el nuevo, nuevas sobre demolidas, demising que se conservan). Con eso se confirma o corrige la lista de demo; cada diferencia con N/HOJA + recorte circulado.

## R-ALC-07 — Altura de partitions existentes a demoler sin altura impresa (usuario, 2026-11-02, VS #679 Downey)
- Se cargan **hasta el B.O. de estructura impreso** de su bahía (o el más cercano impreso: joists / beams / deck del demo plan o S), **nunca a un cielo supuesto**. Estado DERIVADO con la cota usada; se documenta el delta contra ±12'-0".

## R-ALC-08 — Specs siempre revisadas (usuario, 2026-11-02, VS #679 Downey; TODOS los proyectos)
- En cada proyecto se barre el project manual o las spec sheets del trade (05 40 00 / 05 41 00, 09 21 16, 09 22 16, 09 29 00, 07 84 00, 07 92 00, 06 10 00, Div. 01 alcance / alternates / unit prices, notas de spec en hojas G / A-001 / A15.xx).
- Cada material cargado (gauge, depth / spacing, deflection track, board type / espesor, level of finish, trims / control joints, sealant, backing, demo) se cruza contra la spec y cita sección / párrafo en su fuente.
- Lo que plano y spec permiten aplicar juntos se aplica; conflicto = RFI A/B/C con delta. Si el bid set no trae specs, se declara en el Scope Checklist.

## R-ALC-09 — Hoja de datos del proyecto + hojas obligatorias revisadas (usuario, 2026-11-02; TODOS los proyectos)
- Arriba de todo en README_REVIEW.md y PARA_REVISAR, y en Inputs del Excel como renglones informativos (debajo de las filas fijas; sin hojas ni columnas nuevas): nombre y ciudad, dirección, tipo de proyecto, owner / tenant, arquitecto, GC, fecha de bid y bid set, SF total, pisos, Construction Classification, Occupancy Group, códigos (año), occupancy load, sprinklered, demo sí / no, specs en el set sí / no — cada dato con su HOJA o [PENDIENTE].
- Confirmar las hojas obligatorias revisadas (portada / índice, code analysis / G, notas generales, demo + notas, specs, partition types + detalles, floor plans, RCP, elevaciones / secciones, enlarged / elevaciones interiores, schedules, estructurales, MEP) y listar cualquiera no revisada.

## R-ALC-10 — Conflicto plano vs spec / código: manda el PLANO (usuario, 2026-11-02; TODOS los proyectos)
- Se carga lo del PLANO (opción A) y el renglón lleva una nota: "Estimator decision (option A, drawings govern). Spec / code says <…> (sección / párrafo); delta <…>. Verify at <N/HOJA> and spec <sección>" — con la hoja y la sección exactas donde ir a investigar.
- El RFI se cierra como "estimator decision (option A)" y la nota aparece en Pending / Scope Checklist, SEGUIMIENTO y PARA_REVISAR.

## R-ALC-11 — Lo que el plano no dibuja NO se omite (usuario, 2026-11-02; TODOS los proyectos)
- Textual: "si no lo dibuja, es porque está en otro lado, busca siempre en los spec sheets, metal schedule, o en el structural, pero no se puede ir sin esa información".
- Un elemento que el RCP / floor plan no dibuja se busca en: specs (sección / ¶), metal stud / framing schedule, hojas estructurales (S), detalles típicos (A12.xx). Se carga con su fuente y la nota: "Not drawn on <hoja>; required by <spec ¶ / N/HOJA>. Verify at <hojas>".
- Si el detalle impreso y la spec difieren, se aplica el MÁS ESTRICTO impreso y se anota el delta.
- Solo si no existe en ningún lado = RFI con supuesto conservador CARGADO (nunca "not carried").
- Compuertas: reglas.py A_BARRIDO_NO_DIBUJADO (BE-116, renglón en 0 sin barrido) + A_NO_DIBUJADO (cierre de RFI "not carried … not drawn"), ambas en v81cf4.
- Caso origen: VS Downey RFI-31, lateral bracing de los drywall grid ceilings (092900 ¶ N.1 + J/A12.02 + K/A12.02).
