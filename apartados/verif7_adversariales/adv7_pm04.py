# adv7_pm04: NG-3.1 / BE-PM04 contra las órdenes candidatas v138. Sintético en /tmp/verif7/tmp (no toca el cache real).
import sys, os, json, tempfile; sys.path.insert(0, sys.argv[1]); import verificar_version as V
T = "/tmp/verif7/tmp"; os.makedirs(T, exist_ok=True)
def mk(files):
    c = tempfile.mkdtemp(dir=T)
    for rel, tx in files.items():
        p = os.path.join(c, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w").write(tx if isinstance(tx, str) else json.dumps(tx))
    return c
SUB = {"fecha_iso": "2026-11-12T18:00:00+00:00"}
OK = "# R\nComparado: 2026-11-12 12:00 PT\n- 1351 CSV / 1351 PDF / 1351 emparejados; 0 faltantes en cada lado.\n"
print("X0 control cuadra:", V.csv_cuadra(OK))
for extra in ("- 12 markups unpaired", "- unpaired: 12", "- 12 sin par", "- 12 no encontrados en el CSV", "- 12 left over in the PDF",
              "- el PDF tiene 12 markups más que el CSV", "- PDF has 12 more markups than the CSV", "- 12 sin coincidencia",
              "- Markups en el PDF (total real): 1363", "- 12 not paired", "- 12 markups solo en el PDF", "- 12 only in PDF",
              "- 12 no aparecen en el CSV"):
    c = mk({"proj/SUBIDA_OK_rev20.json": SUB, "proj/CSV_BLUEBEAM_rev20/RESULTADO.md": OK + extra + "\n"})
    print("X1", repr(extra), "-> cuadra:", V.csv_cuadra(OK + extra), "| abiertos:", V.proyectos_abiertos_cache(c))
# X2: rev21 EN CURSO en una subcarpeta del cache, con canon + TIEMPOS + tiempos.log pero SIN VERSION_PROYECTO.txt (vive en el workdir)
c = mk({"proj/SUBIDA_OK_rev20.json": SUB, "proj/CSV_BLUEBEAM_rev20/RESULTADO.md": OK,
        "proj/rev21/TIEMPOS.md": "| Paso | Inicio | Fin |\n|---|---|---|\n| 1 | 2026-11-13 08:00 PT | 2026-11-13 08:40 PT |\n",
        "proj/rev21/tiempos.log": "2026-11-13 08:00 | 1 inicio rev21\n", "proj/rev21/canon/takeoff_canon.json": {"walls": [{"id": "A-1"}]}})
print("X2 rev21 en curso (canon + TIEMPOS + tiempos.log en subcarpeta, sin VERSION_PROYECTO) -> abiertos:", V.proyectos_abiertos_cache(c))
# X3: el bloqueo: ¿existe un candado automático en el commit 'Publica …'?
hooks = "/home/user/Reading-Plans/.claude/settings.json"
s = json.load(open(hooks)); print("X3 hooks del repo:", sorted(s.get("hooks", {}).keys()),
      "| pre-commit git:", os.path.exists("/home/user/Reading-Plans/.git/hooks/pre-commit"))
