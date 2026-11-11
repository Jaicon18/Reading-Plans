#!/bin/bash
# Xfinity Interquest rev1 FINAL: delivery folder (structure O'Reilly rev10 / CR rev18, U-145; folder name U-165) + sub-gates + full gate.
set -e
source /root/xf/work/scripts/env.sh
D=$W/entrega; E="$D/rev1 FINAL PARA REVISAR"
rm -rf "$D" && mkdir -p "$E/Take-off" "$E/Planos marcados" "$E/Auditoria/burbujas" "$E/Auditoria/schedules" "$E/Auditoria/review_items" "$E/Auditoria/rfi_img" "$E/Auditoria/resolucion_AB" "$E/Auditoria/barrido_tags" "$E/Auditoria/evidencia"
ln -s $W/etapas $D/takeoff_work_etapas; ln -s $W $D/takeoff_work
cp $W/set_texto.json $W/indep/fichas.json $W/indep/schedules_indep.json $W/proceso/proyecto_datos.json $D/
cp $W/burbujas/burbujas_verificadas.json $D/; cp -a $W/burbujas/img_verif $D/burbujas_img
cp $W/burbujas/img_verif/*.png "$E/Auditoria/burbujas/"; cp $W/burbujas/burbujas_verificadas.json $W/burbujas/CADENA.md $W/burbujas/callouts_no_aplican.json "$E/Auditoria/burbujas/"
cp $W/burbujas/callouts_no_aplican.json $D/
cp $W/indep/schedules_indep.json $W/indep/fichas.json $W/indep/NOTAS.md "$E/Auditoria/schedules/"; cp $W/indep/img/*.png "$E/Auditoria/schedules/" 2>/dev/null || true
X=$W/etapas/8_excel/XF_Takeoff_FINAL_rev1.xlsx
cp $X "$E/Take-off/"; cp $X.sello.json "$E/Take-off/"
cp "$W/etapas/8_excel/XF_markups_rev1b - OPEN IN BLUEBEAM.pdf" "$E/Planos marcados/"
cp "$W/etapas/7_imagenes/"*" - IMAGE ONLY (not editable) - "*" rev1.png" "$E/Planos marcados/"
cp $W/etapas/4_canon/img/review/RFI-*.png "$E/Auditoria/rfi_img/"; cp $W/etapas/4_canon/img/review/*.png "$E/Auditoria/review_items/"
cp $W/etapas/3_revision/resolucion.md $W/etapas/3_revision/revision.md "$E/Auditoria/resolucion_AB/"; cp -a $W/etapas/3_revision/img "$E/Auditoria/resolucion_AB/"
cp $W/etapas/VERIFICACION_MARKUPS.md $W/etapas/TOOL_LIMITS_CALC.md $W/etapas/PROCESO_CORRIDA.md $W/etapas/DEMO_CRUCE.md "$E/Auditoria/"
cp $W/etapas/1_inventario/inventario.md $W/etapas/1_inventario/inventario.json "$E/Auditoria/barrido_tags/"; cp -a $W/etapas/1_inventario/recortes "$E/Auditoria/barrido_tags/"
cp $W/etapas/4_canon/img/*.png "$E/Auditoria/evidencia/"; cp -a $W/etapas/7_imagenes/planmark "$E/Auditoria/evidencia/"
[ -d $W/revision_indep ] && mkdir -p "$E/Auditoria/revision_independiente" && cp -a $W/revision_indep/. "$E/Auditoria/revision_independiente/"
[ -d $W/Proposal ] && mkdir -p "$E/Proposal" && cp -a $W/Proposal/. "$E/Proposal/"
python3 -I $W/scripts/cobertura_lista.py > /dev/null; python3 $T/../runner/cobertura.py $W/etapas/12_cobertura/lista.json $W/etapas/4_canon/takeoff_canon.json $W/takeoff.json $W/etapas/12_cobertura > /dev/null; ls $W/etapas/12_cobertura
for f in $W/etapas/12_cobertura/cobertura.md; do [ -f $f ] && cp $f "$E/Auditoria/COBERTURA_PASO12.md"; done; [ -f $W/etapas/12_cobertura/cobertura.json ] && cp $W/etapas/12_cobertura/cobertura.json "$E/Auditoria/COBERTURA_PASO12.json"
(cd $W && python3 $T/bitacora.py backcheck $W/revision_indep/R1/INFORME_R1.md $W/etapas/8_excel/XF_Takeoff_FINAL_rev1.xlsx | tail -1)
python3 -I $W/scripts/tiempos.py > /dev/null; cp $W/entrega.json $W/TIEMPOS.md $D/; cp $W/TIEMPOS.md "$E/"
python3 -I $W/scripts/hacer_docs.py "$E" $W/proceso/proyecto_datos.json $W/takeoff.json $W/etapas/4_canon/takeoff_canon.json
python3 -I $T/checklist_revision.py "$E/Take-off/XF_Takeoff_FINAL_rev1.xlsx" "$E/Planos marcados/XF_markups_rev1b - OPEN IN BLUEBEAM.pdf" $PDF $W/etapas/4_canon/takeoff_canon.json "$E/CHECKLIST_REVISION.xlsx" --proy XF | tail -2
(cd $D && python3 $T/compuerta_entrega.py detalles . | tail -1)
(cd $D && python3 $T/compuerta_entrega.py schedules . | tail -1)
(cd $D && python3 $T/compuerta_entrega.py banco . --cache /home/user/Reading-Plans > banco.txt 2>&1 || true; tail -3 banco.txt)
(cd $D && timeout 2400 python3 $T/compuerta_entrega.py . > gate.txt 2>&1 || true)
grep -E "^(FAIL|AMBER)|COMPUERTA" $D/gate.txt | head -80
