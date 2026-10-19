# CAMBIOS tools v73 (arbitraje #21)

Nuevas: cotas_banda.py, chequeos_v73.py, planmark.py (+ test_planmark), glosario.py, vocab_trade.py,
verif_respuesta.py (+ test_glosario, test_verif_respuesta), correr_suite.py, test_v73.py, test_indice_set.py,
test_registro_v73.py.

Cambiadas:
- reglas.py: v73; chequeos A_R73_1, _2, _5, _6, _7, _8 (consistencia con el plano); fos_chain acepta la forma dict
  de canon.py (P02); regex de anchors / pins aceptan el texto en inglés.
- reglas_clasificacion.py: R73.1–R73.18 clasificadas; R70.5 / R72.5 / R72.9 suman los chequeos v73.
- canon.py: WALL_KEYS + hatch_extent, dim_scan (P01); FRT plywood por material, espesor y USO con nombre de la
  plantilla; track_by_element; metal_blocking_by_origin; nombres_contexto.
- accesorios.py: stud reinforcement MEP solo con ductos de mep.cruces (R73.5; lo demás a RFI con delta); familia
  "deflection clips" (R73.6, P04); todos los textos que llegan al Excel en inglés (P08, R73.9).
- plantilla_excel.py: nombres de renglón de la plantilla (NOMBRES_PLANTILLA, track por elemento, metal blocking por
  origen) (R73.3); regex de yields aceptan el texto en inglés.
- particion.py: R72.7 con límite de distancia (R73.18).
- indice_set.py: genérico, sin coordenadas de un set; arma su propio cache (P05).
- registro.py: `corregir` (F01).
- eval_takeoff.py: rango min == max manda; _partition_types; modo "consistencia" no califica; bloque OTHER no sobra.
- test_ciego_tools.py: revisa test_*.py y fixtures; P6 rooms de tres dígitos, P7 ids de wall de planta, P8 lista externa.
- tests con datos sintéticos (rooms, ids y hojas inventados): test_canon, test_closer, test_headers,
  test_inventario, test_studs_nodos, test_corridas, test_etapas_v70, test_esquinas, test_framed_openings…
