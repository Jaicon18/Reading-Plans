import sys,os,tempfile; sys.path.insert(0,sys.argv[1]); import compuerta_entrega as CE
T=os.environ.get("ADVTMP")
log="2026-01-05 10:00 | inicio\n2026-01-05 10:20 | inventario listo\n2026-01-05 10:50 | lecturas listas\n2026-01-05 11:10 | canon\n"
def tt(rows, hdr="| # | Paso | Inicio | Fin | Duración | Evidencia |\n|---|---|---|---|---|---|\n"):
    return "# T PST\n"+hdr+"".join(rows)+"| TOTAL | x | | | 70 min | |\n"
def run(t, reg=None):
    w=tempfile.mkdtemp(dir=T); open(w+"/tiempos.log","w").write(log)
    ev=CE.alarma_fallas(w,5,reg or [],tiempos_txt=t)
    p=CE._pasos_tiempos(t); return [x for x in ev if "--paso" in x], sorted(k for k in p if p[k])
std=["| 1 | inv | 01-05 10:00 PST | 01-05 10:20 PST | 20 min | e |\n","| 2-3 | lect | 01-05 10:20 PST | 01-05 10:50 PST | 30 min | e |\n","| 4 | canon | 01-05 10:50 PST | 01-05 11:10 PST | 20 min | e |\n"]
print("F0 control (std table, no --paso runs):", run(tt(std)))
en=[r.replace("| 2-3 |","| 2–3 |") for r in std]
print("F1 en-dash '2–3' step:", run(tt(en)))
bold=[r.replace("| 4 |","| **4** |").replace("| 1 |","| **1** |") for r in std]
print("F2 bold '**1**' / '**4**':", run(tt(bold)))
suf=[r.replace("| 4 |","| 4a |") for r in std]
print("F3 '4a' step:", run(tt(suf)))
three=["| 1 | 01-05 10:00 PST | 01-05 10:20 PST |\n","| 2-3 | 01-05 10:20 PST | 01-05 10:50 PST |\n","| 4 | 01-05 10:50 PST | 01-05 11:10 PST |\n"]
print("F4 3-column table (Paso|Inicio|Fin):", run(tt(three, "| Paso | Inicio | Fin |\n|---|---|---|\n")))
reord=["| 1 | 01-05 10:00 PST | 01-05 10:20 PST | 20 min | inv |\n","| 2-3 | 01-05 10:20 PST | 01-05 10:50 PST | 30 min | lect |\n","| 4 | 01-05 10:50 PST | 01-05 11:10 PST | 20 min | canon |\n"]
print("F5 cols Paso|Inicio|Fin|Duración|Desc:", run(tt(reord, "| # | Inicio | Fin | Duración | Paso |\n|---|---|---|---|---|\n")))
print("F6 wrong step numbers logged ('--paso 9' for everything):", run(tt(std), [{"evento":"fin","paso":"9"}]*3))
print("F7 run logged as paso '1-9' covers 4?:", run(tt(std), [{"evento":"fin","paso":"1-9"}]))
print("F8 runs 1, 2-3, 4 logged correctly:", run(tt(std), [{"evento":"fin","paso":"1"},{"evento":"fin","paso":"2-3"},{"evento":"fin","paso":"4"}]))
for nm,t in (("F1",tt(en)),("F2",tt(bold)),("F3",tt(suf)),("F4",tt(three,"| Paso | Inicio | Fin |\n|---|---|---|\n"))):
    print(nm,"CE_TIEMPOS tiempos_fallas:", CE.tiempos_fallas(t), "| tiempos_cuadran:", CE.tiempos_cuadran_fallas(t, []))
