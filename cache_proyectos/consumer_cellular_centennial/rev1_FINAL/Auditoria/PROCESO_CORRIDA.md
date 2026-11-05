# PROCESO_CORRIDA - Consumer Cellular - Centennial, CO (skill v81cf47)

1. Download: Elder-Jones set from BuildingConnected (1 PDF, 37 pages) and Elite Retail set from elite-constructionplans.com (37 single sheets + Starlink + bid forms) + BuildingConnected survey documents; read / download only.
2. Sets compared by program (comparacion_sets.json): text identical sheet by sheet; Elder-Jones PDF used as the bid set; 0 annotations; clean copy bidset_SIN_MARKUPS.pdf.
3. Inventory: inventario_tags.py (1_inventario). Text of the set + bubble sweep: compuerta_entrega.py texto (set_texto.json).
4. Readings A and B: two independent subagents (2_lectura/A, 2_lectura/B), same brief and PDF, no files passed between them.
5. Independent schedule reader (indep/fichas.json, schedules_indep.json) and bubble verifier (burbujas/burbujas_verificadas.json, CADENA.md), subagents that never saw the readings nor the Excel.
6. comparar.py (3_revision/revision.md) -> resolution on the crops (scripts/resolver_AB.py, 3_revision/resolucion.md).
7. Calculation chain scripts/cadena.sh: ajustes_canon.py (format / rule fixes, each documented), rfis.py, runner/evidencia.py, canon.py, inventario.py, framed_openings.py, alcance_filtro.py, sellar_y_marcar.py (closer + planmark), markups_bluebeam.py, markups_demo.py, imagenes_hoja.py, takeoff_json.py, plantilla_excel.py, registro / alcances gates, verificar_markups_excel.py. Every tool through bitacora.py run.
8. Delivery gate compuerta_entrega.py and upload subir_entrega.py.
