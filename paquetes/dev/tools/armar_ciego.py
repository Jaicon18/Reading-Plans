#!/usr/bin/env python3
"""armar_ciego.py — v73d: arma el paquete CIEGO (el que usan las pruebas) desde el paquete de desarrollo.

Por qué: tres rondas de parches puntuales no dejaron limpio el zip; las fugas venían de dos fuentes sistemáticas:
los tests / fixtures (datos de ejemplo tomados de corridas reales) y las adendas viejas (narrativa de corridas con
rooms, doors, walls, conteos y largos). Esta tool lo resuelve por construcción:
  1. tools/: copia todo MENOS test_*.py, fixture_reglas.py, las tools muertas y esta misma; agrega solo
     test_smoke_ciego.py (canon 100 % inventado) y los dos checkers (test_ciego_tools.py, test_ciego_v69.py);
  2. referencias/adenda_v*.md: se reescriben GENÉRICAS conservando cada título (el id de la regla en el catálogo no
     cambia): fuera tablas y bloques de código (datos de corridas) y todo número que no sea una medida genérica
     (fracciones y pulgadas, pies-pulgadas, %, gauge, ids de regla / versión, N/HOJA, fechas, numeración de lista)
     pasa a "<n>";
  3. el índice de adendas del SKILL se regenera desde esos títulos limpios y REGLAS_INVIOLABLES.md con el catálogo
     del árbol ciego;
  4. corre test_ciego_tools.py --estricto sobre el árbol ciego: si no da 0 hallazgos, NO arma el zip.
Uso: python3 armar_ciego.py <raiz_dev (con SKILL y tools)> <destino> [--zip salida.zip]
"""
import os
import re
import shutil
import subprocess
import sys
import zipfile

SKILL = "take-off-metal-frame-drywall"
FUERA = re.compile(r"^(test_.*|fixture_reglas|armar_ciego|auditor|hoja_detalle_img|localizar|cruzar_mep)\.py$")
# auditor / hoja_detalle_img / localizar / cruzar_mep: tools muertas (dependen de módulos que no viajan desde v66 o
# están retiradas) y nadie las importa: no van al paquete ciego.
QUEDAN = ("test_ciego_tools.py", "test_ciego_v69.py", "test_smoke_ciego.py")
GENERICO = re.compile(
    r"\d+(?:-\d+/\d+|\s\d+/\d+)?\s?\"|\d+/\d+\"?|\d+'\s?-\s?\d+(?:\s\d+/\d+)?\"?"      # pulgadas / pies-pulgadas
    r"|\d+(?:[.,]\d+)?\s?%|\b\d+\s?(?:ga|GA|gauge|mil)\b|\b\d{3}[ST]\d{3}-\d{2}\b"     # %, gauge, designación
    r"|\b(?:R7\d\.\d+b?|E\d{1,2}|PT\d|D\d{1,2}|A\d{1,2}|v\d+[a-z]?)\b|REGLA \d+\.\d+|§\d+|#0\b"  # ids de regla
    r"|\b\d{0,2}/?[A-Z]{1,2}-?\d{1,3}\.\d{1,3}\b"                                       # N/HOJA
    r"|\d{4}-\d{2}-\d{2}|\d{1,2}-(?:oct|sep|nov)-\d{4}|\b(?:Paso|PASO|Etapa|ETAPA) \d+[A-Z]?\b")
NUM = re.compile(r"\d+(?:[.,]\d+)*")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reglas_catalogo import NARRATIVA as NARR  # noqa: E402  (títulos que el catálogo no toma como regla)


