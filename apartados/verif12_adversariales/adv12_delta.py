# adv12_delta (copia de adv11 con casos nuevos, delta 3aa8703 -> 25f9fd1): delta 37f154d -> 3aa8703 (marcas_rev_anterior/tope/RX_ENTREGA_LOG). v137 vs candidato via proceso_v119. Sintetico en /tmp/verif12/tmp/a12.
# Uso: python3 -I /tmp/verif11/adv11_delta.py   (basado en verif10_adversariales/adv10_delta.py; VP con renglones libres)
import sys, os, json, subprocess, shutil, textwrap
V137 = "/tmp/v137/take-off-metal-frame-drywall"; CAND = "/tmp/v138r3/take-off-metal-frame-drywall"; BASE = "/tmp/verif12/tmp/a12"
RUN = textwrap.dedent(r'''
    import sys, os, json
    S, W, E, NA = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    sys.path.insert(0, os.path.join(S, "tools")); import compuerta_entrega as CE
    tt = open(os.path.join(W, "_TIEMPOS.md")).read()
    try: est, ev = CE.proceso_v119(W, E, tt, NA)
    except Exception as ex: print("EXC", type(ex).__name__, str(ex)[:120]); sys.exit()
    print(json.dumps([est, [x[:120] for x in ev]], ensure_ascii=False))
''')
sys.path.insert(0, os.path.join(CAND, "tools")); import compuerta_entrega as CE
VER = CE._skill_version() or "v81cf138"
H = "| # | Paso | Inicio | Fin | Min |\n|---|---|---|---|---|\n"
NREG = 0
def caso(nombre, log, vps, tt, pasos, na=10, xl="Z9_Takeoff_rev21.xlsx", extra=None):
    global NREG
    w = os.path.join(BASE, nombre.split()[0])
    if os.path.isdir(w): shutil.rmtree(w)
    e = os.path.join(w, "rev21 FINAL PARA REVISAR"); os.makedirs(os.path.join(e, "Take-off"))
    open(os.path.join(e, "Take-off", xl), "w").write("x")
    for rel in (extra or []):
        q = os.path.join(e, rel); os.makedirs(os.path.dirname(q), exist_ok=True); open(q, "w").write("x"); os.utime(q, (2e9, 2e9))
    open(os.path.join(w, "tiempos.log"), "w").write(log)
    open(os.path.join(w, "VERSION_PROYECTO.txt"), "w").write("".join(f"{ts} | {rv} | {VER}\n" for ts, rv in vps))
    open(os.path.join(w, "_TIEMPOS.md"), "w").write(H + tt)
    open(os.path.join(w, "compuerta_corridas.jsonl"), "w").write("".join(json.dumps({"paso": p, "rc": 0}) + "\n" for p in pasos))
    CE.sellar_bitacora(w, os.path.join(w, "compuerta_corridas.jsonl"))
    r = {}
    for k, S in (("v137", V137), ("cand", CAND)):
        p = subprocess.run([sys.executable, "-I", "-c", RUN, S, w, e, str(na)], capture_output=True, text=True)
        r[k] = (p.stdout.strip().splitlines() or ["STDERR " + p.stderr[-200:]])[-1]
    a, b = r["v137"], r["cand"]
    def st(x): return "PASS" if x.startswith('["PASS"') else ("FAIL" if x.startswith('["FAIL"') else x[:12])
    proc137 = [m for m in json.loads(a)[1] if not m.startswith("(7)")] if a.startswith("[") else []
    flag = ""
    if st(b) == "PASS" and proc137:
        flag = "  <<< REGRESION (v137 FAIL de proceso, cand PASS)"; NREG += 1
    print(f"--- {nombre}\n    v137: {a}\n    cand: {b}{flag}")
VP21 = ("2026-11-13T18:00:00Z", "rev21")          # 10:00 PT (posterior a 'inicio rev21' 08:00)
TT = "| 1 | Inv | 11-11 08:00 | 11-11 08:30 | x |\n| 2-3 | Lect | 11-11 08:30 | 11-11 09:30 | x |\n| 4 | Comp | 11-13 08:00 | 11-13 08:30 | x |\n"
BASE_L = "2026-11-11 08:00 | 1 inicio\n2026-11-11 08:30 | 1 fin\n2026-11-11 09:30 | 2-3 fin\n"
FIN = "2026-11-13 08:00 | inicio rev21\n2026-11-13 08:30 | 4 fin\n"
def ev(linea, **k):
    return BASE_L + linea + "\n" + FIN
