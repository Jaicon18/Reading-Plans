#!/bin/bash
# CR City Hotel - cadena pasos 4-7 (cada tool por bitacora.py run; para en el primer rc != 0). Uso: bash scripts/cadena.sh [desde]
source /root/cr/work/scripts/env.sh
REV=${REV:-rev1}; cd $W; C4=$W/etapas/4_canon; X=$W/etapas/8_excel/CR_City_Hotel_Takeoff_FINAL_${REV}.xlsx
N=0; DESDE=${1:-0}
R() { N=$((N+1)); [ $N -lt $DESDE ] && return 0; python3 $T/bitacora.py run "$@" > $W/last.log 2>&1; rc=$?
      echo "$(TZ=America/Los_Angeles date +%H:%M) step $N rc=$rc $(basename $1) $2"
      if [ $rc != 0 ]; then tail -25 $W/last.log | grep -v -i "warn"; exit $rc; fi; }
R scripts/comparar_AB.py
R scripts/canon_AB.py
R scripts/build_canon.py
R scripts/finalizar_canon.py
R scripts/rfis.py
R $T/canon.py $C4/takeoff_canon.json $C4/out
R $T/vigas_sobre_walls.py $PDF NONE A2.02@p18 $C4/takeoff_canon.json --json $C4/out/vigas_out.json
R scripts/evidencias_reglas.py
R scripts/takeoff_json.py $T
R $T/plantilla_excel.py validar takeoff.json
R $T/plantilla_excel.py armar takeoff.json $X --familias $C4/out/familias_out.json --trabajo etapas
echo CHAIN-OK
