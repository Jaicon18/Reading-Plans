# BIBLIOTECA DE ERRORES — pruebas que se corren en TODO proyecto (Paso 12 b)

Cada error confirmado en un proyecto (BOA Broomfield, B&N Colorado Springs, …) es una PRUEBA. En el Paso 12 de cada
entrega se corren TODAS contra el Excel + markups + planos del proyecto, con resultado **PASS / FAIL / N/A** y evidencia
(N/HOJA + recorte circulado). Un FAIL bloquea la entrega hasta corregirse; un error nuevo se agrega aquí el mismo turno.

Formato de cada prueba: **ID · origen · qué falló · cómo se prueba · criterio PASS**.
Los términos del trade van en inglés.

## A. Lectura del plano (detalles, notas, capas)

| ID | Origen | Qué falló | Cómo se prueba | PASS si… |
|---|---|---|---|---|
| BE-01 | B&N rev4 (auditor) — R80e.25 c | Fire-stop track "METAL STUD/TRACK FIRE STOP AT CEILING LINE, TYP." (8/A-410) no se había cuantificado | Buscar en el set todo detalle de top track / ceiling line con "FIRE STOP" o "TYP."; en el Excel debe existir el track de fire stop por tamaño de stud, sobre los walls a deck con ceiling en al menos una cara, + RFI de confirmación | Hay renglón (o parte de renglón con desglose) por tamaño, LF ≤ Σ LF de walls a deck de ese tamaño, y RFI/nota que lo cita |
| BE-02 | B&N rev4 (auditor) — R80e.25 a | Nota "W.R. … FOR WALL AND CEILING CONSTRUCTION" aplicada solo a walls | Leer las partition notes / specs de W.R.; si dicen "ceiling", los GWB ceilings de esos rooms van en W.R. | El desglose del board W.R. incluye los GWB ceilings de cada wet room con GWB ceiling (los de ACT no) |
| BE-03 | B&N rev1–rev6 — RFI-11 | W.R. en walls de wet rooms (todas las caras de restrooms, janitor, alcove) | Para cada room húmedo (finish schedule + notas) listar sus caras; cada cara con gypsum debe estar en W.R. | Toda cara con gypsum de esos rooms está en W.R.; ninguna queda en Type X regular |
| BE-04 | B&N rev6 — R80e.26 | Se cargó W.R. (y plywood) en caras que NO llevan gypsum (Cafe Work Room = FRT plywood + FRP) | Por cada cara en W.R., abrir la sección del type y confirmar que esa cara lleva gypsum board dibujado | Ninguna cara sin gypsum aparece en W.R. / board |
| BE-05 | B&N rev0–rev5 — R80e.26 (RFI-37) | Capas por cara mal contadas: "X = A, B" con dos flechas leído como dos capas por lado; plywood cargado detrás del GWB del lado Sales | Para cada partition type con sección: contar capas lado por lado en el DIBUJO (punteado = gypsum, rayado cruzado = plywood) y seguir cada leader; comparar con "Board by face" del Excel | Cada cara del Excel tiene exactamente las capas y materiales dibujados en su lado |
| BE-06 | B&N rev3–rev5 — RFI-14 / 2/A-221 | Soffit cargado en una sola cara / un solo lado | Todo soffit (framed soffit, header soffit) con sus caras: todos los lados abiertos (N, E, …) y el fondo; board y substrate por cara según su sección | Existen filas para cada lado expuesto del soffit + su fondo, cada uno con su detalle |
| BE-07 | B&N rev5 — R80e.23 | Remate de type por tag "SIM." (cara de extremo de un wall con tag de otro type) no cuantificado | Barrer los tags con "SIM." en la planta; cada uno ubica una cara de remate | Cada tag "SIM." tiene su fila (LF = espesor impreso) con su acabado |
| BE-08 | §0.F (todo proyecto) | Lectura A/B que contradecía una cota impresa | Para walls con cota impresa, comparar LF del Excel con la cota | Todo LF con cota impresa coincide (± 1") o la diferencia es decisión del estimador citada |
| BE-09 | B&N rev1 — RFI-01 | Perímetro existing cuantificado como nuevo | Leer demo plan (legend existing/to remain, key notes) + construction legend + responsibility schedule; los walls existing quedan EXCLUDED con cita y sus markups marcados "EXISTING – EXCLUDED" | Ningún wall existing en el Excel; patch & repair como allowance/RFI |
| BE-10 | B&N rev4 — R80e.25 d | Soffit con cota "HOLD" dejado como "not priced" | Toda cota HOLD + altura RCP + sección = soffit cuantificado; lo no impreso (T.O. WD-1) = RFI con supuesto conservador | Soffit HOLD cuantificado + RFI |
| BE-11 | B&N rev4 — R80e.25 e | Área rotulada "AREA OF 3/4" FIRE RESISTANT PLYWOOD" no cargada | Barrer plantas ampliadas por "AREA OF … PLYWOOD / BACKING / BLOCKING" | Cada área rotulada tiene SF en plywood + RFI de extensión si no está acotada |
| BE-12 | B&N rev4 — R80e.25 f / RFI-31 | Criterio por defecto del skill citado como nota impresa ("ADD FULL LENGTH ADDL HEAD TRACK…") | Cada nota entre comillas del Excel debe existir impresa en la hoja citada | Toda cita textual existe en su hoja; los defaults dicen "not printed / skill default" + RFI |
| BE-13 | B&N rev6 (Paso 12) | Backboard / plywood "BY GC" en hojas E (server room 2/E-103) sin destino | Barrer hojas E/M/P por PLYWOOD, BACKBOARD, BACKING, BLOCKING, ACCESS PANEL, "BY GC" | Cada uno tiene destino: renglón, EXCLUDED con motivo (p. ej. EC por spec) o RFI con delta |
| BE-14 | B&N rev6 (Paso 12, C-01/C-02/C-05) | RFI o Scope que dice "not printed / not specified" cuando el set sí lo imprime (T.O. WD-1 15'-0", alturas de FRP, Level 4) | Por cada RFI / ALC con "not printed", "not specified", "not dimensioned": buscar en specs (A-001A), notas, elevaciones y detalles | Ninguna afirmación "no impreso" tiene la cota o nota impresa en el set |
| BE-15 | B&N rev6 C-06..C-08 + rev7 C7-01 | Detalle leído con otra función: bubble 3 leído como 8; "1 5/8" x 16 GA. METAL JOIST FRAMING @ 48" O.C." (horizontal) cargado como poste vertical | Abrir cada N/HOJA citada a ≥ 200 dpi y confirmar que el miembro rotulado es el que el Excel describe (orientación, función, espaciamiento) | La descripción del renglón coincide con lo dibujado y rotulado |
| BE-16 | B&N rev6 GAP (R80e.27) + rev7 C7-03 | Accesorio impreso por un detalle sin renglón (clip angles, P.A.F. de cross members, #8 screws del relief channel) | Barrer cada detalle del trade por fasteners / clips / runners / plates impresos | Cada accesorio impreso tiene renglón, EXCLUDED con motivo o RFI |
| BE-17 | B&N rev6 (gauge) + rev7 C7-04 / C7-05 | Gauge por fila aplicado, pero los productos que dependen del gauge no se separan (8.A #8 vs #10, 2 vs 3 por conexión; 8.E Type S vs S-12) | Con el gauge de cada fila, recalcular framing screws y drywall screws por gauge | Un renglón por producto y gauge, con su conteo |
| BE-18 | B&N rev6 GAP (ACT, Unistrut, seismic, caulk) | Ítem del set sin destino (ni cuantificado ni excluido ni RFI) | Matriz de cobertura Paso 12 | 0 GAP (cobertura 100 %) |
| BE-19 | B&N rev7 C7-02 / C7-03 | Espaciamiento de fastener impreso reemplazado por un default no impreso (slab pins 12" vs 9/A-410 @ 24" y 8.F 2 rows @ 16"; X-EDNI 8.C vs 8/A-410 #8 @ 24") | Por cada fastener: buscar el espaciamiento en el detalle específico y en la nota típica; el detalle específico manda; conflicto = conservador impreso + RFI | Ningún fastener usa un espaciamiento no impreso sin RFI que cite los impresos |
| BE-52 | B&N rev8 C8-03 | Una pasada anterior dio un ítem por "cubierto por el renglón X" (#8 screws de 8/A-410 → framing screws) y el renglón X no lo contenía | En cada revisión, todo "covered by row X" heredado se re-verifica contra el desglose del renglón X | Cada cobertura heredada aparece en el desglose del renglón citado |
| BE-53 | B&N rev8 C8-02 | El delta de un RFI omitía un accesorio impreso en el mismo detalle que cita (A/A-410 "(1) #10-16 SCREW @ EACH FLANGE" fuera de RFI-28) | Por cada RFI con delta: leer todas las flechas del detalle citado y listar cada pieza impresa | El delta incluye todas las piezas impresas del detalle |
| BE-56 | B&N rev8 C8-01 | Fastener de nota típica (8.F X-DNI) cargado sobre un largo cuya sección de type imprime otro anclaje (types 3/4: HUS-EZ + moment clip, A/A-410) | Por cada fastener con yield por LF: restar los largos cuyos types / detalles imprimen otro anclaje | Ningún LF lleva el fastener típico donde la sección del type imprime otro |

## B. Reglas de método (BOA Broomfield, aplican a todo proyecto)

| ID | Origen | Qué falló | Cómo se prueba | PASS si… |
|---|---|---|---|---|
| BE-20 | BOA — §0.F | Framed soffit cargado solo por perímetro | Framed soffit = studs verticales @ 16" O.C. (L/1.333 + 1) × alto + 2 tracks a todo lo largo | Studs y 2 tracks por soffit |
| BE-21 | BOA — §0.F / R78.13 | Glass mat cargado sin rótulo | Glass mat solo donde un detalle/tag lo rotula | Ningún glass mat sin cita impresa |
| BE-22 | BOA — §0.F / R73.11 / R75.3 | Jamb return de gypsum sin detalle que lo dibuje | Jamb return solo en openings sin frame con return dibujado | Jamb return = 0 o con cita del detalle |
| BE-23 | BOA — §0.F | Acoustical sealant cargado | Debe estar EXCLUDED (solo Clarifications) | Sin renglón de acoustical sealant |
| BE-24 | BOA — reglas inviolables (track) | Top track duplicado / track combinado | bottom track = top track = Σ LF de walls con track (salvo caras de remate sin track); renglones separados | Igualdad (± explicación) y renglones separados |
| BE-25 | BOA — R70.1 / R79.3 | Sistema de ceiling inventado | Suspension (furring + carrying + hanger) solo en ceilings "SUSPENDED GYPSUM BOARD"; otro sistema solo con detalle llamado o que lo corta | Cada ceiling cita su detalle de sistema |
| BE-26 | BOA — R72.1 / R73.1 | Type K (ballistic) medido a nodo y no al hatch/cota | Solo si hay type K / ballistic | N/A si no hay ballistic |
| BE-27 | BOA — R78.36 / R79.2 / R80.3 | ATM / recess sin las piezas impresas | Solo si hay recess de ATM/equipo | N/A si no hay recess |
| BE-28 | BOA — R76.1 / R78.37 | Canopy incompleta / parapet que no sigue la wall exterior | Solo si hay canopy / parapet nuevo | N/A si no hay |
| BE-29 | BOA — R71.10 / R80e.5 | Header "assumed" sin schedule | Header que ningún schedule llama = 0 LF + RFI con delta | Headers 0 + RFI, o con cita |

## C. Formato y trazabilidad (todo proyecto)

| ID | Origen | Qué falló | Cómo se prueba | PASS si… |
|---|---|---|---|---|
| BE-40 | §0.F / R80e.24 (B&N rev4) | Material Summary sin N/HOJA o sin desglose que reproduzca el NET | Cada renglón de Material Summary: "N/SHEET:" + "Breakdown [DERIVED]" (o la operación) cuya suma = NET | Todos los renglones con cita y desglose que suma el NET (± 0.1) |
| BE-41 | R80e.24 | Nombres de archivos internos en el Excel | Buscar .json / .py / carpetas de trabajo en todas las hojas visibles | Ninguno |
| BE-42 | §0.F / R80e.9 | Partitions fuera del orden del schedule / sin subtotales | Orden de los types = orden del schedule del proyecto; SUBTOTAL por type; GRAND TOTAL = Σ subtotales | Orden correcto, subtotales cuadran |
| BE-43 | §0.F | Formato del Excel cambiado | 6 hojas visibles fijas (Inputs, Partition Takeoff, Material Summary, Pending Items, Review Items, Scope Checklist) | Exactamente esas 6 visibles |
| BE-44 | §0.F / R78.20–R78.24 | Markups Bluebeam ausentes o que no cuadran | PDF con una annot por wall (Subject = type, Depth = alto); Σ Length y Σ Wall Area por type = Excel | Cuadre por type ≤ 0.5 % |
| BE-45 | §0.F | Proporciones fuera de rango sin explicación | board vs Σ LF × alto × caras; screws/SF; studs/LF según O.C.; track vs partitions; compound/tape vs board | Todo dentro de rango o explicado en el Excel |
| BE-46 | B&N rev7 C7-06 + rev8 C8-04 | Dos espesores / productos en un mismo renglón (cement board 1/2" de A-221 + 5/8" de 22/A-201); track 3-5/8" + 6" + ledger 8" + ceiling track en un renglón | Leer el espesor impreso de cada fuente del desglose | Un espesor y un producto por renglón |
| BE-47 | B&N rev7 C7-07 / C7-08 | Cantidades o IDs en textos (RFI, Scope, README) que no coinciden con su renglón (585.27 vs 568.27; ALC-X26..X30 vs X40..X44) | Cruce automático de cada número y cada ID ALC- / RFI- citado contra Material Summary / Scope Checklist / Pending Items | Todo número e ID citado existe y coincide |
| BE-48 | B&N rev7 C7-09 | Nombre de archivo interno en el PDF de markups ("Source: takeoff_canon.json" en la leyenda) | Buscar .json / .py / carpetas de trabajo en el texto de las páginas agregadas y en Contents de los markups | Ninguno |
| BE-49 | B&N rev7 (verificación Paso 12) | Cota impresa atribuida al elemento equivocado (46'-0" del track LWT-01 cerca de la nube) | Antes de aplicar o corregir con una cota: seguir sus extension lines y cerrar la cadena con las cotas vecinas (1'-5" + 46'-0" + 1'-5" = 48'-10") | Cada cota usada pertenece al elemento cuantificado |
| BE-50 | B&N rev7 N-03 | Traslape de alcance entre hojas A y E/M/P sin RFI (E-301 265119 soportes de luminarias por el EC vs wires en luminarias cargados por 5/A-121) | Por cada renglón del trade que una spec E/M/P asigne a otro contratista: RFI con delta | Todo traslape tiene RFI |
| BE-51 | B&N rev8 C8-05 | Renglones en LF con selling unit "piece" y Pieces to buy = ROUNDUP(LF) (2x blocking, main / cross tee, molding, 16 ga wire) | Por cada renglón: Unit vs Selling unit vs fórmula de Pieces to buy | Pieces to buy en piezas reales (stock length de Inputs) o venta por LF / coil |
| BE-54 | B&N rev8 C8-08 | Partición por producto (Type S / S-12) sobre board bruto por wall, con la deducción (base de cement board) aplicada solo al total | Recalcular cada partición por cara, aplicando cada deducción a las mismas caras | La suma por producto respeta las deducciones de cada cara |
| BE-55 | B&N rev8 C8-07 | Códigos internos del plan check (C7-0x, C-0x, N-0x, "rev7 plan check") en textos al cliente | Buscar con regex en todas las hojas visibles y en el README | Ninguno |
| BE-57 | B&N rev10 (estimador 27-oct) | Blocking de madera (2x / FRT) con el waste de METAL (Inputs B5 15 %) | Por cada renglón de Material Summary: material madera / board / plywood / cement board → waste NO metal (B6) | Ningún renglón no metálico usa B5 |

---

## Resultados por proyecto

(Se agrega una tabla por entrega. Detalle y evidencia en la carpeta PASO12 del proyecto.)

### B&N Colorado Springs — rev6 (Paso 12, 2026-10-27)

21 PASS · 5 FAIL · 3 N/A. Evidencia: `barnes_noble/PASO12_rev6/` (MATRIZ_COBERTURA.xlsx › Error Library, CERTIFICADO_PASO12.md, img/).

| Prueba | Resultado | Nota |
|---|---|---|
| BE-01 | PASS | 264.21 LF carried (3-5/8" 157.81 + 6" 106.40) + RFI-35; citation must read 3/A-410 (C-07) |
| BE-02 | PASS | Women's 61.19 + Men's 61.11 SF W.R. (Material Summary!R20); Janitor 107 has no GWB ceiling |
| BE-03 | PASS | R20 breakdown covers W2-05..W2-08, W5-01; A-510 does not contradict. Base 1'-2" must be cement board (C-03) |
| BE-04 | PASS | No C-* face in the W.R. breakdown; Work Room = FRT plywood (G/A-221) |
| BE-05 | PASS | G, H, E, F, I, A-D/A-221 checked side by side against "Board by face" - all match |
| BE-06 | PASS | SS-N, SS-E, SS-IN-N, SS-IN-E, SS-GG + bottoms carried. Open: plywood above WD-1 (2/A-221) and soffit corner bead = GAP rows |
| BE-07 | PASS | I SIM. x2 on 1/A-221 = C-I-E1, C-I-E2 |
| BE-08 | FAIL | 19'-0" HOLD ignored for C-E1-S cement board (C-04); T.O. WD-1 printed but RFI-34 says not printed (C-01); FRP heights printed (C-02) |
| BE-09 | PASS | RFI-01 (1/DM-101, A-101, A-002); 17 EXT markups "EXISTING - EXCLUDED". New RFI proposed: A-410 types 1/1A/1B/1C "5/8" GYP BD BY FUTURE TENANT" |
| BE-10 | PASS | SS-GG 6'-2" HOLD quantified (RFI-20 closed); T.O. WD-1 now printed (C-01) |
| BE-11 | PASS | Janitor 17.0 SF 3/4" FRT (11/A-200) + RFI-33 |
| BE-12 | FAIL | 8/A-410 should be 3/A-410 (C-07); 6/A-410 plates not printed (C-08); 6/A-210 is the glazing base detail (C-06) |
| BE-13 | FAIL | 2/E-103 server room 4'x8' FRT plywood "BY GC" - no row / exclusion / RFI |
| BE-20 | PASS | SS-N/E/IN studs in R12 + R28; track = 2 x length (R13) |
| BE-21 | PASS | None carried; ALC-09 NOT APPLICABLE |
| BE-22 | PASS | R36 = 0 citing 1/A-500, 2/A-500 |
| BE-23 | PASS | ALC-19 EXCLUDED; no row |
| BE-24 | PASS | 450.02 + 118.59 = 568.61 LF each = 569.816 - end faces C-I-E1/E2 1.206 (R80e.23) |
| BE-25 | PASS | 5/A-121 suspension; 4/A-121 USG grid for the cloud |
| BE-26 | N/A | No ballistic type in A-410 |
| BE-27 | N/A | R34 none (A-101, A-500, A-221) |
| BE-28 | N/A | ALC-03, ALC-14 NOT APPLICABLE (A-300: no new canopy) |
| BE-29 | PASS | RFI-09 (0 LF + delta 83.32 LF) |
| BE-40 | FAIL | R28 "3-5/8" stud, framed soffit 2/A-221" 61.31 LF has no breakdown / operation; R13 FIRESTOP-TRACK lines have no per-wall breakdown. All other breakdowns sum the NET (+/- 0.1) |
| BE-41 | FAIL | Pending Items RFI-06 "ri07_rcp/", RFI-12, -13, -20, -31, -32, -33, -35, -36 cite "AUDITORIA_rev4/COMPARATIVA_AUDITORIA.xlsx" |
| BE-42 | PASS | Subtotals = rows; GRAND TOTAL 569.816 = sum of subtotals. Observation: A-410 prints no schedule table; order 2, 5, 3, 4 is the declared order (rev1); by type number it would be 2, 3, 4, 5 |
| BE-43 | PASS | 6 visible + hidden "_reglas" gate signature |
| BE-44 | PASS | Sum Length and sum Wall Area (Length x Depth) match on all 18 types (max delta 0.01 LF, type I rounding) |
| BE-45 | PASS | See sheet Proportions; 3 traceability observations |

### B&N Colorado Springs — rev7 (Paso 12, 2.ª pasada, 2026-10-27)

**27 PASS · 10 FAIL · 3 N/A** (40 pruebas). Evidencia: `barnes_noble/PASO12_rev7/` (MATRIZ_COBERTURA.xlsx › Error Library, CERTIFICADO_PASO12.md, img/).

| Prueba | Resultado | Nota |
|---|---|---|
| BE-01 … BE-11 | PASS | Fire-stop track, W.R., capas, soffits, SIM., cotas LF, existing, HOLD, áreas rotuladas |
| BE-12 | FAIL | "24" (type K box)" en RFI-ACC-slab-pins; "compression post" atribuido a 5/A-121; N/SHEET "GA-216" |
| BE-13 | PASS | 2/E-103 + RFI-50 |
| BE-14 | PASS | Muestreo de "not printed" sin hallazgos |
| BE-15 | FAIL | C7-01 (1-5/8" joist framing @ 48" leído como poste) |
| BE-16 | FAIL | C7-03 (#8 screws @ 24" y P.A.F. de 8/A-410) |
| BE-17 | FAIL | C7-04, C7-05 (screws por gauge) |
| BE-18 | FAIL | 2 GAP (N-01, N-03) |
| BE-19 | FAIL | C7-02, C7-03 (espaciamientos impresos) |
| BE-20 … BE-25, BE-29 | PASS | |
| BE-26 … BE-28 | N/A | |
| BE-40 … BE-45 | PASS | |
| BE-46 | FAIL | C7-06 |
| BE-47 | FAIL | C7-07, C7-08 |
| BE-48 | FAIL | C7-09 |
| BE-49 | PASS | rev7 nube 38'-10" correcta |
| BE-50 | FAIL | N-03 |

## Corrida B&N rev8 (2026-10-27)
Back-check final: LIBRARY 37 PASS · 0 FAIL · 3 N/A (`barnes_noble/takeoff_work/etapas/5_auditoria/BACKCHECK_rev8_recheck.md`). Los 10 FAIL (BE-12, 15, 16, 17, 18, 19, 46, 47, 48, 50) quedan corregidos. Las lecciones nuevas están en la regla R80e.29 del skill v80o.


## Corrida B&N rev8 — Paso 12 independiente (2026-10-27)
46 pruebas: 32 PASS · 11 FAIL · 3 N/A. FAIL: BE-16 (C8-02, C8-03), BE-19 (C8-01), BE-40 (C8-08), BE-46 (C8-04), BE-47 (C8-06), BE-51…BE-56 (C8-05, C8-03, C8-02, C8-08, C8-07, C8-01). N/A: BE-26, 27, 28. Veredicto: NO PASA (cobertura 100 %, 0 GAP, 8 CORREGIR). Nota: el back-check rev8 (37/0) dejó C8-01/02/03/08 como "no bloqueantes"; son piezas impresas o reglas del skill → CORREGIR.
## Corrida B&N rev9 (2026-10-27)
Back-check final: 43 PASS · 0 FAIL · 3 N/A (46 pruebas). El detalle está en `barnes_noble/takeoff_work/etapas/5_auditoria/BACKCHECK_rev9.md`. Las pruebas BE-16, 19, 40, 46, 47 y 51 a 56 quedan corregidas. Las lecciones nuevas están en la regla R80e.31 del skill v80p.

## Corrida B&N rev12 (2026-10-28)
Back-check final: 44 PASS · 0 FAIL · 3 N/A (con BE-57), en `barnes_noble/takeoff_work/etapas/5_auditoria/BACKCHECK_rev12.md`. En la primera pasada fallaron BE-41 (nombres de carpetas internas en Pending Items) y BE-40 (desglose del head track cortado); los dos quedaron corregidos.

## Corrida B&N rev13 (2026-10-28)
Back-check final: 44 PASS · 0 FAIL · 3 N/A (`barnes_noble/takeoff_work/etapas/5_auditoria/BACKCHECK_rev13.md`). En la primera pasada falló BE-47: RFI-13 y RFI-22 tenían las cifras viejas; se corrigió con la nota "Revised by RFI-55".
