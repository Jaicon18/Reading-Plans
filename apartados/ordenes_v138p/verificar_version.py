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
4. (U-027) revisar_indice: la VERSIÓN VIGENTE de skills_archivo/INDICE.md existe como zip archivado; (BE-146)
   revisar_indice_encabezado: el "(hoy vN" del encabezado = la última línea "vN = VERSIÓN VIGENTE".
Sale con código 1 si falta algo (no arrancar el proyecto ni marcar la versión vigente).
"""
import datetime
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
CACHE_DEFECTO = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "cache_proyectos"))   # <repo>/.claude/skills/jc-hunter-ordenes -> <repo>/cache_proyectos
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
    """U-020 -> lista de faltas del zip del skill. BE-XF08 (Xfinity 11-nov, v81cf86 publicada con 208 archivos): con una CARPETA
    candidata también se cuentan los archivos (antes solo se contaban en un .zip y la carpeta pasaba); 200 o más = FAIL."""
    if not zipfile.is_zipfile(p):
        if os.path.isdir(p):
            base = p if os.path.isfile(os.path.join(p, "SKILL.md")) else os.path.join(p, "take-off-metal-frame-drywall")
            n = sum(len([f for f in fs]) for r, _d, fs in os.walk(base) if "__pycache__" not in r)
            if n >= 200:
                return [f"BE-XF08: la carpeta candidata tiene {n} archivos (límite de Upload skill < 200)"]
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
    enc = revisar_indice_encabezado(archivo)
    if enc:
        return enc
    zs = [n for n in os.listdir(archivo) if n.startswith(f"take-off-metal-frame-drywall_{v}_") and n.endswith(".zip")]
    if not zs:
        return [f"la versión vigente {v} no tiene zip en skills_archivo"]
    import hashlib
    distintos = {hashlib.md5(open(os.path.join(archivo, n), "rb").read()).hexdigest() for n in zs}
    for n in zs:             # BE-XF08: el zip VIGENTE publicado también se revisa (U-020: < 200 archivos, sin directorios ni __pycache__)
        malas = revisar_zip(os.path.join(archivo, n))
        if malas:
            return [f"BE-XF08: el zip vigente {n}: " + "; ".join(malas)]
    if len(distintos) > 1:   # BE-CF20 (copia idéntica FINAL-<Proyecto> de U-027 no cuenta): dos sesiones archivaron el MISMO número con contenido distinto (línea partida, BE-115)
        return [f"BE-CF20: la versión vigente {v} tiene {len(zs)} zips distintos ({', '.join(sorted(zs))}): unir en v+1"]
    return []


def revisar_indice_encabezado(archivo):
    """BE-146 -> faltas: el encabezado "VERSIÓN VIGENTE ... (hoy vN" de INDICE.md = la ÚLTIMA línea "vM = VERSIÓN VIGENTE" del
    archivo. Caso original (6-nov): v81cf55..v81cf57 publicadas y el encabezado seguía en "hoy v81cf54" (el hook SessionStart
    arrancaba con una versión vieja)."""
    p = os.path.join(archivo, "INDICE.md")
    if not os.path.isfile(p):
        return ["skills_archivo sin INDICE.md"]
    txt = open(p, encoding="utf-8").read()
    m = re.search(r"VERSIÓN VIGENTE[^:]*: [^(]*\(hoy (v[0-9a-z]+)", txt)
    if not m:
        return ["INDICE.md no marca la VERSIÓN VIGENTE"]
    ult = re.findall(r"\b(v[0-9a-z]+) = VERSIÓN VIGENTE", txt)
    if ult and ult[-1] != m.group(1):
        return [f"BE-146: el encabezado de INDICE.md dice 'hoy {m.group(1)}' y la última línea '= VERSIÓN VIGENTE' es {ult[-1]}: "
                f"actualizar el encabezado (o la línea) para que digan la misma versión"]
    return []


def revisar_skill(fuente):
    """BE-87 / BE-VS-11 -> faltas del skill candidato:
    BE-87: dos encabezados R80e.N / R80f.N con el MISMO número y distinto título en SKILL.md (choque de numeración);
    BE-VS-11: un chequeo @chequeo("A_X") de reglas.py que ninguna regla de reglas_clasificacion.py referencia (no corre)."""
    f = []
    sk = fuente.leer("SKILL.md") or ""
    vistos = {}
    for m in re.finditer(r"^#{2,4}\s+(R80[a-z]\.\d+)\s*[—:-]+\s*(.+)$", sk, re.M):
        n, t = m.group(1), re.sub(r"\W+", " ", m.group(2)).strip().lower()[:40]
        if n in vistos and vistos[n] != t:
            f.append(f"BE-87: {n} usado por dos reglas distintas ('{vistos[n][:30]}' / '{t[:30]}')")
        vistos.setdefault(n, t)
    rg, cl = fuente.leer("tools/reglas.py") or "", fuente.leer("tools/reglas_clasificacion.py")
    if rg and cl is not None:
        for a in sorted(set(re.findall(r'@chequeo\("(A_[A-Z0-9_]+)"', rg))):
            if f'"{a}"' not in cl:
                f.append(f"BE-VS-11: el chequeo {a} de reglas.py no está en reglas_clasificacion.py (nunca corre)")
    return f


def revisar_banco(archivo):
    """U-043 / BE-94 -> faltas: la VERSIÓN VIGENTE del INDICE registra la prueba del banco con 0 familias distintas."""
    p = os.path.join(archivo, "INDICE.md")
    if not os.path.isfile(p):
        return ["skills_archivo sin INDICE.md"]
    bloques = re.split(r"\n(?=\*\*\d{2}-[a-z]{3}: )", open(p, encoding="utf-8").read())
    vig = [x for x in bloques if "VERSIÓN VIGENTE PARA EL PRÓXIMO PROYECTO**" in x]
    if not vig:
        return ["INDICE.md sin bloque VERSIÓN VIGENTE"]
    v = vig[-1]
    if not re.search(r"(?i)banco", v):
        return ["U-043: la versión vigente no registra la prueba del banco (todas las lecturas guardadas)"]
    if not re.search(r"(?i)= ?0 (familias )?(distintas|diferencias)|0 familias distintas|0 diferencias|banco:? 0 distintas", v):
        return ["U-043: el banco de la versión vigente no dice 0 familias distintas / 0 diferencias"]
    return []


VERSIONES_DUPLICADAS_HISTORICAS = {"v80u"}


def revisar_versiones_unicas(archivo):
    """BE-144: dos sesiones armaron el mismo número de versión (v81cf43 O'Reilly y CFA; antes BE-CF20).
    Cada número de versión = un solo zip en skills_archivo/. El número se aparta antes de armar
    en skills_archivo/VERSION_EN_CURSO.md (commit + push primero)."""
    import collections, hashlib
    if not archivo or not os.path.isdir(archivo):
        return []
    hashes = collections.defaultdict(set)
    for n in os.listdir(archivo):
        m = re.match(r"take-off-metal-frame-drywall_([^_]+)_.*\.zip$", n)
        if m:
            # copia idéntica (mismo contenido, p. ej. el FINAL-<Proyecto> de U-027) no es otra versión
            hashes[m.group(1)].add(hashlib.md5(open(os.path.join(archivo, n), "rb").read()).hexdigest())
    c = {v: len(h) for v, h in hashes.items()}
    return [f"versión {v} archivada {k} veces (BE-144: apartar el número en VERSION_EN_CURSO.md antes de armar)"
            for v, k in sorted(c.items()) if k > 1 and v not in VERSIONES_DUPLICADAS_HISTORICAS]


def revisar_ordenes(cache, horas=24):
    """U-136: toda orden de la bandeja (_entrantes.jsonl) con más de `horas` sin clasificar en MAPA_ORDENES.json = falta."""
    import json, datetime
    if not cache:
        return []
    car = os.path.join(cache, "ORDENES_CRUDAS")
    ent = os.path.join(car, "_entrantes.jsonl")
    if not os.path.exists(ent):
        return []
    try:
        mapa = json.load(open(os.path.join(car, "MAPA_ORDENES.json"), encoding="utf-8"))
    except Exception:
        mapa = {}
    ahora = datetime.datetime.now(datetime.timezone.utc)
    faltas = []
    for linea in open(ent, encoding="utf-8"):
        try:
            r = json.loads(linea)
        except Exception:
            continue
        if r.get("id") in mapa:
            continue
        try:
            t = datetime.datetime.fromisoformat(r["ts_utc"])
        except Exception:
            t = ahora
        if (ahora - t).total_seconds() > horas * 3600:
            faltas.append(f"{r.get('id')} ({r.get('ts_utc')}) sin clasificar: {r.get('texto','')[:80]}")
    return faltas


RX_POSTMORTEM = re.compile(r"^POSTMORTEM_COBERTURA_(\d{4}-\d{2}-\d{2})[\w.-]*\.md$")
RX_GUIONES = re.compile("[\u2010-\u2015\u2212\u2E3A\u2E3B\uFE58\uFE63\uFF0D\u00AD]")
RX_ANCHO_CERO = re.compile("[\u200B-\u200D\u2060\uFEFF]")


def norm_txt(s, lower=True):
    """v120 (verificación 4): normalización COMÚN de todo texto que se compara (estados, ids, disposiciones, gap_proof): NFKC + todo guion
    Unicode -> '-' (y '--' -> '-') + ancho cero fuera + espacios / NBSP / tabs colapsados + minúsculas. La MISMA función está en
    compuerta_entrega.norm_txt."""
    import unicodedata
    t = unicodedata.normalize("NFKC", str(s or ""))
    t = RX_ANCHO_CERO.sub("", RX_GUIONES.sub("-", t))
    t = re.sub(r"-{2,}", "-", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t.lower() if lower else t


RX_PM_CERRADO = re.compile(r"ok ?- ?confirmed-closed")   # v120: estado de cierre, match COMPLETO sobre norm_txt(estado)
RX_PM_FECHA = re.compile(r"(?im)^\W*fecha\s*:\s*(\d{4}-\d{2}-\d{2})[ t](\d{1,2}):(\d{2})\s*(pt|pst|pdt|utc|z)\b")
PM_ARRASTRE_DESDE = ("2026-11-12", "b")    # v120: desde el 12b (primer post-mortem con verificación independiente) los abiertos se arrastran
                                          # entre principales; los anteriores los cerró la re-revisión completa del 2026-11-12 (124 renglones)
RX_PM_PRINCIPAL = re.compile(r"^POSTMORTEM_COBERTURA_(\d{4}-\d{2}-\d{2})([a-z]?)\.md$")   # el post-mortem; _VERIFICACION / _CIERRE
                                                                                        # / copias son acompañantes, no lo reemplazan


def tabla_postmortem(txt):
    """U-185: renglones de la tabla 'id | error / regla | chequeo | test | estado' -> [(id, estado)]. v121: la columna 'estado' se toma
    por su ENCABEZADO (puede haber columnas después, p. ej. 'notas'); celdas sin negritas."""
    out, ke = [], None
    for ln in txt.splitlines():
        cs = [re.sub(r"[*`]", "", x).strip() for x in ln.strip().strip("|").split("|")]
        if not ln.lstrip().startswith("|"):
            ke = None
            continue
        cl = [c.lower() for c in cs]
        if cs and cl[0] == "id" and any(c.startswith("estado") or c.startswith("status") for c in cl):
            ke = next(k for k, c in enumerate(cl) if c.startswith("estado") or c.startswith("status"))
            continue
        if ke is not None and cs and not set(cs[0]) <= set("-: ") and ke < len(cs):
            out.append((cs[0], cs[ke]))
    return out


def causas_no_guard(txt):
    """U-185 (verificación 12b): tabla de causas '# | causa | candado | estado': un renglón con 'NO GUARD' en su estado sigue abierto."""
    out, dentro = [], False
    for ln in txt.splitlines():
        cs = [x.strip() for x in ln.strip().strip("|").split("|")]
        if ln.lstrip().startswith("|") and cs and cs[0] == "#" and cs[-1].lower().startswith("estado"):
            dentro = True
            continue
        if dentro and not ln.lstrip().startswith("|"):
            dentro = False
            continue
        if dentro and cs and not set(cs[0]) <= set("-: ") and re.search(r"(?i)NO\s+GUARD", cs[-1]):
            out.append((f"causa {cs[0]}", "NO GUARD"))
    return out


def abiertos_postmortem(txt):
    """U-185: renglones WEAK / MISSING abiertos. Cerrado = 'OK ...' o 'conducta: <motivo de al menos 3 palabras>'."""
    ab = []
    for i, e in tabla_postmortem(txt):
        u = e.strip("* ")
        if re.match(r"(?i)OK\b", u):
            continue
        m = re.match(r"(?i)conducta\s*[:—–-]\s*(.+)", u)
        if m and len(m.group(1).split()) >= 3:
            continue
        ab.append((i, (re.match(r"(?i)(WEAK|MISSING)", u) or re.match(r"(\S*)", u)).group(1).upper() or "SIN ESTADO"))
    return ab


def _cierre_pt(iso):
    import datetime
    try:
        t = datetime.datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
        from zoneinfo import ZoneInfo
        return t.astimezone(ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d")
    except Exception:
        return str(iso or "")[:10]


def _cierre_dt(iso):
    import datetime
    try:
        return datetime.datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
    except Exception:
        return None


RX_PM_HORA = re.compile(r"(\d{4}-\d{2}-\d{2})[ T](\d{1,2}:\d{2})(?::\d{2})?\s*(UTC|Z|PT|PST|PDT|[+-]\d{2}:?\d{2})?")


def _pm_hora(nombre, txt):
    """momento del post-mortem: fecha-hora escrita en sus primeras líneas ('2026-11-12 18:40 UTC' / PT); si no trae hora, el FIN del día
    de su nombre en California (un post-mortem de la mañana no puede cubrir un cierre de la tarde si dice su hora)."""
    import datetime
    from zoneinfo import ZoneInfo
    pt = ZoneInfo("America/Los_Angeles")
    m = RX_PM_HORA.search("\n".join(txt.splitlines()[:12]))
    if m:
        t = datetime.datetime.fromisoformat(f"{m.group(1)}T{int(m.group(2).split(':')[0]):02d}:{m.group(2).split(':')[1]}")
        z = (m.group(3) or "PT").upper()
        if z in ("UTC", "Z"):
            return t.replace(tzinfo=datetime.timezone.utc)
        if z in ("PT", "PST", "PDT"):
            return t.replace(tzinfo=pt)
        return datetime.datetime.fromisoformat(t.isoformat() + (z if ":" in z else z[:3] + ":" + z[3:]))
    d = RX_POSTMORTEM.match(nombre).group(1)
    return datetime.datetime.fromisoformat(d + "T23:59:59").replace(tzinfo=pt)


def fecha_verificacion(txt):
    """U-185 (verificación 4): el campo explícito 'Fecha: YYYY-MM-DD HH:MM PT' (o UTC) del encabezado (primeras 15 líneas). -> datetime o None"""
    from zoneinfo import ZoneInfo
    m = RX_PM_FECHA.search("\n".join(norm_txt(re.sub(r"[*_`]", "", l), lower=False) for l in str(txt).splitlines()[:15]))   # v121: **Fecha:**
    if not m:
        return None
    t = datetime.datetime.fromisoformat(f"{m.group(1)}T{int(m.group(2)):02d}:{m.group(3)}")
    return t.replace(tzinfo=datetime.timezone.utc if m.group(4).lower() in ("utc", "z") else ZoneInfo("America/Los_Angeles"))


def fecha_git(path):
    """v121 (U-185, verificación 5): fecha del commit que AGREGÓ el archivo en git (para verificaciones sin 'Fecha:'). -> datetime o None
    (sin git / archivo sin commit)."""
    import subprocess
    try:
        r = subprocess.run(["git", "-C", os.path.dirname(os.path.abspath(path)), "log", "--diff-filter=A", "--follow", "--format=%cI", "--",
                            os.path.basename(path)], capture_output=True, text=True, timeout=30)
        ln = (r.stdout or "").strip().splitlines()
        return datetime.datetime.fromisoformat(ln[-1]) if r.returncode == 0 and ln else None
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


def revisar_postmortem(cache):
    """U-185 (COORDINACIÓN 12-nov) + post-mortem 2026-11-12b (WEAK U-185): el CIERRE es la última subida de la rev vigente del proyecto
    cerrado más reciente (fecha_iso de TODOS sus SUBIDA_OK*.json, hora completa; no primera_subida_iso, no por día). Se evalúa SOLO
    el post-mortem MÁS NUEVO (orden de nombre: 2026-11-12b > 2026-11-12) y tiene que ser posterior al cierre; con WEAK / MISSING
    abiertos = falta (un post-mortem limpio más viejo ya no lo tapa)."""
    import json
    cache = cache or CACHE_DEFECTO                       # v121: sin 3er arg = la ruta por defecto del repo (U-185 corre siempre)
    if not cache or not os.path.isdir(cache):
        return [f"sin cache_proyectos ({cache}): el post-mortem no se puede revisar = falla (U-185 corre siempre)"]
    cierres = []
    for d in os.listdir(cache):
        dd = os.path.join(cache, d)
        if not os.path.isdir(dd):
            continue
        for n in _subidas_ok(dd):                         # v121: recursivo (como BE-PM04)
            try:
                x = json.load(open(n, encoding="utf-8"))
            except Exception:
                continue
            t = _cierre_dt(x.get("fecha_iso") or x.get("primera_subida_iso"))
            if t:
                cierres.append((t, d))
    if not cierres:
        return []
    cierre, proy = max(cierres)
    pms = sorted((RX_PM_PRINCIPAL.match(n).groups(), n) for n in os.listdir(cache) if RX_PM_PRINCIPAL.match(n))
    if not pms:
        return [f"{proy} cerrado {cierre.isoformat()} sin cache_proyectos/POSTMORTEM_COBERTURA_<fecha>[letra].md posterior (U-185)"]
    n = pms[-1][1]                                       # el principal más nuevo: hora y tabla
    txt = open(os.path.join(cache, n), encoding="utf-8").read()
    if _pm_hora(n, txt) < cierre:
        return [f"{proy} cerrado {cierre.isoformat()}: el post-mortem más nuevo ({n}) es anterior al cierre (U-185)"]
    if not tabla_postmortem(txt):
        return [f"{n}: sin la tabla principal 'id | error / regla | chequeo | test | estado' (0 renglones) = falla (U-185)"]
    cadena = [m for g, m in pms if g >= PM_ARRASTRE_DESDE] or [n]
    abiertos, faltas, leidos = {}, [], []
    for pm in cadena:                                    # v120 (verificación 3, C1 / A2): un principal nuevo NO borra los abiertos de uno
        tp = txt if pm == n else open(os.path.join(cache, pm), encoding="utf-8").read()   # anterior: se arrastran
        base = pm[:-3] + "_"
        todos = sorted(m for m in os.listdir(cache) if m.startswith(base) and m.endswith(".md"))
        txts = {m: open(os.path.join(cache, m), encoding="utf-8").read() for m in todos}
        verifs, ahora = [], datetime.datetime.now(datetime.timezone.utc)
        for m in todos:
            if "_VERIFICACION" not in m.upper():
                continue
            t_ = fecha_verificacion(txts[m]) or fecha_git(os.path.join(cache, m))   # v121: sin 'Fecha:' = la fecha de su commit en git
            if t_ is None:
                faltas.append(f"{m}: verificación sin el campo 'Fecha: YYYY-MM-DD HH:MM PT' en su encabezado ni commit en git = falla (U-185)")
            elif t_ > ahora + datetime.timedelta(minutes=10):
                faltas.append(f"{m}: 'Fecha: {t_.isoformat()}' en el futuro = falla (U-185)")
            else:
                verifs.append((t_, m))
        verifs.sort()
        otros = [m for m in todos if "_VERIFICACION" not in m.upper()]
        faltas += [f"{m}: verificación sin la tabla 'id | … | estado' = falla (U-185: no pasa en vacío)" for _t, m in verifs
                   if not tabla_postmortem(txts[m])]
        for m in [pm] + otros:
            t = tp if m == pm else txts[m]
            for i, e in abiertos_postmortem(t) + causas_no_guard(t):
                abiertos.setdefault(norm_txt(i), (e, m, i))
        for _t, m in verifs:                             # un renglón se cierra SOLO con el estado 'ok - confirmed-closed' (match COMPLETO
            for i, e in tabla_postmortem(txts[m]):       # después de norm_txt) y SOLO el id de su PRIMERA columna (verificación 4)
                k0 = norm_txt(i)
                ng = re.fullmatch(r"ng-?(\d+\.\d+)(?: ?/ ?([a-z0-9][\w.-]*))?", k0)
                claves = {k0} | ({f"causa {ng.group(1)}"} | ({ng.group(2)} if ng.group(2) else set()) if ng else set())
                u = norm_txt(e.strip("* "))
                if RX_PM_CERRADO.fullmatch(u):
                    for k in claves:
                        abiertos.pop(k, None)
                elif re.match(r"(weak|missing|still)", u):
                    for k in claves:
                        abiertos[k] = ("MISSING" if u.startswith("missing") else "WEAK", m, i)
        leidos += [pm] + otros + [m for _t, m in verifs]
    if not abiertos and not faltas:
        return []
    ab = [(v[2], (v[0], v[1])) for v in abiertos.values()]
    nw = sum(1 for _i, (e, _m) in ab if e == "WEAK")
    nm = sum(1 for _i, (e, _m) in ab if e == "MISSING")
    ng = sum(1 for _i, (e, _m) in ab if e == "NO GUARD")
    return faltas + ([f"{' + '.join(leidos)}: {nw} WEAK / {nm} MISSING / {ng} NO GUARD abiertos ({len(ab)} renglones; se cierran solo con "
                      "el estado 'OK — CONFIRMED-CLOSED' en una verificación; un principal nuevo no los borra; U-185): "
                      + ", ".join(i for i, _e in ab[:30])] if ab else [])


RX_DEF_TEST = re.compile(r"(?m)^def (test_\w+)\(")


def tests_sin_llamar(fuente):
    """post-mortem 2026-11-12b (BE-CR42 / BE-GK47): todo 'def test_…' de tools/test_*.py del candidato se LLAMA en su archivo (a nivel de
    módulo, en __main__ o en una lista / tupla de funciones); correr_suite ejecuta cada archivo como script, no con pytest.
    -> [archivo::test sin llamar]"""
    if fuente.zip:
        nombres = [n[len(fuente.base):] for n in fuente.zip.namelist() if n.startswith(fuente.base)]
    else:
        nombres = [os.path.relpath(os.path.join(r, f), fuente.base) for r, _d, fs in os.walk(fuente.base) for f in fs]
    out = []
    for rel in sorted(nombres):
        b = os.path.basename(rel)
        if not (rel.startswith("tools/") and b.startswith("test_") and b.endswith(".py")):
            continue
        s = fuente.leer(rel) or ""
        for t in RX_DEF_TEST.findall(s):
            resto = s.replace(f"def {t}(", "")
            if not re.search(rf"\b{t}\s*\(|[\[(,=]\s*{t}\b", resto):
                out.append(f"{b}::{t}")
    return out


def sha_tools(fuente):
    """BE-PM04 (verificación 2): sha256 del árbol tools/ del candidato (ruta relativa + sha256 de cada archivo, sin __pycache__ / .pyc);
    compuerta_entrega.sha_tools calcula lo mismo sobre sus propias tools y lo guarda en PRUEBA_ABIERTOS."""
    import hashlib
    if fuente.zip:
        nombres = [n[len(fuente.base):] for n in fuente.zip.namelist() if n.startswith(fuente.base + "tools/") and not n.endswith("/")]
        leer = lambda r: fuente.zip.read(fuente.base + r)                                  # noqa: E731
    else:
        t = os.path.join(fuente.base, "tools")
        nombres = [os.path.relpath(os.path.join(r, f), fuente.base) for r, _d, fs in os.walk(t) for f in fs]
        leer = lambda r: open(os.path.join(fuente.base, r), "rb").read()                    # noqa: E731
    nombres = sorted(n.replace(os.sep, "/") for n in nombres if "__pycache__" not in n and not n.endswith(".pyc"))
    return hashlib.sha256("\n".join(f"{n} {hashlib.sha256(leer(n)).hexdigest()}" for n in nombres).encode()).hexdigest()


FECHA_U157 = "2026-11-10T00:00:00+00:00"               # U-157: la comparación del CSV del usuario cierra un proyecto (desde aquí)


RX_COMPARADO = re.compile(r"(?im)^\W*comparado\s*:\s*(\d{4}-\d{2}-\d{2})[ t](\d{1,2}):(\d{2})(?::\d{2})?\s*(pt|pst|pdt|utc|z|[+-]\d{2}:?\d{2})\b")


def _fecha_resultado(tx):
    """v120 (verificación 4): el momento de la comparación del CSV es SOLO el campo explícito 'Comparado: YYYY-MM-DD HH:MM PT|UTC|±hh:mm'
    de RESULTADO.md. -> datetime con zona o None (sin el campo = el proyecto cuenta como ABIERTO)."""
    from zoneinfo import ZoneInfo
    m = next((x for x in (RX_COMPARADO.match(norm_txt(re.sub(r"[*_`]", "", ln), lower=False)) for ln in str(tx).splitlines()) if x), None)
    if not m:                                            # v121: 'Comparado:' se lee POR LÍNEA, antes de norm (norm junta las líneas)
        return None
    t = datetime.datetime.fromisoformat(f"{m.group(1)}T{int(m.group(2)):02d}:{m.group(3)}")
    z = m.group(4).lower()
    if z in ("utc", "z"):
        return t.replace(tzinfo=datetime.timezone.utc)
    if z in ("pt", "pst", "pdt"):
        return t.replace(tzinfo=ZoneInfo("America/Los_Angeles"))
    return datetime.datetime.fromisoformat(t.isoformat() + (z if ":" in z else z[:3] + ":" + z[3:]))


def _subidas_ok(dd):
    """v121 (BE-PM04): TODOS los SUBIDA_OK*.json del proyecto, buscados de forma RECURSIVA (REV10_FINAL/SUBIDA_OK.json)."""
    import glob as _g
    return sorted(_g.glob(os.path.join(dd, "**", "SUBIDA_OK*.json"), recursive=True))


def _rev_de(nombre):
    m = re.search(r"(?i)(?:^|[_\-\s])(rev\s*-?\s*\d{1,3}[a-z]?)(?=$|[_\-\s.])", nombre)
    return re.sub(r"[\s-]", "", m.group(1)).lower() if m else None


def _rev_subida(f, dd):
    """rev de un SUBIDA_OK: sufijo del nombre (SUBIDA_OK_rev20a.json), si no la carpeta más cercana con 'revN' (REV10_FINAL_5nov)."""
    r = _rev_de(os.path.basename(f)[:-5])
    d = os.path.dirname(f)
    while not r and os.path.realpath(d).startswith(os.path.realpath(dd)) and os.path.realpath(d) != os.path.realpath(dd):
        r, d = _rev_de(os.path.basename(d)), os.path.dirname(d)
    return r


def _es_proyecto(dd):
    return bool(_subidas_ok(dd)) or os.path.isfile(os.path.join(dd, "VERSION_PROYECTO.txt"))


RX_CONTEO_CSV = re.compile(r"(?i)(\d[\d,]*)\s*CSV\s*/\s*(\d[\d,]*)\s*PDF\s*/\s*(\d[\d,]*)\s*emparejados")
RX_FALTAN_N = re.compile(r"(?i)\b(\d[\d,]*)\s+(?:markups?\s+)?(?:faltantes?|sin\s+pareja|unmatched|missing)\b"
                         r"|\b(?:faltantes?|sin\s+pareja|unmatched|missing)\b[^\d\n|;]{0,30}?[:=]\s*(\d[\d,]*)")


def csv_cuadra(tx):
    """v121 (BE-PM04): RESULTADO.md cuadra: 'N CSV / N PDF / N emparejados' (miles con coma) iguales y > 0, '0 faltantes' y NINGÚN otro
    número de faltantes / sin pareja / unmatched / missing distinto de 0 (formas 'K faltantes', 'faltantes en el CSV: K', 'K markups sin
    pareja')."""
    t = norm_txt(re.sub(r"[*_`]", "", str(tx)), lower=False)
    n = RX_CONTEO_CSV.search(t)
    if not n:
        return False
    v = {int(x.replace(",", "")) for x in n.groups()}
    otros = [int((a or b).replace(",", "")) for a, b in RX_FALTAN_N.findall(t)]
    return len(v) == 1 and v.pop() > 0 and bool(re.search(r"\b0\s+faltantes", t)) and not any(otros)


def proyectos_abiertos_cache(cache, errores=None):
    """BE-PM04 (verificaciones 2, 3 y 4): proyectos con entrega vigente NO cerrada. Abierto = tiene SUBIDA_OK*.json (con o sin rev; fecha en
    'fecha_iso' o 'fecha', con zona; sin fecha o sin zona -> `errores`) con la última subida desde U-157, y NO hay un
    CSV_BLUEBEAM_*/RESULTADO.md con 'N CSV / N PDF / N emparejados' (N > 0), '0 faltantes' sin otro 'K faltantes' y 'Comparado: <fecha>'
    POSTERIOR a la última subida y al último VERSION_PROYECTO.txt (una rev nueva en curso = abierto)."""
    import json
    import glob as _g
    out = []
    errores = errores if errores is not None else []
    if not cache or not os.path.isdir(cache):
        return out
    for d in sorted(os.listdir(cache)):
        dd = os.path.join(cache, d)
        subs, dudoso = [], False
        revs = []
        for f in _subidas_ok(dd):                         # v121: recursivo
            try:
                x = json.load(open(f, encoding="utf-8"))
            except Exception as e:
                errores.append(f"{d}/{os.path.basename(f)} ilegible: {e}")
                dudoso = True
                continue
            t = _cierre_dt(x.get("fecha_iso") or x.get("fecha") or x.get("primera_subida_iso"))
            if t is None:
                errores.append(f"{d}/{os.path.basename(f)} sin fecha ('fecha_iso' / 'fecha'): no se puede saber si está cerrado (BE-PM04)")
                dudoso = True
            elif t.tzinfo is None:
                errores.append(f"{d}/{os.path.basename(f)}: fecha sin zona horaria ({t.isoformat()}) (BE-PM04)")
                dudoso = True
            else:
                subs.append(t)
                revs.append((t, _rev_subida(f, dd) is not None, _rev_subida(f, dd)))
        if dudoso:
            out.append(d)                                # una subida que no se puede fechar = abierto (y FAIL en revisar)
            continue
        if not subs:
            continue
        ult = max(subs)
        if ult < _cierre_dt(FECHA_U157):
            continue
        vp = os.path.join(dd, "VERSION_PROYECTO.txt")
        if os.path.isfile(vp):
            for ln in open(vp, encoding="utf-8", errors="ignore"):
                t = _cierre_dt(ln.split("|")[0].strip())
                if t and t.tzinfo and t > ult:
                    ult = t
        cerr = False
        rev_ult = max(revs)[2] if revs else None          # v121: el CSV cierra SOLO la MISMA rev de la última subida
        for r in _g.glob(os.path.join(dd, "**", "CSV_BLUEBEAM_*", "RESULTADO.md"), recursive=True):
            if not rev_ult or _rev_de(os.path.basename(os.path.dirname(r))) != rev_ult:
                continue
            tx = open(r, encoding="utf-8", errors="ignore").read()
            fr = _fecha_resultado(tx)
            if csv_cuadra(tx) and fr and fr > ult:
                cerr = True
        if not cerr:
            out.append(d)
    return out


RX_VERSION_SKILL = re.compile(r"\*\*VERSION:\s*(v(\d+)cf(\d+)[a-z]?)\*\*")


def revisar_prueba_abiertos(archivo, fuente=None, desde=(81, 119), cache=None):
    """NO GUARD 3.1 / BE-PM04 (+ verificación 12b): ANTES de publicar, la versión del CANDIDATO (línea **VERSION: vNcfM** de su SKILL.md;
    si no, la vigente del INDICE) desde v81cf119 tiene skills_archivo/PRUEBA_ABIERTOS_<v>.json con TODOS los proyectos de
    skills_archivo/PROYECTOS_ABIERTOS.json ({"proyectos": [nombres de cache_proyectos]}), cada uno con 0 regresiones sin explicar."""
    import json
    m = RX_VERSION_SKILL.search((fuente.leer("SKILL.md") or "") if fuente else "")
    if not m:
        p = os.path.join(archivo, "INDICE.md")
        if not os.path.isfile(p):
            return []
        m = re.search(r"VERSIÓN VIGENTE[^:]*: [^(]*\(hoy (v(\d+)cf(\d+)[a-z]?)", open(p, encoding="utf-8").read())
    if not m or (int(m.group(2)), int(m.group(3))) < desde:
        return []
    v = m.group(1)
    fa = os.path.join(archivo, "PROYECTOS_ABIERTOS.json")
    try:
        abiertos = list(json.load(open(fa, encoding="utf-8")).get("proyectos") or [])
    except Exception:
        return [f"sin skills_archivo/PROYECTOS_ABIERTOS.json legible (lista de proyectos abiertos que la versión {v} tiene que probar)"]
    out = []
    if not abiertos:
        out.append("skills_archivo/PROYECTOS_ABIERTOS.json con la lista VACÍA (U-137: no pasa en vacío)")
    cache = cache or os.path.join(os.path.dirname(os.path.abspath(archivo)), "cache_proyectos")   # v120: el detector corre SIEMPRE
    if not os.path.isdir(cache):
        out.append(f"sin cache_proyectos ({cache}): el detector de proyectos abiertos no puede correr (BE-PM04)")
    else:
        fantasmas = [p for p in abiertos if not _es_proyecto(os.path.join(cache, p))]
        if fantasmas:
            out.append("PROYECTOS_ABIERTOS.json nombra carpetas que no son proyectos de cache_proyectos (sin SUBIDA_OK ni "
                       "VERSION_PROYECTO.txt): " + ", ".join(fantasmas))
    errs = []
    reales = [p for p in proyectos_abiertos_cache(cache, errs) if p not in abiertos]
    out += errs
    if reales:
        out.append("PROYECTOS_ABIERTOS.json no trae proyectos con entrega vigente sin CSV comparado N/N: " + ", ".join(reales))
    f = os.path.join(archivo, f"PRUEBA_ABIERTOS_{v}.json")
    if not os.path.isfile(f):
        return out + [f"la versión {v} no tiene skills_archivo/PRUEBA_ABIERTOS_{v}.json (compuerta de la candidata sobre los proyectos "
                      "abiertos antes de publicar)"]
    try:
        x = json.load(open(f, encoding="utf-8"))
    except Exception as e:
        return out + [f"{os.path.basename(f)} ilegible: {e}"]
    if fuente is not None:                              # cada proyecto corrido con ESTAS tools (sha del árbol tools/ del candidato)
        sha = sha_tools(fuente)
        malos = [k for k, pv in (x.get("proyectos") or {}).items() if pv.get("sha_tools") != sha]
        if malos:
            out.append(f"{os.path.basename(f)}: {', '.join(malos)} corrido(s) con otras tools (sha_tools distinto del candidato "
                       f"{sha[:12]}): re-correr prueba_abiertos con el candidato final")
    if x.get("version_candidata") != v:
        out.append(f"{os.path.basename(f)} es de la versión {x.get('version_candidata')}, no de {v}")
    for k, pv in (x.get("proyectos") or {}).items():       # v120 (verificación 3, P3): las regresiones de CADA proyecto se leen
        regs = [r for r in x.get("regresiones") or [] if r.get("proyecto") == k]
        sinx = [r for r in regs if not str(r.get("explicacion") or "").strip()]
        nreg = int(pv.get("regresiones") or 0)
        fv = int(((pv.get("vigente") or {}).get("FAIL")) or 0)
        fc = int(((pv.get("candidata") or {}).get("FAIL")) or 0)
        vig, cand = pv.get("vigente") or {}, pv.get("candidata") or {}
        if not (sum(int(v or 0) for v in vig.values()) > 0 and sum(int(v or 0) for v in cand.values()) > 0):
            out.append(f"{os.path.basename(f)}: {k}: sin los conteos de la compuerta vigente Y de la candidata (> 0): corrida hecha a mano o "
                       "vacía (BE-PM04)")
        if int(pv.get("sin_explicar") or 0) or sinx or nreg != len(regs) or fc > fv + nreg:
            out.append(f"{os.path.basename(f)}: {k}: regresiones {nreg} / sin explicar {pv.get('sin_explicar') or len(sinx)} / FAIL "
                       f"{fv} -> {fc} no cuadran o están sin explicar")
    pr = x.get("proyectos") or {}
    falt = [a for a in abiertos if a not in pr]
    if falt:
        out.append(f"{os.path.basename(f)}: faltan proyectos abiertos {', '.join(falt)} (PROYECTOS_ABIERTOS.json)")
    sin = [r for r in x.get("regresiones") or [] if not str(r.get("explicacion") or "").strip()]
    if sin or not x.get("ok"):
        out.append(f"{os.path.basename(f)}: {len(sin)} regresión(es) PASS -> FAIL sin explicación: "
                   + ", ".join(f"{r.get('proyecto')}:{r.get('chequeo')}" for r in sin[:10]))
    return out


def fechas_publicacion_skill(txt):
    """BE-XF17: FECHAS_PUBLICACION del compuerta_entrega.py del candidato (literal; resuelve las constantes FECHA_Vnnn del módulo)."""
    import ast
    if not txt:
        return {}
    try:
        mod = ast.parse(txt)
    except SyntaxError:
        return {}
    cons, fechas = {}, {}
    for nd in mod.body:
        if isinstance(nd, ast.Assign) and len(nd.targets) == 1 and isinstance(nd.targets[0], ast.Name):
            nm = nd.targets[0].id
            if isinstance(nd.value, ast.Constant) and isinstance(nd.value.value, str):
                cons[nm] = nd.value.value
            elif nm == "FECHAS_PUBLICACION" and isinstance(nd.value, ast.Dict):
                for k, v in zip(nd.value.keys, nd.value.values):
                    val = v.value if isinstance(v, ast.Constant) else cons.get(getattr(v, "id", ""))
                    if isinstance(k, ast.Constant) and val:
                        fechas[k.value] = val
    return fechas


def commits_publicacion(repo):
    """versión -> hora real (%cI) del commit 'Publica <v>' / '<v> VIGENTE' (el más viejo si hay varios)."""
    import subprocess
    try:
        r = subprocess.run(["git", "-C", repo, "log", "--all", "--format=%cI %s"], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode != 0:
        return None
    out = {}
    for ln in (r.stdout or "").splitlines():
        iso, _, msg = ln.partition(" ")
        m = re.search(r"\bPublica (v81cf\d+)\b", msg) or re.search(r"\b(v81cf\d+) VIGENTE\b", msg)
        if m:
            out[m.group(1)] = iso                       # git log va de nuevo a viejo: queda el más viejo
    return out


def revisar_fechas(fuente, repo, tol_s=60):
    """BE-XF17 (COORDINACIÓN 13-nov 06:13): FECHAS_PUBLICACION = hora REAL del commit de publicación de cada versión (se fija DESPUÉS
    del commit, con git log -1 --format=%cI, nunca antes): una fecha a más de 60 s de su commit 'Publica vX' = FALTA; una versión del
    dict sin commit de publicación = FALTA (salvo la propia candidata, que se publica con este commit)."""
    f = fechas_publicacion_skill(fuente.leer("tools/compuerta_entrega.py"))
    cm = commits_publicacion(repo)
    if cm is None or not f:
        return []
    ver = re.search(r"\*\*VERSION:\s*(v81cf\d+)\*\*", fuente.leer("SKILL.md") or "")
    propia = ver.group(1) if ver else None
    out = []
    for v, iso in sorted(f.items()):
        if v not in cm:
            if v != propia:
                out.append(f"FECHAS_PUBLICACION[{v}] = {iso} y no hay commit 'Publica {v}' en git")
            continue
        try:
            d = abs((datetime.datetime.fromisoformat(iso) - datetime.datetime.fromisoformat(cm[v])).total_seconds())
        except ValueError:
            out.append(f"FECHAS_PUBLICACION[{v}] = '{iso}' no es una fecha ISO")
            continue
        if d > tol_s:
            out.append(f"FECHAS_PUBLICACION[{v}] = {iso} vs commit de publicación {cm[v]} ({d:.0f} s > {tol_s} s): la fecha va DESPUÉS del "
                       "commit, con su hora real (BE-XF17)")
    return out


def revisar_version_skill(candidato):
    """BE-XF19 (COORDINACIÓN 13-nov 21:08; v81cf138b escribió 'v81cf140' en SKILL.md y CE_VERSION_ENTREGA bloqueó la final rev20d de CR):
    antes de publicar, compuerta_entrega.version_fallas DEL CANDIDATO sobre su propio SKILL.md (con la línea **VERSION**) = 0 fallas; si no,
    o si no se puede correr, = falta (bloquea). Corre en un proceso aparte (python3 -I) con las tools del candidato (carpeta o zip)."""
    import subprocess
    import tempfile
    base = candidato
    tmp = None
    if zipfile.is_zipfile(candidato):
        tmp = tempfile.mkdtemp(prefix="vv_skill_")
        zipfile.ZipFile(candidato).extractall(tmp)
        base = tmp
    sk = base if os.path.isfile(os.path.join(base, "SKILL.md")) else os.path.join(base, "take-off-metal-frame-drywall")
    if not os.path.isfile(os.path.join(sk, "SKILL.md")) or not os.path.isfile(os.path.join(sk, "tools", "compuerta_entrega.py")):
        return []                                           # sin SKILL.md / tools: lo cubren revisar_skill / revisar_zip
    cod = ("import sys, re, json; sys.path.insert(0, sys.argv[1] + '/tools'); import compuerta_entrega as CE\n"
           "t = open(sys.argv[1] + '/SKILL.md', encoding='utf-8', errors='ignore').read()\n"
           "m = re.search(r'(?m)^\\*\\*VERSION:\\s*(v\\d+cf\\d+[a-z]?)\\*\\*', t)\n"
           "print(json.dumps(['SKILL.md sin la línea **VERSION: vNcfM**'] if not m else CE.version_fallas(t, m.group(1), {})))")
    try:
        r = subprocess.run([sys.executable, "-I", "-c", cod, sk], capture_output=True, text=True, timeout=300, cwd=tempfile.gettempdir())
        out = json.loads((r.stdout or "").strip().splitlines()[-1]) if r.returncode == 0 and (r.stdout or "").strip() else None
    except (OSError, subprocess.SubprocessError, ValueError, IndexError):
        out = None
    if out is None:
        return ["no se pudo correr compuerta_entrega.version_fallas del candidato sobre su SKILL.md (BE-XF19): no se publica sin esa prueba"]
    return [f"{x} (BE-XF19: version_fallas del candidato ≠ 0; en SKILL.md no va el literal de una versión futura)" for x in out]


HORAS_U202 = 4.0


def revisar_pendientes_u202(fuente, ahora=None, horas=HORAS_U202):
    """U-202 (usuario 13-nov, COORDINACIÓN 22:01): ninguna regla queda 'programa-pendiente' más de 4 h. Cada entrada programa-pendiente del
    registro del candidato lleva 'pendiente_desde' (ISO con zona); sin la fecha, fecha ilegible o más de 4 h = falta (bloquea)."""
    import datetime as _dt
    t = fuente.leer("REGLAS_REGISTRO.json")
    if t is None:
        return []
    ahora = ahora or _dt.datetime.now(_dt.timezone.utc)
    f = []
    for e in json.loads(t).get("reglas") or []:
        if e.get("categoria") != "programa-pendiente":
            continue
        d = str(e.get("pendiente_desde") or "").strip()
        if not d:
            f.append(f"{e['id']}: programa-pendiente sin 'pendiente_desde' (U-202: ISO de cuándo entró la regla)")
            continue
        try:
            desde = _dt.datetime.fromisoformat(d.replace("Z", "+00:00"))
            if desde.tzinfo is None:
                raise ValueError("sin zona")
        except ValueError:
            f.append(f"{e['id']}: 'pendiente_desde' ilegible '{d}' (ISO con zona, U-202)")
            continue
        h = (ahora - desde).total_seconds() / 3600
        if h > horas:
            f.append(f"{e['id']}: programa-pendiente desde {d} = {h:.1f} h > {horas:g} h (U-202): su chequeo + test se escribe y publica ya")
    return f


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
    sk = revisar_skill(Fuente(candidato))
    bc = revisar_banco(archivo)
    od = revisar_ordenes(extra[0] if extra else None)
    vu = revisar_versiones_unicas(archivo)
    pm = revisar_postmortem(extra[0] if extra else os.path.join(os.path.dirname(os.path.abspath(archivo)), "cache_proyectos"))
    tl = tests_sin_llamar(Fuente(candidato))
    pa = revisar_prueba_abiertos(archivo, Fuente(candidato), cache=extra[0] if extra else None)
    fp = revisar_fechas(Fuente(candidato), os.path.dirname(os.path.abspath(archivo)))
    vf = revisar_version_skill(candidato)
    pu = revisar_pendientes_u202(Fuente(candidato))
    for nombre, xs in (("REGISTRO (BE-121)", reg), ("ZIP (U-020)", zp), ("INDICE (U-027)", ix), ("SKILL (BE-87 / BE-VS-11)", sk),
                       ("BANCO (U-043)", bc), ("ORDENES (U-136)", od), ("VERSIONES (BE-144)", vu),
                       ("POSTMORTEM (U-185)", pm), ("TESTS SIN LLAMAR (BE-CR42)", tl), ("PRUEBA ABIERTOS (NO GUARD 3.1)", pa),
                       ("FECHAS DE PUBLICACIÓN (BE-XF17)", fp), ("VERSION DEL SKILL.md (BE-XF19)", vf),
                       ("PENDIENTES > 4 h (U-202)", pu)):
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
