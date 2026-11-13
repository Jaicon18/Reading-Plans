import sys, os, tempfile; sys.path.insert(0, sys.argv[1]); import compuerta_entrega as CE
T = "/tmp/verif6/tmp"; os.makedirs(T, exist_ok=True)
TT = ("| Paso | Inicio (PST) | Fin (PST) | Duración |\n|---|---|---|---|\n"
      "| 1 | 11-13 09:00 | 11-13 09:40 | 40 min |\n| 2-3 | 11-13 09:40 | 11-13 11:00 | 80 min |\n"
      "| 4 | 11-13 11:00 | 11-13 12:20 | 80 min |\n| 5 | 11-13 12:20 | 11-13 13:00 | 40 min |\n| TOTAL | | | 240 min |\n")
REG = [{"evento": "fin", "paso": p} for p in ("1", "2-3", "4", "5")]
def caso(log, alertas_al_final=True, alertas_en_vivo=False):
    w = tempfile.mkdtemp(dir=T)
    lines = log.strip().splitlines()
    if alertas_en_vivo:   # alert written at each step close (the intended behaviour)
        for k in range(1, len(lines) + 1):
            open(os.path.join(w, "tiempos.log"), "w").write("\n".join(lines[:k]) + "\n"); CE.alerta_presupuesto(w, 5)
    open(os.path.join(w, "tiempos.log"), "w").write(log)
    if alertas_al_final:  # ONE alert written at the very end (e.g. at the final gate), 240 min = 133 %
        CE.alerta_presupuesto(w, 5)
    return CE.alarma_fallas(w, 5, registro=REG, tiempos_txt=TT)
LOG_FIN = ("2026-11-13 09:00 | 1 inicio\n2026-11-13 09:40 | 1 fin\n2026-11-13 11:00 | 2-3 fin\n2026-11-13 12:20 | 4 fin\n"
           "2026-11-13 13:00 | 5 fin\n")
LOG_TXT = ("2026-11-13 09:00 | inicio inventario\n2026-11-13 09:40 | inventario cerrado\n2026-11-13 11:00 | lecturas A/B cerradas\n"
           "2026-11-13 12:20 | comparación cerrada\n2026-11-13 13:00 | markups cerrados\n")
LOG_ES = LOG_FIN.replace(" fin", " terminado")
print("N0 control: log '| N fin', alerts written live at each step ->", caso(LOG_FIN, False, True))
print("N1 control: log '| N fin', ONE alert at the end ->", [x[:90] for x in caso(LOG_FIN)])
print("N2 log without 'N fin' text (pasos de TIEMPOS.md), ONE alert at the end (no live alarm) ->", caso(LOG_TXT))
print("N3 log '| N terminado' (Spanish), ONE alert at the end ->", caso(LOG_ES))
print("N4 log without 'N fin', NO alert file at all ->", [x[:90] for x in caso(LOG_TXT, False)])
