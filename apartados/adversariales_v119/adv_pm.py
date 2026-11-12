import sys, os, json, tempfile
sys.path.insert(0, sys.argv[1]); import verificar_version as V
cab = "| id | error / regla | chequeo | test | estado |\n|---|---|---|---|---|\n"
def base():
    c = tempfile.mkdtemp(); os.makedirs(c+"/p")
    json.dump({"fecha_iso": "2026-11-12T20:00:00+00:00"}, open(c+"/p/SUBIDA_OK.json","w")); return c
# A1: principal sin tabla
c=base(); open(c+"/POSTMORTEM_COBERTURA_2026-11-12b.md","w").write("# 2026-11-12 16:00 PT\nnada\n")
print("A1 principal sin tabla:", V.revisar_postmortem(c))
# A2: principal falso nuevo 12c con tabla de 1 OK, mientras 12b tiene 7 WEAK
c=base(); open(c+"/POSTMORTEM_COBERTURA_2026-11-12b.md","w").write("# 2026-11-12 16:00 PT\n"+cab+"".join(f"| W{k} | z | n | - | WEAK |\n" for k in range(7)))
open(c+"/POSTMORTEM_COBERTURA_2026-11-12c.md","w").write("# 2026-11-12 17:00 PT\n"+cab+"| X | x | x | x | OK |\n")
print("A2 principal nuevo 1 OK tapa 12b:", V.revisar_postmortem(c))
# A3: principal limpio + VERIF con WEAK + VERIF3 mas nueva sin tabla
c=base(); open(c+"/POSTMORTEM_COBERTURA_2026-11-12b.md","w").write("# 2026-11-12 16:00 PT\n"+cab+"| Q1 | x | x | x | OK |\n")
open(c+"/POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION.md","w").write("# 2026-11-12 17:00 PT\n"+cab+"| Q1 | x | x | x | WEAK — STILL-WEAK |\n| Q9 | x | x | x | WEAK — STILL-WEAK |\n")
print("A3a con verif WEAK:", V.revisar_postmortem(c))
open(c+"/POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION3.md","w").write("# 2026-11-12 18:00 PT\nsin tabla, todo bien\n")
print("A3b + verif nueva SIN tabla:", V.revisar_postmortem(c))
# A4: verif nueva con tabla que omite Q9 (solo Q1 OK)
os.remove(c+"/POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION3.md")
open(c+"/POSTMORTEM_COBERTURA_2026-11-12b_VERIFICACION3.md","w").write("# 2026-11-12 18:00 PT\n"+cab+"| Q1 | x | x | x | OK — CONFIRMED-CLOSED |\n")
print("A4 verif nueva omite Q9:", V.revisar_postmortem(c))
# A5: estado vacio / 'pendiente'
c=base(); open(c+"/POSTMORTEM_COBERTURA_2026-11-12b.md","w").write("# 2026-11-12 16:00 PT\n"+cab+"| Q1 | x | x | x |  |\n| Q2 | x | x | x | OKAY-ish |\n")
print("A5 estado vacio/OKAY:", V.revisar_postmortem(c))
# prueba abiertos: lista vacia
a=tempfile.mkdtemp(); d=tempfile.mkdtemp(); open(d+"/SKILL.md","w").write("**VERSION: v81cf119**\n")
json.dump({"proyectos": []}, open(a+"/PROYECTOS_ABIERTOS.json","w"))
json.dump({"version_candidata":"v81cf119","ok":True,"regresiones":[],"proyectos":{}}, open(a+"/PRUEBA_ABIERTOS_v81cf119.json","w"))
print("B1 lista abiertos vacia:", V.revisar_prueba_abiertos(a, V.Fuente(d)))
json.dump({"proyectos": ["xf","gk"]}, open(a+"/PROYECTOS_ABIERTOS.json","w"))
json.dump({"version_candidata":"v81cf119","ok":True,"regresiones":[],"proyectos":{"xf":{},"gk":{"regresiones":5}}}, open(a+"/PRUEBA_ABIERTOS_v81cf119.json","w"))
print("B2 proyecto con regresiones=5 en su entrada pero top-level vacio:", V.revisar_prueba_abiertos(a, V.Fuente(d)))
