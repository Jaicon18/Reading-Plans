# adv8_be83_cf04_canones: caras_sobre_ceiling (completitud) y be_cf04 (chequeos_biblioteca) en TODOS los canones reales, v137 vs candidato
import sys, os, json, glob, subprocess
V = {"v137": "/tmp/v137/take-off-metal-frame-drywall", "cand": "/tmp/v138r3/take-off-metal-frame-drywall"}
cans = sorted(set(subprocess.run("find /home/user/Reading-Plans/cache_proyectos /root -name '*canon*.json' -size +20k 2>/dev/null | grep -v verif", shell=True, capture_output=True, text=True).stdout.split()))
code = r'''
import sys, os, json
S, P = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(S, "runner")); sys.path.insert(0, os.path.join(S, "tools"))
import completitud as CO, chequeos_biblioteca as CB
c = json.load(open(P))
if not isinstance(c, dict): print(json.dumps(["nodict"])); sys.exit()
try: a = sorted(map(list, CO.caras_sobre_ceiling(c)))
except Exception as e: a = "EXC " + type(e).__name__
try:
    r = CB.be_cf04(CB.B(canon=c)); b = [r[0], [str(x)[:120] for x in (r[1] if len(r) > 1 else [])][:3]]
except Exception as e: b = "EXC " + type(e).__name__ + str(e)[:80]
print(json.dumps([a, b], default=str))
'''
for p in cans:
    out = {}
    for k, s in V.items():
        r = subprocess.run([sys.executable, "-I", "-c", code, s, p], capture_output=True, text=True)
        try: out[k] = json.loads(r.stdout.strip().splitlines()[-1])
        except Exception: out[k] = ("ERR", r.stderr[-200:])
    a, b = out["v137"], out["cand"]
    if a == b: print("IGUAL", p.replace("/home/user/Reading-Plans/cache_proyectos/", ""), str(a[1])[:60] if len(a) > 1 else a); continue
    print("DISTINTO", p)
    for k in ("v137", "cand"):
        x = out[k]
        print("   ", k, "be83:", (x[0] if isinstance(x[0], str) else f"{len(x[0])} caras {x[0][:4]}"), "| cf04:", x[1] if len(x) > 1 else x)
    if isinstance(a[0], list) and isinstance(b[0], list):
        sa = set(map(tuple, map(lambda t: tuple(map(str, t)), a[0]))); sb = set(map(tuple, map(lambda t: tuple(map(str, t)), b[0])))
        print("    be83 solo v137 (silenciadas por el candidato):", sorted(sa - sb)[:10]); print("    be83 solo cand:", sorted(sb - sa)[:10])
