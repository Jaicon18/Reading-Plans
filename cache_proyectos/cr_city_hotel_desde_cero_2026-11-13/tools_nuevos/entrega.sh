#!/bin/bash
# Cadena completa de la entrega (pasos 6-9): todo archivo sale de aquí (CE_PROTOCOLO_3H (3): nada a mano)
set -e
W=/root/cr0/work; T=/root/cr0/skill_w/take-off-metal-frame-drywall/tools; N=/root/cr0/tools_nuevos
D="$W/PRUEBA DESDE CERO 13-nov"; X="$D/Take-off/CR_City_Hotel_Takeoff_rev1.xlsx"
export BITACORA=$W/bitacora.jsonl
export SUBAGENTE_ID=${SUBAGENTE_ID:-autor_cr0_orquestador}
$N/pipeline.sh
cd $W
python3 -s $T/bitacora.py run $T/plantilla_excel.py armar takeoff.json "$X" --familias etapas/4_canon/out/familias_out.json --trabajo $W | tail -1
$N/markups.sh | tail -1
MK="$D/Planos marcados/CR_markups_rev1 - OPEN IN BLUEBEAM.pdf"
python3 -s $T/compuerta_entrega.py vista_bluebeam "$MK" "$X" --canon etapas/4_canon/takeoff_canon.json --csv "$D/Auditoria/VISTA_BLUEBEAM.csv" | tail -1 || true
python3 -s $N/alturas_build.py > $W/alturas_build.log 2>&1 || tail -3 $W/alturas_build.log
python3 -s $T/bitacora.py run $T/comparar_alturas.py "$D/Auditoria/VISTA_BLUEBEAM.csv" "$X" "$D/Auditoria/ALTURAS_IMPRESAS.csv" "$D/Auditoria/COMPARACION_ALTURAS.csv" > $W/alturas3.log 2>&1 || tail -3 $W/alturas3.log
python3 -s $T/bitacora.py run $T/comparar_alturas.py extremo "$D" etapas/4_canon/takeoff_canon.json "$MK" > $W/extremo.log 2>&1 || tail -3 $W/extremo.log
python3 -s $T/compuerta_entrega.py banco $W --cache /home/user/Reading-Plans | tail -1
python3 -s $N/doble_cielo.py
python3 -s $N/docs_entrega.py
bash $W/proposal/build_cr.sh > $W/proposal/build.log 2>&1 || tail -3 $W/proposal/build.log
python3 -s $T/compuerta_entrega.py schedules $W | tail -1
python3 -s $T/compuerta_entrega.py detalles $W | tail -1
python3 -s $T/bitacora.py run $T/compuerta_entrega.py cobertura "$D" > etapas/cobertura.log 2>&1 || tail -3 etapas/cobertura.log
python3 -s $T/checklist_revision.py "$X" "$MK" /root/cr0/bidset/CityHotel_ArchitecturalPlans_4.22.2026_SIN_MARKUPS.pdf etapas/4_canon/takeoff_canon.json "$D/CHECKLIST_REVISION.xlsx" --proy CR --b6 "$D/Auditoria/COBERTURA.csv" | tail -1 || true
python3 -s $T/compuerta_entrega.py leeme "$D" | tail -1
