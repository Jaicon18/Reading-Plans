# ADENDA v34 — 1-oct-2026 · COMPUERTA DE COBERTURA DE DETALLES

## De dónde salió

Rodolfo preguntó si podía hacer un take-off completo solo. La respuesta salió de mirar **quién encontró cada error** en un proyecto anterior.

La auditoría adversarial encontró 14 — perfil de stud mal clasificado, doble conteo de MEP, sheathing facturado como board interior, el wall inclinado que el cruce de MEP se saltaba callado. Pero los que encontró **él** son de otra clase:

| lo que él vio | qué era |
|---|---|
| "¿estás checando las wet areas?" | faltaban 3 de 4 zonas |
| "accesorios incluye taping, screws, pines" | faltaban 5 line items completas |
| "¿los jamb studs van al deck? ¿seguro?" | → salieron [valor retirado E24] LF de head track doble |

**Ninguno lo caza una compuerta de aritmética, porque una compuerta solo revisa lo que a alguien se le ocurrió revisar.**

> El patrón de lo que se escapa es siempre el mismo: **condiciones que SÍ están dibujadas y que no se sabe que hay que buscar.** El head track doble estaba rotulado en 2/S5.20 desde el día uno. Nadie lo escondió: no se abrió el detalle.

Hasta la v33 cada regla fue **reactiva** — una por incidente. Faltaba la que cubre la CLASE.

## REGLA — No se cierra un proyecto sin haber abierto cada detalle de cada hoja que se usó

`verif_detalles.py` arma el universo de detalles de **las hojas que el propio take-off declara como fuente** — si un cierre cita A12.01, entonces TODOS los detalles dibujados en A12.01 entran al universo — y lo compara contra los que los cierres citan de verdad.

**No decide si un detalle aplica.** Eso lo decide quien lo lee. Lo que impide es **cerrar sin haberlo mirado**. Un detalle que se miró y no aplica se declara en `NO_APLICAN` con su motivo escrito, nunca se deja caer en silencio.

**Cómo detecta un detalle:** burbuja = un número de 1-2 dígitos justo ENCIMA de un número de hoja (`[A-Z]{1,2}\d{2}\.\d{2}`), a menos de 30 pt y alineados en x.

**Va por caché** (`cache_detalles.py`): barrer 94 hojas con pdfplumber tarda minutos, y una compuerta que tarda minutos no se corre. Se cachean solo las hojas que el take-off usa — unas 17 — y el caché se invalida solo si cambia el tamaño o la fecha del PDF.

---

## Lo que encontró en su primera run

**46 detalles sin abrir** en hojas que el take-off ya usaba. Y entre ellos, uno que valía material de verdad.

### El purlin que no estaba en ninguna parte

`A09.33`, detalle de fastening del top track al deck:

> `STL TRACK, CL TO BE BETWEEN ATTACHED FLUTES, NO EXCEPTION`
> **`1X1X1 16GA PURLIN, ACROSS MIN. (2) FLUTES`**
> `POWDER-DRIVEN FASTENERS` · `ALTERNATE CEILING DETAIL, VIF FLUTE DIRECTION`

Donde la flute del deck corre **paralela** al track no hay valle donde clavar: hay que poner un purlin de 16 ga cruzando mínimo dos flutes y clavar ahí. **La palabra "purlin" no aparecía ni una vez** en los cierres ni en el Excel.

**[valor retirado E24] LF agregados.** Salen del LF de top track de los walls que corren paralelos a la flute y suben al deck, a (largo de pieza ÷ spacing de pines) LF de purlin por LF de track — una pieza por fastening, con los pines al O.C. que pide el detalle (p. ej. 4/A12.01).

Dirección de la flute **[DERIVADO]**: el deck Type B salva entre joists; las joists de S2.20 corren norte-sur, luego las flutes corren este-oeste. El propio detalle dice `VIF FLUTE DIRECTION`, así que va declarado en Clarifications, y los exteriores y el wall inclinado quedan en Pending (hasta [valor retirado E24] LF más).

### El bulkhead de cielo lleva más de lo que decía el pendiente

El detalle típico de bulkhead (`N/HOJA`) describe la transición de cielo con **`3 5/8" METAL STUD FRAMING AND TRACK @ 16" O.C.`** más bracing @ 48", board, corner L bead y shadow molding — bastante más que el "kicker @ 48"" que decía el pendiente del perímetro de transición.

---

## REGLA — Una cita que una máquina no puede leer no se puede auditar

De los 46, **9 eran falsos positivos**: detalles que **sí se leyeron** pero citados en prosa — *"el detalle C1 dibuja board de una sola face"* en vez de `6/A12.01`.

> **Todo cierre cita sus detalles en formato canónico `N/HOJA`.** La prosa puede acompañar, pero el formato machine-readable tiene que estar.

Segundo defecto propio: la detección cuenta los **marcadores de corte de sección** como si fueran burbujas de título. Un `6/A08.01` sobre una elevación es un corte que apunta al detalle 6, no el detalle 6. Para la compuerta da igual — en los dos casos hay que abrirlo — pero el reporte no debe decir "dibujado en esa hoja".

---

## Cómo se usa en un proyecto nuevo

```
1. cache_detalles.paginas([...])   una vez, con las hojas del mapa
2. verif_detalles.py               lista lo que falta por abrir
3. ver_detalle.py <pag> <hoja> <n> recorta el detalle para leerlo
4. NO_APLICAN                      lo que se miró y no aplica, CON MOTIVO
5. el cierre cita N/HOJA           y la compuerta deja de marcarlo
```

Corre dentro de `entregar.py`. **Mientras queden detalles sin abrir ni declarar, el proyecto no está cerrado.**

---
