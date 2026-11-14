#!/bin/bash
# Cadena del Paso 6-7 (programas): unir canon -> evidencia -> canon.py -> takeoff.json -> Excel
set -e
W=/root/cr0/work; T=/root/cr0/skill_s/take-off-metal-frame-drywall/tools; R=/root/cr0/skill_s/take-off-metal-frame-drywall/runner; N=/root/cr0/tools_nuevos
export BITACORA=$W/bitacora.jsonl
cd $W/etapas && python3 -s $N/unir_canon_final.py .
cd $W && python3 -s $N/normalizar_canon_campos.py etapas/4_canon/takeoff_canon.json etapas/1_inventario/inventario.json
python3 -s $N/recortes_walls.py etapas/4_canon/takeoff_canon.json /root/cr0/bidset/CityHotel_ArchitecturalPlans_4.22.2026_SIN_MARKUPS.pdf SHEET_MAP.md etapas/4_canon/img/walls
python3 -s $R/evidencia.py etapas/4_canon/takeoff_canon.json /root/cr0/bidset/CityHotel_ArchitecturalPlans_4.22.2026_SIN_MARKUPS.pdf SHEET_MAP.md etapas/4_canon/img --canon-out etapas/4_canon/takeoff_canon.json --inventario etapas/1_inventario/inventario.json > evidencia.log 2>&1
python3 -s $N/validar_canon.py etapas/4_canon/takeoff_canon.json $T
python3 -s $T/bitacora.py run $T/canon.py etapas/4_canon/takeoff_canon.json etapas/4_canon/out > canon_run.log 2>&1
python3 -s $T/bitacora.py run $T/inventario.py etapas/4_canon/takeoff_canon.json etapas/4_canon/out/inventario_out.json > /dev/null 2>&1
python3 -s $N/armar_takeoff_json.py etapas takeoff.json alcances_decision.json
