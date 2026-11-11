#!/bin/bash
# Grand Kia rev1 FINAL: carpeta de entrega (estructura CR rev18b / CC rev4 / O'Reilly, U-145) + subcompuertas + compuerta.
set -e
source /root/gk/work/scripts/env.sh
W=$K; REV=${REV:-rev1}
D=$W/entrega; E="$D/$REV FINAL PARA REVISAR"
rm -rf "$D" && mkdir -p "$E/Take-off" "$E/Planos marcados" "$E/Auditoria/burbujas" "$E/Auditoria/schedules" "$E/Auditoria/review_items" "$E/Auditoria/rfi_img" "$E/Auditoria/resolucion_AB" "$E/Auditoria/barrido_tags" "$E/Auditoria/evidencia"
ln -s $W/etapas $D/takeoff_work_etapas; ln -s $W $D/takeoff_work
python3 -I $W/scripts/set_texto_sheetmap.py $W/set_texto.json $W/sheetmap.json > /dev/null || true; cp $W/set_texto.json $W/indep/fichas.json $W/indep/schedules_indep.json $W/proceso/proyecto_datos.json $D/
cp $W/burbujas/burbujas_verificadas.json $D/; cp -a $W/burbujas/img_verif $D/burbujas_img
cp $W/burbujas/img_verif/*.png "$E/Auditoria/burbujas/" 2>/dev/null || true
cp $W/burbujas/burbujas_verificadas.json $W/burbujas/CADENA.md $W/burbujas/callouts_no_aplican.json "$E/Auditoria/burbujas/"
cp $W/indep/schedules_indep.json $W/indep/fichas.json $W/indep/NOTAS.md "$E/Auditoria/schedules/"; cp $W/indep/img/*.png "$E/Auditoria/schedules/" 2>/dev/null || true
X=$W/etapas/8_excel/GK_Takeoff_FINAL_$REV.xlsx
ln -s $X "$E/Take-off/Grand_Kia_Takeoff_FINAL_$REV.xlsx"
[ -f $X.sello.json ] && ln -s $X.sello.json "$E/Take-off/Grand_Kia_Takeoff_FINAL_$REV.xlsx.sello.json"
cp $W/etapas/8_excel/GK_markups_$REV.pdf "$E/Planos marcados/GK_markups_$REV - OPEN IN BLUEBEAM.pdf"
python3 -I $W/scripts/imagenes_hoja.py "$E/Planos marcados/GK_markups_$REV - OPEN IN BLUEBEAM.pdf" "$E/Planos marcados" $REV
cp $W/etapas/4_canon/img/rfi/*.png "$E/Auditoria/rfi_img/" 2>/dev/null || true; cp $W/etapas/4_canon/img/rfi/*.png "$E/Auditoria/review_items/" 2>/dev/null || true
cp $W/etapas/3_revision/resolucion*.md $W/etapas/3_revision/revision.md $W/etapas/3_revision/comparacion_AB.json "$E/Auditoria/resolucion_AB/"
[ -f $W/etapas/3_revision/revision.json ] && cp $W/etapas/3_revision/revision.json "$E/Auditoria/resolucion_AB/"
cp $W/etapas/VERIFICACION_MARKUPS.md $W/etapas/TOOL_LIMITS_CALC.md $W/etapas/PROCESO_CORRIDA.md "$E/Auditoria/"
cp $W/etapas/1_inventario/inventario.md $W/etapas/1_inventario/inventario.json "$E/Auditoria/barrido_tags/"; cp -a $W/etapas/1_inventario/recortes "$E/Auditoria/barrido_tags/"
cp $W/etapas/7_imagenes/*.png "$E/Auditoria/evidencia/" 2>/dev/null || true
cp -a $W/etapas/4_canon/img/det $W/etapas/4_canon/img/gaps "$E/Auditoria/evidencia/" 2>/dev/null || true
cp $W/comparacion_sets.json "$E/Auditoria/comparacion_sets_Brinkman_vs_Crossland.json"
[ -d $W/revision_independiente ] && mkdir -p "$E/Auditoria/revision_independiente" && cp -a $W/revision_independiente/. "$E/Auditoria/revision_independiente/"
[ -d $W/Proposal ] && mkdir -p "$E/Proposal" && cp -a $W/Proposal/. "$E/Proposal/"
python3 -I $W/scripts/tiempos.py > /dev/null; cp $W/entrega.json $W/TIEMPOS.md $D/; cp $W/TIEMPOS.md "$E/"
python3 -I $W/scripts/cobertura_lista.py > /dev/null; python3 $T/../runner/cobertura.py $W/etapas/12_cobertura/lista.json $W/etapas/4_canon/takeoff_canon.json $W/takeoff.json $W/etapas/12_cobertura/cobertura > /dev/null
cp $W/etapas/12_cobertura/cobertura.md "$E/Auditoria/COBERTURA_PASO12.md"; cp $W/etapas/12_cobertura/cobertura.json "$E/Auditoria/COBERTURA_PASO12.json"
python3 -I $W/scripts/demo_cruce.py > /dev/null; [ -f $W/etapas/DEMO_CRUCE.md ] && cp $W/etapas/DEMO_CRUCE.md "$E/Auditoria/"
python3 -I $W/scripts/hacer_docs.py "$E" $W/proceso/proyecto_datos.json $W/takeoff.json $W/etapas/4_canon/takeoff_canon.json
# U-175 / U-176: final height table of the two blind readings + directed resolution
cp $W/alturas/FINAL/*.csv "$E/Auditoria/"; mkdir -p "$E/Auditoria/alturas"; cp -a $W/alturas/A $W/alturas/B $W/alturas/RESOL $W/alturas/BRIEF_*.md "$E/Auditoria/alturas/"
python3 -I $W/scripts/review_imgs.py "$E" $X
MK="$E/Planos marcados/GK_markups_$REV - OPEN IN BLUEBEAM.pdf"; XL="$E/Take-off/Grand_Kia_Takeoff_FINAL_$REV.xlsx"
python3 -I $T/compuerta_entrega.py vista_bluebeam "$MK" "$XL" --canon $W/etapas/4_canon/takeoff_canon.json --csv "$E/Auditoria/VISTA_BLUEBEAM.csv" | tail -1
python3 -I $T/comparar_alturas.py "$E/Auditoria/VISTA_BLUEBEAM.csv" "$XL" "$E/Auditoria/ALTURAS_IMPRESAS.csv" "$E/Auditoria/COMPARACION_ALTURAS.csv" | tail -4 | tee $W/alturas_3lados.txt || true
python3 -I $T/comparar_alturas.py extremo "$E" $W/etapas/4_canon/takeoff_canon.json "$MK" | tee $W/alturas_extremo.txt || true
python3 -I $T/compuerta_entrega.py vista_bluebeam "$MK" "$XL" --canon $W/etapas/4_canon/takeoff_canon.json --csv "$E/Auditoria/VISTA_BLUEBEAM.csv" | tail -1
python3 -I $T/comparar_alturas.py "$E/Auditoria/VISTA_BLUEBEAM.csv" "$XL" "$E/Auditoria/ALTURAS_IMPRESAS.csv" "$E/Auditoria/COMPARACION_ALTURAS.csv" > /dev/null || true
cp $W/entrega_schedules_materiales.json $D/schedules_materiales.json
python3 -I $T/checklist_revision.py "$XL" "$MK" $W/plans/GK_set_SIN_MARKUPS.pdf $W/etapas/4_canon/takeoff_canon.json "$E/GK_CHECKLIST_REVISION.xlsx" --proy GK --b2-3lados "$E/Auditoria/COMPARACION_ALTURAS.csv" --b2-muestra "$E/Auditoria/ALTURAS_MUESTRA.json" | tail -2
(cd $D && python3 $T/compuerta_entrega.py detalles . | tail -1)
(cd $D && python3 $T/compuerta_entrega.py schedules . | tail -1)
(cd $D && python3 $T/compuerta_entrega.py banco . --cache /home/user/Reading-Plans > banco.txt 2>&1 || true; tail -3 banco.txt)
(cd $D && timeout 2400 python3 $T/compuerta_entrega.py . > gate.txt 2>&1 || true)
grep -E "^(FAIL|AMBER)|COMPUERTA" $D/gate.txt | head -80
