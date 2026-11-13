# adv10_delta: delta 49ef0ac -> v138r3 (GAP_REV_ANTERIOR_H=12). v137 vs candidato via proceso_v119. Sintetico en /tmp/verif13/tmp/a10.
# Uso: python3 -I adv10_delta.py   (ejecuta ambos arboles en subprocesos -I)
import sys, os, json, subprocess, shutil, textwrap
V137 = "/tmp/v138fb/take-off-metal-frame-drywall"; CAND = "/tmp/v139p/take-off-metal-frame-drywall"; BASE = "/tmp/verif13/tmp/a10"
RUN = textwrap.dedent(r'''
    import sys, os, json
    S, W, E, NA = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    sys.path.insert(0, os.path.join(S, "tools")); import compuerta_entrega as CE
    tt = open(os.path.join(W, "_TIEMPOS.md")).read()
    try: est, ev = CE.proceso_v119(W, E, tt, NA)
    except Exception as ex: print("EXC", type(ex).__name__, str(ex)[:120]); sys.exit()
    print(json.dumps([est, [x[:110] for x in ev]], ensure_ascii=False))
''')
sys.path.insert(0, os.path.join(CAND, "tools")); import compuerta_entrega as CE
VER = CE._skill_version() or "v81cf138"
H = "| # | Paso | Inicio | Fin | Min |\n|---|---|---|---|---|\n"
def caso(nombre, log, vp, tt, pasos, na=10, alerta=None):
    w = os.path.join(BASE, nombre.split()[0])
    if os.path.isdir(w): shutil.rmtree(w)
    e = os.path.join(w, "rev21 FINAL PARA REVISAR"); os.makedirs(os.path.join(e, "Take-off"))
    open(os.path.join(e, "Take-off", "Z9_Takeoff_rev21.xlsx"), "w").write("x")
    open(os.path.join(w, "tiempos.log"), "w").write(log)
    open(os.path.join(w, "VERSION_PROYECTO.txt"), "w").write(f"{vp} | rev21 | {VER}\n")
    open(os.path.join(w, "_TIEMPOS.md"), "w").write(H + tt)
    open(os.path.join(w, "compuerta_corridas.jsonl"), "w").write("".join(json.dumps({"paso": p, "rc": 0}) + "\n" for p in pasos))
    CE.sellar_bitacora(w, os.path.join(w, "compuerta_corridas.jsonl"))
    r = {}
    for k, S in (("v137", V137), ("cand", CAND)):
        p = subprocess.run([sys.executable, "-I", "-c", RUN, S, w, e, str(na)], capture_output=True, text=True)
        r[k] = (p.stdout.strip().splitlines() or ["STDERR " + p.stderr[-200:]])[-1]
    a, b = r["v137"], r["cand"]
    def st(x): return "PASS" if x.startswith('["PASS"') else ("FAIL" if x.startswith('["FAIL"') else x[:12])
    # v137 siempre falla por la version (7); se marca regresion si el candidato da PASS y v137 tenia una falla de PROCESO (no solo (7))
    proc137 = [m for m in json.loads(a)[1] if not m.startswith("(7)")] if a.startswith("[") else []
    flag = "  <<< REGRESION (v137 FAIL de proceso, cand PASS)" if st(b) == "PASS" and proc137 else ""
    print(f"--- {nombre}\n    v137: {a}\n    cand: {b}{flag}")
# PREV = rev20 cerrada; pasos de rev20 sin etiqueta en el log (como el test oficial)
PREV = "05-nov 11:26 PST | 0 Arranque rev20 | inicio\n"
# A) frontera exacta 12 h: paso 1 cierra 11-12 22:00, 'inicio rev21' 11-13 10:00 (VP 18:00Z = 10:00 PT). Sin --paso 1.
for fin, nm in (("22:00", "A12h00 exactamente 12 h"), ("22:01", "A11h59 11 h 59 min"), ("21:59", "A12h01 12 h 01 min")):
    caso(nm, PREV + f"2026-11-12 21:00 | 1 inicio\n2026-11-12 {fin} | 1 fin\n2026-11-13 10:00 | inicio rev21\n2026-11-13 10:30 | 4 fin\n",
         "2026-11-13T18:00:00Z", f"| 1 | Inventario | 11-12 21:00 | 11-12 {fin} | x |\n| 4 | Comp | 11-13 10:00 | 11-13 10:30 | x |\n", ["4"])
# B) MISMA rev, trabajo de la noche anterior, 'inicio rev21' y VP escritos tarde a la manana siguiente (>12 h): residual de diseno
caso("B_tarde_dia_sig misma rev, arranque anotado al dia siguiente", PREV + "2026-11-12 17:00 | 1 inicio\n2026-11-12 17:30 | 1 fin\n"
     "2026-11-12 18:30 | 2-3 fin\n2026-11-13 08:00 | inicio rev21\n2026-11-13 08:30 | 4 fin\n", "2026-11-13T16:00:00Z",
     "| 1 | Inv | 11-12 17:00 | 11-12 17:30 | x |\n| 2-3 | Lect | 11-12 17:30 | 11-12 18:30 | x |\n| 4 | Comp | 11-13 08:00 | 11-13 08:30 | x |\n", ["4"])
