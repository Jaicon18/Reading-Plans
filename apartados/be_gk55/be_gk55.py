"""BE-GK55 (Grand Kia rev3b, REVERIF17 R17-F1, 12-nov): adding a new wall changed the joints of a wall that did NOT change. build_canon.nodos
paired A-Z1-13 (east end at the kn 51 infill, x1388.2) with the new patch furring F-Z1-21 (east face of the infill, x1395.4) as a T: the 8"
CMU infill is between them, they never meet, and the false node added 1 stud = +8.21 LF of 362S162-19 that no listed change explained.
Rule: between two revisions, every NEW node (L / T / split) that touches a wall whose band did not change must be explained in
CAMBIOS_<rev>.txt (both wall ids named) or the pair is declared non-meeting (corner_skip with N/SHEET); otherwise FAIL.
Usage: python3 be_gk55.py <canon_prev.json> <canon_new.json> <CAMBIOS_rev.txt>   -> exit 1 on FAIL."""
import json, sys


def _clave(n):
    if n.get('kind') == 'T':
        return ('T', n.get('branch'), n.get('through'))
    if n.get('kind') in ('L', 'split'):
        return (n['kind'],) + tuple(sorted(n.get('walls') or []))
    return ('free', n.get('wall'))


def fallas(prev, new, cambios=''):
    bp = {w['id']: w.get('band') for w in prev.get('walls') or []}
    bn = {w['id']: w for w in new.get('walls') or []}
    viejos = {_clave(n) for n in prev.get('nodes') or []}
    ev = []
    for n in new.get('nodes') or []:
        k = _clave(n)
        if k[0] == 'free' or k in viejos:
            continue
        ids = [x for x in k[1:] if x]
        quietos = [x for x in ids if x in bp and bp[x] == (bn.get(x) or {}).get('band')]
        if not quietos:
            continue
        skip = any(o in ((bn.get(x) or {}).get('corner_skip_info') or (bn.get(x) or {}).get('corner_skip') or {}) for x in ids for o in ids if o != x)
        if skip or all(x in cambios for x in ids):
            continue
        ev.append(f"new node {k[0]} {' / '.join(ids)}: touches unchanged wall(s) {', '.join(quietos)} and is not explained in CAMBIOS "
                  f"(both ids) nor declared non-meeting (corner_skip with N/SHEET) - a new wall must not change the joints of an old one "
                  f"by proximity (BE-GK55)")
    return ev


if __name__ == '__main__':
    ev = fallas(json.load(open(sys.argv[1])), json.load(open(sys.argv[2])), open(sys.argv[3], encoding='utf-8').read() if len(sys.argv) > 3 else '')
    print('\n'.join(ev) if ev else 'BE-GK55 PASS: every new node is explained')
    sys.exit(1 if ev else 0)