def generico(texto):
    out, en_codigo = [], False
    for ln in texto.split("\n"):
        if ln.strip().startswith("```"):
            if not en_codigo:
                out.append("(ejemplo de una corrida retirado del paquete ciego)")
            en_codigo = not en_codigo
            continue
        if en_codigo or re.match(r"^\s*\|", ln):
            continue
        ln = re.sub(r"\b" + "B" + "OA_", "<PREFIJO>_", ln)   # prefijo de archivos de una prueba
        mt = re.match(r"^\s*#{2,4} (.+)$", ln)
        if mt:                                           # título de regla: intacto (id de la regla en el catálogo);
            out.append(NUM.sub("<n>", ln) if NARR.search(mt.group(1).strip()) else ln)   # narrativa: se limpia
            continue
        if re.match(r"^\s*# ", ln):                     # título de adenda (nivel 1, no es regla): se limpia
            out.append(NUM.sub("<n>", ln))
            continue
        m = re.match(r"^(\s*\d+\.\s)", ln)
        pre, cuerpo = (m.group(1), ln[m.end():]) if m else ("", ln)
        partes, i = [], 0
        for g in GENERICO.finditer(cuerpo):
            partes.append(NUM.sub("<n>", cuerpo[i:g.start()]))
            partes.append(g.group(0))
            i = g.end()
        partes.append(NUM.sub("<n>", cuerpo[i:]))
        out.append(pre + "".join(partes))
    return "\n".join(out)


def armar(raiz, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(os.path.join(raiz, SKILL), os.path.join(dest, SKILL), ignore=shutil.ignore_patterns("__pycache__"))
    td = os.path.join(dest, "tools")
    os.makedirs(td)
    for f in sorted(os.listdir(os.path.join(raiz, "tools"))):
        src = os.path.join(raiz, "tools", f)
        if os.path.isdir(src) or (FUERA.match(f) and f not in QUEDAN):
            continue
        shutil.copy2(src, os.path.join(td, f))
    for f in os.listdir(os.path.join(raiz, ".")):
        if f.startswith("CAMBIOS") and f.endswith(".md"):
            shutil.copy2(os.path.join(raiz, f), os.path.join(dest, f))
    rd = os.path.join(dest, SKILL, "referencias")
    for f in sorted(os.listdir(rd)):
        if f.startswith("adenda_v") and f.endswith(".md"):
            p = os.path.join(rd, f)
            txt = open(p, encoding="utf-8").read()
            open(p, "w", encoding="utf-8").write(generico(txt))
    # v73e: el índice de adendas del SKILL se regenera desde los títulos ya limpios de cada adenda
    sp = os.path.join(dest, SKILL, "SKILL.md")
    sk = open(sp, encoding="utf-8").read()
    for f in sorted(os.listdir(rd)):
        if f.startswith("adenda_v") and f.endswith(".md"):
            tit = next((ln[2:].strip() for ln in open(os.path.join(rd, f), encoding="utf-8").read().splitlines()
                        if ln.startswith("# ")), None)
            if tit:
                sk = re.sub(r"(?m)^- \*\*`" + re.escape(f) + r"`\*\* — .*$",
                            lambda _m, f=f, t=tit: f"- **`{f}`** — {t}", sk)
    open(sp, "w", encoding="utf-8").write(sk)
    env = dict(os.environ, TAKEOFF_SKILL=os.path.join(dest, SKILL))
    tab = subprocess.run([sys.executable, "-I", os.path.join(td, "reglas.py"), "tabla"], capture_output=True, text=True,
                         env=env)
    open(os.path.join(rd, "REGLAS_INVIOLABLES.md"), "w", encoding="utf-8").write(tab.stdout)
    r = subprocess.run([sys.executable, "-I", os.path.join(td, "test_ciego_tools.py"), "--estricto"],
                       capture_output=True, text=True, env=env, cwd=td)
    return r.returncode, r.stdout


def main(argv):
    a = list(argv[1:])
    z = None
    if "--zip" in a:
        i = a.index("--zip")
        z = a[i + 1]
        del a[i:i + 2]
    if len(a) != 2:
        print(__doc__)
        return 2
    rc, out = armar(a[0], a[1])
    print(out.strip().splitlines()[-1] if out.strip() else "")
    if rc != 0:
        print(out)
        print("NO SE ARMA: el árbol ciego tiene hallazgos")
        return 1
    if z:
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
            for base, _, fs in os.walk(a[1]):
                for f in sorted(fs):
                    if "__pycache__" in base:
                        continue
                    p = os.path.join(base, f)
                    zf.write(p, os.path.relpath(p, a[1]))
        print("zip:", z)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
