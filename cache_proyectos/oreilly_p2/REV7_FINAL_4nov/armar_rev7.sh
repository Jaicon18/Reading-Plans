#!/bin/bash
# Arma la carpeta de entrega rev5 desde una corrida ($1 = run25x): Excel / sello por symlink (la bitácora los registró
# ahí: _vigente compara por realpath), markups + PNG A1.1_type_<T>.png, docs desde el Excel, ENTREGA_OK con la compuerta.
set -e
R=/tmp/claude-scratch/oreilly_p2; RUN=$R/$1; W=$R/rev7c; E="$W/rev7 FINAL — ESTA ES LA VERSIÓN FINAL PARA REVISAR"
T=$R/v81cf33/take-off-metal-frame-drywall/tools
[ -f $RUN/takeoff_work/etapas/5_auditoria/BACKCHECK_INFORME.md.rev6 ] || cp $R/run25a/takeoff_work/etapas/5_auditoria/BACKCHECK_INFORME.md $RUN/takeoff_work/etapas/5_auditoria/BACKCHECK_INFORME.md && touch $RUN/takeoff_work/etapas/5_auditoria/BACKCHECK_INFORME.md.rev6
mkdir -p $RUN/takeoff_work/etapas/5_auditoria/img_rev5 && cp $R/lect_datos/img/HT_*.png $RUN/takeoff_work/etapas/5_auditoria/img_rev5/
grep -q "Addendum rev6" $RUN/takeoff_work/etapas/5_auditoria/BACKCHECK_INFORME.md || cat $R/rev7in/backcheck_rev6.md >> $RUN/takeoff_work/etapas/5_auditoria/BACKCHECK_INFORME.md
grep -q "Addendum rev7" $RUN/takeoff_work/etapas/5_auditoria/BACKCHECK_INFORME.md || cat $R/rev7in/backcheck_rev7.md >> $RUN/takeoff_work/etapas/5_auditoria/BACKCHECK_INFORME.md
(cd $RUN/takeoff_work && python3 -I $T/bitacora.py backcheck $PWD/etapas/5_auditoria/BACKCHECK_INFORME.md $PWD/etapas/8_excel/Takeoff_runner.xlsx)
rm -rf $W && mkdir -p "$E/Take-off" "$E/Planos marcados" "$E/Auditoria"
ln -s $RUN/takeoff_work $W/takeoff_work
cp $R/rev7in/set_texto.json $R/rev7in/fichas.json $R/rev7in/entrega.json $R/rev7in/TIEMPOS.md $R/rev7in/proyecto_datos.json $W/
[ -f $R/rev7in/set_texto_v2.json ] && cp $R/rev7in/set_texto_v2.json $W/set_texto.json
cp $R/rev7in/burbujas_verificadas.json $W/ && cp -a $R/rev7in/burbujas_img $W/
mkdir -p "$E/Auditoria/burbujas" && cp $R/rev7in/burbujas_img/*.png "$E/Auditoria/burbujas/" && cp $R/rev7in/burbujas_verificadas.json "$E/Auditoria/burbujas/"
ln -s $RUN/takeoff_work/etapas/8_excel/Takeoff_runner.xlsx "$E/Take-off/OReilly_Evans_Takeoff_FINAL_rev7.xlsx"
ln -s $RUN/takeoff_work/etapas/8_excel/Takeoff_runner.xlsx.sello.json "$E/Take-off/OReilly_Evans_Takeoff_FINAL_rev7.xlsx.sello.json"
cp $RUN/takeoff_work/etapas/6_markups/markups.pdf "$E/Planos marcados/OReilly_Evans_FINAL_markups_rev7.pdf"
for p in $RUN/takeoff_work/etapas/7_imagenes/marcado_*.png; do b=$(basename $p .png); cp $p "$E/Planos marcados/A1.1_type_${b#marcado_}.png"; done
cp "$R/rev7in/CAMBIOS_vs_rev4.md" "$E/Auditoria/"
mkdir -p "$E/Auditoria/review_items" && cp $RUN/takeoff_work/etapas/4_canon/img/review_*.png "$E/Auditoria/review_items/"
mkdir -p "$E/Auditoria/img_head_track" && cp $R/lect_datos/img/HT_*.png "$E/Auditoria/img_head_track/"
mkdir -p $W/tools && cp $R/rev7in/tools/cambios_vs_rev4.py $W/tools/
(cd $W && python3 -I tools/cambios_vs_rev4.py /home/user/reading-plans/cache_proyectos/oreilly/FINAL_FOR_REVIEW_2026-11-01_rev4/Take-off/OReilly_Evans_Takeoff_FINAL_rev4.xlsx "$E/Take-off/OReilly_Evans_Takeoff_FINAL_rev7.xlsx" tabla_vs_rev4.md > /dev/null)
(cd $W && python3 -I $R/rev7in/hacer_docs7.py "$E" proyecto_datos.json tabla_vs_rev4.md)
(cd $W && python3 -I $T/compuerta_entrega.py banco . --cache /home/user/reading-plans > banco.txt 2>&1 || true; cat banco.txt)
(cd $W && timeout 1800 python3 -I $T/compuerta_entrega.py . > gate.txt 2>&1 || true)
grep COMPUERTA $W/gate.txt
