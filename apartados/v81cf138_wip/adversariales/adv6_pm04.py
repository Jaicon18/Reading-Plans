import sys, os, json, tempfile; sys.path.insert(0, sys.argv[1]); import verificar_version as V
T = "/tmp/v138wip/tmp"; os.makedirs(T, exist_ok=True)
def mk(files):
    c = tempfile.mkdtemp(dir=T)
    for rel, tx in files.items():
        p = os.path.join(c, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w").write(tx if isinstance(tx, str) else json.dumps(tx))
    return c
SUB = {"fecha_iso": "2026-11-12T18:00:00+00:00"}
OK = "# R\nComparado: 2026-11-12 12:00 PT\n- 1351 CSV / 1351 PDF / 1351 emparejados; 0 faltantes en cada lado.\n"
c = mk({"proj/SUBIDA_OK_rev20.json": SUB, "proj/CSV_BLUEBEAM_rev20/RESULTADO.md": OK})
print("W0 control (rev20 subida + CSV rev20 N/N) -> abiertos:", V.proyectos_abiertos_cache(c))
# W1: project in progress (first rev, nothing uploaded yet) -> never listed as open
c = mk({"nuevo_proj/TIEMPOS.md": "| Paso | Inicio |\n|---|---|\n| 1 | 2026-11-13 08:00 PT |\n",
        "nuevo_proj/canon/takeoff_canon.json": {"walls": [{"id": "A-1"}]}, "nuevo_proj/tiempos.log": "2026-11-13T08:00:00-08:00 | rev1 inicio\n"})
print("W1 project with canon + TIEMPOS, no SUBIDA_OK yet -> abiertos:", V.proyectos_abiertos_cache(c), "| _es_proyecto:", V._es_proyecto(os.path.join(c, "nuevo_proj")))
# W2: mismatch words not in RX_FALTAN_N
for extra in ("- 12 markups no emparejados en el PDF", "- 12 huérfanos en el PDF", "- 12 sin emparejar", "- 12 extra markups in PDF",
              "- 12 duplicados", "- diferencias: 12", "- 12 not matched"):
    c = mk({"proj/SUBIDA_OK_rev20.json": SUB, "proj/CSV_BLUEBEAM_rev20/RESULTADO.md": OK + extra + "\n"})
    print("W2", repr(extra), "-> cuadra:", V.csv_cuadra(OK + extra), "| abiertos:", V.proyectos_abiertos_cache(c))
# W3: newer rev in progress detected only through VERSION_PROYECTO.txt in the CACHE project folder; real VERSION_PROYECTO lives in the workdir
c = mk({"proj/SUBIDA_OK_rev20.json": SUB, "proj/CSV_BLUEBEAM_rev20/RESULTADO.md": OK,
        "proj/rev21_work/VERSION_PROYECTO.txt": "2026-11-13T15:00:00+00:00 | rev21 | v81cf137 | \n"})
print("W3 rev21 started (VERSION_PROYECTO.txt in a rev subfolder) after rev20 closed -> abiertos:", V.proyectos_abiertos_cache(c))
# W4: real cache (read only): which projects does the detector see?
e = []; print("W4 real cache abiertos:", V.proyectos_abiertos_cache("/home/user/Reading-Plans/cache_proyectos", e), e)
