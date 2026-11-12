import sys,os,json,tempfile; sys.path.insert(0,sys.argv[1]); import verificar_version as V
T=os.environ.get("ADVTMP")
def mk(subs, res=None, vp=None, sub_dir=""):
    c=tempfile.mkdtemp(dir=T); d=os.path.join(c,"proj",sub_dir); os.makedirs(d)
    for n,f in subs.items(): json.dump(f,open(os.path.join(d,n),"w"))
    for rd,tx in (res or {}).items():
        os.makedirs(os.path.join(c,"proj",rd)); open(os.path.join(c,"proj",rd,"RESULTADO.md"),"w").write(tx)
    if vp: open(os.path.join(c,"proj","VERSION_PROYECTO.txt"),"w").write(vp)
    return c
OKR=lambda t:f"# R\nComparado: {t}\n- 1351 CSV / 1351 PDF / 1351 emparejados; 0 faltantes en cada lado.\n"
# R0 control
c=mk({"SUBIDA_OK_rev20.json":{"fecha_iso":"2026-11-12T18:00:00+00:00"}},{"CSV_BLUEBEAM_rev20":OKR("2026-11-12 12:00 PT")})
print("R0 control rev20 CSV after rev20 upload -> closed:",V.proyectos_abiertos_cache(c))
# R1 stale CSV dir of an OLDER rev (rev19) re-compared after rev20 upload (same counts) -> should be open
c=mk({"SUBIDA_OK_rev19.json":{"fecha_iso":"2026-11-11T18:00:00+00:00"},"SUBIDA_OK_rev20.json":{"fecha_iso":"2026-11-12T18:00:00+00:00"}},{"CSV_BLUEBEAM_rev19":OKR("2026-11-12 12:00 PT")})
print("R1 CSV_BLUEBEAM_rev19 re-run after rev20 upload -> open?",V.proyectos_abiertos_cache(c))
# R2 SUBIDA_OK kept in a rev subfolder (O'Reilly layout REV10_FINAL/SUBIDA_OK.json), no CSV -> open?
c=mk({"SUBIDA_OK.json":{"fecha_iso":"2026-11-12T18:00:00+00:00"}},sub_dir="REV3_FINAL")
e=[]; print("R2 SUBIDA_OK only in rev subfolder -> open?",V.proyectos_abiertos_cache(c,e),e, "| _es_proyecto:",V._es_proyecto(os.path.join(c,"proj")))
# R3 thousands separator '1,351 CSV / 1,351 PDF / 1,350 emparejados' (1 missing) -> open?
c=mk({"SUBIDA_OK.json":{"fecha_iso":"2026-11-12T18:00:00+00:00"}},{"CSV_BLUEBEAM_rev1":"Comparado: 2026-11-12 12:00 PT\n1,351 CSV / 1,351 PDF / 1,350 emparejados; 0 faltantes\n"})
print("R3 '1,351/1,351/1,350' -> open?",V.proyectos_abiertos_cache(c))
# R4 'Comparado' in prose header (date with ~ and AM) like the real CR file -> treated open (conservative)
c=mk({"SUBIDA_OK.json":{"fecha_iso":"2026-11-12T18:00:00+00:00"}},{"CSV_BLUEBEAM_rev1":"- Fecha: 12-nov-2026 ~10:45 AM PT\n1351 CSV / 1351 PDF / 1351 emparejados; 0 faltantes\n"})
print("R4 prose date only -> open:",V.proyectos_abiertos_cache(c))
# R5 'Comparado:' line present but the counts line says 'faltantes: 3' (colon form) -> open?
c=mk({"SUBIDA_OK.json":{"fecha_iso":"2026-11-12T18:00:00+00:00"}},{"CSV_BLUEBEAM_rev1":"Comparado: 2026-11-12 12:00 PT\n1351 CSV / 1351 PDF / 1351 emparejados; 0 faltantes en el PDF; faltantes en el CSV: 3\n"})
print("R5 'faltantes en el CSV: 3' -> open?",V.proyectos_abiertos_cache(c))
FIRST=lambda t:f"Comparado: {t}\n# R\n- 1351 CSV / 1351 PDF / 1351 emparejados; 0 faltantes en cada lado.\n"
c=mk({"SUBIDA_OK_rev20.json":{"fecha_iso":"2026-11-12T18:00:00+00:00"}},{"CSV_BLUEBEAM_rev20":FIRST("2026-11-12 12:00 PT")})
print("R0b control with 'Comparado:' as FIRST line -> closed:",V.proyectos_abiertos_cache(c))
c=mk({"SUBIDA_OK_rev19.json":{"fecha_iso":"2026-11-11T18:00:00+00:00"},"SUBIDA_OK_rev20.json":{"fecha_iso":"2026-11-12T18:00:00+00:00"}},{"CSV_BLUEBEAM_rev19":FIRST("2026-11-12 12:00 PT")})
print("R1b stale CSV_BLUEBEAM_rev19 (Comparado first) after rev20 upload -> open?",V.proyectos_abiertos_cache(c))
c=mk({"SUBIDA_OK.json":{"fecha_iso":"2026-11-12T18:00:00+00:00"}},{"CSV_BLUEBEAM_rev1":"Comparado: 2026-11-12 12:00 PT\n1,351 CSV / 1,351 PDF / 1,350 emparejados; 0 faltantes\n"})
print("R3b '1,351/1,351/1,350' -> open?",V.proyectos_abiertos_cache(c))
c=mk({"SUBIDA_OK.json":{"fecha_iso":"2026-11-12T18:00:00+00:00"}},{"CSV_BLUEBEAM_rev1":"Comparado: 2026-11-12 12:00 PT\n1351 CSV / 1351 PDF / 1351 emparejados; 0 faltantes en el PDF; faltantes en el CSV: 3\n"})
print("R5b 'faltantes en el CSV: 3' -> open?",V.proyectos_abiertos_cache(c))
c=mk({"SUBIDA_OK.json":{"fecha_iso":"2026-11-12T18:00:00+00:00"}},{"CSV_BLUEBEAM_rev1":"Comparado: 2026-11-12 12:00 PT\n1351 CSV / 1351 PDF / 1351 emparejados; 0 faltantes en el PDF; 3 markups sin pareja en el CSV\n"})
print("R5c '3 markups sin pareja' -> open?",V.proyectos_abiertos_cache(c))
