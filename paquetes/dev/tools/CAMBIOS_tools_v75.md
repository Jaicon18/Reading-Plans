# CAMBIOS tools v75

- canon.py: TRACK_NOMBRES sin "soffit"; renglón "other framing" (R75.2); `ids_partition_takeoff`,
  `verificar_track_nombres` (R75.1); track_by_element después de partition_types; llama chequeos_v75.
- familias.py: EXCLUYE de "track de ceilings / soffits" lo que empieza con bottom / top (R75.1).
- accesorios.py: `_sill_return` sin default cuando hay return y sill; `_label_gyp` (R75.3); `_storefront_de_cripples`
  (R75.4).
- chequeos_v75.py (nuevo): R75.5 `verificar_r75_5`, R75.6 `alcove_con_esquina`, R75.7 `returns_sin_esquina`.
- reglas_clasificacion.py: R75.1–R75.7.
- test_v75.py (nuevo, 7 casos sintéticos); fixtures de test_canon / test_accesorios con jamb_return_label y
  sill_return.
- test_ciego_tools.py: P23 / P24 / P25 (estricto).
- inventario.py, studs_nodos.py, dataset.py: textos genéricos.
- v75b: textos genéricos (canon.py, familias.py, partition_types.py, inventario.py, README_etapas.md); test_ciego_tools P25 con comas y P18 con signo en comentarios.
