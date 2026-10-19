#!/usr/bin/env python3
"""test_verif_respuesta.py — v73: la compuerta de la respuesta caza términos del trade en español fuera del código
y deja pasar el código citado (datos sintéticos)."""
import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import verif_respuesta as VR  # noqa: E402

F = []


def ok(n, c):
    print(("OK   " if c else "FALLA"), n)
    c or F.append(n)


m = VR.revisar("El muro lleva tablaroca y canal.\nLa clave `muro` es del cierre.\n```\nperfilería metálica\n```")
ok("caza muro, tablaroca y canal en el renglón 1", sorted(t for n, t, _ in m if n == 1) == ["canal", "muro", "tablaroca"])
ok("no caza código (renglones 2-5)", not [x for x in m if x[0] > 1])
ok("inglés limpio", VR.revisar("The wall takes 5/8\" gypsum board on 3-5/8\" studs; joint compound and tape.") == [])
d = tempfile.mkdtemp()
p = os.path.join(d, "r.md")
open(p, "w").write("Dos capas de panel de yeso.\n")
ok("rc 1 con marcas", subprocess.run([sys.executable, "-I", os.path.join(AQUI, "verif_respuesta.py"), p],
                                     capture_output=True).returncode == 1)
open(p, "w").write("Two layers of gypsum board; el resto en español sin términos del trade.\n")
ok("rc 0 limpia", subprocess.run([sys.executable, "-I", os.path.join(AQUI, "verif_respuesta.py"), p],
                                 capture_output=True).returncode == 0)
print("test_verif_respuesta:", "OK" if not F else f"{len(F)} fallo(s)")
sys.exit(1 if F else 0)
