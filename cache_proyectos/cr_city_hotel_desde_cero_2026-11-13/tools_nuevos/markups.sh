#!/bin/bash
# Paso 8 (programas): markups Bluebeam de walls (+ cielos si hay rcp_polys) -> PDF de entrega + imagen por hoja
set -e
W=/root/cr0/work; T=/root/cr0/skill_s/take-off-metal-frame-drywall/tools; N=/root/cr0/tools_nuevos
D="$W/PRUEBA DESDE CERO 13-nov"; PM="$D/Planos marcados"; mkdir -p "$PM" $W/etapas/6_markups
export BITACORA=$W/bitacora.jsonl
PDF=/root/cr0/bidset/CityHotel_ArchitecturalPlans_4.22.2026_SIN_MARKUPS.pdf
cd $W
python3 -s $T/bitacora.py run $T/markups_bluebeam.py $PDF etapas/4_canon/takeoff_canon.json etapas/6_markups/markups_walls.pdf --inventario etapas/1_inventario/inventario.json > etapas/6_markups/markups_walls.log 2>&1 || { tail -5 etapas/6_markups/markups_walls.log; exit 1; }
SRC=etapas/6_markups/markups_walls.pdf
if [ -f etapas/6_markups/rcp_polys.json ]; then
  python3 -s $T/bitacora.py run $T/markups_rcp.py $SRC etapas/4_canon/takeoff_canon.json etapas/6_markups/rcp_polys.json etapas/6_markups/markups_all.pdf etapas/6_markups/png_rcp > etapas/6_markups/markups_rcp.log 2>&1 || tail -8 etapas/6_markups/markups_rcp.log
  [ -f etapas/6_markups/markups_all.pdf ] && SRC=etapas/6_markups/markups_all.pdf
fi
python3 -s $N/rcp_cuartos.py
python3 -s $T/bitacora.py run $T/markups_rcp.py excluded $SRC etapas/6_markups/rcp_cuartos.json --out etapas/6_markups/markups_excl.pdf > etapas/6_markups/markups_excl.log 2>&1 || tail -3 etapas/6_markups/markups_excl.log
[ -f etapas/6_markups/markups_excl.pdf ] && SRC=etapas/6_markups/markups_excl.pdf
rm -f "$PM"/*markups*OPEN\ IN\ BLUEBEAM.pdf
python3 -s $T/bitacora.py run $T/quitar_firmas_labels.py $SRC etapas/6_markups/markups_lab.pdf etapas/6_markups/page_sheets.json > etapas/6_markups/labels.log 2>&1 || { tail -3 etapas/6_markups/labels.log; exit 1; }
python3 -s $T/bitacora.py run $T/escala_pagina.py etapas/6_markups/markups_lab.pdf etapas/6_markups/markups_final.pdf >> etapas/6_markups/labels.log 2>&1 || { tail -3 etapas/6_markups/labels.log; exit 1; }
cp etapas/6_markups/markups_final.pdf "$PM/CR_markups_rev1 - OPEN IN BLUEBEAM.pdf"
python3 -s $N/imagenes_hojas.py "$PM/CR_markups_rev1 - OPEN IN BLUEBEAM.pdf" "$PM" rev1
