import sys,os; sys.path.insert(0,sys.argv[1]); import compuerta_entrega as CE
def tab(rows, head="| Paso | Inicio | Fin | Duración |"):
    return head+"\n|---|---|---|---|\n"+"".join(rows)
base=lambda c1,c2,c3:[f"| {c1} | 11-13 09:00 | 11-13 09:30 | 30 min |\n",f"| {c2} | 11-13 09:30 | 11-13 10:00 | 30 min |\n",f"| {c3} | 11-13 10:00 | 11-13 10:20 | 20 min |\n"]
cases={"M0 control '1','2-3','4'":tab(base("1","2-3","4")),
 "M1 'Paso 1','Paso 2-3','Paso 4'":tab(base("Paso 1","Paso 2-3","Paso 4")),
 "M2 '1. Inventario','2-3. Lecturas A/B','4. Comparación'":tab(base("1. Inventario","2-3. Lecturas A/B","4. Comparación")),
 "M3 '1 Inventario','2-3 Lecturas A/B','4 Comparación'":tab(base("1 Inventario","2-3 Lecturas A/B","4 Comparación")),
 "M4 'Step 1','Steps 2-3','Step 4' (English)":tab(base("Step 1","Steps 2-3","Step 4"),"| Step | Start | End | Duration |"),
}
for k,t in cases.items():
    print(k,"-> pasos exigidos:",CE.pasos_cerrados_tiempos(t),"| CE_TIEMPOS fallas:",CE.tiempos_fallas(t))
import tempfile
LOG="2026-11-13 09:00 | 1 inicio\n2026-11-13 09:30 | 1 fin\n2026-11-13 10:00 | 2-3 fin\n2026-11-13 10:20 | 4 fin\n"
print("---- full alarma_fallas (tiempos.log cuadra, NO --paso runs in compuerta_corridas.jsonl):")
for k,t in cases.items():
    t=t+"| TOTAL | | | 80 min |\n"
    w=tempfile.mkdtemp(dir=os.environ.get("ADVTMP")); open(os.path.join(w,"tiempos.log"),"w").write(LOG)
    ev=CE.alarma_fallas(w,5,registro=[],tiempos_txt=t)
    print(k,"-> CE_TIEMPOS:",CE.tiempos_fallas(t),"| alarma_fallas:",[x[:70] for x in ev])
LOG2="2026-11-13 09:00 | inicio inventario\n2026-11-13 09:30 | inventario cerrado\n2026-11-13 10:00 | lecturas A/B cerradas\n2026-11-13 10:20 | comparación cerrada\n"
print("---- log WITHOUT 'N fin' text (E3 style) + step labels with words:")
for k,t in cases.items():
    t=t+"| TOTAL | | | 80 min |\n"
    w=tempfile.mkdtemp(dir=os.environ.get("ADVTMP")); open(os.path.join(w,"tiempos.log"),"w").write(LOG2)
    print(k,"-> CE_TIEMPOS:",CE.tiempos_fallas(t),"| alarma_fallas:",[x[:70] for x in CE.alarma_fallas(w,5,registro=[],tiempos_txt=t)])
