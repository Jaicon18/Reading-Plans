"""Verifica que un skill de arranque contenga TODAS las reglas acumuladas Y que cada regla "programa" tenga su compuerta.

Uso: python3 -I verificar_version.py <skill_dir_o_zip> <skills_archivo_dir> [<cache_proyectos_dir>]
     python3 -I verificar_version.py --selftest
1. (BE-115) Busca ids de reglas (R80e.N, R80w.N, R7x.N, R-ALC-NN, BE-N, BE-XX-NN, U-NNN) en todas las versiones archivadas
   (zips) y en cache_proyectos/*.md, y reporta las que no aparecen en el skill candidato.
2. (BE-121) revisar_registro: el candidato trae REGLAS_REGISTRO.json; toda regla "programa" tiene chequeo(s) que EXISTEN
   (archivo + función / compuerta A_*) y un test que existe y cita su token; "historico" apunta a una regla del registro;
   "programa-pendiente" dice por qué. Cobertura: todo R-ALC del REGLAS_ALCANCE.md, todo BE de la BIBLIOTECA_ERRORES.md y
   todo [U-NNN] de REGLAS_USUARIO_CLAUDE.md / REGLAS_HISTORICO.md está en el registro; toda regla vigente lleva su [U-NNN].
3. (U-020) revisar_zip: < 200 archivos, SKILL.md con YAML name / description, sin __pycache__, sin tools.orig_*, sin
   entradas de directorio (zip -D).
4. (U-027) revisar_indice: la VERSIÓN VIGENTE de skills_archivo/INDICE.md existe como zip archivado.
Sale con código 1 si falta algo (no arrancar el proyecto ni marcar la versión vigente).
"""
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
# Ids citados solo como "no existe" (no son reglas).
IGNORAR = {"BE-109"}

PAT = re.compile(r"\b(R80[a-z]\.\d+|R7\d\.\d+|R-ALC-\d+|BE-[A-Z]{2,3}-?\d+|BE-\d+|U-\d{3})\b")


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


class Fuente:
    """Lee archivos del skill candidato (zip o carpeta) por ruta relativa a la carpeta del skill (la que tiene SKILL.md)."""

    def __init__(self, p):
        self.zip = zipfile.ZipFile(p) if zipfile.is_zipfile(p) else None
        if self.zip:
            sk = [n for n in self.zip.namelist() if n.endswith("SKILL.md") and n.count("/") <= 1]
            self.base = sk[0][:-len("SKILL.md")] if sk else ""
        else:
            self.base = p if os.path.isfile(os.path.join(p, "SKILL.md")) else os.path.join(p, "take-off-metal-frame-drywall")

    def leer(self, rel):
        try:
            if self.zip:
                return self.zip.read(self.base + rel).decode("utf-8", "ignore")
            return open(os.path.join(self.base, rel), encoding="utf-8", errors="ignore").read()
        except (KeyError, OSError):
            return None


def _ruta(fuente, ordenes_dir, ref):
    pre, rel = ref.split(":", 1)
    if pre == "take-off":
        return fuente.leer(rel)
    if pre == "ordenes":
        p = os.path.join(ordenes_dir, rel)
        return open(p, encoding="utf-8", errors="ignore").read() if os.path.isfile(p) else None
    return None


def _tiene_funcion(txt, nombre):
    if nombre in ("modulo", "main") and txt is not None:
        return True
    if nombre.startswith("A_"):
        return f'"{nombre}"' in txt
    return re.search(r"^\s*def " + re.escape(nombre) + r"\b|^" + re.escape(nombre) + r"\s*=", txt, re.M) is not None


def ids_biblioteca(txt):
    ids = set()
    for l in txt.splitlines():
        m = re.match(r"\|\s*(BE-[A-Z0-9-]+)\s*\|", l) or re.match(r"#+\s*(BE-[A-Z0-9-]+)\b", l) or \
            re.match(r"[-*]\s*\*{0,2}(BE-[A-Z0-9-]+)\*{0,2}\s*[:—-]", l)
        if m:
            ids.add(m.group(1))
    return ids


