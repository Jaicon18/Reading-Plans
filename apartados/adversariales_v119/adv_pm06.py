import sys,os,tempfile; sys.path.insert(0,sys.argv[1]); import compuerta_entrega as CE
w=tempfile.mkdtemp(); print("A sin tiempos.log:", CE.alarma_fallas(w,5,[]))
open(w+"/tiempos.log","w").write("2026-01-05 10:00 | inicio\n")
print("B 1 marca:", CE.alarma_fallas(w,5,[]))
open(w+"/tiempos.log","w").write("2026-01-05 10:00 | paso 1 start\n2026-01-05 12:00 | paso 4 done\n2026-01-05 18:00 | entregado\n")
print("C 8h sin 'N fin' ni alertas:", CE.alarma_fallas(w,5,[]))
