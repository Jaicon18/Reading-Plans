#!/bin/bash
# CR City Hotel rev4 FINAL: carpeta de entrega (estructura O'Reilly rev30, U-145) + subcompuertas + compuerta completa.
set -e
source /root/cr/work/scripts/env.sh
D=$W/entrega; E="$D/rev4 FINAL — ESTA ES LA VERSIÓN FINAL PARA REVISAR"
rm -rf "$D" && mkdir -p "$E/Take-off" "$E/Planos marcados" "$E/Auditoria/burbujas" "$E/Auditoria/schedules" "$E/Auditoria/review_items" "$E/Auditoria/rfi_img" "$E/Auditoria/resolucion_AB" "$E/Auditoria/barrido_tags"
ln -s $W/etapas $D/takeoff_work_etapas; ln -s $W $D/takeoff_work
# burbujas_unir.py ya corrido; burbujas_verificadas.json final (con destinos agregados a mano) es la fuente -- no re-unir
cp $W/set_texto.json $W/indep/fichas.json $W/indep/schedules_indep.json $W/proceso/proyecto_datos.json $D/
cp $W/burbujas/burbujas_verificadas.json $D/; cp -a $W/burbujas/img_verif $D/burbujas_img
cp $W/burbujas/img_verif/*.png "$E/Auditoria/burbujas/"; cp $W/burbujas/burbujas_verificadas.json $W/burbujas/CADENA.md $W/burbujas/callouts_no_aplican.json "$E/Auditoria/burbujas/"
cp $W/indep/schedules_indep.json $W/indep/fichas.json $W/indep/NOTAS.md "$E/Auditoria/schedules/"; cp $W/indep/img/*.png "$E/Auditoria/schedules/" 2>/dev/null || true
X=$W/etapas/8_excel/CR_City_Hotel_Takeoff_FINAL_rev4.xlsx
ln -s $X "$E/Take-off/CR_City_Hotel_Takeoff_FINAL_rev4.xlsx"
[ -f $X.sello.json ] && ln -s $X.sello.json "$E/Take-off/CR_City_Hotel_Takeoff_FINAL_rev4.xlsx.sello.json"
cp $W/etapas/8_excel/CR_City_Hotel_markups_rev4.pdf "$E/Planos marcados/"
cp $W/etapas/7_imagenes/*_marked_by_type_rev4.png "$E/Planos marcados/"
cp $W/etapas/6_markups/rcp_png/*.png "$E/Planos marcados/" 2>/dev/null || true
cp $W/etapas/4_canon/img/rfi/*.png "$E/Auditoria/rfi_img/"; cp $W/etapas/4_canon/img/rfi/*.png "$E/Auditoria/review_items/"
cp $W/etapas/3_revision/resolucion*.md $W/etapas/3_revision/revision.md $W/etapas/3_revision/comparacion_AB.json "$E/Auditoria/resolucion_AB/"
cp $W/etapas/COBERTURA_PASO12.md $W/etapas/COBERTURA_PASO12.json "$E/Auditoria/"; cp $W/etapas/VERIFICACION_MARKUPS.md $W/etapas/TOOL_LIMITS_CALC.md $W/etapas/PROCESO_CORRIDA.md $W/etapas/6_markups/rcp_polys_check.json "$E/Auditoria/"
cp $W/etapas/1_inventario/inventario.md $W/etapas/1_inventario/inventario.json "$E/Auditoria/barrido_tags/"; cp -a $W/etapas/1_inventario/recortes "$E/Auditoria/barrido_tags/"; mkdir -p "$E/Auditoria/evidencia_walls"; cp -a $W/etapas/7_imagenes/walls $W/etapas/7_imagenes/alturas "$E/Auditoria/evidencia_walls/"
cp $W/comparacion_sets.json "$E/Auditoria/comparacion_sets_2025_vs_2026.json"
[ -d $W/auditoria_U138 ] && mkdir -p "$E/Auditoria/auditoria_U138" && cp -a $W/auditoria_U138/. "$E/Auditoria/auditoria_U138/"
[ -d $W/auditoria_U138_2 ] && mkdir -p "$E/Auditoria/auditoria_U138_2" && cp -a $W/auditoria_U138_2/INFORME_AUDITORIA_U138_2.md $W/auditoria_U138_2/RESOLUCION_HALLAZGOS_U138_2.md $W/auditoria_U138_2/BRIEF.md $W/auditoria_U138_2/img "$E/Auditoria/auditoria_U138_2/"
[ -d $W/Proposal ] && mkdir -p "$E/Proposal" && cp -a $W/Proposal/. "$E/Proposal/"
python3 -I $W/scripts/tiempos.py > /dev/null; cp $W/entrega.json $W/TIEMPOS.md $D/
python3 -I $W/scripts/delta_rev.py rev1 rev2 > /dev/null; python3 -I $W/scripts/delta_rev.py rev2 rev3 > /dev/null; python3 -I $W/scripts/delta_rev.py rev3 rev4 > /dev/null; cp $W/etapas/DELTA_rev1_rev2.md $W/etapas/DELTA_rev2_rev3.md $W/etapas/DELTA_rev3_rev4.md "$E/Auditoria/"; mkdir -p "$E/Auditoria/rcp_rev4"; cp $W/etapas/4_canon/img/rcp_rev4/*.png "$E/Auditoria/rcp_rev4/"
python3 -I $W/scripts/hacer_docs.py "$E" $W/proceso/proyecto_datos.json $W/takeoff.json $W/etapas/4_canon/takeoff_canon.json
(cd $D && python3 $T/compuerta_entrega.py detalles . | tail -1)
(cd $D && python3 $T/compuerta_entrega.py schedules . | tail -1)
(cd $D && python3 $T/compuerta_entrega.py banco . --cache /home/user/reading-plans > banco.txt 2>&1 || true; tail -3 banco.txt)
(cd $D && timeout 2400 python3 $T/compuerta_entrega.py . > gate.txt 2>&1 || true)
grep -E "^(FAIL|AMBER)|COMPUERTA" $D/gate.txt | head -60
