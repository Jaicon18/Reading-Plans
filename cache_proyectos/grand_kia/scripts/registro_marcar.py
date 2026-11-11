"""Grand Kia: closes every 'pendiente' row of registro.json (ALC-01..24) with `registro.py marcar` through bitacora.py run, from
the Scope Checklist of takeoff.json (estado + note with N/SHEET). Never edits registro.json by hand.
Use: python3 bitacora.py run scripts/registro_marcar.py <tools_dir>"""
import json, os, subprocess, sys
K = '/root/gk/work'
T = sys.argv[1]
td = json.load(open(os.path.join(K, "takeoff.json")))
reg = json.load(open(os.path.join(K, "registro.json")))
nota = {}
for a in td["alcances"]:
    if a["id"].startswith("ALC-E"):
        continue
    pre = {"NO APLICA": "NO APLICA", "EXCLUDED": "EXCLUDED"}.get(a["estado"], "CUANTIFICADO")
    if a["id"] == "ALC-19":
        pre = "EXCLUDED: acoustical sealant excluded in all projects (estimator standing order);"
    nota[a["id"]] = f"{pre}: {a['nota']}" if not pre.endswith(";") else f"{pre} {a['nota']}"
rc = 0
for r in reg["renglones"]:
    if r["estado"] == "verificado" and r["id"] in nota and nota[r["id"]][:1500] != str(r.get("nota") or r.get("evidencia") or ""):
        p = subprocess.run([sys.executable, os.path.join(T, "bitacora.py"), "run", os.path.join(T, "registro.py"), "corregir",
                            os.path.join(K, "registro.json"), r["id"], "verificado", nota[r["id"]][:1500]], cwd=K, capture_output=True, text=True)
        print(r["id"], "corregir", p.returncode); rc |= p.returncode
        continue
    if r["estado"] != "pendiente":
        continue
    if r["id"] not in nota:
        print(r["id"], "NO EVIDENCE - left pending"); rc = 1; continue
    p = subprocess.run([sys.executable, os.path.join(T, "bitacora.py"), "run", os.path.join(T, "registro.py"), "marcar",
                        os.path.join(K, "registro.json"), r["id"], "verificado", nota[r["id"]][:1500]], cwd=K, capture_output=True, text=True)
    print(r["id"], p.returncode, ((p.stdout + p.stderr).strip().splitlines() or [""])[0][:120])
    rc |= p.returncode
sys.exit(rc)
