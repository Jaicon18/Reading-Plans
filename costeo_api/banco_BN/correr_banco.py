"""Banco de regresión B&N (sin API): re-arma cada lectura guardada (#3, #4, #5, #7) con el runner y el skill ACTUALES
y da la tabla material x corrida vs rev13. Un arreglo entra solo si no empeora ningún material en ninguna lectura.
Uso: python3 correr_banco.py <salida_dir> [--base banco_base.json]  (con --base marca los materiales que empeoran)."""
import sys, os, json, subprocess, shutil, re, warnings
warnings.filterwarnings("ignore")
AQUI = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(AQUI, "..", ".."))
RT = "/home/user/takeoff_runtime"; P = os.path.join(REPO, "cache_proyectos/barnes_noble")
REV13 = f"{P}/FINAL_FOR_REVIEW_2026-10-24_rev13/Take-off/Barnes_Noble_ColoradoSprings_Takeoff_FINAL_rev13.xlsx"
# referencia = familias_out.json del dry-run (reproduce rev13 exacto); los números de la corrida salen de familias_out.json
# (programas), que existe aunque una compuerta de contenido no deje armar el Excel sin la corrección pagada
REF = os.path.join(AQUI, "familias_rev13_dryrun.json")
PRIN = ['5/8" gyp board Type X', '5/8" gyp Type X W.R.', '3-5/8" stud (todos los gauges)', '6" stud (todos los gauges)',
        '8" stud (todos los gauges)', 'bottom track (todos)', 'track de ceilings / soffits', 'bracing C.R. channel',
        'cement board', '5/8" cement board', 'FRT plywood (SF)', 'FRT blocking', 'FRP',
        'metal trim (corner bead, casing, shadow molding)', 'metal stud blocking (362CR / STUD BLOCKING)',
        'nested inner runner (deflection head)']
def mats(fo):
    return (json.load(open(fo)).get("familias") or {}) if os.path.exists(fo) else None
out = os.path.abspath(sys.argv[1]); base = sys.argv[sys.argv.index("--base") + 1] if "--base" in sys.argv else None
os.makedirs(out, exist_ok=True); res = {}
for r in ("r3", "r4", "r5", "r7"):
    w = os.path.join(out, r); shutil.rmtree(w, ignore_errors=True)
    cmd = [sys.executable, "-W", "ignore", os.path.join(REPO, "costeo_api/runner/run_takeoff.py"), "--sin-api",
           "--pdf", f"{RT}/bidset/bidset_SIN_MARKUPS.pdf", "--skill", f"{RT}/skill/take-off-metal-frame-drywall",
           "--project-inputs", f"{P}/takeoff_work", "--evidence-root", P,
           "--overlay", os.path.join(REPO, "costeo_api/runner/decisiones_BN.json"),
           "--ref-base", os.path.join(REPO, "costeo_api/runner/canon_BN_sin_decisiones.json"), "--trade-plan-sheets", "A-101,A-221",
           "--sealer", f"{P}/takeoff_work/scripts/sellar_y_marcar.py", "--compare-with", REV13, "--budget", "0",
           "--reusar-lecturas", os.path.join(AQUI, r), "--reusar-resolucion", os.path.join(AQUI, f"{r}_AB.json"), "--work", w]
    p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, env=dict(os.environ, RUNNER_COSTOS=os.path.join(out, "costos_banco.csv")))
    m = mats(os.path.join(w, "takeoff_work/etapas/4_canon/out/familias_out.json"))
    res[r] = m if m else {"_error": (p.stdout + p.stderr).strip().splitlines()[-1][:200]}
    if p.returncode != 0 and m:
        res[r]["_excel"] = (p.stdout + p.stderr).strip().splitlines()[-1][:160]
ref = json.load(open(REF))["familias"]; json.dump({"rev13": ref, **res}, open(os.path.join(out, "banco.json"), "w"), indent=1)
prev = json.load(open(base)) if base else None
err = lambda v, n: None if v.get(n) is None or not ref.get(n) else (v[n] - ref[n]) / ref[n] * 100
peor = []
print("| Material | rev13 | " + " | ".join(res) + " |"); print("|---" * (len(res) + 2) + "|")
for n in PRIN:
    cel = []
    for r, v in res.items():
        if "_error" in v: cel.append("ERROR"); continue
        e = err(v, n); s = "—" if e is None else f"{e:+.1f} %"
        if prev and r in prev and "_error" not in prev[r]:
            e0 = err(prev[r], n)
            if e is not None and e0 is not None and abs(e) > abs(e0) + 0.05: s += " ▲"; peor.append(f"{r} {n} {e0:+.1f} -> {e:+.1f}")
            elif e is not None and e0 is not None and abs(e) < abs(e0) - 0.05: s += " ▼"
        cel.append(s)
    print(f"| {n} | {ref.get(n, 0):,.0f} | " + " | ".join(cel) + " |")
for r, v in res.items():
    if "_error" in v or "_excel" in v: print(f"\n{r}: {v.get('_error') or 'Excel no armó (sin corrección): ' + v['_excel']}")
print("\nEMPEORA: " + ("; ".join(peor) if peor else "nada") if prev else "")