def revisar_registro(fuente, ordenes_dir, cache_dir=None):
    """BE-121 -> lista de faltas (texto)."""
    f = []
    t = fuente.leer("REGLAS_REGISTRO.json")
    if t is None:
        return ["el skill candidato no trae REGLAS_REGISTRO.json (BE-121)"]
    reg = json.loads(t)
    ids = {e["id"] for e in reg.get("reglas") or []}
    for e in reg.get("reglas") or []:
        cat, i = e.get("categoria"), e["id"]
        if cat == "programa":
            chs, ts = e.get("chequeos") or [], [e.get("test")] + list(e.get("tests_extra") or [])
            if not chs:
                f.append(f"{i}: programa sin chequeo")
            for ch in chs:
                arch, _, fn = ch.partition("::")
                txt = _ruta(fuente, ordenes_dir, arch)
                if txt is None:
                    f.append(f"{i}: el chequeo {arch} no existe")
                elif not _tiene_funcion(txt, fn):
                    f.append(f"{i}: {arch} no tiene {fn}")
            for tt in ts:
                if not tt or not tt.get("archivo"):
                    f.append(f"{i}: programa sin test")
                    continue
                txt = _ruta(fuente, ordenes_dir, tt["archivo"])
                if txt is None:
                    f.append(f"{i}: el test {tt['archivo']} no existe")
                elif not re.search(r"(?<![\w-])" + re.escape(tt.get("token") or "") + r"(?![\w])", txt):
                    f.append(f"{i}: el test {tt['archivo']} no cita '{tt.get('token')}'")
        elif cat == "historico":
            if e.get("reemplazada_por") not in ids:
                f.append(f"{i}: histórica sin regla vigente que la reemplace")
        elif cat == "programa-pendiente":
            if not str(e.get("motivo") or "").strip():
                f.append(f"{i}: programa-pendiente sin motivo")
        elif cat != "conducta":
            f.append(f"{i}: categoría desconocida '{cat}'")
    alc = os.path.join(ordenes_dir, "REGLAS_ALCANCE.md")
    if os.path.isfile(alc):
        for x in sorted(set(re.findall(r"^## (R-ALC-\d+)", open(alc, encoding="utf-8").read(), re.M)) - ids):
            f.append(f"{x}: en REGLAS_ALCANCE.md pero no en el registro")
    bib = os.path.join(ordenes_dir, "BIBLIOTECA_ERRORES.md")
    if os.path.isfile(bib):
        for x in sorted(ids_biblioteca(open(bib, encoding="utf-8").read()) - ids):
            f.append(f"{x}: en BIBLIOTECA_ERRORES.md pero no en el registro")
    if cache_dir:
        for n in ("REGLAS_USUARIO_CLAUDE.md", "REGLAS_HISTORICO.md"):
            p = os.path.join(cache_dir, n)
            if not os.path.isfile(p):
                f.append(f"falta cache_proyectos/{n}")
                continue
            txt = open(p, encoding="utf-8").read()
            for x in sorted(set(re.findall(r"\[(U-\d{3})", txt)) - ids):
                f.append(f"{x}: en {n} pero no en el registro")
            if n == "REGLAS_USUARIO_CLAUDE.md":
                vig = txt.split("## REGLAS VIGENTES", 1)[-1]
                for l in vig.splitlines():
                    if l.startswith("- ") and not re.match(r"- \[U-\d{3}", l):
                        f.append(f"regla vigente sin id [U-NNN] (agregarla al registro): {l[:80]}")
    return f


def revisar_zip(p):
    """U-020 -> lista de faltas del zip del skill."""
    if not zipfile.is_zipfile(p):
        return []
    f = []
    with zipfile.ZipFile(p) as z:
        ns = z.namelist()
        arch = [n for n in ns if not n.endswith("/")]
        if len(arch) >= 200:
            f.append(f"zip con {len(arch)} archivos (límite < 200)")
        if any(n.endswith("/") for n in ns):
            f.append("zip con entradas de directorio (usar zip -D)")
        if any("__pycache__" in n for n in ns):
            f.append("zip con __pycache__")
        if any(re.search(r"(^|/)tools\.orig_", n) for n in ns):
            f.append("zip con carpeta de respaldo tools.orig_*")
        sk = [n for n in ns if n.endswith("SKILL.md") and n.count("/") <= 1]
        if not sk:
            f.append("zip sin SKILL.md")
        else:
            t = z.read(sk[0]).decode("utf-8", "ignore")
            m = re.match(r"---\n(.*?)\n---", t, re.S)
            if not m or not re.search(r"^name:\s*\S", m.group(1), re.M) or not re.search(r"^description:\s*\S", m.group(1), re.M):
                f.append("SKILL.md sin YAML name / description")
    return f


def revisar_indice(archivo):
    """U-027 -> faltas: la versión vigente de INDICE.md tiene su zip archivado."""
    p = os.path.join(archivo, "INDICE.md")
    if not os.path.isfile(p):
        return ["skills_archivo sin INDICE.md"]
    m = re.search(r"VERSIÓN VIGENTE[^:]*: [^(]*\(hoy (v[0-9a-z]+)", open(p, encoding="utf-8").read())
    if not m:
        return ["INDICE.md no marca la VERSIÓN VIGENTE"]
    v = m.group(1)
    if not [n for n in os.listdir(archivo) if n.startswith(f"take-off-metal-frame-drywall_{v}_") and n.endswith(".zip")]:
        return [f"la versión vigente {v} no tiene zip en skills_archivo"]
    return []


def main(argv):
    if argv[1:] == ["--selftest"]:
        return selftest()
    if len(argv) < 3:
        print(__doc__)
        return 2
    candidato, archivo = argv[1], argv[2]
    extra = argv[3:]
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
    malo = False
    if faltan:
        print("FALTAN:", " ".join(faltan))
        malo = True
    reg = revisar_registro(Fuente(candidato), AQUI, extra[0] if extra else None)
    zp = revisar_zip(candidato)
    ix = revisar_indice(archivo)
    for nombre, xs in (("REGISTRO (BE-121)", reg), ("ZIP (U-020)", zp), ("INDICE (U-027)", ix)):
        if xs:
            malo = True
            print(f"{nombre}: {len(xs)} falta(s)")
            for x in xs[:40]:
                print("  - " + x)
    if malo:
        return 1
    print("OK: el skill contiene todas las reglas acumuladas y cada regla 'programa' tiene chequeo + test.")
    return 0


def selftest():
    sys.path.insert(0, AQUI)
    import test_verificar_version as T
    T.correr()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
