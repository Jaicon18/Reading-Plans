import sys,os,tempfile; sys.path.insert(0,sys.argv[1]); import compuerta_entrega as CE
T=os.environ.get("ADVTMP")
TT="| Paso | Inicio | Fin | Duración |\n|---|---|---|---|\n| 1 | 11-13 09:00 | 11-13 09:30 | 30 min |\n| 4 | 11-13 09:30 | 11-13 10:00 | 30 min |\n"
def mk(log_parent=None, log_w=None):
    p=tempfile.mkdtemp(dir=T); w=os.path.join(p,"rev21"); os.makedirs(w)
    if log_parent is not None: open(os.path.join(p,"tiempos.log"),"w").write(log_parent)
    if log_w is not None: open(os.path.join(w,"tiempos.log"),"w").write(log_w)
    return w
OLD="05-nov 11:26 PST | 0 Arranque | inicio\n05-nov 19:42 PST | 4-6 | fin\n"
NEW="2026-11-13 09:00 | 1 inicio rev21\n2026-11-13 09:30 | 1 fin\n2026-11-13 10:00 | 4 fin\n"
# P0 control: rev21 own log, started 13-nov -> FAIL
w=mk(log_w=NEW); print("P0 rev21 own log 13-nov ->", CE.proceso_v119(w,None,TT,5)[0])
# P1 realistic: project-wide cumulative tiempos.log in the project folder (CR / XF layout) with old 05-nov lines, rev21 appended 13-nov
w=mk(log_parent=OLD+NEW); e,m=CE.proceso_v119(w,None,TT,5); print("P1 cumulative project log (05-nov ... 13-nov), rev21 started 13-nov ->", e, "|", m[0][:120])
# P1b same but all in old format: '13-nov 09:00 PST'
NEWO="13-nov 09:00 PST | 1 inicio rev21\n13-nov 09:30 PST | 1 fin\n13-nov 10:00 PST | 4 fin\n"
w=mk(log_parent=OLD+NEWO); print("P1b cumulative old-format log, rev21 13-nov ->", CE.proceso_v119(w,None,TT,5)[0])
# P2 old-format only, rev started 12-nov 14:30 PST (after FECHA_V119 11:00 PST) -> FAIL
w=mk(log_w="12-nov 14:30 PST | 1 inicio\n12-nov 15:00 PST | 1 fin\n"); print("P2 old format 12-nov 14:30 PST (after v119) ->", CE.proceso_v119(w,None,TT,5)[0])
# P3 old format with a stray earlier line copied from the previous rev's header (realistic copy/paste of log header)
w=mk(log_w="10-nov 21:01 PST | (copiado de rev3) arranque proyecto\n2026-11-13 09:00 | 1 inicio\n2026-11-13 09:30 | 1 fin\n"); print("P3 rev log with one copied old header line ->", CE.proceso_v119(w,None,TT,5)[0])
# P4 no log, scratch workdir outside git -> FAIL
w=mk(); print("P4 no log, no git ->", CE.proceso_v119(w,None,TT,5)[0])
# P5 typo date in log first line '2025-11-13 09:00' (wrong year) -> AMBER?
w=mk(log_w="2025-11-13 09:00 | 1 inicio\n2026-11-13 09:30 | 1 fin\n"); print("P5 year typo 2025 on first line ->", CE.proceso_v119(w,None,TT,5)[0])
