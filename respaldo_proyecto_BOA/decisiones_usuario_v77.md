# Decisiones del usuario para v77 (20-oct, sesión Bluebeam una por una)

## 6a ATM extra framing (resuelta 20-oct ~12:20 p.m. LA)
Usuario: "medí toda la pared diagonal donde está la ATM, ahí ya está todo el metal que se ocupa, ya no hay que añadir nada más, ni para la sistered wall, y todo va desde el piso al deck con top and bottom runners".
Regla genérica: el framing del ATM recess = la wall completa donde está el ATM (todo su largo), studs de piso a deck + bottom runner + top runner. NO sumar sistered studs ni filas de furring aparte. Ese wall se cuenta una sola vez (no duplicar con su partition type).

## 6b header / box beam (en curso 20-oct ~12:30 p.m. LA)
Usuario: "esta box beam está hecha con 4 studs, multiplicado por lo largo".
Regla genérica: box beam = 4 studs × largo. OJO: la referencia v4 (305.63) suma cada largo UNA vez (sin ×4) y el office front lo toma por abertura 6 × (7.5 + 1.333) = 53.00. Pendiente: largo del CONT. BOX BEAM (continuo vs por abertura) y si la referencia se corrige a ×4.
- 20-oct: CONT. BOX BEAM del office front = opción B CONTINUO (primera a última jamb de cada frente + 1'-4") × 4. Correcta según el usuario. La referencia debe corregirse (53.00 por abertura sin ×4 → continuo ×4).
- 20-oct: "los box beam llevan 4, los headers usualmente llevan 2 piezas, míralo en el schedule". 7/S5.20 HEADER SCHEDULE - WALLS [CONFIRMADO, imagen s520/header_schedule_7-S5.20.png]: non load brg interior <=3'-4" SINGLE TRACK 18 GA; <=6'-0" DOUBLE TRACK 18 GA; <=8'-0" 2-362CSJ20; load bearing todos "2-...". Regla: box beam/box header ×4; header × piezas del schedule (2 salvo single track). Pendiente: doors R.O. 3'-4" (single track) ¿1 o 2?
- 20-oct ERROR MÍO: pregunté algo que el plano ya contesta (single track ≤3'-4"). Usuario: "léelo y haz lo que ellos te dicen". REGLA: cuando el schedule/detalle impreso da la respuesta, se aplica sin preguntar (E23). Doors R.O. ≤3'-4" = SINGLE TRACK = 1 pieza (7/S5.20).

## 6c 3/4" FRT plywood at storefront piers (en curso)
Leído por mí 1/A09.25 y 2/A09.25 [CONFIRMADO, imágenes s520/pier_*.png]: "3/4" FRT PLYWOOD" solo como strip en cada jamb del storefront (2 por pier); las caras del pier = "CONTINUOUS AWB ON 5/8" FRT PLYWOOD BONDED TO POLYISO" (nailbase) + 5/8" gypsum board. Regla: las caras del pier NO van en el renglón 3/4" FRT plywood. Ancho del strip NO impreso → pregunta al usuario.
- 20-oct: usuario "tú mídelo y eso dale". Medido por geometría vectorial del PDF a la escala impresa 1 1/2" = 1'-0" (108 pt/ft; comprobado: espesor del ply dibujado 6.72–6.84 pt = 0.75"). Strips [DERIVADO]: 2/A09.25 G-jamb 0.759 ft, F-jamb 0.500 ft; 1/A09.25 F-jamb 0.759 ft, G-jamb 0.758 ft; suma 2.776 ft × T/GLAZING 8'-6" [CONFIRMADO A09.01] = 23.59 SF (1 ply). Dibujo muestra 2 capas de 3/4" con rótulo singular → se lleva 1 ply + RFI delta +23.59 SF si son 2. Imágenes s520/pier_*_marcado.png. Regla genérica: el strip de plywood en jamb se mide del detalle (vector a escala impresa, verificado con un espesor/cota impresa) y × alto impreso; las caras del pier no entran.

## 6d sill track (resuelta por el plano, sin pregunta)
2/S5.20 HEAD TRACK @ NON LOAD BRG [CONFIRMADO, imagen s520/head_2-S5.20.png]: "ADD FULL LENGTH ADDL HEAD TRACK @ OPNG >4'-0"" + NOTE "INVERT DETAIL FOR SILL CONDITION" → sill de abertura > 4'-0" = doble track. Regla: sill track = (R.O. + 1'-4") × (2 si R.O. > 4'-0", si no 1), solo aberturas con sill. Con los R.O. de la referencia [DERIVADO]: GL-2 6 × 9.333 × 2 = 112.00 + walk-up ATM 3.58 + drive-up ATM 3.51 + ductos 2 × 2.333 = 4.67 → 123.76 LF (la referencia 67.76 no duplicaba; las pruebas ~119 iban bien).

## Track de ceilings en bordes de transición (resuelta por el plano)
7/A09.33 TYPICAL CEILING TRANSITION DETAIL [CONFIRMADO, imagen s520/transition_7-A09.33.png]: framing vertical desde estructura (3 5/8" kicker @ 48" O.C.) con 5/8" gypsum board y retorno de 6"; el ceiling programado remata con SHADOW MOLDING, sin track propio en ese borde. Regla (= R73.16/R76.6): en un borde de transición NO se suma track de perímetro del ceiling; solo el track de la transición. Referencia 1,323.03 → 1,246.00 (−77.03).

## ⚠ Interpretación de D1 por el arbitraje #25 (pendiente de confirmar con el usuario, 21-oct 5:20 p.m. LA del 20)
El árbitro leyó D1 como: extra framing ATM = la wall del ATM completa (studs 338.47 + 2 runners × 21.46 = 381.39 LF), y sacó esos LF de 6" stud y bottom/top track para no duplicar. Referencia v5 = 381.39.
Lectura alternativa: "ahí ya está todo el metal, ya no hay que añadir nada más" = la wall ya está en su partition type y el extra framing ATM = 0 (o se queda en la wall). PREGUNTAR antes de lanzar #26.
- 20-oct 6:30 p.m. LA: revisé A02.01 (imagen s520/ATM_paredes_marcado.png). La "pared diagonal donde está la ATM" del usuario es la wall diagonal a 60° del 24 HR Vestibule 101 (tag F, walk-up DAY 1 ATM, 1/A08.11). El árbitro #25 tomó OTRA wall: la exterior de grid 2 (drive-up, 7/A08.11), 21.46 ft → 381.39. Muy probablemente v77/ref v5 tienen D1 en la wall equivocada. Preguntado al usuario; NO lanzar #26 hasta respuesta.

## Respuestas 20-oct ~8:30 p.m. LA ("tú estás en lo correcto, es 82.23 y 84.04, sí como hace la roja")
- A1: correcto lo de las pruebas (rojo): el wall Corridor 111 / Break Room 118 + Electrical 120 + NER 121 incluye el tramo de la door 118B (20.52). A1 total aceptado 82.23–84.04 LF. Regla: el largo del wall corre a través de los openings de door hasta la esquina/intersección.
- ATM: la pared es la ROJA = wall diagonal a 60° del 24 HR Vestibule 101 (tag F, walk-up ATM, 1/A08.11). El árbitro #25 se equivocó de wall (tomó la exterior de grid 2). Corregir en v77b; la referencia del usuario 109.87 corresponde a esa wall diagonal.
- 20-oct ~8:30 p.m.: usuario "haz una pregunta a la vez" + "no me des tanta información porque me saturas" → REGLA: mensajes cortísimos, una sola pregunta, sin tablas largas ni resúmenes extra.
- Lanzado arbitraje #25b → v77b (session_01BSzBZ66nEqYFGXCnQmszfx) para corregir la wall del ATM y A1.
- G: wall ATM Room 102 / Office 5 CB 109 = 12'-4" (12.333), no 11'-7 1/2". Usuario 20-oct ~8:40 p.m.
- G: wall Office 6 CB 110 / Women's Restroom 114 = 12'-4" (12.333). Usuario 20-oct.
- G1: return office front Office 5 CB 109 / Office 6 CB 110 = 3'-6" (3.507). Usuario 20-oct.
- G1: return sur office front Office 6 CB 110 (sin tag) = 3'-2" (3.18). Usuario 20-oct.
- B2K: 1'-9 1/4" (1.773). Usuario 20-oct.
- EXT 6": fachada norte (grid F, Office 1 ME 105) = 13.19 LF (pruebas), no 14.95. Usuario 20-oct.
- 3-5/8" stud: correcto ~6,690 LF (pruebas): se suman studs extra en esquinas y en intersecciones T. Usuario 20-oct.
- ⛔ ACOUSTICAL SEALANT: EXCLUIRLO en TODOS los proyectos (usuario 20-oct ~9 p.m.). Fuera del take-off, del Excel y de la calificación (modo excluir).
- ⛔ MARKUPS BLUEBEAM (usuario 20-oct ~9:15 p.m.): entregar SIEMPRE, en todos los proyectos, un PDF del bid set con markups reales de Bluebeam por wall (color por partition type; subject = type; LF y N/HOJA en el markup; visibles en Markups List, editables). Implementar en v78 (después de #26); verificar que funcionan en Bluebeam antes de volverlo regla fija.
- ⛔ REGLA PERMANENTE (usuario 20-oct ~9:40 p.m.): SIEMPRE una pregunta a la vez, y antes decir el total ("tengo N preguntas en total, te las haré una a la vez"). También en el skill: preguntas al estimador = total anunciado + una por turno. Usuario: "haz lo que creas más importante para que aprendas solo" (autonomía).
- 20-oct ~9:45 p.m.: arbitraje #25b (v77b, carpeta 1jhVo0aUD9boVCYfaQcYprOTnoVUyXAZJ; dev 1nEqzOzOlnJ2QAwYyz6MwpBxtMz23q7ap md5 afdd7e6a37fc03b59e8f5d2a782b90fa; ciego 104p4dhMr-0YB3aCcvpGGgPrFi7qFxGNH md5 c6f319b0a4cd2dbeff858bc700473de5; SKILL ciego 87ad9f65fad855f68f2f6b9ce2dadf0d) NO aplicó los send_message (G/G1/B2K/EXT/stud/sealant/preguntas) → van en v77c en el prompt inicial. Hallazgo: wall diagonal F completa = 340–356 LF; el 109.87 de la referencia v4 = 49.87 (sistered+furring drive-up 6/A08.11) + 60.00 (walls G/G1), NO es la wall F. Lectura probable del usuario: la wall F ya en su type tiene todo el metal → extra framing ATM = 0. PREGUNTAR (1 pregunta).
- 20-oct ~9:50 p.m.: ATM extra framing = 0 (la wall F diagonal ya tiene todo el metal en su type F). Usuario: "perfecto".
- ⛔ PROCEDIMIENTO DE REVISIÓN (usuario, permanente): revisar con el estimador empezando por el FLOOR PLAN, partitions en ORDEN ALFABÉTICO (A1, A1K, A5, B, B2, B2K, C1, EXT…, F, G, G1…), y al terminar el floor plan seguir con los DETALLES que marca el floor plan, en orden. Igual que en BOA. Una pregunta a la vez con total anunciado.
- 20-oct ~9:15 p.m.: v77c listo (carpeta 'ARBITRAJE 25c y PAQUETE v77c'; dev 1xZZFbo2cgHKvbKOb7Y22bVjBzUeD4fSx md5 93d2ed3fc48b2f870646dde430e995da; ciego 1ktTbr4UvIGQbiud694CXiEiTSOaa1MUb md5 6f7ad5e71b133f43b64ada9821ed550f; SKILL ciego def2b9647bdae33dfce37a885c2395ec). 25A 95.6 / 25B 96.5 vs ref v7 (rearmados). PARA REVISAR (2): 6/A08.11 imprime sistered+furring drive-up (+49.87 si se carga); parapet norte sigue 14.95 (−1.76 si sigue a la wall).
- 20-oct ~9:25 p.m.: SÍ contar sistered 2 1/2" + furring del drive-up impresos en 6/A08.11 (+49.87 LF). Regla genérica: si un detalle IMPRIME sistered/furring en un ATM o recess, se cuenta (extra framing = lo impreso); si no imprime nada, 0. → v78 / ref v8.
- 20-oct ~9:30 p.m.: parapet sigue el largo de la wall exterior de su fachada (norte = 13.19, −1.76 LF parapet track). Regla genérica: parapet LF = LF de la wall exterior debajo (salvo detalle que diga otra cosa). → v78 / ref v8.

## 22-oct — REGLA INVIOLABLE (usuario): markups Bluebeam
El usuario abrió BOA_Broomfield_29A_markups.pdf en Bluebeam: "los mark up están perfectos". Desde ahora, en TODOS los proyectos, las marcas se entregan EXACTAMENTE así: anotaciones PDF reales, editables en Bluebeam y visibles en la Markups List (markups_bluebeam.py v80), una por wall/elemento. Regla inviolable, con compuerta (sin markups editables verificados no hay entrega).
- 23-oct: usuario preguntó si los markups están a escala. Hallazgo: markups_bluebeam.py v80 dibuja line/polyline en la posición real con el LF en Contents, pero SIN /Measure ni /IT de medición → Bluebeam no mide su largo. Pedido al árbitro #29 (v81): viewport /Measure con la escala impresa por hoja + markups de medición (LineDimension/PolyLineDimension) + compuerta ±1 % contra el canon.
- 23-oct CIERRE P1: glass mat = ~350 SF (lo que encuentran las pruebas). El 15/A09.27 drive-up canopy NO lleva glass mat. Ref 462 queda corregida a ~350.
- 23-oct CIERRE P2: CSR soffit 10/A09.33 = studs verticales 3-5/8" @ 16" O.C. + 2 tracks (top y bottom) a lo largo del soffit. Regla genérica para todo framed soffit.
- 23-oct REGLA: todo entregable se guarda SIEMPRE en Drive: Shared drives › Drive › Claude outputs (donde siempre). Dar ruta carpeta por carpeta.
- 23-oct REGLA INVIOLABLE (usuario): de aquí en adelante YO subo todo entregable a su lugar en Drive (Claude outputs / carpeta del proyecto), sin que el usuario tenga que hacerlo. Si el archivo es grande, lanzar una sesión remota del entorno (tiene gdrive_fetch.py put). Siempre dar ruta carpeta por carpeta.
