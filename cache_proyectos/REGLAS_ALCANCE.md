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
