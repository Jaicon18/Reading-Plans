# adv11_delta: delta 37f154d -> 3aa8703 (marcas_rev_anterior/tope/RX_ENTREGA_LOG). v137 vs candidato via proceso_v119. Sintetico en /tmp/verif12/tmp/a11.
# Uso: python3 -I /tmp/verif11/adv11_delta.py   (basado en verif10_adversariales/adv10_delta.py; VP con renglones libres)
import sys, os, json, subprocess, shutil, textwrap
V137 = "/tmp/v137/take-off-metal-frame-drywall"; CAND = "/tmp/v138r3/take-off-metal-frame-drywall"; BASE = "/tmp/verif12/tmp/a11"
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
def caso(nombre, log, vps, tt, pasos, na=10):
    global NREG
    w = os.path.join(BASE, nombre.split()[0])
    if os.path.isdir(w): shutil.rmtree(w)
    e = os.path.join(w, "rev21 FINAL PARA REVISAR"); os.makedirs(os.path.join(e, "Take-off"))
    open(os.path.join(e, "Take-off", "Z9_Takeoff_rev21.xlsx"), "w").write("x")
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
VP21 = ("2026-11-13T16:00:00Z", "rev21")          # 08:00 PT
# Escenario base B (misma rev, 'inicio rev21' anotado tarde): pasos 1 y 2-3 de rev21 cerrados la noche anterior SIN --paso
def base_b(nota):
    return ("2026-11-12 17:00 | 1 inicio\n2026-11-12 17:30 | 1 fin" + nota + "\n2026-11-12 18:30 | 2-3 fin\n"
            "2026-11-13 08:00 | inicio rev21\n2026-11-13 08:30 | 4 fin\n")
TT_B = "| 1 | Inv | 11-12 17:00 | 11-12 17:30 | x |\n| 2-3 | Lect | 11-12 17:30 | 11-12 18:30 | x |\n| 4 | Comp | 11-13 08:00 | 11-13 08:30 | x |\n"
caso("C0_control_sin_evidencia B sin evidencia (debe = v137)", base_b(""), [VP21], TT_B, ["4"])
caso("F1_rev_en_nota nota de la rev actual con 'Rev 5' de los planos", base_b(" | planos A-101 Rev 5 del arquitecto"), [VP21], TT_B, ["4"])
caso("F2_upload_nota nota 'uploaded' de la rev actual", base_b(" | uploaded plans to Drive"), [VP21], TT_B, ["4"])
caso("F3_entregados nota 'planos entregados por el GC'", base_b(" | planos entregados por el GC"), [VP21], TT_B, ["4"])
caso("F3b_no_entregado nota 'aun NO entregado'", base_b(" | aun no entregado"), [VP21], TT_B, ["4"])
caso("F3c_deliverables nota 'deliverables'", base_b(" | lista de deliverables"), [VP21], TT_B, ["4"])
# F4: alarma - marcas de la rev actual antes de una marca de evidencia falsa (dentro de las 12 h) se descartan: cruce del 50 % oculto
caso("F4_alarma_oculta cruce 50% oculto por marcas descartadas (nota 'subidos')",
     "2026-11-13 02:00 | 0 Arranque | inicio\n2026-11-13 04:50 | planos subidos por el GC\n2026-11-13 05:00 | inicio rev21\n"
     "2026-11-13 05:30 | 4 fin\n2026-11-13 06:20 | 5 fin\n", [("2026-11-13T13:00:00Z", "rev21")],
     "| 4 | Comp | 11-13 05:00 | 11-13 05:30 | x |\n| 5 | Cuant | 11-13 05:30 | 11-13 06:20 | x |\n", ["4", "5"])
caso("F4c_control misma alarma sin la nota (debe = v137 FAIL)",
     "2026-11-13 02:00 | 0 Arranque | inicio\n2026-11-13 04:50 | planos del GC\n2026-11-13 05:00 | inicio rev21\n"
     "2026-11-13 05:30 | 4 fin\n2026-11-13 06:20 | 5 fin\n", [("2026-11-13T13:00:00Z", "rev21")],
     "| 4 | Comp | 11-13 05:00 | 11-13 05:30 | x |\n| 5 | Cuant | 11-13 05:30 | 11-13 06:20 | x |\n", ["4", "5"])