# C) marcas de la rev ACTUAL hacia atras dentro de la rev (cada salto <= 12 h no es 'fuera de orden'): 10:00 -> 23:00 (dia ant.) -> 12:00
caso("C_cadena_atras marcas de la rev con saltos atras <12h", "2026-11-13 10:00 | inicio rev21\n2026-11-12 23:00 | 1 fin\n"
     "2026-11-12 12:00 | 2-3 fin\n2026-11-13 10:30 | 4 fin\n", "2026-11-13T18:00:00Z",
     "| 1 | Inv | 11-12 22:00 | 11-12 23:00 | x |\n| 2-3 | Lect | 11-12 11:00 | 11-12 12:00 | x |\n| 4 | Comp | 11-13 10:00 | 11-13 10:30 | x |\n",
     ["1", "4"])
# D) paso exento (rev anterior) + marca '| 5 fin' DESPUES del arranque sin fila ni --paso: debe seguir FAIL
caso("D_marca_post paso exento + marca posterior del mismo paso sin corrida", PREV + "2026-11-11 09:00 | 5 fin\n2026-11-13 10:00 | inicio rev21\n"
     "2026-11-13 11:00 | 5 fin\n2026-11-13 11:30 | 4 fin\n", "2026-11-13T18:00:00Z",
     "| 5 | Cuant | 11-11 08:00 | 11-11 09:00 | x |\n| 4 | Comp | 11-13 10:00 | 11-13 11:30 | x |\n", ["4"])
# E) fila sin fecha (solo HH:MM) de la rev anterior >12 h antes: no se exime; su marca vieja se descarta -> no cuadra (FAIL, mas estricto)
caso("E_sin_fecha fila sin MM-DD de rev anterior con su --paso", PREV + "2026-11-11 09:00 | 1 fin\n2026-11-13 10:00 | inicio rev21\n"
     "2026-11-13 10:30 | 4 fin\n", "2026-11-13T18:00:00Z", "| 1 | Inv | 08:00 | 09:00 | x |\n| 4 | Comp | 11-13 10:00 | 11-13 10:30 | x |\n", ["1", "4"])
# F) filas duplicadas identicas: una vieja exenta, la otra igual -> ambas fuera (misma Fin, misma marca)
caso("F_dup filas identicas viejas", PREV + "2026-11-11 09:00 | 1 fin\n2026-11-13 10:00 | inicio rev21\n2026-11-13 10:30 | 4 fin\n",
     "2026-11-13T18:00:00Z", "| 1 | Inv | 11-11 08:00 | 11-11 09:00 | x |\n| 1 | Inv | 11-11 08:00 | 11-11 09:00 | x |\n"
     "| 4 | Comp | 11-13 10:00 | 11-13 10:30 | x |\n", ["4"])
# G) alarma: marcas en la ventana (arranque-12h, arranque) de la rev anterior SIN fila exenta cuentan para t0 -> cruce detectado
caso("G_alarma_ventana cruce del presupuesto con marcas de la ventana de 12 h", PREV + "2026-11-13 00:30 | 9 fin\n2026-11-13 08:00 | inicio rev21\n"
     "2026-11-13 08:30 | 4 fin\n", "2026-11-13T16:00:00Z", "| 9 | Sub | 11-13 00:00 | 11-13 00:30 | x |\n| 4 | Comp | 11-13 08:00 | 11-13 08:30 | x |\n",
     ["4", "9"], na=1)
# H) alarma: la rev ACTUAL pasa el presupuesto por si sola (arranque 08:00, pasos hasta 13:00, na=1) sin ALERTA -> FAIL en ambos
caso("H_alarma_propia la rev actual cruza el presupuesto sola", PREV + "2026-11-11 09:00 | 1 fin\n2026-11-13 08:00 | inicio rev21\n"
     "2026-11-13 10:00 | 2-3 fin\n2026-11-13 13:00 | 4 fin\n", "2026-11-13T16:00:00Z",
     "| 1 | Inv | 11-11 08:00 | 11-11 09:00 | x |\n| 2-3 | L | 11-13 08:00 | 11-13 10:00 | x |\n| 4 | Comp | 11-13 10:00 | 11-13 13:00 | x |\n",
     ["2-3", "4"], na=1)
# I) TZ: VERSION_PROYECTO sin zona (operador escribe hora PT 10:00 sin Z) -> se lee como UTC = 02:00 PT (arranque MAS temprano, mas estricto)
caso("I_vp_naive VP sin zona", PREV + "2026-11-12 17:00 | 1 fin\n2026-11-13 10:00 | inicio rev21\n2026-11-13 10:30 | 4 fin\n",
     "2026-11-13T10:00:00", "| 1 | Inv | 11-12 16:00 | 11-12 17:00 | x |\n| 4 | Comp | 11-13 10:00 | 11-13 10:30 | x |\n", ["4"])
# J) TZ: log escrito en UTC por error (marcas +8 h) con VP UTC correcto: el arranque sale de VP (min) -> ver si se exime algo de la misma rev
caso("J_log_utc log en hora UTC, VP correcto", PREV + "2026-11-13 04:30 | 1 fin\n2026-11-13 18:00 | inicio rev21\n2026-11-13 18:30 | 4 fin\n",
     "2026-11-13T18:00:00Z", "| 1 | Inv | 11-13 04:00 | 11-13 04:30 | x |\n| 4 | Comp | 11-13 18:00 | 11-13 18:30 | x |\n", ["4"])
