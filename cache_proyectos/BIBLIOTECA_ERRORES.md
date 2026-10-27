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

---

## Resultados por proyecto

(Se agrega una tabla por entrega. Detalle y evidencia en la carpeta PASO12 del proyecto.)
