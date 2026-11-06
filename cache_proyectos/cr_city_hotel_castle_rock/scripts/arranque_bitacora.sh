#!/bin/bash
# CR City Hotel - pasos de arranque EN ORDEN en la bitácora (regla 56.1: registro crear ANTES del primer Excel).
source /root/cr/work/scripts/env.sh; cd $W
R() { python3 $T/bitacora.py run "$@" > $W/last.log 2>&1; rc=$?; echo "arranque rc=$rc $(basename $1) $2"; [ $rc != 0 ] && { tail -15 $W/last.log; exit $rc; }; return 0; }
[ -f registro.json ] && { echo "registro ya creado"; exit 0; }
R $T/arranque.py $PDF 18 10
R $T/inventario_tags.py $PDF etapas/1_inventario_runner --sin-recortes
R $T/alcances.py escanear $PDF escaneo.json
R $T/registro.py crear registro.json renglones_alc.json
R $T/contar_tags.py $PDF A2.02@p18 W.62 DW.4 XW.6.3 --json etapas/1_inventario/contar_tags_A202.json
