# CAMBIOS v76 — hand-off entre tareas, jogs entre caras, box con tag, entrega coherente (arbitraje de dos pruebas ciegas)

Origen: dos pruebas ciegas del mismo set con el mismo paquete. Pasaron la calificación, pero varias familias
dependían de la lectura: una corrida dejó la canopy "para otra tarea" y nadie la tomó (joists, sheathing y track del
soffit), no generó el sheathing de los column wraps ni el substrate de las aberturas, midió un jog del contorno
ballistic de cara exterior a cara exterior y cargó dos veces el borde de un ceiling que ya era transición; la otra
sacó de su type un box con tag por su `location` y no pudo entregar porque dos tools se contradecían. Cada cambio es
genérico (ningún número, wall ni room de un proyecto) y tiene test sintético (test_v76.py). Reglas R76.1–R76.9 en
SKILL §23.

## Compuertas nuevas (chequeos_v76.py, llamadas por canon.py)
- R76.1 canopy completa: fascia_box ↔ canopy_joist por facade; canopy_joist → run canopy_soffit; un renglón de
  `otros_ceilings` con soffit / canopy y framing queda consumido (`consumed_by`) o excluido con N/HOJA. Un hand-off
  a otra tarea no es estado final.
- R76.2 column wrap sin board: `sheathing {material, source}` (canon genera Σ faces × alto) o motivo.
- R76.3 jog ballistic derivado de las bandas K: hueco entre caras enfrentadas; falta / sobra / cruza un espesor = error.
- R76.4 substrate de aberturas exteriores: `substrate {label, source, material, sill}` o motivo; canon genera el strip
  con `constants.opening_substrate_width_ft`; strip a mano de head / jamb / sill = error.
- R76.5 box / pier con tag de partition type sigue en su type (location no manda); LF = caras interiores; parte
  `part_of` interior suma sus caras.
- R76.6 perímetro de ceiling completo (≥ 2·√(π·área)); `ceiling_transition.edge_of`; canon resta las transiciones.

## Entrega coherente
- plantilla_excel.py `verificar_r71_track`: clasifica los renglones con familias.py en su unidad (parapet, heads y
  other framing suman la familia); los tamaños que exigen renglón salen de las filas de partition types.
- bitacora.py: el paso E24 acepta `test_ciego.py` o `test_ciego_tools.py`; `test_ciego.py` viaja en el paquete ciego.
- R76.7 (regla inviolable): ningún texto se escribe para satisfacer un regex de compuerta. `A_BLOCKING` lee el
  rótulo (y `frt_basis`), no el source; blocking 2X / WOOD sin FRT impreso = material `wood` (renglón propio).
- `fos_chain_faces` (caja parcial: una cadena o medida por face) aceptado por canon.py y `A_WRAP_FOS`.

## Nombres de renglón (plantilla del estimador)
- Nailbase: "Exterior sheathing <th> FRT plywood bonded to <espesor impreso> polyiso"
  (`constants.nailbase_polyiso_in {value, source}` obligatoria con nailbase).
- Joists de framed soffit en su renglón "3-5/8" stud, framed soffit <detalle> (LF)" dentro de su familia.

## Sin cambio (con motivo)
- Clips de bridging: la plantilla del estimador no los compra; closer.py los usa como control.
- Bracing de parapets: cada tramo usa su altura (un tramo bajo da 0 filas); no hay sobreconteo.

## Pendiente del estimador (sin decidir; SKILL §22 dice dónde entra cada respuesta)
- extra framing ATM; header / box beam; 3/4" FRT plywood en piers; sill track; track de perímetro en un borde de
  transición (R76.6 aplica R73.16; la otra lectura va como RFI con delta).
