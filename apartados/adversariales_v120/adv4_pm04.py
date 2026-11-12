import sys,os,json,tempfile; sys.path.insert(0,sys.argv[1]); import verificar_version as V
cand=sys.argv[2]; F=V.Fuente(cand); sha=V.sha_tools(F); T=os.environ.get("ADVTMP")
def cache_with(files, name="proj", c=None):
    c=c or tempfile.mkdtemp(dir=T); d=c+"/"+name; os.makedirs(d,exist_ok=True)
    for n,v in files.items():
        p=os.path.join(d,n); os.makedirs(os.path.dirname(p),exist_ok=True)
        open(p,"w").write(json.dumps(v) if isinstance(v,dict) else v)
    return c
csv="2026-11-12 12:00 PT\n- 10 CSV / 10 PDF / 10 emparejados; 0 faltantes en cada lado.\n"
sub=lambda t:{"fecha_iso":t}
print("Q0 control: subida 10:00Z, CSV 12:00 PT after -> closed:", V.proyectos_abiertos_cache(cache_with({"SUBIDA_OK.json":sub("2026-11-12T10:00:00+00:00"),"CSV_BLUEBEAM_rev1/RESULTADO.md":csv})))
print("Q1 SUBIDA_OK dated BEFORE CSV but a newer SUBIDA_OK_rev2 w/o fecha_iso (key 'fecha') -> open?", V.proyectos_abiertos_cache(cache_with({"SUBIDA_OK.json":sub("2026-11-12T10:00:00+00:00"),"CSV_BLUEBEAM_rev1/RESULTADO.md":csv,"SUBIDA_OK_rev2.json":{"fecha":"2026-11-12T23:00:00+00:00"}})))
print("Q2 CSV RESULTADO 0 CSV / 0 PDF / 0 emparejados (vacuous) -> open?", V.proyectos_abiertos_cache(cache_with({"SUBIDA_OK.json":sub("2026-11-12T10:00:00+00:00"),"CSV_BLUEBEAM_rev1/RESULTADO.md":"2026-11-12 12:00 PT\n0 CSV / 0 PDF / 0 emparejados; 0 faltantes\n"})))
print("Q3 RESULTADO compared 09:00 PT (before subida 2026-11-12 20:00Z) but first date cited is a later bid date -> open?", V.proyectos_abiertos_cache(cache_with({"SUBIDA_OK.json":sub("2026-11-12T20:00:00+00:00"),"CSV_BLUEBEAM_rev1/RESULTADO.md":"Bid due 2026-11-20 14:00\nCompared 2026-11-12 09:00 PT\n10 CSV / 10 PDF / 10 emparejados; 0 faltantes\n"})))
try:
    r=V.proyectos_abiertos_cache(cache_with({"SUBIDA_OK.json":sub("2026-11-12T20:00:00"),"CSV_BLUEBEAM_rev1/RESULTADO.md":csv})); print("Q4 naive fecha_iso:", r)
