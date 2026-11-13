# adv7_retro: v120-RETRO contra v81cf138: la "fuente independiente" (inicio_independiente) copiada de la rev anterior. Sintético.
import sys, os, json, tempfile; sys.path.insert(0, sys.argv[1]); import compuerta_entrega as CE
T = "/tmp/verif7/tmp"; os.makedirs(T, exist_ok=True)
TT = "| Paso | Inicio | Fin | Duración |\n|---|---|---|---|\n| 1 | 11-13 09:00 | 11-13 09:30 | 30 min |\n| 4 | 11-13 09:30 | 11-13 10:00 | 30 min |\n"
NEWX = "2026-11-13 09:00 | 1 inicio\n2026-11-13 09:30 | 1 fin\n2026-11-13 10:00 | 4 fin\n"
def mk(log, vp=None, bit=None, xl=None, name="rev21"):
    p = tempfile.mkdtemp(dir=T); w = os.path.join(p, name); os.makedirs(w)
    open(os.path.join(w, "tiempos.log"), "w").write(log)
    if vp is not None: open(os.path.join(w, "VERSION_PROYECTO.txt"), "w").write(vp)
    if bit is not None: open(os.path.join(w, "bitacora.jsonl"), "w").write("".join(json.dumps(r) + "\n" for r in bit))
    if xl: os.makedirs(os.path.join(w, "Take-off")); open(os.path.join(w, "Take-off", xl), "w").write("x")
    return w
def show(k, w):
    e, m = CE.proceso_v119(w, None, TT, 5); print(k, "->", e, "|", (m[0] if m else "")[:170])
HDR = "05-nov 11:26 PST | arranque proyecto\n"            # encabezado copiado SIN etiqueta (como Z2)
VP20 = "2026-11-05T19:30:00+00:00 | rev20 | v81cf110 | \n"   # VERSION_PROYECTO.txt de la rev20, copiado con la carpeta
show("R0 control Z2 (sin fuente independiente)", mk(HDR + NEWX))
show("R1 carpeta rev21 copiada de rev20: VERSION_PROYECTO.txt solo con el renglón rev20 + encabezado copiado", mk(HDR + NEWX, vp=VP20))
show("R1b igual con el Excel de la rev21 (etiqueta = 21)", mk(HDR + NEWX, vp=VP20, xl="Z9_Takeoff_rev21.xlsx"))
show("R2 sin VERSION_PROYECTO, bitacora.jsonl copiada de la rev20 (primer ts 05-nov)",
     mk(HDR + NEWX, bit=[{"tool": "canon.py", "args": [], "rc": 0, "hashes": {}, "ts": "2026-11-05T19:40:00"}]))
