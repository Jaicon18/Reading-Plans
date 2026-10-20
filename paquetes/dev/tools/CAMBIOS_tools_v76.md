# CAMBIOS tools v76

- chequeos_v76.py (nuevo): R76.1 `r76_1` (fascia_box ↔ canopy_joist por facade, canopy_joist → run canopy_soffit,
  hand-off de `otros_ceilings` consumido), R76.2 `r76_2` + `sheathing_column_wraps`, R76.3 `jogs_k` + `r76_3`
  (jog ballistic = hueco entre caras), R76.4 `aberturas_ext` + `r76_4` (substrate de aberturas), R76.5 `r76_5`
  (box con tag), R76.6 `bordes_transicion` + `r76_6_perimetro`.
- canon.py: llama `chequeos_v76.verificar`; `_column_wrap_sheathing` (R76.2); `_opening_substrate` (R76.4); track
  de perímetro de ceiling = perímetro − transiciones con `edge_of` (R76.6); `_polyiso` (nombre del nailbase con el
  espesor impreso); `stud_by_element` (framed soffit en su renglón); blocking material `wood` + `frt_basis`;
  `fos_chain_faces`; R70.6 no exige `type_lf_basis` cuando hay caras interiores con largo; WALL_KEYS con
  `sheathing`, `edge_of`, `beam_override`, `part_of`, `same_box_ok`, `opening_ref`, `type_change_rfi`,
  `anchorage`, `orientation`, `sheets_searched` (las leen otras tools).
- partition_types.py: `TAG_TYPE`; pier / column_wrap con tag de type sigue en su type aunque `location` sea exterior
  (R76.5); parte `part_of` interior de un box con tag suma sus caras al LF del box.
- plantilla_excel.py: `verificar_r71_track` clasifica con familias.py (en su unidad) y toma los tamaños de las filas
  de partition types (no de OTHER FRAMING); renglones `stud_by_element` y "Blocking 2X wood (not labeled FRT)".
- reglas.py: `A_BLOCKING` lee el rótulo (y `frt_basis`), no el source; `A_WRAP_FOS` acepta `fos_chain_faces`.
- reglas_clasificacion.py: R76.1–R76.9.
- bitacora.py: el paso E24 acepta `test_ciego.py` o `test_ciego_tools.py`. armar_ciego.py: `test_ciego.py` viaja.
- test_ciego.py: texto genérico. test_ciego_tools.py: comentario de P18B genérico.
- test_v76.py (nuevo, casos sintéticos por regla).
