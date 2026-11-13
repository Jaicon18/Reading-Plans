# adv8_cr_canon: caras_sobre_ceiling y be_cf04 sobre el canon real de CR rev20b, v137 vs candidato
import sys, os, json, importlib, types
S = sys.argv[1]; CAN = sys.argv[2]
sys.path.insert(0, os.path.join(S, "runner")); sys.path.insert(0, os.path.join(S, "tools"))
import completitud as CO
c = json.load(open(CAN))
try:
    r = CO.caras_sobre_ceiling(c)
    print("caras_sobre_ceiling n=", len(r))
    for x in r: print("  ", x)
except Exception as e:
    print("caras_sobre_ceiling EXC", type(e).__name__, e)
import collections
fz = collections.Counter(type(w.get("faces")).__name__ for w in CO._muros(c))
print("tipos de faces en _muros:", dict(fz))
