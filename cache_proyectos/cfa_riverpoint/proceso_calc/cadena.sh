#!/bin/bash
# Stage 4-5 chain on the final canon (every tool through bitacora.py run). Stops at the first rc != 0.
source /tmp/claude-0/-home-user-reading-plans/00739bfa-f4e4-5132-80c8-c9e8628b8f17/scratchpad/cfa_calc/env.sh
cd $W; C4=$W/etapas/4_canon; X=$W/etapas/8_excel/CFA2284_RiverPoint_Takeoff_FINAL_rev1.xlsx
R() { python3 $T/bitacora.py run "$@" > /tmp/claude-0/-home-user-reading-plans/00739bfa-f4e4-5132-80c8-c9e8628b8f17/scratchpad/cfa_calc/last.log 2>&1; rc=$?; echo "rc=$rc $(basename $1) $2"; if [ $rc != 0 ]; then tail -40 /tmp/claude-0/-home-user-reading-plans/00739bfa-f4e4-5132-80c8-c9e8628b8f17/scratchpad/cfa_calc/last.log; exit $rc; fi; }
R $T/test_ciego.py
R $T/arranque.py $S/cfa_work/plano/bidset_CLEAN.pdf
R $T/alcances.py escanear $PDF escaneo.json
R $T/alcances.py renglones escaneo.json renglones.json
R $T/inventario_tags.py $PDF $W/etapas/1_inventario/runner --sin-recortes
R $T/contar_tags.py $PDF A-202@p13 M2.1 M3.5 W4 W4.1 W6 W8 SW6 --json $W/etapas/1_inventario/contar_tags_A-202.json
R $T/../runner/evidencia.py $C4/takeoff_canon.json $PDF $W/etapas/0_mapa/SHEET_MAP.md $C4/img_runner --canon-out $C4/takeoff_canon.json --inventario $W/etapas/1_inventario/inventario.json
R $W/scripts/evidencia_rfis.py $PDF
R $T/canon.py $C4/takeoff_canon.json $C4/out --fo $C4/fo_in.json
R $W/scripts/rfi16_delta.py $T
R $W/scripts/formato_canon.py
R $T/canon.py $C4/takeoff_canon.json $C4/out --fo $C4/fo_in.json
R $T/inventario.py $C4/takeoff_canon.json $C4/out/inventario_out.json
R $T/framed_openings.py $C4/fo_in.json $C4/out/framed_openings_out.json
R $T/alcance_filtro.py $C4/alcance_in.json $C4/out/alcance_out.json
R $T/vigas_sobre_walls.py $PDF NONE A-202 $C4/takeoff_canon.json --json $C4/vigas_out.json
R $W/scripts/sellar_y_marcar.py $T $PDF
R $T/markups_bluebeam.py $PDF $C4/takeoff_canon.json $W/etapas/6_markups/markups.pdf --json $W/etapas/6_markups/markups.json
R $W/scripts/demo_geom_markups.py
R $T/markups_demo.py $W/etapas/6_markups/markups.pdf $W/etapas/6_markups/demo_geom.json 18 $W/etapas/6_markups/markups_con_demo.pdf $W/etapas/6_markups/demo_png
R $W/scripts/imagenes_hoja.py $T $PDF
R $W/scripts/takeoff_json.py $T
R $W/scripts/evidencias_reglas.py
R $T/plantilla_excel.py validar takeoff.json
R $T/plantilla_excel.py armar takeoff.json $X --familias etapas/4_canon/out/familias_out.json --trabajo etapas
R $T/plantilla_excel.py verificar $X --salidas $C4/out
R $T/registro.py entregable registro.json
R $T/alcances.py compuerta registro.json escaneo.json $X
echo CHAIN-OK
