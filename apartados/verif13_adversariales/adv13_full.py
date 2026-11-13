# adv12_delta (copia de adv11 con casos nuevos, delta 3aa8703 -> 25f9fd1): delta 37f154d -> 3aa8703 (marcas_rev_anterior/tope/RX_ENTREGA_LOG). v137 vs candidato via proceso_v119. Sintetico en /tmp/verif13/tmp/a12.
# Uso: python3 -I /tmp/verif13/adv11_delta.py   (basado en verif10_adversariales/adv10_delta.py; VP con renglones libres)
import sys, os, json, subprocess, shutil, textwrap
V137 = "/tmp/v138fb/take-off-metal-frame-drywall"; CAND = "/tmp/v139p/take-off-metal-frame-drywall"; BASE = "/tmp/verif13/tmp/a13"
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
TT = "| 1 | Inv | 11-11 08:00 | 11-11 08:30 | x |\n| 2-3 | Lect | 11-11 08:30 | 11-11 09:30 | x |\n| 4 | Comp | 11-13 08:00 | 11-13 08:30 | x |\n"
BASE_L = "2026-11-11 08:00 | 1 inicio\n2026-11-11 08:30 | 1 fin\n2026-11-11 09:30 | 2-3 fin\n"
FIN = "2026-11-13 08:00 | inicio rev21\n2026-11-13 08:30 | 4 fin\n"
def ev(linea, **k):
    return BASE_L + linea + "\n" + FIN
caso("C1_legit control 'rev20 entregada' (PASS legitimo)", ev("2026-11-11 18:00 | rev20 entregada"), [("2026-11-13T18:00:00Z", "rev21")], TT, ["4"])
# ===== verificacion 13: ataques nuevos sobre la funcion completa =====
VP21 = ("2026-11-13T18:00:00Z", "rev21")
LOGW = ("2026-11-12 17:00 | 0 Arranque\n2026-11-12 17:30 | 1 fin\n2026-11-12 18:30 | 2-3 fin\n2026-11-13 08:00 | inicio rev21\n"
        "2026-11-13 08:30 | 4 fin\n")
TTW = "| 1 | Inv | 11-12 17:00 | 11-12 17:30 | x |\n| 2-3 | Lect | 11-12 17:30 | 11-12 18:30 | x |\n| 4 | Comp | 11-13 08:00 | 11-13 08:30 | x |\n"
# W2: rev actual mal leida SOLO desde VERSION_PROYECTO (typo --rev rev22), Excel sin etiqueta: k0 salta 'inicio rev21' y la vuelve evidencia
caso("W2_vp_rev22 Excel sin revN, VP ultimo renglon rev22 (typo), log 'inicio rev21' tardio", LOGW, [("2026-11-13T18:00:00Z", "rev22")], TTW, ["4"], xl="Z9_Takeoff.xlsx")
caso("W2b_vp_rev21_rev22 Excel sin revN, VP rev21 y luego rev22", LOGW, [("2026-11-13T16:05:00Z", "rev21"), ("2026-11-13T18:00:00Z", "rev22")], TTW, ["4"], xl="Z9_Takeoff.xlsx")
caso("W2c_control Excel rev21 + VP rev22 (deben discrepar: FAIL)", LOGW, [("2026-11-13T18:00:00Z", "rev22")], TTW, ["4"])
caso("W2d_control Excel sin revN + VP rev21 (FAIL)", LOGW, [VP21], TTW, ["4"], xl="Z9_Takeoff.xlsx")
caso("W2e_markup_pdf_rev22 Excel rev21 viejo + PDF de markups '_rev22' mas nuevo + VP rev22", LOGW, [("2026-11-13T18:00:00Z", "rev22")], TTW, ["4"], xl="Z9_Takeoff.xlsx", extra=["Planos marcados/Z9_markups_rev22.pdf"])
# X1: 'linea' quita por TEXTO: misma linea en dos tablas con columnas Inicio/Fin invertidas -> se quita la fila de la rev actual
LOGX = ("2026-11-12 19:00 | 1 inicio\n2026-11-12 19:30 | 1 fin\n2026-11-12 19:45 | rev20 entregada\n2026-11-13 07:59 | nota\n"
        "2026-11-12 19:40 | 5 fin\n2026-11-13 08:00 | inicio rev21\n2026-11-13 08:30 | 4 fin\n")
