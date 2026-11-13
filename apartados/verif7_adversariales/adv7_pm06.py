# adv7_pm06: NG-3.3 / BE-PM06 + CE_PROTOCOLO_3H (tiempos_desde) contra v81cf138. Sintético en /tmp/verif7/tmp.
import sys, os, json, tempfile; sys.path.insert(0, sys.argv[1]); import compuerta_entrega as CE
T = "/tmp/verif7/tmp"; os.makedirs(T, exist_ok=True)
VER = CE._skill_version() or "v81cf138"
def mk(log, tt_rows, vp_ts, pasos_corridos, cumulative=False, xl="Z9_Takeoff_rev21.xlsx"):
    w0 = tempfile.mkdtemp(dir=T); w = os.path.join(w0, "rev21") if cumulative else w0
    e = os.path.join(w, "rev21 FINAL PARA REVISAR"); os.makedirs(os.path.join(e, "Take-off"))
    open(os.path.join(e, "Take-off", xl), "w").write("x")
    open(os.path.join(w0 if cumulative else w, "tiempos.log"), "w").write(log)
    open(os.path.join(w, "VERSION_PROYECTO.txt"), "w").write(f"{vp_ts} | rev21 | {VER}\n")
    if pasos_corridos:
        open(os.path.join(w, "compuerta_corridas.jsonl"), "w").write("".join(json.dumps({"paso": p, "rc": 0}) + "\n" for p in pasos_corridos))
        CE.sellar_bitacora(w, os.path.join(w, "compuerta_corridas.jsonl"))
    tt = "| # | Paso | Inicio | Fin | Min |\n|---|---|---|---|---|\n" + "".join(tt_rows)
    return w, e, tt
ROWS = ["| 1 | Inventario | 11-13 08:00 | 11-13 08:30 | 30 |\n", "| 2-3 | Lecturas | 11-13 08:30 | 11-13 09:30 | 60 |\n",
        "| 4 | Comparación | 11-13 10:00 | 11-13 10:30 | 30 |\n"]
# P0 control: el log trae todas las marcas de la rev; los pasos 1 y 2-3 sin '--paso' -> FAIL
w, e, tt = mk("2026-11-13 08:00 | 1 inicio rev21\n2026-11-13 08:30 | 1 fin\n2026-11-13 09:30 | 2-3 fin\n2026-11-13 10:30 | 4 fin\n",
              ROWS, "2026-11-13T16:00:00+00:00", ["4"])
print("P0 control (log completo, pasos 1 y 2-3 sin --paso) ->", CE.proceso_v119(w, e, tt, 5))
# P1: MISMA rev (todo 13-nov, después de v119; VERSION_PROYECTO.txt fijado 08:00 PT), pero la marca 'inicio rev21' se escribió tarde (10:00):
#     los pasos 1 y 2-3 de ESTA rev (sin --paso) quedan 'de una rev anterior'
w, e, tt = mk("2026-11-13 10:00 | 4 inicio rev21\n2026-11-13 10:30 | 4 fin\n", ROWS, "2026-11-13T16:00:00+00:00", ["4"])
print("P1 log propio que arranca tarde (10:00), VERSION_PROYECTO 08:00 PT ->", CE.proceso_v119(w, e, tt, 5))
# P2: log acumulado del proyecto; marcas de la rev21 de 08:00-09:30 sin etiqueta y la etiqueta 'inicio rev21' recién a las 10:00
w, e, tt = mk("05-nov 11:26 PST | 0 Arranque rev20 | inicio\n05-nov 19:00 PST | rev20 entregada\n"
              "2026-11-13 08:00 | 1 inicio\n2026-11-13 08:30 | 1 fin\n2026-11-13 09:30 | 2-3 fin\n"
              "2026-11-13 10:00 | inicio rev21 (etiqueta)\n2026-11-13 10:30 | 4 fin\n", ROWS, "2026-11-13T16:00:00+00:00", ["4"], cumulative=True)
print("P2 log acumulado, etiqueta 'inicio rev21' tarde (10:00), pasos 1 y 2-3 del 13-nov ->", CE.proceso_v119(w, e, tt, 5))
# P3 (alarma): presupuesto 180 min; la rev arranca 08:00, el 100 % se cruza 11:00; el plazo se mide desde la marca tardía
LOG = ("2026-11-13 10:00 | inicio rev21\n2026-11-13 10:30 | 4 fin\n2026-11-13 11:40 | 5 fin\n2026-11-13 13:10 | 6 fin\n")
ROWS3 = ROWS + ["| 5 | Markups | 11-13 10:30 | 11-13 11:40 | 70 |\n", "| 6 | Excel | 11-13 11:40 | 11-13 13:10 | 90 |\n"]
w, e, tt = mk(LOG, ROWS3, "2026-11-13T16:00:00+00:00", ["1", "2-3", "4", "5", "6"])
CE.alerta_presupuesto(w, 5)    # UNA alerta al final (190 min desde 10:00 = 105 %); desde las 08:00 reales ya eran 310 min
print("P3 arranque real 08:00 (VERSION_PROYECTO), log desde 10:00, una alerta al final ->", CE.proceso_v119(w, e, tt, 5))
