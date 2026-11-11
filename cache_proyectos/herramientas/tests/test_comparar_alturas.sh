#!/bin/bash
# U-175: con alturas impresas correctas = 0 (20/20); con W2-02 cambiada a 9'-6" = 1 (FAIL).
d=$(dirname "$0"); t=$(mktemp -d)
python3 -I $d/../comparar_alturas.py $d/xf_vista_bluebeam.csv $d/xf_takeoff_rev1.xlsx $d/xf_alturas_ok.csv $t/a.csv >/dev/null || { echo "FAIL ok-case"; exit 1; }
python3 -I $d/../comparar_alturas.py $d/xf_vista_bluebeam.csv $d/xf_takeoff_rev1.xlsx $d/xf_alturas_mal.csv $t/b.csv >/dev/null && { echo "FAIL bad-case not detected"; exit 1; }
echo "PASS test_comparar_alturas"
