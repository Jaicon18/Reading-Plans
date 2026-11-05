#!/bin/bash
# Consumer Cellular Centennial - stages 4-9 chain (adapted from HFT Loveland cadena.sh). Every tool through bitacora.py run;
# stops at the first rc != 0.  Usage: bash scripts/cadena.sh [from_step]
source /root/cc/work/scripts/env.sh
REV=${REV:-rev1}; export REV
cd $K; C4=$K/etapas/4_canon; M=$K/etapas/6_markups; X=$K/etapas/8_excel/Consumer_Cellular_Centennial_Takeoff_FINAL_${REV}.xlsx
mkdir -p $C4/out $M $K/etapas/7_imagenes $K/etapas/8_excel
N=0; DESDE=${1:-0}
R() { N=$((N+1)); [ $N -lt $DESDE ] && return 0; python3 $T/bitacora.py run "$@" > $K/last.log 2>&1; rc=$?
      echo "$(TZ=America/Los_Angeles date +%H:%M) step $N rc=$rc $(basename $1) $2"
      if [ $rc != 0 ]; then tail -30 $K/last.log | grep -v -i "warn"; exit $rc; fi; }
[ ${1:-0} -le 1 ] && python3 -I scripts/resolver_AB.py > /dev/null
R scripts/ajustes_canon.py
R scripts/rfis.py
R scripts/preparar.py
R $T/inventario_tags.py $PDF $K/etapas/1_inventario/runner --sin-recortes
R $T/contar_tags.py $PDF A100@p7 A3 C3 D E3 --json $K/etapas/1_inventario/contar_tags_A100.json
R $T/../runner/evidencia.py $C4/takeoff_canon.json $PDF $K/etapas/0_mapa/SHEET_MAP.md $C4/img_runner --canon-out $C4/takeoff_canon.json --inventario $K/etapas/1_inventario/inventario.json
R $T/canon.py $C4/takeoff_canon.json $C4/out
R scripts/insumos_canon.py fo
R $T/inventario.py $C4/takeoff_canon.json $C4/out/inventario_out.json
R $T/framed_openings.py $C4/fo_in.json $C4/out/framed_openings_out.json
R scripts/insumos_canon.py alcance
R $T/alcance_filtro.py $C4/alcance_in.json $C4/out/alcance_out.json
R $T/vigas_sobre_walls.py $PDF NONE A100@p7 $C4/takeoff_canon.json --json $C4/vigas_out.json
R scripts/sellar_y_marcar.py $T $PDF
R $T/markups_bluebeam.py $PDF $C4/takeoff_canon.json $M/markups.pdf --json $M/markups.json
R scripts/demo_geom.py
R scripts/demo_geom_markups.py
R $T/markups_demo.py $M/markups.pdf $M/demo_geom.json 18.0 $M/markups_con_demo.pdf $M/demo_png
R $T/markups_bluebeam.py verificar $M/markups_con_demo.pdf $C4/takeoff_canon.json
python3 -I scripts/rcp_polys.py > /dev/null
R $T/markups_rcp.py $M/markups_con_demo.pdf $C4/takeoff_canon.json $M/rcp_polys.json $M/markups_con_rcp.pdf $M/rcp_png
R scripts/imagenes_hoja.py $T $PDF
R scripts/takeoff_json.py $T
R scripts/evidencias_reglas.py
R $T/plantilla_excel.py validar takeoff.json
R $T/plantilla_excel.py armar takeoff.json $X --familias etapas/4_canon/out/familias_out.json --trabajo etapas
R $T/plantilla_excel.py verificar $X --salidas $C4/out
R scripts/registro_marcar.py $T
R $T/registro.py entregable registro.json
R $T/alcances.py compuerta registro.json escaneo.json $X
cp $M/markups_con_rcp.pdf $K/etapas/8_excel/Consumer_Cellular_Centennial_markups_${REV}.pdf
R $T/verificar_markups_excel.py $K/etapas/8_excel/Consumer_Cellular_Centennial_markups_${REV}.pdf $X $C4/takeoff_canon.json --out $K/etapas/VERIFICACION_MARKUPS.md
echo CHAIN-OK