except Exception as e: print("Q4 naive fecha_iso -> crash (fails loud):", type(e).__name__)
# PRUEBA fabricada a mano: entry only sha + ok
a=tempfile.mkdtemp(dir=T); c=cache_with({"SUBIDA_OK.json":sub("2026-11-12T10:00:00+00:00")},name="xf")
json.dump({"proyectos":["xf"]},open(a+"/PROYECTOS_ABIERTOS.json","w"))
json.dump({"version_candidata":"v81cf120","ok":True,"regresiones":[],"proyectos":{"xf":{"sha_tools":sha}}},open(a+"/PRUEBA_ABIERTOS_v81cf120.json","w"))
print("Q5 hand-made PRUEBA (only sha_tools, no vigente/candidata counts) -> fallas:", V.revisar_prueba_abiertos(a,F,cache=c))
json.dump({"version_candidata":"v81cf120","ok":True,"regresiones":[],"proyectos":{"xf":{"sha_tools":sha,"vigente":{"FAIL":0,"PASS":0},"candidata":{"FAIL":0,"PASS":0}}}},open(a+"/PRUEBA_ABIERTOS_v81cf120.json","w"))
print("Q5b PRUEBA with 0 PASS / 0 FAIL (no checks run) -> fallas:", V.revisar_prueba_abiertos(a,F,cache=c))
# fake name existing as a non-project dir, real open project omitted
c2=cache_with({"SUBIDA_OK.json":sub("2026-11-12T10:00:00+00:00")},name="xf"); os.makedirs(c2+"/herramientas")
json.dump({"proyectos":["herramientas"]},open(a+"/PROYECTOS_ABIERTOS.json","w"))
json.dump({"version_candidata":"v81cf120","ok":True,"regresiones":[],"proyectos":{"herramientas":{"sha_tools":sha}}},open(a+"/PRUEBA_ABIERTOS_v81cf120.json","w"))
print("Q6 list names existing non-project dir 'herramientas', omits xf -> fallas:", V.revisar_prueba_abiertos(a,F,cache=c2))
json.dump({"proyectos":["xf","herramientas"]},open(a+"/PROYECTOS_ABIERTOS.json","w"))
json.dump({"version_candidata":"v81cf120","ok":True,"regresiones":[],"proyectos":{"xf":{"sha_tools":sha,"vigente":{"FAIL":3},"candidata":{"FAIL":3}},"herramientas":{"sha_tools":sha}}},open(a+"/PRUEBA_ABIERTOS_v81cf120.json","w"))
print("Q6b list xf + fake 'herramientas' -> fallas:", V.revisar_prueba_abiertos(a,F,cache=c2))
print("Q7 P4b/P4c re-run: SUBIDA_OK.json newer than CSV -> open:", V.proyectos_abiertos_cache(cache_with({"SUBIDA_OK_rev1.json":sub("2026-11-11T10:00:00+00:00"),"CSV_BLUEBEAM_rev1/RESULTADO.md":"2026-11-11 12:00 PT\n10 CSV / 10 PDF / 10 emparejados; 0 faltantes\n","SUBIDA_OK.json":sub("2026-11-12T10:00:00+00:00")})),
  "| VERSION_PROYECTO newer:", V.proyectos_abiertos_cache(cache_with({"SUBIDA_OK_rev1.json":sub("2026-11-11T10:00:00+00:00"),"CSV_BLUEBEAM_rev1/RESULTADO.md":"2026-11-11 12:00 PT\n10 CSV / 10 PDF / 10 emparejados; 0 faltantes\n","VERSION_PROYECTO.txt":"2026-11-12T10:00:00+00:00 | rev2\n"})),
  "| RESULTADO sin fecha:", V.proyectos_abiertos_cache(cache_with({"SUBIDA_OK.json":sub("2026-11-11T10:00:00+00:00"),"CSV_BLUEBEAM_rev1/RESULTADO.md":"10 CSV / 10 PDF / 10 emparejados; 0 faltantes\n"})),
  "| 0 + 3 faltantes:", V.proyectos_abiertos_cache(cache_with({"SUBIDA_OK.json":sub("2026-11-11T10:00:00+00:00"),"CSV_BLUEBEAM_rev1/RESULTADO.md":"2026-11-11 12:00 PT\n10 CSV / 10 PDF / 10 emparejados; 0 faltantes; 3 faltantes\n"})))
a2=tempfile.mkdtemp(dir=T); json.dump({"proyectos":["xf"]},open(a2+"/PROYECTOS_ABIERTOS.json","w"))
print("Q8 no cache arg and no sibling cache -> fallas:", V.revisar_prueba_abiertos(a2,F))
json.dump({"version_candidata":"v81cf120","ok":True,"regresiones":[],"proyectos":{"xf":{"sha_tools":sha,"regresiones":5,"sin_explicar":5}}},open(a+"/PRUEBA_ABIERTOS_v81cf120.json","w")); json.dump({"proyectos":["xf"]},open(a+"/PROYECTOS_ABIERTOS.json","w"))
print("Q9 P3 entry regresiones 5 sin explicar 5:", V.revisar_prueba_abiertos(a,F,cache=c))
