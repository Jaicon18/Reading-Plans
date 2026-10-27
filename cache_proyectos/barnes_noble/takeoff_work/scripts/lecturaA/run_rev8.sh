# rev5: cadena completa (build -> canon -> tools -> excel)
W=/tmp/claude-0/-home-user-Reading-Plans/b9c208e2-64c4-5dc6-9d1d-2546bd4c85dc/scratchpad; T=$W/skill/take-off-metal-frame-drywall/tools
export REV1=1 REV2=1 REV3=1 REV4=1 REV5=1 REV6=1 REV7=1 REV8=1
(cd $W/lecturaA && bash run_final.sh 1 >/dev/null 2>&1)
cd /home/user/Reading-Plans/cache_proyectos/barnes_noble/takeoff_work; export BITACORA=$PWD/bitacora.jsonl; K=$PWD; P=$W/bidset/bidset_SIN_MARKUPS.pdf; X=etapas/8_excel/Barnes_Noble_ColoradoSprings_Takeoff_FINAL_rev8.xlsx
python3 $T/bitacora.py run $T/canon.py $K/etapas/4_canon/takeoff_canon.json $K/etapas/4_canon/out --fo $K/etapas/4_canon/fo_in.json >/dev/null 2>&1; echo canon $(tail -1 bitacora.jsonl | python3 -c "import json,sys;print(json.load(sys.stdin)['rc'])")
for a in "$T/inventario.py etapas/4_canon/takeoff_canon.json etapas/4_canon/out/inventario_out.json" "$T/vigas_sobre_walls.py $P NONE A-101 $K/etapas/4_canon/takeoff_canon.json --json $K/etapas/4_canon/vigas_out.json" "$T/framed_openings.py $K/etapas/4_canon/fo_in.json $K/etapas/4_canon/out/framed_openings_out.json" "$T/alcance_filtro.py $K/etapas/4_canon/alcance_in.json $K/etapas/4_canon/out/alcance_out.json" "scripts/sellar_y_marcar.py $T $P" "$T/markups_bluebeam.py $P $K/etapas/4_canon/takeoff_canon.json $K/etapas/6_markups/markups.pdf --json $K/etapas/6_markups/markups.json" "scripts/markups_existing.py $T $K/etapas/6_markups/markups.pdf $K/etapas/4_canon/existing_excluded.json"; do python3 $T/bitacora.py run $a 2>&1 | tail -1 | grep -o 'rc=[0-9]'; done | sort | uniq -c
python3 $W/lecturaA/excel_json.py >/dev/null || { echo EXCEL_JSON_FAIL; exit 1; }
python3 $T/bitacora.py run $T/plantilla_excel.py validar takeoff.json 2>&1 | tail -1 | grep -o 'rc=.'
python3 $T/bitacora.py run $T/plantilla_excel.py armar takeoff.json $X --familias etapas/4_canon/out/familias_out.json --trabajo etapas 2>&1 | tail -2 | head -1
