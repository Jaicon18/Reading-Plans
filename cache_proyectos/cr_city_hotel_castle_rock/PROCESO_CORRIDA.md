# PROCESO DE LA CORRIDA - CR City Hotel (skill v81cf55 en curso = v81cf54 + BE-CR01..04)

1. Arranque: órdenes jc-hunter-ordenes U-001..U-150 leídas; skill vigente v81cf52 → v81cf54 (+ BE-CR01..04); verificar_version 0 faltantes.
2. Descarga: BuildingConnected (solo lectura / descarga, U-129), 19 archivos; set vigente 2026 Permit Drawings (148 hojas A/S/MP/E) + Project Manual Vol 1 / 2; 2025 Full Drawing Set comparado por programa (comparacion_sets.json). Gmail: único GC Owen-Ames-Kimball (U-091).
3. Copia limpia: bidset_SIN_MARKUPS.pdf (86 sellos del arquitecto quitados, 0 markups de take-off); todos los renders desde esa copia.
4. Inventario por script: inventario_tags.py (arreglado BE-CR01) 354 tags, 617 burbujas, rc 0.
5. Lector independiente de schedules (subagente sin Excel): indep/fichas.json (49 types), schedules_indep.json, NOTAS.md.
6. Lecturas A y B independientes por piso (8 subagentes: A L1-L4 walls + ceilings + soffits; B L1-L4 walls), carpetas separadas, mismo PDF, inventario y brief; B no ve A.
7. Burbujas: 2 subagentes (G1 / G2) verifican a ojo 605 burbujas + 57 agregadas a ojo y siguen cada cadena a su destino (CADENA.md).
8. Comparación por programa (scripts/comparar_AB.py) + resolución por piso (4 subagentes) con reglas fijas R1-R7 tomadas del plano, cada decisión con N/HOJA + crop (3_revision/resolucion.md).
9. Cálculo: scripts/build_canon.py + finalizar_canon.py + rfis.py → canon.py (board-only en existing_walls, C-H studs / J-runner y USG suspension en misc_items con op visible) → familias_out.json; plantilla_excel.py arma el Excel fijo de 6 hojas.
10. Proyecto WOOD-FRAMED: todo framing de wood EXCLUDED (Div. 06, U-139); nuestro alcance = gypsum board, exterior gyp sheathing, cement board, shaftliner + C-H studs / J-runner, resilient channel, drywall suspension, soffits, trim.
