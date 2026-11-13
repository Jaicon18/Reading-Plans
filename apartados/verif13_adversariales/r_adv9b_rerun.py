# adv9_protocolo2: aislar la regresion Q4-residual sin ruido de version ni de rev20.
import sys, os, json, subprocess, tempfile, shutil, textwrap
V137 = "/tmp/v138fb/take-off-metal-frame-drywall"; CAND = "/tmp/v139p/take-off-metal-frame-drywall"
BASE = "/tmp/verif13/tmp/a9b"
RUN = textwrap.dedent(r'''
    import sys, os, re, json
    S, W, E = sys.argv[1], sys.argv[2], sys.argv[3]
    sys.path.insert(0, os.path.join(S, "tools"))
    import compuerta_entrega as CE
    # pin VERSION_PROYECTO version token to THIS tree's skill version (mata el falso (7))
    vp = os.path.join(W, "VERSION_PROYECTO.txt"); v = CE._skill_version() or "v81cf138"
    t = open(vp).read(); t = re.sub(r"v81cf\d+", v, t); open(vp, "w").write(t)
    try: CE.sellar_bitacora(W, vp)
    except Exception: pass
    tt = open(os.path.join(W, "_TIEMPOS.md")).read()
    try: est, ev = CE.proceso_v119(W, E, tt, 5)
    except Exception as ex: print("EXC " + type(ex).__name__ + " " + str(ex)[:120]); sys.exit()
    print(json.dumps([est, [x[:85] for x in ev]]))
''')
def build(folder, logtxt, vptxt, tt, cor):
    w = os.path.join(BASE, folder)
    if os.path.isdir(w): shutil.rmtree(w)
    e = os.path.join(w, "rev21 FINAL PARA REVISAR"); os.makedirs(os.path.join(e, "Take-off"))
    open(os.path.join(e, "Take-off", "Z9_Takeoff_rev21.xlsx"), "w").write("x")
    open(os.path.join(w, "tiempos.log"), "w").write(logtxt)
    open(os.path.join(w, "VERSION_PROYECTO.txt"), "w").write(vptxt)
    open(os.path.join(w, "_TIEMPOS.md"), "w").write(tt)
    if cor: 
        open(os.path.join(w, "compuerta_corridas.jsonl"), "w").write(cor)
        sys.path.insert(0, os.path.join(CAND, "tools")); import compuerta_entrega as CE
        try: CE.sellar_bitacora(w, os.path.join(w, "compuerta_corridas.jsonl"))
        except Exception: pass
    return w, e
def run(S, w, e):
    r = subprocess.run([sys.executable,"-I","-c",RUN,S,w,e], capture_output=True, text=True)
    o=(r.stdout or "").strip().splitlines(); return o[-1] if o else "STDERR "+r.stderr[-200:]
def caso(n, logtxt, vptxt, tt, cor):
    import copy
    wa,ea=build(n.split()[0]+"_a", logtxt, vptxt, tt, cor); a=run(V137,wa,ea)
    wb,eb=build(n.split()[0]+"_b", logtxt, vptxt, tt, cor); b=run(CAND,wb,eb)
    reg = "FAIL" in a and '"PASS"' in b
    print(f"--- {n}\n    v137: {a}\n    cand: {b}{'   <<< REGRESION' if reg else ''}")

TT=("| # | Paso | Inicio | Fin | Min |\n|---|---|---|---|---|\n"
    "| 1 | Inventario | 11-13 08:00 | 11-13 08:30 | 30 |\n"
    "| 2-3 | Lecturas | 11-13 08:30 | 11-13 09:30 | 60 |\n"
    "| 4 | Comparacion | 11-13 10:00 | 11-13 10:30 | 30 |\n")
COR=json.dumps({"paso":"4","rc":0})+"\n"
# Toda la actividad es del 13-nov (rev21). La manana cierra 1 y 2-3; 'inicio rev21' se anota a las 10:00.
LOG=("2026-11-13 08:00 | 1 inicio\n2026-11-13 08:30 | 1 fin\n2026-11-13 09:30 | 2-3 fin\n"
     "2026-11-13 10:00 | inicio rev21\n2026-11-13 10:30 | 4 fin\n")
VP ="2026-11-13T18:00:00Z | rev21 | v81cf138\n"   # 10:00 PST (anotado tarde, como el inicio)
caso("Q4res manana-con-marcas + inicio-rev-tardio (VP tambien tardio, sin git)", LOG, VP, TT, COR)

# Variante A: SIN VERSION_PROYECTO (BE-PM05 no seguido) -> desde = solo el inicio tardio
import os as _os
def caso_novp(n, logtxt, tt, cor, git_early=False):
    import shutil, subprocess
    for S, tag in ((V137,"_a"),(CAND,"_b")):
        pass
    def mk(folder):
        w=_os.path.join(BASE,folder)
        if _os.path.isdir(w): shutil.rmtree(w)
        e=_os.path.join(w,"rev21 FINAL PARA REVISAR"); _os.makedirs(_os.path.join(e,"Take-off"))
        open(_os.path.join(e,"Take-off","Z9_Takeoff_rev21.xlsx"),"w").write("x")
        open(_os.path.join(w,"tiempos.log"),"w").write(logtxt)
        open(_os.path.join(w,"_TIEMPOS.md"),"w").write(tt)
        if cor: open(_os.path.join(w,"compuerta_corridas.jsonl"),"w").write(cor)
        if git_early:
            subprocess.run(["git","-C",w,"init","-q"],check=False)
            subprocess.run(["git","-C",w,"config","user.email","a@b.c"],check=False)
            subprocess.run(["git","-C",w,"config","user.name","a"],check=False)
            # commit temprano (08:00 del 13-nov) tocando la carpeta de la rev
            env=dict(_os.environ, GIT_AUTHOR_DATE="2026-11-13T08:00:00-08:00", GIT_COMMITTER_DATE="2026-11-13T08:00:00-08:00")
            subprocess.run(["git","-C",w,"add","-A"],check=False)
            subprocess.run(["git","-C",w,"commit","-q","-m","init"],env=env,check=False)
        return w,e
    wa,ea=mk(n.split()[0]+"_a"); wb,eb=mk(n.split()[0]+"_b")
    a=run(V137,wa,ea); b=run(CAND,wb,eb)
    # novp: el RUN intenta reescribir VERSION_PROYECTO; adaptamos: si no existe lo salta
    reg="FAIL" in a and '"PASS"' in b
    print(f"--- {n}\n    v137: {a}\n    cand: {b}{'   <<< REGRESION' if reg else ''}")

RUN = RUN.replace('t = open(vp).read()', 't = open(vp).read() if os.path.isfile(vp) else ""').replace('open(vp, "w").write(t)', 'open(vp,"w").write(t) if t else None')
caso_novp("NoVP sin VERSION_PROYECTO + inicio tardio (sin git)", LOG, TT, COR, git_early=False)
caso_novp("GitEarly delivery es repo git con commit 08:00 (ancla temprana)", LOG, TT, COR, git_early=True)
