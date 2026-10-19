#!/usr/bin/env python3
"""correr_suite.py — v73: corre TODA la suite del paquete desde una carpeta limpia, sin pasos a mano.

Por qué: la prueba 21B tuvo que instalar pymupdf y copiar la estructura del zip para llegar a 45/45 (la primera
corrida dio 37/45: módulo faltante y SKILL.md fuera de ruta). Esta tool lo hace sola:
  1. asegura las dependencias (arranque.asegurar_deps + Pillow / openpyxl): pip --quiet, con
     --break-system-packages si el sistema lo pide; lo que no se instale se dice y la suite no corre;
  2. ubica el skill: ../take-off-metal-frame-drywall, $TAKEOFF_SKILL o ~/.claude/skills/...; copia tools/ y el skill
     a una carpeta temporal con la estructura del zip (tools/ junto a take-off-metal-frame-drywall/);
  3. corre cada test_*.py con `python3 -I` desde esa copia y resume N/N con el log de cada falla.
Uso: python3 correr_suite.py [--skill <carpeta del skill>] [--solo test_x.py ...]     rc 0 = todo OK
"""
import glob
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
EXTRA = (("PIL", "Pillow"), ("openpyxl", "openpyxl"))


def deps():
    sys.path.insert(0, AQUI)
    import arranque
    return arranque.asegurar_deps(tuple(arranque.DEPS) + EXTRA)


def skill(d=None):
    for c in (d, os.path.join(AQUI, "..", "take-off-metal-frame-drywall"), os.environ.get("TAKEOFF_SKILL"),
              os.path.expanduser("~/.claude/skills/take-off-metal-frame-drywall")):
        if c and os.path.isfile(os.path.join(c, "SKILL.md")):
            return os.path.abspath(c)
    return None


def main(argv):
    a = list(argv[1:])
    sk = None
    if "--skill" in a:
        i = a.index("--skill")
        sk = a[i + 1]
        del a[i:i + 2]
    solo = a[a.index("--solo") + 1:] if "--solo" in a else []
    falta = deps()
    if falta:
        print("NO CORRE: faltan dependencias que no se pudieron instalar:", ", ".join(falta))
        return 1
    sk = skill(sk)
    if not sk:
        print("NO CORRE: no encuentro SKILL.md (pasar --skill o $TAKEOFF_SKILL)")
        return 1
    raiz = tempfile.mkdtemp(prefix="suite_v73_")
    shutil.copytree(AQUI, os.path.join(raiz, "tools"), ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(sk, os.path.join(raiz, "take-off-metal-frame-drywall"), ignore=shutil.ignore_patterns("__pycache__"))
    t = os.path.join(raiz, "tools")
    tests = solo or sorted(os.path.basename(x) for x in glob.glob(os.path.join(t, "test_*.py")))
    env = dict(os.environ, TAKEOFF_SKILL=os.path.join(raiz, "take-off-metal-frame-drywall"))
    env.pop("BITACORA", None)
    ok, malos = 0, []
    for x in tests:
        r = subprocess.run([sys.executable, "-I", x], cwd=t, capture_output=True, text=True, env=env, timeout=1800)
        open(os.path.join(raiz, x + ".log"), "w").write(r.stdout + r.stderr)
        if r.returncode == 0:
            ok += 1
        else:
            malos.append(x)
            print(f"FALLA {x}\n" + "\n".join((r.stdout + r.stderr).strip().splitlines()[-6:]))
    print(f"suite: {ok}/{len(tests)} OK ({raiz})")
    return 0 if not malos else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
