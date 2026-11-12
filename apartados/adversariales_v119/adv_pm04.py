import sys,os,json,tempfile,shutil; sys.path.insert(0,sys.argv[1]); import verificar_version as V
cand=sys.argv[2]; F=V.Fuente(cand); sha=V.sha_tools(F)
sys.path.insert(0,os.path.join(cand,"tools")); import compuerta_entrega as CE
print("sha V == sha CE:", sha==CE.sha_tools(os.path.join(cand,"tools")) if 'tools_dir' in CE.sha_tools.__code__.co_varnames else CE.sha_tools()==sha, sha[:12])
def cache_with(files):
    c=tempfile.mkdtemp(); d=c+"/proj"; os.makedirs(d)
    for n,v in files.items():
        p=os.path.join(d,n); os.makedirs(os.path.dirname(p),exist_ok=True)
        open(p,"w").write(json.dumps(v) if isinstance(v,dict) else v)
    return c
csv="- comparar_csv_bluebeam.py: 10 CSV / 10 PDF / 10 emparejados; 0 faltantes en cada lado.\n"
c=cache_with({"SUBIDA_OK_rev1.json":{"fecha_iso":"2026-11-11T10:00:00+00:00"},"CSV_BLUEBEAM_rev1/RESULTADO.md":csv})
print("P4-0 rev1 + CSV rev1 N/N -> closed:", V.proyectos_abiertos_cache(c))
c=cache_with({"SUBIDA_OK_rev1.json":{"fecha_iso":"2026-11-11T10:00:00+00:00"},"CSV_BLUEBEAM_rev1/RESULTADO.md":csv,"SUBIDA_OK_rev2.json":{"fecha_iso":"2026-11-12T10:00:00+00:00"}})
print("P4a newer SUBIDA_OK_rev2 -> open?", V.proyectos_abiertos_cache(c))
c=cache_with({"SUBIDA_OK_rev1.json":{"fecha_iso":"2026-11-11T10:00:00+00:00"},"CSV_BLUEBEAM_rev1/RESULTADO.md":csv,"SUBIDA_OK.json":{"fecha_iso":"2026-11-12T10:00:00+00:00"}})
print("P4b newer SUBIDA_OK.json (sin rev) -> open?", V.proyectos_abiertos_cache(c))
c=cache_with({"SUBIDA_OK_rev1.json":{"fecha_iso":"2026-11-11T10:00:00+00:00"},"CSV_BLUEBEAM_rev1/RESULTADO.md":csv,"VERSION_PROYECTO.txt":"2026-11-12T10:00:00+00:00 | rev2 | v81cf118 | \n"})
print("P4c newer VERSION_PROYECTO rev2 (sin subida) -> open?", V.proyectos_abiertos_cache(c))
c=cache_with({"SUBIDA_OK_rev2.json":{"fecha_iso":"2026-11-12T10:00:00+00:00"},"CSV_BLUEBEAM_rev2/RESULTADO.md":"10 CSV / 10 PDF / 10 emparejados; 0 faltantes; 3 faltantes en PDF\n"})
print("P4d RESULTADO con '0 faltantes' y '3 faltantes' -> closed?", V.proyectos_abiertos_cache(c))
c=cache_with({"SUBIDA_OK.json":{"fecha_iso":"2026-11-12T10:00:00+00:00"},"CSV_BLUEBEAM_rev0/RESULTADO.md":csv})
print("P4e SUBIDA_OK.json + CSV de cualquier rev -> closed:", V.proyectos_abiertos_cache(c))
# PRUEBA
a=tempfile.mkdtemp()
def pr(proy, top=None, abiertos=None, cache=None):
    json.dump({"proyectos": abiertos or list(proy)}, open(a+"/PROYECTOS_ABIERTOS.json","w"))
    json.dump(dict({"version_candidata":"v81cf119","ok":True,"regresiones":[],"proyectos":proy}, **(top or {})), open(a+"/PRUEBA_ABIERTOS_v81cf119.json","w"))
    return V.revisar_prueba_abiertos(a, F, cache=cache)
print("P0 ok:", pr({"xf":{"sha_tools":sha,"regresiones":0}}))
print("P2 stale sha:", pr({"xf":{"sha_tools":"0"*64}}))
print("P2b sin sha_tools:", pr({"xf":{}}))
print("P3 entry regresiones=5 sin_explicar=5, top-level vacío ok=true:", pr({"xf":{"sha_tools":sha,"regresiones":5,"sin_explicar":5}}))
print("P3b candidata FAIL 12 vs vigente FAIL 0, top empty:", pr({"xf":{"sha_tools":sha,"vigente":{"FAIL":0},"candidata":{"FAIL":12},"regresiones":0}}))
print("P5 version_candidata missing (None):", pr({"xf":{"sha_tools":sha}}, top={"version_candidata":None}))
print("P6 lista con nombre que no existe en cache, PRUEBA lo trae:", pr({"zz_fake":{"sha_tools":sha}}))
c=cache_with({"SUBIDA_OK.json":{"fecha_iso":"2026-11-12T10:00:00+00:00"}})
print("P7 cache con proyecto abierto no listado:", pr({"xf":{"sha_tools":sha}}, cache=c))
print("P8 sin cache arg (main sin extra) -> detector off:", V.proyectos_abiertos_cache(None))
