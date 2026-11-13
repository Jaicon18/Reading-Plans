# adv8_pm06: CE_PROTOCOLO_3H proceso_v119 / arranque_rev_desde / tiempos_desde — v137 vs candidato. Sintético en /tmp/verif10/tmp.
import sys, os, json, tempfile; sys.path.insert(0, sys.argv[1]); import compuerta_entrega as CE
T = "/tmp/verif10/tmp"; os.makedirs(T, exist_ok=True)
VER = CE._skill_version()
def mk(log, rows, vp_ts, pasos_corridos):
    w = tempfile.mkdtemp(dir=T)
    e = os.path.join(w, "rev21 FINAL PARA REVISAR"); os.makedirs(os.path.join(e, "Take-off"))
    open(os.path.join(e, "Take-off", "Z9_Takeoff_rev21.xlsx"), "w").write("x")
    if log is not None: open(os.path.join(w, "tiempos.log"), "w").write(log)
    open(os.path.join(w, "VERSION_PROYECTO.txt"), "w").write(f"{vp_ts} | rev21 | {VER}\n")
    if pasos_corridos:
        open(os.path.join(w, "compuerta_corridas.jsonl"), "w").write("".join(json.dumps({"paso": p, "rc": 0}) + "\n" for p in pasos_corridos))
        CE.sellar_bitacora(w, os.path.join(w, "compuerta_corridas.jsonl"))
    tt = "| # | Paso | Inicio | Fin | Min |\n|---|---|---|---|---|\n" + "".join(rows)
    return w, e, tt
def show(n, r):
    print(n, "->", r[0], "|", " || ".join(m[:150] for m in r[1][:5]))
# Q1: TIEMPOS.md arrastra el paso 9 de la rev anterior (cierra 08:40); el paso 1 de ESTA rev empieza 08:40 (inicio = fin del anterior)
#     y cierra 09:30, sin su --paso. Log de la rev desde 08:45 sin marcas 'N fin' (solo texto libre).
ROWS = ["| 9 | Subida rev20 | 11-13 08:00 | 11-13 08:40 | 40 |\n", "| 1 | Inventario rev21 | 11-13 08:40 | 11-13 09:30 | 50 |\n",
        "| 4 | Comparación | 11-13 09:30 | 11-13 10:30 | 60 |\n"]
w, e, tt = mk("2026-11-13 08:45 | inicio rev21\n2026-11-13 09:30 | inventario listo\n2026-11-13 10:30 | comparacion lista\n", ROWS,
              "2026-11-13T16:45:00+00:00", ["4"])
print("tiempos_desde Q1:", CE.tiempos_desde(tt, CE.arranque_rev_desde(w, e, CE.inicio_rev_info(w, e)[0])) if hasattr(CE, "tiempos_desde") else "-")
show("Q1 fila del paso 1 (cierra DESPUÉS del arranque) borrada porque su Inicio = Fin del paso 9 anterior", CE.proceso_v119(w, e, tt, 5))
# Q2: tiempos.log existe pero sin marcas legibles (texto libre); sin git; VERSION_PROYECTO.txt fijado AL FINAL (14:00 PT);
#     todos los pasos de ESTA rev cerraron antes de las 14:00 y ninguno tiene su --paso
ROWS2 = ["| 1 | Inventario | 11-13 08:00 | 11-13 08:30 | 30 |\n", "| 2-3 | Lecturas | 11-13 08:30 | 11-13 09:30 | 60 |\n",
         "| 4 | Comparación | 11-13 10:00 | 11-13 10:30 | 30 |\n"]
w, e, tt = mk("arranque rev21 a las 8 de la mañana\nlecturas listas\n", ROWS2, "2026-11-13T22:00:00+00:00", [])
show("Q2 log sin marcas ISO + VERSION_PROYECTO fijado al final (14:00 PT), pasos sin --paso", CE.proceso_v119(w, e, tt, 5))
# Q3: sin tiempos.log; VERSION_PROYECTO al final
w, e, tt = mk(None, ROWS2, "2026-11-13T22:00:00+00:00", [])
show("Q3 SIN tiempos.log + VERSION_PROYECTO fijado al final", CE.proceso_v119(w, e, tt, 5))
# Q4: log con 1 sola marca (la de inicio, tarde 13:50) + VERSION_PROYECTO 14:00; pasos 1-4 cerrados 08:30-10:30 sin --paso
w, e, tt = mk("2026-11-13 13:50 | inicio rev21\n", ROWS2, "2026-11-13T22:00:00+00:00", [])
show("Q4 log con UNA marca tardía 13:50 + VERSION_PROYECTO 14:00; pasos de la mañana sin --paso", CE.proceso_v119(w, e, tt, 5))
# Q1b: igual que Q1 con presupuesto mayor (na=40 hojas) para que la alarma no tape: ¿queda algo que marque el paso 1 sin --paso?
w, e, tt = mk("2026-11-13 08:45 | inicio rev21\n2026-11-13 09:30 | inventario listo\n2026-11-13 10:30 | comparacion lista\n", ROWS,
              "2026-11-13T16:45:00+00:00", ["4"])
print("presupuesto na=40:", CE.presupuesto_min(40))
show("Q1b (Q1 con presupuesto grande)", CE.proceso_v119(w, e, tt, 40))
