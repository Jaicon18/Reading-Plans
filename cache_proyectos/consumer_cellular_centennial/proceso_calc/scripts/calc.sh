source /root/cc/work/scripts/env.sh; cd $W
python3 -I scripts/resolver_AB.py >/dev/null && python3 $T/bitacora.py run scripts/ajustes_canon.py >/dev/null 2>&1 && python3 $T/bitacora.py run scripts/rfis.py >/dev/null 2>&1 && python3 $T/bitacora.py run $T/canon.py etapas/4_canon/takeoff_canon.json etapas/4_canon/out 2>&1 | grep -v -i warn | tail -${1:-6}
