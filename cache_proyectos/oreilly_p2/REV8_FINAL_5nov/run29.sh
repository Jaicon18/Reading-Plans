#!/bin/bash
cd /tmp/claude-scratch/oreilly_p2
env -u TAKEOFF_API_KEY python3 /tmp/claude-scratch/v81cf42/take-off-metal-frame-drywall/runner/run_takeoff.py --sin-api --pdf plans/bidset_con_markups_SIN_MARKUPS.pdf --skill /tmp/claude-scratch/v81cf42/take-off-metal-frame-drywall --project-inputs proj23/takeoff_work --evidence-root proj23 --overlay lect_resolucion/overlay_OReilly_p2_rev8.json --reusar-lecturas /tmp/claude-scratch/oreilly_p2/lect --reusar-resolucion lect_resolucion/takeoff_canon_AB.json --plan-sheet A1.1 --trade-plan-sheets A1.1 --sealer proj23/takeoff_work/scripts/sellar_y_marcar.py --cobertura-lista proj23/takeoff_work/etapas/5_auditoria/cobertura_lista.json --work /tmp/claude-scratch/oreilly_p2/$1 > ensamble/$1.log 2>&1
echo rc=$?
grep -E "^[0-9]{2}:[0-9]{2}|DETENIDO|FALLA|ERROR|Error" ensamble/$1.log | grep -v "^ " | tail -25 | cut -c1-500