caso("C0_control sin evidencia", BASE_L + FIN, [VP21], TT, ["4"])
caso("C1_legit 'rev20 entregada' (debe PASS)", ev("2026-11-11 18:00 | rev20 entregada"), [VP21], TT, ["4"])
for i, l in enumerate(["REV20 entregada", "Rev20 entregada", "prev20 entregada", "rev20 NO entregada", "rev 20 entregada",
                       "rev20entregada", "rev20 entregadas", "inicio REV20", "reinicio rev20", "rev2026 entregada"]):
    caso(f"L{i}_etq '{l}' (debe FAIL)", ev("2026-11-11 18:00 | " + l), [VP21], TT, ["4"])
caso("L10_rev22 'rev22 entregada' rev POSTERIOR (debe FAIL)", ev("2026-11-11 18:00 | rev22 entregada"), [VP21], TT, ["4"])
caso("L11_rev21a 'rev21a entregada' > rev21 (debe FAIL)", ev("2026-11-11 18:00 | rev21a entregada"), [VP21], TT, ["4"])
caso("L12_rev21 'rev21 subida' misma rev (k0) (debe FAIL)", ev("2026-11-11 18:00 | rev21 subida"), [VP21], TT, ["4"])
caso("O1_reinicio 're-inicio rev20' (observacion)", ev("2026-11-11 18:00 | re-inicio rev20"), [VP21], TT, ["4"])
caso("O2_neg 'rev20 entregada? no' (observacion)", ev("2026-11-11 18:00 | rev20 entregada? no, pendiente"), [VP21], TT, ["4"])
caso("O3_neg 'falta rev20 subida' (observacion)", ev("2026-11-11 18:00 | falta: rev20 subida"), [VP21], TT, ["4"])
# orden natural con otras etiquetas
caso("N1_rev9_vs_rev10 actual rev10, 'rev9 entregada' (legit PASS)", ev("2026-11-11 18:00 | rev9 entregada").replace("rev21", "rev10"),
     [("2026-11-13T18:00:00Z", "rev10")], TT, ["4"], xl="Z9_Takeoff_rev10.xlsx")
caso("N2_rev10_vs_rev9 actual rev9, 'rev10 entregada' (debe FAIL)", ev("2026-11-11 18:00 | rev10 entregada").replace("rev21", "rev9"),
     [("2026-11-13T18:00:00Z", "rev9")], TT, ["4"], xl="Z9_Takeoff_rev9.xlsx")
caso("N3_rev20a_vs_rev20 actual rev20, 'rev20a entregada' (debe FAIL)", ev("2026-11-11 18:00 | rev20a entregada").replace("rev21", "rev20"),
     [("2026-11-13T18:00:00Z", "rev20")], TT, ["4"], xl="Z9_Takeoff_rev20.xlsx")
caso("N4_rev20_vs_rev20a actual rev20a, 'rev20 entregada' (legit PASS)", ev("2026-11-11 18:00 | rev20 entregada").replace("rev21", "rev20a"),
     [("2026-11-13T18:00:00Z", "rev20a")], TT, ["4"], xl="Z9_Takeoff_rev20a.xlsx")
# evidencia exactamente en el arranque / 1 min antes
caso("T1_ev_en_arranque 'rev20 entregada' 08:00 = arranque (debe FAIL)",
     BASE_L + "2026-11-13 08:00 | rev20 entregada\n" + FIN, [VP21], TT, ["4"])
caso("T2_ev_1min_antes 'rev20 entregada' 07:59 (tope = arranque-12h: filas del 11-11 legit PASS)",
     BASE_L + "2026-11-13 07:59 | rev20 entregada\n" + FIN, [VP21], TT, ["4"])
caso("T3_tz VP rev20 '2026-11-13T15:30:00Z' (07:30 PT < arranque 08:00), sin marca de evidencia",
     BASE_L + FIN, [("2026-11-13T15:30:00Z", "rev20"), VP21], TT, ["4"])
