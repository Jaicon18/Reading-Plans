import sys, os, tempfile; sys.path.insert(0, sys.argv[1]); import compuerta_entrega as CE
T = "/tmp/v138wip/tmp"; os.makedirs(T, exist_ok=True)
TT = "| Paso | Inicio | Fin | Duración |\n|---|---|---|---|\n| 1 | 11-13 09:00 | 11-13 09:30 | 30 min |\n| 4 | 11-13 09:30 | 11-13 10:00 | 30 min |\n"
def mk(name="rev21", log_parent=None, log_w=None):
    p = tempfile.mkdtemp(dir=T); w = os.path.join(p, name); os.makedirs(w)
    if log_parent is not None: open(os.path.join(p, "tiempos.log"), "w").write(log_parent)
    if log_w is not None: open(os.path.join(w, "tiempos.log"), "w").write(log_w)
    return w
NEW = "2026-11-13 09:00 | 1 inicio rev21\n2026-11-13 09:30 | 1 fin\n2026-11-13 10:00 | 4 fin\n"
NEWX = "2026-11-13 09:00 | 1 inicio\n2026-11-13 09:30 | 1 fin\n2026-11-13 10:00 | 4 fin\n"
def show(k, w):
    e, m = CE.proceso_v119(w, None, TT, 5); print(k, "->", e, "|", (m[0] if m else "")[:150])
show("Z0 control own log rev21 13-nov", mk(log_w=NEW))
# Z1: cumulative project log; the closing line of the PREVIOUS rev (before v119) mentions the next rev label
show("Z1 cumulative log, rev20 closing line '05-nov ... rev20 entregada; sigue rev21 (RFI-30)' + rev21 13-nov",
     mk(log_parent="05-nov 11:26 PST | 0 Arranque rev20 | inicio\n05-nov 19:42 PST | rev20 entregada; sigue rev21 cuando conteste RFI-30\n" + NEW))
# Z2: own rev log (not cumulative), first line copied header WITHOUT a rev label (10-nov), then the real 13-nov marks
show("Z2 own log, one copied header line without rev label '10-nov 21:01 PST | arranque proyecto'",
     mk(log_w="10-nov 21:01 PST | arranque proyecto\n" + NEWX))
# Z3: own log, first line is an ISO line from 2026-11-11 (planning note), real work 13-nov
show("Z3 own log, first line '2026-11-11 18:00 | nota: plan de la rev' then 13-nov", mk(log_w="2026-11-11 18:00 | nota: plan de la rev\n" + NEWX))
# Z4: own log with rev label written on an OLD line (typo in the date 2026-11-03 instead of 2026-11-13)
show("Z4 own log, 'inicio rev21' with mistyped date 2026-11-03 then 13-nov marks",
     mk(log_w="2026-11-03 09:00 | 1 inicio rev21\n2026-11-13 09:30 | 1 fin\n2026-11-13 10:00 | 4 fin\n"))
