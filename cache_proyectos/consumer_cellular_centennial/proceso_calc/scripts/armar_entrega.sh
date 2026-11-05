#!/bin/bash
# Builds the rev1 FINAL delivery folder (structure = O'Reilly rev10 FINAL, U-145) from the chain run, then the gate subcommands.
set -e
source /root/cc/work/scripts/env.sh
D=$W/entrega; E="$D/rev1 FINAL — ESTA ES LA VERSIÓN FINAL PARA REVISAR"
rm -rf "$D" && mkdir -p "$E/Take-off" "$E/Planos marcados" "$E/Auditoria/burbujas" "$E/Auditoria/schedules" "$E/Auditoria/review_items" "$E/Auditoria/rfi_img" "$E/Auditoria/backcheck"
ln -s $W/etapas $D/takeoff_work_etapas
ln -s $W $D/takeoff_work
python3 -I $W/scripts/burbujas_destinos.py > /dev/null
cp $W/set_texto.json $W/indep/fichas.json $W/indep/schedules_indep.json $W/proceso/proyecto_datos.json $D/
cp $W/burbujas/burbujas_verificadas.json $D/; cp -a $W/burbujas/img_verif $D/burbujas_img
cp $W/burbujas/img_verif/*.png "$E/Auditoria/burbujas/"; cp $W/burbujas/burbujas_verificadas.json $W/burbujas/CADENA.md "$E/Auditoria/burbujas/"
cp $W/indep/schedules_indep.json $W/indep/fichas.json $W/indep/fichas_lector_original.json $W/indep/NOTAS.md "$E/Auditoria/schedules/"; cp $W/indep/img/*.png "$E/Auditoria/schedules/" 2>/dev/null || true
X=$W/etapas/8_excel/Consumer_Cellular_Centennial_Takeoff_FINAL_rev1.xlsx
ln -s $X "$E/Take-off/Consumer_Cellular_Centennial_Takeoff_FINAL_rev1.xlsx"
[ -f $X.sello.json ] && ln -s $X.sello.json "$E/Take-off/Consumer_Cellular_Centennial_Takeoff_FINAL_rev1.xlsx.sello.json"
cp $W/etapas/8_excel/Consumer_Cellular_Centennial_markups_rev1.pdf "$E/Planos marcados/Consumer_Cellular_Centennial_markups_rev1.pdf"
for p in $W/etapas/7_imagenes/planmark/A100_type_*.png; do cp $p "$E/Planos marcados/"; done
for p in $W/etapas/7_imagenes/*_marked_by_type_rev1.png; do cp $p "$E/Planos marcados/"; done
cp $W/etapas/6_markups/demo_png/*.png "$E/Planos marcados/" 2>/dev/null || true
cp $W/etapas/6_markups/rcp_png/*.png "$E/Planos marcados/" 2>/dev/null || true
cp $W/etapas/4_canon/img/rfi/*.png "$E/Auditoria/rfi_img/"; cp $W/etapas/4_canon/img/rfi/*.png "$E/Auditoria/review_items/"
cp $W/etapas/4_canon/img/demo_check.png $W/etapas/4_canon/img/rcp_check.png "$E/Auditoria/"
cp $W/etapas/3_revision/resolucion.md $W/etapas/3_revision/revision.md $W/etapas/VERIFICACION_MARKUPS.md $W/etapas/TOOL_LIMITS_CALC.md $W/etapas/DEMO_CRUCE.md $W/etapas/PROCESO_CORRIDA.md "$E/Auditoria/"
mkdir -p "$E/Auditoria/barrido_tags" && cp $W/etapas/1_inventario/recortes/*.png $W/etapas/1_inventario/inventario.md $W/etapas/1_inventario/mapa_PC_a_PT.json "$E/Auditoria/barrido_tags/"
cp $W/comparacion_sets.json "$E/Auditoria/comparacion_sets_Elite_vs_ElderJones.json"
[ -f $W/etapas/5_auditoria/BACKCHECK_INFORME.md ] && cp $W/etapas/5_auditoria/BACKCHECK_INFORME.md "$E/Auditoria/backcheck/" && cp $W/etapas/5_auditoria/img_bc/*.png "$E/Auditoria/backcheck/" 2>/dev/null || true
python3 -I $W/scripts/tiempos.py > /dev/null; cp $W/entrega.json $W/TIEMPOS.md $D/
python3 -I $W/scripts/hacer_docs.py "$E" $W/proceso/proyecto_datos.json $W/takeoff.json $W/etapas/4_canon/takeoff_canon.json
(cd $D && python3 $T/compuerta_entrega.py detalles . | tail -1)
(cd $D && python3 $T/compuerta_entrega.py schedules . | tail -1)
(cd $D && python3 $T/compuerta_entrega.py banco . --cache /home/user/reading-plans > banco.txt 2>&1 || true; tail -3 banco.txt)
(cd $D && timeout 1800 python3 $T/compuerta_entrega.py . > gate.txt 2>&1 || true)
grep -E "^(FAIL|AMBER)|COMPUERTA" $D/gate.txt