caso("T4_tz VP rev20 '2026-11-13T16:30:00Z' (08:30 PT > arranque) (debe FAIL)",
     BASE_L + FIN, [("2026-11-13T16:30:00Z", "rev20"), VP21], TT, ["4"])
caso("T5_tz VP rev20 '2026-11-13T07:30:00-08:00' (debe PASS legit)",
     BASE_L + FIN, [("2026-11-13T07:30:00-08:00", "rev20"), VP21], TT, ["4"])
# etiqueta actual no detectable
caso("U1_sin_etiqueta Excel/carpeta/VP sin revN (debe FAIL)", ev("2026-11-11 18:00 | rev20 entregada").replace("inicio rev21", "inicio"),
     [("2026-11-13T18:00:00Z", "actual")], TT, ["4"], xl="Z9_Takeoff.xlsx")
# varias evidencias
caso("M1_dos_ev rev19 entregada (11-10) y rev20 entregada (11-11 07:00, antes de los pasos) (pasos 11-11 > tope: FAIL)",
     "2026-11-10 09:00 | rev19 entregada\n2026-11-11 07:00 | rev20 entregada\n" + BASE_L + FIN, [VP21], TT, ["4"])
# alarma: duplicado exacto de una marca exenta, puesto DESPUES de la evidencia (regla 4/6: no es 'antes de la evidencia')
TTD = "| 1 | Inv | 11-11 08:00 | 11-11 08:30 | x |\n| 4 | Comp | 11-13 08:00 | 11-13 08:30 | x |\n"
caso("D1_dup_despues_ev copia exacta '1 fin' despues de 'rev20 entregada' (regla estricta: se queda en la alarma)",
     "2026-11-11 08:00 | 1 inicio\n2026-11-11 08:30 | 1 fin\n2026-11-11 18:00 | rev20 entregada\n2026-11-11 08:30 | 1 fin\n" + FIN,
     [VP21], TTD, ["4"])
caso("D1c_control sin la copia", "2026-11-11 08:00 | 1 inicio\n2026-11-11 08:30 | 1 fin\n2026-11-11 18:00 | rev20 entregada\n" + FIN,
     [VP21], TTD, ["4"])
caso("D2_dup_en_rev copia exacta '1 fin' de rev20 DENTRO de rev21 (paso 5 de rev21 sin --paso escrito con hora de 1 fin? no: copia)",
     "2026-11-12 20:00 | 1 inicio\n2026-11-12 20:00 | 1 fin\n2026-11-13 07:00 | rev20 entregada\n2026-11-13 08:00 | inicio rev21\n2026-11-12 20:00 | 1 fin\n2026-11-13 08:30 | 4 fin\n",
     [VP21], "| 1 | Inv | 11-12 19:00 | 11-12 20:00 | x |\n| 4 | Comp | 11-13 08:00 | 11-13 08:30 | x |\n", ["4"])
# etiqueta actual mal detectada: PDF de planos 'Rev 25' mas nuevo en la entrega -> rev actual = 25; 'inicio rev21' (la PROPIA) pasa por evidencia
LOGW = ("2026-11-12 17:00 | 0 Arranque\n2026-11-12 17:30 | 1 fin\n2026-11-12 18:30 | 2-3 fin\n2026-11-13 08:00 | inicio rev21\n"
        "2026-11-13 08:30 | 4 fin\n")
TTW = "| 1 | Inv | 11-12 17:00 | 11-12 17:30 | x |\n| 2-3 | Lect | 11-12 17:30 | 11-12 18:30 | x |\n| 4 | Comp | 11-13 08:00 | 11-13 08:30 | x |\n"
caso("W0_control etiqueta bien (rev21): pasos propios sin --paso = FAIL", LOGW, [VP21], TTW, ["4"])
caso("W1_pdf_rev25 PDF 'A-101 Rev 25.pdf' mas nuevo en la entrega: rev actual leida = 25", LOGW, [VP21], TTW, ["4"],
     extra=["Planos/A-101 Rev 25.pdf"])
print("REGRESIONES:", NREG)