caso("F4b_alarma_rev_real la evidencia real 'rev20 entregada' 10 min antes; '0 Arranque' 02:00 sin etiqueta",
     "2026-11-13 02:00 | 0 Arranque | inicio\n2026-11-13 04:50 | rev20 entregada\n2026-11-13 05:00 | inicio rev21\n"
     "2026-11-13 05:30 | 4 fin\n2026-11-13 06:20 | 5 fin\n", [("2026-11-13T13:00:00Z", "rev21")],
     "| 4 | Comp | 11-13 05:00 | 11-13 05:30 | x |\n| 5 | Cuant | 11-13 05:30 | 11-13 06:20 | x |\n", ["4", "5"])
# F5: tope de VERSION_PROYECTO de OTRA rev POSTERIOR al arranque; fila 2-3 sin marca ni --paso
LOG5 = "2026-11-12 09:00 | 0 Arranque | inicio\n2026-11-13 10:00 | inicio rev21\n2026-11-13 10:30 | 4 fin\n"
TT5 = "| 2-3 | Lect | 11-12 10:00 | 11-12 12:00 | x |\n| 4 | Comp | 11-13 10:00 | 11-13 10:30 | x |\n"
caso("F5_vp_tope_posterior VP rev20 con sello POSTERIOR al arranque de rev21", LOG5,
     [("2026-11-14T00:00:00Z", "rev20"), ("2026-11-13T18:00:00Z", "rev21")], TT5, ["4"])
caso("F5c_vp_tope_anterior control: VP rev20 anterior a la fila", LOG5,
     [("2026-11-01T00:00:00Z", "rev20"), ("2026-11-13T18:00:00Z", "rev21")], TT5, ["4"])
caso("F5d_vp_rev22 VP con renglon rev22 (rev POSTERIOR) posterior al arranque", LOG5,
     [("2026-11-13T18:00:00Z", "rev21"), ("2026-11-14T00:00:00Z", "rev22")], TT5, ["4"])
# F6: tope de una marca con hora POSTERIOR al arranque (errata de fecha), puesta antes del arranque en el archivo
caso("F6_marca_tope_posterior 'rev20 entregada' con fecha 11-14 antes de 'inicio rev21' 11-13",
     "2026-11-12 09:00 | 0 Arranque | inicio\n2026-11-14 09:00 | rev20 entregada\n2026-11-13 10:00 | inicio rev21\n2026-11-13 10:30 | 4 fin\n",
     [("2026-11-13T18:00:00Z", "rev21")], TT5, ["4"])
# F7: tope de una evidencia FALSA ('Rev 5' de planos) -> fila sin marca exenta
caso("F7_tope_falso fila sin marca exenta por tope de nota 'Rev 5'",
     "2026-11-12 09:00 | 0 Arranque | inicio\n2026-11-12 20:00 | recibido A-101 Rev 5\n2026-11-13 10:00 | inicio rev21\n2026-11-13 10:30 | 4 fin\n",
     [("2026-11-13T18:00:00Z", "rev21")], TT5, ["4"])
# F8: evidencia DESPUES del arranque en el archivo (control: nada exento)
caso("F8_evidencia_post 'rev20 entregada' despues de 'inicio rev21'",
     "2026-11-12 09:00 | 0 Arranque | inicio\n2026-11-12 10:00 | 2-3 fin\n2026-11-13 10:00 | inicio rev21\n2026-11-13 10:05 | rev20 entregada\n2026-11-13 10:30 | 4 fin\n",
     [("2026-11-13T18:00:00Z", "rev21")], TT5.replace("11-12 12:00", "11-12 10:00"), ["4"])
# F9: varias revs: rev19 entregada, luego pasos sin etiqueta, luego inicio rev21 (evidencia = rev19 solamente)
caso("F9_varias_revs rev19 entregada y luego pasos de rev21 sin etiqueta anotados antes de 'inicio rev21'",
     "2026-11-10 09:00 | rev19 entregada\n2026-11-12 17:00 | 1 inicio\n2026-11-12 17:30 | 1 fin\n2026-11-12 18:30 | 2-3 fin\n"
     "2026-11-13 08:00 | inicio rev21\n2026-11-13 08:30 | 4 fin\n", [VP21], TT_B, ["4"])
print("REGRESIONES:", NREG)
