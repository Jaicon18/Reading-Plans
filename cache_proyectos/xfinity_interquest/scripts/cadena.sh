#!/bin/bash
# Xfinity - Interquest, Colorado Springs, CO (BCI National) - stages 4-8 chain (same step order as the reference chain).
# Every tool through bitacora.py run; stops at the first rc != 0.  Usage: bash scripts/cadena.sh [from_step]
# Our canon resolution = scripts/resolver.py + scripts/formato.py (the reference ajustes_canon.py / build_canon.py /
# resolver_AB.py are of another project and are NOT run). Stage 3 (comparar.py / comparar_extra.py) is closed in
# etapas/3_revision and not re-run here.
source /root/xf/work/scripts/env.sh
REV=${REV:-rev1}; export REV
cd $K; C4=$K/etapas/4_canon; M=$K/etapas/6_markups; X=$K/etapas/8_excel/XF_Takeoff_FINAL_${REV}.xlsx
PDFREV=${PDFREV:-rev1b}; FINAL="$K/etapas/8_excel/XF_markups_${PDFREV} - OPEN IN BLUEBEAM.pdf"  # BE-XF07: rev1b = leyenda con Subject LEGEND
mkdir -p $C4/out $M $K/etapas/7_imagenes $K/etapas/8_excel
N=0; DESDE=${1:-0}
R() { N=$((N+1)); [ $N -lt $DESDE ] && return 0; python3 $T/bitacora.py run "$@" > $K/last.log 2>&1; rc=$?
      echo "$(TZ=America/Los_Angeles date +%H:%M) step $N rc=$rc $(basename $1) $2"
      if [ $rc != 0 ]; then tail -30 $K/last.log | grep -v -i "warn"; exit $rc; fi; }
if [ ${1:-0} -le 1 ]; then rm -f $K/registro.json $K/escaneo.json; fi      # fresh run: the ledger is rebuilt by this chain
R scripts/normalizar_B.py
R $T/comparar.py $K/etapas/2_lectura/canon_A.json $K/etapas/2_lectura/canon_B.json $K/etapas/1_inventario/inventario.json $K/etapas/3_revision --pdf $PDF
R $T/comparar_extra.py $K/etapas/2_lectura/canon_A.json $K/etapas/2_lectura/canon_B.json $K/etapas/1_inventario/inventario.json $K/etapas/3_revision
R scripts/resolver.py
R scripts/formato.py
R scripts/preparar.py
R $T/arranque.py $PDF
R $T/inventario_tags.py $PDF $K/etapas/1_inventario_runner --sin-recortes
R $T/contar_tags.py $PDF A2.0@p5 W1 W2 W2A W3 W4 --json $K/etapas/1_inventario/contar_tags_A2.0.json
R $T/../runner/evidencia.py $C4/takeoff_canon.json $PDF $K/etapas/0_mapa/SHEET_MAP.md $C4/img_runner --canon-out $C4/takeoff_canon.json --inventario $K/etapas/1_inventario/inventario.json
R scripts/alturas_img.py
R $T/canon.py $C4/takeoff_canon.json $C4/out
R scripts/insumos_canon.py fo
R $T/inventario.py $C4/takeoff_canon.json $C4/out/inventario_out.json
R $T/framed_openings.py $C4/fo_in.json $C4/out/framed_openings_out.json
R scripts/insumos_canon.py alcance
R $T/alcance_filtro.py $C4/alcance_in.json $C4/out/alcance_out.json
R $T/vigas_sobre_walls.py $PDF NONE A2.0@p5 $C4/takeoff_canon.json --json $C4/vigas_out.json
R scripts/sellar_y_marcar.py $T $PDF
R $T/markups_bluebeam.py $PDF $C4/takeoff_canon.json $M/markups.pdf --json $M/markups.json
R scripts/demo_geom.py
R scripts/demo_geom_markups.py
R scripts/demo_cruce.py
R $T/markups_demo.py $M/markups.pdf $M/demo_geom.json 18.0 $M/markups_con_demo.pdf $M/demo_png
R $T/markups_bluebeam.py verificar $M/markups_con_demo.pdf $C4/takeoff_canon.json
R scripts/rcp_polys.py
R $T/markups_rcp.py $M/markups_con_demo.pdf $C4/takeoff_canon.json $M/rcp_polys.json $M/markups_con_rcp.pdf $M/rcp_png
R scripts/excluded_rcp.py $T $M/markups_con_rcp.pdf $M/markups_con_excluded0.pdf
R scripts/cf_markups.py $M/markups_con_excluded0.pdf $M/markups_con_excluded1.pdf
R scripts/quitar_shx_markups.py $M/markups_con_excluded1.pdf $M/markups_con_excluded2.pdf
R scripts/leyendas_hojas.py $M/markups_con_excluded2.pdf $M/markups_con_excluded.pdf
R scripts/rcp_cuartos_extra.py
R scripts/verificar_final.py $T $M/markups_con_excluded.pdf
R scripts/imagenes_hoja.py $T $PDF
R $T/alcances.py escanear $PDF $K/escaneo.json
R $T/alcances.py renglones $K/escaneo.json $K/etapas/alcances_renglones.json
R scripts/registro_renglones.py
R $T/registro.py crear $K/registro.json $K/etapas/registro_renglones.json
R scripts/takeoff_json.py $T
R scripts/evidencias_reglas.py
R $T/plantilla_excel.py validar takeoff.json
R $T/plantilla_excel.py armar takeoff.json $X --familias etapas/4_canon/out/familias_out.json --trabajo etapas
R $T/plantilla_excel.py verificar $X --salidas $C4/out
R scripts/registro_marcar.py $T
R $T/registro.py entregable registro.json
R $T/alcances.py compuerta registro.json escaneo.json $X
cp $M/markups_con_excluded.pdf "$FINAL"
R scripts/verificar_final.py $T "$FINAL"
R $T/verificar_markups_excel.py "$FINAL" $X $C4/takeoff_canon.json --out $K/etapas/VERIFICACION_MARKUPS.md
echo CHAIN-OK
