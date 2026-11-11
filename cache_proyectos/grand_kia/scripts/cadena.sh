#!/bin/bash
# Grand Kia - cadena etapas 4-9 (adaptada de Consumer Cellular / CR City Hotel). Toda tool por bitacora.py run; para al
# primer rc != 0.  Uso: bash scripts/cadena.sh [desde_paso]
source /root/gk/work/scripts/env.sh
REV=${REV:-rev1}; export REV
cd $K; C4=$K/etapas/4_canon; M=$K/etapas/6_markups; X=$K/etapas/8_excel/GK_Takeoff_FINAL_${REV}.xlsx
mkdir -p $C4/out $M $K/etapas/7_imagenes $K/etapas/8_excel
N=0; DESDE=${1:-0}
R() { N=$((N+1)); [ $N -lt $DESDE ] && return 0; python3 -W ignore $T/bitacora.py run "$@" > $K/last.log 2>&1; rc=$?
      echo "$(TZ=America/Los_Angeles date +%H:%M) step $N rc=$rc $(basename $1) $2"
      if [ $rc != 0 ]; then tail -30 $K/last.log | grep -v -i "warn"; exit $rc; fi; }
if [ $DESDE -le 1 ]; then python3 -I scripts/rfi_barrido.py > /dev/null && python3 -I scripts/img_walls.py > /dev/null && python3 -I scripts/misc_gen.py > /dev/null && python3 -I scripts/build_canon.py > /dev/null && python3 -W ignore $T/bitacora.py run scripts/disponer_tags.py | tail -3 && python3 -I scripts/rcp_polys.py > /dev/null && python3 -I scripts/alturas_final.py > /dev/null && python3 -I scripts/alcance_notas.py > /dev/null; fi
R $T/canon.py $C4/takeoff_canon.json $C4/out
R $T/inventario.py $C4/takeoff_canon.json $C4/out/inventario_out.json
R $T/test_ciego_tools.py
R scripts/sellar_y_marcar.py $T $K/plans/GK_set_SIN_MARKUPS.pdf
R $T/markups_bluebeam.py $PDF $C4/takeoff_canon.json $M/markups.pdf --json $M/markups.json
R $T/markups_demo.py $M/markups.pdf $C4/demo_geom_out.json 6.75 $M/markups_con_demo.pdf $M/demo_png
R $T/markups_bluebeam.py verificar $M/markups_con_demo.pdf $C4/takeoff_canon.json
R $T/markups_rcp.py $M/markups_con_demo.pdf $C4/takeoff_canon.json $M/rcp_polys.json $M/markups_con_rcp.pdf $M/rcp_png
R $T/quitar_firmas_labels.py $M/markups_con_rcp.pdf $M/markups_labels.pdf $K/etapas/1_inventario/inventario.json "$(python3 -I scripts/labels.py)"
R $T/markups_rcp.py excluded $M/markups_labels.pdf $C4/rcp_cuartos.json --out $M/markups_excl.pdf
python3 -I scripts/alcance_notas.py > /dev/null
R scripts/takeoff_json.py $T
R $T/plantilla_excel.py validar takeoff.json
R $T/plantilla_excel.py armar takeoff.json $X --familias etapas/4_canon/out/familias_out.json --trabajo etapas
R $T/plantilla_excel.py verificar $X --salidas $C4/out
R scripts/registro_marcar.py $T
R $T/registro.py entregable registro.json
R $T/alcances.py compuerta registro.json escaneo.json $X
cp $M/markups_excl.pdf $K/etapas/8_excel/GK_markups_${REV}.pdf
R $T/verificar_markups_excel.py $K/etapas/8_excel/GK_markups_${REV}.pdf $X $C4/takeoff_canon.json --out $K/etapas/VERIFICACION_MARKUPS.md
python3 -I scripts/backcheck_md.py > /dev/null && python3 -W ignore $T/bitacora.py backcheck $K/etapas/BACKCHECK_rev1.md $X | tail -1
echo CHAIN-OK
