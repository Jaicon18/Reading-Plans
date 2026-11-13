# adv9_protocolo: CE_PROTOCOLO_3H proceso_v119 / tiempos_desde — v137 vs candidato.
# Hunt: una rev cuyo arranque NO tiene senal mas temprana que una marca 'inicio revN' escrita tarde;
# los pasos de la manana de la MISMA rev (sin su --paso) deberian seguir siendo FAIL.
import sys, os, json, subprocess, tempfile, shutil, textwrap
V137 = "/tmp/v138fb/take-off-metal-frame-drywall"
CAND = "/tmp/v139p/take-off-metal-frame-drywall"
BASE = "/tmp/verif13/tmp/a9a"

RUN = textwrap.dedent(r'''
    import sys, os
    S, W, E = sys.argv[1], sys.argv[2], sys.argv[3]
    sys.path.insert(0, os.path.join(S, "tools"))
    import compuerta_entrega as CE
    tt = open(os.path.join(W, "_TIEMPOS.md")).read()
    try:
        est, ev = CE.proceso_v119(W, E, tt, 5)
    except Exception as ex:
        print("EXC " + type(ex).__name__ + " " + str(ex)[:120]); sys.exit()
    import json
    print(json.dumps([est, [x[:90] for x in ev]]))
''')

def build(logtxt, vptxt, tt, corridas, folder):
    w = os.path.join(BASE, folder)
    if os.path.isdir(w): shutil.rmtree(w)
    e = os.path.join(w, "rev21 FINAL PARA REVISAR")
    os.makedirs(os.path.join(e, "Take-off"))
    open(os.path.join(e, "Take-off", "Z9_Takeoff_rev21.xlsx"), "w").write("x")
    open(os.path.join(w, "tiempos.log"), "w").write(logtxt)
    open(os.path.join(w, "VERSION_PROYECTO.txt"), "w").write(vptxt)
    open(os.path.join(w, "_TIEMPOS.md"), "w").write(tt)
    if corridas is not None:
        open(os.path.join(w, "compuerta_corridas.jsonl"), "w").write(corridas)
    # sellar bitacora para que los sellos no fallen aparte
    sys.path.insert(0, os.path.join(CAND, "tools")); import compuerta_entrega as CE
    for fn in ("compuerta_corridas.jsonl", "VERSION_PROYECTO.txt"):
        p = os.path.join(w, fn)
        if os.path.isfile(p):
            try: CE.sellar_bitacora(w, p)
            except Exception: pass
    return w, e

def run(S, w, e):
    r = subprocess.run([sys.executable, "-I", "-c", RUN, S, w, e], capture_output=True, text=True)
    out = (r.stdout or "").strip().splitlines()
    return out[-1] if out else ("STDERR " + r.stderr[-200:])

def caso(nombre, logtxt, vptxt, tt, corridas):
    w, e = build(logtxt, vptxt, tt, corridas, nombre.split()[0])
    a = run(V137, w, e); b = run(CAND, w, e)
    flag = "  <<< REGRESION" if ("FAIL" in a and '"PASS"' in b) else ""
    print(f"--- {nombre}")
    print(f"    v137 : {a}")
    print(f"    cand : {b}{flag}")

# TIEMPOS.md: pasos 1, 2-3 (manana) + 4 (tarde). Solo el paso 4 tiene corrida --paso.
TT = ("| # | Paso | Inicio | Fin | Min |\n|---|---|---|---|---|\n"
      "| 1 | Inventario | 11-13 08:00 | 11-13 08:30 | 30 |\n"
      "| 2-3 | Lecturas | 11-13 08:30 | 11-13 09:30 | 60 |\n"
      "| 4 | Comparacion | 11-13 10:00 | 11-13 10:30 | 30 |\n")
COR = json.dumps({"paso": "4", "rc": 0}) + "\n"

# ATAQUE Q4-residual: la manana (1,2-3) SI esta en el log con sus marcas, pero 'inicio rev21' se escribe tarde (10:00)
# y no hay git ni VERSION_PROYECTO mas temprano -> desde=10:00 -> la manana queda antes del arranque.
LOG_TARDE = ("05-nov 11:26 PST | 0 Arranque rev20 | inicio\n"
             "05-nov 19:00 PST | rev20 entregada\n"
             "2026-11-13 08:00 | 1 inicio\n"
             "2026-11-13 08:30 | 1 fin\n"
             "2026-11-13 09:30 | 2-3 fin\n"
             "2026-11-13 10:00 | inicio rev21\n"
             "2026-11-13 10:30 | 4 fin\n")
VP_TARDE = "2026-11-13T18:00:00Z | rev21 | v81cf138\n"   # 10:00 PST, no mas temprano que el inicio
caso("Q4res log con marcas de la manana + inicio-rev tardio", LOG_TARDE, VP_TARDE, TT, COR)

# Variante: VERSION_PROYECTO temprano (arranque real 08:00) -> deberia NO eximir
VP_TEMPRANO = "2026-11-13T15:50:00Z | rev21 | v81cf138\n"  # 07:50 PST
caso("Q4b VERSION_PROYECTO temprano (07:50)", LOG_TARDE, VP_TEMPRANO, TT, COR)

# Control: log SIN las marcas de la manana (como el test oficial) -> FAIL en ambos
LOG_SIN = ("2026-11-13 10:00 | inicio rev21\n2026-11-13 10:30 | 4 fin\n")
caso("CTRL log sin marcas de manana", LOG_SIN, VP_TARDE, TT, COR)