TA = "| 1 | Inv | 11-12 19:00 | 11-12 19:30 | x |\n| 4 | Comp | 11-13 08:00 | 11-13 08:30 | x |\n| 5 | Rev | 11-12 19:40 | 11-13 09:00 | x |\n"
TB = "\nrev20 (tabla vieja)\n\n| # | Paso | Fin | Inicio | Min |\n|---|---|---|---|---|\n| 5 | Rev | 11-12 19:40 | 11-13 09:00 | x |\n"
caso("X1_linea_dos_tablas fila 5 de rev21 (fin 11-13 09:00 sin marca) identica en texto a la fila 5 de rev20 de otra tabla (Fin/Inicio)", LOGX, [VP21], TA + TB, ["4", "5"])
caso("X1c_control sin la tabla vieja (FAIL: paso 5 de rev21 sin marca 09:00)", LOGX, [VP21], TA, ["4", "5"])
caso("X1d_control tabla vieja con texto distinto (FAIL)", LOGX, [VP21], TA + TB.replace("| Rev |", "| Rev20 |"), ["4", "5"])
# negaciones / dudas fuera de la lista
for i, l in enumerate(["rev20 subida fallida", "rev20 subida: error 403", "rev20 entregada (falso)", "¡rev20 entregada! nunca", "¿rev20 entregada",
                       "rev20 entregada -> rechazada", "rev20 subida mañana", "rev20 entregada [cancelada]", "rev20 entregada NO", "rev20 entregada ?"]):
    caso(f"G{i}_neg '{l}'", ev("2026-11-11 18:00 | " + l), [VP21], TT, ["4"])
# fechas raras / robustez
caso("Y1_vp_anio1 VP rev21 '0001-01-01T00:00:00Z'", ev("2026-11-11 18:00 | rev20 entregada"), [("0001-01-01T00:00:00Z", "rev21")], TT, ["4"])
caso("Y2_vp_rev20_anio1 VP rev20 '0001-01-01T00:00:00Z' + rev21 (rama VP)", BASE_L + FIN, [("0001-01-01T00:00:00Z", "rev20"), VP21], TT, ["4"])
caso("Y3_vp_ts_basura VP rev20 'ayer' + rev21", BASE_L + FIN, [("ayer", "rev20"), VP21], TT, ["4"])
caso("Y4_fila_sin_fecha fila 1 con Fin '08:30' sin MM-DD", ev("2026-11-11 18:00 | rev20 entregada"), [VP21],
     "| 1 | Inv | 08:00 | 08:30 | x |\n| 4 | Comp | 11-13 08:00 | 11-13 08:30 | x |\n", ["4"])
caso("Y5_fila_fecha_imposible Fin '02-30 08:30'", ev("2026-11-11 18:00 | rev20 entregada"), [VP21],
     "| 1 | Inv | 02-30 08:00 | 02-30 08:30 | x |\n| 4 | Comp | 11-13 08:00 | 11-13 08:30 | x |\n", ["4"])
caso("Y6_log_fecha_imposible marca '2026-13-45 08:00'", "2026-13-45 08:00 | rev20 entregada\n" + BASE_L + FIN, [VP21], TT, ["4"])
caso("Y7_vp_tz_rara VP rev20 '2026-11-11T18:00:00+14:00'", BASE_L + FIN, [("2026-11-11T18:00:00+14:00", "rev20"), VP21], TT, ["4"])
caso("Y8_ev_anio_previo 'rev20 entregada' 2025-11-11 (anio anterior)", BASE_L.replace("2026-11-11", "2026-11-11") + "2025-11-11 18:00 | rev20 entregada\n" + FIN, [VP21], TT, ["4"])
caso("Y9_rev0 'inicio rev0' como evidencia (rev menor valida)", ev("2026-11-11 18:00 | inicio rev0"), [VP21], TT, ["4"])
# fila de rev21 con fecha anterior al tope (mentira de fecha): regla 'cierra antes del tope' sin marca
caso("Z1_fila_rev21_fecha_vieja fila 5 'Fin 11-03 09:00' sin marca, sin --paso 5", ev("2026-11-11 18:00 | rev20 entregada"), [VP21],
     TT + "| 5 | Rev | 11-03 08:00 | 11-03 09:00 | x |\n", ["4"])
caso("Z1c_control mismo sin evidencia (FAIL)", BASE_L + FIN, [VP21], TT + "| 5 | Rev | 11-03 08:00 | 11-03 09:00 | x |\n", ["4"])
# evidencia de 're-subida' de rev20 DESPUES de pasos de rev21 sin etiqueta (orden del archivo respetado)
caso("Z2_resubida rev21 pasos 11-11 sin etiqueta, luego 'rev20 subida' 11-12 20:00 (re-subida), 'inicio rev21' 11-13",
     "2026-11-10 08:00 | rev20 entregada\n" + BASE_L + "2026-11-12 19:00 | rev20 subida\n" + FIN, [VP21], TT, ["4"])
print("REGRESIONES:", NREG)
