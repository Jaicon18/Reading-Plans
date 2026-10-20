# ADENDA v<n> — <n>-oct-<n> · COMPUERTA DE COBERTURA DE DETALLES

## De dónde salió

Rodolfo preguntó si podía hacer un take-off completo solo. La respuesta salió de mirar **quién encontró cada error** en un proyecto anterior.

La auditoría adversarial encontró <n> — perfil de stud mal clasificado, doble conteo de MEP, sheathing facturado como board interior, el wall inclinado que el cruce de MEP se saltaba callado. Pero los que encontró **él** son de otra clase:


**Ninguno lo caza una compuerta de aritmética, porque una compuerta solo revisa lo que a alguien se le ocurrió revisar.**

> El patrón de lo que se escapa es siempre el mismo: **condiciones que SÍ están dibujadas y que no se sabe que hay que buscar.** El head track doble estaba rotulado en 2/S5.20 desde el día uno. Nadie lo escondió: no se abrió el detalle.

Hasta la v33 cada regla fue **reactiva** — una por incidente. Faltaba la que cubre la CLASE.

## REGLA — No se cierra un proyecto sin haber abierto cada detalle de cada hoja que se usó

`verif_detalles.py` arma el universo de detalles de **las hojas que el propio take-off declara como fuente** — si un cierre cita A12.<n>, entonces TODOS los detalles dibujados en A12.<n> entran al universo — y lo compara contra los que los cierres citan de verdad.

**No decide si un detalle aplica.** Eso lo decide quien lo lee. Lo que impide es **cerrar sin haberlo mirado**. Un detalle que se miró y no aplica se declara en `NO_APLICAN` con su motivo escrito, nunca se deja caer en silencio.

**Cómo detecta un detalle:** burbuja = un número de <n>-<n> dígitos justo ENCIMA de un número de hoja (`[A-Z]{<n>}\d{<n>}\.\d{<n>}`), a menos de <n> pt y alineados en x.

**Va por caché** (`cache_detalles.py`): barrer <n> hojas con pdfplumber tarda minutos, y una compuerta que tarda minutos no se corre. Se cachean solo las hojas que el take-off usa — unas <n> — y el caché se invalida solo si cambia el tamaño o la fecha del PDF.

---

## Lo que encontró en su primera run

**<n> detalles sin abrir** en hojas que el take-off ya usaba. Y entre ellos, uno que valía material de verdad.

### El purlin que no estaba en ninguna parte

`A09.<n>`, detalle de fastening del top track al deck:

> `STL TRACK, CL TO BE BETWEEN ATTACHED FLUTES, NO EXCEPTION`
> **`<n>X<n>X<n> 16GA PURLIN, ACROSS MIN. (<n>) FLUTES`**
> `POWDER-DRIVEN FASTENERS` · `ALTERNATE CEILING DETAIL, VIF FLUTE DIRECTION`

Donde la flute del deck corre **paralela** al track no hay valle donde clavar: hay que poner un purlin de 16 ga cruzando mínimo dos flutes y clavar ahí. **La palabra "purlin" no aparecía ni una vez** en los cierres ni en el Excel.

**[valor retirado E24] LF agregados.** Salen del LF de top track de los walls que corren paralelos a la flute y suben al deck, a (largo de pieza ÷ spacing de pines) LF de purlin por LF de track — una pieza por fastening, con los pines al O.C. que pide el detalle (p. ej. 4/A12.01).

Dirección de la flute **[DERIVADO]**: el deck Type B salva entre joists; las joists de S2.20 corren norte-sur, luego las flutes corren este-oeste. El propio detalle dice `VIF FLUTE DIRECTION`, así que va declarado en Clarifications, y los exteriores y el wall inclinado quedan en Pending (hasta [valor retirado E24] LF más).

### El bulkhead de cielo lleva más de lo que decía el pendiente

El detalle típico de bulkhead (`N/HOJA`) describe la transición de cielo con **`3 5/8" METAL STUD FRAMING AND TRACK @ 16" O.C.`** más bracing @ 48", board, corner L bead y shadow molding — bastante más que el "kicker @ 48"" que decía el pendiente del perímetro de transición.

---

## REGLA — Una cita que una máquina no puede leer no se puede auditar

De los <n>, **<n> eran falsos positivos**: detalles que **sí se leyeron** pero citados en prosa — *"el detalle C<n> dibuja board de una sola face"* en vez de `6/A12.01`.

> **Todo cierre cita sus detalles en formato canónico `N/HOJA`.** La prosa puede acompañar, pero el formato machine-readable tiene que estar.

Segundo defecto propio: la detección cuenta los **marcadores de corte de sección** como si fueran burbujas de título. Un `6/A08.01` sobre una elevación es un corte que apunta al detalle <n>, no el detalle <n>. Para la compuerta da igual — en los dos casos hay que abrirlo — pero el reporte no debe decir "dibujado en esa hoja".

---

## Cómo se usa en un proyecto nuevo

(ejemplo de una corrida retirado del paquete ciego)

Corre dentro de `entregar.py`. **Mientras queden detalles sin abrir ni declarar, el proyecto no está cerrado.**

---
