source /root/xf/work/scripts/env.sh; cd $W
python3 -I scripts/resolver.py >/dev/null && python3 -I scripts/formato.py >/dev/null && python3 $T/canon.py etapas/4_canon/takeoff_canon.json etapas/4_canon/out 2>&1 | grep -v -i warn | tail -${1:-5}
