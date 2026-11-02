"""Marks the 24 ALC rows of registro.json with registro.py marcar (through bitacora.py run), from the Scope Checklist
notes of takeoff.json. Never edits registro.json by hand."""
import json, os, subprocess, sys
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = sys.argv[1]
td = json.load(open(os.path.join(K, "takeoff.json")))
reg = json.load(open(os.path.join(K, "registro.json")))
est = {r["id"]: r["estado"] for r in reg["renglones"]}
rc = 0
for a in td["alcances"]:
    if not a["id"].startswith("ALC-") or a["id"].startswith("ALC-E") or a["id"] not in est or est[a["id"]] != "pendiente":
        continue
    if a["id"] == "ALC-19":
        nota = "EXCLUDED: acoustical sealant excluded in all projects (estimator standing order); " + a["nota"]
    elif a["estado"] == "NO APLICA":
        nota = "NO APLICA: " + a["nota"]
    else:
        nota = "CUANTIFICADO: " + a["nota"]
    p = subprocess.run([sys.executable, os.path.join(T, "bitacora.py"), "run", os.path.join(T, "registro.py"), "marcar",
                        os.path.join(K, "registro.json"), a["id"], "verificado", nota], cwd=K, capture_output=True, text=True)
    print(a["id"], p.returncode, (p.stdout + p.stderr).strip().splitlines()[0][:120])
    rc |= p.returncode
sys.exit(rc)
