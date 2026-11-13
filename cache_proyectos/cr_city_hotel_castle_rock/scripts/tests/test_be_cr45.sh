#!/bin/bash
# BE-CR45: el canon rev20c debe dar exactamente 6 (a) + 6 (b) y rc 1; el canon rev20d, 0 y rc 0.
cd "$(dirname "$0")"
o=$(python3 -I test_ducha_cbu.py fixture_canon_rev20c.json fixture_banos_cbu.json); r=$?
na=$(grep -c "^(a)" <<<"$o"); nb=$(grep -c "^(b)" <<<"$o")
[ $r = 1 ] && [ $na = 6 ] && [ $nb = 6 ] || { echo "FAIL rev20c: rc $r a=$na b=$nb"; exit 1; }
python3 -I test_ducha_cbu.py fixture_canon_rev20d.json fixture_banos_cbu.json >/dev/null || { echo "FAIL rev20d no da 0"; exit 1; }
echo "BE-CR45 OK (rev20c 6+6, rev20d 0)"
