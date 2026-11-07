#!/bin/bash
# CR City Hotel - cadena pasos 4-7 (cada tool por bitacora.py run; para en el primer rc != 0). Uso: bash scripts/cadena.sh [desde]
source /root/cr/work/scripts/env.sh
REV=${REV:-rev4}; cd $W; C4=$W/etapas/4_canon; X=$W/etapas/8_excel/CR_City_Hotel_Takeoff_FINAL_${REV}.xlsx
N=0; DESDE=${1:-0}
R() { N=$((N+1)); [ $N -lt $DESDE ] && return 0; python3 $T/bitacora.py run "$@" > $W/last.log 2>&1; rc=$?
      echo "$(TZ=America/Los_Angeles date +%H:%M) step $N rc=$rc $(basename $1) $2"
      if [ $rc != 0 ]; then tail -25 $W/last.log | grep -v -i "warn"; exit $rc; fi; }
R scripts/comparar_AB.py
R scripts/canon_AB.py
R $T/comparar.py $W/etapas/2_lectura/canon_A.json $W/etapas/2_lectura/canon_B.json $W/etapas/1_inventario/inventario.json $W/etapas/3_revision --pdf $PDF
R $T/comparar_extra.py $W/etapas/2_lectura/canon_A.json $W/etapas/2_lectura/canon_B.json $W/etapas/1_inventario/inventario.json $W/etapas/3_revision
R scripts/build_canon.py
R scripts/vanos_puertas.py
R scripts/esquinas_cb.py
R scripts/finalizar_canon.py
R scripts/shafts_l3l4.py
R scripts/banos_cbu.py
R scripts/canon_extras.py
R scripts/imagenes_walls.py
R scripts/rfis.py
R $T/inventario.py $C4/takeoff_canon.json $C4/out/inventario_walls.json
R scripts/sellos_evidencia.py
R $T/test_ciego_tools.py
R scripts/rcp_polys.py
R $T/canon.py $C4/takeoff_canon.json $C4/out
R scripts/insumos_canon.py fo
R $T/framed_openings.py $C4/fo_in.json $C4/out/framed_openings_out.json
R scripts/insumos_canon.py alcance
R $T/alcance_filtro.py $C4/alcance_in.json $C4/out/alcance_out.json
R $T/markups_bluebeam.py $PDF $C4/takeoff_canon.json $W/etapas/6_markups/markups.pdf --json $W/etapas/6_markups/markups.json --inventario $W/etapas/1_inventario/paginas_hojas.json
R $T/markups_rcp.py $W/etapas/6_markups/markups.pdf $C4/takeoff_canon.json $W/etapas/6_markups/rcp_polys.json $W/etapas/6_markups/markups_con_rcp.pdf $W/etapas/6_markups/rcp_png
R scripts/imagenes_hoja.py
R $T/vigas_sobre_walls.py $PDF NONE A2.02@p18 $C4/takeoff_canon.json --json $C4/out/vigas_out.json
R scripts/evidencias_reglas.py
R scripts/takeoff_json.py $T
R scripts/cobertura.py
R $T/plantilla_excel.py validar takeoff.json
R $T/plantilla_excel.py armar takeoff.json $X --familias $C4/out/familias_out.json --trabajo etapas
R scripts/registro_marcar.py $T
R $T/registro.py entregable registro.json
R $T/alcances.py compuerta registro.json escaneo.json $X
cp $W/etapas/6_markups/markups_con_rcp.pdf $W/etapas/8_excel/CR_City_Hotel_markups_${REV}.pdf
R $T/verificar_markups_excel.py $W/etapas/8_excel/CR_City_Hotel_markups_${REV}.pdf $X $C4/takeoff_canon.json --out $W/etapas/VERIFICACION_MARKUPS.md
echo CHAIN-OK
