"""Verifica que un skill de arranque contenga TODAS las reglas acumuladas.

Uso: python3 -I verificar_version.py <skill_dir_o_zip> <skills_archivo_dir> [<cache_proyectos_dir>]
Busca ids de reglas (R80e.N, R80w.N, R7x.N, R-ALC-NN, BE-N, BE-XX-NN) en todas las
versiones archivadas (zips) y en cache_proyectos/*.md, y reporta las que no aparecen
en el skill candidato. Sale con código 1 si falta alguna (no arrancar el proyecto).
"""
import os
import re
import sys
import zipfile

# Ids citados solo como "no existe" (no son reglas).
IGNORAR = {"BE-109"}

PAT = re.compile(r"\b(R80[a-z]\.\d+|R7\d\.\d+|R-ALC-\d+|BE-[A-Z]{2,3}-?\d+|BE-\d+)\b")


def ids_en_texto(t):
    return set(PAT.findall(t))


def ids_en_ruta(p):
    out = set()
    if zipfile.is_zipfile(p):
        with zipfile.ZipFile(p) as z:
            for n in z.namelist():
                if n.endswith((".md", ".py", ".json")):
                    out |= ids_en_texto(z.read(n).decode("utf-8", "ignore"))
    elif os.path.isdir(p):
        for raiz, _, archivos in os.walk(p):
            for a in archivos:
                if a.endswith((".md", ".py", ".json")):
                    with open(os.path.join(raiz, a), encoding="utf-8", errors="ignore") as f:
                        out |= ids_en_texto(f.read())
    elif os.path.isfile(p):
        with open(p, encoding="utf-8", errors="ignore") as f:
            out |= ids_en_texto(f.read())
    return out


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    candidato, archivo = sys.argv[1], sys.argv[2]
    extra = sys.argv[3:]
    tiene = ids_en_ruta(candidato)
    todas = set()
    for n in os.listdir(archivo):
        p = os.path.join(archivo, n)
        if n.endswith(".zip") or os.path.isdir(p):
            todas |= ids_en_ruta(p)
    for e in extra:
        todas |= ids_en_ruta(e)
    faltan = sorted(todas - tiene - IGNORAR)
    print(f"Reglas acumuladas: {len(todas)} · en el candidato: {len(tiene & todas)} · faltan: {len(faltan)}")
    if faltan:
        print("FALTAN:", " ".join(faltan))
        sys.exit(1)
    print("OK: el skill contiene todas las reglas acumuladas.")


if __name__ == "__main__":
    main()
