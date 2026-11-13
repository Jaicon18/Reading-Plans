# adv7_falt_b: (1) celdas separadas en v137 vs v138; (2) descubrimiento de archivos directos en COORDINACION/ y Auditoria/
import sys, os, json, tempfile; sys.path.insert(0, sys.argv[1]); import chequeos_biblioteca as CB, compuerta_entrega as CE
T = "/tmp/verif7/tmp"; os.makedirs(T, exist_ok=True)
can = {"walls": [], "ceilings": [{"room": "Z9 Corridor 901", "area_sf": 50.0}], "rcp_tags": []}
for raw in ("| 1 | corridor 901 ceiling missing | OPEN |", "| 1 | corridor 901 ceiling | MISSING | OPEN |", "| 1 | Room 901 | ceiling | missing |"):
    print("celdas", repr(raw), "->", CB.faltantes_auditoria(CB.B(canon=can, textos={"Auditoria/AUDITORIA_U181_rev9.md": raw}))[0])
for rel in ("Auditoria/hallazgos.csv", "Auditoria/notas.md", "Auditoria/sub/notas.md", "COORDINACION/sub/hallazgos.md", "COORDINACION/hallazgos.md"):
    w = tempfile.mkdtemp(dir=T); p = os.path.join(w, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write("| 1 | corridor 901 ceiling missing | OPEN |\n")
    print("rglob", rel, [os.path.relpath(x, w) for pat in ("**/Auditoria/**/*.md", "**/Auditoria/**/*.csv", "**/COORDINACION/**/*.md") for x in CB._rglob_seguro(w, pat)])
