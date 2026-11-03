#!/bin/bash
# HFT Loveland - stages 4-9 chain (adapted from CFA River Point cadena_rev4.sh). Every tool through bitacora.py run;
# stops at the first rc != 0. K = work dir: default W (final run on etapas/4_canon/takeoff_canon.json);
# K=$W/dryrun for the dry run on a copy of reading A.  Usage: bash scripts/cadena.sh [from_step]
source "$(dirname "$0")/env.sh"
REV=${REV:-rev3}
cd $K; C4=$K/etapas/4_canon; M=$K/etapas/6_markups; X=$K/etapas/8_excel/HFT_Loveland_Takeoff_FINAL_${REV}.xlsx
F=$K/FINAL; FP="$F/Planos marcados"; mkdir -p $C4/out $M $K/etapas/7_imagenes $K/etapas/8_excel "$F/Take-off" "$FP" $F/proceso
ORIGPDF=${ORIGPDF:-$W/plano/bidset_ORIG.pdf}
REV=${REV:-rev3}
N=0; DESDE=${1:-0}
R() { N=$((N+1)); [ $N -lt $DESDE ] && return 0; python3 $T/bitacora.py run "$@" > $K/last.log 2>&1; rc=$?
      echo "$(TZ=America/Los_Angeles date +%H:%M) step $N rc=$rc $(basename $1) $2"
      if [ $rc != 0 ]; then tail -40 $K/last.log; exit $rc; fi; }
R $T/test_ciego.py
R $T/arranque.py $ORIGPDF
R $T/alcances.py escanear $PDF escaneo.json
R $T/alcances.py renglones escaneo.json renglones.json
if [ -f registro.json ]; then N=$((N+1)); else R $T/registro.py crear registro.json renglones.json; fi
R $T/inventario_tags.py $PDF $K/etapas/1_inventario/runner --sin-recortes
R $T/contar_tags.py $PDF A1.1@p8 A B C D E --json $K/etapas/1_inventario/contar_tags_A1.1.json
R $W/scripts/preparar.py
R $W/scripts/disponer_tags.py
R $W/scripts/rev2_canon.py $T
R $W/scripts/rev3_d01_zonas.py $PDF
R $T/../runner/evidencia.py $C4/takeoff_canon.json $PDF $K/etapas/0_mapa/SHEET_MAP.md $C4/img_runner --canon-out $C4/takeoff_canon.json --inventario $K/etapas/1_inventario/inventario.json
R $W/scripts/evidencia_rfis.py $PDF $ORIGPDF
R $W/scripts/formato_canon.py $T $PDF
R $W/scripts/insumos_canon.py fo
R $T/canon.py $C4/takeoff_canon.json $C4/out --fo $C4/fo_in.json
R $T/inventario.py $C4/takeoff_canon.json $C4/out/inventario_out.json
R $T/framed_openings.py $C4/fo_in.json $C4/out/framed_openings_out.json
R $W/scripts/insumos_canon.py alcance
R $T/alcance_filtro.py $C4/alcance_in.json $C4/out/alcance_out.json
R $T/vigas_sobre_walls.py $PDF NONE A1.1@p8 $C4/takeoff_canon.json --json $C4/vigas_out.json   # S2.0 not registrable: TOOL_LIMITS_CALC #1
R $W/scripts/sellar_y_marcar.py $T $PDF
R $T/markups_bluebeam.py $PDF $C4/takeoff_canon.json $M/markups.pdf --json $M/markups.json
R $W/scripts/demo_geom_markups.py
R $T/markups_demo.py $M/markups.pdf $M/demo_geom.json 6.75 $M/markups_con_demo.pdf $M/demo_png
R $T/markups_bluebeam.py verificar $M/markups_con_demo.pdf $C4/takeoff_canon.json
R $W/scripts/imagenes_hoja.py $T $PDF
R $W/scripts/takeoff_json.py $T
R $W/scripts/evidencias_reglas.py
R $T/plantilla_excel.py validar takeoff.json
R $T/plantilla_excel.py armar takeoff.json $X --familias etapas/4_canon/out/familias_out.json --trabajo etapas
R $T/plantilla_excel.py verificar $X --salidas $C4/out
R $W/scripts/registro_marcar.py $T
R $T/registro.py entregable registro.json
R $T/alcances.py compuerta registro.json escaneo.json $X
cp $M/markups_con_demo.pdf $K/etapas/8_excel/HFT_Loveland_markups_${REV}.pdf
R $W/scripts/demo_cruce.py
R $T/verificar_markups_excel.py $K/etapas/8_excel/HFT_Loveland_markups_${REV}.pdf $X $C4/takeoff_canon.json --out $K/etapas/VERIFICACION_MARKUPS.md
# ---- delivery folder FINAL (the README / PARA_REVISAR / SEGUIMIENTO are written by the orchestrator)
cp $X "$F/Take-off/HFT_Loveland_Takeoff_FINAL_${REV}.xlsx"
cp $K/etapas/8_excel/HFT_Loveland_markups_${REV}.pdf "$FP/HFT_Loveland_markups_${REV}.pdf"
rm -f "$FP"/*.png; for p in $K/etapas/7_imagenes/*_marked_by_type_${REV}.png; do b=$(basename $p _marked_by_type_${REV}.png); cp "$p" "$FP/${b}_HFT_Loveland_marked_${REV}.png"; done
cp $K/etapas/VERIFICACION_MARKUPS.md $K/etapas/DEMO_CRUCE.md $K/etapas/TOOL_LIMITS_CALC.md $F/proceso/
# reglas.py compuerta (final mode): the ONLY failure allowed is the missing back-check (separate session, bitacora backcheck)
N=$((N+1)); if [ $N -ge $DESDE ]; then python3 $T/bitacora.py run $T/reglas.py compuerta etapas --excel $X > $K/last.log 2>&1; rc=$?
  nf=$(grep -c "^FALLA" $K/last.log); nb=$(grep -c "^FALLA .*NO HAY BACK-CHECK" $K/last.log)
  echo "$(TZ=America/Los_Angeles date +%H:%M) step $N rc=$rc reglas.py compuerta: $nf failure(s), $nb = back-check pending"
  if [ $rc != 0 ] && [ "$nf" != "$nb" ]; then tail -40 $K/last.log; exit $rc; fi; fi
R $T/etapas.py compuerta etapas
R $T/auditoria_entrega.py "$F/Take-off/HFT_Loveland_Takeoff_FINAL_${REV}.xlsx" "$FP/HFT_Loveland_markups_${REV}.pdf" $C4/takeoff_canon.json --md $F/proceso/AUDITORIA_ENTREGA.md --imagenes "$FP" --rfis-abiertos
cp $K/etapas/PROCESO_CORRIDA.md $F/proceso/
echo CHAIN-OK
