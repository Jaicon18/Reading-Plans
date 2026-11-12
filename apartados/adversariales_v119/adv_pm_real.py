import sys,os; sys.path.insert(0,sys.argv[1]); import verificar_version as V
c=sys.argv[2]
print("real:", len(V.revisar_postmortem(c)))
open(c+"/POSTMORTEM_COBERTURA_2026-11-12c.md","w").write("# 2026-11-12 23:00 PT\n| id | error / regla | chequeo | test | estado |\n|---|---|---|---|---|\n| X | x | x | x | OK |\n")
print("C1 principal 12c 1 row OK sobre 12b con 6 abiertos:", V.revisar_postmortem(c))
os.remove(c+"/POSTMORTEM_COBERTURA_2026-11-12c.md")
# verificación que cierra con id distinto (sin NG) — p.ej. 'BE-PM04' solo
open(c+"/POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION3.md","w").write("# 2026-11-12 23:00 PT\n| id | error / regla | chequeo | test | estado |\n|---|---|---|---|---|\n| BE-PM04 | x | x | x | OK — CONFIRMED-CLOSED |\n| U-185 | x | x | x | OK — CONFIRMED-CLOSED |\n")
print("C2 verif3 cierra 'BE-PM04' (id distinto) + U-185:", V.revisar_postmortem(c))
# verif3 con hora ANTERIOR a verif2 pero nombre posterior
open(c+"/POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION3.md","w").write("# 2026-11-12 08:00 PT\n| id | error / regla | chequeo | test | estado |\n|---|---|---|---|---|\n"+"".join(f"| {i} | x | x | x | OK — CONFIRMED-CLOSED |\n" for i in ["U-185","NG-3.1 / BE-PM04","NG-3.3 / BE-PM06","U-193"]))
print("C3 verif3 hora 08:00 (antes de verif2) cierra todo:", V.revisar_postmortem(c))
# verif3 'OK — CONFIRMED-CLOSED' escrito dentro de 'NOT CONFIRMED-CLOSED'
open(c+"/POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION3.md","w").write("# 2026-11-12 23:00 PT\n| id | error / regla | chequeo | test | estado |\n|---|---|---|---|---|\n"+"".join(f"| {i} | x | x | x | WEAK — NOT CONFIRMED-CLOSED |\n" for i in ["U-185","NG-3.1 / BE-PM04","NG-3.3 / BE-PM06","U-193"]))
print("C4 'WEAK — NOT CONFIRMED-CLOSED':", V.revisar_postmortem(c))
os.remove(c+"/POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION3.md")
